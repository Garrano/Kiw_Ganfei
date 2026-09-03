# -*- coding: utf-8 -*-
"""CTRL-17. De que lado do rio esta cada bloco?

Mascara de agua da ortofoto de 2025 (luminancia baixa + azul dominante — um
criterio de AGUA, nao de vegetacao), etiquetagem das componentes de TERRA, e
teste de que componente contem cada poligono e cada ponto de referencia
conhecido. Serve para nao repetir o erro do «B1», que mediu vegetacao do outro
lado do rio Minho sem que ninguem tivesse verificado a margem.

Pontos de referencia usados (identificados por conversao para WGS84 e
comparacao com toponimos publicos):
  fortaleza de Valenca   E 529600 N 4653200  -> 42,0303 N  8,6424 O  PORTUGAL
  centro de Tui          E 529300 N 4655300  -> 42,0492 N  8,6459 O  ESPANHA
"""
import json
import os
import numpy as np
import rasterio
from matplotlib.path import Path as MPath
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
JAN = (528600.0, 4653000.0, 531790.0, 4655780.0)
RES = 2.0
REF = {"fortaleza de Valenca (PT)": (529600.0, 4653200.0),
       "centro de Tui (ES)": (529300.0, 4655300.0),
       "pomar do caso (centro)": (530835.0, 4655160.0),
       "aldeia a SE do bloco SW": (529950.0, 4653800.0)}

with rasterio.open(ORTO) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    w = int(round((JAN[2] - JAN[0]) / RES))
    h = int(round((JAN[3] - JAN[1]) / RES))
    a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w), boundless=True,
                fill_value=0).astype("float32")
lum = a.mean(0)
val = lum > 0
agua = (lum < np.percentile(lum[val], 12)) & (a[2] >= a[0] - 2) & val
agua = ndimage.binary_opening(agua, np.ones((5, 5)))
agua = ndimage.binary_closing(agua, np.ones((9, 9)))
lab, n = ndimage.label(agua, np.ones((3, 3)))
tam = ndimage.sum(agua, lab, range(1, n + 1))
rio = lab == (int(tam.argmax()) + 1)
rio = ndimage.binary_dilation(rio, np.ones((3, 3)))
print("rio: %.1f ha" % (rio.sum() * RES ** 2 / 1e4))

terra = (~rio) & val
tl, nt = ndimage.label(terra, np.ones((3, 3)))


def comp(E, N):
    j = int((E - JAN[0]) / RES)
    i = int((JAN[3] - N) / RES)
    if not (0 <= i < tl.shape[0] and 0 <= j < tl.shape[1]):
        return -1
    return int(tl[i, j])


print()
print("componente de terra de cada ponto de referencia:")
for k, (E, N) in REF.items():
    print("  %-28s componente %d" % (k, comp(E, N)))

gj = json.load(open(os.path.join(OUT, "controlos.geojson")))
print()
print("componente de terra de cada poligono (centroide e 4 vertices):")
for f in gj["features"]:
    p = np.array(f["geometry"]["coordinates"][0])
    cs = [comp(p[:, 0].mean(), p[:, 1].mean())]
    for i in range(0, len(p) - 1, max(1, (len(p) - 1) // 4)):
        cs.append(comp(*p[i]))
    print("  %-5s %s" % (f["properties"]["id"], cs))

fig, ax = plt.subplots(figsize=(13, 13 * (JAN[3] - JAN[1]) / (JAN[2] - JAN[0])),
                       dpi=170)
ax.imshow(np.where(rio, 1.0, np.nan), extent=[JAN[0], JAN[2], JAN[1], JAN[3]],
          cmap="cool", vmin=0, vmax=1)
ax.imshow(np.where(rio, np.nan, tl % 9 + 1),
          extent=[JAN[0], JAN[2], JAN[1], JAN[3]], cmap="tab10", alpha=0.55)
for k, (E, N) in REF.items():
    ax.plot(E, N, "k*", ms=9)
    ax.text(E + 20, N, k, fontsize=6)
for f in gj["features"]:
    p = np.array(f["geometry"]["coordinates"][0])
    ax.plot(p[:, 0], p[:, 1], "k-", lw=1.2)
    ax.text(p[:, 0].mean(), p[:, 1].mean(), f["properties"]["id"], fontsize=7)
ax.set_title("Superficie de agua (ciano) e componentes de terra — de que "
             "margem e cada bloco", fontsize=9)
ax.tick_params(labelsize=6)
fig.savefig(os.path.join(OUT, "ctrl_17_margem.png"), bbox_inches="tight")
plt.close(fig)
print("-> ctrl_17_margem.png")
