# Camada 2 — Sinal vegetal · certificado R3

**Data:** 31-08-2026
**Substitui:** `CAMADA_2_CERTIFICADO_R2.md` e `CAMADA_2_TESTES_T1_T5.md`.
**Motivo:** o Controlo 3 exigiu reemissão como certificado — a lista operativa
vivia num ficheiro que não é certificado, logo **não era herdável**. Havia duas
listas fechadas com o mesmo nome e conteúdos diferentes.
**Precedência:** este documento e o `CAMADA_2_CONTROLO3_ADVERSARIO.md` mandam
sobre tudo o que a camada 2 escreveu antes. Onde discordarem, **ganha o
adversário** (emenda de 29-08 à regra 1).

---

## 0 · A PARAGEM DE LINHA DA MOEDA — RETIRADA, e a decisão original REPOSTA

A R2 rejeitou a decisão do adversário da C2 («os números que sobem são o fosso»)
com o fundamento de que a contaminação da referência era um facto novo de 31-08.

**Não era.** O `REDERIVACAO_MASCARAS.md` §3.2 da C0 já continha a contaminação,
os mesmos cinco pontos na `zona0`, a mesma conclusão de conservadorismo e uma
quantificação no §4.4. A C3 tinha-a certificado em 29-08 no B10, com 18 células.

> **A rejeição cai, e a decisão do adversário da C2 é REPOSTA:** a moeda de
> registo é o **fosso**, com as margens que ele exigiu — a amplitude do patamar
> de cada unidade.

**E isto simplifica em vez de complicar.** A contaminação não invalida o fosso:
torna-o **conservador**, como a C0 já dizia. As duas moedas passam a conviver
sem conflito: o fosso é a moeda de registo e é um limite inferior; o nível
absoluto entra como **complemento**, com a ressalva de plataforma do V10.

## 1 · A PARAGEM DE LINHA DO L1 — LEVANTADA, com a palavra que faltava

O `l1_data_do_voo.py` correu em 31-08 e estabeleceu **06-07-2025, 14:34:53 a
14:51:08 UTC**, um só dia, 0,27 h de amplitude, `global_encoding` bit 0 = 1.
A paragem de 29-08 fica formalmente levantada.

**Mas o Controlo 3 acrescentou a palavra que faltava, e é a mais importante
deste documento:**

> A partição operativa `COM = h ≥ 0,5 m` vem de um voo que cai **DENTRO da
> janela do acontecimento**. «Ter pérgola» é, portanto, um estado
> **PÓS-TRATAMENTO**. Se alguma parte do foco oriental foi arrancada e
> re-armada, a partição está a seleccionar **pelo resultado**.

Esta frase acompanha a partição em todo o lado onde ela for usada, e desce à
C3 e à C4 como condição de leitura, não como nota de rodapé.

---

## 2 · CONFIRMADO

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| **O contraste entre foco e controlo, medido nas mesmas cenas e no mesmo processamento.** −0,115 (ocidental) e −0,110 (oriental). | `multiverso_degrau.py`, `degrau_vs_recta_pergola.py` | **não** — Sentinel-2. Ver transversal A | **±0,02 a 0,03**, e o controlo é declarado **contaminado**, não conservador |
| **O sinal e a ordenação do degrau são invariantes em 43 corridas ANINHADAS.** Focos e controlo não se tocam em nenhuma. | `multiverso_degrau.py` | a partição vem do LiDAR — mas ver §1: é pós-tratamento | amplitude; sem valor central |
| **O degrau bate a recta com o ponto de quebra contabilizado.** ΔAICc −6,6 a −7,6 nos focos; **+6,4 no controlo**; nulo do máximo p = 0,003 a 0,023 nos focos e 0,37 nos não-focos. | `t1_ponto_de_quebra.py` | — (decomposição interna) | o nulo permuta a ordem das cenas e procura o seu próprio corte |
| **O Landsat replica a DIRECÇÃO e a DATAÇÃO do degrau.** p exacto 0,0110 = 1/91 nos dois focos; controlo p = 0,978. | `landsat_degrau_absoluto.py` | **sim** — USGS/OLI/LaSRC | **n = 35 (12 inteiros) e 27 (2 inteiros) píxeis.** A palavra «replica» **não** se aplica às magnitudes |
| **A correcção de dia-do-ano é ≤ 0,0011 e é um limite superior.** | `fenologia_por_unidade.py` | reproduz o −0,0162/58 dias do adversário da C2 | com o **sinal do coeficiente por unidade** declarado: a referência desce, o oriental sobe |
| **Os três núcleos satélite tinham base 2017-24 normal** — 0,878 · 0,872 · 0,901 — **e desceram já em 2025**, cena que não entrou na sua selecção. | `satelites_sem_2026.py` | — | medição directa. **O número de satélites não passa** |
| **A reprodução dos números da C2 passa à quarta casa.** OESTE 0,1283 contra 0,128; ESTE plantado 0,1179 contra 0,118. | `emparelhar_moedas.py` | reprodução independente do resultado central | 0,0003 e 0,0001 |
| **O radar distingue o disco ocidental e não o oriental**, e a razão é a composição deste. | `c2_09_sar_verificacao.json` (C2) | **sim** — Sentinel-1, duas órbitas | sobre **discos**, não sobre focos |

## 3 · REJEITADO — o que sai do PASSA PARA CIMA

