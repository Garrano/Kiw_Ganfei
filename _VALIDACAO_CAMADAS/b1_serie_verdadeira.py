# -*- coding: utf-8 -*-
"""A serie do B1 — o verdadeiro, desta vez.

Historia curta deste ficheiro
-----------------------------
Durante semanas houve uma serie chamada "lobulo oeste B1" cuja AOI ficava na
cidade de Valenca, do outro lado do rio Minho. Media vegetacao urbana. Foi
retirada em 28-08-2026, com tudo o que dela dependia.

Depois disso, tres tentativas de o localizar falharam: por ancoras verbais
(escala 30% errada), por ajuste da forma do desenho (residuo de 64 m, maior
que o espacamento entre valvulas), e por contagem de fileiras ancorada nos
extremos da parcela (que a coordenada real do armazem desmentiu por 321 m).

O B1 foi finalmente localizado por duas coordenadas dadas pelo gestor:
    inicio  42.03757663, -8.64358173   ->  E 529500  N 4654010
    fim     42.04118411, -8.63687114   ->  E 530054  N 4654413
685 m de comprimento, azimute 54 graus, a 526 m do corpo principal.

E aterra exactamente sobre os blocos C1a e C1b, que a sessao do controlo
externo tinha delimitado na ortofoto sem nunca olhar para NDVI nenhum — e que
tinha proposto como CANDIDATOS A CONTROLO EXTERNO, perguntando apenas se
pertenciam a exploracao. Pertencem: sao o B1.

Duas consequencias
------------------
1. C1a e C1b deixam de ser controlo externo. Sao a mesma exploracao, a mesma
   origem de agua e a mesma gestao. A conclusao "nao existe controlo externo
   de kiwi contemporaneo neste aluviao" sai reforcada, nao enfraquecida.

2. As mascaras do B1 nasceram de uma sessao que nunca viu o sinal que agora se
   vai medir. E o oposto do defeito que tudo isto veio corrigir — em
   `fazer_masks_v2.py` o `pomar` era `nd2026 > 0.78` e a `manchaW` era
   `nd2026 < 0.76`, e media-se depois a evolucao ate 2026.

O que esta serie testa
----------------------
O gestor confirmou que as valvulas 2-5 do B1 tem raizes de SUMMER KIWI,
sobre-enxertadas com Enza Gold em 2016 e com Erica em 2020, e que o corpo
principal e Erica de PE FRANCO. E o unico contraste de porta-enxerto do caso.
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
AOI = (529950, 4654600, 531950, 4655600)
W_B1 = (529300, 4653800, 530300, 4654600)          # 1000 x 800 m sobre o B1
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])

ctrl = json.load(open("../_VALIDACAO_CAMADAS/SAIDA_C0/controlos.geojson"))
geoms = [f["geometry"] for f in ctrl["features"]
         if f["properties"].get("id") in ("C1a", "C1b")]
print("poligonos do B1 (C1a + C1b), delimitados sem NDVI: %d" % len(geoms))

prov = json.load(open("sentinel/proveniencia.json"))
cenas = {c["data"]: c["cena"] for c in prov["cenas"]}
g = json.load(open("sentinel/masks_geograficas.json"))
REF = np.array([[c == "1" for c in L] for L in g["saudavel_bits"]], bool)

tf = rasterio.transform.from_origin(W_B1[0], W_B1[3], 10.0, 10.0)
mask_b1 = ~geometry_mask(geoms, out_shape=(80, 100), transform=tf, invert=False)
print("mascara B1: %d celulas = %.2f ha" % (mask_b1.sum(), mask_b1.sum() / 100))

linhas = []
for d in DATAS:
    it = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                      "sentinel-2-l2a/items/" + cenas[d], timeout=90).json()
    a = it["assets"]
    off = it["properties"].get("earthsearch:boa_offset_applied", False)

    def rd(k):
        with rasterio.Env(**ENV), rasterio.open(a[k]["href"]) as ds:
            return ds.read(1, window=from_bounds(*W_B1, transform=ds.transform)
                           ).astype("float32")

    r, n = rd("red"), rd("nir")
    nd_b1 = (n - r) / (n + r)
    ref = float(np.nanmean(rasterio.open("sentinel/%s.tif" % d).read(1)[REF]))
    v = float(np.nanmean(nd_b1[mask_b1]))
    linhas.append((d, v, ref, ref - v, off))
    print("  %s  B1 %.4f | referencia %.4f | fosso %+.4f | offset BOA %s"
          % (d, v, ref, ref - v, off))

b1 = np.array([x[1] for x in linhas])
rf = np.array([x[2] for x in linhas])
fo = np.array([x[3] for x in linhas])
print("\n" + "=" * 70)
for nome, s in (("B1 — nível absoluto", b1),
                ("referência do corpo principal", rf),
                ("fosso: referência menos B1", fo)):
    r = stats.linregress(anos, s)
    print("%-32s %.3f -> %.3f   declive %+.5f/ano  p=%.4f"
          % (nome, s[0], s[-1], r.slope, r.pvalue))
print("=" * 70)
json.dump(dict(
    _b1_coordenadas={"inicio": [529500, 4654010], "fim": [530054, 4654413],
                     "fonte": "gestor, 28-08-2026"},
    _mascara="C1a + C1b de controlos.geojson, delimitados na ortofoto sem NDVI",
    _area_ha=round(mask_b1.sum() / 100, 2),
    serie=[dict(data=d, b1=round(v, 4), referencia=round(rr, 4),
                fosso=round(f, 4), boa_offset=o) for d, v, rr, f, o in linhas]),
    open("b1_serie_verdadeira.json", "w", encoding="utf-8"),
    ensure_ascii=False, indent=1)
print("b1_serie_verdadeira.json gravado")
