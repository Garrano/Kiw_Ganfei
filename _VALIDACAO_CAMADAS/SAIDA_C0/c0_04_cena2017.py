# -*- coding: utf-8 -*-
"""C0-04. A cena de 2017-07-02 e a primeira da serie. Toda a classificacao
«ja em defice na primeira cena» depende dela. Testa-se se ela e comparavel:

 a) dia-do-ano de cada cena da serie, contra as duas excluidas por fenologia;
 b) variancia da referencia sa por data;
 c) descarrega cenas alternativas de 2017 (12-07, 11-08, 31-08) do AWS e
    recalcula, para cada uma, a mascara de defice e a area «ja em defice na
    primeira cena» — se a area mudar muito, a classificacao e artefacto de data;
 d) verifica empiricamente o degrau de harmonizacao BOA, comparando DN brutos
    de alvos estaveis (agua e area urbana) entre 2021 e 2022.
"""
import json
import os
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from matplotlib.path import Path as MP

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
CACHE = os.path.join(OUT, "cenas_extra")
os.makedirs(CACHE, exist_ok=True)
API = "https://earth-search.aws.element84.com/v1"
AOI = (529950, 4654600, 531950, 4655600)
H, W = 100, 200
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
yy, xx = np.mgrid[0:H, 0:W]
pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(H, W) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
pomar = mk["pomar"]

DATAS = ["2017-07-02", "2018-08-31", "2019-09-02", "2020-07-18", "2021-07-16",
         "2022-07-31", "2023-08-07", "2024-07-22", "2025-06-17", "2025-08-14",
         "2026-07-27"]
FORA = {"2019-09-02", "2025-06-17"}


def doy(d):
    import datetime
    return datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10])).timetuple().tm_yday


print("=" * 78)
print("a) DIA DO ANO — a regra de fenologia e consistente?")
print("=" * 78)
for d in DATAS:
    print("  %s  DOY=%3d  %s" % (d, doy(d),
                                 "EXCLUIDA por fenologia" if d in FORA else "usada"))
usa = [doy(d) for d in DATAS if d not in FORA]
print("  usadas: DOY min=%d max=%d amplitude=%d dias"
      % (min(usa), max(usa), max(usa) - min(usa)))
print("  2018-08-31 (DOY %d) FICA; 2019-09-02 (DOY %d) SAI -> %d dias de "
      "diferenca" % (doy("2018-08-31"), doy("2019-09-02"),
                     doy("2019-09-02") - doy("2018-08-31")))
print("  2025-06-17 (DOY %d) SAI; 2017-07-02 (DOY %d) FICA -> %d dias de "
      "diferenca" % (doy("2025-06-17"), doy("2017-07-02"),
                     doy("2017-07-02") - doy("2025-06-17")))


def ler(d):
    with rasterio.open(os.path.join(BASE, "sentinel", d + ".tif")) as ds:
        return ds.read(1)


ND = {d: ler(d) for d in DATAS}
print()
print("=" * 78)
print("b) DISPERSAO DA REFERENCIA SA POR DATA")
print("=" * 78)
for d in DATAS:
    v = ND[d][sau]
    print("  %s  media=%.4f  dp=%.4f  p05=%.4f  min=%.4f  n<0.70=%d"
          % (d, np.nanmean(v), np.nanstd(v), np.nanpercentile(v, 5),
             np.nanmin(v), int((v < 0.70).sum())))


# --------------------------------------------- c) cenas alternativas de 2017
def baixa(cid, data, aoi=AOI, w=W, h=H):
    dst = os.path.join(CACHE, data + "_" + cid + ".tif")
    if os.path.exists(dst):
        with rasterio.open(dst) as ds:
            return ds.read(1)
    a = requests.get("%s/collections/sentinel-2-l2a/items/%s" % (API, cid),
                     timeout=120).json()["assets"]

    def rd(k, shape=None):
        with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
            win = from_bounds(*aoi, transform=ds.transform)
            if shape is None:
                return (ds.read(1, window=win),
                        ds.window_transform(win), ds.crs)
            return (ds.read(1, window=win, out_shape=shape,
                            resampling=Resampling.nearest), None, None)

    red, tr, crs = rd("red")
    nir, _, _ = rd("nir")
    scl, _, _ = rd("scl", red.shape)
    red = red.astype("float32")
    nir = nir.astype("float32")
    with np.errstate(invalid="ignore", divide="ignore"):
        nd = (nir - red) / (nir + red)
    nd[np.isin(scl, [0, 1, 3, 8, 9, 10])] = np.nan
    with rasterio.open(dst, "w", driver="GTiff", height=nd.shape[0],
                       width=nd.shape[1], count=1, dtype="float32", crs=crs,
                       transform=tr, nodata=np.nan, compress="deflate") as o:
        o.write(nd, 1)
    return nd


ALT2017 = [("2017-07-02", "S2B_29TNG_20170702_0_L2A"),
           ("2017-07-12", "S2B_29TNG_20170712_0_L2A"),
           ("2017-08-11", "S2B_29TNG_20170811_0_L2A"),
           ("2017-08-18", "S2B_29TNG_20170818_0_L2A"),
           ("2017-08-31", "S2B_29TNG_20170831_0_L2A")]

print()
print("=" * 78)
print("c) A PRIMEIRA CENA — quatro datas de 2017, mesma AOI, mesmo metodo")
print("=" * 78)
print("  data        ref_media ref_dp  pomar_med  frac_pomar_em_defice  "
      "area_defice_ha")
