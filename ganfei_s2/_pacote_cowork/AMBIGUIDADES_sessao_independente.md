# Ambiguidades da especificação — reexecução cega Ganfei

Implementação independente, sem acesso ao código nem aos resultados do autor.
Cada entrada: o que estava ambíguo → interpretações defensáveis → a que escolhi
(e porquê) → **quanto muda o resultado com a alternativa (calculado, não
estimado)**. Os cálculos das alternativas estão em `codigo/variantes_a.py`
(máscaras, Q1, Q2, Q5) e `codigo/variantes_b.py` (Q3, Q3b, Q4); os registos de
execução em `codigo/variantes_a.log` e `codigo/variantes_b.log`. Todas as
escolhas estão parametrizadas no dicionário `OPT` de `codigo/lib.py`.

Convenção de gravidade: **[GRANDE]** muda o sentido de uma conclusão ou um
número operativo em mais de ~10 %; **[MÉDIA]** muda números reportáveis na
segunda casa; **[PEQUENA]** só afecta casas decimais ou casos raros;
**[NULA-AQUI]** existe na especificação mas, com estes dados, dá exactamente o
mesmo resultado (foi medido, não assumido).

---

## A. Máscaras (afecta todos os quadros)

### A1. Onde está o centro do pixel em coordenadas de máscara — [GRANDE]

**Ambíguo.** A especificação diz "um pixel pertence à máscara se o seu centro
cai dentro do polígono", mas não diz se, nas coordenadas de `masks.json`, o
pixel (linha i, coluna j) tem o centro em (j+0,5, i+0,5) (convenção
GDAL/rasterio: inteiros são cantos) ou em (j, i) (convenção
matplotlib/`imshow`, típica de polígonos clicados sobre uma imagem). Os
vértices misturam inteiros e meios (`53.0, 73.5`), o que é compatível com
ambas.

**Escolhi** centro em +0,5 (convenção geoespacial; é a que `rasterio.features.
rasterize` aplica por construção).

**Alternativa (centro em +0,0)** — pixels que mudam de pertença: pomar 189,
manchaW 39, zona0 35, referência sã 73 (de 415 → 446 pixels). Efeito:

| quadro | efeito da alternativa |
|---|---|
| Q1 `def_mod_ha` | dif. média 0,08 ha, máx 0,40 ha (pomar 2019: 5,76 → 5,36) |
| Q1 `def_mod_pct` | dif. média 1,0 pp, máx 4,7 pp (zona0 2020: 39,4 → 44,1 %) |
| Q1 `ndvi_mediana` | máx 0,029 (zona0 2025-08-14: 0,694 → 0,665) |
| Q2 maior componente 2026 | manchaW 3,65 → 3,51 ha; zona0 2,21 → 2,18 ha; zona0_alargada 3,80 → 3,97 ha; alongamento manchaW 1,38 → 1,46 |

Nenhum quadro sobrevive intacto: 44/44 médias e 33/33 áreas de défice mudam.

### A2. Regra de fronteira quando o centro cai exactamente sobre uma aresta — [MÉDIA]

**Ambíguo.** Com vértices em .5 e centros em +0,5, há arestas horizontais e
verticais que passam **exactamente** pelos centros de pixels; "cai dentro" não
define se a fronteira conta. Ferramentas diferentes decidem de forma diferente
(GDAL usa regra de varrimento com meio-aberto; `matplotlib.path.Path.
contains_points` decide caso a caso).

**Escolhi** `rasterio.features.rasterize` (GDAL), por ser o instrumento
canónico e ter regra documentada.

**Alternativa (`matplotlib.Path`, mesma convenção de centro)** — pixels
diferentes: pomar 27, saudavel_2 16, zona0 16 (221 → 207), saudavel_3 8,
manchaW 6, referência 24. Efeito em Q1: `def_mod_ha` máx 0,14 ha (zona0 2026:
2,21 → 2,07), `def_mod_pct` máx 1,2 pp; Q2 2026: manchaW 3,65 → 3,56 ha, zona0
2,21 → 2,07 ha e **orientação de zona0 1,1° → 179,6°** (é a mesma direcção,
mas nota que o intervalo [0,180) faz um salto aqui). Só a fronteira, sem mudar
de convenção, já mexe na segunda casa decimal de todas as áreas.

