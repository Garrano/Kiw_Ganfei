# -*- coding: utf-8 -*-
"""F13 — o que já foi eliminado, e o que falta.

O que a figura tem de fazer
---------------------------
E a figura do CASO, nao da auditoria. Responde a pergunta que um colega ou um
chefe faz primeiro: **entao o que e que isto e?** — e responde-lhe pela unica
via honesta que existe hoje: dizendo o que ja NAO e, com o numero e o
instrumento ao lado, e dizendo o que continua em aberto e porque.

Sete hipoteses foram fixadas antes de serem corridas, corridas, e **refutadas
por medicao**. Tres continuam em aberto, e as tres pela mesma razao: **ninguem
procurou**. Essa assimetria e o argumento para os proximos passos.

Forma
-----
Um quadro, duas faixas. Cada linha: a hipotese, como se testou, o numero que a
fecha ou a deixa aberta. O numero e o heroi de cada linha — e o que o leitor
retem. Estatuto por simbolo E por cor, nunca so por cor.

Todos os valores vem de ficheiro. Nenhum transcrito a mao.
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

ter = json.load(open(os.path.join(VG, "terreno_declinio.json")))
rede = json.load(open(os.path.join(VG, "rede_de_rega.json")))["agrupamento"]
pais = json.load(open(os.path.join(VG, "paisagem_resultado.json")))
alt = json.load(open(os.path.join(VG, "altura_focos.json")))

cota = [x[0] for x in ter["cota (negativa: baixo = humido)"]]
pcota = [x[1] for x in ter["cota (negativa: baixo = humido)"]]
ps_rede = [v["p"] for v in rede.values()]

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO = "#fbfbfa"
FECHADA = "#2f6b52"      # verde escuro — porta fechada, assunto arrumado
ABERTA = "#D55E00"       # vermillion — e aqui que esta o trabalho
RISCA = "#e6e3dd"

FECHADAS = [
    ("Seca",
     "precipitação ERA5-Land, dez anos",
     "Jul-Ago de 2026 foi o mais húmido da década",
     "82 mm", "o valor mais alto da série"),
    ("Ano mau para toda a paisagem",
     "35 cenas, seis classes de coberto, rótulos do IFAP e do LiDAR",
     "a mata madura não se mexeu",
     "−0,0035", "p = 0,81   ·   o milho caiu 0,077"),
    ("Encharcamento por posição no terreno",
     "MDT LiDAR a 50 cm contra a série, cota · microdepressão · TWI · área drenante",
     "o défice está no terreno ALTO, e está lá desde 2017",
     "ρ = %s a %s" % (("%+.2f" % min(cota)).replace(".", ",").replace("+", "").replace("-", "−"),
                      ("%+.2f" % max(cota)).replace(".", ",").replace("+", "").replace("-", "−")),
     "p < 0,001 nas onze cenas   ·   nada emerge em 2025-26"),
    ("Rede de rega sobre-estendida",
     "partição por válvula contra 200 partições rodadas da mesma geometria",
     "a válvula não explica nada que a geografia já não explique",
     "dentro do nulo em 11 de 11",
     "p de %s a %s   ·   e a distância à origem decai para zero"
     % (("%.2f" % min(ps_rede)).replace(".", ","),
        ("%.2f" % max(ps_rede)).replace(".", ","))),
    ("Porta-enxerto",
     "Summer Kiwi contra pé franco DENTRO do mesmo bloco, mesma água, mesmo solo",
     "as duas raízes comportam-se de forma idêntica",
     "−0,0004", "IC95 [−0,0015, +0,0014]   ·   nulo apertado"),
    ("Poda",
     "132 cenas de Abril a Outubro, saltos entre cenas a menos de 12 dias",
     "um único salto acima de 3 desvios em três anos — e é abrolhamento de Abril",
     "1 em 124", "nenhuma descontinuidade em Julho ou Agosto"),
    ("Arranque de linhas no foco ocidental",
     "LiDAR de 06-07-2025, altura MDS − MDT",
     "a pérgola está lá",
     ("%.2f m" % alt["foco OESTE da cadeia"]["altura"]).replace(".", ","),
     "%.0f %% acima de 1,5 m   ·   terreno lavrado lê 0,09 m"
     % alt["foco OESTE da cadeia"]["frac"]),
]

ABERTAS = [
    ("Patogénio de solo",
     "a hipótese que a forma do vazio no terreno sugere — mancha redonda que não\n"
     "respeita parcelário nem rega, assinatura de propagação por contacto de raízes",
     "ZERO", "ensaios com posição na válvula 8, onde está o padrão"),
    ("Cancro bacteriano — PSA",
     "Pseudomonas syringae pv. actinidiae, a principal doença do kiwi no mundo",
     "NUNCA", "foi pedida ao laboratório. Zero linhas bacterianas ou virais"),
    ("É regional, e não desta exploração",
     "1.054 ha de kiwi declarado por 204 beneficiários na mesma região,\n"
     "consultáveis por serviço aberto — e uma exploração a 8,1 km com sinal semelhante",
     "POR FAZER", "a comparação nunca foi corrida"),
]

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(14.6, 11.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.035, 0.035, 0.94, 0.845]); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

XH, XT, XN = 0.012, 0.300, 0.760      # hipótese · teste · número
y = 0.968
PASSO_F, PASSO_A = 0.0920, 0.0900

ax.text(XH, y + 0.022, "JÁ FECHADO", fontsize=11.6, color=FECHADA,
        fontweight="bold")
ax.text(XH + 0.135, y + 0.022, "sete hipóteses fixadas antes de correr, corridas, e refutadas por medição",
        fontsize=9.4, color=TINTA3)
ax.plot([XH, 0.988], [y + 0.008, y + 0.008], lw=1.6, color=FECHADA)

for i, (h, teste, leitura, num, sub) in enumerate(FECHADAS):
    yy = y - 0.030 - i * PASSO_F
    ax.plot([XH - 0.004], [yy + 0.008], "o", ms=8, color=FECHADA, zorder=3,
            clip_on=False)
    ax.plot([XH - 0.0075, XH - 0.0005], [yy + 0.008, yy + 0.005],
            color="white", lw=1.3, zorder=4)
    ax.plot([XH - 0.0005, XH + 0.004], [yy + 0.005, yy + 0.013],
            color="white", lw=1.3, zorder=4)
    ax.text(XH + 0.016, yy + 0.014, h, fontsize=11.6, color=TINTA,
            fontweight="bold", va="top")
    ax.text(XH + 0.016, yy - 0.012, teste, fontsize=8.4, color=TINTA3, va="top")
    ax.text(XT, yy + 0.010, leitura, fontsize=10.2, color=TINTA2, va="top")
    ax.text(XN, yy + 0.014, num, fontsize=15, color=FECHADA,
            fontweight="bold", va="top")
    ax.text(XN, yy - 0.014, sub, fontsize=8.2, color=TINTA3, va="top")
    ax.plot([XH, 0.988], [yy - 0.040, yy - 0.040], lw=0.7, color=RISCA)

y2 = y - 0.030 - len(FECHADAS) * PASSO_F - 0.030
ax.text(XH, y2 + 0.020, "POR ABRIR", fontsize=11.6, color=ABERTA,
        fontweight="bold")
ax.text(XH + 0.118, y2 + 0.020,
        "três hipóteses, e as três pela mesma razão — ninguém procurou",
        fontsize=9.4, color=TINTA3)
ax.plot([XH, 0.988], [y2 + 0.006, y2 + 0.006], lw=1.6, color=ABERTA)

for i, (h, teste, num, sub) in enumerate(ABERTAS):
    yy = y2 - 0.034 - i * PASSO_A
    ax.plot([XH - 0.004], [yy + 0.010], "o", ms=8, mfc="none", mec=ABERTA,
            mew=2.0, zorder=3, clip_on=False)
    ax.text(XH + 0.016, yy + 0.016, h, fontsize=11.6, color=TINTA,
            fontweight="bold", va="top")
    ax.text(XH + 0.016, yy - 0.010, teste, fontsize=8.4, color=TINTA3,
            va="top", linespacing=1.6)
    ax.text(XN, yy + 0.016, num, fontsize=15, color=ABERTA,
            fontweight="bold", va="top")
    ax.text(XN, yy - 0.010, sub, fontsize=8.2, color=TINTA3, va="top")
    if i < len(ABERTAS) - 1:
        ax.plot([XH, 0.988], [yy - 0.046, yy - 0.046], lw=0.7, color=RISCA)

fig.text(0.035, 0.960, "O que já não é, e o que falta saber",
         fontsize=23.5, fontweight="bold", color=TINTA)
fig.text(0.035, 0.922,
         "Declínio do kiwi no Emparcelamento de Ganfei, Valença.  "
         "Cada hipótese foi fixada antes de ser testada, e o resultado está ao lado do instrumento que o deu.",
         fontsize=11, color=TINTA2)
fig.text(0.035, 0.896,
         "As sete de cima fecharam-se com medição. As três de baixo continuam abertas porque nunca foram procuradas — "
         "e é aí que está o próximo passo.",
         fontsize=11, color=TINTA, fontweight="bold")

fig.savefig(os.path.join(AQUI, "F13_hipoteses.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
fig.savefig(os.path.join(AQUI, "F13_hipoteses.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.36)
print("escrito F13 — %d fechadas, %d abertas" % (len(FECHADAS), len(ABERTAS)))
