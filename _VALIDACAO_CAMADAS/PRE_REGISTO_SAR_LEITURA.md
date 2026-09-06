# CRITÉRIO DE LEITURA — SAR de ano inteiro, 1613 cenas, 2016-2026

**Escrito a 06-09-2026, antes de olhar para a trajectória.** Vai a adversário
independente e **espera-se pela resposta** antes de qualquer leitura.

---

## 0 · O que eu já vi, e é obrigatório declarar

Não estou cego, e a diferença importa:

- **VI** o contraste de inverno do `c1_13_sar_serie.csv`, em espaço dB, agregação
  antiga: dez invernos entre +0,170 e −0,553, e **2025-26 a −1,256 (órbita 125) e
  −1,057 (147)**. Vi também que todas as unidades subiram +0,83 a +1,02 dB em
  2025-26 e que o oeste foi o único que não subiu.
- **NÃO VI** nada da série nova: nem verão, nem primavera, nem outono, nem
  nenhuma trajectória em potência linear.

Do ficheiro novo extraí **só ruído**, que é parâmetro de estorvo: σ por cena de
pares a ≤ 6 dias, e σ entre anos **calculado apenas na unidade de controlo**, que
é o nulo. Não olhei para nenhum foco em nenhuma estação.

## 1 · As unidades, e a que hoje mudou de estatuto

| unidade | fronteira | estatuto |
|---|---|---|
| **`zona0`** (oriental) | polígono fixo, escrito à mão, anterior ao acontecimento | **primária.** É a única fronteira limpa que temos |
| `este` (disco de 90 m) | centro `FOCO_ESTE`, rank 61 de 2421 | secundária |
| `oeste` (disco de 90 m) | centro `FOCO_OESTE` — **rank 4 de 2421, percentil 0,17 %** | **contaminada.** Só como confirmação de direcção, nunca de magnitude |
| `resto` | pomar menos os dois discos, menos `zona0`, menos referência | controlo |
| `referencia` | grelha regular de 110 células, ≥ 30 m do bordo, sem critério radiométrico | âncora (**auditada hoje e limpa**) |
| `nu2021` | chão lavrado de 2021 | segundo nulo |

**Ressalva que viaja com tudo:** a auditoria de 06-09 mediu que a referência
partilha **18 das 110 células (16 %)** com os discos dos focos. Nas leituras que
usam `resto − referencia` isso não morde, porque o `resto` exclui os discos. Nas
que usam `oeste − referencia` ou `este − referencia`, morde e **atenua**: o
resultado sai conservador.

E o `pomar` **não se usa** — 22,3 % dele vem de ortofoto posterior ao
acontecimento.

## 2 · SEVERIDADE — calculada antes, com o ano como unidade

A lição do `p8`: cenas dentro de um ano não são réplicas, porque a humidade e a
fenologia são comuns ao ano. σ entre anos, medido no controlo:

| estação | sd entre anos | SE (1 contra 9) | **MDE** (α 0,05; potência 80 %; t com 9 g.l.) |
|---|---|---|---|
| **Inverno** (Nov-Fev) | 0,117-0,153 | 0,123-0,160 | **0,39 a 0,50 dB** |
| **Primavera** (Mar-Mai) | 0,160-0,163 | 0,167-0,171 | **0,53 a 0,54 dB** |
| Verão (Jun-Ago) | 0,306-0,340 | 0,321-0,357 | 1,01 a 1,13 dB |
| Outono (Set-Out) | 0,272-0,292 | 0,287-0,307 | 0,90 a 0,97 dB |

**Declarado antes:** o instrumento tem **duas a três vezes mais potência no
Inverno e na Primavera** do que no Verão. Não é acaso — no Verão a retrodifusão
varia com o crescimento do copado. **Um resultado nulo no Verão é fraco e será
relatado como fraco.**

## 3 · As quatro perguntas, e o que decide cada uma

### P1 · O radar vê o acontecimento? (fecha a condição 2 do portão)

Contraste `zona0 − referencia` no ano hidrológico 2025-26 contra os nove
anteriores, **por estação e por órbita em separado**.

