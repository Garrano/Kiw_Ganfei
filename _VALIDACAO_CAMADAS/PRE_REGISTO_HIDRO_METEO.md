# Pré-registo · duas camadas novas — hidrologia e meteorologia×fenologia

**10-09-2026.** Escrito **antes** de descarregar ou correr fosse o que for, como
a C9 exige. A C9 já foi violada duas vezes neste processo, as duas por eu correr
primeiro e escrever o critério depois.

Duas camadas, pedidas pelo analista:

- **H** — o nível do rio e o freático no período em que o declínio começou;
- **M** — meteorologia sobre a série de satélite, justaposta aos estados
  fenológicos do kiwi, para caracterizar esse período.

Ambas têm de passar por certificação e adversário antes de entrar seja onde for.

---

## 0 · O que já está em disco, e o que não está

Corrido com `ja_existe.py` antes de desenhar (S1).

| | estado |
|---|---|
| **chuva diária** | **existe, parcial.** `sar_ano_inteiro_dedup.csv` traz `dias_desde_chuva5`, `chuva_7d_mm`, `chuva_30d_mm` — mas **só nas datas de passagem do Sentinel-1**, não em série diária contínua. Fonte: open-meteo. E o `IX-06` obriga a excluir o primeiro ano hidrológico |
| **rede de estações EMC** | **não cobre o período.** A mais próxima de Valença é **Monção–Valinha**, no mesmo vale do Minho — e está **desactivada**, com ficheiro de 2008. Ponte de Lima–Refóios, activa, tem pluviosidade até 2011. O declínio é de 2021 em diante |
| **fenologia da actinídea** | **existe, e não é daqui.** `FENOLOGIA DA ACTINÍDEA…xlsx`, quatro locais: Celorico de Basto, Resende, Santo Tirso, Vila do Conde. **Nenhum no vale do Minho**; o mais próximo a ~80 km |
| **nível do rio / freático** | **nada em disco.** Tem de vir de fonte externa |
| **cota do terreno** | **existe e é boa.** `b.Z` do MDT LiDAR da DGT. Os dez pontos de colheita estão a **6,47 – 8,11 m** |

---

## 1 · CAMADA H — o rio e o freático

### 1.1 A pergunta, fixada

> Durante a janela em que o declínio começou, **a água esteve suficientemente
> alta, e tempo suficiente, para asfixiar raiz de kiwi nas cotas onde estão as
> manchas?**

Unidade: **o dia**. Fronteira: os polígonos das manchas, cotas 6,4 – 8,2 m.
«Suficientemente alta» e «tempo suficiente» definem-se em 1.3, antes de olhar
para dados.

### 1.2 A CONDIÇÃO BLOQUEANTE, e é a que mata isto se for ignorada

> **Nenhuma comparação entre nível de rio e cota de terreno se faz sem um
> DATUM COMUM declarado e verificado.**

Uma leitura hidrométrica em «metros acima do zero da escala» **não é comparável**
com uma cota do MDT em metros acima do nível médio do mar. A diferença entre os
dois é o zero da escala, que é um número que tem de ser obtido e escrito.

**Se o zero da escala não for obtido, a camada H para aqui e diz-se que parou.**
Não se estima, não se assume, não se «calibra pela cheia conhecida». Este dossiê
já foi apanhado a comparar unidades diferentes — o `IX-22` é disso.

Segunda ressalva, do mesmo tipo: **o Minho é tidal em Valença**. Uma série de
nível sem maré separada mistura dois sinais com períodos completamente
diferentes, e a maré não afoga raiz nenhuma a 7 m de cota.

### 1.3 Os critérios, todos antes de correr

| | critério | limiar | de onde vem |
|---|---|---|---|
| **H-A** | datum comum obtido e escrito | **obrigatório** | 1.2 — sem ele nada mais corre |
| **H-B** | série diária de nível cobre 2019–2026 com < 10 % de falhas | ≥ 90 % | uma série com buracos não mede duração |
| **H-C** | maré separada do caudal | declarado | 1.2 |
| **H-D** | «episódio de risco» = nível a **menos de 1,5 m abaixo** da cota da mancha durante **≥ 5 dias consecutivos** | — | 1,5 m é a profundidade radicular efectiva típica do kiwi em solo aluvionar; 5 dias é o limiar de hipoxia radicular usado na literatura de KVDS. **Ambos os números têm de ser confirmados na bibliografia do dossiê antes de valerem** — se não se confirmarem, o critério é reescrito ANTES de correr, e regista-se |
| **H-E** | contraste: os episódios de risco são **mais frequentes ou mais longos** nas cotas das manchas do que nas cotas do pomar são | diferença declarada com incerteza | senão o rio explica o pomar todo e não explica a mancha |

