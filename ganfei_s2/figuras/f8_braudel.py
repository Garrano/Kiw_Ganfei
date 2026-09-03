# -*- coding: utf-8 -*-
"""F8 — os tres registos de tempo. Companheira da F3, nao substituta.

Porque existe, e porque nao substitui a F3
------------------------------------------
A F3 poe satelite, gestao e laboratorio num **so** eixo do tempo. Serve para
ver coincidencias de data, e e para isso que continua a existir.

Esta figura faz o contrario, e e essa a tese de Braudel: os factos deste caso
nao correm todos ao mesmo ritmo, e por isso **nao cabem no mesmo eixo**. Cada
faixa tem a sua propria escala temporal, e a razao entre elas e o argumento.
O acontecimento de 2024-2026 ocupa dois anos; a conjuntura que o hospeda ocupa
trinta e cinco; a estrutura que hospeda essa nao tem data.

    acontecimento   o que se mede, ao dia e ao mes
    conjuntura      o que a exploracao decidiu, em decadas
    estrutura       o que nao muda: terraco, cota, dreno, solo, clima

A leitura que a figura serve: **as duas manchas diferem no registo de baixo —
uma esta no ponto baixo e humido, a outra no alto e pobre — e comportam-se de
maneira diferente no registo de cima: uma definha, a outra foi limpa.** A
estrutura nao causa o acontecimento; condiciona-o.

Nota de honestidade que a propria figura carrega: a faixa de baixo e a mais
solida e a que menos se mexe; a de cima e a que tem numeros com intervalo de
confianca e a que mais mudou de leitura em quarenta e oito horas.
"""
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, FancyBboxPatch

AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f2f1ed"
OESTE, ESTE = "#2a78d6", "#eb6834"          # mesma paleta da F3
NEUTRO, GEO = "#9a9890", "#7d6b52"

fig = plt.figure(figsize=(12.6, 11.2), dpi=200)
fig.patch.set_facecolor(FUNDO)
gs = fig.add_gridspec(3, 1, height_ratios=[1.06, 1.0, 0.80],
                      hspace=0.42, left=0.075, right=0.975,
                      top=0.845, bottom=0.085)
axA = fig.add_subplot(gs[0])   # acontecimento
axC = fig.add_subplot(gs[1])   # conjuntura
axE = fig.add_subplot(gs[2])   # estrutura


def veste(ax, x0, x1, titulo, subtitulo, tempo):
    ax.set_xlim(x0, x1); ax.set_ylim(0, 1)
    ax.set_facecolor(FUNDO)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, pad=6)
    ax.text(0, 1.24, titulo, transform=ax.transAxes, fontsize=13.5,
            fontweight="bold", color=TINTA, va="top")
    ax.text(0, 1.105, subtitulo, transform=ax.transAxes, fontsize=9.4,
            color=TINTA2, va="top")
    ax.text(1, 1.24, tempo, transform=ax.transAxes, fontsize=9.2,
            color=TINTA3, va="top", ha="right", style="italic")


# ---------------------------------------------------------------- ESTRUTURA
veste(axE, 0, 1, "ESTRUTURA",
      "O que não muda. Não tem data, e é o registo mais sólido do dossiê.",
      "tempo quase imóvel")
axE.axhspan(0.06, 0.94, color="#efece5", lw=0)
axE.plot([0.02, 0.98], [0.10, 0.10], color=GEO, lw=2.4, solid_capstyle="butt")
axE.text(0.5, 0.035, "terraço aluvial da margem esquerda do Minho  ·  "
         "clima atlântico, Entre Douro e Minho  ·  origem de água única",
         ha="center", va="center", fontsize=9.0, color=GEO)

EST = [
    (0.175, OESTE, "OESTE", "ponto BAIXO",
     ["cota mediana 6,64 m", "13,4 m do dreno", "carência de cálcio",
      "confirmada em duas matrizes"]),
    (0.615, ESTE, "ESTE", "ponto ALTO",
     ["cota mediana 7,83 m", "55,8 m do dreno",
      "o solo mais pobre da exploração", "radar sempre anómalo, dez Invernos"]),
]
for x, cor, nome, qual, linhas in EST:
    axE.add_patch(FancyBboxPatch((x, 0.30), 0.245, 0.52,
                                 boxstyle="round,pad=0.012,rounding_size=0.02",
                                 fc="white", ec=cor, lw=1.6,
                                 transform=axE.transData, zorder=3))
    axE.text(x + 0.1225, 0.745, "%s  —  %s" % (nome, qual), ha="center",
             fontsize=10.4, fontweight="bold", color=cor, zorder=4)
    for j, t in enumerate(linhas):
        axE.text(x + 0.1225, 0.655 - j * 0.082, t, ha="center", fontsize=8.5,
                 color=TINTA2, zorder=4)
