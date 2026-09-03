# -*- coding: utf-8 -*-
"""Os satelites, com o ano da seleccao retirado. O teste que nao e circular.

O problema com o teste anterior
-------------------------------
Os tres nucleos satelite foram IDENTIFICADOS como nucleos do mapa de defice —
ou seja, foram escolhidos por terem NDVI baixo, e a cena em que foram
escolhidos e a de 2026. Testar depois se cairam mais do que discos ao acaso e
em boa parte perguntar se sao baixos em 2026 os sitios que se escolheram por
serem baixos em 2026.

O resultado anterior (percentil 1,2 / 1,2 / 2,4 % da nula de vizinhanca) nao
esta errado, mas nao esta limpo, e o dossie ja pagou caro por publicar
resultados que so a construcao produzia.

O que a seleccao NAO forca
--------------------------
Duas coisas, e sao as duas que interessam:

1. **O nivel ANTERIOR.** Um sitio pode ser baixo em 2026 por sempre ter sido
   baixo — e metade do foco oriental e exactamente isso. Os satelites nao:
   0,878 · 0,872 · 0,901 de media em 2017-2024, contra 0,867 a 0,892 nas
   parcelas do IFAP. **Estavam normais, e o #3 acima da mediana.** A seleccao
   nao podia produzir isto.

2. **2025.** A cena de 2025-08-14 nao entrou na seleccao. Se os satelites ja
   estavam a descer em 2025, a seleccao de 2026 nao o explica.

O teste, fixado antes de correr
-------------------------------
    Degrau = 2025 SO, contra a media de 2017-2024. A cena de 2026 sai do
    calculo inteiro — nao entra no alvo nem na nula.

    H0 : em 2025, os satelites nao diferem de discos do mesmo tamanho
         sorteados no pomar com pergola longe dos focos.

Criterio a priori: **percentil <= 10 da nula de vizinhanca** — mais folgado
que os 5 % anteriores porque uma cena so tem mais ruido que a media de duas, e
fixa-se isso antes de ver o numero, nao depois.

Um satelite que passe aqui esta estabelecido com uma cena que a sua propria
seleccao nao viu. Um que nao passe fica com o estatuto de «visto em 2026,
nao confirmado em 2025», que e uma afirmacao mais fraca e honesta.
"""
import json
import os

import numpy as np
import rasterio

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14"]          # 2026 FORA
I25 = len(DATAS) - 1

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
C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)
dfoco = np.minimum(np.hypot(EE - C_OR[0], NN - C_OR[1]),
                   np.hypot(EE - C_OC[0], NN - C_OC[1]))

SAT = [("#1  ·  79 m do oriental", 531016.0, 4655184.0, 0.21),
       ("#2  ·  82 m do oriental", 530889.0, 4655118.0, 0.24),
       ("#3  ·  143 m do ocidental", 530359.0, 4654986.0, 0.21)]

RNG = np.random.default_rng(20260831)
NNULA = 1000
UNIV = POMAR & COM & (dfoco > 120) & ~ZONA0
iy, ix = np.where(UNIV)


def d25(m):
    v = np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])
    return float(v[I25] - v[:I25].mean()), v


print("=" * 86)
print("OS SATELITES SEM A CENA QUE OS SELECCIONOU  —  2025 contra 2017-2024")
print("=" * 86)
print()
print("universo da nula: %d celulas a mais de 120 m de qualquer foco"
      % UNIV.sum())
print()
print("%-28s %5s %9s %9s %10s %9s"
      % ("satelite", "cel", "base", "2025", "degrau 25", "perc.nula"))

saida = {"nota": "2026 excluida do calculo — foi a cena da seleccao",
         "satelites": []}
for nome, e, n_, ha in SAT:
    raio = float(np.sqrt(ha * 10000.0 / np.pi))
    m = (((EE - e) ** 2 + (NN - n_) ** 2) <= raio ** 2) & POMAR
    mc = m & COM
    alvo = mc if mc.sum() >= 8 else m
    d, v = d25(alvo)
    k = int(alvo.sum())
    nulos = []
    for _ in range(NNULA):
        j = RNG.integers(len(iy))
        dd = (EE - EE[iy[j], ix[j]]) ** 2 + (NN - NN[iy[j], ix[j]]) ** 2
        sel = np.argsort(np.where(UNIV, dd, np.inf).ravel())[:k]
        mm = np.zeros(POMAR.size, bool)
        mm[sel] = True
        nulos.append(d25(mm.reshape(ny, nx))[0])
    nulos = np.array(nulos)
    perc = float(100.0 * np.mean(nulos <= d))
    passa = (d < 0) and (perc <= 10.0)
    print("%-28s %5d %9.3f %9.3f %+10.4f %7.1f %%  %s"
          % (nome, k, v[:I25].mean(), v[I25], d, perc,
             "PASSA" if passa else "NAO PASSA"))
    saida["satelites"].append(dict(
        nome=nome, celulas=k, base=float(v[:I25].mean()),
        v2025=float(v[I25]), degrau_2025=d, percentil_nula=perc,
        passa=bool(passa), nula_p10=float(np.percentile(nulos, 10)),
        nula_mediana=float(np.median(nulos))))

print()
print("PARA COMPARAR:")
for nome, m in (("resto do pomar (controlo)", POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF),
                ("foco ORIENTAL com pergola", ZONA0 & COM),
                ("foco OCIDENTAL com pergola",
                 (np.hypot(EE - C_OC[0], NN - C_OC[1]) <= 90) & POMAR & COM)):
    d, v = d25(m)
    print("  %-28s %5d %9.3f %9.3f %+10.4f"
          % (nome, m.sum(), v[:I25].mean(), v[I25], d))

print()
print("=" * 86)
print("VEREDICTO — o que fica estabelecido sem a cena da seleccao")
print("=" * 86)
print()
n_ok = sum(1 for s in saida["satelites"] if s["passa"])
for s in saida["satelites"]:
    print("  %-28s %-10s  base %.3f (normal)  ·  2025 %+.4f  ·  percentil %.1f %%"
          % (s["nome"], "PASSA" if s["passa"] else "NAO PASSA",
             s["base"], s["degrau_2025"], s["percentil_nula"]))
saida["n_passa"] = n_ok
print()
print("passam %d de %d com a cena da seleccao retirada." % (n_ok, len(SAT)))

json.dump(saida, open(os.path.join(VG, "satelites_sem_2026.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito satelites_sem_2026.json")