### A3. Máscara vazia / componente inexistente — [PEQUENA]

**Ambíguo.** Não se diz o que reportar quando a máscara de défice fica vazia
após abertura (acontece em manchaW em 2021, 2022 e 2023: 4, 3 e 5 pixels brutos,
0 depois da abertura 2×2).

**Escolhi** área 0 e geometria `NaN` (linha mantida no quadro). Alternativas:
omitir a linha, ou saltar a abertura quando ela anula tudo. A alternativa de
"abertura antes da intersecção" (ver B3) devolve 2, 2 e 3 pixels nesses anos —
i.e. transforma "sem foco" em "foco de 0,02–0,03 ha", o que muda a data de
primeira detecção em manchaW se alguém a ler no quadro.

---

## B. Quadro 1 e Quadro 2

### B1. NaN dentro das máscaras — [NULA-AQUI]

**Ambíguo.** Média "ignorando NaN" está definida para `ref`, mas não para as
outras médias/medianas nem para as contagens de défice (NaN < limiar é falso:
conta como "não défice" ou exclui-se?).

**Escolhi** `nanmean`/`nanmedian` em todas; NaN não conta como défice.
**Medido:** os únicos NaN da série principal são 36 pixels em 2017-07-02,
linhas 40–61, colunas 161–199 — fora de todas as máscaras. No lóbulo oeste
(Q5), os 40 NaN de 2017 também estão fora do bloco. Diferença = 0 em todas as
células de Q1, Q2 e Q5. A ambiguidade é real mas inerte com estes dados; fica
activa se as máscaras forem redesenhadas para leste da coluna 160.

### B2. Percentagem sobre pixels totais ou válidos — [NULA-AQUI]

A especificação resolve-o para Q1 ("sobre o total"), mas não para Q5. Como não
há NaN dentro das máscaras (B1), as duas dão o mesmo em todas as datas
(medido: 0/33 diferenças em Q1; 0/11 em Q5).

### B3. Ordem "intersectar com a região" e "abrir" — [MÉDIA]

**Ambíguo.** O texto diz "máscara de défice = (NDVI < ref−0,05) ∩ região" e
depois "aplicar abertura". Li-o literalmente (abrir *depois* de intersectar).
Mas é igualmente defensável abrir o mapa de défice do pomar inteiro e só depois
recortar pela região — evita que a aresta da região destrua quadrados 2×2 que
existem na imagem.

**Alternativa (abrir antes de intersectar)** — 25 das 33 células de
`deficit_pos_abertura_ha` mudam, sempre para cima: manchaW 2020 15 → 25 px,
manchaW 2025-08-14 136 → 148 px, zona0_alargada 2024 196 → 204 px; e manchaW
2021/2022/2023 passam de 0 a 2–3 px (ver A3).

### B4. Forma e implementação do elemento estruturante 2×2 — [NULA-AQUI, verificado]

Um elemento par não tem centro; `scipy.ndimage.binary_opening` com
`np.ones((2,2))` usa uma origem convencionada. Implementei a abertura pela
definição (união dos quadrados 2×2 totalmente contidos) e comparei com o
scipy: **0 pixels de diferença em todas as 33 combinações data×região**. Já a
dilatação 15×15 e o fecho 5×5 são ímpares, sem ambiguidade de origem.

### B5. Conectividade da maior componente — [PEQUENA aqui, potencialmente GRANDE]

**Escolhi** 8-conectividade (o habitual em detecção de manchas; `skimage` usa-a
por defeito). O `scipy.ndimage.label` usa 4 por defeito — outro implementador
cairia aí sem pensar.

