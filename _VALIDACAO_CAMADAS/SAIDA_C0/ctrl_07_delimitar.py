# -*- coding: utf-8 -*-
"""CTRL-07. Delimitacao fina de um bloco pela sua ESTRUTURA.

Mapa de periodicidade linear a passo de 4 m (bloco de 16 m) dentro de uma
janela pequena, limiar, limpeza morfologica, contorno exterior e
simplificacao. O poligono sai da estrutura visivel na ortofoto — nunca de
brilho, cor ou indice.

uso: python ctrl_07_delimitar.py <nome> <Emin> <Nmin> <Emax> <Nmax>
       [ano] [percentil] [area_min_ha]
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
ANOS = {"2012": "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
        "2021": "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
        "2025": "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"}
RES = 0.5
BL = 32          # 16 m
STEP = 8         # 4 m
LMIN, LMAX = 2.5, 9.0


def mapa(jan, ano):
    with rasterio.open(os.path.join(BASE, "orto", ANOS[ano])) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        W = int(round((jan[2] - jan[0]) / RES))
        H = int(round((jan[3] - jan[1]) / RES))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, H, W),
                    boundless=True, fill_value=0)
    lum = a.mean(0).astype("float32")
    fy = np.fft.fftfreq(BL)[:, None]
    fx = np.fft.fftfreq(BL)[None, :]
    fr = np.sqrt(fy ** 2 + fx ** 2)
    with np.errstate(divide="ignore"):
        lam = RES / np.maximum(fr, 1e-9)
    banda = (lam >= LMIN) & (lam <= LMAX)
    fundo = (lam > LMAX) & (lam < 30.0)
    jw = np.outer(np.hanning(BL), np.hanning(BL)).astype("float32")
    ny = (H - BL) // STEP + 1
    nx = (W - BL) // STEP + 1
    f = np.zeros((ny, nx), "float32")
    for i in range(ny):
        for j in range(nx):
            b = lum[i * STEP:i * STEP + BL, j * STEP:j * STEP + BL]
            if b.std() < 3.0:
                continue
            F = np.fft.fft2((b - b.mean()) * jw)
            p = F.real ** 2 + F.imag ** 2
            f[i, j] = (p * banda).max() / (p[fundo].sum() + p[banda].sum() + 1e-9)
    ext = [jan[0] + BL * RES / 2, jan[0] + ((nx - 1) * STEP + BL / 2) * RES,
           jan[3] - ((ny - 1) * STEP + BL / 2) * RES, jan[3] - BL * RES / 2]
    return lum, f, ext


def main(nome, jan, ano="2025", pc=88.0, amin=1.0):
    lum, f, ext = mapa(jan, ano)
    lim = np.percentile(f[f > 0], pc)
    m = f >= lim
    m = ndimage.binary_closing(m, np.ones((7, 7)))
    m = ndimage.binary_opening(m, np.ones((5, 5)))
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m, np.ones((3, 3)))
    cell = (STEP * RES) ** 2
    tam = ndimage.sum(m, lab, range(1, n + 1)) * cell / 1e4
    keep = [i + 1 for i in range(n) if tam[i] >= amin]
    print("%s ano=%s limiar p%.0f=%.4f  %d componentes >= %.1f ha"
          % (nome, ano, pc, lim, len(keep), amin))
    tot = 0.0
    for i in keep:
        print("   componente %d: %.2f ha" % (i, tam[i - 1]))
        tot += tam[i - 1]
    print("   TOTAL %.2f ha" % tot)
    np.save(os.path.join(OUT, "ctrl_07_%s_mask.npy" % nome),
            np.isin(lab, keep))
    json.dump(dict(janela=list(jan), ano=ano, percentil=pc, limiar=float(lim),
                   extent_mapa=[float(x) for x in ext],
                   passo_m=STEP * RES, bloco_m=BL * RES,
                   areas_ha=[float(tam[i - 1]) for i in keep],
                   total_ha=float(tot)),
              open(os.path.join(OUT, "ctrl_07_%s.json" % nome), "w"), indent=1)

    fig, axs = plt.subplots(1, 2, figsize=(24, 12 * (jan[3] - jan[1])
                                           / (jan[2] - jan[0]) + 1), dpi=150)
    for ax in axs:
        ax.imshow(np.clip(lum / np.percentile(lum, 99) * 0.9, 0, 1),
                  extent=[jan[0], jan[2], jan[1], jan[3]], cmap="gray")
        ax.tick_params(labelsize=6)
    axs[1].contour(np.isin(lab, keep), levels=[0.5], colors="red",
                   linewidths=1.2, extent=[ext[0], ext[1], ext[2], ext[3]],
                   origin="upper")
    axs[0].set_title("%s — ortofoto %s (luminancia)" % (nome, ano), fontsize=9)
    axs[1].set_title("contorno da mascara de periodicidade (p%.0f)  %.2f ha"
                     % (pc, tot), fontsize=9)
    fig.savefig(os.path.join(OUT, "ctrl_07_%s_%s.png" % (nome, ano)),
                bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_07_%s_%s.png" % (nome, ano))


if __name__ == "__main__":
    main(sys.argv[1], tuple(float(x) for x in sys.argv[2:6]),
         sys.argv[6] if len(sys.argv) > 6 else "2025",
         float(sys.argv[7]) if len(sys.argv) > 7 else 88.0,
         float(sys.argv[8]) if len(sys.argv) > 8 else 1.0)
