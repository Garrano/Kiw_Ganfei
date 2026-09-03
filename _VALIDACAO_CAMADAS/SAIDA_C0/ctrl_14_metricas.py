# -*- coding: utf-8 -*-
"""CTRL-14. Metricas geometricas dos candidatos a controlo + geojson.

Para cada poligono: area, distancia ao pomar do caso (bordo e centroide),
cota LiDAR (media, min, max, amplitude, desvio), lado do rio, distancia a
margem e altura sobre o plano de agua.

Superficie de agua: obtida da ortofoto de 2025 por luminancia baixa e azul
dominante. E um criterio de AGUA, nao de vegetacao; nao entra NIR nem indice.

Tambem reporta as quantidades-ancora do CONTROLOS.md que sao geometricas.
"""
import glob
import json
import os
import numpy as np
import rasterio
from matplotlib.path import Path as MPath
from pyproj import Transformer
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
ORTO = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
AOI = (529950, 4654600, 531950, 4655600)
JAN = (528600.0, 4653000.0, 531790.0, 4655780.0)   # janela da agua
T32_37 = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
T32_43 = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)


# ------------------------------------------------------------------- agua
def superficie_agua(jan, res=2.0):
    with rasterio.open(ORTO) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0).astype("float32")
    lum = a.mean(0)
    agua = (lum < np.percentile(lum[lum > 0], 12)) & (a[2] >= a[0] - 2) \
        & (lum > 0)
    agua = ndimage.binary_opening(agua, np.ones((5, 5)))
    agua = ndimage.binary_closing(agua, np.ones((9, 9)))
    lab, n = ndimage.label(agua, np.ones((3, 3)))
    if n:
        tam = ndimage.sum(agua, lab, range(1, n + 1))
        agua = lab == (int(tam.argmax()) + 1)
    print("agua: %.1f ha na janela %s" % (agua.sum() * res ** 2 / 1e4,
                                          tuple(int(x) for x in jan)))
    return agua, res


AGUA, ARES = superficie_agua(JAN)
DIST = ndimage.distance_transform_edt(~AGUA) * ARES


def dist_agua(E, N):
    j = int((E - JAN[0]) / ARES)
    i = int((JAN[3] - N) / ARES)
    if 0 <= i < DIST.shape[0] and 0 <= j < DIST.shape[1]:
        return float(DIST[i, j])
    return float("nan")


# ------------------------------------------------------------------ LiDAR
MDT = sorted(glob.glob(os.path.join(BASE, "lidar", "MDT-*.tif")))


def cotas(pol):
    """Cotas LiDAR dentro do poligono (32629), amostradas a 2 m."""
    e0, e1 = pol[:, 0].min(), pol[:, 0].max()
    n0, n1 = pol[:, 1].min(), pol[:, 1].max()
    ee, nn = np.meshgrid(np.arange(e0, e1 + 2, 2.0),
                         np.arange(n0, n1 + 2, 2.0))
    dentro = MPath(pol).contains_points(np.column_stack([ee.ravel(),
                                                         nn.ravel()]))
    P = np.column_stack([ee.ravel(), nn.ravel()])[dentro]
    if not len(P):
        return None
    x3, y3 = T32_37.transform(P[:, 0], P[:, 1])
    v = np.full(len(P), np.nan)
    for f in MDT:
        with rasterio.open(f) as ds:
            b = ds.bounds
            k = np.isnan(v) & (x3 >= b.left) & (x3 < b.right) \
                & (y3 >= b.bottom) & (y3 < b.top)
            if not k.any():
                continue
            s = np.array(list(ds.sample(np.column_stack([x3[k], y3[k]]),
                                        indexes=1)), float).ravel()
            nd = ds.nodata
            if nd is not None:
                s[s == nd] = np.nan
            s[s < -100] = np.nan
            v[k] = s
    return v[np.isfinite(v)]