**Alternativa (4)** — muda apenas 2020-07-18: zona0 maior componente 0,64 →
0,55 ha e alongamento 2,04 → 1,85; zona0_alargada 3 → 4 componentes (área da
maior igual). Nas restantes 31 células, igual. O efeito é pequeno porque a
abertura 2×2 já elimina quase todas as ligações diagonais; num foco mais
fragmentado seria decisivo.

### B6. Centróide: índice de pixel ou centro de pixel — [PEQUENA]

Reportei o centróide na convenção de A1 (j+0,5, i+0,5). Com índices puros,
todas as coordenadas descem 0,5 px (5 m). Não muda alongamento nem orientação.

### B7. Covariância com ddof=1 ou ddof=0 — [PEQUENA]

`np.cov` usa ddof=1 por defeito; "matriz de covariância das coordenadas" pode
ser populacional. **Alongamento é idêntico** (a razão cancela). Os comprimentos
dos eixos escalam por √((n−1)/n): 0,4 % para n≈100–400, mas **13 % para as
componentes de 4 pixels** (manchaW 2019 e 2024: 11,5 m → 10,0 m).

### B8. Convenção da orientação — [GRANDE para quem lê o ângulo]

**Ambíguo.** "Orientação do eixo maior em graus, [0,180)" — a partir de que
eixo e em que sentido? Em coordenadas de imagem (y para baixo) o ângulo do
vector próprio é horário a partir de +x (este); em coordenadas cartesianas/
geográficas (y para cima) é anti-horário, e a partir do norte seria outra
coisa ainda.

**Escolhi** imagem (y para baixo), a partir de +x, horário.
**Alternativa (y para cima):** θ → 180−θ. Em 2026-07-27: manchaW 166,9° →
13,1°; zona0_alargada 167,3° → 12,7°; zona0 1,1° → 178,9°. O mesmo eixo
físico lê-se como "quase E–W, inclinado para NW" ou "quase E–W, inclinado para
NE" — a prosa que interpretar o ângulo em termos de vinha/linhas de plantação
pode errar o lado.

---

## C. Quadro 3 e 3b (Landsat)

### C1. Numeração dos bits de `qa_pixel` — [GRANDE]

**Ambíguo.** "bit 1 (nuvem dilatada), bit 3 (nuvem), bit 4 (sombra)". Na
documentação USGS Collection 2 os bits são contados a partir de 0 (bit 1 = valor
2, bit 3 = 8, bit 4 = 16), e a legenda coincide com essa contagem — mas um
implementador que conte a partir de 1 usa os valores 1, 4 e 8 (fill, cirrus,
nuvem) e nunca vai reparar, porque o código corre.

**Escolhi** 0-based (bits 2|8|16 = 26), que é o que as legendas designam.

**Alternativa (1-based, 1|4|8)** — cenas válidas manchaW 134 → 142; zona0
131 → 138. Médias anuais de ΔLST (manchaW): 2020 +0,18 → +0,64 °C; **2021
+0,27 → −0,50 °C**; 2026 +2,46 → +2,06 °C; 2017 +0,59 → +0,85 °C. Q3b:
declive −15,9 → −12,5 °C/NDVI, **r −0,77 → −0,44**; resíduo anual 2021
−0,36 → −1,20 °C. A ambiguidade decide se 2021 aquece ou arrefece e se o
resíduo de 2021 "se distingue do ruído".

### C2. Onde aplicar a máscara: na grelha 10 m reamostrada ou na grelha nativa 30 m — [MÉDIA]

**Ambíguo.** A especificação manda reamostrar para 100×200 e depois calcular
médias por máscara; mas as máscaras são polígonos e podiam ser rasterizadas
directamente a 30 m. As duas não são equivalentes: a 10 m, cada célula Landsat
pesa pelo número de centros de 10 m que contém (1 a 9); a 30 m, cada célula
pesa 1 e o limiar "20 pixels válidos" significa 1,8 ha em vez de 0,2 ha.

