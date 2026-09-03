# MEMO OPERACIONAL — CONSTRUÇÃO DA INFOGRAFIA DE APRESENTAÇÃO
## Ganfei · Declínio da actinídea · Emparcelamento de Valença
**De:** sessão Cowork (remota) · **Para:** sessão Claude Code (local, Windows)
**Data:** 31-08-2026 · **Versão:** 1.0 · **Estado:** instruções executáveis

---

## 0. ANTES DE COMEÇAR — LEIA ISTO PRIMEIRO

### 0.1 O que esta sessão já viu
Tenho acesso de leitura a `C:\Users\Jackster2\Downloads\ganfei_s2` e a
`C:\Users\Jackster2\Downloads\_FIGURAS_DOSSIE`. Já li:
`_serie_geografica.txt`, `difusa_nucleos.csv`, `m2_nucleos.csv`,
`focos_datacao_geometria.csv`, `cota_vs_ndvi.csv`,
`lidar_topografia_por_mascara.csv`, `tracos_1995_coordenadas.csv`,
`pendente_pomares_novos.csv`, `b1_nucleo_serie.csv`, `expansao_b1.csv`,
`_pacote_cowork/LEIA-ME.md`, `_pacote_cowork/LACUNA_BIOTICA.md`, e as
figuras `F8_braudel.png`, `F13_hipoteses.png`, `F14_plano.png`.

**Não estou a pedir trabalho do zero.** O corpo de figuras existente é bom —
a F13 e a F14 estão a nível de publicação. O que falta é **arquitectura de
apresentação**: uma sequência com uma tese no topo, um público definido
(o chefe / CCDR-N interno, decidido com D em 31-08), e dois suportes
(página interactiva + conjunto impresso «legacy»).

### 0.2 O que mudou face ao dossier §27
O dossier `tier1-soa-framework-draft.md` está em v1.19 e **está
desactualizado**. A série com máscaras geográficas correu, e fecha o
bloqueio de §27.1. Os factos novos que a apresentação tem de usar:

- A **série sem máscaras** (`_serie_geografica.txt`) mostra o foco ocidental
  a emergir sozinho, só em 2025–2026 (`núcleo E~530480`). A nota do próprio
  ficheiro está certa e deve entrar na apresentação como texto:
  *«nas máscaras antigas ele estava definido desde o início, porque manchaW
  era o NDVI baixo de 2026 — não podia deixar de lá estar. Aqui tem de
  aparecer sozinho, e aparece.»*
- O **fosso da Zona 0 (sem solo nu de 2021) à referência** cresce
  **+0,01103/ano, p = 0,0162** — é o único resultado inferencial com p
  significativo do processo. É o número mais forte que temos.
- A **referência sistemática também desce** (0,888 em 2017 → 0,843 em 2026;
  declive −0,00395/ano, p = 0,1462, **não significativo**). Isto **corrige**
  o §19.2 do dossier («a referência não caiu em 2025»). A palavra
  «selectivo» sai da apresentação.
- **Sete hipóteses fechadas por medição** (F13): seca, ano mau regional,
  encharcamento por posição, rede de rega sobre-estendida, porta-enxerto,
  poda, arranque de linhas. Em particular: a **diluição hidráulica** está
  fechada (dentro do nulo em 11 de 11) e o **porta-enxerto** está fechado
  (−0,0004; IC95 −0,0015 a +0,0014). Ambas eram hipóteses de topo no
  dossier. **Saem da narrativa como candidatas e entram como fechadas.**
- **Três hipóteses por abrir**, todas pela mesma razão — ninguém procurou:
  patogénio de solo (zero ensaios com posição na válvula 8), PSA (nunca
  pedido ao laboratório), e a comparação regional (por fazer).

### 0.3 A tese da apresentação (o topo da pirâmide)
Uma frase, e tudo o resto é a sua expansão:

> **Sete explicações foram fechadas por medição. As três que continuam
> abertas continuam abertas porque ninguém as procurou — e a mais provável
> é uma doença de solo que nunca foi analisada onde o padrão está.
> Resolve-se em Setembro, com uma campanha de 12 plantas e 48 amostras,
> por 400 a 1.100 euros.**

Três pilares MECE por baixo:
- **A — O que sabemos.** Dois focos com data. O oriental degrada-se desde
  antes da série (p = 0,016). O ocidental nasce em 2025 e emerge sozinho de
  um mapa que nenhuma máscara define.
- **B — O que já não é.** Sete hipóteses fixadas antes de correr, corridas,
  refutadas. A custo zero, sem sair do gabinete.
- **C — O que falta.** A biologia. Nunca foi procurada onde o padrão está.
  Três acções, uma data, um orçamento, e uma via de isenção.

---

## 1. CONTRATO DE SAÍDA — ONDE DEIXAR TUDO

### 1.1 Pasta única
```
C:\Users\Jackster2\Downloads\ganfei_s2\_apresentacao\
```
**Criar esta pasta.** É a única pasta que esta sessão vai ler para recolher
o trabalho. Nada de resultados finais fora daqui. Estrutura obrigatória:

```
_apresentacao\
├── 00_ENTREGA.md              <- relatório para mim. Ler §9.
├── PALETA.md                  <- tokens finais, copiados de §3 e confirmados
├── NUMEROS_USADOS.csv         <- todo o número impresso, com origem. Ler §8.
├── PROVENIENCIA.csv           <- figura -> dados -> script -> data
├── figuras\
│   ├── png\                   <- A00..A11 a 300 dpi, A3 e A4
│   ├── svg\                   <- A00..A11 vectorial (fonttype=path)
│   ├── svg_editavel\          <- só as que D vai querer editar (fonttype=none)
│   └── bw\                    <- versão cinzentos de cada figura (teste)
├── timelapse\
│   ├── frames\                <- A05_f01.png .. A05_f09.png
│   ├── A05_timelapse.mp4
│   ├── A05_timelapse.webm
│   └── A05_timelapse.gif
├── pagina\
│   ├── index.html             <- página scrollytelling, ficheiro único
│   └── assets\                <- só se inevitável; preferir data: URI
├── dados\                     <- cópia CONGELADA do CSV que cada figura leu
└── scripts\                   <- a00_*.py .. a11_*.py + timelapse + página
```