def area_ha(p):
    x = np.append(p[:, 0], p[0, 0])
    y = np.append(p[:, 1], p[0, 1])
    return abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])) / 2.0 / 1e4


def dist_bordo(pol, rect):
    """Distancia minima entre o poligono e o rectangulo do pomar do caso."""
    ex = np.linspace(rect[0], rect[2], 200)
    ny_ = np.linspace(rect[1], rect[3], 120)
    bordo = np.vstack([
        np.column_stack([ex, np.full_like(ex, rect[1])]),
        np.column_stack([ex, np.full_like(ex, rect[3])]),
        np.column_stack([np.full_like(ny_, rect[0]), ny_]),
        np.column_stack([np.full_like(ny_, rect[2]), ny_])])
    # densifica o poligono
    d = []
    for i in range(len(pol)):
        a, b = pol[i], pol[(i + 1) % len(pol)]
        t = np.linspace(0, 1, max(2, int(np.hypot(*(b - a)) / 5) + 1))
        d.append(a + (b - a) * t[:, None])
    P = np.vstack(d)
    dd = np.hypot(P[:, 0][:, None] - bordo[:, 0][None, :],
                  P[:, 1][:, None] - bordo[:, 1][None, :])
    return float(dd.min())


# --------------------------------------------------------------- entrada
def carrega():
    c = []
    j = json.load(open(os.path.join(OUT, "ctrl_13_blocoSW.json")))
    nomes = {2: ("C1a", "bloco SW — parcela norte"),
             9: ("C1b", "bloco SW — parcela central e sul"),
             13: ("C1c", "bloco SW — parcela de estufas, extremo SO")}
    for p in j["parcelas"]:
        if p["id"] in nomes:
            cid, desc = nomes[p["id"]]
            c.append((cid, desc, np.array(p["vertices"][:-1], float),
                      "material de cobertura, ortofoto 2025 25 cm, "
                      "fecho 14 m, Douglas-Peucker 4 m"))
    for f, cid, desc in ((("ctrl_10_C2_vinha_NO.json"), "C2",
                          "vinha ribeirinha a NO do pomar do caso"),
                         (("ctrl_10_C3_vinha_S.json"), "C3",
                          "vinha a sul do pomar do caso")):
        j = json.load(open(os.path.join(OUT, f)))
        p = max(j["parcelas"], key=lambda s: s["area_ha"])
        c.append((cid, desc, np.array(p["vertices"], float),
                  "periodicidade linear 2,5-9 m, ortofoto 2025 25 cm, "
                  "inveltorio convexo da mancha"))
    return c


CX, CY = (CASO[0] + CASO[2]) / 2, (CASO[1] + CASO[3]) / 2
feats = []
print()
print("=" * 100)
print("CANDIDATOS")
print("=" * 100)
for cid, desc, pol, prov in carrega():
    a = area_ha(pol)
    cx, cy = pol[:, 0].mean(), pol[:, 1].mean()
    dc = float(np.hypot(cx - CX, cy - CY))
    db = dist_bordo(pol, CASO)
    v = cotas(pol)
    da = dist_agua(cx, cy)
    lon, lat = T32_43.transform(cx, cy)
    r = dict(id=cid, descricao=desc, area_ha=round(a, 2),
             centroide=[round(float(cx), 1), round(float(cy), 1)],
             centroide_wgs84=[round(float(lat), 6), round(float(lon), 6)],
             dist_centroide_m=round(dc, 0), dist_bordo_m=round(db, 0),
             dist_margem_m=round(da, 0),
             cota_media_m=None if v is None else round(float(v.mean()), 2),
             cota_min_m=None if v is None else round(float(v.min()), 2),
             cota_max_m=None if v is None else round(float(v.max()), 2),
             cota_amplitude_m=None if v is None
             else round(float(v.max() - v.min()), 2),
             cota_dp_m=None if v is None else round(float(v.std()), 2),
             n_amostras_lidar=0 if v is None else int(v.size),
             proveniencia_limite=prov)
    print("%-4s %-42s %6.2f ha  d_centro=%4.0f m  d_bordo=%4.0f m  "
          "cota %6.2f (%.2f..%.2f, dp %.2f, n=%d)  margem=%.0f m"
          % (cid, desc[:42], a, dc, db,
             -99 if v is None else v.mean(),
             -99 if v is None else v.min(),
             -99 if v is None else v.max(),
             -99 if v is None else v.std(),
             0 if v is None else v.size, da))
    feats.append((r, pol))

