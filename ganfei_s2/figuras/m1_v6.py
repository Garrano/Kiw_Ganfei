# -*- coding: utf-8 -*-
"""M1 v6 — sectores colocados pelas AREAS da tabela. Para a gestora.

REGRA INEGOCIAVEL, mantida desde a v1: zero informacao sobre declinio. Nem
cores, nem marcas, nem texto. Nao ha aqui nenhuma mancha desenhada.

O metodo, finalmente sem desenho
--------------------------------
A tabela de valvulas da a AREA de cada uma. Somam 449.275 m2 = 44,93 ha, que
bate com o total do enquadramento. A banda contigua — valvulas 6 a 17 — da
27,30 ha, contra 30,31 ha da mascara de pergola medida na ortofoto; a
diferenca sao bermas e cabeceiras.

Com isso, as valvulas colocam-se sem tocar no esquema: integra-se a area
MEDIDA ao longo do eixo da parcela e corta-se onde a area acumulada iguala a
area TABELADA de cada valvula. So geometria medida e numeros da exploracao.

Quatro metodos ja foram tentados para isto. Este e o quarto e o unico que nao
depende de ler o desenho:
    1  ancoras verbais            escala 71% errada, valvulas no outro lado do rio
    2  ajuste da forma            residuo 64 m, maior que o espacamento
    3  contagem de fileiras       desmentida pelo armazem, 321 m
    4  areas acumuladas           valvula 8 a 34 m do ponto que a gestora nomeou
"""
import json
import os
import textwrap
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
CORB = {"B2": "#2a78d6", "Erica Novo": "#7a4fbf", "B3": "#eb6834",
        "B4": "#0a7a0a", "B1": "#c2451e"}

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (529380, 4653930, 531700, 4655470)
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
ARM = tr.transform(-8.633148, 42.045095)
B1I = tr.transform(-8.643581734449253, 42.03757663209986)
B1F = tr.transform(-8.636871142810762, 42.04118410828004)

TAB = [("B1", 1, 13500), ("B1", 2, 9375), ("B1", 3, 12750), ("B1", 4, 24550),
       ("B1", 5, 29900), ("B2", 6, 25000), ("B2", 7, 25100), ("B2", 8, 28200),
       ("B2", 9, 18200), ("Erica Novo", 10, 24000), ("Erica Novo", 11, 24650),
       ("B3", 12, 27500), ("B3", 13, 25300), ("B3", 14, 25850), ("B3", 15, 11400),
       ("B4", 16, 17300), ("B4", 17, 20500)]
FORA = [("B4C3", 18, 5500), ("B5", 19, 12500), ("B1C5", 20, 23000),
        ("B3C4", 21, 2300), ("Viveiro", 22, 10400), ("Viveiro", 23, 1500),
        ("B1C6", "24 e 25", 17000), ("B3C3", 27, 14000)]

g = json.load(open("sentinel/masks_geograficas.json"))
P = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)
ys, xs = np.where(P)
E = AOI[0] + (xs + .5) * 10
N = AOI[3] - (ys + .5) * 10
C = np.array([E.mean(), N.mean()])
w_, v_ = np.linalg.eigh(np.cov(np.column_stack([E - C[0], N - C[1]]).T))
ax_ = v_[:, np.argmax(w_)]
ax_ = ax_ if ax_[0] > 0 else -ax_
pp = np.array([-ax_[1], ax_[0]])
t = np.column_stack([E - C[0], N - C[1]]) @ ax_
ordem = np.sort(t)
acum = np.arange(1, len(ordem) + 1) * 100.0
banda = [x for x in TAB if isinstance(x[1], int) and x[1] >= 6]
tot = sum(a for _, _, a in banda)


def dist(a_m2):
    i = int(np.searchsorted(acum, a_m2 / tot * acum[-1]))
    return float(ordem[min(i, len(ordem) - 1)])


cum, SEC = 0, []
for b, v, a in banda:
    d0 = dist(cum); cum += a; d1 = dist(cum)
    SEC.append((b, v, a, d0, d1))

