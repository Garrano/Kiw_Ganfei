# Camada 2 — resposta ao adversário R2: os cinco testes, corridos

**Data:** 31-08-2026 · **Responde a:** `CAMADA_2_ADVERSARIO_R2.md`, Parte 5.
**Precedência:** onde estes resultados contrariam o `CAMADA_2_CERTIFICADO_R2.md`,
ganham eles — são medição contra afirmação.

**Saldo: dois factos voltam, um cai por inteiro, dois ganham margem, e o teste
mais barato de todos abriu a maior lacuna do caso.**

---

## T1 · O rácio degrau/recta SOBREVIVE. R2 tinha razão no método e errou no efeito.

A acusação era boa: `TARDIO = d >= "2025"` foi escolhido depois de ver a série,
logo o degrau tem um parâmetro que a comparação não contava. Testado de três
maneiras.

**Perfil de todos os pontos de quebra** (seis interiores, com pelo menos duas
cenas de cada lado): o corte 2024|2025 é o máximo em todas as unidades de foco.
Confirma-se que o número publicado era o máximo de uma família.

**AICc, contando a quebra como terceiro parâmetro:**

| unidade | ΔAICc (degrau − recta) | vence |
|---|---|---|
| ORIENTAL Zona 0 com pérgola | **−7,63** | degrau |
| OCIDENTAL disco 90 m | **−6,74** | degrau |
| ORIENTAL disco 90 m | −6,57 | degrau |
| resto do pomar | +6,36 | **recta** |
| **B1 · lóbulo SW (kiwi)** | **+9,57** | **recta** |

**Nulo do máximo** — 20 000 permutações da ordem das cenas, e em cada uma a
nula procura o seu próprio melhor corte, tal como nós:

| unidade | razão obs. | p95 do nulo | p |
|---|---|---|---|
| ORIENTAL Zona 0 | 3,98 | 2,64 | **0,0227** |
| ORIENTAL disco | 3,54 | 2,20 | **0,0150** |
| OCIDENTAL disco | 3,60 | 2,09 | **0,0030** |
| resto do pomar | 1,29 | 1,67 | 0,368 |
| **B1 · lóbulo SW** | 1,31 | 1,96 | 0,358 |

**S2 volta ao PASSA PARA CIMA**, com o método corrigido e com o B1 dentro. E o
B1 é o que mais acrescenta: **é a terceira unidade de kiwi da exploração, e nela
a recta ganha com a maior margem das cinco.** O degrau não é uma propriedade de
«pomar de kiwi em Ganfei» — é uma propriedade dos dois focos.

## T2 · A pergunta que faltava É respondível, e a lacuna é maior do que o adversário supôs

O adversário pediu a contagem sem a ir buscar. Buscada, ao mesmo catálogo
público de onde veio toda a série.

**Entre 2025-08-14 e 2026-07-27 existem 60 cenas com menos de 20 % de nuvem. Onze
delas estão em plena estação — o mesmo critério que a série usa.**

| 2025 | 08-16 (×2) · 08-21 · 08-23 · 08-24 · 08-26 (×2) | DOY 228–238 |
| 2026 | 07-02 (×2) · 07-05 · 07-25 | DOY 183–206 |

Sete cenas **dois a doze dias depois** da cena de 2025 usada, e quatro **dois a
vinte e cinco dias antes** da de 2026.

**Consequência.** A frase «um acontecimento, duas épocas» — que atravessa esta
camada e todas as de cima — assenta em **duas cenas separadas por onze meses**,
com **onze cenas equivalentes por olhar no intervalo**. Um acontecimento agudo
único e dois declínios sucessivos continuam indistinguíveis, e agora sabe-se que
não é por falta de dados.

**Não se corre aqui.** Esta camada identifica a lacuna; medi-la é análise nova e
tem de ser desenhada, não improvisada. **Vai para NÃO TESTÁVEL com o inventário
anexo, que é o oposto de uma lacuna vaga.**

## T3 · S5 CAI. E o satélite #1 não é um satélite.

