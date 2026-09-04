# A2 · CONTROLO 3 — o adversário sobre os nove boletins de físico-química do solo

**Data:** 04-09-2026 · **Alvo:** `a2_solo_caracterizacao.py` + `.json`, e os
factos **D7, D8 e D9** tal como entraram na `LISTA_FINAL_2026-08-31.md` e no
`registo_de_factos.py` às 08:40 de hoje.
**Código:** `_VALIDADE_GESTAO\_controlo3_a2\` — treze scripts, todos corridos.
**Não toquei em nada fora dessa pasta.** Não descarreguei nada.

---

**O D7 sobrevive na conclusão e nenhuma das suas três razões sobrevive. O D8 cai
inteiro. O D9 parte-se em dois: a metade da CTC fica, a metade da profundidade
não.**

E há uma coisa maior do que os três. **O D8 assenta no número `+0,092` que o
Controlo 3 rejeitou ontem à noite às 23:07** — nove horas antes de o
`a2_solo_caracterizacao.py` ser escrito — e usa o B1 como comparador de
não-declínio, que é textualmente a **retirada 18** e é textualmente o que a
**secção F da mesma `LISTA_FINAL`** proíbe escrever.

---

## CONFIRMADO

**C1 · Os dados reproduzem-se, e a extracção é fiel à fonte.**
Reconstruí a matriz 9 × 12 do `c3_04_registo_principal.csv` e comparei-a célula
a célula com a folha **«Fisico-Quimica por Talhao»** do
`Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx`, de que ela deriva:
**108 de 108 células idênticas, zero discrepâncias.** Nove ficheiros-fonte, nove
números de boletim, um cliente (*Kiwi 1000, Lda*), um laboratório (*A2 Análises
Químicas, Guimarães*), doze linhas por boletim. Os nove valores de pH e a ordem
em que o D8 os apresenta estão certos.
*Ficheiros:* `c3a2_02_matriz.py`, `c3a2_09_extraccao.py`.

**C2 · A primeira metade do D9 está certa, e verifiquei-a a montante.**
Procurei «CTC», «satura» e «bases» **nas nove folhas dos dois livros de Excel**,
não só no CSV: **zero ocorrências em qualquer dos dois.** Não há complexo de
troca em lado nenhum do dossiê. A afirmação «faltam a CTC e a saturação em
bases» é verdadeira e é verificável contra a fonte, não só contra o derivado.
*Ficheiro:* `c3a2_09_extraccao.py` §D.

**C3 · A condição 6 está genuinamente satisfeita, e é raro.**
`fronteira("código de bloco escrito pelo laboratório")` — o rótulo
`Terrain_Block_Parcel` vem do boletim, escrito por quem colheu, e não pode ter
sido derivado de nenhum sinal nosso porque é anterior a todos eles. É o
contrário do `fazer_masks_v2.py`, e digo-o com a mesma clareza com que rejeito o
resto.

**C4 · A conclusão do D7 sobrevive.** Estes nove boletins não podem testar
afectado contra não afectado. **Nenhuma das três razões escritas sustenta isso**
(ver R2, R3 e X1), mas a conclusão sobrevive por razões melhores, medidas: são
**oito talhões e não nove** (R1), **quatro unidades distintas com posição**, e
nenhuma partição dos oito resiste à correcção de multiplicidade (X3).

**C5 · NÃO é a retirada 9 outra vez. O «B1» dos boletins é o sector B1.**
Era a pergunta 3, e a resposta é a favor. Sobrepus os seis polígonos do IFAP ao
eixo das **duas coordenadas duras do gestor** (E529500 N4654010 → E530054
N4654413, 685 m, azimute 54°, `b1_divisao.py` / R2 G36):

| CUL_ID | ha | distância ao eixo do gestor |
|---|---|---|
| 6476415 · 6476420 · 8845729 · 8845739 · 8845740 | 11,36 | **0 m** — o eixo atravessa-as |
| 6476425 | 1,27 | 45 m |

**87 % da área a menos de 150 m do eixo, 98 % a menos de 200 m.** Não há aqui
duas entidades em sítios diferentes, como havia com a AOI de Valença. O prefixo
«B1» dos boletins e o sector B1 medido em Landsat são o mesmo sítio.
**Mas não são a mesma área** — ver R5 — e nada liga «C1», «C3» ou «C4» a uma
parcela concreta — ver N2.
*Ficheiro:* `c3a2_06_q3_identidade.py`.

**C6 · O `instantanea()` do D9 é legítimo, sem reserva.** É um inventário de um
conjunto fixo de documentos. Não compara nada ao longo do tempo.

---

## CORRIGIDO

**R1 · «Nove boletins» são OITO talhões. E o nono é a única estimativa de erro
que este conjunto tem, e ninguém a usou.**

`B2 - V7` (2026-03-03, ficheiro `B2_V7__Marc_o_26.pdf`, boletim 2601932) e
`B2 - Zona 1 (V7)` (2026-06-17, `B2_V7__Junho_26.pdf`, 2606721) são **o mesmo
talhão, a mesma válvula 7**, colocados pela C3 na mesma coordenada
E530392,4 N4654977,1. A pré-voo do próprio ficheiro responde à pergunta 8 —
«quantas observações independentes, mesmo?» — com «nove boletins; não 108
registos». Acertou no primeiro nível e falhou no seguinte: **são 8**.

E a repetição vale mais do que a contagem. É o **piso de ruído medido**:

| parâmetro | Março | Junho | razão |
|---|---|---|---|
| **pH** | 5,8 | 5,6 | **0,2 unidades** |
| CaO | 264 | 505 | 1,91× |
| MgO | 62,9 | 93,0 | 1,48× |
| MO | 1,7 % | 2,4 % | 1,41 % |
| C:N | 6,7 | 9,3 | 1,39× |
| **Textura** | **Franca** | **Argilosa** | **muda de classe** |

A folha «Traceability Gaps» do livro EN já regista a inconsistência de textura
como item aberto. **A de pH nunca foi registada, e é ela que decide o D8.**
*Ficheiros:* `c3a2_05_multiplicidade.py` §B, `c3a2_00_dados.py`.

**R2 · «Zero têm coordenada» — o zero é uma constante escrita à mão, e o
ficheiro que o D7 cita coloca SEIS dos nove.**

No `a2_solo_caracterizacao.py`:

```
print("  boletins com COORDENADA: 0 de %d" % len(ph))
print("  boletins inequivocamente DENTRO de um foco: 0 de %d" % len(ph))
```

Os dois zeros são **literais**. Não saem de nenhuma leitura: o script nunca abre
o `c3_07_registos_colocados.csv`. E esse ficheiro — que o enunciado do facto
nomeia como fonte — dá isto:

| boletim | classe | E | d(foco O) | d(foco E) | défice 2026 |
|---|---|---|---|---|---|
| Erica 2016 R | INFERIDO | 530700,5 | 219 | 278 | 2,8 % |
| Erica 2016 E | INFERIDO | 530700,5 | 219 | 278 | 2,8 % |
| B2 - V7 | COLOCADO | 530392,4 | **120** | 601 | 21,2 % |
| B2 - Zona 1 (V7) | COLOCADO | 530392,4 | **120** | 601 | 21,2 % |
| **B3 - 7 ha** | COLOCADO-BLOCO | 530940,9 | 471 | **67** | **46,9 %** |
| Parcela B4 | AMBIGUO | 531296,3 | 854 | 379 | 6,2 % |
| B1 C1 · C3 · C4 | FORA DA BANDA | — | — | — | — |

**Seis de nove têm posição UTM em disco.** A redacção certa não é «zero têm
coordenada»: é *«seis dos nove têm posição, de classes COLOCADO (2),
COLOCADO-BLOCO (1), INFERIDO (2) e AMBIGUO (1); as três primeiras vêm da
partição por válvula, que o C7 desqualifica para quantidades; os três do B1 não
têm posição nenhuma.»* É a mesma conclusão e é uma afirmação verificável em vez
de um número escrito à mão. É também a armadilha do `print("ok")` incondicional
da §7 do `ANTES_DE_COMECAR`, noutra roupa.
*Ficheiro:* `c3a2_10_veredicto.py` §B.

**R3 · «Zero inequivocamente dentro de um foco» — o `B3 - 7 ha` está a 67 m do
centro do foco ORIENTAL, e o disco de toda esta cadeia tem r = 90 m.**
`c3_07_georreferenciar.py`, linha 50: `discos_dos_focos(pomar, raio=90.0)`.
67 < 90. O boletim do bloco do foco oriental está dentro do disco do foco
oriental. A palavra «inequivocamente» faz algum trabalho — a colocação é o
centróide do bloco, e o próprio ficheiro nota que «a tabela dá 9,01 ha ao B3 e o
boletim diz 7 ha» — mas a frase publicada não diz isso: diz zero.
*Ficheiro:* `c3a2_10_veredicto.py` §B.

**R4 · Os «12 parâmetros» são TREZE grandezas, e a décima terceira parte o
conjunto exactamente pela partição que o D8 usa.**

Dentro da cadeia do Manganês há um segundo valor, o **MnAI**:

| lote | boletins | MnAI |
|---|---|---|
| 2026-03-03 | Erica 2016 R · Erica 2016 E · B2-V7 · B3-7 ha | **não** |
| 2026-06/07 | B2-Zona 1 · **B1 C1 · B1 C3 · B1 C4** · Parcela B4 | **sim** (39,5 · 57,1 · 58,3 · 49,6 · 49,5) |

Duas consequências. Primeira: o D9 conta **linhas**, não grandezas — um
inventário que perde a décima terceira não é um inventário. Segunda, e é pior:
**«ser do B1» e «ser do lote de Julho» são a mesma partição mais um elemento**,
e o lote **demonstravelmente difere**, porque reporta uma grandeza a mais.
Nenhum desenho com n = 8 separa as duas coisas. O confundimento não é uma
hipótese minha: está impresso nos valores.
*Ficheiro:* `c3a2_12_lote.py`.

**R5 · O sector B1 medido tem 12,63 ha; o B1 que a exploração declara tem 9,01.
Ninguém reconciliou os +40 %.**
As seis parcelas do IFAP somam **12,63 ha**; a tabela de áreas do gestor dá às
válvulas 1 a 5 — que é o que a exploração chama B1 — **9,01 ha**
(13500+9375+12750+24550+29900 m²). E **1,60 ha do sector (13 %) ficam a sul de
N4654010**, que é o extremo sudoeste que o gestor deu. O `+0,092` é a mediana de
quatro parcelas de um polígono 40 % maior do que o objecto de que o boletim traz
o nome.
*Ficheiro:* `c3a2_06_q3_identidade.py`.

**R6 · A segunda metade do D9 tem de ser reescrita: «não está no CSV» não é
«não foi medida», e desta vez há prova de que há página por ler.**

Era a pergunta 4, e a resposta tem três camadas.

**(a) Os cinco campos verificados não podiam conter uma profundidade.**

| campo | valores distintos nos 108 registos |
|---|---|
| `Notes` | **1 — e é vazio. 108 vazios de 108.** |
| `Matrix` | 1 — «Solo» |
| `Test_Category` | 1 — «Físico-química» |
| `Interpretation` | 12 — o nome do parâmetro |
| `Method` | 6 — a norma analítica (ISO 10390, Mehlich 3/ICP-OES…) |

Nenhum é campo de metadados de **colheita**. O esquema do CSV **não tem coluna
nenhuma** onde uma profundidade pudesse estar. E o detector procura as cadeias
`cm`, `profund`, `0-2`, `0-3`, **`20`** e **`30`** — os dois últimos casam com
qualquer número; se o `Method` dissesse «ISO 10930», este teste teria impresso
«menção a profundidade: sim». **Não é um detector de profundidade: é um detector
de dois dígitos aplicado a cinco campos errados.** Não tinha ramo de refutação.

**(b) Há uma página que uma das extracções não leu, e está escrito.** A folha
«Soil Chemistry by Block» do livro EN escreve **«n/a (page 2 not extracted)»**
em **nove células** — Fe e Mn dos quatro boletins de Julho e Mn do de Junho — e
a folha PT tem números nessas mesmas células. O `c3_03` já registara o mesmo
para o Azoto Total (nove linhas em falta no EN). **Um boletim A2 declara a
profundidade no cabeçalho da amostra, que é exactamente o material que não
passou para nenhuma tabela.**

**(c) Os nove PDF não estão nesta máquina.** Procurei-os em `Downloads`,
`Documents` e `Desktop`: **zero de nove**. Não posso decidir, e ninguém pode com
o que está em disco — ver N1.

Redacção certa: *«A profundidade de colheita não consta de nenhum campo do
registo extraído, e o registo extraído não tem campo de colheita nenhum. Se está
declarada no boletim original, não se sabe: os PDF não estão no dossiê e uma das
duas extracções assinala páginas não lidas nestes mesmos boletins.»*
*Ficheiros:* `c3a2_08_q4_profundidade.py`, `c3a2_10_veredicto.py` §A.

**R7 · A prosa da `LISTA_FINAL` e o registo executável nomeiam instrumentos
diferentes para o D8.**
A prosa: «*Confirmado por:* instrumento genuinamente independente — a química
não sabe nada de NDVI». O `registo_de_factos.py`:
`instrumento="pH(H2O)…"`, `confirmar_com("série óptica do B1 (Landsat 100 cenas
+ Sentinel-2)")`. **O confirmador é o NDVI.** A frase da prosa lê-se como se a
química fosse o confirmador, e é o contrário.

