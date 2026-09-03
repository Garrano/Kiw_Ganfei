# -*- coding: utf-8 -*-
"""C1-01 — inventario dos 21 mosaicos MDT 50 cm: campanhas, cobertura, costuras.

Pergunta: os 21 mosaicos vem todos da mesma campanha? Se nao, onde caem as
costuras em relacao ao pomar e aos dois focos? Uma diferenca de cota entre
focos que coincida com uma costura de campanha e artefacto, nao terreno.
"""
import glob, os, sys, json
import numpy as np
import rasterio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

fs = sorted(glob.glob(os.path.join(RAIZ, "lidar", "MDT-50cm-*.tif")))
print("mosaicos:", len(fs))

linhas = []
for f in fs:
    with rasterio.open(f) as s:
        tags = s.tags()
        b = s.bounds
        linhas.append(dict(nome=os.path.basename(f), crs=str(s.crs), res=s.res[0],
                           shape=s.shape, left=b.left, bottom=b.bottom,
                           right=b.right, top=b.top, nodata=s.nodata,
                           tags=tags))

crss = set(l["crs"] for l in linhas)
ress = set(l["res"] for l in linhas)
print("CRS distintos:", crss, "| resolucoes:", ress)

# tags que possam identificar campanha
chaves = set()
for l in linhas:
    chaves |= set(l["tags"].keys())
print("tags disponiveis:", sorted(chaves))
for l in linhas[:3]:
    print(" ", l["nome"], l["tags"])

# --- cobertura da uniao dos mosaicos ---
L = min(l["left"] for l in linhas); R = max(l["right"] for l in linhas)
B = min(l["bottom"] for l in linhas); T = max(l["top"] for l in linhas)
print("uniao 3763: E %.1f..%.1f  N %.1f..%.1f  (%.0f x %.0f m)" % (L, R, B, T, R - L, T - B))

# --- a AOI (32629) transformada para 3763 ---
cantos = [(AOI[0], AOI[1]), (AOI[2], AOI[1]), (AOI[2], AOI[3]), (AOI[0], AOI[3])]
c3763 = [T_29_TO_3763.transform(*c) for c in cantos]
xs = [c[0] for c in c3763]; ys = [c[1] for c in c3763]
print("AOI em 3763: E %.1f..%.1f  N %.1f..%.1f" % (min(xs), max(xs), min(ys), max(ys)))

# --- cobertura celula a celula da grelha de 10 m: quais celulas tem MDT? ---
E29, N29 = centros_celulas()
X, Y = T_29_TO_3763.transform(E29.ravel(), N29.ravel())
X = X.reshape(E29.shape); Y = Y.reshape(E29.shape)

cobertura = np.zeros(E29.shape, dtype=np.int16) - 1   # indice do mosaico, -1 = nenhum
for i, l in enumerate(linhas):
    dentro = (X >= l["left"]) & (X < l["right"]) & (Y >= l["bottom"]) & (Y < l["top"])
    cobertura[dentro & (cobertura < 0)] = i

masc, meta = carrega_mascaras()
pomar = masc["pomar"]
print("celulas da AOI sem mosaico MDT: %d de %d (%.1f%%)" %
      ((cobertura < 0).sum(), cobertura.size, 100 * (cobertura < 0).mean()))
print("celulas do POMAR sem mosaico MDT: %d de %d" %
      ((pomar & (cobertura < 0)).sum(), pomar.sum()))

# limite leste da cobertura, em E de 32629
col_sem = np.where((cobertura < 0).any(axis=0))[0]
if len(col_sem):
    print("colunas sem cobertura: %d..%d  ->  E >= %.0f  (%.0f m mais a leste da AOI)"
          % (col_sem.min(), col_sem.max(),
             ORIGEM_NO[0] + col_sem.min() * PASSO,
             AOI[2] - (ORIGEM_NO[0] + col_sem.min() * PASSO)))

# --- que mosaicos tocam o pomar, e quais tocam cada foco ---
do, de = discos_dos_focos(pomar)
print("\ndisco OESTE: %d celulas (%.2f ha) | disco ESTE: %d celulas (%.2f ha)"
      % (do.sum(), do.sum() / 100.0, de.sum(), de.sum() / 100.0))
for nome, m in (("pomar", pomar), ("foco OESTE", do), ("foco ESTE", de),
                ("zona0(=foco ESTE, poligono antigo)", masc["zona0"]),
                ("saudavel(110)", masc["saudavel"])):
    idx = sorted(set(cobertura[m].tolist()))
    print("%-38s mosaicos: %s" % (nome, [linhas[i]["nome"][9:15] if i >= 0 else "SEM" for i in idx]))

with open(os.path.join(SAIDA, "c1_01_mosaicos.json"), "w", encoding="utf-8") as f:
    json.dump(linhas, f, ensure_ascii=False, indent=1, default=str)
np.save(os.path.join(SAIDA, "c1_01_cobertura_mosaico.npy"), cobertura)
print("\nescrito c1_01_mosaicos.json e c1_01_cobertura_mosaico.npy")
