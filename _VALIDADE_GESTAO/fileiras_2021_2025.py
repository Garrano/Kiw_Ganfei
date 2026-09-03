# -*- coding: utf-8 -*-
"""As fileiras ainda la estao? — gestao contra fisiologia, pela estrutura.

Porque existe
-------------
Tres linhas independentes convergiram na mesma lacuna no mesmo dia:

  1. O gestor: «poda ou arranque de linhas podem ser verificaveis com imagens
     em datas proximas».
  2. O analista independente A, ao declarar o que nao conseguiu determinar:
     nao ha uma unica observacao de terreno, e poda ou arranque dariam
     exactamente o mesmo sinal que doenca.
  3. O adversario da C2: a camada perguntou «aquilo era pomar?» ao ramo
     descendente e nunca ao ramo ASCENDENTE. Faltavam duas linhas para saber
     se as ha de «declinio novo» ainda tem fileiras.

O instrumento
-------------
A prominencia do primeiro pico secundario da autocorrelacao radial, a escala do
compasso de 5 m. E a funcao do `c2_12`, copiada verbatim.

E o unico instrumento de ortofoto comparavel ENTRE EPOCAS, e a razao esta
escrita pela propria C2 no `c2_13`: mede PERIODICIDADE ESPACIAL, nao nivel de
sinal. Uma medida de estrutura e imune ao equilibrio de um JPEG; uma medida de
nivel nao e. As duas ortofotos usadas — 2021 e 2025 — sao ambas a 25 cm.

A leitura
---------
    fileiras presentes em 2021 e em 2025   ->  o copado declinou; a estrutura
                                               fisica esta la. Compativel com
                                               fisiologia, incompativel com
                                               arranque.
    fileiras em 2021 e ausentes em 2025    ->  arranque ou replantacao. O sinal
                                               nao e doenca.
    ausentes em ambas                      ->  nunca foi pomar naquela janela.

Limite declarado: a ortofoto de 2025 e anterior ao incremento de 2026. Testa o
incremento de 2024->2025 (2,91 -> 5,43 ha). Para 2026 nao existe ortofoto, e so
a serie densa intra-estacao pode responder.
"""
import json
import os
import sys

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
from scipy import stats

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF, NU21 = masc["pomar"], masc["saudavel"], masc["nu2021"] & masc["pomar"]
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool)
defice26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)
do, de = discos_dos_focos(POMAR)

UNID = [("NOVO declinio 2026", novo & POMAR),
        ("defice 2026 total", defice26 & POMAR),
        ("foco OESTE", do & POMAR),
        ("foco ESTE plantado", de & POMAR & ~NU21),
        ("referencia sistematica", REF),
        ("resto do pomar", POMAR & ~defice26 & ~REF)]
for n, m in UNID:
    print("%-24s %6.2f ha" % (n, m.sum() / 100.0))


def prominencia(bloco, res_m):
    """Copiada verbatim de c2_12_pergola_2012.py — nao alterar."""
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


ORTOS = [("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25),
         ("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25)]
MAPAS, res = {}, {}
alvo = np.zeros_like(POMAR)
for _, m in UNID:
    alvo |= m

for epoca, ficheiro, res_m in ORTOS:
    caminho = os.path.join(RAIZ, "orto", ficheiro)
    if not os.path.exists(caminho):
        print("FALTA %s" % ficheiro)
        continue
    ds = rasterio.open(caminho)
    W = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*W, transform=ds.transform)
    lum = np.dstack([ds.read(i, window=w).astype("float32")
                     for i in (1, 2, 3)]).mean(2)
    H, L = lum.shape
    passo = int(round(PASSO / res_m))
    meia = int(round(20.0 / res_m))
    print("\n%s  %d x %d px a %.2f m  (CRS %s)" % (epoca, L, H, res_m, ds.crs))
    P = np.full((NL, NC), np.nan)
    ys, xs = np.where(alvo)
    for y, x in zip(ys, xs):
        cy, cx = int((y + 0.5) * passo), int((x + 0.5) * passo)
        if cy - meia < 0 or cx - meia < 0 or cy + meia > H or cx + meia > L:
            continue
        P[y, x] = prominencia(lum[cy - meia:cy + meia, cx - meia:cx + meia], res_m)
    MAPAS[epoca] = P
    res[epoca] = {}
    for nome, m in UNID:
        v = P[m & np.isfinite(P)]
        res[epoca][nome] = dict(n=int(v.size),
                                mediana=float(np.median(v)) if v.size else None)
        print("   %-24s n=%4d  prominencia mediana %.4f"
              % (nome, v.size, np.median(v) if v.size else np.nan))

if len(MAPAS) == 2:
    A, B = MAPAS["2021"], MAPAS["2025"]
    print("\n" + "=" * 68)
    print("VARIACAO 2021 -> 2025 DA ESTRUTURA DE FILEIRAS, celula a celula")
    print("(emparelhado: cada celula e o seu proprio controlo)\n")
    ref = REF & np.isfinite(A) & np.isfinite(B)
    dref = np.median(B[ref] - A[ref])
    print("   deriva geral da referencia sistematica: %+.4f" % dref)
    print("   (subtraida a todas as unidades abaixo — e o que resta de"
          " diferenca de captacao entre as duas ortofotos)\n")
    linhas = {}
    for nome, m in UNID:
        k = m & np.isfinite(A) & np.isfinite(B)
        if k.sum() < 10:
            continue
        d = (B[k] - A[k]) - dref
        w = stats.wilcoxon(B[k] - A[k] - dref)
        perda = float(np.mean(d < -0.10) * 100)
        linhas[nome] = dict(n=int(k.sum()), delta=float(np.median(d)),
                            p=float(w.pvalue), pct_perda=perda)
        print("   %-24s n=%4d  delta %+.4f  p=%.4g  | %5.1f %% das celulas"
              " perdem >0,10" % (nome, k.sum(), np.median(d), w.pvalue, perda))
    print("\n   Leitura: delta proximo de zero = as fileiras aguentaram.")
    print("            delta muito negativo    = estrutura desapareceu.")
    res["variacao_2021_2025"] = linhas
    res["deriva_referencia"] = float(dref)
    np.save(os.path.join(AQUI, "prom_2021.npy"), A)
    np.save(os.path.join(AQUI, "prom_2025.npy"), B)

json.dump(res, open(os.path.join(AQUI, "fileiras.json"), "w"), indent=1)
print("\nescrito fileiras.json")
