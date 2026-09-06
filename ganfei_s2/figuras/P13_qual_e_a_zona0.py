# -*- coding: utf-8 -*-
"""P13 — mapa C: onde e a Zona 0?

A PERGUNTA E FEITA POR FORMA, NAO POR FRASE.

A prancha nao traz nenhuma pergunta escrita no corpo. Traz:

  · dois discos identicos — mesmo raio, mesma espessura, mesmo tracejado, e
    tracejado porque uma linha interrompida le-se como provisoria, ao contrario
    de uma linha cheia, que le como estabelecida;
  · uma etiqueta A e B, neutra e geografica, sem juizo;
  · e ao lado de cada uma, uma **caixa vazia**. Uma caixa vazia junto de um
    rotulo e a interrogacao mais legivel que a cartografia tem: nao precisa de
    lingua nenhuma, e a pessoa sabe o que fazer com ela sem instrucoes.

O titulo faz o resto. Um titulo interrogativo e do registo da peca — nao e uma
nota de rodape a explicar o nosso trabalho.

O QUE NAO ESTA AQUI, DE PROPOSITO
---------------------------------
Nada do nosso processo. Nem metodo, nem ressalva, nem a razao interna por que
perguntamos. Quem le a carta decide olhando para o terreno, e o resto vive no
email e no registo.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "base"))
from carta_base import (cartela_institucional, fontes, Base, PAPEL, TINTA,  # noqa
                        TINTA2, TINTA3)

POENTE = (530485.0, 4655053.0)
NASCENTE = (530977.0, 4655117.0)
RAIO = 90.0

b = Base()
fig, ax, axl = b.figura(larg=16.0, rodape=0.72)
ytop = cartela_institucional(fig)

b.terreno(ax)
b.cadastro(ax)
b.sectores(ax)
b.rotulos(ax)
b.toponimos(ax)


def marcador(x, y, letra):
    """Disco tracejado + etiqueta + caixa vazia. A caixa e a pergunta."""
    ax.add_patch(Circle((x, y), RAIO, facecolor="#FFFFFF", alpha=0.14,
                        edgecolor="none", zorder=5))
    ax.add_patch(Circle((x, y), RAIO, facecolor="none", edgecolor=TINTA,
                        lw=2.4, ls=(0, (7, 4)), zorder=6))
    ax.plot([x], [y], marker="+", ms=12, mew=1.7, color=TINTA, zorder=8)

    # a etiqueta e a caixa, juntas, acima do disco
    yb = y + RAIO + 22
    ax.add_patch(FancyBboxPatch((x - 78, yb), 156, 62,
                                boxstyle="round,pad=0,rounding_size=8",
                                transform=ax.transData, facecolor=PAPEL,
                                edgecolor=TINTA3, lw=0.8, alpha=0.96, zorder=8))
    ax.text(x - 40, yb + 31, letra, fontsize=20, weight="bold", color=TINTA,
            ha="center", va="center", zorder=9)
    # a caixa vazia — o unico elemento interrogativo da prancha
    ax.add_patch(plt.Rectangle((x + 6, yb + 12), 38, 38, transform=ax.transData,
                               facecolor="#FFFFFF", edgecolor=TINTA, lw=2.0,
                               zorder=9))


marcador(*POENTE, letra="A")
marcador(*NASCENTE, letra="B")

# a distancia entre os dois, que e o facto que torna a escolha necessaria
ax.annotate("", xy=NASCENTE, xytext=POENTE,
            arrowprops=dict(arrowstyle="<->", color=TINTA2, lw=1.2,
                            shrinkA=RAIO + 5, shrinkB=RAIO + 5), zorder=7)
mx, my = (POENTE[0] + NASCENTE[0]) / 2, (POENTE[1] + NASCENTE[1]) / 2
ax.text(mx, my - 34, "500 m", fontsize=9.5, color=TINTA, weight="bold",
        ha="center", va="top", zorder=9,
        bbox=dict(boxstyle="round,pad=0.28", fc=PAPEL, ec=TINTA3, lw=0.7,
                  alpha=0.97))

b.moldura(ax)

# ── cabeçalho: o título faz a pergunta ──────────────────────────────────────
fig.text(0.035, ytop, "ONDE É A ZONA 0?", fontsize=23, weight="bold",
         color=TINTA, va="top", ha="left")
fig.text(0.035, ytop - 0.31 / fig.get_figheight(),
         "Emparcelamento de Ganfei, Valença",
         fontsize=10.5, color=TINTA2, va="top", ha="left")

# ── legenda: mínima. Repete os dois marcadores e não diz mais nada ──────────
axl.set_xlim(0, 1); axl.set_ylim(0, 1); axl.axis("off")
# um quadrado em fracção de eixo só sai quadrado se se corrigir pelo rácio da
# caixa do eixo — senão a legenda desmente o desenho, que é a pior coisa que
# uma legenda pode fazer.
# Para um rectangulo sair QUADRADO: largura_frac * W == altura_frac * H, logo
# altura_frac = largura_frac * W / H. A versao anterior multiplicava por H/W em
# vez de dividir, e as caixas sairam barras a atravessar a legenda inteira.
_bb = axl.get_window_extent()
_r = _bb.width / _bb.height          # <1 numa coluna alta e estreita
LADO = 0.052                      # lado do quadrado, em fracção de largura
for i, (l, onde) in enumerate((("A", "poente"), ("B", "nascente"))):
    y = 0.945 - i * 0.105
    axl.text(0.045, y, l, fontsize=18, weight="bold", color=TINTA,
             ha="center", va="center", transform=axl.transAxes, zorder=4)
    axl.add_patch(plt.Rectangle((0.10, y - LADO * _r / 2), LADO, LADO * _r,
                                transform=axl.transAxes, facecolor="#FFFFFF",
                                edgecolor=TINTA, lw=2.0, zorder=4))
    axl.text(0.185, y, onde, fontsize=9.5, color=TINTA2,
             ha="left", va="center", transform=axl.transAxes, zorder=4)

axl.text(0.045, 0.775, "Assinale uma.", fontsize=9.5, color=TINTA2,
         va="top", ha="left", transform=axl.transAxes)

fontes(fig, ["modelo de terreno LiDAR 50 cm, DGT",
             "parcelário IFAP 2025",
             "manchas: Sentinel-2, infravermelho próximo e vermelho"],
       y=0.012)

out = os.path.join(AQUI, "P13_qual_e_a_zona0.png")
fig.savefig(out, dpi=200, facecolor=PAPEL)
print("escrito %s" % out)
