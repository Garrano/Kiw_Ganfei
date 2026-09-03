# P1 e P2 — as duas perguntas em aberto, corridas

**Data:** 31-08-2026. As duas primeiras acções da fila do encerramento.
**Precedência:** medição contra afirmação. Onde isto contrarie a R3, ganha isto.

---

## P1 · Pérgola no foco oriental — o instrumento falha em 2025 e responde em 2021

Método: `c2_12_pergola_2012.py`, **sem uma linha alterada**. Prominência do
primeiro pico secundário da autocorrelação radial da luminância, janela de 40 m,
comparada **dentro de cada imagem**.

### Verificação antes de ler o resultado

| | REF (tem pérgola) | NU21 (chão lavrado) | IQR disjuntos? |
|---|---|---|---|
| **2021** | 0,0449 · IQR 0,029–0,058 | −0,0178 · IQR −0,021 a −0,015 | **sim — discrimina** |
| **2025** | 0,3293 · IQR 0,270–0,368 | **0,2396 · IQR −0,007 a 0,404** | **não — não discrimina** |

E reproduzo o número que a C2 publicou para 2021: **0,0449 contra os 0,045
dela.**

### O que isto significa

**A ortofoto de 2025 não pode responder à pergunta.** As duas âncoras não se
separam: chão lavrado conhecido dá uma distribuição que cobre a da referência
inteira. A causa mais provável está documentada pela própria C0 — a ortofoto de
2025 mostra **«camalhões com cobertura de plástico contínua»**, e plástico em
linha produz periodicidade de ~5 m que não é pérgola. **O instrumento mede
estrutura periódica, e em 2025 há duas estruturas periódicas diferentes.**

**Mas 2021 discrimina, e dá uma resposta que ninguém procurou.**

| unidade (posição entre chão lavrado 0 % e referência 100 %) | 2021 |
|---|---|
| REF · referência sistemática | 100 % |
| RESTO · resto do pomar com pérgola | **80 %** |
| **ORI-COM · foco oriental, a metade que o LiDAR de 2025 diz TER pérgola** | **14 %** |
| **ORI-SEM · foco oriental, a metade sem pérgola** | **6 %** |
| NU21 · chão lavrado | 0 % |

> **Em 2021, o foco oriental não tinha assinatura de pérgola — INCLUINDO a
> metade que o LiDAR de 2025 diz ter.** Enquanto o resto do pomar lia 80 %, as
> duas metades do oriental liam 14 % e 6 %, isto é, indistinguíveis de chão
> lavrado.

### A consequência, e é grande

A estrutura que o LiDAR encontra no oriental em Julho de 2025 **apareceu depois
de 2021**. Tem **quatro anos ou menos**.

Isso não confirma «arranque» nem «declínio» — responde a outra coisa, e a
resposta reenquadra o caso: **o degrau de 2025-26 no foco oriental está a
acontecer sobre copado recente, não sobre pomar adulto em declínio.** Uma
plantação nova falha por razões diferentes de uma adulta.

E fecha, pelo lado que interessa, a objecção do Controlo 3: a partição
`h ≥ 0,5` é pós-tratamento — mas agora sabemos **o que ela está a seleccionar**:
copado instalado entre 2021 e 2025.

**O que continua por decidir:** se aquilo foi arrancado e replantado, ou se
nunca tinha sido plantado antes de 2021. A ortofoto de 2012 e a de 2010 podem
responder — o método discrimina nelas (a C2 usou-as) e **não foram corridas para
esta unidade.** É a acção seguinte, e é barata.

---

## P2 · As onze cenas — **são dois passos, não um**

Descarregadas e medidas as oito cenas de plena estação com nuvem aceitável do
intervalo, mais as duas da série: **dez pontos onde havia dois**.

Mede-se o **contraste foco-menos-controlo**, que é a grandeza certificada — um
desvio de plataforma comum cancela-se.

| data | plataforma | nuvem | contraste OCIDENTAL | contraste ORIENTAL |
|---|---|---|---|---|
| 2025-08-14 | *(série)* | — | −0,0525 | −0,1081 |
| 2025-08-16 | S2a | 0,1 % | −0,0500 | −0,1029 |
| 2025-08-21 | S2c | 11,3 % | −0,0475 | −0,1051 |
| 2025-08-23 | S2a | 0,0 % | −0,0524 | −0,1021 |
| 2025-08-24 | S2c | 12,8 % | −0,0482 | −0,0930 |
| 2025-08-26 | S2a | 7,5 % | −0,0495 | −0,0920 |
| **2026-07-02** | S2a | 0,0 % | **−0,2288** | −0,1837 |
| **2026-07-05** | S2b | 4,5 % | **−0,2224** | −0,1769 |
| 2026-07-25 | S2b | 19,2 % | −0,1300 | −0,1381 |
| 2026-07-27 | *(série)* | — | −0,1396 | −0,1633 |

