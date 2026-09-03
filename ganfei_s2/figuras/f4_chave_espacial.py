# -*- coding: utf-8 -*-
"""F4 — Chave espacial.

Painel A: ESQUEMA, nao imagem. A 10 m, uma ortofoto em tons de cinzento nao
suporta anotacao — o esquema mostra as relacoes, que e o que interessa aqui.
Painel B: NDVI muito claro como fundo, com chamadas NUMERADAS e a legenda ao
lado. Nenhum rotulo comprido sobre o mapa.
"""
import json, csv, os
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import requests

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA = "#fcfcfb", "#dedcd6"
Z0C, MWC, B1C = "#2a78d6", "#eb6834", "#1baf7a"
CRIT, NEUTRO, ROXO = "#d03b3b", "#6f6d66", "#7a4fbf"
AGUA, CAMPO = "#dfe6ec", "#f2f1ec"

AOI = (529950, 4654600, 531950, 4655600)
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
         CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]


def defice(dt):
    with rasterio.open("sentinel/%s.tif" % dt) as ds:
        nd = ds.read(1)
    return (nd < float(np.nanmean(nd[sau])) - 0.05) & mk["pomar"], nd


d24, _ = defice("2024-07-22")
d26, nd26 = defice("2026-07-27")
frente = ndimage.binary_opening(d26 & ~d24, np.ones((2, 2)))

W = (528200, 4654050, 532200, 4655900)
prov = json.load(open("sentinel/proveniencia.json"))
cena = [c for c in prov["cenas"] if c["data"] == "2026-07-27"][0]["cena"]
a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                 "sentinel-2-l2a/items/" + cena, timeout=90).json()["assets"]


def rd(k):
    with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
        return ds.read(1, window=from_bounds(*W, transform=ds.transform)).astype("float32")


ndw = (rd("nir") - rd("red")) / (rd("nir") + rd("red"))
rio = ndimage.binary_closing(ndw < 0.22, np.ones((3, 3)))

nucleos = list(csv.DictReader(open("difusa_nucleos.csv", encoding="utf-8")))
tracos = {r["elemento"]: r for r in
          csv.DictReader(open("_pacote_cowork/tracos_1995_coordenadas.csv",
                              encoding="utf-8"))}

fig = plt.figure(figsize=(16.8, 14.2), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.045, 0.976, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.045, 0.950, "Chave espacial", fontsize=21, color=TINTA,
         fontweight="bold")
fig.text(0.955, 0.955, "F4 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")

# ============ PAINEL A — esquema ============================================
axA = fig.add_axes([0.045, 0.632, 0.910, 0.278])
axA.set_xlim(0, ndw.shape[1]); axA.set_ylim(ndw.shape[0], 0)
axA.set_xticks([]); axA.set_yticks([])
axA.set_facecolor(CAMPO)
for s in axA.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.7)
axA.imshow(np.where(rio, 1, np.nan), cmap=matplotlib.colors.ListedColormap([AGUA]),
           interpolation="nearest", zorder=1)


def A(Ex, Nx):
    return (Ex - W[0]) / 10.0, (W[3] - Nx) / 10.0


pol = np.array(masks["pomar"])
px = (AOI[0] + pol[:, 0] * 10 - W[0]) / 10.0
py = (W[3] - (AOI[3] - pol[:, 1] * 10)) / 10.0
axA.add_patch(Polygon(np.column_stack([px, py]), closed=True, facecolor="white",
                      edgecolor=TINTA, lw=1.8, zorder=3))
