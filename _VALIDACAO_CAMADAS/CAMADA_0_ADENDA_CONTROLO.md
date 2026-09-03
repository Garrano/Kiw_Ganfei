# Camada 0 — adenda: blocos candidatos a CONTROLO EXTERNO

Sessão de geometria pura, 28-08-2026. Kiwi do Emparcelamento de Ganfei, Valença.
Código em `SAIDA_C0\ctrl_*.py`. Polígonos em `SAIDA_C0\controlos.geojson`
(EPSG:32629).

## Regra dura desta sessão, e o que ela custou

**Não foi lido NDVI nem nenhum índice de vegetação, em fase nenhuma.** Nem para
escolher candidatos, nem para os desenhar, nem para os medir. A banda 4 (NIR)
das ortofotos nunca foi aberta. Os únicos critérios usados foram:

| critério | o que é | onde entra |
|---|---|---|
| periodicidade linear 2,5–9 m | pico de Fourier da luminância R+G+B em janelas de 16–32 m | prospecção e delimitação de C2, C3 |
| material de cobertura | luminância alta **e** saturação baixa (plástico, rede, estufa) | delimitação de C1a/b/c |
| copado fechado *vs* entrelinha aberta | leitura visual a 25 cm em época com folha | identificação da cultura |
| água | luminância baixa **e** azul dominante | margem do rio, distâncias |
| cota | MDT LiDAR DGT 50 cm | altimetria |

Nenhum destes é sinal de vigor. Um bloco entrou na lista por ter **linhas
regulares**, nunca por estar verde.

O custo desta regra apareceu logo: a ortofoto de 2025 foi voada — segundo o STAC
da DGT, entre 29-03 e 26-07-2025 — com o kiwi deste canto ainda sem folha. Nessa
imagem o pomar do caso e o bloco a sudoeste são **estruturalmente
indistinguíveis**: ambos aparecem como faixas brancas de cobertura sobre uma
grelha de ~4,9 m. Foi preciso ir às épocas com folha (2012, 2021, 2023) para os
separar. Se a identificação tivesse sido feita só em 2025 — e sem índice — o
bloco SW teria sido proposto como pomar de kiwi. Fica registado porque é
exactamente o tipo de erro que esta cadeia existe para apanhar.

---

## 1. Resultado em três linhas

1. O bloco de ~16 ha a sudoeste está delimitado: **13,60 ha em três parcelas**
   (C1a 5,68 + C1b 5,92 + C1c 2,00), a 528 m do bordo do polígono `pomar`.
2. **Deixou de ter copado fechado entre 2012 e 2021.** Em 2010 e 2012 lia-se
   como latada coberta; em 2021, 2023 e 2025 lê-se como cultura em linha sobre
   camalhão, com cobertura de plástico. **Não serve como controlo
   contemporâneo.**
3. Na prospecção dos ~3 km cobertos pela imagem disponível, **não existe segundo
   pomar de latada em produção no aluvião do Minho**. O que existe é vinha,
   milho, hortícolas em túnel e estufas. Um controlo externo contemporâneo de
   kiwi **não está disponível a esta distância** — e essa é a resposta à revisão
   adversarial, não uma falha da prospecção.

E um achado que não estava pedido: **o candidato mais próximo em linha recta,
C2, está na margem oposta do rio Minho.** Fica a 293 m do bordo do polígono
`pomar` e a 2 m do bordo do rectângulo declarado no enunciado, e mesmo assim há
250 m de água entre os dois centróides. É a mesma armadilha do «B1». Está
rejeitado, e está no geojson marcado como rejeitado precisamente para que
ninguém o volte a apanhar.

---

## 2. Como se prospectou, e o que ficou de fora

**Janela de prospecção.** Círculo de 3 km em torno do centróide do pomar do
caso (E 530835, N 4655160), cortado pela cobertura disponível.

