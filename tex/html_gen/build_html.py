#!/usr/bin/env python3
"""tex/ kaynaklarından site/index.html ve html/*.html sayfalarını üretir (Mühendislik Matematiği).

Kullanım:  python3 tex/html_gen/build_html.py
Gerekenler: xelatex, pdftocairo, node (KaTeX ile formülleri önceden işlemek için).
TikZ/pgfplots çizimleri LaTeX ile derlenip SVG'ye çevrilir (html/assets/gfx, önbellekli).
"""
import hashlib
import html as H
import json
import math
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

GEN = Path(__file__).resolve().parent
TEX = GEN.parent
ROOT = TEX.parent
OUT = ROOT / 'html'
AS = OUT / 'assets'
GFX = AS / 'gfx'
BUILD = GEN / '.build'

# eski sayfa adresleri -> yeni sayfa
REDIRECTS = {}

DOCS = [
    dict(src='02_Soru_Cozumu', out='soru-cozumu', hue='#34D399', group='sinav', label='Soru çözümü',
         desc='Derste tahtada çözülen bütün örnekler konu konu, soru metni ve adım adım çözümüyle; kaynak kitaplardan ek alıştırmalar.'),
    dict(src='Konu_01_vektorler', out='konu-01-vektorler', hue='#60A5FA', group='konu', label='3B koordinatlar ve vektörler', no='1',
         desc='Üç boyutlu koordinat sistemi, vektör cebiri, skaler (iç) çarpım, vektörel çarpım ve karma çarpım.'),
    dict(src='Konu_02_dogru_duzlem', out='konu-02-dogru-duzlem', hue='#C084FC', group='konu', label='Doğru, düzlem ve yüzeyler', no='2',
         desc='Doğru ve düzlem denklemleri, uzaklıklar, açılar; silindirler ve kuadratik yüzeyler.'),
    dict(src='Konu_03_vektor_fonksiyon', out='konu-03-vektor-fonksiyon', hue='#F472B6', group='konu', label='Vektör fonksiyonları ve uzay eğrileri', no='3',
         desc='Uzay eğrileri, türev ve integral, yay uzunluğu, eğrilik, TNB çatısı, hız ve ivme.'),
    dict(src='Konu_04_limit_sureklilik', out='konu-04-limit-sureklilik', hue='#2DD4BF', group='konu', label='Çok değişkenli fonksiyonlar, limit, süreklilik', no='4',
         desc='Tanım kümesi, seviye eğrileri, iki değişkenli limit, yol testi, kutupsal koordinat ve süreklilik.'),
    dict(src='Konu_05_kismi_turev', out='konu-05-kismi-turev', hue='#FBBF24', group='konu', label='Kısmi türevler ve teğet düzlem', no='5',
         desc='Kısmi türev, yüksek mertebeden türevler, Clairaut, teğet düzlem, lineer yaklaşım ve diferansiyel.'),
    dict(src='Konu_06_zincir_gradyan', out='konu-06-zincir-gradyan', hue='#22D3EE', group='konu', label='Zincir kuralı, yönlü türev, gradyan', no='6',
         desc='Zincir kuralı ve ağaç diyagramı, kapalı türev, yönlü türev, gradyan vektörü ve seviye yüzeylerine teğet düzlem.'),
    dict(src='03_Konu_Anlatimi_Tum', out='konu-tumu', hue='#E879F9', group='konu', label='Tüm konular tek sayfada', no='∑',
         desc='Altı konunun hepsi art arda; baştan sona tekrar için.'),
]

COLORS = {'ana': '#1F4E79', 'vurgu': '#C00000', 'yesil': '#2E7D32', 'turuncu': '#E65100', 'gri': '#555555',
          'red': '#C00000', 'blue': '#1F4E79', 'green': '#2E7D32', 'orange': '#E65100', 'violet': '#6B3FA0',
          'black': '#222222', 'gray': '#555555', 'mor': '#6B3FA0'}
GRAPHIC_ENVS = ('tikzpicture', 'forest')
WARN = Counter()

TR = str.maketrans('çğıöşüÇĞİÖŞÜâîû', 'cgiosucgiosuaiu')


def slug(t):
    t = t.translate(TR).lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:60] or 'b'


# ------------------------------------------------------------------ okuma yardımcıları
def read_group(s, i):
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('kapanmayan { : ' + s[i:i + 80])


def read_opt(s, i):
    depth = bd = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            bd += 1
        elif c == '}':
            bd -= 1
        elif bd == 0 and c == '[':
            depth += 1
        elif bd == 0 and c == ']':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('kapanmayan [ : ' + s[i:i + 80])


def ws(s, i):
    """Argümandan önceki boşlukları atla (boş satırı geçmeden)."""
    j = i
    nl = 0
    while j < len(s) and s[j] in ' \t\n':
        if s[j] == '\n':
            nl += 1
            if nl > 1:
                return i
        j += 1
    return j


def arg(s, i):
    j = ws(s, i)
    if j < len(s) and s[j] == '{':
        return read_group(s, j)
    m = re.compile(r'\\([A-Za-z]+|.)').match(s, j)
    if m:
        return m.group(0), m.end()
    return s[j:j + 1], j + 1


def opt(s, i):
    j = ws(s, i)
    if j < len(s) and s[j] == '[':
        return read_opt(s, j)
    return None, i


def env_body(s, i, name):
    pat = re.compile(r'\\(begin|end)\{' + re.escape(name) + r'\}')
    depth = 1
    for m in pat.finditer(s, i):
        depth += 1 if m.group(1) == 'begin' else -1
        if depth == 0:
            return s[i:m.start()], m.end()
    raise ValueError('kapanmayan ortam ' + name)


def strip_comments(s):
    return re.sub(r'(?<!\\)%.*', '', s)


def top_split(s, pattern):
    """pattern'in süslü parantez ve ortam dışında kalan eşleşmelerinden böl."""
    rx = re.compile(pattern)
    parts = []
    last = 0
    depth = env = 0
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '%':
            j = s.find('\n', i)
            i = n if j < 0 else j
            continue
        if depth == 0 and env == 0:
            m = rx.match(s, i)
            if m:
                parts.append(s[last:i])
                last = i = m.end()
                continue
        if c == '\\':
            if s.startswith('\\begin{lstlisting}', i):
                _, k = env_body(s, i + 18, 'lstlisting')
                i = k
                continue
            if s.startswith('\\begin{', i):
                env += 1
            elif s.startswith('\\end{', i):
                env -= 1
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        i += 1
    parts.append(s[last:])
    return parts


# ------------------------------------------------------------------ makrolar ve belge kaynağı
def expand_inputs(s, depth=0):
    def rep(m):
        name = m.group(2)
        if m.group(1) == 'frag':
            name = 'frag/' + name
        p = TEX / (name if name.endswith('.tex') else name + '.tex')
        return expand_inputs(p.read_text(encoding='utf-8'), depth + 1)
    return re.sub(r'\\(input|frag)\{([^}]+)\}', rep, s)


def parse_macros(src):
    """\\newcommand tanımlarından grafik üreten makroları bul: ad -> (argüman sayısı, varsayılan opsiyon var mı)."""
    out = {}
    for m in re.finditer(r'\\newcommand\{\\(\w+)\}(?:\[(\d)\])?(\[[^\]]*\])?', src):
        try:
            body, _ = read_group(src, ws(src, m.end()))
        except ValueError:
            continue
        if 'tikzpicture' in body or 'forest' in body:
            n = int(m.group(2) or 0)
            out[m.group(1)] = (n - (1 if m.group(3) else 0), bool(m.group(3)))
    return out


