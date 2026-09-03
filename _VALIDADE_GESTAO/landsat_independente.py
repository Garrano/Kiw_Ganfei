# -*- coding: utf-8 -*-
"""Landsat 8/9 — a segunda medicao optica de proveniencia independente.

O que o certificado da C2 pediu
-------------------------------
Na lista NAO TESTAVEL: «a queda do foco ESTE em 2025-2026 nao tem instrumento
independente, e o radar positivamente nao a ve». Pede «uma segunda medicao
optica de outra proveniencia».

O LiDAR respondeu ao substrato — ha planta ali — mas nao a datacao, porque e
uma data so. Isto responde a datacao.

Porque o Landsat conta como independente
----------------------------------------
Outra agencia (USGS/NASA, nao ESA), outro sensor (OLI-2, nao MSI), outra
cadeia de calibracao e de correccao atmosferica (LaSRC, nao Sen2Cor), outra
orbita e outra hora de passagem. Partilha com o Sentinel-2 apenas o principio
fisico. E imune, por construcao, ao vies de calibracao do S2C que estragou
metade do degrau publicado.

O preco: 30 m em vez de 10.

CORRECCAO DE 31-08-2026, exigida pelo Controlo 3. Este cabecalho dizia:

    «O foco ESTE com pergola tem 1,27 ha, ou seja 14 pixeis Landsat. Poucos.
     Por isso so se usam pixeis **inteiramente dentro** da unidade, e
     reporta-se o n.»

**O codigo nunca fez nem uma coisa nem outra.** Faz `reproject(..., RS.nearest)`
da cena para a grelha de 10 m e depois `np.median(ndvi[m])` sobre a mascara de
10 m: cada pixel Landsat de 30 m passa a nove celulas, e nao ha filtro de
contencao nem contagem na saida. O unico teste e `v.size < 0.5 * m.sum()`, que
verifica fraccao de celulas finitas, nao independencia.

E a familia exacta do `fazer_masks_v2.py` que a `CLAUDE.md` deste projecto
nomeia para nunca mais se repetir — cabecalho a afirmar uma coisa, codigo a
fazer outra. Foi apanhado pelo adversario da R2, contado pelo T4, e so agora
corrigido no sitio onde enganava.

O n verdadeiro, medido em `t4_n_landsat.py` (blocos de 30 m distintos, e entre
parentesis os que caem inteiramente dentro da unidade):

    OESTE com pergola     35  (12)
    ESTE  com pergola     27  ( 2)
    resto do pomar       334  (105)
    referencia           110  ( 0)   <- uma celula por pixel: o valor que sai
                                        e o da vizinhanca de 30 m, nao o dela

**Qualquer numero deste ficheiro tem de circular com o seu n.** A serie da
referencia nao deve circular de todo.

Duas grandezas, nao uma
-----------------------
NDVI, para ser comparavel com tudo o que ja se fez.
NDMI = (NIR - SWIR1) / (NIR + SWIR1), agua no copado. **Nao e a mesma
grandeza que verdura** e o Sentinel-2 nunca no-la deu nesta cadeia. Uma videira
com stress hidrico ou vascular perde NDMI antes de perder NDVI.
"""
import json
import os
import sys

import numpy as np
import planetary_computer as pc
import pystac_client
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject
from rasterio.transform import from_origin
from rasterio.windows import from_bounds
from pyproj import Transformer

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(AQUI, "chm_altura.npy"))
COM, SEM = np.isfinite(h) & (h >= 0.5), np.isfinite(h) & (h < 0.5)
do, de = discos_dos_focos(POMAR)

UN = [("ESTE com pergola", de & POMAR & COM),
      ("ESTE sem pergola", de & POMAR & SEM),
      ("OESTE com pergola", do & POMAR & COM),
      ("referencia", REF),
      ("resto do pomar", POMAR & COM & ~do & ~de & ~REF)]

