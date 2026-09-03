# -*- coding: utf-8 -*-
"""C0-15. Tarefa 7 — M1 e M2 refeitas.

M1  Valvulas e sectores, para confirmacao pela gestora. ZERO informacao de
    declinio. Novidade em relacao a M1 anterior: o esquema de rega e colocado
    por ajuste de forma medido (escala 0,829 m/px, rotacao +33,05 graus), nao
    por duas indicacoes verbais; as fronteiras de sector deixam de ser linhas
    N-S inventadas e passam a ser as proprias faixas do esquema, que sao
    perpendiculares ao eixo real da parcela; o porta-enxerto NAO e desenhado
    dentro da parcela, porque as valvulas 2-5 caem fora dela.

M2  Declinio. A classe cinzenta «nunca esteve sao / falha de copado» e
    substituida por «ja em defice na primeira cena (2017) — inicio nao
    datavel», que e o que os dados dizem.

Ambas em SAIDA_C0. Nao se toca nos originais de ganfei_s2/figuras/.
"""
import json
import os
import textwrap
import numpy as np
import fitz
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle
from matplotlib.colors import ListedColormap, BoundaryNorm

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
W = (530050, 4654800, 531650, 4655550)
TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM = "#d03b3b", "#fab219", "#0a7a0a"
AZUL, ROXO = "#2a78d6", "#7a4fbf"

masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
G = json.load(open(os.path.join(OUT, "c0_13_georref.json")))
EIXO = json.load(open(os.path.join(OUT, "c0_11_eixo.json")))
esc = G["escala_m_por_px300"]
th = np.radians(G["rotacao_graus"])
Sc = np.array(G["origem_px"])
Tc = np.array(G["origem_utm"])
Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
Rinv = np.linalg.inv(Rm)


def pol_utm(k):
    p = np.array(masks[k], float)
    return np.column_stack([AOI[0] + p[:, 0] * 10.0, AOI[3] - p[:, 1] * 10.0])


POM = pol_utm("pomar")

# ------------------------------------------------------------ base: ortofoto
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
with rasterio.open(ORTO) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *W, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    arr = ds.read([1, 2, 3], window=win,
                  out_shape=(3, int(win.height / 2), int(win.width / 2)),
                  boundless=True, fill_value=0).astype("float32")
RGB = np.clip(np.moveaxis(arr, 0, -1) / max(np.percentile(arr, 99.5), 1), 0, 1)
RGB = 0.45 + 0.55 * RGB                      # clarear, para as capas lerem bem

# ------------------------------------------- esquema de rega reprojectado
doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
DES = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3].astype("float32") / 255.0
DH, DW = DES.shape[:2]
NX, NY = 1600, 750
gx = np.linspace(W[0], W[2], NX)
gy = np.linspace(W[3], W[1], NY)
GX, GY = np.meshgrid(gx, gy)
P = np.column_stack([GX.ravel() - Tc[0], GY.ravel() - Tc[1]])
Q = (P @ Rinv.T) / esc + Sc                  # -> (px_x, -px_y)
qx = np.rint(Q[:, 0]).astype(int)
qy = np.rint(-Q[:, 1]).astype(int)
ok = (qx >= 0) & (qx < DW) & (qy >= 0) & (qy < DH)
ESQ = np.ones((NY * NX, 3), "float32")
ESQ[ok] = DES[qy[ok], qx[ok]]
ESQ = ESQ.reshape(NY, NX, 3)
# alfa: SO o desenho CAD — limite do terreno (rosa), faixas de sector (pastel)
# e os aneis das valvulas (vermelho escuro). As anotacoes a mao (tinta azul,
# laranja, vermelho vivo) e o texto impresso ficam de fora: sujam o mapa.
r, g, b = ESQ[:, :, 0], ESQ[:, :, 1], ESQ[:, :, 2]
mx = ESQ.max(2)
mn = ESQ.min(2)
sat = mx - mn
rosa_o = ((r > 0.55) & (r - g > 0.12) & (r - b > 0.02) & (r - b < 0.34)
          & (g > 0.30))
pastel = (mn > 0.60) & (sat > 0.045) & (sat < 0.30)
anel = ((r > 0.35) & (r < 0.86) & (r - g > 0.16) & (r - b > 0.12)
        & (r - b < 0.42) & (g < 0.60))
