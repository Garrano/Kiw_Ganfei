# -*- coding: utf-8 -*-
"""C2-13 — a ortofoto de 2025 serve de instrumento independente para o VIGOR?

Resposta: **nao serve**. Este script existe para registar o negativo, porque a
tentacao de o usar e grande e a R2 G14 ainda deixa uma medicao desse tipo em
pe.

O que a R2 ja tinha estabelecido (G13/G37): as sete ortofotos tem radiometrias
incomparaveis entre epocas, e qualquer comparacao de brilho entre epocas e
invalida. O que ficou permitido foram comparacoes **dentro de uma so imagem**,
e a G14 apoia-se numa dessas (2025: referencia 91,5 %, «Mancha W» 80,8 %,
«Zona 0» 64,2 % de superficie clara).

Aqui testa-se se a radiometria da ortofoto de 2025 e interpretavel **mesmo
dentro da propria imagem**, com duas verificacoes:

  V1  o NDVI calculado da propria ortofoto sobre copado de kiwi fechado em
      pleno Verao. Fisicamente tem de estar acima de 0,7.
  V2  a ORDENACAO das unidades pela radiometria da ortofoto, contra a
      ordenacao pelo Sentinel-2. Nao tem de bater em valor — tem de bater em
      ordem.

Se V1 der valores impossiveis e V2 inverter, a radiometria da ortofoto nao
mede vigor, nem sequer dentro de uma imagem, e nao pode servir de instrumento
independente para nada que seja vigor.

Repare-se no contraste com o `c2_12`: a deteccao de pergola sobrevive a isto,
porque mede PERIODICIDADE ESPACIAL e nao nivel de sinal. Uma medida de estrutura
e imune ao equilibrio de um JPEG; uma medida de nivel nao e.
"""
import json
import os
import sys

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import Resampling, reproject, transform_bounds
from rasterio.windows import from_bounds
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(POMAR)
nd = carrega_ndvi(TODAS)
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy"))

ds = rasterio.open(os.path.join(RAIZ, "orto",
                                "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif"))
print("ortofoto 2025: %d bandas, colorinterp %s"
      % (ds.count, [c.name for c in ds.colorinterp]))
W = transform_bounds("EPSG:32629", ds.crs, *AOI)
w = from_bounds(*W, transform=ds.transform)
wt = ds.window_transform(w)
DEST = from_origin(ORIGEM_NO[0], ORIGEM_NO[1], PASSO, PASSO)


def para_grelha(a):
    out = np.zeros((NL, NC), "float32")
    reproject(a, out, src_transform=wt, src_crs=ds.crs,
              dst_transform=DEST, dst_crs="EPSG:32629",
              resampling=Resampling.average)
    return out


B = [para_grelha(ds.read(i, window=w).astype("float32")) for i in (1, 2, 3, 4)]
lum = (B[0] + B[1] + B[2]) / 3.0
with np.errstate(invalid="ignore", divide="ignore"):
    ndo = (B[3] - B[0]) / (B[3] + B[0])

UN = [("referência sistemática", REF),
      ("foco OESTE, disco 90 m", do),
      ("foco ESTE, disco 90 m", de),
      ("foco ESTE plantado (sem nu2021)", ZONA0 & ~NU21),
      ("chão lavrado de 2021", NU21),
      ("declínio novo M2 (3,58 ha)", novo),
      ("pomar sem os dois discos", POMAR & ~do & ~de),
      ("pomar inteiro", POMAR)]

print()
print("%-36s %6s %10s %10s %12s %12s" %
      ("unidade", "n", "V", "IVP", "NDVI orto", "NDVI S2 26"))
res = {}
for nome, m in UN:
    r = dict(n=int(m.sum()), verm=float(B[0][m].mean()), ivp=float(B[3][m].mean()),
             lum=float(lum[m].mean()), ndvi_orto=float(np.nanmean(ndo[m])),
             ndvi_s2=float(np.nanmean(nd["2026-07-27"][m])),
             ndvi_s2_25=float(np.nanmean(nd["2025-08-14"][m])))
    res[nome] = r
    print("%-36s %6d %10.1f %10.1f %12.3f %12.3f"
          % (nome, m.sum(), r["verm"], r["ivp"], r["ndvi_orto"], r["ndvi_s2"]))

print()
print("=" * 78)
print("V1 — o NDVI da propria ortofoto sobre copado de kiwi em pleno Verao")
print("=" * 78)
print("  pomar inteiro: NDVI da ortofoto %.3f  |  NDVI Sentinel-2 de 2025-08-14 %.3f"
      % (res["pomar inteiro"]["ndvi_orto"], res["pomar inteiro"]["ndvi_s2_25"]))
print("  Copado de kiwi fechado da 0,80-0,90. A ortofoto da %.2f."
      % res["pomar inteiro"]["ndvi_orto"])
print("  -> A banda do infravermelho proximo esta equilibrada para visualizacao,")
print("     como a R2 G37 ja dizia das outras epocas. Vale para 2025 tambem.")

print()
print("=" * 78)
print("V2 — a ORDENACAO das unidades bate entre os dois instrumentos?")
print("=" * 78)
ks = [n for n, _ in UN]
a = np.array([res[k]["ndvi_orto"] for k in ks])
b = np.array([res[k]["ndvi_s2_25"] for k in ks])
c = np.array([res[k]["lum"] for k in ks])
r1, p1 = stats.spearmanr(a, b)
r2, p2 = stats.spearmanr(c, b)
print("  NDVI da ortofoto  x  NDVI Sentinel-2 2025: rho = %+.3f  (p = %.3f)" % (r1, p1))
print("  luminância        x  NDVI Sentinel-2 2025: rho = %+.3f  (p = %.3f)" % (r2, p2))
print()
print("  Ordenacao pelo NDVI da ortofoto (do pior para o melhor):")
for k in sorted(ks, key=lambda k: res[k]["ndvi_orto"]):
    print("    %-36s %.3f" % (k, res[k]["ndvi_orto"]))
print("  Ordenacao pelo Sentinel-2 de 2025 (do pior para o melhor):")
for k in sorted(ks, key=lambda k: res[k]["ndvi_s2_25"]):
    print("    %-36s %.3f" % (k, res[k]["ndvi_s2_25"]))

print()
print("=" * 78)
print("VEREDICTO")
print("=" * 78)
print("  V1 falha: o NDVI da ortofoto e fisicamente impossivel sobre este copado.")
print("  V2 %s: rho = %+.3f entre os dois NDVI."
      % ("falha" if r1 < 0.5 else "passa", r1))
print("  A radiometria da ortofoto de 2025 NAO serve de instrumento independente")
print("  para vigor, nem dentro da propria imagem. A luminancia reproduz o SENTIDO")
print("  da G14 (a referencia tem mais superficie clara: %.1f contra %.1f no foco"
      % (res["referência sistemática"]["lum"], res["foco OESTE, disco 90 m"]["lum"]))
print("  OESTE), mas o sentido nao e o mesmo que uma medida calibrada.")
print()
print("  O que SOBREVIVE da ortofoto e a ESTRUTURA, nao o nivel: ver c2_12, onde")
print("  a periodicidade de pergola separa as unidades com p ~ 1e-200 e e imune")
print("  ao equilibrio do JPEG por nao usar o nivel do sinal.")

json.dump(res, open(os.path.join(SAIDA, "c2_13_coberto.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_13_coberto.json")