GMACROS = {}
PREAMBLE_DEFS = []
MATH = []
GFXREG = {}
# diyagram önbelleği yalnızca çağrı metnine değil, makro tanımlarına da bağlı olmalı
GFX_SALT = (TEX / 'ortak.sty').read_text(encoding='utf-8')


def math_ph(tex, display):
    MATH.append((tex.strip(), display))
    return f'\x01M{len(MATH) - 1}\x02'


def gfx_ph(raw, kind):
    h = hashlib.sha1((GFX_SALT + raw).encode()).hexdigest()[:12]
    GFXREG[h] = raw
    return f'\x01G{h}:{kind}\x02'


# ------------------------------------------------------------------ çıktı biriktirici
class Out:
    def __init__(self):
        self.items = []
        self.styles = []
        self.buf = []

    def wrap(self, h):
        if not self.styles:
            return h
        return ''.join(o for o, _ in self.styles) + h + ''.join(c for _, c in reversed(self.styles))

    def flush(self):
        if self.buf:
            self.items.append(('i', self.wrap(''.join(self.buf))))
            self.buf = []

    def text(self, t):
        self.buf.append(t)

    def inline(self, h):
        self.flush()
        self.items.append(('i', self.wrap(h)))

    def block(self, h, kind='b'):
        self.flush()
        self.items.append((kind, h))

    def extend(self, sub):
        self.flush()
        for k, h in sub:
            self.items.append((k, self.wrap(h) if k == 'i' else h))

    def done(self):
        self.flush()
        return self.items


def is_blank(h):
    return re.sub(r'(\s|&nbsp;|&emsp;|&thinsp;|<br>)+', '', h) == ''


def render_block(items):
    out = []
    para = []
    row = []

    def flush_para():
        h = ''.join(para)
        h = re.sub(r'^(\s|<br>)+|(\s|<br>)+$', '', h)
        if not is_blank(h):
            out.append(f'<p>{h}</p>')
        para.clear()

    def flush_row():
        if row:
            out.append('<div class="mprow">' + ''.join(row) + '</div>')
            row.clear()

    for k, h in items:
        if k == 'flag':
            continue
        if k == 'mp':
            flush_para()
            row.append(h)
            continue
        if k == 'p':
            flush_para()
            continue
        if k == 'hfill':
            if not row:
                para.append(' ')
            continue
        if row and k in ('i', 'br') and is_blank(h):
            continue
        flush_row()
        if k in ('i', 'br'):
            para.append(h)
        else:
            flush_para()
            out.append(h)
    flush_para()
    flush_row()
    return '\n'.join(out)


def render_inline(items):
    r = []
    for k, h in items:
        if k == 'flag':
            continue
        if k == 'p':
            r.append(' ')
        elif k == 'mp':
            r.append(h)
        else:
            r.append(h)
    return ''.join(r).strip()


def render_cell(items):
    if any(k in ('b', 'g', 'mp') for k, _ in items):
        return render_block(items)
    return render_inline(items)


# ------------------------------------------------------------------ kod renklendirme
KW = set('while for if else return int double bool void class struct public private new delete NULL true false '
         'do break continue string char float nullptr this template typename const'.split())


def highlight(code):
    out = []
    for m in re.finditer(r'(//[^\n]*)|("[^"\n]*")|(\b\d+\b)|(\w+)|(\s+)|(.)', code):
        t = H.escape(m.group(0), quote=False)
        if m.group(1):
            out.append(f'<span class="k-c">{t}</span>')
        elif m.group(2):
            out.append(f'<span class="k-s">{t}</span>')
        elif m.group(3):
            out.append(f'<span class="k-n">{t}</span>')
        elif m.group(4) and m.group(0) in KW:
            out.append(f'<span class="k-k">{t}</span>')
        else:
            out.append(t)
    return ''.join(out)


def color_class(c):
    base = re.split(r'[!]', c.strip())[0]
    return 'c-' + (base if base in COLORS else 'ana')


# ------------------------------------------------------------------ tablolar
def parse_spec(spec):
    for _ in range(5):
        spec = re.sub(r'\*\{(\d+)\}\{([^{}]*)\}', lambda m: m.group(2) * int(m.group(1)), spec)
    out = []
    i = 0
    while i < len(spec):
        c = spec[i]
        if c in '><@!':
            j = ws(spec, i + 1)
            if j < len(spec) and spec[j] == '{':
                _, i = read_group(spec, j)
                continue
        elif c in 'lcr':
            out.append(c)
        elif c in 'pmb':
            j = ws(spec, i + 1)
            if j < len(spec) and spec[j] == '{':
                _, i = read_group(spec, j)
                out.append('l')
                continue
        elif c == 'X':
            out.append('l')
        i += 1
    return out


RULES = re.compile(r'\\(toprule|midrule|bottomrule|hline|endhead|endfirsthead|endfoot|endlastfoot)\b'
                   r'|\\cmidrule(\([^)]*\))?\{[^}]*\}')


