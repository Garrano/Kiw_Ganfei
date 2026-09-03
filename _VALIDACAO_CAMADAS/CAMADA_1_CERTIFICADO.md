# Camada 1 — Substrato · CERTIFICADO

Sessão C1, 28/29-08-2026. Código e figuras em `SAIDA_C1\`.

**Não há paragem de linha.** Nenhum facto herdado da R2 foi rejeitado. Três
foram precisados e um número herdado (o r = −0,756 da retirada térmica) foi
localizado: existe, mas não é o que a frase que o cita diz que é.

**Herança usada.** `CAMADA_0_REVISAO_R2.md` e o seu suplemento (G34–G37), e
`REGISTO_DE_NOMES.md`. O `CAMADA_0_CERTIFICADO.md` e o `CAMADA_1_PROMPT.md`
foram lidos para método e contexto; onde divergem da R2, a R2 venceu. Nenhum
facto retirado pela R2 (G13, G14, o «lóbulo oeste B1», a distância de 1,06 km)
entra em nenhum cálculo desta camada. A máscara `manchaW` não foi usada: onde
o vocabulário antigo aparece em ficheiros herdados, foi traduzido segundo o
`REGISTO_DE_NOMES.md` — **`manchaW` = FOCO OESTE, `zona0` = FOCO ESTE** — e a
tradução está declarada em cada script.

**Unidades de comparação.** Os dois focos comparam-se por **discos geométricos
de 90 m de raio** centrados nas coordenadas da G34, intersectados com o
polígono `pomar`: 248 células (2,48 ha) a oeste, 255 (2,55 ha) a este. É a
mesma regra para os dois, não usa NDVI, não usa mapa de défice e não usa a
forma de nenhuma mancha. O polígono `zona0` (202 células) é reportado ao lado
por continuidade — é o foco ESTE no vocabulário antigo. A referência é a rede
sistemática de 110 células da R2 G4.

---

## CONFIRMADO

| facto | ficheiro e cálculo que o prova | INSTRUMENTO INDEPENDENTE | margem |
|---|---|---|---|
| **Os 21 mosaicos MDT de 50 cm cobrem a AOI inteira.** Zero das 20.000 células da grelha de 10 m fica sem MDT, e zero das 3031 células do `pomar`. | `c1_01_lidar_inventario.py` — bounds de cada mosaico contra os centros das células transformados para EPSG:3763 | os mosaicos são 21 ficheiros distintos do fornecedor; a cobertura foi contada célula a célula, não lida de metadados | exacta |
| **Os dois focos caem em mosaicos de campanhas de voo diferentes.** Foco OESTE inteiro no 158565 (voo **2025-08-02**); foco ESTE inteiro no 159565 (voo **2026-01-15**). A costura entre os dois corre a E ≈ 530755, exactamente entre eles. | `c1_02_costura.py` — catálogo OGC-API da DGT, `datetime` por item | medição empírica na costura, sem metadados (linha seguinte) | exacta |
| **A costura não introduz degrau vertical utilizável.** Atravessando-a, faixa de 10 m contra faixa de 10 m: **+0,058 m** de mediana. O mesmo passo de 10 m *dentro* de cada mosaico, sem costura: +0,025 m (158565) e +0,028 m (159565). Sobre 2000 linhas de costura, 1000 m. | `c1_02_costura.py` §b | o controlo é o próprio terreno a igual distância, não outro metadado | ±0,06 m |
| **O foco ESTE está 1,204 m mais alto que o foco OESTE.** Medianas: OESTE 6,638 m (percentil **30** do pomar), referência 6,798 m (percentil 38), ESTE 7,842 m (percentil **84**), `zona0` 8,069 m (percentil 90). Mann-Whitney p ≈ 0 (n = 248 e 255). Vinte vezes o degrau máximo possível da costura. | `c1_03_mdt.py` + `c1_04_focos_terreno.py` | **Copernicus GLO-30** (`lidar/_glo30.tif`, TanDEM-X, radar, 30 m, missão e sensor sem relação com o LiDAR aéreo): **mesma ordenação nas quatro unidades** — OESTE 7,372 < referência 7,632 < ESTE 7,684 < `zona0` 7,884; ESTE − OESTE **+0,312 m**, mesmo sinal. `c1_10_nivelamento.py` §a | ±0,06 m (costura) |
| **E não é só «estar mais a leste».** Ajustado o perfil longitudinal do próprio pomar (eixo azimute 70,3° da R2 G3, subida de +0,085 % para ENE, r² 0,177), o foco ESTE fica **+0,589 m acima** do perfil e o OESTE **−0,198 m abaixo**; a referência −0,233 m; `zona0` +0,800 m. É um alto local, não o extremo de um plano inclinado. | `c1_10_nivelamento.py` §c — regressão da cota na coordenada ao longo do eixo, resíduos por unidade | a ordenação dos resíduos reproduz-se no GLO-30 (linha acima) | ±0,10 m |
| **O foco ESTE é o interflúvio; o foco OESTE está na drenagem.** Altura sobre a linha de drenagem mais próxima (HAND): OESTE 0,130 m, referência 0,150 m, ESTE 0,353 m, `zona0` 0,538 m (ESTE − referência +0,203 m, p = 1,1e-6; OESTE − ESTE −0,223 m, p = 1,1e-24). Distância à drenagem: **13,4 m / 23,6 m / 55,8 m / 73,0 m**. Área contribuinte p95: 875 / 603 / 381 / 331 m². Fracção da unidade sobre linha de drenagem (≥ 2000 m²): **1,99 % / 1,01 % / 0,33 % / 0,01 %**. | `c1_05_bacia.py` e `c1_11_escalas.py` — pysheds `fill_pits → fill_depressions → resolve_flats → flowdir → accumulation` a 1 m sobre MDT próprio | **Sentinel-1 RTC** (radar C, 441 cenas): o foco ESTE tem VV consistentemente mais baixo, o OESTE não — linha abaixo. Dois instrumentos sem relação apontam o mesmo sentido | limiar de 2000 m² declarado |
| **A armadilha do `resolve_flats` é real e enorme.** 33,14 % do MDT de 1 m é plano. Sem resolver planos, a acumulação máxima é **4.465 m²**; com eles, **313.739 m²** — factor **70**. `fill_depressions` altera 0 células. Qualquer delimitação de bacia feita sem esse passo é artefacto. | `c1_05_bacia.py` — as duas variantes corridas lado a lado no mesmo MDT | os scripts herdados `escoamento.py` e `bacia2.py` **têm** o passo; `bacia.py` (que produziu `bacia.json`) não o tem | exacta |
| **A química do solo entra no mapa: o bloco do foco ESTE é o mais pobre da exploração.** O `B3 - 7 ha (2026-03-03)` tem CaO **< 154 mg/kg** (abaixo do limite de detecção), MgO 36,0, K₂O 74,7, P₂O₅ 107, C:N 5,9, MO 1,6 %, pH 5,6 — o **mínimo dos nove boletins em cinco dos sete parâmetros**. Os vizinhos imediatos na banda são `Erica Novo` (válvulas 10-11, a oeste) com CaO 879 e 1200, e `B4` (válvulas 16-17, a leste) com CaO 1100. **É um buraco, não o extremo de um gradiente.** | `c1_06_solo_no_mapa.py` — folha «Soil Chemistry by Block» de `Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx`, ligada a `valvulas_por_area.json` (R2 G35) | o **SAR** e o **MDT**, independentes da química, põem o mesmo bloco como o mais alto, o mais afastado da drenagem e o de retrodifusão mais baixa | ver NÃO TESTÁVEL: n = 1 por bloco |
| **A colocação das válvulas da R2 G35 reproduz-se.** Soma das áreas tabeladas das válvulas 6-17 = **27,30 ha**, igual ao declarado. Válvula 8 a **35 m** do centro do foco OESTE (a G35 diz 34 m). Válvulas mais próximas do foco ESTE: **13 a 81 m, 14 a 93 m** — B3, como a G34 diz. | `c1_06_solo_no_mapa.py` — aritmética sobre `valvulas_por_area.json` | a nomeação independente do gestor («Zona 0 = válvulas 8, 9, 10»), que não entrou no cálculo da G35 | ±10 m sobre a posição da G35 |
| **A carência de cálcio no bloco do foco OESTE está confirmada por segunda matriz.** O boletim de solo mais próximo do foco OESTE é `B2 - V7`, a **111 m** (válvula 7): CaO 264 e 505 mg/kg («muito baixo» / «baixo»). A **análise foliar** do mesmo bloco (`B2_V7__Folha__Junho_26.pdf`, Junho/2026) dá **Ca 2,2 % contra referência 3–4,7 %, «Baixo»**. | `c1_06_solo_no_mapa.py`; folha «Master Log» do mesmo livro | **a folha é outra matriz, outro método analítico e outra data** que o solo — é o instrumento independente | leitura directa |
| **O chão lavrado de 2021 está quase todo no foco ESTE e nenhum no OESTE.** Das 167 células de `nu2021` (1,67 ha), **101 caem no disco ESTE (39,6 % dele)**, **0 no disco OESTE**, **0 na referência sistemática**; 91 das 202 células de `zona0` são chão lavrado (**45,0 %** — reproduz a G30 ao decimal). As restantes 66 células ficam a E530835–531165 / N4655015–4655265, contíguas, ainda em B3. | `c1_04_focos_terreno.py` §nu2021, sobre `nu2021_bits` de `masks_geograficas.json` | a máscara vem da ortofoto de 25 cm de 2021 (comparação **dentro de uma só imagem**, permitida pela R2 G37); o MDT e o SAR, ambos posteriores e independentes dela, separam a mesma área | ±1 célula |
| **Esse chão tem assinatura de radar própria — mas ela é anterior a 2021.** Nos Invernos de 2016-17 a 2025-26 (441 cenas Sentinel-1 RTC, órbitas 125 e 147 em separado), `nu2021` tem VV **1,2 a 3,5 dB abaixo** da referência sistemática, **em todos os dez Invernos**, incluindo os cinco anteriores à ortofoto. Antes/depois de 2021: órbita 125 **−0,19 dB (p = 0,20)**, órbita 147 **+0,62 dB (p = 0,009)** — sinais opostos, nenhum degrau. | `c1_13_sar_antes_depois.py` | o SAR é um instrumento (radar activo, banda C) sem relação com a ortofoto óptica que definiu a máscara; e as duas órbitas são geometrias de vista independentes | ±0,3 dB entre Invernos |
| **A lavra e o foco são dois sinais separáveis.** Dentro do disco ESTE, parte lavrada menos parte não lavrada = **−0,856 dB** (órbita 125, p = 3,7e-8) e **−0,854 dB** (órbita 147, p = 2,0e-4). O chão lavrado **fora** do disco ESTE está a −1,94 / −2,86 dB da referência (p ≈ 1e-9/1e-10). A parte **não lavrada** do foco ESTE está a −0,77 / −0,56 dB (p = 3,3e-7 / 4,4e-6). | `c1_12_sar_lavrado.py` — unidades disjuntas por construção | duas órbitas com geometria de vista diferente dão o mesmo valor a três casas | ±0,2 dB |
| **O foco OESTE é indistinguível da referência no radar durante nove Invernos, e cai no décimo.** VV do foco OESTE menos o pomar inteiro: entre −0,30 e +0,48 dB de 2016-17 a 2024-25; no Inverno de **2025-26**, **−1,107 dB** (órbita 125) e **−0,774 dB** (órbita 147) — o maior desvio da série nas duas órbitas. Nesse mesmo Inverno o pomar inteiro está no seu **menor** desvio contra a referência (−0,17 / −0,27 dB): não é efeito de campanha nem de calibração. | `c1_13_sar_antes_depois.py` + `c1_15_figuras.py` (F3) | duas órbitas independentes; e o pomar inteiro serve de controlo interno na mesma cena | ±0,25 dB |
| **A rugosidade do foco ESTE sobrevive ao controlo de campanha.** Rugosidade a 25 m: ESTE 0,167 m, OESTE 0,124, referência 0,124. O viés de campanha medido no pomar inteiro (1521 células Ago/2025 contra 1476 Jan/2026) é **0,0073 m**. Contra as células de referência **da mesma campanha**, o foco ESTE está **+0,0379 m** (p = 1,3e-18) e o foco OESTE **+0,0016 m** (p = 0,058). | `c1_04_focos_terreno.py` §controlo de campanha | o controlo é a partição do voo, não outro cálculo do mesmo MDT | ±0,008 m |
| **A precipitação herdada reproduz-se exactamente e a ordenação dos Invernos é certificável.** `pendente_precipitacao.csv` reproduzido com **diferença máxima de 0,00 mm**. Ordenação contra **ERA5** (Spearman +0,927, p = 1,1e-4, 10 Invernos) e contra **CERRA** (+0,900, p = 0,037, nos 5 Invernos que cobre). Mais seco: 2021-22, 663,6 mm. Mais húmidos: 2022-23 (1809,3) e 2023-24 (1807,8). 2024-25 = 1156,7 mm, a meio. | `c1_08_clima.py` | ERA5 e CERRA são reanálises com núcleos e assimilação distintos do ERA5-Land | ±25 mm (viés entre produtos) |
| **A retirada da linha térmica está bem fundada.** ΔT contra ΔNDVI, 118 cenas Landsat 8/9 completas: foco ESTE Pearson −0,769 / Spearman **−0,756**; foco OESTE −0,657; agregado dos dois −0,591. Decisivo: o **controlo interno** (terreno agrícola fora do pomar, definido sem referência aos focos) dá **r = −0,925**, a mais forte de todas — o acoplamento é uma propriedade genérica da superfície, não das manchas. O resíduo de ΔT depois de retirado o ΔNDVI ainda correlaciona com a temperatura do ar (r = −0,356 e +0,516). **A linha não é ressuscitada.** | `c1_07_termico.py` sobre `audit_termico.csv` | o controlo interno é uma unidade que não entrou no argumento original da retirada | r declarado |
| **O pomar é duas vezes mais plano que o terreno envolvente comparável, à escala da parcela.** Resíduo do ajuste de um plano em janelas de 60 m: pomar **0,0355 m** (n = 61), envolvente à mesma cota e a > 30 m do pomar **0,0703 m** (n = 80), p = 3,2e-10. Declive de forma (50 m): pomar 0,449°, envolvente 0,515°, p = 2,0e-14. | `c1_10_nivelamento.py` §c e `c1_11_escalas.py` | a comparação é com terreno **fora** do pomar na mesma faixa de cota do mesmo MDT — não com outro cálculo sobre o pomar | ±0,01 m |

### Quantidades-âncora (CONTROLOS.md, controlo 2)

`c1_14_ancoras.py` · ficheiro `c1_14_ancoras.json`.

| âncora | declarado na abertura | obtido em C1 |
|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | **igual**, nas 11 imagens |
| grelha | 200×100 de 10 m | **igual** |
| cenas na série | 11 | **11** |
| polígono `pomar` | 2903 px / 29,0 ha | **3031 px / 30,31 ha** — é a máscara geográfica da R2 G2, não a antiga |
| referência sã | 454 px | **110 células / 1,10 ha** — rede sistemática da R2 G4 |
| máscara `manchaW` | 427 px | **não existe** (retirada pela R2 G4) |
| máscara `zona0` | 220 px | **202 células / 2,02 ha**; centróide E530999 N4655102, a 27 m do centro declarado do foco ESTE |
| NDVI da referência, 2017-07-02 | 0,838 | **0,8884** |
| NDVI da referência, 2026-07-27 | 0,886 | **0,8425** |
| — âncoras novas da R2 — | | |
| pomar (G2) | 30,31 ha | **30,31 ha** |
| referência sistemática (G4) | 1,10 ha / 110 células | **1,10 ha / 110 células** |
| banda contígua (G35) | 27,30 ha | **27,30 ha** |
| total da tabela (G35) | 44,93 ha | **não verificável aqui** — 27,30 medido + 17,66 declarado sem posição = 44,96 |
| chão lavrado de 2021 | 1,67 ha | **1,67 ha / 167 células** |
| distância entre os focos | — | **496 m** |

Os dois valores de NDVI **invertem o sinal** face ao declarado, e reproduzem
exactamente a R2 G6/G25 (0,8884 → 0,8425). Não é divergência: são objectos
diferentes. Os valores da abertura são da referência antiga, escolhida por
NDVI alto na última cena; os obtidos são da rede sistemática. Registado aqui
porque o controlo 2 obriga, e porque é a confirmação mais barata de que a
camada está a ler as máscaras certas.

---

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| **G20:** «o MDT cobre o polígono; faltam-lhe os 198 m mais a leste da AOI». | O facto é verdadeiro **do ficheiro `dem_aoi.npy`**, não do acervo LiDAR. Esse ficheiro foi escrito às 10:27 de 28-08 e acaba exactamente em E3763 = −40000, o bordo direito da coluna de mosaicos 159; os mosaicos 160xxx e 161xxx só chegaram ao disco às 11:09. **Os 21 mosaicos actuais cobrem a AOI inteira**, sem uma única célula em falta. | Nada acima cai. Mas nenhuma camada precisa de aceitar a lacuna: quem quiser terreno a leste de E531500 tem-no. Esta camada não usou `dem_aoi.npy`; construiu o seu MDT dos mosaicos (`c1_03_dem50.npy`). |
| **`REGISTO_DE_NOMES.md`** atribui ao foco OESTE «válvulas 8, 9 e 10 — a 10 a 47 m do centro, a 9 a 105 m, a 8 a 157 m» e ao foco ESTE «15 a 77 m, 14 a 116 m». | Esses números vêm de `valvulas_v6.json`, que a **G35 substituiu**. Com `valvulas_por_area.json`: foco OESTE — **8 a 35 m, 9 a 98 m, 7 a 111 m, 10 a 171 m**; foco ESTE — **13 a 81 m, 14 a 93 m, 12 a 154 m, 15 a 174 m**. | A tabela da G34 («OESTE: válvulas 8 e 9; ESTE: 13 e 14») está certa; as duas tabelas do `REGISTO_DE_NOMES.md` estão desactualizadas e devem ser lidas contra `valvulas_por_area.json`. Nenhuma conclusão muda — a G35 já é a fonte operativa. |
| **A retirada térmica cita «r = −0,756»** sem dizer de quê. | É o **Spearman do foco ESTE** (`zona0` no vocabulário antigo) sozinho. O Pearson da mesma unidade é −0,769; o do foco OESTE é −0,657; o agregado dos dois é **−0,591**. | A retirada mantém-se e reforça-se (ver CONFIRMADO). Mas quem citar «−0,756» tem de dizer que é de um foco só, e não do conjunto. |
| Um declive calculado a 2,5 m dá o foco ESTE **1,45° mais inclinado** que o OESTE e o pomar **3,1° mais inclinado** que o terreno envolvente. | A essa escala, num pomar de compasso 5,0 m com sulcos e rodados, isso é **micro-relevo de cultivo, não forma de terreno**. Ao declive de **forma** (gradiente do MDT suavizado a 50 m) os focos **não se distinguem**: OESTE 0,336°, referência 0,406°, ESTE 0,427° (ESTE − referência p = 0,20, não significativo); e o pomar fica **mais plano** que o envolvente, não mais inclinado (0,449° contra 0,515°, p = 2,0e-14). Dentro do foco ESTE, as células lavradas em 2021 estão +2,29° acima das não lavradas ao micro-relevo — é lá que a diferença mora. | Nenhuma camada acima pode dizer «o foco ESTE está numa encosta». **Não está.** O que o separa é a cota, a altura sobre a drenagem e a distância à drenagem — não a inclinação. |
| `pendente_escoamento.csv`, `pendente_nivelamento.csv` e `lidar_topografia_por_mascara.csv` dão topografia e escoamento por máscara. | Os três foram calculados sobre `masks.json` — as máscaras circulares que a R2 G5 substituiu — e com o vocabulário invertido. As três estão **refeitas** aqui sobre `masks_geograficas.json`, com controlo de campanha. O sentido dos contrastes sobrevive; os valores mudam (p. ex. fracção em linha de drenagem: `zona0` 0,03 % herdado, **0,010 %** medido; referência 1,51 % herdado, **1,01 %** medido, mas a referência é outro objecto). | Usar `c1_04`, `c1_05` e `c1_11`. Os três CSV herdados ficam como histórico. |
| `pendente_bacia.csv` declara «bacia_total 49,14 ha, união de 40 exutórios». | Não é reproduzível: o ficheiro não diz quais são os 40 exutórios nem onde estão. A grandeza que esta camada mede e publica é outra — a **área contribuinte máxima que chega a uma célula do pomar, 13.891 m² (1,39 ha)**, e o máximo da janela inteira, 313.739 m² (31,37 ha). | Não é rejeição, é falta de definição. Quem quiser um número de bacia tem de nomear o exutório. |

---

## REJEITADO

| o que não sobrevive | porquê | que conclusões acima caem com ele |
|---|---|---|
| **`lidar/bacia.json`, definitivamente.** | Medido outra vez, e a R2 G21 confirma-se em todos os pontos: declara 36,9 ha; a sua *bbox* em EPSG:32629 é E530417–531057 / N4654450–4655254 = 640 × 805 m = **51,52 ha**; e cobre **59,7 %** das células do `pomar`, faltando-lhe 272 m a oeste e 468 m a leste. Foi produzido por `bacia.py`, que **não tem o passo `resolve_flats`** — e sem ele a acumulação máxima é 70 vezes menor que a real. | Qualquer afirmação sobre «a bacia do pomar» apoiada nesse ficheiro. Substituído por `c1_05_acumulacao1m.npy` e pelas grandezas de `c1_05_bacia.json`. |
| **A leitura «a lavra de 2021 mudou aquele solo».** | A assinatura de radar daquele chão **já lá estava em 2016-17**, cinco Invernos antes da ortofoto, e o teste antes/depois dá sinais opostos nas duas órbitas (−0,19 dB, p = 0,20; +0,62 dB, p = 0,009). O solo nu de 2021 está **sobre** terreno que já era distinto; não o tornou distinto. | Cai qualquer datação do contraste do foco ESTE em 2021, e cai qualquer cronologia que use a ortofoto de 2021 como marco de alteração daquele solo. A pergunta «o que aconteceu ali a meio da série» tem, no substrato, uma resposta negativa: **nada que o SAR consiga datar**. O que ali está é anterior à série. |
| **A hipótese de que o contraste de cota entre focos possa ser artefacto de campanha de voo.** | Testada e morta: os dois focos estão de facto em campanhas diferentes (Ago/2025 e Jan/2026), mas o degrau máximo medido na costura que os separa é **0,058 m** contra um contraste de **1,204 m**, e a ordenação das quatro unidades reproduz-se num sensor sem qualquer relação (GLO-30, radar). | Nenhuma. É um negativo registado, para não voltar a ser levantado sem dados novos. |
| **A linha térmica como sinal independente.** Confirmada a retirada, não reaberta. | Ver CONFIRMADO. O controlo interno, que não fazia parte do argumento original, dá o acoplamento mais forte de todos (r = −0,925): ΔT e ΔNDVI medem a mesma coisa em qualquer superfície desta AOI, não só nas manchas. | Qualquer «aquecimento da mancha» tratado como evidência independente do óptico. |

---

## NÃO TESTÁVEL

| o que não se conseguiu verificar | o que faria falta |
|---|---|
| **Se há inversão de horizontes ou uma sola de compactação.** Nenhum instrumento desta camada vê abaixo da superfície. O MDT mede a cota do solo, o SAR a rugosidade e a humidade dos primeiros centímetros, os boletins A2 a camada de amostragem. A planaridade a 60 m e o contraste químico são **compatíveis** com truncatura por terraplanagem, e não a provam: um terraço aluvial também é plano, e uma parcela alta também lixivia sem ter sido cortada. | Sondagens a trado com **descrição de horizontes** e profundidade do contacto, em pelo menos três pontos por unidade (foco OESTE, foco ESTE, referência sistemática); densidade aparente por horizonte; penetrómetro. É trabalho de campo, não de gabinete. As coordenadas dos pontos estão em `c1_16_pontos_de_sondagem.csv`. |
| **Se o CaO < 154 mg/kg é uma propriedade do bloco B3 ou daquele ponto de colheita.** Há **um único** boletim para B3. A variabilidade intra-bloco conhecida é enorme: dentro do B1, três sub-parcelas dão CaO de **314, 439 e 4700 mg/kg** — um factor de 15; e o mesmo `B2 - V7`, amostrado com três meses de intervalo, dá **264 e 505 mg/kg** e **texturas diferentes** («Franca» em Março, «Argilosa» em Junho). | Réplicas dentro de B3 — pelo menos três pontos com GPS —, e o ponto GPS de cada colheita já feita, não só o nome do bloco. A própria folha «Traceability Gaps» do livro levanta este ponto para B2-V7. |
| **Se `Erica 2016 R/E` é o bloco `Erica Novo` da tabela de válvulas.** A identificação é inferência: o sufixo «E» reaparece no boletim de nemátodes 343 como «Erica Novo E», o que reforça mas não prova. Se estiver errada, dois dos nove boletins mudam de sítio. | Confirmação do gestor: «Erica 2016» e «Erica Novo» são o mesmo bloco? |
| **Onde é que `Parcela B4` foi colhido.** O bloco B4 tem válvulas 16-17 na banda contígua **e** a parcela solta B4C3, sem posição (R2 G35). O boletim não distingue. | Idem. |
| **A química dos três boletins do B1.** B1 está fora da banda contígua; dentro dele não se sabe onde acaba cada válvula (R2 G35/G36), logo C1, C3 e C4 não têm posição. Ficam registados com a posição de conjunto do B1 e um raio de incerteza de 343 m. | O parcelário, ou pontos GPS. |
| **A profundidade do nível freático, e se ela difere entre focos.** O HAND e a distância à drenagem são *proxies* topográficos, não medições. Um contraste de 0,22 m de HAND num aluvião pode ou não corresponder a um contraste de água disponível. | Piezómetros, ou pelo menos a profundidade da água em furos existentes, com data. |
| **Se o défice de VV do foco ESTE é do solo ou da estrutura da planta.** O kiwi é caduco: no Inverno mede-se sobretudo solo, pérgola e lenho. Mas se aquele sector tiver menos lenho, ou plantas mais novas, ou compassos diferentes, isso baixa VV sem que o solo seja diferente. Esta camada não pode separar as duas coisas. | É pergunta para a C2 (estrutura do coberto) e para o campo (contagem de plantas por linha, idade). |
| **Se a queda de VV do foco OESTE no Inverno de 2025-26 é do solo ou do coberto.** Mesmo problema, agravado por um viés de selecção: o disco OESTE está centrado numa coordenada que foi escolhida por o NDVI ter caído ali. O **momento** não é circular — nove Invernos anteriores servem de controlo interno —, mas o **lugar** é. | Repetir a medição sobre uma partição do pomar que não conheça os focos (p. ex. por válvula), e ver se a válvula 8 se destaca sozinha. |
| **A temperatura do solo.** A retirada térmica fecha a porta ao LST diurno de Landsat, e não há LST nocturno nem sensores de campo neste acervo. | LST nocturno (ECOSTRESS), ou sondas no terreno. |
| **Se a precipitação distingue os focos.** Não distingue e não pode: ERA5-Land tem ~9 km, ERA5 ~28 km, CERRA ~5,5 km, e os focos estão a **496 m**. A precipitação data anos; não localiza nada. | Um udómetro na exploração. Não existe. |
| **A hidráulica da rede de rega para lá da origem única.** Confirmou-se a informação de que há uma só origem (relato do gestor, R2), e a tabela dá área por válvula. Não há pressões, caudais por sector medidos, diâmetros, nem registo de horas de rega. O esquema PRILUX de 2009 tabela caudais (65–99,9 m³, soma 1053,3) mas isso é projecto, não operação. | Registo de rega por sector, ou um ensaio de uniformidade de emissores. Sem isso, «a rega explica o padrão» não é testável em nenhum sentido. |

---

## PASSA PARA CIMA

Lista fechada. **O que não estiver aqui, não existe para as camadas acima.**
Todos os factos usam o vocabulário do `REGISTO_DE_NOMES.md`: os focos
identificam-se por coordenada.

**S1.** O MDT de trabalho desta cadeia é `SAIDA_C1\c1_03_dem50.npy` (0,5 m,
EPSG:3763, transform e shape em `c1_03_dem50.json`), construído dos 21
mosaicos DGT. **Cobre a AOI inteira**, zero células em falta no `pomar`.
`lidar/dem_aoi.npy` está incompleto a leste e não deve ser usado. *(exacta)*

**S2.** Os 21 mosaicos vêm de **quatro campanhas de voo**: 2025-08-02 (9),
2026-01-15 (8), 2026-01-14 (2), 2026-01-13 (2). O foco OESTE está no voo de
Agosto e o foco ESTE no de Janeiro. **A costura entre eles não introduz degrau
utilizável: 0,058 m contra 0,025–0,028 m de passo natural.** *(±0,06 m)*

**S3.** **O foco ESTE é o ponto alto e o foco OESTE o ponto baixo.** Cota
mediana: OESTE 6,638 m (percentil 30 do pomar), referência sistemática
6,798 m (38), ESTE 7,842 m (84), `zona0` 8,069 m (90). Diferença ESTE−OESTE
**+1,204 m**. Ordenação confirmada por Copernicus GLO-30. *(±0,06 m)*

**S4.** **E é um alto local, não o efeito do declive geral.** Contra o perfil
longitudinal do próprio pomar (+0,085 % para ENE), o foco ESTE está **+0,589 m
acima** e o OESTE **−0,198 m abaixo**. *(±0,10 m)*

**S5.** **Os focos não diferem em inclinação.** Declive de forma a 50 m: OESTE
0,336°, referência 0,406°, ESTE 0,427° (p = 0,20). Toda a parcela está abaixo
de 0,5°. Qualquer afirmação de «encosta» é falsa. O declive a 2,5 m (OESTE
4,63°, ESTE 6,08°) mede sulcos, não terreno. *(p declarado)*

**S6.** **A posição hidráulica dos dois focos é oposta.** Altura sobre a
drenagem: OESTE 0,130 m, referência 0,150 m, ESTE 0,353 m. Distância à
drenagem: **13,4 / 23,6 / 55,8 m**. Fracção sobre linha de drenagem
(≥ 2000 m²): **1,99 % / 1,01 % / 0,33 %**. O foco OESTE recebe água
concentrada, o foco ESTE não recebe nenhuma. *(limiar declarado)*

**S7.** **`lidar/bacia.json` está morto.** Ver REJEITADO. Qualquer
encaminhamento de escoamento neste MDT tem de passar por `resolve_flats`: sem
ele a acumulação máxima é 70 vezes menor. *(exacta)*

**S8.** **O bloco do foco ESTE (B3, válvulas 12-15) tem o solo mais pobre da
exploração**: CaO < 154 mg/kg (abaixo da detecção), MgO 36,0, K₂O 74,7,
P₂O₅ 107, C:N 5,9, pH 5,6 — mínimo de nove boletins em cinco de sete
parâmetros. **Os vizinhos imediatos são muito mais ricos**: `Erica Novo`
(válvulas 10-11) CaO 879 e 1200; `B4` (válvulas 16-17) CaO 1100. **É um
buraco, não um gradiente.** *(n = 1 boletim — ver S9)*

**S9.** **Um boletim não caracteriza um bloco.** Dentro do B1, três
sub-parcelas dão CaO 314, 439 e 4700 mg/kg. O mesmo `B2 - V7`, a três meses de
distância, dá CaO 264 e 505 **e texturas diferentes** («Franca» / «Argilosa»).
Nenhuma diferença química entre blocos abaixo de um factor de 2 é
interpretável com estes dados. *(declarado)*

**S10.** **O bloco do foco OESTE está confirmadamente carente de cálcio, por
duas matrizes.** Solo em `B2 - V7` (válvula 7, a 111 m do foco): CaO 264 e
505 mg/kg. Folha do mesmo bloco, Junho/2026: **Ca 2,2 % contra referência
3–4,7 %, «Baixo»**. Não existe análise foliar para o B3. *(leitura directa)*

**S11.** **A colocação por área da R2 G35 reproduz-se**: banda contígua
27,30 ha; válvula 8 a 35 m do foco OESTE; válvulas 13 (81 m) e 14 (93 m) as
mais próximas do foco ESTE. As tabelas de válvulas do `REGISTO_DE_NOMES.md`
estão desactualizadas — usar `valvulas_por_area.json`. *(±10 m sobre a G35)*

**S12.** **O chão lavrado de 2021 (1,67 ha) está 60 % dentro do foco ESTE e 0 %
no foco OESTE e na referência.** 45,0 % do polígono `zona0` é chão lavrado. As
66 células restantes são contíguas, a E530835–531165, ainda em B3. *(±1 célula)*

**S13.** **A distinção física daquele chão é anterior a 2021.** Em VV de
Sentinel-1 está 1,2 a 3,5 dB abaixo da referência em **todos os dez Invernos
desde 2016-17**, e o teste antes/depois da ortofoto dá sinais opostos nas duas
órbitas. **A lavra de 2021 não criou o contraste.** *(±0,3 dB)*

**S14.** **Lavra e foco são dois sinais separáveis.** Lavrado menos não
lavrado, dentro do foco ESTE: −0,856 e −0,854 dB nas duas órbitas. A parte não
lavrada do foco ESTE está a −0,77 / −0,56 dB da referência: o foco tem
assinatura própria para lá da lavra. *(±0,2 dB)*

**S15.** **No radar, o foco ESTE está sempre abaixo da referência e o foco
OESTE nunca esteve — até ao Inverno de 2025-26.** ESTE: −0,95 a −1,11 dB, as
duas órbitas, os dez Invernos, p entre 1e-6 e 1e-8, mesmo sinal em 83–97 % das
cenas. OESTE: −0,10 a −0,19 dB, não significativo na órbita 125 (p = 0,27).
**No Inverno de 2025-26 o foco OESTE cai para −1,107 dB (órbita 125) e
−0,774 dB (órbita 147) contra o pomar inteiro — o maior desvio da série nas
duas órbitas — enquanto o pomar inteiro está no seu menor desvio.** *(±0,25 dB)*
**Cuidado ao usar:** o *momento* não é circular, mas o *lugar* é — o disco
OESTE está centrado onde o NDVI caiu. Ver NÃO TESTÁVEL.

**S16.** **A precipitação está certificada como série anual e é inútil como
discriminante espacial.** `pendente_precipitacao.csv` reproduzido a 0,00 mm;
ordenação confirmada por ERA5 (Spearman +0,927) e CERRA (+0,900). Inverno mais
seco 2021-22 (663,6 mm); mais húmidos 2022-23 (1809,3) e 2023-24 (1807,8);
2024-25 = 1156,7 mm. **Nenhum produto disponível resolve 496 m: a precipitação
não pode explicar diferença entre focos.** *(±25 mm)*

**S17.** **A linha térmica fica retirada.** ΔT e ΔNDVI da mesma cena Landsat
correlacionam a −0,591 (agregado), −0,769 (foco ESTE), −0,657 (foco OESTE) — e
a **−0,925 no controlo interno fora do pomar**, o que mostra que o acoplamento
é genérico da superfície. O «r = −0,756» que circula é o Spearman do foco ESTE
sozinho. **Não ressuscitar sem LST nocturno ou temperatura de solo medida.**
*(r declarado)*

**S18.** **O pomar é duas vezes mais plano que o envolvente à escala da
parcela** (resíduo de plano em janelas de 60 m: 0,0355 m contra 0,0703 m,
p = 3,2e-10) e ligeiramente mais plano à escala de forma. **Compatível com
terraplanagem de emparcelamento; não é prova, e a truncatura de horizontes
continua por medir.** *(±0,01 m)*

**S19.** **A rugosidade a 25 m do foco ESTE excede a referência mesmo dentro
da mesma campanha de voo** (+0,0379 m, p = 1,3e-18); a do foco OESTE não
(+0,0016 m, p = 0,058). O viés entre campanhas é 0,0073 m. *(±0,008 m)*

**S20. Síntese, e é o que esta camada existe para responder.** **Os dois focos
têm substratos opostos em todas as variáveis que os separam.** O foco ESTE é
alto, afastado da drenagem, sem escoamento a chegar-lhe, com o solo mais
pobre em bases da exploração, com o micro-relevo mais rugoso, com retrodifusão
de Inverno permanentemente baixa desde 2016, e com 40 % da sua área lavrada em
2021 sobre terreno que já era distinto antes disso. O foco OESTE é baixo, sobre
linhas de drenagem, com o dobro da água concentrada da referência,
indistinguível dela em terreno, em rugosidade e em radar durante nove
Invernos — e chega ao Inverno de 2025-26 com o maior défice de radar da série.
**Não há uma única variável de substrato em que os dois focos se pareçam.**
Qualquer explicação única para os dois tem de sobreviver a isto. *(consequência
de S3–S6, S8, S12–S15, S19)*

---

## Entregas desta camada

```
_VALIDACAO_CAMADAS\
  CAMADA_1_CERTIFICADO.md        este ficheiro
  CAMADA_2_PROMPT.md             prompt da camada seguinte
  SAIDA_C1\
    c1_00_comum.py               geometria herdada, discos dos focos, máscaras
    c1_01_lidar_inventario.py    cobertura dos 21 mosaicos, que mosaico toca cada foco
    c1_02_costura.py             campanhas de voo e ensaio de costura
    c1_03_mdt.py                 MDT próprio a 0,5 m; cota, declive, TPI, rugosidade
    c1_04_focos_terreno.py       terreno por unidade + controlo de campanha + nu2021
    c1_05_bacia.py               bacia.json medido e rejeitado; pysheds com resolve_flats
    c1_06_solo_no_mapa.py        os 9 boletins A2 ligados a posição, com confiança
    c1_07_termico.py             verificação da retirada térmica
    c1_08_clima.py               precipitação contra ERA5 e CERRA
    c1_09_sar.py                 Sentinel-1 três Invernos, máscaras geográficas
    c1_10_nivelamento.py         GLO-30, nu2021 dentro do foco, planaridade
    c1_11_escalas.py             declive de forma a 50 m, HAND, distância à drenagem
    c1_12_sar_lavrado.py         lavra separada do foco, unidades disjuntas
    c1_13_sar_antes_depois.py    441 cenas, dez Invernos, antes/depois de 2021
    c1_14_ancoras.py             as quantidades-âncora
    c1_15_figuras.py             F1-F4
    c1_16_pontos_de_sondagem.py  pontos propostos para a validação de campo
    C1_F1_substrato.png          cota, HAND e chão lavrado no mapa
    C1_F2_quimica_no_mapa.png    os boletins A2 georreferenciados
    C1_F3_sar_invernos.png       dez Invernos de VV por unidade
    C1_F4_contraste.png          sinopse do contraste entre focos
    c1_*.json / .csv / .npy      resultados intermédios
```

Nada em `ganfei_s2\` foi modificado.
