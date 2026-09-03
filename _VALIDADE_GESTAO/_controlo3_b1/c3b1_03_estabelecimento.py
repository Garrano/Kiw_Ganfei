# -*- coding: utf-8 -*-
"""Q2 e Q3 · quantos dos 29 «mantidos» estao em estabelecimento, e as 4 do B1
sao mesmo «de base continua»?

A triagem de descontinuidade (`reg01_triagem_descontinuidade.py`) exclui
unidades que CAIRAM (queda >= 0,25 e nivel posterior < 0,60). Nao tem criterio
nenhum para unidades que SUBIRAM. Uma parcela a encher e tao invalida como
comparador quanto uma a colapsar, e passa.

CRITERIO DE ESTABELECIMENTO, fixado antes de correr
---------------------------------------------------
Uma unidade esta em ESTABELECIMENTO na linha de base se satisfizer as tres:
    E1 · nivel de 2017 abaixo de 0,80 (kiwi maduro nesta cache le 0,83-0,90);
    E2 · declive OLS 2017-2024 acima de +0,010/ano;
    E3 · o nivel de 2023-24 esta pelo menos 0,05 acima do de 2017-18.
E marca-se tambem o caso mais fraco (duas das tres) como SUSPEITA.

E o outro lado da moeda, que a triagem tambem nao ve:
    D1 · queda >= 0,25 entre anos consecutivos DENTRO de 2017-2024 — mesmo que
         recupere depois. A triagem so exclui se o nivel POSTERIOR MEDIO ficar
         abaixo de 0,60, e a media inclui a recuperacao: uma unidade que cai
         0,43 e volta a subir passa.

VERIFICACAO DOS NUMEROS PUBLICADOS
-----------------------------------
«sobem em 67-78 % dos anos, declive +0,012 a +0,028/ano» — recalculado aqui.

O DEGRAU DE PLANALTO
--------------------
Estatistica que nao mistura a rampa com o acontecimento: nivel medio de 2025-26
menos nivel medio de 2023-24. Aplicada a todas as unidades, incluindo os focos.
"""
import json
import os

import numpy as np

import c3b1_00_comum as C

ANOS = C.ANOS
T = np.arange(10, dtype=float)
VALIDOS_B1 = [6476415, 6476420, 8845740, 6476425]

datas, V = C.matriz()
NIV = {u: C.anual(datas, V[u]) for u in V}
UNI = C.MANTIDOS + list(C.FOCOS)


def perfil(y):
    b = y[:8]
    ok = np.isfinite(b)
    decl = np.polyfit(T[:8][ok], b[ok], 1)[0] if ok.sum() >= 3 else np.nan
    d = np.diff(b[ok])
    sobe = 100 * np.mean(d > 0) if d.size else np.nan
    n1718 = np.nanmean(b[:2])
    n2324 = np.nanmean(b[6:8])
    queda = float(np.max(-d)) if d.size else np.nan
    e1 = np.isfinite(b[0]) and b[0] < 0.80
    e2 = np.isfinite(decl) and decl > 0.010
    e3 = np.isfinite(n2324 - n1718) and (n2324 - n1718) > 0.05
    return dict(n2017=float(b[0]), decl=float(decl), sobe=float(sobe),
                salto=float(n2324 - n1718), queda=queda,
                e=[bool(e1), bool(e2), bool(e3)], n=int(e1) + int(e2) + int(e3),
                planalto=float(np.nanmean(y[8:]) - np.nanmean(y[6:8])))


P = {u: perfil(NIV[u]) for u in UNI + C.CUL_B1}

print("=" * 116)
print("Q2 · OS 29 MANTIDOS DA REG-01 — quantos estao em estabelecimento?")
print("=" * 116)
print()
print("%-10s %7s %8s %8s %8s %8s %7s %6s  %s"
      % ("CUL_ID", "ENT", "2017", "decl/ano", "% sobe", "salto", "maior",
         "E1E2E3", "leitura"))
print("%-10s %7s %8s %8s %8s %8s %7s %6s"
      % ("", "", "", "17-24", "17-24", "23/24-17/18", "queda", ""))
est, susp = [], []
for u in sorted(C.MANTIDOS, key=lambda z: -P[z]["decl"]):
    p = P[u]
    lab = ("ESTABELECIMENTO" if p["n"] == 3 else
           ("suspeita (%d/3)" % p["n"] if p["n"] == 2 else ""))
    if p["n"] == 3:
        est.append(u)
    elif p["n"] == 2:
        susp.append(u)
    print("%-10d %7s %8.3f %+8.4f %7.0f %% %+8.3f %7.3f %6s  %s%s"
          % (u, C.ENT[u], p["n2017"], p["decl"], p["sobe"], p["salto"],
             p["queda"], "".join("X" if x else "." for x in p["e"]), lab,
             "   <-- B1" if u in C.CUL_B1 else ""))
