# -*- coding: utf-8 -*-
"""O piso de Inverno — o teste que separa videira viva de videira arrancada.

O analista B (espacial) reporta que o piso de Inverno de 2024/25 subiu para
0,525 e 0,676 nos nucleos de leste enquanto o controlo ficou em 0,286, e le
isso como cobertura verde continua onde uma pergola de folha caduca devia
estar despida — ou seja, videiras arrancadas. E da ao foco OESTE o veredicto
oposto: piso de Inverno normal, videiras vivas com vigor reduzido.

Isto e demasiado decisivo para entrar por relatorio de terceiro. Verifica-se
aqui de forma independente, com mascaras proprias e serie propria.

A logica, que e boa e nao e minha: o kiwi e de folha caduca. Em Dezembro a
Fevereiro uma pergola viva deixa ver o chao e le baixo. Se um talhao le ALTO
no Inverno, o que la esta e verde permanente — erva, coberto, replantacao
jovem — e nao uma pergola adormecida.
"""
import datetime as dtm
import json
import os
import sys

import numpy as np
import rasterio
import requests
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.windows import from_bounds
from scipy import ndimage

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
NU21 = masc["nu2021"] & POMAR
d26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)
do, de = discos_dos_focos(POMAR)

# nucleos do B, pelas coordenadas que ele publica, com discos de 80 m
def disco(x, y, r=80.0):
    yy, xx = np.mgrid[:NL, :NC]
    cx = AOI[0] + (xx + .5) * PASSO
    cy = AOI[3] - (yy + .5) * PASSO
    return np.hypot(cx - x, cy - y) <= r

N1 = disco(530476, 4655046) & POMAR
N2 = disco(530895, 4655052) & POMAR
N3 = disco(531068, 4655145) & POMAR
UN = [("N1 foco OESTE", N1), ("N2 leste", N2), ("N3 leste", N3),
      ("foco ESTE da cadeia", de & POMAR & ~NU21),
      ("referencia", REF), ("resto do pomar", POMAR & ~d26 & ~REF)]
for n, m in UN:
    print("%-22s %5.2f ha" % (n, m.sum() / 100.0))

tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1]); lo2, la2 = tr.transform(AOI[2], AOI[3])
# a janela inteira de dez anos rebenta o endpoint; pede-se Inverno a Inverno
por_data = {}
for ano in range(2017, 2027):
    for i0, i1 in (("%d-12-01" % ano, "%d-12-31" % ano),
                   ("%d-01-01" % ano, "%d-02-28" % ano)):
        try:
            r = requests.post(
                "https://earth-search.aws.element84.com/v1/search",
                json={"collections": ["sentinel-2-l2a"],
                      "bbox": [lo, la, lo2, la2],
                      "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (i0, i1),
                      "query": {"eo:cloud_cover": {"lt": 25}}, "limit": 100},
                timeout=120).json()
        except Exception as e:
            print("  falhou %s: %s" % (i0, e))
            continue
        if "features" not in r:
            print("  sem features %s: %s" % (i0, str(r)[:120]))
            continue
        for x in r["features"]:
            por_data.setdefault(x["properties"]["datetime"][:10], x["assets"])
cenas = sorted(por_data.items())
print("\ncenas de Dez-Jan-Fev com nuvem <25%%: %d" % len(cenas))

reg = []
for dt, a in cenas:
    try:
        def rd(b, **kw):
            with rasterio.Env(**ENV), rasterio.open(a[b]["href"]) as ds:
                return ds.read(1, window=from_bounds(*AOI, transform=ds.transform), **kw)
        red = rd("red").astype("float32"); nir = rd("nir").astype("float32")
        scl = rd("scl", out_shape=red.shape, resampling=Resampling.nearest)
        nd = np.where(np.isin(scl, [4, 5, 6, 7]),
                      (nir - red) / (nir + red + 1e-9), np.nan)
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
print("cenas validas em todas as mascaras: %d" % len(reg))
json.dump(reg, open(os.path.join(AQUI, "piso_inverno.json"), "w"), indent=1)

def inverno(d):
    y, m = int(d[:4]), int(d[5:7])
    return y if m == 12 else y - 1

anos = sorted({inverno(r["data"]) for r in reg})
print("\nPISO DE INVERNO (mediana Dez-Fev do NDVI), por Inverno\n")
print("%-9s %5s " % ("Inverno", "n") + "".join("%15s" % n for n, _ in UN))
tab = {}
for A_ in anos:
    sub = [r for r in reg if inverno(r["data"]) == A_]
    if len(sub) < 2:
        continue
    linha = {n: float(np.median([r[n] for r in sub])) for n, _ in UN}
    tab["%d/%d" % (A_, (A_ + 1) % 100)] = dict(n=len(sub), **linha)
    print("%-9s %5d " % ("%d/%d" % (A_, (A_ + 1) % 100), len(sub))
          + "".join("%15.3f" % linha[n] for n, _ in UN))
json.dump(tab, open(os.path.join(AQUI, "piso_inverno_tabela.json"), "w"), indent=1)
print("""
LEITURA
   piso baixo, proximo do controlo  ->  pergola de folha caduca adormecida.
                                        As videiras estao la.
   piso alto, muito acima           ->  verde permanente onde devia estar
                                        despido. As videiras nao estao la.""")
