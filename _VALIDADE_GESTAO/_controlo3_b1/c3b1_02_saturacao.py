# -*- coding: utf-8 -*-
"""Q1 · a leitura de «estabelecimento» e real, ou e a retirada 14 ao contrario?

A taxonomia regista tres achados mortos pela MESMA curva — uma curva de
estabelecimento a saturar, lida como tendencia. Aqui a curva e lida COMO
estabelecimento. Tres testes, e o terceiro e o que decide.

TESTE A · uma curva de estabelecimento SATURA. Estas saturam?
  Ajusta-se, a 2017-2024 (so a linha de base, para nao usar o periodo em
  disputa), tres modelos:
      c   y = a                       (constante, 1 parametro)
      r   y = a + b t                 (recta, 2)
      s   y = A - B exp(-k t)         (saturante, 3)
  e compara-se por AICc. Uma curva de estabelecimento verdadeira prefere `s` e
  tem k grande (satura cedo). Uma rampa linear prefere `r`.

TESTE B · o declive da segunda metade contra o da primeira.
  Saturacao => declive(2021-24) << declive(2017-20). Sem pressupor forma.

TESTE C · O QUE ESTE TESTE FARIA SE A HIPOTESE FOSSE FALSA.
  Injecta-se um acontecimento REAL de -0,0854 em todas as cenas de 2025-26 de
  cada parcela do B1 e recalcula-se o mesmo degrau que o `b1_como_unidade.py`
  publica. Se o degrau continuar POSITIVO, entao «o B1 nao tem o degrau» nao e
  uma medicao do acontecimento: e uma medicao da rampa, e nao distingue.

TESTE D · o contrafactual proprio.
  Ajusta-se a saturante so a 2017-2024, extrapola-se para 2025 e 2026, e
  mede-se o residuo. E o unico teste que pergunta se o B1 caiu ABAIXO DE SI
  PROPRIO, em vez de perguntar se caiu abaixo da media dos seus proprios anos
  jovens.
"""
import json
import os

import numpy as np
from scipy.optimize import curve_fit

import c3b1_00_comum as C

ANOS = C.ANOS
T = np.arange(10, dtype=float)          # 2017 = 0
KBASE = 8                               # 2017..2024
FOCOS_VAL = {"foco OCIDENTAL": -0.0839, "foco ORIENTAL": -0.0869}
ALVO = float(np.mean(list(FOCOS_VAL.values())))
VALIDOS = [6476415, 6476420, 8845740, 6476425]

datas, V = C.matriz()
NIV = {u: C.anual(datas, V[u]) for u in V}


def aicc(res, k, n):
    rss = float(np.sum(res ** 2))
    if rss <= 0:
        rss = 1e-12
    a = n * np.log(rss / n) + 2 * k
    return a + (2 * k * (k + 1) / (n - k - 1) if n - k - 1 > 0 else np.inf)


def sat(t, A, B, k):
    return A - B * np.exp(-k * t)


def ajusta(y, t):
    """Devolve AICc de constante, recta, saturante + parametros da saturante."""
    ok = np.isfinite(y)
    yy, tt = y[ok], t[ok]
    n = yy.size
    out = {}
    out["c"] = aicc(yy - yy.mean(), 1, n)
    p = np.polyfit(tt, yy, 1)
    out["r"] = aicc(yy - np.polyval(p, tt), 2, n)
    out["decl"] = float(p[0])
    try:
        pp, _ = curve_fit(sat, tt, yy, p0=[max(yy), max(yy) - min(yy), .5],
                          bounds=([0, 0, .01], [1.5, 2, 5]), maxfev=40000)
        out["s"] = aicc(yy - sat(tt, *pp), 3, n)
        out["par"] = [float(x) for x in pp]
    except Exception as e:
        out["s"], out["par"] = np.inf, None
        out["erro"] = type(e).__name__
    return out


print("=" * 108)
print("TESTE A · ajuste a 2017-2024 — constante / recta / saturante, por AICc")
print("=" * 108)
print()
print("%-10s %8s %8s %8s  %-12s %8s %8s %8s"
      % ("unidade", "AICc c", "AICc r", "AICc s", "melhor", "A", "k",
         "% da subida ate 2024"))
A = {}
for c in C.CUL_B1:
    y = NIV[c][:KBASE]
    r = ajusta(y, T[:KBASE])
    A[c] = r
    best = min("crs", key=lambda z: r[z])
    fr = np.nan
    if r["par"]:
        Ah, Bh, kh = r["par"]
        # fraccao da subida total ja feita em 2024 (t = 7)
        fr = 100 * (1 - np.exp(-kh * 7))
    print("%-10d %8.2f %8.2f %8.2f  %-12s %8s %8s %14.0f %%"
          % (c, r["c"], r["r"], r["s"],
             {"c": "constante", "r": "RECTA", "s": "saturante"}[best],
             "%.3f" % r["par"][0] if r["par"] else "-",
             "%.3f" % r["par"][2] if r["par"] else "-", fr))

