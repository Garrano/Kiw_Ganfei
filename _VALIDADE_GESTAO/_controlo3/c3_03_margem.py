# -*- coding: utf-8 -*-
"""Q4 — a margem de 0,020 aguenta?

A afirmacao e «os focos sao o pior e o segundo pior», e ela nao depende do valor
do degrau: depende de UMA distancia, a que separa o foco OCIDENTAL (o menos mau
dos dois) do melhor bloco sobrevivente. Tudo o resto e decoracao.

Tres medidas:

  A · BOOTSTRAP SOBRE AS CENAS. Reamostram-se com reposicao as cenas do periodo
      PRE e as do POS, separadamente, preservando o n de cada — que e o
      bootstrap correcto para uma diferenca de medias. Em cada reamostra
      recalcula-se a mediana regional por cena e TODOS os degraus, e conta-se
      quantas vezes os focos continuam a ser o 1.o e o 2.o.

  B · JACKKNIFE POR ANO. Retira-se um ano de cada vez. Se a conclusao vier de um
      ano so, ve-se aqui.

  C · QUANTOS BLOCOS TERIAM DE MUDAR. A resposta exacta e um: basta um bloco
      descer 0,0201 para o foco OCIDENTAL deixar de ser o 2.o. Mede-se o erro
      padrao de bloco pelo bootstrap e ve-se quantos blocos tem um erro padrao
      dessa ordem.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import carregar, matriz

FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]
EXCL = {"6705427", "6705428", "6705429", "6705432", "6705442",
        "8845729", "8845731", "8845739"}

D = carregar()
datas, unid, V, PIX = matriz(D)
idx = {u: i for i, u in enumerate(unid)}
BLOCOS = [u for u in unid if u.isdigit()]
DENTRO = [c for c in BLOCOS if c not in EXCL]
ALVO = DENTRO + FOCOS
D_i = np.array([idx[u] for u in DENTRO])
A_i = np.array([idx[u] for u in ALVO])

# ------------------------------------------- cenas validas (o crivo do original)
val, per = [], []
for k, d in enumerate(datas):
    v = V[k, D_i]
    if np.isfinite(v).sum() >= 0.7 * len(D_i):
        val.append(k)
        per.append("pos" if d >= "2025" else "pre")
val = np.array(val)
per = np.array(per)
PRE = val[per == "pre"]
POS = val[per == "pos"]
print("cenas validas: %d   (pre %d · pos %d)" % (len(val), len(PRE), len(POS)))
import collections
print("cenas POS por ano: %s" % dict(collections.Counter(datas[k][:4] for k in POS)))
print("cenas PRE por ano: %s" % dict(collections.Counter(datas[k][:4] for k in PRE)))


def deg_de(ipre, ipos):
    """Degraus de todas as unidades-alvo, dadas listas de indices de cena."""
    out = {}
    for nome, ii in (("pre", ipre), ("pos", ipos)):
        acc = np.zeros(len(ALVO))
        cnt = np.zeros(len(ALVO))
        for k in ii:
            row = V[k]
            v = row[D_i]
            ok = np.isfinite(v)
            med = float(np.median(v[ok]))
            a = row[A_i]
            m = np.isfinite(a)
            acc[m] += a[m] - med
            cnt[m] += 1
        out[nome] = np.where(cnt >= 1, acc / np.maximum(cnt, 1), np.nan)
    return out["pos"] - out["pre"]


base = deg_de(PRE, POS)
b = {u: base[i] for i, u in enumerate(ALVO)}
ordem = sorted(ALVO, key=lambda u: b[u])
print()
print("base: %s" % "  ".join("%s %+0.4f" % (u, b[u]) for u in ordem[:4]))
MARG = b[ordem[2]] - b["foco OCIDENTAL"]
print("margem base (3.o lugar menos foco OCIDENTAL) = %+0.4f" % MARG)

# ------------------------------------------------------------------ A bootstrap
rng = np.random.default_rng(20260903)
NB = 2000
ok12 = 0
ok_top2_conjunto = 0
margens = []
degs = np.zeros((NB, len(ALVO)))
for t in range(NB):
    ip = rng.choice(PRE, size=len(PRE), replace=True)
    iq = rng.choice(POS, size=len(POS), replace=True)
    g = deg_de(ip, iq)
    degs[t] = g
    o = np.argsort(g)
    dois = {ALVO[o[0]], ALVO[o[1]]}
    if dois == set(FOCOS):
        ok12 += 1
    if ALVO[o[0]] in FOCOS or ALVO[o[1]] in FOCOS:
        ok_top2_conjunto += 1
    margens.append(g[ALVO.index(ALVO[o[2]])] - g[ALVO.index("foco OCIDENTAL")])

margens = np.array(margens)
print()
print("=" * 92)
print("A · BOOTSTRAP sobre as cenas, %d reamostras" % NB)
print("=" * 92)
print("  os DOIS focos sao o 1.o e o 2.o em %.1f %% das reamostras" % (100 * ok12 / NB))
print("  PELO MENOS UM foco esta no top-2 em %.1f %%" % (100 * ok_top2_conjunto / NB))
print("  margem (3.o menos foco OCIDENTAL): mediana %+0.4f · IC95 [%+0.4f, %+0.4f]"
      % (np.median(margens), np.percentile(margens, 2.5), np.percentile(margens, 97.5)))
print("  P(margem <= 0) = %.3f" % float(np.mean(margens <= 0)))
for f in FOCOS:
    i = ALVO.index(f)
    print("  %-16s degrau %+0.4f · IC95 [%+0.4f, %+0.4f] · ep %.4f"
          % (f, b[f], np.percentile(degs[:, i], 2.5), np.percentile(degs[:, i], 97.5),
             degs[:, i].std(ddof=1)))
for u in ordem[2:5]:
    i = ALVO.index(u)
    print("  %-16s degrau %+0.4f · IC95 [%+0.4f, %+0.4f] · ep %.4f"
          % (u, b[u], np.percentile(degs[:, i], 2.5), np.percentile(degs[:, i], 97.5),
             degs[:, i].std(ddof=1)))

# ------------------------------------------------------------------ B jackknife
print()
print("=" * 92)
print("B · JACKKNIFE POR ANO — retira-se um ano de cada vez")
print("=" * 92)
anos = sorted({datas[k][:4] for k in val})
print("  %-6s %6s %6s %11s %11s %11s %8s %s"
      % ("fora", "n_pre", "n_pos", "deg_oc", "deg_or", "3.o lugar", "margem", "1.o/2.o?"))
for a in anos:
    ip = np.array([k for k in PRE if datas[k][:4] != a])
    iq = np.array([k for k in POS if datas[k][:4] != a])
    if len(ip) < 5 or len(iq) < 2:
        print("  %-6s   impossivel (pre=%d pos=%d)" % (a, len(ip), len(iq)))
        continue
    g = deg_de(ip, iq)
    o = np.argsort(g)
    m = g[o[2]] - g[ALVO.index("foco OCIDENTAL")]
    print("  %-6s %6d %6d %+11.4f %+11.4f %11s %+8.4f %s"
          % (a, len(ip), len(iq), g[ALVO.index("foco OCIDENTAL")],
             g[ALVO.index("foco ORIENTAL")], ALVO[o[2]], m,
             "sim" if {ALVO[o[0]], ALVO[o[1]]} == set(FOCOS) else "NAO"))

# ------------------------------------------------------- C quantos blocos mudam
print()
print("=" * 92)
print("C · QUANTOS BLOCOS TERIAM DE MUDAR")
print("=" * 92)
print("  para o foco OCIDENTAL deixar de ser o 2.o basta UM bloco descer %.4f." % MARG)
ep = degs.std(axis=0, ddof=1)
n_maior = sum(1 for i, u in enumerate(ALVO) if u in DENTRO and ep[i] >= MARG)
print("  erro padrao de bloco (bootstrap de cenas): mediana %.4f · max %.4f"
      % (np.median([ep[ALVO.index(u)] for u in DENTRO]),
         max(ep[ALVO.index(u)] for u in DENTRO)))
print("  blocos cujo erro padrao SOZINHO chega a %.4f: %d de %d"
      % (MARG, n_maior, len(DENTRO)))
print("  os cinco blocos mais proximos do foco OCIDENTAL:")
for u in ordem[2:7]:
    i = ALVO.index(u)
    print("     %-10s %+0.4f  (a %.4f do foco OCIDENTAL, ep %.4f -> %.1f ep de distancia)"
          % (u, b[u], b[u] - b["foco OCIDENTAL"], ep[i],
             (b[u] - b["foco OCIDENTAL"]) / ep[i]))

json.dump(dict(margem_base=float(MARG),
               p_dois_focos_top2=float(ok12 / NB),
               margem_ic=[float(np.percentile(margens, 2.5)),
                          float(np.percentile(margens, 97.5))],
               p_margem_negativa=float(np.mean(margens <= 0)),
               ep={u: float(ep[i]) for i, u in enumerate(ALVO)},
               degrau={u: float(b[u]) for u in ALVO}),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "c3_03_margem.json"), "w"), indent=1)
print()
print("escrito c3_03_margem.json")
