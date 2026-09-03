# -*- coding: utf-8 -*-
"""G08 — mascara `pomar` definitiva, so a partir da ortofoto.

REGRA, em tres condicoes, todas geograficas e nenhuma tocando em NDVI Sentinel:

  1. ESTRUTURA — a celula tem, em pelo menos uma das epocas 2010, 2012 ou 2025,
     um pico de autocorrelacao com compasso 4,4-5,6 m (a fiada de kiwi em
     pergola). Prova de que ha pergola instalada. Um bacelo debilitado continua
     a ter postes e fiadas, portanto isto segue a cultura e nao o vigor.

  2. COPADO A MEIO DA SERIE — a celula nao e solo nu na ortofoto de 2021. Solo
     lavrado tem luminancia muito acima de qualquer copado (ver histograma em
     v08_hist_2021.png): a separacao e categorica, entre coberto e descoberto, e
     nao um juizo de vigor entre coberturas vegetais. Serve para nao meter na
     mascara parcelas que so foram plantadas depois de 2021 nem parcelas
     arrancadas antes.

  3. MARGEM SUL — a celula esta do lado do rio onde esta a exploracao. O rio
     Minho e extraido da propria ortofoto (agua = NIR baixo) e usado como
     barreira de conectividade. Sem isto entra uma vinha da margem oposta com
     compasso semelhante — falso positivo visto em v06_cand_sobre_2025.png.

Produz ainda, para a camada seguinte poder ler a serie com honestidade:
  pomar_estavel — subconjunto com estrutura em 2012 E em 2025 (pergola instalada
                  antes do inicio da serie e ainda instalada no fim)
  plantado_apos — dentro de `pomar`, sem estrutura em 2010 nem 2012
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"


def campo10(ano):
    """bandas medias por celula de 10 m: (lum, nir)"""
    a = np.load(os.path.join(SAI, "orto_%s_10m.npy" % ano)).astype("float32")
    lum = a[:3].mean(0)
    nir = a[3] if a.shape[0] > 3 else a[0]
    return lum, nir


if __name__ == "__main__":
    a10 = np.load(os.path.join(SAI, "assin_2010.npy"))
    a12 = np.load(os.path.join(SAI, "assin_2012.npy"))
    a25 = np.load(os.path.join(SAI, "assin_2025.npy"))
    estrutura = a10 | a12 | a25

    lum21, nir21 = campo10("2021")
    lum25, nir25 = campo10("2025")

    # --- 3. agua e margem ----------------------------------------------------
    # agua no Minho: NIR muito baixo. Confirmado no histograma (v08_hist).
    agua = (nir21 < 45) & (lum21 < 90)
    agua = ndimage.binary_closing(agua, np.ones((3, 3)))
    lab_a, na = ndimage.label(agua)
    if na:
        tam = ndimage.sum(agua, lab_a, range(1, na + 1))
        agua = lab_a == int(np.argmax(tam)) + 1          # so o corpo do rio
    print("agua (rio Minho) na AOI: %d celulas = %.2f ha" % (agua.sum(), agua.sum() / 100))

    # --- 2. solo nu em 2021 --------------------------------------------------
    LIM_NU = 110.0
    nu21 = lum21 > LIM_NU
    print("solo/coberto claro em 2021 (lum > %.0f): %d celulas" % (LIM_NU, nu21.sum()))

    # --- combinar ------------------------------------------------------------
    m = estrutura & ~nu21 & ~agua
    m = ndimage.binary_opening(m, np.ones((2, 2)))
    m = ndimage.binary_closing(m, np.ones((3, 3)))

    # conectividade em terra: so componentes ligadas a maior, sem atravessar agua
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    tam = ndimage.sum(m, lab, range(1, n + 1))
    principal = int(np.argmax(tam)) + 1
    terra = ~agua
    lt, _ = ndimage.label(terra, structure=np.ones((3, 3)))
    lado = lt[lab == principal]
    lado = int(np.bincount(lado[lado > 0]).argmax())
    guarda = np.zeros_like(m)
    for k in range(1, n + 1):
        if tam[k - 1] < 10:                      # < 0,10 ha: ruido
            continue
        cel = lab == k
        if np.bincount(lt[cel][lt[cel] > 0]).argmax() == lado:
            guarda |= cel
    pomar = guarda
    # tapar so buracos pequenos (<= 4 celulas), interiores
    inv, ni = ndimage.label(~pomar)
    for k in range(1, ni + 1):
        c = inv == k
        if c.sum() <= 4:
            ys, xs = np.where(c)
            if ys.min() > 0 and xs.min() > 0 and ys.max() < 99 and xs.max() < 199:
                pomar |= c
    print("\npomar final: %d celulas = %.2f ha" % (pomar.sum(), pomar.sum() / 100))

    estavel = pomar & a12 & a25
    novo = pomar & ~(a10 | a12)
    print("  pomar_estavel (estrutura em 2012 E 2025): %d cel = %.2f ha"
          % (estavel.sum(), estavel.sum() / 100))
    print("  plantado depois de 2012 (sem estrutura em 2010/2012): %d cel = %.2f ha"
          % (novo.sum(), novo.sum() / 100))

    np.save(os.path.join(SAI, "pomar.npy"), pomar)
    np.save(os.path.join(SAI, "pomar_estavel.npy"), estavel)
    np.save(os.path.join(SAI, "plantado_apos_2012.npy"), novo)
    np.save(os.path.join(SAI, "agua.npy"), agua)

    # --- histogramas de apoio ------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.4), dpi=120)
    ax[0].hist(lum21[~agua].ravel(), bins=80, color="0.3")
    ax[0].axvline(LIM_NU, color="r")
    ax[0].set_title("2021 — luminancia por celula de 10 m (sem agua)\n"
                    "vermelho = limiar de solo nu %.0f" % LIM_NU, fontsize=9)
    ax[1].hist(nir21.ravel(), bins=80, color="0.3")
    ax[1].axvline(45, color="b")
    ax[1].set_title("2021 — NIR por celula\nazul = limiar de agua 45", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v08_hist_2021.png"), dpi=120)
    plt.close(fig)

    # --- comparacao com a antiga --------------------------------------------
    from matplotlib.path import Path as MP
    antigas = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    yy, xx = np.mgrid[0:100, 0:200]
    pts = np.vstack((xx.ravel(), yy.ravel())).T
    velho = MP(antigas["pomar"]).contains_points(pts).reshape(100, 200)
    inter = (pomar & velho).sum()
    print("\nantigo %.2f ha | novo %.2f ha | int %.2f ha | IoU %.3f | so-antigo %.2f | so-novo %.2f"
          % (velho.sum() / 100, pomar.sum() / 100, inter / 100,
             inter / max((pomar | velho).sum(), 1),
             (velho & ~pomar).sum() / 100, (pomar & ~velho).sum() / 100))

    # --- inspeccao -----------------------------------------------------------
    for ano in ("2012", "2021", "2025"):
        orto = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        rgb = np.clip(np.transpose(orto[:3], (1, 2, 0)) / 255.0, 0, 1)
        fig, ax = plt.subplots(figsize=(22, 11), dpi=110)
        ax.imshow(rgb, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        for mm, cor, lw in ((velho, "red", 1.2), (pomar, "yellow", 1.8)):
            ax.contour(mm.astype(float), levels=[0.5], colors=cor, linewidths=lw,
                       extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.set_title("`pomar` novo, geografico (amarelo, %.2f ha) vs antigo, "
                     "semeado por NDVI 2026 (vermelho, %.2f ha) — ortofoto %s"
                     % (pomar.sum() / 100, velho.sum() / 100, ano), fontsize=13)
        ax.tick_params(labelsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v08_pomar_sobre_%s.png" % ano), dpi=110)
        plt.close(fig)
        print("-> v08_pomar_sobre_%s.png" % ano)