**Escolhi** máscara a 10 m sobre o produto reamostrado (leitura literal).

**Alternativa (30 m)** — cenas válidas 134 → 132 e 131 → 130; ΔLST anual
muda até 0,10 °C (manchaW 2018 +0,42 → +0,52; zona0 2018 +0,29 → +0,20);
Q3b quase igual (declive −15,9 → −16,0, r −0,768 → −0,772). Os anos com
poucas cenas são os mais sensíveis.

### C3. A regra dos 20 pixels aplica-se também à referência? — [PEQUENA]

**Escolhi** aplicar às três máscaras (uma diferença precisa de dois termos
válidos). Há 11 cenas em que a referência tem <20 válidos; em 4 delas a
manchaW tinha ≥20 e a cena foi descartada por causa da referência. A
alternativa (nunca descartar pela referência) mantinha diferenças calculadas
sobre 0–19 pixels de referência.

### C4. Reamostragem por vizinho mais próximo: método — [NULA-AQUI + achado]

Implementei por mapeamento do centro de cada pixel 10 m para a célula 30 m que
o contém, e comparei com `rasterio.warp.reproject(..., nearest)`: **0 pixels
diferentes**. Achado: a grelha Landsat (33×67, 529950–531960 E, 4654610–
4655600 N) não cobre a última linha da grelha de 10 m (200 pixels sem dado,
linha 99) e excede 10 m a leste; nenhuma máscara toca essa linha, logo sem
efeito nos quadros.

Sensibilidade a **bilinear** (não é o que a especificação diz; medi só para
saber quanto pesa a escolha): ΔLST anual muda ≤0,02 °C. O método de
reamostragem é irrelevante face a C1.

### C5. Q3b: que cenas entram e como se agrega o resíduo — [PEQUENA]

Usei todas as cenas com ΔLST e ΔNDVI de manchaW válidos (134), OLS de ΔLST
sobre ΔNDVI, resíduo médio por ano civil com pesos iguais por cena. Alternativas
não medidas mas evidentes: ponderar por ano, ou excluir Abril (NDVI 0,3–0,5,
copado ainda ausente — ver OBSERVACOES). Reporto também o desvio-padrão do
resíduo por ano para se poder julgar "não se distingue do ruído".

---

## D. Quadro 4 (topografia)

### D1. Domínio da regressão cota~NDVI — [GRANDE — inverte o sinal]

**Ambíguo.** "Ao nível do pixel de 10 m, excluindo os pixels de manchaW e
zona0" — sobre todo o rectângulo 100×200 ou só sobre o `pomar`? A frase não diz
"pomar".

