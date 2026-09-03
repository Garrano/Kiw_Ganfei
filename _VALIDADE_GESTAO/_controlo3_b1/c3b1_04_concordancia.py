# -*- coding: utf-8 -*-
"""Q4 · a «concordancia» entre as duas corridas e real?

Uma usa poligonos do IFAP (12,63 ha, 6 parcelas, Landsat 30 m, 100 cenas) e da
um DEGRAU. A outra usa a mascara C1a+C1b (11,60 ha, Sentinel-2 10 m, 9 cenas) e
da NIVEIS e um FOSSO a uma referencia. Sao a mesma coisa?

Torna-se comparavel de tres maneiras:
  A · cruza-se o instrumento com a geometria — as 4 combinacoes;
  B · decompoe-se o «fosso fecha de 0,328 para 0,068»: quanto e o B1 a subir e
      quanto e a REFERENCIA a descer? A referencia e o corpo principal do
      pomar, que e a unidade que teve o acontecimento;
  C · pesa-se quanto da mascara C1a+C1b e a plantacao nova que a triagem
      exclui.
"""
import json
import os

import numpy as np
from matplotlib.path import Path as MP
from shapely.geometry import shape
from shapely.ops import unary_union

import c3b1_00_comum as C

VALIDOS = [6476415, 6476420, 8845740, 6476425]
CS = os.path.join(C.VG, "_reg01_cache")

# ---------------------------------------------------- geometrias, malha 10 e 30
ctrl = json.load(open(r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
                      r"\SAIDA_C0\controlos.geojson", encoding="utf-8"))
C1 = unary_union([shape(f["geometry"]) for f in ctrl["features"]
                  if f["properties"].get("id") in ("C1a", "C1b")])
IF6 = unary_union([C.GEO[c] for c in C.CUL_B1])
IF4 = unary_union([C.GEO[c] for c in VALIDOS])

NC10, NL10 = int((C.BB[2] - C.BB[0]) / 10), int((C.BB[3] - C.BB[1]) / 10)
E10, N10 = np.meshgrid(C.BB[0] + (np.arange(NC10) + .5) * 10.,
                       C.BB[3] - (np.arange(NL10) + .5) * 10.)
P10 = np.column_stack([E10.ravel(), N10.ravel()])


def m10(g):
    if g.geom_type == "Polygon":
        gs = [g]
    else:
        gs = list(g.geoms)
    out = np.zeros(P10.shape[0], bool)
    for h in gs:
        out |= MP(np.array(list(h.exterior.coords))).contains_points(P10)
    return out.reshape(NL10, NC10)


def m30(g):
    if g.geom_type == "Polygon":
        gs = [g]
    else:
        gs = list(g.geoms)
    out = np.zeros(C.PTS.shape[0], bool)
    for h in gs:
        out |= MP(np.array(list(h.exterior.coords))).contains_points(C.PTS)
    return out.reshape(C.NL, C.NC)


G = {"C1a+C1b (ortofoto)": C1, "IFAP 6 parcelas": IF6, "IFAP 4 validas": IF4}
M30 = {k: m30(g) for k, g in G.items()}
M10 = {k: m10(g) for k, g in G.items()}

print("=" * 104)
print("A · O MESMO SECTOR, NAS QUATRO COMBINACOES DE INSTRUMENTO x GEOMETRIA")
print("=" * 104)
print()
for k in G:
    print("%-22s %6.2f ha   %4d celulas de 30 m   %5d de 10 m"
          % (k, G[k].area / 1e4, M30[k].sum(), M10[k].sum()))

# ---- Landsat
datas, V = C.matriz()
med = np.array([np.nanmedian([V[c][i] for c in C.MANTIDOS])
                for i in range(len(datas))])
pos = np.array([d >= "2025" for d in datas])
LS = {}
for k, m in M30.items():
    s = []
    for i, d in enumerate(datas):
        nd = np.load(os.path.join(C.VG, "_reg01_landsat_cache",
                                  C._fich[d]))["ndvi"]
        v = nd[m]
        v = v[np.isfinite(v)]
        s.append(float(np.median(v)) if v.size >= max(3, .5 * m.sum()) else np.nan)
    LS[k] = np.array(s)

print()
print("LANDSAT 30 m, 100 cenas — o sector como UMA unidade")
print("%-22s %9s %9s %9s   %s" % ("", "nivel 17-24", "nivel 25-26",
                                  "degrau*", "* desvio a mediana dos 29"))
for k in G:
    dv = LS[k] - med
    a, b = dv[~pos], dv[pos]
    print("%-22s %9.4f %9.4f %+9.4f"
          % (k, np.nanmean(LS[k][~pos]), np.nanmean(LS[k][pos]),
             np.nanmean(b) - np.nanmean(a)))

