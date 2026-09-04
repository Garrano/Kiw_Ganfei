# -*- coding: utf-8 -*-
"""Q5 - os numeros que a P10 desenha, contra o que existe em disco."""
import io
import json
import os
import re

import numpy as np
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely.ops import transform as sht, unary_union

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"

print("=== o '60 %' do docstring: que fraccao da exploracao o MDT cobre? ===")
DEMJ = json.load(open(os.path.join(VC, "SAIDA_C1", "c1_03_dem50.json"),
                      encoding="utf-8"))
t = DEMJ["transform"]
ny, nx = DEMJ["shape"]
x0, y0, px = t[2], t[5], t[0]
tr = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)
cx = [x0, x0 + nx * px, x0, x0 + nx * px]
cy = [y0, y0, y0 - ny * px, y0 - ny * px]
DX, DY = tr.transform(cx, cy)
DEMBOX = box(min(DX), min(DY), max(DX), max(DY))

trw = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
CUL_B1 = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
b1 = []
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL_B1:
        b1.append(sht(lambda x, y, z=None: trw.transform(x, y),
                      shape(f["geometry"])).buffer(0))
B1 = unary_union(b1)

TOTAL_HA = 44.93          # exploracao declarada, C8
POMAR_HA = 30.31          # o poligono principal, P02
print("  exploracao declarada          : %.2f ha" % TOTAL_HA)
print("  poligono principal (pomar)    : %.2f ha" % POMAR_HA)
print("  sector B1                     : %.2f ha" % (B1.area / 1e4))
print("  B1 dentro da caixa do MDT     : %.2f ha" % (B1.intersection(DEMBOX).area / 1e4))
cob = POMAR_HA + B1.intersection(DEMBOX).area / 1e4
print("  cobertura do MDT (pomar + B1) : %.2f ha = %.1f %% de %.2f"
      % (cob, 100 * cob / TOTAL_HA, TOTAL_HA))
print("  a P10 diz 60 %% -> corresponde a %.2f ha" % (0.60 * TOTAL_HA))
print("  e o '60,8 %%' do painel e OUTRA coisa: a cobertura da particao por")
print("  valvula (27,3 ha de 44,93), facto C8. Duas grandezas, um numero.")

print()
print("=== o '28 %% de area sem pergola' no foco oriental ===")
for f in ("LISTA_FINAL_2026-08-31.md",):
    txt = io.open(os.path.join(VC, f), encoding="utf-8", errors="replace").read()
    for m in re.finditer("28 %", txt):
        print("  %s: ...%s..." % (f, txt[max(0, m.start() - 150):m.start() + 60]
                                  .replace(chr(10), " ")))

print()
print("=== a verificacao 7 do certificar.py e a P10 ===")
FIG = r"C:/Users/Jackster2/Downloads/ganfei_s2/figuras"
LISTA = os.path.join(VC, "LISTA_FINAL_2026-08-31.md")
t_lista = os.path.getmtime(LISTA)
for f in sorted(os.listdir(FIG)):
    if not f.lower().endswith(".png"):
        continue
    if not re.match("^[Pp][0-9]", f):
        continue
    visto = f.lower().startswith("p0")
    fonte = os.path.join(FIG, f[:f.rfind(".")].lower() + ".py")
    velha = os.path.getmtime(os.path.join(FIG, f)) < t_lista
    print("  %-28s vista pela verif.7: %-5s  mais velha que a LISTA: %s"
          % (f, visto, velha))
