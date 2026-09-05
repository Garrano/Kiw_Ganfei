# -*- coding: utf-8 -*-
"""P12 — CAMADA DO ESQUEMA DE REGA. Papel vegetal para pôr sobre a P11.

Duas saídas do mesmo desenho:

    P12_camada_rega.png            fundo transparente, só a mancha do mapa,
                                   registada célula a célula com a P11
    P12_camada_rega_isolada.png    a mesma, em papel e com legenda, para se
                                   ler sozinha

PORQUE ESTA CAMADA NÃO DESENHA A POSIÇÃO DAS VÁLVULAS
------------------------------------------------------
Há quatro reconstruções das posições em disco. **Discordam entre 92 e 398 m**,
e o espaçamento entre válvulas vizinhas é de 98 m: a discordância é maior do
que a distância entre válvulas. Só a `por_area` passa o teste das áreas
declaradas — **e esse teste é circular**, porque a `por_area` foi construída
por área acumulada para bater com essas mesmas áreas.

Há, isso sim, uma verificação que não é circular e que só se encontrou a 04-09:
o gestor nomeou «Zona 0 = válvulas 8, 9, 10», e a colocação por área põe a
válvula 8 a **34 m** desse ponto, com a frase fora do cálculo
(`m1_v8_implantacao.py`). Chega para o sector; não chega para a célula de uma
válvula numa malha de 98 m.

QUATRO TENTATIVAS DE GEORREFERENCIAR, E O ESTADO A 04-09
---------------------------------------------------------
    1. ICP global automático .................... RMS  70,3 m   falhou
    2. afim, pontos à vista ..................... RMS 189,1 m   falhou
    3. idem, com a ponta oriental corrigida ..... RMS 112,4 m   falhou
    4. ICP local POR BLOCO, escala fixa ......... RMS  33,6 m (banda)
                                                  RMS  24,6 m (lobo)   falhou

A tentativa 3 falhou por um erro meu: a ponta oriental do desenho fora lida em
x = 1562 px quando está em **x ≈ 2160** — 600 píxeis, ou 750 m. E dela saiu uma
conclusão publicada e depois **retirada**: «o desenho não tem escala única».

O gestor deu então a escala — **1:3500 em A1**, ou 1,259 m/px neste scan — e a
banda, remedida, dá 1,263. **O desenho está à escala.** A tentativa 4 fixa a
escala nesse valor (é testemunho: ganha ao cálculo) e ajusta por bloco.

Ficou perto e **não passou**: o critério pré-registado pedia RMS < 30 m e ≥8/12
válvulas dentro das parcelas na banda, ≥4/5 no lobo. Saiu 33,6 m com 6/12, e
24,6 m com 3/5. Todas as válvulas caem a **≤ 26 m** das parcelas — que é o chão
de leitura do método — mas o critério é o critério, e **não se publicam
posições**.

E o desenho mostra por que razão nenhuma reconstrução 1-D podia acertar: há
**duas fiadas de válvulas na mesma estação de linha** — as 10 e 13 de um lado
da conduta, as 11 e 12 do outro, todas anotadas «306 a 307».

O QUE O ESQUEMA FIXA, E QUE ESTA CAMADA DESENHA
------------------------------------------------
Topologia, não geometria. Que válvula serve que sector do gestor, em que
estação de linha está, e o débito dos sectores impressos onde a etiqueta foi
lida. Tudo isto está no desenho e não depende de georreferenciação nenhuma.

O registo com a P11 é ao nível do **sector**, que é o nível que aguenta: as
áreas por sector batem com as declaradas dentro de 17,7 %. Ao nível da válvula
não aguenta, e a camada diz isso em vez de o esconder.
"""
import io
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import matplotlib.patheffects as pe

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "base"))
from carta_base import (Base, cartela_institucional, COR, PAPEL, TINTA, TINTA2, TINTA3, virg,  # noqa
                        _halo)

CONDUTA = "#1B6E8C"
ALERTA = "#8C3B2E"

# A marginália vai numa serifa humanista, não na grotesca do corpo do mapa.
# É a convenção da cartografia impressa: a proveniência lê-se como nota de
# rodapé, e não como mais um rótulo a competir com os do terreno.
MARGINALIA = dict(family="Palatino Linotype", fontsize=7.0, style="italic",
                  linespacing=1.62)

