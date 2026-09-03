"""Micro-morfologia do terraco aluvial: detrending LOCAL com janela grande,
so sobre a faixa 3-12 m (terraco), fora do canal e da encosta."""
import json, numpy as np, rasterio
from scipy import ndimage
from rasterio.warp import transform as tr
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
d = np.load("lidar/t2_dem1m.npy"); meta = json.load(open("lidar/t2_dem1m.json"))
T = rasterio.Affine(*meta["transform"]); H, W = d.shape
val = ~np.isnan(d)
terr = val & (d > 3) & (d < 12)
print(f"terraco 3-12 m: {terr.sum()/1e6:.2f} km2")

def media_local(a, m, size):
    num = ndimage.uniform_filter(np.where(m, a, 0.0), size=size)
    den = ndimage.uniform_filter(m.astype("float32"), size=size)
    return np.where(den > 0.05, num/np.maximum(den, 1e-6), np.nan)

for JAN in (301, 601):
    base = media_local(np.nan_to_num(d), terr, JAN)
    r = np.where(terr, d - base, np.nan)
    print(f"janela {JAN} m: residuo p2={np.nanpercentile(r,2):+.2f} "
          f"p50={np.nanpercentile(r,50):+.2f} p98={np.nanpercentile(r,98):+.2f} "
          f"dp={np.nanstd(r):.3f} m")
    if JAN == 601: res = r

masks = json.load(open("sentinel/masks.json"))
gy, gx = np.mgrid[0:H, 0:W]; gp = np.vstack((gx.ravel(), gy.ravel())).T
def para(poly):
    ux = [AOI[0] + p[0]*10 for p in poly]; uy = [AOI[3] - p[1]*10 for p in poly]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
mk = {k: MP(para(v)).contains_points(gp).reshape(H, W) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
print(f"\n{'mascara':10s} {'residuo medio':>14s} {'p10':>8s} {'p90':>8s} {'% < -20 cm':>12s}")
for k in ("pomar", "saudavel", "manchaW", "zona0"):
    v = res[mk[k]]; v = v[~np.isnan(v)]
    print(f"{k:10s} {v.mean():+14.3f} {np.percentile(v,10):+8.3f} {np.percentile(v,90):+8.3f} "
          f"{100*(v < -0.20).mean():12.1f}")

def hs(a, az, alt=25):
    z = np.nan_to_num(a, nan=float(np.nanmean(a)))
    gyy, gxx = np.gradient(z)
    slope = np.pi/2 - np.arctan(np.hypot(gxx, gyy)*6)
    asp = np.arctan2(-gxx, gyy)
    A_ = np.radians(360-az+90); L = np.radians(alt)
    return np.sin(L)*np.sin(slope) + np.cos(L)*np.cos(slope)*np.cos(A_-asp)
multi = np.mean([hs(np.where(terr, d, np.nan), a) for a in (0, 90, 180, 270)], axis=0)

fig, axs = plt.subplots(2, 1, figsize=(19, 21))
axs[0].imshow(np.where(terr, multi, np.nan), cmap="gray")
axs[0].set_title("Sombreado multi-direccional — terraço aluvial (3–12 m), MDT 1 m", fontsize=13)
im = axs[1].imshow(res, cmap="RdBu", vmin=-0.5, vmax=0.5)
axs[1].set_title("Resíduo local (janela 600 m) — azul = depressão", fontsize=13)
fig.colorbar(im, ax=axs[1], shrink=.6, label="m")
for ax in axs:
    for k, c in (("pomar","k"),("saudavel","#00b0a0"),("manchaW","#C2451E"),("zona0","#E4A11B")):
        ax.contour(mk[k], levels=[.5], colors=c, linewidths=2.0)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("t2_paleo.png", dpi=125, bbox_inches="tight")
np.save("lidar/t2_residuo.npy", res.astype("float32"))
print("\n-> t2_paleo.png")
