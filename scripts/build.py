#!/usr/bin/env python3
"""Tek içerik kaynağından LaTeX ve çevrimdışı web çıktısı. Python stdlib."""
from pathlib import Path
import sys,json,re,html,shutil,subprocess,argparse
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'content'))
from course import TOPICS,SOURCES
PHOTOS=json.loads((BASE/'content/photos.json').read_text())
EXAMPLES=[]
for ti,t in enumerate(TOPICS,1):
 q=0
 for si,s in enumerate(t['sections'],1):
  s['id']=f'bolum-{si}'
  for b in s['blocks']:
   if b['type']=='example':
    q+=1;b['id']=f'soru-{ti}-{q}';b['number']=f'{ti}.{q}';b['topic']=ti;b['section']=si;EXAMPLES.append(b)
 t['count']=q

def tex(s):
 # Metin içindeki matematiği aynen koru, diğer yerlerde TeX özel karakterlerini kaçır.
 parts=re.split(r'(\\\([\s\S]*?\\\))',s)
 for i in range(0,len(parts),2):
  parts[i]=''.join({'&':r'\&','%':r'\%','#':r'\#','_':r'\_','$':r'\$','{':r'\{','}':r'\}'}.get(c,c) for c in parts[i])
 return ''.join(parts).replace(r'\rm üçgen',r'\text{üçgen}').replace(r'\rm dörtyüzlü',r'\text{dörtyüzlü}')

