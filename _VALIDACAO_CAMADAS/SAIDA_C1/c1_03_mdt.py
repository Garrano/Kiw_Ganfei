# -*- coding: utf-8 -*-
"""C1-03 — MDT proprio a 50 cm sobre a AOI inteira, a partir dos 21 mosaicos.

Nao usa `dem_aoi.npy`: esse foi construido as 10h27 com apenas 15 dos mosaicos
(so ficheiros ate a coluna 159), o que explica a lacuna de 198 m a leste da
G20. Os 21 mosaicos actuais cobrem a AOI toda (c1_01).

Produz:
  c1_03_dem50.npy   MDT 0,5 m em EPSG:3763 sobre a caixa envolvente da AOI
  c1_03_dem50.json  transform / shape / crs
  c1_03_camp50.npy  campanha de voo por celula (0=Ago2025, 1=Jan2026, -1=sem)
  c1_03_grelha.npz  por celula da grelha de 10 m: cota, declive, exposicao,
                    TPI(50 m), rugosidade(25 m), campanha dominante
"""
import glob, os, sys, json
import numpy as np
import rasterio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

LID = os.path.join(RAIZ, "lidar")
paths = sorted(glob.glob(os.path.join(LID, "MDT-50cm-*.tif")))
VOO = json.load(open(os.path.join(SAIDA, "c1_02_costura.json"), encoding="utf-8"))["campanhas"]
tid2camp = {}
for data, lst in VOO.items():
    for t in lst:
        tid2camp["1" + t.rstrip("-")] = 0 if data.startswith("2025") else 1

# ---- caixa envolvente da AOI em 3763, com folga de 300 m para o escoamento ----
FOLGA = 300.0
cantos = [(AOI[0], AOI[1]), (AOI[2], AOI[1]), (AOI[2], AOI[3]), (AOI[0], AOI[3])]
c = np.array([T_29_TO_3763.transform(*p) for p in cantos])
L = np.floor((c[:, 0].min() - FOLGA) * 2) / 2
R = np.ceil((c[:, 0].max() + FOLGA) * 2) / 2
B = np.floor((c[:, 1].min() - FOLGA) * 2) / 2
T = np.ceil((c[:, 1].max() + FOLGA) * 2) / 2
W = int(round((R - L) / 0.5)); H = int(round((T - B) / 0.5))
print("destino 3763: E %.1f..%.1f  N %.1f..%.1f  -> %d x %d px @0,5 m" % (L, R, B, T, W, H))

dem = np.full((H, W), np.nan, dtype=np.float32)
camp = np.full((H, W), -1, dtype=np.int8)
for p in paths:
    tid = os.path.basename(p)[10:16].rstrip("-")
    with rasterio.open(p) as s:
        b = s.bounds
        if b.right <= L or b.left >= R or b.top <= B or b.bottom >= T:
            continue
        x0, x1 = max(L, b.left), min(R, b.right)
        y0, y1 = max(B, b.bottom), min(T, b.top)
        c0 = int(round((x0 - b.left) / 0.5)); c1 = int(round((x1 - b.left) / 0.5))
        r0 = int(round((b.top - y1) / 0.5)); r1 = int(round((b.top - y0) / 0.5))
        v = s.read(1, window=((r0, r1), (c0, c1))).astype(np.float32)
    v[v == -999.0] = np.nan
    dc0 = int(round((x0 - L) / 0.5)); dr0 = int(round((T - y1) / 0.5))
    alvo = dem[dr0:dr0 + v.shape[0], dc0:dc0 + v.shape[1]]
    novo = np.isnan(alvo) & ~np.isnan(v)
    alvo[novo] = v[novo]
    camp[dr0:dr0 + v.shape[0], dc0:dc0 + v.shape[1]][novo] = tid2camp["1" + tid]

print("MDT: %.2f%% sem dado | cota %.2f..%.2f m" %
      (100 * np.isnan(dem).mean(), np.nanmin(dem), np.nanmax(dem)))
Tr = rasterio.Affine(0.5, 0, L, 0, -0.5, T)
np.save(os.path.join(SAIDA, "c1_03_dem50.npy"), dem)
np.save(os.path.join(SAIDA, "c1_03_camp50.npy"), camp)
json.dump({"transform": [Tr.a, Tr.b, Tr.c, Tr.d, Tr.e, Tr.f],
           "shape": [H, W], "crs": "EPSG:3763", "folga_m": FOLGA},
          open(os.path.join(SAIDA, "c1_03_dem50.json"), "w"), indent=1)

