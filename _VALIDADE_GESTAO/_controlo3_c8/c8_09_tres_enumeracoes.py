# -*- coding: utf-8 -*-
"""C8-09 · sector, valvula, parcela — tres enumeracoes da mesma rede.

PERGUNTA FIXA
-------------
A tabela «Debito dos Sectores» e informacao quantitativa do documento que
ninguem usou. **Sustenta ou contradiz alguma coisa?**

  H (a testar): sector = valvula. Se for verdade, a dispersao dos caudais por
  sector tem de ser da ordem da dispersao das areas por valvula — um sector
  grande consome mais.

  Falsifica-se se as duas dispersoes diferirem por mais de uma ordem de
  grandeza.

O QUE ISTO NAO DECIDE: nao converte caudal em area (a tabela nao declara
tempo de rega nem area), e nao mapeia sector em valvula. Diz se o mapeamento
1:1 e possivel.
"""
import os
import json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))

DEB = dict(A=65.0, B=85.0, C=90.5, D=96.8, E=87.6, F=79.1, G=99.9, H=91.5,
           I=78.5, J=71.6, L=56.8, M=55.3, N=82.7)
AREAS = {6: 25000, 7: 25100, 8: 28200, 9: 18200, 10: 24000, 11: 24650,
         12: 27500, 13: 25300, 14: 25850, 15: 11400, 16: 17300, 17: 20500,
         1: 13500, 2: 9375, 3: 12750, 4: 24550, 5: 29900,
         18: 5500, 19: 12500, 20: 23000, 21: 2300, 22: 10400, 23: 1500,
         27: 14000}
SOLTA_2425 = 17000     # «24·25» vem agregado na tabela

d = np.array(sorted(DEB.values()))
a = np.array(sorted(AREAS.values()) + [SOLTA_2425])
L = "=" * 78
print(L)
print("A · as tres enumeracoes")
print(L)
print("  sectores impressos na tabela de debito ......... %2d  (A..N, sem K)" % len(DEB))
print("  numeros de valvula circulados no desenho ....... 17 legiveis (1..17),")
print("      e um 18.o bloco anotado a leste da v17 cujo numero nao e legivel")
print("      a 200 dpi. O CAMADA_0_CERTIFICADO ja registava «pelo menos 18».")
print("  entradas na tabela de areas do gestor .......... %2d  (1..25 e 27,"
      % (len(AREAS) + 1))
print("      com «24·25» agregado numa linha; nao ha 26)")
print()
print("  tres enumeracoes, tres cardinalidades: 13, 18, 25. Nenhuma e funcao")
print("  simples de outra.")

print()
print(L)
print("B · a hipotese sector = valvula")
print(L)
print("  debito por sector (m3): min %.1f  max %.1f  mediana %.1f  razao %.2fx"
      % (d.min(), d.max(), np.median(d), d.max() / d.min()))
print("  area por valvula (m2):  min %d  max %d  mediana %.0f  razao %.1fx"
      % (a.min(), a.max(), np.median(a), a.max() / float(a.min())))
print("  coef. de variacao:  debito %.3f   ·   area %.3f"
      % (d.std(ddof=1) / d.mean(), a.std(ddof=1) / a.mean()))
print()
print("  razao entre as duas dispersoes: %.1fx" % ((a.max() / a.min()) / (d.max() / d.min())))
print("  H FALSIFICADA. Os sectores estao dimensionados a carga hidraulica")
print("  aproximadamente igual (1,8x de amplitude); as valvulas do gestor vao")
print("  de 0,15 a 2,99 ha (20x). **Sector e valvula nao sao a mesma particao**,")
print("  e nenhuma area sai de um caudal.")

print()
print(L)
print("C · o que a tabela sustenta, e o que nao sustenta")
print(L)
print("  SUSTENTA o C7 por uma via nova e documental: a atribuicao de area por")
print("  valvula nao tem no desenho fundamento nenhum, porque o desenho conta")
print("  sectores e o gestor conta valvulas, e sao %d contra %d."
      % (len(DEB), len(AREAS) + 1))
print("  SUSTENTA que o projecto de 2009 ja sectorizava o troco oeste — ha")
print("  tramado de sector impresso nos dois trocos (c8_04_sectores.json).")
print("  NAO SUSTENTA nenhuma area, nenhum factor, nenhuma sobre-extensao")
print("  quantificada: a tabela declara m3 e nao declara nem area nem tempo.")
print("  total dos caudais tabelados: %.1f m3." % sum(DEB.values()))
print("  NAO TESTAVEL, e fica escrito: o mapeamento sector -> valvula. Fecha-o")
print("  a tabela de sectores com area, ou o gestor. Nao o fecha mais calculo.")

json.dump(dict(n_sectores=len(DEB), n_valvulas_desenho=17,
               n_entradas_tabela_gestor=len(AREAS) + 1,
               debito_min=float(d.min()), debito_max=float(d.max()),
               debito_razao=float(d.max() / d.min()),
               area_min=int(a.min()), area_max=int(a.max()),
               area_razao=float(a.max() / a.min()),
               cv_debito=float(d.std(ddof=1) / d.mean()),
               cv_area=float(a.std(ddof=1) / a.mean()),
               total_debito_m3=sum(DEB.values()),
               h_sector_igual_valvula="FALSIFICADA"),
          open(os.path.join(AQUI, "c8_09_tres_enumeracoes.json"), "w"), indent=1)
print()
print("escrito c8_09_tres_enumeracoes.json")
