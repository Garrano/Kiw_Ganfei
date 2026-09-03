# -*- coding: utf-8 -*-
"""Amplitude sazonal — a forma da curva separa declinio de arranque.

A pergunta do gestor: dar as imagens mais recentes ao longo dos meses de
expressao vegetativa para confirmar se e declinio ou remocao.

O discriminante nao e o NIVEL, e a FORMA:

  videira viva em declinio   abre em Maio e fecha mal. Ha amplitude entre o
                             piso de Inverno e o pico de Verao; o pico e que
                             esta baixo.
  videira arrancada          nao abre. Erva ou solo o ano inteiro: curva
                             achatada, amplitude pequena, e o piso de Inverno
                             sobe em vez de descer.

Corre-se sobre os nucleos do analista B, pelas coordenadas que ele publica,
porque a mascara do foco ESTE desta sessao nao cobre o N3 — esta a 95 m, fora
do disco, e foi por isso que a serie densa desta sessao nao viu a queda de
dezoito dias que ele viu.
"""
import json
import os
import sys

import numpy as np
import rasterio
import requests
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.windows import from_bounds

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
d26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)


def disco(x, y, r=70.0):
    yy, xx = np.mgrid[:NL, :NC]
    return np.hypot(AOI[0] + (xx + .5) * PASSO - x,
                    AOI[3] - (yy + .5) * PASSO - y) <= r


UN = [("N1 oeste", disco(530476, 4655046) & POMAR),
      ("N2 leste", disco(530895, 4655052) & POMAR),
      ("N3 leste", disco(531068, 4655145) & POMAR),
      ("referencia", REF),
      ("resto do pomar", POMAR & ~d26 & ~REF)]
for n, m in UN:
    print("%-16s %5.2f ha" % (n, m.sum() / 100.0))

tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1]); lo2, la2 = tr.transform(AOI[2], AOI[3])
por_data = {}
for ano in range(2022, 2027):
    for m0 in range(1, 13):
        m1 = m0 % 12 + 1
        a1 = ano + (1 if m1 == 1 else 0)
        try:
            r = requests.post(
                "https://earth-search.aws.element84.com/v1/search",
                json={"collections": ["sentinel-2-l2a"], "bbox": [lo, la, lo2, la2],
                      "datetime": "%d-%02d-01T00:00:00Z/%d-%02d-01T00:00:00Z"
                                  % (ano, m0, a1, m1),
                      "query": {"eo:cloud_cover": {"lt": 30}}, "limit": 100},
                timeout=120).json()
        except Exception:
            continue
        for x in r.get("features", []):
            por_data.setdefault(x["properties"]["datetime"][:10], x["assets"])
cenas = sorted(por_data.items())
print("\ncenas 2022-2026 com nuvem <30%%: %d" % len(cenas))

reg = []
for k, (dt, a) in enumerate(cenas):
    try:
        def rd(b, **kw):
            with rasterio.Env(**ENV), rasterio.open(a[b]["href"]) as ds:
                return ds.read(1, window=from_bounds(*AOI, transform=ds.transform), **kw)
        red = rd("red").astype("float32"); nir = rd("nir").astype("float32")
        scl = rd("scl", out_shape=red.shape, resampling=Resampling.nearest)
        nd = np.where(np.isin(scl, [4, 5, 6, 7]), (nir - red) / (nir + red + 1e-9), np.nan)
        linha, ok = {"data": dt}, True
        for nome, m in UN:
            v = nd[m]; v = v[np.isfinite(v)]
            if v.size < 0.6 * m.sum():
                ok = False; break
            linha[nome] = float(np.median(v))
        if ok:
            reg.append(linha)
    except Exception:
        pass
    if (k + 1) % 40 == 0:
        print("  %d/%d lidas, %d validas" % (k + 1, len(cenas), len(reg)))
print("validas: %d" % len(reg))
json.dump(reg, open(os.path.join(AQUI, "amplitude_serie.json"), "w"), indent=1)

print("\nCURVA SAZONAL — mediana por mes, por ano\n")
tab = {}
for nome, _ in UN:
    print("%s" % nome)
    print("      " + "".join("%7s" % m for m in
          ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]))
    for ano in range(2022, 2027):
        L = []
        for m0 in range(1, 13):
            v = [r[nome] for r in reg
                 if int(r["data"][:4]) == ano and int(r["data"][5:7]) == m0]
            L.append(float(np.median(v)) if v else np.nan)
        tab.setdefault(nome, {})[ano] = L
        print("  %d " % ano + "".join("      ." if np.isnan(x) else "%7.3f" % x
                                      for x in L))
    print()

print("AMPLITUDE SAZONAL = pico Jul-Ago menos piso Dez-Fev, por ano\n")
print("%-16s" % "" + "".join("%9d" % a for a in range(2022, 2027)))
amp = {}
for nome, _ in UN:
    L = []
    for ano in range(2022, 2027):
        ver = [r[nome] for r in reg if int(r["data"][:4]) == ano
               and int(r["data"][5:7]) in (7, 8)]
        inv = [r[nome] for r in reg
               if (int(r["data"][:4]) == ano and int(r["data"][5:7]) in (1, 2))
               or (int(r["data"][:4]) == ano - 1 and int(r["data"][5:7]) == 12)]
        L.append(np.median(ver) - np.median(inv) if ver and inv else np.nan)
    amp[nome] = [None if np.isnan(x) else float(x) for x in L]
    print("%-16s" % nome + "".join("        ." if np.isnan(x) else "%9.3f" % x
                                   for x in L))
json.dump(dict(curva=tab, amplitude=amp),
          open(os.path.join(AQUI, "amplitude.json"), "w"), indent=1, default=str)
print("""
LEITURA
  amplitude mantida, pico mais baixo  ->  videira viva, vigor reduzido
  amplitude a colapsar                ->  a videira deixou de abrir""")
