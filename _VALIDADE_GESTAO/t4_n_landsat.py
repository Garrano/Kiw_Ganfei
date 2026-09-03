# -*- coding: utf-8 -*-
"""T4 — quantos píxeis Landsat INDEPENDENTES tem cada unidade?

A acusação, textual
-------------------
`CAMADA_2_ADVERSARIO_R2.md`, R1: o cabeçalho de `landsat_independente.py` diz
que «só se usam píxeis inteiramente dentro da unidade, e reporta-se o n». O
código faz `reproject(..., RS.nearest)` para a grelha de 10 m e depois mediana
sobre a máscara de 10 m — **cada píxel Landsat de 30 m passa a nove células, e
o n nunca é reportado.**

O que este teste faz, e o que não faz
-------------------------------------
FAZ: conta quantos **blocos de 30 m distintos** cada unidade toca, que é o
número de píxeis Landsat independentes que a alimentam, a menos do desfasamento
da grelha.

NÃO FAZ: não usa a grelha real do Landsat. As cenas são lidas por streaming e
não estão em disco; ir buscá-las seria trabalho novo, e o adversário pediu uma
contagem, não uma reprodução. **Usa-se uma grelha de 30 m alinhada à AOI**, o
que dá o número certo de ordem de grandeza e pode errar por ±1 bloco em cada
direcção conforme o desfasamento. Está dito, e é o suficiente para a margem que
falta ao S3.

O B1 não entra
--------------
O lóbulo SW fica fora da AOI principal e as suas células não existem nesta
grelha. **O Landsat nunca foi corrido no B1** — o que é, por si, uma lacuna a
registar: a terceira unidade de kiwi da exploração não tem segunda constelação.
"""
import json
import os

import numpy as np

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
FIN = np.isfinite(h)
COM, SEM = FIN & (h >= 0.5), FIN & (h < 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
dsc = lambda c, r=90.: (((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r * r) & POMAR
C_OC, C_OR = (530485.0, 4655053.0), (530977.0, 4655117.0)
do, de = dsc(C_OC), dsc(C_OR)

# as unidades tal como `landsat_independente.py` as define
UN = [("ESTE com pergola", de & COM),
      ("ESTE sem pergola", de & SEM),
      ("OESTE com pergola", do & COM),
      ("referencia", REF),
      ("resto do pomar", POMAR & COM & ~do & ~de & ~REF)]

# blocos de 30 m alinhados a AOI
BE = ((EE - AOI[0]) // 30).astype(int)
BN = ((AOI[3] - NN) // 30).astype(int)
BLOCO = BE * 10000 + BN

print("=" * 88)
print("T4 · PÍXEIS LANDSAT INDEPENDENTES POR UNIDADE")
print("=" * 88)
print()
print("%-24s %8s %9s %10s %12s %10s"
      % ("unidade", "cél 10 m", "ha", "blocos 30 m", "cél/bloco", "inteiros"))
saida = {"nota": "grelha de 30 m alinhada a AOI; ±1 bloco por desfasamento",
         "unidades": {}}
for nome, m in UN:
    if m.sum() == 0:
        continue
    b = BLOCO[m]
    uniq, cont = np.unique(b, return_counts=True)
    inteiros = int((cont == 9).sum())
    saida["unidades"][nome] = dict(celulas=int(m.sum()), ha=m.sum() / 100.0,
                                   blocos=int(uniq.size),
                                   inteiros=inteiros,
                                   cel_por_bloco=float(m.sum() / uniq.size))
    print("%-24s %8d %9.2f %10d %12.1f %10d"
          % (nome, m.sum(), m.sum() / 100.0, uniq.size,
             m.sum() / uniq.size, inteiros))

print()
print("=" * 88)
print("O QUE ISTO FAZ AO S3")
print("=" * 88)
print()
for nome in ("OESTE com pergola", "ESTE com pergola", "resto do pomar"):
    u = saida["unidades"][nome]
    print("  %-22s %3d píxeis Landsat  (%d inteiramente dentro)"
          % (nome, u["blocos"], u["inteiros"]))
print()
print("A mediana anual de cada unidade assenta nestes números, não nas células")
print("de 10 m. O S3 tem de os levar impressos.")
print()
print("E fica registado: **o B1 não tem série Landsat.** A terceira unidade de")
print("kiwi da exploração — 12,64 ha declarados, ENT 472062 — nunca foi medida")
print("por segunda constelação. Vai para NÃO TESTÁVEL.")

json.dump(saida, open(os.path.join(VG, "t4_n_landsat.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito t4_n_landsat.json")
