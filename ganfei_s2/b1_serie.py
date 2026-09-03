"""Serie NDVI sobre o lobulo oeste (candidato a B1), MESMAS cenas da serie
principal — os IDs vem do proveniencia.json, para a referencia sa ser comparavel."""
import json, csv, os, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

AOI_B1 = (528400, 4654900, 529400, 4655700)          # 1000 x 800 m
OUT = "sentinel_b1"; os.makedirs(OUT, exist_ok=True)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
         GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="2")
prov = json.load(open("sentinel/proveniencia.json"))
alvo = [(c["data"], c["cena"]) for c in prov["cenas"]]
print(f"{len(alvo)} cenas da serie principal a reutilizar")

def uma(par):
    data, cid = par
    r = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     f"sentinel-2-l2a/items/{cid}", timeout=90).json()
    a = r["assets"]
    def rd(k, shape=None):
        with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
            w = from_bounds(*AOI_B1, transform=ds.transform)
            if shape is None:
                arr = ds.read(1, window=w); return arr, ds.window_transform(w), ds.crs
            return ds.read(1, window=w, out_shape=shape, resampling=Resampling.nearest), None, None
    red, tr, crs = rd("red"); nir, _, _ = rd("nir")
    scl, _, _ = rd("scl", red.shape)
    red = red.astype("float32"); nir = nir.astype("float32")
    with np.errstate(invalid="ignore", divide="ignore"):
        nd = (nir - red) / (nir + red)
    mau = np.isin(scl, [0, 1, 3, 8, 9, 10])
    nd[mau] = np.nan
    with rasterio.open(f"{OUT}/{data}.tif", "w", driver="GTiff", height=nd.shape[0],
                       width=nd.shape[1], count=1, dtype="float32", crs=crs,
                       transform=tr, nodata=np.nan, compress="deflate") as o:
        o.write(nd, 1)
    return data, cid, float(mau.mean()*100), nd.shape

with ThreadPoolExecutor(max_workers=6) as ex:
    res = sorted(ex.map(uma, alvo))
for d, c, m, s in res:
    print(f"  {d}  {c}  mascarado={m:.2f}%  {s}")
json.dump({"aoi_b1": AOI_B1, "cenas": [{"data": d, "cena": c} for d, c, _, _ in res]},
          open(f"{OUT}/proveniencia_b1.json", "w"), indent=2)
print(f"-> {OUT}/")
