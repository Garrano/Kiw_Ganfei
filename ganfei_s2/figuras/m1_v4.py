# -*- coding: utf-8 -*-
"""M1 v4 — Valvulas, colocadas por DUAS vias que discordam. Para a gestora.

REGRA INEGOCIAVEL, mantida: zero informacao sobre declinio. Nem cores, nem
marcas, nem texto. Nao ha aqui nenhuma mancha desenhada.

O que muda da v3
----------------
A v3 dizia "nao conseguimos colocar as valvulas, marque-as a senhora". Isso
era verdade com o metodo que tinha — ajustar a FORMA do desenho a parcela,
que dava 64 m de erro contra 49 m de espacamento.

As anotacoes a mao davam outra via, que nao estava a ser usada: os NUMEROS DE
LINHA. As linhas sao as fileiras da pergola e contam-se na ortofoto.

Ha agora duas colocacoes, e discordam em 469 m:

  METODO A — numeros de linha. As anotacoes dizem "valvula 6 e 7 / linhas 130
  e 131", "8 e 9 / 267-268", "10,11,12,13 / 306-307", "14 e 15 / 336-337",
  "16 / 409", "17 / 423". Sao 292,5 intervalos entre a primeira e a ultima.
  O compasso das fileiras, medido na ortofoto por autocorrelacao radial numa
  sessao que nao conhecia estes numeros, e 5,00 m. Ora 292,5 x 5,00 = 1462 m,
  e a parcela mede 1458 m — 0,3% de erro. E as valvulas 10-13 caem a 1 m do
  centro da Zona 0, que a gestora tinha situado nas "valvulas 8, 9 e 10" sem
  que isso fosse usado para as colocar.

  METODO B — geometria relativa do desenho, com a mesma ancoragem nos extremos.
  Le as posicoes dos circulos no desenho e transporta-as para o terreno.

O DESENHO NAO ESTA A ESCALA. O cartucho declara 1/3500 @ A1, o que daria
0,629 m por pixel a 400 dpi; o ajuste ancorado da 0,788 — 25% de diferenca.
Por isso os dois metodos nao podem ser reconciliados por escala nenhuma, e por
isso se mostram os dois.
"""
import json
import os
import textwrap
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, FancyArrowPatch

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
VA, VB = "#2a78d6", "#7a4fbf"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (528780, 4653950, 531760, 4655500)

A = json.load(open("valvulas_por_linha.json"))["valvulas"]
ROT = {130.5: "6 e 7", 267.5: "8 e 9", 306.5: "10 a 13",
       336.5: "14 e 15", 409.0: "16", 423.0: "17"}
V4 = json.load(open("valvulas_v4.json"))
B, LOBO = V4["corpo"], V4["lobo_oeste"]
g = json.load(open("sentinel/masks_geograficas.json"))
POMAR = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)

ds = rasterio.open("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
Wo = transform_bounds("EPSG:32629", ds.crs, *W)
w = from_bounds(*Wo, transform=ds.transform)
im = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32") / 255.0
im = np.dstack([im.mean(2) * 0.5 + 0.46] * 3)

fig = plt.figure(figsize=(17.8, 12.6), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.038, 0.979, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.038, 0.952, "M1 · Onde ficam as válvulas — duas leituras que discordam",
         fontsize=20, color=TINTA, fontweight="bold")
fig.text(0.962, 0.957, "M1 v4 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.038, 0.918,
         "Conseguimos agora colocar as válvulas por duas vias independentes. Elas "
         "concordam nos extremos e discordam no meio — 469 m, cerca de dez "
         "posições de válvula. Precisamos que nos diga qual está certa.",
         fontsize=9.2, color=TINTA2)

ax = fig.add_axes([0.038, 0.352, 0.925, 0.545])
ax.imshow(im, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)
ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
           np.linspace(AOI[3] - 5, AOI[1] + 5, 100),
           POMAR.astype(float), [0.5], colors=[TINTA], linewidths=2.0)

