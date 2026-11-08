# Mühendislik Matematiği · Çalışma Atölyesi

156 ders/defter fotoğrafı ve `mufredat.png` temelinde hazırlanan Türkçe çalışma sitesi. Tasarım ve okuma yapısı `/home/kemal/DSA/Vize_Hazirlik` sitesini referans alır.

- 6 müfredat başlığının ayrıntılı anlatımı; 89 çözümlü örnek kaydı (bazıları çok alt sorulu).
- 8 PDF: 6 konu kitabı, çözümlü soru bankası ve tüm konuları içeren birleşik kitap.
- Bütün PDF'ler **XeLaTeX** ile, özgün `.tex` kaynaklarından derlenir.
- Web ve PDF aynı `content/course.py` kaynağından üretilir.
- Tam metin arama, yerel KaTeX, koyu/açık tema, soru filtresi, çözümü açma/kapama, tarayıcıda çalışma kaydı.
- 156 fotoğrafın ayrı konu eşleştirmesi: `analysis/FOTOGRAF_INCELEMESI.md` ve `fotograflar.html`.

## Açmak

`index.html` doğrudan tarayıcıda açılabilir; internet gerektirmez. İsteğe bağlı yerel sunucu:

```bash
cd /home/kemal/muhmat/Muhendislik_Matematigi
python3 -m http.server 8765 --bind 127.0.0.1
```

Ardından `http://127.0.0.1:8765` açılır. İlerleme sunucunun adresine/tarayıcıya özgü localStorage kaydıdır; cihazlar arasında eşitlenmez.

## Yeniden üretmek

Gerekenler: Python 3, XeLaTeX (TeX Live), Noto Serif, Noto Sans, Noto Sans Mono, TikZ/PGFPlots, Poppler. Fotoğraf küçük görselleri için Pillow gerekir; mevcut küçük görseller çalıştırmak için yeterlidir.

```bash
python3 scripts/photo_index.py
python3 scripts/figures.py
python3 scripts/build.py --compile --package
```

Her bir PDF ayrı da derlenebilir:

```bash
cd tex
xelatex -interaction=nonstopmode -halt-on-error 01-vektorler.tex
xelatex -interaction=nonstopmode -halt-on-error 01-vektorler.tex
```

`pdf/` teslim dosyalarını, `tex/` LaTeX kaynaklarını, `assets/figures/` TikZ/PGFPlots çizimlerini, `dist/` yayıma hazır statik siteyi içerir. `tex-kaynaklari.zip`, kaynak ve şekilleri birlikte taşır. `.openai/hosting.json` özel Sites proje kimliğidir.

## Kaynak ve aktarım sınırları

Fotoğrafların tamamı konu bakımından gözden geçirilerek eşleştirildi. Aynı tahtanın tekrar çekimleri korundu. Soluk, kesilmiş veya kişiyle örtülmüş sembollerden tahmini soru üretilmedi. Doğrudan çözülen örnekler kaynak fotoğrafına bağlıdır; diğer örnekler **Pekiştirme** olarak etiketlenir. Tarihler dosya adlarından gelir; ders tarihi olarak varsayılmaz.

Kreyszig'in Wiley bölüm dizini ve Kreyszig temelli açık üniversite notları kontrol kaynağıdır. Kullanıcının belirttiği Zill–Wright (Cangül çevirisi, 2013) ve Mustafa Balcı (2013) kitaplarının tam metinleri sağlanmadı; bunlardan okunmuş sayfa veya soru numarası iddia edilmez. Gradyan/yönlü türev müfredatta bulunup fotoğraflarda açık anlatımı görünmeyen tamamlayıcı bölümdür. Kaynak ayrıntıları `kaynaklar.html` ve her PDF'nin sonunda yer alır.