| | |
|---|---|
| **VÊ** | \|Δ\| ≥ MDE nas duas órbitas, mesmo sentido, na mesma estação |
| **UMA ÓRBITA SÓ** | artefacto de geometria — não é resultado |
| **NÃO VÊ** | \|Δ\| < MDE nas duas |

**«Não vê» não é «não houve».** O radar mede estrutura e humidade; um declínio
fisiológico sem alteração de estrutura é invisível. Escrito antes para não ser
negociado depois.

### P2 · Quando? (é o que o óptico não consegue)

Se P1 der **VÊ**, série mensal do contraste, e a transição localiza-se entre
duas datas consecutivas. Com ~23 cenas de inverno por ano e por órbita, a
revisita efectiva é de ~6 dias.

**Regra:** a datação só se publica se as **duas órbitas** puserem a transição
dentro da mesma janela de 30 dias. Se discordarem, publica-se o intervalo que
as contém e diz-se que discordam.

### P3 · Declínio ou arranque? (a maior condição aberta do processo)

É o par de canais que o inverno torna possível, e é a razão de ser deste
desenho:

| Verão (copado presente) | Inverno (sem folha; estrutura e solo) | leitura |
|---|---|---|
| cai | **não cai** | **DECLÍNIO** — a planta perdeu folha, a pérgola está de pé |
| cai | **cai também** | **ARRANQUE ou remoção de estrutura** |
| não cai | cai | não é copado — é solo ou instalação |

**Ressalva pré-registada:** o Verão tem MDE de ~1,1 dB contra ~0,45 no Inverno.
Um Verão que «não cai» pode ser falta de potência. Só se lê a primeira linha se
o Verão cair **acima** do seu próprio MDE; caso contrário o resultado é
**INDETERMINADO**, e diz-se.

### P4 · É encharcamento? (a explicação concorrente benigna, e nunca foi testada)

O foco ocidental é o ponto mais baixo da exploração, a 13,4 m da drenagem. Água
parada dá retrodifusão **baixa** por reflexão especular. Um inverno húmido com
encharcamento produz o padrão sem acontecimento nenhum no pomar.

**Discriminador:** se for encharcamento, a anomalia **depende da chuva
recente**; se for perda de copado, não depende.

Regressão do contraste sobre `dias_desde_chuva5` e `chuva_7d_mm`, dentro do
inverno, nos dez anos:

- **coeficiente significativo e a anomalia de 2025-26 desaparece ao controlar a
  chuva** → é **ENCHARCAMENTO**, e o acontecimento óptico continua por explicar
  por outra via;
- **coeficiente não significativo, ou a anomalia sobrevive ao controlo** → não é
  encharcamento;
- **e o teste directo:** o `nu2021` — chão lavrado, sem copado nenhum — tem de
  responder à chuva **mais** do que os focos. Se responder menos, o modelo de
  humidade está errado e o teste não decide.

## 4 · Controlos negativos, e correm ANTES das quatro perguntas

1. **`resto − referencia`** — duas unidades de kiwi vivo, mesma chuva, ninguém
   alega acontecimento em nenhuma. É o nulo de que saiu o σ deste documento.
2. **`nu2021 − referencia`** — chão sem copado.

**Pré-registado:** se o controlo 1 se deslocar ≥ MDE em 2025-26, **a leitura não
se faz** — o que se está a ver é o ano, não o pomar.

**Ressalva honesta, e é a lição do `p8`:** «ninguém alega» não é «sabe-se que não
houve». É um nulo assumido. Se o adversário souber construir um nulo *conhecido*
a partir do que há em disco — por exemplo metades disjuntas do próprio `resto`,
do tamanho de cada foco — esse ganha, e passo a usá-lo.

## 5 · O que este desenho NÃO faz

- **não diz a causa;**
- **não estima a magnitude ocidental** — a fronteira está no percentil 0,17 %
  do mapa que mede, e nada aqui corrige isso;
