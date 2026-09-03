# B1 · CONTROLO 3 — o adversário sobre o sector medido como unidade

**Data:** 03-09-2026 · **Alvo:** `b1_como_unidade.py` + `.json` (Landsat, 100
cenas, 6 parcelas do IFAP), a análise anterior `ganfei_s2\b1_serie_verdadeira.py`
(Sentinel-2, 9 cenas, máscara C1a+C1b), a triagem
`reg01_triagem_descontinuidade.py`, e a condição 5 do `guarda.py`.
**Código:** `_VALIDADE_GESTAO\_controlo3_b1\` — onze scripts, todos corridos.
**Não toquei em nada fora dessa pasta.** Não descarreguei nada: a ortofoto que
uso já estava em disco, descarregada esta manhã pelo `c3_08_orto_tres.py` para
todo o ENT 472062 — e as seis parcelas do B1 são todas desse dono, pelo que
cabem na mesma janela.

**A conclusão do B1 resiste. O teste que a produziu não.**

O sector B1 não tem o acontecimento de 2025-26, e não é comparador — as duas
coisas ficam de pé, e a segunda fica mais forte do que estava escrita. Mas o
número publicado (**+0,0921** contra **−0,0854**) sai de uma estatística que
**responde a mesma coisa quer o B1 tenha o acontecimento, quer não**: injectei
o acontecimento real em todas as cenas de 2025-26 e o critério voltou a
imprimir «H1, sinais opostos». E uma das quatro parcelas «de base contínua» não
tem linha de base de kiwi nenhuma — a ortofoto mostra-a em chão nu a 98,3 % em
2018.

Além disso: a condição 5 do portão, reescrita hoje de manhã por exigência do
relatório anterior, **certifica como contínuas as oito unidades que a triagem
existe para excluir**. Corri-a. Passa.

---

## CONFIRMADO

**C1 · A corrida reproduz-se.**
Reconstruí as máscaras das seis parcelas, reli as 100 cenas da cache e
recalculei de raiz. Os **níveis anuais batem ao máximo de diferença 0,00e+00**;
os seis degraus batem a **1,97e−04** — a diferença vem só de o
`b1_como_unidade.py` calcular a mediana regional sem a guarda de cobertura que
aplica às parcelas. As quatro «válidas» são as mesmas quatro.
*Ficheiros:* `c3b1_00_comum.py`, reprodução em §C1.

**C2 · A enumeração das seis parcelas está certa, e não falta nenhuma.**
Sobrepus a caixa declarada do sector (E 529 495–530 063 · N 4 653 832–4 654 477)
a todos os polígonos do IFAP: caem lá **seis parcelas, 12,63 ha, todas 100 %
dentro, todas do ENT 472062**. Não há sétima parcela omitida, nem uma parcela a
meio. Isto era o modo de falha da família B e não se repetiu.
*Ficheiro:* `c3b1_01_geometria.py` §A.

**C3 · A leitura de «estabelecimento» é real para três das quatro — e agora com
instrumento independente.**
Esta era a pergunta 1, e a resposta não podia sair da série. Fui à ortofoto da
DGT (2007 · 2010 · 2012 · 2018 · 2021 · 2025, IRG/FalsaCor, 1 m) e **olhei para
os recortes**:

| CUL_ID | 2007 | 2010 | 2012 | 2018 | 2021 | 2025 | o que se vê |
|---|---|---|---|---|---|---|---|
| 6476415 | campo aberto | grelha de plantas novas | a encher | copado em linhas | **rede** | rede | plantada ~2009-10 |
| 6476420 | campo aberto | grelha de plantas novas | a encher | copado em linhas | **rede** | rede | plantada ~2009-10 |
| 8845740 | campo aberto | grelha de plantas novas | a encher | linhas com solo | rede | rede | plantada ~2009-10 |

**Três pomares plantados por volta de 2009-2010 em campo aberto, ainda a
encher.** A subida de 2017 a 2024 é isso, e não é uma tendência a ser lida como
estabelecimento nem o contrário: é estabelecimento verificado por um instrumento
que não é NDVI. A retirada 14 não se repetiu aqui.
*Ficheiros:* `c3b1_09_orto.py`, `crop_6476415.png`, `crop_6476420.png`,
`crop_8845740.png`.

**C4 · O B1 não tem o acontecimento — por um teste que TEM potência.**
Ajustei a cada parcela uma curva saturante **só a 2017-2024**, extrapolei para
2025 e 2026, e medi o resíduo. Assim a rampa de estabelecimento está *no
modelo* em vez de estar na linha de base, e um acontecimento de −0,085
apareceria como um resíduo de −0,085:

| CUL_ID | prev. 2025 | obs. | prev. 2026 | obs. | resíduo |
|---|---|---|---|---|---|
| 6476415 | 0,867 | 0,859 | 0,891 | 0,883 | **−0,0074** |
| 6476420 | 0,846 | 0,855 | 0,856 | 0,866 | **+0,0096** |
| 8845740 | 0,782 | 0,780 | 0,800 | 0,837 | **+0,0173** |

Resíduo mediano **+0,0096**, contra um acontecimento procurado de **−0,0854** —
oito vezes a dispersão observada. **As três parcelas estão em cima de si
próprias.** A conclusão do B1 sobrevive; o que muda é qual o teste que a
sustenta.
*Ficheiro:* `c3b1_10_veredicto.py` §C.

**C5 · O buraco da pergunta 2 existe, e está medido — mas não move o A3.**
A triagem não tem critério nenhum para unidades que subiram. Apliquei um
rastreio de estabelecimento aos 29 mantidos (nível de 2017 < 0,80 · declive
2017-24 > +0,010/ano · nível 2023-24 pelo menos 0,05 acima do de 2017-18):
**nove dos 29 cumprem as três, e um cumpre duas.** Um terço da população de
comparação está a encher durante a linha de base. Retirei-os:

| conjunto de comparação | n | degrau OC | lugares | margem |
|---|---|---|---|---|
| os 29 da triagem oficial | 29 | −0,0839 | 2.º e 1.º | +0,0200 |
| **sem as 9 em estabelecimento** | 20 | −0,0705 | 2.º e 1.º | **+0,0207** |
| sem estabelecimento e sem a suspeita | 19 | −0,0714 | 2.º e 1.º | +0,0207 |
| sem as 4 parcelas do B1 | 25 | −0,0785 | 2.º e 1.º | +0,0205 |
| sem estabelecimento **e** sem o dono 472062 | 12 | −0,0676 | 2.º e 1.º | +0,0207 |

O receio da pergunta 2 — «o A3 está a comparar copado maduro com pomar jovem» —
**é verdadeiro na descrição e falso na consequência**. Confirma o C11 do
relatório anterior por outro rastreio (nove unidades, não treze; a sobreposição
não é total).
*Ficheiros:* `c3b1_03_estabelecimento.py`, `c3b1_05_multiverso.py` §A.

**C6 · A cronologia da pergunta 6 sobrevive ao cronómetro.**
Fui tentar matá-la pelo relógio: `reg01_triagem_descontinuidade.py` está gravado
às 23:25:25 e a sua saída `reg01_triagem.json` às 23:25:38 — **treze segundos**
para ler 100 cenas Landsat duas vezes sobre 39 e 31 unidades. Cronometrei esse
trabalho exacto na mesma máquina e na mesma cache: **3,2 s** (0,0 s de máscaras,
1,7 s na primeira passagem, 1,5 s na segunda). Com as importações cabe. **Não há
contradição, e havia lugar para uma.**
*Ficheiro:* `c3b1_08_cronometro.py`.

**C7 · E os dois ficheiros da pergunta 6 têm `ctime` = `mtime`.**
`orto_297313_fraccao.json` 23:23:22/23:23:22 e
`reg01_triagem_descontinuidade.py` 23:25:25/23:25:25 — nenhum foi editado depois
de criado, o que fecha a objecção mais óbvia. **Os 123 s são reais.** Vale a
pena notar, porque não é geral: no mesmo directório, `reg01_landsat.py` foi
criado às 23:01:27 e reescrito às **23:25:46**, +1 459 s.
*Ficheiro:* `c3b1_07_datas.py` §6.

---

## CORRIGIDO

**R1 · Uma das quatro «de base contínua» não tem linha de base de kiwi nenhuma.
A ortofoto, e não a série.**
Era a pergunta 3, e a resposta é pior do que a suspeita que a motivou.

| CUL_ID | fracção sem coberto — 2007 · 2010 · 2012 · **2018** · 2021 · 2025 |
|---|---|
| **6476425** | 0,0 % · 0,3 % · 3,6 % · **98,3 %** · 75,0 % · 15,8 % |
| mediana dos 9 blocos de controlo do mesmo dono | 0,0 % · 6,7 % · 9,3 % · 9,5 % · 3,4 % · 6,9 % |

E o recorte decide o que a fracção não decidia (`crop_6476425.png`): **2007 e
2010 mostram mato e árvores; 2012 mostra parte já cortada; 2018 mostra o
triângulo inteiro em chão nu; 2021 mostra pérgola nova acabada de montar; 2025
mostra rede branca.** O nível de **0,890 em 2017** que os limiares leram como
«kiwi maduro» é **vegetação lenhosa**, não é kiwi. A queda para 0,457 em 2018 é
o arranque. A subida de 2019 a 2026 é uma plantação nova.

6476425 sai pela **mesma regra** que tirou 8845729 e 8845739. Ficam **três**
parcelas, e nenhuma delas é kiwi maduro.
O veredicto não muda de classe: degrau mediano das três **+0,1067**, sinais
opostos.
*Ficheiros:* `c3b1_09_orto.py`, `c3b1_10_veredicto.py` §A.

**R2 · «O sector B1 acaba de ser medido como unidade pela primeira vez» — as
seis parcelas já estavam medidas, e quatro delas estão DENTRO da população de
comparação do A3.**
Os seis CUL_ID do B1 são **seis dos 37 blocos** da REG-01 em Landsat, corrida a
01-09. Quatro (6476415 · 6476420 · 8845740 · 6476425) estão entre os **29
mantidos**; duas (8845729 · 8845739) estão entre os oito excluídos. O que é novo
é **agrupá-las e chamar-lhes B1**, não medi-las.

Isto tem duas consequências que nenhum documento regista:
- a mediana regional contra a qual o degrau do B1 é medido **contém o B1**
  (4 de 29). Medi o efeito: retirando-o, o degrau do B1 passa de **+0,0920 a
  +0,0980** — a auto-inclusão é conservadora para a afirmação do B1;
- e é **anti-conservadora para os focos**: sem as quatro parcelas do B1 na
  mediana, o foco OCIDENTAL passa de −0,0839 para **−0,0785**. Pequeno, mas vai
  na direcção da conclusão, e não estava dito.
*Ficheiro:* `c3b1_01_geometria.py`, `c3b1_05_multiverso.py`.

**R3 · «O fosso à referência fecha de 0,328 para 0,068» — 18 % disso é a
referência a cair, e no troço recente é 38 %.**
A referência da corrida de Sentinel-2 é o **corpo principal do pomar** — a
unidade que teve o acontecimento. Decompus:

| | Δ fosso | do B1 a subir | da referência a cair |
|---|---|---|---|
| 2017 → 2026 | −0,2602 | −0,2144 (**82 %**) | −0,0459 (**18 %**) |
| **2024 → 2026** | −0,1448 | −0,0900 (62 %) | −0,0549 (**38 %**) |

Um fosso que fecha porque o denominador colapsa não mede o numerador a subir.
Sobre 2017-2026 a leitura aguenta; sobre a janela do acontecimento, mais de um
terço do fecho é o outro lado a descer. **A frase tem de dizer qual das duas
janelas está a citar.**
*Ficheiro:* `c3b1_04_concordancia.py` §B.

**R4 · O critério do `b1_como_unidade.py` não foi «fixado antes de correr». O
próprio ficheiro diz as duas coisas.**
O cabeçalho escreve «HIPÓTESE E CRITÉRIO, FIXADOS ANTES DE CORRER». Trinta
linhas abaixo, no código, está: «CORRIGIDO: a primeira versão era
`abs(med_b1)/abs(alvo)`, e por isso um degrau POSITIVO da mesma magnitude
disparava “H0 · o B1 TEM o degrau”».
As datas confirmam-no e datam-no: `b1_como_unidade.py` criado às **22:43:15**,
`b1_como_unidade.json` criado às **22:43:26** (onze segundos depois — a primeira
corrida), o `.py` reescrito às **22:45:26**, o `.json` reescrito às **22:45:32**.
**Correu, viu, corrigiu o critério, correu outra vez.** A correcção está certa —
um critério que não distingue melhoria de declínio não é um critério — e está
declarada com honestidade no código. Mas então a frase do cabeçalho tem de sair,
tal como saiu a palavra «cego» do A3.
*Ficheiro:* `c3b1_07_datas.py` §6.

**R5 · «Entra aqui a mesma triagem de descontinuidade que retirou o A3» — não é
a mesma.**
O `b1_como_unidade.py` reimplementa a triagem e acrescenta-lhe uma segunda regra
(`jovem`: média da base < 0,60) que não existe em
`reg01_triagem_descontinuidade.py`. Verifiquei o que ela faz: **neste caso, nada
— as duas regras dão as mesmas quatro válidas.** Mas uma reimplementação com uma
regra a mais não é «a mesma triagem», e é assim que duas cadeias divergem sem
que ninguém dê por isso.

**R6 · O instrumento da fracção sem coberto lê REDE como chão nu. Está provado.**
6476415 lê **46,8 % «sem coberto» em 2021** e o recorte mostra um pomar inteiro
debaixo de rede; 6476420 lê **55,1 %** da mesma maneira. A mediana dos controlos
do mesmo dono em 2021 é 3,4 %, portanto não é um efeito de imagem: é a rede, que
no IRG lê cinzento-azulado como o solo. Isto não anula o C6 do relatório
anterior — lá **olhou-se** para os recortes, que é o que salva o método — mas
qualquer uso futuro da fracção depois de ~2019 nas parcelas deste dono tem de
ser olhado, não só medido.
*Ficheiros:* `c3b1_09_orto.py`, `crop_6476415.png`.

**R7 · A pergunta 5, respondida: o C3 fica mais forte e tem de ser reescrito; o
A1 nunca incluiu o B1.**
- **C3** («não há controlo externo contemporâneo de kiwi neste caso») fica **mais
  forte**, e por uma razão nova e independente da que lá está. A actual assenta
  em «mesma exploração». A que se acrescenta é: **nenhuma das seis parcelas do
  B1 tem linha de base de kiwi maduro** — três são plantações de ~2010 ainda a
  encher (ortofoto), uma é mato convertido depois de 2018 (ortofoto), duas são
  plantações posteriores a 2021 (ortofoto, 01-09). **Zero maduras.** Não há
  controlo externo *nem interno*.
- **A1** («o acontecimento é em duas posições e não no resto») — o «resto» do A1
  foi medido dentro da AOI de 2 × 1 km, que **exclui o B1 por construção**. O B1
  nunca esteve no «resto». Pode agora juntar-se-lhe, mas citando o teste
  contrafactual do C4, **não** o degrau publicado (ver X1), e mantendo a marca de
  que continua a ser óptico dos dois lados (ver N1).

---

## REJEITADO

**X1 · «O B1 não tem o degrau de 2025-26 · degrau mediano +0,0921 contra −0,0854
dos focos · sinais opostos.» O conteúdo sobrevive. O TESTE sai.**

Fiz-lhe a pergunta da família C: *o que é que este teste faria se a hipótese
fosse falsa?* Injectei o acontecimento real — **−0,0854 em todas as 29 cenas de
2025-26** — em cada parcela do B1 e recalculei o mesmo degrau:

| CUL_ID | degrau real | **com −0,0854 injectado** | detecta? |
|---|---|---|---|
| 6476415 | +0,1067 | **+0,0213** | não |
| 6476420 | +0,0773 | −0,0081 | sim, à justa |
| 8845740 | +0,1249 | **+0,0395** | não |
| 6476425 | +0,0577 | −0,0277 | sim, à justa |
| **mediana das 4** | **+0,0920** | **+0,0066** | **NÃO** |

Com o acontecimento inteiro lá dentro, o critério publicado imprime **«H1, e por
margem larga: o B1 não só não desce como SOBE (+0,0066) enquanto os focos descem
(−0,0854). Sinais opostos.»** — a mesma frase, a mesma classe de veredicto.

E o piso de detecção, medido por varrimento:

| acontecimento injectado | degrau mediano | o que o critério diz |
|---|---|---|
| 0,000 | +0,1067 | H1 (sinais opostos) |
| −0,100 | +0,0067 | H1 (sinais opostos) |
| **−0,120** | ≈ 0 | muda de sinal |
| **−0,180** | −0,073 | primeira vez que diz **H0** |
| −0,200 | −0,0933 | H0 |

**O piso é 2,1× o acontecimento que se procura.** Um teste que só declara «tem o
degrau» a partir do dobro do degrau que anda a procurar não está a medir o B1:
está a medir a rampa de estabelecimento que ficou dentro da janela de base. É o
mesmo defeito estrutural do **T5** que este Controlo 3 já matou — um cálculo
cujo ramo de refutação é inalcançável.

**O que se pode escrever:** o resultado do C4 — as três parcelas estão em cima
da sua própria curva ajustada só à linha de base, resíduo mediano **+0,0096**
contra um acontecimento procurado de −0,0854. Esse teste tem potência e dá a
mesma resposta. **A conclusão fica; o número +0,0921 e o critério dos terços
saem.**
*Ficheiros:* `c3b1_02_saturacao.py` §C, `c3b1_10_veredicto.py` §B.

**X2 · «A corrida nova em Landsat concorda com a análise anterior em Sentinel-2,
com outra fronteira e outra sessão.» A aritmética é verdadeira. A palavra
«concorda» está a fazer trabalho que não pode.**

Cruzei instrumento × geometria, as quatro combinações:

| | Landsat 30 m, degrau | Sentinel-2 10 m, degrau absoluto |
|---|---|---|
| C1a+C1b (ortofoto, 11,60 ha) | **+0,0720** | **+0,0847** |
| IFAP 6 parcelas (12,63 ha) | **+0,0710** | **+0,0842** |
| IFAP 4 «válidas» (8,56 ha) | +0,0908 | +0,1095 |

**Um milésimo entre as duas geometrias em Landsat, cinco décimos de milésimo em
Sentinel-2.** A concordância numérica é real e reproduz-se — digo-o com a mesma
clareza com que rejeito o resto. O que não é sustentável é o que a frase
implica:

1. **Não são instrumentos independentes.** São dois NDVI ópticos. O cabeçalho do
   `b1_como_unidade.py` di-lo, textualmente: «isto **não** é instrumento
   independente para o sinal: é óptico dos dois lados». A `CLAUDE.md` deste
   projecto fecha a questão: *um NDVI não se confirma com outro NDVI.*
2. **Não são a mesma unidade.** Jaccard **0,738**. Do IFAP, 2,34 ha (19 %) ficam
   fora do C1; do C1, 1,31 ha (11 %) não são kiwi declarado.
3. **E a discordância está escondida na composição.** Da máscara C1a+C1b usada
   em Sentinel-2: **33 % é 8845729 + 8845739**, as duas parcelas que a corrida
   nova exclui como plantação nova; **11 % não é kiwi declarado**; e **6476425 —
   uma das quatro que a corrida nova declara válida — está a 0 %** dentro dela.

Ou seja: a corrida nova concorda com a antiga sobre um objecto de que exclui um
terço e a que falta um sexto. Reescrever para: *as duas medições dão a mesma
subida sobre geometrias com Jaccard 0,738; não são instrumentos independentes, e
33 % da máscara de 2026-08 é material que a triagem de 2026-09 retira.*
*Ficheiro:* `c3b1_04_concordancia.py` §A e §C.

**X3 · «O B1 não é comparador válido porque as 4 parcelas estão em
estabelecimento.» A conclusão é certa; a razão está incompleta e um sexto dela é
falso.**
Não são quatro em estabelecimento: são **três em estabelecimento verificado por
ortofoto** e **uma sem linha de base de kiwi** (R1). E há uma quarta categoria
que a frase perde: 6476415 e 6476425 **têm quedas anuais acima do limiar da
triagem** dentro de 2017-2024 (0,321 em 2019 e 0,433 em 2018) e só passaram
porque o critério mede a **média de todos os anos seguintes**, que a recuperação
levanta acima de 0,60. Pelo nível **do ano da queda** — que é o que a frase
«mudança de uso» significa — as duas seriam **excluídas**:

| CUL_ID | cai | nível no ano da queda | média de lá até 2026 | veredicto da triagem |
|---|---|---|---|---|
| 6476415 | 0,321 em 2019 | **0,466** | 0,776 | fica |
| 6476425 | 0,433 em 2018 | **0,457** | 0,672 | fica |

Redacção certa: *nenhuma das seis parcelas do B1 tem linha de base de kiwi
maduro entre 2017 e 2026 — três são plantações de ~2010 ainda a encher, uma é
mato convertido em pomar depois de 2018, duas são plantações posteriores a 2021.
Duas das quatro que a triagem manteve caem mais de 0,25 num ano dentro da linha
de base e só sobrevivem porque o critério promedia a recuperação.*
*Ficheiros:* `c3b1_03_estabelecimento.py` §Q3, `c3b1_09_orto.py`.

---

## NÃO TESTÁVEL

**N1 · Se o B1 teve o acontecimento, com instrumento INDEPENDENTE.**
Landsat e Sentinel-2 são ópticos os dois. Não há SAR em cache para a janela do
B1, o LiDAR está bloqueado desde 01-09 (autenticação da DGT) e a ortofoto não
bracketa o acontecimento — as épocas são 2021 e 2025, e o segundo passo é
**Julho de 2026**. O facto fica onde a `LISTA_FINAL` põe estes: **secção B, sem
instrumento independente, com a marca à vista.**
*Teste que decidiria:* SAR sobre a janela do B1, com a mesma cadeia do A2 — a
única física diferente que este caso demonstrou saber usar.

**N2 · A queda de 6476415 em 2019 (0,787 → 0,466 → recuperada em 2021).**
Não há ortofoto entre 2018 e 2021. A de 2018 mostra copado normal e a de 2021
mostra rede. **Não decido**, e importa: se for arranque parcial, a parcela cai na
categoria do 6476425 e o B1 passa a ter **duas** parcelas em três.

**N3 · Se a ordem dos ficheiros da pergunta 6 é a ordem do pensamento.**
Aqui a resposta é precisa, e é a pergunta que foi feita. Testei os cinco modos
de falha do `st_ctime` no Windows, empiricamente, nesta máquina:

| experiência | resultado |
|---|---|
| `st_ctime` é o mesmo que `GetFileTime`/CreationTime? | **sim** — é criação, **não** é o «change time» do POSIX |
| copiar (`shutil.copy2`) | **repõe o ctime para agora** e preserva o mtime — o ctime pode ficar *depois* do mtime |
| mudar de nome / mover no mesmo volume | **preserva** o ctime — não prova que o ficheiro estava nesta pasta |
| reescrever o conteúdo | **não toca no ctime** — um ficheiro criado às 23:25 e reescrito às 03:00 continua a dizer 23:25 |
| apagar e recriar com o mesmo nome em 2 s | **ctime idêntico ao anterior, diferença +0,00 s** — é o tunelamento do NTFS, janela de ~15 s |
| `SetFileTime` sem privilégios | **funcionou** — recuou o ctime um ano. Qualquer processo do utilizador escreve neste campo |

**O que garante, e é fraco:** que uma entrada com este nome apareceu nesta pasta
a esta hora.
**O que NÃO garante:** que o conteúdo seja dessa hora; que o ficheiro não tenha
chegado já escrito de outro lado; que a ordem entre dois ficheiros seja a ordem
do trabalho; nada, se houve recriação em 15 s; nada contra alteração deliberada.

**Aplicado ao caso concreto, e a favor:** as duas objecções que matariam a
afirmação não se aplicam — o intervalo é de **123 s**, muito fora da janela de
tunelamento, e os dois ficheiros têm `ctime` **igual** ao `mtime`, o que exclui
edição posterior (C7). Fica de pé **uma** objecção que não consigo fechar: um
ficheiro copiado com `copy` simples fica com ctime *e* mtime iguais à hora da
cópia, indistinguível de escrita fresca. Portanto:

> **É sólido como afirmação sobre quando as duas entradas apareceram, e é isso
> que o X1 anterior precisa.** Não é sólido como afirmação sobre honestidade —
> e não precisa de ser, porque ninguém está a alegar manipulação. O que o `ctime`
> **nunca** vai dar é o que a `N1` do relatório anterior pediu: um compromisso
> **anterior** à corrida. Isso só um repositório dá, e o custo continua a ser
> nenhum.
*Ficheiro:* `c3b1_07_datas.py`.

**N4 · Se as 6 parcelas eram kiwi antes de 2007.** A ortofoto começa em 2007 e
mostra campo aberto em quatro delas e mato em 6476425. Antes disso não sei, e
não é preciso saber: a linha de base do caso é 2017.

---

## LINE-STOP

**L1 · A condição 5 do `guarda.py`, reescrita hoje de manhã, certifica como
contínuas as oito unidades que a triagem existe para excluir. Corri o portão.**

A reescrita substituiu a cadeia de caracteres por **prova em disco**: exige o
caminho de um rastreio de descontinuidade e a lista das unidades. Lê-lhe duas
chaves — `nivel`/`nivel_anual` para saber o que está *coberto*, e `alerta` para
saber o que está *marcado*.

**`reg01_triagem.json` não escreve `alerta` nenhuma.** Escreve `excluidos` e
`mantidos`. Logo `R.get("alerta", [])` vem vazia, **nenhuma unidade fica
marcada**, e as oito excluídas — que estão todas em `nivel_anual`, porque o
ficheiro guarda a série de todas — contam como cobertas e não alertadas.

```
--- T3 · pedir ao portao que certifique as OITO que a triagem excluiu
VEREDICTO: as oito excluidas tem linha de base continua
  unidade no tempo: reg01_triagem.json, 0 cenas, 39 unidades, 2.0 dias
                    — verificadas: 6705420, 6705421, 6705422, 6705424,
                      6705427, 8845729, 8845731, 8845739
  *** PASSOU ***
