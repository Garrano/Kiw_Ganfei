# -*- coding: utf-8 -*-
"""M2 — Areas em declinio: incidencia e ano de manifestacao. USO INTERNO.

NAO enviar a gestora antes de a M1 voltar confirmada. A M1 pergunta a geometria;
se quem responde vir este mapa primeiro, a resposta fica contaminada e a
confirmacao deixa de valer.

Metodo. Nove cenas de plena estacao (Jul/Ago), 2017 a 2026. Para cada data,
defice = NDVI abaixo da referencia sa da mesma data menos 0,05, dentro do
poligono do pomar. Para cada pixel:
  ano_inicio  primeiro ano de uma sequencia de >=2 anos consecutivos em defice
              (um ano isolado e ruido, nao manifestacao)
  incidencia  fraccao dos nove anos em defice
As fronteiras de sector da M1 aparecem a tracejado ténue, so para cruzamento.
"""
import csv
import json
import os
import textwrap
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.colors import ListedColormap, BoundaryNorm

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
AZUL, ROXO = "#2a78d6", "#7a4fbf"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (530000, 4654750, 531700, 4655500)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
pomar = mk["pomar"]

DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
ANOS = [int(d[:4]) for d in DATAS]

defs = []
for d in DATAS:
    with rasterio.open("sentinel/%s.tif" % d) as ds:
        nd = ds.read(1)
    defs.append((nd < float(np.nanmean(nd[sau])) - 0.05) & pomar)
D = np.stack(defs)

incid = D.sum(0) / len(DATAS)
inicio = np.full(D.shape[1:], 0, int)
for i in range(len(DATAS) - 1):
    novo = (inicio == 0) & D[i] & D[i + 1]
    inicio[novo] = ANOS[i]

# Um pixel so DECLINOU se antes esteve sao: pelo menos dois anos consecutivos
# fora de defice antes do primeiro par em defice. Pixels em defice desde 2017
# com incidencia alta nunca foram copado sao — sao falhas, caminhos, outra
# cultura. Conta-los como declinio inflaciona a area e falsifica a cronologia.
sao_antes = np.zeros(D.shape[1:], bool)
for i in range(len(DATAS) - 1):
    ainda = inicio == ANOS[i]
    if i == 0:
        continue                      # comeca em defice logo em 2017: nunca sao
    # exigir: sao na primeira cena da serie, e sao em pelo menos metade dos
    # anos anteriores ao arranque. Com um so ano anterior, esse ano basta.
    sao_antes |= ainda & ~D[0] & ((~D[:i]).mean(0) >= 0.5)
nunca_sao = (inicio > 0) & ~sao_antes
inicio_declinio = np.where(sao_antes, inicio, 0)

# ranking por nucleo conexo, com o ano de inicio dominante
persist = ndimage.binary_opening((incid >= 2 / 9) & sao_antes, np.ones((2, 2)))
lab, n = ndimage.label(persist, np.ones((3, 3)))
NOMES = {}
for k, nome in (("manchaW", "Mancha W"), ("zona0", "Zona 0")):
    for i in set(lab[mk[k] & (lab > 0)].ravel()):
        NOMES[int(i)] = nome

linhas = []
for i in range(1, n + 1):
    m = lab == i
    if m.sum() < 4:
        continue
    ini = inicio_declinio[m & (inicio_declinio > 0)]
    ys, xs = np.where(m)
    linhas.append(dict(
        nome=NOMES.get(i, "sem nome"),
        ha=m.sum() / 100.0,
        ano=int(np.median(ini)) if ini.size else 0,
        inc=float(incid[m].mean()),
        E=AOI[0] + xs.mean() * 10, N=AOI[3] - ys.mean() * 10,
        ult=float(D[-1][m].mean())))
linhas.sort(key=lambda r: (-r["ha"] * r["inc"]))
for i, r in enumerate(linhas):
    if r["nome"] == "sem nome":
        r["nome"] = "Núcleo %d" % (i + 1)

with open("m2_nucleos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["nome", "ha", "ano", "inc", "E", "N", "ult"])
    w.writeheader()
    for r in linhas:
        w.writerow({k: (round(v, 4) if isinstance(v, float) else v)
                    for k, v in r.items()})

prov = json.load(open("sentinel/proveniencia.json"))
cena = [c for c in prov["cenas"] if c["data"] == "2026-07-27"][0]["cena"]
a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                 "sentinel-2-l2a/items/" + cena, timeout=90).json()["assets"]


def rd(k):
    with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
        return ds.read(1, window=from_bounds(*W, transform=ds.transform)
                       ).astype("float32")


rgb = np.clip(np.dstack([rd("red"), rd("green"), rd("blue")]) / 2900.0, 0, 1) ** 0.82

