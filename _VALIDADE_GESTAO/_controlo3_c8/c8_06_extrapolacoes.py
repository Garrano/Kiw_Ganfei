# -*- coding: utf-8 -*-
"""C8-06 · as duas extrapolacoes do troco oeste contra o testemunho de tipo 1.

PERGUNTA FIXA
-------------
O esquema, extrapolado, sabe onde estao as valvulas 1-5?

  H0 (a falsificar): as posicoes extrapoladas caem dentro da incerteza
  declarada (+-150 m) do segmento que o gestor deu por coordenadas.

Duas extrapolacoes independentes do MESMO desenho existem em disco:
  · `c0_13_georref.json` — ajuste por forma, 13 aneis detectados, dos quais os
    dois de menor x caem no troco oeste;
  · `valvulas_v4.json['lobo_oeste']` — extrapolacao por geometria relativa.

E existe um instrumento que nao e o desenho: **as duas coordenadas duras do
gestor** (`ganfei_s2\\b1_divisao.py`, de -8.643582 42.037577 a -8.636871
42.041184), testemunho de tipo 1 de 28-08.

Falsifica-se H0 se a distancia mediana ao segmento exceder 150 m.
"""
import json
import os
import numpy as np
from pyproj import Transformer

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
G2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
AQUI = os.path.dirname(os.path.abspath(__file__))

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
A = np.array(tr.transform(-8.643581734449253, 42.03757663209986))
B = np.array(tr.transform(-8.636871142810762, 42.04118410828004))
print("segmento do gestor (tipo 1): E %.0f N %.0f  ->  E %.0f N %.0f  (%.0f m)"
      % (A[0], A[1], B[0], B[1], np.hypot(*(B - A))))


def d_seg(p):
    p = np.asarray(p, float)
    v = B - A
    t = np.clip(np.dot(p - A, v) / np.dot(v, v), 0, 1)
    return float(np.hypot(*(A + t * v - p)))


geo = json.load(open(os.path.join(VC, "SAIDA_C0", "c0_13_georref.json")))
pares = sorted(zip(geo["valvulas_px"], geo["valvulas_utm"]),
               key=lambda t: t[0][0])
oeste = [u for px, u in pares if px[0] < 700]
v4 = json.load(open(os.path.join(G2, "valvulas_v4.json"), encoding="utf-8"))
lobo = [(k, tuple(v)) for k, v in sorted(v4["lobo_oeste"].items(), key=lambda t: int(t[0]))]

print()
print("A · `c0_13_georref.json` — os aneis de menor x (troco oeste do desenho)")
for u in oeste:
    print("   E %.0f N %.0f   dist. ao segmento do gestor = %6.1f m"
          % (u[0], u[1], d_seg(u)))
dA = [d_seg(u) for u in oeste]

print()
print("B · `valvulas_v4.json['lobo_oeste']` — valvulas 1 a 5 extrapoladas")
for k, u in lobo:
    print("   v%-2s E %.0f N %.0f   dist. ao segmento do gestor = %6.1f m"
          % (k, u[0], u[1], d_seg(u)))
dB = [d_seg(u) for _, u in lobo]

print()
print("mediana da distancia:  c0_13 = %.1f m   ·   v4 lobo_oeste = %.1f m"
      % (np.median(dA), np.median(dB)))
print("incerteza declarada do lobo em valvulas_v4.json: +-150 m")
print("H0 (as posicoes caem dentro de +-150 m): %s para o v4"
      % ("SOBREVIVE" if np.median(dB) <= 150 else "FALSIFICADA"))
print("H0 para o c0_13: %s"
      % ("SOBREVIVE" if np.median(dA) <= 150 else "FALSIFICADA"))

# e as duas extrapolacoes entre si
D = np.array([[np.hypot(u[0] - w[0], u[1] - w[1]) for _, w in lobo]
              for u in oeste])
print()
print("as duas extrapolacoes do MESMO desenho, uma contra a outra:")
print("   distancia minima entre conjuntos: %.0f m" % D.min())
print("   distancia entre centroides:       %.0f m"
      % np.hypot(np.mean([u[0] for u in oeste]) - np.mean([w[0] for _, w in lobo]),
                 np.mean([u[1] for u in oeste]) - np.mean([w[1] for _, w in lobo])))
print()
print("LEITURA: duas georreferenciacoes do mesmo PDF, feitas na mesma tarde,")
print("colocam o troco oeste a mais de meio quilometro uma da outra. O desenho")
print("NAO carrega posicao utilizavel para as valvulas 1-5 — nem para as")
print("confirmar, nem para as negar. Quem tem posicao e o gestor.")

json.dump(dict(segmento_gestor=[A.tolist(), B.tolist()],
               c0_13_oeste=[list(u) for u in oeste], dist_c0_13=dA,
               v4_lobo={k: list(u) for k, u in lobo}, dist_v4=dB,
               mediana_c0_13=float(np.median(dA)), mediana_v4=float(np.median(dB)),
               limiar_m=150,
               entre_extrapolacoes_min_m=float(D.min())),
          open(os.path.join(AQUI, "c8_06_extrapolacoes.json"), "w"), indent=1)
print("\nescrito c8_06_extrapolacoes.json")
