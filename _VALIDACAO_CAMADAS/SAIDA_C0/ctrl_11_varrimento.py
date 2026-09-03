# -*- coding: utf-8 -*-
"""CTRL-11. Varrimento visual do aluviao, na ortofoto de 2021 (25 cm), que foi
voada com a folha desenvolvida.

Porque 2021 e nao 2025: na ortofoto de 2025 (voo entre 29-03 e 26-07-2025,
segundo o STAC da DGT) este canto foi voado com o kiwi ainda sem folha, e um
pomar de latada aparece como faixas brancas de rede/cobertura — indistinguivel,
a olho, de tuneis de pequenos frutos. Com folha, a latada fecha a entrelinha e
o quarteirao le-se como um copado continuo; a cultura em linha mantem a
entrelinha aberta. E esse o criterio de estrutura usado aqui.

Quatro paineis a 0,7 m cobrindo a planicie aluvial dentro de ~3 km.
So R,G,B. Nenhum indice.
"""
import os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif")
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
PAINEIS = {
    "A_caso_e_leste": (530000, 4654600, 531800, 4655700),
    "B_sul_do_caso": (529900, 4653900, 531700, 4655000),
    "C_blocoSW": (529200, 4653500, 530400, 4654700),
    "D_valenca_sul": (528800, 4652200, 530600, 4653600),
}
RES = 0.7

for nome, jan in PAINEIS.items():
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / RES))
        h = int(round((jan[3] - jan[1]) / RES))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0)
    rgb = np.moveaxis(a, 0, -1).astype("float32")
    rgb = np.clip(rgb / max(np.percentile(rgb, 99.3), 1.0), 0, 1)
    fig, ax = plt.subplots(figsize=(18, 18 * (jan[3] - jan[1])
                                    / (jan[2] - jan[0])), dpi=180)
    ax.imshow(rgb, extent=[jan[0], jan[2], jan[1], jan[3]])
    ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0],
                           CASO[3] - CASO[1], fill=False, edgecolor="red",
                           lw=1.6))
    for e in range(int(jan[0]) // 100 * 100, int(jan[2]) + 100, 100):
        if jan[0] <= e <= jan[2]:
            ax.axvline(e, color="yellow", lw=0.3, alpha=0.45)
    for n in range(int(jan[1]) // 100 * 100, int(jan[3]) + 100, 100):
        if jan[1] <= n <= jan[3]:
            ax.axhline(n, color="yellow", lw=0.3, alpha=0.45)
    ax.set_title("Varrimento %s — ortofoto DGT 2021 (25 cm) a %.1f m, "
                 "grelha 100 m, EPSG:32629" % (nome, RES), fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_11_%s.png" % nome), bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_11_%s.png  %s" % (nome, rgb.shape))
