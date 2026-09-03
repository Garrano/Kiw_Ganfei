"""Sentinel-1 RTC (gamma0 corrigido de terreno) nos tres Invernos.
Testa a hipotese de encharcamento no sector W, que o optico nao consegue separar.
Orbitas tratadas em SEPARADO — misturar geometrias invalida a comparacao."""
import json, csv, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
ALVO = {"saudavel": sau, "manchaW": mk["manchaW"], "zona0": mk["zona0"]}

tok = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc",
                   timeout=60).json()["token"]

INV = {"2022-23": ("2022-11-01", "2023-03-31"),
       "2023-24": ("2023-11-01", "2024-03-31"),
       "2024-25": ("2024-11-01", "2025-03-31")}
feats = []
for inv, (a, b) in INV.items():
    r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
        "collections": ["sentinel-1-rtc"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": f"{a}T00:00:00Z/{b}T23:59:59Z", "limit": 200}, timeout=120).json()["features"]
    for f in r: f["_inv"] = inv
    feats += r
print("cenas RTC:", len(feats))

def uma(f):
    try:
        p = f["properties"]
        out = {"inverno": f["_inv"], "data": p["datetime"][:10],
               "orbita": p.get("sat:relative_orbit"), "passagem": p.get("sat:orbit_state")}
        band = {}
        for pol in ("vv", "vh"):
            href = f["assets"][pol]["href"] + "?" + tok
            with rasterio.Env(**E), rasterio.open(href) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                arr = ds.read(1, window=w, boundless=True, fill_value=np.nan).astype("float32")
            arr[arr <= 0] = np.nan
            band[pol] = 10 * np.log10(arr)
        if band["vv"].shape != (100, 200):
            out["erro"] = f"forma {band['vv'].shape}"; return out
        for nm, m in ALVO.items():
            for pol in ("vv", "vh"):
                v = band[pol][m]; v = v[~np.isnan(v)]
                out[f"{nm}_{pol}_db"] = round(float(v.mean()), 3) if v.size else ""
        return out
    except Exception as ex:
        return {"inverno": f["_inv"], "data": f["properties"]["datetime"][:10],
                "erro": str(ex)[:70]}

with ThreadPoolExecutor(max_workers=6) as ex:
    linhas = list(ex.map(uma, feats))
erros = [l for l in linhas if "erro" in l]
linhas = [l for l in linhas if "erro" not in l and l.get("manchaW_vv_db") != ""]
print(f"lidas {len(linhas)}, erros {len(erros)}")
if erros: print("  ex:", erros[0].get("erro"))
linhas.sort(key=lambda r: r["data"])
campos = ["inverno", "data", "orbita", "passagem"] + \
         [f"{n}_{p}_db" for n in ALVO for p in ("vv", "vh")]
with open("sar_invernos.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
    w.writeheader(); w.writerows(linhas)

print(f"\n{'inverno':9s} {'orbita':>7s} {'n':>3s} "
      f"{'dVV manchaW-sa':>15s} {'dVH manchaW-sa':>15s} {'dVV zona0-sa':>13s}")
for inv in INV:
    for orb in sorted({l["orbita"] for l in linhas}):
        sub = [l for l in linhas if l["inverno"] == inv and l["orbita"] == orb]
        if not sub: continue
        dvv = np.mean([l["manchaW_vv_db"] - l["saudavel_vv_db"] for l in sub])
        dvh = np.mean([l["manchaW_vh_db"] - l["saudavel_vh_db"] for l in sub])
        dz = np.mean([l["zona0_vv_db"] - l["saudavel_vv_db"] for l in sub])
        print(f"{inv:9s} {orb:7d} {len(sub):3d} {dvv:+15.3f} {dvh:+15.3f} {dz:+13.3f}")
print("\n-> sar_invernos.csv")
