"""Serie densa Jul2023-Jun2025 sobre a AOI: NDVI, NDMI (humidade) e BSI (solo nu)
nas mascaras manchaW / zona0 / saudavel. Objectivo: datar e caracterizar o que
mudou no sector W entre Jul/2024 e Jun/2025."""
import json, csv, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
         GDAL_HTTP_MAX_RETRY="2", GDAL_HTTP_RETRY_DELAY="1")
masks_px = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks_px.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
ALVO = {"manchaW": mk["manchaW"], "zona0": mk["zona0"], "saudavel": sau}

feats = []
for a, b in (("2023-07-01", "2024-06-30"), ("2024-07-01", "2025-06-30")):
    r = requests.post("https://earth-search.aws.element84.com/v1/search", json={
        "collections": ["sentinel-2-l2a"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": f"{a}T00:00:00Z/{b}T23:59:59Z",
        "query": {"eo:cloud_cover": {"lt": 30}}, "limit": 200}, timeout=120).json()["features"]
    feats += r
feats = [f for f in feats if all(f["assets"].get(k, {}).get("href", "").startswith("https://")
                                 for k in ("red", "nir", "blue", "swir16", "scl"))]
print("cenas utilizaveis:", len(feats))

def ler(href, shape=None):
    with rasterio.Env(**E), rasterio.open(href) as ds:
        w = from_bounds(*AOI, transform=ds.transform)
        if shape is None:
            return ds.read(1, window=w).astype("float32")
        return ds.read(1, window=w, out_shape=shape, resampling=Resampling.nearest).astype("float32")

def uma(f):
    try:
        a = f["assets"]
        red = ler(a["red"]["href"]); nir = ler(a["nir"]["href"]); blue = ler(a["blue"]["href"])
        swir = ler(a["swir16"]["href"], red.shape)
        scl = ler(a["scl"]["href"], red.shape)
        bom = ~np.isin(scl, [0, 1, 3, 8, 9, 10])
        with np.errstate(invalid="ignore", divide="ignore"):
            ndvi = (nir - red) / (nir + red)
            ndmi = (nir - swir) / (nir + swir)
            bsi = ((swir + red) - (nir + blue)) / ((swir + red) + (nir + blue))
        out = {"data": f["properties"]["datetime"][:10],
               "nuvens": round(f["properties"]["eo:cloud_cover"], 1)}
        for nm, m in ALVO.items():
            v = m & bom
            cob = v.sum() / m.sum()
            out[f"{nm}_cobertura"] = round(float(cob), 2)
            if cob < 0.6:
                for i in ("ndvi", "ndmi", "bsi"): out[f"{nm}_{i}"] = ""
                continue
            for i, arr in (("ndvi", ndvi), ("ndmi", ndmi), ("bsi", bsi)):
                out[f"{nm}_{i}"] = round(float(np.nanmean(arr[v])), 4)
        return out
    except Exception as ex:
        return {"data": f["properties"]["datetime"][:10], "nuvens": -1, "erro": str(ex)[:60]}

with ThreadPoolExecutor(max_workers=8) as ex:
    linhas = list(ex.map(uma, feats))
linhas = [l for l in linhas if "erro" not in l]
linhas.sort(key=lambda r: r["data"])
campos = ["data", "nuvens"] + [f"{n}_{s}" for n in ALVO for s in ("cobertura", "ndvi", "ndmi", "bsi")]
with open("serie_densa_W.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
    w.writeheader(); w.writerows(linhas)
uteis = [l for l in linhas if l.get("manchaW_ndvi") != ""]
print(f"{len(linhas)} cenas lidas, {len(uteis)} com >=60% da manchaW valida")
print("-> serie_densa_W.csv")
