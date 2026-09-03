# -*- coding: utf-8 -*-
"""2026 foi um ano mau para a paisagem, ou so para este pomar?

A contradicao que ninguem resolveu
----------------------------------
A corrida B do multiverso imprimiu que a **vegetacao envolvente caiu 0,075
entre 2024 e 2026 — o dobro da queda do bloco** — e nunca juntou os dois
numeros. A corrida C mediu que a sua referencia **nao se move**: −0,0070,
p = 0,54.

**As duas nao podem estar as duas certas.** E se a primeira estiver, o pomar
esta a cair MENOS do que a paisagem a volta, e o enquadramento do caso
inverte-se: deixa de ser «este pomar adoeceu» e passa a ser «2026 foi mau para
tudo, e o pomar aguentou melhor do que a paisagem».

Porque e que as duas podem discordar
------------------------------------
Porque «vegetacao envolvente» e «referencia estavel» nao sao a mesma coisa. Se
a envolvente incluir culturas anuais, pastagem ou matos, ela responde ao ano
meteorologico; se for mata madura de folha persistente, nao responde quase
nada. **A discordancia pode nao ser erro de ninguem: pode ser duas definicoes.**

O desenho
---------
Mede-se a variacao 2024→2026 em **classes de coberto separadas**, todas nas
MESMAS cenas e na mesma janela, com rotulos que nao vem de nos:

  parcelario IFAP   kiwi (124), vinha (34), milho (6), pastagem/prado (142/143)
  LiDAR             mata alta, altura acima de 5 m em terreno nao declarado
                    mato/incultura, altura entre 0,5 e 5 m, nao declarado

Se a queda for geral, aparece em todas as classes. Se for so no kiwi, aparece
so no kiwi. Se aparecer nas anuais e nas pastagens mas nao na mata, e ano
meteorologico e nao mortalidade.

**Isto nao decide a causa. Decide o denominador.**
"""
import glob
import json
import os
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
from scipy import ndimage, stats

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

AOI = (528600.0, 4653400.0, 532600.0, 4655900.0)
PASSO = 10.0
NC = int((AOI[2] - AOI[0]) / PASSO)
NL = int((AOI[3] - AOI[1]) / PASSO)
DEST = from_origin(AOI[0], AOI[3], PASSO, PASSO)
print("janela: %d x %d celulas (%.1f x %.1f km)"
      % (NC, NL, (AOI[2] - AOI[0]) / 1000, (AOI[3] - AOI[1]) / 1000))

# ------------------------------------------------------------------- altura
alt = {}
for tag in ("MDS", "MDT"):
    srcs = [rasterio.open(p) for p in sorted(glob.glob(
        os.path.join(RAIZ, "lidar", "%s-50cm-*.tif" % tag)))]
    b = transform_bounds("EPSG:32629", srcs[0].crs, *AOI)
    mos, tr = merge(srcs, bounds=(b[0] - 60, b[1] - 60, b[2] + 60, b[3] + 60),
                    res=(2.0, 2.0), nodata=-999.0)
    o = np.full((NL * 5, NC * 5), np.nan, "float32")
    reproject(mos[0], o, src_transform=tr, src_crs=srcs[0].crs, src_nodata=-999.0,
              dst_transform=from_origin(AOI[0], AOI[3], 2.0, 2.0),
              dst_crs="EPSG:32629", dst_nodata=np.nan, resampling=RS.bilinear)
    alt[tag] = o
    for s in srcs:
        s.close()
H = np.nanmedian((alt["MDS"] - alt["MDT"]).reshape(NL, 5, NC, 5), axis=(1, 3))

# --------------------------------------------------------------- parcelario
B = ("https://agrodigital.ccdr-n.pt/MapasLeft_Net_para_servidor/"
     "MapasLeft_Net_para_servidor/MapasLeft_Net/MapaComCAOP/IfapWfsProxy.ashx")
t = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
ti = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
lo, la = t.transform(AOI[0] - 200, AOI[1] - 200)
lo2, la2 = t.transform(AOI[2] + 200, AOI[3] + 200)
d = requests.get(B, params={"layer": "culturas.2025jun10", "max": 50000,
                            "bbox": "%.6f,%.6f,%.6f,%.6f" % (lo, la, lo2, la2)},
                 timeout=300).json()


def utm(g):
    c = lambda a: [list(ti.transform(x, y)) for x, y in a]
    return ({"type": "Polygon", "coordinates": [c(a) for a in g["coordinates"]]}
            if g["type"] == "Polygon" else
            {"type": "MultiPolygon",
             "coordinates": [[c(a) for a in p] for p in g["coordinates"]]})


