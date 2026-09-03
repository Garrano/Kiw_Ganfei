# Camada 4 — Inferência

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada C4 de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md` e depois `CONTROLOS.md`. Os
controlos 1 e 2 aplicam-se-te por inteiro. O controlo 3 — o adversário — só
corre em C0 e C2, portanto não levas adversário: **escreve na mesma a secção
«Nota ao adversário que não vou ter»**, como a C3 fez, e não a escondas no fim.

A tua camada é a inferência: a matriz de diagnóstico, o livro-razão das
exclusões, o argumento geométrico. És a primeira camada com autorização para
perguntar **porquê**. As quatro abaixo de ti tinham-no proibido, e cumpriram.

**Aviso de nomenclatura, que já custou caro três vezes neste processo.** Nunca
escrevas «OESTE» ou «ESTE» sem a coordenada ao lado. E o **B1** é um bloco
separado a **sudoeste** (E529500 N4654010 a E530054 N4654413) — **não** é o
«foco OESTE». Usa sempre coordenada e válvula.

---

## O que herdas — e só isto

Cinco listas fechadas, por esta ordem de precedência. Trata-as como dados, não
as revalides, e não uses nada que não esteja aqui.

### Da C0, `CAMADA_0_REVISAO_R2.md` (substitui o certificado da C0)

**G1** AOI (529950, 4654600, 531950, 4655600), EPSG:32629, grelha de 10 m,
200×100. *(exacta)*

**G2** O polígono `pomar` tem **30,31 ha**, derivado da ortofoto por
periodicidade de compasso (5,0 m). *(±10 m no contorno)*

**G3** Eixo do pomar: azimute **70,3°**, comprimento **1458 m**. *(dois caminhos)*

**G4** `pomar` 30,31 ha · referência sistemática **1,10 ha / 110 células** ·
`zona0` 2,02 ha. **`manchaW` não existe como máscara.**

**G5** Conjunto operativo de máscaras: `sentinel\masks_geograficas.json`.

**G19/G36** O bloco de ~16 ha a sudoeste é o **B1**: válvulas 1 a 5, **9,01 ha**,
entre E529500 N4654010 e E530054 N4654413, a **526 m** do corpo principal.
Porta-enxerto **Summer Kiwi** nas v2-5, sobre-enxertado com Enza Gold em 2016 e
com Erica por volta de 2020; a v1 e **todo o corpo principal** são pé franco de
**Erica**. É o único contraste de porta-enxerto do caso.

**G24** Quarentena da AOI 528400–529400: é tecido urbano de Valença.

**G26** **Não existe controlo externo de kiwi contemporâneo neste aluvião.**
Varrimento de ~3 km, 13 candidatos, 11 falsos positivos. Com dados de satélite
este caso não distingue «esta parcela declina» de «todo o kiwi deste aluvião
fez isto». **Não é lacuna de busca; é resultado.**

**G32** **Houve rede, e só no B1**, no período do Enza Gold. Datas por dar.

**G34** Os focos identificam-se por **coordenada**:

| | FOCO OESTE | FOCO ESTE |
|---|---|---|
| centro | **E530485 N4655053** | **E530977 N4655117** |
| bloco / válvulas | B2, válvulas **8** (a 35 m) e 9 (98 m) | B3, válvulas **13** (81 m) e **14** (93 m) |

**⚠ A linha «amostras» desta tabela está em NÃO RESOLVIDO — conflito entre
relato e documento, com a precedência por decidir** (C3 R2, §0). Nada nos dois
livros de laboratório coloca as quatro ITS ou o «Kiwi 1000» num talhão, e
**nenhuma frase da G34 sobre esforço de amostragem pode ser usada por ti**. Mas
uma ausência documental não refuta testemunho directo: suspende-o. **Não a
trates como facto excluído.** A pergunta que a resolve está na lista das que
faltam.

**G35** As válvulas 6 a 17 estão colocadas por área acumulada. Banda contígua
**27,30 ha**; total da tabela 44,93 ha. Posições em
`ganfei_s2\valvulas_por_area.json`. **As tabelas de válvulas do
`REGISTO_DE_NOMES.md` e o `valvulas_v6.json` estão desactualizados.** Fora da
banda contígua, oito parcelas soltas (17,66 ha) têm área e **não têm posição**.

### Da C1, `CAMADA_1_CERTIFICADO.md`

**S3.** **O foco ESTE é o ponto alto e o foco OESTE o ponto baixo.** Cota
mediana: OESTE 6,638 m (percentil 30), referência 6,798 m (38), ESTE 7,842 m
(84). Diferença **+1,204 m**, confirmada por Copernicus GLO-30. *(±0,06 m)*

**S4.** É um **alto local**: contra o perfil longitudinal, o ESTE está +0,589 m
acima e o OESTE −0,198 m abaixo. *(±0,10 m)*

**S5.** **Os focos não diferem em inclinação.** 0,336°, 0,406° e 0,427°,
p = 0,20. Toda a parcela abaixo de 0,5°. **Qualquer afirmação de «encosta» é
falsa.** *(p declarado)*

**S6.** **A posição hidráulica dos dois focos é oposta.** Altura sobre a
drenagem: OESTE 0,130 m, referência 0,150 m, ESTE 0,353 m. Distância à
drenagem: **13,4 / 23,6 / 55,8 m**. **O foco OESTE recebe água concentrada; o
ESTE não recebe nenhuma.** *(limiar declarado)*

**S8.** **O B3 (válvulas 12-15) tem o solo mais pobre da exploração**: CaO
< 154 mg/kg, MgO 36,0, K₂O 74,7, P₂O₅ 107, C:N 5,9, pH 5,6 — mínimo de nove
boletins em cinco de sete parâmetros. **É um buraco, não um gradiente.**
*(n = 1 boletim — ver S9)*

**S9.** **Um boletim não caracteriza um bloco.** Dentro do B1, três sub-parcelas
dão CaO **314, 439 e 4700** mg/kg. O mesmo `B2 - V7`, a três meses, dá 264 e 505
**e texturas diferentes**. **Nenhuma diferença química entre blocos abaixo de um
factor de 2 é interpretável com estes dados.** *(declarado)*

**S10.** **O bloco do foco OESTE está confirmadamente carente de cálcio, por
duas matrizes.** Solo em `B2 - V7`: CaO 264 e 505 mg/kg. Folha do mesmo bloco,
Junho/2026: **Ca 2,2 % contra referência 3–4,7 %, «Baixo»**. **Não existe
análise foliar para o B3.** *(leitura directa)*

**S12.** **O chão lavrado de 2021 (1,67 ha) está 60 % dentro do foco ESTE e 0 %
no foco OESTE e na referência.** *(±1 célula)*

**S13.** **A distinção física daquele chão é anterior a 2021.** Em VV está 1,2 a
3,5 dB abaixo da referência em **todos os dez Invernos desde 2016-17**.
*(±0,3 dB)*

**S15.** **No radar, o foco ESTE está sempre abaixo da referência e o foco OESTE
nunca esteve — até ao Inverno de 2025-26**, em que cai para −1,107 dB (órbita
125) e −0,775 dB (147), o maior desvio da série. *(±0,25 dB)*

**S16.** **A precipitação é inútil como discriminante espacial.** Nenhum produto
resolve 496 m. *(±25 mm)*

**S17.** **A linha térmica fica retirada.** O acoplamento ΔT–ΔNDVI é −0,925 no
controlo interno **fora** do pomar: é genérico da superfície. **Não ressuscitar
sem LST nocturno ou temperatura de solo medida.**

**S18.** **O pomar é duas vezes mais plano que o envolvente** (0,0355 m contra
0,0703 m a 60 m, p = 3,2e-10). Compatível com terraplanagem; **não é prova**.

**S19.** **A rugosidade a 25 m do foco ESTE excede a referência dentro da mesma
campanha de voo** (+0,0379 m, p = 1,3e-18); a do OESTE não (+0,0016 m,
p = 0,058). *(±0,008 m)*

**S20.** **Os dois focos têm substratos opostos em todas as variáveis que os
separam.** **Não há uma única variável de substrato em que se pareçam.**

### Da C2, `CAMADA_2_CERTIFICADO.md`, com as retiradas do adversário já aplicadas

**V1.** Défice = **NDVI abaixo da referência sistemática da própria data menos
0,05, com abertura 2×2**. Série de plena estação: **dez** cenas. *(exacta)*

**V2 (na forma corrigida por R3 e pela adenda de LiDAR).** **O acontecimento é
de 2025-2026 e atinge os dois focos na mesma janela.** Em **fosso à referência
da mesma data** — a moeda operativa — os degraus são **+0,0720 (foco OESTE)** e
**+0,0585 (foco ESTE, restrito a copado)**, enquanto o resto do pomar **fecha** o
fosso. **Os números −0,1426 e −0,1439 em nível absoluto estão RETIRADOS.** Até
2024 nenhum foco tem tendência significativa. *(margem: amplitude do patamar de
cada unidade, não ±0,01)*

**V3.** **NDVI e SAR datam o mesmo acontecimento nos mesmos sítios.** Sobre 81
mosaicos de 60 m de geometria pura, a queda de NDVI 2024→2026 correlaciona com
a anomalia de VV do Inverno de 2025-26 a **ρ = +0,57 a +0,60** (permutação
p < 0,0002). Nos nove Invernos anteriores ρ ∈ [−0,22, +0,31]; três placebos dão
−0,05, +0,27, +0,11. **Item por declarar (R2):** o Inverno de **2016-17** dá
ρ = +0,314 com p = 0,0043 — é significativo e está arrumado dentro do intervalo
apresentado como ruído. **A frase «retirando os mosaicos a menos de 130 m dos
focos, sobrevive» está em NÃO TESTÁVEL** até a permutação correr sobre os 56.

**V4 (reescrita por R1).** Sobre a partição documental das doze válvulas, a
**válvula 8 — que contém o foco OESTE — tem a maior anomalia negativa de VV do
Inverno de 2025-26 por um factor de cinco** (−0,660 dB contra −0,135 da
segunda). **É UM instrumento, não dois.** O Spearman entre queda de NDVI e
anomalia de VV sobre as doze válvulas é ρ = +0,476, **p = 0,118**.

**V5 (sem o IoU, retirado por R4).** **Os 8,08 ha em défice de 2017 e os 7,86 ha
de 2026 não são o mesmo objecto.** Ao limiar 0,25 são **5,37 e 0,32 ha**. **O
acontecimento de 2025-2026 é extenso e moderado.** **Não uses 2017 como linha de
base de saúde.**

**V6 (na formulação estreita de W1).** **Pelo menos 5,37 ha do polígono `pomar`
não tinham estrutura de fileira visível em 2010 nem em 2012, e tinham-na em
2021.** A data de plantação continua por dar.

**V7.** **O chão lavrado de 2021 já estava despido em 2017**, no óptico: 166 de
167 células em défice, contra 27 % do pomar. Dois instrumentos, dois princípios
físicos, a mesma conclusão negativa. *(±1 célula)*

**V8 (com a taxa de base de W2).** **3,58 ha passam a regra M2** — declínio novo
sobre terreno comprovadamente são. **O número defensável é 2,60 ha (critério
duro), com 3,58 como tecto.** Repartem-se em **2,02 ha a 24 m do foco OESTE** e
**1,41 ha em três manchas a 62, 72 e 167 m do foco ESTE**. **Taxa de base, que
inverte a impressão:** o défice de 2026 é **2,7 vezes mais provável sobre
terreno com histórico** (45,8 %) do que sobre terreno são (17,1 %).

**V9.** **A grandeza operativa é a magnitude, não a fracção.** Reporta sempre a
magnitude com o nível absoluto ao lado.

**V10.** **O nível absoluto não pode carregar uma afirmação sobre o pomar todo.**
As duas cenas de NDVI mais baixo da série são as duas únicas do S2C.

**V11.** **A barra de erro da série é ~3 ha, e vem medida.** O salto de 2024
(2,91) para 2026 (7,86) é de 4,95 ha e sobrevive. **A fenologia não é a
explicação.** *(±0,4 ha)*

### Da adenda de LiDAR, `CAMADA_2_ADENDA_LIDAR.md` — **ganha sobre o certificado da C2**

**L1.** Voo LiDAR DGT de **06-07-2025**, datado pelo tempo GPS dos pontos e não
pelos metadados. Referência 2,34 m / 99,2 % acima de 1,5 m; terreno lavrado
0,09 m / 15,2 %.

**L2.** **3,77 das 30,31 ha do polígono não tinham pérgola nessa data.**

**L3.** O **foco OESTE é copado vivo** (2,25 m, 90,2 %); **metade do disco ESTE
não é** (0,47 m, 50,2 % das células abaixo de 0,5 m).

**L4 — RETIRADO** pelo `ADVERSARIO_2026-08-29.md`. **Não o uses.** O
teste-placebo «degrau em copado contra degrau em chão» assentava na etiqueta
«pérgola / chão», e essa etiqueta caiu: o limiar operativo era 0,5 m e não os
1,5 m que a adenda justifica, e 0,5 m cai a 0,03 m da mediana do foco ESTE — a
partição cortava a unidade pelo seu próprio centro. **Lê esse ficheiro antes de
tocares em qualquer coisa do lado oriental.** O que sobrevive da adenda é a
**altura medida**, que ninguém retirou (L1, L2, L3).

**L5.** Em fosso, os degraus são **+0,0720 (OESTE)** e **+0,0585 (ESTE)**. A
diferença face aos números publicados é a referência a cair.

**L6 — RETIRADO** pelo `ADVERSARIO_2026-08-29.md`, pela mesma razão que a L4: a
série «restrita a copado» é uma partição pela etiqueta retirada. **Não uses «o
degrau sanitário parte de zero».**

**L7.** As **1,41 ha** de declínio novo junto ao foco ESTE são copado (71–92 %
com pérgola), e as **3,58 ha** de declínio novo total também (79,9 %).

**L8.** Amplitude sazonal relativa à referência, 276 cenas de 2022 a 2026,
**independente do LiDAR**: o núcleo oriental N3, em **E531068 N4655145**, cai a
**0,10 em 2025** — não folia — e recupera a **0,65 em 2026**; o foco OESTE desce
monotonamente **0,97 → 0,95 → 0,76 → 0,54 → 0,30**; o resto do pomar fica em
0,97–1,05.

**Aviso que acompanha tudo o que está acima:** a partição do LiDAR **vale até
06-07-2025 e é hipótese depois disso**. Terreno limpo depois desse dia — já
dentro de 2026 — continua a ser contado como sanitário. **Fecha-se com um
segundo voo, ou com uma visita. Não com mais análise.**

**Facto do parcelário, por confirmar:** o núcleo oriental N3, em E531068
N4655145, lê **0,27 m** de altura — nível de terreno lavrado — e o parcelário
IFAP mostra-o **declarado como KIWI a 10-06-2025**, com a amplitude sazonal a
recuperar em 2026. **Replantação é a leitura coerente, e não está confirmada.**

### Da C3, `CAMADA_3_CERTIFICADO_R2.md` — **a revisão R2, não o certificado**

O certificado original da C3 foi atacado (`CAMADA_3_ADVERSARIO.md`, oito
retiradas) e substituído pela `CAMADA_3_CERTIFICADO_R2.md`. **Onde os dois
discordarem, ganha a revisão.** É a lista abaixo que herdas.

**B1.** **A fonte é o `Registo Principal` do livro PT, com 221 registos.** O
`Master Log` EN é o mesmo livro com 18 registos incompletos e nenhum exclusivo.
*(exacta; o instrumento é o `Value`, que diverge em 9 de 212 pares)*

**B2.** **Dos 221 registos, 111 têm posição na banda contígua e 110 não têm.**
Dos 110: 53 sem posição declarada pelo próprio documento, 40 no B1, 16 do pomar
espanhol, 1 ficha de produto. **Sobram 204 registos de Ganfei.** *(±10 m sobre
a G35; 24 dos 111 são inferidos; **sem instrumento independente** — a tabela do
gestor produz a colocação, não a confirma; **35 dos 53 dependem do item por
resolver da G34**)*

**B3 — reformulado, e a reformulação é a razão de a revisão existir.** **O único
ensaio microbiológico com posição em todo o caso é o *Meloidogyne hapla*,
positivo em 4/4 unidades colocadas** (6/6 amostras, contando as duas sem
posição). **Nenhum ensaio de fungo ou de oomiceta tem posição.** Das 20 linhas
organismo × matriz, **18 nunca foram ensaiadas em nenhuma amostra colocável**, e
a própria folha declara a convenção: «célula em branco = esse organismo **não
foi testado** nessa amostra (não é o mesmo que um resultado negativo)». **Para 18
das 20 linhas, a pergunta "está onde o padrão está?" não tem dados que a possam
responder em qualquer sentido.** *(categórica quanto à cobertura)*

> **⚠ Aviso que te diz respeito directamente, porque és a camada da exclusão.**
> A frase antiga — «nenhum organismo está onde o padrão está» — lê-se como
> *procurámos e não encontrámos*, e num livro-razão de exclusões entraria como
> **exclusão**. A frase certa lê-se como *não procurámos*, e **não exclui nada**:
> é uma instrução de amostragem para a C5. Ler a primeira onde está a segunda é
> o erro do *P. sojae* com dados melhores, e o `CONTROLOS.md` lista esse como o
> segundo dos três erros que custaram semanas a este processo.

**B4.** **Nove das vinte linhas organismo × matriz vêm de uma só amostra a
granel sem posição** («Kiwi 1000», informe 331/2025, 2025-06-06, madeira + raiz
+ solo). É toda a patologia de madeira e quase toda a de raiz. «Kiwi 1000, Lda»
é `Client_Titular` em **131 de 221** registos. *(exacta; **sujeito ao item da
G34** — se houver testemunho que localize a amostra, B4 cai)*

**B5 — reformulado.** **Nenhum dos 221 registos nomeia a válvula 8.** Os rótulos
existentes do B2 são `B2 - V7`, `B2 - Zona 1 (V7)`, `B2 - Zona 1`, `B2.V7` e
`V7` — **51 registos, todos na v7**. E a unidade que tem as amostras **não está
fora do foco**: **38 das suas 325 células (11,7 %, 0,38 ha) estão dentro do disco
de 90 m**, e a distância mínima de uma célula da v7 ao foco é **53 m**. *(±10 m;
sem instrumento independente)* **Lê-se «nenhum documento nomeia a v8», não «a v8
nunca foi amostrada»** — essa segunda leitura depende do item da G34.

**B6 — reformulado.** **O esforço não está distribuído pelo défice: está
concentrado.** 45,9 % de todos os registos colocados numa única unidade de
3,25 ha (v7); Erica Novo 25,2 %; B3 e B4 14,4 % cada; **oito das doze válvulas
com zero**. **Não existe correlação estimável entre esforço e padrão com estes
dados.** *(descritiva)* **Há selecção total** — não pelo mapa de NDVI, mas por
conveniência operacional, que é uma armadilha diferente e igualmente séria
porque também produz coincidência entre biologia e lugar sem causa comum.

**B7.** **A única amostra biológica do lado oriental é um composto de bloco
sobre 9,92 ha, dos quais 16,3 % são chão lavrado** (v13: 22,6 %; v14: 13,8 %).
**A contagem de 28/37 não pode ser atribuída a plantas do foco ESTE.** *(±10 m;
a fracção de chão é a de 2021)* **A margem encosta à altura medida** — 0,47 m de
mediana no disco ESTE, 50,2 % das células abaixo de 0,5 m, contra 2,34 m e
99,2 % na referência — **e não à etiqueta «sem pérgola», que foi retirada.**

**B8.** **As quatro ITS não são comparáveis entre si, e a diversidade não entra
em nenhuma conclusão.** Profundidade filtrada de 4 964 a 25 078 (5,1x);
qualificadas de 2,8 % a 29,2 % (10x). **Riqueza de ASV, Simpson e Shannon seguem
todos a profundidade a ρ = +1,000** (p exacto **0,083**); só o Pielou se descola
(ρ = +0,400). *(ρ exacto; **sem instrumento independente, e declarado** — passa
porque a conclusão é negativa)*

**B9.** **A *Rosellinia* tem duas amostras, e o negativo molecular é ANTERIOR
por catorze meses.** Campo: 2026-08-04, raiz, uma planta arrancada, local não
especificado, macroscópico, amostra **não enviada**. Molecular: 2025-06-06,
**solo**, composto «Kiwi 1000», sem posição. **Não é a mesma planta, não é a
mesma matriz, e não é depois.** *(exacta; o instrumento é o número de informe e
de expediente, atribuídos pelo laboratório na recepção)*

**B10 — reformulado, e com duas vias independentes.** **16,4 % das células da
referência sistemática (18 de 110) caem dentro dos discos de 90 m dos dois
focos** — 12 no OESTE, 6 no ESTE. É contaminação **geométrica**: a pertença ao
disco não depende do sinal. **A consequência é específica de 2026:** retirá-las
desloca a mediana da referência em **+0,0133** nessa cena e em menos de 0,0025 em
todas as oito anteriores (máximo **0,0010** até 2024). A queda 2024→2026 passa de
**−0,0219** para **−0,0096**. **Segunda via, independente:** a **média** da
referência cai **0,0548** enquanto a **mediana** cai **0,0219**, e a distância
entre as duas passa de −0,0011 (2024) a −0,0340 (2026). **O sentido é
conservador:** limpar a referência torna o acontecimento **maior**. *(**margem
não declarada** — não há bootstrap e a cena é a S2C; parte do +0,0133 pode ser
re-ordenação da mediana)* **Retirado:** as contagens «23 do défice» e «19 do M2»
dentro da referência — medem dispersão interna, não intrusão. **Âncora:** os
«9,47 → 10,32 ha» são **sem** abertura morfológica; o défice de 2026 de 7,86 ha é
**com** abertura 2×2.

**B11.** **Toda a amostragem com posição é posterior ao acontecimento.** As doze
amostras físicas colocadas repartem-se por **2026-03-03 (5), 2026-05-06 (4),
2026-06-17 (2) e 2026-07-08 (1)** — nenhuma anterior a Março de 2026. As três
únicas amostras anteriores a 2026 do caso inteiro — o «Kiwi 1000» de 2025-06-06 e
os dois Becrop — são precisamente as que não têm posição. *(exacta; 12 relatórios
são 9 acontecimentos de amostragem pela regra data × unidade, ou 10 contando
sub-blocos — divergência declarada, não arbitrada)* **Não há linha de base
biológica. Nenhuma comparação antes/depois é possível com estes materiais.**

---

## O que ficou por resolver abaixo de ti

1. **A metade oriental de V2 continua sem datação por segundo instrumento, e
   agora também sem o teste-placebo.** A objecção «e se aquilo é chão?» estava
   dada como fechada pela L4; **a L4 foi retirada**. O que resta é a altura
   medida (L3) numa só data, 06-07-2025. O radar de Inverno positivamente não vê
   a queda: as válvulas do B3 têm anomalias de VV **positivas** nesse Inverno.
2. **Nenhum ponto do B1 tem posição** (G35/G36), incluindo a fronteira do
   porta-enxerto — que é o único contraste de porta-enxerto do caso. Raio de
   incerteza 343 m. **A contagem de nemátodes mais alta de todas (250/200 cc)
   está aí.**
3. **`Erica 2016 R/E` é o mesmo bloco que `Erica Novo`?** É inferência. Se
   estiver errada, **24 dos 111 registos com posição mudam de sítio** (21,6 %).
4. **`Parcela B4`: onde foi colhido?** B4 tem v16-17 na banda **e** a parcela
   solta B4C3 sem posição. Dezasseis registos ficam ambíguos, e o B4 é uma das
   quatro unidades da única correlação nemátodes × padrão que existe.
5. **Não existe controlo externo de kiwi contemporâneo** (G26).
6. **Não há data de plantação** para as 5,37 ha novas (V6).
7. **A permutação de V3 sobre os 56 mosaicos não correu** (R2 do adversário).
8. **Não se sabe onde foi colhido o «Kiwi 1000»**, e dele dependem nove dos
   vinte resultados de patologia.
9. **A partição do LiDAR não cobre 2026.** Terreno limpo depois de 06-07-2025
   conta como sanitário.
10. **De onde veio a linha «amostras» da G34?** *(C3 R2 §0.4 — a entrada de maior
    valor da camada abaixo de ti.)* Quem afirmou que as ISFBV0314–17 e o «Kiwi
    1000» são do foco OESTE, e com que base? Se for memória de uma pessoa, é
    **testemunho directo** e a regra deste projecto diz que se corrige
    perguntando outra vez, não com réplica — e nesse caso **B3, B4 e B5
    reescrevem-se**. Se for inferência, a suspensão consolida-se em rejeição. É
    uma pergunta de uma linha e decide o estatuto de três dos onze factos que
    herdas.
11. **`REF ∩ défice(ano)` para as oito cenas anteriores a 2026** não foi
    calculado. Sem essa coluna não se sabe se «23 células da referência em
    défice» é intrusão do acontecimento ou a cauda inferior que uma referência
    com este espalhamento tem em qualquer ano. **Os dois números foram retirados
    de B10 por isso.** São três linhas sobre ficheiros que já estão em disco, e a
    decisão de as correr é de quem for dono da referência — a C2.
12. **A margem de B10 não existe.** Não há bootstrap, não há intervalo, e a cena
    de 2026 é a S2C que a V10 identificou como o maior confundente da série.
    Parte do +0,0133 pode ser re-ordenação da mediana, e nada na C3 separa as
    duas coisas.
13. **A série tem nove cenas no código e dez no certificado.** `c2_00_comum.DATAS`
    contém nove datas; a **V1 da C2** declara «dez (as nove anteriores mais
    2019-09-02)». **Todo o B10 correu sobre nove.** O adversário da C2 já tinha
    mandado esse item de volta à C0 (condição 1 do seu veredicto) e ele continua
    por re-certificar. **Não o resolvas: declara-o.**
14. **O registo de operações da exploração para o B2 e o B3 em 2024-2026** —
    arranque, replantação, poda severa, substituição de pérgola, falha de rega,
    com data e sector — continua por pedir. O adversário da C2 disse que vale
    mais do que qualquer análise adicional. **A C3 acrescenta a razão: sem ele
    não se sabe se a amostragem de 2026 caiu sobre plantas adultas, sobre
    replantação, ou sobre chão.** É uma pergunta de uma linha ao gestor.

---

## O que foi rejeitado, e não podes usar

Isto é tão importante como o que passa.

- **Qualquer frase da G34 sobre esforço de amostragem** (C3 R2 §0). Nada nos
  dois livros coloca as quatro ITS ou o «Kiwi 1000» num talhão. **Mas a linha
  está em NÃO RESOLVIDO, não em REJEITADO:** não a uses, e também não a trates
  como excluída. *(Não podem ser atribuídas a um **talhão**; a atribuição ao
  pomar é presumida e plausível — o `Client_Titular` das ITS é «Fauna Útil SL»,
  o mesmo submissor dos cinco informes de nemátodes que têm talhão.)*
- **«O foco OESTE está mais amostrado»** (C3). Não se sustenta nos documentos.
- **«Nenhum organismo está onde o padrão está»** (C3, retirado por R2 do seu
  adversário). A categoria não existe no classificador e a afirmação não podia
  falhar. **Usa B3 na forma reformulada, que é sobre cobertura de ensaio.**
- **O ρ = −0,044 e «a amostragem não foi dirigida pelo padrão»** (C3, retirado
  por R3). O vector tinha um valor não-nulo e onze empates a zero. **Usa B6 na
  forma reformulada.**
- **«A amostra colocada mais próxima está a 120 m»** (C3, retirado por R4). Os
  120 m são a distância de um centróide de Voronoi; **nenhuma amostra do caso tem
  coordenada**, e 11,7 % da unidade amostrada está dentro do disco do foco.
- **As contagens «23 células do défice» e «19 do M2» dentro da referência**
  (C3, retirado por R5). Medem a dispersão interna da referência, não intrusão, e
  não têm linha de base por ano.
- **A margem «±0,001 NDVI» de B10** (C3, retirado por R5). Não vem de lado
  nenhum.
- **`lidar\bacia.json`** (C1). Produzido sem `resolve_flats`.
- **«A lavra de 2021 mudou aquele solo»** (C1/C2). A assinatura já lá estava em
  2016-17 no radar e em 2017 no óptico.
- **A linha térmica como sinal independente** (C1 S17). **Não a ressuscites.**
- **«O foco ESTE está numa encosta»** (C1). 0,427° de declive de forma.
- **Qualquer série do B1, e qualquer comparação de nível de NDVI entre o B1 e o
  corpo principal** (R2). Três tentativas, três contaminações.
- **Qualquer percentagem de cobertura tirada de ortofoto** (R2 G13/G37 + C2).
  Sobrevive a estrutura, não o nível.
- **A curva em U do défice como objecto único**, e 2017 como linha de base de
  saúde (V5).
- **«O foco ESTE declina desde 2020»** enquanto afirmação sobre plantas (V2).
- **A taxa de −0,0150/ano da parte plantada do foco ESTE** (C2).
- **Os números −0,1426 e −0,1439 em nível absoluto, e a margem ±0,01** (R3 +
  L5). A moeda é o fosso.
- **O IoU = 0,29 como prova de que 2017 e 2026 são objectos diferentes** (R4).
  0,29 é o que a métrica devolve para «anos afastados».
- **«A v8 destaca-se nos dois instrumentos»** (R1). Um instrumento.
- **A riqueza de ASV das quatro ITS como grandeza biológica** (B8).
- **A subida de 41 para 82 dos Becrop como recuperação** (C3). Épocas opostas,
  n = 1 por data, sem parcela associada.
- **Os 16 registos do informe 240/2023 (Kiwi Atlántico, Ribadumia)** e a ficha
  técnica do húmus. **Armadilha:** o talhão espanhol chama-se «B-3/C-3» e o
  pomar de Ganfei tem um bloco «B3».
- **A «válvula 27»** (C3, busca refeita sobre **18 folhas dos dois livros**): 34
  ocorrências do número 27 isolado, todas `Record_ID` ou a data 2023-06-27,
  **zero por explicar**. Se aparecer, pergunta de onde veio antes de a usar.
  *(De passagem: «Zona 0» ocorre **zero** vezes nos dois livros; «Zona 1» ocorre
  49. O vocabulário do gestor no material de laboratório é «Zona 1».)*
- **O contraste de CaO entre o v7/B2 e a Erica Novo** (C3). Fica em 1,7x —
  abaixo do factor de 2 que a C1 S9 fixa como limiar de interpretabilidade. E a
  razão mais forte é outra: **os dois boletins do lado Erica Novo são
  precisamente os dois inferidos**. **Mas a S10 da C1 sobrevive inteira** — ela
  afirma um défice de cálcio contra um intervalo de referência analítico,
  confirmado por **folha** (outra matriz, outro método, outra data), que é
  afirmação diferente do contraste entre blocos. **Não arrumes as duas juntas.**
- **A «podredumbre radicular» dos Becrop como instrumento independente** (C3 R2
  §1). A categoria **existe** — está na coluna `Notes` dos registos 79 e 86, e o
  79 nomeia *Phytophthora sojae*. O que cai é a etiqueta de instrumento
  independente: são duas anotações do mesmo compilador sobre os mesmos dois
  relatórios. **A conclusão «os dois Becrop não são comparáveis» aguenta-se** nos
  163 dias entre épocas opostas, no n = 1 por data, no «No hay parcela asociada»
  e na freguesia declarada.
- **A entrada de CORRIGIDO da C3 sobre a L5** (C3 R2 §4, retirada pela própria
  C3). A L5 **não estava errada**: a divergência 0,054 contra 0,0218 é **média
  contra mediana** sobre as mesmas 110 células e as mesmas duas datas. Nenhuma
  das duas sessões errou.

---

## Materiais

Só estes. Não tens dados brutos: a tua matéria-prima são os quatro certificados
e os JSON de saída, que existem para poderes citar o cálculo em vez do dossiê.

```
Downloads\_VALIDACAO_CAMADAS\
  CAMADA_0_REVISAO_R2.md        + suplemento G34-G37
  CAMADA_0_ADENDA_CONTROLO.md   o controlo externo que não existe
  CAMADA_1_CERTIFICADO.md       S1-S20
  CAMADA_2_CERTIFICADO.md       V1-V11
  CAMADA_2_ADVERSARIO.md        R1-R4, W1-W7, os cinco testes de cinco minutos
  CAMADA_2_ADENDA_LIDAR.md      L1-L8 — ganha sobre o certificado da C2,
                                MAS L4 e L6 estao RETIRADOS; ver o aviso no topo
  ADVERSARIO_2026-08-29.md      o adversario da adenda — retira L4 e L6 e a
                                etiqueta «pergola / chao». LE-O antes da adenda
  CAMADA_3_CERTIFICADO.md       histórico — atacado, NÃO uses a lista dele
  CAMADA_3_ADVERSARIO.md        R1-R8, W1-W9, o veredicto e os cinco testes
  CAMADA_3_CERTIFICADO_R2.md    B1-B11 revistos — **GANHA sobre o certificado**
  REFERENCIAS_MULTIVERSO.md     o que a literatura estabelece sobre divergência
  SAIDA_C1\  SAIDA_C2\  SAIDA_C3\   código e JSON de cada camada
