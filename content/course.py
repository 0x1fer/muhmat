"""Özgün Türkçe ders metni. Hem LaTeX hem web bu veriden üretilir."""
TOPICS=[]
def topic(slug,title,desc,color,goals):
    t=dict(slug=slug,title=title,desc=desc,color=color,goals=goals,sections=[]);TOPICS.append(t);return t
def sec(t,title,*blocks):t['sections'].append(dict(title=title,blocks=list(blocks)))
def p(text):return dict(type='p',text=text)
def f(text):return dict(type='formula',text=text)
def note(title,text):return dict(type='note',title=title,text=text)
def li(*items):return dict(type='list',items=list(items))
def ex(title,question,solution,source=None):return dict(type='example',title=title,question=question,solution=solution,source=source)
def fig(name,caption):return dict(type='figure',name=name,caption=caption)
def table(headers,rows):return dict(type='table',headers=headers,rows=rows)

t=topic('01-vektorler','Üç boyutlu uzay ve vektörler','Koordinatlar, norm, birim vektör, skaler ve vektörel çarpım, izdüşüm ve lineer bağımsızlık.','#818CF8',[
'Nokta ile vektör arasındaki farkı açıklamak; uzunluk ve yön bulmak.',
'Bir soruda skaler çarpım mı vektörel çarpım mı gerektiğini seçmek.',
'Alan, hacim, izdüşüm ve bağımsızlık problemlerini çözmek.'])
sec(t,'Uzayı koordinatlarla okumak',
p(r'Bir noktayı belirtmek için konum, bir vektörü belirtmek için büyüklük ve yön gerekir. Sağ elli Kartezyen sistemde \(P=(x,y,z)\) noktasının koordinatları sırasıyla \(yz\), \(xz\), \(xy\) düzlemlerine göre işaretli konumunu anlatır. \(xy\) düzlemi \(z=0\), \(xz\) düzlemi \(y=0\), \(yz\) düzlemi \(x=0\) ile tanımlanır. Üç koordinatın işaretleri uzayı sekiz bölgeye ayırır.'),
p(r'\(A\) noktasından \(B\) noktasına giden vektör her koordinatta son eksi ilk alınarak bulunur. Başlangıç noktası değişse bile aynı büyüklük ve yönü koruyan oklar aynı serbest vektörü temsil eder. Buna karşılık \(\overrightarrow{OA}\), başlangıcı orijin olduğu için konum vektörüdür.'),
f(r'\overrightarrow{AB}=(x_B-x_A,y_B-y_A,z_B-z_A),\qquad d(A,B)=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2+(z_B-z_A)^2}.'),
note('Ön bilgi',r'Tek değişkenli türev ve integral kuralları sonraki bölümlerde kullanılacak. Bu ilk bölüm için Pisagor bağıntısı, determinant ve temel trigonometri yeterlidir.'))
sec(t,'Vektör işlemleri, norm ve birim vektör',
p(r'\(\mathbf u=(u_1,u_2,u_3)\) ve \(\mathbf v=(v_1,v_2,v_3)\) için toplama bileşen bileşen yapılır. \(\lambda\mathbf u\) uzunluğu \(|\lambda|\) katına çıkarır; \(\lambda<0\) ise yönü ters çevirir. Standart baz \(\mathbf i=(1,0,0),\mathbf j=(0,1,0),\mathbf k=(0,0,1)\) olduğundan \(\mathbf u=u_1\mathbf i+u_2\mathbf j+u_3\mathbf k\) yazılır.'),
f(r'\mathbf u+\mathbf v=(u_1+v_1,u_2+v_2,u_3+v_3),\quad \|\mathbf u\|=\sqrt{u_1^2+u_2^2+u_3^2},\quad \widehat{\mathbf u}=\frac{\mathbf u}{\|\mathbf u\|}\quad(\mathbf u\ne\mathbf0).'),
ex('Birim vektör',r'\(\mathbf u=(3,4)\) yönündeki birim vektörü bulunuz.',[
r'Önce norm alınır: \(\|\mathbf u\|=\sqrt{9+16}=5\).',r'Her bileşeni 5 ile bölünce \(\widehat{\mathbf u}=(3/5,4/5)\) elde edilir. Norm kontrolü \(9/25+16/25=1\) verir. Ters yöndeki birim vektör bunun negatifidir.'],'IMG-20261009-WA0026.jpg'),
note('Sıfır vektörü',r'\(\mathbf0\) için yön ve birim vektör tanımlanmaz. Birimleştirme yapmadan önce paydanın sıfır olmadığını kontrol et.'))
sec(t,'Skaler çarpım, açı ve diklik',
p(r'Skaler çarpım iki vektörün aynı doğrultuda ne kadar bileşeni bulunduğunu ölçer; sonucu sayıdır. Bileşen formülü hesaplamada, geometrik formül açı yorumunda kullanılır. Sıfır olmayan vektörler için çarpım pozitifse dar, negatifse geniş, sıfırsa dik açı vardır.'),
f(r'\mathbf u\cdot\mathbf v=u_1v_1+u_2v_2+u_3v_3=\|\mathbf u\|\|\mathbf v\|\cos\theta,\qquad \cos\theta=\frac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\|\mathbf v\|}.'),
ex('Dersteki açı sorusu',r'\(\mathbf u=(2,-1,3)\) ve \(\mathbf v=(1,4,2)\) dik midir? \(\cos\theta\) nedir?',[
r'\(\mathbf u\cdot\mathbf v=2-4+6=4\). Çarpım sıfır olmadığından dik değildirler.',r'\(\|\mathbf u\|=\sqrt{14}\), \(\|\mathbf v\|=\sqrt{21}\). Dolayısıyla \(\cos\theta=4/\sqrt{294}\). Pozitif sonuç açının dar olduğunu doğrular.'],'IMG-20261009-WA0032.jpg'),
p(r'Yön kosinüsleri, vektörün pozitif koordinat eksenleriyle yaptığı açıların kosinüsleridir. \(\cos\alpha=u_1/\|\mathbf u\|\), \(\cos\beta=u_2/\|\mathbf u\|\), \(\cos\gamma=u_3/\|\mathbf u\|\) ve \(\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1\). Bu bağıntı birim vektör kontrolünün başka bir biçimidir.'),
note('Vektör açısı ve doğru açısı',r'İki vektörün açısı \([0,\pi]\) aralığındadır. İki yönsüz doğru arasındaki küçük açı için paydaki skaler çarpımın mutlak değeri kullanılır.'))
sec(t,'İzdüşüm: bir vektörü iki parçaya ayırmak',
p(r'Bir kuvveti eğim boyunca ve eğime dik bileşenlerine ayırırken izdüşüm kullanılır. \(\mathbf u\) vektörünün \(\mathbf v\) doğrultusundaki işaretli skaler bileşeni bir sayıdır; vektörel izdüşümü ise bu sayı ile \(\widehat{\mathbf v}\) çarpılarak elde edilir.'),
f(r'\operatorname{comp}_{\mathbf v}\mathbf u=\frac{\mathbf u\cdot\mathbf v}{\|\mathbf v\|},\qquad \operatorname{proj}_{\mathbf v}\mathbf u=\frac{\mathbf u\cdot\mathbf v}{\|\mathbf v\|^2}\mathbf v.'),
p(r'\(\mathbf u_{\perp}=\mathbf u-\operatorname{proj}_{\mathbf v}\mathbf u\) kalanı \(\mathbf v\) ile diktir. Kontrol için kalanla \(\mathbf v\) skaler çarpılır. İşaretli bileşen negatif olabilir; izdüşümün uzunluğu istendiğinde mutlak değer alınır.'),
ex('İzdüşüm hesabı',r'\(\mathbf u=(2,1,2)\) vektörünü \(\mathbf v=(1,0,1)\) doğrultusuna izdüşürünüz.',[
r'\(\mathbf u\cdot\mathbf v=4\), \(\|\mathbf v\|^2=2\). Bu yüzden izdüşüm \(2(1,0,1)=(2,0,2)\).',r'Dik kalan \((0,1,0)\) olur ve \((0,1,0)\cdot(1,0,1)=0\). Skaler bileşen \(4/\sqrt2=2\sqrt2\).']),
fig('projection','İzdüşüm, vektörü bir doğrultuya paralel ve o doğrultuya dik iki bileşene ayırır.'))
sec(t,'Vektörel çarpım ve alan',
p(r'Vektörel çarpım \(\mathbb R^3\) içinde her iki girdiye de dik bir vektör üretir. Yönü sağ el kuralıyla belirlenir. Sıra değişirse işaret değişir; bu yüzden determinant açılımındaki orta bileşenin eksi işaretine dikkat edilir.'),
f(r'\mathbf u\times\mathbf v=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\u_1&u_2&u_3\\v_1&v_2&v_3\end{vmatrix}=(u_2v_3-u_3v_2,\ u_3v_1-u_1v_3,\ u_1v_2-u_2v_1).'),
f(r'\|\mathbf u\times\mathbf v\|=\|\mathbf u\|\|\mathbf v\|\sin\theta,\qquad A_{\rm paralelkenar}=\|\mathbf u\times\mathbf v\|,\quad A_{\rm üçgen}=\frac12\|\mathbf u\times\mathbf v\|.'),
ex('Tahtadaki vektörel çarpım',r'\(\mathbf u=(1,2,3)\), \(\mathbf v=(2,0,1)\) için \(\mathbf u\times\mathbf v\) bulunuz.',[
r'Bileşenler \((2\cdot1-3\cdot0,\,3\cdot2-1\cdot1,\,1\cdot0-2\cdot2)\) şeklindedir. Sonuç \((2,5,-4)\).',r'Diklik kontrolleri: \((2,5,-4)\cdot(1,2,3)=2+10-12=0\) ve \((2,5,-4)\cdot(2,0,1)=4-4=0\). Alan \(\sqrt{45}=3\sqrt5\), üçgen alanı \(3\sqrt5/2\).'],'IMG-20261023-WA0029.jpg'),
note('Paralellik testi',r'Sıfır olmayan iki vektör için \(\mathbf u\times\mathbf v=\mathbf0\) paralellik demektir. Bileşen oranlarını kullanmak mümkün olsa da sıfır bileşenler varsa çapraz çarpım daha güvenlidir.'))
sec(t,'Karma çarpım, hacim ve aynı düzlemde olma',
p(r'Üç vektörün skaler karma çarpımı bir taban alanı ile işaretli yüksekliğin çarpımıdır. Sonucun mutlak değeri paralelyüzlünün hacmidir. Üç vektör aynı düzlemsel alt uzaydaysa yükseklik sıfırdır; determinant da sıfır olur.'),
f(r'[\mathbf u,\mathbf v,\mathbf w]=\mathbf u\cdot(\mathbf v\times\mathbf w),\qquad V=|[\mathbf u,\mathbf v,\mathbf w]|,\qquad V_{\rm dörtyüzlü}=\frac{V}{6}.'),
ex('Hacim ve bağımsızlık',r'\(\mathbf u=(1,0,0),\mathbf v=(0,2,0),\mathbf w=(1,1,3)\) için hacim ve bağımsızlık nedir?',[
r'\(\mathbf v\times\mathbf w=(6,0,-2)\); \(\mathbf u\cdot(\mathbf v\times\mathbf w)=6\). Paralelyüzlü hacmi 6, dörtyüzlü hacmi 1 birim küptür.',r'Determinant sıfır olmadığından bu üç vektör lineer bağımsızdır ve \(\mathbb R^3\) için baz oluşturur.']),
p(r'Lineer bağımsızlık, \(\alpha\mathbf u+\beta\mathbf v+\gamma\mathbf w=\mathbf0\) eşitliğinin yalnızca sıfır katsayılarla sağlanmasıdır. İki vektörde bağımsızlık paralel olmamaya, üç vektörde sıfır olmayan determinanta indirgenir. \(\mathbb R^2\) içinde ikiden fazla vektör bağımsız olamaz.'))
sec(t,'Dersteki lineer bağımsızlık örnekleri',
ex('Düzlemde bağımlı vektörler',r'\(\mathbf u=(1,2)\), \(\mathbf v=(-3,-6)\) bağımsız mıdır?',[
r'\(\mathbf v=-3\mathbf u\). Bu nedenle \(3\mathbf u+\mathbf v=\mathbf0\), sıfırdan farklı katsayılarla sağlanır.',r'Doğrultuları aynı olduğu için birlikte düzlemi germezler; yalnızca bir doğruyu gererler.'],'IMG-20261009-WA0033.jpg'),
ex('Düzlemde baz',r'\(\mathbf u=(2,-3)\), \(\mathbf v=(-5,4)\) düzlem için baz mıdır?',[
r'Determinant \(2\cdot4-(-3)(-5)=8-15=-7\ne0\). Dolayısıyla bağımsızdırlar ve bazdırlar.',r'Her \((x,y)\), \(\alpha\mathbf u+\beta\mathbf v\) olarak tek biçimde yazılır. Denklem sistemi çözülürse \(\alpha=-(4x+5y)/7\), \(\beta=-(3x+2y)/7\). Yerine koyma her iki koordinatı doğrular.'],'IMG-20261009-WA0034.jpg'))
sec(t,'Yöntem seçimi ve kendi kendini kontrol',
table(['İstenen','Kullanılacak işlem','Kontrol'],[
['Açı / diklik',r'\(\mathbf u\cdot\mathbf v\)','Sonuç bir sayıdır.'],
['Dik vektör / alan',r'\(\mathbf u\times\mathbf v\)','Her iki vektörle skaler çarpım sıfır.'],
['Hacim / üçlü bağımsızlık','Karma çarpım','Hacim negatif olamaz.'],
['Yön / birim vektör','Norma bölme','Norm 1 olmalı.']]),
ex('Pekiştirme',r'\(\mathbf a=(1,1,0),\mathbf b=(1,-1,2)\) için diklik, birim vektör ve paralelkenar alanını bulunuz.',[
r'\(\mathbf a\cdot\mathbf b=0\), dolayısıyla diktirler. \(\widehat{\mathbf a}=(1,1,0)/\sqrt2\).',r'\(\mathbf a\times\mathbf b=(2,-2,-2)\); alan \(2\sqrt3\). Ayrıca dik vektörlerde alan \(\|\mathbf a\|\|\mathbf b\|=\sqrt2\sqrt6=2\sqrt3\), aynı sonucu verir.']))

