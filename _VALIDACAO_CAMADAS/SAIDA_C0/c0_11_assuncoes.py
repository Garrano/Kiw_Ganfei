# -*- coding: utf-8 -*-
"""C0-11. Tarefa 6 — outras assuncoes geometricas por confirmar.

 a) AOI do LiDAR (lidar/dem_aoi.json, EPSG:3763) cobre a AOI Sentinel?
 b) coordenadas do traco de 1995: caem dentro do poligono `pomar`? e os dois
    pontos REF batem com os centroides medidos das mascaras?
 c) bacia.json: bbox e area declarada — a bbox tem mesmo 36,9 ha?
 d) distancias citadas: 1,06 km do «lobulo oeste»; distancia manchaW-zona0.
 e) eixo real da parcela (PCA do poligono `pomar`) — para as fronteiras da M1.
 f) AOI alargada 700 m em Sentinel-2: o copado e cortado a S, E ou W?
"""
import json
import os
import numpy as np
import rasterio
import requests
from pyproj import Transformer
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
AOI = (529950, 4654600, 531950, 4655600)
B1 = (528400, 4654900, 529400, 4655700)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
t2929_3763 = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
t3763_2929 = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)


def utm(k):
    p = np.array(masks[k])
    return AOI[0] + p[:, 0] * 10.0, AOI[3] - p[:, 1] * 10.0


# ------------------------------------------------------------- a) LiDAR
print("=" * 74)
print("a) AOI DO LiDAR")
print("=" * 74)
for nome, fj in (("dem_aoi", "dem_aoi.json"), ("t2_dem1m", "t2_dem1m.json")):
    j = json.load(open(os.path.join(BASE, "lidar", fj)))
    tr = j["transform"]
    h, w = j["shape"]
    x0, y0 = tr[2], tr[5]
    x1 = x0 + w * tr[0]
    y1 = y0 + h * tr[4]
    print("  %-9s EPSG:%s  x %.1f..%.1f  y %.1f..%.1f  (%.0f x %.0f m)"
          % (nome, j["crs"].split(":")[-1], x0, x1, min(y0, y1), max(y0, y1),
             abs(x1 - x0), abs(y1 - y0)))
    cx, cy = [], []
    for E in (AOI[0], AOI[2]):
        for N in (AOI[1], AOI[3]):
            a, b = t2929_3763.transform(E, N)
            cx.append(a)
            cy.append(b)
    cobre = (min(cx) >= min(x0, x1) and max(cx) <= max(x0, x1)
             and min(cy) >= min(y0, y1) and max(cy) <= max(y0, y1))
    print("      AOI Sentinel em 3763: x %.1f..%.1f  y %.1f..%.1f -> cobre: %s"
          % (min(cx), max(cx), min(cy), max(cy), cobre))
    if not cobre:
        print("      *** o LiDAR NAO cobre a AOI toda ***")

# --------------------------------------------------------- b) traco de 1995
print()
print("=" * 74)
print("b) COORDENADAS DO TRACO DE 1995")
print("=" * 74)
import csv                                                      # noqa: E402
p = os.path.join(BASE, "_pacote_cowork", "tracos_1995_coordenadas.csv")
PE, PN = utm("pomar")
caminho = MP(np.column_stack([PE, PN]))
mwE, mwN = utm("manchaW")
z0E, z0N = utm("zona0")
cmw = (mwE.mean(), mwN.mean())
cz0 = (z0E.mean(), z0N.mean())
for r in csv.DictReader(open(p, encoding="utf-8")):
    E, N = float(r["UTM29N_E"]), float(r["UTM29N_N"])
    dentro = bool(caminho.contains_point((E, N)))
    # coerencia das tres representacoes de coordenadas
    m, pp = t2929_3763.transform(E, N)
    dm = np.hypot(m - float(r["PT-TM06_M"]), pp - float(r["PT-TM06_P"]))
    print("  %-32s E%d N%d  dentro do pomar: %-5s  erro TM06: %.1f m"
          % (r["elemento"][:32], E, N, dentro, dm))
print("  centroide medido de manchaW: E%.0f N%.0f   (CSV diz E530470 N4655060"
      " -> %.0f m)" % (cmw[0], cmw[1], np.hypot(cmw[0] - 530470,
                                                cmw[1] - 4655060)))
