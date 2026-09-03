# -*- coding: utf-8 -*-
"""CTRL-00. Que area util temos? Extensao das ortofotos e do LiDAR em 32629.

Nao le NDVI nem qualquer indice. So metadados geometricos.
"""
import os
import glob
import rasterio
from rasterio.warp import transform_bounds

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)     # so referencia de distancia
CX = (CASO[0] + CASO[2]) / 2.0
CY = (CASO[1] + CASO[3]) / 2.0

print("=" * 92)
print("CENTROIDE DO POMAR DO CASO (so para distancias): E %.1f  N %.1f" % (CX, CY))
print("=" * 92)

for f in sorted(glob.glob(os.path.join(BASE, "orto", "*.tif"))):
    with rasterio.open(f) as ds:
        b = transform_bounds(ds.crs, "EPSG:32629", *ds.bounds, densify_pts=21)
        print("%-58s %s res=%.2f nb=%d" % (os.path.basename(f)[:58],
                                           str(ds.crs), ds.transform.a, ds.count))
        print("    32629: E %.0f..%.0f  N %.0f..%.0f   (%.2f x %.2f km)"
              % (b[0], b[2], b[1], b[3], (b[2] - b[0]) / 1000, (b[3] - b[1]) / 1000))
        print("    raio util a partir do centroide: O %.0f  E %.0f  S %.0f  N %.0f m"
              % (CX - b[0], b[2] - CX, CY - b[1], b[3] - CY))

print()
print("=" * 92)
print("LiDAR MDT — mosaicos")
print("=" * 92)
for f in sorted(glob.glob(os.path.join(BASE, "lidar", "MDT-*.tif"))):
    with rasterio.open(f) as ds:
        b = transform_bounds(ds.crs, "EPSG:32629", *ds.bounds, densify_pts=21)
        print("  %-42s %s res=%.2f  32629 E %.0f..%.0f N %.0f..%.0f"
              % (os.path.basename(f), str(ds.crs), ds.transform.a,
                 b[0], b[2], b[1], b[3]))
