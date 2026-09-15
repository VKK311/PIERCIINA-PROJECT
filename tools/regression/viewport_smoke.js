#!/usr/bin/env node
/**
 * Viewport + storefront-behaviour smoke for one or more published products.
 *
 *   node tools/regression/viewport_smoke.js PM-042,PM-043,PM-044 \
 *        [PINKMALL.html|PINKMALL_REVIEW_STANDALONE.html] [port]
 *
 * product_regression.js proves one product's record, media and PDP in a single
 * desktop window. This covers what that cannot: the same products across the
 * phone/tablet/desktop widths a customer actually uses, plus the storefront
 * behaviours that are shared rather than per-record — wishlist, the Viber order
 * message, NEW IN, price order and the category filter.
 *
 * Expectations are read from tools/regression/expect/<ID>.json, so this file
 * carries no product knowledge and needs no edit when a product is published.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const IDS = (process.argv[2] || '').split(',').map(s => s.trim()).filter(Boolean);
const FILE = process.argv[3] || 'PINKMALL.html';
const PORT = process.argv[4] || '8151';
if (!IDS.length) { console.error('usage: viewport_smoke.js PM-0xx[,PM-0yy] [file] [port]'); process.exit(2); }

const EXPECT = {};
for (const id of IDS) {
  EXPECT[id] = JSON.parse(fs.readFileSync(
    path.join(__dirname, 'expect', id + '.json'), 'utf8'));
}

// Phone, large phone, tablet, laptop, desktop.
const VIEWPORTS = [[375,667],[390,844],[430,932],[768,1024],[1366,768],[1920,1080]];

// ── Canonical freshness rule, re-implemented test-side ──────────────────
// Mirrors isProductNew() in PINKMALL.html: a parseable newUntil wins and is
// INCLUSIVE through 23:59:59 local time on that date; raw isNew is only the
// fallback. Implemented here rather than called from the store so that the
// expectation is derived from product data, not from the code under test.
const expectedNew = (prod, now = Date.now()) => {
  if (prod && prod.newUntil) {
    const until = Date.parse(prod.newUntil + 'T23:59:59');
    if (isFinite(until)) return now <= until;
  }
  return !!(prod && prod.isNew);
};

let fail = 0;
const ok = (c, m, d) => { if (!c) fail++; console.log((c ? '  PASS  ' : '  FAIL  ') + m + (d ? '  — ' + d : '')); };

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const newCtx = async (viewport) => {
    const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2 });
    await ctx.addInitScript(() => {
      try { localStorage.setItem('pierciina_consent_v1', JSON.stringify(
        { v: 1, analytics: true, marketing: true, ts: Date.now() })); } catch (e) {}
    });
    return ctx;
  };

  for (const [width, height] of VIEWPORTS) {
    const ctx = await newCtx({ width, height });
    const page = await ctx.newPage();
    await page.goto(`http://127.0.0.1:${PORT}/${FILE}`, { waitUntil: 'networkidle' });
    console.log(`\n== ${FILE} @ ${width}x${height} ==`);
    ok((await page.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth)) <= 1,
      'grid page: no horizontal overflow');

    for (const id of IDS) {
      const exp = EXPECT[id];
      const native = `${exp.nativeWidth}x${exp.nativeHeight}`;
      await page.evaluate(c => window.PinkMallStore.setFilters({ category: c, query: '' }), exp.category);
      await page.waitForTimeout(300);
      // Scope to the filtered shop grid. A product also renders in #pmsNewRail
      // while it is NEW, and that rail sits earlier in the document, so an
      // unscoped querySelector silently changes which node it measures the day
      // a product stops being NEW. Scoping keeps this assertion about the
      // category grid regardless of freshness.
      await page.evaluate(i => {
        const el = document.querySelector(`#pmsShopGrid [data-pms-id="${i}"]`)
                || document.querySelector(`[data-pms-id="${i}"]`);
        if (el) el.scrollIntoView({ block: 'center', inline: 'center' });
      }, id);
      await page.waitForFunction(i => {
        const im = document.querySelector(`#pmsShopGrid [data-pms-id="${i}"] img`)
                || document.querySelector(`[data-pms-id="${i}"] img`);
        return im && im.complete && im.naturalWidth > 0;
      }, id, { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(250);

      const card = await page.evaluate(i => {
        const el = document.querySelector(`#pmsShopGrid [data-pms-id="${i}"]`)
                || document.querySelector(`[data-pms-id="${i}"]`);
        if (!el) return null;
        const root = el.closest('article.pms-card') || el;
        const r = root.getBoundingClientRect();
        const im = el.querySelector('img');
        // A card lives either in div.pms-rail (a deliberate horizontal
        // scroller, where being off-screen at rest is the design) or in the
        // div.pms-grid of the filtered shop. Measure against whichever
        // container actually holds it, and name it, so a layout failure says
        // which surface broke instead of dereferencing null.
        const rail = root.closest('.pms-rail');
        const grid = root.closest('.pms-grid');
        const box  = rail || grid;
        const rr   = box ? box.getBoundingClientRect() : null;
        return { natural: im ? im.naturalWidth + 'x' + im.naturalHeight : null,
                 fit: im && getComputedStyle(im).objectFit,
                 x: r.x, w: r.width,
                 container: rail ? 'rail' : (grid ? 'grid' : 'none'),
                 inContainer: rr ? (r.left >= rr.left - 1 && r.right <= rr.right + 1) : null,
                 containerInPage: rr ? (rr.left >= -1 && rr.right <= innerWidth + 1) : null };
      }, id);
      ok(!!card, `${id}: card in ${exp.category}`);
      if (card) {
        ok(card.container !== 'none', `${id}: card sits in a known layout container`,
           `container=${card.container}`);
        ok(card.inContainer === true,
           `${id}: card scrolls fully into the ${exp.category} ${card.container}`,
           `x=${Math.round(card.x)} w=${Math.round(card.w)} container=${card.container}`);
        ok(card.containerInPage === true,
           `${id}: the ${card.container} itself stays inside the viewport`);
        ok(card.natural === native, `${id}: card image native ${native}`, card.natural);
        ok(card.fit === 'contain', `${id}: card fit contain`, card.fit);
      }

      await page.evaluate(i => {
        window.PinkMallStore.clearFilters(); window.PinkMallStore.openProduct(i);
      }, id);
      await page.waitForTimeout(700);
      const pdp = await page.evaluate(() => {
        const s = document.querySelector('#pmsSheet');
        const hero = document.querySelector('#pmsSheet .pms-detail-main img');
        return { open: !!s && s.offsetHeight > 0,
                 ovf: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                 thumbs: document.querySelectorAll('#pmsSheet .pms-thumb').length,
                 heroFit: hero ? getComputedStyle(hero).objectFit : null,
                 heroNatural: hero ? hero.naturalWidth + 'x' + hero.naturalHeight : null,
                 text: s ? s.innerText : '' };
      });
      ok(pdp.open, `${id}: PDP opens`);
      ok(pdp.ovf <= 1, `${id}: PDP no horizontal overflow`, 'ovf=' + pdp.ovf);
      // detailMediaHTML() sets multi = imgs.length > 1 and renders the thumb
      // strip only when multi, so a single-frame product correctly shows no
      // thumbnails. PM-041 is the owner-approved one-image exception; the
      // expectation is derived from the frame count rather than assuming
      // every product has a multi-image gallery.
      const wantThumbs = exp.frames.length > 1 ? exp.frames.length : 0;
      ok(pdp.thumbs === wantThumbs,
         `${id}: ${wantThumbs} gallery thumbnails on the PDP for ${exp.frames.length} frame(s)`,
         'thumbs=' + pdp.thumbs);
      ok(pdp.heroFit === 'contain', `${id}: PDP hero contain`, pdp.heroFit);
      ok(pdp.heroNatural === native, `${id}: PDP hero native ${native}`, pdp.heroNatural);
      for (const sz of exp.sizes) ok(pdp.text.includes(sz), `${id}: size ${sz} shown`);
    }
    await ctx.close();
  }

  // Shared storefront behaviour. Width-independent, so one window is enough.
  const ctx = await newCtx({ width: 1366, height: 768 });
  const page = await ctx.newPage();
  await page.goto(`http://127.0.0.1:${PORT}/${FILE}`, { waitUntil: 'networkidle' });
  console.log(`\n== ${FILE} storefront behaviour ==`);

  const cat = await page.evaluate(ids => {
    const S = window.PinkMallStore, out = {};
    for (const id of ids) {
      const p = S.products.find(x => x.id === id);
      // A fixture naming a product the catalogue no longer carries is a real
      // finding. Record it and move on rather than throwing inside the page.
      if (!p) { out[id] = { missing: true }; continue; }
      // The order path must be exercised with a size the product actually
      // has. Hard-coding 'ONE SIZE' silently broke every product with real
      // sizes (PM-031 is 36-40): resolveOrder() rejected the size, so
      // buildViberOrderUrl() returned null and the suite died on a
      // TypeError instead of reporting a failure. Take the size from the
      // product's own availability/inventory bag and keep only sizes the
      // store does not consider sold out; ONE SIZE products still pick
      // 'ONE SIZE' naturally because that is the only key they carry.
      const bag = S.__isAvailabilityMode(p) ? p.availability : p.inventory;
      const allSizes = bag ? Object.keys(bag) : [];
      const sellable = allSizes.filter(sz => S.__sizeState(p, sz) !== 'soldout');
      const size = sellable.length ? sellable[0] : null;
      out[id] = { price: p.priceEUR, oldPrice: p.oldPriceEUR, selectedBy: p.selectedBy,
                  name: p.name, slug: p.slug,
                  isNew: S.__isProductNew(p),
                  newUntil: p.newUntil === undefined ? null : p.newUntil,
                  rawIsNew: !!p.isNew,
                  inNewRail: !!document.querySelector(`#pmsNewRail [data-pms-id="${id}"]`),
                  allSizes, sellable, size,
                  hasComposition: 'composition' in p && p.composition != null,
                  msg: size === null ? null : S.buildViberMessage(id, size),
                  url: size === null ? null : S.buildViberOrderUrl(id, size),
                  canOrder: size === null ? null : S.canOrder(id, size) };
      S.toggleWishlist(id); out[id].wishOn = S.isWishlisted(id);
      S.toggleWishlist(id); out[id].wishOff = !S.isWishlisted(id);
    }
    out.__ids = S.products.map(x => x.id);
    out.__slugs = S.products.map(x => x.slug);
    out.__sorted = S.products.filter(x => ids.includes(x.id))
                             .sort((a, b) => a.priceEUR - b.priceEUR).map(x => x.id);
    return out;
  }, IDS);

  const any = EXPECT[IDS[0]];
  ok(cat.__ids.length === any.catalogueSize, `catalogue holds ${any.catalogueSize} products`,
     'n=' + cat.__ids.length);
  ok(cat.__ids.filter((v, i, a) => a.indexOf(v) !== i).length === 0, 'no duplicate ids');
  ok(cat.__slugs.filter((v, i, a) => a.indexOf(v) !== i).length === 0, 'no duplicate slugs');

  for (const id of IDS) {
    const exp = EXPECT[id], f = cat[id];
    if (!f || f.missing) {
      ok(false, `${id}: product present in the catalogue`,
         f && f.missing ? 'not found in PinkMallStore.products' : 'no data collected');
      continue;
    }
    ok(f.price === exp.priceEUR, `${id}: price is exactly EUR ${exp.priceEUR}`, 'EUR ' + f.price);
    ok(f.oldPrice === null, `${id}: no old price`);
    ok(f.selectedBy === null, `${id}: selectedBy null`);
    ok(f.hasComposition === !!exp.composition,
       `${id}: ${exp.composition ? 'material published' : 'no material row'}`);
    // Freshness expectation derived from the product's own data, then checked
    // against both the store's verdict and NEW IN rail membership. Expired
    // products are expected to be absent, not expected to still be NEW.
    const wantNew = expectedNew({ newUntil: f.newUntil, isNew: f.rawIsNew });
    ok(f.isNew === wantNew,
       `${id}: freshness matches the catalogue rule (newUntil ${f.newUntil || 'none'}, isNew ${f.rawIsNew})`,
       `store=${f.isNew} want=${wantNew}`);
    ok(f.inNewRail === wantNew,
       `${id}: ${wantNew ? 'present in' : 'absent from'} the NEW IN rail`,
       `inRail=${f.inNewRail}`);

    // Order path, on a size the product really has.
    ok(f.size !== null, `${id}: has at least one sellable size`,
       `sizes=[${f.allSizes.join(',')}] sellable=[${f.sellable.join(',')}]`);
    ok(exp.sizes.includes(f.size), `${id}: chosen size ${f.size} is one the fixture declares`,
       `fixture=[${exp.sizes.join(',')}]`);
    ok(f.canOrder === true, `${id}: size ${f.size} orderable`, `canOrder=${f.canOrder}`);
    // Guarded: a null message/url is a FAIL with context, never a crash.
    if (f.msg === null || typeof f.msg !== 'string') {
      ok(false, `${id}: Viber message built for size ${f.size}`, `msg=${JSON.stringify(f.msg)}`);
    } else {
      ok(f.msg.includes(f.name), `${id}: Viber message names the product`, f.name);
      ok(f.msg.includes(f.size), `${id}: Viber message states size ${f.size}`, f.msg);
      ok(f.msg.includes(id), `${id}: Viber message carries the product ID`);
    }
    if (typeof f.url !== 'string' || !f.url) {
      ok(false, `${id}: Viber order URL built for size ${f.size}`, `url=${JSON.stringify(f.url)}`);
    } else {
      ok(f.url.startsWith(exp.viberUrl), `${id}: canonical Viber route unchanged`, f.url);
      // CONFIG.viberUrl is an https business link, and supportsPrefill() only
      // accepts viber: deep links, so no prefill is appended.
      ok(!/\?text=/.test(f.url), `${id}: no ?text= on the Viber URL`);
    }
    ok(f.wishOn && f.wishOff, `${id}: wishlist add and remove both work`);
  }

  const byPrice = IDS.slice().sort((a, b) => EXPECT[a].priceEUR - EXPECT[b].priceEUR);
  ok(JSON.stringify(cat.__sorted) === JSON.stringify(byPrice), 'price sort orders the batch',
     cat.__sorted.map(i => `${i}:${EXPECT[i].priceEUR}`).join(' < '));

  for (const id of IDS) {
    const hit = await page.evaluate(([c, i]) => {
      window.PinkMallStore.setFilters({ category: c, query: '' });
      return (window.PinkMallStore.getResults() || []).some(x => x.id === i);
    }, [EXPECT[id].category, id]);
    ok(hit, `${id}: ${EXPECT[id].category} filter returns it`);
  }

  await ctx.close();
  await browser.close();
  console.log(`\nVIEWPORT SMOKE (${FILE}): ${fail ? fail + ' FAILED' : 'all passed'}`);
  process.exit(fail ? 1 : 0);
})().catch(e => {
  // Exit 1 means the storefront failed an assertion; exit 2 means the harness
  // itself broke. Collapsing the two hides product defects behind stack
  // traces, which is exactly how the ONE SIZE assumption stayed invisible.
  console.error('HARNESS CRASH', e && e.stack ? e.stack : e);
  process.exit(2);
});
