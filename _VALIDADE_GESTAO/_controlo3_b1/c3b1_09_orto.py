# -*- coding: utf-8 -*-
"""Q3 (fecho) e condicao 2 · a ortofoto sobre as SEIS parcelas do B1.

O B1 foi medido so com optico de satelite: Landsat e Sentinel-2. Sao dois
sensores, mas e o mesmo instrumento no sentido que interessa — **um NDVI nao se
confirma com outro NDVI**. A leitura de «estabelecimento» e uma inferencia sobre
a forma da serie, feita com o instrumento que produziu a serie: e literalmente
o modo de falha que retirou o A3.

A ortofoto da DGT e o instrumento independente, e ja esta em disco: o mosaico
IRG/FalsaCor de TODO o ENT 472062 foi descarregado a 03-09 pelo `c3_08_orto_tres`
para `_controlo3\\_orto472062\\`, e as seis parcelas do B1 sao todas do ENT
472062 — cabem na mesma janela. **Nao se descarrega nada.**

METODO — o mesmo de `orto_297313_fraccao.py` e `c3_08_orto_tres.py`:
    limiar  = percentil 10 do indice IR-R nos blocos de CONTROLO do mesmo dono
              que NAO sao do B1, medido DENTRO de cada imagem;
    fraccao = % de pixeis de cada parcela abaixo desse limiar.

CRITERIO, escrito antes de correr
---------------------------------
    O1 · se 6476425 (nivel 0,890 em 2017, 0,457 em 2018) mostrar coberto em
         2012 e chao em 2018, entao NAO esta «em estabelecimento»: e um pomar
         MADURO ARRANCADO, e a subida de 2019-2026 e recuperacao de plantacao
         nova sobre um pomar destruido — outra coisa, e mais grave.
    O2 · se 6476415 (queda em 2019) mostrar coberto em 2018 e chao em 2021, a
         sua «linha de base continua» nao existe.
    O3 · se 6476420 mostrar coberto em todas as epocas, e a UNICA parcela do
         B1 com linha de base verificada por instrumento independente.
    O4 · se a ortofoto nao discriminar (controlo com fraccao alta), escreve-se
         NAO TESTAVEL.
"""
import json
import os

import numpy as np
from PIL import Image
from matplotlib.path import Path as MP
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

import c3b1_00_comum as C

Image.MAX_IMAGE_PIXELS = None
CACHE = os.path.join(C.VG, "_controlo3", "_orto472062")
PX = 1.0
DONO = 472062
EPOCAS = [("2007", "Ortos2007-FalsaCor"), ("2010", "Ortos2010-FalsaCor"),
          ("2012", "Ortos2012-FalsaCor"), ("2018", "Ortos2018-IRG"),
          ("2021", "Ortos2021-IRG"), ("2025", "Ortos2025-IRG")]
VALIDOS = [6476415, 6476420, 8845740, 6476425]

tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)

BL = []
for ft in C.KF:
    c = ft["properties"].get("CUL_ID")
    if c is None or int(c) not in C.ENT or C.ENT[int(c)] != DONO:
        continue
    g = para(shape(ft["geometry"])).buffer(0)
    BL.append(dict(cul=int(c), geom=g, ha=g.area / 1e4, alvo=int(c) in C.CUL_B1))
print("blocos do ENT %d: %d   (do B1 %d · controlo %d)"
      % (DONO, len(BL), sum(b["alvo"] for b in BL), sum(not b["alvo"] for b in BL)))

xs = [v for b in BL for v in (b["geom"].bounds[0], b["geom"].bounds[2])]
ys = [v for b in BL for v in (b["geom"].bounds[1], b["geom"].bounds[3])]
BB = (min(xs) - 30, min(ys) - 30, max(xs) + 30, max(ys) + 30)
NCx, NLy = int((BB[2] - BB[0]) / PX), int((BB[3] - BB[1]) / PX)
print("janela: %.0f x %.0f m -> %d x %d px" % (BB[2] - BB[0], BB[3] - BB[1],
                                               NCx, NLy))
EE, NN = np.meshgrid(BB[0] + (np.arange(NCx) + .5) * PX,
                     BB[3] - (np.arange(NLy) + .5) * PX)
pts = np.column_stack([EE.ravel(), NN.ravel()])
for b in BL:
    b["m"] = MP(np.array(list(b["geom"].exterior.coords))
                ).contains_points(pts).reshape(NLy, NCx)
    b["n"] = int(b["m"].sum())
CTRL = np.any([b["m"] for b in BL if not b["alvo"]], axis=0)
print("pixeis: B1 %d · controlo %d"
      % (sum(b["n"] for b in BL if b["alvo"]), int(CTRL.sum())))

