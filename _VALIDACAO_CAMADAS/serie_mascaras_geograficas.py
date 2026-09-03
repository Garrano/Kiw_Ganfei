# -*- coding: utf-8 -*-
"""Re-execucao integral da serie com as mascaras GEOGRAFICAS.

Substitui todos os numeros por mascara produzidos com `masks.json`, que era
circular: `pomar` = NDVI 2026 > 0,78 e `manchaW` = NDVI 2026 < 0,76, apesar de
o cabecalho do script que as gerou afirmar o contrario.

Duas decisoes de metodo, tomadas depois de arbitrar a divergencia entre a
sessao de re-derivacao e a sessao principal:

1. A GRANDEZA. Havia duas em uso e davam respostas opostas.
   - Fraccao de pixeis abaixo de (referencia - 0,05): SATURA. A Zona 0 chega a
     100% em 2026 nos dois conjuntos de mascaras, o declive fica preso pelo
     tecto e a medida deixa de distinguir seja o que for. Nao serve.
   - Magnitude, referencia menos media da mascara: nao satura, e e nela que a
     circularidade se ve. E esta a grandeza operativa.
   A fraccao continua reportada, mas como descritivo, nunca como teste.

2. O ABSOLUTO. A magnitude e uma DIFERENCA, e a referencia nova esta ela
   propria a descer (-0,00395/ano). Um fosso constante com uma referencia que
   desce significa que as duas descem juntas — o que e uma afirmacao
   completamente diferente de "esta mancha declina". Por isso reporta-se
   sempre o par: o fosso E o nivel absoluto.
"""
import json
import numpy as np
import rasterio
from matplotlib.path import Path as MP
from scipy import stats, ndimage

AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])

g = json.load(open("sentinel/masks_geograficas.json"))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0, NU21 = (bits("pomar_bits"), bits("saudavel_bits"),
                           bits("zona0_bits"), bits("nu2021_bits"))
nd = {d: rasterio.open("sentinel/%s.tif" % d).read(1) for d in DATAS}


def tend(v):
    r = stats.linregress(anos, v)
    return r.slope, r.pvalue


print("=" * 78)
print("NIVEL ABSOLUTO DE NDVI  (nao e diferenca — nao depende da referencia)")
print("=" * 78)
Z0_LIMPA = ZONA0 & ~NU21          # Zona 0 sem o solo lavrado de 2021
alvos = [("referencia sistematica", REF), ("pomar inteiro", POMAR),
         ("Zona 0", ZONA0), ("Zona 0 sem solo nu 2021", Z0_LIMPA)]
print("\n%-26s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
guardado = {}
for nome, m in alvos:
    v = np.array([float(np.nanmean(nd[d][m])) for d in DATAS])
    guardado[nome] = v
    s, p = tend(v)
    print("%-26s %s   declive %+.5f/ano  p=%.4f"
          % (nome, "  ".join("%.3f" % x for x in v), s, p))

print("\n" + "=" * 78)
print("FOSSO ATE A REFERENCIA  (a grandeza operativa)")
print("=" * 78)
for nome, m in alvos[2:]:
    v = guardado["referencia sistematica"] - guardado[nome]
    s, p = tend(v)
    print("%-26s %s   declive %+.5f/ano  p=%.4f"
          % (nome, "  ".join("%.3f" % x for x in v), s, p))

print("\n" + "=" * 78)
print("MANCHAS QUE EMERGEM DO MAPA DE DEFICE  (nenhuma mascara as define)")
print("=" * 78)
for d in DATAS:
    ref = float(np.nanmean(nd[d][REF]))
    dfc = ndimage.binary_opening((nd[d] < ref - 0.05) & POMAR, np.ones((2, 2)))
    lab, n = ndimage.label(dfc, np.ones((3, 3)))
    nucs = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 15:
            continue
        ys, xs = np.where(m)
        nucs.append((m.sum() / 100, AOI[0] + xs.mean() * 10))
    nucs.sort(reverse=True)
    print("%s  defice %5.2f ha (%4.1f%% do pomar) | nucleos>=0,15 ha: %s"
          % (d, dfc.sum() / 100, 100 * dfc.sum() / POMAR.sum(),
             "  ".join("%.2f ha@E%.0f" % x for x in nucs[:4]) or "nenhum"))
print("""
NOTA. O nucleo ocidental (E~530480) so aparece em 2025-2026. Nas mascaras
antigas ele estava DEFINIDO desde o inicio, porque `manchaW` era o NDVI baixo
de 2026 — nao podia deixar de la estar. Aqui ele tem de aparecer sozinho, e
aparece: e a verificacao mais forte do dossie.
""")
