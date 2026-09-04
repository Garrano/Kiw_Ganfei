# -*- coding: utf-8 -*-
"""C3/A2 · 04 — Q5: os OUTROS onze parametros, com a mesma disciplina do D8.

O D8 olhou o pH. Aqui corre-se o mesmo desenho nos doze, e declara-se a
pergunta ANTES: para cada parametro, o boletim do bloco do foco ocupa uma
posicao extrema entre os nove?

TRES definicoes de «afectado», todas em disco, nenhuma inventada aqui:
  D-a  pct_defice_2026 da unidade em que o registo foi colocado
       (`c3_07_georreferenciacao.json`) — 6 dos 9 boletins tem uma.
  D-b  distancia ao foco mais proximo, do mesmo ficheiro.
  D-c  binaria: o boletim e do bloco que CONTEM um disco de foco (r=90 m).
Nenhuma delas atribui AREA a valvula nenhuma — e o C7 proibe area, nao posicao.
"""
import itertools, json, os, re, sys
from fractions import Fraction

OUT = os.path.dirname(os.path.abspath(__file__))
CRU = json.load(open(os.path.join(OUT, "c3a2_matriz_cru.json")))

BLOCOS = ["Erica 2016 R","Erica 2016 E","B2 - V7","B3 - 7 ha",
          "B2 - Zona 1 (V7)","B1 C1","B1 C3","B1 C4","Parcela B4"]
# de c3_07_registos_colocados.csv / c3_07_georreferenciacao.json
POS = {"Erica 2016 R": (2.8, 219.0), "Erica 2016 E": (2.8, 219.0),
       "B2 - V7": (21.2, 120.0), "B2 - Zona 1 (V7)": (21.2, 120.0),
       "B3 - 7 ha": (46.9, 67.0), "Parcela B4": (6.2, 379.0)}
FOCO = ("B2 - V7", "B2 - Zona 1 (V7)", "B3 - 7 ha")   # D-c
B1 = ("B1 C1", "B1 C3", "B1 C4")

def val(s):
    m = re.search(r"[-+]?\d+(?:[.,]\d+)?", str(s))
    return float(m.group(0).replace(",", ".")) if m else None

def postos(vals):
    o = sorted(range(len(vals)), key=lambda i: vals[i]); r = [0.0]*len(vals); i = 0
    while i < len(o):
        j = i
        while j+1 < len(o) and vals[o[j+1]] == vals[o[i]]: j += 1
        for k in range(i, j+1): r[o[k]] = (i+j)/2.0 + 1
        i = j+1
    return r

def spearman(x, y):
    rx, ry = postos(x), postos(y); n = len(x)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = (sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry)) ** 0.5
    return num/den if den else float("nan")

def perm_p(vals, grupo_idx, sentido="menor"):
    """p exacto: a soma de postos do grupo e tao extrema por acaso?"""
    R = postos(vals); n = len(vals); k = len(grupo_idx)
    alvo = sum(R[i] for i in grupo_idx)
    tot = list(itertools.combinations(range(n), k))
    if sentido == "menor":
        c = sum(1 for g in tot if sum(R[i] for i in g) <= alvo)
    else:
        c = sum(1 for g in tot if sum(R[i] for i in g) >= alvo)
    return c/len(tot), alvo, len(tot)

PARS = [p for p in CRU if "Textura" not in p]
print("="*100)
print("Q5 · os DOZE parametros com a disciplina do D8 — nao so o pH")
print("="*100)
print()
print("%-22s %9s %9s %9s | %8s %8s | %7s" %
      ("parametro","B3(foco E)","B2V7 mar","B2V7 jun","rho def","rho dist","p focos"))
print("-"*100)
linhas = {}
for p in PARS:
    v = [val(CRU[p][b][0]) for b in BLOCOS]
    cens = [CRU[p][b][2] for b in BLOCOS]
    R = postos(v)
    r_b3 = R[BLOCOS.index("B3 - 7 ha")]
    r_v7m = R[BLOCOS.index("B2 - V7")]
    r_v7j = R[BLOCOS.index("B2 - Zona 1 (V7)")]
    # rho contra deficit e contra distancia, so nos 6 colocados
    col = [b for b in BLOCOS if b in POS]
    vv = [val(CRU[p][b][0]) for b in col]
    rho_d = spearman(vv, [POS[b][0] for b in col])
    rho_x = spearman(vv, [POS[b][1] for b in col])
    pf, alvo, nt = perm_p(v, [BLOCOS.index(b) for b in FOCO], "menor")
    print("%-22s %9s %9s %9s | %8.3f %8.3f | %7.4f"
          % (p[:22], "%.1f/9" % r_b3, "%.1f/9" % r_v7m, "%.1f/9" % r_v7j,
             rho_d, rho_x, pf))
    linhas[p] = dict(posto_B3=r_b3, posto_V7_mar=r_v7m, posto_V7_jun=r_v7j,
                     rho_deficit=rho_d, rho_distancia=rho_x, p_focos_menores=pf,
                     censurados=sum(1 for c in cens if c))
print()
print("  posto 1 = o valor MAIS BAIXO dos nove.  rho def: negativo = mais")
print("  deficit com menos do parametro.  p focos: teste de permutacao exacto,")
print("  84 combinacoes, H = 'os tres boletins dos blocos com foco sao os mais")
print("  baixos'. Unilateral, e declarado antes de correr.")
print()
print("="*100)
print("O contraste com o D8, no mesmo formato")
print("="*100)
R = postos([val(CRU["pH (H2O)"][b][0]) for b in BLOCOS])
pB1, alvo, nt = perm_p([val(CRU["pH (H2O)"][b][0]) for b in BLOCOS],
                       [BLOCOS.index(b) for b in B1], "menor")
print("  pH · B1 mais baixo que o resto : p = %.4f  (o D8)" % pB1)
print("  pH · focos mais baixos         : p = %.4f" % linhas["pH (H2O)"]["p_focos_menores"])
print()
print("  TEXTURA (classe, nao ordenavel):")
for b in BLOCOS: print("    %-20s %s" % (b, CRU["Textura"][b][0]))
json.dump(linhas, open(os.path.join(OUT, "c3a2_q5.json"), "w"), indent=1)
print()
print("escrito c3a2_q5.json")
