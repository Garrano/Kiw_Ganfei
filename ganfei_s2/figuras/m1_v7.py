# -*- coding: utf-8 -*-
"""M1 v7 — a propria Implantacao Geral como mapa. Para a gestora.

REGRA INEGOCIAVEL, desde a v1: zero informacao sobre declinio.

Porque a v7 abandona a reconstrucao
-----------------------------------
As versoes 1 a 6 tentaram reconstruir a planta sobre a imagem de satelite, por
quatro metodos. O ultimo funciona (valvulas colocadas por area acumulada, com a
valvula 8 a 34 m do ponto que o gestor nomeou), mas para o efeito de OBTER
CONFIRMACAO isso e o instrumento errado: pede-se a alguem que confirme um
desenho nosso, feito por um metodo que ele nao tem como julgar.

A Implantacao Geral e o documento dele. Tem legenda, tem os sectores
desenhados, tem os limites do terreno, esta a 1/3500 e foi verificada por
Dario Faria em Jul/2009. Confirmar contra ela e uma tarefa que ele pode fazer
de facto.

Esta versao mostra a planta como esta, junta a tabela de areas que ele deu, e
pergunta o que falta. A nossa colocacao por area fica de fora — se aparecer
aqui, deixa de ser confirmacao independente e passa a ser concordancia
induzida.
"""
import os
import textwrap
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
CORB = {"B1": "#c2451e", "B2": "#2a78d6", "Erica Novo": "#7a4fbf",
        "B3": "#eb6834", "B4": "#0a7a0a", "outras": "#6f6d66"}

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PLANTA = "../_rega_400.png"

TAB = [("B1", "1", 13500), ("B1", "2", 9375), ("B1", "3", 12750),
       ("B1", "4", 24550), ("B1", "5", 29900),
       ("B2", "6", 25000), ("B2", "7", 25100), ("B2", "8", 28200),
       ("B2", "9", 18200),
       ("Erica Novo", "10", 24000), ("Erica Novo", "11", 24650),
       ("B3", "12", 27500), ("B3", "13", 25300), ("B3", "14", 25850),
       ("B3", "15", 11400),
       ("B4", "16", 17300), ("B4", "17", 20500),
       ("outras", "18 · B4C3", 5500), ("outras", "19 · B5", 12500),
       ("outras", "20 · B1C5", 23000), ("outras", "21 · B3C4", 2300),
       ("outras", "22 · viveiro", 10400), ("outras", "23 · viveiro", 1500),
       ("outras", "24 e 25 · B1C6", 17000), ("outras", "27 · B3C3", 14000)]
TOT = sum(a for _, _, a in TAB)

im = Image.open(PLANTA).convert("RGB")
planta = np.asarray(im.crop((80, 60, 4460, 1820)))

fig = plt.figure(figsize=(18.0, 12.8), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.034, 0.980, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.034, 0.953, "M1 · A sua planta de implantação, e o que falta nela",
         fontsize=20, color=TINTA, fontweight="bold")
fig.text(0.966, 0.958, "M1 v7 · 28-08-2026", fontsize=8, color=TINTA3,
         ha="right")
fig.text(0.034, 0.921,
         "Trabalhámos sobre a sua planta em vez de fazermos outra. É ela que tem "
         "os sectores desenhados, os limites do terreno e a escala. As nossas "
         "medições de satélite ficam de fora desta folha de propósito — "
         "queremos que a confirmação seja sua, não nossa.",
         fontsize=9.2, color=TINTA2)

ax = fig.add_axes([0.034, 0.470, 0.700, 0.432])
ax.imshow(planta)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.9)
ax.text(0.006, 0.028,
        "PRILUX · «Sistema de rega para espaços verdes» · Implantação Geral · "
        "ESC 1/3500 @ A1 · JUL/09 · verif. Dario Faria",
        transform=ax.transAxes, fontsize=6.8, color=TINTA2, va="bottom",
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=RISCA, lw=0.8,
                  alpha=0.92))

axt = fig.add_axes([0.752, 0.470, 0.214, 0.432])
axt.set_xlim(0, 1); axt.set_ylim(0, 1); axt.set_axis_off()
axt.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA, lw=0.8))
axt.text(0.055, 0.972, "A SUA TABELA DE ÁREAS", fontsize=8.4, color=TINTA,
         fontweight="bold", va="top")
axt.text(0.055, 0.946, "25 válvulas · 44,93 ha", fontsize=7.0, color=TINTA2,
         va="top")
y = 0.905
bloco_ant = None
for b, v, a in TAB:
    if b != bloco_ant:
        y -= 0.008
        sub = sum(x[2] for x in TAB if x[0] == b)
        axt.text(0.055, y, "%s — %.2f ha" % (b, sub / 1e4), fontsize=7.0,
                 color=CORB[b], fontweight="bold", va="top")
        y -= 0.026
        bloco_ant = b
    axt.add_patch(Rectangle((0.075, y - 0.014), 0.020, 0.013,
                            facecolor=CORB[b], edgecolor="none"))
    axt.text(0.112, y, v, fontsize=6.6, color=TINTA, va="top")
    axt.text(0.945, y, "%s m²" % format(a, ",").replace(",", " "),
             fontsize=6.6, color=TINTA2, va="top", ha="right")
    y -= 0.0208