FR = {}
for ano, cam in EPOCAS:
    f = os.path.join(CACHE, "%s_%s_%dm.png" % (ano, cam, int(PX)))
    if not os.path.exists(f):
        print("  %s — sem cache, nao se descarrega. NAO TESTAVEL nesta epoca" % ano)
        continue
    a = np.array(Image.open(f).convert("RGB")).astype("float32")
    if a.shape[:2] != (NLy, NCx):
        print("  %s — a cache tem %s e a janela %s. Nao se pode usar."
              % (ano, a.shape[:2], (NLy, NCx)))
        continue
    ir, rd = a[..., 0], a[..., 1]
    v = np.where(ir + rd > 8, (ir - rd) / np.maximum(ir + rd, 1e-6), np.nan)
    cob = float(np.isfinite(v[CTRL]).mean())
    lim = float(np.nanpercentile(v[CTRL], 10))
    FR[ano] = dict(lim=lim, cob=cob, blocos={})
    for b in BL:
        w = v[b["m"]]
        w = w[np.isfinite(w)]
        FR[ano]["blocos"][b["cul"]] = float(100 * np.mean(w < lim)) if w.size else np.nan

print()
print("=" * 104)
print("FRACCAO SEM COBERTO (%), ortofoto DGT — limiar = p10 do controlo do mesmo dono")
print("=" * 104)
print()
anos = [a for a, _ in EPOCAS if a in FR]
print("%-10s %6s %s   %s" % ("CUL_ID", "ha", " ".join("%7s" % a for a in anos),
                             "triagem do B1"))
for b in sorted(BL, key=lambda z: -z["alvo"]):
    if not b["alvo"]:
        continue
    c = b["cul"]
    print("%-10d %6.2f %s   %s"
          % (c, b["ha"], " ".join("%6.1f%%" % FR[a]["blocos"][c] for a in anos),
             "VALIDA" if c in VALIDOS else "FORA (plantacao nova)"))
med = {a: float(np.median([FR[a]["blocos"][b["cul"]] for b in BL if not b["alvo"]]))
       for a in anos}
print("%-10s %6s %s   %s" % ("mediana", "", " ".join("%6.1f%%" % med[a] for a in anos),
                             "dos %d blocos de controlo do mesmo dono"
                             % sum(not b["alvo"] for b in BL)))
print()
print("cobertura da imagem no controlo: %s"
      % "  ".join("%s %.0f%%" % (a, 100 * FR[a]["cob"]) for a in anos))

print()
print("=" * 104)
print("O QUE OS CRITERIOS DIZEM")
print("=" * 104)
print()
for c, crit in ((6476425, "O1"), (6476415, "O2"), (6476420, "O3")):
    s = [FR[a]["blocos"][c] for a in anos]
    print("%s · %-9d %s" % (crit, c,
                            "  ".join("%s %.1f%%" % (a, x) for a, x in zip(anos, s))))
print()
print("recortes por parcela e por epoca em _controlo3_b1\\crop_*.png")

# ------- recortes para OLHAR, que e o que a fraccao nao decide
for b in BL:
    if not b["alvo"]:
        continue
    x0, y0, x1, y1 = b["geom"].bounds
    j0, j1 = int((x0 - 20 - BB[0]) / PX), int((x1 + 20 - BB[0]) / PX)
    i0, i1 = int((BB[3] - y1 - 20) / PX), int((BB[3] - y0 + 20) / PX)
    tiras = []
    for ano, cam in EPOCAS:
        f = os.path.join(CACHE, "%s_%s_%dm.png" % (ano, cam, int(PX)))
        if not os.path.exists(f):
            continue
        a = np.array(Image.open(f).convert("RGB"))[max(i0, 0):i1, max(j0, 0):j1]
        tiras.append(a)
    if not tiras:
        continue
    h = max(t.shape[0] for t in tiras)
    w = max(t.shape[1] for t in tiras)
    lin = np.zeros((h, w * len(tiras) + 6 * (len(tiras) - 1), 3), np.uint8)
    for k, t in enumerate(tiras):
        o = k * (w + 6)
        lin[:t.shape[0], o:o + t.shape[1]] = t
    Image.fromarray(lin).save(os.path.join(C.OUT, "crop_%d.png" % b["cul"]))

json.dump(dict(anos=anos, fraccao={str(b["cul"]): {a: FR[a]["blocos"][b["cul"]]
                                                   for a in anos} for b in BL},
               mediana_controlo=med,
               cobertura={a: FR[a]["cob"] for a in anos}),
          open(os.path.join(C.OUT, "c3b1_09_orto.json"), "w"), indent=1)
print("escrito c3b1_09_orto.json")
