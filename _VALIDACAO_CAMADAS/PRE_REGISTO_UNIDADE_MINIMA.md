# Pré-registo · a unidade mínima a que um núcleo de défice é afirmável

**Escrito a 2026-09-11, ANTES de correr.** Guião: `_VALIDADE_GESTAO/unidade_minima.py`.

---

## 1 · A pergunta, fixada

*Qual é o menor núcleo contíguo de défice que não se explica pelo que este
pomar produz quando não está a acontecer nada?*

Unidade de análise: **componente conexa** (vizinhança-8) do mapa de défice de
uma cena, em células de 10 m. Fronteiras: dentro do polígono `pomar`
(30,31 ha, derivado só de ortofotos DGT). Termo definido: «défice» é a
definição já pré-registada na `c2_00_comum` — NDVI abaixo de
(referência sã da mesma data − 0,05), com abertura morfológica 2×2.

## 2 · Porque não serve o que já lá está

A `c2_00_comum` tem `MIN_NUCLEO = 15` células (0,15 ha). É um **limite mínimo
de cartografia**, fixado por convenção, não por nulo nenhum. Serve para não
listar ruído; **não autoriza a dizer que um núcleo de 15 células é real**.
A pergunta acima nunca foi respondida neste caso.

## 3 · O nulo, e porque é este

**O nulo é a própria série** — a mesma lógica que o
`terreno_contra_declinio.py` usou a 29-08 e que o `CLAUDE.md` endossa. O nulo
ingénuo está **explicitamente excluído** pelo projecto: com autocorrelação
espacial de 0,86 a 0,96, permutar células ao acaso torna tudo significativo.

**Janela do nulo — cinco cenas:** `2020-07-18`, `2021-07-16`, `2022-07-31`,
`2023-08-07`, `2024-07-22`.

A janela é escolhida por **dois critérios externos aos tamanhos dos núcleos**,
e isso é o que a torna legítima:

1. todas **precedem** a perda de copado certificada (2,20 ha, Jul-2024 →
   Jul-2025, certificada e auditada);
2. todas **sucedem** o estabelecimento do Erica Novo, que em 2017 tinha NDVI
   médio 0,694 e só em 2020 chega a 0,871 — uma plantação a entrar em produção
   não é um pomar em declínio, e as cenas de 2017 e 2018 saem por isso.

Nenhum dos dois critérios olha para o tamanho de núcleo nenhum. **Se a janela
fosse escolhida por a área em défice ser baixa nesses anos, seria escolher o
nulo pelo resultado** — e não é.

`2019-09-02` está fora por fenologia (G10), como em toda a camada.

## 4 · A estatística, e o limiar

Juntam-se os tamanhos de **todas** as componentes conexas das cinco cenas do
nulo. **A unidade mínima é o percentil 95 dessa distribuição conjunta**,
arredondado para cima à célula.

Lê-se: *um núcleo deste tamanho ou maior aparece em menos de 5 % das
componentes que este pomar produz num ano sem acontecimento.*

## 5 · O que se afirma depois, e o que não se afirma

- **Afirma-se:** quais os núcleos de 2025 e 2026 que igualam ou excedem a
  unidade mínima, e onde estão.
- **NÃO se afirma** que um núcleo acima do limiar tem causa biótica, nem que um
  abaixo não existe. O teste é de **extensão**, não de etiologia.
- **NÃO se afirma** nada sobre o B1: tem zero células na AOI Sentinel
  (E529950–531950, N4654600–4655600). Não medido ≠ sem declínio.

## 6 · Os portões de paragem — escritos antes, e decidem por esta ordem

| | portão | o que obriga |
|---|---|---|
| **U-A** | **poder.** Se o maior núcleo de 2026 **não** atingir o percentil 95 do nulo, o teste **NÃO TESTÁVEL**. | É a lição da RQ6: um teste sem resolução devolve sempre «nada a assinalar», e isso não é resultado nenhum — é a forma B. Decide **antes** de qualquer leitura. |
| **U-B** | **base.** Se as cinco cenas do nulo derem menos de **40 componentes** no total, não há distribuição para tirar um percentil 95. | Um percentil 95 sobre 12 valores é o maior de 12, não um percentil. |
| **U-C** | **estabilidade.** O percentil 95 recalculado deixando **uma cena de fora de cada vez** (*leave-one-out*, cinco recálculos) não pode variar mais de **±30 %**. | Se variar mais, o limiar é de uma cena e não do período, e diz-se isso em vez de o usar. |
| **U-D** | **sensibilidade ao limiar de défice.** Repete-se tudo a 0,03 e 0,08 além do 0,05 pré-registado. Se o conjunto de núcleos afirmados em 2026 mudar de identidade (e não só de contorno), é escolha e não achado — declara-se. | É a mesma prova a que a `c2_05_manchas.py` já submeteu o foco ocidental. |

## 7 · O que já se sabe que este teste NÃO pode ver

A referência sã **desce ela própria** — 0,897 (2024) → 0,860 (2025) → 0,843
(2026). Como o défice é medido contra ela, **o limiar move-se com o padrão**.
Consequência assumida e declarada: nos anos em que a referência desce, este
teste **subestima** o défice. Não se corrige aqui; regista-se, e a peça que o
mostrar tem de o dizer na cara.

E os dois anos da descida são os dois primeiros em **Sentinel-2C** (era S2A/S2B
até 2024). A mudança de unidade **não está excluída** como explicação do
deslocamento comum. Isso não afecta este teste — que é de extensão relativa,
dentro de cada cena — mas afecta qualquer leitura de nível absoluto.

---

*Assinado antes da corrida. Resultado, seja qual for, vai para o §8 deste
ficheiro, e o guião entra na `pendentes.csv` para adversário.*
