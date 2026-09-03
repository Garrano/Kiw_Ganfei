# -*- coding: utf-8 -*-
"""C3 · figuras. Duas, e so duas.

F1 — onde estao as amostras contra onde esta o padrao. E a figura da camada:
     mostra o buraco de amostragem na valvula 8.
F2 — a riqueza de ASV contra a profundidade de leitura, e os indices robustos.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import (AOI, FOCO_ESTE, FOCO_OESTE, ORIGEM_NO, carrega_mascaras,
                         discos_dos_focos)

C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
DL = r"C:\Users\Jackster2\Downloads"
OUT = os.path.dirname(os.path.abspath(__file__))

masc, _ = carrega_mascaras()
pomar, nu2021 = masc["pomar"], masc["nu2021"]
defice26 = np.load(os.path.join(C2, "c2_05_defice_2026.npy"))
novo = np.load(os.path.join(C2, "c2_05_novo_m2.npy"))
with open(os.path.join(DL, "ganfei_s2", "valvulas_por_area.json"), encoding="utf-8") as f:
    VALV = json.load(f)
with open(os.path.join(OUT, "c3_07_georreferenciacao.json"), encoding="utf-8") as f:
    GEO = json.load(f)
col = pd.read_csv(os.path.join(OUT, "c3_07_registos_colocados.csv"))

ext = [AOI[0], AOI[2], AOI[1], AOI[3]]

# ---------------------------------------------------------------- F1
fig, ax = plt.subplots(figsize=(15, 7.2))
fundo = np.zeros(pomar.shape)
fundo[pomar] = 1
fundo[defice26] = 2
fundo[novo] = 3
fundo[nu2021 & pomar] = 4
cmap = matplotlib.colors.ListedColormap(
    ["#f7f7f7", "#d9e8d2", "#f2c07a", "#c9482f", "#9e9e9e"])
ax.imshow(fundo, extent=ext, origin="upper", cmap=cmap, vmin=0, vmax=4,
          interpolation="nearest")

# esforco de amostragem por unidade
esf = col[col["classe_posicao"].isin(["COLOCADO", "COLOCADO-BLOCO", "INFERIDO",
                                      "AMBIGUO"])].groupby("unidade").size().to_dict()
for k in sorted(VALV, key=int):
    v = VALV[k]
    n_v = esf.get("v%s" % k, 0)
    n_b = esf.get(v["bloco"], 0)
    n = n_v + (n_b / len([j for j in VALV if VALV[j]["bloco"] == v["bloco"]]))
    ax.plot(v["E"], v["N"], "o", ms=5, mfc="white", mec="k", mew=1.2, zorder=5)
    if n > 0:
        ax.scatter([v["E"]], [v["N"]], s=n * 26, facecolor="#2b5fa8", alpha=0.32,
                   edgecolor="#1b3f70", zorder=4)
    ax.annotate("v%s" % k, (v["E"], v["N"]), textcoords="offset points",
                xytext=(0, -15), ha="center", fontsize=8.5, zorder=6)
    ax.annotate("%d" % round(n), (v["E"], v["N"]), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=8, color="#1b3f70",
                fontweight="bold", zorder=6)

for (E, N), nome, cor in ((FOCO_OESTE, "FOCO OESTE\nE530485 N4655053", "#111111"),
                          (FOCO_ESTE, "FOCO ESTE\nE530977 N4655117", "#111111")):
    circ = plt.Circle((E, N), 90, fill=False, ec=cor, lw=2.0, ls="--", zorder=7)
    ax.add_patch(circ)
    ax.plot(E, N, "x", color=cor, ms=11, mew=2.4, zorder=8)
    ax.annotate(nome, (E, N), textcoords="offset points", xytext=(0, 100),
                ha="center", fontsize=9, fontweight="bold", zorder=8)

ax.annotate("a v8 contem o FOCO OESTE\n50,7 % em défice · 47,1 % declínio novo\n"
            "ZERO registos de laboratório",
            (VALV["8"]["E"], VALV["8"]["N"]), textcoords="offset points",
            xytext=(-40, -78), ha="center", fontsize=9.5, color="#7a1d10",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#fff4f1", ec="#c9482f", lw=1.3),
            arrowprops=dict(arrowstyle="->", color="#c9482f", lw=1.6), zorder=9)

leg = [matplotlib.patches.Patch(fc="#d9e8d2", label="pomar sem défice em 2026"),
       matplotlib.patches.Patch(fc="#f2c07a", label="défice de 2026 com história anterior"),
       matplotlib.patches.Patch(fc="#c9482f", label="declínio novo pela regra M2 (3,58 ha)"),
       matplotlib.patches.Patch(fc="#9e9e9e", label="chão lavrado em 2021 (nu2021, 1,67 ha)"),
       plt.Line2D([], [], marker="o", ls="", mfc="#2b5fa8", mec="#1b3f70", alpha=0.5,
                  ms=11, label="registos de laboratório colocados na unidade")]
ax.legend(handles=leg, loc="lower right", fontsize=9, framealpha=0.94)
ax.set_title("C3 · onde estão as amostras contra onde está o padrão\n"
             "posições das válvulas de `valvulas_por_area.json` (R2 G35); "
             "padrão de `SAIDA_C2\\c2_05_*.npy`; focos por coordenada (R2 G34)",
             fontsize=11.5)
ax.set_xlabel("E (EPSG:32629)"); ax.set_ylabel("N (EPSG:32629)")
ax.set_xlim(530100, 531550); ax.set_ylim(4654820, 4655450)
ax.grid(alpha=0.18, lw=0.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "C3_F1_amostras_contra_padrao.png"), dpi=155)
print("escrito C3_F1_amostras_contra_padrao.png")

# ---------------------------------------------------------------- F2
with open(os.path.join(OUT, "c3_10_esforco_its_becrop.json"), encoding="utf-8") as f:
    R = json.load(f)["its"]
fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.3))
nomes = [a.replace("_ITS.pdf", "") for a in R["amostras"]]
axs[0].scatter(R["filtradas"], R["asv"], s=95, color="#c9482f", zorder=3)
for i, n in enumerate(nomes):
    axs[0].annotate(n, (R["filtradas"][i], R["asv"][i]), textcoords="offset points",
                    xytext=(7, -3), fontsize=8)
z = np.polyfit(R["filtradas"], R["asv"], 1)
xx = np.linspace(min(R["filtradas"]), max(R["filtradas"]), 50)
axs[0].plot(xx, np.polyval(z, xx), "--", color="#888", lw=1.2, zorder=2)
axs[0].set_title("riqueza de ASV contra profundidade\nρ de Spearman = +1,000 (4 de 4)",
                 fontsize=10)
axs[0].set_xlabel("leituras filtradas"); axs[0].set_ylabel("riqueza de ASV")

axs[1].bar(range(4), R["pielou"], color="#2b5fa8")
axs[1].set_ylim(0.75, 0.88); axs[1].set_xticks(range(4))
axs[1].set_xticklabels(nomes, rotation=30, ha="right", fontsize=8)
axs[1].set_title("equitabilidade de Pielou\namplitude 1,06x — indistinguíveis", fontsize=10)

axs[2].bar(range(4), R["pct_qualificadas"], color="#5a7d3a")
axs[2].set_xticks(range(4))
axs[2].set_xticklabels(nomes, rotation=30, ha="right", fontsize=8)
axs[2].set_title("%% de leituras qualificadas\n2,8 %% a 29,2 %% — amplitude de 10x", fontsize=10)
axs[2].set_ylabel("%")
for a in axs:
    a.grid(alpha=0.2, lw=0.5, axis="y")
fig.suptitle("C3 · as quatro ITS não são comparáveis entre si: a riqueza segue a "
             "profundidade e mais nada", fontsize=11.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "C3_F2_its_profundidade.png"), dpi=155)
print("escrito C3_F2_its_profundidade.png")
