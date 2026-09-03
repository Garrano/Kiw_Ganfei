# -*- coding: utf-8 -*-
"""CTRL-05. Painel multi-epoca do mesmo recorte (2004, 2007, 2010, 2012,
2021, 2025). Serve para distinguir LATADA (copado continuo que fecha a
entrelinha) de CULTURA EM LINHA / TUNEL (entrelinha sempre visivel).

So R,G,B. Nenhum indice.
uso: python ctrl_05_painel.py <nome> <Emin> <Nmin> <Emax> <Nmax>
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
ANOS = [("2004", "ortos20042006_cog_50cm_rgbi_jpg_002-3_v01.tif"),
        ("2007", "ortos2007_cog_50cm_rgbi_jpg_002-3_v01.tif"),
        ("2010", "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif"),
        ("2012", "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif"),
        ("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"),
        ("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")]


def painel(nome, jan, alvo=1500):
    fig, axs = plt.subplots(2, 3, figsize=(21, 14 * (jan[3] - jan[1])
                                          / (jan[2] - jan[0]) + 1), dpi=145)
    for ax, (ano, fn) in zip(axs.ravel(), ANOS):
        with rasterio.open(os.path.join(BASE, "orto", fn)) as ds:
            jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
            win = from_bounds(*jb, transform=ds.transform)
            r = max(ds.transform.a,
                    max(jan[2] - jan[0], jan[3] - jan[1]) / alvo)
            w = int(round((jan[2] - jan[0]) / r))
            h = int(round((jan[3] - jan[1]) / r))
            a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                        boundless=True, fill_value=0)
        rgb = np.moveaxis(a, 0, -1).astype("float32")
        rgb = np.clip(rgb / max(np.percentile(rgb, 99.3), 1.0), 0, 1)
        ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
        ax.set_title("%s  (%.2f m/px)" % (ano, r), fontsize=9)
        ax.tick_params(labelsize=5)
    fig.suptitle("%s   E %.0f..%.0f  N %.0f..%.0f  EPSG:32629"
                 % (nome, jan[0], jan[2], jan[1], jan[3]), fontsize=11)
    f = os.path.join(OUT, "ctrl_05_painel_%s.png" % nome)
    fig.savefig(f, bbox_inches="tight")
    plt.close(fig)
    print("-> %s" % os.path.basename(f))


if __name__ == "__main__":
    painel(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]))