| sector | cobertura | resultado |
|---|---|---|
| O e SO até 3 km | mosaico 002-3 a 25 cm, 7 épocas | Valença urbana, fortaleza, A3; nenhum pomar |
| S até 3 km | idem | minifúndio de faixas, vinha, milho; nenhum pomar |
| SO ribeirinho (bloco SW) | idem | **C1a, C1b, C1c** |
| E, de E 531800 a E 533900 | OrtoSat2023 por WMS (o COG 002-4 do STAC responde **403**, balde privado) | faixas de sequeiro, aldeia, monte florestado, estufas; nenhum pomar |
| NE, margem direita | OrtoSat2023 por WMS | paisagem galega de faixas, ETAR, estufas; nenhum pomar de latada |
| E, além de E 533900 | **sem cobertura obtida** | **não prospectado** |
| margem direita, além de 1 km | **não prospectado em detalhe** | outro país; sem LiDAR DGT válido |

Duas lacunas assinaladas, não tapadas: o sector a leste de E 533900 e o interior
da margem direita. Nenhuma das duas é candidata plausível — a primeira já é
encosta, a segunda é Espanha — mas nenhuma foi verificada.

**Detector.** Mapa de periodicidade linear (FFT em blocos de 32 m, passo 16 m,
banda 3–9 m) sobre 14,2 km² a 0,5 m. Deu 13 componentes acima de 0,6 ha ao
percentil 93 (`ctrl_02_candidatos.csv`, `ctrl_04_lista.py`). **Onze dos treze
eram falsos positivos** — a periodicidade vinha das faixas estreitas do
minifúndio e dos regos de lavoura, não de estrutura de pomar. Todos foram
abertos a 25 cm antes de qualquer decisão. É por isso que o detector serve para
nomear e não para concluir.

---

## 3. Os blocos

Área por fórmula de Gauss sobre o polígono. Cota do MDT LiDAR DGT 50 cm,
amostrada a 2 m dentro do polígono. Distâncias ao **polígono `pomar`** de
`masks.json` (não à caixa envolvente), bordo a bordo e centróide a centróide.

| id | descrição | área (ha) | d. bordo (m) | d. centróide (m) | cota média (m) | cota mín–máx | dp | n LiDAR | compasso (m) | azimute linhas | dist. margem (m) | margem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1a | bloco SW, parcela norte | 5,68 | 528 | 1297 | 6,39 | 4,85–9,29 | 0,92 | 14 171 | 4,87 | 81° | 218 | esquerda |
| C1b | bloco SW, parcela central e sul | 5,92 | 781 | 1580 | 6,02 | 4,22–8,22 | 0,81 | 14 783 | 4,53 | 82° | 204 | esquerda |
| C1c | bloco SW, estufas, extremo SO | 2,00 | 1111 | 1850 | 5,97 | 2,62–11,22 | 1,06 | 4 971 | 4,87 | 81° | 134 | esquerda |
| C2 | vinha ribeirinha a NO | 5,21 | 293 | 728 | 6,14 | 5,15–7,36 | 0,47 | 13 052 | 3,35 | 174° | 192 | **direita** |
| C3 | vinha a sul | 2,74 | 87 | 754 | 8,22 | 7,72–8,63 | 0,13 | 6 864 | 2,72 | 12° | 392 | esquerda |
| REF | rectângulo declarado do caso *(referência, não analisado)* | 79,46 | — | — | 6,10 | 0,85–13,10 | 2,67 | 198 940 | 4,91 | 33° | — | esquerda |

A cota do REF varia 12 m porque o **rectângulo** apanha o rio e o talude da
margem; 19,6 % da sua área é água. O polígono `pomar` de `masks.json`, esse, tem
**0,00 ha de água** — verificado contra a máscara de água da ortofoto de 2025.
Não há paragem de linha a declarar sobre a C0.

### 3.1 Proveniência de cada limite

Nenhum polígono é uma caixa envolvente. Cada lado assenta num objecto visível.

