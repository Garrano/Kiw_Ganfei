# -*- coding: utf-8 -*-
"""C3/A2 · 12 — os nove boletins nao sao um instrumento: sao DOIS lotes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

R = [x for x in carrega("c3_04_registo_principal.csv")
     if "sico-Qu" in str(x.get("Doc_Type",""))]
mn = {str(x["Terrain_Block_Parcel"]).strip(): str(x["Value"])
      for x in R if "Mangan" in x["Organism_Parameter"]}
dt = {str(x["Terrain_Block_Parcel"]).strip(): str(x["Sample_Date"])[:10] for x in R}
print("="*92)
print("O 13.o valor: MnAI, dentro da cadeia do Manganes")
print("="*92)
print("  %-20s %-12s %s" % ("boletim","colheita","tem MnAI?"))
com, sem = [], []
for b in sorted(mn, key=lambda k: dt[k]):
    t = "MnAI" in mn[b]
    (com if t else sem).append(b)
    print("  %-20s %-12s %s" % (b, dt[b], "SIM  " + mn[b].split("/")[1].strip()
                                if t else "nao"))
print()
print("  COM MnAI (%d): %s" % (len(com), ", ".join(com)))
print("  SEM MnAI (%d): %s" % (len(sem), ", ".join(sem)))
print("""
  A divisao e exacta e e temporal: os quatro boletins de 2026-03-03 nao trazem
  MnAI; os cinco de Junho e Julho trazem. Os TRES boletins do B1 estao todos no
  lote de Julho.

  Consequencias, e sao duas:
   1 · o D9 escreve «os 12 parametros sao pH, textura, MO, C:N, N, P2O5, K2O,
       CaO, MgO, S, Fe, Mn». Sao doze LINHAS; as grandezas sao treze, e a
       decima terceira so existe em cinco dos nove. Um inventario que conta
       linhas em vez de grandezas nao e um inventario.
   2 · «ser do B1» e «ser do lote de Julho» sao a mesma particao aumentada de
       um elemento (o B4). Nenhum desenho com n = 9 as separa — e o lote
       DEMONSTRAVELMENTE difere, porque reporta uma grandeza a mais.
       O confundimento nao e hipotetico: esta impresso nos valores.
""")
