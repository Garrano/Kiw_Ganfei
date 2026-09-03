# -*- coding: utf-8 -*-
"""C1-14 — as dez quantidades-ancora (CONTROLOS.md, controlo 2) mais as novas
que a R2 estabelece. Reporta-se o valor obtido, mesmo quando a camada nao lhe
tocou, para a divergencia entre camadas saltar sozinha.
"""
import os, sys, json, glob
import numpy as np
import rasterio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

lin = []
def reg(nome, decl, obt, un, nota=""):
    lin.append(dict(ancora=nome, declarado=decl, obtido=obt, unidade=un, nota=nota))
    igual = (str(decl) == str(obt))
    print("%-46s decl %-28s obt %-28s %s %s"
          % (nome, str(decl), str(obt), un, "" if igual else "  <-- DIFERE"))

# --- AOI e grelha ---
tifs = sorted(glob.glob(os.path.join(RAIZ, "sentinel", "*.tif")))
bs, shp = set(), set()
for t in tifs:
    with rasterio.open(t) as s:
        bs.add(tuple(round(x) for x in s.bounds)); shp.add(s.shape)
reg("AOI (EPSG:32629)", "529950, 4654600, 531950, 4655600",
    ", ".join(str(x) for x in sorted(bs)[0]) if len(bs) == 1 else "NAO UNICA", "")
reg("grelha", "200x100 de 10 m", "%dx%d" % (list(shp)[0][1], list(shp)[0][0]) if len(shp) == 1 else "?", "px")
reg("cenas na serie", 11, len(tifs), "datas")

masc, meta = carrega_mascaras()
# --- poligono pomar: valor R2 (30,31 ha), nao o declarado de abertura (29,0) ---
reg("poligono `pomar` (declarado na abertura)", 2903, int(masc["pomar"].sum()), "px de 10 m",
    "a abertura declara 2903 px / 29,0 ha do poligono antigo; a R2 G2 substitui por 3031 px / 30,31 ha")
reg("poligono `pomar` em ha", "29,0 (abertura) / 30,31 (R2 G2)",
    "%.2f" % (masc["pomar"].sum() / 100), "ha")
reg("referencia sa", "454 (antiga) / 110 celulas (R2 G4)", int(masc["saudavel"].sum()), "px",
    "a referencia sistematica da R2 substitui as tres manchas escolhidas")
reg("mascara `manchaW`", "427", "NAO EXISTE", "px",
    "R2 G4 retira-a; era circular em relacao ao NDVI que se media")
reg("mascara `zona0`", 220, int(masc["zona0"].sum()), "px",
    "R2: 202 das 220 celulas sobrevivem a interseccao com o pomar novo; = FOCO ESTE")

# --- ancoras novas da R2 ---
reg("pomar (R2 G2)", "30,31", "%.2f" % (masc["pomar"].sum() / 100), "ha")
reg("referencia sistematica (R2 G4)", "1,10 ha / 110 celulas",
    "%.2f ha / %d celulas" % (masc["saudavel"].sum() / 100, masc["saudavel"].sum()), "")
V = valvulas()
tot = sum(v["area_m2"] for v in V.values())
reg("total da banda contigua (R2 G35)", "27,30", "%.2f" % (tot / 1e4), "ha",
    "soma das areas tabeladas das valvulas 6 a 17")
reg("total da tabela de valvulas (R2 G35)", "44,93", "44,93", "ha",
    "NAO VERIFICAVEL nesta camada: as oito parcelas soltas (17,66 ha) nao tem posicao; 27,30 + 17,66 = 44,96")

# --- NDVI da referencia: reportado por exigencia do controlo 2 ---
def nd(f):
    with rasterio.open(f) as s:
        return s.read(1)
for data, decl in (("2017-07-02", 0.838), ("2026-07-27", 0.886)):
    a = nd(os.path.join(RAIZ, "sentinel", data + ".tif"))
    v_sist = float(np.nanmean(a[masc["saudavel"]]))
    reg("NDVI medio da referencia, %s" % data, decl, "%.4f" % v_sist, "",
        "medido na referencia SISTEMATICA (110 celulas). O valor declarado e da referencia antiga, escolhida por NDVI alto na ultima cena — objectos diferentes")

# --- os dois focos ---
reg("foco OESTE (R2 G34)", "E530485 N4655053", "E530485 N4655053", "EPSG:32629", "herdado, nao remedido nesta camada")
reg("foco ESTE (R2 G34)", "E530977 N4655117", "E530977 N4655117", "EPSG:32629", "herdado")
E29, N29 = centros_celulas()
z = masc["zona0"]
reg("centroide do poligono `zona0`", "—", "E%.0f N%.0f" % (E29[z].mean(), N29[z].mean()),
    "EPSG:32629", "a %.0f m do centro declarado do foco ESTE"
    % np.hypot(E29[z].mean() - FOCO_ESTE[0], N29[z].mean() - FOCO_ESTE[1]))
reg("distancia entre os dois focos", "—",
    "%.0f" % np.hypot(FOCO_ESTE[0] - FOCO_OESTE[0], FOCO_ESTE[1] - FOCO_OESTE[1]), "m")
reg("chao lavrado em 2021 dentro do pomar", "1,67 (masks_geograficas)",
    "%.2f" % ((masc["nu2021"] & masc["pomar"]).sum() / 100), "ha")

json.dump(lin, open(os.path.join(SAIDA, "c1_14_ancoras.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_14_ancoras.json")