### 1.4 O que falsifica a hipótese hidrológica

Se, entre 2019 e o início do declínio, **nunca houve episódio de risco** pelo
critério H-D nas cotas das manchas, **a via do rio não explica o arranque do
declínio** — e isso é um resultado, não uma falha. Fecha uma hipótese que hoje
está aberta e que custa dinheiro drenar.

### 1.5 Fontes a tentar, por ordem, e o que cada uma resolve

1. **SNIRH** (APA) — estações hidrométricas e **piezómetros**. Um piezómetro é a
   medição directa do freático e dispensa toda a inferência de 1.2. Se existir um
   no aluvião do Minho perto de Valença, é o instrumento certo e o resto é
   secundário.
2. **Confederación Hidrográfica Miño-Sil** — o Minho é internacional; as escalas
   do lado espanhol (Tui, Salvaterra) podem ter série melhor.
3. **Reanálise/modelo** só como último recurso, e declarada como tal: não mede
   freático, modela escoamento.

---

## 2 · CAMADA M — meteorologia × fenologia

### 2.1 A pergunta, fixada

> **Que tempo fez na janela em que o declínio começou, e em que estado
> fenológico apanhou a planta?**

É **caracterização**, não teste de causa. Isso importa porque muda o que se pode
escrever no fim: descreve-se a coincidência, não se atribui.

### 2.2 A ressalva que viaja com a camada toda

> **Não temos fenologia de Ganfei. Temos fenologia regional de quatro locais, o
> mais próximo a ~80 km, nenhum no vale do Minho.**

Transferir isso para Valença é uma suposição, e mede-se:

**M-A · teste de transferência regional.** Para cada estado fenológico e cada
ano com dois ou mais locais observados, calcular a **amplitude entre locais em
dias**. Se a mediana dessa amplitude for **> 14 dias**, a transferência regional
não é defensável e os estados entram na prancha como **banda**, nunca como data.
Se for ≤ 14 dias, entram como banda de amplitude medida — **nunca como linha**.

### 2.3 Os critérios

| | critério | limiar |
|---|---|---|
| **M-A** | transferência regional (acima) | mediana da amplitude entre locais |
| **M-B** | a série meteorológica cobre 2016–2026 em passo diário, com fonte única e declarada | sem mistura de fontes na mesma série |
| **M-C** | as variáveis são as pedidas e nada mais: **temperatura (máx/mín), precipitação, e radiação/insolação**. Cada uma com unidade e origem escritas | — |
| **M-D** | a série meteorológica é **cruzada com as datas das cenas de satélite que já estão certificadas**, não com cenas novas | senão introduz-se um instrumento por auditar dentro de uma camada nova |

### 2.4 O que esta camada NÃO pode concluir

Não pode atribuir o declínio ao tempo. Com **um** pomar, **um** episódio e sem
controlo externo — e o `DEC-04` retirou o único controlo interno que havia —
qualquer coincidência entre tempo e quebra é **compatível com** a hipótese
climática e com todas as outras. A camada serve para **descrever a janela** e
para **excluir**: se não houve nada de anormal no tempo, a via climática perde
peso relativo.

---

## 3 · O adversário

Corre depois de cada camada, vê este documento antes, e é-lhe posto:

1. O datum foi mesmo obtido, ou foi assumido? Mostra a fonte.
2. A maré foi separada? Como se verificou?
3. Os limiares 1,5 m e 5 dias vieram da bibliografia do dossiê, ou foram
   escolhidos depois de ver a série?
4. A amplitude entre locais de fenologia foi calculada antes ou depois de se
   desenhar a prancha?
5. Alguma série mistura fontes sem o dizer?
6. A camada conclui alguma coisa que o §2.4 proíbe?

---

# 4 · Progresso, 10-09-2026 · CAMADA H

## 4.1 Candidatos identificados, por distância à origem do declínio

Do inventário de estações hidrométricas do SNIRH (dados abertos, 692 + 338
pontos, lido com leitor próprio de shapefile). Distância a E530977 N4655117:

| distância | código | nome | estado |
|---|---|---|---|
| **10,0 km** | **01F/03H** | **MAZEDO** | **DESATIVADA** — tem *nível instantâneo* e *nível médio diário* |
| **11,0 km** | **01G/05H** | **MONÇÃO** | **ATIVA** |
| 19,4 km | 01G/04H | SEGUDE | ativa |
| 19,6 km | 01G/02H | FOZ DO MOURO (EDP) | ativa |

> **Não há estação hidrométrica activa em Valença.** A mais próxima no Minho é
> Monção, **11 km a montante**.

