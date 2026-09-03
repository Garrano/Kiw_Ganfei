# -*- coding: utf-8 -*-
"""Continuacao de `serie_oriental_pergola.py` — recta contra degrau, so em copado.

Porque foi preciso
------------------
A restricao ao copado com pergola respondeu a pergunta que se fez, e no
caminho mostrou outra coisa: **as duas unidades nao tem a mesma FORMA de
serie.**

  ORIENTAL com pergola : desce devagar e continuamente desde 2017.
  OCIDENTAL com pergola: fica colado a referencia oito anos — em cinco das
                         nove cenas ESTA ACIMA dela — e so depois se afasta.

Uma regressao linear sobre nove pontos e o modelo certo para a primeira e o
modelo errado para a segunda: um degrau tardio empurra o declive para cima e
o p para baixo ao mesmo tempo, e o resultado le-se como «nao significativo»
quando o que la esta e o sinal mais limpo do dossie.

Por isso ajustam-se DOIS modelos com o MESMO numero de parametros — recta
(declive + ordenada) contra patamar-ate-2024 mais patamar-2025-26 (duas
medias) — e compara-se a soma dos quadrados dos residuos. Nenhum dos dois e
favorecido pela contagem de parametros.

O teste do degrau e por PERMUTACAO, nao por t. Nove pontos, series temporais,
residuos correlacionados: o t de Welch nao e de confianca. Permuta-se a
etiqueta de ano 20 000 vezes e conta-se quantas vezes um degrau tao grande
aparece por acaso. E a unica das duas contas que nao assume nada.

RESSALVA que acompanha o numero ocidental para onde ele for: o centro do
disco ocidental foi lido de onde o defice de 2026 esta. O TAMANHO do degrau
la dentro esta inflacionado por essa escolha. O que nao esta inflacionado, e
e por isso que a peca P03 existe, e o facto de o nucleo EMERGIR em 2025-26 de
um mapa que nenhuma mascara define.
"""
import json
import os

import numpy as np
import rasterio
from scipy import stats

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"

AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])
TARDIO = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))


def bits(k):
    return np.array([[c == "1" for c in L] for L in g[k]], bool)


POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
ZONA0, NU21 = bits("zona0_bits"), bits("nu2021_bits")
nd = {d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}
h = np.load(os.path.join(VG, "chm_altura.npy"))

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + 0.5) * 10.0,
                     AOI[3] - (np.arange(ny) + 0.5) * 10.0)


def disco(c, r=90.0):
    return ((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r ** 2


FIN = np.isfinite(h)
COM = FIN & (h >= 0.5)
DOC = disco((530485.0, 4655053.0)) & POMAR & COM
DOR = disco((530977.0, 4655117.0)) & POMAR & COM
Z0C = ZONA0 & COM
RESTO = POMAR & COM & ~disco((530485.0, 4655053.0)) & ~disco((530977.0, 4655117.0)) & ~REF

RNG = np.random.default_rng(20260831)
NPERM = 20000


def fosso(m):
    return np.array([float(np.nanmean(nd[d][REF]) - np.nanmean(nd[d][m]))
                     for d in DATAS])


def nivel(m):
    return np.array([float(np.nanmean(nd[d][m])) for d in DATAS])


def permuta_degrau(v):
    """p por permutacao da etiqueta de ano, para uma diferenca de medias."""
    obs = abs(v[TARDIO].mean() - v[~TARDIO].mean())
    k = int(TARDIO.sum())
    n = len(v)
    cnt = 0
    for _ in range(NPERM):
        idx = RNG.permutation(n)[:k]
        sel = np.zeros(n, bool)
        sel[idx] = True
        if abs(v[sel].mean() - v[~sel].mean()) >= obs:
            cnt += 1
    return obs, (cnt + 1) / (NPERM + 1.0)


UN = [("ORIENTAL  Zona 0 com pergola", Z0C),
      ("ORIENTAL  disco 90 m com pergola", DOR),
      ("OCIDENTAL disco 90 m com pergola", DOC),
      ("resto do pomar com pergola", RESTO)]

saida = {"n_perm": NPERM, "datas": DATAS, "unidades": {}}

for etiqueta, serie_f in (("FOSSO A REFERENCIA", fosso), ("NIVEL ABSOLUTO", nivel)):
    print("=" * 86)
    print("RECTA CONTRA DEGRAU  —  %s" % etiqueta)
    print("=" * 86)
    print()
    print("%-34s %10s %9s %10s %10s %9s %9s"
          % ("", "b/ano", "p(b)", "SQR recta", "SQR degrau", "degrau", "p perm"))
    for n_, m in UN:
        v = serie_f(m)
        lr = stats.linregress(anos, v)
        sqr_lin = float(np.sum((v - (lr.intercept + lr.slope * anos)) ** 2))
        c1, c2 = float(v[~TARDIO].mean()), float(v[TARDIO].mean())
        sqr_deg = float(np.sum((v - np.where(TARDIO, c2, c1)) ** 2))
        q = sqr_lin / sqr_deg if sqr_deg else float("inf")
        d, pp = permuta_degrau(v)
        forma = "DEGRAU" if q > 1.5 else ("recta" if q < 0.67 else "indistintos")
        print("%-34s %+10.5f %9.4f %10.5f %10.5f %+9.4f %9.4f   %s (%.2f:1)"
              % (n_, lr.slope, lr.pvalue, sqr_lin, sqr_deg, c2 - c1, pp,
                 forma, q))
        saida["unidades"].setdefault(n_, {})[etiqueta] = dict(
            ha=m.sum() / 100.0, serie=[float(x) for x in v],
            b=float(lr.slope), p_b=float(lr.pvalue), sqr_recta=sqr_lin,
            sqr_degrau=sqr_deg, razao=q, degrau=c2 - c1, p_perm=float(pp),
            forma=forma)
    print()

print("=" * 86)
print("O CONTRASTE, EM UMA LINHA CADA")
print("=" * 86)
print()
o = saida["unidades"]["ORIENTAL  Zona 0 com pergola"]["FOSSO A REFERENCIA"]
w = saida["unidades"]["OCIDENTAL disco 90 m com pergola"]["FOSSO A REFERENCIA"]
print("ORIENTAL  : %s" % "  ".join("%+.3f" % x for x in o["serie"]))
print("OCIDENTAL : %s" % "  ".join("%+.3f" % x for x in w["serie"]))
print()
pre = np.array(w["serie"])[~TARDIO]
print("O ocidental esteve dentro de %+.3f a %+.3f da referencia em 2017-2024, "
      "e ABAIXO dela\nem %d das %d cenas desse periodo. Depois: %+.3f e %+.3f."
      % (pre.min(), pre.max(), int((pre < 0).sum()), len(pre),
         w["serie"][-2], w["serie"][-1]))

json.dump(saida, open(os.path.join(VG, "degrau_vs_recta_pergola.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito degrau_vs_recta_pergola.json")