t=topic('02-analitik-geometri','Doğrular, düzlemler ve kuadratik yüzeyler','Parametrik denklemler, açılar, uzaklıklar; küre, silindir, koni ve temel kuadriklerin kesitleri.','#22D3EE',[
'Bir doğruyu nokta ve yönle, bir düzlemi nokta ve normalle kurmak.',
'Kesişim, açı ve uzaklıkta uygun vektörü belirlemek.',
'Kuadratik yüzeyleri işaretleri ve düzlem kesitleriyle tanımak.'])
sec(t,'Uzayda doğru: nokta ve yön',
p(r'Bir doğrunun tek bir başlangıç noktası \(P_0\) ve sıfır olmayan bir doğrultu vektörü \(\mathbf u\) bilinirse tüm noktaları bir parametreyle üretilir. İki nokta verilmişse yön olarak aralarındaki fark alınır. Aynı doğru için başlangıç noktası veya yönün sıfır olmayan katı değişebilir.'),
f(r'\mathbf r(t)=\mathbf r_0+t\mathbf u,\quad x=x_0+at,\ y=y_0+bt,\ z=z_0+ct,\qquad t\in\mathbb R.'),
p(r'\(a,b,c\) sıfır değilse \((x-x_0)/a=(y-y_0)/b=(z-z_0)/c\) simetrik biçimi elde edilir. Bir bileşen sıfırsa ona ait koordinat sabittir. Örneğin \(b=0\) ise \(y=y_0\) ayrıca yazılır; sıfıra bölme yapılmaz.'),
ex('İki noktadan geçen doğru',r'\(A=(0,1,2)\), \(B=(3,1,-1)\) doğrusunu bulunuz.',[
r'\(\overrightarrow{AB}=(3,0,-3)\), bunun yerine \((1,0,-1)\) kullanılabilir.',r'\(x=t,\ y=1,\ z=2-t\). Kartezyen biçim \(x=2-z,\ y=1\). Parametre 0 iken A, 3 iken B elde edilir.'],'IMG-20261009-WA0032.jpg'),
ex('Nokta ve paralel vektör',r'\(A=(1,2,3)\) noktasından geçen ve \((2,3,0)\) yönüne paralel doğruyu yazınız.',[
r'\(x=1+2t,\ y=2+3t,\ z=3\).',r'Simetrik gösterim \((x-1)/2=(y-2)/3\), ayrıca \(z=3\). İki denklem uzayda tek doğruyu belirler.'],'IMG-20261009-WA0030.jpg'))
sec(t,'Doğruların konumları ve açıları',
p(r'İki doğru karşılaştırılırken ilk adım yön vektörlerini karşılaştırmaktır. Paralel yönler için bir doğrunun noktası ötekinin üzerinde de bulunuyorsa doğrular çakışıktır. Paralel olmayan yönlerde kesişim için iki parametreli üç denklem çözülür. Çözüm yoksa doğrular aykırıdır.'),
f(r'\cos\varphi=\frac{|\mathbf u\cdot\mathbf v|}{\|\mathbf u\|\|\mathbf v\|},\qquad 0\le\varphi\le\frac\pi2.'),
note('Uzayda diklik nüansı',r'\(\mathbf u\cdot\mathbf v=0\) yönlerin dik olduğunu söyler. Doğruların dik kesiştiğini söylemek için ayrıca kesiştiklerini kontrol et; uzayda aykırı doğruların da yönleri dik olabilir.'),
ex('Tahtadaki sıfır paydalı gösterim',r'Tahtada \(x/1=y/1=z/0\) ve \((x-1)/1=y/(-1)=z/0\) ile belirtilen doğruların açısı nedir?',[
r'Bu gösterimde \(z/0\) gerçek bir bölüm değildir; \(z=0\) kısıtının kısa yazımı olarak yorumlanır. Parametrik biçimler \((t,t,0)\) ve \((1+s,-s,0)\) olur.',r'Yönler \((1,1,0)\), \((1,-1,0)\), çarpımları 0. \(t=1+s=-s\) den \(t=1/2,s=-1/2\); kesişim \((1/2,1/2,0)\). Dolayısıyla açı \(90^\circ\).'],'IMG-20261001-WA0014.jpg'))
sec(t,'Düzlem denklemi ve normal vektör',
p(r'Bir düzlemin içinde pek çok doğrultu vardır; bunların tümüne dik olan bir normal vektör düzlemin yönelimini belirler. \(P_0\) düzlem üzerinde ve \(\mathbf n=(A,B,C)\ne\mathbf0\) normal ise her \(P\) noktası için \(\overrightarrow{P_0P}\cdot\mathbf n=0\) yazılır.'),
f(r'A(x-x_0)+B(y-y_0)+C(z-z_0)=0\quad\Longleftrightarrow\quad Ax+By+Cz+D=0.'),
p(r'Üç nokta verildiğinde aynı başlangıçtan çıkan iki fark vektörünün vektörel çarpımı normal olur. Çarpım sıfırsa noktalar doğrudaştır ve tek bir düzlem belirlemez. Bulunan denklemi her üç noktada denemek iyi bir hata kontrolüdür.'),
ex('Koordinat eksenlerini kesen düzlem',r'\(A=(1,0,0),B=(0,1,0),C=(0,0,1)\) noktalarından geçen düzlemi bulunuz.',[
r'\(\overrightarrow{AB}=(-1,1,0)\), \(\overrightarrow{AC}=(-1,0,1)\). Çarpımları \((1,1,1)\).',r'\((x-1)+y+z=0\), yani \(x+y+z=1\). Üç nokta da denklemi sağlar.'],'IMG-20261001-WA0014.jpg'),
ex('Nokta ve normal ile düzlem',r'\(A=(2,3,4)\) noktasından geçen, normali \((1,3,4)\) olan düzlemi bulunuz.',[
r'\((x-2)+3(y-3)+4(z-4)=0\).',r'Düzenlenince \(x+3y+4z-27=0\). Normalin herhangi bir sıfır olmayan katı aynı düzlemi verir.'],'IMG-20261023-WA0030.jpg'))
sec(t,'Doğru-düzlem ve iki düzlemin kesişimi',
p(r'Doğruyu düzlemde yerine koyunca parametre için tek bir lineer denklem çıkar. \(\mathbf n\cdot\mathbf u\ne0\) ise tek kesişim vardır. \(\mathbf n\cdot\mathbf u=0\) ise doğru düzleme paraleldir; başlangıç noktası denklemi sağlıyorsa doğru düzlemin içindedir.'),
ex('Dersteki doğru-düzlem kesişimi',r'\((x-2)/1=y/2=(z+1)/(-1)\) doğrusu ile \(x-y+2z=3\) düzleminin kesişimi nedir?',[
r'\(x=2+t,\ y=2t,\ z=-1-t\) yazılır.',r'Yerine koyunca \((2+t)-2t+2(-1-t)=3\), yani \(-3t=3\). \(t=-1\) ile nokta \((1,-2,0)\). Kontrol: \(1-(-2)+0=3\).'],'IMG-20261001-WA0014.jpg'),
p(r'Paralel olmayan iki düzlemin kesişim doğrusunun yönü \(\mathbf n_1\times\mathbf n_2\) olur. Bir koordinatı uygun seçip kalan iki denklemi çözerek doğru üzerinde bir nokta bulunur. İki normal paralelse kesişim bir doğru olamaz; düzlemler çakışık veya ayrık paraleldir.'),
ex('İki düzlemin arakesiti',r'\(x+y+z=2\) ve \(x-y+z=0\) düzlemlerinin kesişimini yazınız.',[
r'Denklemleri çıkarınca \(2y=2\), yani \(y=1\). Sonra \(x+z=1\).',r'\(x=t\) seçilirse \(\mathbf r(t)=(t,1,1-t)\). Yön \((1,0,-1)\), normallerin vektörel çarpımına paraleldir.']))
sec(t,'Açı sorularında hangi vektör kullanılır?',
table(['Geometrik çift','İlişkilendirilecek vektör','Formül'],[
['Doğru - doğru','İki yön',r'\(\cos\varphi=|\mathbf u\cdot\mathbf v|/(\|\mathbf u\|\|\mathbf v\|)\)'],
['Düzlem - düzlem','İki normal',r'\(\cos\varphi=|\mathbf n_1\cdot\mathbf n_2|/(\|\mathbf n_1\|\|\mathbf n_2\|)\)'],
['Doğru - düzlem','Yön ve normal',r'\(\sin\varphi=|\mathbf u\cdot\mathbf n|/(\|\mathbf u\|\|\mathbf n\|)\)']]),
p(r'Doğru ile düzlem açısında sinüs kullanılmasının nedeni, yönle normal arasındaki dar açıya tümleyen olmasıdır. Doğru düzleme paralelse \(\mathbf u\cdot\mathbf n=0\) ve açı 0; düzleme dikse \(\mathbf u\parallel\mathbf n\) ve açı \(90^\circ\) çıkar. İki düzlemin dikliği normal vektörlerin dikliğidir.'))
sec(t,'Noktanın doğruya ve düzleme uzaklığı',
p(r'Uzaklık her zaman en kısa, dolayısıyla dik bağlantının uzunluğudur. Nokta-doğru uzaklığında \(\overrightarrow{AP}\) ile yön vektörünün oluşturduğu paralelkenarın alanı tabana bölünür. Nokta-düzlem uzaklığında ise \(\overrightarrow{P_0P}\) normal doğrultusuna izdüşürülür.'),
f(r'd(P,\ell)=\frac{\|\overrightarrow{AP}\times\mathbf u\|}{\|\mathbf u\|},\qquad d(P,\Pi)=\frac{|Ax_P+By_P+Cz_P+D|}{\sqrt{A^2+B^2+C^2}}.'),
ex('Tahtadaki nokta-doğru uzaklığı',r'\(P=(2,3,-1)\) noktasının \((x-1)/1=(y-2)/1=(z-13)/4\) doğrusuna uzaklığını bulunuz.',[
r'Doğru üzerinde \(A=(1,2,13)\), yön \(\mathbf u=(1,1,4)\). \(\overrightarrow{AP}=(1,1,-14)\).',r'\(\overrightarrow{AP}\times\mathbf u=(18,-18,0)\); normu \(18\sqrt2\). Yönün normu \(\sqrt{18}=3\sqrt2\). Uzaklık 6.'],'IMG-20261023-WA0057.jpg'),
ex('Çalışma sorusu: nokta-düzlem uzaklığı',r'\(P=(1,0,2)\) noktasının \(x+2y-2z+4=0\) düzlemine uzaklığı nedir?',[
r'Pay \(|1+0-4+4|=1\), payda \(\sqrt{1+4+4}=3\). Uzaklık \(1/3\).',r'Dik izdüşüm noktası \(H=P-\frac{1}{9}(1,2,-2)=(8/9,-2/9,20/9)\). Denkleme koyunca sıfır çıkar ve \(\|P-H\|=1/3\).'],'IMG-20261001-WA0014.jpg'),
p(r'Paralel düzlemler aynı normal katsayılarıyla yazılmışsa \(d=|D_2-D_1|/\|\mathbf n\|\). Katsayılar yalnızca orantılıysa önce aynı normale dönüştür. Aykırı doğrular için \(d=|(\mathbf r_2-\mathbf r_1)\cdot(\mathbf u\times\mathbf v)|/\|\mathbf u\times\mathbf v\|\); bu son bağıntı paralel doğrularda kullanılmaz.'))
sec(t,'Küre ve kareye tamamlama',
p(r'Küre, bir merkezden eşit uzaklıktaki noktaların kümesidir. Genel denklemde üç kare teriminin katsayısı aynı ve çapraz terimler yoksa kareye tamamlama ile merkez ve yarıçap okunabilir. Sabit terimden yarıçapın karesini yanlış işaretle çıkarmamak için her koordinatı ayrı düzenle.'),
f(r'(x-a)^2+(y-b)^2+(z-c)^2=R^2.'),
ex('Dersteki küre sorusu',r'\(x^2+y^2+z^2+4x-6y+2z-11=0\) küresinin merkezi ve yarıçapı nedir?',[
r'\((x+2)^2-4+(y-3)^2-9+(z+1)^2-1-11=0\).',r'\((x+2)^2+(y-3)^2+(z+1)^2=25\). Merkez \((-2,3,-1)\), yarıçap 5.'],'IMG-20261009-WA0032.jpg'))
sec(t,'Silindirler ve kuadratik yüzeyleri tanıma',
p(r'Bir denklemde bir koordinat hiç görünmüyorsa düzlemdeki eğri o koordinat boyunca taşınır. Örneğin \(x^2+y^2=4\), \(z\) eksenine paralel dairesel silindirdir; \(z=y^2\), \(x\) doğrultusunda uzayan parabolik silindirdir. Silindirin mutlaka dairesel olması gerekmez.'),
table(['Yüzey','Standart örnek','Ayırt edici özellik'],[
['Elipsoid',r'\(x^2/a^2+y^2/b^2+z^2/c^2=1\)','Üç kare de pozitif; kapalı.'],
['Tek kanatlı hiperboloid',r'\(x^2/a^2+y^2/b^2-z^2/c^2=1\)','Bir eksi; eksi işaretli eksen boyunca tek parça.'],
['Çift kanatlı hiperboloid',r'\(-x^2/a^2-y^2/b^2+z^2/c^2=1\)','İki eksi; artı işaretli eksende iki parça.'],
['Eliptik koni',r'\(z^2/c^2=x^2/a^2+y^2/b^2\)','Sıfır seviyesi; iki kanat tepe noktasında birleşir.'],
['Eliptik paraboloid',r'\(z=x^2/a^2+y^2/b^2\)','Yatay kesit elips; dikey kesit parabol.'],
['Hiperbolik paraboloid',r'\(z=x^2/a^2-y^2/b^2\)','Eyer; iki ana doğrultuda ters bükülme.']]),
fig('quadrics','Eliptik paraboloid ve hiperbolik paraboloid: kesitlerin işareti yüzeyin biçimini belirler.'),
note('Eksenleri ezberleme',r'Önce denklemi standart biçime getir. Eksi işaretli ya da tek başına kalan değişken değişirse yüzeyin ekseni de değişir; yüzey adını yalnızca \(z\) eksenine bakarak seçme.'))
sec(t,'Kesitlerle çizim: adım adım',
li(r'Ötelemeler varsa \(X=x-a,Y=y-b,Z=z-c\) ile merkezi veya tepeyi belirle.',r'\(x=0,y=0,z=0\) kesitlerini al; elips, hiperbol veya parabol olup olmadığını incele.',r'\(z=k\) gibi paralel kesitlerde boyutun nasıl değiştiğini bul.',r'Simetriyi, eksen kesişimlerini ve varsa boş kesitleri işaretle.'),
ex('İki yüzeyin kesitlerini karşılaştır',r'\(x^2+y^2-z^2=1\) ve \(z^2-x^2-y^2=1\) neden farklıdır?',[
r'İlkinde \(z=k\) için \(x^2+y^2=1+k^2\). Her k için çember vardır; en dar kesit \(z=0\) düzlemindedir. Tek kanatlı hiperboloid.',r'İkincide \(x^2+y^2=k^2-1\). \(|k|<1\) için kesit yok; \(k=\pm1\) için bir nokta, dışarıda çember vardır. Çift kanatlı hiperboloid.']),
ex('Pekiştirme: yüzeyi tanı',r'\(z=4-x^2-y^2\) yüzeyinin tepesini, açılma yönünü ve \(z=0\) kesitini bulunuz.',[
r'Tepe \((0,0,4)\), karelerin katsayıları negatif olduğundan aşağı açılan eliptik paraboloid.',r'\(z=0\) kesiti \(x^2+y^2=4\), yarıçapı 2 olan çember. \(z>4\) için kesit yoktur.']))

