# Adversário da Camada 5 — Decisão

29-08-2026. Último documento da cadeia. Ataca `CAMADA_5_CERTIFICADO.md` e
`SAIDA_C5\`.

**O que li.** `ADVERSARIO_PROMPT.md`, `PROTOCOLO.md` (com a emenda de hoje à
regra 1), `CONTROLOS.md`, `CAMADA_3_ADVERSARIO.md`, `CAMADA_4_ADVERSARIO.md`,
`_MULTIVERSO\ADVERSARIO_H1.md`; o `CAMADA_5_CERTIFICADO.md` inteiro; e o código
e os CSV de `SAIDA_C5\` linha a linha. Para arbitrar afirmações do certificado
sobre ficheiros de outras camadas li também, **sem recomputar nada**, o
cabeçalho e os campos de evidência de `SAIDA_C4\c4_razao_exclusoes.csv`, o
`c4_01_numeros.json`, as listas fechadas de C0-R2, C1, C2, adenda de LiDAR,
C3-R2 e C4, e verifiquei a existência de dois ficheiros (`landsat.json` existe;
`c2_12_prom_2025.npy` não existe em lado nenhum).

**Não modifiquei nada em `ganfei_s2\`, `SAIDA_C5\` nem `_VALIDADE_GESTAO\`.**

---

## SUMÁRIO — o que muda

| alvo | veredicto |
|---|---|
| **re-etiquetagem das 59** | **o juízo linha a linha aguenta; a prova de que o é, não.** O script **não lê nenhum dos campos de evidência** que o cabeçalho diz que lê. O instrumento independente declarado em CONFIRMADO C1 **não existe no código.** |
| **«24 mal rotuladas, 11 encontradas»** | **corrige-se para «18 mal rotuladas, 10 encontradas + 1 por confirmar»**, com o critério explícito. As restantes 6 são re-descrições correctas, não correcções. |
| **«três exclusões, não sete»** | **são DUAS.** O INS-01 não tem instrumento independente na acepção do Controlo 1: quatro corridas de NDVI sobre as mesmas cenas são concordância máquina-a-máquina. |
| **ABI-04 → EXCLUÍDA-INTERNA** | **retira-se o «JÁ FECHADA».** É a categoria intermédia que ainda se lê como resolvida, e o campo do próprio CSV diz «instrumento independente: nenhum». |
| **as quatro EXCLUÍDA-LOCAL** | **aguentam como não-detecções, não como exclusões.** Três declaram «instrumento independente: nenhum»; a quarta declara um **número de expediente**, que não é instrumento. |
| **desenho de amostragem** | **os dois pares sãos passam** (verifiquei: v6 e v17 são mesmo as únicas duas de doze com os três indicadores a 0,0). **O transecto não passa como está.** **Falta o painel foliar no ficheiro.** **U2 não tem controlo de proximidade.** |
| **`SUSTENTADA-LOCAL`** | **passa. Nenhuma linha subiu de estatuto.** Mas a categoria parou uma linha antes do fim: o INS-03. |
| **rejeição de F6 e F5** | **certa, e substancialmente completa.** Duas das cinco regras salvas tinham factos retirados por razão declarada, e a rejeição não pede a retirada dos ficheiros. |
| **«a decisão não fecha»** | **é honestidade, não evasão** — com **uma excepção**: a REG-01 não é condição de arranque da campanha e tinha de ser. |
| **margem sobre a paisagem** | **certa no que diz, insuficiente no que não diz.** O negativo da mata é subpotente ao nível que interessa: não distingue «não caiu» de «caiu tanto como o pomar». |
| **transversal C0–C5** | **de 92 factos nas sete listas fechadas, 38 têm instrumento de outra natureza.** A C5 contribui **zero**. |

**Veredicto em uma linha:** o certificado da C5 é o trabalho mais honesto da
cadeia e o mais frágil no sítio onde diz que é forte. **Segue para o relatório
com sete retiradas e cinco margens.** **O desenho de amostragem NÃO pode ser
executado como está** — por três defeitos concretos e reparáveis, nenhum deles
caro.

---

## 0 · A EMENDA À REGRA 1 — a C5 foi a primeira camada debaixo dela

**Cumpriu-a, e é preciso dizê-lo com a mesma clareza com que direi o resto.**
Verifiquei o rasto, não a declaração de leitura:

- **As dez alterações obrigatórias do `CAMADA_4_ADVERSARIO.md` estão todas
  aplicadas** e cada uma leva a sua marca na coluna `origem_da_alteracao`
  (R2 → BIO-10/11/12/14; R3 → INS-01; R5 → BIO-16; R6 → ABI-08; R7 → INS-02;
  R8 → ABI-04; R9 → ABI-11; R10 → ABI-03/REG-02/INS-04; R1 → §2.1 e a coluna
  `procurado_onde`). Isto é verificável no ficheiro, não na prosa.
- **A parametrização retirada não sobreviveu ao transporte.** Procurei-a:
  `530476`, `11,4`, `3,98`, `válvula 27`, `Zona 0`, `IoU`, `15–40 m`,
  `37 m/ano` — **zero ocorrências** no `c5_reetiquetagem.csv`. O `ambito` do
  CSV da C4 dizia, para BIO-10/11/12/14, «núcleo redondo de 3.98 ha, centro
  E530476 N4655046, a 11.4 m do centro do foco OESTE». A C5 reescreveu o campo.
  **É a primeira vez em toda a cadeia que uma retirada viaja para cima em vez
  de ser reencontrada por um adversário posterior.**
- O `−0,048` aparece uma vez, e aparece **para dizer que não vem de nenhuma das
  quatro corridas**. É uso correcto.

**A emenda funcionou.** Uma linha de protocolo produziu mais correcção
transportada do que as dezassete retiradas anteriores somadas.

**Uma reserva, e não é retórica.** O `c5_amostragem.csv` carrega **doze vezes**,
no campo `margem` das doze linhas do T1, o texto «NÃO se usa o centro E530476
N4655046». É um aviso, não um uso. Mas este é o ficheiro que vai para o
terreno, e uma coordenada UTM escrita doze vezes numa coluna de um CSV é uma
coordenada que alguém pode ler como alvo. **Substituir por «não se usa a
coordenada de núcleo da corrida B (retirada — ver §2.2 do certificado)».**
Custo: uma cadeia de caracteres.

---

# PARTE 1 · FACTOS A RETIRAR DO PASSA PARA CIMA

Por ordem de gravidade, seguindo a ordem de ataque pedida.

---

## R1 · A re-etiquetagem não é uma re-derivação. O código não lê nenhum dos campos que o cabeçalho diz que lê.

**Este é o achado do documento, e é a regra de higiene que o `CLAUDE.md` deste
projecto nomeia como a que já custou mais caro: ler o cabeçalho e o código
juntos.**

Cabeçalho de `c5_01_reetiquetagem.py`, linhas 17-30:

```
REGRA DE DERIVACAO — a etiqueta nova sai dos CAMPOS DE EVIDENCIA, nao da antiga
------------------------------------------------------------------------------
Para cada linha le-se `ambito`, `prova`, `instrumento independente`,
`margem e leitura` e `o que a fecharia`, e aplica-se:
   houve ensaio em Ganfei? -- nao --> NUNCA PROCURADA
                           +-- so em Espanha --> SO FORA DE GANFEI
                           +-- sim, POSITIVO, um ponto, sem par --> ...
