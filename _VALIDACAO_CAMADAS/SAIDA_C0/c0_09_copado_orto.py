# -*- coding: utf-8 -*-
"""C0-09. Onde esta o copado, medido na ortofoto de 25 cm.

 1. deteccao da assinatura «pomar com rede» (cobertura clara + textura de
    linhas) na ortofoto de 2025, numa janela larga que ultrapassa a AOI;
 2. area dessa assinatura dentro da AOI, dentro/fora do poligono `pomar`,
    e fora da AOI — para responder «onde estao as outras ~16 ha»;
 3. fraccao de area muito clara na janela da ADENDA (E530550-531200,
    N4654930-4655300) em 2010, 2021 e 2025, para verificar a mudanca de
    coberto declarada.
"""
import json
import os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
JAN = (529200, 4653900, 531800, 4655700)          # janela larga
RES = 1.0                                          # m/px de trabalho
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))


def le(caminho, jan, res):
    with rasterio.open(caminho) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        n = min(ds.count, 4)
        a = ds.read(list(range(1, n + 1)), window=win, out_shape=(n, h, w),
                    boundless=True, fill_value=0)
    return a.astype("float32")


ORT = {a: os.path.join(BASE, "orto", f) for a, f in (
    ("2010", "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif"),
    ("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"),
    ("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"))}

a25 = le(ORT["2025"], JAN, RES)
Hh, Ww = a25.shape[1:]
print("janela %s a %.1f m/px -> %dx%d" % (str(JAN), RES, Ww, Hh))
lum = a25[:3].mean(0)
valido = lum > 0
print("pixeis com dados: %.1f%%" % (100 * valido.mean()))

# assinatura da rede: claro e pouco saturado
mx = a25[:3].max(0)
mn = a25[:3].min(0)
sat = (mx - mn) / np.maximum(mx, 1)
claro = (lum > np.percentile(lum[valido], 78)) & (sat < 0.22) & valido
# textura de linhas: desvio padrao local alto na direccao transversal
sm = ndimage.uniform_filter(lum, 9)
sq = ndimage.uniform_filter(lum * lum, 9)
tex = np.sqrt(np.maximum(sq - sm * sm, 0))
rede = claro & (tex > np.percentile(tex[valido], 55))
rede = ndimage.binary_closing(rede, np.ones((7, 7)))
rede = ndimage.binary_opening(rede, np.ones((5, 5)))
rede = ndimage.binary_fill_holes(rede)
lab, n = ndimage.label(rede, np.ones((3, 3)))
tam = ndimage.sum(rede, lab, range(1, n + 1))
grandes = np.zeros_like(rede)
for i in np.argsort(tam)[::-1][:12]:
    if tam[i] * RES * RES < 5000:                  # < 0.5 ha
        continue
    grandes |= (lab == i + 1)
print("assinatura de rede: %d px = %.2f ha (blocos >=0.5 ha)"
      % (grandes.sum(), grandes.sum() * RES * RES / 10000.0))


def utm2px(E, N):
    return (E - JAN[0]) / RES, (JAN[3] - N) / RES


yy, xx = np.mgrid[0:Hh, 0:Ww]
E = JAN[0] + xx * RES
N = JAN[3] - yy * RES
dentro_aoi = (E >= AOI[0]) & (E <= AOI[2]) & (N >= AOI[1]) & (N <= AOI[3])
pol = np.array(masks["pomar"])
polE = AOI[0] + pol[:, 0] * 10.0
polN = AOI[3] - pol[:, 1] * 10.0
pomar = MP(np.column_stack([polE, polN])).contains_points(
    np.column_stack([E.ravel(), N.ravel()])).reshape(Hh, Ww)

ha = lambda m: m.sum() * RES * RES / 10000.0       # noqa: E731
print()
print("=" * 70)
print("2. REPARTICAO DA ASSINATURA DE REDE")
print("=" * 70)
print("  poligono `pomar` (referencia)          %6.2f ha" % ha(pomar))
print("  rede dentro do poligono `pomar`        %6.2f ha  (%.0f%% do poligono)"
      % (ha(grandes & pomar), 100 * (grandes & pomar).sum() / pomar.sum()))
print("  rede dentro da AOI mas fora do pomar   %6.2f ha"
      % ha(grandes & dentro_aoi & ~pomar))
print("  rede FORA da AOI (nesta janela)        %6.2f ha"
      % ha(grandes & ~dentro_aoi))
print("  rede total na janela                   %6.2f ha" % ha(grandes))
print("  poligono `pomar` SEM assinatura de rede %6.2f ha"
      % ha(pomar & ~grandes))

# blocos fora da AOI, um a um
lab2, n2 = ndimage.label(grandes & ~dentro_aoi, np.ones((3, 3)))
print()
print("  blocos com assinatura de rede fora da AOI:")
for i in range(1, n2 + 1):
    m = lab2 == i
    if ha(m) < 0.5:
        continue
    ys, xs = np.where(m)
    print("    bloco %d: %6.2f ha  E %d..%d  N %d..%d  centro E%d N%d"
          % (i, ha(m), JAN[0] + xs.min() * RES, JAN[0] + xs.max() * RES,
             JAN[3] - ys.max() * RES, JAN[3] - ys.min() * RES,
             JAN[0] + xs.mean() * RES, JAN[3] - ys.mean() * RES))

# --------------------------------------------------- 3. janela da ADENDA
print()
print("=" * 70)
print("3. FRACCAO DE AREA MUITO CLARA NA JANELA DA ADENDA")
print("   E530550-531200 / N4654930-4655300")
print("=" * 70)
JAD = (530550, 4654930, 531200, 4655300)
for ano in ("2010", "2021", "2025"):
    a = le(ORT[ano], JAD, 0.5)
    L = a[:3].mean(0)
    v = L > 0
    if v.sum() == 0:
        print("  %s: sem dados" % ano)
        continue
    for lim in (170, 190, 210):
        print("  %s  lim=%d  fraccao clara = %5.1f%%   (media=%.1f  p90=%.1f)"
              % (ano, lim, 100 * (L[v] > lim).mean(), L[v].mean(),
                 np.percentile(L[v], 90)))

# ------------------------------------------------------------------- figura
fig, ax = plt.subplots(figsize=(20, 14), dpi=140)
rgb = np.moveaxis(a25[:3], 0, -1)
rgb = np.clip(rgb / max(np.percentile(rgb, 99.5), 1), 0, 1)
ax.imshow(rgb, extent=[JAN[0], JAN[2], JAN[1], JAN[3]])
ax.imshow(np.where(grandes, 1.0, np.nan), extent=[JAN[0], JAN[2], JAN[1],
                                                  JAN[3]],
          cmap="autumn", alpha=0.35)
ax.add_patch(Rectangle((AOI[0], AOI[1]), AOI[2] - AOI[0], AOI[3] - AOI[1],
                       fill=False, edgecolor="yellow", lw=2))
ax.add_patch(MPoly(np.column_stack([polE, polN]), closed=True, fill=False,
                   edgecolor="red", lw=2))
ax.add_patch(Rectangle((JAD[0], JAD[1]), JAD[2] - JAD[0], JAD[3] - JAD[1],
                       fill=False, edgecolor="cyan", lw=1.5, ls="--"))
ax.set_title("Assinatura «pomar com rede» na ortofoto 2025 (laranja) · "
             "AOI amarelo · poligono `pomar` vermelho · janela ADENDA ciano",
             fontsize=11)
fig.savefig(os.path.join(OUT, "c0_09_rede_2025.png"), bbox_inches="tight")
plt.close(fig)
print("\n-> c0_09_rede_2025.png")
