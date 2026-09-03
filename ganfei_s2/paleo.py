"""Micro-morfologia da veia aluvial: residuo do MDT em relacao a superficie
regional. Revela paleocanais e a arquitectura do aluviao, que e o que determina
a drenagem interna — e que o escoamento de superficie nao mostra."""
import json, glob, numpy as np, rasterio
from rasterio.merge import merge
from scipy import ndimage
from matplotlib.path import Path as MP
from rasterio.warp import transform as tr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
srcs = [rasterio.open(p) for p in sorted(glob.glob("lidar/MDT-50cm-*.tif"))]
mos, T0 = merge(srcs, nodata=-999.0)
d = mos[0][::2, ::2].astype("float32")
T = rasterio.Affine(T0.a*2, 0, T0.c, 0, T0.e*2, T0.f)
d[d == -999.0] = np.nan
val = ~np.isnan(d)
base = np.where(val, d, np.nanmedian(d))
res = d - ndimage.uniform_filter(base, size=151)      # residuo a 150 m
res[~val] = np.nan
# so a veiga: abaixo de 12 m exclui a encosta
veiga = val & (d < 12)
print(f"veiga (<12 m): {veiga.sum()/1e4:.1f} ha de {val.sum()/1e4:.1f} ha")
print(f"residuo na veiga: p5={np.nanpercentile(res[veiga],5):+.2f} "
      f"p50={np.nanpercentile(res[veiga],50):+.2f} p95={np.nanpercentile(res[veiga],95):+.2f} m")

masks = json.load(open("sentinel/masks.json"))
H, W = d.shape
gy, gx = np.mgrid[0:H, 0:W]; gp = np.vstack((gx.ravel(), gy.ravel())).T
def para(poly):
    ux = [AOI[0] + p[0]*10 for p in poly]; uy = [AOI[3] - p[1]*10 for p in poly]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
mk = {k: MP(para(v)).contains_points(gp).reshape(H, W) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
print(f"\n{'mascara':10s} {'residuo medio':>14s} {'% abaixo de -10 cm':>20s}")
for k in ("pomar", "saudavel", "manchaW", "zona0"):
    v = res[mk[k]]; v = v[~np.isnan(v)]
    print(f"{k:10s} {v.mean():+14.3f} {100*(v < -0.10).mean():20.1f}")

# sombreado para leitura visual
def hillshade(a, az=315, alt=35):
    x, y = np.gradient(np.nan_to_num(a, nan=np.nanmean(a)))
    slope = np.pi/2 - np.arctan(np.hypot(x, y))
    asp = np.arctan2(-x, y)
    az = np.radians(360-az+90); alt = np.radians(alt)
    return (np.sin(alt)*np.sin(slope) + np.cos(alt)*np.cos(slope)*np.cos(az-asp))
fig, axs = plt.subplots(1, 2, figsize=(22, 11))
axs[0].imshow(hillshade(d), cmap="gray")
axs[0].set_title("Sombreado do MDT LiDAR (1 m) — 2 x 2 km", fontsize=12)
im = axs[1].imshow(np.where(veiga, res, np.nan), cmap="RdBu", vmin=-0.35, vmax=0.35)
axs[1].set_title("Resíduo do terreno a 150 m — azul = baixo (paleocanais?)", fontsize=12)
fig.colorbar(im, ax=axs[1], shrink=.7, label="m")
for ax in axs:
    for k, c in (("pomar","k"),("saudavel","#00b0a0"),("manchaW","#C2451E"),("zona0","#E4A11B")):
        ax.contour(mk[k], levels=[.5], colors=c, linewidths=1.7)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("paleo.png", dpi=140, bbox_inches="tight")
print("\n-> paleo.png")
