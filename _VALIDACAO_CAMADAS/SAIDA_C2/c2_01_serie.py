# -*- coding: utf-8 -*-
"""C2-01 — reproducao da serie geografica e medicao da circularidade antiga.

Tres coisas:
  a) reproduzir `_serie_geografica.txt` valor a valor com as mascaras
     geograficas, para confirmar que esta camada esta a ler os mesmos objectos;
  b) medir quanto e que a circularidade do `masks.json` antigo valia, em NDVI,
     para o facto «era circular» deixar de ser adjectivo e passar a numero;
  c) escrever a serie completa (niveis absolutos, fossos, defice, fraccao) em
     JSON, para os scripts seguintes nao repetirem leitura de raster.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, meta = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
Z0_LIMPA = ZONA0 & ~NU21
nd = carrega_ndvi(TODAS)
anos = anos_decimais(DATAS)

print("=" * 78)
print("a) AREAS DAS MASCARAS GEOGRAFICAS")
print("=" * 78)
for k, m in [("pomar", POMAR), ("saudavel (referencia sistematica)", REF),
             ("zona0 = FOCO ESTE (vocabulario antigo)", ZONA0),
             ("nu2021 (chao lavrado, dentro do pomar)", NU21 & POMAR)]:
    print("  %-42s %5d celulas   %6.2f ha" % (k, m.sum(), m.sum() / 100.0))

do, de = discos_dos_focos(POMAR)
print("  %-42s %5d celulas   %6.2f ha" % ("disco OESTE r=90 m (C1)", do.sum(), do.sum() / 100.0))
print("  %-42s %5d celulas   %6.2f ha" % ("disco ESTE  r=90 m (C1)", de.sum(), de.sum() / 100.0))

print()
print("=" * 78)
print("b) NIVEL ABSOLUTO DE NDVI  (nao depende da referencia)")
print("=" * 78)
alvos = [("referencia sistematica", REF), ("pomar inteiro", POMAR),
         ("FOCO ESTE (zona0)", ZONA0), ("FOCO ESTE sem chao lavrado", Z0_LIMPA),
         ("disco OESTE r=90", do), ("disco ESTE r=90", de)]
print("\n%-30s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
niveis = {}
for nome, m in alvos:
    v = np.array([float(np.nanmean(nd[d][m])) for d in DATAS])
    niveis[nome] = v
    r = stats.linregress(anos, v)
    print("%-30s %s   declive %+.5f/ano  p=%.4f"
          % (nome, "  ".join("%.3f" % x for x in v), r.slope, r.pvalue))

print()
print("=" * 78)
print("c) FOSSO ATE A REFERENCIA  (a grandeza operativa, R2 G31)")
print("=" * 78)
fossos = {}
for nome, _ in alvos[2:]:
    v = niveis["referencia sistematica"] - niveis[nome]
    fossos[nome] = v
    r = stats.linregress(anos, v)
    print("%-30s %s   declive %+.5f/ano  p=%.4f"
          % (nome, "  ".join("%.3f" % x for x in v), r.slope, r.pvalue))

print()
print("=" * 78)
print("d) DEFICE E NUCLEOS  (nenhuma mascara os define)")
print("=" * 78)
serie = []
for d in DATAS:
    ref = float(np.nanmean(nd[d][REF]))
    dfc = mapa_defice(nd[d], POMAR, ref)
    nucs = nucleos(dfc)
    serie.append(dict(data=d, doy=doy(d), ref=ref, defice_ha=dfc.sum() / 100.0,
                      frac_pct=100.0 * dfc.sum() / POMAR.sum(),
                      nucleos=[[round(a, 2), round(e), round(n)] for a, e, n, _ in nucs]))
    print("%s  defice %5.2f ha (%4.1f%% do pomar) | nucleos>=0,15 ha: %s"
          % (d, dfc.sum() / 100.0, 100.0 * dfc.sum() / POMAR.sum(),
             "  ".join("%.2f ha@E%.0f" % (a, e) for a, e, _, _ in nucs[:4]) or "nenhum"))

print()
print("=" * 78)
print("e) QUANTO VALIA A CIRCULARIDADE DO masks.json ANTIGO")
print("=" * 78)
print("Le-se o ficheiro antigo UMA vez, so para medir. Nao entra em mais nada.")
with open(os.path.join(RAIZ, "sentinel", "masks.json"), encoding="utf-8") as f:
    velho = json.load(f)
print("  chaves do masks.json antigo:", [k for k in velho if not k.startswith("_")])

from matplotlib.path import Path as MP  # noqa: E402


def poli_para_mascara(poly):
    """Poligonos de masks.json / masks_geograficas.json em coordenadas de PIXEL
    (coluna, linha), nao em UTM. Rasteriza sobre os centros das celulas."""
    cc, ll = np.meshgrid(np.arange(NC, dtype=float), np.arange(NL, dtype=float))
    pts = np.column_stack([cc.ravel(), ll.ravel()])
    m = np.zeros(pts.shape[0], bool)
    grupos = poly if isinstance(poly[0][0], (list, tuple)) else [poly]
    for g in grupos:
        a = np.array(g, float)
        if a.ndim != 2 or a.shape[0] < 3:
            continue
        m |= MP(a).contains_points(pts)
    return m.reshape(cc.shape)


nd26 = nd["2026-07-27"]
velhas = {}
for k in ("pomar", "manchaW", "zona0", "saudavel", "saudavel_2", "saudavel_3"):
    if k in velho:
        try:
            velhas[k] = poli_para_mascara(velho[k])
        except Exception as e:
            print("  (nao reconstrui %s: %s)" % (k, e))

for k, m in velhas.items():
    if m.sum() == 0:
        continue
    print("  %-12s %5d celulas | NDVI 2026 min %.3f  media %.3f  max %.3f"
          % (k, m.sum(), np.nanmin(nd26[m]), np.nanmean(nd26[m]), np.nanmax(nd26[m])))

if "manchaW" in velhas and velhas["manchaW"].sum() > 0:
    mw = velhas["manchaW"]
    frac = float((nd26[mw] < 0.76).mean())
    print("\n  TESTE DE CIRCULARIDADE: fraccao da `manchaW` antiga com nd2026 < 0,76")
    print("  = %.3f. Uma mascara geografica honesta nao teria razao para dar isto." % frac)
    print("  Nivel de NDVI 2026 da `manchaW` antiga: %.3f" % np.nanmean(nd26[mw]))
    print("  Nivel de NDVI 2026 do FOCO OESTE tal como emerge do defice: ver c2_04.")

if "saudavel" in velhas:
    sv = velhas["saudavel"] | velhas.get("saudavel_2", np.zeros_like(velhas["saudavel"])) \
         | velhas.get("saudavel_3", np.zeros_like(velhas["saudavel"]))
    if sv.sum():
        v_velha = np.array([float(np.nanmean(nd[d][sv & POMAR])) for d in DATAS])
        r = stats.linregress(anos, v_velha)
        print("\n  Referencia ANTIGA (3 manchas escolhidas por aparencia), dentro do pomar novo:")
        print("  %s   declive %+.5f/ano  p=%.4f"
              % ("  ".join("%.3f" % x for x in v_velha), r.slope, r.pvalue))
        r2 = stats.linregress(anos, niveis["referencia sistematica"])
        print("  Referencia SISTEMATICA:")
        print("  %s   declive %+.5f/ano  p=%.4f"
              % ("  ".join("%.3f" % x for x in niveis["referencia sistematica"]),
                 r2.slope, r2.pvalue))
        print("  Diferenca de declive: %+.5f/ano  ->  %+.3f NDVI sobre os 9,1 anos da serie"
              % (r.slope - r2.slope, (r.slope - r2.slope) * (anos[-1] - anos[0])))

json.dump(dict(
    datas=DATAS, doy=[doy(d) for d in DATAS], anos=list(anos),
    niveis={k: list(map(float, v)) for k, v in niveis.items()},
    fossos={k: list(map(float, v)) for k, v in fossos.items()},
    serie=serie,
    areas_celulas=dict(pomar=int(POMAR.sum()), saudavel=int(REF.sum()),
                       zona0=int(ZONA0.sum()), nu2021=int((NU21 & POMAR).sum()),
                       disco_oeste=int(do.sum()), disco_este=int(de.sum())),
), open(os.path.join(SAIDA, "c2_01_serie.json"), "w", encoding="utf-8"),
    ensure_ascii=False, indent=1)
print("\nescrito c2_01_serie.json")
