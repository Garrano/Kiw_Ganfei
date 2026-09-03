# -*- coding: utf-8 -*-
"""G03 — campos descritores da ortofoto, na grelha de analise de 10 m.

Nao produz nenhuma mascara. Produz os campos que uma mascara podera vir a usar,
e as imagens que permitem julga-los a olho ANTES de escolher qualquer limiar.
Foi essa a falha das duas tentativas anteriores: escolheu-se o limiar primeiro e
so depois se olhou (ou nem isso).

Para cada celula de 10 m calcula-se, numa janela de 40 x 40 m a 0,5 m:

  per   — PERIODICIDADE. Fraccao da potencia do espectro 2D que cai na banda de
          comprimentos de onda 2,5-9 m, depois de remover a tendencia local.
          A pergola tem postes e fiadas em malha regular a esse compasso; a sebe
          e a mata tem textura alta mas APERIODICA; o campo lavrado e liso.
          Este e o discriminante que a variancia local (tentativa 1) nao tem.
  dir   — ANISOTROPIA do pico periodico (0 = malha isotropa, 1 = so fiadas).
  lam   — comprimento de onda dominante, em metros, dentro da banda.
  dp    — desvio padrao local da luminancia a 3 m (a assinatura da tentativa 1,
          calculada so para se poder mostrar que sozinha nao chega).
  lum   — luminancia media
  bri   — fraccao de pixeis com luminancia > 200 (cobertura branca de 2025)

Saida: campos_<ano>.npz e v03_campos_<ano>.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
RES = 0.5
JAN = 80                 # 80 px a 0,5 m = 40 m
LAM_MIN, LAM_MAX = 2.5, 9.0   # metros


def campos(lum):
    """lum: 2000 x 4000 a 0,5 m. Devolve (per, dir, lam, dp, lm, bri) a 10 m."""
    ny, nx = 100, 200
    # --- descritores simples, por agregacao de blocos 20x20 -------------------
    lm = lum.reshape(ny, 20, nx, 20).mean(axis=(1, 3))
    bri = (lum > 200).reshape(ny, 20, nx, 20).mean(axis=(1, 3))
    J = 6                                    # 3 m
    m1 = ndimage.uniform_filter(lum, J)
    m2 = ndimage.uniform_filter(lum * lum, J)
    dp10 = np.sqrt(np.maximum(m2 - m1 * m1, 0)).reshape(ny, 20, nx, 20).mean(axis=(1, 3))

    # --- espectro por janela --------------------------------------------------
    # frequencias em ciclos/m para uma janela de JAN px a RES m
    f = np.fft.fftfreq(JAN, d=RES)
    FY, FX = np.meshgrid(f, f, indexing="ij")
    R = np.hypot(FY, FX)
    banda = (R >= 1.0 / LAM_MAX) & (R <= 1.0 / LAM_MIN)
    total = R > 0
    hann = np.hanning(JAN)
    W2 = np.outer(hann, hann)

    per = np.zeros((ny, nx), "float32")
    ani = np.zeros((ny, nx), "float32")
    lam = np.full((ny, nx), np.nan, "float32")

    # tendencia removida a escala de 15 m (30 px): mantem o compasso, tira o
    # gradiente de parcela e a sombra
    fundo = ndimage.uniform_filter(lum, 30)
    alta = lum - fundo
    H, L = lum.shape
    meia = JAN // 2
    for i in range(ny):
        cy = i * 20 + 10
        y0 = min(max(cy - meia, 0), H - JAN)
        faixa = alta[y0:y0 + JAN]
        for j in range(nx):
            cx = j * 20 + 10
            x0 = min(max(cx - meia, 0), L - JAN)
            w = faixa[:, x0:x0 + JAN] * W2
            P = np.abs(np.fft.fft2(w)) ** 2
            tot = P[total].sum()
            if tot <= 0:
                continue
            pb = P[banda]
            per[i, j] = pb.sum() / tot
            k = int(np.argmax(pb))
            ry, rx = FY[banda][k], FX[banda][k]
            lam[i, j] = 1.0 / max(np.hypot(ry, rx), 1e-9)
            # anisotropia: potencia no sector do pico (+-25 graus) vs banda toda
            ang = np.abs(np.arctan2(FY[banda], FX[banda]) - np.arctan2(ry, rx))
            ang = np.minimum(ang % np.pi, np.pi - (ang % np.pi))
            ani[i, j] = pb[ang < np.deg2rad(25)].sum() / max(pb.sum(), 1e-12)
    return per, ani, lam, dp10, lm, bri


def mostra(nome, ano, dados, titulos, cmaps):
    fig, axes = plt.subplots(len(dados), 1, figsize=(16, 3.1 * len(dados)), dpi=105)
    for ax, a, t, cm in zip(np.atleast_1d(axes), dados, titulos, cmaps):
        im = ax.imshow(a, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], cmap=cm,
                       origin="upper", aspect="equal")
        ax.set_title("%s — %s" % (ano, t), fontsize=10)
        ax.tick_params(labelsize=7)
        plt.colorbar(im, ax=ax, fraction=0.021, pad=0.01)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, nome), dpi=105)
    plt.close(fig)
    print("-> %s" % nome)


if __name__ == "__main__":
    for ano in ("2010", "2012", "2021", "2025"):
        a = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano)).astype("float32")
        lum = a[:3].mean(0)
        per, ani, lam, dp, lm, bri = campos(lum)
        np.savez(os.path.join(SAI, "campos_%s.npz" % ano),
                 per=per, ani=ani, lam=lam, dp=dp, lum=lm, bri=bri)
        print("%s: per %.4f-%.4f (mediana %.4f)  lam mediana %.2f m"
              % (ano, np.nanmin(per), np.nanmax(per), np.nanmedian(per),
                 np.nanmedian(lam)))
        mostra("v03_campos_%s.png" % ano, ano,
               [per, ani, dp, bri],
               ["periodicidade 2,5-9 m (fraccao da potencia)",
                "anisotropia do pico", "desvio padrao local a 3 m (tentativa 1)",
                "fraccao de pixeis claros (>200)"],
               ["magma", "viridis", "magma", "gray"])