**C1a, C1b** — contorno da máscara de material de cobertura na ortofoto de 2025
a 25 cm (luminância > p91 e saturação < 0,18), fecho morfológico de 14 m,
abertura, preenchimento de buracos, contorno exterior, Douglas-Peucker a 4 m
(`ctrl_13_contornos.py`). O fecho de 14 m cola as linhas da mesma parcela e não
salta as faixas de pousio de 25 m que separam parcelas — foi esse o parâmetro
que decidiu onde acaba uma parcela e começa a outra.

- NO: caminho de terra sobre o dique e a galeria ripícola da margem esquerda do
  Minho. Presente e no mesmo sítio nas 7 épocas.
- SE: estrada municipal empedrada que sobe do lugar para NNE. Limite físico
  nítido nas 7 épocas.
- NE e SO: cabeceiras das parcelas contra faixas de pousio.
- **Lado com maior incerteza:** a cabeceira norte de C1a. Solo nu seco também é
  claro e pouco saturado, e o contorno faz aí uma saliência de ~0,4 ha para
  dentro do campo lavrado. Incerteza declarada **±10 m nesse lado, ±4 m nos
  restantes.**

**C1c** — mesma cadeia. O contorno inclui telhados de armazéns do lugar a sul;
±0,3 ha por excesso.

**C2, C3** — invólucro convexo da mancha de periodicidade linear (2,5–9 m) na
ortofoto de 2025, união de 10 m (`ctrl_10_poligonos.py`). São parcelas únicas e
convexas, pelo que o invólucro reproduz o limite. A O e a N por caminhos de
terra; a E e a S, em C2, pela galeria ripícola do Minho e de um braço
secundário. Preenchimento da mancha dentro do polígono: 72 % em C2, 86 % em C3.
Incerteza **±8 m**. C2 fica por defeito: a vinha continua para norte, fora do
invólucro.

### 3.2 Comparação com a medição anterior

A sessão anterior mediu **16,36 ha** neste mesmo sítio, por soma das componentes
≥ 0,4 ha de uma assinatura de «coberto claro + textura», dentro de uma janela
rectangular (`c0_16_bloco_sw.py`). Aqui obtêm-se **13,60 ha** em três polígonos
fechados, ou **15,32 ha** se se baixar o limiar de luminância de p91 para p88 e
os polígonos se fundirem em dois. A diferença é quase toda faixas de pousio
claro e a saliência da cabeceira norte. **Não é um erro da medição anterior; é a
diferença entre somar píxeis numa janela e fechar um polígono.** Quem precisar
de um número único: **14,5 ± 1,5 ha**. E, para a área que está de facto sob
cobertura em 2025, o plástico visível soma **3,24 ha** em C1a + C1b (1,36 +
1,88) — o resto da parcela é entrelinha.

---

## 4. O que cada bloco controla, e o que não controla

### C1a e C1b — bloco SW, 11,6 ha, a 528 m

**Sequência de estrutura, época a época** (`ctrl_05_painel_blocoSW.png`,
`ctrl_15_instrumento_independente.png`):

| época | o que se vê |
|---|---|
| 2004, 2007 | campo aberto, sem estrutura |
| 2010 | bloco implantado, cobertura clara em linhas |
| 2012 | **copado contínuo escuro com pontos claros regulares** — compatível com latada coberta com rede |
| 2021 | linhas separadas por entrelinha aberta, com plástico ao longo da linha |
| 2023 *(OrtoSat2023, outro sensor)* | linhas separadas por entrelinha aberta |
| 2025 | camalhões com cobertura de plástico contínua |

**Controla:**
- substrato — mesmo aluvião do Minho, mesma margem, 0 travessias de água;
- cota — 6,4 m e 6,0 m contra 6,1 m no rectângulo do caso; amplitude interna de
  4,4 e 4,0 m contra 12,3 m no rectângulo (que inclui o rio);
- distância à margem — 218 e 204 m, da mesma ordem que a frente ribeirinha do
  próprio pomar;
- clima local e regime de nevoeiro do vale;
- **coorte de plantação** — implantado entre 2007 e 2010, exactamente como o
  pomar do caso, que também está ausente em 2004 e em 2007 e já está no
  terreno em 2010, ainda em implantação e só na metade poente
  (`ctrl_05_painel_REF_idade.png`). Esta é a coincidência mais valiosa que
  aparece nesta prospecção, e é o que torna a alínea seguinte tão pesada.

