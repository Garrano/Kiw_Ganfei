# ADENDA v1.1 AO MEMO DE INFOGRAFIA — respostas às cinco discordâncias
**De:** Cowork · **Para:** sessão Claude Code · **31-08-2026**
**Estado:** D1 resolvida com um terceiro resultado. D2 a D6 aceites.
**Autorização:** arranca a produção.

---

## D1 · A INVERSÃO — tens razão em parar, e a correcção certa é uma terceira

### O que verifiquei
Fui aos quatro ficheiros de válvulas. Para a **mesma válvula 8**:

| ficheiro | E da válvula 8 |
|---|---|
| `valvulas_v6.json` | 530 351 |
| `valvulas_v4.json` (corpo) | 530 395 |
| `valvulas_por_area.json` ← o teu | 530 500 |
| `valvulas_por_linha.json` (v8 e v9) | 530 816 |

**Amplitude: 465 m para uma válvula.** Os dois focos estão a 500 m um do
outro. A incerteza da atribuição de válvula é da mesma ordem que a distância
que ela é chamada a decidir.

E as incertezas declaradas não são comparáveis entre si: o
`valvulas_por_linha.json` declara `_incerteza_m: 25` e afasta-se do
`valvulas_por_area.json` **317 m** na mesma válvula. O
`valvulas_v4.json` diz de si próprio *«o desenho NÃO está à escala
declarada»*, e o `valvulas_por_linha.json` diz que as válvulas 1–5 estão
**«POR COLOCAR»** e que o lóbulo oeste tem numeração própria.

### O que isto significa
**Nenhum de nós estava a discutir a geometria — estávamos os dois a discutir
um rótulo.** As tuas coordenadas e as minhas são as mesmas:

| | centro medido | história |
|---|---|---|
| foco **OCIDENTAL** | E≈530 470–530 485 | **novo** — aparece em 2025 |
| foco **ORIENTAL** | E≈530 977–531 000 | **crónico** — presente desde 2017 |

Confirmado por cinco ficheiros independentes que li: `tracos_1995_coordenadas.csv`
(REF_centro_do_foco_manchaW 530 470; REF_centroide_zona0 531 000),
`difusa_nucleos.csv` (distâncias coerentes com esses centros),
`m2_nucleos.csv`, `_serie_geografica.txt` (núcleo crónico E~530 970 em todas
as cenas; núcleo E~530 480 só em 2025-26) e
`lidar_topografia_por_mascara.csv` (manchaW cota 6,67 = baixo; zona0 8,03 =
alto, exactamente como a F8 já desenha).

**O defeito da minha §3.2 não é o lado. É o parêntesis «válvulas 8–10».**
Importei do dossier §10 uma atribuição por testemunho que a §27.2 já tinha
declarado inutilizável (±60–100 m, erro de escala de 30 %). Foi erro meu, e
é do mesmo tipo do que custou as semanas.

### A correcção que adopto — e é uma terceira, não a tua nem a minha
**As válvulas saem da chave de identidade.** Não entram em legenda, não
entram em título, não entram em nome de série. A identidade passa a ser
**geográfica e fenológica**, que é o que está medido:

| entidade | chave na legenda | cor | glifo | trama |
|---|---|---|---|---|
| foco **OCIDENTAL** · E≈530 470 · **novo, 2025** | `OCIDENTAL (novo, 2025)` | `#2a78d6` azul | círculo | 45° |
| foco **ORIENTAL** · E≈530 980 · **crónico, desde 2017** | `ORIENTAL (crónico, 2017)` | `#eb6834` laranja | losango | 135° |
| lóbulo **OESTE isolado** · identidade em aberto | `LÓBULO OESTE` | `#1baf7a` água | triângulo | — |

**Azul no ocidental, laranja no oriental — a tua atribuição, e por uma razão
melhor do que a das válvulas:** a F8 já está renderizada com a caixa «OESTE —
ponto BAIXO» a azul e «ESTE — ponto ALTO» a laranja. A minha §3.2 contradizia
uma figura que já existe. Alinho o sistema pela figura.

**Regra permanente, e vai para a `PALETA.md`:**
> Toda a menção a um foco, em qualquer peça, leva **coordenada E ao lado do
> nome**. Uma válvula só pode aparecer numa peça como **atribuição com
> proveniência e amplitude** — «atribuição da gestora; quatro reconstruções
> do esquema divergem 465 m nesta válvula» — nunca como identificador.

Isto não é excesso de cautela: o item 1 da tua lista de RETIRADO é «a
designação dos dois focos esteve invertida e sobreviveu a quatro auditorias».
A coordenada ao lado do nome é a única correcção que impede o item 1 de
voltar a acontecer, e é por isso que passa a ser regra e não recomendação.

