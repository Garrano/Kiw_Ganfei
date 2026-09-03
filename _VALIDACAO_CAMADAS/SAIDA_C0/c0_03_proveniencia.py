# -*- coding: utf-8 -*-
"""C0-03. Proveniencia das 11 cenas contra o catalogo STAC Earth Search.

Para cada ID de proveniencia.json:
  - o item existe no catalogo?
  - a data do item bate com a data do ficheiro?
  - baseline de processamento e earthsearch:boa_offset_applied
  - nuvens declaradas
  - a AOI esta dentro do footprint do item?
E, independentemente: pesquisa TODAS as cenas de plena estacao disponiveis
sobre a AOI, para ver se a escolha de datas deixou de fora cenas limpas.
"""
import json
import os
import numpy as np
import requests

BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
API = "https://earth-search.aws.element84.com/v1"
AOI = (529950, 4654600, 531950, 4655600)
LON, LAT = -8.62601, 42.04734

prov = json.load(open(os.path.join(BASE, "sentinel", "proveniencia.json")))
res = []
print("=" * 100)
print("%-12s %-28s %-8s %-6s %-6s %-8s %-7s %s"
      % ("data_fich", "id", "data_STAC", "base", "boa", "nuvens", "AOI_in",
         "plataforma"))
print("=" * 100)
for c in prov["cenas"]:
    cid = c["cena"]
    r = requests.get("%s/collections/sentinel-2-l2a/items/%s" % (API, cid),
                     timeout=90)
    if r.status_code != 200:
        print("%-12s %-28s  *** HTTP %d — NAO EXISTE ***"
              % (c["data"], cid, r.status_code))
        res.append(dict(data=c["data"], id=cid, existe=False))
        continue
    it = r.json()
    p = it["properties"]
    dstac = p["datetime"][:10]
    base = p.get("s2:processing_baseline", p.get("processing:version", "?"))
    boa = p.get("earthsearch:boa_offset_applied", None)
    nuv = p.get("eo:cloud_cover", None)
    # footprint
    g = it["geometry"]
    ring = g["coordinates"][0] if g["type"] == "Polygon" else g["coordinates"][0][0]
    xs = [q[0] for q in ring]
    ys = [q[1] for q in ring]
    dentro = (min(xs) < LON < max(xs)) and (min(ys) < LAT < max(ys))
    print("%-12s %-28s %-8s %-6s %-6s %-8.4f %-7s %s"
          % (c["data"], cid, dstac, base, boa, nuv or -1, dentro,
             p.get("platform", "?")))
    res.append(dict(data=c["data"], id=cid, existe=True, data_stac=dstac,
                    baseline=str(base), boa_offset_applied=boa,
                    nuvens=nuv, aoi_no_footprint=bool(dentro),
                    plataforma=p.get("platform"),
                    mgrs=p.get("grid:code", p.get("s2:mgrs_tile"))))
    if dstac != c["data"]:
        print("      *** DATA NAO BATE: ficheiro %s vs STAC %s ***"
              % (c["data"], dstac))

# ---------------------------------------------------- procura independente
print()
print("=" * 100)
print("PROCURA INDEPENDENTE — todas as cenas <10% nuvem sobre a AOI, "
      "Jun a Set, 2017-2026")
print("=" * 100)
q = dict(collections=["sentinel-2-l2a"],
         intersects={"type": "Point", "coordinates": [LON, LAT]},
         datetime="2017-01-01T00:00:00Z/2026-12-31T23:59:59Z",
         query={"eo:cloud_cover": {"lt": 10}}, limit=100)
todas = []
nxt = "%s/search" % API
body = dict(q)
while nxt:
    rr = requests.post(nxt, json=body, timeout=120).json()
    todas += rr.get("features", [])
    links = {l["rel"]: l for l in rr.get("links", [])}
    if "next" in links and len(todas) < 900:
        nxt = links["next"]["href"]
        body = links["next"].get("body", body)
    else:
        nxt = None
print("total de itens <10%% nuvem 2017-2026: %d" % len(todas))
usadas = set(c["cena"] for c in prov["cenas"])
porano = {}
for f in todas:
    p = f["properties"]
    d = p["datetime"][:10]
    mes = int(d[5:7])
    if not (6 <= mes <= 9):
        continue
    porano.setdefault(d[:4], []).append((d, f["id"], p.get("eo:cloud_cover", 99)))
print()
print("cenas de Jun-Set com <10%% nuvem, por ano (* = usada na serie):")
for ano in sorted(porano):
    L = sorted(porano[ano])
    marc = ["%s%s(%.1f%%)" % ("*" if i in usadas else " ", d[5:], n)
            for d, i, n in L]
    print("  %s  n=%2d  %s" % (ano, len(L), " ".join(marc)))

json.dump({"cenas": res, "disponiveis_jun_set": {a: [[d, i, n] for d, i, n in
                                                     sorted(v)]
                                                 for a, v in porano.items()}},
          open(os.path.join(OUT, "c0_03_proveniencia.json"), "w"), indent=1)
print("\n-> c0_03_proveniencia.json")