# ------------------------------------------------------------------ dönüştürücü
class Conv:
    def __init__(self):
        self.heads = []
        self.cnt = [0, 0, 0]
        self.ids = set()
        self.stats = Counter()
        self.unknown = Counter()

    def uid(self, base):
        b = base
        k = 2
        while b in self.ids:
            b = f'{base}-{k}'
            k += 1
        self.ids.add(b)
        return b

    # --------------------------------------------------------------
    def conv(self, s, tt=False):
        o = Out()
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c == '%':
                j = s.find('\n', i)
                if j < 0:
                    break
                i = j + 1
                while i < n and s[i] in ' \t':
                    i += 1
                continue
            if c == '\\':
                i = self.command(s, i, o, tt)
                continue
            if c == '{':
                body, i = read_group(s, i)
                o.extend(self.conv(body, tt))
                continue
            if c == '}':
                i += 1
                continue
            if c == '$':
                if s.startswith('$$', i):
                    j = s.find('$$', i + 2)
                    o.block('<div class="mathd">' + math_ph(s[i + 2:j], True) + '</div>')
                    i = j + 2
                    continue
                j = i + 1
                while j < n and s[j] != '$':
                    j += 2 if s[j] == '\\' else 1
                o.inline(math_ph(s[i + 1:j], False))
                i = j + 1
                continue
            if c == '\n':
                j = i + 1
                while j < n and s[j] in ' \t':
                    j += 1
                if j < n and s[j] == '\n':
                    o.flush()
                    o.items.append(('p', ''))
                    while j < n and s[j] in ' \t\n':
                        j += 1
                    i = j
                else:
                    o.text(' ')
                    i = j
                continue
            if c in ' \t':
                o.text(' ')
                while i < n and s[i] in ' \t':
                    i += 1
                continue
            if c == '~':
                o.text('&nbsp;')
            elif c == '-' and not tt and s.startswith('---', i):
                o.text('—')
                i += 3
                continue
            elif c == '-' and not tt and s.startswith('--', i):
                o.text('–')
                i += 2
                continue
            elif c == '`' and s.startswith('``', i):
                o.text('“')
                i += 2
                continue
            elif c == "'" and s.startswith("''", i):
                o.text('”')
                i += 2
                continue
            elif c in '<>&"':
                o.text(H.escape(c))
            else:
                o.text(c)
            i += 1
        return o.done()

    def inl(self, s, tt=False):
        return render_inline(self.conv(s, tt))

    # --------------------------------------------------------------
    def pure_graphic(self, x):
        t = strip_comments(x).strip()
        m = re.match(r'\\begin\{(tikzpicture|forest)\}', t)
        if m:
            body, k = env_body(t, m.end(), m.group(1))
            if m.group(1) == 'tikzpicture' and is_bar_chart(body):
                return False
            return t[k:].strip() == ''
        m = re.match(r'\\([A-Za-z]+)', t)
        if not m:
            return False
        name = m.group(1)
        j = m.end()
        if name in GMACROS:
            nargs, hasopt = GMACROS[name]
            if hasopt:
                _, j = opt(t, j)
            for _ in range(nargs):
                _, j = arg(t, j)
            return t[j:].strip() == ''
        if name in ('scalebox', 'sigdir', 'resizebox'):
            k = {'scalebox': 2, 'sigdir': 1, 'resizebox': 3}[name]
            a = None
            for _ in range(k):
                a, j = arg(t, j)
            return t[j:].strip() == '' and self.pure_graphic(a)
        return False

    def unwrap(self, x):
        t = strip_comments(x).strip()
        m = re.match(r'\\(scalebox|sigdir|resizebox)\b', t)
        if not m:
            return t
        k = {'scalebox': 2, 'sigdir': 1, 'resizebox': 3}[m.group(1)]
        j = m.end()
        a = t
        for _ in range(k):
            a, j = arg(t, j)
        return self.unwrap(a)

    def graphic(self, o, raw, kind):
        self.stats['gfx'] += 1
        o.block(gfx_ph(raw.strip(), kind), 'g')

    def gkind(self, raw):
        if 'forest' in raw:
            return 'tree'
        if re.search(r'\\ak|\[ak', raw):
            return 'flow'
        return 'fig'

    # --------------------------------------------------------------
    def command(self, s, i, o, tt):
        m = re.compile(r'\\([A-Za-z]+\*?|.)', re.S).match(s, i)
        name = m.group(1)
        j = m.end()
        letters = name[0].isalpha()

        def eat_space(k):
            if not letters:
                return k
            return ws(s, k)

        # --- tek karakterli komutlar
        if name in ('\\', 'newline'):
            if j < len(s) and s[j] == '*':
                j += 1
            _, j = opt(s, j)
            o.flush()
            o.items.append(('br', '<br>'))
            return j
        if not letters:
            if name in '%&_#${}':
                o.text(H.escape(name))
            elif name == ',':
                o.text('&thinsp;')
            elif name in ';: \n':
                o.text(' ')
            elif name == '(':
                k = s.find('\\)', j)
                o.inline(math_ph(s[j:k], False))
                return k + 2
            elif name == '[':
                k = s.find('\\]', j)
                o.block('<div class="mathd">' + math_ph(s[j:k], True) + '</div>')
                return k + 2
            return j

        base = name.rstrip('*')

        if base == 'begin':
            env, k = arg(s, j)
            return self.env(env, s, i, k, o, tt)
        if base == 'end':
            _, k = arg(s, j)
            return k

        # --- başlıklar
        if base in ('section', 'subsection', 'subsubsection'):
            _, j = opt(s, j)
            title, j = arg(s, j)
            lvl = {'section': 2, 'subsection': 3, 'subsubsection': 4}[base]
            if not name.endswith('*'):
                d = lvl - 2
                self.cnt[d] += 1
                for z in range(d + 1, 3):
                    self.cnt[z] = 0
                num = '.'.join(str(x) for x in self.cnt[:d + 1])
            else:
                num = ''
            th = self.inl(title)
            tid = self.uid(slug(re.sub(r'<[^>]+>|\x01[^\x02]*\x02', '', th)))
            o.block(f'<h{lvl} id="{tid}" class="h"><span class="num">{num}</span>'
                    f'<span class="ht">{th}</span></h{lvl}>')
            self.heads.append((lvl, num, th, tid))
            return j
        if base == 'kart':
            title, j = arg(s, j)
            th = self.inl(title)
            tid = self.uid('kart-' + slug(re.sub(r'<[^>]+>|\x01[^\x02]*\x02', '', th)))
            o.block(f'<h4 id="{tid}" class="h kart"><span class="ht">{th}</span></h4>')
            self.heads.append((5, '', th, tid))
            self.stats['kart'] += 1
            return j
        if base == 'setcounter':
            cname, j = arg(s, j)
            val, j = arg(s, j)
            if cname == 'section':
                self.cnt = [int(val), 0, 0]
            return j

        # --- grafik makroları
        if base in GMACROS:
            nargs, hasopt = GMACROS[base]
            k = j
            if hasopt:
                _, k = opt(s, k)
            for _ in range(nargs):
                _, k = arg(s, k)
            self.graphic(o, s[i:k], 'flow')
            return k
        if base in ('scalebox', 'sigdir', 'resizebox', 'adjustbox', 'centerline', 'mbox', 'makebox', 'fbox'):
            nreq = {'scalebox': 2, 'sigdir': 1, 'resizebox': 3, 'adjustbox': 2, 'centerline': 1,
                    'mbox': 1, 'makebox': 1, 'fbox': 1}[base]
            k = j
            if base == 'makebox':
                _, k = opt(s, k)
                _, k = opt(s, k)
            args = []
            for _ in range(nreq):
                a, k = arg(s, k)
                args.append(a)
            x = args[-1]
            if self.pure_graphic(x):
                raw = self.unwrap(x)  # küçültmeyi tarayıcı yapar (max-width), ağaçlar okunur boyutta kalsın
                self.graphic(o, raw, self.gkind(raw))
            elif base == 'centerline':
                o.block('<div class="center">' + render_block(self.conv(x, tt)) + '</div>')
            else:
                o.extend(self.conv(x, tt))
            return k

        # --- satır içi biçimler
        WRAP = {'textbf': ('<strong>', '</strong>'), 'textit': ('<em>', '</em>'), 'emph': ('<em>', '</em>'),
                'texttt': ('<code class="tt">', '</code>'), 'underline': ('<u>', '</u>'),
                'vurg': ('<strong class="vurg">', '</strong>'), 'alinti': ('<q class="alinti">', '</q>'),
                'textsuperscript': ('<sup>', '</sup>'), 'textsubscript': ('<sub>', '</sub>'),
                'textrm': ('', ''), 'textsf': ('', ''), 'textsc': ('<span class="sc">', '</span>'),
                'textnormal': ('', ''), 'text': ('', ''), 'textup': ('', '')}
        if base in WRAP:
            a, j = arg(s, j)
            op, cl = WRAP[base]
            o.inline(op + self.inl(a, tt or base == 'texttt') + cl)
            return j
        if base == 'foto':
            a, j = arg(s, j)
            t = H.escape(strip_comments(a).strip())
            o.inline(f'<span class="zd" title="Tahta fotoğrafı (dosya adı)">foto {t}</span>')
            return j
        if base == 'texorpdfstring':
            a, j = arg(s, j)
            _, j = arg(s, j)
            o.extend(self.conv(a, tt))
            return j
        if base == 'ekal':
            o.inline('<span class="ekal">Ek alıştırma</span> ')
            return eat_space(j)
        if base == 'okunamadi':
            a, j = arg(s, j)
            o.inline('<em class="okunamadi">(fotoğrafta okunamadı: ' + self.inl(a) + ')</em>')
            return j
        if base == 'textcolor':
            c, j = arg(s, j)
            a, j = arg(s, j)
            o.inline(f'<span class="{color_class(c)}">' + self.inl(a, tt) + '</span>')
            return j
        if base in ('href',):
            u, j = arg(s, j)
            a, j = arg(s, j)
            o.inline(f'<a href="{H.escape(u)}">' + self.inl(a) + '</a>')
            return j
        if base == 'url':
            u, j = arg(s, j)
            o.inline(f'<a href="{H.escape(u)}">{H.escape(u)}</a>')
            return j
        if base == 'footnote':
            a, j = arg(s, j)
            o.inline(f'<span class="fn">({self.inl(a)})</span>')
            return j
        if base == 'multicolumn':
            _, j = arg(s, j)
            _, j = arg(s, j)
            a, j = arg(s, j)
            o.extend(self.conv(a, tt))
            return j
        if base == 'multirow':
            _, j = arg(s, j)
            _, j = arg(s, j)
            a, j = arg(s, j)
            o.extend(self.conv(a, tt))
            return j

        # --- bildirimler
        DECL = {'bfseries': ('<strong>', '</strong>'), 'itshape': ('<em>', '</em>'), 'em': ('<em>', '</em>'),
                'ttfamily': ('<span class="tt">', '</span>'),
                'footnotesize': ('<span class="fs-s">', '</span>'), 'scriptsize': ('<span class="fs-s">', '</span>'),
                'tiny': ('<span class="fs-s">', '</span>'),
                'large': ('<span class="fs-l">', '</span>'), 'Large': ('<span class="fs-l">', '</span>'),
                'LARGE': ('<span class="fs-l">', '</span>'), 'huge': ('<span class="fs-l">', '</span>')}
        if base in DECL:
            o.flush()
            o.styles.append(DECL[base])
            return eat_space(j)
        if base == 'color':
            c, j = arg(s, j)
            o.flush()
            o.styles.append((f'<span class="{color_class(c)}">', '</span>'))
            return j
        if base in ('small', 'normalsize', 'normalfont', 'raggedright', 'raggedleft', 'upshape', 'mdseries',
                    'rmfamily', 'sffamily'):
            return eat_space(j)
        if base == 'centering':
            o.flush()
            o.items.append(('flag', 'center'))
            return eat_space(j)

        # --- semboller
        SYM = {'quad': '&emsp;', 'qquad': '&emsp;&emsp;', 'dots': '…', 'ldots': '…', 'checkmark': '✓',
               'triangleright': '▸', 'textasciitilde': '~', 'S': '§', 'textbackslash': '\\', 'LaTeX': 'LaTeX',
               'TeX': 'TeX', 'textbullet': '•', 'textendash': '–', 'textemdash': '—', 'i': 'ı',
               'textless': '&lt;', 'textgreater': '&gt;', 'enspace': '&ensp;', 'space': ' ', 'today': '9 Kasım 2026',
               'times': '×', 'to': '→', 'Rightarrow': '⇒', 'leftrightarrow': '↔', 'rightarrow': '→'}
        if base in SYM:
            o.text(SYM[base])
            return eat_space(j) if base not in ('quad', 'qquad') else ws(s, j)

        # --- paragraf ve boşluk
        if base in ('par', 'medskip', 'bigskip', 'smallskip', 'clearpage', 'newpage', 'pagebreak'):
            o.flush()
            o.items.append(('p', ''))
            if base == 'pagebreak':
                _, j = opt(s, j)
            return eat_space(j)
        if base == 'hfill':
            o.flush()
            o.items.append(('hfill', ''))
            return eat_space(j)
        if base in ('noindent', 'nopagebreak', 'maketitle', 'tableofcontents', 'protect', 'relax', 'item',
                    'toprule', 'midrule', 'bottomrule', 'hline', 'endhead', 'null', 'leavevmode', 'linebreak'):
            return eat_space(j)
        ONEARG = ('thispagestyle', 'pagestyle', 'vspace', 'needspace', 'label', 'phantom', 'hphantom',
                  'vphantom', 'enlargethispage', 'addvspace')
        if base in ONEARG:
            _, j = arg(s, j)
            return j
        if base == 'hspace':
            _, j = arg(s, j)
            o.text(' ')
            return j
        if base in ('setlength', 'addtolength', 'rule', 'addtocontents'):
            _, j = opt(s, j)
            _, j = arg(s, j)
            _, j = arg(s, j)
            return j

        self.unknown[base] += 1
        return eat_space(j)

    # --------------------------------------------------------------
    def env(self, name, s, i0, j, o, tt):
        if name in GRAPHIC_ENVS:
            body, k = env_body(s, j, name)
            if name == 'tikzpicture' and is_bar_chart(body):
                o.block(chart_html(self, body))
                self.stats['chart'] += 1
            else:
                raw = s[i0:k]
                self.graphic(o, raw, self.gkind(raw))
            return k
        if name == 'lstlisting':
            _, j = opt(s, j)
            k = s.find('\\end{lstlisting}', j)
            code = s[j:k].strip('\n')
            code = re.sub(r'\n\s*$', '', code)
            o.block(f'<div class="code"><pre><code>{highlight(code)}</code></pre></div>')
            self.stats['code'] += 1
            return k + len('\\end{lstlisting}')

        spec = {'minipage': 'om', 'tabular': 'om', 'tabularx': 'mm', 'longtable': 'om', 'tabular*': 'mom',
                'itemize': 'o', 'enumerate': 'o', 'description': 'o', 'tahta': 'o', 'dikkat': 'o', 'bilgi': 'o',
                'soru': 'o', 'cevap': 'o', 'tanim': 'o', 'teorem': 'o', 'ozet': 'o', 'adjustbox': 'm'}.get(name, '')
        args = []
        for t in spec:
            if t == 'o':
                a, j = opt(s, j)
            else:
                a, j = arg(s, j)
            args.append(a)
        body, k = env_body(s, j, name)

        if name in ('itemize', 'enumerate', 'description'):
            o.block(self.listing(name, body))
        elif name in ('center', 'flushleft', 'flushright'):
            cls = {'center': 'center', 'flushleft': 'left', 'flushright': 'right'}[name]
            o.block(f'<div class="{cls}">' + render_block(self.conv(body, tt)) + '</div>')
        elif name == 'minipage':
            w = args[1]
            mm = re.match(r'\s*([\d.]*)\s*\\(linewidth|textwidth|columnwidth|hsize)', w)
            if mm:
                frac = float(mm.group(1) or 1)
            else:
                mm = re.match(r'\s*([\d.]+)\s*cm', w)
                frac = float(mm.group(1)) / 16.6 if mm else 0.5
            items = self.conv(body, tt)
            center = any(k_ == 'flag' for k_, _ in items)
            o.block(f'<div class="mp{" center" if center else ""}" style="--w:{frac:.3f}">'
                    + render_block(items) + '</div>', 'mp')
        elif name in ('tabular', 'tabularx', 'longtable', 'tabular*'):
            o.block(self.table(args[-1], body, name == 'longtable'))
        elif name in ('tahta', 'dikkat', 'bilgi', 'soru', 'cevap', 'tanim', 'teorem', 'ozet'):
            o.block(self.box(name, args[0], body))
        elif name == 'cozum':
            # sorunun altındaki çözüm bloğu: varsayılan kapalı, başlığı aç/kapa düğmesi
            self.stats['cozum'] += 1
            o.block('<details class="box box-cozum"><summary class="box-h"><i class="shape s-basla"></i>'
                    '<span class="bt">Çözüm</span><span class="tog" aria-hidden="true"></span></summary>'
                    '<div class="box-b">' + render_block(self.conv(body)) + '</div></details>')
        elif name in ('equation', 'equation*', 'align', 'align*', 'displaymath', 'gather*'):
            tex = body if 'align' not in name else '\\begin{aligned}' + body + '\\end{aligned}'
            o.block('<div class="mathd">' + math_ph(tex, True) + '</div>')
        elif name in ('quote', 'quotation'):
            o.block('<blockquote>' + render_block(self.conv(body, tt)) + '</blockquote>')
        else:
            if name not in ('adjustbox',):
                self.unknown['env:' + name] += 1
            o.extend(self.conv(body, tt))
        return k

    def listing(self, name, body):
        parts = top_split(body, r'\\item\b')
        lis = []
        for p in parts[1:]:
            label = None
            if re.match(r'\s*\[', p):
                label, k = read_opt(p, p.index('['))
                p = p[k:]
            inner = render_block(self.conv(p))
            if inner.startswith('<p>') and inner.endswith('</p>') and inner.count('<p>') == 1:
                inner = inner[3:-4]
            lab = f'<strong class="lab">{self.inl(label)}</strong> ' if label else ''
            lis.append(f'<li>{lab}{inner}</li>')
        tag = {'itemize': 'ul', 'enumerate': 'ol', 'description': 'ul'}[name]
        return f'<{tag} class="l">' + ''.join(lis) + f'</{tag}>'

    def box(self, name, title, body):
        shape = {'tahta': 'ekran', 'dikkat': 'karar', 'bilgi': 'islem', 'soru': 'giris', 'cevap': 'basla',
                 'tanim': 'islem', 'teorem': 'karar', 'ozet': 'giris'}[name]
        default = {'tahta': 'Derste tahtada', 'dikkat': 'Sık yapılan hatalar', 'bilgi': 'Bilgi', 'soru': 'Soru',
                   'cevap': 'Çözüm', 'tanim': 'Tanım', 'teorem': 'Teorem / Formül', 'ozet': 'Özet ve formül kutusu'}[name]
        t = self.inl(title) if title is not None else ''
        if name == 'tahta':
            t = default + (' ' + t if t else '')
        elif name in ('tanim', 'teorem'):
            t = default + (' – ' + t if t else '')
        elif not t:
            t = default
        self.stats[name] += 1
        inner = render_block(self.conv(body))
        if name == 'cevap':
            return (f'<details class="box box-cevap" open><summary class="box-h"><i class="shape s-{shape}"></i>'
                    f'<span class="bt">{t}</span><span class="tog" aria-hidden="true"></span></summary>'
                    f'<div class="box-b">{inner}</div></details>')
        extra = f' id="{self.uid("soru-" + str(self.stats["soru"]))}"' if name == 'soru' else ''
        return (f'<section class="box box-{name}"{extra}><div class="box-h"><i class="shape s-{shape}"></i>'
                f'<span class="bt">{t}</span></div><div class="box-b">{inner}</div></section>')

    def table(self, spec, body, longt):
        aligns = parse_spec(spec)
        body = strip_comments(body)
        rows = top_split(body, r'\\\\(?:\s*\[[^\]]*\])?')
        mid = re.search(r'\\midrule|\\endhead', body)
        head, rows_out = [], []
        pos = 0
        for r in rows:
            start = pos
            pos += len(r) + 2
            is_head = mid is not None and start < mid.start() and '\\endhead' not in r[:0] \
                and not re.match(r'\s*\\midrule', r)
            clean = RULES.sub('', r).strip()
            if not clean:
                continue
            cells = top_split(clean, r'&')
            tds = []
            ci = 0
            for cell in cells:
                span = 1
                mm = re.match(r'\s*\\multicolumn\{(\d+)\}\{([^}]*)\}', cell)
                al = aligns[ci] if ci < len(aligns) else 'l'
                if mm:
                    span = int(mm.group(1))
                    al = (parse_spec(mm.group(2)) or ['c'])[0]
                    cell, _ = arg(cell, mm.end())
                tag = 'th' if is_head else 'td'
                cls = {'c': ' class="ac"', 'r': ' class="ar"'}.get(al, '')
                sp = f' colspan="{span}"' if span > 1 else ''
                tds.append(f'<{tag}{cls}{sp}>{render_cell(self.conv(cell.strip()))}</{tag}>')
                ci += span
            (head if is_head else rows_out).append('<tr>' + ''.join(tds) + '</tr>')
        cls = 'tbl'
        if longt and len(rows_out) >= 5:
            cls += ' trace'
        if len(rows_out) > 14:
            cls += ' long'
        self.stats['table'] += 1
        th = f'<thead>{"".join(head)}</thead>' if head else ''
        return f'<div class="tbl-wrap"><table class="{cls}">{th}<tbody>{"".join(rows_out)}</tbody></table></div>'