## 4.2 H-A NÃO SATISFEITA — e a camada pára aqui, como estava escrito

A ficha de estação do SNIRH é um **portal de consulta**: dá os parâmetros com
dados, e **não publica a cota do zero da escala**. Sem esse número, nenhuma
leitura de nível se compara com a cota do terreno — e as cotas dos pontos de
colheita são conhecidas ao centímetro (6,14 a 8,16 m).

**Isto não se estima e não se calibra por cheia conhecida.** O §1.2 declarou-o
bloqueante antes de se procurar, e mantém-se.

**Vias para o destravar, por ordem:**

1. **Pedido à APA** — cota do zero da escala de 01G/05H e 01F/03H, e datum
   altimétrico de referência. É um email, e é a via limpa.
2. **Piezómetro.** A rede de águas subterrâneas é um conjunto de dados
   **separado**, que não está no inventário hidrométrico e ainda não foi
   localizado. Um piezómetro no aluvião mede o freático **directamente** e
   dispensa toda a inferência de nível de rio — continua a ser o instrumento
   certo, e vale mais procurá-lo do que resolver o datum de uma escala.
3. **Lado espanhol** — Confederación Hidrográfica Miño-Sil, escalas em Tui e
   Salvaterra, frente a Valença.

## 4.3 A ressalva da maré continua de pé, e agora tem número

Monção fica **11 km a montante** de Valença. O limite da maré no Minho anda pela
zona de Valença/Tui, o que significa que Monção pode estar **acima** dele e
Ganfei **abaixo** — ou seja, a estação e o pomar podem estar em regimes
diferentes. Isto tem de ser verificado antes de qualquer transferência de nível
entre os dois, e não se resolve com a série: resolve-se com a documentação do
regime.

## 4.4 Estado

**CAMADA H: PARADA na condição bloqueante, como previsto.** Candidatos
identificados e distâncias medidas; nenhuma leitura de nível feita, nenhuma
comparação com cota feita. Nada desta secção é citável como resultado — é
inventário.

## 4.5 O lado espanhol — e a resposta é diferente para cada camada

Tui fica **em frente a Ganfei, a ~2 km**, contra os 11 km de Monção. Valia
perguntar. Mas o ganho não é onde se esperava.

### Para o RIO (camada H): Espanha não aproxima nada

| estação | rio | distância | nota |
|---|---|---|---|
| **A044 · Tui** | **rio LOURO** | ~2 km | **é um afluente, não o Minho.** Serve como indicador local de escoamento; **não** serve para o nível do Minho |
| **N015 · Salvaterra do Miño** | Minho | ~11 km a montante | imagem ao espelho de Monção, na outra margem |

> **No canal principal do Minho não há estação na secção Tui–Valença.** As duas
> mais próximas, uma de cada país, estão ambas a ~11 km a montante. A hipótese
> de que o lado espanhol resolvia a distância **não se confirma.**

**O que o lado espanhol PODE resolver é outra coisa, e é a que bloqueia:** o
*anuario de aforos* do MAPAMA publica as características das estações,
**incluindo a cota do zero da escala** — que é exactamente a condição **H-A**.
Se a série a usar vier a ser a espanhola, o datum vem publicado em vez de
depender de um pedido. **Vale mais por isto do que pela distância.**

### Para a METEOROLOGIA (camada M): Espanha resolve o problema

| | do lado português | do lado galego |
|---|---|---|
| estação mais próxima | Monção–Valinha, **desactivada**, ficheiro de 2008 | **Tui (Areas)** e **Salvaterra (Meder)**, MeteoGalicia |
| distância | 11 km | **~2 km** (Tui) |
| cobertura do período do declínio | **nenhuma** — a rede EMC pára em 2011 | **até ao presente** |
| série longa | — | **O Rosal (AEMET 1730E): diária desde 1989**, horária desde 2019 |
| descarga | — | CSV e JSON |

> **A rede galega cobre o que a portuguesa não cobre, e a 2 km em vez de 11.**
> Tui está no mesmo vale, no mesmo aluvião, na margem oposta.

**Ressalva que a M-B obriga a declarar:** atravessar a fronteira muda de rede, de
instrumento e de rotina de validação. Se a série for MeteoGalicia, é
MeteoGalicia **do princípio ao fim** — não se emenda com dados portugueses a
meio, que é precisamente o que a M-B proíbe.

### Estado das duas camadas, 10-09

- **H — PARADA em H-A.** Candidatos identificados dos dois lados; o datum não
  está publicado do lado português. Próximo passo: ou pedido à APA, ou o
  *anuario de aforos* espanhol, ou — melhor que ambos — localizar um piezómetro,
  que ainda não foi encontrado porque a rede de águas subterrâneas é um conjunto
  de dados separado.
