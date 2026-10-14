# Mine Manas'ın Direktifleri

Önceki konuşmalarda verilen tüm talimatların özeti. Konuşmaların kelimesi kelimesine kaydı: [`docs/konusmalar/`](konusmalar/). Yeni bir direktif gelince bu dosyaya eklenir.

## Genel

- Türkçe konuşulur. Arayüz Türkçe; ayar tarif ederken düğmelerin Türkçe karşılığı da verilir.
- Mine Manas ajansı (Vega Dijital) için içerik üretir; **influencer değildir**. Abartılı efekt sevmez.
- Sınırlar dürüstçe söylenir: yapılamayan şey "yapamam" diye açıkça belirtilir, yerine öneri verilir.
- İzin, ayar ya da yetki gerekiyorsa **Claude önerir**; Mine yetkiyi verir.
- Abonelikler: CapCut Pro, Canva Pro, ChatGPT (ücretli), Magnific. Claude'a bağlanabilen yalnızca Canva (bağlayıcı yeniden bağlanmalı). Adobe bağlayıcısı bağlı.

## Video kurgu (asıl iş)

**Mine çeker, Claude kurgular.** Edit Mine'ın vaktini çok alıyor; asıl çözülmesi gereken kurgu.

1. **Çekim:** Prompter ile çekilir. Ham çekim efektsiz ve altyazısızdır.
2. **Gönderim:** Büyük dosyalar Google Drive linkiyle gelir ("Bağlantıya sahip herkes görüntüleyebilir"). Sohbete doğrudan yükleme sınırı 30 MB.
3. **Prompter metni** ayrıca gönderilir. Konuşma metinle birebir aynıdır.
4. **Kesim:**
   - Prompter metninde **olmayan her şey kesilir**. Kameramana verilen direktifler ("biraz yaklaş", "tamam, tekrar alıyorum" gibi) bu kapsamdadır.
   - Tekrar okunan cümlelerde en iyi okunan bırakılır.
   - Ölü anlar, duraklamalar, "ııı" ve "şey"ler kesilir.
   - Yöntem: faster-whisper ile yazıya dök, prompter metniyle karşılaştır.
5. **Hareket:** Video tek düze akmamalı; anlatılan konular sıkıcı olabiliyor.
   - Aralarda zoom in ve zoom out, önemli cümlede punch-in yapılır.
   - Küçük kamera efektleri eklenir: kısa sarsıntı, flaş, yavaş yaklaşma, vinyet, hafif bulanık geçiş.
   - Hepsi **dozunda, abartmadan** kullanılır.
   - Neyin nereye konacağına Claude metnin anlamına göre karar verir.
6. **Ses efektleri:** Whoosh, deklanşör ve pop gibi efektler eklenir. Mine kendi ses efektlerini gönderirse onlar kullanılır.
7. **Stok görüntü:**
   - Claude görüntü üretmez, öneri verir. Metin çekimden önce gelirse hangi cümleye hangi stok planın gerektiği saniyesiyle listelenir.
   - Mine görüntüleri gönderir, Claude yerleştirir.
8. **Teslim:** Altyazısız, temiz, 1080p, 9:16 MP4.
9. **Altyazı:** Altyazıyı Mine CapCut'ta kendisi ekler. Font ve stil **değişmez** (bkz. [`video-stili.md`](video-stili.md)).
10. **İsim girişi:** İlk ~3 saniyede "Mine MANAS / Founder | Digital Marketing Manager" aynı şablonla gelir.
    - Telefonda kesilmemesi için yazı **daha küçük** olur ve güvenli alan içinde kalır.
    - Bu girişi Mine CapCut'ta da yapabilir.
11. **Tempo:** Video hızlandırılmaz. 1.2x denendi, Mine "çok hızlı" dedi ve iptal etti. Tempo kesimlerle ve hareketle sağlanır.
12. **Revizyon:** Notlar saniye bazında verilir ("0:08 zoom'u kaldır").

**Manifesto videosundan öğrenilenler (v2 geri bildirimi):**
- **Zoom bol olmalı.** Neredeyse her vurgu kelimesinde punch-in ya da zoom out yapılır. Örnek videolardaki yoğunluk hedeflenir.
- **Giriş (hook) en önemli kısım.** Flaşlı giriş, sert zoom out ve ilk saniyelerde sık punch-in yapılır.
- **Tam ekran ara görüntüler.** Anlatılan şey görselle gösterilir (ürün, logo, dünya gibi) ve ekran kaydırma geçişiyle girip çıkar. Marka örneği verilince markanın logosu gösterilir. Tam ekran MANİFESTO kartı beğenildi.
- **Kapanış kartı** (logo, site, WhatsApp) beğenildi, aynı kalır.

**Kullanılmayacaklar:** Renkli ışık parlaması (light leak), "matrix" efekti, CapCut tarzı abartılı trend efektleri.

**Harmanlanacak referanslar:**
- Mine'ın kendi Reels kurgusu.
- Claude ile kurgulanmış referans video ("Andrej Karpathy'nin 4 yöntemi"). Bu videodan alınacak öğeler: beyaz kartlı başlıklar, numaralı yöntem kartları, ekran görüntüsü üzerinde vurgu, sade geçişler.

## Animasyonlu tanıtım videoları

- Format 9:16 (1080×1920). Örnek: `videolar/geo-tanitim-9x16/`, WhatsApp'tan gelen referans videonun yapısıyla yapıldı.
- Logo: `assets/logo/logo-lacivert.png` açık zeminde, `assets/logo/logo-beyaz.png` koyu zeminde kullanılır. Logo laciverti `#14284C`.
- Seslendirme ElevenLabs ile yapılır.
  - Türkçe sesler (önerilen: Sesil) ücretli plan ister; şu an İngilizce "Sarah" sesi kullanılıyor.
  - API anahtarı **asla depoya yazılmaz**. Ortam değişkeni `ELEVENLABS_API_KEY` olarak tanımlanmalı.
  - Sohbette paylaşılan eski anahtar iptal edilip yenilenmeli.

## Marka

- Kaynaklar: [`marka-rehberi.md`](marka-rehberi.md) ve `CLAUDE.md`.
- Instagram: https://www.instagram.com/vegadijitalcom/ (giriş yapılmadan içerik büyük ölçüde görünmez).
