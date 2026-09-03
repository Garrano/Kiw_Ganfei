# -*- coding: utf-8 -*-
"""B1 contra corpo principal — a experiencia natural que estava fora da janela.

A pergunta, e porque e a que importa
------------------------------------
O declinio do kiwi e uma doenca de raiz, e o porta-enxerto e o maior modificador
conhecido. Esta exploracao tem os dois bracos da experiencia dentro de si:

    B1, valvulas 2-5      raiz de SUMMER KIWI, enxertada Erica por volta de 2020
    corpo principal       ERICA DE PE FRANCO

Mesma origem de agua, mesmo terraco aluvial, mesmo gestor, mesmo clima, mesma
casta acima do ponto de enxertia desde ~2020. **A unica diferenca sistematica e
o que esta debaixo do solo.**

Todo o dossie ate hoje mediu **so o braco de pe franco**, porque a AOI foi
desenhada na primeira hora sobre o corpo principal e nunca mais foi
questionada. Os tres analistas independentes assinalaram, cada um por si, que o
B1 estava fora do raster.

A janela, e o confundimento que a fixa
--------------------------------------
O B1 foi cortado e enxertado com Enza Gold em **2016**, teve rede nesse periodo,
e foi re-enxertado com Erica por volta de **2020**, com a rede removida. A serie
anterior a 2021 mistura enxertia e rede e nao e interpretavel.

**Janela de comparacao: 2021-2026.** Os dois bracos com a mesma casta, a diferir
so na raiz.

O que NAO se pode fazer, e ja custou caro
-----------------------------------------
Nao comparar **niveis** de NDVI entre B1 e corpo principal — a C2 proibiu-o e a
razao mantem-se: sao instalacoes de idade e densidade diferentes. Compara-se a
**trajectoria** de cada um contra uma referencia comum dentro da mesma cena.

Mascaras e referencia, nenhuma derivada do sinal
------------------------------------------------
  kiwi        poligonos declarados IFAP, codigo 124, campanha 2025
  altura      MDS-MDT do voo LiDAR de 06-07-2025
  referencia  terreno NAO declarado com altura acima de 5 m — mata perene,
              fora dos dois bracos, definida por geometria

Limitacao declarada
-------------------
O B1 tem 13,01 ha na tabela do gestor, dos quais as valvulas 2-5 (Summer Kiwi)
sao 7,66 ha; a valvula 1 e os satelites B1C5 e B1C6 sao pe franco. **Nao tenho
as posicoes das valvulas 1 a 5** — o `valvulas_por_area.json` comeca na 6 — e
por isso nao consigo separar dentro do B1. O braco medido e portanto
**maioritariamente, nao exclusivamente, Summer Kiwi.** Pedir ao gestor o
esquema de valvulas do B1 fecha isto.
"""
import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np
import rasterio
import requests
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.features import rasterize
from rasterio.merge import merge
from rasterio.transform import from_origin
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject, transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

AOI3 = (529300.0, 4653700.0, 531900.0, 4655700.0)
PASSO = 10.0
NC = int((AOI3[2] - AOI3[0]) / PASSO)
NL = int((AOI3[3] - AOI3[1]) / PASSO)
DEST = from_origin(AOI3[0], AOI3[3], PASSO, PASSO)
print("janela: %d x %d celulas (%.0f x %.0f m)"
      % (NC, NL, AOI3[2] - AOI3[0], AOI3[3] - AOI3[1]))

# ------------------------------------------------------------------- altura
alt = {}
for tag in ("MDS", "MDT"):
    srcs = [rasterio.open(p) for p in sorted(glob.glob(
        os.path.join(RAIZ, "lidar", "%s-50cm-*.tif" % tag)))]
    b = transform_bounds("EPSG:32629", srcs[0].crs, *AOI3)
    mos, tr = merge(srcs, bounds=(b[0] - 60, b[1] - 60, b[2] + 60, b[3] + 60),
                    res=(2.0, 2.0), nodata=-999.0)
    o = np.full((NL * 5, NC * 5), np.nan, "float32")
    reproject(mos[0], o, src_transform=tr, src_crs=srcs[0].crs, src_nodata=-999.0,
              dst_transform=from_origin(AOI3[0], AOI3[3], 2.0, 2.0),
              dst_crs="EPSG:32629", dst_nodata=np.nan, resampling=RS.bilinear)
    alt[tag] = o
    for s in srcs:
        s.close()