- **M — desbloqueada do lado meteorológico, bloqueada do lado fenológico.** A
  meteorologia resolve-se com MeteoGalicia. A fenologia não: o `IX-26` mostrou
  que a transferência regional portuguesa não é defensável, e a via aberta é a
  **Estación Fitopatolóxica Areeiro**, que faz seguimento fenológico de kiwi a
  ~50 km e já é contraparte deste processo.

---

# 5 · CAMADA H · o piezómetro existe — e mede o aquífero errado

## 5.1 O que se encontrou

Rede de quantidade das águas subterrâneas do SNIRH (1242 pontos, dados abertos).
Três piezómetros a menos de 20 km de Ganfei:

| | distância | estado | **sistema aquífero** |
|---|---|---|---|
| **3/N2** | **9,9 km** | **INACTIVA** | A0 — Maciço Antigo Indiferenciado |
| 3/N3 | 14,4 km | INACTIVA | A0 — Maciço Antigo Indiferenciado |
| 3/N1 | 19,5 km | ACTIVA | A0 — Maciço Antigo Indiferenciado |

## 5.2 Porque nenhum serve

> **Os três medem o `A0 — MACIÇO ANTIGO INDIFERENCIADO`: rocha fracturada.
> Ganfei está em ALUVIÃO** — «alluvial soils heavily disturbed/mixed during land
> consolidation ~35 years ago» (§1 do enquadramento).

São **aquíferos diferentes**, com comportamento diferente. Um nível de água em
granito fissurado a 10 km não diz o que faz a toalha freática num terraço
aluvionar junto ao rio: a recarga, a transmissividade e a resposta à cheia não
têm relação nenhuma entre os dois.

E acresce que **o mais próximo está inactivo**; o único activo está a 19,5 km e
é do mesmo aquífero errado.

> **Não existe piezómetro no aluvião do Minho perto de Ganfei.** O instrumento
> directo — o que dispensava toda a inferência da §1.2 — **não existe para este
> sítio.**

## 5.3 O que isto faz à camada H

Fecha a via barata e deixa duas:

1. **Nível do rio + datum**, com toda a cadeia de inferência que a §1.2 declara,
   e com a ressalva da maré por resolver. Continua bloqueada em **H-A**.
2. **Medir no sítio.** E isto já está planeado: **as covas de perfil da `DEC-08`
   atingem a toalha freática se ela for pouco profunda.**

## 5.4 A consequência prática, e é a que interessa

> **As covas SÃO o piezómetro.** A campanha de campo é a única via que este caso
> tem para medir o freático onde ele importa — debaixo das plantas, à cota das
> plantas, no aquífero das plantas.

Isso acrescenta requisitos à campanha, e têm de entrar na ficha de campo (T5):

- **profundidade ao nível da água em cada cova**, medida e datada, com a hora
  (o rio é tidal em Valença — se houver influência, vê-se na hora);
- **cota da boca da cova** por GPS, senão a leitura não se compara entre covas
  nem com a cota do terreno;
- **sinais de hidromorfia por horizonte** — gleização, mosqueado, concreções —
  que registam o regime de água **do passado**, e não só o do dia da visita;
- **profundidade e espessura de qualquer camada compactada**, com resistência à
  penetração;
- e, se a cova for reaproveitável, **deixar tubo de observação** — transforma uma
  medição única numa série, que é o que falta a este caso.

**Sem isto, a campanha responde à biologia e deixa a hipótese abiótica onde ela
está há um mês: a melhor do dossiê e a única sem um único teste.**

---

# 6 · CAMADA M · a estação existe, e está a 5 km

## 6.1 As candidatas, por distância à origem do declínio

Rede da MeteoGalicia, 169 estações com geometria (serviço aberto, sem chave).

| distância | estação | id | nota |
|---|---|---|---|
| **5,2 km** | **Sobrada** | 10177 | Tomiño, no vale. **Estação principal** |
| 5,7 km | Monte Aloia | 10060 | Tui — mas é o **monte**, não o vale; sem valor como análogo do pomar |
| 5,7 km | Entenza | 19054 | Salceda de Caselas |
| 10,9 km | Atios | 10165 | O Porriño, principal |
| 16,9 km | Meder | 19057 | Salvaterra do Miño |

**Comparação com o lado português:** Monção–Valinha, a 11 km, **desactivada, com
ficheiro de 2008**; Ponte de Lima, pluviosidade até 2011. Do nosso lado não há
nada que cubra o período do declínio.

