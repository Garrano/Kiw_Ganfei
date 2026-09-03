# -*- coding: utf-8 -*-
"""P1 — o foco oriental é copado em declínio, ou copado arrancado?

A pergunta, e quem a fez
-----------------------
`CAMADA_2_CONTROLO3_ADVERSARIO.md`, transversal B, e antes dela o próprio
`PROTOCOLO.md`, onde este teste é **condição de arranque desde a C2 original e
nunca correu**:

  «A partição que sustenta toda a leitura — altura ≥ 0,5 m — vem de um voo que
  cai DENTRO da janela do acontecimento. "Ter pérgola" é um estado
  PÓS-TRATAMENTO. Se alguma parte do foco oriental foi arrancada e re-armada, a
  partição está a seleccionar pelo resultado.»

O discriminador, e é físico
---------------------------
A pérgola de kiwi tem **postes e cabos em malha regular de ~5 m**. O LiDAR mede
o que está acima do chão; a ortofoto mede a estrutura no chão. Cruzando os dois:

  postes SEM copado   ->  a planta morreu ou foi arrancada **sob a estrutura**
                          que ficou de pé.  É DECLÍNIO (ou arranque de plantas).
  SEM postes          ->  nunca esteve plantado, ou a instalação inteira saiu.
                          É OUTRA COISA, e a partição está a medir isso.

O método é o certificado, sem alteração
---------------------------------------
`c2_12_pergola_2012.py`: prominência do primeiro pico secundário da
autocorrelação radial da luminância, janela de 40 m, comparada **dentro de cada
imagem** — a R2 G37 proíbe comparar brilho entre épocas, e esta medida não usa
brilho: centra e normaliza dentro do próprio bloco.

Corre-se em **2021 e 2025**, cada uma isolada. A de 2021 já foi corrida pela C2
para outras unidades e serve de verificação de que reproduzo o método.

As unidades, e são cinco
------------------------
  ORI-COM   foco oriental, células COM pérgola no LiDAR (h >= 0,5)
  ORI-SEM   foco oriental, células SEM pérgola no LiDAR (h < 0,5)   <- a chave
  REF       referência sistemática — tem pérgola de certeza
  RESTO     resto do pomar com pérgola
  NU21      chão lavrado de 2021 — não tem pérgola de certeza

REF e NU21 são as âncoras: uma em cima e uma em baixo, medidas na mesma imagem.
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

UN = [("ORI-COM  foco oriental com pérgola", ZONA0 & COM),
      ("ORI-SEM  foco oriental SEM pérgola", ZONA0 & SEM),
      ("REF      referência sistemática", REF),
      ("RESTO    resto do pomar c/ pérgola", POMAR & COM & ~ZONA0 & ~REF),
      ("NU21     chão lavrado de 2021", NU21 & POMAR)]

ORTOS = [("2021", "ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25),
         ("2025", "ortos2025_cog_25cm_rgbi_jpg_002-3_v01.tif", 0.25)]


def prominencia(bloco, res_m):
    """Copiada de `c2_12_pergola_2012.py`, sem alteração."""
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


print("=" * 92)
print("P1 · PROMINÊNCIA DE PÉRGOLA NO FOCO ORIENTAL — declínio ou arranque?")
print("=" * 92)
print()
for nome, m in UN:
    print("  %-38s %5d células  %5.2f ha" % (nome, m.sum(), m.sum() / 100.0))

saida = {"metodo": "c2_12_pergola_2012.py, sem alteracao", "epocas": {}}
alvo = np.zeros_like(POMAR)
for _, m in UN:
    alvo |= m

for epoca, ficheiro, res_m in ORTOS:
    caminho = os.path.join(S2, "orto", ficheiro)
    if not os.path.exists(caminho):
        print("\nfalta %s" % ficheiro)
        continue
    ds = rasterio.open(caminho)
    W = transform_bounds("EPSG:32629", ds.crs, *AOI)
    w = from_bounds(*W, transform=ds.transform)
    lum = np.dstack([ds.read(i, window=w).astype("float32")
                     for i in (1, 2, 3)]).mean(2)
    H, L = lum.shape
    passo = int(round(10.0 / res_m))
    meia = int(round(20.0 / res_m))
    print()
    print("=" * 92)
    print("%s — %d x %d px a %.2f m" % (epoca, L, H, res_m))
    print("=" * 92)
    print()

    P = np.full((NL, NC), np.nan)
    ys, xs = np.where(alvo)
    for y, x in zip(ys, xs):
        cy, cx = int((y + 0.5) * passo), int((x + 0.5) * passo)
        y0, y1, x0, x1 = cy - meia, cy + meia, cx - meia, cx + meia
        if y0 < 0 or x0 < 0 or y1 > H or x1 > L:
            continue
        P[y, x] = prominencia(lum[y0:y1, x0:x1], res_m)

    linha = {}
    print("%-38s %5s %11s %11s %11s"
          % ("unidade", "n", "mediana", "p25", "p75"))
    for nome, m in UN:
        v = P[m & ~np.isnan(P)]
        if v.size < 5:
            print("%-38s %5d   poucas células" % (nome, v.size))
            continue
        linha[nome] = dict(n=int(v.size), mediana=float(np.median(v)),
                           p25=float(np.percentile(v, 25)),
                           p75=float(np.percentile(v, 75)))
        print("%-38s %5d %11.4f %11.4f %11.4f"
              % (nome, v.size, np.median(v), np.percentile(v, 25),
                 np.percentile(v, 75)))
    saida["epocas"][epoca] = linha

    # a leitura, dentro desta imagem
    if all(k in linha for k in [u[0] for u in UN]):
        ref = linha["REF      referência sistemática"]["mediana"]
        nu = linha["NU21     chão lavrado de 2021"]["mediana"]
        sem = linha["ORI-SEM  foco oriental SEM pérgola"]["mediana"]
        com = linha["ORI-COM  foco oriental com pérgola"]["mediana"]
        span = ref - nu
        print()
        print("  âncoras nesta imagem: REF %.4f (tem pérgola)  ·  NU21 %.4f (não tem)"
              % (ref, nu))
        if abs(span) > 1e-9:
            pos = (sem - nu) / span
            print("  ORI-SEM está a %.0f %% do caminho entre chão lavrado e referência"
                  % (100 * pos))
            saida["epocas"][epoca]["_posicao_ORI_SEM"] = float(pos)

json.dump(saida, open(os.path.join(VG, "p1_pergola_oriental_2025.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito p1_pergola_oriental_2025.json")
