# -*- coding: utf-8 -*-
"""B1 por sub-blocos — a procurar o contraste de porta-enxerto.

O que se procura
----------------
O gestor confirmou: valvula 1 = pe franco de Erica; valvulas 2-5 = raizes de
SUMMER KIWI, sobre-enxertadas com Enza Gold em 2016 e com Erica por volta de
2020. E o unico contraste de porta-enxerto do caso, e esta dentro do MESMO
bloco — mesma agua, mesmo solo, mesma gestao, mesma posicao na rede.

O problema
----------
Nao se sabe onde acaba a valvula 1 e comecam as 2-5. As anotacoes dao linhas
149 (valvulas 1, 2 e 3) e 186-187 (valvulas 4 e 5), mas com numeracao propria
do B1 e sem se saber de que extremo conta. No esboco, a valvula 1 esta numa
parcela pequena e destacada, a sudoeste, fora do bloco estriado.

O que se faz em vez de adivinhar
--------------------------------
Duas particoes que nao dependem de saber onde estao as valvulas:

  A. Os tres poligonos que a sessao do controlo externo delimitou na ortofoto
     — C1a, C1b, C1c — sem nunca ter olhado para NDVI. Sao divisoes fisicas
     visiveis: caminhos, sebes, limites de parcela.

  B. Cortes de 100 m ao longo do eixo do bloco, do extremo SW ao NE.

Se houver um contraste de porta-enxerto, ele tem de aparecer como uma
descontinuidade numa destas particoes. Se nao aparecer em nenhuma, o contraste
nao e detectavel a 10 m — e isso tambem e resultado.
"""
import json
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from rasterio.features import geometry_mask
from scipy import stats

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
W = (529300, 4653800, 530300, 4654600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])
B1_INI = np.array([529500.0, 4654010.0])
B1_FIM = np.array([530054.0, 4654413.0])

ctrl = json.load(open("../_VALIDACAO_CAMADAS/SAIDA_C0/controlos.geojson"))
tf = rasterio.transform.from_origin(W[0], W[3], 10.0, 10.0)
sub = {}
for f in ctrl["features"]:
    pid = f["properties"].get("id")
    if pid in ("C1a", "C1b", "C1c"):
        sub[pid] = ~geometry_mask([f["geometry"]], out_shape=(80, 100),
                                  transform=tf, invert=False)
todo = sub["C1a"] | sub["C1b"] | sub["C1c"]

yy, xx = np.mgrid[0:80, 0:100]
E = W[0] + (xx + .5) * 10.0
N = W[3] - (yy + .5) * 10.0
u = (B1_FIM - B1_INI) / np.linalg.norm(B1_FIM - B1_INI)
d = (E - B1_INI[0]) * u[0] + (N - B1_INI[1]) * u[1]
CORTES = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500),
          (500, 600), (600, 700)]

g = json.load(open("sentinel/masks_geograficas.json"))
REF = np.array([[c == "1" for c in L] for L in g["saudavel_bits"]], bool)

serie = {}
for dt in DATAS:
    cena = [c for c in json.load(open("sentinel/proveniencia.json"))["cenas"]
            if c["data"] == dt][0]["cena"]
    a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     "sentinel-2-l2a/items/" + cena, timeout=90).json()["assets"]

    def rd(k):
        with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
            return ds.read(1, window=from_bounds(*W, transform=ds.transform)
                           ).astype("float32")

    r, n = rd("red"), rd("nir")
    serie[dt] = (n - r) / (n + r)
ref = {dt: float(np.nanmean(rasterio.open("sentinel/%s.tif" % dt).read(1)[REF]))
       for dt in DATAS}


def corre(nome, m):
    if m.sum() < 8:
        print("   %-28s  poucas células (%d)" % (nome, m.sum()))
        return
    v = np.array([float(np.nanmean(serie[dt][m])) for dt in DATAS])
    rr = stats.linregress(anos, v)
    print("   %-28s %5.2f ha  %.3f -> %.3f   %+.5f/ano  p=%.4f"
          % (nome, m.sum() / 100, v[0], v[-1], rr.slope, rr.pvalue))
    return v


print("A · SUB-BLOCOS FÍSICOS (delimitados sem NDVI)\n")
print("   %-28s %7s  %s" % ("", "área", "NDVI 2017 -> 2026   tendência"))
for k in ("C1c", "C1b", "C1a"):
    corre(k + "  (SW -> NE)", sub[k])
print("\nB · CORTES DE 100 m AO LONGO DO EIXO, do extremo SW ao NE\n")
guardado = {}
for a0, a1 in CORTES:
    m = todo & (d >= a0) & (d < a1)
    guardado[(a0, a1)] = corre("%3d–%3d m do início" % (a0, a1), m)
print("""
LEITURA
  A válvula 1 é, no esboço, uma parcela pequena e destacada no extremo
  sudoeste — que é o início do bloco, e portanto os primeiros cortes. Se o
  porta-enxerto fizer diferença, a descontinuidade tem de estar entre os
  primeiros 100–200 m e o resto. Não se afirma qual é a válvula 1: mede-se o
  bloco por partes e vê-se se ele é homogéneo ou não.""")
json.dump({"sub_blocos": {k: round(float(sub[k].sum()) / 100, 2) for k in sub},
           "cortes_m": [list(c) for c in CORTES],
           "_nota": "válvula 1 não localizada; partições físicas e geométricas"},
          open("b1_subblocos.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