cat = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace)
tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1])
lo2, la2 = tr.transform(AOI[2], AOI[3])
itens = list(cat.search(collections=["landsat-c2-l2"],
                        bbox=[lo, la, lo2, la2],
                        datetime="2013-01-01/2026-12-31",
                        query={"eo:cloud_cover": {"lt": 40},
                               "platform": {"in": ["landsat-8", "landsat-9"]}}
                        ).items())
itens = [i for i in itens if 6 <= i.datetime.month <= 9]
itens.sort(key=lambda i: i.datetime)
print("cenas Landsat 8/9 de Jun-Set, nuvem <40%%: %d" % len(itens))

# grelha de destino: a nossa grelha de 10 m, para as mascaras baterem
DEST = from_origin(AOI[0], AOI[3], PASSO, PASSO)


def le(item, chave):
    a = item.assets[chave]
    with rasterio.open(a.href) as ds:
        b = transform_bounds_cache(ds.crs)
        w = from_bounds(*b, transform=ds.transform)
        arr = ds.read(1, window=w).astype("float32")
        out = np.full((NL, NC), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(w), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=RS.nearest)
        return out


from rasterio.warp import transform_bounds
_cache = {}


def transform_bounds_cache(crs):
    k = str(crs)
    if k not in _cache:
        _cache[k] = transform_bounds("EPSG:32629", crs, *AOI)
    return _cache[k]


reg = []
for k, it in enumerate(itens):
    try:
        red = le(it, "red"); nir = le(it, "nir08")
        sw1 = le(it, "swir16"); qa = le(it, "qa_pixel")
        # escala Collection-2 Level-2
        esc = lambda a: a * 0.0000275 - 0.2
        red, nir, sw1 = esc(red), esc(nir), esc(sw1)
        q = qa.astype("int32")
        limpo = np.isfinite(qa) & ((q & 0b11000) == 0) & ((q & 0b10) == 0)
        ndvi = np.where(limpo, (nir - red) / (nir + red + 1e-9), np.nan)
        ndmi = np.where(limpo, (nir - sw1) / (nir + sw1 + 1e-9), np.nan)
        linha = {"data": it.datetime.strftime("%Y-%m-%d"),
                 "plataforma": it.properties.get("platform")}
        ok = True
        for nome, m in UN:
            v, w = ndvi[m], ndmi[m]
            v, w = v[np.isfinite(v)], w[np.isfinite(w)]
            if v.size < 0.5 * m.sum():
                ok = False
                break
            linha[nome] = float(np.median(v))
            linha[nome + " |NDMI"] = float(np.median(w))
        if ok and 0.2 < linha["referencia"] < 1.0:
            reg.append(linha)
    except Exception as e:
        pass
    if (k + 1) % 20 == 0:
        print("  %d/%d, %d validas" % (k + 1, len(itens), len(reg)))

print("cenas validas: %d" % len(reg))
json.dump(reg, open(os.path.join(AQUI, "landsat.json"), "w"), indent=1)

for ind, suf in (("NDVI", ""), ("NDMI", " |NDMI")):
    print("\n%s — fosso a referencia (referencia menos unidade), por ano" % ind)
    anos = sorted({r["data"][:4] for r in reg})
    print("%-20s" % "" + "".join("%8s" % a for a in anos))
    for nome, _ in UN:
        if nome == "referencia":
            continue
        L = []
        for a in anos:
            v = [r["referencia" + suf] - r[nome + suf]
                 for r in reg if r["data"][:4] == a]
            L.append(np.median(v) if v else np.nan)
        print("%-20s" % nome + "".join("       ." if np.isnan(x) else "%8.3f" % x
                                       for x in L))
    L = []
    for a in anos:
        v = [r["referencia" + suf] for r in reg if r["data"][:4] == a]
        L.append(np.median(v) if v else np.nan)
    print("%-20s" % "(nivel da referencia)" + "".join(
        "       ." if np.isnan(x) else "%8.3f" % x for x in L))
