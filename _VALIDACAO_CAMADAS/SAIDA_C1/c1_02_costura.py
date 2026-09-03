# -*- coding: utf-8 -*-
"""C1-02 — campanhas de voo e ensaio de costura.

O foco OESTE cai inteiro no mosaico 158565 e o foco ESTE inteiro no 159565
(c1_01). Antes de comparar cotas entre focos e obrigatorio saber se os dois
mosaicos sao do mesmo voo e se ha degrau na fronteira que os separa.

Duas provas independentes uma da outra:
  (a) metadados do fornecedor  — datetime de cada item no catalogo DGT
  (b) medicao empirica na costura — perfil de cota nas faixas de 10 m de cada
      lado da fronteira comum, comparado com o gradiente local do terreno.
"""
import glob, os, sys, json, ssl, urllib.request
import numpy as np
import rasterio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

LID = os.path.join(RAIZ, "lidar")
paths = sorted(glob.glob(os.path.join(LID, "MDT-50cm-*.tif")))

# ---------- (a) catalogo do fornecedor ----------
voo = {}
try:
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    u = ("https://dgt-be.a.incd.pt:8081/collections/MDT-50cm/items?f=json&limit=400"
         "&bbox=-8.660,42.035,-8.600,42.058")
    with urllib.request.urlopen(u, timeout=180, context=ctx) as r:
        meta = json.load(r)
    feats = meta.get("features") or meta["data"]["features"]
    voo = {f["id"]: f["properties"]["datetime"][:10] for f in feats}
    print("catalogo DGT: %d itens" % len(voo))
except Exception as e:
    print("catalogo DGT indisponivel:", type(e).__name__, e)

camp = {}
for p in paths:
    tid = os.path.basename(p).replace("_v02.tif", "")
    camp.setdefault(voo.get(tid, "?"), []).append(tid[10:16])
for d in sorted(camp):
    print("  %s : %2d mosaicos  %s" % (d, len(camp[d]), sorted(camp[d])))

TILE_OESTE, TILE_ESTE = "158565", "159565"
d_o = voo.get("MDT-50cm-%s-07-2025" % TILE_OESTE, "?")
d_e = voo.get("MDT-50cm-%s-07-2025" % TILE_ESTE, "?")
print("\nfoco OESTE -> mosaico %s, voo %s" % (TILE_OESTE, d_o))
print("foco ESTE  -> mosaico %s, voo %s" % (TILE_ESTE, d_e))
print("MESMA CAMPANHA?" , d_o == d_e and d_o != "?")

# ---------- (b) ensaio empirico na costura 158565 | 159565 ----------
po = [p for p in paths if TILE_OESTE in p][0]
pe = [p for p in paths if TILE_ESTE in p][0]
with rasterio.open(po) as s1, rasterio.open(pe) as s2:
    b1, b2 = s1.bounds, s2.bounds
    print("\n%s bounds %s\n%s bounds %s" % (TILE_OESTE, tuple(b1), TILE_ESTE, tuple(b2)))
    assert abs(b1.right - b2.left) < 1, "nao sao adjacentes"
    # 20 px = 10 m de cada lado
    a = s1.read(1, window=((0, s1.height), (s1.width - 20, s1.width))).astype("float64")
    b = s2.read(1, window=((0, s2.height), (0, 20))).astype("float64")
    # faixa de controlo: 10 m mais para dentro de cada mosaico (sem costura)
    ac = s1.read(1, window=((0, s1.height), (s1.width - 40, s1.width - 20))).astype("float64")
    bc = s2.read(1, window=((0, s2.height), (20, 40))).astype("float64")
    ytop = b1.top

for arr in (a, b, ac, bc):
    arr[arr == -999.0] = np.nan

n = min(a.shape[0], b.shape[0])
a, b, ac, bc = a[:n], b[:n], ac[:n], bc[:n]
ok = ~np.isnan(a).any(1) & ~np.isnan(b).any(1) & ~np.isnan(ac).any(1) & ~np.isnan(bc).any(1)
print("linhas de costura utilizaveis: %d de %d (%.0f m)" % (ok.sum(), n, 0.5 * ok.sum()))

ma, mb = np.nanmean(a[ok], 1), np.nanmean(b[ok], 1)
mac, mbc = np.nanmean(ac[ok], 1), np.nanmean(bc[ok], 1)
salto = mb - ma                    # atravessa a costura, 10 m
ctrl_o = ma - mac                  # dentro do 158565, 10 m, sem costura
ctrl_e = mbc - mb                  # dentro do 159565, 10 m, sem costura
print("\ndegrau atravessando a costura (10 m -> 10 m):")
print("  mediana %+.4f m | media %+.4f | dp %.4f | p5 %+.4f p95 %+.4f"
      % (np.median(salto), salto.mean(), salto.std(), np.percentile(salto, 5), np.percentile(salto, 95)))
print("controlo, mesmo passo de 10 m SEM costura (dois lados):")
print("  158565 interior: mediana %+.4f m dp %.4f" % (np.median(ctrl_o), ctrl_o.std()))
print("  159565 interior: mediana %+.4f m dp %.4f" % (np.median(ctrl_e), ctrl_e.std()))
print("=> o degrau da costura excede o passo natural do terreno? %s"
      % ("SIM" if abs(np.median(salto)) > 3 * max(abs(np.median(ctrl_o)), abs(np.median(ctrl_e)), 1e-9) and abs(np.median(salto)) > 0.05 else "NAO"))

# so a parte da costura que atravessa o pomar interessa
ys = ytop - (np.arange(n)[ok] + 0.5) * 0.5
E29, N29 = T_3763_TO_29.transform(np.full(ys.shape, (b1.right)), ys)
print("\ncostura em 32629: E ~%.0f, N %.0f..%.0f" % (E29.mean(), N29.min(), N29.max()))

json.dump({"campanhas": {k: sorted(v) for k, v in camp.items()},
           "tile_foco_oeste": TILE_OESTE, "voo_oeste": d_o,
           "tile_foco_este": TILE_ESTE, "voo_este": d_e,
           "degrau_costura_mediana_m": float(np.median(salto)),
           "degrau_costura_dp_m": float(salto.std()),
           "controlo_oeste_mediana_m": float(np.median(ctrl_o)),
           "controlo_este_mediana_m": float(np.median(ctrl_e))},
          open(os.path.join(SAIDA, "c1_02_costura.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_02_costura.json")
