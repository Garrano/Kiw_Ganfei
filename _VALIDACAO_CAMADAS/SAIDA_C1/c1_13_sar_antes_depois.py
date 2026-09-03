# -*- coding: utf-8 -*-
"""C1-13 — a assinatura de radar do chao lavrado ja la estava antes de 2021?

C1-12 mostra que o chao que aparece lavrado na ortofoto de 2021 tem, nos
Invernos de 2022-23 a 2024-25, VV entre 1,7 e 2,9 dB abaixo da referencia
sistematica, e que isso acontece tambem fora do foco ESTE.

Falta datar. Sentinel-1 cobre desde 2014. Se o deficit estiver ausente nos
Invernos anteriores a 2021 e presente depois, a alteracao data-se; se estiver
la desde 2017, o solo nu de 2021 e sintoma de algo mais antigo e nao a causa.

Mesma orbita, mesma mascara, mesma estatistica. Nada aqui usa NDVI.
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
ALVO = {"referencia": saud, "lavrado2021": nu, "lavrado_fora_do_este": nu & ~de,
        "este_nao_lavrado": de & ~nu, "oeste": do, "pomar": pomar}

tok = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc",
                   timeout=60).json()["token"]
INV = {}
for a in range(2016, 2026):
    INV["%d-%02d" % (a, (a + 1) % 100)] = ("%d-11-01" % a, "%d-03-31" % (a + 1))
feats = []
for inv, (a, b) in INV.items():
    try:
        r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
            "collections": ["sentinel-1-rtc"],
            "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
            "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (a, b), "limit": 300},
            timeout=180).json().get("features", [])
    except Exception as e:
        print("busca %s falhou: %s" % (inv, e)); continue
    for f in r:
        f["_inv"] = inv
    feats += r
    print("  %s: %d cenas" % (inv, len(r)))
print("total: %d cenas" % len(feats))


def uma(f):
    try:
        with rasterio.Env(**ENV), rasterio.open(f["assets"]["vv"]["href"] + "?" + tok) as ds:
            a = ds.read(1, window=from_bounds(*AOI, transform=ds.transform), out_shape=(NL, NC),
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


with ThreadPoolExecutor(10) as ex:
    L = [x for x in ex.map(uma, feats) if x]
L.sort(key=lambda r: (r["data"], r["orbita"]))
print("cenas lidas: %d" % len(L))
with open(os.path.join(SAIDA, "c1_13_sar_serie.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)

orb = np.array([r["orbita"] for r in L])
inv = np.array([r["inverno"] for r in L])
V = {k: np.array([r[k] for r in L]) for k in ALVO}
invs = sorted(set(inv))

print("\n=== dVV contra a referencia sistematica, Inverno a Inverno (dB) ===")
print("A ortofoto que mostra o solo lavrado e de 2021. Os Invernos <= 2020-21")
print("sao ANTES; 2021-22 em diante sao DEPOIS.")
res = {}
for o in sorted(set(orb)):
    print("\n  --- orbita %d ---" % o)
    print("  %-9s %4s %14s %22s %18s %9s" % ("inverno", "n", "lavrado2021", "lavrado_fora_do_este",
                                              "este_nao_lavrado", "oeste"))
    for i in invs:
        m = (orb == o) & (inv == i)
        if m.sum() < 3:
            continue
        vals = []
        for k in ("lavrado2021", "lavrado_fora_do_este", "este_nao_lavrado", "oeste"):
            d = (V[k] - V["referencia"])[m]
            vals.append(np.nanmedian(d))
            res.setdefault(k, {}).setdefault(int(o), {})[i] = float(np.nanmedian(d))
        print("  %-9s %4d %14.3f %22.3f %18.3f %9.3f" % (i, m.sum(), *vals))

print("\n=== antes (ate 2020-21) contra depois (2021-22 em diante) ===")
antes = np.isin(inv, [i for i in invs if int(i[:4]) <= 2020])
dep = ~antes
for o in sorted(set(orb)):
    print("  orbita %d: n(antes)=%d  n(depois)=%d" % (o, ((orb == o) & antes).sum(),
                                                      ((orb == o) & dep).sum()))
    for k in ("lavrado2021", "lavrado_fora_do_este", "este_nao_lavrado", "oeste"):
        a = (V[k] - V["referencia"])[(orb == o) & antes]
        b = (V[k] - V["referencia"])[(orb == o) & dep]
        a, b = a[~np.isnan(a)], b[~np.isnan(b)]
        if len(a) < 5 or len(b) < 5:
            print("    %-22s dados insuficientes" % k); continue
        p = stats.mannwhitneyu(a, b, alternative="two-sided")[1]
        print("    %-22s antes %+7.3f | depois %+7.3f | variacao %+7.3f dB | p=%.1e"
              % (k, np.median(a), np.median(b), np.median(b) - np.median(a), p))

json.dump(res, open(os.path.join(SAIDA, "c1_13_sar_serie.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_13_sar_serie.csv/.json")
