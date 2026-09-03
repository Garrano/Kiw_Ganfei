# Camada 2 — Sinal vegetal · revisão R2

**Data:** 31-08-2026 · **Escreve:** sessão Claude Code
**Precedência:** ganha sobre `CAMADA_2_CERTIFICADO.md` e sobre
`CAMADA_2_ADVERSARIO.md`, pela regra com que a `CAMADA_3_CERTIFICADO_R2`
ganhou sobre os seus.
**Herda:** C0 + `CAMADA_0_REVISAO_R2` + `CAMADA_0_REVISAO_R3` (G38–G41), e os
adversários de todas as camadas abaixo.

---

## 0 · A PARAGEM DE LINHA, formalizada com três dias de atraso

A regra 2 diz que quem rejeita um facto de uma camada abaixo **pára, escreve o
que rejeitou, e devolve**. Rejeitei uma decisão do adversário desta camada em
28-08 e continuei a construir por cima. Isto é a devolução.

### O que rejeito

`CAMADA_2_ADVERSARIO.md`, decisão sobre o que sobe:

> «os números que passam para cima têm de ser **0,128 e 0,118 no fosso**, não
> −0,1426 e −0,1439 em nível absoluto, e a margem tem de ser a amplitude do
> patamar de cada unidade.»

### Porquê — e é um facto novo, não uma preferência

**A referência que define o fosso tem catorze das suas 110 células dentro dos
discos dos focos.** Essas catorze dão degrau de **−0,1458**, ou seja, são os
focos. Cinco caem dentro do próprio polígono da Zona 0; a mais próxima está a
**10 m** de um centro. Retirando só essas catorze, o degrau da referência cai de
−0,0481 para **−0,0235**.

**O fosso mede, em parte, os focos contra si próprios.** O adversário não podia
saber: a contaminação só foi medida em 31-08.

### O que NÃO cai com isto

Nada da C2 fica errado. **Os números do fosso continuam certos como fosso**, e
esta revisão reproduz-os à quarta casa (ver §5). O que cai é a sua **promoção a
moeda de registo**.

### Onde recomeça

Nesta camada, com a grelha de referência reconstruída segundo
`PRE_REGISTO_REFERENCIA.md` — **assinado em 31-08 e ainda por correr**. Fica em
NÃO TESTÁVEL abaixo, com o critério de *line-stop* já fixado por escrito.

### O que aceito do adversário, e aplico

**A margem.** Ele exigiu a amplitude do patamar de cada unidade e não «±0,01».
Aplicada: cada facto abaixo leva a amplitude do multiverso ou o intervalo
medido, nunca um ±0,01 genérico.

---

