# -*- coding: utf-8 -*-
"""P08 — o plano de Setembro. Onde ir, o que colher, e o que cada ponto decide.

PROVENIENCIA, E A CORRECCAO QUE A PRE-VOO EXIGIU
------------------------------------------------
Deriva da F14, confrontada com o registo antes de ser composta. **Uma linha
nao passou.** A F14 listava, entre as correccoes que o rastreio exigira, «a
pergunta regional como CONDICAO DE ARRANQUE, nao como tarefa».

Essa condicao **esta fechada desde 01-09-2026**, e fechou duas vezes: primeiro
ao contrario do esperado, depois — quando a ortofoto mostrou que cinco dos
blocos comparados tinham sido desmatados em 2024 — invertida outra vez. O
estado final, com 29 blocos de linha de base continua: **os dois focos desta
exploracao sao o pior e o segundo pior da regiao.**

E vai com o intervalo, porque sem ele nao e um facto: **P(a ordenacao estar
errada) = 0,07 pela reamostragem de cenas e 0,25 pela reamostragem de anos, e
retirada 2026 a conclusao cai.** Ver `REG01_RETRACCAO_A3.md` e o adversario em
`REG01_CONTROLO3_ADVERSARIO.md`.

O que isto muda no plano: **a campanha e nesta exploracao e so nesta.** A ideia
de por pontos em duas exploracoes vinha do A3 retirado e cai com ele. E a
condicao de arranque deixa de travar: agora suporta a medida de parcela.

O QUE A F14 JA DIZIA, E QUE SE MANTEM
=====================================

O que a figura tem de fazer
---------------------------
Transformar «faltam ensaios» em «e isto, custa isto, e responde a isto».

E o unico desenho deste caso em que **cada ponto tem escrito, antes de existir,
o que se conclui se der positivo e o que se conclui se der negativo**. Sem isso
nao e desenho, e confirmacao.

A honestidade que a figura tem de respeitar
-------------------------------------------
**O transecto NAO tem coordenada nossa.** O centro e a orla sao o que o gestor
apontar no terreno, no dia. Nao se desenha ali um ponto: desenha-se uma zona e
diz-se porque. Usar o centro que o satelite calculou seria ancorar a colheita
no proprio sinal que se vai medir — o erro fundador deste caso.

As tres outras unidades tem coordenada, e vem do ficheiro operativo de
valvulas, nao de anomalia de imagem.

O que esta figura acrescenta ao desenho da camada de decisao
------------------------------------------------------------
Quatro correccoes que o adversario dessa camada exigiu e que ela nao chegou a
aplicar, marcadas a laranja: **painel foliar** (o desenho tinha zero amostras de
folha, e a perna foliar e a unica comparacao com padrao externo do caso);
**segunda radial a 90 graus obrigatoria** (estava «opcional», e e o que
distingue propagacao de mancha estatica); **controlo de proximidade no B3**; e
**a pergunta regional como condicao de arranque**, nao como tarefa.
"""
import csv
import io
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, FancyBboxPatch, Wedge

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C5 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C5"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"

masc, _ = carrega_mascaras()
POMAR = masc["pomar"]
H = np.load(os.path.join(VG, "chm_altura.npy"))
AM = list(csv.DictReader(io.open(os.path.join(C5, "c5_amostragem.csv"),
                                 encoding="utf-8-sig"), delimiter=";"))

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, RISCA = "#fbfbfa", "#e6e3dd"
T1C = "#0072B2"     # transecto
U2C = "#D55E00"     # foco oriental
SAO = "#2f6b52"     # pares sãos
NOVO = "#CC79A7"    # o que esta figura acrescenta

verde = LinearSegmentedColormap.from_list(
    "c", ["#f4f6f2", "#dfe8da", "#c2d6bb", "#a7c49f"])

fig = plt.figure(figsize=(15.2, 9.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.030, 0.075, 0.505, 0.735])
axd = fig.add_axes([0.560, 0.075, 0.425, 0.735]); axd.axis("off")

ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
ax.imshow(np.where(POMAR, H, np.nan), extent=ext, cmap=verde, vmin=0, vmax=2.6,
          interpolation="nearest")
ax.imshow(np.where(POMAR & np.isfinite(H) & (H < 0.5), 1.0, np.nan), extent=ext,
          cmap=matplotlib.colors.ListedColormap(["#e8d6c6"]), vmin=0, vmax=1,
          interpolation="nearest")

