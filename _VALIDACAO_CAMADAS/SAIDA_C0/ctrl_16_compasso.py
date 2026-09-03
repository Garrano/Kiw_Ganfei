# -*- coding: utf-8 -*-
"""CTRL-16. Compasso entre linhas (m) e azimute das linhas, por bloco.

Espectro de Fourier da luminancia dentro de cada poligono, na ortofoto de 2025
a 25 cm. E uma medida de ESTRUTURA. Nao entra NIR nem indice.

O compasso e o unico numero que separa, por si so, uma latada de kiwi
(4,5-5,5 m no Minho) de um tunel de pequenos frutos (2-3,5 m) — e nao separa
uma latada de kiwi de um pomar de outra especie ao mesmo compasso. Por isso
vale como indicio, nunca como prova de especie.
"""
import json
import os
import numpy as np
import rasterio
from matplotlib.path import Path as MPath
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
RES = 0.5
BL = 128          # 64 m

gj = json.load(open(os.path.join(OUT, "controlos.geojson")))
fy = np.fft.fftfreq(BL)[:, None]
fx = np.fft.fftfreq(BL)[None, :]
fr = np.sqrt(fy ** 2 + fx ** 2)
with np.errstate(divide="ignore"):
    lam = RES / np.maximum(fr, 1e-9)
banda = (lam >= 1.8) & (lam <= 12.0)
jw = np.outer(np.hanning(BL), np.hanning(BL)).astype("float32")

print("%-5s %-46s %8s %8s %6s" % ("id", "descricao", "compasso",
                                  "azimute", "n"))
saida = {}
for f in gj["features"]:
    p = np.array(f["geometry"]["coordinates"][0])
    jan = (p[:, 0].min() - 5, p[:, 1].min() - 5,
           p[:, 0].max() + 5, p[:, 1].max() + 5)
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        W = int(round((jan[2] - jan[0]) / RES))
        H = int(round((jan[3] - jan[1]) / RES))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, H, W),
                    boundless=True, fill_value=0).astype("float32")
    lum = a.mean(0)
    gx, gy = np.meshgrid(jan[0] + (np.arange(W) + 0.5) * RES,
                         jan[3] - (np.arange(H) + 0.5) * RES)
    dentro = MPath(p).contains_points(
        np.column_stack([gx.ravel(), gy.ravel()])).reshape(H, W)
    ls, azs = [], []
    for i in range(0, H - BL, BL // 2):
        for j in range(0, W - BL, BL // 2):
            if not dentro[i:i + BL, j:j + BL].all():
                continue
            b = lum[i:i + BL, j:j + BL]
            if b.std() < 3:
                continue
            F = np.fft.fft2((b - b.mean()) * jw)
            pw = (F.real ** 2 + F.imag ** 2) * banda
            k = int(pw.argmax())
            ls.append(lam.flat[k])
            # azimute da NORMAL as linhas -> soma 90 para a direccao das linhas
            azs.append(np.degrees(np.arctan2(fx[0, k % BL], fy[k // BL, 0])))
    if not ls:
        print("%-5s %-46s %8s %8s %6d" % (f["properties"]["id"],
                                          f["properties"]["descricao"][:46],
                                          "-", "-", 0))
        continue
    L = float(np.median(ls))
    az = float(np.median(np.mod(np.array(azs) + 90.0, 180.0)))
    print("%-5s %-46s %6.2f m %6.1f g %6d"
          % (f["properties"]["id"], f["properties"]["descricao"][:46], L,
             az, len(ls)))
    saida[f["properties"]["id"]] = dict(compasso_m=round(L, 2),
                                        azimute_linhas_g=round(az, 1),
                                        n_janelas=len(ls))
json.dump(saida, open(os.path.join(OUT, "ctrl_16_compasso.json"), "w"),
          indent=1)
print("-> ctrl_16_compasso.json")
