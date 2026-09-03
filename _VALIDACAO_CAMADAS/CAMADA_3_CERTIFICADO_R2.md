# Camada 3 — Biologia · revisão R2

29-08-2026. **Esta revisão substitui o `CAMADA_3_CERTIFICADO.md`.** Onde os dois
discordarem, **ganha a revisão** — pela mesma regra que a `CAMADA_0_REVISAO_R2.md`
usou com o certificado da C0.

Escrita depois do `CAMADA_3_ADVERSARIO.md`, cujo veredicto foi: *o certificado
não segue como está; segue com as oito retiradas da parte 1 e com a paragem de
linha reformulada nos termos de §0.3*, sob **uma condição única e bloqueante —
que o T2 corra antes de a C4 arrancar**.

**O T2 correu.** Os sete números estão publicados em §3. Correu também o **T4**,
que era meu e tinha ficado por fazer, e que resolveu a divergência em vez de a
declarar corrigida. Código novo: `SAIDA_C3\c3_13_T2_T4.py` →
`c3_13_T2_T4.json` + `c3_13_saida.txt`. Nada foi modificado em `ganfei_s2\`.

**Aceito sete das oito retiradas na íntegra.** Contesto a **premissa** da R1 —
com prova — e aceito a sua **conclusão**. Está em §1, primeiro, porque uma
retirada mal fundada é tão grave como uma afirmação mal fundada, e o protocolo
não me deixa concedê-la em silêncio.

---

## 0 · A paragem de linha, reformulada

### 0.1 · O dispositivo muda: de REJEITADO para NÃO RESOLVIDO

A linha «amostras» da tabela **G34** da `CAMADA_0_REVISAO_R2.md` passa de
**REJEITADO** a:

> **NÃO RESOLVIDO — conflito entre relato e documento, com a precedência por
> decidir.**

O adversário tem razão e a razão é do `CLAUDE.md` deste projecto, não de uma
preferência de redacção. A G34 aparece no suplemento da R2 sob o cabeçalho «três
coisas vieram do gestor», ao lado da G35 e da G36. Se a linha veio da mesma
origem, é **testemunho directo** — e a regra do projecto é explícita: *não se
corrige com réplica; corrige-se perguntando outra vez a quem sabe.* O
instrumento com que eu a derrubei foi o **silêncio de um documento**, e um livro
que não regista o talhão não prova que ninguém saiba o talhão.

A diferença não é semântica. Com «REJEITADO», B5 lê-se **«a v8 nunca foi
amostrada»**. Com «NÃO RESOLVIDO», lê-se **«a v8 não tem nenhuma amostra que os
documentos consigam lá pôr»** — que é bastante mais fraco e é o que os dados
suportam.

### 0.2 · O que se mantém, e com prova melhor do que a que citei

**Nada nos dois livros coloca as quatro ITS ou o «Kiwi 1000» num talhão.** Isto
está estabelecido, e **nenhuma frase da G34 sobre esforço de amostragem pode ser
usada pela C4.**

**Retiro «três sítios independentes».** São três anotações do mesmo compilador
dentro do mesmo livro, todas com a mesma ressalva («nas páginas *extraídas*»,
«nos ficheiros *revistos*»), e reduzem-se a uma só observação de origem. É **um**
instrumento com três frases, e chamar-lhe independente é a violação de controlo 1
que eu próprio apanhei noutras camadas.

**A prova real é outra e é mais forte,** e o adversário encontrou-a nos meus
dados: nas vinte linhas das ITS **todos os campos de identificação estão vazios
ao mesmo tempo** — `Terrain_Block_Parcel`, `Sample_Date`, `Lab_Provider` e
`Parish_Municipality`, com o próprio livro a marcar a atribuição ao pomar como
**presumida**.

**E aceito a correcção de sentido inverso, que limita a minha própria rejeição.**
O `Client_Titular` das quatro ITS é **«Fauna Útil SL (titular/submitting org)»** —
exactamente o mesmo submissor dos cinco informes de nemátodes 339–343/2026, os
únicos com código de talhão do caso. Isso não lhes dá talhão, mas torna
insustentável a frase que escrevi, «não podem ser atribuídas ao foco OESTE **nem
a lado nenhum**». Não podem ser atribuídas a um **talhão**. A atribuição ao pomar
é presumida e é plausível. **A frase sai.**

### 0.3 · A execução esteve errada, e a frase que a justificava era falsa

**Retiro esta frase do certificado:**

> «Não há nada por cima que dependa da linha rejeitada e que eu esteja a
> construir: a rejeição é o produto.»

**É falsa pelos meus próprios números.** Quatro dos onze factos da lista fechada
estão construídos em cima da rejeição — **B2** (35 dos 53 «sem posição
declarada»), **B3** (nove das vinte linhas), **B4** (cai inteiro se o «Kiwi 1000»
tiver lugar) e **B5** (se a linha da G34 estivesse certa, a v8 teria vinte
registos). E escrevi o `CAMADA_4_PROMPT.md`, que já os transportava verbatim.

A regra 2 do protocolo é literal: *pára, escreve o que rejeitaste, e devolve.*
Rejeitei, construí quatro factos por cima, e passei o bastão com uma caixa de
aviso em cima. **Não foi uma paragem de linha parcial; foi uma rejeição seguida
de continuação normal.** Registo-o como falha de procedimento minha.

### 0.4 · A pergunta que nunca fiz, e que é a única que resolve isto

**De onde veio a atribuição das ISFBV0314–17 e do «Kiwi 1000» ao foco OESTE?**

Não está em NÃO TESTÁVEL, não estava na paragem de linha, não estava no prompt
da C4. É de uma linha. Se a resposta for «da minha memória», a linha volta como
testemunho e a C3 reescreve B3, B4 e B5. Se for «de nenhum lado, foi inferido», a
suspensão consolida-se em rejeição — e B5 reescreve-se na mesma, porque a
ausência continua a ser documental e não física. **Passa para NÃO TESTÁVEL como
o item de maior valor da minha camada.**

---

## 1 · A R1 — contesto a premissa, aceito a conclusão

Esta é a única retirada que não aceito como está, e explico-me com ficheiro e
comando, porque o adversário acusa a linha de ser *um facto que não existe em
lado nenhum* — que é a acusação mais grave que se pode fazer nesta cadeia.

**A R1 diz:**

> «Esta categoria não existe. Procurei "podred", "podrid", "root rot",
> "radicular", "No Detectado" e "MUITO ALTO" em `c3_05_folhas.txt`, no
> `c3_04_registo_principal.csv` (os 221 registos, 22 colunas), e em todo o
> `_VALIDACAO_CAMADAS\`. **Contagem: zero, em todo o lado.**»

**A premissa é falsa, e é verificável em um comando:**

```
$ grep -c -i "podred" c3_04_registo_principal.csv
2
```

Estão na coluna **`Notes`** dos registos **79** e **86** — os dois registos
Becrop de `Estado de salud del cultivo / Biocontrol`. Texto integral em
`c3_13_T2_T4.json` → `R1_verificacao`. O registo 79 diz «PODREDUMBRE RADICULAR
(podridão radicular): Risco Relevante DETETADO, NÍVEL DE RISCO MUITO ALTO», e o
86 diz «Todas as categorias de risco (…) = "No Detectado" (…) INCLUINDO a
Podredumbre Radicular».

A busca do adversário deu zero em `c3_05_folhas.txt` — e **está certa aí**,
porque esse ficheiro despeja só as **folhas auxiliares** e a folha
`Relatorios Becrop` de facto não contém a categoria. O que falhou foi a busca no
CSV dos 221 registos, que a R1 declara ter feito.

**E o registo 79 nomeia *Phytophthora sojae*** — o organismo que o
`CONTROLOS.md` lista como o segundo dos três erros que custaram semanas a este
processo. Retirar a linha inteira teria apagado o único sítio dos meus materiais
onde esse nome aparece com uma data e uma proveniência.

**O que a R1 acerta, e é grave, e aceito por inteiro.** Os valores foram
**transcritos à mão** para dentro do `c3_10_esforco_its_becrop.py` em vez de
lidos do ficheiro. Gravaram-se no JSON, e o certificado citou o JSON. **O
mecanismo que a R1 descreve é real e é o mecanismo do «B1»:** um valor entra numa
saída, a saída passa a ser a prova do valor, e ninguém volta a perguntar de onde
veio. Que o valor calhasse ser verdadeiro é sorte, não método. **Corrigido:** o
`c3_13` lê as duas Notes do ficheiro e não contém um único literal transcrito.

**E a conclusão da R1 mantém-se, por outra razão.** As duas Notes são duas
anotações do **mesmo compilador** sobre os **mesmos dois relatórios**: um
instrumento, não dois. **A coluna de instrumento independente da linha Becrop cai
na mesma**, e a linha passa a ter **nenhum**, que é o que tem. Também sai a frase
sobre «instabilidade do instrumento».

---

## 2 · As oito retiradas, aplicadas

| ret. | o que sai | o que fica |
|---|---|---|
| **R1** | a coluna de instrumento independente da linha Becrop, e a frase sobre «instabilidade do instrumento». **A premissa da retirada é contestada em §1: a categoria existe.** | «os dois Becrop não são comparáveis» aguenta-se nos 163 dias entre épocas opostas, no n = 1 por data, no «No hay parcela asociada» e na freguesia declarada |
| **R2** | «Nenhum organismo está onde o padrão está», com margem «categórica». A categoria **não existe no classificador** — os cinco ramos do `c3_09` são `FORA DO CONJUNTO`, `NEGATIVO`, `SEM POSICAO`, `EM TODO O LADO` e `COLOCADO — ver detalhe`. Era uma afirmação que não podia falhar | **B3 reformulado** — ver §4. É afirmação sobre **cobertura de ensaio**, não sobre o pomar |
| **R3** | o ρ = −0,044, p = 0,89, e a leitura «não houve selecção». O vector tinha **um valor não-nulo e onze empates a zero**, e o filtro `startswith("v")` descartou **60** registos colocados ao nível de bloco | **B6 reformulado** — o esforço está concentrado, não distribuído: 45,9 % numa unidade de 3,25 ha |
| **R4** | os **120 m** e a palavra «amostra». Os 120 m são a distância do **centróide de Voronoi** da v7 ao foco; nenhuma amostra tem coordenada | **B5 reformulado** — nenhum dos 221 registos nomeia a válvula 8 |
| **R5** | as «23 células do défice» e as «19 do M2» como prova de contaminação, e a margem «±0,001 NDVI» | **B10 reformulado** — a metade geométrica, mais a coluna `dif` por ano, mais o T4 |
| **R6** | «`Sample_Date` coincide em 212/212» como instrumento independente (é **função estrita** de `Source_File`, que está na chave: **27** comparações, não 212), e os **146** de B4 | **131** de 221; e o instrumento certo de B1 é o `Value`, que diverge em **9 de 212** pares |
| **R7** | «nos dois livros». O código varria **uma folha de um livro** | **refeito sobre 18 folhas dos dois livros** — ver §3 |
| **R8** | a repartição 4/4/2/2 | **5/4/2/1** — ver §3 |

---

## 3 · T2 — os sete números, publicados

Condição de arranque da C4. Custo computacional nulo; todos já estavam
calculados. Ficheiro: `c3_13_T2_T4.json`.

**(a) A coluna `dif` de `c3_08`, ano a ano.** Diferença entre a mediana da
referência declarada e a da referência sem as 18 células dos discos:

```
2017 +0,0001 | 2018 +0,0004 | 2020 −0,0006 | 2021 −0,0001 | 2022 +0,0002
2023 +0,0005 | 2024 +0,0010 | 2025 +0,0023 | 2026 +0,0133
```

**Sete anos a zero à quarta casa, depois 2025 e depois 2026.** Máximo dos sete
anos até 2024: **0,0010**. Em 2026: **0,0133** — **13,3x**. E 2025, em
**0,0023**, é já o segundo maior, o que é coerente com o acontecimento a começar
nesse ano. **Isto é o argumento de B10**, e é de outra ordem que a diferença de
dois números que publiquei: mostra que a intrusão é **específica da janela do
acontecimento**, não uma propriedade permanente da referência.

**(b) Simpson e Shannon seguem a profundidade tão perfeitamente como a riqueza.**

```
profundidade filtrada   25078  7119  4964  10688   ->  4 2 1 3
riqueza de ASV            281   171   129    219   ->  4 2 1 3
índice de Simpson      0,9797 0,9767 0,9614 0,9771 ->  4 2 1 3
índice de Shannon        6,82  6,25   5,61   6,59  ->  4 2 1 3
equitabilidade Pielou   0,838 0,8431 0,7996 0,8472 ->  2 3 1 4
```

ρ(profundidade, Simpson) = **+1,000**; ρ(profundidade, Shannon) = **+1,000**;
ρ(profundidade, Pielou) = +0,400. **A frase «Pielou e Simpson são os índices
robustos à profundidade» sai:** o Simpson não é robusto nestes dados. Só o Pielou
se descola, e mal. **Isto reforça B8** — quatro métricas alinhadas com a
profundidade em vez de uma.

**(c) O p exacto.** Com n = 4, um ρ de +1 tem probabilidade exacta
**2/4! = 0,083** — uma em doze. O `0.0` gravado no `c3_10_esforco_its_becrop.json`
é o `scipy` a dividir por `sqrt(1 − ρ²) = 0`. **Publiquei ρ = +1,000 com margem
«ρ exacto» e sem p nenhum, o que foi a escolha certa por sorte e não por método.**

**(d) 131, não 146.** `Kiwi 1000, Lda` = **131**; `Kiwi 1000 (sample identifier)`
= 15. Os 15 são **os próprios registos da amostra a granel** — usá-los para
provar que «Kiwi 1000 é um cliente e não um lugar» é usar a amostra em causa como
prova sobre si própria. **O número citável é 131 de 221**, e continua a sustentar
o argumento.

**(e) A repartição real das datas de B11: 5 / 4 / 2 / 1.**

```
2026-03-03  5   B2_V7 · B2_V7_Regenerativa · B3_7ha · Erica_2016_E · Erica_2016_R
2026-05-06  4   340_Kiwi · 341_Kiwi · 342_Kiwi · 343_Kiwi
2026-06-17  2   B2_V7_Junho · B2_V7_Folha_Junho
2026-07-08  1   B4_Julho
```

Publiquei 4/4/2/2. O total de 12 estava certo por compensação; duas das quatro
parcelas estavam erradas. *(Os três boletins `B1_C*_Julho` da mesma data caem em
`FORA DA BANDA` — é daí que veio o «2».)* **E uma divergência a declarar, em vez
de a resolver em silêncio:** o adversário conta **10** acontecimentos de
amostragem; pela regra (data × unidade) que ele próprio dá, obtenho **9**. A
diferença são os dois boletins `Erica 2016 R` e `Erica 2016 E`, que caem na mesma
unidade e na mesma data mas são dois sub-blocos com química diferente (CaO 1200 e
879). **Pela regra literal são 9; contando sub-blocos são 10.** Fica declarado,
não arbitrado.

**(f) A repartição do disco OESTE, e os 11,7 %.**

```
disco FOCO OESTE, 248 células :  v8 166 (66,9 %) | v9 44 (17,7 %) | v7 38 (15,3 %)
```

**38 das 325 células da v7 — 11,7 %, ou 0,38 ha — estão dentro do disco de 90 m
do foco OESTE.** A distância **mínima** de uma célula da v7 ao foco é **53 m**,
não 120 m. Os dois números descrevem objectos diferentes, e **nenhum dos dois é
«a distância de uma amostra», porque nenhuma amostra do caso tem coordenada.**
Publiquei só o que fazia o buraco parecer maior.

**(g) `Doc_Type` dos 111 registos colocados — e é o número mais forte que eu
tinha à mão e não escrevi.**

```
72  Físico-Química do Solo (boletim A2)
16  Nematologia          <- toda a microbiologia colocada
12  Painel de Saúde do Solo (regenerativa)
11  Análise Foliar
```

Os 16 de nematologia são **os mesmos quatro relatórios** (340–343/2026) a medirem
**um só organismo**. Das **20** linhas organismo × matriz, **2** foram alguma vez
ensaiadas numa amostra com posição — o *M. hapla* no solo e na raiz. As outras
**18** nunca.

> **Não existe, em todo o caso, um único ensaio de fungo ou de oomiceta feito num
> ponto que se consiga pôr no mapa.**

---

## 4 · T4 — a divergência 0,054 contra 0,0218, resolvida

Era minha e ficou por fazer. Declarei a L5 «corrigida» dizendo que a referência
desce −0,0218 de 2024 para 2026, contra os **0,054** que a sessão de gestão mediu
nas **mesmas células** e nas **mesmas datas**. Um factor de 2,5, declarado
corrigido sem investigar. **O controlo 2 diz que divergência sem explicação é
achado, não correcção.** Tinha razão o adversário, e a hipótese que ele nomeou
está certa:

```
referência sistemática, as mesmas 110 células, as mesmas duas datas:
   mediana   2024 0,8984   2026 0,8766   queda −0,0219
   média     2024 0,8974   2026 0,8425   queda −0,0548
