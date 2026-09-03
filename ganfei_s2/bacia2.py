"""Bacia contribuinte com pysheds: fill_pits -> fill_depressions -> resolve_flats,
que e o que faltava. GLO-30 sobre 9x8 km em torno do pomar."""
import json, requests, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform as tr
from pysheds.grid import Grid
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
W = (526000, 4649000, 535000, 4657000)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")
f = requests.post("https://earth-search.aws.element84.com/v1/search", json={
    "collections": ["cop-dem-glo-30"],
    "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]}, "limit": 5},
    timeout=90).json()["features"][0]
lo, la = tr("EPSG:32629", "EPSG:4326", [W[0], W[2]], [W[1], W[3]])
with rasterio.Env(**E), rasterio.open(f["assets"]["data"]["href"]) as ds:
    win = from_bounds(min(lo), min(la), max(lo), max(la), transform=ds.transform)
    arr = ds.read(1, window=win)
    T = ds.window_transform(win); crs = ds.crs
prof = {"driver": "GTiff", "height": arr.shape[0], "width": arr.shape[1], "count": 1,
        "dtype": "float32", "crs": crs, "transform": T, "nodata": -9999.0}
with rasterio.open("lidar/_glo30.tif", "w", **prof) as o: o.write(arr.astype("float32"), 1)

grid = Grid.from_raster("lidar/_glo30.tif")
dem = grid.read_raster("lidar/_glo30.tif")
dem = grid.fill_pits(dem)
dem = grid.fill_depressions(dem)
dem = grid.resolve_flats(dem)          # <- o passo que faltava
fdir = grid.flowdir(dem)
acc = grid.accumulation(fdir)
print(f"DEM {np.asarray(dem).shape}  acumulacao max {np.asarray(acc).max():.0f} celulas")

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pm = MP(masks["pomar"]).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)
py, px = np.where(pm)
ux = AOI[0] + px*10; uy = AOI[3] - py*10
glo, gla = tr("EPSG:32629", "EPSG:4326", list(ux), list(uy))

# exutorio: a celula do pomar com maior acumulacao
A = np.asarray(acc); best = None
for x, y in zip(glo, gla):
    c = int((x - T.c)/T.a); r = int((y - T.f)/T.e)
    if 0 <= r < A.shape[0] and 0 <= c < A.shape[1]:
        if best is None or A[r, c] > best[0]: best = (A[r, c], x, y, r, c)
print(f"exutorio: acumulacao {best[0]:.0f} celulas = {best[0]*900/1e4:.1f} ha")
cat = grid.catchment(x=best[1], y=best[2], fdir=fdir, xytype="coordinate")
C = np.asarray(cat)
print(f"bacia do exutorio: {C.sum()} celulas = {C.sum()*900/1e4:.1f} ha")
ys, xs = np.where(C)
lon0 = T.c + xs.min()*T.a; lon1 = T.c + (xs.max()+1)*T.a
lat1 = T.f + ys.min()*T.e; lat0 = T.f + (ys.max()+1)*T.e
print(f"extensao: lon {lon0:.5f}..{lon1:.5f}  lat {lat0:.5f}..{lat1:.5f}")
json.dump({"bbox_wgs84": [lon0, lat0, lon1, lat1], "ha": float(C.sum()*900/1e4)},
          open("lidar/bacia.json", "w"))
fig, ax = plt.subplots(figsize=(11, 10))
ax.imshow(np.asarray(dem), cmap="terrain")
ax.contour(C, levels=[.5], colors="r", linewidths=1.6)
alvo = np.zeros(A.shape, bool)
for x, y in zip(glo, gla):
    c = int((x - T.c)/T.a); r = int((y - T.f)/T.e)
    if 0 <= r < A.shape[0] and 0 <= c < A.shape[1]: alvo[r, c] = True
ax.contour(alvo, levels=[.5], colors="k", linewidths=1.6)
ax.set_title(f"Bacia contribuinte = {C.sum()*900/1e4:.0f} ha (vermelho) | pomar (preto)")
ax.set_xticks([]); ax.set_yticks([])
fig.savefig("bacia.png", dpi=140, bbox_inches="tight")
