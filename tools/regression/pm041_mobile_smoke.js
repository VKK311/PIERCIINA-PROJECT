#!/usr/bin/env node
const { chromium } = require('playwright');
const file = process.argv[2] || 'PINKMALL.html';
const port = process.argv[3] || '8131';
const viewports = [[375,667],[390,844],[430,932],[768,1024],[1024,768],[1366,768],[1440,900],[1920,1080]];

(async () => {
  const browser = await chromium.launch();
  let failed = false;
  for (const [width,height] of viewports) {
    const ctx = await browser.newContext({ viewport: { width, height } });
    const page = await ctx.newPage();
    await page.addInitScript(() => {
      try { localStorage.setItem('pierciina_consent_v1', JSON.stringify({v:1,analytics:true,marketing:true,ts:Date.now()})); } catch(e) {}
    });
    await page.goto(`http://127.0.0.1:${port}/${file}`, { waitUntil: 'networkidle' });
    const base = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: innerWidth }));
    if (base.sw > base.iw + 1) {
      console.error(`FAIL ${width}x${height}: page overflow ${base.sw}>${base.iw}`); failed = true;
    }
    await page.evaluate(() => { window.PinkMallStore.clearFilters(); window.PinkMallStore.openProduct('PM-041'); });
    await page.waitForTimeout(350);
    const pdp = await page.evaluate(() => {
      const sheet = document.querySelector('#pmsSheet');
      const img = sheet && sheet.querySelector('img');
      const r = sheet && sheet.getBoundingClientRect();
      return {
        open: !!sheet && sheet.offsetHeight > 0,
        overflow: document.documentElement.scrollWidth > innerWidth + 1,
        left: r ? r.left : 0,
        right: r ? r.right : 0,
        imageOk: !!img && img.complete && img.naturalWidth === 1000 && img.naturalHeight === 455
      };
    });
    if (!pdp.open || pdp.overflow || pdp.left < -1 || pdp.right > width + 1 || !pdp.imageOk) {
      console.error(`FAIL ${width}x${height}:`, pdp); failed = true;
    } else {
      console.log(`PASS ${width}x${height}`);
    }
    await ctx.close();
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