ALFA = np.where(rosa_o | pastel | anel, 0.80, 0.0)
ALFA = ndimage.median_filter(ALFA, 3)
# corredor: so ate 220 m do poligono medido — fora disso o desenho nada diz
_seg0, _seg1 = POM[:-1], POM[1:]
_d = _seg1 - _seg0
_L2 = (_d * _d).sum(1)
_pt = np.column_stack([GX.ravel(), GY.ravel()])
_t = np.clip(((_pt[:, None, :] - _seg0[None]) * _d[None]).sum(2) / _L2[None],
             0, 1)
_pr = _seg0[None] + _t[:, :, None] * _d[None]
_dist = np.sqrt(((_pt[:, None, :] - _pr) ** 2).sum(2)).min(1).reshape(NY, NX)
ALFA = np.where(_dist < 220, ALFA, 0.0)

# valvulas georreferenciadas
VAL = np.array(G["valvulas_utm"])
VPX = np.array(G["valvulas_px"])
dentro = np.array([MP(POM).contains_point(p) for p in VAL])

# eixo e perpendicular da parcela
cen = np.array(EIXO["centroide"])
u = np.array(EIXO["eixo"])
v = np.array(EIXO["transversal"])

# =========================================================== M1 =============
fig = plt.figure(figsize=(17.6, 12.2), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.040, 0.978, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.040, 0.951, "M1 · Válvulas e sectores — para confirmação  (versão 2)",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.960, 0.956, "M1 v2 · camada C0 · 28-08-2026", fontsize=8,
         color=TINTA3, ha="right")
fig.text(0.040, 0.893,
         "Esta versão corrige dois erros da anterior. (1) O esquema de rega "
         "está agora colocado por medição — a escala e a rotação saem do "
         "ajuste da forma do\nterreno desenhado à parcela medida no satélite, "
         "e não de indicações verbais. (2) As fronteiras de sector já não são "
         "linhas norte-sul: são as próprias\nfaixas do seu esquema, que são "
         "perpendiculares ao eixo da parcela (o eixo corre a 70° de azimute, "
         "WSW–ENE). Continua a não haver aqui nenhuma\ninformação sobre "
         "estado sanitário: nem cores, nem marcas, nem texto.",
         fontsize=8.6, color=TINTA2, linespacing=1.5)

ax = fig.add_axes([0.040, 0.352, 0.920, 0.500])
ax.imshow(RGB, extent=[W[0], W[2], W[1], W[3]])
ax.imshow(ESQ, extent=[W[0], W[2], W[1], W[3]], alpha=ALFA, zorder=3)
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)
ax.add_patch(MPoly(POM, closed=True, facecolor="none", edgecolor="white",
                   lw=3.4, zorder=4))
ax.add_patch(MPoly(POM, closed=True, facecolor="none", edgecolor=TINTA,
                   lw=1.6, zorder=5))
for p, d in zip(VAL, dentro):
    if not d:
        continue
    ax.add_patch(Circle(p, 75, facecolor="none", edgecolor="white", lw=2.2,
                        zorder=6, alpha=0.85))
    ax.add_patch(Circle(p, 75, facecolor="none", edgecolor="#0d5fc4", lw=1.0,
                        ls=(0, (3, 3)), zorder=7))
    ax.plot([p[0]], [p[1]], "o", ms=7, color="#0d5fc4", mec="white", mew=1.4,
            zorder=8)
# eixo medido
for sgn, cor in ((1, "#0d5fc4"),):
    a = cen + u * EIXO["t_min"]
    b = cen + u * EIXO["t_max"]
    ax.plot([a[0], b[0]], [a[1], b[1]], color="white", lw=3.0, zorder=6)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=TINTA, lw=1.1, ls=(0, (7, 4)),
            zorder=7)
ax.text(cen[0], cen[1] + 120, "eixo medido da parcela — azimute 70°",
        fontsize=7.6, color=TINTA, ha="center", zorder=9,
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=TINTA3, lw=0.8,
                  alpha=0.92))
# escala
ax.plot([W[0] + 60, W[0] + 260], [W[1] + 50, W[1] + 50], color="white", lw=5)
ax.plot([W[0] + 60, W[0] + 260], [W[1] + 50, W[1] + 50], color=TINTA, lw=2)
ax.text(W[0] + 160, W[1] + 66, "200 m", fontsize=7.5, color=TINTA,
        ha="center", fontweight="bold")
