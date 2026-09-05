# -*- coding: utf-8 -*-
"""Carta-base de Ganfei — módulo de desenho reutilizável.

Isto NÃO é uma figura. É o substrato que todas as figuras seguintes desenham
por baixo dos seus dados: o esquema de rega, os tipos de solo, os porta-enxertos,
as datas de plantação, as manchas de mortalidade. Todas têm de assentar na
**mesma geometria e nos mesmos nomes**, senão comparam-se coisas diferentes.

    from carta_base import Base
    b = Base()
    fig, ax = b.figura()
    b.terreno(ax)               # relevo, água, curvas de nível, escoamento
    b.cadastro(ax)              # parcelas do IFAP
    b.sectores(ax)              # os cinco sectores do gestor, preenchidos
    b.valvulas(ax)              # as 17 válvulas, numeradas
    b.rotulos(ax)               # nomes dos sectores
    b.moldura(ax)               # quadrícula UTM, escala, norte
    # ... a camada nova desenha-se aqui, por cima ...
    b.legenda(axl, entradas=[...])

NOMES. São os do gestor, e só esses: **B1, B2, Erica Novo, B3, B4**. Vêm da
tabela de válvulas dele (`valvulas_por_area.json`) e dos boletins A2, que
trazem o código de bloco escrito. Não se inventa nem se traduz nenhum.

CRS. EPSG:32629 (ETRS89 / UTM 29N) — a grelha em que este processo faz todas as
contas. O MDT da DGT vem em EPSG:3763 e é reprojectado no `preparar_base.py`;
o parcelário vem em WGS84. Misturar os três sem dizer qual é qual já quase
custou uma análise inteira.

COR. Os cinco sectores usam uma paleta verificada com o validador de CVD:
pior par adjacente ΔE 11,0 (deutan). O relevo fica em cinzentos e tons de
terra dessaturados **de propósito** — a cor é um recurso escasso e pertence aos
dados que vierem por cima, não ao fundo.
"""
import io
import json
import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly, Rectangle, FancyArrow
import matplotlib.patheffects as pe
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))

# ── identidade visual ───────────────────────────────────────────────────────
PAPEL = "#FBFAF7"
TINTA = "#1F1D1A"
TINTA2 = "#5C574F"
TINTA3 = "#8A8378"
COR = {"B1": "#0072B2", "B2": "#D55E00", "Erica Novo": "#009E73",
       "B3": "#7E4E9B", "B4": "#E69F00"}
AGUA = "#5E93AE"
NIVEL_AGUA = 2.5      # m — abaixo disto e leito do Minho, nao terreno
# A marginália — proveniência, método, ressalvas — vai numa serifa humanista
# e não na grotesca do corpo do mapa. É a convenção da cartografia impressa:
# lê-se como nota de rodapé, não como mais um rótulo a competir com o terreno.
MARGINALIA = dict(family="Palatino Linotype", fontsize=7.0, style="italic",
                  linespacing=1.62)
CURVA = "#A79C88"
CURVA_ALTA = "#B2977A"

# rampa hipsométrica: fina na plataforma (4-10 m), comprimida na encosta
RAMPA = [(0.0, "#C4CED2"), (2.5, "#DBDFDE"), (4.0, "#E7E7DC"), (7.0, "#F0EEE2"),
         (10.0, "#E9E2CD"), (20.0, "#DCCFB2"), (50.0, "#C6B290"),
         (100.0, "#AD9170"), (160.0, "#8E7050")]

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 0.7,
    "figure.facecolor": PAPEL,
    "savefig.facecolor": PAPEL,
    "text.color": TINTA,
    "axes.edgecolor": TINTA2,
})


def _halo(w=3.0, c=PAPEL):
    return [pe.withStroke(linewidth=w, foreground=c)]


