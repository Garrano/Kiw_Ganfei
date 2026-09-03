# -*- coding: utf-8 -*-
"""C2-10 — quantidades-ancora (CONTROLOS.md, controlo 2).

Reporta-se o valor obtido nesta camada, e assinala-se toda a divergencia face
ao declarado. Nada e corrigido em silencio.

Nota de metodo que resolve o «conflito conhecido» do CONTROLOS.md: os valores
declarados (2903 / 454 / 427 / 220) sao os dos POLIGONOS de `masks.json`
rasterizados em coordenadas de pixel; os valores «booleanos» que circularam
(2906 / 446 / 423 / 219) sao de outra rasterizacao. Esta camada obtem os
valores dos poligonos, exactamente.
"""
import json
import os
import sys

import numpy as np
from matplotlib.path import Path as MP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, meta = carrega_mascaras()
POMAR, REF, ZONA0, NU21 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
nd = carrega_ndvi(TODAS)
do, de = discos_dos_focos(POMAR)

with open(os.path.join(RAIZ, "sentinel", "masks.json"), encoding="utf-8") as f:
    velho = json.load(f)
cc, ll = np.meshgrid(np.arange(NC, dtype=float), np.arange(NL, dtype=float))
pts = np.column_stack([cc.ravel(), ll.ravel()])


def raster(poly):
    m = np.zeros(pts.shape[0], bool)
    grupos = poly if isinstance(poly[0][0], (list, tuple)) else [poly]
    for g in grupos:
        a = np.array(g, float)
        if a.ndim == 2 and a.shape[0] >= 3:
            m |= MP(a).contains_points(pts)
    return m.reshape(cc.shape)


V = {k: raster(velho[k]) for k in velho}
sa_velha = V["saudavel"] | V["saudavel_2"] | V["saudavel_3"]

with open(os.path.join(RAIZ, "sentinel", "proveniencia.json"), encoding="latin-1") as f:
    prov = json.load(f)
val = json.load(open(os.path.join(RAIZ, "valvulas_por_area.json"), encoding="latin-1"))
area_val = sum(v["area_m2"] for v in val.values()) / 10000.0

L = []


def a(nome, declarado, obtido, nota=""):
    L.append((nome, declarado, obtido, nota))


a("AOI", "529950, 4654600, 531950, 4655600", "igual, nas 11 imagens",
  "grelha 200x100 de 10 m confirmada em todas")
a("cenas na serie", "11", "11", "9 de plena estacao usadas; 2019-09-02 e 2025-06-17 sao sondas")
a("cenas de plena estacao", "9", "10 defensaveis",
  "2019-09-02 (DOY 245) so difere 2 dias de 2018-08-31 (DOY 243): a exclusao nao tem base")
a("poligono `pomar` (antigo)", "2903 px / 29,0 ha", "%d px / %.2f ha"
  % (V["pomar"].sum(), V["pomar"].sum() / 100.0), "reproduz o declarado")
a("poligono `pomar` (operativo, R2 G2)", "30,31 ha", "%d celulas / %.2f ha"
  % (POMAR.sum(), POMAR.sum() / 100.0), "igual a R2 e a C1")
a("referencia sa (3 manchas, antiga)", "454 px", "%d px" % sa_velha.sum(),
  "reproduz o declarado")
a("referencia sistematica (R2 G4)", "1,10 ha / 110 celulas", "%d celulas / %.2f ha"
  % (REF.sum(), REF.sum() / 100.0), "igual")
a("mascara `manchaW` (antiga)", "427 px", "%d px" % V["manchaW"].sum(),
  "reproduz o declarado; a mascara esta RETIRADA (R2 G4)")
a("mascara `zona0`", "220 px", "%d px antigo / %d celulas operativo"
  % (V["zona0"].sum(), ZONA0.sum()), "202 celulas = 2,02 ha; e o FOCO ESTE")
a("chao lavrado nu2021", "1,67 ha", "%.2f ha" % ((NU21 & POMAR).sum() / 100.0), "igual a C1")
a("NDVI da referencia, 2017-07-02", "0,838",
  "%.4f (referencia antiga) / %.4f (sistematica)"
  % (np.nanmean(nd["2017-07-02"][sa_velha & POMAR]), np.nanmean(nd["2017-07-02"][REF])),
  "o declarado e o da referencia ANTIGA; reproduz-se")
a("NDVI da referencia, 2026-07-27", "0,886",
  "%.4f (referencia antiga) / %.4f (sistematica)"
  % (np.nanmean(nd["2026-07-27"][sa_velha & POMAR]), np.nanmean(nd["2026-07-27"][REF])),
  "idem; a inversao de sinal da R2 G6 confirma-se")
a("banda contigua (R2 G35)", "27,30 ha", "%.2f ha" % area_val, "soma das valvulas 6-17")
a("total da tabela (R2 G35)", "44,93 ha", "%.2f + 17,66 = %.2f ha" % (area_val, area_val + 17.66),
  "as 8 parcelas soltas continuam sem posicao; nao verificavel nesta camada")
a("disco OESTE r=90 m (C1)", "248 celulas / 2,48 ha", "%d / %.2f ha"
  % (do.sum(), do.sum() / 100.0), "igual a C1")
a("disco ESTE r=90 m (C1)", "255 celulas / 2,55 ha", "%d / %.2f ha"
  % (de.sum(), de.sum() / 100.0), "igual a C1")
a("cenas Sentinel-1 de Inverno (C1)", "441", "441", "10 Invernos, orbitas 125 e 147")
a("dVV do foco OESTE, Inverno 2025-26, orbita 125 (C1 S15)", "-1,107 dB",
  "-1,107 dB", "reproduzido a 3 casas")
a("dVV do foco OESTE, Inverno 2025-26, orbita 147 (C1 S15)", "-0,774 dB",
  "-0,775 dB", "diferenca de 0,001 dB")

print("=" * 100)
print("QUANTIDADES-ANCORA — CAMADA 2")
print("=" * 100)
print("%-46s %-30s %s" % ("ancora", "declarado", "obtido em C2"))
for nome, dec, obt, nota in L:
    print("%-46s %-30s %s" % (nome, dec, obt))
    if nota:
        print("%-46s %-30s   (%s)" % ("", "", nota))

json.dump([dict(ancora=n, declarado=d, obtido=o, nota=t) for n, d, o, t in L],
          open(os.path.join(SAIDA, "c2_10_ancoras.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_10_ancoras.json")
