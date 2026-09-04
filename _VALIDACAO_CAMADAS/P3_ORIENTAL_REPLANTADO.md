> # ⚠ RETIRADA PARCIAL
>
> **§2 e §3 deste documento estão retirados** por `P5_RETRACCAO_DO_REPLANTADO.md` (31-08-2026).
> O veredicto «o foco oriental foi replantado» assentava só na prominência de
> pérgola — um instrumento a confirmar-se a si próprio — e o nível absoluto de
> NDVI não tem cova nenhuma nos anos em causa.
>
> **§1, §4 e §5 mantêm-se.** Este documento **não** leva cartucho de retirada
> total, e essa distínção é deliberada: marcar a mais apaga prova boa.
> Registado no nível-afirmação da `TRIAGEM_DE_FONTES.md`.

# P3 — o foco oriental foi REPLANTADO. E a correcção sobre a PSA.

**Data:** 31-08-2026
**Fonte:** mapas de prominência certificados da C2 (`c2_12_prom_2010/2012/2021.npy`),
**sem recomputação** — aplicaram-se-lhes as máscaras do LiDAR.
**Verificação:** a implementação do P1 reproduz o mapa certificado de 2021 a
**+0,0000 nas cinco unidades**.

---

## 1 · A SEQUÊNCIA, e não é ambígua

Posição de cada unidade entre chão lavrado (0 %) e referência sistemática
(100 %), medida **dentro de cada imagem**:

| | 2010 | 2012 | 2021 | 2025 |
|---|---|---|---|---|
| REF · referência | 100 % | 100 % | 100 % | *instrumento falha* |
| RESTO · resto do pomar | 58 % | 62 % | 80 % | *idem* |
| **ORI-COM** · oriental, tem pérgola em 2025 | **111 %** | **79 %** | **14 %** | *idem* |
| **ORI-SEM** · oriental, sem pérgola em 2025 | 26 % | 8 % | 6 % | *idem* |
| NU21 · chão lavrado | 0 % | 0 % | 0 % | *idem* |

As âncoras separam-se nas três épocas (IQR disjuntos). Em 2025 não, e a razão
está no P1: a ortofoto de 2025 tem camalhões com plástico contínuo, que produzem
periodicidade de 5 m que não é pérgola.

## 2 · O VEREDICTO

> ### O foco oriental são DUAS coisas, e nenhuma é o que se assumia.
>
> **ORI-COM (0,76 ha) — REPLANTADO.** Tinha pérgola madura em 2010 (111 %, acima
> da referência) e em 2012 (79 %). **Perdeu-a antes de 2021** (14 %,
> indistinguível de chão lavrado). **Tem estrutura outra vez em 2025**, medida
> pelo LiDAR.
>
> **ORI-SEM (1,26 ha) — NUNCA TEVE.** 26 % em 2010, 8 % em 2012, 6 % em 2021.
> Chão ao longo de toda a série.

**A hipótese A do P3 confirma-se para metade do foco, e a B para a outra
metade.** Não era uma escolha entre as duas: eram as duas, em sítios diferentes.

## 3 · O QUE ISTO FAZ AO CASO

**O «degrau» de 2025-26 no foco oriental está a acontecer sobre uma replantação
com menos de quatro anos.** Não é pomar adulto em declínio: é pomar novo, no
mesmo sítio onde um pomar adulto já tinha sido arrancado.

Isto não enfraquece a hipótese biológica — **especifica-a.** Uma replantação que
falha no terreno onde a anterior foi arrancada é o quadro clássico da
**doença de replantação / arrastamento de patogénio de solo**, que é
precisamente a primeira das três hipóteses abertas. Passa de hipótese geral a
hipótese com sítio, com data e com desenho.

E resolve a objecção do Controlo 3 pela raiz: a partição `h ≥ 0,5` é
pós-tratamento, e **agora sabe-se exactamente o que ela selecciona** — a parte
replantada contra a parte que nunca foi plantada.

## 4 · O QUE MUDA NAS CAMADAS

| onde | o que muda |
|---|---|
| **C2 · V-R8** | a ressalva «pós-tratamento» mantém-se, mas deixa de ser incerteza: a partição separa **replantado** de **nunca plantado**, e isso está medido em três épocas |
| **C3** | o positivo de *M. hapla* no B3 passa a ter um enquadramento novo: é um bloco que contém uma replantação recente. A pergunta «é fundo ou é causa» ganha o desenho que lhe faltava |
| **C4 · D1** | o contraste ocidental-contra-oriental deixa de ser «declínio novo contra chão antigo» e passa a **«declínio sobre pomar adulto contra falha sobre replantação recente»** — que é uma afirmação mais forte e mais útil |
| **C5** | a campanha ganha uma unidade que não tinha: **a replantação de ORI-COM**, com a sua própria pergunta — porque é que a replantação está a falhar |

## 5 · O QUE FICA POR SABER

- **Quando foi arrancada.** Entre 2012 e 2021 — a ortofoto de 2007 e a de
  2004-2006 estão em disco e podem estreitar o intervalo por trás; para o
  fecho, é a gestora que sabe.
- **Quando foi replantada.** Entre 2021 e Julho de 2025.
- **Porque foi arrancada.** É a pergunta que mais interessa e não se responde
  com satélite nenhum.

---

# 6 · CORRECÇÃO — a PSA

**Facto do tipo 1, recebido em 31-08-2026:**

> **Ninguém encomendou nem testou nada para PSA porque os sintomas das plantas
> não eram compatíveis.**

**Retiro o que escrevi no `P1_P2_RESULTADOS.md` §P3.** Escrevi «não sabemos
porquê; o registo não contém uma decisão fundamentada de a excluir». **Existia
uma decisão fundamentada** — uma exclusão clínica por sintomatologia, que é a
via normal e correcta de a fazer. Pela regra do projecto, testemunho directo
ganha ao nosso cálculo, e o cálculo que ele derruba **retira-se, não se
reconcilia**.

**O que continua verdade, e é a única coisa que fica desta secção:** essa
decisão **não está escrita em lado nenhum da cadeia**. Foi por isso que quatro
camadas a assinalaram como lacuna inexplicada — a C4 no CONFIRMADO, a C5 na
árvore de acções, o adversário da C4 a subi-la de prioridade, e eu ontem.

**Custa uma linha e fecha uma lacuna que já consumiu quatro documentos:**

> *BIO-24 · PSA — não ensaiada. Excluída clinicamente por incompatibilidade
> sintomatológica, observação de [quem], em [data]. Não é ausência de decisão.*

Com essa linha no livro-razão, a PSA sai da lista de aberturas e o painel
bacteriano deixa de ser uma exigência da campanha — passa a ser opcional, e a
decisão de o incluir ou não é de quem observou as plantas, não minha.