ax.text(W[2] - 20, W[1] + 20, "ortofoto DGT 2025, 25 cm · norte em cima · "
        "esquema de rega sobreposto por ajuste medido", fontsize=6.8,
        color=TINTA, ha="right", va="bottom")

fig.text(0.040, 0.330, "O QUE ESTE MAPA AFIRMA, E COM QUE CONFIANÇA",
         fontsize=8.8, color=TINTA, fontweight="bold")
CAIXAS = [
    (BOM, "MEDIDO — ±10 m",
     "O contorno preto é o copado de 2026 medido no satélite: 29,0 ha. O eixo "
     "da parcela (70° de azimute, 1445 m por 328 m) é medido no mesmo "
     "polígono. Não vem do esquema."),
    (AVISO, "COLOCADO POR AJUSTE — ±60 a 100 m",
     "O esquema por cima é o seu desenho, à escala que ele próprio declara "
     "(1/3500 @ A1), rodado 33° para assentar na parcela. O comprimento do "
     "troço desenhado bate com a parcela medida com 2 % de erro. Cada válvula "
     "tem um círculo tracejado com o raio da incerteza."),
    (CRIT, "NÃO DESENHADO",
     "As válvulas 1–5 (o «B1» do seu esquema, anotado 1,77 ha) NÃO caem nesta "
     "parcela: caem cerca de 1 km a sudoeste. Por isso não há aqui nenhuma "
     "área de porta-enxerto Summer Kiwi — se ela existe nesta parcela, o "
     "esquema não a mostra."),
]
for i, (cor, tit, txt) in enumerate(CAIXAS):
    x = 0.040 + i * 0.3135
    axc = fig.add_axes([x, 0.196, 0.2935, 0.126])
    axc.set_xlim(0, 1); axc.set_ylim(0, 1); axc.set_axis_off()
    axc.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axc.add_patch(Rectangle((0, 0.94), 1, 0.06, facecolor=cor,
                            edgecolor="none"))
    axc.text(0.030, 0.870, tit, fontsize=8.4, color=cor, fontweight="bold",
             va="top")
    axc.text(0.030, 0.720, "\n".join(textwrap.wrap(txt, 58)), fontsize=6.8,
             color=TINTA2, va="top", linespacing=1.58)

fig.text(0.040, 0.168, "O QUE PRECISAMOS QUE CONFIRME OU CORRIJA",
         fontsize=8.8, color=TINTA, fontweight="bold")
PERG = [
    "1.  O esquema está assente no sítio certo? Repare no contorno do terreno "
    "desenhado: passa onde deve passar, ou está desviado — e para que lado?",
    "2.  As válvulas estão nos sítios certos? O seu esquema mostra duas filas, "
    "uma a norte e outra a sul da conduta. Confirma que é assim no terreno?",
    "3.  As válvulas 1 a 5 ficam mesmo num bloco separado, a sudoeste, junto "
    "ao rio? Se sim, esse bloco entra ou não neste estudo?",
    "4.  Onde estão exactamente as videiras com raiz de Summer Kiwi? Marque-as "
    "por cima desta imagem: não as desenhámos porque não sabemos.",
    "5.  As restantes válvulas do projecto (até à 27), o viveiro e a B3C3: "
    "estão dentro desta imagem, ou fora? Se fora, para que lado e a que "
    "distância?",
    "6.  A conduta principal corre onde o esquema a põe, e a água entra pelo "
    "lado oeste?",
]
for i, p in enumerate(PERG):
    fig.text(0.040, 0.142 - i * 0.0205, p, fontsize=7.7, color=TINTA2)

fig.text(0.040, 0.008,
         "NOTA DE MÉTODO: a versão anterior desta figura colocava as válvulas "
         "a partir de duas indicações verbais, e daí saía uma escala 30 % "
         "maior do que a que o próprio esquema declara. Foi esse erro de "
         "escala que, levado ao extremo oeste do desenho, gerou uma área de "
         "estudo do outro lado do rio Minho, agora retirada.",
         fontsize=7.4, color=CRIT, fontweight="bold")
fig.savefig(os.path.join(OUT, "M1_valvulas_v2.png"), facecolor=FUNDO,
            bbox_inches="tight")
