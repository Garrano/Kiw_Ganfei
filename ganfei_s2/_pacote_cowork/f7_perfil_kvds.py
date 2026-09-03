# -*- coding: utf-8 -*-
"""F7 — O caso de Ganfei contra o perfil de risco de KVDS.

NOTA DE PROVENIENCIA. Esta figura foi pedida como "os sete factores de risco de
Mandala 2024". Essa citacao circula no processo (tier1_framework_draft.md, §2)
mas NAO se confirma: a busca na literatura de KVDS nao encontra uma enumeracao
de sete factores, nem CEC baixa nem metodo de propagacao aparecem como factores
de risco de KVDS nas fontes acessiveis. A figura foi por isso construida sobre
o perfil de risco que E citavel, com a fonte marcada linha a linha.

Codificacao de estado: glifo (forma) + cor + rotulo, nunca cor sozinha.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Polygon

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM, NEUTRO = "#d03b3b", "#fab219", "#0a7a0a", "#9a9890"
AZUL = "#2a78d6"

# estado = (rotulo, cor, forma)
BATE = ("BATE — E ESTA MEDIDO", BOM, "cheio")
SUSP = ("SUSPEITO — NUNCA MEDIDO", CRIT, "vazio")
PARC = ("PARCIAL", AVISO, "meio")
NEG = ("TESTADO, NEGATIVO", NEUTRO, "cruz")
NAO = ("NÃO DOCUMENTADO EM KVDS", NEUTRO, "traco")

BLOCOS = [
 ("Física do solo e da água — o núcleo do síndrome", [
  dict(f="Encharcamento e anóxia radicular",
   lit="O factor desencadeante central. A videira de kiwi é muito sensível a "
       "défice de oxigénio na zona radicular (Frontiers 2024; Donati 2020).",
   nos="Hipótese do «imperme» levantada na visita de 04/08 por juízo visual. "
       "NENHUM poço de perfil foi aberto. Zero medições de cota freática, "
       "zero penetrómetro, zero amostras abaixo de 40 cm.",
   fonte="visita de campo, 2026", e=SUSP),
  dict(f="Compactação e inversão de horizontes",
   lit="Solos remexidos e compactados geram as condições de hipoxia. Perfis "
       "pedogenéticos «imaturos», de meteorização interrompida, são um dos "
       "dois extremos associados ao declínio (Plant and Soil, 2026).",
   nos="O emparcelamento tem 35 anos. Inversão de horizontes e sola de "
       "compactação são plausíveis por história, não por medição. O LiDAR "
       "mostra a microtopografia, não o perfil.",
   fonte="história do emparcelamento", e=SUSP),
  dict(f="Temperatura alta do solo",
   lit="Favorece os oomicetas e agrava a procura transpirativa.",
   nos="Série térmica Landsat corrida: 148 cenas. A anomalia existe mas está "
       "correlacionada com o ΔNDVI (r = −0,756) — é consequência da perda de "
       "copado, não linha de prova independente. Retirada como tal.",
   fonte="audit_termico.csv", e=PARC),
  dict(f="Colapso apoplético em procura evapotranspirativa alta",
   lit="Apresentação típica: murchidão irreversível e rápida, sem recuperação "
       "na estação seguinte.",
   nos="É o que a visita de campo descreve, e o que a gestora relata. "
       "Observação qualitativa, n não registado.",
   fonte="nota de visita, 04-08-2026", e=PARC),
 ]),
 ("Química e pedogénese", [
  dict(f="Solo ácido e pobre em bases",
   lit="O encharcamento prolongado mobiliza e lixivia catiões (Ca, Na, P); o "
       "desvio do equilíbrio mineralógico é apontado como factor-chave "
       "(Plant and Soil, 2026).",
   nos="MEDIDO E BATE. pH 5,2 a 5,6 em quatro blocos («precisa de 3 a 6 t/ha "
       "de cal»); CaO «muito baixo» em três (<154, 264, 314 mg/kg) contra "
       "4700 no B1 C1. É a correspondência quantitativa mais forte que temos.",
   fonte="11 boletins A2, 2026", e=BATE),
  dict(f="Desequilíbrio de fósforo",
   lit="Não é factor de risco descrito para KVDS; entra aqui por ser um dado "
       "forte que não se pode ignorar.",
   nos="P2O5 em EXCESSO em cinco dos nove pontos (134 a 324 mg/kg). "
       "Interpretação por fazer.",
   fonte="11 boletins A2, 2026", e=NAO),
  dict(f="Matéria orgânica e razão C:N",
   lit="Ligado à saúde microbiana do solo, não a KVDS em particular.",
   nos="MO 1,6–2,4% («média») em quase tudo, 4,5% no B1 C1. C:N baixa (5,9 e "
       "6,7) em dois blocos. Sem contraste são/doente, não decide nada.",
   fonte="11 boletins A2, 2026", e=NAO),
 ]),
 ("Biologia e hospedeiro", [
  dict(f="Oomicetas de solo (P. vexans, Phytophthora)",
   lit="Papel central atribuído na literatura de KVDS. Não são detectáveis "
       "visualmente; existe qPCR específico (Guaschino 2025).",
   nos="Oomicetas NEGATIVOS no solo — mas só a 0–30 cm, e a sondagem visual "
       "não os deteta. Em contrapartida G. intermedium POSITIVO em RAIZ na "
       "mesma amostra: prova interna de que o solo sub-deteta e o tecido "
       "radicular rende. O único P. sojae do processo é da B3C3, parcela "
       "isolada — não do corpo em declínio.",
   fonte="Areeiro 331/2025", e=NEG),
  dict(f="Desequilíbrio da comunidade microbiana",
   lit="O síndrome é multifactorial e ligado a desequilíbrio da comunidade "
       "rizosférica (Frontiers 2024; Microorganisms 2024).",
   nos="Quatro amostras ITS, todas da Zona 0. Retenção de leituras 29%, 3%, "
       "4% e 10% — duas delas não sustentam comparação de diversidade. Sem "
       "controlo são emparelhado.",
   fonte="ISFBV0314–17", e=PARC),
  dict(f="Pé franco — sem porta-enxerto",
   lit="NÃO é factor de risco documentado para KVDS nas fontes consultadas. "
       "O porta-enxerto entra na literatura como MEDIDA (material tolerante "
       "ao encharcamento na replantação), não como factor de risco medido.",
   nos="Confirmado pela gestora em 28-08-2026: o corpo principal é Erica de "
       "pé franco. Sem porta-enxerto não há tampão nenhum. Mas é UNIFORME, "
       "logo não explica o padrão — como M. hapla.",
   fonte="gestora, 2026", e=NAO),
 ]),
]

COL = [0.000, 0.180, 0.470, 0.775]
CAB = ["Factor", "O que a literatura de KVDS diz",
       "O que o caso de Ganfei tem", "Estado"]
W_LIT, W_NOS = 46, 48
TOPO = 0.858


def alturas():
    ys, y = [], TOPO
    for tit, linhas in BLOCOS:
        y -= 0.048
        for d in linhas:
            n = max(len(textwrap.wrap(d["lit"], W_LIT)),
                    len(textwrap.wrap(d["nos"], W_NOS)),
                    len(textwrap.wrap(d["f"], 22)) + 1)
            ys.append((y, n)); y -= 0.0128 * n + 0.0128
        y -= 0.014
    return ys, y


POS, BAIXO = alturas()
BAIXO -= 0.126
LARGURA = 17.8
fig = plt.figure(figsize=(LARGURA, LARGURA * (1.06 - BAIXO) / 1.10), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.036, 0.0, 0.928, 1.0])
ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(BAIXO, 1.06)
K = 0.928 * 1.10 / (1.06 - BAIXO)


def disco(x, y, r, forma, cor):
    if forma == "cheio":
        ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * K, facecolor=cor,
                             edgecolor="none", clip_on=False))
    elif forma == "vazio":
        ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * K, facecolor="none",
                             edgecolor=cor, lw=1.8, clip_on=False))
    elif forma == "meio":
        ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * K, facecolor="none",
                             edgecolor=cor, lw=1.5, clip_on=False))
        ax.add_patch(Polygon([(x, y - r * K), (x, y + r * K),
                              (x - r, y + r * K), (x - r, y - r * K)],
                             facecolor=cor, edgecolor="none", clip_on=False))
    elif forma == "cruz":
        for dx, dy in ((1, 1), (1, -1)):
            ax.plot([x - r * 0.75, x + r * 0.75],
                    [y - r * K * 0.75 * dy, y + r * K * 0.75 * dy],
                    color=cor, lw=1.8, clip_on=False, solid_capstyle="round")
    else:
        ax.plot([x - r, x + r], [y, y], color=cor, lw=2.4, clip_on=False,
                solid_capstyle="round")


ax.text(0, 1.054, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
        fontsize=9.5, color=TINTA2, va="top")
ax.text(0, 1.030, "O caso contra o perfil de risco de KVDS", fontsize=21,
        color=TINTA, fontweight="bold", va="top")
ax.text(1, 1.036, "F7 · 28-08-2026", fontsize=8, color=TINTA3, ha="right",
        va="top")
ax.text(0, 0.988,
        "Dez factores do perfil documentado de declínio da videira de kiwi, e o "
        "que o processo de Ganfei tem para cada um. A coluna da direita não é "
        "uma opinião: é o estado da prova.",
        fontsize=9.0, color=TINTA2, va="top")

# aviso de proveniencia — a citacao pedida nao se confirma
ax.add_patch(Rectangle((0, 0.884), 1, 0.070, facecolor="#fdf3e3",
                       edgecolor=AVISO, lw=1.2))
ax.text(0.010, 0.946, "SOBRE A FONTE", fontsize=7.4, color=TINTA,
        fontweight="bold", va="top")
ax.text(0.010, 0.930,
        "Esta figura foi pedida como «os sete factores de risco de Mandalà 2024». "
        "Essa citação circula no processo mas NÃO se confirma: a literatura de "
        "KVDS acessível não enumera sete factores,\ne nem CEC baixa nem método "
        "de propagação aparecem nela como factores de risco. A figura foi "
        "construída sobre o perfil que É citável, com a fonte marcada linha a "
        "linha —\ne as três linhas que não pertencem ao perfil de KVDS estão "
        "assinaladas como tal, em vez de serem contadas a favor.",
        fontsize=6.9, color=TINTA2, va="top", linespacing=1.6)

for c, t in zip(COL, CAB):
    ax.text(c, 0.872, t.upper(), fontsize=7.0, color=TINTA2, fontweight="bold",
            va="top")

i = 0
for tit, linhas in BLOCOS:
    y0 = POS[i][0] + 0.020
    ax.add_patch(Rectangle((0, y0), 1, 0.020, facecolor=TINTA,
                           edgecolor="none"))
    ax.text(0.008, y0 + 0.0095, tit.upper(), fontsize=7.6, color="white",
            fontweight="bold", va="center")
    for d in linhas:
        y, n = POS[i]; i += 1
        alt = 0.0128 * n + 0.0125
        if (i % 2) == 0:
            ax.add_patch(Rectangle((0, y - alt + 0.010), 1, alt,
                                   facecolor=FAIXA, edgecolor="none"))
        ax.text(COL[0], y, "\n".join(textwrap.wrap(d["f"], 22)), fontsize=8.4,
                color=TINTA, fontweight="bold", va="top", linespacing=1.35)
        ax.text(COL[0], y - 0.0128 * max(len(textwrap.wrap(d["f"], 22)), 1)
                - 0.004, d["fonte"], fontsize=6.0, color=TINTA3, va="top",
                style="italic")
        ax.text(COL[1], y, "\n".join(textwrap.wrap(d["lit"], W_LIT)),
                fontsize=6.6, color=TINTA2, va="top", linespacing=1.58)
        ax.text(COL[2], y, "\n".join(textwrap.wrap(d["nos"], W_NOS)),
                fontsize=6.6, color=TINTA, va="top", linespacing=1.58)
        rot, cor, forma = d["e"]
        disco(COL[3] + 0.014, y - 0.008, 0.011, forma, cor)
        ax.text(COL[3] + 0.034, y - 0.008, "\n".join(textwrap.wrap(rot, 17)),
                fontsize=6.5, color=cor, fontweight="bold", va="center",
                linespacing=1.4)
    i = i  # bloco seguinte

# ---------------- contagem e leitura --------------------------------------
yb = BAIXO + 0.098
ax.add_patch(Rectangle((0, yb - 0.004), 1, 0.030, facecolor=AZUL, alpha=0.09,
                       edgecolor="none"))
CONTA = [("1", "medido e a bater", BOM, "cheio"),
         ("2", "suspeito e NUNCA medido", CRIT, "vazio"),
         ("3", "parcial ou retirado", AVISO, "meio"),
         ("1", "testado e negativo — mas só à superfície", NEUTRO, "cruz"),
         ("3", "não é factor de KVDS documentado", NEUTRO, "traco")]
x = 0.010
for num, rot, cor, forma in CONTA:
    disco(x + 0.008, yb + 0.011, 0.009, forma, cor)
    ax.text(x + 0.024, yb + 0.011, num, fontsize=10.5, color=cor,
            fontweight="bold", va="center")
    ax.text(x + 0.040, yb + 0.011, rot, fontsize=6.8, color=TINTA2,
            va="center")
    x += 0.040 + 0.0058 * len(rot)

ax.text(0, yb - 0.026, "A LEITURA", fontsize=8.4, color=TINTA,
        fontweight="bold", va="top")
ax.text(0, yb - 0.044,
        "Bater no perfil de risco NÃO é diagnóstico. Quase todos os pomares "
        "de aluvião remexido da região dariam uma tabela parecida — o perfil "
        "diz que o sítio é vulnerável, não que a doença é esta.",
        fontsize=7.9, color=TINTA2, va="top")
ax.text(0, yb - 0.062,
        "O que decide é a assimetria da tabela: o único factor MEDIDO e a "
        "bater é a química do solo; os dois factores centrais do síndrome — "
        "encharcamento e compactação — continuam por medir ao fim de nove "
        "colheitas e de uma visita técnica.",
        fontsize=7.9, color=TINTA2, va="top")
ax.text(0, yb - 0.080,
        "E há três observações geométricas do próprio caso que empurram para "
        "este lado, não para o contacto radicular: o satélite a 143 m do "
        "centro da Mancha W, o arranque sectorial em cinco dias, e a taxa de "
        "avanço. Um agente que se move com a água explica os três; um fungo "
        "de contacto não explica nenhum.",
        fontsize=7.9, color=TINTA, fontweight="bold", va="top")
ax.text(0, yb - 0.104,
        "Fontes: Frontiers in Microbiology 2024 (10.3389/fmicb.2024.1330865) · "
        "Plant and Soil 2026 (10.1007/s11104-026-08777-0) · Microorganisms "
        "2024 (10.3390/microorganisms12112347) · Donati 2020 · Guaschino 2025. "
        "Dados do caso: 11 boletins A2 2026, Areeiro 331/2025, ISFBV0314–17, "
        "audit_termico.csv, difusa_nucleos.csv.",
        fontsize=6.3, color=TINTA3, va="top", linespacing=1.5)

fig.savefig("F7_perfil_kvds.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F7_perfil_kvds.svg", facecolor=FUNDO, bbox_inches="tight")
print("F7 gravada")
