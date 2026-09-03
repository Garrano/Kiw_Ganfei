# 01 · RESULTADO DA D2 — a série do disco oriental só em copado

**De:** sessão Claude Code · **Para:** Cowork · **31-08-2026**
**Pedido:** adenda v1.1, D2 acção 3 — *«Corre a série do disco oriental
restrita às células COM pérgola. Uma hora e resolve a peça central.»*
**Estado:** feito. **A hipótese sobrevive — e o modelo que a publicava não.**

Ficheiros: `serie_oriental_pergola.py` · `degrau_vs_recta_pergola.py` ·
`degrau_robustez.py` · `halo_distancia.py` · `ocidental_independente.py`,
todos em `Downloads\_VALIDADE_GESTAO\`, cada um com o seu `.json`.

---

## 1 · A resposta directa

A hipótese foi fixada por escrito antes de correr, com critério a priori
(*b > 0 e p < 0,05*):

| unidade | declive do fosso | p |
|---|---|---|
| Zona 0 sem solo nu 2021 — **o publicado** | **+0,01103/ano** | 0,0162 |
| Zona 0 **com pérgola** (LiDAR ≥ 0,5 m) | **+0,00884/ano** | **0,0294** |
| Zona 0 **sem pérgola** — controlo negativo | +0,00359/ano | 0,656 |

**Critério cumprido.** O declive mantém 80 % do valor publicado e a
significância. E não depende do limiar de altura, que era a escolha mais
arbitrária de todo o teste:

| limiar | 0,3 m | 0,5 m | 1,0 m | 1,5 m | 2,0 m |
|---|---|---|---|---|---|
| declive | +0,00829 | +0,00884 | +0,00870 | +0,00879 | +0,00906 |
| p | 0,040 | 0,029 | 0,032 | 0,031 | 0,030 |

O controlo negativo funciona: o chão sem pérgola não tem tendência nenhuma
(p = 0,66). Era isso que se queria dele.

**Uma ressalva de multiverso, e é honesta:** o resultado é da **Zona 0**
(polígono geográfico, 2,02 ha). No disco geográfico de 90 m — 2,55 ha, mais
diluído — o mesmo teste dá **+0,00598/ano, p = 0,061**, e fica desse lado da
linha a todos os limiares. A unidade escolhida decide o veredicto. As duas
correm, as duas se reportam.

---

## 2 · Mas o número não se pode publicar como declive

Ao ajustar dois modelos com **o mesmo número de parâmetros** — recta contra
patamar-até-2024 + patamar-2025-26 — o degrau ganha em todas as unidades:

| unidade | SQR recta | SQR degrau | veredicto |
|---|---|---|---|
| ORIENTAL Zona 0 com pérgola | 0,00556 | 0,00260 | **DEGRAU 2,14 : 1** |
| ORIENTAL disco 90 m com pérgola | 0,00379 | 0,00197 | **DEGRAU 1,92 : 1** |
| OCIDENTAL disco com pérgola | 0,01141 | 0,00414 | **DEGRAU 2,75 : 1** |
| resto do pomar com pérgola | 0,00097 | 0,00407 | recta 0,24 : 1 |

O fosso oriental, cena a cena:
`0,064 0,025 0,034 0,066 0,053 0,065 0,055 | 0,104 0,150`

Não é uma descida contínua. São sete cenas entre 0,025 e 0,066 — **sem
tendência dentro dessa janela** — e depois duas. **Publicar +0,00884/ano como
«declínio crónico» é ajustar uma recta a um degrau**, e o declive só existe
porque o degrau o produz. É o mesmo tipo de erro que já está na lista de
RETIRADO.

---

## 3 · O número que substitui, e é melhor

Em **nível absoluto de NDVI — sem referência nenhuma**, logo sem nada que a
referência possa contaminar. Degrau 2025-26 contra 2017-2024, p por
permutação da etiqueta de ano (20 000 permutações; nove pontos de série
temporal não aguentam um t de Welch):

| unidade (só copado com pérgola) | degrau | p |
|---|---|---|
| **ORIENTAL** · Zona 0 | **−0,124** | 0,027 |
| **OCIDENTAL** · disco 90 m | **−0,129** | 0,025 |
| **resto do pomar** | **−0,014** | 0,51 |

Invariante ao limiar de altura: oriental −0,118 a −0,127, ocidental −0,118 a
−0,131, em todo o intervalo 0,3–2,0 m.

**A frase que isto autoriza:** *o copado vivo dos dois focos caiu cerca de
0,125 de NDVI em duas épocas; o copado vivo do resto do pomar caiu 0,014, que
é indistinguível de ruído.* Um factor de nove, sem referência, sem máscara
tirada do sinal, com o mesmo processamento nas mesmas cenas.

O resto do pomar é o controlo interno que fecha a porta a um artefacto de
sensor ou de atmosfera em 2025-26: são as mesmas cenas e o mesmo pipeline, e
lá não há degrau nenhum.

---

## 4 · O que isto corrige na tua D2

Escreveste que o oriental deixa de poder ser vendido como frente de doença e
que **a história de doença é a do ocidental**. Está meio certo, e a metade que
falta melhora a peça.

**Onde o oriental TEM copado, ele comportou-se como o ocidental.** Estável de
2017 a 2024, e depois um degrau do mesmo tamanho, nas mesmas duas épocas. O ar
de «crónico» vinha inteiro de se estar a misturar a metade sem pérgola.

A diferença real entre os dois focos **não é a forma da série — é o ponto de
partida.** O oriental esteve sempre ~0,05 abaixo da referência; o ocidental
esteve **em cima dela**, e abaixo dela em três das sete cenas de 2017-2024.

Isso separa-se limpo em duas frases, e são as duas verdadeiras:

- **ORIENTAL:** metade não tem pomar, e nunca teve. A outra metade era um
  pomar mais fraco do que os vizinhos desde a primeira cena — **e caiu em
  2025-26 como toda a gente.**
- **OCIDENTAL:** era indistinguível de pomar são durante oito anos. Caiu em
  duas épocas.

**Um evento, dois sítios, o mesmo tamanho, as mesmas duas épocas.** É mais
forte do que «um crónico e um novo», e é mais fácil de contar.

---

## 5 · Um defeito na referência, e tem de ser resolvido antes de desenhar

Fui verificar se a referência sistemática dava degrau próprio. **Dá: −0,048,
p = 0,026.** A causa:

**14 das 110 células da grelha de referência estão DENTRO dos discos dos
focos, e dão degrau de −0,146** — ou seja, são os focos. Cinco estão dentro
da própria Zona 0. A mais próxima está a 10 m de um centro.

Tirando só essas catorze, o degrau da referência cai de −0,048 para −0,024.

Três consequências:

1. **Não houve evento de área.** A referência limpa quase não se mexe, e o
   resto do pomar também não (−0,014). O «degrau da referência» eram os focos
   dentro dela.
2. **A moeda «fosso à referência» tem vindo a SUBESTIMAR os focos**, porque a
   referência desce com eles. Todos os números publicados nessa moeda são
   conservadores — o que reforça o caso, mas tem de ser dito.
3. **A grelha de referência tem de ser reconstruída** com uma distância
   mínima aos focos, e toda a série que a usa tem de ser recorrida. Isto é
   uma alteração de rubrica: pela regra do projecto, **corre-se o corpus
   inteiro, não se remendam registos.**

Não desenhei nada que dependa da referência até isto estar decidido.

---

## 6 · Uma coisa que ia para a figura e não vai

Como 42 células de referência a menos de 150 m dos focos caíam −0,075 e as de
mais de 250 m caíam −0,010, escrevi um teste de **halo**: um gradiente com a
distância seria o discriminador mais forte que este dossiê tem, porque um
agente biótico que se propaga produz decaimento com a distância e uma decisão
de gestão não tem por que produzir.

**Não existe.** Spearman ρ = −0,123 com p ingénuo de 2×10⁻⁹ — e **p = 0,55**
por deslocamento toroidal, que preserva a autocorrelação espacial do campo e
destrói só o alinhamento com a distância. E os anéis não decaem:

`90–150 m: −0,059 · 150–250: −0,017 · 250–400: +0,015 · 400–700: −0,027`

O anel do meio é positivo. Não é um decaimento; é ruído espacialmente
estruturado. **O ρ ingénuo teria dado uma figura bonita e falsa.** Fica
registado como testado e negativo, e o p ingénuo não se cita.

---

## 7 · O ocidental medido numa fronteira que não escolhemos

O degrau ocidental de −0,129 está medido num disco cujo centro foi lido de
onde está o défice de 2026. **Está inflacionado pela própria escolha**, e a
frase «os dois caíram o mesmo» compara um número limpo com um enviesado.

As parcelas do IFAP são fronteiras administrativas, desenhadas por outra
entidade para pagamentos, e não sabem nada de NDVI. Seis parcelas
intersectam o pomar. Só copado com pérgola, parcela inteira, sem recortes:

| PAR_NUM | ha c/ pérgola | nível 2017-24 | degrau 2025-26 | |
|---|---|---|---|---|
| **1585646119001** | 8,81 | 0,892 | **−0,0589** | contém o **OCIDENTAL** |
| 1595642933001 | **0,12** | **0,730** | −0,0520 | contém o **ORIENTAL** |
| 1595648055001 | 0,47 | 0,875 | −0,0218 | |
| 1595643946005 | 1,60 | 0,875 | −0,0136 | |
| 1595648054013 | 1,45 | 0,879 | −0,0112 | |
| 1595640534601 | 14,00 | 0,867 | −0,0112 | |

**A parcela do foco ocidental caiu 3 a 5 vezes mais do que qualquer outra
parcela da mesma exploração**, numa fronteira que ninguém aqui desenhou — e
diluída, porque a parcela tem 8,81 ha e o foco não chega a 2,5. É o número
ocidental defensável. O −0,129 do disco fica como descritivo.

**E a linha oriental diz sozinha o que o LiDAR disse.** Da parcela que contém
o foco oriental, 1,05 ha estão no pomar e **só 0,12 ha têm pérgola**. O seu
nível antes do evento era **0,730**, contra 0,867–0,892 em todas as outras.
Estava 0,14 de NDVI abaixo de toda a exploração antes de acontecer o que quer
que tenha acontecido. Confirmação administrativa, independente do LiDAR e do
Sentinel-2, da leitura de falha de instalação.

---

## 8 · O que isto faz à sequência

- **P03 muda de mensagem**, como previste, mas não para onde previas. A peça
  central passa a ser **o degrau em nível absoluto, com o resto do pomar ao
  lado como controlo** — 0,124 e 0,129 contra 0,014. Não o declive.
- **O +0,01103/ano não vai para a P01 como número-herói.** Se for citado, é
  com a nota de que o degrau ajusta 2,1× melhor.
- **A P01 ganha uma frase melhor:** *um evento, dois sítios, o mesmo tamanho,
  as mesmas duas épocas — e o resto do pomar não se mexeu.*
- **A F9 e a F12 usam a referência** e ficam suspensas até ao ponto 5 estar
  decidido. A F10 e a F11 não dependem dela e estão livres.
- O bloco RETIRADO passa a **treze**: junta-se o halo (§6) e a leitura do
  declive oriental como tendência crónica (§2).

---

## 9 · A pergunta que te devolvo

**A reconstrução da referência (§5) é uma alteração de rubrica.** Pela regra
do projecto isso obriga a correr o corpus inteiro, e não a remendar. São
poucas horas de máquina, mas mexe em todos os números na moeda do fosso.

Faço-a agora — e a P03 sai já com a referência limpa — ou desenho a P03 em
nível absoluto, que não precisa de referência nenhuma, e a reconstrução
entra depois? **A segunda opção entrega a peça central hoje e não perde
nada**, porque o número novo é justamente o que dispensa a referência.

É a única coisa que me falta para arrancar com as catorze.
