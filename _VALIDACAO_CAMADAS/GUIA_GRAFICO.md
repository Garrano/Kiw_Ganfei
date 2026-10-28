# GUIA GRÁFICO

**O que uma peça pode dizer, e como o diz.** Vale para cartas, pranchas,
infografia, documentos e interfaces — tudo o que sai daqui com informação
desenhada.

Está escrito em duas camadas, e a separação é deliberada:

- **O MÉTODO** é invariante. Não depende deste caso, desta marca, nem desta
  ferramenta. É a parte que se leva para outro projecto inteira.
- **OS PARÂMETROS** são deste caso — cinco cores, duas famílias de letra, uma
  rampa de cota. Trocam-se por outros sem tocar no método.

Nada aqui é gosto. Cada regra existe porque uma peça falhou por não a ter, e a
falha está nomeada ao lado. A proveniência académica está no fim.

---

# PARTE I · O MÉTODO

## 1 · Uma peça enuncia; não interroga

**A pergunta vive no corpo da mensagem. A peça serve-a tornando-a mais clara, e
não funciona sozinha.**

Nenhuma pergunta escrita na prancha, no slide, no painel. Quando a peça tem
mesmo de colher uma resposta, o dispositivo é **forma, não frase**: uma caixa
vazia junto de um rótulo, um campo por preencher, uma célula em branco.

Excepção, e é uma convenção centenária em geologia e arqueologia: o **rótulo
interrogado** — `N?` em itálico — não é pergunta, é a notação de **atributo
inferido**. Distingue-se pela forma: uma frase que *fecha* em `?` interroga; um
`?` colado a um rótulo curto qualifica.

> *Falhou assim:* a prancha levava sete perguntas numa caixa. Eram lacunas
> **nossas** anotadas no documento que ia para o destinatário.

## 2 · Título nominal e institucional

`<ORGANIZAÇÃO> · <sintagma nominal>`. Um título é uma **designação**, não uma
fala, não uma conclusão, não um achado.

«GANFEI · ESQUEMA DE REGA» — sim.
«O que a rega nos diz sobre o declínio» — não.

## 3 · Nada do nosso processo na peça

Nem método, nem ressalva, nem estatuto de validação, nem vocabulário interno.
Quem recebe não trabalha aqui.

**A derivação não é processo.** Dizer de que instrumento e de que datas vem uma
classe é obrigação da peça — e vai em **língua corrente**, nunca em jargão
nosso: «obtida por altura de copado medida por altimetria aérea, cruzada com
imagem de satélite», e não «MDS−MDT + NDVI S2 L2A».

Onde é que o método vai, então: num **ficheiro companheiro**, um resumo por
peça. A peça mostra; o companheiro explica. Ver §12.

## 4 · FONTES declaradas, em estilo próprio

É o que separa uma carta de uma figura. Instrumento, entidade, data, escala.
Em registo tipográfico distinto do corpo (§8) — lê-se como nota de rodapé, não
como mais um rótulo a competir com o conteúdo.

## 5 · Sem deixis. Registo impessoal e nominal

Nenhuma primeira nem segunda pessoa no texto desenhado. **Uma legenda nomeia o
fenómeno, nunca a relação do autor com ele.**

«o talhão por que perguntamos» · «na posição que temos» · «as que nos indicou»
— todas erradas pela mesma razão: põem o autor dentro da legenda.

## 6 · Nenhuma classe nomeada por contraste

«as outras válvulas», «os restantes sectores», «demais casos». **Uma entrada de
legenda define-se pelo que É.**

E há uma razão mecânica, não só estilística: **um termo relativo sobrevive à
remoção do seu contraste sem dar erro nenhum.**

> *Falhou assim:* removi a classe destacada e o «outras» ficou na legenda, a
> apontar para nada. Nenhuma ferramenta deu erro.

## 7 · A anotação é para NOMES e VALORES; a identidade de classe é da legenda

Sobre o mapa, sobre o gráfico, sobre a planta: **topónimos, códigos, medidas.**
Nomes próprios e números.

