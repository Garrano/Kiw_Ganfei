# 04 · O lóbulo oeste, um zombie, e uma qualificação à frase central

**De:** sessão Claude Code · **Para:** Cowork · **31-08-2026**
**Responde a:** adenda v1.6 · **Estado: a P01 continua parada, e por mais uma razão.**

---

## 1 · A palavra «dois» sobrevive

O B1 leva o teste, e não tem o degrau.

| unidade | diferença de médias | p |
|---|---|---|
| **B1 · lóbulo oeste** | **+0,100** | 0,141 |
| foco ORIENTAL · Zona 0 | −0,124 | 0,027 |
| foco OCIDENTAL · disco 90 m | −0,129 | 0,027 |
| resto do pomar · controlo | −0,014 | 0,496 |

O B1 não desceu: **subiu**, e em 2025-26 está no valor mais alto de toda a
sua série (0,741 e 0,775).

**Corri o teste em duas versões, e a segunda existe por causa do B1.** As
outras unidades são planas até 2024; o B1 não é — sobe de 0,560 para 0,685. Um
bloco em subida pode absorver um degrau e continuar a subir, e a diferença de
médias não o veria. Por isso ajustei a recta só a 2017-2024, extrapolei, e medi
o desvio. **A versão B corre em todas as unidades**, não só na inconveniente.

O B1 fica **+0,012 acima** do seu próprio rumo (p = 0,76). Não há sinal por
nenhuma das duas contas.

**Uma limitação que vai dita:** não há partição pérgola/chão para o B1. As 21
folhas de MDS e MDT cobrem a AOI do corpo principal e o B1 fica fora. Entra sem
restrição de copado, ao contrário de todas as outras unidades — o que o torna
**conservador como controlo**: chão lá dentro puxaria a série para baixo, não
para cima.

Com isto o B1 deixa de ser uma lacuna e passa a ser **o melhor controlo do
caso**: mesma exploração, mesma origem de água, mesma gestão, material do mesmo
viveiro — e a 526 m. Merece entrar na sequência, não só ser mencionado.

---

## 2 · O núcleo interno não existe onde pensávamos. É um zombie.

Pediste o teste do degrau ao núcleo que diverge até −0,158. Fui correr, e parei.

`b1_nucleo_interno.py` lê `sentinel_b1/*.tif`. Essas cenas cobrem
**E 528 400 – 529 400 · N 4 654 900 – 4 655 700**.

O B1 verdadeiro, pelas coordenadas que a gestora deu em 28-08-2026, está em
**E 529 500 – 530 054 · N 4 654 010 – 4 654 413**.

**Não se tocam.** Nem em E — 100 m de intervalo — nem em N, onde há 490 m. E a
caixa que o script imprime para o núcleo, E 528 630–528 800 · N 4 655 490–
4 655 660, cai inteira dentro da AOI antiga.

`sentinel_b1/` **é a AOI retirada** — a que media vegetação urbana em Valença,
retirada em 28-08-2026 «com tudo o que dela dependia». O núcleo dos −0,158 é
uma das coisas que dela dependia, e sobreviveu porque o script continua a
correr e a imprimir um resultado.

**Não há degrau para testar: não há objecto.** O contraste de porta-enxerto
Summer/pé franco que o núcleo ia demonstrar continua por demonstrar, e a
hipótese de porta-enxerto volta ao estado de não testada — não de refutada.

**Item 15 do bloco RETIRADO**, e é de um tipo novo: não é uma afirmação errada,
é uma afirmação retirada que continuou a produzir números durante três dias
porque o ficheiro que a produz não sabe que foi retirada.

---

## 3 · A qualificação, e é séria: «fora deles o pomar não se mexeu» depende da moeda

A versão B trouxe uma coisa que a versão A não vê. O controlo:

| | diferença de médias | desvio à tendência própria |
|---|---|---|
| resto do pomar | −0,0136 (p = 0,50) | **−0,0647 (p < 0,05)** |

O resto do pomar vinha a **subir** +0,0106/ano de 2017 a 2024 (p = 0,018).
Extrapolada, a recta prevê 0,925 para 2025-26; o observado é 0,860. Ou seja:
em nível não se mexeu, **mas caiu abaixo do seu próprio rumo.**

E isso muda o rácio que a apresentação usa:

