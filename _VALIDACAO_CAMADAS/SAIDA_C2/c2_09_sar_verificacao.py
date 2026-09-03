# -*- coding: utf-8 -*-
"""C2-09 — a pilha SAR reproduz a C1? E qual e a especificidade do cruzamento?

Duas coisas.

(a) REPRODUCAO DA C1 S15. A C1 afirma que o foco OESTE, contra o pomar inteiro,
    esta entre -0,30 e +0,48 dB de 2016-17 a 2024-25 e cai para -1,107 dB
    (orbita 125) e -0,774 dB (orbita 147) no Inverno de 2025-26. Se a minha
    pilha nao reproduzir isto, o cruzamento da C2 nao vale nada e ha paragem de
    linha. Usa-se a estatistica da C1: mediana, sobre as cenas do Inverno, da
    diferenca (unidade - pomar) calculada dentro de cada cena.

(b) ESPECIFICIDADE. Uma correlacao alta no Inverno de 2025-26 so prova alguma
    coisa se nao houver correlacao igual com um par de anos sem evento. Mede-se
    rho(X) - rho(X') Inverno a Inverno, e faz-se um teste de permutacao: quantas
    das 5000 reatribuicoes ao acaso das unidades dao um rho >= ao observado.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, NU21 = masc["pomar"], masc["saudavel"], masc["nu2021"] & masc["pomar"]
do, de = discos_dos_focos(POMAR)
nd = carrega_ndvi(TODAS)
E, N = centros_celulas()

pilha = np.load(os.path.join(SAIDA, "c2_07_sar_pilha.npy"))
meta = json.load(open(os.path.join(SAIDA, "c2_07_sar_cenas.json"), encoding="utf-8"))
inv = np.array([m["inverno"] for m in meta])
orb = np.array([m["orbita"] if m["orbita"] is not None else -1 for m in meta])
INVS = sorted(set(inv))
res = {}

print("=" * 78)
print("(a) REPRODUCAO DA C1 S15 — dVV contra o pomar inteiro, por Inverno")
print("=" * 78)
ALVO = {"OESTE disco r=90": do, "ESTE disco r=90": de,
        "referencia": REF, "lavrado2021": NU21}
for o in (125, 147):
    print("\n  --- orbita %d ---" % o)
    print("  %-9s %5s %18s %18s %14s %14s"
          % ("Inverno", "n", "OESTE-pomar", "ESTE-pomar", "ref-pomar", "lavr-pomar"))
    for w in INVS:
        sel = (inv == w) & (orb == o)
        if sel.sum() < 3:
            continue
        sub = pilha[sel]
        with np.errstate(invalid="ignore"):
            p = np.nanmean(sub[:, POMAR], axis=1)
            linha = []
            for nome, m in ALVO.items():
                linha.append(float(np.nanmedian(np.nanmean(sub[:, m], axis=1) - p)))
        print("  %-9s %5d %18.3f %18.3f %14.3f %14.3f"
              % (w, sel.sum(), *linha))
        res.setdefault("c1_s15", {}).setdefault(str(o), {})[w] = linha

print("\n  C1 S15 declara: OESTE entre -0,30 e +0,48 dB nos nove primeiros")
print("  Invernos, e -1,107 dB (orb 125) / -0,774 dB (orb 147) em 2025-26.")
for o in (125, 147):
    v = res["c1_s15"][str(o)]
    ant = [v[w][0] for w in INVS if w != "2025-26" and w in v]
    print("  medido, orbita %d: nove primeiros de %+.3f a %+.3f | 2025-26 %+.3f"
          % (o, min(ant), max(ant), v["2025-26"][0]))

print()
print("=" * 78)
print("(b) ESPECIFICIDADE DO CRUZAMENTO — quadricula de 60 m")
print("=" * 78)
LADO = 6
P = {}
for i0 in range(0, NL, LADO):
    for j0 in range(0, NC, LADO):
        m = np.zeros((NL, NC), bool)
        m[i0:i0 + LADO, j0:j0 + LADO] = True
        m &= POMAR
        if m.sum() >= 20:
            P["q%02d_%02d" % (i0, j0)] = m
ks = sorted(P)
print("  %d unidades" % len(ks))


def dn(m, a, b):
    return float(np.nanmean(nd[b][m]) - np.nanmean(nd[a][m])
                 - (np.nanmean(nd[b][POMAR]) - np.nanmean(nd[a][POMAR])))


def vv(m, w):
    sel = inv == w
    sub = pilha[sel]
    with np.errstate(invalid="ignore"):
        return float(np.nanmedian(np.nanmean(sub[:, m], axis=1)
                                  - np.nanmean(sub[:, POMAR], axis=1)))


PARES = [("evento 2024->2026", "2024-07-22", "2026-07-27"),
         ("placebo 2022->2024", "2022-07-31", "2024-07-22"),
         ("placebo 2020->2022", "2020-07-18", "2022-07-31"),
         ("placebo 2018->2020", "2018-08-31", "2020-07-18")]
X = {nome: np.array([dn(P[k], a, b) for k in ks]) for nome, a, b in PARES}
Y = {w: np.array([vv(P[k], w) for k in ks]) for w in INVS}

print("\n  %-10s %s" % ("Inverno", "".join("%22s" % n for n, _, _ in PARES)))
for w in INVS:
    linha = []
    for nome, _, _ in PARES:
        ok = ~(np.isnan(X[nome]) | np.isnan(Y[w]))
        r, p = stats.spearmanr(X[nome][ok], Y[w][ok])
        linha.append("rho%+.3f p%.4f" % (r, p))
        res.setdefault("especificidade", {}).setdefault(w, {})[nome] = \
            dict(rho=float(r), p=float(p))
    print("  %-10s %s" % (w, "".join("%22s" % x for x in linha)))

print("\n  Especificidade = rho(evento) - max(rho dos tres placebos):")
for w in INVS:
    e = res["especificidade"][w]["evento 2024->2026"]["rho"]
    pl = max(res["especificidade"][w][n]["rho"] for n, _, _ in PARES[1:])
    print("    %-10s  %+0.3f - %+0.3f = %+0.3f" % (w, e, pl, e - pl))
    res["especificidade"][w]["margem"] = float(e - pl)

print()
print("  --- teste de permutacao, Inverno de 2025-26 ---")
rng = np.random.default_rng(20260829)
xe, y = X["evento 2024->2026"], Y["2025-26"]
ok = ~(np.isnan(xe) | np.isnan(y))
robs = stats.spearmanr(xe[ok], y[ok])[0]
nulo = np.array([stats.spearmanr(rng.permutation(xe[ok]), y[ok])[0]
                 for _ in range(5000)])
print("    rho observado %+0.3f | p de permutacao (unilateral) = %.5f"
      % (robs, (nulo >= robs).mean()))
print("    maximo do nulo em 5000 permutacoes: %+0.3f" % nulo.max())
res["permutacao"] = dict(rho=float(robs), p=float((nulo >= robs).mean()),
                         max_nulo=float(nulo.max()), n=int(ok.sum()))

print("\n  --- e o mesmo teste tirando as unidades dos dois focos ---")
E2, N2 = centros_celulas()
longe = []
for k in ks:
    m = P[k]
    ce, cn = E2[m].mean(), N2[m].mean()
    if np.hypot(ce - FOCO_OESTE[0], cn - FOCO_OESTE[1]) > 130 and \
       np.hypot(ce - FOCO_ESTE[0], cn - FOCO_ESTE[1]) > 130:
        longe.append(ks.index(k))
longe = np.array(longe)
okl = ok.copy()
mask = np.zeros(len(ks), bool)
mask[longe] = True
sel = ok & mask
r, p = stats.spearmanr(xe[sel], y[sel])
print("    %d unidades a mais de 130 m dos dois focos: rho %+0.3f  p %.4f"
      % (sel.sum(), r, p))
print("    Se sobrevive aqui, o cruzamento nao e um efeito dos dois focos")
print("    a puxarem sozinhos a correlacao.")
res["sem_focos"] = dict(n=int(sel.sum()), rho=float(r), p=float(p))

json.dump(res, open(os.path.join(SAIDA, "c2_09_sar_verificacao.json"), "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito c2_09_sar_verificacao.json")
