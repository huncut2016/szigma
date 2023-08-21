---
title: "Az Apollo-program gyöngye, avagy a Cordic algoritmus"
date: 2023-08-21T11:54:31+02:00
draft: false 
authors: ["Zoller András", "Máté Lőrinc"]
heading: "Matematika"
summary: "A CORDIC (Coordinate Rotation Digital Computer) algoritmus egy iteratív számítási módszer, melyet gyakran trigonometriai műveletekhez használnak digitális eszközökben. Az algoritmus forgatások és transzlációk segítségével közelíti a trigonometriai függvényeket, és egyszerű bitműveletekkel hatékonyan implementálható."
cover: "images/cordic-cover.png"
images: ["images/cordic-cover.png"]
katex: true 
---

# Nagy vonalakban 

A CORDIC (Coordinate Rotation Digital Computer) algoritmus egy iteratív numerikus eljárás, amelyet gyakran használnak trigonometriai és más matematikai műveletek számítására digitális számítógépekben és beágyazott rendszerekben. Az algoritmus célja, hogy forgatások és transzlációk segítségével átalakítsa a bemeneti értékeket olyan értékekké, amelyeknek a trigonometriai függvényei (például szinusz és koszinusz) könnyen számíthatók.

A CORDIC algoritmus előnye, hogy csak egyszerű bitműveleteket és összeadásokat használ, így gyors és hatékony implementációt tesz lehetővé hardveres és szoftveres környezetben egyaránt. Az algoritmust széles körben alkalmazzák digitális jelfeldolgozásban, navigációs rendszerekben és egyéb alkalmazásokban, ahol gyors és pontos trigonometriai számításokra van szükség.

# Hogyan is működik?

![cordic algoritmus képe](images/CORDIC1.png)
Vegyük a 2 dimenziós forgatásmátrixot $R^{\alpha} =  \begin{bmatrix}\cos(\alpha) & -\sin(\alpha) \\\\ \sin(\alpha) & \cos(\alpha) \end{bmatrix}$

Kell találni egy módszert, amely teljesíti ezeket a feltételeket: $v_{n+1} = v_{n}R^{\alpha_{n}}$ és $\displaystyle\lim_{ n \to \infty }v_{n} = v'$

Mivel a számítógépek nagyon jók abban, hogy összeadjanak-kivonjanak, és osszanak-szorozzanak kettővel (binárisban el kell tolni a számot egyel jobbra, vagy balra), ezért az algoritmust erre kell optimalizálni. Ezek az kis nüanszok akkor igazán fontosak, ha például a CPU, ami futtatja az programunkat nem támogatja a lebegőpontos számokat.

Kövessünk el egy cselt és $R^{\alpha}$-ból emeljünk ki $\cos(\alpha)$-t $\implies$ $\cos(\alpha)\begin{bmatrix} 1 & -\tan(\alpha) \\\\ \tan(\alpha) & 1 \end{bmatrix}$

Egyelőre ne foglalkozzunk a $\cos \alpha$ szorzóval, hanem figyeljük meg, hogy mi lenne, ha $\tan \alpha$ pont valami $2$ negatív hatvány lenne 

$$
\begin{align}
\begin{bmatrix}
1 & - 2^{-n} \\\\
2^{-n} & 1 \\\\
\end{bmatrix}
\begin{bmatrix}
x_{i} \\\\
y_{i} \\\\
\end{bmatrix}=
\begin{bmatrix}
x_{i} - 2^{-n}y_{i} \\\\
 2^{-n} x_{i} + y_{i}
\end{bmatrix} 
\end{align}
$$

Csak $2$-vel való osztás és összeadás-kivonás, pont amire gyúrtunk.
Ezzel a hirtelen fellendüléssel alkossunk meg egy algoritmust majd bizonyítsuk be, hogy működik is.

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
Összefoglalva annyit csinál az algoritmus, hogy addig forgatja $v$-t, amíg $\alpha$ túl nem megy a megadott szögön, ha ez bekövetkezik, akkor visszaforgatja (nyilván mindig $\arctan(2^{-n})$ szöggel)

## Bizonyítás

Általánosan feltételezzünk egy sorozatot $(a_{n})_{n\in\mathbb{N}}$

Vegyünk egy pontot $d$-t és valamilyen algoritmus szerint adjuk össze/vonjuk ki a sorozat tagjait úgy, hogy $d$-hez konvergáljon. Formálisan: $\sum \sigma_{n}a_{n} \to d \quad \sigma \in \\{1, -1\\}$ 

Feltételezzük ezeket:

1. ${\color{orange}a_{n} \to 0}$ 

1. ${\color{orange}a_{n} > a_{n+1}}$ or ${\color{orange}a_{n} < a_{n+1}}$

1. $\sum a_{n} \geq |d|$ , ha ez nem lenne igaz, akkor soha nem tudnánk elérni $d$-t

**Evidens kitétel**:  Ha valami $a_{i}$ túllő $d$-n valami $\epsilon$ hibával, akkor legalább kell még $\epsilon$ hogy visszatérjünk 

![cordic algoritmus képe](images/CORDIC2.png)

Ezért, $\displaystyle \epsilon \leq \sum_{k=i+1}a_{k}$ és a legrosszabb esetben:

4. $\displaystyle {\color{orange}a_i \leq \sum_{k=i+1}a_{k}}$

Az algoritmus futása közben gyüjtsük össze azoknak az $a$-knak az összegét egy sorozatba, amelyek két $\sigma$ előjelváltása között helyezkednek el. Nevezzük ezt a sorozatot $T_{n}$-nek

