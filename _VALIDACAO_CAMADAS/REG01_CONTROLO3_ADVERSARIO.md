# REG-01 · CONTROLO 3 — o adversário sobre a cadeia da comparação regional

**Data:** 03-09-2026 · **Alvo:** a cadeia REG-01 completa, do S2 de 31-08 à
retracção do A3 de 01-09, incluindo a triagem de descontinuidade e a condição 5
do `guarda.py`.
**Código:** `_VALIDADE_GESTAO\_controlo3\` — onze scripts, todos corridos.
**Não toquei em nada fora dessa pasta.** Não descarreguei nenhuma cena que já
estivesse em cache; descarreguei ortofoto nova, do WMS público da DGT, para os
três blocos que não a tinham.

**A conclusão invertida resiste.** Atirei-lhe quarenta combinações de limiar,
três definições de mediana, duas mascaras de chão de datas opostas, a remoção
dos treze blocos suspeitos e a remoção do dono inteiro — e os dois focos ficam
em primeiro e segundo em todas. O que **não** resiste é a **forma da frase**:
ela está escrita como facto e o material sustenta-a com uma probabilidade de
erro entre 7 % e 25 %, conforme o que se reamostra. E dois números publicados
estão errados.

---

## CONFIRMADO

**C1 · A triagem reproduz-se exactamente.**
Reconstruí as máscaras dos 37 blocos e dos dois focos, reli as 100 cenas da
cache e recalculei tudo de raiz. Os oito excluídos são os mesmos oito; os 31
degraus batem ao **máximo de diferença 0,00e+00**.
*Ficheiro:* `_controlo3\c3_01_triagem_sensibilidade.py` §A.

**C2 · A triagem não reordena nada: só remove.**
Ao retirar blocos da mediana regional, o desvio de **todas** as unidades
sobreviventes desloca-se pela mesma constante. Medida: **−0,0165**, com
amplitude de −0,0162 a −0,0168 nos 29. A ordenação dos sobreviventes é a mesma
antes e depois. Isto é bom para a cadeia — significa que a inversão não veio de
uma mudança de referência, veio de retirar competidores — e é preciso dizê-lo,
porque a diferença entre o −0,0676 publicado a 01-09 de manhã e o −0,0839
publicado à noite **não é um facto novo sobre Ganfei**: é a constante.
*Ficheiro:* comparação `reg01_landsat.json` × `reg01_triagem.json`.

**C3 · A janela 2017-2024 não é o que protege Ganfei.**
Apliquei o critério de exclusão **simetricamente**, com a janela da queda
estendida até 2026. Os focos sobrevivem à mesma, e por larga margem nas duas
condições:

| unidade | maior queda anual (janela até 2026) | nível depois | X1 (≥ 0,25) | X2 (< 0,60) |
|---|---|---|---|---|
| foco OCIDENTAL | **0,106** em 2026 | **0,723** | não | não |
| foco ORIENTAL | **0,060** em 2025 | **0,743** | não | não |

A queda dos focos é **um quarto** do limiar e o nível é **0,12 acima** do chão.
Nenhuma das duas condições chega perto. O desenho da janela é uma escolha
discutível (ver R2), mas **não é ela que salva o caso**.
*Ficheiro:* `c3_01_triagem_sensibilidade.py` §B.

**C4 · O limiar sobrevive às quarenta combinações pedidas.**
Grelha queda {0,15 · 0,20 · 0,25 · 0,30 · 0,35} × chão {0,55 · 0,60 · 0,65 ·
0,70}, nas duas variantes de `depois` (até 2024 e até 2026). **Quarenta
combinações, quarenta vezes os focos em primeiro e segundo**, com a margem
sempre entre +0,0197 e +0,0212. Não há um limiar plausível dentro do intervalo
pedido que inverta.
*Ficheiro:* `c3_01_triagem_sensibilidade.py` §C, `c3_01_sensibilidade.json`.

**C5 · E o penhasco está longe, na queda.**
Fui procurar onde o critério parte. Na queda, parte entre **0,40 e 0,41** — os
cinco blocos do 297313 caem 0,402 a 0,451 num ano. O ponto de operação, 0,25,
está a **1,6×** do penhasco. Isso é um planalto largo, e é a evidência mais
forte de que o limiar não foi afinado para dar a resposta.
*Ficheiro:* `_controlo3\c3_02_penhasco.py` §B.

**C6 · Os três excluídos do ENT 472062 estão bem excluídos — e agora com
instrumento independente.**
Foram excluídos só pela forma da série, e isso é o pecado que retirou o A3. Fui
buscar a ortofoto da DGT (WMS público, EPSG:3763, IRG e RGB, 2007/2010/2012/
2018/2021/2025), medi a fracção sem coberto pelo mesmo método de
`orto_297313_fraccao.py` — quantil dentro da mesma imagem, contra os **doze
blocos do mesmo dono** — e depois **olhei para as imagens**:

| CUL_ID | ha | 2007 | 2010 | 2012 | 2018 | 2021 | **2025** |
|---|---|---|---|---|---|---|---|
| 8845729 | 1,88 | 12,7 % | 16,4 % | 52,4 % | 94,2 % | 13,6 % | 21,9 % |
| 8845731 | 0,98 | 0,0 % | 51,6 % | 40,9 % | 99,1 % | **97,3 %** | 23,7 % |
| 8845739 | 2,20 | 17,1 % | 22,1 % | 69,0 % | 96,5 % | 8,5 % | 21,8 % |
| **mediana dos doze** | | 0,1 % | 5,6 % | 7,9 % | 8,8 % | 4,6 % | 6,7 % |

E o olhar decide o que a fracção não decidia. Nos três recortes RGB
(`c3_09_8845729.png`, `c3_09_8845731.png`, `c3_09_8845739.png`): **2012, 2018 e
2021 mostram campo aberto — terra lavrada, pastagem, mato. 2025 mostra pérgola
nova, linhas brancas de rede, plantação recente.** Os três blocos **nunca
tiveram kiwi na linha de base**. Sair da comparação é o que tinham de fazer.
*Ficheiros:* `c3_08_orto_tres.py`, `c3_09_olhar.py`, `c3_08_orto_tres.json`.

**C7 · E a exclusão dos três não decide nada, de qualquer maneira.**
Corri a REG-01 com os cinco fora e os três dentro: margem **+0,0202**. Com os
oito fora: **+0,0200**. **Dois décimos de milésimo.** A inversão da REG-01
assenta inteiramente nos cinco blocos do 297313, que têm ortofoto desde 01-09.
Se os três estivessem mal excluídos, a conclusão não se movia — o que quer
dizer que este risco, que era o que a pergunta 3 temia, não existe.
*Ficheiro:* `c3_02_penhasco.py` §E.

**C8 · O filtro de copado não importa informação do acontecimento.**
Esta era a minha melhor hipótese de matar o foco ORIENTAL, e falhou. A máscara
dele é `zona0 & COM`, e `COM` é altura do CHM ≥ 0,5 m do **voo LiDAR de
06-07-2025** — que a C2 da `LISTA_FINAL` declara **pós-tratamento**. Sem esse
filtro o foco cai de 1.º para **3.º lugar** (−0,0615). Máscara derivada de
depois, a decidir um lugar: era um *line-stop* à vista.

Só que existe o instrumento **pré** para fazer o mesmo trabalho — `nu2021_bits`,
chão lavrado dentro do pomar na **ortofoto DGT de 2021**, a 25 cm — e ele dá a
mesma resposta, mais forte:

| máscara do foco ORIENTAL | n30 | degrau | lugar |
|---|---|---|---|
| `zona0 & COM` (CHM 07-2025) — a que a cadeia usa | 10 | −0,0869 | **1.º** |
| `zona0 & ~nu2021` (**ortofoto 2021, pré-acontecimento**) | 13 | **−0,1067** | **1.º** |
| `zona0 & ~nu2021 & COM` | 9 | −0,0924 | 1.º |
| `zona0` crua (45 % chão lavrado em 2021) | 24 | −0,0615 | 3.º |

Os dois filtros concordam em **73,8 %** das células da `zona0`, e o filtro de
2021 — que **não pode** conter informação de 2025-26 — põe o foco no mesmo
lugar. O que faz o foco cair para 3.º não é o LiDAR: é incluir 0,9 ha de chão
que já era chão em 2021.
*Ficheiro:* `_controlo3\c3_07_mascara_pre.py`.

**C9 · A assimetria de recorte existe, é grave em princípio, e o facto
sobrevive-lhe.**
Do lado de Ganfei a comparação põe **dois recortes internos** de um pomar de
30 ha — 2,18 e 0,76 ha, escolhidos onde o problema está. Do outro lado,
**29 parcelas administrativas inteiras**, de 0,54 a 11,33 ha, nenhuma recortada.
Um recorte é só o mau; uma parcela inteira é a média do bom com o mau. É a
comparação de um **máximo de muitos** contra uma **média de cada um**, e devia
ter sido levantada em algum dos documentos. Não foi.

Dei então o mesmo privilégio a toda a gente: para cada bloco, as **k piores
células de 30 m**, com k igual ao n do foco. E fi-lo **fora de amostra** —
escolhem-se as k piores só com as cenas de 2025, avalia-se o degrau só com as de
2026 — para não estar a seleccionar sobre o resultado:

| k = 26 células (2,34 ha) | k piores, fora de amostra |
|---|---|
| **foco OCIDENTAL** | **−0,1545** |
| 6476416 (contém **88 %** do próprio foco) | −0,1629 |
| 4405900 (contém 90 % do foco oriental) | −0,1313 |
| 6709642 — o melhor bloco que **não** contém foco | −0,0655 |

| k = 10 células (0,90 ha) | k piores, fora de amostra |
|---|---|
| **foco ORIENTAL** | **−0,1094** |
| 6476416 · 4405900 (os dois contêm os focos) | −0,2272 · −0,1559 |
| 6709642 — melhor bloco sem foco | −0,0851 |

Excluindo os dois blocos que **contêm** os focos, o foco OCIDENTAL bate **9 de
10** e o ORIENTAL bate **22 de 24**. Contra o melhor competidor sem conflito de
interesse, o factor é **2,4×** e **1,3×**. A assimetria não explica o resultado.

E um sinal lateral que vale a pena guardar: o foco OCIDENTAL (−0,1545) **não
bate** as 26 piores células do seu próprio bloco (−0,1629). Se o disco tivesse
sido colocado a maximizar o sinal, batia. Não bate — o que é consistente com o
centro ter vindo de onde `SAIDA_C1\c1_00_comum.py` diz que veio, do gestor.
*Ficheiro:* `_controlo3\c3_06_unidade.py`.

**C10 · A mediana ponderada por dono não muda a ordem.**
Calculei a mediana das medianas de cada dono — cada dono conta uma vez — e
também a mediana **sem nenhum bloco do dono do pomar em estudo**. Nas três
definições, os focos são o primeiro e o segundo:

| definição da mediana regional | degrau OC | degrau OR | margem |
|---|---|---|---|
| por bloco (a usada) | −0,0839 | −0,0869 | +0,0200 |
| **ponderada por dono** | **−0,1526** | **−0,1552** | +0,0210 |
| sem o dono do pomar (472062) | −0,0773 | −0,0804 | +0,0200 |

*Ficheiro:* `_controlo3\c3_04_anos_e_donos.py`.

**C11 · E não muda com os blocos suspeitos fora, nem com o dono inteiro fora.**
Treze dos 29 sobreviventes falham um rastreio de pomar jovem (nível de 2017
entre 0,555 e 0,754 — um kiwi maduro lê 0,83 a 0,90 — ou declive 2017-24 acima
de +0,010/ano, ou fracção sem coberto de 2021 acima de 20 %). Retirei-os:

| conjunto de comparação | n | degrau OC | lugares | margem |
|---|---|---|---|---|
| os 29 da triagem oficial | 29 | −0,0839 | 2.º e 1.º | +0,0200 |
| sem os 13 suspeitos de pomar jovem | 16 | −0,0730 | 2.º e 1.º | +0,0212 |
| sem nenhum bloco do 472062 | 17 | −0,0773 | 2.º e 1.º | +0,0200 |
| **sem o dono E sem os suspeitos** | **11** | **−0,0698** | **2.º e 1.º** | **+0,0207** |

Onze blocos maduros de outros donos, e o resultado é o mesmo.
*Ficheiro:* `_controlo3\c3_10_jovens.py`.

---

## CORRIGIDO

**R1 · A margem não é 0,023. É 0,0200.**
A `REG01_RETRACCAO_A3` §6 e o A3 da `LISTA_FINAL` escrevem «margem 0,023».
0,0231 é a distância do **foco ORIENTAL** (−0,0869) ao melhor bloco
sobrevivente. Mas a afirmação é «o pior **e o segundo pior**», e quem a governa
é o foco **OCIDENTAL**, o menos mau dos dois: −0,0839 contra −0,0638. **A margem
que sustenta a frase é 0,0200.** Citar a maior das duas é citar a que não
decide. Além disso o segundo bloco, 6709642, está a −0,0627 — ou seja há **dois**
blocos dentro de 0,0212, não um.

**R2 · «Percentil 0 %» para os dois focos não pode ser verdade.**
Dois objectos distintos não ocupam o mesmo percentil 0 de uma ordenação
conjunta. O 0 % sai de comparar cada foco só contra os 29 blocos, cada um por
sua vez. Na ordenação conjunta de 31 unidades, os lugares são **1 e 2**, e os
percentis 3,2 % e 6,5 %. Escrever «percentil 0 %» duas vezes na mesma tabela
sugere um empate no extremo que a medida não produziu.

**R3 · «8 dos 37 blocos mudaram de uso dentro de 2017-2024» é falso para três
deles, e a palavra «replantação» está invertida.**
`REG01_RETRACCAO_A3` §6 e a `LISTA_FINAL` A3 descrevem os três do ENT 472062
como blocos «que caem e recuperam, com forma de replantação». A ortofoto diz
outra coisa (C6):

- **não mudaram de uso dentro da linha de base** — em 2012, 2018 **e** 2021 são
  campo aberto, os três;
- **8845731 ganhou coberto, não o perdeu**: fracção sem coberto **97,3 % em
  2021 → 23,7 % em 2025**. Uma queda de 73,6 pontos na direcção contrária à que
  «replantação» faz imaginar;
- o que os três são é **plantação nova posterior a 2021**.

A redacção certa: *três blocos do ENT 472062 que **não têm cultura na linha de
base** — campo aberto até 2021 e pérgola nova em 2025.* E a exclusão deles fica
mais forte, não mais fraca: um bloco sem linha de base não é competidor, é ruído.

**R4 · O degrau não é reportável a quatro casas. A ordem é; o número não.**
O mesmo acontecimento, medido nas mesmas cenas, dá:

| | degrau do foco OCIDENTAL |
|---|---|
| mediana por bloco (a publicada) | −0,0839 |
| mediana ponderada por dono | **−0,1526** |
| sem os blocos de pomar jovem | −0,0730 |

**Oitenta e dois por cento de amplitude** entre a maior e a menor. A ordenação
é invariante às três; a magnitude não é. Qualquer peça que escreva «−0,084» sem
a amplitude ao lado está a escrever um número que a próxima escolha de mediana
desfaz — é o mesmo problema que o B4 já tem para Julho de 2026.

**R5 · O limiar do chão foi tomado no topo da banda que o justifica, e a
fronteira da inversão está dentro dessa banda.**
`REG01_RETRACCAO_A3` §6 diz que o 0,60 é «limiar herdado da série NU21, não
inventado agora», e a série NU21 dá **0,49 a 0,61** para chão lavrado. 0,60 é o
**topo** dessa banda. Fui procurar a fronteira em passos de 0,005:

| chão | excluídos | lugares dos focos |
|---|---|---|
| 0,495 | 3 | 4.º e 3.º |
| **0,505** | 4 | **3.º e 2.º** |
| **0,510** | 6 | **2.º e 1.º** |
| 0,600 (o usado) | 8 | 2.º e 1.º |

**A inversão parte em 0,507.** Um valor no fundo da banda citada — 0,49 a 0,505,
cerca de 13 % dela — deixa o bloco 6705442 (nível pós-queda 0,508) dentro da
comparação, e os focos deixam de ser os dois piores. A escolha do topo da banda
está a fazer trabalho. **Mitigação, e é real:** 6705442 tem 20,9 % sem coberto
na ortofoto de 2025 contra 1,0 % da mediana dos doze — **quem o exclui é a
ortofoto, não o limiar.** O limiar só tem de concordar com ela. Mas então diga-se
isso, e não «limiar herdado, portanto robusto».

---

## REJEITADO

**X1 · «Critério de exclusão escrito antes de correr **e aplicado cego aos
37**».** A segunda metade sai.
A própria `REG01_RETRACCAO_A3` identifica os cinco blocos do 297313 pela
ortofoto (§2) e pela série anual (§3) **antes** de o §6 correr o critério. O
critério foi escrito por quem já sabia quais cinco tinha de apanhar, e os dois
limiares — 0,25 e 0,60 — apanham exactamente esses cinco e mais nenhum. Isso não
é cego; é um critério calibrado contra um alvo conhecido. *A defesa existe e
está medida (C5): o planalto vai de 0,15 a 0,40 na queda e de 0,51 a 0,80 no
chão, e um critério afinado à resposta estaria numa aresta, não num planalto.*
**Mas a frase «aplicado cego» não é sustentável e tem de sair.** O que se pode
escrever é: *critério fixado antes da corrida, aplicado uniformemente aos 37, e
robusto num planalto de limiares que vai de 0,15 a 0,40 × 0,51 a 0,80.*

**X2 · «Confirmado por: ortofoto DGT 2007-2025 (…) que datam a exclusão de cada
bloco».** Sai como está.
A ortofoto datava a exclusão de **cinco dos oito**. Os outros três não tinham
ortofoto nenhuma até hoje, e quando a têm, a data que ela dá é outra: não é uma
mudança de uso dentro de 2017-2024, é uma plantação nova posterior a 2021.
A frase atribui a oito blocos uma verificação que existia para cinco. Substituir
por: *cinco confirmados por ortofoto em 01-09; três por ortofoto em 03-09, com
outra leitura (R3).*

**X3 · A frase «Os dois focos de Ganfei são o pior e o segundo pior da
região», dita sem intervalo.**
Não rejeito o conteúdo — ele resistiu a tudo o que lhe atirei. Rejeito a
**forma**. Ver LINE-STOP 1: a probabilidade de a ordenação estar errada é 7 % a
25 % conforme o que se reamostra, e a `LISTA_FINAL` regista-a ao lado de factos
com p = 0,011 e de séries de 441 cenas, sem marca que a distinga.

---

## NÃO TESTÁVEL

**N1 · Se o critério de exclusão foi mesmo escrito antes de correr.**
Não há controlo de versões nesta pasta (`git rev-parse` falha), e
`reg01_triagem_descontinuidade.py` e `reg01_triagem.json` têm a **mesma hora de
modificação, 01-09 às 23:25**. Toda a cadeia — ortofoto 23:22, Landsat 23:25,
triagem 23:25, retracção 23:27 — cabe em cinco minutos de escrita de ficheiros.
Nada nisto contradiz a afirmação; nada a sustenta.
*Teste que decidiria:* pôr `_VALIDADE_GESTAO\` sob o repositório que já existe em
`CLAUDE\`, e comprometer o critério **antes** da corrida. Custo nenhum, e é a
única coisa que torna «pré-registado» uma afirmação verificável em vez de uma
afirmação sobre a memória de quem escreve.

**N2 · Se as 29 unidades mantidas têm identidade contínua.**
A condição 5 do portão foi cumprida sobre os **8 excluídos**. Sobre os **29
mantidos**, ninguém a verificou — e o rastreio (C11) marca **13 deles** como
prováveis pomares jovens, com nível de 2017 entre 0,555 e 0,754 e declives até
+0,046/ano. Um pomar plantado em 2018 que cresce em linha recta **não tem queda
nenhuma** e passa a triagem inteira; e sobe a mediana regional no período pós,
empurrando o degrau de toda a gente — incluindo o dos focos — para baixo. **O
enviesamento vai na direcção da conclusão.** Está mostrado que retirar os treze
não inverte nada (C11), mas isso é um teste de sensibilidade, não uma
verificação de identidade.
*Teste que decidiria:* a mesma fracção de ortofoto de `c3_08_orto_tres.py` sobre
os 29, em 2018 · 2021 · 2025. Já corre para 15 deles; o resto é uma janela WMS.
**Seis minutos de máquina.**

**N3 · Se as duas unidades de Ganfei têm identidade contínua.**
Isto não foi perguntado em documento nenhum da cadeia. O `zona0` é 41,6 % do
polígono 8845731 — que hoje sei ser plantação nova posterior a 2021 — e 45 % da
sua área era chão lavrado na ortofoto de 2021. O filtro `& COM` resolve-o na
prática, e o teste com a máscara de 2021 mostra que resolve **bem** (C8). Mas
«a máscara compensa» não é o mesmo que «a unidade foi verificada».
*Teste que decidiria:* a mesma fracção de ortofoto sobre `pomar`, `zona0` e o
disco ocidental em 2007 · 2010 · 2012 · 2018 · 2021 · 2025 — os dados são o
mesmo WMS e o código é o mesmo.

**N4 · Se há causa partilhada, ou causa nenhuma.** Inalterado, e os documentos
anteriores já o dizem bem: nenhum instrumento aqui mede causa. Deixo-o na lista
para que a ausência não se leia como esquecimento.

**N5 · O LiDAR sobre os três blocos novos.** Não tentei. O
`REG01_RETRACCAO_A3` §7 regista que o *endpoint* da DGT passou a exigir
autenticação, inclusive para folhas já descarregadas com sucesso. Não gastei
tempo a confirmá-lo — e a ortofoto respondeu à pergunta sem ele.

---

## LINE-STOP

**L1 · A frase está escrita como facto, e a incerteza de amostragem diz que não
é. Não avança até levar o intervalo ao lado.**

A afirmação depende de **uma** distância: 0,0200 entre o foco OCIDENTAL e o
melhor bloco sobrevivente. Medi a incerteza dessa distância de duas maneiras.

*Bootstrap sobre as cenas*, reamostrando com reposição as 71 do PRE e as 29 do
POS separadamente, 2 000 réplicas:

> os dois focos são o 1.º e o 2.º em **91,4 %** das reamostras.
> margem: mediana +0,0185 · **IC95 [−0,0023 · +0,0468]** · **P(margem ≤ 0) =
> 0,072**.

*Bootstrap de anos*, que é o correcto — 29 cenas do pós, mas **dois anos**, e
seis cenas em treze dias de Agosto de 2025 não são seis observações:

> os dois focos são o 1.º e o 2.º em **74,6 %** das reamostras.
> **P(margem ≤ 0) = 0,252.**

*Jackknife por ano*, dez corridas, uma por ano retirado:

> nove das dez mantêm os focos em 1.º e 2.º. **A décima não.** Retirado **2026**,
> o foco OCIDENTAL vai a −0,0428, o terceiro lugar passa a −0,0639, e a margem
> fica **−0,0211**: o foco sai do topo.

**A conclusão inteira assenta nas dez cenas de 2026.** E o **B4** da
`LISTA_FINAL` já regista, por outra via, que *«Julho de 2026 não é estável — o
contraste vai de −0,229 a −0,130, a escolha da cena muda o número por 1,7×»*.
As duas observações são a mesma, e nenhuma delas está ao lado do A3.

O que tem de mudar antes de a REG-01 avançar: o A3 passa a ler-se

> *entre as unidades com linha de base contínua, os dois focos são o pior e o
> segundo pior — **P(a ordenação estar errada) = 0,07 pela reamostragem de
> cenas e 0,25 pela reamostragem de anos; retirado 2026, cai**.*

Não é uma retracção. É a diferença entre um facto e um facto com intervalo, e
esta cadeia já retirou dezanove veredictos por não a fazer.

**L2 · A condição 5 do `guarda.py` autoriza a afirmação de hoje, e volta a
autorizar o A3 que ela foi escrita para bloquear.**

Não respondi a esta pergunta a ler o código. Pus o portão a julgar. Corri
`_controlo3\c3_11_guarda_condicao5.py`.

*Primeiro*, a afirmação de hoje, com tudo o que ela tem — instrumento, duas
confirmações independentes, `comparacao_temporal=True` e
`identidade_no_tempo("ortofoto DGT + série anual")`:

> **O PORTÃO AUTORIZA.**

E autoriza apesar de, ao mesmo tempo, a identidade no tempo estar verificada
para os 8 excluídos e para nenhum dos 29 mantidos (N2), a unidade-alvo ser um
recorte contra parcelas inteiras (C9), a mediana de controlo ter 12 dos 29
blocos do próprio dono (C10) e a margem ter P(≤ 0) = 0,252 (L1).

*Segundo*, e é o que fecha a pergunta 6. Reconstruí o **A3 retirado** — os cinco
blocos do 297313, Sentinel-2 confirmado por Landsat — e acrescentei-lhe **uma
linha**:

```
g.identidade_no_tempo("declaracao do IFAP, campanha 2026")
```

> **VEREDICTO: há blocos vizinhos muito piores**
> unidade no tempo: declaracao do IFAP, campanha 2026

**Passa.** Uma linha a mais, zero dados a mais, e o décimo nono veredicto
retirado sai outra vez — com uma «verificação» que o cabeçalho de
`reg01_landsat.py` **explicitamente declara não ser uma**: «a declaração do IFAP
cobre uma campanha; a continuidade da cultura ao longo da linha de base NÃO está
verificada».

Três buracos, por gravidade:

**A · `identidade_no_tempo(instrumento, ok=True)` tem o `ok` verdadeiro por
omissão.** As condições 3 e 4 recebem **números** — `ancoras()` recebe duas
amostras e compara quartis, `reproduz()` recebe duas matrizes e mede a diferença
máxima. A condição 5 recebe **uma cadeia de caracteres e acredita nela**. É a
única condição do portão que não calcula nada.

**B · `comparacao_temporal` é `False` por omissão, e quem a liga é o analista.**
No auto-teste, o A3 só é bloqueado porque o autor do auto-teste, que já sabia a
resposta, construiu o objecto com a bandeira ligada. Um facto temporal declarado
sem ela atravessa as quatro condições antigas como se a quinta não existisse — e
é exactamente o analista que não pensou na identidade da unidade quem decide se
a bandeira se liga.

**C · Nenhuma das cinco condições interroga a unidade no ESPAÇO.** As quatro
primeiras interrogam o instrumento; a quinta, a unidade no tempo. Nenhuma
pergunta de onde veio a máscara nem se ela foi derivada do sinal que se vai
medir — **que é a primeira das duas regras de higiene da `CLAUDE.md`**, a lição
do `fazer_masks_v2.py`, e a única regra escrita deste projecto que não tem
condição no portão. Neste caso a máscara do foco ORIENTAL leva um filtro de um
instrumento datado dentro da janela do acontecimento, e passou sem que ninguém
tivesse de o declarar. Sobreviveu ao teste (C8) — mas sobreviveu porque eu fui
correr o teste, não porque o portão o exigisse.

**O próximo erro da mesma família, escrito antes de acontecer.** A condição 5
nasceu da frase *«dois instrumentos concordarem não valida a definição da
unidade»*, e cobriu-lhe metade — a unidade no tempo. A outra metade é:

> **dois instrumentos concordarem não valida o recorte da unidade no espaço,
> nem a população com que ela é comparada.**

Na forma em que vai aparecer: *uma unidade recortada onde o sinal é pior — por
sinal, por testemunho, ou por um filtro derivado de um instrumento datado depois
do acontecimento — comparada com unidades administrativas inteiras que ninguém
recortou, e declarada «a pior de N», com dois instrumentos a concordar.* Os dois
instrumentos concordam porque vêem o mesmo recorte. As cinco condições passam
todas. E o número é um **máximo de muitos** de um lado e uma **média de cada um**
do outro — que é, literalmente, a comparação que a REG-01 refeita faz hoje.

A condição que falta, e o que ela teria de exigir — **medido, não declarado**,
como `ancoras()` e `reproduz()`:

```
6 · SIMETRIA DE RECORTE. Quando o facto ordena unidades, ou todas sofreram o
    mesmo recorte, ou o recorte foi aplicado às comparadoras e o facto
    sobrevive. Bloqueia se a unidade-alvo não bater as comparadoras recortadas
    da mesma maneira, e exige que a selecção seja fora de amostra.
