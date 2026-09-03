# -*- coding: utf-8 -*-
"""C1-05 — G21: `bacia.json` e inutilizavel. Redelinear ou rejeitar.

Primeiro mede-se o que `bacia.json` diz, para o registo. Depois refaz-se o
encaminhamento com pysheds, com `resolve_flats` — a armadilha conhecida e que
a direccao de escoamento sem resolucao de planos converge em poucas iteracoes
e devolve um artefacto (aluviao praticamente plano: 3,4 m de amplitude em
1,4 km).
"""
import os, sys, json, warnings
import numpy as np
import rasterio
from rasterio.transform import Affine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *
warnings.filterwarnings("ignore")

# ---------- (a) o que bacia.json diz ----------
bj = json.load(open(os.path.join(RAIZ, "lidar", "bacia.json"), encoding="utf-8"))
from pyproj import Transformer
Tw = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
lo0, la0, lo1, la1 = bj["bbox_wgs84"]
(x0, y0) = Tw.transform(lo0, la0); (x1, y1) = Tw.transform(lo1, la1)
print("bacia.json declara ha = %s" % bj["ha"])
print("  bbox em 32629: E %.0f..%.0f  N %.0f..%.0f  = %.0f x %.0f m = %.2f ha"
      % (x0, x1, y0, y1, x1 - x0, y1 - y0, (x1 - x0) * (y1 - y0) / 1e4))
masc, _ = carrega_mascaras()
pomar = masc["pomar"]
E29, N29 = centros_celulas()
dentro = (E29 >= x0) & (E29 <= x1) & (N29 >= y0) & (N29 <= y1)
print("  celulas do pomar dentro dessa bbox: %d de %d (%.1f%%)"
      % ((pomar & dentro).sum(), pomar.sum(), 100 * (pomar & dentro).sum() / pomar.sum()))
print("  pomar a oeste da bbox: %.0f m | a leste: %.0f m"
      % (max(0, x0 - E29[pomar].min()), max(0, E29[pomar].max() - x1)))

# ---------- (b) redelinear a partir do MDT ----------
meta = json.load(open(os.path.join(SAIDA, "c1_03_dem50.json")))
dem50 = np.load(os.path.join(SAIDA, "c1_03_dem50.npy"))
Tr = Affine(*meta["transform"])
# 1 m: a 0,5 m o micro-relevo (sulcos, fiadas, valas de 30 cm) domina o
# encaminhamento e produz milhares de bacias de um pixel.
dem = dem50[::2, ::2].astype(np.float64)
Tr1 = Affine(Tr.a * 2, 0, Tr.c, 0, Tr.e * 2, Tr.f)
H, W = dem.shape
print("\nMDT de trabalho: %d x %d @1 m | amplitude %.2f..%.2f m"
      % (H, W, np.nanmin(dem), np.nanmax(dem)))

from pysheds.grid import Grid
from pysheds.view import Raster, ViewFinder
NOD = -32768.0
d = np.where(np.isnan(dem), NOD, dem).astype(np.float64)
import pyproj
vf = ViewFinder(affine=Tr1, shape=d.shape,
                crs=pyproj.Proj("EPSG:3763", preserve_units=True), nodata=NOD)
r = Raster(d, viewfinder=vf)
grid = Grid.from_raster(r)

print("a preencher depressoes ...")
pit = grid.fill_pits(r)
fl = grid.fill_depressions(pit)
n_dep = int(np.sum((fl > pit) & (pit != NOD)))
print("  celulas alteradas por fill_depressions: %d (%.2f%% da area)"
      % (n_dep, 100 * n_dep / fl.size))

print("a resolver planos (resolve_flats) ...")
infl = grid.resolve_flats(fl)
mudou = int(np.sum(np.abs(np.asarray(infl) - np.asarray(fl)) > 0))
print("  celulas alteradas por resolve_flats: %d (%.2f%%)" % (mudou, 100 * mudou / fl.size))