# --- RETRACTACAO 28-08-2026 -------------------------------------------------
# Ate hoje esta figura desenhava um "lobulo oeste B1" a 1,06 km, com serie
# propria em sentinel_b1/. Essa AOI (528400-529400 E) esta em Valenca, do
# OUTRO LADO do rio Minho: o script que a criou ja lhe chamava "candidato a
# B1" e nunca foi confirmada. Toda a serie b1 media vegetacao urbana.
# B1 sao as valvulas 1-5 = o extremo OESTE deste mesmo poligono, e a Mancha W
# fica a cavalo do limite B1/B2 — que e exactamente o que o enquadramento ja
# dizia em §10 v1.3 ("flanco oeste da Mancha W, em B1-este/B2-oeste").
lim_b1 = 530550
axA.add_patch(Rectangle((A(530150, 4655900)[0], 0),
                        (lim_b1 - 530150) / 10.0, ndw.shape[0],
                        facecolor=B1C, alpha=0.13, edgecolor="none", zorder=2))
axA.plot([A(lim_b1, 0)[0]] * 2, [0, ndw.shape[0]], color=B1C, lw=1.4,
         ls=(0, (5, 3)), zorder=4)
axA.text(A(530350, 4655900)[0], 30, "B1\nválvulas 1–5", fontsize=7.6,
         color=B1C, fontweight="bold", ha="center", va="top", linespacing=1.4,
         zorder=5)
axA.text(A(531100, 4655900)[0], 30,
         "B2 · Erica Novo · B3 · B4 · B5 …\nválvulas 6 a 27",
         fontsize=7.6, color=TINTA2, fontweight="bold", ha="center", va="top",
         linespacing=1.4, zorder=5)

axA.add_patch(Rectangle((8, 96), 176, 80, facecolor="white", alpha=0.90,
                        edgecolor=CRIT, lw=1.4, zorder=6))
axA.text(13, 102, "RETRACTAÇÃO · 28-08-2026", fontsize=7.2, color=CRIT,
         fontweight="bold", va="top", zorder=7)
axA.text(13, 114,
         "Esta figura desenhava, até hoje, um «lóbulo oeste B1» a 1,06 km daqui, com\n"
         "série de satélite própria. Essa área fica em Valença, do OUTRO LADO do rio:\n"
         "o script que a criou já lhe chamava «candidato a B1» e nunca foi confirmada.\n"
         "Toda a série media vegetação urbana. Retirada, e com ela o «controlo externo».",
         fontsize=6.1, color=TINTA, va="top", linespacing=1.55, zorder=7)
axA.text(13, 146,
         "B1 são as válvulas 1–5 = o extremo OESTE deste mesmo pomar (a verde). A\n"
         "Mancha W fica a cavalo do limite B1/B2 — o que confirma o enquadramento,\n"
         "que já situava o «Kiwi 1000» no flanco oeste dela, em B1-este/B2-oeste.\n"
         "NÃO existe bloco são comparável fora do pomar: o controlo tem de ser interno.",
         fontsize=6.1, color=CRIT, va="top", linespacing=1.55, zorder=7)

axA.text(px.mean(), py.max() + 10, "CORPO PRINCIPAL\n29,0 ha de copado",
         fontsize=8.0, color=TINTA, fontweight="bold", ha="center", va="top",
         linespacing=1.4, zorder=4)
axA.text(ndw.shape[1] * 0.5, ndw.shape[0] - 3,
         "Entre 2022 e 2025 entraram 11,16 ha de pomar novo na mesma origem de "
         "água. Não os desenho: as parcelas exactas não estão confirmadas.",
         fontsize=7.6, color=TINTA2, style="italic", ha="center", va="bottom",
         zorder=4)

# ============ PAINEL B — mapa + chamadas numeradas ==========================
axB = fig.add_axes([0.045, 0.235, 0.640, 0.362])
axB.imshow(nd26, cmap="Greys_r", vmin=0.20, vmax=1.00,
           interpolation="bilinear", alpha=0.32)
axB.set_xticks([]); axB.set_yticks([])
for s in axB.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.7)
axB.imshow(np.where(frente, 1, np.nan),
           cmap=matplotlib.colors.ListedColormap(["#ff7a1a"]),
           interpolation="nearest", alpha=0.80)