### 1.2 Regra de congelamento
Cada figura lê o seu CSV a partir de `dados\`, **não** da raiz de
`ganfei_s2\`. Copiar o CSV para `dados\` no início do script e registar em
`PROVENIENCIA.csv` o `mtime` e o tamanho do original. Motivo: quando eu
recolher as figuras, quero conseguir refazer qualquer número sem depender
de o ficheiro de origem ter mudado entretanto.

### 1.3 Como eu recolho
Não faças nada. Eu leio `_apresentacao\` directamente e trago para cá o que
preciso. Só preciso que **`00_ENTREGA.md` exista e esteja actualizado** — é
o primeiro ficheiro que abro.

---

## 2. FORMATOS E MEDIDAS — EXACTOS

### 2.1 Dois tamanhos por figura, sempre
| Uso | Tamanho | Orientação | Margem | dpi PNG |
|---|---|---|---|---|
| Mestre / reunião / página | **A3 · 420 × 297 mm** | horizontal | 18 mm | 300 |
| Dossier impresso «legacy» | **A4 · 210 × 297 mm** | vertical | 15 mm | 300 |

Em matplotlib: `figsize=(16.54, 11.69)` para A3 horizontal e
`figsize=(8.27, 11.69)` para A4 vertical, `dpi=300` no `savefig`.

**A versão A4 não é um redimensionamento.** É uma reflow: o conteúdo que na
A3 está em duas colunas passa a empilhar. Se uma figura não couber em A4
com corpo a 10,5 pt legível, **divide-a em A4a/A4b** e diz-mo no
`00_ENTREGA.md`. Nunca encolher tipo abaixo de 9 pt para caber.

### 2.2 Decisão que tomo aqui, para não te bloquear
**Todas as figuras têm de sobreviver a fotocópia a preto-e-branco.** D ainda
não respondeu à pergunta, e o custo de a assumir é baixo enquanto o custo de
descobrir tarde é refazer treze figuras. Consequência operacional em §3.6.

### 2.3 Tipos de ficheiro
- `png\` — 300 dpi, fundo `#fcfcfb` **opaco** (não transparente: em Word um
  fundo transparente fica branco puro e quebra a harmonia).
- `svg\` — `matplotlib.rcParams['svg.fonttype'] = 'path'`. Garante que abre
  igual em qualquer máquina.
- `svg_editavel\` — `'none'`, só para A00, A03 e A11 (as que D vai querer
  mexer à mão).
- PDF combinado: **não** gerar por agora. Peço-o depois, quando a sequência
  estiver fechada.

### 2.4 O bug que tens de corrigir primeiro
**A `F8_braudel.png` está sem acentos.** «propria», «razao»,
«acontecimento», «decadas», «imovel». A `F13` tem os acentos todos certos —
logo é um problema de script, não de sistema. Antes de qualquer figura nova:

```python
import matplotlib as mpl
mpl.rcParams['font.family']   = 'DejaVu Sans'   # tem Latin-1 completo
mpl.rcParams['axes.unicode_minus'] = False       # usa U+2212 correcto
mpl.rcParams['svg.fonttype']  = 'path'
mpl.rcParams['pdf.fonttype']  = 42
```
E **nunca** normalizar/remover diacríticos no texto. Verificação em §8.4.

---

## 3. SISTEMA DE DESENHO — TOKENS FECHADOS, NÃO NEGOCIÁVEIS

Copia esta secção para `_apresentacao\PALETA.md` sem alterar valores. Já está
validada (separação sob daltonismo, contraste, banda de luminosidade). Não
substituas nenhum hexadecimal por gosto.

### 3.1 Superfícies e tinta
| Papel | Hex |
|---|---|
| Superfície da figura | `#fcfcfb` |
| Plano de página (faixas de fundo) | `#f9f9f7` |
| Tinta primária (títulos, valores) | `#0b0b0b` |
| Tinta secundária (corpo) | `#52514e` |
| Tinta atenuada (eixos, legendas, fonte) | `#898781` |
| Grelha (fio de cabelo) | `#e1e0d9` |
| Linha de base / eixo | `#c3c2b7` |
| Anel de contorno | `rgba(11,11,11,0.10)` |

### 3.2 Identidade — três entidades, três cores, para sempre
| Entidade | Papel | Hex | Nome curto na legenda |
|---|---|---|---|
| **Foco ORIENTAL** (Zona 0, válvulas 8–10) | slot 1 | `#2a78d6` | azul |
| **Foco OCIDENTAL** (Mancha W) | slot 2 | `#eb6834` | laranja |
| **Lóbulo OESTE isolado** (B1 a confirmar) | slot 3 | `#1baf7a` | água |

Isto confirma o que a `LEIA-ME.md` já adoptou. **Não acrescentar uma quarta
cor de identidade.** Se precisares de uma quarta entidade (ex.: o núcleo
interno de B1, ver §5-A07), usa **a mesma cor da entidade-mãe com traço a
tracejado** — é um subconjunto, não uma entidade nova.

### 3.3 Regra de separação de contextos — a mais importante das três
> **As cores de identidade nunca aparecem num painel raster.
> As cores da rampa nunca aparecem num gráfico de linhas.**

Nos mapas de défice a cor codifica **só magnitude**. A identidade dos focos
é carregada por **contorno a `#0b0b0b`, 1,5 pt, e rótulo directo**. Isto
evita que o azul signifique «Zona 0» num painel e «acima da referência» no
painel ao lado. Nas séries temporais, o inverso: identidade a cor, nenhuma
rampa presente.

