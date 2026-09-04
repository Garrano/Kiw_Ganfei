# -*- coding: utf-8 -*-
"""Substrato da carta-base de Ganfei: terreno, drenagem, sectores.

Produz os ficheiros que a P11 desenha. Separado do desenho de propósito: o
substrato demora e não muda; o desenho itera.

O QUE ENTRA
-----------
    MDT LiDAR 50 cm da DGT       7 folhas, EPSG:3763 -> reamostrado a 1 m em 32629
    parcelário IFAP 2025         cultura 124 (KIWI), WGS84 -> 32629
    tabela de válvulas do gestor valvulas_por_area.json (v6-17) + v4 (v1-5)

O QUE SAI
---------
    base_terreno.npz    cota, declive, sombreado, acumulação de escoamento
    base_sectores.json  polígonos dos cinco sectores em EPSG:32629

A REGRA DA PARTIÇÃO, escrita antes de correr
---------------------------------------------
O gestor nomeia cinco sectores — **B1, B2, Erica Novo, B3, B4** — e define-os
por **válvula**, não por parcela: o B1 é «as válvulas 1 a 5». As parcelas do
IFAP não coincidem com eles (uma parcela de 11,33 ha atravessa dois sectores).

Regra: **cada ponto de kiwi pertence ao sector da válvula mais próxima.** É uma
partição inferida e diz-se; o cadastro não a contém.

FALSIFICAÇÃO. A tabela do gestor declara a área de cada válvula. Se a partição
estiver certa, a área que ela dá a cada sector tem de bater com a soma das áreas
das válvulas desse sector. **Discrepância acima de 25 % em qualquer sector e a
partição não se usa** — desenha-se só as válvulas e as parcelas, sem sectores.

O B1 é a excepção e não precisa da regra: as suas seis parcelas do IFAP são
conhecidas (12,63 ha) e o sector é a união delas.
"""
import glob
import io
import json
import os

import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject
from pyproj import Transformer
from shapely.geometry import Point, shape, mapping
from shapely.ops import transform as sht, unary_union

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
PIX = 1.0
FOLGA = 260.0

T3763_29 = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)
T4326_29 = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)

# ── válvulas do gestor ──────────────────────────────────────────────────────
VA = json.load(io.open(os.path.join(D, "_VALIDACAO_CAMADAS/valvulas_por_area.json"),
                       encoding="utf-8"))
V4 = json.load(io.open(os.path.join(D, "ganfei_s2/valvulas_v4.json"), encoding="utf-8"))
VALV = {int(k): dict(E=v["E"], N=v["N"], bloco=v["bloco"], area_m2=v["area_m2"])
        for k, v in VA.items()}
for k, (e, n) in V4["lobo_oeste"].items():
    VALV[int(k)] = dict(E=e, N=n, bloco="B1", area_m2=None)
ORDEM = ["B1", "B2", "Erica Novo", "B3", "B4"]
SEC_VALV = {b: sorted(k for k, v in VALV.items() if v["bloco"] == b) for b in ORDEM}
print("sectores do gestor e as suas válvulas:")
for b in ORDEM:
    a = [VALV[k]["area_m2"] for k in SEC_VALV[b]]
    ha = sum(x for x in a if x) / 1e4
    print("  %-11s v%-22s %s" % (b, ",".join(str(k) for k in SEC_VALV[b]),
                                 "%5.2f ha declarados" % ha if ha else
                                 "área por válvula não declarada"))

