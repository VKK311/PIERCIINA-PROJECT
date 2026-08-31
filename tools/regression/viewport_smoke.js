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
      await page.evaluate(i => {
        const el = document.querySelector(`[data-pms-id="${i}"]`);
        if (el) el.scrollIntoView({ block: 'center', inline: 'center' });
      }, id);
      await page.waitForFunction(i => {
        const im = document.querySelector(`[data-pms-id="${i}"] img`);
        return im && im.complete && im.naturalWidth > 0;
      }, id, { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(250);

      const card = await page.evaluate(i => {
        const el = document.querySelector(`[data-pms-id="${i}"]`);
        if (!el) return null;
        const root = el.closest('article.pms-card') || el;
        const r = root.getBoundingClientRect();
        const im = el.querySelector('img');
        // Cards sit in div.pms-rail, a deliberate horizontal scroller. A card
        // off-screen at rest is the design, so assert that scrolling the rail
        // brings it fully into the rail, and that the rail itself never spills
        // onto the page (page-level overflow is asserted above).
        const rail = root.closest('.pms-rail');
        const rr = rail ? rail.getBoundingClientRect() : null;
        return { natural: im ? im.naturalWidth + 'x' + im.naturalHeight : null,
                 fit: im && getComputedStyle(im).objectFit,
                 x: r.x, w: r.width,
                 inRail: rr ? (r.left >= rr.left - 1 && r.right <= rr.right + 1) : null,
                 railInPage: rr ? (rr.left >= -1 && rr.right <= innerWidth + 1) : null };
      }, id);
      ok(!!card, `${id}: card in ${exp.category}`);
      if (card) {
        ok(card.inRail === true, `${id}: card scrolls fully into the ${exp.category} rail`,
           `x=${Math.round(card.x)} w=${Math.round(card.w)}`);
        ok(card.railInPage === true, `${id}: the rail itself stays inside the viewport`);
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
      ok(pdp.thumbs === exp.frames.length, `${id}: ${exp.frames.length} gallery frames on the PDP`,
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
      out[id] = { price: p.priceEUR, oldPrice: p.oldPriceEUR, selectedBy: p.selectedBy,
                  name: p.name, slug: p.slug, isNew: S.__isProductNew(p),
                  hasComposition: 'composition' in p && p.composition != null,
                  msg: S.buildViberMessage(id, 'ONE SIZE'),
                  url: S.buildViberOrderUrl(id, 'ONE SIZE'),
                  canOrder: S.canOrder(id, 'ONE SIZE') };
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
    ok(f.price === exp.priceEUR, `${id}: price is exactly EUR ${exp.priceEUR}`, 'EUR ' + f.price);
    ok(f.oldPrice === null, `${id}: no old price`);
    ok(f.selectedBy === null, `${id}: selectedBy null`);
    ok(f.hasComposition === !!exp.composition,
       `${id}: ${exp.composition ? 'material published' : 'no material row'}`);
    ok(f.isNew === true, `${id}: counts as NEW IN (newUntil ${exp.newUntil})`);
    ok(f.canOrder === true, `${id}: ONE SIZE orderable`);
    ok(f.msg.includes(f.name), `${id}: Viber message names the product`, f.name);
    ok(/ONE SIZE/i.test(f.msg), `${id}: Viber message states ONE SIZE`);
    ok(f.msg.includes(id), `${id}: Viber message carries the product ID`);
    ok(f.url.startsWith(exp.viberUrl), `${id}: canonical Viber route unchanged`);
    ok(!/\?text=/.test(f.url), `${id}: no ?text= on the Viber URL`);
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
})();
