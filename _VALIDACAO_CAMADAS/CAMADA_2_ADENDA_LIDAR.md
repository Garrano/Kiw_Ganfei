# Camada 2 — adenda de LiDAR

29-08-2026. **Esta adenda substitui partes do `CAMADA_2_CERTIFICADO.md`.** Onde
o certificado e esta adenda discordarem, **a adenda ganha**, pela mesma razão
que a `CAMADA_0_REVISAO_R2.md` ganha sobre o certificado da C0: entrou
instrumento novo.

Lê-se depois de `CAMADA_2_ADVERSARIO.md`, cujas retiradas se mantêm todas.

> ## ⚠ AVISO DE RETIRADA — 29-08-2026, mesmo dia
>
> Esta adenda foi rastreada pelo `ADVERSARIO_2026-08-29.md` **depois** de
> escrita. **Dois dos oito factos da lista fechada foram RETIRADOS e um foi
> corrigido.** Quem lê esta adenda tem de ler primeiro este aviso:
>
> **L4 — RETIRADO.** A adenda diz que o degrau do foco ESTE «existe em copado
> (p=0,042) e não existe em chão (p=0,368)», e chama-lhe o teste-placebo que a
> C2 não podia correr. **É falso.** O próprio `refazer_c2_este.json` regista, na
> parte **sem** pérgola, um degrau de **+0,0531** contra **+0,0585** no copado —
> **91 % do mesmo tamanho**. O que separa os dois valores p é a variância
> residual, **23 vezes maior** no chão, não o efeito. O número estava na tabela
> impressa e foi lido por cima. Acresce que o teste é um Welch de 2 contra 8
> pontos, estatística que o adversário anterior já tinha declarado incapaz de
> dar significância. **Não há controlo negativo. A frase «o sinal está onde
> estão as plantas e não está onde elas não estão» é retirada.**
>
> **L6 — RETIRADO E SUBSTITUÍDO.** A adenda diz «0,00 ha em 2022, 2023 e 2024»
> no copado vivo. **Era artefacto.** `mapa_defice` aplica a abertura morfológica
> 2×2 **depois** de intersectar com a máscara recebida, logo calcular o défice
> dentro de um subconjunto não é calculá-lo no polígono e dividir. A costura
> perdia **15 a 41 %** do défice, e os três anos que liam zero eram precisamente
> os de maior perda (39 %, 31 %, 34 %).
>
> **Valores corrigidos**, com a abertura a correr **uma vez** sobre o polígono e
> só depois a divisão — as partes somam agora exactamente o total em todas as
> cenas:
>
> | | 2017 | 2020 | 2022 | 2023 | 2024 | 2025 | 2026 |
> |---|---|---|---|---|---|---|---|
> | copado vivo | 5,78 | 2,26 | 0,83 | 0,66 | **0,67** | 2,31 | **4,66** |
> | chão | 2,30 | 1,79 | 2,33 | 2,42 | 2,24 | 3,12 | 3,20 |
>
> O piso real é **0,66–0,67 ha** e o evento é uma multiplicação por **7,0** em
> dois anos. É afirmação mais fraca do que «parte de zero» e é a verdadeira.
> Figura F9 refeita em consequência.
>
> **VIÉS DE SOBREVIVÊNCIA — não declarado na versão original.** A adenda declara
> o limite **para a frente** da partição de 06-07-2025 e nunca o limite **para
> trás**, que é onde ela mais se usa: classifica o défice de 2017 com uma
> medição de 2025. O conjunto «copado vivo» é, por construção, **o que ainda
> estava vivo em 2025**; mortalidade consumada antes disso conta como chão em
> toda a série. Isto não enfraquece o «parte de zero» — **explica-o**.
>
> **Outras correcções do mesmo adversário, a ter em conta:**
> - O limiar **operativo** é `h ≥ 0,5 m`, e não os 1,5 m que esta adenda
>   justifica três vezes. E 0,5 m cai a **0,03 m da mediana do foco ESTE**, ou
>   seja corta a unidade pelo seu próprio centro.
> - O IFAP declara **KIWI em 65 % do terreno que esta adenda chama «chão»**, o
>   que contradiz a frase do §1.3.
> - A correcção de V10 é atribuída ao LiDAR, mas a coluna `nu2021` recomputada
>   já discorda dos números publicados pela C2 — **as duas máscaras concordam
>   entre si**, e a discordância é com o certificado.
> - A coincidência de **1,3 %** entre 44,36 ha declarados e 44,93 ha da tabela
>   **não é independente**: o ENT_ID foi seleccionado pela geografia que o gestor
>   deu e compara-se com uma tabela do mesmo gestor. A comparação desagregada
>   concorda pior (2,9 %).
>
> **O que o adversário credita e não estava na lista fechada:** a série Landsat
> — fosso do v8/B2 em ±0,004 durante onze anos, depois 0,046 e 0,146, com a
> referência a cair 0,026 contra 0,054 do Sentinel-2 — **é o melhor resultado do
> dia** e não tinha entrado. E o piso de Inverno (N3 a 0,654 contra 0,358 da
> referência em 2024/25) é melhor prova do que a amplitude de Verão e nunca foi
> citado.
>
> **Nomenclatura:** onde esta adenda escreve «foco OESTE», leia-se **v8/B2,
> E530485 N4655053**. **Não é o B1**, que fica a 900 m a sudoeste. A colisão de
> nomes já custou tempo a este projecto duas vezes.

