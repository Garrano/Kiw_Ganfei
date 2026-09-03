# -*- coding: utf-8 -*-
"""O que a triagem NAO procura: pomares JOVENS entre os 29 sobreviventes.

A ortofoto mostrou que 8845729, 8845731 e 8845739 eram campo aberto em 2012,
2018 e 2021 e tinham pergola nova em 2025. Nao sao «replantacao»: sao PLANTACAO
NOVA. A triagem apanhou-os por acaso — porque a instalacao deixou uma queda de
um ano na serie.

Um pomar plantado em 2018 e que cresce em linha recta NAO tem queda nenhuma, e
passa a triagem inteira. E um pomar em crescimento tem degrau POSITIVO grande,
sobe a mediana regional no periodo POS e empurra o degrau de toda a gente —
incluindo o dos focos — para baixo. O enviesamento vai NA DIRECCAO DA CONCLUSAO.

Duas medidas:
  A · rastreio pela serie: nivel de 2017, declive 2017-2024, e a fraccao sem
      coberto de 2021 na ortofoto onde ela existe (blocos do 472062, medidos em
      `c3_08`, e blocos do 297313, medidos em `orto_297313_fraccao.json`);
  B · a REG-01 refeita SEM os blocos que o rastreio marca como jovens.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import ANOS, VG, carregar, degraus, matriz, nivel_anual

OUT = os.path.dirname(os.path.abspath(__file__))
FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]
EXCL = {"6705427", "6705428", "6705429", "6705432", "6705442",
        "8845729", "8845731", "8845739"}

D = carregar()
datas, unid, V, PIX = matriz(D)
N = nivel_anual(datas, unid, V)
ENT = {str(k): v for k, v in D["ENT"].items()}
HA = {str(k): v for k, v in D["HA"].items()}
DENTRO = [u for u in unid if u.isdigit() and u not in EXCL]

# fraccao sem coberto de 2021, onde existe
F21 = {}
p = os.path.join(OUT, "c3_08_orto_tres.json")
if os.path.exists(p):
    for c, v in json.load(open(p))["fraccao"]["2021"]["blocos"].items():
        F21[str(c)] = v
p = os.path.join(VG, "orto_297313_fraccao.json")
if os.path.exists(p):
    for c, v in json.load(open(p))["2021"]["blocos"].items():
        F21[str(c)] = v

DEG = degraus(datas, unid, V, DENTRO, FOCOS)
print("=" * 104)
print("A · RASTREIO — quem parece pomar jovem entre os 29 sobreviventes")
print("=" * 104)
print()
print("%-10s %-8s %6s %7s %7s %9s %8s %9s" % ("CUL_ID", "ENT", "ha", "n2017",
                                              "n2024", "decl/ano", "f2021", "degrau"))
lin = []
for c in DENTRO:
    n = np.array([N[c][a] for a in ANOS[:8]], float)  # 2017-2024
    k = np.isfinite(n)
    dec = np.polyfit(np.arange(8)[k], n[k], 1)[0] if k.sum() >= 4 else np.nan
    lin.append((c, N[c]["2017"], N[c]["2024"], dec, F21.get(c, np.nan), DEG[c]))
for c, a17, a24, dec, f21, dg in sorted(lin, key=lambda z: -z[3]):
    marca = ""
    if (np.isfinite(f21) and f21 > 20) or dec > 0.010 or a17 < 0.70:
        marca = "  <== suspeito"
    print("%-10s %-8s %6.2f %7.3f %7.3f %+9.4f %8s %+9.4f%s"
          % (c, ENT[c], HA[c], a17, a24, dec,
             "%.1f%%" % f21 if np.isfinite(f21) else "  -  ", dg, marca))

SUSP = [c for c, a17, a24, dec, f21, dg in lin
        if (np.isfinite(f21) and f21 > 20) or dec > 0.010 or a17 < 0.70]
print()
print("suspeitos: %d — %s" % (len(SUSP), ", ".join(SUSP)))
print("(criterio: fraccao sem coberto de 2021 > 20 %%, OU declive 2017-24 > +0,010/ano,")
print(" OU nivel de 2017 abaixo de 0,70 — um pomar maduro de kiwi le 0,80 a 0,90)")

print()
print("=" * 104)
print("B · A REG-01 refeita SEM os suspeitos")
print("=" * 104)


def julga(de, etiqueta):
    g = degraus(datas, unid, V, de, FOCOS)
    todos = sorted([g[c] for c in de] + [g[f] for f in FOCOS])
    lo = 1 + sum(1 for x in todos if x < g["foco OCIDENTAL"])
    lr = 1 + sum(1 for x in todos if x < g["foco ORIENTAL"])
    ter = todos[2]
    print("  %-42s n=%2d · oc %+0.4f (lugar %d) · or %+0.4f (lugar %d) · "
          "3.o %+0.4f · margem %+0.4f %s"
          % (etiqueta, len(de), g["foco OCIDENTAL"], lo, g["foco ORIENTAL"], lr,
             ter, ter - g["foco OCIDENTAL"],
             "" if sorted([lo, lr]) == [1, 2] else " <== NAO SAO 1.o E 2.o"))
    return g


julga(DENTRO, "os 29 da triagem oficial")
julga([c for c in DENTRO if c not in SUSP], "sem os suspeitos de pomar jovem")
julga([c for c in DENTRO if str(ENT[c]) != "472062"],
      "sem NENHUM bloco do dono do pomar (472062)")
julga([c for c in DENTRO if str(ENT[c]) != "472062" and c not in SUSP],
      "sem o dono do pomar E sem os suspeitos")
maduros = [c for c in DENTRO if c not in SUSP and N[c]["2017"] >= 0.80]
julga(maduros, "so blocos com nivel 2017 >= 0,80")
