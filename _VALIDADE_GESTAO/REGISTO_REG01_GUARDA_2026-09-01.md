# REG-01 — guarda de cultura e ano da quebra

**Data:** 1 de Setembro de 2026
**Objecto:** `reg01_local_ou_regional.py`, `reg01_landsat.py`, `reg01_landsat_r3.py`
**Origem:** verificação pedida à frase «o degrau de 2025-26 não é exclusivo desta
exploração, e há blocos vizinhos muito piores» — pergunta directa: *os blocos de
comparação são também kiwi?*

---

## 1 · A pergunta que originou isto — respondida, e a resposta é sim

Os blocos de comparação vêm de
`_MULTIVERSO/SAIDA_H2_patologista/ifap_kiwi_largo.json`, produzido por
`03_ifap_largo.py` com o filtro literal `PUN_CUL_COD != "124"` → salta.

Verificado polígono a polígono, no ficheiro e não no nome:

| campo | valor |
|---|---|
| polígonos | 53 |
| `PUN_CUL_COD` | **124 em 53 de 53** |
| `PUN_CUL_DESC` | **KIWI em 53 de 53** |
| `CUL_CAMPANHA` | **2025 em 53 de 53** |

Após os filtros de dimensão e cobertura (≥ 0,5 ha, ≥ 20 células inteiras, série
completa nas nove cenas) ficam **38 blocos**: 15 do ENT 472062 e 23 de seis
outros beneficiários. **A comparação é kiwi contra kiwi.** A preocupação de
comparabilidade de cultura fica respondida.

**Porque não bastava.** Duas coisas apareceram ao verificar isto, e ambas
atingem a frase que motivou a pergunta.

---

## 2 · Defeito 1 — a metade «muito piores» atribui o acontecimento errado

Os cinco blocos com degrau mais negativo (ENT 297313, −0,21 a −0,40) **quebram
em 2024**, não em 2025-26. Desvio à mediana regional, cena a cena:

```
6705427  +0,033 +0,017 +0,019 +0,026 +0,011 −0,026 │ −0,392 │ −0,399 −0,494
          2017   2018   2020   2021   2022   2023   │  2024  │  2025   2026
```

Plano e ligeiramente positivo até 2023, um degrau de ~0,4 em 2024-07, e fica em
baixo. A mesma forma nos cinco.

**Como passaram despercebidos.** O degrau é `média(2025-26) − média(2017-2024)`.
Um colapso em 2024 cai dentro da **própria linha de base**, dilui-se por oito
cenas, e ainda assim pontua como degrau grande — suficiente para encabeçar a
tabela ordenada. Quem lesse essa tabela leria os cinco piores como exemplos
piores do acontecimento de 2025-26. **Não são.** São um acontecimento diferente,
um ano antes e muito maior.

Isto é verificável por terceiros no mesmo parcelário: qualquer leitor com o
`ifap_kiwi_largo.json` reproduz a série e vê o degrau em 2024.

## 3 · Defeito 2 — a continuidade da cultura não está verificada

`CUL_CAMPANHA` é **2025 nos 53 polígonos**. Uma só campanha. A declaração prova
que os blocos eram kiwi **em 2025**; não diz nada sobre 2017-2024, que é toda a
linha de base.

Os cinco blocos com penhasco em 2024 têm exactamente a forma de um arranque ou
de uma replantação. Se for isso, não eram kiwi durante a maior parte da linha de
base, e ficam desqualificados como comparadores por uma segunda razão,
independente da primeira.

**Isto não se resolve com mais cálculo.** É facto de tipo 1: pede as campanhas
anteriores do parcelário, ou pergunta-se a quem sabe. Fica registado como **não
verificado**, e nenhuma conclusão pode assentar nele.

---

## 4 · O que foi alterado

### 4.1 · Guarda de cultura — nos três scripts

Os três liam `ifap_kiwi_largo.json` e confiavam no **nome do ficheiro**;
`reg01_local_ou_regional.py:72` lia só `CUL_ID` e nunca `PUN_CUL_COD`. O ficheiro
está limpo hoje, mas se fosse regerado com outro filtro nenhum dos três daria por
isso — é o modo de falha do cabeçalho do `fazer_masks_v2.py`, que quatro
auditorias deixaram passar.

A guarda verifica o código declarado polígono a polígono, aborta com
`SystemExit` se aparecer cultura não-124, e imprime a ressalva da campanha única.

### 4.2 · Ano da quebra — no cálculo, na tabela e no JSON

`reg01_local_ou_regional.py` passa a exportar, por bloco:

- `quebra_ano` — ano da maior queda de cena para cena no desvio
- `quebra_queda` — o valor dessa queda
- `quebra_no_acontecimento` — booleano, `quebra_ano >= 2025`

