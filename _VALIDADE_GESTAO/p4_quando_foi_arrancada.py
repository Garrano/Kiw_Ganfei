# -*- coding: utf-8 -*-
"""P4 — quando foi arrancada a pérgola do ORI-COM?

Duas metades, e são perguntas diferentes
----------------------------------------
O P3 estabeleceu: **ORI-COM tinha pérgola em 2010 (111 %) e 2012 (79 %), e não
tinha em 2021 (14 %).** O arranque está entre 2012 e 2021.

**As ortofotos de 2004 e 2007 são ANTERIORES a 2010 — não estreitam o
arranque.** Dizem quando foi *plantada*, que é outra pergunta e também interessa
(uma pérgola de 2004 arrancada em ~2015 tem uma história diferente de uma de
2009 arrancada com seis anos).

**O que estreita o arranque é a série óptica**, que cobre precisamente o
intervalo cego: Landsat desde 2013 e Sentinel-2 desde 2017. Se o ORI-COM já
lesse baixo em 2017, foi arrancado antes; se lesse alto e caísse depois, a data
fica dentro da série.

Este ficheiro faz as duas coisas
--------------------------------
**A ·** prominência de pérgola em 1995, 2004-2006 e 2007, com o método
certificado, sem alteração. Verifica-se primeiro se cada imagem discrimina —
1995 é a 1 m e infravermelho-vermelho-verde, e um compasso de 5 m a 1 m de
resolução são cinco píxeis: pode não chegar. Diz-se.

**B ·** o NDVI absoluto do ORI-COM em cada cena da série, contra a referência e
contra o ORI-SEM. Não é prominência: é nível. Serve para datar, não para
classificar.
"""
import json
import os

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
AOI = (529950, 4654600, 531950, 4655600)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
ZONA0, NU21 = bits("zona0_bits"), bits("nu2021_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
FIN = np.isfinite(h)
COM, SEM = FIN & (h >= 0.5), FIN & (h < 0.5)
NL, NC = POMAR.shape

UN = [("ORI-COM", ZONA0 & COM), ("ORI-SEM", ZONA0 & SEM),
      ("REF", REF), ("RESTO", POMAR & COM & ~ZONA0 & ~REF),
      ("NU21", NU21 & POMAR)]


def prominencia(bloco, res_m):
    """Copiada de `c2_12_pergola_2012.py`, sem alteracao."""
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


# 2010 e 2012 entram NAO por interesse — ja estao certificados — mas para
# VERIFICAR o meu caminho de codigo a 50 cm contra os mapas da C2. Se os meus
# numeros baterem com `c2_12_prom_2010.npy` e `_2012.npy`, entao o que eu
# calcular para 2004-06 e 2007, que partilham o mesmo caminho, e de confianca.
# Sem esta verificacao, os numeros novos nao tem contra o que ser lidos.
ORTOS = [("1995", "ortos1995_cog_1m_irg_jpg_002-3_v01.tif", 1.0),
         ("2004-06", "ortos20042006_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2007", "ortos2007_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2010 [verif]", "ortos2010_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2012 [verif]", "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5)]
CERT = {"2010 [verif]": "c2_12_prom_2010.npy",
        "2012 [verif]": "c2_12_prom_2012.npy"}

print("=" * 90)
print("A · PROMINÊNCIA DE PÉRGOLA ANTES DE 2010")
print("=" * 90)

saida = {"A_prominencia": {}, "B_ndvi": {}}
alvo = np.zeros_like(POMAR)
for _, m in UN:
    alvo |= m

for epoca, fich, res_m in ORTOS:
    caminho = os.path.join(S2, "orto", fich)
    if not os.path.exists(caminho):
        print("\nfalta %s" % fich)
        continue
    ds = rasterio.open(caminho)
    W = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*W, transform=ds.transform)
    nb = min(3, ds.count)
    lum = np.dstack([ds.read(i, window=w).astype("float32")
                     for i in range(1, nb + 1)]).mean(2)
    H, L = lum.shape
    passo, meia = int(round(10.0 / res_m)), int(round(20.0 / res_m))
    P = np.full((NL, NC), np.nan)
    ys, xs = np.where(alvo)
    for y, x in zip(ys, xs):
        cy, cx = int((y + 0.5) * passo), int((x + 0.5) * passo)
        y0, y1, x0, x1 = cy - meia, cy + meia, cx - meia, cx + meia
        if y0 < 0 or x0 < 0 or y1 > H or x1 > L:
            continue
        P[y, x] = prominencia(lum[y0:y1, x0:x1], res_m)

    linha = {}
    for nome, m in UN:
        v = P[m & np.isfinite(P)]
        if v.size >= 5:
            linha[nome] = dict(n=int(v.size), mediana=float(np.median(v)),
                               p25=float(np.percentile(v, 25)),
                               p75=float(np.percentile(v, 75)))
    R, N = linha.get("REF"), linha.get("NU21")
    sep = bool(R and N and R["p25"] > N["p75"])
    print()
    print("%s  (%.2f m, %d bandas)   âncoras: REF %.4f · NU21 %.4f · %s"
          % (epoca, res_m, nb, R["mediana"] if R else float("nan"),
             N["mediana"] if N else float("nan"),
             "DISCRIMINA" if sep else "NÃO DISCRIMINA"))
    if sep:
        span = R["mediana"] - N["mediana"]
        for nome in linha:
            linha[nome]["pos"] = float(100 * (linha[nome]["mediana"] - N["mediana"]) / span)
        for nome in ("ORI-COM", "ORI-SEM", "RESTO", "REF", "NU21"):
            if nome in linha:
                print("    %-10s %6.0f %%   (mediana %+.4f, n=%d)"
                      % (nome, linha[nome]["pos"], linha[nome]["mediana"],
                         linha[nome]["n"]))
    saida["A_prominencia"][epoca] = dict(discrimina=sep, res_m=res_m,
                                         bandas=nb, unidades=linha)

    # verificacao contra o mapa certificado, quando existe
    if epoca in CERT:
        Q = np.load(os.path.join(C2, CERT[epoca]))
        d = P[np.isfinite(P) & np.isfinite(Q)] - Q[np.isfinite(P) & np.isfinite(Q)]
        print("    VERIFICAÇÃO contra %s: n=%d  |máx dif| = %.2e  mediana = %+.2e"
              % (CERT[epoca], d.size, np.abs(d).max(), np.median(d)))
        saida["A_prominencia"][epoca]["verificacao_max_dif"] = float(np.abs(d).max())

# ------------------------------------------------------------------ parte B
print()
print("=" * 90)
print("B · O QUE A SÉRIE ÓPTICA DIZ NO INTERVALO CEGO (2013-2021)")
print("=" * 90)
print()

LS = json.load(open(os.path.join(VG, "landsat.json")))
anos_ls = sorted({int(r["data"][:4]) for r in LS})
print("Landsat, mediana anual de NDVI — unidades da C2 (disco de 90 m):")
print("%-26s %s" % ("", "  ".join("%4d" % a for a in anos_ls)))
for k in ("ESTE com pergola", "ESTE sem pergola", "referencia"):
    v = []
    for a in anos_ls:
        x = [r[k] for r in LS if int(r["data"][:4]) == a and r.get(k) is not None]
        v.append(np.median(x) if x else np.nan)
    print("%-26s %s" % (k, "  ".join("%.3f" % z for z in v)))
    saida["B_ndvi"]["landsat_" + k] = [float(z) for z in v]

DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
print()
print("Sentinel-2, nível absoluto nas unidades DESTE ficheiro:")
print("%-12s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
for nome, m in UN:
    v = []
    for d in DATAS:
        a = rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
        v.append(float(np.nanmean(a[m])))
    print("%-12s %s" % (nome, "  ".join("%.3f" % z for z in v)))
    saida["B_ndvi"]["s2_" + nome] = v

print()
print("=" * 90)
print("LEITURA")
print("=" * 90)
print()
oc = saida["B_ndvi"]["s2_ORI-COM"]
rf = saida["B_ndvi"]["s2_REF"]
print("ORI-COM contra a referência, por cena:")
for d, a, b in zip(DATAS, oc, rf):
    print("   %s   %.3f  contra %.3f   ->  fosso %+.3f" % (d, a, b, b - a))

json.dump(saida, open(os.path.join(VG, "p4_quando_foi_arrancada.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito p4_quando_foi_arrancada.json")