## 1 · CONFIRMADO

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| **A referência sistemática está contaminada pelos focos.** 14 das 110 células caem dentro dos discos e dão degrau de −0,1458; 5 caem dentro da Zona 0; a mais próxima a 10 m de um centro. Limpa dessas catorze, a referência desce −0,0235 em vez de −0,0481. Separada por distância: >150 m dá −0,0163 (n=61), <150 m dá −0,0748 (n=42). | `halo_distancia.py`, secção de referência | — (é uma propriedade da grelha, não um facto de terreno) | exacta sobre a grelha |
| **O degrau em nível absoluto é invariante em todo o espaço de análise percorrido — 43 corridas.** As unidades são **aninhadas** (discos concêntricos de 60/90/120 m) e os limiares também (0,3 ⊂ … ⊂ 2,0): isto é **invariância, não replicação independente**. 5 unidades × 3 raios × 5 limiares de altura. **ORIENTAL** −0,1274 a −0,0351 (n=23, p<0,05 em 20); **OCIDENTAL** −0,1872 a −0,0542 (n=20, p<0,05 em 15); **CONTROLO** −0,0020 a +0,0009 (n=5, p mínimo 1,000). Nenhuma das 43 muda de sinal. O pior foco está 17× acima do melhor controlo. | `multiverso_degrau.py` → `.json` | a partição vem do LiDAR (G38), não do NDVI | amplitude impressa; não há valor central |
| **O degrau ajusta melhor que a recta nos focos, e pior no controlo.** Em nível absoluto, mesmo número de parâmetros: ORIENTAL Zona 0 **3,98:1**, ORIENTAL disco **3,54:1**, OCIDENTAL disco **3,60:1**, **resto do pomar 0,84:1 — ganha a recta.** | `degrau_vs_recta_pergola.py` → `.json` | — (decomposição interna) | soma de quadrados, exacta |
| **O Landsat replica o degrau, e no mínimo p que o teste permite.** 140 cenas, 14 anos, mediana anual, p **exacto** por enumeração das C(14,2)=91 divisões. OCIDENTAL **−0,1128**, ORIENTAL **−0,0791**, ambos **p = 0,0110** — que é 1/91, o mínimo atingível: a divisão observada é a de maior degrau das 91. Controlo −0,0012, p=0,978. Chão sem pérgola −0,0439, p=0,418. | `landsat_degrau_absoluto.py` → `.json` | **USGS/NASA, OLI, LaSRC, outra órbita** — responde ao pedido que o certificado da C2 deixou em NÃO TESTÁVEL para o foco oriental | p exacto, não amostrado |
| **A diferença de dia-do-ano entre os dois grupos não explica o degrau.** Os grupos diferem 8,7 dias (208,3 contra 217,0). Sonda intra-anual 2025-06-17/2025-08-14, mesmo ano e sensor, **por unidade**: correcções de −0,0007 (OCIDENTAL) e +0,0011 (ORIENTAL). Corrigidos: **−0,1281** e **−0,1247**. | `fenologia_por_unidade.py` → `.json` | reproduz o número que o adversário desta camada mediu na referência: **−0,0162 em 58 dias**, exacto | limite SUPERIOR do efeito: 2025 é ano do acontecimento, logo o declive medido é fenologia mais queda |
| **Os três núcleos satélite descem já em 2025, cena que não entrou na sua selecção.** Base 2017-24 normal — 0,878 · 0,872 · 0,901, contra 0,867–0,892 nas parcelas do IFAP. Degrau de 2025 só: −0,0480 · −0,0414 · −0,0365, nos percentis **2,4 % · 4,7 % · 8,7 %** de mil discos do mesmo tamanho sorteados no pomar com pérgola a >120 m dos focos. | `satelites_sem_2026.py` → `.json` | a base normal e o ano de 2025 são as duas coisas que a selecção (feita em 2026) não podia fabricar | percentil sobre nula de vizinhança, n=1000 |
| **A reprodução dos números desta camada passa à quarta casa.** Refeita a conta do adversário — fosso, estimando 2024→2026, unidades dele: OESTE **0,1283** contra 0,128 publicado; ESTE plantado **0,1179** contra 0,118. | `emparelhar_moedas.py` → `.json` | é reprodução independente do resultado central da C2 | 0,0003 e 0,0001 |

## 2 · CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| «O degrau publicado é +0,01103/ano no fosso da Zona 0 sem `nu2021`, p=0,0162» — lido como taxa de declínio. | Restrito às células com pérgola do LiDAR dá **+0,00884/ano, p=0,0294**, e é invariante ao limiar (0,0083–0,0091 entre 0,3 e 2,0 m). **Mas o modelo é o errado:** o degrau bate a recta 3,98:1. Não há ano em que aquela unidade tenha caído 0,015. | O declive **não se cita como taxa**. A C5 já tinha esta correcção para a R2 G30; aplica-se agora também à versão restrita. |
| A partição planta/chão do foco oriental usava `nu2021`, da ortofoto de 2021. | **22,7 % do que a `nu2021` deixava passar como plantado não tem pérgola** no LiDAR, e metade do disco oriental está abaixo de 0,5 m. A partição operativa passa a ser a altura MDS−MDT ≥ 0,5 m. | Todas as unidades orientais têm de declarar qual partição usam. As duas correm; as duas se reportam. |
| Não havia instrumento independente para o foco oriental (NÃO TESTÁVEL da C2). | **Passa a haver: o Landsat.** E a assimetria fica escrita: para o **ocidental** já havia — o Sentinel-1, certificado por esta camada. Para o **oriental** o radar **não distingue**, e sabe-se porquê. | A frase «única série de outra proveniência» é falsa e sai. A correcta é a estreita. |
| **A minha própria S1, na primeira redacção desta revisão.** Escrevi o degrau em nível absoluto como se o número fosse todo de terreno. | **Colide com o V10 desta camada, que está certificado e eu não tinha lido:** «o nível absoluto não pode carregar uma afirmação sobre o pomar todo» — as duas cenas mais baixas da série são **as duas únicas do S2C**, e o mesmo degrau aparece **fora do pomar**: −0,048 na mediana do exterior e **−0,025 num alvo de mata estável definido só com 2017-2024**. Logo **até −0,025 do meu −0,1288 pode ser efeito de cena, não de campo.** | **A magnitude absoluta deixa de passar sozinha.** O que passa é o **contraste foco-menos-controlo**, medido nas mesmas cenas, onde qualquer degrau uniforme de plataforma se cancela: **−0,1152 (ocidental)** e **−0,1100 (oriental)**. A componente de campo do valor absoluto é ≈ −0,104, não −0,129. |

