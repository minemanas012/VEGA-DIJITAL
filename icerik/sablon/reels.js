// Kullanım: node reels.js <reels.html> <çıktı.mp4> [stills t1 t2 ...]
// Sayfadaki render(t) fonksiyonunu 30 fps kare kare çalıştırıp 1080x1920 MP4 üretir (sessiz).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [html, out, mode, ...ts] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  if (mode === 'stills') {
    for (const t of ts) { await p.evaluate(t => render(+t), t); await p.screenshot({ path: `${out}_${t}.png` }); }
  } else {
    const fps = 30, dur = await p.evaluate(() => DUR), N = Math.round(fps * dur);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => render(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log(N, 'kare ->', out);
  }
  await b.close();
})();