**Não controla:**
- **espécie e cultura actual.** Entre 2012 e 2021 deixou de ter copado fechado.
  Qualquer série 2017–2026 medida aqui mistura o que quer que ali esteja agora
  com o que ali estava antes. Isso é fatal para um controlo da série do caso;
- gestão, rega, fertilização, tratamentos — proprietário desconhecido, e a
  sessão anterior perguntou pela propriedade sem a determinar;
- **origem da água** — não determinável na ortofoto. Não há reservatório, nem
  furo, nem casa de bombas visível dentro ou junto do bloco. **Não sei**, e não
  há forma de saber por imagem;
- histórico de nivelamento e de movimentação de terras.

**Veredicto:** não serve como controlo contemporâneo de kiwi. Serve, e só,
como **controlo histórico para 2010–2012** — e mesmo esse com a reserva de a
espécie não estar provada, apenas o compasso (4,87 e 4,53 m, contra 4,91 m no
caso) e o fecho do copado.

Uma nota de fronteira de camada: o facto de o único bloco de coorte comparável,
no mesmo aluvião, ter deixado de ter copado fechado entre 2012 e 2021 é um facto
geométrico. **Não digo o que significa.** Isso é C4.

### C1c — estufas, 2,00 ha, a 1111 m

Rejeitado. Horticultura protegida com cobertura permanente. Fica delimitado só
para não voltar a ser somado a C1b, como aconteceu na medição de 16,36 ha.

### C2 — vinha ribeirinha, 5,21 ha, a 293 m — **REJEITADO POR MARGEM**

Compasso 3,35 m, linhas a 174°, estrutura de bardo em todas as épocas
verificadas: é vinha, não latada. Mas o motivo da rejeição é anterior a esse:
**está na margem direita.** O segmento recto entre o seu centróide e o centróide
do pomar atravessa **250 m de água do Minho**; o segmento até à fortaleza de
Valença atravessa o rio **duas** vezes; o segmento até ao centro de Tui não
atravessa nada (`ctrl_17_margem.py`).

Isto merece ser dito com todas as letras: C2 está a **2 m** do bordo do
rectângulo declarado no enunciado, é o candidato mais próximo em linha recta, e
está noutro país. Se a prospecção tivesse parado na distância euclidiana, C2
teria entrado. É o «B1» outra vez, com outro nome.

Controla: nada que sirva o caso. Não controla: margem, país, jurisdição, gestão,
origem de água, cultura, compasso.

### C3 — vinha a sul, 2,74 ha, a 87 m

**Controla:**
- substrato aluvionar e clima local, a 87 m do bordo do pomar, na mesma margem;
- é o **único par contemporâneo útil** da prospecção — mas para uma pergunta
  diferente e mais fraca: *o sítio está a degradar-se para qualquer cultura
  perene, ou só para esta?* Se o efeito fosse do sítio, uma vinha a 87 m no
  mesmo aluvião devia acusá-lo.

**Não controla:**
- espécie (*Vitis*, não *Actinidia*), sistema de condução, compasso (2,72 m
  contra 4,91 m), profundidade radicular, exigência hídrica, calendário de rega;
- origem da água — **não determinada**. Cota média 8,22 m, dois metros acima do
  pomar, e 392 m da margem, o que a coloca noutra posição hidráulica;
- gestão.

**Veredicto:** não é controlo de kiwi. É um par de sítio, e é o melhor que este
raio de 3 km tem para dar.

---

## 5. Quantidades-âncora (`CONTROLOS.md`, controlo 2)