## 3 · REJEITADO

| o que não sobrevive | porquê | o que cai com ele |
|---|---|---|
| **Um halo de decaimento do dano com a distância ao foco.** | ρ de Spearman −0,1233 com p ingénuo 2,23×10⁻⁹ — mas **p = 0,5547 por deslocamento toroidal**, que preserva a autocorrelação espacial do campo e destrói só o alinhamento com a distância. E os anéis não decaem: −0,059 · −0,017 · **+0,015** · −0,027. O do meio é positivo. | Qualquer leitura de frente difusiva. O que resta é compatível com padrão **descontínuo**: sem gradiente contínuo, e com manchas destacadas que descem. |
| **A leitura do radar como cobrindo os dois focos.** | O foco oriental varia de −0,25 a −1,31 dB (órbita 125) e de −0,13 a −1,75 (órbita 147) nos nove primeiros Invernos, e dá −0,82 e −0,67 em 2025-26: **dentro da sua própria banda nas duas órbitas.** O ocidental está numa banda estreita e sai dela nas duas. | A afirmação «o radar confirma os dois focos». O radar confirma **um**. A razão é conhecida e é a mesma que obrigou a dividir o oriental: metade dele é chão, e chão já era baixo no radar nos dez Invernos. |
| **Uma «convergência» entre as duas moedas.** | Os 0,128/0,118 do fosso e os 0,1288/0,1236 do absoluto respondem a perguntas diferentes em **três eixos**: grandeza, estimando (2024→2026 contra patamar-contra-patamar) e unidade. Na mesma unidade e mesmo estimando as duas moedas dão −0,1288 e +0,0808, e diferem **exactamente pelo degrau da referência, −0,0481** — identidade verificada a 10⁻⁹ em cinco unidades. A proximidade numérica é a compensação de dois enviesamentos opostos de tamanho quase igual. | Qualquer figura ou frase que apresente as duas moedas como concordantes. É o mesmo erro que a ronda H1 pagou ao comparar NDRE com NDVI. |

## 4 · NÃO TESTÁVEL

- **A reconstrução da grelha de referência.** Pré-registada em
  `PRE_REGISTO_REFERENCIA.md` (exclusão só por inclusão: 90 m do disco mais 30 m
  de margem justificada em três termos; **não 150 m**, e a justificação de não
  alargar é o negativo do halo). **Não corrida.** *Line-stop já fixado: se os
  fossos ENCOLHEREM com a referência limpa, a leitura de contaminação está
  errada e reabre.*
- **Se o radar vê o copado oriental depois de se lhe tirar o chão.** A unidade
  certificada do radar é o disco inteiro, com a metade sem pérgola dentro.
- **Se há efeito de vizinhança a 90–150 m dos focos.** O t ingénuo diz que sim
  (t=−8,48); o toroidal sobre o pomar diz que não há gradiente. Os dois testes
  discordam e o mais conservador é o que respeita a autocorrelação. Fica aberto.
- **A distinção degrau contra declínio a acelerar** permanece, como a C5 já
  dizia — o ajuste favorece o degrau, mas não exclui aceleração.

## 4b · QUANTIDADES-ÂNCORA — controlo 2, em falta na primeira redacção

O adversário apanhou: a primeira redacção não reportava nenhuma das dez, e o
`CONTROLOS.md` obriga **todas** as camadas a reportá-las «mesmo que não lhes
tenham tocado». Reportam-se os valores **obtidos**, com a divergência assinalada
e **sem corrigir a tabela declarada em silêncio**, como o controlo manda.

| âncora | declarado | obtido nesta camada | divergência |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | — |
| polígono `pomar` | 2 903 px · 29,0 ha | **3 031 px · 30,31 ha** | +128 px · +1,31 ha |
| referência sã | 454 px | **110 px** | −344 px |
| máscara `manchaW` | 427 px | **não existe** | retirada pela C0 — era `nd2026 < 0,76` |
| máscara `zona0` | 220 px | **202 px** | −18 px |
| máscara `nu2021` | — | 167 px | não estava na tabela |
| cenas na série | 11 | 11 | — |
| cenas de plena estação | 9 | 9 | — |
| NDVI médio da referência, 2017-07-02 | 0,838 | **0,888** | **+0,050** |
| NDVI médio da referência, 2026-07-27 | 0,886 | **0,843** | **−0,043** |

**As duas últimas linhas invertem o sinal, e isso não é ruído.** A tabela
declarada diz que a referência **subiu** de 0,838 para 0,886 entre 2017 e 2026;
a referência geográfica desta camada **desce** de 0,888 para 0,843. É a
confirmação numérica da G25 da C0 — *«a referência antiga subia por
construção»* — e é exactamente o género de divergência que o controlo 2 existe
para fazer saltar sem ninguém comparar nada à mão.

