# -*- coding: utf-8 -*-
"""Duas verificacoes que o degrau tem de passar antes de ir para uma figura.

1. RESISTE AO LIMIAR? O corte de 0,5 m que separa «tem pergola» de «nao tem»
   e uma escolha nossa. Se o degrau so aparecer a 0,5 m, e do limiar.

2. A PROPRIA REFERENCIA DA DEGRAU? Se der, entao parte do que se le nos focos
   e um evento de toda a area e nao dos focos. A conta que resolve isto e a do
   NIVEL ABSOLUTO, que nao usa referencia nenhuma — mas o tamanho relativo tem
   de ser dito.
"""
import json
import os

import numpy as np
import rasterio

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
TARDIO = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
nd = {d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}
h = np.load(os.path.join(VG, "chm_altura.npy"))
ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
dsc = lambda c, r=90.: ((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r ** 2
FIN = np.isfinite(h)
OC, OR_ = dsc((530485., 4655053.)), dsc((530977., 4655117.))

RNG = np.random.default_rng(20260831)
NP_ = 20000


def nivel(m):
    return np.array([float(np.nanmean(nd[d][m])) for d in DATAS])


def perm(v):
    obs = abs(v[TARDIO].mean() - v[~TARDIO].mean())
    k, n, c = int(TARDIO.sum()), len(v), 0
    for _ in range(NP_):
        s = np.zeros(n, bool)
        s[RNG.permutation(n)[:k]] = True
        if abs(v[s].mean() - v[~s].mean()) >= obs:
            c += 1
    return (c + 1) / (NP_ + 1.)


print("=" * 78)
print("1 · O DEGRAU RESISTE AO LIMIAR DE ALTURA?   (nivel absoluto, sem referencia)")
print("=" * 78)
print()
print("%-8s %8s %10s %8s %8s %10s %8s"
      % ("limiar", "Z0 ha", "degrau Z0", "p", "OC ha", "degrau OC", "p"))
rob = {}
for lim in (0.3, 0.5, 1.0, 1.5, 2.0):
    C = FIN & (h >= lim)
    z, o = ZONA0 & C, OC & POMAR & C
    vz, vo = nivel(z), nivel(o)
    dz = vz[TARDIO].mean() - vz[~TARDIO].mean()
    do_ = vo[TARDIO].mean() - vo[~TARDIO].mean()
    pz, po = perm(vz), perm(vo)
    rob["%.1f" % lim] = dict(ha_z=z.sum() / 100., d_z=float(dz), p_z=pz,
                             ha_o=o.sum() / 100., d_o=float(do_), p_o=po)
    print("%-8.1f %8.2f %+10.4f %8.4f %8.2f %+10.4f %8.4f"
          % (lim, z.sum() / 100., dz, pz, o.sum() / 100., do_, po))

print()
print("=" * 78)
print("2 · A PROPRIA REFERENCIA DA DEGRAU?  E o resto do pomar?")
print("=" * 78)
print()
COM = FIN & (h >= 0.5)
ALVO = [("referencia sistematica (1,10 ha)", REF),
        ("referencia, so celulas com pergola", REF & COM),
        ("resto do pomar com pergola", POMAR & COM & ~OC & ~OR_ & ~REF),
        ("ORIENTAL Zona 0 com pergola", ZONA0 & COM),
        ("OCIDENTAL disco com pergola", OC & POMAR & COM)]
print("%-38s %s   %9s %8s" % ("", "  ".join(d[2:7] for d in DATAS),
                              "degrau", "p perm"))
tab = {}
for n_, m in ALVO:
    v = nivel(m)
    d = float(v[TARDIO].mean() - v[~TARDIO].mean())
    p = perm(v)
    tab[n_] = dict(ha=m.sum() / 100., serie=[float(x) for x in v],
                   degrau=d, p_perm=p)
    print("%-38s %s   %+9.4f %8.4f%s"
          % (n_, "  ".join("%.3f" % x for x in v), d, p,
             "  *" if p < 0.05 else ""))

print()
dref = tab["referencia sistematica (1,10 ha)"]["degrau"]
for n_ in ("ORIENTAL Zona 0 com pergola", "OCIDENTAL disco com pergola",
           "resto do pomar com pergola"):
    print("%-38s queda %.3f  =  %.1f x a da referencia"
          % (n_, -tab[n_]["degrau"], tab[n_]["degrau"] / dref))

json.dump(dict(robustez_limiar=rob, degraus=tab),
          open(os.path.join(VG, "degrau_robustez.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito degrau_robustez.json")
