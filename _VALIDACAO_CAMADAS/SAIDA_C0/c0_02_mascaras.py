# -*- coding: utf-8 -*-
"""C0-02. As mascaras: contagens, areas, sobreposicoes, circularidade,
e a tendencia da referencia sa ao longo das 11 datas.

Reproduz tambem as mascaras BOOLEANAS de fazer_masks_v2.py a partir da cena
de 2026, para arbitrar a discrepancia 2906/2903, 446/454, 423/427, 219/220.
"""
import json
import os
import numpy as np
import rasterio
from scipy import ndimage, stats
from matplotlib.path import Path as MP

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
H, W = 100, 200
DATAS = ["2017-07-02", "2018-08-31", "2019-09-02", "2020-07-18", "2021-07-16",
         "2022-07-31", "2023-08-07", "2024-07-22", "2025-06-17", "2025-08-14",
         "2026-07-27"]
PLENA = [d for d in DATAS if d not in ("2019-09-02", "2025-06-17")]

masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
yy, xx = np.mgrid[0:H, 0:W]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(H, W) for k, v in masks.items()}


def ler(d):
    with rasterio.open(os.path.join(BASE, "sentinel", d + ".tif")) as ds:
        return ds.read(1)


ND = {d: ler(d) for d in DATAS}
nd26 = ND["2026-07-27"]

# ------------------------------------------------------------------ contagens
print("=" * 78)
print("1. CONTAGENS  (poligono rasterizado, matplotlib.path.contains_points)")
print("=" * 78)
for k in ("pomar", "saudavel", "saudavel_2", "saudavel_3", "manchaW", "zona0"):
    print("  %-11s %5d px = %6.2f ha   vertices=%d"
          % (k, mk[k].sum(), mk[k].sum() / 100.0, len(masks[k])))
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
print("  %-11s %5d px = %6.2f ha" % ("SAUDAVEL u", sau.sum(), sau.sum() / 100.0))

# --------------------------------------------- reproducao das mascaras booleanas
print()
print("=" * 78)
print("2. REPRODUCAO DAS MASCARAS BOOLEANAS de fazer_masks_v2.py (cena 2026)")
print("=" * 78)


