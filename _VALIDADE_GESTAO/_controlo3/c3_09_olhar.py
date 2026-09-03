# -*- coding: utf-8 -*-
"""Olhar para os tres blocos. A fraccao e um numero; a imagem e o instrumento.

Recorta 8845729, 8845731 e 8845739 em RGB nas epocas de 2012, 2018, 2021 e 2025 e
monta uma folha por bloco. Sem isto estou a fazer o que o A3 fez: decidir sobre a
identidade de uma unidade a partir de um indice.
"""
import json
import os
import sys

import numpy as np
import requests
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

Image.MAX_IMAGE_PIXELS = None
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
OUT = os.path.join(VG, "_controlo3")
CACHE = os.path.join(OUT, "_orto472062")
TRES = [8845729, 8845731, 8845739]
EP = [("2012", "Ortos2012-RGB"), ("2018", "Ortos2018-RGB"),
      ("2021", "Ortos2021-RGB"), ("2025", "Ortos2025-RGB")]
PX = 0.5

tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
G = {}
for ft in KF:
    c = ft["properties"].get("CUL_ID")
    if c is not None and int(c) in TRES:
        G[int(c)] = para(shape(ft["geometry"])).buffer(0)


def getmap(ano, camada, BB, NCx, NLy, tag):
    f = os.path.join(CACHE, "crop_%s_%s_%s.png" % (ano, camada, tag))
    if os.path.exists(f) and os.path.getsize(f) > 5000:
        return Image.open(f).convert("RGB")
    u = "https://cartografia.dgterritorio.gov.pt/wms/ortos%s" % ano
    p = {"service": "WMS", "request": "GetMap", "version": "1.1.1",
         "layers": camada, "styles": "", "srs": "EPSG:3763",
         "bbox": "%f,%f,%f,%f" % BB, "width": NCx, "height": NLy,
         "format": "image/png"}
    r = requests.get(u, params=p, timeout=600)
    if "image" not in (r.headers.get("Content-Type") or ""):
        raise IOError(r.text[:150])
    open(f, "wb").write(r.content)
    return Image.open(f).convert("RGB")


for cul in TRES:
    g = G[cul]
    b = g.bounds
    BB = (b[0] - 25, b[1] - 25, b[2] + 25, b[3] + 25)
    NCx, NLy = int((BB[2] - BB[0]) / PX), int((BB[3] - BB[1]) / PX)
    tiles = []
    for ano, cam in EP:
        try:
            im = getmap(ano, cam, BB, NCx, NLy, str(cul)).copy()
        except Exception as e:
            print("%d %s falhou: %s" % (cul, ano, str(e)[:80]))
            continue
        d = ImageDraw.Draw(im)
        xy = [((x - BB[0]) / PX, (BB[3] - y) / PX) for x, y in g.exterior.coords]
        d.line(xy + [xy[0]], fill=(255, 255, 0), width=3)
        d.text((8, 8), "%d  %s" % (cul, ano), fill=(255, 255, 0))
        tiles.append(im)
    if not tiles:
        continue
    W = sum(t.width for t in tiles) + 8 * (len(tiles) - 1)
    H = max(t.height for t in tiles)
    folha = Image.new("RGB", (W, H), (20, 20, 20))
    x = 0
    for t in tiles:
        folha.paste(t, (x, 0))
        x += t.width + 8
    esc = min(1.0, 1800.0 / W)
    folha = folha.resize((int(W * esc), int(H * esc)), Image.LANCZOS)
    p = os.path.join(OUT, "c3_09_%d.png" % cul)
    folha.save(p)
    print("escrito %s  (%d x %d)" % (p, folha.width, folha.height))
