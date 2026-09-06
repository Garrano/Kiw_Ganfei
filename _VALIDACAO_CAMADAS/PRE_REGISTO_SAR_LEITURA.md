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
