"""Vega Dijital — sanatsal seri (perspektif kompozitleri).
Kaynak görseller: Art Institute of Chicago, kamu malı (CC0). Bkz. README.md.
Kullanım: python3 kompozit.py  -> 01-ekrandan-cikan.png, 02-olcek.png, 03-manolya.png"""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
K = 'kaynak/'
F = '../../assets/fonts/'
NAVY = (10, 20, 48); INK = (20, 40, 76)


def rgba(path):
    a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if a.shape[2] == 3:
        a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    return a.astype(np.float32) / 255  # BGRA


def over(dst, src, mask=None):
    """dst BGR float, src BGRA float (aynı boyut)."""
    a = src[..., 3:4] if mask is None else src[..., 3:4] * mask[..., None]
    return dst * (1 - a) + src[..., :3] * a


def warp(img, quad, size=(W, H)):
    h, w = img.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(quad))
    return cv2.warpPerspective(img, M, size, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def poly(quad, size=(W, H), blur=0):
    m = np.zeros((size[1], size[0]), np.float32)
    cv2.fillPoly(m, [np.int32(np.round(quad))], 1.0, lineType=cv2.LINE_AA)
    return cv2.GaussianBlur(m, (0, 0), blur) if blur else m


def halfplane_above(p1, p2, size=(W, H)):
    yy, xx = np.mgrid[0:size[1], 0:size[0]].astype(np.float32)
    (x1, y1), (x2, y2) = p1, p2
    yline = y1 + (xx - x1) * (y2 - y1) / (x2 - x1)
    return np.clip(yline - yy + 0.5, 0, 1)


def place(img, x, y, scale, size=(W, H)):
    """BGRA görseli (x,y) sol üst köşeye ölçekleyip tuvale koyar."""
    h, w = img.shape[:2]
    M = np.float32([[scale, 0, x], [0, scale, y]])
    return cv2.warpAffine(img, M, size, flags=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC, borderValue=0)


def shadow(layer, dx, dy, blur, op):
    a = layer[..., 3]
    a = cv2.warpAffine(a, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H))
    return cv2.GaussianBlur(a, (0, 0), blur) * op


def gradient(c1, c2, vertical=True):
    t = np.linspace(0, 1, H if vertical else W, dtype=np.float32)
    g = np.array(c1, np.float32)[None] * (1 - t[:, None]) + np.array(c2, np.float32)[None] * t[:, None]
    return np.repeat(g[:, None, :], W, 1) / 255 if vertical else np.repeat(g[None], H, 0) / 255


def blob(img, cx, cy, r, color, op):
    m = np.zeros((H, W), np.float32); cv2.circle(m, (cx, cy), r, 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), r * 0.6) * op
    return img * (1 - m[..., None]) + np.array(color, np.float32)[None, None] / 255 * m[..., None]


def grain(img, amt=0.035, seed=3):
    n = np.random.default_rng(seed).normal(0, amt, (H, W, 1)).astype(np.float32)
    return np.clip(img + n, 0, 1)


def to_pil(img):
    return Image.fromarray(cv2.cvtColor((np.clip(img, 0, 1) * 255).astype(np.uint8), cv2.COLOR_BGR2RGB))


def text(pil, xy, s, size, weight='Black', fill=NAVY, spacing=0, lead=1.05):
    f = ImageFont.truetype(F + f'Montserrat-{weight}.ttf', size)
    d = ImageDraw.Draw(pil)
    y = xy[1]
    for line in s.split('\n'):
        d.text((xy[0], y), line, font=f, fill=fill, spacing=spacing)
        y += int(size * lead)
    return y


def logo(pil, white=False, x=None, y=None, h=64):
    lg = Image.open('../../assets/logo/' + ('logo-beyaz.png' if white else 'logo-lacivert.png')).convert('RGBA')
    lg = lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)
    pil.paste(lg, (x if x is not None else W - lg.width - 56, y if y is not None else H - h - 50), lg)


def tag(pil, xy, s, fill=INK):
    f = ImageFont.truetype(F + 'Montserrat-Bold.ttf', 22)
    ImageDraw.Draw(pil).text(xy, s, font=f, fill=fill)