# ---- Sentinel-2, 9 cenas da cache regional, mesma malha de 10 m
DS2 = sorted(x[5:15] for x in os.listdir(CS))
print()
print("SENTINEL-2 10 m, %d cenas — as mesmas geometrias" % len(DS2))
S2 = {k: [] for k in G}
for d in DS2:
    nd = np.load(os.path.join(CS, "ndvi_%s.npy" % d))
    for k, m in M10.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        S2[k].append(float(np.median(v)))
print("%-22s %s" % ("", " ".join("%7s" % d[2:7] for d in DS2)))
for k in G:
    print("%-22s %s" % (k, " ".join("%7.3f" % x for x in S2[k])))

print()
print("degrau em S2 (media 2025-26 menos media 2017-24), nivel absoluto:")
ip = [i for i, d in enumerate(DS2) if d >= "2025"]
ia = [i for i, d in enumerate(DS2) if d < "2025"]
for k in G:
    a = np.array(S2[k])
    print("  %-22s %+.4f" % (k, a[ip].mean() - a[ia].mean()))

print()
print("=" * 104)
print("B · DECOMPOSICAO DO «FOSSO FECHA DE 0,328 PARA 0,068»")
print("=" * 104)
print()
B = json.load(open(r"C:\Users\Jackster2\Downloads\ganfei_s2"
                   r"\b1_serie_verdadeira.json", encoding="utf-8"))["serie"]
print("%-12s %9s %9s %9s" % ("data", "B1", "referencia", "fosso"))
for r in B:
    print("%-12s %9.4f %9.4f %9.4f" % (r["data"], r["b1"], r["referencia"],
                                       r["fosso"]))
b0, bN = B[0]["b1"], B[-1]["b1"]
r0, rN = B[0]["referencia"], B[-1]["referencia"]
d = (B[-1]["fosso"] - B[0]["fosso"])
print()
print("2017 -> 2026   fosso %+.4f  =  B1 %+.4f (%.0f %%) + referencia %+.4f (%.0f %%)"
      % (d, -(bN - b0), 100 * abs(bN - b0) / (abs(bN - b0) + abs(rN - r0)),
         (rN - r0), 100 * abs(rN - r0) / (abs(bN - b0) + abs(rN - r0))))
i24 = [i for i, r in enumerate(B) if r["data"][:4] == "2024"][0]
b1_, r1_ = B[i24]["b1"], B[i24]["referencia"]
d2 = B[-1]["fosso"] - B[i24]["fosso"]
print("2024 -> 2026   fosso %+.4f  =  B1 %+.4f (%.0f %%) + referencia %+.4f (%.0f %%)"
      % (d2, -(bN - b1_), 100 * abs(bN - b1_) / (abs(bN - b1_) + abs(rN - r1_)),
         (rN - r1_), 100 * abs(rN - r1_) / (abs(bN - b1_) + abs(rN - r1_))))
print()
print("A REFERENCIA e o corpo principal do pomar — a unidade que TEVE o")
print("acontecimento. Um fosso que fecha porque o denominador desce nao mede")
print("o numerador a subir.")

print()
print("=" * 104)
print("C · QUANTO DA MASCARA C1a+C1b E A PLANTACAO NOVA QUE A TRIAGEM EXCLUI")
print("=" * 104)
print()
tot = C1.area
for c in C.CUL_B1:
    i = C.GEO[c].intersection(C1).area
    print("  %-9d %5.2f ha dentro de C1a+C1b = %5.1f %% da mascara S2   %s"
          % (c, i / 1e4, 100 * i / tot,
             "EXCLUIDA pela triagem (plantacao nova)" if c in C.EXCLUIDOS
             else "mantida"))
exc = sum(C.GEO[c].intersection(C1).area for c in C.CUL_B1 if c in C.EXCLUIDOS)
print()
print("  total EXCLUIDO dentro da mascara S2: %.2f ha = %.0f %%"
      % (exc / 1e4, 100 * exc / tot))
fora = tot - sum(C.GEO[c].intersection(C1).area for c in C.CUL_B1)
print("  area da mascara S2 que nao e kiwi declarado: %.2f ha = %.0f %%"
      % (fora / 1e4, 100 * fora / tot))

json.dump(dict(areas={k: G[k].area / 1e4 for k in G},
               landsat_degrau={k: float(np.nanmean((LS[k] - med)[pos])
                                        - np.nanmean((LS[k] - med)[~pos]))
                               for k in G},
               s2_niveis={k: S2[k] for k in G}, s2_datas=DS2,
               frac_excluida_na_mascara_s2=exc / tot,
               frac_nao_kiwi_na_mascara_s2=fora / tot),
          open(os.path.join(C.OUT, "c3b1_04_concordancia.json"), "w"), indent=1)
print()
print("escrito c3b1_04_concordancia.json")