```

Neste caso passaria — o C9 mostra que passa, 9 de 10 e 22 de 24. **Mas passaria
medido.** E as duas correcções mínimas à condição 5, antes de qualquer outra
coisa: `identidade_no_tempo` deixa de aceitar uma cadeia de caracteres e passa a
receber a prova (as duas séries, ou as duas fracções, e a diferença entre elas);
e `comparacao_temporal` deixa de ter valor por omissão — ou o autor declara, ou
o veredicto não sai.

---

## NOTA DE MÉTODO

Onze scripts, em `_VALIDADE_GESTAO\_controlo3\`:

| | ficheiro | o que decide |
|---|---|---|
| 00 | `c3_00_comum.py` | matriz cena × unidade, reconstruída da cache |
| 01 | `c3_01_triagem_sensibilidade.py` | reprodução, simetria da janela, grelha 40× |
| 02 | `c3_02_penhasco.py` | onde os limiares partem; o peso dos três |
| 03 | `c3_03_margem.py` | bootstrap de cenas, jackknife por ano |
| 04 | `c3_04_anos_e_donos.py` | bootstrap de anos, mediana por dono |
| 05 | `c3_05_sobreposicao.py` | os focos contra os polígonos do IFAP |
| 06 | `c3_06_unidade.py` | o filtro de copado; simetria de recorte |
| 07 | `c3_07_mascara_pre.py` | a máscara de 2021 contra a de 2025 |
| 08 | `c3_08_orto_tres.py` | ortofoto sobre os três excluídos |
| 09 | `c3_09_olhar.py` | os recortes RGB, 2012 · 2018 · 2021 · 2025 |
| 10 | `c3_10_jovens.py` | rastreio de pomar jovem entre os 29 |
| 11 | `c3_11_guarda_condicao5.py` | o portão posto a julgar a afirmação de hoje |

**Falhas técnicas, para o registo.** Uma só: o `c3_07` rebentou na primeira
corrida com `UnicodeEncodeError` num `∩` impresso na consola cp1252. Substituí o
caracter e correu. Nenhum resultado foi afectado, e nenhum teste ficou por
correr por razão técnica.

**O que não fiz.** Não tentei o LiDAR (N5). Não refiz a corrida em Sentinel-2:
toda a auditoria corre no Landsat, que é o instrumento em que a triagem e a
retracção assentam — se o resultado dependesse da constelação, a discordância
entre as duas já teria aparecido em 01-09, e não apareceu.

---

**Nota final.** Vim procurar o erro. Encontrei dois números errados, uma
descrição de três blocos que estava invertida, uma palavra — «cego» — que não se
sustenta, e um portão que volta a autorizar o veredicto que ele foi escrito para
bloquear. **Não encontrei maneira de derrubar a conclusão.** Quarenta limiares,
três medianas, duas máscaras de chão de datas opostas, o recorte estendido a
todos os competidores fora de amostra, treze blocos suspeitos retirados, o dono
inteiro retirado — os dois focos ficam em primeiro e segundo em todas. O que
resta contra ela não é um erro de desenho: é a amostra. **Dois anos no período
pós, e a conclusão inteira assente em 2026.** Isso não se corrige com mais
análise, e é por isso que é *line-stop* e não retirada.