fig.savefig(os.path.join(OUT, "M1_valvulas_v2.svg"), facecolor=FUNDO,
            bbox_inches="tight")
plt.close(fig)
print("M1 v2 gravada — sem qualquer informacao de declinio")

# =========================================================== M2 =============
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
    with rasterio.open(os.path.join(BASE, "sentinel", d + ".tif")) as ds:
        nd = ds.read(1)
    defs.append((nd < float(np.nanmean(nd[sau])) - 0.05) & pomar)
D = np.stack(defs)
incid = D.sum(0) / len(DATAS)
inicio = np.zeros(D.shape[1:], int)
for i in range(len(DATAS) - 1):
    inicio[(inicio == 0) & D[i] & D[i + 1]] = ANOS[i]
sao_antes = np.zeros(D.shape[1:], bool)
for i in range(1, len(DATAS) - 1):
    sao_antes |= (inicio == ANOS[i]) & ~D[0] & ((~D[:i]).mean(0) >= 0.5)
ja_2017 = (inicio > 0) & ~sao_antes
inicio_decl = np.where(sao_antes, inicio, 0)
print("M2: ja em defice na 1a cena = %.2f ha ; declinou depois = %.2f ha"
      % (ja_2017.sum() / 100.0, sao_antes.sum() / 100.0))

fig = plt.figure(figsize=(17.6, 12.6), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.040, 0.978, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.040, 0.952, "M2 · Onde e desde quando — USO INTERNO  (versão 2)",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.960, 0.957, "M2 v2 · camada C0 · 28-08-2026", fontsize=8,
         color=TINTA3, ha="right")
fig.text(0.040, 0.924,
         "Não enviar à gestora antes de a M1 voltar confirmada. Correcção "
         "desta versão: a classe cinzenta que dizia «nunca esteve são — falha "
         "de copado» estava errada. A ortofoto de 2025 a 25 cm mostra linhas "
         "de pomar contínuas em toda essa área.",
         fontsize=8.8, color=CRIT, fontweight="bold")

ax = fig.add_axes([0.040, 0.400, 0.660, 0.500])
ax.imshow(RGB, extent=[W[0], W[2], W[1], W[3]])
ax.set_xlim(W[0], W[2]); ax.set_ylim(W[1], W[3])
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(TINTA3); s.set_linewidth(0.8)
ESCADA = [2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
CORES = ["#4a1010", "#7d1a1a", "#a82626", "#c8442f", "#e06a3c", "#ee9159",
         "#f7b785", "#fbd9b8"]
ax.imshow(np.where(inicio_decl > 0, inicio_decl, np.nan),
          cmap=ListedColormap(CORES), norm=BoundaryNorm(ESCADA + [2026],
                                                        len(CORES)),
          extent=[AOI[0], AOI[2], AOI[1], AOI[3]], interpolation="nearest",
          alpha=0.92, zorder=4)
ax.imshow(np.where(ja_2017, 1, np.nan), cmap=ListedColormap(["#3b2a6b"]),
          extent=[AOI[0], AOI[2], AOI[1], AOI[3]], interpolation="nearest",
          alpha=0.82, zorder=3)
ax.add_patch(MPoly(POM, closed=True, facecolor="none", edgecolor="white",
                   lw=2.6, zorder=5))
ax.text(W[0] + 20, W[3] - 24, "sem fronteiras de sector: a colocação do "
        "esquema tem ±60–100 m e não as sustenta", fontsize=6.6, color="white",
        va="top", zorder=8)

axl = fig.add_axes([0.040, 0.340, 0.660, 0.032])
axl.set_xlim(0, len(CORES) + 6.4); axl.set_ylim(0, 1); axl.set_axis_off()
for i, (an, c) in enumerate(zip(ESCADA, CORES)):
    axl.add_patch(Rectangle((i, 0.42), 1, 0.58, facecolor=c, edgecolor="none"))
    axl.text(i + 0.5, 0.24, str(an), fontsize=7.4, color=TINTA2, ha="center")
axl.add_patch(Rectangle((len(CORES) + 0.35, 0.42), 0.9, 0.58,
                        facecolor="#3b2a6b", edgecolor="none"))
axl.text(len(CORES) + 1.45, 0.72,
         "já em défice na primeira cena (2017) —\ninício NÃO datável: "
         "%.2f ha" % (ja_2017.sum() / 100.0),
         fontsize=6.6, color=TINTA2, va="center", linespacing=1.4)
axl.text(0, 1.22, "ANO DA PRIMEIRA MANIFESTAÇÃO — dois anos consecutivos em "
         "défice; um ano isolado não conta", fontsize=7.6, color=TINTA,
         fontweight="bold", va="bottom")

axr = fig.add_axes([0.722, 0.340, 0.238, 0.560])
axr.set_xlim(0, 1); axr.set_ylim(0, 1); axr.set_axis_off()
axr.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                        lw=0.8))
axr.text(0.05, 0.972, "O QUE MUDA NESTA VERSÃO", fontsize=8.4, color=TINTA,
         fontweight="bold", va="top")
