# -*- coding: utf-8 -*-
"""P14 — mapa D do email: os 2,20 ha que perderam copado entre Jul-2024 e Jul-2025.

A prancha existe para fazer UMA pergunta ao gestor — «o que aconteceu aqui?» —
e para separar visualmente duas coisas que o processo andou meses a confundir:

  · 2,20 ha que TINHAM copado em Julho de 2024, ao nivel do pomar (NDVI 0,829
    contra 0,898), e que em Julho de 2025 nao tinham nenhum;
  · 1,57 ha que NUNCA tiveram copado nesta decada (NDVI de Julho ~0,59).

Os 3,77 ha que o `altura_copado.py` publica sao a soma dos dois, e o ficheiro
nao os separa. So o segundo grupo e que e perda.

O INSTRUMENTO, e porque se pode confiar nele
--------------------------------------------
Altura de copado por LiDAR aereo: MDS menos MDT, limiar de 0,5 m, voo datado de
06-07-2025 (uma so data, verificada nas duas folhas LAZ). E o unico instrumento
deste caso que mede GEOMETRIA e nao reflectancia, e foi certificado e atacado a
06-09 (AUD-17): reproduzido dos ladrilhos brutos a diferenca 0,000e+00.

A RESSALVA QUE VIAJA COM A PRANCHA
-----------------------------------
O LiDAR mede FOLHA, nao estrutura. Uma pergola nua — postes e arame — move a
estatistica em 0,018 contra um desvio entre celulas de 0,135, sete vezes abaixo.
**Isto mostra onde o copado desapareceu; nao diz se a instalacao ficou de pe.**
E exactamente por isso que a pergunta vai ao gestor.
"""
import io
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "base"))
from carta_base import (cartela_institucional, fontes, Base, PAPEL, TINTA,  # noqa
                        TINTA2, TINTA3, virg)

S2 = os.path.join(AQUI, "..")
VG = r"C:/Users/Jackster2/Downloads/_VALIDADE_GESTAO"
AOI = (529950.0, 4654600.0, 531950.0, 4655600.0)      # a grelha das mascaras

