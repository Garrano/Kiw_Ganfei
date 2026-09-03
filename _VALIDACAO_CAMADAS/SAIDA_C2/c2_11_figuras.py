# -*- coding: utf-8 -*-
"""C2-11 — figuras da camada 2."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(POMAR)
SERIE = sorted(DATAS + ["2019-09-02"])
nd = carrega_ndvi(TODAS)
REFV = {d: float(np.nanmean(nd[d][REF])) for d in TODAS}
an = anos_decimais(SERIE)
E, N = centros_celulas()
rot = [d[2:7] for d in SERIE]

# ============================================================ F1
fig, ax = plt.subplots(2, 2, figsize=(13.5, 9))

a = ax[0, 0]
for nome, m, cor in [("referência sistemática", REF, "#2b7"),
                     ("pomar sem os dois focos", POMAR & ~do & ~de, "#888"),
                     ("foco OESTE (disco 90 m)", do, "#c33"),
                     ("foco ESTE plantado", ZONA0 & ~NU21, "#36c")]:
    v = [float(np.nanmean(nd[d][m])) for d in SERIE]
    a.plot(an, v, "o-", color=cor, label=nome, lw=1.8, ms=4)
a.axvspan(2024.9, 2026.7, color="#fdd", zorder=0)
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.set_ylabel("NDVI absoluto"); a.legend(fontsize=7.5, loc="lower left")
a.set_title("a) nível absoluto — os dois focos param juntos em 2025", fontsize=9.5)
a.grid(alpha=.25)

a = ax[0, 1]
ref = np.array([REFV[d] for d in SERIE])
for nome, m, cor in [("pomar sem os dois focos", POMAR & ~do & ~de, "#888"),
                     ("foco OESTE (disco 90 m)", do, "#c33"),
                     ("foco ESTE plantado", ZONA0 & ~NU21, "#36c")]:
    v = ref - np.array([float(np.nanmean(nd[d][m])) for d in SERIE])
    a.plot(an, v, "o-", color=cor, label=nome, lw=1.8, ms=4)
a.axhline(0, color="k", lw=.6)
a.axvspan(2024.9, 2026.7, color="#fdd", zorder=0)
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.set_ylabel("fosso até à referência (NDVI)")
a.legend(fontsize=7.5, loc="upper left")
a.set_title("b) a grandeza operativa: magnitude, não fracção", fontsize=9.5)
a.grid(alpha=.25)

a = ax[1, 0]
LIM = [0.05, 0.10, 0.15, 0.20, 0.25]
for t, cor in zip(LIM, plt.cm.viridis(np.linspace(0, .85, len(LIM)))):
    v = [mapa_defice(nd[d], POMAR, REFV[d], limiar=t).sum() / 100.0 for d in SERIE]
    a.plot(an, v, "o-", color=cor, label="limiar %.2f" % t, lw=1.6, ms=3.5)
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.set_ylabel("área em défice (ha)"); a.legend(fontsize=7.5)
a.set_title("c) a curva em U só existe ao limiar mais raso", fontsize=9.5)
a.grid(alpha=.25)

a = ax[1, 1]
fundo = mapa_defice(nd["2017-07-02"], POMAR, REFV["2017-07-02"], limiar=0.25)
v = [float(np.nanmean(nd[d][fundo])) for d in SERIE]
a.plot(an, v, "o-", color="#e73", lw=2, ms=5,
       label="as 5,37 ha em défice grave em 2017")
v2 = [float(np.nanmean(nd[d][REF])) for d in SERIE]
a.plot(an, v2, "o--", color="#2b7", lw=1.4, ms=3, label="referência sistemática")
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.set_ylabel("NDVI absoluto"); a.legend(fontsize=7.5, loc="lower right")
a.set_title("d) 0,50 → 0,75 num ano: é copado a instalar-se, não a recuperar",
            fontsize=9.5)
a.grid(alpha=.25)

fig.suptitle("C2 · F1 — a série com máscaras geográficas, e o que a curva em U "
             "é feita de", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, .96))
fig.savefig(os.path.join(SAIDA, "C2_F1_serie.png"), dpi=135)
plt.close(fig)
print("C2_F1_serie.png")

# ============================================================ F2
M = {d: mapa_defice(nd[d], POMAR, REFV[d]) for d in SERIE}
antes = [d for d in SERIE if d < "2025"]
SAO = POMAR & ~np.any([M[d] for d in antes], axis=0)
novo = M["2026-07-27"] & SAO

fig, ax = plt.subplots(2, 2, figsize=(14, 7.2))
ext = (AOI[0], AOI[2], AOI[1], AOI[3])


def base(a):
    a.imshow(np.where(POMAR, .82, np.nan), extent=ext, cmap="Greys",
             vmin=0, vmax=1, origin="upper")
    a.plot(*FOCO_OESTE, "x", color="#c33", ms=9, mew=2)
    a.plot(*FOCO_ESTE, "x", color="#36c", ms=9, mew=2)
    a.set_xlim(530200, 531500); a.set_ylim(4654850, 4655400)
    a.set_xticks([]); a.set_yticks([])


for i, d in enumerate(["2017-07-02", "2024-07-22", "2026-07-27"]):
    a = ax.ravel()[i]
    base(a)
    a.imshow(np.where(M[d], 1.0, np.nan), extent=ext, cmap="autumn_r",
             vmin=0, vmax=1.4, origin="upper")
    a.set_title("%s — défice %.2f ha" % (d, M[d].sum() / 100.0), fontsize=9.5)

a = ax.ravel()[3]
base(a)
a.imshow(np.where(NU21, 1.0, np.nan), extent=ext, cmap="bone", vmin=0, vmax=2.5,
         origin="upper")
a.imshow(np.where(novo, 1.0, np.nan), extent=ext, cmap="cool", vmin=0, vmax=1.4,
         origin="upper")
a.set_title("declínio novo pela regra M2: %.2f ha  ·  cinzento = chão lavrado 2021"
            % (novo.sum() / 100.0), fontsize=9.5, pad=6)
fig.suptitle("C2 · F2 — os mapas de défice, e o que passa a regra M2 "
             "(× vermelho = foco OESTE, × azul = foco ESTE)", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, .93))
fig.savefig(os.path.join(SAIDA, "C2_F2_mapas.png"), dpi=135)
plt.close(fig)
print("C2_F2_mapas.png")

# ============================================================ F3
pilha = np.load(os.path.join(SAIDA, "c2_07_sar_pilha.npy"))
meta = json.load(open(os.path.join(SAIDA, "c2_07_sar_cenas.json"), encoding="utf-8"))
inv = np.array([m["inverno"] for m in meta])
INVS = sorted(set(inv))
LADO = 6
P = {}
for i0 in range(0, NL, LADO):
    for j0 in range(0, NC, LADO):
        m = np.zeros((NL, NC), bool)
        m[i0:i0 + LADO, j0:j0 + LADO] = True
        m &= POMAR
        if m.sum() >= 20:
            P["q%02d_%02d" % (i0, j0)] = m
ks = sorted(P)


def dn(m, a2, b2):
    return float(np.nanmean(nd[b2][m]) - np.nanmean(nd[a2][m])
                 - (np.nanmean(nd[b2][POMAR]) - np.nanmean(nd[a2][POMAR])))


def vv(m, w):
    sub = pilha[inv == w]
    with np.errstate(invalid="ignore"):
        return float(np.nanmedian(np.nanmean(sub[:, m], axis=1)
                                  - np.nanmean(sub[:, POMAR], axis=1)))


X = np.array([dn(P[k], "2024-07-22", "2026-07-27") for k in ks])
XP = np.array([dn(P[k], "2022-07-31", "2024-07-22") for k in ks])
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))

a = ax[0]
Y = np.array([vv(P[k], "2025-26") for k in ks])
dmin = np.array([min(np.hypot(E[P[k]].mean() - FOCO_OESTE[0], N[P[k]].mean() - FOCO_OESTE[1]),
                     np.hypot(E[P[k]].mean() - FOCO_ESTE[0], N[P[k]].mean() - FOCO_ESTE[1]))
                 for k in ks])
s = a.scatter(X, Y, c=dmin, cmap="viridis_r", s=34, edgecolor="k", lw=.3)
plt.colorbar(s, ax=a, label="distância ao foco mais próximo (m)")
r, p = stats.spearmanr(X, Y)
a.set_xlabel("ΔNDVI 2024→2026, relativo ao pomar (Sentinel-2, óptico)")
a.set_ylabel("anomalia VV do Inverno 2025-26 (Sentinel-1, radar)")
a.set_title("a) 81 mosaicos de 60 m, cegos aos focos\nρ = %+.3f  p = %.1e" % (r, p),
            fontsize=9.5)
a.grid(alpha=.25)

a = ax[1]
re = [stats.spearmanr(X, [vv(P[k], w) for k in ks])[0] for w in INVS]
rp = [stats.spearmanr(XP, [vv(P[k], w) for k in ks])[0] for w in INVS]
x = np.arange(len(INVS))
a.bar(x - .2, re, .4, color="#c33", label="ΔNDVI 2024→2026 (o evento)")
a.bar(x + .2, rp, .4, color="#aaa", label="ΔNDVI 2022→2024 (placebo)")
a.axhline(0, color="k", lw=.7)
a.set_xticks(x); a.set_xticklabels(INVS, rotation=60, fontsize=7.5)
a.set_ylabel("ρ de Spearman entre os 81 mosaicos")
a.legend(fontsize=7.5)
a.set_title("b) o acordo entre instrumentos é específico\ndo Inverno de 2025-26",
            fontsize=9.5)
a.grid(alpha=.25, axis="y")

a = ax[2]
cr = json.load(open(os.path.join(SAIDA, "c2_08_cruzamento.json"), encoding="utf-8"))
tab = sorted(cr["valvulas"], key=lambda t: t["vv_anom"])
nomes = [t["valvula"] for t in tab]
a.barh(range(len(tab)), [t["vv_anom"] for t in tab],
       color=["#c33" if t["valvula"] == "v8" else "#89a" for t in tab])
a.set_yticks(range(len(tab))); a.set_yticklabels(nomes, fontsize=8)
a.axvline(0, color="k", lw=.7)
a.set_xlabel("anomalia de VV no Inverno de 2025-26 (dB)")
a.set_title("c) o teste que a C1 pediu: a válvula 8\ndestaca-se sozinha, nos dois "
            "instrumentos", fontsize=9.5)
a.grid(alpha=.25, axis="x")

fig.suptitle("C2 · F3 — o cruzamento NDVI × SAR sobre partições que não conhecem "
             "os focos", fontsize=11)
fig.tight_layout(rect=(0, 0, 1, .92))
fig.savefig(os.path.join(SAIDA, "C2_F3_cruzamento.png"), dpi=135)
plt.close(fig)
print("C2_F3_cruzamento.png")

# ============================================================ F4
fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.6))
a = ax[0]
prov = {}
with open(os.path.join(RAIZ, "sentinel", "proveniencia.json"), encoding="latin-1") as f:
    for c in json.load(f)["cenas"]:
        prov[c["data"]] = c["cena"][:3]
T2 = np.load(os.path.join(SAIDA, "c2_04_T2.npy"))
for nome, m, cor in [("referência sistemática (dentro do pomar)", REF, "#2b7"),
                     ("T2 mata estável fora do pomar", T2, "#753")]:
    v = [float(np.nanmean(nd[d][m])) for d in SERIE]
    a.plot(an, v, "o-", color=cor, label=nome, lw=1.8, ms=4)
for i, d in enumerate(SERIE):
    if prov[d] == "S2C":
        a.axvline(an[i], color="#c33", ls=":", lw=1.2)
a.text(an[-2], 0.90, "cenas S2C", color="#c33", fontsize=8, ha="center")
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.set_ylabel("NDVI absoluto"); a.legend(fontsize=7.5, loc="lower left")
a.set_title("a) metade da descida da referência é da cena,\nnão do pomar", fontsize=9.5)
a.grid(alpha=.25)

a = ax[1]
fe = [100 * float(np.nanmean(nd[d][de] < REFV[d] - 0.05)) for d in SERIE]
fo = [100 * float(np.nanmean(nd[d][do] < REFV[d] - 0.05)) for d in SERIE]
me = [1000 * (REFV[d] - float(np.nanmean(nd[d][de]))) for d in SERIE]
mo = [1000 * (REFV[d] - float(np.nanmean(nd[d][do]))) for d in SERIE]
a.plot(an, fe, "s--", color="#36c", label="fracção, foco ESTE (%)", lw=1.4, ms=4)
a.plot(an, fo, "s--", color="#c33", label="fracção, foco OESTE (%)", lw=1.4, ms=4)
a.plot(an, me, "o-", color="#36c", label="magnitude × 1000, ESTE", lw=2, ms=4)
a.plot(an, mo, "o-", color="#c33", label="magnitude × 1000, OESTE", lw=2, ms=4)
a.set_xticks(an); a.set_xticklabels(rot, rotation=45, fontsize=7)
a.legend(fontsize=7.5, loc="upper left")
a.set_title("b) a fracção satura e esconde: o ESTE vai de 54 % a 94 %\n"
            "com a magnitude constante", fontsize=9.5)
a.grid(alpha=.25)
fig.suptitle("C2 · F4 — os dois avisos de método: o nível absoluto e a fracção",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, .91))
fig.savefig(os.path.join(SAIDA, "C2_F4_metodo.png"), dpi=135)
plt.close(fig)
print("C2_F4_metodo.png")