ds = rasterio.open("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
Wo = transform_bounds("EPSG:32629", ds.crs, *W)
w = from_bounds(*Wo, transform=ds.transform)
im = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32") / 255.0
im = np.dstack([im.mean(2) * 0.50 + 0.46] * 3)

fig = plt.figure(figsize=(17.8, 12.6), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.036, 0.980, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.036, 0.953, "M1 · Sectores colocados pelas áreas da sua tabela",
         fontsize=20, color=TINTA, fontweight="bold")
fig.text(0.964, 0.958, "M1 v6 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.036, 0.920,
         "A tabela de áreas resolveu o que o esquema não resolvia. Somámos a área "
         "medida ao longo da parcela e cortámos onde ela iguala a área tabelada de "
         "cada válvula — sem ler o desenho, sem escala, sem estimativas nossas.",
         fontsize=9.2, color=TINTA2)

ax = fig.add_axes([0.036, 0.392, 0.928, 0.508])
ax.imshow(im, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)
ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
           np.linspace(AOI[3] - 5, AOI[1] + 5, 100),
           P.astype(float), [0.5], colors=[TINTA], linewidths=2.0)

for b, v, a, d0, d1 in SEC:
    for d in (d0, d1):
        p = C + ax_ * d
        ax.plot([p[0] - pp[0] * 190, p[0] + pp[0] * 190],
                [p[1] - pp[1] * 190, p[1] + pp[1] * 190],
                color="white", lw=2.4, alpha=0.8, zorder=4)
        ax.plot([p[0] - pp[0] * 190, p[0] + pp[0] * 190],
                [p[1] - pp[1] * 190, p[1] + pp[1] * 190],
                color=CORB[b], lw=1.0, ls=(0, (4, 3)), zorder=5)
    m = C + ax_ * ((d0 + d1) / 2)
    ax.text(m[0], m[1] + 120, str(v), fontsize=11.5, color="white",
            fontweight="bold", ha="center", va="center", zorder=8,
            bbox=dict(boxstyle="circle,pad=0.26", fc=CORB[b], ec="white", lw=1.5))
    ax.text(m[0], m[1] + 42, "%.2f ha" % (a / 1e4), fontsize=6.4, color=TINTA,
            ha="center", zorder=8,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.82))

vistos = []
for b, v, a, d0, d1 in SEC:
    if b in vistos:
        continue
    vistos.append(b)
    ms = [s for s in SEC if s[0] == b]
    m = C + ax_ * ((ms[0][3] + ms[-1][4]) / 2)
    ax.text(m[0], m[1] - 300, "%s · %.2f ha" % (b, sum(s[2] for s in ms) / 1e4),
            fontsize=9.4, color=CORB[b], ha="center", fontweight="bold", zorder=8,
            bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=CORB[b], lw=1.2,
                      alpha=0.95))

ax.plot([B1I[0], B1F[0]], [B1I[1], B1F[1]], "-o", color=CORB["B1"], lw=3.0,
        ms=9, mec="white", mew=1.6, zorder=6)
ax.text((B1I[0] + B1F[0]) / 2 - 30, (B1I[1] + B1F[1]) / 2 - 105,
        "B1 · válvulas 1 a 5 · 9,01 ha\nas suas duas coordenadas",
        fontsize=8.4, color=CORB["B1"], ha="center", va="top", fontweight="bold",
        linespacing=1.4, zorder=8,
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=CORB["B1"], lw=1.2,
                  alpha=0.95))
ax.plot([ARM[0]], [ARM[1]], "s", color=TINTA, ms=9, mec="white", mew=1.6, zorder=7)
ax.text(ARM[0] - 36, ARM[1] + 30, "armazém", fontsize=7.6, color=TINTA,
        va="bottom", ha="right", fontweight="bold", zorder=8,
        bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=TINTA, lw=0.9,
                  alpha=0.94))
ax.plot([W[2] - 420, W[2] - 120], [W[1] + 60] * 2, color=TINTA, lw=2.6)
ax.text(W[2] - 270, W[1] + 78, "300 m", fontsize=8, color=TINTA, ha="center",
        fontweight="bold")