print()
print("dos 29 mantidos: %d em ESTABELECIMENTO (3/3), %d suspeitos (2/3)"
      % (len(est), len(susp)))
print("  estabelecimento: %s" % ", ".join(str(x) for x in sorted(est)))
print("  suspeitos      : %s" % ", ".join(str(x) for x in sorted(susp)))
print("  dos 4 do B1 «validos», %d estao em estabelecimento e %d suspeitos"
      % (sum(1 for c in VALIDOS_B1 if c in est),
         sum(1 for c in VALIDOS_B1 if c in susp)))

print()
print("=" * 116)
print("Q3 · AS 4 «DE BASE CONTINUA» — e a queda que a triagem deixou passar")
print("=" * 116)
print()
print("%-10s %s  %s"
      % ("CUL_ID", " ".join("%6s" % a for a in ANOS), "maior queda em 2017-24"))
for c in C.CUL_B1:
    y = NIV[c]
    d = np.diff(y[:8])
    i = int(np.nanargmax(-d))
    print("%-10d %s  cai %.3f em %s -> %s%s"
          % (c, " ".join("%6.3f" % x if np.isfinite(x) else "     ." for x in y),
             -d[i], ANOS[i + 1],
             "acima do limiar 0,25" if -d[i] >= 0.25 else "abaixo do limiar",
             "   [dita VALIDA]" if c in VALIDOS_B1 else ""))
print()
print("porque e que passam — o `depois` da triagem e a MEDIA de todos os anos")
print("seguintes, e a recuperacao levanta-a acima de 0,60:")
for c in C.CUL_B1:
    y = NIV[c]
    d = np.diff(y[:8])
    i = int(np.nanargmax(-d))
    if -d[i] < 0.25:
        continue
    seg = y[i + 1:]
    seg = seg[np.isfinite(seg)]
    print("  %-9d cai em %s para %.3f; media de %s ate 2026 = %.3f  (limiar 0,60)"
          % (c, ANOS[i + 1], y[i + 1], ANOS[i + 1], seg.mean()))
    print("            nivel do ANO da queda so: %.3f  ->  %s"
          % (y[i + 1], "EXCLUIRIA" if y[i + 1] < 0.60 else "manteria"))

print()
print("=" * 116)
print("VERIFICACAO DOS NUMEROS PUBLICADOS PARA AS 4 (2017-2026, serie completa)")
print("=" * 116)
print()
for c in VALIDOS_B1:
    y = NIV[c]
    ok = np.isfinite(y)
    d = np.diff(y[ok])
    print("  %-9d sobe em %4.0f %% dos anos   ·   declive 2017-26 %+.4f/ano"
          % (c, 100 * np.mean(d > 0), np.polyfit(T[ok], y[ok], 1)[0]))
print()
print("  publicado: «sobem em 67-78 %% dos anos, declive +0,012 a +0,028/ano»")

print()
print("=" * 116)
print("O DEGRAU DE PLANALTO — 2025-26 menos 2023-24, para todos")
print("=" * 116)
print()
arr = sorted(((P[u]["planalto"], u) for u in C.MANTIDOS))
print("os 5 piores dos 29 mantidos:")
for v, u in arr[:5]:
    print("   %-10d %+.4f" % (u, v))
print("   ...")
print("os 3 melhores:")
for v, u in arr[-3:]:
    print("   %-10d %+.4f" % (u, v))
print()
for f in C.FOCOS:
    v = P[f]["planalto"]
    print("%-16s %+.4f   percentil entre os 29: %.0f %%"
          % (f, v, 100 * np.mean([a[0] <= v for a in arr])))
print()
for c in C.CUL_B1:
    print("B1 %-13d %+.4f%s" % (c, P[c]["planalto"],
                                "   [dita VALIDA]" if c in VALIDOS_B1 else ""))
print()
print("B1, mediana das 4 validas: %+.4f"
      % float(np.median([P[c]["planalto"] for c in VALIDOS_B1])))

json.dump(dict(perfil={str(u): P[u] for u in P},
               estabelecimento=[int(x) for x in est],
               suspeitos=[int(x) for x in susp],
               n_mantidos=len(C.MANTIDOS)),
          open(os.path.join(C.OUT, "c3b1_03_estabelecimento.json"), "w"), indent=1)
print()
print("escrito c3b1_03_estabelecimento.json")
