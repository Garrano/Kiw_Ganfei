# -*- coding: utf-8 -*-
"""C3/A2 · 11 — o que os SEIS boletins colocaveis dizem, sozinhos.

O D8 conclui «a acidez nao acompanha o declinio» a partir dos nove. Tres dos
nove (o B1) nao tem posicao nenhuma. Este ficheiro pergunta o que dizem os
SEIS que tem — usando o `pct_defice_2026` da unidade em que a C3 os colocou,
que e um numero em disco e nao uma quantidade por valvula (o C7 proibe AREA
por valvula, nao posicao).
"""
import itertools, json, os
from fractions import Fraction

# unidade distinta -> (pH medio dos boletins dela, pct_defice_2026, d_foco_min)
U = {
    "Erica Novo (2 boletins: R 7,2 · E 6,6)": ((7.2+6.6)/2, 2.8, 219.0),
    "B4 (1 boletim: 6,1)":                    (6.1,          6.2, 379.0),
    "v7 / B2 (2 boletins: mar 5,8 · jun 5,6)":((5.8+5.6)/2, 21.2, 120.0),
    "B3 (1 boletim: 5,6)":                    (5.6,         46.9,  67.0),
}
print("="*98)
print("As QUATRO unidades distintas com posicao, ordenadas por defice de 2026")
print("="*98)
print()
print("  %-42s %6s %9s %9s" % ("unidade","pH","defice%","d_foco m"))
for k,(ph,df,d) in sorted(U.items(), key=lambda kv: kv[1][1]):
    print("  %-42s %6.2f %9.1f %9.0f" % (k, ph, df, d))
print()
ph = [U[k][0] for k in U]; df = [U[k][1] for k in U]; dd = [U[k][2] for k in U]

def postos(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r=[0.0]*len(v); i=0
    while i < len(o):
        j=i
        while j+1<len(o) and v[o[j+1]]==v[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2.0+1
        i=j+1
    return r

def rho(x,y):
    rx,ry=postos(x),postos(y); n=len(x); mx=sum(rx)/n; my=sum(ry)/n
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den

r_obs = rho(ph, df)
# p exacto por permutacao completa das 4! = 24 ordens
perm = list(itertools.permutations(range(4)))
c = sum(1 for p in perm if rho([ph[i] for i in p], df) <= r_obs)
print("  Spearman(pH, defice 2026) = %+.3f   sobre n = 4 unidades distintas" % r_obs)
print("  p unilateral exacto (24 permutacoes) = %s = %.4f" % (Fraction(c,24), c/24))
r2 = rho(ph, dd); c2 = sum(1 for p in perm if rho([ph[i] for i in p], dd) >= r2)
print("  Spearman(pH, distancia ao foco) = %+.3f  ·  p unilateral = %.4f" % (r2, c2/24))
print()
print("""  A relacao e PERFEITAMENTE monotona e no sentido CONTRARIO ao do D8: quanto
  mais acido, maior o defice de 2026 e menor a distancia ao foco. Com n = 4 o
  p mais pequeno atingivel e 1/24 = 0,0417, e e esse que sai.

  NAO estou a afirmar que a acidez causa o declinio. Estou a afirmar tres
  coisas, e so estas:
    1 · a mesma tabela de nove boletins sustenta a leitura oposta a do D8,
        assim que se restringe aos que tem posicao;
    2 · o que inverte o sinal e a inclusao dos TRES boletins do B1 — os unicos
        sem posicao nenhuma, e os unicos cujo grupo a seccao F da LISTA_FINAL
        proibe usar como comparador;
    3 · uma afirmacao cujo sinal depende de incluir ou nao o unico grupo que o
        registo proibe usar nao e um facto: e uma escolha de analise nao
        declarada. E a regra do multiverso desta CLAUDE.md — relatar a
        distribuicao, nao a corrida preferida.
""")
print("="*98)
print("O piso de ruido, medido com o unico talhao repetido")
print("="*98)
print("""
  `B2 - V7` (2026-03-03) pH 5,8  ·  `B2 - Zona 1 (V7)` (2026-06-17) pH 5,6
  -> repeticao no MESMO talhao: 0,2 unidades de pH = factor 1,58 em [H+].
  O intervalo que o D8 usa (5,3 do B1 C4 ao 5,6 seguinte) = 0,3 unidades =
  factor 2,0 em [H+]. **1,3 a 1,6 vezes o ruido do proprio instrumento.**
  E o S9 da CAMADA_1 ja tinha escrito a regra: «nenhuma diferenca quimica
  entre blocos abaixo de um factor de 2 e interpretavel com estes dados».
""")