# ------------------------------------------------------------------ grafikler (pgfplots -> HTML)
def is_bar_chart(body):
    """Yalnızca çubuk grafikler HTML'e çevrilir; fonksiyon/yüzey çizimleri SVG olarak derlenir."""
    m = re.search(r'\\begin\{axis\}\s*\[([^\]]*)', body)
    return bool(m) and re.search(r'\\b[xy]bar\\b', m.group(1)) is not None and 'coordinates' in body


def axis_opt(opts, key):
    m = re.search(r'(?:^|[,\[\s])' + re.escape(key) + r'\s*=\s*', opts)
    if not m:
        return None
    j = m.end()
    if j < len(opts) and opts[j] == '{':
        v, _ = read_group(opts, j)
        return v
    m2 = re.match(r'[^,\]]*', opts[j:])
    return m2.group(0).strip()


def chart_html(cv, body):
    m = re.search(r'\\begin\{axis\}', body)
    opts, j = read_opt(body, ws(body, m.end()))
    ab, _ = env_body(body, j, 'axis')
    fill = re.search(r'fill=(\w+)', opts)
    color = color_class(fill.group(1)) if fill else 'c-ana'
    if 'coordinates' in ab:
        coords = re.search(r'coordinates\s*\{(.*?)\};', ab, re.S).group(1)
        pairs = re.findall(r'\(([^(),]+),([^()]+)\)', coords)
        horiz = re.search(r'\bxbar\b', opts) is not None
        if horiz:
            data = [(b.strip(), float(a)) for a, b in pairs]
            mx = float(axis_opt(opts, 'xmax') or max(v for _, v in data) * 1.1)
            lab = axis_opt(opts, 'xlabel') or ''
        else:
            data = [(a.strip(), float(b)) for a, b in pairs]
            mx = float(axis_opt(opts, 'ymax') or max(v for _, v in data) * 1.1)
            lab = axis_opt(opts, 'ylabel') or ''
        pct = '\\%' in (axis_opt(opts, 'nodes near coords') or '') or '\\%' in lab
        labh = cv.inl(lab)
        rows = []
        for name, v in data:
            val = f'%{v:g}' if pct else f'{v:g}'
            rows.append(f'<div class="bar-row"><span class="bar-l">{H.escape(name)}</span>'
                        f'<span class="bar-t"><span class="bar" style="--v:{v / mx:.4f}"></span>'
                        f'<span class="bar-v">{val}</span></span></div>')
        kind = 'chart-h' if horiz else 'chart-v'
        return (f'<figure class="chart {kind} {color}"><div class="bars">{"".join(rows)}</div>'
                f'<figcaption>{labh}</figcaption></figure>')
    # fonksiyon grafikleri (büyüme fonksiyonları)
    dom = axis_opt(opts, 'domain') or '1:10'
    x0, x1 = (float(v) for v in dom.split(':'))
    ymax = float(axis_opt(opts, 'ymax') or 40)
    series = []
    for pm in re.finditer(r'\\addplot\s*\[([^\]]*)\]\s*\{([^}]*)\}\s*;\s*\\addlegendentry\{(.*?)\}\s*$', ab, re.M):
        style, expr, leg = pm.groups()
        col = next((c for c in style.split(',') if c.strip() in COLORS), 'ana').strip()
        py = expr.replace('^', '**').replace('ln(', 'math.log(')
        pts = []
        steps = 90
        for k in range(steps + 1):
            x = x0 + (x1 - x0) * k / steps
            y = eval(py, {'math': math, 'x': x})
            pts.append((round(x, 3), round(y, 3)))
        nm = leg.strip('$').replace('\\log', ' log ').replace('^2', '²').replace('^n', 'ⁿ').replace('{', '').replace('}', '')
        nm = re.sub(r'\s+', ' ', nm).replace('( ', '(').replace(' )', ')')
        series.append(dict(c=col, d='dashed' in style, leg=cv.inl(leg), nm=nm, pts=pts))
    W, Hh, P = 560, 300, 36

    def sx(x):
        return P + (x - x0) / (x1 - x0) * (W - P - 10)

    def sy(y):
        return Hh - P - min(y, ymax * 1.05) / ymax * (Hh - P - 10)
    paths = []
    for k, sr in enumerate(series):
        d = 'M' + ' L'.join(f'{sx(x):.1f},{sy(y):.1f}' for x, y in sr['pts'] if y <= ymax * 1.05)
        paths.append(f'<path class="ser c-{sr["c"]}{" dash" if sr["d"] else ""}" data-i="{k}" d="{d}"/>')
    grid = ''.join(f'<line x1="{P}" x2="{W - 10}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/>'
                   f'<text x="{P - 6}" y="{sy(v) + 4:.1f}" class="tick" text-anchor="end">{v:g}</text>'
                   for v in range(0, int(ymax) + 1, 10))
    grid += ''.join(f'<text x="{sx(v):.1f}" y="{Hh - P + 16}" class="tick" text-anchor="middle">{v}</text>'
                    for v in range(int(x0), int(x1) + 1))
    legend = ''.join(f'<button type="button" class="leg c-{sr["c"]}" data-i="{k}" data-name="{H.escape(sr["nm"])}"><i></i>{sr["leg"]}</button>'
                     for k, sr in enumerate(series))
    data = H.escape(json.dumps([[p[1] for p in sr['pts']] for sr in series]))
    xl = cv.inl(axis_opt(opts, 'xlabel') or '')
    return (f'<figure class="chart chart-f" data-x0="{x0}" data-x1="{x1}" data-ymax="{ymax}" data-series="{data}">'
            f'<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="Büyüme fonksiyonları grafiği">{grid}'
            f'<line class="axis" x1="{P}" y1="{Hh - P}" x2="{W - 10}" y2="{Hh - P}"/>'
            f'<line class="axis" x1="{P}" y1="10" x2="{P}" y2="{Hh - P}"/>{"".join(paths)}'
            f'<line class="cursor" x1="0" x2="0" y1="10" y2="{Hh - P}"/></svg>'
            f'<div class="legend">{legend}</div>'
            f'<label class="nslider">n = <output>5</output><input type="range" min="{x0}" max="{x1}" step="0.1" value="5"></label>'
            f'<div class="nvals"></div><figcaption>{xl}. Eğrilere tıklayarak gizleyip gösterebilir, '
            f'kaydırıcıyla n büyürken değerlerin nasıl ayrıştığını görebilirsin.</figcaption></figure>')


