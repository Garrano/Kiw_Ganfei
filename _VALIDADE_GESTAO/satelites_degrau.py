# -*- coding: utf-8 -*-
"""Porta de entrada da P12: os tres nucleos satelite passam o teste de degrau?

Porque este teste e obrigatorio
-------------------------------
O dossie afirma «as frentes ja sairam das manchas desenhadas: ha tres nucleos
destacados a 79, 82 e 143 metros». Se for verdade, e a UNICA prova de
propagacao nao contigua que o caso tem — e uma propagacao descontigua e um
discriminador forte entre hipoteses.

Mas os tres foram derivados sob o regime de mascaras antigo, e a medicao limpa
mostrou que **fora dos dois focos o pomar nao se mexeu**: o controlo da 0,014
com p = 0,51, e nao ha halo (rho ingenuo p = 2e-9, toroidal p = 0,55).

Ou os tres satelites sao reais e sao a excepcao a essa frase, ou fazem parte
dos 0,014 e a frase esta errada. Nao podem ser as duas coisas.

O teste, fixado antes de correr
-------------------------------
Cada satelite e um poligono pequeno com coordenada publicada. Corre-se-lhe o
MESMO teste que fechou a P03 — degrau em nivel absoluto, 2025-26 contra
2017-24, p por permutacao da etiqueta de ano — e compara-se com:

  · o CONTROLO (resto do pomar com pergola), que nao da degrau;
  · e uma DISTRIBUICAO NULA DE VIZINHANCA: mil discos do mesmo tamanho,
    sorteados ao acaso no pomar com pergola fora dos focos. Isto e o que a
    P03 nao tinha e este teste precisa, porque um poligono de 21 celulas tem
    ruido que um de 800 nao tem. **Um satelite so conta se cair na cauda
    dessa distribuicao**, nao se apenas parecer negativo.

Criterio a priori: **degrau < 0 e percentil <= 5 da nula de vizinhanca.**

Se os tres sobreviverem, sao a peca mais consequente do dossie e a P12
desenha-os. Se nao sobreviverem, saem, e a lista de RETIRADO passa a catorze.
Escrito antes de ver o resultado.
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
C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)
dfoco = np.minimum(np.hypot(EE - C_OR[0], NN - C_OR[1]),
                   np.hypot(EE - C_OC[0], NN - C_OC[1]))

# coordenadas publicadas no dossie (difusa_nucleos.csv, via memo A07)
SAT = [("#1  ·  79 m do oriental", 531016.0, 4655184.0, 0.21),
       ("#2  ·  82 m do oriental", 530889.0, 4655118.0, 0.24),
       ("#3  ·  143 m do ocidental", 530359.0, 4654986.0, 0.21)]

RNG = np.random.default_rng(20260831)
NPERM = 20000
NNULA = 1000


def serie(m):
    return np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])


def degrau(v):
    return float(v[T].mean() - v[~T].mean())


def perm_p(v):
    obs = abs(degrau(v))
    k, n, c = int(T.sum()), len(v), 0
    for _ in range(NPERM):
        s = np.zeros(n, bool)
        s[RNG.permutation(n)[:k]] = True
        if abs(v[s].mean() - v[~s].mean()) >= obs:
            c += 1
    return (c + 1) / (NPERM + 1.)


print("=" * 88)
print("OS TRES SATELITES — degrau em nivel absoluto, no copado com pergola")
print("=" * 88)
print()

# universo para a nula de vizinhanca: pomar com pergola, longe dos focos
UNIV = POMAR & COM & (dfoco > 120) & ~ZONA0
iy, ix = np.where(UNIV)
print("universo da distribuicao nula: %d celulas (%.2f ha) a mais de 120 m "
      "de qualquer foco" % (UNIV.sum(), UNIV.sum() / 100.))
print()

saida = {"satelites": [], "n_nula": NNULA}
print("%-28s %6s %6s %9s %9s %9s %8s"
      % ("satelite", "cel", "ha", "dist foco", "degrau", "p perm", "perc.nula"))

for nome, e, n_, ha_pub in SAT:
    # disco do raio que reproduz a area publicada
    raio = float(np.sqrt(ha_pub * 10000.0 / np.pi))
    m = (((EE - e) ** 2 + (NN - n_) ** 2) <= raio ** 2) & POMAR
    mc = m & COM
    alvo = mc if mc.sum() >= 8 else m
    usou_com = mc.sum() >= 8
    if alvo.sum() < 4:
        print("%-28s  fora do poligono do pomar — nao avaliavel" % nome)
        continue
    v = serie(alvo)
    d = degrau(v)
    p = perm_p(v)
    df = float(dfoco[alvo].mean())

    # nula de vizinhanca: NNULA discos do MESMO numero de celulas
    k = int(alvo.sum())
    nulos = []
    for _ in range(NNULA):
        j = RNG.integers(len(iy))
        cy, cx = iy[j], ix[j]
        dd = (EE - EE[cy, cx]) ** 2 + (NN - NN[cy, cx]) ** 2
        cand = np.where(UNIV, dd, np.inf).ravel()
        sel = np.argsort(cand)[:k]
        mm = np.zeros(POMAR.size, bool)
        mm[sel] = True
        nulos.append(degrau(serie(mm.reshape(ny, nx))))
    nulos = np.array(nulos)
    perc = float(100.0 * np.mean(nulos <= d))
    passa = (d < 0) and (perc <= 5.0)
    print("%-28s %6d %6.2f %8.0f m %+9.4f %9.4f %7.1f %%  %s"
          % (nome, alvo.sum(), alvo.sum() / 100., df, d, p, perc,
             "PASSA" if passa else "NAO PASSA"))
    saida["satelites"].append(dict(
        nome=nome, e=e, n=n_, ha_publicada=ha_pub, celulas=int(alvo.sum()),
        so_com_pergola=bool(usou_com), dist_foco=df, degrau=d, p_perm=p,
        percentil_nula=perc, passa=bool(passa),
        nula_p05=float(np.percentile(nulos, 5)),
        nula_mediana=float(np.median(nulos)),
        serie=[float(x) for x in v]))

print()
print("PARA COMPARAR, no mesmo calculo:")
CTRL = POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF
vc = serie(CTRL)
print("  %-26s %6d %6.2f %18s %+9.4f %9.4f"
      % ("resto do pomar (controlo)", CTRL.sum(), CTRL.sum() / 100., "",
         degrau(vc), perm_p(vc)))
vz = serie(ZONA0 & COM)
print("  %-26s %6d %6.2f %18s %+9.4f %9.4f"
      % ("foco ORIENTAL com pergola", (ZONA0 & COM).sum(),
         (ZONA0 & COM).sum() / 100., "", degrau(vz), perm_p(vz)))

print()
print("=" * 88)
print("VEREDICTO")
print("=" * 88)
n_passa = sum(1 for s in saida["satelites"] if s["passa"])
print()
for s in saida["satelites"]:
    print("  %-28s %s  (degrau %+.4f, percentil %.1f %% da nula de vizinhanca)"
          % (s["nome"], "PASSA" if s["passa"] else "NAO PASSA",
             s["degrau"], s["percentil_nula"]))
print()
if n_passa == len(saida["satelites"]) and n_passa > 0:
    print("Os tres passam. Sao a unica prova de propagacao nao contigua do")
    print("caso, e a P12 desenha-os com a nula de vizinhanca ao lado.")
elif n_passa == 0:
    print("Nenhum passa. A afirmacao «as frentes ja sairam das manchas»")
    print("sai da apresentacao, e a lista de RETIRADO passa a catorze.")
else:
    print("Passam %d de %d. Desenham-se so os que passam, e diz-se quantos" %
          (n_passa, len(saida["satelites"])))
    print("foram testados — nunca so os sobreviventes sem o denominador.")
saida["n_passa"] = n_passa

json.dump(saida, open(os.path.join(VG, "satelites_degrau.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito satelites_degrau.json")
