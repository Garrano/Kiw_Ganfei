# -*- coding: utf-8 -*-
"""A assinatura espectral do kiwi, contra vinha, milho, pastagem e floresta.

Porque isto so agora e possivel
--------------------------------
Uma assinatura espectral precisa de **rotulos**. Ate hoje nao tinhamos nenhuns:
todas as classes deste caso saiam de limiares que nos proprios escolhemos, o
que e a definicao de circularidade.

O parcelario IFAP da rotulos que nao sao nossos — codigo de cultura declarado
pelo beneficiario e aceite pela administracao, campanha de 2025. E o LiDAR da
uma sexta classe que o parcelario nao tem: **floresta**, identificada por
altura acima de 5 m em terreno nao declarado. Uma pergola de kiwi tem 1,8 a
2,5 m; um pinhal ou eucaliptal tem muito mais.

Nenhuma das seis classes vem de um limiar sobre o sinal que se vai medir.

O que se mede
-------------
1. **Climatologia mensal de NDVI**, Janeiro de 2025 a Agosto de 2026. A
   fenologia e o discriminante forte: o kiwi e caduco e abrolha TARDE (Abril-
   Maio); a vinha e caduca com indice foliar muito menor; o milho e uma cultura
   de Verao com pico curto; a pastagem e permanente; a floresta de resinosas nao
   se mexe.
2. **Reflectancia por banda e NDMI no Verao**, do Landsat, que traz o SWIR que
   o Sentinel-2 nunca nos deu nesta cadeia. O teor de agua do copado separa
   estruturas de indice foliar alto de estruturas abertas.

Para que serve, alem da curiosidade
-----------------------------------
Testa se o nosso poligono de pomar e espectralmente coerente com kiwi
declarado noutro sitio, e se as 3,77 ha sem pergola se parecem com pastagem —
que e o que o parcelario diz que sao.
"""
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

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
LID = os.path.join(RAIZ, "lidar")
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

# janela alargada: precisamos de vinha, milho e floresta, que nao cabem na AOI
AOI2 = (528600.0, 4653400.0, 532600.0, 4655900.0)
PASSO = 10.0
NC = int((AOI2[2] - AOI2[0]) / PASSO)
NL = int((AOI2[3] - AOI2[1]) / PASSO)
DEST = from_origin(AOI2[0], AOI2[3], PASSO, PASSO)
print("janela alargada: %d x %d celulas de 10 m (%.0f x %.0f m)"
      % (NC, NL, AOI2[2] - AOI2[0], AOI2[3] - AOI2[1]))

# ---------------------------------------------------------------- 1. LiDAR
import glob
alt = {}
for tag in ("MDS", "MDT"):
    srcs = [rasterio.open(p) for p in sorted(glob.glob(os.path.join(LID, "%s-50cm-*.tif" % tag)))]
    b = transform_bounds("EPSG:32629", srcs[0].crs, *AOI2)
    mos, tr = merge(srcs, bounds=(b[0] - 60, b[1] - 60, b[2] + 60, b[3] + 60),
                    res=(2.0, 2.0), nodata=-999.0)
    out = np.full((NL * 5, NC * 5), np.nan, "float32")
    reproject(mos[0], out, src_transform=tr, src_crs=srcs[0].crs, src_nodata=-999.0,
              dst_transform=from_origin(AOI2[0], AOI2[3], 2.0, 2.0),
              dst_crs="EPSG:32629", dst_nodata=np.nan, resampling=RS.bilinear)
    alt[tag] = out
    for s in srcs:
        s.close()
CHM2 = alt["MDS"] - alt["MDT"]
H = np.nanmedian(CHM2.reshape(NL, 5, NC, 5), axis=(1, 3))
print("altura: mediana %.2f m, %.1f%% acima de 5 m" % (np.nanmedian(H), 100 * np.nanmean(H > 5)))

# ------------------------------------------------------------- 2. parcelario
B = ("https://agrodigital.ccdr-n.pt/MapasLeft_Net_para_servidor/"
     "MapasLeft_Net_para_servidor/MapasLeft_Net/MapaComCAOP/IfapWfsProxy.ashx")
t = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
ti = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
lo, la = t.transform(AOI2[0] - 200, AOI2[1] - 200)
lo2, la2 = t.transform(AOI2[2] + 200, AOI2[3] + 200)
d = requests.get(B, params={"layer": "culturas.2025jun10", "max": 50000,
                            "bbox": "%.6f,%.6f,%.6f,%.6f" % (lo, la, lo2, la2)},
                 timeout=300).json()


