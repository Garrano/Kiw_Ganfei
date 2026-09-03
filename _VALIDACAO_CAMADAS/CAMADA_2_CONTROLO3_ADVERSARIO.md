# Camada 2 · Controlo 3 — adversário independente do certificado R2

**Data:** 01-09-2026 · **Escreve:** sessão paralela, sem acesso a dados brutos
**Ataca:** `CAMADA_2_CERTIFICADO_R2.md` e `CAMADA_2_TESTES_T1_T5.md`
**Lê:** o código em `_VALIDADE_GESTAO\`, o `PROTOCOLO.md`, o `CONTROLOS.md`,
o `PRE_REGISTO_REFERENCIA.md` e o `REDERIVACAO_MASCARAS.md` da C0.

---

## 0 · Âmbito, e o que deliberadamente não fiz

Não recomputei nada. Não abri nenhum `.tif`, `.npy`, `.laz` nem nenhum `.json`
de resultados. Onde precisei de um número para julgar uma afirmação, **nomeio o
número e o ficheiro** e ponho-o na lista dos cinco testes, em vez de o ir
buscar.

**Não li o `CAMADA_2_ADVERSARIO.md` nem o `CAMADA_2_ADVERSARIO_R2.md`.** Foram
escritos pela mesma sessão que escreveu o certificado e os cinco testes; lê-los
era herdar a ancoragem que este controlo existe para quebrar. Conheço as suas
acusações apenas pelas citações que os próprios ficheiros atacados fazem delas.

O trabalho foi **ler cada cabeçalho contra o código que vem a seguir**. Foi aí
que estava quase tudo o que se segue.

A lista fechada operativa não é a do certificado (S1–S8). É a de
`CAMADA_2_TESTES_T1_T5.md`, **S1–S9**, que ganha por ser medição posterior. É
essa que ataco. Registo desde já que **existem duas listas fechadas em
circulação com o mesmo nome e conteúdos diferentes**, escritas com um dia de
intervalo, e que a segunda não é um certificado — o que a torna, pela regra 1
do protocolo, a classe de documento que a camada seguinte não está autorizada
a herdar. É preciso reemitir como certificado R3.

---

## 1 · Factos a retirar do PASSA PARA CIMA

### R1 · **S6 sai por inteiro.** O teste que o promoveu não podia falhar, e o facto não é novo.

S6 diz: «PROMOVIDO A MEDIÇÃO. A referência tinha 14 células nos focos; limpa, o
seu degrau cai de −0,0481 para −0,0189, e os cinco fossos crescem. Os números
do fosso eram conservadores — medido, não inferido.»

**Primeira razão: o T5 é uma identidade algébrica disfarçada de teste.**

Em `t5_referencia_reconstruida.py`, o fosso de cada unidade é `r − v`, e o que
se lê na tabela é a sua **média sobre as nove cenas**:

```python
fa, fl = r_ant - v, r_lim - v
ma, ml = float(fa.mean()), float(fl.mean())
```

`v` não muda quando se limpa a referência. Logo, para **todas** as unidades,

```
fosso_limpo − fosso_antigo  =  média(r_limpa) − média(r_antiga)  =  δ
```

— **a mesma constante aditiva**, seja a unidade um foco, o resto do pomar ou o
B1. A tabela do T5 confirma-o e ninguém reparou: as cinco variações são
+0,0084 · +0,0085 · +0,0084 · +0,0084 · +0,0085. **É o mesmo número cinco
vezes.**

A frase «cinco fossos cresceram, nenhum encolheu, nenhum mudou de sinal»
carrega, por isso, exactamente **um bit de informação: o sinal de δ**. E o
sinal de δ ficou determinado no momento em que se escolheram, para excluir, as
catorze células com o degrau mais negativo da grelha (−0,1458). Retirar as
células que mais desceram sobe necessariamente a média da referência. **O ramo
«os fossos encolhem → LINE-STOP» do pré-registo era inalcançável por
construção.**

Um pré-registo cujo ramo de falsificação não pode ocorrer não é um pré-registo:
é uma análise defensável barata de gerar, que é precisamente o que a literatura
do multiverso citada por este projecto identifica como o mecanismo pelo qual a
prova fica vulnerável a relato selectivo.

O mesmo vale para a «verificação de construção passou» (o degrau em absoluto
não mexeu): a referência não entra na fórmula do absoluto. O código di-lo —
`# verificacao de que o absoluto nao mexeu` — e o `.md` reporta-o como
verificação passada.

**Segunda razão, e é a mais grave: o facto não é novo.** O §0 do certificado
funda a sua paragem de linha em «é um facto novo, não uma preferência» e «o
adversário não podia saber: a contaminação só foi medida em 31-08». O
`halo_distancia.py` escreve «Isto tem tres consequencias, e nenhuma delas
estava escrita em lado nenhum».

Está escrita. `REDERIVACAO_MASCARAS.md` §3.2 — documento da C0, de herança
obrigatória, que **define a própria máscara `saudavel` que a C2 reanalisou**:

> «**A grelha não evita as manchas, e não deve evitar.** Das 110 células, **18
> caem dentro da antiga `manchaW` e 5 dentro da `zona0`**. É isso que faz dela
> uma amostra e não uma escolha: apanha o pomar em proporção, incluindo a parte
> doente. O efeito é conservador — puxa a referência para baixo e portanto
> **subestima** o défice (quantificado em §4.4).»