for k, c, lw, ls in (("pomar", TINTA, 1.8, "-"), ("manchaW", MWC, 2.2, "-"),
                     ("zona0", Z0C, 2.2, "-")):
    p = np.array(masks[k])
    axB.plot(np.append(p[:, 0], p[0, 0]), np.append(p[:, 1], p[0, 1]),
             color=c, lw=lw, linestyle=ls)
for k in ("saudavel", "saudavel_2", "saudavel_3"):
    p = np.array(masks[k])
    axB.plot(np.append(p[:, 0], p[0, 0]), np.append(p[:, 1], p[0, 1]),
             color=NEUTRO, lw=1.1, linestyle=(0, (4, 2)))

L1a, L1b = tracos["L1_linear_EW_240m_inicio"], tracos["L1_linear_EW_240m_fim"]
xa = (float(L1a["UTM29N_E"]) - AOI[0]) / 10.0
ya = (AOI[3] - float(L1a["UTM29N_N"])) / 10.0
xb = (float(L1b["UTM29N_E"]) - AOI[0]) / 10.0
yb = (AOI[3] - float(L1b["UTM29N_N"])) / 10.0
axB.plot([xa, xb], [ya, yb], color=ROXO, lw=2.4, linestyle=(0, (7, 3)), zorder=5)

CHAM = [
    (53.6, 54.8, "1", MWC),
    (102.1, 48.1, "2", Z0C),
    (float(nucleos[0]["centro_x"]), float(nucleos[0]["centro_y"]), "3", CRIT),
    (float(nucleos[1]["centro_x"]), float(nucleos[1]["centro_y"]), "4", CRIT),
    (float(nucleos[2]["centro_x"]), float(nucleos[2]["centro_y"]), "5", CRIT),
    (xa + (xb - xa) * 0.16, ya + (yb - ya) * 0.16, "6", ROXO),
]
for x, y, n, cor in CHAM:
    axB.add_patch(Circle((x, y), 4.6, facecolor="white", edgecolor=cor, lw=1.9,
                         zorder=7))
    axB.text(x, y, n, fontsize=7.8, color=cor, ha="center", va="center",
             fontweight="bold", zorder=8)
axB.text(0.012, 0.955, "B · DETALHE DO CORPO PRINCIPAL", transform=axB.transAxes,
         fontsize=8.6, color=TINTA, fontweight="bold", va="top")
axB.text(0.012, 0.900,
         "AOI 2 × 1 km · UTM29N (529950, 4654600 → 531950, 4655600)\nNDVI de 27-07-2026",
         transform=axB.transAxes, fontsize=6.8, color=TINTA2, va="top",
         linespacing=1.4)

# ---- chave lateral ---------------------------------------------------------
axK = fig.add_axes([0.700, 0.235, 0.255, 0.362]); axK.set_axis_off()
axK.set_xlim(0, 1); axK.set_ylim(0, 1)
axK.text(0, 0.985, "CHAVE", fontsize=8.6, color=TINTA, fontweight="bold",
         va="top")
LEG = [
    ("1", MWC, "Centro da Mancha W",
     "fixo desde 2024, ±17 m, enquanto\na área triplicava"),
    ("2", Z0C, "Centro da Zona 0",
     "fixo desde 2017, nove anos"),
    ("3", CRIT, "Satélite · 0,21 ha",
     "a 79 m da Zona 0\n−8,625206 / 42,048096"),
    ("4", CRIT, "Satélite · 0,24 ha",
     "a 82 m da Zona 0\n−8,626744 / 42,047507"),
    ("5", CRIT, "Satélite · 0,21 ha",
     "a 143 m da Mancha W\n−8,633157 / 42,046334"),
    ("6", ROXO, "Traço linear de 1995 · 240 m",
     "alvo do pedido de telas finais\nde drenagem ao arquivo"),
]
y = 0.930
for n, cor, tit, det in LEG:
    axK.add_patch(Circle((0.030, y), 0.020, facecolor="white", edgecolor=cor,
                         lw=1.9, transform=axK.transAxes, clip_on=False))
    axK.text(0.030, y, n, fontsize=7.8, color=cor, ha="center", va="center",
             fontweight="bold", transform=axK.transAxes)
    axK.text(0.085, y + 0.010, tit, fontsize=7.6, color=TINTA,
             fontweight="bold", va="center")
    axK.text(0.085, y - 0.033, det, fontsize=6.6, color=TINTA2, va="center",
             linespacing=1.45)
    y -= 0.116

