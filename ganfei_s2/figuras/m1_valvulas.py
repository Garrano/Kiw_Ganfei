# -*- coding: utf-8 -*-
"""M1 — Mapa de valvulas e sectores, PARA CONFIRMACAO PELA GESTORA.

REGRA DESTE FICHEIRO: nao contem NENHUMA informacao sobre areas em declinio.
Nem cores, nem marcas, nem texto. A confirmacao da geometria nao vale nada se
quem confirma souber onde nos encontramos alguma coisa. O mapa do declinio e o
M2, que fica interno.

Como as valvulas foram colocadas
--------------------------------
O "Esquema de rega retificado" e um desenho a mao SEM coordenadas e NAO e
proporcional: um ajuste proporcional directo poe as valvulas 1-5 em E528634-
529088, que fica do outro lado do rio Minho. (Foi exactamente esse o erro que
gerou a AOI "lobulo oeste B1" e que foi retirado em 28-08-2026.)

O que se usa em vez disso sao duas ancoras dadas pela propria gestora:
  A1  Mancha W fica a cavalo do limite B1/B2  (§10 v1.3: "Kiwi 1000" no flanco
      oeste da Mancha W, em B1-este/B2-oeste)
  A2  Zona 0 = valvulas 8, 9, 10               (§10 v1.2)
Com as duas, a escala sai 1,08 m por unidade do esboco, e so as valvulas 6 a 13
caem dentro do poligono medido. As 1-5 e as 14-17 NAO sao colocaveis — e estao
assinaladas como tal, em vez de serem desenhadas por adivinhacao.

Incerteza declarada: +-40 m nas fronteiras de sector.
"""
import json
import os
import textwrap
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
AZUL, VERDE, ROXO = "#2a78d6", "#1baf7a", "#7a4fbf"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (530000, 4654750, 531700, 4655500)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

masks = json.load(open("sentinel/masks.json"))
prov = json.load(open("sentinel/proveniencia.json"))
cena = [c for c in prov["cenas"] if c["data"] == "2026-07-27"][0]["cena"]
a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                 "sentinel-2-l2a/items/" + cena, timeout=90).json()["assets"]


def rd(k):
    with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
        return ds.read(1, window=from_bounds(*W, transform=ds.transform)
                       ).astype("float32")


rgb = np.clip(np.dstack([rd("red"), rd("green"), rd("blue")]) / 2900.0, 0, 1) ** 0.82

# --- ancoras e escala ------------------------------------------------------
X_MW, X_Z0 = 1900.0, 2370.0
E_MW, E_Z0 = 530492.0, 530999.0
ESC = (E_Z0 - E_MW) / (X_Z0 - X_MW)


def Ev(x):
    return E_MW + (x - X_MW) * ESC


# (numero, x no esboco, lado)  — so as que caem no poligono
VALVULAS = [(6, 1990, "N"), (7, 2130, "N"), (8, 2270, "N"), (9, 2350, "S"),
            (10, 2480, "N"), (11, 2500, "S"), (12, 2700, "S"), (13, 2560, "N")]
LIM_B1B2 = Ev(X_MW)

fig = plt.figure(figsize=(17.6, 11.6), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.040, 0.977, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.040, 0.950, "M1 · Válvulas e sectores — para confirmação",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.960, 0.955, "M1 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.040, 0.918,
         "Esta é a nossa leitura do esquema de rega sobre a imagem de satélite. "
         "Pedimos que confirme ou corrija. As posições marcadas a tracejado são "
         "as que NÃO conseguimos estabelecer. Não desenhámos nada para elas: "
         "marcar uma zona no mapa já seria sugerir onde ficam.",
         fontsize=9.2, color=TINTA2)

ax = fig.add_axes([0.040, 0.335, 0.920, 0.560])
ax.imshow(rgb, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)

pol = np.array(masks["pomar"])
Px = AOI[0] + pol[:, 0] * 10.0
Py = AOI[3] - pol[:, 1] * 10.0
ax.add_patch(Polygon(np.column_stack([Px, Py]), closed=True, facecolor="none",
                     edgecolor="white", lw=3.4, zorder=3))
ax.add_patch(Polygon(np.column_stack([Px, Py]), closed=True, facecolor="none",
                     edgecolor=TINTA, lw=1.6, zorder=4))

# fronteiras de sector
fronteiras = [LIM_B1B2] + [Ev((VALVULAS[i][1] + VALVULAS[i + 1][1]) / 2)
                           for i in range(len(VALVULAS) - 1)]
for E in sorted(set(round(f) for f in fronteiras)):
    if W[0] < E < W[2]:
        ax.plot([E, E], [W[1], W[3]], color="white", lw=2.2, alpha=0.75, zorder=5)
        ax.plot([E, E], [W[1], W[3]], color=TINTA2, lw=0.9, ls=(0, (5, 3)),
                zorder=6)

# conduta principal, a meia altura do bloco
Ycond = 4655080
ax.plot([W[0] + 20, W[2] - 20], [Ycond, Ycond], color="#0d5fc4", lw=3.0,
        alpha=0.9, zorder=7, solid_capstyle="round")
for E in np.arange(W[0] + 140, W[2] - 60, 260):
    ax.add_patch(FancyArrowPatch((E, Ycond), (E + 70, Ycond), arrowstyle="-|>",
                                 mutation_scale=15, color="#0d5fc4", lw=0,
                                 zorder=8))

