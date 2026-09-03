# -*- coding: utf-8 -*-
"""C1-09 — Sentinel-1 RTC re-executado com as mascaras GEOGRAFICAS.

Porque se refaz: `sar_invernos.csv` usou `masks.json`. Nessas, `manchaW` era
`pomar & (nd2026 < 0,76)` dilatada e `saudavel` foi escolhida por NDVI alto na
ultima cena — as duas sao circulares em relacao ao sinal optico. Um contraste
de retrodifusao medido sobre uma mascara desenhada pelo NDVI nao e um
instrumento independente; e o mesmo instrumento outra vez.

Aqui as unidades sao: referencia sistematica (110 celulas, rede regular),
discos geometricos de 90 m nos dois focos (R2 G34), o poligono `zona0` e o
chao lavrado de 2021. Nenhuma delas usa NDVI.

Orbitas tratadas em separado — misturar geometrias de vista invalida a
comparacao de gamma0.
"""
import os, sys, json, csv
import numpy as np
import requests, rasterio
from rasterio.windows import from_bounds
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
masc, _ = carrega_mascaras()
pomar, saud, zona0, nu2021 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(pomar)
ALVO = {"referencia": saud, "foco_oeste": do, "foco_este": de,
        "zona0_poligono": zona0, "nu2021": nu2021 & pomar, "pomar": pomar}
for k, v in ALVO.items():
    print("%-16s %5d celulas = %.2f ha" % (k, v.sum(), v.sum() / 100))

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
        "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (a, b), "limit": 200},
        timeout=180).json()["features"]
    for f in r:
        f["_inv"] = inv
    feats += r
print("\ncenas Sentinel-1 RTC: %d" % len(feats))


def uma(f):
    try:
        out = {}
        for pol in ("vv", "vh"):
            if pol not in f["assets"]:
                return None
            with rasterio.Env(**ENV), rasterio.open(f["assets"][pol]["href"] + "?" + tok) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                a = ds.read(1, window=w, out_shape=(NL, NC),
                            resampling=rasterio.enums.Resampling.average).astype("float64")
            a[a <= 0] = np.nan
            out[pol] = 10 * np.log10(a)
        p = f["properties"]
        lin = dict(inverno=f["_inv"], data=p["datetime"][:10],
                   orbita=p.get("sat:relative_orbit"),
                   passagem=p.get("sat:orbit_state", "")[:10])
        for nome, m in ALVO.items():
            for pol in ("vv", "vh"):
                v = out[pol][m]
                lin["%s_%s_db" % (nome, pol)] = round(float(np.nanmean(v)), 4)
        return lin
    except Exception:
        return None


with ThreadPoolExecutor(8) as ex:
    linhas = [x for x in ex.map(uma, feats) if x]
linhas.sort(key=lambda r: (r["data"], r["orbita"]))
print("cenas lidas com sucesso: %d" % len(linhas))

cols = list(linhas[0].keys())
with open(os.path.join(SAIDA, "c1_09_sar_geografico.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(linhas)

# ---------- analise ----------
from scipy import stats
orb = np.array([r["orbita"] for r in linhas])
inv = np.array([r["inverno"] for r in linhas])
G = {k: {p: np.array([r["%s_%s_db" % (k, p)] for r in linhas]) for p in ("vv", "vh")}
     for k in ALVO}

print("\n=== gamma0 medio por unidade, por orbita (dB) ===")
print("%-16s %6s %5s %9s %9s %11s %11s" % ("unidade", "orbita", "n", "VV", "VH", "VV-ref", "VH-ref"))
res = {}
for o in sorted(set(orb)):
    m = orb == o
    for k in ("referencia", "foco_oeste", "foco_este", "zona0_poligono", "nu2021", "pomar"):
        dvv = G[k]["vv"][m] - G["referencia"]["vv"][m]
        dvh = G[k]["vh"][m] - G["referencia"]["vh"][m]
        print("%-16s %6d %5d %9.3f %9.3f %+11.3f %+11.3f"
              % (k, o, m.sum(), np.nanmean(G[k]["vv"][m]), np.nanmean(G[k]["vh"][m]),
                 np.nanmean(dvv), np.nanmean(dvh)))
        res.setdefault(k, {})[int(o)] = dict(
            vv=float(np.nanmean(G[k]["vv"][m])), vh=float(np.nanmean(G[k]["vh"][m])),
            d_vv=float(np.nanmean(dvv)), d_vh=float(np.nanmean(dvh)),
            d_vv_dp=float(np.nanstd(dvv)), n=int(m.sum()))
    print()

print("=== teste: cada foco contra a referencia, emparelhado por cena ===")
for o in sorted(set(orb)):
    m = orb == o
    for k in ("foco_oeste", "foco_este", "zona0_poligono", "nu2021"):
        d = G[k]["vv"][m] - G["referencia"]["vv"][m]
        d = d[~np.isnan(d)]
        t, p = stats.wilcoxon(d)
        print("  orbita %d  %-16s dVV mediana %+.3f dB  n=%d  Wilcoxon p=%.1e  | sinal constante em %d%% das cenas"
              % (o, k, np.median(d), len(d), p, round(100 * max((d < 0).mean(), (d > 0).mean()))))
    print()

print("=== estabilidade entre Invernos (dVV do foco ESTE contra a referencia) ===")
for o in sorted(set(orb)):
    for i in sorted(set(inv)):
        m = (orb == o) & (inv == i)
        if m.sum() < 3:
            continue
        d = G["foco_este"]["vv"][m] - G["referencia"]["vv"][m]
        d2 = G["foco_oeste"]["vv"][m] - G["referencia"]["vv"][m]
        print("  orbita %d  %s  n=%2d  ESTE %+.3f dB | OESTE %+.3f dB"
              % (o, i, m.sum(), np.nanmean(d), np.nanmean(d2)))

json.dump(res, open(os.path.join(SAIDA, "c1_09_sar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_09_sar_geografico.csv e c1_09_sar.json")
