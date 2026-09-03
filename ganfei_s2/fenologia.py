"""Atraso fenologico na Primavera, por mascara, 2018-2026.
Solo encharcado aquece devagar e atrasa o abrolhamento/fecho do coberto."""
import json, csv, requests, numpy as np, datetime as dt
from concurrent.futures import ThreadPoolExecutor
import rasterio
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
ALVO = ("saudavel", "manchaW", "zona0")

feats = []
for ano in range(2018, 2027):
    r = requests.post("https://earth-search.aws.element84.com/v1/search", json={
        "collections": ["sentinel-2-l2a"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": f"{ano}-02-15T00:00:00Z/{ano}-07-20T23:59:59Z",
        "query": {"eo:cloud_cover": {"lt": 35}}, "limit": 300}, timeout=120).json()["features"]
    feats += [f for f in r if all(f["assets"].get(k, {}).get("href", "").startswith("https://")
                                  for k in ("red", "nir", "scl"))]
print("cenas de Primavera:", len(feats))

def uma(f):
    try:
        a = f["assets"]
        def rd(k, shape=None):
            with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                if shape is None: return ds.read(1, window=w).astype("float32")
                return ds.read(1, window=w, out_shape=shape,
                               resampling=Resampling.nearest).astype("float32")
        red = rd("red"); nir = rd("nir"); scl = rd("scl", red.shape)
        if red.shape != (100, 200): return None
        bom = ~np.isin(scl, [0, 1, 3, 8, 9, 10])
        with np.errstate(invalid="ignore", divide="ignore"):
            nd = (nir - red) / (nir + red)
        out = {"data": f["properties"]["datetime"][:10]}
        for nm in ALVO:
            m = mk[nm] & bom
            out[nm] = round(float(np.nanmean(nd[m])), 4) if m.sum() > 0.6*mk[nm].sum() else ""
        return out
    except Exception:
        return None

with ThreadPoolExecutor(max_workers=8) as ex:
    linhas = [x for x in ex.map(uma, feats) if x and x.get("manchaW") != ""]
linhas.sort(key=lambda r: r["data"])
print("utilizaveis:", len(linhas))
with open("fenologia.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["data"] + list(ALVO), extrasaction="ignore")
    w.writeheader(); w.writerows(linhas)

def doy(s): 
    d = dt.date.fromisoformat(s); return d.timetuple().tm_yday
print(f"\n{'ano':5s} " + "".join(f"{n+' (dia)':>16s}" for n in ALVO) +
      f"{'atraso W':>10s}{'atraso Z':>10s}")
res = {}
for ano in range(2018, 2027):
    g = [l for l in linhas if l["data"][:4] == str(ano)]
    if len(g) < 8: continue
    row = {}
    for nm in ALVO:
        d = np.array([doy(l["data"]) for l in g if l[nm] != ""])
        v = np.array([float(l[nm]) for l in g if l[nm] != ""])
        if v.size < 8: continue
        base = np.percentile(v[d < 90], 50) if (d < 90).any() else v.min()
        topo = np.percentile(v[d > 160], 50) if (d > 160).any() else v.max()
        alvo = base + 0.5*(topo - base)
        cruz = None
        for i in range(1, len(d)):
            if v[i-1] < alvo <= v[i]:
                cruz = d[i-1] + (alvo - v[i-1])/(v[i] - v[i-1])*(d[i] - d[i-1]); break
        row[nm] = cruz
    if len(row) == 3 and all(v is not None for v in row.values()):
        res[ano] = row
        print(f"{ano:5d} " + "".join(f"{row[n]:16.1f}" for n in ALVO) +
              f"{row['manchaW']-row['saudavel']:+10.1f}{row['zona0']-row['saudavel']:+10.1f}")
fig, ax = plt.subplots(figsize=(11, 6))
for nm, c in (("saudavel","#2f6e26"), ("manchaW","#C2451E"), ("zona0","#E4A11B")):
    ax.plot(list(res), [res[a][nm] for a in res], "-o", color=c, lw=2, label=nm)
ax.set_ylabel("dia do ano em que o NDVI cruza 50% da amplitude")
ax.set_xlabel("ano"); ax.grid(alpha=.25); ax.legend(frameon=False)
ax.set_title("Ganfei — data de fecho do coberto por mascara")
fig.tight_layout(); fig.savefig("fenologia.png", dpi=150)
print("\n-> fenologia.csv, fenologia.png")
