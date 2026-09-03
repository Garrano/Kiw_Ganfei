# -*- coding: utf-8 -*-
"""CTRL-06. Alarga a prospeccao para LESTE e NORTE, onde o mosaico local
002-3 acaba (E 531800 / N 4655790).

O COG 002-4 da DGT que o STAC anuncia responde 403 (bucket `orto` privado),
por isso usa-se o WMS publico OrtoSat2023 da DGT
  https://ortos.dgterritorio.gov.pt/wms/ortosat2023
camada `ortoSat2023-CorVerdadeira`, em EPSG:3763.

Primeiro faz-se um teste de registo: pede-se a mesma janela do pomar do caso
e compara-se com a ortofoto local de 2025. So depois se usa o resto.

So R,G,B. Nenhum indice de vegetacao.
"""
import io
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


def wms(jan32629, res=0.6):
    """Devolve RGB da janela (E,N em 32629) via WMS, em grelha 32629."""
    xs, ys = [], []
    for e in (jan32629[0], jan32629[2]):
        for n in (jan32629[1], jan32629[3]):
            x, y = T.transform(e, n)
            xs.append(x)
            ys.append(y)
    bb = (min(xs), min(ys), max(xs), max(ys))
    w = int(round((bb[2] - bb[0]) / res))
    h = int(round((bb[3] - bb[1]) / res))
    assert w <= 4096 and h <= 4096, "janela demasiado grande: %dx%d" % (w, h)
    p = dict(service="WMS", version="1.1.1", request="GetMap",
             layers="ortoSat2023-CorVerdadeira", styles="",
             srs="EPSG:3763", bbox="%f,%f,%f,%f" % bb,
             width=w, height=h, format="image/png")
    r = requests.get(WMS, params=p, timeout=180, verify=False)
    r.raise_for_status()
    assert r.headers.get("content-type", "").startswith("image"), r.text[:300]
    a = np.asarray(Image.open(io.BytesIO(r.content)).convert("RGB"))
    return a, bb


def local(jan, res=0.6):
    p = os.path.join(BASE, "orto", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif")
    with rasterio.open(p) as ds:
        jb = transform_bounds("EPSG:32629", ds.crs, *jan, densify_pts=21)
        win = from_bounds(*jb, transform=ds.transform)
        w = int(round((jan[2] - jan[0]) / res))
        h = int(round((jan[3] - jan[1]) / res))
        a = ds.read([1, 2, 3], window=win, out_shape=(3, h, w),
                    boundless=True, fill_value=0)
    return np.moveaxis(a, 0, -1)


def norm(a):
    a = a.astype("float32")
    return np.clip(a / max(np.percentile(a, 99.3), 1.0), 0, 1)


# ------------------------------------------------- 1. teste de registo
TESTE = (530600.0, 4655000.0, 531100.0, 4655350.0)
aw, bb = wms(TESTE, 0.5)
al = local(TESTE, 0.5)
print("teste de registo: WMS %s  local %s  bbox3763 %s"
      % (aw.shape, al.shape, tuple(round(x) for x in bb)))
fig, axs = plt.subplots(1, 2, figsize=(18, 7), dpi=150)
axs[0].imshow(norm(al), extent=[TESTE[0], TESTE[2], TESTE[1], TESTE[3]])
axs[0].set_title("local: ortofoto DGT 2025, 25 cm (reamostrada a 0,5 m)", fontsize=9)
axs[1].imshow(norm(aw), extent=[TESTE[0], TESTE[2], TESTE[1], TESTE[3]])
axs[1].set_title("WMS: OrtoSat2023 CorVerdadeira", fontsize=9)
for ax in axs:
    ax.tick_params(labelsize=6)
fig.suptitle("CTRL-06 teste de registo — mesma janela E %.0f..%.0f N %.0f..%.0f"
             % TESTE, fontsize=10)
fig.savefig(os.path.join(OUT, "ctrl_06_registo.png"), bbox_inches="tight")
plt.close(fig)
print("-> ctrl_06_registo.png")

# ------------------------------------------------- 2. sector leste
for nome, jan, res in (("leste", (531500.0, 4653900.0, 533900.0, 4655900.0), 0.6),
                       ("nordeste", (530000.0, 4655600.0, 532400.0, 4657000.0), 0.6)):
    a, bb = wms(jan, res)
    np.save(os.path.join(OUT, "ctrl_06_%s.npy" % nome), a)
    fig, ax = plt.subplots(figsize=(17, 17 * (jan[3] - jan[1]) / (jan[2] - jan[0])),
                           dpi=180)
    ax.imshow(norm(a), extent=[jan[0], jan[2], jan[1], jan[3]])
    ax.add_patch(Rectangle((CASO[0], CASO[1]), CASO[2] - CASO[0],
                           CASO[3] - CASO[1], fill=False, edgecolor="red", lw=2))
    for e in range(int(jan[0]) // 250 * 250, int(jan[2]) + 250, 250):
        if jan[0] <= e <= jan[2]:
            ax.axvline(e, color="w", lw=0.3, alpha=0.5)
    for n in range(int(jan[1]) // 250 * 250, int(jan[3]) + 250, 250):
        if jan[1] <= n <= jan[3]:
            ax.axhline(n, color="w", lw=0.3, alpha=0.5)
    ax.set_title("OrtoSat2023 (DGT WMS) — sector %s, grelha 250 m, EPSG:32629"
                 % nome, fontsize=9)
    ax.tick_params(labelsize=6)
    fig.savefig(os.path.join(OUT, "ctrl_06_%s.png" % nome), bbox_inches="tight")
    plt.close(fig)
    print("-> ctrl_06_%s.png  %s" % (nome, a.shape))
