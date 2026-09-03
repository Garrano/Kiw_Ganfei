# -*- coding: utf-8 -*-
"""Uma unidade OCIDENTAL que nao foi escolhida pelo sinal.

O problema
----------
O degrau ocidental de -0,1288 esta medido num disco de 90 m cujo centro
(E530485) foi lido de onde o defice de 2026 esta. **O valor esta inflacionado
pela propria escolha do centro**, e a direccao do enviesamento e conhecida:
para cima. Isso torna a frase «os dois focos cairam o mesmo» — oriental
-0,124 contra ocidental -0,129 — uma comparacao entre um numero limpo e um
numero inflacionado. Nao se pode publicar assim.

A solucao
---------
As parcelas do IFAP sao fronteiras ADMINISTRATIVAS. Foram desenhadas para
pagamentos, por outra entidade, anos antes, e nao sabem nada de NDVI. Uma
parcela que contenha o foco ocidental da uma unidade cuja fronteira nao foi
escolhida por nos.

Continua a haver uma escolha nossa — QUAL parcela — e essa escolha e feita
pela geografia (a que contem o ponto), nao pelo valor. Reporta-se a parcela
inteira, sem recortes, e reportam-se todas as parcelas do pomar para o leitor
ver onde a ocidental cai na distribuicao. Uma parcela que so parecesse
extrema depois de escolhida nao passaria neste teste.
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
COM = np.isfinite(h) & (h >= 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
pts = np.column_stack([EE.ravel(), NN.ravel()])

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
D = json.load(open(os.path.join(VG, "ifap_parcelas.json")))

FOCO_OC = (530485.0, 4655053.0)
FOCO_OR = (530999.0, 4655102.0)  # centroide da Zona 0

deg = np.nanmean(nd[T], 0) - np.nanmean(nd[~T], 0)

RNG = np.random.default_rng(20260831)


def perm_p(v, obs, nperm=20000):
    """p por permutacao da etiqueta de ano — nove pontos nao aguentam um t."""
    k, n, c = int(T.sum()), len(v), 0
    for _ in range(nperm):
        s = np.zeros(n, bool)
        s[RNG.permutation(n)[:k]] = True
        if abs(v[s].mean() - v[~s].mean()) >= abs(obs):
            c += 1
    return (c + 1) / (nperm + 1.)

print("=" * 88)
print("PARCELAS DO IFAP QUE INTERSECTAM O POMAR — fronteiras administrativas")
print("=" * 88)
print()
print("%-16s %7s %7s %9s %9s %8s %9s  %s"
      % ("PAR_NUM", "ha tot", "ha com", "altura", "degrau", "p perm", "2017-24", "contem"))
linhas = []
for ft in D["features"]:
    geom = ft["geometry"]
    aneis = (geom["coordinates"] if geom["type"] == "Polygon"
             else [c for p in geom["coordinates"] for c in p])
    dentro = np.zeros(pts.shape[0], bool)
    for k, anel in enumerate(aneis):
        xy = np.array(anel)
        x, y = tr.transform(xy[:, 0], xy[:, 1])
        m = MP(np.column_stack([x, y])).contains_points(pts)
        dentro = m if k == 0 else (dentro & ~m)
    M = dentro.reshape(ny, nx) & POMAR
    if M.sum() < 8:
        continue
    MC = M & COM
    if MC.sum() < 8:
        continue
    v = np.array([float(np.nanmean(nd[i][MC])) for i in range(len(DATAS))])
    d_ = float(v[T].mean() - v[~T].mean())
    p_ = perm_p(v, d_)
    tem = []
    for nome, c in (("OCIDENTAL", FOCO_OC), ("ORIENTAL", FOCO_OR)):
        j = int(np.argmin((EE - c[0]) ** 2 + (NN - c[1]) ** 2))
        if M.ravel()[j]:
            tem.append(nome)
    p = ft["properties"]
    linhas.append(dict(par=p.get("PAR_NUM"), ent=p.get("ENT_ID"),
                       ha=M.sum() / 100., ha_com=MC.sum() / 100.,
                       altura=float(np.median(h[MC])), degrau=d_, p=p_,
                       base=float(v[~T].mean()), serie=[float(x) for x in v],
                       contem=tem))

linhas.sort(key=lambda r: r["degrau"])
for r in linhas:
    print("%-16s %7.2f %7.2f %8.2fm %+9.4f %8.4f %9.3f  %s"
          % (r["par"], r["ha"], r["ha_com"], r["altura"], r["degrau"],
             r["p"], r["base"], ", ".join(r["contem"]) or ""))

print()
print("=" * 88)
print("ONDE CAI CADA FOCO NA DISTRIBUICAO DAS PARCELAS")
print("=" * 88)
print()
degs = np.array([r["degrau"] for r in linhas])
print("n parcelas = %d   mediana do degrau = %+.4f   IQR = %+.4f a %+.4f"
      % (len(linhas), np.median(degs), np.percentile(degs, 25),
         np.percentile(degs, 75)))
print()
for alvo in ("OCIDENTAL", "ORIENTAL"):
    for i, r in enumerate(linhas):
        if alvo in r["contem"]:
            pct = 100.0 * i / max(len(linhas) - 1, 1)
            print("parcela que contem o foco %-9s : %-16s  degrau %+.4f  "
                  "= percentil %.0f de %d parcelas"
                  % (alvo, r["par"], r["degrau"], pct, len(linhas)))
            print("   %s" % "  ".join("%.3f" % x for x in r["serie"]))

json.dump(linhas, open(os.path.join(VG, "ocidental_independente.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito ocidental_independente.json")