$$
\begin{array}{|c|c|c|c|}
\hline
{\color{orange}\mathbf{T_n}}   & {\color{orange}\mathbf{\sum a}}                                              & {\color{orange}\mathbf{i}} &{\color{orange}\mathbf{\sigma_i}}  \\\\
\hline
T_1   & \sum_{k=0}^{i_{1}}a_{k}                  & i_{1} & 1          \\\\
\hline
T_2   & \sum_{k=i_{1}+1}^{i_{2}}a_{k} & i_{2} & -1          \\\\
\hline
\vdots & \vdots                                         & \vdots    \\\\
\hline
\end{array}
$$

**I. Szcenárió**: Ha $\exist \max{\color{orange}n}$ ($\sigma_{i}$ véges alkalomkor vált előjelet),  az azt jelenti, hogy az algoritmus elért egy olyan pontot, ahol $\epsilon_{i} = \sum_{k=i+1}a_{k}$ ami azt jelenti, hogy az összeg konvergál $d$-hez

**II. Szcenárió**: $\sum_{n=0}(-1)^nT_{k}$ 
![cordic algoritmus képe](images/CORDIC3.png)

$\epsilon_{1} = |c+p-d| \quad \epsilon_{2}=|d-p|$


$d \in \delta=[\epsilon_{1}; \epsilon_{2}] \quad \quad p>0$

$|\delta| = \epsilon_{1}+\epsilon_{2} = c \to 0 \implies \text{converges}$

#### Ebben a specifikus eseztben 

$a_{n} = \tan^{-1}(2^{-n})$
1. $a_{n} \to 0 \quad (2^{-n} \to 0 \text{  és } \tan ^{-1}(0) = 0)$
2. $a_{n} < a_{n+1}$
3. $d\in[-90^{\circ};90^{\circ}]$ és $\sum a_{n} \approx 99.882$
4. $a_{n} \leq \sum_{i=n+1}a_{n}$

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

Hozzuk létre $\frac{b_{n}}{2} = b_{n+1}$ és $b_{0} = a_{n}$

$b_{k} < a_{n+k} \quad k>0 \implies \sum_{k>0}b_{k} < \sum_{k>0}a_{n+k}$

$b_{0} = \sum_{k>0}b_{k} = {\color{green}a_{n} < \sum_{k>0}a_{n+k}}$ 

És beláttuk, hogy az algoritmus működni fog, nyilván olyan könnyítéseket vettünk, minthogy $d \in [-90^{\circ}; 90^{\circ}]$, de mindenki tudja, hogy egy tükrözéssel ezt kit tudjuk terjeszteni.

## Arassuk le a babérokat

### Probléma 
A mátrix, amivel mindig forgatunk $\cos(\arctan(\sigma_n2^{-n}))\begin{bmatrix} 1 & -\sigma_n2^{-n} \\\\ \sigma_n2^{-n} & 1 \end{bmatrix}$, de mondhatnánk, hogy mit érünk azzal, hogy bonyolult $\arctan(\cos(2^{-n}))$ értékeket kell számolnunk és szorozgatnunk. Amit öröm, az holnap bánat. Gyorsan tudunk mátrixot vektorral szorozni, de a korrigáló $\cos$ értéket drága megmondani.

### A földön lelt Deák

Aki jártasabb trigonometriából, az tudja, hogy $\cos\alpha = \cos-\alpha$, ezért $\sigma_n$-et el is hagyhatjuk $\cos(\arctan(2^{-n}))\begin{bmatrix} 1 & -\sigma_n2^{-n} \\\\ \sigma_n2^{-n} & 1 \end{bmatrix}$. Aki még jártasabb, az néhány átalakítással kihozhatja, hogy $\cos(\arctan(2^{-n})) = \frac{1}{\sqrt{ 1+2^{-2n} }}$ és ha jobban megnézzük, akkor az az algoritmust így is felírhatjuk:
$\displaystyle 
\begin{bmatrix}
    x_{i+1}\\\\ 
    y_{i+1}
\end{bmatrix}= K_{i}
\begin{bmatrix}
1 &-\sigma_{i}2^{-i}\\\\
\sigma_{i}2^{-i} &1
\end{bmatrix}
\begin{bmatrix}
x_{i} \\\\
 y_{i}
\end{bmatrix}$

$\displaystyle K_{i}={\frac{1}{\sqrt{1+2^{-2i}}}}$

$\displaystyle K(n)=\prod_{i=0}^{n-1}K_{i}=\prod_{i=0}^{n-1}{\frac {1}{\sqrt {1+2^{-2i}}}}$

$\displaystyle K=\lim _{n\to \infty }K(n)\approx 0.6072529350088812561694$

Meg is találtuk az aranytojást, elég egy konstanst kiszámítani, majd a végén megszorozni vele a vektorunkat. Az $\arctan(2^{-n})$ értékeket meg szintén előre ki tudjuk számítani, soha nem változnak. (amennyiben nem lenne elég, nagyon kicsi szögekre $\arctan x \approx x$) 

## Végső algoritmus

```cpp
#include <cmath>
#include <iostream>
#include <math.h>

constexpr float atans[41] = {45.0,
                             26.56505117707799,
                             14.036243467926479,
                             ...
                             1.0422041580219652e-10,
                             5.211020790109826e-11};

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

    float factor = sigma * ldexp(1, i);
    xp = x - y * factor;
    yp = y + x * factor;

    x = xp;
    y = yp;

    alpha += sign * atans[i];

    ++i;
    epsilon = abs(alpha - angle);
  }

  return y * K;
}
```