> **Sobrada, a 5,2 km, com série corrente, contra nada a menos de 11 km e nada
> depois de 2011 do lado de cá.**

## 6.2 O que estas estações medem, e há mais do que se pediu

A **Paramos**, em Tui, aparece no serviço de dez minutos com um conjunto
agrometeorológico que serve directamente este caso:

| | |
|---|---|
| temperatura | a **1,5 m** e a **0,1 m** |
| chuva | `PP_SUM_1.5m` |
| **humidade do solo** | **`HS_CV_AVG_-0.2m`, m³/m³, a 20 cm** |
| temperatura do solo | a −0,1 m |
| humidade foliar | horas acumuladas |
| vento, pressão, humidade relativa | sim |

**A humidade do solo a 20 cm não é o freático** — não mede toalha, mede o regime
hídrico do horizonte superficial. Mas é a medição mais próxima do encharcamento
que este caso tem sem ir ao terreno, e **não estava prevista no pedido**.

**Falta a radiação/insolação**, que o analista pediu. Não aparece na lista de
Paramos; tem de ser procurada estação a estação, e pode obrigar a uma segunda
estação — o que a **M-B proíbe misturar na mesma série**.

## 6.3 O que falta verificar antes de descarregar seja o que for

1. **Sobrada mede o quê, e desde quando?** A lista de parâmetros acima é de
   Paramos, não de Sobrada. Não se assume que são iguais.
2. **A cota da estação.** Uma estação a meia encosta não é análogo de um terraço
   aluvionar a 7 m. Se Sobrada estiver alta, Paramos ou outra do fundo do vale
   vale mais, mesmo que fique mais longe.
3. **Paramos não aparece no serviço de dados diários** — só no de dez minutos.
   Perceber se tem série diária publicada, ou se obriga a agregar dos dez
   minutos, que é outra decisão a declarar.

## 6.4 Estado

**M — desbloqueada na meteorologia, com três verificações por fazer antes de
descarregar. Continua bloqueada na fenologia** (`IX-26`), e a via é Areeiro.

---

# 7 · CAMADA M · a fenologia de kiwi em Areeiro — existe, e é prosa

## 7.1 O que se varreu

Boletins fitossanitários da Estación Fitopatolóxica Areeiro, arquivo de **2018 a
2026**, com URL limpo por data (`/-/aviso-fitosanitario-DD-MM-AAAA`). Varridos
os anos 2022–2026 (~24 boletins/ano). Um pedido por segundo, com identificação.

## 7.2 O kiwi É cultura coberta — várias vezes por ano

A barra lateral de cada ano lista as culturas de cada boletim, e o kiwi aparece
com regularidade. Exemplos: **2025** — 2, 8 e 15 de Maio; **2026** — 10 de
Fevereiro, 1 e 16 de Abril.

## 7.3 Mas o estado fenológico do kiwi NÃO vem em BBCH

É a diferença que decide o que se pode desenhar. Comparar:

| cultura | como o estado é dado |
|---|---|
| **viña** (albariño) | **`Estado fenolóxico: G-(H). BBCH: 55-57`** — código, datado |
| **kiwi** | **prosa**: *«cos botóns florais desenvolvidos»*, *«polo menos ata a apertura da flor»* |

> **A fenologia de kiwi de Areeiro ancora a FASE, não a data.** Serve para dizer
> «nesta semana, na região, o kiwi estava com botão floral desenvolvido». Não dá
> um código por data.

E **não declara cultivar** na secção de kiwi — o que, num caso onde Ganfei tem
summerkiwi, Enza Gold e Erica, é uma ressalva viva.

## 7.4 Como se compara com a via portuguesa, que o IX-26 fechou

| | Santo Tirso (PT) | Areeiro (ES) |
|---|---|---|
| distância a Ganfei | ~100 km | **~50 km** |
| região bioclimática | interior do Porto | **baixo Minho / Rías Baixas — a mesma** |
| cobertura do período | 2014–2026, esparsa | **semanal na estação, 2018–2026** |
| forma do dado | Baggiolini + BBCH | **prosa** |
| cultivar | Hayward | não declarada |
| amplitude entre locais | **não calculável** (nenhum ano tem dois locais) | não aplicável — é um local |

**Nenhuma das duas permite medir a amplitude entre locais**, que era o teste
M-A. Logo, em qualquer dos casos, **os estados entram na prancha como banda,
nunca como data** — e com Areeiro a banda é mais larga, porque a fonte é prosa.

## 7.5 O achado lateral, e pode valer mais do que a fenologia