| âncora | declarado | obtido nesta camada | nota |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | não mexida |
| polígono `pomar`, píxeis de 10 m | 2903 | **2891** | contagem por centro de píxel dentro do polígono |
| polígono `pomar`, ha | 29,0 | **28,97** | fórmula de Gauss |
| referência sã (3 manchas), píxeis | 454 | **410** (241 + 96 + 73) | divergência de 44 píxeis; ver abaixo |
| máscara `manchaW`, píxeis | 427 | **424** | |
| máscara `zona0`, píxeis | 220 | **221** | |
| cenas na série | 11 | não recontado | metadado de C0, não tocado aqui |
| cenas de plena estação | 9 | não recontado | idem |
| NDVI médio da referência, 2017-07-02 | 0,838 | **não medido** | regra dura desta sessão |
| NDVI médio da referência, 2026-07-27 | 0,886 | **não medido** | idem |

Sobre a divergência das 454 → 410: os valores obtidos aqui vêm de rasterizar os
**polígonos** de `masks.json` por centro de píxel numa grelha de 10 m alinhada
com a AOI. Os declarados podem vir da contagem booleana da máscara, que inclui
píxeis de bordo. O `CONTROLOS.md` já assinala este conflito conhecido
(2906 / 446 / 423 / 219 na prosa). **Não corrigi nada em silêncio: os três
conjuntos de números são diferentes entre si e a discrepância maior é justamente
na referência sã**, que é a máscara de que dependem as duas âncoras de NDVI.
Quem for medir NDVI a seguir tem de resolver isto primeiro.

Os dois valores de NDVI ficam por medir de propósito. Registá-los aqui exigiria
quebrar a regra que dá valor a tudo o resto desta sessão.

---

## 6. Instrumento independente (`CONTROLOS.md`, controlo 1)

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| C1a/C1b têm entrelinha aberta em 2021 e 2025 | `ctrl_11_varrimento.py`, `ctrl_13_contornos.py`, ortofoto aérea DGT | **OrtoSat2023** (satélite, outro sensor, outra data) por WMS público — `ctrl_15_instrumento_independente.png` | qualitativo |
| C1a/C1b tinham copado fechado em 2012 | ortofoto 2012 a 50 cm | ortofoto 2010 a 50 cm, campanha e câmara distintas — a estrutura já lá está e já é contínua | qualitativo |
| geometria do WMS bate com a do mosaico local | `ctrl_06_leste.py`, teste de registo | recorte da **mesma** janela nos dois produtos, sobrepostos — `ctrl_06_registo.png`: estradas, limites de parcela e linha de água coincidem | < 1 m aparente |
| C2 está na margem direita | `ctrl_17_margem.py`, travessias de água | conversão do centróide para WGS84 e comparação com topónimos públicos (fortaleza de Valença 42,0303 N 8,6424 O; Tui 42,0492 N 8,6459 O) — `ctrl_00_extensoes.py` | inequívoco |
| cotas dos blocos | MDT LiDAR DGT 50 cm | **não confirmado por segundo instrumento.** Só há um MDT. Vai para não testável | ver abaixo |
| áreas dos polígonos | fórmula de Gauss sobre o contorno | contagem independente de píxeis da máscara (`area_mancha_ha` no geojson) — batem a menos de 0,02 ha | ±0,02 ha |
| compasso das linhas | FFT da luminância, `ctrl_16_compasso.py` | contagem directa de linhas a 25 cm nos recortes `ctrl_09_SW*.png` | ±0,2 m |

**Não testável, e assumido como tal:**

- **Cotas.** O MDT LiDAR é a única fonte altimétrica com resolução útil aqui.
  Não há segundo instrumento. As cotas médias vão para o geojson como medidas,
  mas nenhuma conclusão desta adenda depende delas.
- **Origem da água de C1a, C1b, C3.** Não há reservatório, furo, casa de bombas
  ou conduta visível na ortofoto para nenhum dos três. A única infra-estrutura
  hidráulica que a prospecção encontrou é um **reservatório revestido de ~0,3 ha
  em E 530290 / N 4655700**, e esse pertence a C2 — na margem errada. Para os
  blocos da margem esquerda: **não sei, e não há forma de saber por imagem.**
  Precisa do cadastro de captações da APA / ARH-Norte, ou de ida ao terreno.
