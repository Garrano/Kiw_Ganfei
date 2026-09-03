# -*- coding: utf-8 -*-
"""C0-01. Geometria bruta dos 11 GeoTIFF da serie principal e dos 11 de b1.

Verifica: CRS, transform, shape, bounds, alinhamento a grelha de 10 m,
igualdade da grelha entre datas, fraccao de NaN (nuvem/SCL) total e dentro
do poligono do pomar. Nada e assumido: tudo sai do ficheiro.
"""
import json
import os
import numpy as np
import rasterio
from matplotlib.path import Path as MP

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI_DECL = (529950, 4654600, 531950, 4655600)
AOI_B1_DECL = (528400, 4654900, 529400, 4655700)

masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))


def rasteriza(poly, H, W):
    yy, xx = np.mgrid[0:H, 0:W]
    pts = np.vstack((xx.ravel(), yy.ravel())).T
    return MP(poly).contains_points(pts).reshape(H, W)


def inspecciona(pasta, aoi_declarada, poligono=None):
    linhas = []
    fich = sorted(f for f in os.listdir(os.path.join(BASE, pasta))
                  if f.endswith(".tif"))
    ref = None
    for f in fich:
        p = os.path.join(BASE, pasta, f)
        with rasterio.open(p) as ds:
            tr = ds.transform
            b = ds.bounds
            arr = ds.read(1)
            crs = str(ds.crs)
            nod = ds.nodata
        H, W = arr.shape
        nan = float(np.isnan(arr).mean() * 100)
        d = dict(ficheiro=f, crs=crs, shape="%dx%d" % (H, W),
                 res="%.3f,%.3f" % (tr.a, tr.e),
                 bounds=(b.left, b.bottom, b.right, b.top),
                 bate_aoi=(round(b.left), round(b.bottom), round(b.right),
                           round(b.top)) == tuple(aoi_declarada),
                 grelha10=(b.left % 10 == 0 and b.top % 10 == 0),
                 nodata=str(nod), nan_pct=round(nan, 4),
                 vmin=float(np.nanmin(arr)), vmax=float(np.nanmax(arr)),
                 vmed=round(float(np.nanmean(arr)), 4))
        if poligono is not None:
            m = rasteriza(poligono, H, W)
            d["nan_dentro_pomar_pct"] = round(
                float(np.isnan(arr[m]).mean() * 100), 4)
            d["ndvi_medio_pomar"] = round(float(np.nanmean(arr[m])), 4)
        if ref is None:
            ref = (crs, tr, arr.shape)
            d["grelha_igual_1a"] = True
        else:
            d["grelha_igual_1a"] = (crs == ref[0] and tr == ref[1]
                                    and arr.shape == ref[2])
        linhas.append(d)
    return linhas


print("=" * 78)
print("SERIE PRINCIPAL  sentinel/   AOI declarada", AOI_DECL)
print("=" * 78)
A = inspecciona("sentinel", AOI_DECL, masks["pomar"])
for d in A:
    print("%s crs=%s %s res=%s bounds=%s bate_AOI=%s grelha_igual=%s "
          "nan=%.3f%% nan_pomar=%.3f%% min=%.3f max=%.3f med_pomar=%.4f"
          % (d["ficheiro"], d["crs"], d["shape"], d["res"],
             tuple(int(x) for x in d["bounds"]), d["bate_aoi"],
             d["grelha_igual_1a"], d["nan_pct"], d["nan_dentro_pomar_pct"],
             d["vmin"], d["vmax"], d["ndvi_medio_pomar"]))

print()
print("=" * 78)
print("SERIE B1 (quarentena)  sentinel_b1/   AOI declarada", AOI_B1_DECL)
print("=" * 78)
B = inspecciona("sentinel_b1", AOI_B1_DECL)
for d in B:
    print("%s crs=%s %s bounds=%s bate_AOI=%s grelha_igual=%s nan=%.3f%% "
          "med=%.4f" % (d["ficheiro"], d["crs"], d["shape"],
                        tuple(int(x) for x in d["bounds"]), d["bate_aoi"],
                        d["grelha_igual_1a"], d["nan_pct"], d["vmed"]))

# sobreposicao das duas AOI
ax0, ay0, ax1, ay1 = AOI_DECL
bx0, by0, bx1, by1 = AOI_B1_DECL
ox = max(0, min(ax1, bx1) - max(ax0, bx0))
oy = max(0, min(ay1, by1) - max(ay0, by0))
print()
print("Sobreposicao AOI principal x AOI b1: %d m x %d m = %.2f ha"
      % (ox, oy, ox * oy / 10000.0))
print("Distancia entre centroides: %.0f m"
      % np.hypot((ax0 + ax1) / 2 - (bx0 + bx1) / 2,
                 (ay0 + ay1) / 2 - (by0 + by1) / 2))
print("Folga em E entre bordo E de b1 (%d) e bordo W da principal (%d): %d m"
      % (bx1, ax0, ax0 - bx1))

json.dump({"principal": A, "b1": B}, open(os.path.join(OUT, "c0_01_rasters.json"),
                                          "w"), indent=1, default=str)
print("\n-> c0_01_rasters.json")
