# -*- coding: utf-8 -*-
"""G13 — a `zona0` em todas as epocas de ortofoto disponiveis.

v12_zona0.png levantou uma duvida grave: o interior da `zona0` parece campo
lavrado em 2021 e faixa sem fiadas em 2012, e so aparece com fiadas cobertas em
2025. Se assim for, a `zona0` nao e «sub-parcela de linhas mortas»: e, em boa
parte, chao que nao teve pomar durante a maior parte da serie.

Antes de afirmar isso ha que distinguir duas historias diferentes:
  (i)  nunca esteve plantada ate depois de 2021  -> NDVI baixo por ausencia
  (ii) esteve plantada e foi arrancada           -> NDVI baixo por arranque
1995, 2004, 2007 e 2010 separam as duas.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
ANOS = ["1995", "2004", "2007", "2010", "2012", "2021", "2025"]
JAN = (530850, 531200, 4654980, 4655230)


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    z0 = raster(ant["zona0"])
    mw = raster(ant["manchaW"])
    z50 = np.kron(z0.astype(float), np.ones((20, 20)))
    e0, e1, n0, n1 = JAN
    c0, c1 = int((e0 - AOI[0]) / 0.5), int((e1 - AOI[0]) / 0.5)
    l0, l1 = int((AOI[3] - n1) / 0.5), int((AOI[3] - n0) / 0.5)

    fig, axes = plt.subplots(2, 4, figsize=(22, 10), dpi=120)
    for ax, ano in zip(axes.ravel(), ANOS):
        o = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        ax.imshow(np.transpose(o[:3, l0:l1, c0:c1], (1, 2, 0)) / 255.0,
                  extent=[e0, e1, n0, n1], origin="upper")
        ax.contour(z50[l0:l1, c0:c1], levels=[0.5], colors="#ff3300", linewidths=2.0,
                   extent=[e0, e1, n0, n1], origin="upper")
        ax.set_title(ano, fontsize=12); ax.tick_params(labelsize=7)
    axes.ravel()[-1].axis("off")
    fig.suptitle("`zona0` (vermelho) em todas as epocas de ortofoto DGT", fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v13_zona0_epocas.png"), dpi=120)
    plt.close(fig)
    print("-> v13_zona0_epocas.png")

    # quanto da zona0 e da manchaW tem estrutura de pergola em cada epoca
    print("\nfraccao com assinatura de compasso 5 m (estrutura de pergola):")
    print("  mascara      2010    2012    2025")
    for nm, m in (("zona0", z0), ("manchaW", mw)):
        v = []
        for ano in ("2010", "2012", "2025"):
            a = np.load(os.path.join(SAI, "assin_%s.npy" % ano))
            v.append(100 * (a & m).sum() / m.sum())
        print("  %-10s %6.1f%% %6.1f%% %6.1f%%" % (nm, *v))
    pnovo = np.load(os.path.join(SAI, "pomar_novo.npy"))
    p2012 = np.load(os.path.join(SAI, "pomar_2012.npy"))
    print("\n  zona0   dentro de pomar_2012 %.1f%% | dentro de pomar_novo %.1f%%"
          % (100 * (z0 & p2012).sum() / z0.sum(), 100 * (z0 & pnovo).sum() / z0.sum()))
    print("  manchaW dentro de pomar_2012 %.1f%% | dentro de pomar_novo %.1f%%"
          % (100 * (mw & p2012).sum() / mw.sum(), 100 * (mw & pnovo).sum() / mw.sum()))

    # luminancia por epoca dentro da zona0 e num nucleo de pergola de controlo
    ctrl = np.zeros((100, 200), bool)
    ctrl[int((AOI[3] - 4655250) / 10):int((AOI[3] - 4655050) / 10),
         int((530400 - AOI[0]) / 10):int((530800 - AOI[0]) / 10)] = True
    print("\nluminancia mediana por celula de 10 m:")
    print("  epoca   zona0   nucleo-controlo")
    for ano in ANOS:
        a = np.load(os.path.join(SAI, "orto_%s_10m.npy" % ano)).astype("float32")
        lum = a[:3].mean(0)
        print("  %-6s  %6.1f  %6.1f" % (ano, np.median(lum[z0]), np.median(lum[ctrl])))
