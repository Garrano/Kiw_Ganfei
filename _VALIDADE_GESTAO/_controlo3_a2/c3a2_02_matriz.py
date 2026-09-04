# -*- coding: utf-8 -*-
"""C3/A2 · 02 — a matriz 9 boletins x 12 parametros, com os valores crus."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

OUT = os.path.dirname(os.path.abspath(__file__))
A = carrega("c3_04_registo_principal.csv")
R = [x for x in A if "sico-Qu" in str(x.get("Doc_Type",""))]

BLOCOS = ["Erica 2016 R","Erica 2016 E","B2 - V7","B3 - 7 ha",
          "B2 - Zona 1 (V7)","B1 C1","B1 C3","B1 C4","Parcela B4"]
PARS = ["pH (H2O)","Textura","Mat","Raz","Azoto","sforo","ssio","lcio",
        "sio (MgO)","Enxofre","Ferro","Mangan"]

def num(v):
    """Primeiro numero da cadeia de Value; devolve (valor, prefixo) — '<' importa."""
    s = str(v).strip()
    pre = "<" if s.startswith("<") else (">" if s.startswith(">") else "")
    m = re.search(r"[-+]?\d+(?:[.,]\d+)?", s)
    return (float(m.group(0).replace(",", ".")) if m else None), pre

M = collections.defaultdict(dict)
CRU = collections.defaultdict(dict)
for x in R:
    b = str(x["Terrain_Block_Parcel"]).strip()
    p = str(x["Organism_Parameter"]).strip()
    v, pre = num(x["Value"])
    M[p][b] = v
    CRU[p][b] = (str(x["Value"]), str(x["Unit"]), pre)

if __name__ == "__main__":
    nome = {p: [q for q in M if p in q][0] for p in PARS}
    print("%-18s" % "parametro", end="")
    for b in BLOCOS: print("%12s" % b[:11], end="")
    print()
    print("-"*(18+12*9))
    for p in PARS:
        q = nome[p]
        print("%-18s" % q[:18], end="")
        for b in BLOCOS:
            v = CRU[q][b][0]
            print("%12s" % v[:11], end="")
        print()
    print()
    print("unidades:", {nome[p]: CRU[nome[p]][BLOCOS[0]][1] for p in PARS})
    json.dump({q: {b: M[q][b] for b in BLOCOS} for q in M},
              open(os.path.join(OUT, "c3a2_matriz.json"), "w"), indent=1)
    json.dump({q: {b: CRU[q][b] for b in BLOCOS} for q in CRU},
              open(os.path.join(OUT, "c3a2_matriz_cru.json"), "w"), indent=1)
    print("escrito c3a2_matriz.json")