g = json.load(io.open(os.path.join(S2, "sentinel", "masks_geograficas.json"),
                      encoding="utf-8"))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POM, NU = bits("pomar_bits"), bits("nu2021_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
SEM = POM & (h < 0.5)
PERDA = SEM & ~NU          # tinha copado em 2024 e nao tem em 2025
NUNCA = SEM & NU           # nunca teve nesta decada

COR_PERDA, COR_NUNCA = "#C4342B", "#8A8378"

b = Base()
fig, ax, axl = b.figura(larg=16.0, rodape=0.72)
ytop = cartela_institucional(fig)

b.terreno(ax)
b.cadastro(ax)
b.sectores(ax, alfa=0.20)
b.rotulos(ax)
b.toponimos(ax)


def pinta(m, cor, z, alfa=0.88):
    rgba = np.zeros(m.shape + (4,), float)
    c = matplotlib.colors.to_rgb(cor)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = c
    rgba[..., 3] = np.where(m, alfa, 0.0)
    ax.imshow(rgba, extent=(AOI[0], AOI[2], AOI[1], AOI[3]), origin="upper",
              interpolation="nearest", zorder=6)


pinta(NUNCA, COR_NUNCA, 6, 0.62)
pinta(PERDA, COR_PERDA, 7, 0.90)
# ── reparticao por sector: e assim que o gestor pensa, e nao em indices ─────
inv = {v: k for k, v in b.COD.items()}
col = ((np.meshgrid(AOI[0] + (np.arange(200) + .5) * 10.,
                    AOI[3] - (np.arange(100) + .5) * 10.)[0] - b.bb[0]) / b.pix
       ).astype(int)
row = ((b.bb[3] - np.meshgrid(AOI[0] + (np.arange(200) + .5) * 10.,
                              AOI[3] - (np.arange(100) + .5) * 10.)[1]) / b.pix
       ).astype(int)
ok = (row >= 0) & (row < b.SEC.shape[0]) & (col >= 0) & (col < b.SEC.shape[1])
sec = np.zeros_like(row)
sec[ok] = b.SEC[row[ok], col[ok]]
REP = []
for c, nome in sorted(inv.items()):
    pp = (PERDA & (sec == c)).sum() / 100.0
    nn = (NUNCA & (sec == c)).sum() / 100.0
    if pp >= 0.005 or nn >= 0.005:
        REP.append((nome, pp, nn))
REP.append(("fora da partição", (PERDA & (sec == 0)).sum() / 100.0,
            (NUNCA & (sec == 0)).sum() / 100.0))

b.moldura(ax)

fig.text(0.035, ytop, "ONDE DESAPARECERAM AS PLANTAS", fontsize=23,
         weight="bold", color=TINTA, va="top", ha="left")
fig.text(0.035, ytop - 0.31 / fig.get_figheight(),
         "Emparcelamento de Ganfei, Valença",
         fontsize=10.5, color=TINTA2, va="top", ha="left")
fig.text(0.955, ytop - (21 - 10.5) * 0.70 / 72 / fig.get_figheight(),
         "%s ha perderam as plantas  ·  %s ha nunca as tiveram"
         % (virg(PERDA.sum() / 100.0, 2), virg(NUNCA.sum() / 100.0, 2)),
         fontsize=10.5, color=TINTA2, va="top", ha="right")
fig.text(0.955, ytop - (21 - 10.5) * 0.70 / 72 / fig.get_figheight() - 0.026,
         "entre Julho de 2024 e Julho de 2025",
         fontsize=8.6, color=TINTA3, va="top", ha="right")

# ── legenda ─────────────────────────────────────────────────────────────────
axl.set_xlim(0, 1); axl.set_ylim(0, 1); axl.axis("off")
axl.text(0.02, 0.975, "A PERGUNTA", fontsize=9.0, weight="bold", color=TINTA,
         va="top", ha="left", transform=axl.transAxes)
axl.text(0.02, 0.938,
         "O que aconteceu nas manchas\na vermelho?",
         fontsize=9.2, color=TINTA, va="top", ha="left",
         transform=axl.transAxes, linespacing=1.55)

y0 = 0.855
for cor, alfa, tit, sub in (
        (COR_PERDA, 0.90, "%s ha  ·  perderam as plantas" % virg(PERDA.sum() / 100.0, 2),
         "tinham plantas em 2024.\nEm 2025, nenhuma."),
        (COR_NUNCA, 0.62, "%s ha  ·  nunca as tiveram" % virg(NUNCA.sum() / 100.0, 2),
         "sem plantas em toda a década.")):
    axl.add_patch(plt.Rectangle((0.03, y0 - 0.030), 0.075, 0.034,
                                transform=axl.transAxes, facecolor=cor,
                                alpha=alfa, edgecolor="none", zorder=3))
    axl.text(0.125, y0 - 0.013, tit, fontsize=8.0, weight="bold", color=TINTA,
             ha="left", va="center", transform=axl.transAxes)
    axl.text(0.125, y0 - 0.048, sub, fontsize=7.2, color=TINTA2, ha="left",
             va="top", transform=axl.transAxes, linespacing=1.5)
    y0 -= 0.145

axl.text(0.02, 0.545, "ONDE, POR SECTOR", fontsize=9.0, weight="bold",
         color=TINTA, va="top", ha="left", transform=axl.transAxes)
_l = ["%-16s %6s %6s" % ("", "perdeu", "nunca")]
for _n, _p, _q in REP:
    _l.append("%-16s %6s %6s" % (_n[:16], virg(_p, 2), virg(_q, 2)))
_l.append("-" * 30)
_l.append("%-16s %6s %6s" % ("total (ha)", virg(PERDA.sum() / 100., 2),
                             virg(NUNCA.sum() / 100., 2)))
axl.text(0.02, 0.508, "\n".join(_l),
         fontsize=6.8, color=TINTA, va="top", ha="left", family="monospace",
         transform=axl.transAxes, linespacing=1.62)

fontes(fig, ["altura das plantas: LiDAR DGT, voo de 06-07-2025",
             "modelo de terreno LiDAR 50 cm, DGT",
             "parcelário IFAP 2025",
             "comparação 2024/2025: Sentinel-2"], y=0.012)

out = os.path.join(AQUI, "P14_perda_de_copado.png")
fig.savefig(out, dpi=200, facecolor=PAPEL)
print("perderam %.2f ha  ·  nunca tiveram %.2f ha  ·  total %.2f ha"
      % (PERDA.sum() / 100.0, NUNCA.sum() / 100.0, SEM.sum() / 100.0))
print("escrito %s" % out)