---

## REJEITADO

**X1 · «A acidez do solo não acompanha o declínio.» O D8 cai inteiro — por seis
vias independentes, e bastava uma.**

**(a) O número que ele cita foi rejeitado ontem à noite.** Datas NTFS,
`ctime = mtime` nos dois:

| ficheiro | criado |
|---|---|
| `b1_como_unidade.json` (donde sai o `+0,0921`) | 03-09 **22:45:32** |
| `B1_CONTROLO3_ADVERSARIO.md` — X1, que o rejeita | 03-09 **23:07:55** |
| `guarda.py`, reescrito em resposta | 03-09 **23:10:23** |
| **`a2_solo_caracterizacao.py`, que o volta a citar** | **04-09 08:28:02** |

O X1 de ontem mostrou que o critério que produz o `+0,0921` **imprime a mesma
frase com o acontecimento inteiro injectado**, e que o piso de detecção é 2,1×
o degrau procurado. A `LISTA_FINAL` de hoje **incorporou** a outra conclusão do
mesmo relatório (o eixo média/mediana, no A3) e **não incorporou esta**. Ficou a
metade que qualificava o A3 e saiu a metade que retirava o número — e o número
saiu a confirmar um facto novo.

**(b) Usa o B1 como comparador de não-declínio.** A `LISTA_FINAL`, secção E,
retirada 18: «*O B1 é o comparador sem degrau*». A `LISTA_FINAL`, secção F, o
que não se pode escrever: «*que o B1 é comparador de coisa nenhuma*». O D8, na
secção D da mesma página: «*os dois pH mais baixos são do B1, **que não
declina***». É a retirada 18 revivida com outro instrumento a montante.

