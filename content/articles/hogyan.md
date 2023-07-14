---
title: "Hogyan írj cikket a Szigma oldalán?"
date: 2023-05-28T16:41:02+02:00
draft: false 
authors: ["Zoller András"]
heading: "újságírás"
summary: "A Szigma oldalára egy nagyon népszerű leírónyelvvel lehet a cikkeket készíteni, amelyet Markdownnak hívnak. Ebben a cikkben küröljárjuk, hogy pontosan hogyan kell csinálni"
cover: "https://cdn.pixabay.com/photo/2020/02/08/09/52/chalk-4829602_1280.jpg"
images: ["https://cdn.pixabay.com/photo/2020/02/08/09/52/chalk-4829602_1280.jpg"]
katex: true 
---

# Mi az a Markdown?
> A Markdown egy széles körben elterjedt egyszerű jelölőnyelv formázott szövegek létrehozásához. A Markdownt John Gruber és Aaron Schwartz alkotta meg 2004-ben, céljuk egy olyan jelölőnyelv létrehozása volt, mely forráskód formájában is kényelmesen olvasható.

{{<cite>}} Wikipépia {{</cite>}}

# Markdown Cheat Sheet

# # Heading 1
## ## Heading 2
### ### Heading 3

--- 

*\*Italic text\**
\*\***Bold text**\*\*

--- 

## Lists

### Unordered List:
```
- Item 1
- Item 2
- Item 3
```
- Item 1
- Item 2
- Item 3

### Ordered List:
```
1. Item 1
2. Item 2
3. Item 3
```

1. Item 1
2. Item 2
3. Item 3

---

## Links

```
[Link text](https://www.example.com)
```

[Link text](https://www.example.com)

---

## Images

&#123;&#123;\<image src="image.png"\>&#125;&#125;


---

## Blockquotes

```
> This is a blockquote.
```

> This is a blockquote.


---

## Code

Inline code: \`code\`

Code block:
\`\`\`
function sayHello() {
  console.log("Hello, world!");
}
\`\`\`
```
function sayHello() {
  console.log("Hello, world!");
}
```


---

## Tables

```
| Column 1 | Column 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```
| Column 1 | Column 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |


---

## Horizontal Rule

```
---
```
---

## Escaping Characters

To escape special characters, use a backslash (\\).