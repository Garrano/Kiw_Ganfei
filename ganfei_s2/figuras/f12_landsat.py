# -*- coding: utf-8 -*-
"""F12 — a medição independente. Catorze anos de Landsat.

O que a figura tem de fazer
---------------------------
Todo o resto do dossie corre sobre Sentinel-2. Isso significa um sensor, uma
agencia, uma cadeia de correccao atmosferica e um arquivo. A cadeia de validacao
inteira nasceu de um facto que so tinha o instrumento que o produziu, e a sua
regra 1 e que **nenhum facto passa verificado so por esse instrumento**.

Esta e a unica serie do caso que vem de outro lado: **USGS/NASA em vez de ESA,
OLI em vez de MSI, LaSRC em vez de Sen2Cor, outra orbita e outra hora de
passagem.** Partilha com o Sentinel-2 apenas o principio fisico.

O adversario da ronda H1 chamou-lhe «o melhor resultado do dia» e registou que
**cinco certificados consecutivos a declararam sem a certificar**. Nunca foi
desenhada.

Forma
-----
Uma serie, um eixo. A grandeza e o **fosso a referencia dentro da mesma cena** —
referencia menos unidade — porque comparar dentro da cena remove atmosfera,
sensor, angulo e data de uma vez. Zero significa «indistinguivel da referencia».

Tres linhas, nao quatro: as duas partes do foco oriental separadas, porque o
LiDAR mostrou que metade dele nao tem planta, e **a parte sem planta e o
controlo negativo desta figura**.

O que esta figura NAO mostra, e porque
--------------------------------------
O ficheiro tem tambem NDMI, e existiu uma leitura — «os focos perdem agua antes
de verdura» — que foi **RETIRADA por inteiro** pelo rastreio (R6), e com ela a
inferencia hidraulica que dela saia. **Nao se desenha o que foi retirado**, nem
sequer como ilustracao.
"""
import json
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
D = json.load(open(os.path.join(VG, "landsat.json")))

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO = "#fbfbfa"
OESTE, ESTE, CHAO, RESTO = "#0072B2", "#D55E00", "#b9b5ad", "#4c9a5a"

UN = [("OESTE com pergola", "v8 / B2  —  copado vivo", OESTE, "o", 2.9),
      ("ESTE com pergola", "ESTE, a parte com pérgola", ESTE, "s", 2.2),
      ("ESTE sem pergola", "ESTE, a parte SEM pérgola  —  o controlo", CHAO, "^", 1.8),
      ("resto do pomar", "resto do pomar", RESTO, "D", 1.6)]

anos = list(range(2013, 2027))
serie, n_ano = {}, {}
for k, _, _, _, _ in UN:
    L, N = [], []
    for a in anos:
        v = [r["referencia"] - r[k] for r in D if int(r["data"][:4]) == a]
        L.append(np.median(v) if v else np.nan)
        N.append(len(v))
    serie[k] = np.array(L)
    n_ano[k] = N
nref = [sum(1 for r in D if int(r["data"][:4]) == a) for a in anos]

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(13.4, 7.8), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.058, 0.185, 0.665, 0.60])
ax.set_facecolor(FUNDO)

# a faixa dos onze anos planos, e o seu envelope medido
o = serie["OESTE com pergola"]
i23 = anos.index(2023)
env = np.nanmax(np.abs(o[:i23 + 1]))
ax.axhspan(-env, env, xmin=0, xmax=(2023.6 - 2012.4) / (2026.9 - 2012.4),
           color=OESTE, alpha=0.07, lw=0)
ax.axhline(0, color=TINTA3, lw=0.9, zorder=1)

for k, rot, cor, mk, lw in UN:
    ax.plot(anos, serie[k], "-", color=cor, lw=lw, zorder=4,
            alpha=1.0 if k.startswith("OESTE") else 0.95)
    ax.plot(anos, serie[k], mk, color=cor, ms=6.4 if lw > 2 else 5.2,
            mec="white", mew=1.2, zorder=5)

ax.annotate("0,146", (2026, o[-1]), xytext=(11, 0), textcoords="offset points",
            color=OESTE, fontsize=12.5, fontweight="bold", va="center")
ax.annotate("0,046", (2025, o[-2]), xytext=(-4, -19), textcoords="offset points",
            color=OESTE, fontsize=10, fontweight="bold", ha="center")
e = serie["ESTE com pergola"]
ax.annotate("0,138", (2026, e[-1]), xytext=(11, 0), textcoords="offset points",
            color=ESTE, fontsize=10.5, fontweight="bold", va="center")
c = serie["ESTE sem pergola"]
ax.annotate("sem tendência em catorze anos", (2023, c[anos.index(2023)]),
            xytext=(0, 13), textcoords="offset points", color="#8d8a84",
            fontsize=9, ha="center")
r_ = serie["resto do pomar"]
ax.annotate("−0,004", (2026, r_[-1]), xytext=(11, 0), textcoords="offset points",
            color=RESTO, fontsize=9.5, va="center")

ax.text(2017.6, -0.030,
        "onze anos dentro de ±%s do zero — indistinguível da referência"
        % ("%.3f" % env).replace(".", ","), ha="center", va="center",
        fontsize=9.6, color=OESTE, style="italic")