- **Espécie de C1a e C1b entre 2010 e 2012.** O compasso de 4,5–4,9 m e o fecho
  do copado são compatíveis com latada de kiwi e também com outras fruteiras em
  latada. Não é determinável por estrutura vista de cima.
- **Propriedade.** Não determinada para nenhum bloco.

---

## 7. O que passa para cima

Factos que a camada seguinte pode tratar como dados:

1. `SAIDA_C0\controlos.geojson` — 5 polígonos de candidatos + o rectângulo de
   referência, EPSG:32629, com área, cota, compasso, azimute, distâncias e
   proveniência de cada limite.
2. **Não existe, dentro dos ~3 km cobertos e na margem esquerda portuguesa,
   nenhum segundo pomar de latada em produção.** Qualquer controlo externo
   contemporâneo de kiwi terá de vir de mais longe, e ao vir de mais longe
   deixa de partilhar a origem de água e a gestão.
3. O bloco de ~16 ha a sudoeste é **14,5 ± 1,5 ha**, está a **528 m** do bordo
   do polígono `pomar` (não a 750 m), e **mudou de estrutura entre 2012 e
   2021**.
4. O bloco a sudoeste e o pomar do caso são da **mesma coorte**: ambos ausentes
   em 2004 e em 2007, ambos já no terreno em 2010.
5. **C2 está na margem direita do Minho.** Não pode ser usado. A distância
   euclidiana ao rectângulo declarado (2 m) é enganadora.
6. O polígono `pomar` de `masks.json` não contém água (0,00 ha de 28,97 ha). O
   **rectângulo** dado no enunciado contém 19,6 % de água e não deve ser usado
   para nada além de referência de distância.
7. A contagem de píxeis da referência sã diverge do declarado em 44 píxeis
   (410 contra 454). Assinalado, não corrigido.

Tudo o que não está nesta lista, não passa.

---

## 8. Ficheiros

```
SAIDA_C0\
  controlos.geojson                     polígonos finais, EPSG:32629
  ctrl_00_extensoes.py                  extensão das ortofotos e do LiDAR
  ctrl_01_vista_larga.py     .png       prospecção a 1 m + MDT da janela
  ctrl_02_estrutura.py       .png .csv  detector de periodicidade, 14,2 km²
  ctrl_03_recortes.py        .png       recortes a 25 cm para confirmação
  ctrl_04_lista.py                      relista candidatos ao percentil 93
  ctrl_05_painel.py          .png       painel de 6 épocas por bloco
  ctrl_06_leste.py           .png       WMS OrtoSat2023, sectores E e NE
  ctrl_07_delimitar.py                  mapa de periodicidade fino (4 m)
  ctrl_08_envelope.py                   envelope da estrutura (tentativa)
  ctrl_09_grelha.py          .png       recortes com grelha de 25/50 m
  ctrl_10_poligonos.py       .png       invólucro convexo — C2, C3
  ctrl_11_varrimento.py      .png       varrimento do aluvião em 2021
  ctrl_12_parcelas.py        .png       rectângulo de área mínima (tentativa)
  ctrl_13_contornos.py       .png       contornos finais — C1a, C1b, C1c
  ctrl_14_metricas.py                   cota, distâncias, âncoras, geojson
  ctrl_15_instrumento_...py  .png       OrtoSat2023 + mapa final
  ctrl_16_compasso.py        .json      compasso e azimute por bloco
  ctrl_17_margem.py          .png       componentes de terra (falhou; ver 17b)
  ctrl_17b_travessias.py                travessias de água; água dentro do caso
  ctrl_18_distancias.py      .json      distâncias ao polígono `pomar`
  ctrl_19_geojson_final.py              enriquece o geojson
```

`ctrl_08` e `ctrl_12` ficam no directório apesar de terem sido abandonados: o
envelope morfológico e o rectângulo de área mínima atravessavam faixas de pousio
e apanhavam telhados. Ficam porque um adversário deve poder ver o que foi
tentado e porquê foi trocado, e não só o método que sobreviveu.
