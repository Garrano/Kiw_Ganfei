# -*- coding: utf-8 -*-
"""Q6 (fecho) · o relogio contra o trabalho.

`reg01_triagem_descontinuidade.py` tem ctime = mtime = 01-09 23:25:25.
`reg01_triagem.json`, que e a saida dele, tem ctime = mtime = 23:25:38.
**Treze segundos.**

O script le a cache Landsat inteira DUAS vezes (100 cenas x 39 mascaras na
primeira passagem, 100 x 31 na segunda), constroi 37 mascaras de poligono e
duas mascaras de foco reamostradas. Se esse trabalho levar mais de 13 s, entao
o JSON nao pode ter sido produzido pelo ficheiro que esta em disco com aquela
hora — a corrida comecou ANTES de o script ter sido gravado.

Mede-se o trabalho, com a mesma cache e a mesma maquina.
"""
import json
import os
import time

import numpy as np

import c3b1_00_comum as C

CL = os.path.join(C.VG, "_reg01_landsat_cache")

t0 = time.time()
_ = {c: C.M[c] for c in C.M}
t_masc = time.time() - t0

t0 = time.time()
n = 0
for r in C.CENAS:
    f = C._fich.get(r["data"])
    if not f:
        continue
    nd = np.load(os.path.join(CL, f))["ndvi"]
    for c, m in C.M.items():
        v = nd[m]
        v = v[np.isfinite(v)]
    for nome, m in C.FOCOS.items():
        v = nd[m]
        v = v[np.isfinite(v)]
    n += 1
t_p1 = time.time() - t0

t0 = time.time()
for r in C.CENAS:
    f = C._fich.get(r["data"])
    if not f:
        continue
    nd = np.load(os.path.join(CL, f))["ndvi"]
    for c in C.MANTIDOS:
        v = nd[C.M[c]]
        v = v[np.isfinite(v)]
    for nome, m in C.FOCOS.items():
        v = nd[m]
        v = v[np.isfinite(v)]
t_p2 = time.time() - t0

print("=" * 90)
print("QUANTO TEMPO LEVA O TRABALHO DE `reg01_triagem_descontinuidade.py`")
print("=" * 90)
print()
print("  construir as mascaras (37 poligonos + 2 focos) : %6.1f s" % t_masc)
print("  1.a passagem — %3d cenas x 39 unidades         : %6.1f s" % (n, t_p1))
print("  2.a passagem — %3d cenas x 31 unidades         : %6.1f s" % (n, t_p2))
print("  " + "-" * 55)
print("  TOTAL medido (sem importacoes nem I/O de saida): %6.1f s"
      % (t_masc + t_p1 + t_p2))
print()
print("  a cache esta quente (ja foi lida varias vezes nesta sessao); numa")
print("  leitura fria de disco o total so pode ser MAIOR.")
print()
q = lambda p: os.stat(p).st_mtime
f_py = os.path.join(C.VG, "reg01_triagem_descontinuidade.py")
f_js = os.path.join(C.VG, "reg01_triagem.json")
d = q(f_js) - q(f_py)
print("  intervalo real entre o script gravado e o JSON escrito: %.0f s" % d)
print()
if t_masc + t_p1 + t_p2 > d:
    print("  VEREDICTO: o trabalho nao cabe no intervalo. O `reg01_triagem.json`")
    print("  em disco NAO foi produzido pela corrida que comecou depois de o")
    print("  script ter aquela hora de gravacao. Ou o script foi gravado a meio")
    print("  de uma corrida ja a decorrer, ou foi editado depois de correr.")
    print()
    print("  Isto NAO contradiz o conteudo — a reproducao do Controlo 3 anterior")
    print("  bateu ao maximo de diferenca 0,00e+00. Contradiz a leitura das")
    print("  horas como cronologia de trabalho.")
else:
    print("  VEREDICTO: o trabalho cabe no intervalo. A cronologia e consistente.")
print("=" * 90)

json.dump(dict(t_mascaras=t_masc, t_passagem1=t_p1, t_passagem2=t_p2,
               t_total=t_masc + t_p1 + t_p2, intervalo_real=d, n_cenas=n),
          open(os.path.join(C.OUT, "c3b1_08_cronometro.json"), "w"), indent=1)