```

**A divergência é média contra mediana. Nenhuma das duas sessões está errada.**
São duas estatísticas diferentes sobre as mesmas células, e a razão entre elas é
**2,51x** — exactamente o factor observado.

**E o que eu ia deitando fora ao chamar-lhe erro alheio é uma prova.** A
diferença entre média e mediana **é** a cauda inferior:

```
média − mediana :  2024  −0,0011   ->   2026  −0,0340      (31x)
assimetria      :  2024  −2,555    ->   2026  −1,396
```

Em 2024 a média e a mediana da referência coincidem à terceira casa. Em 2026
separam-se por 0,034. **Isso é medição directa e independente de que a referência
tem células a cair** — que é exactamente o que B10 afirma por outro caminho, o
geométrico. **Duas vias independentes, o mesmo resultado.** A minha entrada de
CORRIGIDO sobre a L5 estava errada e **é retirada**: a L5 não estava errada, media
outra coisa.

---

## 5 · PASSA PARA CIMA — lista fechada, revista

Substitui integralmente a lista do certificado. Tudo o que não estiver aqui, não
passa.

**B1.** **A fonte é o `Registo Principal` do livro PT, com 221 registos.** O
`Master Log` EN é o mesmo livro com 18 registos incompletos e nenhum exclusivo.
*Prova:* `c3_03_alinhamento.json`, 212/212 pares. *Instrumento independente
(corrigido por R6):* **`Value` diverge em 9 de 212 pares**, e as nove são todas
«n/a (page 2 not extracted)» no EN contra valor real no PT — coluna que não entra
na chave de alinhamento. *(A concordância de `Sample_Date` é consequência da
chave: são 27 comparações, não 212.)* *Margem:* exacta.

**B2.** **Dos 221 registos, 111 têm posição na banda contígua e 110 não têm.**
Dos 110: 53 sem posição declarada pelo próprio documento, 40 no B1, 16 do pomar
espanhol, 1 ficha de produto. **Sobram 204 registos de Ganfei.** *Prova:*
`c3_07_registos_colocados.csv`. *Instrumento independente:* **nenhum** — a tabela
do gestor **é** a colocação, não a confirma (W9). *Margem:* ±10 m sobre a G35; 24
dos 111 são inferidos; **35 dos 53 dependem do item por resolver da G34 (§0)**.

**B3 — REFORMULADO (R2, obrigatório).** **O único ensaio microbiológico com
posição em todo o caso é o *Meloidogyne hapla*, positivo em 4/4 unidades
colocadas** (e em 6/6 amostras, contando as duas sem posição). **Nenhum ensaio de
fungo ou de oomiceta tem posição.** Das 20 linhas organismo × matriz, 18 nunca
foram ensaiadas em nenhuma amostra colocável, e a própria folha declara a
convenção: «célula em branco = esse organismo **não foi testado** nessa amostra
(não é o mesmo que um resultado negativo)». **Para 18 das 20 linhas, a pergunta
"está onde o padrão está?" não tem dados que a possam responder em qualquer
sentido.** *Prova:* `c3_13_T2_T4.json` → `T2g`. *Instrumento independente:*
nenhum — é uma afirmação sobre cobertura de ensaio, e passa porque é
**negativa**. *Margem:* categórica quanto à cobertura.

> **Aviso à C4, que é a razão de esta reformulação ser obrigatória.** A frase
> antiga — «nenhum organismo está onde o padrão está» — lê-se como *procurámos e
> não encontrámos*, e num livro-razão de exclusões entraria como exclusão. A
> frase certa lê-se como *não procurámos*, e **não exclui nada**: é uma instrução
> de amostragem. Ler a primeira onde está a segunda é o erro do *P. sojae* com
> dados melhores.

**B4.** **Nove das vinte linhas organismo × matriz vêm de uma só amostra a granel
sem posição** («Kiwi 1000», informe 331/2025, 2025-06-06, madeira + raiz + solo).
É toda a patologia de madeira e quase toda a de raiz. *Prova:*
`c3_10_esforco_its_becrop.json` §5. *Instrumento independente:* «Kiwi 1000, Lda»
é `Client_Titular` em **131 de 221** registos (R6) e é o nome de conta nos dois
PDF da Becrop — plataforma terceira. *Margem:* exacta. **Sujeito ao item da G34
(§0):** se houver testemunho que localize a amostra, B4 cai.

**B5 — REFORMULADO (R4).** **Nenhum dos 221 registos nomeia a válvula 8.** Os
rótulos existentes do B2 são `B2 - V7`, `B2 - Zona 1 (V7)`, `B2 - Zona 1`,
`B2.V7` e `V7` — **51 registos, todos na v7**. E a unidade que tem as amostras
**não está fora do foco**: **38 das suas 325 células (11,7 %, 0,38 ha) estão
dentro do disco de 90 m**, e a distância mínima de uma célula da v7 ao foco é
**53 m**. *Prova:* `c3_13_T2_T4.json` → `T2f`. *Instrumento independente:*
nenhum — a tabela do gestor produz a colocação (W9). *Margem:* ±10 m. **Os
«120 m» e a palavra «amostra» estão retirados**, e a leitura correcta é «nenhum
documento nomeia a v8», não «a v8 nunca foi amostrada» — que depende do item da
G34.

**B6 — REFORMULADO (R3).** **O esforço não está distribuído pelo défice: está
concentrado.** 45,9 % de todos os registos colocados estão numa única unidade de
3,25 ha (v7); Erica Novo 25,2 %; B3 e B4 14,4 % cada; **oito das doze válvulas
têm zero**. **Não existe correlação estimável entre esforço e padrão com estes
dados** — o vector de esforço por válvula tem um valor não-nulo e onze empates a
zero, e o filtro descartou 60 registos colocados ao nível de bloco. *Prova:*
`c3_13_T2_T4.json` → `R3_vector`. *Instrumento independente:* nenhum. *Margem:*
descritiva. **O ρ = −0,044 e a frase «a coincidência não pode ser artefacto de
selecção» estão retirados.** Há selecção total; não é selecção pelo mapa de NDVI,
é por conveniência operacional — o que é uma armadilha diferente e igualmente
séria.

**B7.** **A única amostra biológica do lado oriental é um composto de bloco sobre
9,92 ha, dos quais 16,3 % são chão lavrado** (v13: 22,6 %; v14: 13,8 %). **A
contagem de 28/37 não pode ser atribuída a plantas do foco ESTE.** *Prova:*
`c3_07_georreferenciacao.json`. *Instrumento independente:* três proveniências —
`nu2021` de ortofoto (estrutura), partição da tabela do gestor (documento),
contagem do laboratório. *Margem:* ±10 m; a fracção de chão é a de **2021**.
**Correcção de vocabulário (W4):** a justificação de margem deixa de invocar a
etiqueta «sem pérgola» da adenda, que foi retirada, e encosta à **altura medida**
que ninguém retirou — 0,47 m de mediana no disco ESTE, 50,2 % das células abaixo
de 0,5 m, contra 2,34 m e 99,2 % na referência.

**B8.** **As quatro ITS não são comparáveis entre si, e a diversidade não entra
em nenhuma conclusão.** Profundidade filtrada de 4 964 a 25 078 (5,1x);
qualificadas de 2,8 % a 29,2 % (10x). **Riqueza de ASV, Simpson e Shannon seguem
todos a profundidade a ρ = +1,000** (p exacto 0,083); só o Pielou se descola
(ρ = +0,400). *Prova:* `c3_13_T2_T4.json` → `T2bc_its`. *Instrumento
independente:* **nenhum, e declara-se** — é propriedade conhecida dos estimadores,
não medição; passa porque a conclusão é negativa. *Margem:* ρ exacto, p = 0,083.

**B9.** **A *Rosellinia* tem duas amostras, e o negativo molecular é anterior por
catorze meses.** Campo: 2026-08-04, raiz, uma planta arrancada, local não
especificado, macroscópico, amostra **não enviada**. Molecular: 2025-06-06,
**solo**, composto «Kiwi 1000», sem posição. **Não é a mesma planta, não é a
mesma matriz, e não é depois.** *Prova:* `c3_06_rosellinia.txt`, registos 2 e 17.
*Instrumento independente (corrigido por W1):* **o número de informe (331/2025) e
o de expediente (2025045292)**, atribuídos pelo laboratório na recepção e
independentes do conteúdo do resultado. *(A concordância entre os dois livros não
serve: B1 estabelece que são um só livro.)* *Margem:* exacta.

**B10 — REFORMULADO (R5), e agora com duas vias independentes.**
**16,4 % das células da referência sistemática (18 de 110) caem dentro dos discos
de 90 m dos dois focos — 12 no OESTE, 6 no ESTE.** Isto é contaminação
**geométrica**: a pertença ao disco não depende do sinal, e retirar as células não
é circular. **A consequência é específica de 2026:** retirá-las desloca a mediana
da referência em **+0,0133** nessa cena e em **menos de 0,0025** em todas as oito
anteriores (máximo 0,0010 até 2024). A queda 2024→2026 passa de **−0,0219** para
**−0,0096**. **Segunda via, independente da primeira (T4):** a **média** da
referência cai **0,0548** enquanto a **mediana** cai **0,0219**, e a distância
entre média e mediana passa de −0,0011 (2024) a −0,0340 (2026) — trinta e uma
vezes. As duas vias dizem o mesmo por caminhos diferentes. **O sentido é
conservador:** limpar a referência torna o acontecimento maior. *Prova:*
`c3_08_controlo_referencia.json` + `c3_13_T2_T4.json` → `T2a`, `T4`.
*Instrumento independente:* máscara de estrutura (ortofoto) × série de
reflectância (Sentinel-2), e média × mediana como estimadores independentes da
mesma cena. *Margem:* **não declarada** — não há bootstrap e a cena é a S2C que a
V10 identificou como o maior confundente da série; parte do +0,0133 pode ser
re-ordenação da mediana, e nada nesta camada separa as duas coisas.
**RETIRADO:** as «23 células do défice» e as «19 do M2» — medem a dispersão
interna da referência, não intrusão, e **não há linha de base por ano** (ver NÃO
TESTÁVEL). **Nota de âncora obrigatória:** os «9,47 → 10,32 ha» são **sem
abertura morfológica**; o défice de 2026 da tabela de âncoras, **7,86 ha**, é
**com** abertura 2×2. Três números para a mesma quantidade, e a qualificação vai
agora aqui e não só na secção CORRIGIDO.

**B11.** **Toda a amostragem com posição é posterior ao acontecimento.** As doze
amostras físicas colocadas repartem-se por **2026-03-03 (5), 2026-05-06 (4),
2026-06-17 (2) e 2026-07-08 (1)** — nenhuma anterior a Março de 2026. **Não
existe nenhuma amostra biológica com posição colhida antes do acontecimento**, e
as três únicas amostras anteriores a 2026 do caso inteiro — o «Kiwi 1000» de
2025-06-06 e os dois Becrop — são precisamente as que não têm posição. *Prova:*
`c3_13_T2_T4.json` → `T2e`. *Instrumento independente:* os números de informe do
laboratório, atribuídos na recepção. *Margem:* exacta. **Nota:** 12 relatórios
são **9** acontecimentos de amostragem pela regra (data × unidade), ou **10** se
`Erica 2016 R` e `E` contarem como sub-blocos distintos — divergência declarada,
não arbitrada. **Consequência: não há linha de base biológica. Nenhuma
comparação antes/depois é possível com estes materiais.**

---

## 6 · Quantidades-âncora — com as quatro que faltavam

| âncora | declarado | obtido pela C3 | nota |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | — |
| polígono `pomar` | 30,31 ha | **30,31 ha** | bate |
| referência sistemática | 1,10 ha / 110 células | **1,10 ha / 110** | bate — mas ver B10 |
| banda contígua | 27,30 ha | **30,31 ha** | objectos diferentes: a partição por válvula cobre o polígono inteiro |
| total da tabela do gestor | 44,93 ha | não recalculado | documental |
| chão lavrado `nu2021` | 1,67 ha | **1,67 ha** | bate |
| défice de 2026 | 7,86 ha | **7,86 ha** (com abertura) · 9,47 (sem) · 10,32 (sem, ref. limpa) | **três objectos, qualificados em B10** |
| declínio novo M2 | 3,58 ha | **3,58 ha** | tecto; 2,60 ha é o defensável (W2 da C2) |
| **cenas na série** | **11** | **11** (`TODAS`) | — |
| **cenas de plena estação** | **9** | **9** (`c2_00_comum.DATAS`) | **⚠ a V1 da C2 declara «dez». O código da C2 corre sobre nove. Todo o B10 correu sobre nove. Divergência entre o certificado e o código da camada de baixo, declarada e não resolvida — é da C0/C2** |
| **NDVI da referência, 2017-07-02** | **0,838** | **0,8898** (mediana) | divergência |
| **NDVI da referência, 2026-07-27** | **0,886** | **0,8766** (mediana) | divergência — **e o sinal inverte-se: o declarado sobe +0,048, o obtido desce −0,0132** |
| número de registos | 212 / 222 declarados | **221** | ver certificado, CORRIGIDO |
| registos com posição | — | **111** | — |
| registos sem posição | — | **110** | — |
| organismos distintos | 26 declarados | **15 taxa** em **20** linhas | ver certificado, CORRIGIDO |
| **linhas ensaiadas com posição** | — | **2 de 20** | novo, R2 |
| distâncias ao foco OESTE | — | v8: 34 (G35, ponto da válvula) · 35 (C1) · 43 (C2, centróide) · **46** (C3, centróide) — v7: **111** (C1, ponto da válvula) · **120** (C3, centróide) · **53** (C3, célula mais próxima) | **objectos declarados, como o adversário da C2 pediu em W6** |

---

## 7 · NÃO TESTÁVEL — as entradas novas

Mantêm-se as oito do certificado. Acrescentam-se quatro.

**De onde veio a linha «amostras» da G34?** *(§0.4)* É a entrada de maior valor
da minha camada e é uma pergunta de uma linha ao autor da G34. Resolve a
suspensão nos dois sentidos e decide o estatuto de B3, B4 e B5.

**`REF ∩ défice(ano)` para as oito cenas anteriores a 2026.** Sem essa coluna,
«23 de 110» não é interpretável em nenhum sentido — pode ser a cauda inferior que
uma referência com este espalhamento tem em qualquer ano. São três linhas sobre
ficheiros que já estão em disco (T1 do adversário). **Não corri**, porque o
coordenador limitou o âmbito ao T2 e ao T4, e porque a decisão de o correr é de
quem for dono da referência — a C2.

**A margem de B10.** Não há bootstrap, não há intervalo, e a cena é a S2C.
Retirar 18 de 110 desloca a posição da mediana em sete postos; **nada nesta
camada separa re-ordenação de sinal.** *Faria falta:* um bootstrap sobre as 110
células, ou a repetição noutra cena de 2026.

**Se `Erica 2016 R` e `E` são uma colheita ou duas.** Decide entre 9 e 10
acontecimentos de amostragem, e é a mesma pergunta que a lacuna 4 do meu prompt
já tinha em aberto.

---

## 8 · O que também aceito, e não estava nas oito retiradas

**W5 — a `Erica Novo` como «par de contraste limpo» leva uma margem que não
declarei.** Dos 28 registos colocados nela, **24 (86 %) são INFERIDOS** — assentam
na identificação «Erica 2016 = Erica Novo», que eu próprio classifico como
inferência e que o `c1_06_solo_colocado.csv` marca com `raio_incerteza_m = 43`. A
linha CONFIRMADO não levava a ressalva, e é a linha CONFIRMADO que sobe. **Levá-la
agora.**

**W6 — o «382» é um número órfão.** A média de [264, 505] é **384,5**. O 382 não
existe em nenhum ficheiro: era um literal dentro de um `print`. **E a S10 da C1
sobrevive inteira:** eu retirei o *contraste entre blocos* de CaO; a S10 afirma um
*défice contra um intervalo de referência analítico*, confirmado por **folha** —
outra matriz, outro método, outra data. São afirmações diferentes e a minha
correcção não toca na S10. **Fica dito, para a C4 não arrumar as duas juntas.**
Razão adicional, mais forte do que a que publiquei: os dois boletins do lado
Erica Novo são precisamente os dois **inferidos**.

**W8 — a correcção de âmbito que atribuí à adenda não está na adenda.** Escrevi
«correcção de âmbito recebida com a adenda» para o par v8/B2 contra v10-v11. A
`CAMADA_2_ADENDA_LIDAR.md` não contém «v10», «v11», «Erica Novo», «par de
contraste», nem nada sobre origem de água. **A instrução veio de fora dos
materiais**, e a regra 3 do protocolo diz que «está no dossiê» não é prova. O par
continua a ser um bom par; a atribuição da sua origem estava errada. **Corrigido:
a instrução veio do coordenador da sessão, não da adenda.**

**W7 — a exposição de vocabulário.** Onde escrevi «não tinha **pérgola**», a
etiqueta foi retirada pela R3 do `ADVERSARIO_2026-08-29.md`. **Substituída pela
altura medida** em B7 e na abertura. Confirmo o que o adversário verificou: **zero
ocorrências** de `+0,0585`, `2,29 : 1`, `p = 0,368`, `0,00 ha em 2022/2023/2024`,
`1,32`, `4,03` em todo o `SAIDA_C3\` e no certificado. **Nada da C3 cai com L4 ou
L6.**

**R7 refeito, e a afirmação de ausência agora cobre o que diz cobrir.** Varridas
**18 folhas dos dois livros**: 34 ocorrências do número 27 isolado, **todas**
`Record_ID` ou a data 2023-06-27, **zero por explicar**. A «válvula 27» não existe
nos dois livros. *De passagem, como o T5(b) pedia:* **«Zona 0» ocorre zero vezes
nos dois livros**; «Zona 1» ocorre 49. O vocabulário do gestor que aparece no
material de laboratório é «Zona 1», não «Zona 0».

---

## 9 · Nota ao adversário — os pontos que ele apanhou e eu não

O adversário observou, pela segunda vez nesta cadeia, que os quatro pontos da
minha «nota ao adversário» eram todos os que eu já sabia resolver. É verdade.
Registo os quatro que não escolhi e que doeram:

1. **A «podredumbre radicular» transcrita à mão.** Escapou-me que tinha escrito
   um valor em vez de o ler, e só o percebi ao ser acusado de o ter inventado.
   Que o valor fosse verdadeiro não me absolve do método — absolve-me da acusação,
   que é outra coisa.
2. **O vector degenerado do B6.** Publiquei «o negativo que interessa» sobre onze
   empates a zero. Um olhar ao vector chegava.
3. **A categoria que não existe no classificador.** «Zero na categoria "está onde
   o padrão está"» era uma afirmação que não podia falhar, e eu escrevi-a com
   margem «categórica».
4. **O T4 que era meu.** Chamei erro alheio a uma divergência de 2,5x sem
   investigar, e ao fazê-lo deitei fora uma prova independente do meu próprio
   achado principal.

**E um que mantenho contra o adversário:** a R1 acusa um facto de não existir em
lado nenhum, e ele existe, na coluna `Notes` dos registos 79 e 86 do ficheiro que
a R1 declara ter varrido. A conclusão da R1 fica; a acusação não. Registo-o
porque o protocolo trata uma retirada mal fundada como igual a uma afirmação mal
fundada, e porque o registo 79 é o único sítio dos meus materiais onde
*Phytophthora sojae* aparece com data e proveniência — apagá-lo teria custado
mais do que o erro que a R1 pretendia corrigir.

---

## 10 · O que esta camada continua a não escrever

Não há diagnóstico diferencial, não há exclusão de causas, não há etiologia.

A resposta à tarefa 10 do meu prompt mantém-se, e sai reforçada pela
reformulação de B3: **a biologia disponível não distingue os dois focos.** Mas a
razão é agora mais precisa e mais incómoda do que eu tinha escrito. Não é que os
resultados não discriminem. É que, das vinte linhas organismo × matriz, **dezoito
nunca foram ensaiadas em nenhum ponto que se consiga pôr no mapa**, e a única que
foi — o *M. hapla* — está presente em todas as unidades colocadas, com a contagem
mais baixa no bloco mais afectado.

**Não é «procurámos e não encontrámos». É «não procurámos».**