# ---- ARMADILHA: comparar COM e SEM resolve_flats ----
saida = {}
for etiq, base in (("SEM resolve_flats", fl), ("COM resolve_flats", infl)):
    fdir = grid.flowdir(base)
    acc = grid.accumulation(fdir)
    a = np.asarray(acc, dtype=np.float64)
    saida[etiq] = a
    print("  %-18s acumulacao: max %.0f cel (%.2f ha) | p99,9 %.0f | %% celulas com acc>=2000: %.3f"
          % (etiq, a.max(), a.max() / 1e4, np.percentile(a, 99.9), 100 * (a >= 2000).mean()))

acc = saida["COM resolve_flats"]
accs = saida["SEM resolve_flats"]
print("  razao dos maximos COM/SEM: %.2f" % (acc.max() / max(accs.max(), 1)))

# ---------- (c) bacia de contribuicao do pomar ----------
# exutorio: a celula de maior acumulacao na fronteira jusante do pomar.
# Constroi-se a mascara do pomar no referencial do MDT.
def para_mdt(mask10):
    ii, jj = np.nonzero(mask10)
    e = ORIGEM_NO[0] + (jj + 0.5) * PASSO
    n = ORIGEM_NO[1] - (ii + 0.5) * PASSO
    X, Y = T_29_TO_3763.transform(e, n)
    c = ((np.asarray(X) - Tr1.c) / Tr1.a).astype(int)
    rr = ((Tr1.f - np.asarray(Y)) / (-Tr1.e)).astype(int)
    m = np.zeros((H, W), bool)
    ok = (c >= 0) & (c < W) & (rr >= 0) & (rr < H)
    # cada celula de 10 m = 10x10 px de 1 m
    for dr in range(-5, 6):
        for dc in range(-5, 6):
            m[np.clip(rr[ok] + dr, 0, H - 1), np.clip(c[ok] + dc, 0, W - 1)] = True
    return m

mp = para_mdt(pomar)
print("\npomar no MDT: %d px de 1 m = %.2f ha" % (mp.sum(), mp.sum() / 1e4))

# quanta agua de fora entra no pomar: acumulacao a chegar as celulas do pomar
# que vem de celulas fora dele -> aproximacao pelo maximo de acumulacao no bordo
acc_pomar = acc[mp]
print("acumulacao dentro do pomar: mediana %.0f m2 | p95 %.0f | p99 %.0f | max %.0f m2 (%.2f ha)"
      % (np.median(acc_pomar), np.percentile(acc_pomar, 95),
         np.percentile(acc_pomar, 99), acc_pomar.max(), acc_pomar.max() / 1e4))

# bacia a montante de cada foco
do, de = discos_dos_focos(pomar)
zona0 = masc["zona0"]; saud = masc["saudavel"]
print("\nacumulacao (m2 a montante) por unidade, celulas de 1 m:")
linhas = {}
for nome, m10 in (("foco OESTE", do), ("foco ESTE", de), ("zona0", zona0),
                  ("referencia", saud), ("pomar", pomar)):
    m = para_mdt(m10); v = acc[m]
    linhas[nome] = dict(mediana=float(np.median(v)), p95=float(np.percentile(v, 95)),
                        p99=float(np.percentile(v, 99)), maximo=float(v.max()),
                        pct_linha_2000m2=float(100 * (v >= 2000).mean()),
                        pct_linha_10000m2=float(100 * (v >= 10000).mean()))
    print("  %-11s mediana %6.0f | p95 %8.0f | p99 %9.0f | max %10.0f | %%>=2000 m2 %6.3f | %%>=1 ha %5.3f"
          % (nome, np.median(v), np.percentile(v, 95), np.percentile(v, 99), v.max(),
             100 * (v >= 2000).mean(), 100 * (v >= 10000).mean()))

np.save(os.path.join(SAIDA, "c1_05_acumulacao1m.npy"), acc.astype(np.float32))
json.dump({"bacia_json_declarado_ha": bj["ha"],
           "bacia_json_bbox_ha": float((x1 - x0) * (y1 - y0) / 1e4),
           "bacia_json_cobre_pct_do_pomar": float(100 * (pomar & dentro).sum() / pomar.sum()),
           "acc_max_com_flats": float(acc.max()), "acc_max_sem_flats": float(accs.max()),
           "por_unidade": linhas},
          open(os.path.join(SAIDA, "c1_05_bacia.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_05_bacia.json e c1_05_acumulacao1m.npy")
