// Kullanım: node render.js <html> <çıktı-klasörü>
// HTML'deki her .slide ayrı PNG olarak kaydedilir (dosya adı: data-name ya da sıra no).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [html, out] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const els = await p.$$('.slide');
  for (let i = 0; i < els.length; i++) {
    const name = (await els[i].getAttribute('data-name')) || String(i + 1).padStart(2, '0');
    await els[i].screenshot({ path: path.join(out, name + '.png') });
  }
  console.log(els.length, 'görsel ->', out);
  await b.close();
})();
