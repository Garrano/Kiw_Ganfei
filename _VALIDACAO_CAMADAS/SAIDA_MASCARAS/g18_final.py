# -*- coding: utf-8 -*-
"""G18 — diagnostico final da referencia, mapas de defice, e masks_geograficas.json."""
import os
import json
import glob
import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage, stats
from skimage import measure
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
PLENA = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
LIM_DEF = 0.05


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


def bits(m):
    return ["".join("1" if v else "0" for v in linha) for linha in m]


def contornos(m, tol=0.6):
    out = []
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    for k in range(1, n + 1):
        c = measure.find_contours((lab == k).astype(float), 0.5)
        if not c:
            continue
        p = measure.approximate_polygon(max(c, key=len), tolerance=tol)
        out.append([[round(float(x), 1), round(float(y), 1)] for y, x in p])
    return out


if __name__ == "__main__":
    fich = sorted(glob.glob(os.path.join(GAN, "sentinel", "*.tif")))
    datas = [os.path.basename(f)[:10] for f in fich]
    nd = np.stack([rasterio.open(f).read(1).astype("float64") for f in fich])
    ip = [i for i, d in enumerate(datas) if d in PLENA]
    x = np.array([int(datas[i][:4]) + (int(datas[i][5:7]) - 1) / 12 for i in ip])

    pomar = np.load(os.path.join(SAI, "pomar.npy"))
    ref = np.load(os.path.join(SAI, "saudavel.npy"))
    z0 = np.load(os.path.join(SAI, "zona0.npy"))
    nu21 = np.load(os.path.join(SAI, "nu2021.npy"))
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    mw_ant, z0_ant = raster(ant["manchaW"]), raster(ant["zona0"])

    # --- diagnostico: a referencia desce por causa das celulas em mancha? ----
    print("DIAGNOSTICO — de onde vem o declive negativo da referencia")
    print("  (so diagnostico: retirar celulas por elas estarem em mancha e")
    print("   seleccionar pelo resultado, e nao entra na definicao da mascara)")
    for nome, m in (("referencia completa (110)", ref),
                    ("sem as 18 celulas em manchaW", ref & ~mw_ant),
                    ("sem manchaW e sem zona0", ref & ~mw_ant & ~z0_ant),
                    ("so as 18 celulas em manchaW", ref & mw_ant)):
        y = np.array([np.nanmean(nd[i][m]) for i in ip])
        s = stats.linregress(x, y)
        print("  %-32s n=%3d  %+.5f/ano  p=%.4f  2017 %.4f  2026 %.4f"
              % (nome, m.sum(), s.slope, s.pvalue, y[0], y[-1]))

    # --- mapa de declive por celula -----------------------------------------
    Y = nd[ip][:, pomar]
    dec = np.array([stats.linregress(x, Y[:, k]).slope for k in range(Y.shape[1])])
    mapa = np.full((100, 200), np.nan)
    mapa[pomar] = dec
    print("\ndeclive por celula dentro do `pomar` (9 cenas):")
    print("  mediana %+.5f/ano | p25 %+.5f | p75 %+.5f | celulas a descer %.1f %%"
          % (np.median(dec), np.percentile(dec, 25), np.percentile(dec, 75),
             100 * (dec < 0).mean()))

    # --- manchas emergentes na ultima cena ----------------------------------
    k26 = datas.index("2026-07-27")
    mref = float(np.nanmean(nd[k26][ref]))
    dmap = pomar & (nd[k26] < mref - LIM_DEF)
    lab, n = ndimage.label(dmap, structure=np.ones((3, 3)))
    tam = ndimage.sum(dmap, lab, range(1, n + 1))
    print("\nmanchas de defice em 2026-07-27 (referencia %.4f, limiar %.4f):" % (mref, mref - LIM_DEF))
    for k in np.argsort(tam)[::-1]:
        if tam[k] < 20:
            continue
        ys, xs = np.where(lab == k + 1)
        print("  %5.2f ha  E %.0f-%.0f  N %.0f-%.0f  |  %.0f %% dessa mancha esta "
              "sobre chao lavrado em 2021"
              % (tam[k] / 100, AOI[0] + 10 * xs.min(), AOI[0] + 10 * xs.max() + 10,
                 AOI[3] - 10 * ys.max() - 10, AOI[3] - 10 * ys.min(),
                 100 * (nu21 & (lab == k + 1)).sum() / tam[k]))

    # --- figura: defice e declive -------------------------------------------
    orto = np.load(os.path.join(SAI, "orto_2025_50cm.npy"))
    ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
    fig, axes = plt.subplots(2, 1, figsize=(17, 11), dpi=110)
    axes[0].imshow(np.clip(np.transpose(orto[:3], (1, 2, 0)) / 255.0, 0, 1),
                   extent=ext, origin="upper")
    im = axes[0].imshow(np.where(dmap, 1.0, np.nan), extent=ext, origin="upper",
                        cmap="autumn", alpha=0.55, vmin=0, vmax=1)
    axes[0].contour(pomar.astype(float), levels=[0.5], colors="yellow", linewidths=1.3,
                    extent=ext, origin="upper")
    axes[0].contour(nu21.astype(float), levels=[0.5], colors="cyan", linewidths=1.4,
                    extent=ext, origin="upper")
    axes[0].set_title("manchas de defice em 2026-07-27 emergentes do mapa (%.2f ha); "
                      "ciano = chao lavrado em 2021" % (dmap.sum() / 100), fontsize=11)
    im = axes[1].imshow(mapa, extent=ext, origin="upper", cmap="RdBu",
                        vmin=-0.03, vmax=0.03)
    axes[1].contour(pomar.astype(float), levels=[0.5], colors="k", linewidths=0.8,
                    extent=ext, origin="upper")
    axes[1].set_title("declive do NDVI por celula, 9 cenas de plena estacao (/ano)",
                      fontsize=11)
    plt.colorbar(im, ax=axes[1], fraction=0.023, pad=0.01)
    for ax in axes:
        ax.set_xlim(530100, 531600); ax.set_ylim(4654800, 4655500)
        ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v18_defice_declive.png"), dpi=110)
    plt.close(fig)
    print("-> v18_defice_declive.png")

    # --- masks_geograficas.json ---------------------------------------------
    saida = {
        "_metodo": "Mascaras derivadas exclusivamente das ortofotos DGT (EPSG:3763), "
                   "reprojectadas com rasterio.warp.reproject para a grelha de analise. "
                   "Nenhuma mascara usa NDVI Sentinel de nenhuma data.",
        "_assinatura": "compasso de fiada de 4,4-5,6 m detectado pela prominencia do "
                       "primeiro pico secundario da autocorrelacao radial, em janela de "
                       "40 m, nas epocas 2010, 2012 e 2025 (25/50 cm).",
        "_grelha": {"crs": "EPSG:32629", "aoi": list(AOI), "linhas": 100,
                    "colunas": 200, "passo_m": 10.0,
                    "origem_canto_NO": [AOI[0], AOI[3]],
                    "nota": "identica a sentinel/*.tif"},
        "_ordem": "cada *_bits e uma lista de 100 cadeias de 200 caracteres '0'/'1'; "
                  "linha 0 = norte, coluna 0 = oeste. Ler com "
                  "np.array([[c=='1' for c in l] for l in bits])",
        "pomar_bits": bits(pomar),
        "saudavel_bits": bits(ref),
        "zona0_bits": bits(z0),
        "nu2021_bits": bits(nu21),
        "pomar": contornos(pomar),
        "saudavel": contornos(ref),
        "zona0": contornos(z0),
        "nu2021": contornos(nu21),
        "_areas_ha": {"pomar": pomar.sum() / 100, "saudavel": ref.sum() / 100,
                      "zona0": z0.sum() / 100, "nu2021": nu21.sum() / 100},
        "_saudavel_desenho": "grelha regular: uma celula de 10 m de 30 em 30 m sobre o "
                             "pomar com pergola detectada em 2010 ou 2012, a >= 20 m de "
                             "qualquer bordo. Nenhuma celula escolhida por valor "
                             "radiometrico. 110 celulas, 1,10 ha, a cobrir todo o eixo "
                             "E530250-531490.",
        "_saudavel_limite": "Referencia INTERNA: mede contraste espacial. Nao pode "
                            "detectar declinio uniforme do pomar inteiro.",
        "_manchaW": "RETIRADA. Era `pomar & (nd2026 < 0,76)` dilatada — definia a mancha "
                    "pelo sinal que depois se media. As manchas passam a sair do mapa de "
                    "defice, data a data.",
        "_zona0": "poligono geografico do ficheiro antigo, intersectado com o novo pomar "
                  "(202 das 220 celulas). ATENCAO: 41,4 % da sua area e chao lavrado na "
                  "ortofoto de 2021 — ver nu2021_bool.",
        "_nu2021": "chao lavrado dentro do pomar na ortofoto de 2021 (25 cm), 1,67 ha. "
                   "Nao e mascara de analise; serve para separar planta de chao.",
    }
    cam = os.path.join(GAN, "sentinel", "masks_geograficas.json")
    with open(cam, "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1)
    print("-> %s (%.0f kB)" % (cam, os.path.getsize(cam) / 1024))
