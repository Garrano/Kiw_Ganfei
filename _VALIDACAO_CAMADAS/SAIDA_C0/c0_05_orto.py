# -*- coding: utf-8 -*-
"""C0-05. Ortofotos DGT: cobertura, CRS, e o teste da AOI alargada.

 1. metadados de cada ortofoto (CRS, extensao, resolucao) e se cobrem a AOI
    e a AOI alargada 700 m em cada direccao;
 2. recorte RGB da AOI alargada a partir da ortofoto de 2025 (25 cm), com a
    AOI e o poligono `pomar` desenhados por cima — para ver se a AOI corta
    pomar a sul, leste ou oeste;
 3. deteccao de copado de pomar na ortofoto de 2025 por textura/verde, dentro
    e fora do poligono, para responder «onde estao as outras ~16 ha».
"""
import json
import os
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
BUF = 700
AOI_L = (AOI[0] - BUF, AOI[1] - BUF, AOI[2] + BUF, AOI[3] + BUF)
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))

print("=" * 96)
print("1. ORTOFOTOS DGT — metadados e cobertura")
print("=" * 96)
fich = sorted(f for f in os.listdir(os.path.join(BASE, "orto"))
              if f.endswith(".tif"))
info = []
for f in fich:
    p = os.path.join(BASE, "orto", f)
    with rasterio.open(p) as ds:
        b = ds.bounds
        crs = ds.crs
        res = (ds.transform.a, -ds.transform.e)
        nb = ds.count
        try:
            b32629 = transform_bounds(crs, "EPSG:32629", *b, densify_pts=21)
        except Exception:                                     # noqa: BLE001
            b32629 = None
    cob = cobl = None
    if b32629:
        cob = (b32629[0] <= AOI[0] and b32629[1] <= AOI[1]
               and b32629[2] >= AOI[2] and b32629[3] >= AOI[3])
        cobl = (b32629[0] <= AOI_L[0] and b32629[1] <= AOI_L[1]
                and b32629[2] >= AOI_L[2] and b32629[3] >= AOI_L[3])
    print("  %-52s %-12s res=%.2f m nb=%d" % (f[:52], str(crs), res[0], nb))
    print("      extensao em 32629: " +
          str(tuple(int(x) for x in b32629) if b32629 else "?"))
    print("      cobre AOI: %s   cobre AOI+700m: %s" % (cob, cobl))
    info.append(dict(ficheiro=f, crs=str(crs), res=res[0], bandas=nb,
                     bounds_32629=[float(x) for x in b32629] if b32629 else None,
                     cobre_aoi=bool(cob), cobre_aoi_alargada=bool(cobl)))

json.dump(info, open(os.path.join(OUT, "c0_05_orto_meta.json"), "w"), indent=1)

# ------------------------------------------------------------------ recortes
ORTO25 = os.path.join(BASE, "orto",
                      "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")


def recorte(caminho, jan32629, alvo_px=2400):
    with rasterio.open(caminho) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan32629, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        esc = max(1, int(max(win.width, win.height) / alvo_px))
        h = int(win.height / esc)
        w = int(win.width / esc)
        n = min(ds.count, 4)
        arr = ds.read(list(range(1, n + 1)), window=win, out_shape=(n, h, w),
                      boundless=True, fill_value=0)
    return arr, jb


print()
print("=" * 96)
print("2. RECORTE DA AOI ALARGADA (+700 m) NA ORTOFOTO DE 2025")
print("=" * 96)
arr, jb = recorte(ORTO25, AOI_L, 3000)
rgb = np.moveaxis(arr[:3], 0, -1).astype("float32")
rgb = np.clip(rgb / max(np.percentile(rgb, 99.5), 1), 0, 1)
print("  janela lida %s  forma %s" % (tuple(int(x) for x in AOI_L), rgb.shape))

fig, ax = plt.subplots(figsize=(16, 12), dpi=150)
ax.imshow(rgb, extent=[AOI_L[0], AOI_L[2], AOI_L[1], AOI_L[3]])
ax.add_patch(Rectangle((AOI[0], AOI[1]), AOI[2] - AOI[0], AOI[3] - AOI[1],
                       fill=False, edgecolor="yellow", lw=2.5))
pol = np.array(masks["pomar"])
ax.add_patch(MPoly(np.column_stack([AOI[0] + pol[:, 0] * 10.0,
                                    AOI[3] - pol[:, 1] * 10.0]),
                   closed=True, fill=False, edgecolor="red", lw=2.0))
for e in range(int(AOI_L[0]) // 200 * 200, int(AOI_L[2]), 200):
    ax.axvline(e, color="w", lw=0.25, alpha=0.35)
for n in range(int(AOI_L[1]) // 200 * 200, int(AOI_L[3]), 200):
    ax.axhline(n, color="w", lw=0.25, alpha=0.35)
ax.set_title("Ortofoto DGT 2025 (25 cm) — AOI a amarelo, poligono `pomar` a "
             "vermelho, AOI alargada +700 m", fontsize=10)
ax.set_xlabel("E (EPSG:32629)")
ax.set_ylabel("N (EPSG:32629)")
fig.savefig(os.path.join(OUT, "c0_05_aoi_alargada_2025.png"),
            bbox_inches="tight")
plt.close(fig)
print("  -> c0_05_aoi_alargada_2025.png")

# recorte so da AOI, a resolucao maior
arr2, _ = recorte(ORTO25, AOI, 4000)
rgb2 = np.moveaxis(arr2[:3], 0, -1).astype("float32")
rgb2 = np.clip(rgb2 / max(np.percentile(rgb2, 99.5), 1), 0, 1)
fig, ax = plt.subplots(figsize=(20, 10), dpi=170)
ax.imshow(rgb2, extent=[AOI[0], AOI[2], AOI[1], AOI[3]])
ax.add_patch(MPoly(np.column_stack([AOI[0] + pol[:, 0] * 10.0,
                                    AOI[3] - pol[:, 1] * 10.0]),
                   closed=True, fill=False, edgecolor="red", lw=1.6))
for k, c in (("zona0", "cyan"), ("manchaW", "magenta"),
             ("saudavel", "lime"), ("saudavel_2", "lime"),
             ("saudavel_3", "lime")):
    q = np.array(masks[k])
    ax.add_patch(MPoly(np.column_stack([AOI[0] + q[:, 0] * 10.0,
                                        AOI[3] - q[:, 1] * 10.0]),
                       closed=True, fill=False, edgecolor=c, lw=1.4))
ax.set_title("AOI sobre ortofoto 2025 — pomar(vermelho) zona0(ciano) "
             "manchaW(magenta) saudavel x3(verde)", fontsize=10)
fig.savefig(os.path.join(OUT, "c0_05_aoi_mascaras_2025.png"),
            bbox_inches="tight")
plt.close(fig)
print("  -> c0_05_aoi_mascaras_2025.png")
