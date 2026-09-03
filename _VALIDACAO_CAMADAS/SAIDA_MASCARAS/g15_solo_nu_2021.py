# -*- coding: utf-8 -*-
"""G15 — solo descoberto em 2021 DENTRO do `pomar`, e onde e que ele cai.

G14 procurou a sequencia completa pergola(2010/12) -> nu(2021) -> pergola(2025)
e deu ZERO: a faixa que esta nua em 2021 nao tinha sido detectada com compasso
em 2010 nem em 2012. Nao se pode portanto afirmar que houve arranque.

O que fica, e que e verificavel a olho na ortofoto de 25 cm, e mais simples e
igualmente consequente: ha 2,53 ha dentro do `pomar` que em 2021 — a meio da
serie Sentinel — sao chao lavrado, e que em 2025 tem fiadas cobertas. Seja qual
for a historia anterior, nesses hectares nao havia planta produtiva em 2021.

Esta mascara NAO entra na definicao do `pomar`. Serve para a camada seguinte
poder separar, no mapa de defice, o que e planta em declinio do que e chao.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
LIM = 130.0


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    pomar = np.load(os.path.join(SAI, "pomar.npy"))
    lum21 = np.load(os.path.join(SAI, "orto_2021_10m.npy")).astype("float32")[:3].mean(0)
    nu = pomar & (lum21 > LIM)
    nu = ndimage.binary_opening(nu, np.ones((2, 2)))
    lab, n = ndimage.label(nu, structure=np.ones((3, 3)))
    tam = ndimage.sum(nu, lab, range(1, n + 1))
    nu = np.isin(lab, [k + 1 for k in range(n) if tam[k] >= 6])
    print("solo descoberto em 2021 dentro do `pomar`: %d celulas = %.2f ha (%.1f %% do pomar)"
          % (nu.sum(), nu.sum() / 100, 100 * nu.sum() / pomar.sum()))
    lab, n = ndimage.label(nu, structure=np.ones((3, 3)))
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        print("  talhao %d: %.2f ha  E %.0f-%.0f  N %.0f-%.0f"
              % (k, (lab == k).sum() / 100,
                 AOI[0] + 10 * xs.min(), AOI[0] + 10 * xs.max() + 10,
                 AOI[3] - 10 * ys.max() - 10, AOI[3] - 10 * ys.min()))

    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    z0, mw = raster(ant["zona0"]), raster(ant["manchaW"])
    ref = np.load(os.path.join(SAI, "saudavel.npy"))
    print("\nfraccao de cada mascara que esta descoberta em 2021:")
    for nm, m in (("zona0 antiga", z0), ("manchaW antiga", mw),
                  ("referencia sistematica", ref), ("pomar novo", pomar)):
        print("  %-24s %5.1f %%" % (nm, 100 * (nu & m).sum() / m.sum()))
    np.save(os.path.join(SAI, "nu2021.npy"), nu)

    ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
    fig, axes = plt.subplots(2, 1, figsize=(17, 11), dpi=110)
    for ax, ano in zip(axes, ("2021", "2025")):
        o = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        ax.imshow(np.clip(np.transpose(o[:3], (1, 2, 0)) / 255.0, 0, 1),
                  extent=ext, origin="upper")
        ax.contour(pomar.astype(float), levels=[0.5], colors="yellow", linewidths=1.3,
                   extent=ext, origin="upper")
        ax.contourf(nu.astype(float), levels=[0.5, 1.5], colors=["#ff00ff"], alpha=0.5,
                    extent=ext, origin="upper")
        ax.contour(z0.astype(float), levels=[0.5], colors="#ff3300", linewidths=1.8,
                   extent=ext, origin="upper")
        ax.set_xlim(530100, 531600); ax.set_ylim(4654800, 4655500)
        ax.set_title("%s — magenta: chao lavrado em 2021 dentro do `pomar` (%.2f ha); "
                     "vermelho: `zona0`" % (ano, nu.sum() / 100), fontsize=11)
        ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v15_nu2021.png"), dpi=110)
    plt.close(fig)
    print("-> v15_nu2021.png")
