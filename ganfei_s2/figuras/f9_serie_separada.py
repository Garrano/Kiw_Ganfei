# -*- coding: utf-8 -*-
"""F9 — a serie do defice separada pelo LiDAR de 06-07-2025.  VERSAO 2.

Porque houve versao 2
---------------------
A versao 1 publicava «zero em 2022, 2023 e 2024» no copado vivo. **Era um
artefacto**, apanhado pelo adversario e confirmado: `mapa_defice` aplica a
abertura morfologica 2x2 DEPOIS de intersectar com a mascara recebida, portanto
calcular o defice dentro de um subconjunto nao e o mesmo que calcula-lo no
poligono e dividir depois. A costura perdia 15 a 41 % do defice, e os tres anos
que liam zero eram precisamente os de maior perda.

**Correccao:** a abertura corre UMA VEZ sobre o poligono inteiro, como na serie
publicada, e o mapa de defice resultante e que se divide pela particao do
LiDAR. As duas partes somam agora exactamente o total, em todas as cenas.

O piso real e 0,66-0,67 ha em 2023-2024, e o evento e uma multiplicacao por
7,0 em dois anos. E uma afirmacao mais fraca que «parte de zero» e e a
verdadeira.

Forma: tres linhas num so eixo, nao empilhadas. Cor Okabe-Ito, segura para
daltonismo; identidade reforcada por marcador e rotulo directo, nunca so por cor.
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
from matplotlib.lines import Line2D

AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
D = json.load(open(r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO\serie_separada_v2.json"))
datas = sorted(D)
x = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12.0 for d in datas])
viv = np.array([D[d]["vivo"] for d in datas])
lim = np.array([D[d]["limpo"] for d in datas])
tot = np.array([D[d]["total"] for d in datas])

AZUL, VERM, CINZ = "#0072B2", "#D55E00", "#9AA0A6"
TINTA, TINTA2 = "#1a1a1a", "#5f6368"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.linewidth": 0.8})
fig, ax = plt.subplots(figsize=(10.4, 6.0), dpi=200)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")

i23, i24, i26 = datas.index("2023-08-07"), datas.index("2024-07-22"), datas.index("2026-07-27")
ax.axvspan(x[i23] - 0.45, x[i24] + 0.45, color=AZUL, alpha=0.05, lw=0)
ax.annotate("", xy=(x[i26], viv[i26]), xytext=(x[i24], viv[i24]),
            arrowprops=dict(arrowstyle="-", lw=7, color=AZUL, alpha=0.13))
ax.text(2025.5, 2.45, "\u00d77,0 em dois anos", fontsize=10.5, color=AZUL,
        fontweight="bold", ha="center", rotation=52)

ax.plot(x, tot, "-", color=CINZ, lw=1.4, zorder=2)
ax.plot(x, tot, "o", color=CINZ, ms=4.2, mec="white", mew=1.2, zorder=3)
ax.plot(x, lim, "-", color=VERM, lw=2.0, zorder=4)
ax.plot(x, lim, "s", color=VERM, ms=6.0, mec="white", mew=1.4, zorder=5)
ax.plot(x, viv, "-", color=AZUL, lw=2.6, zorder=6)
ax.plot(x, viv, "o", color=AZUL, ms=7.0, mec="white", mew=1.5, zorder=7)

ax.annotate("4,66 ha", (x[-1], viv[-1]), xytext=(10, 2), textcoords="offset points",
            color=AZUL, fontsize=11, fontweight="bold", va="center")
ax.annotate("3,20 ha", (x[-1], lim[-1]), xytext=(10, 0), textcoords="offset points",
            color=VERM, fontsize=10, va="center")
ax.annotate("7,86 ha", (x[-1], tot[-1]), xytext=(10, 0), textcoords="offset points",
            color=CINZ, fontsize=9.5, va="center")
ax.annotate("piso 0,66 \u2013 0,67 ha", (x[i23], viv[i23]), xytext=(0, -20),
            textcoords="offset points", color=AZUL, fontsize=9, ha="center")

ax.axvline(2025.51, color=TINTA2, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax.text(2025.44, 8.5, "LiDAR  06-07-2025\na partição vem daqui", rotation=90,
        ha="right", va="top", fontsize=7.6, color=TINTA2, linespacing=1.4)

ax.set_xlim(2016.6, 2027.35); ax.set_ylim(-0.45, 9.0)
porano = {}
for xi, d in zip(x, datas):
    porano.setdefault(int(d[:4]), []).append(xi)
ax.set_xticks([float(np.mean(v)) for k, v in sorted(porano.items())])
ax.set_xticklabels([str(k) for k in sorted(porano)], fontsize=9.5, color=TINTA2)
ax.set_yticks(range(0, 10, 2))
ax.set_yticklabels(["%d" % v for v in range(0, 10, 2)], fontsize=9.5, color=TINTA2)
ax.set_ylabel("área em défice  (ha)", fontsize=10, color=TINTA2, labelpad=8)
ax.grid(axis="y", color="#e8eaed", lw=0.8, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#dadce0")

ax.set_title("Défice de copado em Ganfei, separado pelo que o LiDAR encontrou no terreno",
             fontsize=13.5, color=TINTA, pad=26, loc="left", fontweight="bold")
ax.text(0, 1.045, "A série publicada somava videira viva a definhar com chão onde a planta já não existe. "
        "Separadas, o copado vivo desce sete anos até um piso de 0,66 ha e multiplica por sete em dois.",
        transform=ax.transAxes, fontsize=9.6, color=TINTA2)

leg = [Line2D([], [], color=AZUL, lw=2.6, marker="o", ms=7, mec="white", mew=1.5,
              label="com pérgola em 06-07-2025  ·  26,54 ha  —  copado vivo"),
       Line2D([], [], color=VERM, lw=2.0, marker="s", ms=6, mec="white", mew=1.4,
              label="sem pérgola  ·  3,77 ha  —  ausência de planta, não doença"),
       Line2D([], [], color=CINZ, lw=1.4, marker="o", ms=4.2, mec="white", mew=1.2,
              label="polígono inteiro  ·  30,31 ha  —  a série publicada")]
ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=1,
          frameon=False, fontsize=9.2, labelspacing=0.75, handlelength=2.6)

fig.text(0.062, -0.115,
         "Critério: altura MDS\u2212MDT \u2265 0,5 m na grelha de 10 m, voo LiDAR DGT de 06-07-2025 (data do tempo GPS dos pontos, não dos metadados).  "
         "Défice = NDVI abaixo da referência da própria cena menos 0,05.\n"
         "A abertura morfologica 2\u00d72 corre UMA VEZ sobre o poligono e so depois se divide \u2014 as duas linhas somam exactamente a cinzenta em todas as cenas.  "
         "Uma versão anterior dividia primeiro e lia zeros que eram costura.\n"
         "VIÉS DE SOBREVIVÊNCIA: a partição é de 2025, logo «copado vivo» é o que ainda estava vivo nessa data. Mortalidade consumada antes de 2025 conta como chão em toda a série, "
         "e a melhoria de 2017 a 2024 é medida só sobre sobreviventes.\n"
         "A mascara vem do LiDAR e a serie e de NDVI \u2014 instrumentos independentes.  Niveis absolutos nao comparaveis entre plataformas (vies S2C \u22480,048 NDVI).",
         fontsize=7.4, color=TINTA2, linespacing=1.7, va="top")

fig.savefig(os.path.join(AQUI, "F9_serie_separada.png"), bbox_inches="tight",
            facecolor="white", pad_inches=0.42)
fig.savefig(os.path.join(AQUI, "F9_serie_separada.svg"), bbox_inches="tight",
            facecolor="white", pad_inches=0.42)
print("escrito F9_serie_separada v2")