# ── A CONVENÇÃO, e é o que faz esta camada servir para alguma coisa ─────────
#
#   TRAÇO CONTÍNUO, opaco   — está escrito numa fonte: no esquema, no
#                             parcelário do IFAP, ou dito pelo gestor.
#   TRAÇO INTERROMPIDO, 55 %— é nosso. Inferência, partição ou leitura por
#                             confirmar. **É o que se leva ao gestor.**
#
# Não é decoração: metade do que uma carta destas costuma afirmar não tem
# fonte, e sem esta distinção o leitor não consegue saber qual metade.
CONFIRMADO = dict(linestyle="-", alpha=1.00)
POR_CONF = dict(linestyle=(0, (5, 3)), alpha=0.55)

PERGUNTAS = [
    "Confirmar as etiquetas de sector das válvulas 10 a 17 (lemos G, F, E e D "
    "nas 6, 7, 8 e 9).",
    "Onde fica cada válvula DENTRO do seu sector? É o que nenhuma fonte nossa "
    "resolve.",
    "As válvulas 10, 11, 12 e 13 estão todas na estação 306–307, em fiadas "
    "opostas da conduta?",
    "Qual é a válvula desactivada na linha 185, e desde quando?",
    "As «4 novas válvulas» anotadas já foram instaladas? Com que números?",
    "A numeração de linha do B1 é independente da da banda (149, 137, 156, 705)?",
    "As divisões entre B2, Erica Novo, B3 e B4 no terreno — onde passam?",
]

# ── O QUE ESTÁ ESCRITO NO ESQUEMA. Transcrição, não inferência. ─────────────
#   `linhas` — estação de linha anotada à mão pelo gestor sobre o desenho.
#   `sectores_lidos` — etiqueta impressa do sector, lida a 650 dpi.
#   `debito` — m³ da caixa «Débito dos Sectores» do próprio esquema.
DEBITO = {"A": 65.0, "B": 85.0, "C": 90.5, "D": 95.8, "E": 87.6, "F": 79.1,
          "G": 99.9, "H": 91.5, "I": 78.5, "J": 71.6, "L": 55.8, "M": 55.3,
          "N": 82.7}
# ── ETIQUETAS DE SECTOR, com a origem de cada uma. Três estados:
#     "lida"      — lida por nós no desenho a 650 dpi. Entra a cheio.
#     "gestor"    — lida pelo gestor. Entra a tracejado, para ele confirmar.
#     ausente     — por ler. Não se inventa.
ETIQ = {6: ("G", "lida"), 7: ("F", "lida"), 8: ("E", "lida"), 9: ("D", "lida"),
        4: ("I", "gestor"), 5: ("H", "gestor"), 13: ("D", "gestor"),
        14: ("B", "gestor"), 15: ("N", "gestor"), 16: ("M", "gestor"),
        17: ("A", "gestor")}
BLOCOS = {
    "B1": dict(valvulas=[1, 2, 3, 4, 5],
               linhas="149 → v1,2,3  ·  137 e 156 → v4,5  ·  eixo linha 705",
               nota="numeração de linha PRÓPRIA"),
    "B2": dict(valvulas=[6, 7, 8, 9],
               linhas="130–131 → v6,7   ·   267–268 → v8,9", nota=""),
    "Erica Novo": dict(valvulas=[10, 11], linhas="306–307",
                       nota="mesma estação que as v12 e v13"),
    "B3": dict(valvulas=[12, 13, 14, 15],
               linhas="306–307 → v12,13   ·   336–337 → v14,15", nota=""),
    "B4": dict(valvulas=[16, 17],
               linhas="353 e 409 → v16   ·   423 → v17", nota=""),
}
for _b, _d in BLOCOS.items():
    _d["sectores"] = [ETIQ[v][0] for v in _d["valvulas"]
                      if ETIQ.get(v, ("", ""))[1] == "lida"]
NOTAS = [
    ("conduta principal sai do armazém na linha 222; linha da bomba, 229", CONDUTA),
    ("condutas de 2,5″ (v1), 3″ e 4″ no B1; 6″ na linha da bomba", CONDUTA),
    ("uma válvula DESACTIVADA na linha 185", ALERTA),
    ("«4 novas válvulas» anotadas, sem número atribuído", ALERTA),
    ("origem de água ÚNICA para toda a exploração", CONDUTA),
]


