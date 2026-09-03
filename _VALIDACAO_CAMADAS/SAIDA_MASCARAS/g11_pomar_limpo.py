# -*- coding: utf-8 -*-
"""G11 — `pomar` com os dois falsos positivos vistos em v10 resolvidos.

A inspeccao visual de v10_pomar_sobre_2025.png mostrou duas componentes que a
assinatura de compasso apanha e que nao sao a exploracao:

  a) uma vinha na MARGEM NORTE do Minho (E530080-530200, N4655330-4655560).
     O teste de conectividade em terra do G10 nao a apanhou porque a arvoredo
     ribeirinho tapa o rio em EPSG:32629 E530000-530250 e abre uma ponte falsa.
  b) um bloco de ESTUFAS a sudeste (E531480-531580, N4654880-4655000): telhado
     branco com nervuras a ~5 m, compasso indistinguivel do da cobertura.

Dois testes ao nivel da COMPONENTE, nao da celula — e importante que sejam ao
nivel da componente, porque qualquer teste por celula sobre a luminancia de 2021
apagaria a `zona0` (G09).

  T1 travessia do rio: o segmento entre o centroide da componente e o centroide
     da componente principal atravessa agua? Se sim, e outra margem.
  T2 estrutura construida: mediana da luminancia da componente na ortofoto de
     2021 acima de 140. A pergola de kiwi em 2021 tem copado fechado e escuro
     (mediana 108,6 no nucleo); um telhado de estufa nao.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import measure
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
LIM_ESTUFA = 140.0


def raster(poly, H=100, W=200):
    yy, xx = np.mgrid[0:H, 0:W]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(H, W)


def atravessa(agua, p, q, n=400):
    t = np.linspace(0, 1, n)
    yy = np.round(p[0] + (q[0] - p[0]) * t).astype(int)
    xx = np.round(p[1] + (q[1] - p[1]) * t).astype(int)
    return int(agua[yy, xx].sum())


if __name__ == "__main__":
    a10 = np.load(os.path.join(SAI, "assin_2010.npy"))
    a12 = np.load(os.path.join(SAI, "assin_2012.npy"))
    a25 = np.load(os.path.join(SAI, "assin_2025.npy"))
    o21 = np.load(os.path.join(SAI, "orto_2021_10m.npy")).astype("float32")
    lum21, nir21 = o21[:3].mean(0), o21[3]

    agua = (nir21 < 45) & (lum21 < 90)
    lab_a, na = ndimage.label(agua)
    agua = lab_a == int(np.argmax(ndimage.sum(agua, lab_a, range(1, na + 1)))) + 1
    agua = ndimage.binary_fill_holes(ndimage.binary_closing(agua, np.ones((3, 3))))

    bruto = (a10 | a12 | a25) & ~agua
    bruto = ndimage.binary_closing(ndimage.binary_opening(bruto, np.ones((2, 2))),
                                   np.ones((3, 3)))
    lab, n = ndimage.label(bruto, structure=np.ones((3, 3)))
    tam = ndimage.sum(bruto, lab, range(1, n + 1))
    princ = int(np.argmax(tam)) + 1
    cp = ndimage.center_of_mass(bruto, lab, princ)

    pomar = np.zeros_like(bruto)
    print("componentes com >= 0,10 ha:")
    for k in range(1, n + 1):
        if tam[k - 1] < 10:
            continue
        cel = lab == k
        c = ndimage.center_of_mass(cel)
        cruza = atravessa(agua, c, cp) if k != princ else 0
        med = float(np.median(lum21[cel]))
        e, nn = AOI[0] + 10 * c[1] + 5, AOI[3] - 10 * c[0] - 5
        if cruza >= 3:
            veredicto = "REJEITADA (outra margem, %d celulas de agua no caminho)" % cruza
        elif med > LIM_ESTUFA:
            veredicto = "REJEITADA (estrutura construida, lum21 mediana %.0f)" % med
        else:
            veredicto = "aceite"
            pomar |= cel
        print("  %5.2f ha  E%.0f N%.0f  lum21 %5.1f  %s"
              % (tam[k - 1] / 100, e, nn, med, veredicto))

    inv, ni = ndimage.label(~pomar)
    for k in range(1, ni + 1):
        c = inv == k
        if c.sum() <= 4:
            ys, xs = np.where(c)
            if ys.min() > 0 and xs.min() > 0 and ys.max() < 99 and xs.max() < 199:
                pomar |= c

    p2012 = pomar & (a10 | a12)
    pnovo = pomar & ~(a10 | a12)
    print("\npomar       %5.2f ha   pomar_2012 %5.2f ha   pomar_novo %5.2f ha"
          % (pomar.sum() / 100, p2012.sum() / 100, pnovo.sum() / 100))
    for nm, m in (("pomar", pomar), ("pomar_2012", p2012), ("pomar_novo", pnovo),
                  ("agua", agua)):
        np.save(os.path.join(SAI, "%s.npy" % nm), m)

    ys, xs = np.where(pomar)
    E, N = AOI[0] + 10 * xs + 5, AOI[3] - 10 * ys - 5
    P = np.vstack((E - E.mean(), N - N.mean()))
    u, s, _ = np.linalg.svd(P @ P.T / len(E))
    print("extensao E %.0f-%.0f  N %.0f-%.0f | centroide E%.0f N%.0f | azimute %.1f"
          % (E.min() - 5, E.max() + 5, N.min() - 5, N.max() + 5, E.mean(), N.mean(),
             (90 - np.rad2deg(np.arctan2(u[1, 0], u[0, 0]))) % 180))

    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    velho = raster(ant["pomar"])
    inter = (pomar & velho).sum()
    print("antigo %.2f | novo %.2f | IoU %.3f | so-antigo %.2f | so-novo %.2f"
          % (velho.sum() / 100, pomar.sum() / 100, inter / (pomar | velho).sum(),
             (velho & ~pomar).sum() / 100, (pomar & ~velho).sum() / 100))

    for ano in ("2012", "2021", "2025"):
        orto = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        rgb = np.clip(np.transpose(orto[:3], (1, 2, 0)) / 255.0, 0, 1)
        fig, ax = plt.subplots(figsize=(22, 11), dpi=115)
        ax.imshow(rgb, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.contour(velho.astype(float), levels=[0.5], colors="red", linewidths=1.1,
                   extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.contour(pomar.astype(float), levels=[0.5], colors="yellow", linewidths=1.9,
                   extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.set_title("`pomar` geografico (amarelo, %.2f ha) vs antigo semeado por "
                     "NDVI 2026 (vermelho, %.2f ha) — ortofoto %s"
                     % (pomar.sum() / 100, velho.sum() / 100, ano), fontsize=13)
        ax.tick_params(labelsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v11_pomar_sobre_%s.png" % ano), dpi=115)
        plt.close(fig)
        print("-> v11_pomar_sobre_%s.png" % ano)
