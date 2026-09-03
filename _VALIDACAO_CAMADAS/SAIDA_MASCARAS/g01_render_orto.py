# -*- coding: utf-8 -*-
"""G01 — reprojectar as ortofotos DGT para a grelha de analise e olhar para elas.

Licao das duas tentativas falhadas: nenhum numero vale nada antes de a mascara
ser vista sobre a ortofoto. Este script nao decide nada; so produz as imagens
de base, ja em EPSG:32629 e alinhadas com a AOI, a 0,5 m e a 10 m.

Saida:
  orto_<ano>_50cm.npy   RGB(+NIR) reamostrado para 0,5 m sobre a AOI (2000x4000)
  orto_<ano>_10m.npy    o mesmo agregado por media para a grelha 100x200
  v01_orto_<ano>.png    imagem para inspeccao visual
"""
import os
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.windows import from_bounds
from rasterio.transform import from_origin
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)          # EPSG:32629
BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"

ORTOS = {
    "1995": "ortos1995_cog_1m_irg_jpg_002-3_v01.tif",
    "2004": "ortos20042006_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2007": "ortos2007_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2010": "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2012": "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif",
    "2021": "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif",
    "2025": "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif",
}

# grelha fina: 0,5 m, canto NO da AOI, 2000 linhas x 4000 colunas
RES_F = 0.5
NYF = int((AOI[3] - AOI[1]) / RES_F)
NXF = int((AOI[2] - AOI[0]) / RES_F)
T_FINA = from_origin(AOI[0], AOI[3], RES_F, RES_F)
# grelha de analise: 10 m, 100 x 200 (identica aos sentinel/*.tif)
T_10 = from_origin(AOI[0], AOI[3], 10.0, 10.0)


def le_e_reprojecta(caminho, nbandas):
    ds = rasterio.open(caminho)
    # janela na ortofoto que cobre a AOI, com folga
    wb = transform_bounds("EPSG:32629", ds.crs, *AOI)
    wb = (wb[0] - 100, wb[1] - 100, wb[2] + 100, wb[3] + 100)
    win = from_bounds(*wb, transform=ds.transform).round_offsets().round_lengths()
    t_src = rasterio.windows.transform(win, ds.transform)
    saida = np.zeros((nbandas, NYF, NXF), "float32")
    for b in range(nbandas):
        a = ds.read(b + 1, window=win, boundless=True, fill_value=0).astype("float32")
        reproject(a, saida[b], src_transform=t_src, src_crs=ds.crs,
                  dst_transform=T_FINA, dst_crs="EPSG:32629",
                  resampling=Resampling.average, src_nodata=None, dst_nodata=None)
    print("  %s: janela %dx%d px em %s -> %dx%d a 0,5 m"
          % (os.path.basename(caminho), win.width, win.height, ds.crs, NXF, NYF))
    ds.close()
    return saida


def agrega10(a):
    """0,5 m -> 10 m por media de blocos 20x20. Alinhamento exacto por construcao."""
    n = a.shape[0]
    return a.reshape(n, 100, 20, 200, 20).mean(axis=(2, 4))


if __name__ == "__main__":
    for ano, nome in ORTOS.items():
        cam = os.path.join(BASE, "orto", nome)
        nb = 3 if ano == "1995" else 4
        a = le_e_reprojecta(cam, nb)
        np.save(os.path.join(SAI, "orto_%s_50cm.npy" % ano), a.astype("uint8"))
        np.save(os.path.join(SAI, "orto_%s_10m.npy" % ano), agrega10(a).astype("float32"))

        rgb = np.transpose(a[:3], (1, 2, 0)) / 255.0
        rgb = np.clip(rgb, 0, 1)
        fig, ax = plt.subplots(figsize=(20, 10), dpi=110)
        ax.imshow(rgb, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.set_title("Ortofoto DGT %s reprojectada para EPSG:32629 (0,5 m) — AOI de analise" % ano)
        ax.set_xlabel("E (m, UTM29N)"); ax.set_ylabel("N (m)")
        ax.grid(color="w", alpha=0.25, lw=0.4)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v01_orto_%s.png" % ano), dpi=110)
        plt.close(fig)
        print("  -> v01_orto_%s.png" % ano)
    print("feito")
