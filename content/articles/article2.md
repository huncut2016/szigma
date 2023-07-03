---
title: "Sorozatok határértéke"
date: 2023-04-15T12:13:59+01:00
draft: false 
authors: ["Zoller András", "Juhász István", "Répás Mátyás"]
heading: "Matematika"
summary: "Rengetegszer hallunk a sorozatok határértékéről, de soha nem tudjuk, hogy mit is jelnt valjójában. Ebben a cikkben megismerheted, hogy mit is jelent pontosan ez a fogalom."
images: ["http://szigma.szigbp.hu/wp-content/uploads/2018/03/25_11034_79992_f099b686cb0fddd7dd9bfbd5f00e7d17_7ff3fa_301.jpg"]
cover: "http://szigma.szigbp.hu/wp-content/uploads/2018/03/25_11034_79992_f099b686cb0fddd7dd9bfbd5f00e7d17_7ff3fa_301.jpg"
katex: true 
---
# Limit of sequences

## Definition

### Definition 1.

A **limit point of a sequence** $a_{n}$ is a point $\color{orange}L$ such that every neighbourhood of $\color{orange}L$ contains all points of the sequence with numbers above some $n_{0}$.

### Formal definition 
{{<formula>}}
\forall \;\; \epsilon \! > \! 0 \;\; \exists n_0 \text{ s.t. } n \geq n_0 \quad |{\color{orange}L}-a_n| \leq \epsilon
{{</formula>}}

- If for all $\epsilon>0$ exist an $n_{0}$ such that every $n \geq n_{0}$  than $|{\color{orange}L}-a_{n}|\leq \epsilon$, $\color{orange}L$ is the limit of $a_{n}$

- If for all $\epsilon>1$ exist an $n_{0}$ such that every $n \geq n_{0}$  than $|{\color{orange}L}-a_{n}|\leq \epsilon$, $\color{orange}L$ is the limit of $a_{n}$

{{<image src="http://csodafizika.hu/ds/ds.jpg" alt="Ez egy nagyon kellemes kép a káoszról">}}

Nem nagyon tudom, hogy mi lehet ennek az oka 

{{<image src="https://user-images.githubusercontent.com/81006960/142606746-3d6191e3-d8f0-465f-9aef-070dc6c88958.png" alt="Valami random kép Githubról">}}
