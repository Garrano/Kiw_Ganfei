# -*- coding: utf-8 -*-
"""CTRL-15. Instrumento independente e mapa final.

1) Cada bloco visto num SEGUNDO sensor e numa TERCEIRA data — o WMS publico
   OrtoSat2023 da DGT (satelite, 2023) — para que a identificacao da estrutura
   nao dependa so do mosaico aereo local. Regra 1 do CONTROLOS.md.
2) Mapa final dos candidatos sobre a ortofoto de 2021 (com folha).

So R,G,B. Nenhum indice de vegetacao.
"""
import io
import json
import os
import numpy as np
import requests
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

requests.packages.urllib3.disable_warnings()
BASE = r"C:\Users\Jackster2\Downloads\ganfei_s2"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
WMS = "https://ortos.dgterritorio.gov.pt/wms/ortosat2023"
CASO = (530150.0, 4654870.0, 531520.0, 4655450.0)
T = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
JANELAS = [("C1 bloco SW", (529420, 4653800, 530120, 4654520)),
           ("C2 vinha NO", (530040, 4655300, 530420, 4655740)),
           ("C3 vinha S", (530180, 4654540, 530600, 4654900))]


def wms(jan, res=0.5):
    xs, ys = [], []
    for e in (jan[0], jan[2]):
        for n in (jan[1], jan[3]):
            x, y = T.transform(e, n)
            xs.append(x)
            ys.append(y)
    bb = (min(xs), min(ys), max(xs), max(ys))
    p = dict(service="WMS", version="1.1.1", request="GetMap",
             layers="ortoSat2023-CorVerdadeira", styles="", srs="EPSG:3763",
             bbox="%f,%f,%f,%f" % bb,
             width=int(round((bb[2] - bb[0]) / res)),
             height=int(round((bb[3] - bb[1]) / res)), format="image/png")
    r = requests.get(WMS, params=p, timeout=180, verify=False)
    r.raise_for_status()
    return np.asarray(Image.open(io.BytesIO(r.content)).convert("RGB"))


def norm(a):
    a = a.astype("float32")
    return np.clip(a / max(np.percentile(a, 99.3), 1.0), 0, 1)


gj = json.load(open(os.path.join(OUT, "controlos.geojson")))
pols = {f["properties"]["id"]: np.array(f["geometry"]["coordinates"][0])
        for f in gj["features"]}

fig, axs = plt.subplots(1, 3, figsize=(22, 8), dpi=160)
for ax, (nome, jan) in zip(axs, JANELAS):
    a = wms(jan)
    ax.imshow(norm(a), extent=[jan[0], jan[2], jan[1], jan[3]])
    for k, p in pols.items():
        if k == "REF":
            continue
        if (p[:, 0].min() < jan[2] and p[:, 0].max() > jan[0]
                and p[:, 1].min() < jan[3] and p[:, 1].max() > jan[1]):
            ax.plot(p[:, 0], p[:, 1], "-", color="red", lw=1.3)
            ax.text(p[:, 0].mean(), p[:, 1].mean(), k, color="yellow",
                    fontsize=8, ha="center")
    ax.set_title("%s — OrtoSat2023 (DGT), 2.o sensor, 3.a data" % nome,
                 fontsize=9)
    ax.tick_params(labelsize=5)
fig.savefig(os.path.join(OUT, "ctrl_15_instrumento_independente.png"),
            bbox_inches="tight")
plt.close(fig)
print("-> ctrl_15_instrumento_independente.png")

# ------------------------------------------------------------- mapa final
JAN = (529200.0, 4653600.0, 531790.0, 4655780.0)
ORTO21 = os.path.join(BASE, "orto", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif")
with rasterio.open(ORTO21) as ds:
    jb = transform_bounds("EPSG:32629", ds.crs, *JAN, densify_pts=21)
    win = from_bounds(*jb, transform=ds.transform)
    w = int(round((JAN[2] - JAN[0]) / 1.0))
    h = int(round((JAN[3] - JAN[1]) / 1.0))
    a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w), boundless=True,
                fill_value=0)
fig, ax = plt.subplots(figsize=(17, 17 * (JAN[3] - JAN[1]) / (JAN[2] - JAN[0])),
                       dpi=185)
ax.imshow(norm(np.moveaxis(a, 0, -1)),
          extent=[JAN[0], JAN[2], JAN[1], JAN[3]])
ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0],
                       CASO[3] - CASO[1], fill=False, edgecolor="white",
                       lw=1.8, ls="--"))
ax.text(CASO[0] + 30, CASO[1] + 30, "pomar do caso (referencia, nao analisado)",
        color="white", fontsize=6)
cores = dict(C1a="red", C1b="red", C1c="orange", C2="magenta", C3="cyan")
for k, p in pols.items():
    if k == "REF":
        continue
    ax.plot(p[:, 0], p[:, 1], "-", color=cores.get(k, "red"), lw=1.6)
    ax.text(p[:, 0].mean(), p[:, 1].mean(), k, color=cores.get(k, "red"),
            fontsize=9, ha="center", weight="bold")
for e in range(int(JAN[0]) // 250 * 250, int(JAN[2]) + 250, 250):
    if JAN[0] <= e <= JAN[2]:
        ax.axvline(e, color="w", lw=0.25, alpha=0.35)
for n in range(int(JAN[1]) // 250 * 250, int(JAN[3]) + 250, 250):
    if JAN[1] <= n <= JAN[3]:
        ax.axhline(n, color="w", lw=0.25, alpha=0.35)
ax.set_title("Candidatos a controlo externo — ortofoto DGT 2021 (25 cm, com "
             "folha), EPSG:32629, grelha 250 m", fontsize=10)
ax.tick_params(labelsize=6)
fig.savefig(os.path.join(OUT, "ctrl_15_mapa_controlos.png"),
            bbox_inches="tight")
plt.close(fig)
print("-> ctrl_15_mapa_controlos.png")
