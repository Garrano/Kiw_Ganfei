# -*- coding: utf-8 -*-
"""D2 accao 3 — a serie do disco ORIENTAL restrita as celulas COM pergola.

A pergunta, fixada antes de correr
----------------------------------
O numero mais forte da apresentacao e o declive do fosso a referencia na
«Zona 0 sem solo nu 2021»: +0,01103/ano, p = 0,0162. A mascara `nu2021` vem
da ORTOFOTO de 2021 e so sabe distinguir solo lavrado de solo nao lavrado.

O LiDAR de 06-07-2025 mede outra coisa: se ha ou nao ESTRUTURA acima do chao.
E diz que 50,2 % do disco oriental esta abaixo de 0,5 m, e que 22,7 % do que
a `nu2021` deixava passar como plantado nao tem pergola nenhuma.

Se metade do disco oriental nao tem pomar, o declive de +0,01103 mede uma
coisa mista: parte declinio de planta viva, parte chao que nunca teve planta
ou de onde ela ja saiu.

HIPOTESE FIXA, falsificavel, escrita antes de ver o resultado:
    H : o declive positivo do fosso no disco oriental SOBREVIVE quando se
        restringe as celulas com estrutura acima de 0,5 m no LiDAR de 2025.
    Criterio de sobrevivencia, fixado a priori: declive > 0 e p < 0,05.

Se H se confirma, o numero passa a ser publicavel sozinho. Se H cai, o
resultado e MAIS interessante: o «foco cronico» era em boa parte falha de
instalacao, e a historia de doenca e a do foco ocidental. Os dois desfechos
sao reportaveis; nenhum e mau.

Metodo — identico a `serie_mascaras_geograficas.py`, so muda a mascara
--------------------------------------------------------------------
Mesma grelha, mesmas nove datas de plena estacao, mesma grandeza (fosso =
referencia da propria cena menos media da unidade), mesma regressao. A unica
alteracao e o criterio que separa planta de chao. Assim os numeros sao
comparaveis linha a linha com o que ja esta publicado.

Multiverso: o limiar de altura e uma ESCOLHA. Corre-se a cinco limiares e
reporta-se a distribuicao, nao a corrida preferida.

RESSALVA DE PROVENIENCIA. O centro do disco OCIDENTAL (E530485) foi lido de
onde o defice de 2026 esta. Uma serie calculada dentro dele NAO e prova
independente de que ali aconteceu alguma coisa — a prova independente e a
emergencia dos nucleos sem mascara nenhuma. O disco ocidental entra aqui so
como contraste de altura de copado, nao como teste.
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
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])

FOCO_OCIDENTAL = (530485.0, 4655053.0)
FOCO_ORIENTAL = (530977.0, 4655117.0)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))


def bits(k):
    return np.array([[c == "1" for c in L] for L in g[k]], bool)


POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
ZONA0, NU21 = bits("zona0_bits"), bits("nu2021_bits")
nd = {d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}
h = np.load(os.path.join(VG, "chm_altura.npy"))

ny, nx = POMAR.shape
E = AOI[0] + (np.arange(nx) + 0.5) * 10.0
N = AOI[3] - (np.arange(ny) + 0.5) * 10.0
EE, NN = np.meshgrid(E, N)


def disco(c, r=90.0):
    return ((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r ** 2


DOC = disco(FOCO_OCIDENTAL) & POMAR
DOR = disco(FOCO_ORIENTAL) & POMAR
FIN = np.isfinite(h)


def tend(v):
    r = stats.linregress(anos, v)
    return float(r.slope), float(r.pvalue)


def fosso(m, ref=None):
    """Fosso a referencia, cena a cena. Referencia inalterada por comparabilidade."""
    R = REF if ref is None else ref
    return np.array([float(np.nanmean(nd[d][R]) - np.nanmean(nd[d][m]))
                     for d in DATAS])


def nivel(m):
    return np.array([float(np.nanmean(nd[d][m])) for d in DATAS])


saida = {"hipotese": "declive do fosso no disco oriental sobrevive a restricao "
                     "COM pergola; criterio a priori b>0 e p<0,05",
         "datas": DATAS}

print("=" * 84)
print("O QUE O LiDAR ENCONTRA EM CADA UNIDADE")
print("=" * 84)
print("%-40s %7s %9s %9s %9s" % ("", "ha", "altura", "%<0,5 m", "%>1,5 m"))
UN0 = [("pomar inteiro", POMAR),
       ("referencia sistematica", REF),
       ("Zona 0 (disco oriental da C2)", ZONA0),
       ("Zona 0 sem solo nu 2021  <-- publicado", ZONA0 & ~NU21),
       ("disco ORIENTAL 90 m  E530977", DOR),
       ("disco OCIDENTAL 90 m  E530485", DOC)]
saida["unidades"] = {}
for n_, m in UN0:
    k = m & FIN
    hm = float(np.median(h[k])) if k.any() else float("nan")
    ps = float(100 * np.mean(h[k] < 0.5)) if k.any() else float("nan")
    pa = float(100 * np.mean(h[k] > 1.5)) if k.any() else float("nan")
    print("%-40s %7.2f %7.2f m %8.1f %% %8.1f %%"
          % (n_, m.sum() / 100.0, hm, ps, pa))
    saida["unidades"][n_] = dict(ha=m.sum() / 100.0, altura_mediana=hm,
                                 pct_sem=ps, pct_alto=pa)

print()
print("=" * 84)
print("O TESTE — fosso a referencia, o mesmo calculo, so muda a mascara")
print("=" * 84)
print()
print("%-40s %s" % ("", "  ".join(d[2:7] for d in DATAS)))

COM05 = FIN & (h >= 0.5)
SEM05 = FIN & (h < 0.5)
ALVOS = [
    ("Zona 0 sem solo nu 2021  (PUBLICADO)", ZONA0 & ~NU21),
    ("Zona 0 COM pergola  (>=0,5 m)", ZONA0 & COM05),
    ("Zona 0 SEM pergola  (<0,5 m)", ZONA0 & SEM05),
    ("Zona 0 sem nu2021 E com pergola", ZONA0 & ~NU21 & COM05),
    ("disco ORIENTAL COM pergola", DOR & COM05),
    ("disco ORIENTAL SEM pergola", DOR & SEM05),
    ("disco OCIDENTAL COM pergola", DOC & COM05),
    ("resto do pomar COM pergola", POMAR & COM05 & ~DOR & ~DOC & ~REF),
]
res = {}
for n_, m in ALVOS:
    if m.sum() < 10:
        print("%-40s  menos de 10 celulas, nao se corre" % n_)
        continue
    f = fosso(m)
    b, p = tend(f)
    a = nivel(m)
    ba, pa = tend(a)
    res[n_] = dict(ha=m.sum() / 100.0, fosso=[float(v) for v in f],
                   b=b, p=p, nivel=[float(v) for v in a],
                   b_nivel=ba, p_nivel=pa)
    print("%-40s %s   %+.5f/ano  p=%.4f%s"
          % (n_, "  ".join("%.3f" % v for v in f), b, p,
             "  *" if p < 0.05 else ""))
saida["fosso"] = res

print()
print("NIVEL ABSOLUTO nas mesmas unidades (nao depende da referencia)")
print()
print("%-40s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
for n_ in res:
    print("%-40s %s   %+.5f/ano  p=%.4f"
          % (n_, "  ".join("%.3f" % v for v in res[n_]["nivel"]),
             res[n_]["b_nivel"], res[n_]["p_nivel"]))

print()
print("=" * 84)
print("MULTIVERSO DO LIMIAR — o limiar de altura e uma escolha, nao um facto")
print("=" * 84)
print()
print("%-8s %9s %12s %9s %12s %9s"
      % ("limiar", "Z0 ha", "b Z0 com", "p", "b ORI com", "p"))
mv = {}
for lim in (0.3, 0.5, 1.0, 1.5, 2.0):
    C = FIN & (h >= lim)
    z, o = ZONA0 & C, DOR & C
    if z.sum() < 10 or o.sum() < 10:
        print("%-8.1f %9.2f   a unidade esvazia-se" % (lim, z.sum() / 100.0))
        continue
    bz, pz = tend(fosso(z))
    bo, po = tend(fosso(o))
    mv["%.1f" % lim] = dict(ha_z=z.sum() / 100.0, b_z=bz, p_z=pz,
                            ha_o=o.sum() / 100.0, b_o=bo, p_o=po)
    print("%-8.1f %9.2f %+12.5f %9.4f %+12.5f %9.4f"
          % (lim, z.sum() / 100.0, bz, pz, bo, po))
saida["multiverso_limiar"] = mv

print()
print("=" * 84)
print("SENSIBILIDADE DA REFERENCIA — e se a propria referencia se restringir")
print("=" * 84)
REFC = REF & COM05
print("referencia inteira %.2f ha  |  referencia com pergola %.2f ha"
      % (REF.sum() / 100.0, REFC.sum() / 100.0))
saida["ref_restrita"] = {}
for n_, m in [("Zona 0 COM pergola", ZONA0 & COM05),
              ("disco ORIENTAL COM pergola", DOR & COM05)]:
    b2, p2 = tend(fosso(m, ref=REFC))
    print("%-40s %+.5f/ano  p=%.4f  (ref restrita)" % (n_, b2, p2))
    saida["ref_restrita"][n_] = dict(b=b2, p=p2)

print()
print("=" * 84)
print("VEREDICTO SOBRE A HIPOTESE FIXADA")
print("=" * 84)
k = "Zona 0 COM pergola  (>=0,5 m)"
if k in res:
    b, p = res[k]["b"], res[k]["p"]
    ok = bool(b > 0 and p < 0.05)
    pb = res["Zona 0 sem solo nu 2021  (PUBLICADO)"]
    print()
    print("Zona 0 restrita a celulas com pergola:  b = %+.5f/ano   p = %.4f"
          % (b, p))
    print("criterio a priori (b>0 e p<0,05):       %s"
          % ("CUMPRIDO" if ok else "NAO CUMPRIDO"))
    print("publicado (nu2021):                     b = %+.5f/ano   p = %.4f"
          % (pb["b"], pb["p"]))
    print("razao dos declives:                     %.2f"
          % (b / pb["b"] if pb["b"] else float("nan")))
    saida["veredicto"] = dict(b=b, p=p, cumprido=ok,
                              b_publicado=pb["b"], p_publicado=pb["p"])

json.dump(saida, open(os.path.join(VG, "serie_oriental_pergola.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito serie_oriental_pergola.json")