for r in A:
    ax.add_patch(Circle((r["E"], r["N"]), 25, facecolor=VA, alpha=0.20,
                        edgecolor=VA, lw=1.0, zorder=4))
    ax.plot([r["E"]], [r["N"]], "o", color=VA, ms=6, zorder=5,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.text(r["E"], r["N"] + 46, ROT[r["linha"]], fontsize=7.4, color=VA,
            ha="center",
            fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=VA, lw=0.7,
                      alpha=0.92))
for v in sorted(B, key=lambda k: int(k)):
    x, y = B[v]
    ax.plot([x], [y], "s", color=VB, ms=5, zorder=5, markeredgecolor="white",
            markeredgewidth=0.9)
    ax.text(x, y - 58, v, fontsize=6.8, color=VB, ha="center",
            fontweight="bold", zorder=6)

Eb = np.array([LOBO[v][0] for v in LOBO]); Nb = np.array([LOBO[v][1] for v in LOBO])
ax.add_patch(Ellipse((Eb.mean(), Nb.mean()), 620, 380, angle=20,
                     facecolor=CRIT, alpha=0.09, edgecolor=CRIT, lw=1.6,
                     ls=(0, (6, 4)), zorder=4))
for dx in (-1, 1):
    ax.plot([Eb.mean() - dx * 300, Eb.mean() + dx * 300],
            [Nb.mean() - 185, Nb.mean() + 185], color=CRIT, lw=2.6, zorder=6)
ax.text(Eb.mean(), Nb.mean() + 300,
        "ONDE O DESENHO PORIA AS VÁLVULAS 1–5\nREFUTADO: atravessa 306 m de rio",
        fontsize=7.8, color=CRIT, ha="center", va="bottom", fontweight="bold",
        linespacing=1.4, zorder=7,
        bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=CRIT, lw=1.4,
                  alpha=0.95))
ax.annotate("", xy=(Eb.mean() + 260, Nb.mean() + 190),
            xytext=(530120, 4654860),
            arrowprops=dict(arrowstyle="<-", color=CRIT, lw=1.2,
                            ls=(0, (5, 3)), alpha=0.6), zorder=4)
ax.add_patch(Ellipse((529890, 4654345), 700, 500, angle=25, facecolor=BOM,
                     alpha=0.13, edgecolor=BOM, lw=1.8, zorder=4))
ax.text(529890, 4654345 - 300,
        "único bloco de pomar na margem certa,\nnesta direcção — 13,6 ha",
        fontsize=7.6, color=BOM, ha="center", va="top", fontweight="bold",
        linespacing=1.4, zorder=7,
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=BOM, lw=1.0,
                  alpha=0.94))

ax.plot([W[0] + 90, W[0] + 90 + 300], [W[1] + 70] * 2, color=TINTA, lw=2.6)
ax.text(W[0] + 240, W[1] + 88, "300 m", fontsize=8, color=TINTA, ha="center",
        fontweight="bold")
ax.text(W[2] - 20, W[1] + 20, "ortofoto DGT 2025, 25 cm, esbatida · norte em "
        "cima · contorno = pomar medido por estrutura de pérgola",
        fontsize=6.6, color=TINTA2, ha="right", va="bottom")
for cor, marca, rot, y in ((VA, "o", "A · pelos números de linha das suas "
                            "anotações", 0.955),
                           (VB, "s", "B · pela geometria do desenho", 0.915)):
    ax.plot([W[0] + 120], [W[1] + (W[3] - W[1]) * y], marca, color=cor, ms=8,
            markeredgecolor="white", markeredgewidth=1.2, zorder=8)
    ax.text(W[0] + 175, W[1] + (W[3] - W[1]) * y, rot, fontsize=8.2, color=cor,
            va="center", fontweight="bold", zorder=8,
            bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=cor, lw=0.8,
                      alpha=0.93))