t=topic('03-uzay-egrileri','Vektör fonksiyonları, eğriler ve hareket','Vektörel limit, türev ve integral; yay uzunluğu, Frenet çatısı, eğrilik, hız ve ivme.','#34D399',[
'Vektör fonksiyonunu bileşenlerinden incelemek; eğriyi ve yönünü belirlemek.',
'Teğet, normal, binormal ve eğriliği hesaplamak.',
'Hız vektörünü süratten ayırmak; ivmeyi teğetsel ve normal bileşenlerine ayırmak.'])
sec(t,'Vektör değerli fonksiyon ve tanım kümesi',
p(r'Bir gerçek parametreyi bir vektöre gönderen fonksiyon \(\mathbf r:I\to\mathbb R^3\) biçimindedir. \(\mathbf r(t)=(x(t),y(t),z(t))\) konum vektörünün ucu bir uzay eğrisi çizer. Parametre zaman olabilir; ancak her parametrizasyon fiziksel zaman değildir. Tanım kümesi, üç bileşenin tanım kümelerinin kesişimidir.'),
ex('Defterdeki tanım kümesi örneği',r'\(\mathbf F(t)=(t+1,\ln(1-t),\sqrt{4-t^2})\) için tanım kümesini bulunuz.',[
r'İlk bileşen tüm gerçek sayılarda tanımlıdır. Logaritma için \(1-t>0\), yani \(t<1\). Karekök için \(-2\le t\le2\).',r'Koşulları birlikte sağlamak gerekir: \(I=[-2,1)\). \(-2\) kabul edilir, çünkü kök sıfır olabilir; 1 kabul edilmez, çünkü logaritma argümanı sıfır olamaz.'],'IMG-20261009-WA0016.jpg'),
p(r'Vektör fonksiyonlarında toplama, skalerle çarpma, skaler ve vektörel çarpım her t anında uygulanır. Skaler çarpımın çıktısı gerçek sayılı bir fonksiyon; vektörel çarpımın çıktısı yeniden vektör fonksiyonudur.'),
ex('Vektör fonksiyonlarıyla işlemler',r'\(\mathbf F=(t,t^2,t^3)\), \(\mathbf G=(1-t,1+t^2,t)\). Toplamı, skaler ve vektörel çarpımı bulunuz.',[
r'\(\mathbf F+\mathbf G=(1,1+2t^2,t^3+t)\).',r'\(\mathbf F\cdot\mathbf G=t(1-t)+t^2(1+t^2)+t^4=t+2t^4\).',r'\(\mathbf F\times\mathbf G=(-t^5,t^3-t^4-t^2,t+2t^3-t^2)\). Her bileşen determinant açılımından gelir.'],'IMG-20261009-WA0017.jpg'))
sec(t,'Limit ve süreklilik bileşenlere ayrılır',
f(r'\lim_{t\to t_0}\mathbf r(t)=(L_1,L_2,L_3)\quad\Longleftrightarrow\quad\lim x(t)=L_1,\ \lim y(t)=L_2,\ \lim z(t)=L_3.'),
p(r'Bu eşdeğerlik sonlu boyutta normla yakınsamanın koordinat yakınsamasıyla aynı olmasından gelir. Süreklilik için fonksiyonun noktada tanımlı olması, limitin var olması ve limitin o noktadaki değere eşit olması gerekir. Tek bileşendeki bir sıçrama bütün vektör fonksiyonunu süreksiz yapar.'),
ex('Defterdeki limit işlemleri',r'\(\mathbf F(t)=(\sin t,\cos t,1+t)\), \(\mathbf G(t)=(\cos2t,\sin3t,e^t+1)\) için t sıfıra giderken skaler ve vektörel çarpım limitlerini bulunuz.',[
r'\(\mathbf F\to(0,1,1)\), \(\mathbf G\to(1,0,2)\).',r'Skaler çarpım limiti \((0,1,1)\cdot(1,0,2)=2\). Vektörel çarpım limiti \((0,1,1)\times(1,0,2)=(2,1,-1)\).'],'IMG-20261009-WA0019.jpg'),
ex('Tam kısım içeren süreklilik',r'\(\mathbf F(t)=(|t|+1,t\lfloor t\rfloor,2+t^2)\) fonksiyonu 0 ve 1 noktalarında sürekli midir?',[
r'İlk ve üçüncü bileşen her yerde süreklidir. İkinci bileşen 0 yakınında solda \(-t\), sağda 0 olur; iki yandan limit 0, değer de 0. Dolayısıyla 0 noktasında süreklidir.',r'1 yakınında solda ikinci bileşen 0, sağda t olur. Limitler 0 ve 1 olduğundan 1 noktasında süreksizdir.'],'IMG-20261009-WA0019.jpg'))
sec(t,'Eğriyi, izini ve yönünü ayırt etmek',
p(r'Parametrik denklemlerden t yok edilerek eğrinin hangi yüzeylerin üzerinde bulunduğu anlaşılır. Ancak parametreyi yok etmek yönü ve kaç kez dolaşıldığını kaybettirir. Aynı geometrik iz farklı parametrizasyonlarla farklı hızlarda ve ters yönlerde taranabilir.'),
ex('Çember ve helis',r'\(\mathbf r(t)=(a\cos t,a\sin t,0)\) ile \(\mathbf h(t)=(\cos t,\sin t,3t)\) eğrilerini yorumlayınız.',[
r'İlkinde \(x^2+y^2=a^2\), \(z=0\). \(a>0\) ve \(0\le t\le2\pi\) için pozitif z yönünden bakıldığında çember saat yönünün tersine bir tur taranır.',r'İkincide \(x^2+y^2=1\); yükseklik t ile artar. Bir turda t, \(2\pi\) artar ve yükseklik \(6\pi\) değişir. Bu eğri bir helistir.'],'IMG-20261009-WA0022.jpg'),
p(r'Bir parametrizasyon sürekli, parçalı türevlenebilir olabilir. Düzgünlük için ilgili aralıkta türevin sürekli ve \(\mathbf r\,\prime(t)\ne\mathbf0\) olması istenir. Türevin sıfır olduğu bir parametrizasyon noktasında standart birim teğet formülü doğrudan uygulanmaz; eğrinin geometrisi ayrıca incelenir.'),
ex('Parçalı düzgün eğri',r'\(\mathbf r(t)=(a\cos t,a|\sin t|,0)\), \(-2\pi\le t\le2\pi\), \(a>0\) için düzgünlük nasıldır?',[
r'\(\sin t\) işaret değiştirdiğinde mutlak değerin türevi değişir. \(t=k\pi\) noktalarında tek taraflı teğet vektörler uyuşmaz; verilen parametrizasyon düzgün değildir.',r'Aradaki açık aralıklarda türev vardır ve normu a olur. Dolayısıyla sonlu sayıda parçaya ayrılarak parçalı düzgün kabul edilir. İz üst yarım çemberdir; birden fazla kez taranır.'],'IMG-20261015-WA0038.jpg'))
sec(t,'Türev, teğet doğrusu ve çarpım kuralları',
p(r'\(\Delta\mathbf r/\Delta t\), iki konum arasındaki kirişin zamana oranıdır. Limitte anlık değişim vektörüne dönüşür. \(\mathbf r\,\prime(t_0)\ne\mathbf0\) ise bu vektör eğrinin o noktadaki teğet yönüdür. Teğet doğrusu yeni bir parametreyle \(\mathbf q(s)=\mathbf r(t_0)+s\mathbf r\,\prime(t_0)\) olarak yazılır.'),
f(r'\mathbf r\,\prime(t)=\lim_{h\to0}\frac{\mathbf r(t+h)-\mathbf r(t)}h=(x\prime(t),y\prime(t),z\prime(t)).'),
f(r'\begin{aligned}(\phi\mathbf F)\prime&=\phi\prime\mathbf F+\phi\mathbf F\prime,\\(\mathbf F\cdot\mathbf G)\prime&=\mathbf F\prime\cdot\mathbf G+\mathbf F\cdot\mathbf G\prime,\\(\mathbf F\times\mathbf G)\prime&=\mathbf F\prime\times\mathbf G+\mathbf F\times\mathbf G\prime.\end{aligned}'),
ex('Dersteki temel türevler',r'\(\mathbf F(t)=(t,t^2,t^3)\) ve \(\mathbf G(t)=(t\ln t-t,e^t,e^{-t})\) türevlerini bulunuz.',[
r'Bileşenler ayrı türevlenir: \(\mathbf F\prime=(1,2t,3t^2)\).',r'İkinci fonksiyonun ilk bileşeninde çarpım kuralı \((t\ln t-t)\prime=\ln t+1-1=\ln t\) verir. \(\mathbf G\prime=(\ln t,e^t,-e^{-t})\), \(t>0\).'],'IMG-20261023-WA0058.jpg'),
ex('Zincir kuralı içeren vektör türevi',r'\(\mathbf F(t)=(\arcsin(4t),-3\arctan(2t-1),7\ln(3t^2))\) türevini bulunuz.',[
r'İlk bileşenin türevi \(4/\sqrt{1-16t^2}\); ikincinin türevi \(-6/[1+(2t-1)^2]\).',r'Üçüncü bileşen \(7(6t)/(3t^2)=14/t\). Türev formüllerinin ortak geçerlilik aralığı \(-1/4<t<1/4\), \(t\ne0\). Fonksiyon uçlarda tanımlı olsa da bu türevler uçlarda sonlu değildir.'],'IMG-20261023-WA0058.jpg'),
ex('Tahtadaki özdeşliğin kanıtı',r'\([\mathbf F(t)\times\mathbf F\prime(t)]\prime=\mathbf F(t)\times\mathbf F\prime\prime(t)\) olduğunu gösteriniz.',[
r'Çarpım kuralı sol tarafı \(\mathbf F\prime\times\mathbf F\prime+\mathbf F\times\mathbf F\prime\prime\) yapar.',r'Bir vektörün kendisiyle vektörel çarpımı sıfırdır. İlk terim silinince istenen özdeşlik kalır.'],'IMG-20261023-WA0058.jpg'))
sec(t,'Vektör fonksiyonlarının integrali',
p(r'İntegral de bileşen bileşen hesaplanır. Belirsiz integralde sabit bir vektör \(\mathbf C=(C_1,C_2,C_3)\) eklenir. Tek bir skaler sabiti bütün bileşenlere zorunlu olarak aynı eklemek genel çözümü daraltır. Başlangıç koşulu varsa üç sabit ayrı ayrı belirlenir.'),
f(r'\int_a^b\mathbf r(t)\,dt=\left(\int_a^b x(t)\,dt,\int_a^b y(t)\,dt,\int_a^b z(t)\,dt\right).'),
ex('Başlangıç koşullu integral',r'\(\mathbf r\prime(t)=(2t,e^{3t},4\sin2t)\), \(\mathbf r(0)=(2,1,-2)\). Konumu bulunuz.',[
r'İntegral \(\mathbf r(t)=(t^2+C_1,e^{3t}/3+C_2,-2\cos2t+C_3)\).',r'Başlangıçtan \(C_1=2,C_2=2/3,C_3=0\). Dolayısıyla \(\mathbf r(t)=(t^2+2,(e^{3t}+2)/3,-2\cos2t)\).'],'IMG-20261015-WA0037.jpg'),
ex('Dersteki belirli integral üçlüsü',r'\(\int_0^1(4t^3,3,2(t+1))dt\), \(\int_1^2(6-6t,3\sqrt t,4/t^2)dt\) ve \(\int_{-\pi/4}^{\pi/4}(\sin t,1+\cos t,\sec^2t)dt\) hesaplayınız.',[
r'İlkinde ilkel fonksiyon \((t^4,3t,t^2+2t)\). Sonuç \((1,3,3)\).',r'İkincide ilkel fonksiyon \((6t-3t^2,2t^{3/2},-4/t)\). Sonuç \((-3,4\sqrt2-2,2)\).',r'Üçüncüde sinüs tek fonksiyon olduğundan ilk bileşen 0. İkinci \(\pi/2+\sqrt2\), üçüncü \(\tan(\pi/4)-\tan(-\pi/4)=2\).'],'IMG-20261023-WA0058.jpg'))
sec(t,'Yay uzunluğu ve yay parametresi',
p(r'Küçük bir zaman aralığında alınan yol yaklaşık \(\|\mathbf r\prime(t)\|dt\) olur. Bu parçaları toplamak integrali verir. Normun integralini almak gerekir; integralin normu genellikle yer değiştirmedir ve yol uzunluğundan küçük olabilir. Eğri tekrar taranırsa integral tekrar gidilen yolu da sayar.'),
f(r'L=\int_a^b\|\mathbf r\prime(t)\|dt,\qquad s(t)=\int_a^t\|\mathbf r\prime(u)\|du,\qquad\frac{ds}{dt}=\|\mathbf r\prime(t)\|.'),
ex('Dersteki 5-12-13 helisi',r'\(\mathbf r(t)=(5\cos t,5\sin t,12t)\), \(0\le t\le2\pi\), uzunluğunu bulunuz.',[
r'\(\mathbf r\prime=(-5\sin t,5\cos t,12)\); norm \(\sqrt{25\sin^2t+25\cos^2t+144}=13\).',r'\(L=\int_0^{2\pi}13dt=26\pi\). Bu aralıkta \(s=13t\) olduğundan yay parametreli biçim \((5\cos(s/13),5\sin(s/13),12s/13)\), \(0\le s\le26\pi\).'],'IMG-20261015-WA0039.jpg'))
sec(t,'Frenet çatısı: teğet, normal, binormal',
p(r'Birim teğet \(\mathbf T\) hareket yönünü gösterir. \(\mathbf T\) yön değiştiriyorsa türevi teğete diktir; birimleştirilince asal normal \(\mathbf N\) elde edilir. \(\mathbf B=\mathbf T\times\mathbf N\) eğrinin anlık dönme düzlemine diktir. Bu üçlü sağ elli ortonormal bir çatıdır.'),
f(r'\mathbf T=\frac{\mathbf r\prime}{\|\mathbf r\prime\|},\qquad\mathbf N=\frac{\mathbf T\prime}{\|\mathbf T\prime\|},\qquad\mathbf B=\mathbf T\times\mathbf N=\frac{\mathbf r\prime\times\mathbf r\prime\prime}{\|\mathbf r\prime\times\mathbf r\prime\prime\|}.'),
note('Geçerlilik koşulu',r'\(\mathbf T\) için hız sıfır olmamalıdır. \(\mathbf N\) ve \(\mathbf B\) için ayrıca eğrilik sıfır olmamalıdır. Düz bir doğruda normal ve binormal bu formüllerle tek olarak belirlenmez.'),
ex('Çemberin Frenet çatısı',r'\(\mathbf r(t)=(\cos t,\sin t,0)\) için \(\mathbf T,\mathbf N,\mathbf B\) nedir?',[
r'\(\mathbf r\prime=(-\sin t,\cos t,0)\) normu 1 olduğundan \(\mathbf T=(-\sin t,\cos t,0)\).',r'\(\mathbf T\prime=(-\cos t,-\sin t,0)\) normu da 1: \(\mathbf N=(-\cos t,-\sin t,0)\).',r'Çarpım \(\mathbf B=(0,0,1)\). Normal merkeze yönelir; binormal sabittir.'],'IMG-20261015-WA0034.jpg'),
ex('Dersteki uzay eğrisinin Frenet üçlüsü',r'\(\mathbf r(t)=(e^t,e^{-t},\sqrt2\,t)\) için \(t=0\) anındaki çatıyı bulunuz.',[
r'\(\mathbf v(0)=(1,-1,\sqrt2)\), normu 2; \(\mathbf a(0)=(1,1,0)\). Dolayısıyla \(\mathbf T(0)=(1,-1,\sqrt2)/2\).',r'\(\mathbf v(0)\cdot\mathbf a(0)=0\), süratin türevi o anda 0. \(\mathbf T\prime(0)=\mathbf a(0)/2\); normu \(1/\sqrt2\). Böylece \(\mathbf N(0)=(1,1,0)/\sqrt2\).',r'\(\mathbf B(0)=(-1/2,1/2,1/\sqrt2)\). Üç vektörün normları 1 ve ikili skaler çarpımları sıfırdır.'],'IMG-20261015-WA0040.jpg'),
fig('helix','Uzay eğrisi üzerinde T teğet, N merkeze dönme yönü, B ise ikisine dik yönü gösterir.'))
sec(t,'Eğrilik ve eğrilik yarıçapı',
p(r'Eğrilik, birim uzunluk başına teğet yönünün ne kadar değiştiğidir. Parametre daha hızlı ilerlediği için teğet daha hızlı değişebilir; bunu fiziksel hızdan ayırmak için \(d\mathbf T/dt\), \(ds/dt\) ile bölünür. Bir çemberde eğrilik yarıçapın tersidir.'),
f(r'\kappa=\left\|\frac{d\mathbf T}{ds}\right\|=\frac{\|\mathbf T\prime(t)\|}{\|\mathbf r\prime(t)\|}=\frac{\|\mathbf r\prime\times\mathbf r\prime\prime\|}{\|\mathbf r\prime\|^3},\qquad \rho=\frac1\kappa.'),
p(r'Düzlemde \(y=f(x)\) grafiği için \(\mathbf r(x)=(x,f(x),0)\) seçilirse \(\kappa=|f\prime\prime(x)|/[1+(f\prime(x))^2]^{3/2}\). Mutlak değer eğriliğin negatif olmamasını sağlar. Birim yay uzunluğuyla parametrelendirilmiş eğride \(\|d\mathbf r/ds\|=1\) ve \(\kappa=\|d^2\mathbf r/ds^2\|\).'),
ex('Genel helisin eğriliği',r'\(\mathbf r(t)=(a\cos t,a\sin t,bt)\), \(a>0\), için eğrilik nedir?',[
r'\(\|\mathbf r\prime\|=\sqrt{a^2+b^2}\). \(\mathbf r\prime\times\mathbf r\prime\prime=(ab\sin t,-ab\cos t,a^2)\), normu \(a\sqrt{a^2+b^2}\).',r'\(\kappa=a/(a^2+b^2)\), \(\rho=(a^2+b^2)/a\). \(b=0\) olursa çember sonucu \(1/a\) elde edilir.']),
p(r'Ek bilgi: eğrinin uzayda dönme düzleminin değişimini burulma ölçer. Yeterince türevlenebilir ve \(\mathbf r\prime\times\mathbf r\prime\prime\ne0\) iken \(\tau=[(\mathbf r\prime\times\mathbf r\prime\prime)\cdot\mathbf r\prime\prime\prime]/\|\mathbf r\prime\times\mathbf r\prime\prime\|^2\). Bu müfredatta temel hedef eğriliktir; burulma tamamlayıcıdır.'))
sec(t,'Hız vektörü, sürat ve ivme',
p(r'Hız \(\mathbf v=\mathbf r\prime\) vektördür; sürat \(v=\|\mathbf v\|\) sayıdır. İvme \(\mathbf a=\mathbf v\prime\), hem süratin hem yönün değişmesini içerir. Sabit sürat sıfır ivme demek değildir: çembersel harekette yön değişir. \(\mathbf v\cdot\mathbf a=\tfrac12(v^2)\prime\) olduğundan hız ve ivmenin dikliği o anda süratin türevinin sıfır olmasıyla ilişkilidir.'),
ex('Tahtadaki hareket örneği',r'\(\mathbf r(t)=(5\cos t,5\sin t,6t^2)\). Hız, ivme ve bunların dik olduğu anı bulunuz.',[
r'\(\mathbf v=(-5\sin t,5\cos t,12t)\), \(\mathbf a=(-5\cos t,-5\sin t,12)\).',r'\(\mathbf v\cdot\mathbf a=25\sin t\cos t-25\sin t\cos t+144t=144t\). Yalnızca \(t=0\) anında diktirler.'],'IMG-20261015-WA0036.jpg'),
ex('Üstel ve trigonometrik hareket',r'\(\mathbf r(t)=(e^{-t},2\cos3t,2\sin3t)\). \(t=0\) anında hız, ivme büyüklükleri ve birim teğeti bulunuz.',[
r'\(\mathbf v=(-e^{-t},-6\sin3t,6\cos3t)\), \(\mathbf a=(e^{-t},-18\cos3t,-18\sin3t)\).',r'\(\mathbf v(0)=(-1,0,6)\), \(\|\mathbf v(0)\|=\sqrt{37}\); \(\mathbf a(0)=(1,-18,0)\), \(\|\mathbf a(0)\|=\sqrt{325}=5\sqrt{13}\).',r'\(\mathbf T(0)=(-1,0,6)/\sqrt{37}\). Vektörü büyüklüğüyle karıştırmamak için sonucun türünü kontrol et.'],'IMG-20261015-WA0036.jpg'))
sec(t,'İvmenin teğetsel ve normal bileşenleri',
p(r'\(\mathbf v=v\mathbf T\) ifadesinin türevi alınırsa ivmenin bir kısmı sürati, diğer kısmı yönü değiştirir. Normal bileşen, eğriliğin ve süratin karesinin çarpımıdır. Teğetsel katsayı negatif olabilir; normal katsayı negatif değildir.'),
f(r'\mathbf a=\frac{dv}{dt}\mathbf T+\kappa v^2\mathbf N,\qquad a_T=\frac{\mathbf v\cdot\mathbf a}{\|\mathbf v\|},\qquad a_N=\frac{\|\mathbf v\times\mathbf a\|}{\|\mathbf v\|}.'),
ex('Dairesel harekette ivme',r'\(\mathbf r(t)=(a\cos\omega t,a\sin\omega t,0)\), \(a>0,\omega\ne0\) için \(a_T,a_N\) nedir?',[
r'Sürat \(a|\omega|\) sabit olduğundan \(a_T=0\). Eğrilik \(1/a\).',r'\(a_N=(1/a)(a^2\omega^2)=a\omega^2\). İvme tamamen içeriye yönelir; sürat sabit olmasına rağmen sıfır değildir.']),
li('Önce türevlerle hız ve ivmeyi bul; sonra norm al.', 'Frenet çatısı istenirse her vektörün birim ve diğerlerine dik olduğunu kontrol et.', 'Yay uzunluğunda integralin içine norm, eğrilikte normun küpünü yaz.', 'Normal ve binormal için sıfır eğrilik olasılığını kontrol et.'))