```

**O código a seguir não lê nenhum desses campos.** O ficheiro de entrada tem
nove colunas:

```
id ; classe ; causa ; estatuto ; ambito ; prova (certificado e numero) ;
instrumento independente ; margem e leitura ; o que a fecharia
```

e o script usa exactamente quatro — `r["id"]`, `r["classe"]`, `r["causa"]`,
`r["estatuto"]` — todas na mesma linha de escrita (linha 805). **As cinco
colunas de evidência nunca são abertas.** A árvore de decisão do cabeçalho não
está implementada em lado nenhum: as 59 etiquetas são um dicionário `R = {}`
escrito à mão, chave a chave, ao longo de 700 linhas.

**Três consequências, e a segunda é a que obriga a retirar.**

**(a) O cabeçalho descreve uma operação que o código não faz.** É a mesma
estrutura exacta do `fazer_masks_v2.py` — cabeçalho a afirmar polígonos
geográficos, código a derivar do sinal — que o `CLAUDE.md` regista como tendo
passado por quatro auditorias. Aqui o sentido do erro é benigno (o cabeçalho
promete mais rigor do que o código executa, não menos), mas o mecanismo é
idêntico e a auditabilidade perde-se do mesmo modo.

**(b) O instrumento independente declarado em CONFIRMADO C1 não existe.** O
certificado escreve, na coluna «instrumento independente» da sua própria tabela
CONFIRMADO:

> «**SIM** — a re-derivação usa os campos `ambito`/`prova`/`margem`, que são
> independentes da coluna `estatuto` que se está a testar»

**É falso contra o ficheiro.** A re-derivação usa a coluna `estatuto` (escreve-a
como `estatuto_C4`) e não usa `ambito`, `prova` nem `margem`. O Controlo 1 diz
que um facto sem instrumento independente vai para NÃO TESTÁVEL. **Retira-se o
«SIM» de C1 e substitui-se por «não — é juízo de uma sessão, sem instrumento».**
Que é, aliás, exactamente o que a própria nota 3 ao adversário confessa
(«a classificação é minha e não foi verificada por ninguém… isto é N = 1»).
**A confissão está certa; a linha do CONFIRMADO contradiz a confissão.**

**(c) O CSV de saída deita fora as colunas de evidência.** As dezasseis colunas
de `c5_reetiquetagem.csv` não incluem `prova (certificado e numero)` nem
`instrumento independente`. O adversário da C4 exigiu partir `estatuto` em
`estatuto` + `procurado_onde` e acrescentar `n` e `poder`: a C5 fez as três
coisas — **e perdeu duas colunas no mesmo movimento.** Quem receber o
livro-razão re-etiquetado, que é o produto que viaja para o relatório, **deixa
de poder ver a prova de cada linha e o instrumento que a sustenta.** Num livro
de exclusões isso é o inverso do que se pretendia. **Correcção: transportar as
cinco colunas de origem para o CSV de saída. Custo: cinco entradas numa lista.**

**Nota de justiça.** Nada disto diz que os 59 juízos estão errados. Verifiquei
os que consegui arbitrar contra os campos da C4 e **não encontrei nenhum
contradito pela evidência da linha**. O que se retira é a afirmação de que a
operação é uma re-derivação verificável, e o instrumento independente que dela
se reclamou.

---

## R2 · «24 mal rotuladas, 11 encontradas» corrige-se para 18 e 10 + 1. E a correcção é no sentido de a C5 ter sido mais dura do que o material aguenta.

A C5 pergunta-se, na nota 3, se a sua contagem mais dura vem de rigor ou de um
classificador que sabe que vai reportar «pior». **É rigor em dezoito casos e é o
segundo efeito em seis.** Percorridas as 41, com o critério declarado pela
própria C5 — «a etiqueta “ninguém procurou” é falsa para esta linha»:

**Mal rotuladas sem discussão — 18:**

| linhas | n | porquê a etiqueta é falsa |
|---|---|---|
| BIO-01…09 | 9 | positivo de laboratório em Ganfei. «Ninguém procurou» é o contrário do que aconteceu. |
| BIO-17 | 1 | medido em cinco unidades, positivo em todas. |
| GES-01 | 1 | corrida, e o único instrumento que a data contraria-a em parte. |
| GES-02 | 1 | corrida, e os números favorecem-na. |
| GES-03 | 1 | constrangida por LiDAR de 06-07-2025. |
| GES-06, GES-07 | 2 | não são causas candidatas; inflacionam o 41 e o 59. |
| REG-01 | 1 | procurou-se, com o instrumento que não resolve. |
| INS-05 | 1 | leitura retirada; não é causa. |
| REG-03 | 1 | resolvida — **mas ver abaixo.** |

**Re-descrições correctas, que não são correcções de rótulo — 6:**

- **BIO-15, 18, 19, 20, 21 (5).** O campo da própria C5 diz «**0 pontos de
  Ganfei**… ZERO informação sobre Ganfei em qualquer sentido». Para Ganfei,
  «não testada» é **literalmente verdadeira**, e o estatuto operativo é
  idêntico a NUNCA PROCURADA. A re-etiqueta acrescenta um aviso valioso — que
  existe material espanhol rejeitado que alguém pode ler como cobertura — mas
  **não corrige um erro de rótulo, acrescenta uma armadilha ao rótulo certo.**
- **BIO-13 (1).** «NÃO TESTADA» é literalmente exacta: a amostra foi colhida e
  **nunca foi enviada**. O que é falso é a legenda «ninguém procurou» —
  alguém observou. É a linha mais defensável das seis e mesmo assim é
  re-descrição, não correcção.

**Retira-se «24» e passa a «18 mal rotuladas + 6 re-descritas».** A distinção
importa porque «24 mal rotuladas» é a frase que vai viajar, e ela diz ao leitor
que vinte e quatro linhas estavam erradas. **Dezoito estavam.**

**E «11 encontradas» retira-se para «10 encontradas + 1 por confirmar».** As
onze são BIO-01…09 (9) + BIO-13 + BIO-17. **A coluna `resultado` de BIO-13, no
CSV da própria C5, diz «POSITIVO macroscópico, por confirmar».** Contá-la entre
«procuradas e ENCONTRADAS em Ganfei» é a mesma operação que a C5 diagnosticou
duas páginas antes: *a prosa cuidada não sobrevive à agregação, e é a agregação
que viaja*. **A C5 nomeou o mecanismo e cometeu-o um nível acima.**

**Uma linha que não pertence a esta contagem por outra razão: REG-03.** A sua
`origem_da_alteracao` diz «medição do coordenador de 29-08-2026». **Não foi
re-derivada de nenhum campo da C4** — mudou porque chegou instrumento novo a
meio da corrida. É a única das 41 cuja alteração não vem da operação que o
capítulo 1 descreve, e o capítulo 1 não o distingue.

---

## R3 · São DUAS exclusões, não três. O INS-01 não tem instrumento independente.

A peça central do certificado — «a C4 publicava sete; são três» — está no bom
sentido e não vai longe o suficiente.

**ABI-01 e ABI-02 aguentam limpas, e digo-o com a mesma clareza.** Declive:
0,336/0,406/0,427 graus, todos abaixo de 0,5, **LiDAR/MDT contra série óptica**.
Posição topográfica húmida: hipótese fixada antes de correr, na direcção certa,
contradita com ρ da cota negativo nas onze cenas, p < 1e-24, ~2200 células,
**MDT contra Sentinel-2**. São as duas melhores linhas de todo o livro-razão e
sobrevivem a este ataque sem margem nova.

**INS-01 não aguenta o estatuto.** O campo de instrumento independente da C4,
que a C5 aceitou sem o rever, diz:

> «SIM — quatro corridas independentes, com personas e desenhos diferentes, que
> é a forma de agregação que Botvinik-Nezer 2020 estabelece»

**Quatro corridas independentes são quatro analistas, não dois instrumentos.**
O `CONTROLOS.md` é literal: «*Um valor de NDVI não se confirma com outro cálculo
de NDVI. Confirma-se contra a ortofoto, contra o SAR, contra a fotografia de
campo, contra um documento, ou contra observação directa.*» E o `CLAUDE.md`:
«*Machine-vs-machine agreement measures [reliability] only, and must never be
reported as [validity].*» Botvinik-Nezer 2020 resolve **variabilidade
analítica** — que é o problema 3 da tipologia do `CLAUDE.md`, a inferência. O
viés de calibração do S2C é um **facto sobre o sensor**, e um facto sobre um
sensor não se estabelece correndo o mesmo sensor quatro vezes com quatro
personas.

Pior: as quatro corridas medem o degrau **fora do pomar**, e o próprio campo
regista que aí «**sensor e ano estão confundidos**». Quatro medições
emparelhadas de um par confundido dão quatro estimativas do mesmo par
confundido. **O que desconfunde sensor de ano é outro sensor no mesmo ano — e
está em disco.**

**Retira-se:** «TRÊS estão excluídas com instrumento independente e desenho
falsificável». **São DUAS — ABI-01 e ABI-02.** O INS-01 passa a
**EXCLUÍDA-CONDICIONAL**, condicionada à certificação da série Landsat, pela
mesma operação e pela mesma razão com que a C5 pôs o INS-02 em condicional.

**Consequência sobre a P1 e sobre o §6 NÃO PODE 5:** onde o relatório dissesse
«São três», passa a dizer **«São duas, e uma terceira fica condicionada a um
ficheiro que já está em disco»**. O sentido continua a ser o da C5 — mais duro
do que o publicado — e é a segunda vez neste documento que a C5 não foi dura
que baste.

**Nota sobre ABI-02, que a C5 anunciou corrigir e não corrigiu.** O certificado
escreve: «*a ressalva do TWI estava no campo de texto livre e a coluna dizia
EXCLUÍDA — passa a estar na coluna*». **Não passou.** No
`c5_reetiquetagem.csv`, o `estatuto_C5` de ABI-02 é `EXCLUIDA` e o `decisao_C5`
é `JA FECHADA`; a perna do TWI, que a própria linha classifica «**NUNCA
PROCURADA por falta de gama do instrumento**», continua a viver no texto livre.
Não foi criada linha nenhuma. **É, literalmente, o defeito 3.3 do adversário da
C4 — a disciplina no texto livre, o estatuto na coluna — repetido na mesma
frase em que se anuncia a sua correcção.** Custo da correcção verdadeira: uma
linha `ABI-02b`.

---

## R4 · ABI-04 é a categoria intermédia que ainda se lê como resolvida. Retira-se o «JÁ FECHADA».

O ataque pedia que eu verificasse se alguma das quatro que caíram devia ter
caído mais fundo. **Três caíram bem. Uma não.**

| linha | caiu para | continua aberta? | veredicto |
|---|---|---|---|
| BIO-16 | INCONCLUSIVA | sim (`NAO PROCURAR`, não excluída) | **bem** |
| ABI-08 | NUNCA PROCURADA | sim | **bem, e é a queda mais funda e mais correcta do documento** |
| INS-02 | EXCLUÍDA-CONDICIONAL | sim (`PROCURAR` — uma linha à C0) | **bem** |
| **ABI-04** | **EXCLUÍDA-INTERNA** | **NÃO — `decisao_C5 = JA FECHADA`** | **mal** |

O campo da C4 para ABI-04 diz «instrumento independente: **nenhum** — é a mesma
série óptica reagrupada». A C5 **cita esta frase** na sua própria nota, invoca
o Controlo 1 — «*o Controlo 1 manda que um facto sem instrumento independente
não passe como excluído sem marca*» — e depois **põe a marca e fecha a linha na
mesma.** O Controlo 1 não manda pôr marca. Manda mandar para NÃO TESTÁVEL:

> «Se não houver instrumento independente disponível, o facto vai para NÃO
> TESTÁVEL, **não** para PASSA PARA CIMA.»

E a linha é consequente: a C5 escreve que **é na v8 que está a maior anomalia
de radar do caso**, e a v8 é uma válvula. Um teste de agrupamento por válvula
sem instrumento independente, dado por fechado, é o mecanismo pelo qual a
hipótese de rede de rega sai da lista sem nunca ter sido testada contra nada de
fora do óptico.

**Retira-se `JA FECHADA` de ABI-04.** Passa a `PROCURAR`, custo **NULO**: o
esquema da rede e o registo de avarias vêm no mesmo pedido de documentos da
acção 2 do §4. **E a contagem «5 já fechadas» passa a 4.**

---

## R5 · As quatro EXCLUÍDA-LOCAL não aguentam o verbo «excluída». A C5 previu-o na sua nota 5 e tinha razão.

A nota 5 ao adversário pede-me explicitamente que ataque as quatro em vez de as
elogiar, porque três documentos as elogiaram e ninguém as atacou. **Ataquei-as,
e a confissão estava justificada.**

Os campos de evidência da C4, que a C5 não leu em código:

| linha | instrumento independente declarado |
|---|---|
| **BIO-10** *Armillaria* raiz | **nenhum** |
| **BIO-11** *Armillaria* solo | **nenhum** (o segundo negativo é Ribadumia, rejeitado) |
| **BIO-14** oomicetas solo | **nenhum** |
| **BIO-12** *Rosellinia* solo | «**o número de informe (331/2025) e o de expediente (2025045292)**, atribuídos pelo laboratório na recepção» |

**Três das quatro declaram não ter instrumento independente**, e a quarta
declara um **número de expediente**. Um número de expediente prova que o
documento existe e que a amostra deu entrada. **Não é um instrumento sobre a
ausência de *Rosellinia* no solo.** É proveniência, e a cadeia já confundiu
proveniência com prova uma vez, quando o nome de um ficheiro fez de prova de
que era o B1 — e a G9 da C0-R2 existe precisamente para registar que «*o nome
do ficheiro não estava a fazer de prova*».

**E há um argumento que a própria C5 construiu e não aplicou aqui.** Para
demolir o verbo «excluído» em BIO-16 a C5 escreve: «**um ensaio que não pode
rejeitar não é um ensaio**». Aplique-se a BIO-11, com o campo da linha:

> «Sensibilidade de um composto de solo para organismo de distribuição em
> **manchas** não está declarada em lado nenhum.»

Um composto de solo, n = 1, para um organismo que ocorre em manchas, com
sensibilidade não declarada, **não pode rejeitar** — nem sequer localmente.
O que produziu é uma **não-detecção**, que é uma coisa diferente de uma
exclusão de âmbito reduzido. A C5 aplicou o seu próprio critério a uma linha e
não às quatro onde tinha confessado que não estava a olhar.

**Correcção:** as quatro passam de `EXCLUÍDA-LOCAL` a **`NÃO DETECTADA — n = 1,
composto, sensibilidade não declarada`**, e a tabela §1.1 deixa de ter uma
escada de cinco estatutos com o verbo «excluída» à cabeça de quatro deles. Isto
**não** enfraquece nada que o relatório queira dizer: as quatro já estavam com
`decisao_C5 = PROCURAR`. **O que muda é o verbo que viaja.**

---

## R6 · O transecto não distingue propagação radial de mancha estática, que é a única coisa que o justifica.

A pergunta que me foi posta é a certa, e a resposta é **não**.

**Três defeitos, e são independentes.**

**(a) Não há réplica onde a réplica é necessária, e há onde não é.** O
certificado escreve «12 plantas» e «três pontos por unidade e não seis» como se
as quatro unidades tivessem a mesma estrutura. **Não têm.** No
`c5_amostragem.csv`:

- **T1**: três *posições* — centro, orla, fora — com **uma planta cada**. Não
  são réplicas: são três níveis distintos de um factor, com **n = 1 por nível**.
- **U2, U3, U4**: três *plantas* cada, **todas no mesmo nível**. São réplicas
  puras, sem gradiente nenhum a medir.

**O desenho tem replicação onde não precisa dela e nenhuma onde precisa.** Um
único isolamento falhado, uma única contaminação de placa, uma única planta
atípica num dos três pontos, e o «gradiente» inverte-se ou desaparece. A defesa
da C5 — «passar de 3 para 6 não muda porque a pergunta ainda é *existe
contraste*» — é válida para U3 e U4 e **não é válida para o T1**, onde a
pergunta é *existe gradiente*, e um gradiente sobre três observações singulares
não é uma medida, é um desenho.

**(b) Uma mancha estática produz exactamente o mesmo padrão.** Centro positivo,
orla positiva, fora negativo é o resultado esperado tanto de uma frente em
propagação como de um foco parado desde 2024. **O que distingue os dois é o
tempo, e este desenho tem uma data.** A C5 sabe-o e oferece um discriminante
alternativo — agente primário na orla, colonizadores secundários no centro —
mas esse discriminante é sobre **identidade de espécie**, não sobre gradiente,
e não está declarado como o critério de decisão em §2.4, onde a linha do T1 diz
«**gradiente** centro > orla > fora». **A frase que decide o resultado e a frase
que o poderia sustentar são frases diferentes.**

**(c) O salto de ≥ 20 m não tem limite superior e deixa a transição por
amostrar.** T1c é «≥ 20 m além da orla». Uma orla é uma linha; entre a orla e
os 20 m está toda a informação sobre a **largura da frente**, que é a grandeza
que separa propagação lenta de propagação rápida de mancha parada. Com um ponto
dentro, um na linha e um a distância indefinida para lá, o desenho mede **um
degrau**, não uma frente. E «≥ 20 m» sem tecto significa que duas equipas
diferentes colhem em sítios diferentes.

**As três correcções, e nenhuma custa uma segunda deslocação:**

1. **A segunda radial a ~90° passa de «opcional» a obrigatória.** O próprio
   `c5_02_saida.txt` chama-lhe «o upgrade mais barato que este desenho tem —
   duplica a força do gradiente sem deslocar equipa». **Um upgrade que duplica
   a força da única inferência que justifica a forma do desenho não é
   opcional.** Passa T1 de 3 para 6 pontos e o gradiente de n = 1 para n = 2 por
   nível.
2. **Acrescentar T1b′ a meio caminho entre a orla e T1c** (5–8 m), para haver
   ponto na transição.
3. **Fixar T1c em «20–25 m»**, com tecto.

**Efectivos depois da correcção:** T1 passa de 3 para 8 pontos; total de
17 plantas e 68 amostras em vez de 12 e 48. **É a mesma deslocação, o mesmo
laboratório, a mesma data.**

---

## R7 · O painel foliar não está no ficheiro. Há zero amostras de folha nas 48.

**Um número no ficheiro que o texto contradiz, e é o achado mais operacional
deste documento.**

O §2.3 do certificado lista cinco painéis «**os mesmos em todos os pontos**», e
o quinto é:

> «análise foliar, Ca e macronutrientes | **folha** | ABI-11 / ABI-12»

O `c5_02_amostragem.py` define:

```python
MATRIZES = ["raiz fina", "colo/tronco", "solo 0-30 cm", "solo 40-80 cm"]
```

e gera `12 plantas × 4 matrizes = 48`. **Não há matriz «folha».** Confirmei no
CSV: `grep -c folha c5_amostragem.csv` → **0**. A palavra não ocorre uma única
vez no ficheiro que vai para o terreno.

**Isto não é uma imprecisão de redacção.** A perna foliar de ABI-11 é, por
declaração repetida da própria C5, «**a única vez em toda a cadeia em que um
número deste caso é comparado com um padrão externo**». A medida 3 do §7.1 —
«fazer análise foliar no B3 e no par são, na mesma data» — **é executada por
este CSV e por mais nenhum documento**. As decisões de ABI-11 e ABI-12 no
livro-razão são «PROCURAR o par foliar» e «PROCURAR (simétrico de ABI-11)».
**Uma equipa que execute o `c5_amostragem.csv` tal como está volta do campo sem
uma única folha**, e a única ligação da cadeia a um padrão exterior fica por
fazer numa campanha desenhada, entre outras coisas, para a fazer.

**Correcção:** `MATRIZES` passa a cinco entradas; 12 plantas × 5 = **60
amostras**; com a correcção R6, 17 × 5 = **85**. Custo: uma entrada numa lista
Python e um saco de folhas por planta.

---

## R8 · U2 não tem controlo de proximidade, e é a unidade cujo resultado positivo o certificado diz não saber ler.

O desenho dá ao foco ocidental **dois** controlos: T1c (proximidade — mesma
fila, mesma válvula, metros) e U3 (terreno — 253 m, mesmo bloco). Dá ao foco
oriental **um**: U4, a 474 m, **noutro bloco (B4, não B3)**.

E a margem de U4, escrita pela própria C5, diz o que isso significa:

> «o B4 é um bloco diferente do B3, logo este par controla o **TERRENO**
> oriental e **não a GESTÃO do B3**»

Ora a gestão do B3 é, por declaração da própria camada, **o confundente
dominante daquele lado**: GES-04 NUNCA PROCURADA, 52,4 % do défice do disco
oriental anterior a 2025, 22,6 % e 13,8 % de chão lavrado nas v13/v14 já em
2021, e «**nenhum resultado de 2026 é interpretável**» sem o registo de
operações. **Portanto U2 tem três plantas sintomáticas e nenhum ponto
assintomático que partilhe com elas a gestão que as confunde.**

Leia-se agora o §2.4 na linha de U2: «**mesmo agente que T1** → um problema com
duas expressões». **Essa leitura não é sustentável sem um assintomático do
B3.** Se o agente estiver também no terreno são do B3, não explica o foco
oriental — que é exactamente o raciocínio que a C5 escreve para o lado
ocidental e não escreve para o oriental. **A assimetria é do desenho, não do
terreno.**

**Correcção:** acrescentar **U2c — três plantas assintomáticas em v12 ou v15,
dentro do B3**, escolhidas por défice de 2026 baixo *e* `nu2021` baixo. Custo:
três plantas, uma paragem a duzentos metros das outras.

*(Nota lateral: nenhuma das doze válvulas do `c4_01_numeros.json` serve de par
perfeito no B3 — v12 tem 28,7 % de défice e 12,8 % de chão lavrado, v15 tem
59,3 % e 15,6 %. **Isso é informação, não obstáculo:** significa que o B3 não
tem terreno são, e um controlo imperfeito declarado vale mais do que nenhum.)*

---

## R9 · «O que a medição de paisagem estabelece com força é o negativo» — é ao contrário. O negativo é a parte fraca.

A margem que a C5 acrescentou é **certa e é dela**: a janela contém o pomar,
logo a classe «kiwi» não é controlo externo; fecha a REG-03, não fecha a
REG-01; a faixa poente entra na quarentena da G24. Verifiquei as duas coisas
que ela diz ter verificado e ambas se confirmam pela descrição: as máscaras vêm
de `CUL` (parcelário IFAP) e de `H` (MDS − MDT), **nenhuma do sinal medido**, e
o desenho podia dar positivo e deu, no milho. **Isto é bom trabalho e mantém-se.**

**O que não se sustenta é a hierarquia que a C5 põe por cima.** Ela escreve, e
repete em §0.1, na CONFIRMADO C4, no §6 PODE 9 e no campo da REG-03:

> «O que a medição estabelece **com força** é o **negativo** — a mata não caiu —
> e a ordenação.»

**A ordenação, sim. O negativo, não.** Um negativo é forte quando o desenho
tinha potência para detectar o efeito que interessa. Recuperando o erro-padrão
do p declarado: mata alta, ponto −0,0035 com p = 0,81 → z ≈ 0,24 →
EP ≈ 0,0146 → **IC 95 % aproximadamente [−0,032 ; +0,025]**. Agora as
grandezas contra as quais o negativo é invocado:

| grandeza | valor de dois anos | dentro do IC da mata? |
|---|---|---|
| queda da referência sistemática (G6/G25, −0,00395/ano) | **−0,0079** | **sim** |
| queda em bloco do corpo principal (REG-02, −0,054 / 5 anos) | **−0,0216** | **sim** |

**A medição não consegue distinguir «a mata não caiu» de «a mata caiu
exactamente tanto como o pomar».** Com n = 17-18 cenas autocorrelacionadas —
e a própria C5 escreve que o n efectivo é menor — não podia. A C5 transporta a
cautela «nenhuma das variações é significativa» e depois, três parágrafos
adiante, converte a não-significância no **facto forte** da medição. São a mesma
frase lida nos dois sentidos.

**O que sobrevive, e é bastante:**

1. **A reconciliação B-contra-C aguenta inteira.** A corrida B media coberto de
   ciclo curto, a C media lenhoso perene; a divergência era de definição. O
   milho a −0,0769 demonstra-o dentro do próprio desenho. **REG-03 fecha.**
2. **A ordenação aguenta** — ciclo curto responde ao ano meteorológico, lenhoso
   não — porque a ordenação não precisa de significância em cada linha.
3. **O cenário que invertia o enquadramento — a envolvente a cair o dobro do
   bloco — fica afastado**, porque a leitura que o produzia era a de definição
   errada.

**Retira-se:** «o que a medição estabelece com força é o negativo». **Fica:**
«a medição resolve a divergência B/C por definição, estabelece a ordenação, e
**não tem potência para decidir se a mata caiu tanto como o pomar** — o que
mantém o enquadramento do caso **plausível e por confirmar**, não confirmado».

**E a REG-01 fica com o estatuto certo.** A C5 acertou aqui: `NUNCA PROCURADA
COM O INSTRUMENTO CERTO`, raiz da árvore, PRIORIDADE 1 ABSOLUTA. **Concordo com
a etiqueta, com a posição na árvore e com a consequência declarada** («enquanto
REG-01 estiver por fechar, nenhuma medida irreversível se justifica»). É a
melhor decisão estrutural desta camada e é a resposta certa à pergunta que o
adversário da C4 disse faltar a toda a cadeia.

**Com uma falha, que é a de R10.**

---

## R10 · A REG-01 é a raiz da árvore, custa BAIXO, e não é condição de arranque da campanha. Tinha de ser.

Aqui a C5 evita comprometer-se onde o material já lhe permitia comprometer-se —
que é, pelos termos do meu próprio mandato, uma falha tão grave como
comprometer-se de mais.

Junte-se o que a C5 escreve, em quatro sítios diferentes:

- **§3:** «se a causa for regional, quase todas as medidas de parcela que se
  possam recomendar são inúteis»; «enquanto REG-01 estiver por fechar, **nenhuma
  medida irreversível se justifica**».
- **§5:** REG-01 é a **raiz** da árvore. «Se regional, todos os ramos abaixo
  são discutíveis mas não accionáveis.»
- **`c5_02_saida.txt`:** «As quatro unidades estão dentro da mesma exploração…
  **se a causa for regional, as quatro dão o mesmo resultado e isso NÃO será
  informativo.**»
- **Livro-razão, REG-01:** custo **BAIXO**; «o custo BAIXOU: a medição de
  paisagem demonstra que a consulta ao parcelário é programável e já corre… **é
  a mesma chamada com outra janela**».

**E depois o §2.5 lista quatro condições de arranque, e a REG-01 não é
nenhuma delas.** Uma campanha de laboratório com deslocação de equipa,
48 amostras (60 ou 85 depois das correcções acima), fossas de perfil e um
laboratório contratado é dinheiro gasto — e a camada que o autoriza escreveu,
com todas as letras, que se a resposta à raiz for «regional» aquele dinheiro
não produz informação.

**Não é preciso adiar a campanha. É preciso ordenar.** REG-01 fecha-se com uma
consulta ao parcelário que já está programada e a correr, mais uma segunda
corrida sobre o ENT 297313. **Isso são dias, não épocas**, e o §2.5 já adia a
campanha por três outras condições que também demoram dias.

**Correcção obrigatória:** a **REG-01 passa a condição de arranque n.º 0 do
§2.5** — «localizar dois ou três beneficiários de kiwi da região pelo
parcelário e medir; se todos derem o mesmo degrau de 2024-2026 que Ganfei, a
campanha de 48 amostras não corre nesta forma».

**O mesmo se aplica, com menor força, ao INS-06.** A nota 4 ao adversário
confessa: três linhas sobre ficheiros que já estão em disco, custo NULO, e
mexem em «**todas as grandezas-título** que cito, incluindo as 2,60/3,58 ha que
uso para justificar o foco ocidental como unidade de amostragem». **Um teste de
custo nulo que pode mover a grandeza que justifica a escolha da unidade de
amostragem é condição de arranque, não acompanhamento.** A C5 escreve
«decidi que era melhor entregar o desenho do que os testes, e essa decisão pode
estar errada». **Está errada, e é o único sítio deste certificado onde digo isso
sem margem.**

---

## R11 · A rejeição da F6 e da F5 está certa e não está completa: os ficheiros continuam no pacote de entrega.

**A rejeição substantiva verifica-se e é correcta.** Fui ao
`ganfei_s2\_pacote_cowork\f5_amostragem.py` e ao `f6_arvore_decisao.py` e
confirmei que os factos que a C5 nomeia estão **impressos nas figuras**:

- Painel B da F5: `"MANCHA W", "expansão concêntrica · 15–40 m/ano"` e
  `"ZONA 0", "o foco mais antigo · nove anos"` — **os dois retirados**.
- Um estrato inteiro, `"SATÉLITES 3 · 4 · 5", "testam se o agente salta
  distâncias"`, construído sobre a geometria de avanço radial — **retirada**.