A identidade de classe pertence à legenda. Anotar «o talhão em causa» por cima
da feição **duplica a legenda e desalinha-se dela na primeira edição**.

*Heurística que uma máquina consegue aplicar:* uma anotação no eixo do desenho
que começa por minúscula e tem duas ou mais palavras é descrição, não nome.

## 8 · Só os nomes de quem recebe

Uma peça designa as coisas pelos nomes que o destinatário usa todos os dias —
nunca pela taxonomia analítica que nós inventámos para trabalhar.

«Talhão a nascente» não quer dizer nada a quem tem os talhões com nome.

E pior do que inventar é **reaproveitar**: um termo do destinatário aplicado por
nós a outro referente contradi-lo sem o dizer.

> *Falhou assim:* «Zona 0» é uma palavra do gestor — ele escreveu que são as
> válvulas 8, 9 e 10 — e a prancha imprimia-a sobre outro bloco.

## 9 · Toda a série parcialmente representada declara o intervalo

«válvulas de rega, **6 a 17**». Sem isso, a ausência das 1 a 5 lê-se como
inexistência.

É a regra que nenhuma verificação automática apanha e que **Monmonier** trata
como a forma mais comum de mentir com um mapa: a omissão silenciosa.

## 10 · O canal de proveniência — a regra que mais rende

**Reserve-se uma variável visual, sempre activa, para dizer de onde vem cada
coisa. Essa variável nunca transporta dados.**

Na prática, duas classes e nada mais:

| | significa |
|---|---|
| **traço contínuo, opaco** | está escrito numa fonte — documento, cadastro, registo, ou dito pelo destinatário |
| **traço interrompido, 55 %** | é nosso: inferência, partição, leitura por confirmar |

Porque é que isto é o mais importante do guia: **metade do que uma peça destas
costuma afirmar não tem fonte, e sem esta distinção o leitor não consegue saber
qual metade.** Com ela, a peça serve de documento de trabalho — leva-se ao
destinatário e ele corrige o que está a tracejado.

Generaliza para lá do mapa sem mudar nada:

- **documento** — texto corrido para o que tem fonte; itálico ou fundo ténue
  para o que é nosso, com a legenda da convenção na primeira página;
- **interface** — borda sólida contra borda tracejada, e um `title` que diz
  qual é qual; nunca cor, que já está ocupada;
- **tabela** — uma coluna `fonte` que nunca fica vazia.

## 11 · Correspondência legenda ↔ desenho, por instanciação

Cada classe declarada na legenda tem de ter **ocorrências no desenho**, e cada
símbolo no desenho tem de estar na legenda. Nos dois sentidos.

É o que a ISO 19117 formaliza. Não é automático: uma classe fica na legenda
depois de os seus dados terem sido filtrados, e nada se queixa.

## 12 · O ficheiro companheiro

Um resumo por peça, fora dela. Três secções fixas:

- **o que mostra** — em língua corrente;
- **com que instrumento** — proveniência, datas, resolução;
- **o que NÃO se conclui daqui** — a secção que falta em toda a parte e é a que
  impede a peça de ser citada a mais.

Aqui vive tudo o que a §3 expulsou da prancha: método, critérios, desvios,
ressalvas, o que falhou.

---

# PARTE II · TIPOGRAFIA

## 13 · Dois registos, e só dois

| registo | família | papel |
|---|---|---|
| **corpo** | grotesca humanista (DejaVu Sans, Inter, Source Sans) | títulos, rótulos, legendas, eixos — tudo o que é conteúdo |
| **marginália** | serifa humanista **em itálico** (Palatino, Constantia, Charter) | fontes, proveniência, notas de edição |

A serifa itálica na marginália **muda o registo de leitura**: a proveniência
passa a ler-se como nota de rodapé em vez de competir com os rótulos do
conteúdo. É convenção da cartografia impressa desde Zapf, e resolve sozinha um
problema que nenhum ajuste de tamanho resolve.

## 14 · Escala tipográfica

Hierarquia por **papel**, não por gosto. Valores para uma prancha de 16″ a
200 dpi; escalar proporcionalmente.

