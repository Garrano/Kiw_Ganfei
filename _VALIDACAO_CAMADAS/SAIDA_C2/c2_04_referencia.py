# -*- coding: utf-8 -*-
"""C2-04 — a referencia esta a descer. E do pomar, da atmosfera ou do satelite?

A R2 G6/G25 fixa que a referencia sistematica desce, 0,8884 -> 0,8425,
-0,00395/ano, e chama-lhe «o facto mais importante desta revisao». A C1
reproduziu-o. Mas ninguem perguntou de onde vem a descida, e ha um confundente
que salta a vista assim que se juntam as datas com os identificadores das cenas
do `proveniencia.json`:

  2017-07-02  S2B   ref 0,888        2023-08-07  S2B   ref 0,917
  2018-08-31  S2A   ref 0,904        2024-07-22  S2B   ref 0,897
  2019-09-02  S2A   ref 0,916        2025-06-17  S2A   ref 0,876
  2020-07-18  S2A   ref 0,891        2025-08-14  S2C   ref 0,860
  2021-07-16  S2A   ref 0,901        2026-07-27  S2C   ref 0,843
  2022-07-31  S2A   ref 0,898

**Os dois valores mais baixos da serie sao as duas unicas cenas do S2C.** Se a
descida for do sensor, ela nao e do pomar — e o «facto mais importante da R2»
muda de natureza (nao deixa de ser verdade que a referencia antiga subia por
construcao; deixa de ser verdade que a nova desce por causa do pomar).

O teste tem de usar alvos FORA do pomar, na mesma cena. Se todo o verde da AOI
desce nas cenas S2C, e da cena. Se so o pomar desce, e do pomar.

Tres alvos, por ordem de independencia:
  T1  toda a AOI fora do pomar (nenhuma escolha, nenhum criterio)
  T2  mata/galeria estavel: pixeis fora do pomar com NDVI alto e variancia baixa
      **definidos so com 2017-2024** — as cenas em teste nao entram na escolha
  T3  o proprio pomar

Isto NAO desfaz a metrica de defice: ela usa a referencia da propria data e e
uma diferenca dentro da cena, logo e imune a qualquer degrau de cena. O que
esta em causa e a leitura do NIVEL ABSOLUTO.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
nd = carrega_ndvi(TODAS)
SERIE = sorted(DATAS + ["2019-09-02"])

with open(os.path.join(RAIZ, "sentinel", "proveniencia.json"), encoding="latin-1") as f:
    prov = {c["data"]: c["cena"] for c in json.load(f)["cenas"]}
plat = {d: prov[d][:3] for d in TODAS}

FORA = ~POMAR
# T2: definido SO com 2017-2024. As cenas em teste (2025, 2026) nao entram.
cal = [d for d in TODAS if d < "2025"]
pilha = np.stack([nd[d] for d in cal])
mu, sd = np.nanmean(pilha, 0), np.nanstd(pilha, 0)
T2 = FORA & (mu > 0.80) & (sd < 0.04)
print("T2 (mata/galeria estavel, definida so com 2017-2024): %d celulas (%.2f ha)"
      % (T2.sum(), T2.sum() / 100.0))
print("T1 (tudo fora do pomar): %d celulas" % FORA.sum())

print()
print("=" * 78)
print("NIVEL DE NDVI POR ALVO, E O SATELITE DE CADA CENA")
print("=" * 78)
print("%-12s %5s %8s %10s %10s %10s %10s" %
      ("data", "sat", "DOY", "referencia", "T2 estav.", "T1 fora", "pomar"))
tab = {}
for d in SERIE:
    r = dict(sat=plat[d], doy=doy(d),
             ref=float(np.nanmean(nd[d][REF])),
             t2=float(np.nanmean(nd[d][T2])),
             t1=float(np.nanmedian(nd[d][FORA])),
             pomar=float(np.nanmean(nd[d][POMAR])))
    tab[d] = r
    print("%-12s %5s %8d %10.3f %10.3f %10.3f %10.3f"
          % (d, r["sat"], r["doy"], r["ref"], r["t2"], r["t1"], r["pomar"]))

print()
print("=" * 78)
print("DECLIVES 2017-2026 POR ALVO")
print("=" * 78)
an = anos_decimais(SERIE)
for k, nome in [("ref", "referencia sistematica"), ("t2", "T2 mata estavel"),
                ("t1", "T1 mediana fora do pomar"), ("pomar", "pomar inteiro")]:
    v = np.array([tab[d][k] for d in SERIE])
    r = stats.linregress(an, v)
    print("  %-26s %+0.5f/ano  p=%.4f   2017 %.3f -> 2026 %.3f  (%+0.3f)"
          % (nome, r.slope, r.pvalue, v[0], v[-1], v[-1] - v[0]))

print()
print("=" * 78)
print("AS DUAS CENAS S2C CONTRA AS OITO ANTERIORES, POR ALVO")
print("=" * 78)
s2c = [d for d in SERIE if plat[d] == "S2C"]
ant = [d for d in SERIE if plat[d] != "S2C"]
print("  cenas S2C: %s" % ", ".join(s2c))
for k, nome in [("ref", "referencia sistematica"), ("t2", "T2 mata estavel"),
                ("t1", "T1 mediana fora do pomar"), ("pomar", "pomar inteiro")]:
    a = np.array([tab[d][k] for d in ant])
    b = np.array([tab[d][k] for d in s2c])
    print("  %-26s antes %.3f | S2C %.3f | degrau %+0.3f"
          % (nome, a.mean(), b.mean(), b.mean() - a.mean()))

print()
print("  --- e a cena de 2025-06-17, que e S2A e ja esta baixa? ---")
d = "2025-06-17"
r = dict(sat=plat[d], ref=float(np.nanmean(nd[d][REF])), t2=float(np.nanmean(nd[d][T2])),
         t1=float(np.nanmedian(nd[d][FORA])), pomar=float(np.nanmean(nd[d][POMAR])))
print("  %-12s %5s  ref %.3f  T2 %.3f  T1 %.3f  pomar %.3f"
      % (d, r["sat"], r["ref"], r["t2"], r["t1"], r["pomar"]))

print()
print("=" * 78)
print("A GRANDEZA QUE INTERESSA: referencia MENOS alvo externo, dentro da cena")
print("=" * 78)
print("  Se a descida for da cena, esta diferenca fica constante.")
print("  Se for do pomar, ela abre.")
print("%-12s %5s %14s %14s" % ("data", "sat", "ref - T2", "pomar - T2"))
for d in SERIE:
    print("%-12s %5s %14.3f %14.3f"
          % (d, plat[d], tab[d]["ref"] - tab[d]["t2"], tab[d]["pomar"] - tab[d]["t2"]))
v = np.array([tab[d]["ref"] - tab[d]["t2"] for d in SERIE])
r = stats.linregress(an, v)
print("\n  ref - T2:  declive %+0.5f/ano  p=%.4f" % (r.slope, r.pvalue))
v2 = np.array([tab[d]["pomar"] - tab[d]["t2"] for d in SERIE])
r2 = stats.linregress(an, v2)
print("  pomar - T2: declive %+0.5f/ano  p=%.4f" % (r2.slope, r2.pvalue))

json.dump(dict(tabela=tab, satelite=plat, t2_celulas=int(T2.sum())),
          open(os.path.join(SAIDA, "c2_04_referencia.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
np.save(os.path.join(SAIDA, "c2_04_T2.npy"), T2)
print("\nescrito c2_04_referencia.json / c2_04_T2.npy")