t=topic('04-cok-degiskenli-limit','Çok değişkenli fonksiyonlar, limit ve süreklilik','Tanım bölgeleri, seviye eğrileri, komşuluklar, yol testi ve sıkıştırma ile limit.','#FBBF24',[
'Tanım kümesini eşitsizliklerle ve bir çizimle ifade etmek.',
'Limitin yokluğunu iki yolla göstermek; varlığını tüm yollar için kanıtlamak.',
'Parçalı tanımlı bir fonksiyonun sürekliliğini incelemek.'])
sec(t,'Birden fazla girdiye sahip fonksiyon',
p(r'\(f:D\subseteq\mathbb R^2\to\mathbb R\) fonksiyonu her \((x,y)\) noktasına bir sayı atar. Grafik \(z=f(x,y)\) uzayda bir yüzeydir; tanım kümesi ise \(xy\) düzlemindedir. Örneğin \(A(a,h)=ah/2\) üçgen alanı iki değişkenlidir; \(V(x,y,h)=xyh\) kutu hacmi üç değişkenlidir. Üç değişkenli skaler fonksiyonun grafiği dört boyutlu olur; seviye yüzeyleriyle görselleştirilir.'),
p(r'Tanım kümesi \(D\), fonksiyonun gerçek değer almasını sağlayan bütün girdilerdir. Görüntü kümesi \(f(D)\) ise gerçekten ulaşılabilen çıktılardır. Bir ifadede birden fazla kısıt varsa hepsi aynı anda sağlanmalıdır.'),
li(r'Karekök içi en az 0 olmalı.',r'Logaritma içi kesinlikle pozitif olmalı.',r'Payda sıfır olamaz.',r'\(\arcsin u\) ve \(\arccos u\) için \(-1\le u\le1\).'))
sec(t,'Dersteki tanım bölgesi örnekleri',
ex('Disk ve eğik şerit',r'\(f(x,y)=\sqrt{64-x^2-y^2}\) ve \(g(x,y)=\arccos(x-y)\) için tanım ve görüntü kümelerini bulunuz.',[
r'İlkinde \(x^2+y^2\le64\): merkezi orijin, yarıçapı 8 olan kapalı disk. Çıktılar \([0,8]\); grafik üst yarım küredir.',r'İkincide \(-1\le x-y\le1\), yani \(x-1\le y\le x+1\). Sınır doğruları dahil bir şerit. Görüntü \([0,\pi]\).'],'IMG-20261015-WA0041.jpg'),
ex('Kök ve logaritmayı birlikte ele almak',r'\(f(x,y)=\sqrt{xy}+\log(1-x^2-y^2)\) fonksiyonunun tanım bölgesini bulunuz.',[
r'\(xy\ge0\) ve \(x^2+y^2<1\) birlikte gerekli.',r'Bölge açık birim diskin birinci ve üçüncü bölgelerde kalan parçaları ile disk içindeki eksen parçalarıdır. Eksenler dahildir; çember dahil değildir.'],'IMG-20261015-WA0042.jpg'),
ex('İşaret ayırımı gerektiren kök',r'\(f(x,y)=\sqrt{xy-x^4}+xy\) ve \(g(x,y)=\sqrt{x^2-y}+x^2+y^2+1\) tanım bölgelerini bulunuz.',[
r'İlkinde \(x(y-x^3)\ge0\). \(x>0\) iken \(y\ge x^3\), \(x<0\) iken \(y\le x^3\); \(x=0\) iken her y geçerlidir. Sonuç \(\{x>0,y\ge x^3\}\cup\{x<0,y\le x^3\}\cup\{x=0\}\).',r'İkincide \(y\le x^2\). Parabol ve altı dahildir. İlk soruda x ile bölmeden önce x işareti ayrılmazsa bölgenin yarısı kaybolur.'],'IMG-20261022-WA0053.jpg'),
ex('Her yerde tanımlı logaritma',r'\(\ln(x^2+y^2+4)\) için tanım kümesi nedir?',[
r'\(x^2+y^2+4\ge4>0\) her noktada doğrudur. Dolayısıyla tanım kümesi \(\mathbb R^2\).',r'Logaritma artan olduğundan görüntü kümesi \([\ln4,\infty)\).'],'IMG-20261022-WA0053.jpg'))
sec(t,'Seviye eğrileri ve seviye yüzeyleri',
p(r'\(f(x,y)=c\) denklemi aynı fonksiyon değerine sahip girdileri birleştirir. Haritadaki eş yükseklik eğrileri buna örnektir. Seviye eğrisi \(xy\) düzlemindedir; yüzey üzerinde \(z=c\) kesitinin düzleme izdüşümü olarak düşünülebilir. \(F(x,y,z)=c\) ise üç boyutlu uzayda bir seviye yüzeyidir.'),
ex('Paraboloidin seviye eğrileri',r'\(f(x,y)=x^2+y^2\) için \(c=0,1,4\) seviyelerini bulunuz.',[
r'\(c=0\) için yalnızca orijin, \(c=1\) için yarıçapı 1 çember, \(c=4\) için yarıçapı 2 çember vardır.',r'\(c<0\) için seviye kümesi boştur. Yüzey \(z=x^2+y^2\) yukarı açılan paraboloiddir.'],'IMG-20261015-WA0042.jpg'),
fig('levels','Aynı yüzey hem üç boyutlu grafik hem iki boyutlu seviye eğrileriyle okunabilir.'))
sec(t,'Komşuluk ve limitin tam anlamı',
p(r'\((a,b)\) merkezli, yarıçapı \(\delta\) olan açık disk bir komşuluktur. Limit tanımında merkez nokta dışarıda bırakılır. Yaklaşım yalnızca tanım kümesindeki noktalardan yapılır. \((a,b)\), bu kümenin bir yığılma noktası olmalıdır.'),
f(r'\lim_{(x,y)\to(a,b)}f(x,y)=L\ \Longleftrightarrow\ \forall\varepsilon>0\ \exists\delta>0:\ 0<\sqrt{(x-a)^2+(y-b)^2}<\delta\ \Longrightarrow\ |f(x,y)-L|<\varepsilon.'),
p(r'Burada tek bir \(\delta\), izin verilen bütün yaklaşım yönlerini aynı anda kontrol etmelidir. Bu nedenle iki eksen üzerinde aynı sonucu bulmak limitin varlığını kanıtlamaz. Buna karşılık iki farklı yol üzerinde farklı sonuç bulmak limitin yokluğunu kanıtlamaya yeter.'),
note('Doğru testi tek başına yeterli değildir',r'Bütün \(y=mx\) doğruları aynı sonucu verse bile bir parabolda başka sonuç çıkabilir. Varlık için süreklilik, cebirsel dönüşüm veya tüm yönler için geçerli bir üst sınır kullan.'))
sec(t,'Süreklilik ve doğrudan yerine koyma',
p(r'Bir fonksiyon noktada tanımlıysa ve limiti değerine eşitse o noktada süreklidir. Polinomlar her yerde, rasyonel fonksiyonlar paydaları sıfır olmayan yerde süreklidir. Sürekli fonksiyonların uygun bileşkeleri de süreklidir. Bu kurallar uygunsa en kısa çözüm doğrudan yerine koymaktır.'),
ex('Polinom limiti',r'\(P(x,y)=5x^2y^2+4xy^3-8xy^2+3\) için \((x,y)\to(1,2)\) limitini bulunuz.',[
r'Polinom her yerde süreklidir; limit \(P(1,2)\).',r'\(5\cdot1\cdot4+4\cdot1\cdot8-8\cdot1\cdot4+3=20+32-32+3=23\).'],'IMG-20261022-WA0053.jpg'),
ex('Dersin kısa limitleri',r'\(\lim_{(x,y)\to(0,0)}(2x^2+y^2+1)/(x^2+y^2+3)\), \(\lim_{(x,y)\to(0,\ln2)}e^{x-y}\), \(\lim_{(x,y)\to(1,0)}x\sin y/(x^2+1)\) nedir?',[
r'İlk payda 3 olur; limit \(1/3\).',r'İkinci ifade süreklidir: \(e^{-\ln2}=1/2\).',r'Üçüncü payda 2 ve sinüs sıfır olur; limit 0.'],'IMG-20261022-WA0053.jpg'))
sec(t,'Belirsizlikte cebir ve standart limitler',
ex('Eşlenikle sadeleştirme',r'\(\lim_{(x,y)\to(0,0)}[2-\sqrt{xy+4}]/(xy)\) hesaplayınız.',[
r'İfade kendi tanım kümesinde \(xy\ne0\) koşuluyla incelenir. Eşlenikle çarpınca pay \(4-(xy+4)=-xy\).',r'Yakında \(-1/[2+\sqrt{xy+4}]\) ile aynı olur. Bu sürekli ifadenin limiti \(-1/4\). Fonksiyonun eksenlerde tanımsız olması limit almayı engellemez.'],'IMG-20261022-WA0053.jpg'),
ex('Sinüs içeren limitler',r'\(\lim_{(x,y)\to(0,0)}\sin(xy)/x\) ve \(\lim_{(x,y)\to(0,0)}e^y\sin x/x\) hesaplayınız.',[
r'İlk ifade, uygun noktalarda \(y[\sin(xy)/(xy)]\) olur. Standart \(\sin u/u\to1\) limiti ve \(y\to0\) ile sonuç 0. Doğrudan \(|\sin(xy)/x|\le|y|\) sınırı da aynı sonucu verir.',r'İkincide \(e^y\to1\) ve \(\sin x/x\to1\); sonuç 1. Her iki limitte yaklaşım fonksiyonun tanımlı olduğu noktalar üzerindendir.'],'IMG-20261022-WA0056.jpg'))
sec(t,'İki farklı yolla limitin yokluğu',
ex('Doğruya bağlı sonuç',r'\(f(x,y)=2xy/(x^2+y^2)\) için orijindeki limiti inceleyiniz.',[
r'\(y=0\) yolunda değer 0; \(y=x\) yolunda, \(x\ne0\) için değer 1.',r'İki yol aynı noktaya gider fakat sonuçlar farklıdır. Dolayısıyla limit yoktur. Genel \(y=mx\) yolunda \(2m/(1+m^2)\) çıkar.'],'IMG-20261022-WA0058.jpg'),
ex('Parabol yoluyla limitin yokluğu',r'\(f(x,y)=(x^4-y^2)/(x^4+y^2)\) için orijindeki limiti inceleyiniz.',[
r'\(y=0\) boyunca değer 1; \(y=x^2\) boyunca değer 0. İki sonuç farklı, limit yok.',r'Genel \(y=ax^2\) yolunda \((1-a^2)/(1+a^2)\) çıkar. Bu örnek, paydadaki dereceleri eşleştirerek uygun yol seçmeyi öğretir.'],'IMG-20261022-WA0056.jpg'),
ex('İki başka karşı örnek',r'\((x-y)/(x+y)\), \(x/\sqrt{x^2+y^2}\) ve \((x^2+y^2)/y^2\) orijinde limite sahip midir?',[
r'İlkinde \(y=0\) yolu 1, \(x=0\) yolu -1 verir. İkinci ifadede pozitif x ekseni 1, negatif x ekseni -1 verir. İkisinin de limiti yoktur.',r'Üçüncüde y sıfır olamaz; \(y=x\) yolunda 2, \(y=2x\) yolunda \(5/4\) çıkar. Bu limit de yoktur. Tanımsız yolları test yolu olarak seçme.'],'IMG-20261022-WA0054.jpg'))
sec(t,'Kutupsal koordinatlar ve sıkıştırma',
p(r'Orijine yaklaşırken \(x=r\cos\theta,y=r\sin\theta\), \(r\to0^+\) dönüşümü yararlıdır. Ancak sabit bir açı seçmek yalnızca bir ışını test eder. Limitin varlığını göstermek için \(\theta\) ne olursa olsun sıfıra giden bir sınır bulunmalıdır. Örneğin \(|r\cos\theta\sin^2\theta|\le r\) eşitsizliği böyle bir sınırdır.'),
ex('Dersteki parçalı fonksiyonun sürekliliği',r'\(f(x,y)=\sin(xy^2)/(x^2+y^2)\) orijin dışında, \(f(0,0)=0\) olsun. Her yerde sürekli olduğunu gösteriniz.',[
r'Orijin dışında payda sıfır değildir, dolayısıyla süreklidir. Orijinde \(|\sin u|\le|u|\) kullanılır.',r'\(|f(x,y)|\le |x|y^2/(x^2+y^2)\le|x|\le\sqrt{x^2+y^2}\to0\). Böylece limit 0 olur ve atanmış değere eşittir.',r'Kutupsal yazım da sınırı \(r|\cos\theta|\sin^2\theta\le r\) yapar. Bu tüm açılar için geçerli olduğu için kanıttır.'],'IMG-20261022-WA0054.jpg'),
fig('paths','Aynı noktaya farklı yollarla yaklaşılır. Limitin varlığı bütün bu yolları aynı anda kapsar.'))
sec(t,'Limit için uygulanabilir karar sırası',
li('Önce tanım kümesini ve noktanın yığılma noktası olup olmadığını kontrol et.', 'Süreklilik uygunsa yerine koy. Belirsizlik varsa eşlenik veya çarpanlara ayırma dene.', 'Yokluk şüphesinde iki uygun yol seç; farklı sonuç bulunca kanıt tamamdır.', 'Varlık şüphesinde sıkıştırma veya açıdan bağımsız bir kutupsal üst sınır kur.', 'Parçalı tanımda bulunan limiti atanmış nokta değeriyle karşılaştır.'),
ex('Bütün doğruların aynı sonucu vermesi yetmez',r'\(f(x,y)=x^2y/(x^4+y^2)\) orijinde limite sahip midir?',[
r'\(y=mx\) ve sabit \(m\ne0\) için \(f=mx/(x^2+m^2)\to0\). \(m=0\) ve dikey eksen de 0 verir.',r'Fakat \(y=x^2\) boyunca \(f=1/2\). Bu nedenle limit yoktur. Bütün doğruların kontrol edilmesi bile genel limit için yeterli değildir.']))