A tabela marca `[quebra fora de 2025-26]` em cada linha que não pertence ao
acontecimento, e imprime um censo do ano da quebra. **O defeito 1 deixa de ser
possível de cometer por leitura da tabela.**

Censo, nos 38 blocos:

| ano da quebra | blocos |
|---|---|
| 2018 | 5 |
| 2020 | 5 |
| 2021 | 6 |
| 2022 | 3 |
| **2024** | **10** |
| 2025 | 6 ← acontecimento |
| 2026 | 3 ← acontecimento |

**Quebram em 2025-26: 9 blocos, 7 deles de outros beneficiários.**
Quebram antes: 29 — não são exemplos deste acontecimento.

---

## 5 · Verificação — o que foi corrido, e o resultado

**Teste positivo.** `python reg01_local_ou_regional.py`, nove cenas em cache
(mesmos IDs do `proveniencia.json`; não se escolheram cenas novas). Corre até ao
fim, 38 blocos, guarda passa, JSON regenerado com as três chaves novas. Os
degraus e os percentis **não mudaram** — a alteração é aditiva.

**Teste negativo.** `teste_guarda_cultura.py` extrai o bloco literal da guarda de
cada um dos três scripts e corre-o contra (a) o ficheiro real e (b) uma cópia em
memória com um polígono re-etiquetado como vinha (código 231). Não escreve nada
em disco.

```
reg01_local_ou_regional.py     real=passa  poluido_dispara=True
reg01_landsat.py               real=passa  poluido_dispara=True
reg01_landsat_r3.py            real=passa  poluido_dispara=True
```

Os três passam no real e disparam no poluído. **A guarda está exercitada, não só
escrita.**

**Cópia anterior:** `_bak_20260901/` — os três ficheiros, antes da alteração.

**Instrumento independente:** nenhum. Isto é Sentinel-2 a verificar Sentinel-2.
O que é independente são as **fronteiras** — o parcelário do IFAP, documento de
outra entidade, desenhado para pagamentos, anos antes desta análise. Declara-se,
não se dilui.

### 5.1 · Os dois scripts Landsat, recorridos

Corridos depois da guarda, sobre 102 cenas Landsat 8/9 em cache. **As saídas
saem byte a byte iguais às anteriores** (`diff` contra `_bak_20260901/*.antes`):
a guarda é não-mutante, como tem de ser.

`reg01_landsat.py` — 38 blocos herdados do S2 sem re-selecção, 37 sobrevivem ao
mínimo de 6 células de 30 m (cai o 6705423, n=5). Critérios pré-registados:

| critério | resultado | veredicto |
|---|---|---|
| **R1** · os cinco do 297313 entre os oito piores | **5 de 5** (lugares 1, 2, 3, 4, 5 de 37) | REPLICA |
| **R2** · Spearman S2 × Landsat ≥ 0,50 | **rho = +0,890** (p = 1,7 × 10⁻¹³, n = 37) | REPLICA |

`reg01_landsat_r3.py` — 100 cenas (70 em 2017-24, 29 em 2025-26), focos
remascarados a 30 m com cobertura ≥ 5/9:

| unidade | n30 | degrau L | percentil L | percentil S2 |
|---|---|---|---|---|
| foco OCIDENTAL | 26 | −0,0676 | **14 %** | 13 % |
| foco ORIENTAL | 10 | −0,0706 | **14 %** | 13 % |
| pomar inteiro | 335 | +0,0099 | 41 % | 37 % |

**R3 replica:** os dois focos ficam no percentil 14, acima do p10 fixado a
priori. A conclusão do S2 mantém-se no segundo instrumento. O NDMI, que não é
critério pré-registado, dá a mesma ordenação (focos ao percentil 14).

**O que isto fecha, e o que não fecha.** Fecha o controlo 1 do `CONTROLOS.md`:
o resultado regional deixa de assentar num instrumento só — Landsat 8/9 é outra
agência, outro sensor, outra correcção atmosférica, outra órbita, e as cenas nem
sequer são as mesmas. **Não fecha a atribuição:** replicar a medição dos cinco
blocos do 297313 não os move para 2025-26. Continuam a quebrar em 2024 (§2).

**Cabeçalho corrigido.** O docstring de `reg01_landsat.py` afirmava que os cinco
eram «duas a quatro vezes pior do que os focos de Ganfei», sem o ano. Ficava um
cabeçalho a dizer o que o código não sustenta — o modo de falha do
`fazer_masks_v2.py`. Levou nota datada a remeter para §2 e §6.

### 5.2 · Sensibilidade — e se os 29 saírem?

Os blocos que quebram fora de 2025-26 não são comparadores legítimos deste
acontecimento. Retirando-os:

