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

# Kamera planı: (zaman, hedef ölçek, geçiş süresi; 0 = ani kesme)
KEYS = [
    (0.00, 1.35, 0), (0.02, 1.00, 0.5),          # giriş: flaş + sert zoom out
    (0.70, 1.12, 0), (1.72, 1.00, 0.25), (2.66, 1.18, 0), (3.58, 1.10, 0.3), (4.16, 1.32, 0),
    (5.63, 1.00, 0), (7.33, 1.14, 0),
    (8.59, 1.22, 0), (10.21, 1.06, 0.3), (11.19, 1.18, 0),
    (12.95, 1.35, 0), (12.97, 1.00, 0.6),          # konu geçişi zoom out
    (14.41, 1.10, 0), (15.99, 1.20, 0),
    (17.39, 1.00, 0), (18.11, 1.08, 0.4), (19.07, 1.30, 0),
    (20.95, 1.00, 0.5), (21.87, 1.10, 0),
    (26.60, 1.00, 0), (27.00, 1.08, 0.4),
    (30.00, 1.18, 0), (31.08, 1.00, 0.3),
    (35.42, 1.00, 0),
    (37.31, 1.20, 0), (38.53, 1.00, 0.25), (39.27, 1.22, 0),
    (40.57, 1.00, 0), (41.79, 1.10, 0.3), (43.09, 1.18, 0), (43.83, 1.00, 0.3), (45.49, 1.30, 0),
]
SHAKE = [(4.16, 0.28), (19.07, 0.28), (45.49, 0.3)]
FLASH = [(0.0, 0.30), (35.42, 0.22)]
MANIFESTO = (35.42, 37.31)
SL = 0.35
VID_OUT = [22.6, 27.35, 32.05]   # video sola kayarak çıkar (ara görüntü sağdan gelir)
VID_IN = [26.6, 30.0]            # video sağdan kayarak döner

def cam(t):
    s = KEYS[0][1]; last_t = 0
    for i, (tk, target, d) in enumerate(KEYS):
        if t < tk: break
        start = s
        s = target if d == 0 or t >= tk + d else start + (target - start) * ease((t - tk) / d)
        last_t = tk + d
    s *= 1 + min(0.04, 0.012 * max(0, t - last_t))   # yavaş yaklaşma
    dx = dy = 0.0
    for ts, d in SHAKE:
        if ts <= t < ts + d:
            k = 1 - (t - ts) / d
            dx += 16 * k * np.sin((t - ts) * 95)
            dy += 11 * k * np.cos((t - ts) * 77)
    for to in VID_OUT:
        if to <= t < to + SL: dx -= W * ease((t - to) / SL)
    for ti in VID_IN:
        if ti <= t < ti + SL: dx += W * (1 - ease((t - ti) / SL))
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
    sfx = [('whoosh.wav', -0.05), ('shutter.wav', 0.0),
           ('pop.wav', 4.16), ('pop.wav', 19.07), ('pop.wav', 45.49), ('pop.wav', 33.52),
           ('whoosh.wav', 12.95 - 0.2), ('whoosh.wav', 20.95 - 0.2),
           ('whoosh.wav', 22.6 - 0.1), ('whoosh.wav', 24.7 - 0.1), ('pop.wav', 25.25), ('whoosh.wav', 26.6 - 0.1),
           ('whoosh.wav', 27.35 - 0.1), ('whoosh.wav', 30.0 - 0.1), ('whoosh.wav', 32.05 - 0.1),
           ('shutter.wav', 35.42), ('pop.wav', 7.25), ('pop.wav', 40.9),
           ('whoosh.wav', END - 0.2), ('pop.wav', END + 0.15)]
    inputs = ['-i', '../calisma.mkv']
    fx = []
    for i, (f, t) in enumerate(sfx):
        inputs += ['-i', f]
        vol = 0.18 if 'whoosh' in f else (0.16 if 'pop' in f else 0.28)
        fx.append(f'[{i + 1}:a]aresample=48000,volume={vol},adelay={max(0,int(t * 1000))}|{max(0,int(t * 1000))},apad=whole_dur={TOTAL:.3f}[s{i}]')
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
