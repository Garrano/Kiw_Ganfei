# -*- coding: utf-8 -*-
"""Q4e - a cota do B1, medida dos mosaicos que ja estavam em disco.

A peca afirma «nao ha cota, nao ha declive, nao ha drenagem» para o B1.
Os mosaicos MDT-50cm-157564 e -158564 cobrem 100 % do sector e estavam na
mesma pasta que o resto. Isto le-os.
"""
import json
import os

import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as sht, unary_union

LID = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
AQUI = os.path.dirname(os.path.abspath(__file__))

tw = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
CUL = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
parc = []
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL:
        parc.append((int(f["properties"]["CUL_ID"]),
                     sht(lambda x, y, z=None: tw.transform(x, y),
                         shape(f["geometry"])).buffer(0)))

TILES = [os.path.join(LID, "MDT-50cm-157564-07-2025_v02.tif"),
         os.path.join(LID, "MDT-50cm-158564-07-2025_v02.tif")]


def cota_de(geom):
    vals = []
    for t in TILES:
        with rasterio.open(t) as s:
            if not geom.intersects(
                    __import__("shapely").geometry.box(*s.bounds)):
                continue
            try:
                out, _ = rio_mask(s, [mapping(geom)], crop=True, filled=True,
                                  nodata=-999.0)
            except ValueError:
                continue
            v = out[0].astype("float64")
            v[v <= -998] = np.nan
            vals.append(v[np.isfinite(v)])
    return np.concatenate(vals) if vals else np.array([])


print("=== cota do sector B1, do MDT LiDAR de 50 cm (EPSG:3763) ===")
print("%-10s %8s %10s %8s %8s %8s %8s"
      % ("CUL_ID", "ha", "n px", "mediana", "media", "p5", "p95"))
todos = []
for cid, g in parc:
    v = cota_de(g)
    todos.append(v)
    if v.size:
        print("%-10d %8.2f %10d %8.3f %8.3f %8.3f %8.3f"
              % (cid, g.area / 1e4, v.size, np.median(v), v.mean(),
                 np.percentile(v, 5), np.percentile(v, 95)))
    else:
        print("%-10d %8.2f %10s" % (cid, g.area / 1e4, "SEM DADO"))
V = np.concatenate([t for t in todos if t.size])
UNI = unary_union([g for _, g in parc])
print("-" * 72)
print("%-10s %8.2f %10d %8.3f %8.3f %8.3f %8.3f"
      % ("B1 todo", UNI.area / 1e4, V.size, np.median(V), V.mean(),
         np.percentile(V, 5), np.percentile(V, 95)))
print("cobertura: %.1f %% da area do sector (a 0,5 m)"
      % (100 * V.size * 0.25 / UNI.area))

print()
print("=== o B1 contra as quatro unidades do C9 ===")
VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
TER = json.load(open(os.path.join(VC, "SAIDA_C1",
                                  "c1_04_terreno_por_unidade.json"),
                     encoding="utf-8"))
linhas = [("foco ORIENTAL", TER["foco ESTE (disco 90 m)"]["cota"]),
          ("resto do pomar", TER["resto do pomar"]["cota"]),
          ("referencia", TER["referencia sistematica"]["cota"]),
          ("foco OCIDENTAL", TER["foco OESTE (disco 90 m)"]["cota"]),
          ("sector B1", float(np.median(V)))]
for n, c in sorted(linhas, key=lambda x: -x[1]):
    marca = ""
    if n == "foco ORIENTAL":
        marca = "  <- a peca chama-lhe O PONTO ALTO"
    if n == "foco OCIDENTAL":
        marca = "  <- a peca chama-lhe O PONTO BAIXO"
    if n == "sector B1":
        marca = "  <- MEDIDO AQUI, e a peca diz que nao existe"
    print("   %-16s %7.2f m%s" % (n, c, marca))
print()
print("   contraste ORIENTAL - OCIDENTAL : %.3f m  (o '1,20 m' da peca)"
      % (TER["foco ESTE (disco 90 m)"]["cota"]
         - TER["foco OESTE (disco 90 m)"]["cota"]))
print("   contraste ORIENTAL - B1        : %.3f m"
      % (TER["foco ESTE (disco 90 m)"]["cota"] - np.median(V)))
print("   contraste OCIDENTAL - B1       : %.3f m"
      % (TER["foco OESTE (disco 90 m)"]["cota"] - np.median(V)))
np.save(os.path.join(AQUI, "b1_cota_50cm.npy"), V)
json.dump({"cota_mediana_m": float(np.median(V)),
           "cota_media_m": float(V.mean()),
           "cota_p5_m": float(np.percentile(V, 5)),
           "cota_p95_m": float(np.percentile(V, 95)),
           "n_px_50cm": int(V.size),
           "area_ha": float(UNI.area / 1e4),
           "mosaicos": [os.path.basename(t) for t in TILES],
           "nota": ("cota do sector B1 medida pelo Controlo 3 a 04-09-2026 "
                    "dos mosaicos que ja estavam em disco; a P10 afirma que "
                    "este sector nao tem cota")},
          open(os.path.join(AQUI, "b1_cota.json"), "w", encoding="utf-8"),
          ensure_ascii=True, indent=1)
print("\nescrito b1_cota.json e b1_cota_50cm.npy")
