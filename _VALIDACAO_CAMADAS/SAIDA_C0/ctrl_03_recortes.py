# -*- coding: utf-8 -*-
"""CTRL-03. Recortes a 25 cm para CONFIRMACAO VISUAL de cada candidato.

Regra: nenhum candidato passa sem ser olhado a resolucao nativa. So R,G,B.
Chamada:  python ctrl_03_recortes.py <nome> <Emin> <Nmin> <Emax> <Nmax> [ano]
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
ANOS = {
    "1995": "ortos1995_cog_1m_irg_jpg_002-3_v01.tif",
    "2004": "ortos20042006_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2007": "ortos2007_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2010": "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2012": "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2021": "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
    "2025": "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif",
}


def recorte(jan, ano="2025", res=0.25, alvo=2600):
    p = os.path.join(BASE, "orto", ANOS[ano])
    with rasterio.open(p) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        r = max(res, max(jan[2] - jan[0], jan[3] - jan[1]) / alvo)
        w = int(round((jan[2] - jan[0]) / r))
        h = int(round((jan[3] - jan[1]) / r))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0)
    rgb = np.moveaxis(a, 0, -1).astype("float32")
    return np.clip(rgb / max(np.percentile(rgb, 99.3), 1.0), 0, 1), r


def desenha(nome, jan, ano="2025", grelha=100):
    rgb, r = recorte(jan, ano)
    fig, ax = plt.subplots(figsize=(16, 16 * (jan[3] - jan[1]) / (jan[2] - jan[0])),
                           dpi=170)
    ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
    for e in range(int(jan[0]) // grelha * grelha, int(jan[2]) + grelha, grelha):
        if jan[0] <= e <= jan[2]:
            ax.axvline(e, color="yellow", lw=0.35, alpha=0.6)
    for n in range(int(jan[1]) // grelha * grelha, int(jan[3]) + grelha, grelha):
        if jan[1] <= n <= jan[3]:
            ax.axhline(n, color="yellow", lw=0.35, alpha=0.6)
    ax.set_title("%s  ortofoto %s  (%.2f m/px)  grelha %d m  EPSG:32629"
                 % (nome, ano, r, grelha), fontsize=9)
    ax.tick_params(labelsize=6)
    f = os.path.join(OUT, "ctrl_03_%s_%s.png" % (nome, ano))
    fig.savefig(f, bbox_inches="tight")
    plt.close(fig)
    print("-> %s   (%.2f m/px)" % (os.path.basename(f), r))


if __name__ == "__main__":
    if len(sys.argv) >= 6:
        desenha(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]),
                sys.argv[6] if len(sys.argv) > 6 else "2025")
    else:
        print("uso: nome Emin Nmin Emax Nmax [ano]")