| o que sai | porquê |
|---|---|
| **S6 inteiro.** «A referência está contaminada, logo os fossos são conservadores — medido pelo T5.» | **O T5 é uma identidade algébrica.** O fosso é `ref − unidade`, logo limpar a referência desloca **todos** os fossos pela mesma constante: as cinco variações são **+0,008430**, idênticas à nona casa. «Cinco fossos cresceram, nenhum encolheu» é **um** número repetido cinco vezes, não cinco confirmações. E o facto não era novo: está no `REDERIVACAO_MASCARAS.md` §3.2 da C0 e no B10 da C3. **O que sobrevive é a coluna dos declives**, que dependem da forma da série e diferem por unidade. |
| **S9 inteiro** (o B1 como comparador sem degrau). | **Zero instrumentos independentes** — sem LiDAR, sem Landsat, sem SAR, sem partição de copado. **A recta ganha porque há tendência**, não porque não houve evento: é um bloco jovem a subir de 0,56 para 0,69 contra 0,82–0,88 nas outras unidades. E o veredicto foi decidido por um limiar **`> -0.03` inventado sem justificação** (`lobulo_oeste_degrau.py`, linha 174). |
| **O p do anel de 90–160 m** (S7). | Mann-Whitney sobre 600 reamostragens **sobrepostas**: os discos partilham células, logo não são independentes e o p < 0,0001 é fabricado. |
| **A afirmação «não há halo»** passa de REJEITADO a **NÃO TESTÁVEL**. | O nulo toroidal roda o campo sobre o rectângulo inteiro e injecta mata e milho nas células do pomar. Sem potência declarada, «não há gradiente» é ausência de prova. |
| **As magnitudes absolutas de S1b.** | O próprio CORRIGIDO da R2 já as tinha recusado, e voltaram na lista fechada. |
| **A palavra «replica» aplicada às magnitudes do Landsat.** | Ver o n acima. |

## 4 · NÃO TESTÁVEL

- **A natureza do foco oriental: copado em declínio, ou copado arrancado e
  re-armado?** *(a pergunta que faltava, transversal B do Controlo 3.)* A C0
  registou 41,4 % da `zona0` como chão lavrado em 2021, 1,04 ha no seu centro.
  **O teste que separa as hipóteses está no `PROTOCOLO.md` como condição de
  arranque e nunca correu:** a prominência de pérgola por autocorrelação radial
  sobre a ortofoto de 2025, o mesmo método do `c2_12_pergola_2012.py`.
  **Enquanto não correr, a C3 e a C4 estão a construir etiologia sobre uma
  unidade cuja natureza não foi estabelecida** — com outra roupa, o mesmo erro
  do lóbulo oeste.
- **O número de acontecimentos entre 2025-08-14 e 2026-07-27.** Onze cenas de
  plena estação por olhar, inventariadas em `t2_cenas_descartadas.json`.
- **Se existe gradiente com a distância.** O nulo toroidal não tem potência
  declarada.
- **O B1 em qualquer instrumento que não seja o NDVI do Sentinel-2.**
- **Se o radar vê o copado oriental sem o chão.**

## 5 · PASSA PARA CIMA — lista fechada, e é esta

**V-R1.** Contraste foco-menos-controlo: **−0,115** e **−0,110**, ±0,02–0,03.
O controlo é **contaminado**, não conservador.

**V-R2.** Sinal e ordenação invariantes em 43 corridas **aninhadas**; focos e
controlo não se tocam.

**V-R3.** O degrau bate a recta com o ponto de quebra contabilizado: ΔAICc
−6,6 a −7,6 nos focos, **+6,4 no controlo**.

**V-R4.** O Landsat replica **direcção e datação**, p exacto 0,0110 = 1/91,
com **n = 35 (12) e 27 (2) píxeis**. Magnitudes não.

**V-R5.** Correcção de dia-do-ano ≤ 0,0011, limite superior, com o sinal por
unidade.

**V-R6.** Os três núcleos tinham **base 2017-24 normal** e desceram em 2025.
Sem número de satélites.

**V-R7.** O radar distingue o **disco** ocidental e não o oriental.

**V-R8.** **A partição pérgola/chão é PÓS-TRATAMENTO** — voo dentro da janela
do acontecimento. Toda a leitura que dela dependa herda isto.

**Tudo o que não está em V-R1 a V-R8 não passa.**

## 6 · TRANSVERSAL A — dois em oito, e vai dito em voz alta

`CONTROLOS.md` controlo 1: um facto sem instrumento independente vai para NÃO
TESTÁVEL, **não** para PASSA PARA CIMA.

Dos oito que passam, **só V-R4 (Landsat) e V-R7 (radar) têm instrumento
independente**. Os outros seis são Sentinel-2 ou decomposições internas.

A leitura benigna — V-R1, V-R2, V-R3 e V-R5 são o mesmo facto visto de quatro
ângulos, e V-R4 e V-R7 confirmam-no — é verdadeira e substancial. A leitura
dura é que **o certificado passa seis factos que a regra manda mandar para NÃO
TESTÁVEL**. Fica escrito, e não diluído.

## 7 · QUANTIDADES-ÂNCORA — controlo 2

| âncora | declarado | obtido | divergência |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | igual | — |
| polígono `pomar` | 2 903 px · 29,0 ha | **3 031 px · 30,31 ha** | +128 px |
| referência sã | 454 px | **110 px** | −344 px (desenho novo) |
| `manchaW` | 427 px | **não existe** | retirada pela C0 |
| `zona0` | 220 px | **202 px** | −18 px |
| cenas na série | 11 | 11 | — |
| cenas de plena estação | 9 | 9 | — |
| NDVI ref. 2017-07-02 | 0,838 | **0,888** | **+0,050** |
| NDVI ref. 2026-07-27 | 0,886 | **0,843** | **−0,043** |

As duas últimas **invertem o sinal**: a tabela declarada diz que a referência
subiu, a geográfica diz que desce. É a confirmação numérica da G25 da C0 —
«a referência antiga subia por construção» — e saltou sem ninguém comparar nada
à mão, que é para isso que o controlo existe.