**(c) A probabilidade, calculada exactamente — Q1.**
Enumerei as C(9,3) = 84 atribuições possíveis:

| | valor exacto |
|---|---|
| P(os dois mais baixos serem ambos de um grupo fixo de 3) | **7/84 = 1/12 = 0,0833** |
| P(esse grupo conter o mínimo **e** o máximo) | **7/84 = 1/12 = 0,0833** |
| Mann-Whitney exacto, B1 contra o resto, unilateral «mais ácido» | **21/84 = 0,2500** |
| o mesmo, colapsando a pseudo-réplica do V7 (n = 8) | **0,2857** |

**A coincidência que o D8 não conta é exactamente tão provável como a que
conta.** Os postos do B1 são **1, 2 e 9**: o grupo ocupa os dois últimos lugares
e o primeiro. O B1 abrange **5,2 a 7,4**, que é o intervalo inteiro dos nove.
Perguntar o que significa «a acidez não acompanha» quando o grupo cobre todo o
intervalo é a pergunta certa, e a resposta é: **não significa nada**. Um grupo
que contém simultaneamente o solo mais ácido e o solo mais básico da exploração
não é evidência sobre acidez em direcção nenhuma.

**(d) O sinal é 1,3 a 1,6 vezes o ruído do próprio instrumento.** A repetição no
mesmo talhão (R1) dá 0,2 unidades de pH; o intervalo que o D8 usa — do 5,3 do
B1 C4 ao 5,6 seguinte — é 0,3. Em concentração de H⁺: ruído 1,58×, sinal 2,0×.
O **S9 da `CAMADA_1_CERTIFICADO`** já tinha escrito a regra: «*nenhuma diferença
química entre blocos abaixo de um factor de 2 é interpretável com estes
dados*».

