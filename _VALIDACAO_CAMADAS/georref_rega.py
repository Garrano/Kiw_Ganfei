# -*- coding: utf-8 -*-
"""Georreferencia o esquema de rega por AJUSTE DE FORMA, e testa-o às cegas.

Critério em `PRE_REGISTO_ESCALA_REGA.md`, escrito antes desta corrida.

PORQUE NÃO SE ESCOLHEM PONTOS À MÃO
------------------------------------
A tentativa anterior calibrou por **contagem de fileiras** e extrapolou o lobo
«pela geometria relativa do desenho». Deu uma escala inflada 25,4 % e pôs as
válvulas 1-5 a 662 m do sítio. Escolher vértices à vista é a forma G — leitura
de um só leitor, sem guarda mecânica, e é a única forma que continua aberta.

Aqui a transformação sai de **todos os píxeis coloridos ao mesmo tempo**: a
mancha dos sectores no desenho contra o polígono do parcelário IFAP. Não há
ponto escolhido, logo não há ponto escolhido depois de se ver o resíduo.

A CEGUEIRA
----------
O ajuste usa **só o corpo principal** — a componente ligada maior da mancha,
contra o polígono `banda`. **O lobo oeste não entra.** Depois a transformação,
já fixada, é aplicada ao lobo e o resultado é confrontado com o polígono `b1`
do IFAP, que não tocou no ajuste. É esse o teste com poder.
"""
import io
import json
import math
import os
import sys


import numpy as np
from PIL import Image
from scipy import ndimage, optimize

AQUI = os.path.dirname(os.path.abspath(__file__))
DL = r"C:/Users/Jackster2/Downloads"
SCAN = os.path.join(DL, "_esquema_rega", "scan.jpeg")
BASE = os.path.join(DL, "ganfei_s2", "figuras", "base", "base_sectores.json")

# escala declarada, derivada só de metadados do ficheiro (ver pré-registo §2)
RED_A1_A4 = 1.0 / (2 * math.sqrt(2))
ESC_PAG = 3500.0 / RED_A1_A4                 # 1:9899 na página A4
M_POR_PX = (25.4 / 200.0) * ESC_PAG / 1000.0  # imagem embebida = 200 dpi
TOL_ESCALA = 0.03


def mancha_sectores(caminho):
    """Máscara dos sectores coloridos. Papel é branco, escrita é escura."""
    im = np.asarray(Image.open(caminho).convert("RGB")).astype(np.int16)
    mx, mn = im.max(2), im.min(2)
    sat = mx - mn                       # saturação bruta
    claro = mx > 110                    # exclui traço e escrita escura
    # pastel: saturado o suficiente para não ser papel, claro o suficiente
    # para não ser caneta
    m = (sat > 18) & (sat < 150) & claro
    # a metade de baixo é anotação manuscrita, cartela e legenda
    m[int(m.shape[0] * 0.46):, :] = False
    m[:, int(m.shape[1] * 0.93):] = False
    m = ndimage.binary_opening(m, np.ones((3, 3)))
    # CORRIDA 1 usava fecho 9x9 e partiu a mancha em 11 componentes: os
    # sectores estao separados por traco preto e papel branco, e a «componente
    # maior» era UM sector, nao o corpo. Tudo o que veio a seguir media uma
    # coisa sem sentido. O fecho tem de ser maior que a espessura do traco e
    # muito menor que o vao entre o corpo e o lobo:
    #   traco entre sectores  ~  3 a 8 px
    #   vao corpo <-> lobo    ~  300 px (parcelas nao coloridas pelo meio)
    # 21 px = 26 m no terreno. Fica no meio, por duas ordens de grandeza.
    m = ndimage.binary_closing(m, np.ones((21, 21)))
    m = ndimage.binary_fill_holes(m)
    return m


def componentes(m, minimo=1500):
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    tam = ndimage.sum(m, lab, range(1, n + 1))
    ordem = np.argsort(tam)[::-1]
    return [(lab == (i + 1)) for i in ordem if tam[i] >= minimo], tam[ordem]


# O objectivo é a DISTÂNCIA ENTRE CONTORNOS, e não sobreposição de área.
# Rasterizar o polígono na grelha inteira custava 3,9 M testes de contenção por
# iteração e não acabava. O contorno dá o mesmo ajuste — quatro parâmetros — a
# custo comportável, e é o que a literatura de registo de imagem usa (ICP).

def contorno(m, n=1400):
    """Amostra de pontos do CONTORNO da mancha, em píxeis."""
    b = m & ~ndimage.binary_erosion(m, np.ones((3, 3)))
    ys, xs = np.nonzero(b)
    if len(xs) > n:
        i = np.linspace(0, len(xs) - 1, n).astype(int)
        xs, ys = xs[i], ys[i]
    return np.column_stack([xs, ys]).astype(float)


def densifica(polys, passo=4.0):
    """Vértices do polígono densificados, em UTM, para a árvore de vizinhos."""
    saida = []
    for poly in polys:
        for ring in poly:
            r = np.asarray(ring, float)
            for a, bb in zip(r[:-1], r[1:]):
                d = math.hypot(*(bb - a))
                k = max(int(d / passo), 1)
                for j in range(k):
                    saida.append(a + (bb - a) * (j / float(k)))
    return np.asarray(saida)


def px_para_utm(pts, s, ang, tx, ty):
    """px -> UTM:  E = tx + s(x·cos − y·sin) ; N = ty − s(x·sin + y·cos)"""
    ca, sa = math.cos(ang), math.sin(ang)
    x, y = pts[:, 0], pts[:, 1]
    return np.column_stack([tx + s * (x * ca - y * sa),
                            ty - s * (x * sa + y * ca)])


