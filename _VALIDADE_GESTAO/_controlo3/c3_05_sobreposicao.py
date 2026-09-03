# -*- coding: utf-8 -*-
"""O bloco 8845731 esta a 7 m do centro do foco ORIENTAL. Quanto se sobrepoem?

Isto nao estava na lista de perguntas. Apareceu ao localizar os tres blocos
excluidos do ENT 472062: o centroide de 8845731 e E530982 N4655112, e o centro
declarado do FOCO ESTE, na `REGISTO_DE_NOMES.md` e em toda a cadeia, e
E530977 N4655117. Sete metros.

Se as duas mascaras cobrirem o mesmo chao, a triagem exclui como «linha de base
descontinua» a MESMA unidade que a REG-01 refeita poe em segundo pior lugar da
regiao.

Mede-se em tres grelhas: os poligonos em si, a grelha de 10 m das mascaras do
caso, e a grelha de 30 m onde a REG-01 corre.
"""
import os
import sys

import numpy as np
from matplotlib.path import Path as MP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import carregar

D = carregar()
G, M, F = D["GEOM"], D["M"], D["FOCOS"]
E10, N10, POMAR, ZONA0, COM = D["E10"], D["N10"], D["POMAR"], D["ZONA0"], D["COM"]

DOC10 = (np.hypot(E10 - 530485., N10 - 4655053.) <= 90) & POMAR & COM
DOR10 = ZONA0 & COM
CAND = {"foco OCIDENTAL": DOC10, "foco ORIENTAL": DOR10,
        "zona0 crua (sem COM)": ZONA0,
        "disco OESTE cru (sem POMAR nem COM)":
            np.hypot(E10 - 530485., N10 - 4655053.) <= 90}

pts10 = np.column_stack([E10.ravel(), N10.ravel()])
POL = {}
for c, g in G.items():
    POL[c] = MP(np.array(list(g.exterior.coords))).contains_points(
        pts10).reshape(E10.shape)

print("=" * 100)
print("SOBREPOSICAO das mascaras dos focos com os poligonos do IFAP (grelha de 10 m)")
print("=" * 100)
print()
for nome, m in CAND.items():
    print("%-38s %3d celulas de 10 m = %.2f ha" % (nome, m.sum(), m.sum() * 0.01))
    tot = m.sum()
    linhas = []
    for c in sorted(POL, key=lambda z: -(POL[z] & m).sum()):
        n = int((POL[c] & m).sum())
        if n:
            linhas.append((c, n, 100.0 * n / tot, 100.0 * n / max(POL[c].sum(), 1)))
    for c, n, pf, pb in linhas[:6]:
        print("     %-9d %3d cel  = %5.1f %% do foco  e %5.1f %% do bloco %s"
              % (c, n, pf, pb,
                 "  <== EXCLUIDO PELA TRIAGEM" if c in (8845729, 8845731, 8845739)
                 else ""))
    fora = tot - sum(x[1] for x in linhas)
    print("     %-9s %3d cel  = %5.1f %% do foco  FORA de qualquer bloco de kiwi do IFAP"
          % ("(nenhum)", fora, 100.0 * fora / tot))
    print()

print("=" * 100)
print("O MESMO na grelha de 30 m, que e onde a REG-01 corre")
print("=" * 100)
print()
for nome in ("foco OCIDENTAL", "foco ORIENTAL"):
    m = F[nome]
    tot = int(m.sum())
    print("%-16s %d celulas de 30 m" % (nome, tot))
    for c in sorted(M, key=lambda z: -(M[z] & m).sum())[:4]:
        n = int((M[c] & m).sum())
        if n:
            print("     %-9d %2d cel de 30 m = %5.1f %% do foco  e %5.1f %% do bloco %s"
                  % (c, n, 100.0 * n / tot, 100.0 * n / max(M[c].sum(), 1),
                     "  <== EXCLUIDO PELA TRIAGEM" if c in (8845729, 8845731, 8845739)
                     else ""))
    print()

print("=" * 100)
print("DISTANCIAS entre centroides")
print("=" * 100)
CEN = {"foco OESTE declarado": (530485., 4655053.),
       "foco ESTE declarado": (530977., 4655117.)}
for nome, (x, y) in CEN.items():
    for c in (8845729, 8845731, 8845739, 4405900, 6476416, 8845724):
        g = G[c]
        d = np.hypot(g.centroid.x - x, g.centroid.y - y)
        if d < 400:
            print("  %-22s -> bloco %-9d %6.0f m %s"
                  % (nome, c, d, "(EXCLUIDO)" if c in (8845729, 8845731, 8845739) else ""))
