# -*- coding: utf-8 -*-
"""C2-06 — a parte plantada do foco ESTE: o declive linear e o modelo errado.

A R2 G30 e a C1 S12 fixam: removido o chao lavrado de 2021, a parte plantada do
foco ESTE cai -0,0150/ano com p = 0,032. O prompt pede que se refaca e se diga
se a significancia aguenta com a definicao de defice fixada.

Reproduz-se — mas a leitura muda. Um declive linear sobre nove pontos supoe uma
descida constante. A serie nao tem forma de descida constante:

  0,848  0,887  0,862  0,858  0,857  0,851  0,860  |  0,754  0,687
  \____________ sete anos entre 0,848 e 0,887 ____/     \__ dois anos __/

Testa-se explicitamente qual dos dois modelos a serie prefere:
  M_linear    recta unica sobre os 10 pontos
  M_degrau    patamar constante ate 2024 + patamar depois (dois parametros)

E aplica-se a mesma pergunta ao foco OESTE, ao pomar e a referencia, para o
resultado nao ser uma propriedade da unidade escolhida.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(POMAR)
SERIE = sorted(DATAS + ["2019-09-02"])
nd = carrega_ndvi(TODAS)
REFV = {d: float(np.nanmean(nd[d][REF])) for d in TODAS}
an = anos_decimais(SERIE)
res = {}

UNID = [
    ("FOCO ESTE plantado (zona0 sem nu2021)", ZONA0 & ~NU21),
    ("FOCO ESTE chao lavrado (zona0 & nu2021)", ZONA0 & NU21),
    ("FOCO ESTE disco r=90 plantado", de & ~NU21),
    ("FOCO OESTE disco r=90", do),
    ("pomar sem os dois discos", POMAR & ~do & ~de),
    ("referencia sistematica", REF),
]

print("=" * 78)
print("NIVEIS, COM A CENA DE 2019 REPOSTA")
print("=" * 78)
print("%-40s %s" % ("", "  ".join(d[2:7] for d in SERIE)))
V = {}
for nome, m in UNID:
    v = np.array([float(np.nanmean(nd[d][m])) for d in SERIE])
    V[nome] = v
    print("%-40s %s  n=%d" % (nome, "  ".join("%.3f" % x for x in v), m.sum()))

print()
print("=" * 78)
print("MODELO LINEAR contra MODELO DE DEGRAU EM 2025")
print("=" * 78)
print("  M_linear: NDVI = a + b*ano                 (2 parametros)")
print("  M_degrau: NDVI = c1 se ano<=2024, c2 depois (2 parametros)")
print("  Mesmo numero de parametros: comparam-se directamente por soma de")
print("  quadrados dos residuos e por R2.")
print()
print("%-40s %10s %8s %10s %10s %8s" %
      ("unidade", "b/ano", "p(b)", "SQR lin", "SQR deg", "degrau"))
tardio = np.array([d >= "2025" for d in SERIE])
for nome, m in UNID:
    v = V[nome]
    r = stats.linregress(an, v)
    sqr_lin = float(((v - (r.intercept + r.slope * an)) ** 2).sum())
    c1, c2 = v[~tardio].mean(), v[tardio].mean()
    aj = np.where(tardio, c2, c1)
    sqr_deg = float(((v - aj) ** 2).sum())
    t, p = stats.ttest_ind(v[~tardio], v[tardio], equal_var=False)
    print("%-40s %+10.5f %8.4f %10.5f %10.5f %+8.4f"
          % (nome, r.slope, r.pvalue, sqr_lin, sqr_deg, c2 - c1))
    res.setdefault("modelos", {})[nome] = dict(
        declive=float(r.slope), p_declive=float(r.pvalue),
        sqr_linear=sqr_lin, sqr_degrau=sqr_deg,
        patamar_ate2024=float(c1), patamar_2025_26=float(c2),
        degrau=float(c2 - c1), p_degrau=float(p))

print()
print("  Razao de verosimilhanca aproximada (SQR_lin / SQR_degrau):")
for nome, _ in UNID:
    r = res["modelos"][nome]
    q = r["sqr_linear"] / r["sqr_degrau"] if r["sqr_degrau"] else float("inf")
    veredicto = "DEGRAU" if q > 1.5 else ("linear" if q < 0.67 else "indistintos")
    print("    %-40s %6.2f   -> %s" % (nome, q, veredicto))

print()
print("=" * 78)
print("O PATAMAR ATE 2024 E MESMO PLANO?")
print("=" * 78)
print("  Declive das 8 cenas de 2017 a 2024 apenas.")
cedo = np.array([d < "2025" for d in SERIE])
for nome, _ in UNID:
    v = V[nome][cedo]
    r = stats.linregress(an[cedo], v)
    print("  %-40s %+0.5f/ano  p=%.4f  (n=%d)" % (nome, r.slope, r.pvalue, cedo.sum()))
    res.setdefault("ate2024", {})[nome] = dict(declive=float(r.slope), p=float(r.pvalue))

print()
print("=" * 78)
print("O FOSSO ATE A REFERENCIA (grandeza operativa) COM O NIVEL AO LADO")
print("=" * 78)
print("%-40s %s" % ("", "  ".join(d[2:7] for d in SERIE)))
for nome, _ in UNID[:-1]:
    f = V["referencia sistematica"] - V[nome]
    r = stats.linregress(an, f)
    rc = stats.linregress(an[cedo], f[cedo])
    print("%-40s %s" % (nome + " (fosso)", "  ".join("%.3f" % x for x in f)))
    print("%-40s declive total %+0.5f/ano p=%.4f | ate 2024 %+0.5f/ano p=%.4f"
          % ("", r.slope, r.pvalue, rc.slope, rc.pvalue))
    res.setdefault("fosso", {})[nome] = dict(
        serie=[float(x) for x in f], declive=float(r.slope), p=float(r.pvalue),
        declive_ate2024=float(rc.slope), p_ate2024=float(rc.pvalue))

print()
print("=" * 78)
print("O QUE E QUE O NUCLEO ESTE DE 2020-2024 TINHA DENTRO?")
print("=" * 78)
from scipy import ndimage  # noqa: E402
E, N = centros_celulas()
for d in ["2020-07-18", "2022-07-31", "2024-07-22", "2026-07-27"]:
    b = mapa_defice(nd[d], POMAR, REFV[d])
    lab, n = ndimage.label(b, np.ones((3, 3)))
    melhor, mm = 0, None
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 15:
            continue
        if np.hypot(E[m].mean() - FOCO_ESTE[0], N[m].mean() - FOCO_ESTE[1]) <= 150 \
                and m.sum() > melhor:
            melhor, mm = m.sum(), m
    if mm is None:
        print("  %s: sem nucleo junto ao foco ESTE" % d)
        continue
    print("  %s: nucleo de %.2f ha | %.0f%% dele e chao lavrado de 2021"
          % (d, melhor / 100.0, 100.0 * (mm & NU21).sum() / melhor))
    res.setdefault("nucleo_este", {})[d] = dict(
        ha=melhor / 100.0, pct_lavrado=float(100.0 * (mm & NU21).sum() / melhor))

json.dump(res, open(os.path.join(SAIDA, "c2_06_este.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_06_este.json")