- **não usa o `pomar`**, por 22,3 % dele ser posterior ao acontecimento;
- **não reconcilia com o NDVI se discordar.** Se o radar disser uma coisa e o
  óptico outra, é um conflito a registar, não a resolver.

## 6 · Ficheiros

`sar_ler.py` lê `sar_ano_inteiro.csv` e escreve `sar_leitura.json`. **Não toca em
dados.** Carimbo de produtor.

---

## 7 · ADENDA de 06-09-2026 — três correcções em auto-verificação, antes de ler

O adversário da C9 foi cortado por limite de sessão ao fim de 18 comandos. A
última coisa que deixou escrita foi **«reprodução exacta»** sobre a recomputação
dos MDE do §2 — confirma a aritmética e não chegou ao resto. **A leitura não se
faz até ele voltar.** Entretanto fiz as verificações da tarefa dele que são
sobre a *geração dos dados* e não sobre o resultado.

### 7.1 · A desduplicação falhou, e o ficheiro estava a contar a dobrar

```
linhas originais       1613
pares (data,orbita) unicos  1013
duplicadas removidas    600
duplicadas DIVERGENTES    0   <- eram copias exactas
```

O `sar_ano_inteiro.py` desduplica por `(data, orbita)` na construção do
catálogo — e mesmo assim entraram 600 repetições. A causa provável: a corrida em
primeiro plano que julguei falhada continuou viva quando lancei a de fundo, e as
duas escreveram no mesmo ficheiro em modo `append`.

**É o mesmo defeito que o adversário apanhou no `c1_13`** — molduras contadas
como réplicas — entrado por outra porta, no ficheiro escrito para o evitar.
Nenhuma informação se perdeu (as duplicadas são idênticas), mas qualquer
variância calculada sobre o ficheiro bruto está errada.

**A leitura usa `sar_ano_inteiro_dedup.csv`.**

### 7.2 · A censura não existe, e a coluna que a auditaria não informa

As colunas `_n` são **idênticas nas quatro estações** para as seis unidades:
`oeste` 248, `este` 255, `zona0` 202, `resto` 2411, `referencia` 110, `nu2021`
167. O `a[a<=0] = nan` nunca disparou neste AOI. Boa notícia — e significa que
essa coluna, que eu tinha posto para tornar a censura auditável, não carrega
informação nenhuma.

### 7.3 · O confundimento de plataforma é real, e o ano de tratamento é o pior caso

```
ano     S1A   S1B   S1C   S1D
2016     57    14     0     0
2017     59    60     0     0
2018-21  ~60   ~57    0     0
2022     60     0     0     0
2023     56     0     0     0
2024     48     0     0     0
2025     60     0    45     0
2026     28     0    38    20
```

**O ano de tratamento é medido por dois satélites que não existem em nenhum ano
da linha de base.** O S1B falhou em Dezembro de 2021; o S1C entra em 2025 e o
S1D em 2026. E o campo vinha com maiúsculas inconsistentes (`SENTINEL-1A` contra
`sentinel-1a`), que partiria o mesmo satélite em dois a quem agrupasse pelo
texto.

**A correcção, e é barata:** o **S1A está presente em todos os onze anos**.
Restringir a ele dá uma série homogénea em plataforma de 2016 a 2026, e custa
quase nada em potência:

| estação | órb | anos | cenas/ano | sd entre anos | **MDE só S1A** | (MDE com tudo) |
|---|---|---|---|---|---|---|
| **Inverno** | 125 | 11 | 9 | 0,168 | **0,55** | 0,50 |
| **Inverno** | 147 | 11 | 9 | 0,135 | **0,44** | 0,39 |
| **Primavera** | 125 | 11 | 7 | 0,153 | **0,50** | 0,53 |
| **Primavera** | 147 | 11 | 7 | 0,160 | **0,53** | 0,54 |
| Verão | 125 | 11 | 7 | 0,351 | 1,16 | 1,13 |
| Verão | 147 | 10 | 7 | 0,278 | 0,94 | 1,01 |
| Outono | 125 | 10 | 5 | 0,283 | 0,95 | 0,90 |
| Outono | 147 | 10 | 5 | 0,306 | 1,03 | 0,97 |