**As cinco regras salvas: verifiquei-as uma a uma contra o livro-razão
re-etiquetado, e as cinco aguentam.** GPS por amostra (nenhuma das 221 tem
coordenada), controlo emparelhado (nenhuma colheita teve assintomático), painel
de raiz (a decisão de gestão está na raiz), uma data um laboratório, 40–80 cm
(ABI-10/ABI-13 NUNCA PROCURADA, zero descrições de perfil no caso). **E a
substituição da sexta — «margem, não centro» por «centro E orla E fora» — é
estritamente melhor, como a C5 diz, porque a regra antiga vedava o T1a que é
onde vive o discriminante primário-contra-secundário.**

**Duas coisas que a C5 não diz, e a segunda é operacional.**

**(a) Duas das cinco regras que sobrevivem tinham factos retirados como razão
declarada.** Está impresso no painel C da F5, e é o que sai na figura:

- «Controlo emparelhado» é justificada por «*M. hapla* saiu positivo em **5 de
  5 blocos, sãos incluídos**» — são **4 unidades com posição**, e **«sãos
  incluídos» não tem suporte nenhum**: o caso não tem um único bloco
  estabelecido como são. A regra é boa; a razão impressa é falsa.
- «Uma data, um laboratório» é justificada por «os dois Becrop são o mesmo
  sector (**válvula 27**, confirmado pelo gestor)» — **a válvula 27 não existe
  em nenhum dos dois livros (R7 da C3)**.
