# -*- coding: utf-8 -*-
"""P5 — a estrutura desapareceu, ou MUDOU DE COMPASSO?

Porque este ficheiro existe
---------------------------
O P3 concluiu «ORI-COM foi REPLANTADO» a partir de uma coisa só: a prominência
de pérgola caiu de 79 % (2012) para 14 % (2021).

**O P4 contradiz isso.** O NDVI do ORI-COM lê **0,824 · 0,879 · 0,857 · 0,835 ·
0,845 · 0,852 · 0,843** de 2017 a 2024 — sem cova nenhuma. Neste pomar o chão
nu lê 0,49 a 0,61 (NU21). **Um arranque seguido de replantação deixa uma cova de
vários anos, e não há.**

Logo uma das duas leituras está errada, ou as duas medem coisas diferentes.

A hipótese que o P3 não considerou
----------------------------------
`c2_12_pergola_2012.py` procura o pico **só na janela de 4,0 a 6,2 m**, porque
foi assim que o compasso do pomar foi medido. **Se as linhas mudarem de
compasso — replantação com outro espaçamento, ou conversão de latada para outro
sistema de condução — a periodicidade sai da janela e a prominência colapsa sem
que a vegetação mude.**

O instrumento não distingue «estrutura desapareceu» de «estrutura mudou de
escala». Nunca se lhe perguntou.

O teste
-------
Para ORI-COM, ORI-SEM, REF e RESTO, em 2012 e 2021, calcula-se o **perfil radial
completo de 0 a 12 m** e procura-se **onde está o máximo**, sem janela imposta.

  · pico em 4-6 m nas duas épocas  ->  compasso mantém-se; a queda é real
  · pico em 4-6 m em 2012 e NOUTRO sítio em 2021  ->  mudou o compasso, e a
    conclusão de arranque cai
  · sem pico nenhum em 2021  ->  estrutura mesmo desapareceu
"""
import json
import os

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
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


def perfil_radial(bloco, res_m):
    """O perfil INTEIRO, sem janela imposta. Mesma normalizacao do metodo."""
    x = bloco.astype("float64")
    x = x - x.mean()
    s = x.std()
    if s < 1e-6:
        return None
    x /= s
    F = np.fft.rfft2(x)
    ac = np.fft.irfft2(F * np.conj(F), s=x.shape)
    ac = np.fft.fftshift(ac) / ac.max()
    n0, n1 = np.array(ac.shape) // 2
    yy, xx = np.mgrid[:ac.shape[0], :ac.shape[1]]
    r = np.hypot(yy - n0, xx - n1) * res_m
    bins = np.arange(0, 12.0, res_m)
    p = []
    for i in range(len(bins) - 1):
        m = (r >= bins[i]) & (r < bins[i + 1])
        p.append(ac[m].mean() if m.any() else np.nan)
    return np.array(p), (bins[:-1] + bins[1:]) / 2


ORTOS = [("2012", "ortos2012_cog_50cm_rgbi_jpg_002-3_v01.tif", 0.5),
         ("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25)]

print("=" * 92)
print("P5 · ONDE ESTÁ O PICO? — perfil radial completo, sem janela imposta")
print("=" * 92)

saida = {}
for epoca, fich, res_m in ORTOS:
    ds = rasterio.open(os.path.join(S2, "orto", fich))
    W = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*W, transform=ds.transform)
    lum = np.dstack([ds.read(i, window=w).astype("float32")
                     for i in (1, 2, 3)]).mean(2)
    H, L = lum.shape
    passo, meia = int(round(10.0 / res_m)), int(round(20.0 / res_m))
    print()
    print("=" * 92)
    print("%s  (%.2f m)" % (epoca, res_m))
    print("=" * 92)
    saida[epoca] = {}
    for nome, m in UN:
        ys, xs = np.where(m)
        perfis = []
        for y, x in zip(ys, xs):
            cy, cx = int((y + 0.5) * passo), int((x + 0.5) * passo)
            y0, y1, x0, x1 = cy - meia, cy + meia, cx - meia, cx + meia
            if y0 < 0 or x0 < 0 or y1 > H or x1 > L:
                continue
            r = perfil_radial(lum[y0:y1, x0:x1], res_m)
            if r is not None:
                perfis.append(r[0])
                c = r[1]
        if len(perfis) < 5:
            continue
        P = np.nanmedian(np.vstack(perfis), axis=0)
        # pico: maximo local acima de 2 m, para nao apanhar o pico central
        val = c >= 2.0
        i = int(np.nanargmax(np.where(val, P, -np.inf)))
        # prominencia no pico encontrado, contra o vale imediatamente antes
        antes = (c >= 2.0) & (c < c[i])
        prom = float(P[i] - np.nanmin(P[antes])) if antes.any() else float("nan")
        saida[epoca][nome] = dict(pico_m=float(c[i]), valor=float(P[i]),
                                  prominencia_no_pico=prom, n=len(perfis))
        print("  %-9s n=%4d   pico a %4.2f m   valor %+.4f   prominência aí %+.4f"
              % (nome, len(perfis), c[i], P[i], prom))
        # imprime o perfil na zona de interesse
        faixa = (c >= 2.5) & (c <= 9.0)
        print("           perfil 2,5–9 m: %s"
              % "  ".join("%.1f:%+.3f" % (a, b) for a, b in zip(c[faixa], P[faixa])
                          if abs(a - round(a * 2) / 2) < 1e-9))

print()
print("=" * 92)
print("VEREDICTO")
print("=" * 92)
print()
for nome in ("ORI-COM", "REF", "RESTO", "ORI-SEM"):
    a = saida.get("2012", {}).get(nome)
    b = saida.get("2021", {}).get(nome)
    if a and b:
        print("  %-9s  2012: pico a %4.2f m   ->   2021: pico a %4.2f m   %s"
              % (nome, a["pico_m"], b["pico_m"],
                 "MESMO compasso" if abs(a["pico_m"] - b["pico_m"]) < 1.0
                 else "COMPASSO DIFERENTE"))

json.dump(saida, open(os.path.join(VG, "p5_onde_esta_o_pico.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito p5_onde_esta_o_pico.json")
