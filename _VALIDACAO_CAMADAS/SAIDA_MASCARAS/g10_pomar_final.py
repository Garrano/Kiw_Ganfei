# -*- coding: utf-8 -*-
"""G10 — `pomar` definitivo. So estrutura de pergola + geografia. Sem copado.

Porque caiu o filtro de solo nu do G08
--------------------------------------
G09 mediu a luminancia de 2021 dentro da `zona0` antiga: p50 = 120,7 e p75 =
151,1, contra 108,6 no nucleo da lente. A `zona0` — que e precisamente a area
onde o declinio comeca — JA ESTAVA CLARA na ortofoto de 2021. Qualquer limiar de
"solo nu" apagava metade dela (50 % a 120, 46 % a 130). Isso seria uma nova
circularidade, e da pior especie: a mascara deixaria de fora exactamente o sinal
que se quer medir. O filtro foi retirado.

Fica so o que segue a INFRAESTRUTURA e nao o coberto:

  1. compasso de fiada de 4,4-5,6 m detectado por prominencia da autocorrelacao
     em 2010, 2012 ou 2025 (ver G05). Postes e fiadas existem com a planta viva
     ou moribunda.
  2. margem correcta do rio Minho, por conectividade em terra, com o rio tapado
     (`fill_holes`) para os bancos de areia nao servirem de ponte.
  3. componentes com menos de 0,10 ha caem (ruido).

Sub-mascaras que a camada seguinte precisa de ter:
  pomar_2012 — pergola ja instalada em 2010 ou 2012, isto e ANTES do inicio da
               serie (2017). E sobre esta que um declinio 2017-2026 se pode ler
               sem o confundimento de plantacao nova.
  pomar_novo — pergola detectada so em 2025.
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


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    a10 = np.load(os.path.join(SAI, "assin_2010.npy"))
    a12 = np.load(os.path.join(SAI, "assin_2012.npy"))
    a25 = np.load(os.path.join(SAI, "assin_2025.npy"))

    # --- barreira de agua ----------------------------------------------------
    o21 = np.load(os.path.join(SAI, "orto_2021_10m.npy")).astype("float32")
    lum21, nir21 = o21[:3].mean(0), o21[3]
    agua = (nir21 < 45) & (lum21 < 90)
    lab_a, na = ndimage.label(agua)
    tam = ndimage.sum(agua, lab_a, range(1, na + 1))
    agua = lab_a == int(np.argmax(tam)) + 1
    agua = ndimage.binary_closing(agua, np.ones((3, 3)))
    agua = ndimage.binary_fill_holes(agua)          # ilhas e bancos = barreira
    print("rio Minho (barreira): %.2f ha" % (agua.sum() / 100))

    bruto = (a10 | a12 | a25) & ~agua
    bruto = ndimage.binary_opening(bruto, np.ones((2, 2)))
    bruto = ndimage.binary_closing(bruto, np.ones((3, 3)))

    # --- so a margem do pomar ------------------------------------------------
    terra = ~agua
    lt, _ = ndimage.label(terra, structure=np.ones((3, 3)))
    lab, n = ndimage.label(bruto, structure=np.ones((3, 3)))
    tam = ndimage.sum(bruto, lab, range(1, n + 1))
    princ = int(np.argmax(tam)) + 1
    v = lt[lab == princ]
    margem = int(np.bincount(v[v > 0]).argmax())
    pomar = np.zeros_like(bruto)
    fora = []
    for k in range(1, n + 1):
        cel = lab == k
        if tam[k - 1] < 10:
            continue
        vv = lt[cel][lt[cel] > 0]
        if len(vv) and int(np.bincount(vv).argmax()) == margem:
            pomar |= cel
        else:
            ys, xs = np.where(cel)
            fora.append((tam[k - 1] / 100,
                         AOI[0] + 10 * xs.mean(), AOI[3] - 10 * ys.mean()))
    for a, e, nn in fora:
        print("  componente rejeitada por estar na outra margem: %.2f ha "
              "em E%.0f N%.0f" % (a, e, nn))

    inv, ni = ndimage.label(~pomar)
    for k in range(1, ni + 1):
        c = inv == k
        if c.sum() <= 4:
            ys, xs = np.where(c)
            if ys.min() > 0 and xs.min() > 0 and ys.max() < 99 and xs.max() < 199:
                pomar |= c

    p2012 = pomar & (a10 | a12)
    pnovo = pomar & ~(a10 | a12)
    print("\npomar        %4d celulas = %5.2f ha" % (pomar.sum(), pomar.sum() / 100))
    print("pomar_2012   %4d celulas = %5.2f ha  (pergola ja instalada antes da serie)"
          % (p2012.sum(), p2012.sum() / 100))
    print("pomar_novo   %4d celulas = %5.2f ha  (estrutura so vista em 2025)"
          % (pnovo.sum(), pnovo.sum() / 100))

    for nm, m in (("pomar", pomar), ("pomar_2012", p2012), ("pomar_novo", pnovo)):
        np.save(os.path.join(SAI, "%s.npy" % nm), m)
    np.save(os.path.join(SAI, "agua.npy"), agua)

    # eixo e extensao, para comparar com G2/G3 do certificado
    ys, xs = np.where(pomar)
    E = AOI[0] + 10 * xs + 5
    N = AOI[3] - 10 * ys - 5
    print("\nextensao: E %.0f-%.0f  N %.0f-%.0f  centroide E%.0f N%.0f"
          % (E.min() - 5, E.max() + 5, N.min() - 5, N.max() + 5, E.mean(), N.mean()))
    P = np.vstack((E - E.mean(), N - N.mean()))
    u, s, _ = np.linalg.svd(P @ P.T / len(E))
    az = (90 - np.rad2deg(np.arctan2(u[1, 0], u[0, 0]))) % 180
    print("azimute do eixo maior: %.1f graus" % az)

    # --- comparacao e inspeccao ---------------------------------------------
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    velho = raster(ant["pomar"])
    inter = (pomar & velho).sum()
    print("\nantigo %.2f | novo %.2f | int %.2f | IoU %.3f | so-antigo %.2f | so-novo %.2f"
          % (velho.sum() / 100, pomar.sum() / 100, inter / 100,
             inter / (pomar | velho).sum(), (velho & ~pomar).sum() / 100,
             (pomar & ~velho).sum() / 100))

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
        fig.savefig(os.path.join(SAI, "v10_pomar_sobre_%s.png" % ano), dpi=115)
        plt.close(fig)
        print("-> v10_pomar_sobre_%s.png" % ano)
