# -*- coding: utf-8 -*-
"""Q4 (continuacao) e Q5 — o bootstrap certo, e a mediana com dois donos.

PORQUE O BOOTSTRAP DE CENAS NAO CHEGA
--------------------------------------
Reamostrar cenas trata cada cena como uma observacao independente. Nao sao: seis
cenas em treze dias de Agosto de 2025 medem o mesmo estado do copado. O periodo
POS tem 29 cenas mas so DOIS anos. Um bootstrap que reamostra cenas divide por
sqrt(29) uma coisa que so tem 2 graus de liberdade.

Aqui reamostram-se ANOS com reposicao dentro de cada periodo (8 anos no PRE, 2
no POS), que e o bootstrap de blocos correcto para dados agrupados por epoca.

Q5 · A MEDIANA COM DOIS DONOS
------------------------------
Dos 29 blocos sobreviventes, 15 sao do ENT 297313 e 11 do 472062 — o proprio dono
do pomar em estudo. Uma mediana por bloco e, na pratica, uma mediana de dois
donos com pesos 15 e 11. Recalcula-se com a mediana PONDERADA POR DONO: primeiro
a mediana dentro de cada dono, depois a mediana dessas medianas — cada dono
conta uma vez.

E corre-se ainda a versao que interessa mais: a mediana SEM o dono do pomar
(472062), para o controlo deixar de conter o proprio sujeito.
"""
import collections
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import VG, carregar, matriz

FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]
EXCL = {"6705427", "6705428", "6705429", "6705432", "6705442",
        "8845729", "8845731", "8845739"}

D = carregar()
datas, unid, V, PIX = matriz(D)
idx = {u: i for i, u in enumerate(unid)}
ENT = {str(k): v for k, v in D["ENT"].items()}
BLOCOS = [u for u in unid if u.isdigit()]
DENTRO = [c for c in BLOCOS if c not in EXCL]
ALVO = DENTRO + FOCOS
D_i = np.array([idx[u] for u in DENTRO])
A_i = np.array([idx[u] for u in ALVO])

print("donos dos %d blocos sobreviventes: %s"
      % (len(DENTRO), dict(collections.Counter(ENT[c] for c in DENTRO))))

val = [k for k, d in enumerate(datas)
       if np.isfinite(V[k, D_i]).sum() >= 0.7 * len(D_i)]
ANOP = collections.defaultdict(list)
for k in val:
    ANOP[datas[k][:4]].append(k)
APRE = sorted(a for a in ANOP if a < "2025")
APOS = sorted(a for a in ANOP if a >= "2025")


def med_por_bloco(row, ok):
    return float(np.median(row[D_i][ok]))


def med_por_dono(row, ok):
    """mediana das medianas de cada dono — cada dono conta uma vez."""
    porduno = collections.defaultdict(list)
    for j, c in enumerate(DENTRO):
        if ok[j]:
            porduno[ENT[c]].append(row[D_i][j])
    if not porduno:
        return np.nan
    return float(np.median([np.median(v) for v in porduno.values()]))


def med_sem_dono_do_pomar(row, ok):
    v = [row[D_i][j] for j, c in enumerate(DENTRO)
         if ok[j] and str(ENT[c]) != "472062"]
    return float(np.median(v)) if v else np.nan


def degraus(cenas_pre, cenas_pos, medf):
    acc = {p: np.zeros(len(ALVO)) for p in ("pre", "pos")}
    cnt = {p: np.zeros(len(ALVO)) for p in ("pre", "pos")}
    for p, ii in (("pre", cenas_pre), ("pos", cenas_pos)):
        for k in ii:
            row = V[k]
            ok = np.isfinite(row[D_i])
            med = medf(row, ok)
            if not np.isfinite(med):
                continue
            a = row[A_i]
            m = np.isfinite(a)
            acc[p][m] += a[m] - med
            cnt[p][m] += 1
    g = acc["pos"] / np.maximum(cnt["pos"], 1) - acc["pre"] / np.maximum(cnt["pre"], 1)
    return {u: float(g[i]) for i, u in enumerate(ALVO)}