# ------------------------------------------------------------------ LaTeX -> SVG
def compile_gfx():
    GFX.mkdir(parents=True, exist_ok=True)
    dims_path = GFX / 'dims.json'
    dims = json.loads(dims_path.read_text()) if dims_path.exists() else {}
    todo = [(h, raw) for h, raw in GFXREG.items() if h not in dims or not (GFX / f'g_{h}.svg').exists()]
    if todo:
        BUILD.mkdir(exist_ok=True)
        print(f'  {len(todo)} diyagram derleniyor...')
        ok = run_batch(todo)
        if not ok:
            print('  toplu derleme başarısız, tek tek deneniyor')
            for h, raw in todo:
                run_batch([(h, raw)])
        for h, raw in todo:
            svg = GFX / f'g_{h}.svg'
            if svg.exists():
                t = svg.read_text()[:600]
                w = float(re.search(r'width="([\d.]+)', t).group(1))
                hh = float(re.search(r'height="([\d.]+)', t).group(1))
                dims[h] = [w, hh]
            else:
                print('  HATA: diyagram derlenemedi:', raw[:120].replace('\n', ' '))
    # artık kullanılmayan eski SVG'leri temizle
    for f in GFX.glob('g_*.svg'):
        if f.stem[2:] not in GFXREG:
            f.unlink()
    dims = {h: v for h, v in dims.items() if h in GFXREG}
    dims_path.write_text(json.dumps(dims))
    return dims


