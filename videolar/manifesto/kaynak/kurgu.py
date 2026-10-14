"""Vega Dijital — manifesto videosu kurgusu.
Girdi: ../calisma.mkv (1080x1920 çalışma kopyası), timeline.json, gf/ (grafik kareleri), sfx.
Çıktı: cikti.mp4 (altyazısız 1080x1920 30fps)."""
import json, os, subprocess, numpy as np, cv2, wave

FPS = 30
W, H = 1080, 1920
AX, AY = 540, 600          # zoom merkezi: yüz
TL = json.load(open('timeline.json'))
END = TL[-1]['out'][1]     # 46.81
OUTRO = 2.0
TOTAL = END + OUTRO
N = int(round(TOTAL * FPS))

def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

# Kamera planı: (başlangıç, bitiş, ölçek_başı, ölçek_sonu) segment içi yavaş hareket
# + anlık punch-in/zoom-out olayları
BASE = [
    (0.00, 5.63, 1.00, 1.05),
    (5.63, 8.59, 1.00, 1.04),
    (8.59, 12.95, 1.12, 1.16),
    (12.95, 17.39, 1.00, 1.03),
    (17.39, 20.95, 1.08, 1.10),
    (20.95, 24.02, 1.00, 1.05),
    (24.02, 26.65, 1.12, 1.14),
    (26.65, 35.42, 1.00, 1.08),
    (35.42, 37.31, 1.00, 1.00),
    (37.31, 40.57, 1.15, 1.18),
    (40.57, END, 1.00, 1.10),
]
# (zaman, ek ölçek, giriş süresi) — punch-in: hızlı giriş, segment sonuna kadar kalır
PUNCH = [(4.16, 0.11, 0.12), (19.07, 0.09, 0.12), (33.52, 0.10, 0.12), (45.49, 0.06, 0.15)]
# (zaman, başlangıç fazlası, süre) — zoom out: büyükten normale yumuşak iniş
ZOOMOUT = [(12.95, 0.25, 0.7), (26.65, 0.14, 0.55), (20.95, 0.12, 0.5)]
SHAKE = [(19.07, 0.28), (33.52, 0.28)]
FLASH = [(35.42, 0.22)]
MANIFESTO = (35.42, 37.31)

def cam(t):
    s = 1.0
    for a, b, s0, s1 in BASE:
        if a <= t < b:
            s = s0 + (s1 - s0) * (t - a) / (b - a)
            seg_a, seg_b = a, b
            break
    else:
        seg_a, seg_b = 0, END
    for tp, add, d in PUNCH:
        if seg_a <= tp < seg_b and t >= tp:
            s += add * ease((t - tp) / d)
    for tz, extra, d in ZOOMOUT:
        if tz <= t < tz + d:
            s += extra * (1 - ease((t - tz) / d))
    dx = dy = 0.0
    for ts, d in SHAKE:
        if ts <= t < ts + d:
            k = 1 - (t - ts) / d
            dx += 14 * k * np.sin((t - ts) * 95)
            dy += 10 * k * np.cos((t - ts) * 77)
    return s, dx, dy

def frames_for(seg):
    s0, s1 = seg['src']
    n = int(round(seg['out'][1] * FPS)) - int(round(seg['out'][0] * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{s0:.3f}', '-i', '../calisma.mkv', '-t', f'{s1 - s0 + 0.2:.3f}',
                          '-an', '-r', str(FPS), '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        yield last
    p.stdout.close(); p.wait()

def gen_frames():
    for seg in TL:
        yield from frames_for(seg)

# ---- Ses ----
def build_audio():
    parts = []
    for seg in TL:
        s0, s1 = seg['src']
        n = int(round(seg['out'][1] * FPS)) - int(round(seg['out'][0] * FPS))
        parts.append(f"[0:a]atrim={s0:.3f}:{s0 + n / FPS:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={n / FPS - 0.02:.3f}:d=0.02[a{len(parts)}]")
    k = len(parts)
    concat = ''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1,highpass=f=80,afftdn=nf=-28,loudnorm=I=-14:TP=-1.5:LRA=9,apad=whole_dur={TOTAL:.3f}[voice]'
    sfx = [('whoosh.wav', 12.95 - 0.25), ('whoosh.wav', 20.95 - 0.25), ('whoosh.wav', 26.65 - 0.25),
           ('pop.wav', 4.16), ('pop.wav', 19.07), ('pop.wav', 33.52), ('shutter.wav', 35.42),
           ('pop.wav', 7.25), ('pop.wav', 22.7), ('pop.wav', 40.9), ('whoosh.wav', END - 0.2), ('pop.wav', END + 0.15)]
    inputs = ['-i', '../calisma.mkv']
    fx = []
    for i, (f, t) in enumerate(sfx):
        inputs += ['-i', f]
        vol = 0.22 if 'whoosh' in f else (0.16 if 'pop' in f else 0.28)
        fx.append(f'[{i + 1}:a]aresample=48000,volume={vol},adelay={int(t * 1000)}|{int(t * 1000)},apad=whole_dur={TOTAL:.3f}[s{i}]')
    mix = '[voice]' + ''.join(f'[s{i}]' for i in range(len(sfx))) + f'amix=inputs={len(sfx) + 1}:normalize=0:duration=first,atrim=0:{TOTAL:.3f},alimiter=limit=0.89[out]'
    fc = ';'.join(parts + [concat] + fx + [mix])
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[out]', '-ac', '2', '-ar', '48000', 'ses.wav'], check=True)

def main():
    build_audio()
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', 'ses.wav', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', 'cikti.mp4'], stdin=subprocess.PIPE)
    src = gen_frames()
    last = None
    for i in range(N):
        t = i / FPS
        if t < END:
            f = next(src, None)
            if f is None: f = last
            last = f
            s, dx, dy = cam(t)
            M = np.float32([[s, 0, AX - s * AX + dx], [0, s, AY - s * AY + dy]])
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            if MANIFESTO[0] <= t < MANIFESTO[1]:
                k = min(1, (t - MANIFESTO[0]) / 0.15, (MANIFESTO[1] - t) / 0.2)
                f = cv2.addWeighted(f, 1 - k, cv2.GaussianBlur(f, (0, 0), 22), k, 0)
            for tf, d in FLASH:
                if tf <= t < tf + d:
                    a = 0.85 * (1 - (t - tf) / d) ** 2
                    f = cv2.addWeighted(f, 1 - a, np.full_like(f, 255), a, 0)
        else:
            f = np.zeros((H, W, 3), np.uint8)
        gp = f'gf/{i:05d}.png'
        if os.path.exists(gp):
            g = cv2.imread(gp, cv2.IMREAD_UNCHANGED)
            if g.shape[2] == 4:
                a = g[..., 3:].astype(np.float32) / 255
                f = (f.astype(np.float32) * (1 - a) + g[..., :3].astype(np.float32) * a).astype(np.uint8)
            else:
                f = g
        enc.stdin.write(np.ascontiguousarray(f).tobytes())
        if i % 300 == 0: print('kare', i, '/', N, flush=True)
    enc.stdin.close(); enc.wait()
    print('bitti')

if __name__ == '__main__':
    main()
