# -*- coding: utf-8 -*-
"""C3/A2 · 03 — Q1: o D8 e um teste ou uma coincidencia com n=9?

Calcula EXACTAMENTE, por enumeracao das C(9,3)=84 atribuicoes possiveis:
  a) P(os dois pH mais baixos serem ambos de um grupo fixo de 3)
  b) P(esse grupo conter simultaneamente o minimo e o maximo)
  c) Mann-Whitney exacto, B1 (n=3) contra o resto (n=6), nos dois sentidos
  d) o mesmo com a pseudo-replica corrigida (B2-V7 e B2-Zona1 sao o MESMO talhao)
"""
import itertools, json, os
from fractions import Fraction

PH = {"Erica 2016 R":7.2,"Erica 2016 E":6.6,"B2 - V7":5.8,"B3 - 7 ha":5.6,
      "B2 - Zona 1 (V7)":5.6,"B1 C1":7.4,"B1 C3":5.2,"B1 C4":5.3,"Parcela B4":6.1}
B1 = ("B1 C1","B1 C3","B1 C4")
nomes = list(PH)
v = [PH[b] for b in nomes]

def rank_medio(vals):
    """postos com media nos empates"""
    ordem = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0]*len(vals)
    i = 0
    while i < len(ordem):
        j = i
        while j+1 < len(ordem) and vals[ordem[j+1]] == vals[ordem[i]]: j += 1
        m = (i+j)/2.0 + 1
        for k in range(i, j+1): r[ordem[k]] = m
        i = j+1
    return r

print("="*92)
print("Q1 · a probabilidade EXACTA, por enumeracao completa")
print("="*92)
print()
ord_ph = sorted(PH.items(), key=lambda kv: kv[1])
print("  os nove, por ordem:")
for i,(b,x) in enumerate(ord_ph,1):
    print("   %d. %-20s %.1f  %s" % (i,b,x,"<-- B1" if b in B1 else ""))
print()

# a) os dois mais baixos ambos no grupo de 3
tot = list(itertools.combinations(range(9), 3))
idx_min2 = {nomes.index(ord_ph[0][0]), nomes.index(ord_ph[1][0])}
idx_min  = nomes.index(ord_ph[0][0]); idx_max = nomes.index(ord_ph[-1][0])
a = sum(1 for c in tot if idx_min2 <= set(c))
b = sum(1 for c in tot if idx_min in c and idx_max in c)
print("  a) P(os DOIS mais baixos serem ambos do mesmo grupo de 3) = %s = %.4f"
      % (Fraction(a,len(tot)), a/len(tot)))
print("     (= C(7,1)/C(9,3) = 7/84 = 1/12)")
print("  b) P(o grupo de 3 conter o MINIMO **e** o MAXIMO)         = %s = %.4f"
      % (Fraction(b,len(tot)), b/len(tot)))
print("     -> a coincidencia que o D8 nao conta e TAO provavel como a que conta.")
print()

# c) Mann-Whitney exacto
R = rank_medio(v)
alvo = sum(R[nomes.index(x)] for x in B1)
print("  c) soma de postos do B1 = %.1f  (postos %s), esperado sob H0 = %.1f"
      % (alvo, sorted(R[nomes.index(x)] for x in B1), 3*(9+1)/2.0))
menor = sum(1 for c in tot if sum(R[i] for i in c) <= alvo)
maior = sum(1 for c in tot if sum(R[i] for i in c) >= alvo)
print("     p unilateral (B1 mais ACIDO) = %s = %.4f" % (Fraction(menor,84), menor/84))
print("     p unilateral (B1 mais BASICO)= %s = %.4f" % (Fraction(maior,84), maior/84))
print("     p bilateral                  = %.4f" % min(1.0, 2*min(menor,maior)/84))
print()

# d) corrigindo a pseudo-replica: B2-V7 e B2-Zona 1 (V7) sao o MESMO talhao
print("  d) MESMO calculo depois de colapsar a pseudo-replica")
print("     (B2 - V7 marco/5,8 e B2 - Zona 1 (V7) junho/5,6 sao o mesmo talhao,")
print("      mesmo ficheiro-fonte B2_V7__*.pdf, mesma valvula 7)")
PH8 = dict(PH); PH8.pop("B2 - Zona 1 (V7)"); PH8.pop("B2 - V7")
PH8["B2-V7 (media das 2 colheitas)"] = round((5.8+5.6)/2, 2)
n8 = list(PH8); v8 = [PH8[k] for k in n8]; R8 = rank_medio(v8)
tot8 = list(itertools.combinations(range(len(n8)), 3))
alvo8 = sum(R8[n8.index(x)] for x in B1)
m8 = sum(1 for c in tot8 if sum(R8[i] for i in c) <= alvo8)
print("     n = %d talhoes.  soma de postos do B1 = %.1f de %d combinacoes"
      % (len(n8), alvo8, len(tot8)))
print("     p unilateral (B1 mais acido) = %.4f" % (m8/len(tot8)))
print()
print("  VEREDICTO Q1: nenhum dos quatro calculos desce abaixo de 0,05.")
print("  A afirmacao 'os dois mais baixos sao do B1' e um acontecimento de")
print("  p = 0,083 sob mistura ao acaso — e o B1 abrange 5,2 a 7,4, que e o")
print("  intervalo INTEIRO dos nove (min E max, ambos dele).")
json.dump(dict(p_dois_mais_baixos=a/len(tot), p_min_e_max=b/len(tot),
               mw_p_acido=menor/84, mw_p_basico=maior/84,
               mw_p_acido_sem_pseudoreplica=m8/len(tot8),
               amplitude_B1=[5.2,7.4], amplitude_todos=[5.2,7.4]),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "c3a2_q1.json"), "w"), indent=1)