---

## D2 · ACEITE, E MUDA A MENSAGEM DE A04 — não só a ressalva

Aceito integralmente, e vai mais longe do que escreves.

Se no disco oriental **50,2 % das células estão abaixo de 0,5 m** e **22,7 %
do que a máscara chamava «plantado» não tem pérgola**, então o declive de
+0,01103/ano (p = 0,0162) mede uma coisa **mista**: parte declínio de planta
viva, parte **pomar que nunca lá esteve ou que já foi removido**.

Consequência para a apresentação, e é grande: **o foco oriental deixa de
poder ser vendido como «uma frente de doença crónica».** A leitura honesta é
que o lado oriental é, em proporção por quantificar, uma **falha de
instalação/estabelecimento** — o que é coerente com tudo o resto que sabemos
dele (terreno alto, solo mais pobre da exploração, deprimido desde a
primeira cena).

E isso **reforça** o caso, não o enfraquece: **a história de doença é a do
foco ocidental** — terreno bom, cota baixa, canópia saudável até 2024,
colapso em 2025 num sítio onde havia planta. É aí que a biologia tem de ser
procurada, e é isso que a campanha de Setembro tem de dizer que vai fazer.

**Acções:**
1. A04 divide a mensagem em duas linhas, não uma. Oriental: «deprimido desde
   a primeira cena, e metade do disco não tem copado — o que ali falta é em
   parte pomar». Ocidental: «tinha copado, perdeu-o em duas épocas».
2. O número +0,01103/ano só se publica **com a fracção sem copado impressa ao
   lado**, na mesma linha. Nunca sozinho.
3. **Corre a série do disco oriental restrita às células COM pérgola** (MDS−MDT
   acima do teu limiar). Se o declive sobreviver, é o número mais forte do
   processo e passa a ser publicável sozinho. Se não sobreviver, é um
   resultado ainda mais interessante e a A04 di-lo. **Uma hora de trabalho e
   resolve a peça central.** Faz isto antes de desenhar a A04.

---

## D3 · ACEITE — F10 e F12 no caule, e a F12 sobe mais do que propões

- **F10** entra logo a seguir à A00. Concordo: sem ela a tese «dois focos»
  não se sustenta, e agora sabemos que ela também é a peça que sustenta a D2.
- **F12 sobe ao caule e ganha o lugar imediatamente a seguir à A04.** Um
  instrumento independente do Sentinel-2 é a resposta à única pergunta que um
  revisor hostil faz primeiro — *«isto é o vosso processamento ou é o
  campo?»*. Onze anos dentro de ±0,004 e depois 0,046 e 0,146 é uma resposta
  completa, e não a quero num cartão expansível.
- **F11** imediatamente antes do pedido, como propões.
- **F9** dentro da A04, como propões.

---

## D4 · ACEITE, e a tua ressalva vai impressa

44,93 ha (tabela do gestor) contra 44,36 ha (IFAP, ENT 472062), 1,3 %. A
ressalva que tu próprio registaste — as fontes não são independentes, o
ENT_ID foi seleccionado pela geografia do gestor — **vai no rodapé da peça
que usar o número**, com essas palavras. Concordância, não validação cruzada.

---

## D5 · ACEITE — e o teste da paisagem sobe a A02

«A mata madura não se mexeu: −0,0035, p = 0,81; o milho caiu 0,077» é a peça
que responde a «isto é o pomar ou é o ano». Passa a ser **o painel direito
da A02**, ao lado do perfil topográfico. O inventário (1 054 ha, 204
beneficiários, uma exploração a 8,1 km com degrau em 2024) entra na A10 como
teste por correr — é um dos critérios de refutação, não um facto arrumado.

---

## D6 · ACEITE

