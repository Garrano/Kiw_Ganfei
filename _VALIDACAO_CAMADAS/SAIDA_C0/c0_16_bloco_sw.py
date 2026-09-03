# -*- coding: utf-8 -*-
"""C0-16. Duas medidas finais.

 a) area do bloco de pomar com rede a sudoeste (onde cai o troco OESTE do
    esquema de rega), medida na ortofoto de 2025 numa janela que so o contem;
 b) o poligono `pomar` esta todo dentro do MDT LiDAR (lidar/dem_aoi.json)?
"""
import json
import os
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
JAN = (529350, 4653700, 530150, 4654550)          # so o bloco SW
RES = 0.5

with rasterio.open(ORTO) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    w = int((JAN[2] - JAN[0]) / RES)
    h = int((JAN[3] - JAN[1]) / RES)
    a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w), boundless=True,
                fill_value=0).astype("float32")
lum = a.mean(0)
mx, mn = a.max(0), a.min(0)
sat = (mx - mn) / np.maximum(mx, 1)
val = lum > 0
sm = ndimage.uniform_filter(lum, 15)
sq = ndimage.uniform_filter(lum * lum, 15)
tex = np.sqrt(np.maximum(sq - sm * sm, 0))
rede = (lum > np.percentile(lum[val], 70)) & (sat < 0.20) & val \
    & (tex > np.percentile(tex[val], 60))
rede = ndimage.binary_closing(rede, np.ones((11, 11)))
rede = ndimage.binary_opening(rede, np.ones((9, 9)))
rede = ndimage.binary_fill_holes(rede)
lab, n = ndimage.label(rede, np.ones((3, 3)))
tam = ndimage.sum(rede, lab, range(1, n + 1)) * RES * RES / 1e4
print("=" * 70)
print("a) BLOCO DE POMAR COM REDE A SUDOESTE — janela %s" % str(JAN))
print("=" * 70)
tot = 0.0
for i in np.argsort(tam)[::-1][:8]:
    if tam[i] < 0.4:
        continue
    m = lab == i + 1
    ys, xs = np.where(m)
    tot += tam[i]
    print("  %5.2f ha   E %d..%d   N %d..%d"
          % (tam[i], JAN[0] + xs.min() * RES, JAN[0] + xs.max() * RES,
             JAN[3] - ys.max() * RES, JAN[3] - ys.min() * RES))
print("  TOTAL dos blocos >=0,4 ha nesta janela: %.2f ha" % tot)
print("  (medida por assinatura de coberto claro + textura de linhas; "
       "sobrestima em caminhos e sub-estima em rede em ma condicao)")
print("  fora da AOI Sentinel? bordo N da janela=%d < bordo S da AOI=%d: %s"
      % (JAN[3], AOI[1], JAN[3] < AOI[1]))

# --------------------------------------------------------------- b) LiDAR
print()
print("=" * 70)
print("b) O POLIGONO `pomar` ESTA DENTRO DO MDT LiDAR?")
print("=" * 70)
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
p = np.array(masks["pomar"], float)
PE = AOI[0] + p[:, 0] * 10.0
PN = AOI[3] - p[:, 1] * 10.0
t = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
mx3, my3 = t.transform(PE, PN)
j = json.load(open(os.path.join(BASE, "lidar", "dem_aoi.json")))
tr = j["transform"]
hh, ww = j["shape"]
x0, y0 = tr[2], tr[5]
x1 = x0 + ww * tr[0]
y1 = y0 + hh * tr[4]
print("  dem_aoi 3763: x %.1f..%.1f  y %.1f..%.1f" % (x0, x1, min(y0, y1),
                                                      max(y0, y1)))
print("  poligono em 3763: x %.1f..%.1f  y %.1f..%.1f"
      % (mx3.min(), mx3.max(), my3.min(), my3.max()))
dentro = (mx3.min() >= min(x0, x1) and mx3.max() <= max(x0, x1)
          and my3.min() >= min(y0, y1) and my3.max() <= max(y0, y1))
print("  poligono `pomar` inteiramente dentro do dem_aoi: %s" % dentro)
c = []
for E in (AOI[0], AOI[2]):
    for N in (AOI[1], AOI[3]):
        c.append(t.transform(E, N))
cx = [q[0] for q in c]
print("  AOI inteira dentro do dem_aoi: %s   (falta a leste: %.0f m)"
      % (max(cx) <= max(x0, x1), max(0.0, max(cx) - max(x0, x1))))
