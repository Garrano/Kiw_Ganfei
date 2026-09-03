# Camada 1 — Substrato

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada C1 de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md`, que explica a pilha e as regras.

A tua camada é o **substrato**: terreno, solo, clima, hidráulica, térmico.
Abaixo de ti só está a C0 — geometria e proveniência. Herdas o certificado dela
e mais nada. Não leias o dossiê, as figuras F1–F7, nem qualquer conclusão. Se
abrires uma por engano, regista-o no teu certificado, como a C0 registou.

**Não teorizes acima da tua camada.** Não opinas sobre patogénios, sobre
etiologia, nem sobre o que causa o declínio. Se um resultado te sugerir uma
causa, guarda-a: não é a tua pergunta, e escrevê-la contamina quem vier a
seguir.

## O que herdas — e só isto

Certificado por **C0 (geometria e proveniência)**, 28-08-2026. Trata como dados,
não revalides, e não uses nada que não esteja nesta lista.

**G1.** A AOI de estudo é (529950, 4654600, 531950, 4655600) em EPSG:32629,
grelha de 10 m, 200×100 píxeis. *(exacta)*

**G2.** O polígono `pomar` tem 2903 píxeis = 29,03 ha, ocupa E 530145–531525 /
N 4654865–4655465, e está inteiramente dentro da AOI com ≥135 m de folga em
qualquer direcção. *(±10 m no contorno)*

**G3.** O eixo maior da parcela é o **azimute 70,0°** (WSW–ENE); comprimento
1445 m, largura 328 m, centróide E530791 N4655130. Qualquer fronteira
transversal defensável é perpendicular a esse eixo, ou seja azimute 160°.
*(azimute ±1°, comprimento ±10 m)*

**G4.** Áreas das máscaras, na definição operativa (polígono rasterizado):
`pomar` 29,03 ha · `saudavel`+`saudavel_2`+`saudavel_3` 4,54 ha (2,64 + 1,19 +
0,71) · `manchaW` 4,27 ha · `zona0` 2,20 ha. Todas dentro de `pomar`; nenhuma se
intersecta com as outras. *(±0,01 ha por píxel de bordo)*

**G5.** As máscaras são estáticas — os mesmos polígonos em todas as datas — mas
**duas são circulares em relação ao NDVI**: `pomar` é semeada por `nd2026 >
0,78`; `saudavel×3` exige `nd2026 > 0,78`; `manchaW` é `nd2026 < 0,76` dilatada.
Só `zona0` é um polígono geográfico traçado à mão. *(facto de código)*

**G6.** A referência sã não desce: +0,0038 NDVI/ano (9 cenas de plena estação,
p = 0,13). Mas foi escolhida por ter NDVI alto na **última** cena da série, o
que a enviesa para cima no fim; o enviesamento não foi quantificado.

**G7.** A série é radiometricamente comparável, verificado em alvos estáveis:
NDVI 0,212–0,241 sobre 7637 píxeis SCL 5 comuns a sete datas, sem degrau em
2022. *(±0,015 NDVI)*

**G8.** Nenhuma data tem nuvem dentro do polígono `pomar`. *(exacta)*

**G9.** As 11 cenas existem no catálogo, os identificadores batem, a janela lida
corresponde à AOI. *(exacta)*

**G10.** A composição da série **não tem justificação fenológica consistente**:
as nove datas ditas de plena estação cobrem os dias-do-ano 183 a 243; excluiu-se
o dia 245 e manteve-se o 243. Tratá-las como fenologicamente homogéneas é uma
suposição por demonstrar.

**G11.** 8,21 ha do polígono `pomar` já estavam abaixo da referência menos 0,05
na **primeira** cena da série, e o valor é robusto à escolha da cena de 2017
(7,65–8,21 ha em cinco cenas limpas desse ano). A ortofoto de 2025 a 25 cm
mostra linhas de pomar contínuas nessa área: não é falha de copado. **A série de
satélite não consegue datar o início do declínio, porque começa depois dele.**
*(±0,6 ha)*

**G12.** Área que passou de sã a deficitária durante a série: 3,75 ha. *(±0,6 ha)*

**G13.** Houve alteração física do coberto entre 2021 e 2025 na janela
E530550–531200 / N4654930–4655300: fracção de píxeis claros 5,1 % (2010) →
2,3 % (2021) → 16,4 % (2025); percentil 90 da luminância 141 → 147 → 213.
Facto de imagem, sem interpretação.

**G14.** *Negativo já registado, para não voltar a entrar sem prova:* a hipótese
«a cobertura/rede explica o padrão de défice» **foi testada e o resultado é
negativo** — a máscara de cobertura ocupa 21 % da Mancha W, 22 % da Zona 0 e
25 % da referência sã (é uniforme), e o NDVI sob cobertura é 0,02 a 0,03 mais
**alto**. *(herdado, não remedido pela C0)*

**G15.** O esquema de rega é um plano CAD à escala 1/3500 @ A1 (PRILUX,
Jul/2009, `LEVANTAMENTO: -`) e **é proporcional**: o troço este bate com a
parcela medida a 2–5 % no comprimento. A folha **não tem o norte para cima**:
está rodada +33,05°. *(±3 % na escala, ±1,5° na rotação)*

**G16.** Georreferenciação disponível: escala 0,8290 m por píxel de um render a
300 dpi do PDF, rotação +33,05°, origem em
`_VALIDACAO_CAMADAS\SAIDA_C0\c0_13_georref.json`. **Resíduo mediano 64 m, p90
110 m.** Nada mais fino do que ±60–100 m pode ser afirmado com ela.

**G17.** **Nenhum ponto do terreno pode ser atribuído a uma válvula ou a um
sector com a informação actual.** O espaçamento entre válvulas no esquema é da
mesma ordem que a incerteza da colocação.

**G18.** O esquema mostra as válvulas em **duas filas**, norte e sul de uma
conduta, e os sectores como **faixas transversais** ao eixo — nunca como bandas
norte-sul. Sectores nomeados por letra (A a N, sem K), com caudais tabelados
(65 a 99,9 m³ por sector, soma 1053,3).

**G19.** **Existe pomar com rede fora de toda a área estudada:** um bloco de
16,4 ha em E529350–530085 / N4653700–4654478, ~750 m a sudoeste do polígono
`pomar` e inteiramente a sul da AOI. O troço oeste do esquema (válvulas 1–5)
cai sobre ele por extrapolação. *(área ±2 ha; pertença NÃO confirmada)*

**G20.** O MDT `lidar/dem_aoi.json` cobre o polígono `pomar` inteiro, mas não os
198 m mais a leste da AOI. `lidar/t2_dem1m.json` cobre tudo. *(exacta)*

**G21.** `lidar/bacia.json` **não pode ser usado como está**: declara 36,9 ha, a
sua *bbox* mede 51,5 ha, e essa *bbox* não cobre o polígono `pomar` — falta-lhe
272 m a oeste, 468 m a leste e 211 m a norte. *(exacta)*

**G22.** As sete ortofotos DGT em `orto\` estão em EPSG:3763 e cobrem
E 523753–531800 / N 4650711–4655790 em UTM29N. Cobrem o polígono `pomar`
inteiro; **não** cobrem os 150 m mais a leste da AOI. Épocas: 1995 (1 m, IRG),
2004–2006, 2007, 2010, 2012 (50 cm), 2021, 2025 (25 cm). *(exacta)*

**G23.** As coordenadas do traço de 1995 caem todas dentro do polígono `pomar`,
são consistentes entre UTM29N / PT-TM06 / WGS84 a ≤0,1 m, e o L1 corresponde a
uma feição linear visível na ortofoto de 1995. Os dois pontos `REF_` são
aproximações (24 m e 11 m de erro contra os centróides medidos): **usar os
centróides medidos, não os do CSV**.

**G24.** **Em quarentena, e não reentra por nenhuma porta:** a AOI (528400,
4654900, 529400, 4655700), o nome «lóbulo oeste B1», o bloco de 7,88 ha, a
distância de 1,06 km, e os 49 ficheiros listados em
`SAIDA_C0\c0_10_inventario_b1.csv`.

## O que ficou por resolver abaixo de ti

Estas lacunas são da C0 e **afectam-te directamente**:

1. **A bacia não está delineada.** `lidar/bacia.json` declara 36,9 ha; a sua
   *bbox* mede 51,5 ha e não cobre o pomar. O número 36,9 coincide exactamente
   com 29,03 (pomar) + 7,88 (bloco em quarentena). *Porque te afecta:* toda a
   hidrologia de encosta que assente nessa bacia está por refazer. **Redelineia
   a bacia a partir do MDT antes de usar qualquer coisa que dependa dela.**

2. **A máscara `pomar` foi semeada pelo NDVI de 2026.** Copado que já tivesse
   descido abaixo de 0,78 nessa data e não fosse recuperado pelo fecho
   morfológico está fora da máscara. 4,87 ha do polígono não têm assinatura de
   rede na ortofoto de 25 cm; e dentro da AOI, fora do polígono, há até 13,36 ha
   com essa assinatura (limite superior: inclui caminhos, estufas e edifícios).
   *Porque te afecta:* se relacionares cota, declive ou humidade com «o pomar»,
   estás a relacionar com uma máscara definida pelo vigor. Diz sempre sobre que
   máscara estás a medir, e se possível repete sobre uma máscara alternativa.

3. **~16 ha da exploração não estão em nenhuma área estudada.** O candidato
   medido é o bloco sudoeste (G19), fora da AOI e fora da cobertura do
   `dem_aoi`. *Porque te afecta:* se a rega tem origem única e o bloco pertence à
   mesma rede, a hidráulica que modelares está incompleta. E o `dem_aoi` não o
   cobre.

4. **A colocação das válvulas tem ±60–100 m.** *Porque te afecta:* não podes
   ligar um trecho de conduta, uma pressão ou um caudal a um ponto do terreno
   com precisão melhor do que essa. A hidráulica pode ser modelada em topologia
   (montante/jusante, ordem das válvulas), não em geometria fina.

5. **A regra de fenologia não se sustenta** (G10). *Porque te afecta:* se
   comparares térmico, precipitação ou SAR com a série óptica data a data,
   estás a comparar com um conjunto que mistura o dia 183 com o dia 243.

6. **A faixa E531800–531950 da AOI não tem ortofoto e o `dem_aoi` não chega aos
   198 m mais a leste.** *Porque te afecta:* qualquer estatística «na AOI»
   calculada sobre esses dois produtos tem um bordo truncado. O polígono `pomar`
   não chega lá, portanto o efeito é nulo se medires sobre o polígono.

## O que foi rejeitado, e não podes usar

- **Tudo o que deriva de `sentinel_b1/`**: as 22 imagens, `expansao_b1.csv`,
  `b1_nucleo_serie.csv`, `Q5_b1.csv`, os scripts `b1_serie.py`, `b1_analise.py`,
  `b1_nucleo_interno.py`, `q5.py`, e a constante `area_bloco_ha = 7,88`. A AOI
  mede tecido urbano de Valença (SCL 2026: 63 % vegetação de jardim, 37 % sem
  vegetação, 0 % água), a 745–1996 m do pomar, com o rio Minho pelo meio.
  **Cai com ela qualquer «bloco de controlo são» e qualquer exclusão que se
  tenha apoiado no comportamento do «B1» — incluindo qualquer exclusão de falha
  de fonte de rega.** Se encontrares um número que dependa dele, pára e regista.
- **A escala de 1,0787 m por unidade de esboço** e, com ela, a posição das
  válvulas 6–13 e todas as fronteiras de sector das versões antigas da M1 e da
  M2. Está 30 % acima da real.
- **A distância «1,06 km»**. Não é reproduzível: 745 m de caixa a polígono,
  1281 m de centro a polígono, 1996 m de centróide a centróide. Não a
  substituas por outra: a entidade que ela media não existe.
- **A interpretação «falha de copado / caminhos / outra cultura»** dos 8,21 ha.
  A medição sobrevive; a interpretação não.
- **A incerteza declarada de ±40 m** na colocação das válvulas.
- **`lidar/bacia.json` como está.**

## Materiais

```
Downloads\ganfei_s2\lidar\
    MDT-50cm-1565xx / 1566xx-07-2025_v02.tif   21 mosaicos MDT DGT, 50 cm, EPSG:3763
    dem_aoi.npy / dem_aoi.json                 recorte 0,5 m (2041x3625), NÃO cobre 198 m a leste da AOI
    masks_mdt.npy                              4 máscaras rasterizadas no referencial do MDT
    t2_dem1m.npy / t2_dem1m.json               1 m (3683x5908), 4 campanhas: 2025-08-02 (9),
                                               2026-01-15 (8), 2026-01-14 (2), 2026-01-13 (2)
    t2_residuo.npy                             resíduo entre campanhas — o «ensaio de costura»
    _mdt1m.tif, _glo30.tif                     MDT 1 m e Copernicus GLO-30
    bacia.json                                 REJEITADO, ver acima
