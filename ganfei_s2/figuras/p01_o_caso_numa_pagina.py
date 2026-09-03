# -*- coding: utf-8 -*-
"""P01 — o caso numa página. A única peça que se lê de certeza.

O TEXTO VEM DA ADENDA v1.4 §3, E QUATRO AFIRMAÇÕES DELE FORAM CORRIGIDAS
--------------------------------------------------------------------------
A v1.4 escreveu a P01 pronta a compor. Entre essa data e hoje este processo
retirou **dezanove** veredictos, e a pré-voo do `ANTES_DE_COMECAR.md` obriga a
confrontar cada número com o registo antes de o desenhar. Quatro não passaram:

1. **«0 análises de doença alguma vez feitas nas zonas afectadas»** — falso.
   O **D2** certifica quatro unidades colocadas, todas positivas a *M. hapla*.
   O zero verdadeiro, e que não precisa de ressalva nenhuma, é outro e está no
   **D5**: **nenhuma das doze amostras com posição é anterior ao acontecimento.**

2. **«nenhuma foi colhida nas zonas doentes com o sítio registado»** — falso
   pela mesma razão. O que é verdade é o **D3**: do lado oriental existe uma só
   amostra, e é um composto sobre 9,92 ha dos quais 28,1 % nem sequer têm
   plantas.

3. **«sete estão fechadas (…) três continuam abertas»** — a P06 corrida hoje dá
   **sete fechadas, uma confundida e duas abertas**. A terceira era «é regional,
   e não desta exploração», e fechou a 01-09.

4. **«a causa mais provável é a única que nunca foi procurada»** — já não é «a
   única». A PSA passou de lacuna a **exclusão clínica** por testemunho de tipo
   1 (`C4_ADENDA_RAZAO_2026-09-03.md`): a decisão existe, o registo dela é que
   não. Fica **uma** hipótese por procurar, e é o patogénio de solo.

E dois números que a v1.4 deixou por fixar, agora tomados do certificado e não
recalculados: a distância entre os dois focos é **496 m** (`c4_01_numeros.json`,
não os 488 m que a minha máscara dá — condição 4 do portão, reproduz-se o
certificado), e a área é a do **kiwi declarado ao IFAP pela exploração**,
44,4 ha, dos quais o bloco que contém as duas zonas tem 30,3 ha.

O QUE NÃO ENTRA, E É A REGRA DA PRÓPRIA PEÇA
---------------------------------------------
«Qualquer número que precise de uma ressalva para ser lido — se precisa de
ressalva, é das outras treze peças.» Por isso **não entra aqui** o resultado da
REG-01 («as duas zonas são as duas piores de toda a região»), apesar de ser o
achado mais forte do caso: ele vem com P(ordenação errada) de 0,07 a 0,25 e cai
se se retirar 2026. Vai na P04, com o intervalo ao lado.

Zero siglas. Sem valores de p. Sem nomes de organismos. Sem a palavra hipótese.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import sys
VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
sys.path.insert(0, os.path.join(VC, "SAIDA_C2"))
from c2_00_comum import carrega_mascaras, discos_dos_focos   # noqa

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, RISCA = "#fbfbfa", "#e6e3dd"
OCID, ORIE, NEUTRO = "#2a78d6", "#eb6834", "#6b6f76"

# ── os números, do certificado — nenhum recalculado aqui
NUM = json.load(open(os.path.join(VC, "SAIDA_C4", "c4_01_numeros.json"),
                     encoding="utf-8"))
D_FOCOS = NUM["foco_OESTE_ao_foco_ESTE_m"]

masc, _ = carrega_mascaras()
POMAR = masc["pomar"]
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
do, de = discos_dos_focos(POMAR)
AOI = (529950, 4654600, 531950, 4655600)
HA_BLOCO = POMAR.sum() / 100.0
print("distancia certificada entre focos: %.0f m" % D_FOCOS)
print("bloco com as duas zonas: %.1f ha" % HA_BLOCO)

# ══════════════════════════════════════════════════════════════ a página
fig = plt.figure(figsize=(16.6, 13.6), dpi=200)
fig.patch.set_facecolor(FUNDO)

fig.text(0.040, 0.958,
         "Um pomar de kiwi perdeu um oitavo do seu vigor em duas estações,",
         fontsize=25, color=TINTA, fontweight="bold", va="top")
fig.text(0.040, 0.906,
         "em duas zonas separadas — e a explicação mais provável é a que "
         "ninguém foi procurar",
         fontsize=25, color=TINTA, fontweight="bold", va="top")
fig.plot = None

# ── os três números
ax = fig.add_axes([0.040, 0.700, 0.560, 0.135]); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
HER = [("−0,12", ORIE,
        "o que perderam as plantas" + chr(10) + "vivas das duas zonas"
        + chr(10) + "doentes, de 2024 a 2026"),
       ("−0,01", NEUTRO,
        "o que perderam as plantas" + chr(10) + "de todo o resto do mesmo"
        + chr(10) + "pomar, no mesmo período"),
       ("0", "#8c1c13",
        "análises colhidas ANTES de" + chr(10) + "as plantas adoecerem."
        + chr(10) + "As doze são posteriores")]
for i, (v, cor, leg) in enumerate(HER):
    x = i * 0.340
    ax.text(x, 1.02, v, fontsize=40, color=cor, fontweight="bold", va="top")
    ax.text(x, 0.34, leg, fontsize=9.4, color=TINTA2, va="top", linespacing=1.48)
    if i:
        ax.plot([x - 0.028, x - 0.028], [0.02, 1.00], lw=1.0, color=RISCA)

# ── o corpo
CORPO = [
 ("O que se passou.",
  "Um pomar de kiwi em Valença, com cerca de 44 hectares declarados, tem duas "
  "zonas doentes. Não estão\nligadas: ficam a meio quilómetro uma da outra, com "
  "pomar são pelo meio. Entre 2024 e 2026 as plantas\ndessas duas zonas perderam "
  "cerca de um oitavo do seu vigor, e perderam-no ao mesmo tempo e na mesma\n"
  "medida. As plantas de todo o resto do pomar não perderam praticamente nada."),
 ("Como sabemos.",
  "Nove verões de imagens de dois satélites diferentes, um levantamento laser do "
  "terreno, um radar que\natravessa nuvens, registos de chuva e de temperatura, e "
  "o cadastro agrícola oficial. Cinco maneiras de\nolhar, independentes umas das "
  "outras. Dizem todas a mesma coisa, e uma delas usa limites de parcela\n"
  "desenhados por outra entidade, para pagamentos, que não sabe nada disto."),
 ("O que já não pode ser.",
  "Foram levantadas dez explicações e sete estão fechadas, cada uma por uma "
  "medição feita de propósito:\nnão foi seca — os dois meses foram os mais húmidos "
  "da década —, não foi encharcamento, não foi um mau\nano da região, não foi a "
  "rega, não foi a poda, não foi o tipo de planta, e não é um problema de toda a\n"
  "zona. Nenhuma delas sobrevive aos números."),
 ("O que falta.",
  "Duas explicações continuam abertas. Uma delas nunca foi procurada, e é a mais "
  "provável: uma doença do\nsolo. O obstáculo é simples de dizer — de todas as "
  "análises feitas neste pomar, **nenhuma foi colhida\nantes de as plantas "
  "adoecerem**, e do lado oriental existe uma só, misturada sobre dez hectares "
  "dos\nquais um quarto nem plantas tem. Sabe-se que há organismos no pomar; não "
  "se sabe se estão onde as\nplantas estão a morrer, e é isso que decide o que se "
  "faz a seguir."),
 ("O que se propõe.",
  "Uma colheita em Setembro: doze plantas, quarenta e oito amostras, um "
  "laboratório, uma deslocação.\nEstá escrito, antes de existir, o que cada "
  "resultado permite concluir — e também o que nos faria\nconcluir que estamos "
  "errados."),
]
# A geometria e derivada, nao adivinhada. A primeira versao usava 0,0345 por
# linha e os titulos entravam pelo paragrafo anterior: a altura real de uma
# linha e fonte x linespacing em pontos, dividida pela altura do eixo em pontos.
CORPO_H, F_TXT, F_TIT, LSP = 0.560, 10.2, 11.6, 1.60
alt_pt = CORPO_H * 13.6 * 72.0
LINHA = F_TXT * LSP / alt_pt
TITULO = F_TIT * 1.7 / alt_pt
GAP = 0.6 * LINHA
ax2 = fig.add_axes([0.040, 0.108, 0.560, CORPO_H]); ax2.axis("off")
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
print("altura de linha derivada: %.4f do eixo (%d pt)" % (LINHA, alt_pt))
y = 0.995
for tit, txt in CORPO:
    ax2.text(0.0, y, tit, fontsize=F_TIT, color=TINTA, fontweight="bold",
             va="top")
    ax2.text(0.0, y - TITULO, txt.replace("**", ""), fontsize=F_TXT,
             color=TINTA2, va="top", linespacing=LSP)
    y -= TITULO + (txt.count(chr(10)) + 1) * LINHA + GAP
if y < -0.01:
    raise SystemExit("o corpo transborda o eixo em %.3f — encurtar o texto" % -y)

# ── o mapa: contorno, duas zonas, escala, norte. Mais nada.
axm = fig.add_axes([0.640, 0.330, 0.340, 0.560])
axm.set_facecolor(FUNDO)
for s in axm.spines.values():
    s.set_visible(False)
axm.set_xticks([]); axm.set_yticks([])

# ═══════════════════════════════════════════════════════════════════════════
# O MAPA PASSOU A SER EM COORDENADAS, E A RAZAO E O B1
# ═══════════════════════════════════════════════════════════════════════════
# A primeira versao desenhava em celulas da mascara, e por isso **so podia
# mostrar o que a AOI contem**. O B1 — o sector a sudoeste, 12,63 ha de kiwi da
# MESMA exploracao, localizado por duas coordenadas do gestor (testemunho de
# tipo 1, 28-08-2026) — fica **123 m a sul e 455 m a oeste do canto da AOI**.
# Estava fora do desenho por construcao, e nenhuma figura deste caso o mostrava.
#
# Isso tornava a propria peca incoerente: o texto diz «cerca de 44 hectares
# declarados» e o mapa mostrava 30,3. A diferenca e exactamente o B1.
#
# Nao confundir com a AOI `b1` (528400-529400, 4654900-4655700), que media
# tecido urbano de Valenca do outro lado do Minho e foi retirada a 28-08 com
# 49 ficheiros em quarentena. **Sao duas coisas diferentes com o mesmo nome**,
# e e a armadilha que esta figura documenta.
E0, N0, PASSO = AOI[0], AOI[3], 10.0


def para_utm(mask):
    """Contorno da mascara, em metros UTM, para poder coexistir com o B1."""
    return mask


ext = (E0, E0 + POMAR.shape[1] * PASSO, N0 - POMAR.shape[0] * PASSO, N0)
axm.contour(POMAR.astype(float), levels=[0.5], colors=[TINTA3], linewidths=1.4,
            extent=ext, origin="upper")
for m, cor in ((do & POMAR & COM, OCID), (de & POMAR & COM, ORIE)):
    axm.contourf(m.astype(float), levels=[0.5, 1.5], colors=[cor], alpha=0.90,
                 extent=ext, origin="upper")

# ── o B1, pelos poligonos do IFAP: fronteiras de outra entidade, exactas
from shapely.geometry import shape as _shape          # noqa: E402
from shapely.ops import transform as _sht             # noqa: E402
from pyproj import Transformer as _Tr                 # noqa: E402
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CUL_B1 = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
_tr = _Tr.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
_K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
_KF = _K["features"] if isinstance(_K, dict) else _K
B1_HA, b1x, b1y = 0.0, [], []
for _f in _KF:
    if int(_f["properties"]["CUL_ID"]) not in CUL_B1:
        continue
    g = _sht(lambda x, y, z=None: _tr.transform(x, y), _shape(_f["geometry"]))
    g = g.buffer(0)
    B1_HA += g.area / 1e4
    xy = np.array(list(g.exterior.coords))
    b1x += [xy[:, 0].min(), xy[:, 0].max()]
    b1y += [xy[:, 1].min(), xy[:, 1].max()]
    axm.fill(xy[:, 0], xy[:, 1], facecolor=NEUTRO, alpha=0.30, zorder=2)
    axm.plot(xy[:, 0], xy[:, 1], color=NEUTRO, lw=1.1, zorder=3)
print("B1 desenhado: %.2f ha de kiwi em %d parcelas do IFAP"
      % (B1_HA, len(CUL_B1)))

# ── janela que contem os dois sectores
mg = 90
x0 = min(E0 + np.where(POMAR.any(0))[0][0] * PASSO, min(b1x)) - mg
x1 = max(E0 + np.where(POMAR.any(0))[0][-1] * PASSO, max(b1x)) + mg
y0 = min(N0 - np.where(POMAR.any(1))[0][-1] * PASSO, min(b1y)) - mg
y1 = max(N0 - np.where(POMAR.any(1))[0][0] * PASSO, max(b1y)) + mg
axm.set_xlim(x0, x1); axm.set_ylim(y0, y1)
axm.set_aspect("equal")

axm.annotate("OCIDENTAL", xy=(530486, 4655052), xytext=(x0 + 20, y1 - 40),
             fontsize=10.4, color=OCID, fontweight="bold", va="top",
             arrowprops=dict(arrowstyle="-", color=OCID, lw=1.0))
axm.annotate("ORIENTAL", xy=(530969, 4655126), xytext=(x1 - 20, y1 - 20),
             fontsize=10.4, color=ORIE, fontweight="bold", ha="right",
             va="top", arrowprops=dict(arrowstyle="-", color=ORIE, lw=1.0))
axm.annotate("B1  ·  mesmo dono,\n12,6 ha de kiwi",
             xy=(529780, 4654240), xytext=(530250, 4654150),
             fontsize=10.0, color=NEUTRO, fontweight="bold", va="top",
             linespacing=1.4,
             arrowprops=dict(arrowstyle="-", color=NEUTRO, lw=1.0))
axm.plot([x1 - 40 - 200, x1 - 40], [y0 + 40, y0 + 40], lw=2.2, color=TINTA)
axm.text(x1 - 40 - 100, y0 + 52, "200 m", fontsize=8.6, color=TINTA2,
         ha="center", va="bottom")
axm.annotate("", xy=(x1 - 55, y0 + 300), xytext=(x1 - 55, y0 + 200),
             arrowprops=dict(arrowstyle="-|>", color=TINTA, lw=1.2))
axm.text(x1 - 55, y0 + 310, "N", fontsize=9.4, color=TINTA, ha="center",
         va="bottom")
fig.text(0.640, 0.288,
         # Os parenteses sao obrigatorios: com `+ chr(10) +` a meio, o `%` ligava
         # so ao ultimo literal e nao a concatenacao inteira.
         ("As duas zonas doentes, a %d m uma da outra, dentro do bloco de "
          "%.0f ha." + chr(10) + "A cinzento, o sector B1: %.1f ha de kiwi do "
          "mesmo dono, 500 m a sudoeste — fora da janela em que tudo o resto "
          "foi medido.") % (round(D_FOCOS), HA_BLOCO, B1_HA),
         fontsize=9.2, color=TINTA3, va="top")

# ── o bloco de decisão
axd = fig.add_axes([0.640, 0.100, 0.340, 0.135]); axd.axis("off")
axd.set_xlim(0, 1); axd.set_ylim(0, 1)
axd.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor="#f4f1ea",
                            edgecolor=RISCA, lw=1.0))
axd.text(0.045, 0.86, "PEDIDO", fontsize=10.2, color=TINTA, fontweight="bold",
         va="top")
axd.text(0.045, 0.63,
         "Autorização de despesa até 1.100 € + IVA\n"
         "(mínimo viável 360 €) para o painel de\n"
         "Setembro, à tabela oficial em vigor.",
         fontsize=9.4, color=TINTA2, va="top", linespacing=1.5)
axd.text(0.045, 0.16, "Decisão até: ____ · Colheita: Setembro de 2026",
         fontsize=8.8, color=TINTA3, va="top")

fig.text(0.040, 0.058,
         "Sete das dez explicações fecharam com medição; uma foi testada e o "
         "desenho não a isola; duas continuam abertas. "
         "O que sustenta cada frase desta página está nas peças seguintes, "
         "com a sua margem de erro ao lado.",
         fontsize=8.6, color=TINTA3)

fig.savefig(os.path.join(AQUI, "P01_o_caso_numa_pagina.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
fig.savefig(os.path.join(AQUI, "P01_o_caso_numa_pagina.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.32)
print("escrito P01 — o caso numa pagina")