t=topic('05-kismi-turev','Kısmi türev, teğet düzlem ve lineer yaklaşım','Kısmi ve karma türevler, türevlenebilirlik, diferansiyel, lineerleştirme ve hata sınırı.','#F472B6',[
'Kısmi türev alırken hangi değişkenin sabit tutulduğunu açıklamak.',
'Kısmi türevlerin varlığı ile türevlenebilirliği ayırt etmek.',
'Teğet düzlem, diferansiyel ve lineer yaklaşımı hata sınırıyla kullanmak.'])
sec(t,'Kısmi türev: tek yöndeki değişim',
p(r'İki değişkenli bir fonksiyonda x değişirken y sabit tutulursa tek değişkenli bir kesit elde edilir. Bu kesitin türevi \(f_x\) olur. Benzer biçimde y değişirken x sabit tutularak \(f_y\) bulunur. Sabit tutmak, diğer değişkeni sıfır yapmak demek değildir; türev sırasında katsayı gibi davranmasını sağlamaktır.'),
f(r'f_x(a,b)=\lim_{h\to0}\frac{f(a+h,b)-f(a,b)}h,\qquad f_y(a,b)=\lim_{h\to0}\frac{f(a,b+h)-f(a,b)}h.'),
ex('Dersteki temel kısmi türev',r'\(f(x,y)=x^2y^3+3x\) için birinci kısmi türevleri bulunuz.',[
r'x yönünde y sabittir: \(f_x=2xy^3+3\). y yönünde x sabittir: \(f_y=3x^2y^2\).',r'Örneğin \((1,2)\) noktasında \(f_x=19\), \(f_y=12\). Bunlar yüzeyin koordinat kesitlerindeki eğimleridir.'],'IMG-20261022-WA0055.jpg'),
ex('Limit tanımıyla kısmi türev',r'\(f(x,y)=x^2y\) için \(f_x(a,b)\) değerini tanımdan bulunuz.',[
r'\([f(a+h,b)-f(a,b)]/h=[(a+h)^2b-a^2b]/h=2ab+bh\).',r'h sıfıra giderken \(f_x(a,b)=2ab\) elde edilir. Bu, diğer değişkeni neden sabit tuttuğumuzu doğrudan gösterir.']))
sec(t,'Yüksek mertebeli ve karma türevler',
p(r'Birinci kısmi türevler de fonksiyon olduğundan yeniden türevlenebilir. Bu notlarda \(f_{xy}=(f_x)_y\): önce x, sonra y türevi demektir. İşlem sırasını açık yazmak farklı kaynaklardaki gösterim karışıklığını önler. Karma türevler bir komşulukta sürekli ise Clairaut-Schwarz teoremi \(f_{xy}=f_{yx}\) verir.'),
f(r'f_{xx}=\frac{\partial^2 f}{\partial x^2},\quad f_{xy}=\frac{\partial}{\partial y}\left(\frac{\partial f}{\partial x}\right),\quad f_{yx}=\frac{\partial}{\partial x}\left(\frac{\partial f}{\partial y}\right),\quad f_{yy}=\frac{\partial^2f}{\partial y^2}.'),
ex('Dersteki rasyonel fonksiyonun ikinci türevleri',r'\(f(x,y)=xy/(x^2+y^2)\), \((x,y)\ne(0,0)\) için ikinci kısmi türevleri bulunuz.',[
r'\(S=x^2+y^2\) kısaltmasıyla bölüm kuralından \(f_x=y(y^2-x^2)/S^2\), \(f_y=x(x^2-y^2)/S^2\).',r'\(f_{xx}\) için \(-2xy/S^2-4xy(y^2-x^2)/S^3\) ortak paydada toplanır: \(f_{xx}=2xy(x^2-3y^2)/S^3\).',r'Simetriyle \(f_{yy}=2xy(y^2-3x^2)/S^3\). Karma türev \(f_{xy}=(-x^4+6x^2y^2-y^4)/S^3\).',r'Orijin dışında türevler süreklidir; \(f_{yx}=f_{xy}\). Orijinde başlangıç fonksiyonu tanımlı olmadığı için bu formüller orijine uygulanmaz.'],'IMG-20261022-WA0055.jpg'),
note('Teoremin koşulları',r'Karma türevlerin eşitliğini koşulsuz kabul etme. Sürekli ikinci kısmi türevler yeterli bir koşuldur; parçalı tanımlı fonksiyonlarda ayrı kontrol gerekebilir.'))
sec(t,'Türevlenebilirlik neden daha güçlüdür?',
p(r'Kısmi türevler iki özel yönü ölçer. Türevlenebilirlik ise noktanın çevresindeki tüm küçük değişimlerin aynı lineer fonksiyonla açıklanabilmesini ister. Hata, yer değiştirmenin uzunluğuna göre ihmal edilebilir olmalıdır. Bu koşul teğet düzlemin yüzeyi yerel olarak temsil etmesini sağlar.'),
f(r'f(a+h,b+k)=f(a,b)+f_x(a,b)h+f_y(a,b)k+R(h,k),\quad\frac{R(h,k)}{\sqrt{h^2+k^2}}\to0.'),
p(r'\(f_x,f_y\) bir komşulukta var ve noktada sürekli ise f o noktada türevlenebilirdir. Türevlenebilirlik sürekliliği ve kısmi türevlerin varlığını gerektirir. Ters yöndeki çıkarımlar tek başlarına doğru değildir.'),
ex('Kısmi türevler var, süreklilik yok',r'\(f(x,y)=xy/(x^2+y^2)\) orijin dışında, \(f(0,0)=0\) olsun. Orijinde kısmi türevleri ve türevlenebilirliği inceleyiniz.',[
r'Eksenler boyunca fonksiyon sıfırdır. Bu yüzden \(f_x(0,0)=f_y(0,0)=0\).',r'\(y=x\) boyunca değer \(1/2\), dolayısıyla fonksiyon orijinde sürekli değildir. Sürekli olmayan fonksiyon türevlenebilir olamaz.']))
sec(t,'Teğet düzlem ve normal doğru',
p(r'\(z=f(x,y)\) grafiğinde \(P=(a,b,f(a,b))\) noktasındaki iki teğet yön \((1,0,f_x)\) ve \((0,1,f_y)\) olur. Çarpımları \((-f_x,-f_y,1)\) normalini verir. Yeterli türevlenebilirlik koşulları altında bu normal teğet düzlemi belirler.'),
f(r'z-f(a,b)=f_x(a,b)(x-a)+f_y(a,b)(y-b).'),
f(r'\text{Normal doğru: }\ (x,y,z)=(a,b,f(a,b))+t(-f_x(a,b),-f_y(a,b),1).'),
ex('Teğet düzlem ve lineer model',r'\(f(x,y)=x^2+y^2\) için \((1,2,5)\) noktasındaki teğet düzlemi ve normal doğruyu bulunuz.',[
r'\(f_x=2x,f_y=2y\). Noktadaki eğimler 2 ve 4. Düzlem \(z-5=2(x-1)+4(y-2)\), yani \(z=2x+4y-5\).',r'Normal doğru \((x,y,z)=(1,2,5)+t(-2,-4,1)\). Normalin işaretini ters almak aynı doğruyu verir.']),
fig('tangent','Yüzey ile teğet düzlem, temas noktası yakınında aynı birinci mertebe değişimi verir.'))
sec(t,'Lineerleştirme ve yaklaşık değer',
p(r'Lineerleştirme \(L(x,y)\), teğet düzlemin z değeri olarak okunan afin fonksiyondur. Hesabı kolay bir merkez seçilir; merkezdeki fonksiyon değeri ve türevler bulunur; hedef noktanın küçük farkları formüle konur. Yaklaşımın güvenilirliği, merkeze uzaklık ve ikinci türevlerin büyüklüğüne bağlıdır.'),
f(r'L(x,y)=f(a,b)+f_x(a,b)(x-a)+f_y(a,b)(y-b),\qquad f(x,y)\approx L(x,y).'),
ex('Dersteki üstel fonksiyonun iki lineerleştirmesi',r'\(f(x,y)=e^{2y-x}\) için \(P=(0,0)\) ve \(Q=(1,2)\) merkezlerindeki lineerleştirmeleri bulunuz.',[
r'\(f_x=-e^{2y-x}\), \(f_y=2e^{2y-x}\). P merkezinde \(L_P=1-x+2y\).',r'Q merkezinde \(f=e^3,f_x=-e^3,f_y=2e^3\). Bu yüzden \(L_Q=e^3-e^3(x-1)+2e^3(y-2)=e^3(2y-x-2)\).',r'Her model kendi merkezinin yakınında kullanılır. Örneğin \(f(0.01,0.02)=e^{0.03}\approx1.03\); bu hedef P merkezine yakındır.'],'IMG-20261105-WA0038.jpg'),
ex('Karekökün yaklaşık değeri',r'\(\sqrt{(3.01)^2+(3.98)^2}\) ifadesini diferansiyel veya lineer modelle yaklaşık hesaplayınız.',[
r'\(f(x,y)=\sqrt{x^2+y^2}\), merkez \((3,4)\), \(f=5\). \(f_x=3/5,f_y=4/5\).',r'\(h=0.01,k=-0.02\). Yaklaşık değer \(5+(3/5)(0.01)+(4/5)(-0.02)=4.99\).']))
sec(t,'Lineer yaklaşımın hata sınırı',
p(r'İkinci türevler merkezi hedefe bağlayan parçayı içeren bir bölgede sürekli ve \(|f_{xx}|\le M\), \(|f_{xy}|\le M\), \(|f_{yy}|\le M\) olsun. Tek değişkenli Taylor teoremi \(g(t)=f(a+th,b+tk)\) fonksiyonuna uygulanırsa aşağıdaki güvenli üst sınır elde edilir. M yalnızca merkezdeki değer değildir; bütün ilgili bölgede geçerli olmalıdır.'),
f(r'|f(a+h,b+k)-L(a+h,b+k)|\le\frac M2(|h|+|k|)^2.'),
ex('Defterdeki hata sınırı',r'\(f=x^2+3xy+2y^2+4\), merkez \((2,1)\), \(|x-2|,|y-1|\le0.01\). Lineerleştirmeyi ve hata sınırını bulunuz.',[
r'\(f(2,1)=16\), \(f_x(2,1)=7\), \(f_y(2,1)=10\). \(L=16+7(x-2)+10(y-1)=7x+10y-8\).',r'\(f_{xx}=2,f_{xy}=3,f_{yy}=4\). M=4 seçilir; hata en fazla \(\tfrac42(0.01+0.01)^2=0.0008\).',r'Kontrol: gerçek kalan \(h^2+3hk+2k^2\) olur. Mutlak değer için daha sıkı \(0.0006\) sınırı da mümkündür; dersteki \(0.0008\) güvenli ve doğrudur.'],'IMG-20261022-WA0060.jpg'),
ex('İkinci hata sınırı sorusu',r'\(f=x^2-3xy+y^2\), merkez \((1,2)\), \(|x-1|,|y-2|\le0.1\). L ve güvenli hata sınırını bulunuz.',[
r'\(f(1,2)=-1,f_x=-4,f_y=1\) olduğundan \(L=-1-4(x-1)+(y-2)=-4x+y+1\).',r'İkinci türevlerin mutlak değerleri 2,3,2; M=3. Hata \(\le(3/2)(0.1+0.1)^2=0.06\).'],'IMG-20261105-WA0038.jpg'),
ex('Küçük bölgede kosinüs hatası',r'\(f(x,y)=1+x+\cos y\), merkez \((0,0)\), \(|x|,|y|\le0.2\). L ve hata sınırını bulunuz.',[
r'\(f(0,0)=2,f_x=1,f_y(0,0)=0\). Böylece \(L=2+x\).',r'\(f_{xx}=f_{xy}=0,|f_{yy}|=|\cos y|\le1\). Genel sınır 0.08 verir; yalnız y yönündeki gerçek ikinci terim kullanılırsa \(|f-L|=|\cos y-1|\le y^2/2\le0.02\).'],'IMG-20261105-WA0040.jpg'))
sec(t,'Tam diferansiyel ve gerçek artış',
p(r'Gerçek artış \(\Delta f=f(a+\Delta x,b+\Delta y)-f(a,b)\) tam farktır. Diferansiyel \(df=f_x\,dx+f_y\,dy\) bu farkın lineer kısmıdır. Yaklaşık hesapta \(dx=\Delta x,dy=\Delta y\) alınır; buna rağmen \(df\) ve \(\Delta f\) genel olarak eşit değildir. Üç değişkende \(dw=f_xdx+f_ydy+f_zdz\).'),
ex('Tahtadaki silindir hacmi değişimi',r'Yarıçapı 3 cm, yüksekliği 10 cm olan silindirde yarıçap 0.01 cm artsın, yükseklik 0.1 cm azalsın. Hacim değişimini yaklaşık bulunuz.',[
r'\(V=\pi r^2h\); \(dV=2\pi rh\,dr+\pi r^2\,dh\). \(dr=0.01,dh=-0.1\).',r'\(dV=60\pi(0.01)+9\pi(-0.1)=-0.3\pi\) santimetre küp. Başlangıç hacmi \(90\pi\), yeni hacim yaklaşık \(89.7\pi\).',r'Tam değer \(\pi(3.01)^2(9.9)=89.69499\pi\). Yaklaşık ve tam değer arasındaki fark \(0.00501\pi\); yüksek mertebeli terimlerden gelir.'],'IMG-20261108-WA0066.jpg'),
ex('Silindir için ikinci ders sorusu',r'Yarıçap 10 cm den 9.9 cm ye, yükseklik 30 cm den 30.3 cm ye değişiyor. Yaklaşık hacim değişimi nedir?',[
r'\(dr=-0.1,dh=0.3\). \(dV=2\pi(10)(30)(-0.1)+\pi(100)(0.3)=-30\pi\) santimetre küp.',r'Başlangıç hacmi \(3000\pi\), yeni hacim yaklaşık \(2970\pi\). İşaret hacmin azaldığını gösterir.'],'IMG-20261108-WA0083.jpg'))
sec(t,'İkinci tam diferansiyel ve Hessian',
p(r'Bağımsız \(dx,dy\) artışları sabit kabul edilerek bir kez daha diferansiyel alınır. Karma terim iki kez geldiği için katsayı 2 olur. \(d^2f\), karesi alınmış \(df\) değildir. İkinci mertebe Taylor yaklaşımında bu terimin yarısı kullanılır.'),
f(r'd^2f=f_{xx}dx^2+2f_{xy}dx\,dy+f_{yy}dy^2,\qquad f(a+h,b+k)\approx f+df+\frac12d^2f.'),
f(r'd^2w=w_{xx}dx^2+w_{yy}dy^2+w_{zz}dz^2+2w_{xy}dx\,dy+2w_{xz}dx\,dz+2w_{yz}dy\,dz.'),
ex('Tahtadaki polinom diferansiyeli',r'\(f=x^3+5xy^2+3xy+4x-3y+5\) için df ve ikinci diferansiyeli yazınız.',[
r'\(f_x=3x^2+5y^2+3y+4\), \(f_y=10xy+3x-3\). df bu katsayılarla dx ve dy nin toplamıdır.',r'\(f_{xx}=6x,f_{xy}=10y+3,f_{yy}=10x\). Dolayısıyla \(d^2f=6x\,dx^2+2(10y+3)dx\,dy+10x\,dy^2\).'],'IMG-20261108-WA0082.jpg'),
ex('Üç değişkenli polinomun diferansiyelleri',r'\(w=3x^2yz^2-3xy+2yz^2+xyz\) için birinci ve ikinci diferansiyeli bulunuz.',[
r'\(w_x=6xyz^2-3y+yz\), \(w_y=3x^2z^2-3x+2z^2+xz\), \(w_z=6x^2yz+4yz+xy\). \(dw=w_xdx+w_ydy+w_zdz\).',r'\(w_{xx}=6yz^2,w_{yy}=0,w_{zz}=6x^2y+4y\). Karma türevler \(w_{xy}=6xz^2-3+z\), \(w_{xz}=12xyz+y\), \(w_{yz}=6x^2z+4z+x\).',r'İkinci diferansiyel bu altı katsayı yukarıdaki genel formüle yerleştirilerek elde edilir. Her karma terimin katsayısı 2 ile çarpılır.'],'IMG-20261108-WA0082.jpg'))
sec(t,'Türevlenebilirliğe ilişkin hızlı kontrol',
li('Kısmi türevde diğer girdiyi sabit tut; nokta değerini türev aldıktan sonra yerleştir.', 'Karma türevde hangi değişkene önce türev aldığını yaz.', 'Teğet düzlem için yüzeydeki noktanın gerçekten grafiğin üzerinde olduğunu doğrula.', 'Lineerleştirmede sabit terimi unutma: L merkezde f değerini vermeli.', 'Hata üst sınırında ikinci türevleri bütün bölgede sınırla; yalnız merkezde ölçme.'))