A secção de kiwi dos boletins é sobretudo sobre **bacterioses** — e o gestor
declarou que a **PSA nunca foi encomendada porque os sintomas não eram
compatíveis** (`D6` da `LISTA_FINAL`, tipo 1).

> Os boletins de Areeiro dão, semana a semana e ano a ano, a **pressão regional
> de bacteriose em kiwi** do outro lado do rio. Isso é contexto epidemiológico
> que este processo não tem por nenhuma outra via, e é gratuito.

## 7.6 Estado

**M — fenologia: fonte identificada, qualidade medida, e é mais fraca do que se
esperava.** Ancora fase, não data; sem cultivar; entra como banda.

**O seguimento fenológico anual de kiwi que a própria Areeiro declara fazer NÃO
está nestes boletins.** Se existir em forma tabelada, **tem de ser pedido** — e
o pedido tem base, porque a Areeiro já é contraparte deste processo pelo
relatório 331/2025.

---

# 8 · CAMADA M · juntar as duas fontes de fenologia — o que dá e o que não dá

## 8.1 A ideia, e porque era boa

Com **duas** fontes independentes a reportar o mesmo evento no mesmo ano, a
diferença entre elas **é** a margem de erro — e o teste `M-A`, que ficou
incalculável por nenhum ano ter dois locais, passaria a ter n.

## 8.2 Não dá: as duas fontes nunca coincidem no ano

| fonte | anos com floração (BBCH 59–65) |
|---|---|
| Santo Tirso (PT), Hayward | **2016, 2017, 2021, 2023** |
| Areeiro (ES), sem cultivar declarada | **2018, 2019, 2025** |

> **Sobreposição: zero.** O `M-A` continua incalculável — e agora sabe-se que
> não é por falta de fontes, é por falta de coincidência.

## 8.3 O que dá: cobertura combinada, e um piso de incerteza que se mede

**Cobertura.** Juntas, as duas dão âncora de floração em **sete anos**:
2016, 2017, **2018**, **2019**, 2021, 2023, **2025**. Isso é utilizável — desde
que a proveniência de cada ano viaje com o ponto, porque **anos diferentes vêm
de sítios diferentes**, e isso é uma fonte de erro que não existe numa série de
um só sítio.

**Piso de incerteza, medido.** As datas de Areeiro **não são datas de
observação**: são datas de boletim. «Apertura da flor» num boletim de 25-05
quer dizer que a floração decorria por volta dessa semana — não que começou
nesse dia. A série está **censurada por intervalo ao calendário semanal**, o que
lhe dá **±7 dias por construção**, antes de qualquer transferência espacial.

Comparar as amplitudes ilustra-o:

| | amplitude interanual da data de floração |
|---|---|
| Santo Tirso (datas de observação) | 5 a 16 de Maio — **11 dias** |
| Areeiro (datas de boletim) | 17 de Abril a 25 de Maio — **38 dias** |

A diferença não é toda biologia: parte é a censura semanal e parte é o facto de
o boletim só falar de kiwi quando há razão fitossanitária para isso.

## 8.4 O orçamento de erro, declarado por parcelas

| termo | valor | estatuto |
|---|---|---|
| censura ao calendário de boletim (Areeiro) | **±7 dias** | **medido** |
| transferência espacial Pontevedra → Valença (~50 km) | ? | **não medido** |
| transferência espacial Santo Tirso → Valença (~100 km) | ? | **não medido** |
| desencontro de cultivar (Hayward vs summerkiwi/Enza Gold/Erica) | ? | **não medido** |

> **Só o primeiro termo é mensurável com o que temos.** A banda mínima
> defensável é **±7 dias**, e a banda verdadeira é maior por um valor que não
> sabemos. Isto **não** desqualifica a camada — obriga-a a entrar como banda com
> o termo espacial declarado como desconhecido, que é diferente de fingir que
> não existe.

## 8.5 O que fecharia a lacuna, e é barato

O `M-A` original — amplitude **entre locais no mesmo ano** — fica calculável
assim que **um** ano tiver as duas fontes. Duas vias:

1. **Rever os 13 boletins de Areeiro que têm secção de kiwi mas nenhuma frase
   que a tabela apanhou.** Se algum for de 2016, 2017, 2021 ou 2023, o teste
   passa a ter n.
2. **Pedir a Areeiro o seguimento fenológico anual tabelado** — que a estação
   declara fazer e que não está nos boletins. Se cobrir os anos do registo
   português, o `M-A` fica com vários pontos em vez de um.

---

# 9 · CAMADA H · a rede confirmada por segunda via, e uma correcção minha

## 9.1 Confirmação independente do inventário

