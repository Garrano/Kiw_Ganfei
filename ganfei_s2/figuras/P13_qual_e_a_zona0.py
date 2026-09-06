# -*- coding: utf-8 -*-
"""P13 — mapa C do email: qual dos dois e a Zona 0?

Esta prancha NAO responde a pergunta. Faz a pergunta.

O gestor disse a 06-09-2026 que a Zona 0 sao as valvulas 8, 9 e 10 — B2 mais
Erica Novo. Nos temos duas manchas de quebra separadas por ~500 m, e um ficheiro
interno com o nome trocado: a mascara chamada `zona0_bits` tem o centroide a
516 m do foco POENTE e a 26 m do NASCENTE (IX-18).

Por isso os dois discos aqui saem com rotulos **neutros e geograficos** —
POENTE e NASCENTE — e a legenda pergunta. Rotular um deles de «Zona 0» seria
por na boca do gestor a resposta que lhe estamos a pedir, e a CLAUSULAS ja
regista que a designacao dos focos foi invertida por quatro auditorias.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "base"))
from carta_base import (cartela_institucional, Base, PAPEL, TINTA, TINTA2,  # noqa
                        TINTA3, virg)

# as coordenadas certificadas, do c1_00_comum.py
POENTE = (530485.0, 4655053.0)
NASCENTE = (530977.0, 4655117.0)
RAIO = 90.0

b = Base()
fig, ax, axl = b.figura(larg=16.0)
ytop = cartela_institucional(fig)

b.terreno(ax)
b.cadastro(ax)
b.sectores(ax)
b.rotulos(ax)
b.toponimos(ax)

# ── os dois discos, com peso identico ───────────────────────────────────────
for (x, y), letra in ((POENTE, "A"), (NASCENTE, "B")):
    ax.add_patch(Circle((x, y), RAIO, facecolor="none", edgecolor=TINTA,
                        lw=2.2, ls=(0, (6, 3)), zorder=6))
    ax.add_patch(Circle((x, y), RAIO, facecolor="#FFFFFF", alpha=0.16,
                        edgecolor="none", zorder=5))
    ax.text(x, y + RAIO + 26, letra, fontsize=17, weight="bold", color=TINTA,
            ha="center", va="bottom", zorder=8,
            path_effects=None)
    ax.plot([x], [y], marker="+", ms=11, mew=1.6, color=TINTA, zorder=8)

ax.annotate("", xy=NASCENTE, xytext=POENTE,
            arrowprops=dict(arrowstyle="<->", color=TINTA3, lw=1.0,
                            shrinkA=RAIO + 4, shrinkB=RAIO + 4), zorder=4)
mx, my = (POENTE[0] + NASCENTE[0]) / 2, (POENTE[1] + NASCENTE[1]) / 2
ax.text(mx, my - 30, "≈ 500 m", fontsize=8.6, color=TINTA2, style="italic",
        ha="center", va="top", zorder=9,
        bbox=dict(boxstyle="round,pad=0.22", fc="#FBFAF7", ec="none", alpha=0.88))

b.moldura(ax)

fig.text(0.035, ytop, "GANFEI · QUAL DOS DOIS É A ZONA 0?", fontsize=21,
         weight="bold", color=TINTA, va="top", ha="left")
fig.text(0.035, ytop - 0.30 / fig.get_figheight(),
         "Emparcelamento de Ganfei, Valença — pedido de confirmação ao gestor",
         fontsize=10.5, color=TINTA2, va="top", ha="left")
fig.text(0.955, ytop - (21 - 10.5) * 0.70 / 72 / fig.get_figheight(),
         "duas manchas de quebra  ·  discos de 90 m  ·  separadas ≈ 500 m",
         fontsize=10.5, color=TINTA2, va="top", ha="right")
fig.text(0.955, ytop - (21 - 10.5) * 0.70 / 72 / fig.get_figheight() - 0.026,
         "ETRS89 / UTM 29N (EPSG:32629)  ·  quadrícula 250 m",
         fontsize=8.2, color=TINTA3, va="top", ha="right")

# ── a legenda E a pergunta ──────────────────────────────────────────────────
axl.set_xlim(0, 1); axl.set_ylim(0, 1); axl.axis("off")
axl.text(0.02, 0.975, "A PERGUNTA", fontsize=9.0, weight="bold", color=TINTA,
         va="top", ha="left", transform=axl.transAxes)
axl.text(0.02, 0.935,
         "Disse-nos que a Zona 0 são as\nválvulas 8, 9 e 10 — B2 mais\nErica Novo.\n\n"
         "Vemos duas manchas de quebra,\nseparadas por cerca de meio\nquilómetro.\n\n"
         "Qual delas é a Zona 0, «onde\ntudo começou»?",
         fontsize=8.0, color=TINTA, va="top", ha="left",
         transform=axl.transAxes, linespacing=1.55)

axl.text(0.02, 0.545, "BASTA RISCAR", fontsize=9.0, weight="bold", color=TINTA,
         va="top", ha="left", transform=axl.transAxes)
for i, (l, txt) in enumerate((("A", "a poente"), ("B", "a nascente"))):
    y = 0.495 - i * 0.075
    axl.add_patch(plt.Rectangle((0.03, y - 0.030), 0.055, 0.048,
                                transform=axl.transAxes, facecolor="none",
                                edgecolor=TINTA, lw=1.2, zorder=3))
    axl.text(0.0575, y - 0.006, l, fontsize=10.5, weight="bold", color=TINTA,
             ha="center", va="center", transform=axl.transAxes, zorder=4)
    axl.text(0.11, y - 0.006, txt, fontsize=8.2, color=TINTA2, ha="left",
             va="center", transform=axl.transAxes)

axl.text(0.02, 0.30,
         "Perguntamos porque temos um\nficheiro interno com o nome\ntrocado, e queremos corrigi-lo\n"
         "antes de escrever seja o que for.\n\nOs dois discos têm o mesmo raio\ne o mesmo peso de desenho:\n"
         "nenhum está assinalado como\nresposta.",
         fontsize=7.4, color=TINTA3, va="top", ha="left", style="italic",
         transform=axl.transAxes, linespacing=1.55)

# o rodape institucional saiu: colidia com os rotulos de coordenada do eixo, e
# a cartela do topo ja identifica a origem. Uma carta nao repete a assinatura.

out = os.path.join(AQUI, "P13_qual_e_a_zona0.png")
fig.savefig(out, dpi=200, facecolor=PAPEL)
print("escrito %s" % out)
