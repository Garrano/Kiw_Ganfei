# GEORREFERENCIAÇÃO DO ESQUEMA DE REGA — CONTROLO 3, ADVERSÁRIO

**Data:** 04-09-2026 · **Mandato:** encontrar o erro, não confirmar.
**Alvo:** `georref_por_bloco.py` e as peças escritas antes do facto da escala.
**Instrumentos usados, todos diferentes do que produziu o alvo:** detecção dos
círculos por filtro de anel; contagem da máscara por vizinhança; reajuste com a
tinta das válvulas retirada; Monte Carlo do critério; leitura das etiquetas por
ampliação directa do `scan.jpeg`; comparação de áreas e perímetros.

Ficheiros de trabalho no scratchpad da sessão (`c3_mask.py`, `c3_valv2.py`,
`c3_refit.py`, `c3_diag.py`, `c3_poder.py`, `c3_over.py`). **Nenhum ficheiro do
processo foi alterado.**

---

## LINE-STOP

### LS-1 · A máscara `linha` é maioritariamente tinta das válvulas. O «controlo independente» não é independente.

`georref_por_bloco.py:31-33` afirma:

> «Controlo independente — **nenhuma válvula entra no ajuste**»

É falso. A máscara construída em `georref_por_bloco.py:112-117`

```
linha = (R - G > 18) & (R - B > 6) & (R > 90) & (R < 215) & (G < 175)
```

apanha os **dezassete** círculos vermelhos das válvulas e os algarismos dentro
deles. Medido:

| | px |
|---|---|
| máscara total (`ys < 900`), como no ficheiro | **8 989** |
| a menos de 25 px de um centro de válvula | **4 409 — 49,0 %** |
| a menos de 28 px de um centro de válvula | **5 026 — 55,9 %** |

Não é contaminação marginal: **é a maioria da fonte do ajuste.** As quinze
maiores componentes conexas da máscara são todas anéis de válvula (ex.: a
componente 56, 191 px, bbox x 1118-1146 / y 362-403 — é o círculo da v7).

Consequência directa, e é o line-stop: as contagens **6/12** e **3/5** que o
critério usa como controlo são calculadas sobre pontos cuja tinta já entrou no
ajuste. Não medem concordância independente; medem quão bem o ICP conseguiu
pousar a nuvem de tinta sobre as parcelas. **Isto é a família A da taxonomia —
a frase e a prova usam o mesmo sensor.**

Prova pelo reajuste (`c3_refit.py`), com os discos de 28 px em torno das
válvulas removidos da máscara e tudo o resto igual:

| corrida | banda RMS | banda dentro | lobo RMS | lobo dentro |
|---|---|---|---|---|
| publicada (máscara suja, escala fixa) | 33,6 m | **6/12** | 24,6 m | 3/5 |
| **sem os círculos**, escala fixa | 39,1 m | **9/12** | 28,8 m | 3/5 |
| máscara suja, escala livre | 34,9 m | 9/12 | 23,5 m | 3/5 |
| **sem os círculos**, escala livre | 39,0 m | **11/12** | 23,3 m | 4/5 |

**O RMS e o «controlo» andam em sentidos opostos.** Tirar a tinta das válvulas
piora o RMS em 5,5 m e melhora o controlo de 6/12 para 9/12 — que é exactamente
o que se espera quando os dados do controlo estão dentro do ajuste. Enquanto os
círculos lá estiverem, **nenhum dos dois números significa o que o ficheiro diz
que significa**.

### LS-2 · A inicialização do lobo é construída a partir das coordenadas das válvulas.

`georref_por_bloco.py:86-91` contra `:78-81`:

```
INIC["lobo"][0] = ((104, 781), ...)      VALV[1]  = (104, 781)      — idêntico
INIC["lobo"][1] = ((380, 615), ...)      (VALV[4]+VALV[5])/2 = (380,0 , 615,0)
```

