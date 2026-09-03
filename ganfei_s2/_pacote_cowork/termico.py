"""Temperatura de superficie Landsat C2 L2 (ST_B10) por mascara.
Raiz comprometida transpira menos -> coberto mais quente no Verao."""
import json, csv, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
TOK = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/landsat-c2-l2",
                   timeout=60).json()["token"]
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
ALVO = ("saudavel", "manchaW", "zona0")

feats = []
for ano in range(2017, 2027):
    r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
        "collections": ["landsat-c2-l2"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": f"{ano}-06-15T00:00:00Z/{ano}-09-15T23:59:59Z",
        "query": {"eo:cloud_cover": {"lt": 25},
                  "platform": {"in": ["landsat-8", "landsat-9"]}},
        "limit": 100}, timeout=120).json().get("features", [])
    feats += r
print("cenas Landsat de verao, nuvens <25%:", len(feats))

def uma(f):
    try:
        a = f["assets"]
        if "lwir11" not in a: return None
        def rd(k, shape=None):
            href = a[k]["href"] + "?" + TOK
            with rasterio.Env(**E), rasterio.open(href) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                if shape is None:
                    return ds.read(1, window=w, boundless=True, fill_value=0)
                return ds.read(1, window=w, out_shape=shape, boundless=True,
                               fill_value=0, resampling=Resampling.nearest)
        st = rd("lwir11").astype("float32")
        if st.shape[0] < 3: return None
        qa = rd("qa_pixel", st.shape)
        # QA_PIXEL: bit 1 dilated cloud, 3 cloud, 4 cloud shadow
        mau = ((qa >> 1) & 1) | ((qa >> 3) & 1) | ((qa >> 4) & 1)
        st[(st == 0) | (mau > 0)] = np.nan
        st = st * 0.00341802 + 149.0 - 273.15          # -> Celsius
        out = {"data": f["properties"]["datetime"][:10],
               "plataforma": f["properties"].get("platform"),
               "nuvens": round(f["properties"]["eo:cloud_cover"], 1)}
        for nm in ALVO:
            m = mk[nm]
            sy = (np.arange(st.shape[0]) * 100 // st.shape[0])
            sx = (np.arange(st.shape[1]) * 200 // st.shape[1])
            big = st[np.ix_(np.clip((np.arange(100)*st.shape[0])//100, 0, st.shape[0]-1),
                            np.clip((np.arange(200)*st.shape[1])//200, 0, st.shape[1]-1))]
            v = big[m]; v = v[~np.isnan(v)]
            out[f"{nm}_st"] = round(float(v.mean()), 3) if v.size > 20 else ""
            out[f"{nm}_n"] = int(v.size)
        return out
    except Exception as ex:
        return {"data": f["properties"]["datetime"][:10], "erro": str(ex)[:60]}

with ThreadPoolExecutor(max_workers=6) as ex:
    linhas = [x for x in ex.map(uma, feats) if x]
err = [l for l in linhas if "erro" in l]
linhas = [l for l in linhas if "erro" not in l
          and all(l.get(f"{n}_st") not in ("", None) for n in ALVO)]
linhas.sort(key=lambda r: r["data"])
print(f"utilizaveis: {len(linhas)}  (erros {len(err)})")
if err: print("  ex:", err[0]["erro"])
with open("termico.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()), extrasaction="ignore")
    w.writeheader(); w.writerows(linhas)
print(f"\n{'data':11s} {'saudavel':>9s} {'manchaW':>8s} {'dT':>7s} {'zona0':>7s} {'dT':>7s}")
for l in linhas:
    dW = l["manchaW_st"] - l["saudavel_st"]; dZ = l["zona0_st"] - l["saudavel_st"]
    print(f"{l['data']:11s} {l['saudavel_st']:9.2f} {l['manchaW_st']:8.2f} {dW:+7.2f} "
          f"{l['zona0_st']:7.2f} {dZ:+7.2f}")
print("\nmedia de dT por ano:")
anos = {}
for l in linhas: anos.setdefault(l["data"][:4], []).append(l)
for a in sorted(anos):
    g = anos[a]
    print(f"  {a}  n={len(g)}  manchaW {np.mean([x['manchaW_st']-x['saudavel_st'] for x in g]):+.2f} C"
          f"   zona0 {np.mean([x['zona0_st']-x['saudavel_st'] for x in g]):+.2f} C")