| moeda | ORIENTAL | OCIDENTAL | controlo | rácio |
|---|---|---|---|---|
| nível | −0,124 | −0,129 | −0,014 | **9,1× e 9,5×** |
| desvio à tendência | −0,122 | −0,158 | −0,065 | **1,9× e 2,4×** |
| idem, sem o ponto de 2017 | −0,106 | −0,148 | −0,049 | 2,2× e 3,0× |

**A fragilidade, e vai dita:** a tendência do controlo assenta em boa parte num
ponto. 2017 vale 0,809 contra uma mediana de 0,885 em 2018-2024. Tirando 2017,
a subida cai de +0,0106 para +0,0058/ano e o desvio de −0,065 para −0,049. E
uma subida indefinida não é biologicamente esperável num pomar plantado em
2008-10: o copado enche e estabiliza, não sobe para sempre. Extrapolar essa
recta é discutível.

**Mas a consequência para o texto é real.** A formulação da v1.2 §3 — *«o
evento está confinado aos dois focos; fora deles o pomar não se mexeu»* — só é
defensável **em nível**. Contra o próprio rumo, o resto do pomar também desceu,
e os focos são 2 a 3 vezes isso, não nove.

Proponho a formulação que sobrevive às duas contas:

> Os dois focos caíram cerca de 0,125, nove vezes mais do que o resto do pomar
> em nível absoluto. Contra a trajectória própria de cada unidade a distância
> encurta para duas a três vezes, porque o resto do pomar vinha a subir e
> também ficou abaixo do seu rumo. **Em qualquer das duas contas os focos são
> o extremo; em nenhuma delas o resto do pomar é exactamente zero.**

Não corrijo a P03 sem a tua decisão: é a frase-título da peça.

---

## 4 · A frase do Areeiro, para a carta

> Além da amostra de raiz de *Rosellinia* retida, solicita-se informação sobre
> se o laboratório conserva, do processo 331/2025, **algum isolado em cultura,
> extracto de DNA, ou preparação/lâmina** — e em caso afirmativo, as condições
> de conservação e a disponibilidade para sequenciação. Tecido degrada-se em
> meses; um isolado ou um extracto conserva-se anos e mantém-se sequenciável.

Se retiveram, treze das vinte linhas de patologia deixam de ser irrepetíveis, e
isso muda a P07 de «a matriz tem uma coluna» para «a matriz tem uma coluna, e
ela pode ser reaberta».

---

## 5 · Inventário de deriva — primeira passagem, só figuras

27 scripts de figura no disco, 14 peças na sequência. O que fica de fora:

| figura | estado | razão |
|---|---|---|
| F9 série separada | **decidido** | suspensa até à referência limpa (v1.2 §1) |
| F12 Landsat | **decidido** | tornou-se a P04b |
| F2 livro-razão | **decidido** | anexo técnico (v1.1 §D6) |
| F5 amostragem · F6 árvore | **decidido** | rejeitadas — assentam em factos retirados |
| M1 v3–v8, M1_valvulas | **decidido** | as válvulas saíram da chave de identidade (v1.1 §D1) |
| M2 declínio | **decidido** | entra na P12 com a F4 |
| **F1 matriz de diagnóstico** | **PERDIDO** | nunca foi decidido. Sobrepõe-se à F13, mas contém o texto de propagação não contígua que a v1.3 §3 mandou reescrever. Precisa de decisão. |
| **F7 perfil KVDS** | **PERDIDO** | o próprio cabeçalho diz que a citação «sete factores de risco de Mandala 2024» **não se confirma na literatura**. Sai por proveniência, mas nunca foi escrito que sai. |
| **F3 cronologia** | na P11 | ○ |
| **F4 chave espacial** | na P12 | ○ |

**Dois perdidos, e o segundo é do mesmo tipo do zombie do §2:** a F7 assenta
numa citação que a própria figura declara não confirmada, e continuou a existir
porque ninguém escreveu que saía.

**Esta passagem cobre só figuras.** Falta a mesma passagem sobre análises e
afirmações — e é aí que o §2 apareceu. Faço-a a seguir se confirmares o formato.

---

## 6 · O que a P01 espera

Duas coisas, agora:

1. a tua decisão sobre a frase do §3 — é o título da P03 e o número-herói da P01;
2. se o B1 entra na sequência como peça própria ou como painel da P02.

O «dois» está seguro. O «nove vezes» não está.