### 3.4 Rampa do défice (só rasters)
Divergente **azul ↔ vermelho**, ponto neutro cinzento.
- Pólo positivo (acima da referência): `#2a78d6` → `#cde2fb`
- Neutro (zero): `#f0efec`
- Pólo negativo (défice): `#f6b8b8` → `#d03b3b` → `#7a1e1e`
- **Domínio fixo em todas as datas: −0,30 a +0,10, centrado em 0.**
  Domínio fixo é obrigatório — uma escala que muda por fotograma faz o
  timelapse mentir.
- Uma só barra de cor, partilhada, sempre no mesmo sítio.

### 3.5 Estados de evidência — a escala calibrada
Seis estados. **Cor + glifo + palavra, sempre os três.** Nunca cor sozinha.

| Estado | Quando se usa | Hex | Glifo |
|---|---|---|---|
| **CONFIRMADO** | ≥2 instrumentos independentes concordam | `#0ca30c` | ✔✔ |
| **PROVÁVEL** | um instrumento, ou inferência forte | `#fab219` | ◐ |
| **POR TESTAR** | plausível, nunca medido | `#898781` | ○ |
| **CONTRADITO** | medição em sentido contrário | `#d03b3b` | ✖ |
| **RETIRADO** | já foi afirmado e caiu | `#52514e` + risco | ⊘ |
| **SUSPENSO** | número existe mas não é publicável | `#ec835a` + trama | ⏸ |

Estes hexadecimais são do conjunto de estado e **nunca** são usados como cor
de série. Se um vermelho de estado ficar ao lado do vermelho da rampa, é
por isso que a palavra e o glifo são obrigatórios.

**`RETIRADO` aparece na apresentação de propósito.** O que foi retirado é
prova de auto-correcção — é o argumento que financia a fase seguinte. Lista
mínima que tem de aparecer em A08 com o carimbo ⊘: o sinal térmico como
«primeira detecção fisiológica» (é contabilidade de copado), a narrativa de
alastramento concêntrico a partir da Zona 0, a radiometria das ortofotos
DGT, e as máscaras derivadas do NDVI de 2026.

### 3.6 Medição vs testemunho, e a sobrevivência a fotocópia
Dois canais que não são cor:

**Canal 1 — proveniência da afirmação:**
- **Medição** → traço cheio, marcador preenchido.
- **Testemunho** → traço a **ponteado** (`linestyle=(0,(1,2))`), marcador
  vazado, e o texto entre aspas com o autor nomeado:
  *«a mancha alastra concentricamente» — Eng.ª Cláudia, visita 04-08-2026*.
- **Inferência nossa** → traço a tracejado longo, sem marcador.

**Canal 2 — sobrevivência a P&B:** cada categoria tem também **forma** e,
nas áreas, **trama**:
- Foco oriental → círculo · trama a 45°
- Foco ocidental → losango · trama a 135°
- Lóbulo oeste → triângulo · sem trama
Usa `hatch='///'` e `'\\\\\\'` em matplotlib; `hatch.linewidth` a 0,6.

### 3.7 Tipografia — escala fixa em pontos no tamanho final
| Papel | pt (A3) | pt (A4) | Peso |
|---|---|---|---|
| Título-mensagem | 26 | 20 | bold |
| Linha de apoio (dek) | 13 | 11 | regular |
| Cabeçalho de secção | 15 | 13 | bold, VERSALETE, espaçado |
| Corpo / anotação | 10,5 | 9,5 | regular |
| Número herói | 34 | 26 | bold |
| Legenda / fonte / rodapé | 8,5 | 8 | regular, `#898781` |

Nada em serifa. Nada em itálico excepto citações de testemunho. Números
grandes com figuras proporcionais; `tabular-nums` **só** em colunas que
alinham verticalmente.

### 3.8 Grelha e espaçamento
- A3: 12 colunas, goteira 6 mm, margem 18 mm.
- A4: 6 colunas, goteira 5 mm, margem 15 mm.
- Distância mínima entre qualquer rótulo e qualquer outro elemento: **3 mm**.
  Isto não é estética — a `F14` tem **sobreposição real** no canto inferior
  esquerdo («PAR SÃO ocidental / v6 · B2» por cima de «âncora de CAMPO» e o
  rótulo `T1` a chocar com `U1`). É correcção obrigatória.

### 3.9 Anatomia obrigatória de toda a figura
De cima para baixo, sempre nesta ordem:
1. **Título-mensagem** — a conclusão, não o tema. «A Mancha W não existia em
   2024» e não «Evolução do NDVI 2018-2026».
2. **Dek** — uma linha: o que é preciso saber para ler a figura.
3. **Corpo.**
4. **Rodapé de proveniência**, a 8,5 pt `#898781`, com **quatro campos
   sempre**: `Dados: … · Instrumento: … · Estado: … · Script: …`
   Exemplo real:
   `Dados: _serie_geografica.txt (28-08-2026) · Instrumento: Sentinel-2 L2A, 9 cenas de Verão · Estado: CONFIRMADO · Script: a04_serie_sem_mascaras.py`

### 3.10 Proibições
- **Nunca** duplo eixo vertical.
- **Nunca** um número em cada ponto — rótulos directos selectivos.
- **Nunca** cor sozinha a carregar significado.
- **Nunca** polígono de linha dura numa fronteira incerta — banda.
- **Nunca** o texto de um valor pintado com a cor da série; texto usa tinta.
- **Nunca** arco-íris; nunca uma cor no ponto médio de uma rampa divergente.
- **Nunca** inventar precisão: se a posição vem de um oval desenhado à mão,
  desenha-se como oval difuso com a nota, ou não se desenha.

---

## 4. A SEQUÊNCIA — DOZE PEÇAS, A00 A A11

