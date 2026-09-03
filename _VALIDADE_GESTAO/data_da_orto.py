# -*- coding: utf-8 -*-
"""A ortofoto de 2025 estava avariada, ou o pomar estava sem folha?

A C2 retirou a G14 porque o NDVI calculado da ortofoto de 2025 sobre copado de
kiwi dava 0,09, «fisicamente impossivel em pleno Verao», e concluiu que a
radiometria da ortofoto nao e interpretavel nem dentro da propria imagem.

Mas o registo SNIG diz que o Lote 1 da campanha ORTOS-2025 foi voado entre
**31/03/2025 e 26/07/2025**. Se a folha de Ganfei for de fim de Marco ou Abril,
o kiwi esta em dormencia ou a abolar, e 0,09 nao e impossivel: e o valor
correcto para uma pergola despida sobre coberto reflector claro.

O teste que separa as duas explicacoes
--------------------------------------
Medir o NDVI da propria ortofoto sobre vegetacao **de folha persistente** na
mesma imagem — pinhal e eucaliptal, que estao verdes em Marco e em Julho.

  se o perene ler alto e o pomar ler baixo  ->  a imagem esta boa e o pomar
                                                estava sem folha. A G14 caiu
                                                por premissa errada.
  se tudo ler baixo                         ->  a radiometria esta avariada e
                                                a C2 tinha razao.
"""
import json
import os
import sys

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]

# amostras de folha persistente e de agua, escolhidas fora do pomar, por
# coordenada, a partir da vista larga: mata a norte e a sul da AOI
ALVOS = [("mata NO", 530150, 4655480, 40),
         ("mata SE", 531500, 4654750, 40),
         ("mata S",  530700, 4654680, 40),
         ("rio Minho", 530300, 4655560, 30)]

for ep, fich in (("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"),
                 ("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")):
    ds = rasterio.open(os.path.join(RAIZ, "orto", fich))
    print("\n=== ortofoto de %s ===" % ep)

    def nd_em(x, y, r):
        b = transform_bounds("EPSG:32629", ds.crs, x - r, y - r, x + r, y + r)
        w = from_bounds(*b, transform=ds.transform)
        red = ds.read(1, window=w).astype("float32")
        nir = ds.read(4, window=w).astype("float32")
        v = (nir - red) / (nir + red + 1e-6)
        return float(np.median(v)), int(v.size)

    for nome, x, y, r in ALVOS:
        v, n = nd_em(x, y, r)
        print("  %-12s NDVI-orto %+.3f   (%d px)" % (nome, v, n))

    # o pomar, pela mascara
    b = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*b, transform=ds.transform)
    red = ds.read(1, window=w).astype("float32")
    nir = ds.read(4, window=w).astype("float32")
    v = (nir - red) / (nir + red + 1e-6)
    H, L = v.shape
    ys, xs = np.where(REF)
    am = []
    for yy, xx in zip(ys, xs):
        cy, cx = int((yy + .5) * H / NL), int((xx + .5) * L / NC)
        if 10 < cy < H - 10 and 10 < cx < L - 10:
            am.append(np.median(v[cy - 10:cy + 10, cx - 10:cx + 10]))
    print("  %-12s NDVI-orto %+.3f   (%d celulas)"
          % ("REFERENCIA", np.median(am), len(am)))
