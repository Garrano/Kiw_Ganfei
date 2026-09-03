# -*- coding: utf-8 -*-
"""Refazer por POSTO — invariante a qualquer transformacao monotona.

Porque se refaz
---------------
A primeira passagem corrigiu a diferenca entre as duas ortofotos subtraindo
uma constante (a deriva mediana da referencia, +0,2844). Isso pressupoe que a
relacao entre as duas imagens e aditiva, e nao e: a referencia passa de 0,0449
para 0,3293, um factor de sete. A calibracao contra solo nu denunciou-o ao
devolver «-137 % acima do chao», que e impossivel.

O que e valido comparar entre duas imagens de radiometria e nitidez diferentes
e a POSICAO RELATIVA de cada unidade dentro da sua propria imagem. O posto
percentual e invariante a qualquer transformacao monotona — aditiva,
multiplicativa, gama, o que for.

A pergunta passa a ser: em 2021, onde estava o declinio novo na ordenacao do
pomar? E em 2025, onde esta?
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
NU21 = masc["nu2021"] & POMAR
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool)
d26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)
do, de = discos_dos_focos(POMAR)
A = np.load(os.path.join(AQUI, "prom_2021.npy"))
B = np.load(os.path.join(AQUI, "prom_2025.npy"))
val = np.isfinite(A) & np.isfinite(B)
print("celulas medidas nas duas ortofotos: %d (%.2f ha)"
      % (val.sum(), val.sum() / 100.0))

UNID = [("declinio NOVO 2026", novo & POMAR),
        ("foco OESTE", do & POMAR),
        ("foco ESTE plantado", de & POMAR & ~NU21),
        ("resto do pomar", POMAR & ~d26 & ~REF),
        ("referencia", REF),
        ("nu2021 lavrado em 2021", NU21)]


def postos(M):
    r = np.full(M.shape, np.nan)
    v = M[val]
    r[val] = stats.rankdata(v) / v.size * 100.0
    return r


RA, RB = postos(A), postos(B)
print("\nPOSTO PERCENTUAL DENTRO DA PROPRIA IMAGEM (mediana da unidade)")
print("100 = a celula mais periodica medida nessa ortofoto\n")
print("   %-24s %8s %8s %9s" % ("", "2021", "2025", "variacao"))
out = {}
for nome, m in UNID:
    k = m & val
    if k.sum() < 10:
        continue
    a, b = float(np.median(RA[k])), float(np.median(RB[k]))
    w = stats.wilcoxon(RB[k] - RA[k])
    out[nome] = dict(n=int(k.sum()), posto2021=a, posto2025=b,
                     variacao=b - a, p=float(w.pvalue))
    print("   %-24s %7.1f  %7.1f   %+7.1f   (n=%d, p=%.3g)"
          % (nome, a, b, b - a, k.sum(), w.pvalue))

# o chao do instrumento em cada imagem, medido em terreno sabidamente sem
# fileiras em 2021
kn = NU21 & val
print("\nCHAO em 2021 (terreno lavrado, sem copado): posto %.1f"
      % np.median(RA[kn]))
print("Se uma unidade em 2025 cair a esse posto, nao tem fileiras.")
print("Se ficar claramente acima, a estrutura esta la e o copado rareou.")
json.dump(out, open(os.path.join(AQUI, "postos.json"), "w"), indent=1)