Mesmas cinco células na `zona0`. Mesma conclusão. Já quantificada, num §4.4 que
o certificado R2 não cita. A C0 não só sabia: tinha-o registado como
**propriedade deliberada do desenho**.

**O que cai com isto.** (a) A promoção de S6 a medição. (b) O levantamento da
paragem de linha da moeda no T5. (c) A frase «deixa de haver duas moedas em
conflito: há uma grandeza com duas leituras, e as duas contam a mesma
história». (d) **E, por precedência, a própria paragem de linha do §0:** o
certificado rejeitou uma decisão do seu adversário invocando novidade que não
existe, e o corolário da regra 1 diz que, onde certificado e adversário
discordam, ganha o adversário. **A decisão do adversário sobre a moeda tem de
ser reposta ou re-argumentada com outro fundamento.**

**Teste que o derrubaria em dois minutos:** T-a, §4.

---

### R2 · **S7, segunda metade: o `p < 0,0001` do anel sai. As medianas ficam.**

S7 revisto: «o anel de 90–160 m tem mais dano do que o terreno a mais de 120 m
(−0,0271 contra −0,0166, p < 0,0001)».

Esse p vem de `t3_nula_no_estrato.py`:

```python
nl = nula(U_LONGE, kmed, 600)
nb = nula(U_BANDA, kmed, 600)
t = st.mannwhitneyu(nl, nb)
```

`nula()` sorteia repetidamente um centro e toma as `k` células mais próximas
dentro do universo. As 600 «observações» de cada braço são **reamostragens
sobrepostas de um campo fixo**, não observações independentes: com ~21 células
por disco e universos pequenos — a banda 90–160 m é um anel de 70 m de largura
à volta de dois centros —, os mesmos píxeis entram em dezenas de sorteios. O n
efectivo é o número de manchas não sobrepostas, da ordem de dez a vinte por
estrato, não 600. Um Mann-Whitney sobre 600 reamostragens de um campo
espacialmente autocorrelacionado **fabrica o p**: cresce em significância com o
número de sorteios, que é uma escolha nossa.

A ironia é exacta e vale registá-la: é o mesmo erro que a mesma sessão recusou,
correctamente, em `halo_distancia.py` — «permutar celula a celula da p a menos:
as celulas vizinhas nao sao independentes» — e substituiu por um nulo toroidal.
Três dias depois cometeu-o.

**Fica:** a diferença de medianas (−0,0271 contra −0,0166) como **descritivo do
campo**, sem p. **Sai:** o p, e com ele a força da frase «o dano não pára na
fronteira arbitrária dos discos», que passa de resultado a hipótese.

---

### R3 · **S7, primeira metade: «não há halo» sai como afirmação de ausência.**

O nulo toroidal de `halo_distancia.py` roda o campo `deg` inteiro e só depois o
indexa pela máscara do pomar:

```python
r = np.roll(np.roll(campo, dy, 0), dx, 1)[mask]
```

`deg` foi calculado sobre **toda a AOI de 2 × 1 km**, não sobre o pomar. Cada
rotação injecta, nas células do pomar, valores de degrau vindos de mata, milho,
caminho e edificado — coberturas cuja estrutura espacial é muito mais forte e
mais em bloco do que a do interior de um pomar homogéneo. O nulo fica
**sobredisperso**, o |ρ| nulo é rotineiramente grande, e o teste perde potência
por construção.

`p toroidal = 0,55` é compatível com «não há halo» e igualmente compatível com
«há um halo que este teste não vê». **Não distingue os dois, e a potência nunca
foi declarada.**

Isto importa mais do que parece, porque o negativo é **carga estrutural**: o
`PRE_REGISTO_REFERENCIA.md` §2 usa-o como justificação operacional para não
alargar a margem além dos 120 m — «Sem efeito de vizinhança demonstrado, uma
margem grande seria selecção conveniente da referência. O negativo do halo tem
exactamente este uso operacional: impedir que a margem cresça.» Um pré-registo
inteiro está apoiado num resultado nulo de um teste sem potência declarada. E o
T3 mediu depois, no mesmo dossiê, uma diferença real de banda a 90–160 m.

**S7 passa a:** «não foi detectado gradiente contínuo com a distância; o nulo
usado tem potência por estabelecer, e uma medição posterior encontra mais dano
no anel 90–160 m». **Vai para NÃO TESTÁVEL** até o nulo ser refeito com o campo
restrito ao pomar.

---

### R4 · **S9 sai por inteiro. Não tem instrumento, e não é um comparador.**

S9 é o único facto **novo** que os cinco testes acrescentam, e é o mais frágil
dos nove.

**(a) Viola o Controlo 1 sem atenuante.** O B1 não tem LiDAR (as 21 folhas
cobrem só a AOI principal — dito em `lobulo_oeste_degrau.py`), não tem Landsat
(dito em `t4_n_landsat.py`, que o manda para NÃO TESTÁVEL), não tem SAR e não
tem partição pérgola/chão. É medido por **um só instrumento**, a série
Sentinel-2, exactamente como o `CONTROLOS.md` §1 proíbe: «Se não houver
instrumento independente disponível, o facto vai para NÃO TESTÁVEL, não para
PASSA PARA CIMA.» O T4 manda-o para NÃO TESTÁVEL numa linha e o S9 sobe na
linha seguinte.

