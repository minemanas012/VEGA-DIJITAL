# Manifesto videosu: kurgu notları

**Ham çekim:** `MARKANIZIN SADECE NE SATTIĞINI ANLATIYORSANIZ.mp4`
- Google Drive'dan alındı.
- 4K (2160×3840), HEVC, 1 dk 48 sn.
- Ham dosya depoda değil, boyutu çok büyük.

**Teslim:** `manifesto-9x16-1.2x-altyazisiz.mp4`
- 1080×1920, 30 fps, altyazısız.
- Mine'ın isteğiyle **1.2 hıza** alındı; ses perdesi korundu. Süre 40,7 sn.
- Aşağıdaki saniyeler 1.2x öncesi kurguya göre verildi. 1.2x videodaki karşılığını bulmak için 1,2'ye bölün.

## Kesilenler

| Ham çekimde | Neden |
|---|---|
| 0:00–0:31 | İlk deneme yarıda kalmış. Ardından kameramana direktifler var: "şey biraz indir", "başa al", "arkaya indir", "bir daha başa al prompteri". |
| 0:45–0:52 | "Aslında bu mesele… misyon" yarıda kalmış, cümle baştan tekrar okunmuş. |
| 1:00–1:12 | Patagonia cümlesinin ilk okuması ve "Onlar yalnızca…" takılması. İkinci okuma kullanıldı. |
| 1:32–1:39 | "Çünkü insanlar…" yanlış başlangıç. |
| 1:45 sonrası | Çekim sonu. |
| Cümle araları | 0,4 sn'den uzun duraklamalar kısaltıldı. |

## Kamera hareketleri

Çıktı videosundaki saniyeler.

| Saniye | Hareket | Ses |
|---|---|---|
| 0–5,6 | Yavaş yaklaşma; "kaçırıyor" kelimesinde punch-in | pop |
| 5,6 | Kesme, geniş plan | |
| 8,6 | Yakın plan | |
| 12,9 | Zoom out (yeni konu: vizyon/misyon) | whoosh |
| 19,1 | "karakter" kelimesinde punch-in ve kısa sarsıntı | pop |
| 20,9 | Zoom out (Patagonia örneği) | whoosh |
| 26,6 | Zoom out ("Yıllardır…") | whoosh |
| 33,5 | "dur deyin" kelimesinde punch-in ve kısa sarsıntı | pop |
| 35,4 | Flaş ve tam ekran MANİFESTO kartı (arka plan bulanık) | deklanşör |
| 37,3 | Yakın plan | |
| 45,5 | "duruşlarıyla" kelimesinde hafif punch-in | |
| 46,8 | Kapanış kartı: logo, vegadijital.com.tr ve WhatsApp çağrısı | whoosh, pop |

## Grafikler

Grafikler gövde hizasında, ekranın %46–72'si arasında duruyor. Yüz ve alttaki altyazı alanı (%78–82) boş kalıyor.

| Saniye | Grafik |
|---|---|
| 7–13 | "Ürün" kartı üstü çiziliyor; ardından "Fikir + Hikâye" kartı geliyor |
| 14–21 | "Vizyon" ve "Misyon" kartları geliyor, sonra "+ KARAKTER" kartı |
| 22,5–26,5 | "ÖRNEK · Patagonia" kartı; altında "mont" ve "çanta" |
| 27–35 | Alıntı kartları: "Dünyayı kurtarmak için iş yapıyoruz." ve "Tüketim çılgınlığına **dur deyin.**" |
| 35,4–37,3 | Tam ekran MANİFESTO kartı |
| 37,3–40,5 | "Ne sattığınız" kartı üstü çiziliyor; ardından "**Neyi temsil ettiğiniz**" kartı geliyor |
| 40,8–46,8 | "Sıradan markalar → ürünleriyle" ve "Güçlü markalar → **duruşlarıyla**" kartları; altında "HATIRLANIR" |

## Yeniden üretmek için

Betikler `kaynak/` klasöründe.

1. `words.py`: Kesitlerdeki kelimelerin zamanlarını çıkarır.
2. `node grafik.js`: Grafik karelerini üretir.
3. `sfx.py`: Ses efektlerini üretir.
4. `kurgu.py`: Videoyu kurgular.

Kesitler `segs.json` dosyasında, kamera planı `kurgu.py` içinde, grafik zamanlamaları `grafik.html` içinde.
