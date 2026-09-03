# Camada 5 — Decisão

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada C5 de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md` e depois `CONTROLOS.md`. Os
controlos 1 e 2 aplicam-se-te por inteiro. O controlo 3 — o adversário — corre
em C0 e C2; a C4 levou um por decisão do coordenador. **Assume que levas
também: escreve a secção «Nota ao adversário» e não a escondas no fim, e não
escolhas para ela os pontos que já sabes resolver — foi o que as três camadas
anteriores fizeram e foi apanhado nas três.**

A tua camada é a decisão: **desenho de amostragem, árvore do Pilar D, medidas.**
És a última e dependes de tudo. És também a primeira com autorização para dizer
**o que fazer**. As cinco abaixo tinham-no proibido.

**Aviso de nomenclatura, que já custou tempo três vezes neste processo.** Nunca
escrevas «OESTE» ou «ESTE» sem a coordenada ao lado.

| nome | coordenada | bloco / válvulas |
|---|---|---|
| **foco OESTE** | **E530485 N4655053** | B2, v8 (ponto a 34,5 m) e v9 (97,7 m) |
| **foco ESTE** | **E530977 N4655117** | B3, v13 (80,8 m) e v14 (93,2 m) |
| **núcleo N3** | **E531068 N4655145** | **a 95,2 m do foco ESTE — FORA do disco de 90 m. NÃO é o foco ESTE.** |
| **maior vazio circular** | **NÃO É GEOMETRIA — ver aviso abaixo** | zona, não ponto |
| **B1** | bloco separado, v1-v5, a **772–1435 m a sudoeste** do foco OESTE | **NÃO é o «foco OESTE»** |

> **Aviso sobre o «maior vazio circular», corrigido pelo adversário da C4.** A
> versão anterior desta linha dava-lhe centro `E530476 N4655046`, 3,98 ha, e
> «a 11,4 m do centro do foco OESTE», ao lado das coordenadas de testemunho e
> com o mesmo estatuto. **Estava errado e a C5 tê-lo-ia tratado como geometria.**
>
> O objecto é o **núcleo n.º 22 da corrida B do multiverso**, delimitado por
> **anomalia de NDVI e NDMI** — não por levantamento —, com `first =
> 2026-07-27`, área entre **2,38 e 3,98 ha conforme a corrida**, e centro com
> **30 m de dispersão** entre derivações independentes. **Os 11,4 m eram a
> distância entre duas estimativas do mesmo centróide pelo mesmo instrumento:
> informação locacional zero, e precisão falsa a 1,14 células de 10 m.**
>
> E há um desencontro de datas: é **geometria de 2026** aplicada a uma colheita
> de **06-06-2025**. Só **55,7 %** da zona declarada cai dentro do disco de
> 90 m do foco.
>
> **O que é testemunho, e vale:** o gestor situou a amostra «Kiwi 1000» — que é
> o **informe 331/2025 V.1**, expediente 2025045292 — no **lado oeste do maior
> vazio circular**. **Lado oeste de uma zona, não centro de um polígono.** Usa-o
> assim e não converses a zona em ponto.
>
> **E pergunta por fazer, que decide isto:** o gestor identificou esse vazio **no
> terreno** ou **numa imagem nossa**? Se foi numa imagem nossa, a colocação
> herda o nosso produto e não é independente.

**E três raios de disco circulam para os mesmos focos — 70 m, 90 m e 120 m.**
Sempre que citares uma área ou uma distância de foco, diz qual.

**As tabelas de válvulas do `REGISTO_DE_NOMES.md` e o `valvulas_v6.json` estão
desactualizados.** O ficheiro operativo é `ganfei_s2\valvulas_por_area.json`
(G35). O `REGISTO_DE_NOMES.md` põe a v8 a 157 m do foco OESTE; o ficheiro
operativo põe-na a 34,5 m.

---

## O que herdas — e só isto

Seis listas fechadas, por esta ordem de precedência. Trata-as como dados, não as
revalides, e não uses nada que não esteja aqui.

**Antes das listas, três correcções que existem a montante e que os prompts
anteriores não transportaram.** Verifica-as antes de usares qualquer coisa dos
lados oriental ou hídrico:

- **A L8 vale com 251 cenas e SEM a leitura de «recuperação» do N3.** A
  amplitude da referência — o denominador — perde metade de si própria em 2024 e
  outra vez em 2026 (0,601 · 0,590 · 0,265 · 0,538 · 0,277). A subida do N3 de
  0,10 para 0,65 **é o denominador a cair**. Sobrevive o **0,10 de 2025** e a
  **monotonia** do foco OESTE.
- **A L7 leva dois acertos:** 0,61 ha a **60,0 m** e 0,55 ha a **74,7 m** (áreas
  e distâncias trocadas no texto publicado), e a mancha de 0,55 ha tem altura
  mediana **1,466 m**, abaixo do limiar de 1,5 m. «Não é chão» aguenta;
  «pérgola completa» não.
- **A leitura «os focos perdem água antes de verdura» (NDMI contra NDVI) está
  RETIRADA por inteiro**, e com ela a inferência hidráulica ou vascular que dela
  derivava. Não a uses e não a ressuscites. Ver a secção dos rejeitados.
- **O viés de calibração do Sentinel-2C não existe nos dados, e nunca existiu.**
  Quatro medições emparelhadas, de quatro corridas independentes, dão **≈ zero**
  (A: sem viés em NDVI; C: +0,0007/+0,0045; céptico: +0,000/+0,004;
  patologista: +0,012). **O valor de −0,048 que circulou por toda a cadeia não
  vem de nenhuma delas:** vem de um degrau de nível medido **fora do pomar**,
  onde sensor e ano estão confundidos. **Cai a segunda metade da L5** — «o viés
  do S2C explica quase toda a queda da referência». **A primeira metade
  mantém-se.** Fonte: `_MULTIVERSO\ADVERSARIO_H1.md`.
- **O voo LiDAR de 06-07-2025 cai DENTRO da janela em análise.** Não distingue
  «nunca teve pérgola» de «teve até Julho de 2024». **A metade oriental de L3
  não é teste de nada sobre o lado oriental**, e a margem de B7 que a ela
  encosta fica enfraquecida. **A metade ocidental é decisiva:** confirma que o
  foco ocidental, v8/B2, é copado vivo — 2,25 m, 90,2 %.

### Da C0, `CAMADA_0_REVISAO_R2.md` (substitui o certificado da C0)

**G1** AOI (529950, 4654600, 531950, 4655600), EPSG:32629, grelha de 10 m,
200×100. *(exacta)*

**G2** `pomar` = **30,31 ha**, da ortofoto por periodicidade de compasso
(5,0 m). *(±10 m no contorno)*

**G3** Eixo: azimute **70,3°**, comprimento **1458 m**. *(dois caminhos)*

**G4** `pomar` 30,31 ha · referência sistemática **1,10 ha / 110 células** ·
`zona0` 2,02 ha. **`manchaW` não existe como máscara.**

**G5** Conjunto operativo: `sentinel\masks_geograficas.json`.

**G6/G25** **A referência sistemática DESCE**: 0,8884 → 0,8425, **−0,00395/ano**.

**G19/G36** O bloco a sudoeste é o **B1**: v1-v5, **9,01 ha**, a **526 m do
corpo principal**. Porta-enxerto **Summer Kiwi** nas v2-5, sobre-enxertado com
Enza Gold em 2016 e Erica por volta de 2020; a v1 e **todo o corpo principal**
são pé franco de **Erica**. **É o único contraste de porta-enxerto do caso.**
*(Duas caixas de coordenadas circulam para o B1 e duas distâncias — ver a lista
das divergências declaradas.)*

**G24** Quarentena da AOI 528400–529400: tecido urbano de Valença.

**G26** **Não existe controlo externo de kiwi contemporâneo neste aluvião.**
Varrimento de ~3 km, 13 candidatos, 11 falsos positivos. Com dados de satélite
este caso **não distingue** «esta parcela declina» de «todo o kiwi deste aluvião
fez isto». **Não é lacuna de busca; é resultado.**

**G32** **Houve rede, e só no B1**, no período do Enza Gold. Datas por dar.

**G34** Os focos identificam-se por coordenada (tabela acima). **A linha
«amostras» desta tabela está resolvida a meio:** ver a arbitragem em C4 §0.

**G35** As válvulas 6-17 estão colocadas por área acumulada. Banda contígua
**27,30 ha** (recalculada e confirmada pela C4); total da tabela 44,93 ha.
Posições em `ganfei_s2\valvulas_por_area.json`. Fora da banda, **oito parcelas
soltas (17,66 ha) têm área e não têm posição — o B1 entre elas.**

### Da C1, `CAMADA_1_CERTIFICADO.md`

**S3.** O foco ESTE é o ponto alto e o OESTE o ponto baixo: 6,638 m (percentil
30) contra 7,842 m (84), diferença **+1,204 m**, confirmada por GLO-30.
*(±0,06 m)*

**S4.** É um **alto local**. *(±0,10 m)*

**S5.** **Os focos não diferem em inclinação.** 0,336° / 0,406° / 0,427°,
p = 0,20; tudo abaixo de 0,5°. **«Encosta» é falso.** *(p declarado)*

**S6.** **A posição hidráulica dos dois focos é oposta.** Altura sobre a
drenagem 0,130 / 0,150 / 0,353 m; distância à drenagem **13,4 / 23,6 / 55,8 m**.
**O foco OESTE recebe água concentrada; o ESTE não recebe nenhuma.**

**S8.** **O B3 tem o solo mais pobre da exploração** — mínimo de nove boletins
em cinco de sete parâmetros. *(n = 1 boletim — ver S9)*

**S9.** **Um boletim não caracteriza um bloco.** Dentro do B1, três sub-parcelas
dão CaO **314, 439 e 4700** mg/kg. **Nenhuma diferença química entre blocos
abaixo de um factor de 2 é interpretável com estes dados.**

**S10.** **O bloco do foco OESTE está confirmadamente carente de cálcio, por
duas matrizes.** Solo 264 e 505 mg/kg CaO; folha Junho/2026 **Ca 2,2 % contra
referência 3–4,7 %, «Baixo»**. **Não existe análise foliar para o B3.** *(A C3
retirou o contraste de CaO ENTRE blocos; a S10 sobrevive inteira — são
afirmações diferentes. Não as arrumes juntas.)*

**S12.** **O chão lavrado de 2021 (1,67 ha) está 60 % dentro do foco ESTE e 0 %
no foco OESTE e na referência.** *(±1 célula)*

**S13.** **A distinção física daquele chão é anterior a 2021.** Em VV está 1,2 a
3,5 dB abaixo da referência em **todos os dez Invernos desde 2016-17**.

**S15.** **No radar, o foco ESTE está sempre abaixo da referência e o OESTE
nunca esteve — até ao Inverno de 2025-26**, em que cai para −1,107 dB (órbita
125) e −0,775 dB (147). *(±0,25 dB)*

**S16.** **A precipitação é inútil como discriminante espacial.** Nenhum produto
resolve 496 m.

**S17.** **A linha térmica fica retirada.** Acoplamento ΔT–ΔNDVI de −0,925 no
controlo interno **fora** do pomar: é genérico da superfície. **Não ressuscitar
sem LST nocturno ou temperatura de solo medida.** *(Caiu o instrumento, não a
causa — ver o livro-razão, ABI-07.)*

**S18.** **O pomar é duas vezes mais plano que o envolvente** (p = 3,2e-10).
Compatível com terraplanagem; **não é prova**.

**S19.** **A rugosidade a 25 m do foco ESTE excede a referência dentro da mesma
campanha de voo** (+0,0379 m, p = 1,3e-18); a do OESTE não (p = 0,058).

**S20.** **Os dois focos têm substratos opostos em todas as variáveis que os
separam.**

### Da C2, `CAMADA_2_CERTIFICADO.md`, com as retiradas do adversário aplicadas

**V1.** Défice = **NDVI abaixo da referência sistemática da própria data menos
0,05, com abertura 2×2**.

**V2 (corrigida por R3 e pela adenda).** **O acontecimento é de 2025-2026 e
atinge os dois focos na mesma janela.** Em **fosso à referência da mesma data**
— a moeda operativa — os degraus são **+0,0720 (foco OESTE)** e **+0,0585 (foco
ESTE, na metade do disco com altura mediana ≥ 0,5 m)**, enquanto o resto do
pomar **fecha** o fosso. **Os números −0,1426 e −0,1439 em nível absoluto estão
RETIRADOS.** *(A etiqueta «restrito a copado» foi retirada pela R3; o número
mantém-se. O corte de 0,5 m cai a 0,03 m da mediana da unidade que parte.)*

**V3.** **NDVI e SAR datam o mesmo acontecimento nos mesmos sítios.** ρ = **+0,57
a +0,60** sobre 81 mosaicos de 60 m de geometria pura, permutação p < 0,0002.
*Por declarar:* o Inverno de **2016-17** dá ρ = +0,314, p = 0,0043. **A frase
«retirando os mosaicos a menos de 130 m, sobrevive» está em NÃO TESTÁVEL.**

**V4 (reescrita por R1).** A **válvula 8 tem a maior anomalia negativa de VV do
Inverno de 2025-26 por um factor de cinco** (−0,660 dB contra −0,135). **É UM
instrumento, não dois.** Spearman sobre as doze válvulas: ρ = +0,476,
**p = 0,118**.

**V5.** **Os 8,08 ha em défice de 2017 e os 7,86 de 2026 não são o mesmo
objecto.** Ao limiar 0,25 são 5,37 e 0,32 ha. **O acontecimento de 2025-2026 é
extenso e moderado. Não uses 2017 como linha de base de saúde.**

**V6.** **Pelo menos 5,37 ha do polígono não tinham estrutura de fileira em 2010
nem em 2012, e tinham-na em 2021.** Data de plantação por dar.

**V8.** **3,58 ha passam a regra M2** — declínio novo sobre terreno
comprovadamente são. **O número defensável é 2,60 ha, com 3,58 como tecto.**
Repartem-se em **2,02 ha a 24 m do foco OESTE** e **1,41 ha em três manchas do
foco ESTE**. **Taxa de base:** o défice de 2026 é **2,68×** mais provável sobre
terreno com histórico (45,8 %) do que sobre terreno são (17,1 %).

**V9.** **A grandeza operativa é a magnitude, não a fracção.**

**V10.** **O nível absoluto não pode carregar uma afirmação sobre o pomar
todo.** As duas cenas de NDVI mais baixo são as duas únicas do S2C.

**V11.** **A barra de erro da série é ~3 ha e vem medida.** O salto de 2024
(2,91) para 2026 (7,86) é de 4,95 ha e sobrevive. **A fenologia não é a
explicação.** *(V11 depende inteiramente da cena de 2019-09-02, que a R2 G10
mandou excluir e a C2 repôs. A C0 nunca a re-certificou.)*

### Da adenda de LiDAR — **ganha sobre o certificado da C2**

**L1.** Voo LiDAR DGT de **06-07-2025**, datado pelo tempo GPS dos pontos.
Referência 2,34 m / 99,2 % acima de 1,5 m; terreno lavrado 0,09 m / 15,2 %.
*(Sem script em disco: o cálculo do tempo GPS não existe como ficheiro.)*

**L2.** **3,77 das 30,31 ha do polígono tinham altura mediana inferior a 0,5 m
nessa data.** *(A etiqueta «sem pérgola / chão» foi RETIRADA: o IFAP declara
KIWI em 65 % dessa área. Diz «altura mediana < 0,5 m», nunca «chão».)*

**L3.** O **foco OESTE é copado vivo** (2,25 m, 90,2 %); **metade do disco ESTE
não é** (0,47 m, 50,2 % das células abaixo de 0,5 m).

**L4 — RETIRADO. L6 — RETIRADO.** Não os uses, em nenhuma forma. Não uses «o
degrau sanitário parte de zero» nem «o sinal está onde estão as plantas e não
está onde elas não estão».

**L5 (só a primeira metade).** Em fosso, os degraus são **+0,0720 (OESTE)** e
**+0,0585 (ESTE)**, e não −0,1426 e −0,1439. A diferença face aos números
publicados é a referência a cair. **A segunda metade — «e o viés do S2C explica
quase toda a queda da referência» — está RETIRADA.** Cai a explicação, não a
medição.

**L7 (com os acertos de W2).** As manchas de declínio novo junto ao foco ESTE
são **0,61 ha a 60,0 m e 0,55 ha a 74,7 m** (mais 0,25 ha a 166 m), com 71–92 %
acima do limiar; **a de 0,55 ha tem altura mediana 1,466 m**. As 3,58 ha totais
lêem 2,17 m e 79,9 %.

**L8 (na forma corrigida).** Amplitude sazonal relativa à referência, **251
cenas** de 2022 a 2026: o foco OESTE desce monotonamente **0,97 → 0,95 → 0,76 →
0,54 → 0,30**; o núcleo N3 cai a **0,10 em 2025**. **A «recuperação a 0,65 em
2026» está retirada** — é o denominador a cair. O resto do pomar fica em
0,97–1,05.

**Aviso que acompanha tudo isto:** a partição de altura **vale a 06-07-2025 e é
hipótese depois disso** — e também **antes**: classifica o défice de 2017 com
uma medição de 2025. **Fecha-se com um segundo voo, ou com uma visita. Não com
mais análise.**

### Da C3, `CAMADA_3_CERTIFICADO_R2.md` — **a revisão, não o certificado**

**B1.** A fonte é o `Registo Principal` do livro PT, com **221 registos**. O
`Master Log` EN é o mesmo livro. *(instrumento: o `Value`, que diverge em 9 de
212 pares)*

**B2.** **111 registos têm posição na banda contígua e 110 não têm.** Dos 110:
53 sem posição declarada, 40 no B1, 16 do pomar espanhol, 1 ficha de produto.
*(±10 m; 24 dos 111 são inferidos; **sem instrumento independente**)*

**B3 — na forma que a C4 corrige (ver §0 e a linha CORRIGIDO da C4).** Das 20
linhas organismo × matriz, **2** foram ensaiadas numa unidade colocada, **15**
têm algum lugar declarado, e **13 assentam numa só amostra composta** *(o campo do JSON — `linhas_com_lugar_mas_sem_par_de_comparacao` — diz **10**; o 13 soma-lhe as três linhas cuja segunda fonte é o material espanhol de Ribadumia, que está rejeitado. O argumento é bom e não estava escrito: fica escrito aqui. **As três linhas somadas são precisamente as que carregam os resultados negativos.**)*. A folha
declara a convenção: «célula em branco = esse organismo **não foi testado**
nessa amostra (não é o mesmo que um resultado negativo)».

**B5.** **Nenhum dos 221 registos nomeia a válvula 8.** Os rótulos do B2 são
`B2 - V7` e variantes — **51 registos, todos na v7**. **38 das 325 células da v7
(11,7 %, 0,38 ha) estão dentro do disco de 90 m do foco OESTE, e a distância
mínima é 53 m.** **Lê-se «nenhum documento nomeia a v8», nunca «a v8 nunca foi
amostrada».**

**B6.** **O esforço não está distribuído pelo défice: está concentrado.** 45,9 %
dos registos colocados numa unidade de 3,25 ha (v7); oito das doze válvulas com
zero. **Há selecção total, por conveniência operacional.**

**B7.** **A única amostra biológica do lado oriental é um composto de bloco
sobre 9,92 ha, dos quais 16,3 % são chão lavrado** (v13: 22,6 %; v14: 13,8 %).
**A contagem de 28/37 não pode ser atribuída a plantas do foco ESTE.**

**B8.** **As quatro ITS não são comparáveis entre si.** Riqueza, Simpson e
Shannon seguem a profundidade a ρ = +1,000 (p exacto 0,083). **A diversidade não
entra em nenhuma conclusão.**

**B9.** **A *Rosellinia* tem duas amostras, e o negativo molecular é ANTERIOR por
catorze meses.** Campo: 2026-08-04, **raiz**, uma planta arrancada, local não
especificado, macroscópico, **amostra não enviada**. Molecular: 2025-06-06,
**solo**, sem posição própria. **Não é a mesma planta, não é a mesma matriz, e
não é depois.**

**B10.** **16,4 % das células da referência (18 de 110) caem dentro dos discos
de 90 m dos dois focos.** Contaminação **geométrica**. Retirá-las desloca a
mediana **+0,0133** em 2026 e menos de 0,0025 em todas as oito anteriores.
Segunda via: a **média** cai 0,0548 contra 0,0219 da **mediana**, e a distância
entre as duas passa de −0,0011 (2024) a −0,0340 (2026). **O sentido é
conservador: limpar a referência torna o acontecimento maior.** *(margem **não
declarada**)*

**B11.** **Não há linha de base biológica.** Nenhuma amostra é anterior ao
acontecimento. *(A C4 corrige: existe agora **uma** amostra com zona declarada,
de 2025-06-06, contemporânea do arranque. Continua a não haver base.)*

### Da C4, `CAMADA_4_CERTIFICADO.md` — **a tua camada imediatamente abaixo**

**D1.** **A composição do défice de 2026 separa os dois focos.** Na **v8**
(contém o foco OESTE), **93 % do défice de 2026 é declínio novo** e **0 % era
chão lavrado em 2021**; nas **v13/v14** (contêm o foco ESTE), **36 % e 34 %**,
sobre **22,6 % e 13,8 %** de chão lavrado. Por permanência, no disco de **120 m**:
**3,5 %** do défice do foco OESTE tem histórico anterior a 2025, contra
**52,4 %** do foco ESTE. *Instrumento:* tabela do gestor × ortofoto 2021 ×
Sentinel-2. *Margem:* ±10 m; **disco de 120 m, não 90**.

**D2.** **Há um acontecimento recente partilhado, e cai sobre dois terrenos com
histórias opostas.** Liga-o a **48 %** do défice do foco ESTE, não aos outros
52 %. *Margem:* os dados **não separam degrau de declínio a acelerar**.

**D3.** **O argumento geométrico tem força na v8 e só na v8.** A taxa de base
(2,68×) faz de «proximidade a um foco» quase sempre «proximidade a défice
antigo»; **a v8 é o único sítio onde esse confundente não existe**. **2,60 ha
defensável, 3,58 ha tecto, os dois limites inferiores por D4.**

**D4.** **Toda a magnitude expressa em fosso à referência é um limite inferior,
e a área em défice também.** «O resto do pomar fecha o fosso» **não** quer dizer
«o resto do pomar está são». **E a explicação instrumental que competia com isto
está excluída** — o viés do S2C é ≈ zero em quatro corridas independentes. O que
fica no lugar é medição: a **média** da referência cai **0,0548** contra
**0,0219** da **mediana**, com o afastamento entre as duas a alargar **31×** de
2024 para 2026 — **um subconjunto de células da referência a colapsar, e não é
sensor**. *Margem:* **direcção certificada, dimensão não** (não há bootstrap); e
o efeito do S2C sobre as **estatísticas de cauda** nunca foi medido.

**D5.** **O *M. hapla* está excluído como explicação do contraste entre os
focos, e não está excluído como stress de fundo.** ρ(défice, solo) = **−0,40**,
ρ(défice, raiz) = **−0,80** sobre 4 unidades; contagem mais baixa no bloco mais
afectado; **a mais alta (250/200 cc) no B1, que não tem posição.** *Margem:*
n = 4, uma data, **nenhum ρ significativo**.

**D6.** **A matriz de diagnóstico tem uma só coluna útil.** Das 20 linhas: **13
assentam numa única amostra composta**, 2 têm contraste multi-unidade, 5 não têm
fonte de Ganfei. **Dos 5 resultados NEGATIVOS, 4 vêm da mesma amostra e 1 só
existe em Espanha: nenhum negativo deste caso vem de uma amostra comparável.**

**D7.** **Nove presenças de patogénio estão localizadas no foco ocidental, e
nenhuma é causa.** Quatro de madeira (*F. cerealis*, *F. equiseti*,
*F. oxysporum*, *N. parvum*) e cinco de raiz (*Ceratobasidium*, *F. oxysporum*,
*F. solani*, *N. parvum*, *Globisporangium intermedium*), do informe **331/2025**
(= amostra «Kiwi 1000»), colheita **2025-06-06**, situada por **testemunho de
tipo 1** no lado oeste do maior vazio circular. **Nenhuma foi alguma vez
procurada em nenhum outro ponto deste pomar.** *Margem:* **zona, não ponto**;
amostra **composta** sobre matéria desconhecida; **n = 1**; **sem par de
comparação**.
**⚠ Passa como PRESENÇA LOCALIZADA e nada mais.**

**D8.** **Nenhum ensaio bacteriano ou viral foi alguma vez feito neste caso.** Os
15 taxa são fungos, oomicetas e um nemátode. A ***Pseudomonas syringae* pv.
*actinidiae* nunca foi procurada**, em nenhuma matriz, em nenhuma data.

**E o livro-razão inteiro**, que é o produto principal da C4:
`SAIDA_C4\c4_razao_exclusoes.csv` — **59 causas candidatas**, das quais **41 NÃO
TESTADAS**, 7 excluídas, 4 excluídas só numa zona e numa data, 5 sustentadas, 2
inconclusivas. **Lê-o inteiro antes de desenhares fosse o que fosse.**

> **NÃO é «a lista do que ninguém procurou», e a etiqueta não é de confiar.** O
> adversário da C4 verificou-as e concluiu que **pelo menos dezasseis das
> quarenta e uma estão mal rotuladas**, e que para **nove delas o inverso é
> verdade: foram procuradas e encontradas.** «NÃO TESTADA» está a fazer o
> trabalho de três coisas diferentes — nunca ensaiada, ensaiada num só sítio sem
> comparação, e ensaiada e positiva sem replicado.
>
> **Primeira coisa a fazer, antes de qualquer desenho:** re-derivar o estatuto de
> cada uma das 41 **a partir dos campos de evidência da própria linha**, não da
> etiqueta, e publicar a re-etiquetagem. Se não o fizeres, vais orçamentar
> **primeiros ensaios onde o que falta é um segundo ponto de comparação** — que
> é o erro mais caro que esta camada pode cometer.

---

## O que ficou por resolver abaixo de ti

Por ordem de quanto te afecta.

1. **Local contra regional, e é a maior de todas.** G26 diz que com satélite
   este caso **não distingue** «esta parcela declina» de «todo o kiwi deste
   aluvião fez isto», e que isso é **resultado**. `_MULTIVERSO\AGREGACAO_H2.md`
   H2-4 acrescenta um dado positivo — outra exploração de kiwi a **8,1 km**, com
   **76,22 ha** declarados (ENT 297313), com **colapso em degrau em 2024** —
   mas **uma corrida, uma medição, não verificado independentemente**. **Nenhuma
   medida que recomendes pode assumir que a causa é local.**

2. **A matriz tem uma coluna.** Não existe, em todo o caso, um segundo ponto
   ensaiado para nenhuma das treze linhas do informe 331/2025 — nem doente, nem
   são. **É a tua primeira tarefa e não é opcional.**

3. **O registo de operações do B2 e do B3 em 2024-2026** — arranque,
   replantação, poda severa, substituição de pérgola, falha de rega, com data e
   sector. **Pedido por duas sessões independentes e ainda por fazer.** Sem ele
   não se sabe se a amostragem de 2026 caiu sobre plantas adultas, sobre
   replantação, ou sobre chão — e **nenhum resultado de 2026 é interpretável**.

4. **O T3 do adversário da C2 nunca correu.** Era **condição de arranque da C3**:
   apontar a prominência de pérgola à ortofoto de **2025**, sobre as 3,58 ha de
   `c2_05_novo_m2.npy`, o disco OESTE, `zona0 & ~nu2021` e a referência. Não
   existe `c2_12_prom_2025.npy` e a lista `ORTOS` de `c2_12_pergola_2012.py`
   continua sem 2025. **É o teste que distingue copado em declínio de copado
   arrancado, replantado ou re-armado.** O LiDAR substitui-o **numa só data** e
   não cobre 2026.

5. **A série Landsat da referência nunca entrou em nenhuma lista fechada.** É o
   **único instrumento verdadeiramente externo** que este caso produziu — outra
   agência, outro sensor — e mede a referência a cair 0,888 → 0,874 → 0,862.
   Está em `_VALIDADE_GESTAO\landsat.json`. **Sem ela, D4 certifica direcção e
   não dimensão.**

6. **Replantação contra chão limpo mantido, no N3 (E531068 N4655145).** As duas
   leituras são mutuamente exclusivas e o material não as separa; a que os
   números favorecem é a segunda. **Fecha-se com um segundo voo ou uma visita,
   não com análise.**

7. **As quatro ITS ISFBV0314–17 continuam em NÃO RESOLVIDO.** O gestor **não
   sabe** de onde vieram, e **os quatro PDF não existem nesta máquina**
   (verificado por busca em toda a árvore). **Documento indisponível, não
   informação inexistente.**

8. **Sobre o que foi composta a amostra 331/2025?** Ninguém perguntou. Decide se
   D7 vale para uma planta ou para meio hectare.

9. **A G10 nunca foi re-certificada** (condição 1 do adversário da C2), e a V11
   depende inteiramente da cena de 2019-09-02.

10. **Nove cenas no código, dez no certificado da C2.** Declarado por três
    camadas, resolvido por nenhuma. **Não o resolvas: declara-o.**

11. **A margem de B10 não existe** — não há bootstrap.

12. **A paisagem envolvente e a referência dizem coisas incompatíveis.** Uma
    corrida imprimiu que a **vegetação envolvente caiu 0,075 entre 2024 e 2026 —
    o dobro da queda do bloco** — e nunca juntou os dois números; outra mediu
    que a sua referência **não se move** (−0,0070, p = 0,54). **As duas não
    podem estar as duas certas.** **Se a paisagem caiu o dobro do bloco, o
    enquadramento do caso inverte-se** e a pergunta regional (item 1) deixa de
    ser secundária. Não a resolvas por escolha: reconcilia as duas corridas
    sobre a mesma máscara e a mesma janela, **e declara qual é o objecto
    “envolvente” em cada uma**.

12-b. **O efeito do S2C sobre as estatísticas de CAUDA nunca foi medido.** O
    viés sobre o **nível** está excluído. Mas um degrau de sensor não é uniforme
    em NDVI, e **todas as grandezas-título desta cadeia — área em défice,
    dispersão, fracção, M2 — são estatísticas de cauda**. São **três linhas**
    sobre ficheiros que já estão em disco: desvio-padrão e assimetria das
    células **fora** do pomar nas duas cenas S2C.

13. **Nenhum ponto do B1 tem posição**, incluindo a fronteira do porta-enxerto,
    que é o único contraste do caso. **H2b está INCONCLUSIVO** e resolve-se
    pedindo **o esquema de válvulas do B1**, não calculando. E a contagem de
    nemátodes mais alta de todas está lá.

14. **Não há data de plantação** para as 5,37 ha de V6, e o enchimento de uma
    pérgola nova vale **+0,06 a +0,11 NDVI/ano** — várias vezes o efeito
    procurado.

---

## O que foi rejeitado, e não podes usar

Isto é tão importante como o que passa.

- **«Nenhum organismo está onde o padrão está»**, em qualquer forma. **Nove
  organismos estão onde o padrão está, e isso continua a não excluir nada.**
- **Promover qualquer um desses nove a causa.** Uma amostra, composta, um sítio,
  um dia, sem par de comparação. **Um patogénio encontrado no foco e nunca
  procurado fora dele não é prova de que causou o foco.** É a configuração do
  *P. sojae* com dados melhores e com a localização certa.
- **Ler os quatro negativos do 331/2025 (*Armillaria* raiz e solo, *Rosellinia*
  solo, oomicetas solo) como exclusões para o pomar.** Valem numa zona, numa
  data, numa matriz, n = 1.
- **Ler o negativo de oomicetas em SOLO como exclusão de *Phytophthora*.** A
  mesma amostra dá **positivo** a um oomiceta na **raiz**.
- **Qualquer exclusão construída sobre o informe 240/2023** (Kiwi Atlántico,
  Ribadumia). **Armadilha activa:** o talhão espanhol chama-se **B-3/C-3** e o
  bloco do foco ESTE chama-se **B3**.
- **Promover o *Phytophthora sojae* do registo 79.** Notes de um relatório sem
  parcela associada, noutra freguesia.
- **Ler factos do N3 como factos do foco ESTE.** 95,2 m, fora do disco.
- **«A recuperação do N3 a 0,65» como prova de replantação.** Denominador.
- **A leitura água-antes-de-verdura (NDMI×NDVI) e a inferência hidráulica ou
  vascular que dela deriva.**
- **«O resto do pomar está são porque fecha o fosso.»** Ver D4.
- **A linha térmica diurna como sinal** (S17). **Não a ressuscites.**
- **O viés de calibração do S2C de −0,048 NDVI, em qualquer uso**, e em
  particular como explicação da queda da referência. Não existe nos dados.
- **A metade oriental de L3 como teste do lado oriental.** O voo está dentro
  da janela em análise.
- **«O foco ESTE está numa encosta»** (S5). **«A lavra de 2021 mudou aquele
  solo»** (a assinatura já lá estava em 2016-17). **«O foco ESTE declina desde
  2020» como afirmação sobre plantas** (V2).
- **Qualquer série do B1 e qualquer comparação de nível de NDVI entre o B1 e o
  corpo principal.** Três tentativas, três contaminações.
- **Qualquer percentagem de cobertura tirada de ortofoto** entre épocas. **A
  curva em U do défice como objecto único**, e **2017 como linha de base de
  saúde** (V5). **O IoU = 0,29.** **«A v8 destaca-se nos dois instrumentos»** —
  um instrumento. **A riqueza de ASV das ITS como grandeza biológica.** **A
  subida de 41 para 82 dos Becrop como recuperação.** **A «válvula 27»**, que
  não existe nos dois livros. **A margem «±0,001 NDVI» de B10.** **As contagens
  «23 do défice» e «19 do M2» dentro da referência.** **`lidar\bacia.json`.**
- **A «podredumbre radicular» dos Becrop como instrumento independente.** A
  categoria **existe** (Notes dos registos 79 e 86); o que cai é a etiqueta de
  independência — são duas anotações do mesmo compilador.
- **L4, L6, e a etiqueta «pérgola / chão»** da adenda de LiDAR, em qualquer
  formulação.

---

## Materiais

Só estes. Não tens dados brutos: a tua matéria-prima são os certificados e os
JSON de saída, que existem para poderes citar o cálculo em vez do dossiê.

```
Downloads\_VALIDACAO_CAMADAS\
  CAMADA_0_REVISAO_R2.md        + suplemento G34-G37
  CAMADA_0_ADENDA_CONTROLO.md   o controlo externo que nao existe
  CAMADA_1_CERTIFICADO.md       S1-S20
  CAMADA_2_CERTIFICADO.md       V1-V11
  CAMADA_2_ADVERSARIO.md        R1-R4, W1-W7
  CAMADA_2_ADENDA_LIDAR.md      L1-L8 — L4 e L6 RETIRADOS; le o aviso no topo
  ADVERSARIO_2026-08-29.md      retira L4/L6 e a etiqueta; corrige L7 e L8.
                                LE-O ANTES da adenda.
  CAMADA_3_CERTIFICADO_R2.md    B1-B11 — GANHA sobre o certificado da C3
  CAMADA_3_ADVERSARIO.md        R1-R8, W1-W9
  CAMADA_4_CERTIFICADO.md       D1-D8, a arbitragem do «Kiwi 1000», e o
                                livro-razao
  REFERENCIAS_MULTIVERSO.md
  SAIDA_C1\ SAIDA_C2\ SAIDA_C3\ SAIDA_C4\
