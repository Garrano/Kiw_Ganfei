# -*- coding: utf-8 -*-
"""C1-04 — o terreno difere entre os dois focos, e entre eles e o resto?

Unidades de comparacao, todas geograficas e nenhuma derivada de NDVI:
  * disco de 90 m centrado em cada foco (R2 G34), intersectado com o pomar —
    definicao simetrica, mesma regra para os dois;
  * `zona0` de masks_geograficas.json (202 celulas) = o poligono antigo do
    foco ESTE, mantido para continuidade;
  * `saudavel` (110 celulas da rede sistematica) = referencia;
  * resto do pomar.

Controlo obrigatorio: o foco OESTE cai no voo de Ago/2025 e o ESTE no de
Jan/2026 (c1_02). Toda a estatistica de micro-relevo e repetida dentro de cada
campanha, para separar terreno de artefacto de voo.
"""
import os, sys, json
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

g = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))
masc, meta = carrega_mascaras()
pomar, saud, zona0, nu2021 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(pomar)
resto = pomar & ~do & ~de

E29, N29 = centros_celulas()

print("=== ancoras de area (controlo 2) ===")
for k, m in (("pomar", pomar), ("saudavel", saud), ("zona0", zona0), ("nu2021", nu2021)):
    print("  %-9s %5d celulas = %5.2f ha" % (k, m.sum(), m.sum() / 100))
print("  disco OESTE %d cel = %.2f ha | disco ESTE %d cel = %.2f ha"
      % (do.sum(), do.sum() / 100, de.sum(), de.sum() / 100))
print("  centroide zona0: E%.0f N%.0f  (foco ESTE declarado E%.0f N%.0f)"
      % (E29[zona0].mean(), N29[zona0].mean(), *FOCO_ESTE))

GRUPOS = [("foco OESTE (disco 90 m)", do), ("foco ESTE (disco 90 m)", de),
          ("zona0 (poligono, =foco ESTE)", zona0),
          ("referencia sistematica", saud), ("resto do pomar", resto),
          ("pomar inteiro", pomar)]

campos = ["cota", "declive", "tpi", "res150", "rug25", "cota_dp"]
print("\n=== terreno por unidade (medianas; celulas de 10 m) ===")
cab = "%-30s %5s " % ("unidade", "n") + " ".join("%9s" % c for c in campos) + " %8s" % "expos."
print(cab)
res = {}
for nome, m in GRUPOS:
    v = [np.nanmedian(g[c][m]) for c in campos]
    sx = np.nanmean(np.sin(np.radians(g["exposicao"][m])))
    cx = np.nanmean(np.cos(np.radians(g["exposicao"][m])))
    az = np.degrees(np.arctan2(sx, cx)) % 360
    res[nome] = dict(n=int(m.sum()), **{c: float(np.nanmedian(g[c][m])) for c in campos},
                     exposicao=float(az))
    print("%-30s %5d " % (nome, m.sum()) + " ".join("%9.3f" % x for x in v) + " %8.0f" % az)

# percentil da cota de cada foco dentro do pomar
cp = g["cota"][pomar]
for nome, m in (("foco OESTE", do), ("foco ESTE", de), ("zona0", zona0), ("referencia", saud)):
    q = 100 * (cp < np.nanmedian(g["cota"][m])).mean()
    print("  percentil da cota de %-12s no pomar: %5.1f" % (nome, q))

# ---- testes formais oeste vs este, e cada foco vs referencia ----
print("\n=== testes (Mann-Whitney bilateral, celulas de 10 m) ===")
def mw(a, b):
    a = a[~np.isnan(a)]; b = b[~np.isnan(b)]
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return np.median(a) - np.median(b), p
for c in campos:
    d1, p1 = mw(g[c][do], g[c][de])
    d2, p2 = mw(g[c][do], g[c][saud])
    d3, p3 = mw(g[c][de], g[c][saud])
    print("%-8s OESTE-ESTE %+8.3f p=%.1e | OESTE-ref %+8.3f p=%.1e | ESTE-ref %+8.3f p=%.1e"
          % (c, d1, p1, d2, p2, d3, p3))

# ---- CONTROLO DE CAMPANHA: a rugosidade depende do voo? ----
print("\n=== controlo de campanha (o micro-relevo e do terreno ou do voo?) ===")
camp = g["campanha"]
puro_ago = pomar & (camp < 0.01)
puro_jan = pomar & (camp > 0.99)
print("pomar em voo Ago/2025: %d cel | Jan/2026: %d cel | misto: %d"
      % (puro_ago.sum(), puro_jan.sum(), (pomar & ~puro_ago & ~puro_jan).sum()))
for c in ("rug25", "cota_dp", "declive"):
    d, p = mw(g[c][puro_ago], g[c][puro_jan])
    print("  %-8s mediana Ago %.4f | Jan %.4f | dif %+.4f  p=%.1e"
          % (c, np.nanmedian(g[c][puro_ago]), np.nanmedian(g[c][puro_jan]), d, p))
print("  foco OESTE em campanha:", np.unique(np.round(camp[do], 2)))
print("  foco ESTE  em campanha:", np.unique(np.round(camp[de], 2)))

# rugosidade dos focos contra a referencia DA MESMA CAMPANHA
for nome, m in (("foco OESTE", do), ("foco ESTE", de)):
    mesma = puro_ago if nome.endswith("OESTE") else puro_jan
    ref = saud & mesma
    if ref.sum() >= 10:
        d, p = mw(g["rug25"][m], g["rug25"][ref])
        print("  rug25 %-11s vs referencia da MESMA campanha (n=%d): %+.4f  p=%.1e"
              % (nome, ref.sum(), d, p))
    else:
        print("  rug25 %-11s: referencia da mesma campanha tem so %d celulas — nao testavel"
              % (nome, ref.sum()))

# ---- o chao lavrado de 2021 ----
print("\n=== nu2021 (chao lavrado na ortofoto de 2021, 1,67 ha) ===")
print("  celulas: %d | dentro do disco OESTE: %d | dentro do disco ESTE: %d | zona0: %d"
      % (nu2021.sum(), (nu2021 & do).sum(), (nu2021 & de).sum(), (nu2021 & zona0).sum()))
print("  fraccao do disco OESTE lavrada: %.1f%% | do disco ESTE: %.1f%% | da referencia: %.1f%%"
      % (100 * (nu2021 & do).sum() / do.sum(), 100 * (nu2021 & de).sum() / de.sum(),
         100 * (nu2021 & saud).sum() / max(saud.sum(), 1)))
for c in campos:
    d, p = mw(g[c][nu2021 & pomar], g[c][pomar & ~nu2021])
    print("  %-8s lavrado-nao lavrado %+8.3f  p=%.1e" % (c, d, p))

json.dump(res, open(os.path.join(SAIDA, "c1_04_terreno_por_unidade.json"), "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito c1_04_terreno_por_unidade.json")