- «40–80 cm» é justificada por «**sete das dez** exclusões abióticas» — número
  que a própria C5 rejeita duas linhas antes.

A C5 escreve que re-justifica as cinco a partir do livro-razão, e re-justifica
mesmo. **Mas não regista que as razões antigas continuam impressas nos
ficheiros que sobrevivem**, e uma regra certa com uma razão falsa impressa ao
lado é como um facto retirado volta.

**(b) A rejeição é de leitura, não de ficheiro.** O §6 NÃO PODE 15 diz que as
figuras «não podem ser apresentadas como estado actual». **Continuam em
`_pacote_cowork\`, que é uma pasta de entrega, com os PNG e os SVG ao lado dos
scripts.** Uma rejeição que deixa o artefacto na pasta de entrega não é uma
rejeição: é uma nota que quem abrir a pasta não vai ler. **Pelo hábito desta
casa** — o `CLAUDE.md` proíbe apagar para resolver duplicados e manda mover
para `_superseded\` com registo — **a acção certa é mover `F5_amostragem.*` e
`F6_arvore_decisao.*` para `_superseded\` e deixar no lugar delas um ficheiro de
uma linha a apontar para o §5 deste certificado.** Não é o adversário que o
faz; fica registado como acção.

---

# PARTE 2 · FACTOS A MANTER, COM MARGEM MAIOR

---

## M1 · Os dois pares sãos passam. Verifiquei, e a verificação é mais forte do que a que a C5 fez.

O ataque pedia que eu confirmasse que o «défice, M2 e chão-lavrado todos a 0 %»
está **calculado e não afirmado**. **Está calculado**: o script lê
`num["por_valvula"]["v6"]["pct_defice_2026"]` e os outros dois campos
directamente do `c4_01_numeros.json`, e imprime-os. Nenhum é transcrito.

**Mas a afirmação a seguir — «são as únicas duas» — é prosa: o script imprime
três válvulas (v6, v17, v16) e não varre as doze.** Varri-as eu:

| válvula | ha | défice 26 | novo M2 | chão 2021 |
|---|---|---|---|---|
| **v6** | 2,33 | **0,0 %** | **0,0 %** | **0,0 %** |
| **v17** | 2,17 | **0,0 %** | **0,0 %** | **0,0 %** |
| v11 | 2,83 | 1,4 % | 1,4 % | 0,0 % |
| v10 | 2,52 | 4,4 % | 0,0 % | 0,0 % |
| v16 | 2,00 | 13,0 % | 0,0 % | 2,5 % |
| v7 · v9 · v12 · v8 · v14 · v13 · v15 | — | 21,2 a 59,3 % | — | — |

**A afirmação está certa: v6 e v17 são mesmo as únicas duas de doze com os três
indicadores a 0,0.** Passa, e passa reforçada.

**E um ponto a favor que a C5 não fez para si própria.** A cautela 2 do §0.1
diz «nada neste plano é uma média de bloco», e à primeira leitura a escolha dos
pares parece violá-la, por ser uma estatística de válvula aplicada a um disco
de 40 m. **Não viola**, e a razão é técnica: `pct_defice_2026 = 0,0 %` não é uma
média, é uma afirmação de **«nenhuma célula»**. Se nenhuma célula das 2,33 ha
está em défice, nenhuma célula do disco interior está. **A estatística
transfere-se para baixo; uma média não transferiria.** A C5 tinha aqui um
argumento forte e não o usou.

**As margens que se mantêm, e uma nova:**

1. **A margem que a C5 declara está certa e não se suaviza.** «0 % em défice» =
   «nunca abaixo da referência menos 0,05», e a referência está a cair (INS-04).
   É «demonstravelmente não pior do que a referência», **não «são»**. E a nota 1
   ao adversário identifica correctamente a direcção do viés: atenua os
   positivos e **não é conservadora para os negativos**, que são metade do que
   este desenho produz. **Isto tem de ir no relatório com estas palavras.**
2. **GES-08 é condição de arranque e está correctamente posta como tal.**
3. **Nova, e é minha: nada verifica que o disco de 40 m está contido no
   polígono da válvula.** O alvo é o **ponto da válvula**, que é uma peça
   hidráulica, e um disco de 40 m à volta dele pode sair para a válvula
   vizinha — a v7, que tem 21,2 % de défice, ou a v16, que tem 13,0 %. A
   garantia de «0 %» só vale **dentro** de v6 e de v17. **Correcção de campo, de
   custo zero: as três plantas de U3 e U4 colhem-se dentro do polígono da
   válvula, e o GPS regista-o.**

---

## M2 · O «13» é 10 lido de um ficheiro mais 3 escritos à mão no código.

A C5 fez o melhor trabalho de proveniência da cadeia sobre este número — apanhou
que o campo do JSON diz **10** e que o texto de cinco documentos diz **13** — e
depois publicou o 13 como CONFIRMADO C3, «exacta», com instrumento independente
«o campo do JSON contra o texto do certificado».

O código:

```python
print("  ... mais as 3 cuja 2.a fonte e Ribadumia (rejeitada) = %d  <- o «13»"
      % (mr["linhas_com_lugar_mas_sem_par_de_comparacao"] + 3))
