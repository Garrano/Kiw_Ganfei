# C8 · CONTROLO 3 — o adversário sobre o troço de rede que nenhum teste alcançou

**Data:** 04-09-2026 · **Alvo:** o facto **C8** da `LISTA_FINAL_2026-08-31.md`,
o script que o produziu (`_VALIDADE_GESTAO\valvulas_1a5_o_troco_que_falta.py`
+ `valvulas_1a5.json`, escritos hoje às 08:38), a entrada correspondente em
`registo_de_factos.py` §C8, e o `Esquema de rega retificado.pdf` de que tudo
isto se reclama.
**Código:** `_VALIDADE_GESTAO\_controlo3_c8\` — nove scripts, todos corridos.
**Não toquei em nada fora dessa pasta**, nem nos boletins A2, nem em
`_controlo3_a2\`. Não descarreguei nada: o PDF já estava em disco desde
28-08 11:48, e a tabela de áreas do gestor já estava transcrita em
`ganfei_s2\b1_divisao.py` e em `ganfei_s2\figuras\m1_v8_implantacao.py`.

---

**A conclusão do C8 resiste. Quase nenhuma das provas com que ele a sustenta
resiste, e a prova central é falsa.**

O teste que fechou «rede de rega sobre-estendida» **de facto** não alcançava o
troço oeste — e prova-se pela caixa da AOI, que não passa pelo esquema de rega
nem por nenhuma das suas reconstruções. Mas a frase que o C8 escreve como
achado — *«as válvulas 1 a 5 não estão em nenhuma das quatro reconstruções»* —
**é falsa**: estão em `valvulas_v4.json`, com coordenada UTM, numa chave
chamada `lobo_oeste` que o leitor do C8 não abre por um defeito de duas linhas.
E o critério que o próprio C8 fixou antes de correr diz, textualmente, que se
elas estiverem em alguma reconstrução «a hipótese continua fechada e este
ficheiro não serve para nada». **O veredicto foi publicado contra o critério
pré-registado do documento que o publicou.**

O C8 também subestima o problema por um factor de duas vezes: não é um troço
que falta, são dois, e o que ficou fora da partição são **39,2 % da área
tabelada da exploração**, não cinco válvulas.

E há uma coisa pior do que qualquer número: **tudo o que o C8 apresenta como
descoberta de hoje estava em disco desde 28-08 às 23:37 e 01-09 às 18:20.** A
nota «POR COLOCAR» que ele cita como estado do conhecimento foi escrita às
22:19 de 28-08 e **substituída setenta e oito minutos depois**, na mesma noite,
pelo G36 da `CAMADA_0_REVISAO_R2.md`, que coloca o B1 = válvulas 1 a 5 = 9,01
ha com duas coordenadas duras do gestor.

---

## CONFIRMADO

**C1 · O núcleo do C8 é verdadeiro, e prova-se sem tocar no esquema de rega.**
A partição por válvula do `rede_de_rega.py` corre sobre as células de
`masks_geograficas.json` dentro da AOI **E 529 950–531 950 · N 4 654 600–
4 655 600**. O sector B1, medido pelo IFAP, é **E 529 495–530 063 ·
N 4 653 832–4 654 477**. As duas caixas **não se intersectam**: o B1 fica
**123 m a sul** do bordo sul da AOI. A partição de Voronoi nunca teve uma
célula no B1, em nenhuma das 11 cenas, com qualquer conjunto de válvulas.
Isto é a pergunta 11 da pré-voo, e a resposta é a que o C8 dá.
*Ficheiro:* `c8_05_veredicto.py` §V3.
**E é melhor prova do que a que o C8 usou**, porque não passa pelo esquema:
depende só da AOI e do parcelário, dois objectos independentes do desenho.

**C2 · As doze unidades da partição são mesmo as 6 a 17, todas no corpo.**
`rede_de_rega.json` guarda `por_valvula` com exactamente doze chaves — 6, 7, 8,
9, 10, 11, 12, 13, 14, 15, 16, 17 — e o teste de ordem na rede reporta `n=12`
em todas as cenas. As posições vêm de `valvulas_por_area.json`, que enumera
essas doze e mais nenhuma.
*Ficheiro:* `c8_05_veredicto.py` §V2.

**C3 · A nomenclatura fecha, e fecha por leitura directa do documento.**
Abri o PDF e li as notas manuscritas à mão, em tinta azul, por baixo do
desenho: «Cabo eléctrico do Campo **B1 C3** para o **B1 C2** passa a 3 metros
das arriostas», «Cabo eléctrico do Armazém para o **B1** passa a 12 metros da
vedação do campo das ovelhas», «Conduta de água principal do Armazém para o
**B1** passa a 15 metros…», «Cruzamento de condutas no **B1 C2** passa a 4
metros da arriosta no eito da Linha 149», «válvula desactiva na linha 185».
E a palavra **B1**, a vermelho, está escrita sobre o troço oeste.
Os boletins de solo rotulados B1 C1 / C3 / C4 são sub-campos deste troço, tal
como o C8 diz. **Esta parte do C8 é sólida e é útil.**
*Ficheiros:* `rec_F_faixa_baixa2.png`, `rec_A_lobo_oeste.png`, e o recorte
`_esquema\notas.png` que já estava em disco.

**C4 · «Reabrir não é confirmar» está certo e deve ficar.**
A formulação final do C8 — *não se conclui que a rega explica o declínio,
conclui-se que a hipótese não foi testada onde teria de ser* — é a única forma
dizível, e o C8 acertou nela. **Nada do que se segue a retira.**

**C5 · O documento tem uma identidade, e agora está medida.**
O PDF é de uma página A4 paisagem com **uma só imagem embebida, JPEG de
2338 × 1654 px** — exactamente A4 a **200 dpi**. Não tem texto extraível
(`get_text()` devolve 0 caracteres). A cartela diz **SISTEMA DE REGA PARA
ESPAÇOS VERDES · Valença–Minho · «Sistema de rega automatizado para kiwis» ·
desenhador Tiago Fonseca · PRILUX · DATA JUL 09 · ESC 1/3500 @ A1**.
*Ficheiros:* `c8_01_extrai.py`, `c8_01_extrai.json`, `T13_cartucho.png`.
**Consequência de método, e não é do C8:** a C0 renderizou este PDF a **300
dpi** (`c0_06`, `c0_08`, `c0_13`). Trezentos dpi sobre um original de 200
**interpola**; não acrescenta informação, e faz parecer mensurável o que não é.

---

## CORRIGIDO

**R1 · O «11/11» são cenas, não válvulas. O C8 escreve «11 a 12 válvulas».**
`rede_de_rega.json` tem onze cenas no teste de agrupamento — 2017-07-02 a
2026-07-27 — e **as onze têm p > 0,05**. As unidades da partição são **doze**,
sempre doze. Não há nenhuma corrida com 11 válvulas.
O script imprime, em F4: «*O teste que fechou «rede sobre-estendida» correu
sobre **11 a 12** válvulas, todas no corpo principal*» — misturando a contagem
de cenas com a contagem de unidades, e deixando uma ambiguidade onde não há
nenhuma. A `LISTA_FINAL` e o `registo_de_factos.py` §C8 dizem «doze», que está
certo; **a saída do script e a prosa divergem, e o `certificar.py` não apanha
isto porque só compara códigos de facto, não números dentro deles.**
*Forma corrigida:* «doze válvulas, todas do corpo principal, em onze cenas».
*Ficheiro:* `c8_05_veredicto.py` §V2.

**R2 · Não é um troço que falta. São dois, e valem 39,2 % da exploração.**
A tabela de áreas do gestor — testemunho de tipo 1, transcrita em
`ganfei_s2\figuras\m1_v8_implantacao.py` e `ganfei_s2\b1_divisao.py` — tem
**vinte e cinco entradas de válvula**, não doze:

| conjunto | válvulas | área |
|---|---|---|
| banda contígua, a que entrou no teste | 6–17 (12) | **27,30 ha** |
| **B1** | 1–5 (5) | **9,01 ha** |
| **parcelas soltas** B4C3, B5, B1C5, B3C4, Viveiro ×2, B1C6, B3C3 | 18–25 e 27 (8 entradas) | **8,62 ha** |
| **total tabelado** | 25 | **44,93 ha** |

A partição por válvula usou **27,30 de 44,93 ha = 60,8 %**. Ficaram fora
**17,63 ha, 39,2 %, em treze unidades de válvula**. O C8 fala de «cinco
válvulas»; são treze.
*Ficheiro:* `c8_05_veredicto.py` §V4.
*E isto responde à pergunta 6 do mandato:* sim, existem válvulas para lá da 17,
e não estão só nas notas manuscritas — estão na **tabela de áreas**, que é
documento e não anotação. Não há válvula 26; a 24 e a 25 vêm agregadas numa
linha.

**R3 · A correcção de 03-09 não foi suficiente. A frase que ficou tem o mesmo
defeito da que substituiu.**
A frase corrigida diz: *«O que é sólido é o contido: o B1 do IFAP cai
inteiramente dentro da caixa do G19.»* Medi as quatro folgas:

| bordo | folga do B1 dentro do G19 |
|---|---|
| oeste | 145 m |
| este | **22 m** |
| sul | 132 m |
| **norte** | **1 m** |

**Os quatro bordos têm folga inferior à incerteza declarada de ±150 m.**
Deslocar a caixa do G19 de 150 m em qualquer direcção — o que o erro declarado
permite — destrói a continência. Dizer «cai inteiramente dentro» dentro de um
envelope de ±150 m é a mesma coincidência de arredondamento que «batem a 1
metro», com outra roupa.
*Ficheiro:* `c8_05_veredicto.py` §V5.

**E há um teste que decide isto, e não é recomputação.** Existem **duas**
georreferenciações independentes do mesmo PDF, feitas na mesma tarde de 28-08.
Medidas contra o segmento que o gestor deu por coordenadas (E 529 500
N 4 654 010 → E 530 054 N 4 654 413, tipo 1):

| extrapolação | distância mediana ao segmento do gestor |
|---|---|
| `c0_13_georref.json`, os dois anéis de menor x | **94 m** — sobrevive aos ±150 m |
| `valvulas_v4.json['lobo_oeste']`, válvulas 1–5 | **491 m** — **falsificada** |

E **uma contra a outra: 505 m de distância mínima entre os conjuntos, 734 m
entre centróides.** Duas leituras do mesmo desenho, feitas na mesma tarde
(`c0_13_georref.json` às 18:45, `valvulas_v4.json` às 22:24 de 28-08),
colocam o troço oeste a mais de meio quilómetro uma da outra.
**O esquema não carrega posição utilizável para as válvulas 1–5.** Quem tem
posição é o gestor, e tem-na desde 28-08.
*Ficheiro:* `c8_06_extrapolacoes.py`, `c8_06_extrapolacoes.json`.
*Forma corrigida:* apagar o G19 desta frase. Escrever «o B1 fica entre
E 529 500 N 4 654 010 e E 530 054 N 4 654 413, por duas coordenadas do gestor»,
que é tipo 1 e não precisa do desenho.

**R4 · «Um lóbulo fisicamente separado ao extremo oeste» — não é o que o
desenho desenha.**
A linha «Limites do terreno» corre sem interrupção do troço oeste ao extremo
leste, e entre os dois há três parcelas desenhadas **dentro do mesmo limite**,
sem tramado de sector. Medido: o tramado de sector existe de x = 133 a
x = 2129, e o maior intervalo sem tramado nenhum é de **393 px, de x = 624 a
x = 1016 — 19,7 % do comprimento desenhado**.
*Forma corrigida:* «o extremo oeste da mesma parcela desenhada, separado do
corpo regado por cerca de um quinto do comprimento sem sector de rega».
*Ficheiros:* `c8_07_contiguidade.py`, `T3_vazio_meio.png`.
*Ressalva:* a continuidade da linha de limite é **leitura visual** do recorte
nomeado. Tentei medi-la por componentes conexas e o traço, de 1 px e degradado
pelo JPEG, aparece em 323 de 549 colunas do vão — **não decide**, e não se
apresenta como se decidisse. O que está medido é o vão sem sector.

**R5 · «As notas manuscritas do projectista» — a atribuição não tem
fundamento.**
A cartela data a impressão de **JUL 09**. As notas manuscritas descrevem
alterações **posteriores** à obra: «**6 novas válvulas**» (leitura provável;
o dígito é ambíguo a 200 dpi) e «válvula desactiva na linha 185». Esta última
é a mesma alteração que o gestor relatou, e que `rede_de_rega.py` cita no
cabeçalho como testemunho. **O projectista de 2009 não podia anotar uma
desactivação posterior.**
*Forma corrigida:* «as notas manuscritas sobre o desenho», sem atribuição.
**Quem as escreveu, e quando: NÃO SABIDO**, e fica em branco à vista.
*Ficheiros:* `_esquema\notas.png`, `T13_cartucho.png`.

**R6 · A tabela «Débito dos Sectores» tem treze sectores, não catorze.**
Transcrita do documento: A-65 · B-85 · C-90,5 · D-96,8 · E-87,6 · F-79,1 ·
G-99,9 · H-91,5 · I-78,5 · J-71,6 · L-56,8 · M-55,3 · N-82,7 m³.
**Não há sector K** — o desenho usa o alfabeto português antigo, que o salta.
Quem contar de A a N em alfabeto inglês conta catorze; são treze. Total
**1040,3 m³**. E o `valvulas_v6.json`, escrito a 28-08, já tinha a lista
`_sectores` com estes treze exactos.
*Ficheiro:* `c8_04_sectores.py`, `c8_04_sectores.json`.

**R7 · `rede_de_rega.py` diz «a válvula 185 foi desactivada». Não existe
válvula 185.**
O desenho diz «válvula desactiva **na linha 185**» — a 185 é uma fileira de
plantação, e as válvulas vão até 27. O `m1_v7.py` já tem a frase certa. A
correcção não muda cálculo nenhum, mas é a assinatura da família B — o nome a
fazer trabalho de prova — no cabeçalho do próprio ficheiro que produziu o
número que o C8 ataca. *Fica corrigido no registo, não no ficheiro.*

---

## REJEITADO

**X1 · «As válvulas 1 a 5 não estão em nenhuma [das quatro reconstruções]» —
FALSO. E o próprio C8 tinha escrito o que fazer se assim fosse.**

`ganfei_s2\valvulas_v4.json` tem uma chave `lobo_oeste` com as cinco:

```
1  E 528 959  N 4 654 101      4  E 529 034  N 4 654 163
2  E 528 996  N 4 654 106      5  E 529 219  N 4 654 234
3  E 529 110  N 4 654 187
```

O leitor do C8 faz `d.get("valvulas", d.get("metros_por_linha", d))`. O
`valvulas_v4.json` não tem nenhuma dessas duas chaves, logo cai no dicionário
de topo, cujas chaves são `_metodo`, `m_por_pixel_400dpi`, `corpo`,
`lobo_oeste`… — nenhuma é um dígito. Devolve zero. **E o comentário que o
próprio C8 escreveu por cima dessa linha afirma que «`valvulas_v4.json` tem
"corpo"/"lobo_oeste" … nenhuma delas enumera válvulas».** As duas enumeram:
`corpo` tem a 6 à 17 e `lobo_oeste` tem a 1 à 5.
Lidas as quatro pela estrutura real de cada uma — o mesmo critério que o
`c4_r2_01_multiverso_das_valvulas.py` já usava desde 01-09 — a união é
**1 a 17**, e as 1 a 5 não faltam a nenhuma união.
*Ficheiro:* `c8_05_veredicto.py` §V1.

**O que torna isto uma paragem de linha e não uma gralha:** o critério
pré-registado do C8, na sua própria docstring, diz textualmente —

> «Se as válvulas 1-5 estiverem em **alguma** das quatro reconstruções, a
> hipótese continua fechada e este ficheiro não serve para nada.»

Aplicado honestamente aos ficheiros, esse critério imprimia «a hipótese
continua fechada». **O veredicto publicado é o contrário do que o critério
pré-registado manda.** É a armadilha nº 7 da lista mecânica — *contar o que a
saída diz, não o que se espera* — só que aqui a saída também estava errada,
porque o leitor estava errado.

**A ironia, e é instrutiva:** se o C8 tivesse lido bem, teria fechado a
hipótese — e teria fechado mal, porque as posições de `lobo_oeste` estão
**falsificadas pelo testemunho do gestor** (R3: 491 m de mediana contra ±150 m
declarados). **O critério estava mal desenhado.** «Estão nalgum ficheiro?» não
é a pergunta; «entraram na partição que correu?» é. E a resposta a essa é não,
e prova-se pela AOI (C1).

**X2 · «Com um fundamento que invoca "o lóbulo oeste", o objecto retirado a
28-08» — é uma correspondência de cadeia de caracteres, não um teste de
referente.**
O teste do C8 é literalmente `usa_lobo = "lobo" in str(nota).lower()`.
O objecto retirado a 28-08 é a **AOI** `b1` = (528 400, 4 654 900, 529 400,
4 655 700), tecido urbano de Valença do outro lado do Minho, com 49 ficheiros
em quarentena (G24). O `lobo_oeste` do `valvulas_v4.json` está em
N 4 654 101–4 654 234 — **666 a 799 m a sul do bordo sul dessa AOI**, e a
360–549 m do B1 real. **Não é o mesmo objecto.** A palavra «lobo oeste» é usada em
`valvulas_por_linha.json` e em `valvulas_v4.json` como descrição do troço oeste
do **desenho**.
E o raciocínio da nota «POR COLOCAR» é sólido e independente da AOI retirada:
o esquema anota as linhas **137 e 156** para as válvulas 4 e 5 e a **149** para
as 1, 2 e 3 — e as âncoras desse ficheiro vão da linha 130,5 à 423, no corpo
principal. Se aquelas linhas fossem as mesmas, as válvulas 1-5 cairiam dentro
do corpo, o que é geometricamente impossível. Logo o troço oeste tem numeração
de linha própria, e as âncoras não o alcançam. **Isso está certo.** Li as
anotações no desenho e confirmam-se.
*Ficheiros:* `T3_vazio_meio.png`, `rec_A_lobo_oeste.png`, `c8_05_veredicto.py`
§V1.
**Isto é a família B a acontecer dentro da peça que existe para a apanhar:** o
nome do objecto a fazer trabalho de prova.

**X3 · «O esquema anota 1,77 ha para o B1; o IFAP dá 12,63 ha — factor 7,1×.»
Sai inteira.**

*(a) Não encontrei o «1,77 ha» no documento.* Varri a folha inteira à procura
de tinta vermelha saturada: **17 aglomerados com ≥120 px**, e o mais largo tem
**63 px**. O aglomerado «B1», de dois caracteres, mede 35 px — cerca de 18 px
por carácter. «1,77 ha» mediria ~122 px. Nenhum aglomerado na folha se aproxima
disso. Os dezassete são os círculos de válvula e o «B1».
**Diz-se «não encontrado», não «não existe»:** a 200 dpi, uma anotação a lápis
ou a azul claro pode ficar abaixo do limiar.
*Ficheiros:* `c8_03_tinta.py`, `c8_03_tinta.json`, `c8_08_o_177.py`.

*(b) A tabela do gestor contradiz o número.* B1 = válvulas 1 a 5 = **13 500 +
9 375 + 12 750 + 24 550 + 29 900 = 90 075 m² = 9,01 ha**. Nenhuma válvula do B1
tem 1,77 ha. A mais pequena tem 1,35 ha. 1,77 ha são **20 % do B1**.

*(c) O quociente compara três definições de unidade.* Um sector de rega é uma
unidade hidráulica; uma parcela do IFAP é uma unidade administrativa; o bloco
do G19 é uma assinatura de textura em ortofoto. **Dividir uma pela outra não
mede discrepância nenhuma.** E o **C7**, já certificado, proíbe exactamente
isto: «a atribuição de válvulas não sustenta nenhuma quantidade… nenhuma peça
pode escrever uma área por válvula». O C8 escreve o factor 7,1× e chama-lhe
«uma instância concreta do C7». **Não é uma instância do C7 — é uma violação
do C7.**

*E isto já tinha sido mandado retirar.* `CAMADA_0_ADVERSARIO.md`, 28-08 19:17,
no veredicto: «*retirar da M1 v2 os rótulos «válvulas 1–5 / B1 / 1,77 ha» … que
são prosa a viajar num mapa que sai para fora*». O mesmo documento propôs medir
as duas áreas anotadas como teste de cinco minutos; não consta que tenha
corrido. **Sete dias depois o rótulo voltou, como facto certificado.**

**X4 · «O C8 é um achado novo» — não é. É o estado do registo às 22:19 de
28-08, ressuscitado.**
A cronologia por datas de ficheiro:

| | |
|---|---|
| 28-08 22:19 | `valvulas_por_linha.json` — a nota «POR COLOCAR» que o C8 cita |
| 28-08 22:24 | `valvulas_v4.json` — **coloca** as válvulas 1–5 |
| 28-08 23:37 | `CAMADA_0_REVISAO_R2.md` — **G35**: «o gestor deu a tabela válvula↔bloco↔área, total 44,93 ha»; **G36**: «**B1 = válvulas 1 a 5 = 9,01 ha**, entre E529500 N4654010 e E530054 N4654413, a 526 m do corpo principal» |
| 28-08 23:59 | `b1_divisao.py` — divide o B1 pelas cinco válvulas |
| 01-09 18:20 | `CAMADA_0_REVISAO_R3.md` §2, cujo título é literalmente «**FECHA a NÃO TESTÁVEL do bloco sudoeste — G19**» |
| 04-09 08:38 | o C8 |

**A nota «POR COLOCAR» durou setenta e oito minutos.** O C8 cita-a às 08:38 de
04-09 como se fosse o estado corrente.

E a resposta à pergunta 2 do mandato é **sim, e com mais precisão do que a
pergunta supunha**: o NÃO TESTÁVEL da C0 nomeava três coisas que o fechariam —
«a tabela de válvulas com áreas, ou a confirmação da gestora, ou o parcelário».
**Chegaram as três**, e a R3 fechou-o a 01-09, e a `LISTA_FINAL` já o regista
como **C3**. O C8 escreve «*E fecha o "pertença NÃO confirmada" do G19*» como
se fosse consequência sua; é consequência da R3, três dias antes.

**Mas o C8 não é redundante, e é justo dizê-lo.** O que a R3 deixou **aberto**,
em NÃO TESTÁVEL e por escrito, foi: «*Se a rede de rega é partilhada entre o
corpo principal e o bloco sudoeste. O parcelário não responde a isto.*»
**Essa é exactamente a pergunta do C8.** O que o C8 acrescenta de genuinamente
novo é a **contradição**: a P06 continuava a listar a hipótese na coluna JÁ
FECHADO enquanto a R3 a tinha em NÃO TESTÁVEL desde 01-09. **Isso vale, e é o
que o C8 devia ter dito de si próprio** — em vez de se apresentar como achado.

**X5 · A condição 2 do portão, no §C8 do `registo_de_factos.py`, está
satisfeita por auto-referência.**
Três confirmadores estão declarados:
1. «testemunho do gestor, tipo 1, 03-09-2026» — **este vale**, e é o que
   sustenta o facto;
2. «o próprio esquema de rega (PDF, 28-08)», com `prova = o PDF` — **o esquema
   não confirma independentemente uma afirmação sobre as reconstruções do
   esquema.** É um NDVI a confirmar um NDVI;
3. «geometria, com a incerteza à vista», com `prova = valvulas_1a5.json` — que
   é **o ficheiro de saída do script que está a ser certificado**.
O portão passa porque o nº 1 basta. Mas dois dos três confirmadores são o
próprio objecto. *Corri o portão: `registo_de_factos.py` dá 26 factos, 0
bloqueios, e o `certificar.py` certifica.* **A certificação é verdadeira e não
protege deste erro** — nenhuma das seis condições interroga se o leitor do
ficheiro leu o ficheiro.

---

## NÃO TESTÁVEL

- **O mapeamento sector → válvula.** Três enumerações da mesma rede, três
  cardinalidades: **13** sectores impressos, **18** números de válvula no
  desenho, **25** entradas na tabela do gestor. E as dispersões são
  incompatíveis com uma correspondência 1:1 — o débito por sector varia
  **1,81×** (55,3 a 99,9 m³, CV 0,179) e a área por válvula varia **19,9×**
  (1 500 a 29 900 m², CV 0,462), **onze vezes mais**. Fecha-o uma tabela de
  sectores com área, ou o gestor. Não o fecha mais cálculo.
  *Ficheiro:* `c8_09_tres_enumeracoes.py`, `.json`.
- **O número do décimo-oitavo bloco.** A leste da válvula 17 há um quarto
  bloco tramado com número circulado a vermelho que **não é legível a 200 dpi**,
  em nenhuma rotação que tentei. O `CAMADA_0_CERTIFICADO` já registava «o
  desenho mostra pelo menos 18 números». A tabela do gestor tem uma válvula 18
  (B4C3, 5 500 m²), o que é compatível e não é prova.
  *Ficheiros:* `Z_ultimo.png`, `Z_rot_*.png`, `T7_v16_v18.png`.
- **Se a rede é hidraulicamente partilhada entre os dois troços.** Já estava
  aberto desde a R3 da C0. O parcelário não responde, a pertença administrativa
  não determina origem de água, e **contiguidade de propriedade não é
  contiguidade hidráulica**. O que existe a favor: o projecto de 2009 sectoriza
  os dois troços na mesma folha e na mesma tabela de débito, e as notas
  manuscritas descrevem uma conduta principal *do Armazém para o B1*. Isso é
  indício documental, não medição.
- **Quem escreveu as anotações manuscritas, e quando.** NÃO SABIDO (R5).
- **Se o «1,77 ha» existe em alguma parte do documento.** Fecha-o uma
  digitalização a resolução maior, que a C0 já tinha pedido a 28-08. Enquanto
  não existir, o número não pode aparecer em peça nenhuma.

---

## LINE-STOP

**Não passa nada que cite o F1 do C8 — «as válvulas 1 a 5 não estão em nenhuma
das quatro reconstruções» — enquanto essa frase estiver escrita.** É falsa por
leitura de ficheiro, e a leitura está em `c8_05_veredicto.py` §V1, que corre em
dois segundos.

**A paragem é sobre a prova, não sobre a conclusão.** O C8 sobrevive, e
sobrevive melhor do que estava: reescrito sobre a caixa da AOI (C1) e sobre a
tabela de áreas do gestor (R2), passa a dizer uma coisa mais forte e mais
defensável do que a que dizia.

**A forma que passa**, e é para substituir o parágrafo inteiro:

> **C8 · A hipótese «rede de rega sobre-estendida» foi fechada por um teste que
> cobria 60,8 % da exploração.**
> A partição por válvula correu sobre **doze válvulas — 6 a 17 — em onze
> cenas**, todas dentro da AOI E 529 950–531 950 · N 4 654 600–4 655 600.
> A tabela de áreas do gestor tem **vinte e cinco entradas de válvula, 44,93
> ha**. Ficaram fora **17,63 ha (39,2 %) em treze unidades**: o **B1**
> (válvulas 1–5, 9,01 ha, entre E 529 500 N 4 654 010 e E 530 054 N 4 654 413
> por coordenadas do gestor, **123 m a sul do bordo da AOI**) e as **oito
> parcelas soltas** (válvulas 18–25 e 27, 8,62 ha), que têm área tabelada e
> **não têm posição**.
> *Confirmado por:* **testemunho de tipo 1** — a tabela válvula↔bloco↔área e as
> duas coordenadas do B1, gestor, 28-08-2026 — e pela **geometria da AOI**, que
> é independente do esquema de rega.
> *A hipótese não passa a confirmada.* Passa de FECHADA a **fechada só para o
> corpo principal**, que é o que a `CAMADA_0_REVISAO_R3.md` já tinha em NÃO
> TESTÁVEL desde 01-09 — «se a rede de rega é partilhada entre o corpo
> principal e o bloco sudoeste». **O que o C8 acrescenta é que a P06 continuava
> a dizer o contrário.**
> *E o esquema de rega não entra nesta frase:* duas georreferenciações do mesmo
> PDF colocam o troço oeste a 505–734 m uma da outra, e a que coloca as
> válvulas 1–5 erra **491 m** contra o testemunho, sobre uma incerteza
> declarada de ±150 m. **O desenho serve para saber o que existe — sectores,
> válvulas, nomenclatura B1C2/B1C3 — não para saber onde.**

**As três frases que saem e não voltam:** «as válvulas 1 a 5 não estão em
nenhuma», «o fundamento invoca o objecto retirado a 28-08», e «o esquema anota
1,77 ha … factor 7,1×».

**E uma correcção de método, que é a única que vale para a próxima vez.**
O C8 fixou o critério antes de correr, como manda a regra — e fixou o critério
errado. «As válvulas estão nalgum ficheiro?» não decide nada sobre um teste;
decide sobre um ficheiro. A pergunta que decidia era «**que células entraram na
partição que correu?**», e essa responde-se em três linhas contra a AOI, sem
abrir reconstrução nenhuma. **Um critério pré-registado protege contra o
resultado que dá jeito; não protege contra a pergunta errada.** É o ponto 3 do
`ANTES_DE_COMECAR` — pergunta aberta, ou pergunta ao lado, garante divergência
não interpretável — e foi por aí que esta peça se perdeu, com o número certo
no fim.
