# -*- coding: utf-8 -*-
"""F3 — Cronologia de tres faixas: satelite, gestao, laboratorio.

Um so eixo do tempo. A faixa de cima e o unico grafico; as duas de baixo sao
pistas de eventos que partilham esse eixo. Nao ha segundo eixo vertical.
Paleta: slots 1 e 2 da paleta de referencia (azul, laranja) — validada
all-pairs (CVD 24.7, visao normal 33.6, contraste >=3:1). Rotulos directos.
Eventos escalonados em niveis para nao colidirem.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f2f1ed"
Z0, MW = "#2a78d6", "#eb6834"
CRIT, NEUTRO = "#d03b3b", "#9a9890"

ANOS = np.arange(2017, 2027)
SERIE_Z0 = [-0.1488, -0.0853, -0.1269, -0.0702, -0.1776,
            -0.1484, -0.1730, -0.1582, -0.2217, -0.2306]
SERIE_MW = [-0.0407, -0.0183, 0.0009, -0.0008, 0.0129,
            0.0076, 0.0008, 0.0006, -0.0521, -0.1385]

# (ano, nivel, titulo, detalhe)
GESTAO = [
    (2016.4, 0, "Corte e enxertia com Enza Gold", "válvulas 2–5 (B1)"),
    (2020.4, 0, "Corte e enxertia com Erica", "válvulas 2–5 (B1)"),
    (2022.5, 0, "+4,09 ha de pomar novo", "o maior incremento"),
    (2023.5, 1, "+2,85 ha", "origem de água única"),
    (2024.6, 0, "+1,50 ha", None),
    (2025.6, 1, "+2,72 ha", None),
]
LAB = [
    (2023.6, 0, "Becrop A32A0C", "B3C3 (válv. 27, PARCELA ISOLADA — não o "
     "corpo em declínio) · P. sojae +, saúde Muito Baixa"),
    (2024.1, 2, "Becrop A32A0B", "mesmo sector · P. sojae não detectado, "
     "saúde Alta · atribuído a Trichoderma + húmus"),
    (2025.45, 0, "Areeiro 331/2025 «Kiwi 1000»",
     "Mancha W · M. hapla +, G. intermedium +, oomicetas no solo −"),
    (2025.75, 2, "4 amostras ITS", "Zona 0 · só comunidade, sem painel de patogénios"),
    (2026.25, 1, "Lote de nemátodos + boletins de solo", "B1 e B4"),
    (2026.70, 3, "Visita de campo 04/08", "planta arrancada, Rosellinia visual, n=1"),
]

fig = plt.figure(figsize=(17.0, 12.0), dpi=200)
fig.patch.set_facecolor(FUNDO)
X0, X1 = 2016.15, 2028.6
ESQ, LARG = 0.050, 0.905

ax = fig.add_axes([ESQ, 0.545, LARG, 0.335])
ax.set_facecolor(FUNDO)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(TINTA3); ax.spines[s].set_linewidth(0.7)
ax.set_xlim(X0, X1); ax.set_ylim(-0.268, 0.072)
ax.set_yticks([0, -0.05, -0.10, -0.15, -0.20, -0.25])
ax.tick_params(labelsize=7.6, colors=TINTA2, length=3)
ax.set_xticks(range(2017, 2027))
ax.set_xticklabels([])
ax.grid(axis="y", color=RISCA, lw=0.6); ax.set_axisbelow(True)
ax.set_ylabel("NDVI de Verão menos a referência sã", fontsize=8.4, color=TINTA2)

for a, b, m, rot in ((2016.9, 2020.4, -0.1078, "planalto  −0,108"),
                     (2020.6, 2024.4, -0.1643, "planalto  −0,164"),
                     (2024.6, 2026.4, -0.2262, "planalto  −0,226")):
    ax.add_patch(Rectangle((a, m - 0.006), b - a, 0.012, facecolor=Z0,
                           alpha=0.13, edgecolor="none", zorder=1))
    ax.text((a + b) / 2, m + 0.012, rot, fontsize=6.8, color=Z0, ha="center")

ax.axhline(0, color=TINTA, lw=1.2, zorder=3)
ax.text(X0 + 0.06, 0.007, "referência sã", fontsize=7.4, color=TINTA2)
ax.plot(ANOS, SERIE_Z0, "-o", color=Z0, lw=2.0, ms=6.5, zorder=5,
        markeredgecolor=FUNDO, markeredgewidth=1.4)
ax.plot(ANOS, SERIE_MW, "-s", color=MW, lw=2.0, ms=6.0, zorder=5,
        markeredgecolor=FUNDO, markeredgewidth=1.4)
ax.text(2026.18, -0.2306, "  Zona 0", fontsize=11, color=Z0,
        fontweight="bold", va="center")
ax.text(2026.18, -0.1385, "  Mancha W", fontsize=11, color=MW,
        fontweight="bold", va="center")


def seta(x, y, texto, dx, dy, cor, ha):
    ax.annotate(texto, xy=(x, y), xytext=(x + dx, y + dy), fontsize=7.4,
                color=cor, fontweight="bold", ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=cor, lw=0.9, alpha=0.8,
                                connectionstyle="arc3,rad=0.15"))


seta(2021, -0.1776, "1.º degrau  −0,057\nsem nada na faixa de gestão",
     -0.25, -0.045, Z0, "right")
seta(2025, -0.2217, "2.º degrau  −0,062", 0.55, -0.022, Z0, "left")
seta(2024, 0.0006, "semente: 4 pixels (0,04 ha)\nem Julho de 2024",
     -0.35, 0.042, MW, "right")
ax.axvspan(2025.24, 2025.40, color=CRIT, alpha=0.10, zorder=0)
ax.text(2025.32, 0.052, "23–28 abr 2025", fontsize=7.2, color=CRIT,
        ha="center", fontweight="bold")
ax.text(2025.32, 0.036, "divergência abre", fontsize=6.8, color=CRIT, ha="center")

fig.text(ESQ, 0.972, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(ESQ, 0.938, "Cronologia de três faixas", fontsize=21, color=TINTA,
         fontweight="bold")
fig.text(0.955, 0.942, "F3 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(ESQ, 0.900,
         "Um só eixo do tempo. É da sobreposição das três faixas que sai toda a "
         "inferência causal do caso — e onde ela falha.",
         fontsize=8.6, color=TINTA2)
fig.text(ESQ, 0.884, "SATÉLITE — o que foi medido", fontsize=7.8, color=TINTA2,
         fontweight="bold")


def pista(rect, titulo, eventos, n_niveis):
    a = fig.add_axes(rect)
    a.set_xlim(X0, X1); a.set_ylim(0, 1); a.set_axis_off()
    a.add_patch(Rectangle((X0, 0), X1 - X0, 1, facecolor=FAIXA,
                          edgecolor="none", zorder=0))
    a.text(X0 + 0.06, 0.93, titulo, fontsize=7.8, color=TINTA2,
           fontweight="bold", va="top")
    passo = 0.72 / max(n_niveis, 1)
    for x, lvl, t1, t2 in eventos:
        yt = 0.74 - lvl * passo
        a.plot([x, x], [0.03, yt], color=NEUTRO, lw=1.0, alpha=0.55, zorder=1)
        a.plot([x], [yt], "o", color=NEUTRO, ms=6.0, zorder=3,
               markeredgecolor=FUNDO, markeredgewidth=1.2)
        a.text(x + 0.07, yt + 0.055, t1, fontsize=7.4, color=TINTA,
               ha="left", va="center", fontweight="bold")
        if t2:
            a.text(x + 0.07, yt - 0.055, t2, fontsize=6.6, color=TINTA2,
                   ha="left", va="center")
    return a


pista([ESQ, 0.372, LARG, 0.140], "GESTÃO — o que a exploração fez", GESTAO, 2)
pista([ESQ, 0.152, LARG, 0.196], "LABORATÓRIO — o que foi analisado", LAB, 4)

axe = fig.add_axes([ESQ, 0.140, LARG, 0.0001])
axe.set_xlim(X0, X1); axe.set_yticks([])
for s in ("top", "right", "left"):
    axe.spines[s].set_visible(False)
axe.spines["bottom"].set_color(TINTA); axe.spines["bottom"].set_linewidth(1.0)
axe.set_xticks(range(2017, 2027))
axe.set_xticklabels([str(a) for a in range(2017, 2027)], fontsize=8.4,
                    color=TINTA)
axe.tick_params(length=4, colors=TINTA)

for x, cor, lw in ((2021, Z0, 1.4), (2022.5, NEUTRO, 1.0), (2025.32, CRIT, 1.6)):
    fig.add_artist(plt.Line2D([ESQ + LARG * (x - X0) / (X1 - X0)] * 2,
                              [0.142, 0.880], color=cor, lw=lw, alpha=0.26,
                              zorder=0))

fig.text(ESQ, 0.088, "O QUE A SOBREPOSIÇÃO MOSTRA", fontsize=8.2, color=TINTA,
         fontweight="bold")
fig.text(ESQ, 0.062,
         "2021 — a Zona 0 dá o primeiro degrau e não há NADA na faixa de gestão "
         "nesse ano. O que quer que o tenha causado, não foi a rede: os pomares "
         "novos só começam em 2022.", fontsize=7.9, color=TINTA2)
fig.text(ESQ, 0.040,
         "2025 — a divergência abre em 23–28 de Abril, no mínimo de procura de "
         "rega, e no ano de +2,72 ha novos. A coincidência é real; a explicação "
         "hidráulica tem o problema de a data ser Abril.", fontsize=7.9,
         color=TINTA2)
fig.text(ESQ, 0.018,
         "A faixa do laboratório nunca tocou a Zona 0 com um painel de patogénios "
         "— só comunidade ITS. É o foco mais antigo e o menos analisado.",
         fontsize=7.9, color=CRIT, fontweight="bold")

fig.savefig("F3_cronologia.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F3_cronologia.svg", facecolor=FUNDO, bbox_inches="tight")
print("F3 gravada")