| conjunto | n | p10 | pior bloco da exploração |
|---|---|---|---|
| todos os blocos | 38 | −0,2420 | percentil **21 %** |
| só os que quebram em 2025-26 | 9 | −0,0399 | percentil **22 %** |

**A conclusão de cabeçalho aguenta.** O critério fixado a priori era «acima do
percentil 10», e o pior bloco da exploração fica em 21 % ou 22 % conforme se
conte ou não os 29. H1 cai nos dois casos. A conclusão **nunca dependeu** dos
blocos do 297313.

**Duas ressalvas, e a segunda é a que interessa.**

Primeira: com n = 9 o p10 é degenerado — coincide com o próprio bloco da
exploração. O teste sobrevive, mas a versão restrita tem apoio fino.

Segunda, e é o achado: entre os nove que quebram no acontecimento certo, o bloco
da exploração (−0,0399) é o **segundo mais negativo**, praticamente empatado com
o primeiro (6709642, −0,0401). Quatro dos nove têm degrau ≥ 0.

> **«Há blocos vizinhos muito piores» não é apenas mal atribuído — restrito ao
> acontecimento certo, é o contrário do que os dados dizem.** A exploração está
> no extremo mau do conjunto de comparadores legítimos, não no meio dele.

O que continua verdadeiro é a outra metade: **o acontecimento não é exclusivo
desta exploração** — sete blocos de outros beneficiários quebram em 2025-26.

---

## 6 · O que o relatório pode e não pode afirmar

### PODE

- Que os blocos de comparação são kiwi declarado no parcelário do IFAP, campanha
  2025, com fronteiras que não desenhámos.
- Que o acontecimento **não é exclusivo desta exploração**: nove blocos quebram
  em 2025-26, sete deles de outros beneficiários.
- Que, pelo critério fixado a priori, o pior bloco da exploração fica no
  **percentil 21** da distribuição regional, acima do p10 → **H1 cai, o
  acontecimento lê-se como regional.** É esta a parte forte, e não precisa da
  metade «muito piores».

### NÃO PODE — e esta lista é a que interessa

- **Não pode** chamar «vizinhos muito piores» aos blocos do ENT 297313 sem dizer
  que quebram em 2024. Não pertencem a este acontecimento.
- **Não pode** afirmar que os co-movimentos de 2025-26 são piores do que o da
  exploração: são de ordem de grandeza semelhante (−0,03 a −0,09) e de blocos
  pequenos (0,85 a 3,15 ha).
- **Não pode** tratar os blocos como kiwi ao longo de 2017-2024. A declaração é
  de uma campanha só (§3).
- **Não pode** usar o REG-01 para dizer que a exploração é *típica*. A medida é
  de bloco inteiro e os focos são ~2,5 ha dentro de parcelas de 9,65 e 11,33 ha —
  a mesma diluição de ~4× que o `p04a_parcelas_ifap.py` assinala. O REG-01 mostra
  que a exploração não é extremo ao nível do bloco; não mostra mais.

### Redacção que passa

> O degrau de 2025-26 não é exclusivo desta exploração: seis blocos de kiwi de
> outros beneficiários quebram em 2025 e três em 2026, com quedas da mesma ordem
> de grandeza (−0,03 a −0,09). Pelo critério fixado a priori, o pior bloco da
> exploração fica no percentil 21 da distribuição regional, acima do p10 — o
> acontecimento é regional. Os blocos regionalmente mais afectados (ENT 297313,
> −0,21 a −0,40) **não pertencem a este acontecimento**: quebram em 2024.

---

## 7 · Fica em aberto

1. **Continuidade da cultura em 2017-2024** (§3) — campanhas anteriores do
   parcelário, ou pergunta a quem sabe. Facto de tipo 1. Até lá, **não
   verificado**, e nenhuma conclusão assenta nele.
2. **O que aconteceu ao ENT 297313 em 2024** — dez blocos quebram nesse ano,
   cinco deles com ~0,4. Não é objecto deste dossiê, mas se for arranque ou
   replantação muda quem pode servir de comparador.
3. ~~`reg01_landsat.py` e `reg01_landsat_r3.py` por recorrer.~~ **Fechado
   em 1-09-2026** — corridos, R1/R2/R3 replicam, saídas idênticas às anteriores
   (§5.1).
4. **Ano da quebra no Landsat.** O `reg01_landsat.json` guarda só os degraus por
   período, não a série cena a cena, por isso não tem `quebra_ano`. A atribuição
   está estabelecida pelo S2 (§2) e o Landsat replica a medição, não a data. Se
   alguma vez for preciso datar a quebra no segundo instrumento, exige
   re-derivar das 102 cenas em cache — não é uma alteração aditiva.