| elemento | corpo | peso |
|---|---|---|
| título | 21 | bold |
| subtítulo / cartela | 10,5 | normal |
| rótulo de feição principal | 13 | bold |
| entrada de legenda | 8,4 | normal |
| sub-entrada de legenda | 6,9 | normal |
| cabeçalho de secção da legenda | 7,6 | bold, VERSALETE |
| número dentro de símbolo | 8,6 | bold |
| coordenadas, escala | 6,8 | normal |
| **marginália** | **7,0** | **itálico, serifa** |

**Piso de legibilidade: 6,2.** Abaixo disto não se encolhe — corta-se conteúdo
ou aumenta-se a peça.

## 15 · Texto sobre imagem leva halo, nunca caixa

`path_effects.withStroke(linewidth=3, foreground=<papel>)`. Uma caixa opaca
abre um buraco no desenho; o halo deixa o terreno ler-se por baixo.

## 16 · O símbolo da legenda não se desenha com uma forma geométrica

**Um `Circle` em coordenadas de eixo estica-se** quando o painel é estreito e
alto — sai uma gota. Usar um **marcador** (`plot(..., marker="o")`), que é
invariante à proporção do eixo.

> *Falhou assim:* os cinco símbolos da legenda saíram em forma de lágrima, e
> ninguém reparou durante quatro revisões.

---

# PARTE III · COR

## 17 · A cor é um recurso escasso e pertence aos dados

O fundo — relevo, sombreado, base, *chrome* da interface — vai **dessaturado de
propósito**. Cinzentos, tons de terra, neutros. A cor saturada fica reservada
para o que o leitor tem de distinguir.

Quando o fundo compete, não se corrige escurecendo os dados: **dessatura-se o
fundo.**

> *Falhou assim:* o azul do rio competia com o azul de um sector que lhe ficava
> ao lado. A correcção foi tirar saturação ao rio, não mudar o sector.

## 18 · Quatro usos, e cada um tem uma regra

| uso | regra |
|---|---|
| **identidade** (categorias) | matizes atribuídos por ordem fixa, **nunca cíclicos**. A 9.ª categoria não é um matiz novo: agrega-se em «Outros», faz-se pequenos múltiplos, ou codifica-se em dois canais |
| **magnitude** | **um só matiz**, claro → escuro |
| **polaridade** | dois matizes + **cinzento neutro** ao meio. Nunca um matiz no meio |
| **estado** (bom/aviso/grave/crítico) | paleta reservada, nunca reutilizada para «categoria 4», e sempre acompanhada de ícone e rótulo |

**Nunca arco-íris. Nunca dois eixos verticais num gráfico.**

## 19 · Validar é um comando, não um juízo

```bash
node <skill>/dataviz/scripts/validate_palette.js "#0072B2,#D55E00,#009E73,#7E4E9B,#E69F00" --mode light
```

Verifica banda de luminosidade, piso de croma, **separação para daltonismo**
entre pares adjacentes, piso de visão normal, e contraste contra o fundo.

**Não se avalia uma paleta a olho.** Alvo ΔE ≥ 8 (OKLab ×100); 6–8 só é legal
com codificação secundária — rótulo directo, afastamento, textura.

E a codificação secundária só conta se as classes forem **espacialmente
separadas**: duas classes vizinhas no desenho com ΔE 7 não passam, por muito
rótulo que levem.

## 20 · Identidade nunca por rank

A cor segue a **entidade**, não a posição. Um filtro que muda o número de séries
não pode repintar as que sobram.

## 21 · Texto veste cor de texto

Valores, rótulos e legendas ficam nos tons de tinta — nunca na cor da série. Um
quadrado colorido ao lado transporta a identidade.

---

# PARTE IV · COMPOSIÇÃO

## 22 · Mobiliário obrigatório numa carta

Projecção declarada · quadrícula com passo nomeado · escala gráfica com
subdivisões · norte · topónimos · fontes.

Sem projecção declarada não é uma carta, é um desenho.

## 23 · Rótulo no ponto mais interior, não no centróide

