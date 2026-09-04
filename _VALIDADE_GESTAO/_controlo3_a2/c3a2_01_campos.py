# -*- coding: utf-8 -*-
"""C3/A2 · 01 — os 22 campos, valor a valor, nos 108 registos."""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

A = carrega("c3_04_registo_principal.csv")
R = [x for x in A if "sico-Qu" in str(x.get("Doc_Type",""))]
cols = list(R[0].keys())
print("colunas (%d): %s" % (len(cols), ", ".join(cols)))
print()
for c in cols:
    v = collections.Counter(str(x.get(c,"")) for x in R)
    vaz = sum(n for k,n in v.items() if not k.strip())
    print("=== %s  (distintos=%d, vazios=%d)" % (c, len(v), vaz))
    for k,n in sorted(v.items(), key=lambda kv:-kv[1])[:14]:
        print("   %3d | %s" % (n, k[:150].replace("\n"," ")))
    print()
