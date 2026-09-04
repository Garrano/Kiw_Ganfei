# -*- coding: utf-8 -*-
"""C3/A2 · 05 — o nulo que respeita a estrutura, e a repetibilidade interna.

TRES coisas que nem o D8 nem o D9 fizeram:

A · MULTIPLICIDADE COM CORRELACAO. Onze parametros do mesmo tubo nao sao onze
    testes independentes. O nulo correcto permuta o ROTULO DE BLOCO uma vez e
    recalcula os onze — 84 permutacoes, todas enumeraveis.

B · REPETIBILIDADE INTERNA, que existe e nunca foi usada: `B2 - V7` (2026-03-03)
    e `B2 - Zona 1 (V7)` (2026-06-17) sao o MESMO talhao, mesma valvula 7, dois
    ficheiros-fonte `B2_V7__Marc_o_26.pdf` e `B2_V7__Junho_26.pdf`. A diferenca
    entre os dois e o piso de ruido de tudo o que se disser com estes boletins.

C · CONFUNDIMENTO COM A DATA DE COLHEITA. Marco (4), Junho (1), Julho (4).
"""
import itertools, json, os, re

OUT = os.path.dirname(os.path.abspath(__file__))
CRU = json.load(open(os.path.join(OUT, "c3a2_matriz_cru.json")))
BLOCOS = ["Erica 2016 R","Erica 2016 E","B2 - V7","B3 - 7 ha",
          "B2 - Zona 1 (V7)","B1 C1","B1 C3","B1 C4","Parcela B4"]
DATA = {"Erica 2016 R":"03","Erica 2016 E":"03","B2 - V7":"03","B3 - 7 ha":"03",
        "B2 - Zona 1 (V7)":"06","B1 C1":"07","B1 C3":"07","B1 C4":"07",
        "Parcela B4":"07"}
FOCO = ("B2 - V7","B2 - Zona 1 (V7)","B3 - 7 ha")
B1 = ("B1 C1","B1 C3","B1 C4")
PARS = [p for p in CRU if "Textura" not in p]

def val(s):
    m = re.search(r"[-+]?\d+(?:[.,]\d+)?", str(s))
    return float(m.group(0).replace(",", ".")) if m else None