y -= 0.010
axK.plot([0, 1], [y + 0.030, y + 0.030], color=RISCA, lw=0.8)
for rot, cor, tipo in (("pomar · copado 2026, 29,0 ha", TINTA, "l"),
                       ("Mancha W · 4,27 ha", MWC, "l"),
                       ("Zona 0 · 2,20 ha", Z0C, "l"),
                       ("referência sã · 3 manchas, 4,54 ha", NEUTRO, "t"),
                       ("frente em avanço 2024→2026", "#ff7a1a", "a")):
    if tipo == "l":
        axK.plot([0.010, 0.062], [y, y], color=cor, lw=2.2)
    elif tipo == "t":
        axK.plot([0.010, 0.062], [y, y], color=cor, lw=1.6,
                 linestyle=(0, (4, 2)))
    else:
        axK.add_patch(Rectangle((0.010, y - 0.012), 0.052, 0.024,
                                facecolor="#ff7a1a", alpha=0.80,
                                edgecolor="none"))
    axK.text(0.085, y, rot, fontsize=7.2, color=TINTA, va="center")
    y -= 0.050

# ---- rodape ----------------------------------------------------------------
fig.text(0.045, 0.176, "ONDE AMOSTRAR EM SETEMBRO", fontsize=8.6, color=TINTA,
         fontweight="bold")
fig.text(0.045, 0.148,
         "A área a laranja é a frente que avançou entre 2024 e 2026 — %0.2f ha. "
         "É aí que estão as plantas sintomáticas mas ainda vivas; o centro dos "
         "focos tem sobretudo colonizadores secundários." % (frente.sum() / 100.0),
         fontsize=8.0, color=TINTA2)
fig.text(0.045, 0.118, "S1", fontsize=8.6, color=Z0C, fontweight="bold")
fig.text(0.072, 0.118,
         "Zona 0 — margem em avanço, com par assintomático a ≥20 m. "
         "É o foco mais antigo e NUNCA teve painel etiológico.",
         fontsize=8.0, color=TINTA2)
fig.text(0.045, 0.090, "S2", fontsize=8.6, color=MWC, fontweight="bold")
fig.text(0.072, 0.090,
         "Mancha W — margem em avanço, mais a berma sul junto da planta arrancada. "
         "Cria a primeira série etiológica do caso (2025→2026).",
         fontsize=8.0, color=TINTA2)
fig.text(0.045, 0.062, "S3", fontsize=8.6, color=CRIT, fontweight="bold")
fig.text(0.072, 0.062,
         "Satélites 3, 4 e 5 — coordenadas na chave. Testam se o agente salta "
         "distâncias: o 5 está a 143 m do centro da Mancha W e destacado dela.",
         fontsize=8.0, color=TINTA2)
fig.text(0.045, 0.030,
         "Não desenho os sectores de válvulas: o esquema de rega é um desenho à mão "
         "sem coordenadas, e georreferenciá-lo seria inventar precisão.",
         fontsize=7.2, color=TINTA3)

fig.savefig("figuras/F4_chave_espacial.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/F4_chave_espacial.svg", facecolor=FUNDO, bbox_inches="tight")
print("F4 gravada — frente em avanco %.2f ha" % (frente.sum() / 100.0))
