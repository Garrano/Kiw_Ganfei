# -*- coding: utf-8 -*-
"""F6 — Arvore de decisao do Pilar D, com o teste geometrico acrescentado.

O Pilar D do enquadramento lista cinco desfechos laboratoriais e o que fazer em
cada um. Esta figura acrescenta uma coluna que o texto nao tem: se cada desfecho
e ou nao COMPATIVEL com a geometria que o satelite ja mediu — centroide fixo a
+-17 m enquanto a area triplica, avanco radial de 15-40 m/ano, mancha nao
alinhada com as linhas de plantacao (165 graus contra 74 graus).

Essa coluna e o unico sitio do dossie onde as duas linhas de prova se cruzam
antes de haver resultados de laboratorio. Ela ja exclui ramos.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, FancyArrowPatch

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM, NEUTRO = "#d03b3b", "#fab219", "#0a7a0a", "#9a9890"
LACUNA, VERDE_F = "#efe7e4", "#e8f2e6"

LARGURA, ALTURA = 18.2, 12.8
fig = plt.figure(figsize=(LARGURA, ALTURA), dpi=200)
fig.patch.set_facecolor(FUNDO)
fig.text(0.036, 0.977, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
         fontsize=9.5, color=TINTA2)
fig.text(0.036, 0.951, "Árvore de decisão · o que fazer com cada resultado",
         fontsize=21, color=TINTA, fontweight="bold")
fig.text(0.964, 0.956, "F6 · 28-08-2026", fontsize=8, color=TINTA3, ha="right")
fig.text(0.036, 0.921,
         "Os cinco desfechos possíveis da colheita de Setembro, e a decisão de "
         "gestão que cada um obriga. A terceira linha de cada cartão é o "
         "acrescento desta figura: a geometria que o satélite já mediu não "
         "espera pelo laboratório — ela já vota.",
         fontsize=9.0, color=TINTA2)

# ---------------- no raiz --------------------------------------------------
axR = fig.add_axes([0.036, 0.828, 0.928, 0.068])
axR.set_xlim(0, 1); axR.set_ylim(0, 1); axR.set_axis_off()
axR.add_patch(Rectangle((0, 0), 1, 1, facecolor=TINTA, edgecolor="none"))
axR.text(0.018, 0.63, "RESULTADOS DE S1 · S2 · S3   →   OUTUBRO DE 2026",
         fontsize=11.5, color="white", fontweight="bold", va="center")
axR.text(0.018, 0.24,
         "15 plantas, 51 amostras, painel de raiz + oomicetas + nemátodos, com "
         "controlos assintomáticos emparelhados e coordenadas em cada amostra.",
         fontsize=7.6, color="#d8d6d0", va="center")
axR.text(0.982, 0.50, "F5", fontsize=15, color="#67655e", fontweight="bold",
         ha="right", va="center")

RAMOS = [
    dict(
        nome="Rosellinia necatrix\nconfirmada na raiz",
        prior=("POR TESTAR", CRIT),
        geo=("COMPATÍVEL", BOM),
        geo_txt="Alastra por contacto raiz-a-raiz e produz exactamente manchas "
                "circulares em expansão. É o único ramo que a geometria prevê "
                "sem forçar nada.",
        accao=["Saneamento com arranque do sistema radicular completo",
               "Contenção física da mancha; trabalhar os focos em último",
               "Tratamentos de solo tipo fluaziname onde autorizados",
               "Trichoderma só como adjuvante, nunca como medida principal",
               "Sem replantação de susceptíveis no perímetro"],
        custo="Alto e irreversível no perímetro tratado. Mas é o ramo com "
              "maior custo de atraso: alastra enquanto se decide."),
    dict(
        nome="Oomicetas / quadro\nKVDS confirmado",
        prior=("POR TESTAR A 40–80 cm", CRIT),
        geo=("PARCIAL", AVISO),
        geo_txt="Faz manchas, mas normalmente ao longo de linhas de água e "
                "rega. A nossa não segue as linhas de plantação (165° contra "
                "74°) nem a drenagem cartografada.",
        accao=["Romper a camada compactada, onde o poço de perfil a confirmar",
               "Valas de drenagem; camalhões nas replantações",
               "Rega de precisão — aplicações curtas, sem encharcamento",
               "Porta-enxertos tolerantes ao encharcamento na replantação",
               "Gestão do microclima do copado"],
        custo="Muito alto em obra, mas quase todo reversível e útil sob "
              "qualquer hipótese. É o ramo mais «sem arrependimento»."),
    dict(
        nome="Botriosferiáceas /\nesca no lenho",
        prior=("JÁ CONFIRMADO", BOM),
        geo=("INCOMPATÍVEL", CRIT),
        geo_txt="Dissemina-se por poda e inóculo aéreo — não produz frente "
                "radial no solo. Já está confirmado e mesmo assim não explica "
                "o mapa.",
        accao=["Saneamento de poda e protecção de feridas",
               "Remover braços mortos",
               "Redução de stress hídrico e térmico",
               "TRATAR COMO CONSEQUÊNCIA, não como causa"],
        custo="Baixo. Faz-se de qualquer maneira. O erro é parar aqui: foi "
              "o que já aconteceu — o painel existente é quase todo de lenho."),
    dict(
        nome="Meloidogyne hapla\nem densidade alta",
        prior=("JÁ CONFIRMADO — 5 de 5 blocos", BOM),
        geo=("INCOMPATÍVEL COMO CAUSA ÚNICA", CRIT),
        geo_txt="Positivo em todos os blocos amostrados, sãos incluídos. Um "
                "factor presente em todo o lado não pode explicar um padrão "
                "que só ocorre nalguns sítios.",
        accao=["Entra na decisão de porta-enxerto e de replantação",
               "Pesar como co-factor de predisposição, nunca como causa",
               "Contagens nos mesmos pontos, para ter contraste são/doente",
               "Não desviar orçamento de nematodicida do painel de raiz"],
        custo="Médio. O risco aqui não é o custo, é a distracção: é o "
              "resultado mais fácil de obter e o menos explicativo."),
    dict(
        nome="Nada confirmado\n+ física do solo forte",
        prior=("7 exclusões abióticas já negativas", AVISO),
        geo=("INCOMPATÍVEL", CRIT),
        geo_txt="Um padrão abiótico é estático e segue a topografia. O nosso "
                "centróide está fixo a ±17 m enquanto a área triplica, e "
                "avança 15–40 m por ano. Isso não é solo a mudar.",
        accao=["Reabrir o Pilar B em força: poços de perfil, penetrómetro",
               "Repetir o painel a 40–80 cm antes de aceitar o «nada»",
               "Reavaliar se a colheita cumpriu as seis regras da F5",
               "Um negativo com desenho errado não é um negativo"],
        custo="O ramo mais perigoso do dossiê: parece uma conclusão e é "
              "quase sempre uma falha de amostragem."),
]

N = len(RAMOS)
ESQ, DIR, GAP = 0.036, 0.964, 0.0105
LC = ((DIR - ESQ) - GAP * (N - 1)) / N
TOPO, ALT = 0.170, 0.612

for i, r in enumerate(RAMOS):
    x = ESQ + i * (LC + GAP)
    xc = x + LC / 2
    fig.add_artist(FancyArrowPatch((xc, 0.822), (xc, TOPO + ALT + 0.006),
                                   arrowstyle="-|>", mutation_scale=11,
                                   color=TINTA3, lw=1.0, shrinkA=0, shrinkB=0))
    ax = fig.add_axes([x, TOPO, LC, ALT])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
    k = LC * LARGURA / (ALT * ALTURA)
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=FAIXA, edgecolor=RISCA,
                           lw=0.8))

    cor_geo = r["geo"][1]
    ax.add_patch(Rectangle((0, 0.962), 1, 0.038, facecolor=cor_geo,
                           edgecolor="none"))
    ax.text(0.055, 0.918, r["nome"], fontsize=10.2, color=TINTA,
            fontweight="bold", va="top", linespacing=1.30)

    # chip do estado actual da prova
    txt, cor = r["prior"]
    ax.add_patch(Rectangle((0.055, 0.792), 0.89, 0.030, facecolor=cor,
                           alpha=0.15, edgecolor="none"))
    ax.add_patch(Ellipse((0.088, 0.807), 0.030, 0.030 * k, facecolor=cor,
                         edgecolor="none"))
    ax.text(0.118, 0.807, txt, fontsize=6.5, color=cor, fontweight="bold",
            va="center")

    # bloco da geometria — o acrescento desta figura
    ax.add_patch(Rectangle((0.028, 0.560), 0.944, 0.212,
                           facecolor=VERDE_F if cor_geo == BOM else LACUNA,
                           edgecolor=cor_geo, lw=1.1))
    ax.text(0.055, 0.742, "A GEOMETRIA DIZ", fontsize=6.0, color=TINTA2,
            fontweight="bold", va="top")
    ax.text(0.055, 0.712, r["geo"][0], fontsize=7.6, color=cor_geo,
            fontweight="bold", va="top")
    ax.text(0.055, 0.678, "\n".join(textwrap.wrap(r["geo_txt"], 40)),
            fontsize=6.0, color=TINTA2, va="top", linespacing=1.58)

    ax.text(0.055, 0.538, "DECISÃO DE GESTÃO", fontsize=6.4, color=TINTA,
            fontweight="bold", va="top")
    y = 0.502
    for a in r["accao"]:
        linhas = textwrap.wrap(a, 44)
        ax.text(0.062, y, "—", fontsize=6.2, color=cor_geo, va="top",
                fontweight="bold")
        ax.text(0.105, y, "\n".join(linhas), fontsize=6.3, color=TINTA2,
                va="top", linespacing=1.55)
        y -= 0.024 + 0.0255 * len(linhas)
    assert y > 0.150, "as accoes transbordam o rodape do cartao"

    ax.plot([0.055, 0.945], [0.142, 0.142], color=RISCA, lw=0.9)
    ax.text(0.055, 0.120, "CUSTO E REVERSIBILIDADE", fontsize=6.0,
            color=TINTA3, fontweight="bold", va="top")
    ax.text(0.055, 0.092, "\n".join(textwrap.wrap(r["custo"], 42)),
            fontsize=6.1, color=TINTA2, va="top", linespacing=1.58)

# ---------------- faixa do Pilar C ----------------------------------------
axC = fig.add_axes([ESQ, 0.088, DIR - ESQ, 0.062])
axC.set_xlim(0, 1); axC.set_ylim(0, 1); axC.set_axis_off()
axC.add_patch(Rectangle((0, 0), 1, 1, facecolor=VERDE_F, edgecolor=BOM,
                        lw=1.2))
axC.text(0.010, 0.72, "EM QUALQUER DOS RAMOS — começar já, sem esperar pelo "
         "laboratório  ·  PILAR C", fontsize=8.4, color=BOM,
         fontweight="bold", va="center")
axC.text(0.010, 0.28,
         "Arrancar plantas mortas COM a raiz e retirar do local (não estilhaçar "
         "nem enterrar)  ·  controlar infestantes com mobilização superficial  "
         "·  trabalhar os focos em último e limpar máquinas  ·  disciplina de "
         "rega, sem encharcamento nas margens  ·  não replantar nas falhas "
         "até haver etiologia.", fontsize=7.3, color=TINTA2, va="center")

fig.text(ESQ, 0.058,
         "A LEITURA QUE ATRAVESSA OS CINCO RAMOS", fontsize=8.2, color=TINTA,
         fontweight="bold")
fig.text(ESQ, 0.034,
         "Dos cinco desfechos, quatro são incompatíveis ou só parcialmente "
         "compatíveis com a geometria medida. O único que a geometria prevê "
         "sem forçar nada — alastramento radial por contacto — é justamente o "
         "que nunca foi testado.",
         fontsize=7.9, color=TINTA2)
fig.text(ESQ, 0.010,
         "Isto NÃO é um diagnóstico. É uma ordenação de prioridade de teste: "
         "diz onde gastar a colheita de Setembro, não o que ela vai dar. O "
         "quadro provável continua a ser multifactorial — o desenho tem de "
         "conseguir atribuir peso relativo, não coroar um culpado.",
         fontsize=7.9, color=CRIT, fontweight="bold")

fig.savefig("F6_arvore_decisao.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F6_arvore_decisao.svg", facecolor=FUNDO, bbox_inches="tight")
print("F6 gravada")
