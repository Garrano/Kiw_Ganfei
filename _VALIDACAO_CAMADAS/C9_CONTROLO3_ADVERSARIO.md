# C9 — CONTROLO 3 · ADVERSÁRIO

**Alvo:** o facto **C9** (`registo_de_factos.py`, linhas 293–308) e a peça
**P10 · o mapa de Braudel** (`ganfei_s2\figuras\p10_braudel_mapa.py`).
**Data:** 04-09-2026. **Sexta corrida.**
**Trabalho em** `_VALIDADE_GESTAO\_controlo3_c9\` — nada foi tocado fora dessa pasta.

**Versão auditada:** `p10_braudel_mapa.py` de **09:27**, a que produziu
`P10_braudel_mapa.png` às 09:28. **A sessão paralela reescreveu o ficheiro às
09:42, a meio desta auditoria** — ver LINE-STOP 6. Onde o texto vivo já mudou,
digo-o.

---

## O QUE ESTA CORRIDA FEZ

Nove scripts, todos em `_VALIDADE_GESTAO\_controlo3_c9\`:

| script | o que corre |
|---|---|
| `q1_estrutura.py` | as seis variáveis estruturais da C1, e onde os dois focos caem em cada uma |
| `q2_glo30.py` | a ordenação GLO-30 contra a do LiDAR, par a par, com a probabilidade de acaso |
| `q2b_copado.py` | a concordância GLO-30 é do chão ou do copado? |
| `q2c_ruido.py` | o contraste GLO-30 contra o ruído do próprio GLO-30 |
| `q3_dispersao.py` | dispersão intra-unidade da cota, a 10 m e a 50 cm |
| `q4_geometria.py` | o bordo do MDT, o B1, e a aritmética dos «445 m» |
| `q4b_cobertura.py` | o MDT tem dado sobre o B1? |
| `q4d/q4e/q4f` | os mosaicos que cobrem o B1; a cota do B1; a sua confirmação |
| `q5_numeros.py`, `q6_portao.py` | o sweep dos números da peça; os dois exploits do portão |

**Resultado sumário: o C9 resiste no essencial e a sua frase central não.**
A medição está boa. A inferência está mais larga do que a prova. E três das
quatro afirmações de proveniência da peça são falsas.

---

## 1 · CONFIRMADO

**C-1 · O contraste de 1,20 m sobrevive à escolha da unidade.** *(Q3)*
`q3_dispersao.py`, sobre `c1_03_grelha.npz` e `c1_03_dem50.npy`.

| unidade | n | mediana | dp | p5 | p95 |
|---|---|---|---|---|---|
| foco OCIDENTAL | 248 | 6,638 | **0,253** | 6,269 | 7,093 |
| foco ORIENTAL | 255 | 7,842 | **0,351** | 7,280 | 8,295 |
| referência | 110 | 6,798 | 0,570 | 6,062 | 7,923 |
| resto do pomar | 2 528 | 6,982 | 0,674 | 6,042 | 8,210 |

Desvio-padrão combinado **0,306 m** contra **1,204 m** de contraste: **d de Cohen
= 3,93**. As duas distribuições **não se tocam** — 0,0 % das células do OCIDENTAL
acima da mediana do ORIENTAL, e vice-versa; AUC 0,997. A 50 cm (101 749 e
101 777 píxeis) o quadro é o mesmo: dp 0,282 e 0,387. **A pergunta Q3 era boa e
a resposta é que o facto aguenta.** Não é uma diferença de médias a boiar dentro
do ruído.

*Uma armadilha para quem ler o JSON:* o campo `cota_dp` (0,124 / 0,164) **não é**
esta dispersão — é o desvio-padrão dentro de cada célula de 10 m, agregado por
mediana (`c1_03_mdt.py`, `cota_dp=agrega(dem, np.nanstd)`). Quem o tomasse por
dispersão intra-unidade subestimava-a por um factor de 2. A peça não o faz; mas
o número está lá, ao lado, com nome ambíguo.

**C-2 · A concordância do GLO-30 não é artefacto de copado.** *(Q2)*
`q2b_copado.py`. Esta era a via de morte óbvia: o GLO-30 é um **MDS** de radar, e
se o foco oriental tivesse mais copado, leria mais alto por razão vegetal e não
de terreno. **Mede-se e é ao contrário:** CHM do OCIDENTAL **2,25 m**, do
ORIENTAL **0,47 m**. O oriental tem *menos* copado e lê-se *mais alto* no MDS. O
copado empurra no sentido oposto ao observado. **A objecção morre, e o S3 fica
mais forte por ela.**

**C-3 · A data do voo, «06-07-2025», está certa.** `l1_data_do_voo.json`,
reproduzido por mim das duas folhas LAZ com `laspy`: `global_encoding` bit 0 = 1
(Adjusted Standard GPS Time), 16 636 497 + 17 761 266 pontos, **todos em
2025-07-06**, das 14:34:53 às 14:51:08 UTC. A linha de crédito da peça é fiel ao
instrumento primário.

**C-4 · Os números rastreáveis.** *(Q5)* 496 m entre focos
(`CAMADA_1_CERTIFICADO.md`:72) · 12,63 ha e 6 parcelas do B1 (medido do
`ifap_kiwi_largo.json`: 12,632 ha, 6 polígonos) · as quatro cotas (verbatim do
`c1_04_terreno_por_unidade.json`) · «0,036 contra 0,070, p = 3e-10»
(certificado S18: 0,0355 / 0,0703 / p = 3,2e-10) · −0,050, −0,13 a −0,23 · doze
válvulas e 60,8 % (facto C8) · a pérgola entre 2007 e 2010 · as 27 válvulas
(`CAMADA_0_CERTIFICADO.md`:87). **Nenhum destes é inventado.**

---

## 2 · CORRIGIDO

**R-1 · «A ordenação reproduz-se no GLO-30» — reproduz-se para outras quatro
unidades que não as que a peça desenha.** *(Q2)* `q2_glo30.py`.

O S3 nomeia **OESTE, referência, ESTE, zona0**. Com essas quatro, a ordenação
reproduz-se exactamente, ρ de Spearman = **+1,00**. A peça imprime outras
quatro — **OCIDENTAL, referência, resto do pomar, ORIENTAL**. Com essas:

```
ordem LiDAR : OCID < referência < resto < ORIE
ordem GLO-30: OCID < resto < referência < ORIE      <- inverte
```

ρ = +0,80, **e o par referência/resto troca de sinal**. A peça herda uma
confirmação ganha por um conjunto e credita-a ao conjunto que mostra.

E a força da confirmação é menor do que «quatro unidades» sugere: **a `zona0` é
87 % o disco ESTE** — 176 das suas 202 células estão lá dentro, e 176 das 255 do
ESTE são `zona0`. São **três** conjuntos distintos e um subconjunto de um deles.
P(ordenação exacta) não é 1/24 = 0,042; para três unidades livres é 1/6 = 0,167.
E o que a peça de facto invoca no rodapé é **o sinal de um par**: uma moeda ao ar.

Acrescente-se o que `q2c_ruido.py` mede ao nível do píxel GLO-30 (44 e 48 píxeis
distintos): contraste **+0,413 m**, dp combinado 0,713, **d = 0,58** (contra 3,93
no LiDAR), IC95 **[+0,121 · +0,705]**. O critério de aprovação escrito no próprio
`c1_10_nivelamento.py` é `dg > 0.3`; o valor guardado, 0,312 m, **passa por
0,012 m** — e o IC95 contém o limiar. **A confirmação existe e é do sinal
correcto. Não é «a ordenação das quatro unidades», e não é forte.**

**R-2 · Não há «duas campanhas de voo». As duas folhas são do mesmo voo, com
dezasseis minutos de intervalo.**

A peça escreve, no rodapé e no docstring: *«o degrau de costura entre as duas
campanhas de voo é de 0,058 m contra os 1,204 m do contraste»*. O
`c1_02_costura.json` diz `voo_oeste: 2025-08-02`, `voo_este: 2026-01-15`. **É
falso.** As duas folhas — LO-158565 e LO-159565, as dos dois focos — foram
voadas **ambas a 06-07-2025**, entre as 14:34:53 e as 14:51:08 UTC. Está em
`_VALIDADE_GESTAO\l1_data_do_voo.json` desde 31-08, calculado *a pedido do
adversário de 29-08*, e a própria P02 escreve que os metadados **«dão uma janela
inútil de catorze meses»**. Reproduzi-o das LAZ.

**A correcção reforça o C9.** O confunditor contra o qual o controlo de costura
defendia não é pequeno: **não existe**. Mas três coisas ficam por arrumar, e são
line-stop:

- o **S2** do `CAMADA_1_CERTIFICADO.md` afirma as quatro campanhas como facto;
- `c1_03_mdt.py` constrói `c1_03_camp50.npy` a partir dessas datas;
- o «**controlo de campanha**» de `c1_04_focos_terreno.py` testa uma partição
  que não é real — testou nada.

**R-3 · Os «445 m» medem a aresta errada, e o sinal está invertido.** *(Q4)*
`q4_geometria.py`.

```
bordo SUL do mosaico     N 4 654 276,8
bordo NORTE do B1        N 4 654 477,0
bordo SUL   do B1        N 4 653 832,1