**Escolhi** pomar (a pergunta é "os focos estão em cotas anómalas para *este
pomar*"; a AOI inclui rio, estradas e outras parcelas).

**Alternativa (toda a AOI com cota)** — n 2253 → 17 428; **declive −0,048 →
+0,036 NDVI/m** (inverte); r −0,28 → +0,33; NDVI previsto para manchaW 0,851
→ 0,431 e a "diferença observado−previsto" passa de **−0,105 para +0,314**;
zona0 de −0,126 para +0,183. Com a alternativa, os focos ficam *acima* do
esperado para a cota. É a ambiguidade com maior poder de inverter uma conclusão.

### D2. Distribuição de cotas por máscara: células de 50 cm ou pixels de 10 m — [PEQUENA/MÉDIA]

**Escolhi** células do MDT (polígono transformado para EPSG:3763 e rasterizado
a 50 cm) — são "as cotas" propriamente ditas.
**Alternativa (médias por pixel de 10 m)** — média e mediana iguais à segunda
casa; desvio-padrão desce (manchaW 0,311 → 0,282; zona0 0,358 → 0,319), p5/p95
apertam até 0,12 m (zona0 p95 8,569 → 8,451). O percentil da mediana no pomar
muda <0,4 pp.

### D3. Como transportar as máscaras para EPSG:3763 — [PEQUENA]

Polígono transformado (vértices reprojectados, rasterizado a 50 cm) ou
herança da pertença do pixel de 10 m (cada célula do MDT pertence à máscara do
pixel que contém o seu centro). Diferença: ref 173 229 → 166 136 células,
zona0 86 864 → 88 466; cotas médias mudam ≤0,017 m (zona0 8,004 → 7,987);
percentil de zona0 92,4 → 91,9.

### D4. Definição de "percentil que a mediana ocupa" — [NULA-AQUI]

`percentileofscore` com `rank`, `weak`, `strict` ou `mean`: idênticos a duas
casas (32,48 / 52,47 / 92,38) porque não há empates a 50 cm.

### D5. Sentido da regressão — [GRANDE se lido ao contrário]

"Regressão linear entre cota e NDVI" seguida de "NDVI previsto" implica
NDVI = a·cota + b. A regressão inversa (cota sobre NDVI) invertida
algebricamente daria NDVI previsto de 1,03 para manchaW e 0,24 para zona0 —
absurdo, mas é o que sai se se trocar x e y. Registado porque a frase permite.

### D6. NDVI previsto: na cota média ou média das previsões — [NULA]

Iguais por linearidade (verificado: 0,850564 em ambos).

---

## E. Quadro 5 (lóbulo oeste)

### E1. Métrica da distância "a mais de 5 px" — [MÉDIA]

**Escolhi** euclidiana (`distance_transform_edt`), estrita (>5).
**Alternativa Chebyshev (quadrado 11×11)** — bloco 788 → 733 px (−7 %);
área em défice desce em todas as 11 datas (2018: 3,59 → 3,38 ha; 2023: 2,13 →
1,78 ha); NDVI médio muda ≤0,003. **Manhattan:** 807 px. **≥5 em vez de >5:**
810 px. A escolha da métrica move o bloco em ±0,5 ha.

### E2. Conectividade na maior componente (b1) — [NULA-AQUI]

4 vs 8: bloco idêntico (788 px, 0 diferenças).

### E3. Fecho 5×5 no bordo da imagem — [NULA-AQUI]

`scipy` trata o exterior como fundo; um fecho com *padding* dá o mesmo porque o
bloco não toca o bordo (linhas 18–58, colunas 13–49 de 80×100).

### E4. Limiar "> 0,78" vs "≥ 0,78" — [NULA-AQUI]

Nenhum pixel tem exactamente 0,78 em float32.

### E5. Referência do corpo principal: a ambiguidade A1 propaga-se — [PEQUENA]

O `ref` de cada data vem da união das três máscaras sãs do corpo principal;
com centro em +0,0 a união tem 446 pixels em vez de 415. **Medido:** `ref`
muda até 0,0035 (2017: 0,8432 → 0,8397; 2026: 0,8885 → 0,8866) e a área em
défice do bloco muda até 0,06 ha (2025-08-14: 3,17 → 3,11 ha; 2026: 1,59 →
1,54 ha). O bloco em si não muda (é definido só a partir da imagem b1).

---

## F. Achados fora das ambiguidades (não exigiram escolha, mas convém saber)

- **Nada precisou de rede.** As únicas dependências foram numpy, scipy,
  rasterio, pyproj (transformação 32629↔3763) e matplotlib. `cenas.json`
  refere uma fonte STAC/AWS, mas as imagens já estão em disco.
- `dados/sentinel/masks.json` é uma cópia byte-a-byte de `dados/masks.json`.
- O manifesto Landsat tem 148 cenas e todas existem em disco; nenhuma cena
  órfã. Cenas por ano: 15, 9, 9, 9, 7, 18, 23, 20, 23, 15 (2017→2026).
- O MDT não cobre toda a AOI (1926 pixels de 10 m sem cota, todos fora do
  pomar) e tem 24 460 células NaN, nenhuma dentro das máscaras.
- Não houve empates na escolha da maior componente em nenhuma célula de Q2
  (coluna `empates_maior`).
