# Observações — julgamento sobre máscaras, datas e método

Baseado exclusivamente nos dados em `dados/`, nos quadros que produzi e nas
figuras em `figuras/` (F1: NDVI + máscaras nas 11 datas; F2: mapas de défice;
F3: zoom 2024/2026; F4: média pré-2025 vs 2025–26 e diferença; F5: bloco b1;
F6: cota vs NDVI). Números de apoio em `codigo/diagnostico.log`. Não comento
causas.

## 1. Máscaras mal colocadas ou arbitrárias

**manchaW (425 px, 4,25 ha) foi desenhada sobre o estado final.** O polígono
segue de perto a mancha pálida de 2026-07-27 (F3): a maior componente de
défice moderado do pomar nessa data tem 406 px e 364 deles caem dentro de
manchaW; 56 px do polígono (13 %) não estão em défice em 2026 (NDVI médio
0,865, essencialmente a orla). Consequência para o Quadro 2: a "área em
défice em manchaW" está limitada por cima pelo próprio polígono (86,8 % em
2026) e a "datação" mede quando o défice apareceu *dentro de uma forma
escolhida a posteriori*. É a máscara mais circular do conjunto. O valor de
2017 (27 % em défice) está contaminado pela qualidade dessa imagem (ver §2), e
2018-08-31 (25 %) é a única outra data pré-2025 com défice relevante — as
datas seguintes têm 1–8 %.

**zona0 (221 px) não é um foco que "apareceu": está em défice em todas as
datas.** 52 % em 2017, 39–71 % entre 2018 e 2024, 96–100 % em 2025–26. A mancha
pálida é visível em F1 desde 2017. O polígono acompanha a mancha, mas a sua
aresta leste (colunas 113–115) coincide com a aresta do pomar/caminho, e há
uma faixa a NE (linhas 30–45, colunas 113–125, 62 px de pomar) com 19–30 px em
défice em todas as datas e que não pertence a máscara nenhuma. Se zona0 é a
"zona zero", a sua fronteira NE é arbitrária.

**A referência sã captura o que se pretende, mas com um risco.** As três
máscaras são internamente homogéneas (dp 0,003–0,03 na maioria das datas) e as
médias dos três polígonos diferem entre si por ≤0,02 excepto em 2017 e
2020/2025-06 (saudavel_3). `saudavel_2` é uma tira de 6 pixels de altura, a
5 px de zona0. `saudavel_3` (73 px) está no lóbulo NE, encostada às duas
maiores componentes de défice de 2026 fora dos focos (111 px nas linhas 21–35 /
colunas 125–138 e 62 px nas linhas 14–25 / colunas 142–153; F4 mostra o lóbulo
inteiro a escurecer). Tem 4 px em défice em 2026 e a maior dispersão interna
das três. Se esse lóbulo continuar a descer, a referência desce com ele e
esconde défice — a `ref` ainda está estável (0,883–0,920 desde 2018), mas é
para aqui que se deve olhar.

**pomar inclui estrutura que não é copado.** Em anos "bons" (2019–2024) o pomar
tem 17–22 % de pixels abaixo de ref−0,05: caminhos, orlas e as faixas
transversais do lóbulo NE (visíveis em todas as datas de F1). Esse fundo
estrutural não é défice sanitário e não está descontado em Q1. Em 2026, **50 %
do défice moderado do pomar (585 de 1172 px) e 46 % do severo (416 de 905 px)
estão fora de manchaW ∪ zona0** — as duas máscaras de foco explicam metade do
sinal.

**Detalhe geométrico que torna todas as máscaras frágeis:** os vértices em
coordenadas .5 fazem as arestas passar exactamente por centros de pixel na
convenção +0,5 (AMBIGUIDADES A1/A2). Duas ferramentas de rasterização dão
zona0 com 221 ou 207 pixels sem mudar nada no ficheiro.

## 2. Datas a excluir ou a sinalizar