print()
print("=" * 108)
print("TESTE B · declive 2017-2020 contra declive 2021-2024 (saturar = travar)")
print("=" * 108)
print()
print("%-10s %12s %12s %10s   %s"
      % ("unidade", "decl 17-20", "decl 21-24", "razao", "leitura"))
for c in C.CUL_B1:
    y = NIV[c]
    d1 = np.polyfit(T[:4][np.isfinite(y[:4])], y[:4][np.isfinite(y[:4])], 1)[0]
    d2 = np.polyfit(T[4:8][np.isfinite(y[4:8])], y[4:8][np.isfinite(y[4:8])], 1)[0]
    raz = d2 / d1 if d1 != 0 else np.nan
    print("%-10d %+12.4f %+12.4f %10.2f   %s"
          % (c, d1, d2, raz,
             "trava (satura)" if d2 < .5 * d1 else
             ("acelera" if d2 > d1 else "abranda pouco")))

print()
print("=" * 108)
print("TESTE C · o que o degrau publicado faria se o B1 TIVESSE o acontecimento")
print("=" * 108)
print()
# reconstroi o degrau exactamente como b1_como_unidade.py: desvio a mediana dos
# 29 mantidos, media(pos) - media(pre), pos = data >= 2025
regm = [C.M[c] for c in C.MANTIDOS]
med = []
for i, d in enumerate(datas):
    vals = [V[c][i] for c in C.MANTIDOS]
    med.append(np.nanmedian(vals))
med = np.array(med)
pos = np.array([d >= "2025" for d in datas])


def degrau(serie, injecta=0.0):
    s = serie.copy()
    s[pos] += injecta
    dv = s - med
    a, b = dv[~pos], dv[pos]
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if a.size < 5 or b.size < 2:
        return np.nan
    return float(b.mean() - a.mean())


print("cenas: %d PRE, %d POS" % ((~pos).sum(), pos.sum()))
print()
print("%-10s %12s %14s %14s   %s"
      % ("unidade", "degrau real", "com -0,0854", "com -0,1700", "detecta?"))
INJ = {}
for c in C.CUL_B1:
    d0 = degrau(V[c])
    d1 = degrau(V[c], ALVO)
    d2 = degrau(V[c], 2 * ALVO)
    INJ[c] = [d0, d1, d2]
    print("%-10d %+12.4f %+14.4f %+14.4f   %s"
          % (c, d0, d1, d2,
             "NAO — continua positivo" if d1 > 0 else "sim, fica negativo"))

med_real = float(np.median([degrau(V[c]) for c in VALIDOS]))
med_inj = float(np.median([degrau(V[c], ALVO) for c in VALIDOS]))
print()
print("degrau MEDIANO das 4 validas, real         : %+.4f" % med_real)
print("degrau MEDIANO das 4 validas, com -0,0854  : %+.4f" % med_inj)
print("criterio publicado: sinal oposto ao dos focos -> «H1, e por margem larga»")
print("com o acontecimento INJECTADO o criterio diz : %s"
      % ("«H1, sinais opostos» — OUTRA VEZ" if med_inj > 0
         else "H0/nao decide"))

print()
print("=" * 108)
print("TESTE D · o contrafactual — ajuste a 2017-2024, extrapolado a 2025-26")
print("=" * 108)
print()
print("%-10s %9s %9s %9s %9s   %s"
      % ("unidade", "prev 2025", "obs 2025", "prev 2026", "obs 2026", "residuo medio"))
RES = {}
for c in C.CUL_B1:
    r = A[c]
    if not r["par"]:
        continue
    p25, p26 = sat(8., *r["par"]), sat(9., *r["par"])
    o25, o26 = NIV[c][8], NIV[c][9]
    rm = float(np.nanmean([o25 - p25, o26 - p26]))
    RES[c] = rm
    print("%-10d %9.3f %9.3f %9.3f %9.3f   %+.4f  %s"
          % (c, p25, o25, p26, o26, rm,
             "ABAIXO de si proprio" if rm < -0.02 else
             ("acima" if rm > 0.02 else "em cima da curva")))
print()
print("residuo mediano das 4 validas: %+.4f"
      % float(np.median([RES[c] for c in VALIDOS if c in RES])))
print("para comparacao, o degrau dos focos e %+.4f" % ALVO)

json.dump(dict(ajuste={str(c): {k: (None if not np.isfinite(v) else v)
                                for k, v in A[c].items() if k != "par"}
                       for c in C.CUL_B1},
               par={str(c): A[c]["par"] for c in C.CUL_B1},
               injeccao={str(c): INJ[c] for c in C.CUL_B1},
               degrau_mediano_real=med_real, degrau_mediano_injectado=med_inj,
               residuo_contrafactual={str(c): RES.get(c) for c in C.CUL_B1}),
          open(os.path.join(C.OUT, "c3b1_02_saturacao.json"), "w"), indent=1)
print()
print("escrito c3b1_02_saturacao.json")