# ── identidade institucional ────────────────────────────────────────────────
#
# O logótipo é o da CCDR-N, extraído do cabeçalho das próprias circulares da
# Estação de Avisos (`circul_10_junho_2025_EAEDM.pdf`, 172×57 px). Não é
# redesenhado nem aproximado: é a marca deles, tirada de um documento deles.
#
# A designação vem do gestor da unidade — testemunho directo. A portaria dos
# estatutos de 2026 não nomeia divisões temáticas (só as territoriais), mas as
# divisões são criadas por deliberação do conselho directivo e não pela
# portaria: o silêncio do diploma não é inexistência.
# HIERARQUIA. A identidade do editor é **subordinada** ao assunto da folha.
# Na primeira versão ela media 7,4/8,6/7,4 pt com a linha do meio a negro e a
# negrito, contra um título de 21 — razão de 2,4 para 1, e o negrito a puxá-la
# ainda mais para cima. Duas coisas a disputar o mesmo lugar.
#
# Aqui a razão passa a ~3,4 para 1, o negro sai (a identidade fica em TINTA2 e
# TINTA3), e o peso forte guarda-se só para a divisão, que é a linha com
# significado. O logótipo encolhe na mesma proporção.
# A identidade corre numa LINHA, ao lado do logótipo, e não empilhada em três.
# Empilhada, formava um bloco com massa própria que competia com o título; em
# linha, lê-se como o cabeçalho de folha que é — uma tira de crédito, não um
# segundo título.
#
# E cai a redundância que estava lá: o logótipo já diz CCDR NORTE. Escrever
# «CCDR-N» ao lado dele é dizer duas vezes a mesma coisa, e ocupava o lugar
# onde a divisão devia estar a ganhar peso.
#
# Dentro da linha a hierarquia mantém-se pelo peso: a divisão é a única com
# significado operacional, e é a única em semibold.
# QUAL NOME CARREGA A FOLHA — decidido por robustez, não por gosto.
#
# A prática de topo diz: a entidade-mãe é a marca dominante, a unidade é
# subordinada, e um título de unidade só se contextualiza quando não é único
# dentro do Estado. A marginália cartográfica pede, além do produtor, a
# identificação da SÉRIE.
#
# Aqui isso resolve-se por um facto medido. Os estatutos mudaram a meio do
# período experimental (Portaria 239/2026, em vigor 30-05-2026); as divisões
# nomeadas no diploma são TERRITORIAIS, e as temáticas criam-se por deliberação
# do conselho directivo — podem mudar sem diploma. Já «Estação de Avisos»
# ocorre ZERO vezes nos estatutos e assina 292 boletins em 46 anos.
#
# A divisão é legalmente real e administrativamente volátil; a estação é
# administrativamente invisível e operacionalmente permanente. Uma identidade
# assente na divisão envelhece com a próxima deliberação.
#
# E os próprios documentos que saem já resolvem isto: o cabeçalho da circular
# traz AVISOS AGRÍCOLAS e ESTAÇÃO DE AVISOS DE ENTRE DOURO E MINHO, e NÃO
# nomeia a divisão. Essa solução atravessou a mudança de estatutos intacta.
#
# A divisão desce ao rodapé como unidade responsável: não se perde, deixa de
# competir com o título, e não data a folha.
INSTITUICAO = [
    ("Comissão de Coordenação e Desenvolvimento Regional do Norte, I.P.",
     TINTA3, "normal"),
    ("Avisos Agrícolas — Estação de Avisos de Entre Douro e Minho",
     TINTA2, "semibold"),
]
UNIDADE_RODAPE = "Divisão Agroalimentar e Pescas — Entre Douro e Minho"
CORPO_INST = 7.0
# o logótipo vai com fundo chaveado a transparente — um logótipo dentro de uma
# caixa branca sobre papel creme lê-se como um autocolante, não como uma marca
LOGO = os.path.join(AQUI, "..", "marca", "ccdrn_alpha.png")


