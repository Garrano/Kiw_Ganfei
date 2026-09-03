# -*- coding: utf-8 -*-
"""B1 nao e homogeneo: ha um nucleo em declinio dentro dele.

A media do bloco B1 e plana (-0,013 NDVI/decada, dentro da dispersao) e por
isso o bloco foi descrito como "sem tendencia de declinio". Isso e verdade a
nivel de bloco e ENGANADOR: 0,72 ha em queda dentro de 9,25 ha de copado
ficam diluidos na media.

Este script mapeia o declive por pixel dentro de B1 (so cenas de Jul/Ago, para
nao misturar fenologia), testa se os pixels em queda estao agregados mais do
que o acaso por permutacao espacial, e extrai a serie do nucleo contra o resto
do bloco.

Motivo: a gestora confirmou em 28-08-2026 que as valvulas 2-5 de B1 tem raizes
de Summer Kiwi (sobre-enxertadas com Enza Gold em 2016 e Erica em 2020), e que
a valvula 1 e o resto do pomar sao pe franco de Erica. Se este nucleo for a
valvula 1, o contraste de porta-enxerto fica demonstrado dentro do mesmo bloco,
com agua, solo, gestao e posicao na rede iguais. Se nao for, a hipotese cai.
"""
import csv
import glob
import numpy as np
import rasterio
from scipy import ndimage

LIMIAR = -0.06        # NDVI/decada
N_PERM = 2000
rng = np.random.default_rng(7)

fs = sorted(glob.glob("sentinel_b1/*.tif"))
datas = [f.replace("\\", "/").split("/")[-1][:-4] for f in fs]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in datas])
plena = np.array([int(d[5:7]) in (7, 8) for d in datas])
pilha = np.stack([rasterio.open(f).read(1) for f in fs]).astype("float32")
T = rasterio.open(fs[0]).transform

# copado estavel nas primeiras quatro epocas — mascara geografica, nao derivada
# do periodo que queremos medir
base = np.nanmedian(pilha[:4], axis=0)
cop = ndimage.binary_opening((base > 0.70) & np.isfinite(base), np.ones((2, 2)))
lab, n = ndimage.label(cop)
cop = lab == (int(np.argmax(ndimage.sum(cop, lab, range(1, n + 1)))) + 1)

X = anos[plena]
A = np.vstack([X, np.ones_like(X)]).T
Yf = pilha[plena].reshape(int(plena.sum()), -1)
decl = np.linalg.lstsq(A, np.nan_to_num(Yf, nan=float(np.nanmean(Yf))),
                       rcond=None)[0][0].reshape(pilha.shape[1:]) * 10

queda = cop & (decl < LIMIAR)
k = int(queda.sum())


def maior(m):
    l, _ = ndimage.label(ndimage.binary_opening(m, np.ones((2, 2))))
    return 0 if l.max() == 0 else int(ndimage.sum(m, l, range(1, l.max() + 1)).max())


obs = maior(queda)
idx = np.argwhere(cop)
nulo = np.empty(N_PERM, int)
for i in range(N_PERM):
    m = np.zeros_like(cop)
    s = idx[rng.choice(len(idx), k, replace=False)]
    m[s[:, 0], s[:, 1]] = True
    nulo[i] = maior(m)
p = float((nulo >= obs).mean())

yy, xx = np.mgrid[0:decl.shape[0], 0:decl.shape[1]]
E = T.c + (xx + .5) * T.a
N_ = T.f + (yy + .5) * T.e
nucleo = ndimage.binary_opening(
    queda & (N_ > 4655480) & (E > 528620) & (E < 528820), np.ones((2, 2)))
resto = cop & ~ndimage.binary_dilation(nucleo, np.ones((7, 7)))

print("copado B1        %4d px (%.2f ha)" % (cop.sum(), cop.sum() / 100))
print("abaixo de %.2f  %4d px (%.0f%%; ~10%% seria ruido)"
      % (LIMIAR, k, 100 * k / cop.sum()))
print("maior agregado   %d px | nulo mediana %d, p95 %d | p = %.4f"
      % (obs, np.median(nulo), np.percentile(nulo, 95), p))
print("nucleo norte     %4d px (%.2f ha) | resto %d px"
      % (nucleo.sum(), nucleo.sum() / 100, resto.sum()))
ys, xs = np.where(nucleo)
print("caixa do nucleo  E %.0f–%.0f  N %.0f–%.0f (UTM29N)"
      % ((T.c + xs.min() * T.a), (T.c + (xs.max() + 1) * T.a),
         (T.f + (ys.max() + 1) * T.e), (T.f + ys.min() * T.e)))

with open("b1_nucleo_serie.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["data", "plena_estacao", "nucleo_ndvi", "resto_b1_ndvi",
                "diferenca"])
    for i, d in enumerate(datas):
        a, b = float(np.nanmean(pilha[i][nucleo])), float(np.nanmean(pilha[i][resto]))
        w.writerow([d, int(plena[i]), round(a, 4), round(b, 4), round(a - b, 4)])
print("\nb1_nucleo_serie.csv gravado")
