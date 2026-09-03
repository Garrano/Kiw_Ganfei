# -*- coding: utf-8 -*-
"""C1-15 — figuras da camada do substrato."""
import os, sys, json, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

g = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))
g2 = dict(np.load(os.path.join(SAIDA, "c1_11_escalas.npz")))
masc, _ = carrega_mascaras()
pomar, saud, zona0, nu = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(pomar)
V = valvulas()
solo = json.load(open(os.path.join(SAIDA, "c1_06_solo_colocado.json"), encoding="utf-8"))
ext = [AOI[0], AOI[2], AOI[1], AOI[3]]

def moldura(ax, tit):
    ax.set_title(tit, fontsize=10, loc="left")
    ax.set_xlim(530100, 531600); ax.set_ylim(4654800, 4655500)
    ax.set_aspect("equal"); ax.tick_params(labelsize=7)
    ax.set_xlabel("E (EPSG:32629)", fontsize=7); ax.set_ylabel("N", fontsize=7)

def focos(ax, leg=False):
    for (e, n), c, nome in ((FOCO_OESTE, "#1f77b4", "foco OESTE «Zona 0»"),
                            (FOCO_ESTE, "#d62728", "foco ESTE (B3)")):
        ax.add_patch(Circle((e, n), 90, fill=False, ec=c, lw=2,
                            label=nome if leg else None))
        ax.plot(e, n, "+", color=c, ms=9, mew=2)

def valv(ax, rot=True):
    for k, v in V.items():
        ax.plot(v["E"], v["N"], "o", ms=4, mfc="w", mec="k", mew=0.8, zorder=5)
        if rot:
            ax.annotate(k, (v["E"], v["N"]), textcoords="offset points",
                        xytext=(0, 6), ha="center", fontsize=6, zorder=6)

# ================= F1: substrato =================
fig, axs = plt.subplots(3, 1, figsize=(12, 13))
m = np.where(pomar, g["cota"], np.nan)
im = axs[0].imshow(m, extent=ext, cmap="terrain", origin="upper")
plt.colorbar(im, ax=axs[0], label="cota MDT (m)", fraction=0.02)
focos(axs[0], True); valv(axs[0])
moldura(axs[0], "F1a · Cota do MDT LiDAR 50 cm no pomar (30,31 ha).\n"
                "Foco ESTE +1,20 m acima do foco OESTE, e +0,59 m acima do perfil longitudinal do pomar.")
axs[0].legend(fontsize=7, loc="lower right")

m = np.where(pomar, g2["hand"], np.nan)
im = axs[1].imshow(m, extent=ext, cmap="RdYlBu_r", origin="upper", vmin=0, vmax=1.0)
plt.colorbar(im, ax=axs[1], label="altura sobre a drenagem, HAND (m)", fraction=0.02)
focos(axs[1]); valv(axs[1], False)
moldura(axs[1], "F1b · Altura sobre a linha de drenagem mais proxima (HAND).\n"
                "OESTE 0,13 m | referencia 0,15 m | ESTE 0,35 m.   Distancia a drenagem: 13 | 24 | 56 m.")

rgb = np.zeros(pomar.shape + (4,))
rgb[pomar] = (0.85, 0.85, 0.85, 1)
rgb[nu] = (0.55, 0.27, 0.07, 1)
axs[2].imshow(rgb, extent=ext, origin="upper")
focos(axs[2]); valv(axs[2], False)
moldura(axs[2], "F1c · Chao lavrado na ortofoto de 2021 (1,67 ha, castanho).\n"
                "101 das 167 celulas caem no foco ESTE (40 % dele); ZERO no OESTE, ZERO na referencia.")
fig.tight_layout()
fig.savefig(os.path.join(SAIDA, "C1_F1_substrato.png"), dpi=140)
plt.close(fig)

# ================= F2: quimica no mapa =================
fig, ax = plt.subplots(figsize=(13, 5.2))
ax.imshow(np.where(pomar, 1.0, np.nan), extent=ext, cmap="Greys", vmin=0, vmax=3, origin="upper")
focos(ax, True); valv(ax)
for r in solo:
    if r["E"] is None or r["confianca"] == "FORA DA BANDA":
        continue
    cao = r["CaO"]
    cor = plt.cm.RdYlGn(min(cao / 1300.0, 1.0))
    ax.scatter([r["E"]], [r["N"]], s=260, marker="s", c=[cor], ec="k", lw=1.2, zorder=7)
    if r["raio_incerteza_m"]:
        ax.add_patch(Circle((r["E"], r["N"]), r["raio_incerteza_m"], fill=False,
                            ec="k", ls=":", lw=0.8))
    ax.annotate("%s\nCaO %s%d  pH %.1f" %
                (r["bloco"], "<" if r["CaO_censurado"] else "", cao, r["pH"]),
                (r["E"], r["N"]), textcoords="offset points", xytext=(0, -34),
                ha="center", fontsize=7, zorder=8,
                bbox=dict(fc="w", alpha=0.75, ec="none", pad=1.2))
