# Konu ve Soru Çözümü .tex dosyaları için yazım kılavuzu

Bu dosyalar hem XeLaTeX ile PDF'e derlenir (tex/build.sh), hem de `tex/html_gen/build_html.py` ile web sayfasına
dönüştürülür. Dönüştürücü küçük, kendi yazdığımız bir LaTeX ayrıştırıcısıdır; aşağıdaki kurallara uyulursa her iki çıktı
da düzgün olur.

## Dosyalar
- `tex/konu/NN_ad.tex`  : konu anlatımı gövdesi (preamble YOK, `\documentclass` YOK). `\section{...}` ile başlar.
- `tex/soru/NN_ad.tex`  : Soru Çözümü belgesindeki bu konunun bölümü. Tek bir `\section{Konu N: ...}` ile başlar.
- Ortak stil: `tex/ortak.sty` (değiştirme; yeni paket/komut ekleme).

## Kullanılabilecek ortamlar (ortak.sty)
- `\begin{tanim}[Başlık]...\end{tanim}`  — tanım (başlık isteğe bağlı)
- `\begin{teorem}[Başlık]...\end{teorem}` — teorem / önemli formül
- `\begin{tahta}[\foto{IMG-20261023-WA0011}]...\end{tahta}` — hocanın tahtaya yazdığı not (fotoğraf adı .jpg'siz)
- `\begin{dikkat}...\end{dikkat}` — varsayılan başlık "Sık yapılan hatalar"; `\begin{dikkat}[Dikkat]` da olur
- `\begin{bilgi}[Başlık]...\end{bilgi}` — sezgi, ek bilgi, kaynak notu
- `\begin{ozet}...\end{ozet}` — bölüm/konu sonu özet ve formül kutusu
- `\begin{soru}[Örnek 3 \foto{IMG-20261009-WA0021}]...\end{soru}` ardından `\begin{cevap}...\end{cevap}`
  (cevap varsayılan başlığı "Çözüm"; `\begin{cevap}[Çözüm (adım adım)]` olabilir)
- Listeler: itemize, enumerate (opsiyonel `[label=...]` KULLANMA, düz kullan), description
- Tablolar: `\begin{center}\begin{tabular}{l c}\toprule ... \\\midrule ... \\\bottomrule\end{tabular}\end{center}`
- Matematik: `$...$`, `\[ ... \]`, `$$...$$`, `\begin{align*}...\end{align*}`, `\begin{equation*}`.
  İçeride `\begin{cases}`, `\begin{vmatrix}`, `\begin{pmatrix}`, `\boxed{}`, `\overrightarrow{AB}`, `\mathbf{}`,
  `\nabla`, `\partial`, `\iint`, `\left( \right)`, `\text{...}`, `\quad`, `\lim_{(x,y)\to(0,0)}` kullanılabilir (KaTeX destekler).
- Yardımcı komutlar: `\foto{IMG-...}` (fotoğraf etiketi), `\ekal` (Ek alıştırma etiketi, soru başlığında kullan:
  `\begin{soru}[\ekal Ek alıştırma 2]`), `\okunamadi{açıklama}` (tahtada okunamayan yer), `\vurg{metin}` (kırmızı kalın).
- Şekiller: `\begin{center}\begin{tikzpicture}...\end{tikzpicture}\end{center}`. 3B için
  `[x={(-0.5cm,-0.4cm)},y={(1cm,0cm)},z={(0cm,1cm)}]` gibi eğik izdüşüm kullan; stiller: `eks` (eksen oku), `vek` (vektör oku).
  pgfplots ile 2B/3B grafikler: `\begin{tikzpicture}\begin{axis}[...]\addplot3[surf,...]{...};\end{axis}\end{tikzpicture}`.
  Şekiller otomatik SVG'ye çevrilir. Her konuya, anlamayı gerçekten kolaylaştıran 2–5 şekil yeterli (çok uzun derleme olmasın;
  `samples` ≤ 25 tut).
- Renkler: ana, vurgu, yesil, turuncu, gri, mor (`\textcolor{vurgu}{...}`).

## YAPMA
- Yeni `\newcommand`, `\def`, paket ekleme YOK. Matematik içinde kendi makron YOK (KaTeX bilmez).
- `\label/\ref`, `\cite`, dipnot zinciri, `\includegraphics` (fotoğraf gömme) YOK.
- `enumerate` için `[label=(\alph*)]` gibi seçenekler YOK; `(a)`, `(b)` yazacaksan `description` ya da düz metin kullan.
- `\verb`, `lstlisting` gereksiz.
- Matematik dışında `_` ve `^` YOK; `%`, `&`, `#` karakterlerini metinde `\%`, `\&`, `\#` olarak yaz.
- `\section*` kullanma (numaralı başlıklar içindekilerde çıkar).
- Türkçe tırnak: ``...'' kullanılabilir.

## Konu dosyasının iskeleti (önerilen)
```
\section{Konunun adı}
\subsection{Amaç ve sezgi}           % neden bu konu, geometrik sezgi, nerede kullanılır
\subsection{...temel kavramlar...}   % tanım kutuları, teorem kutuları, şekiller
  ... her alt başlıkta: tanım → teorem/formül → adım adım yöntem → tahtadaki örnek(ler) (soru+cevap, \foto ile)
\subsection{Kaynak kitaplardan ek örnekler}   % soru başlığında \ekal
\subsection{Sık yapılan hatalar}     % dikkat kutusu(ları)
\subsection{Özet ve formül kutusu}   % ozet kutusu (tablo/formüller)
```
Alt başlık sayısı konu büyüklüğüne göre 6–12 arası olsun. Metin Türkçe, açık, öğrenciye hitap eden bir dil; kitaplardan uzun
alıntı yapma, kendi anlatımınla yaz.

## Tahta içeriğine sadakat
- Tahtada çözülen HER örnek, konu anlatımında ilgili alt başlıkta tam çözümüyle yer alsın (soru+cevap, `\foto{}` ile).
  Aynı örnek birden çok fotoğrafta görünüyorsa bir kez yaz, `\foto{A}, \foto{B}` diye iki kaynağı da ver.
- Tahtada okunamayan yer → `\okunamadi{...}` ile işaretle ve kaynak kitaplara göre doğrusunu ayrıca belirt
  (ör. "Kaynaklara göre doğrusu: ...").
- Tahtadaki hesap/yazım hatalarını sessizce düzeltme: doğrusunu yaz ve küçük bir `bilgi`/`dikkat` notu ile belirt
  ("Tahtada ... yazılmıştı; doğrusu ...").
- Notlarda "başka bir derse ait" diye işaretlenen fotoğrafları (ör. sıralama algoritması) içeriğe KATMA.

## Soru Çözümü dosyası
- Bu konuda derste çözülen TÜM soru/örnekler, derste işlenme sırasıyla: `\begin{soru}[Soru N \foto{...}]` + `\begin{cevap}`.
  Çözüm adım adım, her adımın gerekçesiyle (konu anlatımındakinden daha da açıklayıcı olabilir).
- Tahtada yalnızca sorusu yazılıp çözülmemiş "çalışma soruları/problemler" varsa onları da tam çözümüyle ekle;
  başlığına "(derste çalışma sorusu olarak verildi)" yaz.
- Sonda en az 4–6 adet `\ekal` işaretli ek alıştırma (kaynak kitaplardaki tipik alıştırmalara benzer), tam çözümlü.
- Alt başlıklar (`\subsection`) ile alt konulara ayır.