# ---------------------------------------------------------------- 1
def p1():
    bg = gradient((236, 230, 222), (214, 206, 196))[..., ::-1].copy()
    bg = blob(bg, 760, 420, 360, (255, 210, 225), 0.55)
    bg = blob(bg, 300, 1150, 300, (200, 235, 220), 0.45)
    # telefon (sağa dönük, perspektifli)
    TL, TR, BR, BL = (250, 600), (930, 650), (930, 1235), (250, 1305)
    side = [TR, (TR[0] + 20, TR[1] + 14), (BR[0] + 20, BR[1] - 6), BR]
    floor = np.zeros((H, W), np.float32); cv2.ellipse(floor, (600, 1300), (400, 44), -4, 0, 360, 1, -1)
    floor = cv2.GaussianBlur(floor, (0, 0), 26) * 0.45
    img = bg * (1 - floor[..., None])
    body = poly([TL, TR, BR, BL]); sidem = poly(side)
    img = img * (1 - sidem[..., None]) + np.array([30, 18, 8], np.float32) / 255 * sidem[..., None]
    img = img * (1 - body[..., None]) + np.array(NAVY[::-1], np.float32) / 255 * body[..., None]
    # ekran
    def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    i = 0.045; j = 0.03
    sTL = lerp(lerp(TL, TR, i), lerp(BL, BR, i), j); sTR = lerp(lerp(TL, TR, 1 - i), lerp(BL, BR, 1 - i), j)
    sBR = lerp(lerp(TL, TR, 1 - i), lerp(BL, BR, 1 - i), 1 - j); sBL = lerp(lerp(TL, TR, i), lerp(BL, BR, i), 1 - j)
    sky = cv2.imread(K + 'rousseau-ilkbahar.jpg').astype(np.float32) / 255
    sky = sky[0:1000, 250:1150]
    sq = [sTL, sTR, sBR, sBL]
    scr = warp(sky, sq); sm = poly(sq)
    img = img * (1 - sm[..., None]) + scr * sm[..., None]
    # ekrana hafif cam parlaması
    gl = poly([sTL, (sTL[0] + 260, sTL[1] + 26), (sTL[0] + 60, sBL[1]), sBL]) * sm * 0.10
    img = img + gl[..., None]
    # büst: alt kısmı (kaide) ekran altında kalır
    b = rgba(K + 'mochi-genc-bust.png')
    ys, xs = np.where(b[..., 3] > 0.1); b = b[ys.min():ys.max(), xs.min():xs.max()]
    b = b[:int(b.shape[0] * 0.56)]             # kaideyi at
    sc = 980 / b.shape[0]                      # kesim çizgisi ekranın alt kenarının altında kalsın
    bx = 650 - b.shape[1] * sc / 2; by = 330
    bl = place(b, bx, by, sc)
    mask = np.clip(sm + halfplane_above(sTL, sTR), 0, 1)
    sh = shadow(bl, 16, 26, 18, 0.45) * mask * body
    img = img * (1 - sh[..., None])
    img = over(img, bl, mask)
    # ekranın alt kenarında hafif "çıkış" ışıması
    img = grain(img)
    pil = to_pil(img)
    text(pil, (70, 104), 'Markanız\nekranda\nkalmasın.', 66, lead=1.04)
    tag(pil, (72, 60), 'GÖRSEL TASARIM · VEGA DİJİTAL')
    logo(pil)
    pil.save('01-ekrandan-cikan.png')


# ---------------------------------------------------------------- 2
def p2():
    sky = cv2.imread(K + 'rousseau-ilkbahar.jpg')
    h, w = sky.shape[:2]; s = H / h
    sky = cv2.resize(sky, (int(w * s), H), interpolation=cv2.INTER_CUBIC)
    x0 = (sky.shape[1] - W) // 2 - 60
    img = sky[:, x0:x0 + W].astype(np.float32) / 255
    # arama çubuğu (düz olarak çizilip yere yatırılır)
    bw, bh = 1400, 230
    bar = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=(255, 255, 255, 255))
    d.ellipse((70, 60, 160, 150), outline=(106, 115, 144, 255), width=14)
    d.line((148, 138, 195, 185), fill=(106, 115, 144, 255), width=16)
    f = ImageFont.truetype(F + 'Montserrat-SemiBold.ttf', 74)
    d.text((240, 72), 'dijital pazarlama ajansı', font=f, fill=INK + (255,))
    barr = cv2.cvtColor(np.array(bar), cv2.COLOR_RGBA2BGRA).astype(np.float32) / 255
    quad = [(150, 930), (1010, 900), (1120, 1060), (-30, 1110)]
    side = [quad[3], quad[2], (quad[2][0], quad[2][1] + 16), (quad[3][0], quad[3][1] + 18)]
    gs = poly([(q[0] + 10, q[1] + 40) for q in quad], blur=22) * 0.55
    img = img * (1 - gs[..., None])
    sm = poly(side)
    img = img * (1 - sm[..., None]) + np.array([170, 172, 176], np.float32) / 255 * sm[..., None]
    wb = warp(barr, quad)
    img = over(img, wb)
    # minik figür çubuğun üstünde
    fig = rgba(K + 'rogers-kayip-pleiade.png')
    ys, xs = np.where(fig[..., 3] > 0.1); fig = fig[ys.min():ys.max(), xs.min():xs.max()]
    fl = place(fig, 640, 690, 0.155)
    fsh = np.zeros((H, W), np.float32); cv2.ellipse(fsh, (705, 990), (60, 12), -3, 0, 360, 1, -1)
    img = img * (1 - (cv2.GaussianBlur(fsh, (0, 0), 8) * 0.5)[..., None])
    img = over(img, fl)
    # üstte koyulaşma (yazı için)
    t = np.linspace(1, 0, H, dtype=np.float32)[:, None, None] ** 3
    img = img * (1 - 0.45 * t)
    img = grain(img, 0.03)
    pil = to_pil(img)
    text(pil, (70, 104), 'Görünür olmak,\ndoğru yerde\ndurmaktır.', 70, fill=(255, 255, 255), lead=1.04)
    tag(pil, (72, 60), 'GÖRSEL TASARIM · VEGA DİJİTAL', fill=(255, 255, 255))
    logo(pil, white=True)
    pil.save('02-olcek.png')


