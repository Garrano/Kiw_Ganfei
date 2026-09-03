# -*- coding: utf-8 -*-
"""G14 — onde e que houve ARRANQUE e REPLANTACAO durante a serie.

v12 mostrou que `pomar_novo` (estrutura de compasso nao detectada em 2010/2012)
tem duas origens misturadas: mudanca real de uso e falha do detector quando o
copado fecha e as fiadas deixam de ter contraste. Nao serve como facto.

O que SE consegue estabelecer, e verificar a olho, e um acontecimento muito mais
especifico e muito mais consequente:

    pergola presente em 2010 ou 2012  E  solo nu em 2021  E  pergola em 2025

isto e, talhoes ARRANCADOS entre 2012 e 2021 e REPLANTADOS antes de 2025. Um
talhao assim tem, na serie Sentinel de 2017 a 2026, NDVI baixo por AUSENCIA DE
PLANTA, e depois a subir por CRESCIMENTO — e nada disso e declinio.

O criterio de solo nu usa-se aqui deliberadamente, ao contrario do G08: la
servia para DEFINIR o pomar (e apagava o sinal), aqui serve para MARCAR um
acontecimento dentro do pomar ja definido. Sao usos opostos.
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
LIM_NU = 130.0


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    pomar = np.load(os.path.join(SAI, "pomar.npy"))
    a10 = np.load(os.path.join(SAI, "assin_2010.npy"))
    a12 = np.load(os.path.join(SAI, "assin_2012.npy"))
    a25 = np.load(os.path.join(SAI, "assin_2025.npy"))
    lum21 = np.load(os.path.join(SAI, "orto_2021_10m.npy")).astype("float32")[:3].mean(0)

    nu21 = lum21 > LIM_NU
    arr = pomar & (a10 | a12) & nu21 & a25
    arr = ndimage.binary_opening(arr, np.ones((2, 2)))
    lab, n = ndimage.label(arr, structure=np.ones((3, 3)))
    tam = ndimage.sum(arr, lab, range(1, n + 1))
    arr = np.isin(lab, [k + 1 for k in range(n) if tam[k] >= 8])   # >= 0,08 ha
    print("arranque + replantacao (2012->2021 nu ->2025 pergola): %d celulas = %.2f ha"
          % (arr.sum(), arr.sum() / 100))
    lab, n = ndimage.label(arr, structure=np.ones((3, 3)))
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        print("  talhao %d: %.2f ha  E %.0f-%.0f  N %.0f-%.0f"
              % (k, (lab == k).sum() / 100,
                 AOI[0] + 10 * xs.min(), AOI[0] + 10 * xs.max() + 10,
                 AOI[3] - 10 * ys.max() - 10, AOI[3] - 10 * ys.min()))

    # solo nu em 2021 dentro do pomar, sem exigir o resto (limite superior)
    nu_pomar = pomar & nu21
    print("\ntodo o solo nu de 2021 dentro do `pomar`: %.2f ha (limite superior)"
          % (nu_pomar.sum() / 100))

    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    z0, mw = raster(ant["zona0"]), raster(ant["manchaW"])
    print("\nsobreposicao com as mascaras antigas:")
    print("  zona0   %.1f %% da sua area esta em arranque+replantacao"
          % (100 * (arr & z0).sum() / z0.sum()))
    print("  manchaW %.1f %%" % (100 * (arr & mw).sum() / mw.sum()))
    np.save(os.path.join(SAI, "arranque_replantacao.npy"), arr)

    ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
    fig, axes = plt.subplots(3, 1, figsize=(17, 15), dpi=105)
    for ax, ano in zip(axes, ("2012", "2021", "2025")):
        o = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        ax.imshow(np.clip(np.transpose(o[:3], (1, 2, 0)) / 255.0, 0, 1),
                  extent=ext, origin="upper")
        ax.contour(pomar.astype(float), levels=[0.5], colors="yellow", linewidths=1.3,
                   extent=ext, origin="upper")
        ax.contourf(arr.astype(float), levels=[0.5, 1.5], colors=["#ff00ff"], alpha=0.45,
                    extent=ext, origin="upper")
        ax.contour(z0.astype(float), levels=[0.5], colors="#ff3300", linewidths=1.8,
                   extent=ext, origin="upper")
        ax.set_xlim(530100, 531600); ax.set_ylim(4654800, 4655500)
        ax.set_title("%s — magenta: arrancado entre 2012 e 2021 e replantado antes de "
                     "2025 (%.2f ha); vermelho: zona0" % (ano, arr.sum() / 100), fontsize=11)
        ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v14_arranque.png"), dpi=105)
    plt.close(fig)
    print("-> v14_arranque.png")