O centróide de uma forma estreita ou côncava cai fora dela, ou em cima do
bordo. Usar o **pólo de inacessibilidade** — o ponto mais distante da fronteira:

```python
dt = ndimage.distance_transform_edt(mascara)
iy, ix = np.unravel_index(np.argmax(dt), dt.shape)
```

E para formas estreitas, quebrar o nome em duas linhas em vez de o deixar
transbordar para a classe do lado — onde se lê como se fosse dela.

## 24 · Crachás e etiquetas afastam-se da feição, com tirante

Cinco etiquetas postas nos respectivos centróides numa faixa estreita
atropelam-se todas. Deslocam-se para o espaço vazio **do mesmo lado**, cada uma
com um tirante fino até ao seu ponto de ancoragem.

Escolher o lado olhando para o espaço disponível — não alternar por regra.

## 25 · Camadas registadas, e o registo verifica-se

Quando uma peça se sobrepõe a outra, as duas saem **da mesma geometria e do
mesmo módulo**: mesma projecção, mesma caixa, mesma figura, mesmos eixos. A
camada de cima leva fundo transparente.

Verificar compondo as duas e olhando — não assumindo:

```python
assert base.size == camada.size
Image.alpha_composite(base, camada).save("_composto.png")
```

## 26 · Duas peças nunca dizem coisas diferentes

Se a camada diz que uma posição não está resolvida, a base **não a pode
desenhar**. Duas peças em contradição valem menos do que qualquer uma delas.

É a verificação que só aparece quando se compõem as duas — e por isso §25 não é
opcional.

---

# PARTE V · O QUE SE VERIFICA E O QUE SE OLHA

## 27 · Executável

```bash
python _VALIDACAO_CAMADAS/cartas.py        # as oito condições da Parte I
node  <skill>/dataviz/scripts/validate_palette.js "<hex,...>" --mode light
```

A `cartas.py` lê o texto **desenhado** por `ast` — só o que entra em `.text()` e
`.annotate()` — para que um comentário possa explicar a regra sem a violar. Tem
bateria própria (`--auto-teste`) e corre no gancho de fim de turno.

## 28 · O que nenhuma das duas vê — e tem de ser olhado

Corpo pequeno de mais · sobreposição · rótulo cortado · transbordo para a classe
vizinha · símbolo deformado · **correspondência legenda↔desenho por
instanciação** (§11) · a série parcial sem intervalo declarado (§9).

**A peça tem de ser aberta depois de gerada, e a legenda lida contra o que
aparece.** Não há atalho.

> *Porque está escrito como ordem e não como conselho:* a regra foi-me dada por
> escrito, corrigi uma prancha, repeti a mesma falta na seguinte, escrevi a
> verificação — e na prancha a seguir falhei por outras três vias, todas
> elementares.

---

# PARTE VI · OS PARÂMETROS DESTE CASO

Trocar estes valores é todo o trabalho de adaptação. O método acima não muda.

## 29 · Tintas e papel

```python
PAPEL  = "#FBFAF7"   # fundo quente, não branco puro
TINTA  = "#1F1D1A"   # texto principal
TINTA2 = "#5C574F"   # secundário, molduras
TINTA3 = "#8A8378"   # terciário, coordenadas, marginália
```

## 30 · Paleta de identidade — cinco classes, validada

```python
COR = {"B1": "#0072B2", "B2": "#D55E00", "Erica Novo": "#009E73",
       "B3": "#7E4E9B", "B4": "#E69F00"}
```

Pior par adjacente ΔE **11,0** (deutan), 25,8 (visão normal). Passa todas as
verificações excepto um aviso de contraste no `#E69F00`, coberto por rótulo
directo.

Derivada de Okabe–Ito, com o magenta original `#CC79A7` **substituído** por
`#7E4E9B` porque dava ΔE 7,6 contra o verde — e essas duas classes são vizinhas
no terreno, o que impede a excepção da codificação secundária (§19).

## 31 · Letra

```python
"font.family": "DejaVu Sans"                      # corpo
MARGINALIA = dict(family="Palatino Linotype",     # fontes e proveniência
                  fontsize=7.0, style="italic", linespacing=1.62)
```

