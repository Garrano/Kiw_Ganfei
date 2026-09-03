# -*- coding: utf-8 -*-
"""C0-14. Duas verificacoes finais.

 a) o troco OESTE do esquema (valvulas 1-5, o «B1» anotado com 1,77 ha), depois
    de georreferenciado pelo ajuste do troco ESTE, cai sobre alguma coisa real?
    Compara-se com a assinatura de pomar com rede na ortofoto de 2025.
 b) o traco de 1995: as coordenadas em tracos_1995_coordenadas.csv apontam para
    alguma feicao visivel na ortofoto de 1995?
"""
import csv
import json
import os
import numpy as np
import fitz
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
G = json.load(open(os.path.join(OUT, "c0_13_georref.json")))
esc = G["escala_m_por_px300"]
th = np.radians(G["rotacao_graus"])
Sc = np.array(G["origem_px"])
Tc = np.array(G["origem_utm"])
Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])


def para_utm(P):
    return (np.asarray(P, float) - Sc) @ Rm.T * esc + Tc


doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3]
H, W = img.shape[:2]
R, Gg, B = (img[:, :, i].astype(int) for i in range(3))
rosa = (R > 140) & (R - Gg > 30) & (R - B > 5) & (Gg > 70) & (B > 70)
z = np.zeros((H, W), bool)
z[380:1320, 120:3260] = True
rz = ndimage.binary_opening(rosa & z, np.ones((2, 2)))
py, px = np.where(rz)
oeste = px < 620
UO = para_utm(np.column_stack([px[oeste].astype(float),
                               -py[oeste].astype(float)]))
print("=" * 74)
print("a) TROCO OESTE DO ESQUEMA, GEORREFERENCIADO")
print("=" * 74)
print("  n=%d pontos  E %.0f..%.0f   N %.0f..%.0f"
      % (len(UO), UO[:, 0].min(), UO[:, 0].max(), UO[:, 1].min(),
         UO[:, 1].max()))
print("  centroide: E%.0f N%.0f" % (UO[:, 0].mean(), UO[:, 1].mean()))
print("  extensao: %.0f m x %.0f m"
      % (UO[:, 0].max() - UO[:, 0].min(), UO[:, 1].max() - UO[:, 1].min()))

ORTO25 = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
JANO = (529200, 4653800, 530400, 4654700)


def le(caminho, jan, res, bandas=(1, 2, 3)):
    with rasterio.open(caminho) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        bandas = [b for b in bandas if b <= ds.count]
        a = ds.read(bandas, window=win, out_shape=(len(bandas), h, w),
                    boundless=True, fill_value=0)
    return a.astype("float32")


a = le(ORTO25, JANO, 1.0)
rgb = np.clip(np.moveaxis(a, 0, -1) / max(np.percentile(a, 99.5), 1), 0, 1)
fig, ax = plt.subplots(figsize=(15, 11), dpi=140)
ax.imshow(rgb, extent=[JANO[0], JANO[2], JANO[1], JANO[3]])
ax.scatter(UO[:, 0], UO[:, 1], s=1.2, c="magenta")
ax.set_title("Troco OESTE do esquema (valvulas 1-5, «B1», 1,77 ha anotado) "
             "georreferenciado, sobre a ortofoto 2025", fontsize=10)
for e in range(JANO[0], JANO[2] + 1, 100):
    ax.axvline(e, color="yellow", lw=0.3, alpha=0.5)
for n in range(JANO[1], JANO[3] + 1, 100):
    ax.axhline(n, color="yellow", lw=0.3, alpha=0.5)
fig.savefig(os.path.join(OUT, "c0_14_lobo_oeste.png"), bbox_inches="tight")
plt.close(fig)
print("  -> c0_14_lobo_oeste.png")

# ------------------------------------------------------------- b) 1995
print()
print("=" * 74)
print("b) TRACO DE 1995 SOBRE A ORTOFOTO DE 1995 (1 m, IRG)")
print("=" * 74)
O95 = os.path.join(BASE, "orto", "ortos1995_cog_1m_irg_jpg_002-3_v01.tif")
J95 = (530250, 4654950, 530700, 4655220)
b95 = le(O95, J95, 0.5, (1, 2, 3))
b25 = le(ORTO25, J95, 0.5, (1, 2, 3))
print("  janela %s" % str(J95))
fig, axs = plt.subplots(2, 1, figsize=(16, 16), dpi=150)
for ax, arr, tit in ((axs[0], b95, "ortofoto 1995 (1 m, infravermelho-verde)"),
                     (axs[1], b25, "ortofoto 2025 (25 cm, RGB)")):
    im = np.clip(np.moveaxis(arr, 0, -1) / max(np.percentile(arr, 99), 1), 0, 1)
    ax.imshow(im, extent=[J95[0], J95[2], J95[1], J95[3]])
    for r in csv.DictReader(open(os.path.join(BASE, "_pacote_cowork",
                                              "tracos_1995_coordenadas.csv"),
                                 encoding="utf-8")):
        E, N = float(r["UTM29N_E"]), float(r["UTM29N_N"])
        if not (J95[0] < E < J95[2] and J95[1] < N < J95[3]):
            continue
        ax.plot([E], [N], "o", ms=9, mfc="none", mec="cyan", mew=2)
        ax.text(E + 6, N + 6, r["elemento"][:22], color="cyan", fontsize=7)
    # o L1 declarado: linear E-W de 240 m
    ax.plot([530342, 530583], [4655046, 4655050], color="red", lw=1.6,
            ls="--")
    ax.set_title(tit, fontsize=10)
fig.savefig(os.path.join(OUT, "c0_14_traco1995.png"), bbox_inches="tight")
plt.close(fig)
print("  -> c0_14_traco1995.png")
