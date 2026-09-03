# -*- coding: utf-8 -*-
"""C2-02 — ATAQUE AO ACHADO CENTRAL: e fenologia, ou e o pomar?

O achado central e a curva em U do defice: 8,08 ha (2017) -> 2,91 (2024) ->
7,86 (2026). Seis anos a melhorar e dois a duplicar.

O ramo descendente (2017-2024) tem uma explicacao alternativa obvia que
ninguem testou: **a cena de 2017 e a mais precoce da serie**. Dia-do-ano:

  2017-07-02 = 183   <- a mais precoce de todas
  2021-07-16 = 197
  2020-07-18 = 200
  2024-07-22 = 204   <- o minimo do defice
  2026-07-27 = 208
  2022-07-31 = 212
  2023-08-07 = 219
  2025-08-14 = 226
  2018-08-31 = 243

O kiwi e caduco e de abrolhamento tardio; em inicio de Julho o copado pode
ainda nao estar fechado. Se o defice depender do dia-do-ano, os 8,08 ha de 2017
podem ser copado por fechar, e nao pomar em declinio — e o «ramo de melhoria»
de seis anos desaparece.

Como se testa sem circularidade: com as **duas cenas que a serie exclui**.

  SONDA A — 2025-06-17 (DOY 168) contra 2025-08-14 (DOY 226).
    Mesmo ano, mesmo pomar, mesmas plantas, 58 dias de diferenca. Mede o efeito
    do dia-do-ano com tudo o resto constante. E a calibracao que falta.

  SONDA B — 2018-08-31 (DOY 243) contra 2019-09-02 (DOY 245).
    Dois dias de diferenca no calendario, um ano de diferenca. Mede o ruido
    inter-anual a fenologia igualada — o piso contra o qual qualquer variacao
    da serie tem de ser comparada.

Nada aqui usa mascara definida por NDVI.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(POMAR)
nd = carrega_ndvi(TODAS)
res = {}


def linha(d):
    a = nd[d]
    ref = float(np.nanmean(a[REF]))
    dfc = mapa_defice(a, POMAR, ref)
    return dict(data=d, doy=doy(d), ref=ref,
                pomar=float(np.nanmean(a[POMAR])),
                oeste=float(np.nanmean(a[do])),
                este=float(np.nanmean(a[de])),
                defice_ha=dfc.sum() / 100.0,
                frac_pct=100.0 * dfc.sum() / POMAR.sum(),
                p10_pomar=float(np.nanpercentile(a[POMAR], 10)),
                sd_pomar=float(np.nanstd(a[POMAR])))


print("=" * 78)
print("SONDA A — o efeito do dia-do-ano, medido DENTRO de 2025")
print("=" * 78)
A = [linha("2025-06-17"), linha("2025-08-14")]
print("%-12s %4s %7s %7s %7s %7s %10s %8s" %
      ("data", "DOY", "ref", "pomar", "OESTE", "ESTE", "defice ha", "frac %"))
for r in A:
    print("%-12s %4d %7.3f %7.3f %7.3f %7.3f %10.2f %8.1f"
          % (r["data"], r["doy"], r["ref"], r["pomar"], r["oeste"], r["este"],
             r["defice_ha"], r["frac_pct"]))
dA = A[1]["defice_ha"] - A[0]["defice_ha"]
ddoy = A[1]["doy"] - A[0]["doy"]
print("\n  58 dias de fenologia valem %+0.2f ha de defice (%+.4f ha/dia)"
      % (dA, dA / ddoy))
print("  e %+0.4f de NDVI na referencia, %+0.4f no pomar inteiro."
      % (A[1]["ref"] - A[0]["ref"], A[1]["pomar"] - A[0]["pomar"]))
res["sonda_A_2025"] = A

print()
print("=" * 78)
print("SONDA B — o ruido inter-anual a fenologia igualada")
print("=" * 78)
B = [linha("2018-08-31"), linha("2019-09-02")]
print("%-12s %4s %7s %7s %7s %7s %10s %8s" %
      ("data", "DOY", "ref", "pomar", "OESTE", "ESTE", "defice ha", "frac %"))
for r in B:
    print("%-12s %4d %7.3f %7.3f %7.3f %7.3f %10.2f %8.1f"
          % (r["data"], r["doy"], r["ref"], r["pomar"], r["oeste"], r["este"],
             r["defice_ha"], r["frac_pct"]))
print("\n  2 dias de calendario, 1 ano de intervalo: %+0.2f ha de defice."
      % (B[1]["defice_ha"] - B[0]["defice_ha"]))
print("  E o piso de ruido de uma serie anual de uma cena por ano.")
res["sonda_B_2018_2019"] = B

print()
print("=" * 78)
print("O EFEITO DO DIA-DO-ANO NA SERIE DE PLENA ESTACAO")
print("=" * 78)
L = [linha(d) for d in DATAS]
res["serie"] = L
dd = np.array([r["doy"] for r in L], float)
df = np.array([r["defice_ha"] for r in L])
an = anos_decimais(DATAS)
print("%-12s %4s %10s" % ("data", "DOY", "defice ha"))
for r in L:
    print("%-12s %4d %10.2f" % (r["data"], r["doy"], r["defice_ha"]))

r1 = stats.linregress(dd, df)
print("\n  defice ~ DOY (n=9): declive %+0.4f ha/dia, r=%.3f, p=%.4f"
      % (r1.slope, r1.rvalue, r1.pvalue))
print("  (a sonda A, dentro de um ano so, deu %+0.4f ha/dia)" % (dA / ddoy))
rho, prho = stats.spearmanr(dd, df)
print("  Spearman DOY x defice: rho=%.3f, p=%.4f" % (rho, prho))

print("\n  --- correccao do defice para DOY 208 (o do ano terminal, 2026) ---")
print("  Duas calibracoes independentes; nenhuma e escolhida a posteriori.")
for nome, k in [("sonda A (dentro de 2025)", dA / ddoy),
                ("regressao da serie (n=9)", r1.slope)]:
    corr = df - k * (dd - 208.0)
    print("\n  %s: %+0.4f ha/dia" % (nome, k))
    print("  %-12s %s" % ("", "  ".join("%5s" % d[2:7] for d in DATAS)))
    print("  %-12s %s" % ("bruto", "  ".join("%5.2f" % x for x in df)))
    print("  %-12s %s" % ("corrigido", "  ".join("%5.2f" % x for x in corr)))
    print("  2017 corrigido = %.2f ha  (bruto 8,08).  2024 = %.2f.  2026 = %.2f."
          % (corr[0], corr[6], corr[8]))
    print("  amplitude do ramo 2017->2024: bruto %.2f ha, corrigido %.2f ha"
          % (df[0] - df[6], corr[0] - corr[6]))
    print("  amplitude do salto 2024->2026: bruto %.2f ha, corrigido %.2f ha"
          % (df[8] - df[6], corr[8] - corr[6]))
    res.setdefault("correccoes", {})[nome] = dict(
        ha_por_dia=float(k), corrigido=[float(x) for x in corr])

print()
print("=" * 78)
print("O SALTO 2024->2026 E IMUNE A FENOLOGIA?")
print("=" * 78)
print("  2024-07-22 = DOY 204 e 2026-07-27 = DOY 208: 4 dias de diferenca.")
print("  Pela sonda A isso vale %+0.3f ha; o salto medido e %+0.2f ha."
      % (4 * dA / ddoy, df[8] - df[6]))
print("  Racio: a fenologia explica %.2f%% do salto."
      % (100.0 * abs(4 * dA / ddoy) / abs(df[8] - df[6])))
print("\n  O ramo de melhoria 2017->2024 tem 21 dias de DOY (183->204);")
print("  pela sonda A isso vale %+0.2f ha, contra %.2f ha medidos."
      % (21 * dA / ddoy, df[0] - df[6]))
print("  Racio: a fenologia explica %.0f%% do ramo de melhoria."
      % (100.0 * abs(21 * dA / ddoy) / abs(df[0] - df[6])))

print()
print("=" * 78)
print("CONTROLO: a cena de 2017 e a unica de baseline anterior ao offset BOA")
print("=" * 78)
print("  Se houvesse desvio radiometrico, veria-se no CONTRASTE dentro da cena.")
for r in L:
    print("  %-12s ref %.3f  pomar %.3f  p10 do pomar %.3f  sd %.4f  ref-p10 %.3f"
          % (r["data"], r["ref"], r["pomar"], r["p10_pomar"], r["sd_pomar"],
             r["ref"] - r["p10_pomar"]))

json.dump(res, open(os.path.join(SAIDA, "c2_02_fenologia.json"), "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito c2_02_fenologia.json")
