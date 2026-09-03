# Adversário da Camada 2 — revisão R2

**Data:** 31-08-2026
**Ataca:** `CAMADA_2_CERTIFICADO_R2.md`, secções PASSA PARA CIMA (S1–S8) e as
suas dependências.
**Método:** conforme `ADVERSARIO_PROMPT.md` — **nada foi recomputado e nenhum
dado bruto foi aberto.** O que se leu foi o certificado, o `PROTOCOLO.md`, o
`CONTROLOS.md` e o código que a camada escreveu. Onde faço falta a um dado,
digo qual é e não vou buscá-lo.

**Aviso de proveniência, e conta contra este documento:** a camada e o seu
adversário são a mesma sessão. `CONTROLOS.md` manda correr o adversário em
sessão paralela precisamente porque «duas sessões com o mesmo prompt cometem
erros correlacionados» — e aqui nem duas há. **Este adversário apanha lapsos de
execução e leituras erradas do próprio código. Não pode apanhar a premissa
falsa que eu partilho comigo mesmo.** Tratem-no como um piso, não como o
escrutínio que o controlo 3 exige.

---

## SUMÁRIO

**Quatro factos a reformular, três a manter com margem maior, uma falha dura de
procedimento, e uma pergunta que ninguém fez.** O certificado **não volta à
origem** — a estrutura do achado aguenta —, mas **não pode seguir como está**:
duas das reformulações são de redacção que induz em erro, e uma é um cabeçalho
que mente sobre o seu próprio código.

---

# PARTE 1 · FACTOS A REFORMULAR

## R1 · S3 — o cabeçalho do Landsat mente sobre o código. É a assinatura do `fazer_masks_v2`.

`landsat_independente.py`, linhas 22-23, docstring:

> «O preço: 30 m em vez de 10. O foco ESTE com pergola tem 1,27 ha, ou seja 14
> pixeis Landsat. Poucos. **Por isso só se usam pixeis inteiramente dentro da
> unidade, e reporta-se o n.**»

**O código não faz nem uma coisa nem outra.**

- Não selecciona píxeis inteiramente dentro. Faz `reproject(..., resampling=
  RS.nearest)` da cena Landsat **para a grelha de 10 m** e depois
  `np.median(ndvi[m])` sobre a máscara de 10 m. Cada píxel Landsat de 30 m
  passa a **nove células**, e a mediana corre sobre valores duplicados.
- **Não reporta n em lado nenhum.** A saída (`linha[nome] = float(np.median(v))`)
  não carrega contagem. Não existe n em `landsat.json`.

O único filtro é `if v.size < 0.5 * m.sum()`, que verifica fracção de células
finitas — não independência.

**O que teria de ser verdade para isto estar errado:** que eu tivesse lido mal
o `reproject`. Não tenho: `RS.nearest` para `DEST` na grelha de 10 m está
explícito.

**Porque importa.** Para «ORIENTAL com pérgola», 0,76 ha = 76 células ≈ **oito
píxeis Landsat independentes**. A mediana anual de cada ano assenta nisso. O p
exacto sobre 14 anos não muda de forma — é sobre médias anuais, não sobre
píxeis — mas **a incerteza de cada média anual está por declarar**, e o
certificado apresenta S3 sem uma única contagem.

**E é a assinatura exacta do erro que o `CLAUDE.md` do projecto nomeia:** um
cabeçalho que afirma uma coisa e um código que faz outra, com quatro auditorias
a passar por cima porque ninguém leu os dois juntos.

**O que cai com ele:** nada, em substância. **O que cai é o direito de S3 subir
sem n.** Reformular: *o Landsat replica a direcção e a datação; a magnitude
assenta em ~8 a ~25 píxeis independentes por unidade, e o n vai declarado.*

**Teste de cinco minutos:** contar píxeis Landsat distintos por unidade —
`len(np.unique(indice_do_pixel_landsat[m]))`. Uma linha.

## R2 · S2 — o ponto de quebra foi escolhido a olho, e os dois modelos não têm o mesmo número de parâmetros

`degrau_vs_recta_pergola.py` declara a comparação como justa: recta (declive +
ordenada) contra patamar-e-degrau (duas médias), «mesmo número de parâmetros».

