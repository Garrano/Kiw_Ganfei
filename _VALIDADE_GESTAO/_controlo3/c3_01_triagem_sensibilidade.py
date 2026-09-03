# -*- coding: utf-8 -*-
"""Q1 e Q2 — a triagem e circular? e o limiar sobrevive?

Tres coisas, por esta ordem:

  A · REPRODUCAO. Corro a triagem tal como esta escrita e verifico que dou os
      mesmos 8 excluidos e os mesmos degraus. Sem isto nada do resto vale.

  B · SIMETRIA (Q1). A janela do criterio e 2017-2024. Aplico-o tambem com a
      janela ate 2026 e vejo quem sai. Se Ganfei sair, a janela e que a
      protegia; se nao sair, a proteccao vem dos limiares e nao da janela.

  C · SENSIBILIDADE (Q2). Grelha 4 quedas x 4 chaos (16 combinacoes) e, para
      cada uma, o lugar dos dois focos na distribuicao dos sobreviventes.
      Procura-se o ponto em que deixam de ser o pior e o segundo pior.

Nota tecnica que muda o desenho: no codigo original, `depois` e a media dos
niveis desde o ano da queda ATE 2026 — inclui portanto o periodo POS. Corro as
duas variantes (`depois` ate 2024, `depois` ate 2026) porque a segunda pode
excluir um bloco POR ELE TER caido em 2025-26, que e o proprio acontecimento
que se quer comparar.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import ANOS, VG, carregar, degraus, matriz, nivel_anual

FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]


def triar(N, blocos, queda_min, chao, ate="2024", depois_ate="2026"):
    """Devolve (fora, dentro, detalhe). `ate` = ultimo ano da janela da queda."""
    fora, dentro, det = [], [], {}
    for c in blocos:
        n = [N[c][a] for a in ANOS]
        pior, ondes = 0.0, None
        for i in range(len(ANOS) - 1):
            if ANOS[i + 1] > ate:
                break
            if np.isfinite(n[i]) and np.isfinite(n[i + 1]):
                d = n[i] - n[i + 1]
                if d > pior:
                    pior, ondes = d, ANOS[i + 1]
        dep = np.nan
        if ondes:
            k = ANOS.index(ondes)
            j = ANOS.index(depois_ate) + 1
            v = [x for x in n[k:j] if np.isfinite(x)]
            dep = float(np.mean(v)) if v else np.nan
        ex = pior >= queda_min and np.isfinite(dep) and dep < chao
        (fora if ex else dentro).append(c)
        det[c] = (pior, ondes, dep, ex)
    return fora, dentro, det


D = carregar()
datas, unid, V, PIX = matriz(D)
N = nivel_anual(datas, unid, V)
BLOCOS = [u for u in unid if u.isdigit()]
OFICIAL = json.load(open(os.path.join(VG, "reg01_triagem.json"), encoding="utf-8"))

print("=" * 100)
print("A · REPRODUCAO da triagem tal como esta escrita")
print("=" * 100)
fora, dentro, det = triar(N, BLOCOS, 0.25, 0.60)
esp = sorted(str(x) for x in OFICIAL["excluidos"])
print("  excluidos meus     : %s" % ", ".join(sorted(fora)))
print("  excluidos oficiais : %s" % ", ".join(esp))
print("  IGUAL" if sorted(fora) == esp else "  *** DIVERGE ***")
DEG = degraus(datas, unid, V, dentro, FOCOS + ["pomar inteiro"])
of = OFICIAL["degrau_refeito"]
dif = max(abs(DEG[k] - of[k]) for k in DEG if k in of)
print("  degraus: n=%d, |max dif| ao oficial = %.2e" % (len(DEG), dif))

arr = np.array(sorted(DEG[c] for c in dentro))
print()
for f in FOCOS:
    print("  %-16s %+0.4f   percentil %.0f %%   lugar %d de %d unidades"
          % (f, DEG[f], 100 * np.mean(arr <= DEG[f]),
             1 + sum(1 for x in arr if x < DEG[f]), len(arr) + 1))
print("  pior bloco sobrevivente: %.4f   margem ao pior foco = %.4f, ao melhor foco = %.4f"
      % (arr[0], min(DEG[f] for f in FOCOS) * -1 + arr[0] * 0 - 0,
         arr[0] - max(DEG[f] for f in FOCOS)))
print("  margem OCIDENTAL = %+0.4f   margem ORIENTAL = %+0.4f"
      % (arr[0] - DEG["foco OCIDENTAL"], arr[0] - DEG["foco ORIENTAL"]))

print()
print("=" * 100)
print("B · SIMETRIA — o mesmo criterio com a janela da queda ate 2026")
print("=" * 100)
for ate in ("2024", "2026"):
    fo, de, dt = triar(N, BLOCOS + FOCOS, 0.25, 0.60, ate=ate)
    print("  janela ate %s -> excluidos %d: %s" % (ate, len(fo), ", ".join(sorted(fo))))
    for f in FOCOS:
        p, o, dp, ex = dt[f]
        print("     %-16s maior queda %.3f em %s, nivel depois %.3f -> %s"
              % (f, p, o, dp, "EXCLUIDO" if ex else "fica"))

print()
print("  E se o criterio da queda fosse SO sobre a magnitude (sem o chao)?")
for ate in ("2024", "2026"):
    _, _, dt = triar(N, BLOCOS + FOCOS, 0.25, 9.9, ate=ate)
    q = sorted(((dt[c][0], c) for c in BLOCOS + FOCOS), reverse=True)
    print("     ate %s · maiores quedas anuais: %s"
          % (ate, "  ".join("%s %.2f" % (c, v) for v, c in q[:8])))

print()
print("=" * 100)
print("C · SENSIBILIDADE — grelha queda x chao, variante `depois` ate 2026 (a do codigo)")
print("=" * 100)
QS = [0.15, 0.20, 0.25, 0.30, 0.35]
CS = [0.55, 0.60, 0.65, 0.70]
res = {}
for depois_ate in ("2026", "2024"):
    print()
    print("  --- `depois` calculado ate %s ---" % depois_ate)
    print("  %-6s %s" % ("queda", " ".join("%-30s" % ("chao %.2f" % c) for c in CS)))
    for q in QS:
        cel = []
        for ch in CS:
            fo, de, dt = triar(N, BLOCOS, q, ch, depois_ate=depois_ate)
            dg = degraus(datas, unid, V, de, FOCOS)
            a = np.array(sorted(dg[c] for c in de))
            todos = sorted([dg[c] for c in de] + [dg[f] for f in FOCOS])
            lo = 1 + sum(1 for x in todos if x < dg["foco OCIDENTAL"])
            lr = 1 + sum(1 for x in todos if x < dg["foco ORIENTAL"])
            marg = a[0] - max(dg[f] for f in FOCOS)
            piores = sorted([lo, lr]) == [1, 2]
            res[(depois_ate, q, ch)] = dict(n_fora=len(fo), fora=sorted(fo),
                                            lug_oc=lo, lug_or=lr,
                                            deg_oc=dg["foco OCIDENTAL"],
                                            deg_or=dg["foco ORIENTAL"],
                                            pior_bloco=float(a[0]),
                                            margem=float(marg),
                                            piores=bool(piores))
            cel.append("%2d fora · lug %d/%d · m %+0.3f %s"
                       % (len(fo), lo, lr, marg, "OK" if piores else "**"))
        print("  %-6.2f %s" % (q, " ".join("%-30s" % x for x in cel)))
print()
print("  OK = os dois focos sao o 1.o e o 2.o. ** = deixaram de ser.")

inv = [k for k, v in res.items() if not v["piores"]]
print()
if inv:
    print("  COMBINACOES QUE INVERTEM (%d de %d):" % (len(inv), len(res)))
    for k in sorted(inv):
        v = res[k]
        print("     depois ate %s · queda %.2f · chao %.2f -> %d fora, lugares %d e %d, "
              "pior bloco %+0.4f" % (k[0], k[1], k[2], v["n_fora"], v["lug_oc"],
                                     v["lug_or"], v["pior_bloco"]))
else:
    print("  NENHUMA das %d combinacoes tira os focos do 1.o e 2.o lugar." % len(res))

json.dump({"%s|%.2f|%.2f" % k: v for k, v in res.items()},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "c3_01_sensibilidade.json"), "w"), indent=1)
print()
print("escrito c3_01_sensibilidade.json")