Não é aproximado: é o mesmo ponto e o ponto médio exacto. As duas âncoras que
fixam rotação e translação do lobo **são as válvulas 1, 4 e 5** — três das cinco
que depois contam como controlo. O comentário «dois pontos escolhidos por
**forma**» (`:85`) descreve a banda, não o lobo.

O controlo do lobo está contaminado duas vezes (LS-1 e LS-2). **O bloco «lobo»
não tem controlo nenhum.**

### LS-3 · A fonte não é uma fronteira, e o alvo é coberto a meio.

Com a transformação publicada (`c3_diag.py`):

| | banda | lobo |
|---|---|---|
| traço do desenho que cai **dentro** do polígono do IFAP | **66,3 %** | **46,8 %** |
| contorno do IFAP com traço do desenho a < 30 m | 49,9 % | 44,5 % |
| contorno do IFAP com traço do desenho a < 60 m | 80,2 % | 69,2 % |

Um registo fronteira-contra-fronteira tem o traço **sobre** o anel, não dentro
dele. 66 % dentro diz que a «fonte» é conteúdo interior — círculos de válvula e
separadores de sector — e não o limite. E metade do contorno do IFAP não tem
contrapartida nenhuma no desenho.

O ICP de `:137-166` só minimiza fonte→alvo. Nunca vê a metade do alvo que ficou
sem correspondência. **O RMS de 33,6 m não é o erro do registo; é a distância
média de uma nuvem de tinta ao ponto mais próximo de um contorno parcialmente
irrelevante.** A figura de sobreposição confirma-o à vista: no lobo, o traço
preto atravessa as parcelas na diagonal e a parcela mais a sul (o «bico do
papagaio») não tem traço nenhum por perto.

---

## REJEITADO

### R-1 · A condição 2 do critério é uma identidade. `georref_por_bloco.py:208-215`

```
c2 = True   # escala fixa no valor declarado; deixou de ser estimada
```

e o ficheiro imprime, na linha do veredicto, `escala  +0.0% < 10% OK`. O JSON
regista `desvio_escala: 5,29e-16` (banda) e `1,76e-16` (lobo) — zero-máquina,
porque a escala foi imposta em `:160` e depois lida de volta em `:180`.

**Um teste cujo resultado não pode ser outro não é um teste, e imprimir-lhe
«OK» é pior do que removê-lo:** quem lê a saída vê três condições e uma delas é
teatro. É a família C da taxonomia, com a mesma forma do T5 — «limpar a
referência deslocava todos os fossos pela mesma constante, idêntica à nona
casa». Aqui a constante é 1,2589820359281436 e a coincidência é à décima sexta.

### R-2 · A emenda de meio da corrida é mover a baliza, e a razão escrita para ela está errada.

`georref_por_bloco.py:38-54` justifica fixar a escala invocando «testemunho
ganha ao cálculo». Rejeito, por três razões independentes.

**(a) A doutrina diz o contrário do que foi feito.** `CLAUDE.md` §1 dos três
tipos: *«o cálculo que ele derrubar é retirado, não reconciliado»*. O testemunho
(1:3500) derrubou o cálculo (escala livre 1,148 / 1,130). A doutrina manda
**retirar** essa corrida. O que se fez foi **reconciliar**: assar o testemunho
dentro do estimador e correr outra vez. Reconciliar é a palavra que a regra
proíbe.

**(b) O texto da emenda afirma um facto que não se verifica.** `:42-44` diz «a
escala fugiu para 1,148 na banda e 1,130 no lobo … A condição 2 foi escrita para
apanhar isso, **e apanhou**». Calculado:

| | escala livre | desvio de 1,259 | limite 10 % |
|---|---|---|---|
| banda | 1,1481 | **8,81 %** | **passa** |
| lobo | 1,1295 | **10,28 %** | falha, por 0,28 pontos |

**A condição 2 não apanhou a banda.** A banda, na primeira corrida, passava a
condição 2 e passava o controlo (9/12); falhava só o RMS, por 4,9 m. A emenda
foi justificada por um disparo que só ocorreu num bloco e por três décimas de
ponto percentual.