t=topic('06-zincir-gradyan','Zincir kuralı, yönlü türev ve gradyan','Bağımlılık ağaçları, kapalı türev, değişken dönüşümleri, en hızlı artış ve seviye yüzeyine normal.','#FB923C',[
'Birden fazla yoldan gelen türev katkılarını zincir kuralında toplamak.',
'Kapalı denklemlerde türevleri geçerlilik koşullarıyla hesaplamak.',
'Gradyan ve birim yön kullanarak yönlü türev ve en hızlı artışı bulmak.'])
sec(t,'Bağımlılık ağacı ve tek parametreli zincir kuralı',
p(r'\(z=f(x,y)\) ve \(x=x(t),y=y(t)\) ise t değişince z iki yoldan etkilenir. Her yol üzerindeki türevler çarpılır ve yollar toplanır. Önce hangi değişkenin hangisine bağlı olduğunu çizmek, eksik terimleri önler. f nin türevleri \((x(t),y(t))\) noktasında değerlendirilir.'),
f(r'\frac{dz}{dt}=f_x\frac{dx}{dt}+f_y\frac{dy}{dt},\qquad\frac{dw}{dt}=f_xx\prime(t)+f_yy\prime(t)+f_zz\prime(t).'),
p(r'İkinci formülde \(f_xx\prime\) ifadesi \(f_x\,x\prime\) çarpımıdır; ikinci kısmi türev \(f_{xx}\) ile karıştırılmamalıdır. Bütün ara değişkenler aynı parametreye bağlıysa d/dt kullanılır.'),
ex('Tahtadaki trigonometrik zincir örneği',r'\(z=x^2+y^2\), \(x=\cos t+\sin t\), \(y=\cos t-\sin t\). dz/dt nedir?',[
r'\(z_x=2x,z_y=2y\); \(x\prime=-\sin t+\cos t\), \(y\prime=-\sin t-\cos t\). Zincir toplamı 0 olur.',r'Doğrudan kontrol: \((\cos t+\sin t)^2+(\cos t-\sin t)^2=2\). Sabit fonksiyonun türevi 0.'],'IMG-20261105-WA0041.jpg'),
ex('Çarpanlı fonksiyonda zincir kuralı',r'\(z=xy\), \(x=\cos t,y=\sin t\). dz/dt yi bulunuz.',[
r'\(z_x=y,z_y=x\). Böylece \(z\prime=\sin t(-\sin t)+\cos t\cos t=\cos^2t-\sin^2t\).',r'Doğrudan \(z=\tfrac12\sin2t\) türevi de \(\cos2t\), aynı sonuçtur.'],'IMG-20261105-WA0041.jpg'))
sec(t,'İki yeni değişkene bağlı zincir kuralı',
p(r'\(z=f(x(u,v),y(u,v))\) olduğunda u ve v bağımsız yeni değişkenlerdir. u ya göre türev alırken v sabit tutulur. Aynı dış fonksiyonun farklı iç yolları katkı verir. Daha çok ara değişken varsa her biri için bir terim eklenir.'),
f(r'\frac{\partial z}{\partial u}=f_xx_u+f_yy_u,\qquad\frac{\partial z}{\partial v}=f_xx_v+f_yy_v.'),
p(r'Bu formüllerde \(f_xx_u\), \(f_x\,x_u\) çarpımıdır. Matris biçimi \(D(f\circ g)=Df(g)Dg\) ile aynı düzeni ifade eder. Çarpım sırası, önce iç değişkenlerin değişimi sonra dış fonksiyonun etkisi uygulanacak biçimdedir.'),
ex('Tahtadaki logaritma örneği',r'\(z=\ln(x^2+y^2)\), \(x=e^u\cos v,y=e^u\sin v\). \(z_u,z_v\) nedir?',[
r'\(f_x=2x/(x^2+y^2)\), \(f_y=2y/(x^2+y^2)\). \(x_u=x,y_u=y,x_v=-y,y_v=x\).',r'\(z_u=2(x^2+y^2)/(x^2+y^2)=2\); \(z_v=(-2xy+2xy)/(x^2+y^2)=0\).',r'Kontrol: \(x^2+y^2=e^{2u}\), dolayısıyla \(z=2u\).'],'IMG-20261108-WA0074.jpg'),
ex('Üç ara değişkenli ders örneği',r'\(S=\ln(x^2+y^2+z^2)\), \(x=u+v,y=u-v,z=2\sqrt{uv}\). Pozitif u ve v için \(S_u,S_v\) bulunuz.',[
r'\(x_u=x_v=1,y_u=1,y_v=-1,z_u=v/\sqrt{uv},z_v=u/\sqrt{uv}\).',r'Payda \(x^2+y^2+z^2=2(u+v)^2\). Zincir toplamları \(S_u=S_v=2/(u+v)\).',r'Doğrudan \(S=\ln2+2\ln(u+v)\) aynı sonucu verir. \(u,v>0\) seçimi kökün içte türevlenmesini ve logaritmanın tanımını güvenceye alır.'],'IMG-20261108-WA0077.jpg'))
sec(t,'Hem doğrudan hem dolaylı bağımlılık',
p(r'Bazen bir değişken hem f içinde doğrudan görünür hem de ara değişkenlerin içinde yer alır. Örneğin \(z=f(x,y)\), \(y=y(x)\) ise f nin x e doğrudan katkısı da eklenmelidir. Yalnızca dolaylı yolu almak bir terimi kaybettirir.'),
f(r'\frac{dz}{dx}=f_x+f_y\frac{dy}{dx}.'),
ex('İki bağımsız yeni değişkenle karmaşık örnek',r'\(z=e^{x/y}\), \(x=\sin u,y=u^2v\), \(u,v\ne0\). \(z_u,z_v\) yi bulunuz.',[
r'\(f_x=e^{x/y}/y\), \(f_y=-xe^{x/y}/y^2\). \(x_u=\cos u,x_v=0,y_u=2uv,y_v=u^2\).',r'\(z_u=e^{\sin u/(u^2v)}[\cos u/(u^2v)-2\sin u/(u^3v)]\).',r'\(z_v=-e^{\sin u/(u^2v)}\sin u/(u^2v^2)\). İç ifadeyi önce sadeleştirip türev almak da kontrol yöntemidir.'],'IMG-20261108-WA0079.jpg'))
sec(t,'Kapalı fonksiyonlarda türev',
p(r'\(F(x,y)=0\) denklemi y yi açıkça çözmeden yerel olarak y(x) tanımlayabilir. F bir komşulukta sürekli birinci türevlere sahipse ve \(F_y\ne0\) ise kapalı fonksiyon teoremi bu yerel çözümü güvenceye alır. Türev alınırken y nin de x e bağlı olduğu unutulmamalıdır.'),
f(r'F_x+F_yy\prime=0\quad\Longrightarrow\quad y\prime=-\frac{F_x}{F_y},\qquad F_y\ne0.'),
p(r'Üç değişkende \(F(x,y,z)=0\), z yi yerel olarak z(x,y) tanımlıyorsa x türevinde y sabit, y türevinde x sabit tutulur. Sürekli birinci türevler ve \(F_z\ne0\) koşuluyla aşağıdaki formüller geçerlidir.'),
f(r'z_x=-\frac{F_x}{F_z},\qquad z_y=-\frac{F_y}{F_z}.'),
ex('Tahtadaki kapalı türev sorusu',r'\(2x^4z^3+3xy^2+4xz+3y+5x-23=0\) denkleminin tanımladığı z(x,y) için \((1,2)\) noktasında \(z_x,z_y\) nedir?',[
r'Önce z bulunur: \(2z^3+4z=0\). Gerçek çözüm \(z=0\); inceleme noktası \((1,2,0)\).',r'\(F_x=8x^3z^3+3y^2+4z+5\), \(F_y=6xy+3\), \(F_z=6x^4z^2+4x\).',r'Noktada \(F_x=17,F_y=15,F_z=4\ne0\). Böylece \(z_x=-17/4,z_y=-15/4\). Yerel z(x,y) yorumu geçerlidir.'],'IMG-20261108-WA0081.jpg'),
ex('Kapalı denklemin teğet düzlemi',r'\(x^2+y^2+z^2=9\) küresinin \((1,2,2)\) noktasındaki teğet düzlemi nedir?',[
r'\(F=x^2+y^2+z^2-9\), gradyanı \((2x,2y,2z)\). Noktada normal \((2,4,4)\).',r'\(2(x-1)+4(y-2)+4(z-2)=0\), yani \(x+2y+2z=9\). Bu normal merkezden noktaya giden yarıçapla paraleldir.']))
sec(t,'İkinci türevde zincir kuralı',
p(r'Bir değişken dönüşümünde ikinci türev alınırken ilk zincir toplamının hem katsayıları hem türevleri değişir. Bu nedenle iç fonksiyonların ikinci türevleri de ortaya çıkar. \(x=x(t),y=y(t)\) için sürekli ikinci türevler varsayımıyla:'),
f(r'\frac{d^2z}{dt^2}=f_{xx}(x\prime)^2+2f_{xy}x\prime y\prime+f_{yy}(y\prime)^2+f_xx\prime\prime+f_yy\prime\prime.'),
ex('Dersteki diferansiyel denklem dönüşümü',r'\(x=e^t\) dönüşümü altında \(x^2y_{xx}+xy_x-y=0\) denklemini t değişkenine dönüştürünüz.',[
r'\(dt/dx=1/x\). Dolayısıyla \(y_x=y_t/x\).',r'Yeniden x türevi: \(y_{xx}=(y_{tt}-y_t)/x^2\). Burada hem \(y_t\) hem \(1/x\) türevlenir.',r'Denklem \((y_{tt}-y_t)+y_t-y=0\), yani \(y_{tt}-y=0\) olur. Dönüşüm \(x>0\) için geçerlidir.'],'IMG-20261105-WA0042.jpg'))
sec(t,'Gradyan: türevleri bir vektörde toplamak',
note('Müfredatı tamamlayan anlatım',r'Fotoğraflarda zincir kuralı ve kapalı türev örnekleri açıkça görülüyor. Yönlü türev ve gradyan ise verilen müfredatın 6. başlığında yer alıyor; bu alt bölümler standart vektör analizi kurallarıyla tamamlandı. Aşağıdaki örnekler ders tahtasından aktarılmış sorular olarak sunulmuyor.'),
p(r'Bir skaler alanın gradyanı kısmi türevlerden oluşan vektördür. Sıcaklık alanında her noktada hangi yöne gidildiğinde sıcaklığın daha hızlı arttığını anlatır. Skaler alan sayısal değer verir; onun gradyanı bir vektör alanıdır. Bu fark, birim ve boyut kontrolü için önemlidir.'),
f(r'\nabla f=(f_x,f_y),\qquad\nabla F=(F_x,F_y,F_z).'),
p(r'Türevlenebilirlik altında küçük bir \(\mathbf h\) yer değiştirmesi için \(f(P+\mathbf h)-f(P)\approx\nabla f(P)\cdot\mathbf h\). Böylece önceki bölümdeki tam diferansiyel, gradyanın yer değiştirmeyle skaler çarpımıdır. Gradyanın bileşenleri, koordinat eksenlerindeki değişim hızlarıdır.'))
sec(t,'Yönlü türev ve yönü birimleştirme',
p(r'Kısmi türev yalnız eksenler boyunca değişimi ölçerken yönlü türev seçilen herhangi bir birim yönde birim uzunluk başına değişimi ölçer. \(\mathbf u\) birim olmak zorundadır. Yön \(\mathbf v\) olarak verilirse önce \(\mathbf v/\|\mathbf v\|\) alınır. P den Q ya yön sorulursa vektör Q-P dir.'),
f(r'D_{\mathbf u}f(P)=\lim_{h\to0}\frac{f(P+h\mathbf u)-f(P)}h=\nabla f(P)\cdot\mathbf u,\qquad\|\mathbf u\|=1.'),
p(r'Son eşitlik f nin P de türevlenebilirliği altında geçerlidir. Yalnızca kısmi türevlerin varlığını bilmek yeterli değildir. Birim olmayan vektörle skaler çarpım, o parametrizasyonun hızını da içerir; standart yönlü türevle aynı sayı olmayabilir.'),
ex('Birim olmayan yönden yönlü türev',r'\(f(x,y)=x^2y+3y\), \(P=(1,2)\), yön \(\mathbf v=(3,4)\). Yönlü türev nedir?',[
r'\(f_x=2xy,f_y=x^2+3\). \(\nabla f(1,2)=(4,4)\).',r'Yönün normu 5; \(\mathbf u=(3/5,4/5)\). \(D_{\mathbf u}f=4(3/5)+4(4/5)=28/5\).',r'Birimleştirmeden alınan 28 sonucu, parametre hızını 5 katına çıkarır ve bu sorunun istediği birim uzunluk başına türev değildir.']),
ex('P den Q ya doğru değişim',r'\(F(x,y,z)=x^2+y^2+z^2\), \(P=(1,0,2)\), \(Q=(3,1,4)\). P de Q yönündeki türev nedir?',[
r'\(Q-P=(2,1,2)\), norm 3; birim yön \((2,1,2)/3\). \(\nabla F(P)=(2,0,4)\).',r'Skaler çarpım \((4+0+8)/3=4\). Sonucun pozitif olması bu yönde ilk anda alan değerinin arttığını gösterir.']))
sec(t,'En hızlı artış, azalış ve değişmeyen yön',
p(r'Sıfır olmayan gradyan için \(D_{\mathbf u}f=\|\nabla f\|\cos\theta\). En büyük kosinüs 1, en küçük -1 olduğundan en hızlı artış gradyan yönündedir. Gradyana dik yönlerde birinci mertebeden değişim sıfırdır. Bu, fonksiyonun o doğrultuda her uzaklıkta sabit kalacağı anlamına gelmez.'),
f(r'\max_{\|\mathbf u\|=1}D_{\mathbf u}f=\|\nabla f\|,\quad\mathbf u_{\max}=\frac{\nabla f}{\|\nabla f\|},\quad\min D_{\mathbf u}f=-\|\nabla f\|.'),
ex('Gradyanla yön seçmek',r'\(f=x^2+2y^2\) için P=(1,1) noktasında en hızlı artış yönü, hızı ve sıfır değişim yönü nedir?',[
r'\(\nabla f=(2x,4y)\); P de \((2,4)\), norm \(2\sqrt5\). En hızlı artış birim yönü \((1,2)/\sqrt5\), hızı \(2\sqrt5\).',r'En hızlı azalış ters yönde ve türev \(-2\sqrt5\). Sıfır türev yönlerinden biri \((-2,1)/\sqrt5\), çünkü \((2,4)\cdot(-2,1)=0\).']),
note('Gradyan sıfırsa',r'\(\nabla f(P)=\mathbf0\) ve f türevlenebilir ise tüm birim yönlerde birinci yönlü türev sıfırdır. Bu bilgi tek başına maksimum, minimum veya sabitlik göstermez; daha yüksek mertebe inceleme gerekir.'),
fig('gradient','Gradyan seviye eğrisine diktir. Birim yön gradyana döndükçe yönlü türev artar.'))
sec(t,'Gradyan neden seviye kümesine diktir?',
p(r'\(f(x(t),y(t))=c\) seviye eğrisi boyunca sabittir. Zincir kuralıyla \(0=f_xx\prime+f_yy\prime=\nabla f\cdot\mathbf r\prime\). Dolayısıyla sıfır olmayan gradyan eğrinin teğetine diktir. Üç boyutta aynı kanıt seviye yüzeyi üzerindeki bütün teğet yönler için geçerlidir.'),
f(r'\nabla F(P)\cdot\big((x,y,z)-P\big)=0,\qquad F(P)=c,\quad\nabla F(P)\ne\mathbf0.'),
ex('Seviye eğrisinin teğet doğrusu',r'\(x^2+2y^2=3\) eğrisinin (1,1) noktasındaki teğeti nedir?',[
r'Gradyan \((2,4)\) teğete normaldir. \(2(x-1)+4(y-1)=0\), yani \(x+2y=3\).',r'Bu doğrultu önceki örnekteki sıfır yönlü türev doğrultusuyla aynıdır. Teğet doğrusu eğriye yalnızca yerel olarak yaklaşır.']))
sec(t,'Bütün konuları bağlayan çözüm stratejisi',
li('Değişkenlerin bağımlılıklarını önce yaz; her bağımsız yolun katkısını ekle.', 'Kapalı türevde önce noktayı tamamla, sonra paydadaki türevin sıfır olmadığını denetle.', 'Yönlü türevde yönü birimleştir; türevlenebilirlik koşulunu kontrol et.', 'En hızlı artış yön sorusudur, en hızlı artış hızı ise norm sorusudur.', 'Seviye yüzeyinde gradyanı normal olarak kullan; noktanın yüzeyde olduğunu doğrula.'),
ex('Birleşik pekiştirme',r'\(f(x,y)=e^{x-y}\), P=(0,0). P de teğet düzlem, \((1,1)\) yönünde türev ve en hızlı artış yönünü bulunuz.',[
r'\(f(P)=1,\nabla f(P)=(1,-1)\). Grafik üzerindeki teğet düzlem \(z=1+x-y\).',r'Birim yön \((1,1)/\sqrt2\); yönlü türev 0. En hızlı artış yönü \((1,-1)/\sqrt2\), artış hızı \(\sqrt2\).',r'\(x=y\) doğrusu üzerinde fonksiyon gerçekten 1 dir. Bu örnekte sıfır türev sabit seviye doğrultusuna karşılık gelir; her fonksiyonda böyle küresel bir sonuç çıkarılmaz.']))

