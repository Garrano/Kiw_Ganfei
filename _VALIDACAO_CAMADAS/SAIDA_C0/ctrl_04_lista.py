# -*- coding: utf-8 -*-
"""CTRL-04. Relista os candidatos de estrutura a limiar mais baixo (p93).

Le ctrl_02_forca.npy — nao recalcula, nao le NDVI.
"""
import json
import os
import numpy as np
from scipy import ndimage

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
j = json.load(open(os.path.join(OUT, "ctrl_02_periodicidade.json")))
JAN = j["janela"]
RES, BL, STEP = j["res"], j["bloco_px"], j["passo_px"]
forca = np.load(os.path.join(OUT, "ctrl_02_forca.npy"))
lamb = np.load(os.path.join(OUT, "ctrl_02_lambda.npy"))
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
CX, CY = (CASO[0] + CASO[2]) / 2, (CASO[1] + CASO[3]) / 2

lim = np.percentile(forca[forca > 0], 93.0)
m = forca >= lim
m = ndimage.binary_closing(m, np.ones((3, 3)))
m = ndimage.binary_opening(m, np.ones((2, 2)))
lab, n = ndimage.label(m, np.ones((3, 3)))
tam = ndimage.sum(m, lab, range(1, n + 1)) * (STEP * RES) ** 2 / 1e4
print("limiar p93 = %.4f ; %d componentes" % (lim, n))
print("%-5s %8s  %-28s %-28s %8s %6s" % ("id", "ha_bruta", "E", "N", "dist_m", "lam"))
k = 0
for idx in np.argsort(tam)[::-1]:
    if tam[idx] < 0.6:
        break
    k += 1
    mm = lab == idx + 1
    ys, xs = np.where(mm)
    e0 = JAN[0] + (xs.min() * STEP + BL / 2) * RES
    e1 = JAN[0] + (xs.max() * STEP + BL / 2) * RES
    n1 = JAN[3] - (ys.min() * STEP + BL / 2) * RES
    n0 = JAN[3] - (ys.max() * STEP + BL / 2) * RES
    ec, nc = (e0 + e1) / 2, (n0 + n1) / 2
    d = np.hypot(ec - CX, nc - CY)
    print("Q%02d %8.2f  %-28s %-28s %8.0f %6.1f"
          % (k, tam[idx], "%.0f..%.0f" % (e0, e1), "%.0f..%.0f" % (n0, n1),
             d, float(np.median(lamb[mm]))))