**Não é justa.** `TARDIO = d >= "2025"` é uma constante escrita à mão. **O ponto
de quebra não foi ajustado: foi escolhido depois de se ver onde a série cai.**
Um modelo de degrau com ponto de quebra livre tem **três** parâmetros. Comparar
os seus resíduos com os de uma recta de dois é dar-lhe uma vantagem que não está
contabilizada.

**O que teria de ser verdade para isto não importar:** que o ponto de quebra
tivesse sido fixado antes de olhar para a série, ou que qualquer outro ponto de
quebra desse a mesma razão. Nenhuma das duas está demonstrada.

**E este defeito não é meu — é herdado.** A C2 publicou 4,35 : 1 e 4,05 : 1 com
a mesma construção, e a R2 reproduziu-a a 3,98 : 1 sem a questionar. **Duas
camadas correram a mesma comparação e nenhuma declarou o parâmetro escondido.**

**O que cai com ele:** o número 3,5–4,0 : 1, não a leitura. A série tem sete
pontos entre 0,824 e 0,879 e dois em 0,756 e 0,693; que aquilo é um degrau vê-se
sem modelo nenhum. **Reformular: retirar o rácio de S2, ou publicá-lo com o
ponto de quebra ajustado e penalizado.**

**Teste de cinco minutos:** recalcular a razão para **todos** os pontos de
quebra possíveis (há sete) e reportar o perfil. Se 2024|2025 for o máximo — e
vai ser — o valor honesto é o que sobra depois de descontar a escolha.

## R3 · S5 — a distribuição nula dos satélites não é permutável com os alvos

`satelites_sem_2026.py`:

```
UNIV = POMAR & COM & (dfoco > 120) & ~ZONA0
```

e os três alvos estão, por `satelites_degrau.json`, a **83 m, 112 m e 145 m** do
foco mais próximo.

**Dois dos três alvos vivem dentro da banda que a nula exclui.** A nula é
sorteada de `> 120 m`; os alvos #1 e #2 estão a 83 e 112 m. Estão a ser
comparados com uma população de outro estrato de distância.

**Objecção que eu próprio levantaria a isto:** S7 mostra que não há gradiente
com a distância, logo o estrato não deveria importar. **Não serve.** S7 testa
um **gradiente contínuo** por deslocamento toroidal; não testa se a banda
60–120 m difere em nível ou em variância da banda >120 m. São perguntas
diferentes, e a segunda nunca foi feita.

**O que cai com ele:** os percentis 2,4 / 4,7 / 8,7 %. **Não cai a base
2017-24 normal (0,878 · 0,872 · 0,901), que é medição directa e é o argumento
mais forte de S5.**

**Teste de cinco minutos:** redesenhar a nula em `60 < dfoco < 150` e ver se os
percentis se movem.

## R4 · S1 — o contraste é menos exposto ao degrau de plataforma, não imune

A R2 corrigiu-se bem ao passar do valor absoluto para o contraste. Mas escreveu:

> «Um degrau uniforme de plataforma cancela-se nesta diferença.»

**A palavra é «uniforme», e o V10 desta mesma camada mostra que não é.** Os
números dele: **−0,048** na mediana do que está fora do pomar e **−0,025** num
alvo de mata estável. Duas coberturas, dois valores, quase o dobro um do outro.
Se o desvio de plataforma varia com a cobertura, **não se cancela** entre foco
e controlo, que têm coberturas diferentes por construção — um é copado em
colapso, o outro copado são.

**O que cai com ele:** a palavra «imune». O contraste continua a ser a melhor
das duas moedas, e a diferença entre −0,048 e −0,025 (0,023) é pequena face a
−0,115. **Reformular: «menos exposto, com resíduo possível da ordem de 0,02».**

**Teste de cinco minutos:** medir o degrau de plataforma **no próprio controlo**
contra o alvo de mata do `c2_04_referencia.py`. Se forem iguais, o cancelamento
é bom.

---

# PARTE 2 · FACTOS A MANTER, COM MARGEM MAIOR

## M1 · S1b — «43 análises» não são 43, e a palavra «independentes» tem de sair

As unidades incluem **discos concêntricos de 60, 90 e 120 m no mesmo centro** e
**cinco limiares de altura encaixados** (0,3 ⊂ 0,5 ⊂ 1,0 ⊂ 1,5 ⊂ 2,0). O disco
de 60 está dentro do de 90, que está dentro do de 120; as células do limiar 2,0
são um subconjunto das do 0,3.