4 654 276,8 − 4 653 832,1 = +444,6 m   <- o número da peça
4 654 276,8 − 4 654 477,0 = −200,3 m   <- a folga real entre as duas caixas
```

Os 445 m são a distância do bordo do mosaico à aresta **mais afastada** do B1.
A folga real é **negativa**: a caixa entra **200 m dentro** do sector. **43,8 %
da área do B1 cai dentro dela.** A peça desenha as duas geometrias na mesma
janela e rotula-as como separadas por 445 m.

**R-4 · Os «60 % da exploração» são 79,8 %, e o número parece vir de outro
facto.** *(Q5)* `q5_numeros.py`. O recorte cobre o polígono principal (30,31 ha)
mais 5,53 ha do B1 = **35,84 ha de 44,93 = 79,8 %**. Mesmo excluindo o B1 por
inteiro, 30,31/44,93 = **67,5 %**. Nenhuma leitura dá 60 %. O painel da direita, três
centímetros acima, escreve «**60,8 %**» — que é a cobertura da partição por
válvula, facto C8, **outra grandeza**. Duas quantidades, um número.

**R-5 · O bordo desenhado não é o do LiDAR.** É `AOI + FOLGA = 300.0`,
constante escolhida em `c1_03_mdt.py`. A peça chamava-lhe «bordo do MDT LiDAR».
*A sessão paralela corrigiu este rótulo às 09:42* — passou a «bordo do MOSAICO
recortado (AOI + 300 m) — não do LiDAR». **O docstring e o PNG em disco ainda
carregam a versão antiga.**

**R-6 · Os «28 % de área sem pérgola» no foco oriental são 50,2 %.**
Medido com o critério que **o próprio script define três linhas acima**:
`COM = np.isfinite(h) & (h >= 0.5)` sobre `chm_altura.npy`.

| unidade | células | sem pérgola | % |
|---|---|---|---|
| foco ORIENTAL | 255 | 128 | **50,2 %** |
| foco OCIDENTAL | 248 | 30 | 12,1 % |
| referência | 110 | 7 | 6,4 % |
| pomar | 3 031 | 377 | 12,4 % |

E 50,2 % é exactamente o que a **P02** escreve — «no oriental, metade é chão».
A peça desenha os dois focos com esta máscara e depois escreve, no rodapé, um
número que ela contradiz. **O «28 %» está na `LISTA_FINAL` e no registo** — é a
verificação 2 verde por cima de conteúdo errado.

---

## 3 · REJEITADO

**X-1 · «Não há cota, não há declive, não há drenagem» para o B1. É falso duas
vezes — e a cota está medida no fim desta secção.** *(Q4)*

Primeiro: **5,50 ha do B1 já têm cota válida** dentro do `c1_03_dem50.npy` que a
peça abre para desenhar o bordo (`q4b_cobertura.py`; 13 742 de 31 603 pontos de
amostra, 100 % com valor onde caem dentro da caixa). Duas das seis parcelas estão
cobertas a 93 % e a 100 %.

Segundo, e decisivo: **100 % do sector é coberto por mosaicos que já estavam na
mesma pasta** — `MDT-50cm-157564-07-2025_v02.tif` (6,29 ha) e
`MDT-50cm-158564-07-2025_v02.tif` (6,35 ha), dois dos vinte e um que
`c1_03_mdt.py` já abre (`q4d_tiles.py`). **O que falta ao B1 não é LiDAR. É uma
constante:** `FOLGA = 300.0`, aplicada à caixa de uma AOI que a própria peça
declara ser «uma DECISÃO, não uma fronteira do terreno». A peça desenha o
resultado de um recorte como se fosse o fim do instrumento.

**Então medi-a.** `q4e_cota_do_b1.py`, 505 700 píxeis a 50 cm, cobertura 100,0 %:

| CUL_ID | ha | mediana |
|---|---|---|
| 6476415 | 3,89 | 6,187 |
| 8845729 | 1,88 | 6,346 |
| 6476420 | 2,50 | 6,096 |
| 8845739 | 2,20 | 5,982 |
| 8845740 | 0,90 | 5,674 |
| 6476425 | 1,28 | 5,705 |
| **B1 todo** | **12,64** | **6,062** |

**O B1 está 0,576 m ABAIXO do foco OCIDENTAL — o que a peça chama «o ponto
BAIXO» — e 1,780 m abaixo do ORIENTAL.**

Sujeitei o meu próprio número às regras que aplico aos outros
(`q4f_b1_confirmacao.py`): **controlo de costura** entre as duas folhas que o
cobrem — degrau mediano **0,046 m** contra os 0,576 m em causa, razão 12,4× — e
**instrumento independente**: o GLO-30 põe o B1 a 6,497 m, **abaixo dos dois
focos, com o sinal certo nas duas comparações** (−0,978 e −1,249 m). A sessão
paralela chegou ao mesmo valor às 09:41 (`b1_terreno.json`, mediana
6,062077522277832, n = 506 125) — réplica no mesmo directório, que confirma a
execução e não as premissas (pré-voo §6); a confirmação que conta é a do GLO-30.

**X-2 · A inferência central, como está escrita, é rejeitada.** *(Q1)*
`q1_estrutura.py`.

> «Duas unidades em posições opostas não podem partilhar uma causa que venha da
> posição.»

É um negativo universal assente numa das **seis** variáveis estruturais que o
certificado da C1 tem para as mesmas unidades. Nas outras cinco:

| variável | OCID | ORIE | ref | resto | onde caem os focos |
|---|---|---|---|---|---|
| **cota** | 6,638 | 7,842 | 6,798 | 6,982 | **extremos opostos** |
| declive | 4,631 | 6,082 | 4,619 | 4,705 | extremos |
| rug25 | 0,1242 | 0,1667 | 0,1242 | 0,1281 | extremos |
| **tpi** | −0,0040 | −0,0031 | −0,0008 | +0,0015 | **par adjacente** |
| **res150** | 0,0142 | 0,0172 | 0,0168 | 0,0486 | **quase idênticos** |
| **exposição** | 324,6° | 326,7° | 331,9° | 333,2° | **par adjacente** |

Nos três últimos os dois focos são **o par mais parecido do conjunto**, e
parecidos *contra* as outras unidades:

- **exposição:** 2,2° a separá-los; 8,6° até ao resto do pomar;
- **tpi:** indistinguíveis um do outro (Mann-Whitney **p = 0,43**) e, **juntos**,
  diferentes de referência+resto (**p = 0,016**) — ambos mais côncavos;
- **res150:** indistinguíveis um do outro (**p = 0,98**) e, juntos, diferentes de
  referência+resto (**p = 7,4×10⁻⁷**, −0,030 m) — ambos mais rebaixados em
  relação à vizinhança larga.

**Os dois focos partilham três atributos de posição.** A frase escolhe a variável
em que são opostos e cala as três em que são o par. Isso é a vulnerabilidade que
a Bertran 2026 nomeia: relato selectivo quando as análises defensáveis são
baratas de gerar.

**O que fica de pé, e é útil:** *uma causa monótona na cota absoluta, na gama
6,6–7,8 m e à escala do disco de 90 m, não explica as duas manchas.* Isso mata
«o baixo alaga» e mata «o alto seca» — não é pouco.

**O que a frase NÃO exclui, e diz que exclui:**
1. uma causa ancorada na **concavidade local** ou no **rebaixamento face à
   vizinhança de 150 m** — variáveis em que os dois focos coincidem, medidas
   acima;
2. uma causa a **profundidade constante** e não a cota constante — sola de
   compactação, inversão de horizontes. O próprio `CAMADA_1_CERTIFICADO.md`:111
   lista isto como não visto por instrumento nenhum da camada;
3. uma resposta **não monótona** na cota;
4. uma causa que **não venha da posição** — raiz, material de plantação, rede,
   máquina — cuja expressão a posição apenas module.

**E o B1 refaz o argumento em melhor.** Com a cota que a peça diz não existir, o
eixo passa a ter cinco pontos:

```
B1          6,06 m   nao entra no acontecimento
OCIDENTAL   6,64 m   AFECTADO
referencia  6,80 m   —
resto       6,98 m   —
ORIENTAL    7,84 m   AFECTADO
```

Não é monótono e não é em U: o mais baixo de todos não é afectado, o segundo
mais baixo é, os dois do meio não são, o mais alto é. **A cota não ordena as
unidades pelo desfecho.** É mais forte do que «extremos opostos», resiste às
quatro fugas acima, e precisa exactamente da unidade que a peça declarou sem
dados. *O título que a sessão paralela pôs às 09:42 — «A cota não acompanha o
declínio» — é esta frase.*

---

## 4 · NÃO TESTÁVEL

**N-1 · Se o B1 é um contraste de desfecho válido.** Medi-lhe a cota, não a
saúde. A própria peça ressalva que o B1 «está a encher, que é outra coisa».
Enquanto isso não estiver decidido, o quinto ponto do eixo é **uma cota sem
rótulo** — e escrevo-o assim, não como «o são».

**N-2 · A época dos mosaicos que cobrem o B1.** Só há LAZ em disco para
158565 e 159565. Para 157564 e 158564 não há tempo GPS, e o catálogo já se
provou inútil. O controlo de costura limita um degrau **local** a 0,046 m; não
limita um desvio de datum de folha inteira. A cota do B1 é sólida em ordenação,
menos em valor absoluto.

**N-3 · Se o GLO-30 é «independente que baste» para uma afirmação sobre o chão.**
É outro modelo de elevação. Testei e rejeitei a via de falha que consigo testar —
o copado (C-2). Um erro sistemático **comum a todos os produtos de elevação**
sobre este aluvião não é testável com o que está em disco. O rodapé da peça
chama-lhe «um sensor sem relação com o LiDAR»; é mais exacto dizer *outra missão
e outra física, a medir uma superfície que não é a mesma*.

**N-4 · De onde veio o «28 %».** Sei que está errado (R-6) e não sei que
denominador o produziria. Não o reconstruo por inferência.

---

## 5 · LINE-STOP

**L-1 · A prova de independência do C9 é o ficheiro do próprio instrumento.**
`registo_de_factos.py`:302–305 declara o GLO-30 como confirmador e passa
`prova=PV["terreno"]` = **`c1_04_terreno_por_unidade.json`** — a saída do LiDAR.
Verifiquei: a cadeia `glo` não ocorre nesse ficheiro, em chave nenhuma nem em
valor nenhum. O resultado do GLO-30 vive noutro sítio, no
`c1_10_nivelamento.json`. **A condição 2 pergunta `os.path.exists` e mais nada.**
Corri a linha viva em `q6_portao.py`; sai `VEREDICTO` com
`[c1_04_terreno_por_unidade.json]` ao lado do nome «GLO-30».

**L-2 · A quinta encarnação de «ausência tratada como aprovação»: as condições
3, 4 e 6 continuam a ser opcionais.**

O omissivo da condição 5 foi invertido a 03-09 com a razão escrita no próprio
ficheiro — *«quem se esquece da bandeira é exactamente quem precisa dela»*. **A
condição 6 não foi.** `if self._fronteira is not None and not self._fronteira[0]`
— quem nunca chama `fronteira()` nunca é interrogado sobre ela. É a condição que
existe pelo `fazer_masks_v2.py`, e a regra que a `CLAUDE.md` põe em primeiro
lugar. O mesmo vale para `ancoras()` (3) e `reproduz()` (4).

Reconstruí a **retirada número 1** deste dossiê — a AOI `b1`, tecido urbano de
Valença do outro lado do Minho, 49 ficheiros em quarentena — e **o portão
autorizou-a** (`q6_portao.py`, exploit 2):

```
VEREDICTO: o degrau e regional; nada em Ganfei o causou
  instrumento    : razao entre o infravermelho proximo e o vermelho,
                   Sentinel-2, sobre a pasta sentinel_b1/
  confirmado por : a mesma razao, calculada em Landsat 8/9 [MODELO_PROMPT.md]
  unidade no tempo: rastreio_que_eu_inventei.json, 999 cenas, 2 unidades,
                    0.0 dias - verificadas: POMAR, VALENCA_URBANO
