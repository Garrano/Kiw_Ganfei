# -*- coding: utf-8 -*-
"""Q4 · as duas geometrias do B1, sobrepostas.

Pergunta 1: quais parcelas do IFAP caem dentro da caixa declarada do sector B1
            (E 529 495-530 063 · N 4 653 832-4 654 477)? Sao mesmo seis?
Pergunta 2: os poligonos C1a + C1b (11,56 ha, ortofoto, sessao do controlo
            externo) e as seis parcelas do IFAP (12,63 ha) medem o mesmo chao?
            Interseccao, uniao, Jaccard, e o que cada um tem que o outro nao tem.
Pergunta 3: alguma parcela do B1 esta entre os 37 blocos da REG-01? entre os 29?
"""
import json
import os

import numpy as np
from shapely.geometry import box, shape
from shapely.ops import unary_union

import c3b1_00_comum as C

CAIXA = box(529495, 4653832, 530063, 4654477)

print("=" * 100)
print("A · QUE PARCELAS DO IFAP CAEM NA CAIXA DECLARADA DO SECTOR B1")
print("=" * 100)
print()
dentro = []
for c, g in sorted(C.GEO.items()):
    inter = g.intersection(CAIXA).area
    if inter > 0:
        dentro.append((c, g.area / 1e4, 100 * inter / g.area))
print("%-10s %7s %8s %7s %10s %8s"
      % ("CUL_ID", "ENT", "ha", "% na", "na CUL_B1", "REG-01"))
for c, ha, pc in sorted(dentro, key=lambda z: -z[1]):
    print("%-10d %7s %8.2f %6.1f%% %10s %8s"
          % (c, C.ENT.get(c, "?"), ha, pc,
             "SIM" if c in C.CUL_B1 else "-- NAO --",
             "mantido" if c in C.MANTIDOS else
             ("EXCLUIDO" if c in C.EXCLUIDOS else "fora")))
print()
print("total na caixa: %d parcelas, %.2f ha" % (len(dentro), sum(x[1] for x in dentro)))
print("a lista CUL_B1 do script: %d parcelas, %.2f ha"
      % (len(C.CUL_B1), sum(C.GEO[c].area for c in C.CUL_B1) / 1e4))

print()
print("=" * 100)
print("B · OS SEIS DO IFAP CONTRA C1a + C1b (ortofoto, sem NDVI)")
print("=" * 100)
print()
ctrl = json.load(open(r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
                      r"\SAIDA_C0\controlos.geojson", encoding="utf-8"))
gs = {}
for f in ctrl["features"]:
    i = f["properties"].get("id")
    if i in ("C1a", "C1b"):
        gs[i] = shape(f["geometry"])
print("C1a/C1b encontrados: %s" % sorted(gs))
crs_ctrl = ctrl.get("crs")
print("crs declarado no geojson: %s" % crs_ctrl)
xs = [p[0] for g in gs.values() for p in np.array(g.exterior.coords)]
print("gama de X dos poligonos C1: %.1f a %.1f  ->  %s"
      % (min(xs), max(xs), "UTM (ja projectado)" if abs(min(xs)) > 1000
         else "graus (lat/lon)"))
C1 = unary_union(list(gs.values()))
print("area C1a+C1b: %.2f ha" % (C1.area / 1e4))

IF6 = unary_union([C.GEO[c] for c in C.CUL_B1])
inter = C1.intersection(IF6).area / 1e4
uni = C1.union(IF6).area / 1e4
print()
print("IFAP 6 parcelas : %.2f ha" % (IF6.area / 1e4))
print("C1a + C1b       : %.2f ha" % (C1.area / 1e4))
print("interseccao     : %.2f ha" % inter)
print("uniao           : %.2f ha" % uni)
print("Jaccard         : %.3f" % (inter / uni))
print("do IFAP, fora do C1 : %.2f ha (%.0f %%)"
      % (IF6.area / 1e4 - inter, 100 * (1 - inter / (IF6.area / 1e4))))
print("do C1, fora do IFAP : %.2f ha (%.0f %%)"
      % (C1.area / 1e4 - inter, 100 * (1 - inter / (C1.area / 1e4))))
print()
print("quanto de cada parcela do IFAP esta dentro do C1a+C1b:")
for c in C.CUL_B1:
    g = C.GEO[c]
    print("  %-9d %5.2f ha  ->  %5.1f %% dentro de C1a+C1b"
          % (c, g.area / 1e4, 100 * g.intersection(C1).area / g.area))

json.dump(dict(na_caixa=[[c, ha, pc] for c, ha, pc in dentro],
               ha_ifap6=IF6.area / 1e4, ha_c1=C1.area / 1e4,
               ha_inter=inter, jaccard=inter / uni,
               b1_em_reg01=[c for c in C.CUL_B1 if c in C.DEG_L],
               b1_mantidos=[c for c in C.CUL_B1 if c in C.MANTIDOS],
               b1_excluidos=[c for c in C.CUL_B1 if c in C.EXCLUIDOS]),
          open(os.path.join(C.OUT, "c3b1_01_geometria.json"), "w"), indent=1)
print()
print("escrito c3b1_01_geometria.json")
