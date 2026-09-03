# -*- coding: utf-8 -*-
"""Q2 continuacao — ONDE esta o penhasco.

A grelha 0,15-0,35 x 0,55-0,70 nao inverte nada. Isso nao chega para dizer que o
limiar e robusto: pode simplesmente estar longe do sitio onde ele importa.
Aqui procura-se o sitio.

Duas frentes:
  · a queda, ate 0,50 — os cinco caem 0,40 a 0,45 num ano, portanto ha um
    penhasco entre 0,40 e 0,45 onde eles deixam de ser apanhados;
  · o chao, de 0,35 a 0,70 — o nivel deles depois da queda e 0,45 a 0,51,
    portanto ha outro penhasco por volta de 0,50.

E, para referencia, o caso SEM TRIAGEM NENHUMA.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import ANOS, carregar, degraus, matriz, nivel_anual
from c3_01_triagem_sensibilidade import triar

FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]
D = carregar()
datas, unid, V, PIX = matriz(D)
N = nivel_anual(datas, unid, V)
BLOCOS = [u for u in unid if u.isdigit()]
CINCO = ["6705427", "6705428", "6705429", "6705432", "6705442"]


def lugar(de):
    dg = degraus(datas, unid, V, de, FOCOS)
    todos = sorted([dg[c] for c in de] + [dg[f] for f in FOCOS])
    lo = 1 + sum(1 for x in todos if x < dg["foco OCIDENTAL"])
    lr = 1 + sum(1 for x in todos if x < dg["foco ORIENTAL"])
    pior = min(dg[c] for c in de)
    return lo, lr, dg["foco OCIDENTAL"], dg["foco ORIENTAL"], pior


print("=" * 96)
print("A · o nivel dos cinco depois da queda, e a queda de cada um")
print("=" * 96)
_, _, det = triar(N, BLOCOS, 0.0, 9.9)
for c in CINCO + ["8845729", "8845731", "8845739"]:
    p, o, dp, _ = det[c]
    print("  %-10s queda %.3f em %s · nivel medio depois (ate 2026) %.3f" % (c, p, o, dp))

print()
print("=" * 96)
print("B · PENHASCO na queda (chao fixo em 0,60)")
print("=" * 96)
print("  %-7s %6s %6s %5s %5s %11s %11s %11s" % ("queda", "n_fora", "cinco", "l_oc",
                                                 "l_or", "deg_oc", "deg_or", "pior_bl"))
for q in [0.20, 0.30, 0.35, 0.38, 0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.50]:
    fo, de, _ = triar(N, BLOCOS, q, 0.60)
    lo, lr, doc, dor, pior = lugar(de)
    print("  %-7.2f %6d %6d %5d %5d %+11.4f %+11.4f %+11.4f   %s"
          % (q, len(fo), sum(1 for c in CINCO if c in fo), lo, lr, doc, dor, pior,
             "" if sorted([lo, lr]) == [1, 2] else "<== JA NAO SAO 1.o E 2.o"))

print()
print("=" * 96)
print("C · PENHASCO no chao (queda fixa em 0,25)")
print("=" * 96)
print("  %-7s %6s %6s %5s %5s %11s %11s %11s" % ("chao", "n_fora", "cinco", "l_oc",
                                                 "l_or", "deg_oc", "deg_or", "pior_bl"))
for ch in [0.35, 0.40, 0.44, 0.46, 0.48, 0.50, 0.52, 0.55, 0.60, 0.70, 0.80]:
    fo, de, _ = triar(N, BLOCOS, 0.25, ch)
    lo, lr, doc, dor, pior = lugar(de)
    print("  %-7.2f %6d %6d %5d %5d %+11.4f %+11.4f %+11.4f   %s"
          % (ch, len(fo), sum(1 for c in CINCO if c in fo), lo, lr, doc, dor, pior,
             "" if sorted([lo, lr]) == [1, 2] else "<== JA NAO SAO 1.o E 2.o"))

print()
print("=" * 96)
print("D · SEM TRIAGEM NENHUMA — a REG-01 antes da correccao")
print("=" * 96)
lo, lr, doc, dor, pior = lugar(BLOCOS)
print("  37 blocos · focos em lugar %d e %d de 39 · degrau %+0.4f e %+0.4f · pior bloco %+0.4f"
      % (lo, lr, doc, dor, pior))

print()
print("=" * 96)
print("E · so os CINCO fora (sem os tres do 472062) — os tres mudam alguma coisa?")
print("=" * 96)
de = [c for c in BLOCOS if c not in CINCO]
lo, lr, doc, dor, pior = lugar(de)
print("  32 blocos · lugares %d e %d de 34 · degrau %+0.4f e %+0.4f · pior bloco %+0.4f"
      % (lo, lr, doc, dor, pior))
print("  margem = %+0.4f (com os tres fora era +0,0200)" % (pior - doc))

print()
print("F · so os TRES fora (os cinco ficam)")
de = [c for c in BLOCOS if c not in ("8845729", "8845731", "8845739")]
lo, lr, doc, dor, pior = lugar(de)
print("  34 blocos · lugares %d e %d de 36 · degrau %+0.4f e %+0.4f · pior bloco %+0.4f"
      % (lo, lr, doc, dor, pior))
