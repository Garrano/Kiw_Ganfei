# -*- coding: utf-8 -*-
"""C1a/C1b são o kiwi do IFAP, ou são outra coisa dentro do mesmo bloco?

A colisão
---------
Sobre exactamente o mesmo terreno, a 750 m a sudoeste do pomar, há duas
leituras que não podem ser as duas verdadeiras da mesma área:

  ORTOFOTO (C0, adenda de controlo)
    C1a e C1b, 11,60 ha. `estrutura_por_epoca`: 2012 «copado continuo escuro,
    compativel com latada coberta»; 2021 e 2023 «linhas separadas por
    entrelinha aberta»; 2025 «camalhoes com tunel/cobertura de plastico
    continua». `nao_controla`: «proprietario desconhecido», «origem da agua
    nao determinada». Veredicto: **nao serve como controlo contemporaneo de
    kiwi**.

  PARCELÁRIO IFAP, campanha 2025
    12,64 ha declarados **KIWI** (codigo 124) em seis poligonos, todos em
    parcelas do **ENT 472062 — a mesma exploracao do pomar**.

O proprietario nao e desconhecido, e a cultura declarada e kiwi.

A hipótese que resolve, e é geométrica
--------------------------------------
`proveniencia_limite` de C1a e C1b: **«material de cobertura, ortofoto 2025
25 cm»**. Os poligonos foram desenhados **a volta do plastico**. Se o plastico
e o kiwi ocuparem partes diferentes do bloco, as duas leituras sao ambas
verdadeiras e falam de sitios diferentes — e entao:

  · a serie `b1_serie_verdadeira.json` mediu a area do plastico, nao o kiwi;
  · o teste de degrau que corri em `lobulo_oeste_degrau.py` foi a unidade
    errada;
  · e as 12,64 ha de kiwi continuam por medir.

Se, pelo contrario, se sobrepuserem, entao ou o IFAP declara kiwi onde ha
tuneis de plastico, ou a leitura da ortofoto esta errada — e a regra do
projecto diz qual ganha: **o registo de quem sabe ganha ao nosso calculo**.

Este script nao decide por argumento. Mede a sobreposicao.
"""
import json
import os

import numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon, MultiPolygon, shape
from shapely.ops import transform as sh_transform, unary_union

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C0 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para_utm = lambda g: sh_transform(lambda x, y, z=None: tr.transform(x, y), g)

# ---- C1a e C1b, ja em EPSG:32629 ----------------------------------------
D = json.load(open(os.path.join(C0, "controlos.geojson")))
CTRL = {}
for ft in D["features"]:
    i = ft["properties"]["id"]
    if i in ("C1a", "C1b", "C1c"):
        CTRL[i] = shape(ft["geometry"]).buffer(0)

# ---- kiwi do IFAP no bloco, em WGS84 -> UTM ------------------------------
G19 = (529350.0, 4653700.0, 530085.0, 4654478.0)
C = json.load(open(os.path.join(VG, "ifap_culturas.json")))
P = json.load(open(os.path.join(VG, "ifap_parcelas.json")))

parc = []
for ft in P["features"]:
    g = para_utm(shape(ft["geometry"])).buffer(0)
    parc.append((g, ft["properties"].get("ENT_ID"), ft["properties"].get("PAR_NUM")))

kiwi = []
for ft in C["features"]:
    if str(ft["properties"].get("PUN_CUL_COD")) != "124":
        continue
    g = para_utm(shape(ft["geometry"])).buffer(0)
    c = g.centroid
    if not (G19[0] <= c.x <= G19[2] and G19[1] <= c.y <= G19[3]):
        continue
    dono = None
    for pg, e, pn in parc:
        if pg.contains(c):
            dono = e
            break
    kiwi.append((ft["properties"].get("CUL_ID"), g, dono))

K = unary_union([g for _, g, _ in kiwi])
CT = unary_union(list(CTRL.values()))
CAB = unary_union([CTRL["C1a"], CTRL["C1b"]])

ha = lambda g: g.area / 1e4

