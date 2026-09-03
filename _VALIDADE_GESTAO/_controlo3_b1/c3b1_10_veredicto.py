# -*- coding: utf-8 -*-
"""O veredicto do B1 refeito com a composicao corrigida pela ortofoto, e o
PISO DE DETECCAO do criterio publicado.

A ortofoto (c3b1_09) diz, com instrumento independente:
  · 6476415 · 6476420 · 8845740 — campo aberto em 2007, plantadas por volta de
    2009-2010, a encher ate hoje. ESTABELECIMENTO CONFIRMADO.
  · 6476425 — mato/arvores ate 2012, CHAO NU em 2018 (98,3 %), pergola nova em
    2021, rede em 2025. **Nao tem linha de base de kiwi nenhuma.** O nivel de
    0,890 em 2017 nao e kiwi maduro: e vegetacao lenhosa. Sai pela mesma regra
    que tirou 8845729 e 8845739.
  · 8845729 · 8845739 — ja excluidas.

Restam TRES parcelas, todas em estabelecimento. Refaz-se o veredicto.

E mede-se o PISO DE DETECCAO: qual e o acontecimento minimo que o criterio
publicado (`razao > 2/3` com o mesmo sinal) conseguiria declarar. Se o piso for
maior do que o acontecimento que se procura, o teste nao tem potencia e o
veredicto nao e sobre o B1: e sobre o instrumento.
"""
import json
import os

import numpy as np
from scipy.optimize import curve_fit

import c3b1_00_comum as C

FOCOS = {"foco OCIDENTAL": -0.0839, "foco ORIENTAL": -0.0869}
ALVO = float(np.mean(list(FOCOS.values())))
TRES = [6476415, 6476420, 8845740]
QUATRO = [6476415, 6476420, 8845740, 6476425]

datas, V = C.matriz()
med = np.array([np.nanmedian([V[c][i] for c in C.MANTIDOS])
                for i in range(len(datas))])
pos = np.array([d >= "2025" for d in datas])


def degrau(c, inj=0.0):
    s = V[c].copy()
    s[pos] += inj
    dv = s - med
    a, b = dv[~pos], dv[pos]
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    return float(b.mean() - a.mean())


def criterio(conj, inj=0.0):
    m = float(np.median([degrau(c, inj) for c in conj]))
    mesmo = (m < 0) == (ALVO < 0)
    raz = abs(m) / abs(ALVO) if mesmo else 0.0
    if not mesmo:
        v = "H1 (sinais opostos)"
    elif raz < 1 / 3.:
        v = "H1 (o B1 nao tem o degrau)"
    elif raz > 2 / 3.:
        v = "H0 (o B1 TEM o degrau)"
    else:
        v = "NAO DECIDE"
    return m, raz, v


print("=" * 96)
print("A · O VEREDICTO COM A COMPOSICAO CORRIGIDA")
print("=" * 96)
print()
for nome, conj in (("as 4 publicadas", QUATRO),
                   ("as 3 que a ortofoto sustenta", TRES)):
    m, r, v = criterio(conj)
    print("%-32s n=%d  degrau mediano %+.4f  razao %.2f  ->  %s"
          % (nome, len(conj), m, r, v))
print()
print("o veredicto nao muda de classe. Muda a composicao, e muda o que se pode")
print("escrever a seguir: nao ha nenhuma parcela de kiwi maduro no B1.")

print()
print("=" * 96)
print("B · O PISO DE DETECCAO — que acontecimento e que este criterio veria?")
print("=" * 96)
print()
print("%-10s %14s %14s   %s" % ("injectado", "degrau mediano", "razao",
                                "o que o criterio diria"))
piso13 = piso23 = None
for inj in np.arange(0, -0.601, -0.02):
    m, r, v = criterio(TRES, float(inj))
    if piso13 is None and m < 0:
        piso13 = float(inj)
    if piso23 is None and v.startswith("H0"):
        piso23 = float(inj)
    if abs(inj) < 1e-9 or abs(inj % 0.10) < 1e-9 or abs(abs(inj % 0.10) - 0.10) < 1e-9:
        print("%+10.3f %+14.4f %14.2f   %s" % (inj, m, r, v))
print()
print("o degrau so muda de SINAL com um acontecimento de %+.3f" % piso13)
print("o criterio so diz «H0 · o B1 TEM o degrau» com %+.3f" % piso23)
print("o acontecimento que se procura e de %+.4f" % ALVO)
print()
print("PISO / ALVO = %.1f x    ->    %s"
      % (abs(piso23) / abs(ALVO),
         "o teste nao tem potencia para o acontecimento que procura."
         if abs(piso23) > abs(ALVO) else "o teste tem potencia."))

print()
print("=" * 96)
print("C · O TESTE QUE TEM POTENCIA — cada parcela contra a sua propria curva")
print("=" * 96)
print()


def sat(t, A, B, k):
    return A - B * np.exp(-k * t)


T = np.arange(10, dtype=float)
print("%-10s %9s %9s %9s %9s %10s"
      % ("CUL_ID", "prev 2025", "obs", "prev 2026", "obs", "residuo"))
res = {}
for c in TRES + [6476425]:
    y = C.anual(datas, V[c])
    ok = np.isfinite(y[:8])
    p, _ = curve_fit(sat, T[:8][ok], y[:8][ok], p0=[max(y[:8]), .3, .5],
                     bounds=([0, 0, .01], [1.5, 2, 5]), maxfev=40000)
    r = float(np.nanmean([y[8] - sat(8., *p), y[9] - sat(9., *p)]))
    res[c] = r
    print("%-10d %9.3f %9.3f %9.3f %9.3f %+10.4f%s"
          % (c, sat(8., *p), y[8], sat(9., *p), y[9], r,
             "   <- sem linha de base de kiwi" if c == 6476425 else ""))
print()
print("residuo mediano das 3: %+.4f   ·   acontecimento procurado: %+.4f"
      % (float(np.median([res[c] for c in TRES])), ALVO))
print()
print("Este teste tem potencia: um acontecimento de -0,085 apareceria como um")
print("residuo de -0,085, porque a curva de estabelecimento esta no modelo em")
print("vez de estar na linha de base. E ele nao aparece.")

json.dump(dict(veredicto_4=criterio(QUATRO)[:2], veredicto_3=criterio(TRES)[:2],
               piso_sinal=piso13, piso_h0=piso23, alvo=ALVO,
               residuo={str(c): res[c] for c in res}),
          open(os.path.join(C.OUT, "c3b1_10_veredicto.json"), "w"), indent=1)
print()
print("escrito c3b1_10_veredicto.json")