O serviço REST do SNIAmb (`Estacoes_monitorizacao_aguas_subterraneas`, camada
«Ponto de observação») devolve, numa caixa de ~25 km à volta de Ganfei,
**exactamente os mesmos quatro pontos** que o shapefile de dados abertos:

| distância | ref | tipo | estado |
|---|---|---|---|
| 9,9 km | 3/N2 | piezómetro | **inactiva** |
| 14,3 km | 7/N1 | nascente | inactiva |
| 14,4 km | 3/N3 | piezómetro | inactiva |
| **19,5 km** | **3/N1** | **piezómetro** | **ACTIVA** |

Duas vias independentes, o mesmo resultado. **Não há mais rede de monitorização
de águas subterrâneas perto de Ganfei do que isto.**

## 9.2 CORRECÇÃO — a minha objecção do §5.2 estava mal fundamentada

Escrevi que os piezómetros **«medem o aquífero errado»** porque estão no
`A0 — Maciço Antigo Indiferenciado` e Ganfei está em aluvião. Fui verificar
contra a carta de unidades hidrogeológicas, e:

| ponto | unidade |
|---|---|
| **GANFEI** | **A1 · A — Maciço Antigo** |
| 3/N2 | A1 · A — Maciço Antigo |
| 3/N1 | A1 · A — Maciço Antigo |

> **À escala da carta nacional, Ganfei está na MESMA unidade que os piezómetros.**
> O argumento «aquífero diferente», tal como o escrevi, **não se sustenta contra
> esta fonte** e fica retirado.

**O que é verdade, e é outra coisa:** a carta nacional é uma classificação
grosseira que arruma no «Maciço Antigo» tudo o que não é bacia sedimentar
reconhecida. **Não tem polígono para o aluvião do Minho.** Que o código seja o
mesmo não prova que a hidrogeologia local debaixo do pomar seja rocha fracturada
— prova que a carta não distingue.

## 9.3 O que continua a valer, e sobre outros fundamentos

- **Distância**: 9,9 km o mais próximo, **19,5 km o único activo**.
- **Um terraço fluvial a 6–8 m tem uma toalha ligada ao rio**; um piezómetro em
  meio fissurado a 10–20 km não a segue. Isto continua a ser verdade — mas
  **agora é uma afirmação sobre a geologia LOCAL, que eu ainda não demonstrei**,
  e não sobre o código da carta.
- **Fecha-se com o LNEG**: a base de dados de recursos hidrogeológicos tem as
  fichas dos pontos de água com **litologia do furo**. É isso que mostra se há
  aluvião, com que espessura, e se algum furo perto de Ganfei o atravessa. O
  geoportal do LNEG não respondeu ao endereço REST que tentei; é o passo
  seguinte, por outra via.

## 9.4 Onde isto deixa a camada H

Sem alteração no essencial: **H continua parada em H-A**, e **as covas de
perfil continuam a ser o instrumento real**. O que mudou foi a qualidade do
argumento — deixei de o ter apoiado numa leitura errada da carta.

---

# 10 · CAMADA H · o LNEG tem sondagens com log a 1,7 km

## 10.1 A via, e como se lá chega

A base de dados de recursos hidrogeológicos do LNEG não tem serviço WFS nem
ArcGIS REST — os endereços tentados dão 404. Tem uma **API própria do portal**:

```
POST https://geoportal.lneg.pt/umbraco/HydrogeologicalResourcesDBPlugin/
     HydrogeologicalResourcesDBApi/GetTableData
corpo:  {"carta":"2","length":200,"start":0}
```

A pesquisa é por **carta geológica**, e a **`002 — VALENÇA`** é a folha de
Ganfei. Devolve **36 pontos de água**, com coordenadas, freguesia, unidade,
objectivo, uso, número de relatório e um sinalizador de repositório disponível.

## 10.2 O que há perto

| distância | ref | tipo | freguesia | relatório | log disponível |
|---|---|---|---|---|---|
| **1,68 km** | **2S0001** | sondagem | Valença | **22117** | **sim** |
| **1,99 km** | **2S0002** | sondagem | Valença | **22117** | **sim** |
| 2,74 km | 2S0008/9/10 | sondagem | Valença | 22365 | sim |
| 3,5–3,7 km | 2S0021…2S0033 | sondagem | Cristelo Covo | 28172 | sim |

As de 1,7 e 2,0 km são de **prospecção para abastecimento público**; o grupo de
Cristelo Covo é **reconhecimento geotécnico** — que costuma trazer perfil com
espessura de cobertura e resistência, exactamente o que interessa.

## 10.3 O que isto fecha e o que não fecha