TX = [("A classe roxa não é falha de copado.",
       "São %.2f ha que já estavam abaixo da referência na primeira cena da "
       "série. A ortofoto de 2025 mostra linhas de pomar contínuas nessa área. "
       "Não são caminhos nem falhas." % (ja_2017.sum() / 100.0)),
      ("O início não é datável por satélite.",
       "Se aquilo já estava em défice em 2017, começou antes de 2017 — e a "
       "série começa em 2017. A cronologia que esta figura mostra é a das "
       "manifestações posteriores, não a do começo."),
      ("Não é artefacto da data escolhida.",
       "Repetiu-se o cálculo com as outras quatro cenas limpas de 2017 "
       "(12-07, 11-08, 18-08, 31-08): a área dá 7,65 a 8,21 ha. A conclusão "
       "não depende de se ter escolhido 02-07."),
      ("A referência não está a descer.",
       "Declive da referência sã nas 9 cenas de plena estação: +0,0038 "
       "NDVI/ano, p = 0,13. Não é significativo. O défice não está a ser "
       "subestimado por essa via."),
      ("Mas a referência é circular.",
       "As três manchas «sãs» foram escolhidas por terem NDVI > 0,78 na cena "
       "de 2026 — a última. Isso enviesa a referência para cima no fim da "
       "série. É uma limitação estrutural, não um erro de cálculo.")]
y = 0.915
for tit, txt in TX:
    axr.text(0.05, y, tit, fontsize=7.4, color=TINTA, fontweight="bold",
             va="top")
    axr.text(0.05, y - 0.028, "\n".join(textwrap.wrap(txt, 46)), fontsize=6.4,
             color=TINTA2, va="top", linespacing=1.55)
    y -= 0.030 + 0.0152 * (len(textwrap.wrap(txt, 44)) + 1.0)

fig.text(0.040, 0.300, "RESSALVAS QUE SE MANTÊM", fontsize=8.8, color=TINTA,
         fontweight="bold")
RES = [
    "A máscara `pomar` foi ela própria construída a partir do NDVI de 2026 "
    "(limiar 0,78). Copado que já tivesse descido abaixo desse limiar em 2026 "
    "e não fosse recuperado pelo fecho morfológico está FORA da máscara — ou "
    "seja, fora desta figura.",
    "A «Mancha W» foi definida como NDVI < 0,76 em 2026 e depois dilatada. "
    "Medir a série dela é, em parte, circular. A «Zona 0» é um polígono "
    "geográfico e não tem esse problema.",
    "2019-09-02 e 2025-06-17 ficaram de fora por fenologia, mas 2018-08-31 "
    "(dia 243) ficou dentro e 2019-09-02 (dia 245) ficou fora: a regra de "
    "fenologia não é consistente e deve ser reescrita.",
    "A 10 m, um núcleo de 4 píxeis é 0,04 ha e a fronteira tem ±1 píxel: as "
    "áreas têm sentido, as formas exactas não.",
    "Nenhum destes núcleos foi visitado no terreno. São défice de NDVI, não "
    "diagnóstico.",
]
yy2 = 0.276
for t in RES:
    linhas = textwrap.wrap(t, 148)
    for L in linhas:
        fig.text(0.040, yy2, L, fontsize=7.6, color=TINTA2)
        yy2 -= 0.0175
    yy2 -= 0.008
fig.savefig(os.path.join(OUT, "M2_declinio_v2.png"), facecolor=FUNDO,
            bbox_inches="tight")
fig.savefig(os.path.join(OUT, "M2_declinio_v2.svg"), facecolor=FUNDO,
            bbox_inches="tight")
plt.close(fig)
print("M2 v2 gravada")