def utm(g):
    c = lambda a: [list(ti.transform(x, y)) for x, y in a]
    return ({"type": "Polygon", "coordinates": [c(a) for a in g["coordinates"]]}
            if g["type"] == "Polygon" else
            {"type": "MultiPolygon",
             "coordinates": [[c(a) for a in p] for p in g["coordinates"]]})


formas, cod, nomes = [], {}, {}
for i, f in enumerate(d["features"], 1):
    p = f["properties"]
    if not p.get("PUN_CUL_COD"):
        continue
    c = int(p["PUN_CUL_COD"]); cod[i] = c; nomes[c] = p["PUN_CUL_DESC"]
    formas.append((utm(f["geometry"]), i))
idx = rasterize(formas, out_shape=(NL, NC), transform=DEST, fill=0, dtype="int32")
CUL = np.zeros((NL, NC), "int32")
for i, c in cod.items():
    CUL[idx == i] = c
print("cultura declarada em %.1f %% da janela" % (100 * (CUL > 0).mean()))

# --------------------------------------------------------------- 3. classes
# erosao de uma celula para evitar pixeis de fronteira
from scipy import ndimage


def puro(m, it=1):
    return ndimage.binary_erosion(m, np.ones((3, 3)), iterations=it)


CLASSES = [
    ("kiwi", puro(CUL == 124)),
    ("vinha", puro(CUL == 34)),
    ("milho", puro(CUL == 6)),
    ("pastagem/prado", puro(np.isin(CUL, [142, 143]))),
    ("floresta >5 m", puro((CUL == 0) & np.isfinite(H) & (H > 5.0), 2)),
]
print("\n%-18s %8s" % ("classe", "ha"))
for n, m in CLASSES:
    print("%-18s %8.2f" % (n, m.sum() / 100.0))

# ---------------------------------------------------- 4. climatologia S2
por_data = {}
for ano in (2025, 2026):
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
print("\ncenas Sentinel-2 2025-2026, nuvem <25%%: %d" % len(cenas))

mens = defaultdict(lambda: defaultdict(list))
for k, (dt, a) in enumerate(cenas):
    try:
        def rd(b, **kw):
            with rasterio.Env(**ENV), rasterio.open(a[b]["href"]) as ds:
                return ds.read(1, window=from_bounds(*AOI2, transform=ds.transform), **kw)
        red = rd("red").astype("float32"); nir = rd("nir").astype("float32")
        scl = rd("scl", out_shape=red.shape, resampling=Resampling.nearest)
        nd = np.where(np.isin(scl, [4, 5, 6, 7]), (nir - red) / (nir + red + 1e-9), np.nan)
        for nome, m in CLASSES:
            v = nd[m]; v = v[np.isfinite(v)]
            if v.size > 0.5 * m.sum():
                mens[nome][int(dt[5:7])].append(float(np.median(v)))
    except Exception:
        pass
    if (k + 1) % 30 == 0:
        print("  %d/%d" % (k + 1, len(cenas)))

print("\nCLIMATOLOGIA MENSAL DE NDVI  (mediana de todas as cenas do mes)\n")
print("%-18s" % "" + "".join("%7s" % s for s in
      ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]))
clim = {}
for nome, _ in CLASSES:
    L = [float(np.median(mens[nome][m])) if mens[nome][m] else np.nan for m in range(1, 13)]
    clim[nome] = L
    print("%-18s" % nome + "".join("      ." if np.isnan(v) else "%7.3f" % v for v in L))

print("\nDISCRIMINANTES DERIVADOS\n")
print("%-18s %9s %9s %11s %13s" %
      ("classe", "piso DJF", "pico JA", "amplitude", "mes de subida"))
disc = {}
for nome, _ in CLASSES:
    L = np.array(clim[nome])
    inv = np.nanmedian([L[11], L[0], L[1]])
    pic = np.nanmedian([L[6], L[7]])
    meio = inv + 0.5 * (pic - inv)
    subida = np.nan
    for m in range(2, 8):
        if np.isfinite(L[m]) and L[m] >= meio:
            subida = m + 1; break
    disc[nome] = dict(piso=float(inv), pico=float(pic), amp=float(pic - inv),
                      mes_subida=None if np.isnan(subida) else int(subida))
    print("%-18s %9.3f %9.3f %11.3f %13s"
          % (nome, inv, pic, pic - inv, "%d" % subida if subida == subida else "-"))
json.dump(dict(clim=clim, disc=disc, nomes={str(k): v for k, v in nomes.items()}),
          open(os.path.join(AQUI, "assinatura.json"), "w"), indent=1, ensure_ascii=False)
np.save(os.path.join(AQUI, "assin_CUL.npy"), CUL)
np.save(os.path.join(AQUI, "assin_H.npy"), H)
print("\nescrito assinatura.json")
