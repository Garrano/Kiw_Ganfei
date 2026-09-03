# -*- coding: utf-8 -*-
"""CTRL-12. Parcelas por deteccao do MATERIAL de cobertura (plastico/rede)
na ortofoto de 2025 a 25 cm, e rectangulo de area minima por parcela.

Criterio: pixeis muito claros e pouco saturados — plastico branco e rede.
E um criterio de MATERIAL, nao de vegetacao: nao entra a banda NIR nem
qualquer razao de bandas. Um pomar de latada com a rede recolhida sobre a
linha, um tunel de plastico e uma estufa dao todos sinal aqui; e por isso que
a identificacao da CULTURA se faz depois, a olho, nas epocas com folha.

Cada parcela sai como rectangulo de area minima (as parcelas do aluviao sao
paralelogramos entre caminhos rectos), com a area de Gauss e o grau de
preenchimento pela mascara.

uso: python ctrl_12_parcelas.py <nome> <Emin> <Nmin> <Emax> <Nmax>
     <fecho_m> <area_min_ha>
"""
import json
import os
import sys
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
RES = 0.5


def rect_min(pts):
    """Rectangulo de area minima (calipers rotativos sobre o inveltorio)."""
    h = ConvexHull(pts)
    v = pts[h.vertices]
    melhor = None
    for i in range(len(v)):
        d = v[(i + 1) % len(v)] - v[i]
        ang = np.arctan2(d[1], d[0])
        c, s = np.cos(-ang), np.sin(-ang)
        R = np.array([[c, -s], [s, c]])
        q = v @ R.T
        w = q[:, 0].max() - q[:, 0].min()
        hh = q[:, 1].max() - q[:, 1].min()
        if melhor is None or w * hh < melhor[0]:
            x0, x1 = q[:, 0].min(), q[:, 0].max()
            y0, y1 = q[:, 1].min(), q[:, 1].max()
            cnt = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
            melhor = (w * hh, cnt @ np.linalg.inv(R).T)
    return melhor[1]


def area_ha(p):
    x = np.append(p[:, 0], p[0, 0])
    y = np.append(p[:, 1], p[0, 1])
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2.0 / 1e4


def main(nome, jan, fecho_m, amin):
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        W = int(round((jan[2] - jan[0]) / RES))
        H = int(round((jan[3] - jan[1]) / RES))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, H, W),
                    boundless=True, fill_value=0).astype("float32")
    lum = a.mean(0)
    mx, mn = a.max(0), a.min(0)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    valido = lum > 0
    plast = (lum > np.percentile(lum[valido], 88)) & (sat < 0.18) & valido
    print("%s  pixeis de material claro: %.2f ha"
          % (nome, plast.sum() * RES ** 2 / 1e4))
    k = max(3, int(round(fecho_m / RES)))
    g = ndimage.binary_closing(plast, np.ones((k, k)))
    g = ndimage.binary_opening(g, np.ones((max(3, k // 2),) * 2))
    g = ndimage.binary_fill_holes(g)
    lab, n = ndimage.label(g, np.ones((3, 3)))
    saida = []
    for i in range(1, n + 1):
        sel = lab == i
        acob = sel.sum() * RES ** 2 / 1e4
        if acob < amin:
            continue
        yy, xx = np.where(sel[::4, ::4])
        pts = np.column_stack([jan[0] + (xx * 4 + 0.5) * RES,
                               jan[3] - (yy * 4 + 0.5) * RES])
        r = rect_min(pts)
        ar = area_ha(r)
        estr = (plast & sel).sum() * RES ** 2 / 1e4
        print("  parcela %d: rectangulo %.2f ha ; mancha %.2f ha ; "
              "material %.2f ha (%.0f%% do rectangulo)"
              % (i, ar, acob, estr, 100 * estr / ar))
        saida.append(dict(id=int(i), area_ha_rect=round(float(ar), 2),
                          area_ha_mancha=round(float(acob), 2),
                          area_ha_material=round(float(estr), 2),
                          vertices=[[round(float(x), 1), round(float(y), 1)]
                                    for x, y in r]))
    tot = sum(s["area_ha_rect"] for s in saida)
    print("  TOTAL rectangulos %.2f ha em %d parcelas" % (tot, len(saida)))
    json.dump(dict(nome=nome, janela=list(jan), fecho_m=fecho_m,
                   area_min_ha=amin, total_ha=round(tot, 2), parcelas=saida),
              open(os.path.join(OUT, "ctrl_12_%s.json" % nome), "w"), indent=1)
    rgb = np.moveaxis(a, 0, -1)
    rgb = np.clip(rgb / max(np.percentile(rgb, 99.3), 1.0), 0, 1)
    fig, ax = plt.subplots(figsize=(17, 17 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=180)
    ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
    for s in saida:
        v = np.array(s["vertices"] + s["vertices"][:1])
        ax.plot(v[:, 0], v[:, 1], "-", color="red", lw=1.6)
        ax.text(v[:4, 0].mean(), v[:4, 1].mean(), "%d · %.2f ha"
                % (s["id"], s["area_ha_rect"]), color="yellow", fontsize=7,
                ha="center")
    ax.set_title("%s — parcelas por material de cobertura, ortofoto 2025 "
                 "(%.2f ha)" % (nome, tot), fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_12_%s.png" % nome), bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_12_%s.png" % nome)


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]),
         float(sys.argv[6]), float(sys.argv[7]))
