# -*- coding: utf-8 -*-
"""O multiverso do degrau em NIVEL ABSOLUTO — a moeda nova, atravessada.

Porque e preciso
----------------
Na moeda antiga (fosso a referencia) a unidade escolhida decidia o veredicto:
o poligono da Zona 0 dava p = 0,029 e o disco de 90 m dava p = 0,061. Isso e
exactamente o que a literatura do multiverso descreve — analises defensaveis
baratas de gerar, e a prova a ficar vulneravel a relato selectivo.

A moeda nova nao divide por uma referencia, logo espera-se que seja mais
robusta. **Esperar nao e medir.** Corre-se o espaco inteiro e imprime-se a
AMPLITUDE, nao o melhor valor.

O espaco de analise, fixado antes de correr
-------------------------------------------
Tres eixos, e nenhum deles e o valor medido:

  UNIDADE   ORIENTAL : poligono Zona 0 (geografico, ficheiro antigo)
                       disco no centroide da Zona 0
                       parcela IFAP 1595642933001 (administrativa)
            OCIDENTAL: disco no centro do defice de 2026 (centro do SINAL)
                       parcela IFAP 1585646119001 (administrativa)
  RAIO      60, 90, 120 m — so para as unidades que sao discos
  LIMIAR    0,3 · 0,5 · 1,0 · 1,5 · 2,0 m de altura no LiDAR

O controlo — resto do pomar com pergola — corre em todas as combinacoes de
limiar, porque tem de continuar a nao dar degrau em nenhuma delas. Um controlo
que so funciona a um limiar nao e controlo.

PROVENIENCIA, e nao se dilui na tabela
--------------------------------------
Das cinco unidades, quatro tem fronteira independente do NDVI e uma nao: o
disco ocidental foi centrado onde esta o defice de 2026. Vai marcada em todas
as saidas. As parcelas do IFAP sao o oposto — desenhadas por outra entidade
para pagamentos, anos antes, e diluidas por incluirem area sa.

O que faria a P03 mudar de mensagem
-----------------------------------
Se o degrau dos focos variar de sinal, ou se o intervalo de qualquer foco
tocar o intervalo do controlo, a figura passa a mostrar a banda e a peca
di-lo. Escrito antes de ver o resultado.
"""
import json
import os

import numpy as np
import rasterio
from matplotlib.path import Path as MP
from pyproj import Transformer

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
T = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
nd = np.stack([rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
               for d in DATAS])
h = np.load(os.path.join(VG, "chm_altura.npy"))
FIN = np.isfinite(h)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
pts = np.column_stack([EE.ravel(), NN.ravel()])

C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
IF = json.load(open(os.path.join(VG, "ifap_parcelas.json")))


def parcela(num):
    for ft in IF["features"]:
        if ft["properties"].get("PAR_NUM") != num:
            continue
        gm = ft["geometry"]
        aneis = (gm["coordinates"] if gm["type"] == "Polygon"
                 else [c for p in gm["coordinates"] for c in p])
        dentro = np.zeros(pts.shape[0], bool)
        for k, anel in enumerate(aneis):
            xy = np.array(anel)
            x, y = tr.transform(xy[:, 0], xy[:, 1])
            m = MP(np.column_stack([x, y])).contains_points(pts)
            dentro = m if k == 0 else (dentro & ~m)
        return dentro.reshape(ny, nx) & POMAR
    raise KeyError(num)


P_OC = parcela("1585646119001")
P_OR = parcela("1595642933001")


def disco(c, r):
    return (((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r * r) & POMAR


RNG = np.random.default_rng(20260831)
NPERM = 20000


def degrau_p(m):
    v = np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])
    obs = v[T].mean() - v[~T].mean()
    k, n, c = int(T.sum()), len(v), 0
    for _ in range(NPERM):
        s = np.zeros(n, bool)
        s[RNG.permutation(n)[:k]] = True
        if abs(v[s].mean() - v[~s].mean()) >= abs(obs):
            c += 1
    return float(obs), (c + 1) / (NPERM + 1.), v


LIMIARES = (0.3, 0.5, 1.0, 1.5, 2.0)
RAIOS = (60, 90, 120)

UNIDADES = []
for r in RAIOS:
    UNIDADES.append(("ORIENTAL", "disco %d m" % r, disco(C_OR, r), True))
UNIDADES.append(("ORIENTAL", "poligono Zona 0", ZONA0.copy(), True))
UNIDADES.append(("ORIENTAL", "parcela IFAP 1595642933001", P_OR, True))
for r in RAIOS:
    UNIDADES.append(("OCIDENTAL", "disco %d m" % r, disco(C_OC, r), False))
