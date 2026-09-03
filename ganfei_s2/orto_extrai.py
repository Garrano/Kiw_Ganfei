"""Recorte das 4 epocas sobre o pomar + zoom na Mancha W e na Zona 0."""
import json, glob, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds, transform as tr
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
B = transform_bounds("EPSG:32629", "EPSG:3763", *AOI)
B = (B[0], B[1], min(B[2], -40010), B[3])          # tile acaba em -40000
print("janela EPSG:3763:", [round(v) for v in B])
EP = {"1995": "orto/ortos1995_cog_1m_irg_jpg_002-3_v01.tif",
      "2012": "orto/ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
      "2021": "orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
      "2025": "orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"}

masks = json.load(open("sentinel/masks.json"))
def poly3763(p):
    ux = [AOI[0]+q[0]*10 for q in p]; uy = [AOI[3]-q[1]*10 for q in p]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return list(zip(ex, ny))

def ler(path, bounds, maxpx=2400):
    with rasterio.open(path) as ds:
        w = from_bounds(*bounds, transform=ds.transform)
        h = int(w.height); wd = int(w.width)
        f = max(1, int(max(h, wd)/maxpx))
        out = (ds.count, max(1, h//f), max(1, wd//f))
        a = ds.read(window=w, out_shape=out).astype("float32")
        T = ds.window_transform(w)
        T = rasterio.Affine(T.a*f, 0, T.c, 0, T.e*f, T.f)
        return a, T

def rgb_ndvi(a, ep):
    if ep == "1995":                       # IRG: b1=IR, b2=R, b3=G
        ir, r, g = a[0], a[1], a[2]
        rgb = np.stack([r, g, np.clip(g*1.05, 0, 255)], -1)/255.0
        nd = (ir-r)/np.maximum(ir+r, 1e-6)
    else:                                  # RGBI: b1=R b2=G b3=B b4=NIR
        r, g, b, nir = a[0], a[1], a[2], a[3]
        rgb = np.stack([r, g, b], -1)/255.0
        nd = (nir-r)/np.maximum(nir+r, 1e-6)
    return np.clip(rgb, 0, 1), nd

for nome, bb, mx in (("pomar", B, 2400),
                     ("manchaW", None, 1400), ("zona0", None, 1400)):
    if nome != "pomar":
        pp = np.array(poly3763(masks[nome]))
        cx, cy = pp[:,0].mean(), pp[:,1].mean()
        bb = (cx-260, cy-260, cx+260, cy+260)
    fig, axs = plt.subplots(2, 4, figsize=(24, 11))
    for j, (ep, path) in enumerate(EP.items()):
        a, T = ler(path, bb, mx)
        rgb, nd = rgb_ndvi(a, ep)
        axs[0, j].imshow(rgb); axs[0, j].set_title(f"{ep}  {'IRG' if ep=='1995' else 'RGB'}",
                                                   fontsize=13)
        im = axs[1, j].imshow(nd, cmap="RdYlGn", vmin=0.0, vmax=0.75)
        axs[1, j].set_title(f"{ep}  NDVI", fontsize=13)
        for ax in (axs[0, j], axs[1, j]):
            for k, c in (("pomar","k"),("manchaW","#C2451E"),("zona0","#E4A11B")):
                p = np.array(poly3763(masks[k]))
                px = (p[:,0]-T.c)/T.a; py = (p[:,1]-T.f)/T.e
                ax.plot(np.append(px, px[0]), np.append(py, py[0]), color=c, lw=1.6)
            ax.set_xlim(0, rgb.shape[1]); ax.set_ylim(rgb.shape[0], 0)
            ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(f"Ortofotos DGT — {nome}", fontsize=15)
    fig.tight_layout(); fig.savefig(f"orto_{nome}.png", dpi=110, bbox_inches="tight")
    plt.close(fig); print(f"-> orto_{nome}.png")