# ---------------------------------------------------------------- 3
def p3():
    bg = gradient((19, 32, 64), (8, 14, 34))[..., ::-1].copy()
    bg = blob(bg, 820, 300, 380, (45, 107, 255), 0.35)
    bg = blob(bg, 200, 1150, 320, (143, 227, 200), 0.22)
    img = bg
    paint = cv2.imread(K + 'heade-manolya.jpg').astype(np.float32) / 255
    cut = rgba(K + 'heade-manolya-dekupe.png')
    ph, pw = paint.shape[:2]
    # tarayıcı penceresi (sola dönük perspektif); resim pencereye oturur, çiçekler taşar
    win = [(120, 520), (820, 470), (860, 1000), (90, 1060)]
    bar_h = 0.085
    def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    cTL, cTR = lerp(win[0], win[3], bar_h), lerp(win[1], win[2], bar_h)
    content = [cTL, cTR, win[2], win[3]]
    # içerik alanı resmin orta bölümünü gösterir; aynı dönüşüm resmin tamamına uygulanır
    cx0, cy0, cx1, cy1 = 330, 120, 1300, 900
    src = np.float32([[cx0, cy0], [cx1, cy0], [cx1, cy1], [cx0, cy1]])
    Mx = cv2.getPerspectiveTransform(src, np.float32(content))
    wp = cv2.warpPerspective(paint, Mx, (W, H), flags=cv2.INTER_CUBIC)
    wc = cv2.warpPerspective(cut, Mx, (W, H), flags=cv2.INTER_CUBIC)
    shw = poly([(p[0] + 30, p[1] + 50) for p in win], blur=40) * 0.6
    img = img * (1 - shw[..., None])
    wm = poly(win)
    img = img * (1 - wm[..., None]) + np.array([250, 247, 244], np.float32) / 255 * wm[..., None]
    for k, col in enumerate([(87, 95, 255), (46, 189, 254), (64, 201, 40)]):
        p = lerp(lerp(win[0], win[1], 0.04 + k * 0.035), lerp(win[3], win[2], 0.04 + k * 0.035), bar_h / 2)
        cv2.circle(img, (int(p[0]), int(p[1])), 11, tuple(c / 255 for c in col), -1, cv2.LINE_AA)
    ub = [lerp(lerp(win[0], win[1], .22), lerp(win[3], win[2], .22), bar_h * .25), lerp(lerp(win[0], win[1], .78), lerp(win[3], win[2], .78), bar_h * .25),
          lerp(lerp(win[0], win[1], .78), lerp(win[3], win[2], .78), bar_h * .75), lerp(lerp(win[0], win[1], .22), lerp(win[3], win[2], .22), bar_h * .75)]
    um = poly(ub); img = img * (1 - um[..., None] * .08)
    cm = poly(content)
    img = img * (1 - cm[..., None]) + wp * cm[..., None]
    # pencere dışına taşan çiçekler + gölgesi
    outside = 1 - cm
    csh = cv2.GaussianBlur(wc[..., 3] * outside, (0, 0), 14)
    csh = cv2.warpAffine(csh, np.float32([[1, 0, 18], [0, 1, 30]]), (W, H)) * 0.55
    img = img * (1 - csh[..., None])
    img = over(img, wc, outside)
    img = grain(img, 0.03)
    pil = to_pil(img)
    text(pil, (70, 104), 'Estetik ve işlev,\naynı karede.', 68, fill=(255, 255, 255), lead=1.05)
    tag(pil, (72, 60), 'GÖRSEL TASARIM · VEGA DİJİTAL', fill=(255, 255, 255))
    logo(pil, white=True)
    pil.save('03-manolya.png')


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or ['1', '2', '3']):
        {'1': p1, '2': p2, '3': p3}[n]()
        print('ok', n)