def cartela_institucional(fig, x=0.035, y=0.980, alt_logo=0.034,
                          respiro_pol=0.40, risco=True):
    """Logótipo e identidade numa linha só, a atravessar a folha.

    Os segmentos são medidos e encadeados: o matplotlib não compõe pesos
    diferentes dentro de um `text`, portanto desenha-se um de cada vez e
    avança-se pela largura renderizada de cada um.

    `respiro_pol` — o branco entre a tira e o título, em polegadas. É
    estrutura: a convenção da folha impressa é que valha pelo menos a altura
    de maiúscula do título (0,29 pol com 21 pt), e de preferência mais.

    Devolve o `y` onde o título pode começar.
    """
    import matplotlib.image as mpimg
    W = fig.get_figwidth() * fig.dpi
    if os.path.exists(LOGO):
        im = mpimg.imread(LOGO)
        h, w = im.shape[:2]
        larg = alt_logo * (w / h) * (fig.get_figheight() / fig.get_figwidth())
        ax = fig.add_axes([x, y - alt_logo, larg, alt_logo], zorder=20)
        ax.imshow(im, interpolation="lanczos")
        ax.axis("off")
        xt = x + larg + 0.014
    else:
        xt = x
    ymeio = y - alt_logo / 2.0
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()

    def por(txt, cor, peso):
        """Desenha e devolve a largura em fracção de figura."""
        t = fig.text(por.x, ymeio, txt, fontsize=CORPO_INST, color=cor,
                     weight=peso, va="center", ha="left")
        return t.get_window_extent(renderer=ren).width / W

    por.x = xt
    for k, (txt, cor, peso) in enumerate(INSTITUICAO):
        if k:
            por.x += por("   ·   ", TINTA3, "normal")
        por.x += por(txt, cor, peso)

    fundo = y - alt_logo
    if risco:
        # filete: formaliza a tira sem lhe dar massa. Fica bem abaixo do
        # logótipo e bem acima do título, e atravessa a largura útil.
        yr = fundo - 0.011
        fig.add_artist(plt.Line2D([x, 0.955], [yr, yr], color=TINTA3,
                                  lw=0.6, alpha=.45,
                                  transform=fig.transFigure, zorder=19))
        fundo = yr
    return fundo - respiro_pol / fig.get_figheight()


def virg(x, casas=1):
    return ("%%.%df" % casas % x).replace(".", ",")


def _hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)])