**(e) Restringindo aos boletins que TÊM posição, a relação inverte-se — e
inverte-se perfeitamente.** Quatro unidades distintas, com o `pct_defice_2026`
da unidade em que a C3 as colocou:

| unidade | pH | défice 2026 | d(foco) |
|---|---|---|---|
| Erica Novo (R 7,2 · E 6,6) | 6,90 | 2,8 % | 219 m |
| B4 | 6,10 | 6,2 % | 379 m |
| v7 / B2 (mar 5,8 · jun 5,6) | 5,70 | 21,2 % | 120 m |
| **B3** | **5,60** | **46,9 %** | **67 m** |

**Spearman(pH, défice) = −1,000**, monotonia perfeita, p unilateral exacto
**1/24 = 0,0417** sobre as 24 permutações.

**Não estou a afirmar que a acidez causa o declínio** — n = 4, e a atribuição
passa pela válvula. Estou a afirmar que **a mesma tabela de nove boletins
sustenta a leitura oposta à do D8 assim que se retiram os três únicos boletins
sem posição nenhuma**, que são precisamente os que o registo proíbe usar como
comparador. Uma afirmação cujo **sinal** depende de incluir ou não o único grupo
proibido não é um facto: é uma corrida preferida de uma distribuição de duas.

**(f) A partição está confundida com o lote de laboratório** (R4).

*Ficheiros:* `c3a2_03_q1_probabilidade.py`, `c3a2_05_multiplicidade.py`,
`c3a2_11_inversao.py`, `c3a2_12_lote.py`.

---

**X2 · «Hipótese pré-registada que só podia falhar.» A honestidade da declaração
não está em causa; a afirmação sobre o desenho está errada, e a redacção excede
o que o desenho permite.**

