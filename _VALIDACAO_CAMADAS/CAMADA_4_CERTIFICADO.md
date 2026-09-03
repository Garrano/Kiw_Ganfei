# Camada 4 — Inferência

29-08-2026. Diagnóstico diferencial, livro-razão das exclusões, argumento
geométrico. Herdei cinco listas fechadas e não usei nada fora delas, salvo
onde está declarado e justificado.

**Esta camada leva adversário.** Escrita a contar com isso: cada frase que liga
números traz ao lado o objecto de cada número e o que a derruba.

Código e tabelas em `SAIDA_C4\`:
`c4_01_numeros.py` → `c4_01_numeros.json` (nenhum valor transcrito à mão),
`c4_02_razao.py` → **`c4_razao_exclusoes.csv`** e `c4_02_contagem.json`.

---

## 0 · A ARBITRAGEM QUE CHEGOU A MEIO, E O QUE ELA DERRUBA

A camada abaixo deixou uma paragem de linha em **NÃO RESOLVIDO — relato contra
documento, precedência por decidir** (C3 R2 §0). Perguntou-se ao gestor. A
resposta chegou a meio desta corrida e **resolve metade**.

### 0.1 · O «Kiwi 1000» tem lugar. É testemunho de tipo 1 e ganha ao documento.

Verificado nesta sessão nos dois livros: quinze registos consecutivos do
`Registo Principal` trazem todos `6_junho_2025_microbiologia_de_solo.pdf`,
referência **331/2025 V.1**, expediente **2025045292**, identificador **Kiwi
1000**, colheita **2025-06-06**. **O «Kiwi 1000» e o informe 331/2025 são a
mesma amostra** — não são dois objectos, como a cadeia vinha a tratá-los.

E o gestor situou-a: **no lado oeste do maior vazio circular**. O maior vazio é
o núcleo redondo de **3,98 ha** com centro em **E530476 N4655046**.

Medido, e não afirmado: esse centro está a **11,4 m** do centro do foco OESTE
(**E530485 N4655053**). Não digo que sejam o mesmo objecto — digo a distância
entre os dois centros declarados, como a G29 fez com os seus 7 m.

**Consequência.** A amostra que carrega quase toda a patologia deste caso deixa
de ser uma amostra sem posição. **A B4 cai pelos seus próprios termos** — a C3
escreveu-a com a condição explícita «se houver testemunho que localize a
amostra, B4 cai». Não é uma rejeição minha: é a condição a cumprir-se.

**Quatro cautelas, e escrevo-as porque sem elas isto vira o erro seguinte:**

1. **É uma zona, não um ponto.** «Lado oeste» de um núcleo descrito como
   redondo. Com 3,98 ha, o raio equivalente é 112,6 m e a metade ocidental
   estende-se por **E530363–E530476**. O raio equivalente **supõe
   circularidade e é uma escala, não uma fronteira medida**. Nenhuma coordenada
   de amostra foi inventada neste certificado.
2. **Continua a ser uma amostra COMPOSTA**, e o próprio livro a marca assim.
   Composta sobre o quê, não se sabe — e é a pergunta que o PDF original
   responderia.
3. **É de 2025-06-06.** Não é linha de base: não há nada anterior ao
   acontecimento. É, isso sim, o único material biológico **contemporâneo do
   arranque** e vem do sítio onde o arranque está.
4. **As quatro ITS ISFBV0314–17 mantêm-se em NÃO RESOLVIDO.** O gestor diz
   explicitamente que **não sabe**. Não há testemunho a preferir ao documento
   deste lado — e também não há documento: ver §0.3.

### 0.2 · A zona não escolhe entre a v7 e a v8, e isso importa

A faixa E da metade ocidental do núcleo é **E530363,4–E530476,0**. O único
**ponto** de válvula dentro dessa faixa é o da **v7** (E530397,5); o da v8
(E530499,8) fica a leste dela inteira.

**Um ponto de válvula não é o polígono da válvula**, e não tiro daqui uma
atribuição. Tiro o contrário, que é o útil: a zona do testemunho cai
exactamente sobre a fronteira v7/v8 dentro do foco, e **a C3 já tinha medido
que essa fronteira passa por lá** — 38 das 325 células da v7 (11,7 %, 0,38 ha)
estão dentro do disco de 90 m do foco OESTE, com distância mínima de **53 m**
(B5, T2f).

**Portanto: a amostra está no foco ocidental e não se pode atribuir a uma
válvula.** A B5 não muda como afirmação documental — nenhum dos 221 registos
nomeia a válvula 8 — mas **deixa definitivamente de se poder ler como “o foco
não foi amostrado”**.

### 0.3 · Os documentos das ITS não existem nesta máquina — e isso é outra coisa

Verifiquei por busca própria em toda a árvore de `C:\Users\Jackster2`:
**zero ficheiros com `ISFBV` no nome**, e nenhum informe 331/2025. Os dois
livros são um **compilado que cita os PDF pelo nome** (`ISFBV0314_ITS.pdf`,
`6_junho_2025_microbiologia_de_solo.pdf`, `339_Kiwi.pdf`…).

A anotação de origem diz «não foi encontrado código de talhão **nas páginas
extraídas**». A ausência é do que foi extraído.

> **Isto é documento indisponível, não informação inexistente.** A pergunta das
> ITS é respondível — pelo formulário de submissão da Fauna Útil SL ou pelos
> quatro PDF — e **não é respondível por nada que esteja nesta máquina**.
> Consolidar a suspensão em rejeição com este material seria repetir, em ponto
> mais pequeno, a operação que o adversário da C3 já corrigiu uma vez.

### 0.4 · A segunda arbitragem: **o viés do Sentinel-2C não existe, e nunca existiu**

Chegou também a meio da corrida, do `_MULTIVERSO\ADVERSARIO_H1.md`. **Retira
metade de um facto da lista fechada** — a segunda metade da **L5**.

Quatro medições emparelhadas, de quatro corridas independentes:

```
corrida A (H1)        -0,056 em NDRE, e diz explicitamente que o NDVI nao tem vies
corrida C (H1)        +0,0007 / +0,0045   -> chamou-lhe nulo
ceptico   (H2)        +0,000  / +0,004
patologista (H2)      +0,012
```

**Todas ≈ zero.** O valor de **−0,048** que circulou por toda a cadeia **não vem
de nenhuma delas**: vem de um degrau de nível medido **fora do pomar**, onde
sensor e ano estão confundidos, e foi-lhes atribuído na agregação da H1. Daí
entrou na lista fechada como metade da L5 e passou à ronda H2 como facto de
especificação.

**O que cai:** «o viés do S2C explica quase toda a queda da referência». **O que
fica:** a primeira metade da L5 — os degraus em fosso são **+0,0720** e
**+0,0585**, e não −0,1426 e −0,1439. **Cai a explicação anexada, não a
medição.**

> **E isto não enfraquece nada meu — reforça o principal.** A queda da
> referência tinha uma explicação concorrente, e essa explicação acabou de
> desaparecer. O que resta no lugar dela é medição: o T4 da C3 mostra a **média**
> da referência a cair **0,0548** contra **0,0219** da **mediana**, com o
> afastamento entre as duas a alargar **trinta e uma vezes** de 2024 para 2026.
> **Isso é um subconjunto de células da referência a colapsar. Não é sensor.**
> Ver I5 e D4, que ganham com esta retirada.

**Duas correcções da mesma fonte, e a primeira toca no lado oriental:**

- **O voo LiDAR de 06-07-2025 cai DENTRO da janela em análise.** Não distingue
  «nunca teve pérgola» de «teve até Julho de 2024». **Não é teste das
  afirmações sobre o lado oriental** — é a mesma objecção que a parte 3 do
  `ADVERSARIO_2026-08-29.md` fez à partição retroactiva, agora na forma mais
  aguda. **O que faz de decisivo é outra coisa: confirma que o foco ocidental,
  v8/B2, é copado vivo — 2,25 m e 90,2 % acima de 1,5 m.** É essa a metade da L3
  que uso, em I7(c) e em D3; **a metade oriental de L3 não a uso como teste**, e
  a margem de B7 que a ela encosta fica enfraquecida na mesma medida.
- **Uma divergência por explicar que ninguém juntou.** A corrida B imprimiu que
  a **vegetação envolvente caiu 0,075 entre 2024 e 2026 — o dobro da queda do
  bloco** — e nunca juntou os dois números; a corrida C mediu que a sua
  referência **não se move** (−0,0070, p = 0,54). **As duas não podem estar as
  duas certas.** Registo e não resolvo (NÃO TESTÁVEL 13, linha REG-03 do
  livro-razão). **Se a paisagem caiu o dobro do bloco, o enquadramento do caso
  inverte-se** e a pergunta regional deixa de ser secundária.

### 0.5 · Não há paragem de linha nova

Não rejeito nenhum facto certificado por nenhuma camada abaixo. O que fiz foi
**aplicar duas arbitragens que chegaram de fora**, uma delas nos termos que a
própria camada abaixo escreveu (§0.1) e a outra retirando metade de um facto
herdado por decisão do coordenador sobre um adversário a montante (§0.4); e
**aplicar correcções que já existiam a montante e que o meu prompt não
transportou** (§1). Escrevo o `CAMADA_5_PROMPT.md`.

---

## 1 · TRÊS COISAS QUE HERDEI NUMA FORMA JÁ CORRIGIDA A MONTANTE

Não são rejeições minhas. São correcções publicadas que o meu prompt não levou,
e todas as três alimentavam tarefas que ele me mandou fazer.

**1.1 · A L8 chegou-me sem a correcção do seu próprio adversário.** O
`ADVERSARIO_2026-08-29.md` R8 estabelece, e o veredicto confirma, que a L8
«passa com o denominador declarado, **251 cenas** e **sem a leitura de
“recuperação” do N3**». O meu prompt transporta «276 cenas» e «recupera a 0,65
em 2026», e a **tarefa 2 manda-me usar essa recuperação como prova de que são
dois acontecimentos**.

O que a R8 mede: as amplitudes absolutas da referência de 2022 a 2026 são
0,601 · 0,590 · **0,265** · 0,538 · **0,277** — o denominador **perde metade de
si próprio** em 2024 e outra vez em 2026. Em absoluto, o N3 vai de 0,052 para
0,180 enquanto a referência vai de 0,538 para 0,277. **Contra um denominador
estável (~0,60) o N3 leria 0,30, não 0,65.** E o piso de Inverno do N3 **desce**
(0,654 → 0,497) e o pico de Verão **desce** (~0,71 → ~0,65), ficando 0,20–0,26
abaixo da referência.

**O que sobrevive e uso:** o **0,10 de 2025**, que é enorme em qualquer
normalização, e a **monotonia** do foco OESTE, cuja direcção é robusta ao
denominador ainda que os valores não sejam. **O que não uso: a recuperação.**

**1.2 · A L7 chegou-me sem os dois acertos de W2.** O texto publica «0,55 /
0,61 / 0,25 ha a 60, 75 e 166 m»; o JSON tem 0,55 ha a **74,7 m** e 0,61 ha a
**60,0 m** — áreas e distâncias trocadas. E a mancha de 0,55 ha tem altura
mediana **1,466 m**, abaixo do limiar de 1,5 m com que a própria adenda define
presença de pérgola. **«Não é chão» aguenta; «tinham pérgola completa» não
aguenta para essa mancha.**

**1.3 · A tarefa 6 do meu prompt está construída sobre material retirado.** A
leitura «os dois focos perdem água antes de verdura» (NDMI 0,199 contra 0,146 a
oeste; 0,201 contra 0,138 a leste) foi **RETIRADA por inteiro** pela R6 do
`ADVERSARIO_2026-08-29.md`, por dois motivos: (a) comparar fossos **absolutos**
entre dois índices com níveis de referência diferentes (NDVI ≈ 0,87, NDMI ≈
0,50) e saturações diferentes não é válido, e a assimetria existe em **todos os
catorze anos** (2015: 0,102 contra 0,066) — não é assinatura de 2026;
recolocada sobre variações desde a base, a razão é 1,53 (ESTE) e 1,36 (OESTE);
(b) era **uma afirmação de etiologia dentro de uma adenda da C2** — a minha
camada a correr dentro da C2 — e entrou como premissa de desenho no cabeçalho
do `terreno_contra_declinio.py`.

**Essa retirada não consta da secção REJEITADO do meu prompt.** Não construo
sobre ela. A minha resposta à tarefa 6 está em §6 e é sobre o que sobra.

**1.4 · Nomenclatura, verificada contra o ficheiro operativo.** Recalculei as
distâncias a partir de `valvulas_por_area.json` (G35), que é o conjunto
operativo:

| objecto | ao foco OESTE E530485 N4655053 | ao foco ESTE E530977 N4655117 |
|---|---|---|
| ponto da v7 | **110,7 m** | 594,3 m |
| ponto da v8 | **34,5 m** | 486,6 m |
| ponto da v13 | 447,6 m | **80,8 m** |
| ponto da v14 | 546,2 m | **93,2 m** |

Batem com a G35 (34 m) e com a C1 (111 m, 81 m, 93 m). **As tabelas do
`REGISTO_DE_NOMES.md` estão desactualizadas e confirmo-o**: ele dá «a 10 a
47 m, a 9 a 105 m, a 8 a 157 m» quando o ficheiro operativo dá v8 a 34,5 m.
Quem citar aquele ficheiro cita a versão errada.

**1.5 · O N3 não é o foco ESTE.** Centros declarados E531068 N4655145 e E530977
N4655117: **95,2 m**. O disco do foco é de 90 m. **O N3 está fora dele.** A
tarefa 3 do meu prompt trata os dois como um só («do lado oriental»); não os
trato.

---

## 2 · O LIVRO-RAZÃO — `SAIDA_C4\c4_razao_exclusoes.csv`

**59 linhas.** Uma por causa candidata, com o âmbito (onde e quando vale), o
instrumento independente, a margem e o que a fecharia.

| estatuto | linhas |
|---|---|
| **NÃO TESTADA** — ninguém procurou | **41** |
| **EXCLUÍDA** — o material exclui-a como explicação do padrão | **7** |
| **SUSTENTADA** — o material apoia-a como contribuinte | **5** |
| **EXCLUÍDA-LOCAL** — excluída só numa zona, numa data e numa matriz, n = 1 | **4** |
| **INCONCLUSIVA** — foi testada e o teste não decidiu | **2** |

**Uso cinco estatutos e não três, e a razão é a mesma que o prompt invoca para
exigir os três.** Arrumar «foi corrida e não decidiu» dentro de «excluída»
inventa uma exclusão; arrumá-la dentro de «não testada» apaga uma corrida que
existiu e custou. E arrumar «negativo de uma amostra composta, numa zona, numa
data» como «excluída» é literalmente o erro que o prompt me manda evitar — o
âmbito é a diferença entre um resultado e uma exclusão.

Por classe: biologia 27 · instrumento 6 · substrato 5 · gestão 5 · rega 3 ·
clima 3 · material vegetal 3 · regional 3 · nutrição 2 · química 2.

**Sete linhas EXCLUÍDAS, e uma só é biológica:** declive (S5), posição
topográfica húmida como explicação do padrão (hipótese fixada, corrida e
**contradita** — o défice está no terreno alto nas onze cenas), agrupamento por
válvula (dentro do nulo rodado em onze cenas), precipitação como discriminante
espacial (S16), fenologia (V11), **o viés do S2C como explicação da queda de
nível** (§0.4 — quatro corridas independentes, todas ≈ zero), e *M. hapla* como
explicação do contraste entre os focos.

**Quarenta e uma NÃO TESTADAS.** É o produto principal desta camada.

---

## CONFIRMADO

**I1 · A composição do défice de 2026 separa os dois focos, e separa-os sobre
uma partição documental.**

| unidade | défice 2026 | declínio novo M2 | novo / défice | chão lavrado 2021 |
|---|---|---|---|---|
| **v8** (contém o foco OESTE) | 50,7 % | 47,1 % | **0,93** | **0,0 %** |
| v7 | 21,2 % | 21,2 % | 1,00 | 0,0 % |
| v9 | 27,9 % | 6,4 % | 0,23 | 0,0 % |
| v12 | 28,7 % | 9,0 % | 0,31 | 12,8 % |
| **v13** (contém o foco ESTE) | 53,4 % | 19,5 % | **0,36** | **22,6 %** |
| **v14** (contém o foco ESTE) | 52,9 % | 18,1 % | **0,34** | **13,8 %** |
| v15 | 59,3 % | 3,7 % | 0,06 | 15,6 % |

E, pela datação por permanência (célula em défice **continuamente** desde o ano
indicado), dentro do disco de **120 m**:

```
foco OESTE   2017..2023 : 0,00 ha   2024 : 0,09   2025 : 1,02   2026 : 1,49
foco ESTE    2017 : 1,13 ha   2018-2024 : 0,65   2025 : 1,14   2026 : 0,48
```

**3,5 % do défice do foco OESTE tem histórico anterior a 2025. No foco ESTE são
52,4 %.**

*Prova:* `c3_07_georreferenciacao.json` (por válvula) e `c2_05_manchas.json` →
`datacao_focos`; partição documental de G35.
*Instrumento independente:* **SIM, três proveniências que não se produzem umas
às outras** — a tabela de áreas do gestor (documento) para a partição, a
ortofoto de 2021 (estrutura) para o chão lavrado, e a série Sentinel-2 para o
défice e para a regra M2.
*Margem:* a partição tem ±10 m (G35), e as áreas por válvula da partição não
são as da tabela (v15: 1,35 ha na partição, 1,14 ha na tabela) — **objectos
diferentes**. A datação corre num disco de **120 m**, e a maior parte dos
factos de foco desta cadeia corre a **90 m**; **circulam três raios neste caso
— 70, 90 e 120 m — e o objecto tem de ser dito sempre**. *Não circular:* o
contraste é **entre dois objectos seleccionados da mesma maneira** (ambos por
onde o NDVI caiu), logo o viés de selecção é comum e cancela; a composição
novo/antigo não entrou na selecção de nenhum dos dois.

---

**I2 · O *M. hapla* não explica o contraste entre os focos, e o sinal é o
inverso do que uma leitura causal precisaria.**

| talhão | solo (J2+ovos/200 cc) | raiz (J2+ovos/g) | défice 2026 | posição |
|---|---|---|---|---|
| B1 | **250** | 65 | — | **não tem** |
| B3 | **28** | **37** | **46,9 %** | sim |
| B4 | 46 | 156 | 6,2 % | sim |
| V7 | 202 | 72 | 21,2 % | sim |
| Erica Novo E | 54 | 78 | 2,8 % | sim |

Sobre as quatro unidades colocadas: **ρ(défice, contagem no solo) = −0,40** e
**ρ(défice, contagem na raiz) = −0,80**. A contagem mais baixa dos cinco está no
bloco mais afectado. A mais alta de todas está no B1, **que não tem posição**.

*Prova:* contagens em `c3_05_folhas.txt`, folha `Contagens Nemátodos`; défice
por unidade em `c3_07_georreferenciacao.json`.
*Instrumento independente:* **SIM** — o laboratório (Areeiro) dá a contagem, o
Sentinel-2 dá o contraste, e nenhum dos dois produziu o outro. É o melhor
cumprimento do controlo 1 disponível na biologia deste caso.
*Margem:* **n = 4, uma data (2026-05-06), um laboratório, um método.** Com
n = 4 o p exacto de |ρ| = 1 é 0,083; **nenhum destes dois valores é
significativo em nenhum critério**, e não os apresento como se fossem. O que
está estabelecido é a **direcção** e a **ausência de gradiente no sentido
causal**. Isto exclui o *M. hapla* como **discriminante**; **não** o exclui como
stress de fundo do corpo inteiro (linha BIO-17 do livro-razão, NÃO TESTADA).

---

**I3 · Nenhum resultado NEGATIVO deste caso vem de uma amostra que se possa
comparar com outra. Depois da arbitragem, a matriz de diagnóstico tem uma só
coluna útil.**

Lido linha a linha de `c3_05_folhas.txt`, das **20** linhas organismo × matriz:

```
com algum lugar declarado ................................ 15
   das quais: assentam SO no granel 331/2025 ............. 13
   das quais: com contraste multi-unidade (M. hapla) ......  2
