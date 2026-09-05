# CLÁUSULAS — para os padrões pararem de se repetir

**O que este documento é.** A `ANTES_DE_COMECAR.md` diz como trabalhar. As
`HIPOTESES_FECHADAS.md` dizem o que já se tentou. Isto diz **porque é que os
mesmos erros voltaram**, e o que os impede — não por boa vontade, mas por
máquina.

**O que o obrigou.** Vinte e três veredictos retirados. Sete encarnações do
mesmo defeito no mesmo ficheiro. E, num único turno de 04-09-2026, a repetição
de dois estudos que já estavam em disco. Nenhuma destas coisas foi apanhada por
recomputação; todas por ir a um instrumento diferente, ou por o gestor dizer.

---

## 1 · O invariante

Passei as vinte e três retiradas em revista, uma a uma. **Todas partilham uma
única propriedade:**

> **Alguma coisa que devia ser independente não era.**

O controlo, o nulo, a janela, o instrumento, o leitor, ou a memória. Não são
vinte e três erros — é um erro com vinte e três formas. As oito abaixo são
essas formas, cada uma com as retiradas que a instanciam.

| | forma | instâncias no registo |
|---|---|---|
| **A** | **o controlo partilha dados com o que controla** | placebo do chão a 91 % do sinal (5); nulo ingénuo contra autocorrelação 0,86-0,96 (12); o lóbulo como «melhor controlo» (15); 55,9 % dos píxeis do ICP eram as próprias válvulas (04-09); `por_area` validada contra as áreas que a calibraram |
| **B** | **um teste que não podia falhar** | o T5 como identidade algébrica (17); as sete encarnações no `guarda.py`; `c2 = True`; a verificação 7 cega à P10; RMS < 30 com P(passar) = 0,21 |
| **C** | **a janela decide em silêncio** | a AOI que media Valença urbana (9); o rio a entrar por uma janela mal recortada (6); o mosaico da C1 recortado a 300 m, que deixava o B1 fora; a abertura morfológica aplicada depois da intersecção (4) |
| **D** | **forma do modelo errada** | deriva tratada como aditiva sendo 7× multiplicativa (8); declive lido como crónico quando o degrau ajusta 4 : 1 melhor (13) |
| **E** | **o cabeçalho e o código divergem** | `fazer_masks_v2` («polígonos estáticos» sobre `nd2026 > 0,78`); os «34 m» do `m1_v8` que não reconciliam; o `georref_manual` a declarar 1,7 m/px; o bug do leitor das válvulas 1-5 (21) |
| **F** | **um insumo morto continua a alimentar a jusante** | o núcleo «p < 0,0005» a imprimir três dias depois de a AOI morrer (10); o D8 assente num número rejeitado nove horas antes (20); os ficheiros retirados que continuavam a correr (04-09) |
| **G** | **erro de leitura tomado por sinal** | a ponta oriental lida 600 px ao lado (04-09); a designação dos focos invertida por quatro auditorias (1); NDRE comparado com NDVI e chamado convergência (3); a mudança de cobertura da ortofoto lida como periodicidade (7) |
| **H** | **repetir o que já está em disco** | o B1; o esquema de rega; a rede de rega — os três em 04-09, e os três já analisados |

A **B** e a **H** são as que mais custaram, e são as duas que a máquina não
vigiava.

---

## 2 · O que a literatura já resolveu, e que faltava aqui

O projecto cita o multiverso analítico — Silberzahn, Breznau, Botvinik-Nezer,
Kummerfeld & Jones, Bertran. Essa literatura descreve **a dispersão**. O que
faltava era a literatura sobre **como fechar cada forma de dependência**.

**Severidade** — Mayo & Spanos. Uma afirmação só está testada na medida em que
passou um teste que **provavelmente teria encontrado a falha, se ela existisse**.
O poder não é um extra do teste: é o que faz dele um teste. Fecha a forma **B**.

**Controlos negativos** — Lipsitch, Tchetgen Tchetgen & Cohen. Um controlo
negativo é um par exposição-desfecho onde se **sabe** que não há efeito, sujeito
às mesmas fontes de viés. Se o método «encontra» efeito ali, o método está
partido. Fecha **A** e dá o instrumento para **B**.

**Fuga de dados** — Kapoor & Narayanan. Taxonomia de oito tipos de fuga,
297 artigos afectados em 17 campos. O remédio deles é a **model info sheet**:
uma ficha fixa que declara, por análise, o que o conjunto de teste partilha com
o de treino. Fecha **A**, e é a forma exacta do defeito de 04-09.

**Curva de especificação** — Simonsohn, Simmons & Nelson. Quando há várias
análises simultaneamente defensáveis, arbitrárias e motivadas, reporta-se a
**distribuição sobre todas**, não a escolhida. Fecha **D**, e fecha a variante
de **B** em que o critério é escolhido depois de se ver o resultado.

