# -*- coding: utf-8 -*-
"""C2-07 — descarrega a pilha Sentinel-1 RTC de Invernos, CELULA A CELULA.

A C1 (c1_13) leu as mesmas cenas mas guardou so medias por mascara. Para o
cruzamento da C2 e preciso o valor de cada celula em cada cena, porque o teste
que separa o MOMENTO do LUGAR precisa de correr sobre uma particao do pomar que
nao conhece os focos.

Guarda:
  c2_07_sar_pilha.npy   (n_cenas, 100, 200) float32, VV em dB
  c2_07_sar_cenas.json  data, inverno, orbita de cada cena, pela mesma ordem

Nao usa NDVI. Nao usa as coordenadas dos focos.
"""
import json
import os
import sys

import numpy as np
import rasterio
import requests
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import AOI, NL, NC, SAIDA  # noqa

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")
tok = requests.get(
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc",
    timeout=60).json()["token"]

INV = {}
for a in range(2016, 2026):
    INV["%d-%02d" % (a, (a + 1) % 100)] = ("%d-11-01" % a, "%d-03-31" % (a + 1))

feats = []
for inv, (a, b) in INV.items():
    try:
        r = requests.post(
            "https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
                "collections": ["sentinel-1-rtc"],
                "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
                "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (a, b), "limit": 300},
            timeout=180).json().get("features", [])
    except Exception as e:
        print("busca %s falhou: %s" % (inv, e))
        continue
    for f in r:
        f["_inv"] = inv
    feats += r
    print("  %s: %d cenas" % (inv, len(r)))
print("total: %d cenas" % len(feats))


def uma(f):
    try:
        with rasterio.Env(**ENV), \
                rasterio.open(f["assets"]["vv"]["href"] + "?" + tok) as ds:
            a = ds.read(1, window=from_bounds(*AOI, transform=ds.transform),
                        out_shape=(NL, NC),
                        resampling=rasterio.enums.Resampling.average).astype("float64")
        a[a <= 0] = np.nan
        p = f["properties"]
        return (dict(inverno=f["_inv"], data=p["datetime"][:10],
                     orbita=p.get("sat:relative_orbit")),
                (10 * np.log10(a)).astype("float32"))
    except Exception:
        return None


with ThreadPoolExecutor(10) as ex:
    got = [x for x in ex.map(uma, feats) if x is not None]
print("cenas lidas: %d" % len(got))

got.sort(key=lambda t: (t[0]["data"], t[0]["orbita"] or 0))
meta = [t[0] for t in got]
pilha = np.stack([t[1] for t in got])
np.save(os.path.join(SAIDA, "c2_07_sar_pilha.npy"), pilha)
json.dump(meta, open(os.path.join(SAIDA, "c2_07_sar_cenas.json"), "w",
                     encoding="utf-8"), ensure_ascii=False, indent=1)
print("pilha %s guardada" % (pilha.shape,))
for inv in sorted(set(m["inverno"] for m in meta)):
    sub = [m for m in meta if m["inverno"] == inv]
    print("  %s: %d cenas, orbitas %s"
          % (inv, len(sub), sorted(set(m["orbita"] for m in sub))))