axE.annotate("", xy=(0.428, 0.245), xytext=(0.612, 0.245),
             arrowprops=dict(arrowstyle="<->", lw=1.0, color=TINTA3))
axE.text(0.52, 0.185, "500 m  ·  hidraulicamente opostos", ha="center",
         va="top", fontsize=8.4, color=TINTA3, style="italic")
axE.set_xticks([])

# --------------------------------------------------------------- CONJUNTURA
veste(axC, 1988, 2027.4, "CONJUNTURA",
      "O que a exploração decidiu. Trinta e cinco anos de emparcelamento, "
      "porta-enxertos e plantações.", "décadas")
axC.axhspan(0.30, 0.44, color=FAIXA, lw=0)
for a in range(1990, 2027, 5):
    axC.axvline(a, color=RISCA, lw=0.7, zorder=0)
axC.set_xticks(list(range(1990, 2027, 5)))
axC.set_xticklabels([str(a) for a in range(1990, 2027, 5)],
                    fontsize=9, color=TINTA2)

# um nivel proprio para cada evento: dois patamares acima, dois abaixo
CONJ = [
    (1991, 0.62, "Emparcelamento", "cerca de 35 anos", NEUTRO, "^", True),
    (2011, 0.26, "Pérgola ainda a instalar-se",
     "visível nas ortofotos de 2010 e 2012", NEUTRO, "o", False),
    (2016, 0.85, "Enxertia Enza Gold  ·  rede instalada",
     "válvulas 2-5 (B1), sobre raiz de Summer Kiwi", ESTE, "D", True),
    (2020, 0.16, "Re-enxertia Erica  ·  rede removida",
     "as mesmas válvulas 2-5  ·  a rede existiu só no B1", ESTE, "D", False),
]
for x, y, t, sub, cor, mk, acima in CONJ:
    axC.plot([x], [0.37], marker=mk, ms=7.5, color=cor, mec="white", mew=1.3,
             zorder=5)
    axC.plot([x, x], [0.37, y - (0.05 if acima else -0.05)], color=cor,
             lw=0.9, alpha=0.55, zorder=2)
    axC.text(x, y, t, ha="center", va="bottom" if acima else "top",
             fontsize=9.0, color=TINTA)
    if sub:
        axC.text(x, y + (0.075 if acima else -0.075), sub, ha="center",
                 va="bottom" if acima else "top", fontsize=7.6, color=TINTA3,
                 linespacing=1.45)

# as quatro plantacoes recentes, como um so intervalo
axC.annotate("", xy=(2021.7, 0.575), xytext=(2025.3, 0.575),
             arrowprops=dict(arrowstyle="-", lw=5, color="#cfe0f5"))
for a, ha_ in ((2022, 4.09), (2023, 2.85), (2024, 1.50), (2025, 2.72)):
    axC.plot([a], [0.37], marker="o", ms=5.4, color=OESTE, mec="white",
             mew=1.1, zorder=5)
axC.text(2023.5, 0.62, "+11,16 ha de pomar novo em quatro anos",
         ha="center", va="bottom", fontsize=9.0, color=TINTA)
axC.text(2023.5, 0.695, "4,09  ·  2,85  ·  1,50  ·  2,72 ha  —  toda a agua "
         "da mesma origem", ha="center", va="bottom", fontsize=7.6, color=TINTA3)

axC.annotate("", xy=(2017, 0.475), xytext=(2024.4, 0.475),
             arrowprops=dict(arrowstyle="-", lw=4, color="#cfe0f5"))
axC.text(2020.7, 0.492, "o resto do pomar fecha o fosso à referência:  "
         "0,092 (2017)  \u2192  0,020 (2024)", ha="center", va="bottom",
         fontsize=8.0, color="#2a78d6")

# ------------------------------------------------------------ ACONTECIMENTO
veste(axA, 2024.35, 2026.92, "ACONTECIMENTO",
      "O que se mede. Dois anos, ao dia. É o registo mais frágil: "
      "e o que mais mudou de leitura em quarenta e oito horas.", "meses")
for a in (2025, 2026):
    axA.axvline(a, color=RISCA, lw=0.7, zorder=0)
