> ### Corrigido a 03-09-2026 pelo Controlo 3
> Este documento continua válido no essencial — a retirada do A3 e a inversão da
> REG-01 resistiram a tudo o que o adversário lhes atirou. **Quatro números e
> uma frase estão errados aqui**, e a versão certa está na `LISTA_FINAL` e em
> `REG01_CONTROLO3_ADVERSARIO.md`:
>
> · **margem 0,023 → 0,0200** (0,023 é a do foco oriental; quem governa a frase
>   é o ocidental);
> · **«percentil 0 %» duas vezes → 3,2 % e 6,5 %** na ordenação conjunta de 31;
> · **«três do 472062, com forma de replantação» → invertido:** são campo aberto
>   até 2021 e pérgola nova em 2025, e um deles *ganhou* coberto;
> · **«aplicado cego aos 37» → sai.** Os cinco já tinham sido identificados pela
>   ortofoto antes de o critério correr;
> · **falta o intervalo:** P(ordenação errada) = 0,07 por cenas, 0,25 por anos, e
>   retirado 2026 a conclusão cai.

# RETIRO o A3. Os cinco blocos do 297313 foram desmatados em 2024 — e a REG-01 inverte-se

**Data:** 01-09-2026 · **Retira:** `REG01_RESULTADO.md` e
`REG01_LANDSAT_REPLICACAO.md`, e o **A3** da `LISTA_FINAL`.
**Instrumentos:** ortofoto DGT 2025 (50 cm) + série anual Landsat (100 cenas).

---

## 1 · O QUE EU ESCREVI, E COM QUE CONFIANÇA

Ontem: *cinco blocos de kiwi do ENT 297313 com degrau de −0,21 a −0,40, duas a
quatro vezes pior do que os focos de Ganfei.* E hoje de manhã dei-lhe o segundo
instrumento: Landsat, 100 cenas, os mesmos cinco nos cinco piores lugares,
**Spearman ρ = +0,890**. O `guarda.py` autorizou o veredicto — **a primeira vez
nesta cadeia sem a marca de NÃO TESTÁVEL.**

Estava errado.

## 2 · O QUE A ORTOFOTO MOSTROU

Fracção de píxeis abaixo do percentil 10 dos **doze blocos do mesmo dono**,
medida **dentro de cada imagem** (imune ao esticamento do WMS):

| CUL_ID | ha | 2007 | 2010 | 2012 | 2018 | 2021 | **2025** |
|---|---|---|---|---|---|---|---|
| 6705427 | 1,28 | 0,0 % | 0,0 % | 0,0 % | 0,6 % | 0,3 % | **14,3 %** |
| 6705428 | 1,02 | 0,0 % | 0,0 % | 0,0 % | 0,9 % | 0,1 % | **44,0 %** |
| 6705429 | 2,28 | 0,1 % | 0,0 % | 0,0 % | 1,7 % | 1,1 % | **35,8 %** |
| 6705432 | 2,31 | 0,2 % | 0,0 % | 0,1 % | 2,4 % | 0,7 % | **15,3 %** |
| 6705442 | 0,62 | 0,0 % | 0,0 % | 0,0 % | 1,2 % | 0,4 % | **20,9 %** |
| **mediana dos DOZE** | | 0,1 % | 0,0 % | 0,0 % | 2,3 % | 1,3 % | **1,0 %** |

**Os cinco, todos. Os doze, nenhum.**

## 3 · O QUE A SÉRIE ANUAL DATOU

Nível absoluto no Landsat, mediana das cenas de Verão de cada ano:

| | 2017 | … | 2022 | **2023** | **2024** | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| 6705427 | 0,865 | | 0,812 | **0,854** | **0,418** | 0,430 | 0,420 |
| 6705429 | 0,877 | | 0,841 | **0,877** | **0,426** | 0,472 | 0,407 |
| 6705428 | 0,832 | | 0,814 | **0,854** | **0,420** | 0,457 | 0,448 |
| 6705432 | 0,879 | | 0,839 | **0,875** | **0,473** | 0,525 | 0,491 |
| 6705442 | 0,858 | | 0,828 | **0,869** | **0,461** | 0,533 | 0,531 |

> **Em 2023 estavam no ponto mais alto de toda a sua série. Em 2024 estavam em
> 0,42.** Um ano, sem precursor, e depois estabilizam no domínio do solo — a
> série NU21 já certificada neste caso dá 0,49 a 0,61 para chão lavrado.

## 4 · PORQUE É QUE O MEU DEGRAU MEDIU ISTO

O degrau era `média(2025-26) − média(2017-2024)`. **O colapso é de 2024, e 2024
estava do lado PRÉ da fronteira.** Uma mudança de uso a cavalo da fronteira dos
períodos produz exactamente o número que eu publiquei, sem que nada tenha
declinado em 2025-26.

E a réplica em Landsat replicou-o **porque estava a medir a mesma coisa errada**.

