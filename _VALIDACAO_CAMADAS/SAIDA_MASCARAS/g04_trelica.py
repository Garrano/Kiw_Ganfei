# -*- coding: utf-8 -*-
"""G04 — indice de TRELICA por autocorrelacao, na grelha de analise.

Porque nao a variancia (tentativa 1) nem a fraccao de potencia numa banda (G03):
a variancia local mede so "quanto varia" — sebes, arvores dispersas, caminhos e
telhados variam muito. A fraccao de potencia numa banda larga tambem nao separa,
porque textura aperiodica espalha potencia por toda a banda.

O que distingue mesmo uma pergola: os postes e as fiadas estao numa MALHA
REGULAR. Numa malha, a autocorrelacao normalizada volta a subir a distancia do
compasso. Em textura aperiodica nao volta. Logo:

    treli = max da autocorrelacao normalizada para desfasamentos entre 3 e 9 m

calculada numa janela de 40 x 40 m sobre a luminancia passada a filtro
passa-alto (remocao da media a 15 m, que apaga o gradiente de parcela e a
sombra mas preserva o compasso).

Guarda tambem `lag` (o desfasamento do maximo, em metros) — que deve rondar o
compasso de plantacao — e `ang` (a direccao desse maximo).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
RES, JAN = 0.5, 80
LAG_MIN, LAG_MAX = 3.0, 9.0


def indice(lum):
    ny, nx = 100, 200
    fundo = ndimage.uniform_filter(lum, 30)      # 15 m
    alta = lum - fundo
    hann = np.hanning(JAN)
    W2 = np.outer(hann, hann)
    # mapa de desfasamentos (com wrap) em metros
    d = np.fft.fftfreq(JAN, d=1.0 / JAN) * RES   # 0,0.5,...,-1,-0.5
    DY, DX = np.meshgrid(d, d, indexing="ij")
    RD = np.hypot(DY, DX)
    anel = (RD >= LAG_MIN) & (RD <= LAG_MAX)

    tre = np.zeros((ny, nx), "float32")
    lag = np.zeros((ny, nx), "float32")
    ang = np.zeros((ny, nx), "float32")
    H, L = lum.shape
    meia = JAN // 2
    for i in range(ny):
        y0 = min(max(i * 20 + 10 - meia, 0), H - JAN)
        faixa = alta[y0:y0 + JAN]
        for j in range(nx):
            x0 = min(max(j * 20 + 10 - meia, 0), L - JAN)
            w = faixa[:, x0:x0 + JAN] * W2
            w = w - w.mean()
            F = np.fft.fft2(w)
            ac = np.real(np.fft.ifft2(np.abs(F) ** 2))
            c0 = ac[0, 0]
            if c0 <= 1e-9:
                continue
            v = ac[anel] / c0
            k = int(np.argmax(v))
            tre[i, j] = v[k]
            lag[i, j] = RD[anel][k]
            ang[i, j] = np.rad2deg(np.arctan2(DY[anel][k], DX[anel][k])) % 180
    return tre, lag, ang


def painel(nome, camadas, titulos, cmaps, vlims):
    n = len(camadas)
    fig, axes = plt.subplots(n, 1, figsize=(17, 4.6 * n), dpi=100)
    for ax, a, t, cm, vl in zip(np.atleast_1d(axes), camadas, titulos, cmaps, vlims):
        im = ax.imshow(a, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], cmap=cm,
                       origin="upper", vmin=vl[0], vmax=vl[1], interpolation="nearest")
        ax.set_title(t, fontsize=11)
        ax.tick_params(labelsize=7)
        plt.colorbar(im, ax=ax, fraction=0.023, pad=0.01)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, nome), dpi=100)
    plt.close(fig)
    print("-> %s" % nome)


if __name__ == "__main__":
    guarda = {}
    for ano in ("2010", "2012", "2021", "2025"):
        a = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano)).astype("float32")
        lum = a[:3].mean(0)
        tre, lag, ang = indice(lum)
        np.savez(os.path.join(SAI, "trelica_%s.npz" % ano), tre=tre, lag=lag, ang=ang)
        guarda[ano] = tre
        print("%s: trelica p50 %.3f  p90 %.3f  max %.3f | lag mediano %.1f m"
              % (ano, np.percentile(tre, 50), np.percentile(tre, 90), tre.max(),
                 np.median(lag)))
        painel("v04_trelica_%s.png" % ano, [tre, lag],
               ["%s — indice de trelica (autocorrelacao max, 3-9 m)" % ano,
                "%s — desfasamento do maximo (m)" % ano],
               ["inferno", "twilight"], [(0, 0.6), (3, 9)])

    est = np.min(np.stack([guarda[a] for a in ("2010", "2012", "2021")]), axis=0)
    np.save(os.path.join(SAI, "trelica_min3epocas.npy"), est)
    painel("v04_trelica_estavel.png", [est],
           ["minimo do indice de trelica em 2010, 2012 e 2021 "
            "(so passa o que tem malha nas tres epocas)"], ["inferno"], [(0, 0.6)])
