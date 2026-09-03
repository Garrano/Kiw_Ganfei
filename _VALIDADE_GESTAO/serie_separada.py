# -*- coding: utf-8 -*-
"""A serie do defice, separada em duas: copado a definhar e chao limpo.

Porque se refaz
---------------
O LiDAR de 06-07-2025 mostra que 3,77 das 30,31 ha do poligono nao tinham
pergola nenhuma nessa data, e que 40,7 % do defice de 2026 cai nesse terreno.
A serie publicada — 8,08 (2017) / 4,05 (2020) / 2,91 (2024) / 5,43 (2025) /
7,86 (2026) ha — soma duas coisas que nao sao a mesma:

    copado a declinar      videira viva com menos folha
    chao limpo             videira arrancada; NDVI baixo por nao haver planta

Uma e um facto sanitario. A outra e uma decisao de gestao. Trata-las como uma
so grandeza foi o erro de validade que este caso carregava.

Sobre a circularidade — o ponto que importa
-------------------------------------------
A mascara que separa as duas vem do **LiDAR**, nao do NDVI. Isto e o oposto
exacto do erro de `fazer_masks_v2.py`, onde `pomar` era `nd2026 > 0,78` e se
media depois a evolucao ate 2026. Aqui o criterio e altura fisica medida por
um instrumento que nao ve reflectancia, num voo de 06-07-2025, e a serie que
se mede e de NDVI. Sao grandezas independentes.

Limite declarado, e nao e pequeno
---------------------------------
O LiDAR e **uma data**. Diz o que havia em 06-07-2025. Nao diz:
  - quando cada talhao foi limpo, so que foi antes dessa data;
  - se algum talhao foi limpo DEPOIS, ja em 2026 — e o de 2026 e precisamente
    o ano em causa. As 3,58 ha de declinio novo tinham pergola em Julho de
    2025, mas nada aqui prova que a mantiveram em Julho de 2026.
A separacao e portanto valida ate 06-07-2025 e uma hipotese depois disso.
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
h = np.load(os.path.join(AQUI, "chm_altura.npy"))

VIVO = POMAR & np.isfinite(h) & (h >= 0.5)
LIMPO = POMAR & np.isfinite(h) & (h < 0.5)
SEMDADOS = POMAR & ~np.isfinite(h)
print("particao do poligono pelo LiDAR de 06-07-2025, limiar 0,5 m")
print("  com pergola   %5.2f ha" % (VIVO.sum() / 100.0))
print("  sem pergola   %5.2f ha" % (LIMPO.sum() / 100.0))
print("  sem dados     %5.2f ha" % (SEMDADOS.sum() / 100.0))
print("  referencia sistematica dentro de 'com pergola': %d de %d celulas"
      % ((REF & VIVO).sum(), REF.sum()))

nd = carrega_ndvi(TODAS)
datas = sorted(nd)
print("\n%-12s %8s | %8s %8s %8s | %9s %9s"
      % ("data", "ref", "TOTAL", "pergola", "limpo", "fosso perg", "fosso limpo"))
print("%-12s %8s | %8s %8s %8s | %9s %9s"
      % ("", "", "ha", "ha", "ha", "NDVI", "NDVI"))
tab = {}
for d in datas:
    a = nd[d]
    r = float(np.nanmean(a[REF]))
    dt = mapa_defice(a, POMAR, r)
    # o defice recalculado DENTRO de cada subconjunto, com a mesma regra
    dv = mapa_defice(a, VIVO, r)
    dl = mapa_defice(a, LIMPO, r)
    fv = float(r - np.nanmean(a[VIVO & ~REF]))
    fl = float(r - np.nanmean(a[LIMPO])) if LIMPO.any() else np.nan
    tab[d] = dict(ref=r, total_ha=dt.sum() / 100.0, vivo_ha=dv.sum() / 100.0,
                  limpo_ha=dl.sum() / 100.0, fosso_vivo=fv, fosso_limpo=fl)
    print("%-12s %8.3f | %8.2f %8.2f %8.2f | %9.3f %9.3f"
          % (d, r, dt.sum() / 100.0, dv.sum() / 100.0, dl.sum() / 100.0, fv, fl))

json.dump(tab, open(os.path.join(AQUI, "serie_separada.json"), "w"), indent=1)

print("\n" + "=" * 74)
print("O QUE MUDA\n")
tot = np.array([tab[d]["total_ha"] for d in datas])
viv = np.array([tab[d]["vivo_ha"] for d in datas])
lim = np.array([tab[d]["limpo_ha"] for d in datas])
anos = np.array([int(d[:4]) for d in datas], float)
print("serie publicada (todo o poligono):")
print("   " + "  ".join("%d:%.2f" % (a, t) for a, t in zip(anos, tot)))
print("\nso onde havia pergola em 06-07-2025 (%.2f ha):" % (VIVO.sum() / 100.0))
print("   " + "  ".join("%d:%.2f" % (a, v) for a, v in zip(anos, viv)))
print("\nso onde NAO havia pergola (%.2f ha):" % (LIMPO.sum() / 100.0))
print("   " + "  ".join("%d:%.2f" % (a, l) for a, l in zip(anos, lim)))

for nome, s in (("TOTAL", tot), ("com pergola", viv), ("sem pergola", lim)):
    i24 = list(anos).index(2024.0) if 2024.0 in anos else None
    i26 = list(anos).index(2026.0) if 2026.0 in anos else None
    if i24 is None or i26 is None:
        continue
    r = stats.linregress(anos, s)
    print("\n%-12s 2024 %.2f -> 2026 %.2f  (%+.2f ha, x%.2f) | declive %+.3f ha/ano p=%.3f"
          % (nome, s[i24], s[i26], s[i26] - s[i24],
             s[i26] / s[i24] if s[i24] else np.nan, r.slope, r.pvalue))

print("""
A LEITURA
   'com pergola' e a serie sanitaria: videira viva, com mais ou menos folha.
   'sem pergola' nao e doenca: e terreno onde a planta foi retirada, e o NDVI
   baixo mede a ausencia da planta, nao o estado dela.""")