**(b) A unidade não é comparável.** O próprio cabeçalho di-lo: o B1 «sobe de
0,560 para 0,685 entre 2017 e 2024», enquanto o corpo principal vive entre 0,82
e 0,88. É um bloco jovem, em enchimento, longe da saturação; os focos são
copado maduro saturado. O veredicto «a recta vence por ΔAICc +9,57» é o que uma
série monotonamente crescente **sempre** dá — o modelo de degrau não consegue
ajustar uma subida. Note-se que o «resto do pomar», que ninguém contesta ser o
mesmo campo, dá também recta (+6,36). Logo a frase do T1 —

> «O degrau não é uma propriedade de «pomar de kiwi em Ganfei» — é uma
> propriedade dos dois focos.»

— não decorre. O que os dados mostram é «o degrau não é propriedade de unidades
que têm tendência», que é outra coisa e é quase tautológica.

**(c) O cabeçalho declara a direcção do enviesamento ao contrário.**
`lobulo_oeste_degrau.py`:

> «o B1 entra sem restricao de copado… Isso torna-o **conservador** para a
> leitura de controlo — se houvesse chao la dentro, ele puxaria a serie para
> baixo, nao para cima.»

Para um **nível**, sim. Para um **degrau**, não: chão dentro da unidade **dilui
o degrau para zero**, o que torna o resultado nulo *mais* fácil de obter, ou
seja **anti-conservador** para a conclusão «o B1 não tem degrau». E coberto
herbáceo traz variação interanual própria e grande — o `paisagem.py` deste
mesmo projecto mediu milho a −0,077. O sinal do enviesamento está trocado no
cabeçalho e a conclusão herdou-o.

**(d) O veredicto binário depende de um número mágico.** Linha 174:

```python
if a["degrau"] > 0 and b["desvio"] > -0.03:
```

O limiar de −0,03 que decide se a palavra «dois» se mantém não aparece em
nenhum cabeçalho, em nenhum pré-registo e em nenhum dos dois `.md`.

**O que sobrevive, e é honesto:** «a série Sentinel-2 do B1 não replica o
degrau», como afirmação descritiva de um instrumento único, acompanhada do
desnível de nível (0,56–0,69 contra 0,82–0,88) e da lista dos instrumentos que
lá nunca foram. **Não** como «o comparador mais próximo que o caso tem».

**A favor do B1, e digo-o com a mesma clareza:** a proveniência da máscara é
das coisas mais limpas do dossiê. `b1_serie_verdadeira.py` lê os polígonos C1a
e C1b de `SAIDA_C0\controlos.geojson`, delimitados na ortofoto por uma sessão
que nunca viu NDVI, e a localização vem de **duas coordenadas dadas pelo
gestor** — testemunho directo, tipo 1. É o oposto exacto do defeito que
originou a cadeia. O problema do S9 não é onde o B1 está: é o que se lhe
pendurou em cima.

---

### R5 · **S3: sai a palavra «replica» e saem as grandezas. Ficam direcção e datação.**

O cabeçalho de `landsat_independente.py` diz:

> «O preco: 30 m em vez de 10. O foco ESTE com pergola tem 1,27 ha, ou seja 14
> pixeis Landsat. Poucos. **Por isso so se usam pixeis inteiramente dentro da
> unidade, e reporta-se o n.**»

O código não contém filtro nenhum. Faz `reproject(..., RS.nearest)` para a
grelha de 10 m — cada píxel Landsat de 30 m passa a nove células — e depois
`np.median(ndvi[m])` sobre a máscara de 10 m. O `n` não é impresso em lado
nenhum do ficheiro. **É a mesma classe de defeito que o `fazer_masks_v2.py`:
cabeçalho a afirmar uma protecção que o código a seguir não tem.**

O T4 apanhou a discrepância e contou os blocos — 27 píxeis no foco oriental,
**2 inteiramente dentro** — mas **não reestimou nada**. O S3 continua a levar o
número produzido pelo estimador que o seu próprio cabeçalho renega. Contar a
margem não é corrigir o viés.

E há uma consequência que o T4 não tirou: **as unidades não são disjuntas a 30
m.** A mesma célula Landsat alimenta «ESTE com pergola» (27 blocos) e «resto do
pomar» (334 blocos), porque a disjunção foi imposta a 10 m. **O tratamento e o
seu próprio controlo partilham píxeis.** Num contraste isso atenua; num
«controlo que é a peça central do teste», como o cabeçalho lhe chama, isso
descaracteriza-o.

Acresce, e não está declarado em lado nenhum: **as cenas são aceites ou
rejeitadas por valores do sinal.**

```python
if v.size < 0.5 * m.sum(): ok = False
...
if ok and 0.2 < linha["referencia"] < 1.0:
```

Uma regra de aceitação de cena que lê o NDVI da referência é da mesma família
que uma máscara que lê o NDVI. Provavelmente é inócua — provavelmente só
apanha nuvem — mas «provavelmente» é o que esta cadeia decidiu não aceitar.

**Fica de S3:** o Landsat, sendo outra agência, outro sensor e outra cadeia de
correcção, sustenta que **houve uma queda, nestes sítios, entre 2013-2024 e
2025-2026, e não no controlo**. Direcção e datação. **Sai:** −0,1128 e −0,0791
como grandezas, e a palavra «replica», que sugere concordância de magnitude
entre duas medições que a própria camada diz não serem comparáveis em escala.