**Isto é aninhamento apresentado como replicação.** A afirmação honesta não é
«43 análises independentes concordam» — é **«o sinal e a ordenação são
invariantes em todo o espaço de análise percorrido»**, que é uma afirmação de
robustez e é verdadeira.

O certificado já escreve «43 análises» sem o adjectivo em S1b. **Mas escreve-o
em §1 CONFIRMADO: «sobrevive a 43 análises independentes».** Essa linha muda.

## M2 · S4 — a sonda fenológica tem duas premissas por declarar

1. **Linearidade.** Divide-se a diferença de 58 dias por 58 e aplica-se a 8,7.
   O NDVI está a 0,88 — perto da saturação — e a curva sazonal não é uma recta.
2. **Transporte de 2025 para 2017-2024.** O coeficiente é medido em 2025 e
   aplicado à diferença entre os dois grupos, um dos quais é 2017-2024.

A conclusão sobrevive porque a correcção é minúscula (≤ 0,0011) e porque está
declarada como limite superior. **Mas as duas premissas não estão escritas**, e
a segunda tem sinal desconhecido.

## M3 · S6 — a consequência é raciocinada, não medida

S6 afirma: «Todos os números na moeda do fosso são conservadores». O raciocínio
está certo — se a referência desce com os focos, o fosso encolhe. **Mas isso é
inferência, e o que a mediria é exactamente a reconstrução pré-registada que não
correu.** O certificado já tem o *line-stop*; **falta marcar a consequência como
inferida.**

---

# PARTE 3 · FALHA DURA DE PROCEDIMENTO

## O certificado não reporta uma única quantidade-âncora

`CONTROLOS.md`, controlo 2:

> «Um punhado de valores que **todas** as camadas reportam, sempre, na mesma
> secção do certificado, **mesmo que não lhes tenham tocado**.»

A `CAMADA_2_CERTIFICADO_R2.md` não reporta nenhuma das dez. Nem a AOI, nem os
píxeis do polígono, nem as cenas da série, nem os dois NDVI de referência.

**Isto não é formalidade.** O controlo existe para que «divergência entre
camadas salte sem ninguém comparar nada à mão» — e esta revisão mexeu
precisamente na referência, que é onde duas das dez âncoras vivem. **É a camada
com maior razão para as reportar e é a única que não as reporta.**

**Não segue sem isto.**

---

# PARTE 4 · AS TRANSVERSAIS

## A · A regra do instrumento independente — seis de nove factos falham

`CONTROLOS.md` controlo 1: «Se não houver instrumento independente disponível,
o facto vai para NÃO TESTÁVEL, **não para PASSA PARA CIMA**.»

| facto | instrumento independente |
|---|---|
| S1 · contraste | **não** — Sentinel-2 |
| S1b · invariância | **não** — Sentinel-2 (a partição é LiDAR, o sinal não) |
| S2 · degrau contra recta | **não** — decomposição interna |
| S3 · Landsat | **sim** — USGS/OLI/LaSRC |
| S4 · fenologia | **não** — Sentinel-2 |
| S5 · satélites | **não** — Sentinel-2 |
| S6 · contaminação da referência | **não** — propriedade da grelha |
| S7 · não há halo | **não** — Sentinel-2 |
| S8 · assimetria do radar | **sim** — Sentinel-1 |

**Dois de nove.** A leitura benigna é que S1/S1b/S2/S4 são todos o mesmo facto
visto de ângulos diferentes, e que S3 e S8 confirmam esse facto — o que é
verdade e é substancial. A leitura dura é que **o certificado passa sete factos
que a regra manda mandar para NÃO TESTÁVEL**, e não o discute em lado nenhum.

**Exijo que a secção CONFIRMADO nomeie, facto a facto, quando a coluna do
instrumento independente está vazia.** Duas delas dizem «—» com uma
justificação; as outras cinco não.

## B · A pergunta que falta

**Ninguém perguntou o que acontece ENTRE 2025-08-14 e 2026-07-27.**

O acontecimento inteiro está datado por **duas cenas separadas por onze meses**.
A regra de «plena estação» — que é boa e existe por razões fenológicas — descarta
tudo o que está entre elas. E depois toda a cadeia, desta camada até à C5,
escreve «um acontecimento, duas épocas».

**Um acontecimento catastrófico único e dois declínios sucessivos são
indistinguíveis neste desenho.** E não são a mesma coisa:

- para a **biologia**, um é compatível com um evento agudo (asfixia radicular,
  colapso apoplético), o outro com uma frente que avança;
