# -*- coding: utf-8 -*-
"""Q4f - a minha propria cota do B1, sujeita as regras que aplico aos outros.

(a) controlo de costura: os dois mosaicos que cobrem o B1 concordam na fronteira?
(b) instrumento independente: o GLO-30 poe o B1 abaixo do foco OCIDENTAL?
"""
import glob
import json
import os

import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask
from pyproj import Transformer
from shapely.geometry import shape, mapping, box
from shapely.ops import transform as sht, unary_union

LID = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------- (a) costura entre 157564 e 158564 ----------------
A = os.path.join(LID, "MDT-50cm-157564-07-2025_v02.tif")
B = os.path.join(LID, "MDT-50cm-158564-07-2025_v02.tif")
with rasterio.open(A) as s1, rasterio.open(B) as s2:
    b1b, b2b = s1.bounds, s2.bounds
    print("157564 bounds %s" % (tuple(round(v, 1) for v in b1b),))
    print("158564 bounds %s" % (tuple(round(v, 1) for v in b2b),))
    adj = abs(b1b.right - b2b.left) < 1
    print("adjacentes na vertical? %s (dif %.2f m)" % (adj, abs(b1b.right - b2b.left)))
    if adj:
        a = s1.read(1, window=((0, s1.height), (s1.width - 20, s1.width))).astype("float64")
        b = s2.read(1, window=((0, s2.height), (0, 20))).astype("float64")
        ac = s1.read(1, window=((0, s1.height), (s1.width - 40, s1.width - 20))).astype("float64")
        bc = s2.read(1, window=((0, s2.height), (20, 40))).astype("float64")
for arr in (a, b, ac, bc):
    arr[arr == -999.0] = np.nan
n = min(a.shape[0], b.shape[0])
a, b, ac, bc = a[:n], b[:n], ac[:n], bc[:n]
ok = ~np.isnan(a).any(1) & ~np.isnan(b).any(1) & ~np.isnan(ac).any(1) & ~np.isnan(bc).any(1)
ma, mb = np.nanmean(a[ok], 1), np.nanmean(b[ok], 1)
mac, mbc = np.nanmean(ac[ok], 1), np.nanmean(bc[ok], 1)
salto = mb - ma
print("\ncostura 157564|158564 (a que atravessa o B1), %d linhas utilizaveis:" % ok.sum())
print("  degrau mediano %+.4f m | dp %.4f" % (np.median(salto), salto.std()))
print("  controlo interior 157564 %+.4f m | 158564 %+.4f m"
      % (np.median(ma - mac), np.median(mbc - mb)))
print("  => o degrau da costura e %.3f m, contra os %.3f m que separam o B1 do"
      % (abs(np.median(salto)), 0.576))
print("     foco OCIDENTAL. Razao %.1f x." % (0.576 / max(abs(np.median(salto)), 1e-9)))

# ---------------- (b) GLO-30 sobre o B1 e sobre os focos ----------------
tw = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
CUL = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
B1WGS = unary_union([shape(f["geometry"]).buffer(0) for f in KF
                     if int(f["properties"]["CUL_ID"]) in CUL])

with rasterio.open(os.path.join(LID, "_glo30.tif")) as s:
    glo = s.read(1).astype("float64")
    Tg = s.transform
    glo[glo <= -1000] = np.nan
    try:
        out, _ = rio_mask(s, [mapping(B1WGS)], crop=True, filled=True, nodata=-9999.0)
        vb = out[0].astype("float64")
        vb[vb <= -998] = np.nan
        vb = vb[np.isfinite(vb)]
    except ValueError:
        vb = np.array([])

T29 = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
FOCO_OESTE = (530485.0, 4655053.0)
FOCO_ESTE = (530977.0, 4655117.0)


def glo_disco(utm, raio=90.0):
    lo, la = T29.transform(*utm)
    c = int((lo - Tg.c) / Tg.a)
    r = int((la - Tg.f) / Tg.e)
    k = max(1, int(round(raio / 23.0)))
    v = glo[max(0, r - k):r + k + 1, max(0, c - k):c + k + 1].ravel()
    return v[np.isfinite(v)]


vo, ve = glo_disco(FOCO_OESTE), glo_disco(FOCO_ESTE)
print("\nGLO-30 (instrumento independente, radar):")
print("  foco OCIDENTAL n=%3d  mediana %.3f m" % (len(vo), np.median(vo)))
print("  foco ORIENTAL  n=%3d  mediana %.3f m" % (len(ve), np.median(ve)))
print("  sector B1      n=%3d  mediana %.3f m" % (len(vb), np.median(vb)))
print("\n  B1 menos OCIDENTAL:  LiDAR %+.3f m   GLO-30 %+.3f m   -> sinal %s"
      % (6.062 - 6.638, np.median(vb) - np.median(vo),
         "IGUAL" if np.sign(6.062 - 6.638) == np.sign(np.median(vb) - np.median(vo))
         else "*** INVERTIDO ***"))
print("  B1 menos ORIENTAL :  LiDAR %+.3f m   GLO-30 %+.3f m   -> sinal %s"
      % (6.062 - 7.842, np.median(vb) - np.median(ve),
         "IGUAL" if np.sign(6.062 - 7.842) == np.sign(np.median(vb) - np.median(ve))
         else "*** INVERTIDO ***"))
