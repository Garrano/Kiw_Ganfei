# -*- coding: utf-8 -*-
"""Quanto le o SOLO NU? — a escala que faltava.

Perda de periodicidade nao separa arranque de desfolha: as duas destroem o
padrao de 5 m. Sem saber o que le terreno sabidamente sem fileiras, o valor
-0,1362 nao tem escala.

Calibra-se com a mascara `nu2021` — terreno lavrado, sem copado, identificado
na ortofoto de 2021 e ja usado pela cadeia como tal. Da o CHAO do instrumento
na propria imagem de 2021.

E imprime-se a fraccao do caminho ate esse chao que cada unidade percorreu.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
NU21 = masc["nu2021"] & POMAR
novo = np.load(os.path.join(SAIDA, "c2_05_novo_m2.npy")).astype(bool)
defice26 = np.load(os.path.join(SAIDA, "c2_05_defice_2026.npy")).astype(bool)
do, de = discos_dos_focos(POMAR)
A = np.load(os.path.join(AQUI, "prom_2021.npy"))
B = np.load(os.path.join(AQUI, "prom_2025.npy"))

# o chao: terreno lavrado sem copado, medido na ortofoto de 2021
k = NU21 & np.isfinite(A)
if k.sum() < 10:
    print("nu2021 fora do alvo medido — recalcular com nu2021 incluido")
    sys.exit(1)
chao21 = float(np.median(A[k]))
tecto21 = float(np.median(A[REF & np.isfinite(A)]))
print("ESCALA na ortofoto de 2021, no proprio instrumento")
print("   chao   solo lavrado sem copado (nu2021, %.2f ha) : %.4f"
      % (k.sum() / 100.0, chao21))
print("   tecto  referencia sistematica                    : %.4f" % tecto21)
print("   amplitude util                                   : %.4f"
      % (tecto21 - chao21))

dref = float(np.median(B[REF & np.isfinite(A) & np.isfinite(B)]
                       - A[REF & np.isfinite(A) & np.isfinite(B)]))
print("\nEM 2025, corrigido da deriva de captacao (%+.4f)" % dref)
print("Fraccao da amplitude util que cada unidade perdeu desde 2021.")
print("100 %% = desceu ate ao nivel do solo lavrado.\n")
UNID = [("declinio NOVO 2026", novo & POMAR),
        ("foco OESTE", do & POMAR),
        ("foco ESTE plantado", de & POMAR & ~NU21),
        ("resto do pomar", POMAR & ~defice26 & ~REF),
        ("referencia", REF)]
out = dict(chao_nu2021=chao21, tecto_ref2021=tecto21, deriva=dref, unidades={})
for nome, m in UNID:
    kk = m & np.isfinite(A) & np.isfinite(B)
    if kk.sum() < 10:
        continue
    a = float(np.median(A[kk]))
    b = float(np.median(B[kk])) - dref
    frac = (a - b) / (tecto21 - chao21) * 100.0
    acima = (b - chao21) / (tecto21 - chao21) * 100.0
    out["unidades"][nome] = dict(n=int(kk.sum()), p2021=a, p2025_corr=b,
                                 pct_amplitude_perdida=frac,
                                 pct_acima_do_chao=acima)
    print("   %-22s 2021 %+.4f -> 2025 %+.4f | perdeu %5.1f %% da amplitude"
          " | fica %5.1f %% acima do chao" % (nome, a, b, frac, acima))
print("""
LEITURA
   fica muito acima do chao  ->  a estrutura fisica esta la; o copado
                                 rareou. Compativel com fisiologia.
   fica ao nivel do chao     ->  nao ha fileiras. Arranque ou replantacao.""")
json.dump(out, open(os.path.join(AQUI, "escala_nu.json"), "w"), indent=1)
