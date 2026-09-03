# -*- coding: utf-8 -*-
"""P04 — «Nada disto foi escolhido por nós». Fusão do IFAP com o Landsat.

Porque as duas sao uma
----------------------
As parcelas do IFAP e o Landsat pareciam duas pecas porque vem de dois sitios.
Mas a mensagem de nenhuma delas e «parcelas» ou «Landsat» — e a mesma, e e uma
so:

    O resultado nao depende de nada que nos tenhamos escolhido.

Uma fronteira que outra entidade desenhou, para pagamentos, anos antes. Um
instrumento de outra agencia, com outro sensor e outra cadeia de correccao.
Duas maneiras de tirar a nossa mao do resultado, e a peca e sobre isso.

Separadas, o caule ficava com nove pecas. Nove nao e um caule.

O que NAO entrou na fusao
-------------------------
A subida do copado oriental de 0,780 para 0,853 entre 2013 e 2017, que so o
Landsat ve. **Nao e corroboracao independente — e a morte do «declinio
cronico»**, que e a mensagem da P03. Foi para la, como anotacao da serie
oriental. Separacao por mensagem, nao por instrumento.

A serie completa de catorze anos tambem nao entra: fica na P04b, que e a
versao A4 desta metade. Aqui usa-se so a comparacao, que e o que carrega a
mensagem.

Duas ressalvas que viajam com os numeros
----------------------------------------
1. **Nao se comparam MAGNITUDES entre constelacoes.** 30 m contra 10 m: um
   pixel Landsat sobre o foco apanha copado sao a volta e atenua. Compara-se o
   degrau que cada uma mede na sua propria escala, com o seu proprio controlo.
2. **A parcela oriental nao e significativa** (p = 0,37) e a razao esta a
   vista: 0,12 ha sao doze celulas. O que ela estabelece e o NIVEL — 0,730
   contra 0,867-0,892 — e o nivel e medicao directa, nao inferencia.
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

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
L = sorted(json.load(open(os.path.join(VG, "ocidental_independente.json"))),
           key=lambda r: r["degrau"])
LS = json.load(open(os.path.join(VG, "landsat_degrau_absoluto.json")))
MV = json.load(open(os.path.join(VG, "multiverso_degrau.json")))
DR = json.load(open(os.path.join(VG, "degrau_vs_recta_pergola.json")))
C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
SAR = json.load(open(os.path.join(C2, "c2_09_sar_verificacao.json")))["c1_s15"]
INV = ["2016-17", "2017-18", "2018-19", "2019-20", "2020-21",
       "2021-22", "2022-23", "2023-24", "2024-25"]

AZUL, LARANJA, NEUTRO = "#2a78d6", "#eb6834", "#6b6f76"
TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, GRELHA = "#fcfcfb", "#eceae5"


def pt(v, casas=3, sinal=False):
    s = ("%+.*f" if sinal else "%.*f") % (casas, v)
    return s.replace("-", "−").replace(".", ",")


def cor_de(r):
    if "OCIDENTAL" in r["contem"]:
        return AZUL
    if "ORIENTAL" in r["contem"]:
        return LARANJA
    return NEUTRO


n = len(L)
y = np.arange(n)[::-1]

fig = plt.figure(figsize=(15.4, 7.9), dpi=200)
fig.patch.set_facecolor(FUNDO)

# ══════════════════════════════ METADE ESQUERDA — a fronteira ══════════════
axid = fig.add_axes([0.042, 0.205, 0.205, 0.505]); axid.axis("off")
axid.set_xlim(0, 1); axid.set_ylim(-0.75, n - 0.25)
for r, yy in zip(L, y):
    c, foco = cor_de(r), bool(r["contem"])
    axid.text(0, yy + 0.19, r["par"], ha="left", va="center", fontsize=9.6,
              color=TINTA if foco else TINTA2,
              fontweight="bold" if foco else "normal",
              family="DejaVu Sans Mono")
    axid.text(0, yy - 0.20,
              "%s ha c/ pérgola  ·  nível %s" % (pt(r["ha_com"], 2),
                                                 pt(r["base"])),
              ha="left", va="center", fontsize=8.0,
              color=c if foco else TINTA3,
              fontweight="bold" if foco else "normal")
    if foco:
        axid.plot([0.905], [yy + 0.19],
                  "o" if "OCIDENTAL" in r["contem"] else "D",
                  ms=8, color=c, mec=FUNDO, mew=1.4, clip_on=False)

ax2 = fig.add_axes([0.256, 0.205, 0.230, 0.505])
ax2.set_facecolor(FUNDO)
ax2.axvline(0, color="#c9c5bd", lw=1.0, zorder=1)
for r, yy in zip(L, y):
    c, foco, sig = cor_de(r), bool(r["contem"]), r["p"] < 0.05
    ax2.barh(yy, r["degrau"], height=0.44, color=c, zorder=3,
             alpha=1.0 if sig else 0.30, edgecolor=c, lw=0 if sig else 1.4)
    ax2.text(r["degrau"] - 0.0025, yy, pt(r["degrau"], sinal=True), ha="right",
             va="center", fontsize=10.2 if foco else 9.2, color=c,
             fontweight="bold" if foco else "normal")
    ax2.text(0.0028, yy, "p = %s%s" % (pt(r["p"], 3).lstrip("0"),
                                       "  ✳" if sig else ""),
             ha="left", va="center", fontsize=8.2, color=c if sig else TINTA3)
ax2.set_xlim(-0.081, 0.034)
ax2.set_ylim(-0.75, n - 0.25)
ax2.set_yticks([])
ax2.set_xticks([-0.06, -0.04, -0.02, 0])
ax2.set_xticklabels(["−0,06", "−0,04", "−0,02", "0"], fontsize=8.6, color=TINTA2)
ax2.grid(axis="x", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right", "left"):
    ax2.spines[s].set_visible(False)
ax2.spines["bottom"].set_color("#dcd9d3")
ax2.set_xlabel("queda de 2025-26  (NDVI)", fontsize=9.2, color=TINTA2, labelpad=7)

fig.text(0.042, 0.792, "A FRONTEIRA", fontsize=11.4, color=TINTA,
         fontweight="bold", va="top")
fig.text(0.042, 0.756,
         "As seis parcelas do IFAP que intersectam o pomar. Desenhadas por outra\n"
         "entidade, para pagamentos da PAC, anos antes — e não sabem nada de NDVI.",
         fontsize=8.9, color=TINTA2, linespacing=1.65, va="top")
fig.text(0.486, 0.756, "barra cheia\np < 0,05", fontsize=8.0, color=TINTA3,
         ha="right", linespacing=1.5, va="top")

# ══════════════════════════════ METADE DIREITA — os instrumentos ═══════════
# Dois blocos: em cima os dois opticos (mesma fisica, agencias diferentes), em
# baixo o radar (fisica diferente). A separacao e a mensagem: um segundo sensor
# optico e replica; um sensor que nao olha para a cor da folha e outra ordem de
# corroboracao.
axr = fig.add_axes([0.605, 0.432, 0.215, 0.243])
axr.set_facecolor(FUNDO)
PARES = [
    ("OCIDENTAL", AZUL, "o",
     [r["degrau"] for r in MV["unidades"] if r["foco"] == "OCIDENTAL"
      and r["unidade"] == "disco 90 m" and r["limiar"] == 0.5][0],
     LS["unidades"]["OCIDENTAL com pergola"]["degrau"]),
    ("ORIENTAL", LARANJA, "D",
     [r["degrau"] for r in MV["unidades"] if r["foco"] == "ORIENTAL"
      and r["unidade"] == "poligono Zona 0" and r["limiar"] == 0.5][0],
     LS["unidades"]["ORIENTAL com pergola"]["degrau"]),
    ("CONTROLO  ·  resto do pomar", NEUTRO, "s",
     DR["unidades"]["resto do pomar com pergola"]["NIVEL ABSOLUTO"]["degrau"],
     LS["unidades"]["resto do pomar  (CONTROLO)"]["degrau"]),
]
for nome, cor, mk, s2, ls_ in PARES:
    axr.plot([0, 1], [s2, ls_], "-", color=cor, lw=2.2, alpha=0.5, zorder=3)
    axr.plot([0, 1], [s2, ls_], mk, ms=9.5, color=cor, mec=FUNDO, mew=1.6,
             zorder=4)
    axr.text(-0.085, s2 + (0.006 if nome.startswith("ORI") else -0.004),
             pt(s2, sinal=True), ha="right", va="center",
             fontsize=10.2, color=cor, fontweight="bold")
    axr.text(1.085, ls_, pt(ls_, sinal=True), ha="left", va="center",
             fontsize=10.2, color=cor, fontweight="bold")
    axr.text(0.5, (s2 + ls_) / 2 + (0.019 if nome.startswith("CONTROLO") else 0.008),
             nome, ha="center", va="bottom",
             fontsize=9.2, color=cor, fontweight="bold")
axr.axhline(0, color="#c9c5bd", lw=1.0, zorder=1)
axr.set_xlim(-0.62, 1.62)
axr.set_ylim(-0.152, 0.030)
axr.set_xticks([0, 1])
axr.set_xticklabels(["Sentinel-2\nESA · MSI", "Landsat 8/9\nUSGS · OLI"],
                    fontsize=8.8, color=TINTA2, linespacing=1.6)
axr.set_yticks([])
for s in ("top", "right", "left"):
    axr.spines[s].set_visible(False)
axr.spines["bottom"].set_color("#dcd9d3")
fig.text(0.605, 0.700, "ÓPTICO  ·  duas agências, a mesma física",
         fontsize=9.0, color=TINTA2, fontweight="bold", va="top")

# ------------------------------------------------ radar: a outra física
axs = fig.add_axes([0.605, 0.198, 0.215, 0.132])
axs.set_facecolor(FUNDO)
FOCOS = [("OCIDENTAL", AZUL, 0), ("ORIENTAL", LARANJA, 1)]
yy = 0
rot_y, lab_y = [], []
sar_res = {}
for nome, cor, col in FOCOS:
    for orb in ("125", "147"):
        v = [SAR[orb][w][col] for w in INV]
        t = SAR[orb]["2025-26"][col]
        fora = not (min(v) <= t <= max(v))
        sar_res[(nome, orb)] = (min(v), max(v), t, fora)
        axs.plot([min(v), max(v)], [yy, yy], color=cor, lw=5.5, alpha=0.22,
                 solid_capstyle="butt", zorder=2)
        axs.plot([t], [yy], "o" if col == 0 else "D", ms=8.5, color=cor,
                 mec=FUNDO, mew=1.5, zorder=5,
                 mfc=cor if fora else "none")
        axs.text(t - 0.09 if fora else t + 0.13, yy,
                 pt(t, 2, sinal=True) if fora else "dentro da banda",
                 ha="right" if fora else "left", va="center",
                 fontsize=8.6 if fora else 7.8,
                 color=cor if fora else TINTA3,
                 fontweight="bold" if fora else "normal")
        rot_y.append(yy)
        lab_y.append("%s · órb. %s" % (nome[:4], orb))
        yy += 1
    yy += 0.55
axs.set_xlim(-1.62, 1.35)
axs.set_ylim(yy - 0.9, -0.75)
axs.set_yticks(rot_y)
axs.set_yticklabels(lab_y, fontsize=7.4, color=TINTA3)
for tl, (nm, _, _) in zip(axs.get_yticklabels(),
                          [f for f in FOCOS for _ in (0, 1)]):
    tl.set_color(AZUL if nm == "OCIDENTAL" else LARANJA)
axs.set_xticks([-1.5, -1.0, -0.5, 0, 0.5])
axs.set_xticklabels(["−1,5", "−1,0", "−0,5", "0", "0,5"], fontsize=8.4,
                    color=TINTA2)
axs.set_xlabel("γ⁰ VV do foco menos o pomar inteiro  (dB)", fontsize=8.6,
               color=TINTA2, labelpad=6)
axs.grid(axis="x", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right", "left"):
    axs.spines[s].set_visible(False)
axs.spines["bottom"].set_color("#dcd9d3")
fig.text(0.605, 0.358, "RADAR  ·  outra física", fontsize=9.0,
         color=TINTA2, fontweight="bold", va="top")
fig.text(0.716, 0.3585, "— barra = nove Invernos, marca = 2025-26",
         fontsize=7.6, color=TINTA3, va="top")

fig.text(0.605, 0.792, "OS INSTRUMENTOS", fontsize=11.4, color=TINTA,
         fontweight="bold", va="top")
fig.text(0.605, 0.756,
         "Três sensores, duas físicas. Um segundo óptico é réplica; um radar não\n"
         "olha para a cor da folha — mede estrutura e humidade.",
         fontsize=8.9, color=TINTA2, linespacing=1.65, va="top")

# a leitura do p em palavras: 0,011 le-se ao contrario do que significa
fig.text(0.845, 0.712, "O QUE O LANDSAT DIZ", fontsize=9.2, color=TINTA,
         fontweight="bold", va="top")
fig.text(0.845, 0.676,
         "Há 91 maneiras de partir catorze\n"
         "anos em doze e dois. Nos dois focos,\n"
         "a divisão que a natureza escolheu\n"
         "é a que dá o MAIOR degrau das 91.\n\n"
         "Não «passou à tangente»: é o extremo\n"
         "do que este teste pode medir.\n\n"
         "No resto do pomar a conta dá 0,98.",
         fontsize=8.3, color=TINTA2, va="top", linespacing=1.72)

fig.text(0.845, 0.418, "E O RADAR", fontsize=9.2, color=TINTA,
         fontweight="bold", va="top")
fig.text(0.845, 0.382,
         "441 cenas, dez Invernos, duas\n"
         "órbitas. O foco OCIDENTAL sai da\n"
         "sua banda nas duas.\n\n"
         "O ORIENTAL fica dentro, e sabe-se\n"
         "porquê: metade dele é chão, e chão\n"
         "já era baixo no radar em todos os\n"
         "dez Invernos. É o mesmo motivo por\n"
         "que ele teve de ser dividido.",
         fontsize=8.3, color=TINTA3, va="top", linespacing=1.72)

# divisoria entre as duas metades
fig.add_artist(plt.Line2D([0.545, 0.545], [0.175, 0.800], color="#e2dfd9",
                          lw=1.0, transform=fig.transFigure))

# ══════════════════════════════════════════════════════════════════ titulo
fig.text(0.042, 0.940, "Nada disto foi escolhido por nós",
         fontsize=23.5, fontweight="bold", color=TINTA)
fig.text(0.042, 0.895,
         "Uma fronteira desenhada por outra entidade, e três instrumentos que não são nossos. "
         "Duas maneiras de tirar a nossa mão do resultado.",
         fontsize=11.4, color=TINTA2)
fig.text(0.042, 0.856,
         "A parcela do foco ocidental cai 3 a 5 vezes mais do que qualquer outra da mesma exploração. "
         "E três sensores, em duas físicas, datam o mesmo acontecimento.",
         fontsize=11.4, color=TINTA, fontweight="bold")

fig.text(0.042, 0.128,
         "PORQUE ESTA PEÇA EXISTE: todas as outras unidades do dossiê têm uma fronteira que nós desenhámos, e todas as outras séries vêm do mesmo sensor. Aqui não há nem uma coisa nem outra.\n"
         "AS SEIS PARCELAS, não só a interessante — uma parcela que só parecesse extrema depois de escolhida não passaria neste teste. A escolha é geográfica: a que contém o ponto. ENT_ID 472062, verificável por terceiros.\n"
         "A PARCELA ORIENTAL NÃO É SIGNIFICATIVA (p = 0,37): 0,12 ha são doze células. O que ela estabelece é o NÍVEL — 0,730 contra 0,867–0,892 nas outras cinco — e o nível é medição directa, não inferência.\n"
         "NÃO SE COMPARAM MAGNITUDES entre constelações, e a figura não o faz: 30 m contra 10 m, e um píxel Landsat sobre o foco apanha copado são à volta. O que replica é a direcção, a datação e a separação do controlo.\n"
         "A ASSIMETRIA DO RADAR VAI ESCRITA: para o foco ocidental já havia instrumento independente antes do Landsat — o Sentinel-1, certificado pela camada 2 (441 cenas, reproduzidas da camada 1 à terceira casa). Para o oriental não havia, e é o Landsat que o traz.\n"
         "Se o radar vê o copado oriental depois de se lhe tirar o chão é pergunta POR CORRER, e está listada como aberta: a unidade certificada do radar é o disco inteiro, com a metade sem pérgola lá dentro.\n"
         "Só células com pérgola no LiDAR de 06-07-2025. Parcelas inteiras, sem recortes. p das parcelas por permutação da etiqueta de ano (20 000 sorteios); p do Landsat exacto, por enumeração das 91 divisões.",
         fontsize=7.9, color=TINTA3, linespacing=1.88, va="top")

fig.savefig(os.path.join(AQUI, "P04_nada_escolhido.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "P04_nada_escolhido.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito P04 — fusão IFAP + Landsat")
print("  parcela ocidental %+.4f (p=%.4f) contra mediana das outras %+.4f"
      % (L[0]["degrau"], L[0]["p"],
         float(np.median([r["degrau"] for r in L if not r["contem"]]))))
for nome, _, _, s2, ls_ in PARES:
    print("  %-28s S2 %+.4f   Landsat %+.4f" % (nome, s2, ls_))