def desenha(ax, b, transparente):
    """A camada. Nada aqui depende de uma posição de válvula."""
    X = np.linspace(b.bb[0], b.bb[2], b.Z.shape[1])
    Y = np.linspace(b.bb[3], b.bb[1], b.Z.shape[0])
    from scipy import ndimage

    # ── o contorno dos sectores, para a camada se ler sozinha e para registar
    pontos = {}
    for nome in b.ORDEM:
        m = (b.SEC == b.COD[nome])
        if not m.any():
            continue
        ms = ndimage.binary_closing(m, np.ones((5, 5)))
        ax.contour(X, Y, ms.astype(float), levels=[.5],
                   colors=PAPEL if not transparente else "#FFFFFF",
                   linewidths=2.4, alpha=.45 if transparente else .9, zorder=5)
        # O B1 é a união de seis parcelas do IFAP: fronteira de outra entidade,
        # contínua. As divisões entre B2, Erica Novo, B3 e B4 saem da NOSSA
        # partição por válvula, e vão a tracejado — é o que falta confirmar.
        est = CONFIRMADO if nome == "B1" else POR_CONF
        ax.contour(X, Y, ms.astype(float), levels=[.5], colors=[COR[nome]],
                   linewidths=1.6, linestyles=[est["linestyle"]],
                   alpha=est["alpha"], zorder=6)
        if transparente:
            cm = matplotlib.colors.ListedColormap([COR[nome]])
            ax.imshow(np.ma.masked_where(~m, np.ones_like(m, float)),
                      extent=b.ext, origin="upper", cmap=cm, alpha=.10,
                      zorder=4, interpolation="nearest")
        dt = ndimage.distance_transform_edt(m)
        iy, ix = np.unravel_index(np.argmax(dt), dt.shape)
        pontos[nome] = (b.bb[0] + ix * b.pix, b.bb[3] - iy * b.pix)

    # ── a espinha: ordem da rede, oeste → este. SCHEMÁTICA, e diz-se.
    seq = [pontos[n] for n in b.ORDEM if n in pontos]
    ax.plot([p[0] for p in seq], [p[1] for p in seq], color=CONDUTA,
            lw=2.0, alpha=POR_CONF["alpha"], dashes=(5, 3),
            dash_capstyle="round", zorder=7)

    # ── as estações. Deslocadas da banda com tirante: a banda tem 200 m de
    #    largura e cinco crachás postos no centróide atropelam-se todos.
    # Todos para SUDESTE. A noroeste da banda está o rio, e o crachá do
    # Erica Novo caiu em cima do topónimo RIO MINHO.
    DESVIO = {"B1": (0, -250), "B2": (-150, -320), "Erica Novo": (30, -700),
              "B3": (170, -330), "B4": (60, -600)}
    CH, ESP, ALT = 26.0, 64.0, 150.0
    for nome in b.ORDEM:
        if nome not in pontos:
            continue
        Ea, Na = pontos[nome]
        dx, dy = DESVIO.get(nome, (0, 260))
        E, N = Ea + dx, Na + dy
        d = BLOCOS[nome]
        vs = d["valvulas"]
        larg = max(ESP * len(vs) + 46, 24 * len(nome) + 46)
        ax.plot([Ea, E], [Na, N], color=COR[nome], lw=1.0, alpha=.65,
                dashes=(3, 2.5), zorder=8)
        ax.plot([Ea], [Na], "o", ms=4.4, mfc=COR[nome], mec=PAPEL, mew=1.0,
                zorder=9)
        ax.add_patch(FancyBboxPatch((E - larg / 2, N - ALT / 2), larg, ALT,
                                    boxstyle="round,pad=8,rounding_size=18",
                                    facecolor=PAPEL, alpha=.93,
                                    edgecolor=COR[nome], linewidth=1.8,
                                    zorder=9))
        ax.annotate(nome, (E, N + ALT * .31), ha="center", va="center",
                    fontsize=13.0, weight="bold", color=TINTA, zorder=11)
        for i, v in enumerate(vs):
            cx = E - (len(vs) - 1) * ESP / 2 + i * ESP
            ax.add_patch(Circle((cx, N - ALT * .19), CH, facecolor=COR[nome],
                                edgecolor=PAPEL, linewidth=1.6, zorder=10))
            ax.annotate(str(v), (cx, N - ALT * .19), ha="center", va="center",
                        fontsize=8.6, weight="bold", color="white", zorder=11)
            if v in ETIQ:
                let, orig = ETIQ[v]
                ax.annotate(let if orig == "lida" else let + "?",
                            (cx, N - ALT * .19 - CH - 13), ha="center",
                            va="center", fontsize=8.0,
                            weight="bold" if orig == "lida" else "normal",
                            style="normal" if orig == "lida" else "italic",
                            color=TINTA if orig == "lida" else TINTA2,
                            alpha=1.0 if orig == "lida" else .8, zorder=11)
        deb = sum(DEBITO[x] for x in d["sectores"]) if d["sectores"] else None
        ax.annotate("linhas %s" % d["linhas"].split("·")[0].strip(),
                    (E, N - ALT * .78), ha="center", va="top", fontsize=7.0,
                    color=TINTA2, path_effects=_halo(2.8), zorder=11)
        if deb:
            ax.annotate("sectores %s  ·  %s m³"
                        % ("+".join(d["sectores"]), virg(deb)),
                        (E, N - ALT * .78 - 34), ha="center", va="top",
                        fontsize=7.0, color=CONDUTA, weight="bold",
                        path_effects=_halo(2.8), zorder=11)
        # Não se escreve «sector impresso por ler» debaixo dos outros quatro:
        # é uma lacuna NOSSA anotada na carta do gestor. A pergunta vai no
        # email, e a razão fica no FIGURAS_ABSTRACTS.md.

    # A ressalva da posição não resolvida saiu do mapa em 04-09. O traço
    # interrompido já a diz, e a chave da legenda explica-o; repeti-la por
    # extenso era pôr na carta do gestor uma lacuna que é nossa. Fica no
    # FIGURAS_ABSTRACTS.md, com os números.
    return ax