Redesenhada a nula no estrato dos alvos — e **corrigido um defeito do próprio
teste**: a primeira banda (60–150 m) incluía células dentro dos discos de 90 m,
ou seja a nula estava contaminada pelos focos. Banda limpa: 90–160 m.

| satélite | degrau 2025 | percentil >120 m | percentil 90–160 m |
|---|---|---|---|
| #1 · 83 m | −0,0480 | 2,4 % | **9,6 %** |
| #2 · 112 m | −0,0414 | 4,6 % | **14,2 %** |
| #3 · 145 m | −0,0365 | 7,1 % | **29,2 %** |

**No seu próprio estrato de distância, os três são banais.** Os percentis
publicados vinham de uma comparação com terreno mais afastado.

**E as bandas diferem de facto:** discos de 21 células dão mediana **−0,0166**
a mais de 120 m contra **−0,0271** entre 90 e 160 m, Mann-Whitney p < 0,0001.
Há mais dano no anel próximo — mas **não é um gradiente** (S7 mantém-se). A
leitura parcimoniosa não é «halo»: **é que o corte dos discos aos 90 m é
arbitrário e o dano não pára lá.** Os focos são maiores do que os discos.

**E o #1 está a 83 m do centro, dentro do disco de 90 m.** Não é um núcleo
destacado: é parte do foco oriental. Restam **dois** candidatos a satélite, e
nenhum se distingue da sua vizinhança.

**S5 sai do PASSA PARA CIMA.** Sobrevive apenas a medição directa: a base
2017-24 dos três é normal (0,878 · 0,872 · 0,901) e os três descem em 2025.

## T4 · S3 mantém-se, com a margem que lhe faltava — e o pior número é o da referência

Contagem de blocos de 30 m distintos por unidade (grelha alinhada à AOI, ±1
bloco de desfasamento):

| unidade | células 10 m | píxeis Landsat | inteiramente dentro |
|---|---|---|---|
| OESTE com pérgola | 218 | **35** | 12 |
| ESTE com pérgola | 127 | **27** | **2** |
| resto do pomar | 2 220 | 334 | 105 |
| **referência sistemática** | 110 | **110** | **0** |

**Duas coisas más.** O foco oriental tem 27 píxeis Landsat e **só dois
inteiramente dentro** — 25 dos 27 atravessam a fronteira, logo o valor da
unidade é largamente a sua vizinhança. E a **referência é 110 células em 110
píxeis distintos**: cada célula de referência ocupa **um nono** de um píxel
Landsat, e o valor que dela sai é o da vizinhança de 30 m, não o dela.

**S3 mantém-se para a direcção e a datação** — que é o que ela sustenta — **com
o n impresso**. A linha «referência sistemática −0,0159» do Landsat **sai**: não
mede a referência.

**E fica registado que o B1 não tem Landsat.** A terceira unidade de kiwi da
exploração nunca foi medida por segunda constelação. NÃO TESTÁVEL.

## T5 · A referência reconstruída. A paragem de linha da moeda LEVANTA-SE.

Corrida a regra pré-registada: excluir células de referência a menos de **120 m**
(90 do disco + 30 de margem justificada). **Nada foi decidido depois.**

- referência antiga: 110 células · degrau **−0,0481**
- referência limpa: **95 células** · degrau **−0,0189**
- limite do pré-registo (não descer abaixo de 60): **cumprido**

| unidade | fosso médio antigo | com referência limpa | declive limpo |
|---|---|---|---|
| Zona 0 sem nu2021 (o publicado) | +0,0595 | +0,0679 | **+0,01427/ano** |
| ORIENTAL Zona 0 com pérgola | +0,0683 | +0,0768 | **+0,01208/ano** |
| OCIDENTAL disco 90 m | +0,0246 | +0,0330 | +0,00941/ano |
| resto do pomar | +0,0179 | +0,0263 | **−0,00478/ano** |
| **B1 · lóbulo SW (kiwi)** | +0,2092 | +0,2177 | **−0,02042/ano** |

