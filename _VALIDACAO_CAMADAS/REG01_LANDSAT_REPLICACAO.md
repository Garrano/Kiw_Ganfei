> # ⚠ RETIRADO em 01-09-2026
> Este documento sustenta o **A3**, que foi retirado: os cinco blocos do
> ENT 297313 tinham sido **desmatados em 2024**, e a queda caía do lado PRÉ da
> fronteira dos períodos. A conclusão da REG-01 **inverteu-se** — os focos de
> Ganfei são o pior e o segundo pior da região entre unidades de linha de base
> contínua (percentil 0 %).
> **Fica por ser o registo do erro e da sua descoberta.** O que vale está em
> `REG01_RETRACCAO_A3.md`. Não citar daqui.

# REG-01 · LANDSAT — replica nos três critérios, e o facto sobe a instrumento independente

**Data:** 01-09-2026 · **Ficheiros:** `reg01_landsat.py`, `reg01_landsat_r3.py`
**Acção 1 da fila.** O `guarda.py` autoriza o veredicto pela primeira vez sem a
marca de NÃO TESTÁVEL.

---

## Os critérios, escritos antes de correr

| | critério | limiar | resultado |
|---|---|---|---|
| **R1** | os cinco blocos do ENT 297313 entre os **oito piores** | ≥ 4 de 5 | **5 de 5** ✔ |
| **R2** | Spearman entre o degrau S2 e o Landsat | ρ ≥ 0,50 | **ρ = +0,890**, p < 10⁻⁴ ✔ |
| **R3** | focos de Ganfei **acima** do percentil 10 | > 10 % | **14 %** e **14 %** ✔ |

**R1 era a condição principal**, com falsificação escrita: se os cinco se
espalhassem pelo meio da distribuição, a REG-01 reabria. Não se espalharam.

## O que muda entre os dois instrumentos, e é de propósito

| | Sentinel-2 | Landsat 8/9 |
|---|---|---|
| agência | ESA | **USGS/NASA** |
| sensor | MSI | **OLI / OLI-2** |
| correcção atmosférica | Sen2Cor | **LaSRC** |
| órbita, hora de passagem | uma | **outra** |
| resolução | 10 m | 30 m |
| **cenas** | **9 datas escolhidas** | **100 cenas**, Jun–Set, nuvem < 40 %, 2017-2026 |

**As cenas mudaram de propósito.** Se o resultado do S2 dependesse da escolha
das nove datas, cem cenas de outra órbita apanhavam-no. Não apanharam.

O que **não** mudou, e não podia: as fronteiras (os mesmos polígonos do IFAP,
sem re-selecção) e a estatística (desvio à mediana regional da mesma cena;
degrau = média 2025-26 menos média 2017-2024).

## Os cinco, nos dois instrumentos

| CUL_ID | ha | **n30** | degrau Landsat | lugar | degrau S2 |
|---|---|---|---|---|---|
| 6705427 | 1,28 | 15 | **−0,3167** | **1.º de 37** | −0,4021 |
| 6705429 | 2,28 | 27 | **−0,2916** | **2.º** | −0,3820 |
| 6705428 | 1,02 | 11 | **−0,2720** | **3.º** | −0,3486 |
| 6705442 | 0,62 | 7 | **−0,2392** | **4.º** | −0,2081 |
| 6705432 | 2,30 | 25 | **−0,2388** | **5.º** | −0,3211 |

**Os mesmos cinco, nos cinco primeiros lugares.** O sexto pior do Landsat está a
−0,047 — **cinco vezes acima**. O corte é o mesmo nos dois instrumentos.

E os focos de Ganfei: **−0,0676** (ocidental, n30 = 26) e **−0,0706** (oriental,
n30 = 10). O pomar inteiro: **+0,0099**, percentil 41 — acima da mediana
regional.

## O extra que não estava pré-registado: NDMI

O Landsat traz o SWIR, que o Sentinel-2 nunca deu nesta cadeia. NDMI é **água no
copado, não verdura** — outra grandeza, não outra medição da mesma.