**(c) O custo observável.** A emenda melhorou o RMS da banda em 1,3 m (34,9 →
33,6) e **degradou o único controlo declarado independente de 9/12 para 6/12** —
isto é, converteu um bloco que falhava uma condição num bloco que falha duas.
Mudar o estimador depois de ver o resultado, de forma que o controlo declarado
piora e o resíduo preferido melhora, é mover a baliza — mesmo quando a mudança
tem um argumento doutrinário por cima.

**E havia diagnóstico a ser silenciado.** A escala livre a querer encolher 9-10 %
era sintoma, não capricho: com os círculos removidos, a escala livre da banda
sobe para **1,2106** (3,8 % do declarado). Ou seja, **a maior parte do encolhimento
era a tinta das válvulas a puxar**. Fixar a escala tapou o sintoma sem tocar na
causa. E no lobo, com a máscara limpa, a escala livre vai a **0,9044 m/px — 28 %
abaixo do declarado**: a geometria do lobo, sem a tinta das válvulas, não suporta
a escala declarada de todo. Isso é um facto novo que a emenda impediu de aparecer.

### R-3 · «As 13 letras A–N cobrem só a banda; o B1 está fora do sistema de letras» — falso, por leitura directa.

`debito_e_sectores.py:2` (título) e `debito_e_sectores.json` (`hipotese_vencedora:
"H2"`, e as oito partições `melhores`).

Ampliei as bandas do lobo directamente do `scan.jpeg` (6-7×, rotação de 90°,
contraste esticado sobre o mínimo dos canais). Lê-se, sem ambiguidade:

| válvula | banda | etiqueta impressa lida por mim |
|---|---|---|
| **5** | verde | **«sector H»** |
| **4** | azul | **«sector I»** |
| **3** | laranja | **«sector J»** (o glifo final é o mais fraco dos quatro) |
| 2 | laranja | etiqueta presente, glifo final não resolvido |
| 1 | — | sem banda de cor e **sem etiqueta**: fica no triângulo do «papagaio» |

O `.py` já traz a ressalva de 04-09 (`:18-30`); **o `.json` não traz nada** e
continua a publicar H2 e as oito partições. Todas as oito colocam H e I fora do
B1 (a melhor: `erica=[C,H]`, `b4=[A,I]`) — e ambas estão impressas dentro do B1.
**As oito caem.** Com elas cai o alvo de **38,0 m³/ha** (`taxa_se_banda`) que
serve de referência à busca, e cai o «coerente a 1,2 %» que o ficheiro apresenta
como o que fica certificado.

O que fica de pé é o inverso do que o ficheiro conclui: a premissa «débito ∝
área» não se sustenta em nenhuma das duas hipóteses — a leitura G+F+E+D dá 37,55
m³/ha, que é 44,5 % acima de H1 (26,0) e as letras **estão** no B1. Não é a
atribuição que está errada; é a premissa.

Isto também confirma, por instrumento independente, a leitura do gestor (4=I,
5=H) — que em `P12_camada_rega.py:124-126` ainda entra a tracejado como
«gestor». **Passa a leitura confirmada.**

### R-4 · «Ampliar mais não acrescenta informação — os pixéis não existem.» `FIGURAS_ABSTRACTS.md:144`

Falso, e falsificado pelo item anterior: ampliei o mesmo JPEG e li quatro
etiquetas que a peça dá por ilegíveis. A frase justifica não olhar outra vez, e
foi escrita sobre um ficheiro onde olhar outra vez dava resposta.

### R-5 · A ressalva do tempo, como justificação do limiar de 30 m. `georref_por_bloco.py:55-59`

> «Dezasseis anos de replantação e de redesenho de parcelas põem um chão no
> resíduo que não é erro de ajuste. **Por isso o critério é 30 m e não 10.**»

Rejeito o **uso** da ressalva, não a ressalva.