---

## O instrumento que entrou

**LiDAR aerotransportado da DGT, voo de 6 de Julho de 2025, das 14h34m53s às
14h51m08s UTC**, folhas LO-158565 e LO-159565 da mesma passagem. LAS 1.4,
16,6 e 17,8 milhões de pontos, densidade nominal 10 pt/m². Produtos MDS e MDT
a 50 cm, 21 folhas sobre a AOI.

**A data não veio dos metadados.** O registo SNIG dá para o Lote I uma janela
de catorze meses (12-05-2024 a 23-07-2025), inútil para este caso. A data saiu
do **tempo GPS dos pontos**. Quem repetir isto deve fazer o mesmo: o campo
`datetime` da API do Centro de Dados é geração de produto, não voo.

**Porque muda alguma coisa.** Tudo o que esta cadeia usou até aqui mede
reflectância — NDVI, NDRE, ortofoto, periodicidade — e o radar mede
retrodifusão. O LiDAR mede **geometria**. É a primeira vez neste caso que a
regra do projecto, de que nenhum facto passa adiante verificado só pelo
instrumento que o produziu, pôde ser cumprida a sério.

**A medição.** `MDS − MDT` na grelha de 10 m; a grandeza é a altura mediana e
a fracção de píxeis de 50 cm acima de 1,5 m, limiar que fica abaixo da pérgola
de kiwi (1,8–2 m) e acima de qualquer coberto herbáceo. Controlo interno: o
terreno que a `nu2021` marca como lavrado lê **0,09 m**; a referência
sistemática lê **2,34 m com 99,2 %**.

**Não é circular, e é o inverso exacto do erro conhecido.** Em
`fazer_masks_v2.py` a máscara `pomar` era `nd2026 > 0,78` e media-se depois a
evolução até 2026. Aqui a máscara vem de altura física medida por um
instrumento que não vê reflectância, e a série medida é de NDVI.

---

## O que a partição encontrou

Do polígono de 30,31 ha, **3,77 ha (12,4 %) não tinham pérgola nenhuma em
06-07-2025**.

| unidade | altura | % acima de 1,5 m |
|---|---|---|
| referência sistemática | 2,34 m | 99,2 % |
| resto do pomar | 2,32 m | 99,2 % |
| foco OESTE, disco todo | 2,25 m | 90,2 % |
| declínio NOVO de 2026 (V8) | 2,17 m | 79,9 % |
| **foco ESTE, disco todo** | **0,47 m** | **35,0 %** |
| *nu2021, lavrado em 2021* | *0,09 m* | *15,2 %* |