# cotas do pomar do caso, so para referencia de contexto (nao e analise dele)
polc = np.array([[CASO[0], CASO[1]], [CASO[2], CASO[1]],
                 [CASO[2], CASO[3]], [CASO[0], CASO[3]]], float)
vc = cotas(polc)
print()
print("rectangulo declarado do pomar do caso (so para referencia de cota):")
print("  cota media %.2f m, %.2f..%.2f, dp %.2f, n=%d"
      % (vc.mean(), vc.min(), vc.max(), vc.std(), vc.size))

# -------------------------------------------------------------- ancoras
print()
print("=" * 100)
print("QUANTIDADES-ANCORA (CONTROLOS.md) — so as que sao geometricas")
print("=" * 100)
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
print("AOI declarada: %s" % (AOI,))
for k in ("pomar", "zona0", "manchaW", "saudavel", "saudavel_2", "saudavel_3"):
    if k not in masks:
        continue
    q = np.array(masks[k], float)
    E = AOI[0] + q[:, 0] * 10.0
    N = AOI[3] - q[:, 1] * 10.0
    pol = np.column_stack([E, N])
    gx, gy = np.meshgrid(np.arange(AOI[0] + 5, AOI[2], 10.0),
                         np.arange(AOI[3] - 5, AOI[1], -10.0))
    d = MPath(pol).contains_points(np.column_stack([gx.ravel(), gy.ravel()]))
    print("  %-11s poligono: %8.2f ha ; %5d pixeis de 10 m dentro"
          % (k, area_ha(pol), int(d.sum())))
cen = json.load(open(os.path.join(OUT, "c0_03_proveniencia.json"))) \
    if os.path.exists(os.path.join(OUT, "c0_03_proveniencia.json")) else None
if isinstance(cen, dict):
    print("  cenas listadas em c0_03_proveniencia.json: %s"
          % ", ".join(list(cen)[:3]))
print("  NDVI medio da referencia 2017-07-02 e 2026-07-27: NAO MEDIDO — "
      "esta sessao tem regra dura de nao tocar em indice de vegetacao.")

# --------------------------------------------------------------- geojson
gj = dict(type="FeatureCollection",
          name="controlos_externos_candidatos",
          crs=dict(type="name",
                   properties=dict(name="urn:ogc:def:crs:EPSG::32629")),
          features=[])
for r, pol in feats:
    coords = [[float(x), float(y)] for x, y in pol]
    coords.append(coords[0])
    gj["features"].append(dict(type="Feature", properties=r,
                               geometry=dict(type="Polygon",
                                             coordinates=[coords])))
coords = [[float(x), float(y)] for x, y in polc]
coords.append(coords[0])
gj["features"].append(dict(
    type="Feature",
    properties=dict(id="REF", descricao="rectangulo declarado do pomar do "
                    "caso — referencia de distancia, NAO analisado nesta "
                    "sessao", area_ha=round(area_ha(polc), 2),
                    cota_media_m=round(float(vc.mean()), 2),
                    cota_min_m=round(float(vc.min()), 2),
                    cota_max_m=round(float(vc.max()), 2),
                    proveniencia_limite="dado no enunciado (caixa envolvente)"),
    geometry=dict(type="Polygon", coordinates=[coords])))
os.makedirs(SAI, exist_ok=True)
json.dump(gj, open(os.path.join(SAI, "controlos.geojson"), "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print()
print("-> controlos.geojson  (%d feicoes, EPSG:32629)" % len(gj["features"]))