UNI = [("U3", 530260.3, 4654936.1, SAO, "PAR SÃO ocidental\nv6 · B2"),
       ("U2", 530977.0, 4655117.0, U2C, "FOCO oriental\nv13 · v14 · B3"),
       ("U4", 531394.7, 4655341.8, SAO, "PAR SÃO oriental\nv17 · B4")]
for nome, x, y, cor, rot in UNI:
    ax.add_patch(Circle((x, y), 62, fc=cor, ec="white", lw=2.0, alpha=0.90,
                        zorder=6))
    ax.text(x, y, nome, ha="center", va="center", fontsize=11.5, color="white",
            fontweight="bold", zorder=7)
    dy = -96 if nome in ("U2", "U3") else 96
    ax.annotate(rot, (x, y + dy), ha="center",
                va="bottom" if dy > 0 else "top", fontsize=8.8, color=cor,
                fontweight="bold", linespacing=1.5, zorder=7)

# o transecto: zona, nao ponto
zx, zy = 530485.0, 4655053.0
ax.add_patch(Circle((zx, zy), 150, fill=False, ec=T1C, lw=2.2,
                    ls=(0, (5, 4)), zorder=6))
ax.text(zx, zy + 168, "T1  ·  TRANSECTO", ha="center", va="bottom",
        fontsize=11.5, color=T1C, fontweight="bold", zorder=7)
# A nota da ancora estava por baixo do circulo do T1 e caia por cima da
# etiqueta do U3, que ocupa esse canto. Passa para a direita do circulo, onde
# ha campo livre, e alinha a esquerda.
ax.text(zx + 178, zy - 96,
        "âncora de CAMPO, não nossa\no centro e a orla são\no que o gestor apontar no dia",
        ha="left", va="top", fontsize=8.5, color=T1C, linespacing=1.55,
        zorder=7, style="italic")
for k, (r_, lab) in enumerate(((-88, "centro"), (0, "orla"), (96, "fora"))):
    ax.plot([zx + r_], [zy], "o", ms=9.5, color=T1C, mec="white", mew=1.6,
            zorder=8)
    ax.text(zx + r_, zy + 22, lab, ha="center", va="bottom",
            fontsize=8.6, color=T1C, zorder=8, fontweight="bold")
ax.annotate("", xy=(zx + 128, zy), xytext=(zx - 112, zy),
            arrowprops=dict(arrowstyle="->", lw=1.6, color=T1C), zorder=7)
ax.add_patch(Wedge((zx, zy), 150, 78, 102, fc=NOVO, alpha=0.22, lw=0, zorder=5))
ax.annotate("2.ª radial a 90°\nOBRIGATÓRIA", (zx, zy + 150), xytext=(-96, 16),
            textcoords="offset points", ha="center", fontsize=8.2, color=NOVO,
            fontweight="bold", linespacing=1.5, zorder=8)

ax.set_xlim(AOI[0] + 130, AOI[2] - 260); ax.set_ylim(AOI[1] + 230, AOI[3] - 110)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.plot([AOI[0] + 1330, AOI[0] + 1530], [AOI[1] + 280, AOI[1] + 280],
        color=TINTA, lw=2.4, solid_capstyle="butt")
ax.text(AOI[0] + 1430, AOI[1] + 292, "200 m", ha="center", va="bottom",
        fontsize=8.4, color=TINTA)

