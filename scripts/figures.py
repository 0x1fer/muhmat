from pathlib import Path
import subprocess
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'assets/figures';OUT.mkdir(parents=True,exist_ok=True)
HEAD=r'''\documentclass[tikz,border=8pt]{standalone}
\usepackage{amsmath}\usepackage{pgfplots}\pgfplotsset{compat=1.18}\usetikzlibrary{arrows.meta}
\definecolor{ink}{HTML}{334155}\definecolor{blue}{HTML}{6366F1}\definecolor{green}{HTML}{059669}\definecolor{orange}{HTML}{EA580C}
\begin{document}
'''
figs={
'projection':r'''\begin{tikzpicture}[>=Stealth,scale=1.1]
\draw[->,ink] (-.3,0)--(5.3,0) node[right]{$x$};\draw[->,ink](0,-.3)--(0,3.5)node[above]{$y$};
\draw[very thick,->,blue](0,0)--(4,2.7)node[above]{$\mathbf u$};
\draw[very thick,->,green](0,0)--(4,0)node[below,midway]{$\operatorname{proj}_{\mathbf v}\mathbf u$};
\draw[thick,dashed,orange,->](4,0)--(4,2.7)node[right,midway]{$\mathbf u_\perp$};
\draw[ink](3.75,0)--(3.75,.25)--(4,.25);\node[below right]at(5,0){$\mathbf v$};
\end{tikzpicture}''',
'quadrics':r'''\begin{tikzpicture}
\begin{axis}[width=7cm,height=6cm,view={35}{25},axis lines=center,xlabel=$x$,ylabel=$y$,zlabel=$z$,ticks=none,title={$z=x^2+y^2$}]
\addplot3[surf,shader=interp,domain=-1:1,y domain=-1:1,samples=17,colormap/viridis]{x^2+y^2};\end{axis}
\begin{axis}[at={(7.5cm,0)},anchor=south west,width=7cm,height=6cm,view={35}{25},axis lines=center,xlabel=$x$,ylabel=$y$,zlabel=$z$,ticks=none,title={$z=x^2-y^2$}]
\addplot3[surf,shader=interp,domain=-1:1,y domain=-1:1,samples=17,colormap/viridis]{x^2-y^2};\end{axis}\end{tikzpicture}''',
'helix':r'''\begin{tikzpicture}\begin{axis}[width=12cm,height=7cm,view={35}{22},axis lines=center,xlabel=$x$,ylabel=$y$,zlabel=$z$,ticks=none,xmin=-1.5,xmax=2,ymin=-1.5,ymax=2,zmin=0,zmax=5]
\addplot3[very thick,blue,domain=0:720,samples=100,samples y=0]({cos(x)},{sin(x)},{x/160});
\addplot3[thick,->,green]coordinates{(1,0,2.25)(1,1,2.7)} node[pos=1,right]{$\mathbf T$};
\addplot3[thick,->,orange]coordinates{(1,0,2.25)(0,0,2.25)} node[pos=1,above]{$\mathbf N$};
\addplot3[thick,->,ink]coordinates{(1,0,2.25)(1,-.4,3.15)} node[pos=1,right]{$\mathbf B$};
\end{axis}\end{tikzpicture}''',
'levels':r'''\begin{tikzpicture}
\begin{axis}[width=7cm,height=6cm,view={30}{25},axis lines=center,xlabel=$x$,ylabel=$y$,zlabel=$z$,ticks=none,title={$z=x^2+y^2$}]
\addplot3[surf,opacity=.7,shader=interp,domain=-2:2,y domain=-2:2,samples=18,colormap/viridis]{x^2+y^2};\end{axis}
\begin{axis}[at={(7.5cm,0)},anchor=south west,width=7cm,height=6cm,axis equal image,axis lines=middle,xmin=-2.7,xmax=2.7,ymin=-2.7,ymax=2.7,xlabel=$x$,ylabel=$y$,ticks=none,title={Seviye: $x^2+y^2=c$}]
\addplot[blue,thick,domain=0:360,samples=80]({cos(x)},{sin(x)});\addplot[green,thick,domain=0:360,samples=80]({2*cos(x)},{2*sin(x)});
\node[blue]at(axis cs:1.3,.6){$c=1$};\node[green]at(axis cs:2,1.7){$c=4$};\end{axis}\end{tikzpicture}''',
'paths':r'''\begin{tikzpicture}\begin{axis}[width=11cm,height=6cm,axis lines=middle,xmin=-1.6,xmax=1.6,ymin=-1.4,ymax=2,xlabel=$x$,ylabel=$y$,grid=major,legend style={at={(1.03,1)},anchor=north west}]
\addplot[blue,thick,domain=-1.3:1.3]{x};\addlegendentry{$y=x$}
\addplot[green,thick,domain=-1.3:1.3]{x^2};\addlegendentry{$y=x^2$}
\addplot[orange,thick,domain=-1.3:1.3]{0};\addlegendentry{$y=0$}
\addplot[only marks,mark=*,ink]coordinates{(0,0)};\end{axis}\end{tikzpicture}''',
'tangent':r'''\begin{tikzpicture}\begin{axis}[width=12cm,height=7cm,view={35}{25},axis lines=center,xlabel=$x$,ylabel=$y$,zlabel=$z$,ticks=none,xmin=0,xmax=2,ymin=1,ymax=3]
\addplot3[surf,opacity=.6,shader=interp,domain=0:2,y domain=1:3,samples=16,colormap/viridis]{x^2+y^2};
\addplot3[mesh,blue,domain=.2:1.8,y domain=1.2:2.8,samples=8]{2*x+4*y-5};
\addplot3[only marks,mark=*,mark size=2pt,orange]coordinates{(1,2,5)}node[above]{$P$};\end{axis}\end{tikzpicture}''',
'gradient':r'''\begin{tikzpicture}[>=Stealth]\begin{axis}[width=11cm,height=7cm,axis equal image,axis lines=middle,xmin=-2,xmax=2.2,ymin=-1.7,ymax=2,xlabel=$x$,ylabel=$y$,ticks=none]
\addplot[blue,thick,domain=0:360,samples=100]({sqrt(3)*cos(x)},{sqrt(1.5)*sin(x)});
\addplot[green,thick,->]coordinates{(1,1)(1.5,2)}node[right]{$\nabla f=(2,4)$};
\addplot[orange,thick,domain=-.6:1.7]{1.5-.5*x};
\addplot[only marks,mark=*,ink]coordinates{(1,1)}node[below]{$P$};
\node[blue]at(axis cs:-1.2,1.5){$x^2+2y^2=3$};\end{axis}\end{tikzpicture}'''
}
for name,body in figs.items():
 (OUT/f'{name}.tex').write_text(HEAD+body+'\n\\end{document}\n')
 result=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=OUT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if result.returncode: print(result.stdout.decode()[-2500:]);raise SystemExit(name)
 subprocess.run(['pdftocairo','-svg',str(OUT/f'{name}.pdf'),str(OUT/f'{name}.svg')],check=True)
 print(name,'OK',flush=True)
