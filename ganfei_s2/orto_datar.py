"""(1) Datar a plantacao: 1995->2012. (2) Grelha de coordenadas sobre o traco."""
import json, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds, transform as tr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open("sentinel/masks.json"))
def poly(p):
    ux=[AOI[0]+q[0]*10 for q in p]; uy=[AOI[3]-q[1]*10 for q in p]
    ex,ny = tr("EPSG:32629","EPSG:3763",ux,uy); return np.array(list(zip(ex,ny)))
EP = [("1995","orto/ortos1995_cog_1m_irg_jpg_002-3_v01.tif"),
      ("2004-06","orto/ortos20042006_cog_50cm_rgbi_jpg_002-3_v01.tif"),
      ("2007","orto/ortos2007_cog_50cm_rgbi_jpg_002-3_v01.tif"),
      ("2010","orto/ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif"),
      ("2012","orto/ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif")]
def ler(path, bb, maxpx=1800):
    with rasterio.open(path) as ds:
        w = from_bounds(*bb, transform=ds.transform)
        h,wd = int(w.height), int(w.width); f = max(1, int(max(h,wd)/maxpx))
        a = ds.read(window=w, out_shape=(ds.count, max(1,h//f), max(1,wd//f))).astype("float32")
        T = ds.window_transform(w); T = rasterio.Affine(T.a*f,0,T.c,0,T.e*f,T.f)
    return a, T
def vis(a, ep):
    rgb = np.stack([a[1],a[2],a[2]],-1) if ep=="1995" else np.stack([a[0],a[1],a[2]],-1)
    lo,hi = np.percentile(rgb,[2,98]); return np.clip((rgb-lo)/max(hi-lo,1e-6),0,1)

# (1) plantacao: zoom no centro da lente
p = poly(masks["manchaW"]); cx, cy = p[:,0].mean(), p[:,1].mean()
bb = (cx-160, cy-160, cx+160, cy+160)
fig, axs = plt.subplots(1, 5, figsize=(26, 6))
for ax,(ep,path) in zip(axs, EP):
    a,T = ler(path, bb, 900)
    ax.imshow(vis(a,ep), interpolation="bilinear")
    ax.set_title(f"{ep}  |  320 x 320 m", fontsize=13)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Datar a plantacao — centro da Mancha W", fontsize=15)
fig.tight_layout(); fig.savefig("orto_plantacao.png", dpi=130, bbox_inches="tight")
print("-> orto_plantacao.png")

# (2) 1995 sobre a Mancha W com grelha UTM29N de 50 m
p = poly(masks["manchaW"]); cx, cy = p[:,0].mean(), p[:,1].mean()
bb = (cx-230, cy-230, cx+230, cy+230)
a, T = ler(EP[0][1], bb, 2000)
img = vis(a, "1995")
H, W = img.shape[:2]
fig, ax = plt.subplots(figsize=(16, 16))
ax.imshow(img, interpolation="bilinear")
# grelha em UTM29N
cor = np.array([[T.c + i*T.a, T.f + j*T.e] for j in (0, H) for i in (0, W)])
ux, uy = tr("EPSG:3763", "EPSG:32629", list(cor[:,0]), list(cor[:,1]))
e0, e1 = min(ux), max(ux); n0, n1 = min(uy), max(uy)
for E in range(int(e0//50*50), int(e1)+50, 50):
    for N in range(int(n0//50*50), int(n1)+50, 50):
        x3, y3 = tr("EPSG:32629","EPSG:3763",[E],[N])
        px = (x3[0]-T.c)/T.a; py = (y3[0]-T.f)/T.e
        if 0 <= px < W and 0 <= py < H:
            ax.plot(px, py, "+", color="cyan", ms=9, mew=1.3)
            ax.text(px+4, py-4, f"{E:.0f}\n{N:.0f}", fontsize=6, color="cyan")
pp = (p - [T.c, T.f]) / [T.a, T.e]
ax.plot(np.append(pp[:,0],pp[0,0]), np.append(pp[:,1],pp[0,1]), color="#C2451E", lw=2)
ax.set_title("1995, 1 m — Mancha W — cruzes = grelha UTM29N de 50 m (E/N)", fontsize=13)
ax.set_xticks([]); ax.set_yticks([])
fig.savefig("orto1995_grelha.png", dpi=150, bbox_inches="tight")
print("-> orto1995_grelha.png")