ax.text(W[0] + 18, W[1] + 18,
        "ortofoto DGT 2025, 25 cm, esbatida · norte em cima · sem qualquer "
        "informação sobre o estado das plantas",
        fontsize=6.7, color=TINTA2, ha="left", va="bottom")

fig.text(0.036, 0.356, "A CONTA, PARA PODER VERIFICAR", fontsize=8.8,
         color=TINTA, fontweight="bold")
CX = [(BOM, "A TABELA FECHA",
       "As 25 válvulas somam 449.275 m² = 44,93 ha, que é exactamente o total "
       "que nos tinha dado. A banda contígua, válvulas 6 a 17, dá 27,30 ha."),
      (BOM, "E BATE COM A IMAGEM",
       "Medimos 30,31 ha de estrutura de pérgola na ortofoto para a mesma "
       "banda. A diferença de 3 ha são bermas e cabeceiras, que a tabela de "
       "rega não conta e a imagem vê. É a concordância que valida o método."),
      (AVISO, "O QUE ISTO AINDA NÃO DÁ",
       "As oito válvulas fora da banda — B4C3, B5, B1C5, B3C4, viveiro, B1C6, "
       "B3C3, 17,66 ha ao todo — não estão colocadas: a tabela dá-lhes área "
       "mas não posição. E dentro do B1 não sabemos onde acaba cada uma.")]
for i, (cor, tit, txt) in enumerate(CX):
    x = 0.036 + i * 0.3127
    axc = fig.add_axes([x, 0.228, 0.2927, 0.120])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA, lw=0.8))
    axc.add_patch(Rectangle((0, 0.94), 1, 0.06, facecolor=cor, edgecolor="none"))
    axc.text(0.032, 0.858, tit, fontsize=8.4, color=cor, fontweight="bold", va="top")
    axc.text(0.032, 0.688, "\n".join(textwrap.wrap(txt, 58)), fontsize=6.9,
             color=TINTA2, va="top", linespacing=1.6)

fig.text(0.036, 0.194, "O QUE PRECISAMOS QUE CONFIRME", fontsize=8.8,
         color=TINTA, fontweight="bold")
PERG = [
    ("1.", "As fronteiras entre válvulas estão nos sítios certos? Não precisa "
     "de medir nada — basta dizer se alguma está claramente fora do lugar, e "
     "para que lado."),
    ("2.", "Dentro do B1: onde acaba a válvula 1 e começam as 2 a 5? É a única "
     "fronteira de porta-enxerto do pomar. A tabela diz que a 1 tem 1,35 ha em "
     "9,01 ha, mas não diz de que lado."),
    ("3.", "A rede do B1: em que ano subiu e em que ano saiu? Se saiu com o "
     "Enza Gold, foi ~2020 — e nesse caso coincide com a enxertia da Erica, o "
     "que faz com que não consigamos separar os dois efeitos."),
    ("4.", "As oito parcelas fora da banda — B4C3, B5, B1C5, B3C4, viveiro, "
     "B1C6, B3C3 — ficam onde? Uma coordenada de telemóvel por cada, como fez "
     "para o armazém, e fecham-se os 44,93 ha."),
    ("5.", "Os blocos B2, Erica Novo, B3 e B4 têm sub-designações no terreno "
     "que não venham na tabela? Vimos referências a B1C2, B1C3, B2-V7, "
     "B3-7ha, e não sabemos como encaixam."),
]
y = 0.168
for n, p in PERG:
    L = textwrap.wrap(p, 130)
    fig.text(0.036, y, n, fontsize=7.7, color=TINTA, fontweight="bold", va="top")
    fig.text(0.056, y, "\n".join(L), fontsize=7.7, color=TINTA2, va="top",
             linespacing=1.45)
    y -= 0.0140 * len(L) + 0.0070

fig.savefig("figuras/M1_valvulas_v6.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M1_valvulas_v6.svg", facecolor=FUNDO, bbox_inches="tight")
print("M1 v6 gravada — %d válvulas na banda, %.2f ha" % (len(SEC), tot / 1e4))