E fica dito: o Landsat é **radiómetro independente sobre selecção dependente**.
As unidades vêm de `discos_dos_focos()`, cujos centros saíram do sinal
Sentinel-2 — o ocidental explicitamente. Responde a «a queda está nestes
píxeis?». Não responde a «eram estes os píxeis certos?».

---

### R6 · **S1b: saem os números absolutos. Fica a invariância de sinal e ordenação.**

O próprio certificado, em CORRIGIDO, decide que «a magnitude absoluta deixa de
passar sozinha», porque até −0,025 do −0,1288 pode ser efeito de cena. E depois
o S1b sobe com as amplitudes em **nível absoluto** (ORIENTAL −0,1274 a −0,0351;
OCIDENTAL −0,1872 a −0,0542). Esses números carregam a componente de plataforma
que o S1 acabou de recusar, sem a subtrair. Ou sobem como contrastes ou não
sobem.

Duas notas sobre as 43 corridas, ambas verificadas no código:

**O desenho descrito não é o desenho corrido.** O certificado escreve «5
unidades × 3 raios × 5 limiares», o que dá 75 e não 43. O `multiverso_degrau.py`
constrói **nove definições de unidade** (3 discos + Zona 0 + IFAP no oriental;
3 discos + IFAP no ocidental) × 5 limiares = 45, menos 2 que caem por
`m.sum() < 8`, = 43. Aritmética diferente, conclusão igual — mas uma camada que
declara o seu espaço de análise tem de o declarar como ele é.

**O eixo com mais alavanca é o único que ficou fixo.** As 43 variam raio e
limiar de altura. Não variam: o conjunto de cenas, a origem das máscaras, a
fonte de altura, nem o corte em 2025. O `DATAS` é um literal **copiado à mão em
pelo menos sete ficheiros**, sempre igual, sempre sem 2019. E o V10 desta mesma
camada diz que as duas cenas mais baixas da série são as duas únicas do S2C —
ou seja, a variável de tratamento (`d >= "2025"`) é **colinear com a variável
de plataforma** em todas as 43. Chamar-lhe multiverso quando o eixo que decide
o resultado está congelado é generoso. O certificado tem razão em dizer
«invariância, não replicação independente»; a frase certa é ainda mais estreita:
**invariância a duas escolhas de geometria, medida com um conjunto de cenas
nunca posto em causa.**

---

## 2 · Factos a manter, com margem maior

### M1 · S1 (o contraste) — mantém-se. É a moeda certa. Mas o controlo não está identificado.

A decisão de passar o contraste em vez da magnitude é a melhor decisão do
documento, e o raciocínio é correcto.

O que está optimista é a margem. O controlo −0,0136 que produz os −0,1152 /
−0,1100 vem de `degrau_vs_recta_pergola.py`, linha 78:

```python
RESTO = POMAR & COM & ~disco((530485.0, 4655053.0)) & ~disco((530977.0, 4655117.0)) & ~REF
```

**A `ZONA0` não é excluída.** A parte do polígono oriental que caia fora do
disco de 90 m centrado em (530977, 4655117) está **dentro do controlo** — e o
polígono oriental é a unidade que mais desce no dossiê. É por isso que este
controlo lê −0,0136 e o do `multiverso_degrau.py`, que exclui discos de 120 m
*e* a Zona 0, lê −0,0017.

A nota 1 do §6 chama a esta escolha «o mais conservador». O nome exacto é **o
mais contaminado** — conservador apenas porque, aqui, contaminação e
conservadorismo apontam ao mesmo lado. Não é a mesma coisa, porque um controlo
contaminado deixa de servir para o que um controlo serve: dizer o que faz uma
unidade sem tratamento.

**Margem a declarar:** o contraste vive entre −0,1152 e −0,1271 (ocidental) e
entre −0,1100 e −0,1219 (oriental), conforme a linha de controlo, **mais** o
resíduo de plataforma de ~0,02 que o próprio S1 admite. Ou seja **±0,02 a
±0,03**, não quatro casas decimais. O rácio foco/controlo, que varia de 9× a
17×, não é uma quantidade: é uma família.

### M2 · S4 (fenologia) — mantém-se. «Limite superior» não é uma propriedade geral.

O argumento é: 2025 é ano do acontecimento, logo o declive intra-anual medido é
fenologia **mais** queda, logo a correcção sobrestima a fenologia. **Isso só
vale se o declive medido for negativo.** O cabeçalho do próprio
`fenologia_por_unidade.py` cita o número que desmente a generalização: na mesma
janela a referência **desce** 0,0162 e o foco ESTE **sobe** 0,050. Para uma
unidade com declive intra-anual positivo, o mesmo raciocínio faz da correcção
um **limite inferior**.

Numericamente não muda nada — as correcções são ≤ 0,0011. Mantém-se o número.
**Sai a frase universal «é um limite superior»**, que passa a ser declarada por
unidade, com o sinal do coeficiente impresso ao lado.

Segunda margem: extrapola-se linearmente um declive de 58 dias para uma
diferença de 8,7 dias, perto da saturação, com uma cena de base a DOY 243
(2018-08-31), já no ombro descendente. A curvatura nunca foi testada. É pequeno,
mas deve ficar escrito.

### M3 · S8 (radar) — mantém-se quase como está.

