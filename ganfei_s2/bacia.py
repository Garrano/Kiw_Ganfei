"""Delimita a bacia que drena para o pomar, com Copernicus DEM 30 m,
e traduz o resultado em tiles DGT necessarios."""
import json, requests, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds, transform as tr
from skimage.morphology import reconstruction
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
W = (526000, 4649000, 535000, 4657000)          # 9 x 8 km, apanha o monte a sul
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")
f = requests.post("https://earth-search.aws.element84.com/v1/search", json={
    "collections": ["cop-dem-glo-30"],
    "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]}, "limit": 5},
    timeout=90).json()["features"][0]
lo, la = tr("EPSG:32629", "EPSG:4326", [W[0], W[2]], [W[1], W[3]])
with rasterio.Env(**E), rasterio.open(f["assets"]["data"]["href"]) as ds:
    win = from_bounds(min(lo), min(la), max(lo), max(la), transform=ds.transform)
    dem = ds.read(1, window=win).astype("float64")
    T = ds.window_transform(win); CRS = ds.crs
H, Wd = dem.shape
print(f"DEM {dem.shape}  cota {dem.min():.0f}..{dem.max():.0f} m")

# enchimento de depressoes
sem = dem.copy(); sem[1:-1,1:-1] = dem.max()
fill = reconstruction(sem, dem, method="erosion")

# D8: receptor de cada celula
dy = [-1,-1,-1,0,0,1,1,1]; dx = [-1,0,1,-1,1,-1,0,1]
dist = np.array([np.sqrt(2),1,np.sqrt(2),1,1,np.sqrt(2),1,np.sqrt(2)])
best = np.full((H,Wd), -1, np.int8); slope = np.zeros((H,Wd))
for k in range(8):
    viz = np.full((H,Wd), np.inf)
    ys0,ys1 = max(0,dy[k]), H+min(0,dy[k]); xs0,xs1 = max(0,dx[k]), Wd+min(0,dx[k])
    viz[ys0:ys1, xs0:xs1] = fill[max(0,-dy[k]):H-max(0,dy[k]), max(0,-dx[k]):Wd-max(0,dx[k])]
    s = (fill - viz) / dist[k]
    m = s > slope
    slope[m] = s[m]; best[m] = k

# celulas do pomar (em graus -> indice do DEM)
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pm = MP(masks["pomar"]).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100,200)
py, px = np.where(pm)
ux = AOI[0] + px*10; uy = AOI[3] - py*10
glo, gla = tr("EPSG:32629", "EPSG:4326", list(ux), list(uy))
alvo = np.zeros((H,Wd), bool)
for x, y in zip(glo, gla):
    c = int((x - T.c)/T.a); r = int((y - T.f)/T.e)
    if 0 <= r < H and 0 <= c < Wd: alvo[r, c] = True
print(f"celulas de 30 m sobre o pomar: {alvo.sum()}")

# propagacao a montante: adiciona quem drena para uma celula ja marcada
bacia = alvo.copy()
for it in range(4000):
    novo = np.zeros_like(bacia)
    for k in range(8):
        ys0,ys1 = max(0,dy[k]), H+min(0,dy[k]); xs0,xs1 = max(0,dx[k]), Wd+min(0,dx[k])
        recebe = np.zeros((H,Wd), bool)
        recebe[ys0:ys1, xs0:xs1] = bacia[max(0,-dy[k]):H-max(0,dy[k]), max(0,-dx[k]):Wd-max(0,dx[k])]
        novo |= (best == k) & recebe
    if (novo & ~bacia).sum() == 0: break
    bacia |= novo
print(f"bacia contribuinte: {bacia.sum()} celulas = {bacia.sum()*900/1e4:.1f} ha  ({it} iteracoes)")

ys, xs = np.where(bacia)
lon0 = T.c + xs.min()*T.a; lon1 = T.c + (xs.max()+1)*T.a
lat1 = T.f + ys.min()*T.e; lat0 = T.f + (ys.max()+1)*T.e
print(f"extensao da bacia: lon {lon0:.5f}..{lon1:.5f}  lat {lat0:.5f}..{lat1:.5f}")
json.dump({"bbox_wgs84": [lon0, lat0, lon1, lat1], "ha": bacia.sum()*900/1e4},
          open("lidar/bacia.json", "w"))
plt.figure(figsize=(10,9))
plt.imshow(fill, cmap="terrain"); plt.contour(bacia, levels=[.5], colors="r", linewidths=1.5)
plt.contour(alvo, levels=[.5], colors="k", linewidths=1.5)
plt.title(f"Bacia que drena para o pomar — {bacia.sum()*900/1e4:.0f} ha (GLO-30)")
plt.xticks([]); plt.yticks([])
plt.savefig("bacia.png", dpi=140, bbox_inches="tight")