**Não está medida, e não é mensurável com o que está aqui.** Todas as 53
feições de `_MULTIVERSO/SAIDA_H2_patologista/ifap_kiwi_largo.json` têm
`CUL_CAMPANHA = 2025`. Não há camada histórica de parcelário no repositório. Sob
`ANTES_DE_COMECAR.md` §3, um facto sem instrumento independente **fica registado
como não verificado — não se dilui numa ressalva**. Aqui foi diluído, e a
ressalva saiu com o tamanho exacto do resíduo que desculpa.

**O único apoio quantitativo disponível aponta para uma ordem de grandeza muito
menor.** O gestor declara 39,94 ha (12,63 + 9,65 + 4,87 + 9,01 + 3,78); o alvo do
ajuste — kiwi IFAP 2025 — soma **42,60 ha** (b1 12,63 + banda 29,97). A
diferença, 2,66 ha, repartida por 8 582 m de perímetro dos dois alvos, é uma
faixa uniforme de **3,1 m**. Para o resíduo de 25-35 m ser mudança real de
fronteira seria preciso um deslocamento uniforme de 30 m sobre esse perímetro:
**25,7 ha**, mais de metade da exploração. Não é isso que aconteceu.

**O precedente da REG01 não transfere.** As cinco parcelas desmatadas em 2024 do
`REG01_RETRACCAO_A3.md` são 6705427 / 28 / 29 / 32 / 42, do ENT 297313.
`parcelas_b1` são 6476415, 6476420, 6476425, 8845729, 8845739, 8845740. Nenhuma
coincide. O A3 é razão para **testar**, não resultado a citar.

**O que fica em aberto, e é a pergunta certa a levar ao gestor:** três das seis
parcelas do B1 têm CUL_ID na casa dos 8,8 milhões contra 6,4 milhões das outras
três. Isso sugere registo posterior. É verificável numa única pergunta — «estas
três parcelas foram plantadas ou reparceladas depois de 2009?» — e é testemunho
de tipo 1. Enquanto não houver resposta, **o resíduo não pode ser atribuído ao
tempo.**

---

## CORRIGIDO

### C-1 · A ponta oriental não está em x ≈ 2160. Está em **x = 2138, y 561-565**.

Publicado em `FIGURAS_ABSTRACTS.md:102`, `P12_camada_rega.py:34`,
`escala_do_desenho.py` (cartucho), `georref_manual.py:52` e
`georref_por_bloco.py:88`.

Medido: o píxel mais a leste da máscara de limite está em **x = 2138**. Não há
um único píxel de traço acima de x = 2138 (`x ≥ 2140: 0 px`). Erro de **22 px =
28 m**, para leste.

Honestamente: **não muda o ajuste.** Refeito com a ponta corrigida, o resultado
é idêntico ao milímetro (banda RMS 39,1 m, 9/12; lobo 28,8 m, 3/5), porque o
ponto só inicializa e o ICP recupera. Mas é um número publicado e está errado, e
é o mesmo número que já custou uma retractação — desta vez por 22 px em vez de
por 600.

### C-2 · «a banda dá 1,263 m/px — 0,3 % de desvio» → **1,288 m/px, 2,3 %**, e o «0,3 %» é uma propriedade da minha leitura, não do desenho.

`FIGURAS_ABSTRACTS.md:107`, `P12_camada_rega.py:38`, `escala_do_desenho.py`
(cartucho), `georref_por_bloco.py:8-9`.

Recomputado com o mesmo par de pontos e a ponta medida (2138, 563): **1,2880
m/px, desvio 2,30 %**.

E a sensibilidade, que é o que falta declarar. Deslocando só a ponta oriental
dentro do erro de leitura que o próprio processo declara (±15 px):

| dx | escala | desvio |
|---|---|---|
| −15 px | 1,2795 | 1,63 % |
| −5 px | 1,2686 | 0,76 % |
| **0 (publicado)** | **1,2632** | **0,33 %** |
| +5 px | 1,2578 | 0,09 % |
| +15 px | 1,2472 | 0,93 % |