# ---------- derivadas a 50 cm ----------
def suaviza(a, k):
    """media movel quadrada de lado k px, tolerante a NaN, por soma acumulada."""
    v = np.nan_to_num(a, nan=0.0).astype(np.float64)
    m = (~np.isnan(a)).astype(np.float64)
    def box(x):
        cs = np.cumsum(np.cumsum(x, 0), 1)
        cs = np.pad(cs, ((1, 0), (1, 0)))
        h2 = k // 2
        r0 = np.clip(np.arange(x.shape[0]) - h2, 0, x.shape[0])
        r1 = np.clip(np.arange(x.shape[0]) + h2 + 1, 0, x.shape[0])
        c0 = np.clip(np.arange(x.shape[1]) - h2, 0, x.shape[1])
        c1 = np.clip(np.arange(x.shape[1]) + h2 + 1, 0, x.shape[1])
        return (cs[np.ix_(r1, c1)] - cs[np.ix_(r0, c1)]
                - cs[np.ix_(r1, c0)] + cs[np.ix_(r0, c0)])
    s, w = box(v), box(m)
    out = np.where(w > 0, s / np.maximum(w, 1e-9), np.nan)
    return out

# declive por diferencas centrais sobre o MDT suavizado a 2,5 m (ruido do LiDAR)
dsuave = suaviza(dem, 5).astype(np.float32)
gy, gx = np.gradient(dsuave, 0.5, 0.5)
declive = np.degrees(np.arctan(np.hypot(gx, gy))).astype(np.float32)
exposicao = (np.degrees(np.arctan2(-gx, gy)) % 360).astype(np.float32)

# TPI a 50 m: cota menos media local de 50 m
tpi = (dem - suaviza(dem, 101)).astype(np.float32)
# rugosidade: dp local a 25 m do residuo em relacao a superficie de 25 m
res25 = dem - suaviza(dem, 51)
rug25 = np.sqrt(np.maximum(suaviza(res25 ** 2, 51), 0)).astype(np.float32)
# residuo a 150 m: quanto uma celula esta acima/abaixo da vizinhanca larga
res150 = (dem - suaviza(dem, 301)).astype(np.float32)

# ---------- agregar a grelha de 10 m da C0 ----------
E29, N29 = centros_celulas()
X, Y = T_29_TO_3763.transform(E29.ravel(), N29.ravel())
col = ((np.asarray(X) - L) / 0.5).reshape(E29.shape)
row = ((T - np.asarray(Y)) / 0.5).reshape(E29.shape)

def agrega(campo, fn=np.nanmean, meia=10):
    """estatistica do campo a 0,5 m dentro de cada celula de 10 m."""
    out = np.full(E29.shape, np.nan, dtype=np.float32)
    for i in range(NL):
        for j in range(NC):
            r = int(round(row[i, j])); cc = int(round(col[i, j]))
            r0, r1 = max(0, r - meia), min(H, r + meia)
            c0, c1 = max(0, cc - meia), min(W, cc + meia)
            if r1 <= r0 or c1 <= c0:
                continue
            bl = campo[r0:r1, c0:c1]
            if np.isnan(bl).all():
                continue
            out[i, j] = fn(bl)
    return out

print("a agregar a grelha de 10 m ...")
g = dict(
    cota=agrega(dem), declive=agrega(declive), tpi=agrega(tpi),
    rug25=agrega(rug25), res150=agrega(res150),
    cota_dp=agrega(dem, np.nanstd),
)
# exposicao: media circular
sx = agrega(np.sin(np.radians(exposicao))); cx = agrega(np.cos(np.radians(exposicao)))
g["exposicao"] = (np.degrees(np.arctan2(sx, cx)) % 360).astype(np.float32)
g["campanha"] = agrega(camp.astype(np.float32), np.nanmean)

np.savez(os.path.join(SAIDA, "c1_03_grelha.npz"), **g)
masc, _ = carrega_mascaras()
p = masc["pomar"]
print("\ncelulas do pomar sem cota: %d" % np.isnan(g["cota"][p]).sum())
print("cota do pomar: %.3f .. %.3f m (mediana %.3f)" %
      (np.nanmin(g["cota"][p]), np.nanmax(g["cota"][p]), np.nanmedian(g["cota"][p])))
print("escrito c1_03_grelha.npz")
