# -*- coding: utf-8 -*-
"""C0-13. Georreferenciacao do esquema de rega por ajuste de forma.

Transformacao de semelhanca (escala, rotacao, translacao) estimada por
alinhamento dos referenciais principais: troco ESTE da linha «Limites do
terreno» do desenho  <->  poligono `pomar` medido no Sentinel.

Nenhum parametro vem de indicacao verbal. Sai um residuo mensuravel: a
distancia de cada ponto da linha desenhada ao poligono medido.
"""
import json
import os
import numpy as np
import fitz
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))

# ------------------------------------------------------- alvo: poligono pomar
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
pomar = MP(masks["pomar"]).contains_points(pts).reshape(100, 200)
ys, xs = np.where(pomar)
TE = AOI[0] + xs * 10.0 + 5
TN = AOI[3] - ys * 10.0 - 5
T = np.column_stack([TE, TN])
Tc = T.mean(0)
_, _, vtT = np.linalg.svd(T - Tc, full_matrices=False)
if vtT[0, 0] < 0:
    vtT = -vtT

# ------------------------------------------------- fonte: linha rosa, troco E
doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3]
H, W = img.shape[:2]
R, G, B = (img[:, :, i].astype(int) for i in range(3))
rosa = (R > 140) & (R - G > 30) & (R - B > 5) & (G > 70) & (B > 70)
z = np.zeros((H, W), bool)
z[380:1320, 120:3260] = True
rz = ndimage.binary_opening(rosa & z, np.ones((2, 2)))
py, px = np.where(rz)
sel = px >= 1450
S = np.column_stack([px[sel].astype(float), -py[sel].astype(float)])
Sc = S.mean(0)
_, _, vtS = np.linalg.svd(S - Sc, full_matrices=False)
if vtS[0, 0] < 0:
    vtS = -vtS

# escala pela razao dos comprimentos ao longo do eixo principal
lS = np.ptp((S - Sc) @ vtS[0])
lT = np.ptp((T - Tc) @ vtT[0])
esc = lT / lS
# rotacao: angulo entre os eixos principais
aS = np.arctan2(vtS[0, 1], vtS[0, 0])
aT = np.arctan2(vtT[0, 1], vtT[0, 0])
th = aT - aS
Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
print("escala   = %.4f m por px (300 dpi)" % esc)
print("rotacao  = %+.2f graus" % np.degrees(th))
print("origem   : centroide do troco ESTE do desenho -> centroide do `pomar`")


def para_utm(P):
    """P: Nx2 em (px_x, -px_y) do render a 300 dpi."""
    return (np.asarray(P, float) - Sc) @ Rm.T * esc + Tc


# ---------------------------------------------------------------- residuo
lin = np.array(masks["pomar"], float)
polE = AOI[0] + lin[:, 0] * 10.0
polN = AOI[3] - lin[:, 1] * 10.0
poly = np.column_stack([polE, polN])
U = para_utm(S)
# distancia de cada ponto transformado ao contorno medido
seg0 = poly[:-1]
seg1 = poly[1:]
d = seg1 - seg0
L2 = (d * d).sum(1)
t = np.clip(((U[:, None, :] - seg0[None]) * d[None]).sum(2) / L2[None], 0, 1)
proj = seg0[None] + t[:, :, None] * d[None]
dist = np.sqrt(((U[:, None, :] - proj) ** 2).sum(2)).min(1)
print()
print("RESIDUO — distancia de cada ponto da linha desenhada ao contorno medido")
print("  n=%d  mediana=%.0f m  media=%.0f m  p90=%.0f m  max=%.0f m"
      % (len(dist), np.median(dist), dist.mean(), np.percentile(dist, 90),
         dist.max()))
print("  fraccao a menos de 25 m: %.0f%%   a menos de 50 m: %.0f%%"
      % (100 * (dist < 25).mean(), 100 * (dist < 50).mean()))

# ------------------------------------------- valvulas: circulos detectados
verm = (R > 90) & (R - G > 40) & (R - B > 30) & (R < 220) & (G < 150)
vm = ndimage.binary_closing(verm & z, np.ones((5, 5)))
lab, n = ndimage.label(vm, np.ones((3, 3)))
circ = []
for j in range(1, n + 1):
    m = lab == j
    s = int(m.sum())
    if not (400 < s < 12000):
        continue
    cy, cx = ndimage.center_of_mass(m)
    a, b = np.where(m)
    h = a.max() - a.min() + 1
    w = b.max() - b.min() + 1
    if not (18 < w < 95 and 18 < h < 95) or abs(w - h) > 0.45 * max(w, h):
        continue
    circ.append((cx, cy, s))
circ.sort()
UV = para_utm([(c[0], -c[1]) for c in circ])
print()
print("CIRCULOS DE VALVULA DETECTADOS, transformados (so os do troco ESTE "
      "sao fiaveis; x>=1450)")
for (cx, cy, s), (E, N) in zip(circ, UV):
    dentro = MP(poly).contains_point((E, N))
    print("  px x=%7.1f y=%7.1f  ->  E%.0f N%.0f   dentro do `pomar`: %s   %s"
          % (cx, cy, E, N, dentro, "" if cx >= 1450 else "(troco OESTE)"))

# ------------------------------------------------------------------- figura
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
JAN = (529900, 4654500, 531800, 4655600)
with rasterio.open(ORTO) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    arr = ds.read([1, 2, 3], window=win,
                  out_shape=(3, int(win.height / 3), int(win.width / 3)),
                  boundless=True, fill_value=0).astype("float32")
rgb = np.clip(np.moveaxis(arr, 0, -1) / max(np.percentile(arr, 99.5), 1), 0, 1)

fig, ax = plt.subplots(figsize=(20, 11), dpi=150)
ax.imshow(rgb, extent=[JAN[0], JAN[2], JAN[1], JAN[3]])
ax.scatter(U[:, 0], U[:, 1], s=0.8, c="magenta",
           label="«Limites do terreno» do esquema, georreferenciado")
ax.add_patch(MPoly(poly, closed=True, fill=False, edgecolor="red", lw=2,
                   label="poligono `pomar` (Sentinel)"))
for (cx, cy, s), (E, N) in zip(circ, UV):
    if cx < 1450:
        continue
    ax.plot([E], [N], "o", ms=10, mfc="none", mec="yellow", mew=2)
ax.set_xlim(JAN[0], JAN[2])
ax.set_ylim(JAN[1], JAN[3])
ax.legend(loc="lower left", fontsize=8)
ax.set_title("Esquema de rega georreferenciado por ajuste de forma "
             "(escala %.3f m/px, rotacao %+.1f graus) — residuo mediano %.0f m"
             % (esc, np.degrees(th), np.median(dist)), fontsize=11)
fig.savefig(os.path.join(OUT, "c0_13_georref.png"), bbox_inches="tight")
plt.close(fig)
json.dump({"escala_m_por_px300": float(esc),
           "rotacao_graus": float(np.degrees(th)),
           "origem_px": Sc.tolist(), "origem_utm": Tc.tolist(),
           "residuo_mediano_m": float(np.median(dist)),
           "residuo_p90_m": float(np.percentile(dist, 90)),
           "valvulas_utm": [[float(a), float(b)] for a, b in UV],
           "valvulas_px": [[float(a), float(b), int(c)] for a, b, c in circ]},
          open(os.path.join(OUT, "c0_13_georref.json"), "w"), indent=1)
print("\n-> c0_13_georref.png, c0_13_georref.json")
