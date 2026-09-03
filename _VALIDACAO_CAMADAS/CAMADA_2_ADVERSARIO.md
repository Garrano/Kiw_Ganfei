# Camada 2 — adversário do certificado

29-08-2026. Sessão adversarial, sem acesso aos dados brutos e sem recomputação.
Lidos: `CAMADA_2_CERTIFICADO.md`, `PROTOCOLO.md`, `CONTROLOS.md`,
`CAMADA_0_REVISAO_R2.md` (+ suplemento G34–G37), `CAMADA_1_CERTIFICADO.md`, e os
catorze scripts e os JSON de `SAIDA_C2\`. Nenhuma cena foi aberta, nenhuma
ortofoto foi descarregada, nada foi recalculado. Onde precisei de um dado para
julgar, nomeio-o em vez de o ir buscar.

**Nota de abertura, para o registo ser honesto.** Esta é uma camada bem feita.
Três coisas são sérias e raras: reproduziu a pilha SAR da C1 a partir de um
descarregamento independente e bateu à terceira casa; resolveu o «conflito
conhecido» das contagens de máscara do `CONTROLOS.md` ao píxel; e construiu um
instrumento de **estrutura** (periodicidade de pérgola) depois de demonstrar,
com um negativo escrito, que o instrumento de **nível** da mesma ortofoto não
serve — o que é exactamente o que o controlo 1 pede e o que quase nunca se faz.
O ataque que se segue é forte precisamente porque há material para atacar.

O achado principal desta revisão **não é** nenhum dos quatro que a C2 nomeou na
sua «Nota ao adversário». É uma pergunta que a camada tinha o instrumento, a
imagem e o hábito para fazer, e não fez. Está na parte 3.

---

## 1. Factos a retirar do PASSA PARA CIMA

Quatro retiradas. Nenhuma delas apaga uma medição: em todas, o que cai é a
**frase que liga os números** — o mesmo tipo de erro que a própria C2 apanhou na
R2 G28, e a que ela própria não escapou.

---

### R1 · V4, «a válvula 8 destaca-se sozinha, **nos dois instrumentos**»

**O que teria de ser verdade para isto estar errado.** Que a ordenação das doze
válvulas pela queda de NDVI não seja informação independente — porque a válvula
8 foi identificada por conter o foco OESTE, e o foco OESTE é, por definição da
G34 e da G29, **o sítio onde o NDVI caiu**. Perguntar depois se a válvula que
contém o sítio onde o NDVI caiu é a válvula onde o NDVI mais caiu não é um
teste; é uma verificação de aritmética.

**O que o código diz.** `c2_08_cruzamento.py` corre o teste correcto e a C2 não
o publica. O Spearman entre a queda de NDVI e a anomalia de VV sobre as doze
válvulas está em `c2_08_cruzamento.json`:

```
spearman_valvulas: rho = +0.4755,  p = 0.1182
```

**ρ = +0,48 com p = 0,118.** Este é o único número da linha V4 que é uma
afirmação de dois instrumentos, e é o único que o certificado não menciona. O
que o certificado publica em vez dele — «a v8 é a primeira nas duas ordenações»
— é a coincidência de dois máximos, e um dos dois máximos é circular.

**Como se testa em cinco minutos.** Já está testado: ler a linha acima do JSON
que a própria camada escreveu.

**O que sobrevive, e deve substituir V4.** Sobre uma partição de proveniência
documental (tabela de áreas do gestor, R2 G35), a válvula que contém o foco
OESTE tem a maior anomalia negativa de VV do Inverno de 2025-26 por um factor
de cinco: **−0,660 dB contra −0,135 dB da segunda**. Isso é sólido, é
espectacular, e é **um** instrumento. É a C1 S15 medida sobre outro recorte do
mesmo terreno com o mesmo radar. A partição é independente; a **grandeza** não
é. Tem de passar para cima assim, sem «nos dois instrumentos» e sem «é o teste
que a C1 pediu em S15, e passa».

**Se cair, o que cai com ele.** V4 é hoje o pilar de independência de V2 do lado
ocidental, ao lado de V3. V3 aguenta o peso sozinha; V4 corrigida acrescenta
localização, não instrumento. Nada mais cai.

---

### R2 · V3, a frase «retirando os 25 mosaicos a menos de 130 m dos dois focos, sobrevive»

O corpo de V3 é o melhor trabalho da camada e não está em causa. Está em causa
**a última frase**, que é justamente a que o prompt desta sessão identifica como
aquela em que a verificação mais forte do caso agora assenta.

**O que teria de ser verdade para isto estar errado.** Duas premissas, e as duas
são falsas na leitura literal do código.

*Premissa 1: «a mais de 130 m dos dois centros» = «sem os focos».* O filtro em
`c2_09_sar_verificacao.py` compara o **centróide** de cada mosaico de 60 m com
as **duas coordenadas** dos focos. Um mosaico de 60 m tem meia-diagonal de 42 m:
um mosaico cujo centróide está a 131 m do foco pode conter células a **89 m** do
centro — dentro do disco de 90 m que a C1 usa para definir o foco. Mais grave:
a própria V8 põe **1,41 ha de declínio novo em três manchas a 62, 72 e 167 m do
foco ESTE**. A mancha dos 167 m **sobrevive ao filtro**. O teste não retira o
acontecimento; retira duas coordenadas e deixa lá parte da mancha que o
acontecimento produziu. A afirmação defensável é «a correlação não é obra dos
25 mosaicos centrais», que é bastante mais fraca do que «o lugar já não é
circular».

*Premissa 2: p = 0,0010 é comparável ao p < 0,0002 da linha anterior.* Não é. O
p da linha principal é de **permutação** (5000 reatribuições) — a camada usou
permutação precisamente porque não confiava no p assintótico sobre 81 mosaicos
espacialmente autocorrelacionados. O p = 0,0010 da linha de sobrevivência é o
**p assintótico do `scipy.stats.spearmanr`**, calculado sobre n = 56, e a
permutação não foi repetida para o subconjunto. E o valor observado é
desconfortável: **ρ = +0,429 com n = 56, contra um máximo do nulo de +0,426 com
n = 81**. Com menos unidades o nulo alarga. O número de sobrevivência cai, tal
como está, praticamente em cima do máximo do nulo do teste maior.

**Como se testa em cinco minutos.** Correr a mesma permutação de 5000
reatribuições sobre o subconjunto de 56, com a pilha que já está em disco. E
definir «sem focos» pelo **mapa de défice de 2026** (`c2_05_defice_2026.npy`,
também em disco), não pela distância a dois pontos.

**Se cair, o que cai com ele.** Nada de V3 cai — o corpo (ρ = +0,57 a +0,60,
especificidade temporal ao Inverno de 2025-26, três placebos, duas órbitas em
separado) aguenta-se sem esta linha. Cai a **conclusão** que a C2 tira dela e
que herda da pergunta em aberto da C1: que «o lugar já não é circular». Isso
ainda não está estabelecido. Deve ir para NÃO TESTÁVEL até a permutação ser
refeita.

**E há um segundo item por declarar em V3.** A tabela de especificidade em
`c2_09_sar_verificacao.json` mostra que o Inverno de **2016-17** dá, com o par
do evento, **ρ = +0,314 com p = 0,0043** (81 mosaicos) e **ρ = +0,713 com
p = 0,0092** (12 válvulas). O certificado escreve «nos nove Invernos anteriores,
ρ vai de −0,22 a +0,31», o que arruma um resultado significativo dentro de um
intervalo apresentado como ruído. A margem de especificidade continua grande
(+0,60 contra +0,31) e V3 aguenta; mas o Inverno mais antigo da série
correlacionar significativamente com a queda de 2024→2026 é um sinal de
componente estrutural permanente, e o próprio docstring do `c2_08` diz que é
esse o resultado que mataria o cruzamento. Tem de ficar escrito.

---

### R3 · V2, os números **−0,1426** e **−0,1439** e a margem «±0,01 NDVI»

**O que teria de ser verdade para isto estar errado.** Que um degrau medido com
**duas** cenas depois da quebra tenha uma margem de ±0,01, e que o nível
absoluto de NDVI possa carregar a afirmação. As duas coisas são negadas por
outros ficheiros da mesma camada.

**O que o código diz, e o certificado não.** `c2_06_este.json` guarda o teste de
Welch que compara as oito cenas do patamar com as duas do degrau:

```
FOCO OESTE disco r=90            degrau -0.1426   p_degrau = 0.1935
FOCO ESTE plantado (zona0-nu21)  degrau -0.1439   p_degrau = 0.1364
referencia sistematica           degrau -0.0501   p_degrau = 0.0726
pomar sem os dois discos         degrau -0.0204   p_degrau = 0.1341
```

O certificado publica o rácio de somas de quadrados (4,35 : 1 e 4,05 : 1) e a
margem «±0,01 NDVI». O rácio de SQR é descritivo e não tem conteúdo
inferencial; o p do teste que a camada correu **existe, está gravado, e não
aparece em lado nenhum do certificado**. Isto é o modo de falha que este
processo já conhece: a prosa e o código a dizerem coisas diferentes.

Em defesa da C2: com n = 2 depois da quebra, nenhum t-test pode dar
significância, e a estatística correcta estava disponível e é melhor — as duas
cenas do degrau são os **dois valores mais baixos de dez**, o que dá um teste de
ordenação exacto com p = 1/45 = **0,022**. A camada reportou o número errado e
escondeu o segundo pior, tendo o melhor à mão.

**Só que esse teste de ordenação não separa o degrau da cena.** As duas cenas
mais baixas da série são as duas únicas do **S2C** — é a própria V10 que o
estabelece, e a referência sistemática dá o mesmo padrão de ordenação com um
degrau de −0,0501. O que separa os focos da cena não é a ordenação: é a
**magnitude contra o controlo interno**. E aí o certificado dá os números certos
lado a lado mas na moeda errada.

**A moeda certa é a que a própria V1 fixa** — fosso à referência da mesma data.
`c2_06_este.json`, secção `fosso`:

```
FOCO OESTE   ... 2024: 0,008  2025: 0,061  2026: 0,136   subida de 0,128
FOCO ESTE pl ... 2024: 0,038  2025: 0,107  2026: 0,156   subida de 0,118
pomar s/discos . 2024: 0,020  2025: 0,011  2026: 0,005   fecha, não abre
```

O facto sobrevive inteiro e continua notável — os dois focos abrem o fosso
0,128 e 0,118 enquanto o resto do pomar o **fecha**. Mas os números que passam
para cima têm de ser **0,128 e 0,118 no fosso**, não −0,1426 e −0,1439 em nível
absoluto, e a margem tem de ser a amplitude do patamar de cada unidade (OESTE:
−0,002 a 0,030; ESTE plantado: 0,017 a 0,066), não «±0,01».

**Se cair, o que cai com ele.** V2 é o facto de que mais coisas dependem: V3
data-o, V4 localiza-o, V8 quantifica-o, e a C3 inteira vai ser escrita contra
ele. Não cai — mas passa para cima com ~15 % menos magnitude, com uma margem
três a cinco vezes maior, e sem poder ser citado em nível absoluto.

---

### R4 · V5, o número **IoU = 0,29** (retira-se o número, mantém-se o facto)

**O que teria de ser verdade para isto estar errado.** Que 0,29 seja baixo *para
esta métrica*. Não há nenhum nulo declarado. A matriz completa está em
`c2_03_defice.json` e a própria camada a imprimiu:

```
IoU(2017, 2026) = 0,29      <- apresentado como prova de que são objectos diferentes
IoU(2024, 2026) = 0,36
IoU(2021, 2026) = 0,34
IoU(2018, 2026) = 0,24
IoU(2020, 2026) = 0,31
```

O défice de 2026 sobrepõe-se a **todos** os anos anteriores com IoU entre 0,24 e
0,37, incluindo os anos do patamar cujo défice ninguém contesta ser a mesma
coisa a persistir. 0,29 não é o valor de «objectos diferentes»: é o valor que
esta métrica devolve para «anos afastados». O número não distingue nada e deve
sair.

**O que sobrevive de V5, e é forte.** Sobram duas pernas e chegam: (a) o rácio
de profundidade — ao limiar 0,25, 5,37 ha em 2017 contra **0,32 ha** em 2026, e
ao 0,30, 4,91 contra 0,11; (b) a pérgola de V6. A caracterização «extenso e
moderado» é o achado utilizável e não depende do IoU.

**Se cair, o que cai com ele.** Só o número. V5 fica com duas pernas em vez de
três, o que é honesto: apresentar três provas quando duas são a mesma medição
com nomes diferentes é o que o controlo 1 existe para impedir.

---

## 2. Factos a manter, com margem maior

### W1 · V6 e a retirada dos «8 ha» — **a retirada é sólida**. Diga-se com clareza.

O prompt pede um juízo sobre isto. O juízo é: **sim, a retirada aguenta**, e
aguenta por uma razão que resiste à minha primeira objecção.

A minha primeira objecção era que a prominência colapsa entre épocas — a
referência, que tem pérgola de certeza, dá 0,253 em 2010, 0,220 em 2012 e
**0,045** em 2021, um factor de cinco. Se o instrumento se apaga, o «p = 0,11,
indistinguível» de 2021 seria um não-resultado lido como positivo. Mas
`c2_12_pergola.json` mata a objecção: em 2021 o instrumento **ainda separa**,
com U1 significativamente **acima** do resto do pomar (p = 7,7e-08). E o
argumento nunca compara magnitudes entre épocas — compara, dentro de cada
imagem, U1 contra U2 e U3. Dentro de 2010: U1 = −0,024, U3 = +0,204. Dentro de
2021: U1 = +0,043, U2 = +0,045, U3 = +0,023. A inversão qualitativa é real e é
imune ao desequilíbrio do JPEG, tal como a C2 diz e ao contrário do que a
radiometria da mesma ortofoto faz (`c2_13`, correctamente registado como
negativo). **A retirada da curva em U como objecto único está bem fundada.**

**O que o resto do caso ainda encosta ao facto retirado.** Duas coisas, e são
menores. A R2 G11 lia os ~8 ha de 2017 como «copado a fechar» e a C2 confirma-a
— logo G11 não cai, muda de estatuto de leitura para medição. E a C1 S13/S14 não
toca nisto. Não encontrei nenhuma afirmação viva noutra camada que dependa de
2017 ser linha de base de saúde. A retirada é limpa.

**A margem que tem de alargar, em quatro pontos.**

1. **Não há controlo negativo nem positivo, além da própria referência.** Nunca
   se mediu a prominência sobre terreno que se saiba não ser pomar (edifício,
   estrada, milho, mata) nas mesmas imagens de 2010 e 2012. Sem isso,
   «prominência ≈ 0» significa «sem periodicidade a 5 m visível», e a passagem
   daí para «não era pomar» é inferência, não medição. A `nu2021` estava
   disponível e teria servido de controlo em 2021, e não foi usada.

2. **As 5,37 ha são a área do défice grave de 2017, não a área medida sem
   pérgola.** O mapa de prominência está gravado célula a célula
   (`c2_12_prom_2010.npy`, `_2012.npy`) e a área directa — quantas células do
   pomar têm prominência abaixo do percentil 5 da referência nas duas épocas —
   **nunca foi calculada**. V6 diz «pelo menos 5,37 ha (18 %)» e trata 5,37 como
   limite inferior; é ao contrário: 5,37 é a área de um mapa de NDVI de 2017,
   que a pérgola confirma no essencial mas não delimita.

3. **A georreferenciação de `c2_12` não está estabelecida, e diverge da de
   `c2_13` sobre os mesmos dados.** `c2_13` reprojecta correctamente
   (`reproject(..., src_crs=ds.crs, dst_crs="EPSG:32629")`). `c2_12`, no mesmo
   dia e na mesma pasta, lê uma janela pela caixa envolvente reprojectada e
   depois indexa o *array* com `cy = (y+0,5)*passo`, isto é, assume que a grelha
   de píxeis da ortofoto está alinhada e sem rotação face à grelha UTM. Isso só
   é verdade se `ds.crs` for `EPSG:32629`; se as ortofotos DGT vierem em
   `EPSG:3763`, como é habitual, há rotação de convergência de meridiano e um
   desalinhamento crescente com a distância ao centro da AOI, da ordem de uma a
   duas células nos extremos. **Dado que preciso e não vou buscar:** o CRS de
   `orto\ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif`. O viés vai no sentido de
   diluir o contraste, não de o criar — com p entre 1e-59 e 1e-213 o sentido não
   se inverte — mas a **atribuição de área e a localização** de V6 dependem
   disto.

4. **«Concentrada a E530600–530800, entre os dois focos»** não é calculada em
   nenhum script nem aparece em nenhum JSON. É prosa. E os quatro números de
   NDVI de V6 e da linha CONFIRMADO correspondente — 0,498 / 0,753 / 0,826 /
   0,780 — também não aparecem em nenhum ficheiro de saída: existem, mas só
   dentro do painel (d) de `c2_11_figuras.py`, e o certificado atribui-os a
   «`c2_03` §1», que não os calcula. A regra 3 do protocolo («um facto, uma
   prova») pede a citação certa.

**Formulação que aguenta:** *pelo menos 5,37 ha do polígono `pomar` não tinham
estrutura de fileira visível em 2010 nem em 2012, e tinham-na em 2021*. A data
de plantação continua onde a C2 a pôs, em NÃO TESTÁVEL, e faz muito bem.

---

### W2 · V8, as 3,58 ha da regra M2 — falta-lhe a taxa de base, e ela inverte a impressão

`c2_05_manchas.json` dá `sao_antes_ha = 20,97` de 30,31 ha de pomar. Com isso:

```
terreno são até 2024:        20,97 ha  ->  3,58 ha em défice em 2026  = 17,1 %
terreno com histórico:        9,34 ha  ->  4,28 ha em défice em 2026  = 45,8 %
```

O acontecimento de 2026 é **2,7 vezes mais provável sobre terreno que já tinha
estado em défice** do que sobre terreno são. O certificado apresenta as 3,58 ha
como «declínio novo sobre terreno comprovadamente são», o que é verdade e é a
área certa para procurar causa recente; mas deixa a impressão de que o evento
prefere terreno são, e a medição da própria camada diz o contrário. Para a C3 e
a C4 isto não é cosmético: é a diferença entre «apareceu algo novo» e «agravou-se
o que já lá estava».

Segundo ponto de margem: as 3,58 ha são um **limite superior**. A abertura
morfológica 2×2 é aplicada aos mapas de todos os anos, o que torna o critério
«nunca esteve em défice» mais fácil de satisfazer (uma célula isolada em défice
em 2019 é apagada e passa a contar como sã). O critério duro — **2,60 ha** — é o
número defensável e devia ser o que passa para cima, com 3,58 ao lado como
tecto.

Terceiro: V11 declara uma barra de erro de ~3 ha para a série, e V8 é construída
sobre a intersecção de **oito mapas de uma cena por ano**. A barra nunca é
propagada. Ou ela se aplica — e então «nunca esteve em défice» é uma afirmação
com ruído por célula — ou V11 tem de dizer o que cobre.

---

### W3 · «De 2024 para 2026 o pomar não se deslocou: dispersou-se»

O contrafactual está bem feito e a conclusão «a deslocação explica 0 %» é
trivialmente robusta, porque a média não mexeu (−0,0292 → −0,0290). O problema é
o par de números escolhido para descrever a dispersão. A tabela completa de
`c2_03_defice.json`:

```
sd:    2017 0,1541 | 2018 0,0720 | 2019 0,0737 | 2020 0,0686 | 2021 0,1039
       2022 0,0886 | 2023 0,0715 | 2024 0,0764 | 2025 0,0861 | 2026 0,1018