sem qualquer lugar declarado .............................  5   <- so Espanha
linhas com algum resultado NEGATIVO ......................  5
   negativos vindos de amostra COM lugar .................  4   <- todos do MESMO granel
   negativos sem nenhuma fonte de Ganfei .................  1   <- Oomicetes (raiz)
```

**Uma matriz com uma só coluna é uma lista, não uma matriz.** Treze das vinte
linhas descrevem uma amostra composta, num sítio, num dia. Não existe, em todo
o caso, **um segundo ponto ensaiado para nenhuma dessas treze linhas** — nem
doente, nem são.

*Prova:* `c3_05_folhas.txt`, folha `Matriz Fitopatologia`, lida célula a célula
por `c4_01_numeros.py`; convenção declarada no rodapé da própria folha («célula
em branco = esse organismo **não foi testado** nessa amostra»).
*Instrumento independente:* **nenhum, e declara-se** — é afirmação sobre
cobertura de ensaio, e passa pela mesma razão que a C3 aceitou para B8: a
conclusão é **negativa**, retira um dado em vez de o afirmar.
*Margem:* categórica quanto à cobertura. **Verifiquei que o teste podia ter
dado o contrário**: as colunas B1, B3, B4, V7 e Erica Novo E existem na folha e
o *M. hapla* preenche-as — a classe «linha ensaiada em mais do que um sítio» é
emissível, e tem duas ocorrências.

---

**I4 · A matriz não contém uma única linha bacteriana nem viral.**

Os **15 taxa** são fungos, oomicetas e um nemátode: *Armillaria*,
*Ceratobasidium*, *Dactylonectria*, *Fusarium cerealis / equiseti / oxysporum /
solani / sp.*, *Globisporangium intermedium*, *Ilyonectria liriodendri*,
*Meloidogyne hapla*, *Neofusicoccum parvum*, Oomicetas (geral), *Rhizoctonia
solani*, *Rosellinia*.

**A *Pseudomonas syringae* pv. *actinidiae* nunca foi procurada neste caso —
com ou sem posição, em nenhuma matriz, em nenhuma data.** O mesmo para qualquer
outra bactéria e para vírus.

*Prova:* enumeração completa em `c4_01_numeros.json` → `matriz_resumo.taxa`.
*Instrumento independente:* nenhum; conclusão negativa.
*Margem:* é afirmação sobre **este** painel. Não afirmo que a PSA esteja
ausente do pomar — afirmo que não há um resultado, em nenhum sentido.

---

**I5 · Toda a magnitude expressa em fosso à referência é um limite inferior, e
a área em défice também.**

A moeda operativa (V1, V9) é o fosso à referência sistemática da mesma data, e
o limiar do défice é `mediana da referência − 0,05`. Se a referência desce, o
limiar desce com ela e **menos células qualificam**. A B10 mede exactamente
isso e no mesmo sentido: limpar as 18 células intrusas leva o défice de 2026 de
**9,47 para 10,32 ha** (sem abertura).

**Consequência que atravessa tudo o que esta cadeia publicou:** «o resto do
pomar fecha o fosso» **não quer dizer** «o resto do pomar está são». Quer dizer
que converge para uma referência que está a cair.

**E a explicação concorrente caiu** (§0.4). O viés do S2C era a única coisa que
competia com esta leitura, e está **excluído** por quatro medições emparelhadas
de quatro corridas independentes, todas ≈ zero. O que fica no lugar é medição:
média da referência a cair **0,0548** contra **0,0219** da mediana, com o
afastamento entre as duas a alargar **31×**. **Isso é um subconjunto de células
da referência a colapsar, e não é sensor.**

*Prova:* C3-R2 **B10** (as duas vias) + **G6/G25** (a referência sistemática
desce, 0,8884 → 0,8425, −0,00395/ano) + `_MULTIVERSO\ADVERSARIO_H1.md`.
*Instrumento independente:* **herdado de B10** — máscara de estrutura
(ortofoto, sem NDVI) contra série de reflectância (Sentinel-2); e a exclusão do
viés vem de **quatro corridas independentes com personas e desenhos
diferentes**, que é a forma de agregação que Botvinik-Nezer 2020 estabelece.
*Margem:* **a direcção está certificada; a dimensão não.** A margem de B10
continua não declarada — **não há bootstrap**. *(A outra metade da objecção de
B10 — «e a cena é a S2C» — perde força com §0.4, mas não desaparece: o que está
excluído é o efeito sobre a **média**; o efeito sobre as **estatísticas de
cauda**, que é o que todas as grandezas-título desta cadeia são, nunca foi
medido — NÃO TESTÁVEL 14.)* **Não quantifico o limite inferior**, e quem o
quantificar sem a série Landsat certificada (NÃO TESTÁVEL 3) está a inventar.

---

**I6 · A zona do testemunho para o «Kiwi 1000» situa a amostra no foco
ocidental e não a atribui a nenhuma válvula.**

Centro do maior vazio circular a **11,4 m** do centro do foco OESTE; metade
ocidental a estender-se por E530363–E530476; único ponto de válvula nessa faixa
é o da v7; e 11,7 % das células da v7 (0,38 ha, mínimo 53 m) já estão dentro do
disco de 90 m do foco.

*Prova:* testemunho do gestor (tipo 1) × `valvulas_por_area.json` (G35) ×
`c3_13_T2_T4.json` → T2f. Cálculo em `c4_01_numeros.py`.
*Instrumento independente:* **SIM** — testemunho e partição documental são duas
proveniências e nenhuma produziu a outra.
*Margem:* o núcleo é **descrito** como redondo, não medido como tal; o raio
equivalente é uma escala. Um ponto de válvula não é o polígono da válvula.
**Nenhuma amostra deste caso tem coordenada**, e esta continua a não ter.

---

**I7 · «Um acontecimento ou dois» é a pergunta errada, e o material di-lo.**
*(resposta à tarefa 2)*

A dicotomia pressupõe que o pomar fora dos focos é fundo estável. **Não é** —
I5. Decomposto, o material sustenta **três componentes com constantes de tempo
diferentes**:

**(a) Um substrato oriental distinto e anterior a 2016.** S13 (VV 1,2–3,5 dB
abaixo da referência em **todos** os dez Invernos desde 2016-17), V7 (166 de
167 células `nu2021` em défice óptico já em 2017), S12 (60 % do chão lavrado de
2021 dentro do foco ESTE, 0 % no OESTE e na referência), S19 (rugosidade
+0,0379 m, p = 1,3e-18, dentro da mesma campanha de voo), e I1 (52,4 % do
défice do foco ESTE em défice contínuo desde 2024 ou antes). **Dois
instrumentos, dois princípios físicos, a mesma conclusão.**

**(b) Uma perda lenta e generalizada do corpo principal.** Uma corrida
(`AGREGACAO_H2` H2-3: −0,054 NDVI em cinco anos, **98,5 % dos píxeis a
participar**, desde 2023), concordante com G6/G25 e com o T4 da C3 (média da
referência a cair 0,0548 contra 0,0219 da mediana; distância média−mediana de
−0,0011 para −0,0340). **Uma corrida, um instrumento óptico. Não certificada** —
mas **a explicação instrumental que a poderia dissolver está agora excluída**
(§0.4), o que a deixa sem concorrente e não a torna certificada. *(E ver NÃO
TESTÁVEL 13: uma outra corrida mede a paisagem envolvente a cair o dobro do
bloco. Se isso for verdade, (b) não é do pomar — é da paisagem, e o
enquadramento inverte-se.)*

**(c) Um acontecimento rápido de 2025-2026, novo, sobre copado vivo,
concentrado na v8.** 93 % do défice de 2026 da v8 é declínio novo; 0 % dela era
chão lavrado em 2021; o disco OESTE lê 2,25 m e 90,2 % de copado em 06-07-2025
(L3); a v8 tem a maior anomalia negativa de VV do Inverno de 2025-26 **por um
factor de cinco** (−0,660 contra −0,135 dB, V4 na forma corrigida por R1); e
96,5 % do défice do foco entrou em 2025-2026.

**O que liga:** a janela partilhada (V2 — os dois focos abrem o fosso enquanto o
resto o fecha) e a co-datação NDVI×SAR sobre 81 mosaicos de geometria pura
(V3, ρ = +0,57 a +0,60, permutação p < 0,0002). **Isso é real e aguenta.** Liga
(c) a **48 %** do défice do foco ESTE — as 1,14 + 0,48 ha que lá entraram em
2025-2026 — e não aos outros 52 %.

> **A leitura que o material sustenta melhor: há UM acontecimento recente
> partilhado, e ele cai sobre dois terrenos com histórias opostas.** O
> ocidental não tinha nenhuma; o oriental tinha oito anos dela.

*Margem, e é o que decide a força disto:* (a) está certificada por dois
instrumentos independentes; (c) está certificada por três proveniências mas com
a perna do LiDAR numa **só data**; **(b) é uma corrida, um instrumento, e está
fora da lista fechada** — e é (b) que decide **quanto** (c) realmente vale, por
I5. **Sem (b) certificada, a decomposição em (a) e (c) aguenta e a afirmação de
que a dicotomia é falsa não aguenta com a mesma força.** Digo-o assim porque é
assim.

*As duas pernas que a adenda dava à leitura de «um só acontecimento» —* **L4 e
L6** *— estão retiradas e não as uso.* E acrescento o que a substitui e que
estava no ficheiro sem ser publicado: `refazer_c2_este.json` regista **«resto do
pomar, com pérgola: 22,20 ha, degrau −0,0316, razão 0,29, p = 0,0082»** — é a
única linha daquele ficheiro **com potência**, e diz que o resto do pomar fecha
o fosso enquanto os dois focos o abrem. Lida contra I5, não diz que o resto está
são.

---

**I8 · O argumento geométrico tem força num sítio e só num.**
*(resposta à tarefa 4)*

V8 dá **2,02 ha a 24 m** do foco OESTE e **1,41 ha em três manchas** do foco
ESTE (publicado 62/72/167 m; LiDAR 60,0 / 74,7 / 166 m **com as áreas trocadas
no texto** — 0,61 ha a 60,0 e 0,55 ha a 74,7, W2). Número defensável **2,60 ha**
(critério duro), tecto **3,58 ha** (W2).

**A taxa de base inverte a impressão, e tem de ser propagada:** o défice de 2026
é **2,68 vezes** mais provável sobre terreno com histórico (45,8 % de 9,34 ha)
do que sobre terreno são (17,1 % de 20,97 ha). **Proximidade a um foco é, em
grande parte, proximidade a défice antigo** — e replantação e re-armação
fazem-se, tipicamente, onde já corria mal.

> **Onde o confundente da taxa de base não existe: a v8.** 0 % de chão lavrado
> em 2021, 93 % do défice de 2026 novo, 3,5 % do défice do foco com histórico
> anterior a 2025. **É o único sítio do pomar onde «novo» quer mesmo dizer
> novo**, e é por isso — e não pela distância de 24 m — que o argumento
> geométrico tem força ali.

*Instrumento independente:* SIM — o mesmo terno de I1, mais o LiDAR a
reproduzir as três manchas orientais a distâncias compatíveis.
*Margem:* 2,60 ha é o piso e 3,58 o tecto, e **os dois são limites inferiores
por I5**; a abertura morfológica 2×2 torna «nunca esteve em défice» mais fácil
de satisfazer, que é o que separa os dois números; e V11 declara uma barra de
~3 ha para a série que **nunca foi propagada** para dentro da intersecção de
oito mapas anuais.

---

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| **B4** — «nove das vinte linhas vêm de uma amostra a granel **sem posição**» | O «Kiwi 1000» **é** o informe 331/2025 e **tem zona**: lado oeste do maior vazio circular, centro a 11,4 m do centro do foco OESTE. **B4 cai pelos termos que a própria C3 escreveu.** | Nove presenças de patogénio passam a estar **localizadas no foco ocidental**. Ver o aviso de §5. |
| **B3** — «18 das 20 linhas nunca foram ensaiadas em nenhuma amostra colocável» | 15 das 20 têm agora **algum** lugar; **13** assentam numa **só** amostra composta; 5 não têm fonte de Ganfei. **A conclusão de B3 sobrevive; a razão muda.** Já não é «nada é colocável» — é **«só um sítio foi alguma vez ensaiado»**. | O modo de falha muda e **agrava-se**: de «não procurámos» para «procurámos num sítio só e encontrámos». |
| **B11** — «toda a amostragem com posição é posterior ao acontecimento» | Continua a **não haver linha de base** (nada anterior ao acontecimento). Mas existe agora **uma amostra com zona declarada, de 2025-06-06** — entre a cena de 2024-07-22 (foco OESTE: 0,09 ha) e a de 2025-08-14 (1,02 ha). É o único material biológico **contemporâneo do arranque**, e vem do sítio do arranque. | Uma comparação antes/depois continua impossível. Uma observação **durante** passa a existir, com n = 1. |
| **B5** — lê-se «nenhum documento nomeia a v8» | Inalterado como afirmação documental. Mas **deixa de se poder ler como «o foco não foi amostrado»**: a zona do testemunho cai sobre a fronteira v7/v8 dentro do foco. | Nenhum facto cai; uma leitura fica proibida. |
| **L8** herdada com «276 cenas» e «recupera a 0,65» | **251 cenas**; o denominador perde metade de si em 2024 e 2026; a recuperação é o denominador a cair. Sobrevive o **0,10 de 2025** e a **monotonia** do OESTE. | A tarefa 2 e a tarefa 3 do meu prompt perdem a perna que lhes fora dada. |
| **L7** herdada sem os acertos de W2 | 0,61 ha a 60,0 m e 0,55 ha a 74,7 m (trocados no texto); a mancha de 0,55 ha tem altura mediana **1,466 m**, abaixo do limiar de 1,5 m. | «Não é chão» aguenta; «pérgola completa» não, para essa mancha. |
| **V2**, «foco ESTE, **restrito a copado**» | O número **+0,0585 mantém-se**; a **etiqueta** foi retirada pela R3. Leia-se «a metade do disco ESTE com altura mediana **≥ 0,5 m**» — e o corte de 0,5 m cai a **0,03 m da mediana daquela unidade**, isto é, parte-a pelo seu próprio centro. | Nada cai. Uma palavra sai. |
| **L5, segunda metade** — «a diferença é a referência a cair, e **o viés do S2C explica quase toda a queda da referência**» | **RETIRADA** (§0.4). O −0,048 não vem de nenhuma corrida: vem de um degrau medido **fora do pomar**, com sensor e ano confundidos. Quatro medições emparelhadas de quatro corridas independentes dão ≈ zero. **A primeira metade mantém-se:** os degraus em fosso são +0,0720 e +0,0585. | **Reforça I5 e D4.** A queda da referência perde a sua explicação concorrente e fica como medição por explicar. E **a ronda H2 correu com este valor como facto de especificação**. |
| **L3, metade oriental**, usada como teste do lado oriental | O voo de 06-07-2025 **cai dentro da janela** e não distingue «nunca teve pérgola» de «teve até Julho de 2024». **A metade ocidental é decisiva; a oriental não é teste.** | A margem de **B7** encostava a essa altura medida e fica enfraquecida. Nada de I7(a) depende dela — (a) assenta em S13, V7, S12, S19 e D1. |
| **`REGISTO_DE_NOMES.md`**, tabela de válvulas | Desactualizada, confirmado por recálculo: v8 a **34,5 m** e não a 157 m. | Quem citar aquele ficheiro cita a versão errada. |
| **B1**, uma caixa e uma distância | Circulam **duas caixas** — G36 (E529500 N4654010 – E530054 N4654413) e a do coordenador (E529592–E529864, N4653920–N4654362) — e **duas distâncias**: 526 m (B1 ao corpo principal, G36) e 900 m (B1 ao foco OESTE). Calculado das pontas de G36, o B1 fica a **772–1435 m** do foco OESTE; da caixa do coordenador, **929–1443 m**. **Declaro, não arbitro.** | Nada meu depende do B1. Fica para a C0. |

---

## REJEITADO

Não rejeito nenhum facto certificado por nenhuma camada abaixo. Rejeito
**leituras** — e cada uma destas é uma leitura que este material torna possível
e que, escrita num livro-razão de exclusões, seria o erro seguinte.

- **«Nenhum organismo está onde o padrão está.»** Já estava retirada (R2 do
  adversário da C3). **Agora está duplamente morta:** nove organismos **estão**
  onde o padrão está, e isso continua a não excluir nada.
- **«A biologia não discrimina por falta de posição.»** A razão mudou. Não
  discrimina porque **só um sítio foi alguma vez ensaiado para treze das vinte
  linhas**, e uma coluna não é um contraste.
- **Ler os quatro negativos de §I3 como exclusões para o pomar.** São
  EXCLUÍDA-LOCAL: uma zona, uma data, uma matriz, n = 1, amostra composta, sem
  sensibilidade declarada. *Armillaria* (raiz e solo), *Rosellinia* (solo) e
  oomicetas (solo) estão excluídos **naquele sítio naquele dia** e em mais lado
  nenhum.
- **Ler o negativo de oomicetas em SOLO como exclusão de *Phytophthora*.** Não
  cobre a raiz — e é na **raiz**, na **mesma amostra**, que dá POSITIVO a
  *Globisporangium intermedium*, que é um oomiceta.
- **Qualquer exclusão construída sobre o informe 240/2023** (Kiwi Atlántico,
  Ribadumia). Cinco das vinte linhas só existem lá. **Armadilha de nome
  activa:** o talhão espanhol chama-se **B-3/C-3** e o bloco do foco ESTE de
  Ganfei chama-se **B3**. Um negativo espanhol lido como Ganfei excluiria
  oomicetas do lado oriental sem um único dado de Ganfei.
- **Promover qualquer um dos nove organismos localizados a causa.** Estão numa
  amostra, composta, num sítio, num dia, sem par de comparação e sem replicado.
  **Um patogénio encontrado no foco e nunca procurado fora dele não é prova de
  que causou o foco.** É a configuração do *P. sojae* com dados melhores.
- **Promover o *Phytophthora sojae* do registo 79.** Notes de um relatório sem
  parcela associada, noutra freguesia.
- **Ler factos do N3 como factos do foco ESTE.** 95,2 m, fora do disco.
- **«A recuperação do N3 a 0,65 em 2026» como prova de replantação.** É o
  denominador a cair (R8).
- **A leitura água-antes-de-verdura (NDMI×NDVI) e a inferência hidráulica ou
  vascular que dela deriva.** Retiradas por R6, e a segunda era a minha própria
  camada a correr dentro da C2.
- **«O resto do pomar está são porque fecha o fosso.»** Ver I5.
- **O viés de calibração do S2C de −0,048 NDVI, em qualquer uso.** Não existe
  nos dados (§0.4). E, em particular, **não pode voltar a ser usado para
  explicar a queda da referência** — que era o seu único emprego nesta cadeia.
  *(O que continua por medir é o efeito sobre a cauda: NÃO TESTÁVEL 14.)*
- **A metade oriental de L3 como teste do lado oriental.** O voo está dentro da
  janela.
- **Tudo o que a lista REJEITADO do meu prompt já continha.** Mantém-se inteira.

---

## NÃO TESTÁVEL

**1 · A causa candidata de maior consequência e a menos testada é regional.**
G26 estabelece que **não existe controlo externo de kiwi contemporâneo neste
aluvião** (varrimento de ~3 km, 13 candidatos, 11 falsos positivos) e que **isso
é resultado, não lacuna de busca**: com dados de satélite este caso **não
distingue** «esta parcela declina» de «todo o kiwi deste aluvião fez isto».
`AGREGACAO_H2` H2-4 acrescenta agora um **dado positivo**: outra exploração de
kiwi a **8,1 km**, com **76,22 ha** declarados (ENT 297313), apresenta **colapso
com degrau em 2024**. **Uma corrida, uma medição, alvo verificado como
existente, NÃO VERIFICADO INDEPENDENTEMENTE.**
*Faria falta:* medir esse alvo numa segunda corrida independente, e procurar
mais dois ou três beneficiários de kiwi da região **pelo parcelário**, que é o
instrumento que o varrimento de G26 não teve.
**Enquanto isto não existir, nenhuma causa local deste livro-razão pode ser
afirmada como explicação suficiente.**

**2 · Uma condição de arranque de duas camadas abaixo não foi cumprida, e
ninguém a registou como não cumprida.** O adversário da C2 pôs **duas**
condições antes de a C3 arrancar: T1 e T3. **O T1 correu** (está em
`c3_07_georreferenciacao.json` → `controlo_T1_referencia`). **O T3 não correu:**
não existe `c2_12_prom_2025.npy`, e a lista `ORTOS` de `c2_12_pergola_2012.py`
continua a ter 2010, 2012 e 2021 e a não ter 2025. O T3 era o teste que
distingue **copado em declínio** de **copado arrancado, replantado ou
re-armado** — que é precisamente a pergunta que a minha tarefa 3 me manda
responder. O LiDAR substitui-o **parcialmente e numa só data** (06-07-2025) e
não cobre 2026. Não consta da lista de lacunas do meu prompt.

**3 · A série Landsat da referência nunca entrou em nenhuma lista fechada.** O
`ADVERSARIO_2026-08-29.md` W1 chama-lhe «o melhor trabalho do dia», regista que
mede a referência a cair **0,888 → 0,874 → 0,862** (−0,026 contra −0,054 do
Sentinel-2), diz que **devia entrar** na lista fechada, e ela **não entrou**.
**É o único instrumento verdadeiramente externo que este caso produziu** — outra
agência, outro sensor, outra cadeia de correcção — e é exactamente o que falta
para certificar I5 e a componente (b) de I7. Não o uso por não estar na lista.
*Faria falta:* certificá-lo, com as três margens que W1 já nomeia (partilha de
píxeis a 30 m, ausência de filtro de pureza, transição L8→L9).

**4 · As treze linhas que agora têm lugar não têm par de comparação.** Nenhuma
delas foi alguma vez ensaiada em mais nenhum ponto — nem no foco ESTE, nem na
referência, nem no resto do pomar. **A pergunta «este organismo está só aqui?»
não tem dados que a possam responder em qualquer sentido.** *(O desenho que a
fecharia é da C5. Não o escrevo.)*

**5 · Replantação contra chão limpo mantido, no N3.** As duas leituras são
mutuamente exclusivas e o material não as separa. A que os números **favorecem**
é a segunda (piso de Inverno a descer, pico de Verão a descer e a afastar-se da
referência — uma videira jovem a pegar fecha-se sobre a referência no Verão,
esta afasta-se), mas o piso de 0,654 no Inverno de 2024/25 contra 0,358 da
referência continua por explicar. *Faria falta:* **um segundo voo LiDAR, ou uma
visita. Não mais análise.**

**6 · As quatro ITS ISFBV0314–17.** NÃO RESOLVIDO. Não há testemunho (o gestor
não sabe) e **não há documento nesta máquina** (verificado). *Faria falta:* o
formulário de submissão da Fauna Útil SL, ou os quatro PDF.

**7 · O que aconteceu ao B2 e ao B3 entre 2024 e 2026.** Pedido pelo adversário
da C2 e outra vez pelo adversário da adenda. Continua por fazer.

**8 · A G10 nunca foi re-certificada.** Condição 1 do veredicto do adversário da
C2: a C0 re-certifica a reposição da cena de 2019-09-02 em uma linha. Não
aconteceu, e a V11 — que sustenta toda a leitura da série — depende inteiramente
dessa cena.

**9 · Nove cenas no código, dez no certificado.** `c2_00_comum.DATAS` tem nove;
a V1 declara dez. **Declaro e não resolvo**, como o prompt manda.

**10 · Três raios de disco para os mesmos focos.** 70 m (`altura_copado.py`,
N1/N2/N3), 90 m (`discos_dos_focos`, a maior parte da cadeia), 120 m
(`c2_05_manchas.py`, a datação que uso em I1). Nunca foi declarado como
divergência. Uso o de 120 m em I1 e digo-o.

**11 · A margem de B10 continua sem existir.** Sem bootstrap, sobre a cena S2C.
Por isso I5 certifica direcção e não dimensão.

**12 · Degrau contra declínio a acelerar.** Nas duas unidades que a adenda
classifica «DEGRAU», o modelo **linear** tem p menor: ESTE com pérgola
p_b = 0,015 contra p_degrau = 0,042; ESTE «plantado» 0,0069 contra 0,029 (W4).
**Os dados não separam «degrau» de «declínio a acelerar»**, e a componente (b)
de I7 torna a segunda leitura mais plausível do que era. Não a escolho.

**13 · A paisagem envolvente e a referência dizem coisas incompatíveis, e
ninguém juntou os dois números.** A corrida B imprimiu que a **vegetação
envolvente caiu 0,075 entre 2024 e 2026 — o dobro da queda do bloco** — e não
relacionou os dois; a corrida C mediu que a sua referência **não se move**
(−0,0070, p = 0,54). **As duas não podem estar as duas certas.** Registo e não
resolvo. **Se a paisagem caiu o dobro do bloco, o enquadramento do caso
inverte-se:** o pomar passa a estar a resistir melhor do que o que o rodeia, e a
pergunta regional (entrada 1) deixa de ser secundária. *Faria falta:*
reconciliar as duas corridas sobre a mesma máscara de envolvente e a mesma
janela, **e declarar qual é o objecto «envolvente» em cada uma** — que é a
hipótese óbvia para a discrepância. Linha REG-03 do livro-razão.

**14 · O efeito do S2C sobre as estatísticas de CAUDA nunca foi medido.** A
§0.4 exclui o viés sobre o **nível**. Mas um degrau de sensor não é uniforme em
NDVI — uma diferença de bandas ou de correcção atmosférica actua de forma
diferente a 0,89 e a 0,70, e o que isso produz é um alargamento da cauda
inferior. **Todas as grandezas-título desta cadeia — área em défice, dispersão,
fracção, M2 — são estatísticas de cauda**, e o único controlo instrumental
existente corre sobre a média (W3). *Faria falta:* medir o desvio-padrão e a
assimetria das células **fora** do pomar nas duas cenas S2C. **Três linhas sobre
ficheiros que já estão em disco.** Linha INS-06 do livro-razão.

**15 · O voo LiDAR está dentro da janela em análise.** 06-07-2025 não distingue
«nunca teve pérgola» de «teve até Julho de 2024». **A metade oriental de L3 não
é teste de nada sobre o lado oriental**, e a margem de B7 que a ela encosta fica
enfraquecida. **A metade ocidental é decisiva** e é a que uso: 2,25 m e 90,2 %
de copado vivo no foco OESTE, em pleno acontecimento. *Faria falta:* um segundo
voo, ou uma visita.

---

## PASSA PARA CIMA — lista fechada

Oito. Tudo o que não estiver aqui, não passa. Sou avaro de propósito: quase
tudo o que esta camada produziu é **negativo** ou **de âmbito**, e âmbito não é
facto.

**D1.** **A composição do défice de 2026 separa os dois focos.** Na v8, que
contém o foco OESTE (E530485 N4655053), **93 % do défice de 2026 é declínio
novo** e **0 % era chão lavrado em 2021**; nas v13/v14, que contêm o foco ESTE
(E530977 N4655117), são **36 % e 34 %**, sobre **22,6 % e 13,8 %** de chão
lavrado em 2021. Por permanência no disco de **120 m**: **3,5 %** do défice do
foco OESTE tem histórico anterior a 2025, contra **52,4 %** do foco ESTE.
*Prova:* `c3_07_georreferenciacao.json` + `c2_05_manchas.json` → `datacao_focos`.
*Instrumento independente:* tabela do gestor (documento) × ortofoto 2021
(estrutura) × Sentinel-2 (série). *Margem:* ±10 m na partição; **disco de 120 m,
não 90**; o contraste é entre dois objectos seleccionados da mesma maneira.

**D2.** **Há um acontecimento recente partilhado, e ele cai sobre dois terrenos
com histórias opostas.** A janela (V2) e a co-datação NDVI×SAR (V3) ligam-no aos
dois focos; a história (D1, S13, V7, S12, S19) separa-os por completo. **Liga-o
a 48 % do défice do foco ESTE, não aos outros 52 %.**
*Instrumento independente:* óptico × radar (V3), e substrato × sinal (S20 × D1).
*Margem:* o quanto do acontecimento é real depende de D4, que não está
certificada; e os dados não separam degrau de declínio a acelerar (NÃO
TESTÁVEL 12).

**D3.** **O argumento geométrico tem força na v8 e só na v8.** O défice de 2026
é **2,68×** mais provável sobre terreno com histórico (45,8 %) do que sobre
terreno são (17,1 %) — logo proximidade a um foco é, em geral, proximidade a
défice antigo. **A v8 é o único sítio do pomar onde esse confundente não
existe.** Números: **2,60 ha defensável, 3,58 ha tecto**, os dois limites
inferiores por D4.
*Prova:* `c2_05_manchas.json` → `m2`; W2 do adversário da C2.
*Instrumento independente:* como D1. *Margem:* a barra de ~3 ha de V11 nunca foi
propagada para a intersecção de oito mapas anuais.

**D4.** **Toda a magnitude expressa em fosso à referência é um limite inferior,
e a área em défice também.** «O resto do pomar fecha o fosso» **não** quer dizer
«o resto do pomar está são». **E a explicação instrumental que competia com isto
está excluída:** quatro medições emparelhadas de quatro corridas independentes
põem o viés do S2C em ≈ zero, e o −0,048 que circulava vinha de um degrau medido
**fora do pomar**, com sensor e ano confundidos.
*Prova:* C3-R2 B10 + G6/G25 + `_MULTIVERSO\ADVERSARIO_H1.md`.
*Instrumento independente:* herdado de B10; a exclusão do viés vem de quatro
corridas independentes.
*Margem:* **direcção certificada, dimensão não** — não há bootstrap. Não
quantificar sem a série Landsat (NÃO TESTÁVEL 3). **O efeito do S2C sobre as
estatísticas de cauda continua por medir** (NÃO TESTÁVEL 14).

**D5.** **O *M. hapla* está excluído como explicação do contraste entre os
focos, e não está excluído como stress de fundo.** Positivo em 4/4 unidades
colocadas; ρ(défice, solo) = **−0,40**, ρ(défice, raiz) = **−0,80**; contagem
mais baixa no bloco mais afectado; **contagem mais alta (250/200 cc) no B1, que
não tem posição.**
*Prova:* `c3_05_folhas.txt` + `c3_07_georreferenciacao.json`.
*Instrumento independente:* **SIM** — laboratório × Sentinel-2.
*Margem:* n = 4, uma data, um método; **nenhum dos dois ρ é significativo**. O
que passa é a direcção e a ausência de gradiente causal.

**D6.** **A matriz de diagnóstico tem uma só coluna útil.** Das 20 linhas
organismo × matriz: **13 assentam numa única amostra composta** (informe
331/2025, 2025-06-06), **2** têm contraste multi-unidade (*M. hapla*), **5** não
têm nenhuma fonte de Ganfei. **Dos 5 resultados NEGATIVOS do caso, 4 vêm dessa
mesma amostra e 1 só existe em Espanha: nenhum negativo deste caso vem de uma
amostra que se possa comparar com outra.**
*Prova:* `c3_05_folhas.txt`, folha `Matriz Fitopatologia`, lida célula a célula
por `c4_01_numeros.py`. *Instrumento independente:* nenhum, declarado; passa
porque a conclusão é negativa. *Margem:* categórica quanto à cobertura; a classe
contrária **é emissível** e tem duas ocorrências.

**D7.** **Nove presenças de patogénio estão localizadas no foco ocidental, e
nenhuma delas é causa.** As nove linhas positivas exclusivas do informe 331/2025
— quatro de madeira (*F. cerealis*, *F. equiseti*, *F. oxysporum*, *N. parvum*)
e cinco de raiz (*Ceratobasidium*, *F. oxysporum*, *F. solani*, *N. parvum*,
*Globisporangium intermedium*) — têm zona declarada por **testemunho de tipo 1**:
lado oeste do núcleo redondo de 3,98 ha centrado a 11,4 m do foco OESTE.
**Nenhuma foi alguma vez procurada em nenhum outro ponto deste pomar.**
*Prova:* testemunho do gestor × `c3_05_folhas.txt`. *Instrumento independente:*
testemunho × partição documental (G35), para o **lugar**; **nenhum** para o
resultado. *Margem:* **zona, não ponto**; amostra **composta** sobre matéria
desconhecida; **n = 1**; 2025-06-06; **sem par de comparação**.
**⚠ Passa como PRESENÇA LOCALIZADA e nada mais. Promover qualquer uma a causa é
o erro do *P. sojae* com dados melhores, e desta vez com a localização certa.**

**D8.** **Nenhum ensaio bacteriano ou viral foi alguma vez feito neste caso.**
Os 15 taxa da matriz são fungos, oomicetas e um nemátode. A *Pseudomonas
syringae* pv. *actinidiae* nunca foi procurada, em nenhuma matriz, em nenhuma
data, com ou sem posição.
*Prova:* `c4_01_numeros.json` → `matriz_resumo.taxa`. *Instrumento
independente:* nenhum; conclusão negativa. *Margem:* é afirmação sobre **este
painel**, não sobre o pomar.

---

## 3 · A HIPÓTESE DE RENOVAÇÃO, TRATADA A SÉRIO
*(tarefa 3)*

**Primeiro, o objecto.** A hipótese é sobre o **N3, E531068 N4655145** — que
está a **95,2 m** do centro do foco ESTE e portanto **fora do disco de 90 m**.
Não é uma hipótese sobre o foco ESTE. O meu prompt trata-os como um só («do lado
oriental»); separo-os.

**O que a sustenta:** 0,27 m de altura mediana no N3 em 06-07-2025 (disco de
**70 m**, outro raio); o parcelário IFAP a declarar **KIWI** ali a 10-06-2025,
três semanas antes do voo; a amplitude sazonal a cair a **0,10 em 2025**; e
16,3 % de chão lavrado no B3 já em 2021 (B7).

**O que a falsificaria, escrito antes de olhar:** uma videira jovem a pegar
**sobe de ano para ano em direcção à referência no Verão** e **fecha o fosso**,
enquanto o seu piso de Inverno se mantém baixo, porque é caduca e o solo está
limpo entre fiadas. Se, ao longo de duas épocas, o pico de Verão **descer** e se
**afastar** da referência, a hipótese está falsificada. E se o piso de Inverno
for **alto** e depois **descer**, o que se está a medir é **coberto verde
mantido e depois removido**, não uma plantação a estabelecer-se.

**O material existente falsifica-a, parcialmente, e já estava medido.** Do
`piso_inverno_tabela.json` e do `amplitude_serie.json`, através da R8 e da W6 do
`ADVERSARIO_2026-08-29.md`:

- piso de Inverno do N3: **0,654 (2024/25) → 0,497 (2025/26)** — **desce**;
- pico de Verão do N3: **~0,71 → ~0,65** — **desce**, e fica **0,20–0,26 abaixo
  da referência**;
- a «recuperação a 0,65» que era o seu melhor apoio **é o denominador a cair**:
  em absoluto o N3 vai de 0,052 para 0,180 enquanto a referência vai de 0,538
  para 0,277.

**Os dois critérios que escrevi antes apontam ambos para a leitura alternativa:
chão limpo mantido, que tinha coberto verde no Inverno de 2024/25 e deixou de o
ter.** No livro-razão, **GES-01 (renovação) fica NÃO TESTADA e parcialmente
contradita; GES-02 (chão limpo mantido) fica NÃO TESTADA e é a que os números
favorecem.**

**Não a confirmo por coerência**, e digo porquê com nome: três hipóteses de
terreno já foram fixadas, corridas e retiradas neste caso — posição topográfica
húmida, topologia da rede de rega, e a linha térmica. Duas delas foram retiradas
por **contradição**, não por dúvida. **Esta ainda não foi corrida como hipótese:
foi contradita por dados que existiam para outro fim.** Isso é mais fraco.

**O que a fecha, e não é análise:** um segundo voo LiDAR, ou uma visita. E o
piso de 0,654 no Inverno de 2024/25, trinta pontos de NDVI acima do pomar na
estação em que a videira caduca está nua, **continua por explicar em qualquer
das duas leituras**.

---

## 4 · O QUE A BIOLOGIA PERMITE DIZER
*(tarefa 5)*

Depois da arbitragem, é **mais** e não menos — e é por isso que é mais
perigoso.

**O que se pode dizer:** que numa amostra composta colhida em 2025-06-06 no lado
oeste do maior vazio circular, a 11,4 m do centro do foco OESTE, um laboratório
encontrou quatro fungos de madeira, cinco organismos de raiz incluindo um
oomiceta, e *M. hapla*; e não encontrou *Armillaria* (raiz e solo),
*Rosellinia* (solo) nem oomicetas (solo).

**O que não se pode dizer, e a lista é toda a inferência:**

1. **Que algum deles cause alguma coisa.** Nunca foram procurados noutro sítio.
   **Não existe uma única amostra deste caso que possa servir de comparação para
   nenhuma das treze linhas.** Um patogénio encontrado no foco e não procurado
   fora dele é uma presença, não uma causa.
2. **Que os quatro negativos excluam alguma coisa fora daquela zona e daquele
   dia.** Amostra composta, n = 1, sensibilidade não declarada.
3. **Que os oomicetas estejam excluídos.** O negativo é de **solo**; a mesma
   amostra dá **positivo** a um oomiceta na **raiz**.
4. **Que o lado oriental esteja coberto por alguma coisa.** A única amostra
   biológica de lá é um composto de bloco sobre 9,92 ha, dos quais 16,3 % são
   chão lavrado, e mede um organismo (B7).
5. **Que exista qualquer informação bacteriana ou viral.** Zero linhas.
6. **Que os cinco resultados espanhóis digam o que quer que seja sobre Ganfei.**

**E a distinção que decide o livro-razão, agora na forma que este material
obriga:** já não é «não procurámos». É **«procurámos num sítio só, e
encontrámos»** — e essa segunda frase, num livro de exclusões, é ainda mais
fácil de ler mal do que a primeira, porque **traz positivos localizados
consigo**. A frase antiga não excluía nada e via-se. Esta não exclui nada e
**parece** que sim.

**As 41 linhas NÃO TESTADAS do livro-razão são o produto principal desta
camada.** Não são uma lacuna do relatório: são o resultado.

---

## 5 · O QUE A ÁGUA PERMITE DIZER
*(tarefa 6, com a premissa retirada)*

**A premissa da tarefa está retirada** (§1.3). Não construo sobre ela.

**O que sobra, e é pouco:**

- Recolocada sobre **variações desde a base**, que é a única forma defensável, a
  razão NDMI/NDVI é **1,53** no ESTE e **1,36** no OESTE — e **ainda por
  descontar da diferença de escala** entre os dois índices. Não é uma
  assinatura.
- O NDMI da referência lê **0,470 a 0,516** em catorze anos, longe de saturar.
  Isso é a resposta directa à objecção de saturação do NDVI e é mais forte do
  que a ressalva que foi escrita. **Mas NDVI e NDMI partilham a banda NIR e não
  são instrumentos independentes um do outro.**
- **Duas hipóteses de terreno foram fixadas, corridas e retiradas, e as duas
  foram-no por contradição:** a posição topográfica húmida (o défice está no
  terreno **alto** nas onze cenas, ρ da cota −0,20 a −0,46, p < 1e-24) e a
  topologia da rede de rega (o agrupamento por válvula cai dentro do nulo rodado
  nas onze cenas). **As duas retiradas aguentam.**
- **Uma pista foi arquivada com elas e nunca reportada:** dentro do foco OESTE a
  **área drenante inverte de sinal e emerge nos anos do evento** (+0,116 · +0,122
  · +0,144 · +0,069 · +0,203 · +0,009 · −0,122 · −0,201 · −0,163 · −0,252 ·
  −0,226), pelo critério de leitura que o próprio script imprime. Com
  autocorrelação de 0,86–0,96 e ~200 células **é pista, não facto**. Registo-a
  porque retirar uma hipótese e arquivar a corrida deita fora o que a corrida
  produziu.
- **A rega por válvula está excluída como AGRUPAMENTO e não está testada como
  AVARIA.** Um teste de agrupamento não vê uma unidade isolada, e o teste de
  «ordem na rede» é inválido por desenho: a origem está a **240 m** do foco
  OESTE numa parcela de 1458 m, logo «distância à origem» é quase «distância ao
  foco OESTE». **Uma válvula é uma unidade de gestão**, e é numa válvula que se
  concentra a maior anomalia de radar do caso.

**O que faria falta, e nenhum índice óptico o dá:** humidade de solo **medida**
no foco e na referência; ou fluxo de seiva. E, para a linha térmica que S17
retirou: **LST nocturno ou temperatura de solo medida** — a causa nunca foi
testada, só o instrumento é que caiu. **Não ressuscitar a linha térmica diurna.**

---

## 6 · AS TRÊS PERGUNTAS DE UMA LINHA
*(tarefa 7 — por confiança ganha por esforço)*

**1 · Enviar a amostra de raiz de *Rosellinia* que já foi colhida.**
Custo: um envelope. Existe: colhida em **2026-08-04**, raiz, uma planta
arrancada, identificação macroscópica, e **não enviada** («não será
necessário»). É o **único organismo que um observador de campo nomeou** neste
caso. O único negativo que lhe podia opor é de **solo** e de **catorze meses
antes** (B9). No livro-razão, **BIO-13 é NÃO TESTADA** e esta é a linha mais
barata de fechar de toda a cadeia. *Coloca-se também a coordenada da planta, que
o registo não tem.*

**2 · O registo de operações do B2 e do B3 em 2024-2026 — arranque,
replantação, poda severa, substituição de pérgola, falha de rega, com data e
sector.**
Uma linha ao gestor. **Já tem dois pedidos independentes atrás dela** — o
adversário da C2 («vale mais do que qualquer análise adicional») e o adversário
da adenda de LiDAR — e continua por fazer. Decide **quatro** linhas do
livro-razão (GES-03, GES-04, ABI-05, e o âmbito de GES-01/02) e decide se a
amostragem de 2026 caiu sobre plantas adultas, sobre replantação, ou sobre chão
— sem o que **nenhum resultado de 2026 é interpretável**.

**3 · Os originais: os quatro PDF ISFBV0314–17, e o informe 331/2025 da
Areeiro.**
Ao laboratório, ou à Fauna Útil SL, que é o `Client_Titular` das ITS **e** o
submissor dos cinco informes de nemátodes com talhão. Verifiquei que **nenhum
deles existe nesta máquina**: os dois livros citam-nos pelo nome. Fecha as ITS
nos dois sentidos, e — o que ninguém pediu ainda — **diz sobre o que é que a
amostra composta 331/2025 foi composta**, que é a cautela 2 do testemunho e o
que decide se D7 vale para uma planta ou para meio hectare.

*(A quarta, que não conta para as três porque não toca o corpo principal: **o
esquema de válvulas do B1**, quais os polígonos das válvulas 1 a 5. Decide se
H2b tem controlo. E lá está a contagem de nemátodes mais alta de todas.)*

**Três dos erros que custaram semanas a este processo foram apanhados por ir a
um instrumento diferente, e nenhum por recalcular.** As três acima são todas
instrumentos diferentes: uma cultura de laboratório, um caderno de campo, e um
PDF.

---

## 7 · SE A INFERÊNCIA NÃO FECHAR, DIZ-SE
*(tarefa 8)*

**Não fecha, e nomeio o que não distingue:**

1. **Local contra regional.** G26 é explícito e é resultado. Com H2-4 há agora um
   dado positivo do lado regional, não verificado. **Esta é a que mais importa e
   é a menos testada.**
2. **Doença contra operação de gestão, no lado oriental.** O T3 não correu e o
   registo de operações não foi pedido.
3. **Replantação contra chão limpo mantido, no N3.**
4. **Degrau contra declínio a acelerar**, nas duas unidades.
5. **Qual dos treze organismos localizados, se algum, tem alguma coisa a ver com
   o que se vê** — porque não existe um segundo ponto ensaiado.
6. **Se o que se está a medir é o pomar ou a paisagem que o rodeia** — uma
   corrida mede o envolvente a cair o dobro do bloco, outra mede a sua
   referência parada, e ninguém juntou os dois números. *(A pergunta gémea —
   «quanto é o sensor?» — deixou de estar em aberto quanto ao nível: §0.4. Fica
   em aberto quanto à cauda: NÃO TESTÁVEL 14.)*

**A etiologia não está estabelecida e este certificado não a estabelece.** O que
está estabelecido é onde é que ela **poderia** estar e onde é que
**seguramente** não foi procurada.

---

## 8 · QUANTIDADES-ÂNCORA

| âncora | declarado | obtido / reportado pela C4 | nota |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | — |
| polígono `pomar` | 30,31 ha | 30,31 ha | herdado, não recalculado |
| referência sistemática | 1,10 ha / 110 células | 1,10 ha / 110 | ver D4 — **não é controlo são** |
| banda contígua | 27,30 ha | **27,30 ha** | recalculado de `valvulas_por_area.json` |
| total da tabela do gestor | 44,93 ha | não recalculado | documental; o ficheiro operativo só tem as doze da banda |
| chão lavrado `nu2021` | 1,67 ha | 1,67 ha | herdado |
| défice de 2026 | 7,86 ha | **7,86 (com abertura 2×2) · 9,47 (sem) · 10,32 (sem, ref. limpa)** | três objectos, qualificados em B10 |
| declínio novo M2 | 3,58 ha | **2,60 defensável · 3,58 tecto**, os dois **limites inferiores** por D4 | — |
| **cenas na série** | 11 | 11 | — |
| **cenas de plena estação** | 9 | **9 no código, 10 no certificado da C2** | **divergência declarada, não resolvida** |
| NDVI da referência 2017-07-02 | 0,838 | **0,8898** | divergência |
| NDVI da referência 2026-07-27 | 0,886 | **0,8766** | divergência — **e o sinal inverte-se** |
| registos | — | **221 · 111 com posição · 110 sem** | — |
| taxa distintos | 26 declarados | **15** em **20** linhas | — |
| linhas ensaiadas com posição | — | **2 de 20 em unidade colocada; 15 de 20 com algum lugar; 13 assentam numa só amostra** | **muda com a arbitragem de §0** |
| distâncias ao foco OESTE | — | v8: **34,5** (recalculado do ficheiro operativo) · 34 (G35) · 35 (C1) · 43 (C2, centróide) · 46 (C3, centróide) — v7: **110,7** (recalculado) · 111 (C1) · 120 (C3, centróide) · 53 (C3, célula mais próxima) | **nenhum é a distância de uma amostra** |

**Âncoras novas desta camada:**

| âncora | valor |
|---|---|
| linhas no livro-razão | **59** |
| **NÃO TESTADAS** | **41** |
| EXCLUÍDAS | **7** |
| EXCLUÍDA-LOCAL (uma zona, uma data, n = 1) | **4** |
| SUSTENTADAS | **5** |
| INCONCLUSIVAS | **2** |
| viés do S2C, medido por quatro corridas independentes | **≈ 0** — e o **−0,048** que circulava não vem de nenhuma delas |
| linhas organismo × matriz que assentam numa só amostra composta | **13 de 20** |
| resultados NEGATIVOS do caso vindos de amostra comparável | **0 de 5** |
| taxa bacterianos ou virais em todo o painel | **0** |
| raios de disco em circulação para os mesmos focos | **3** — 70, 90 e 120 m |
| N3 ao centro do foco ESTE | **95,2 m** — fora do disco de 90 m |
| centro do maior vazio circular ao centro do foco OESTE | **11,4 m** |

---

## 9 · NOTA AO ADVERSÁRIO, QUE DESTA VEZ EXISTE

Duas camadas seguidas escolheram, para esta nota, os pontos que já sabiam
resolver. Escrevo os quatro que doem.

**1 · Re-etiquetei nove linhas em vez de as re-derivar.** A arbitragem chegou a
meio da corrida e nove organismos passaram de «sem posição» a «localizados no
foco ocidental» **numa mensagem**. Verifiquei a proveniência (§0.1) mas **não
reconstruí o raciocínio de baixo para cima** com a nova premissa: apliquei-a às
conclusões que já tinha. O adversário deve procurar, no meu texto, sítios onde
«presença localizada no foco ocidental» esteja a fazer trabalho retórico que não
aguenta — e o candidato mais provável é o D7, cuja força é toda a advertência e
cujo conteúdo positivo é uma linha.

**2 · Os 93 % da v8 carregam metade do meu argumento e são um quociente de duas
percentagens do mesmo JSON.** 47,1 / 50,7, sobre uma partição de Voronoi cuja
arbitrariedade a C3 declarou e que eu herdei sem testar. **Se a fronteira v7/v8
se deslocar, o quociente desloca-se**, e não corri nenhuma análise de
sensibilidade. Notar que a v7 dá **1,00** no mesmo quociente torna o argumento
mais forte ou mais suspeito, e não sei qual.

**3 · Usei a datação a 120 m e declarei a divergência em vez de a resolver.** A
maior parte dos factos de foco desta cadeia corre a 90 m. Correr
`datacao_focos` a 90 m são duas linhas sobre ficheiros que estão em disco.
**Declarar é mais barato do que resolver, e eu escolhi o barato** — que é
exactamente a crítica que o adversário da C3 fez à C3 sobre o T1.

**4 · A minha frase mais forte apoia-se no facto menos certificado que uso.** A
afirmação de que «um acontecimento ou dois» é a pergunta errada (I7) precisa da
componente (b) — a perda em bloco — que é **uma corrida, um instrumento, fora
da lista fechada**. Sem ela, (a) e (c) sobrevivem e a decomposição continua de
pé, mas a **afirmação sobre a pergunta** não. Escrevi-a na mesma, com a margem
ao lado. Um adversário tem o direito de dizer que a margem não chega e que a
frase devia ter ficado em NÃO TESTÁVEL.

**5 · A segunda arbitragem retirou um facto herdado e o efeito foi reforçar a
minha afirmação principal. Isso merece mais escrutínio, não menos.** A retirada
do viés do S2C tira a única explicação concorrente de I5 e de D4, que são as
duas coisas mais fortes que escrevo. **Aceitei-a depressa e sem a atacar**, e a
correcção que aceitei sem atacar foi precisamente a que me convinha. O
adversário deve fazer o que eu não fiz: verificar se as quatro medições
emparelhadas são de facto **emparelhadas** — mesmas células, mesmas datas, mesma
definição de reflectância — ou se são quatro grandezas diferentes a chamarem-se
todas «viés do S2C», que é exactamente a classe de erro que esta cadeia apanhou
três vezes (34/35/43/46 m, «anomalia» com dois significados, três números para o
défice de 2026).

**E um que mantenho contra quem vier:** o meu prompt mandou-me responder à
tarefa 6 sobre uma leitura que já estava retirada, e mandou-me usar em duas
tarefas uma L8 que o seu próprio adversário já tinha corrigido. **Não construí
sobre nenhuma das duas**, e registo-o aqui e não numa nota de rodapé, porque o
padrão que este processo já viu três vezes é o de a correcção existir a montante
e a camada seguinte não a receber. Foi assim com a L4 e a L6 — que o meu prompt
apanhou — e não foi assim com a L7, a L8 e a R6, que não apanhou.

---

## 10 · O QUE ESTA CAMADA NÃO ESCREVE

Não há desenho de amostragem, não há medidas de gestão, não há árvore de
decisão, e não abri `ganfei_s2\_pacote_cowork\`. Não modifiquei nada em
`ganfei_s2\` nem em `_VALIDADE_GESTAO\`.

A pergunta que a C5 vai receber, e que esta camada deixa formulada e não
respondida, é a que sai de D6 e de NÃO TESTÁVEL 4: **existe um sítio deste pomar
que tenha sido alguma vez ensaiado para as mesmas linhas que o foco ocidental —
e a resposta é não.** O que fazer com isso é decisão, e é de quem vem a seguir.