print("=" * 88)
print("AS DUAS DELIMITAÇÕES, SOBRE O MESMO BLOCO")
print("=" * 88)
print()
for i in ("C1a", "C1b", "C1c"):
    g = CTRL[i]
    print("  %-5s %6.2f ha   E %.0f–%.0f   N %.0f–%.0f"
          % (i, ha(g), g.bounds[0], g.bounds[2], g.bounds[1], g.bounds[3]))
print("  %-5s %6.2f ha   (C1a + C1b, o que a série do «B1» mediu)" % ("soma", ha(CAB)))
print()
print("  %-5s %6.2f ha   E %.0f–%.0f   N %.0f–%.0f   (kiwi IFAP 2025)"
      % ("KIWI", ha(K), K.bounds[0], K.bounds[2], K.bounds[1], K.bounds[3]))

print()
print("=" * 88)
print("A SOBREPOSIÇÃO — a pergunta toda")
print("=" * 88)
print()
inter = CAB.intersection(K)
print("  C1a+C1b                       %6.2f ha" % ha(CAB))
print("  kiwi IFAP no bloco            %6.2f ha" % ha(K))
print("  INTERSECÇÃO                   %6.2f ha" % ha(inter))
print()
print("  do kiwi, quanto cai em C1a+C1b : %5.1f %%"
      % (100 * ha(inter) / ha(K) if ha(K) else 0))
print("  de C1a+C1b, quanto é kiwi      : %5.1f %%"
      % (100 * ha(inter) / ha(CAB) if ha(CAB) else 0))
print("  kiwi FORA de C1a+C1b           : %6.2f ha" % ha(K.difference(CAB)))
print("  C1a+C1b FORA do kiwi           : %6.2f ha" % ha(CAB.difference(K)))

print()
print("polígono a polígono:")
print()
print("  %-10s %7s %10s %9s %9s  %s"
      % ("CUL_ID", "ha", "ENT_ID", "em C1a/b", "% dele", "onde"))
for cid, g, dono in sorted(kiwi, key=lambda t: -t[1].area):
    i2 = g.intersection(CAB)
    pct = 100 * ha(i2) / ha(g) if ha(g) else 0
    onde = "dentro" if pct > 80 else ("parcial" if pct > 5 else "FORA")
    print("  %-10s %7.2f %10s %9.2f %8.1f %%  %s"
          % (cid, ha(g), dono, ha(i2), pct, onde))

print()
print("=" * 88)
print("VEREDICTO")
print("=" * 88)
print()
frac = ha(inter) / ha(K) if ha(K) else 0
if frac < 0.25:
    print("As duas delimitações são de SÍTIOS DIFERENTES dentro do mesmo bloco.")
    print("As duas leituras podem ser ambas verdadeiras, e são de coisas distintas:")
    print("C1a/C1b foram desenhados à volta do plástico e é isso que contêm;")
    print("o kiwi declarado está noutro sítio, e NUNCA FOI MEDIDO.")
    print()
    print("Consequência directa: a série `b1_serie_verdadeira.json` e o teste de")
    print("degrau que corri sobre ela mediram a área do plástico. A unidade estava")
    print("errada, e a conclusão sobre o «lóbulo» não se aplica ao kiwi.")
elif frac > 0.75:
    print("São o MESMO sítio. Então o IFAP declara kiwi onde a ortofoto lê túneis")
    print("de plástico, e há uma contradição de facto a resolver — não por nós, mas")
    print("perguntando. Pela regra do projecto o registo ganha ao nosso cálculo.")
else:
    print("Sobrepõem-se em parte (%.0f %%). Nem uma coisa nem outra: é preciso")
    print("separar por polígono e tratar cada um pelo que é." % (100 * frac))

json.dump(dict(ha_c1a=ha(CTRL["C1a"]), ha_c1b=ha(CTRL["C1b"]),
               ha_c1ab=ha(CAB), ha_kiwi=ha(K), ha_inter=ha(inter),
               frac_kiwi_em_c1ab=frac,
               kiwi=[dict(cul_id=c, ha=ha(g), ent=d,
                          ha_em_c1ab=ha(g.intersection(CAB)))
                     for c, g, d in kiwi]),
          open(os.path.join(VG, "c1ab_contra_kiwi_ifap.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito c1ab_contra_kiwi_ifap.json")
