---
title: "Az Apollo-program gyöngye, avagy a CORDIC-algoritmus"
date: 2023-08-21T11:54:31+02:00
draft: false 
authors: ["Zoller András", "Máté Lőrinc"]
heading: "Matematika"
summary: "A CORDIC-algoritmus (Coordinate Rotation Digital Computer) egy iteratív számítási módszer, melyet gyakran trigonometriai műveletekhez használnak digitális eszközökben. Az algoritmus forgatások és transzlációk segítségével közelíti a trigonometriai függvényeket, és egyszerű bitműveletekkel hatékonyan implementálható."
cover: "images/cordic-cover.png"
images: ["images/cordic-cover.png"]
katex: true 
---

# Nagy vonalakban 

A CORDIC-algoritmus (Coordinate Rotation Digital Computer) egy iteratív numerikus eljárás, amelyet gyakran használnak trigonometriai és más matematikai műveletek számítására digitális számítógépekben és beágyazott rendszerekben. Az algoritmus célja, hogy forgatások és transzlációk segítségével átalakítsa a bemeneti értékeket olyan értékekké, amelyeknek a trigonometriai függvényei (például szinusz és koszinusz) könnyen számíthatók.

A CORDIC-algoritmus előnye, hogy csak egyszerű bitműveleteket és összeadásokat használ, így gyors és hatékony implementációt tesz lehetővé hardveres és szoftveres környezetben egyaránt. Az algoritmust széles körben alkalmazzák digitális jelfeldolgozásban, navigációs rendszerekben és egyéb alkalmazásokban, ahol gyors és pontos trigonometriai számításokra van szükség.

# Hogyan is működik?

![cordic algoritmus képe](images/CORDIC1.png)
Vegyük a 2 dimenziós forgatásmátrixot: $R^{\alpha} =  \begin{bmatrix}\cos(\alpha) & -\sin(\alpha) \\\\ \sin(\alpha) & \cos(\alpha) \end{bmatrix}$

Kell találni egy módszert, amely teljesíti ezeket a feltételeket: $v_{n+1} = v_{n}R^{\alpha_{n}}$ és $\displaystyle\lim_{ n \to \infty }v_{n} = v'$

Mivel a számítógépek nagyon jók abban, hogy összeadjanak-kivonjanak és osszanak-szorozzanak kettővel (binárisban el kell tolni a számot eggyel jobbra vagy balra), ezért az algoritmust erre kell optimalizálni. Ezek a kis nüanszok akkor igazán fontosak, ha például a CPU, ami futtatja a programunkat, nem támogatja a lebegőpontos számokat.

Vessünk be egy cselt, és $R^{\alpha}$-ból emeljünk ki $\cos(\alpha)$-t $\implies$ $\cos(\alpha)\begin{bmatrix} 1 & -\tan(\alpha) \\\\ \tan(\alpha) & 1 \end{bmatrix}$

Egyelőre ne foglalkozzunk a $\cos \alpha$ szorzóval, hanem figyeljük meg, hogy mi lenne, ha $\tan \alpha$ pont $2$ negatív hatványa lenne (ez azért előnyös feltételezés, mert kettő hatványokkal szorozni-osztani nagyon gyors a számítógépeken):

$$
\begin{align}
\notag
\begin{bmatrix}
1 & - 2^{-n} \\\\
2^{-n} & 1 \\\\
\end{bmatrix}
\begin{bmatrix}
x_{k} \\\\
y_{k} \\\\
\end{bmatrix}=
\begin{bmatrix}
x_{k} - 2^{-n}y_{k} \\\\
 2^{-n} x_{k} + y_{k}
\end{bmatrix} 
\end{align}
$$

Csak $2$-vel való osztás és összeadás-kivonás, pont, amire gyúrtunk.
Ezzel a hirtelen fellendüléssel alkossunk meg egy algoritmust, majd bizonyítsuk be, hogy működik is.

# Az algoritmus

```julia
function cordic(szog::Real)::Real
	αn = 0.0
	v0 = [1.0, 0.0]
	
	for n ∈ 0:∞
		𝞼n = αn > szog ? -1 : 1
        k = 2^-n
		βn = atan(k) * 𝞼n
		
		R = cos(βn)[1 -k;
			        k 1]
		
		v0 = R * v0
		αn = αn + βn
	end
end
```
Összefoglalva annyit csinál az algoritmus, hogy addig forgatja $v$-t, amíg $\alpha$ túl nem megy a megadott szögön. Ha ez bekövetkezik, akkor visszaforgatja (nyilván mindig $\arctan(2^{-n})$ szöggel).

## Bizonyítás