O «0,3 %» não é uma medição do desenho: é **um par de pontos, N = 1**, com uma
banda de incerteza de ±1,6 % em que 0,3 % é um valor qualquer. E o ponto que o
produz é o mesmo que a retractação anterior identificou como a origem do erro.
**A frase «o desenho está à escala» é defensável; o «0,3 %» não é.** O que a
prova sustenta é: *o desenho está à escala declarada dentro de ~2 %, medido num
único par de pontos.*

### C-3 · As coordenadas `VALV` estão certas dentro do chão de leitura. Discordo em 1 a 17 px, e isso não muda nada.

Reli as dezassete de forma independente, com um filtro de anel (correlação com
um núcleo anelar r = 13 px sobre o mapa de vermelhidão, máximos locais), sem
olhar para o dicionário antes.

| v | declarado | detectado | Δ px | Δ m |
|---|---|---|---|---|
| 1 | (104, 781) | (108, 791) | 10,8 | 13,6 |
| 2 | (195, 716) | (190, 718) | 5,4 | 6,8 |
| 3 | (394, 722) | (391, 731) | 9,5 | 11,9 |
| 4 | (257, 614) | (255, 608) | 6,3 | 8,0 |
| 5 | (503, 616) | (505, 629) | 13,2 | 16,6 |
| 6 | (1051, 356) | (1046, 359) | 5,8 | 7,3 |
| 7 | (1138, 376) | (1131, 380) | 8,1 | 10,2 |
| 8 | (1213, 387) | (1209, 400) | 13,6 | 17,1 |
| 9 | (1265, 411) | (1268, 419) | 8,5 | 10,8 |
| 10 | (1337, 378) | (1335, 378) | 2,0 | 2,5 |
| 11 | (1342, 521) | (1335, 527) | 9,2 | 11,6 |
| 12 | (1480, 414) | (1481, 414) | 1,0 | 1,3 |
| 13 | (1400, 398) | (1412, 402) | 12,6 | 15,9 |
| 14 | (1623, 450) | *não detectada* | — | — |
| 15 | (1726, 466) | (1721, 470) | 6,4 | 8,1 |
| 16 | (1820, 543) | (1812, 554) | 13,6 | 17,1 |
| 17 | (1969, 564) | (1970, 556) | 8,1 | 10,2 |

Mediana 8,5 px ≈ 10,7 m; máximo 13,6 px ≈ 17,1 m. A v14 escapou ao filtro (anel
mais grosso e mais aberto), mas confirmei-a à vista em (1622, 450) — 1 px do
declarado.

**Veredicto: `VALV` é sólido a ±17 px ≈ ±21 m, que é o chão de leitura já
declarado.** Reler as válvulas não pode salvar nem afundar este ajuste (ver
C-7). A entrada não é o problema; o problema é o que se fez com ela.

**A válvula 1, em particular** (o launcher pediu atenção): confirmada em
(105, 786) contra (104, 781) declarado — 5 px. Mas duas coisas ficam a dizer-se.
Primeira, **a v1 está fora das bandas de cor** — não tem trama de sector nem
etiqueta; está no triângulo do «papagaio», junto ao «Tubo 2,5 pol» a caneta
azul. Segunda, **é uma das duas âncoras da inicialização do lobo** (LS-2). O
seu «dentro» é o menos informativo dos cinco e é, em parte, imposto.

### C-4 · Há **dois** círculos «17» na ponta oriental. `VALV` só regista um.

Em (1974, 556) e em (2098, 581), em duas parcelas tramadas a azul separadas.
`VALV[17] = (1969, 564)` é o primeiro. O segundo está **124 px = 156 m a leste**
do declarado, a sua tinta entra na máscara e portanto **entra no ajuste**, e não
está no controlo. A leitura mais provável é uma válvula a servir duas parcelas
do mesmo sector — mas isso é inferência minha, e a pergunta certa é para o
gestor.

### C-5 · `georref_manual.py`: o limiar em prosa não é o limiar em código.