# ── parcelas de kiwi ────────────────────────────────────────────────────────
CUL_B1 = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}
K = json.load(io.open(os.path.join(D, "_MULTIVERSO/SAIDA_H2_patologista/ifap_kiwi_largo.json"),
                      encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
PARC = {}
for f in KF:
    g = sht(lambda x, y, z=None: T4326_29.transform(x, y), shape(f["geometry"])).buffer(0)
    PARC[int(f["properties"]["CUL_ID"])] = g
pv = [Point(v["E"], v["N"]) for v in VALV.values()]
B1 = unary_union([PARC[c] for c in CUL_B1])
BANDA = unary_union([g for c, g in PARC.items()
                     if c not in CUL_B1 and min(g.distance(p) for p in pv) < 150])
print()
print("B1     %6.2f ha em %d parcelas" % (B1.area / 1e4, len(CUL_B1)))
print("banda  %6.2f ha  (o gestor declara 27,30 ha na R2 G35)" % (BANDA.area / 1e4))

# ── caixa e mosaico do terreno ──────────────────────────────────────────────
TUDO = unary_union([B1, BANDA])
x0, y0, x1, y1 = TUDO.bounds
BB = (x0 - FOLGA, y0 - FOLGA, x1 + FOLGA, y1 + FOLGA)
NC = int((BB[2] - BB[0]) / PIX)
NL = int((BB[3] - BB[1]) / PIX)
print()
print("caixa: E %.0f..%.0f  N %.0f..%.0f  ->  %d x %d células de %.1f m"
      % (BB[0], BB[2], BB[1], BB[3], NC, NL, PIX))

dst = np.full((NL, NC), np.nan, "float32")
tr = rasterio.transform.from_origin(BB[0], BB[3], PIX, PIX)
usadas = []
for p in sorted(glob.glob(os.path.join(D, "ganfei_s2/lidar/MDT-50cm-*.tif"))):
    with rasterio.open(p) as ds:
        b = ds.bounds
        xs, ys = T3763_29.transform([b.left, b.right, b.left, b.right],
                                    [b.bottom, b.bottom, b.top, b.top])
        if (max(xs) < BB[0] or min(xs) > BB[2]
                or max(ys) < BB[1] or min(ys) > BB[3]):
            continue
        tmp = np.full((NL, NC), np.nan, "float32")
        reproject(rasterio.band(ds, 1), tmp,
                  src_transform=ds.transform, src_crs=ds.crs,
                  dst_transform=tr, dst_crs="EPSG:32629",
                  src_nodata=ds.nodata, dst_nodata=np.nan,
                  resampling=Resampling.bilinear)
        m = np.isfinite(tmp) & ~np.isfinite(dst)
        dst[m] = tmp[m]
        usadas.append(os.path.basename(p))
print("folhas usadas: %d · %.1f %% da caixa com cota" % (len(usadas),
                                                         100 * np.isfinite(dst).mean()))
Z = dst
val = Z[np.isfinite(Z)]
print("cota: %.2f .. %.2f m  (p1 %.2f · p99 %.2f)"
      % (val.min(), val.max(), np.percentile(val, 1), np.percentile(val, 99)))

# ── declive e sombreado ─────────────────────────────────────────────────────
Zf = np.where(np.isfinite(Z), Z, np.nanmedian(Z))
gy, gx = np.gradient(Zf, PIX)
declive = np.degrees(np.arctan(np.hypot(gx, gy)))
asp = np.arctan2(-gx, gy)
incl = np.arctan(np.hypot(gx, gy))


def sombra(az_deg, alt_deg=40.0):
    az = np.radians(360.0 - az_deg + 90.0)
    alt = np.radians(alt_deg)
    return (np.sin(alt) * np.cos(incl)
            + np.cos(alt) * np.sin(incl) * np.cos(az - asp))


# sombreado multidireccional: um só azimute inventa lombas onde o terreno é
# plano, e este terreno tem 33 % de células planas (medido na C1-05).
S = np.mean([sombra(a) for a in (225.0, 270.0, 315.0, 360.0)], axis=0)
S = np.clip((S - np.nanpercentile(S, 2)) /
            (np.nanpercentile(S, 98) - np.nanpercentile(S, 2)), 0, 1)

# ── escoamento ──────────────────────────────────────────────────────────────
ACUM = None
try:
    from pysheds.grid import Grid
    import tempfile
    tmpf = os.path.join(tempfile.gettempdir(), "_base_dem.tif")
    with rasterio.open(tmpf, "w", driver="GTiff", height=NL, width=NC, count=1,
                       dtype="float32", crs="EPSG:32629", transform=tr,
                       nodata=-9999) as o:
        o.write(np.where(np.isfinite(Z), Z, -9999).astype("float32"), 1)
    grid = Grid.from_raster(tmpf)
    dem = grid.read_raster(tmpf)
    # os tres passos. Sem resolve_flats a acumulacao maxima cai por um factor
    # de 70 neste terreno — medido na C1-05, e a razao de estar aqui.
    dem = grid.fill_pits(dem)
    dem = grid.fill_depressions(dem)
    dem = grid.resolve_flats(dem)
    fdir = grid.flowdir(dem)
    ACUM = np.array(grid.accumulation(fdir), "float32")
    print("escoamento: acumulação máxima %.0f m² (com resolve_flats)"
          % (ACUM.max() * PIX * PIX))
except Exception as e:
    print("escoamento NÃO calculado: %s" % e)

# ── partição por válvula mais próxima, e a falsificação ─────────────────────
E, N = np.meshgrid(BB[0] + (np.arange(NC) + .5) * PIX,
                   BB[3] - (np.arange(NL) + .5) * PIX)
from matplotlib.path import Path as MP


def mascara(geo):
    m = np.zeros((NL, NC), bool)
    gs = geo.geoms if geo.geom_type == "MultiPolygon" else [geo]
    pts = np.column_stack([E.ravel(), N.ravel()])
    for g in gs:
        m |= MP(np.array(list(g.exterior.coords))).contains_points(pts).reshape(NL, NC)
    return m


MB1, MBA = mascara(B1), mascara(BANDA)
vk = sorted(k for k in VALV if VALV[k]["bloco"] != "B1")
dv = np.stack([np.hypot(E - VALV[k]["E"], N - VALV[k]["N"]) for k in vk])
maisperto = np.array(vk)[np.argmin(dv, axis=0)]
SEC = np.zeros((NL, NC), "int8")
COD = {b: i + 1 for i, b in enumerate(ORDEM)}
SEC[MB1] = COD["B1"]
for k in vk:
    SEC[MBA & (maisperto == k) & (SEC == 0)] = COD[VALV[k]["bloco"]]

print()
print("%-12s %10s %10s %8s" % ("sector", "partição", "declarado", "desvio"))
ok = True
areas = {}
for b in ORDEM:
    a = (SEC == COD[b]).sum() * PIX * PIX / 1e4
    areas[b] = a
    dec = sum(VALV[k]["area_m2"] or 0 for k in SEC_VALV[b]) / 1e4
    if b == "B1":
        dec = 12.63   # IFAP, seis parcelas — nao ha area declarada por valvula
    dif = 100 * (a - dec) / dec if dec else float("nan")
    print("%-12s %8.2f ha %8.2f ha %7.1f %%" % (b, a, dec, dif))
    if abs(dif) > 25:
        ok = False
print()
print("critério: desvio > 25 %% em qualquer sector => a partição NÃO se usa.")
print("-> %s" % ("PARTIÇÃO ACEITE" if ok else "PARTIÇÃO REJEITADA — desenhar só válvulas e parcelas"))

# ── saída ───────────────────────────────────────────────────────────────────
np.savez_compressed(os.path.join(AQUI, "base_terreno.npz"),
                    Z=Z.astype("float32"), sombra=S.astype("float32"),
                    declive=declive.astype("float32"), sector=SEC,
                    acum=(ACUM if ACUM is not None else np.zeros((1, 1), "float32")),
                    bb=np.array(BB), pix=PIX)
json.dump(dict(crs="EPSG:32629", bb=list(BB), pix=PIX,
               ordem=ORDEM, codigo=COD, particao_aceite=bool(ok),
               regra="cada ponto pertence ao sector da válvula mais próxima; "
                     "B1 é a união das suas seis parcelas do IFAP",
               valvulas={str(k): v for k, v in VALV.items()},
               areas_particao_ha={b: round(areas[b], 2) for b in ORDEM},
               parcelas_b1=sorted(CUL_B1),
               b1=mapping(B1), banda=mapping(BANDA),
               folhas_mdt=usadas),
          io.open(os.path.join(AQUI, "base_sectores.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print()
print("escritos base_terreno.npz e base_sectores.json")
