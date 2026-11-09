#!/bin/bash
# Kullanim: ./build.sh   (XeLaTeX, pdftocairo ve node gerekir)
cd "$(dirname "$0")"
mkdir -p ../pdf
for f in 02_Soru_Cozumu 03_Konu_Anlatimi_Tum Konu_*.tex; do
  f=${f%.tex}
  for i in 1 2; do xelatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null 2>&1 || { echo "HATA: $f (log: tex/$f.log)"; break; }; done
  [ -f "$f.pdf" ] && mv -f "$f.pdf" ../pdf/ && echo "OK: pdf/$f.pdf"
done
rm -f *.aux *.log *.toc *.out
# HTML sayfalari (../index.html ve ../html/)
python3 html_gen/build_html.py
