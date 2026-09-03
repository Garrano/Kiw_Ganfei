# -*- coding: utf-8 -*-
"""C1-10 — nivelamento/truncatura, e verificacao do MDT por instrumento externo.

Tres coisas:
 (a) Copernicus GLO-30 (`lidar/_glo30.tif`) — modelo de elevacao de radar
     (TanDEM-X), missao, sensor e processamento inteiramente distintos do
     LiDAR aereo da DGT. E o instrumento independente para o contraste de cota
     entre os dois focos.
 (b) O chao lavrado de 2021 (`nu2021`) contra o resto do foco ESTE: a diferenca
     de terreno e do foco ou so da parte lavrada?
 (c) Hipotese de nivelamento: a superficie do pomar e mais plana/regular do que
     o terreno envolvente? Se houve emparcelamento com terraplanagem ha ~35
     anos, deve ver-se como excesso de planaridade a escala das parcelas.
"""
import os, sys, json
import numpy as np
import rasterio
from rasterio.transform import Affine
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

g = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))
masc, _ = carrega_mascaras()
pomar, saud, zona0, nu2021 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(pomar)
E29, N29 = centros_celulas()

def mw(a, b):
    a = a[~np.isnan(a)]; b = b[~np.isnan(b)]
    if len(a) < 5 or len(b) < 5:
        return np.nan, np.nan
    return np.median(a) - np.median(b), stats.mannwhitneyu(a, b, alternative="two-sided")[1]

# ---------- (a) instrumento independente: Copernicus GLO-30 ----------
print("=== (a) GLO-30 (radar TanDEM-X) contra o LiDAR aereo da DGT ===")
with rasterio.open(os.path.join(RAIZ, "lidar", "_glo30.tif")) as s:
    glo = s.read(1).astype("float64")
    Tg = s.transform
    glo[glo <= -1000] = np.nan
lon, lat = T_29_TO_WGS.transform(E29.ravel(), N29.ravel())
cg = ((np.asarray(lon) - Tg.c) / Tg.a).astype(int).reshape(E29.shape)
rg = ((np.asarray(lat) - Tg.f) / Tg.e).astype(int).reshape(E29.shape)
ok = (cg >= 0) & (cg < glo.shape[1]) & (rg >= 0) & (rg < glo.shape[0])
gl = np.full(E29.shape, np.nan)
gl[ok] = glo[rg[ok], cg[ok]]
print("  GLO-30 e um MDS: inclui copado e rede. Compara-se so o CONTRASTE entre")
print("  unidades, nunca o valor absoluto.")
print("  %-26s %9s %9s" % ("unidade", "LiDAR", "GLO-30"))
vals = {}
for nome, m in (("foco OESTE", do), ("foco ESTE", de), ("zona0", zona0), ("referencia", saud)):
    a, b = np.nanmedian(g["cota"][m]), np.nanmedian(gl[m])
    vals[nome] = (a, b)
    print("  %-26s %9.3f %9.3f" % (nome, a, b))
dl = vals["foco ESTE"][0] - vals["foco OESTE"][0]
dg = vals["foco ESTE"][1] - vals["foco OESTE"][1]
print("  ESTE menos OESTE:  LiDAR %+.3f m | GLO-30 %+.3f m" % (dl, dg))
print("  => o contraste de cota entre focos e confirmado por instrumento independente? %s"
      % ("SIM, mesmo sinal e mesma ordem de grandeza" if dg > 0.3 and abs(dg - dl) < 1.5 else "ver valores"))
# correlacao espacial dos dois modelos sobre o pomar
m = pomar & ~np.isnan(gl) & ~np.isnan(g["cota"])
r, p = stats.pearsonr(g["cota"][m], gl[m])
print("  correlacao LiDAR x GLO-30 nas %d celulas do pomar: r=%+.3f (p=%.1e)" % (m.sum(), r, p))

# ---------- (b) o chao lavrado de 2021 dentro do foco ESTE ----------
print("\n=== (b) `nu2021` contra o resto do foco ESTE ===")
dentro = de & nu2021
fora = de & ~nu2021
print("  foco ESTE: %d celulas, das quais %d lavradas em 2021 (%.0f%%) e %d nao"
      % (de.sum(), dentro.sum(), 100 * dentro.sum() / de.sum(), fora.sum()))
for c in ("cota", "declive", "rug25", "res150", "tpi"):
    d, p = mw(g[c][dentro], g[c][fora])
    print("  %-8s lavrado - nao lavrado, DENTRO do foco ESTE: %+8.3f  p=%.1e" % (c, d, p))
print("  o resto do foco ESTE (nao lavrado) contra a referencia:")
for c in ("cota", "declive", "rug25"):
    d, p = mw(g[c][fora], g[c][saud])
    print("  %-8s %+8.3f  p=%.1e" % (c, d, p))
