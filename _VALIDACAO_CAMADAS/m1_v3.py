# -*- coding: utf-8 -*-
"""M1 v3 — Valvulas e sectores, PARA CONFIRMACAO PELA GESTORA.

REGRA INEGOCIAVEL: zero informacao sobre declinio. Nem cores, nem marcas, nem
texto. A confirmacao da geometria nao vale nada se quem confirma souber onde
encontramos alguma coisa.

O que muda da v2
----------------
1. O contorno passa a ser a mascara GEOGRAFICA (30,31 ha, derivada da ortofoto
   por periodicidade de compasso). A v2 ainda usava o poligono circular, que
   era NDVI de 2026 acima de 0,78.

2. Deixa de haver atribuicao ponto->valvula, e a figura MOSTRA porque:
      espacamento entre valvulas consecutivas   mediana  49 m
      incerteza do ajuste do esquema            mediana  64 m,  p90 110 m
   A incerteza e 1,3 a 2,2 vezes o espacamento. Os circulos de erro sobrepoem-
   se. Nao e uma cautela — e aritmetica: qualquer ponto do terreno cai dentro
   do erro de duas ou mais valvulas. Desenhar numeros sobre a imagem seria
   afirmar uma resolucao que o desenho nao tem.

O ajuste vem de SAIDA_C0\\c0_13_georref.json: escala 0,8290 m/px a 300 dpi
(o cartucho declara 1/3500 @ A1, que da 0,84-0,87 conforme a moldura), rotacao
33,05 graus, residuo mediano 64,1 m.
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
from matplotlib.patches import Rectangle, Circle, Polygon
from scipy import ndimage

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM, AZUL = "#d03b3b", "#fab219", "#0a7a0a", "#0d5fc4"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (530080, 4654820, 531620, 4655460)
BASE = "../_VALIDACAO_CAMADAS/SAIDA_C0/c0_13_georref.json"

fit = json.load(open(BASE, encoding="utf-8"))
V = np.array(fit["valvulas_utm"])
RES = fit["residuo_mediano_m"]
P90 = fit["residuo_p90_m"]
V = V[(V[:, 0] > W[0]) & (V[:, 0] < W[2]) & (V[:, 1] > W[1]) & (V[:, 1] < W[3])]

g = json.load(open("sentinel/masks_geograficas.json"))
POMAR = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)

ds = rasterio.open("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
Wo = transform_bounds("EPSG:32629", ds.crs, *W)
w = from_bounds(*Wo, transform=ds.transform)
img = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32") / 255.0
cinza = img.mean(2)
img = np.dstack([cinza * 0.55 + 0.42] * 3)          # esbatido, so como base

fig = plt.figure(figsize=(17.8, 12.2), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.038, 0.978, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.038, 0.951, "M1 · Válvulas e sectores — para confirmação  (versão 3)",
         fontsize=20.5, color=TINTA, fontweight="bold")
fig.text(0.962, 0.956, "M1 v3 · 28-08-2026", fontsize=8, color=TINTA3,
         ha="right")
fig.text(0.038, 0.916,
         "Não desenhamos aqui nenhum número de válvula sobre a imagem, e a razão está\n"
         "no gráfico à direita: a incerteza com que conseguimos assentar o seu esquema\n"
         "é MAIOR do que a distância entre válvulas vizinhas.",
         fontsize=9.2, color=TINTA2, va="top", linespacing=1.5)

ax = fig.add_axes([0.038, 0.398, 0.660, 0.505])
ax.imshow(img, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)

cont = ndimage.binary_dilation(POMAR, np.ones((3, 3))) & ~POMAR
ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
           np.linspace(AOI[3] - 5, AOI[1] + 5, 100),
           POMAR.astype(float), [0.5], colors=[TINTA], linewidths=2.0)

for x, y in V:
    ax.add_patch(Circle((x, y), P90, facecolor=AZUL, alpha=0.055,
                        edgecolor="none", zorder=3))
for x, y in V:
    ax.add_patch(Circle((x, y), RES, facecolor=AZUL, alpha=0.13,
                        edgecolor=AZUL, lw=0.6, zorder=4))
    ax.plot([x], [y], "+", color=AZUL, ms=7, mew=1.4, zorder=5)

ax.plot([W[0] + 60, W[0] + 60 + 200], [W[1] + 45] * 2, color=TINTA, lw=2.6)
ax.text(W[0] + 160, W[1] + 58, "200 m", fontsize=8, color=TINTA, ha="center",
        fontweight="bold")
ax.text(W[2] - 20, W[1] + 20,
        "ortofoto DGT 2025, 25 cm, esbatida · norte em cima · contorno = pomar "
        "medido por estrutura de pérgola, 30,31 ha",
        fontsize=6.6, color=TINTA2, ha="right", va="bottom")
ax.text(W[0] + 20, W[3] - 24,
        "cada cruz é uma válvula do seu esquema; o disco à volta é o erro com "
        "que a conseguimos colocar",
        fontsize=7.0, color=AZUL, va="top", fontweight="bold")

# ---------------- porque nao ha numeros ------------------------------------
axg = fig.add_axes([0.722, 0.640, 0.240, 0.252])
axg.set_facecolor(FAIXA)
for s in axg.spines.values():
    s.set_color(RISCA)
axg.set_xlim(0, 130); axg.set_ylim(0, 3.4)
axg.set_yticks([]); axg.tick_params(labelsize=7, colors=TINTA2)
axg.text(128, -0.32, "metros", fontsize=7.0, color=TINTA3, ha="right")
for i, (rot, val, cor) in enumerate([
        ("distância entre válvulas vizinhas\n(mediana)", 49, TINTA2),
        ("erro do ajuste (mediana)", RES, AVISO),
        ("erro do ajuste (p90)", P90, CRIT)]):
    axg.barh(2.6 - i, val, height=0.46, color=cor, alpha=0.85)
    axg.text(val + 3, 2.6 - i, "%.0f m" % val, fontsize=8, color=cor,
             va="center", fontweight="bold")
    axg.text(2, 2.6 - i - 0.34, rot, fontsize=6.4, color=TINTA2, va="top")
fig.text(0.722, 0.906, "PORQUE NÃO HÁ NÚMEROS NO MAPA", fontsize=8.6,
         color=TINTA, fontweight="bold")

axt = fig.add_axes([0.722, 0.470, 0.240, 0.118])
axt.set_xlim(0, 1); axt.set_ylim(0, 1); axt.set_axis_off()
axt.add_patch(Rectangle((0, 0), 1, 1, facecolor="#fdf3e3", edgecolor=AVISO,
                        lw=1.2))
axt.text(0.055, 0.90,
         "\n".join(textwrap.wrap(
             "O erro é 1,3 a 2,2 vezes maior do que o espaçamento. Os discos "
             "sobrepõem-se: qualquer ponto do terreno cai dentro do erro de "
             "duas ou mais válvulas. Pôr números seria afirmar uma precisão "
             "que o desenho não tem — foi esse tipo de erro que, na versão 1 "
             "desta figura, atirou cinco válvulas para o outro lado do rio.",
             44)),
         fontsize=6.9, color=TINTA, va="top", linespacing=1.62)

# ---------------- confianca ------------------------------------------------
fig.text(0.038, 0.360, "O QUE ESTE MAPA AFIRMA, E COM QUE CONFIANÇA",
         fontsize=8.8, color=TINTA, fontweight="bold")
CAIXAS = [
    (BOM, "MEDIDO — ±10 m",
     "O contorno preto. Vem da ortofoto, pela estrutura de pérgola: postes em "
     "malha de 5,0 m, que existe esteja a planta boa ou má. 30,31 ha. Não vem "
     "do esquema nem de índices de vegetação."),
    (AVISO, "COLOCADO POR AJUSTE — ±64 m",
     "As cruzes. O seu esquema foi assente pela forma do terreno desenhado, à "
     "escala que ele próprio declara (1/3500 @ A1) e rodado 33°. O troço "
     "desenhado bate com a parcela medida a 2% de erro."),
    (CRIT, "NÃO DESENHADO",
     "As válvulas 1–5 («B1», anotado 1,77 ha) e as vinhas com raiz de Summer "
     "Kiwi. O esquema põe esse lobo a cerca de 1 km a sudoeste, fora desta "
     "parcela. Não sabemos, e não inventámos."),
]
for i, (cor, tit, txt) in enumerate(CAIXAS):
    x = 0.038 + i * 0.3123
    axc = fig.add_axes([x, 0.232, 0.2923, 0.114])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axc.add_patch(Rectangle((0, 0.93), 1, 0.07, facecolor=cor, edgecolor="none"))
    axc.text(0.032, 0.845, tit, fontsize=8.6, color=cor, fontweight="bold",
             va="top")
    axc.text(0.032, 0.655, "\n".join(textwrap.wrap(txt, 57)), fontsize=7.0,
             color=TINTA2, va="top", linespacing=1.62)

fig.text(0.038, 0.196, "O QUE PRECISAMOS QUE CONFIRME OU CORRIJA",
         fontsize=8.8, color=TINTA, fontweight="bold")
PERG = [
    "1.  Imprima esta folha e marque por cima onde estão as válvulas. É o "
    "único modo de fecharmos isto — nós não conseguimos.",
    "2.  O seu esquema mostra duas filas, uma a norte e outra a sul da "
    "conduta. Confirma que é assim no terreno?",
    "3.  As válvulas 1 a 5 ficam mesmo num bloco separado a sudoeste? Esse "
    "bloco pertence à exploração, e entra ou não neste estudo?",
    "4.  Onde estão exactamente as videiras com raiz de Summer Kiwi? Marque-as "
    "também — não as desenhámos porque não sabemos.",
    "5.  O viveiro e a B3C3 ficam dentro desta imagem ou fora? Se fora, para "
    "que lado e a que distância?",
    "6.  A conduta principal corre onde o esquema a põe, e a água entra pelo "
    "lado oeste?",
]
for i, p in enumerate(PERG):
    fig.text(0.038, 0.168 - i * 0.0224, p, fontsize=7.9, color=TINTA2)

fig.text(0.038, 0.016,
         "NOTA DE MÉTODO: a versão 1 desta figura colocava as válvulas a partir "
         "de duas indicações verbais, e daí saía uma escala 30% maior do que a "
         "que o próprio esquema declara. Esse erro, levado ao extremo oeste do "
         "desenho, gerou uma área de estudo do outro lado do rio Minho — desde "
         "então retirada, com tudo o que dela dependia.",
         fontsize=7.4, color=CRIT, fontweight="bold")

fig.savefig("figuras/M1_valvulas_v3.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M1_valvulas_v3.svg", facecolor=FUNDO, bbox_inches="tight")
print("M1 v3 gravada — %d valvulas na janela, erro %.0f m, espacamento 49 m"
      % (len(V), RES))