def run_batch(todo):
    pre = [r'\documentclass[11pt]{article}', r'\usepackage{ortak}',
           r'\usepackage[active,tightpage]{preview}', r'\setlength\PreviewBorder{2pt}',
           ] + PREAMBLE_DEFS + [r'\pagestyle{empty}', r'\begin{document}']
    body = [f'\\begin{{preview}}{raw}\\end{{preview}}' for _, raw in todo]
    (BUILD / 'gfx.tex').write_text('\n'.join(pre + body + [r'\end{document}']), encoding='utf-8')
    r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', f'-output-directory={BUILD}',
                        str(BUILD / 'gfx.tex')], cwd=TEX, capture_output=True, text=True)
    pdf = BUILD / 'gfx.pdf'
    if r.returncode != 0 or not pdf.exists():
        log = (BUILD / 'gfx.log').read_text(errors='ignore')
        err = re.search(r'^!.*(?:\n.*){0,4}', log, re.M)
        print('  xelatex hatası:', err.group(0) if err else r.stdout[-400:])
        return False
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    if pages != len(todo):
        print(f'  sayfa sayısı uyuşmuyor: {pages} != {len(todo)}')
        return False
    for k, (h, _) in enumerate(todo, 1):
        subprocess.run(['pdftocairo', '-svg', '-f', str(k), '-l', str(k), str(pdf), str(GFX / f'g_{h}.svg')],
                       check=True)
    pdf.unlink()
    return True