print("  centroide medido de zona0  : E%.0f N%.0f   (CSV diz E531000 N4655090"
      " -> %.0f m)" % (cz0[0], cz0[1], np.hypot(cz0[0] - 531000,
                                                cz0[1] - 4655090)))

# ------------------------------------------------------------------ c) bacia
print()
print("=" * 74)
print("c) bacia.json")
print("=" * 74)
b = json.load(open(os.path.join(BASE, "lidar", "bacia.json")))
lo0, la0, lo1, la1 = b["bbox_wgs84"]
t4326_2929 = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
x0, y0 = t4326_2929.transform(lo0, la0)
x1, y1 = t4326_2929.transform(lo1, la1)
print("  bbox em UTM: E %.0f..%.0f  N %.0f..%.0f  = %.0f x %.0f m = %.1f ha"
      % (x0, x1, y0, y1, x1 - x0, y1 - y0, (x1 - x0) * (y1 - y0) / 1e4))
print("  «ha» declarado no ficheiro: %.1f  -> a bbox NAO e a area da bacia"
      % b["ha"])
print("  a bbox cobre o poligono `pomar`? E: %s  N: %s"
      % (x0 <= PE.min() and x1 >= PE.max(), y0 <= PN.min() and y1 >= PN.max()))
print("  poligono `pomar`: E %.0f..%.0f  N %.0f..%.0f"
      % (PE.min(), PE.max(), PN.min(), PN.max()))

# ------------------------------------------------------------ d) distancias
print()
print("=" * 74)
print("d) DISTANCIAS CITADAS")
print("=" * 74)
cb1 = ((B1[0] + B1[2]) / 2, (B1[1] + B1[3]) / 2)
cpo = (PE.mean(), PN.mean())
print("  centro AOI b1 -> centroide do poligono `pomar`: %.0f m"
      % np.hypot(cb1[0] - cpo[0], cb1[1] - cpo[1]))
print("  centro AOI b1 -> ponto mais proximo do poligono: %.0f m"
      % np.min(np.hypot(PE - cb1[0], PN - cb1[1])))
print("  «1,06 km» citado: nao reproduzivel por nenhuma destas medidas")
print("  centroide manchaW -> centroide zona0: %.0f m"
      % np.hypot(cmw[0] - cz0[0], cmw[1] - cz0[1]))
d = np.min(np.hypot(mwE[:, None] - z0E[None, :], mwN[:, None] - z0N[None, :]))
print("  bordo a bordo manchaW/zona0: %.0f m" % d)

# ------------------------------------------------------------ e) eixo da parcela
print()
print("=" * 74)
print("e) EIXO REAL DA PARCELA (PCA do poligono `pomar`, ponderado por area)")
print("=" * 74)
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mkp = MP(masks["pomar"]).contains_points(pts).reshape(100, 200)
ys, xs = np.where(mkp)
E = AOI[0] + xs * 10.0 + 5
N = AOI[3] - ys * 10.0 - 5
X = np.column_stack([E, N])
Xc = X - X.mean(0)
u, s, vt = np.linalg.svd(Xc, full_matrices=False)
az = np.degrees(np.arctan2(vt[0, 0], vt[0, 1])) % 180
print("  centroide: E%.0f N%.0f" % (X.mean(0)[0], X.mean(0)[1]))
print("  eixo maior: azimute %.1f graus (0=N, 90=E)   -> %.1f graus acima "
      "da horizontal E-W" % (az, 90 - az))
pr1 = Xc @ vt[0]
pr2 = Xc @ vt[1]
print("  extensao ao longo do eixo: %.0f m ; transversal: %.0f m"
      % (pr1.max() - pr1.min(), pr2.max() - pr2.min()))
print("  extremos do eixo: E%.0f N%.0f  ->  E%.0f N%.0f"
      % (X.mean(0)[0] + pr1.min() * vt[0][0], X.mean(0)[1] + pr1.min() * vt[0][1],
         X.mean(0)[0] + pr1.max() * vt[0][0], X.mean(0)[1] + pr1.max() * vt[0][1]))