Estrutura Braudel (estrutura → conjuntura → acontecimento) por baixo, mas
**a palavra «Braudel» só aparece na versão técnica**, nunca na do chefe: para
um decisor administrativo lê-se como ornamento e gasta credibilidade.

Para cada peça dou: **mensagem · candidato existente · o que fazer · dados ·
o que NÃO desenhar · verificação.**

**Primeira tarefa antes de desenhar seja o que for:** abre a `figuras\` e
mapeia F1–F14 + M1v8 + M2 contra os doze lugares abaixo. Escreve esse
mapeamento em `00_ENTREGA.md` §1. Só vi F8, F13 e F14 — o mapeamento das
outras é teu, e confio nele.

---

### A00 · O CASO NUMA PÁGINA — **NOVA**
- **Mensagem:** «Sete explicações fechadas por medição; três abertas porque
  ninguém procurou; a resposta custa 400 a 1.100 euros e uma campanha de
  Setembro.»
- **Formato:** só A4 vertical. É o papel que circula sozinho.
- **Conteúdo, nesta ordem e nada mais:**
  1. Título-mensagem a 20 pt.
  2. Três **números-herói** em linha, a 26 pt, com legenda de uma linha:
     `7` hipóteses fechadas · `3` por abrir · `0` análises de patogénio no
     foco mais antigo.
  3. Um mapa pequeno (≤ 70 mm de altura): o pomar, os dois focos com rótulo,
     escala de 200 m, norte. Sem rampa, sem legenda técnica — dois contornos
     e dois nomes.
  4. Quatro linhas de «o que aconteceu», em português corrente, **sem uma
     única sigla**. Nada de NDVI, RNQP, KVDS, PCR, qPCR, ITS. Se um termo é
     inevitável, glosa-o na mesma frase.
  5. Um bloco de decisão: o que se pede, a quem, até quando, quanto custa.
- **O que NÃO desenhar:** rampa de cor, eixos, valores de p, nomes de
  organismos, coordenadas.
- **Verificação:** dá a ler a alguém que não conheça o caso. Se perguntar «o
  que é NDVI?», a peça falhou.

---

### A01 · OS TRÊS REGISTOS DE TEMPO — **F8, corrigir**
- **Mensagem (manter):** «O acontecimento ocupa dois anos, a conjuntura que
  o hospeda ocupa trinta e cinco, e a estrutura não tem data.»
- **Está bom.** A ideia das três faixas com escalas próprias e o triângulo
  de ligação diagonal é a melhor peça conceptual do conjunto.
- **Corrigir, por ordem:**
  1. **Acentos** (§2.4). Toda a figura está sem diacríticos.
  2. Acrescentar a **etiqueta de estado §3.5 a cada facto**. Neste momento
     factos confirmados e inferências têm o mesmo peso visual. Em concreto:
     `Emparcelamento` → PROVÁVEL (não há telas finais); `LiDAR 06-07-2025`
     → CONFIRMADO; `+11,16 ha de pomar novo` → CONFIRMADO, mas o «toda a
     água da mesma origem» → **agora CONTRADITO como causa** (F13 fecha a
     diluição: dentro do nulo em 11 de 11). **Corrigir o texto**, não só a
     etiqueta.
  3. A faixa CONJUNTURA tem de ser desenhada como **sabidamente incompleta**
     — fundo esbatido e a nota «registo reconstruído a posteriori a partir
     de testemunho; ausência de marca não significa ausência de operação».
  4. `carência de cálcio confirmada em duas matrizes` (caixa OESTE) precisa
     de etiqueta e fonte no rodapé — é uma afirmação nova e forte.
  5. `13,4 m do dreno` / `55,8 m do dreno`: identificar no rodapé **que**
     dreno e de onde vem a geometria. Se vem do MDT/escoamento e não das
     telas finais do emparcelamento, tem de dizer isso.
- **O que NÃO desenhar:** seta causal de nenhuma faixa para outra. A figura
  mostra co-ocorrência de escalas, não causalidade.

---

### A02 · A ESTRUTURA: DOIS PONTOS HIDRAULICAMENTE OPOSTOS — **F8 (banda inferior) → figura própria**
- **Mensagem:** «Os dois focos ocupam os extremos opostos de um campo com
  2,1 m de amplitude total — e, dentro do copado, o terreno baixo é o
  terreno bom.»
- **Construir:** perfil topográfico E→W a partir do MDT LiDAR 50 cm, com os
  dois focos marcados, e ao lado o gráfico de dispersão cota × NDVI 2026 com
  a recta de regressão e os dois focos assinalados como resíduos.
- **Dados:** `lidar_topografia_por_mascara.csv`, `cota_vs_ndvi.csv`.
  Valores a imprimir: mediana OCIDENTAL 6,67 m (percentil 32 do pomar),
  ORIENTAL 8,03 m (percentil 92); declive −0,0579 NDVI/m; r = −0,338;
  n = 2258 fora dos focos; défice face ao previsto pela cota: −0,107
  (ocidental) e −0,122 (oriental).
- **Escopo obrigatório no título ou no dek:** «**dentro do copado do
  pomar**». A regressão inverte de sinal (r = +0,325) se a AOI inteira
  entrar, porque inclui o rio. Se isto não estiver escrito, a figura é
  falsa a nível de paisagem.
- **Nota crítica no corpo:** `r² ≈ 11 %` — a cota explica pouco. A figura
  serve para **excluir o encharcamento por posição**, não para explicar o
  declínio.
- **O que NÃO desenhar:** nada que sugira que a cota causa o declínio.

---

### A03 · CRONOLOGIA DE TRÊS FAIXAS — **F3, corrigir**
- **Mensagem:** «Satélite, gestão e laboratório num só eixo — e a faixa da
  gestão está vazia porque não foi registada, não porque nada aconteceu.»
- **Corrigir:**
  1. **Retirar a seta causal «degrau 2021 ⇒ não pode ser diluição».** A
     diluição já está fechada por outra via (F13), e o degrau de 2021 nunca
     passou no teste de changepoint.
  2. Barras dos pomares novos anotadas «**ano de DETECÇÃO de copado**
     (plantação ≈ ano−1; obras antes)». Valores de
     `pendente_pomares_novos.csv`: 2022 → 4,09 ha (blocos 4 e 6);
     2023 → 2,85 (1, 2, 8); 2024 → 1,50 (5, 7); 2025 → 2,72 (bloco 3).
     Total 11,16 ha. **A maior coorte é 2022, não 2025** — confirmado no CSV.
  3. Faixa de gestão a fundo esbatido com a nota de incompletude.
  4. Faixa de laboratório: **separar visualmente B3C3 (válvula 27, parcela
     isolada) do corpo principal**. O *P. sojae* do Becrop é de B3C3. Já foi
     corrigido em 28-08 — confirma que se manteve.

---

### A04 · AS MANCHAS EMERGEM SOZINHAS — **NOVA · PRIORIDADE MÁXIMA**
Esta é a figura que fecha a acusação de circularidade das máscaras. **Não
existe ainda e é a mais importante do conjunto.**
- **Mensagem:** «Quando nenhuma máscara define as manchas, o foco ocidental
  aparece só em 2025 — e o oriental está lá desde a primeira cena.»
- **Construir, dois painéis:**
  - **Painel esquerdo — os núcleos por ano.** Uma linha por ano (2017 a
    2026), e em cada linha os núcleos ≥ 0,15 ha posicionados pela sua
    coordenada E, com a área a controlar o tamanho do símbolo. O leitor vê
    a coluna em E≈530 970 presente em **todas** as linhas, e a coluna em
    E≈530 480 a **aparecer só nas duas últimas**.
  - **Painel direito — o fosso à referência.** Duas séries: `Zona 0` e
    `Zona 0 sem solo nu 2021`. Imprimir o declive e o p da segunda:
    **+0,01103/ano, p = 0,0162**. E, a traço fino e atenuada, a referência
    sistemática em nível absoluto, com o seu declive
    **−0,00395/ano, p = 0,1462 (não significativo)**.
- **Dados:** `_serie_geografica.txt` (parsear; se preferires, exporta
  primeiro para `dados\serie_geografica.csv` e regista-o).
- **Texto obrigatório no corpo, quase literal do ficheiro:**
  «Nas máscaras antigas o núcleo ocidental estava definido desde o início,
  porque `manchaW` era o NDVI baixo de 2026 — não podia deixar de lá estar.
  Aqui tem de aparecer sozinho, e aparece.»
- **Ressalva obrigatória:** 2017 tem critério não comparável em área
  (referência a 0,838, fase de instalação) — desenhar 2017 a cinzento e
  fora da leitura de tendência, mas **presente**, porque o seu núcleo
  oriental de 7,55 ha é real e valida a antiguidade do foco.
- **O que NÃO desenhar:** áreas derivadas das máscaras antigas
  (4,23 ha manchaW, 29,1 ha pomar, 11,5 ha défice, 84,3 %). Estão suspensas.
- **Verificação:** os números do painel esquerdo têm de reproduzir
  exactamente as linhas «MANCHAS QUE EMERGEM DO MAPA DE DEFICE».

---

### A05 · TIMELAPSE — **NOVA** · especificação completa em §6
- **Mensagem:** «Nove verões, uma escala de cor fixa: o oriental não sara e
  o ocidental nasce.»
- Só existe na página e na reunião. **Nunca sozinho** — ver A06.

---

### A06 · O GÉMEO ESTÁTICO DO TIMELAPSE — **NOVA** (base: `defice_miniaturas.png`)
- **Mensagem:** a mesma de A05.
- **Porque existe:** medição publicada (Robertson et al., IEEE TVCG 2008):
  a animação é ~60 % mais rápida em modo *apresentação* mas ~82 % mais lenta
  e **significativamente menos exacta** em modo *análise*, contra pequenos
  múltiplos. Quem lê sozinho e quem contesta precisa da grelha. **Esta é a
  figura que vai impressa no dossier; o timelapse não vai.**
- **Construir:** grelha 3 × 3, nove cenas de registo (2017 a cinzento como
  prólogo fora da grelha, se couber), **mesma extensão, mesma rampa, uma só
  barra de cor**, data + área de défice por baixo de cada painel.
- **Dados:** `sentinel\*.tif` + máscaras geográficas
  (`sentinel\masks_geograficas.json`).

---

### A07 · CHAVE ESPACIAL E OS SATÉLITES — **F4 + M2, corrigir**
- **Mensagem:** «As frentes já saíram das manchas desenhadas: há três núcleos
  destacados a 79, 82 e 143 metros.»
- **Dados:** `difusa_nucleos.csv` (valores exactos: #1 0,21 ha, UTM
  531016/4655184, 79 m do foco oriental; #2 0,24 ha, 530889/4655118, 82 m do
  oriental; #3 0,21 ha, 530359/4654986, **143 m do ocidental**);
  `m2_nucleos.csv`; `focos_datacao_geometria.csv`.
- **Corrigir / garantir:**
  1. **Excluir a faixa de bordo ≤ 1 píxel ANTES da abertura morfológica** —
     0,6 a 1,3 ha do défice em todos os anos é píxel misto de fronteira, e
     entra como se fosse doença.
  2. **Garantir que os três núcleos sobrevivem à abertura** (têm 21–24 px).
     Se a abertura os apagar, desenhá-los como símbolos próprios.
  3. **Grelha de sensibilidade na legenda**: elemento estruturante ∈ {1,2,3}
     px × limiar ∈ {−0,03, −0,05, −0,07} → mínimo e máximo da área. Fronteira
     como **banda**, não linha dura.
  4. **Distinguir polígono de crescimento de banda de colheita viva.** A
     amostragem vai à margem verde→amarelo, não ao núcleo morto. Se a
     figura não separar os dois, o plano de Setembro herda o erro.
  5. Manter a decisão — certa — de **não desenhar sectores de válvulas**
     (o esquema não tem coordenadas; o erro de escala M1 pôs as válvulas
     1–5 a 2 km de distância). Escrever essa razão na figura.
- **Nota que vale a pena investigar antes de desenhar:** em
  `focos_datacao_geometria.csv` a orientação do foco ocidental passa de ~50°
  (2017-18) para **165–168° (2025-26)**, com alongamento 1,44 e eixo maior
  129 m em 2026. O traço L1 de 1995 tem azimute ~89°. **Resolve primeiro a
  convenção angular do teu `regionprops`** (0° = eixo x? sentido?) e só
  depois digas se há ou não alinhamento. Se depois de resolvida a convenção
  o alinhamento existir, é um resultado; se não existir, é um negativo útil
  que fecha o L1. **Não afirmes nenhum dos dois sem resolver a convenção.**

---

### A08 · O QUE JÁ NÃO É, E O QUE FALTA SABER — **F13, polir**
- **É a melhor figura do conjunto.** A estrutura «hipótese fixada antes de
  correr · instrumento · resultado numérico à direita» é exactamente a
  gramática certa e já está a nível de publicação.
- **Acrescentar:**
  1. Um terceiro bloco, curto, por baixo dos dois: **RETIRADO** (§3.5) — o
     que já foi afirmado neste processo e caiu. Quatro linhas chegam. É a
     peça de credibilidade e não existe em lado nenhum.
  2. Em cada linha «JÁ FECHADO», anotar **o que a exclusão não cobre**. A
     convergência para o subsolo é uma propriedade dos instrumentos de
     superfície, não uma medição do campo — e tem de estar escrito, senão a
     figura promete mais do que mede.
  3. Na linha «Encharcamento por posição no terreno», acrescentar o escopo
     «dentro do copado» (mesma razão de A02).
- **Não mexer:** nos valores, na ordenação, nos glifos, na cor. Está certo.

---

### A09 · O LIVRO-RAZÃO DAS EXCLUSÕES — **F2, decidir**
A F13 cobre agora quase tudo o que a F2 fazia, e melhor. **Proposta: a F2
sai da sequência de apresentação e passa a anexo técnico** (para o INIAV e
para quem contesta), com as duas correcções que a revisão de figuras exigiu:
sai a seta «⇒ 40–80 cm» (o alvo honesto é o perfil completo **0–120 cm**), e
cada linha da coluna «o que a exclusão não cobre» anotada como lacuna
**forçada pela física do instrumento** ou **editorial**.
**Decide tu e diz-me em `00_ENTREGA.md`.** Se achares que a F2 acrescenta ao
chefe, fica em A09; se não, A09 fica vazio e a sequência tem onze peças.

---

### A10 · O QUE NOS FARIA MUDAR DE IDEIAS — **NOVA**
- **Mensagem:** «O modelo está escrito de forma a poder ser refutado — e
  estas são as três medições que o refutam.»
- **Conteúdo:** os três critérios de refutação, desenhados como três cartões
  com «se acontecer X → o modelo cai»:
  1. os registos de rega/bombagem 2024-25 não mostram nenhuma anomalia nos
     sectores dos focos;
  2. as covas não encontram água suspensa, nem horizonte impermeável, nem
     dreno degradado sob o foco ocidental;
  3. os painéis de margem não mostram diferencial de carga de patogénios
     face aos controlos assintomáticos emparelhados.
- **Porquê:** é a peça que distingue um dossier de uma narrativa, e é o
  argumento que sustenta a proposta de isenção junto do Conselho Directivo.
- **Nota:** a F14 já faz isto **por ponto de amostragem** («se POSITIVO / se
  NEGATIVO»). A A10 fá-lo **ao nível do modelo**. São complementares; se
  achares que se fundem numa só, funde e diz-mo.

---

### A11 · O PLANO DE SETEMBRO — **F14, corrigir**
- **Está muito boa.** 12 plantas, 48 amostras, quatro matrizes, e a
  pré-inscrição do que cada resultado conclui. Manter tudo isso.
- **Corrigir:**
  1. **Sobreposições de rótulo** no canto inferior esquerdo: «PAR SÃO
     ocidental / v6 · B2» colide com «âncora de CAMPO, não nossa…» e o
     rótulo «T1» colide com «U1». Regra dos 3 mm de §3.8.
  2. Acrescentar, num rodapé próprio, **o orçamento e a via**: núcleo mínimo
     €360–480, painel Tier-1 completo €700–1.100, ambos **+ IVA**, tabela
     Deliberação n.º 603/2024, com a via de **isenção por manifesto interesse
     público** (proposta fundamentada ao Conselho Directivo do INIAV, ou
     protocolo de colaboração). Sem isto a figura pede sem custear.
  3. Marcar explicitamente que **o foco oriental nunca teve painel de
     patogénios** — só comunidade ITS, e essas quatro amostras retêm 29 %,
     3 %, 4 % e 10 % das leituras, o que não permite comparar diversidade.
     É a justificação central de toda a campanha e tem de estar na figura
     que a pede.

---

## 5. UMA PEÇA QUE PODE VIR A SER A DÉCIMA TERCEIRA

`b1_nucleo_serie.csv` mostra que, **dentro** do lóbulo oeste, há um núcleo
interno a divergir do resto do bloco de forma monótona:
−0,017 (2017) → −0,088 (2021) → −0,104 (2022) → −0,128 (Ago 2025) →
**−0,158 (2026)**. Isto é um terceiro objecto, com dez anos de história e
sem qualquer atenção no dossier.

**Não desenhes já.** Verifica primeiro se este núcleo é: (a) um terceiro
foco incipiente, (b) o efeito das duas decotes/enxertias de 2016 e 2020 numa
sub-área, ou (c) uma sub-parcela com outra idade/gestão. Se for (a), é uma
figura própria e muda a mensagem da apresentação — o caso passa de dois
focos a um processo que se repete. **Diz-me o que encontras antes de
construir.**

---

## 6. TIMELAPSE — ESPECIFICAÇÃO COMPLETA (A05)

### 6.1 Fotogramas
Nove cenas de registo, uma por fotograma, por ordem:
`2018-08-31, 2020-07-18, 2021-07-16, 2022-07-31, 2023-08-07, 2024-07-22,
2025-06-17, 2025-08-14, 2026-07-27`.
`2017-07-02` entra como **prólogo**, primeiro fotograma, com tarja
«critério não comparável — fase de instalação» e a rampa esbatida a 60 %.
`2019-09-02` fica **fora** (sinalizador de fenologia) e a ausência é
declarada no rodapé — não se salta uma data em silêncio.

### 6.2 O que cada fotograma mostra
- Raster de **défice por píxel** = NDVI(cena) − média da referência
  geográfica **nessa mesma cena**. Recortado à máscara geográfica do pomar.
- Rampa divergente de §3.4, **domínio fixo −0,30 a +0,10 em todos os
  fotogramas**, barra de cor sempre no mesmo sítio e sempre visível.
- **Nada de máscaras de mancha desenhadas por cima.** O ponto desta peça é
  que as manchas aparecem sozinhas. Se puseres o contorno de `manchaW` por
  cima, destróis exactamente o argumento.

### 6.3 Elementos fixos (não se movem entre fotogramas)
Canto superior esquerdo: título. Canto superior direito: **a data em 34 pt**.
Em baixo: régua do tempo 2017→2026 com um cursor a andar. Escala de 200 m e
seta de norte no canto inferior direito. Barra de cor à direita.

### 6.4 Anotações — aparecem e ficam
| A partir de | Texto |
|---|---|
| 2018 | «foco oriental já presente» |
| 2024 | «défice mínimo do período» |
| 2025-08 | «**aparece o foco ocidental**» ← o momento da peça |
| 2026 | «4,03 ha · amplitude 0,30» |
Aparecem com fade de 0,3 s e **não desaparecem**. O leitor tem de terminar a
ver a soma, não o último fotograma isolado.

### 6.5 Tempos e exportação
- 1,2 s por fotograma + 0,4 s de fade. Paragem de **2,5 s** no fotograma
  2025-08-14 (é o achado).
- `A05_timelapse.mp4`: H.264, `yuv420p`, dimensões **pares**, 1920 × 1200.
- `A05_timelapse.webm`: VP9, mesmas dimensões.
- `A05_timelapse.gif`: 10 fps, paleta optimizada, **≤ 8 MB**. Se não couber,
  reduz para 1280 × 800 antes de reduzir a qualidade.
- `frames\A05_f01.png` … `f10.png` a 300 dpi — são o material da A06 e o
  material de recurso se o vídeo não passar num sistema.

### 6.6 Na página
Controlado por **scroll** (o leitor puxa o tempo), **sem auto-play**, com um
botão «reproduzir» para quem quiser a versão narrada. O `.mp4` é para a
reunião. Justificação em A06.

---

## 7. A PÁGINA (scrollytelling) — `pagina\index.html`

**Constrói-a depois das figuras, não antes.** As figuras são a fonte; a
página é a montagem.

- **Ficheiro único.** CSS e JS embutidos. Imagens como `data:` URI. Sem
  dependências externas — vai ser publicada como Artifact e nesse ambiente
  os hosts externos estão bloqueados.
- **Estrutura em copo de martini:** o caule é a narrativa conduzida (A00 →
  A01 → A04 → A05 → A08 → A11); a boca aberta são os cartões expansíveis com
  o resto (A02, A03, A06, A07, A09, A10) e as ligações aos CSV.
- **Menu de cinco módulos** (a estrutura é do Food Systems Dashboard,
  traduzida): `Herança · Pressões · O que se vê · O que se pode fazer ·
  Casos e testemunhos`.
- **Tema claro e escuro.** Define todos os tokens em `:root` e redefine só os
  que mudam em `@media (prefers-color-scheme: dark)` **e** em
  `:root[data-theme="dark"]`. O `body` tem de ter fundo explícito.
- **Sem `localStorage`** por agora.
- **Largura:** conteúdo com `max-width` de 72 ch para texto; figuras a toda a
  largura com `overflow-x: auto` no seu próprio contentor. O corpo da página
  nunca faz scroll horizontal.
- **Cada figura tem, por baixo, uma linha de proveniência** igual à do
  rodapé da figura, e um `<details>` com «como foi calculado».

---

## 8. CONTROLO DE NÚMEROS E VERIFICAÇÃO — O PORTÃO

Este processo já teve máscaras circulares, um erro de escala de 30 %, uma
detecção térmica retirada e organismos de um caso externo a entrar no
registo. Nenhuma figura sai sem passar isto.

### 8.1 `NUMEROS_USADOS.csv` — obrigatório
Uma linha por **cada número impresso em cada figura**. Colunas exactas:
```
figura,elemento,valor_impresso,unidade,ficheiro_fonte,coluna_ou_linha,script,estado_evidencia,nota
```
Se um número não tiver ficheiro de origem, **não vai para a figura**. O
«44,9 ha» é o caso conhecido: existe só em prosa e não tem script — ou lhe
encontras fonte, ou sai, ou vai com etiqueta POR TESTAR.

### 8.2 `PROVENIENCIA.csv`
```
figura,ficheiro_dados,mtime_original,bytes_original,script,data_geracao,instrumento,estado
```

### 8.3 Rastreio de contaminação — correr e registar o resultado
`grep -ri` em **todos** os ficheiros de `_apresentacao\` (incluindo SVG e
scripts) por: `Dactylonectria`, `Ilyonectria`, `Rhizoctonia solani`,
`Kiwi Atlántico`, `240/2023`. São de um caso externo. Zero ocorrências, ou
ocorrência explicitamente rotulada «caso externo, não é Ganfei».
Segundo rastreio: `B3/C3` e `mesmo bloco` — a atribuição da válvula 27 é
**testemunho da gestora**, não metadado da plataforma (a Becrop não tem
parcela associada). Onde aparecer, tem de ler «atribuição da gestora;
plataforma sem parcela; confirmação pedida».

### 8.4 Checklist antes de declarar uma figura pronta
1. **Acentos.** `grep -c "ã\|ç\|é\|í\|ó\|ú\|â\|ê\|õ"` no SVG > 0, e
   inspecção visual do PNG. A F8 falha isto hoje.
2. **Colisões.** Renderiza no tamanho final e **olha para a figura**. A
   regra dos 3 mm de §3.8. A F14 falha isto hoje.
3. **Cinzentos.** Converte para escala de cinzentos e confirma que todas as
   categorias continuam distinguíveis. Se não, falta trama ou forma.
4. **Daltonismo.** Simula protanopia e deuteranopia. As três cores de
   identidade passam; qualquer cor que tenhas acrescentado tem de ser testada.
5. **Um eixo.** Nenhuma figura com dois eixos verticais.
6. **Cor nunca sozinha.** Todo o estado tem glifo + palavra.
7. **Rodapé de proveniência** com os quatro campos de §3.9.
8. **Números suspensos.** Nenhuma área derivada das máscaras antigas sem
   tarja SUSPENSO. Lista: 4,23 ha manchaW · 29,1 ha pomar · 11,5 ha défice ·
   84,3 % · decomposições do défice · percentis de cota por máscara.
9. **Contaminação** (§8.3) limpa.
10. **Reprodutibilidade.** Apaga o PNG e volta a correr o script. Tem de sair
    byte-a-byte igual (fixa `random_state` onde houver aleatoriedade).

---

## 9. O QUE ME DEVOLVES — `00_ENTREGA.md`

Escreve, por esta ordem:

**§1 · Mapeamento.** Tabela `A00..A11 → figura existente / NOVA / não se
aplica`, com uma linha de justificação por cada. Se discordares de algum
lugar da sequência, diz e propõe.

**§2 · Feito.** Lista do que ficou pronto, com caminho relativo.

**§3 · Não feito, e porquê.** Sem eufemismo.

**§4 · Desacordos.** Onde é que este memo está errado à luz dos ficheiros.
Tens os dados e eu não. Se uma instrução minha contradiz o que está no
disco, **o disco ganha** — regista o desacordo e segue o disco.

**§5 · Números que não passaram no portão.** Quais, e o que fizeste.

**§6 · Resultado do teste do L1** (A07): qual é a convenção angular do teu
`regionprops`, e depois de a resolver, há ou não alinhamento entre o eixo
maior do foco ocidental e o azimute do L1.

**§7 · O núcleo interno do lóbulo oeste** (§5): (a), (b) ou (c)?

**§8 · Verificações.** Os dez pontos de §8.4, um a um, com «passou» ou o que
falhou.

**§9 · Perguntas para mim.**

---

## 10. ORDEM DE EXECUÇÃO

Não faças tudo em paralelo. Esta ordem existe porque cada passo condiciona
o seguinte.

1. **Correcção dos acentos** em toda a `figuras\` (§2.4). Meia hora, e sem
   isto nada do resto é apresentável.
2. **`00_ENTREGA.md` §1** — o mapeamento. Antes de desenhar.
3. **A04** — as manchas emergem sozinhas. É a figura que fecha a
   circularidade e é a mais importante que falta.
4. **A05 + A06** — timelapse e o seu gémeo.
5. **A00** — a página do chefe. Só depois de A04 estar feita, porque os
   números-herói saem de lá.
6. **A11** (correcções à F14) e **A08** (adição do bloco RETIRADO à F13).
7. **A01, A02, A03, A07** — as correcções às figuras existentes.
8. **A10** — os critérios de refutação.
9. **A página** — última.

Se o tempo acabar a meio, para no ponto 6: A00 + A04 + A05/A06 + A08 + A11
já são uma apresentação defensável.

---

## 11. O QUE EU AINDA NÃO SEI, E QUE MUDA COISAS

Estas ficam em aberto — se souberes a resposta a alguma, aplica-a e diz-mo.

1. **Formato de impressão do conjunto legacy.** Assumi A3 horizontal como
   mestre + A4 vertical, e assumi que tem de sobreviver a fotocópia. Se D
   disser outra coisa, é a §2 que muda.
2. **Que decisão exacta se pede ao chefe** — verba, tempo de equipa, ou
   assinatura da proposta de isenção. Muda o bloco final da A00 e da A11.
3. **Há data de reunião?** Se houver, o `.mp4` narrado é prioritário; se não,
   a página chega.
4. **Nomear ou anonimizar** laboratórios, gestora e técnicos. A regra de
   testemunho (§3.6) exige nomear quem testemunhou — mas num documento que
   acompanha uma proposta ao INIAV isso tem consequências.
5. **A comparação regional** («1.054 ha de kiwi por 204 beneficiários; uma
   exploração a 8,1 km com sinal semelhante») está POR FAZER na F13. Se
   correr antes da apresentação, **passa a ser a A02 e empurra tudo** — é a
   única peça que responde à pergunta «este pomar declina, ou declina todo
   o kiwi neste aluvião?», e é a pergunta que um chefe faz primeiro.

---

**Fim do memo.** Qualquer coisa neste documento que colida com os ficheiros
no disco: o disco ganha, e regista o desacordo em `00_ENTREGA.md` §4.
