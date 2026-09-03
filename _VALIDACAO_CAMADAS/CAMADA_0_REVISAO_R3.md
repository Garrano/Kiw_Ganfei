# Camada 0 — revisão R3 do certificado

**Data:** 31-08-2026 · **Escreve:** sessão Claude Code
**Precedência:** esta R3 ganha sobre a R2 e sobre o certificado da C0, pela
mesma regra com que a R2 ganhava sobre o certificado.

**Porque existe.** Três factos de geometria e proveniência foram produzidos em
31-08-2026 e ficaram fora da cadeia. Dois fecham entradas que a C0 tinha
deixado em NÃO TESTÁVEL; um descarrega uma paragem de linha em vigor desde
29-08 que bloqueava tudo o que dependia dela. Nenhum é análise nova de sinal —
são todos geometria, documento e proveniência, que é o que compete a esta
camada.

---

## 1 · DESCARREGADA a paragem de linha do L1 — a data do voo tem cálculo em disco

`ADVERSARIO_2026-08-29.md`, veredicto, textual:

> «**Não passa nada que dependa de L1 enquanto L1 não tiver o cálculo em
> disco.** São duas linhas de `laspy`. Enquanto não existirem, o facto fundador
> desta adenda tem o mesmo estatuto epistémico que a pasta `sentinel_b1\` tinha
> em 27 de Agosto: provavelmente certo, e sem prova.»

**Estava certo: o cálculo não existia.** Uma varredura por `laspy`, `gps_time`
ou `adjusted standard` em todos os `.py` do projecto devolvia zero ficheiros. A
data esteve três dias em circulação, entrou em figuras, e ancora a partição
pérgola/chão de que depende toda a camada 2 revista.

**Corrido em 31-08-2026.**

| facto | ficheiro e cálculo | margem |
|---|---|---|
| **O voo LiDAR das duas folhas decorreu em 06-07-2025, entre as 14:34:53 e as 14:51:08 UTC.** Bit 0 de `global_encoding` = 1 nas duas, logo os tempos são *Adjusted Standard GPS Time*: GPS padrão = valor + 1e9, UTC = época 1980-01-06 mais os segundos menos 18 de saltos. 16 636 497 pontos em LO-158565 e 17 761 266 em LO-159565. Amplitude de **0,27 h em cada folha**, e **um só dia** em ambas. | `l1_data_do_voo.py` → `l1_data_do_voo.json` | ±1 s no instante; a amplitude é medida, não estimada |

**Correcção que sai daqui, e aplica-se a quem já usou a frase:** «14h35» é o
**início**, não um instante. A forma dizível é «6 de Julho de 2025, entre as
14h35 e as 14h51 UTC». Já corrigida na peça que a usava.

**O que isto liberta:** tudo o que dependia de L1 deixa de estar suspenso.

## 2 · FECHA a NÃO TESTÁVEL do bloco sudoeste — G19

A C0 escreveu, em NÃO TESTÁVEL:

> «**Se o bloco de 16,4 ha a sudoeste (E529350–530085, N4653700–4654478)
> pertence à exploração.** … a assinatura de rede não prova propriedade.»

e nomeou o que resolveria: **«a tabela de válvulas com áreas, ou a confirmação
da gestora sobre a M1 v2, ou o parcelário»**. O parcelário existia e ninguém o
tinha trazido a esta pergunta.

| facto | ficheiro e cálculo | margem |
|---|---|---|
| **Dezasseis parcelas têm centróide no bloco, somando 19,00 ha.** Destas, **seis são do ENT 472062 — o beneficiário do corpo principal — e somam 13,23 ha.** As restantes 5,77 ha repartem-se por **sete outros beneficiários**. | `g19_parcelario.py` → `.json`, sobre `ifap_parcelas.json` | a C0 mediu 16,4 ± 2 ha por assinatura de rede; 19,00 medido por polígono administrativo |
| **Há 12,64 ha de KIWI declarado (código 124) no bloco, em seis polígonos, e os seis caem em parcelas do ENT 472062.** Sem excepção. Nenhum dos outros sete beneficiários declara kiwi ali — declaram milho, aveia, pastagem, nabo. | idem, cruzamento espacial polígono-de-cultura × parcela | exacto sobre a declaração de campanha 2025 |
| **A lacuna de área fecha.** 30,31 ha do polígono do pomar + 12,64 ha aqui = 42,95, contra os 44,93 da tabela do gestor e os 44,36 declarados ao IFAP pelo ENT 472062. | `ifap_exploracao_total.json` | 1,98 ha por explicar, contra 15,9 antes |

**VEREDICTO: o bloco é, na sua maior parte, da mesma exploração.** A NÃO
TESTÁVEL fecha, e fecha para o lado que **não** dá controlo externo: as 12,64 ha
de kiwi ali são da mesma gestão. **O caso continua sem qualquer controlo
externo contemporâneo de kiwi**, e agora sabe-se por medição e não por omissão.

**Ressalva que viaja com o facto:** o ENT_ID é o beneficiário declarado numa
campanha. Prova pertença administrativa; **não prova rede de rega partilhada
nem origem de água comum**. Isso continua em NÃO TESTÁVEL.

## 3 · CORRIGE um campo da adenda de controlo — C1a e C1b

`CAMADA_0_ADENDA_CONTROLO.md`, campo `nao_controla` de C1a, diz:

> «gestão, rega, fertilizacão, tratamentos: **proprietário desconhecido**»

**Não é desconhecido.** É o ENT 472062.

| facto | ficheiro e cálculo | margem |
|---|---|---|
| **C1a + C1b (11,60 ha) e o kiwi declarado no bloco (12,63 ha) são o mesmo sítio.** Intersecção 10,29 ha: **81,5 % do kiwi cai dentro de C1a+C1b, e 88,7 % de C1a+C1b é kiwi declarado.** Quatro dos seis polígonos a 85–99 %, um a 76 %, e só o mais a sul fora. | `c1ab_contra_kiwi_ifap.py` → `.json`, intersecção por `shapely` | exacto sobre as duas geometrias |

**O que muda, e o que não muda.** O `veredicto` de C1a — *«NÃO serve como
controlo contemporâneo de kiwi; serve apenas como controlo HISTÓRICO 2010-2012,
e mesmo esse com a reserva de a espécie não estar provada»* — **mantém-se
inteiro**, e ganha fundamento melhor do que tinha:

- a espécie **está agora provada** por declaração administrativa: é kiwi;
- e a `estrutura_por_epoca` que o justificava — «entrelinha aberta em 2021 e
  2023, camalhões com plástico contínuo em 2025» — deixa de ser um sinal
  ambíguo de mudança de cultura e passa a ter nome: **é um bloco de kiwi
  re-enxertado cuja copa ainda não fechou.** O que a C0 leu como possível troca
  de cultura é a assinatura da re-enxertia.

**A correcção é de fundamento, não de conclusão.** Quem usou «pode ser outra
cultura» para desqualificar o bloco usou uma razão que agora está falsificada;
a desqualificação continua correcta pela razão certa.

---

## O QUE A CAMADA 2 PODE TRATAR COMO DADO

Lista fechada. Só isto passa desta revisão.

**G38.** O voo LiDAR das duas folhas é de **06-07-2025, 14:34:53–14:51:08 UTC**,
um só dia, amplitude 0,27 h por folha, calculado do tempo GPS dos pontos.
*(±1 s)*

**G39.** O bloco sudoeste tem **19,00 ha de parcelas**, das quais **13,23 ha do
ENT 472062**, e **12,64 ha de kiwi declarado, todo do ENT 472062**. *(exacto
sobre a campanha 2025)*

**G40.** **C1a+C1b e o kiwi declarado do bloco são o mesmo sítio** — 81,5 % e
88,7 % de sobreposição. *(exacto)*

**G41.** A lacuna de área da exploração passa de 15,9 ha para **1,98 ha**.
*(±2 ha, herdado da medição por assinatura)*

---

## NÃO TESTÁVEL — entradas que se mantêm ou nascem aqui

- **Origem da água de C1a, C1b e C3.** Continua sem resolver: a pertença
  administrativa não a determina, e não há reservatório, furo nem conduta
  visível na ortofoto.
- **Se a rede de rega é partilhada entre o corpo principal e o bloco sudoeste.**
  O parcelário não responde a isto.
- **O que resta da lacuna de área** — 1,98 ha sem correspondência.

---

## NOTA DE PROCEDIMENTO, e é sobre mim

Os três factos acima foram produzidos em 31-08 e ficaram **três dias fora da
cadeia**, em notas de entrega para a sessão de apresentação. Dois deles fechavam
entradas que esta camada tinha deixado abertas; um descarregava uma paragem de
linha em vigor.

É o mesmo trajecto pelo qual o «núcleo em declínio» da AOI quarentenada voltou:
**não pela cadeia, mas por fora dela.** A regra 1 não é só autorização para
herdar — é obrigação de devolver. Fica registado.
