# -*- coding: utf-8 -*-
"""C1-12 — o chao lavrado de 2021 tem assinatura de radar propria, ou e so o
foco ESTE outra vez?

`nu2021` esta 60 % dentro do disco do foco ESTE. Sem separar as duas coisas, o
deficit de -1,7 a -2,0 dB de C1-09 podia ser inteiramente o foco. Aqui as
unidades sao disjuntas:
   ESTE lavrado      = disco ESTE  &  nu2021
   ESTE nao lavrado  = disco ESTE  & ~nu2021
   lavrado fora      = nu2021      & ~disco ESTE
"""
import os, sys, json, csv
import numpy as np
import requests, rasterio
from rasterio.windows import from_bounds
from concurrent.futures import ThreadPoolExecutor
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
masc, _ = carrega_mascaras()
pomar, saud, nu = masc["pomar"], masc["saudavel"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(pomar)
ALVO = {"referencia": saud,
        "este_lavrado": de & nu, "este_nao_lavrado": de & ~nu,
        "lavrado_fora_do_este": nu & ~de, "oeste": do}
for k, v in ALVO.items():
    print("%-22s %4d celulas = %.2f ha" % (k, v.sum(), v.sum() / 100))

tok = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc",
                   timeout=60).json()["token"]
INV = {"2022-23": ("2022-11-01", "2023-03-31"), "2023-24": ("2023-11-01", "2024-03-31"),
       "2024-25": ("2024-11-01", "2025-03-31")}
feats = []
for inv, (a, b) in INV.items():
    r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
        "collections": ["sentinel-1-rtc"],
        "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
        "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (a, b), "limit": 200},
        timeout=180).json()["features"]
    for f in r:
        f["_inv"] = inv
    feats += r


def uma(f):
    try:
        with rasterio.Env(**ENV), rasterio.open(f["assets"]["vv"]["href"] + "?" + tok) as ds:
            a = ds.read(1, window=from_bounds(*AOI, transform=ds.transform),
                        out_shape=(NL, NC),
                        resampling=rasterio.enums.Resampling.average).astype("float64")
        a[a <= 0] = np.nan
        db = 10 * np.log10(a)
        p = f["properties"]
        lin = dict(inverno=f["_inv"], data=p["datetime"][:10], orbita=p.get("sat:relative_orbit"))
        for nome, m in ALVO.items():
            lin[nome] = round(float(np.nanmean(db[m])), 4)
        return lin
    except Exception:
        return None


with ThreadPoolExecutor(8) as ex:
    L = [x for x in ex.map(uma, feats) if x]
L.sort(key=lambda r: (r["data"], r["orbita"]))
print("\ncenas lidas: %d" % len(L))
with open(os.path.join(SAIDA, "c1_12_sar_lavrado.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)

orb = np.array([r["orbita"] for r in L])
V = {k: np.array([r[k] for r in L]) for k in ALVO}
print("\n=== VV em relacao a referencia sistematica (dB), por orbita ===")
res = {}
for o in sorted(set(orb)):
    m = orb == o
    print("  orbita %d (n=%d)" % (o, m.sum()))
    for k in ("este_lavrado", "este_nao_lavrado", "lavrado_fora_do_este", "oeste"):
        d = (V[k] - V["referencia"])[m]
        d = d[~np.isnan(d)]
        p = stats.wilcoxon(d)[1]
        print("    %-22s %+7.3f dB  p=%.1e" % (k, np.median(d), p))
        res.setdefault(k, {})[int(o)] = dict(d_vv=float(np.median(d)), p=float(p), n=int(len(d)))
    # o lavrado contra o nao lavrado DENTRO do foco ESTE
    d = (V["este_lavrado"] - V["este_nao_lavrado"])[m]
    d = d[~np.isnan(d)]
    print("    %-22s %+7.3f dB  p=%.1e   <- separa lavrado de foco"
          % ("lavrado - nao lavrado", np.median(d), stats.wilcoxon(d)[1]))
    res.setdefault("lavrado_menos_nao_lavrado", {})[int(o)] = dict(
        d_vv=float(np.median(d)), p=float(stats.wilcoxon(d)[1]))

print("\n=== o lavrado FORA do foco ESTE contra a referencia (teste decisivo) ===")
print("Se o chao lavrado de 2021 baixa a retrodifusao mesmo onde NAO ha foco,")
print("a assinatura e do trabalho de solo e nao do declinio.")
for o in sorted(set(orb)):
    m = orb == o
    d = (V["lavrado_fora_do_este"] - V["referencia"])[m]
    d = d[~np.isnan(d)]
    print("  orbita %d: %+.3f dB  p=%.1e  (n=%d)" % (o, np.median(d), stats.wilcoxon(d)[1], len(d)))

json.dump(res, open(os.path.join(SAIDA, "c1_12_sar_lavrado.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_12_sar_lavrado.csv/.json")