> ### A lição, e é maior do que este caso
> **Dois instrumentos independentes concordarem não valida a definição da
> unidade.** O controlo 1 exige instrumento independente para o *sinal*; nada na
> cadeia exigia verificação da *unidade ao longo do tempo*. Um ρ de 0,890 entre
> duas agências, dois sensores e duas correcções atmosféricas não viu isto, e
> não podia.
>
> A ressalva estava escrita — a guarda de cultura de `reg01_landsat.py` diz que
> a declaração do IFAP cobre uma campanha e que «a continuidade da cultura ao
> longo da linha de base NÃO está verificada; um bloco arrancado ou replantado a
> meio da série produz um degrau que não é sintoma». **Estava no código que eu
> corri, e eu publiquei o resultado à mesma.**

## 5 · A FORMA DA QUEDA SEPARA REMOÇÃO DE DECLÍNIO

| | 2023 | 2024 | 2025 | 2026 | forma |
|---|---|---|---|---|---|
| 6705427 | 0,854 | **0,418** | 0,430 | 0,420 | **um ano, sem precursor** |
| 6705429 | 0,877 | **0,426** | 0,472 | 0,407 | **um ano, sem precursor** |
| **foco OCIDENTAL** | 0,888 | 0,884 | 0,829 | **0,723** | **progressivo, dois anos** |
| **foco ORIENTAL** | 0,794 | 0,821 | 0,761 | **0,724** | **progressivo, dois anos** |

Os cinco caem 0,43 num ano a partir do valor mais alto da sua série e param em
0,42. Os focos de Ganfei descem 0,17 em dois passos e estão em **0,72** — muito
acima do chão. **Um copado a rarear não é um copado que foi retirado.**

Isto **não exclui** que a remoção tenha sido decidida por causa de um problema
sanitário. Exclui que os cinco sejam uma instância do acontecimento de 2025-26:
no Verão anterior à remoção o copado estava normal e indistinguível dos doze.

## 6 · A REG-01, REFEITA

Critério de exclusão, escrito antes de correr e aplicado **cego aos 37 blocos**:
queda ≥ 0,25 entre anos consecutivos **dentro de 2017-2024** *e* nível médio
posterior < 0,60 (limiar herdado da série NU21, não inventado agora).

**Saem 8 blocos** — os cinco do 297313 e **três do próprio ENT 472062**
(8845729, 8845731, 8845739), que caem e recuperam, com forma de replantação.
Ficam 29.

| | degrau | percentil |
|---|---|---|
| **foco OCIDENTAL** | **−0,0839** | **0 %** |
| **foco ORIENTAL** | **−0,0869** | **0 %** |
| pior bloco sobrevivente (6705424) | −0,0638 | 3 % |

> ### **Os dois focos de Ganfei são o pior e o segundo pior da região.**
> **A conclusão da REG-01 inverte-se: H1 não cai. O acontecimento de 2025-26 é,
> entre as unidades com linha de base contínua, específico desta exploração.**

Margem: 0,023 abaixo do pior bloco sobrevivente. É primeiro e segundo, não é
primeiro por muito.

## 7 · O LIDAR — não foi possível, e não é um resultado negativo

As folhas MDS/MDT-50cm-**157557**-07-2025 existem no catálogo da DGT (20,6 e
20,1 MB). **O endpoint de descarga passou a redirigir para autenticação**
(Keycloak, `auth.cdd.dgterritorio.gov.pt`) — e falha inclusive na folha 157563,
descarregada com sucesso a 29-08-2026. Não se contornou.

Fica registado como **acesso perdido**, não como teste. A resposta veio da
ortofoto (outro serviço, WMS público) e da série anual.

**Consequência a registar:** o LiDAR de Ganfei que sustenta a partição
pérgola/chão veio deste mesmo endpoint. **Não é re-descarregável hoje.** Os
ficheiros locais continuam válidos; a via de reprodução por terceiros não.

## 8 · O QUE MUDA

| era | passa a ser |
|---|---|
| **A3** · «há blocos vizinhos muito piores» | **RETIRADO.** Eram desmatação de 2024 |
| REG-01 · «não é exclusivo desta exploração» | **INVERTIDO.** É o pior da região |
| «contactar o ENT 297313» — acção 1 | **cai.** Não há sintoma partilhado para comparar |
| «campanha com pontos nas duas explorações» | **cai.** Volta a ser uma exploração |
| «nenhuma medida irreversível antes da REG-01» | a condição está fechada, e agora **suporta** medida de parcela |

E acrescenta-se uma acção que não existia:

> **Triagem de descontinuidade em qualquer comparação futura entre parcelas.**
> `reg01_triagem_descontinuidade.py` faz isto em minutos e devia correr **antes**
> de qualquer estatística de degrau, não depois.

## 9 · A CONTA

Este é o **décimo nono** veredicto retirado, e o primeiro que tinha passado o
`guarda.py` com instrumento independente concordante. O portão fez o que devia
com a informação que tinha; **o que lhe faltava era uma condição sobre a unidade,
não sobre o instrumento.**

Passa a fazer parte do portão: um facto que compare unidades ao longo do tempo
tem de declarar que a **identidade da unidade** foi verificada nesse intervalo.