```

O mesmo com `b1_como_unidade.json` sobre as duas parcelas que o próprio script
imprime como «FORA — base média 0,58 < 0,60 (plantação nova)»: **passa**.

**A condição 5 trocou uma afirmação por um ficheiro, e continua a não ler o
veredicto que o ficheiro contém.** É a terceira encarnação do mesmo erro: a
primeira acreditava numa frase; a segunda acredita na *existência* de um
ficheiro. O relatório anterior escreveu que `ancoras()` e `reproduz()` recebem
números e a condição 5 recebia uma cadeia — agora recebe um caminho, e continua
a não calcular nada sobre o conteúdo.

**A correcção, e é de três linhas:**
```
excluidas = set(map(str, R.get("excluidos", []))) | set(map(str, R.get("alerta", [])))
mantidas  = set(map(str, R.get("mantidos", R.get("validos", cobertas))))
if pedidas & excluidas:  -> BLOQUEIA, nomeando quais
if pedidas - mantidas:   -> BLOQUEIA: a unidade nao esta na lista de MANTIDAS,
                            e o silencio nao conta como aprovacao
```
A pertença tem de ser à lista das **mantidas**, não à cobertura. Um ficheiro que
enumera 39 séries cobre tudo o que mediu, incluindo o que reprovou.

**E há um segundo caso, que este mesmo teste apanhou:** a afirmação do B1 como
está escrita hoje — instrumento Landsat, «confirmado por» NDVI Sentinel-2,
fronteira do IFAP, `identidade_no_tempo(reg01_triagem.json, [as 4 válidas])` —
**passa o portão inteiro**. Passa apesar de o instrumento «independente» ser
outro NDVI, o que a `CLAUDE.md` proíbe em letra e o cabeçalho do próprio script
declara. **A condição 2 verifica um booleano `concorda`; não tem noção nenhuma
de independência física.** Nada no portão impede que dois sensores da mesma
família se confirmem um ao outro — que é exactamente a família A da taxonomia,
cinco retiradas.
*Ficheiro:* `c3b1_06_guarda.py`.

---

**L2 · O A3 não é invariante à estatística de agregação. Quatro em oito.**

Isto não é o intervalo de amostragem que o relatório anterior já registou. É
outro eixo, e não foi variado por ninguém: o degrau publicado é
**média**(desvio 2025-26) − **média**(desvio 2017-2024). A mediana é tão
defensável como a média — é a estatística que esta cadeia usa em todo o lado
para agregar — e a janela de base é uma escolha, não um dado, precisamente
porque um terço das unidades está a encher dentro dela (C5).

Oito corridas, quatro janelas × duas estatísticas:

| base | estatística | degrau OC | degrau OR | lugar OC | lugar OR | margem |
|---|---|---|---|---|---|---|
| 2017-24 | **média (a publicada)** | −0,0839 | −0,0869 | 2 | 1 | **+0,0200** |
| 2017-24 | mediana | −0,0663 | −0,0762 | **3** | 1 | **−0,0012** |
| 2019-24 | média | −0,0820 | −0,0826 | 2 | 1 | +0,0218 |
| 2019-24 | mediana | −0,0655 | −0,0707 | 2 | 1 | +0,0006 |
| 2021-24 | média | −0,0767 | −0,0710 | 1 | 2 | +0,0142 |
| 2021-24 | mediana | −0,0570 | −0,0653 | **3** | 1 | **−0,0036** |
| 2023-24 | média | −0,0688 | −0,0530 | 1 | **4** | **−0,0023** |
| 2023-24 | mediana | −0,0451 | −0,0353 | **3** | **5** | **−0,0245** |

> **Os dois focos são o 1.º e o 2.º em 4 das 8 corridas.**
> Lugar do OCIDENTAL: 1, 1, 2, 2, 2, 3, 3, 3. Lugar do ORIENTAL: 1, 1, 1, 1, 1,
> 2, 4, 5.
> Margem: mínimo **−0,0245** · **mediana −0,0003** · máximo +0,0218.

Quem entra é sempre o mesmo: **6705424** (ENT 297313) escorrega para entre os
dois focos em três das quatro corridas com mediana, e nas janelas curtas
aparecem 8189628 e 8189734. 6705424 é maduro (2017 = 0,851), declive −0,004/ano,
maior queda 0,048 — passa todos os rastreios. **Não é um bloco suspeito a
entrar por uma porta lateral: é um competidor legítimo que a escolha da
estatística estava a esconder.**

O mesmo aparece numa estatística que nem sequer usa a janela de base — o degrau
de planalto, nível de 2025-26 menos nível de 2023-24: OCIDENTAL **−0,1097**
(percentil 0 %) mas ORIENTAL **−0,0647**, atrás de 8189734 (−0,0849) e 8189628
(−0,0820), ou seja **4.º**.

**A frase «o pior e o segundo pior» é uma corrida preferida de uma
distribuição.** A regra da `CLAUDE.md` sobre isto é explícita — *relatar a
distribuição, não a corrida preferida* — e é a única das regras do multiverso
que esta cadeia ainda não cumpriu para o A3. O que se pode escrever, medido:

> *o foco OCIDENTAL é o pior em 2 de 8 corridas e está nos três piores em 8 de
> 8; o foco ORIENTAL é o pior em 5 de 8 e o seu lugar varia entre 1 e 5. Os dois
> juntos ocupam os dois primeiros lugares em 4 de 8. A isto acresce a incerteza
> de amostragem já registada (P = 0,07 por cenas, 0,25 por anos).*

**Isto não é uma retracção do A3, e não o transforma em falso.** É a diferença
entre «são o pior e o segundo pior» e «estão consistentemente na cauda, e o
lugar exacto depende de escolhas defensáveis». A primeira forma é a que a
`LISTA_FINAL` publica, e é a que esta cadeia já retirou dezanove vezes.
*Ficheiro:* `c3b1_05_multiverso.py` §B.

---

## NOTA DE MÉTODO

Onze scripts, em `_VALIDADE_GESTAO\_controlo3_b1\`:

| | ficheiro | o que decide |
|---|---|---|
| 00 | `c3b1_00_comum.py` | matriz cena × unidade reconstruída da cache; 37 blocos + 6 do B1 + 2 focos |
| 01 | `c3b1_01_geometria.py` | as parcelas na caixa do B1; IFAP contra C1a+C1b |
| 02 | `c3b1_02_saturacao.py` | saturação por AICc; declives por metade; **a injecção**; o contrafactual |
| 03 | `c3b1_03_estabelecimento.py` | o rastreio de estabelecimento sobre os 29; a queda que a triagem promedia |
| 04 | `c3b1_04_concordancia.py` | instrumento × geometria; a decomposição do fosso; a composição da máscara S2 |
| 05 | `c3b1_05_multiverso.py` | REG-01 sem estabelecimento; **as oito corridas de janela × estatística** |
| 06 | `c3b1_06_guarda.py` | o portão posto a julgar o B1 e as oito excluídas |
| 07 | `c3b1_07_datas.py` | as seis experiências sobre o `st_ctime`; a cadeia real |
| 08 | `c3b1_08_cronometro.py` | o trabalho da triagem contra o intervalo de 14 s |
| 09 | `c3b1_09_orto.py` | **a ortofoto sobre as seis parcelas**, e os recortes |
| 10 | `c3b1_10_veredicto.py` | a composição corrigida; **o piso de detecção** |

Mais seis recortes, um por parcela — `crop_6476415.png` · `crop_6476420.png` ·
`crop_6476425.png` · `crop_8845729.png` · `crop_8845739.png` ·
`crop_8845740.png` — com as seis épocas lado a lado, e são eles que decidem o R1
e o C3.

**Falhas técnicas, para o registo: nenhuma.** Nenhum teste ficou por correr por
razão técnica. A consola cp1252 mutilou acentos na saída impressa, sem afectar
nenhum cálculo. O laboratório do `c3b1_07` criou e apagou ficheiros só dentro de
`_controlo3_b1\_lab\`.

**O que não fiz.** Não descarreguei nada — a ortofoto já estava em disco e as
seis parcelas do B1 cabiam na janela do ENT 472062 pedida esta manhã. Não tentei
o LiDAR (bloqueado desde 01-09). Não fui a SAR: não há cache para a janela do B1
e a instrução era não descarregar. Não corri o `certificar.py`: alterar a
`LISTA_FINAL` não é trabalho de adversário.

---

**Nota final.** Vim procurar o erro, e a instrução era dizer com a mesma clareza
se a leitura resistisse. **Resiste, e o teste que a produziu não.**

O B1 não tem o acontecimento — mostrei-o por um teste com potência, depois de
mostrar que o teste publicado não a tem: injectei o acontecimento inteiro e ele
voltou a imprimir a mesma frase. O B1 não é comparador — e é menos comparador do
que estava escrito, porque a ortofoto tirou-lhe a quarta parcela e não lhe deixou
nenhuma de kiwi maduro. As duas corridas concordam ao milésimo, e essa
concordância não é a corroboração que a frase sugere: são dois NDVI sobre
geometrias com Jaccard 0,738, uma delas com um terço de plantação nova.

O que fica em aberto é maior do que o B1. **O portão volta a autorizar o que foi
escrito para bloquear** — desta vez com um ficheiro em vez de uma frase, e o
ficheiro é o próprio registo das exclusões. E **o A3 depende de uma escolha entre
média e mediana que ninguém declarou estar a fazer**: quatro corridas em oito
tiram os focos dos dois primeiros lugares, e é sempre o mesmo bloco maduro a
entrar pelo meio.