Os mesmos cinco ocupam os cinco piores lugares também em NDMI, com **−0,313 a
−0,405**. Os focos de Ganfei: −0,105 e −0,110, percentil 14 — **o mesmo lugar**.

**Não se lê isto como fisiologia.** Solo nu baixa o NDMI tanto como uma planta em
stress hídrico, e a composição destes blocos não foi verificada (ver ressalvas).
O que o NDMI acrescenta é uma **terceira concordância independente da banda**,
não um mecanismo.

## O n, que desta vez está impresso

O `landsat_independente.py` prometia no cabeçalho «só píxeis inteiramente dentro
da unidade, e reporta-se o n» e o código **não fazia nem uma coisa nem outra** —
reamostrava para 10 m, repetindo cada píxel nove vezes, e nunca contava nada.
Foi apanhado pelo Controlo 3.

Aqui trabalha-se **na grelha de 30 m**, o n sai por bloco, e blocos com n < 6
não entram (nenhum caiu). Nos focos exigiu-se **cobertura ≥ 5 das 9 células de
10 m** — a primeira contagem, sem esse crivo, dava 33 e 18 células para focos de
2,18 e 0,76 ha, ou seja **mais área do que os focos têm**. Corrigida, dá 26 e 10.

**E mesmo assim o n impresso é um limite superior**: são células da nossa grelha,
não píxeis nativos do Landsat, e a reamostragem por vizinho mais próximo pode pôr
um píxel nativo em duas células ou em nenhuma.

## O que o portão autorizou, e o que continuou a bloquear

**Autorizado** — primeira vez sem marca de NÃO TESTÁVEL:

> o degrau de 2025-26 **não é exclusivo desta exploração**, e há blocos vizinhos
> muito piores
> · instrumento: NDVI Sentinel-2, 38 blocos IFAP, 9 cenas
> · confirmado por: NDVI Landsat 8/9, 100 cenas
> · confirmado por: NDMI Landsat, outra banda

**Bloqueado, outra vez:**

> «a causa é regional» — **nenhum instrumento mede causa.** Replicar um padrão
> espacial em duas constelações não identifica o agente. Continua a valer que
> dois sítios com o mesmo sintoma podem ter causas diferentes.

## As ressalvas, que sobrevivem à replicação

- **A composição dos blocos do 297313 continua por verificar.** Parte daquele
  −0,32 pode ser chão, arranque ou replantação. **Duas constelações concordarem
  não muda isto** — ambas veriam chão da mesma maneira, e o NDMI baixo é
  compatível com solo nu. É a razão pela qual a acção 3 da fila (LiDAR ou
  ortofoto sobre aqueles cinco blocos) **não foi tornada dispensável por este
  resultado**.
- **A mediana regional continua dominada por dois donos**, 30 dos 37 blocos.
- **Os focos de Ganfei estão no limite da resolução do Landsat**: 26 e 10
  células. O percentil 14 deles é consistente com o S2, não é preciso.
- **O degrau do Landsat é sistematicamente menor** que o do S2 (−0,32 contra
  −0,40; −0,068 contra −0,106). Esperado — 30 m mistura o alvo com a vizinhança.
  **A ordenação replica; as magnitudes não, e não se diz que replicam.**

## A fila, depois disto

| | acção | estado |
|---|---|---|
| ~~1~~ | ~~repetir a REG-01 com o Landsat~~ | **feita — replica nos três critérios** |
| **1** | **contactar o ENT 297313**, ou quem o acompanhe na CCDR-N | sem custo, e agora com dois instrumentos a sustentá-la |
| **2** | LiDAR ou ortofoto sobre os cinco blocos do 297313 | **não dispensada pela replicação** — decide declínio contra chão |
| 3 | a linha da PSA no livro-razão | sem custo |
| 4 | campanha de Setembro, com pontos nas **duas** explorações | alto |

---

**Nota.** Isto é o primeiro facto desta cadeia a passar o `guarda.py` com
instrumento independente concordante em vez de `nao_testavel()`. Os dezoito que
foram retirados caíram todos por lhe faltar exactamente isto.