def ht(s):return html.escape(s)
PREAMBLE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=21mm,headheight=16pt]{geometry}
\usepackage{fontspec}\setmainfont{Noto Serif}\setsansfont{Noto Sans}\setmonofont{Noto Sans Mono}
\usepackage{polyglossia}\setdefaultlanguage{turkish}
\usepackage{amsmath,amssymb,mathtools,graphicx,xcolor,booktabs,tabularx,array,enumitem}
\usepackage[most]{tcolorbox}\usepackage{fancyhdr,titlesec,needspace}
\usepackage[unicode,hidelinks,breaklinks]{hyperref}\usepackage{bookmark}
\definecolor{ink}{HTML}{18233A}\definecolor{accent}{HTML}{545AC4}\definecolor{green}{HTML}{087E66}\definecolor{paper}{HTML}{F3F5FA}
\color{ink}\setlength{\parindent}{0pt}\setlength{\parskip}{7pt}\linespread{1.10}
\setlength{\emergencystretch}{3em}\allowdisplaybreaks
\setlist{topsep=4pt,itemsep=4pt,leftmargin=*}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\sffamily\small MÜHENDİSLİK MATEMATİĞİ}\fancyhead[R]{\sffamily\small Ders çalışma notları}\fancyfoot[L]{\sffamily\scriptsize Fotoğraflar + müfredat | 8 Kasım 2026}\fancyfoot[R]{\sffamily\thepage}
\titleformat{\section}{\Large\sffamily\bfseries\color{accent}}{\thesection}{.6em}{}
\titleformat{\subsection}{\large\sffamily\bfseries}{\thesubsection}{.6em}{}
\tcbset{enhanced,breakable,boxrule=.4pt,arc=2mm,left=3mm,right=3mm,top=2mm,bottom=2mm,before skip=8pt,after skip=8pt,fonttitle=\sffamily\bfseries,colback=paper,colframe=accent,coltitle=white}
\newcommand{\notebox}[2]{\begin{tcolorbox}[title={#1},colframe=accent!70!black]#2\end{tcolorbox}}
\hypersetup{pdfauthor={Mühendislik Matematiği Çalışma Atölyesi},pdfsubject={Ders fotoğrafları ve altı başlıklı müfredata göre özgün Türkçe çalışma notları}}
\begin{document}
'''

def source_tex():
 out=[r'\section*{Kaynaklar ve kapsam}',r'\addcontentsline{toc}{section}{Kaynaklar ve kapsam}',tex('Bu metin 156 ders/defter fotoğrafı ve altı başlıklı müfredata göre özgün olarak yazıldı. Fotoğraflar dersin sıra ve örneklerini belirler. Ek sorular pekiştirme olarak etiketlidir; çıkmış sınav sorusu iddiası yoktur. Soluk semboller tahminle aktarılmadı. Gradyan ve yönlü türev, müfredat gereği tamamlanan anlatımdır. Fotoğraf bazında inceleme dizini web sitesinde ve analysis/FOTOGRAF_INCELEMESI.md dosyasında bulunur.')]
 for s in SOURCES:
  out.append(r'\textbf{'+tex(s['title'])+'}. '+tex(s['detail'])+('\n'+r'{\footnotesize\url{'+s['url']+'}}' if s['url'] else '')+r'\par')
 return '\n'.join(out)

def block_tex(b):
 kind=b['type']
 if kind=='p':return tex(b['text'])+'\n\n'
 if kind=='formula':return '\n{\\small\\[\n'+b['text'].replace(r'\rm üçgen',r'\text{üçgen}').replace(r'\rm dörtyüzlü',r'\text{dörtyüzlü}')+'\n\\]}\n'
 if kind=='note':return r'\notebox{'+tex(b['title'])+'}{'+tex(b['text'])+'}\n'
 if kind=='list':return '\\begin{enumerate}\n'+'\n'.join(r'\item '+tex(x) for x in b['items'])+'\n\\end{enumerate}\n'
 if kind=='example':
  typ='Ders fotoğrafından' if b['source'] else 'Pekiştirme'
  out=r'\Needspace{10\baselineskip}\begin{tcolorbox}[title={Örnek '+b['number']+' | '+tex(b['title'])+r'},colframe=accent]'+tex(b['question'])+'\n'
  out+=r'\par\vspace{1mm}{\scriptsize\sffamily '+typ+(r' | \nolinkurl{'+b['source']+'}' if b['source'] else '')+r'}\end{tcolorbox}'+'\n'
  out+=r'\begin{tcolorbox}[title={Adım adım çözüm},colback=green!3!white,colframe=green]'+r'\begin{enumerate}'+'\n'
  out+='\n'.join(r'\item '+tex(x) for x in b['solution'])+'\n'+r'\end{enumerate}\end{tcolorbox}'+'\n'
  return out
 if kind=='figure':return r'\begin{center}\includegraphics[width=.94\linewidth,height=65mm,keepaspectratio]{../assets/figures/'+b['name']+r'.pdf}\par{\small\sffamily '+tex(b['caption'])+r'}\end{center}'+'\n'
 if kind=='table':
  cols=len(b['headers']);out=r'\begin{center}\small\renewcommand{\arraystretch}{1.35}\begin{tabularx}{\linewidth}{'+' '.join([r'>{\raggedright\arraybackslash}X']*cols)+r'}\toprule'+'\n'
  out+=' & '.join(r'\textbf{'+tex(c)+'}' for c in b['headers'])+r'\\\midrule'+'\n'
  out+='\n'.join(' & '.join(tex(c) for c in row)+r'\\' for row in b['rows'])+'\n'+r'\bottomrule\end{tabularx}\end{center}'+'\n';return out
 raise ValueError(kind)

def title_tex(title,desc,label):
 return '\n'.join([r'\hypersetup{pdftitle={'+tex(title)+'}}',r'{\sffamily\small\color{accent} ÇALIŞMA ATÖLYESİ / '+label+r'\par}',r'\vspace{8mm}',r'{\Huge\sffamily\bfseries\raggedright\hyphenpenalty=10000 '+tex(title)+r'\par}',r'\vspace{3mm}',r'{\large '+tex(desc)+r'\par}',r'\vspace{4mm}\hrule\vspace{4mm}'])

def section_heading(s):
 return (r'\Needspace{14\baselineskip}' if s['blocks'] and s['blocks'][0]['type']=='example' else '')+r'\section{'+tex(s['title'])+'}\n'

def make_tex():
 (BASE/'tex/preamble.tex').write_text(PREAMBLE)
 for i,t in enumerate(TOPICS,1):
  body=title_tex(t['title'],t['desc'],f'KONU {i:02}')
  body+=r'\subsection*{Bu bölümün hedefleri}\begin{itemize}'+'\n'+'\n'.join(r'\item '+tex(g) for g in t['goals'])+r'\end{itemize}'
  body+='\n'+r'{\small\tableofcontents}\clearpage'+'\n'
  for s in t['sections']:
   body+=section_heading(s)+''.join(block_tex(b) for b in s['blocks'])
  body+='\n\\clearpage\n'+source_tex()+'\n\\end{document}\n'
  (BASE/'tex'/f'{t["slug"]}.tex').write_text(r'\input{preamble.tex}'+'\n'+body)
 # Soru bankası aynı soru nesnelerinden, tüm çözümleriyle üretilir.
 body=title_tex('Soru çözüm atölyesi','Ders fotoğraflarından alınan örnekler ve ek pekiştirme soruları. Her soruda tam çözüm ve kaynak etiketi.','ÇÖZÜMLÜ SORULAR')
 body+=tex(f'{len(EXAMPLES)} çözümlü örnek. Çıkmış sınav sorusu içermez. Birden fazla alt sorusu bulunan örnekler tek kayıt olarak sayıldı.')+'\n'+r'\tableofcontents\clearpage'+'\n'
 for i,t in enumerate(TOPICS,1):
  body+=r'\clearpage\section{'+tex(t['title'])+'}\n'
  body+=''.join(block_tex(b) for b in EXAMPLES if b['topic']==i)
 body+='\n\\clearpage\n'+source_tex()+'\n\\end{document}\n'
 (BASE/'tex/07-soru-cozumleri.tex').write_text(r'\input{preamble.tex}'+'\n'+body)
 # Birleşik kitap da doğrudan XeLaTeX ile derlenir; PDF birleştirme kısayolu kullanılmaz.
 body=title_tex('Mühendislik matematiği','Altı konunun ayrıntılı anlatımı, tüm çözümlü örnekler, görseller ve kaynak notları.','TAM DERS KİTABI')
 body+=tex('Önerilen sıra: önce tanım ve geometrik yorum, sonra çözümü kapatarak örnek, ardından kaynak fotoğrafı ile karşılaştırma. Her bölümün sonunda yöntem seçimi ve kontrol adımları bulunur.')+'\n'+r'\tableofcontents\clearpage'+'\n'
 for i,t in enumerate(TOPICS,1):
  body+=r'\clearpage\part{'+tex(t['title'])+'}\n'
  for s in t['sections']:body+=section_heading(s)+''.join(block_tex(b) for b in s['blocks'])
 body+='\n\\clearpage\n'+source_tex()+'\n\\end{document}\n'
 (BASE/'tex/08-tum-konular.tex').write_text(r'\input{preamble.tex}'+'\n'+body)

def render_block(b,bank=False):
 kind=b['type']
 if kind=='p':return '<p>'+ht(b['text'])+'</p>'
 if kind=='formula':return '<div class="equation">\\['+ht(b['text'].replace(r'\rm üçgen',r'\text{üçgen}').replace(r'\rm dörtyüzlü',r'\text{dörtyüzlü}'))+'\\]</div>'
 if kind=='note':return '<aside class="callout"><strong>'+ht(b['title'])+'</strong><p>'+ht(b['text'])+'</p></aside>'
 if kind=='list':return '<ol>'+''.join('<li>'+ht(x)+'</li>' for x in b['items'])+'</ol>'
 if kind=='figure':return f'<figure class="diagram"><img loading="lazy" src="assets/figures/{b["name"]}.svg" alt="{ht(b["caption"])}"><figcaption>{ht(b["caption"])}</figcaption></figure>'
 if kind=='table':return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+ht(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+ht(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
 if kind=='example':
  src='<a class="source-link" href="fotograflar.html#'+b['source'][:-4]+'">Ders fotoğrafı ↗</a>' if b['source'] else '<span class="tag">Pekiştirme</span>'
  return f'<article class="exercise" id="{b["id"]}" data-topic="{b["topic"]}" data-origin="{"ders" if b["source"] else "ek"}"><div class="exercise-top"><span class="qnum">{b["number"]}</span>{src}<label class="check"><input type="checkbox" data-study="{b["id"]}"> Çözdüm</label></div><h3>{ht(b["title"])}</h3><p>{ht(b["question"])}</p><details class="solution"><summary>Adım adım çözümü göster</summary><ol>'+''.join('<li>'+ht(x)+'</li>' for x in b['solution'])+'</ol></details></article>'
 raise ValueError(kind)

NAV=lambda:'<a href="index.html">Genel bakış</a>'+''.join(f'<a href="{t["slug"]}.html"><i style="background:{t["color"]}"></i>{i}. {ht(t["title"])}</a>' for i,t in enumerate(TOPICS,1))+'<a href="soru-cozumleri.html">Soru çözüm atölyesi</a><a href="fotograflar.html">Fotoğraf dizini</a><a href="kaynaklar.html">Müfredat ve kaynaklar</a>'
def page(title,body,slug='home',color='#818CF8',aside=''):
 return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Mühendislik matematiği: ders fotoğraflarına dayalı ayrıntılı konu anlatımları, LaTeX PDF notları ve çözümlü sorular."><title>{ht(title)} · Mühendislik Matematiği</title><script>try{{document.documentElement.dataset.theme=localStorage.getItem('muhmat:theme')||'dark'}}catch(e){{document.documentElement.dataset.theme='dark'}}</script><link rel="stylesheet" href="assets/reference.css"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/katex/katex.min.css"><script defer src="assets/katex/katex.min.js"></script><script defer src="assets/search-index.js"></script><script defer src="assets/site.js"></script></head><body data-page="{slug}" style="--accent:{color}"><a href="#main" class="skip-link">İçeriğe geç</a><div class="reading-progress" aria-hidden="true"><span></span></div><header class="topbar"><a class="brand" href="index.html"><span class="brand-dot"></span><span>mühmat<span class="brand-sub"> / çalışma atölyesi</span></span></a><nav class="topnav"><a href="index.html#konular">Konular</a><a href="soru-cozumleri.html">Soru çözümü</a><a href="fotograflar.html">Fotoğraflar</a></nav><div class="tb-actions"><button class="tb-btn" data-search aria-label="İçerikte ara"><span class="ic ic-search"></span><span class="search-label">Ara</span><kbd>Ctrl K</kbd></button><button class="tb-btn" id="themeBtn" aria-label="Açık veya koyu tema"><span class="ic ic-theme"></span></button><button class="tb-btn nav-toggle" id="navToggle" aria-expanded="false" aria-controls="mobileNav" aria-label="Menüyü aç">☰</button></div></header><nav id="mobileNav" class="mobile-nav" hidden>{NAV()}</nav>{f'<div class="reader-layout"><aside class="reader-nav"><div class="nav-title">DERS ROTASI</div>{NAV()}<div class="nav-title">BU SAYFADA</div>{aside}</aside>' if slug not in ['home','photos'] else ''}<main id="main" class="{'home-wrap' if slug=='home' else 'photo-wrap' if slug=='photos' else 'reader'}">{body}</main>{'</div>' if slug not in ['home','photos'] else ''}<footer class="site-footer"><span>Mühendislik Matematiği · 8 Kasım 2026</span><a href="kaynaklar.html">Kapsam ve kaynaklar</a><a href="pdf/08-tum-konular.pdf">Tüm notlar · PDF ↗</a><button id="resetProgress" class="text-button">Çalışma kaydını sıfırla</button></footer><dialog id="searchDialog"><form method="dialog"><button class="close-search" aria-label="Aramayı kapat">Kapat · Esc</button></form><label for="searchInput">Bütün ders notlarında ara</label><input id="searchInput" type="search" placeholder="Örn. eğrilik, düzlem, zincir kuralı…" autocomplete="off"><div id="searchResults" aria-live="polite"></div></dialog></body></html>'''

def make_html():
 n=len(EXAMPLES);direct=sum(bool(b['source']) for b in EXAMPLES)
 hero=f'''<section class="hero"><div><div class="eyebrow"><span></span> DERS FOTOĞRAFLARINDAN ÇALIŞMA NOTLARINA</div><h1>Mühendislik<br><span class="gradient-text">matematiği.</span></h1><p class="lead">Formülü ezberlemekten, <strong>konuyu anlamaya.</strong><br>Tahtadaki konuların açıklamaları, adım adım çözümler ve LaTeX ders notları bir arada.</p><div class="hero-actions"><a class="button primary" href="{TOPICS[0]['slug']}.html">Çalışmaya başla <span>→</span></a><a class="button" href="pdf/08-tum-konular.pdf">Tüm notlar · PDF ↗</a></div><p class="micro">6 müfredat başlığı · çevrimdışı erişim · kendi hızında çalışma</p></div><div class="hero-visual"><div class="orbit-label">GEOMETRİDEN DEĞİŞİME</div><svg viewBox="0 0 400 280" aria-label="Vektör, eğri ve teğet geometrisi" role="img"><defs><linearGradient id="curve"><stop stop-color="#818cf8"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs><g stroke="currentColor" opacity=".16"><path d="M45 235L350 100M45 235L240 265M45 235L45 35"/><path d="M90 215L285 245M140 193L335 223M190 171L385 201M95 243L400 108M145 251L400 138M195 258L400 168"/></g><path d="M60 219C125 195 105 55 190 70S310 230 350 94" fill="none" stroke="url(#curve)" stroke-width="4"/><path d="M145 190L235 40" stroke="#34d399" stroke-width="2"/><circle cx="190" cy="115" r="6" fill="#34d399"/><path d="M45 235L190 115" stroke="#a78bfa" stroke-width="2" stroke-dasharray="5 6"/><g fill="currentColor" font-family="serif" font-style="italic" font-size="19"><text x="348" y="86">r(t)</text><text x="239" y="44">T</text><text x="50" y="31">z</text><text x="240" y="278">x</text><text x="356" y="105">y</text></g></svg><div class="visual-equation">\\(D_{{\\mathbf u}}f=\\nabla f\\cdot\\mathbf u\\)</div><div class="visual-caption">Bir fikir, farklı gösterimler.</div></div></section><section class="stats"><div><b>6</b><span>ayrıntılı konu</span></div><div><b>{n}</b><span>çözümlü örnek</span></div><div><b>156</b><span>ders fotoğrafı</span></div><div><b>8</b><span>LaTeX PDF</span></div></section><section class="continue-panel"><div><span class="eyebrow">SENİN ÇALIŞMA ALANIN</span><h2 id="progressText">Bir konuyla başla.</h2><p>Çalıştığın bölümleri ve çözdüğün soruları işaretle. Kaydın bu tarayıcıda saklanır.</p><a id="resumeLink" href="{TOPICS[0]['slug']}.html">İlk konuya git →</a></div><div class="progress-ring" id="progressRing"><span id="progressPercent">%0</span></div></section><div class="section-heading" id="konular"><div><span class="eyebrow">ADIM ADIM İLERLE</span><h2>Konu anlatımları</h2></div><p>Müfredattaki sırayla, temelden uygulamaya.</p></div><section class="topic-grid">'''
 for i,t in enumerate(TOPICS,1):
  hero+=f'''<article class="topic-card" style="--hue:{t['color']}"><div class="card-line"><span class="number">0{i}</span><a class="pdf-link" href="pdf/{t['slug']}.pdf" aria-label="{ht(t['title'])} PDF">PDF ↗</a></div><h3><a href="{t['slug']}.html">{ht(t['title'])}</a></h3><p>{ht(t['desc'])}</p><div class="card-meta"><span>{len(t['sections'])} alt bölüm</span><span>{t['count']} çözümlü örnek</span></div><div class="card-bottom"><span data-topic-progress="{i}">Henüz başlamadın</span><a href="{t['slug']}.html" aria-label="{ht(t['title'])} konusunu aç">→</a></div></article>'''
 hero+='</section><section class="workshop-banner"><div><span class="eyebrow">ÖNCE KENDİN DENE</span><h2>Soru çözüm atölyesi</h2><p>'+str(direct)+' ders örneği ve '+str(n-direct)+' ek pekiştirme sorusu. Soruları konuya ve kaynağına göre süz; hazır olduğunda çözümü aç.</p></div><a class="button primary" href="soru-cozumleri.html">Soruları çöz →</a></section><section class="home-bottom"><article><h2>Nasıl çalışmalı?</h2><ol><li>Tanımı ve geometrik yorumunu oku.</li><li>Örneği çözümü açmadan kendin dene.</li><li>Adımları karşılaştır, kaynak fotoğrafına dön.</li><li>Çalıştığın alt bölümü işaretle ve PDF ile tekrar et.</li></ol></article><article><h2>Bu notların kaynağı</h2><p>156 fotoğraf ve verilen müfredat esas alındı. Okunabilen ders örnekleri dosya adlarıyla ilişkilendirildi. Gradyan ve yönlü türev müfredatı tamamlayan anlatımdır.</p><a href="fotograflar.html">Fotoğraf inceleme dizini ↗</a><br><a href="kaynaklar.html">Kaynaklara ve kapsam notuna bak ↗</a></article></section>'
 (BASE/'index.html').write_text(page('Çalışma atölyesi',hero))
 for i,t in enumerate(TOPICS,1):
  body=f'<div class="eyebrow">KONU 0{i} / 06</div><h1>{ht(t["title"])}</h1><p class="page-lead">{ht(t["desc"])}</p><div class="page-actions"><a class="button primary" href="pdf/{t["slug"]}.pdf">Konu PDF’sini aç ↗</a><a class="button" href="soru-cozumleri.html?konu={i}">Bu konunun soruları →</a><button class="button" id="toggleSolutions">Tüm çözümleri aç</button></div><aside class="learning-goals"><strong>Bu bölümde ne öğreneceksin?</strong><ul>'+''.join('<li>'+ht(g)+'</li>' for g in t['goals'])+'</ul></aside>'
  aside=''
  for si,s in enumerate(t['sections'],1):
   unit=f'konu-{i}-{si}';aside+=f'<a class="toc-link" href="#{s["id"]}">{si}. {ht(s["title"])}</a>'
   body+=f'<section class="lesson-section" id="{s["id"]}"><div class="section-top"><span>{i}.{si}</span><label class="check"><input type="checkbox" data-study="{unit}"> Çalıştım</label></div><h2>{ht(s["title"])}</h2>'+''.join(render_block(b) for b in s['blocks'])+'</section>'
  body+='<div class="next-prev">'+(f'<a href="{TOPICS[i-2]["slug"]}.html">← Önceki konu</a>' if i>1 else '<a href="index.html">← Genel bakış</a>')+(f'<a href="{TOPICS[i]["slug"]}.html">Sonraki konu →</a>' if i<6 else '<a href="soru-cozumleri.html">Soru atölyesi →</a>')+'</div>'
  (BASE/f'{t["slug"]}.html').write_text(page(t['title'],body,t['slug'],t['color'],aside))
 filters='<div class="filters"><label>Konu<select id="topicFilter"><option value="">Tüm konular</option>'+''.join(f'<option value="{i}">{i}. {ht(t["title"])}</option>' for i,t in enumerate(TOPICS,1))+'</select></label><label>Kaynak<select id="originFilter"><option value="">Bütün sorular</option><option value="ders">Ders fotoğrafından</option><option value="ek">Pekiştirme</option></select></label><label>Sorularda ara<input id="questionSearch" type="search" placeholder="Örn. helis, uzaklık…"></label></div>'
 body=f'<div class="eyebrow">OKU · DENE · KARŞILAŞTIR</div><h1>Soru çözüm atölyesi</h1><p class="page-lead">{n} çözümlü örnek. Çıkmış sınav sorusu yerine ders fotoğraflarındaki örnekler ve özgün pekiştirme soruları.</p><div class="page-actions"><a class="button primary" href="pdf/07-soru-cozumleri.pdf">Çözüm PDF’si ↗</a><button class="button" id="toggleSolutions">Tüm çözümleri aç</button></div>'+filters+f'<p id="filterCount" role="status">{n} soru gösteriliyor</p><div id="questionList">'+''.join(render_block(b,True) for b in EXAMPLES)+'</div><p id="noQuestions" hidden>Bu filtrelerle eşleşen soru bulunamadı.</p>'
 (BASE/'soru-cozumleri.html').write_text(page('Soru çözüm atölyesi',body,'questions','#34D399'))
 body='<div class="eyebrow">KAPSAM VE İZLENEBİLİRLİK</div><h1>Müfredat ve kaynaklar</h1><p class="page-lead">Dersin kapsamı, fotoğrafların nasıl kullanıldığı ve kaynaklara erişim durumu.</p><figure class="syllabus"><img src="assets/mufredat.png" alt="Altı başlıklı mühendislik matematiği ders müfredatı"></figure><h2>Kapsam haritası</h2><ol>'+''.join(f'<li><a href="{t["slug"]}.html">{ht(t["title"])}</a></li>' for t in TOPICS)+'</ol><aside class="callout"><strong>Fotoğraf aktarımı hakkında</strong><p>Fotoğrafların tümü konu bakımından incelendi. Aynı tahtanın farklı açılardan çekimleri ayrı kayıtlarda korundu. Tam okunamayan semboller tahminle soruya dönüştürülmedi. Doğrudan aktarılmış örneklerin fotoğraf bağlantısı bulunur; ek örnekler “Pekiştirme” etiketi taşır. Dosya adındaki tarih, kesin ders tarihi olarak yorumlanmadı.</p></aside><h2>Kaynak kullanımı</h2>'
 for s in SOURCES:body+='<article class="source-item"><h3>'+ht(s['title'])+'</h3><p>'+ht(s['detail'])+'</p>'+(f'<a href="{ht(s["url"])}" target="_blank" rel="noreferrer">Kaynağı aç ↗</a>' if s['url'] else '')+'</article>'
 body+='<h2>LaTeX ve yeniden üretilebilirlik</h2><p>PDF’ler XeLaTeX ile derlendi. Formüller resim olarak yapıştırılmadı. Web anlatımı ve PDF’ler aynı içerik verisinden üretildi. Matematik çizimleri TikZ/PGFPlots ile oluşturuldu. Sitenin çalışması için internet bağlantısı gerekmez; formül motoru ve yazı tipleri yereldir.</p><p><a href="tex-kaynaklari.zip">LaTeX kaynaklarını indir ↗</a> · <a href="pdf/08-tum-konular.pdf">Birleşik ders kitabı ↗</a> · <a href="analysis/FOTOGRAF_INCELEMESI.md">Fotoğraf inceleme raporu ↗</a></p>'
 (BASE/'kaynaklar.html').write_text(page('Müfredat ve kaynaklar',body,'sources'))
 body='<div class="eyebrow">DERSİN İZİ</div><h1>Fotoğraf inceleme dizini</h1><p class="page-lead">156 ders ve defter fotoğrafı. Her kayıtta görülen konular ve doğrudan aktarılan sorular yer alır. Görsele tıklayarak özgün boyutunu açabilirsin.</p><label class="photo-filter">Fotoğraflarda ara<input id="photoSearch" type="search" placeholder="Dosya adı veya konu: örn. silindir, WA0058…"></label><p id="photoCount" role="status">156 fotoğraf</p><div class="photo-grid">'
 for row in PHOTOS:
  linked=[b for b in EXAMPLES if b['source']==row['file']]
  body+=f'<article class="photo-card" id="{row["file"][:-4]}"><a href="assets/photos/{row["file"]}" target="_blank" rel="noreferrer"><img src="assets/thumbs/{row["file"]}" loading="lazy" alt="{ht(row["summary"])}"></a><div><div class="eyebrow">{row["kind"]} · {row["id"]:03}</div><h2>{row["file"]}</h2><p>{ht(row["summary"])}</p><p class="micro">{ht(row["reading"])}</p><div class="photo-links">'+''.join(f'<a href="{TOPICS[j-1]["slug"]}.html">Konu {j} ↗</a>' for j in row['topics'])+''.join(f'<a href="soru-cozumleri.html#{b["id"]}">Örnek {b["number"]} ↗</a>' for b in linked)+'</div></div></article>'
 body+='</div><p id="noPhotos" hidden>Eşleşen fotoğraf bulunamadı.</p>'
 (BASE/'fotograflar.html').write_text(page('Fotoğraf dizini',body,'photos'))
 # Tam metin arama dizini; çözüm adımları da indekslenir.
 search=[]
 for i,t in enumerate(TOPICS,1):
  for s in t['sections']:
   text=' '.join(str(b.get('text',''))+' '+str(b.get('question',''))+' '+' '.join(b.get('solution',[])) for b in s['blocks'])
   search.append(dict(title=t['title']+' · '+s['title'],url=t['slug']+'.html#'+s['id'],text=text))
 for b in EXAMPLES:search.append(dict(title='Örnek '+b['number']+' · '+b['title'],url='soru-cozumleri.html#'+b['id'],text=b['question']+' '+' '.join(b['solution'])))
 (BASE/'assets/search-index.js').write_text('window.SEARCH_INDEX='+json.dumps(search,ensure_ascii=False)+';\nwindow.COURSE_META='+json.dumps([dict(slug=t['slug'],title=t['title'],sections=len(t['sections']),questions=t['count']) for t in TOPICS],ensure_ascii=False)+';')
 (BASE/'content/course.json').write_text(json.dumps(TOPICS,ensure_ascii=False,indent=2))

def compile_pdfs():
 for src in sorted((BASE/'tex').glob('[0-9]*.tex')):
  for run in range(4):
   r=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',src.name],cwd=src.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   if r.returncode:
    print(r.stdout.decode()[-6000:]);raise SystemExit(src.name+' FAILED')
  shutil.copy2(src.with_suffix('.pdf'),BASE/'pdf'/src.with_suffix('.pdf').name)
  print(src.name,'OK',flush=True)

def package():
 # LaTeX archive includes source, corpus and vector figures, so recompilation works.
 import zipfile
 with zipfile.ZipFile(BASE/'tex-kaynaklari.zip','w',zipfile.ZIP_DEFLATED) as z:
  for folder,globs in [('tex',['*.tex']),('content',['*.py','*.json']),('scripts',['*.py']),('assets/figures',['*.tex','*.pdf'])]:
   for glob in globs:
    for path in (BASE/folder).glob(glob):z.write(path,path.relative_to(BASE))
  z.write(BASE/'README.md','README.md')
 dist=BASE/'dist';dist.mkdir(exist_ok=True)
 for p in BASE.glob('*.html'):shutil.copy2(p,dist/p.name)
 for path in ['assets','pdf','analysis']:
  shutil.copytree(BASE/path,dist/path,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.log','*.aux','*.tex','*.out'))
 shutil.copy2(BASE/'tex-kaynaklari.zip',dist/'tex-kaynaklari.zip')
 (BASE/'analysis/build-summary.json').write_text(json.dumps(dict(topics=len(TOPICS),sections=sum(len(t['sections']) for t in TOPICS),examples=len(EXAMPLES),from_photos=sum(bool(b['source']) for b in EXAMPLES),photographs=len(PHOTOS),pdfs=8),indent=2))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--compile',action='store_true');parser.add_argument('--package',action='store_true');args=parser.parse_args()
 make_tex();make_html()
 if args.compile:compile_pdfs()
 if args.package:package()
 print('Generated',len(TOPICS),'topics',len(EXAMPLES),'solved examples')