CHM = alt["MDS"] - alt["MDT"]
H = np.nanmedian(CHM.reshape(NL, 5, NC, 5), axis=(1, 3))
FRAC = np.nanmean((CHM > 1.5).astype("float32").reshape(NL, 5, NC, 5), axis=(1, 3))
print("altura: %.1f%% da janela com dados" % (100 * np.isfinite(H).mean()))

# --------------------------------------------------------------- parcelario
B = ("https://agrodigital.ccdr-n.pt/MapasLeft_Net_para_servidor/"
     "MapasLeft_Net_para_servidor/MapasLeft_Net/MapaComCAOP/IfapWfsProxy.ashx")
t = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
ti = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
lo, la = t.transform(AOI3[0] - 200, AOI3[1] - 200)
lo2, la2 = t.transform(AOI3[2] + 200, AOI3[3] + 200)
d = requests.get(B, params={"layer": "culturas.2025jun10", "max": 50000,
                            "bbox": "%.6f,%.6f,%.6f,%.6f" % (lo, la, lo2, la2)},
                 timeout=300).json()


def utm(g):
    c = lambda a: [list(ti.transform(x, y)) for x, y in a]
    return ({"type": "Polygon", "coordinates": [c(a) for a in g["coordinates"]]}
            if g["type"] == "Polygon" else
            {"type": "MultiPolygon",
             "coordinates": [[c(a) for a in p] for p in g["coordinates"]]})


formas = [(utm(f["geometry"]), 1) for f in d["features"]
          if f["properties"].get("PUN_CUL_COD") == "124"]
KIWI = rasterize(formas, out_shape=(NL, NC), transform=DEST, fill=0,
                 dtype="uint8").astype(bool)
outras = [(utm(f["geometry"]), 1) for f in d["features"]
          if f["properties"].get("PUN_CUL_COD") not in (None, "124")]
OUTRAS = rasterize(outras, out_shape=(NL, NC), transform=DEST, fill=0,
                   dtype="uint8").astype(bool) if outras else np.zeros_like(KIWI)
print("kiwi declarado na janela: %.2f ha" % (KIWI.sum() / 100.0))

yy, xx = np.mgrid[:NL, :NC]
Ec = AOI3[0] + (xx + .5) * PASSO
Nc = AOI3[3] - (yy + .5) * PASSO

ero = lambda m, i=1: ndimage.binary_erosion(m, np.ones((3, 3)), iterations=i)
COM = np.isfinite(H) & (H >= 0.5)
B1 = ero(KIWI & COM & (Ec < 530200) & (Nc < 4654650))
CORPO = ero(KIWI & COM & (Nc > 4654750) & (Ec > 530100))
MATA = ero((~KIWI) & (~OUTRAS) & np.isfinite(H) & (H > 5.0), 2)
print("\n%-22s %8s %10s %11s" % ("braco", "ha", "altura", "%>1,5 m"))
for n, m in (("B1 (Summer Kiwi*)", B1), ("corpo (Erica pe franco)", CORPO),
             ("mata, referencia", MATA)):
    k = m & np.isfinite(H)
    print("%-22s %8.2f %8.2f m %10.1f %%"
          % (n, m.sum() / 100.0, np.median(H[k]), 100 * np.median(FRAC[k])))
print("* maioritariamente: valvulas 2-5 sao Summer Kiwi (7,66 ha de 13,01);"
      " valvula 1 e satelites sao pe franco")

