# -*- coding: utf-8 -*-
"""C2-05 — geometria das manchas: emergencia, sensibilidade, e a regra M2.

Quatro perguntas:

  A) O FOCO OESTE emerge sozinho de mascaras que nunca ouviram falar dele
     (R2 G29)? E se sim, quao robusta e a emergencia ao limiar e ao elemento
     estruturante? Se a mancha so existir a limiar 0,05 com abertura 2x2,
     nao e um achado, e uma escolha.

  B) A REGRA M2 — so conta como declinio o que esteve comprovadamente sao
     antes. Quanto do defice de 2026 passa nessa regra?

  C) A geometria: frente em avanco ou nucleos difusos? Mede-se pela distancia
     das celulas novas as celulas ja em defice no ano anterior. Uma frente que
     avanca po-las todas encostadas; nucleos novos po-las longe.

  D) Datacao celula a celula: em que ano e que cada celula do defice de 2026
     entrou em defice, e ficou la.
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"] & masc["pomar"]
SERIE = sorted(DATAS + ["2019-09-02"])
nd = carrega_ndvi(TODAS)
REFV = {d: float(np.nanmean(nd[d][REF])) for d in TODAS}
E, N = centros_celulas()
res = {}

print("=" * 78)
print("A) O FOCO OESTE EMERGE SOZINHO? SENSIBILIDADE AO LIMIAR E AO ELEMENTO")
print("=" * 78)
print("  Procura-se, sem nenhuma mascara, o maior nucleo contiguo a menos de")
print("  120 m de E530485 N4655053 (o centro declarado do foco OESTE), em cada")
print("  ano e para cada combinacao (limiar, elemento). A coordenada e usada so")
print("  para IDENTIFICAR o nucleo depois de ele aparecer, nunca para o criar.")
LIM = [0.03, 0.05, 0.08, 0.10, 0.15]
ELEM = [("nenhum", None), ("2x2", (2, 2)), ("3x3", (3, 3))]


def nucleo_junto(d, limiar, elem, centro, raio=120.0):
    b = mapa_defice(nd[d], POMAR, REFV[d], limiar=limiar, abertura=elem)
    lab, n = ndimage.label(b, np.ones((3, 3)))
    melhor = (0.0, None, None)
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 5:
            continue
        ce, cn = E[m].mean(), N[m].mean()
        if (ce - centro[0]) ** 2 + (cn - centro[1]) ** 2 <= raio ** 2:
            if m.sum() / 100.0 > melhor[0]:
                melhor = (m.sum() / 100.0, ce, cn)
    return melhor


for nome_e, elem in ELEM:
    print("\n  --- elemento %s ---" % nome_e)
    print("  %-12s %s" % ("data", "".join("%12.2f" % t for t in LIM)))
    for d in SERIE:
        v = [nucleo_junto(d, t, elem, FOCO_OESTE)[0] for t in LIM]
        print("  %-12s %s" % (d, "".join("%12.2f" % x for x in v)))
        res.setdefault("oeste_sens", {}).setdefault(nome_e, {})[d] = [float(x) for x in v]

print("\n  Conclusao a ler na tabela: em quantas das %d combinacoes"
      % (len(LIM) * len(ELEM)))
print("  (limiar x elemento) o nucleo do OESTE esta AUSENTE em 2024 e PRESENTE em 2026?")
aus = pres = amb = 0
for nome_e in [n for n, _ in ELEM]:
    for i, t in enumerate(LIM):
        a24 = res["oeste_sens"][nome_e]["2024-07-22"][i]
        a26 = res["oeste_sens"][nome_e]["2026-07-27"][i]
        if a24 < 0.15 and a26 >= 0.15:
            amb += 1
        if a24 >= 0.15:
            pres += 1
        if a26 < 0.15:
            aus += 1
print("  ausente em 2024 E presente em 2026: %d de %d combinacoes"
      % (amb, len(LIM) * len(ELEM)))
print("  presente ja em 2024 (contradiz a emergencia): %d" % pres)
print("  ausente ainda em 2026: %d" % aus)

print("\n  Centroide do nucleo OESTE, na definicao operativa (0,05 / 2x2):")
for d in SERIE:
    a, ce, cn = nucleo_junto(d, 0.05, (2, 2), FOCO_OESTE)
    if a:
        print("    %s  %.2f ha  centro E%.0f N%.0f  (a %.0f m do centro declarado)"
              % (d, a, ce - 5, cn + 5,
                 np.hypot(ce - 5 - FOCO_OESTE[0], cn + 5 - FOCO_OESTE[1])))
    else:
        print("    %s  ausente" % d)

print()
print("=" * 78)
print("B) REGRA M2 — so conta como declinio o que esteve comprovadamente sao")
print("=" * 78)
M = {d: mapa_defice(nd[d], POMAR, REFV[d]) for d in SERIE}
antes = [d for d in SERIE if d < "2025"]
SAO_ANTES = POMAR & ~np.any([M[d] for d in antes], axis=0)   # nunca em defice ate 2024
print("  Celulas do pomar que NUNCA estiveram em defice de 2017 a 2024:")
print("    %d celulas, %.2f ha (%.0f%% do pomar)"
      % (SAO_ANTES.sum(), SAO_ANTES.sum() / 100.0, 100.0 * SAO_ANTES.sum() / POMAR.sum()))
d26 = M["2026-07-27"]
d25 = M["2025-08-14"]
print("\n  Defice de 2026: %.2f ha. Destes:" % (d26.sum() / 100.0))
print("    %.2f ha passam a regra M2 (estiveram sempre sos ate 2024)"
      % ((d26 & SAO_ANTES).sum() / 100.0))
print("    %.2f ha ja tinham estado em defice alguma vez ate 2024"
      % ((d26 & ~SAO_ANTES).sum() / 100.0))
print("  Defice de 2025: %.2f ha, dos quais %.2f ha passam a M2"
      % (d25.sum() / 100.0, (d25 & SAO_ANTES).sum() / 100.0))
novo = d26 & SAO_ANTES
res["m2"] = dict(sao_antes_ha=SAO_ANTES.sum() / 100.0,
                 defice26_ha=d26.sum() / 100.0,
                 novo26_ha=float((d26 & SAO_ANTES).sum() / 100.0),
                 novo25_ha=float((d25 & SAO_ANTES).sum() / 100.0))

print("\n  Onde esta esse declinio novo? nucleos >= 0,15 ha:")
for a, ce, cn, c in nucleos(novo):
    do_ = np.hypot(ce - FOCO_OESTE[0], cn - FOCO_OESTE[1])
    de_ = np.hypot(ce - FOCO_ESTE[0], cn - FOCO_ESTE[1])
    print("    %.2f ha  E%.0f N%.0f  | %4.0f m do foco OESTE | %4.0f m do foco ESTE"
          % (a, ce, cn, do_, de_))

print("\n  E o mesmo, no contrafactual mais duro: celulas que estiveram")
print("  SEMPRE acima da referencia menos 0,05 em TODAS as 8 cenas de 2017-2024")
print("  E cujo NDVI de 2024 estava acima de %.3f:" % (REFV["2024-07-22"] - 0.02))
duro = SAO_ANTES & (nd["2024-07-22"] > REFV["2024-07-22"] - 0.02)
print("    base: %.2f ha; em defice em 2026: %.2f ha"
      % (duro.sum() / 100.0, (duro & d26).sum() / 100.0))

print()
print("=" * 78)
print("C) FRENTE EM AVANCO OU NUCLEOS DIFUSOS?")
print("=" * 78)
print("  Para cada par de anos consecutivos: distancia das celulas NOVAS em")
print("  defice a celula em defice mais proxima do ano anterior.")
print("%-12s %10s %12s %12s %12s" %
      ("passagem", "novas ha", "mediana m", "p75 m", "%% a <=14 m"))
for a, b in zip(SERIE[:-1], SERIE[1:]):
    nova = M[b] & ~M[a]
    if nova.sum() == 0 or M[a].sum() == 0:
        continue
    dist = ndimage.distance_transform_edt(~M[a]) * 10.0
    v = dist[nova]
    print("%-12s %10.2f %12.1f %12.1f %11.0f%%"
          % ("%s->%s" % (a[2:7], b[2:7]), nova.sum() / 100.0,
             np.median(v), np.percentile(v, 75), 100.0 * (v <= 14.2).mean()))
    res.setdefault("frente", {})["%s->%s" % (a, b)] = dict(
        novas_ha=float(nova.sum() / 100.0), mediana_m=float(np.median(v)),
        pct_contiguo=float(100.0 * (v <= 14.2).mean()))

print()
print("=" * 78)
print("D) DATACAO CELULA A CELULA do defice de 2026")
print("=" * 78)
print("  Primeiro ano em que cada celula do defice de 2026 entrou em defice e")
print("  la ficou ate ao fim (sem voltar a estar sa).")
ordem = SERIE
conta = {}
for c in zip(*np.where(d26)):
    hist = [M[d][c] for d in ordem]
    ano = ordem[-1]
    for i in range(len(ordem)):
        if all(hist[i:]):
            ano = ordem[i]
            break
    conta[ano] = conta.get(ano, 0) + 1
print("  %-12s %10s %10s" % ("desde", "celulas", "ha"))
for d in ordem:
    if d in conta:
        print("  %-12s %10d %10.2f" % (d, conta[d], conta[d] / 100.0))
res["datacao_2026"] = {d: conta.get(d, 0) / 100.0 for d in ordem}

print("\n  O mesmo, so dentro de um raio de 120 m de cada foco:")
for nome, ctr in [("OESTE", FOCO_OESTE), ("ESTE", FOCO_ESTE)]:
    disco = ((E - ctr[0]) ** 2 + (N - ctr[1]) ** 2) <= 120.0 ** 2
    sub = {}
    for c in zip(*np.where(d26 & disco)):
        hist = [M[d][c] for d in ordem]
        ano = ordem[-1]
        for i in range(len(ordem)):
            if all(hist[i:]):
                ano = ordem[i]
                break
        sub[ano] = sub.get(ano, 0) + 1
    print("    foco %s (%.2f ha em defice em 2026): %s"
          % (nome, (d26 & disco).sum() / 100.0,
             "  ".join("%s:%.2f ha" % (d[:4], sub[d] / 100.0) for d in ordem if d in sub)))
    res.setdefault("datacao_focos", {})[nome] = {d: sub.get(d, 0) / 100.0 for d in ordem}

np.save(os.path.join(SAIDA, "c2_05_defice_2026.npy"), d26)
np.save(os.path.join(SAIDA, "c2_05_novo_m2.npy"), novo)
json.dump(res, open(os.path.join(SAIDA, "c2_05_manchas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_05_manchas.json")