SOURCES=[
 dict(title='Birincil ders malzemesi',detail='Kullanıcının sağladığı 156 JPG ders/defter fotoğrafı ve mufredat.png. Dosya tarihleri ders tarihi olarak varsayılmadı. Konu-fotoğraf eşleştirmesi fotoğraf dizinindedir.',url=''),
 dict(title='Erwin Kreyszig · Advanced Engineering Mathematics',detail='Dersin belirtilen kitabı. Wiley 10. baskı bölüm diziniyle vektör diferansiyel hesabı başlığı eşleştirildi; tam kitap dosyası sağlanmadı. Kitaptan birebir metin veya soru aktarımı yapılmadı.',url='https://bcs.wiley.com/he-bcs/Books?action=contents&bcsId=6140&itemId=0470458364'),
 dict(title='KOCW · Kreyszig temelli Bölüm 9 ders notları',detail='Sungkyunkwan / Kim Munhyeon, vektörler ve vektör fonksiyonları. Açık üniversite notu kavram ve formül kontrolünde kullanıldı. Buradaki Türkçe açıklamalar ve çözümler özgün olarak yazıldı.',url='https://contents.kocw.net/KOCW/document/2015/sungkyunkwan/kimmunhyeon3/8.pdf'),
 dict(title='Zill ve Wright · Calculus / Matematik',detail='Kullanıcının verdiği bibliyografya: İ. N. Cangül çevirisi, Nobel, 2013. Tam metne erişilmedi; baskıya özgü sayfa ve soru numarası atfedilmedi.',url=''),
 dict(title='Mustafa Balcı · Genel Matematik II',detail='Kullanıcının verdiği bibliyografya: Sürat, 2013. Tam metin sağlanmadı; bu kitaptan doğrulanmış alıntı veya sayfa atfı yapılmadı.',url=''),
 dict(title='MIT OCW · 18.02 ders notları',detail='Denis Auroux, 2007. Ders düzeni ve kavram denetimi için açık ders dizini. Müfredat dışındaki çok katlı integraller ve integral teoremleri bu çalışmaya eklenmedi.',url='https://ocw.mit.edu/courses/18-02-multivariable-calculus-fall-2007/pages/lecture-notes/'),
 dict(title='MIT · Teğet düzlem ve gradyan',detail='Gradyanın teğet düzlem ve yönlü türevle ilişkisi için açık teknik kontrol kaynağı. Konuya eklenen örnekler özgün pekiştirme sorularıdır.',url='https://www.ocw.mit.edu/ans7870/18/18.013a/textbook/HTML/chapter06/section05.html'),
]

