# -*- coding: utf-8 -*-
"""M1 v5 — para a gestora. ZERO informacao sobre declinio, como sempre.

Porque ha uma v5
----------------
A v4 mostrava duas colocacoes de valvulas que discordavam em 469 m e pedia que
se fosse a valvula 10 dizer qual estava certa. Desde entao:

  * a gestora deu a coordenada do ARMAZEM (42.045095, -8.633148). A colocacao
    por contagem de fileiras punha a linha 222 — "conduta principal a saida do
    armazem" — a 321 m de onde o armazem esta. A ancoragem nos extremos da
    parcela, que produzia a coincidencia de "0,3%", estava errada: era uma
    suposicao imposta, nao testada.

  * a gestora deu as duas pontas do B1 (42.03757663,-8.64358173 e
    42.04118411,-8.63687114). O B1 fica a 526 m a sudoeste do corpo principal
    e aterra exactamente sobre os blocos que uma sessao independente tinha
    delimitado na ortofoto sem nunca olhar para NDVI.

  * mediu-se a cobertura clara (rede/plastico) na ortofoto de 2025 com um
    criterio de luminancia E saturacao: 83% do corpo principal e 71% do B1.
    Uma medicao anterior, so por luminancia, dava 25% e estava errada.

A v5 mostra o que ficou estabelecido, retira o que caiu — incluindo a nossa
propria medicao de cobertura, que nao se sustenta — e acrescenta a
pergunta da rede — que e nova e pode ser a mais importante das cinco.
"""
import json
import os
import textwrap
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM, AZUL = "#d03b3b", "#fab219", "#0a7a0a", "#0d5fc4"

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AOI = (529950, 4654600, 531950, 4655600)
W = (529280, 4653880, 531700, 4655480)
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
ARM = tr.transform(-8.633148, 42.045095)
B1I = tr.transform(-8.643581734449253, 42.03757663209986)
B1F = tr.transform(-8.636871142810762, 42.04118410828004)

g = json.load(open("sentinel/masks_geograficas.json"))
POMAR = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)
ctrl = json.load(open("../_VALIDACAO_CAMADAS/SAIDA_C0/controlos.geojson"))

ds = rasterio.open("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
Wo = transform_bounds("EPSG:32629", ds.crs, *W)
w = from_bounds(*Wo, transform=ds.transform)
im = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32") / 255.0
im = np.dstack([im.mean(2) * 0.52 + 0.44] * 3)

fig = plt.figure(figsize=(17.8, 12.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.038, 0.979, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.038, 0.952, "M1 · O que já está fixado, e as cinco coisas que faltam",
         fontsize=20, color=TINTA, fontweight="bold")
fig.text(0.962, 0.957, "M1 v5 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.038, 0.918,
         "As duas coordenadas que nos deu — o armazém e as pontas do B1 — "
         "fecharam questões que estavam em aberto há semanas, e desfizeram uma "
         "colocação nossa que parecia boa. Obrigado. Falta pouco, e a pergunta "
         "nova é a última.", fontsize=9.2, color=TINTA2)

ax = fig.add_axes([0.038, 0.372, 0.925, 0.525])
ax.imshow(im, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)
ax.contour(np.linspace(AOI[0] + 5, AOI[2] - 5, 200),
           np.linspace(AOI[3] - 5, AOI[1] + 5, 100),
           POMAR.astype(float), [0.5], colors=[TINTA], linewidths=2.2)
ax.text(531000, 4655420, "CORPO PRINCIPAL — 30,3 ha de copado medido",
        fontsize=8.6, color=TINTA, ha="center", fontweight="bold", zorder=8,
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=TINTA, lw=1.0,
                  alpha=0.93))

for f in ctrl["features"]:
    if f["properties"].get("id") not in ("C1a", "C1b", "C1c"):
        continue
    cs = f["geometry"]["coordinates"]
    while isinstance(cs[0][0], list):
        cs = cs[0]
    ax.add_patch(Polygon(np.array(cs), closed=True, facecolor=BOM, alpha=0.12,
                         edgecolor=BOM, lw=1.6, zorder=4))
ax.plot([B1I[0], B1F[0]], [B1I[1], B1F[1]], "-o", color=BOM, lw=3.0, ms=10,
        mec="white", mew=1.8, zorder=6)
ax.text((B1I[0] + B1F[0]) / 2 - 40, (B1I[1] + B1F[1]) / 2 - 120,
        "B1 — as suas duas coordenadas\n685 m · válvulas 1 a 5",
        fontsize=8.6, color=BOM, ha="center", va="top", fontweight="bold",
        linespacing=1.4, zorder=8,
        bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=BOM, lw=1.2,
                  alpha=0.94))
ax.plot([ARM[0]], [ARM[1]], "s", color=CRIT, ms=11, mec="white", mew=1.8,
        zorder=7)
ax.text(ARM[0] + 45, ARM[1] - 40, "ARMAZÉM\na sua coordenada", fontsize=8.2,
        color=CRIT, va="top", fontweight="bold", linespacing=1.4, zorder=8,
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=CRIT, lw=1.1,
                  alpha=0.94))