# ------------------------------------------------------------------ KaTeX
def render_math():
    katex = AS / 'katex' / 'katex.min.js'
    js = ("const k=require(process.argv[1]);const fs=require('fs');"
          "const a=JSON.parse(fs.readFileSync(0,'utf8'));"
          "process.stdout.write(JSON.stringify(a.map(([t,d])=>{try{return k.renderToString(t,"
          "{displayMode:d,throwOnError:false,strict:'ignore',output:'html'})}catch(e){return '<code>'+t+'</code>'}})))")
    items = []
    for tex, d in MATH:
        t = re.sub(r'\\color\{(\w+)(![\d]+)?\}', lambda m: '\\color{' + COLORS.get(m.group(1), '#1F4E79') + '}', tex)
        t = re.sub(r'\\textcolor\{(\w+)\}', lambda m: '\\textcolor{' + COLORS.get(m.group(1), '#1F4E79') + '}', t)
        items.append([t, d])
    r = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(items), capture_output=True, text=True,
                       check=True)
    out = json.loads(r.stdout)
    rev = {v.lower(): k for k, v in COLORS.items() if k in ('ana', 'vurgu', 'yesil', 'turuncu', 'gri')}

    def fix(h):
        return re.sub(r'color:\s*(#[0-9a-fA-F]{6})',
                      lambda m: f'color:var(--k-{rev[m.group(1).lower()]})' if m.group(1).lower() in rev else m.group(0),
                      h)
    return [fix(h) for h in out]


# ------------------------------------------------------------------ sayfa şablonları
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;1,14..32,400'
         '&family=Plus+Jakarta+Sans:wght@600;700;800'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">')
THEME_JS = ("<script>var t='dark',h=false;try{t=localStorage.getItem('muhmat:theme')||'dark';"
            "h=localStorage.getItem('muhmat:tocHidden')==='true';}catch(e){}"
            "document.documentElement.dataset.theme=t;if(h)document.documentElement.classList.add('toc-hidden');</script>")


def plain(h, maths):
    h = re.sub(r'\x01M(\d+)\x02', lambda m: ' ' + maths[int(m.group(1))][0] + ' ', h)
    h = re.sub(r'\x01G[^\x02]*\x02', ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = H.unescape(h)
    # arama önizlemesinde LaTeX komut adları görünmesin
    h = re.sub(r'\\[A-Za-z]+\*?', ' ', h)
    h = re.sub(r'[\\{}^_]', '', h)
    return re.sub(r'\s+', ' ', h).strip()


def build_toc(heads):
    out = ['<ol class="toc-l">']
    open_l2 = open_l3 = False
    for lvl, num, th, tid in heads:
        if lvl == 2:
            if open_l3:
                out.append('</ol>')
                open_l3 = False
            if open_l2:
                out.append('</li>')
            out.append(f'<li class="t2"><a href="#{tid}"><span class="tn">{num}</span><span>{th}</span></a>')
            open_l2 = True
        elif lvl in (4, 5) and open_l3:
            out.append(f'<li class="t4"><a href="#{tid}"><span class="tn">{num}</span><span>{th}</span></a></li>')
        elif lvl == 3:
            if not open_l3:
                out.append('<ol class="toc-s">')
                open_l3 = True
            out.append(f'<li class="t3"><a href="#{tid}"><span class="tn">{num}</span><span>{th}</span></a></li>')
    if open_l3:
        out.append('</ol>')
    if open_l2:
        out.append('</li>')
    out.append('</ol>')
    return ''.join(out)


def page_html(doc, meta, body, toc, prev, nxt, stats):
    kicker = H.escape(doc['label']) if doc['group'] == 'sinav' else f'Konu {doc["no"]}'
    if doc['out'] == 'konu-tumu':
        kicker = 'Konu anlatımı'
    chips = []
    if stats['h2']:
        chips.append(f'{stats["h2"]} bölüm')
    if stats['gfx']:
        chips.append(f'{stats["gfx"]} diyagram')
    if stats['soru']:
        chips.append(f'{stats["soru"]} soru')
    if stats['cevap']:
        chips.append(f'{stats["cevap"]} çözüm kutusu')
    if stats['tanim']:
        chips.append(f'{stats["tanim"]} tanım')
    if stats['teorem']:
        chips.append(f'{stats["teorem"]} teorem/formül')
    chips_h = ''.join(f'<li>{c}</li>' for c in chips)
    quiz = ('<button class="tb-btn" id="quizBtn" type="button" title="Bütün çözümleri aç veya kapat">'
            '<span class="ic ic-eye"></span><span class="lbl">'
            + ('Çözümleri göster' if stats['cozum'] else 'Çözümleri gizle') + '</span></button>') if stats['cevap'] or stats['cozum'] else ''
    pv = (f'<a class="pg prev" href="{prev["out"]}.html"><small>Önceki</small><span>{H.escape(prev["label"])}</span></a>'
          if prev else '<span></span>')
    nx = (f'<a class="pg next" href="{nxt["out"]}.html"><small>Sonraki</small><span>{H.escape(nxt["label"])}</span></a>'
          if nxt else '<span></span>')
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(meta["title_plain"])} | Mühendislik Matematiği</title>
{THEME_JS}
{FONTS}
<link rel="stylesheet" href="assets/katex/katex.min.css">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="doc g-{doc["group"]}" data-page="{doc["out"]}" data-group="{doc["group"]}" data-unit="h{stats["unit"]}" data-title="{H.escape(doc["label"])}" style="--accent:{doc["hue"]}">
<div class="readbar"><span></span></div>
<header class="topbar">
  <button class="tb-btn menu" id="menuBtn" type="button" aria-label="İçindekileri gizle veya göster" aria-controls="toc" title="İçindekileri gizle / göster"><span class="ic ic-menu"></span></button>
  <a class="brand" href="../index.html"><span class="brand-dot"></span>Müh. Matematiği</a>
  <span class="crumb">{H.escape(doc["label"])}</span>
  <div class="tb-actions">
    <button class="tb-btn sbtn" id="searchBtn" type="button"><span class="ic ic-search"></span><span class="lbl">Ara</span><kbd>Ctrl K</kbd></button>
    {quiz}
    <button class="tb-btn" id="themeBtn" type="button" aria-label="Tema değiştir"><span class="ic ic-theme"></span></button>
  </div>
</header>
<div class="layout">
  <aside class="toc" id="toc">
    <div class="toc-head">
      <span>İçindekiler</span>
      <span class="toc-prog"><b id="pgDone">0</b>/<b id="pgAll">{stats["units"]}</b> {"başlık" if stats["unit"] == 3 else "bölüm"} çalışıldı</span>
      <span class="meter"><i id="pgBar"></i></span>
    </div>
    <nav>{toc}</nav>
  </aside>
  <main class="content" id="content">
    <header class="doc-hero">
      <p class="kicker">{kicker}</p>
      <h1>{meta["title"]}</h1>
      <p class="byline">{meta["author"]}</p>
      <ul class="chips">{chips_h}</ul>
    </header>
    <article class="prose">
{body}
    </article>
    <nav class="pager">{pv}{nx}</nav>
  </main>
</div>
<div class="lightbox" id="lightbox" hidden>
  <div class="lb-bar"><button type="button" data-z="-1" aria-label="Uzaklaştır">−</button><button type="button" data-z="0">Sığdır</button><button type="button" data-z="1" aria-label="Yakınlaştır">+</button><button type="button" data-z="x" aria-label="Kapat">✕</button></div>
  <div class="lb-stage"><div class="lb-frame"><img alt=""></div></div>