for num, x, lado in VALVULAS:
    E = Ev(x)
    if not (W[0] < E < W[2]):
        continue
    ymarca = Ycond + (150 if lado == "N" else -150)
    ax.plot([E, E], [Ycond, ymarca], color="#0d5fc4", lw=1.4, zorder=8)
    ax.plot([E], [Ycond], "o", color="#0d5fc4", ms=7, zorder=9,
            markeredgecolor="white", markeredgewidth=1.4)
    ax.text(E, ymarca + (34 if lado == "N" else -34), str(num), fontsize=13,
            color="white", fontweight="bold", ha="center", va="center",
            zorder=10,
            bbox=dict(boxstyle="circle,pad=0.30", fc="#0d5fc4", ec="white",
                      lw=1.6))

# nomes da nossa analise — geograficos, sem qualquer estado sanitario
for k, cor, nome in (("manchaW", ROXO, "«Mancha W»"),
                     ("zona0", AZUL, "«Zona 0»  = válvulas 8 · 9 · 10")):
    p = np.array(masks[k])
    X = AOI[0] + p[:, 0] * 10.0
    Y = AOI[3] - p[:, 1] * 10.0
    ax.add_patch(Polygon(np.column_stack([X, Y]), closed=True, facecolor="none",
                         edgecolor="white", lw=3.0, zorder=10))
    ax.add_patch(Polygon(np.column_stack([X, Y]), closed=True, facecolor="none",
                         edgecolor=cor, lw=2.0, zorder=11))
    ax.text(X.mean(), Y.min() - 30, nome, fontsize=8.4, color=cor,
            fontweight="bold", ha="center", va="top", zorder=12,
            bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=cor, lw=1.0,
                      alpha=0.94))

# NAO se desenha nenhuma regiao para as valvulas 1-5 e 14-17: marcar uma faixa
# na margem do mapa implicaria uma localizacao, que e precisamente o que nao
# temos. Fica so na legenda.

ax.text(W[0] + 20, Ycond + 26, "CONDUTA PRINCIPAL — origem única, a montante "
        "a oeste", fontsize=8.0, color="#0d5fc4", fontweight="bold", va="bottom",
        zorder=12,
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec="#0d5fc4", lw=1.0,
                  alpha=0.92))
ax.text(W[2] - 20, W[1] + 20, "imagem Sentinel-2, 27-07-2026 · 10 m/píxel · "
        "norte em cima", fontsize=6.8, color="white", ha="right", va="bottom",
        zorder=12)

# ---------------- legenda e perguntas --------------------------------------
fig.text(0.040, 0.300, "O QUE ESTE MAPA AFIRMA, E COM QUE CONFIANÇA",
         fontsize=8.8, color=TINTA, fontweight="bold")

CAIXAS = [
    (BOM, "MEDIDO — alta confiança",
     "O contorno do pomar (linha preta) vem da imagem de satélite, não do "
     "esquema. 29,0 ha de copado. As duas manchas nomeadas são polígonos "
     "geográficos fixos, iguais em todas as datas."),
    (AVISO, "DEDUZIDO — ±40 m",
     "As válvulas 6 a 13 e as fronteiras de sector saem de duas indicações "
     "suas: que a Mancha W fica no limite B1/B2, e que a Zona 0 são as "
     "válvulas 8, 9 e 10. Daí sai a escala. É a parte a confirmar."),
    (CRIT, "NÃO ESTABELECIDO",
     "Válvulas 1–5 e 14–17. O esquema de rega não é proporcional: ajustá-lo "
     "directamente punha as válvulas 1–5 do outro lado do rio. Preferimos "
     "deixar em branco a inventar."),
]
for i, (cor, tit, txt) in enumerate(CAIXAS):
    x = 0.040 + i * 0.3135
    axc = fig.add_axes([x, 0.176, 0.2935, 0.112])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axc.add_patch(Rectangle((0, 0.93), 1, 0.07, facecolor=cor, edgecolor="none"))
    axc.text(0.030, 0.845, tit, fontsize=8.6, color=cor, fontweight="bold",
             va="top")
    axc.text(0.030, 0.680, "\n".join(textwrap.wrap(txt, 56)), fontsize=7.0,
             color=TINTA2, va="top", linespacing=1.62)

fig.text(0.040, 0.146, "O QUE PRECISAMOS QUE CONFIRME OU CORRIJA",
         fontsize=8.8, color=TINTA, fontweight="bold")
PERG = [
    "1.  As válvulas 6 a 13 estão nos sítios certos? Se alguma estiver "
    "trocada de lado da conduta (norte/sul), diga qual.",
    "2.  Onde ficam as válvulas 1 a 5 (B1) e as 14 a 17? Basta um traço por "
    "cima desta imagem impressa.",
    "3.  Confirma que TODO o corpo principal é Erica de pé franco, e que só as "
    "válvulas 2–5 têm raiz de Summer Kiwi? A válvula 1 é pé franco?",
    "4.  A conduta principal corre mesmo a meio do bloco, como aqui? E a água "
    "entra pelo lado oeste?",
    "5.  O viveiro (válvulas 22–23) e a B3C3 (válvula 27) ficam fora desta "
    "imagem — a que distância, e para que lado?",
]
for i, p in enumerate(PERG):
    fig.text(0.040, 0.118 - i * 0.0215, p, fontsize=7.9, color=TINTA2)

fig.text(0.040, 0.008,
         "PORTA-ENXERTOS, conforme nos indicou:  corpo principal = Erica de PÉ "
         "FRANCO (sem porta-enxerto)  ·  válvulas 2–5 = raiz de SUMMER KIWI, "
         "sobre-enxertada com Enza Gold em 2016 e com Erica em 2020.",
         fontsize=7.9, color=TINTA, fontweight="bold")

fig.savefig("figuras/M1_valvulas.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M1_valvulas.svg", facecolor=FUNDO, bbox_inches="tight")
print("M1 gravada — SEM qualquer informacao de declinio")