**Equipas vermelhas** — Coles, Arslan, Tiokhin & Lakens. O adversário entra
**no início** e critica cada passo, não no fim. Aqui o Controlo 3 já existe,
mas chegava sempre **depois de publicar**.

---

## 3 · As cláusulas

Cada uma diz o que exige, o que a força, e se está **executável** ou ainda em
prosa. Uma cláusula em prosa cumpre-se quando dá jeito — está escrito na
`CLAUDE.md` e foi provado sete vezes.

### C1 · Severidade declarada · **executável**
Nenhum critério conta sem a probabilidade de falhar sob uma perturbação do
tamanho que interessa, **calculada antes de se olhar para o resultado**. Um
limiar que quase nunca passa não é um teste, é um carimbo de recusa; um que
quase sempre passa não é nada.
*Aplicado no `georref_v5.py`: a condição C mede o poder por Monte Carlo (±3°,
±80 m) e reprova o próprio critério se ele passar em mais de 20 % das
perturbações.*

### C2 · Cada condição bloqueia sozinha · **executável**
Toda a condição do portão tem de ser a **única razão** de bloqueio em pelo menos
um caso de auto-teste. Se nunca bloqueia sozinha, ficar inerte é indetectável.
*Medido a 04-09: **0 de 9** condições isolavam, e duas nem sequer disparavam.
Corrigido — o `guarda.py` tem agora nove casos de isolamento, e o `certificar.py`
falha se algum deixar de isolar.* **É esta a cláusula que explica as sete
encarnações**: não foram sete descuidos, foi uma bateria sem poder para os
apanhar.

### C3 · Ficha de fuga · **prosa, por executar**
Antes de correr, cada análise declara o que o **controlo** partilha com o
**ajuste**: dados, máscara, janela, instrumento, analista. Se partilhar
qualquer um, não é controlo — é parte do ajuste.
*O defeito de 04-09 tinha esta forma exacta: a fonte que o ICP alinhava continha
os círculos das válvulas, e as válvulas eram o controlo. A frase «nenhuma
válvula entra no ajuste» estava escrita no ficheiro e era falsa.*

### C4 · A janela declara-se, mede-se, e diz o que exclui · **prosa**
Qualquer AOI, máscara ou recorte publica a sua extensão e **o que fica de fora**,
e responde: *o que estou a afirmar cabe dentro desta janela?* Quatro retiradas
vieram de uma janela a decidir em silêncio.

### C5 · Distribuição, não a corrida preferida · **prosa**
Onde houver variantes defensáveis do critério ou do modelo, reporta-se a
distribuição sobre todas. *O Controlo 3 mostrou que **seis de oito** formulações
defensáveis do critério de georreferenciação publicariam, e que a variante que
eu ofereci logo a seguir ao falhanço — «todas a ≤ 26 m» — era precisamente uma
das que passam.*

### C6 · O cabeçalho é executável ou não é cabeçalho · **prosa**
Um número afirmado num docstring aparece na saída do próprio ficheiro, ou vai
marcado como não calculado ali. *Repeti os «34 m» do `m1_v8` sem verificar o
código, e não reconciliam: a mesma reconstrução põe a válvula 8 a 506 m da
máscara. É a armadilha do `fazer_masks_v2` — ler o cabeçalho e o código juntos.*

### C7 · Retirado significa inerte · **executável**
Um ficheiro retirado **recusa-se a correr**: imprime o cartucho e sai. *Até
04-09, o `escala_do_desenho.py` estava retirado, corria na mesma, imprimia a
conclusão falsa e **reescrevia o seu próprio `.json` com ela**. O cartucho
protegia quem lê e não quem executa.* O cartucho é reconhecido em `.md` **e** em
`.py`, e a verificação 8 do certificador bloqueia se um facto se apoiar num
ficheiro morto.

### C8 · O negativo indexa-se, e vem no arranque · **executável**
As hipóteses testadas e fechadas vivem em `HIPOTESES_FECHADAS.md`, injectado no
arranque de cada sessão pelo gancho `SessionStart`, ao lado da pré-voo.
*A triagem é **cega ao negativo por construção**: classifica como corrente o que
sustenta um facto certificado, e uma hipótese refutada não sustenta facto
nenhum. O `rede_de_rega.py` — onze cenas, critério pré-registado, refutado duas
vezes — está em `NAO_ALCANCADO`. Foi assim que o repeti.*

### C9 · O adversário vê o critério antes da corrida · **prosa**
O Controlo 3 existe e funciona — apanhou o D8, o C8, o C9, a triagem, e a
georreferenciação. Mas chega sempre **depois de publicar**, e por isso o custo é
sempre uma retirada. A cláusula é a da literatura das equipas vermelhas: o
adversário lê o critério **antes**.

### S1 · Procurar é um comando, e vem antes de criar · **executável**
`python ja_existe.py <termos>` varre as quatro árvores — os 1 282 ficheiros,
não só os correntes — e devolve cada acerto **com o seu estado**: a classe da
triagem, se pré-registou uma falsificação, e se já consta das hipóteses
fechadas. Ordena pelo que interessa antes de começar: primeiro o que já está
fechado.