Downloads\_MULTIVERSO\AGREGACAO_H2.md      H2a SUPORTA · H2b INCONCLUSIVO
Downloads\_MULTIVERSO\ADVERSARIO_H1.md     retira o vies do S2C e a metade
                                           oriental de L3. LE-O ANTES da
                                           agregacao da H1.
Downloads\_VALIDADE_GESTAO\                os scripts da adenda + REGISTO.md
Downloads\ganfei_s2\valvulas_por_area.json
Downloads\ganfei_s2\sentinel\masks_geograficas.json
```

**Podes agora abrir `ganfei_s2\_pacote_cowork\`** — contém a árvore de decisão e
material da tua camada, e foi vedado às anteriores precisamente para chegar
intacto até aqui. **Lê-o depois de leres o livro-razão, nunca antes:** se o
leres primeiro, desenhas a amostragem para as causas que já estão na árvore, que
é a forma exacta do erro da máscara derivada do sinal.

**Não modifiques nada em `Downloads\ganfei_s2\` nem em `_VALIDADE_GESTAO\`.**

---

## Tarefas

1. **O desenho de amostragem, e a restrição que o determina.** A matriz de
   diagnóstico tem **uma coluna**: treze das vinte linhas descrevem uma amostra
   composta, num sítio, num dia (D6, D7). **A primeira coisa que qualquer
   amostragem tem de produzir é a coluna que falta** — as mesmas linhas, no
   mesmo laboratório, no mesmo método, num terreno que a C2 estabeleça como
   **comprovadamente são**, e num terreno oriental. Nomeia as unidades por
   **coordenada**, diz quantos pontos, e diz **o que farias com um positivo e o
   que farias com um negativo antes de os teres** — se as duas respostas forem a
   mesma, o ponto não vale a pena. Saída: `SAIDA_C5\c5_amostragem.csv`.

2. **As 41 linhas NÃO TESTADAS, triadas — depois de re-etiquetadas.**
   `c4_razao_exclusoes.csv` tem 41 causas rotuladas NÃO TESTADA, e **a etiqueta
   está errada em pelo menos dezasseis; nove foram procuradas e encontradas**
   (ver o aviso no bloco do livro-razão). **Re-deriva o estatuto de cada uma a
   partir dos campos de evidência antes de ordenar seja o que for**, e publica a
   re-etiquetagem em `SAIDA_C5\c5_reetiquetagem.csv`. Só depois:
   **não as podes procurar todas.** Ordena-as por
   *consequência × custo*, e diz explicitamente quais é que decides **não**
   procurar e porquê. **Uma causa que decides não procurar continua a ser uma
   causa não excluída, e o relatório tem de a levar assim.** Nota que a linha
   BIO-24/25 — bactérias, e a **PSA** — tem custo baixo e consequência alta, e
   nunca foi tocada.

3. **A pergunta que decide se este caso pode ser fechado: local ou regional?**
   G26 diz que o satélite não distingue e que isso é resultado; H2-4 dá um
   candidato a 8,1 km com colapso em 2024, não verificado. **Diz o que é preciso
   para fechar isto e diz o que acontece ao relatório se não for feito.** Não é
   retórico: se for regional, quase todas as medidas de parcela que se possam
   recomendar são inúteis.

4. **As quatro acções que não são análise, e o que cada uma fecha.** Pela ordem
   que a C4 estabeleceu: enviar a amostra de raiz de *Rosellinia* já colhida em
   2026-08-04 e nunca enviada; o registo de operações do B2 e do B3 em 2024-2026;
   os originais ISFBV0314–17 e o informe 331/2025; e o esquema de válvulas do B1.
   **Duas delas já têm pedidos anteriores por cumprir.** Diz quem pergunta, a
   quem, e o que muda em cada uma das duas respostas possíveis.

5. **A árvore do Pilar D.** Constrói-a **contra o livro-razão**, não contra a
   lista de causas investigadas. Cada ramo tem de nomear a linha do livro que o
   sustenta e o estatuto dela. **Um ramo que assente numa linha NÃO TESTADA tem
   de o dizer no próprio ramo.**

6. **O que o relatório pode afirmar, e o que não pode.** Escreve as duas listas.
   A segunda é mais importante e vai ser mais longa. Inclui explicitamente: que
   a etiologia **não está estabelecida**; que **toda a magnitude em fosso é
   limite inferior** (D4); que a distinção local/regional **não está feita**; e
   que os nove organismos localizados são **presenças**, não causas.

7. **As medidas.** Separa as que valem **independentemente da causa** (e há-as —
   nutrição, drenagem, calendário de operações registado) das que **dependem de
   um diagnóstico que ainda não existe**. **Não recomendes nenhuma medida
   dirigida a um dos nove organismos de D7.**

8. **Se a decisão não fechar, di-lo.** «O material não sustenta uma recomendação
   dirigida» é saída válida e obrigatória. O protocolo trata a dúvida assinalada
   como resultado; uma recomendação inventada custa dinheiro a alguém.

---

## Onde já se errou nesta matéria

- **Uma máscara derivada do sinal que se ia medir.** Foi o erro central e passou
  por quatro auditorias. **O equivalente na tua camada é desenhar a amostragem a
  partir da árvore de decisão que já existe**, e depois concluir que a causa é um
  dos ramos que estavam lá. Lê o livro-razão antes do `_pacote_cowork\`.
- **Um positivo tratado como discriminante.** *M. hapla*, positivo em todos os
  blocos amostrados. **A contagem mais baixa está no bloco mais afectado e a
  mais alta está no bloco sem posição.**
- **Um patogénio atribuído ao corpo em declínio sem posição.** *P. sojae*.
  **Agora há nove patogénios COM posição no foco ocidental, e a tentação é
  maior, não menor.**
- **Nomes de focos trocados.** «Zona 0» significou dois sítios a 500 m um do
  outro durante semanas. **Coordenada sempre.**
- **O «B1» que era Valença.** Uma pergunta de identidade que ninguém fez à
  camada de baixo.
- **Uma frase que liga números certos.** Nenhuma das retiradas dos três
  adversários apagou uma medição; quase todas apagaram a frase.
- **Uma afirmação que não podia falhar.** Antes de escreveres um resultado
  negativo, **verifica que o teste podia ter dado positivo**.
- **Um valor transcrito à mão para dentro de um script, gravado num JSON, e
  depois citado a partir do JSON.** É o mecanismo do «B1». **Lê do ficheiro.**
- **Uma divergência declarada corrigida sem ser investigada.** A C3 chamou erro
  alheio a um factor de 2,5 que era média contra mediana — e ao fazê-lo deitou
  fora uma prova independente do seu próprio achado. **Divergência sem
  explicação é achado, não correcção.**
- **Uma correcção que existe a montante e que o prompt seguinte não transporta.**
  Aconteceu três vezes (L7, L8, a retirada da leitura NDMI). **Antes de usares
  qualquer facto deste prompt, confirma-o no ficheiro que o adversário mais
  recente daquela camada escreveu.**
- **Uma condição de arranque cumprida a meio.** O adversário da C2 pôs T1 e T3
  antes da C3; o T1 correu, o T3 não, e ninguém registou que não. **Se puseres
  uma condição, verifica que foi cumprida antes de a dares por cumprida.**

---

## O que entregar

1. `CAMADA_5_CERTIFICADO.md`, com as cinco secções do protocolo — CONFIRMADO,
   CORRIGIDO, REJEITADO, NÃO TESTÁVEL, PASSA PARA CIMA. **Não há camada acima de
   ti:** a tua secção PASSA PARA CIMA é o que vai para o relatório e para quem
   decide gastar dinheiro. **Sê mais avaro do que qualquer camada anterior.**
   Cada facto leva o certificado e o número que o sustenta, o **instrumento
   independente** (controlo 1) e a margem.
2. `SAIDA_C5\c5_amostragem.csv` e a árvore do Pilar D.
3. A secção **«Nota ao adversário»**, com os pontos que doem e não os que já
   sabes resolver.

Reporta as **quantidades-âncora**: `pomar` 30,31 ha · referência sistemática
1,10 ha / 110 células · banda contígua 27,30 ha · total da tabela 44,93 ha ·
chão lavrado 1,67 ha · **défice de 2026 7,86 ha com abertura 2×2 / 9,47 sem /
10,32 sem e com referência limpa** · declínio novo M2 **2,60 ha defensável e
3,58 tecto, os dois limites inferiores** · **cenas na série 11, de plena estação
9 no código e 10 no certificado da C2 — declara a divergência** · NDVI da
referência 2017-07-02 **0,838 declarado / 0,8898 obtido** e 2026-07-27 **0,886
declarado / 0,8766 obtido**, com o **sinal invertido** · 221 registos, 111 com
posição, 15 taxa, **2 de 20 linhas ensaiadas em unidade colocada, 15 com algum
lugar, 13 assentes numa só amostra (JSON: 10 + 3 de fonte espanhola rejeitada)** · **livro-razão: 59 causas, 41 NÃO
TESTADAS**. E acrescenta as tuas: quantos pontos de amostragem, quantas das 41
decides procurar, e quantas decides não procurar.

**Sobre distâncias, porque já houve nove números para dois objectos.** Sempre
que citares uma distância, diz de que objecto é. Ao foco OESTE: v8 — **34,5 m**
(ponto da válvula, recalculado do ficheiro operativo), 34 (G35), 35 (C1), 43
(C2, centróide de Voronoi), 46 (C3, centróide); v7 — **110,7 m** (ponto da
válvula), 111 (C1), 120 (C3, centróide), 53 (C3, célula mais próxima).
**Nenhum deles é a distância de uma amostra, porque nenhuma amostra deste caso
tem coordenada — incluindo a que agora tem zona.**

Se rejeitares um facto herdado, **pára** e devolve. Escreve o que rejeitaste com
destaque, e **não escrevas nem a árvore nem as medidas antes de a rejeição estar
arbitrada.** A C3 rejeitou, construiu quatro factos por cima, escreveu o prompt
seguinte, e só o adversário travou a cadeia.
