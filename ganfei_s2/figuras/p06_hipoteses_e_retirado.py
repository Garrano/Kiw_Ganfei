# -*- coding: utf-8 -*-
"""P06 — o que já não é, o que está confundido, o que falta saber. E o que retirámos.

Três mudanças em relação à F13, e todas vêm da adenda v1.8
----------------------------------------------------------
1. **O porta-enxerto sai de FECHADO.** A F13 lia «as duas raízes comportam-se
   de forma idêntica, −0,0004, nulo apertado» — verdade DENTRO do bloco, e
   incompleta. Entre blocos as trajectórias diferem (+0,2253 NDVI, e o radar
   confirma em duas órbitas), mas a janela **não isola a raiz**: os dois braços
   diferem na raiz *e* nos anos desde a enxertia, e o segundo domina. O estado
   honesto não é «fechado» nem «não testado» — é **testado e confundido**, com
   o multiverso a dizer qual escolha decide.

2. **Entra a coluna do RETIRADO, com dezanove linhas.** Não é um apêndice de
   modéstia: é o argumento que vai à frente do pedido. Um processo que apanha
   os seus próprios erros, e cada vez mais depressa, vale mais para quem decide
   do que qualquer p.

3. **A caixa ilustrativa é o halo**, e não o rio. O rio mostra um instrumento
   mal usado — água a ler NDVI positivo. O halo mostra uma estatística
   *correcta* à vista, morta por um teste melhor. É o caso mais difícil de
   contar e o mais útil.

Forma
-----
Duas colunas. À esquerda as hipóteses, em três bandas com cor e glifo próprios
— identidade nunca só por cor. À direita o RETIRADO, uma linha por item, com o
ano em que morreu e quem o matou. A caixa do halo fecha a coluna.
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

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"
alt = json.load(open(os.path.join(VG, "altura_focos.json")))

TINTA, TINTA2, TINTA3 = "#111111", "#55524d", "#94918b"
FUNDO, RISCA = "#fbfbfa", "#e6e3dd"
FECHADA = "#2f6b52"
CONFUND = "#8a6d1f"
ABERTA = "#eb6834"
MORTO = "#6b6f76"

vg = lambda v, c=2: ("%.*f" % (c, v)).replace(".", ",").replace("-", "−")

FECHADAS = [
    ("É regional, e não desta exploração",
     "37 blocos de kiwi do IFAP, 21,7 x 17,1 km, Sentinel-2 e 100 cenas Landsat," + chr(10) +
     "com triagem de descontinuidade a tirar 8 que mudaram de uso",
     "dos 29 que ficam, os dois focos são o 1.º e o 2.º",
     "P(errada) 0,07 a 0,25"),
    ("Seca", "precipitação ERA5-Land, dez anos",
     "Jul-Ago de 2026 foi o mais húmido da década", "82 mm"),
    ("Ano mau para toda a paisagem",
     "35 cenas, seis classes de coberto, rótulos do IFAP e do LiDAR",
     "a mata madura não se mexeu — o milho caiu 0,077", "p = 0,81"),
    ("Encharcamento por posição no terreno",
     "MDT LiDAR a 50 cm: cota, microdepressão, TWI, área drenante",
     "o défice está no terreno ALTO, e está lá desde 2017",
     "p < 0,001 em 11/11"),

    ("Poda", "132 cenas de Abril a Outubro, saltos entre cenas a < 12 dias",
     "um só salto acima de 3 desvios em três anos, e é de Abril",
     "1 em 124"),
    ("Arranque de linhas no foco ocidental",
     "LiDAR de 06-07-2025, altura MDS − MDT",
     "a pérgola está lá — terreno lavrado lê 0,09 m",
     "%s m" % vg(alt["foco OESTE da cadeia"]["altura"])),
]

CONFUNDIDAS = [
    ("Rede de rega sobre-estendida",
     "partição por válvula contra 200 partições rodadas da mesma geometria:" + chr(10) +
     "a válvula não explica nada que a geografia já não explique, 11/11 dentro do nulo.",
     "MAS as quatro reconstruções contêm as válvulas 6 a 17 — TODAS no corpo" + chr(10) +
     "principal. As válvulas 1 a 5, que servem o B1 a 500 m a sudoeste, estão" + chr(10) +
     "«POR COLOCAR», e o fundamento invoca um objecto retirado a 28-08.",
     "fechada só para o corpo principal · o troço que a torna sobre-estendida "
     "nunca foi testado"),
    ("Porta-enxerto  ·  Summer Kiwi contra pé franco",
     "dentro do bloco: nulo apertado, −0,0004, IC95 [−0,0015, +0,0014].  "
     "Entre blocos: trajectórias\n"
     "diferem +0,2253 NDVI, e o radar confirma em duas órbitas — 96 de 96 "
     "especificações positivas.",
     "A janela 2021-2026 NÃO isola a raiz: os braços diferem na raiz e nos anos "
     "desde a enxertia,\n"
     "e o segundo domina. A curva SATURA (recuperação); protecção pela raiz "
     "ALARGARIA.",
     "amplitude da janela 0,164 NDVI  ·  3,8 dp do nulo  ·  todas as outras "
     "oito bifurcações ≤ 0,030"),
]

ABERTAS = [
    ("Patogénio de solo",
     "mancha redonda que não respeita parcelário nem rega — assinatura de\n"
     "propagação por contacto de raízes",
     "ZERO", "ensaios com posição" + chr(10) + "em qualquer dos focos"),
    ("Cancro bacteriano — PSA",
     "Pseudomonas syringae pv. actinidiae, a principal doença do kiwi no mundo." + chr(10) +
     "Excluída por sintomatologia incompatível — testemunho de tipo 1",
     "POR DOCUMENTAR", "a decisão existe;" + chr(10) + "quem e quando, não"),
]

RETIRADO = [
    ("a designação dos dois focos esteve invertida", "sobreviveu a quatro auditorias; a última ocorrência foi a 31-08-2026 e morreu antes de chegar a uma figura"),
    ("viés de calibração do Sentinel-2C, −0,048 NDVI", "as quatro corridas independentes medem ≈ zero; era um degrau medido FORA do pomar"),
    ("uma «convergência» entre analistas", "comparava NDRE com NDVI; no mesmo índice diferem por um factor de 2,17"),
    ("«zero défice em 2022, 2023 e 2024»", "artefacto da abertura morfológica aplicada depois de intersectar; o piso real é 0,66 ha"),
    ("o teste placebo do degrau em chão", "o degrau em chão é 91 % do degrau em copado; só a variância residual difere"),
    ("o rio a ler NDVI +0,314", "água não pode ter NDVI positivo — máscara a entrar por uma janela mal recortada"),
    ("periodicidade das fileiras 2021 contra 2025", "a ortofoto de 2025 tem cobertura reflectiva na linha que a de 2021 não tem"),
    ("correcção de deriva aditiva", "a relação é ~7× multiplicativa; a calibração contra chão nu devolveu «−137 % acima do piso»"),
    ("a AOI «lóbulo oeste B1»", "media tecido urbano de Valença, com o rio pelo meio; 49 ficheiros em quarentena"),
    ("o «núcleo em declínio, p < 0,0005»", "dependia dessa AOI e continuou a imprimir números três dias depois de ela cair"),
    ("a distância de «1,06 km»", "não é reproduzível por nenhuma medida geométrica; a entidade que ela media não existe"),
    ("um halo com decaimento pela distância", "ρ ingénuo p = 2×10⁻⁹; por deslocamento toroidal p = 0,55, e o anel do meio é positivo"),
    ("o declive oriental como «declínio crónico»", "é um degrau, e o degrau ajusta 4 : 1 melhor; não há ano em que aquilo tenha caído 0,015"),
    ("três achados mortos pela MESMA curva", "uma curva de estabelecimento a saturar, lida como tendência: a divergência do lóbulo, o alarme do controlo, a janela do porta-enxerto"),
    ("«o lóbulo é o melhor controlo do caso»", "pertença em NÃO TESTÁVEL, origem da água desconhecida, e o viveiro foi inventado por quem escreveu a frase"),
    ("«o foco oriental foi replantado»", "concluído da prominência sozinha; o NDVI não tem cova em treze anos e em 2021 nem a referência tem o pico no compasso da pérgola"),
    ("«os fossos são conservadores, pelo T5»", "identidade algébrica: limpar a referência desloca todos os fossos pela MESMA constante, +0,008430, idêntica à nona casa"),
    ("«o B1 é o comparador sem degrau»", "zero instrumentos independentes, a recta ganha porque o bloco está em subida, e o veredicto dependia de um limiar inventado"),
    ("«blocos vizinhos com degrau 2 a 4× maior»", "estavam desmatados desde 2024 e a queda caía do lado PRÉ da fronteira; passou o portão com dois instrumentos e ρ = 0,890 porque ambos mediam a mesma coisa errada"),
]

fig = plt.figure(figsize=(18.6, 12.4), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.026, 0.030, 0.952, 0.845]); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

XH, XT, XN = 0.008, 0.212, 0.462          # coluna esquerda
XR, XRD = 0.630, 0.700                    # coluna direita
LIM = 0.607                               # divisória

# ─────────────────────────────────────────── coluna esquerda: as hipóteses
y = 0.975
ax.text(XH, y + 0.018, "JÁ FECHADO", fontsize=11.4, color=FECHADA,
        fontweight="bold")
ax.text(XH + 0.115, y + 0.019, "seis hipóteses fixadas antes de correr, "
        "corridas, e refutadas por medição", fontsize=8.8, color=TINTA3)
ax.plot([XH, LIM - 0.012], [y + 0.006, y + 0.006], lw=1.6, color=FECHADA)
y -= 0.030
for h, teste, leitura, num in FECHADAS:
    ax.plot([XH + 0.004], [y - 0.008], "o", ms=7, color=FECHADA)
    ax.text(XH + 0.020, y, h, fontsize=10.0, color=TINTA, fontweight="bold",
            va="top")
    ax.text(XH + 0.020, y - 0.021, teste, fontsize=8.0, color=TINTA3, va="top")
    ax.text(XT, y - 0.002, leitura, fontsize=9.0, color=TINTA2, va="top")
    ax.text(XN, y - 0.002, num, fontsize=9.6, color=FECHADA, va="top",
            fontweight="bold")
    y -= 0.052
    ax.plot([XH, LIM - 0.012], [y + 0.014, y + 0.014], lw=0.7, color=RISCA)

y -= 0.020
ax.text(XH, y + 0.016, "TESTADO, MAS CONFUNDIDO", fontsize=11.4,
        color=CONFUND, fontweight="bold")
ax.text(XH + 0.238, y + 0.017, "o desenho não consegue isolar o que a "
        "hipótese afirma", fontsize=8.8, color=TINTA3)
ax.plot([XH, LIM - 0.012], [y + 0.004, y + 0.004], lw=1.6, color=CONFUND)
y -= 0.032
for h, achado, porque, mv in CONFUNDIDAS:
    ax.plot([XH + 0.004], [y - 0.008], "s", ms=7, color=CONFUND)
    ax.text(XH + 0.020, y, h, fontsize=10.0, color=TINTA, fontweight="bold",
            va="top")
    ax.text(XH + 0.020, y - 0.022, achado, fontsize=8.2, color=TINTA2,
            va="top", linespacing=1.55)
    ax.text(XH + 0.020, y - 0.070, porque, fontsize=8.2, color=CONFUND,
            va="top", linespacing=1.55, fontweight="bold")
    ax.text(XH + 0.020, y - 0.118, mv, fontsize=7.8, color=TINTA3, va="top")
    y -= 0.178

y -= 0.008
ax.text(XH, y + 0.016, "AINDA ABERTO", fontsize=11.4, color=ABERTA,
        fontweight="bold")
ax.text(XH + 0.148, y + 0.017, "não porque tenha falhado — porque nunca foi "
        "procurado", fontsize=8.8, color=TINTA3)
ax.plot([XH, LIM - 0.012], [y + 0.004, y + 0.004], lw=1.6, color=ABERTA)
y -= 0.034
for h, teste, num, sub in ABERTAS:
    ax.plot([XH + 0.004], [y - 0.008], "D", ms=7, color=ABERTA)
    ax.text(XH + 0.020, y, h, fontsize=10.4, color=TINTA, fontweight="bold",
            va="top")
    ax.text(XH + 0.020, y - 0.022, teste, fontsize=8.0, color=TINTA3,
            va="top", linespacing=1.55)
    ax.text(XN, y - 0.002, num, fontsize=12.5, color=ABERTA, va="top",
            fontweight="bold")
    ax.text(XN, y - 0.032, sub, fontsize=7.8, color=TINTA2, va="top",
            linespacing=1.55)
    y -= 0.078

# ─────────────────────────────────────────────── divisória e coluna direita
ax.plot([LIM, LIM], [0.02, 0.995], lw=1.0, color="#e2dfd9")

y = 0.975
ax.text(XR, y + 0.018, "RETIRADO", fontsize=11.4, color=MORTO,
        fontweight="bold")
ax.text(XR + 0.090, y + 0.019, "dezanove afirmações que este processo matou — "
        "todas nossas", fontsize=8.8, color=TINTA3)
ax.plot([XR, 0.994], [y + 0.006, y + 0.006], lw=1.6, color=MORTO)
y -= 0.030
for i, (o_que, porque) in enumerate(RETIRADO):
    ax.text(XR, y, "%02d" % (i + 1), fontsize=8.0, color=TINTA3, va="top",
            family="DejaVu Sans Mono")
    ax.text(XR + 0.022, y, o_que, fontsize=9.2, color=TINTA, va="top",
            fontweight="bold")
    ax.text(XR + 0.022, y - 0.019, porque, fontsize=7.7, color=TINTA2,
            va="top", linespacing=1.5)
    y -= 0.0505
    ax.plot([XR, 0.994], [y + 0.012, y + 0.012], lw=0.6, color=RISCA)

# a caixa ilustrativa: o halo
y -= 0.012
ax.add_patch(plt.Rectangle((XR, y - 0.132), 0.994 - XR, 0.132,
                           fc="#f2efe9", ec="#ded9d0", lw=0.9, zorder=1))
ax.text(XR + 0.014, y - 0.014, "O CASO MAIS DIFÍCIL DE CONTAR, E O MAIS ÚTIL",
        fontsize=9.0, color=TINTA, fontweight="bold", va="top", zorder=3)
ax.text(XR + 0.014, y - 0.040,
        "Procurámos um decaimento do dano com a distância ao foco. Seria o "
        "discriminador mais forte que este\n"
        "caso tem: um agente que se propaga produz decaimento, uma decisão de "
        "gestão não tem por que produzir.",
        fontsize=8.0, color=TINTA2, va="top", linespacing=1.6, zorder=3)
ax.text(XR + 0.014, y - 0.079,
        "ρ de Spearman = −0,123.  p ingénuo = 2×10⁻⁹.  "
        "p por deslocamento toroidal = 0,55.",
        fontsize=8.6, color=TINTA, va="top", fontweight="bold", zorder=3)
ax.text(XR + 0.014, y - 0.100,
        "E os anéis não decaem: −0,059 · −0,017 · +0,015 · −0,027. O do meio é "
        "positivo. Encontrámos um resultado a\n"
        "p = dois em mil milhões e deitámo-lo fora, porque o teste que respeita "
        "a autocorrelação deu 0,55.",
        fontsize=8.0, color=TINTA2, va="top", linespacing=1.6, zorder=3)

# ─────────────────────────────────────────────────────────────── título
fig.text(0.026, 0.960, "O que já não é, o que falta saber — e o que retirámos",
         fontsize=23, fontweight="bold", color=TINTA)
fig.text(0.026, 0.922,
         "Cada hipótese foi fixada antes de ser testada, e o resultado está ao "
         "lado do instrumento que o deu.",
         fontsize=11, color=TINTA2)
fig.text(0.026, 0.892,
         "Seis fecharam com medição. Duas foram testadas e o desenho não as isola. "
         "Duas continuam abertas: uma porque nunca foi procurada, a outra "
         "porque a decisão de a excluir não está escrita em lado nenhum.",
         fontsize=11, color=TINTA, fontweight="bold")

fig.savefig(os.path.join(AQUI, "P06_hipoteses_e_retirado.png"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
fig.savefig(os.path.join(AQUI, "P06_hipoteses_e_retirado.svg"), facecolor=FUNDO,
            bbox_inches="tight", pad_inches=0.34)
print("escrito P06 — %d fechadas, %d confundidas, %d abertas, %d retiradas"
      % (len(FECHADAS), len(CONFUNDIDAS), len(ABERTAS), len(RETIRADO)))
