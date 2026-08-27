#!/usr/bin/env node
/**
 * Browser-level publication regression for one real product.
 *
 *   node tools/regression/product_regression.js tools/regression/expect/PM-031.json \
 *        [PINKMALL.html|PINKMALL_REVIEW_STANDALONE.html] [port]
 *
 * Repository checks (selftest, standalone path scan) prove structure. They do
 * not prove that the file a human opens actually shows the product, so this
 * drives real Chromium against a served copy and asserts what a reviewer would
 * look for: the record, the media, the card, search, the PDP, the order path,
 * and that no previously published product moved.
 *
 * Frames are identified by the SHA-256 of their bytes, never by filename. The
 * portable build inlines every image as a data: URI, so a filename check there
 * would test the harness's assumptions instead of the artifact; hashing works
 * in both builds and additionally proves the inlined bytes ARE the live bytes.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const EXPECT = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const FILE = process.argv[3] || 'PINKMALL.html';
const PORT = process.argv[4] || '8131';
const BASE = `http://127.0.0.1:${PORT}/${FILE}`;

const ID = EXPECT.id;
const NAMES = EXPECT.frames.map(f => f.file);
const LIVE = {};
for (const f of EXPECT.frames) LIVE[f.sha256] = f.file;

let pass = 0, fail = 0;
const ok  = (n, x) => { pass++; console.log(`  PASS  ${n}${x ? '  — ' + x : ''}`); };
const bad = (n, x) => { fail++; console.log(`  FAIL  ${n}${x ? '  — ' + x : ''}`); };
const is  = (c, n, x) => c ? ok(n, x) : bad(n, x);

(async () => {
  const browser = await chromium.launch({ executablePath: EXPECT.chromium
    || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
  const page = await ctx.newPage();

  // Every 4xx is recorded WITH its URL. A bare console "404" carries no URL, so
  // without this correlation an intermittent miss is unattributable.
  const consoleErrors = [], failedReqs = [], badResponses = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => consoleErrors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => failedReqs.push(r.url() + ' :: ' + (r.failure() || {}).errorText));
  page.on('response', r => { if (r.status() >= 400) badResponses.push(r.status() + ' ' + r.url()); });

  await page.addInitScript(() => {
    try { localStorage.setItem('pierciina_consent_v1', JSON.stringify(
      { v: 1, analytics: true, marketing: true, ts: Date.now() })); } catch (e) {}
  });
  await page.goto(BASE, { waitUntil: 'networkidle' });

  await page.addScriptTag({ content: `
    window.__frameName = async function (src, live) {
      if (!src) return null;
      const buf = await (await fetch(src)).arrayBuffer();
      const h = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', buf)))
                     .map(b => b.toString(16).padStart(2, '0')).join('');
      return live[h] || ('UNKNOWN:' + h.slice(0, 12));
    };` });
  const nameOf = (src) => page.evaluate(([s, l]) => window.__frameName(s, l), [src, LIVE]);

  console.log(`\n== load (${FILE}) ==`);
  // fonts.googleapis.com is reset by this container's egress proxy, identically
  // on builds that predate the product. Environment fact, not a product defect.
  const isFont = u => /fonts\.(googleapis|gstatic)\.com/.test(u);
  const realFails = failedReqs.filter(u => !isFont(u));
  const fontBlocked = failedReqs.length - realFails.length;
  const favicons = badResponses.filter(r => /favicon/i.test(r));
  const realBad  = badResponses.filter(r => !/favicon/i.test(r));
  const realErrors = consoleErrors.filter(t =>
    !/ERR_CONNECTION_RESET/.test(t) && !(/404/.test(t) && !realBad.length));
  is(realErrors.length === 0, 'no console errors beyond blocked fonts/favicon',
     realErrors.slice(0, 3).join(' | '));
  is(realFails.length === 0, 'no failed requests beyond the blocked font CDN',
     realFails.slice(0, 3).join(' | ') || `${fontBlocked} font request(s) blocked by the proxy`);
  is(realBad.length === 0, 'no 4xx/5xx beyond favicon', realBad.slice(0, 5).join(' | ')
     || (favicons.length ? `favicon only: ${favicons[0]}` : ''));

  console.log('\n== catalogue ==');
  const cat = await page.evaluate((id) => {
    const p = window.PinkMallStore.products;
    return { count: p.length, ids: p.map(x => x.id),
             dupIds: p.map(x => x.id).filter((v, i, a) => a.indexOf(v) !== i),
             dupSlugs: p.map(x => x.slug).filter((v, i, a) => a.indexOf(v) !== i),
             target: p.find(x => x.id === id) || null };
  }, ID);
  is(cat.count === EXPECT.catalogueSize, `catalogue holds ${EXPECT.catalogueSize} products`, 'count=' + cat.count);
  is(cat.dupIds.length === 0, 'no duplicate ids', cat.dupIds.join(','));
  is(cat.dupSlugs.length === 0, 'no duplicate slugs', cat.dupSlugs.join(','));

  console.log(`\n== ${ID} record ==`);
  const p = cat.target;
  if (!p) { bad(`${ID} exists`); await browser.close(); process.exit(1); }
  ok(`${ID} exists`);
  is(p.brand === EXPECT.brand, 'brand', p.brand);
  is(p.manufacturerItemNo === EXPECT.manufacturerItemNo, 'manufacturer item', p.manufacturerItemNo);
  is(p.name === EXPECT.name, 'model name', p.name);
  is(p.category === EXPECT.category && p.subcategory === EXPECT.subcategory,
     `${EXPECT.category} > ${EXPECT.subcategory}`, p.category + '/' + p.subcategory);
  is(p.color === EXPECT.color, 'public colour', p.color);
  is(p.priceEUR === EXPECT.priceEUR, `price €${EXPECT.priceEUR}`, String(p.priceEUR));
  is(p.oldPriceEUR === null, 'oldPriceEUR null — no SALE');
  is(p.selectedBy === null, 'selectedBy null');
  is(!('composition' in p) || p.composition == null, 'composition omitted');
  is(p.inventoryMode === 'availability', 'inventoryMode availability');
  is(p.newUntil === EXPECT.newUntil, 'newUntil = publication + 14d', p.newUntil);
  const sizes = Object.keys(p.availability);
  is(JSON.stringify(sizes) === JSON.stringify(EXPECT.sizes), 'sizes ' + EXPECT.sizes.join(','), sizes.join(','));
  is(Object.values(p.availability).every(v => v === 'available'),
     'every size available — no sold-out asserted');
  is(p.media.fit === 'contain', 'media.fit contain');
  is(EXPECT.surface === null ? !('surface' in p.media) : p.media.surface === EXPECT.surface,
     'media.surface', String(p.media.surface));
  is(p.media.gallery.length === NAMES.length - 1 && !!p.media.image, `1 main + ${NAMES.length - 1} gallery`);
  is(p.media.galleryAlt.length === p.media.gallery.length, 'galleryAlt count matches gallery');
  is(!!p.media.imageAlt && /[А-Яа-я]/.test(p.media.imageAlt), 'imageAlt is Bulgarian', p.media.imageAlt);

  const order = [];
  for (const u of [p.media.image].concat(p.media.gallery)) order.push(await nameOf(u));
  is(JSON.stringify(order) === JSON.stringify(NAMES),
     'approved positional order, by content hash', order.join(' → '));

  console.log('\n== media resolve ==');
  for (const u of [p.media.image].concat(p.media.gallery)) {
    const r = await page.evaluate(async (rel) => {
      const res = await fetch(rel);
      if (!res.ok) return { ok: false, status: res.status };
      const b = await res.blob();
      const bmp = await createImageBitmap(b);
      return { ok: true, bytes: b.size, w: bmp.width, h: bmp.height, type: b.type };
    }, u);
    is(r.ok && r.bytes > 5000 && r.w === EXPECT.nativeWidth && r.h === EXPECT.nativeHeight,
       `native ${EXPECT.nativeWidth}×${EXPECT.nativeHeight}: ` + (await nameOf(u)),
       r.ok ? `${r.bytes}B ${r.w}×${r.h} ${r.type}` : 'status ' + r.status);
  }

  console.log('\n== card in grid ==');
  await page.evaluate(c => window.PinkMallStore.setFilters({ category: c, query: '' }), EXPECT.category);
  await page.waitForTimeout(400);
  await page.evaluate(id => {
    const el = document.querySelector(`[data-pms-id="${id}"]`);
    if (el) el.scrollIntoView({ block: 'center' });          // loading="lazy"
  }, ID);
  // Wait on the decode itself; a fixed sleep made this flake under load.
  await page.waitForFunction(id => {
    const img = document.querySelector(`[data-pms-id="${id}"] img`);
    return img && img.complete && img.naturalWidth > 0;
  }, ID, { timeout: 20000 }).catch(() => {});
  const card = await page.evaluate(id => {
    const el = document.querySelector(`[data-pms-id="${id}"]`);
    if (!el) return null;
    const root = el.closest('article.pms-card');
    const img = el.querySelector('img');
    return { src: img && img.getAttribute('src'), alt: img && img.getAttribute('alt'),
             natural: img && [img.naturalWidth, img.naturalHeight],
             objectFit: img && getComputedStyle(img).objectFit,
             text: root ? root.innerText.replace(/\s+/g, ' ').trim() : '' };
  }, ID);
  is(!!card, `${ID} card rendered in ${EXPECT.category}`);
  if (card) {
    is(await nameOf(card.src) === NAMES[0], 'card shows MAIN', await nameOf(card.src));
    is(card.natural && card.natural[0] === EXPECT.nativeWidth, 'card image decoded', String(card.natural));
    is(card.alt === p.media.imageAlt, 'card alt is the authored Bulgarian', card.alt);
    is(card.objectFit === 'contain', 'card fit contain', card.objectFit);
    is(new RegExp(String(EXPECT.priceEUR)).test(card.text), `card shows €${EXPECT.priceEUR}`);
    is(/NEW|НОВО/i.test(card.text), 'NEW badge shown');
  }

  console.log('\n== search ==');
  for (const q of EXPECT.searchTerms) {
    const hit = await page.evaluate(([query, id]) => {
      window.PinkMallStore.clearFilters();
      return (window.PinkMallStore.search(query) || []).some(x => x.id === id);
    }, [q, ID]);
    is(hit, `search "${q}" finds ${ID}`);
  }

  console.log('\n== PDP ==');
  await page.evaluate(id => { window.PinkMallStore.clearFilters(); window.PinkMallStore.openProduct(id); }, ID);
  await page.waitForTimeout(700);
  const pdp = await page.evaluate(() => {
    const s = document.querySelector('#pmsSheet');
    return { open: !!s && s.offsetHeight > 0,
             text: s ? s.innerText.replace(/\s+/g, ' ').trim() : '',
             imgs: s ? Array.from(s.querySelectorAll('img')).map(i => ({
               rawSrc: i.getAttribute('src') || '', alt: i.getAttribute('alt'),
               parent: (i.parentElement.className || '').toString().trim(),
               fit: getComputedStyle(i).objectFit })) : [] };
  });
  is(pdp.open, 'PDP opened');
  is(pdp.text.includes(EXPECT.name), 'PDP shows the model name');
  is(pdp.text.includes(EXPECT.brand), 'PDP shows the brand');
  is(new RegExp(String(EXPECT.priceEUR)).test(pdp.text), `PDP shows €${EXPECT.priceEUR}`);
  for (const sz of EXPECT.sizes) {
    is(new RegExp('(^|\\s)' + sz.replace('.', '\\.') + '(\\s|$)').test(pdp.text), `PDP offers size ${sz}`);
  }
  is(!/Състав|Материал/i.test(pdp.text), 'PDP renders no material row');
  is(!/изчерпан|sold ?out/i.test(pdp.text), 'PDP asserts no sold-out size');
  const liveNames = new Set(NAMES);
  const pdpMedia = [];
  for (const i of pdp.imgs) {
    const n = await nameOf(i.rawSrc);
    if (liveNames.has(n)) pdpMedia.push(Object.assign({}, i, { name: n }));
  }
  is(new Set(pdpMedia.map(i => i.name)).size === NAMES.length, `PDP carries all ${NAMES.length} frames`,
     String(new Set(pdpMedia.map(i => i.name)).size));
  is(pdpMedia.every(i => i.fit === 'contain'), 'PDP media fit contain');
  const hero = pdpMedia.find(i => i.parent === 'pms-detail-main');
  is(!!hero && (hero.alt || '').length > 10, 'PDP hero carries the authored alt');
  is(pdpMedia.filter(i => /pms-thumb/.test(i.parent)).every(i => i.alt === ''),
     'thumbnails are decorative (alt="")');
  is(pdpMedia[0] && pdpMedia[0].name === NAMES[0], 'MAIN leads the PDP gallery',
     pdpMedia.map(i => i.name).join(' → '));

  console.log('\n== every authored alt reaches the hero ==');
  const nThumb = await page.evaluate(() => document.querySelectorAll('#pmsSheet .pms-thumb').length);
  is(nThumb === NAMES.length, `${NAMES.length} thumbnails`, String(nThumb));
  const wantAlt = [p.media.imageAlt].concat(p.media.galleryAlt);
  for (let i = 0; i < nThumb; i++) {
    await page.evaluate(k => document.querySelectorAll('#pmsSheet .pms-thumb')[k].click(), i);
    await page.waitForTimeout(300);
    const h = await page.evaluate(() => {
      const el = document.querySelector('#pmsSheet .pms-detail-main img');
      return { rawSrc: el.getAttribute('src') || '', alt: el.getAttribute('alt') };
    });
    const nm = await nameOf(h.rawSrc);
    is(nm === NAMES[i] && h.alt === wantAlt[i], `frame ${i} is ${NAMES[i]} with its authored alt`, h.alt);
  }

  console.log('\n== order path ==');
  const ord = await page.evaluate(([id, sz]) => {
    const S = window.PinkMallStore;
    return { can: S.canOrder(id, sz), url: S.buildViberOrderUrl(id, sz), msg: S.buildViberMessage(id, sz) };
  }, [ID, EXPECT.sizes[1]]);
  is(ord.can === true, `size ${EXPECT.sizes[1]} is orderable`);
  is((ord.url || '').startsWith(EXPECT.viberUrl), 'Viber destination unchanged', ord.url);
  is(!/\?text=/.test(ord.url || ''), 'no ?text= appended to the Viber URL');
  is(new RegExp(ID).test(ord.msg || ''), 'order message names the product');

  console.log('\n== delivery + integrity ==');
  is(/4\s*[–-]\s*7\s*работни дни/.test(pdp.text), 'delivery reads 4–7 работни дни');
  const junior = await page.evaluate(() =>
    /\b(kids?|junior|jr\.?|youth|girls?|boys?)\b/i.test(document.body.innerText));
  is(!junior, 'no child/junior marker anywhere in rendered text');

  console.log('\n== previously published products untouched ==');
  const others = await page.evaluate(async (ids) => {
    const S = window.PinkMallStore;
    S.closeProduct && S.closeProduct();
    const out = [];
    for (const id of ids) {
      const q = S.getProduct(id);
      const r = await fetch(q.media.image);
      out.push({ id, ok: r.ok, sizes: Object.keys(q.availability || q.inventory || {}).length });
    }
    return out;
  }, EXPECT.priorProducts);
  for (const o of others) is(o.ok && o.sizes > 0, `${o.id} untouched`,
    `main ${o.ok ? 'resolves' : 'MISSING'}, ${o.sizes} sizes`);

  console.log('\n== sort ==');
  const sorted = await page.evaluate(c => {
    window.PinkMallStore.clearFilters();
    return (window.PinkMallStore.setFilters({ category: c, sort: 'price-asc' }) || [])
      .map(x => [x.id, x.priceEUR]);
  }, EXPECT.category);
  const idx = sorted.findIndex(x => x[0] === ID);
  const monotonic = sorted.every((x, i) => i === 0 || sorted[i - 1][1] <= x[1]);
  is(idx >= 0 && monotonic, `price-asc sort places ${ID} correctly`,
     sorted.map(x => x[0] + ':' + x[1]).join(' '));

  await browser.close();
  console.log(`\nREGRESSION (${FILE}): ${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR', e); process.exit(2); });
