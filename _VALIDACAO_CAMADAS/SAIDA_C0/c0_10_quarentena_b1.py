# -*- coding: utf-8 -*-
"""C0-10. Quarentena de sentinel_b1/: prova geografica e inventario completo.

 a) prova: a AOI b1 (528400,4654900,529400,4655700) contem o rio Minho e a
    cidade de Valenca? Mede-se pela classe SCL da propria cena de 2026 e pela
    ortofoto (se a cobrir), e mede-se a distancia ao poligono `pomar`;
 b) inventario: todos os ficheiros que derivam dessa AOI, com as colunas
    afectadas. NAO SE APAGA NADA.
"""
import csv
import json
import os
import re
import numpy as np
import rasterio
import requests
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from matplotlib.path import Path as MP

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
API = "https://earth-search.aws.element84.com/v1"
AOI = (529950, 4654600, 531950, 4655600)
B1 = (528400, 4654900, 529400, 4655700)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
SCL_NOME = {0: "sem dados", 1: "saturado", 2: "sombra/escuro", 3: "sombra nuvem",
            4: "vegetacao", 5: "sem vegetacao", 6: "agua", 7: "nao classif.",
            8: "nuvem media", 9: "nuvem alta", 10: "cirrus", 11: "neve"}

print("=" * 74)
print("a) O QUE HA DENTRO DA AOI b1, medido")
print("=" * 74)
cid = "S2C_29TNG_20260727_0_L2A"
a = requests.get("%s/collections/sentinel-2-l2a/items/%s" % (API, cid),
                 timeout=120).json()["assets"]
for nome, jan in (("AOI b1", B1), ("AOI principal", AOI)):
    with rasterio.Env(**ENV), rasterio.open(a["scl"]["href"]) as ds:
        scl = ds.read(1, window=from_bounds(*jan, transform=ds.transform))
    tot = scl.size
    print("  %s  (%d px de 20 m = %.0f ha)" % (nome, tot, tot * 400 / 1e4))
    for c in sorted(np.unique(scl)):
        print("      SCL %2d %-14s %6.2f %%"
              % (c, SCL_NOME.get(int(c), "?"), 100 * (scl == c).mean()))

# distancia do poligono `pomar` a AOI b1
masks = json.load(open(os.path.join(BASE, "sentinel", "masks.json")))
pol = np.array(masks["pomar"])
PE = AOI[0] + pol[:, 0] * 10.0
PN = AOI[3] - pol[:, 1] * 10.0
dx = np.maximum.reduce([B1[0] - PE, PE - B1[2], np.zeros_like(PE)])
dy = np.maximum.reduce([B1[1] - PN, PN - B1[3], np.zeros_like(PN)])
d = np.hypot(dx, dy)
print()
print("  distancia minima do poligono `pomar` a caixa da AOI b1: %.0f m"
      % d.min())
print("  distancia maxima: %.0f m" % d.max())
print("  ponto mais proximo do pomar: E%.0f N%.0f"
      % (PE[np.argmin(d)], PN[np.argmin(d)]))
print("  a AOI b1 NAO se sobrepoe a AOI principal: intervalo em E de %d m"
      % (AOI[0] - B1[2]))

# a ortofoto cobre a AOI b1?
o25 = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
with rasterio.open(o25) as ds:
    b = transform_bounds(ds.crs, "EPSG:32629", *ds.bounds, densify_pts=21)
print("  ortofoto 2025 em 32629: %s -> cobre a AOI b1: %s"
      % (tuple(int(x) for x in b),
         b[0] <= B1[0] and b[1] <= B1[1] and b[2] >= B1[2] and b[3] >= B1[3]))

# ------------------------------------------------------------- b) inventario
print()
print("=" * 74)
print("b) INVENTARIO DO QUE DERIVA DA AOI b1  (nada e apagado)")
print("=" * 74)
PADRAO = re.compile(r"sentinel_b1|528400|expansao_b1|b1_serie|b1_analise|"
                    r"b1_nucleo|Q5_b1|l[oó]bulo|lobulo", re.I)
RAIZES = [BASE, r"C:\Users\Jackster2\Downloads\_GANFEI_REEXECUCAO_CEGA"]
achados = []
for raiz in RAIZES:
    for dp, _, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, os.path.dirname(raiz))
            ext = os.path.splitext(f)[1].lower()
            if "sentinel_b1" in p.replace("/", "\\"):
                achados.append((rel, os.path.getsize(p),
                                "PRODUTO DIRECTO da AOI b1"))
                continue
            if ext not in (".py", ".csv", ".json", ".md", ".txt"):
                continue
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:                                  # noqa: BLE001
                continue
            hits = sorted(set(m.group(0).lower()
                              for m in PADRAO.finditer(t)))
            if hits:
                achados.append((rel, os.path.getsize(p),
                                "refere: " + ", ".join(hits[:6])))
achados.sort()
for rel, tam, nota in achados:
    print("  %-62s %8d B  %s" % (rel[:62], tam, nota))
print("  TOTAL: %d ficheiros" % len(achados))

# colunas afectadas nos CSV
print()
print("  colunas de CSV que contêm valores da AOI b1:")
for rel, _, _ in achados:
    if not rel.lower().endswith(".csv"):
        continue
    p = os.path.join(os.path.dirname(RAIZES[0]), rel)
    if not os.path.exists(p):
        continue
    try:
        r = csv.reader(open(p, encoding="utf-8", errors="replace"))
        cab = next(r)
    except Exception:                                          # noqa: BLE001
        continue
    cols = [c for c in cab if "b1" in c.lower()]
    if cols:
        print("    %-52s %s" % (os.path.basename(rel), ", ".join(cols)))

with open(os.path.join(OUT, "c0_10_inventario_b1.csv"), "w", newline="",
          encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ficheiro", "bytes", "razao"])
    w.writerows(achados)
print("\n-> c0_10_inventario_b1.csv")