json.dump({"centroide": X.mean(0).tolist(), "eixo": vt[0].tolist(),
           "transversal": vt[1].tolist(), "azimute_deg": float(az),
           "comprimento_m": float(pr1.max() - pr1.min()),
           "largura_m": float(pr2.max() - pr2.min()),
           "t_min": float(pr1.min()), "t_max": float(pr1.max())},
          open(os.path.join(OUT, "c0_11_eixo.json"), "w"), indent=1)

# --------------------------------------------------- f) AOI alargada Sentinel
print()
print("=" * 74)
print("f) AOI ALARGADA 700 m — o copado e cortado?")
print("=" * 74)
GR = (AOI[0] - 700, AOI[1] - 700, AOI[2] + 700, AOI[3] + 700)
cid = "S2C_29TNG_20260727_0_L2A"
a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                 "sentinel-2-l2a/items/" + cid, timeout=120).json()["assets"]


def rd(k):
    with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
        return ds.read(1, window=from_bounds(*GR, transform=ds.transform)
                       ).astype("float32")


red, nir = rd("red"), rd("nir")
with np.errstate(invalid="ignore", divide="ignore"):
    nd = (nir - red) / (nir + red)
h, w = nd.shape
print("  janela alargada %s -> %dx%d px" % (str(GR), w, h))
ex, ey = GR[0], GR[3]
alto = nd > 0.78
# faixas de 100 m junto a cada bordo da AOI original, dentro e fora
for lado, dentro, fora in (
        ("oeste", (AOI[0], AOI[0] + 100), (AOI[0] - 100, AOI[0])),
        ("este", (AOI[2] - 100, AOI[2]), (AOI[2], AOI[2] + 100)),
        ("sul", None, None), ("norte", None, None)):
    if lado in ("oeste", "este"):
        def frac(a, b, ymin=AOI[1], ymax=AOI[3]):
            c0 = int((a - ex) / 10)
            c1 = int((b - ex) / 10)
            r0 = int((ey - ymax) / 10)
            r1 = int((ey - ymin) / 10)
            return 100 * np.nanmean(alto[r0:r1, c0:c1])
        print("  bordo %-6s NDVI>0,78: dentro %.1f%%  fora %.1f%%"
              % (lado, frac(*dentro), frac(*fora)))
    else:
        y_in = (AOI[1], AOI[1] + 100) if lado == "sul" else (AOI[3] - 100, AOI[3])
        y_out = (AOI[1] - 100, AOI[1]) if lado == "sul" else (AOI[3], AOI[3] + 100)

        def fr(y0, y1):
            r0 = int((ey - y1) / 10)
            r1 = int((ey - y0) / 10)
            c0 = int((AOI[0] - ex) / 10)
            c1 = int((AOI[2] - ex) / 10)
            return 100 * np.nanmean(alto[r0:r1, c0:c1])
        print("  bordo %-6s NDVI>0,78: dentro %.1f%%  fora %.1f%%"
              % (lado, fr(*y_in), fr(*y_out)))

fig, ax = plt.subplots(figsize=(18, 11), dpi=140)
im = ax.imshow(nd, extent=[GR[0], GR[2], GR[1], GR[3]], cmap="RdYlGn",
               vmin=0.1, vmax=0.95)
ax.add_patch(Rectangle((AOI[0], AOI[1]), AOI[2] - AOI[0], AOI[3] - AOI[1],
                       fill=False, edgecolor="black", lw=2))
ax.add_patch(Rectangle((B1[0], B1[1]), B1[2] - B1[0], B1[3] - B1[1],
                       fill=False, edgecolor="blue", lw=2, ls="--"))
ax.text(B1[0] + 20, B1[1] + 30, "AOI «b1» — EM QUARENTENA", color="blue",
        fontsize=9, fontweight="bold")
ax.add_patch(MPoly(np.column_stack(utm("pomar")), closed=True, fill=False,
                   edgecolor="black", lw=1.4))
plt.colorbar(im, ax=ax, shrink=0.7, label="NDVI 2026-07-27")
ax.set_title("NDVI 2026-07-27 na AOI alargada 700 m — AOI a preto, "
             "AOI b1 a azul tracejado", fontsize=11)
fig.savefig(os.path.join(OUT, "c0_11_aoi_alargada_ndvi.png"),
            bbox_inches="tight")
plt.close(fig)
print("  -> c0_11_aoi_alargada_ndvi.png")