- para a **gestão**, um justifica procurar o que aconteceu num momento, o outro
  justifica contenção;
- e para a **amostragem de Setembro**, decidem sítios diferentes.

O certificado escreve «degrau» dezenas de vezes. **Um degrau entre dois pontos a
onze meses de distância é uma interpolação, não uma medição.**

**Isto é o análogo da pergunta que faltou no `sentinel_b1`:** não é um cálculo
errado, é uma pergunta que ninguém fez porque a regra que a impedia era
sensata.

**O que preciso, e não vou buscar:** a contagem de cenas Sentinel-2 disponíveis
entre 2025-08-14 e 2026-07-27 que a regra de plena estação descartou, e a sua
distribuição por dia-do-ano. Se houver três ou quatro em Junho-Setembro de 2026
antes de 27-07, a pergunta é respondível **hoje** e sem dados novos.

## C · Entrou alguma coisa pela porta do lado?

**Uma, e é minha.** O `CAMADA_3_PROMPT_R2.md` escreve, na lista do que a C3
herda: «O padrão compatível é **descontínuo**, não difusivo.»

Isso **não está em S1–S8**. S7 diz que não há halo — um negativo. «Descontínuo»
é uma inferência construída a partir do negativo mais os satélites, e a camada 2
não tem competência para a fazer (regra 5: não teorizar acima da própria
camada). **Sai do prompt, ou entra em S como inferência marcada.**

## D · As quantidades-âncora

Não posso comparar: **o certificado não as reporta.** Ver Parte 3. É a única
transversal que não consigo executar, e a razão é o defeito.

---

# PARTE 5 · OS CINCO TESTES DE CINCO MINUTOS, POR VALOR

| # | teste | decide | custo |
|---|---|---|---|
| **1** | Recalcular a razão degrau/recta para os **sete** pontos de quebra possíveis, e reportar o perfil. | R2 — se o rácio é um achado ou uma escolha. | 10 linhas |
| **2** | Contar as cenas S2 entre 2025-08-14 e 2026-07-27 que a regra de plena estação descartou, e o seu DOY. | A pergunta que falta (B). Se houver cenas, muda o desenho da campanha. | 5 linhas |
| **3** | Redesenhar a nula dos satélites em `60 < d < 150 m`. | R3 — se os percentis são interpretáveis. | 2 linhas |
| **4** | Contar píxeis Landsat distintos por unidade. | R1 — a margem que S3 não tem. | 1 linha |
| **5** | Correr a reconstrução da referência, já pré-registada. | S6, e levanta a paragem de linha da moeda. | está escrita |

Os testes 1 e 2 são os que mudam afirmações. O 3 e o 4 põem margens em números
que já existem. O 5 é o único que pode reabrir a camada.

---

# VEREDICTO

**Segue para a camada 3 com retiradas e com margens, e NÃO segue sem as duas
correcções de procedimento.**

**Retira-se de PASSA PARA CIMA:**
- o rácio **3,5–4,0 : 1** de S2, até o ponto de quebra estar tratado (R2);
- os percentis **2,4 / 4,7 / 8,7 %** de S5, até a nula estar no mesmo estrato
  (R3). **A base 2017-24 normal fica** — é medição directa.

**Segue com redacção corrigida:**
- S1: «menos exposto», não «imune» (R4);
- S1b e §1: cai a palavra «independentes» (M1);
- S3: com o n declarado (R1);
- S4: com as duas premissas escritas (M2);
- S6: marcado como inferência (M3).

**Não segue sem:**
- as dez quantidades-âncora reportadas (Parte 3);
- a coluna do instrumento independente preenchida ou justificada facto a facto,
  com a contagem 2/9 dita em voz alta (Transversal A);
- a frase «padrão descontínuo» fora do prompt da C3 (Transversal C).

**O que passa intacto, e é bastante:** a contaminação da referência (S6, o
facto, não a consequência); a invariância de sinal e ordenação em todo o espaço
de análise; a replicação da direcção e da datação pelo Landsat; a assimetria do
radar com a sua explicação; o negativo do halo; e a base normal dos três
satélites antes de 2025.

**E fica dito uma segunda vez:** este adversário é a mesma sessão que escreveu o
certificado. O controlo 3 não foi cumprido. **A camada 2 continua sem o
escrutínio que o seu raio de explosão exige.**