def momentos(m):
    ys, xs = np.nonzero(m)
    cx, cy = xs.mean(), ys.mean()
    u = np.cov(np.vstack([xs - cx, ys - cy]))
    val, vec = np.linalg.eigh(u)
    eixo = vec[:, np.argmax(val)]
    return cx, cy, math.atan2(eixo[1], eixo[0]), m.sum()


def momentos_poly(polys):
    pts = np.vstack([np.asarray(r) for p in polys for r in p])
    c = pts.mean(0)
    u = np.cov((pts - c).T)
    val, vec = np.linalg.eigh(u)
    eixo = vec[:, np.argmax(val)]
    return c[0], c[1], math.atan2(eixo[1], eixo[0])


def area_poly(polys):
    a = 0.0
    for p in polys:
        for i, r in enumerate(p):
            x = np.asarray(r)
            s = 0.5 * abs(np.dot(x[:, 0], np.roll(x[:, 1], 1))
                          - np.dot(x[:, 1], np.roll(x[:, 0], 1)))
            a += s if i == 0 else -s
    return a


def main():
    meta = json.load(io.open(BASE, encoding="utf-8"))
    banda = meta["banda"]["coordinates"]
    b1 = meta["b1"]["coordinates"]

    m = mancha_sectores(SCAN)
    comps, tam = componentes(m)
    print("mancha: %d px em %d componentes (>=1500 px)" % (m.sum(), len(comps)))
    print("  tamanhos:", [int(t) for t in tam[:6]])
    if len(comps) < 2:
        print("PARA: a mancha não separa corpo de lobo — a cegueira do "
              "pré-registo §4 não pode ser garantida.")
        return 1

    corpo = comps[0]
    print("corpo  = componente maior, %d px" % corpo.sum())

    # ── ESTIMATIVA DE ESCALA SÓ POR ÁREA. Independente de qualquer ajuste.
    A_banda = area_poly(banda)
    s_area = math.sqrt(A_banda / corpo.sum())
    print()
    print("area do poligono `banda` (IFAP) : %.0f m2" % A_banda)
    print("escala so por area              : %.4f m/px" % s_area)
    print("escala declarada (metadados)    : %.4f m/px" % M_POR_PX)
    print("  desvio                        : %+.1f %%"
          % (100 * (s_area / M_POR_PX - 1)))

    # ── inicialização por momentos, refinamento por IoU
    cx, cy, ang_i, _ = momentos(corpo)
    ex, ey, ang_p = momentos_poly(banda)

    from scipy.spatial import cKDTree
    C = contorno(corpo)
    Ref = densifica(banda)
    arvore = cKDTree(Ref)
    arv_c = None

    def de(p):
        s, ang, tx, ty = p
        if not (0.5 * M_POR_PX < s < 2.0 * M_POR_PX):
            return 1e9
        q = px_para_utm(C, s, ang, tx, ty)
        d1, _ = arvore.query(q)
        d2, _ = arv_c.query(Ref) if arv_c is not None else (np.zeros(1), None)
        return float(np.sqrt((d1 ** 2).mean()))

    melhor, mp = None, None
    for volta in (0.0, math.pi):
        ang = ang_p - ang_i + volta
        ca, sa = math.cos(ang), math.sin(ang)
        tx = ex - M_POR_PX * (cx * ca - cy * sa)
        ty = ey + M_POR_PX * (cx * sa + cy * ca)
        p0 = np.array([M_POR_PX, ang, tx, ty])
        r = optimize.minimize(de, p0, method="Nelder-Mead",
                              options=dict(maxiter=1200, xatol=1e-4,
                                           fatol=1e-5))
        if melhor is None or r.fun < melhor:
            melhor, mp = r.fun, r.x

    s, ang, tx, ty = mp
    print()
    print("AJUSTE (só o corpo):")
    print("  RMS contorno     %.1f m" % melhor)
    print("  escala           %.4f m/px   (%+.1f %% face à declarada)"
          % (s, 100 * (s / M_POR_PX - 1)))
    print("  rotação          %.2f graus" % math.degrees(ang))

    # ── TESTE CEGO: o lobo, que não entrou em nada
    lobo = comps[1]
    ys, xs = np.nonzero(lobo)
    ca, sa = math.cos(ang), math.sin(ang)
    E = tx + s * (xs * ca - ys * sa)
    N = ty - s * (xs * sa + ys * ca)
    from matplotlib.path import Path
    dentro = np.zeros(len(E), bool)
    for p in b1:
        for r_ in p:
            dentro |= Path(np.asarray(r_)).contains_points(
                np.column_stack([E, N]))
    print()
    print("TESTE CEGO — o lobo projectado contra o polígono B1 do IFAP:")
    print("  lobo             %d px  ->  %.2f ha" % (lobo.sum(),
                                                     lobo.sum() * s * s / 1e4))
    print("  B1 (IFAP)        %.2f ha" % (area_poly(b1) / 1e4))
    print("  fracção do lobo que cai DENTRO do B1 : %.1f %%"
          % (100.0 * dentro.mean()))
    cxl, cyl = E.mean(), N.mean()
    pb = np.vstack([np.asarray(r_) for p in b1 for r_ in p])
    d = math.hypot(cxl - pb[:, 0].mean(), cyl - pb[:, 1].mean())
    print("  distância entre centróides           : %.0f m" % d)

    json.dump(dict(escala_m_px=s, rotacao_rad=ang, tx=tx, ty=ty,
                   rms_contorno_m=melhor, escala_declarada=M_POR_PX,
                   escala_so_area=s_area,
                   lobo_dentro_b1_frac=float(dentro.mean()),
                   lobo_dist_centroides_m=d),
              io.open(os.path.join(AQUI, "georref_rega.json"), "w",
                      encoding="utf-8"), indent=1)
    print()
    print("escrito georref_rega.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
