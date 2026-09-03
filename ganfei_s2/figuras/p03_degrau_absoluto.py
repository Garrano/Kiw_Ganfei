# -*- coding: utf-8 -*-
"""P03 — a peca central. O degrau em NIVEL ABSOLUTO, com controlo interno.

O que esta peca tem de fazer
----------------------------
Todos os ataques que este caso levou foram sobre circularidade: mascaras
tiradas do sinal que depois se media, referencia escolhida dentro do mesmo
poligono pela ultima cena. Esta figura tem de fechar essa classe inteira.

Fecha-a por construcao, e nao por argumento:

  · a grandeza e o NIVEL ABSOLUTO de NDVI — nao ha referencia para contaminar;
  · a particao planta/chao vem do LiDAR de 06-07-2025, outro instrumento;
  · as fronteiras das unidades sao geograficas, de ficheiro anterior a analise;
  · e o CONTROLO — o resto do pomar, com pergola, nas mesmas cenas e no mesmo
    pipeline — esta desenhado ao lado, nao escondido no rodape.

Se o degrau fosse do sensor, da atmosfera, do arquivo ou do nosso codigo, o
controlo tinha-o tambem. Nao tem: -0,014, p = 0,51.

Porque o painel da direita existe
---------------------------------
Na moeda antiga a unidade escolhida decidia o veredicto — o poligono dava
p = 0,029 e o disco de 90 m dava p = 0,061. Publicar so a corrida preferida
seria exactamente o relato selectivo que a literatura do multiverso descreve.

O painel direito mostra as **43 analises** — 5 unidades x 3 raios x 5 limiares
de altura — como pontos. Nenhuma se esconde. A leitura e a SEPARACAO entre as
duas nuvens, nao a posicao de nenhum ponto.

Escolhas de forma
-----------------
Duas moedas na mesma figura seriam duas respostas para a mesma pergunta: so
nivel absoluto. Rotulo directo em cada linha alem da legenda, e marcador
proprio por serie — identidade nunca so por cor. O controlo e neutro de
proposito: e o que ele e. Falha o piso de croma do validador, e a falha e
deliberada e esta compensada por marcador e rotulo directo.
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

MV = json.load(open(os.path.join(VG, "multiverso_degrau.json")))
SP = json.load(open(os.path.join(VG, "serie_oriental_pergola.json")))
DR = json.load(open(os.path.join(VG, "degrau_vs_recta_pergola.json")))

DATAS = SP["datas"]
x = np.arange(len(DATAS))
rot = [d[2:4] for d in DATAS]


def da_mv(foco, unidade, limiar=0.5):
    for r in MV["unidades"]:
        if r["foco"] == foco and r["unidade"] == unidade and r["limiar"] == limiar:
            return r
    raise KeyError((foco, unidade, limiar))


def ctrl(limiar=0.5):
    for r in MV["controlo"]:
        if r["limiar"] == limiar:
            return r
    raise KeyError(limiar)


OR_ = da_mv("ORIENTAL", "poligono Zona 0")
OC_ = da_mv("OCIDENTAL", "disco 90 m")
CHAO = SP["fosso"]["Zona 0 SEM pergola  (<0,5 m)"]["nivel"]

# O controlo depende de quanto se exclui a volta dos focos: excluindo discos de
# 90 m da -0,0136; excluindo 120 m mais a Zona 0 da -0,0017. Desenha-se o
# CONSERVADOR — o que menos favorece a tese — e imprime-se a amplitude.
_c = DR["unidades"]["resto do pomar com pergola"]["NIVEL ABSOLUTO"]
CT_ = dict(serie=_c["serie"], degrau=_c["degrau"], p=_c["p_perm"])
CT_LARGO = ctrl()

AZUL, LARANJA, NEUTRO, CHAOC = "#2a78d6", "#eb6834", "#6b6f76", "#b9b5ad"
TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, GRELHA = "#fcfcfb", "#eceae5"

fig = plt.figure(figsize=(14.6, 8.2), dpi=200)
fig.patch.set_facecolor(FUNDO)

# ----------------------------------------------------------- painel esquerdo
ax = fig.add_axes([0.055, 0.175, 0.545, 0.585])
ax.set_facecolor(FUNDO)
ax.axvspan(6.5, 8.45, color="#efe6df", zorder=0)
ax.text(7.5, 0.9345, "2025 · 2026", ha="center", fontsize=9, color="#a07a5f",
        fontweight="bold")

SER = [("OCIDENTAL  ·  E≈530 485", OC_["serie"], AZUL, "o", 2.7, "-"),
       ("ORIENTAL  ·  E≈530 999", OR_["serie"], LARANJA, "D", 2.7, "-"),
       ("resto do pomar  ·  CONTROLO", CT_["serie"], NEUTRO, "s", 2.2, "-"),
       ("chão sem pérgola  ·  controlo negativo", CHAO, CHAOC, "^", 1.5, (0, (5, 3)))]
for nome, v, cor, mk, lw, ls in SER:
    ax.plot(x, v, ls=ls, color=cor, lw=lw, zorder=4, solid_capstyle="round")
    ax.plot(x, v, mk, color=cor, ms=7.2 if lw > 2 else 5.6, mec=FUNDO, mew=1.6,
            zorder=5)

def pt(v, casas=3, sinal=False):
    """Numero em convencao portuguesa: virgula decimal e sinal de menos U+2212."""
    s = ("%+.*f" if sinal else "%.*f") % (casas, v)
    return s.replace("-", "−").replace(".", ",")


for nome, v, cor, mk, lw, ls in SER:
    ax.annotate(pt(v[-1]), (x[-1], v[-1]), xytext=(11, 0),
                textcoords="offset points", color=cor,
                fontsize=11.5 if lw > 2 else 9.5,
                fontweight="bold" if lw > 2 else "normal", va="center")

for v, cor, d in ((OC_["serie"], AZUL, OC_["degrau"]),
                  (OR_["serie"], LARANJA, OR_["degrau"])):
    base = float(np.mean(v[:7]))
    ax.annotate("", xy=(8.06, v[-1]), xytext=(8.06, base),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=cor,
                                shrinkA=0, shrinkB=0, alpha=0.55))
ax.text(8.42, 0.795, "−0,129", color=AZUL, fontsize=13, fontweight="bold",
        ha="left", va="center")
ax.text(8.42, 0.762, "−0,124", color=LARANJA, fontsize=13, fontweight="bold",
        ha="left", va="center")
ax.text(8.42, 0.883, "−0,014", color=NEUTRO, fontsize=10.5, ha="left",
        va="center")

# O PRÓLOGO QUE MATA O «CRÓNICO». A serie do Sentinel-2 comeca em 2017, e ate
# la nao se ve nada. O Landsat viu, e viu o contrario de declinio: este mesmo
# copado SUBIU 0,072 entre 2013 e 2017. Entra como anotacao e nao como linha,
# porque juntar duas constelacoes num eixo seria comparar escalas que nao sao
# comparaveis — e essa e a ressalva da propria P04b.
LS = json.load(open(os.path.join(VG, "landsat_degrau_absoluto.json")))
_ls = LS["unidades"]["ORIENTAL com pergola"]["serie"]
_sub = _ls[LS["anos"].index(2017)] - _ls[0]
ax.annotate("", xy=(-0.04, OR_["serie"][0] + 0.008), xytext=(0.62, 0.9245),
            arrowprops=dict(arrowstyle="-", lw=1.0, color=LARANJA, alpha=0.45,
                            connectionstyle="arc3,rad=0.22"))
ax.text(0.02, 0.9535,
        "antes disto, o Landsat viu este copado a SUBIR %s de 2013 a 2017.\n"
        "Não vinha em declínio — o «crónico» é o chão ao lado, não esta planta."
        % pt(_sub, sinal=True),
        fontsize=8.6, color=LARANJA, va="top", ha="left", linespacing=1.7)

ax.set_xlim(-0.45, 9.9)
ax.set_ylim(0.55, 0.955)
ax.set_xticks(x)
ax.set_xticklabels(rot, fontsize=9.6, color=TINTA2)
ax.set_yticks([0.6, 0.7, 0.8, 0.9])
ax.set_yticklabels(["0,6", "0,7", "0,8", "0,9"], fontsize=9.6, color=TINTA2)
ax.set_ylabel("NDVI  ·  nível absoluto, sem referência", fontsize=10.2,
              color=TINTA2, labelpad=9)
ax.grid(axis="y", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#dcd9d3")

leg = [Line2D([], [], color=c, lw=lw, ls=ls, marker=m,
              ms=7.2 if lw > 2 else 5.6, mec=FUNDO, mew=1.5, label=n)
       for n, _, c, m, lw, ls in SER]
ax.legend(handles=leg, loc="lower left", frameon=False, fontsize=9.3,
          labelspacing=0.62, handlelength=2.8, bbox_to_anchor=(-0.012, -0.012))

# ------------------------------------------------------------ painel direito
axm = fig.add_axes([0.665, 0.175, 0.245, 0.585])
axm.set_facecolor(FUNDO)
GRUPOS = [("OCIDENTAL", AZUL, "o"), ("ORIENTAL", LARANJA, "D"),
          ("CONTROLO", NEUTRO, "s")]
RNGj = np.random.default_rng(7)
for gi, (foco, cor, mk) in enumerate(GRUPOS):
    if foco == "CONTROLO":
        vals = [r["degrau"] for r in MV["controlo"]]
        indep = [True] * len(vals)
    else:
        rs = [r for r in MV["unidades"] if r["foco"] == foco]
        vals = [r["degrau"] for r in rs]
        indep = [r["independente"] for r in rs]
    y = gi + RNGj.uniform(-0.20, 0.20, len(vals))
    for v, yy, ind in zip(vals, y, indep):
        axm.plot([v], [yy], mk, ms=6.4, mfc=cor if ind else "none",
                 mec=cor, mew=1.5 if not ind else 1.0, alpha=0.9, zorder=4)
    axm.plot([min(vals), max(vals)], [gi - 0.36, gi - 0.36], color=cor, lw=2.4,
             solid_capstyle="butt", zorder=3)
    # a etiqueta do controlo sairia da margem: ancora-se a esquerda do intervalo
    if foco == "CONTROLO":
        ex, ha = min(vals) - 0.006, "right"
    else:
        ex, ha = float(np.mean([min(vals), max(vals)])), "center"
    axm.text(ex, gi - 0.50,
             "%s a %s" % (pt(max(vals), sinal=True), pt(min(vals), sinal=True)),
             ha=ha, va="top", fontsize=8.2, color=cor)
    axm.text(0.008, gi + 0.42, "%s  ·  n=%d" % (foco, len(vals)),
             fontsize=9.4, color=cor, fontweight="bold", va="bottom",
             transform=axm.get_yaxis_transform())

axm.axvline(0, color=TINTA3, lw=0.9, zorder=1)
axm.set_xlim(-0.205, 0.022)
axm.set_ylim(2.85, -0.72)
axm.set_yticks([])
axm.set_xticks([-0.2, -0.15, -0.1, -0.05, 0])
axm.set_xticklabels(["−0,20", "−0,15", "−0,10", "−0,05", "0"], fontsize=8.8,
                    color=TINTA2)
axm.set_xlabel("degrau de 2025-26  (NDVI)", fontsize=9.4, color=TINTA2,
               labelpad=7)
axm.grid(axis="x", color=GRELHA, lw=0.9, zorder=0)
for s in ("top", "right", "left"):
    axm.spines[s].set_visible(False)
axm.spines["bottom"].set_color("#dcd9d3")
axm.text(0.5, 1.055, "AS 43 ANÁLISES, TODAS", transform=axm.transAxes,
         ha="center", fontsize=9.6, color=TINTA, fontweight="bold")
axm.text(0.5, 1.012, "5 unidades × 3 raios × 5 limiares de altura",
         transform=axm.transAxes, ha="center", fontsize=8.4, color=TINTA3)
axm.plot([-0.186], [2.62], "o", ms=6.4, mfc="none", mec=AZUL, mew=1.5,
         clip_on=False)
axm.text(-0.176, 2.62, "vazio = fronteira centrada no sinal", fontsize=7.8,
         color=TINTA3, va="center")

# ------------------------------------------------------------------- titulo
fig.text(0.055, 0.945, "Um acontecimento, dois sítios, o mesmo tamanho",
         fontsize=23, fontweight="bold", color=TINTA)
fig.text(0.055, 0.900,
         "Nível absoluto de NDVI no copado vivo — só células com pérgola no LiDAR de 06-07-2025.",
         fontsize=11.6, color=TINTA2)
fig.text(0.055, 0.862,
         "Os dois focos caíram cerca de 0,125 em duas épocas. O resto do pomar caiu 0,014, "
         "que é indistinguível de ruído.",
         fontsize=11.6, color=TINTA, fontweight="bold")

fig.text(0.055, 0.108,
         "SEM REFERÊNCIA: a grandeza é o nível absoluto, logo não há referência que possa ser contaminada pelos próprios focos — e estava: 14 das 110 células da grelha de referência caem dentro dos discos.\n"
         "O CONTROLO É A PROVA: resto do pomar, com pérgola, mesmas nove cenas, mesmo processamento. Se o degrau viesse do sensor, da atmosfera, do arquivo ou do nosso código, apareceria aqui. Não aparece (p = 0,51).\n"
         "Está desenhado o controlo CONSERVADOR, que exclui 90 m à volta de cada foco: −0,014. Excluindo 120 m mais o polígono oriental fica −0,002 — a escolha desenhada é a que menos favorece a leitura.\n"
         "A partição planta/chão vem do LiDAR — instrumento independente do NDVI. Fronteiras das unidades: polígono geográfico de ficheiro anterior à análise. O disco ocidental é a excepção e vai marcada.\n"
         "FORMA DA SÉRIE: o degrau ajusta 3,5 a 4,0 vezes melhor do que uma recta nas três unidades de foco (soma de quadrados, mesmo número de parâmetros), e 0,8 no controlo, onde ganha a recta. Não é declínio\n"
         "contínuo — são dois patamares. Razões calculadas em nível absoluto, a mesma moeda da figura. p por permutação da etiqueta de ano, 20 000 sorteios.",
         fontsize=7.9, color=TINTA3, linespacing=1.9, va="top")

fig.savefig(os.path.join(AQUI, "P03_degrau_absoluto.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "P03_degrau_absoluto.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito P03  ·  ORIENTAL %+.4f  OCIDENTAL %+.4f  CONTROLO %+.4f"
      % (OR_["degrau"], OC_["degrau"], CT_["degrau"]))
print("multiverso: %d analises de foco, %d de controlo"
      % (len(MV["unidades"]), len(MV["controlo"])))