moldura(ax, "F2 · Os boletins A2 no mapa, pela primeira vez (R2 G35).\n"
            "Quadrado = posicao do bloco; circulo a ponteado = incerteza dentro do bloco.\n"
            "B3, o bloco do foco ESTE, tem o CaO mais baixo de toda a exploracao (<154 mg/kg) "
            "entre vizinhos com 505 e 1100.  Escala de cor: vermelho = pobre, verde = rico.")
fig.tight_layout()
fig.savefig(os.path.join(SAIDA, "C1_F2_quimica_no_mapa.png"), dpi=140)
plt.close(fig)

# ================= F3: SAR por Inverno =================
L = list(csv.DictReader(open(os.path.join(SAIDA, "c1_13_sar_serie.csv"), encoding="utf-8")))
inv = np.array([r["inverno"] for r in L]); orb = np.array([int(r["orbita"]) for r in L])
c = lambda k: np.array([float(r[k]) for r in L])
ref = c("referencia")
invs = sorted(set(inv))
fig, axs = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True)
for ax, o in zip(axs, (125, 147)):
    for k, cor, lab in (("lavrado2021", "#8c564b", "chao lavrado em 2021 (1,67 ha)"),
                        ("este_nao_lavrado", "#d62728", "foco ESTE, parte nao lavrada"),
                        ("oeste", "#1f77b4", "foco OESTE «Zona 0»"),
                        ("pomar", "#7f7f7f", "pomar inteiro")):
        y = [np.nanmedian((c(k) - ref)[(inv == i) & (orb == o)]) for i in invs]
        ax.plot(invs, y, "o-", color=cor, label=lab, lw=1.6, ms=4)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(invs.index("2021-22") - 0.5, color="g", ls="--", lw=1)
    ax.text(invs.index("2021-22") - 0.45, -3.3, "ortofoto de 2021", color="g", fontsize=7, rotation=90)
    ax.set_title("orbita %d" % o, fontsize=10)
    ax.tick_params(axis="x", rotation=60, labelsize=7); ax.grid(alpha=0.25)
    ax.set_xlabel("Inverno (Nov-Mar)", fontsize=8)
axs[0].set_ylabel("VV menos referencia sistematica (dB)", fontsize=8)
axs[0].legend(fontsize=7, loc="lower left")
fig.suptitle("F3 · Sentinel-1 RTC, 441 cenas, dez Invernos, mascaras geograficas (sem NDVI).  "
             "O deficit do chao lavrado JA EXISTIA em 2016-17: a lavra de 2021 nao o criou.\n"
             "O foco OESTE e indistinguivel da referencia em nove Invernos e cai ~1,1 dB no de 2025-26, "
             "nas duas orbitas.", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(os.path.join(SAIDA, "C1_F3_sar_invernos.png"), dpi=140)
plt.close(fig)

# ================= F4: sinopse do contraste =================
fig, axs = plt.subplots(1, 5, figsize=(14, 3.6))
UN = [("OESTE", do, "#1f77b4"), ("ref.", saud, "#2ca02c"), ("ESTE", de, "#d62728")]
paineis = [("cota (m)", g["cota"]), ("declive de forma 50 m (deg)", g2["declive_forma"]),
           ("HAND (m)", g2["hand"]), ("distancia a drenagem (m)", g2["dist_dren"]),
           ("rugosidade 25 m (m)", g["rug25"])]
for ax, (tit, campo) in zip(axs, paineis):
    ax.bar(range(3), [np.nanmedian(campo[m]) for _, m, _ in UN],
           color=[c for _, _, c in UN],
           yerr=[[np.nanmedian(campo[m]) - np.nanpercentile(campo[m], 25) for _, m, _ in UN],
                 [np.nanpercentile(campo[m], 75) - np.nanmedian(campo[m]) for _, m, _ in UN]],
           capsize=3)
    ax.set_xticks(range(3)); ax.set_xticklabels([n for n, _, _ in UN], fontsize=8)
    ax.set_title(tit, fontsize=8); ax.grid(axis="y", alpha=0.25)
fig.suptitle("F4 · O substrato nos dois focos e na referencia sistematica (mediana, barras = quartis).  "
             "O declive de FORMA nao os separa; a cota, a altura sobre a drenagem e a distancia a drenagem separam.", fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.88])
fig.savefig(os.path.join(SAIDA, "C1_F4_contraste.png"), dpi=140)
plt.close(fig)
print("escritas C1_F1..F4")