CPRE = [k for a in APRE for k in ANOP[a]]
CPOS = [k for a in APOS for k in ANOP[a]]

print()
print("=" * 96)
print("Q5 · A MEDIANA REGIONAL, tres definicoes")
print("=" * 96)
tab = {}
for nome, f in (("por bloco (a usada)", med_por_bloco),
                ("ponderada por dono", med_por_dono),
                ("sem o dono do pomar (472062)", med_sem_dono_do_pomar)):
    g = degraus(CPRE, CPOS, f)
    ordem = sorted(ALVO, key=lambda u: g[u])
    lo = 1 + sum(1 for u in ALVO if g[u] < g["foco OCIDENTAL"])
    lr = 1 + sum(1 for u in ALVO if g[u] < g["foco ORIENTAL"])
    marg = g[ordem[2]] - g["foco OCIDENTAL"]
    tab[nome] = dict(deg_oc=g["foco OCIDENTAL"], deg_or=g["foco ORIENTAL"],
                     lug=(lo, lr), terceiro=ordem[2], margem=marg,
                     top2=sorted([lo, lr]) == [1, 2])
    print("  %-32s oc %+0.4f  or %+0.4f  lugares %d e %d  3.o=%s  margem %+0.4f  %s"
          % (nome, g["foco OCIDENTAL"], g["foco ORIENTAL"], lo, lr, ordem[2], marg,
             "1.o e 2.o" if sorted([lo, lr]) == [1, 2] else "*** NAO SAO 1.o E 2.o ***"))

print()
print("  quantos donos INDEPENDENTES ha, afinal:")
c = collections.Counter(ENT[x] for x in DENTRO)
for e, n in c.most_common():
    print("     ENT %-8s %2d blocos%s" % (e, n, "   <-- o dono do pomar em estudo"
                                          if str(e) == "472062" else ""))
print("     -> a mediana por bloco e, a 90 %%, uma mediana de DOIS donos.")

# ------------------------------------------------------- bootstrap de ANOS
print()
print("=" * 96)
print("Q4 (bis) · BOOTSTRAP DE ANOS — 8 anos no PRE, 2 no POS, com reposicao")
print("=" * 96)
rng = np.random.default_rng(20260903)
NB = 2000
ok12 = 0
margens = []
for t in range(NB):
    ap = rng.choice(APRE, size=len(APRE), replace=True)
    aq = rng.choice(APOS, size=len(APOS), replace=True)
    cp = [k for a in ap for k in ANOP[a]]
    cq = [k for a in aq for k in ANOP[a]]
    g = degraus(cp, cq, med_por_bloco)
    o = sorted(ALVO, key=lambda u: g[u])
    if {o[0], o[1]} == set(FOCOS):
        ok12 += 1
    margens.append(g[o[2]] - g["foco OCIDENTAL"])
margens = np.array(margens)
print("  os DOIS focos sao o 1.o e o 2.o em %.1f %% das reamostras de ANOS" % (100 * ok12 / NB))
print("  margem: mediana %+0.4f · IC95 [%+0.4f, %+0.4f] · P(<=0) = %.3f"
      % (np.median(margens), np.percentile(margens, 2.5),
         np.percentile(margens, 97.5), float(np.mean(margens <= 0))))
print()
print("  NOTA: com 2 anos no POS, a reamostra e {2025,2025}, {2025,2026} ou")
print("  {2026,2026} com probabilidades 1/4, 1/2, 1/4. O numero acima e, no fundo,")
print("  a media desses tres cenarios — e o cenario {2025,2025} e o do jackknife")
print("  que ja tinha falhado.")

json.dump(dict(mediana=tab, p_top2_bootstrap_anos=float(ok12 / NB),
               margem_ic_anos=[float(np.percentile(margens, 2.5)),
                               float(np.percentile(margens, 97.5))],
               p_margem_negativa_anos=float(np.mean(margens <= 0)),
               donos=dict(c)),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "c3_04_anos_e_donos.json"), "w"), indent=1)
print()
print("escrito c3_04_anos_e_donos.json")
