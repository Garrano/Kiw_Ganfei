# -*- coding: utf-8 -*-
"""C2-12 — INSTRUMENTO INDEPENDENTE para a leitura «2017 era copado a instalar-se».

A afirmacao a testar: as 5,37 ha que em 2017 estavam mais de 0,25 abaixo da
referencia (NDVI medio 0,498, e 0,753 um ano depois) nao eram pomar em
declinio — era vinha por instalar ou acabada de instalar.

Isso e uma leitura de NDVI, e o controlo 1 do CONTROLOS.md nao a deixa passar
para cima verificada so por NDVI. O instrumento independente e a ORTOFOTO, mas
com uma restricao: a R2 G37 proibe comparar brilho entre epocas. Por isso o
teste e feito **dentro de uma so imagem de cada vez**, e nao mede brilho —
mede ESTRUTURA:

  a pergola de kiwi tem postes e cabos em malha regular de ~5 m. Detecta-se
  pela prominencia do primeiro pico secundario da autocorrelacao radial da
  luminancia, em janela de 40 m — a mesma assinatura com que as mascaras
  geograficas foram derivadas (`masks_geograficas.json`, campo `_assinatura`).
  Uma planta debilitada continua a ter postes; terreno por plantar nao tem.

Corre-se sobre 2010 e 2012 (50 cm) e sobre 2021 (25 cm), cada uma isolada, e
compara-se SEMPRE dentro da mesma imagem, entre tres unidades:

  U1  as 5,37 ha em defice grave em 2017
  U2  a referencia sistematica (110 celulas)
  U3  o resto do pomar

Se em 2010 e 2012 a U1 nao tem assinatura de pergola e a U2 tem, e em 2021 as
duas tem, a leitura fica confirmada por um instrumento que nunca viu NDVI.
"""
import json
import os
import sys

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import ndimage, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, NU21 = masc["pomar"], masc["saudavel"], masc["nu2021"] & masc["pomar"]
nd = carrega_ndvi(TODAS)
r17 = float(np.nanmean(nd["2017-07-02"][REF]))
U1 = mapa_defice(nd["2017-07-02"], POMAR, r17, limiar=0.25)
U2 = REF
U3 = POMAR & ~U1 & ~U2
print("U1 defice grave de 2017: %.2f ha | U2 referencia: %.2f ha | U3 resto: %.2f ha"
      % (U1.sum() / 100.0, U2.sum() / 100.0, U3.sum() / 100.0))

ORTOS = [("2010", "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2012", "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25)]
res = {}


def prominencia(bloco, res_m):
    """Prominencia do primeiro pico secundario da autocorrelacao radial.

    Mede periodicidade a escala do compasso (4,4-5,6 m). Nao usa o nivel de
    brilho: a luminancia e centrada e normalizada dentro do proprio bloco.
    """
    x = bloco.astype("float64")
    x = x - x.mean()
    s = x.std()
    if s < 1e-6:
        return np.nan
    x /= s
    F = np.fft.rfft2(x)
    ac = np.fft.irfft2(F * np.conj(F), s=x.shape)
    ac = np.fft.fftshift(ac) / ac.max()
    n0, n1 = np.array(ac.shape) // 2
    yy, xx = np.mgrid[:ac.shape[0], :ac.shape[1]]
    r = np.hypot(yy - n0, xx - n1) * res_m
    perfil, bins = [], np.arange(0, 12.0, res_m)
    for i in range(len(bins) - 1):
        m = (r >= bins[i]) & (r < bins[i + 1])
        perfil.append(ac[m].mean() if m.any() else np.nan)
    perfil = np.array(perfil)
    c = (bins[:-1] + bins[1:]) / 2
    janela = (c >= 4.0) & (c <= 6.2)
    vale = (c >= 2.0) & (c < 4.0)
    if not janela.any() or not vale.any():
        return np.nan
    return float(np.nanmax(perfil[janela]) - np.nanmin(perfil[vale]))


for epoca, ficheiro, res_m in ORTOS:
    caminho = os.path.join(RAIZ, "orto", ficheiro)
    if not os.path.exists(caminho):
        print("falta %s" % ficheiro)
        continue
    ds = rasterio.open(caminho)
    W = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*W, transform=ds.transform)
    lum = np.dstack([ds.read(i, window=w).astype("float32") for i in (1, 2, 3)]).mean(2)
    H, L = lum.shape
    passo = int(round(10.0 / res_m))       # uma celula de 10 m
    print("\n%s: %d x %d px a %.2f m; %d px por celula" % (epoca, L, H, res_m, passo))

    # janela de 40 m centrada em cada celula de 10 m
    meia = int(round(20.0 / res_m))
    P = np.full((NL, NC), np.nan)
    alvo = U1 | U2 | U3
    ys, xs = np.where(alvo)
    for y, x in zip(ys, xs):
        cy = int((y + 0.5) * passo)
        cx = int((x + 0.5) * passo)
        y0, y1 = cy - meia, cy + meia
        x0, x1 = cx - meia, cx + meia
        if y0 < 0 or x0 < 0 or y1 > H or x1 > L:
            continue
        P[y, x] = prominencia(lum[y0:y1, x0:x1], res_m)

    linha = {}
    for nome, m in [("U1 defice grave 2017", U1), ("U2 referencia", U2),
                    ("U3 resto do pomar", U3)]:
        v = P[m & ~np.isnan(P)]
        linha[nome] = dict(n=int(v.size), mediana=float(np.median(v)) if v.size else None,
                           p25=float(np.percentile(v, 25)) if v.size else None,
                           p75=float(np.percentile(v, 75)) if v.size else None)
        print("  %-24s n=%4d  prominencia mediana %.4f  (p25 %.4f, p75 %.4f)"
              % (nome, v.size, np.median(v), np.percentile(v, 25),
                 np.percentile(v, 75)))
    a = P[U1 & ~np.isnan(P)]
    b = P[U2 & ~np.isnan(P)]
    c = P[U3 & ~np.isnan(P)]
    if a.size > 5 and b.size > 5:
        p1 = stats.mannwhitneyu(a, b, alternative="two-sided")[1]
        p2 = stats.mannwhitneyu(a, c, alternative="two-sided")[1]
        print("  U1 contra U2: p=%.2e | U1 contra U3: p=%.2e" % (p1, p2))
        linha["p_U1_U2"] = float(p1)
        linha["p_U1_U3"] = float(p2)
    res[epoca] = linha
    np.save(os.path.join(SAIDA, "c2_12_prom_%s.npy" % epoca), P)

print()
print("=" * 78)
print("LEITURA")
print("=" * 78)
print("  Se a U1 tem prominencia mais BAIXA que a U2 e a U3 em 2010 e 2012, e")
print("  deixa de ter em 2021, entao naquele sitio nao havia pergola nas duas")
print("  primeiras epocas — o defice de 2017 e instalacao, nao declinio.")
for epoca in res:
    r = res[epoca]
    if r["U1 defice grave 2017"]["mediana"] is None:
        continue
    print("  %s: U1 %.4f | U2 %.4f | U3 %.4f  -> U1/U2 = %.2f"
          % (epoca, r["U1 defice grave 2017"]["mediana"], r["U2 referencia"]["mediana"],
             r["U3 resto do pomar"]["mediana"],
             r["U1 defice grave 2017"]["mediana"] / r["U2 referencia"]["mediana"]))

json.dump(res, open(os.path.join(SAIDA, "c2_12_pergola.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_12_pergola.json")