```

**O `+ 3` é um literal.** Nenhum campo do JSON o produz e nenhum campo nomeia as
três linhas. Reconstruí-as e **fecham**: os quatro negativos com lugar são
*Armillaria* (Raiz), *Armillaria* (Solo), *Rosellinia* (Solo) e Oomicetas
(Solo); o primeiro já está nas dez linhas «só granel», os outros três não; 10 + 3
= 13. **O número está certo. A sua derivação não está no ficheiro.**

E daqui sai uma imprecisão que se corrige numa palavra. O certificado escreve:

> «**As três somadas são precisamente as que carregam os resultados
> NEGATIVOS**»

São **três das quatro**. O quarto negativo — *Armillaria* (Raiz) — já estava nas
dez. Numa camada cuja peça central é ter apanhado um «13» que atravessou cinco
documentos com o valor errado, «precisamente» é a palavra a evitar.

**Mantém-se, com margem: «13 = 10 (campo `linhas_com_lugar_mas_sem_par_de_
comparacao`) + 3 identificadas por reconstrução manual, três das quatro linhas
que carregam negativos com lugar».**

---

## M3 · `SUSTENTADA-LOCAL` passa, e nenhuma linha subiu por causa dela. Mas a categoria parou uma linha antes do fim.

O ataque pedia que eu verificasse se alguma linha subiu de estatuto pela criação
da categoria. **Verifiquei as quatro. Nenhuma subiu; as quatro desceram.**

| linha | C4 | C5 | movimento |
|---|---|---|---|
| ABI-03 | SUSTENTADA | SUSTENTADA-LOCAL | desce **e é reescrita** |
| ABI-11 | SUSTENTADA | SUSTENTADA-LOCAL | desce (só a perna foliar) |
| REG-02 | SUSTENTADA | SUSTENTADA-LOCAL | desce |
| INS-04 | SUSTENTADA | SUSTENTADA-LOCAL | desce |

**ABI-03 merece uma verificação a mais, e sobrevive.** A linha não foi só
requalificada: foi **substituída** — sai «água concentrada no foco OESTE»
(que assentava num contraste de 2 cm), entra «o foco ESTE está mais alto sobre
a drenagem». Uma proposição nova a herdar o prefixo «SUSTENTADA» do ID de uma
proposição retirada é a forma exacta como um juízo se converte em facto. **Neste
caso não é**: o M8 do adversário da C4 autoriza-o explicitamente — «*ABI-03
mantém-se SUSTENTADA se for reescrita como…*» — e o contraste novo, 0,353
contra 0,130/0,150, é de mais de 2× e sobrevive a qualquer margem razoável. **A
C5 foi mais longe do que o mandato — o mandato pedia ABI-11 e REG-02 — e foi na
direcção certa.**

**Onde parou cedo de mais: o INS-03.** É agora a **única** linha de todo o
livro com `SUSTENTADA` sem qualificador. Aplique-se-lhe o critério que a própria
C5 usou para despromover REG-02 e INS-04 — «o próprio campo declara não ter
instrumento independente»:

- O instrumento declarado é «máscara de estrutura (ortofoto) contra série de
  reflectância; mais **média contra mediana** como segunda via». A primeira
  metade é boa. **A segunda não é uma segunda via independente:** média e
  mediana são dois estimadores da **mesma amostra de reflectâncias da mesma
  cena**. Concordarem é aritmética, não confirmação.
- A margem da própria linha: «**não há bootstrap e a cena de 2026 é a S2C;
  parte do +0,0133 pode ser re-ordenação da mediana e nada nesta cadeia separa
  as duas coisas**».

**Passa a SUSTENTADA-LOCAL**, e o livro-razão re-etiquetado fica com **zero
linhas sustentadas sem qualificador de âmbito** — que é, exactamente, o retrato
honesto de um caso onde a etiologia não está estabelecida.

*(O sentido de INS-03 é conservador — limpar a referência torna o acontecimento
maior — e por isso a despromoção não enfraquece nada do que a C5 quer dizer.)*

---

## M4 · «A decisão não fecha» é honestidade. Uma das sete não-distinções fecha hoje, de graça.

Ataquei o §8 pelos dois lados, como o mandato pede. **Seis das sete
não-distinções são reais e nenhuma delas é evasão:** local/regional; doença
contra gestão a nascente; degrau contra declínio a acelerar; qual dos organismos;
identidade vazio-contra-núcleo; cauda do sensor. **As seis medidas do §7.1
comprometem-se onde o material permite** — e a sexta, **não replantar no vazio
antes de o transecto voltar**, é a mais difícil de escrever das seis, porque é a
única que **custa** alguma coisa a quem a recebe (uma época) e a única que
manda **não** fazer. Uma camada evasiva não escreve essa. **Passa inteira.**

**Uma excepção, e fecha com uma chamada telefónica.** A não-distinção n.º 3 —
«replantação contra chão limpo mantido, no N3» — está listada como aberta, e as
linhas GES-01/GES-02 do livro-razão dizem, as duas, `PROCURAR por VISITA`,
custo **NULO**. É a mesma chamada onde já vão as duas perguntas de campo da
condição de arranque n.º 4. **Uma pergunta de custo nulo que fecha uma
não-distinção não pertence à lista das que não fecham: pertence à lista das
acções.** Movê-la para o §4, como acção 5.

*(E note-se o que a C5 já estabeleceu sobre o N3 e não usou aqui: o piso de
Inverno **desce** de 0,654 para 0,497 e o pico de Verão afasta-se da
referência. «Uma videira jovem a pegar FECHA sobre a referência no Verão; esta
AFASTA-SE.» O material já favorece GES-02 sobre GES-01. Está no CSV como
`FAVORECIDA SEM CONFIRMAÇÃO` — e essa é a etiqueta certa.)*

---

## M5 · A observação de campo é o melhor facto do dossiê e ainda não é um facto sobre o vazio.

A C5 trata a observação de campo com o cuidado certo: não lhe atribui área,
raio nem centro; recusa a ligação ao núcleo n.º 22; recusa que a forma
circular promova ou exclua qualquer agente; e regista a margem que ninguém lhe
pediu — se ao gestor foram alguma vez mostrados os nossos mapas de NDVI.
**Nada disto se corrige.**

**Duas margens a acrescentar, e a segunda pesa.**

1. **O teste de identidade de objecto, que a C5 chama «o melhor que este desenho
   tem», é assimétrico.** Se os GPS caírem dentro do polígono do núcleo n.º 22,
   é convergência forte. **Se caírem fora, não é falsificação**: o núcleo é de
   2026 e delimitado por anomalia de NDVI/NDMI, o vazio é do terreno e sem data
   declarada, e há **30 m de dispersão de centro entre derivações
   independentes** do próprio núcleo. Um teste cujo resultado negativo não é
   interpretável é meio teste. **Continua a valer duas leituras de GPS e a
   custar zero — mas o que se escreve antes de o correr é «se coincidir,
   confirma; se não coincidir, não decide».**
2. **O testemunho é de tipo 1 sobre a EXISTÊNCIA e a FORMA do vazio, e é de
   tipo 1 muito mais fraco sobre a colocação do «Kiwi 1000» nele.** O gestor viu
   o vazio no terreno: isso é directo. Que a amostra do informe 331/2025 tenha
   sido colhida **no lado oeste desse vazio** é memória sobre uma colheita de
   **2025-06-06**, referida catorze meses depois, e o modo de falha do tipo 1 é,
   pela tipologia do próprio `CLAUDE.md`, «memória, ambiguidade de referência,
   ou mudança desde a data a que a pessoa se refere» — os três activos aqui.
   **A C5 protege-se disto ao dizer «zona, não ponto», e não diz que a colocação
   é um tipo 1 de segunda ordem.** A acção 1 do §4 já pergunta «onde estava a
   planta arrancada em relação ao vazio»; **acrescente-se, na mesma chamada:
   «e a amostra de 2025 — lembra-se de a ter colhido dentro do vazio, na orla,
   ou fora?»**

---

# PARTE 3 · A PERGUNTA QUE FALTA

O adversário da C4 escolheu «**qual é o nível normal disto?**» e a C5
transportou-a, correctamente, para NÃO TESTÁVEL 13. Mantém-se aberta e é a
maior. **Mas não é a pergunta que falta a esta camada**, porque esta camada
fê-la.

A que falta a esta camada é outra, e é a única que a última camada podia fazer:

> ## Quanto é que esta cadeia custou, e o que é que se comprou com ela?

Seis camadas, sete listas fechadas, cinco adversários, uma revisão R2, duas
adendas, duas rondas de multiverso, dois dias. O que a cadeia produziu, medido
pelo que passa para o relatório: **duas exclusões genuínas em 56 causas
candidatas efectivas**, uma matriz de diagnóstico com uma coluna, e uma lista de
tudo o que não se pode dizer.

**Isto não é uma crítica à cadeia. É a pergunta que decide se ela se repete.**
Porque a resposta, lida com atenção, é dura para o método e favorável ao
protocolo ao mesmo tempo:

- **Nenhum dos factos que sobrevivem foi produzido por análise de imagem.** O
  que sobrevive vem do LiDAR, do SAR, do parcelário, dos boletins de solo, da
  ortofoto usada como **estrutura** e não como radiometria, do testemunho da
  gestora, e — na última hora e por uma pergunta directa — de **uma observação
  de campo**. O `CONTROLOS.md` previu-o na primeira página: «*a informação nova
  veio de fora do cálculo*». **Dois dias de cadeia confirmaram-no e não o
  contrariaram uma única vez.**
- **A cadeia não descobriu a etiologia; descobriu que o material nunca poderia
  tê-la revelado.** Vinte linhas organismo × matriz, treze delas dependentes de
  uma amostra composta, num sítio, num dia, sem par. **Nenhuma quantidade de
  análise sobre esse material produzia um diagnóstico**, e as quatro camadas
  que correram antes da C4 estiveram a refinar a medição de um sinal cuja causa
  o material não continha.
- **O que a cadeia comprou foi a lista do que não se pode afirmar.** As quinze
  linhas do §6 NÃO PODE. Cada uma delas é uma frase que teria entrado num
  relatório com assinatura institucional. **Isso vale os dois dias, e o número
  que o mede não é «quantas causas excluímos» — é «quantas afirmações falsas
  não foram publicadas».**

**Corolário para quem decidir o que fazer a seguir.** Se este processo se
repetir noutro caso, a ordem certa não é a ordem que se seguiu. **A pergunta
«que material existe, e que perguntas é que ele pode responder?» — que foi a C4
a fazer, em quinto lugar — devia ter sido a primeira**, antes da geometria.
Vinte linhas com uma coluna são conhecíveis em duas horas de leitura de um
livro de laboratório, e conhecê-las teria mudado a C0.

---

# PARTE 4 · A TRANSVERSAL DA CADEIA — quantos factos chegam ao topo com instrumento independente

Esta é a medida final do trabalho, e é a que só a última camada pode fazer.

**Regra de contagem, declarada antes de contar.** Percorri as sete listas
fechadas — C0-R2, C1, C2, adenda de LiDAR, C3-R2, C4, C5 — e classifiquei cada
facto operativo em três classes, na acepção do Controlo 1:

- **A · com instrumento independente** — confirmado por um instrumento de
  **outra natureza** (LiDAR contra óptico, SAR contra óptico, ortofoto como
  estrutura contra reflectância, documento, testemunho, laboratório, um segundo
  sensor). Quatro corridas do mesmo instrumento **não contam**.
- **B · afirmação negativa ou de cobertura** — «não existe X», «nunca se
  procurou Y». Passa por convenção, porque **nenhum instrumento pode confirmar
  uma ausência de ensaio**, e as próprias camadas o declaram.
- **C · só o instrumento que o produziu** — inclui os que declaram «nenhum», os
  que pedem emprestado o instrumento de outra linha, e os já retirados cuja
  retirada não viajou.

| lista | factos | A · independente | B · negativo | C · só o próprio instrumento |
|---|---|---|---|---|
| **C0-R2** | 28 | **11** | 6 | 11 |
| **C1** | 20 | **13** | 3 | 4 |
| **C2** | 11 | **3** | 1 | 7 *(4 dos quais retirados ou proibidos pela própria C5)* |
| **adenda LiDAR** | 8 | **4** | 0 | 4 *(2 retirados, 2 parcialmente)* |
| **C3-R2** | 11 | **3** | 5 | 3 |
| **C4** | 8 | **4** | 3 | 1 *(D4, instrumento emprestado)* |
| **C5** | 6 | **0** | 2 | 4 |
| **TOTAL** | **92** | **38** | **20** | **34** |

**Trinta e oito de noventa e dois — 41 % — têm hoje um instrumento
independente a sério.** Vinte são negativos que não podem ter um. **Trinta e
quatro chegam ao topo sustentados só pelo instrumento que os produziu**, por um
instrumento emprestado a outra linha, ou já retirados sem que a retirada tenha
acompanhado o facto.

**Três leituras desta tabela, e a terceira é a que interessa.**

**1 · Os factos com instrumento independente estão quase todos nas duas camadas
de baixo.** Vinte e quatro dos trinta e oito estão em C0 e C1 — as camadas que
respondem a **onde fica** e **o que é o terreno**. Faz sentido: são as perguntas
para as quais existem instrumentos alternativos baratos (uma ortofoto, um MDT,
um cadastro, uma pergunta ao gestor). **A cadeia foi desenhada para pôr a
fundação primeiro, e a fundação é de facto a parte sólida.**

**2 · A independência colapsa exactamente onde o caso vive.** A C2 mede o
fenómeno e tem **três** factos independentes em onze, dos quais um (V3) tem uma
permutação por correr há quatro camadas. A C3 tem **três** em onze, e cinco dos
restantes declaram «nenhum» — e passam porque são negativos sobre cobertura de
ensaio, que é a única coisa que aquele material podia sustentar. **A C4 é a
melhor das três**, com quatro em oito, e mesmo assim a sua linha mais citada,
D4, **empresta a instrumento de outra linha**. Ou seja: **quanto mais perto se
chega do fenómeno, mais fina fica a independência**, e é precisamente aí que a
inferência se apoia.

**3 · A C5 contribui zero, e isso não é um lapso — é o que a camada é.** A C5
não mede: julga. Os seus seis pontos são um juízo sobre 59 linhas (P1), um
desenho (P2), uma lista de pedidos (P3), uma pergunta em aberto (P4), uma
propriedade herdada (P5) e seis decisões (P6). **A única linha que reclama
instrumento independente é a P1, e a reclamação não sobrevive ao código
(R1).** A camada de decisão é, por construção, a camada onde não há instrumento
— o que torna a nota 3 ao adversário («fiz 59 juízos sozinho, e são o produto
principal desta camada») a frase mais importante do certificado.

**E a medida final, que é uma frase.** Esta cadeia inteira existe por causa de
um facto — «o lóbulo oeste é o B1» — que não tinha instrumento independente, e
que teria caído no primeiro dia se alguém tivesse aberto a imagem RGB. **Dois
dias depois, o caso tem um número maior de factos com instrumento independente
do que tinha, tem trinta e quatro que continuam sem, e tem — desde ontem — a
sua primeira observação de terreno.** O item que mais mudou o dossiê nas
últimas vinte e quatro horas não foi nenhuma das sete listas fechadas: foi uma
pergunta feita a uma pessoa que esteve lá. **Se este documento tiver de deixar
uma linha para o próximo caso, é essa.**

---

# PARTE 5 · OS CINCO TESTES DE CINCO MINUTOS

Ordenados por valor. **Os cinco correm sobre ficheiros que já estão em disco ou
sobre uma chamada telefónica. Nenhum precisa de campanha.**

**T1 · Certificar a série Landsat.** `_VALIDADE_GESTAO\landsat.json` **existe** —
verifiquei — e é uma série por unidade desde **2013**, com `referencia`,
`resto do pomar`, `OESTE com pergola`, `ESTE com pergola`, `ESTE sem pergola`,
em NDVI e NDMI. **É outra agência, outro sensor, outra cadeia de correcção, e é
o único instrumento verdadeiramente externo do caso.**
*O que fecha, tudo de uma vez:* a **dimensão** de D4 e de P5 (hoje só direcção);
o estatuto de INS-04 e de REG-02 (hoje SUSTENTADA-LOCAL por falta exactamente
deste ficheiro); **e o INS-01**, porque é o único modo de desconfundir sensor de
ano. Fecha **quatro linhas do livro-razão com um ficheiro**.
*Porque não correu ainda:* está declarado por **cinco camadas consecutivas** e
executado por nenhuma. **Este é o teste que este documento existe para pedir.**

**T2 · INS-06 — o desvio-padrão e a assimetria fora do pomar, nas duas cenas
S2C.** Três linhas. Custo nulo.
*O que decide:* se a cauda inferior alargou com o sensor, **movem-se ao mesmo
tempo** a área em défice, a dispersão, a fracção, o M2, e as 2,60/3,58 ha que
justificam a escolha do foco ocidental como unidade de amostragem. **É condição
de arranque da campanha, não acompanhamento** (R10).

**T3 · A REG-01 pelo parcelário: dois ou três beneficiários de kiwi da região,
mais o ENT 297313 numa segunda corrida.** A consulta já corre — `paisagem.py`,
camada `culturas.2025jun10`, com resposta a uma caixa arbitrária. **É a mesma
chamada com outra janela.**
*O que decide:* a raiz da árvore, e se a campanha de 48 amostras deve sequer
correr na forma actual. **Custo BAIXO por declaração da própria C5.**

**T4 · A chamada única ao gestor, com seis perguntas.** Nenhuma é análise:
(1) registo de operações do B2 e do B3, 2024-2026, com data e sector, mais o
histórico de aplicações; (2) data de plantação por talhão (GES-08); (3) «vê do
lado nascente um vazio comparável ao do poente?»; (4) «onde estava a planta
arrancada de 2026-08-04 em relação ao vazio?»; (5) «a amostra de 2025 — dentro
do vazio, na orla, ou fora?» (M5); (6) «alguma vez lhe mostrámos os nossos
mapas de NDVI?».
*O que fecha:* GES-03, GES-04, ABI-05, ABI-14 (metade), GES-08, o âmbito de
GES-01/02, a interpretabilidade de **todo** o resultado de 2026, e a margem
sobre a independência do testemunho. **Sete linhas do livro-razão numa chamada.**
*A pergunta (3) sozinha pode poupar uma unidade inteira da campanha:* se não
houver vazio a nascente, os dois focos são fenómenos diferentes e sabe-se por
uma pergunta em vez de por doze plantas.

**T5 · O envelope da *Rosellinia*.** A amostra de raiz de 2026-08-04 está
colhida e nunca foi enviada. É a única identificação de campo de um organismo
em todo o caso, e a linha RAIZ não existe na matriz — o único negativo que se
lhe pode opor é de **solo** e de catorze meses **antes**.
*O que decide:* se a única identificação de campo do caso se confirma ou cai.
**Custo: um envelope.** É a linha mais barata de fechar de toda a cadeia e tem
um pedido por cumprir.

*(Os testes T4 e T5 já estão no §4 do certificado. Repito-os aqui porque um
pedido feito duas vezes e não cumprido é um dado sobre o processo, e a terceira
vez tem de ir com o nome de quem responde e uma data.)*

---

# PARTE 6 · VEREDICTO

## O que passa

- **A emenda à regra 1 foi cumprida, e cumprida a sério.** As dez alterações
  obrigatórias estão aplicadas e marcadas; a parametrização retirada não
  sobreviveu ao transporte. **É a primeira vez na cadeia que uma correcção
  viaja para cima em vez de ser reencontrada.**
- **Os dois pares sãos.** Verificado contra as doze válvulas: v6 e v17 são
  mesmo as únicas duas com os três indicadores a 0,0, e o «0 %» está calculado
  do ficheiro, não afirmado.
- **O desenho pode dar negativo, e os negativos estão escritos antes dos
  resultados.** U3/U4 positivos **retiram** candidatos; T1 negativo derruba D7 e
  a leitura das nove presenças. **É desenho, não é confirmação.** Este critério
  passa limpo.
- **A rejeição da F6 e do desenho F5** — correcta nos motivos, e as cinco regras
  salvas aguentam contra o livro-razão re-etiquetado, verificadas uma a uma.
- **`SUSTENTADA-LOCAL`** — corrige uma assimetria real e **nenhuma linha subiu
  de estatuto por ela**. As quatro desceram.
- **«A decisão não fecha»** — é honestidade, não evasão. As seis medidas do
  §7.1 comprometem-se onde o material permite, incluindo a única que manda
  **não** fazer.
- **A nota ao adversário à cabeça, com os seis pontos que a camada não sabe
  resolver.** Cinco dos seis estavam certos e este documento confirma-os. **É a
  melhor prática da cadeia e deve ficar no protocolo.**

## O que se corrige

1. **CONFIRMADO C1** — o instrumento independente declarado **não existe no
   código**. Passa a «juízo de uma sessão, sem instrumento». *(R1)*
2. **«24 mal rotuladas, 11 encontradas»** → **«18 mal rotuladas, 6 re-descritas;
   10 encontradas e 1 por confirmar»**. *(R2)*
3. **«Três exclusões»** → **duas (ABI-01, ABI-02)**; INS-01 passa a
   **EXCLUÍDA-CONDICIONAL** à certificação do Landsat. *(R3)*
4. **ABI-04** — retira-se `JÁ FECHADA`; passa a `PROCURAR`, custo nulo. As «5
   já fechadas» passam a 4. *(R4)*
5. **As quatro EXCLUÍDA-LOCAL** → **NÃO DETECTADA (n = 1, composto,
   sensibilidade não declarada)**. *(R5)*
6. **ABI-02** — criar a linha `ABI-02b` para a perna do TWI, que a própria C5
   classifica NUNCA PROCURADA e deixou no texto livre. *(R3, nota)*
7. **INS-03** → **SUSTENTADA-LOCAL**; o livro fica com zero sustentadas sem
   qualificador. *(M3)*
8. **O «13»** — declarar que são 10 do ficheiro mais 3 reconstruídas à mão, e
   trocar «precisamente as que carregam os negativos» por «três das quatro».
   *(M2)*
9. **§0.1 / CONFIRMADO C4 / §6 PODE 9** — retirar «o que a medição estabelece
   com força é o negativo». Fica a reconciliação de definição, a ordenação, e
   a declaração de que **o desenho não tem potência** para distinguir «a mata
   não caiu» de «a mata caiu tanto como o pomar». *(R9)*
10. **Transportar para o `c5_reetiquetagem.csv` as cinco colunas de evidência da
    C4** que o de saída deitou fora. *(R1c)*
11. **GES-01/GES-02** saem do §8 e entram no §4 como acção 5, por serem de custo
    nulo. *(M4)*
12. **`F5_amostragem.*` e `F6_arvore_decisao.*`** movem-se para `_superseded\`
    com registo, em vez de ficarem no pacote de entrega com uma nota de
    rejeição noutro documento. *(R11b)*
13. **A coordenada retirada sai das doze linhas do `c5_amostragem.csv`**, mesmo
    negada. *(§0)*

## O que se retira

- **O instrumento independente de CONFIRMADO C1.**
- **«Três excluídas com instrumento independente»** — são duas.
- **`JÁ FECHADA` de ABI-04.**
- **O verbo «excluída» das quatro EXCLUÍDA-LOCAL.**
- **«O que a medição de paisagem estabelece com força é o negativo.»**
- **«As três somadas são precisamente as que carregam os negativos.»**
- **A leitura de que o transecto, tal como está, distingue propagação de mancha
  estática.**

**Nada disto derruba a peça central.** As quatro correcções numéricas — 24→18,
11→10+1, 3→2, 5→4 fechadas — vão **todas no mesmo sentido em que a C5 já
apontava**: o caso está pior do que o livro-razão da C4 dizia. A C5 acertou na
direcção em todas e errou na dose em duas, uma para cada lado.

## O desenho de amostragem pode ser executado como está?

# NÃO.

Não por ser mau — é o melhor artefacto desta cadeia e é a primeira coisa em
todo o processo que pode produzir um dado que derrube uma hipótese. **Mas tem
três defeitos que o fariam voltar do campo sem responder ao que foi desenhado
para responder, e um problema de sequência que pode fazer com que não devesse
correr de todo.**

**Os três defeitos, e as reparações:**

| # | defeito | reparação | custo |
|---|---|---|---|
| 1 | **Zero amostras de folha nas 48**, contra um painel foliar declarado em todos os pontos e a medida 3 do §7.1. A única ligação da cadeia a um padrão externo fica por fazer. | `MATRIZES` passa a cinco entradas | uma linha de código, um saco por planta |
| 2 | **O transecto tem n = 1 por nível**, salto de ≥ 20 m sem tecto e nenhum ponto na transição. Não distingue propagação de mancha estática. | segunda radial a 90° **obrigatória**; ponto T1b′ a 5–8 m; T1c fixado em 20–25 m | mesma deslocação, mesma data |
| 3 | **U2 não tem controlo de proximidade no B3**, que é o bloco confundido com gestão — e é a leitura «mesmo agente que T1» que fica inutilizável. | acrescentar **U2c**, três assintomáticas em v12 ou v15 | três plantas, uma paragem |

**Efectivos depois das três reparações: 20 plantas · 100 amostras · uma data ·
um laboratório**, contra 12 e 48. **A campanha continua a ser uma deslocação.**

**E o problema de sequência, que é anterior a tudo isto.** A C5 escreveu que se
a causa for regional as quatro unidades dão o mesmo resultado e **isso não será
informativo**, e pôs a REG-01 na raiz da árvore com prioridade absoluta e custo
BAIXO — e depois não a pôs entre as condições de arranque. **A campanha não
arranca antes de:**

- **REG-01** medida pelo parcelário (T3 desta lista) — **condição nova, n.º 0**;
- **INS-06** corrido (T2) — três linhas sobre ficheiros em disco;
- **GES-08**, o **registo de operações do B2 e do B3**, e o **T3 de pérgola**,
  que são as condições que a C5 já lista e que **estão por cumprir** — confirmei
  que `c2_12_prom_2025.npy` **não existe em lado nenhum**, tal como a C5 diz;
- **as seis perguntas de campo** (T4 desta lista), das quais **uma pode poupar
  uma unidade inteira**.

**Nenhuma destas condições demora mais do que dias, e todas são mais baratas do
que a campanha.** A frase que a C5 escreveu sobre a C3 aplica-se agora a ela
própria e é a forma certa de a encerrar: *as condições de arranque verificam-se
antes de se dar a campanha por iniciada.* **O §2.5 tem o título de uma
verificação e o corpo de uma lista.** Verifique-se — e depois execute-se, que o
desenho merece.

---

*Fim do adversário da C5. Não há camada acima, e não há adversário depois deste.*
