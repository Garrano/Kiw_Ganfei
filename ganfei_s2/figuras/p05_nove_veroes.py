# -*- coding: utf-8 -*-
"""P05 — nove verões, a mesma escala. O leitor vê o degrau com os olhos.

O que esta peça faz que a P03 não faz
-------------------------------------
A P03 prova o degrau com números e com um controlo. Esta mostra-o **sem
números**, e mostra uma coisa que uma serie temporal nao pode mostrar: **onde**.

Um chefe que veja nove mapas iguais em escala, e nos dois ultimos veja duas
manchas escuras aparecer em sitios que estavam claros oito anos, nao precisa
de p nenhum para perceber o que aconteceu. E o unico argumento da apresentacao
que nao depende de aceitar um metodo.

As tres regras que fazem isto valer alguma coisa
------------------------------------------------
1. **Uma so rampa, uma so barra de cor, os mesmos limites nos nove.** Se cada
   painel normalizasse pela sua propria cena, os nove ficavam parecidos e a
   figura mentia. Os limites sao fixos e estao impressos.
2. **A mesma extensao geografica nos nove.** Nenhum painel esta ampliado.
3. **Rampa de UM tom, claro para escuro.** Nada de arco-iris: numa escala
   sequencial o arco-iris inventa fronteiras onde os dados nao as tem.

A area de defice por baixo de cada painel e calculada, nao transcrita, e usa a
definicao publicada — abaixo da referencia da propria cena menos 0,05, com a
abertura morfologica 2x2 a correr UMA VEZ sobre o poligono.

Ressalva que vai impressa
-------------------------
A area de defice usa a referencia, e a referencia tem catorze celulas dentro
dos focos. Por isso a area esta **subestimada** em todos os anos, e o numero
serve para comparar anos entre si, nao como area absoluta. O mapa em si — a
cor — e nivel absoluto e nao depende da referencia.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy import ndimage

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
nd = {d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}

ny, nx = POMAR.shape
ys, xs = np.where(POMAR)
M = 6
r0, r1 = max(ys.min() - M, 0), min(ys.max() + M + 1, ny)
c0, c1 = max(xs.min() - M, 0), min(xs.max() + M + 1, nx)
EXT = (AOI[0] + c0 * 10, AOI[0] + c1 * 10, AOI[3] - r1 * 10, AOI[3] - r0 * 10)

C_OC = (530485.0, 4655053.0)
C_OR = (530999.0, 4655102.0)

AZUL, LARANJA = "#2a78d6", "#eb6834"
TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO = "#fcfcfb"

# rampa de UM tom, claro -> escuro. Sequencial: nada de arco-iris.
RAMPA = LinearSegmentedColormap.from_list(
    "verdura", ["#f7f3e8", "#dfe6c8", "#b9cf9a", "#84ac6b", "#4e8447",
                "#265c2f", "#0f3520"])
VMIN, VMAX = 0.45, 0.95
norm = Normalize(VMIN, VMAX)

fig = plt.figure(figsize=(14.6, 9.2), dpi=200)
fig.patch.set_facecolor(FUNDO)

L, B, W, H = 0.040, 0.098, 0.288, 0.183
GX, GY = 0.014, 0.055

areas = {}
for i, d in enumerate(DATAS):
    r, c = divmod(i, 3)
    ax = fig.add_axes([L + c * (W + GX), B + (2 - r) * (H + GY), W, H])
    a = nd[d]
    ref = float(np.nanmean(a[REF]))
    dfc = ndimage.binary_opening((a < ref - 0.05) & POMAR, np.ones((2, 2)))
    areas[d] = dfc.sum() / 100.0

    campo = np.where(POMAR, a, np.nan)[r0:r1, c0:c1]
    ax.imshow(np.where(POMAR, 0.0, np.nan)[r0:r1, c0:c1], extent=EXT,
              cmap=LinearSegmentedColormap.from_list("g", ["#eceae5", "#eceae5"]),
              vmin=0, vmax=1, interpolation="nearest")
    ax.imshow(campo, extent=EXT, cmap=RAMPA, norm=norm, interpolation="nearest")

    tardio = d >= "2025"
    for (e, n_), cor, mk in ((C_OC, AZUL, "o"), (C_OR, LARANJA, "D")):
        ax.plot([e], [n_], mk, ms=8.5 if tardio else 6.5, mfc="none", mec=cor,
                mew=2.2 if tardio else 1.4,
                alpha=1.0 if tardio else 0.55)

    ax.set_xlim(EXT[0], EXT[1]); ax.set_ylim(EXT[2], EXT[3])
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#2a2a2a" if tardio else "#dcd9d3")
        s.set_linewidth(1.8 if tardio else 0.8)

    ax.text(0.012, 1.075, d[:4], transform=ax.transAxes, fontsize=14,
            fontweight="bold", color=TINTA if tardio else TINTA2, va="top")
    ax.text(0.175, 1.062, d[8:10] + "-" + d[5:7], transform=ax.transAxes,
            fontsize=8.6, color=TINTA3, va="top")
    ax.text(1.0, 1.068, "défice  %s ha" % ("%.2f" % areas[d]).replace(".", ","),
            transform=ax.transAxes, fontsize=9.2, ha="right", va="top",
            color=TINTA if tardio else TINTA3,
            fontweight="bold" if tardio else "normal")

# ------------------------------------------------------ barra de cor, única
axc = fig.add_axes([0.925, 0.098, 0.016, 0.607])
grad = np.linspace(VMAX, VMIN, 256).reshape(-1, 1)
axc.imshow(grad, aspect="auto", cmap=RAMPA, norm=norm,
           extent=(0, 1, VMIN, VMAX))
axc.set_xticks([])
axc.yaxis.tick_right()
axc.set_ylim(VMIN, VMAX)
axc.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9])
axc.set_yticklabels(["0,5", "0,6", "0,7", "0,8", "0,9"], fontsize=8.8,
                    color=TINTA2)
for s in axc.spines.values():
    s.set_color("#dcd9d3")
axc.text(0.5, 1.028, "NDVI", transform=axc.transAxes, ha="center",
         fontsize=9.2, color=TINTA, fontweight="bold")
axc.text(-0.6, 0.5, "a MESMA escala nos nove painéis", transform=axc.transAxes,
         rotation=90, ha="center", va="center", fontsize=8.4, color=TINTA3)

# ---------------------------------------------------------------- legenda
# A legenda vai ACIMA da grelha: dentro do primeiro painel tapava o mapa que a
# peca existe para mostrar.
axl = fig.add_axes([0.040, 0.828, 0.42, 0.001]); axl.axis("off")
axl.set_xlim(0, 1); axl.set_ylim(-1, 1)
axl.plot([0.006], [0], "o", ms=8.5, mfc="none", mec=AZUL, mew=2.2,
         clip_on=False)
axl.text(0.030, 0, "foco OCIDENTAL  ·  E≈530 485", fontsize=9.2, color=AZUL,
         va="center")
axl.plot([0.425], [0], "D", ms=8.5, mfc="none", mec=LARANJA, mew=2.2,
         clip_on=False)
axl.text(0.452, 0, "foco ORIENTAL  ·  E≈530 999", fontsize=9.2, color=LARANJA,
         va="center")
axl.text(0.815, 0, "moldura grossa = as duas épocas do acontecimento",
         fontsize=8.6, color=TINTA3, va="center")

# ------------------------------------------------------------------ titulo
fig.text(0.040, 0.962, "Nove verões, a mesma escala",
         fontsize=23.5, fontweight="bold", color=TINTA)
fig.text(0.040, 0.922,
         "O mesmo pomar, a mesma extensão, a mesma rampa de cor e os mesmos limites nos nove painéis. "
         "Nada foi normalizado por cena.",
         fontsize=11.4, color=TINTA2)
fig.text(0.040, 0.885,
         "Oito anos sem nada nos dois círculos. Depois, dois.",
         fontsize=11.4, color=TINTA, fontweight="bold")

fig.text(0.040, 0.068,
         "UMA SÓ RAMPA, UMA SÓ BARRA, LIMITES FIXOS (0,45–0,95). Se cada painel normalizasse pela sua própria cena, os nove ficavam parecidos e a figura mentia. Rampa de um tom, claro para escuro — "
         "num mapa sequencial o arco-íris inventa fronteiras que os dados não têm.\n"
         "OS CÍRCULOS SÃO GEOGRÁFICOS e estão no mesmo sítio nos nove painéis: não seguem o sinal. Cinzento = fora do polígono do pomar. 2019 e 2025-06 saem da série por fenologia, não por resultado.\n"
         "A ÁREA DE DÉFICE por baixo de cada painel é calculada (abaixo da referência da própria cena menos 0,05, abertura 2×2 uma vez sobre o polígono), e usa a referência — que tem catorze células dentro dos focos.\n"
         "Está por isso SUBESTIMADA em todos os anos, e serve para comparar anos entre si, não como área absoluta. A cor do mapa é nível absoluto e não depende da referência.",
         fontsize=7.9, color=TINTA3, linespacing=1.9, va="top")

fig.savefig(os.path.join(AQUI, "P05_nove_veroes.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "P05_nove_veroes.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito P05 — nove verões")
for d in DATAS:
    print("  %s  défice %5.2f ha" % (d, areas[d]))