**Metade do disco ESTE está abaixo de meio metro.** E **22,7 % do que a C2
chamou «foco ESTE plantado» — a máscara `~nu2021` — não tinha pérgola.** A
`nu2021` era o melhor que existia então, e falha por um quinto.

---

## PASSA — o que a adenda confirma

| facto | como |
|---|---|
| **O degrau do foco ESTE existe, e agora tem controlo negativo.** Restringido a copado (1,27 ha com pérgola): degrau de **+0,0585 em fosso**, degrau bate recta **2,29 : 1**, p = 0,042. Na parte **sem** pérgola (1,28 ha): **1,06 : 1, p = 0,368** — recta e degrau indistintos, nada acontece em 2025. | `refazer_c2_este.py`. É o teste-placebo que a C2 não podia correr: o sinal está onde estão as plantas e não está onde elas não estão. |
| **V8 aguenta por inteiro.** As três manchas de declínio novo junto ao foco ESTE reproduzem-se a 0,55 / 0,61 / 0,25 ha a **60, 75 e 166 m** (publicado: 62, 72, 167 m), e **71 a 92 % delas tinham pérgola**. Não é chão. | idem |
| **A direcção de V10 confirma-se com instrumento melhor.** Fracção sem pérgola do défice dentro do disco ESTE: **71,7 % (2017), 74,5 % (2020), 75,6 % (2024), 61,3 % (2025), 53,4 % (2026)**. O núcleo oriental foi cerca de três quartos chão durante oito anos e cresceu para dentro de copado em 2025-26. | idem |
| **As 3,58 ha de declínio novo de 2026 tinham pérgola completa** — 2,17 m, 79,9 %. Responde à pergunta que o adversário disse que ninguém tinha feito ao ramo **ascendente**: não é terreno arrancado. | `altura_copado.py` |
| **O foco OESTE é pomar vivo.** 2,25 m, 90,2 %, só 12,1 % das células abaixo de meio metro. | idem |

---

## CORRIGE — o que muda de valor

| o que o certificado diz | o que a adenda mede | consequência |
|---|---|---|
| **V2:** degrau de **−0,1426** no foco OESTE e **−0,1439** na parte plantada do ESTE. | Em **fosso**, que é a moeda que a própria camada declarou operativa em V10: **+0,0908** (OESTE disco) e **+0,0724** (ESTE «plantado»); restringindo a copado, **+0,0720** e **+0,0585**. | **Mais de metade do degrau publicado era a referência a cair.** A referência desce 0,054 de 2024 para 2026 e o viés do S2C, medido independentemente por duas sessões, é 0,048. A afirmação de nível não sobrevive; a de fosso sobrevive. |
| **V2:** «os dois focos caem juntos, na mesma janela, **pela mesma quantidade**». | 0,0720 contra 0,0585 em copado. E o degrau do OESTE restringido a copado **perde significância**: p = 0,091. | «Pela mesma quantidade» cai. «Na mesma janela» mantém-se. |
| **V10:** fracções de chão despido de **53 % (2020), 60 % (2022), 78 % (2024), 34 % (2026)**. | Pelo LiDAR: **74,5 %, 75,7 %, 75,6 %, 53,4 %**. | A história é a mesma e é mais estável do que a publicada. Os números do certificado vinham de `nu2021`, uma máscara de 2021 aplicada a dez anos; substituem-se. |
| A série do défice como grandeza única — 8,08 / 4,05 / 2,91 / 5,43 / **7,86 ha**. | **40,7 % do défice de 2026 é terreno sem pérgola.** Separada: só onde havia pérgola, **4,89 → … → 0,00 (2022, 2023, 2024) → 1,32 → 4,03 ha**. | A série publicada somava copado a definhar com chão sem planta. Separada, o degrau sanitário **parte de zero**, não de 2,91 — é mais limpo, não mais fraco. Figura F9. |

---

