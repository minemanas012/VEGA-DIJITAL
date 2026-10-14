# Vega Dijital — Video Kurgu Stili

Kaynak: Mine Manas'ın kendi Reels kurgusu (örnek: `1014.mp4`) + Claude ile kurgulanmış referans video. Abartılı efekt yok; ajans içeriği, influencer değil.

## Format
- 9:16 dikey, 1080×1920 (örnekler 720×1280), 30 fps.
- Konuşan kişi (Mine Manas) + yer yer stok görüntü ara planları.

## Altyazı (DEĞİŞMEZ)
- Font: **Montserrat ExtraBold** (`assets/fonts/`), küçük harf (cümlenin yazıldığı gibi). Not: ffonts.net kaynaklı eski "montserrat-bold" dosyası İ, ğ, Ğ, ş, Ş içermez — kullanılmaz.
- Ana renk: beyaz, ince siyah kontur + hafif gölge.
- Vurgu: aktif/önemli kelime **sarı `#FCE400`**; ikinci vurgu **kırmızı** (yaklaşık `#E00000`, kesin kod doğrulanacak).
- Satır başına 2–4 kelime, en fazla 2 satır, ortalı.
- Konum: alttan yaklaşık %20 yukarıda (y ≈ %78–82), kişinin gövdesi üzerinde.

## İsim girişi (ilk ~3–5 sn)
- Alt bant: üstte turuncu şerit `#C65400` — siyah Montserrat Bold "Founder | Digital Marketing Manager".
- Altında beyaz kutu (sağ köşesi yuvarlatılmış) — siyah Montserrat ExtraBold "Mine MANAS".
- Animasyon: beyaz kutu soldan kayarak gelir → turuncu şerit gelir → isim ve unvan daktilo gibi soldan sağa yazılır.
- **Düzeltme:** PC'de hazırlanan versiyon telefonda sağdan kesiliyordu. Yeni versiyonda yazı ~%15–20 küçük, tüm metin ve kutular ekranın sol/sağ %6 güvenli alanı içinde kalmalı (Instagram arayüzü için alt %15 ve sağ kenar boşluğu korunur).

## Kurgu dili
- Hafif yakınlaştırma (punch-in) vurgu cümlelerinde; ince odak/kamera çerçevesi efekti seyrek.
- Stok görüntü ara planları ilgili cümle boyunca, altyazı devam eder.
- Referans videodan alınabilecek sade öğeler: beyaz kartlı başlıklar, numaralı "Yöntem 1/4" kartları, ekran görüntüsü üzerinde sarı vurgu, kapanışta yorum/takip çağrısı (Vega'da CTA: WhatsApp).
- Hashtag yok; dayanaksız iddia yok (bkz. `marka-rehberi.md`).

## İş akışı (kararlaştırılan)
1. Mine Manas prompter ile çeker; ham çekim (efektsiz, altyazısız) 30 MB altı parçalar halinde yüklenir.
2. Prompter metni (konuşma metni) gönderilir; cümleler sessizlik analiziyle ses bölümlerine eşlenir.
3. Claude kurgular: ölü an/tekrar kesimi, zoom in/out, punch-in, kısa sarsıntı, flaş, ses efekti, stok görüntü yerleşimi, ses dengeleme.
4. Teslim: altyazısız 1080p MP4. Altyazıyı Mine Manas CapCut'ta ekler.
5. Revize notları saniye bazında ("0:08 zoom'u kaldır").
