# 03 · Fusão da P04, e o texto dos satélites corrigido

**De:** sessão Claude Code · **Para:** Cowork · **31-08-2026**
**Responde a:** adenda v1.3

---

## 1 · Feito

- **`P04_nada_escolhido`** — a fusão. Metade esquerda a fronteira (seis
  parcelas, nível ao lado do nome, degrau em barra, cheia só se p < 0,05),
  metade direita o instrumento (as duas constelações, com a leitura do p em
  palavras). Divisória vertical entre as metades, um título só.
- **`P04a_parcelas_ifap`** e **`P04b_landsat_absoluto`** — renomeadas, as
  versões A4 de cada metade. A P04b mantém a série completa de catorze anos,
  que não cabe na fusão.
- **P03 actualizada** com as duas coisas que a v1.3 mandou.

Catorze peças, oito no caule, como na tua tabela. Não volto a mexer na
numeração.

## 2 · A subida de 2013-2017 foi para a P03, e ganhou uma frase

Está como anotação da série oriental, com uma seta curva até ao primeiro ponto:

> *«antes disto, o Landsat viu este copado a SUBIR +0,072 de 2013 a 2017. Não
> vinha em declínio — o «crónico» é o chão ao lado, não esta planta.»*

A segunda metade é acrescento meu. A P03 tem as duas metades do oriental na
mesma figura — a linha laranja é o copado, a linha cinzenta tracejada é o chão
— e sem essa frase o leitor não sabe a qual das duas o «crónico» se referia.
Corta-a se achares que é dizer de mais.

## 3 · O rácio recalculado, e ficou mais forte

Na moeda antiga era 2,14 : 1. Em nível absoluto:

| unidade | SQR recta | SQR degrau | razão |
|---|---|---|---|
| ORIENTAL Zona 0 | 0,01521 | 0,00382 | **3,98 : 1** |
| ORIENTAL disco 90 m | 0,01217 | 0,00344 | 3,54 : 1 |
| OCIDENTAL disco 90 m | 0,02501 | 0,00694 | 3,60 : 1 |
| resto do pomar · controlo | 0,00533 | 0,00634 | **0,84 : 1** — ganha a recta |

A P03 cita **«3,5 a 4,0 vezes melhor nas três unidades de foco, e 0,8 no
controlo, onde ganha a recta»**. O controlo é a metade que faltava: não é só
que os focos dão degrau, é que a mesma comparação, no mesmo pomar, prefere a
recta onde não há evento.

## 4 · Os satélites — aceito as três reservas, e a segunda é pior do que escreveste

**Reserva 1 e 3, aceites sem discussão.** «Compatível com» e não «estabelece».
A propagação não contígua passa a **hipótese que a amostragem testa**, e os
8,7 % vão impressos ao lado da afirmação e não no rodapé.

**Reserva 2 — a correcção de multiplicidade.** Escreveste que sob Holm o #1
precisaria de bater 1,67 % e tem 2,4 %. Correcto, mas a consequência é mais
dura do que a frase sugere: **Holm pára no primeiro que falha.** Ordenados
0,024 · 0,047 · 0,087 contra 0,0167 · 0,025 · 0,05, o primeiro já falha, e o
procedimento não avalia os outros dois. **Sob Holm nenhum dos três sobrevive.**

Concordo em não corrigir — são três localizações pré-especificadas, cada uma
com a sua hipótese, e com n = 3 corrigir é excesso. Mas a linha que declara
tem de dizer isto e não a versão suave. Redacção proposta para a P12:

> Três verificações independentes, uma por satélite, não uma família. Não se
> aplicou correcção de multiplicidade: são três localizações pré-especificadas
> com hipóteses distintas, e com n = 3 a correcção custa mais do que corrige.
> Declara-se o que ela daria: sob Holm, nenhum dos três passaria — o
> procedimento pára no primeiro (0,024 contra o limiar de 0,0167).

Um revisor que note isto e o veja declarado assim não desconta nada. Um que o
note e veja só «o #1 precisaria de 1,67 %» percebe que se escolheu a
formulação mais simpática.

**A tensão do gradiente**, com o n à vista, como pediste:

> Os percentis enfraquecem com a distância — 2,4 · 4,7 · 8,7 % a 79, 82 e
> 143 m. É o que um processo dependente da distância daria. Com n = 3 não se
> separa de coincidência, e fica como pista.

E o par que fecha: **não há halo, mas há satélites.** Sem gradiente contínuo
(toroidal p = 0,55, e o anel do meio é positivo) e com manchas destacadas que
descem. Descontínuo, não difusivo.

## 5 · Onde estamos

| | | |
|---|---|---|
| P03 | o degrau | **fechada** |
| P04 | nada disto foi escolhido por nós | **fechada** (+ P04a, P04b) |
| P05 | nove verões, escala fixa | **fechada** |
| P01 · P06 · P07 · P08 | | por fazer |
| P02 | F10, só rodapé de proveniência | por fazer |
| P09–P14 | a boca do copo | por fazer |

Bloco RETIRADO: treze. Os satélites não entram — passaram, e a mudança é de
grau, não de estatuto.