def legenda(axl, b):
    y = .985
    axl.annotate("O QUE ESTÁ CONFIRMADO", (0, y), xycoords="axes fraction",
                 ha="left", va="top", fontsize=7.6, weight="bold", color=TINTA2)
    y -= .034
    for est, cor, t1, t2 in (
            (CONFIRMADO, TINTA, "traço contínuo",
             "está escrito no esquema, no IFAP, ou dito pelo gestor"),
            (POR_CONF, TINTA, "traço interrompido",
             "inferência ou leitura por confirmar")):
        axl.plot([.012, .145], [y, y], color=cor, lw=1.8,
                 linestyle=est["linestyle"], alpha=est["alpha"],
                 transform=axl.transAxes, clip_on=False)
        axl.annotate(t1, (.185, y), xycoords="axes fraction", ha="left",
                     va="center", fontsize=8.2, color=TINTA)
        axl.annotate(t2, (.185, y - .020), xycoords="axes fraction", ha="left",
                     va="center", fontsize=6.5, color=TINTA3)
        y -= .056
    axl.annotate("G", (.055, y + .004), xycoords="axes fraction", ha="center",
                 va="center", fontsize=9.5, weight="bold", color=TINTA)
    axl.annotate("N?", (.115, y + .004), xycoords="axes fraction", ha="center",
                 va="center", fontsize=9.5, style="italic", color=TINTA2)
    axl.annotate("letra do sector impresso", (.185, y + .010),
                 xycoords="axes fraction", ha="left", va="center",
                 fontsize=8.2, color=TINTA)
    axl.annotate("a cheio, lida no desenho; em itálico com ?,",
                 (.185, y - .012), xycoords="axes fraction", ha="left",
                 va="center", fontsize=6.5, color=TINTA3)
    axl.annotate("lida pelo gestor e por confirmar",
                 (.185, y - .030), xycoords="axes fraction", ha="left",
                 va="center", fontsize=6.5, color=TINTA3)
    y -= .072

    axl.annotate("ESQUEMA DE REGA", (0, y), xycoords="axes fraction",
                 ha="left", va="top", fontsize=7.6, weight="bold", color=TINTA2)
    y -= .030
    for nome in b.ORDEM:
        d = BLOCOS[nome]
        axl.plot([.030], [y - .012], marker="o", ms=11, mfc=COR[nome],
                 mec="none", transform=axl.transAxes, clip_on=False)
        axl.annotate("%s  ·  válvulas %s"
                     % (nome, ", ".join(str(v) for v in d["valvulas"])),
                     (.075, y - .012), xycoords="axes fraction", ha="left",
                     va="center", fontsize=8.2, color=TINTA)
        axl.annotate("linhas %s" % d["linhas"], (.075, y - .034),
                     xycoords="axes fraction", ha="left", va="center",
                     fontsize=6.6, color=TINTA3)
        yy = y - .034
        if d["sectores"]:
            yy -= .020
            axl.annotate("sectores %s  ·  %s m³"
                         % ("+".join(d["sectores"]),
                            virg(sum(DEBITO[s] for s in d["sectores"]))),
                         (.075, yy), xycoords="axes fraction", ha="left",
                         va="center", fontsize=6.6, color=CONDUTA)
        y = yy - .030

    axl.annotate("DO PRÓPRIO ESQUEMA", (0, y), xycoords="axes fraction",
                 ha="left", va="top", fontsize=7.6, weight="bold", color=TINTA2)
    y -= .030
    for txt, cor in NOTAS:
        axl.annotate("·", (.02, y), xycoords="axes fraction", ha="left",
                     va="top", fontsize=9, color=cor)
        axl.annotate(txt, (.058, y), xycoords="axes fraction", ha="left",
                     va="top", fontsize=7.0, color=TINTA, wrap=True)
        y -= .030

    y -= .008
    axl.annotate("DÉBITO DOS SECTORES IMPRESSOS  (m³)", (0, y),
                 xycoords="axes fraction", ha="left", va="top", fontsize=7.6,
                 weight="bold", color=TINTA2)
    y -= .028
    ks = list(DEBITO)
    for i in range(0, len(ks), 4):
        axl.annotate("   ".join("%s %s" % (k, virg(DEBITO[k]))
                                for k in ks[i:i + 4]),
                     (.02, y), xycoords="axes fraction", ha="left", va="top",
                     fontsize=6.8, color=TINTA)
        y -= .022
    # A nota sobre as etiquetas por ler foi para o FIGURAS_ABSTRACTS.md.
    y -= .014

    # O rodapé estava ancorado no fundo enquanto o corpo crescia até lá abaixo,
    # e os dois encavalitavam-se. Passa a seguir o y corrente.
    y -= .052
    axl.annotate("Fonte   «Esquema de rega retificado» (PRDLUX, Jul-09), com as\n"
                 "anotações manuscritas do gestor.",
                 (0, min(y, .120)), xycoords="axes fraction", ha="left",
                 va="top", color=TINTA3, **MARGINALIA)


