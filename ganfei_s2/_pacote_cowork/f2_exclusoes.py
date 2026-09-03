# -*- coding: utf-8 -*-
"""F2 — Livro-razao das exclusoes.

O trabalho desta figura nao e listar o que foi excluido: e mostrar o que cada
exclusao NAO cobre, e que as lacunas convergem todas para o mesmo sitio.
Estado = glifo (forma) + cor + rotulo, mesmo sistema da F1.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, FancyBboxPatch

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
LACUNA = "#efe7e4"          # painel da lacuna — quente, distinto do zebrado frio
AVISO, BOM, NEUTRO, CRIT = "#fab219", "#0ca30c", "#9a9890", "#d03b3b"

EXC = ("EXCLUÍDO", BOM, "vazio")
PAR = ("PARCIAL", AVISO, "meio")
RET = ("RETIRADO", NEUTRO, "traco")

VIAS = [
 dict(via="Precipitação",
      inst="ERA5-Land · 10 Invernos (Out–Mar)",
      medido="O Inverno 2024-25 rendeu 1157 mm — dos mais secos da década. Os de 2022-23 e 2023-24 renderam 1808 e 1809 mm com o pomar são.",
      est=EXC,
      lacuna="Drenagem local e toalha suspensa. A chuva regional não diz o que acontece a 60 cm de profundidade.",
      sub=True, fonte="pendente_precipitacao.csv"),
 dict(via="Água à superfície",
      inst="Sentinel-1 RTC · 71 cenas · 3 Invernos · 2 órbitas",
      medido="Δ (manchaW − sã) entre +0,12 e −0,08 dB, dentro do ruído entre cenas (dp 0,33–0,56). Nenhuma cena abaixo de −1,5 dB; uma lâmina de água daria −5 a −10.",
      est=EXC,
      lacuna="Água subsuperficial. O C-band penetra 2 a 5 cm em solo húmido — não vê a zona radicular.",
      sub=True, fonte="sar_invernos.csv"),
 dict(via="Geada radiativa tardia",
      inst="ERA5-Land horária · 2019–2026",
      medido="Mínima de 20/abr a 5/mai de 2025: 7,0 °C, com vento a 4,0 m/s — não é noite radiativa. Zero horas ≤2 °C em qualquer ano da série.",
      est=EXC,
      lacuna="Nada de material. A célula ERA5 tem 9 km e não resolve poças de ar frio, mas o vento a 4 m/s impede a poça formar-se.",
      sub=False, fonte="pendente_geada.csv"),
 dict(via="Micro-topografia",
      inst="LiDAR DGT · MDT 50 cm · 10 cm de precisão altimétrica",
      medido="ManchaW no percentil 32 de cota do pomar, zona0 no 92. Mas dentro do copado a cota baixa correlaciona com NDVI ALTO (r = −0,34): o baixo é o sítio saudável.",
      est=EXC,
      lacuna="A subsuperfície. Um MDT vê a superfície do terreno e mais nada. Vale dentro do copado — sobre toda a AOI a relação inverte, por artefacto de ocupação do solo.",
      sub=True, fonte="lidar_topografia_por_mascara.csv · cota_vs_ndvi.csv"),
 dict(via="Escoamento superficial",
      inst="pysheds sobre MDT 1 m · bacia de 49,1 ha, fechada",
      medido="1,1 % do pomar em linha de drenagem; manchaW 1,1 %; zona0 0,0 %. Mediana de área a montante: 1 m². Não há rede de drenagem a atravessar o pomar.",
      est=EXC,
      lacuna="Drenos enterrados — invisíveis a um MDT. E a rega da exploração é enterrada.",
      sub=True, fonte="pendente_escoamento.csv"),
 dict(via="Secagem do solo",
      inst="Sentinel-1 · 71 cenas contra dias desde chuva ≥5 mm",
      medido="ManchaW seca a −0,15 e −0,17 dB/dia; a zona sã a −0,12 e −0,17. Mesmo ritmo.",
      est=EXC,
      lacuna="Toalha suspensa a 40–80 cm. Testa a camada superficial, que é a única que o C-band alcança.",
      sub=True, fonte="pendente_sar_declives.csv"),
 dict(via="Atraso fenológico",
      inst="Sentinel-2 · 289 cenas de Primavera · 2018–2026",
      medido="Atraso da manchaW em 2025: −0,7 dias, ou seja nenhum. O coberto arrancou a horas e falhou durante a expansão. Solo frio e encharcado atrasaria o abrolhamento.",
      est=EXC,
      lacuna="Nada de material. O +6,7 dias de 2026 é em parte artefacto da amplitude reduzida.",
      sub=False, fonte="fenologia.csv"),
 dict(via="Nivelamento e truncatura\nde solo",
      inst="LiDAR · resíduo a 150 m · rugosidade a 25 m",
      medido="Resíduo zero em todas as máscaras: nenhuma bancada de corte ou aterro detectável. O pomar tem rugosidade quatro vezes mais uniforme que o terraço em redor.",
      est=PAR,
      lacuna="Trinta anos de lavoura suavizam bancadas. A truncatura resolve-se com fita métrica: espessura do horizonte A, nas covas.",
      sub=True, fonte="pendente_nivelamento.csv"),
 dict(via="Paleocanais e arquitectura\naluvial",
      inst="LiDAR · mosaico de 12,6 km² · 21 tiles",
      medido="O resíduo do terreno fica dominado por bordaduras de parcela e degraus de terraço. Não é legível.",
      est=PAR,
      lacuna="O emparcelamento apagou a expressão superficial. Num terraço reconstruído, o LiDAR tem pouco a dizer.",
      sub=True, fonte="t2_dem1m.npy"),
 dict(via="Térmico como linha\nindependente",
      inst="Landsat 8/9 · 137 cenas · 2017–2026",
      medido="ΔT = −15,5 × ΔNDVI + 0,67 °C, r = −0,756. Resíduo depois de retirar a cobertura: +0,07 em 2025 e +0,41 em 2026, dentro do ruído de 2017–2024.",
      est=RET,
      lacuna="Não é exclusão de um condutor — é a retirada de uma afirmação nossa. O térmico confirma a perda de copado; não acrescenta linha fisiológica independente.",
      sub=False, fonte="audit_a_b_cenas.csv"),
]

COL = [0.000, 0.205, 0.560, 0.665]
W_MED, W_LAC = 52, 44
TOPO = 0.900

fig = None


def altura():
    y = TOPO
    for v in VIAS:
        n = max(len(textwrap.wrap(v["medido"], W_MED)),
                len(textwrap.wrap(v["lacuna"], W_LAC)),
                v["via"].count(chr(10)) + 2)
        y -= 0.0150 * n + 0.026
    return y - 0.215


BAIXO = altura()
fig = plt.figure(figsize=(16.5, 16.5 * (1.02 - BAIXO) / 1.02), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.024, 0.008, 0.952, 0.982])
ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(BAIXO, 1.02)
T = ax.transData


def glifo(x, y, forma, cor):
    if forma == "vazio":
        ax.add_patch(Circle((x, y), 0.0058, facecolor="none", edgecolor=cor,
                            lw=1.7, transform=T, zorder=6, clip_on=False))
    elif forma == "meio":
        ax.add_patch(Circle((x, y), 0.0058, facecolor="none", edgecolor=cor,
                            lw=1.5, transform=T, zorder=6, clip_on=False))
        ax.add_patch(Wedge((x, y), 0.0058, 90, 270, facecolor=cor,
                           edgecolor="none", transform=T, zorder=6, clip_on=False))
    else:
        ax.plot([x - 0.0056, x + 0.0056], [y, y], color=cor, lw=2.0,
                transform=T, zorder=6, solid_capstyle="round", clip_on=False)


ax.text(0, 0.982, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
        fontsize=9.5, color=TINTA2, transform=T)
ax.text(0, 0.948, "Livro-razão das exclusões", fontsize=21, color=TINTA,
        fontweight="bold", transform=T)
ax.text(1, 0.952, "F2 · 28-08-2026", fontsize=8, color=TINTA3, ha="right",
        transform=T)
ax.text(0, 0.925,
        "Dez vias testadas por detecção remota. A coluna que interessa é a última: o que cada exclusão deixa de fora.",
        fontsize=8.6, color=TINTA2, transform=T)

for x, c in ((COL[0], "VIA TESTADA"), (COL[1], "O QUE FOI MEDIDO"),
             (COL[2], "VEREDICTO"), (COL[3], "O QUE A EXCLUSÃO NÃO COBRE")):
    ax.text(x, TOPO + 0.012, c, fontsize=7.6, color=TINTA2,
            fontweight="bold", transform=T)
ax.plot([0, 1], [TOPO + 0.002, TOPO + 0.002], color=TINTA, lw=1.1, transform=T)

y = TOPO
n_sub = 0
for k, v in enumerate(VIAS):
    wm = textwrap.wrap(v["medido"], W_MED)
    wl = textwrap.wrap(v["lacuna"], W_LAC)
    n = max(len(wm), len(wl), v["via"].count(chr(10)) + 2)
    h = 0.0150 * n + 0.026
    if k % 2 == 1:
        ax.add_patch(Rectangle((-0.008, y - h + 0.005), 0.665, h - 0.005,
                     facecolor=FAIXA, edgecolor="none", transform=T, zorder=0,
                     clip_on=False))
    # painel da lacuna, sempre destacado
    ax.add_patch(Rectangle((COL[3] - 0.012, y - h + 0.005), 0.355, h - 0.005,
                 facecolor=LACUNA, edgecolor="none", transform=T, zorder=0,
                 clip_on=False))
    ax.text(COL[0], y - 0.011, v["via"], fontsize=9.2, color=TINTA,
            fontweight="bold", va="top", transform=T, linespacing=1.3)
    ax.text(COL[0], y - 0.011 - 0.0155 * (v["via"].count(chr(10)) + 1),
            v["inst"], fontsize=6.9, color=TINTA3, va="top", transform=T)
    ax.text(COL[1], y - 0.011, "\n".join(wm), fontsize=7.5, color=TINTA2,
            va="top", transform=T, linespacing=1.42)
    glifo(COL[2] + 0.006, y - 0.0165, v["est"][2], v["est"][1])
    ax.text(COL[2] + 0.018, y - 0.0132, v["est"][0], fontsize=7.3, color=TINTA,
            fontweight="bold", va="top", transform=T)
    ax.text(COL[3], y - 0.011, "\n".join(wl), fontsize=7.5, color=TINTA,
            va="top", transform=T, linespacing=1.42)
    if v["sub"]:
        n_sub += 1
        ax.plot([COL[3] - 0.017, COL[3] - 0.017], [y - 0.010, y - h + 0.012],
                color=CRIT, lw=2.4, transform=T, solid_capstyle="round",
                clip_on=False, zorder=4)
    ax.text(COL[1], y - h + 0.012, v["fonte"], fontsize=6.3, color=TINTA3,
            transform=T)
    ax.plot([0, 1], [y - h + 0.005, y - h + 0.005], color=RISCA, lw=0.6,
            transform=T)
    y -= h

# ---- síntese: as lacunas convergem -----------------------------------------
y -= 0.030
ax.plot([0, 1], [y + 0.014, y + 0.014], color=TINTA, lw=1.1, transform=T)
ax.text(0, y - 0.004, "AS LACUNAS CONVERGEM", fontsize=8.4, color=TINTA,
        fontweight="bold", transform=T)

cx, cy = 0.615, y - 0.088
caixa = FancyBboxPatch((cx - 0.150, cy - 0.036), 0.300, 0.072,
                       boxstyle="round,pad=0.004", facecolor=LACUNA,
                       edgecolor=CRIT, lw=1.8, transform=T, zorder=3,
                       clip_on=False)
ax.add_patch(caixa)
ax.text(cx, cy + 0.014, "A SUBSUPERFÍCIE, 40–80 cm", fontsize=11.5,
        color=TINTA, fontweight="bold", ha="center", va="center", transform=T,
        zorder=5)
ax.text(cx, cy - 0.016,
        "toalha suspensa · horizonte impermeável · dreno enterrado · espessura do horizonte A",
        fontsize=7.2, color=TINTA2, ha="center", va="center", transform=T, zorder=5)

rot = [v["via"].replace(chr(10), " ") for v in VIAS if v["sub"]]
for i, r in enumerate(rot):
    yy = y - 0.026 - i * 0.0175
    ax.text(0.008, yy, r, fontsize=7.3, color=TINTA2, va="center", transform=T)
    ax.plot([0.175, 0.300], [yy, yy], color=TINTA3, lw=0.7, transform=T,
            clip_on=False)
    ax.annotate("", xy=(cx - 0.152, cy), xytext=(0.300, yy),
                arrowprops=dict(arrowstyle="-", color=CRIT, lw=1.0, alpha=0.55,
                                connectionstyle="arc3,rad=0.08"),
                transform=T, annotation_clip=False, zorder=2)

ax.text(0, y - 0.176,
        "Sete das dez vias, e todas as quatro que dizem respeito a água, deixam a mesma lacuna. "
        "Nenhum satélite vê abaixo dos primeiros centímetros: o C-band do Sentinel-1 penetra 2 a 5 cm, "
        "o MDT vê a superfície do terreno, o NDVI vê o coberto.",
        fontsize=8.0, color=TINTA2, transform=T)
ax.text(0, y - 0.199,
        "O instrumento que fecha esta lacuna são as COVAS DE PERFIL — e continuam por abrir.",
        fontsize=9.4, color=TINTA, fontweight="bold", transform=T)

# legenda de estados
yl = y - 0.232
for i, (rot_, cor, forma, nota) in enumerate([
        (*EXC, "hipótese afastada pela medição"),
        (*PAR, "afastada em parte; resta ir ao terreno"),
        (*RET, "afirmação nossa, retirada")]):
    x = i * 0.255
    glifo(x + 0.006, yl + 0.002, forma, cor)
    ax.text(x + 0.018, yl - 0.002, rot_, fontsize=7.2, color=TINTA,
            fontweight="bold", transform=T)
    ax.text(x + 0.018, yl - 0.016, nota, fontsize=6.6, color=TINTA2, transform=T)
ax.plot([0.775, 0.790], [yl + 0.002, yl + 0.002], color=CRIT, lw=2.4,
        transform=T, solid_capstyle="round")
ax.text(0.798, yl - 0.002, "lacuna subsuperficial", fontsize=7.2, color=TINTA,
        fontweight="bold", transform=T)
ax.text(0.798, yl - 0.016, "a marca vermelha na coluna da direita",
        fontsize=6.6, color=TINTA2, transform=T)

fig.savefig("F2_livro_razao_exclusoes.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F2_livro_razao_exclusoes.svg", facecolor=FUNDO, bbox_inches="tight")
print("F2 gravada — %d vias, %d com lacuna subsuperficial" % (len(VIAS), n_sub))
