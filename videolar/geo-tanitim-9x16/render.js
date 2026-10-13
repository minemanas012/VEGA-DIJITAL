const { chromium } = require(process.env.PW || 'playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const mode = process.argv[2]; // 'stills' or 'video'
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve('scene.html'));
  if (mode === 'stills') {
    const ts = process.argv.slice(3).map(Number);
    for (const t of ts) { await page.evaluate(t => render(t), t); await page.screenshot({ path: `still_${t}.png` }); }
  } else {
    const fps = 30, dur = 40.6, out = process.argv[3] || 'silent.mp4';
    const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',out], { stdio: ['pipe','inherit','inherit'] });
    const N = Math.round(fps * dur);
    for (let i = 0; i < N; i++) {
      await page.evaluate(t => render(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
