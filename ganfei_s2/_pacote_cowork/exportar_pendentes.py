"""Exporta os resultados que a auditoria marcou como NAO VERIFICAVEIS."""
import json, csv, glob, os, requests, numpy as np, rasterio, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from scipy import ndimage

E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
prov = json.load(open("sentinel/proveniencia.json"))

# ---------- 1. POMARES NOVOS (pilar da hipotese hidraulica) ----------------
W = (528200, 4653800, 532600, 4656200)
anuais = [c for c in prov["cenas"] if c["data"][:4] != "2025" or c["data"] == "2025-08-14"]
def uma(c):
    a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     f"sentinel-2-l2a/items/{c['cena']}", timeout=90).json()["assets"]
    def rd(k, shape=None):
        with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
            w = from_bounds(*W, transform=ds.transform)
            if shape is None: return ds.read(1, window=w).astype("float32")
            return ds.read(1, window=w, out_shape=shape,
                           resampling=Resampling.nearest).astype("float32")
    nir, red = rd("nir"), rd("red"); scl = rd("scl", nir.shape)
    with np.errstate(invalid="ignore", divide="ignore"): nd = (nir-red)/(nir+red)
    nd[np.isin(scl.astype(int), [0,1,3,8,9,10])] = np.nan
    return c["data"][:4], nd
with ThreadPoolExecutor(max_workers=6) as ex: res = dict(ex.map(uma, anuais))
anos = sorted(res); cubo = np.stack([res[a] for a in anos])
cop = cubo > 0.80
novo = ndimage.binary_opening((cop[:4].sum(0) <= 1) & (cop[-4:].sum(0) >= 3), np.ones((3,3)))
lab, n = ndimage.label(novo)
rows = []
for i in range(1, n+1):
    m = lab == i
    if m.sum() < 50: continue
    s = [round(float(np.nanmean(cubo[k][m])), 3) for k in range(len(anos))]
    prim = next((anos[k] for k in range(len(anos))
                 if all(s[j] > 0.78 for j in range(k, min(k+3, len(anos))))), "")
    ys, xs = np.where(m)
    r = {"bloco": len(rows)+1, "ha": round(m.sum()/100, 2), "ano_entrada": prim,
         "UTM_E_min": W[0]+xs.min()*10, "UTM_E_max": W[0]+xs.max()*10,
         "UTM_N_min": W[3]-ys.max()*10, "UTM_N_max": W[3]-ys.min()*10}
    r.update({f"ndvi_{a}": v for a, v in zip(anos, s)})
    rows.append(r)
with open("pendente_pomares_novos.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
tot = sum(r["ha"] for r in rows)
por_ano = {}
for r in rows: por_ano[r["ano_entrada"]] = por_ano.get(r["ano_entrada"], 0) + r["ha"]
print(f"pomares novos: {len(rows)} blocos, {tot:.2f} ha")
for a in sorted(por_ano): print(f"   {a}: {por_ano[a]:.2f} ha")

# ---------- 2. PRECIPITACAO e GEADA (ERA5-Land) ----------------------------
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": 42.047, "longitude": -8.626, "start_date": "2016-09-01",
    "end_date": "2026-08-20", "daily": "precipitation_sum", "timezone": "UTC"},
    timeout=240).json()["daily"]
d = np.array(r["time"], dtype="datetime64[D]")
p = np.array([x if x is not None else np.nan for x in r["precipitation_sum"]], float)
rows = []
for ano in range(2016, 2026):
    m = (d >= np.datetime64(f"{ano}-10-01")) & (d <= np.datetime64(f"{ano+1}-03-31"))
    m2 = (d >= np.datetime64(f"{ano+1}-04-01")) & (d <= np.datetime64(f"{ano+1}-06-15"))
    rows.append({"inverno": f"{ano}-10 a {ano+1}-03",
                 "precip_out_mar_mm": round(float(np.nansum(p[m])), 1),
                 "dias_ge_20mm": int(np.nansum(p[m] >= 20)),
                 "precip_abr_15jun_mm": round(float(np.nansum(p[m2])), 1)})
with open("pendente_precipitacao.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"precipitacao: {len(rows)} invernos")

rows = []
for ano in range(2019, 2027):
    try:
        h = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
            "latitude": 42.047, "longitude": -8.626,
            "start_date": f"{ano}-04-15", "end_date": f"{ano}-05-10",
            "hourly": "temperature_2m,wind_speed_10m,cloud_cover",
            "timezone": "UTC"}, timeout=180).json().get("hourly")
        if not h: continue
        T = np.array(h["time"], dtype="datetime64[h]")
        t = np.array([x if x is not None else np.nan for x in h["temperature_2m"]], float)
        ws = np.array([x if x is not None else np.nan for x in h["wind_speed_10m"]], float)
        cc = np.array([x if x is not None else np.nan for x in h["cloud_cover"]], float)
        sub = (T >= np.datetime64(f"{ano}-04-20")) & (T <= np.datetime64(f"{ano}-05-05T23"))
        i = int(np.nanargmin(t[sub])); idx = np.where(sub)[0][i]
        rows.append({"ano": ano, "min_t2m_20abr_5mai": round(float(np.nanmin(t[sub])), 1),
                     "hora_do_min": str(T[idx]), "vento_ms": round(float(ws[idx]), 1),
                     "nuvens_pct": round(float(cc[idx])),
                     "horas_abaixo_2C": int(np.nansum(t[sub] <= 2)),
                     "horas_abaixo_6C": int(np.nansum(t[sub] <= 6))})
    except Exception: pass
with open("pendente_geada.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"geada: {len(rows)} anos | horas <=2C em 2025: "
      f"{[r['horas_abaixo_2C'] for r in rows if r['ano']==2025]}")