# --------------------------------------------------------- painel de decisão
axd.set_xlim(0, 1); axd.set_ylim(0, 1)
LIN = [
    ("T1", T1C, "TRANSECTO no vazio de terreno",
     "3 plantas · centro, orla, fora",
     "gradiente centro→orla→fora, ou orla acima do centro:\nassinatura de agente de solo em propagação",
     "as nove presenças do 331/2025 não reproduzem\nno próprio vazio — resultado FORTE"),
    ("U2", U2C, "FOCO oriental",
     "3 plantas · só onde há pérgola",
     "MESMO agente que T1: um problema, duas expressões.\nAgente DIFERENTE: o dossiê separa-se em dois",
     "o lado oriental fica sem suporte biótico e a hipótese\nde operação de gestão sobe sozinha ao topo"),
    ("U3", SAO, "PAR SÃO ocidental  ·  v6",
     "3 plantas · mesmo bloco, mesma água",
     "o agente está também onde não há défice:\nDEIXA DE EXPLICAR o padrão e sai da lista",
     "o organismo passa a ter contraste de lugar a duas\nescalas — e é o único que merece segunda época"),
    ("U4", SAO, "PAR SÃO oriental  ·  v17",
     "3 plantas · outro bloco, outro terreno",
     "idem U3, para o lado oriental",
     "idem U3, para o lado oriental"),
]
y = 0.975
for cod, cor, tit, sub, pos, neg in LIN:
    axd.add_patch(FancyBboxPatch((0.005, y - 0.088), 0.075, 0.072,
                                 boxstyle="round,pad=0.008,rounding_size=0.02",
                                 fc=cor, ec="none", transform=axd.transData))
    axd.text(0.0425, y - 0.052, cod, ha="center", va="center", fontsize=12.5,
             color="white", fontweight="bold")
    axd.text(0.10, y, tit, fontsize=11.4, color=TINTA, fontweight="bold",
             va="top")
    axd.text(0.10, y - 0.030, sub, fontsize=8.6, color=TINTA3, va="top")
    axd.text(0.10, y - 0.068, "se POSITIVO", fontsize=7.8, color=cor,
             fontweight="bold", va="top")
    axd.text(0.245, y - 0.068, pos, fontsize=8.5, color=TINTA2, va="top",
             linespacing=1.55)
    axd.text(0.10, y - 0.140, "se NEGATIVO", fontsize=7.8, color=TINTA3,
             fontweight="bold", va="top")
    axd.text(0.245, y - 0.140, neg, fontsize=8.5, color=TINTA2, va="top",
             linespacing=1.55)
    y -= 0.196
    axd.plot([0.005, 0.995], [y + 0.030, y + 0.030], lw=0.7, color=RISCA)

axd.text(0.005, y - 0.010, "E QUATRO CORRECÇÕES QUE O RASTREIO EXIGIU",
         fontsize=9.4, color=NOVO, fontweight="bold", va="top")
axd.text(0.005, y - 0.052,
         "painel FOLIAR em todas as 12 plantas — o desenho tinha zero amostras de folha,\n"
         "e a perna foliar é a única comparação com padrão externo de todo o caso\n"
         "segunda radial a 90° obrigatória  ·  controlo de proximidade no B3\n"
         "a pergunta regional — CORRIDA e FECHADA a 01-09: destas 29 parcelas de\n"
         "base contínua, as duas desta exploração são a pior e a segunda pior.\n"
         "P(ordenação errada) 0,07 a 0,25; retirado 2026, cai. A campanha é AQUI",
         fontsize=8.4, color=TINTA2, va="top", linespacing=1.72)

# ------------------------------------------------------------------- títulos
n_pl = len({r["planta"] for r in AM})
n_am = len(AM)
mat = sorted({r["matriz"] for r in AM})
fig.text(0.030, 0.955, "O que fazer a seguir, e o que cada ponto decide",
         fontsize=22, fontweight="bold", color=TINTA)
fig.text(0.030, 0.915,
         "%d plantas · %d amostras · quatro matrizes (%s) · uma data · um laboratório."
         % (n_pl, n_am, ", ".join(mat)),
         fontsize=10.6, color=TINTA2)
fig.text(0.030, 0.884,
         "Cada ponto tem escrito, antes de existir, o que se conclui se der positivo e o que se conclui se der negativo.",
         fontsize=10.6, color=TINTA, fontweight="bold")

fig.text(0.030, 0.048,
         "O transecto não leva coordenada nossa: o centro e a orla são o que o gestor apontar no terreno, no dia. "
         "Ancorar a colheita no centro que o satélite calculou seria ancorá-la no próprio sinal que se vai medir.\n"
         "As outras três unidades vêm do ficheiro operativo de válvulas. A v6 e a v17 são as únicas duas da exploração com défice, declínio novo e chão lavrado TODOS a zero — "
         "e nenhuma colheita deste caso teve alguma vez um assintomático.\n"
         "Duas leituras de GPS, no centro e na orla, dizem se o vazio que o gestor vê e o núcleo que o satélite mede são o mesmo objecto. Hoje são dois objectos com o mesmo nome.",
         fontsize=7.9, color=TINTA3, linespacing=1.85, va="top")

fig.savefig(os.path.join(AQUI, "P08_plano_de_setembro.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
fig.savefig(os.path.join(AQUI, "P08_plano_de_setembro.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
print("escrito P08 — %d plantas, %d amostras, matrizes: %s" % (n_pl, n_am, mat))
