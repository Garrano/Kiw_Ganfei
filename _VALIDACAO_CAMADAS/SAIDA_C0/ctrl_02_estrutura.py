# -*- coding: utf-8 -*-
"""CTRL-02. Detector de ESTRUTURA (nao de vigor).

Procura, na ortofoto de 2025 a 25 cm reamostrada a 0,5 m, blocos com
periodicidade linear forte de comprimento de onda 3–9 m — a assinatura
geometrica de uma latada (pergola) de kiwi, de uma rede de sombra/granizo
montada sobre postes alinhados, ou de qualquer cultura em linha regular.

NAO le a banda 4 (NIR). NAO calcula NDVI nem qualquer indice. Usa apenas a
luminancia R+G+B, isto e, textura. Um bloco entra na lista de candidatos por
ter linhas regulares, nunca por ser verde ou por ter sinal alto.

Saida:
  ctrl_02_periodicidade.npy / .json  — mapa de forca de periodicidade
  ctrl_02_mapa.png                   — mapa sobre a ortofoto
  ctrl_02_candidatos.csv             — blocos nomeados para confirmacao visual
"""
import json
import os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO25 = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
JAN = (527840.0, 4652200.0, 531795.0, 4655785.0)
RES = 0.5
BL = 64            # bloco de 64 px = 32 m
STEP = 32          # passo de 16 m
LMIN, LMAX = 3.0, 9.0      # comprimento de onda procurado, em metros

with rasterio.open(ORTO25) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    W = int(round((JAN[2] - JAN[0]) / RES))
    H = int(round((JAN[3] - JAN[1]) / RES))
    a = ds.read([1, 2, 3], window=win, out_shape=(3, H, W),
                boundless=True, fill_value=0)
lum = a.mean(0).astype("float32")
del a
print("luminancia %s  (%.1f MB)" % (lum.shape, lum.nbytes / 1e6))

# frequencias em ciclos por pixel -> comprimento de onda em metros
fy = np.fft.fftfreq(BL)[:, None]
fx = np.fft.fftfreq(BL)[None, :]
fr = np.sqrt(fy ** 2 + fx ** 2)
with np.errstate(divide="ignore"):
    lam = RES / np.maximum(fr, 1e-9)
banda = (lam >= LMIN) & (lam <= LMAX)
fundo = (lam > LMAX) & (lam < 40.0)
jan2d = np.outer(np.hanning(BL), np.hanning(BL)).astype("float32")

ny = (H - BL) // STEP + 1
nx = (W - BL) // STEP + 1
forca = np.zeros((ny, nx), "float32")
lamb = np.zeros((ny, nx), "float32")
ang = np.zeros((ny, nx), "float32")
contr = np.zeros((ny, nx), "float32")
print("grelha de blocos %d x %d" % (ny, nx))

for i in range(ny):
    if i % 40 == 0:
        print("  linha %d/%d" % (i, ny))
    y0 = i * STEP
    for j in range(nx):
        x0 = j * STEP
        b = lum[y0:y0 + BL, x0:x0 + BL]
        s = b.std()
        contr[i, j] = s
        if s < 3.0:                      # agua lisa, sombra, vazio
            continue
        f = np.fft.fft2((b - b.mean()) * jan2d)
        p = (f.real ** 2 + f.imag ** 2)
        tot = p[fundo].sum() + p[banda].sum() + 1e-9
        pb = p * banda
        k = int(pb.argmax())
        forca[i, j] = pb.flat[k] / tot
        lamb[i, j] = lam.flat[k]
        ang[i, j] = np.degrees(np.arctan2(fy.flat[k // BL] if False else
                                          fy[k // BL, 0], fx[0, k % BL]))

np.save(os.path.join(OUT, "ctrl_02_forca.npy"), forca)
np.save(os.path.join(OUT, "ctrl_02_lambda.npy"), lamb)
json.dump(dict(janela=list(JAN), res=RES, bloco_px=BL, passo_px=STEP,
               lam_min=LMIN, lam_max=LMAX, shape=[ny, nx],
               origem="ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif R+G+B",
               nota="sem NIR, sem qualquer indice de vegetacao"),
          open(os.path.join(OUT, "ctrl_02_periodicidade.json"), "w"), indent=1)

# ---------------------------------------------------------------- candidatos
lim = np.percentile(forca[forca > 0], 97.0)
m = (forca >= lim) & (contr > 6.0)
m = ndimage.binary_closing(m, np.ones((3, 3)))
m = ndimage.binary_opening(m, np.ones((2, 2)))
lab, n = ndimage.label(m, np.ones((3, 3)))
px_m2 = (STEP * RES) ** 2
tam = ndimage.sum(m, lab, range(1, n + 1)) * px_m2 / 1e4
CX, CY = (CASO[0] + CASO[2]) / 2, (CASO[1] + CASO[3]) / 2
linhas = ["id,area_ha_bruta,E_min,E_max,N_min,N_max,dist_centroide_m,lambda_med_m"]
print()
print("=" * 92)
print("BLOCOS COM PERIODICIDADE LINEAR FORTE (>= p97), >= 0,5 ha")
print("=" * 92)
k = 0
for idx in np.argsort(tam)[::-1]:
    if tam[idx] < 0.5:
        break
    k += 1
    mm = lab == idx + 1
    ys, xs = np.where(mm)
    e0 = JAN[0] + (xs.min() * STEP + BL / 2) * RES
    e1 = JAN[0] + (xs.max() * STEP + BL / 2) * RES
    n1 = JAN[3] - (ys.min() * STEP + BL / 2) * RES
    n0 = JAN[3] - (ys.max() * STEP + BL / 2) * RES
    ec, nc = (e0 + e1) / 2, (n0 + n1) / 2
    d = np.hypot(ec - CX, nc - CY)
    lm = float(np.median(lamb[mm]))
    print("  P%02d  %6.2f ha  E %.0f..%.0f  N %.0f..%.0f  d=%.0f m  lam=%.1f m"
          % (k, tam[idx], e0, e1, n0, n1, d, lm))
    linhas.append("P%02d,%.2f,%.0f,%.0f,%.0f,%.0f,%.0f,%.1f"
                  % (k, tam[idx], e0, e1, n0, n1, d, lm))
open(os.path.join(OUT, "ctrl_02_candidatos.csv"), "w").write("\n".join(linhas))
print("  (%d blocos; area BRUTA da grelha, nao e a area do poligono)" % k)

fig, ax = plt.subplots(figsize=(15, 14), dpi=170)
ax.imshow(np.clip(lum / np.percentile(lum, 99) * 0.8, 0, 1),
          extent=[JAN[0], JAN[2], JAN[1], JAN[3]], cmap="gray")
ax.imshow(np.where(forca >= lim, forca, np.nan),
          extent=[JAN[0] + BL * RES / 2, JAN[0] + ((nx - 1) * STEP + BL / 2) * RES,
                  JAN[3] - ((ny - 1) * STEP + BL / 2) * RES, JAN[3] - BL * RES / 2],
          cmap="autumn", alpha=0.75)
ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0], CASO[3] - CASO[1],
                       fill=False, edgecolor="cyan", lw=1.5))
ax.set_title("Periodicidade linear 3-9 m (p97) — candidatos a estrutura de "
             "latada/linha. SEM indice de vegetacao.", fontsize=9)
fig.savefig(os.path.join(OUT, "ctrl_02_mapa.png"), bbox_inches="tight")
plt.close(fig)
print("-> ctrl_02_mapa.png  ctrl_02_candidatos.csv")