# ------------------- caixas -------------------------------------------------
fig.text(0.038, 0.318, "PORQUE HÁ DUAS LEITURAS", fontsize=8.8, color=TINTA,
         fontweight="bold")
CAIXAS = [
    (VA, "A · NÚMEROS DE LINHA",
     "As suas anotações dizem em que linha fica cada válvula: 130-131 para a 6 "
     "e 7, até 423 para a 17. São 292,5 fileiras. O compasso medido na "
     "ortofoto é 5,00 m, e 292,5 × 5,00 = 1462 m contra 1458 m que a parcela "
     "mede. Erro de 0,3%."),
    (VB, "B · GEOMETRIA DO DESENHO",
     "Lê onde estão os círculos no papel e transporta-os para o terreno, com a "
     "mesma ancoragem nos dois extremos. É o método natural, e é o que dá "
     "diferente: as válvulas ficam todas mais a oeste."),
    (CRIT, "NÃO ESTÁ À ESCALA — e prova-se",
     "O cartucho declara 1/3500 @ A1, que daria 0,629 m por pixel; o ajuste "
     "ancorado dá 0,788 — 25% a mais. Prova: estendendo o desenho para oeste, "
     "as válvulas 1–5 caem do OUTRO LADO DO RIO, com 306 m de água pelo meio. "
     "O desenho não é fiável fora do troço ancorado."),
]
for i, (cor, tit, txt) in enumerate(CAIXAS):
    x = 0.038 + i * 0.3123
    axc = fig.add_axes([x, 0.186, 0.2923, 0.124])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axc.add_patch(Rectangle((0, 0.94), 1, 0.06, facecolor=cor, edgecolor="none"))
    axc.text(0.032, 0.860, tit, fontsize=8.4, color=cor, fontweight="bold",
             va="top")
    axc.text(0.032, 0.690, "\n".join(textwrap.wrap(txt, 58)), fontsize=6.9,
             color=TINTA2, va="top", linespacing=1.6)

fig.text(0.038, 0.152, "A PERGUNTA QUE FECHA ISTO", fontsize=8.8, color=TINTA,
         fontweight="bold")
fig.text(0.038, 0.126,
         "1.  Vá à válvula 10 e diga-nos onde está. Nós temos duas hipóteses a "
         "469 m uma da outra: E 530999 ou E 530530. Uma delas está certa e a "
         "outra não, e isso decide todas as restantes.",
         fontsize=7.9, color=TINTA)
PERG = [
    "2.  As válvulas 1 a 5: o desenho, esticado, põe-nas dentro de Valença, do "
    "outro lado do rio — impossível. O bloco a verde é o único pomar na margem "
    "certa nessa direcção. É esse? Pertence à exploração?",
    "3.  Confirma a leitura das anotações: «válvula 6 e 7, linhas 130 e 131» "
    "quer dizer o par de válvulas assente entre essas duas fileiras?",
    "4.  As fileiras estão numeradas de oeste para leste? E a numeração do "
    "bloco a sudoeste é a mesma, ou recomeça?",
    "5.  O viveiro e a B3C3 ficam dentro desta imagem ou fora — e para que lado?",
]
for i, p in enumerate(PERG):
    fig.text(0.038, 0.098 - i * 0.0215, p, fontsize=7.9, color=TINTA2)

fig.text(0.038, 0.008,
         "NOTA. Uma confirmação independente já existe e favorece o método A: as "
         "válvulas 10 a 13 caem a 1 m do centro de uma zona que a senhora tinha "
         "situado «nas válvulas 8, 9 e 10», e essa frase não foi usada para as "
         "colocar. Mas uma frase não fecha 469 m — por isso a pergunta 1.",
         fontsize=7.6, color=TINTA2, style="italic")

fig.savefig("figuras/M1_valvulas_v4.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M1_valvulas_v4.svg", facecolor=FUNDO, bbox_inches="tight")
print("M1 v4 gravada — %d pontos metodo A, %d metodo B, %d extrapolados"
      % (len(A), len(B), len(LOBO)))