**Pré-registado:** a leitura primária corre **só sobre o S1A**, 606 cenas, e os
MDE da coluna «só S1A» substituem os do §2. A série completa corre como
verificação de robustez secundária, e **se as duas discordarem, isso é
resultado** — significa que a mudança de constelação é visível, e o que se
publica é o S1A.

### 7.4 · O que isto não resolve

Nada disto toca no que o adversário ainda tem por atacar: as fronteiras das
estações, a janela de 30 dias do P2, a regra «mesmo sentido nas duas órbitas»,
a validade do teste de encharcamento, e o nulo conhecido que ele há-de propor.
**Continua por ler.**

---

# 8 · VERSÃO 2 — as nove correcções do adversário, aplicadas antes de ler

O adversário respondeu **antes da corrida** e não revelou nenhum foco. As nove
prescrições dele são o que se segue.

## 8.1 · O achado que reorganiza o desenho: as unidades sobrepõem-se

Matriz completa, verificada por mim célula a célula sobre as máscaras em disco:

```
             referencia  oeste   este  zona0 nu2021  resto
referencia          110     12      6      5      0      0
oeste                12    248      0      0      0      0
este                  6      0    255    176    101      0
zona0                 5      0    176    202     91      0
nu2021                0      0    101     91    167     63
resto                 0      0      0      0     63   2411
```

- **`zona0` ∩ `este` = 176 = 87,1 % da `zona0`.** A «primária» e a «secundária»
  do §1 são a mesma unidade. Lê-las às duas e vê-las concordar **não é
  corroboração — é aritmética.**
- **`zona0` ∩ `nu2021` = 91 = 45,0 %.** O segundo controlo negativo está metade
  dentro da unidade primária. Forma A.
- **`zona0` ∩ `referencia` = 5.** Não declarado no §2, que só declarava as 18
  dos discos.
- **`oeste` ∩ `nu2021` = 0.** É a **única** comparação limpa para o P4.

**Consequências, e substituem o §1:**

| | |
|---|---|
| `zona0` continua **primária** | mas **45 % dela é chão lavrado de 2021**, sem copado em ano nenhum. O P3 fica diluído por construção, e diz-se. |
| `este` **deixa de ser leitura** | é 87 % a mesma coisa. Reporta-se uma vez. |
| `nu2021` **deixa de ser nulo** para `zona0` e `este` | só vale contra o `oeste`, onde a partilha é zero |
| `resto` continua o controlo | zero partilha com qualquer foco |

## 8.2 · A polarização — a omissão mais barata de fechar, e a segunda mais grave

Nem o §2 nem P1-P4 diziam VV ou VH. Medido: **em VH o Verão tem MDE 0,50-0,55,
igual ao Inverno** — a ressalva inteira do P3 desaparecia se o leitor escolhesse
VH. É a forma que matou o segundo critério do registo: limiar por declarar, e
qualquer ramo seleccionável depois.

E a armadilha, para não se escolher VH pela potência. Tecto físico do sinal de
copado — amplitude sazonal do kiwi vivo menos a do chão nu, 2015-2024:

```
VV: orb125 +1,016 dB (p=0,0001)   orb147 +2,047 dB (p<0,0001)
VH: orb125 -0,137 dB (p=0,48)     orb147 +0,047 dB (p=0,87)
```

**Em VH o copado não contribui nada para a amplitude sazonal aqui.** O dobro da
potência e zero sensibilidade à grandeza que o P3 quer medir.

> **DECLARADO: a leitura é em VV.** Menos potência, mas é a única polarização que
> responde ao copado neste sítio. O VH corre como diagnóstico, nunca como leitura.

## 8.3 · As duas órbitas não são réplicas — e o MDE do P1 estava subestimado 1,36×

```
correlacao entre orbitas, contraste de controlo, anomalias: r = +0,901
  a concordancia de sinal remove 1,7x de falso positivo, nao ~30x
  poder REAL do veredicto «VE» com efeito = MDE:  46,9 %  (declarado 80 %)
  MDE VERDADEIRO do P1 = 1,36 x o declarado
     Inverno orb147: 0,40 -> 0,54     Inverno orb125: 0,52 -> 0,70
```