**A diferença de contagem da referência (454 → 110)** é de desenho, não de
erro: a antiga eram três manchas contíguas, a nova é uma malha regular de 30 m.
A do polígono (2 903 → 3 031) vem da redefinição geográfica do `pomar`.

---

## 5 · PASSA PARA CIMA — lista fechada

**S1.** **O que passa é o CONTRASTE, não a magnitude absoluta.** Foco menos
controlo, nas mesmas cenas e no mesmo processamento: **−0,1152 (ocidental)** e
**−0,1100 (oriental)**. Um degrau de plataforma cancela-se nesta diferença **na
medida em que for uniforme entre coberturas — e o V10 mostra que não é
inteiramente**: −0,048 na mediana fora do pomar contra −0,025 num alvo de mata
estável. O contraste é portanto **menos exposto, não imune**, com resíduo
possível da ordem de 0,02. *(a magnitude absoluta −0,1288 / −0,1236 inclui a
componente inteira e não sobe sozinha)*

**S1b.** O **sinal e a ordenação** do degrau sobrevivem a 43 análises: ORIENTAL
−0,1274 a −0,0351 (n=23), OCIDENTAL −0,1872 a −0,0542 (n=20), CONTROLO −0,0020
a +0,0009 (n=5). **Nenhuma das 43 muda de sinal, e os intervalos de foco e
controlo não se tocam.** As 43 são **aninhadas**, não independentes. *(amplitude, não valor central)*

**S2.** ~~O degrau ajusta 3,5–4,0 : 1 melhor que a recta.~~ **RETIRADO pelo adversário R2:** o ponto de quebra 2024|2025 foi escolhido depois de ver a série, logo o modelo de degrau tem um parâmetro a mais que a comparação não contabiliza — defeito herdado do 4,35 : 1 da C2. **O que passa é a forma da série sem modelo:** sete cenas entre 0,824 e 0,879, e duas em 0,756 e 0,693.

**S3.** O Landsat replica: −0,1128 e −0,0791, **p exacto 0,0110 = 1/91**;
controlo −0,0012, p=0,978. *(enumeração completa)*

**S4.** A correcção de dia-do-ano é ≤ 0,0011 em qualquer unidade e é um **limite
superior**. O degrau sobrevive: −0,1281 e −0,1247. *(sonda intra-anual)*

**S5.** Os três satélites têm **base 2017-24 normal — 0,878 · 0,872 · 0,901**,
contra 0,867–0,892 nas parcelas do IFAP, e **descem já em 2025**, cena que não
entrou na sua selecção. ~~Percentis 2,4 / 4,7 / 8,7 %~~ — **RETIRADOS pelo
adversário R3:** a nula é sorteada a >120 m dos focos e dois dos três alvos
estão a 83 e 112 m, ou seja noutro estrato de distância. **Três verificações independentes, não
uma família; sob Holm nenhuma passaria — o procedimento pára no primeiro
(0,024 contra 0,0167). Não se corrige, declara-se.** *(n=3)*

**S6.** A referência sistemática está contaminada: 14/110 células dentro dos
focos. A contagem é exacta. **Que daí resulte serem todos os números do fosso
conservadores é INFERÊNCIA, não medição** — o que a mediria é a reconstrução
pré-registada, que não correu. *(contagem exacta; consequência inferida)*

**S7.** **Não há halo.** *(p toroidal 0,55; anéis não monotónicos)*

**S8.** O radar distingue o foco **ocidental** e **não** o oriental, e a razão é
a composição do oriental. *(bandas de nove Invernos, duas órbitas)*

**Tudo o que não está em S1–S8 não passa.**

---

## 6 · NOTA AO ADVERSÁRIO DESTA REVISÃO

Três coisas que ataco eu próprio, para não terem de ser descobertas:

1. **O controlo tem três valores** conforme o que se exclui à volta dos focos:
   −0,0136 (90 m), −0,0096 (120 m + referência), −0,0017 (120 m + Zona 0). Todos
   indistinguíveis de zero, mas **o rácio foco/controlo varia de 9× a 17×
   conforme a linha**. Fixei −0,0136, o mais conservador. A escolha é minha e
   está por auditar.
2. **O disco ocidental tem centro lido do défice de 2026.** Está marcado em
   todas as saídas, e a parcela do IFAP é a versão de fronteira independente —
   mas o número que a maioria das peças cita é o do disco.
3. **Esta revisão foi escrita pela mesma sessão que produziu os factos.** Não é
   um adversário. Precisa de um.