alt = {}
for data, cid in ALT2017:
    try:
        nd = baixa(cid, data)
    except Exception as e:                                   # noqa: BLE001
        print("  %s  FALHOU: %s" % (data, e))
        continue
    if nd.shape != (H, W):
        print("  %s  forma inesperada %s" % (data, nd.shape))
        continue
    alt[data] = nd
    ref = float(np.nanmean(nd[sau]))
    dfc = (nd < ref - 0.05) & pomar
    print("  %s   %.4f   %.4f   %.4f      %5.1f%%             %.2f"
          % (data, ref, float(np.nanstd(nd[sau])), float(np.nanmean(nd[pomar])),
             100 * dfc.sum() / pomar.sum(), dfc.sum() / 100.0))

print()
print("  Concordancia da mascara de defice entre as quatro datas de 2017")
ks = list(alt)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a = (alt[ks[i]] < np.nanmean(alt[ks[i]][sau]) - 0.05) & pomar
        b = (alt[ks[j]] < np.nanmean(alt[ks[j]][sau]) - 0.05) & pomar
        iou = (a & b).sum() / max((a | b).sum(), 1)
        print("    %s vs %s :  IoU=%.3f   so em A=%d px   so em B=%d px"
              % (ks[i], ks[j], iou, (a & ~b).sum(), (b & ~a).sum()))

# --------------------------- efeito na classe «nunca esteve sao» da M2
print()
print("=" * 78)
print("c2) EFEITO DA PRIMEIRA CENA na classe «nunca esteve sao» (regra da M2)")
print("=" * 78)
PLENA = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
ANOS = [int(d[:4]) for d in PLENA]


def m2_classes(primeira_nd):
    defs = []
    for i, d in enumerate(PLENA):
        nd = primeira_nd if i == 0 else ND[d]
        defs.append((nd < float(np.nanmean(nd[sau])) - 0.05) & pomar)
    D = np.stack(defs)
    incid = D.sum(0) / len(PLENA)
    inicio = np.zeros(D.shape[1:], int)
    for i in range(len(PLENA) - 1):
        novo = (inicio == 0) & D[i] & D[i + 1]
        inicio[novo] = ANOS[i]
    sao_antes = np.zeros(D.shape[1:], bool)
    for i in range(len(PLENA) - 1):
        if i == 0:
            continue
        ainda = inicio == ANOS[i]
        sao_antes |= ainda & ~D[0] & ((~D[:i]).mean(0) >= 0.5)
    nunca = (inicio > 0) & ~sao_antes
    return D, incid, inicio, sao_antes, nunca


for data in ALT2017:
    d0 = data[0]
    if d0 not in alt:
        continue
    D, incid, inicio, sao, nunca = m2_classes(alt[d0])
    print("  primeira cena = %s :  «nunca sao» = %4d px = %5.2f ha   |  "
          "«declinou» = %4d px = %5.2f ha   |  em defice em 2017 = %4d px"
          % (d0, nunca.sum(), nunca.sum() / 100.0, sao.sum(), sao.sum() / 100.0,
             D[0].sum()))

# ----------------------------------------- d) degrau BOA empirico
print()
print("=" * 78)
print("d) HARMONIZACAO BOA — DN brutos de alvos estaveis")
print("=" * 78)
IDS = [("2017-07-02", "S2B_29TNG_20170702_0_L2A"),
       ("2018-08-31", "S2A_29TNG_20180831_1_L2A"),
       ("2020-07-18", "S2A_29TNG_20200718_1_L2A"),
       ("2021-07-16", "S2A_29TNG_20210716_1_L2A"),
       ("2022-07-31", "S2A_29TNG_20220731_0_L2A"),
       ("2023-08-07", "S2B_29TNG_20230807_0_L2A"),
       ("2026-07-27", "S2C_29TNG_20260727_0_L2A")]
# janela larga; os alvos sao escolhidos pelo SCL, nao adivinhados
JAN = (526000, 4652000, 534000, 4658000)
CLASSES = {"agua (SCL 6)": 6, "sem_veg (SCL 5)": 5}
dados = {}
for data, cid in IDS:
    a = requests.get("%s/collections/sentinel-2-l2a/items/%s" % (API, cid),
                     timeout=120).json()["assets"]
    with rasterio.Env(**ENV), rasterio.open(a["scl"]["href"]) as ds:
        scl = ds.read(1, window=from_bounds(*JAN, transform=ds.transform))
    v = {}
    for k in ("red", "nir"):
        with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
            v[k] = ds.read(1, window=from_bounds(*JAN, transform=ds.transform),
                           out_shape=scl.shape,
                           resampling=Resampling.nearest).astype("float64")
    dados[data] = (scl, v["red"], v["nir"])
comum = {}
for nome, cl in CLASSES.items():
    m = np.ones_like(list(dados.values())[0][0], bool)
    for scl, _, _ in dados.values():
        m &= (scl == cl)
    comum[nome] = m
    print("  pixeis %s comuns a todas as datas: %d" % (nome, m.sum()))
print()
print("  %-12s %-16s %9s %9s %9s" % ("data", "alvo", "red_med", "nir_med",
                                     "ndvi"))
for data, _ in IDS:
    scl, red, nir = dados[data]
    for nome, m in comum.items():
        if m.sum() < 20:
            continue
        r, n = red[m].mean(), nir[m].mean()
        print("  %-12s %-16s %9.1f %9.1f %9.4f"
              % (data, nome, r, n, (n - r) / (n + r + 1e-9)))

print("\nfeito")