É o argumento de instrumento independente mais limpo do documento: nove
Invernos de banda própria, duas órbitas, e um **mecanismo declarado** para o
motivo pelo qual o foco oriental é ilegível. Não encontrei como o atacar com o
que me foi dado.

Uma correcção de redacção: o próprio NÃO TESTÁVEL diz que a unidade certificada
do radar é o disco inteiro, com a metade sem pérgola lá dentro. A forma honesta
de S8 é «o radar distingue o **disco** ocidental e não o **disco** oriental» —
uma afirmação sobre discos, não sobre focos.

### M4 · S5, o que sobra — mantém-se a base. Não se diz quantos satélites há.

A parte que sobrevive é boa e o argumento é bem feito: a base 2017-24 normal
(0,878 · 0,872 · 0,901) é a coisa que a selecção de 2026 não podia fabricar.
Mantém-se.

Mas **os três alvos têm duas distâncias diferentes em circulação**, e nunca são
calculadas:

| | rótulo em `satelites_sem_2026.py` e `t3` | tabela do `T1_T5.md` |
|---|---|---|
| #1 | 79 m do oriental | 83 m |
| #2 | **82 m do oriental** | **112 m** |
| #3 | 143 m do ocidental | 145 m |

São **cadeias de caracteres escritas à mão**, nunca derivadas das coordenadas
que estão duas colunas ao lado. A divergência do #2 é de 30 m e é exactamente a
que decide se o #2 também está dentro do disco de 90 m. Se estiver, o T3 tem de
retirar dois alvos e não um, e **resta um único candidato a satélite**. Até
isso ser resolvido (T-c, §4), **o número de satélites não passa**.

### M5 · S2 (restaurado) — mantém-se. O T1 é o melhor trabalho do pacote.

Digo-o com clareza porque é verdade: o perfil de todos os cortes, o AICc com o
terceiro parâmetro, e sobretudo o **nulo do máximo**, em que a nula procura o
seu próprio melhor corte tal como nós, respondem à acusação pela raiz. É
estatística correcta e foi feita contra o interesse de quem a fez.

Duas margens. O nulo permuta a **ordem das cenas**, o que destrói tendência e
degrau ao mesmo tempo: para uma unidade com tendência real o teste está
enviesado a favor do «degrau», e é por isso que as unidades que sobem (resto,
B1) dão p ≈ 0,36. A hipótese nula efectiva é «nenhuma estrutura temporal», não
«tendência sem degrau». E o AICc conta a quebra como **um** parâmetro, que é a
contabilidade convencional mas generosa para uma procura discreta em seis
cortes.

---

## 3 · A pergunta que falta (transversal B)

O erro que abriu esta cadeia não foi um cálculo. Foi uma pergunta que ninguém
fez: *onde fica o pomar*. Procurei a pergunta equivalente aqui, e ela não está
escondida — está escrita, em três sítios, e nunca foi junta.

> ### **O foco oriental é copado em declínio, ou é copado que foi arrancado e re-armado — e o que é que a máscara de pérgola de Julho de 2025 está, afinal, a seleccionar?**

Os três factos, todos já dentro da cadeia:

**1. A `zona0` era chão lavrado a meio da série.** `REDERIVACAO_MASCARAS.md`
§3.4, documento da C0 de herança obrigatória:

> «**41,4 % da área da `zona0` é chão lavrado na ortofoto DGT de 2021**, a 25
> cm, a meio da série Sentinel. O talhão principal mede **1,04 ha** e ocupa
> E530920–531050 / N4655030–4655190, isto é, **o centro da `zona0`**. Na
> ortofoto de 2025 esse mesmo talhão tem fiadas cobertas. […] Não consegui
> datar o acontecimento nem estabelecer se houve arranque.»

**2. O teste que separa as duas hipóteses foi marcado como condição de arranque
e nunca correu.** `PROTOCOLO.md`, tabela de estado:

> «**condição de arranque não cumprida, e nunca registada** — o T3 do
> adversário da C2, prominência de pérgola sobre a ortofoto de 2025, era
> condição de arranque da C3 e **não correu**. É o teste que distingue copado
> em declínio de copado arrancado ou re-armado.»

O certificado R2 não o menciona. O seu NÃO TESTÁVEL tem quatro entradas e
nenhuma é esta.

**3. A partição que define todas as unidades foi medida dentro da janela do
acontecimento.** `COM = np.isfinite(h) & (h >= 0.5)`, sobre `chm_altura.npy`,
do voo LiDAR de **06-07-2025** — um mês antes da cena de 2025-08-14, dentro do
período que se está a medir.

**Juntando os três:** a pertença à unidade oriental é decidida por *haver copado
em Julho de 2025*, sobre um polígono que era 41 % chão nu em 2021, num bloco que
pode ter sido arrancado e re-armado, e a grandeza medida é a variação do NDVI
dessa unidade entre 2017-2024 e 2025-2026. **É um degrau medido através de um
período em que a própria cobertura do solo da unidade mudou, com a pertença
atribuída pelo estado posterior à mudança.** Condicionamento pós-tratamento, em
forma temporal.

Nada no pacote varia isto. O multiverso varia raio e limiar de altura; **a
história de ocupação do solo não é um dos seus eixos**, e não pode ser, porque
a única fonte de altura é uma data.

