# -*- coding: utf-8 -*-
"""Q2 (fecho) e Q5 · o que o estabelecimento entre os 29 faz ao A3.

Duas coisas, e sao diferentes:

A · REG-01 REFEITA sem as unidades em estabelecimento, pelo MEU rastreio
    (o Controlo 3 anterior fez o mesmo com outro rastreio, 13 unidades; este
    tem 10, e a sobreposicao nao e total. Duas regras, dois resultados: e
    isso que se relata).

B · A JANELA DE BASE COMO ESCOLHA DE DESENHO. O degrau publicado usa
    media(2025-26) menos media(2017-2024). Se um terco das unidades esta a
    encher durante 2017-2024, a media da linha de base de cada uma e mais
    baixa do que o seu nivel em 2024, e o degrau que se lhe mede e mais
    positivo do que o acontecimento. Encurtar a janela de base remove a rampa
    sem remover o acontecimento — e um teste, nao uma preferencia.

    Janelas: 2017-24 (a publicada) · 2019-24 · 2021-24 · 2023-24.
    Estatistica: media do desvio e mediana do desvio.
    Oito corridas. Relata-se a DISTRIBUICAO dos lugares dos dois focos, nao a
    corrida preferida (Botvinik-Nezer 2020; a regra da CLAUDE.md).
"""
import json
import os

import numpy as np

import c3b1_00_comum as C

EST = json.load(open(os.path.join(C.OUT, "c3b1_03_estabelecimento.json"),
                     encoding="utf-8"))
ESTAB = [int(x) for x in EST["estabelecimento"]]
SUSP = [int(x) for x in EST["suspeitos"]]

datas, V = C.matriz()
ano = np.array([d[:4] for d in datas])
pos = ano >= "2025"


def corrida(conj, jan_ini, stat=np.mean, alvos=None):
    """Degrau de cada unidade contra a mediana de `conj`, com base >= jan_ini."""
    med = np.array([np.nanmedian([V[c][i] for c in conj])
                    for i in range(len(datas))])
    pre = (ano >= jan_ini) & (ano <= "2024")
    out = {}
    for u in list(conj) + list(alvos or []):
        dv = V[u] - med
        a, b = dv[pre], dv[pos]
        a, b = a[np.isfinite(a)], b[np.isfinite(b)]
        if a.size >= 5 and b.size >= 2:
            out[u] = float(stat(b) - stat(a))
    return out


FOC = list(C.FOCOS)
print("=" * 104)
print("A · REG-01 REFEITA COM E SEM AS UNIDADES EM ESTABELECIMENTO")
print("=" * 104)
print()
print("rastreio deste Controlo 3: %d em estabelecimento (3/3) + %d suspeita (2/3)"
      % (len(ESTAB), len(SUSP)))
print()
print("%-40s %4s %11s %11s %9s %8s"
      % ("conjunto de comparacao", "n", "degrau OC", "degrau OR", "lugares",
         "margem"))
LIN = []
for nome, conj in (("os 29 da triagem oficial", C.MANTIDOS),
                   ("sem as %d em estabelecimento" % len(ESTAB),
                    [c for c in C.MANTIDOS if c not in ESTAB]),
                   ("sem estabelecimento e sem a suspeita",
                    [c for c in C.MANTIDOS if c not in ESTAB + SUSP]),
                   ("sem as 4 parcelas do B1",
                    [c for c in C.MANTIDOS if c not in C.CUL_B1]),
                   ("sem estabelecimento e sem o dono 472062",
                    [c for c in C.MANTIDOS
                     if c not in ESTAB + SUSP and C.ENT[c] != 472062])):
    D = corrida(conj, "2017", np.mean, FOC)
    ordem = sorted(D, key=lambda z: D[z])
    lug = [ordem.index(f) + 1 for f in FOC]
    outros = [D[c] for c in conj if c in D]
    marg = min(outros) - max(D[f] for f in FOC)
    LIN.append((nome, len(conj), D[FOC[0]], D[FOC[1]], lug, marg))
    print("%-40s %4d %+11.4f %+11.4f %5s e %-3s %+8.4f"
          % (nome, len(conj), D[FOC[0]], D[FOC[1]], lug[0], lug[1], marg))
print()
print("margem = melhor bloco sobrevivente menos o menos mau dos dois focos;")
print("positiva quer dizer que os focos sao o 1.o e o 2.o.")

print()
print("=" * 104)
print("B · A JANELA DE BASE — oito corridas, e a distribuicao dos lugares")
print("=" * 104)
print()
print("%-10s %-8s %11s %11s %9s %9s %8s"
      % ("base", "estat.", "degrau OC", "degrau OR", "lugar OC", "lugar OR",
         "margem"))
DIST = []
for jan in ("2017", "2019", "2021", "2023"):
    for sn, st in (("media", np.mean), ("mediana", np.median)):
        D = corrida(C.MANTIDOS, jan, st, FOC)
        ordem = sorted(D, key=lambda z: D[z])
        lug = [ordem.index(f) + 1 for f in FOC]
        outros = [D[c] for c in C.MANTIDOS if c in D]
        marg = min(outros) - max(D[f] for f in FOC)
        DIST.append((jan, sn, D[FOC[0]], D[FOC[1]], lug[0], lug[1], marg))
        print("%-10s %-8s %+11.4f %+11.4f %9d %9d %+8.4f"
              % (jan + "-24", sn, D[FOC[0]], D[FOC[1]], lug[0], lug[1], marg))
n12 = sum(1 for x in DIST if sorted([x[4], x[5]]) == [1, 2])
print()
print("os dois focos sao o 1.o e o 2.o em %d das %d corridas." % (n12, len(DIST)))
print("lugar do foco OCIDENTAL: %s" % sorted(x[4] for x in DIST))
print("lugar do foco ORIENTAL : %s" % sorted(x[5] for x in DIST))
print("margem: min %+.4f  ·  mediana %+.4f  ·  max %+.4f"
      % (min(x[6] for x in DIST), float(np.median([x[6] for x in DIST])),
         max(x[6] for x in DIST)))
print()
print("quem bate o foco ORIENTAL quando ele perde o 2.o lugar:")
for jan in ("2017", "2019", "2021", "2023"):
    D = corrida(C.MANTIDOS, jan, np.mean, FOC)
    ordem = sorted(D, key=lambda z: D[z])
    piores = [u for u in ordem[:5]]
    print("  base %s-24: %s"
          % (jan, "  ".join("%s %+.4f" % (u if isinstance(u, str) else str(u),
                                          D[u]) for u in piores)))

json.dump(dict(estabelecimento=ESTAB, suspeitos=SUSP,
               conjuntos=[[a, b, c_, d_, e_, f_] for a, b, c_, d_, e_, f_ in LIN],
               janelas=[[a, b, c_, d_, e_, f_, g_]
                        for a, b, c_, d_, e_, f_, g_ in DIST]),
          open(os.path.join(C.OUT, "c3b1_05_multiverso.json"), "w"), indent=1)
print()
print("escrito c3b1_05_multiverso.json")