Downloads\_VALIDADE_GESTAO\     os cinco scripts da adenda de LiDAR + REGISTO.md
Downloads\ganfei_s2\valvulas_por_area.json
Downloads\ganfei_s2\sentinel\masks_geograficas.json
```

**Não abras `ganfei_s2\_pacote_cowork\`.** Contém a árvore de decisão e material
da C5. Vê-lo antes de fazeres o teu trabalho contamina-o.

---

## Tarefas

1. **Constrói o livro-razão das exclusões, e conta as linhas.** Uma linha por
   causa candidata. Cada linha nomeia: a causa, o facto que a exclui ou a
   sustenta, o certificado e o número do facto (`S6`, `V3`, `L3`, `B7`…), e o
   **estatuto** — excluída, sustentada, ou **não testada**. Uma causa que
   ninguém testou não é uma causa excluída, e o livro tem de as distinguir a
   olho. Saída: `SAIDA_C4\c4_razao_exclusoes.csv`.

2. **A pergunta que a cadeia inteira preparou: são um acontecimento ou dois?**
   O que aponta para um: mesma janela (V2), correlação NDVI×SAR sobre
   geometria pura (V3). **As duas pernas que a adenda dava a esta leitura — L4 e
   L6 — foram retiradas**, e a resposta tem de contar com isso. O que aponta
   para dois: substratos opostos em **todas** as variáveis que os separam (S20),
   a amplitude sazonal com trajectórias de forma diferente (L8 — o OESTE desce
   monotonamente cinco anos, o ESTE cai a 0,10 e **recupera** a 0,65), e o
   parcelário a declarar KIWI no N3 em Junho de 2025. **Responde às duas, e diz
   qual das duas leituras o material sustenta melhor e com que margem.**

3. **A hipótese de renovação de pomar, tratada como hipótese a sério.** Do lado
   oriental existe uma leitura que não é patologia: corte e replantação. O que a
   sustenta: 0,27 m de altura no N3 em 06-07-2025 (L3), a amplitude sazonal a
   cair a 0,10 e a recuperar a 0,65 (L8), o parcelário a declarar KIWI a
   10-06-2025, 16,3 % de chão lavrado no B3 (B7). **Escreve o que a
   falsificaria** e diz se algum material existente a falsifica. **Não a
   confirmes por coerência:** três hipóteses de terreno já foram fixadas,
   corridas e retiradas neste caso (posição topográfica húmida, topologia da
   rede de rega, e a linha térmica).

4. **O argumento geométrico, com a margem certa.** V8 dá 2,02 ha a 24 m do foco
   OESTE e 1,41 ha a 62, 72 e 167 m do foco ESTE; o LiDAR reproduz a 60, 75 e
   166 m. **Usa 2,60 ha como número defensável e 3,58 como tecto** (W2). E
   propaga a taxa de base: o acontecimento é 2,7 vezes mais provável sobre
   terreno com histórico.

5. **O que a biologia permite dizer, e é pouco — e a distinção que decide o teu
   livro-razão.** A C3 entrega um resultado negativo forte (B3, B5, B7, B11).
   **Não o contornes, e não o promovas.** Diz explicitamente o que a matriz de
   diagnóstico **não pode** conter por falta de posição: os nove organismos do
   «Kiwi 1000» não entram em nenhuma casa do mapa. **E a linha do livro-razão
   para cada um dos 18 organismos nunca ensaiados com posição tem de dizer "NÃO
   TESTADA", nunca "excluída".** Uma causa que ninguém procurou não é uma causa
   excluída, e a tarefa 1 pede-te que as distingas a olho precisamente por isto.
   O único ensaio microbiológico colocável do caso inteiro mede um organismo, o
   *M. hapla*, e ele está em todas as unidades com a contagem mais baixa no
   bloco mais afectado.

6. **A perda de água antes da perda de verdura.** O Landsat 8/9 (140 cenas,
   2013-2026) mostra que os dois focos perdem água do copado mais depressa do
   que verdura: em 2026 o fosso NDMI é **0,199 contra 0,146 de NDVI** a oeste, e
   **0,201 contra 0,138** a leste. **E não foi seca:** Julho-Agosto de 2026 foi o
   mais húmido da década. **Duas hipóteses de terreno já foram fixadas, corridas
   e RETIRADAS:** posição topográfica húmida (o défice está no terreno alto, em
   todas as onze cenas) e topologia da rede de rega (o agrupamento por válvula
   cai dentro do nulo em todas as cenas). Diz o que sobra e o que faria falta.

7. **Nomeia as três perguntas de uma linha que fechariam mais coisas.** Ordena
   por confiança ganha por esforço, como o adversário da C2 fez. Uma delas já
   tem dois pedidos independentes atrás dela e continua por fazer. **Candidatas
   já identificadas e por fazer:** de onde veio a linha «amostras» da G34; de que
   talhão foi colhido o «Kiwi 1000» (informe 331/2025); o formulário de submissão
   das ISFBV; e o registo de operações do B2 e do B3 em 2024-2026. **Três dos
   erros que custaram semanas a este processo foram apanhados por ir a um
   instrumento diferente, e nenhum por recalcular.**

8. **Se a inferência não fechar, di-lo.** «O material não distingue A de B» é
   saída válida e obrigatória. O protocolo trata a dúvida assinalada como
   resultado; um facto inventado destrói a cadeia inteira.

---

## Onde já se errou nesta matéria

- **Uma máscara derivada do sinal que se ia medir.** Foi o erro central de todo
  o processo e passou por quatro auditorias. O equivalente na tua camada é
  construir a matriz de diagnóstico a partir das causas que já foram
  investigadas, e depois concluir que a causa é uma delas. **A ausência de
  investigação não é evidência de ausência**, e a C3 mede exactamente isso:
  **18 das 20 linhas organismo × matriz nunca foram ensaiadas em nenhum ponto
  colocável**, e nenhum documento nomeia a válvula que contém o foco OESTE.
- **Um positivo tratado como discriminante.** *M. hapla* deu positivo em todos
  os blocos amostrados e chegou a ser tratado como achado. **A contagem mais
  baixa dos cinco está no bloco mais afectado.**
- **Um patogénio atribuído ao corpo em declínio sem posição.** Aconteceu com
  *P. sojae*. Repetiu-se, em forma mais subtil, na linha «amostras» da G34. **E
  o nome volta a aparecer:** o registo 79 do `Registo Principal` regista, nas
  `Notes` do Becrop de Agosto de 2023, «Microrganismo em destaque, relacionado
  com a podridão radicular: *Phytophthora sojae*» — num relatório **sem parcela
  associada** e numa freguesia que não é Ganfei. É o mesmo organismo, o mesmo
  problema de posição, e desta vez está registado. **Não o promovas.**
- **Nomes de focos trocados.** Durante semanas «Zona 0» significou dois sítios a
  500 m um do outro. Por isso os focos se identificam por coordenada.
- **O «B1» que era Valença.** Uma pergunta de identidade — *o que é este
  sítio?* — que não se fez a uma camada abaixo daquela onde a inferência corria.
  **Tu és a camada onde a inferência corre. Faz a pergunta.**
- **Uma frase que liga números certos.** Todas as quatro retiradas do adversário
  da C2 foram disso, e seis das oito do adversário da C3: nenhuma apagou uma
  medição, quase todas apagaram a frase. Escreve as tuas frases a contar com isso.
- **Uma afirmação que não podia falhar.** A C3 publicou «zero na categoria "está
  onde o padrão está"» sobre uma categoria que o seu próprio classificador não
  conseguia emitir. Antes de escreveres um resultado negativo, verifica que o
  teste podia ter dado positivo.
- **Um valor transcrito à mão para dentro de um script, gravado num JSON, e
  depois citado a partir do JSON.** Aconteceu na C3 com os números Becrop. É o
  mecanismo do «B1»: a saída passa a ser a prova do valor. **Lê do ficheiro.**
- **Uma divergência declarada corrigida sem ser investigada.** A C3 viu 0,054
  contra 0,0218 na mesma quantidade e chamou-lhe erro alheio. Era média contra
  mediana, e a diferença entre as duas era uma prova independente do seu próprio
  achado. **O controlo 2 diz que divergência sem explicação é achado, não
  correcção** — e o custo de a arrumar como correcção foi deitar fora a prova.

---

## O que entregar

1. `CAMADA_4_CERTIFICADO.md`, com as cinco secções do protocolo — CONFIRMADO,
   CORRIGIDO, REJEITADO, NÃO TESTÁVEL, PASSA PARA CIMA. A secção PASSA PARA
   CIMA é uma **lista fechada**: sê avaro. Cada facto leva o certificado e o
   número do facto que o sustenta, o **instrumento independente** (controlo 1) e
   a margem.
2. `CAMADA_5_PROMPT.md` (decisão), seguindo `MODELO_PROMPT.md`.
3. Código e tabelas em `SAIDA_C4\`.

Reporta as **quantidades-âncora**: `pomar` 30,31 ha · referência sistemática
1,10 ha / 110 células · banda contígua 27,30 ha · total da tabela 44,93 ha ·
chão lavrado 1,67 ha · **défice de 2026 7,86 ha com abertura 2×2 / 9,47 ha sem**
· declínio novo M2 3,58 ha (tecto) e 2,60 ha (defensável) · **cenas na série 11,
de plena estação 9 no código e 10 no certificado da C2 — declara a divergência**
· NDVI da referência 2017-07-02 **0,838 declarado / 0,8898 obtido** e 2026-07-27
**0,886 declarado / 0,8766 obtido**, com o **sinal invertido** · 221 registos,
111 com posição, 15 taxa distintos, **2 de 20 linhas ensaiadas com posição**. E
acrescenta as tuas: número de causas no livro-razão, quantas excluídas, quantas
**não testadas**.

**Sobre distâncias, porque já houve seis números para dois objectos.** Sempre
que citares uma distância ao foco OESTE, diz de que objecto é. Os que existem:
v8 — 34 m (G35, ponto da válvula), 35 m (C1), 43 m (C2, centróide de Voronoi),
46 m (C3, centróide de Voronoi); v7 — 111 m (C1, ponto da válvula), 120 m (C3,
centróide), 53 m (C3, célula mais próxima). **Nenhum deles é a distância de uma
amostra, porque nenhuma amostra do caso tem coordenada.**

**Não teorizes acima da tua camada.** Não desenhes amostragem, não escrevas
medidas de gestão, não construas a árvore de decisão — isso é C5.

**Não modifiques nada em `Downloads\ganfei_s2\`.**

Se rejeitares um facto herdado, **pára** e devolve — **e pára a sério**. A C3
rejeitou a linha «amostras» da G34, construiu quatro factos por cima, escreveu
este prompt, e só o adversário travou a cadeia. Escreve o que rejeitaste com
destaque, **e não escrevas o `CAMADA_5_PROMPT.md` antes de a rejeição estar
arbitrada.**