ax.set_xlim(2012.4, 2027.15)
ax.set_ylim(-0.06, 0.36)
ax.set_xticks(anos)
ax.set_xticklabels([str(a) for a in anos], fontsize=9.2, color=TINTA2)
ax.set_yticks([0, 0.1, 0.2, 0.3])
ax.set_yticklabels(["0", "0,1", "0,2", "0,3"], fontsize=9.2, color=TINTA2)
ax.set_ylabel("fosso à referência, na mesma cena  (NDVI)", fontsize=10,
              color=TINTA2, labelpad=9)
ax.grid(axis="y", color="#eceae5", lw=0.8, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#dcd9d3")

# cenas por ano, em baixo — a densidade sustenta a leitura
axn = fig.add_axes([0.058, 0.100, 0.665, 0.042])
axn.bar(anos, nref, width=0.62, color="#dcd9d3")
for a, v in zip(anos, nref):
    axn.text(a, v + 1.2, "%d" % v, ha="center", va="bottom", fontsize=6.8,
             color=TINTA3)
axn.set_xlim(2012.4, 2027.15); axn.set_ylim(0, 36)
axn.set_xticks([]); axn.set_yticks([]); axn.set_facecolor(FUNDO)
for s in axn.spines.values():
    s.set_visible(False)
axn.text(2012.4, 13, "cenas por ano  ", ha="right", va="center", fontsize=8,
         color=TINTA3)

# ------------------------------------------------------------- lado direito
axr = fig.add_axes([0.745, 0.100, 0.235, 0.685]); axr.axis("off")
axr.set_xlim(0, 1); axr.set_ylim(0, 1)
axr.text(0, 0.995, "PORQUE É INDEPENDENTE", fontsize=9.2, color=TINTA,
         fontweight="bold", va="top")
axr.text(0, 0.945,
         "USGS/NASA, não ESA\nsensor OLI, não MSI\ncorrecção LaSRC, não Sen2Cor\n"
         "outra órbita, outra hora",
         fontsize=8.6, color=TINTA2, va="top", linespacing=1.85)

axr.plot([0, 1], [0.755, 0.755], lw=0.9, color="#e6e3dd")
axr.text(0, 0.705, "140 cenas", fontsize=17, color=TINTA, fontweight="bold",
         va="top")
axr.text(0, 0.645, "Landsat 8 e 9, 2013–2026\nJunho a Setembro",
         fontsize=8.6, color=TINTA2, va="top", linespacing=1.6)

axr.plot([0, 1], [0.555, 0.555], lw=0.9, color="#e6e3dd")
axr.text(0, 0.505, "A RESSALVA", fontsize=9.2, color=TINTA,
         fontweight="bold", va="top")
axr.text(0, 0.458,
         "O NDVI satura sobre copado\nfechado. A linha plana vale como\n"
         "«era indistinguível», NÃO como\n«não havia variação pequena».\n\n"
         "O que a torna interpretável é o\ntamanho do afastamento em\n2025-26, "
         "não a planura.",
         fontsize=8.3, color=TINTA2, va="top", linespacing=1.62)

axr.plot([0, 1], [0.130, 0.130], lw=0.9, color="#e6e3dd")
axr.text(0, 0.088, "A referência do Landsat cai 0,026.\n"
         "O Sentinel-2 dá 0,054 nas\nmesmas células.",
         fontsize=8.0, color=TINTA3, va="top", linespacing=1.62, style="italic")

leg = [Line2D([], [], color=c, lw=lw, marker=m, ms=6.4 if lw > 2 else 5.2,
              mec="white", mew=1.2, label=r)
       for k, r, c, m, lw in UN]
ax.legend(handles=leg, loc="upper left", frameon=False, fontsize=9.2,
          labelspacing=0.6, handlelength=2.4, bbox_to_anchor=(0.008, 0.99))

fig.text(0.058, 0.945, "O outro instrumento diz o mesmo",
         fontsize=20.5, fontweight="bold", color=TINTA)
fig.text(0.058, 0.902,
         "Catorze anos de Landsat 8 e 9 — outra agência, outro sensor, outra correcção atmosférica.",
         fontsize=11, color=TINTA2)
fig.text(0.058, 0.868,
         "Onze anos indistinguível da referência. Depois 0,046 e 0,146.",
         fontsize=11, color=TINTA, fontweight="bold")

fig.text(0.058, 0.062,
         "O fosso é medido DENTRO de cada cena — referência menos unidade — o que remove atmosfera, sensor, ângulo e data de uma vez.  "
         "A partição com/sem pérgola vem do LiDAR de 06-07-2025, não do NDVI.\n"
         "A parte oriental SEM pérgola é o controlo negativo desta figura: fosso grande e ruidoso desde 2013, sem tendência — o que se espera de chão, e o que se vê.\n"
         "O ficheiro contém também NDMI. A leitura que dele se tirou — «os focos perdem água antes de verdura» — foi RETIRADA pelo rastreio, e por isso não é desenhada.",
         fontsize=7.9, color=TINTA3, linespacing=1.85, va="top")

fig.savefig(os.path.join(AQUI, "F12_landsat.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
fig.savefig(os.path.join(AQUI, "F12_landsat.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
print("escrito F12 · envelope dos onze anos = ±%.4f" % env)
print("OESTE:", " ".join("%.3f" % v for v in o))