Era a pergunta 2, e tem duas partes.

**A primeira é aritmética.** «Só podia falhar» é apresentado como propriedade do
desenho. Não é. Com 9 boletins e um grupo de 3, o p unilateral mais pequeno
atingível é **1/84 = 0,0119** — sai se e só se os três boletins do grupo forem os
três valores mais baixos. **O desenho tinha um ramo de confirmação a p = 0,012 e
ele não foi accionado**, porque o terceiro boletim do B1 é o maior dos nove.
O que era impossível não era confirmar: era confirmar *com estes valores*.
«Só podia falhar» é uma propriedade da interpretação que se decidiu dar-lhe.

**A segunda é a redacção, e é a pergunta que foi feita: o D8 está a ser lido
como prova?** Está. Na `LISTA_FINAL` ele aparece **na secção D, entre os
sobreviventes**, com a estrutura tipográfica de um achado:

> **D8 · A acidez do solo não acompanha o declínio.** […] **Falsificada.**
> *Confirmado por:* instrumento genuinamente independente — a química não sabe
> nada de NDVI.

A linha «*Confirmado por:*» é **a mesma linha que o A1 e o A2 usam**, e é o que
distingue, em toda a peça, um facto com instrumento independente de um facto sem
ele. Um resultado nulo com n = 8 recebe a marca reservada aos dois factos mais
fortes do caso. E a ressalva que vem a seguir — «*e não se lê ao contrário: com
n = 9 e sem coordenadas*» — repete o «sem coordenadas» que o R2 acabou de
corrigir.

**O que se pode escrever, e é tudo:** *«O pH dos oito talhões amostrados vai de
5,2 a 7,4. As três amostras do B1 ocupam simultaneamente os dois valores mais
baixos e o mais alto do conjunto (postos 1, 2 e 9), pelo que não sustentam
leitura nenhuma sobre acidez. Os dois blocos que contêm os focos têm pH 5,6 e
5,8, e o laboratório prescreve calcário a ambos.»*

---

**X3 · «Só o pH foi olhado.» Corri os doze — e o pH é o ÚNICO parâmetro em que
os blocos dos focos não estão no extremo. Mas nenhum sobrevive à
multiplicidade, e é isso que é reportável.**

Era a pergunta 5, e a resposta tem as duas metades que ela previa.

**A metade pior.** Posto de cada boletim entre os nove (1 = o valor mais baixo),
e o teste de permutação exacto para «os três boletins dos blocos com foco são os
mais baixos»:

| parâmetro | B3 (foco E) | B2-V7 mar | ρ(défice) | p exacto |
|---|---|---|---|---|
| **Cálcio (CaO)** | **1,0** | **2,0** | **−0,883** | **0,0476** |
| **Razão C:N** | **1,0** | 3,0 | −0,441 | **0,0476** |
| Enxofre (S) | 2,0 | **1,0** | −0,313 | 0,0714 |
| Magnésio (MgO) | **1,0** | 2,0 | −0,618 | 0,0833 |
| Fósforo (P₂O₅) | **1,0** | 4,0 | −0,265 | 0,3571 |
| Matéria orgânica | 1,5 | 4,0 | 0,000 | 0,3810 |
| Manganês (Mn) | 4,0 | 4,0 | −0,135 | 0,4167 |
| Potássio (K₂O) | 2,0 | 8,0 | +0,177 | 0,7143 |
| Azoto total (N) | 7,5 | 5,5 | +0,409 | 0,8452 |
| Ferro (Fe) | 5,0 | 6,0 | +0,794 | 0,9167 |
| **pH (H₂O)** | 3,5 | 5,0 | −0,940 | **0,2500** |

**O `B3 - 7 ha` — o bloco do foco oriental, 46,9 % de défice, 67 m do centro — é
o posto 1 de nove em CaO, MgO, C:N e P₂O₅, e 1,5 em MO.** Isto **já estava
certificado**: é o **S8 da `CAMADA_1_CERTIFICADO`**, «o bloco do foco ESTE tem o
solo mais pobre da exploração, mínimo de nove boletins em cinco de sete
parâmetros», confirmado ali pelo SAR e pelo MDT. **O D8 foi publicado a dizer
que a química não acompanha o declínio, sobre uma tabela cujo mínimo em cinco
parâmetros é o bloco do foco, e num dossiê que já tinha isso certificado.**

**A metade que me obriga a não promover nada.** Onze parâmetros do mesmo tubo
não são onze testes. Construí o nulo que respeita a correlação — permutar o
**rótulo de bloco uma vez** e recalcular os onze, 84 permutações, todas
enumeradas:

