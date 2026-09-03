# -*- coding: utf-8 -*-
"""F1 — Matriz de diagnostico diferencial. Exhibit, nao grafico.

Codificacao: estado = glifo (forma) + cor + rotulo. Nunca cor sozinha —
a forma do glifo garante leitura a preto e branco e sob daltonismo.
Forca de evidencia = tres segmentos preenchidos + a palavra.
Paleta de estado validada (scripts/validate_palette.js): separacao CVD e
visao normal passam; o amarelo fica abaixo de 3:1 no fundo claro e por isso
so aparece como glifo ao lado de texto preto, nunca como texto.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge

TINTA, TINTA2, TINTA3 = "#0b0b0b", "#52514e", "#8a8880"
FUNDO, RISCA, FAIXA = "#fcfcfb", "#dedcd6", "#f4f3ef"
CRIT, AVISO, BOM, NEUTRO = "#d03b3b", "#fab219", "#0ca30c", "#9a9890"

POR = ("POR TESTAR", CRIT, "cheio")
INC = ("INCONCLUSIVO", AVISO, "meio")
EXC = ("EXCLUÍDO", BOM, "vazio")
CON = ("CONFIRMADO", BOM, "quadrado")
DES = ("DESPRIORITIZADO", NEUTRO, "traco")

BLOCOS = [
 ("Agentes biológicos", [
  dict(nome="Rosellinia necatrix",
   favor="Identificação de campo numa planta arrancada (2026); posição na berma sul, e as bermas são reservatório clássico da espécie.",
   ff="Fraca",
   contra="n=1, só visual, confirmação molecular dispensada pela própria equipa. A síntese do projecto conclui que o diagnóstico macroscópico falha.",
   fc="Forte",
   teste="PCR directa na amostra de raiz retida e nas margens em avanço (≈120 €).",
   estado=POR),
  dict(nome="Oomicetas / KVDS\n(P. vexans, Phytophthora)",
   favor="Melhor ajuste epidemiológico do dossiê: colapso apoplético em dias quentes, aluvião remexido, solo ácido e pobre em bases. A expansão radial isotrópica da Mancha W, a 15–40 m/ano, é rápida de mais para contacto radicular e ajusta-se a um agente que se move com a água — e o satélite a 143 m do foco reforça-o (ver F7).",
   ff="Moderada",
   contra="Sondagem de campo negativa — mas a sondagem não deteta oomicetas. E o único P. sojae do processo é da B3C3 (válvula 27), PARCELA ISOLADA, não o corpo em declínio: não é evidência para esta linha.",
   fc="Moderada",
   teste="Isolamento e qPCR em raiz fina e colo, nas margens (80–200 €).",
   estado=POR),
  dict(nome="Complexo da esca",
   favor="Sintomas foliares descritos como compatíveis; registos regionais históricos (Chicau, anos 2000).",
   ff="Fraca",
   contra="Sem sintomas primários no lenho em corte transversal. O sintoma foliar é inespecífico e flutua com o ambiente.",
   fc="Moderada",
   teste="Painel de micologia do lenho, INIAV (40 € + 120 € de confirmação).",
   estado=INC),
  dict(nome="Botryosphaeriaceae\n(N. parvum, Diplodia)",
   favor="Morte de varas da ponta para a base é o síndrome clássico; endófitos latentes activados por calor e stress hídrico; N. parvum positivo no Areeiro.",
   ff="Forte",
   contra="N. parvum nunca foi recuperado de raízes em KVDS publicado — pode ser artefacto de lavagem. O achado no lenho pode ser consequência e não causa.",
   fc="Moderada",
   teste="Painel do lenho alargado, com pares sintomático / assintomático.",
   estado=INC),
  dict(nome="Meloidogyne hapla",
   favor="Domina os nemátodos em kiwi português (37 de 40 pomares); 156 J2+ovos/g no B4 e 65 no B1; dois anos de pressão no extremo oeste.",
   ff="Forte",
   contra="Nenhum estudo testou predisposição nemátodo–fungo em kiwi. Não existe limiar económico publicado para a cultura.",
   fc="Forte",
   teste="Contagens nas margens S1 e S2, com galhas; colaboração UMinho.",
   estado=INC),
  dict(nome="Globisporangium\nintermedium",
   favor="Positivo em raiz (Areeiro 2025); oomiceta mais comum em kiwi em declínio na Turquia (Türkkan 2021).",
   ff="Moderada",
   contra="Mian 2023/25 encontra-o sobretudo em plantas ASSINTOMÁTICAS e propõe que compita com Phytophthora.",
   fc="Moderada",
   teste="Questão de literatura por correr. Até lá, NÃO É ALVO: pode fazer parte da comunidade supressora.",
   estado=INC),
  dict(nome="Fusarium spp.",
   favor="Três espécies positivas no lenho (Areeiro).",
   ff="Fraca",
   contra="A literatura trata-o como secundário da zona radicular; o ITS não separa o complexo F. sambucinum.",
   fc="Forte",
   teste="Sequenciação TEF1 do isolado, se tiver sido retido.",
   estado=DES),
 ]),
 ("Condutores abióticos e narrativas", [
  dict(nome="Camada impermeável /\nfísica do solo",
   favor="Emparcelamento há cerca de 30 anos com mistura de horizontes; solo aluvial; perfil de risco pedogenético de KVDS.",
   ff="Moderada",
   contra="Nunca foi observada. As covas de perfil continuam por abrir.",
   fc="Nenhuma",
   teste="Covas dentro das manchas contra zona sã: profundidade da camada, gleização, penetrómetro, textura por horizonte.",
   estado=POR),
  dict(nome="Água à superfície,\nencharcamento, geada",
   favor="Nenhuma que sobreviva aos testes.",
   ff="Nenhuma",
   contra="Sete testes remotos, todos negativos: precipitação, SAR em três Invernos, cota, escoamento, secagem do solo, geada (7 °C de folga) e atraso fenológico.",
   fc="Forte",
   teste="Feito. NÃO cobre toalha suspensa nem dreno enterrado.",
   estado=EXC),
  dict(nome="Hidráulica de rega\n(diluição da rede)",
   favor="Mais 11,16 ha de pomares novos na mesma origem entre 2022 e 2025; os dois focos dão um degrau em 2025; o B1 é poupado, por posição na rede.",
   ff="Moderada",
   contra="Abril é o mínimo de procura de rega. O degrau de 2021 da Zona 0 antecede as plantações novas. E um défice de rede não produz um foco circular a crescer a partir de um ponto fixo — produziria um sector.",
   fc="Forte",
   teste="Registos de rega, traçado actual da rede, e uma pergunta: houve reforço de captação ou bombagem?",
   estado=POR),
  dict(nome="Truncatura de solo\npelo nivelamento",
   favor="Emparcelamento confirmado; assinatura de rugosidade anormalmente uniforme no LiDAR.",
   ff="Fraca",
   contra="Nenhuma bancada de corte ou aterro detectável a 150 m. E uma truncatura é estática: explica um contorno fixo, não um foco que cresce 45 m em treze meses.",
   fc="Forte",
   teste="Espessura do horizonte A nas covas, na mancha e na zona sã. Fita métrica.",
   estado=POR),
  dict(nome="Expansão concêntrica\nda Mancha W",
   favor="Centróide fixo em 17 m enquanto a área triplicava (1,17 → 3,53 ha em 13 meses); alongamento 1,2–1,4; sem alinhamento com as linhas de plantação (foco a 165°, linhas a 74°); avanço radial de 15–40 m/ano.",
   ff="Forte",
   contra="Um núcleo satélite destacado, a 143 m do centro, aparece em 2026 — a propagação pode já não ser estritamente contígua.",
   fc="Fraca",
   teste="Confirmado por série de satélite 2017–2026. Drone ao nível da videira para mapear a frente activa.",
   estado=CON),
  dict(nome="Propagação a partir da\nZona 0 para o pomar",
   favor="Hipótese de trabalho do §B5, a testar com o arquivo de satélite.",
   ff="Fraca",
   contra="Centróide da Zona 0 fixo há nove anos. A Mancha W nasce em 2024 a 500 m de distância. São dois focos independentes, com cronologias diferentes: a Zona 0 dá degraus em 2021 e 2025, a Mancha W nasce em 2024.",
   fc="Forte",
   teste="Feito, por série de satélite 2017–2026.",
   estado=EXC),
 ]),
 ("Predisposição do hospedeiro", [
  dict(nome="Pé franco\n(planta sem porta-enxerto)",
   favor="Confirmado pelo gestor em 28-08-2026: o corpo principal é Erica de pé franco. Sem porta-enxerto não existe nenhuma tolerância a asfixia radicular nem a patogénios de raiz — é a configuração mais susceptível possível. Convive com um solo ácido e pobre em bases (pH 5,2–5,6 e Ca «muito baixo» em vários blocos), que é o perfil de risco descrito para KVDS. NOTA: a citação «Mandalà 2024, sete factores de risco» que circula no processo NÃO se confirma na literatura — ver F7.",
   ff="Forte",
   contra="É UNIFORME em todo o corpo principal, e por isso não pode explicar um padrão que só ocorre nalguns sítios — exactamente o mesmo problema que M. hapla. Explica porque é que o declínio é grave e irreversível, não onde começa.",
   fc="Forte",
   teste="Susceptibilidade uniforme × solo variável é testável: cruzar a química por bloco com a geometria dos focos, agora que a tabela válvula↔bloco existe. Por confirmar: se B1 foi sobre-enxertado nos troncos existentes, as raízes de B1 também são de pé franco e B1 deixa de ser contraste de propagação.",
   estado=CON),
 ]),
]

COL = [0.000, 0.152, 0.398, 0.645, 0.868]
CAB = ["Candidato", "Evidência a favor", "Evidência contra", "Teste que decide", "Estado"]
W_FAV, W_CON, W_TES = 44, 44, 38
TOPO = 0.902

# duas passagens: a primeira mede a altura total, a segunda desenha.
def altura_total():
    y = TOPO
    for titulo, linhas in BLOCOS:
        y -= 0.031 + 0.015
        for r in linhas:
            n = max(len(textwrap.wrap(r["favor"], W_FAV)),
                    len(textwrap.wrap(r["contra"], W_CON)),
                    len(textwrap.wrap(r["teste"], W_TES)),
                    r["nome"].count(chr(10)) + 1)
            y -= 0.0158 * n + 0.024
    return y - 0.105          # margem para a legenda e rodape

BAIXO = altura_total()
fig = plt.figure(figsize=(17.5, 17.5 * (1.02 - BAIXO) / 1.06), dpi=200)
fig.patch.set_facecolor(FUNDO)
ax = fig.add_axes([0.022, 0.010, 0.958, 0.978])
ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(BAIXO, 1.02)
T = ax.transData


def forca(x, y, nivel):
    n = {"Forte": 3, "Moderada": 2, "Fraca": 1, "Nenhuma": 0}[nivel]
    for i in range(3):
        ax.add_patch(Rectangle((x + i * 0.0074, y), 0.0056, 0.0072,
                     facecolor=TINTA2 if i < n else "none",
                     edgecolor=TINTA3, lw=0.6, transform=T, zorder=5, clip_on=False))
    ax.text(x + 0.0255, y - 0.0009, nivel, fontsize=6.5, color=TINTA2,
            va="bottom", ha="left", transform=T)


def glifo(x, y, forma, cor):
    if forma == "cheio":
        ax.add_patch(Circle((x, y), 0.0060, facecolor=cor, edgecolor="none",
                            transform=T, zorder=6, clip_on=False))
    elif forma == "meio":
        ax.add_patch(Circle((x, y), 0.0060, facecolor="none", edgecolor=cor,
                            lw=1.5, transform=T, zorder=6, clip_on=False))
        ax.add_patch(Wedge((x, y), 0.0060, 90, 270, facecolor=cor,
                           edgecolor="none", transform=T, zorder=6, clip_on=False))
    elif forma == "vazio":
        ax.add_patch(Circle((x, y), 0.0060, facecolor="none", edgecolor=cor,
                            lw=1.7, transform=T, zorder=6, clip_on=False))
    elif forma == "quadrado":
        ax.add_patch(Rectangle((x - 0.0052, y - 0.0052), 0.0104, 0.0104,
                     facecolor=cor, edgecolor="none", transform=T, zorder=6,
                     clip_on=False))
    else:
        ax.plot([x - 0.0058, x + 0.0058], [y, y], color=cor, lw=2.0,
                transform=T, zorder=6, solid_capstyle="round", clip_on=False)


ax.text(0, 0.978, "Declínio do kiwi · Emparcelamento de Ganfei, Valença",
        fontsize=9.5, color=TINTA2, transform=T)
ax.text(0, 0.946, "Matriz de diagnóstico diferencial", fontsize=21,
        color=TINTA, fontweight="bold", transform=T)
ax.text(1, 0.950, "F1 · 28-08-2026", fontsize=8, color=TINTA3, ha="right",
        transform=T)

for i, c in enumerate(CAB):
    ax.text(COL[i], TOPO + 0.012, c.upper(), fontsize=7.6, color=TINTA2,
            fontweight="bold", transform=T)
ax.plot([0, 1], [TOPO + 0.002, TOPO + 0.002], color=TINTA, lw=1.1, transform=T)

y = TOPO
for titulo, linhas in BLOCOS:
    y -= 0.031
    ax.text(0, y + 0.004, titulo.upper(), fontsize=8.4, color=TINTA,
            fontweight="bold", transform=T)
    ax.plot([0, 1], [y - 0.009, y - 0.009], color=TINTA3, lw=0.7, transform=T)
    y -= 0.015
    for k, r in enumerate(linhas):
        wf = textwrap.wrap(r["favor"], W_FAV)
        wc = textwrap.wrap(r["contra"], W_CON)
        wt = textwrap.wrap(r["teste"], W_TES)
        n = max(len(wf), len(wc), len(wt), r["nome"].count("\n") + 1)
        h = 0.0158 * n + 0.024
        if k % 2 == 1:
            ax.add_patch(Rectangle((-0.007, y - h + 0.005), 1.014, h - 0.005,
                         facecolor=FAIXA, edgecolor="none", transform=T, zorder=0, clip_on=False))
        ax.text(COL[0], y - 0.011, r["nome"], fontsize=8.9, color=TINTA,
                fontweight="bold", va="top", transform=T, linespacing=1.35)
        ax.text(COL[1], y - 0.010, "\n".join(wf), fontsize=7.4, color=TINTA2,
                va="top", transform=T, linespacing=1.42)
        forca(COL[1], y - h + 0.015, r["ff"])
        ax.text(COL[2], y - 0.010, "\n".join(wc), fontsize=7.4, color=TINTA2,
                va="top", transform=T, linespacing=1.42)
        forca(COL[2], y - h + 0.015, r["fc"])
        ax.text(COL[3], y - 0.010, "\n".join(wt), fontsize=7.4, color=TINTA2,
                va="top", transform=T, linespacing=1.42)
        glifo(COL[4] + 0.008, y - 0.0165, r["estado"][2], r["estado"][1])
        ax.text(COL[4] + 0.021, y - 0.0133, r["estado"][0], fontsize=7.3,
                color=TINTA, fontweight="bold", va="top", transform=T)
        ax.plot([0, 1], [y - h + 0.005, y - h + 0.005], color=RISCA, lw=0.6,
                transform=T)
        y -= h

y -= 0.012
ax.plot([0, 1], [y + 0.010, y + 0.010], color=TINTA, lw=0.9, transform=T)
leg = [(POR, "nenhum resultado laboratorial existe"),
       (INC, "há resultado, mas não decide"),
       (CON, "estabelecido por evidência"),
       (EXC, "afastado por evidência"),
       (DES, "não muda a gestão deste ano")]
x = 0.0
for (rot, cor, forma), nota in leg:
    glifo(x + 0.006, y - 0.002, forma, cor)
    ax.text(x + 0.018, y - 0.006, rot, fontsize=7.2, color=TINTA,
            fontweight="bold", transform=T)
    ax.text(x + 0.018, y - 0.020, nota, fontsize=6.6, color=TINTA2, transform=T)
    x += 0.197
ax.text(0, y - 0.043,
        "Força de evidência: ▪▪▪ Forte · ▪▪▫ Moderada · ▪▫▫ Fraca · ▫▫▫ Nenhuma.  "
        "O estado é o do conhecimento, não o da gravidade: CONFIRMADO e EXCLUÍDO partilham a cor por serem ambos questões resolvidas.  "
        "As cinco células POR TESTAR são o estado do dossiê, não uma omissão da figura: a Zona 0, o foco mais antigo, nunca teve painel etiológico.",
        fontsize=7.0, color=TINTA2, transform=T)

fig.savefig("F1_matriz_diagnostico.png", facecolor=FUNDO, bbox_inches="tight")
fig.savefig("F1_matriz_diagnostico.svg", facecolor=FUNDO, bbox_inches="tight")
print("F1 gravada — PNG e SVG")