axt.plot([0.055, 0.945], [y - 0.004, y - 0.004], color=TINTA3, lw=0.9)
axt.text(0.055, y - 0.022, "TOTAL", fontsize=7.4, color=TINTA,
         fontweight="bold", va="top")
axt.text(0.945, y - 0.022, "449 275 m²", fontsize=7.4, color=TINTA,
         fontweight="bold", va="top", ha="right")

fig.text(0.034, 0.436, "O QUE A PLANTA JÁ RESOLVE", fontsize=8.8, color=TINTA,
         fontweight="bold")
CX = [(BOM, "É um levantamento, não um esboço",
       "Cartucho: PRILUX, Implantação Geral, escala 1/3500 em A1, Julho de "
       "2009, verificada. Tem legenda própria: electroválvula, ponto de "
       "abastecimento, sector de rega, conduta principal, limites do terreno."),
      (BOM, "E a tabela fecha com ela",
       "As 25 válvulas somam 449.275 m² = 44,93 ha. Os sectores desenhados na "
       "planta e as áreas da tabela são o mesmo sistema, e é isso que nos "
       "permite trabalhar sem inventar nada."),
      (AVISO, "O que a planta tem de 2009",
       "Foi desenhada há dezassete anos. As anotações à mão por cima são "
       "posteriores e é por elas que sabemos das linhas, da válvula "
       "desactivada e das novas. É essa diferença que as perguntas tentam "
       "apanhar.")]
for i, (cor, tit, txt) in enumerate(CX):
    x = 0.034 + i * 0.3127
    axc = fig.add_axes([x, 0.306, 0.2927, 0.122])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axc.add_patch(Rectangle((0, 0.94), 1, 0.06, facecolor=cor,
                            edgecolor="none"))
    axc.text(0.032, 0.858, tit, fontsize=8.4, color=cor, fontweight="bold",
             va="top")
    axc.text(0.032, 0.686, "\n".join(textwrap.wrap(txt, 58)), fontsize=6.9,
             color=TINTA2, va="top", linespacing=1.6)

fig.text(0.034, 0.272, "O QUE MUDOU DESDE 2009 — e é o que precisamos",
         fontsize=8.8, color=TINTA, fontweight="bold")
PERG = [
    ("1.", "Marque na planta, à mão, o que já não corresponde: sectores que "
     "mudaram de tamanho, válvulas que saíram ou entraram, parcelas novas. "
     "Sabemos da válvula desactivada na linha 185 e das novas no B1C2 pelas "
     "suas notas — mas não sabemos se há mais."),
    ("2.", "Dentro do B1, onde acaba a válvula 1 e começam as 2 a 5? A tabela "
     "diz que a 1 tem 1,35 ha em 9,01 ha, e a planta mostra-a numa parcela "
     "destacada a sudoeste — mas não a fronteira. É a única separação de "
     "porta-enxerto do pomar."),
    ("3.", "A rede do B1: em que ano subiu e em que ano saiu? Se saiu com o "
     "Enza Gold, foi por volta de 2020 — o mesmo ano da enxertia da Erica, e "
     "nesse caso os dois efeitos ficam sobrepostos e não os conseguimos "
     "separar."),
    ("4.", "O viveiro está na planta com 1 ha (válvulas 22 e 23, 11.900 m²). "
     "Cresceu desde 2009? E as outras parcelas soltas — B4C3, B5, B1C5, "
     "B3C4, B1C6, B3C3 — ficam onde? Uma coordenada de telemóvel por cada "
     "resolve, como fez para o armazém."),
    ("5.", "Os nomes: vimos B1C2, B1C3, B2-V7, B3-7ha em boletins de "
     "laboratório, e não constam da tabela. Como encaixam nos blocos da "
     "planta?"),
]
y = 0.246
for n, p in PERG:
    L = textwrap.wrap(p, 132)
    fig.text(0.034, y, n, fontsize=7.7, color=TINTA, fontweight="bold",
             va="top")
    fig.text(0.054, y, "\n".join(L), fontsize=7.7, color=TINTA2, va="top",
             linespacing=1.45)
    y -= 0.0140 * len(L) + 0.0072

fig.text(0.034, 0.012,
         "Esta folha não traz nenhuma informação sobre o estado das plantas, de "
         "propósito. As nossas medições existem e são-lhe mostradas a seguir — "
         "mas depois de a geometria estar fechada, não antes.",
         fontsize=7.4, color=TINTA3, style="italic")

fig.savefig("figuras/M1_implantacao_v7.png", facecolor=FUNDO,
            bbox_inches="tight")
fig.savefig("figuras/M1_implantacao_v7.svg", facecolor=FUNDO,
            bbox_inches="tight")
print("M1 v7 gravada — planta %dx%d px, tabela %d válvulas, %.2f ha"
      % (planta.shape[1], planta.shape[0], len(TAB), TOT / 1e4))
