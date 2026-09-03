# -*- coding: utf-8 -*-
"""P04a — a fronteira que não escolhemos. As parcelas do IFAP.

O que esta peca faz que nenhuma outra faz
-----------------------------------------
Todas as outras unidades deste dossie tem uma fronteira que alguem aqui
desenhou: um poligono, um disco, um limiar de altura. Mesmo as geograficas
foram escolhidas por nos, ainda que antes de ver o resultado.

**As parcelas do IFAP nao.** Foram desenhadas por outra entidade, para
pagamentos da PAC, anos antes desta analise, e nao sabem nada de NDVI. Para um
leitor institucional isto vale mais do que qualquer p: e verificavel por
terceiros, no parcelario que a propria CCDR-N tem.

A unica escolha que sobra e QUAL parcela — e essa e feita pela geografia (a
que contem o ponto), nao pelo valor. Por isso desenham-se as SEIS parcelas
que intersectam o pomar, e nao so a interessante. Uma parcela que so parecesse
extrema depois de escolhida nao passava neste teste.

E ha um segundo facto na figura, que nao precisa de teste nenhum
----------------------------------------------------------------
A parcela oriental tem **0,12 ha com pergola em 1,05 ha**, e o seu nivel antes
do acontecimento era **0,730** contra 0,867 a 0,892 em todas as outras cinco.
Isso e medicao directa, nao inferencia: estava 0,14 de NDVI abaixo de toda a
exploracao antes de acontecer o que quer que tenha acontecido. Confirmacao
administrativa da falha de instalacao, independente do LiDAR e do Sentinel-2.

O que esta figura NAO afirma
----------------------------
O degrau da parcela oriental (-0,052) **nao e significativo** (p = 0,37), e a
razao esta a vista na propria figura: 0,12 ha sao doze celulas. Vai desenhado
com o p ao lado e sem asterisco. O que a parcela oriental estabelece e o
NIVEL, nao o degrau — e o nivel nao precisa de teste.
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

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
L = json.load(open(os.path.join(VG, "ocidental_independente.json")))
L = sorted(L, key=lambda r: r["degrau"])

AZUL, LARANJA, NEUTRO = "#2a78d6", "#eb6834", "#6b6f76"
TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, GRELHA = "#fcfcfb", "#eceae5"


def pt(v, casas=3, sinal=False):
    s = ("%+.*f" if sinal else "%.*f") % (casas, v)
    return s.replace("-", "−").replace(".", ",")


def cor_de(r):
    if "OCIDENTAL" in r["contem"]:
        return AZUL
    if "ORIENTAL" in r["contem"]:
        return LARANJA
    return NEUTRO


n = len(L)
y = np.arange(n)[::-1]

fig = plt.figure(figsize=(14.2, 7.4), dpi=200)
fig.patch.set_facecolor(FUNDO)

# ------------------------------------------------- coluna de identificacao
axid = fig.add_axes([0.048, 0.20, 0.262, 0.535]); axid.axis("off")
axid.set_xlim(0, 1)
axid.set_ylim(-0.75, n - 0.25)
for r, yy in zip(L, y):
    c = cor_de(r)
    marca = ("foco OCIDENTAL" if "OCIDENTAL" in r["contem"]
             else "foco ORIENTAL" if "ORIENTAL" in r["contem"] else "")
    axid.text(0, yy + 0.17, r["par"], ha="left", va="center", fontsize=10.4,
              color=TINTA if marca else TINTA2,
              fontweight="bold" if marca else "normal",
              family="DejaVu Sans Mono")
    sub = "%s ha com pérgola  ·  de %s ha" % (pt(r["ha_com"], 2), pt(r["ha"], 2))
    axid.text(0, yy - 0.20, sub, ha="left", va="center", fontsize=8.2,
              color=TINTA3)
    if marca:
        axid.plot([0.62], [yy + 0.17],
                  "o" if "OCIDENTAL" in r["contem"] else "D",
                  ms=8, color=c, mec=FUNDO, mew=1.4, clip_on=False)
        axid.text(0.665, yy + 0.17, marca, ha="left", va="center",
                  fontsize=9.4, color=c, fontweight="bold")

# ------------------------------------------------------ painel 1 — o nivel
ax1 = fig.add_axes([0.335, 0.20, 0.20, 0.535])
ax1.set_facecolor(FUNDO)
for r, yy in zip(L, y):
    c = cor_de(r)
    foco = bool(r["contem"])
    ax1.plot([0.70, r["base"]], [yy, yy], color=c, lw=1.2, alpha=0.28, zorder=2)
    ax1.plot([r["base"]], [yy], "D" if "ORIENTAL" in r["contem"] else
             ("o" if "OCIDENTAL" in r["contem"] else "s"),
             ms=10 if foco else 7.5, color=c, mec=FUNDO, mew=1.6, zorder=4)
    ax1.text(r["base"] + (0.010 if foco else 0.006), yy, pt(r["base"]),
             va="center", fontsize=9.6,
             color=c, fontweight="bold" if foco else "normal")
ax1.axvspan(0.860, 0.900, color="#eceae5", zorder=0)
ax1.text(0.880, -0.68, "as outras cinco\n0,867 – 0,892", ha="center",
         va="bottom", fontsize=8.2, color=TINTA3, linespacing=1.5)
ax1.set_xlim(0.700, 0.935)
ax1.set_ylim(-0.75, n - 0.25)
ax1.set_yticks([])
ax1.set_xticks([0.75, 0.80, 0.85, 0.90])
ax1.set_xticklabels(["0,75", "0,80", "0,85", "0,90"], fontsize=8.8, color=TINTA2)
ax1.grid(axis="x", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right", "left"):
    ax1.spines[s].set_visible(False)
ax1.spines["bottom"].set_color("#dcd9d3")
ax1.set_xlabel("NDVI médio  ·  2017 a 2024", fontsize=9.4, color=TINTA2,
               labelpad=7)
ax1.text(0, 1.045, "ONDE CADA PARCELA ESTAVA, ANTES", transform=ax1.transAxes,
         fontsize=9.6, color=TINTA, fontweight="bold")

# ----------------------------------------------------- painel 2 — o degrau
ax2 = fig.add_axes([0.615, 0.20, 0.315, 0.535])
ax2.set_facecolor(FUNDO)
ax2.axvline(0, color="#c9c5bd", lw=1.0, zorder=1)
for r, yy in zip(L, y):
    c = cor_de(r)
    foco = bool(r["contem"])
    sig = r["p"] < 0.05
    ax2.barh(yy, r["degrau"], height=0.44, color=c,
             alpha=1.0 if sig else 0.30, zorder=3,
             edgecolor=c, lw=1.4 if not sig else 0)
    ax2.text(r["degrau"] - 0.0022, yy, pt(r["degrau"], sinal=True),
             ha="right", va="center", fontsize=10.4 if foco else 9.4,
             color=c, fontweight="bold" if foco else "normal")
    ax2.text(0.0025, yy, "p = %s%s" % (pt(r["p"], 3).lstrip("0"),
                                       "  ✳" if sig else ""),
             ha="left", va="center", fontsize=8.4,
             color=c if sig else TINTA3)
ax2.set_xlim(-0.079, 0.030)
ax2.set_ylim(-0.75, n - 0.25)
ax2.set_yticks([])
ax2.set_xticks([-0.06, -0.04, -0.02, 0])
ax2.set_xticklabels(["−0,06", "−0,04", "−0,02", "0"], fontsize=8.8, color=TINTA2)
ax2.grid(axis="x", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right", "left"):
    ax2.spines[s].set_visible(False)
ax2.spines["bottom"].set_color("#dcd9d3")
ax2.set_xlabel("queda de 2025-26 face a 2017-24  (NDVI)", fontsize=9.4,
               color=TINTA2, labelpad=7)
ax2.text(0, 1.045, "QUANTO CADA UMA CAIU", transform=ax2.transAxes,
         fontsize=9.6, color=TINTA, fontweight="bold")
ax2.text(1.0, 1.045, "barra cheia = p < 0,05", transform=ax2.transAxes,
         ha="right", fontsize=8.2, color=TINTA3)

# ------------------------------------------------------------------ titulo
fig.text(0.048, 0.945, "A fronteira que não escolhemos",
         fontsize=23, fontweight="bold", color=TINTA)
fig.text(0.048, 0.900,
         "As seis parcelas do IFAP que intersectam o pomar — desenhadas por outra entidade, "
         "para pagamentos, anos antes, sem saber nada de NDVI.",
         fontsize=11.4, color=TINTA2)
fig.text(0.048, 0.862,
         "A parcela do foco ocidental caiu três a cinco vezes mais do que qualquer outra da "
         "mesma exploração — e diluída, porque tem 8,81 ha e o foco não chega a 2,5.",
         fontsize=11.4, color=TINTA, fontweight="bold")

fig.text(0.048, 0.128,
         "PORQUE ESTA PEÇA EXISTE: todas as outras unidades do dossiê têm uma fronteira que nós desenhámos. Estas não. São verificáveis por terceiros no parcelário que a CCDR-N já tem — ENT_ID 472062.\n"
         "Estão as SEIS que intersectam o pomar, não só a interessante: uma parcela que só parecesse extrema depois de escolhida não passaria neste teste. A escolha é geográfica — a que contém o ponto.\n"
         "A PARCELA ORIENTAL NÃO É SIGNIFICATIVA (p = 0,37) e a razão está na própria figura: 0,12 ha são doze células. O que ela estabelece é o NÍVEL, e o nível é medição directa, não inferência —\n"
         "estava 0,14 de NDVI abaixo de toda a exploração ANTES de acontecer seja o que for. É confirmação administrativa da falha de instalação, independente do LiDAR e do Sentinel-2.\n"
         "Só células com pérgola no LiDAR de 06-07-2025, parcela inteira, sem recortes. p por permutação da etiqueta de ano, 20 000 sorteios.",
         fontsize=7.9, color=TINTA3, linespacing=1.9, va="top")

fig.savefig(os.path.join(AQUI, "P04a_parcelas_ifap.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "P04a_parcelas_ifap.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito P04 — %d parcelas" % n)
for r in L:
    print("  %-16s %+.4f  p=%.4f  base=%.3f  %s"
          % (r["par"], r["degrau"], r["p"], r["base"], ",".join(r["contem"])))