ax.annotate("", xy=(B1F[0], B1F[1]), xytext=(ARM[0], ARM[1]),
            arrowprops=dict(arrowstyle="<->", color=TINTA2, lw=1.2,
                            ls=(0, (5, 3))), zorder=5)
ax.text((ARM[0] + B1F[0]) / 2 + 30, (ARM[1] + B1F[1]) / 2 + 25, "532 m",
        fontsize=7.6, color=TINTA2, fontweight="bold", zorder=6)
ax.plot([W[0] + 90, W[0] + 90 + 300], [W[1] + 70] * 2, color=TINTA, lw=2.6)
ax.text(W[0] + 240, W[1] + 88, "300 m", fontsize=8, color=TINTA, ha="center",
        fontweight="bold")
ax.text(W[2] - 20, W[1] + 20, "ortofoto DGT 2025, 25 cm, esbatida · norte em cima",
        fontsize=6.8, color=TINTA2, ha="right", va="bottom")
ax.text(W[0] + 20, W[1] + 20,
        "Este mapa não traz nenhuma informação sobre o estado das plantas, de "
        "propósito:\nqueremos que a sua leitura da geometria seja independente "
        "da nossa.",
        fontsize=6.8, color=TINTA2, va="bottom", style="italic", linespacing=1.5)

fig.text(0.038, 0.338, "O QUE FICOU FIXADO, E O QUE CAIU", fontsize=8.8,
         color=TINTA, fontweight="bold")
CAIXAS = [
    (BOM, "FIXADO com as suas coordenadas",
     "O B1: 685 m, a 526 m do corpo principal, sobre três parcelas que uma "
     "sessão independente já tinha delimitado sem saber que eram suas. E o "
     "armazém, que é agora o nosso ponto de referência mais firme."),
    (CRIT, "CAIU — e ainda bem",
     "Tínhamos colocado as válvulas contando fileiras a partir das suas "
     "anotações, e parecia bater a 0,3%. O armazém mostrou que estava a 321 m "
     "do sítio. A coincidência vinha de uma suposição nossa, não dos dados."),
    (AVISO, "A REDE — o senhor sabe, nós não conseguimos medir",
     "Tínhamos calculado quanta rede havia comparando ortofotos de anos "
     "diferentes. Não se pode: os voos têm brilhos muito diferentes entre si e "
     "a conta dava mais rede no corpo principal do que no B1, o contrário do "
     "que nos disse. Retirado. Ficamos com a sua informação — rede só no B1, "
     "no tempo do Enza Gold — e com a pergunta 5."),
]
for i, (cor, tit, txt) in enumerate(CAIXAS):
    x = 0.038 + i * 0.3123
    axc = fig.add_axes([x, 0.208, 0.2923, 0.122])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA, lw=0.8))
    axc.add_patch(Rectangle((0, 0.94), 1, 0.06, facecolor=cor, edgecolor="none"))
    axc.text(0.032, 0.860, tit, fontsize=8.4, color=cor, fontweight="bold", va="top")
    axc.text(0.032, 0.690, "\n".join(textwrap.wrap(txt, 58)), fontsize=6.9,
             color=TINTA2, va="top", linespacing=1.6)

fig.text(0.038, 0.174, "AS CINCO COISAS QUE FALTAM", fontsize=8.8, color=TINTA,
         fontweight="bold")
PERG = [
    ("1.", "Onde está a válvula 10? Bastam coordenadas do telemóvel, como fez "
     "para o armazém. Com esse ponto fechamos a colocação de todas as outras."),
    ("2.", "Dentro do B1: onde acaba a válvula 1 e começam as 2 a 5? É a única "
     "fronteira de porta-enxerto do pomar e não a conseguimos ver — as raízes "
     "não aparecem em satélite nenhum."),
    ("3.", "As fileiras do B1 são numeradas à parte das do corpo principal? "
     "As suas anotações dão linhas 149 e 186-187 no B1 e 130 a 423 no corpo, "
     "e os intervalos sobrepõem-se."),
    ("4.", "O viveiro e a B3C3 ficam onde? Uma coordenada de cada, como a do "
     "armazém, resolve."),
    ("5.", "A REDE do B1: em que ano subiu e em que ano saiu? Foi sobre todas "
     "as válvulas 2 a 5, ou só sobre algumas? Precisamos das duas datas porque "
     "a rede altera o que o satélite lê — e sem elas não sabemos se o que "
     "medimos no B1 é a planta ou é a rede a entrar e a sair."),
]
y = 0.166
for n, p in PERG:
    linhas = textwrap.wrap(p, 132)
    fig.text(0.038, y, n, fontsize=7.6, color=TINTA, fontweight="bold",
             va="top")
    fig.text(0.058, y, "\n".join(linhas), fontsize=7.6, va="top",
             color=CRIT if n == "5." else TINTA2,
             fontweight="bold" if n == "5." else "normal", linespacing=1.45)
    y -= 0.0138 * len(linhas) + 0.0068

fig.savefig("figuras/M1_valvulas_v5.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("figuras/M1_valvulas_v5.svg", facecolor=FUNDO, bbox_inches="tight")
print("M1 v5 gravada")
