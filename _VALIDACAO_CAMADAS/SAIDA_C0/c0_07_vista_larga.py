# -*- coding: utf-8 -*-
"""C0-07. Vista larga da ortofoto 2025 com grelha UTM densa, para localizar
a parcela desenhada no esquema de rega, e recorte da linha rosa do esquema
com a mesma orientacao, para comparacao de forma.
"""
import os
import numpy as np
import fitz
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO25 = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
JAN = (529200, 4654000, 531900, 4655700)

with rasterio.open(ORTO25) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    h = int(win.height / 3)
    w = int(win.width / 3)
    arr = ds.read([1, 2, 3], window=win, out_shape=(3, h, w), boundless=True,
                  fill_value=0)
rgb = np.moveaxis(arr, 0, -1).astype("float32")
rgb = np.clip(rgb / max(np.percentile(rgb, 99.5), 1), 0, 1)

fig, ax = plt.subplots(figsize=(22, 14), dpi=140)
ax.imshow(rgb, extent=[JAN[0], JAN[2], JAN[1], JAN[3]])
for e in range(JAN[0], JAN[2] + 1, 100):
    ax.axvline(e, color="yellow", lw=0.4, alpha=0.55)
    ax.text(e, JAN[1] + 20, str(e), color="yellow", fontsize=6, rotation=90)
for n in range(JAN[1], JAN[3] + 1, 100):
    ax.axhline(n, color="yellow", lw=0.4, alpha=0.55)
    ax.text(JAN[0] + 10, n, str(n), color="yellow", fontsize=6)
ax.set_title("Ortofoto DGT 2025, grelha UTM 32629 de 100 m — "
             "E %d..%d  N %d..%d" % JAN, fontsize=11)
fig.savefig(os.path.join(OUT, "c0_07_orto_grelha.png"), bbox_inches="tight")
plt.close(fig)
print("-> c0_07_orto_grelha.png")

# ---------------------------------------------- linha rosa do esquema, isolada
doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3]
H, W = img.shape[:2]
R, G, B = (img[:, :, i].astype(int) for i in range(3))
rosa = (R > 140) & (R - G > 30) & (R - B > 5) & (G > 70) & (B > 70)
zona = np.zeros((H, W), bool)
zona[300:1300, 100:3300] = True
rz = rosa & zona
ys, xs = np.where(rz)
print("linha rosa: %d px, x %d..%d, y %d..%d" % (rz.sum(), xs.min(), xs.max(),
                                                 ys.min(), ys.max()))
fig, ax = plt.subplots(figsize=(22, 8), dpi=140)
ax.imshow(img[280:1320, 80:3320])
ax.scatter(xs - 80, ys - 280, s=0.4, c="lime")
for x in range(0, 3240, 100):
    ax.axvline(x, color="cyan", lw=0.3, alpha=0.5)
    ax.text(x, 20, str(x + 80), color="cyan", fontsize=5, rotation=90)
ax.set_title("Esquema de rega, render 300 dpi, x absoluto marcado de 100 em "
             "100 px (mesmas coordenadas que m1_valvulas.py usa)", fontsize=10)
fig.savefig(os.path.join(OUT, "c0_07_esquema_grelha.png"), bbox_inches="tight")
plt.close(fig)
print("-> c0_07_esquema_grelha.png")

# extensao da linha rosa e teste da escala de m1
X_MW, E_MW = 1900.0, 530492.0
ESC = (530999.0 - 530492.0) / (2370.0 - 1900.0)
print()
print("ESCALA DE m1_valvulas.py: %.4f m por unidade de esboco" % ESC)
print("  se a unidade for o pixel do render a 300 dpi:")
for nome, x in (("extremo W do desenho", xs.min()),
                ("extremo E do desenho", xs.max())):
    print("    %s (x=%d) -> E %.0f" % (nome, x, E_MW + (x - X_MW) * ESC))
print("    comprimento implicado da parcela desenhada: %.0f m"
      % ((xs.max() - xs.min()) * ESC))
print("  valvulas 1-5 anunciadas em E528634-529088 -> x = %.0f a %.0f"
      % (1900 + (528634 - 530492) / ESC, 1900 + (529088 - 530492) / ESC))