| data | evidência | recomendação |
|---|---|---|
| **2017-07-02** | 36 NaN (máscara de nuvem) a leste; 358 px do pomar com NDVI < 0,5 (as outras datas: 3–128); p10 do pomar 0,48 vs 0,56–0,79; dp da referência 0,103 (5× as restantes); `saudavel` com 41 px < 0,75 (linhas 48–55, colunas 72–84) e média 0,815; correlação com a mediana temporal 0,88. Compatível com neblina/sombra próxima da nuvem mascarada. | **Excluir** ou, no mínimo, não usar como ponto de partida da série. É a origem do "27 % de manchaW em défice em 2017" e do "29 % do pomar". |
| **2025-06-17** | Única data de Junho (as outras: 16 Jul–2 Set); p10 do pomar 0,56; 226 px < 0,5; correlação com a mediana temporal 0,836 (a mais baixa). Aparece em último no `cenas.json`, fora de ordem cronológica — foi acrescentada depois. | Sinalizar como não comparável fenologicamente; os 96 % de zona0 nesta data não devem ser lidos como tendência. |
| 2018-08-31, 2019-09-02 | Fim de estação vs Julho nas restantes; `ref` mais alta (0,888/0,904) e manchaW oscila 25 % → 3 % entre elas. | Manter, mas a variação 2017→2019 em manchaW é essencialmente calendário + qualidade, não sinal. |
| Landsat 2021 | 7 cenas no ano, 6 válidas; 2020: 7 válidas. | As médias anuais de 2020–2021 são as mais frágeis (ver AMBIGUIDADES C1: 2021 vai de +0,27 a −0,50 °C só com a leitura dos bits). |
| Landsat Abril | NDVI 0,3–0,5 na referência (copado ausente); entram nas médias anuais com o mesmo peso que Julho. | Reportar as médias anuais também sem Abril, ou por mês. |

## 3. A decisão do método mais frágil

**A regressão cota~NDVI do Quadro 4.** Três razões, todas medidas:

1. O domínio não está definido e **inverte o sinal**: no pomar, declive −0,048
   NDVI/m, r = −0,28; em toda a AOI, +0,036 e r = +0,33. A "diferença
   observado−previsto" de manchaW passa de −0,105 para +0,314.
2. Mesmo no pomar, a relação é fraca (r² = 0,08) e é produzida pelo lóbulo NE
   (cotas 7,5–8,7 m com faixas de baixo NDVI) contra o corpo principal
   saturado a 0,90 (F6). A amplitude de cotas do pomar é 6–8,7 m; o declive
   está a ser fixado por estrutura de plantação, não por relevo.
3. A conclusão que dela se extrai ("os focos estão abaixo do previsto para a
   cota") depende de dois números de 2026 (−0,105 e −0,126) cuja incerteza
   ninguém reportou.

Logo a seguir, em fragilidade: a leitura dos bits de `qa_pixel` (C1), que
decide se 2021 aqueceu ou arrefeceu e se r de Q3b é −0,77 ou −0,44; e o
limiar absoluto `ref − 0,05`, com `ref` a variar 0,02–0,03 entre anos
(0,883–0,920 desde 2018) — metade do limiar é ruído de referência.

## 4. O número em que apostaria que muda no terreno

**Quadro 2, 2026-07-27, manchaW: maior componente 3,65 ha, 86,8 % da máscara,
alongamento 1,38, orientação 167°.** Porque:

- é uma área medida dentro de um polígono desenhado sobre a própria mancha —
  no terreno o limite do foco não vai coincidir com o traço; a componente de
  défice do pomar tem 4,06 ha e continua para fora do polígono a oeste
  (linhas 42–45, colunas 50–55 e linhas 33–36, colunas 68–76 já têm défice
  severo fora da máscara);
- a orientação e o alongamento são de uma forma recortada pela máscara, não da
  mancha;
- e metade do défice de 2026 do pomar está fora das duas máscaras, portanto
  quem for verificar vai encontrar plantas afectadas onde os quadros dizem
  "sem foco".

Segunda aposta: zona0 a "100 %/2,21 ha" — no terreno é uma zona com défice
desde 2017 e um limite NE arbitrário, e o número que se vai discutir é a área
real, não a percentagem de um polígono que já está saturado.