def disco(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def rasteriza(poly):
    return MP(poly).contains_points(pts).reshape(H, W)


dist = ndimage.distance_transform_edt(~(nd26 < 0.25))
copado = ndimage.binary_opening((nd26 > 0.78) & (dist > 5), np.ones((2, 2)))
lab, _ = ndimage.label(copado)
Z0 = [[97, 43], [112, 43], [115, 48], [113, 54], [106, 57], [99, 56], [95, 49]]
sel = np.zeros_like(copado)
for cy, cx in ((51, 68), (32, 125), (24, 139), (17, 153)):
    i = lab[cy, cx]
    if i == 0:
        ys, xs = np.where(lab > 0)
        j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
        i = lab[ys[j], xs[j]]
    sel |= (lab == i)
pomar_b = ndimage.binary_closing(sel | rasteriza(Z0), disco(6))
pomar_b = ndimage.binary_fill_holes(pomar_b) & (dist > 4)
l2, n2 = ndimage.label(pomar_b)
pomar_b = ndimage.binary_fill_holes(
    l2 == 1 + np.argmax(ndimage.sum(pomar_b, l2, range(1, n2 + 1))))
z0_b = rasteriza(Z0) & pomar_b
jw = np.zeros_like(pomar_b)
jw[44:68, 36:72] = True
mw_b = pomar_b & (nd26 < 0.76) & jw
l4, n4 = ndimage.label(mw_b)
mw_b = l4 == 1 + np.argmax(ndimage.sum(mw_b, l4, range(1, n4 + 1)))
mw_b = ndimage.binary_dilation(mw_b, disco(3)) & pomar_b
CAND = {"saudavel": [[72, 40], [90, 40], [90, 56], [72, 56]],
        "saudavel_2": [[90, 32], [110, 32], [110, 38], [90, 38]],
        "saudavel_3": [[133, 21], [145, 21], [145, 31], [133, 31]]}
interior = ndimage.binary_erosion(pomar_b, disco(3))
longe = ~ndimage.binary_dilation(mw_b | z0_b, disco(5))
sau_b = {k: rasteriza(p) & interior & longe & copado for k, p in CAND.items()}
sauU_b = sau_b["saudavel"] | sau_b["saudavel_2"] | sau_b["saudavel_3"]

TAB = [("pomar", pomar_b, mk["pomar"], 2906, 2903),
       ("saudavel u", sauU_b, sau, 446, 454),
       ("manchaW", mw_b, mk["manchaW"], 423, 427),
       ("zona0", z0_b, mk["zona0"], 219, 220)]
print("  %-11s %8s %8s | %8s %8s | prosa bate? poligono bate?"
      % ("mascara", "booleana", "poligono", "prosa", "operativo"))
for nome, b, p, prosa, oper in TAB:
    print("  %-11s %8d %8d | %8d %8d |    %-5s      %-5s"
          % (nome, b.sum(), p.sum(), prosa, oper,
             b.sum() == prosa, p.sum() == oper))

# ------------------------------------------------------------- sobreposicoes
print()
print("=" * 78)
print("3. SOBREPOSICOES E CONTENCAO (poligonos)")
print("=" * 78)
for k in ("saudavel", "saudavel_2", "saudavel_3", "manchaW", "zona0"):
    dentro = (mk[k] & mk["pomar"]).sum() / max(mk[k].sum(), 1) * 100
    print("  %-11s dentro de `pomar`: %6.2f%%  (%d px fora)"
          % (k, dentro, (mk[k] & ~mk["pomar"]).sum()))
print("  saudavel n manchaW = %d px ; saudavel n zona0 = %d px ; "
      "manchaW n zona0 = %d px"
      % ((sau & mk["manchaW"]).sum(), (sau & mk["zona0"]).sum(),
         (mk["manchaW"] & mk["zona0"]).sum()))

# ------------------------------------------------------------- circularidade
print()
print("=" * 78)
print("4. CIRCULARIDADE: as mascaras dependem do NDVI que depois se mede?")
print("=" * 78)
for k, m in (("pomar", mk["pomar"]), ("saudavel u", sau),
             ("manchaW", mk["manchaW"]), ("zona0", mk["zona0"])):
    v = nd26[m]
    print("  %-11s NDVI 2026: min=%.3f p05=%.3f mediana=%.3f p95=%.3f max=%.3f"
          % (k, np.nanmin(v), np.nanpercentile(v, 5), np.nanmedian(v),
             np.nanpercentile(v, 95), np.nanmax(v)))
print("  fraccao de `saudavel u` com NDVI 2026 <= 0.78: %.2f%%   (limiar `copado`)"
      % (100 * np.mean(nd26[sau] <= 0.78)))
print("  fraccao de `manchaW` com NDVI 2026 >= 0.76: %.2f%%   (limiar mw)"
      % (100 * np.mean(nd26[mk["manchaW"]] >= 0.76)))
print("  fraccao de `pomar` com NDVI 2026 <= 0.78: %.2f%%"
      % (100 * np.mean(nd26[mk["pomar"]] <= 0.78)))

# -------------------------------------------- tendencia da referencia sa
print()
print("=" * 78)
print("5. TENDENCIA DA REFERENCIA SA (o pivo)  -- 11 datas e 9 de plena estacao")
print("=" * 78)
print("  data        ref_media  ref_mediana  ref_dp   pomar_med  zona0_med  mW_med")
serie = {}
for d in DATAS:
    a = ND[d]
    r = a[sau]
    serie[d] = float(np.nanmean(r))
    print("  %s   %.4f     %.4f    %.4f    %.4f    %.4f   %.4f"
          % (d, np.nanmean(r), np.nanmedian(r), np.nanstd(r),
             np.nanmean(a[mk["pomar"]]), np.nanmean(a[mk["zona0"]]),
             np.nanmean(a[mk["manchaW"]])))


def tend(datas, rotulo):
    t = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12.0 for d in datas])
    y = np.array([serie[d] for d in datas])
    lr = stats.linregress(t, y)
    print("  %-22s  declive = %+.5f NDVI/ano  (= %+.4f/decada)  "
          "p = %.4f  r2 = %.3f  n = %d"
          % (rotulo, lr.slope, lr.slope * 10, lr.pvalue, lr.rvalue ** 2, len(t)))
    return lr


print()
tend(DATAS, "referencia, 11 datas")
tend(PLENA, "referencia, 9 plena est.")
t = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12.0 for d in PLENA])
for k, m in (("pomar", mk["pomar"]), ("zona0", mk["zona0"]),
             ("manchaW", mk["manchaW"])):
    y = np.array([float(np.nanmean(ND[d][m])) for d in PLENA])
    lr = stats.linregress(t, y)
    print("  %-22s  declive = %+.5f NDVI/ano  p = %.4f  r2 = %.3f"
          % (k + ", 9 plena est.", lr.slope, lr.pvalue, lr.rvalue ** 2))

# ------------------------------- degrau 2021->2022 (harmonizacao BOA)
print()
print("  delta referencia 2021-07-16 -> 2022-07-31 = %+.4f"
      % (serie["2022-07-31"] - serie["2021-07-16"]))

json.dump({"contagens_poligono": {k: int(mk[k].sum()) for k in mk},
           "contagens_booleanas": {"pomar": int(pomar_b.sum()),
                                   "saudavel_u": int(sauU_b.sum()),
                                   "manchaW": int(mw_b.sum()),
                                   "zona0": int(z0_b.sum())},
           "serie_referencia": serie},
          open(os.path.join(OUT, "c0_02_mascaras.json"), "w"), indent=1)
print("\n-> c0_02_mascaras.json")