- «T1 colide com U1» — erro meu, não existe U1. Retirado.
- **F5 e F6 do `_pacote_cowork\`: confirmo a rejeição e reforço.** Assentam em
  factos retirados; não circulam, não entram em anexo, não vão para
  `_apresentacao\`. Se existirem cópias fora da `_pacote_cowork\`, marca-as no
  próprio ficheiro. As cinco regras salvas do painel C entram na A11.
- **F2 sai da sequência** — decisão tua, aceite. Anexo técnico.

---

## §5 · A LISTA DE ONZE — entra inteira, e o item 1 muda de estatuto

Os onze entram na A08. Três notas:

**O item 1 acabou de acontecer outra vez, entre nós os dois, hoje.** Foi
apanhado em duas horas em vez de semanas, e foi apanhado porque paraste antes
de desenhar. **Isso é a peça.** A A08 deve dizê-lo em texto: *«a última
ocorrência foi a 31-08-2026 e foi detectada antes de chegar a qualquer
figura»*. Um chefe percebe isso melhor do que qualquer p-value: o processo
apanha os seus próprios erros e apanha-os cada vez mais depressa.

**Item 2 — o viés de calibração do Sentinel-2C de −0,048 a cair para ≈ zero.**
Isto é maior do que uma linha de RETIRADO: era um viés citado por todo o
processo e desaparecer significa que **as comparações entre anos com sensores
diferentes não precisam de correcção**. Verifica se alguma série publicada
ainda lhe aplica a correcção; se aplicar, os números mudam.

**Item 6 — o rio a ler NDVI +0,314.** É o exemplo mais legível de todo o
dossier para explicar a um leigo o que é um instrumento mal usado. Água não
pode ter NDVI positivo. **Usa-o como a caixa ilustrativa da A08.**

---

## RESPOSTAS ÀS TUAS TRÊS PERGUNTAS

**1 · Confirmo?** Confirmo o lado (azul = ocidental, laranja = oriental), pela
F8 e não pelas válvulas. E acrescento a regra da coordenada obrigatória e a
saída das válvulas da chave. Ver D1.

**2 · Caule ou cartões?** Caule, as duas, e a F12 mais acima do que propunhas.
Ver D3.

**3 · O timelapse.** Não adies. **Faz a A06 primeiro** — é a impressa e é a
exacta —, e a A05 sai quase de graça dos mesmos fotogramas: são o mesmo
cálculo, a mesma rampa, a mesma extensão. O que fica adiado até haver data de
reunião é só o `.mp4` com paragens e narração. Gera `frames\` e o `.gif`, que
serve a página.

---

## SEQUÊNCIA FINAL — catorze peças, numeração corrida para impressão

Fora `A00b`/`A08b`: num dossier impresso a numeração tem de ser corrida.

| # | peça | fonte | caule? |
|---|---|---|---|
| **P01** | O caso numa página | NOVA | ● caule |
| **P02** | Os dois focos não são a mesma coisa | **F10** | ● caule |
| **P03** | As manchas emergem sozinhas | NOVA | ● caule |
| **P04** | A prova independente (Landsat, 14 anos) | **F12** | ● caule |
| **P05** | Nove verões, escala fixa — grelha | NOVA (A06) | ● caule |
| **P06** | O que já não é, e o que falta saber | **F13** | ● caule |
| **P07** | A matriz tem uma coluna | **F11** | ● caule |
| **P08** | O plano de Setembro | **F14** | ● caule |
| P09 | Os três registos de tempo | F8 | ○ |
| P10 | Dois pontos opostos + teste da paisagem | NOVA | ○ |
| P11 | Cronologia de três faixas | F3 | ○ |
| P12 | Chave espacial e satélites | F4 + M2 | ○ |
| P13 | O que nos faria mudar de ideias | NOVA | ○ |
| P14 | Timelapse | NOVA (A05) | página/reunião |

**Oito peças no caule.** É o que um chefe lê. As seis restantes são a boca
aberta do copo, na página, e o anexo do dossier impresso.

---

## ORDEM DE EXECUÇÃO REVISTA

1. **A série do disco oriental só com células com pérgola** (D2, acção 3).
   Uma hora, e decide a mensagem da P03.
2. **`PALETA.md`** com a chave corrigida e a regra da coordenada.
3. **P03** (as manchas emergem sozinhas) — continua a ser a mais importante.
4. **P05** e depois **P14** (a grelha primeiro, o timelapse dos mesmos fotogramas).
5. **P01** — os números-herói saem da P03.
6. **P06** (bloco RETIRADO com os onze) e **P08** (orçamento + isenção).
7. **P02, P04, P07** — só verificação e rodapé de proveniência; já estão prontas.
8. P09 a P13.
9. A página.

Se o tempo acabar, para no 6. P01 + P02 + P03 + P05 + P06 + P08 é uma
apresentação defensável.

---

**Uma nota final.** O `00_ENTREGA.md` fez exactamente o que devia: parou a
produção por uma colisão de rótulo, verificou os acentos por AST em vez de
`grep`, distinguiu chave de dicionário de texto desenhado, e recusou afirmar
o alinhamento do L1 sem resolver a convenção angular. Nenhuma dessas quatro
coisas estava no memo como instrução — as três primeiras foram melhores do
que o que eu pedi. Continua assim: **onde este documento colidir com o disco,
o disco continua a ganhar.**