```

Quatro portas, todas abertas:
1. **não chamei `fronteira()`** — a condição 6 não disparou;
2. `prova=` aponta para **`MODELO_PROMPT.md`**, um modelo de prompt em markdown.
   Existe, logo conta;
3. o rastreio de identidade é **um JSON que escrevi dois milissegundos antes**,
   com as unidades que eu quis listar como contínuas;
4. a guarda do mesmo índice não disparou porque escrevi «razão entre o
   infravermelho próximo e o vermelho» em vez da cadeia `NDVI` — a lista
   `INDICES` faz correspondência de texto.

**A condição 5 passou de aceitar uma frase a aceitar um ficheiro. Um ficheiro
que eu próprio escrevo é exactamente tão vazio como a frase era.** A quinta
encarnação não é uma condição nova a falhar: é a mesma — o portão continua a
perguntar *se algo está presente*, nunca *se tem alguma coisa a ver com a
afirmação*.

**Mínimo executável:** que `prova=` e `identidade_no_tempo()` exijam um ficheiro
(a) mais antigo que a corrida que o invoca, (b) produzido por um script do
registo, e (c) que contenha a cadeia do instrumento declarado. As três são
verificáveis em cinco linhas.

**L-3 · A verificação 7 do `certificar.py` não vê a P10.**
O filtro é `f.lower().startswith("p0")`. Das onze peças `P*`, **vê dez e falha
uma** — `P10_braudel_mapa.png`. A convenção de dois dígitos com zero à esquerda
quebra-se exactamente na peça mais nova e mais argumentativa.

**Prova ao vivo:** às 09:45 corri `certificar.py` e imprimiu

```
  figuras          nenhuma mais velha que a lista de factos
