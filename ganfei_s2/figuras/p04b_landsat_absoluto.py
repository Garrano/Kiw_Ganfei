# -*- coding: utf-8 -*-
"""P04b — a segunda constelação. Catorze anos de Landsat, em nível absoluto.

A pergunta a que esta figura responde
-------------------------------------
E a primeira que um revisor hostil faz, e nao e sobre estatistica:

    «Isto e o vosso processamento, ou e o campo?»

Todo o resto do dossie corre sobre Sentinel-2 — um sensor, uma agencia, uma
cadeia de correccao atmosferica, um arquivo. Esta e a unica serie que vem de
outro lado: **USGS/NASA em vez de ESA, OLI em vez de MSI, LaSRC em vez de
Sen2Cor, outra orbita, outra hora de passagem.** Partilha com o Sentinel-2
apenas o principio fisico.

Porque so agora se pode desenhar
--------------------------------
Enquanto a moeda foi «fosso a referencia», o Landsat era dificil de usar: a
referencia do Landsat cai 0,026 e a do Sentinel-2 cai 0,054 nas mesmas
celulas, e comparar dois fossos medidos contra duas referencias que se movem
de maneiras diferentes nao prova nada.

Em nivel absoluto o problema desaparece, porque **o teste passa a ser dentro
de cada constelacao**. Nao se compara o VALOR do Landsat com o do Sentinel-2 —
isso exigiria calibracao cruzada e seria atacavel. Compara-se o DEGRAU que
cada uma mede na sua propria escala, cada uma com o seu proprio controlo.

O p e EXACTO, nao amostrado
---------------------------
Catorze anos, dois tardios: C(14,2) = 91 divisoes possiveis. Enumeram-se todas.
Logo o p minimo atingivel e 1/91 = 0,011 — e os dois focos batem nesse minimo,
o que significa que o degrau observado e o maior de todas as 91 divisoes. Diz-se
na figura, porque um p de 0,011 sem essa nota parece mais fraco do que e.

O que esta figura NAO afirma
----------------------------
Que os degraus tenham a mesma MAGNITUDE nas duas constelacoes. Nao tem, e a
razao e conhecida: 30 m contra 10 m. Um pixel Landsat sobre o foco apanha
copado sao a volta, e a mistura atenua. **Replica-se a direccao, a datacao e a
separacao do controlo — nao o numero.** Escrito na figura.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
D = json.load(open(os.path.join(VG, "landsat_degrau_absoluto.json")))
MV = json.load(open(os.path.join(VG, "multiverso_degrau.json")))
DR = json.load(open(os.path.join(VG, "degrau_vs_recta_pergola.json")))

anos = D["anos"]
U = D["unidades"]
AZUL, LARANJA, NEUTRO, CHAOC = "#2a78d6", "#eb6834", "#6b6f76", "#b9b5ad"
TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, GRELHA = "#fcfcfb", "#eceae5"


def pt(v, casas=3, sinal=False):
    s = ("%+.*f" if sinal else "%.*f") % (casas, v)
    return s.replace("-", "−").replace(".", ",")


fig = plt.figure(figsize=(15.0, 8.4), dpi=200)
fig.patch.set_facecolor(FUNDO)

# ------------------------------------------------ painel principal: a serie
ax = fig.add_axes([0.052, 0.205, 0.585, 0.545])
ax.set_facecolor(FUNDO)
ax.axvspan(2024.5, 2026.55, color="#efe6df", zorder=0)
ax.text(2025.5, 0.935, "2025 · 2026", ha="center", fontsize=9,
        color="#a07a5f", fontweight="bold")

SER = [("OCIDENTAL com pérgola", "OCIDENTAL com pergola", AZUL, "o", 2.7, "-"),
       ("ORIENTAL com pérgola", "ORIENTAL com pergola", LARANJA, "D", 2.7, "-"),
       ("resto do pomar  ·  CONTROLO", "resto do pomar  (CONTROLO)", NEUTRO,
        "s", 2.2, "-"),
       ("chão sem pérgola  ·  controlo negativo",
        "ORIENTAL sem pergola  (controlo de chao)", CHAOC, "^", 1.5, (0, (5, 3)))]
for rot, chave, cor, mk, lw, ls in SER:
    v = U[chave]["serie"]
    ax.plot(anos, v, ls=ls, color=cor, lw=lw, zorder=4, solid_capstyle="round")
    ax.plot(anos, v, mk, color=cor, ms=6.8 if lw > 2 else 5.4, mec=FUNDO,
            mew=1.5, zorder=5)
    ax.annotate(pt(v[-1]), (anos[-1], v[-1]), xytext=(10, 0),
                textcoords="offset points", color=cor,
                fontsize=11 if lw > 2 else 9.2,
                fontweight="bold" if lw > 2 else "normal", va="center")

# os degraus NAO se anotam aqui: o painel da direita e que os mostra, e dois
# numeros para a mesma coisa na mesma figura e como nascem leituras trocadas.

ax.set_xlim(2012.4, 2028.6)
ax.set_ylim(0.545, 0.955)
ax.set_xticks(anos)
ax.set_xticklabels([str(a)[2:] for a in anos], fontsize=9.2, color=TINTA2)
ax.set_yticks([0.6, 0.7, 0.8, 0.9])
ax.set_yticklabels(["0,6", "0,7", "0,8", "0,9"], fontsize=9.4, color=TINTA2)
ax.set_ylabel("NDVI Landsat  ·  mediana anual, nível absoluto", fontsize=10,
              color=TINTA2, labelpad=9)
ax.grid(axis="y", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#dcd9d3")

leg = [Line2D([], [], color=c, lw=lw, ls=ls, marker=m,
              ms=6.8 if lw > 2 else 5.4, mec=FUNDO, mew=1.4, label=r)
       for r, _, c, m, lw, ls in SER]
ax.legend(handles=leg, loc="lower left", frameon=False, fontsize=9.2,
          labelspacing=0.6, handlelength=2.8, bbox_to_anchor=(-0.012, -0.015))

# cenas por ano
axn = fig.add_axes([0.052, 0.113, 0.585, 0.036])
ncen = {}
for a in anos:
    ncen[a] = 0
import collections
LJ = json.load(open(os.path.join(VG, "landsat.json")))
cont = collections.Counter(int(r["data"][:4]) for r in LJ)
axn.bar(anos, [cont[a] for a in anos], width=0.60, color="#dcd9d3")
for a in anos:
    axn.text(a, cont[a] + 1.4, "%d" % cont[a], ha="center", va="bottom",
             fontsize=6.6, color=TINTA3)
axn.set_xlim(2012.4, 2028.6); axn.set_ylim(0, 34)
axn.set_xticks([]); axn.set_yticks([]); axn.set_facecolor(FUNDO)
for s in axn.spines.values():
    s.set_visible(False)
axn.text(2012.3, 12, "cenas por ano  ", ha="right", va="center", fontsize=7.8,
         color=TINTA3)

# ---------------------------------------- painel direito: as duas constelacoes
axr = fig.add_axes([0.695, 0.205, 0.235, 0.545])
axr.set_facecolor(FUNDO)
S2 = {"OCIDENTAL": MV["unidades"], "ORIENTAL": MV["unidades"]}
PARES = [
    ("OCIDENTAL", AZUL, "o",
     [r["degrau"] for r in MV["unidades"] if r["foco"] == "OCIDENTAL"
      and r["unidade"] == "disco 90 m" and r["limiar"] == 0.5][0],
     U["OCIDENTAL com pergola"]["degrau"]),
    ("ORIENTAL", LARANJA, "D",
     [r["degrau"] for r in MV["unidades"] if r["foco"] == "ORIENTAL"
      and r["unidade"] == "poligono Zona 0" and r["limiar"] == 0.5][0],
     U["ORIENTAL com pergola"]["degrau"]),
    ("CONTROLO", NEUTRO, "s",
     DR["unidades"]["resto do pomar com pergola"]["NIVEL ABSOLUTO"]["degrau"],
     U["resto do pomar  (CONTROLO)"]["degrau"]),
]
xs = [0, 1]
for gi, (nome, cor, mk, s2, ls_) in enumerate(PARES):
    axr.plot(xs, [s2, ls_], "-", color=cor, lw=2.0, alpha=0.55, zorder=3)
    axr.plot(xs, [s2, ls_], mk, ms=9, color=cor, mec=FUNDO, mew=1.6, zorder=4)
    axr.text(-0.09, s2, pt(s2, sinal=True), ha="right", va="center",
             fontsize=10, color=cor, fontweight="bold")
    axr.text(1.09, ls_, pt(ls_, sinal=True), ha="left", va="center",
             fontsize=10, color=cor, fontweight="bold")
    axr.text(0.5, (s2 + ls_) / 2 + 0.0075, nome, ha="center", va="bottom",
             fontsize=9, color=cor, fontweight="bold")
axr.axhline(0, color="#c9c5bd", lw=1.0, zorder=1)
axr.set_xlim(-0.55, 1.55)
axr.set_ylim(-0.155, 0.028)
axr.set_xticks(xs)
axr.set_xticklabels(["Sentinel-2\nESA · MSI · 10 m",
                     "Landsat 8/9\nUSGS · OLI · 30 m"], fontsize=9,
                    color=TINTA2, linespacing=1.6)
axr.set_yticks([])
for s in ("top", "right", "left"):
    axr.spines[s].set_visible(False)
axr.spines["bottom"].set_color("#dcd9d3")
axr.text(0.5, 1.055, "O MESMO DEGRAU, DUAS CONSTELAÇÕES",
         transform=axr.transAxes, ha="center", fontsize=9.4, color=TINTA,
         fontweight="bold")
axr.text(0.5, 1.012,
         "cada uma na sua escala — não se comparam valores",
         transform=axr.transAxes, ha="center", fontsize=8.2, color=TINTA3)

# ------------------------------------------------------------------ titulo
fig.text(0.052, 0.945, "O outro instrumento vê o mesmo",
         fontsize=23, fontweight="bold", color=TINTA)
fig.text(0.052, 0.900,
         "Catorze anos de Landsat 8 e 9 — outra agência, outro sensor, outra correcção atmosférica, "
         "outra órbita. 140 cenas.",
         fontsize=11.4, color=TINTA2)
fig.text(0.052, 0.862,
         "Os dois focos dão degrau em 2025-26 (p = 0,011, o mínimo que 14 anos permitem). "
         "O resto do pomar não dá: −0,001, p = 0,98.",
         fontsize=11.4, color=TINTA, fontweight="bold")

fig.text(0.052, 0.068,
         "PORQUE CONTA COMO INDEPENDENTE: USGS/NASA e não ESA · sensor OLI e não MSI · correcção LaSRC e não Sen2Cor · outra órbita e outra hora de passagem. Partilha com o Sentinel-2 só o princípio físico.\n"
         "O p É EXACTO: 14 anos, 2 tardios, C(14,2) = 91 divisões possíveis, todas enumeradas. O mínimo atingível é 1/91 = 0,011 — e os dois focos batem nesse mínimo, ou seja o degrau observado é o maior das 91.\n"
         "NÃO SE REPLICA A MAGNITUDE, e não se afirma que se replique: 30 m contra 10 m, e um píxel Landsat sobre o foco apanha copado são à volta. O que replica é a direcção, a datação e a separação do controlo.\n"
         "O chão sem pérgola continua a ser o controlo negativo: ruidoso desde 2013, sem degrau (p = 0,42). O ficheiro contém também NDMI, cuja leitura foi RETIRADA pelo rastreio — e por isso não é desenhada.",
         fontsize=7.9, color=TINTA3, linespacing=1.9, va="top")

fig.savefig(os.path.join(AQUI, "P04b_landsat_absoluto.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "P04b_landsat_absoluto.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito P04b — Landsat")
for k, v in U.items():
    print("  %-42s %+.4f  p=%.4f" % (k, v["degrau"], v["p"]))
