"""5(a): 1995 a resolucao nativa sobre os dois focos — valas, charcos, estruturas.
Mais teste da estacao do voo de 2025 pela galeria ripicola (caducifolia)."""
import json, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform as tr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open("sentinel/masks.json"))
def poly(p):
    ux=[AOI[0]+q[0]*10 for q in p]; uy=[AOI[3]-q[1]*10 for q in p]
    ex,ny = tr("EPSG:32629","EPSG:3763",ux,uy); return np.array(list(zip(ex,ny)))
EP = {"1995":"orto/ortos1995_cog_1m_irg_jpg_002-3_v01.tif",
      "2012":"orto/ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
      "2021":"orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
      "2025":"orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"}
def ler(path, bb):
    with rasterio.open(path) as ds:
        w = from_bounds(*bb, transform=ds.transform)
        a = ds.read(window=w).astype("float32"); T = ds.window_transform(w)
    return a, T
def vis(a, ep, realce=True):
    if ep == "1995": rgb = np.stack([a[1], a[2], a[2]], -1)      # R,G,G
    else:            rgb = np.stack([a[0], a[1], a[2]], -1)
    if realce:
        lo, hi = np.percentile(rgb, [2, 98])
        rgb = np.clip((rgb-lo)/max(hi-lo, 1e-6), 0, 1)
    else: rgb = np.clip(rgb/255.0, 0, 1)
    return rgb

# --- 5(a): 1995 a 1 m sobre cada foco, com realce de contraste --------------
fig, axs = plt.subplots(1, 2, figsize=(20, 10))
for ax, k in zip(axs, ("manchaW", "zona0")):
    p = poly(masks[k]); cx, cy = p[:,0].mean(), p[:,1].mean()
    bb = (cx-220, cy-220, cx+220, cy+220)
    a, T = ler(EP["1995"], bb)
    ax.imshow(vis(a, "1995"), interpolation="bilinear")
    px = (p[:,0]-T.c)/T.a; py = (p[:,1]-T.f)/T.e
    ax.plot(np.append(px,px[0]), np.append(py,py[0]),
            color="#C2451E" if k=="manchaW" else "#E4A11B", lw=2.2)
    ax.set_title(f"1995 (Ago–Set), 1 m — {k}  |  440 x 440 m", fontsize=13)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("orto1995_focos.png", dpi=150, bbox_inches="tight")
print("-> orto1995_focos.png")

# --- estacao do voo de 2025: galeria ripicola (caducifolia) -----------------
p = poly(masks["pomar"]); cx = p[:,0].mean()
cyN = p[:,1].max() + 90                      # ~90 m a norte do pomar = galeria
bb = (cx-200, cyN-90, cx+200, cyN+90)
fig, axs = plt.subplots(2, 2, figsize=(18, 9))
for ax, ep in zip(axs.ravel(), ("1995","2012","2021","2025")):
    a, T = ler(EP[ep], bb)
    ax.imshow(vis(a, ep, realce=False), interpolation="bilinear")
    ax.set_title(f"{ep} — galeria ripicola do Minho (caducifolia)", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Arvores com folha = voo de Primavera/Verao; despidas = Marco", fontsize=13)
fig.tight_layout(); fig.savefig("orto_estacao.png", dpi=130, bbox_inches="tight")
print("-> orto_estacao.png")
