# -*- coding: utf-8 -*-
"""CTRL-17b. De que margem e cada bloco, por contagem de travessias de agua.

O CTRL-17 falhou a etiquetar as margens porque a mascara de agua sai pelos
bordos da janela e a terra fecha por fora — tudo ficou numa componente so.
Aqui resolve-se de outra maneira: conta-se quantas vezes o segmento recto
entre dois pontos entra em agua, e quantos metros de agua atravessa.

Pontos de referencia (convertidos para WGS84 e comparados com toponimos
publicos em ctrl_00_extensoes.py):
  fortaleza de Valenca  E 529600 N 4653200  42,0303 N  8,6424 O   PORTUGAL
  centro de Tui         E 529300 N 4655300  42,0492 N  8,6459 O   ESPANHA

Segunda parte: o rectangulo declarado do caso e o poligono `pomar` de
masks.json contem agua do rio?

Criterio de agua: luminancia baixa e azul dominante. Nao e indice de vegetacao.
"""
import json
import os
import numpy as np
import rasterio
from matplotlib.path import Path as MPath
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
CASO = np.array([[530150, 4654870], [531520, 4654870],
                 [531520, 4655450], [530150, 4655450]], float)
AOI = (529950, 4654600, 531950, 4655600)
VAL = (529600.0, 4653200.0)
TUI = (529300.0, 4655300.0)
POMC = (530835.0, 4655160.0)


def mascara_agua(jan, res, pc):
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0).astype("float32")
    lum = a.mean(0)
    val = lum > 0
    ag = (lum < np.percentile(lum[val], pc)) & (a[2] >= a[0] - 2) & val
    ag = ndimage.binary_opening(ag, np.ones((5, 5)))
    ag = ndimage.binary_closing(ag, np.ones((9, 9)))
    lab, n = ndimage.label(ag, np.ones((3, 3)))
    tam = ndimage.sum(ag, lab, range(1, n + 1))
    return lab == (int(tam.argmax()) + 1), (w, h)


# ---------------------------------------------------- 1. travessias
JAN = (528600.0, 4653000.0, 531790.0, 4655780.0)
RES = 2.0
RIO, _ = mascara_agua(JAN, RES, 12)
print("rio na janela larga: %.1f ha" % (RIO.sum() * RES ** 2 / 1e4))


def em_agua(E, N):
    j = int((E - JAN[0]) / RES)
    i = int((JAN[3] - N) / RES)
    return bool(RIO[i, j]) if (0 <= i < RIO.shape[0]
                               and 0 <= j < RIO.shape[1]) else False


def travessias(p, q):
    d = float(np.hypot(q[0] - p[0], q[1] - p[1]))
    t = np.linspace(0, 1, max(2, int(d)))
    s = [em_agua(p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)
         for u in t]
    n = sum(1 for i in range(1, len(s)) if s[i] and not s[i - 1])
    return n, sum(s) * d / len(t)


gj = json.load(open(os.path.join(OUT, "controlos.geojson"), encoding="utf-8"))
print()
print("%-5s %-30s %-26s %-24s" % ("id", "-> centro do pomar do caso",
                                  "-> fortaleza Valenca (PT)",
                                  "-> centro de Tui (ES)"))
for f in gj["features"]:
    p = np.array(f["geometry"]["coordinates"][0])
    c = (float(p[:, 0].mean()), float(p[:, 1].mean()))
    r = [travessias(c, x) for x in (POMC, VAL, TUI)]
    print("%-5s  %d trav / %5.0f m      %d trav / %5.0f m        "
          "%d trav / %5.0f m"
          % (f["properties"]["id"], r[0][0], r[0][1], r[1][0], r[1][1],
             r[2][0], r[2][1]))
print()
print("controlo do metodo — Valenca(PT) -> Tui(ES): %d travessia(s), %.0f m; "
      "Valenca -> pomar do caso: %d travessia(s), %.0f m"
      % (travessias(VAL, TUI) + travessias(VAL, POMC)))

# ------------------------------------- 2. agua dentro dos poligonos do caso
JAN2 = (529900.0, 4654500.0, 531790.0, 4655780.0)
R2 = 1.0
RIO2, (w, h) = mascara_agua(JAN2, R2, 20)
gx, gy = np.meshgrid(JAN2[0] + (np.arange(w) + .5) * R2,
                     JAN2[3] - (np.arange(h) + .5) * R2)
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
q = np.array(masks["pomar"], float)
POM = np.column_stack([AOI[0] + q[:, 0] * 10.0, AOI[3] - q[:, 1] * 10.0])
print()
for nome, pol in (("rectangulo declarado do caso", CASO),
                  ("poligono `pomar` de masks.json", POM)):
    d = MPath(pol).contains_points(
        np.column_stack([gx.ravel(), gy.ravel()])).reshape(h, w)
    tot = d.sum() * R2 ** 2 / 1e4
    ag = (d & RIO2).sum() * R2 ** 2 / 1e4
    print("%-34s area %6.2f ha ; agua do rio dentro: %5.2f ha (%.1f %%)"
          % (nome, tot, ag, 100 * ag / tot))