axA.set_xticks([2024.5, 2025.0, 2025.5, 2026.0, 2026.5])
axA.set_xticklabels(["Jul 2024", "Jan 2025", "Jul 2025", "Jan 2026", "Jul 2026"],
                    fontsize=9, color=TINTA2)
axA.axhspan(0.44, 0.56, color=FAIXA, lw=0)

ACO = [
    (2024.56, 0.72, ESTE, "N3 colapsa em 18 dias",
     "22-07 a 09-08-2024  ·  0,875 \u2192 0,741\ncom o resto do bloco imóvel", "v"),
    (2025.04, 0.26, ESTE, "Piso de Inverno inverte",
     "N3 a +0,296 da referência\n(estava a \u22120,046 em 2022/23)", "^"),
    (2025.51, 0.76, GEO, "LiDAR  06-07-2025",
     "N3 a 0,27 m  ·  v8/B2 a 2,17 m\no único instrumento não-óptico", "*"),
    (2025.62, 0.22, OESTE, "Defice sanitario sai de zero",
     "1,32 ha, depois de sete anos a descer", "o"),
    (2026.57, 0.70, OESTE, "4,03 ha  ·  amplitude 0,30",
     "a videira abre a um terço do pomar são\nJul-Ago de 2026 o mais húmido "
     "da década", "o"),
]
for x, y, cor, t, sub, mk in ACO:
    axA.plot([x], [0.50], marker=mk, ms=10 if mk == "*" else 7.5, color=cor,
             mec="white", mew=1.3, zorder=5)
    acima = y > 0.56
    axA.plot([x, x], [0.50, y - (0.05 if acima else -0.05)], color=cor, lw=0.9,
             alpha=0.55, zorder=2)
    axA.text(x, y, t, ha="center", va="bottom" if acima else "top",
             fontsize=9.2, color=TINTA, fontweight="normal")
    axA.text(x, y + (0.075 if acima else -0.075), sub, ha="center",
             va="bottom" if acima else "top", fontsize=7.6, color=TINTA3,
             linespacing=1.45)

# cunhas de aproximacao entre faixas
def cunha(ax_de, ax_para, x0, x1):
    p0 = ax_de.transData.transform((x0, 0)); p1 = ax_de.transData.transform((x1, 0))
    q0 = ax_para.transData.transform((ax_para.get_xlim()[0], 1))
    q1 = ax_para.transData.transform((ax_para.get_xlim()[1], 1))
    inv = fig.transFigure.inverted()
    a, b = inv.transform(p0), inv.transform(p1)
    c, d = inv.transform(q0), inv.transform(q1)
    fig.patches.append(Polygon([[a[0], a[1]], [b[0], b[1]], [d[0], d[1]], [c[0], c[1]]],
                               closed=True, fc="#2a78d6", alpha=0.035, lw=0,
                               transform=fig.transFigure, zorder=0))


fig.canvas.draw()
cunha(axC, axA, 2024.35, 2026.92)
axC.plot([2024.35, 2026.92], [0.985, 0.985], color=OESTE, lw=1.1, alpha=0.6,
         clip_on=False)
axC.text(2025.6, 1.02, "ampliado acima", ha="center", va="bottom",
         fontsize=7.8, color=OESTE, style="italic")

fig.text(0.075, 0.968,
         "Ganfei  \u00b7  os tres registos de tempo",
         fontsize=17.5, fontweight="bold", color=TINTA)
fig.text(0.075, 0.938,
         "Cada faixa tem a sua própria escala. E a razão entre elas que é o argumento: "
         "o acontecimento ocupa dois anos, a conjuntura que o hospeda ocupa trinta e cinco, "
         "e a estrutura não tem data.",
         fontsize=10.2, color=TINTA2)

fig.text(0.075, 0.030,
         "Companheira da F3, não substituta: a F3 põe os mesmos factos num só eixo, para ver coincidências de data.  "
         "A estrutura nao causa o acontecimento \u2014 condiciona-o: as duas manchas ocupam posicoes hidraulicas opostas "
         "e comportam-se de maneira diferente.\n"
         "Fonte de cada registo: estrutura \u2014 MDT LiDAR 50 cm, analises de solo, SAR de dez Invernos.  "
         "conjuntura \u2014 testemunho do gestor e tabela de valvulas.  acontecimento \u2014 Sentinel-2, LiDAR de 06-07-2025, ERA5-Land.",
         fontsize=7.6, color=TINTA3, linespacing=1.75, va="top")

fig.savefig(os.path.join(AQUI, "F8_braudel.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.35)
fig.savefig(os.path.join(AQUI, "F8_braudel.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.35)
print("escrito F8_braudel.png / .svg")