UNIDADES.append(("OCIDENTAL", "parcela IFAP 1585646119001", P_OC, True))

# o controlo tem de excluir tudo o que qualquer unidade possa apanhar
QUALQUER = np.zeros_like(POMAR)
for _, _, m, _ in UNIDADES:
    QUALQUER |= m
QUALQUER |= disco(C_OR, 120) | disco(C_OC, 120) | ZONA0

print("=" * 92)
print("MULTIVERSO DO DEGRAU EM NIVEL ABSOLUTO — %d unidades x %d limiares"
      % (len(UNIDADES), len(LIMIARES)))
print("=" * 92)
print()
print("%-9s %-30s %6s %7s %9s %9s %s"
      % ("foco", "unidade", "limiar", "ha", "degrau", "p perm", "fronteira"))

linhas = []
for foco, nome, base, indep in UNIDADES:
    for lim in LIMIARES:
        m = base & FIN & (h >= lim)
        if m.sum() < 8:
            continue
        d, p, v = degrau_p(m)
        linhas.append(dict(foco=foco, unidade=nome, limiar=lim,
                           ha=m.sum() / 100., degrau=d, p=p,
                           independente=indep,
                           serie=[float(x) for x in v]))
        print("%-9s %-30s %6.1f %7.2f %+9.4f %9.4f %s%s"
              % (foco, nome, lim, m.sum() / 100., d, p,
                 "independente" if indep else "CENTRO DO SINAL",
                 "  *" if p < 0.05 else ""))

print()
print("CONTROLO — resto do pomar com pergola, fora de tudo, a cada limiar")
ctrl = []
for lim in LIMIARES:
    m = POMAR & FIN & (h >= lim) & ~QUALQUER & ~REF
    d, p, v = degrau_p(m)
    ctrl.append(dict(limiar=lim, ha=m.sum() / 100., degrau=d, p=p,
                     serie=[float(x) for x in v]))
    print("%-40s %6.1f %7.2f %+9.4f %9.4f" % ("resto do pomar", lim,
                                              m.sum() / 100., d, p))

print()
print("=" * 92)
print("A AMPLITUDE — e o que vai impresso na figura, nao o melhor valor")
print("=" * 92)
print()
for foco in ("ORIENTAL", "OCIDENTAL"):
    v = [r["degrau"] for r in linhas if r["foco"] == foco]
    vi = [r["degrau"] for r in linhas if r["foco"] == foco and r["independente"]]
    ps = [r["p"] for r in linhas if r["foco"] == foco]
    print("%-10s n=%2d   degrau  min %+.4f   mediana %+.4f   max %+.4f"
          % (foco, len(v), min(v), float(np.median(v)), max(v)))
    print("%-10s        p       min %.4f   mediana %.4f   max %.4f   "
          "abaixo de 0,05 em %d de %d"
          % ("", min(ps), float(np.median(ps)), max(ps),
             sum(1 for x in ps if x < 0.05), len(ps)))
    if vi and len(vi) != len(v):
        print("%-10s        so fronteiras independentes: min %+.4f  max %+.4f"
              % ("", min(vi), max(vi)))
cv = [r["degrau"] for r in ctrl]
cp = [r["p"] for r in ctrl]
print("%-10s n=%2d   degrau  min %+.4f   mediana %+.4f   max %+.4f"
      % ("CONTROLO", len(cv), min(cv), float(np.median(cv)), max(cv)))
print("%-10s        p       min %.4f   max %.4f   abaixo de 0,05 em %d de %d"
      % ("", min(cp), max(cp), sum(1 for x in cp if x < 0.05), len(cp)))

print()
todos = [r["degrau"] for r in linhas]
print("OS DOIS CRITERIOS QUE MUDARIAM A MENSAGEM, fixados antes de correr:")
print("  1. algum degrau de foco muda de sinal?      %s"
      % ("SIM — a mensagem muda" if max(todos) > 0 else "nao, todos negativos"))
sobrep = max(todos) >= min(cv)
print("  2. o intervalo dos focos toca o do controlo? %s"
      % ("SIM — a mensagem muda" if sobrep else
         "nao  (pior foco %+.4f  <  melhor controlo %+.4f)" % (max(todos), min(cv))))

json.dump(dict(unidades=linhas, controlo=ctrl,
               centro_oriental=C_OR, centro_ocidental=C_OC),
          open(os.path.join(VG, "multiverso_degrau.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito multiverso_degrau.json")