def postos(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r=[0.0]*len(v); i=0
    while i < len(o):
        j=i
        while j+1 < len(o) and v[o[j+1]]==v[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2.0+1
        i=j+1
    return r

RANK = {p: postos([val(CRU[p][b][0]) for b in BLOCOS]) for p in PARS}
TODOS = list(itertools.combinations(range(9), 3))

def p_um(p, g):
    R = RANK[p]; alvo = sum(R[i] for i in g)
    return sum(1 for c in TODOS if sum(R[i] for i in c) <= alvo)/len(TODOS)

g_foco = tuple(BLOCOS.index(b) for b in FOCO)
g_b1   = tuple(BLOCOS.index(b) for b in B1)

print("="*96)
print("A · MULTIPLICIDADE, com o nulo que respeita a correlacao entre parametros")
print("="*96)
print()
def estat(g):
    ps = [p_um(p, g) for p in PARS]
    return min(ps), sum(1 for x in ps if x <= 0.05), ps

pmin_f, k_f, ps_f = estat(g_foco)
pmin_b, k_b, ps_b = estat(g_b1)
# distribuicao nula: as 84 escolhas possiveis de 3 boletins
nulo = [estat(g)[:2] for g in TODOS]
p_glob_f = sum(1 for m,_ in nulo if m <= pmin_f)/len(nulo)
p_glob_k = sum(1 for _,k in nulo if k >= k_f)/len(nulo)
print("  grupo dos FOCOS (B2-V7 mar, B2-V7 jun, B3-7ha):")
print("    p minimo entre os 11 parametros : %.4f  (CaO e C:N)" % pmin_f)
print("    parametros com p <= 0,05        : %d de 11" % k_f)
print("    p GLOBAL corrigido (84 permutacoes do rotulo de bloco):")
print("      pelo minimo : %.4f      pelo numero de acertos : %.4f" % (p_glob_f, p_glob_k))
pmin_bb = pmin_b
p_glob_b = sum(1 for m,_ in nulo if m <= pmin_bb)/len(nulo)
print()
print("  grupo B1 (o do D8):")
print("    p minimo entre os 11 parametros : %.4f" % pmin_b)
print("    parametros com p <= 0,05        : %d de 11" % k_b)
print("    p GLOBAL corrigido              : %.4f" % p_glob_b)
print()
print("  Distribuicao nula do numero de acertos, sobre as 84 escolhas de 3:")
import collections
c = collections.Counter(k for _,k in nulo)
for k in sorted(c): print("    %d acertos : %2d das 84 (%.1f%%)" % (k, c[k], 100*c[k]/84))

print()
print("="*96)
print("B · REPETIBILIDADE INTERNA — o mesmo talhao V7, Marco contra Junho")
print("="*96)
print()
print("  %-24s %12s %12s %10s" % ("parametro","Marco","Junho","razao"))
rep = {}
for p in PARS:
    a = val(CRU[p]["B2 - V7"][0]); b = val(CRU[p]["B2 - Zona 1 (V7)"][0])
    r = (max(a,b)/min(a,b)) if (a and b and min(a,b)>0) else float("nan")
    rep[p] = r
    print("  %-24s %12.4g %12.4g %10.2f x" % (p[:24], a, b, r))
print("  %-24s %12s %12s %10s" % ("Textura", CRU["Textura"]["B2 - V7"][0],
                                  CRU["Textura"]["B2 - Zona 1 (V7)"][0], "MUDA"))
print()
print("  pH: 5,8 -> 5,6.  A diferenca de repeticao no MESMO talhao e 0,2 —")
print("  e o intervalo inteiro que o D8 usa (do 5,3 do B1 C4 ao 5,6 seguinte)")
print("  e 0,3. O sinal do D8 e 1,5x o ruido medido do proprio instrumento.")

print()
print("="*96)
print("C · CONFUNDIMENTO COM A DATA DE COLHEITA")
print("="*96)
print()
for d in ("03","06","07"):
    bs = [b for b in BLOCOS if DATA[b]==d]
    print("  2026-%s: %s" % (d, ", ".join(bs)))
print()
print("  Os TRES boletins do B1 sao os TRES unicos de Julho com o B4.")
print("  Os pH de Julho: 7,4 · 5,2 · 5,3 · 6,1 — amplitude 2,2.")
print("  Os pH de Marco: 7,2 · 6,6 · 5,8 · 5,6 — amplitude 1,6.")
pj = [val(CRU["pH (H2O)"][b][0]) for b in BLOCOS if DATA[b]=="07"]
pm = [val(CRU["pH (H2O)"][b][0]) for b in BLOCOS if DATA[b]=="03"]
print("  media Julho %.2f  ·  media Marco %.2f  ·  diferenca %.2f"
      % (sum(pj)/4, sum(pm)/4, sum(pj)/4-sum(pm)/4))
print("  -> a data NAO explica o D8; mas B1 = Julho e uma equivalencia exacta,")
print("     e nenhum desenho com n=9 pode separar 'ser B1' de 'ser de Julho'.")

json.dump(dict(p_min_focos=pmin_f, n_p05_focos=k_f, p_global_focos=p_glob_f,
               p_global_focos_por_acertos=p_glob_k,
               p_min_B1=pmin_b, n_p05_B1=k_b, p_global_B1=p_glob_b,
               p_por_parametro_focos=dict(zip(PARS, ps_f)),
               p_por_parametro_B1=dict(zip(PARS, ps_b)),
               repetibilidade_V7=rep),
          open(os.path.join(OUT,"c3a2_q5_global.json"),"w"), indent=1)
print()
print("escrito c3a2_q5_global.json")