E o argumento físico, independente da estatística: o tecto de copado é +1,02 dB
numa órbita e +2,05 na outra. **Duas medições cujas sensibilidades diferem a
dobrar não são réplicas uma da outra.**

> **DECLARADO:** a leitura primária passa à **média das duas órbitas**, com o MDE
> recalculado sobre a média. A discordância de sentido fica como **bandeira de
> diagnóstico**, não como condição de veredicto.

## 8.4 · P3 — a célula DECLÍNIO era fisicamente inalcançável, e faltava a linha «subiu»

Tecto de copado em VV/orb125: **+1,016 dB**. Limiar que a minha ressalva exigia:
**0,98 dB**. A perda **total** do copado consumiria 96 % do limiar; com a
conjunção das órbitas o limiar subia a ~1,33 dB e **excedia o tecto**. A célula
DECLÍNIO não podia ser seleccionada por defeito nenhum da natureza. Forma B.

> **DECLARADO:** a ressalva do P3 reescreve-se em **unidades do tecto**, não do
> MDE. Uma queda de Verão conta como «cai» se exceder **metade do tecto** —
> 0,51 dB em orb125, 1,02 em orb147.

A tabela ganha as linhas que faltavam:

| Verão | Inverno | leitura |
|---|---|---|
| cai | não cai | **DECLÍNIO** |
| cai | cai | **ARRANQUE** ou remoção de estrutura |
| não cai | cai | não é copado — solo ou instalação |
| **sobe** | qualquer | **INDETERMINADO** — nenhuma hipótese o previa |
| não cai | não cai | **SEM SINAL** |

## 8.5 · A condição de modo comum — o buraco que matou o desenho irmão

```
sd entre anos do NIVEL da referencia (INV orb147) = 0,324 dB
sd entre anos do CONTRASTE                        = 0,122 dB
   -> o desenho descarta 62 % do movimento anual
amplitude do NIVEL da referencia entre anos de base: 0,91 dB
```

Deslocamentos comuns de ~0,9 dB são **rotina** nesta série. Nesse regime «o foco
caiu» e «a referência subiu e o foco não» produzem **o mesmo Δ**, e nenhuma das
quatro perguntas os separa.

> **DECLARADO:** publica-se, ao lado de cada Δ, o **nível absoluto** de
> `referencia` e de `resto` no ano de tratamento contra a distribuição dos anos
> de base. **Um deslocamento de modo comum ≥ 0,5 dB obriga a rotular o resultado
> como «modo comum não separável».**

## 8.6 · P2 — a janela de 30 dias admitia 45 % de concordâncias vazias

```
P(|t125 - t147| <= 30 d | datacoes ao acaso) = 0,449
   janela 12 d -> 0,195      janela 6 d -> 0,104
```

E o número que a sustentava estava errado: «~23 cenas de inverno, revisita ~6
dias» vinha do ficheiro com as 600 duplicadas. **Em S1A são 9-10 cenas e a
mediana é 12 dias.** O P2 contradizia o §7.3 dentro do mesmo documento.

> **DECLARADO: a janela do P2 é de 12 dias** — uma revisita — e a taxa de falsa
> concordância que ela admite, **19,5 %**, publica-se ao lado da datação.

## 8.7 · P4 — a verificação de sanidade estava ao contrário

Medido: o chão nu **fica mais brilhante** com chuva, `b = +0,012 / +0,013 dB/mm`,
`p < 0,0001` nas duas órbitas — resposta dieléctrica, **positiva**. O
encharcamento por reflexão especular faz o oposto: **mais escuro**, coeficiente
**negativo**.

A minha regra comparava **módulos de coeficientes de sinais opostos**: um foco
encharcado teria coeficiente negativo e grande em módulo, «responderia mais», e a
regra disparava NÃO DECIDE **exactamente no caso que o teste existe para apanhar**.

