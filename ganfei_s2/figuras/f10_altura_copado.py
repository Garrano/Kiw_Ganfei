# -*- coding: utf-8 -*-
"""F10 — o mapa que separa o caso em dois.

O que a figura tem de fazer
---------------------------
O dossie tratou durante semanas «dois focos de declinio» como se fossem a mesma
coisa. O LiDAR de 06-07-2025 mostra que nao sao: num ha pergola e videira viva;
no outro, metade e chao. **Esta e a figura que justifica a correccao**, e nunca
existiu.

O instrumento e independente de tudo o resto: MDS menos MDT do voo LiDAR da DGT.
Mede geometria, nao reflectancia. Todo o resto do dossie mede reflectancia.

Forma
-----
Um mapa, uma grandeza — altura de copado. Rampa **sequencial de uma so cor**,
claro para escuro, porque a grandeza e magnitude. A unica excepcao de cor e a
faixa abaixo de 0,5 m, que leva uma cor **de estatuto** distinta e um rotulo
directo, porque nao e «pouca altura»: e **ausencia de planta**, que e outra
categoria. Identidade nunca so por cor — os dois focos levam rotulo e contorno.

A escala esta ancorada em dois controlos medidos no proprio voo, nao escolhidos:
terreno lavrado le 0,09 m; a referencia sistematica le 2,34 m.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Rectangle

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
H = np.load(os.path.join(VG, "chm_altura.npy"))
FOCOS = json.load(open(os.path.join(VG, "altura_focos.json")))

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#8d8a84"
FUNDO = "#fbfbfa"
SEM = "#D55E00"          # Okabe-Ito vermillion — estatuto, nao magnitude
OESTE, ESTE = "#0072B2", "#D55E00"

# rampa sequencial de uma so cor, do claro ao escuro
verde = LinearSegmentedColormap.from_list(
    "copado", ["#f2f5ef", "#cfe0c8", "#97c088", "#5c9b52", "#2f6b32", "#1b4322"])

M = np.where(POMAR, H, np.nan)
sem = POMAR & np.isfinite(H) & (H < 0.5)

fig = plt.figure(figsize=(13.6, 8.2), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.045, 0.135, 0.70, 0.70])
axl = fig.add_axes([0.775, 0.135, 0.195, 0.70]); axl.axis("off")

ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
ax.imshow(np.where(POMAR, 1.0, np.nan), extent=ext, cmap="Greys",
          vmin=0, vmax=1, alpha=0.06, interpolation="nearest")
im = ax.imshow(M, extent=ext, cmap=verde, vmin=0, vmax=2.6,
               interpolation="nearest")
ax.imshow(np.where(sem, 1.0, np.nan), extent=ext, cmap=matplotlib.colors
          .ListedColormap([SEM]), vmin=0, vmax=1, interpolation="nearest")

# contorno do poligono
from scipy import ndimage
b = POMAR ^ ndimage.binary_erosion(POMAR)
ys, xs = np.where(b)
ax.plot(AOI[0] + (xs + .5) * PASSO, AOI[3] - (ys + .5) * PASSO, ".",
        ms=0.7, color=TINTA2, alpha=0.55)

POS = {"foco OESTE da cadeia": (0, 118, "bottom"),
       "foco ESTE da cadeia": (0, -128, "top")}
for (x, y), cor, nome, k in ((FOCO_OESTE, OESTE, "foco OESTE", "foco OESTE da cadeia"),
                             (FOCO_ESTE, ESTE, "foco ESTE", "foco ESTE da cadeia")):
    ax.add_patch(Circle((x, y), 90, fill=False, ec=cor, lw=2.4, zorder=6))
    d = FOCOS[k]
    dx, dy, va = POS[k]
    txt = ("%s   E%.0f N%.0f\n%s m  ·  %.0f %% acima de 1,5 m"
           % (nome, x, y, ("%.2f" % d["altura"]).replace(".", ","), d["frac"]))
    ax.annotate(txt, (x + dx, y + dy), ha="center", va=va, fontsize=9.8,
                color=cor, fontweight="bold", linespacing=1.6, zorder=8,
                bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=cor,
                          lw=1.1, alpha=0.94))
    ax.plot([x, x + dx], [y + (92 if dy > 0 else -92), y + dy * 0.72],
            color=cor, lw=1.0, alpha=0.7, zorder=6)

ry, rx = np.where(REF)
ax.plot(AOI[0] + (rx + .5) * PASSO, AOI[3] - (ry + .5) * PASSO, "s",
        ms=1.9, color="#333333", alpha=0.75, zorder=5)

ax.set_xlim(AOI[0] + 120, AOI[2] - 300); ax.set_ylim(AOI[1] + 175, AOI[3] - 120)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.plot([AOI[0] + 200, AOI[0] + 400], [AOI[1] + 215, AOI[1] + 215],
        color=TINTA, lw=2.6, solid_capstyle="butt")
ax.text(AOI[0] + 300, AOI[1] + 227, "200 m", ha="center", va="bottom",
        fontsize=8.6, color=TINTA)

# ---------------------------------------------------------------- legenda
cax = fig.add_axes([0.79, 0.50, 0.022, 0.30])
cb = fig.colorbar(im, cax=cax)
cb.set_ticks([0, 0.5, 1.5, 2.34, 2.6])
cb.set_ticklabels(["0", "0,5", "1,5", "2,34", ""])
cb.ax.tick_params(labelsize=8.4, colors=TINTA2, length=2)
cb.outline.set_visible(False)
axl.text(0.30, 0.815, "altura de copado\nMDS − MDT  (m)", fontsize=9.4,
         color=TINTA, va="bottom", linespacing=1.5, fontweight="bold")

axl.plot([0.02, 0.14], [0.487, 0.487], lw=9, color=SEM, solid_capstyle="butt")
axl.text(0.19, 0.487, "abaixo de 0,5 m\nSEM PÉRGOLA", fontsize=9,
         color=SEM, va="center", linespacing=1.5, fontweight="bold")
axl.plot([0.08], [0.415], "s", ms=4.5, color="#333333")
axl.text(0.19, 0.415, "referência sistemática\n110 células · 2,34 m",
         fontsize=8.6, color=TINTA2, va="center", linespacing=1.5)

axl.text(0.02, 0.330, "ESCALA ANCORADA", fontsize=8.8, color=TINTA,
         fontweight="bold", va="top")
axl.text(0.02, 0.288,
         "0,09 m   terreno lavrado\n"
         "2,34 m   referência sistemática\n"
         "1,8–2,5  pérgola de kiwi",
         fontsize=8.4, color=TINTA2, va="top", linespacing=1.85)
axl.text(0.02, 0.172, "os dois primeiros são medidos no próprio voo",
         fontsize=7.8, color=TINTA3, va="top", style="italic")

axl.plot([0.02, 0.98], [0.128, 0.128], lw=0.9, color="#dedbd5")
axl.text(0.02, 0.082, "3,77 ha de 30,31", fontsize=14.5, color=SEM,
         fontweight="bold", va="bottom")
axl.text(0.02, 0.070, "do polígono não tinham pérgola\nnenhuma nesse dia",
         fontsize=8.6, color=TINTA2, va="top", linespacing=1.55)
axl.set_xlim(0, 1); axl.set_ylim(0, 1)

# --------------------------------------------------------------- titulo
fig.text(0.045, 0.945, "Os dois focos não são a mesma coisa",
         fontsize=19, fontweight="bold", color=TINTA)
fig.text(0.045, 0.900,
         "Altura de copado medida por LiDAR em 6 de Julho de 2025, às 14h35 UTC. "
         "Mede geometria, não reflectância — tudo o resto do dossiê mede reflectância.",
         fontsize=10.6, color=TINTA2)
fig.text(0.045, 0.866,
         "No foco ocidental há pérgola e videira viva. No oriental, metade é chão.",
         fontsize=10.6, color=TINTA, fontweight="bold")

fig.text(0.045, 0.055,
         "Voo LiDAR da DGT, folhas LO-158565 e LO-159565, 16,6 e 17,8 milhões de pontos.  "
         "A data vem do tempo GPS dos pontos, não dos metadados, que dão uma janela inútil de catorze meses.\n"
         "O voo cai DENTRO da janela em análise: não distingue «nunca teve pérgola» de «teve até Julho de 2024». "
         "Estabelece o que lá estava naquele dia, não a sua história.\n"
         "Confirmação por documento independente: onde o LiDAR não vê pérgola, o beneficiário declarou ao IFAP erva, forragem ou nada — "
         "65 % de kiwi contra 99,4 % na parte com pérgola.",
         fontsize=7.8, color=TINTA3, linespacing=1.8, va="top")

fig.savefig(os.path.join(AQUI, "F10_altura_copado.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
fig.savefig(os.path.join(AQUI, "F10_altura_copado.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
print("escrito F10_altura_copado")