Porque é que esta é *a* pergunta e não mais um reparo: a C3 e a C4 estão a
construir etiologia — nemátodos, subsuperfície, propagação — sobre um degrau
que, pelo menos no foco oriental, tem uma explicação alternativa inteiramente
banal já documentada pela camada de baixo. **O certificado não consegue
distinguir um copado em declínio de um copado substituído, e em nenhum ponto
diz que não consegue.** Isso é uma lacuna de tipo diferente de uma margem
optimista: é a mesma forma do erro do «B1» — uma unidade que se assume ser o
que o nome diz.

**Segunda pergunta que falta, menor mas da mesma família: quem escolheu as nove
datas?** `DATAS` é um literal copiado à mão em sete ficheiros, 2019 nunca lá
está, e o `PROTOCOLO.md` regista a reposição da cena de 2019-09-02 como
**condição 1 do adversário da C2, por re-certificar na C0**, com «a V11 depende
inteiramente dela». Sete cenas de base; uma oitava mudaria tudo o que se
segue. O T2 faz a pergunta certa para o intervalo de onze meses — e é a coisa
mais valiosa dos cinco testes — mas a versão geral, *qual foi a regra de
selecção da série toda e porque é que as duas cenas mais baixas são as duas
únicas do S2C*, nunca é feita.

---

## 4 · Os cinco testes de cinco minutos, por ordem de valor

### T-a · δ é uma constante? (2 min) — decide S6, e com ele o §0
Calcular `média(ref_limpa) − média(ref_antiga)` sobre as nove cenas e comparar
com as cinco `variacao` de `t5_referencia_reconstruida.json`. Se as cinco forem
iguais a δ até à última casa, o T5 é uma identidade e a promoção de S6 a
medição cai. **E abrir o §4.4 do `REDERIVACAO_MASCARAS.md`**, que o §3.2 diz
conter a quantificação do mesmo efeito, feita pela C0 antes. Dois ficheiros,
nenhum cálculo novo.

### T-b · quantos centros orientais existem? (3 min) — toca S1, S1b, S3, S4
Imprimir lado a lado:

| origem | valor |
|---|---|
| `multiverso`, `halo`, `satelites`, `t3`, `t5` | `EE[ZONA0].mean(), NN[ZONA0].mean()` — calculado |
| `fenologia_por_unidade.py`, `emparelhar_moedas.py` | `(530999, 4655102)` |
| **`PRE_REGISTO_REFERENCIA.md` §2** | **`E530999 / N4655102`** |
| `t4_n_landsat.py`, `degrau_vs_recta_pergola.py` | `(530977, 4655117)` |
| `landsat_independente.py` | `c2_00_comum.FOCO_ESTE` — por inspeccionar |

Os dois literais distam 27 m. A convenção de canto/centro do `c2_00_comum`
explica 5 m, não 27. Três consequências se divergirem: (i) **o T5 não implementou
o seu próprio pré-registo assinado**, porque a regra dos 120 m é definida sobre
coordenadas nomeadas e ele usou um centróide recalculado; (ii) o T4 não contou
as unidades que o `landsat_independente.py` usou, apesar de dizer «as unidades
tal como `landsat_independente.py` as define»; (iii) números citados lado a lado
vêm de unidades diferentes. **Nenhum destes ficheiros afirma, em lado nenhum,
que os centros coincidem.**

### T-c · o satélite #2 está dentro do disco? (2 min) — decide quantos satélites há
Calcular a distância das três coordenadas de `SAT` a `C_OR` e `C_OC`. Rótulos
dizem 79 / 82 / 143 m; o `T1_T5.md` diz 83 / 112 / 145 m. Se o #2 estiver a 82
m, está dentro do disco de 90 m como o #1, e sobra **um** candidato.

### T-d · «com pérgola» quer dizer pérgola? (5 min)
`altura_copado.py` justifica **1,5 m** como o limiar que «fica abaixo da pergola
e acima de qualquer coberto herbaceo». Todas as unidades da C2 usam **0,5 m** —
um terço disso, ao alcance de silvado e rebentação. O multiverso sugere
invariância entre 0,3 e 2,0, mas **os números de cabeçalho (−0,1236, −0,1288, e
o controlo −0,0136) não vêm do multiverso**: vêm do
`degrau_vs_recta_pergola.py`, que tem 0,5 escrito à mão e nenhuma alternativa.
Correr esse ficheiro a 1,5. E confirmar se `chm_altura.npy` é altura em metros
ou a **fracção acima de 1,5 m** que o cabeçalho descreve — existe um
`chm_frac_alto.npy` ao lado, e os dois nomes descrevem grandezas diferentes.

### T-e · olhar para a ortofoto de 2021 sobre a unidade oriental (5 min)
Não é análise: é uma vista. A C0 já renderizou `v13_zona0_epocas.png`. Marcar
quais das células de `ZONA0 & COM` caem dentro do 1,04 ha que estava lavrado em
2021 (E530920–531050 / N4655030–4655190). Se for fracção material, o degrau
oriental não é uma medição de declínio e as metades orientais de S1, S2 e S3
têm de ser reescritas. É o primeiro passo, e o mais barato, da pergunta do §3.

**Bónus, 1 minuto.** A tabela do T2 lista «07-02 (×2)», «08-16 (×2)», «08-26
(×2)»: são **oito datas distintas**, não onze — os pares são tiles vizinhos da
mesma passagem. E `eo:cloud_cover` é nebulosidade **de cena sobre o tile**, não
sobre os 2 km da AOI: uma cena a 18 % pode estar toda coberta por cima do pomar.
«Onze cenas por olhar» é um limite superior, e a frase «agora sabe-se que não é
por falta de dados» ainda não está estabelecida. Isto não enfraquece o T2 — a
lacuna existe e é real —, mas o inventário tem de ir com estas duas ressalvas.