b = Base()

# ── 1 · o papel vegetal ─────────────────────────────────────────────────────
fig, ax, axl = b.figura(larg=16.0, legenda=True)
# O papel vegetal NÃO leva cartela institucional: é uma camada para sobrepor,
# e um logótipo repetido por cima do da carta-base fica a dobrar.
ytop = 0.924
axl.set_visible(False)
desenha(ax, b, transparente=True)
b.moldura(ax)
for s in ax.spines.values():
    s.set_alpha(.35)
ax.patch.set_alpha(0.0)
fora = os.path.join(AQUI, "P12_camada_rega.png")
fig.savefig(fora, dpi=200, transparent=True)
print("escrita %s  (transparente, registada com a P11)" % os.path.basename(fora))
plt.close(fig)

# ── 2 · a mesma, legível sozinha ────────────────────────────────────────────
fig, ax, axl = b.figura(larg=16.0, legenda=True)
ytop = cartela_institucional(fig)
b.terreno(ax, curvas=False, escoamento=False)
desenha(ax, b, transparente=False)
b.toponimos(ax)
# A caixa «A confirmar com o gestor» saiu da prancha em 04-09: as sete
# perguntas vão no corpo do email que acompanha o mapa. `PERGUNTAS` continua
# aqui, e é de onde esse email as tira — para não haver duas listas a divergir.
b.moldura(ax)
fig.text(0.035, ytop, "GANFEI · ESQUEMA DE REGA", fontsize=21, weight="bold",
         color=TINTA, va="top", ha="left")
fig.text(0.955, ytop, "17 válvulas  ·  5 sectores  ·  13 sectores "
                       "impressos", fontsize=10.5, color=TINTA2, va="top",
         ha="right")
fig.text(0.955, ytop - 0.034, "ETRS89 / UTM 29N (EPSG:32629)  ·  quadrícula 250 m",
         fontsize=8.2, color=TINTA3, va="top", ha="right")
legenda(axl, b)
fora2 = os.path.join(AQUI, "P12_camada_rega_isolada.png")
fig.savefig(fora2, dpi=200)
print("escrita %s  (com legenda)" % os.path.basename(fora2))
plt.close(fig)

json.dump(dict(debito_m3=DEBITO, blocos=BLOCOS, notas=[n for n, _ in NOTAS],
               posicoes_publicadas=False,
               razao="georreferenciação falhou o critério pré-registado "
                     "(RMS 70,3 m > 20 m) e as quatro reconstruções discordam "
                     "92–398 m para um espaçamento de 98 m"),
          io.open(os.path.join(AQUI, "base", "esquema_rega.json"), "w",
                  encoding="utf-8"), indent=1, ensure_ascii=False)
print("escrito base/esquema_rega.json")