```

enquanto `P10_braudel_mapa.png` (09:28) estava **catorze minutos mais velha que
`p10_braudel_mapa.py`** (09:42). Correcção de uma linha:
`re.match(r"^p\d", f.lower())`.

**L-4 · O tamanho do buraco, medido.** `certificar.py` devolveu
**`CERTIFICADA`, código de saída 0**, às 09:45, com **27 factos passam, 0
bloqueiam** e **«27 códigos coincidem, sem deriva»** — enquanto, ao mesmo tempo,
a peça em disco afirmava: 445 m (aresta errada, sinal invertido), «não há cota»
(falso para 5,5 ha já calculados e para 12,63 ha disponíveis), 60 % (é 79,8 %),
«duas campanhas de voo» (é uma), «28 % sem pérgola» (é 50,2 %, pelo critério do
próprio script) e «a ordenação reproduz-se» (não, para as quatro unidades que
mostra). **Seis afirmações falsas, verificação verde.**

As verificações 1–6 comparam **códigos de facto** entre a prosa e o registo. A 7
compara **datas de ficheiro**. **Nenhuma abre uma figura.** E a única que podia
apanhar deriva por data é a que não vê esta figura.

**L-5 · `c1_02_costura.json` está morto e continua a ser consumido.** As datas
de campanha que contém foram substituídas a 31-08 pela leitura do tempo GPS, e
alimentam ainda `c1_03_camp50.npy` (`c1_03_mdt.py`) e o «controlo de campanha»
de `c1_04_focos_terreno.py`, além do **S2** do certificado da Camada 1. O
ficheiro não está marcado como retirado, por isso a verificação 3 do
`certificar.py` — «nenhum documento vivo cita um retirado» — está verde por cima
dele.

**L-6 · A sessão paralela reescreveu o alvo a meio desta auditoria.**
`p10_braudel_mapa.py`: 09:27 → **09:42**. Mudou o título para «A cota não
acompanha o declínio», a legenda do bordo para «bordo do MOSAICO recortado
(AOI + 300 m) — não do LiDAR», e o subtítulo para «o sector que NÃO declina está
mais baixo do que as duas» — três correcções que coincidem com R-5 e X-2.
**Continuam no ficheiro vivo:** «445 m a sul do bordo do DEM» (docstring, l. 30),
«SEM cota, SEM dreno, SEM declive» (l. 196), «60 % da exploração» (l. 28), «entre
as duas campanhas de voo» (l. 242), «28 % de área sem pérgola» (l. 250). **O
subtítulo novo e o rótulo do mapa contradizem-se agora dentro da mesma página:**
um afirma a cota do B1, o outro diz que ela não existe. E o PNG em disco é
anterior a tudo isto.

---

## O VEREDICTO, EM DUAS LINHAS

**A medição do C9 aguenta e ficou mais forte do que estava** — o contraste de
1,20 m separa sem sobreposição, a confirmação independente não é copado, e o
confunditor de voo contra o qual se defendia nem sequer existe.
**A frase do C9 não aguenta:** escolhe uma de seis variáveis estruturais, e nas
outras três os dois focos são o par mais parecido do conjunto. A versão
defensável — *a cota não ordena as unidades pelo desfecho* — precisa do B1, que a
peça declarou sem dados e que estava em dois ficheiros que o `c1_03_mdt.py` já
abre.

**E o portão certificou tudo isto com código de saída 0.**
