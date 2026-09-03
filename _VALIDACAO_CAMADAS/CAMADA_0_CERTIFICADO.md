# Camada 0 — Geometria e proveniência · CERTIFICADO

**Não há paragem de linha.** Nada do que se mediu invalida a análise inteira.
Há um erro de escala que invalida a colocação das válvulas, uma circularidade
de fundação que enviesa (mas não anula) a medição do sinal, e uma regra de
fenologia que não se sustenta. Tudo isso está abaixo, com o cálculo que o prova.

Sessão C0, 28-08-2026. Código em `SAIDA_C0\`. Cada facto nomeia o script que o
produz; todos correm de novo sem estado escondido.

**Contaminação a declarar.** Numa pesquisa de texto por `sentinel_b1` (tarefa 5)
o resultado devolveu linhas de `AUDITORIA_COWORK_2026-08-28.md` que contêm
conclusões de camadas acima — sobre a exclusão de falha de fonte, sobre o
comportamento do bloco «B1» em Ago/2025, e sobre números do dossiê. Foram lidas
sem intenção. Nenhum facto deste certificado se apoia nelas; onde um número
dessas linhas coincide com um número medido aqui, o medido é o que vale, e
está dito qual é o cálculo. Não abri o dossiê, as figuras F1–F7, nem qualquer
PNG/SVG de saída. Li apenas os dois scripts que a tarefa nomeia
(`m1_valvulas.py`, `m2_declinio.py`) e os scripts de construção de máscaras.

---

## CONFIRMADO

| facto | ficheiro e cálculo que o prova | margem de erro |
|---|---|---|
| A AOI é (529950, 4654600, 531950, 4655600) em EPSG:32629. Os 11 GeoTIFF da série principal têm todos exactamente esses limites, 200×100 píxeis de 10 m, mesmo CRS e mesma transformação afim. | `c0_01_rasters.py` — leitura de `ds.bounds`, `ds.transform`, `ds.crs`, `ds.shape` de cada um dos 11 ficheiros e comparação com a primeira | exacta (0 m) |
| A AOI contém o polígono `pomar` inteiro, com folga em todos os lados. O polígono ocupa E 530145–531525, N 4654865–4655465; sobram 195 m a oeste, 425 m a leste, 265 m a sul, 135 m a norte. | `c0_11_assuncoes.py` §e — rasterização do polígono e extremos em UTM | ±10 m (1 píxel) |
| Alargando a janela 700 m em cada direcção não aparece copado cortado pela AOI. Fracção de NDVI>0,78 na faixa de 100 m dentro/fora de cada bordo: oeste 44,9/23,6 %, este 1,0/9,1 %, sul 28,8/32,4 %, norte 29,3/34,3 %. O que existe fora a sul e a este são campos e mata, não pomar com rede (verificado na ortofoto). | `c0_11_assuncoes.py` §f + `c0_11_aoi_alargada_ndvi.png` + `c0_09_rede_2025.png` | qualitativa |
| As 11 cenas existem no catálogo Earth Search, o identificador bate com a data do ficheiro em todas, e a AOI cai dentro do *footprint* de todas. | `c0_03_proveniencia.py` — pedido `GET /items/{id}` a cada uma; comparação de `properties.datetime[:10]` e teste ponto-em-polígono do `geometry` | exacta |
| A série é radiometricamente comparável. Dez cenas têm `earthsearch:boa_offset_applied = True`; 2017-07-02 tem baseline 00.01, anterior ao *offset* BOA, e por isso `False` — não há nada a aplicar. Verificado empiricamente, e não só pelos metadados: em 7637 píxeis classificados SCL 5 (sem vegetação) comuns a sete datas, o NDVI vale 0,236 (2017), 0,239 (2018), 0,229 (2020), 0,241 (2021), 0,212 (2022), 0,228 (2023), 0,215 (2026). Não há degrau em 2022. | `c0_03_proveniencia.py` (metadados) e `c0_04_cena2017.py` §d (alvos estáveis escolhidos pelo SCL, não adivinhados) | ±0,015 NDVI sobre alvo estável |
| Nenhuma cena tem contaminação de nuvem dentro do polígono `pomar`: a fracção de NaN dentro do polígono é 0,000 % nas 11 datas. Só 2017-07-02 tem NaN na cena inteira (0,18 %), fora do polígono. | `c0_01_rasters.py` — `np.isnan(arr[mascara]).mean()` por data | exacta |
| As duas contagens de máscara **estão as duas certas** e medem objectos diferentes. As da prosa (pomar 2906, saudável 446, manchaW 423, zona0 219) são as máscaras booleanas de `fazer_masks_v2.py`; as operativas (2903, 454, 427, 220) são o contorno dessas máscaras, simplificado e depois rasterizado. Reproduzi as duas a partir da cena de 2026 e batem ao píxel. | `c0_02_mascaras.py` §2 — reexecução integral do pipeline de `fazer_masks_v2.py` e rasterização de `masks.json` | exacta |
| As máscaras são geográficas e estáticas: são polígonos em coordenadas de píxel, iguais em todas as datas. Nenhuma é re-derivada por data. `saudavel`, `saudavel_2` e `saudavel_3` estão 100 % dentro de `pomar` e não se intersectam com `manchaW` nem com `zona0`. | `c0_02_mascaras.py` §1 e §3 | exacta |
| **A referência sã não está a descer.** Declive do NDVI médio da união das três manchas: +0,0038/ano nas 9 cenas de plena estação (p = 0,13, r² = 0,30) e +0,0026/ano nas 11 (p = 0,21). Não é significativo em nenhum dos dois casos. O défice **não** está a ser subestimado por essa via. | `c0_02_mascaras.py` §5 — `scipy.stats.linregress` sobre `nanmean(nd[saudavel_uniao])` | p declarado |
| O eixo real da parcela é WSW–ENE, azimute 70,0°. Extensão 1445 m ao longo do eixo, 328 m na transversal; centróide E530791 N4655130. | `c0_11_assuncoes.py` §e — SVD dos centros dos 2903 píxeis do polígono | ±10 m; azimute ±1° |
| **O esquema de rega tem escala declarada e é um plano CAD, não um esboço.** O bloco de título lê-se: `SISTEMA DE REGA PARA ESPAÇOS VERDES`, `Local da Obra: Valença – Minho`, `Requerente: Dr. Fausto`, `Sistema de rega automatizado para kiwis`, `LEVANTAMENTO: -`, `DESENHADOR: Tiago Pereira`, `VERIFICOU: Dante Faria`, `DATA: JUL 09`, **`ESC: 1/3500 @ A1`**, `PROCESSO: RKTV_12/08`, PRILUX. As anotações a mão estão por cima de uma base impressa. | `c0_rega_D_titulo.png` (recorte a 600 dpi do PDF) | leitura directa |
| **E é proporcional.** A moldura do desenho mede 285,2 mm na folha digitalizada; se corresponder à moldura A1 (811–841 mm), a redução é ×2,84–2,95 e a escala efectiva 1:9950–1:10320, ou seja 0,842–0,874 m por píxel de um render a 300 dpi. A esse metro, o troço ESTE do «Limites do terreno» (x ≥ 1450) mede 1468–1523 m de comprimento e 290–300 m de largura, contra 1445 m e 328 m medidos na parcela: erro de +1,6 a +5,4 % no comprimento e −8 a −12 % na largura. | `c0_08_esquema_medir.py` (moldura) e `c0_12_ajuste_esquema.py` (PCA por troço e comparação) | ±3 % no comprimento |
| A folha **não** está com o norte para cima. O eixo do troço ESTE do desenho faz −13,1° com a horizontal da folha; a parcela medida faz +20,0° com E–W. A rotação é de +33,05°. | `c0_12_ajuste_esquema.py` | ±1,5° |
| Georreferenciação por ajuste de forma (escala 0,8290 m/px a 300 dpi, rotação +33,05°, origem = centróide do troço ESTE sobre o centróide do `pomar`). Nenhum parâmetro vem de indicação verbal. | `c0_13_georref.py` + `c0_13_georref.json` | resíduo mediano 64 m, p90 110 m — ver NÃO TESTÁVEL |
| **A escala usada em `m1_valvulas.py` está 30 % errada.** As duas âncoras dão 1,0787 m por unidade de esboço; o ajuste de forma dá 0,8290 e a escala declarada pelo próprio desenho dá 0,842–0,874. A unidade de esboço é o píxel de um render a 300 dpi do PDF — confirmado porque o desenho ocupa x = 138–3206 nesse render e os valores `X_MW = 1900`, `X_Z0 = 2370`, `VALVULAS x = 1990…2700` caem todos lá dentro. | `c0_07_vista_larga.py` e `c0_12_ajuste_esquema.py` | +30,1 % contra o ajuste; +23 a +28 % contra a escala declarada |
| **Está provado como nasceu o erro da AOI «b1».** Com a escala das âncoras, `Ev(x) = 530492 + (x − 1900) × 1,0787`. O extremo oeste do desenho (x = 138) vai para E528591 e o extremo este (x = 3206) para E531901: um terreno de 3310 m, contra os 1445 m medidos. As válvulas 1–5 anunciadas em E528634–529088 correspondem a x = 178–598, que é exactamente o lóbulo oeste do desenho. A AOI `b1` é 528400–529400. O erro é de escala, propagado por extrapolação para o extremo do desenho. | `c0_07_vista_larga.py` — aritmética explícita, com os x medidos na máscara rosa | exacta |
| A AOI `b1` (528400, 4654900, 529400, 4655700) não contém pomar. SCL da cena de 2026: 62,85 % vegetação, 37,15 % sem vegetação, 0 % água — é tecido urbano de Valença com arvoredo, como se vê na ortofoto DGT de 2025 que a cobre. Não se sobrepõe à AOI principal (550 m de intervalo em E, 0 ha de sobreposição). Dista 745 m da caixa ao ponto mais próximo do polígono `pomar`; do seu centro ao polígono são 1281 m, e centróide a centróide 1996 m. | `c0_10_quarentena_b1.py` §a, `c0_01_rasters.py`, `c0_11_assuncoes.py` §d | ±20 m |
| Inventário fechado do que deriva da AOI `b1`: 49 ficheiros, listados em `SAIDA_C0\c0_10_inventario_b1.csv`. Inclui 22 GeoTIFF + 2 `proveniencia_b1.json` (duas cópias: `ganfei_s2\sentinel_b1\` e `_GANFEI_REEXECUCAO_CEGA\dados\sentinel_b1\`), os scripts `b1_serie.py`, `b1_analise.py`, `b1_nucleo_interno.py` (e a cópia em `_pacote_cowork\`), `q5.py`, `variantes_a.py`, `figuras.py`, `inspeccao.py`, e os CSV `expansao_b1.csv` (9 colunas, 11 linhas), `b1_nucleo_serie.csv` (5 colunas), `Q5_b1.csv` (9 colunas), todos com a constante `area_bloco_ha = 7,88`. **Nada foi apagado.** | `c0_10_quarentena_b1.py` §b | inventário completo dentro de `ganfei_s2\` e `_GANFEI_REEXECUCAO_CEGA\` |
| As coordenadas do traço de 1995 são internamente consistentes e apontam para uma feição real. Os 7 pontos de `tracos_1995_coordenadas.csv` caem todos dentro do polígono `pomar`; as três representações (UTM29N, PT-TM06, WGS84) fecham a ≤0,1 m; e a ortofoto de 1995 mostra uma feição linear E–W ao longo do L1 declarado, em N ≈ 4655047. | `c0_11_assuncoes.py` §b e `c0_14_lobo_oeste_e_1995.py` §b + `c0_14_traco1995.png` | ±10 m na leitura da imagem |
| **A classificação «já em défice na primeira cena» não é artefacto da data escolhida.** Repetindo a regra da M2 com cada uma das cinco cenas limpas de 2017 (02-07, 12-07, 11-08, 18-08, 31-08), a área dá 8,21 / 7,88 / 7,83 / 8,20 / 7,65 ha. A fracção do pomar em défice na primeira cena dá 29,4 / 28,1 / 29,9 / 30,8 / 29,7 %. | `c0_04_cena2017.py` §c e §c2 — cenas alternativas descarregadas do AWS e recalculadas com o mesmo método | ±0,6 ha entre datas |
| **Houve alteração física do coberto entre 2021 e 2025** — confirmado por medição independente. Na janela E530550–531200 / N4654930–4655300, a fracção de píxeis com luminância > 170 vale 5,1 % (2010), 2,3 % (2021) e 16,4 % (2025); a luminância média sobe 105,5 → 115,1 → 132,6 e o percentil 90 sobe 140,7 → 147,0 → 213,3. Os valores absolutos diferem dos citados na ADENDA (8/9/21 %) porque o limiar e a reamostragem são outros; a direcção e a magnitude do salto 2021→2025 são as mesmas. | `c0_09_copado_orto.py` §3 — ortofotos DGT de 2010, 2021 e 2025 lidas a 0,5 m na mesma janela | limiar declarado |
| O MDT LiDAR `lidar/dem_aoi.json` (EPSG:3763, 0,5 m, 1812×1020 m) cobre o polígono `pomar` inteiro, mas **não** cobre os 198 m mais a leste da AOI Sentinel. O `t2_dem1m.json` (5908×3683 m) cobre tudo. | `c0_11_assuncoes.py` §a e `c0_16_bloco_sw.py` §b — transformação dos cantos para 3763 com `pyproj` | exacta |
| A janela do esquema mostra as válvulas em **duas filas**, uma a norte e outra a sul de uma conduta desenhada a preto, e os sectores como **faixas transversais** ao eixo da parcela, com nomes de letra (Sector A a N, sem K) e caudais tabelados (65 a 99,9 m³, soma 1053,3). Foram detectados 13 anéis de válvula no desenho; a numeração legível vai até 18. | `c0_rega_B_centro.png`, `c0_rega_C_direita.png`, `c0_rega_E_legenda.png`, `c0_08_esquema_medir.py` | leitura directa |
| **Existe um bloco de pomar com rede a sudoeste, fora da AOI, com 16,4 ha.** Na janela E529350–530150 / N4653700–4654550 a assinatura de coberto claro com textura de linhas dá 15,77 + 0,59 = 16,36 ha. O bordo norte dessa janela (N4654550) fica abaixo do bordo sul da AOI (N4654600): o bloco nunca esteve dentro de nenhuma AOI usada. | `c0_16_bloco_sw.py` §a + `c0_09_rede_2025.png` | ±2 ha (o detector inclui caminhos) |

---

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| «O *Esquema de rega retificado* é um desenho à mão SEM coordenadas e NÃO é proporcional» (`m1_valvulas.py`, docstring). | É um plano CAD da PRILUX, Julho de 2009, à escala declarada **1/3500 @ A1**, com legenda, tabela de caudais e bloco de título. As anotações a mão estão por cima. O troço este bate com a parcela medida a 2–5 % no comprimento. | Cai a justificação para colocar as válvulas por âncoras verbais. A colocação passa a ser um ajuste de forma medido, com resíduo declarado. Qualquer camada acima que tenha assumido «não há geometria utilizável no esquema» tem de reabrir essa suposição. |
| «Incerteza declarada: ±40 m nas fronteiras de sector» (`m1_valvulas.py`). | A escala das âncoras está 30 % acima da real. Sobre os 710 px que separam as válvulas 6 e 13, isso são 766 m em vez de 598–620 m: um erro relativo de ~150 m entre extremos. A colocação por ajuste de forma tem resíduo mediano de 64 m e p90 de 110 m. A incerteza honesta é **±60 a 100 m**, não ±40. | Nenhum núcleo de declínio pode ser atribuído a uma válvula ou a um sector com a informação actual. Toda a afirmação do tipo «o foco está no sector X» cai. |
| As fronteiras de sector foram desenhadas como linhas verticais N–S (`m1_valvulas.py`, `ax.plot([E, E], [W[1], W[3]])`; idem em `m2_declinio.py`). | O eixo da parcela é o azimute 70°. As fronteiras do esquema são perpendiculares a esse eixo, ou seja azimute 160°. Sobre uma parcela de 328 m de largura, um erro angular de 20° desloca uma fronteira ±60 m nos bordos norte e sul. | Confirma a crítica da gestora. As fronteiras antigas erram por escala **e** por ângulo, e os dois erros somam-se. |
| A prosa citou contagens de máscara (2906/446/423/219) diferentes das operativas (2903/454/427/220), e isso foi registado como defeito. | Não é defeito: são dois objectos. Os primeiros são as máscaras booleanas de `fazer_masks_v2.py`; os segundos são o contorno simplificado (`measure.approximate_polygon`) rasterizado. Reproduzi os dois exactamente. **A ressalva que fica**: o polígono `saudavel` tem 454 px contra 446 da booleana, ou seja acrescenta 8 píxeis (+1,8 %) que **não** passaram nos critérios de origem (`copado`, `interior`, `longe`). | O «defeito conhecido» deve ser reetiquetado como diferença de definição, não como incoerência. Os 8 píxeis extra da referência ficam registados. |
| `lidar/bacia.json` declara `"ha": 36.9`. | A caixa `bbox_wgs84` desse ficheiro mede 640 × 805 m = **51,5 ha**, e **não cobre o polígono `pomar`**: falta-lhe 272 m a oeste, 468 m a leste e 211 m a norte. O valor 36,9 não é a área da caixa. Note-se que 29,03 (pomar) + 7,88 (bloco «b1», em quarentena) = 36,91. | A C1 não pode usar `bacia.json` como está. Ou o 36,9 tem outra origem que não está no ficheiro, ou herdou o bloco em quarentena. Tem de ser redelineado. |
| «O viveiro (válvulas 22–23) e a B3C3 (válvula 27) ficam fora desta imagem» (pergunta 5 da M1 v1). | O esquema desenha um viveiro **dentro** da parcela, no terço centro-leste, marcado a laranja com a palavra VIVEIRO e a azul com «1 ha», sobre uma faixa estreita entre as válvulas 19 e 12 do desenho. Pode ser outro viveiro; mas a pergunta como estava formulada já assumia a resposta. | A pergunta tem de ser reformulada sem pressupor a localização. Feito na M1 v2. |
| A M2 pintava 8,21 ha de cinzento com a legenda «nunca esteve são desde 2017 — não é declínio, é falha de copado». | A **medição** sobrevive: 8,21 ha estavam abaixo da referência menos 0,05 já na primeira cena, e o valor é robusto à escolha da cena de 2017 (7,65–8,21 ha). A **interpretação** não sobrevive: a ortofoto de 2025 a 25 cm mostra linhas de pomar contínuas nessa área, Não são caminhos nem falhas. (Nota lateral, medida numa janela só: na ortofoto de 1995, em E530250–530700 / N4654950–4655220, não há estrutura de linhas de pomar — era campo aberto. Isso é sobre essa janela, não sobre os 8,21 ha.) | A cronologia do caso muda de sentido. Se aquela área já estava em défice em 2017, o declínio começou **antes** do início da série, e a série de satélite não consegue datar o início. A M2 v2 substitui a classe por «já em défice na primeira cena (2017) — início NÃO datável». |
| A distância «1,06 km» entre o corpo principal e o lóbulo oeste. | Não é reproduzível por nenhuma medida geométrica: caixa a polígono 745 m, centro da AOI b1 ao ponto mais próximo do polígono 1281 m, centróide a centróide 1996 m, intervalo entre AOI 550 m. | Retirar o número. Não substituir por outro: a entidade que ele media não existe. |

---

## REJEITADO

| o que não sobrevive | porquê | que conclusões acima caem com ele |
|---|---|---|
| **Tudo o que deriva de `sentinel_b1/`.** As 22 imagens, os três CSV (`expansao_b1.csv`, `b1_nucleo_serie.csv`, `Q5_b1.csv`), os scripts `b1_serie.py`, `b1_analise.py`, `b1_nucleo_interno.py`, `q5.py`, e a constante `area_bloco_ha = 7,88`. | A AOI mede tecido urbano de Valença (SCL: 63 % vegetação de jardim/arvoredo, 37 % sem vegetação, 0 % água), a 745–1996 m do pomar, sem sobreposição com a AOI de estudo, com o rio Minho entre as duas. Não contém pomar. | Cai qualquer «bloco de controlo são», qualquer série de referência externa, qualquer declive calculado sobre ela, e qualquer exclusão ou confirmação que se tenha apoiado no comportamento do «B1». Uma exclusão apoiada num bloco que não existe não é uma exclusão. |
| A escala de 1,0787 m por unidade de esboço, e com ela a posição das válvulas 6–13 e todas as fronteiras de sector da M1 v1 e da M2 v1. | +30,1 % contra o ajuste de forma medido e +23 a +28 % contra a escala que o próprio desenho declara. As duas âncoras verbais que a geram são mutuamente inconsistentes com a métrica do desenho. | Cai toda a atribuição de núcleos a válvulas ou a sectores. Cai a afirmação de que as válvulas 1–5 e 14–17 «não são colocáveis» **por o desenho não ser proporcional** — a razão era outra. |
| A distância «1,06 km». | Ver CORRIGIDO. | Qualquer argumento de proximidade ou de gradiente espacial construído sobre ela. |
| A interpretação «falha de copado / caminhos / outra cultura» dos 8,21 ha. | Ortofoto DGT 2025 a 25 cm: linhas de pomar contínuas em toda a área. | Cai a subtracção desses 8,21 ha da área em declínio, e cai a datação do início do declínio em 2017 ou depois. |
| **A regra de fenologia como está aplicada.** Excluem-se 2019-09-02 (dia 245) e 2025-06-17 (dia 168), mas mantém-se 2018-08-31 (dia **243**) — dois dias antes da que se exclui — e mantém-se 2017-07-02 (dia 183), quinze dias depois da que se exclui. As nove datas «de plena estação» cobrem 60 dias de calendário. | Uma regra que separa o dia 243 do dia 245 e junta o dia 183 com o dia 243 não é uma regra; é uma escolha *a posteriori*. | Não invalida a série, mas invalida a justificação dada para a composição dela. Qualquer camada que trate «as nove cenas de plena estação» como um conjunto fenologicamente homogéneo está a assumir o que não foi demonstrado. |
| A incerteza declarada de ±40 m. | Ver CORRIGIDO. | Toda a leitura conjunta M1×M2 que dependa de as fronteiras estarem a ±40 m. |

---

## NÃO TESTÁVEL

| o que não se conseguiu verificar | o que faria falta para verificar |
|---|---|
| **Se o bloco de 16,4 ha a sudoeste (E529350–530085, N4653700–4654478) pertence à exploração.** O troço OESTE do esquema, georreferenciado pelo ajuste do troço ESTE, cai sobre ele (centróide E529796 N4654111, extensão 389×506 m), e o bloco tem a mesma assinatura de rede. Mas é uma extrapolação de ~1200 px além do troço ajustado, com erro de ordem ±150 m; e a assinatura de rede não prova propriedade. A coincidência com a lacuna de área (44,9 − 29,0 = 15,9 ha, contra 16,4 ha medidos) é forte mas não é prova. | A tabela de válvulas com áreas (nunca a vi), ou a confirmação da gestora sobre a M1 v2 (pergunta 3), ou o parcelário. |
| **Onde estão exactamente as ~16 ha que faltam para as 44,9 ha.** O bloco sudoeste é o candidato medido. Dentro da AOI, fora do polígono `pomar`, há 13,36 ha com assinatura de coberto claro e textura de linhas, mas esse número inclui caminhos, estufas e edifícios e é um limite superior; não consegui separá-los de forma fiável. | A tabela de 27 válvulas com áreas por sector, e a resposta à pergunta 5 da M1 v2. |
| **Quanto copado em declínio ficou de fora da máscara `pomar`.** A máscara é semeada por `nd2026 > 0,78` (`fazer_masks_v2.py`), logo copado que já tivesse descido abaixo desse limiar em 2026 e não fosse recuperado pelo fecho morfológico está excluído por construção. 4,87 ha do polígono não têm assinatura de rede na ortofoto, e 29,9 % do polígono tem NDVI ≤ 0,78 em 2026 (recuperados pelo fecho). Não consegui quantificar o que ficou fora. | Redesenhar `pomar` a partir da ortofoto de 25 cm ou do parcelário, e não do NDVI. É uma tarefa da C0 que fica por fazer, e devia ser feita antes de a C2 medir áreas. |
| **A numeração das válvulas.** Detectei 13 anéis; o desenho mostra pelo menos 18 números, e as notas manuscritas referem-se a válvulas 19 a 27, ao viveiro e à B3C3, que não estão no desenho. Não consigo ler os números com fiabilidade suficiente para os pôr num mapa. | A gestora, sobre a M1 v2. Ou uma digitalização do esquema a resolução maior. |
| **Se o «Limites do terreno» desenhado é o limite cadastral.** O bloco de título diz `LEVANTAMENTO: -`: não houve levantamento. O contorno pode ser decalcado de cartografia ou desenhado à vista. O resíduo mediano de 64 m entre o contorno desenhado e o polígono medido é compatível com qualquer das duas hipóteses (e também com o facto de os dois objectos serem diferentes: um é o terreno, o outro é o copado). | Cartografia cadastral, ou um levantamento GPS de dois ou três vértices. |
| **A proveniência das coordenadas do traço de 1995.** Confirmei que são internamente consistentes e que apontam para uma feição visível na ortofoto de 1995. Não sei quem as mediu, com que método, nem porquê. Os dois pontos `REF_` diferem dos centróides medidos das máscaras em 24 m (manchaW) e 11 m (zona0), o que sugere que são aproximações a olho e não medições. | O registo de quem produziu o CSV. |
| **O que é o valor 36,9 ha em `lidar/bacia.json`.** Não é a área da *bbox* (51,5 ha), e a *bbox* não cobre o pomar. | Redelinear a bacia a partir do MDT, na C1. |
| **Por que razão a referência sã é seis vezes mais dispersa em 2017 do que depois.** Desvio-padrão do NDVI da referência: 0,111 em 2017-07-02, contra 0,014–0,040 em 2018–2026, com 43 dos 454 píxeis abaixo de 0,70. Não é artefacto da data: as outras quatro cenas de 2017 dão 0,065–0,099, também muito acima das seguintes. Não é nuvem (0 % de NaN no polígono). | Não é pergunta da C0 responder porquê. É facto medido e passa para cima como tal. |
| **Se a AOI corta pomar a leste, para lá de E531800.** As sete ortofotos DGT terminam em E531800; a AOI vai até 531950. Verifiquei essa faixa só com Sentinel a 10 m, onde não se distingue pomar com rede de outra vegetação. O polígono `pomar` acaba em E531525, 275 m antes do fim da cobertura de ortofoto, portanto o polígono está coberto — a lacuna é só nos 150 m finais da AOI, onde o polígono não chega. | Ortofoto da folha seguinte a leste. |

---

## PASSA PARA CIMA

Lista fechada. **O que não estiver aqui, não existe para as camadas acima.**

**G1.** A AOI de estudo é (529950, 4654600, 531950, 4655600) em EPSG:32629, grelha de 10 m, 200×100 píxeis. As 11 imagens partilham exactamente essa grelha. *(exacta)*

**G2.** O polígono `pomar` tem 2903 píxeis = **29,03 ha**, ocupa E 530145–531525 / N 4654865–4655465, e está inteiramente dentro da AOI com ≥135 m de folga em qualquer direcção. *(±10 m no contorno)*

**G3.** O eixo maior da parcela é o **azimute 70,0°** (WSW–ENE); comprimento 1445 m, largura 328 m, centróide E530791 N4655130. Qualquer fronteira transversal defensável é perpendicular a esse eixo, isto é azimute 160°. *(azimute ±1°, comprimento ±10 m)*

**G4.** Áreas das máscaras, na definição operativa (polígono rasterizado): `pomar` 29,03 ha · `saudavel`+`saudavel_2`+`saudavel_3` **4,54 ha** (2,64 + 1,19 + 0,71) · `manchaW` **4,27 ha** · `zona0` **2,20 ha**. Todas dentro de `pomar` (manchaW e zona0 com 1 píxel fora cada). Nenhuma se intersecta com as outras. *(±1 píxel na fronteira = ±0,01 ha por píxel de bordo)*

**G5.** As máscaras são estáticas: os mesmos polígonos em todas as datas. **Mas duas delas são circulares em relação ao NDVI que depois se mede**, e isto é obrigatório passar adiante: `pomar` é semeada por `nd2026 > 0,78`; `saudavel×3` exige `nd2026 > 0,78` (via `copado`); `manchaW` é `nd2026 < 0,76` dilatada por um disco de 3 px. Só `zona0` é um polígono geográfico traçado à mão e intersectado com `pomar`. *(facto de código, `fazer_masks_v2.py`, reproduzido em `c0_02_mascaras.py`)*

**G6.** A referência sã **não desce**: +0,0038 NDVI/ano (9 cenas de plena estação, p = 0,13) e +0,0026 (11 cenas, p = 0,21). O défice não está a ser subestimado por deriva da referência. Mas a referência foi escolhida por ter NDVI alto **na última cena da série**, o que a enviesa para cima no fim — a magnitude desse enviesamento não foi quantificada. *(p declarado)*

**G7.** A série é radiometricamente comparável ao longo do tempo, verificado em alvos estáveis e não só nos metadados: NDVI de 0,212 a 0,241 sobre 7637 píxeis SCL 5 comuns a sete datas, sem degrau em 2022. *(±0,015 NDVI)*

**G8.** Nenhuma data tem nuvem dentro do polígono `pomar` (0,000 % de NaN nas 11). *(exacta)*

**G9.** As 11 cenas existem, os identificadores batem, e a janela lida corresponde à AOI. *(exacta)*

**G10.** **A composição da série não tem justificação fenológica consistente.** As nove datas ditas de plena estação cobrem os dias-do-ano 183 a 243; excluiu-se o dia 245 e manteve-se o 243. Tratar as nove como fenologicamente homogéneas é uma suposição por demonstrar. *(dias-do-ano exactos)*

**G11.** **8,21 ha do polígono `pomar` já estavam abaixo da referência menos 0,05 na primeira cena da série.** O valor é robusto à escolha da cena de 2017 (7,65–8,21 ha nas cinco cenas limpas desse ano). A ortofoto de 2025 a 25 cm mostra linhas de pomar contínuas nessa área: **não é falha de copado**. Consequência para quem vier: **a série de satélite não consegue datar o início do declínio, porque começa depois dele.** *(±0,6 ha)*

**G12.** Área que passou de sã a deficitária durante a série (a que a série consegue datar): **3,75 ha**. *(±0,6 ha, pela mesma razão)*

**G13.** Houve **alteração física do coberto entre 2021 e 2025** na janela E530550–531200 / N4654930–4655300: fracção de píxeis claros 5,1 % (2010) → 2,3 % (2021) → 16,4 % (2025); percentil 90 da luminância 141 → 147 → 213. É facto de imagem, sem interpretação. *(limiar 170 declarado; o valor absoluto depende do limiar, a direcção não)*

**G14. Negativo registado, para não voltar a entrar sem prova.** A hipótese «a cobertura/rede explica o padrão de défice» **já foi testada e o resultado é negativo**: a máscara de cobertura ocupa 21 % da Mancha W, 22 % da Zona 0 e 25 % da referência sã — é uniforme — e o NDVI sob cobertura é 0,02 a 0,03 mais **alto**, não mais baixo. *(este teste não foi refeito nesta camada; é herdado da ADENDA e passa como negativo registado, não como facto medido por C0)*

**G15.** O esquema de rega é um plano CAD à escala 1/3500 @ A1 (PRILUX, Jul/2009, sem levantamento) e **é proporcional**: o troço este bate com a parcela medida a 2–5 % no comprimento. A folha não tem o norte para cima: está rodada +33,05°. *(±3 % na escala, ±1,5° na rotação)*

**G16.** Georreferenciação disponível para uso: escala 0,8290 m por píxel de um render a 300 dpi, rotação +33,05°, origem em `SAIDA_C0\c0_13_georref.json`. **Resíduo mediano 64 m, p90 110 m.** Nada mais fino do que ±60–100 m pode ser afirmado com ela. *(declarado)*

**G17.** **Nenhum ponto do terreno pode ser atribuído a uma válvula ou a um sector com a informação actual.** A colocação das válvulas na M1 v1 usava uma escala 30 % errada; a colocação corrigida tem ±60–100 m, e o espaçamento entre válvulas no esquema é da mesma ordem. Qualquer afirmação da forma «isto está no sector X» está por estabelecer. *(consequência de G16)*

**G18.** O esquema mostra as válvulas em **duas filas**, norte e sul de uma conduta, e os sectores como **faixas transversais** ao eixo — nunca como bandas norte-sul. Sectores nomeados por letra (A a N, sem K), com caudais tabelados. *(leitura directa do PDF)*

**G19.** **Existe pomar com rede fora de toda a área estudada:** um bloco de **16,4 ha** em E529350–530085 / N4653700–4654478, ~750 m a sudoeste do polígono `pomar` e inteiramente a sul da AOI. O troço oeste do esquema (válvulas 1–5, o «B1» anotado com 1,77 ha) cai sobre ele por extrapolação da georreferenciação. **Se aí houver porta-enxerto Summer Kiwi, ele está fora de tudo o que se mediu até hoje.** *(área ±2 ha; pertença NÃO confirmada — ver NÃO TESTÁVEL)*

**G20.** O MDT `lidar/dem_aoi.json` cobre o polígono `pomar` inteiro, mas não os 198 m mais a leste da AOI. `lidar/t2_dem1m.json` cobre tudo. *(exacta)*

**G21.** `lidar/bacia.json` **não pode ser usado como está**: declara 36,9 ha, a sua *bbox* mede 51,5 ha, e essa *bbox* não cobre o polígono `pomar` (falta-lhe 272 m a oeste, 468 m a leste, 211 m a norte). *(exacta)*

**G22.** As sete ortofotos DGT em `orto\` estão em **EPSG:3763** e cobrem E 523753–531800 / N 4650711–4655790 em UTM29N. Cobrem o polígono `pomar` inteiro; **não** cobrem os 150 m mais a leste da AOI, nem a AOI alargada. Épocas: 1995 (1 m, IRG), 2004–2006, 2007, 2010, 2012 (50 cm), 2021, 2025 (25 cm). *(exacta)*

**G23.** As coordenadas do traço de 1995 (`_pacote_cowork\tracos_1995_coordenadas.csv`) caem todas dentro do polígono `pomar`, são consistentes entre os três sistemas a ≤0,1 m, e o L1 corresponde a uma feição linear visível na ortofoto de 1995. Os dois pontos `REF_` são aproximações: diferem dos centróides medidos em 24 m (manchaW) e 11 m (zona0) — usar os centróides medidos, não os do CSV. *(±10 m)*

**G24.** **Em quarentena, e não reentra por nenhuma porta:** a AOI (528400, 4654900, 529400, 4655700), o nome «lóbulo oeste B1», o bloco de 7,88 ha, a distância de 1,06 km, e os 49 ficheiros de `SAIDA_C0\c0_10_inventario_b1.csv`. A AOI é tecido urbano de Valença, a 745–1996 m do pomar, com o rio pelo meio. *(exacta)*

---

## Entregas desta camada

```
_VALIDACAO_CAMADAS\
  CAMADA_0_CERTIFICADO.md          este ficheiro
  CAMADA_1_PROMPT.md               prompt da camada seguinte
  SAIDA_C0\
    c0_01_rasters.py               grelha, CRS, NaN das 22 imagens
    c0_02_mascaras.py              contagens, circularidade, tendência da referência
    c0_03_proveniencia.py          catálogo STAC, harmonização, cenas disponíveis
    c0_04_cena2017.py              a primeira cena: fenologia, dispersão, alternativas, BOA
    c0_05_orto.py                  metadados e cobertura das ortofotos
    c0_06_esquema_escala.py        escala declarada do esquema
    c0_07_vista_larga.py           origem aritmética do erro da AOI b1
    c0_08_esquema_medir.py         moldura, anéis de válvula, eixo do desenho
    c0_09_copado_orto.py           assinatura de rede; janela da ADENDA
    c0_10_quarentena_b1.py         prova geográfica e inventário (nada apagado)
    c0_11_assuncoes.py             LiDAR, traço 1995, bacia, distâncias, eixo, AOI alargada
    c0_12_ajuste_esquema.py        o esquema é proporcional?
    c0_13_georref.py               georreferenciação por ajuste de forma
    c0_14_lobo_oeste_e_1995.py     onde cai o lóbulo oeste; o traço em 1995
    c0_15_mapas.py                 M1 v2 e M2 v2
    c0_16_bloco_sw.py              área do bloco sudoeste; cobertura do MDT
    M1_valvulas_v2.png / .svg      mapa para a gestora — zero informação de declínio
    M2_declinio_v2.png / .svg      mapa interno, classe corrigida
    c0_*.png, c0_*.json, c0_*.csv  provas intermédias e resultados
```

Os originais em `ganfei_s2\figuras\` **não foram tocados**. As M1 v2 e M2 v2 estão
em `SAIDA_C0\`.