Downloads\ganfei_s2\lidar_prep.py, lidar_terreno.py, bacia.py, bacia2.py,
    escoamento.py, paleo.py, t2_mosaico.py, t2_paleo.py, t2_paleo2.py,
    nivelamento.py, secagem.py, chuva.py, geada.py, termico.py, sar_invernos.py
Downloads\ganfei_s2\termico.csv, audit_termico.csv, audit_termico.py
Downloads\ganfei_s2\sar_invernos.csv
Downloads\ganfei_s2\lidar_topografia_por_mascara.csv, cota_vs_ndvi.csv
Downloads\ganfei_s2\pendente_bacia.csv, pendente_escoamento.csv,
    pendente_nivelamento.csv, pendente_precipitacao.csv, pendente_geada.csv,
    pendente_sar_declives.csv, pendente_sar_secagem.csv,
    pendente_degrau_campanhas.csv
Downloads\Esquema de rega retificado.pdf     hidráulica: conduta, sectores A–N, caudais
Downloads\ganfei_s2\orto\                    7 épocas DGT, para datar movimentos de terra
Downloads\_VALIDACAO_CAMADAS\SAIDA_C0\c0_13_georref.json   georreferenciação do esquema
Downloads\_VALIDACAO_CAMADAS\SAIDA_C0\c0_11_eixo.json      eixo medido da parcela
```

Boletins de solo A2 (11): **não existem em nenhum destes caminhos.** Procurei em
`Downloads\` até três níveis por `*solo*`, `*A2*`, `*boletim*` e `*analis*`, e
em `ganfei_s2\` inteiro: nada. Se existirem, estão fora de tudo o que a C0 viu.
Se também não os encontrares, isso é resultado — diz onde procuraste, e a T10
fecha com «não localizáveis».

Tens internet (AWS Open Data Sentinel-2, `sentinel-2-l2a`, Earth Search STAC v1,
sem credenciais; e o que mais precisares para ERA5-Land ou Landsat).

## Tarefas

**T1 — O MDT é uma superfície só, ou uma costura?** Em `lidar/t2_dem1m.json` há
quatro campanhas com datas diferentes (Ago/2025 e Jan/2026) e `t2_residuo.npy`
guarda o resíduo entre elas. Mede a distribuição desse resíduo **dentro do
polígono `pomar`** e ao longo das linhas de junção entre campanhas. Se houver um
degrau sistemático na junta, qualquer microrrelevo medido a atravessá-la é
artefacto. Diz qual é a magnitude do degrau e onde passam as juntas.

**T2 — Redelineia a bacia.** `lidar/bacia.json` está rejeitado (G21). Parte do
MDT (`dem_aoi.npy`, ou `t2_dem1m.npy` se precisares de sair da folha), delineia
a bacia que drena para o polígono `pomar`, e diz a área. Compara com os 36,9 ha
declarados. Depois diz explicitamente se `bacia.py` / `bacia2.py` produzem o
`bacia.json` actual e, se sim, onde é que o cálculo derrapa.

**T3 — Topografia por máscara, com a circularidade à vista.** Recalcula cota,
declive e curvatura por máscara (`pomar`, `manchaW`, `zona0`, referência sã) a
partir do MDT, e compara com `lidar_topografia_por_mascara.csv` e
`cota_vs_ndvi.csv`. **Atenção a G5:** `manchaW` e a referência são máscaras
definidas por NDVI. Uma correlação cota↔NDVI medida sobre elas é em parte
circular. Repete a mesma medida sobre `zona0` (que é geográfica) e sobre uma
grelha regular dentro de `pomar`, e diz se a relação sobrevive.

**T4 — A hipótese de nivelamento e truncatura.** `nivelamento.py` e `paleo.py`
existem. Reexecuta-os ou refá-los, e responde: há evidência no MDT de
movimentação de terras — plataformas, taludes, degraus rectilíneos? Se sim,
usa as sete épocas de ortofoto (`orto\`, G22) para **datar** o movimento: entre
que duas épocas aparece. Cuidado: a de 1995 é a 1 m e em infravermelho-verde,
as de 2004–2012 a 50 cm, as de 2021 e 2025 a 25 cm — a resolução muda a
detecção, e uma feição que «aparece» em 2021 pode só ter passado a ser visível.

**T5 — Térmico Landsat, e a sua retirada.** `termico.csv` tem 81 linhas de
dados e `audit_termico.csv` tem 137; a prosa fala de 148 cenas. **Os três
números não fecham — reconcilia-os primeiro.** Depois verifica: qual a
resolução nativa da banda térmica (não a do produto reamostrado), e quantos
píxeis independentes cabem em cada máscara a essa resolução nativa. Se a
`zona0` (2,20 ha) tiver menos de dois píxeis térmicos independentes, nenhuma
diferença térmica entre máscaras é mensurável, e essa é a resposta. Diz também
por que razão o térmico foi retirado, se conseguires estabelecê-lo a partir dos
ficheiros e não de prosa.

**T6 — Precipitação ERA5-Land.** `chuva.py` e `pendente_precipitacao.csv`.
Confirma de que célula ERA5-Land vêm os valores, qual é o tamanho dessa célula
(≈9 km) e a que distância fica o seu centro do polígono `pomar`. Uma célula de
9 km sobre um vale do Minho com relevo não resolve a parcela: diz o que essa
série pode e não pode sustentar. Se houver estação udométrica próxima, diz onde
está e a que distância.

**T7 — SAR Sentinel-1, três Invernos.** `sar_invernos.py`, `sar_invernos.csv`,
`pendente_sar_secagem.csv`, `pendente_sar_declives.csv`. Verifica: órbita
(ascendente/descendente), ângulo de incidência, polarização, e se as três
séries são da mesma órbita — se não forem, não são comparáveis. Depois responde
se a retrodifusão distingue as máscaras, **tendo em conta G13**: houve
alteração física do coberto entre 2021 e 2025 na janela E530550–531200 /
N4654930–4655300, e rede ou cobertura mudam a retrodifusão sem nada mudar no
solo. Testa se o efeito que encontras coincide com essa janela.

**T8 — Hidráulica da rede, em topologia e não em geometria.** Usa o PDF do
esquema (G15, G18) e a georreferenciação de `c0_13_georref.json` (G16). Podes
afirmar a **ordem** das válvulas ao longo da conduta, quais estão a norte e
quais a sul, e os caudais tabelados por sector (A a N). **Não podes** dizer que
um ponto do terreno está no sector X (G17). Com isso: a origem é mesmo única?
De que lado entra a água? Há alguma válvula em fim de linha que fique
sistematicamente a jusante de todas as outras? Responde em topologia.

**T9 — O bloco sudoeste (G19) na tua camada.** 16,4 ha de pomar com rede em
E529350–530085 / N4653700–4654478, fora de tudo o que se mediu. Diz: (a) o
`dem_aoi` cobre-o? (b) e o `t2_dem1m`? (c) está na mesma bacia que o polígono
`pomar`, ou noutra? (d) está à mesma cota, ou noutro nível da planície aluvial?
Isto é geometria e terreno, é teu. **Não** especules sobre se pertence à
exploração — isso está por confirmar com a gestora.

**T10 — Boletins de solo A2.** Procura-os. Se os encontrares: quantos são, que
parâmetros trazem, e — o essencial para esta cadeia — **têm coordenadas ou só um
nome de talhão?** Sem coordenadas, um boletim de solo não se pode relacionar
com nenhum padrão espacial, e isso tem de ficar dito antes de a C2 e a C3
tentarem. Se não os encontrares, diz onde procuraste.

## Onde já se errou nesta matéria

- **O erro de fundação:** uma AOI a 1–2 km do sítio, do outro lado do rio, usada
  durante semanas como bloco de controlo são. Nasceu de uma escala 30 % errada
  aplicada por extrapolação ao extremo de um desenho. Já está isolada (G24), mas
  o padrão do erro interessa-te: **um número foi aceite porque era plausível e
  nunca foi confrontado com a imagem.** Confronta tudo com a imagem.
- **`lidar/bacia.json`** declara 36,9 ha, que é exactamente 29,03 + 7,88 — o
  pomar mais o bloco em quarentena. Pode ser coincidência; pode ser
  contaminação. Não o uses sem redelinear.
- **A distância «1,06 km»** entrou em prosa sem nenhum ficheiro que a
  sustentasse. Se encontrares um número em metros que não saia de um cálculo,
  trata-o como não verificado até o reproduzires.
- **As máscaras `pomar`, `saudavel×3` e `manchaW` foram definidas pelo NDVI de
  2026** (G5). Isto não estava explícito em lado nenhum e é fácil esquecer.
  Qualquer relação entre uma variável de substrato e «o pomar» ou «a mancha»
  arrasta essa selecção.
- **A regra de fenologia** separa o dia 243 do dia 245 e junta o 183 com o 243.
- **A M1 e a M2 antigas** desenhavam fronteiras de sector como linhas N–S. O
  eixo é 70°. As versões corrigidas estão em `SAIDA_C0\M1_valvulas_v2.png` e
  `M2_declinio_v2.png` — mas **não abras a M2** se quiseres manter-te limpo do
  padrão de declínio; ela é da camada C2, não da tua. A M1 podes ver: por
  construção não tem nenhuma informação de estado sanitário.

## O que entregar

1. `CAMADA_1_CERTIFICADO.md`, com as cinco secções exactas do protocolo:
   CONFIRMADO / CORRIGIDO / REJEITADO / NÃO TESTÁVEL / PASSA PARA CIMA.
   A secção **PASSA PARA CIMA** é a mais importante: é a lista fechada de factos
   de substrato que as camadas seguintes podem usar. Sê avaro. O que não estiver
   lá, não existe para elas.
2. `CAMADA_2_PROMPT.md`, seguindo `MODELO_PROMPT.md`. A camada 2 é o **sinal
   vegetal**: série NDVI, limiar de défice, zona de referência, séries da Zona 0
   e da Mancha W, geometria de expansão, núcleos. Enche o modelo com o que
   certificaste, e com as perguntas de substrato que ficaram em aberto e que a
   C2 precisa de saber que estão em aberto.
3. O teu código em `Downloads\_VALIDACAO_CAMADAS\SAIDA_C1\`.

Se rejeitares um facto herdado da C0, **pára** e devolve. Não construas por
cima. Se encontrares algo que invalide a análise inteira, escreve-o na primeira
linha do certificado e pára.
