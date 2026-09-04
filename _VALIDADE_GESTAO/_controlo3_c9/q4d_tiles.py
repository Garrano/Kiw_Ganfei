# -*- coding: utf-8 -*-
"""Q4d - o B1 nao tem cota por FALTA DE LIDAR, ou por causa de FOLGA = 300 m?

O bordo desenhado na P10 nao e o limite do LiDAR: e a caixa da AOI mais 300 m,
escolhida na linha `FOLGA = 300.0` do c1_03_mdt.py. A pergunta e se os mosaicos
que cobrem o B1 ja estao em disco.
"""
import glob
import json
import os

import numpy as np
import rasterio
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely.ops import transform as sht, unary_union

LID = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"

trw = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
tr29 = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
CUL = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
B1 = unary_union([sht(lambda x, y, z=None: trw.transform(x, y),
                      shape(f["geometry"])).buffer(0)
                  for f in KF if int(f["properties"]["CUL_ID"]) in CUL])
b = B1.bounds
X, Y = tr29.transform([b[0], b[2], b[0], b[2]], [b[1], b[1], b[3], b[3]])
B1BOX_3763 = box(min(X), min(Y), max(X), max(Y))
print("B1 em EPSG:3763: X %.1f..%.1f  Y %.1f..%.1f" % (min(X), max(X), min(Y), max(Y)))

paths = sorted(glob.glob(os.path.join(LID, "MDT-50cm-*.tif")))
print("\nmosaicos MDT em disco: %d" % len(paths))
cobrem = []
for p in paths:
    with rasterio.open(p) as s:
        bb = s.bounds
    if box(bb.left, bb.bottom, bb.right, bb.top).intersects(B1BOX_3763):
        inter = box(bb.left, bb.bottom, bb.right, bb.top).intersection(B1)
        cobrem.append((os.path.basename(p), inter.area / 1e4))
print("mosaicos que INTERSECTAM o B1: %d" % len(cobrem))
tot = 0.0
for n, a in cobrem:
    print("   %-34s  %.2f ha do B1" % (n, a))
    tot += a
print("   TOTAL coberto por mosaicos ja em disco: %.2f ha de %.2f (%.1f %%)"
      % (tot, B1.area / 1e4, 100 * tot / (B1.area / 1e4)))

print("\n=> o que falta ao B1 nao e LiDAR. E o recorte:")
print("   c1_03_mdt.py, linha `FOLGA = 300.0`, aplicada a caixa da AOI.")
print("   A AOI e uma decisao (a peca di-lo). O recorte do MDT herda-a, e a")
print("   peca desenha o resultado do recorte como se fosse o fim do LiDAR.")
