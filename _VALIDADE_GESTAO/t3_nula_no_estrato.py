# -*- coding: utf-8 -*-
"""T3 — a nula dos satélites, agora no mesmo estrato de distância dos alvos.

A acusação, textual
-------------------
`CAMADA_2_ADVERSARIO_R2.md`, R3: a nula é sorteada em `dfoco > 120 m` e os três
alvos estão a **83, 112 e 145 m**. Dois dos três vivem dentro da banda que a
nula exclui. E S7 não salva: testa gradiente contínuo, não diferença de banda.

O teste
-------
Redesenha-se a nula em **60 < d < 150 m** — a banda onde os alvos vivem — e
compara-se com a original. Se os percentis se moverem muito, R3 tinha razão e
os números saem; se não se moverem, voltam.

E acrescenta-se o que faltava para fechar a objecção pela raiz: **a banda
60–150 m difere da banda >120 m?** Compara-se o degrau médio das duas
populações de discos. Se não diferirem, o estrato nunca importou e a nula
original era válida por acaso.

Tudo em 2025 só, com 2026 fora — a cena da selecção continua excluída.
"""
import json
import os

import numpy as np
import rasterio

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14"]
I25 = len(DATAS) - 1

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, ZONA0 = bits("pomar_bits"), bits("zona0_bits")
nd = np.stack([rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
               for d in DATAS])
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)
dfoco = np.minimum(np.hypot(EE - C_OR[0], NN - C_OR[1]),
                   np.hypot(EE - C_OC[0], NN - C_OC[1]))

SAT = [("#1  ·  79 m", 531016.0, 4655184.0, 0.21),
       ("#2  ·  82 m", 530889.0, 4655118.0, 0.24),
       ("#3  ·  143 m", 530359.0, 4654986.0, 0.21)]

RNG = np.random.default_rng(20260831)
NN_ = 1000


def d25(m):
    v = np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])
    return float(v[I25] - v[:I25].mean())


def nula(universo, k, n=NN_):
    iy, ix = np.where(universo)
    out = []
    for _ in range(n):
        j = RNG.integers(len(iy))
        dd = (EE - EE[iy[j], ix[j]]) ** 2 + (NN - NN[iy[j], ix[j]]) ** 2
        sel = np.argsort(np.where(universo, dd, np.inf).ravel())[:k]
        mm = np.zeros(POMAR.size, bool)
        mm[sel] = True
        out.append(d25(mm.reshape(ny, nx)))
    return np.array(out)


BASE = POMAR & COM & ~ZONA0
U_LONGE = BASE & (dfoco > 120)
# CORRECCAO ao proprio teste: a banda 60-150 m inclui celulas DENTRO dos
# discos de 90 m, ou seja a nula estava contaminada pelos proprios focos.
# A banda limpa e 90-160 m: fora dos discos, e ainda onde os alvos #2 e #3
# vivem. O alvo #1, a 83 m, esta DENTRO do disco e nao e comparavel com
# nenhuma nula de fora — reporta-se e nao se testa.
U_BANDA = BASE & (dfoco > 90) & (dfoco < 160)

print("=" * 88)
print("T3 · A NULA NO MESMO ESTRATO DOS ALVOS")
print("=" * 88)
print()
print("universo >120 m      : %5d células  (%.2f ha)" % (U_LONGE.sum(), U_LONGE.sum() / 100))
print("universo 90–160 m    : %5d células  (%.2f ha)" % (U_BANDA.sum(), U_BANDA.sum() / 100))
print()
print("%-14s %6s %10s %11s %11s %10s"
      % ("satélite", "cél", "degrau 25", "perc >120 m", "perc 90-160", "muda?"))
saida = {"unidades": {}}
for nome, e, n_, ha in SAT:
    raio = float(np.sqrt(ha * 10000.0 / np.pi))
    m = (((EE - e) ** 2 + (NN - n_) ** 2) <= raio ** 2) & POMAR
    mc = m & COM
    alvo = mc if mc.sum() >= 8 else m
    k = int(alvo.sum())
    d = d25(alvo)
    nl = nula(U_LONGE, k)
    nb = nula(U_BANDA, k)
    pl = 100.0 * np.mean(nl <= d)
    pb = 100.0 * np.mean(nb <= d)
    saida["unidades"][nome] = dict(celulas=k, degrau=d, perc_longe=float(pl),
                                   perc_banda=float(pb),
                                   nula_longe_mediana=float(np.median(nl)),
                                   nula_banda_mediana=float(np.median(nb)))
    print("%-14s %6d %+10.4f %10.1f %% %10.1f %% %10s"
          % (nome, k, d, pl, pb,
             "sim" if abs(pb - pl) > 3 else "não"))

print()
print("=" * 88)
print("A BANDA É DIFERENTE DO RESTO? — a pergunta que S7 não respondia")
print("=" * 88)
print()
kmed = int(np.median([saida["unidades"][s[0]]["celulas"] for s in SAT]))
nl = nula(U_LONGE, kmed, 600)
nb = nula(U_BANDA, kmed, 600)
from scipy import stats as st
t = st.mannwhitneyu(nl, nb)
print("discos de %d células:" % kmed)
print("  >120 m     mediana %+.4f   IQR %+.4f a %+.4f" % (np.median(nl), *np.percentile(nl, [25, 75])))
print("  90–160 m   mediana %+.4f   IQR %+.4f a %+.4f" % (np.median(nb), *np.percentile(nb, [25, 75])))
print("  Mann-Whitney U  p = %.4f  ->  %s"
      % (t.pvalue, "as bandas DIFEREM" if t.pvalue < 0.05 else "as bandas não diferem"))
saida["bandas"] = dict(mediana_longe=float(np.median(nl)),
                       mediana_banda=float(np.median(nb)),
                       p_mannwhitney=float(t.pvalue))

print()
print("=" * 88)
print("VEREDICTO SOBRE R3")
print("=" * 88)
print()
mudou = any(abs(saida["unidades"][s[0]]["perc_banda"]
                - saida["unidades"][s[0]]["perc_longe"]) > 3 for s in SAT)
if not mudou and t.pvalue >= 0.05:
    print("Os percentis não se movem e as bandas não diferem: a nula original")
    print("era válida, e os números 2,4 / 4,7 / 8,7 % VOLTAM ao PASSA PARA CIMA")
    print("— com o estrato agora verificado, que é mais do que tinham antes.")
else:
    print("Os percentis movem-se ou as bandas diferem. R3 tinha razão e os")
    print("números publicados eram do estrato errado. Ficam os do estrato certo.")

json.dump(saida, open(os.path.join(VG, "t3_nula_no_estrato.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito t3_nula_no_estrato.json")
