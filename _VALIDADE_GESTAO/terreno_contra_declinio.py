# -*- coding: utf-8 -*-
"""O declinio segue o terreno? — o teste que aponta a uma causa.

A pergunta
----------
Depois de separar copado vivo de chao limpo, o caso reduz-se ao foco OESTE:
kiwi vivo sobre pe franco de Erica, no ponto mais baixo da exploracao, a 13,4 m
da drenagem, com carencia de calcio confirmada em duas matrizes, a perder
**agua mais depressa do que folha** (fosso NDMI 0,199 contra NDVI 0,146 em
2026, Landsat) — e no Verao mais humido da decada.

Isso nao e seca. E compativel com raiz que nao consegue absorver havendo agua,
que e o que asfixia radicular e Phytophthora produzem.

**A hipotese fixa, antes de correr:** dentro do copado vivo, as celulas em
maior defice em 2026 estao nas posicoes topograficamente mais humidas.

O desenho, e porque nao e circular
----------------------------------
O terreno vem do **MDT LiDAR a 50 cm**. O defice vem do **NDVI**. Instrumentos
independentes, e o terreno nao muda com o ano.

**O nulo ingenuo nao serve.** A licao dos tres analistas independentes foi
exactamente esta: com autocorrelacao espacial de 0,86 a 0,96, permutar celulas
ao acaso torna tudo significativo. O nulo honesto aqui e **a propria serie**:
o terreno e o mesmo em 2017 e em 2026, portanto se a associacao terreno-defice
existir em todos os anos, nao explica nada de novo; se **emergir** em 2025-26,
e um facto sobre o evento.

Metricas de terreno, todas do MDT
---------------------------------
  cota           altitude absoluta
  desvio local   cota menos a mediana num raio de 40 m — microdepressao
  TWI            indice topografico de humidade, ln(a / tan b), com
                 `resolve_flats` obrigatorio (regra do projecto)
  acumulacao     area drenante a montante
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage, stats

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(AQUI, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
VIVO = POMAR & COM
do, de = discos_dos_focos(POMAR)
print("copado vivo: %.2f ha" % (VIVO.sum() / 100.0))

# ------------------------------------------------------------------ terreno
import glob
import rasterio
from rasterio.merge import merge
from rasterio.transform import from_origin
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject, transform_bounds

srcs = [rasterio.open(p) for p in sorted(glob.glob(
    os.path.join(RAIZ, "lidar", "MDT-50cm-*.tif")))]
b = transform_bounds("EPSG:32629", srcs[0].crs, *AOI)
mos, tr = merge(srcs, bounds=(b[0] - 300, b[1] - 300, b[2] + 300, b[3] + 300),
                res=(2.0, 2.0), nodata=-999.0)
# grelha de trabalho a 2 m, com folga de 300 m para a hidrologia nao ser cortada
FOLGA = 300.0
X0, Y1 = AOI[0] - FOLGA, AOI[3] + FOLGA
W = int((AOI[2] - AOI[0] + 2 * FOLGA) / 2.0)
Hh = int((AOI[3] - AOI[1] + 2 * FOLGA) / 2.0)
dem = np.full((Hh, W), np.nan, "float32")
reproject(mos[0], dem, src_transform=tr, src_crs=srcs[0].crs, src_nodata=-999.0,
          dst_transform=from_origin(X0, Y1, 2.0, 2.0), dst_crs="EPSG:32629",
          dst_nodata=np.nan, resampling=RS.bilinear)
for s in srcs:
    s.close()
print("MDT a 2 m: %d x %d, %.1f%% com dados, cota %.2f a %.2f m"
      % (W, Hh, 100 * np.isfinite(dem).mean(), np.nanmin(dem), np.nanmax(dem)))

from pysheds.grid import Grid
from pysheds.view import Raster, ViewFinder
af = from_origin(X0, Y1, 2.0, 2.0)
vf = ViewFinder(affine=af, shape=dem.shape, crs=srcs[0].crs, nodata=np.float32(np.nan))
r = Raster(np.nan_to_num(dem, nan=float(np.nanmax(dem)) + 5).astype("float32"), viewfinder=vf)
grid = Grid.from_raster(r)
pit = grid.fill_pits(r)
dep = grid.fill_depressions(pit)
inf = grid.resolve_flats(dep)                 # obrigatorio — regra do projecto
fdir = grid.flowdir(inf)
acc = grid.accumulation(fdir)
dx, dy = np.gradient(np.asarray(inf), 2.0)
declive = np.hypot(dx, dy)
tan_b = np.maximum(declive, 0.001)
a_esp = (np.asarray(acc) + 1.0) * 2.0         # area por unidade de contorno
TWI2 = np.log(a_esp / tan_b)
print("TWI: %.2f a %.2f, mediana %.2f"
      % (np.nanmin(TWI2), np.nanmax(TWI2), np.nanmedian(TWI2)))

# desvio local da cota: microdepressao
med40 = ndimage.median_filter(np.asarray(inf), size=41)   # 41 px = 82 m
DESV2 = np.asarray(inf) - med40


def para10(A):
    """recorta a folga e agrega a grelha de 10 m"""
    i0 = int(FOLGA / 2.0)
    S = A[i0:i0 + NL * 5, i0:i0 + NC * 5]
    return np.nanmedian(S.reshape(NL, 5, NC, 5), axis=(1, 3))


COTA = para10(np.asarray(inf))
TWI = para10(TWI2)
DESV = para10(DESV2)
ACC = para10(np.log10(np.asarray(acc) + 1.0))
np.save(os.path.join(AQUI, "terreno_twi.npy"), TWI)
np.save(os.path.join(AQUI, "terreno_desvio.npy"), DESV)

print("\nno copado vivo:  cota %.2f-%.2f m | TWI %.1f-%.1f | desvio %.2f a %+.2f m"
      % (np.nanmin(COTA[VIVO]), np.nanmax(COTA[VIVO]), np.nanmin(TWI[VIVO]),
         np.nanmax(TWI[VIVO]), np.nanmin(DESV[VIVO]), np.nanmax(DESV[VIVO])))

# ------------------------------------------------------------------- teste
nd = carrega_ndvi(TODAS)
SERIE = sorted(nd)
MET = [("cota (negativa: baixo = humido)", -COTA),
       ("desvio local (negativo: cova)", -DESV),
       ("TWI", TWI),
       ("log area drenante", ACC)]

print("\nASSOCIACAO TERRENO x FOSSO, ano a ano, dentro do copado vivo")
print("rho de Spearman. Positivo = mais defice onde e mais humido.\n")
print("%-34s %s" % ("", "  ".join("%6s" % d[2:7] for d in SERIE)))
res = {}
for nome, M in MET:
    L = []
    for d in SERIE:
        a = nd[d]
        r_ = float(np.nanmean(a[REF]))
        f = r_ - a
        k = VIVO & np.isfinite(f) & np.isfinite(M)
        rho, p = stats.spearmanr(M[k], f[k])
        L.append((rho, p))
    res[nome] = [(float(x), float(y)) for x, y in L]
    print("%-34s %s" % (nome, "  ".join("%+6.3f" % x for x, _ in L)))
    print("%-34s %s" % ("   p", "  ".join(
        "%6s" % ("<.001" if y < 0.001 else "%.3f" % y) for _, y in L)))

print("""
LEITURA
  A associacao existe em todos os anos   ->  o terreno explica onde o pomar
                                             sempre foi pior. Nao explica 2026.
  Emerge so em 2025-26                   ->  o evento tem assinatura topografica
                                             e a hipotese hidraulica ganha corpo.
  Nao existe                             ->  a hipotese hidraulica cai.""")

# o mesmo dentro do disco OESTE apenas
print("\nSO DENTRO DO FOCO OESTE (copado vivo)\n")
V = do & VIVO
print("%d celulas, %.2f ha" % (V.sum(), V.sum() / 100.0))
print("%-34s %s" % ("", "  ".join("%6s" % d[2:7] for d in SERIE)))
for nome, M in MET:
    L = []
    for d in SERIE:
        a = nd[d]
        f = float(np.nanmean(a[REF])) - a
        k = V & np.isfinite(f) & np.isfinite(M)
        rho, p = stats.spearmanr(M[k], f[k]) if k.sum() > 20 else (np.nan, np.nan)
        L.append((rho, p))
    res[nome + " | foco OESTE"] = [(float(x), float(y)) for x, y in L]
    print("%-34s %s" % (nome, "  ".join("%+6.3f" % x for x, _ in L)))
    print("%-34s %s" % ("   p", "  ".join(
        "%6s" % ("<.001" if y < 0.001 else "%.3f" % y) for _, y in L)))

json.dump({k: v for k, v in res.items()},
          open(os.path.join(AQUI, "terreno_declinio.json"), "w"), indent=1)
print("\nescrito terreno_declinio.json")