> **DECLARADO, e substitui o P4:**
> - **sanidade de SINAL, não de magnitude:** o `nu2021` deve ter coeficiente
>   **positivo e significativo** — já verificado, b = +0,012/+0,013, p < 0,0001;
> - **o discriminador é o SINAL do coeficiente do foco**, e são três previsões
>   distintas: encharcamento → **negativo**; humidade de solo sem água parada →
>   **positivo**; perda de copado → **nulo**;
> - **regressor principal `chuva_30d_mm`**, que existe no ficheiro e eu não usava.
>   `chuva_7d_mm` secundário. **`dias_desde_chuva5` sai** — 55 % das cenas em
>   {0,1,2} e 5,5 % censuradas no tecto de 31;
> - **agregação ao ano**, não regressão sobre cenas: a autocorrelação lag-1 é
>   +0,49 e +0,59, e o n efectivo é 3 a 4 vezes menor do que o aparente;
> - **corre contra o `oeste`**, a única unidade com partilha zero com o `nu2021`.

## 8.8 · O ano hidrológico, que eu nunca defini

Para o Inverno é indiferente; para o Verão do P3 é decisivo — 7 cenas ou 2,
consoante a convenção.

> **DECLARADO: o ano hidrológico começa a 1 de Setembro.** O Verão emparelhado
> com o Inverno de 2025-26 é **Jun-Ago de 2026**, com 3 e 2 cenas S1A contra 7-8
> nos anos de base. **A cobertura é fraca e o P3 no Verão sai com essa ressalva.**

## 8.9 · O nulo conhecido — e o meu era impossível

Eu sugerira «metades disjuntas do `resto`, do tamanho de cada foco». Medido:
**cabe exactamente UMA unidade disjunta de 90 m** no campo elegível. Um nulo
puramente espacial à escala do foco é impossível nesta exploração.

> **DECLARADO, e corre ANTES das quatro perguntas:** placebo temporal cruzado com
> colocação espacial — os 55 discos de 90 m inteiramente contidos no campo
> elegível, cruzados com 10 anos-placebo (cada ano de base tomado à vez como
> «tratamento» contra os nove restantes). **550 ensaios de verdade conhecida**,
> mas com **resolução independente ~40** — o menor p alcançável é ~1/41 ≈ 0,024,
> e é assim que se reporta, não como 550.
>
> A metade temporal **já correu**, sobre o controlo, e é o resultado mais forte
> deste documento: **VV — 0/10 falsos positivos nas quatro estações.** Sob verdade
> conhecida de «não houve», a regra do P1 não dispara uma vez.

## 8.10 · O que continua sem cobertura, e vai dito na leitura

- **O portão autoriza SAR confirmado por SAR.** A lista `INDICES` do `guarda.py`
  é puramente óptica; duas órbitas correlacionadas a **r = +0,90** passam como
  «instrumento independente». É a falha que o Controlo 3 apanhou no B1, na
  modalidade que o remendo não cobriu. **A conjunção das órbitas declara-se como
  diagnóstico, nunca como confirmação independente.**
- **Nenhuma condição do portão vê sobreposição de unidades.** A C3 continua em
  prosa, e era ela que teria apanhado o `nu2021` a 45 % dentro da `zona0`.

## 8.11 · O que ele atacou e aguentou

- a conclusão «Inverno e Primavera têm 2-3× mais potência» é **robusta às sete
  divisões de estação** testadas — não é artefacto de fronteira;
- a ressalva de contaminação do §2 está **certa em direcção e magnitude**: a
  atenuação é 10 % no oeste e 5 % no este, e é conservadora;
- **o portão do §4 não pode ser disparado pelo próprio efeito** — a extinção
  total da `zona0` desloca o controlo em ≤ 0,20 dB, metade do MDE de inverno;
- a composição ascendente/descendente é **1:1 com a órbita e constante** nos onze
  anos: a restrição ao S1A não introduz confundimento de geometria;
- o custo em potência dessa restrição é **~2 %** no SE do ano de tratamento;
- o `nu2021` **não revegetou**: o coeficiente de chuva mantém-se positivo e
  significativo em todos os anos de base.
