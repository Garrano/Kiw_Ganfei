# -*- coding: utf-8 -*-
"""O que a contaminacao da referencia revelou: um gradiente com a distancia.

Como se chegou aqui
-------------------
Ao verificar se a referencia sistematica dava degrau proprio (dava: -0,048 em
2025-26, p = 0,026), descobriu-se porque: **44,5 % das celulas da grelha de
referencia estao a menos de 150 m de um centro de foco, e cinco delas estao
dentro da propria Zona 0.** A celula mais proxima esta a 10 m do centro.

Separadas por distancia, as duas metades da referencia nao se parecem nada:

    referencia a MAIS de 150 m dos focos   degrau  -0,016   (n=61)
    referencia a MENOS de 150 m dos focos  degrau  -0,075   (n=42)

Isto tem tres consequencias, e nenhuma delas estava escrita em lado nenhum:

1. **Nao houve evento de area.** A parte limpa da referencia nao se mexe
   (-0,016), e o resto do pomar tambem nao (-0,014). O «degrau da referencia»
   era os focos a entrar na referencia.

2. **A grandeza «fosso a referencia» tem vindo a SUBESTIMAR os focos**, porque
   a referencia desce com eles. Todos os numeros publicados nessa moeda sao
   conservadores. Isso reforca o caso; nao o enfraquece.

3. **O evento de 2025-26 nao esta confinado aos dois discos.** Ha 42 celulas
   escolhidas em 2010-2012 como pergola sa, numa grelha regular, a 20 m ou
   mais de qualquer bordo — e cairam 0,075. Nao dentro dos focos: ao pe deles.

Um gradiente com a distancia e o discriminador mais forte que este dossie tem
para separar hipoteses. Um agente biotico que se propaga produz decaimento com
a distancia. Uma decisao de gestao, uma avaria de rega ou uma propriedade de
solo nao tem por que produzir.

O TESTE, fixado antes de correr
-------------------------------
Sobre TODAS as celulas do pomar com pergola em 06-07-2025, fora dos dois
discos de 90 m e fora da Zona 0, em aneis de distancia ao centro:

    H0 : o degrau de 2025-26 nao depende da distancia ao foco.
    H1 : o degrau e tanto maior quanto menor a distancia.

Estatistica: correlacao de Spearman entre distancia da celula e degrau da
celula, com p por permutacao espacial em BLOCOS (o vizinho de uma celula nao
e independente dela; permutar celula a celula da p a mais).

PROVENIENCIA, e determina o que se pode concluir
------------------------------------------------
O centro ORIENTAL e o centroide da Zona 0, poligono geografico vindo de
ficheiro antigo e independente de qualquer NDVI. **O gradiente medido a partir
dele e limpo.**

O centro OCIDENTAL foi lido de onde esta o defice de 2026. Um gradiente
medido a partir dele esta parcialmente construido pela propria escolha do
centro, e por isso corre-se, reporta-se, e NAO se conclui dele. Fica como
descritivo.
"""
import json
import os

import numpy as np
import rasterio
from scipy import stats

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
TARDIO = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
nd = np.stack([rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
               for d in DATAS])
h = np.load(os.path.join(VG, "chm_altura.npy"))

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)

# centro oriental = centroide da Zona 0, geografico
C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)          # lido do sinal — descritivo apenas
print("centro ORIENTAL (centroide da Zona 0, geografico): E%.0f N%.0f" % C_OR)
print("centro OCIDENTAL (lido do defice de 2026)        : E%.0f N%.0f" % C_OC)

COM = np.isfinite(h) & (h >= 0.5)
dOR = np.hypot(EE - C_OR[0], NN - C_OR[1])
dOC = np.hypot(EE - C_OC[0], NN - C_OC[1])

# degrau por celula: media 2025-26 menos media 2017-2024
deg = np.nanmean(nd[TARDIO], 0) - np.nanmean(nd[~TARDIO], 0)

# universo: pomar com pergola, FORA dos dois discos e fora da Zona 0
FORA = POMAR & COM & ~ZONA0 & (dOR > 90) & (dOC > 90) & np.isfinite(deg)
print("\ncelulas no universo do teste: %d  (%.2f ha)" % (FORA.sum(), FORA.sum() / 100.))

RNG = np.random.default_rng(20260831)


def p_toroidal(campo, dist, mask, nb=2000):
    """p por deslocamento TOROIDAL do campo de degrau contra o de distancia.

    Permutar celula a celula da p a menos: as celulas vizinhas nao sao
    independentes e uma permutacao livre destroi a autocorrelacao, o que torna
    quase qualquer rho «significativo». O deslocamento toroidal roda o campo
    inteiro, portanto PRESERVA a sua estrutura espacial e destroi apenas o
    alinhamento com a distancia — que e exactamente a hipotese nula que
    interessa.
    """
    d = dist[mask]
    obs = abs(stats.spearmanr(d, campo[mask]).statistic)
    ny_, nx_ = campo.shape
    c = 0
    for _ in range(nb):
        dy = int(RNG.integers(1, ny_))
        dx = int(RNG.integers(1, nx_))
        r = np.roll(np.roll(campo, dy, 0), dx, 1)[mask]
        k = np.isfinite(r)
        if k.sum() < 30:
            continue
        if abs(stats.spearmanr(d[k], r[k]).statistic) >= obs:
            c += 1
    return (c + 1) / (nb + 1.)


print("\n" + "=" * 80)
print("ANEIS DE DISTANCIA — degrau medio do copado, por anel")
print("=" * 80)
saida = {"centro_oriental": C_OR, "centro_ocidental": C_OC, "aneis": {}}
for nome, dist, limpo in (("ORIENTAL (geografico — conclusivo)", dOR, True),
                          ("OCIDENTAL (centro do sinal — descritivo)", dOC, False)):
    print("\n%s" % nome)
    print("%-14s %6s %10s %10s" % ("anel", "n", "degrau", "desv.pad"))
    linhas = []
    for lo, hi in ((90, 150), (150, 250), (250, 400), (400, 700), (700, 2000)):
        m = FORA & (dist > lo) & (dist <= hi)
        if m.sum() < 15:
            continue
        v = deg[m]
        print("%4d–%4d m %6d %+10.4f %10.4f" % (lo, hi, m.sum(), v.mean(), v.std()))
        linhas.append(dict(lo=lo, hi=hi, n=int(m.sum()), degrau=float(v.mean()),
                           dp=float(v.std())))
    d_, y_ = dist[FORA], deg[FORA]
    rho = stats.spearmanr(d_, y_)
    p_bl = p_toroidal(deg, dist, FORA)
    print("Spearman rho = %+.4f   p ingenuo = %.2e   p toroidal = %.4f"
          % (rho.statistic, rho.pvalue, p_bl))
    saida["aneis"][nome] = dict(linhas=linhas, rho=float(rho.statistic),
                                p_ingenuo=float(rho.pvalue), p_toroidal=float(p_bl),
                                conclusivo=limpo)

json.dump(saida, open(os.path.join(VG, "halo_distancia.json"), "w"),
          indent=1, ensure_ascii=False)
print("\nescrito halo_distancia.json")
