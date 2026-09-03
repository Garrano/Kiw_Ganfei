# -*- coding: utf-8 -*-
"""CTRL-13. Contorno das parcelas, versao final.

Mascara de MATERIAL de cobertura (claro e pouco saturado, R+G+B da ortofoto de
2025 a 25 cm), fecho de `fecho_m` para colar as linhas da mesma parcela sem
saltar as faixas de pousio entre parcelas, abertura, preenchimento de buracos,
contorno exterior e simplificacao de Douglas-Peucker a `tol` metros.

NAO usa banda NIR, NDVI, nem qualquer indice de vegetacao. O criterio e a
presenca de plastico/rede e a geometria — nunca o vigor.

uso: python ctrl_13_contornos.py <nome> <Emin> <Nmin> <Emax> <Nmax>
     <fecho_m> <area_min_ha> [percentil_luz] [tol_m]
"""
import json
import os
import sys
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
RES = 0.5


def dp(pts, tol):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a
    L = float(np.hypot(*ab))
    d = (np.hypot(*(pts - a).T) if L < 1e-9
         else np.abs(np.cross(ab, pts - a)) / L)
    i = int(d.argmax())
    if d[i] <= tol:
        return np.array([a, b])
    return np.vstack([dp(pts[:i + 1], tol)[:-1], dp(pts[i:], tol)])


def area_ha(p):
    x = np.append(p[:, 0], p[0, 0])
    y = np.append(p[:, 1], p[0, 1])
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2.0 / 1e4


def contorno(sel, jan, tol):
    fig = plt.figure()
    cs = plt.contour(sel.astype(float), levels=[0.5],
                     extent=[jan[0], jan[2], jan[1], jan[3]], origin="upper")
    ps = [p.vertices for p in cs.get_paths() if len(p.vertices) > 8]
    plt.close(fig)
    if not ps:
        return None
    v = max(ps, key=lambda a: abs(np.trapezoid(a[:, 1], a[:, 0])))
    o = dp(np.asarray(v, float), tol)
    if not np.allclose(o[0], o[-1]):
        o = np.vstack([o, o[:1]])
    return o


def main(nome, jan, fecho_m, amin, pcl=88.0, tol=4.0):
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        W = int(round((jan[2] - jan[0]) / RES))
        H = int(round((jan[3] - jan[1]) / RES))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, H, W),
                    boundless=True, fill_value=0).astype("float32")
    lum = a.mean(0)
    sat = (a.max(0) - a.min(0)) / np.maximum(a.max(0), 1.0)
    val = lum > 0
    mat = (lum > np.percentile(lum[val], pcl)) & (sat < 0.18) & val
    k = max(3, int(round(fecho_m / RES)))
    g = ndimage.binary_closing(mat, np.ones((k, k)))
    g = ndimage.binary_opening(g, np.ones((max(5, k // 2),) * 2))
    g = ndimage.binary_fill_holes(g)
    lab, n = ndimage.label(g, np.ones((3, 3)))
    saida = []
    for i in range(1, n + 1):
        sel = lab == i
        am = sel.sum() * RES ** 2 / 1e4
        if am < amin:
            continue
        p = contorno(sel, jan, tol)
        if p is None:
            continue
        ap = area_ha(p)
        fm = (mat & sel).sum() * RES ** 2 / 1e4
        print("  parcela %2d: poligono %6.2f ha ; mancha %6.2f ha ; "
              "material %5.2f ha (%.0f%%) ; %d vertices"
              % (i, ap, am, fm, 100 * fm / ap, len(p) - 1))
        saida.append(dict(id=int(i), area_ha=round(float(ap), 2),
                          area_mancha_ha=round(float(am), 2),
                          area_material_ha=round(float(fm), 2),
                          fraccao_material=round(float(fm / ap), 3),
                          vertices=[[round(float(x), 1), round(float(y), 1)]
                                    for x, y in p]))
    tot = sum(s["area_ha"] for s in saida)
    print("%s TOTAL %.2f ha em %d parcelas" % (nome, tot, len(saida)))
    json.dump(dict(nome=nome, janela=list(jan), fecho_m=fecho_m,
                   percentil_luz=pcl, tol_m=tol, total_ha=round(tot, 2),
                   parcelas=saida),
              open(os.path.join(OUT, "ctrl_13_%s.json" % nome), "w"), indent=1)
    rgb = np.clip(np.moveaxis(a, 0, -1)
                  / max(np.percentile(a, 99.3), 1.0), 0, 1)
    fig, ax = plt.subplots(figsize=(17, 17 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=180)
    ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
    for s in saida:
        v = np.array(s["vertices"])
        ax.plot(v[:, 0], v[:, 1], "-", color="red", lw=1.6)
        ax.text(v[:, 0].mean(), v[:, 1].mean(), "%d\n%.2f ha"
                % (s["id"], s["area_ha"]), color="yellow", fontsize=7,
                ha="center", va="center")
    ax.set_title("%s — contorno das parcelas cobertas, ortofoto 2025 "
                 "(%.2f ha)" % (nome, tot), fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_13_%s.png" % nome), bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_13_%s.png" % nome)


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]),
         float(sys.argv[6]), float(sys.argv[7]),
         float(sys.argv[8]) if len(sys.argv) > 8 else 88.0,
         float(sys.argv[9]) if len(sys.argv) > 9 else 4.0)
