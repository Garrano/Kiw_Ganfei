# -*- coding: utf-8 -*-
"""Recortes da ortofoto de 2025 a 25 cm — o instrumento independente e o olho.

A periodicidade diz que a estrutura esta la mas enfraquecida. E um algoritmo a
dizer. Um recorte a 25 cm mostra directamente se ha fileiras, e distingue o que
o algoritmo nao distingue: fileira arrancada (solo limpo, sem postes) de
copado ralo (postes, arames e fileira visivel, folhagem escassa).

Quatro janelas de 80 m, todas da MESMA imagem — nao ha comparacao de brilho
entre epocas, que a cadeia ja proibiu.
"""
import os
import sys

import numpy as np
import rasterio
from PIL import Image
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool)


def centro(m):
    ys, xs = np.where(m)
    return (AOI[0] + (xs.mean() + 0.5) * PASSO,
            AOI[3] - (ys.mean() + 0.5) * PASSO)


# o nucleo mais denso do declinio novo, nao o centroide de uma mancha dispersa
den = ndimage.uniform_filter(novo.astype(float), 5)
yy, xx = np.unravel_index(np.argmax(den * novo), novo.shape)
ALVOS = [("A_declinio_novo_nucleo",
          (AOI[0] + (xx + .5) * PASSO, AOI[3] - (yy + .5) * PASSO)),
         ("B_foco_OESTE", (530485.0, 4655053.0)),
         ("C_foco_ESTE", (530977.0, 4655117.0)),
         ("D_referencia", centro(REF))]

LADO = 80.0
for ep, fich in [("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"),
                 ("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif")]:
    ds = rasterio.open(os.path.join(RAIZ, "orto", fich))
    for nome, (x, y) in ALVOS:
        b = transform_bounds("EPSG:32629", ds.crs,
                             x - LADO / 2, y - LADO / 2, x + LADO / 2, y + LADO / 2)
        w = from_bounds(*b, transform=ds.transform)
        rgb = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("uint8")
        im = Image.fromarray(rgb).resize((480, 480), Image.LANCZOS)
        f = os.path.join(AQUI, "%s_%s.png" % (nome, ep))
        im.save(f)
        print("%s  %s  E%.0f N%.0f  %dx%d px" % (ep, nome, x, y, *rgb.shape[:2]))
