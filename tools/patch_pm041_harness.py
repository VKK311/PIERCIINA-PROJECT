#!/usr/bin/env python3
from pathlib import Path

p = Path('tools/regression/product_regression.js')
s = p.read_text(encoding='utf-8')
old = '''  console.log('\\n== every authored alt reaches the hero ==');
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
'''
new = '''  console.log('\\n== every authored alt reaches the hero ==');
  const nThumb = await page.evaluate(() => document.querySelectorAll('#pmsSheet .pms-thumb').length);
  // The storefront intentionally suppresses the thumbnail rail for a one-image
  // product. Multi-image products still expose one thumbnail per frame.
  const expectedThumbs = NAMES.length > 1 ? NAMES.length : 0;
  is(nThumb === expectedThumbs, `${expectedThumbs} thumbnails for ${NAMES.length} frame(s)`, String(nThumb));
  const wantAlt = [p.media.imageAlt].concat(p.media.galleryAlt);
  if (NAMES.length === 1) {
    const h = await page.evaluate(() => {
      const el = document.querySelector('#pmsSheet .pms-detail-main img');
      return { rawSrc: el.getAttribute('src') || '', alt: el.getAttribute('alt') };
    });
    const nm = await nameOf(h.rawSrc);
    is(nm === NAMES[0] && h.alt === wantAlt[0], `single frame is ${NAMES[0]} with its authored alt`, h.alt);
  } else {
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
  }
'''
if old not in s:
    if 'expectedThumbs = NAMES.length > 1 ? NAMES.length : 0' in s:
        print('harness already patched')
    else:
        raise SystemExit('regression harness target block not found')
else:
    p.write_text(s.replace(old, new, 1), encoding='utf-8')
    print('patched product_regression.js for one-image PDPs')
