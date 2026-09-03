# -*- coding: utf-8 -*-
"""Serie densa intra-estacao — separar gestao de fisiologia.

A pergunta
----------
O analista independente A assinalou a lacuna mais incomoda do caso: nao ha uma
unica observacao de terreno, e **poda ou arranque de linhas dariam exactamente
o mesmo sinal que doenca**. Medimos com fiabilidade; nunca estabelecemos
validade.

A nota do gestor resolve-o com dados que ja existem: poda e arranque sao
verificaveis com imagens em datas proximas. As tres causas tem assinaturas
temporais diferentes, e o arquivo tem intervalo mediano de 2 a 3 dias.

    poda         queda abrupta entre cenas a dias de distancia, SEGUIDA de
                 recuperacao ao longo de semanas. Tem calendario.
    arranque     queda abrupta que NAO recupera; o pixel vai para solo e fica.
    fisiologico  declive suave dentro da estacao, sem descontinuidade entre
                 cenas consecutivas.

Com uma cena por ano — que e o que a cadeia inteira usou — nenhuma se separa
de nenhuma.

Desenho
-------
Todas as cenas Sentinel-2 L2A de Abril a Outubro, 2024 a 2026, com nuvem
declarada < 40 %, mascaradas pixel a pixel pelo SCL. NDVI medio por mascara em
cada data. Depois procuram-se saltos entre cenas CONSECUTIVAS, normalizados
pelo intervalo em dias, e compara-se cada mascara com a referencia na MESMA
cena — o que remove efeito de atmosfera, de sensor e de angulo.
"""
import json
import numpy as np
import rasterio
import requests
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")

g = json.load(open("sentinel/masks_geograficas.json"))
D = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
P, REF, Z, NU = D("pomar_bits"), D("saudavel_bits"), D("zona0_bits"), D("nu2021_bits")

nd26 = rasterio.open("sentinel/2026-07-27.tif").read(1)
r26 = float(np.nanmean(nd26[REF]))
dfc = ndimage.binary_opening((nd26 < r26 - 0.05) & P, np.ones((2, 2)))
lab, n = ndimage.label(dfc, np.ones((3, 3)))
FO = {}
for i in range(1, n + 1):
    m = lab == i
    if m.sum() < 50:
        continue
    ys, xs = np.where(m)
    FO["OESTE" if AOI[0] + xs.mean() * 10 < 530700 else "ESTE"] = m
MASC = [("foco OESTE", FO["OESTE"]),
        ("foco ESTE plantado", FO["ESTE"] & ~NU),
        ("resto do pomar", P & ~FO["OESTE"] & ~FO["ESTE"]),
        ("referencia", REF)]

tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1])
lo2, la2 = tr.transform(AOI[2], AOI[3])
busca = requests.post(
    "https://earth-search.aws.element84.com/v1/search",
    json={"collections": ["sentinel-2-l2a"], "bbox": [lo, la, lo2, la2],
          "datetime": "2024-01-01T00:00:00Z/2026-12-31T23:59:59Z",
          "query": {"eo:cloud_cover": {"lt": 40}}, "limit": 500},
    timeout=180).json()["features"]
cenas = []
for f in busca:
    dt = f["properties"]["datetime"][:10]
    if not (4 <= int(dt[5:7]) <= 10):
        continue
    a = f["assets"]
    if not all(a.get(k, {}).get("href", "").startswith("https://")
               for k in ("red", "nir", "scl")):
        continue
    cenas.append((dt, a, f["properties"].get("platform", "?")))
cenas.sort(key=lambda t: t[0])
print("cenas Abr-Out 2024-2026 utilizaveis: %d" % len(cenas))

linhas = []
for k, (dt, a, plat) in enumerate(cenas):
    try:
        def rd(b, **kw):
            with rasterio.Env(**ENV), rasterio.open(a[b]["href"]) as ds:
                return ds.read(1, window=from_bounds(*AOI, transform=ds.transform),
                               **kw)
        red = rd("red").astype("float32")
        nir = rd("nir").astype("float32")
        scl = rd("scl", out_shape=red.shape, resampling=Resampling.nearest)
        bom = np.isin(scl, [4, 5, 6, 7])
        nd = np.where(bom, (nir - red) / (nir + red + 1e-9), np.nan)
        reg = {}
        ok = True
        for nome, m in MASC:
            v = nd[m]
            v = v[np.isfinite(v)]
            if v.size < 0.6 * m.sum():
                ok = False
                break
            reg[nome] = float(np.mean(v))
        if ok:
            linhas.append(dict(data=dt, plataforma=plat, **reg))
    except Exception:
        pass
    if (k + 1) % 25 == 0:
        print("  %d/%d lidas, %d validas" % (k + 1, len(cenas), len(linhas)))

print("\ncenas com cobertura suficiente em todas as mascaras: %d" % len(linhas))
json.dump(linhas, open("serie_densa.json", "w"), indent=1)

import datetime as dtm
D_ = [dtm.date.fromisoformat(r["data"]) for r in linhas]
print("\nSALTOS ENTRE CENAS CONSECUTIVAS — fosso referencia menos mascara")
print("(o fosso na MESMA cena remove atmosfera, sensor e angulo)\n")
for nome, _ in MASC[:3]:
    f = np.array([r["referencia"] - r[nome] for r in linhas])
    dias = np.array([(D_[i + 1] - D_[i]).days for i in range(len(D_) - 1)])
    salto = np.diff(f)
    val = dias <= 12
    print("%s" % nome)
    print("   variacao do fosso entre cenas a <=12 dias: mediana %+.4f, "
          "DP %.4f, n=%d" % (np.median(salto[val]), np.std(salto[val]), val.sum()))
    grandes = np.where(val & (np.abs(salto) > 3 * np.std(salto[val])))[0]
    if grandes.size:
        print("   descontinuidades acima de 3 desvios:")
        for i in grandes:
            print("      %s -> %s (%d d)  fosso %+.4f -> %+.4f  salto %+.4f"
                  % (linhas[i]["data"], linhas[i + 1]["data"], dias[i],
                     f[i], f[i + 1], salto[i]))
    else:
        print("   nenhuma descontinuidade acima de 3 desvios")
    print()