Határozzunk meg egy $a_{n}$ sorozatot. $n\in\mathbb{N}$

Vegyünk egy $d$ pontot, és valamilyen algoritmus szerint adjuk össze/vonjuk ki a sorozat tagjait úgy, hogy $d$-hez konvergáljon. Formálisan: $\sum \sigma_{n}a_{n} \to d \quad \sigma \in \\{-1; 1\\}$ 

Tételezzük fel ezeket:

1. ${\color{orange}a_{n} \to 0}$ 

1. ${\color{orange}\sum a_{n} \geq |d|}$ (ha ez nem lenne igaz, soha nem tudnánk elérni $d$-t)

**Evidens kitétel**:  Ha $a_{m}$ túllő $d$-n valami $\epsilon$ hibával, akkor kell még legalább $\epsilon$, hogy visszatérjünk. 

![cordic algoritmus képe](images/CORDIC2.png)

Ezért $\displaystyle \epsilon \leq \sum_{k=m+1}a_{k}$, és a legrosszabb esetben:

3. $\displaystyle {\color{orange}a_m \leq \sum_{k=m+1}a_{k}}$

Az algoritmus futása közben gyűjtsük össze azoknak az $a$-knak az összegét egy sorozatba, amelyek két $\sigma$ előjelváltása között helyezkednek el (másképpen: minden $T_n$ egy $\sigma$ periódusba tartozó $a$-k összege). Nevezzük ezt a sorozatot $T_{n}$-nek:

$$
\begin{array}{|c|c|c|c|}
\hline
{\color{purple}\mathbf{T_n}}   & {\color{purple}\mathbf{\sum a}}                                              & {\color{purple}\mathbf{m}} &{\color{purple}\mathbf{\sigma_m}}  \\\\
\hline
T_1   & \sum_{k=0}^{m_{1}}a_{k}                  & m_{1} & 1          \\\\
\hline
T_2   & \sum_{k=m_{1}+1}^{m_{2}}a_{k} & m_{2} & -1          \\\\
\hline
\vdots & \vdots                                         & \vdots    \\\\
\hline
\end{array}
$$

**I. eset**: Ha $\exist \max n$ ($\sigma_{m}$ véges alkalomkor vált előjelet), az azt jelenti, hogy az algoritmus elért egy olyan pontot, ahol $\epsilon_{m} = \sum_{k=m+1}a_{k}$, vagyis az összeg konvergál $d$-hez.

**II. eset**: $\sum_{n=0}(-1)^nT_{n}$ 
![cordic algoritmus képe](images/CORDIC3.png)

$\epsilon_{1} = |c+p-d| \quad \epsilon_{2}=|d-p|$


$d \in \delta=[\epsilon_{1}; \epsilon_{2}] \quad \quad p>0$

$|\delta| = \epsilon_{1}+\epsilon_{2} = c \to 0 \implies d\text{-be konvergál}$

#### Ebben a specifikus esetben 

$a_{n} = \tan^{-1}(2^{-n})$
1. $\color{orange}{ a_{n} \to 0} \quad (2^{-n} \to 0 \text{  és } \tan ^{-1}(0) = 0)$
1. $\color{orange} d\in[-\pi/2;\pi/2]$ és $\sum a_{n} \approx 0.5549\pi$
1. $\color{orange} a_{n} \leq \sum_{m=n+1}a_{m}$

$$
\begin{align}
\notag
& \tan ^{-1}(2x) < 2\tan ^{-1}(x)  \\\\
\notag
& \tan ^{-1}(2x) - 2\tan ^{-1}(x)< 0 \\\\
\notag
& f(x) = \tan ^{-1}(2x) - 2\tan ^{-1}(x) \\\\
\notag
& f'(x) =  \frac{-6x^{2}}{4x^{4}+5x^{2}+1} < 0 \quad x > 0 \\\\
\notag
& f(0) = \tan ^{-1}(2x) - 2\tan ^{-1}(x) = 0 \\\\
\notag\\\\
\notag
& \color{green}\implies f(x) < 0 \checkmark \quad x > 0
\notag
\end{align}
$$

---

$\tan ^{-1}(2x) < 2\tan ^{-1}(x) \implies \tan ^{-1}(2^{-n+1}) < 2\tan ^{-1}(2^{-n})$

$\tan ^{-1}(2^{-n+1}) = \color{orange}a_{n-1}$

$2\tan ^{-1}(2^{-n}) = \color{orange}2a_{n}$

---

$a_{n-1} < 2a_{n} \implies \frac{a_{n}}{2} < a_{n+1}$