fig = plt.figure(figsize=(17.6, 12.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.040, 0.978, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.040, 0.952, "M2 · Onde e desde quando — USO INTERNO",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.960, 0.957, "M2 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.040, 0.922,
         "Não enviar à gestora antes de a M1 voltar confirmada. A M1 pergunta a "
         "geometria; quem a responder depois de ver este mapa já não é "
         "testemunha independente.",
         fontsize=9.2, color=CRIT, fontweight="bold")

ax = fig.add_axes([0.040, 0.398, 0.660, 0.508])
ax.imshow(rgb, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)

# rampa sequencial de uma so cor: quanto mais escuro, mais antigo
ESCADA = [2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
CORES = ["#4a1010", "#7d1a1a", "#a82626", "#c8442f", "#e06a3c",
         "#ee9159", "#f7b785", "#fbd9b8"]
cmap = ListedColormap(CORES)
norm = BoundaryNorm(ESCADA + [2026], len(CORES))
capa = np.where(inicio_declinio > 0, inicio_declinio, np.nan)
ax.imshow(capa, cmap=cmap, norm=norm, extent=[AOI[0], AOI[2], AOI[1], AOI[3]],
          interpolation="nearest", alpha=0.92, zorder=4)

ax.imshow(np.where(nunca_sao, 1, np.nan),
          cmap=ListedColormap(["#5b5b5b"]),
          extent=[AOI[0], AOI[2], AOI[1], AOI[3]], interpolation="nearest",
          alpha=0.80, zorder=3)

pol = np.array(masks["pomar"])
ax.add_patch(Polygon(np.column_stack([AOI[0] + pol[:, 0] * 10.0,
                                      AOI[3] - pol[:, 1] * 10.0]),
                     closed=True, facecolor="none", edgecolor="white", lw=2.6,
                     zorder=5))

X_MW, E_MW, ESC = 1900.0, 530492.0, (530999.0 - 530492.0) / (2370.0 - 1900.0)
VX = [1990, 2130, 2270, 2350, 2480, 2500, 2560, 2700]
for i in range(len(VX) - 1):
    E = E_MW + ((VX[i] + VX[i + 1]) / 2 - X_MW) * ESC
    if W[0] < E < W[2]:
        ax.plot([E, E], [W[1], W[3]], color="white", lw=0.9, alpha=0.45,
                ls=(0, (4, 4)), zorder=6)
ax.text(W[0] + 20, W[3] - 24, "fronteiras de sector da M1, a tracejado ténue",
        fontsize=6.6, color="white", va="top", zorder=8)

for r in linhas[:6]:
    ax.plot([r["E"]], [r["N"]], "o", ms=15, mfc="none", mec="white", mew=2.4,
            zorder=9)
    ax.text(r["E"], r["N"], str(linhas.index(r) + 1), fontsize=9,
            color="white", fontweight="bold", ha="center", va="center",
            zorder=10)

# escala de cor
axl = fig.add_axes([0.040, 0.338, 0.660, 0.030])
axl.set_xlim(0, len(CORES)); axl.set_ylim(0, 1); axl.set_axis_off()
for i, (an, c) in enumerate(zip(ESCADA, CORES)):
    axl.add_patch(Rectangle((i, 0.42), 1, 0.58, facecolor=c, edgecolor="none"))
    axl.text(i + 0.5, 0.26, str(an), fontsize=7.4, color=TINTA2, ha="center")
axl.add_patch(Rectangle((len(CORES) + 0.35, 0.42), 0.9, 0.58,
                        facecolor="#5b5b5b", edgecolor="none"))
axl.text(len(CORES) + 1.40, 0.72,
         "nunca esteve são desde 2017 —\nnão é declínio, é falha de copado",
         fontsize=6.6, color=TINTA2, va="center", linespacing=1.4)
axl.set_xlim(0, len(CORES) + 5.6)
axl.text(0, 1.20, "ANO DA PRIMEIRA MANIFESTAÇÃO — dois anos consecutivos em "
         "défice; um ano isolado não conta", fontsize=7.6, color=TINTA,
         fontweight="bold", va="bottom")

# ---------------- ranking --------------------------------------------------
axr = fig.add_axes([0.722, 0.338, 0.238, 0.568])
axr.set_xlim(0, 1); axr.set_ylim(0, 1); axr.set_axis_off()
axr.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA, lw=0.8))
axr.text(0.05, 0.972, "ORDENADOS POR CARGA", fontsize=8.4, color=TINTA,
         fontweight="bold", va="top")
