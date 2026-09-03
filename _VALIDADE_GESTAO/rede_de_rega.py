# -*- coding: utf-8 -*-
"""O declinio segue a rede de rega? — depois de o terreno ter falhado.

Porque esta hipotese substitui a anterior
-----------------------------------------
A hipotese topografica foi fixada, corrida e **retirada**: dentro do copado
vivo o defice esta no terreno ALTO (rho da cota negativo nas onze cenas,
p<0,001), e nenhuma metrica de humidade emerge em 2025-26 — a area drenante
ate decai para zero nos anos do evento.

Se nao e o terreno, e o NDMI cai antes do NDVI, entao o problema esta na planta
ou no que lhe chega. A conjuntura oferece um candidato concreto, e vem de
testemunho, nao de inferencia nossa:

  · toda a exploracao tem **origem de agua unica**;
  · a **valvula 185 foi desactivada** porque levaram a conduta para pomares
    novos;
  · plantaram-se **+11,16 ha** entre 2022 e 2025 (4,09 · 2,85 · 1,50 · 2,72).

**Hipotese fixa:** o defice de 2025-26 organiza-se pela **topologia da rega** —
identidade de valvula e posicao na rede — mais do que pela geografia.

Como se testa, e o que a falsifica
----------------------------------
1. **Agrupamento por valvula.** Se o defice se agrupa por valvula acima do que
   uma particao geografica arbitraria da mesma granularidade explicaria, ha
   sinal de rede. O nulo sao **particoes de Voronoi sobre pontos rodados**
   dentro do pomar — mesma geometria, sem relacao com a rede.
2. **Ordem na rede.** Se a rega e sequencial a partir de uma origem, as
   valvulas mais distantes ao longo da conduta sofrem primeiro. Testa-se a
   correlacao entre o defice medio por valvula e a distancia ao ponto de
   origem, com a valvula como unidade — n=12, nao n=2654 celulas.
3. **Emergencia.** Como no teste do terreno, o criterio e a mesma serie: se o
   agrupamento por valvula existir em todos os anos, e geografia; se **emergir
   em 2025-26**, e evento.

**Falsifica-se** se o agrupamento por valvula nao exceder o nulo geografico,
ou se nao emergir em 2025-26.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(AQUI, "chm_altura.npy"))
VIVO = POMAR & np.isfinite(h) & (h >= 0.5)

V = json.load(open(os.path.join(RAIZ, "valvulas_por_area.json")))
pts = [(int(k), v["E"], v["N"], v.get("bloco"), v.get("area_m2"))
       for k, v in V.items()]
pts.sort()
print("valvulas com posicao: %d" % len(pts))

E, N = centros_celulas()


def voronoi(coords):
    d = np.stack([np.hypot(E - x, N - y) for _, x, y in coords])
    return np.argmin(d, axis=0)


coords = [(k, x, y) for k, x, y, _, _ in pts]
LAB = voronoi(coords)
print("celulas de copado vivo por valvula:")
for i, (k, x, y) in enumerate(coords):
    n = ((LAB == i) & VIVO).sum()
    print("   v%-3d %-12s %5.2f ha de copado vivo" % (k, pts[i][3] or "", n / 100.0))

nd = carrega_ndvi(TODAS)
SERIE = sorted(nd)


def eta2(lab, f, m):
    """fraccao da variancia do fosso explicada pela particao (eta quadrado)"""
    v = f[m]
    g = lab[m]
    tot = ((v - v.mean()) ** 2).sum()
    ent = 0.0
    for u in np.unique(g):
        s = v[g == u]
        if s.size:
            ent += s.size * (s.mean() - v.mean()) ** 2
    return ent / tot if tot else np.nan


# nulo: mesmas 12 posicoes, rodadas em bloco em torno do centroide do pomar
ys, xs = np.where(VIVO)
cx, cy = E[VIVO].mean(), N[VIVO].mean()
NULOS = []
rng = np.random.default_rng(20260829)
for ang in rng.uniform(0, 2 * np.pi, 200):
    c, s = np.cos(ang), np.sin(ang)
    rot = [(k, cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)
           for k, x, y in coords]
    NULOS.append(voronoi(rot))

print("\nAGRUPAMENTO DO FOSSO POR VALVULA, contra 200 particoes rodadas\n")
print("%-12s %9s %11s %9s %8s" % ("cena", "eta2 real", "nulo p50", "nulo p95", "posto"))
res = {}
for d in SERIE:
    a = nd[d]
    f = float(np.nanmean(a[REF])) - a
    m = VIVO & np.isfinite(f)
    e = eta2(LAB, f, m)
    nn = np.array([eta2(L, f, m) for L in NULOS])
    p = float((nn >= e).mean())
    res[d] = dict(eta2=float(e), nulo_p50=float(np.median(nn)),
                  nulo_p95=float(np.percentile(nn, 95)), p=p)
    print("%-12s %9.4f %11.4f %9.4f %8s"
          % (d, e, np.median(nn), np.percentile(nn, 95),
             "p=%.3f" % p))

print("\nDEFICE MEDIO POR VALVULA (fosso), copado vivo\n")
print("%-6s %-12s %s" % ("valv", "bloco", "  ".join("%6s" % d[2:7] for d in SERIE)))
tab = {}
for i, (k, x, y) in enumerate(coords):
    m = VIVO & (LAB == i)
    if m.sum() < 25:
        continue
    L = []
    for d in SERIE:
        a = nd[d]
        L.append(float(np.nanmean(a[REF])) - float(np.nanmean(a[m])))
    tab[k] = L
    print("v%-5d %-12s %s" % (k, pts[i][3] or "", "  ".join("%+6.3f" % v for v in L)))

# ordem na rede: distancia ao ponto de origem (armazem, testemunho do gestor)
ORIG = (530360.0, 4654848.0)
print("\nORDEM NA REDE — distancia a origem contra defice, valvula como unidade\n")
print("%-12s %8s %8s %6s" % ("cena", "rho", "p", "n"))
ordem = {}
for j, d in enumerate(SERIE):
    dd, ff = [], []
    for i, (k, x, y) in enumerate(coords):
        if k in tab:
            dd.append(np.hypot(x - ORIG[0], y - ORIG[1]))
            ff.append(tab[k][j])
    rho, p = stats.spearmanr(dd, ff)
    ordem[d] = dict(rho=float(rho), p=float(p), n=len(dd))
    print("%-12s %+8.3f %8.3f %6d" % (d, rho, p, len(dd)))

json.dump(dict(agrupamento=res, por_valvula=tab, ordem=ordem),
          open(os.path.join(AQUI, "rede_de_rega.json"), "w"), indent=1)
print("""
LEITURA
  eta2 acima do nulo, e a subir em 2025-26  ->  a rede organiza o defice
  eta2 dentro do nulo                       ->  e geografia, nao rede
  rho positivo e a crescer                  ->  as valvulas distantes sofrem
                                                primeiro""")
