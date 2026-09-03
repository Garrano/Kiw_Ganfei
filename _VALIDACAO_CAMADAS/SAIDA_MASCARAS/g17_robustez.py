# -*- coding: utf-8 -*-
"""G17 — o resultado depende do desenho da grelha de referencia?

A referencia sistematica e uma grelha; uma grelha tem passo e tem fase. Se o
declive da referencia mudasse de sinal ao mudar o passo ou a fase, o resultado
nao valia nada. Testam-se passos de 20, 30 e 40 m e todas as fases possiveis,
mais a alternativa sem grelha nenhuma (a mediana do pomar inteiro).
"""
import os
import json
import glob
import numpy as np
import rasterio
from scipy import ndimage, stats
from matplotlib.path import Path as MP

SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
PLENA = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    fich = sorted(glob.glob(os.path.join(GAN, "sentinel", "*.tif")))
    datas = [os.path.basename(f)[:10] for f in fich]
    nd = np.stack([rasterio.open(f).read(1).astype("float64") for f in fich])
    ip = [i for i, d in enumerate(datas) if d in PLENA]
    x = np.array([int(datas[i][:4]) + (int(datas[i][5:7]) - 1) / 12 for i in ip])

    p2012 = np.load(os.path.join(SAI, "pomar_2012.npy"))
    pomar = np.load(os.path.join(SAI, "pomar.npy"))
    interior = ndimage.binary_erosion(p2012, np.ones((5, 5)))

    print("declive do NDVI da referencia, 9 cenas de plena estacao")
    print(" passo  fase   celulas    ha   declive/ano       p      NDVI2017  NDVI2026")
    tudo = []
    for passo in (2, 3, 4):
        for fi in range(passo):
            for fj in range(passo):
                ref = np.zeros_like(pomar)
                ref[fi::passo, fj::passo] = True
                ref &= interior
                if ref.sum() < 40:
                    continue
                y = np.array([np.nanmean(nd[i][ref]) for i in ip])
                s = stats.linregress(x, y)
                tudo.append(s.slope)
                print("  %2d m   %d,%d   %5d  %5.2f   %+.5f   %7.4f   %.4f   %.4f"
                      % (passo * 10, fi, fj, ref.sum(), ref.sum() / 100, s.slope,
                         s.pvalue, np.nanmean(nd[ip[0]][ref]), np.nanmean(nd[ip[-1]][ref])))
    tudo = np.array(tudo)
    print("\n  %d desenhos de grelha: declive de %+.5f a %+.5f, mediana %+.5f"
          % (len(tudo), tudo.min(), tudo.max(), np.median(tudo)))
    print("  desenhos com declive NEGATIVO: %d de %d" % ((tudo < 0).sum(), len(tudo)))

    # alternativas sem grelha
    print("\nalternativas a grelha:")
    for nome, m, f in (("mediana do pomar inteiro", pomar, np.nanmedian),
                       ("mediana do pomar_2012", p2012, np.nanmedian),
                       ("media do pomar inteiro", pomar, np.nanmean),
                       ("percentil 75 do pomar", pomar, lambda v: np.nanpercentile(v, 75))):
        y = np.array([f(nd[i][m]) for i in ip])
        s = stats.linregress(x, y)
        print("  %-28s %+.5f/ano  p=%.4f   2017 %.4f  2026 %.4f"
              % (nome, s.slope, s.pvalue, y[0], y[-1]))

    # e a antiga, para contraste
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    ra = raster(ant["saudavel"]) | raster(ant["saudavel_2"]) | raster(ant["saudavel_3"])
    y = np.array([np.nanmean(nd[i][ra]) for i in ip])
    s = stats.linregress(x, y)
    print("\n  referencia ANTIGA (escolhida por NDVI alto em 2026): %+.5f/ano p=%.4f"
          % (s.slope, s.pvalue))

    # quantas celulas da referencia caem nas mascaras antigas de mancha
    ref = np.load(os.path.join(SAI, "saudavel.npy"))
    mw, z0 = raster(ant["manchaW"]), raster(ant["zona0"])
    print("\n  da referencia nova (%d celulas): %d em manchaW antiga, %d em zona0 antiga"
          % (ref.sum(), (ref & mw).sum(), (ref & z0).sum()))
