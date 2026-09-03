"""Escoamento sobre o MDT LiDAR (1 m, reamostrado de 50 cm), quatro tiles.
Bacia fechada -> acumulacao e linhas de drenagem fiaveis dentro do pomar."""
import json, glob, numpy as np, rasterio
from rasterio.merge import merge
from pysheds.grid import Grid
from matplotlib.path import Path as MP
from rasterio.warp import transform as tr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
srcs = [rasterio.open(p) for p in sorted(glob.glob("lidar/MDT-50cm-*.tif"))]
mos, T0 = merge(srcs, nodata=-999.0)
d = mos[0][::2, ::2].astype("float32")                      # 1 m
T = rasterio.Affine(T0.a*2, 0, T0.c, 0, T0.e*2, T0.f)
d[d == -999.0] = np.nan
print(f"MDT 1 m {d.shape}  nodata {100*np.isnan(d).mean():.2f}%")
d = np.where(np.isnan(d), np.nanmax(d) + 5, d)              # bordo alto, nao suga escoamento
with rasterio.open("lidar/_mdt1m.tif", "w", driver="GTiff", height=d.shape[0],
                   width=d.shape[1], count=1, dtype="float32", crs="EPSG:3763",
                   transform=T, nodata=-9999.0) as o: o.write(d, 1)

grid = Grid.from_raster("lidar/_mdt1m.tif")
dem = grid.read_raster("lidar/_mdt1m.tif")
dem = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(dem)))
fdir = grid.flowdir(dem)
acc = np.asarray(grid.accumulation(fdir))                   # celulas de 1 m2
print(f"acumulacao max {acc.max():.0f} m2")

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
def para(poly):
    ux = [AOI[0] + p[0]*10 for p in poly]; uy = [AOI[3] - p[1]*10 for p in poly]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
H, W = acc.shape
gy, gx = np.mgrid[0:H, 0:W]; gp = np.vstack((gx.ravel(), gy.ravel())).T
mk = {k: MP(para(v)).contains_points(gp).reshape(H, W) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]

# linha de drenagem = acumulacao acima de 2000 m2 (0,2 ha a montante)
LIM = 2000
linha = acc > LIM
print(f"\n{'mascara':10s} {'ha':>6s} {'% em linha de drenagem':>23s} {'acum. mediana m2':>17s} "
      f"{'acum. p95':>10s}")
for k in ("pomar", "saudavel", "manchaW", "zona0"):
    m = mk[k]
    print(f"{k:10s} {m.sum()/1e4:6.2f} {100*linha[m].mean():23.1f} "
          f"{np.median(acc[m]):17.0f} {np.percentile(acc[m],95):10.0f}")

fig, axs = plt.subplots(2, 1, figsize=(16, 12))
cores = {"pomar":"k", "saudavel":"#00b0a0", "manchaW":"#C2451E", "zona0":"#E4A11B"}
ax = axs[0]
im = ax.imshow(np.log10(acc + 1), cmap="cubehelix_r", vmin=0, vmax=4.5)
for k, c in cores.items(): ax.contour(mk[k], levels=[.5], colors=c, linewidths=1.6)
ax.set_title("Acumulação de escoamento sobre o MDT LiDAR 1 m (log10 m² a montante)", fontsize=12)
ax.set_xticks([]); ax.set_yticks([]); fig.colorbar(im, ax=ax, shrink=.85)
ax = axs[1]
ax.imshow(np.where(linha, 1, np.nan), cmap="Blues", vmin=0, vmax=1.4, interpolation="nearest")
for k, c in cores.items(): ax.contour(mk[k], levels=[.5], colors=c, linewidths=1.6)
ax.set_title(f"Linhas de drenagem (> {LIM} m² a montante)", fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("escoamento.png", dpi=140, bbox_inches="tight")
print("\n-> escoamento.png")
