# -*- coding: utf-8 -*-
"""C3/A2 · 09 — o CSV contra a folha de origem, celula a celula."""
import os, sys, re
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

DL = r"C:\Users\Jackster2\Downloads"
PT = os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx")
EN = os.path.join(DL, "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx")

pt = pd.read_excel(PT, sheet_name="Fisico-Quimica por Talhao").astype(str)
A = carrega("c3_04_registo_principal.csv")
R = [x for x in A if "sico-Qu" in str(x.get("Doc_Type",""))]
CSV = {}
for x in R:
    CSV[(str(x["Organism_Parameter"]).strip(),
         str(x["Terrain_Block_Parcel"]).strip())] = str(x["Value"]).strip()

col2blk = {c: c.split(" (2026")[0].strip() for c in pt.columns[1:]}
print("="*104)
print("O CSV contra a folha «Fisico-Quimica por Talhao» — onde perdeu informacao")
print("="*104)
print()
perdidos = []
for i in range(len(pt)):
    par = pt.iloc[i, 0].strip()
    for c in pt.columns[1:]:
        b = col2blk[c]
        orig = pt.loc[i, c].strip()
        alvo = CSV.get((par, b))
        if alvo is None:
            print("  SEM PAR no CSV: %s / %s" % (par, b)); continue
        # o CSV corta tudo depois de '/'?
        if orig != alvo:
            perdidos.append((par, b, orig, alvo))
print("  celulas em que o CSV NAO reproduz a folha: %d de %d"
      % (len(perdidos), len(pt)*(len(pt.columns)-1)))
print()
for par, b, orig, alvo in perdidos:
    print("  %-22s %-18s" % (par[:22], b[:18]))
    print("      folha: %s" % orig[:90])
    print("      CSV  : %s" % alvo[:90])
print()
extra = set()
for par, b, orig, alvo in perdidos:
    for m in re.finditer(r"/\s*([A-Za-z][A-Za-z0-9]*)\s*([\d.]+)", orig):
        extra.add(m.group(1))
print("  GRANDEZAS que a folha tem e o CSV deitou fora: %s" % (sorted(extra) or "nenhuma"))
print()
print("="*104)
print("E o inverso: parametros que o D9 declarou AUSENTES")
print("="*104)
tudo = " || ".join(pt.astype(str).values.ravel().tolist())
for termo in ("CTC", "satura", "bases", "MnAI", "Al", "Na", "profund", "cm"):
    n = len(re.findall(termo, tudo, re.I))
    print("  «%-9s» aparece %d vezes na folha de origem" % (termo, n))
