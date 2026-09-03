"""NDRE (red-edge) contra NDVI: deteccao mais precoce da frente activa?
B05 (red-edge 1, 20 m) e B08 (NIR, 10 m), mesmas 11 cenas."""
import json, csv, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
prov = json.load(open("sentinel/proveniencia.json"))

def uma(c):
    data, cid = c["data"], c["cena"]
    a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     f"sentinel-2-l2a/items/{cid}", timeout=90).json()["assets"]
    def rd(k, shape=None):
        with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
            w = from_bounds(*AOI, transform=ds.transform)
            if shape is None: return ds.read(1, window=w).astype("float32")
            return ds.read(1, window=w, out_shape=shape,
                           resampling=Resampling.bilinear).astype("float32")
    nir = rd("nir"); red = rd("red")
    re1 = rd("rededge1", nir.shape); scl = rd("scl", nir.shape)
    bom = ~np.isin(scl.astype(int), [0, 1, 3, 8, 9, 10])
    with np.errstate(invalid="ignore", divide="ignore"):
        ndvi = (nir-red)/(nir+red)
        ndre = (nir-re1)/(nir+re1)
    out = {"data": data}
    for nm in ("saudavel", "pomar", "manchaW", "zona0"):
        m = mk[nm] & bom
        out[f"{nm}_ndvi"] = round(float(np.nanmean(ndvi[m])), 4)
        out[f"{nm}_ndre"] = round(float(np.nanmean(ndre[m])), 4)
    return out

with ThreadPoolExecutor(max_workers=6) as ex:
    L = sorted(ex.map(uma, prov["cenas"]), key=lambda r: r["data"])
with open("rededge.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
print(f"{'data':12s} | {'NDVI: W-sa':>11s} {'Z0-sa':>7s} | {'NDRE: W-sa':>11s} {'Z0-sa':>7s} "
      f"| {'razao W':>8s}")
for r in L:
    dv = r["manchaW_ndvi"]-r["saudavel_ndvi"]; dz = r["zona0_ndvi"]-r["saudavel_ndvi"]
    ev = r["manchaW_ndre"]-r["saudavel_ndre"]; ez = r["zona0_ndre"]-r["saudavel_ndre"]
    raz = ev/dv if abs(dv) > 0.004 else float("nan")
    print(f"{r['data']:12s} | {dv:+11.4f} {dz:+7.4f} | {ev:+11.4f} {ez:+7.4f} | {raz:8.2f}")
xs = [r["data"] for r in L]
fig, ax = plt.subplots(figsize=(12, 6))
for nm, c in (("manchaW", "#C2451E"), ("zona0", "#E4A11B")):
    ax.plot(xs, [r[f"{nm}_ndvi"]-r["saudavel_ndvi"] for r in L], "-o", color=c, lw=2,
            label=f"{nm} NDVI")
    ax.plot(xs, [r[f"{nm}_ndre"]-r["saudavel_ndre"] for r in L], "--s", color=c, lw=1.8,
            alpha=.75, label=f"{nm} NDRE")
ax.axhline(0, color="k", lw=1); ax.set_ylabel("indice menos zona sa")
ax.grid(alpha=.25); ax.legend(frameon=False, ncol=2)
ax.set_title("NDRE (red-edge) contra NDVI — desvio em relacao a zona sa")
plt.xticks(rotation=45, ha="right"); fig.tight_layout(); fig.savefig("rededge.png", dpi=150)
print("\n-> rededge.csv, rededge.png")