</div>
<div class="search" id="search" hidden>
  <div class="search-panel" role="dialog" aria-label="Arama">
    <input type="search" id="searchIn" placeholder="Konu, formül ya da kelime ara (ör. gradyan, eğrilik, düzlem)" autocomplete="off">
    <ol id="searchOut"></ol>
    <p class="search-hint">Yukarı/aşağı ok ile seç, Enter ile git, Esc ile kapat.</p>
  </div>
</div>
<script src="assets/search-index.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
'''


def doc_meta(cv, pre):
    def get(cmd):
        m = re.search(r'\\' + cmd + r'\{', pre)
        if not m:
            return ''
        v, _ = read_group(pre, m.end() - 1)
        return v
    title = get('title')
    parts = top_split(title, r'\\\\(?:\[[^\]]*\])?')
    t = cv.inl(parts[-1])
    author = cv.inl(get('author'))
    return dict(title=t, title_plain=re.sub(r'<[^>]+>', '', t), author=author)


# ------------------------------------------------------------------ ana akış
def main():
    global GMACROS
    pages = []
    for doc in DOCS:
        src = (TEX / f'{doc["src"]}.tex').read_text(encoding='utf-8')
        pre, rest = src.split('\\begin{document}', 1)
        body = rest.split('\\end{document}', 1)[0]
        for m in re.finditer(r'\\newcommand\{\\(\w+)\}', pre):
            if m.group(1) in ('frag',):
                continue
            k = ws(pre, m.end())
            if pre[k] == '[':
                _, k = read_opt(pre, k)
            defn, k2 = read_group(pre, ws(pre, k))
            full = pre[m.start():k2]
            if full not in PREAMBLE_DEFS:
                PREAMBLE_DEFS.append(full)
        GMACROS.update(parse_macros(pre))
        body = expand_inputs(body)
        cv = Conv()
        items = cv.conv(body)
        html_body = render_block(items)
        meta = doc_meta(cv, pre)
        cv.stats['h2'] = sum(1 for h in cv.heads if h[0] == 2)
        n3 = sum(1 for h in cv.heads if h[0] == 3)
        cv.unit = 3 if n3 > 2 * cv.stats['h2'] else 2
        cv.stats['units'] = n3 if cv.unit == 3 else cv.stats['h2']
        pages.append((doc, meta, html_body, cv))
        if cv.unknown:
            print(f'{doc["src"]}: bilinmeyen komutlar: {dict(cv.unknown)}')

    dims = compile_gfx()
    maths = MATH[:]
    rendered = render_math()

    def subst(h, prefix='assets/'):
        def g(m):
            hsh, kind = m.group(1), m.group(2)
            if hsh not in dims:
                return '<p class="warn">(diyagram derlenemedi)</p>'
            w, hh = dims[hsh]
            sc = 1.38
            alt = {'tree': 'Ağaç diyagramı', 'flow': 'Akış diyagramı'}.get(kind, 'Diyagram')
            return (f'<figure class="gfx gfx-{kind}"><button type="button" class="zoom" aria-label="Büyüt">'
                    f'<img src="{prefix}gfx/g_{hsh}.svg" width="{w * sc:.0f}" height="{hh * sc:.0f}" '
                    f'loading="lazy" alt="{alt}"></button></figure>')
        h = re.sub(r'\x01G(\w+):(\w+)\x02', g, h)
        return re.sub(r'\x01M(\d+)\x02', lambda m: rendered[int(m.group(1))], h)

    OUT.mkdir(exist_ok=True)
    index = []
    summary = []
    for n, (doc, meta, body, cv) in enumerate(pages):
        # arama dizini (bölüm bölüm)
        chunks = re.split(r'(<h[2345] id="[^"]+" class="h[^"]*">.*?</h[2345]>)', body)
        cur = None
        for ch in chunks:
            mh = re.match(r'<h[2345] id="([^"]+)" class="h[^"]*">(.*?)</h[2345]>', ch)
            if mh:
                cur = dict(p=doc['out'], d=doc['label'], id=mh.group(1), t=plain(mh.group(2), maths), x='')
                index.append(cur)
            elif cur is not None:
                cur['x'] = (cur['x'] + ' ' + plain(ch, maths))[:2500]
        prev = pages[n - 1][0] if n > 0 else None
        nxt = pages[n + 1][0] if n + 1 < len(pages) else None
        toc = build_toc(cv.heads)
        cv.stats['unit'] = cv.unit
        page = page_html(doc, meta, subst(body), subst(toc), prev, nxt, cv.stats)
        page = subst(page)
        (OUT / f'{doc["out"]}.html').write_text(page, encoding='utf-8')
        summary.append(dict(out=doc['out'], label=doc['label'], hue=doc['hue'], desc=doc['desc'], group=doc['group'],
                            no=doc.get('no', ''), h2=cv.stats['h2'], gfx=cv.stats['gfx'], soru=cv.stats['soru'],
                            cevap=cv.stats['cevap'], code=cv.stats['code'], tanim=cv.stats['tanim'], teorem=cv.stats['teorem'],
                            units=[h[3] for h in cv.heads if h[0] == cv.unit]))
        print(f'OK: html/{doc["out"]}.html  ({cv.stats["h2"]} bölüm, {cv.stats["gfx"]} diyagram)')

    (AS / 'search-index.js').write_text('window.BZ_INDEX=' + json.dumps(index, ensure_ascii=False) + ';',
                                        encoding='utf-8')
    for f in ('style.css', 'app.js'):
        shutil.copy(GEN / f, AS / f)
    home = (GEN / 'index.tpl.html').read_text(encoding='utf-8')
    home = home.replace('/*PAGES*/', json.dumps(summary, ensure_ascii=False))
    home = home.replace('<!--FONTS-->', FONTS).replace('<!--THEME-->', THEME_JS)
    (ROOT / 'index.html').write_text(home, encoding='utf-8')
    print('OK: index.html (ana sayfa)')
    # tarayıcı önbelleği eski betik/stil dosyasını kullanmasın: bağlantılara içerik özeti ekle
    ver = {f.name: hashlib.sha1(f.read_bytes()).hexdigest()[:8]
           for f in (AS / n for n in ('style.css', 'app.js', 'search-index.js')) if f.exists()}
    for f in [OUT / f'{d["out"]}.html' for d in DOCS] + [ROOT / 'index.html']:
        t = f.read_text(encoding='utf-8')
        t = re.sub(r'(assets/([\w.-]+\.(?:css|js)))(\?v=[0-9a-f]+)?"',
                   lambda m: m.group(1) + ('?v=' + ver[m.group(2)] if m.group(2) in ver else '') + '"', t)
        f.write_text(t, encoding='utf-8')
    for old, new in REDIRECTS.items():
        (OUT / f'{old}.html').write_text(
            f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Yönlendiriliyor</title>'
            f'<meta http-equiv="refresh" content="0; url={new}.html"><link rel="canonical" href="{new}.html">'
            f'<script>location.replace("{new}.html" + location.hash)</script></head>'
            f'<body><a href="{new}.html">Sorular ve çözümler sayfasına git</a></body></html>\n', encoding='utf-8')
    used = {f'g_{h}.svg' for h in GFXREG}
    for f in GFX.glob('g_*.svg'):
        if f.name not in used:
            f.unlink()


if __name__ == '__main__':
    sys.exit(main())
