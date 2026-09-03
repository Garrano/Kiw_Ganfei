# -*- coding: utf-8 -*-
"""CTRL-18. Distancias ao POLIGONO `pomar`, nao a caixa envolvente.

O enunciado da o pomar do caso por uma caixa E 530150-531520 / N 4654870-
4655450. Essa caixa tem 79,5 ha e 19 % dela e agua do rio. As distancias uteis
sao ao poligono `pomar` de masks.json (28,97 ha), que e o que ali esta plantado.

Bordo a bordo com os dois contornos densificados a 4 m. Nao le nenhum indice.
"""
import json
import os
import numpy as np

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)

masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
q = np.array(masks["pomar"], float)
POM = np.column_stack([AOI[0] + q[:, 0] * 10.0, AOI[3] - q[:, 1] * 10.0])


def densifica(p, passo=4.0):
    out = []
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        t = np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / passo) + 1))
        out.append(a + (b - a) * t[:, None])
    return np.vstack(out)


PD = densifica(POM)
CP = POM.mean(0)
gj = json.load(open(os.path.join(OUT, "controlos.geojson"), encoding="utf-8"))
print("centroide do poligono `pomar`: E %.0f  N %.0f" % (CP[0], CP[1]))
print("%-5s %10s %12s %14s" % ("id", "area_ha", "d_bordo_m", "d_centroide_m"))
res = {}
for f in gj["features"]:
    if f["properties"]["id"] == "REF":
        continue
    p = np.array(f["geometry"]["coordinates"][0])
    D = densifica(p)
    d = np.hypot(D[:, 0][:, None] - PD[:, 0][None, :],
                 D[:, 1][:, None] - PD[:, 1][None, :]).min()
    c = np.hypot(p[:, 0].mean() - CP[0], p[:, 1].mean() - CP[1])
    print("%-5s %10.2f %12.0f %14.0f"
          % (f["properties"]["id"], f["properties"]["area_ha"], d, c))
    res[f["properties"]["id"]] = dict(d_bordo_pomar_m=round(float(d)),
                                      d_centroide_pomar_m=round(float(c)))
json.dump(res, open(os.path.join(OUT, "ctrl_18_distancias.json"), "w"),
          indent=1)
print("-> ctrl_18_distancias.json")
