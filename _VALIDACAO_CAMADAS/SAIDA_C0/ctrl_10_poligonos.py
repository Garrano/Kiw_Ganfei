# -*- coding: utf-8 -*-
"""CTRL-10. Poligonos das parcelas com estrutura, por inveltorio convexo.

As parcelas aqui sao quadrilateros (cabeceiras rectas, caminhos rectos), pelo
que o inveltorio convexo da mascara de estrutura reproduz o limite fisico com
erro pequeno, e cada lado fica associado a um objecto visivel na ortofoto
(caminho, galeria ripicola, cabeceira, estrada).

Entrada: mascara de periodicidade (CTRL-07), a 4 m.
Saida:  ctrl_10_<nome>.json com um poligono por parcela e a area de Gauss.

uso: python ctrl_10_poligonos.py <nome> <Emin> <Nmin> <Emax> <Nmax> <ano>
     <percentil> <une_m> <area_min_ha>
"""
import json
import os
import sys
import numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ctrl_07_delimitar import mapa, RES, STEP

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
PASSO = STEP * RES


def area_ha(p):
    x, y = p[:, 0], p[:, 1]
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2.0 / 1e4


def main(nome, jan, ano, pc, une_m, amin):
    lum, f, ext = mapa(jan, ano)
    lim = np.percentile(f[f > 0], pc)
    m = f >= lim
    m = ndimage.binary_closing(m, np.ones((3, 3)))
    m = ndimage.binary_opening(m, np.ones((3, 3)))
    # une parcelas separadas por menos de une_m (caminhos internos)
    k = max(1, int(round(une_m / PASSO)))
    g = ndimage.binary_closing(m, np.ones((k, k)))
    lab, n = ndimage.label(g, np.ones((3, 3)))
    print("%s %s  p%.0f=%.4f  uniao=%d m  %d grupos" % (nome, ano, pc, lim,
                                                        une_m, n))
    # coordenadas do centro de cada celula do mapa
    ny, nx = f.shape
    xs = ext[0] + np.arange(nx) * PASSO
    ys = ext[3] - np.arange(ny) * PASSO
    saida = []
    for i in range(1, n + 1):
        sel = (lab == i) & m
        if sel.sum() * PASSO ** 2 / 1e4 < amin:
            continue
        yy, xx = np.where(sel)
        pts = np.column_stack([xs[xx], ys[yy]])
        h = ConvexHull(pts)
        pol = pts[h.vertices]
        a = area_ha(pol)
        acob = sel.sum() * PASSO ** 2 / 1e4
        print("  parcela %d: envelope %.2f ha ; celulas com estrutura %.2f ha"
              " (%.0f%% de preenchimento) ; %d vertices"
              % (i, a, acob, 100 * acob / a, len(pol)))
        saida.append(dict(id=int(i), area_ha=round(float(a), 2),
                          area_estrutura_ha=round(float(acob), 2),
                          preenchimento=round(float(acob / a), 3),
                          vertices=[[round(float(x), 1), round(float(y), 1)]
                                    for x, y in pol]))
    tot = sum(s["area_ha"] for s in saida)
    print("  TOTAL %.2f ha em %d parcelas" % (tot, len(saida)))
    json.dump(dict(nome=nome, janela=list(jan), ano=ano, percentil=pc,
                   limiar=float(lim), une_m=une_m, area_min_ha=amin,
                   total_ha=round(tot, 2), parcelas=saida),
              open(os.path.join(OUT, "ctrl_10_%s.json" % nome), "w"), indent=1)

    fig, ax = plt.subplots(figsize=(16, 16 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=175)
    ax.imshow(np.clip(lum / np.percentile(lum, 99) * 0.9, 0, 1),
              extent=[jan[0], jan[2], jan[1], jan[3]], cmap="gray")
    for s in saida:
        v = np.array(s["vertices"] + s["vertices"][:1])
        ax.plot(v[:, 0], v[:, 1], "-", color="red", lw=1.5)
        ax.text(v[:, 0].mean(), v[:, 1].mean(), "%d\n%.2f ha"
                % (s["id"], s["area_ha"]), color="yellow", fontsize=6,
                ha="center", va="center")
    ax.set_title("%s — parcelas com estrutura em linha, ortofoto %s (%.2f ha)"
                 % (nome, ano, tot), fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_10_%s_%s.png" % (nome, ano)),
                bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_10_%s_%s.png" % (nome, ano))


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]), sys.argv[6],
         float(sys.argv[7]), float(sys.argv[8]), float(sys.argv[9]))
