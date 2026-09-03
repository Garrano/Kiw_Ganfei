# -*- coding: utf-8 -*-
"""CTRL-09. Recorte com grelha densa e rotulos, para ler vertices a mao
sobre a ortofoto e dar proveniencia fisica a cada lado do poligono.

uso: python ctrl_09_grelha.py <nome> <Emin> <Nmin> <Emax> <Nmax> <ano> <passo>
"""
import os
import sys
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ANOS = {"2010": "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif",
        "2012": "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
        "2021": "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
        "2025": "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"}


def main(nome, jan, ano, passo):
    with rasterio.open(os.path.join(BASE, "orto", ANOS[ano])) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        r = max(ds.transform.a, max(jan[2] - jan[0], jan[3] - jan[1]) / 3000)
        w = int(round((jan[2] - jan[0]) / r))
        h = int(round((jan[3] - jan[1]) / r))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0)
    rgb = np.moveaxis(a, 0, -1).astype("float32")
    rgb = np.clip(rgb / max(np.percentile(rgb, 99.3), 1.0), 0, 1)
    fig, ax = plt.subplots(figsize=(20, 20 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=180)
    ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
    for e in range(int(np.ceil(jan[0] / passo)) * passo, int(jan[2]) + 1, passo):
        ax.axvline(e, color="yellow", lw=0.4, alpha=0.55)
        ax.text(e + 2, jan[1] + 6, "%d" % e, color="yellow", fontsize=4.5,
                rotation=90, va="bottom")
    for n in range(int(np.ceil(jan[1] / passo)) * passo, int(jan[3]) + 1, passo):
        ax.axhline(n, color="yellow", lw=0.4, alpha=0.55)
        ax.text(jan[0] + 4, n + 2, "%d" % n, color="yellow", fontsize=4.5)
    ax.set_title("%s  ortofoto %s (%.2f m/px)  grelha %d m  EPSG:32629"
                 % (nome, ano, r, passo), fontsize=9)
    ax.tick_params(labelsize=6)
    f = os.path.join(OUT, "ctrl_09_%s_%s.png" % (nome, ano))
    fig.savefig(f, bbox_inches="tight")
    plt.close(fig)
    print("-> %s  (%.2f m/px)" % (os.path.basename(f), r))


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]), sys.argv[6],
         int(sys.argv[7]))