| grupo | p mínimo | parâmetros com p ≤ 0,05 | **p GLOBAL** |
|---|---|---|---|
| os três boletins dos focos | 0,0476 | 2 de 11 | **0,286** (pelo mínimo) · **0,095** (por acertos) |
| **o B1 — o grupo do D8** | 0,2500 | **0 de 11** | **0,833** |

Na distribuição nula, **6 das 84 escolhas de três boletins conseguem 2 acertos e
duas conseguem 4** — e as duas melhores contêm ambas o `B3 - 7 ha`. **O grupo
dos focos nem sequer é o melhor dos 84.**

**O que se pode escrever, medido:** *«Dos doze parâmetros, o pH é o único em que
os blocos dos focos não ocupam posição extrema; em CaO, MgO, C:N e P₂O₅ o bloco
do foco oriental é o mais baixo dos nove. Nenhuma destas separações sobrevive à
correcção para os onze parâmetros (p global 0,29 pelo mínimo, 0,10 pela contagem
de acertos), e a do B1 não sobrevive sequer sem correcção (p = 0,25). Com este
n, a química não distingue em direcção nenhuma — e o D8 publicou uma
direcção.»*
*Ficheiros:* `c3a2_04_q5_doze.py`, `c3a2_05_multiplicidade.py`.

---

## NÃO TESTÁVEL

**N1 · Se a profundidade está declarada nos boletins originais.**
Os nove PDF não estão nesta máquina — procurei em `Downloads`, `Documents` e
`Desktop`, zero de nove. Só existem duas extracções em Excel e o CSV derivado
delas, e uma das extracções assinala **nove células como «page 2 not
extracted»** nestes mesmos boletins. **Não decido, e ninguém decide com o que
está em disco.** Fica como não sabido, não como ausência.
*Teste que decidiria:* pedir os nove PDF ao laboratório ou ao gestor. Custo
nenhum. É a mesma fila em que está a linha da PSA.

**N2 · Qual parcela do IFAP é o «B1 C1», o «C3» ou o «C4».**
Nada no corpus liga um número «C» a uma válvula, a um polígono ou a uma
coordenada. A única ligação é o prefixo do rótulo. E o registo tem o
contra-exemplo: a **R2 G35** enumera oito parcelas soltas «com área e sem
posição» e **duas delas chamam-se B1C5 e B1C6**. A numeração «B1 Cn» da
exploração inclui parcelas cuja posição o próprio dossiê declara desconhecida.
A tabela de colocação da C3 escreve-o como nota — `"B1 C1": (…, "sub-parcelas do
B1 sem posicao")` — e «sub-parcelas do B1» é a conclusão, não o dado.
*Teste que decidiria:* perguntar ao gestor a que válvula corresponde cada C.
Testemunho de tipo 1, custo nenhum, e ganha a qualquer cálculo nosso.

**N3 · Se a química do solo difere entre afectado e não afectado.**
É a pergunta que motivou tudo isto, e continua em aberto — mas agora está
medida em vez de suposta: n = 8 talhões, 4 com posição, nenhuma partição
sobrevive à multiplicidade em nenhuma das duas direcções.
*Teste que decidiria:* colheita emparelhada com GPS, dentro e fora dos discos de
90 m, **mesma profundidade declarada e mesmo lote de laboratório**. Os três
controlos que faltam a este conjunto são exactamente os três que R4, R6 e N2
identificam.

**N4 · Se o «B1 C1» é o mesmo solo que o «B1 C3» e o «B1 C4».**
CaO 4700 contra 439 e 314 — **factor de 11 a 15 dentro do mesmo «bloco»**; MO
4,5 % contra 2,1 e 1,7; MgO 242 contra 79 e 81; pH 7,4 contra 5,2 e 5,3. Ou o
C1 foi calcareado, ou não é o mesmo sítio. O S9 da C1 já registara este trio.
**Enquanto isto não fechar, «o B1» não é uma unidade química.**

---

## LINE-STOP

**L1 · A condição 2 do `guarda.py` aceita qualquer cadeia de caracteres como
instrumento independente. Corri-a.**

Reconstruí o D8 exactamente como está no `registo_de_factos.py` e troquei só o
confirmador:

```
--- T1a · confirmador substituido por 'contagem de nuvens em 1997'
VEREDICTO: hipotese pre-registada que so podia falhar
  instrumento    : pH(H2O) em 9 boletins - quimica, nao optica
  confirmado por : contagem de nuvens sobre Braga em 1997 - os dois pH mais
                   baixos, 5,2 e 5,3, sao do B1, que SOBE +0,092 [...]
  *** PASSOU ***
```