axr.text(0.05, 0.944, "área × incidência", fontsize=6.8, color=TINTA2, va="top")
maxc = max(r["ha"] * r["inc"] for r in linhas)
for i, r in enumerate(linhas[:8]):
    y = 0.888 - i * 0.108
    axr.text(0.05, y, "%d" % (i + 1), fontsize=9, color="white",
             fontweight="bold", ha="center", va="center",
             bbox=dict(boxstyle="circle,pad=0.26", fc=TINTA, ec="none"))
    axr.text(0.14, y + 0.020, r["nome"], fontsize=8.4, color=TINTA,
             fontweight="bold", va="center")
    axr.text(0.14, y - 0.012, "%.2f ha · desde %s · %.0f%% dos anos"
             % (r["ha"], r["ano"] or "—", 100 * r["inc"]), fontsize=6.5,
             color=TINTA2, va="center")
    axr.add_patch(Rectangle((0.14, y - 0.050), 0.80 * r["ha"] * r["inc"] / maxc,
                            0.020, facecolor=CRIT, edgecolor="none"))
axr.text(0.05, 0.030, "Coordenadas de cada núcleo em m2_nucleos.csv.",
         fontsize=6.4, color=TINTA3, va="bottom")

# ---------------- leitura --------------------------------------------------
fig.text(0.040, 0.300, "O QUE ESTE MAPA MOSTRA", fontsize=8.8, color=TINTA,
         fontweight="bold")
tot = sum(r["ha"] for r in linhas)
antigo = [r for r in linhas if r["ano"] and r["ano"] <= 2018]
recente = [r for r in linhas if r["ano"] and r["ano"] >= 2024]
fig.text(0.040, 0.276,
         "%d núcleos persistentes, %.1f ha no total, %.0f%% do copado. Os mais "
         "antigos manifestam-se em %d; %d núcleos só aparecem a partir de 2024, "
         "somando %.2f ha."
         % (len(linhas), tot, 100 * tot / (pomar.sum() / 100),
            min(r["ano"] for r in linhas if r["ano"]), len(recente),
            sum(r["ha"] for r in recente)),
         fontsize=8.0, color=TINTA2)
fig.text(0.040, 0.254,
         "A cor é sequencial de propósito: escuro = antigo. Não há aqui nenhuma "
         "afirmação sobre causa — só sobre quando cada sítio passou a estar "
         "abaixo da referência e por quantos anos lá ficou.",
         fontsize=8.0, color=TINTA2)

fig.text(0.040, 0.222, "COMO USAR ISTO COM A M1", fontsize=8.8, color=TINTA,
         fontweight="bold")
PASSOS = [
    "1.  Enviar SÓ a M1. Pedir que corrija as válvulas por cima da imagem "
    "impressa, e que responda às cinco perguntas.",
    "2.  Quando voltar, redesenhar as fronteiras de sector com a correcção "
    "dela e voltar a correr este script — os núcleos passam a ter válvula.",
    "3.  Só então perguntar o histórico de cada sector: replantações, falhas "
    "de rega, avarias, mudanças de prática. Aí já se pode mostrar a M2.",
    "4.  A ordem importa: se a M2 for primeiro, deixamos de saber se a "
    "geometria que ela confirmou é a real ou a que lhe sugerimos.",
]
for i, p in enumerate(PASSOS):
    fig.text(0.040, 0.196 - i * 0.0225, p, fontsize=7.9,
             color=CRIT if i == 3 else TINTA2,
             fontweight="bold" if i == 3 else "normal")

fig.text(0.040, 0.076, "RESSALVAS", fontsize=8.8, color=TINTA,
         fontweight="bold")
fig.text(0.040, 0.052,
         "A referência sã são três manchas dentro do próprio pomar (4,54 ha): "
         "se ela também descer, o défice é subestimado — é a limitação "
         "estrutural desta série e está registada na auditoria.",
         fontsize=7.9, color=TINTA2)
fig.text(0.040, 0.030,
         "2019 e 2025-06 ficaram de fora por fenologia. A 10 m, um núcleo de "
         "4 píxeis é 0,04 ha e a fronteira tem ±1 píxel: as áreas têm sentido, "
         "as formas exactas não.", fontsize=7.9, color=TINTA2)
fig.text(0.040, 0.008,
         "Nenhum destes núcleos foi visitado no terreno. São défice de NDVI, "
         "não diagnóstico — podem ser falha de rega, replantação recente, "
         "outra cultura, ou doença.", fontsize=7.9, color=CRIT,
         fontweight="bold")

fig.savefig("figuras/M2_declinio.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M2_declinio.svg", facecolor=FUNDO, bbox_inches="tight")
print("M2 gravada — %d nucleos, %.2f ha" % (len(linhas), tot))
for r in linhas[:8]:
    print("  %-12s %5.2f ha  desde %s  incid %.0f%%  E%.0f N%.0f"
          % (r["nome"], r["ha"], r["ano"] or "--", 100 * r["inc"], r["E"], r["N"]))
