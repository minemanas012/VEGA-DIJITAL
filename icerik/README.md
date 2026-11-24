# İçerik üretimi

- `sablon/vega.css`: Ortak tasarım şablonu (renkler, fontlar, kartlar).
- `sablon/render.js`: Bir HTML'deki her `.slide` öğesini PNG olarak kaydeder.
  - Kullanım: `node sablon/render.js tasarim.html <klasör>`
- `sablon/reels.js`: Bir HTML animasyonunu 1080×1920 sessiz MP4'e çevirir.
  - Kullanım: `node sablon/reels.js reels.html cikti.mp4`
- `<yıl-ay>/takvim.md`: O ayın içerik takvimi ve paylaşım metinleri.
- `<yıl-ay>/<gün>-<konu>/`: Her gönderinin kaynak HTML'i ve çıktıları (PNG/MP4).