---

## 5 · As transversais A, C e D

*(A transversal B é o §3.)*

### A · A regra do instrumento independente foi cumprida?

**Não, e a coluna que diz que sim é a mais optimista do documento.** Nas sete
linhas do CONFIRMADO, a coluna «instrumento independente» contém:

| conteúdo declarado | é um instrumento? |
|---|---|
| «—» (duas vezes) | honesto, sim |
| «a partição vem do LiDAR (G38), não do NDVI» | **sim**, com reserva grave (abaixo) |
| «USGS/NASA, OLI, LaSRC, outra órbita» | **sim**, com reserva (R5) |
| «reproduz o número que o adversário desta camada mediu na referência» | não. É uma coincidência entre dois cálculos sobre o mesmo raster |
| «a base normal e o ano de 2025 são as duas coisas que a selecção não podia fabricar» | não. É um **argumento**, e é bom — mas argumento não é instrumento |
| «é reprodução independente do resultado central da C2» | **não, e é exactamente o que o Controlo 1 proíbe**: «Um valor de NDVI não se confirma com outro cálculo de NDVI» |

**Dois instrumentos reais em sete linhas.** E os dois são mais fracos do que
declarados:

**O LiDAR.** É genuinamente outra física — geometria contra reflectância — e é
o melhor controlo do dossiê. Mas (i) o voo é de **06-07-2025, dentro da janela
do acontecimento**, o que faz da partição uma variável **pós-tratamento** da
unidade cujo degrau se está a medir: é independente do NDVI, não é independente
do acontecimento; e (ii) havia uma **paragem de linha em vigor** — o
`ADVERSARIO_2026-08-29.md`, citado no cabeçalho do `l1_data_do_voo.py`: «**Não
passa nada que dependa de L1 enquanto L1 não tiver o cálculo em disco.**» O
cálculo passou a existir em **01-09-2026**, depois do certificado e depois dos
cinco testes. Todo o pacote foi escrito sob uma paragem de linha activa, e
nenhum dos dois `.md` a menciona.

**O Landsat.** Radiómetro independente, selecção dependente, estimador que o
próprio cabeçalho renega (R5).

**Consequência:** S1, S1b, S2, S6, S7 e S9 — **seis dos nove** — não têm
instrumento independente nenhum. Pela letra do `CONTROLOS.md` §1 iriam todos
para NÃO TESTÁVEL. Não peço isso, porque S1 e S2 são bem feitos e a saída
honesta é declarar a ausência e não fingi-la resolvida. **Peço que a lista
fechada passe a levar, por facto, a palavra «sem instrumento independente» onde
for o caso.** Um leitor da C3 tem direito a saber que a maioria do que recebe
foi verificada só por dentro.

### C · Alguma coisa entrou pela porta do lado?

**Quatro coisas.**

1. **S1b sobe com magnitudes absolutas** três parágrafos depois de o CORRIGIDO
   do mesmo documento decidir que «a magnitude absoluta deixa de passar
   sozinha». (R6)

2. **O T5 cita o declive como taxa** na frase que levanta a paragem de linha —
   «os focos abrem o fosso a +0,012 a +0,014/ano, o resto do pomar fecha-o a
   −0,005, e o B1 fecha-o a −0,020» — quando o CORRIGIDO do certificado, três
   dias antes, decidira: «**O declive não se cita como taxa.**» A proibição foi
   violada precisamente na conclusão que precisava dela para soar coerente.

3. **O «facto novo» do §0 veio da prosa da camada de baixo**, não de uma
   medição nova, e foi apresentado como novo para justificar rejeitar o
   adversário. (R1)

4. **A condição 1 do adversário da C2 — a reposição da cena de 2019-09-02 —
   está por cumprir e não é mencionada.** Está registada no `PROTOCOLO.md` como
   «por re-certificar na C0», com «a V11 depende inteiramente dela». Sete cenas
   de base, uma em falta, e sete ficheiros com o mesmo literal copiado à mão.

Não encontrei nada no PASSA PARA CIMA que a secção REJEITADO devesse ter
matado. O REJEITADO está bem construído — em particular a rejeição da
«convergência» entre as duas moedas é um bom pedaço de disciplina, e a
verificação algébrica que a sustenta, apesar de ser uma identidade, é o uso
correcto de uma identidade: apanhar erro de código.

### D · As quantidades-âncora batem certo?

**O §4b é a melhor parte do certificado.** Reporta os valores obtidos, assinala
as divergências, e recusa-se a corrigir a tabela declarada em silêncio, como o
controlo manda. A inversão de sinal da referência (0,838→0,886 declarado contra
0,888→0,843 obtido) é o Controlo 2 a funcionar exactamente como foi desenhado:
a divergência saltou sem ninguém comparar nada à mão.

**Duas divergências que faltam.**

**A primeira, e é um achado.** O declive do défice da `zona0` tem, neste
momento, **cinco valores publicados em três documentos, e nenhuma tabela de
reconciliação**:

