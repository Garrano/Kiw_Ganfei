"""Arquitectura aluvial da veiga: residuo em relacao a uma superficie regional
ajustada (polinomio de 2a ordem sobre a veiga), + sombreado multi-direccional.
Objectivo: paleocanais, barras e diques naturais do Minho."""
import json, numpy as np, rasterio
from rasterio.warp import transform as tr
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
d = np.load("lidar/t2_dem1m.npy")
meta = json.load(open("lidar/t2_dem1m.json"))
T = rasterio.Affine(*meta["transform"])
H, W = d.shape
val = ~np.isnan(d)
veiga = val & (d < 15)
print(f"mosaico {d.shape} @1 m | valido {100*val.mean():.1f}% | veiga(<15 m) {veiga.sum()/1e6:.2f} km2")

# superficie regional: polinomio de 2a ordem ajustado so a veiga
ys, xs = np.where(veiga)
sub = np.random.default_rng(0).choice(ys.size, size=min(400000, ys.size), replace=False)
Y = ys[sub].astype("float64"); X = xs[sub].astype("float64"); Z = d[ys[sub], xs[sub]]
A = np.column_stack([np.ones_like(X), X, Y, X*X, Y*Y, X*Y])
coef, *_ = np.linalg.lstsq(A, Z, rcond=None)
gy, gx = np.mgrid[0:H, 0:W]
trend = (coef[0] + coef[1]*gx + coef[2]*gy + coef[3]*gx*gx + coef[4]*gy*gy + coef[5]*gx*gy)
res = np.where(veiga, d - trend, np.nan)
print(f"residuo na veiga: p2={np.nanpercentile(res,2):+.2f} p50={np.nanpercentile(res,50):+.2f} "
      f"p98={np.nanpercentile(res,98):+.2f} m  dp={np.nanstd(res):.2f}")

masks = json.load(open("sentinel/masks.json"))
yy0, xx0 = np.mgrid[0:100, 0:200]; pts0 = np.vstack((xx0.ravel(), yy0.ravel())).T
def para(poly):
    ux = [AOI[0] + p[0]*10 for p in poly]; uy = [AOI[3] - p[1]*10 for p in poly]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
gp = np.vstack((gx.ravel(), gy.ravel())).T
mk = {k: MP(para(v)).contains_points(gp).reshape(H, W) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
print(f"\n{'mascara':10s} {'residuo medio':>14s} {'p10':>7s} {'p90':>7s}")
for k in ("pomar", "saudavel", "manchaW", "zona0"):
    v = res[mk[k]]; v = v[~np.isnan(v)]
    print(f"{k:10s} {v.mean():+14.3f} {np.percentile(v,10):+7.3f} {np.percentile(v,90):+7.3f}")

def hs(a, az, alt=30):
    z = np.nan_to_num(a, nan=np.nanmean(a))
    gyy, gxx = np.gradient(z)
    slope = np.pi/2 - np.arctan(np.hypot(gxx, gyy)*4)
    asp = np.arctan2(-gxx, gyy)
    A_ = np.radians(360-az+90); L = np.radians(alt)
    return np.sin(L)*np.sin(slope) + np.cos(L)*np.cos(slope)*np.cos(A_-asp)
multi = np.mean([hs(d, a) for a in (0, 90, 180, 270)], axis=0)

fig, axs = plt.subplots(2, 1, figsize=(18, 20))
ax = axs[0]
ax.imshow(np.where(val, multi, np.nan), cmap="gray")
ax.set_title("Sombreado multi-direccional do MDT LiDAR 1 m — T2, 5,9 x 3,7 km", fontsize=13)
ax = axs[1]
im = ax.imshow(res, cmap="RdBu", vmin=-0.8, vmax=0.8)
ax.set_title("Resíduo em relação à superfície regional (veiga) — azul = depressão", fontsize=13)
fig.colorbar(im, ax=ax, shrink=.6, label="m")
for ax in axs:
    for k, c in (("pomar","k"),("saudavel","#00b0a0"),("manchaW","#C2451E"),("zona0","#E4A11B")):
        ax.contour(mk[k], levels=[.5], colors=c, linewidths=2.0)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("t2_paleo.png", dpi=125, bbox_inches="tight")
np.save("lidar/t2_residuo.npy", res.astype("float32"))
print("\n-> t2_paleo.png")