**Cinco fossos cresceram, nenhum encolheu, nenhum mudou de sinal.** Pela tabela
pré-registada isto é «o esperado»: os números publicados na moeda do fosso eram
**conservadores** — e isso deixa de ser inferência (a M3 do adversário) e passa a
medição.

**Verificação de construção passou:** o degrau em nível absoluto não mexeu
(−0,1236 e −0,1288), como tinha de ser.

**A paragem de linha da moeda levanta-se.** O fosso volta a ser utilizável,
agora contra uma referência que não contém os focos. **Deixa de haver duas
moedas em conflito: há uma grandeza com duas leituras, e as duas contam a mesma
história** — os focos abrem o fosso a +0,012 a +0,014/ano, o resto do pomar
fecha-o a −0,005, e o B1 fecha-o a −0,020.

---

## PASSA PARA CIMA — revisto depois dos testes

**S1.** Contraste foco-menos-controlo em nível absoluto: **−0,1152** e
**−0,1100**. Menos exposto ao degrau de plataforma, não imune; resíduo possível
~0,02.

**S1b.** Sinal e ordenação invariantes em 43 corridas **aninhadas** (não
independentes). Focos e controlo não se tocam.

**S2 · RESTAURADO.** O degrau bate a recta com o ponto de quebra contabilizado:
ΔAICc −6,6 a −7,6 nos focos, **+6,4 no controlo e +9,6 no B1**; p do máximo
0,003 a 0,023 nos focos, 0,36 nos dois não-focos.

**S3 · COM MARGEM.** Landsat replica direcção e datação; p exacto 0,0110 = 1/91.
**n = 35 (ocidental) e 27 (oriental) píxeis, com 12 e 2 inteiramente dentro.** A
linha da referência Landsat sai.

**S4.** Correcção de dia-do-ano ≤ 0,0011, limite superior. Duas premissas
declaradas: linearidade em 58 dias perto da saturação, e transporte do
coeficiente de 2025 para o grupo 2017-2024.

**S5 · RETIRADO.** No estrato certo os satélites estão nos percentis 9,6 / 14,2
/ 29,2 %. O #1 está dentro do disco. Sobrevive só: base 2017-24 normal e descida
em 2025 — medição directa, sem inferência.

**S6 · PROMOVIDO A MEDIÇÃO.** A referência tinha 14 células nos focos; limpa,
o seu degrau cai de −0,0481 para −0,0189, e **os cinco fossos crescem**. Os
números do fosso eram conservadores — medido, não inferido.

**S7.** Não há gradiente contínuo com a distância. **Mas o anel de 90–160 m tem
mais dano do que o terreno a mais de 120 m** (−0,0271 contra −0,0166,
p < 0,0001): o dano não pára na fronteira arbitrária dos discos.

**S8.** O radar distingue o ocidental e não o oriental, pela composição deste.

**S9 · NOVO.** **O B1 — 12,64 ha de kiwi da mesma exploração — não tem degrau
por nenhum teste**: a recta vence por ΔAICc +9,57, o fosso fecha a −0,020/ano, e
o desvio à tendência própria é +0,012 (p = 0,76). É o comparador mais próximo
que o caso tem, dentro da mesma gestão.

## NÃO TESTÁVEL — entradas novas

- **A forma do acontecimento entre 2025-08-14 e 2026-07-27.** Onze cenas de
  plena estação por olhar, inventariadas em `t2_cenas_descartadas.json`.
  Distingue evento agudo de declínios sucessivos.
- **O B1 no Landsat.** Nunca corrido; fora da AOI descarregada.
- **O radar sobre o copado oriental sem o chão.**
- **Se o anel de 90–160 m é extensão dos focos ou vizinhança afectada.**

---

**Uma nota sobre o T3.** O primeiro desenho do meu próprio teste tinha a nula
contaminada pelos discos que ela devia evitar — o mesmo tipo de erro que o teste
existia para apanhar. Foi visto antes de o resultado ser escrito, e a correcção
mudou os percentis de 25/32/37 % para 9,6/14,2/29,2 %. **A conclusão não mudou;
os números sim, e teriam sido publicados errados.**
