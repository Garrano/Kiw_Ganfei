# Camada 3 — Biologia · certificado

29-08-2026. Sessão C3 da cadeia de validação em camadas.

Lidos, por esta ordem: `PROTOCOLO.md`, `CONTROLOS.md`, `CAMADA_3_PROMPT.md`,
`CAMADA_2_ADENDA_LIDAR.md` (que substitui partes do certificado da C2 — onde
discordarem, ganha a adenda) e `CAMADA_2_ADVERSARIO.md` (cujas retiradas se
mantêm todas). Não foi aberto `ganfei_s2\_pacote_cowork\`. Nada foi modificado
em `ganfei_s2\`.

Código e figuras em `SAIDA_C3\`. Onze scripts, dois PNG, oito JSON.

**Correcção de âmbito recebida com a adenda, e cumprida:** a biologia
concentra-se no **v8 / B2, E530485 N4655053** e no seu par de contraste
**v10-v11, «Erica Novo»**; o que se passa a leste é tratado em separado, como
hipótese distinta, porque metade do disco do foco ESTE não tinha pérgola em
06-07-2025. Os focos nomeiam-se sempre com coordenada e válvula ao lado.

---

## ⚠ PARAGEM DE LINHA PARCIAL — um facto da C0 é rejeitado

**Rejeita-se a linha «amostras» da tabela G34 da `CAMADA_0_REVISAO_R2.md`.**

A G34 escreve, e o `CAMADA_3_PROMPT.md` repete em maiúsculas:

> | amostras | FOCO OESTE: as **quatro ITS** (ISFBV0314–17) **e** o «Kiwi 1000» |
> FOCO ESTE: só nemátodes (340/2026) |
> «**É o foco OESTE que está mais amostrado**, e é o ESTE que só tem contagens
> de nemátodes. A frase inversa circulou durante semanas e está morta.»

Nenhuma das quatro amostras ITS, e nenhuma parte do «Kiwi 1000», tem posição.
O próprio livro-fonte diz isso em **três sítios independentes** (coluna
`Location_Confidence` de 35 registos; rodapé da folha `Diversidade ITS`;
pontos 2 e 3 da folha `Pontos a Esclarecer`), e as quatro ITS não têm sequer
data de amostragem — `Sample_Date` = «Not stated in extracted pages» nos 20
registos. Não podem ser atribuídas ao foco OESTE nem a lado nenhum.

**O resto da G34 mantém-se e é confirmado por esta camada:** as coordenadas dos
dois focos, a atribuição a blocos e válvulas, e a leitura de que o foco ESTE
tem as contagens de nemátodes mais baixas dos cinco blocos.

**O que cai com a linha rejeitada:** a tarefa 4 do meu próprio prompt, que pede
que se avalie «a discrepância de esforço» partindo de que o OESTE está mais
amostrado. Está respondida ao contrário, e a resposta é o achado B5 adiante.

**Porque não paro a cadeia inteira.** O que a C0 fez foi asseverar um facto de
biologia — de que amostra veio o quê — com um instrumento que não o alcança. A
camada que possui esse facto é esta. Não há nada por cima que dependa da linha
rejeitada e que eu esteja a construir: a rejeição é o produto. Registo-a com o
destaque que o protocolo exige e **a C4 não pode usar aquela linha**. Se a
cadeia quiser reinício formal em C0, a correcção é de uma linha e as
coordenadas sobrevivem intactas.

---

## CONFIRMADO

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| **Os dois livros são o mesmo livro.** Alinhamento de sequência sobre (ficheiro‖parâmetro) empareja **212 de 212** linhas do `Master Log` com linhas do `Registo Principal`, sem nenhuma linha órfã do lado EN. | `c3_03_alinhamento.py` → `c3_03_alinhamento.json` | `Sample_Date` coincide em **212/212** dos pares — coluna que não entra na chave de alinhamento e que portanto o testa | exacta |
| **`Meloidogyne hapla` está em todo o lado.** Positivo no solo **e** na raiz em 4/4 unidades colocadas e nas 2 sem posição — seis de seis amostras testadas, cinco blocos. | `c3_09_organismos_contra_padrao.py` → `c3_09_organismos.json` | Sentinel-2: positivo tanto na unidade com **2,8 %** de défice (Erica Novo) como na de **46,9 %** (B3). É o satélite que estabelece que não discrimina | 6 amostras, um laboratório |
| **A `Erica Novo` (v10-v11) é o par de contraste limpo.** 5,35 ha, **2,8 %** em défice em 2026, **0,7 %** em declínio novo M2, **0 %** de chão lavrado. | `c3_07_georreferenciar.py` → `c3_07_georreferenciacao.json` | posições de `valvulas_por_area.json` (tabela do gestor, documental) cruzadas com `c2_05_*.npy` (óptico) — duas proveniências | ±10 m sobre a G35 |
| **A `V7` é a amostra mais próxima do foco OESTE, e está a 120 m.** Válvula 7, 3,25 ha, 21,2 % em défice, 21,2 % em declínio novo. Todos os 51 registos colocados no B2 estão nela. | idem | idem | ±10 m |
| **O foco ESTE tem, de facto, as contagens mais baixas** (28 no solo, 37 na raiz; contra 250/65 no B1, 202/72 na V7, 54/78 na Erica Novo, 46/156 no B4). Esta metade da G34 confirma-se. | `Contagens Nemátodos`, informes 339–343/2026 | — nenhum; é leitura directa de um só laboratório numa só data (2026-05-06) | leitura directa |
| **Os dois Becrop não são comparáveis entre si.** Amostragem em **2023-08-25** e **2024-02-04** — 163 dias, fim de Verão contra pleno Inverno. Plataforma, método e matriz iguais (BPP3.5, ITS3/16S4, solo); a época não. | `c3_10_esforco_its_becrop.py` §9 | os próprios relatórios: a categoria «podredumbre radicular» passa de **risco MUITO ALTO detectado** a **«No Detectado»** nos mesmos 163 dias, o que mede a instabilidade do instrumento e não do pomar | documental |
| **A referência sistemática não está limpa.** Contém **12** células do disco OESTE, **6** do disco ESTE, **23** do défice de 2026 e **19** do declínio novo M2, de 110. | `c3_08_controlo_referencia.py` → `c3_08_controlo_referencia.json` | máscara `saudavel` derivada da ortofoto por periodicidade de pérgola (estrutura) cruzada com mapas de NDVI (reflectância) — dois instrumentos | exacta |

---

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| «`Master Log` 212 registos, `Registo Principal` **222**» (prompt C3) | **221**, não 222. E as duas folhas alinham a 212 pares + **9 linhas só no PT** — nove linhas de **Azoto Total (N)**, uma por cada boletim de solo, que o `Master Log` omite por inteiro. Mais **9 registos** em que o EN escreve «n/a (page 2 not extracted)» e o PT tem valor (Fe e Mn de quatro boletins). | **O livro PT é a fonte.** O EN é o mesmo livro com **18 registos incompletos** e zero registos exclusivos. Toda a contagem citável passa a ser sobre 221. |
| «`Pathology Matrix`: **26** organismos × 8 colunas» (prompt C3) | **20 linhas organismo × matriz** no livro PT (23 no EN, com três linhas duplicadas para as colunas do caso espanhol), sobre **15 taxa distintos**. | Nenhuma consequência de fundo; corrige-se para a contagem não voltar a divergir. |
| A nota do próprio livro: «uma análise molecular do solo **posterior** (informe 331/2025) deu Rosellinia NEGATIVO», e `Location_Confidence` do registo 2 diz «Contradito por dados laboratoriais **posteriores**». | O negativo molecular é **anterior**, por catorze meses. Amostragem do informe 331/2025: **2025-06-06**; resultado 2025-07-07. Identificação de campo: **2026-08-04**. | Não é um laboratório a desmentir o campo. É um rastreio de solo feito mais de um ano antes de a planta ser arrancada. A palavra «contradito» sai. |
| «a válvula 27» (prompt C3, tarefa 8) | **Não existe.** Busca exaustiva pelo número 27 isolado nos dois livros: as únicas ocorrências são um `Record_ID` e a data de resultado 2023-06-27. Não há nenhuma menção a válvula, valve ou V27 em nenhum dos 221 registos. | A tarefa não tem objecto nos meus materiais. Se a «válvula 27» existe, entrou por um ficheiro que não me foi dado — ver NÃO TESTÁVEL. |
| «a `Erica 2016 R/E` é o mesmo bloco que a `Erica Novo`?» — lacuna 4 do prompt | Continua a ser inferência, e agora tem um apoio a mais e um limite claro: o sufixo **E** reaparece em `343_Kiwi.pdf` como «Erica Novo E». Mas os dois boletins `Erica 2016` ficam **INFERIDOS**, não confirmados, e são **24 dos 111 registos com posição**. | Se a inferência estiver errada, **21,6 % dos registos colocados mudam de sítio**. Quantifica-se a lacuna em vez de a repetir. |
| O contraste de CaO entre o par v7/B2 (264, 505) e a Erica Novo (879, 1200) lido como diferença de bloco. | A razão entre os extremos mais próximos é **1,7x** — **abaixo** do factor de 2 que a C1 S9 fixa como limiar de interpretabilidade. Comparar pelas médias (382 contra 1040) é escolher o par favorável. | O contraste químico entre o par de contraste **não passa o próprio critério da C1**. Não pode ser usado para separar as duas unidades. |
| V10 / L5: «a referência desce 0,054 de 2024 para 2026 e o viés do S2C explica quase toda a queda». | A descida medida da mediana da referência é **−0,0218**. Retirando as 18 células que caem dentro dos dois discos, é **−0,0096**. **56 % da queda da referência é o próprio acontecimento dentro do denominador.** | O sentido é **conservador**: limpar a referência torna o acontecimento **maior**, não menor. A área em défice de 2026 sobe de 9,47 para 10,32 ha (limiar 0,05, sem abertura). Nenhuma conclusão da C2 se inverte; os números mudam. |

---

## REJEITADO

**A linha «amostras» da G34** — ver a paragem de linha acima. As quatro ITS e o
«Kiwi 1000» não estão no foco OESTE nem em lado nenhum.

**«O foco OESTE está mais amostrado.»** Está ao contrário do que interessa. A
válvula que **contém** o foco OESTE — a v8, com 50,7 % em défice e 47,1 % em
declínio novo — tem **zero** registos de laboratório. O que existe do lado
ocidental está todo na válvula vizinha, a 120 m. Do lado oriental existe uma
amostra de bloco. Nenhum dos dois focos tem uma amostra sua.

**A riqueza de ASV das quatro ITS como grandeza biológica.** A ordenação da
riqueza é **idêntica** à ordenação da profundidade de leitura nas quatro
amostras (ρ de Spearman = **+1,000**). Os índices robustos à profundidade —
Pielou 0,800 a 0,847, Simpson 0,961 a 0,980 — são indistinguíveis entre si.
Não há rarefacção declarada em lado nenhum. **A diversidade não entra em
nenhuma conclusão.**

**A comparação de pontuação entre os dois Becrop (41 → 82) como recuperação.**
Épocas opostas, n = 1 por data, sem parcela associada, freguesia declarada
(Cristelo Covo e Arão) diferente de Ganfei. A diferença mede a época e a
estabilidade da plataforma, não o pomar.

**Os 16 registos do informe 240/2023 (Kiwi Atlántico S.A.), e o registo da
ficha técnica do húmus líquido.** Dezassete registos fora do conjunto. **A
armadilha é o nome:** o talhão espanhol chama-se **«B-3/C-3»** e o pomar de
Ganfei tem um bloco **«B3»**. Cinco organismos — *Dactylonectria* sp.,
*Fusarium* sp., *Ilyonectria liriodendri*, *Rhizoctonia solani* e os oomicetas
de raiz — **só** aparecem nesse informe e não têm nenhuma presença em Ganfei.

**Qualquer atribuição do «Kiwi 1000» a um lugar.** «Kiwi 1000, Lda» é o **nome
do cliente** em 146 dos 221 registos e o nome da conta nos dois PDF da Becrop.
Uma amostra rotulada «Kiwi 1000» está rotulada com o dono, e o dono tem ~50 ha.

---

## NÃO TESTÁVEL

**Onde foi colhido o «Kiwi 1000» (informe 331/2025, amostragem 2025-06-06).**
É o conjunto de patologia mais rico do caso — madeira, raiz e solo numa só
submissão — e é a única origem de **nove** dos vinte resultados organismo ×
matriz. *Faria falta:* a folha de submissão da Areeiro, ou a pergunta ao
técnico que submeteu. Enquanto não existir, *Fusarium cerealis*, *F. equiseti*,
*F. oxysporum* (madeira e raiz), *F. solani*, *Neofusicoccum parvum* (madeira e
raiz), *Ceratobasidium* sp. e *Globisporangium intermedium* **não têm posição**,
e isto não é nota de rodapé: é metade da patologia do caso.

**A que talhão e a que data correspondem as ITS ISFBV0314–0317.** Sem talhão
**e sem data**. *Faria falta:* o formulário de submissão que atribui os códigos
ISFBV.

**Se os dois relatórios Becrop são sequer deste pomar.** Ambos dizem «No hay
parcela asociada» e declaram uma freguesia que não é Ganfei. *Faria falta:*
confirmação do titular da conta.

**A «válvula 27».** Não existe nos meus materiais. *Faria falta:* saber que
ficheiro a introduziu. Assinalo-o porque um número que ninguém consegue
localizar é exactamente como o «B1» entrou.

**Se as três amostras do B1 (250/65 e os três boletins) são do mesmo
porta-enxerto.** O B1 não tem nenhum ponto com posição (R2 G35/G36, raio 343 m)
e tem Summer Kiwi sobre-enxertado nas v2-5 contra pé franco na v1. A contagem
mais alta do caso — **250 J2+ovos/200 cc** — está num bloco que não se pode pôr
no mapa e cujo porta-enxerto não se sabe.

**Se a amostra de raiz de 04-08-2026 ainda existe.** A nota de campo diz que
foi colhida e **não enviada** («não será necessário»). *Faria falta:* perguntar
se está guardada. É a única via para fechar a *Rosellinia*, e é uma pergunta de
uma linha.

**Se a amostra do B3 representa plantas.** Ver B7 adiante. Não é resolúvel com
os documentos que tenho.

**O registo de operações da exploração para o B2 e o B3 em 2024-2026** —
arranque, replantação, poda severa, substituição de pérgola. O adversário da C2
pediu-o e continua por dar. Da minha camada acrescento a razão pela qual me
afecta directamente: sem ele não sei se a amostragem de 2026-05-06 caiu sobre
plantas adultas, sobre replantação, ou sobre chão.

---

## PASSA PARA CIMA — lista fechada

Tudo o que não estiver aqui, não passa.

**B1.** **A fonte é o `Registo Principal` do livro PT, com 221 registos.** O
`Master Log` EN é o mesmo livro com 18 registos incompletos e nenhum exclusivo.
*Prova:* `c3_03_alinhamento.json`, 212/212 pares. *Instrumento independente:*
`Sample_Date` coincide em 212/212 e não entra na chave de alinhamento.
*Margem:* exacta.

**B2.** **Dos 221 registos, 111 têm posição na banda contígua e 110 não têm.**
Dos 110: 53 sem posição declarada pelo próprio documento, 40 no B1 (fora da
banda), 16 do pomar espanhol, 1 ficha de produto. **Sobram 204 registos de
Ganfei.** *Prova:* `c3_07_registos_colocados.csv`. *Instrumento independente:*
a colocação usa `valvulas_por_area.json` (tabela documental do gestor), não o
sinal. *Margem:* ±10 m sobre a G35; 24 dos 111 são INFERIDOS (ver CORRIGIDO).

**B3.** **Nenhum organismo está onde o padrão está.** Vinte linhas organismo ×
matriz: **9 sem posição**, **5 fora do conjunto**, **4 negativos**, **2 em todo
o lado**. Zero na categoria «está onde o padrão está». *Prova:*
`c3_09_organismos.json`. *Instrumento independente:* a classificação cruza
documentos de laboratório com `c2_05_*.npy`, óptico. *Margem:* categórica.

**B4.** **Nove dos vinte resultados vêm de uma só amostra a granel sem posição
e rotulada com o nome do cliente.** É toda a patologia de madeira e quase toda
a de raiz. *Prova:* `c3_10_esforco_its_becrop.json` §5. *Instrumento
independente:* «Kiwi 1000» aparece como `Client_Titular` em 146 registos e como
nome de conta nos dois PDF da Becrop — plataforma terceira. *Margem:* exacta.

**B5.** **A válvula que contém o foco OESTE não tem nenhuma amostra.** A v8 —
E530499 N4655022, a 46 m do centróide da sua própria partição, 2,78 ha, **50,7 %
em défice em 2026 e 47,1 % em declínio novo M2, 0 % de chão lavrado** — tem
**zero** registos. A amostra colocada mais próxima está na v7, a **120 m**, numa
unidade com 21,2 % de défice. *Prova:* `c3_10_esforco_its_becrop.json` §4.
*Instrumento independente:* posições documentais × mapas ópticos. *Margem:*
±10 m.

**B6.** **A amostragem não foi dirigida pelo padrão.** ρ de Spearman entre o
défice de 2026 da válvula e o número de registos colocados nela = **−0,044,
p = 0,89, n = 12**. *Prova:* idem. *Instrumento independente:* as duas séries
têm proveniências distintas (documental e óptica). *Margem:* p declarado.
**Isto é o negativo que interessa:** a coincidência entre biologia e padrão não
pode ser artefacto de selecção, porque não há selecção — mas também não há
cobertura onde o padrão está.

**B7.** **A única amostra biológica do lado oriental é um composto de bloco
sobre 9,92 ha, dos quais 16,3 % são chão lavrado.** O informe 340/2026 diz «B3»
e o B3 são as válvulas 12-15; dentro dele a v13 tem **22,6 %** de chão lavrado e
a v14 **13,8 %**. **A contagem de 28/37 não pode ser atribuída a plantas do foco
ESTE.** *Prova:* `c3_07_georreferenciacao.json`, partição por válvula.
*Instrumento independente:* a máscara `nu2021` vem de ortofoto (estrutura), a
partição vem da tabela do gestor (documento), a contagem vem do laboratório —
três. *Margem:* ±10 m; e a fracção de chão é a de 2021, que a adenda de LiDAR
mostra ser um sub-cálculo do que havia em 06-07-2025.

**B8.** **As quatro ITS não são comparáveis entre si, e a diversidade não entra
em nenhuma conclusão.** Profundidade filtrada de 4 964 a 25 078 (5,1x) sobre
brutas de 85 773 a 251 395; qualificadas de **2,8 % a 29,2 %** (10x). Riqueza de
ASV 129 a 281 com ρ = **+1,000** contra a profundidade; Pielou 0,800-0,847 e
Simpson 0,961-0,980 indistinguíveis. *Prova:* `c3_10_esforco_its_becrop.json`
§6, figura `C3_F2`. *Instrumento independente:* nenhum — é uma propriedade
conhecida dos estimadores de riqueza, não uma medição. Passa porque a
**conclusão é negativa**: retira um dado, não o afirma. *Margem:* ρ exacto.

**B9.** **A *Rosellinia* tem duas amostras, e o negativo molecular é anterior
por catorze meses.** Campo: 2026-08-04, raiz, uma planta arrancada, local não
especificado, identificação macroscópica, amostra **não enviada**. Molecular:
2025-06-06, **solo**, composto «Kiwi 1000», sem posição. **Não é a mesma planta,
não é a mesma matriz, e não é depois.** *Prova:* `c3_06_rosellinia.txt`,
registos 2 e 17. *Instrumento independente:* as datas estão em campos separados
dos dois livros e coincidem nos dois. *Margem:* exacta.

**B10.** **O controlo T1 que o adversário da C2 exigiu antes de a C3 arrancar
disparou, e a consequência está medida.** Os quatro números são 12, 6, 23 e 19
de 110 — nenhum é zero. Efeito: a queda da mediana da referência de 2024 para
2026 passa de **−0,0218** para **−0,0096** ao retirar as 18 células dentro dos
discos, isto é, **56 % da queda é o acontecimento dentro do denominador**. **O
sentido é conservador:** com a referência limpa o défice de 2026 sobe de 9,47
para 10,32 ha. *Prova:* `c3_08_controlo_referencia.json`. *Instrumento
independente:* máscara de estrutura (ortofoto) × série de reflectância
(Sentinel-2). *Margem:* ±0,001 NDVI na mediana.

**B11.** **Toda a amostragem com posição é posterior ao acontecimento.** As
doze amostras físicas colocadas são de **2026-03-03 (4), 2026-05-06 (4),
2026-06-17 (2) e 2026-07-08 (2)** — nenhuma anterior a Março de 2026. O degrau
de NDVI e a anomalia de VV são de 2025-2026 (V2, V3). **Não existe nenhuma
amostra biológica com posição colhida antes do acontecimento**, e as duas
únicas amostras anteriores a 2026 do caso inteiro — o «Kiwi 1000» de 2025-06-06
e os dois Becrop de 2023-2024 — são precisamente as que não têm posição.
*Prova:* `c3_07_registos_colocados.csv`, agrupado por `Source_File`.
*Instrumento independente:* as datas vêm dos números de informe do laboratório,
que são independentes do conteúdo do resultado. *Margem:* exacta. **Consequência
para quem vier a seguir: não há linha de base biológica. Nenhuma comparação
antes/depois é possível com estes materiais.**

---

## Quantidades-âncora

| âncora | declarado | obtido pela C3 | nota |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | — |
| polígono `pomar` | 30,31 ha | **30,31 ha** | bate |
| referência sistemática | 1,10 ha / 110 células | **1,10 ha / 110** | bate — mas ver B10 |
| banda contígua | 27,30 ha | **30,31 ha** | **objectos diferentes**: a minha partição por válvula cobre o polígono `pomar` inteiro; a G35 dá a área da tabela do gestor. Não é divergência |
| total da tabela do gestor | 44,93 ha | não recalculado | documental, fora da minha camada |
| chão lavrado `nu2021` | 1,67 ha | **1,67 ha** | bate |
| défice de 2026 | 7,86 ha | **7,86 ha** | lido de `c2_05_defice_2026.npy` |
| declínio novo M2 | 3,58 ha | **3,58 ha** | lido de `c2_05_novo_m2.npy` |
| **número de registos** | 212 / 222 declarados | **221** | ver CORRIGIDO |
| **registos com posição** | — | **111** | novo |
| **registos sem posição** | — | **110** | novo |
| **organismos distintos** | 26 declarados | **15 taxa** em **20** linhas organismo × matriz | ver CORRIGIDO |

---

## Nota ao adversário que não vou ter

O controlo 3 não corre em C3. Escrevo na mesma os quatro pontos onde eu
atacaria este certificado, e não os escondo no fim de propósito.

**1 · A partição por válvula mais próxima é minha e não está validada.** As
posições das válvulas são pontos com ±10 m declarados (G35); eu construí à
volta delas uma partição de Voronoi que atribui **todas** as 3 031 células do
pomar a alguma válvula. Isso dá fronteiras nítidas onde a realidade tem tubos.
Os números por unidade — 50,7 %, 46,9 %, 2,8 % — herdam essa arbitrariedade. A
comparação que **não** herda é a ordenação, e é essa que uso.

**2 · Todo o B5 depende de a v8 estar onde a G35 diz.** Se a colocação por área
acumulada estiver deslocada uma válvula, a v7 passa a conter o foco e o
«buraco» desaparece. O que sobrevive nesse cenário é mais fraco mas ainda serve:
nenhum ponto de amostragem tem coordenada própria em todo o caso.

**3 · Os 111 registos «com posição» são 111 linhas, não 111 amostras.** Um
boletim de solo dá doze linhas. Em amostras físicas são **doze** — seis
boletins de solo, uma análise foliar, um painel regenerativo e quatro lotes de
nemátodes/patologia. Reportei linhas porque a âncora pede linhas; quem inferir
densidade de amostragem a partir de 111 vai errar por um factor de nove.

**4 · Não fiz a pergunta ao B4.** A lacuna 5 do meu prompt continua aberta: o
B4 tem as válvulas 16-17 na banda **e** a parcela solta B4C3 sem posição, e o
boletim não distingue. Classifiquei os 16 registos como AMBÍGUOS e usei a
posição da banda. Se estiverem na parcela solta, o B4 sai do mapa — e o B4 é uma
das quatro unidades da correlação nemátodes × défice, que já só tem n = 4.

---

## O que esta camada não escreveu, e porquê

Não há diagnóstico diferencial, não há exclusão de causas, não há etiologia.
Três resultados apontaram-me para causas e ficam por escrever: são C4.

O que digo, e é a resposta à tarefa 10 do meu prompt: **a biologia disponível
não distingue os dois focos.** Não por escassez de resultados — há 204 registos
de Ganfei — mas porque os resultados que têm posição não discriminam
(*M. hapla*, em todo o lado, com a contagem mais baixa no bloco mais afectado)
e os que discriminariam não têm posição (as nove linhas do «Kiwi 1000»). E o
único sítio do caso onde há planta viva a definhar sobre chão que nunca foi
lavrado — a válvula 8 — nunca foi amostrado.