## SAI DE «NÃO TESTÁVEL» — parcialmente

O certificado escreve que «a queda do foco ESTE em 2025-2026 **não tem
instrumento independente**, e o radar positivamente não a vê», e pede «uma
segunda medição óptica de outra proveniência, ou fotografia de campo datada, ou
uma contagem de plantas mortas por linha com data».

**O LiDAR responde a metade disso, e convém ser exacto sobre qual metade.**

- **Responde ao substrato.** A parte do foco ESTE que declina tem 2,12 m de
  pérgola e 80,3 % de cobertura: o NDVI ali mede planta, não solo exposto. E a
  parte sem planta não tem degrau. A objecção «e se aquilo é chão?» fica
  fechada.
- **Não responde à datação.** O voo é **uma data**. Não diz quando o degrau
  começou, e o pedido do certificado por uma medição óptica independente
  **mantém-se em aberto**.

---

## PASSA PARA CIMA — lista fechada

**L1.** Voo LiDAR DGT de **06-07-2025**, datado pelo tempo GPS dos pontos e não
pelos metadados. Referência 2,34 m / 99,2 %; terreno lavrado 0,09 m / 15,2 %.

**L2.** **3,77 das 30,31 ha do polígono não tinham pérgola nessa data.**

**L3.** O **foco OESTE é copado vivo** (2,25 m, 90,2 %); **metade do disco ESTE
não é** (0,47 m, 50,2 % das células abaixo de 0,5 m).

**L4.** O degrau do foco ESTE **existe em copado** (+0,0585 fosso, 2,29 : 1,
p = 0,042) e **não existe em chão** (1,06 : 1, p = 0,368).

**L5.** Em fosso, os degraus são **+0,0720 (OESTE)** e **+0,0585 (ESTE)**, não
−0,1426 e −0,1439. A diferença é a referência a cair, e o viés do S2C explica
quase toda a queda da referência.

**L6.** A série sanitária, restrita a copado: **0,00 ha em 2022, 2023 e 2024**;
1,32 em 2025; **4,03 em 2026**.

**L7.** As **1,41 ha** de declínio novo junto ao foco ESTE são copado
(71–92 % com pérgola), e as **3,58 ha** de declínio novo total também (79,9 %).

**L8.** Amplitude sazonal relativa à referência, medida em 276 cenas de 2022 a
2026 e **independente do LiDAR**: o núcleo oriental N3 cai a **0,10 em 2025** —
não folia — e recupera a 0,65 em 2026; o foco OESTE desce monotonamente
**0,97 → 0,95 → 0,76 → 0,54 → 0,30**; o resto do pomar fica em 0,97–1,05. Os
dois instrumentos concordam no mesmo mês e no mesmo sítio.

---

## Aviso que acompanha tudo o que está acima

**A partição vale até 06-07-2025 e é hipótese depois disso.** O LiDAR é uma
data. Terreno limpo **depois** desse dia — já dentro de 2026, que é o ano em
causa — continua a ser contado como sanitário. As 3,58 ha de declínio novo
tinham pérgola em Julho de 2025, e nada aqui prova que a mantiveram em Julho de
2026.

**Fecha-se isto com um segundo voo, ou com uma visita. Não com mais análise.**

---

## Ficheiros

```
Downloads\_VALIDADE_GESTAO\
  altura_copado.py      MDS-MDT, agregacao a 10 m, por unidade
  refazer_c2_este.py    V2 / V8 / V10 refeitos com a particao do LiDAR
  serie_separada.py     a serie do defice partida em duas
  piso_inverno.py       verificacao independente do piso de Inverno
  amplitude.py          amplitude sazonal, 276 cenas, 2022-2026
  REGISTO.md            o percurso, incluindo dois testes meus retirados
Downloads\ganfei_s2\lidar\        21 folhas MDS + 21 MDT
Downloads\ganfei_s2\lidar\laz\    LO-158565, LO-159565
Downloads\ganfei_s2\figuras\F9_serie_separada.png / .svg
```
