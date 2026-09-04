"""P10 — o mapa de Braudel: a cota não acompanha o declínio.

A TESE
------
Braudel: os factos não correm todos ao mesmo ritmo. A F8 disse isso no tempo,
em três faixas. **Esta peça diz o mesmo no espaço**, com a *longue durée* — o
terreno — a organizar o desenho.

    foco ORIENTAL    7,84 m
    resto do pomar   6,98 m
    referência       6,80 m
    foco OCIDENTAL   6,64 m
    B1               6,06 m   ← o mais baixo, e o único que SOBE

**A ordenação por cota e a ordenação por desfecho não coincidem em ponto
nenhum.** É uma observação, não um silogismo — e substitui a primeira versão
desta peça, que argumentava «posições opostas ⇒ a causa não vem da posição».
Essa inferência era frágil: um lençol freático ou um agente que se propague por
raiz não precisam de tratar o alto e o baixo de forma diferente.

O QUE ESTA PEÇA JÁ AFIRMOU E ERA FALSO
---------------------------------------
Três vezes, e todas corrigidas por auditoria independente ou por pergunta do
gestor. Fica escrito porque é o que a peça ensina:

1. **«As duas manchas estão nos extremos opostos do terreno.»** Falso: o B1
   está abaixo das duas.
2. **«B1: SEM cota, SEM dreno, SEM declive.»** Falso. Duas folhas MDT cobrem-no
   desde 29-08-2026. O que parava não eram os dados: era o **mosaico recortado**
   à AOI + 300 m, e o `c1_03_dem50.json` declara essa folga em texto.
3. **«445 m a sul do bordo.»** Falso, e é a aresta errada: a folga real é
   **−200 m** — a caixa entra dentro do B1, e 5,5 ha já estavam no array que
   esta peça abria.

E uma quarta, de processo: a correcção de (2) foi anunciada por um `print` cuja
substituição **falhou em silêncio**, e o mapa continuou a dizer «SEM cota»
durante meia hora — enquanto o subtítulo, três centímetros acima, já dizia a
cota. A verificação 7 do `certificar.py` filtrava `startswith("p0")` e **era
cega a esta peça**, a única das onze.

A PRÉ-VOO
---------
**3 · fronteira derivada do sinal?** Não. MDT LiDAR, máscara da C2, parcelário.
**7 · a estatística esconde?** As cotas vão por unidade, e o contraste tem
dp intra-unidade 0,25/0,35 m com zero sobreposição entre distribuições (d de
Cohen 3,93, medido pelo Controlo 3).
**11 · a janela contém o que a frase abrange?** Agora sim — foi preciso alargá-la.

O QUE NÃO ENTRA
---------------
Nenhum valor de declínio no mapa. A peça é sobre a **estrutura**; o
acontecimento entra como rótulo de posição. Quem quer o número vai à P03.
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
sys.path.insert(0, os.path.join(VC, "SAIDA_C2"))
from c2_00_comum import carrega_mascaras, discos_dos_focos    # noqa

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, RISCA = "#fbfbfa", "#e6e3dd"
OCID, ORIE, NEUTRO = "#2a78d6", "#eb6834", "#6b6f76"
SEMDADOS = "#ded9d0"

# ── a estrutura, do certificado da C1. Nenhuma cota recalculada aqui.
TER = json.load(open(os.path.join(VC, "SAIDA_C1", "c1_04_terreno_por_unidade.json"),
                     encoding="utf-8"))
COTA = {"foco ORIENTAL": TER["foco ESTE (disco 90 m)"]["cota"],
        "foco OCIDENTAL": TER["foco OESTE (disco 90 m)"]["cota"],
        "referência": TER["referencia sistematica"]["cota"],
        "resto do pomar": TER["resto do pomar"]["cota"]}
print("cotas certificadas (C1): %s"
      % "  ".join("%s %.2f" % (k, v) for k, v in COTA.items()))

# ── o DEM, e o seu bordo
DEMJ = json.load(open(os.path.join(VC, "SAIDA_C1", "c1_03_dem50.json"),
                      encoding="utf-8"))
t = DEMJ["transform"]
ny, nx = DEMJ["shape"]
x0, y0, px = t[2], t[5], t[0]
tr3763 = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)
cx = [x0, x0 + nx * px, x0, x0 + nx * px]
cy = [y0, y0, y0 - ny * px, y0 - ny * px]
DX, DY = tr3763.transform(cx, cy)
DEM_BB = (min(DX), min(DY), max(DX), max(DY))
print("bordo do DEM em UTM: E %.0f..%.0f  N %.0f..%.0f"
      % (DEM_BB[0], DEM_BB[2], DEM_BB[1], DEM_BB[3]))

# ── as unidades
masc, _ = carrega_mascaras()
POMAR = masc["pomar"]
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
do, de = discos_dos_focos(POMAR)
AOI = (529950, 4654600, 531950, 4655600)
E0, N0, P10M = AOI[0], AOI[3], 10.0
ext = (E0, E0 + POMAR.shape[1] * P10M, N0 - POMAR.shape[0] * P10M, N0)

# ── o B1, pelos polígonos do IFAP
CUL_B1 = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
B1 = []
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL_B1:
        g = sht(lambda x, y, z=None: tr.transform(x, y), shape(f["geometry"])).buffer(0)
        B1.append(np.array(list(g.exterior.coords)))
B1_HA = 12.63
print("B1: %d parcelas · %.2f ha" % (len(B1), B1_HA))

# ══════════════════════════════════════════════════════════════════ a página
fig = plt.figure(figsize=(17.4, 11.0), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.035, 0.962, "A cota não acompanha o declínio",
         fontsize=25, color=TINTA, fontweight="bold", va="top")
fig.text(0.035, 0.918,
         "As duas manchas estão em posições opostas dentro do pomar — e o sector "
         "que NÃO declina está mais baixo do que as duas.",
         fontsize=12.4, color=TINTA2, va="top")

ax = fig.add_axes([0.035, 0.235, 0.62, 0.655])
ax.set_facecolor(FUNDO)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

# janela: pomar + B1 + folga
xs = [E0, E0 + POMAR.shape[1] * P10M] + [c[:, 0].min() for c in B1] + [c[:, 0].max() for c in B1]
ys = [N0 - POMAR.shape[0] * P10M, N0] + [c[:, 1].min() for c in B1] + [c[:, 1].max() for c in B1]
mg = 120
JX = (min(xs) - mg, max(xs) + mg)
JY = (min(ys) - mg, max(ys) + mg)

# 1 · a área SEM DADOS de terreno, identificada e não branca
ax.add_patch(Rectangle((JX[0], JY[0]), JX[1] - JX[0], JY[1] - JY[0],
                       facecolor=SEMDADOS, edgecolor="none", zorder=0))
ax.add_patch(Rectangle((DEM_BB[0], DEM_BB[1]), DEM_BB[2] - DEM_BB[0],
                       DEM_BB[3] - DEM_BB[1], facecolor="#f4f1ea",
                       edgecolor=TINTA3, lw=1.2, ls=(0, (6, 4)), zorder=1))
ax.text(DEM_BB[2] - 30, DEM_BB[1] + 26,
        "bordo do MOSAICO recortado — os dados do B1 estão em disco desde 29-08",
        fontsize=8.8, color=TINTA3, ha="right", zorder=6)

# 2 · a AOI — uma DECISÃO, não um dado
ax.add_patch(Rectangle((AOI[0], AOI[1]), AOI[2] - AOI[0], AOI[3] - AOI[1],
                       facecolor="none", edgecolor="#b08a5a", lw=1.4,
                       ls=(0, (2, 3)), zorder=2))
ax.text(AOI[0] + 20, AOI[3] - 34,
        "AOI de 2 × 1 km — uma DECISÃO, não uma fronteira do terreno",
        fontsize=8.8, color="#8a6d1f", zorder=6)

# 3 · o pomar e as duas manchas
ax.contour(POMAR.astype(float), levels=[0.5], colors=[TINTA3], linewidths=1.5,
           extent=ext, origin="upper", zorder=3)
for m, cor in ((do & POMAR & COM, OCID), (de & POMAR & COM, ORIE)):
    ax.contourf(m.astype(float), levels=[0.5, 1.5], colors=[cor], alpha=0.92,
                extent=ext, origin="upper", zorder=4)

# 4 · o B1
for c in B1:
    ax.fill(c[:, 0], c[:, 1], facecolor=NEUTRO, alpha=0.30, zorder=3)
    ax.plot(c[:, 0], c[:, 1], color=NEUTRO, lw=1.1, zorder=4)

ax.set_xlim(*JX); ax.set_ylim(*JY); ax.set_aspect("equal")

# rótulos com a COTA — a camada de baixo a nomear as unidades
ax.annotate("OCIDENTAL\n%.2f m  ·  o ponto BAIXO" % COTA["foco OCIDENTAL"],
            xy=(530486, 4655052), xytext=(JX[0] + 60, JY[1] - 200),
            fontsize=10.6, color=OCID, fontweight="bold", va="top",
            linespacing=1.45,
            arrowprops=dict(arrowstyle="-", color=OCID, lw=1.1))
ax.annotate("ORIENTAL\n%.2f m  ·  o ponto ALTO" % COTA["foco ORIENTAL"],
            xy=(530969, 4655126), xytext=(JX[1] - 60, JY[1] - 200),
            fontsize=10.6, color=ORIE, fontweight="bold", ha="right", va="top",
            linespacing=1.45,
            arrowprops=dict(arrowstyle="-", color=ORIE, lw=1.1))
ax.annotate("B1  ·  12,6 ha do mesmo dono\n6,06 m — 0,58 m ABAIXO dos dois focos",
            xy=(529800, 4654240), xytext=(530330, 4654060),
            fontsize=10.0, color=TINTA, fontweight="bold", va="top",
            linespacing=1.45,
            arrowprops=dict(arrowstyle="-", color=NEUTRO, lw=1.1))
ax.plot([JX[1] - 80 - 300, JX[1] - 80], [JY[0] + 60, JY[0] + 60], lw=2.4,
        color=TINTA, zorder=7)
ax.text(JX[1] - 80 - 150, JY[0] + 72, "300 m", fontsize=8.8, color=TINTA2,
        ha="center", va="bottom", zorder=7)

# ═══════════════════════════════════════════ os três registos, à direita
axr = fig.add_axes([0.685, 0.235, 0.285, 0.655]); axr.axis("off")
axr.set_xlim(0, 1); axr.set_ylim(0, 1)
REG = [
 ("ESTRUTURA", "#2f6b52", "não tem data",
  "O terraço, a cota, o dreno. O pomar é **duas vezes mais plano** que o "
  "terreno à mesma cota (0,036 m contra 0,070, p = 3e-10).\n\n"
  "As duas manchas estão a **1,20 m** uma da outra em cota — nos extremos "
  "opostos.\n\n"
  "**A estrutura não explica o acontecimento.** Duas unidades em posições "
  "opostas não podem partilhar uma causa que venha da posição."),
 ("CONJUNTURA", "#8a6d1f", "décadas",
  "A pérgola aparece entre **2007 e 2010**, no pomar todo ao mesmo tempo.\n\n"
  "O **B1** planta-se depois, e ainda estava a encher em 2026.\n\n"
  "A rede cresce para **27 válvulas**; a partição que a testou usou **doze** — "
  "**60,8 %** da exploração."),
 ("ACONTECIMENTO", "#eb6834", "dois anos",
  "**Dois passos, não um:** −0,050 em Agosto de 2025 e −0,13 a −0,23 em Julho "
  "de 2026.\n\n"
  "Nas duas manchas **ao mesmo tempo e na mesma medida** — apesar de 1,20 m "
  "de cota e 496 m de distância entre elas.\n\n"
  "*É a faixa com intervalo de confiança, e a que mais mudou de leitura.*"),
]
y = 0.985
for tit, cor, ritmo, txt in REG:
    axr.plot([0, 1], [y + 0.012, y + 0.012], lw=2.0, color=cor)
    axr.text(0, y - 0.012, tit, fontsize=12.4, color=cor, fontweight="bold",
             va="top")
    axr.text(1, y - 0.014, ritmo, fontsize=9.4, color=TINTA3, va="top",
             ha="right")
    axr.text(0, y - 0.062, txt.replace("**", ""), fontsize=9.4, color=TINTA2,
             va="top", linespacing=1.55, wrap=True)
    y -= 0.335

fig.text(0.035, 0.155,
         "A ordem das cotas reproduz-se num sensor sem relação com o LiDAR "
         "(GLO-30), e o degrau de costura entre as duas campanhas de voo é de "
         "0,058 m contra os 1,204 m do contraste — a diferença não é artefacto "
         "de voo. Camada 1, S3.",
         fontsize=9.0, color=TINTA2)
fig.text(0.035, 0.108,
         "O QUE ESTE MAPA NÃO DIZ:",
         fontsize=9.6, color=TINTA, fontweight="bold")
fig.text(0.035, 0.078,
         "que a estrutura seja irrelevante — condiciona, e o foco oriental tem "
         "28 % de área sem pérgola que a cota ajuda a explicar;  ·  que o B1 "
         "esteja são — está a encher, que é outra coisa;  ·  nada sobre a causa: "
         "nenhuma camada deste mapa vê abaixo da superfície.",
         fontsize=9.0, color=TINTA2, linespacing=1.6)
fig.text(0.035, 0.026,
         "Terreno: MDT LiDAR 50 cm, voo de 06-07-2025 · cotas do certificado da "
         "Camada 1, não recalculadas · contornos: máscara da C2 e parcelário do "
         "IFAP · B1 localizado por duas coordenadas do gestor, 28-08-2026.",
         fontsize=8.4, color=TINTA3)

fig.savefig(os.path.join(AQUI, "P10_braudel_mapa.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
fig.savefig(os.path.join(AQUI, "P10_braudel_mapa.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
print("escrito P10 — o mapa de Braudel")