*Testado nos três casos de 04-09. `ja_existe.py rede rega` devolve o
`rede_de_rega.py` em primeiro lugar, marcado JÁ FECHADO, com a primeira linha
do cabeçalho. Teria bastado.*

**A justificação é a que o utilizador deu, e é melhor do que a minha proposta
de arrumar a árvore:** nenhuma base de código séria foi lida por inteiro por
ninguém, e todas funcionam. O que a prática de topo faz com árvores grandes
não é indexá-las — é **tornar a procura barata e torná-la hábito**. Um índice
completo é caro de manter e envelhece; a procura não envelhece. E uma árvore
arrumada que não se consulta falha exactamente como uma desarrumada: a 04-09 a
causa não foi a desordem, foi eu não ter procurado.

### S2 · Nenhum artefacto sem produtor, com roquete · **executável**
Todo o `.json` escrito pelo processo leva o carimbo de quem o escreveu, quando,
e de que estado do repositório — `proveniencia.guardar()`. É a **regra 1 de
Sandve**: *for every result, keep track of how it was produced*, e é o que o
Sumatra automatiza.

*Medido: **52 dos 57 `.json` correntes** não trazem marca nenhuma. Um deles, o
`valvulas_v6.json`, traz a ordem espacial dos treze sectores — informação que
mais nenhum ficheiro tem — e **nenhum guião em disco a escreve**. Quando o
adversário perguntou se ela corroborava a leitura das etiquetas, a resposta foi
«não sei de onde vem», e por isso não pôde contar. Um número sem produtor não é
prova: é boato com casas decimais.*

**O roquete é o que torna isto praticável numa árvore herdada.** Retroactivar os
52 seria correr 52 guiões, alguns dos quais descarregam dados. A prática de topo
para dívida herdada não é pagá-la de uma vez — é **impedir que cresça**: fixa-se
a contagem como linha de base e o certificador **falha se ela subir**. Cada
guião tocado passa a usar `guardar()` e a dívida desce sozinha. Verificado: com
a linha de base artificialmente baixada, o certificador falha com código 1.

### S3 · Uma afirmação de ficheiro não alcançado entra por verificar · **prosa**
Um número lido no cabeçalho de um ficheiro fora do conjunto CORRENTE não se
repete: reproduz-se primeiro, ou vai marcado como não verificado.
*Repeti os «34 m» do `m1_v8_implantacao.py` — um ficheiro NAO_ALCANCADO — sem
correr o código, e não reconciliam: a mesma reconstrução põe a válvula 8 a
506 m da máscara. Usei-o para corrigir uma afirmação minha, o que espalhou o
erro em vez de o conter.*

---

## 4 · Onde isto deixa o processo

| forma | fechada por | estado |
|---|---|---|
| A · controlo dependente | C3 | prosa |
| B · teste sem poder | C1, C2 | **executável** |
| C · janela silenciosa | C4 | prosa (pré-voo 3 e 11 já a cobrem) |
| D · forma do modelo | C5 | prosa |
| E · cabeçalho divergente | C6 | prosa |
| F · insumo morto a jusante | C7 | **executável** |
| G · leitura tomada por sinal | — | **aberta** |
| H · repetir o que existe | C8, **S1** | **executável** |
| — · número sem origem rastreável | **S2** | **executável** |
| E · cabeçalho de ficheiro não alcançado | **S3** | prosa |

**A forma G continua aberta, e é honesto dizê-lo.** Não conheço maneira
mecânica de apanhar uma leitura minha errada — a ponta lida 600 px ao lado, os
focos com a designação invertida por quatro auditorias. O único remédio que a
literatura oferece é externo: dupla leitura independente, ou o adversário. Foi
o que funcionou das duas vezes.

E fica um limite que nenhuma cláusula levanta: **a máquina verifica coerência,
não verdade.** As vinte e três retiradas foram todas apanhadas por ir a um
instrumento diferente ou por alguém que sabe o terreno dizer «não é assim». A
cadeia certificada garante que não me contradigo. Não garante que tenha razão.

---

**Fontes.** Mayo & Spanos, *Error Statistics* (2011) · Lipsitch, Tchetgen
Tchetgen & Cohen, *Negative controls*, Epidemiology 21(3) (2010),
10.1097/EDE.0b013e3181d61eeb · Kapoor & Narayanan, *Leakage and the
reproducibility crisis in machine-learning-based science*, Patterns 4(9) (2023),
10.1016/j.patter.2023.100804 · Simonsohn, Simmons & Nelson, *Specification curve
analysis*, Nature Human Behaviour 4 (2020), 10.1038/s41562-020-0912-z · Coles,
Arslan, Tiokhin & Lakens, *Red Team Challenge* (2020-21).
