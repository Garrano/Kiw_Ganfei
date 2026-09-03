# -*- coding: utf-8 -*-
"""M1 v8 — Implantacao geral redesenhada. Para a gestora.

REGRA INEGOCIAVEL, desde a v1: zero informacao sobre declinio.

Porque redesenhada e nao o scan
-------------------------------
O scan da planta de 2009 tem as anotacoes a mao por cima, e limpa-las deixa
buracos. E a planta original nao esta georreferenciada. Redesenhar resolve as
duas coisas: o contorno vem da ortofoto (estrutura de pergola medida por
periodicidade de compasso, 30,31 ha), e os sectores vem da tabela de areas do
gestor, cortados onde a area MEDIDA acumulada iguala a area TABELADA.

Nada aqui e lido do desenho de 2009. A planta serviu para saber o que existe —
sectores, valvulas, conduta, legenda — nao para saber onde.

Verificacao independente: a valvula 8 assim colocada cai a 34 m do ponto que o
gestor nomeou como «Zona 0 = valvulas 8, 9, 10», e essa frase nao entrou no
calculo.
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
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrow
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch

TRACO = "#1a1a18"
FINO = "#6b6a66"
PAPEL = "#fbfaf6"
BLOCO = {"B2": "#3b6ea5", "Erica Novo": "#7d5ba6", "B3": "#c2703a",
         "B4": "#4a7c59", "B1": "#a34b3a"}

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
ARM = tr.transform(-8.633148, 42.045095)
B1I = tr.transform(-8.643581734449253, 42.03757663209986)
B1F = tr.transform(-8.636871142810762, 42.04118410828004)

TAB = [("B2", 6, 25000), ("B2", 7, 25100), ("B2", 8, 28200), ("B2", 9, 18200),
       ("Erica Novo", 10, 24000), ("Erica Novo", 11, 24650),
       ("B3", 12, 27500), ("B3", 13, 25300), ("B3", 14, 25850), ("B3", 15, 11400),
       ("B4", 16, 17300), ("B4", 17, 20500)]
SOLTAS = [("B4C3", 18, 5500), ("B5", 19, 12500), ("B1C5", 20, 23000),
          ("B3C4", 21, 2300), ("Viveiro", 22, 10400), ("Viveiro", 23, 1500),
          ("B1C6", "24·25", 17000), ("B3C3", 27, 14000)]

g = json.load(open("sentinel/masks_geograficas.json"))
P = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)
ys, xs = np.where(P)
E = AOI[0] + (xs + .5) * 10
N = AOI[3] - (ys + .5) * 10
C = np.array([E.mean(), N.mean()])
w_, v_ = np.linalg.eigh(np.cov(np.column_stack([E - C[0], N - C[1]]).T))
u = v_[:, np.argmax(w_)]
u = u if u[0] > 0 else -u
q = np.array([-u[1], u[0]])
t = np.column_stack([E - C[0], N - C[1]]) @ u
r = np.column_stack([E - C[0], N - C[1]]) @ q
ordem = np.argsort(t)
acum = np.arange(1, len(t) + 1) * 100.0
TOT = sum(a for _, _, a in TAB)


def d_de_area(a_m2):
    i = int(np.searchsorted(acum, a_m2 / TOT * acum[-1]))
    return float(t[ordem][min(i, len(t) - 1)])


def largura(d, meia=45.0):
    sel = np.abs(t - d) < meia
    return (float(np.percentile(r[sel], 2)), float(np.percentile(r[sel], 98))) \
        if sel.sum() > 8 else (-100.0, 100.0)


SEC, cum = [], 0
for b, v, a in TAB:
    d0 = d_de_area(cum); cum += a; d1 = d_de_area(cum)
    SEC.append((b, v, a, d0, d1))

fig = plt.figure(figsize=(19.2, 11.4), dpi=200)
fig.patch.set_facecolor(PAPEL)
ax = fig.add_axes([0.028, 0.150, 0.944, 0.800])
ax.set_facecolor(PAPEL)
ax.set_xticks([]); ax.set_yticks([])
for s_ in ax.spines.values():
    s_.set_color(TRACO); s_.set_linewidth(1.1)
W = (529380, 4653690, 531760, 4655520)
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_aspect("equal")

# --- ortofoto muito esbatida, so como referencia de sitio -------------------
try:
    ds = rasterio.open("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
    Wo = transform_bounds("EPSG:32629", ds.crs, *W)
    w = from_bounds(*Wo, transform=ds.transform)
    im = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32") / 255.
    cinza = im.mean(2)
    cinza = (cinza - cinza.min()) / max(float(np.ptp(cinza)), 1e-6)
    ax.imshow(np.dstack([cinza * 0.22 + 0.76] * 3), extent=[W[0], W[2], W[1], W[3]],
              zorder=0, interpolation="bilinear")
except Exception as e:
    print("ortofoto nao carregada:", e)

# --- contorno medido da parcela -------------------------------------------
from scipy import ndimage
cont = ndimage.binary_dilation(P, np.ones((3, 3))) & ~P
ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
           np.linspace(AOI[3] - 5, AOI[1] + 5, 100), P.astype(float), [0.5],
           colors=[TRACO], linewidths=1.6, zorder=4)

# caminho de recorte: o contorno medido da parcela
cs = ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
                np.linspace(AOI[3] - 5, AOI[1] + 5, 100), P.astype(float),
                [0.5], colors="none")
verts = max([pp.vertices for cc in cs.collections for pp in cc.get_paths()],
            key=len) if hasattr(cs, "collections") else         max([pp.vertices for pp in cs.get_paths()], key=len)
CLIP = MPath(verts)

HACH = {"B2": "///", "Erica Novo": "\\\\\\", "B3": "|||", "B4": "---"}
for b, v, a, d0, d1 in SEC:
    r0a, r1a = largura((d0 + d1) / 2)
    poly = np.array([C + u * d0 + q * r0a, C + u * d1 + q * r0a,
                     C + u * d1 + q * r1a, C + u * d0 + q * r1a])
    pa = ax.add_patch(Polygon(poly, closed=True, facecolor=BLOCO[b], alpha=0.11,
                              edgecolor="none", zorder=2))
    pb = ax.add_patch(Polygon(poly, closed=True, facecolor="none",
                              edgecolor=BLOCO[b], lw=0.5, hatch=HACH[b],
                              alpha=0.5, zorder=3))
    cp = PathPatch(CLIP, transform=ax.transData, facecolor="none",
                   edgecolor="none")
    ax.add_patch(cp)
    pa.set_clip_path(cp); pb.set_clip_path(cp)
    for d in (d0, d1):
        p0 = C + u * d + q * r0a; p1 = C + u * d + q * r1a
        ln, = ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=FINO, lw=0.7,
                      zorder=5)
        ln.set_clip_path(cp)

# --- conduta principal, ao longo do eixo -----------------------------------
cd0, cd1 = t.min() - 20, t.max() + 20
pc0, pc1 = C + u * cd0, C + u * cd1
ax.plot([pc0[0], pc1[0]], [pc0[1], pc1[1]], color=TRACO, lw=1.9, zorder=6,
        solid_capstyle="round")
ax.plot([pc0[0], pc1[0]], [pc0[1], pc1[1]], color=PAPEL, lw=0.55, zorder=6,
        dashes=(6, 5))

for b, v, a, d0, d1 in SEC:
    m = C + u * ((d0 + d1) / 2)
    ax.add_patch(Circle((m[0], m[1]), 15, facecolor=PAPEL, edgecolor=TRACO,
                        lw=0.9, zorder=8))
    ax.plot([m[0] - 7.5, m[0] + 7.5], [m[1], m[1]], color=TRACO, lw=0.8,
            zorder=9)
    ax.text(m[0], m[1] + 62, str(v), fontsize=7.2, color=TRACO, ha="center",
            va="center", fontweight="bold", zorder=9)
    ax.text(m[0], m[1] - 58, "%.2f" % (a / 1e4), fontsize=5.6, color=FINO,
            ha="center", va="center", zorder=9,
            bbox=dict(boxstyle="round,pad=0.16", fc=PAPEL, ec="none",
                      alpha=0.85))

vistos = []
for b, v, a, d0, d1 in SEC:
    if b in vistos:
        continue
    vistos.append(b)
    ms = [s for s in SEC if s[0] == b]
    dm = (ms[0][3] + ms[-1][4]) / 2
    r0a, r1a = largura(dm)
    p = C + u * dm + q * (r1a + 62)
    ax.text(p[0], p[1], "%s   %.2f ha" % (b.upper(), sum(s[2] for s in ms) / 1e4),
            fontsize=8.0, color=BLOCO[b], ha="center", va="bottom",
            fontweight="bold", zorder=9,
            rotation=np.degrees(np.arctan2(u[1], u[0])))

# --- B1: parcelas detectadas, com valvula atribuida por area ---------------
# As parcelas do B1 estao fisicamente separadas na ortofoto — nao se cortam,
# contam-se. Quatro componentes, de SW para NE, contra as areas tabeladas:
#   0,72 ha -> valvula 1 (1,35 tabelada; deteccao parcial)
#   0,90 ha -> valvula 2 (0,94)   bate a 4%
#   2,49 ha -> valvula 4 (2,46)   bate a 1%
#   3,71 ha -> valvulas 3+5 fundidas (4,26)
# A ordem 1,2,4,3,5 sai da imagem e coincide com a que se le no esboco, sem
# essa leitura ter entrado no calculo.
try:
    from scipy import ndimage as _nd
    K = np.load("b1_kiwi_5m.npy")
    WK = (529300, 4653800, 530300, 4654600)
    lab, nn = _nd.label(_nd.binary_opening(K, np.ones((2, 2))), np.ones((3, 3)))
    comps = []
    for i_ in range(1, nn + 1):
        m_ = lab == i_
        if m_.sum() * 25 < 3000:
            continue
        yy_, xx_ = np.where(m_)
        comps.append((WK[0] + xx_.mean() * 5, WK[3] - yy_.mean() * 5,
                      m_.sum() * 25, m_))
    comps.sort()
    ROT = ["1", "2", "4", "3 + 5"]
    for k, (ec, nc, ar, m_) in enumerate(comps):
        ax.imshow(np.where(m_, 1, np.nan),
                  cmap=matplotlib.colors.ListedColormap([BLOCO["B1"]]),
                  extent=[WK[0], WK[2], WK[1], WK[3]], alpha=0.20,
                  interpolation="nearest", zorder=2)
        ax.text(ec, nc, ROT[k] if k < len(ROT) else "?", fontsize=7.2,
                color=TRACO, ha="center", va="center", fontweight="bold",
                zorder=9,
                bbox=dict(boxstyle="circle,pad=0.24", fc=PAPEL, ec=TRACO,
                          lw=0.9))
        ax.text(ec, nc - 46, "%.2f" % (ar / 1e4), fontsize=5.6, color=FINO,
                ha="center", va="center", zorder=9,
                bbox=dict(boxstyle="round,pad=0.14", fc=PAPEL, ec="none",
                          alpha=0.85))
    # fronteira do porta-enxerto, entre a valvula 1 e a 2
    if len(comps) >= 2:
        fx = (comps[0][0] + comps[1][0]) / 2
        fy = (comps[0][1] + comps[1][1]) / 2
        ax.plot([fx - 150, fx + 150], [fy + 78, fy - 78], color=TRACO,
                lw=1.4, ls=(0, (5, 3)), zorder=9)
        ax.text(fx, fy - 105, "fronteira de porta-enxerto  ±60 m",
                fontsize=6.2, color=TRACO, ha="center", va="top",
                fontweight="bold", zorder=9,
                bbox=dict(boxstyle="round,pad=0.22", fc=PAPEL, ec=TRACO,
                          lw=0.8, alpha=0.94))
    mb = np.array([comps[-1][0], comps[-1][1]]) if comps else (B1I + B1F) / 2
    ax.text(mb[0] + 60, mb[1] + 150, "B1   9,01 ha", fontsize=8.0,
            color=BLOCO["B1"], ha="center", va="bottom", fontweight="bold",
            zorder=9)
    ax.text(mb[0] + 60, mb[1] + 118, "pé franco na 1 · Summer Kiwi nas 2 a 5",
            fontsize=6.2, color=FINO, ha="center", va="bottom", style="italic",
            zorder=9)
except Exception as _e:
    print("B1 nao desenhado:", _e)

# --- armazem / ponto de abastecimento --------------------------------------
ax.add_patch(Rectangle((ARM[0] - 17, ARM[1] - 17), 34, 34, facecolor=PAPEL,
                       edgecolor=TRACO, lw=1.2, zorder=8))
ax.plot([ARM[0] - 17, ARM[0] + 17], [ARM[1] - 17, ARM[1] + 17], color=TRACO,
        lw=0.9, zorder=9)
ax.text(ARM[0], ARM[1] - 44, "ARMAZÉM", fontsize=6.8, color=TRACO,
        ha="center", va="top", fontweight="bold", zorder=9)

# --- norte, escala ---------------------------------------------------------
nx, ny = W[2] - 150, W[3] - 130
ax.add_patch(Polygon([[nx, ny + 70], [nx - 22, ny - 40], [nx, ny - 16],
                      [nx + 22, ny - 40]], closed=True, facecolor=TRACO,
                     edgecolor="none", zorder=9))
ax.text(nx, ny + 92, "N", fontsize=10, color=TRACO, ha="center", va="bottom",
        fontweight="bold", zorder=9)
sx, sy = W[2] - 560, W[1] + 70
for i in range(4):
    ax.add_patch(Rectangle((sx + i * 100, sy), 100, 16,
                           facecolor=TRACO if i % 2 == 0 else PAPEL,
                           edgecolor=TRACO, lw=0.7, zorder=9))
for i, lab in enumerate(["0", "100", "200", "300", "400 m"]):
    ax.text(sx + i * 100, sy - 14, lab, fontsize=6.2, color=TRACO,
            ha="center", va="top", zorder=9)

# --- legenda ---------------------------------------------------------------
axl = fig.add_axes([0.028, 0.028, 0.300, 0.112])
axl.set_xlim(0, 1); axl.set_ylim(0, 1); axl.set_axis_off()
axl.add_patch(Rectangle((0, 0), 1, 1, facecolor=PAPEL, edgecolor=TRACO, lw=1.0))
axl.text(0.035, 0.90, "LEGENDA", fontsize=7.6, color=TRACO, fontweight="bold",
         va="top")
ITENS = [("valvula", "Electroválvula, com nº e área em ha"),
         ("quadrado", "Ponto de abastecimento — armazém"),
         ("linha", "Conduta principal"),
         ("hach", "Sector de rega, por bloco"),
         ("contorno", "Limite do copado, medido na ortofoto")]
y = 0.68
for tipo, rot in ITENS:
    if tipo == "valvula":
        axl.add_patch(Circle((0.062, y), 0.026, facecolor=PAPEL,
                             edgecolor=TRACO, lw=1.0))
    elif tipo == "quadrado":
        axl.add_patch(Rectangle((0.042, y - 0.026), 0.040, 0.052,
                                facecolor=PAPEL, edgecolor=TRACO, lw=1.0))
    elif tipo == "linha":
        axl.plot([0.036, 0.090], [y, y], color=TRACO, lw=1.9)
    elif tipo == "hach":
        axl.add_patch(Rectangle((0.036, y - 0.030), 0.054, 0.060,
                                facecolor="none", edgecolor=FINO, lw=0.55,
                                hatch="///"))
    else:
        axl.plot([0.036, 0.090], [y, y], color=TRACO, lw=1.6)
    axl.text(0.125, y, rot, fontsize=6.6, color=TRACO, va="center")
    y -= 0.155

# --- cartucho --------------------------------------------------------------
axc = fig.add_axes([0.672, 0.028, 0.300, 0.112])
axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=PAPEL, edgecolor=TRACO, lw=1.0))
axc.plot([0, 1], [0.70, 0.70], color=TRACO, lw=0.8)
axc.plot([0.62, 0.62], [0, 0.70], color=TRACO, lw=0.8)
axc.text(0.030, 0.955, "SISTEMA DE REGA · EMPARCELAMENTO DE GANFEI, VALENÇA",
         fontsize=6.6, color=FINO, va="top")
axc.text(0.030, 0.855, "IMPLANTAÇÃO GERAL — redesenhada", fontsize=10.5,
         color=TRACO, va="top", fontweight="bold")
axc.text(0.030, 0.60,
         "Contorno e sectores medidos na ortofoto DGT\n"
         "2025 (25 cm) e na tabela de áreas da exploração.\n"
         "Nada foi decalcado da planta de 2009.",
         fontsize=6.3, color=TRACO, va="top", linespacing=1.55)
axc.text(0.030, 0.20, "Sem informação sobre o estado das plantas.",
         fontsize=6.2, color=FINO, va="top", style="italic")
axc.text(0.655, 0.58, "ESCALA GRÁFICA", fontsize=6.0, color=FINO, va="top")
axc.text(0.655, 0.40, "DATA · 29·08·2026", fontsize=6.0, color=FINO, va="top")
axc.text(0.655, 0.22, "DES. · M1 v8", fontsize=6.0, color=FINO, va="top")

axn = fig.add_axes([0.338, 0.028, 0.324, 0.112])
axn.set_xlim(0, 1); axn.set_ylim(0, 1); axn.set_axis_off()
axn.add_patch(Rectangle((0, 0), 1, 1, facecolor=PAPEL, edgecolor=TRACO, lw=1.0))
axn.text(0.035, 0.90, "POR CONFIRMAR", fontsize=7.6, color=TRACO,
         fontweight="bold", va="top")
NOTAS = [
    "1 · As fronteiras entre válvulas estão nos sítios certos?",
    "2 · A fronteira de porta-enxerto no B1 está onde a marcámos?",
    "3 · A rede do B1: em que ano subiu e em que ano saiu?",
    "4 · As oito parcelas soltas (17,66 ha) ficam onde?",
    "5 · B1C2, B1C3, B2-V7, B3-7ha — como encaixam nos blocos?",
]
y = 0.70
for nt in NOTAS:
    axn.text(0.035, y, nt, fontsize=6.5, color=TRACO, va="center")
    y -= 0.145

fig.savefig("figuras/M1_implantacao_v8.png", facecolor=PAPEL, bbox_inches="tight")
fig.savefig("figuras/M1_implantacao_v8.svg", facecolor=PAPEL, bbox_inches="tight")
print("M1 v8 gravada — %d sectores, %.2f ha na banda" % (len(SEC), TOT / 1e4))