Linha 39: «RMS do ajuste **< 45 m**». Linha 58: `LIM_RMS = 60.0`, que é o que
`:161` usa e o que o JSON regista (`limiar_rms: 60.0`). Não muda o veredicto
(112,4 > 60 e > 45), mas é exactamente o modo de falha que o `ANTES_DE_COMECAR`
§3 nomeia: **ler o cabeçalho e o código juntos.**

### C-6 · O modo «semelhança» de `georref_manual.py:94-104` é estruturalmente inadmissível.

`M = [[a, −b], [b, a]]` tem `det = a² + b² > 0`, e `aplica()` (`:107-108`) **não
nega o y**. Um scan tem y a crescer para baixo e o UTM tem N a crescer para
cima: qualquer registo correcto inverte a orientação. O modelo não consegue.
Recomputado: RMS **334,9 m**, det +1,206.

A semelhança admissível (mesmo modelo, com y negado antes) dá **RMS 140,3 m,
escala 1,171 m/px**. Portanto o valor de 189,1 m que a tabela de
`FIGURAS_ABSTRACTS.md:97-99` atribui à tentativa 2 é, em parte, artefacto de um
modelo que não podia funcionar — **não é prova sobre o desenho**. (O modo
«afim», esse, é legítimo: `det = −2,04` é a inversão de orientação correcta.)

### C-7 · O critério não mede o que diz medir, e não teria passado com nenhuma leitura das válvulas.

O launcher pergunta se o «dentro/fora» binário é bom. Mediu-se
(`c3_poder.py`, 400 réplicas): perturbando as coordenadas das válvulas com o
ruído que o próprio processo declara e reaplicando a transformação publicada —

| bloco | ruído 1σ | dentro médio | p5-p95 | **P(passar o limiar)** |
|---|---|---|---|---|
| banda | 5 px (6 m) | 6,6 / 12 | 5-8 | **0,21** |
| banda | 10 px (13 m) | 6,8 / 12 | 5-9 | 0,29 |
| banda | 15 px (19 m) | 6,6 / 12 | 4-9 | 0,26 |
| lobo | 5 px (6 m) | 2,7 / 5 | 2-4 | **0,06** |
| lobo | 15 px (19 m) | 2,6 / 5 | 1-4 | 0,12 |

Duas leituras saem daqui.

**Primeira: a contagem de 6/12 não é um problema de leitura.** Mesmo com ruído
quase nulo, a distribuição centra-se em 6,6/12. Reler as válvulas — que é o que
o launcher me mandou fazer, e fiz — **não podia** mudar o veredicto. O que está
mal está na transformação, não na entrada.

**Segunda: o limiar nunca teve poder.** 51 % da área do lobo está a menos de
20 m da fronteira; 32 % da banda. Com um chão de leitura declarado de ±20-25 m,
o teste «dentro/fora» sobre uma fronteira é, por construção, próximo de uma
moeda ao ar. Exigir 4/5 (80 %) de um teste cuja taxa por válvula é ~55 % é
escrever um limiar que uma medição correcta falha na maior parte das vezes.
**Um limiar cujo poder não foi calculado não é um critério pré-registado; é um
número.** E o poder não está calculado em lado nenhum do ficheiro.

**E sim: teria passado com um critério igualmente defensável.** Sobre a corrida
publicada:

| formulação | banda | lobo |
|---|---|---|
| RMS < 30 m *(escolhida)* | **falha** (33,6) | passa (24,6) |
| RMS < 35 m | passa | passa |
| RMS < 45 m *(o que `georref_manual.py:39` escreve)* | passa | passa |
| RMS < 60 m *(o que `georref_manual.py:58` executa)* | passa | passa |
| ≥8/12 e ≥4/5 dentro *(escolhida)* | **falha** (6) | **falha** (3) |
| distância média < 20 m | passa (4,1 m) | passa (7,1 m) |
| distância máxima < 30 m | passa (20,8 m) | passa (26,2 m) |
| dentro de um tampão de 20 m | passa (12/12) | passa (5/5) |

