# -*- coding: utf-8 -*-
"""F5 — Desenho de amostragem para Setembro de 2026.

Tres paineis: (A) perfil em profundidade — que compartimento responde a que
pergunta, e onde e que a amostragem anterior nunca chegou; (B) matriz de
estratos x compartimentos com n e controlos emparelhados; (C) as regras
inegociaveis, cada uma a correccao de um defeito documentado das colheitas
anteriores. Paleta: slots 1/2/3 validados + estado (vermelho = lacuna).

Nota tecnica: os glifos circulares sao Ellipse com a altura corrigida pelo
racio fisico do eixo — Circle em coordenadas de fraccao sai ovalizado.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, BOM, NEUTRO = "#d03b3b", "#0a7a0a", "#9a9890"
Z0, MW = "#2a78d6", "#eb6834"
SOLO_A, SOLO_B, SOLO_C = "#e6dcc9", "#d2c3a6", "#b9a982"

LARGURA, ALTURA = 17.4, 13.4
fig = plt.figure(figsize=(LARGURA, ALTURA), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.042, 0.977, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.042, 0.951, "Desenho de amostragem · Setembro de 2026",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.958, 0.956, "F5 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.042, 0.921,
         "Nove colheitas já foram feitas neste pomar. Nenhuma respondeu à "
         "pergunta central, e sempre pela mesma razão: ou não tinha "
         "coordenadas, ou não tinha controlo, ou não chegou à profundidade certa.",
         fontsize=9.0, color=TINTA2)

# ================= PAINEL A — perfil em profundidade =======================
RA = [0.042, 0.398, 0.400, 0.478]
axA = fig.add_axes(RA)
axA.set_xlim(0, 100); axA.set_ylim(126, -56)
axA.set_axis_off()
fig.text(RA[0], 0.892, "A · O QUE COLHER, E A QUE PROFUNDIDADE",
         fontsize=8.8, color=TINTA, fontweight="bold")

PERF_X0, PERF_X1, CX_BOX = 8.0, 44.0, 48.0
for y0, y1, cor in ((0, 30, SOLO_A), (30, 80, SOLO_B), (80, 120, SOLO_C)):
    axA.add_patch(Rectangle((PERF_X0, y0), PERF_X1 - PERF_X0, y1 - y0,
                            facecolor=cor, edgecolor="none", zorder=1))
axA.add_patch(Rectangle((PERF_X0, 30), PERF_X1 - PERF_X0, 50, facecolor=CRIT,
                        alpha=0.13, edgecolor="none", zorder=2))
axA.text((PERF_X0 + PERF_X1) / 2, 55, "PONTO\nCEGO", fontsize=12.5, color=CRIT,
         fontweight="bold", ha="center", va="center", alpha=0.9,
         linespacing=1.25, zorder=3)
axA.plot([PERF_X0, PERF_X1], [0, 0], color=TINTA, lw=1.6, zorder=4)
for y in (30, 80):
    axA.plot([PERF_X0, PERF_X1], [y, y], color=TINTA3, lw=0.9, ls=(0, (4, 3)),
             zorder=4)

TR = (PERF_X0 + PERF_X1) / 2
axA.add_patch(Rectangle((TR - 1.7, -30), 3.4, 30, facecolor="#6b5540",
                        edgecolor="none", zorder=5))
for dx, dy in ((-13, -36), (-5, -40), (5, -40), (13, -36)):
    axA.plot([TR, TR + dx], [-27, dy], color="#6b5540", lw=1.6, zorder=5)
for x1, y1 in ((TR - 15, 40), (TR - 8, 55), (TR, 62), (TR + 9, 52),
               (TR + 16, 38)):
    axA.plot([TR, x1], [2, y1], color="#8a7358", lw=1.3, zorder=5,
             solid_capstyle="round")
axA.text(TR, -48, "planta na margem em avanço", fontsize=7.4, color=TINTA2,
         ha="center")

axA.plot([PERF_X0 - 3.4] * 2, [0, 120], color=TINTA3, lw=0.8)
for y, r in ((0, "0"), (30, "30 cm"), (80, "80 cm"), (120, "120 cm")):
    axA.plot([PERF_X0 - 4.6, PERF_X0 - 2.2], [y, y], color=TINTA3, lw=0.8)
    axA.text(PERF_X0 - 5.6, y, r, fontsize=6.5, color=TINTA3, va="center",
             ha="right")

CAMADAS = [
    (0, 34, 15, "JÁ AMOSTRADO — E SEMPRE NEGATIVO", BOM,
     "0–30 cm · RIZOSFERA SUPERFICIAL",
     "Os nove boletins de solo e as quatro amostras ITS ficaram todos aqui. "
     "Oomicetas, Armillaria e Rosellinia: todos negativos."),
    (40, 84, 55, "ZERO AMOSTRAS EM NOVE COLHEITAS", CRIT,
     "40–80 cm · A CAMADA QUE FALTA",
     "É aqui que a hipótese do «imperme» se resolve, e é aqui que os oomicetas "
     "sobrevivem ao Verão. Nunca ninguém colheu a esta cota."),
    (90, 124, 100, "POÇO DE PERFIL — PILAR B1", NEUTRO,
     "> 80 cm · SUBSTRATO / TOALHA",
     "Cota do nível freático suspenso, se existir. Resolve-se com poço de "
     "perfil, não com sonda."),
]
for y0, y1, yliga, tag, cor, tit, txt in CAMADAS:
    axA.plot([PERF_X1, CX_BOX], [yliga, (y0 + y1) / 2], color=cor, lw=1.0,
             alpha=0.55, zorder=3)
    axA.add_patch(Rectangle((CX_BOX, y0), 100 - CX_BOX, y1 - y0,
                            facecolor=FUNDO, edgecolor=cor, lw=1.4, zorder=6))
    axA.add_patch(Rectangle((CX_BOX, y0), 100 - CX_BOX, 6.4, facecolor=cor,
                            edgecolor="none", zorder=7))
    axA.text(CX_BOX + 1.6, y0 + 3.4, tag, fontsize=6.1, color="white",
             fontweight="bold", va="center", zorder=8)
    axA.text(CX_BOX + 1.6, y0 + 11.4, tit, fontsize=7.1, color=TINTA,
             fontweight="bold", va="center", zorder=8)
    axA.text(CX_BOX + 1.6, y0 + 15.6, "\n".join(textwrap.wrap(txt, 44)),
             fontsize=6.1, color=TINTA2, va="top", zorder=8, linespacing=1.55)

# ================= PAINEL B — matriz de estratos ===========================
RB = [0.470, 0.398, 0.488, 0.478]
axB = fig.add_axes(RB)
axB.set_xlim(0, 1); axB.set_ylim(0, 1); axB.set_axis_off()
fig.text(RB[0], 0.892, "B · ONDE, QUANTAS, E QUE COMPARTIMENTOS",
         fontsize=8.8, color=TINTA, fontweight="bold")
axB.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor="none"))

# correccao do racio fisico do eixo, para os glifos sairem redondos
K = (RB[2] * LARGURA) / (RB[3] * ALTURA)


def disco(ax, x, y, r, **kw):
    ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * K, **kw))


CX = [0.470, 0.605, 0.740, 0.882]
COLS = ["raízes\nfinas", "colo\n/ tronco", "solo\n0–30 cm", "solo\n40–80 cm"]
for nome, x in zip(COLS, CX):
    axB.text(x, 0.958, nome, fontsize=6.9, color=TINTA2, ha="center",
             va="top", fontweight="bold", linespacing=1.45)
axB.plot([0.025, 0.975], [0.876, 0.876], color=TINTA3, lw=0.9)
axB.add_patch(Rectangle((CX[3] - 0.058, 0.876), 0.116, -0.806, facecolor=CRIT,
                        alpha=0.075, edgecolor="none"))

LINHAS = [
    ("S1", Z0, "ZONA 0", "o foco mais antigo · nove anos",
     "6 plantas — 3 sintomáticas na margem\n+ 3 controlos assintomáticos ≥20 m",
     [1, 1, 1, 1]),
    ("S2", MW, "MANCHA W", "expansão concêntrica · 15–40 m/ano",
     "6 plantas — 3 na margem em avanço\n+ 3 controlos assintomáticos ≥20 m",
     [1, 1, 1, 1]),
    ("S3", CRIT, "SATÉLITES 3 · 4 · 5", "testam se o agente salta distâncias",
     "3 plantas — 1 por satélite\ncontrolo partilhado com S2",
     [1, 0, 1, 1]),
]
for i, (sid, cor, nome, sub, n, marcas) in enumerate(LINHAS):
    y = 0.775 - i * 0.262
    disco(axB, 0.062, y, 0.026, facecolor=cor, edgecolor="none")
    axB.text(0.062, y, sid, fontsize=8.2, color="white", fontweight="bold",
             ha="center", va="center")
    axB.text(0.112, y + 0.028, nome, fontsize=9.4, color=TINTA,
             fontweight="bold", va="center")
    axB.text(0.112, y - 0.012, sub, fontsize=6.7, color=TINTA2, va="center")
    axB.text(0.112, y - 0.062, n, fontsize=6.5, color=TINTA2, va="top",
             linespacing=1.6)
    for x, m in zip(CX, marcas):
        if m:
            disco(axB, x, y, 0.019, facecolor=cor, edgecolor="none")
        else:
            disco(axB, x, y, 0.019, facecolor="none", edgecolor=NEUTRO,
                  lw=1.2, ls=(0, (2, 2)))
    if i < 2:
        axB.plot([0.025, 0.975], [y - 0.132, y - 0.132], color=RISCA, lw=0.9)

axB.text(CX[3], 0.048, "a coluna que nunca\nfoi colhida", fontsize=6.3,
         color=CRIT, ha="center", va="top", fontweight="bold", linespacing=1.4)
axB.text(0.025, 0.040,
         "15 plantas · 51 amostras · uma única data · um único laboratório.",
         fontsize=7.0, color=TINTA, fontweight="bold")
axB.text(0.025, 0.014,
         "○ tracejado = colher apenas se houver sintoma de tronco visível.",
         fontsize=6.6, color=TINTA2)

# ================= PAINEL C — regras inegociaveis ==========================
fig.text(0.042, 0.352, "C · AS SEIS REGRAS QUE FALHARAM ATÉ AGORA",
         fontsize=8.8, color=TINTA, fontweight="bold")
fig.text(0.042, 0.331,
         "Cada uma corresponde a um defeito concreto e documentado das colheitas "
         "anteriores. Sem elas, Setembro produz mais um boletim que não se "
         "consegue ligar ao mapa.", fontsize=7.8, color=TINTA2)

REGRAS = [
    ("GPS em cada amostra",
     "O relatório 331/2025 é «Kiwi 1000», localização NÃO ESPECIFICADA: 14 "
     "organismos sem sítio. As quatro amostras ITS idem. Nada disto se "
     "consegue cruzar com o satélite."),
    ("Controlo emparelhado",
     "Nenhuma colheita até hoje teve assintomático. Sem par, um positivo não "
     "distingue agente de flora normal — e M. hapla saiu positivo em 5 de 5 "
     "blocos, sãos incluídos."),
    ("Margem, não centro",
     "A planta arrancada em 04/08 veio do centro de um foco. No centro há "
     "sobretudo colonizadores secundários; o agente primário está na frente "
     "de 5,92 ha que o satélite delimitou."),
    ("Painel de raiz, não de lenho",
     "O que existe é sobretudo madeira: Fusarium, Neofusicoccum, esca. São "
     "patogénios de stress, activados por outra coisa. A decisão de gestão "
     "está na raiz."),
    ("Uma data, um laboratório",
     "Os dois Becrop são o mesmo sector (válvula 27, confirmado pelo gestor) e "
     "dão «Saúde Muito Baixa» (ago 2023) contra «Saúde Alta» (jan 2024). Cinco "
     "meses, veredictos opostos, n=1 e sem controlo."),
    ("40–80 cm obrigatório",
     "Sete das dez exclusões abióticas deixam a mesma lacuna por cobrir: a "
     "subsuperfície. Colher só à superfície repete exactamente o resultado "
     "que já temos nove vezes."),
]
LARG_C = 0.1450
for i, (tit, txt) in enumerate(REGRAS):
    x = 0.042 + i * (LARG_C + 0.0086)
    axC = fig.add_axes([x, 0.128, LARG_C, 0.184])
    axC.set_xlim(0, 1); axC.set_ylim(0, 1); axC.set_axis_off()
    axC.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                            lw=0.8))
    axC.add_patch(Rectangle((0, 0.958), 1, 0.042, facecolor=CRIT,
                            edgecolor="none"))
    kc = LARG_C * LARGURA / (0.184 * ALTURA)
    axC.add_patch(Ellipse((0.115, 0.845), 0.118, 0.118 * kc, facecolor=CRIT,
                          edgecolor="none"))
    axC.text(0.115, 0.845, str(i + 1), fontsize=8.0, color="white",
             fontweight="bold", ha="center", va="center")
    axC.text(0.215, 0.845, "\n".join(textwrap.wrap(tit, 17)), fontsize=8.0,
             color=TINTA, fontweight="bold", va="center", linespacing=1.35)
    axC.text(0.058, 0.660, "\n".join(textwrap.wrap(txt, 36)), fontsize=6.2,
             color=TINTA2, va="top", linespacing=1.62)

fig.text(0.042, 0.086, "O QUE ESTE DESENHO PODE REFUTAR", fontsize=8.2,
         color=TINTA, fontweight="bold")
fig.text(0.042, 0.062,
         "Se S1, S2 e S3 derem o mesmo agente e os controlos derem negativo, a "
         "etiologia biótica fica estabelecida e o Pilar D abre.",
         fontsize=7.9, color=TINTA2)
fig.text(0.042, 0.040,
         "Se o agente aparecer também nos controlos assintomáticos, deixa de "
         "explicar o padrão — foi exactamente o que aconteceu a M. hapla, "
         "positivo em todos os blocos amostrados.",
         fontsize=7.9, color=TINTA2)
fig.text(0.042, 0.016,
         "Se S1 e S2 derem agentes DIFERENTES, os dois focos são dois problemas "
         "distintos, e a cronologia de faixa única (F3) tem de ser separada em "
         "duas. É o resultado que mais muda o dossiê.",
         fontsize=7.9, color=CRIT, fontweight="bold")

fig.savefig("F5_amostragem.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F5_amostragem.svg", facecolor=FUNDO, bbox_inches="tight")
print("F5 gravada")