| valor | p | origem |
|---|---|---|
| +0,01307/ano | 0,0206 | `REDERIVACAO_MASCARAS.md` §4, máscaras antigas |
| **+0,00556/ano** | **0,3399** | **`REDERIVACAO_MASCARAS.md` §4, máscaras geográficas — «−57 % e perde a significância»** |
| +0,01103/ano | 0,0162 | «o degrau publicado», citado no CORRIGIDO |
| +0,00884/ano | 0,0294 | CORRIGIDO do certificado R2, restrito a pérgola |
| +0,01427/ano | — | T5, «Zona 0 sem nu2021 (o publicado)», referência limpa |

O segundo — o único em que o défice **perde a significância**, e que é da
camada de baixo — **não é citado em lado nenhum da C2 R2**. As unidades e as
referências diferem entre linhas, e é por isso que uma tabela de reconciliação
é obrigatória e não opcional: sem ela, cada peça pode escolher a sua.

**A segunda.** A tabela de âncoras não tem entrada para o **centro do foco
oriental**, que como o T-b mostra tem pelo menos três valores em circulação,
sendo um deles o que um pré-registo assinado nomeia. Deve passar a ter.

---

## 6 · Veredicto

> ## **SEGUE COM AS RETIRADAS — e com uma reposição obrigatória.**

**Retiram-se do PASSA PARA CIMA:** S6 (inteiro), S7 (o p do anel; e a afirmação
de ausência passa a NÃO TESTÁVEL), S9 (inteiro), as magnitudes absolutas de
S1b, e as grandezas e a palavra «replica» de S3.

**Mantêm-se com margem alargada:** S1 (±0,02–0,03, e o controlo declarado como
contaminado e não como conservador), S2 (com o nulo descrito pelo que é), S3
(direcção e datação), S4 (com o sinal do coeficiente por unidade), S5 (a base
normal; o número de satélites não passa até T-c), S8 (sobre discos, não sobre
focos).

**Reposição obrigatória, e é o que impede isto de ser um «segue» simples.** A
paragem de linha do §0 e a rejeição da decisão do adversário sobre a moeda
foram fundadas em novidade que não existe: o `REDERIVACAO_MASCARAS.md` §3.2 da
C0 já continha a contaminação, os mesmos cinco pontos na `zona0`, a mesma
conclusão de conservadorismo, e uma quantificação em §4.4. Pelo corolário da
regra 1, **ganha o adversário**. A decisão dele tem de ser reposta, ou rejeitada
com outro fundamento — mas não com aquele.

**Não mando voltar à origem, e digo porquê.** O núcleo aguenta. A passagem da
magnitude ao contraste é a decisão certa e está bem argumentada. O `T1` é
estatística correcta feita contra o interesse de quem a fez. A marcação de
proveniência no `multiverso_degrau.py` — «quatro têm fronteira independente do
NDVI e uma não», impressa em todas as saídas em vez de diluída na tabela — é
exactamente o que esta cadeia queria produzir. A cadeia de proveniência da
máscara do B1, das coordenadas do gestor aos polígonos C1a/C1b delimitados sem
NDVI, é limpa. O `T3` apanhou e corrigiu, antes de publicar, um defeito do seu
próprio nulo. E o §6 ataca-se a si próprio em três pontos, dos quais dois eu
teria encontrado de qualquer maneira. Isto é um documento escrito de boa fé,
com autocrítica real.

Acontece que também contém **um teste que não podia falhar** (T5), **um p
fabricado por reamostragem** (T3), **uma ausência afirmada a partir de um nulo
sem potência** (S7), **um facto «novo» com três dias de idade num documento de
baixo** (S6), **um comparador sem instrumento nenhum** (S9), e **um cabeçalho a
prometer um filtro que o código não tem** (Landsat) — este último exactamente da
família do `fazer_masks_v2.py`, que é o erro que este projecto escreveu na sua
própria `CLAUDE.md` para nunca mais repetir. Foi apanhado pelo adversário
anterior, foi contado pelo T4, e **nunca foi corrigido**: o S3 continua a levar
o número do estimador renegado.

**Duas condições antes de qualquer coisa subir para a C3:**

1. **Levantar formalmente a paragem de linha do L1.** O `l1_data_do_voo.py`
   correu hoje; o certificado e os cinco testes foram escritos antes dele, sob
   uma paragem que dizia «não passa nada que dependa de L1». Tudo o que passa
   depende de L1, através do `COM = h >= 0.5`. Se a data for 06-07-2025, isso
   tem de ir escrito ao lado da partição, com a palavra **pós-tratamento**.

2. **Registar a pergunta do §3 em NÃO TESTÁVEL, com o teste nomeado.** A
   prominência de pérgola sobre a ortofoto de 2025 é condição de arranque desde
   a C2 original, nunca correu, e é o que separa copado em declínio de copado
   arrancado e re-armado. Enquanto não correr, **a C3 e a C4 estão a construir
   etiologia sobre uma unidade cuja natureza não foi estabelecida** — que é,
   com outra roupa, o mesmo erro do lóbulo oeste.

**E uma nota de forma que não é de forma.** Existem duas listas fechadas com o
mesmo nome e conteúdos diferentes, com um dia de intervalo, e a operativa está
num ficheiro que **não é um certificado** — logo é, pela regra 1, a classe de
documento que a camada seguinte não pode herdar. Reemitir como
`CAMADA_2_CERTIFICADO_R3.md`, com esta lista, estas retiradas e estas margens.
Foi por causa de exactamente isto que dezasseis correcções se perderam contra
uma transportada.