Hozzuk létre a $b_{n}$ sorozatot, $b_{0} := a_{n}$ és $b_{n+1} = \frac{b_{n}}{2}$

$b_{k} < a_{n+k} \quad k>0 \implies \sum_{k>0}b_{k} < \sum_{k>0}a_{n+k}$

$b_{0} = \sum_{k>0}b_{k} = {\color{green}a_{n} < \sum_{k>0}a_{n+k}}$ 

És beláttuk, hogy az algoritmus működni fog. Nyilván olyan könnyítéseket vettünk, mint $d \in [-90^{\circ}; 90^{\circ}]$, de mindenki tudja, hogy ezt egy tükrözéssel ki tudjuk terjeszteni.

## Arassuk le a babérokat

### Probléma 
A mátrix, amivel mindig forgatunk, $\cos(\arctan(\sigma_n2^{-n}))\begin{bmatrix} 1 & -\sigma_n2^{-n} \\\\ \sigma_n2^{-n} & 1 \end{bmatrix}$, de mondhatnánk, hogy mit érünk azzal, hogy bonyolult $\arctan(\cos(2^{-n}))$ értékeket kell számolnunk és szorozgatnunk. 
Amit az egyik oldalon nyertünk, azt a másikon elveszítettük. Bár gyorsan tudunk mátrixot vektorral szorozni, de a korrigáló $\cos$ értéket kiszámolni nagyon erőforrás-igényes lett.

### Az út mellett talált érme 

Aki jártasabb trigonometriában, az tudja, hogy $\cos\alpha = \cos-\alpha$, ezért $\sigma_n$-et el is hagyhatjuk: $\cos(\arctan(2^{-n}))\begin{bmatrix} 1 & -\sigma_n2^{-n} \\\\ \sigma_n2^{-n} & 1 \end{bmatrix}$. Aki még jártasabb, az néhány átalakítással kihozhatja, hogy $\cos(\arctan(2^{-n})) = \frac{1}{\sqrt{ 1+2^{-2n} }}$, és ha jobban megnézzük, akkor az algoritmust így is felírhatjuk:
$\displaystyle 
\begin{bmatrix}
    x_{k+1}\\\\ 
    y_{k+1}
\end{bmatrix}= K_{k}
\begin{bmatrix}
1 &-\sigma_{k}2^{-k}\\\\
\sigma_{k}2^{-k} &1
\end{bmatrix}
\begin{bmatrix}
x_{k} \\\\
 y_{k}
\end{bmatrix}$

$\displaystyle K_{i}={\frac{1}{\sqrt{1+2^{-2i}}}}$

$\displaystyle K(n)=\prod_{i=0}^{n-1}K_{i}=\prod_{i=0}^{n-1}{\frac {1}{\sqrt {1+2^{-2i}}}}$

$\displaystyle K=\lim _{n\to \infty }K(n)\approx 0.6072529350088812561694$

Meg is találtuk az aranytojást: elég egy konstanst kiszámítani, majd a végén megszorozni vele a vektorunkat. Az $\arctan(2^{-n})$ értékeket meg szintén ki tudjuk előre számítani, soha nem változnak. (Amennyiben ez nem lenne elég, nagyon kicsi szögekre $\arctan x \approx x$.) 

## Végső algoritmus

```cpp
#include <cmath>
#include <iostream>
#include <math.h>

constexpr int num_atans = 41;
constexpr float atans[num_atans] = {0.7853981633974483,
                                    0.4636476090008061,
                                    0.24497866312686414,
                                    0.12435499454676144,
                                    0.06241880999595735,
                                    ...
                                    3.637978807091713e-12,
                                    1.8189894035458565e-12,
                                    9.094947017729282e-13};

float cordic_sin(float angle) {
  float epsilon = 0,

        x = 1, y = 0,
        xp = 1, yp = 0, 

        alpha = 0,
        err = 1e-3,
        K = 0.60725293500888120;

  int i = 0;

  while (epsilon > err) {
    float sigma = alpha > angle ? -1 : 1;

    float powerOfTwo = ldexp(1, -i); // ldexp(num, exp) = num*(2^exp)
    float factor = sigma * powerOfTwo;

    // == Mátrix szorzás ==
    xp = x - y * factor;
    yp = y + x * factor;

    x = xp;
    y = yp;

    // == Alfa frissítése ==
    float atan = i < num_atans ? atans[i] : poweroftwo; // arctan(x) ≈ x ha x kicsi
    alpha += sigma* atan;

    ++i;
    epsilon = abs(alpha - angle);
  }

  return y * K;
}
```
{{<cite>}}
C++ algoritmus
{{</cite>}}
