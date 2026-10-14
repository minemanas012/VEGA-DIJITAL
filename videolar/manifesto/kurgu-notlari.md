# Manifesto videosu: kurgu notları

**Ham çekim:** `MARKANIZIN SADECE NE SATTIĞINI ANLATIYORSANIZ.mp4`
- Google Drive'dan alındı.
- 4K (2160×3840), HEVC, 1 dk 48 sn.
- Ham dosya depoda değil, boyutu çok büyük.

**Teslim (v2):** `manifesto-v2-altyazisiz.mp4`
- 1080×1920, 30 fps, altyazısız, 48,8 sn, normal hız.
- `manifesto-v2-onizleme.mp4`: 30 MB altı önizleme kopyası.

**v1'den v2'ye değişenler (Mine'ın notları):**
1. 1.2 hız iptal edildi; normal hız.
2. Tam ekran ara görüntüler kaydırma geçişiyle eklendi: Patagonia logosu, mont ve çanta, dünya, tüketim (AVM).
3. Kapanış kartı aynen kaldı.
4. Zoom in/out sıklaştırıldı. Girişe (hook) flaş ve sert zoom out eklendi.

## Kesilenler

| Ham çekimde | Neden |
|---|---|
| 0:00–0:31 | İlk deneme yarıda kalmış. Ardından kameramana direktifler var: "şey biraz indir", "başa al", "arkaya indir", "bir daha başa al prompteri". |
| 0:45–0:52 | "Aslında bu mesele… misyon" yarıda kalmış, cümle baştan tekrar okunmuş. |
| 1:00–1:12 | Patagonia cümlesinin ilk okuması ve "Onlar yalnızca…" takılması. İkinci okuma kullanıldı. |
| 1:32–1:39 | "Çünkü insanlar…" yanlış başlangıç. |
| 1:45 sonrası | Çekim sonu. |
| Cümle araları | 0,4 sn'den uzun duraklamalar kısaltıldı. |

## Kamera ve ara görüntüler (v2)

Saniyeler çıktı videosuna göre.

| Saniye | Ne oluyor |
|---|---|
| 0 | Flaş ile giriş, 1.35'ten sert zoom out (whoosh ve deklanşör) |
| 0,7 / 2,7 / 4,2 | Kelime vurgulu punch-in'ler. "kaçırıyor"da en güçlüsü, kısa sarsıntıyla |
| 5,6–12,9 | Her cümlede zoom değişimi; "Ürün" ve "Fikir + Hikâye" kartları |
| 12,9 | Konu geçişi zoom out; ardından Vizyon/Misyon ve "+ KARAKTER" kartları, "karakter"de punch-in ve sarsıntı |
| 22,6 | Kaydırma: tam ekran Patagonia logosu |
| 24,7 | Kaydırma: üstte MONT, "çanta" denince altta ÇANTA görseli |
| 26,6 | Videoya dönüş |
| 27,35–30 | Tam ekran dünya ve "Dünyayı kurtarmak için iş yapıyoruz." |
| 32,05–35,4 | Tam ekran AVM ve "Tüketim çılgınlığına dur deyin."; "dur deyin"de sarsıntı |
| 35,4 | Flaş ve MANİFESTO kartı |
| 37,3–46,8 | Kelime vurgulu zoom'lar, karşılaştırma kartı; "duruşlarıyla"da punch-in ve sarsıntı |
| 46,8 | Kapanış kartı |

## Görsel kaynakları

| Görsel | Kaynak | Lisans |
|---|---|---|
| Mont rafı | rawpixel (Openverse) | CC0 |
| Sarı sırt çantası | StockSnap, Felix Russell-Saw | CC0 |
| Dünya | NASA Goddard / Reto Stöckli (rawpixel) | CC0 / kamu malı |
| AVM | StockSnap, Burst | CC0 |
| Patagonia logosu | worldvectorlogo | Tescilli marka; örnek gösterimi amacıyla kullanıldı |

Not: Görsellerin bulunabilen boyutları yaklaşık 1000 piksel. Kalite düşmesin diye görseller tam ekrana büyütülmedi. Arka planda aynı görselin bulanık hali var, önünde net görsel kart olarak duruyor. Mine'ın gönderdiği stok görüntüler varsa onlar tercih edilir.

## Yeniden üretmek için

Betikler `kaynak/` klasöründe.

1. `words.py`: Kesitlerdeki kelimelerin zamanlarını çıkarır.
2. `node grafik.js`: Grafik karelerini üretir.
3. `sfx.py`: Ses efektlerini üretir.
4. `kurgu.py`: Videoyu kurgular.

Kesitler `segs.json` dosyasında, kamera planı `kurgu.py` içinde, grafik zamanlamaları `grafik.html` içinde.