print("  onde esta o `nu2021` fora do foco ESTE: %d celulas" % (nu2021 & ~de).sum())
if (nu2021 & ~de).sum():
    mm = nu2021 & ~de
    print("     E %.0f..%.0f  N %.0f..%.0f" % (E29[mm].min(), E29[mm].max(), N29[mm].min(), N29[mm].max()))

# ---------- (c) nivelamento: planaridade do pomar contra o envolvente ----------
print("\n=== (c) hipotese de nivelamento / terraplanagem ===")
# envolvente: fora do pomar, dentro da AOI, mesma gama de cota (aluviao), a >30 m do pomar
from scipy import ndimage
longe = ~ndimage.binary_dilation(pomar, np.ones((7, 7)))
cot = g["cota"]
banda = longe & (cot >= np.nanpercentile(cot[pomar], 2)) & (cot <= np.nanpercentile(cot[pomar], 98))
banda &= ~np.isnan(g["rug25"])
print("  envolvente comparavel (mesma gama de cota, >30 m do pomar): %d celulas = %.1f ha"
      % (banda.sum(), banda.sum() / 100))
for c in ("rug25", "declive", "res150", "cota_dp"):
    d, p = mw(g[c][pomar], g[c][banda])
    print("  %-8s pomar - envolvente %+8.4f  p=%.1e   (pomar %.4f | envolvente %.4f)"
          % (c, d, p, np.nanmedian(g[c][pomar]), np.nanmedian(g[c][banda])))

# planaridade a escala de parcela: residuo de um plano ajustado em janelas de 60 m
print("\n  planaridade a escala de parcela (residuo de plano em janelas de 60 m):")
def resid_plano(masc_alvo, lado=6):
    out = []
    ii, jj = np.nonzero(masc_alvo)
    for i0 in range(0, NL - lado, lado):
        for j0 in range(0, NC - lado, lado):
            bl = masc_alvo[i0:i0 + lado, j0:j0 + lado]
            if bl.sum() < lado * lado * 0.9:
                continue
            z = cot[i0:i0 + lado, j0:j0 + lado]
            if np.isnan(z).any():
                continue
            yy, xx = np.mgrid[0:lado, 0:lado]
            A = np.c_[xx.ravel(), yy.ravel(), np.ones(lado * lado)]
            coef, *_ = np.linalg.lstsq(A, z.ravel(), rcond=None)
            out.append(np.std(z.ravel() - A @ coef))
    return np.array(out)
rp = resid_plano(pomar); rb = resid_plano(banda)
print("     pomar:      n=%3d janelas, residuo mediano %.4f m (p90 %.4f)"
      % (len(rp), np.median(rp) if len(rp) else np.nan, np.percentile(rp, 90) if len(rp) else np.nan))
print("     envolvente: n=%3d janelas, residuo mediano %.4f m (p90 %.4f)"
      % (len(rb), np.median(rb) if len(rb) else np.nan, np.percentile(rb, 90) if len(rb) else np.nan))
if len(rp) > 5 and len(rb) > 5:
    print("     Mann-Whitney p = %.1e" % stats.mannwhitneyu(rp, rb, alternative="two-sided")[1])

# gradiente longitudinal: o pomar desce de leste para oeste?
print("\n  perfil longitudinal do pomar (eixo azimute 70,3 deg, R2 G3):")
az = np.radians(70.3)
s = (E29 - 530791.0) * np.sin(az) + (N29 - 4655130.0) * np.cos(az)
b = stats.linregress(s[pomar], cot[pomar])
print("     declive ao longo do eixo: %+.5f m/m = %+.3f %%  (r2 %.3f, p %.1e)"
      % (b.slope, 100 * b.slope, b.rvalue ** 2, b.pvalue))
print("     s do foco OESTE %.0f m | s do foco ESTE %.0f m | amplitude do pomar %.0f m"
      % (np.median(s[do]), np.median(s[de]), s[pomar].max() - s[pomar].min()))
res_eixo = cot - (b.slope * s + b.intercept)
for nome, m in (("foco OESTE", do), ("foco ESTE", de), ("zona0", zona0),
                ("referencia", saud), ("nu2021", nu2021 & pomar)):
    print("     residuo em relacao ao perfil, %-11s %+.3f m" % (nome, np.nanmedian(res_eixo[m])))

json.dump({"glo30_este_menos_oeste_m": float(dg), "lidar_este_menos_oeste_m": float(dl),
           "correlacao_lidar_glo30_r": float(r),
           "declive_eixo_pct": float(100 * b.slope),
           "residuo_eixo": {n: float(np.nanmedian(res_eixo[m])) for n, m in
                            (("foco_oeste", do), ("foco_este", de), ("zona0", zona0),
                             ("referencia", saud), ("nu2021", nu2021 & pomar))}},
          open(os.path.join(SAIDA, "c1_10_nivelamento.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_10_nivelamento.json")
