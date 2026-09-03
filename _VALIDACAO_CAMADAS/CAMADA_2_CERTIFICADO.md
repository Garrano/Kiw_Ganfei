# Camada 2 — Sinal vegetal · CERTIFICADO

Sessão C2, 29-08-2026. Código, dados intermédios e quatro figuras em `SAIDA_C2\`.

**Não há paragem de linha.** Nenhum facto herdado da R2 ou da C1 foi rejeitado.
A série geográfica reproduz-se valor a valor, e os dois números da C1 que esta
camada podia contradizer — os −1,107 dB e os −0,774 dB do Inverno de 2025-26 —
reproduzem-se à terceira casa a partir de um descarregamento independente das
441 cenas. Três factos herdados são **precisados**, e um deles muda de leitura
sem mudar de sinal.

**Herança usada.** `CAMADA_0_REVISAO_R2.md` e o suplemento G34–G37,
`CAMADA_1_CERTIFICADO.md` (S1–S20) e `REGISTO_DE_NOMES.md`. O
`CAMADA_0_CERTIFICADO.md` não foi usado como fonte de factos. Nenhuma série do
B1 foi produzida, lida ou usada; nenhum nível de NDVI foi comparado entre o B1 e
o corpo principal; a linha térmica não foi tocada.

**Vocabulário.** Os focos identificam-se por coordenada, como a G34 obriga.
Onde o vocabulário antigo aparece num ficheiro herdado, a tradução está
declarada em cada script: **`zona0` = FOCO ESTE**, **`manchaW` (retirada) =
FOCO OESTE**.

**A definição de défice, fixada nesta camada e usada em tudo o que se segue:**
uma célula está em défice numa data se o seu NDVI estiver abaixo da média da
referência sistemática **dessa mesma data** menos 0,05, depois de uma abertura
morfológica 2×2. É uma diferença dentro da cena, e por isso é imune a qualquer
degrau radiométrico de cena — o que abaixo se verá que importa. Núcleos são
componentes ligados por vizinhança-8 com pelo menos 15 células (0,15 ha).
A sensibilidade a estas escolhas está medida, não assumida (`c2_03`, `c2_05`).

**Uma alteração de composição da série, e a sua razão.** A série de plena
estação passa a ter **dez** cenas, não nove: repõe-se **2019-09-02**. A R2 G10
certifica que a exclusão dela «continua sem justificação» — e de facto o
dia-do-ano 245 dista dois dias do 243 que se manteve. Repor não é rejeitar um
facto: é resolver um item que a camada de baixo deixou explicitamente aberto.
Todos os resultados abaixo são dados com e sem ela; nenhum depende da escolha,
mas a cena de 2019 é o que fixa a barra de erro de toda a série (ver V11).

---

## CONFIRMADO

| facto | ficheiro e cálculo que o prova | INSTRUMENTO INDEPENDENTE | margem |
|---|---|---|---|
| **A série com máscaras geográficas reproduz-se por inteiro.** Os quatro níveis absolutos, os dois fossos, os nove valores de défice e todos os centróides de núcleo de `_serie_geografica.txt` saem iguais a todas as casas impressas, a partir das máscaras de `masks_geograficas.json` e das cenas de `sentinel\*.tif`. | `c2_01_serie.py` §b–d contra `_serie_geografica.txt` | reprodução de uma execução anterior por caminho próprio; as áreas das máscaras batem com as que a C1 mediu por outro código (3031 / 110 / 202 / 167 células) | exacta |
| **As quatro contagens de máscara declaradas na abertura da cadeia reproduzem-se todas, e o «conflito conhecido» do `CONTROLOS.md` resolve-se.** Rasterizando os polígonos de `masks.json` em coordenadas de píxel: `pomar` **2903**, referência das três manchas **454** (264+119+71), `manchaW` **427**, `zona0` **220** — os valores declarados, ao píxel. Os valores «booleanos» que circularam (2906/446/423/219) são de outra rasterização e não são os dos polígonos. | `c2_10_ancoras.py` | os polígonos vêm de um ficheiro que esta camada não escreveu, e a rasterização é feita por `matplotlib.path`, não pelo código que os gerou | exacta |
| **Os dois valores de NDVI da tabela-âncora reproduzem-se, e são da referência ANTIGA.** Referência das três manchas: **0,8379** em 2017-07-02 e **0,8862** em 2026-07-27 — os 0,838 e 0,886 declarados. A referência sistemática dá **0,8884** e **0,8425**. A inversão de sinal da R2 G6/G25 confirma-se: não é divergência, são objectos diferentes. | `c2_10_ancoras.py` | as duas máscaras têm proveniências independentes (desenho manual antiga; grelha sistemática sobre pérgola detectada na ortofoto) | leitura directa |
| **A circularidade do `masks.json` antigo vale +0,0077 NDVI por ano.** A referência antiga sobe +0,00375/ano; a sistemática desce −0,00395/ano. A diferença de declives é **+0,00769/ano**, ou **+0,069 NDVI** sobre os 9,1 anos da série. Ponta a ponta a diferença é **+0,093**, que é o «cerca de 0,09» da R2 G6 — os dois números estão certos e são estimadores diferentes. E 52 % das células da `manchaW` antiga têm NDVI 2026 abaixo de 0,76, o limiar que a definiu. | `c2_01_serie.py` §e | a máscara sistemática foi derivada da ortofoto por periodicidade, sem nenhum NDVI | declives declarados |
| **A fenologia não explica a curva em U, e a sonda que a testa é interna à própria série.** Entre 2025-06-17 (DOY 168) e 2025-08-14 (DOY 226) — mesmo ano, mesmo pomar, 58 dias — o défice varia **−0,39 ha**, isto é −0,0067 ha/dia, e no **sentido contrário** ao que a objecção exigiria. Os 21 dias de DOY que separam 2017 (183) de 2024 (204) valem por isso **0,14 ha**, contra os 5,17 ha do ramo. E 2024 (DOY 204) e 2026 (DOY 208) distam **quatro dias**: a fenologia explica **0,5 %** do salto de 4,95 ha. | `c2_02_fenologia.py`, sondas A e B | a sonda é a cena de 2025-06-17, que a série exclui e que nunca entrou em nenhum resultado anterior | ±0,4 ha |
| **A área em défice de 2017 e a de 2026 não são o mesmo objecto — nem em profundidade nem em lugar.** Ao limiar 0,05 são 8,08 e 7,86 ha; ao limiar 0,20 são **5,72 e 1,94 ha**; ao 0,25, **5,37 e 0,32 ha** (rácio 17); ao 0,30, **4,91 e 0,11 ha** (rácio 45). E não se sobrepõem: IoU(2017, 2026) = **0,29**; só 45 % das células de 2017 estão em défice em 2026. | `c2_03_defice.py` §1 e §2 | ver a linha seguinte: a pérgola na ortofoto | ±1 célula |
| **As 5,37 ha em défice grave em 2017 não tinham pérgola em 2010 nem em 2012, e tinham-na em 2021.** Prominência do primeiro pico secundário da autocorrelação radial da luminância, em janela de 40 m, medida **dentro de cada imagem isoladamente**: em 2010, aquela área dá **−0,024** contra **0,253** da referência sistemática (p = 7e-59) e 0,204 do resto do pomar (p = 2e-205); em 2012, **−0,022** contra 0,220 (p = 2e-61) e 0,155 (p = 7e-213); em 2021, **0,043** contra 0,045 — indistinguível da referência (p = 0,11). | `c2_12_pergola_2012.py` sobre `orto\ortos2010`, `ortos2012`, `ortos2021` | **a ortofoto DGT é um instrumento sem relação com o Sentinel-2**, e a medida é de ESTRUTURA (periodicidade espacial), não de nível — logo é imune ao equilíbrio do JPEG que a R2 G37 identificou. Duas épocas dão o mesmo resultado em separado | p declarado |
| **E o NDVI dessa mesma área passa de 0,498 (2017) a 0,753 num ano e a 0,826 em 2020.** Um ganho de 0,26 NDVI em doze meses não é recuperação de declínio; é copado a instalar-se. Em 2026 essa área está a 0,780 — acima do pomar inteiro. | `c2_03` §1 e a verificação directa das mesmas células ao longo da série | a pérgola, linha acima | ±0,01 |
| **O chão lavrado de 2021 já estava despido em 2017, no óptico.** **166 das 167 células** de `nu2021` (99 %) estavam em défice na cena de 2017, contra 27 % do pomar em geral; 89 % delas estavam em défice **grave** (< referência − 0,25). | `c2_03_defice.py` §2 | a C1 chegou ao mesmo por **radar** (S13: 1,2 a 3,5 dB abaixo da referência em todos os dez Invernos desde 2016-17). Dois instrumentos, dois princípios físicos, a mesma datação negativa | ±1 célula |
| **De 2024 para 2026 o pomar não se deslocou: dispersou-se.** O fosso médio do pomar à referência é **−0,0292 em 2024 e −0,0290 em 2026** — não mexe. A mediana **melhora** (−0,0016 → +0,0215). O que muda é a cauda: desvio-padrão 0,076 → 0,102, assimetria −2,98 → −1,21. Um contrafactual que desloque a distribuição de 2024 para a média de 2026 dá **4,78 ha** de défice, contra 9,58 ha observados: a deslocação explica **0 %** do aumento. | `c2_03_defice.py` §3 | — (interno ao óptico; é uma decomposição, não um facto novo) | exacta |
| **Os dois focos caem juntos, na mesma janela, pela mesma quantidade, e o resto do pomar não cai.** Degrau de nível entre o patamar de 2017-2024 e as duas cenas de 2025-2026: **foco OESTE −0,1426**, **foco ESTE plantado −0,1439**, **pomar sem os dois discos −0,0204**. O modelo de degrau bate o modelo linear por 4,35 : 1 (ESTE) e 4,05 : 1 (OESTE) em soma de quadrados, com o mesmo número de parâmetros; para o resto do pomar os dois modelos são indistinguíveis (1,03 : 1). | `c2_06_este_plantado.py` | para o foco OESTE, o **Sentinel-1** (linha seguinte). Para o foco ESTE, **não há** — ver NÃO TESTÁVEL | ±0,01 NDVI |
| **A pilha SAR desta camada reproduz a C1 S15 à terceira casa.** 441 cenas descarregadas de novo do Planetary Computer, dez Invernos, órbitas 125 e 147. Foco OESTE menos pomar inteiro: nos nove primeiros Invernos **−0,165 a +0,482** (órbita 125) e **−0,301 a +0,365** (órbita 147); no Inverno de 2025-26, **−1,107 dB** e **−0,775 dB**. A C1 declara −1,107 e −0,774. | `c2_07_sar_pilha.py` + `c2_09_sar_verificacao.py` §a | descarregamento e agregação independentes dos da C1, a partir da mesma colecção; as duas órbitas concordam | ±0,001 dB na reprodução |
| **O cruzamento NDVI × SAR passa, sobre uma partição que não conhece os focos.** Em 81 mosaicos de 60 m do pomar, a queda de NDVI 2024→2026 correlaciona com a anomalia de VV do Inverno de 2025-26 a **ρ = +0,57 a +0,60** (p < 1e-7). Nos nove Invernos anteriores, ρ vai de −0,22 a +0,31. Três placebos de NDVI (2022→2024, 2020→2022, 2018→2020) contra o Inverno de 2025-26 dão −0,05, +0,27 e +0,11. Permutação com 5000 reatribuições: p < 0,0002, máximo do nulo +0,426. As duas órbitas dão +0,514 e +0,455 em separado (ambas p < 1e-4). | `c2_08_cruzamento.py`, `c2_09_sar_verificacao.py` §b | **Sentinel-1 RTC banda C, retrodifusão activa de Inverno, contra Sentinel-2 óptico de Verão** — instrumentos, princípios físicos e estações diferentes | ρ e p declarados |
| **E o cruzamento não é obra dos dois focos.** Retirando os 25 mosaicos a menos de 130 m de qualquer dos dois centros, sobram 56 e a correlação mantém-se: **ρ = +0,429, p = 0,0010**. | `c2_09_sar_verificacao.py` §b | idem | idem |
| **A válvula 8 destaca-se sozinha nos dois instrumentos.** Sobre a partição de Voronoi das doze posições de `valvulas_por_area.json`: a válvula com a maior anomalia negativa de VV no Inverno de 2025-26 é a **v8 (−0,660 dB)**, e a seguinte é a v7 com **−0,135 dB** — quase cinco vezes menos. A válvula com a maior queda de NDVI 2024→2026 é também a **v8 (−0,0822)**. O centróide da v8 fica a **43 m** do centro declarado do foco OESTE. | `c2_08_cruzamento.py`, secção final | a partição vem da **tabela de áreas do gestor** (R2 G35), documento externo a todo o sensoriamento remoto; os dois rankings vêm de instrumentos diferentes | ±10 m sobre a G35 |
| **O núcleo do foco OESTE emerge sozinho, e a emergência é robusta.** Em 15 combinações de limiar (0,03 a 0,15) × elemento estruturante (nenhum, 2×2, 3×3), o núcleo está **ausente em 2024 e presente em 2026 em 13**; nas outras 2 (limiar 0,03, o mais frouxo) já há um germe de 0,19–0,27 ha em 2024. Está ausente em **todas as 15** de 2017 a 2023. Na definição operativa: ausente até 2023, **0,09 ha em 2024**, 1,11 ha em 2025, 2,69 ha em 2026, com o centróide a convergir de 39 m para 14 m para 1 m do centro declarado. | `c2_05_manchas.py` §A | o SAR data o mesmo momento no mesmo sítio (linhas acima) | ±0,15 ha |
| **A fracção satura e a magnitude não — medido.** Fracção de células em défice no disco ESTE: 54 % (2017) → 54 % (2024) → 83 % → **94 %** (2026), enquanto a magnitude fica entre 0,065 e 0,185 sem tendência. No disco OESTE a fracção vai de 0 % (2021-2022) a **85 %**. A R2 G31 está certa, e o modo de falha é o descrito: a fracção move-se quando a magnitude não se move, e satura quando ela ainda tem margem. | `c2_03_defice.py` §5 | — (é uma propriedade da métrica, não um facto de terreno) | exacta |
| **Metade da descida da referência é da cena, não do pomar.** As duas cenas de NDVI mais baixo da série são as **duas únicas do S2C** (2025-08-14 e 2026-07-27). Contra oito cenas anteriores, o degrau é **−0,050** na referência sistemática, **−0,048** na mediana de tudo o que está fora do pomar e **−0,025** num alvo de mata estável de 24,3 ha fora do pomar definido **só com as cenas de 2017-2024**. Corrigido por esse alvo, o declive da referência passa de −0,0044/ano para **−0,0028/ano, p = 0,16**. | `c2_04_referencia.py` | os alvos são terreno **fora** do pomar, e a identificação do satélite vem de `proveniencia.json`, documento que não entra em nenhum cálculo | ±0,01 NDVI |
| **A regra M2 dá 3,58 ha de declínio novo em 2026.** Das 7,86 ha em défice em 2026, **3,58 ha** nunca estiveram em défice em nenhuma das oito cenas de 2017 a 2024; 4,28 ha já lá tinham estado. Sob um critério mais duro (nunca em défice **e** NDVI de 2024 acima de referência − 0,02) restam **2,60 ha**. Os núcleos do declínio novo: **2,02 ha a 24 m do foco OESTE**, e **1,41 ha em três manchas a 62, 72 e 167 m do foco ESTE**. | `c2_05_manchas.py` §B | para os 2,02 ha do OESTE, o SAR; para os 1,41 ha do ESTE, **não há** | ±0,15 ha |
| **Datando célula a célula, 5,20 das 7,86 ha do défice de 2026 entraram em 2025 ou 2026.** 2,65 ha entraram em 2025 e lá ficaram; 2,55 ha entraram em 2026; 1,59 ha estão em défice continuamente desde 2017. Dentro de 120 m do foco ESTE, **1,62 das 3,40 ha em défice em 2026 são novas desde 2025** — o foco ESTE também tem um acontecimento de 2025. | `c2_05_manchas.py` §D | — | ±1 célula |
| **O núcleo oriental de 2020 a 2024 é, na maior parte, chão despido.** A fracção do núcleo junto ao foco ESTE que é chão lavrado de 2021: **53 % em 2020, 60 % em 2022, 78 % em 2024** — e **34 % em 2026**, porque em 2026 ele cresceu para dentro de copado plantado. | `c2_06_este_plantado.py`, secção final | a máscara `nu2021` vem da ortofoto de 2021, e o SAR da C1 (S13/S14) separa a mesma área | ±1 célula |
| **O resto do pomar fechou o fosso à referência ao longo da série.** Pomar sem os dois discos: fosso de 0,092 (2017) para 0,020 (2024), declive **−0,00773/ano até 2024, p = 0,015**. Até 2024 este é o único sinal com tendência significativa em toda a série. | `c2_06_este_plantado.py` | a pérgola nas ortofotos de 2010/2012 explica a origem: parte do pomar estava a instalar-se | p declarado |

### Quantidades-âncora (CONTROLOS.md, controlo 2)

`c2_10_ancoras.py` · ficheiro `c2_10_ancoras.json`.

| âncora | declarado | obtido em C2 |
|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | **igual**, nas 11 imagens; grelha 200×100 de 10 m |
| cenas na série | 11 | **11** no acervo |
| cenas de plena estação | 9 | **10 defensáveis** — ver o cabeçalho; a exclusão de 2019-09-02 (DOY 245, contra 243 mantido) não tem base |
| polígono `pomar` (antigo) | 2903 px / 29,0 ha | **2903 px / 29,03 ha** |
| polígono `pomar` (operativo, R2 G2) | 30,31 ha | **3031 células / 30,31 ha** |
| referência sã, 3 manchas (antiga) | 454 px | **454 px** (264 + 119 + 71) |
| referência sistemática (R2 G4) | 1,10 ha / 110 células | **110 células / 1,10 ha** |
| máscara `manchaW` (antiga) | 427 px | **427 px** — a máscara está retirada (R2 G4); reproduzida só para medir a circularidade |
| máscara `zona0` | 220 px | **220 px** no polígono antigo; **202 células / 2,02 ha** na operativa |
| NDVI da referência, 2017-07-02 | 0,838 | **0,8379** (referência antiga) · **0,8884** (sistemática) |
| NDVI da referência, 2026-07-27 | 0,886 | **0,8862** (referência antiga) · **0,8425** (sistemática) |
| chão lavrado de 2021 | 1,67 ha | **1,67 ha / 167 células** |
| banda contígua (R2 G35) | 27,30 ha | **27,30 ha** (soma das válvulas 6-17) |
| total da tabela (R2 G35) | 44,93 ha | **não verificável aqui**: 27,30 medido + 17,66 declarado sem posição = 44,96 (igual à C1) |
| disco OESTE r = 90 m (C1) | 248 células / 2,48 ha | **248 / 2,48 ha** |
| disco ESTE r = 90 m (C1) | 255 células / 2,55 ha | **255 / 2,55 ha** |
| cenas Sentinel-1 de Inverno (C1) | 441 | **441**, dez Invernos, órbitas 125 e 147 |
| dVV foco OESTE, Inverno 2025-26, órbita 125 (C1 S15) | −1,107 dB | **−1,107 dB** |
| dVV foco OESTE, Inverno 2025-26, órbita 147 (C1 S15) | −0,774 dB | **−0,775 dB** |
| — âncoras novas desta camada — | | |
| défice do polígono, 2026 | 7,86 ha | **7,86 ha** ao limiar 0,05; **0,32 ha** ao limiar 0,25 |
| défice do polígono, 2017 | 8,08 ha | **8,08 ha** ao limiar 0,05; **5,37 ha** ao limiar 0,25 |
| declínio novo pela regra M2, 2026 | — | **3,58 ha** (2,60 ha no critério duro) |
| ρ do cruzamento NDVI × SAR, Inverno 2025-26 | — | **+0,573 a +0,603** sobre 81 mosaicos cegos |

Nenhuma divergência sem explicação. As duas únicas linhas em que o obtido não
é o declarado são as cenas de plena estação (mais uma, e a razão está dada) e o
total da tabela (44,96 contra 44,93, exactamente como a C1, e pela mesma razão:
17,66 ha continuam declarados sem posição).

---

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| **R2 G28 e o achado central:** «O evento é de 2025. Défice no polígono: 8,08 ha (2017) → 4,05 (2020) → 2,91 (2024) → 5,43 (2025) → 7,86 (2026). **O pomar melhora seis anos e duplica em dois.**» | Os números estão todos certos e reproduzem-se ao centésimo. **A frase que os liga não está.** Os dois ramos da curva não são o mesmo fenómeno medido duas vezes: são dois fenómenos diferentes que se cruzam no mesmo número por acaso do limiar. O ramo descendente é **instalação de pomar** — 5,37 das 8,08 ha de 2017 são terreno sem pérgola em 2010 e 2012, com NDVI 0,498 que sobe 0,26 num só ano. O ramo ascendente é **declínio de copado adulto**, e é extenso e moderado: ao limiar 0,25 tem 0,32 ha contra as 5,37 ha de 2017. Os dois «8 ha» sobrepõem-se em IoU 0,29. | **A curva em U deixa de ser o achado.** O achado é a metade direita dela. Nenhuma camada acima pode dizer «o pomar recuperou e recaiu», nem tratar 2017 como uma linha de base de saúde, nem falar de «regresso ao estado de 2017». A afirmação que sobrevive, e que é mais forte por ser mais estreita, está em V2 e V5. |
| **R2 G28, «seis anos a melhorar».** | Não são seis anos de melhoria progressiva. Com a cena de 2019 reposta, a série é 8,08 · 6,90 · **3,77** · 4,05 · 3,34 · 3,16 · 3,08 · 2,91 — uma queda entre 2018 e 2019 e depois um patamar entre 2,9 e 4,1 ha durante seis anos. E entre 2018-08-31 e 2019-09-02, duas cenas a **dois dias de dia-do-ano uma da outra**, o défice varia **3,13 ha**. | Não muda nenhuma conclusão, mas fixa a barra de erro que faltava a toda a série: **uma cena por ano não resolve diferenças de défice abaixo de ~3 ha**. Aplicado ao caso: o salto de 2024 (2,91) para 2026 (7,86) é de 4,95 ha e sobrevive; qualquer leitura de um único degrau intermédio da série não sobrevive. |
| **R2 G30 e C1 S12:** «a parte plantada da Zona 0 cai −0,0150/ano, p = 0,032». | O número reproduz-se (**−0,0156/ano, p = 0,016** com 2019 reposto) e a significância aguenta com a definição de défice fixada. Mas **a recta é o modelo errado**: contra um modelo de patamar-e-degrau com o mesmo número de parâmetros, a recta perde por **4,35 : 1** em soma de quadrados. A descrição certa é: plano entre 0,848 e 0,890 durante oito cenas (declive −0,0023/ano, p = 0,38), e um degrau de **−0,144** em 2025-2026. | A prosa da R2 G30 já dizia «plana de 2017 a 2024 e cai significativamente depois» — está certa e é a leitura a usar. **O número −0,0150/ano não deve voltar a ser citado como taxa de declínio**: não há nenhum ano em que aquela unidade tenha caído 0,015. Cair 0,144 em dois anos e estar parada nos oito anteriores é outra afirmação. |
| **R2 G34 e `REGISTO_DE_NOMES.md`:** o foco ESTE «aparece na série desde 2020 (2,01 ha)» e o OESTE só em 2025; e a discrepância entre isso e o relato da gestora é «a coisa mais interessante do caso». | O núcleo oriental **está** na série desde 2020, mas 53 a 78 % dele é **chão despido**, não copado em declínio — e esse chão já estava despido em 2017 no óptico e desde 2016-17 no radar (C1 S13). A parte **plantada** do foco ESTE está plana até 2024 e cai em 2025-2026, **na mesma janela que o OESTE e pela mesma quantidade**. | A frase «o foco ESTE é o mais antigo na série» tem de passar a dizer **de que**: é o mais antigo em *chão sem copado*, e não é mais antigo em *declínio de copado*. A discrepância com o relato da gestora **atenua-se muito**: se a «Zona 0» é onde o declínio de plantas começou, o satélite diz 2024-2025 nos dois focos e não contradiz o relato em nenhum sítio onde haja copado. |
| **R2 G6/G25:** «a referência sistemática desce, −0,00395/ano. Este é o facto mais importante desta revisão.» | Continua verdade que a referência **antiga** subia por construção, e essa é a parte importante e insubstituível da G25. Mas a descida da nova é **cerca de metade efeito de cena**: as duas cenas mais baixas da série são as duas únicas do S2C, e o mesmo degrau (−0,048) aparece fora do pomar. Contra um alvo de mata estável fora do pomar, o declive cai para −0,0028/ano, p = 0,16 — **não significativo**. | Nenhuma camada acima pode ler «a referência desce» como «o pomar todo está a declinar». Isso já estava vedado pelo `_saudavel_limite` («referência interna: não pode detectar declínio uniforme do pomar»), e agora está vedado por medição. **A métrica de défice e a magnitude não são afectadas**: usam a referência da própria data, dentro da mesma cena. |
| **R2 G14:** o teste de cobertura refeito «dentro de uma só imagem (2025)» dá referência 91,5 %, Mancha W 80,8 %, Zona 0 64,2 %. | O **sentido** reproduz-se na luminância (referência 155,3 contra 145,0 no foco OESTE). Mas a radiometria da ortofoto de 2025 não é interpretável **nem dentro da própria imagem**: o NDVI calculado dela sobre copado de kiwi fechado em pleno Verão dá **0,09** (fisicamente impossível; o Sentinel-2 dá 0,83 nas mesmas células duas semanas depois), e a ordenação das oito unidades pelo NDVI da ortofoto está **invertida** face ao Sentinel-2 (ρ = **−0,62**). | A conclusão da G14 («a cobertura não explica o padrão») não cai — mas deixa de ter esta medição a sustentá-la. **Nenhuma medida de nível radiométrico de ortofoto deve ser usada para vigor, nem dentro de uma imagem.** O que sobrevive da ortofoto é a **estrutura** — periodicidade de pérgola —, que é imune ao equilíbrio do JPEG por não usar o nível do sinal, e que nesta camada separa unidades com p ~ 1e-200. |

---

## REJEITADO

| o que não sobrevive | porquê | que conclusões acima caem com ele |
|---|---|---|
| **A leitura de que a área em défice de 2017 mede saúde de pomar.** | Metade dela não era pomar. 5,37 das 8,08 ha não têm assinatura de pérgola nas ortofotos de 2010 nem de 2012, medida dentro de cada imagem e com p entre 1e-59 e 1e-213; têm-na em 2021; e o seu NDVI sobe 0,26 num ano. A R2 G11 já tinha lido isto como «copado a fechar»; aqui deixa de ser leitura e passa a ter instrumento. | Cai qualquer uso de 2017 como linha de base de saúde do pomar, e qualquer taxa de recuperação calculada a partir dela. Cai a comparação directa entre os 8,08 ha e os 7,86 ha. **Não cai** o facto de que aquelas células estavam em défice — estavam, e a medição está certa; cai o que se lhe atribuía. |
| **A curva em U como objecto único.** | Só existe ao limiar mais raso. Ao limiar 0,20 é 5,72 / 1,44 / 1,94 ha (2017 / 2024 / 2026) e ao 0,25 é 5,37 / 0,98 / **0,32** — em 2026 há **menos** área gravemente deficitária do que em 2024. A forma da curva é uma propriedade do limiar, não do pomar. | Cai «o pomar duplica o défice e volta ao estado de 2017». Sobrevive, e fica mais preciso: **o acontecimento de 2025-2026 é extenso e moderado — acrescenta muita área a profundidade média e nenhuma a profundidade grave.** Isso é uma caracterização utilizável, e é diferente de «duplicou». |
| **A radiometria das ortofotos como instrumento de vigor, incluindo dentro de uma só imagem.** | Ver CORRIGIDO, linha da G14: NDVI próprio de 0,09 sobre copado fechado, e ordenação invertida face ao Sentinel-2 (ρ = −0,62) sobre as mesmas oito unidades. A R2 G37 tinha proibido a comparação entre épocas; o que aqui se acrescenta é que **dentro** de uma época também não serve. | Cai a medição de 91,5 / 80,8 / 64,2 % da G14 e qualquer percentagem de cobertura tirada de ortofoto. **Não cai** a detecção de pérgola nem a máscara `nu2021`: as duas são medidas de estrutura. |
| **A ideia de que o foco ESTE é um declínio antigo e progressivo.** | A sua parte plantada não tem tendência até 2024 (−0,0023/ano, p = 0,38) e o modelo de degrau bate o linear por 4,35 : 1. A antiguidade do núcleo oriental é antiguidade de **chão despido**, e esse chão é anterior a toda a série óptica e a todo o radar disponível. | Cai qualquer cronologia que ponha o início do declínio de plantas no foco ESTE em 2020 ou 2021, e cai a assimetria «o ESTE é antigo, o OESTE é recente» como afirmação sobre plantas. **Não cai** nada de C1 S12-S14: a distinção física daquele chão continua estabelecida, e continua anterior a 2021. |

---

## NÃO TESTÁVEL

| o que não se conseguiu verificar | o que faria falta |
|---|---|
| **A queda do foco ESTE em 2025-2026 não tem instrumento independente, e o radar positivamente não a vê.** No Inverno de 2025-26 o disco ESTE está a −0,819 / −0,670 dB do pomar, valores **dentro** do seu próprio intervalo dos nove Invernos anteriores (−0,25 a −1,31 e −0,13 a −1,75). As válvulas do bloco B3 têm anomalias de VV **positivas** nesse Inverno (v13 +0,471, v14 +0,162, v15 +0,124). Isto não refuta a queda de NDVI — o kiwi é caduco e o VV de Inverno mede sobretudo solo, pérgola e lenho, como a C1 avisa — mas significa que **o degrau de −0,144 do foco ESTE é uma medição de um só instrumento**. | Uma segunda medição óptica de outra proveniência (Landsat 8/9, PlanetScope), ou fotografia de campo datada, ou uma contagem de plantas mortas por linha com data. Uma ortofoto entre 2021 e 2025 teria resolvido isto e não existe. |
| **Não se consegue dizer se o degrau de 2025-2026 é uma queda ou o princípio de uma queda.** A série termina em 2026-07-27. Um degrau medido com duas cenas depois da quebra não distingue «caiu e estabilizou» de «está a cair». | Cenas de 2027 em diante. É espera, não trabalho. |
| **Quando é que as 5,37 ha sem pérgola foram plantadas.** Sabe-se que não havia pérgola em 2012 e que havia em 2021; que em Julho de 2017 o NDVI era 0,498 e em Agosto de 2018 já 0,753; que em 2020 estava em 0,826. Isso põe a plantação entre 2012 e 2017, provavelmente 2014-2016, mas **não há ortofoto entre 2012 e 2021** e o intervalo não fecha mais. | A data de plantação, do gestor. É uma pergunta de uma linha e resolve nove anos de incerteza sobre a idade de 18 % do pomar. |
| **Se o défice de VV de Inverno do foco OESTE é do solo ou do coberto.** A C1 deixou esta em aberto (S15, NÃO TESTÁVEL) e esta camada não a fecha. O que esta camada acrescenta é que o **lugar** deixou de ser circular: a correlação corre sobre 81 mosaicos cegos e sobrevive à remoção dos mosaicos dos dois focos. Mas saber que os dois instrumentos concordam no sítio e no momento não diz qual das duas grandezas físicas mudou. | Humidade de solo medida, ou SAR de época de folha (Maio-Setembro) separado do de Inverno, ou coerência interferométrica. |
| **Se as 3,13 ha de variação entre 2018 e 2019 são ruído de medição ou variação real do pomar.** As duas cenas distam dois dias de dia-do-ano e um ano de calendário. Não há maneira, com uma cena por ano, de separar «o instrumento e a atmosfera variam» de «o pomar variou naquele ano». | Uma série densa — todas as cenas sem nuvem de cada estação, não uma por ano — que dê a variância intra-estação. É trabalho de gabinete e está por fazer. Sem ela, a barra de erro de ~3 ha tem de ser tratada como o pior caso. |
| **Se o degrau do S2C é calibração ou atmosfera.** Mediu-se que o degrau existe fora do pomar e que vale cerca de metade da descida da referência. Não se mediu de onde vem. | Cenas do S2A ou S2B nas mesmas datas de 2025 e 2026, ou os relatórios de calibração da missão. A cena de 2025-06-17 (S2A) já está baixa, o que sugere que não é só do S2C. |
| **A idade e o compasso planta a planta.** Toda esta camada mede área e nível, não plantas. Uma célula de 10 m com metade das plantas mortas e uma com todas debilitadas dão o mesmo NDVI. | Contagem por linha, no campo. Vale sobretudo nos 3,58 ha de declínio novo. |
| **Existe um NDVI de terceiros e não foi usado.** A folha «Drone-NDVI Log» do `Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx` regista três capturas de ecrã da plataforma Becrop, de 2026-08-22, com camadas de NDVI por quadrante e contínuo sobre o polígono da exploração. Seria um instrumento óptico de proveniência independente para o padrão de 2026, que é exactamente o que falta a V2 do lado oriental. **Não o testei**: são capturas de ecrã sem georreferenciação e sem sobreposição de códigos de talhão, e a própria folha assinala essa limitação. Registo a omissão em vez de a esconder. | O ficheiro georreferenciado por trás daquelas camadas, ou a exportação do NDVI da plataforma. É um pedido ao fornecedor, não trabalho de gabinete. |

---

## PASSA PARA CIMA

Lista fechada. **O que não estiver aqui, não existe para as camadas acima.**
Vocabulário do `REGISTO_DE_NOMES.md`: os focos identificam-se por coordenada.

**V1.** A série operativa é a de `masks_geograficas.json` e reproduz-se por
inteiro. O défice define-se como **NDVI abaixo da referência sistemática da
própria data menos 0,05, com abertura 2×2**; é uma diferença dentro da cena e
por isso imune a degraus radiométricos. A série de plena estação tem **dez**
cenas: as nove usadas até aqui mais **2019-09-02**, cuja exclusão a R2 G10
declarava sem justificação. *(exacta)*

**V2. O acontecimento é de 2025-2026, e atinge os dois focos ao mesmo tempo e
na mesma medida.** Contra o patamar de 2017-2024, o nível de NDVI dá um degrau
de **−0,1426 no foco OESTE** e **−0,1439 na parte plantada do foco ESTE**,
enquanto o resto do pomar dá **−0,0204**. O modelo de degrau bate o linear por
4 : 1 nos dois focos e empata no resto do pomar. Até 2024 nenhum dos dois focos
tem tendência significativa. **A frase «o foco ESTE declina desde 2020» é falsa
para plantas**; o que existe ali desde antes da série é chão sem copado. *(±0,01
NDVI. Para o foco OESTE há instrumento independente — V3. Para o foco ESTE
**não há**: ver NÃO TESTÁVEL.)*

**V3. NDVI e SAR datam o mesmo acontecimento nos mesmos sítios, e o lugar já
não é circular.** Sobre 81 mosaicos de 60 m do pomar — geometria pura, sem
NDVI e sem as coordenadas dos focos — a queda de NDVI 2024→2026 correlaciona
com a anomalia de VV do Inverno de 2025-26 a **ρ = +0,57 a +0,60** (permutação
p < 0,0002; nulo máximo +0,426). Nos nove Invernos anteriores ρ ∈ [−0,22,
+0,31]; três placebos de NDVI dão −0,05, +0,27, +0,11; as duas órbitas dão
+0,51 e +0,46 em separado. **Retirando os 25 mosaicos a menos de 130 m dos dois
focos, sobrevive: ρ = +0,429, p = 0,0010, n = 56.** *(ρ e p declarados)*

**V4. A válvula 8 destaca-se sozinha, nos dois instrumentos.** Sobre a partição
de Voronoi das doze posições de `valvulas_por_area.json` — proveniência
documental, externa a todo o sensoriamento remoto — a v8 tem a maior anomalia
negativa de VV do Inverno de 2025-26 (**−0,660 dB**, contra −0,135 da segunda) e
a maior queda de NDVI 2024→2026 (**−0,0822**). O seu centróide fica a 43 m do
centro declarado do foco OESTE. É o teste que a C1 pediu em S15, e passa.
*(±10 m sobre a G35)*

**V5. Os 8,08 ha de 2017 e os 7,86 ha de 2026 não são o mesmo objecto.** Ao
limiar 0,25 são **5,37 e 0,32 ha**; ao 0,30, 4,91 e 0,11; IoU entre os dois
mapas **0,29**. O acontecimento de 2025-2026 é **extenso e moderado**:
acrescenta área a profundidade média e **nenhuma** a profundidade grave. Nenhuma
camada acima pode usar 2017 como linha de base de saúde nem falar de
«recuperação e recaída». *(±1 célula)*

**V6. Pelo menos 5,37 ha do polígono `pomar` (18 %) foram plantados depois de
2012.** Não têm assinatura de pérgola nas ortofotos de 2010 nem de 2012
(prominência −0,024 e −0,022 contra 0,253 e 0,220 da referência, p = 7e-59 e
2e-61, medida dentro de cada imagem), têm-na em 2021, e o seu NDVI vai de 0,498
em Julho de 2017 a 0,753 treze meses depois. **O pomar tem pelo menos duas
idades de plantação separadas por nove anos ou mais**, e a mais nova está
concentrada a E530600–530800, entre os dois focos. *(p declarado; a data exacta
de plantação está em NÃO TESTÁVEL)*

**V7. O chão lavrado de 2021 já estava despido em 2017.** 166 das 167 células
de `nu2021` (99 %) estavam em défice na cena de 2017, contra 27 % do pomar; 89 %
delas em défice grave. Isto estende ao **óptico**, e recua a 2017, a datação
negativa que a C1 fez por **radar** (S13). A lavra de 2021 não criou aquele
contraste, e nem o óptico nem o radar conseguem datar o que o criou. *(±1
célula)*

**V8. 3,58 ha passam a regra M2 — declínio novo sobre terreno comprovadamente
são.** Das 7,86 ha em défice em 2026, 3,58 ha nunca estiveram em défice em
nenhuma das oito cenas de 2017 a 2024 (2,60 ha sob o critério duro). Repartem-se
em **2,02 ha a 24 m do foco OESTE** e **1,41 ha em três manchas a 62, 72 e 167 m
do foco ESTE**. É esta a área sobre a qual faz sentido perguntar por uma causa
recente; as outras 4,28 ha têm história anterior. *(±0,15 ha)*

**V9. A grandeza operativa é a magnitude, e a fracção está medida a falhar.** A
fracção do disco ESTE vai de 54 % (2017) a 54 % (2024) a **94 %** (2026)
enquanto a magnitude fica entre 0,065 e 0,185 sem tendência; a do disco OESTE
vai de 0 % a 85 %. Toda a comparação temporal usa referência-menos-máscara,
**sempre reportada com o nível absoluto ao lado**. *(exacta)*

**V10. O nível absoluto não pode carregar uma afirmação sobre o pomar todo.**
As duas cenas de NDVI mais baixo da série são as duas únicas do S2C, e o degrau
delas aparece igualmente fora do pomar (−0,048 na mediana do que está fora,
−0,025 num alvo de mata estável definido só com 2017-2024). Corrigida por esse
alvo, a descida da referência é **−0,0028/ano, p = 0,16** — não significativa.
A métrica de défice e a magnitude não são afectadas. *(±0,01 NDVI)*

**V11. A barra de erro da série é ~3 ha, e vem medida.** Entre 2018-08-31 e
2019-09-02 — **dois dias** de dia-do-ano de intervalo, um ano de calendário — o
défice do polígono varia **3,13 ha**. Uma cena por ano não resolve diferenças
abaixo disso. O salto de 2024 (2,91 ha) para 2026 (7,86 ha) é de 4,95 ha e
sobrevive à barra; nenhum degrau isolado do patamar de 2019-2024 sobrevive. E a
fenologia **não** é a explicação: 58 dias de dia-do-ano medidos dentro de 2025
valem −0,39 ha, e as cenas de 2024 e 2026 distam quatro dias. *(±0,4 ha na
calibração fenológica)*

---

## Nota ao adversário

Esta camada leva adversário, e há quatro sítios onde eu próprio atacaria
primeiro. Ficam nomeados para poupar tempo a quem vier atacar.

1. **V2, metade oriental.** O degrau do foco ESTE é de um só instrumento, e o
   segundo instrumento disponível — o radar de Inverno — positivamente não o vê.
   Está declarado em NÃO TESTÁVEL, mas a linha entre «não vê porque é caduco» e
   «não vê porque não está lá» não foi medida, e eu não sei medi-la com o que
   existe.
2. **V6 e a definição do `pomar`.** Se 18 % do polígono foi plantado depois de
   2012, então o polígono `pomar` da R2 G2 — derivado da ortofoto de 2021 por
   periodicidade de compasso — descreve o pomar de 2021, e foi aplicado sem
   alteração às cenas de 2017 e 2018. Isso está certo para medir *aquele*
   terreno ao longo do tempo, e está errado se alguém ler «percentagem do pomar»
   nas cenas antigas como percentagem do pomar que existia então. Não corrigi o
   polígono; assinalo o uso.
3. **V3 e a escolha do par de anos.** O X do cruzamento é a queda 2024→2026.
   Escolhi-o por ser a janela do acontecimento, o que é uma escolha informada
   pelo resultado. Os três placebos e o teste de permutação existem por causa
   disso, e o placebo mais próximo (2020→2022) dá ρ = +0,27 contra +0,57 — a
   margem é real mas não é enorme.
4. **V10 e o alvo T2.** As células de mata estável foram escolhidas por média
   alta e variância baixa em 2017-2024. Seleccionar por média alta induz alguma
   regressão à média fora da amostra, o que **inflaciona** o degrau que atribuo
   à cena. O viés vai no sentido de eu subestimar a descida real da referência,
   não de a exagerar; mas está lá.

---

## Entregas desta camada

```
_VALIDACAO_CAMADAS\
  CAMADA_2_CERTIFICADO.md       este ficheiro
  CAMADA_3_PROMPT.md            prompt da camada da biologia
  SAIDA_C2\
    c2_00_comum.py              geometria, máscaras, definição de défice
    c2_01_serie.py              reprodução da série; medição da circularidade antiga
    c2_02_fenologia.py          o ataque do dia-do-ano; sondas de 2025 e de 2019
    c2_03_defice.py             profundidade, lugar, forma, sensibilidade, saturação
    c2_04_referencia.py         o degrau do S2C contra alvos fora do pomar
    c2_05_manchas.py            emergência do foco OESTE, regra M2, frente, datação
    c2_06_este_plantado.py      degrau contra recta; o que o núcleo oriental tem dentro
    c2_07_sar_pilha.py          441 cenas Sentinel-1, célula a célula
    c2_08_cruzamento.py         o cruzamento sobre partições cegas; as válvulas
    c2_09_sar_verificacao.py    reprodução da C1 S15; especificidade e permutação
    c2_10_ancoras.py            quantidades-âncora
    c2_11_figuras.py            F1-F4
    c2_12_pergola_2012.py       pérgola nas ortofotos de 2010, 2012 e 2021
    c2_13_coberto_2025.py       o negativo: a radiometria da ortofoto não serve
    C2_F1_serie.png             a série, e de que a curva em U é feita
    C2_F2_mapas.png             mapas de défice e o declínio novo pela regra M2
    C2_F3_cruzamento.png        NDVI × SAR sobre 81 mosaicos cegos; as válvulas
    C2_F4_metodo.png            o degrau do S2C e a saturação da fracção
    c2_*.json / .npy            resultados intermédios; a pilha SAR tem 35 MB
```

Nada em `ganfei_s2\` foi modificado.