formas, cod = [], {}
for i, f in enumerate(d["features"], 1):
    p = f["properties"]
    if not p.get("PUN_CUL_COD"):
        continue
    cod[i] = int(p["PUN_CUL_COD"])
    formas.append((utm(f["geometry"]), i))
idx = rasterize(formas, out_shape=(NL, NC), transform=DEST, fill=0, dtype="int32")
CUL = np.zeros((NL, NC), "int32")
for i, c in cod.items():
    CUL[idx == i] = c

ero = lambda m, i=1: ndimage.binary_erosion(m, np.ones((3, 3)), iterations=i)
CLASSES = [
    ("kiwi (IFAP 124)", ero(CUL == 124)),
    ("vinha (34)", ero(CUL == 34)),
    ("milho (6)", ero(CUL == 6)),
    ("pastagem/prado (142/143)", ero(np.isin(CUL, [142, 143]))),
    ("mata alta >5 m", ero((CUL == 0) & np.isfinite(H) & (H > 5.0), 2)),
    ("mato 0,5-5 m", ero((CUL == 0) & np.isfinite(H) & (H > 0.5) & (H <= 5.0), 2)),
]
print("\n%-28s %8s" % ("classe", "ha"))
for n, m in CLASSES:
    print("%-28s %8.2f" % (n, m.sum() / 100.0))

# ------------------------------------------------------------------- cenas
por_data = {}
for ano in (2024, 2026):
    for m0 in (6, 7, 8):
        m1 = m0 + 1
        try:
            r = requests.post("https://earth-search.aws.element84.com/v1/search",
                              json={"collections": ["sentinel-2-l2a"],
                                    "bbox": [lo, la, lo2, la2],
                                    "datetime": "%d-%02d-01T00:00:00Z/%d-%02d-01T00:00:00Z"
                                                % (ano, m0, ano, m1),
                                    "query": {"eo:cloud_cover": {"lt": 25}},
                                    "limit": 100}, timeout=120).json()
        except Exception:
            continue
        for x in r.get("features", []):
            por_data.setdefault(x["properties"]["datetime"][:10], x["assets"])
cenas = sorted(por_data.items())
print("\ncenas Jun-Ago de 2024 e 2026, nuvem <25%%: %d" % len(cenas))

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
        for n, m in CLASSES:
            v = nd[m]; v = v[np.isfinite(v)]
            if v.size < 0.5 * m.sum():
                ok = False; break
            linha[n] = float(np.median(v))
        if ok:
            reg.append(linha)
    except Exception:
        pass
print("cenas validas em todas as classes: %d" % len(reg))
json.dump(reg, open(os.path.join(AQUI, "paisagem.json"), "w"), indent=1)

print("\nVARIACAO 2024 -> 2026, POR CLASSE DE COBERTO")
print("mesmas cenas, mesma janela, rotulos que nao vem de nos\n")
print("%-28s %9s %9s %10s %10s %8s" %
      ("classe", "2024", "2026", "variacao", "IC95", "p"))
res = {}
for n, _ in CLASSES:
    a24 = [r[n] for r in reg if r["data"][:4] == "2024"]
    a26 = [r[n] for r in reg if r["data"][:4] == "2026"]
    if len(a24) < 3 or len(a26) < 3:
        continue
    d_ = np.mean(a26) - np.mean(a24)
    tt = stats.ttest_ind(a26, a24, equal_var=False)
    se = np.hypot(np.std(a26, ddof=1) / np.sqrt(len(a26)),
                  np.std(a24, ddof=1) / np.sqrt(len(a24)))
    res[n] = dict(n24=len(a24), n26=len(a26), m24=float(np.mean(a24)),
                  m26=float(np.mean(a26)), dif=float(d_), p=float(tt.pvalue))
    print("%-28s %9.4f %9.4f %+10.4f  ±%.4f %8.4f"
          % (n, np.mean(a24), np.mean(a26), d_, 1.96 * se, tt.pvalue))
json.dump(res, open(os.path.join(AQUI, "paisagem_resultado.json"), "w"), indent=1)

print("""
LEITURA
  cai em todas as classes            -> ano meteorologico. O denominador move-se
                                        e o enquadramento do caso muda.
  cai so no kiwi                     -> o efeito e da cultura, nao do ano.
  cai nas anuais e nao na mata       -> resposta de ciclo curto ao ano, e a mata
                                        continua a servir de referencia.""")