### Três leituras, e nenhuma era acessível com duas cenas

**1 · São dois passos.** Em Agosto de 2025 o contraste ocidental é **−0,050**;
em Julho de 2026 é **−0,13 a −0,23**. Não é um acontecimento com dois pontos de
amostra: é um degrau modesto até Agosto de 2025 e **um segundo, maior, entre
Agosto de 2025 e Julho de 2026**.

**2 · Agosto de 2025 é sólido.** Seis cenas em treze dias, três plataformas
diferentes, dão −0,0475 a −0,0525 — **amplitude de 0,005**. É a melhor
reprodutibilidade de todo o dossiê, e valida o processamento de passagem.

**3 · Julho de 2026 NÃO é sólido, e isto é a ressalva mais séria que saiu deste
ciclo.** O contraste ocidental vai de **−0,229 (2 de Julho) a −0,130 (25 de
Julho)** — **em 23 dias, e as duas cenas de cada extremo concordam entre si**
(−0,229/−0,222 e −0,130/−0,140). Não é ruído: é uma mudança real dentro do mês.

> **A escolha da cena dentro de Julho de 2026 muda o número principal por um
> factor de 1,7.** A série usa 27-07, que cai no extremo baixo dessa amplitude.
> Qualquer figura que cite um valor único para 2026 tem de levar a amplitude ao
> lado.

O oriental é mais estável: −0,092 a −0,108 em Agosto de 2025, −0,138 a −0,184 em
Julho de 2026.

---

## P3 · A PSA — a resposta não está no registo, e a pergunta merece ser feita ao contrário

Procurei em toda a cadeia uma razão para a PSA nunca ter sido pedida.

**Não existe nenhuma.** O que o certificado da C4 diz é:

> «A *Pseudomonas syringae* pv. *actinidiae* nunca foi procurada neste caso —
> com ou sem posição, em nenhuma matriz, em nenhuma data. O mesmo para qualquer
> outra bactéria e para vírus. *Instrumento independente:* **nenhum; conclusão
> negativa.** *Margem:* não afirmo que a PSA esteja ausente do pomar — afirmo
> que **não há um resultado, em nenhum sentido**.»

**E a sintomatologia não pode ter sido a razão, por três motivos que estão no
registo:**

1. **Não há amostras de folha.** O adversário da C5 (R7) mostrou que o painel
   foliar existe no texto e não no código: `MATRIZES` tem quatro entradas —
   raiz fina, colo/tronco, solo 0-30, solo 40-80 — e **zero são folha**. A PSA
   manifesta-se em folha, vara e colo; **nunca se amostrou o órgão onde ela se
   vê.**
2. **O painel foi escolhido por um pedido de laboratório, não por um
   diferencial.** Os quinze taxa da matriz são fungos, oomicetas e um nemátode.
   Não há uma única linha bacteriana ou viral em toda a matriz — não é que a
   bacteriologia tenha dado negativo: **nunca foi encomendada.**
3. **O adversário da C4 diz o contrário do que a pergunta supõe.** Ordenada a
   lista por «o que distinguiria este pomar de um pomar normal», ele escreve que
   **a PSA SOBE de prioridade, «porque tem prevalência regional conhecida»** —
   e que as nove linhas do informe 331/2025 descem, porque um segundo ponto
   neste pomar não diz se são fundo.

**A resposta honesta:** não sabemos porquê. O registo não contém uma decisão
fundamentada de a excluir — contém a sua ausência. E dado que ninguém amostrou
folha, ninguém podia ter usado sintomatologia foliar para a descartar.

Isto não afirma que seja PSA. Afirma que **a principal doença do kiwi no mundo
foi deixada de fora de um painel de quinze organismos sem que o registo diga
porquê**, num caso em que o desenho da campanha já vai ao terreno.

---

## O que muda na fila

| era | passa a ser |
|---|---|
| **1 ·** prominência de pérgola em 2025 | **CORRIDA.** 2025 não discrimina; 2021 responde. **Nova acção 1: a mesma medida sobre as ortofotos de 2010 e 2012 no foco oriental** — decide replantação contra nunca-plantado, e o método já discrimina nessas épocas |
| **2 ·** as onze cenas | **CORRIDA.** São dois passos. Julho de 2026 tem amplitude de 1,7× |
| **3 ·** REG-01, a comparação regional | mantém-se, e sobe a primeira |
| **novo ·** painel bacteriano e foliar na campanha | já estava na C5 R2 §4; **este resultado torna-o não negociável** |