```

**O sd de 2026 (0,1018) é inferior ao de 2021 (0,1039)**, num ano com 3,34 ha de
défice. O certificado cita «0,076 → 0,102» como assinatura do acontecimento e
compara só dois pontos de uma série que a própria camada imprimiu. O número que
é de facto sem precedente é a **assimetria** (−2,98 → −1,21; o mínimo histórico
da série é −1,46 em 2017, que é o outro ano anómalo). A frase tem de assentar na
assimetria e citar o sd com a série toda ao lado.

E uma segunda margem, que é maior: **o único controlo de cena que a camada
correu é sobre a média.** O `c2_04` mede o degrau do S2C no nível — na
referência, fora do pomar e num alvo de mata — e conclui, correctamente, que a
métrica de défice é imune a um degrau **uniforme**. Mas um degrau de sensor não
é uniforme em NDVI: uma diferença de bandas ou de correcção atmosférica actua de
forma diferente a 0,89 e a 0,70, e o que isso produz é exactamente um
alargamento da cauda inferior. **Nunca se mediu se o desvio-padrão e a
assimetria das células fora do pomar também mudam nas duas cenas S2C.** Todas as
grandezas-título desta camada — área em défice, dispersão, fracção, M2 — são
estatísticas de cauda, e o único controlo instrumental existente é sobre o
centro da distribuição.

---

### W4 · V10 — sólida, e feita na direcção conservadora

Registo com a mesma clareza com que ataco. Dos três alvos, a C2 escolheu para a
correcção o que dá o **menor** degrau (T2, mata estável, −0,025) em vez do que
lhe seria mais favorável (T1, −0,048). Com T1 a descida residual da referência
seria nula ou positiva. A escolha é a que menos ajuda a conclusão, e a C2 declara
por cima o viés de regressão à média da selecção de T2 e o sinal certo desse
viés. É a linha mais bem executada do certificado. Sem alteração de margem.

### W5 · V7 — o facto mais bem estabelecido da camada

166 de 167 células de `nu2021` em défice óptico em 2017, contra 27 % do pomar;
e a C1 S13 chega à mesma datação negativa por radar em todos os dez Invernos
desde 2016-17. Dois instrumentos, dois princípios físicos, a mesma conclusão
negativa. Nada a alargar.

### W6 · V1 e a tabela de âncoras — exactas, e uma contribuição real

A resolução do «conflito conhecido» do `CONTROLOS.md` (2903/454/427/220 são os
polígonos; 2906/446/423/219 são outra rasterização) é o tipo de arrumação que
este processo precisa e que ninguém tinha feito. Uma nota de higiene: o
certificado dá o centróide de Voronoi da v8 a **43 m** do foco OESTE, enquanto
a R2 G35 dá 34 m e a C1 dá 35 m para a **posição** da válvula. São objectos
diferentes e a C2 não o diz; quem alinhar âncoras entre camadas vê 34 / 35 / 43
sem explicação, que é precisamente o que o controlo 2 existe para evitar.

### W7 · Duas notas de vocabulário, que nesta cadeia já custaram caro

A palavra **«anomalia»** designa duas grandezas diferentes na mesma camada. Em
`c2_08`, na tabela das válvulas, `vv_anom = vv2526 − vv_base` — anomalia a sério,
com a linha de base de cada unidade subtraída. Em `c2_09` e em `c2_11`, a
grandeza Y do cruzamento é `vv(m, w)` = mediana de (unidade − pomar) nesse
Inverno, **sem** subtracção da história da própria unidade: é um **nível**
relativo ao pomar, não uma anomalia. O certificado chama «anomalia de VV do
Inverno de 2025-26» às duas. Isto importa: a v8 só se isola depois de subtraída
a base (em nível bruto, v8 −0,575 e v15 −0,567 estão empatadas), e o cruzamento
de V3 usa a definição que **não** subtrai a base — que é a definição em que uma
diferença estrutural permanente entra directamente na correlação, e é a
explicação natural do ρ = +0,314 do Inverno de 2016-17. A camada que herdou a
inversão da G34 não podia dar o mesmo nome a duas coisas.

Segunda: o docstring de `c2_02` diz da sonda A que mede o dia-do-ano «com tudo o
resto constante». Não mede: **2025-06-17 é S2A e 2025-08-14 é S2C**, como o
`c2_04` da mesma camada estabelece e tabela. A sonda atravessa a mudança de
satélite que a camada identificou como o maior confundente da série.

---

## 3. A pergunta que falta

*(transversal B)*

**A camada perguntou *quando* e *onde*. Nunca perguntou *o quê*.**

Vale a pena ver a forma disto, porque é a forma do erro que abriu esta cadeia. O
erro do «B1» não foi um cálculo: foi uma pergunta de identidade — *o que é este
sítio?* — que não se fez a uma camada abaixo daquela onde a inferência estava a
correr.

A C2 fez essa pergunta, e fê-la bem, **a um dos dois ramos**. Perante os 8,08 ha
de 2017 não perguntou «quanto declinou?», perguntou «aquilo era pomar?» — e para
responder construiu um instrumento de estrutura, demonstrou por escrito que o
instrumento de nível da mesma ortofoto não serve (`c2_13`), apontou o
instrumento bom a 2010, 2012 e 2021, e **reformou um título do caso**. É a
melhor página do certificado.

E depois não fez a mesma pergunta ao outro ramo.

Sobre as 3,58 ha de declínio novo de 2025-2026 — o único terreno de que a camada
diz que faz sentido perguntar por uma causa recente — não há uma única
observação de **o que lá está**. Há um degrau de NDVI de Verão, uma queda de VV
de Inverno no mesmo chão, os dois concentrados numa válvula de rega, os dois a
aparecerem nos mesmos dezoito meses. Tudo isso é igualmente compatível com:

- copado adulto em declínio fisiológico ou patológico; **e**
- copado **arrancado, replantado, cortado, ou com a pérgola desmontada** — uma
  operação de gestão.

Um copado em declínio **mantém as fileiras**. Chão arrancado, replantado ou
re-armado **não as mantém**. A camada tinha o instrumento que distingue as duas
coisas, provado dentro de uma só imagem, com p ~ 1e-200. E tinha a imagem: a
ortofoto de **2025** está aberta em `c2_13_coberto_2025.py`, no mesmo directório,
no mesmo dia. A lista `ORTOS` de `c2_12_pergola_2012.py` tem 2010, 2012 e 2021,
e **não tem 2025**. Duas linhas de código separam esta camada de uma resposta.

Não estou a afirmar que houve arranque. Estou a afirmar três coisas mais fracas
e mais incómodas: que os dados desta camada **não distinguem** as duas
hipóteses; que o certificado **não diz** que não as distingue, nem em NÃO
TESTÁVEL; e que a camada tinha o instrumento, a imagem e o hábito, e não fez a
pergunta ao ramo que declara ser o achado.

Há sinais no próprio material que tornam a pergunta obrigatória, não retórica:

- A taxa de base de W2: o défice de 2026 é 2,7 vezes mais provável sobre terreno
  com histórico. Replantação e re-armação fazem-se, tipicamente, onde já corria
  mal.
- O núcleo oriental **cresce em 2026 para dentro de copado plantado** e o seu
  teor de chão lavrado cai de 78 % para 34 % (`c2_06_este.json`). Terreno
  plantado a passar a comportar-se como chão despido é o padrão de uma
  operação, tanto quanto o de uma doença.
- A anomalia de VV do Inverno concentra-se numa válvula. Uma válvula é uma
  unidade **de gestão**, não uma unidade biológica.
- A V4 e a V8 apontam ambas para a **parcela da v8**, e a única informação
  documental que existe sobre essa parcela é uma área numa tabela. **Dado que
  preciso e não vou buscar:** o registo de operações da exploração para os
  blocos B2 e B3 em 2024, 2025 e 2026 — arranque, replantação, poda severa,
  substituição de pérgola, falha de rega, data e sector. É uma pergunta de uma
  linha ao gestor, do mesmo género da que a C2 já pede em NÃO TESTÁVEL para a
  data de plantação, e vale mais do que qualquer das quatro que ela pede.

**Porque é que isto é grave agora, e não daqui a duas camadas.** A camada
seguinte é a **C3, biologia**, e o `CAMADA_3_PROMPT.md` já está escrito. A C3 vai
georreferenciar 212 registos de laboratório contra o padrão que esta camada
certificou, e as 3,58 ha de V8 são a área onde faz sentido procurar. Se parte
dessas hectares for terreno operado, a C3 vai correlacionar patogénios com um
calendário de máquinas — e essa é a mesma classe de erro que o *P. sojae*
atribuído ao corpo em declínio, que o `CONTROLOS.md` lista como o segundo dos
três erros que custaram semanas a este processo. **O teste da ortofoto de 2025
deve correr antes da C3, não depois.**

---

## 4. Os cinco testes de cinco minutos, por valor

Ordenados por confiança ganha por esforço. Nenhum precisa de dados novos, e
quatro dos cinco correm sobre ficheiros que já estão em `SAIDA_C2\`.

**T1 · Três intersecções e um CRS.** *(três linhas; nada de novo em disco)*
`REF & do`, `REF & de`, `REF & c2_05_defice_2026.npy`, `REF & c2_05_novo_m2.npy`;
e `rasterio.open(orto2010).crs`.
As 110 células da referência sistemática são o **denominador de todas as
grandezas desta camada** — o défice, a magnitude, o fosso, o degrau, a fenologia,
os placebos. A rede é *sistemática sobre o pomar*, não escolhida por saúde: se
alguma das suas células cair dentro de um foco, ou dentro do mapa de défice de
2026, a referência contém o sinal que serve para medir, e todas as magnitudes
estão amortecidas por uma quantidade desconhecida. A camada nunca reporta esta
intersecção. O `c2_12` prova de passagem que `REF ∩ U1 = ∅` em 2017 (537 + 110 +
2384 = 3031), o que é bom sinal, mas não diz nada sobre 2026. O CRS resolve o
ponto 3 de W1. **Se algum destes quatro números não for zero, esta camada volta
para trás inteira** — e é por isso que este teste está em primeiro lugar apesar
de custar três linhas.

**T2 · Publicar quatro números que a camada já calculou.** *(zero computação)*
`p_degrau` = 0,1935 e 0,1364 (`c2_06_este.json`); `spearman_valvulas` ρ = +0,476,
p = 0,118 (`c2_08_cruzamento.json`); a taxa de base de M2 (17,1 % contra 45,8 %);
e o teste de ordenação exacto do degrau (p = 0,022). Custo nulo, e corrige as
margens de V2, V4 e V8 antes de a C3 as usar como dados.

**T3 · Apontar a pérgola de `c2_12` à ortofoto de 2025.** *(duas linhas na lista
`ORTOS`, mais quatro unidades)*
Unidades: as 3,58 ha de `c2_05_novo_m2.npy`, o disco OESTE, `zona0 & ~nu2021`, e
a referência. Comparação **dentro da imagem de 2025**, como em 2010/2012/2021.
Se a prominência das unidades em queda for indistinguível da referência, a
estrutura está lá e o acontecimento é de copado — e V2 ganha o instrumento
independente que hoje lhe falta do lado oriental. Se for como a U1 de 2010, o
que se mediu não é declínio. É a resposta à parte 3 e é o teste mais
consequente da lista.

**T4 · O cruzamento com uma anomalia a sério, e a permutação onde falta.**
*(~20 linhas; a pilha SAR já está em disco)*
Redefinir Y como `vv(u, w) − média de vv(u, ·) nos outros nove Invernos` — a
mesma definição que a tabela das válvulas já usa — e repetir a grelha dez
Invernos × quatro pares. Depois correr as 5000 permutações **sobre os 56
mosaicos** do subconjunto sem focos, e substituir o p = 0,0010 assintótico pelo
p de permutação. Resolve de uma vez o item W7 (dois significados de
«anomalia»), o ρ = +0,314 por explicar de 2016-17, e a R2 acima.

**T5 · A sonda A por unidade e por limiar.** *(um ciclo sobre o que `c2_02` já
carrega)*
A sonda A está medida só sobre a área agregada em défice e só ao limiar 0,05, e
a calibração fenológica que dela sai sustenta V11 e, por V11, toda a leitura da
série. Os dados da própria sonda mostram que o efeito é **fortemente
heterogéneo**: entre DOY 168 e 226 de 2025 a referência **desce** 0,0162
enquanto o foco ESTE **sobe** 0,050 e o p10 do pomar sobe de 0,669 para 0,713.
Um coeficiente médio aplicado a unidades com respostas de sinal contrário não é
uma calibração. Repetir por unidade (referência, dois focos, resto do pomar) e
por limiar (0,05 a 0,30) diz se as 5,37 ha de défice grave da cena mais precoce
da série (DOY 183) são em parte um efeito de dia-do-ano — o que ataca
directamente a área de V6 e o rácio de V5. Segundo ponto do mesmo teste:
declarar que a sonda A atravessa a fronteira S2A→S2C e não é «tudo o resto
constante».

---

## 5. Transversais A, C, D — em resumo

**A · A regra do instrumento independente.** De onze factos: têm instrumento
independente a sério **V3**, **V6** e **V7** (e a metade ocidental de V2 e V8,
via V3). Têm um instrumento que é **o mesmo com outro nome**: **V4** (a perna do
NDVI é a grandeza que produziu o facto), **V11** (a coluna de instrumento
independente da linha da fenologia diz «a sonda é a cena de 2025-06-17» — é o
mesmo Sentinel-2, a mesma máscara, o mesmo cálculo, noutra data), e **V1** (uma
reprodução por caminho próprio é replicação, não segundo instrumento). Não têm
nenhum, e a C2 declara-o correctamente: **V9**, **V10**, a metade oriental de
**V2** e de **V8**. Cumprimento parcial, com duas etiquetas erradas na coluna
que o controlo 1 criou de propósito.

**C · Entrou alguma coisa pela porta do lado?** Três itens.

1. **A cena de 2019-09-02 e o G10.** A R2 G10 está na secção **MANTÉM-SE sem
   alteração** e diz: «A composição fenológica da série continua sem
   justificação: **mantém-se o dia-do-ano 243 e exclui-se o 245**.» O certificado
   da C2 cita-a como «a R2 G10 certifica que a exclusão dela "continua sem
   justificação"» — deslocando o «sem justificação» da *composição* para a
   *exclusão* e deixando cair a cláusula operativa. Com essa leitura, repõe a
   cena, e declara na abertura «**Não há paragem de linha. Nenhum facto herdado
   da R2 ou da C1 foi rejeitado.**» As duas coisas não podem ser verdade ao mesmo
   tempo. E o certificado contradiz-se no mesmo parágrafo: escreve «nenhum
   [resultado] depende da escolha» e, três linhas abaixo, «a cena de 2019 é o que
   fixa a barra de erro de toda a série (ver V11)». **V11 depende inteiramente de
   uma cena que a camada de baixo mandou excluir.** No mérito, a reposição
   parece-me certa — dois dias de dia-do-ano não justificam excluir um ano. No
   procedimento, é uma alteração de facto certificado sem paragem de linha.
2. **A localização de V6** («E530600–530800, entre os dois focos») e os quatro
   valores de NDVI de W1.4 não têm ficheiro. Prosa onde devia haver cálculo.
3. **Uma coisa saiu pela porta do lado.** A secção C do `c2_05_manchas.py` —
   frente em avanço contra núcleos difusos — foi corrida, deu um resultado nulo
   (as células novas de 2025 e 2026 aparecem a mediana de 20–22 m das antigas,
   indistinguível dos anos do patamar: 22,4 m em 2019→2020, 52,4 m em
   2023→2024), e **não aparece em nenhuma das cinco secções do certificado**,
   nem sequer em NÃO TESTÁVEL. A regra 4 do protocolo diz que a dúvida é
   resultado; um teste corrido que não distinguiu nada também é.

**D · As quantidades-âncora batem.** Todas reconciliam, e as duas divergências
estão explicadas exactamente como a C1 as explicou (44,96 contra 44,93; as duas
referências como objectos diferentes). A única linha que não é uma medição mas
uma decisão é «cenas de plena estação: 9 declaradas → 10 defensáveis», e é o
item C.1 acima. A disciplina de âncoras desta camada é boa; a nota de higiene
sobre os 34 / 35 / 43 m da v8 está em W6.

**Sobre a «Nota ao adversário» da C2.** Três dos quatro pontos são reais e estão
subestimados, e o quarto é o menor dos quatro. (1) O lado oriental de V2 é pior
do que declarado: a partição cega da própria camada, as válvulas, dá ΔNDVI
2024→2026 de **+0,0043 (v13)** e **−0,0027 (v14)** — as duas válvulas mais
próximas do foco ESTE — contra −0,0822 na v8. A camada construiu uma partição
independente, aplicou-a ao lado ocidental, e não a aplicou ao lado que ela
própria diz não ter instrumento. (2) A consequência do polígono de 2021 é maior
do que a declarada, porque a **referência sistemática** vem da mesma derivação
e da mesma época: não é só a percentagem do pomar nas cenas antigas que fica
mal definida, é o denominador de tudo. (3) A escolha do par de anos está
correctamente identificada, e o item por declarar é o ρ = +0,314 (p = 0,0043) do
Inverno de 2016-17, não os placebos. (4) O viés de selecção do T2 está
correctamente identificado, correctamente assinado, e é conservador — é o ponto
menos importante dos quatro e o mais fácil de defender. Quem declara os seus
pontos fracos tende a declarar melhor os que já sabe resolver.

---

## Veredicto

**SEGUE PARA A CAMADA 3 COM AS RETIRADAS INDICADAS**, e com duas condições que
não são retiradas.

*Retiradas (parte 1):* R1 reescreve V4 como resultado de um instrumento sobre
uma partição independente; R2 manda a última frase de V3 («o lugar já não é
circular») para NÃO TESTÁVEL até a permutação correr sobre os 56; R3 passa V2
para a moeda do fosso (0,128 e 0,118) com a amplitude do patamar como margem, e
publica os p que estão no JSON; R4 tira o número IoU de V5.

*Condição 1 — um item volta à C0, e é só um.* A reposição de 2019-09-02 altera
um facto que a R2 certificou em **MANTÉM-SE**. Não peço paragem de linha: a
reposição parece-me materialmente certa e travar a cadeia por dois dias de
dia-do-ano seria desproporcionado. Peço a coisa mínima que o protocolo tolera —
que a C0 re-certifique G10 em uma linha, e que a C2 deixe de escrever «nenhum
facto herdado foi rejeitado» enquanto tiver reposto um. V11 fica com o estatuto
que essa re-certificação lhe der.

*Condição 2 — T1 e T3 correm antes de a C3 arrancar.* T1 porque, se alguma
célula da referência sistemática estiver dentro de um foco ou do mapa de défice
de 2026, o denominador de toda a camada está contaminado e o veredicto passa a
«volta à C2» — três linhas separam-nos de saber. T3 porque a C3 vai amostrar
biologia dentro das 3,58 ha de V8, e é preciso saber antes disso se aquelas
hectares têm fileiras.

*O que passa intacto, e é bastante:* **V7** (dois instrumentos, dois princípios
físicos), **V6** na formulação estreita de W1, **V10** (executada na direcção
conservadora), **V1** e a tabela de âncoras, o corpo de **V3**, e o núcleo de
**V5** — a caracterização «extenso e moderado», que é mais útil do que o título
que substituiu.

A retirada dos «8 ha» é sólida e deve manter-se. Não encontrei nenhuma
afirmação viva noutra camada que ainda se apoie no facto retirado. Este
certificado sobrevive a um adversário sério; sobrevive mais estreito, com menos
uma perna em três dos onze factos, e com margens que em dois casos triplicam.
Isso é o que se espera que aconteça, e o «sobrevive» é honesto.