# Ek yakın okumalardan gelen ders örnekleri de aynı konu ve soru bankasına girer.
sec(TOPICS[1],'Fotoğraflardan ek analitik geometri çözümleri',
ex('Doğruya dik düzlem',r'P=(2,3,5) noktasından geçen, \((x-1)/4=(y-2)/(-1)=(z+1)/6\) doğrusuna dik düzlemi bulunuz.',[
r'Doğrunun yönü \((4,-1,6)\), istenen düzlemin normalidir. \(4(x-2)-(y-3)+6(z-5)=0\).',r'Denklem \(4x-y+6z-35=0\). P yi yerine koyunca sıfır, doğru yönüyle normalin paralelliği ise dikliği doğrular.'],'IMG-20261002-WA0024.jpg'),
ex('Aynı yöntemin ikinci örneği',r'A=(2,3,-5) noktasından geçen, normali (7,3,4) olan düzlemi yazınız.',[
r'\(7(x-2)+3(y-3)+4(z+5)=0\).',r'Sonuç \(7x+3y+4z-3=0\). Üçüncü koordinat -5 olduğu için parantezde z+5 gelir.'],'IMG-20261002-WA0020.jpg'),
ex('Tahtadaki ikinci kesişim örneği',r'\((x-1)/2=(y-1)/(-1)=z/3\) doğrusu ile \(2x+3y+z+11=0\) düzleminin kesişimi nedir?',[
r'\(x=1+2t,y=1-t,z=3t\). Yerine koyunca \(2+4t+3-3t+3t+11=0\), yani \(4t+16=0\).',r't=-4, kesişim \((-7,5,-12)\). Kontrol \(-14+15-12+11=0\).'],'IMG-20261002-WA0026.jpg'),
ex('İki düzlemin arakesiti: tahta örneği',r'\(x+y+z=3\) ve \(x-y+z=1\) düzlemlerinin arakesitini bulunuz.',[
r'Çıkarınca y=1. z=0 seçilirse x=2; nokta (2,1,0). Normal çarpımı (2,0,-2), eşdeğer yön (1,0,-1).',r'Doğru \((x,y,z)=(2,1,0)+t(1,0,-1)\). Her iki düzlem denklemine de tüm t ler için uyar.'],'IMG-20261002-WA0026.jpg'),
ex('Defterdeki ikinci küre',r'\(x^2+y^2+z^2-2x-4y-6z-2=0\) küresinin merkezi ve yarıçapını bulunuz.',[
r'\((x-1)^2+(y-2)^2+(z-3)^2=16\).',r'Merkez (1,2,3), yarıçap 4. Tam kareler açıldığında sabit 14, sağdan taşınan 16 ile -2 elde edilmesi kontrol sağlar.'],'IMG-20261009-WA0028.jpg'))
sec(TOPICS[2],'Fotoğraflardan ek eğri ve türev çözümleri',
ex('Parametrik eğrinin türü',r'\(\mathbf r(t)=(2+3t,4+5t,6+4t)\) eğrisinin türünü bulunuz.',[
r'\(\mathbf r(t)=(2,4,6)+t(3,5,4)\); sabit doğrultuda bir doğrudur.',r'Simetrik biçim \((x-2)/3=(y-4)/5=(z-6)/4\).'],'IMG-20261009-WA0021.jpg'),
ex('Kapalı eğri ve uç teğetler',r'\(\mathbf r(t)=(t^2-4,t^3-4t,0)\), \(-2\le t\le2\). Basit ve kapalı mıdır?',[
r'Her iki uç (0,0,0) olur. Farklı t ve s için eşit ilk koordinatlar s=-t gerektirir; ikinci koordinat eşitliği \(2t(t^2-4)=0\) verir.',r'Farklı parametrelerle tek tekrar uçlarda t=2 ve s=-2 dir; t=0 kendi kendine aynı parametredir. Dolayısıyla basit kapalı eğridir.',r'\(\mathbf r\prime=(-4,8,0)\) ve (4,8,0) uçlarda paralel değildir; kapama noktasında köşe vardır. Verilen parametrizasyon parçalı düzgün kapalı eğri olarak ele alınır.'],'IMG-20261009-WA0025.jpg'),
ex('Türev ve ikinci türevin noktadaki değeri',r'\(\mathbf r(t)=(1-\cos t,\sin t,t)\) için \(t=\pi/2\) anındaki ilk iki türevi bulunuz.',[
r'\(\mathbf r\prime=(\sin t,\cos t,1)\), \(\mathbf r\prime\prime=(\cos t,-\sin t,0)\).',r'Noktadaki değerler (1,0,1) ve (0,-1,0). Teğet noktası \((1,1,\pi/2)\), teğet doğrusu bu noktadan (1,0,1) yönünde geçer.'],'IMG-20261009-WA0024.jpg'),
ex('Vektörel çarpımın türevini iki yoldan almak',r'\(\mathbf U=(t,-t,t^2/2)\), \(\mathbf V=(t^4/4,t^3/3,t^2/2)\). Çarpımın türevini bulunuz.',[
r'Önce çarpım: \(\mathbf U\times\mathbf V=(-t^3/2-t^5/6,t^6/8-t^3/2,t^4/3+t^5/4)\).',r'Türev \((-3t^2/2-5t^4/6,3t^5/4-3t^2/2,4t^3/3+5t^4/4)\).',r'Alternatif \(\mathbf U\prime\times\mathbf V+\mathbf U\times\mathbf V\prime\) aynı sonucu verir. Orta bileşenin t altıncı kuvvetinin türevi \(6t^5/8=3t^5/4\); defterdeki bu satır sadeleştirilerek kontrol edildi.'],'IMG-20261009-WA0024.jpg'),
ex('Sabit normun türevi',r'\(\mathbf r(t)=(a\cos t,a\sin t,0)\), a>0, için hızın konuma dik olduğunu kanıtlayınız.',[
r'\(\mathbf r\prime=(-a\sin t,a\cos t,0)\); konumla çarpım \(-a^2\sin t\cos t+a^2\sin t\cos t=0\).',r'Genel gerekçe: \(\mathbf r\cdot\mathbf r=a^2\) sabit olduğundan türevi \(2\mathbf r\cdot\mathbf r\prime=0\).'],'IMG-20261015-WA0036.jpg'))

# Son strateji bölümleri ek soru bloklarından sonra okunur.
for _idx in [1,2]:
    _t=TOPICS[_idx]
    _t['sections'].insert(-1,_t['sections'].pop())
