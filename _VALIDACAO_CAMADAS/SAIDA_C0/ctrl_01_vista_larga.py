# -*- coding: utf-8 -*-
"""CTRL-01. Vista larga de prospeccao, 3 km em redor do pomar do caso.

REGRA DURA DESTA SESSAO: nao se le a banda NIR, nao se calcula NDVI nem
qualquer indice de vegetacao. Le-se APENAS R,G,B da ortofoto (estrutura) e
o MDT LiDAR (geometria). O detector abaixo e de ESTRUTURA (periodicidade de
linhas) e nao de vigor.

Produz:
  ctrl_01_vista_larga.png     — mosaico RGB 2025 com grelha de 250 m
  ctrl_01_mdt.png             — MDT LiDAR da mesma janela (para achar o rio)
"""
import os
import glob
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO25 = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
BLOCO_SW = (529350.0, 4653700.0, 530085.0, 4654478.0)

# janela de prospeccao: 3 km em redor, cortada pela cobertura da ortofoto
JAN = (527840.0, 4652200.0, 531795.0, 4655785.0)
RES = 1.0


def ler_rgb(caminho, jan, res):
    with rasterio.open(caminho) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0)
    return np.moveaxis(a, 0, -1).astype("float32")


rgb = ler_rgb(ORTO25, JAN, RES)
rgb = np.clip(rgb / max(np.percentile(rgb, 99.5), 1.0), 0, 1)
print("vista larga %s  janela %s" % (rgb.shape, tuple(int(x) for x in JAN)))

fig, ax = plt.subplots(figsize=(19, 17), dpi=190)
ax.imshow(rgb, extent=[JAN[0], JAN[2], JAN[1], JAN[3]])
ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0], CASO[3] - CASO[1],
                       fill=False, edgecolor="red", lw=2.0))
ax.add_patch(Rectangle((BLOCO_SW[0], BLOCO_SW[1]), BLOCO_SW[2] - BLOCO_SW[0],
                       BLOCO_SW[3] - BLOCO_SW[1], fill=False,
                       edgecolor="yellow", lw=2.0))
for e in range(int(JAN[0]) // 250 * 250, int(JAN[2]) + 250, 250):
    if JAN[0] <= e <= JAN[2]:
        ax.axvline(e, color="w", lw=0.3, alpha=0.45)
        ax.text(e + 8, JAN[1] + 20, str(e), color="w", fontsize=4.5, rotation=90)
for n in range(int(JAN[1]) // 250 * 250, int(JAN[3]) + 250, 250):
    if JAN[1] <= n <= JAN[3]:
        ax.axhline(n, color="w", lw=0.3, alpha=0.45)
        ax.text(JAN[0] + 10, n + 8, str(n), color="w", fontsize=4.5)
ax.set_title("Ortofoto DGT 2025 (25 cm, reamostrada a 1 m) — prospeccao. "
             "vermelho: pomar do caso; amarelo: bloco SW", fontsize=10)
fig.savefig(os.path.join(OUT, "ctrl_01_vista_larga.png"), bbox_inches="tight")
plt.close(fig)
print("-> ctrl_01_vista_larga.png")

# ------------------------------------------------------------------ MDT
mos = []
for f in sorted(glob.glob(os.path.join(BASE, "lidar", "MDT-*.tif"))):
    with rasterio.open(f) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
        if (jb[0] > ds.bounds.right or jb[2] < ds.bounds.left
                or jb[1] > ds.bounds.top or jb[3] < ds.bounds.bottom):
            continue
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((JAN[2] - JAN[0]) / 2.0))
        h = int(round((JAN[3] - JAN[1]) / 2.0))
        a = ds.read(1, window=win, out_shape=(h, w), boundless=True,
                    fill_value=np.nan).astype("float32")
        nd = ds.nodata
        if nd is not None:
            a[a == nd] = np.nan
        a[a < -100] = np.nan
        mos.append(a)
dem = np.full(mos[0].shape, np.nan, "float32")
for a in mos:
    m = np.isnan(dem) & ~np.isnan(a)
    dem[m] = a[m]
print("MDT cobertura na janela: %.1f%%" % (100.0 * np.isfinite(dem).mean()))

fig, ax = plt.subplots(figsize=(15, 14), dpi=160)
im = ax.imshow(dem, extent=[JAN[0], JAN[2], JAN[1], JAN[3]], cmap="terrain",
               vmin=np.nanpercentile(dem, 1), vmax=np.nanpercentile(dem, 97))
plt.colorbar(im, ax=ax, shrink=0.6, label="m")
ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0], CASO[3] - CASO[1],
                       fill=False, edgecolor="red", lw=1.6))
ax.add_patch(Rectangle((BLOCO_SW[0], BLOCO_SW[1]), BLOCO_SW[2] - BLOCO_SW[0],
                       BLOCO_SW[3] - BLOCO_SW[1], fill=False,
                       edgecolor="k", lw=1.6))
ax.set_title("MDT LiDAR DGT 50 cm (reamostrado a 2 m) — janela de prospeccao",
             fontsize=10)
fig.savefig(os.path.join(OUT, "ctrl_01_mdt.png"), bbox_inches="tight")
plt.close(fig)
np.save(os.path.join(OUT, "ctrl_01_dem2m.npy"), dem)
print("-> ctrl_01_mdt.png  +  ctrl_01_dem2m.npy (2 m, janela acima)")
