"""Bağlantı, içerik bütünlüğü ve hassas matematik sonuçlarının sayısal kontrolü."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,math
BASE=Path(__file__).resolve().parents[1]
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  for k in ['href','src']:
   if k in d:self.links.append(d[k])
pages={}
for path in BASE.glob('*.html'):
 parser=Parse();parser.feed(path.read_text());pages[path]=parser
errors=[];links=0
for path,parser in pages.items():
 for raw in parser.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  target=path.parent/unquote(u.path) if u.path else path
  links+=1
  if not target.exists():errors.append(f'{path.name}: missing {raw}')
  if u.fragment and target.suffix=='.html' and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{path.name}: missing fragment {raw}')
assert not errors,errors
rows=json.loads((BASE/'content/photos.json').read_text());assert len(rows)==156
for row in rows:
 a=BASE.parent/row['file'];b=BASE/'assets/photos'/row['file'];assert hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest(),row['file']
topics=json.loads((BASE/'content/course.json').read_text());qs=[b for t in topics for s in t['sections'] for b in s['blocks'] if b['type']=='example'];assert len(qs)==89
assert len({b['id'] for b in qs})==len(qs)
# Merkezî fark ile rasyonel örneğin analitik birinci/ikinci türevlerini kontrol et.
def close(a,b,tol=2e-4):assert abs(a-b)<tol*max(1,abs(b)),(a,b)
f=lambda x,y:x*y/(x*x+y*y)
for x,y in [(1.2,.7),(-.8,1.1),(2.,-1.)]:
 h=1e-4;S=x*x+y*y
 fx=(f(x+h,y)-f(x-h,y))/(2*h);fy=(f(x,y+h)-f(x,y-h))/(2*h)
 fxx=(f(x+h,y)-2*f(x,y)+f(x-h,y))/(h*h)
 fyy=(f(x,y+h)-2*f(x,y)+f(x,y-h))/(h*h)
 fxy=(f(x+h,y+h)-f(x+h,y-h)-f(x-h,y+h)+f(x-h,y-h))/(4*h*h)
 close(fx,y*(y*y-x*x)/S**2);close(fy,x*(x*x-y*y)/S**2)
 close(fxx,2*x*y*(x*x-3*y*y)/S**3);close(fyy,2*x*y*(y*y-3*x*x)/S**3)
 close(fxy,(-x**4+6*x*x*y*y-y**4)/S**3)
# Vektörel çarpım türevi: defterdeki yüksek kuvvetlerin katsayıları.
def cross(u,v):return(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def U(t):return(t,-t,t*t/2)
def V(t):return(t**4/4,t**3/3,t*t/2)
for t in [.4,1.3,-.7]:
 h=1e-5;a=cross(U(t+h),V(t+h));b=cross(U(t-h),V(t-h))
 expected=(-3*t*t/2-5*t**4/6,3*t**5/4-3*t*t/2,4*t**3/3+5*t**4/4)
 for aa,bb,cc in zip(a,b,expected):close((aa-bb)/(2*h),cc)
# Diğer kritik sonuçlar: kapalı türev, yönlü türev, integral, hacim ve hata.
F=lambda x,y,z:2*x**4*z**3+3*x*y*y+4*x*z+3*y+5*x-23
h=1e-5;fx=(F(1+h,2,0)-F(1-h,2,0))/(2*h);fy=(F(1,2+h,0)-F(1,2-h,0))/(2*h);fz=(F(1,2,h)-F(1,2,-h))/(2*h)
close(-fx/fz,-17/4);close(-fy/fz,-15/4)
g=lambda x,y:x*x*y+3*y
close((g(1+h*3/5,2+h*4/5)-g(1-h*3/5,2-h*4/5))/(2*h),28/5)
close(3.01**2*9.9,89.69499);close((-4/2)-(-4/1),2);close(2*(.02**2),.0008)
summary=dict(html_pages=len(pages),local_links_checked=links,missing_links=0,original_photos_hash_matched=156,examples=89,direct_photo_examples=sum(bool(b['source']) for b in qs),numerical_derivative_checks='passed',notes='Sayısal kontroller genel matematiksel kanıtların yerine geçmez; hassas katsayı ve işaret hatalarını yakalamak için kullanıldı.')
(BASE/'analysis/verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