## 32 · Terreno

```python
AGUA = "#5E93AE"
CURVA, CURVA_ALTA = "#A79C88", "#B2977A"
RAMPA = [(0, "#C4CED2"), (2.5, "#DBDFDE"), (4, "#E7E7DC"), (7, "#F0EEE2"),
         (10, "#E9E2CD"), (20, "#DCCFB2"), (50, "#C6B290"),
         (100, "#AD9170"), (160, "#8E7050")]
```

Rampa **não linear**: fina onde está o objecto de estudo (4–10 m), comprimida na
encosta. Uma rampa linear sobre 0–155 m achatava os 2 m de relevo que importam.

Sombreado **multidireccional** (225°, 270°, 315°, 360°): um só azimute inventa
lombas onde o terreno é plano, e 33 % das células deste terreno são planas.

## 33 · Proveniência

```python
CONFIRMADO = dict(linestyle="-",          alpha=1.00)
POR_CONF   = dict(linestyle=(0, (5, 3)),  alpha=0.55)
```

---

# PARTE VII · LEVAR PARA OUTRO SÍTIO

## 34 · Para um documento

§1–§12 aplicam-se sem alteração. A marginália (§13) passa a nota de rodapé em
serifa itálica. O canal de proveniência (§10) passa a itálico ou fundo ténue,
com a convenção declarada à cabeça. O ficheiro companheiro (§12) passa a anexo
metodológico.

## 35 · Para uma interface

Tokens equivalentes, prontos a colar:

```css
:root {
  --papel: #FBFAF7;  --tinta: #1F1D1A;
  --tinta-2: #5C574F; --tinta-3: #8A8378;

  --fonte-corpo: "Inter", "Source Sans 3", system-ui, sans-serif;
  --fonte-margem: "Charter", "Palatino Linotype", Georgia, serif;

  --c-1: #0072B2; --c-2: #D55E00; --c-3: #009E73;
  --c-4: #7E4E9B; --c-5: #E69F00;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --papel: #16150F; --tinta: #F2EFE6;
    --tinta-2: #B9B2A4; --tinta-3: #8A8378;
  }
}
/* §10 — o canal de proveniência. Nunca transporta dados. */
.de-fonte    { border: 1px solid currentColor; opacity: 1; }
.nosso       { border: 1px dashed currentColor; opacity: .55; }
.margem      { font-family: var(--fonte-margem); font-style: italic;
               font-size: .82rem; line-height: 1.62; color: var(--tinta-3); }
```

**O modo escuro escolhe-se, não se inverte.** Os passos da rampa derivam-se
outra vez e validam-se contra a superfície escura (§19, `--mode dark`).

## 36 · Para um domínio novo

Preencher só esta tabela:

| parâmetro | o que fornecer |
|---|---|
| tintas e papel | claro e escuro |
| paleta de identidade | ordem fixa, validada pelo script |
| matiz sequencial | um só, para magnitude |
| par divergente | dois pólos + neutro |
| paleta de estado | distinta da de identidade |
| duas famílias de letra | corpo e marginália |
| canal de proveniência | duas classes, numa variável não usada por dados |

---

# PROVENIÊNCIA

Não é gosto — é literatura estabelecida:

- **Bertin**, *Sémiologie graphique* (1967) — variáveis visuais, e porque é que
  cada uma serve um tipo de dado e não outro.
- **Imhof**, *Positioning Names on Maps*, The American Cartographer 2(2), 1975
  — a anotação como nome e não como descrição (§7), e a colocação de rótulos.
- **Robinson et al.**, *Elements of Cartography*; **Brewer**, *Designing Better
  Maps* — construção de legenda, hierarquia, figura-fundo.
- **ISO 19117** (*Geographic information — Portrayal*) — correspondência
  classe↔símbolo (§11).
- **Monmonier**, *How to Lie with Maps* — a omissão silenciosa de parte de uma
  série (§9).
- **Okabe & Ito**, *Color Universal Design* — a paleta de origem (§30).
