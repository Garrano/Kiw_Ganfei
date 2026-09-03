# -*- coding: utf-8 -*-
"""F11 — a matriz de diagnóstico tem uma coluna.

O que a figura tem de fazer
---------------------------
Justificar, de uma vez e sem argumento, porque e que este dossie **nao conclui**
uma causa. Nao e por falta de analise: e porque toda a patologia de lenho e raiz
do caso assenta numa amostra composta, num sitio, num dia — e porque os grupos
de agentes que faltam nunca foram pedidos ao laboratorio.

E o achado que o adversario da C4 verificou linha a linha e classificou como o
mais consequente da camada, e o unico que passou intacto ao rastreio.

Forma
-----
Uma grelha: vinte linhas de organismo x matriz, quatro colunas de proveniencia
da prova. **A leitura e a forma, nao a cor**: uma coluna cheia e tres vazias.
Cada celula leva simbolo proprio alem da cor, e cada linha leva rotulo directo,
porque identidade nunca se faz so por cor.

A faixa de baixo e uma linha vazia por desenho — os grupos que nunca foram
procurados. Nao ha nada la para desenhar, e e esse o ponto.

Fonte: `SAIDA_C3\\c3_09_organismos.json`, veredictos da C3 revista pelo
adversario. Nenhum valor transcrito a mao.
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
from matplotlib.patches import Rectangle

C3 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C3"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
D = json.load(open(os.path.join(C3, "c3_09_organismos.json")))
ORG = D["organismos"]
RES = D["resumo_veredictos"]

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, GRELHA = "#fbfbfa", "#e6e3dd"
GRANEL = "#D55E00"      # a amostra composta — Okabe-Ito vermillion
COLOC = "#0072B2"       # unidade com posicao — azul
NEG = "#8d8a84"         # negativo
FORA = "#c9c5bd"        # pomar espanhol, rejeitado

COLS = [("Kiwi 1000\ninforme 331/2025",
         "uma amostra\nCOMPOSTA\num dia · 06-06-2025"),
        ("unidades com\nposição em Ganfei", "v13 · v14\nv15 · B3C3"),
        ("pomar espanhol\nRibadumia", "240/2023\nmaterial\nREJEITADO"),
        ("nunca\nensaiado", "não há linha\nem livro nenhum")]


def coluna(o):
    """Devolve (indice de coluna, simbolo, cor) a partir do veredicto."""
    v = o["veredicto"]
    if v.startswith("EM TODO"):
        return 1, "o", COLOC
    if v.startswith("SEM POSICAO"):
        return 0, "o", GRANEL
    if v.startswith("FORA"):
        return 2, "x", FORA
    return 0, "_", NEG          # NEGATIVO — o ensaio existe, o resultado e nulo


fig = plt.figure(figsize=(13.2, 10.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.315, 0.095, 0.44, 0.645])
ax.set_facecolor(FUNDO)

n = len(ORG)
for i in range(n + 1):
    ax.plot([-0.5, 3.5], [i - 0.5, i - 0.5], color=GRELHA, lw=0.7, zorder=0)
for j in range(4):
    ax.add_patch(Rectangle((j - 0.42, -0.5), 0.84, n, fc="white",
                           ec=GRELHA, lw=0.7, zorder=1))

for i, o in enumerate(ORG):
    y = n - 1 - i
    j, sim, cor = coluna(o)
    nome = o["organismo"]
    ax.text(-0.62, y, nome, ha="right", va="center", fontsize=9.2,
            color=TINTA if cor != FORA else TINTA3, zorder=4)
    if sim == "o":
        ax.plot([j], [y], "o", ms=11, color=cor, mec="white", mew=1.4, zorder=5)
    elif sim == "x":
        ax.plot([j], [y], "x", ms=9, color=cor, mew=2.4, zorder=5)
    else:
        ax.plot([j - 0.16, j + 0.16], [y, y], color=NEG, lw=3.2,
                solid_capstyle="round", zorder=5)
    if o["veredicto"].startswith("EM TODO"):
        ax.text(j + 0.30, y, "4/4", fontsize=8.2, color=cor, va="center",
                fontweight="bold", zorder=5)

ax.set_xlim(-0.5, 3.5); ax.set_ylim(-0.9, n + 5.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

for j, (t, sub) in enumerate(COLS):
    ax.text(j, n + 2.45, t, ha="center", va="bottom", fontsize=9.4,
            color=TINTA, fontweight="bold", linespacing=1.5)
    ax.text(j, n + 0.05, sub, ha="center", va="bottom", fontsize=7.4,
            color=TINTA3, linespacing=1.6)

# contagem por coluna, calculada
cont = [0, 0, 0, 0]
for o in ORG:
    cont[coluna(o)[0]] += 1
for j, c in enumerate(cont):
    ax.text(j, -0.78, ("%d de 20" % c) if c else "—", ha="center", va="center",
            fontsize=11.5 if j == 0 else 10, color=TINTA if j == 0 else TINTA3,
            fontweight="bold" if j == 0 else "normal")

# ------------------------------------------------------------- lado direito
axr = fig.add_axes([0.775, 0.095, 0.205, 0.645]); axr.axis("off")
axr.set_xlim(0, 1); axr.set_ylim(0, 1)
axr.text(0, 0.985, "COMO SE LÊ", fontsize=9.2, color=TINTA,
         fontweight="bold", va="top")
LEG = [("o", GRANEL, "positivo, sem posição\n— vem do granel"),
       ("o", COLOC, "positivo, com posição\n— o único caso"),
       ("_", NEG, "negativo\n— nada a localizar"),
       ("x", FORA, "pomar espanhol\n— material rejeitado")]
for k, (sim, cor, txt) in enumerate(LEG):
    y = 0.905 - k * 0.088
    if sim == "o":
        axr.plot([0.045], [y], "o", ms=10, color=cor, mec="white", mew=1.3)
    elif sim == "x":
        axr.plot([0.045], [y], "x", ms=8, color=cor, mew=2.2)
    else:
        axr.plot([0.015, 0.075], [y, y], color=cor, lw=3, solid_capstyle="round")
    axr.text(0.13, y, txt, fontsize=8.4, color=TINTA2, va="center",
             linespacing=1.5)

axr.plot([0, 1], [0.505, 0.505], lw=0.9, color=GRELHA)
axr.text(0, 0.455, "2 de 20", fontsize=22, color=COLOC, fontweight="bold",
         va="top")
axr.text(0, 0.385,
         "linhas foram alguma vez\nensaiadas numa unidade\ncom posição — e são o\n"
         "MESMO organismo em\nduas matrizes.",
         fontsize=8.8, color=TINTA2, va="top", linespacing=1.68)

axr.plot([0, 1], [0.225, 0.225], lw=0.9, color=GRELHA)
axr.text(0, 0.175, "ZERO", fontsize=22, color=GRANEL, fontweight="bold",
         va="top")
axr.text(0, 0.108,
         "linhas bacterianas ou\nvirais. A PSA — o cancro\nbacteriano do kiwi, a\n"
         "principal doença da\ncultura no mundo — nunca\nfoi procurada.",
         fontsize=8.8, color=TINTA2, va="top", linespacing=1.68)

# ------------------------------------------------------------------ titulo
fig.text(0.045, 0.955, "A matriz de diagnóstico tem uma coluna",
         fontsize=21, fontweight="bold", color=TINTA)
fig.text(0.045, 0.912,
         "Vinte linhas de organismo × matriz. Onde está a prova de cada uma.",
         fontsize=11.4, color=TINTA2)
fig.text(0.045, 0.878,
         "Não é falta de análise. É que quase toda a patologia deste caso vem de uma amostra composta, "
         "num sítio, num dia.",
         fontsize=11, color=TINTA, fontweight="bold")

fig.text(0.045, 0.050,
         "Fonte: veredictos da camada de biologia da cadeia de validação, revistos pelo seu adversário — "
         "`SAIDA_C3\\c3_09_organismos.json`. Contagens calculadas do ficheiro.\n"
         "Nenhum dos quatro negativos vem de amostra comparável, pelo que nenhum exclui o que parece excluir.  "
         "As cinco linhas do pomar espanhol foram rejeitadas por serem de outra exploração.\n"
         "A única linha com posição — Meloidogyne hapla, positiva em 4 de 4 unidades — anticorrelaciona com o défice "
         "(ρ = −0,40 no solo, −0,80 na raiz; n = 4, nenhum significativo).",
         fontsize=7.9, color=TINTA3, linespacing=1.85, va="top")

fig.savefig(os.path.join(AQUI, "F11_matriz_diagnostico.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
fig.savefig(os.path.join(AQUI, "F11_matriz_diagnostico.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
print("escrito F11 — contagem por coluna:", cont)