**Seis de oito formulações defensáveis publicariam.** A escolhida é a mais
estrita de cada família, e isso é a favor de quem a escreveu — foi escrita antes
e foi honrada. Mas então `FIGURAS_ABSTRACTS.md:117` oferece, no parágrafo
imediatamente a seguir ao falhanço, **«Todas as válvulas caem a ≤ 26 m das
parcelas»** — que é, exactamente, a variante que passa. Sob Botvinik-Nezer, isso
é relatar a corrida preferida. A frase honesta é: *seis de oito formulações
defensáveis do critério publicariam; escolhemos a mais estrita e ela falha nos
dois blocos.*

---

## CONFIRMADO

**K-1 · A corrida reproduz-se ao dígito.** Reimplementei o pipeline num
directório diferente e obtive banda RMS 33,592 m / 6 dentro, lobo 24,640 m /
3 dentro — idêntico a `georref_por_bloco.json`. Sem reservas mecânicas.

**K-2 · Os dois blocos falham o critério pré-registado, e o ficheiro di-lo.**
Publicar o falhanço, com os números, é o comportamento certo e não tenho
objecção a essa parte.

**K-3 · «Todas as válvulas caem a ≤ 26 m das parcelas» é aritmeticamente
verdade** — máximo 26,24 m (v4), banda máximo 20,84 m (v15). Confirmado como
número. Ver C-7 quanto ao uso.

**K-4 · A retractação do `escala_do_desenho.py` está certa na direcção.** O
desenho não carece de escala única e a conclusão «banda comprimida 1,9×» era
sobre a leitura, não sobre o desenho. Corrijo a magnitude (C-1, C-2), não o
sentido.

**K-5 · `cor_e_sector.json` resiste.** O par decisivo v7/v16 (ΔRGB 11,1, extremos
opostos da folha) sustenta o veredicto, e o par v8/v9 foi correctamente
descartado por ambiguidade de amostragem. Nada a acrescentar.

**K-6 · A escala declarada de 1:3500 em A1 → 1,259 m/px é aritmeticamente
correcta** (841 mm / 2338 px × 3,5). O testemunho é o que é; o problema não está
nele.

---

## O QUE ESTE RELATÓRIO NÃO DECIDE

- **Não decide se o desenho é registável.** Decide que este ajuste não o mostra.
  Com a máscara limpa dos círculos e a escala livre, a banda chega a 11/12
  válvulas dentro com escala 1,2106 (3,8 % do declarado) — isso é promissor e
  **não é um resultado**, porque foi obtido depois de eu ver os outros.
- **Não decide a letra da válvula 2**, nem se o segundo círculo «17» é uma
  décima-oitava válvula.
- **Não decide** se a fronteira mudou entre 2009 e 2025. Diz que não está medida
  e que a magnitude invocada não é sustentada por nada no repositório.

## O QUE FAZER A SEGUIR, POR ORDEM

1. **Retirar da máscara toda a tinta que não seja limite** — círculos, algarismos,
   separadores internos, o «BI» a vermelho em (345, 865) — e só então voltar a
   falar de RMS. Enquanto 56 % da fonte for tinta de válvula, o número não é
   interpretável.
2. **Reconstruir a inicialização do lobo** com feições que não sejam válvulas.
3. **Apagar `c2 = True`.** Se a escala é testemunho, a condição não se imprime;
   não se imprime «OK».
4. **Calcular o poder do critério antes de o escrever** — a Monte Carlo acima
   leva segundos e teria mostrado, antes de correr, que 4/5 no lobo era
   inatingível.
5. **Marcar `debito_e_sectores.json` como retirado** e propagar: `H`
   e `I` estão impressas no B1 e as oito partições caem.
6. **Perguntar ao gestor**, numa só volta: (a) as três parcelas do B1 com CUL_ID
   ~8,8 M são posteriores a 2009? (b) o segundo círculo «17» é a mesma válvula?
   (c) confirma «sector J» na banda da v3?
