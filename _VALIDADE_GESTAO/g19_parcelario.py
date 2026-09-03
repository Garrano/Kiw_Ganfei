# -*- coding: utf-8 -*-
"""G19 — o bloco de 16,4 ha a sudoeste pertence à exploração? Fecha uma NÃO TESTÁVEL da C0.

A pergunta, e quem a fez
------------------------
`CAMADA_0_CERTIFICADO.md`, NÃO TESTÁVEL:

  «**Se o bloco de 16,4 ha a sudoeste (E529350–530085, N4653700–4654478)
  pertence à exploração.** O troço OESTE do esquema cai sobre ele… e o bloco
  tem a mesma assinatura de rede. Mas é uma extrapolação de ~1200 px além do
  troço ajustado, com erro de ordem ±150 m; e **a assinatura de rede não prova
  propriedade**. A coincidência com a lacuna de área (44,9 − 29,0 = 15,9 ha,
  contra 16,4 ha medidos) é forte mas não é prova.»

E dizia o que faria falta: **«a tabela de válvulas com áreas, ou a confirmação
da gestora sobre a M1 v2, ou o parcelário».**

O parcelário existe desde ontem e ninguém o foi buscar a esta pergunta.

Porque isto passou à frente da P01
----------------------------------
Retirado o lóbulo como controlo, **a apresentação não tem nenhum controlo
externo**: todas as comparações são internas à mesma exploração. Este bloco
decide de que lado cai:

  · se for da MESMA exploração → é mais pomar da mesma gestão, e a frase «fora
    dos focos este pomar não se mexeu» ganha 16 ha de alcance mas continua
    interna;
  · se for de OUTRA exploração e tiver kiwi → é o primeiro controlo externo
    contemporâneo do caso, e a frase passa a «nem este pomar, nem o do lado»,
    que é outra ordem de argumento.

O que este teste pode e não pode
--------------------------------
PODE: dizer que ENT_ID cobre o bloco, que culturas estão declaradas, e que
área. São registos administrativos, não inferência nossa.

NÃO PODE: provar que a rede de rega é partilhada, nem que a água é a mesma. O
ENT_ID é o beneficiário declarado numa campanha; é um facto do tipo 1 (registo
de quem sabe) e vale como tal, não mais.
"""
import json
import os
from collections import Counter

import numpy as np
from matplotlib.path import Path as MP
from pyproj import Transformer

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
G19 = (529350.0, 4653700.0, 530085.0, 4654478.0)
ENT_POMAR = 472062          # o beneficiario do corpo principal

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)


def poligonos(ft):
    gm = ft.get("geometry") or {}
    if not gm:
        return []
    if gm["type"] == "Polygon":
        return [gm["coordinates"]]
    return list(gm["coordinates"])


def utm_e_area(anel):
    a = np.array(anel)
    if a.ndim != 2 or len(a) < 3:
        return None, 0.0
    x, y = tr.transform(a[:, 0], a[:, 1])
    p = np.column_stack([x, y])
    area = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return p, area


def dentro_g19(p):
    cx, cy = p[:, 0].mean(), p[:, 1].mean()
    return G19[0] <= cx <= G19[2] and G19[1] <= cy <= G19[3]


print("=" * 92)
print("G19 — bloco a sudoeste  E%d–%d  N%d–%d" % G19)
print("=" * 92)
print()

P = json.load(open(os.path.join(VG, "ifap_parcelas.json")))
feats = P["features"]
linhas = []
for ft in feats:
    for anel in poligonos(ft):
        p, a = utm_e_area(anel[0] if isinstance(anel[0][0], (list, tuple)) else anel)
        if p is None or not dentro_g19(p):
            continue
        pr = ft["properties"]
        linhas.append(dict(par=pr.get("PAR_NUM"), ent=pr.get("ENT_ID"),
                           ha=a / 10000.0,
                           e=float(p[:, 0].mean()), n=float(p[:, 1].mean())))
        break

linhas.sort(key=lambda r: -r["ha"])
print("PARCELAS com centróide no bloco: %d" % len(linhas))
print()
print("%-16s %10s %9s %10s %10s" % ("PAR_NUM", "ENT_ID", "ha", "E", "N"))
for r in linhas:
    marca = "  <-- mesma exploração" if r["ent"] == ENT_POMAR else ""
    print("%-16s %10s %9.2f %10.0f %10.0f%s"
          % (r["par"], r["ent"], r["ha"], r["e"], r["n"], marca))

ents = Counter(r["ent"] for r in linhas)
ha_por_ent = {}
for r in linhas:
    ha_por_ent[r["ent"]] = ha_por_ent.get(r["ent"], 0.0) + r["ha"]

print()
print("BENEFICIÁRIOS no bloco")
print()
print("%-12s %8s %10s  %s" % ("ENT_ID", "parcelas", "ha", ""))
for e, n_ in ents.most_common():
    print("%-12s %8d %10.2f  %s"
          % (e, n_, ha_por_ent[e],
             "MESMA exploração do pomar" if e == ENT_POMAR else "OUTRA exploração"))

# ---------------------------------------------------------------- culturas
C = json.load(open(os.path.join(VG, "ifap_culturas.json")))
cf = C["features"] if isinstance(C, dict) else C
culturas = []
for ft in cf:
    for anel in poligonos(ft):
        p, a = utm_e_area(anel[0] if isinstance(anel[0][0], (list, tuple)) else anel)
        if p is None or not dentro_g19(p):
            continue
        pr = ft["properties"]
        cod = pr.get("PUN_CUL_COD")
        culturas.append(dict(cod=cod, ha=a / 10000.0,
                             nome=pr.get("PUN_CUL_DESC"),
                             ent=pr.get("ENT_ID")))
        break

print()
print("CULTURAS declaradas no bloco: %d polígonos" % len(culturas))
print()
cnt = Counter((c["cod"], c["nome"]) for c in culturas)
ha_cod = {}
for c in culturas:
    ha_cod[c["cod"]] = ha_cod.get(c["cod"], 0.0) + c["ha"]
print("%-10s %-34s %8s %9s" % ("código", "descrição", "polígs", "ha"))
for (cod, nome), n_ in cnt.most_common():
    marca = "   <-- KIWI" if str(cod) == "124" else ""
    print("%-10s %-34s %8d %9.2f%s"
          % (cod, (nome or "")[:34], n_, ha_cod[cod], marca))

kiwi = [c for c in culturas if str(c["cod"]) == "124"]
ha_kiwi = sum(c["ha"] for c in kiwi)

print()
print("=" * 92)
print("VEREDICTO")
print("=" * 92)
print()
outras = {e: h for e, h in ha_por_ent.items() if e != ENT_POMAR}
print("área de parcelas no bloco          : %.2f ha  (C0 mediu 16,4 ± 2 por assinatura)"
      % sum(ha_por_ent.values()))
print("da MESMA exploração (ENT %d)   : %.2f ha em %d parcelas"
      % (ENT_POMAR, ha_por_ent.get(ENT_POMAR, 0.0), ents.get(ENT_POMAR, 0)))
print("de OUTRAS explorações              : %.2f ha em %d beneficiários"
      % (sum(outras.values()), len(outras)))
print("kiwi declarado no bloco            : %.2f ha em %d polígonos"
      % (ha_kiwi, len(kiwi)))

json.dump(dict(g19=list(G19), parcelas=linhas, culturas=culturas,
               ha_por_ent={str(k): v for k, v in ha_por_ent.items()},
               ha_kiwi=ha_kiwi),
          open(os.path.join(VG, "g19_parcelario.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito g19_parcelario.json")
