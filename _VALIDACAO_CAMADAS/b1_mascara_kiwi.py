# -*- coding: utf-8 -*-
"""B1 — mascara so das faixas de kiwi, e a serie refeita sobre elas.

Porque
------
A serie do B1 corrida antes usava os poligonos C1a/C1b/C1c da sessao do
controlo externo. Esses poligonos sao INVOLUCROS: envolvem o conjunto de
parcelas, e la dentro alternam faixas de pergola com faixas lavradas e prado.
O teste temporal mostrou 46% das celulas com variabilidade inter-anual acima
do percentil 90 do kiwi — ou seja, quase metade nao se comporta como perene.
O esboco de rega diz o mesmo pelo seu lado: as faixas coloridas sao os
sectores regados, as brancas nao sao nada.

Metodo
------
1. ESTRUTURA, da ortofoto de 2021 a 25 cm. A pergola le-se pelas faixas de
   cobertura clara ao longo das linhas. Reduz-se a grelha de 10 m e fica-se
   com a fraccao de cobertura por celula.
2. VALIDACAO TEMPORAL, independente: desvio padrao do NDVI nos nove Veroes.
   O kiwi do corpo principal tem DP mediano de 0,0275. Uma celula de pergola
   nao pode ter variabilidade de cultura anual.
3. So entram na mascara as celulas que passam nas DUAS. Uma sozinha nao
   chega: a estrutura pode confundir estufa com pergola, e a estabilidade
   temporal pode confundir prado permanente com perene.

O que esta mascara NAO resolve
------------------------------
Onde acaba a valvula 1 e comecam as 2-5. Isso continua por saber, e nenhuma
banda o resolve: o porta-enxerto esta debaixo do chao.
"""
import json
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds, reproject, Resampling
from rasterio.transform import from_origin
from rasterio.features import geometry_mask
from scipy import ndimage, stats

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
W = (529300, 4653800, 530300, 4654600)
DESTINO = from_origin(W[0], W[3], 10.0, 10.0)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])

ctrl = json.load(open("../_VALIDACAO_CAMADAS/SAIDA_C0/controlos.geojson"))
env = ~geometry_mask([f["geometry"] for f in ctrl["features"]
                      if f["properties"].get("id") in ("C1a", "C1b", "C1c")],
                     out_shape=(80, 100), transform=DESTINO, invert=False)

# --- 1. estrutura ----------------------------------------------------------
def cobertura(caminho):
    ds = rasterio.open(caminho)
    Wo = transform_bounds("EPSG:32629", ds.crs, *W)
    w = from_bounds(*Wo, transform=ds.transform)
    rgb = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).astype("float32")
    lum = rgb.mean(2)
    sat = rgb.max(2) - rgb.min(2)
    clara = ((lum > np.percentile(lum, 72)) & (sat < 42)).astype("float32")
    fora = np.zeros((80, 100), "float32")
    reproject(clara, fora,
              src_transform=rasterio.windows.transform(w, ds.transform),
              src_crs=ds.crs, dst_transform=DESTINO, dst_crs="EPSG:32629",
              resampling=Resampling.average)
    return fora


c21 = cobertura("orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif")
c25 = cobertura("orto/ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
estrutura = (np.maximum(c21, c25) > 0.30)
print("estrutura de cobertura (2021 ou 2025): %d celulas = %.2f ha"
      % ((estrutura & env).sum(), (estrutura & env).sum() / 100))

# --- 2. estabilidade temporal ---------------------------------------------
prov = {c["data"]: c["cena"] for c in
        json.load(open("sentinel/proveniencia.json"))["cenas"]}
pil = []
for dt in DATAS:
    a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     "sentinel-2-l2a/items/" + prov[dt], timeout=90).json()["assets"]

    def rd(k):
        with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
            return ds.read(1, window=from_bounds(*W, transform=ds.transform)
                           ).astype("float32")

    r, n = rd("red"), rd("nir")
    pil.append((n - r) / (n + r))
P = np.stack(pil)
dp = P.std(0)

g = json.load(open("sentinel/masks_geograficas.json"))
POM = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)
REF = np.array([[c == "1" for c in L] for L in g["saudavel_bits"]], bool)
M = np.stack([rasterio.open("sentinel/%s.tif" % d).read(1) for d in DATAS])
lim = float(np.percentile(M.std(0)[POM], 75))
estavel = dp < lim
print("estabilidade temporal (DP < %.4f, p75 do kiwi): %d celulas dentro do envelope"
      % (lim, (estavel & env).sum()))

KIWI = ndimage.binary_opening(env & estrutura & estavel, np.ones((2, 2)))
print("\nMASCARA DE KIWI DO B1 (as duas condicoes): %d celulas = %.2f ha"
      % (KIWI.sum(), KIWI.sum() / 100))
print("   contra 13,52 ha do envelope — sobra %.0f%%" % (100 * KIWI.sum() / env.sum()))

if KIWI.sum() < 20:
    print("\nMASCARA DEMASIADO PEQUENA — nao se corre serie sobre isto.")
    raise SystemExit

v = np.array([float(np.nanmean(P[i][KIWI])) for i in range(len(DATAS))])
rf = np.array([float(np.nanmean(M[i][REF])) for i in range(len(DATAS))])
print("\nSERIE DO B1, so nas faixas de kiwi\n")
print("   data         B1-kiwi   referência   fosso")
for i, d in enumerate(DATAS):
    print("   %s   %.4f    %.4f     %+.4f" % (d, v[i], rf[i], rf[i] - v[i]))
for nome, s in (("B1 kiwi — nível absoluto", v), ("fosso à referência", rf - v)):
    r = stats.linregress(anos, s)
    print("\n%-28s %.3f -> %.3f   declive %+.5f/ano  p=%.4f"
          % (nome, s[0], s[-1], r.slope, r.pvalue))
np.save("b1_mascara_kiwi.npy", KIWI)
print("\nb1_mascara_kiwi.npy gravado")
