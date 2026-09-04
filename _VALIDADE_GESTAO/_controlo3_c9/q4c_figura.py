# -*- coding: utf-8 -*-
"""Q4c - o que a P10 DESENHA: a caixa do MDT sobrepoe-se aos poligonos do B1?
Redesenha a mesma geometria da peca, sem estilo, para se ver a sobreposicao."""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
AQUI = os.path.dirname(os.path.abspath(__file__))

D = json.load(open(os.path.join(VC, "SAIDA_C1", "c1_03_dem50.json"), encoding="utf-8"))
t = D["transform"]
ny, nx = D["shape"]
x0, y0, px = t[2], t[5], t[0]
tr = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)
DX, DY = tr.transform([x0, x0 + nx * px, x0, x0 + nx * px],
                      [y0, y0, y0 - ny * px, y0 - ny * px])
BB = (min(DX), min(DY), max(DX), max(DY))

trw = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
CUL = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
B1 = []
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL:
        g = sht(lambda x, y, z=None: trw.transform(x, y), shape(f["geometry"])).buffer(0)
        B1.append((int(f["properties"]["CUL_ID"]), np.array(list(g.exterior.coords))))

fig, ax = plt.subplots(figsize=(11, 8), dpi=130)
ax.add_patch(Rectangle((BB[0], BB[1]), BB[2] - BB[0], BB[3] - BB[1],
                       facecolor="#dfe9f5", edgecolor="#2a4d80", lw=1.6,
                       ls="--", label="caixa do MDT LiDAR"))
for cid, c in B1:
    dentro = (c[:, 1].max() > BB[1]) and (c[:, 0].max() > BB[0])
    ax.fill(c[:, 0], c[:, 1], facecolor="#eb6834" if dentro else "#9aa0a6",
            alpha=0.55, zorder=3)
    ax.plot(c[:, 0], c[:, 1], color="#111111", lw=0.9, zorder=4)
    ax.text(c[:, 0].mean(), c[:, 1].mean(), str(cid), fontsize=7,
            ha="center", va="center", zorder=5)
ax.axhline(BB[1], color="#2a4d80", lw=1.2)
ax.annotate("", xy=(529700, BB[1]), xytext=(529700, min(cc[:, 1].min() for _, cc in B1)),
            arrowprops=dict(arrowstyle="<->", color="#b00020", lw=1.6))
ax.text(529715, (BB[1] + min(cc[:, 1].min() for _, cc in B1)) / 2,
        "os 445 m da peca:\nbordo do MDT ate ao\nbordo SUL do B1",
        fontsize=9, color="#b00020", va="center")
ax.annotate("", xy=(530200, BB[1]), xytext=(530200, max(cc[:, 1].max() for _, cc in B1)),
            arrowprops=dict(arrowstyle="<->", color="#1a7a3c", lw=1.6))
ax.text(530215, (BB[1] + max(cc[:, 1].max() for _, cc in B1)) / 2,
        "a realidade: o B1 entra\n200 m DENTRO da caixa\n(5,5 ha com cota)",
        fontsize=9, color="#1a7a3c", va="center")
ax.set_xlim(529380, 530600)
ax.set_ylim(4653700, 4654620)
ax.set_aspect("equal")
ax.set_title("Q4 - a caixa do MDT nao esta 445 m a norte do B1: sobrepoe-se a ele",
             fontsize=11)
ax.legend(loc="lower right", fontsize=8)
fig.savefig(os.path.join(AQUI, "q4_sobreposicao.png"), bbox_inches="tight")
print("escrito q4_sobreposicao.png")
