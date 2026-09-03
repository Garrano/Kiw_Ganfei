# -*- coding: utf-8 -*-
"""MDS - MDT = altura de copado. O instrumento independente.

Porque isto vale
----------------
Tudo o que este caso usou ate agora mede REFLECTANCIA: NDVI, NDRE, ortofoto,
periodicidade, e ate o radar mede retrodifusao. O LiDAR mede GEOMETRIA. Se a
altura disser que ha 2 m de estrutura vegetal sobre um talhao, ha pergola; se
disser zero, nao ha. Nao ha indice pelo meio.

A regra deste projecto e que nenhum facto passa adiante verificado so pelo
instrumento que o produziu. Esta e a primeira vez neste caso que existe um
instrumento verdadeiramente independente.

O que se mede
-------------
Fraccao de pixeis de 50 cm com altura acima de 1,5 m, dentro de cada celula de
10 m. Uma pergola de kiwi tem 1,8 a 2 m; erva tem zero. O limiar de 1,5 m fica
abaixo da pergola e acima de qualquer coberto herbaceo.

Aviso de datacao
----------------
O Lote I foi voado entre 12-05-2024 e 23-07-2025 — catorze meses. A data desta
folha em concreto sai da nuvem LAZ, nao daqui. Sem ela, a leitura e
condicional.
"""
import glob
import json
import os
import sys

import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import Resampling, reproject, transform_bounds
from rasterio.transform import from_origin
from rasterio.windows import from_bounds

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
LID = os.path.join(RAIZ, "lidar")
RES = 0.5
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
NU21 = masc["nu2021"] & POMAR
d26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool)


def disco(x, y, r=70.0):
    yy, xx = np.mgrid[:NL, :NC]
    return np.hypot(AOI[0] + (xx + .5) * PASSO - x,
                    AOI[3] - (yy + .5) * PASSO - y) <= r


UN = [("N1 foco OESTE", disco(530476, 4655046) & POMAR),
      ("N2 leste (B)", disco(530895, 4655052) & POMAR),
      ("N3 leste (B)", disco(531068, 4655145) & POMAR),
      ("declinio NOVO 2026", novo & POMAR),
      ("referencia", REF),
      ("resto do pomar", POMAR & ~d26 & ~REF),
      ("nu2021 (lavrado 2021)", NU21)]

# grelha de destino: a AOI em 32629, a 50 cm
W = int((AOI[2] - AOI[0]) / RES)
H = int((AOI[3] - AOI[1]) / RES)
DEST = from_origin(AOI[0], AOI[3], RES, RES)
saida = {}
for tag in ("MDS", "MDT"):
    fich = sorted(glob.glob(os.path.join(LID, "%s-50cm-*.tif" % tag)))
    srcs = [rasterio.open(p) for p in fich]
    b3763 = transform_bounds("EPSG:32629", srcs[0].crs, *AOI)
    folga = 60.0
    mos, tr = merge(srcs, bounds=(b3763[0] - folga, b3763[1] - folga,
                                  b3763[2] + folga, b3763[3] + folga),
                    res=(RES, RES), nodata=-999.0)
    out = np.full((H, W), np.nan, "float32")
    reproject(mos[0], out, src_transform=tr, src_crs=srcs[0].crs,
              src_nodata=-999.0, dst_transform=DEST, dst_crs="EPSG:32629",
              dst_nodata=np.nan, resampling=Resampling.bilinear)
    saida[tag] = out
    print("%s: %d x %d, %.1f%% com dados, mediana %.2f m"
          % (tag, W, H, 100 * np.isfinite(out).mean(), np.nanmedian(out)))
    for s in srcs:
        s.close()

CHM = saida["MDS"] - saida["MDT"]
np.save(os.path.join(AQUI, "chm_50cm.npy"), CHM)
print("\nCHM: mediana %.2f m, p95 %.2f m, %.1f%% acima de 1,5 m"
      % (np.nanmedian(CHM), np.nanpercentile(CHM, 95),
         100 * np.nanmean(CHM > 1.5)))

# agregar a 10 m: blocos de 20 x 20 pixeis
B = int(PASSO / RES)
alto = (CHM > 1.5).astype("float32")
alto[~np.isfinite(CHM)] = np.nan
frac = np.nanmean(alto.reshape(NL, B, NC, B), axis=(1, 3))
h50 = np.nanmedian(CHM.reshape(NL, B, NC, B), axis=(1, 3))
np.save(os.path.join(AQUI, "chm_frac_alto.npy"), frac)
np.save(os.path.join(AQUI, "chm_altura.npy"), h50)

print("\nALTURA DE COPADO POR UNIDADE\n")
print("%-24s %6s %14s %16s" % ("", "ha", "altura mediana", "% acima de 1,5 m"))
res = {}
for nome, m in UN:
    k = m & np.isfinite(frac)
    if k.sum() < 5:
        continue
    res[nome] = dict(ha=float(m.sum() / 100.0), n=int(k.sum()),
                     altura=float(np.median(h50[k])),
                     frac_alto=float(np.median(frac[k])) * 100)
    print("%-24s %6.2f %11.2f m %14.1f %%"
          % (nome, m.sum() / 100.0, np.median(h50[k]), 100 * np.median(frac[k])))
json.dump(res, open(os.path.join(AQUI, "altura_copado.json"), "w"), indent=1)
print("""
LEITURA
   ~2 m e fraccao alta   ->  a pergola esta la quando se voou
   ~0 m e fraccao baixa  ->  nao ha pergola. Terreno limpo.""")