**Saída idêntica à do confirmador real.** A condição 2 verifica que foi passada
uma cadeia e que o booleano `concorda` é verdadeiro. **Não tem noção nenhuma do
que o confirmador mediu, nem de se ele confirma o facto em vez de lhe fornecer
uma premissa** — e é isto que o D8 faz. A frase tem duas metades:

- (a) *os dois pH mais baixos, 5,2 e 5,3, são do B1* ← química;
- (b) *o B1 não declina* ← NDVI.

O confirmador não está a repetir (a) com outra física. **Está a fornecer (b).**
Não há corroboração: há uma premissa contada como confirmação.

E a reescrita de ontem à noite não fecha isto. O bloqueio de índice igual que o
`veredicto()` ganhou às 23:10 **só dispara quando o instrumento DO FACTO contém
NDVI/NDMI/NDRE/EVI/SAVI/NDWI**. O do D8 é química, por isso a regra nem chega a
ser avaliada — verifiquei, com o confirmador renomeado para «NDVI Landsat +
NDVI Sentinel-2»: **passa**. Isso está certo para o caso geral, química
confirmada por óptica **é** cruzamento de físicas. Não está certo aqui, porque o
que a óptica confirma não é o pH.

**A correcção mínima:** `confirmar_com()` tem de exigir **qual das afirmações do
facto o confirmador replica**, e bloquear quando essa afirmação é uma premissa e
não a conclusão. Enquanto for uma cadeia livre, a condição 2 é a mesma promessa
em prosa que o ficheiro foi escrito para substituir — é a terceira encarnação do
mesmo erro, depois da frase da condição 5 e do ficheiro da condição 5.
*Ficheiro:* `c3a2_07_portao.py` §T1, §T2.

---

**L2 · O `instantanea()` isenta a condição 5 pelo instrumento DO FACTO e não
olha para o que entrou pelo `confirmar_com`. O D8 é instantâneo e importa uma
comparação de dez anos.**

O D8 assina «*pH de uma colheita, sem série*» e com isso dispensa a condição 5.
A proposição que publica — «o B1 **não declina** enquanto os focos descem» — é
uma comparação de 2017-24 contra 2025-26 sobre seis parcelas. **A parte que não
precisa da condição 5 é a que ele declara; a parte que precisa entrou pela
porta que não a interroga.**

Prova, corrida: se a condição 5 fosse aplicada às unidades que a frase usa —

```
T3 · D8 temporal, com as SEIS parcelas do sector B1
  VEREDICTO BLOQUEADO
  · a unidade MUDOU no intervalo comparado (reg01_triagem.json, 39 unidades)
    - EXCLUIDA pelo rastreio: 8845729, 8845739
  >>> BLOQUEOU

T3 · D8 temporal, com as QUATRO que a triagem manteve
  >>> PASSOU
```

**O facto muda de veredicto conforme quem declara as unidades**, e quem as
declara é quem escreve o facto. E o adversário de ontem já tinha mostrado que
uma dessas quatro (`6476425`) é mato convertido depois de 2018 e não tem linha
de base de kiwi nenhuma.

**A correcção:** `confirmar_com()` tem de aceitar uma marca de temporalidade, e
um confirmador temporal tem de **arrastar consigo a condição 5** com as unidades
que usa — mesmo que o facto se declare instantâneo. Um facto não pode ficar
isento por uma propriedade da sua própria metade e importar a outra metade
isenta.

E fica dito para o registo: **o `instantanea()` do D9 é legítimo; o do D7 é
legítimo na letra e a razão assinada está errada** — «cada boletim é uma data
única; não há série a comparar» é falso, porque o V7 tem duas datas (R1).
*Ficheiro:* `c3a2_07_portao.py` §T3, §T4.

---

**L3 · Nada neste aparelho repara que um NÚMERO citado foi retirado.**

O `certificar.py` tem sete verificações. A terceira garante que «nenhum
documento vivo cita um documento **retirado**». Não há verificação nenhuma sobre
**quantidades** retiradas. Por isso o `+0,0921` — rejeitado às 23:07 de ontem,
com o piso de detecção medido a 2,1× o acontecimento procurado — atravessou a
noite, entrou no `registo_de_factos.py` às 08:40 de hoje como nota do
`confirmar_com`, e passou o portão inteiro.

É a assimetria que interessa: **o mesmo relatório do Controlo 3 foi lido e
incorporado em parte**. O eixo média/mediana entrou no A3 da `LISTA_FINAL` como
«incerteza 2 — eixo novo, achado a 03-09 pelo Controlo 3». O X1 do mesmo
relatório, que retirava o número, não entrou — e o número foi usar-se como
confirmador de um facto novo. Não alego intenção nenhuma: alego que **não existe
nada que impeça isto, e que aconteceu em nove horas**.