**Fecha a dúvida sobre a existência do instrumento.** Eu tinha escrito que a
afirmação «um terraço a 6–8 m tem toalha ligada ao rio e o piezómetro em meio
fissurado a 10–20 km não a segue» era **uma afirmação sobre geologia local que
não estava demonstrada**. Os logs que a demonstram ou refutam **existem, estão a
1,7 km, e estão assinalados como disponíveis**.

**Não fecha a afirmação.** Os logs ainda não foram lidos: os endereços de
detalhe do portal não são adivinháveis e o repositório serve-se pela interface
ou por pedido ao LNEG. **Até serem lidos, a afirmação continua por demonstrar** e
não entra em lado nenhum.

**E confirma que a unidade hidrogeológica não serve para nada aqui:** os 36
pontos, incluindo os de Cristelo Covo e os de Valença, estão **todos**
classificados «Maciço Antigo» — o mesmo código de Ganfei. A carta nacional não
distingue aluvião, e já não é argumento em nenhum sentido.

## 10.4 Próximo passo, concreto

Obter os relatórios **22117** (1,7 km, dois furos) e **28172** (3,5 km, treze
sondagens geotécnicas) e ler, em cada um: **espessura de cobertura aluvionar,
litologia por profundidade, e nível de água encontrado durante a perfuração**.
Três números por sondagem, e a hipótese abiótica passa a ter substrato medido em
vez de suposto.

---

# 11 · CAMADA H · o que a base do LNEG dá, e onde pára

## 11.1 Só DUAS sondagens estão à cota do pomar

Os pontos de colheita estão a **6,14–8,16 m**. Das dez sondagens mais próximas:

| dist | ref | **cota** | perfurada até | ano | relatório |
|---|---|---|---|---|---|
| **1,68 km** | **2S0001** | **8,00 m** | **−27,60 m** | 1964 | 22117 |
| **1,99 km** | **2S0002** | **9,00 m** | −15,50 m | 1964 | 22117 |
| 2,74 km | 2S0008/9/10 | **20 m** | −8 a −11,7 m | 1966 | 22365 |
| 3,5–3,7 km | 2S0021…2S0033 | **26–31 m** | −31 a −35 m | 1993 | 28172 |

> **O grupo geotécnico de Cristelo Covo, que parecia o mais promissor por serem
> treze sondagens com perfil, está a 26–31 m de cota — encosta, não terraço.
> Não é análogo do substrato do pomar.**
>
> **As únicas duas à cota do terraço são a 2S0001 e a 2S0002.**

## 11.2 Um indício, e é só isso

A **2S0001**, à cota 8,00 m, muda de diâmetro a **−20,69 m** e outra vez a
−26,40 m. Telescopar assim é o que se faz ao entubar material solto antes de
entrar em rocha — o que sugere **~20 m de cobertura não consolidada** sob o
terraço.

**Não se cita.** Três razões:

1. a base **não tem litologia** — só diâmetros e profundidades;
2. **as unidades do campo de diâmetro são inconsistentes entre registos**
   (0,521 / 20,84 / 108 no mesmo campo), logo a leitura «521 mm» é
   interpretação minha;
3. a 2S0002, à cota 9 m e a 300 m dela, tem **um só troço até −15,50 m** — o que
   não contraria mas também não confirma.

É **hipótese que o relatório fecha**, não achado.

## 11.3 Onde pára: os relatórios exigem registo

O portal serve o PDF por:

```
/umbraco/Surface/DownloadSurface/RequestDownload?nodeid=1193
    &filename=<idTecniBase>&code=<referencia>&registerForm=True&...
```

Testado: **HTTP 403**, e o `GetVisibleReport` devolve **false** — os relatórios
não estão abertos. **Não se cria conta**: é decisão de quem manda, e é a CCDR-N
que tem legitimidade institucional para o pedido.

## 11.4 O pedido a fazer, e é curto

> **Relatório LNEG 22117** — *«Relatório final sobre os furos de pesquisa de água
> em Valença»*, 1993, e as sondagens **2S0001** e **2S0002**, executadas por
> Johann Keller em 15-05-1964.
>
> Ler, em cada uma: **espessura da cobertura aluvionar, litologia por
> profundidade, e nível de água encontrado na perfuração.**

São dois furos à cota do terraço, a menos de 2 km. Com esses três números, a
hipótese abiótica deixa de assentar em suposição sobre o substrato.

## 11.5 Como repetir a consulta

```
POST /umbraco/HydrogeologicalResourcesDBPlugin/HydrogeologicalResourcesDBApi/GetTableData
     {"carta":"2","length":200,"start":0}            → 36 pontos da folha Valença
GET  .../GetDetails?idpa=<idpa>                       → ficha, cota, construção
```