# ------------------------------------------------------------------- serie
por_data = {}
for ano in range(2021, 2027):
    for m0 in range(1, 13):
        m1 = m0 % 12 + 1; a1 = ano + (1 if m1 == 1 else 0)
        try:
            r = requests.post("https://earth-search.aws.element84.com/v1/search",
                              json={"collections": ["sentinel-2-l2a"],
                                    "bbox": [lo, la, lo2, la2],
                                    "datetime": "%d-%02d-01T00:00:00Z/%d-%02d-01T00:00:00Z"
                                                % (ano, m0, a1, m1),
                                    "query": {"eo:cloud_cover": {"lt": 25}},
                                    "limit": 100}, timeout=120).json()
        except Exception:
            continue
        for x in r.get("features", []):
            por_data.setdefault(x["properties"]["datetime"][:10], x["assets"])
cenas = sorted(por_data.items())
print("\ncenas Sentinel-2 2021-2026, nuvem <25%%: %d" % len(cenas))

reg = []
UN = [("B1", B1), ("corpo", CORPO), ("mata", MATA)]
for k, (dt, a) in enumerate(cenas):
    try:
        def rd(b, **kw):
            with rasterio.Env(**ENV), rasterio.open(a[b]["href"]) as ds:
                return ds.read(1, window=from_bounds(*AOI3, transform=ds.transform), **kw)
        red = rd("red").astype("float32"); nir = rd("nir").astype("float32")
        scl = rd("scl", out_shape=red.shape, resampling=Resampling.nearest)
        nd = np.where(np.isin(scl, [4, 5, 6, 7]), (nir - red) / (nir + red + 1e-9), np.nan)
        linha, ok = {"data": dt}, True
        for n, m in UN:
            v = nd[m]; v = v[np.isfinite(v)]
            if v.size < 0.5 * m.sum():
                ok = False; break
            linha[n] = float(np.median(v))
        if ok:
            reg.append(linha)
    except Exception:
        pass
    if (k + 1) % 40 == 0:
        print("  %d/%d, %d validas" % (k + 1, len(cenas), len(reg)))
print("validas: %d" % len(reg))
json.dump(reg, open(os.path.join(AQUI, "b1_serie.json"), "w"), indent=1)

anos = list(range(2021, 2027))
print("\nPICO DE VERAO (mediana Jul-Ago) e FOSSO A MATA\n")
print("%-26s" % "" + "".join("%9d" % a for a in anos))
for n, _ in UN:
    L = [np.median([r[n] for r in reg if int(r["data"][:4]) == a
                    and int(r["data"][5:7]) in (7, 8)] or [np.nan]) for a in anos]
    print("%-26s" % ("%s, pico" % n) + "".join("        ." if np.isnan(v)
                                               else "%9.3f" % v for v in L))
print()
for n, _ in UN[:2]:
    L = []
    for a in anos:
        s = [r["mata"] - r[n] for r in reg if int(r["data"][:4]) == a
             and int(r["data"][5:7]) in (7, 8)]
        L.append(np.median(s) if s else np.nan)
    print("%-26s" % ("fosso %s - mata" % n) + "".join(
        "        ." if np.isnan(v) else "%+9.3f" % v for v in L))

print("\nAMPLITUDE SAZONAL (pico Jul-Ago menos piso Dez-Fev)\n")
print("%-26s" % "" + "".join("%9d" % a for a in anos))
amp = {}
for n, _ in UN:
    L = []
    for a in anos:
        ver = [r[n] for r in reg if int(r["data"][:4]) == a and int(r["data"][5:7]) in (7, 8)]
        inv = [r[n] for r in reg if (int(r["data"][:4]) == a and int(r["data"][5:7]) in (1, 2))
               or (int(r["data"][:4]) == a - 1 and int(r["data"][5:7]) == 12)]
        L.append(np.median(ver) - np.median(inv) if ver and inv else np.nan)
    amp[n] = [None if np.isnan(v) else float(v) for v in L]
    print("%-26s" % n + "".join("        ." if np.isnan(v) else "%9.3f" % v for v in L))
print()
for n in ("B1", "corpo"):
    L = [a / b if a and b else np.nan for a, b in zip(amp[n], amp["mata"])]
    print("%-26s" % ("%s / mata" % n) + "".join(
        "        ." if v != v else "%9.2f" % v for v in L))
json.dump(dict(amplitude=amp), open(os.path.join(AQUI, "b1_amplitude.json"), "w"), indent=1)