**A correcção, e é do mesmo tamanho das outras:** um `retirados.json` com as
quantidades retiradas, o ficheiro que as produziu e a data; e uma oitava
verificação no `certificar.py` que varre o `registo_de_factos.py` e a
`LISTA_FINAL` à procura delas. Custo: um ficheiro e vinte linhas.

---

## NOTA DE MÉTODO

Treze scripts, em `_VALIDADE_GESTAO\_controlo3_a2\`:

| | ficheiro | o que decide |
|---|---|---|
| 00 | `c3a2_00_dados.py` | leitura crua, sem o filtro do alvo; os 9 ficheiros-fonte |
| 01 | `c3a2_01_campos.py` | os 22 campos, valor a valor — donde sai o `Notes` vazio |
| 02 | `c3a2_02_matriz.py` | a matriz 9 × 12, com os valores crus e as censuras |
| 03 | `c3a2_03_q1_probabilidade.py` | **Q1** — as 84 combinações, exactas |
| 04 | `c3a2_04_q5_doze.py` | **Q5** — os doze parâmetros, postos, ρ e p |
| 05 | `c3a2_05_multiplicidade.py` | o nulo com correlação; **a repetibilidade do V7**; a data |
| 06 | `c3a2_06_q3_identidade.py` | **Q3** — o IFAP contra o eixo do gestor; os +40 % |
| 07 | `c3a2_07_portao.py` | **Q6** — o portão reconstruído e os seis ataques |
| 08 | `c3a2_08_q4_profundidade.py` | **Q4** — os cinco campos, os dois livros, os PDF |
| 09 | `c3a2_09_extraccao.py` | o CSV contra a folha de origem, 108 células |
| 10 | `c3a2_10_veredicto.py` | o F2 replicado; o D7 contra o ficheiro que cita; o piso de p |
| 11 | `c3a2_11_inversao.py` | **a inversão nos seis colocáveis**, ρ = −1,000 |
| 12 | `c3a2_12_lote.py` | o MnAI, e os dois lotes de laboratório |

**Falhas técnicas, para o registo:** uma. O bloco (d) do `c3a2_03` colapsava a
pseudo-réplica mal na primeira versão — removia um elemento e acrescentava
outro, mantendo n = 9. Apanhei-o porque a saída imprimia «n = 9 talhões» depois
de a linha acima dizer que ia colapsar dois: **contar o que a saída diz, não o
que se espera**, §7 do `ANTES_DE_COMECAR`. Corrigido e reimpresso; não afecta
nenhum outro número. A consola cp1252 mutilou acentos na saída impressa, sem
afectar cálculo nenhum.

**O que não fiz.** Não descarreguei nada. Não abri os nove PDF, porque não
existem nesta máquina, e digo-o em vez de inferir a partir da sua ausência. Não
corri o `reg01_triagem_descontinuidade.py` — não comparei parcelas em série; a
única série que uso é a que o D8 cita, e essa está julgada. Não corri o
`certificar.py`: alterar a `LISTA_FINAL` não é trabalho de adversário. Não
escrevi nada fora de `_controlo3_a2\`.

---

**Nota final.** Vim procurar o erro e a instrução era dizê-lo com a mesma
clareza se os factos resistissem. **Um resiste em parte, um resiste na conclusão
e em nenhuma das razões, e um cai.**

O D9 divide-se limpo: a CTC e a saturação em bases faltam mesmo, verificado a
montante; a profundidade não está no CSV porque o CSV não tem onde a pôr, e o
que se pode dizer sobre o documento original é **nada**, porque ele não está cá e
há prova impressa de que uma página ficou por ler.

O D7 acerta na conclusão e falha nas três razões, uma das quais é um zero
escrito à mão sobre um ficheiro que diz seis.

O D8 é um resultado nulo com n = 8, num grupo que ocupa simultaneamente os
postos 1, 2 e 9, com um sinal de 1,5× o ruído medido do próprio laboratório,
confundido com o lote de colheita, publicado com a marca tipográfica reservada
aos factos com instrumento independente — e o seu confirmador é o número que
este mesmo Controlo 3 retirou nove horas antes. **Restringido aos boletins que
têm posição, o sinal inverte-se perfeitamente.**

E o que fica maior do que o A2 são as duas portas. **A condição 2 aceita
«contagem de nuvens sobre Braga em 1997» como instrumento independente** — corri
e passa. E **o `instantanea()` deixa um facto declarar-se sem tempo e importar
uma série de dez anos pela porta ao lado**, sem que a condição 5 seja alguma vez
chamada. O portão foi reescrito três vezes por causa da condição 5. Esta é a
condição 2, e é a mesma forma de erro: **verificar que alguma coisa foi
declarada, em vez de verificar o que ela diz.**
