# Rederivação geográfica das máscaras de análise

Sessão de geometria, 28-08-2026. Código e imagens em `SAIDA_MASCARAS\`.
Máscaras novas em `ganfei_s2\sentinel\masks_geograficas.json`.
**Nada em `ganfei_s2\` foi alterado ou apagado** — `masks.json` mantém a data e a
soma MD5 de origem (`3d30f41dc2262f9779bd68087deea36d`).

Aplica-se o `CONTROLOS.md` na íntegra: cada facto certificado leva o
**instrumento independente** que o confirma, e as dez quantidades-âncora estão
reportadas no fim.

---

## 1. O defeito que se veio corrigir

`fazer_masks_v2.py` abre com «poligonos GEOGRAFICOS e ESTATICOS; nenhum e
re-derivado por data» e a seguir escreve:

```python
copado = binary_opening((nd > 0.78) & (dist > 5), ...)   # nd = 2026-07-27
mw     = pomar & (nd < 0.76) & jw
```

`pomar` é «NDVI de 2026 acima de 0,78». `manchaW` é «NDVI de 2026 abaixo de
0,76». A série mede depois como o NDVI da `manchaW` evoluiu de 2017 até 2026 —
circular por construção. `saudavel` depende de `copado`, logo a referência
também foi escolhida sobre a última cena da série que ela calibra.

Confirmado por leitura de código e reexecução: as áreas do ficheiro antigo
reproduzem-se ao píxel (29,03 / 4,54 / 4,27 / 2,20 ha).

---

## 2. Método

### 2.1 Alinhamento

As ortofotos DGT estão em **EPSG:3763**; a grelha de análise está em
**EPSG:32629**. Não se subamostrou nenhuma janela. Cada época foi reprojectada
com `rasterio.warp.reproject` para duas grelhas explícitas, ambas ancoradas no
canto NO da AOI (529950, 4655600): uma de 0,5 m (2000 × 4000) para inspecção, e
a de análise a 10 m (100 × 200), esta obtida por agregação exacta de blocos
20 × 20 da primeira — portanto com alinhamento garantido por construção, e não
por coincidência. `g01_render_orto.py`.

### 2.2 A assinatura: compasso de fiada, não textura

Quatro assinaturas foram ensaiadas e três falharam. Fica o registo porque a
falha é informativa:

| tentativa | assinatura | resultado | porque falhou |
|---|---|---|---|
| 1 (anterior) | desvio-padrão local da luminância | 42,99 ha, IoU 0,315 | sebes e árvores dispersas também têm textura alta |
| 2 (anterior) | textura alta **e** homogénea a 50 m | 14,45 ha, IoU 0,000 | seleccionou campo liso — região completamente outra |
| 3 (`g03`) | fracção da potência do espectro na banda 2,5–9 m | mapa sem separação | textura aperiódica espalha potência por toda a banda |
| 4 (`g04`) | máximo da autocorrelação no anel 3–9 m | desfasamento mediano 3,2 m = bordo do anel | mede suavidade, não compasso: a autocorrelação decai monotonamente |
| **5 (`g05`)** | **prominência do primeiro pico secundário da autocorrelação radial, por sector angular** | **separação limpa** | um pico secundário só existe se houver periodicidade real |

A medida que resulta: percorre-se o perfil radial da autocorrelação r(d) numa
janela de 40 × 40 m sobre a luminância passada a filtro passa-alto de 15 m,
encontra-se o primeiro mínimo local d₀ e mede-se quanto o perfil volta a subir
depois dele. Textura aperiódica não volta a subir.

O que aparece então é decisivo: **uma região coerente de compasso 5,0 m que tem
exactamente a forma do bloco, em 2012 e em 2025, e mais nada na AOI a tem.**
5 m é o compasso de fiada de kiwi em pergola. A vinha das parcelas a sul dá 2–3 m;
as estufas 7–9 m; o campo lavrado não dá pico nenhum.

**As duas épocas são independentes e têm estados de coberto opostos** — em 2012
a fiada é jovem e vê-se o chão entre linhas; em 2025 a fiada está sob cobertura
branca, em altíssimo contraste. Que duas situações opostas devolvam a mesma
geometria é o que dá confiança, e não o valor de nenhum limiar.

### 2.3 Inspecção visual a cada passo

Foi a lição das duas tentativas anteriores: ambas eram óbvias à vista e
invisíveis na estatística. Cada candidato foi desenhado sobre a ortofoto e
olhado — `v06`, `v07`, `v08`, `v10`, `v11`, `v12`, `v13`, `v14`, `v15`, `v18`.
Foi assim que se apanharam os dois falsos positivos que sobreviviam à
estatística (§3.1) e o erro de concepção do §3.4.

---

## 3. As máscaras, uma a uma

### 3.1 `pomar` — 30,31 ha

**Regra.** Célula com compasso de 4,4–5,6 m detectado em **2010, 2012 ou 2025**,
na margem do rio onde está a exploração, em componente de ≥ 0,10 ha.
Nenhum NDVI Sentinel, de nenhuma data, entra nesta definição.

**Porquê a estrutura e não o coberto.** Postes e fiadas existem com a planta viva
ou moribunda. Uma videira debilitada continua a ter pergola. A assinatura segue
a cultura, não o vigor — que é precisamente o que a máscara antiga não fazia.

**Dois falsos positivos, apanhados a olho e resolvidos por teste ao nível da
componente** (`g11`), nunca ao nível da célula:

| componente | área | veredicto |
|---|---|---|
| E530155 N4655441 | 0,58 ha | **rejeitada** — vinha na margem **norte** do Minho; 150 células de água no segmento até ao bloco principal |
| E531518 N4654921 | 0,55 ha | **rejeitada** — bloco de **estufas**; luminância mediana de 2021 = 172, contra 108,9 no núcleo da pergola |
| E530680 N4655084 | 26,03 ha | aceite (lente principal) |
| E531196 / E531349 / E531488 | 2,11 / 1,60 / 0,57 ha | aceites (faixas da escada NE) |

O teste tem de ser por componente e não por célula: qualquer limiar de
luminância aplicado célula a célula apagaria a `zona0` (§3.4).

**Instrumento independente:** ortofotos DGT a 25 cm (2021 e 2025) e 50 cm (2010,
2012), que não entram em nenhuma medição de NDVI. Concordância com o eixo medido
pela C0 por via inteiramente diferente (SVD sobre o polígono antigo): **azimute
70,3° contra 70,0°**, extensão E530140–531530 / N4654850–4655460 contra
E530145–531525 / N4654865–4655465. Diferença ≤ 15 m em qualquer bordo.

### 3.2 `saudavel` — 1,10 ha, 110 células

**Regra.** Grelha regular: uma célula de 10 m de 30 em 30 m, sobre o pomar com
pergola detectada em 2010 ou 2012, a ≥ 20 m de qualquer bordo. **Nenhuma célula
é aceite ou rejeitada por causa de nenhum valor radiométrico, de nenhuma data.**
O único critério é a posição. Cobre todo o eixo, E530250–531490.

**Porquê não «as manchas que parecem sãs».** Uma referência escolhida por parecer
sã mede distância ao **melhor caso**, não distância ao normal, e desloca-se
sozinha quando o pomar inteiro desce. A antiga foi escolhida por ter NDVI alto em
**2026-07-27** — a última cena da série que ela própria calibra —, e o efeito
disso é mensurável e grande (§4).

**Restringe-se a pergola instalada antes de 2017** para a referência não apanhar
plantação nova, que sobe por crescimento e não por sanidade. É um critério de
idade da infraestrutura, não de vigor.

**Robustez do desenho** (`g17`). Uma grelha tem passo e tem fase; se o resultado
dependesse deles não valeria nada. Testaram-se passos de 20, 30 e 40 m e **todas**
as fases: 29 desenhos. Declive do NDVI da referência entre −0,00319 e −0,00442
por ano. **Os 29 dão declive negativo.** A referência antiga dá +0,00375.

**A grelha não evita as manchas, e não deve evitar.** Das 110 células, **18 caem
dentro da antiga `manchaW` e 5 dentro da `zona0`**. É isso que faz dela uma
amostra e não uma escolha: apanha o pomar em proporção, incluindo a parte
doente. O efeito é conservador — puxa a referência para baixo e portanto
**subestima** o défice (quantificado em §4.4).

**Limite que é obrigatório declarar.** Uma referência interna mede contraste
**espacial**. Se o pomar inteiro descer, ela desce com ele e o défice não muda.
Nenhuma referência tirada de dentro do pomar pode detectar declínio uniforme.
Para isso seria precisa uma referência externa — e foi exactamente uma
referência externa mal georreferenciada (o bloco «B1») que originou esta cadeia.
Reportam-se por isso também as alternativas sem grelha:

| referência alternativa | declive (9 cenas) | p |
|---|---|---|
| mediana do `pomar` inteiro | −0,00098/ano | 0,65 |
| mediana do `pomar_2012` | −0,00162/ano | 0,42 |
| percentil 75 do `pomar` | −0,00014/ano | 0,93 |

### 3.3 `manchaW` — **retirada**

Não há máscara `manchaW` no ficheiro novo. Era `pomar & (nd2026 < 0,76)`
dilatada por um disco de 3 px: definia a mancha pelo sinal que depois se media.
Uma mancha é um **resultado**, não um lugar.

O défice passa a ser medido célula a célula contra a referência geográfica, e as
manchas saem do mapa, data a data. Que isto funciona, vê-se no resultado: em
2026-07-27 emergem quatro componentes de ≥ 0,20 ha, e a segunda maior é

> **3,00 ha em E530340–530620 / N4654950–4655180, com 0 % sobre chão lavrado**

que é, sem ter sido posta lá, a área da antiga `manchaW` (E530310–530670 /
N4654920–4655160). A mancha reaparece por si a partir de uma máscara que não a
conhece. É a verificação mais forte que este trabalho produziu.

### 3.4 `zona0` — 2,02 ha, verificada, e com uma reserva grave

O polígono antigo é genuinamente geográfico e foi mantido, intersectado com o
novo `pomar`: **202 das 220 células (91,8 %)** caem dentro. As 18 que ficam de
fora estão no caminho que a limita a sudeste.

**Mas a verificação contra a ortofoto encontra outra coisa** (`g13`, `g15`;
imagens `v12_zona0.png`, `v13_zona0_epocas.png`, `v15_nu2021.png`):

> **41,4 % da área da `zona0` é chão lavrado na ortofoto DGT de 2021**, a 25 cm,
> a meio da série Sentinel. O talhão principal mede **1,04 ha** e ocupa
> E530920–531050 / N4655030–4655190, isto é, o centro da `zona0`. Na ortofoto de
> 2025 esse mesmo talhão tem fiadas cobertas.

O código antigo descreve a `zona0` como «linhas mortas, NDVI baixo». A leitura
directa da ortofoto diz que, em 2021, em 41 % dela **não havia planta**. O NDVI
baixo dessa fracção é ausência de cultura, não vinha em declínio.

Sequência completa nas sete épocas: 1995, 2004 e 2007 campo aberto; 2010 e 2012
pergola nos flancos com faixa clara ao meio; **2021 chão lavrado ao centro**;
2025 fiadas cobertas. Não consegui datar o acontecimento nem estabelecer se
houve arranque (§6).

Para contraste, medido no mesmo cálculo: **0 %** da antiga `manchaW` e **0 %** da
referência sistemática estão sobre chão lavrado em 2021. A `manchaW` está
genuinamente coberta de planta; o problema dela é de definição, não de substrato.

Publica-se por isso, junto das máscaras, uma camada `nu2021` (1,67 ha, 5,5 % do
pomar) — **que não é máscara de análise**: serve só para a camada seguinte poder
separar, no mapa de défice, o que é planta em declínio do que é chão.

---

## 4. Desvio, quantidade a quantidade

Ambas as séries correram no **mesmo código** (`g16_serie.py`), com a **mesma
regra de défice** (célula em défice ⇔ NDVI < referência da data − 0,05), sobre as
**mesmas 11 cenas**. A única diferença são as máscaras.

### 4.1 Geometria

| quantidade | antigo | novo | desvio |
|---|---|---|---|
| `pomar` | 29,03 ha (2903 cél.) | 30,31 ha (3031 cél.) | +1,28 ha (+4,4 %) |
| IoU `pomar` antigo × novo | — | — | **0,844** |
| só no antigo / só no novo | — | — | 1,87 ha / 3,15 ha |
| referência sã | 4,54 ha (454 cél.) | 1,10 ha (110 cél.) | −3,44 ha |
| `manchaW` | 4,27 ha (427 cél.) | **retirada** | — |
| `zona0` | 2,20 ha (220 cél.) | 2,02 ha (202 cél.) | −0,18 ha |
| azimute do eixo | 70,0° (C0) | 70,3° | +0,3° |

### 4.2 Série

| quantidade | antigo | novo | desvio |
|---|---|---|---|
| NDVI da referência, 2017-07-02 | 0,8379 | 0,8884 | **+0,0505** |
| NDVI da referência, 2026-07-27 | 0,8862 | 0,8425 | **−0,0436** |
| **declive da referência** (9 cenas) | **+0,00375/ano** (p 0,125) | **−0,00395/ano** (p 0,146) | **inverte o sinal** |
| NDVI do `pomar`, 2017-07-02 | 0,7787 | 0,7940 | +0,0153 |
| NDVI do `pomar`, 2026-07-27 | 0,8082 | 0,8136 | +0,0054 |
| declive do `pomar` | +0,00240/ano (p 0,55) | +0,00124/ano (p 0,74) | −0,0012 |
| NDVI da `zona0`, 2017-07-02 | 0,6891 | 0,6877 | −0,0014 |
| NDVI da `zona0`, 2026-07-27 | 0,6556 | 0,6612 | +0,0056 |
| declive da `zona0` | −0,00932/ano (p 0,156) | −0,00951/ano (p 0,177) | −0,0002 |
| **défice da `zona0`** (ref − zona0) | **+0,01307/ano, p = 0,0206** | **+0,00556/ano, p = 0,3399** | **−57 % e perde a significância** |
| % do pomar em défice, 2017-07-02 | 29,42 % | 31,74 % | +2,3 pp |
| % do pomar em défice, 2026-07-27 | 39,61 % | 31,61 % | **−8,0 pp** |
| área em défice, 2017-07-02 | 8,54 ha | 9,62 ha | +1,08 ha |
| área em défice, 2026-07-27 | 11,50 ha | 9,58 ha | −1,92 ha |
| maior mancha, 2026-07-27 | 4,72 ha | 4,60 ha | −0,12 ha |

### 4.3 As três consequências que este desvio tem

**(a) O sinal do declive da referência inverte-se.** A C0 certificou em **G6**
que «a referência sã não desce: +0,0038/ano» e concluiu que o défice não estava a
ser subestimado. Com uma referência escolhida por posição e não por aparência, o
declive é **−0,0040/ano**, e é negativo nos 29 desenhos de grelha testados.
Nenhum dos dois é significativo (p 0,12–0,19); o que muda é o sinal, e portanto a
direcção do enviesamento. **G6 tem de ser reaberto.** A própria G6 já registava
que «a magnitude desse enviesamento não foi quantificada» — está quantificada:
0,05 de NDVI em 2017 e 0,044 em 2026, em sentidos opostos, ou seja ~0,094 de
inclinação artificial ao longo da série.

**(b) O único resultado estatisticamente significativo da análise antiga não
sobrevive.** «O défice da Zona 0 cresce a +0,0131/ano, p = 0,0206» passa a
+0,0056/ano, p = 0,3399. Mais de metade do crescimento aparente era a referência
a ser mantida alta no fim da série por construção. O défice da Zona 0 continua
positivo e continua a maior parte, mas **não é distinguível de ruído** com a
referência corrigida.

**(c) O salto da última cena encolhe.** A fracção do pomar em défice em 2026
passa de 39,61 % para 31,61 %. O salto de 2024 (16,3 %) para 2026 (39,6 %) era em
parte artefacto: `pomar` era «NDVI 2026 > 0,78» e a referência «NDVI 2026 alto»,
o que aperta a distribuição de 2026 contra o limiar.

### 4.4 Diagnóstico: de onde vem o declive negativo da referência

Só diagnóstico. **Retirar células por elas estarem em mancha é seleccionar pelo
resultado, e não entra na definição de nenhuma máscara.**

| subconjunto | n | declive | p | 2017 | 2026 |
|---|---|---|---|---|---|
| referência completa | 110 | −0,00395 | 0,146 | 0,8884 | 0,8425 |
| sem as 18 células na `manchaW` antiga | 92 | −0,00240 | 0,245 | 0,8875 | 0,8622 |
| sem `manchaW` e sem `zona0` | 87 | −0,00159 | 0,383 | 0,8885 | 0,8721 |
| **só as 18 células na `manchaW`** | 18 | **−0,01184** | 0,067 | 0,8929 | **0,7420** |

Leitura: fora das manchas a referência está praticamente plana (−0,0016,
p = 0,38); a queda vem das 18 células que a grelha, por ser cega, colocou dentro
da mancha. **É assim que deve ser** — uma amostra sistemática apanha o pomar em
proporção — e o efeito é conservador: subestima o défice, não o inflaciona.

Coerente com o mapa de declive por célula (`v18_defice_declive.png`): mediana
−0,0003/ano, 54,1 % das células a descer, sem declínio generalizado. Há uma
parcela em E530580–530820 com declive fortemente **positivo**, que na ortofoto é
chão aberto em 2012 e copado fechado em 2021: crescimento de plantação, não
recuperação.

### 4.5 As manchas emergentes de 2026-07-27

Componentes de ≥ 0,20 ha, do mapa de défice, sem nenhuma máscara de mancha:

| área | extensão | sobre chão lavrado em 2021 |
|---|---|---|
| 4,60 ha | E530810–531170 / N4654980–4655250 | **34 %** |
| 3,00 ha | E530340–530620 / N4654950–4655180 | 0 % |
| 0,47 ha | E531110–531240 / N4655160–4655360 | 21 % |
| 0,21 ha | E530480–530610 / N4654860–4654910 | 0 % |

A maior mancha — a que cobre a `zona0` — tem **um terço da sua área sobre chão
que estava lavrado em 2021**. A segunda, a oeste, não tem nenhuma.

---

## 5. Quantidades-âncora (Controlo 2)

| Âncora | Declarado | Medido nesta camada | Difere? |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | idem, exacta; grelha 100 × 200 a 10 m | não |
| polígono `pomar` (píxeis) | 2903 | **3031** | **sim, +128** |
| polígono `pomar` (ha) | 29,0 | **30,31** | **sim, +1,28** |
| referência sã (píxeis) | 454 | **110** (desenho sistemático, outro objecto) | **sim** |
| máscara `manchaW` (píxeis) | 427 | **retirada por desenho** | **sim** |
| máscara `zona0` (píxeis) | 220 | **202** (∩ com o novo `pomar`) | **sim, −18** |
| cenas na série | 11 | 11 | não |
| cenas de plena estação | 9 | 9 usadas; justificação continua por demonstrar (C0/G10) | não, mas herdada com reserva |
| NDVI médio da referência, 2017-07-02 | 0,838 | **0,8884** | **sim, +0,050** |
| NDVI médio da referência, 2026-07-27 | 0,886 | **0,8425** | **sim, −0,044** |

Sobre o conflito conhecido booleana × polígono: **as máscaras novas não têm esse
conflito.** São entregues como grelha booleana explícita (`*_bits`, 100 linhas de
200 caracteres) e os contornos são derivados dela, não o contrário. A contagem de
células é a definição operativa e é única. Reproduzi na mesma corrida as
contagens antigas — 2903 / 454 / 427 / 220 — e batem.

---

## 6. Instrumentos independentes (Controlo 1)

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| `pomar` = 30,31 ha, E530140–531530 / N4654850–4655460 | `g11_pomar_limpo.py` | ortofoto DGT 2025 a 25 cm (cobertura branca) **e** 2012 a 50 cm (fiada jovem) — dois estados de coberto opostos; inspecção visual em `v11_pomar_sobre_2021/2025.png` | ±1 célula = ±10 m no contorno |
| eixo do `pomar` = azimute 70,3° | `g11`, SVD sobre as células | C0/G3 mediu 70,0° sobre o polígono antigo, por via inteiramente diferente | ±1° |
| compasso de fiada = 5,0 m | `g05_prominencia.py` | valor agronómico corrente de pergola de kiwi; e coerente entre 2012 e 2025 | ±0,5 m (passo do perfil) |
| a componente de E530155 N4655441 está na outra margem | `g11`, travessia de água | ortofoto: o rio Minho é visível entre as duas | qualitativa, inequívoca |
| a componente de E531518 N4654921 é estufa | `g11`, luminância 2021 = 172 | ortofoto 2021 e 2025: telhados de vidro visíveis | qualitativa, inequívoca |
| 41,4 % da `zona0` é chão lavrado em 2021 | `g15_solo_nu_2021.py`, limiar 130 | leitura directa da ortofoto a 25 cm em sete épocas (`v13_zona0_epocas.png`) | limiar declarado; a direcção não depende dele |
| a `manchaW` antiga não está sobre chão lavrado (0 %) | `g15`, mesmo cálculo | mesma ortofoto | idem |
| declive da referência é negativo | `g16`, `g17` | **não há instrumento independente** — é NDVI confirmado com NDVI. Ver §7 | — |

**Facto que por isso NÃO passa como certificado:** o declive de −0,0040/ano da
referência sistemática. É NDVI verificado contra NDVI. O que passa é a
afirmação mais fraca e verificável: *o sinal do declive da referência depende da
regra de escolha da referência, e a regra antiga escolhia sobre a última cena da
série.* Essa afirmação prova-se com o código, não com o sinal.

---

## 7. O que não se conseguiu resolver

**7.1 Datar o que aconteceu no centro da `zona0`.** Sei que em 2021 é chão
lavrado e que em 2025 tem fiadas cobertas. Não sei se houve arranque de vinha
adulta ou se o talhão nunca chegou a estar plantado. Procurei a sequência
completa `pergola em 2010/2012 → nu em 2021 → pergola em 2025` e deu **zero
células** (`g14`): a faixa que está nua em 2021 não tinha sido detectada com
compasso em 2010 nem em 2012. Isto é compatível com as duas histórias e não
separa nenhuma. Faltam: uma ortofoto entre 2012 e 2021, ou o registo de
plantação da exploração.

**7.2 Quanto do `pomar` é plantação posterior a 2017.** A sub-máscara
`pomar_novo` (6,77 ha, «sem compasso detectado em 2010/2012») **não é utilizável
como facto** e não foi publicada. A inspecção (`v12_mascaras_novas.png`) mostra
que mistura duas origens: mudança real de uso, e falha do detector quando o
copado fecha e as fiadas perdem contraste. O detector tem falsos negativos
demonstrados — a `manchaW` dá 69,8 % de assinatura em 2010 e só 22,5 % em 2012,
sem que nada tenha lá mudado.

**7.3 Se o défice absoluto está certo.** Só se mediu contraste espacial. Uma
descida uniforme de todo o pomar é invisível a qualquer referência interna, e não
há referência externa utilizável — a que existia era o bloco «B1», em quarentena.

**7.4 A faixa a leste de E531530.** As ortofotos DGT terminam em E531800 e o
`pomar` novo acaba em E531530, portanto o polígono está coberto. Mas a AOI vai
até E531950 e não se pode excluir pergola nos 150 m finais só com Sentinel a
10 m. Herda-se a lacuna da C0.

**7.5 A composição da série.** Usei as mesmas 9 cenas de plena estação para os
declives, para o desvio ser atribuível às máscaras. A C0 rejeitou a justificação
fenológica dessa composição (dia 243 dentro, dia 245 fora) e essa rejeição
mantém-se de pé: os declives desta secção herdam-na.

**7.6 O tamanho da referência.** 1,10 ha contra 4,54 ha. É consequência do
desenho: uma grelha de 30 m sobre uma parcela de 328 m de largura, com recuo de
20 m ao bordo, não dá mais. O erro-padrão da média da referência sobe de ~0,001
(2017–2024) para 0,0075 (2026) — não por a amostra ser pequena, mas por a
referência estar a ficar heterogénea no fim da série, o que é informação que a
referência antiga apagava por construção. Passos de 20 m (2,55 ha) dão o mesmo
declive.

---

## 8. Ficheiros

```
_VALIDACAO_CAMADAS\
  REDERIVACAO_MASCARAS.md          este ficheiro
  SAIDA_MASCARAS\
    g01_render_orto.py             reprojecção das 7 épocas para a grelha
    g02_recortes.py                recortes a 0,5 m por época
    g03_campos.py                  descritores; periodicidade por banda (falhou)
    g04_trelica.py                 autocorrelação no anel (falhou)
    g05_prominencia.py             prominência do pico — a assinatura que serve
    g06_candidato.py               primeiro candidato + contorno sobre a ortofoto
    g07_zoom.py                    inspecção bordo a bordo
    g08_pomar.py                   versão com filtro de solo nu (rejeitada, §3.4)
    g09_diagnostico.py             luminâncias; porque o filtro de solo nu cai
    g10_pomar_final.py             pomar sem esse filtro
    g11_pomar_limpo.py             testes por componente; `pomar` final
    g12_referencia_zona0.py        grelha sistemática; verificação da zona0
    g13_zona0_epocas.py            a zona0 nas sete épocas
    g14_arranque.py                procura de arranque+replantação (deu zero)
    g15_solo_nu_2021.py            chão lavrado dentro do pomar em 2021
    g16_serie.py                   série antiga × nova, desvio quantidade a quantidade
    g17_robustez.py                29 desenhos de grelha para a referência
    g18_final.py                   diagnóstico, mapas, masks_geograficas.json
    v01..v18_*.png                 49 imagens de inspecção
    *.npy, serie.json              intermédios reproduzíveis

ganfei_s2\sentinel\
  masks_geograficas.json           NOVO (100 kB). masks.json não foi tocado.
```

`masks_geograficas.json` traz, para cada máscara, a grelha booleana explícita
(`pomar_bits`, `saudavel_bits`, `zona0_bits`, `nu2021_bits` — 100 cadeias de 200
caracteres) e os contornos derivados dela, mais a grelha declarada
(EPSG:32629, origem 529950 / 4655600, 10 m, 100 × 200) e a nota de método de cada
uma.
