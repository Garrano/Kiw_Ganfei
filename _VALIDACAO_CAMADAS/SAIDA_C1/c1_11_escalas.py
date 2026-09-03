# -*- coding: utf-8 -*-
"""C1-11 — separar as escalas, e altura sobre a drenagem.

O `declive` de C1-03 e calculado sobre o MDT suavizado a 2,5 m: num pomar com
fiadas de 5 m, sulcos e rodados isso mede micro-relevo de cultivo, nao forma de
terreno. Aqui calcula-se tambem o declive de FORMA (gradiente do MDT suavizado
a 50 m) e a altura sobre a linha de drenagem mais proxima (HAND), que e a
grandeza que governa a profundidade do nivel freatico num aluviao.
"""
import os, sys, json
import numpy as np
import rasterio
from rasterio.transform import Affine
from scipy import stats, ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

meta = json.load(open(os.path.join(SAIDA, "c1_03_dem50.json")))
dem50 = np.load(os.path.join(SAIDA, "c1_03_dem50.npy"))
acc = np.load(os.path.join(SAIDA, "c1_05_acumulacao1m.npy"))     # 1 m
Tr = Affine(*meta["transform"])
Tr1 = Affine(Tr.a * 2, 0, Tr.c, 0, Tr.e * 2, Tr.f)
dem1 = dem50[::2, ::2].astype(np.float64)
H, W = dem1.shape

# --- declive de forma: gradiente do MDT suavizado a 50 m ---
def suav(a, k):
    v = np.nan_to_num(a, nan=0.0); m = (~np.isnan(a)).astype(float)
    ker = np.ones(k) / k
    def sep(x):
        x = ndimage.convolve1d(x, ker, axis=0, mode="nearest")
        return ndimage.convolve1d(x, ker, axis=1, mode="nearest")
    s, w = sep(v), sep(m)
    return np.where(w > 0.2, s / np.maximum(w, 1e-9), np.nan)

d50 = suav(dem1, 51)
gy, gx = np.gradient(d50, 1.0, 1.0)
declive_forma = np.degrees(np.arctan(np.hypot(gx, gy)))

# --- HAND: altura sobre a celula de drenagem mais proxima ---
LIM = 2000.0     # m2 de area contribuinte para uma celula contar como drenagem
dren = acc >= LIM
print("celulas de drenagem (acc >= %.0f m2): %d = %.2f ha (%.2f%% da janela)"
      % (LIM, dren.sum(), dren.sum() / 1e4, 100 * dren.mean()))
idx = ndimage.distance_transform_edt(~dren, return_distances=False, return_indices=True)
z_dren = dem1[idx[0], idx[1]]
hand = dem1 - z_dren
dist_dren = ndimage.distance_transform_edt(~dren)
print("HAND na janela: mediana %.2f m | p95 %.2f m" % (np.nanmedian(hand), np.nanpercentile(hand, 95)))

# --- agregar a grelha de 10 m ---
E29, N29 = centros_celulas()
X, Y = T_29_TO_3763.transform(E29.ravel(), N29.ravel())
col = ((np.asarray(X) - Tr1.c) / Tr1.a).reshape(E29.shape).astype(int)
row = ((Tr1.f - np.asarray(Y)) / (-Tr1.e)).reshape(E29.shape).astype(int)

def agrega(campo, fn=np.nanmedian, meia=5):
    out = np.full(E29.shape, np.nan)
    for i in range(NL):
        for j in range(NC):
            r0, r1 = max(0, row[i, j] - meia), min(H, row[i, j] + meia)
            c0, c1 = max(0, col[i, j] - meia), min(W, col[i, j] + meia)
            if r1 <= r0 or c1 <= c0:
                continue
            bl = campo[r0:r1, c0:c1]
            if np.isnan(bl).all():
                continue
            out[i, j] = fn(bl)
    return out

G = dict(declive_forma=agrega(declive_forma), hand=agrega(hand),
         dist_dren=agrega(dist_dren), acc_p95=agrega(acc, lambda x: np.nanpercentile(x, 95)))
np.savez(os.path.join(SAIDA, "c1_11_escalas.npz"), **G)

masc, _ = carrega_mascaras()
pomar, saud, zona0, nu2021 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(pomar)
g3 = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))

def mw(a, b):
    a = a[~np.isnan(a)]; b = b[~np.isnan(b)]
    return np.median(a) - np.median(b), stats.mannwhitneyu(a, b, alternative="two-sided")[1]

print("\n=== as duas escalas, lado a lado (medianas) ===")
print("%-26s %5s %14s %14s %10s %10s %10s"
      % ("unidade", "n", "declive 2,5 m", "declive 50 m", "HAND m", "d.dren m", "acc p95"))
UN = [("foco OESTE", do), ("foco ESTE", de), ("zona0", zona0),
      ("referencia sistematica", saud), ("nu2021", nu2021 & pomar), ("pomar", pomar)]
saida = {}
for nome, m in UN:
    v = (np.nanmedian(g3["declive"][m]), np.nanmedian(G["declive_forma"][m]),
         np.nanmedian(G["hand"][m]), np.nanmedian(G["dist_dren"][m]),
         np.nanmedian(G["acc_p95"][m]))
    saida[nome] = dict(n=int(m.sum()), declive_micro=float(v[0]), declive_forma=float(v[1]),
                       hand_m=float(v[2]), dist_drenagem_m=float(v[3]), acc_p95_m2=float(v[4]))
    print("%-26s %5d %14.3f %14.3f %10.3f %10.1f %10.0f" % (nome, m.sum(), *v))

print("\n=== testes contra a referencia sistematica ===")
for c in ("declive_forma", "hand", "dist_dren"):
    for nome, m in (("foco OESTE", do), ("foco ESTE", de)):
        d, p = mw(G[c][m], G[c][saud])
        print("  %-14s %-11s %+8.3f  p=%.1e" % (c, nome, d, p))
d, p = mw(G["hand"][do], G["hand"][de])
print("  HAND OESTE - ESTE: %+.3f m  p=%.1e" % (d, p))

print("\n=== declive de forma: o pomar contra o envolvente ===")
longe = ~ndimage.binary_dilation(pomar, np.ones((7, 7)))
cot = g3["cota"]
banda = longe & (cot >= np.nanpercentile(cot[pomar], 2)) & (cot <= np.nanpercentile(cot[pomar], 98)) \
        & ~np.isnan(G["declive_forma"])
d, p = mw(G["declive_forma"][pomar], G["declive_forma"][banda])
print("  pomar %.3f deg | envolvente %.3f deg | dif %+.3f  p=%.1e"
      % (np.nanmedian(G["declive_forma"][pomar]), np.nanmedian(G["declive_forma"][banda]), d, p))
print("  (o declive a 2,5 m dava o pomar MUITO mais inclinado que o envolvente;")
print("   a 50 m a diferenca e outra. A 2,5 m estava a medir sulcos, nao forma.)")

json.dump(saida, open(os.path.join(SAIDA, "c1_11_escalas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_11_escalas.npz/.json")
