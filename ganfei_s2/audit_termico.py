"""Testes (a) e (b) da auditoria adversarial.
(a) A referencia sa aqueceu em 2025? LST absoluta controlada por temperatura
    do ar a hora da passagem e por um controlo externo estavel.
(b) O aquecimento sobrevive a cobertura constante? Regressao dT x dNDVI da
    MESMA cena Landsat (nao do Sentinel, para nao misturar datas)."""
import json, csv, requests, numpy as np, rasterio, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib.path import Path as MP
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
TOK = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/landsat-c2-l2",
                   timeout=60).json()["token"]
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
# controlo externo: terreno agricola fora do pomar, >100 m dele, vegetado em 2026
with rasterio.open("sentinel/2026-07-27.tif") as ds: nd26 = ds.read(1)
fora = ~ndimage.binary_dilation(mk["pomar"], np.ones((21, 21)))
ctrl = fora & (nd26 > 0.55) & (nd26 < 0.88)
print(f"controlo externo: {ctrl.sum()/100:.2f} ha")

feats = []
for ano in range(2017, 2027):
    r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
        "collections": ["landsat-c2-l2"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": f"{ano}-04-01T00:00:00Z/{ano}-09-30T23:59:59Z",
        "query": {"eo:cloud_cover": {"lt": 25},
                  "platform": {"in": ["landsat-8", "landsat-9"]}},
        "limit": 100}, timeout=120).json().get("features", [])
    feats += r
print("cenas Landsat Abr-Set 2017-2026:", len(feats))

def uma(f):
    try:
        a = f["assets"]
        if not all(k in a for k in ("lwir11", "qa_pixel", "red", "nir08")): return None
        def rd(k, shape=None):
            with rasterio.Env(**E), rasterio.open(a[k]["href"] + "?" + TOK) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                if shape is None:
                    return ds.read(1, window=w, boundless=True, fill_value=0)
                return ds.read(1, window=w, out_shape=shape, boundless=True,
                               fill_value=0, resampling=Resampling.nearest)
        st = rd("lwir11").astype("float32")
        if st.shape[0] < 3: return None
        qa = rd("qa_pixel", st.shape)
        red = rd("red", st.shape).astype("float32")
        nir = rd("nir08", st.shape).astype("float32")
        mau = ((qa >> 1) & 1) | ((qa >> 3) & 1) | ((qa >> 4) & 1)
        bad = (st == 0) | (mau > 0)
        st = st * 0.00341802 + 149.0 - 273.15
        red = red * 2.75e-5 - 0.2; nir = nir * 2.75e-5 - 0.2
        with np.errstate(invalid="ignore", divide="ignore"):
            nd = (nir - red) / (nir + red)
        st[bad] = np.nan; nd[bad] = np.nan
        big = lambda A: A[np.ix_(np.clip((np.arange(100)*A.shape[0])//100, 0, A.shape[0]-1),
                                np.clip((np.arange(200)*A.shape[1])//200, 0, A.shape[1]-1))]
        ST, ND = big(st), big(nd)
        out = {"data": f["properties"]["datetime"][:10],
               "hora_utc": f["properties"]["datetime"][11:16],
               "nuvens": round(f["properties"]["eo:cloud_cover"], 1)}
        for nm, m in (("saudavel", sau), ("manchaW", mk["manchaW"]),
                      ("zona0", mk["zona0"]), ("controlo", ctrl)):
            v = ST[m]; v = v[~np.isnan(v)]
            w = ND[m]; w = w[~np.isnan(w)]
            out[f"{nm}_st"] = round(float(v.mean()), 3) if v.size > 20 else ""
            out[f"{nm}_ndvi"] = round(float(w.mean()), 4) if w.size > 20 else ""
        return out
    except Exception:
        return None

with ThreadPoolExecutor(max_workers=6) as ex:
    L = [x for x in ex.map(uma, feats) if x and x["saudavel_st"] != "" and x["controlo_st"] != ""]
L.sort(key=lambda r: r["data"])
print(f"cenas utilizaveis: {len(L)}")

# guardar antes de qualquer coisa que possa falhar
with open("audit_termico.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
print("-> audit_termico.csv (sem t_ar)")

# temperatura do ar a hora da passagem (ERA5-Land), ano a ano
tar = {}
for ano in range(2017, 2027):
    try:
        r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
            "latitude": 42.047, "longitude": -8.626,
            "start_date": f"{ano}-04-01", "end_date": f"{ano}-09-30",
            "hourly": "temperature_2m", "timezone": "UTC"}, timeout=180).json()
        h = r.get("hourly")
        if not h: print(f"  {ano}: sem dados ({str(r)[:80]})"); continue
        tar.update({t[:13]: v for t, v in zip(h["time"], h["temperature_2m"]) if v is not None})
    except Exception as e:
        print(f"  {ano}: {str(e)[:60]}")
print(f"horas de t_ar obtidas: {len(tar)}")
for x in L:
    h = f"{x['data']}T{x['hora_utc'][:2]}"
    x["t_ar"] = tar.get(h, "")
with open("audit_termico.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
print("-> audit_termico.csv")
