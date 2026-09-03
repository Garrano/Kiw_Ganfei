# -*- coding: utf-8 -*-
"""Refazer o que a C2 publicou sobre o foco ESTE, com a particao do LiDAR.

O que se refaz e porque
-----------------------
A C2 separou copado de chao com a mascara `nu2021`, tirada da ortofoto de 2021.
Era o melhor que existia entao. O LiDAR de 06-07-2025 mostra que ela falha:
**22,7 % do que a C2 chamou «foco ESTE plantado» nao tem pergola nenhuma**, e
metade do disco ESTE inteiro esta abaixo de meio metro de altura.

Isso poe em causa, por ordem de gravidade:

  V2   o degrau de -0,1439 no «foco ESTE plantado», e o «os dois focos caem
       juntos, pela mesma quantidade»
  V8   as 1,41 ha de declinio novo em tres manchas junto ao foco ESTE
  V9   as 1,62 ha novas desde 2025 dentro de 120 m do foco ESTE
  V10  as fraccoes de chao despido (53/60/78/34 %), medidas com `nu2021`

E ha um item da lista NAO TESTAVEL que deixa de o ser: a C2 escreveu que «a
queda do foco ESTE em 2025-2026 nao tem instrumento independente, e o radar
positivamente nao a ve». Agora ha instrumento, e nao e optico.

Metodo — o mesmo da C2, so muda a mascara
-----------------------------------------
Gap = referencia da propria cena menos a media da unidade. Dois modelos com o
mesmo numero de parametros: recta sobre os dez pontos, contra patamar ate 2024
mais patamar em 2025-26. Razao de somas de quadrados. Identico a
`c2_06_este_plantado.py`, para os numeros serem comparaveis linha a linha.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
NU21 = masc["nu2021"] & POMAR
h = np.load(os.path.join(AQUI, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)     # tinha pergola em 06-07-2025
SEM = np.isfinite(h) & (h < 0.5)
do, de = discos_dos_focos(POMAR)

UN = [
    ("OESTE  (C2, disco todo)", do & POMAR),
    ("OESTE  com pergola", do & POMAR & COM),
    ("ESTE   C2 'plantado' (~nu2021)", de & POMAR & ~NU21),
    ("ESTE   com pergola (LiDAR)", de & POMAR & COM),
    ("ESTE   sem pergola (LiDAR)", de & POMAR & SEM),
    ("resto do pomar, com pergola", POMAR & COM & ~do & ~de & ~REF),
]
print("AS UNIDADES\n")
print("%-34s %7s %10s %12s" % ("", "ha", "altura", "%>1,5 m"))
for n, m in UN:
    k = m & np.isfinite(h)
    print("%-34s %7.2f %8.2f m %10.1f %%"
          % (n, m.sum() / 100.0, np.median(h[k]) if k.any() else np.nan,
             100 * np.mean(h[k] > 1.5) if k.any() else np.nan))
print("\nsobreposicao: do que a C2 chamou 'ESTE plantado', %.1f %% nao tinha "
      "pergola em 06-07-2025" % (100 * (de & POMAR & ~NU21 & SEM).sum()
                                 / max((de & POMAR & ~NU21).sum(), 1)))

nd = carrega_ndvi(TODAS)
SERIE = sorted(nd)
anos = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12.0 for d in SERIE])
tardio = np.array([d >= "2025" for d in SERIE])

print("\n" + "=" * 78)
print("V2 REFEITO — recta contra degrau, na moeda operativa (fosso)\n")
print("%-34s %9s %8s %9s %9s %8s" %
      ("unidade", "b/ano", "p(b)", "SQR lin", "SQR deg", "degrau"))
res = {}
for nome, m in UN:
    if m.sum() < 10:
        continue
    f = np.array([float(np.nanmean(a[REF]) - np.nanmean(a[m]))
                  for a in (nd[d] for d in SERIE)])
    lr = stats.linregress(anos, f)
    sqr_lin = float(np.sum((f - (lr.intercept + lr.slope * anos)) ** 2))
    c1, c2 = float(f[~tardio].mean()), float(f[tardio].mean())
    aj = np.where(tardio, c2, c1)
    sqr_deg = float(np.sum((f - aj) ** 2))
    q = sqr_lin / sqr_deg if sqr_deg else np.inf
    t = stats.ttest_ind(f[tardio], f[~tardio], equal_var=False)
    res[nome] = dict(ha=m.sum() / 100.0, b=lr.slope, p_b=lr.pvalue,
                     sqr_lin=sqr_lin, sqr_deg=sqr_deg, razao=q,
                     degrau=c2 - c1, p_degrau=float(t.pvalue),
                     fosso=[float(v) for v in f])
    print("%-34s %+9.4f %8.3f %9.5f %9.5f %+8.4f   %s (%.2f:1) p=%.3f"
          % (nome, lr.slope, lr.pvalue, sqr_lin, sqr_deg, c2 - c1,
             "DEGRAU" if q > 1.5 else ("linear" if q < 0.67 else "indistintos"),
             q, t.pvalue))

print("\nserie do fosso, cena a cena")
print("%-34s %s" % ("", "  ".join(d[2:7] for d in SERIE)))
for nome in res:
    print("%-34s %s" % (nome, "  ".join("%5.3f" % v for v in res[nome]["fosso"])))

print("\n" + "=" * 78)
print("V10 REFEITO — quanto do nucleo oriental e chao, por LiDAR e nao por nu2021\n")
print("%-12s %10s %12s %12s" % ("cena", "defice ha", "% sem pergola", "% em nu2021"))
v10 = {}
for d in SERIE:
    a = nd[d]
    r = float(np.nanmean(a[REF]))
    dfc = mapa_defice(a, POMAR, r) & de
    if dfc.sum() == 0:
        continue
    pl = 100.0 * (dfc & SEM).sum() / dfc.sum()
    pn = 100.0 * (dfc & NU21).sum() / dfc.sum()
    v10[d] = dict(ha=dfc.sum() / 100.0, pct_sem_pergola=pl, pct_nu2021=pn)
    print("%-12s %10.2f %12.1f %12.1f" % (d, dfc.sum() / 100.0, pl, pn))

print("\n" + "=" * 78)
print("V8 REFEITO — as manchas de declinio novo junto ao foco ESTE\n")
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool) & POMAR
from scipy import ndimage
lab, n = ndimage.label(novo, np.ones((3, 3)))
E, N = centros_celulas()
print("%-6s %7s %10s %14s %12s" % ("mancha", "ha", "dist ESTE", "% sem pergola", "altura"))
v8 = []
for i in range(1, n + 1):
    m = lab == i
    if m.sum() < 10:
        continue
    dE = float(np.hypot(E[m].mean() - FOCO_ESTE[0], N[m].mean() - FOCO_ESTE[1]))
    dO = float(np.hypot(E[m].mean() - FOCO_OESTE[0], N[m].mean() - FOCO_OESTE[1]))
    k = m & np.isfinite(h)
    pl = 100.0 * np.mean(h[k] < 0.5) if k.any() else np.nan
    v8.append(dict(ha=m.sum() / 100.0, d_este=dE, d_oeste=dO,
                   pct_sem_pergola=pl, altura=float(np.median(h[k]))))
    if dE < dO:
        print("%-6d %7.2f %8.0f m %13.1f %% %10.2f m"
              % (i, m.sum() / 100.0, dE, pl, np.median(h[k])))
json.dump(dict(v2=res, v10=v10, v8=v8),
          open(os.path.join(AQUI, "refazer_c2_este.json"), "w"), indent=1)