class Base(object):
    ORDEM = ["B1", "B2", "Erica Novo", "B3", "B4"]

    def __init__(self, pasta=AQUI):
        d = np.load(os.path.join(pasta, "base_terreno.npz"))
        self.Z = d["Z"]
        self.S = d["sombra"]
        self.SEC = d["sector"]
        self.ACUM = d["acum"]
        self.bb = tuple(d["bb"])
        self.pix = float(d["pix"])
        self.meta = json.load(io.open(os.path.join(pasta, "base_sectores.json"),
                                      encoding="utf-8"))
        self.COD = self.meta["codigo"]
        self.areas = self.meta["areas_particao_ha"]
        self.valv = {int(k): v for k, v in self.meta["valvulas"].items()}
        self.ext = (self.bb[0], self.bb[2], self.bb[1], self.bb[3])

    def tem_posicao(self, k):
        v = self.valv[k]
        return (self.bb[0] <= v["E"] <= self.bb[2]
                and self.bb[1] <= v["N"] <= self.bb[3])

    def sem_posicao(self):
        return sorted(k for k in self.valv if not self.tem_posicao(k))

    # ── enquadramento ───────────────────────────────────────────────────────
    def figura(self, larg=16.0, legenda=True, cabecalho=1.88, rodape=0.42):
        """A folha. `cabecalho` em polegadas.

        1,88 pol é o que a banda precisa: margem (0,21) + bloco da identidade
        (0,41) + respiro (0,42) + título (0,35) + subtítulo (0,18) + ar até à
        moldura (0,15). Com 1,62 o subtítulo da P11 ficava cortado pelo mapa —
        o respiro maior empurrou-o para dentro da moldura.
        """
        rl = 0.225 if legenda else 0.0
        w = 0.955 - rl - 0.035
        mapa = larg * w / ((self.bb[2] - self.bb[0]) / (self.bb[3] - self.bb[1]))
        alt = mapa + cabecalho + rodape
        self._cabecalho, self._alt = cabecalho, alt
        fig = plt.figure(figsize=(larg, alt))
        ax = fig.add_axes([0.035, rodape / alt, w, mapa / alt])
        ax.set_xlim(self.bb[0], self.bb[2])
        ax.set_ylim(self.bb[1], self.bb[3])
        ax.set_aspect("equal")
        ax.set_facecolor(PAPEL)
        axl = (fig.add_axes([0.035 + w + 0.022, rodape / alt, rl - 0.022, mapa / alt])
               if legenda else None)
        if axl is not None:
            axl.set_xlim(0, 1)
            axl.set_ylim(0, 1)
            axl.axis("off")
        return fig, ax, axl

    # ── camadas ─────────────────────────────────────────────────────────────
    def terreno(self, ax, curvas=True, escoamento=True):
        Z, S = self.Z, self.S
        val = np.array([r[0] for r in RAMPA])
        cols = np.array([_hex2rgb(r[1]) for r in RAMPA])
        Zc = np.clip(np.nan_to_num(Z, nan=val[0]), val[0], val[-1])
        rgb = np.stack([np.interp(Zc, val, cols[:, i]) for i in range(3)], -1)
        rgb = np.clip(rgb * (0.60 + 0.58 * S)[..., None], 0, 1)
        alfa = np.where(np.isfinite(Z), 1.0, 0.0)
        ax.imshow(np.dstack([rgb, alfa]), extent=self.ext, origin="upper",
                  interpolation="bilinear", zorder=1)

        # sem cobertura: tramado leve, para nao se ler como terreno plano
        nod = ~np.isfinite(Z)
        if nod.any():
            ax.contourf(np.flipud(nod.astype(float)), levels=[0.5, 1.5],
                        extent=self.ext, colors="none", hatches=["////"],
                        zorder=2)
            for c in ax.collections[-1:]:
                c.set_edgecolor("#CFC9BC")
                c.set_linewidth(0.0)

        if curvas:
            Zs = ndimage.gaussian_filter(np.nan_to_num(Z, nan=np.nanmedian(Z)), 6)
            Zs[nod] = np.nan
            X = np.linspace(self.bb[0], self.bb[2], Z.shape[1])
            Y = np.linspace(self.bb[3], self.bb[1], Z.shape[0])
            baixo = np.where(Zs < 15, Zs, np.nan)
            cs = ax.contour(X, Y, baixo, levels=np.arange(3, 15, 1.0),
                            colors=CURVA, linewidths=0.45, zorder=3)
            ax.clabel(cs, levels=[4, 6, 8, 10, 12], fmt="%d", fontsize=6.2,
                      colors=CURVA, inline_spacing=6)
            alto = np.where(Zs >= 14, Zs, np.nan)
            cs2 = ax.contour(X, Y, alto, levels=np.arange(20, 180, 20.0),
                             colors=CURVA_ALTA, linewidths=0.55, zorder=3)
            ax.clabel(cs2, fmt="%d", fontsize=6.2, colors=CURVA_ALTA,
                      inline_spacing=6)

        # Escoamento. Os limiares sao altos e o leito e excluido de proposito:
        # a varzea e plana, a acumulacao espalha-se por ela, e com um limiar
        # baixo a camada pinta 3 % da carta e le-se como agua parada — que e o
        # contrario do que mede. So o que ja e canal aparece.
        if escoamento and self.ACUM.shape == self.Z.shape:
            m2 = self.pix * self.pix
            seco = np.isfinite(self.Z) & (self.Z >= NIVEL_AGUA)
            for lim, al in ((50000 / m2, 0.50), (200000 / m2, 0.85)):
                M = np.ma.masked_where(~((self.ACUM >= lim) & seco),
                                       np.ones_like(self.ACUM))
                ax.imshow(M, extent=self.ext, origin="upper", zorder=4,
                          cmap=mpl.colors.ListedColormap([AGUA]), alpha=al,
                          interpolation="nearest")
        return ax

    def cadastro(self, ax, cor="#6E675C", lw=0.4):
        for chave in ("banda", "b1"):
            pass
        try:
            from shapely.geometry import shape
            for chave in ("b1", "banda"):
                g = shape(self.meta[chave])
                gs = g.geoms if g.geom_type == "MultiPolygon" else [g]
                for p in gs:
                    ax.add_patch(MplPoly(np.array(p.exterior.coords), closed=True,
                                         facecolor="none", edgecolor=cor,
                                         linewidth=lw, zorder=5, alpha=0.55))
        except Exception:
            pass
        return ax

    def sectores(self, ax, alfa=0.42, contorno=True):
        X = np.linspace(self.bb[0], self.bb[2], self.Z.shape[1])
        Y = np.linspace(self.bb[3], self.bb[1], self.Z.shape[0])
        for b in self.ORDEM:
            m = (self.SEC == self.COD[b])
            if not m.any():
                continue
            cm = mpl.colors.ListedColormap([COR[b]])
            ax.imshow(np.ma.masked_where(~m, np.ones_like(m, float)),
                      extent=self.ext, origin="upper", cmap=cm, alpha=alfa,
                      zorder=6, interpolation="nearest")
            if contorno:
                ms = ndimage.binary_closing(m, np.ones((5, 5)))
                ax.contour(X, Y, ms.astype(float), levels=[0.5], colors=PAPEL,
                           linewidths=2.6, zorder=7)
                ax.contour(X, Y, ms.astype(float), levels=[0.5], colors=[COR[b]],
                           linewidths=1.3, zorder=8)
        return ax

    def valvulas(self, ax, numeros=True):
        """So as que tem posicao. As 1 a 5 NAO se desenham.

        O gestor diz que o B1 sao as valvulas 1 a 5. A reconstrucao do esquema
        de rega poe-nas 365 a 555 m a OESTE do B1 — fora das parcelas dele. O
        proprio `valvulas_1a5.json` ja o dizia: o lobo oeste tem numeracao
        propria e as ancoras do desenho nao o alcancam. Desenha-las seria pôr
        na carta-base uma posicao que o processo sabe estar errada.
        """
        for k in sorted(self.valv):
            v = self.valv[k]
            if not self.tem_posicao(k):
                continue
            ax.plot(v["E"], v["N"], "o", ms=6.2, mfc=COR[v["bloco"]],
                    mec=PAPEL, mew=1.3, zorder=10)
            if numeros:
                ax.annotate(str(k), (v["E"], v["N"]), xytext=(0, 8.5),
                            textcoords="offset points", ha="center", va="bottom",
                            fontsize=6.6, weight="bold", color=TINTA,
                            path_effects=_halo(2.4), zorder=11)
        return ax

    def rotulos(self, ax, area=False):
        for b in self.ORDEM:
            m = (self.SEC == self.COD[b])
            if not m.any():
                continue
            # ponto mais interior, nao centroide: o centroide de um sector
            # estreito cai em cima do bordo e o rotulo colide com a valvula.
            dt = ndimage.distance_transform_edt(m)
            iy, ix = np.unravel_index(np.argmax(dt), dt.shape)
            E = self.bb[0] + (ix + .5) * self.pix
            N = self.bb[3] - (iy + .5) * self.pix
            # sector estreito -> nome em duas linhas, senao o rotulo transborda
            # para o sector do lado e le-se como se fosse dele.
            largo = 2 * dt.max() * self.pix
            t = b if largo > 11 * len(b) else b.replace(" ", chr(10))
            if area:
                t += "  %s ha" % virg(self.areas[b])
            ax.annotate(t, (E, N), ha="center", va="center",
                        fontsize=13.5 if b != "Erica Novo" else 12,
                        weight="bold", color=TINTA, linespacing=1.25,
                        path_effects=_halo(4.2), zorder=12)
        return ax

    def toponimos(self, ax):
        """O rio e o vazio da outra margem.

        Identificacao: a mancha continua abaixo de 2,5 m (59,8 ha na caixa,
        centro em 8,634 W / 42,046 N) e, imediatamente a noroeste dela, o
        limite da cobertura LiDAR nacional. Sao dois indicadores de origem
        diferente a coincidir — a cota e a fronteira do voo — e e assim que
        esta identificacao se sustenta; nenhum deles sozinho bastava.
        """
        agua = np.isfinite(self.Z) & (self.Z < NIVEL_AGUA)
        agua = ndimage.binary_opening(agua, np.ones((9, 9)))
        if agua.sum() > 5000:
            ys, xs = np.nonzero(agua)
            E = self.bb[0] + xs * self.pix
            N = self.bb[3] - ys * self.pix
            u = np.linalg.svd(np.column_stack([E - E.mean(), N - N.mean()])
                              [::37], full_matrices=False)[2][0]
            ang = np.degrees(np.arctan2(u[1], u[0]))
            ang = ang + 180 if ang < -90 else (ang - 180 if ang > 90 else ang)
            k = np.argsort(N)[int(.80 * len(N))]
            ax.annotate("RIO MINHO", (E[k], N[k]), ha="center", va="center",
                        rotation=ang, rotation_mode="anchor", fontsize=11.5,
                        color="#2E6076", weight="bold", alpha=.85,
                        path_effects=_halo(3.2), zorder=13)
        nod = ~np.isfinite(self.Z)
        if nod.sum() > 20000:
            lab = ndimage.label(nod)[0]
            maior = np.argmax(np.bincount(lab.ravel())[1:]) + 1
            ys, xs = np.nonzero(lab == maior)
            ax.annotate("sem cobertura MDT" + chr(10) + "(outra margem)",
                        (self.bb[0] + np.median(xs) * self.pix,
                         self.bb[3] - np.median(ys) * self.pix),
                        ha="center", va="center", fontsize=8.2, color=TINTA3,
                        linespacing=1.4, path_effects=_halo(3.0), zorder=13)
        return ax

    # ── moldura ─────────────────────────────────────────────────────────────
    def moldura(self, ax, passo=250):
        x0, x1, y0, y1 = self.ext
        xt = np.arange(np.ceil(x0 / passo) * passo, x1, passo)
        yt = np.arange(np.ceil(y0 / passo) * passo, y1, passo)
        ax.set_xticks(xt)
        ax.set_yticks(yt)
        ax.set_xticklabels(["%d" % v for v in xt], fontsize=6.8, color=TINTA3)
        ax.set_yticklabels(["%d" % v for v in yt], fontsize=6.8, color=TINTA3,
                           rotation=90, va="center")
        ax.tick_params(length=3, width=0.6, color=TINTA2, pad=2)
        for v in xt:
            ax.axvline(v, color=TINTA3, lw=0.25, alpha=0.30, zorder=9)
        for v in yt:
            ax.axhline(v, color=TINTA3, lw=0.25, alpha=0.30, zorder=9)
        for s in ax.spines.values():
            s.set_color(TINTA2)
            s.set_linewidth(0.9)
        self._escala(ax)
        self._norte(ax)
        return ax

    def _escala(self, ax, comp=500.0):
        x0, x1, y0, y1 = self.ext
        bx = x0 + 0.035 * (x1 - x0)
        by = y0 + 0.042 * (y1 - y0)
        h = 0.0075 * (y1 - y0)
        ax.add_patch(Rectangle((bx - 24, by - h * 1.5), comp + 66, h * 5.4,
                               facecolor=PAPEL, edgecolor="none", alpha=0.86,
                               zorder=14))
        for i in range(4):
            ax.add_patch(Rectangle((bx + i * comp / 4, by), comp / 4, h,
                                   facecolor=TINTA if i % 2 == 0 else PAPEL,
                                   edgecolor=TINTA, linewidth=0.6, zorder=15))
        for i, lab in ((0, "0"), (2, "250"), (4, "500 m")):
            ax.annotate(lab, (bx + i * comp / 4, by + h * 1.5), ha="center",
                        va="bottom", fontsize=6.8, color=TINTA, zorder=16)
        return ax

    def _norte(self, ax):
        x0, x1, y0, y1 = self.ext
        cx = x1 - 0.042 * (x1 - x0)
        cy = y1 - 0.075 * (y1 - y0)
        L = 0.045 * (y1 - y0)
        ax.add_patch(FancyArrow(cx, cy - L / 2, 0, L, width=L * 0.045,
                                head_width=L * 0.26, head_length=L * 0.34,
                                length_includes_head=True, facecolor=TINTA,
                                edgecolor=PAPEL, linewidth=0.8, zorder=15))
        ax.annotate("N", (cx, cy + L / 2 + L * 0.10), ha="center", va="bottom",
                    fontsize=9.5, weight="bold", color=TINTA,
                    path_effects=_halo(2.6), zorder=16)
        return ax

    # ── legenda ─────────────────────────────────────────────────────────────
    def legenda(self, axl, extra=None, nota=""):
        y = 0.985
        sw, sh, gap = 0.155, 0.030, 0.0125

        def titulo(t, y):
            axl.annotate(t.upper(), (0, y), xycoords="axes fraction",
                         ha="left", va="top", fontsize=7.6, weight="bold",
                         color=TINTA2, annotation_clip=False)
            return y - 0.028

        def linha(y, corr, txt, sub="", hatch=None, alfa=1.0, lw=0.0, lc=None):
            axl.add_patch(Rectangle((0, y - sh), sw, sh, transform=axl.transAxes,
                                    facecolor=corr, alpha=alfa, hatch=hatch,
                                    edgecolor=lc or "none", linewidth=lw,
                                    clip_on=False))
            axl.annotate(txt, (sw + 0.055, y - sh * 0.42), xycoords="axes fraction",
                         ha="left", va="center", fontsize=8.4, color=TINTA,
                         annotation_clip=False)
            if sub:
                axl.annotate(sub, (sw + 0.055, y - sh * 1.05),
                             xycoords="axes fraction", ha="left", va="center",
                             fontsize=6.9, color=TINTA3, annotation_clip=False)
            return y - sh - (gap + 0.012 if sub else gap)

        def glifo_linha(y, corr, txt, sub="", lw=1.2):
            yy = y - sh * 0.5
            axl.plot([0.012, sw - 0.012], [yy, yy], color=corr, lw=lw,
                     transform=axl.transAxes, clip_on=False, solid_capstyle="round")
            axl.annotate(txt, (sw + 0.055, yy), xycoords="axes fraction",
                         ha="left", va="center", fontsize=8.4, color=TINTA,
                         annotation_clip=False)
            if sub:
                axl.annotate(sub, (sw + 0.055, y - sh * 1.05),
                             xycoords="axes fraction", ha="left", va="center",
                             fontsize=6.9, color=TINTA3, annotation_clip=False)
            return y - sh - (gap + 0.012 if sub else gap)

        y = titulo("Sectores  ·  nomes do gestor", y)
        for b in self.ORDEM:
            vs = sorted(k for k, v in self.valv.items() if v["bloco"] == b)
            y = linha(y, COR[b], "%s   %s ha" % (b, virg(self.areas[b])),
                      "válvulas %s" % ("%d–%d" % (vs[0], vs[-1]) if len(vs) > 1
                                       else str(vs[0])), alfa=0.55,
                      lw=1.1, lc=COR[b])
        y -= 0.012

        y = titulo("Terreno", y)
        grad = np.linspace(0, 1, 256)[None, :]
        axl.imshow(grad, extent=(0, sw, y - sh, y), aspect="auto",
                   cmap=mpl.colors.LinearSegmentedColormap.from_list(
                       "h", [r[1] for r in RAMPA]), transform=axl.transAxes,
                   clip_on=False, zorder=3)
        axl.annotate("cota  0 → 155 m", (sw + 0.055, y - sh * 0.5),
                     xycoords="axes fraction", ha="left", va="center",
                     fontsize=8.4, color=TINTA, annotation_clip=False)
        axl.annotate("os sectores estão todos entre 5 e 9 m",
                     (sw + 0.055, y - sh * 1.12), xycoords="axes fraction",
                     ha="left", va="center", fontsize=6.9, color=TINTA3,
                     annotation_clip=False)
        y -= sh + gap + 0.014
        y = glifo_linha(y, CURVA, "curvas de nível",
                        "1 m até 15 m · 20 m acima")
        y = linha(y, AGUA, "linhas de escoamento",
                  "acumulação ≥ 5 ha (fina) e ≥ 20 ha (grossa)", alfa=0.8)
        y = linha(y, "none", "sem cobertura MDT", "fora do voo LiDAR da DGT",
                  hatch="////", lw=0.0, lc="#CFC9BC")
        y -= 0.010

        y = titulo("Símbolos", y)
        y = glifo_linha(y, "#6E675C", "limite de parcela (IFAP)",
                        "cultura 124 · KIWI", lw=0.9)
        # A nota «válvulas 1-5: posição por determinar» saiu da legenda em
        # 05-09. É uma lacuna NOSSA anotada numa carta que vai para fora, e a
        # carta afirma o que sabe — não confessa o que não sabe. A razão vive
        # no FIGURAS_ABSTRACTS.md e a pergunta vive no email.

        for e in (extra or []):
            y = linha(y, e.get("cor", "none"), e["texto"], e.get("sub", ""),
                      hatch=e.get("hatch"), alfa=e.get("alfa", 1.0),
                      lw=e.get("lw", 0.0), lc=e.get("lc"))

        if nota:
            # a unidade responsável vai aqui, antes das fontes: é proveniência
            # administrativa, não identidade de folha
            nota = "Unidade responsável   %s\n\n%s" % (UNIDADE_RODAPE, nota)
            axl.annotate(nota, (0, 0.005), xycoords="axes fraction", ha="left",
                         va="bottom", color=TINTA3, annotation_clip=False,
                         **MARGINALIA)
        return axl
