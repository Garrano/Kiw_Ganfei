# -*- coding: utf-8 -*-
"""CTRL-08. Envelope operacional de um bloco: junta as sub-parcelas com
estrutura em linha que estao separadas apenas por caminhos e cabeceiras,
e devolve o contorno simplificado em EPSG:32629.

Parte do mapa de periodicidade de CTRL-07 (estrutura, nunca indice), fecha
a 30 m, abre a 10 m, e fica com as componentes acima de area_min.
Imprime os vertices do contorno para poderem ser conferidos um a um sobre a
ortofoto.

uso: python ctrl_08_envelope.py <nome> <Emin> <Nmin> <Emax> <Nmax> <ano>
     <percentil> <fecho_m> <area_min_ha>
"""
import json
import os
import sys
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ctrl_07_delimitar import mapa, RES, STEP

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
PASSO = STEP * RES        # 4 m por celula do mapa


def anel(mask, ext, tol=6.0):
    """Contorno exterior da mascara, em coordenadas 32629, simplificado."""
    import matplotlib.pyplot as _plt
    fig = _plt.figure()
    cs = _plt.contour(mask.astype(float), levels=[0.5],
                      extent=[ext[0], ext[1], ext[2], ext[3]], origin="upper")
    caminhos = []
    for p in cs.get_paths():
        v = p.vertices
        if len(v) < 4:
            continue
        caminhos.append(v)
    _plt.close(fig)
    if not caminhos:
        return None
    v = max(caminhos, key=lambda a: abs(np.trapezoid(a[:, 1], a[:, 0])))
    return simplifica(v, tol)


def simplifica(v, tol):
    """Douglas-Peucker."""
    def dp(pts):
        if len(pts) < 3:
            return pts
        a, b = pts[0], pts[-1]
        ab = b - a
        L = np.hypot(*ab)
        if L < 1e-9:
            d = np.hypot(*(pts - a).T)
        else:
            d = np.abs(np.cross(ab, pts - a)) / L
        i = int(d.argmax())
        if d[i] <= tol:
            return np.array([a, b])
        return np.vstack([dp(pts[:i + 1])[:-1], dp(pts[i:])])
    fechado = np.allclose(v[0], v[-1])
    out = dp(np.asarray(v, float))
    if fechado and not np.allclose(out[0], out[-1]):
        out = np.vstack([out, out[:1]])
    return out


def area_ha(p):
    x, y = p[:, 0], p[:, 1]
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2.0 / 1e4


def main(nome, jan, ano, pc, fecho_m, amin):
    lum, f, ext = mapa(jan, ano)
    lim = np.percentile(f[f > 0], pc)
    k = max(3, int(round(fecho_m / PASSO)))
    m = f >= lim
    m = ndimage.binary_closing(m, np.ones((k, k)))
    m = ndimage.binary_opening(m, np.ones((max(3, k // 3),) * 2))
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m, np.ones((3, 3)))
    tam = ndimage.sum(m, lab, range(1, n + 1)) * PASSO ** 2 / 1e4
    keep = [i + 1 for i in range(n) if tam[i] >= amin]
    print("%s %s p%.0f=%.4f fecho=%d m  -> %d componentes"
          % (nome, ano, pc, lim, fecho_m, len(keep)))
    saida = []
    for i in keep:
        p = anel(lab == i, ext, tol=6.0)
        if p is None:
            continue
        a = area_ha(p)
        print("  componente %d: %.2f ha (mascara %.2f ha), %d vertices"
              % (i, a, tam[i - 1], len(p)))
        for v in p:
            print("      %.0f %.0f" % (v[0], v[1]))
        saida.append(dict(componente=int(i), area_ha_poligono=float(a),
                          area_ha_mascara=float(tam[i - 1]),
                          vertices=[[round(float(x), 1), round(float(y), 1)]
                                    for x, y in p]))
    json.dump(dict(nome=nome, janela=list(jan), ano=ano, percentil=pc,
                   limiar=float(lim), fecho_m=fecho_m, area_min_ha=amin,
                   passo_m=PASSO, componentes=saida),
              open(os.path.join(OUT, "ctrl_08_%s.json" % nome), "w"), indent=1)
    fig, ax = plt.subplots(figsize=(15, 15 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=170)
    ax.imshow(np.clip(lum / np.percentile(lum, 99) * 0.9, 0, 1),
              extent=[jan[0], jan[2], jan[1], jan[3]], cmap="gray")
    for c in saida:
        v = np.array(c["vertices"])
        ax.plot(v[:, 0], v[:, 1], "-", color="red", lw=1.6)
        ax.plot(v[:, 0], v[:, 1], ".", color="yellow", ms=3)
    for e in range(int(jan[0]) // 100 * 100, int(jan[2]) + 100, 100):
        if jan[0] <= e <= jan[2]:
            ax.axvline(e, color="cyan", lw=0.25, alpha=0.5)
    for nn in range(int(jan[1]) // 100 * 100, int(jan[3]) + 100, 100):
        if jan[1] <= nn <= jan[3]:
            ax.axhline(nn, color="cyan", lw=0.25, alpha=0.5)
    ax.set_title("%s — envelope da estrutura, ortofoto %s" % (nome, ano),
                 fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_08_%s_%s.png" % (nome, ano)),
                bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_08_%s_%s.png" % (nome, ano))


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]), sys.argv[6],
         float(sys.argv[7]), float(sys.argv[8]), float(sys.argv[9]))
