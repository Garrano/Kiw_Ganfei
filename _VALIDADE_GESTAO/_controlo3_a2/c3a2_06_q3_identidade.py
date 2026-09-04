# -*- coding: utf-8 -*-
"""C3/A2 · 06 — Q3: «B1 C1/C3/C4» e o sector B1? A retirada 9 outra vez?

DUAS entidades chamadas B1, e desta vez nao e a AOI de Valenca:

  (i)  o B1 DA EXPLORACAO — valvulas 1 a 5, areas tabeladas 13500+9375+12750+
       24550+29900 = 90.075 m2 = **9,01 ha**, entre as duas coordenadas duras
       do gestor E529500 N4654010 e E530054 N4654413 (R2 G36 / `b1_divisao.py`).
       E deste vocabulario que vem o rotulo «B1 Cn» dos boletins.

  (ii) o SECTOR B1 medido opticamente — E 529 495-530 063 x N 4 653 832-
       4 654 477, seis parcelas do IFAP, **12,63 ha** (`b1_como_unidade.py`).

Este ficheiro mede a diferenca entre as duas, com os poligonos do IFAP em disco.
"""
import json, os
import numpy as np
from shapely.geometry import shape, box, LineString
from shapely.ops import transform as sht
from pyproj import Transformer

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CUL_B1 = [6476415, 8845729, 6476420, 8845739, 8845740, 6476425]
VALIDOS = [6476415, 6476420, 8845740, 6476425]
CAIXA = (529495.0, 4653832.0, 530063.0, 4654477.0)      # sector B1 (optico)
A = (529500.0, 4654010.0); B = (530054.0, 4654413.0)    # gestor, R2 G36
TAB_HA = 9.01                                            # tabela de areas, v1-v5

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
GEO = {int(f["properties"]["CUL_ID"]): para(shape(f["geometry"])).buffer(0)
       for f in KF if int(f["properties"]["CUL_ID"]) in CUL_B1}

eixo = LineString([A, B])
print("="*96)
print("Q3 · as duas entidades chamadas B1")
print("="*96)
print()
print("  eixo do gestor: %.0f m, azimute %.1f graus"
      % (eixo.length, np.degrees(np.arctan2(B[0]-A[0], B[1]-A[1]))))
print()
print("  %-10s %7s  %8s %8s  %s" % ("CUL_ID","ha","d(eixo)","N min","dentro da caixa optica?"))
tot = 0.0
for c in CUL_B1:
    g = GEO[c]; ha = g.area/1e4; tot += ha
    d = g.distance(eixo)
    ymin = g.bounds[1]
    dentro = box(*CAIXA).contains(g)
    print("  %-10d %7.2f  %8.0f %8.0f  %s%s"
          % (c, ha, d, ymin, "sim" if dentro else "NAO",
             "   <- valida na triagem" if c in VALIDOS else ""))
print("  %-10s %7.2f" % ("TOTAL", tot))
print()
print("  area do IFAP no sector          : %.2f ha" % tot)
print("  area TABELADA do B1 do gestor   : %.2f ha  (valvulas 1 a 5)" % TAB_HA)
print("  diferenca                       : %+.2f ha  (%+.0f %%)"
      % (tot-TAB_HA, 100*(tot-TAB_HA)/TAB_HA))
print()
# quanto do IFAP cai a SUL do inicio do eixo do gestor
sul = box(CAIXA[0], CAIXA[1], CAIXA[2], A[1])
hs = sum(g.intersection(sul).area/1e4 for g in GEO.values())
print("  kiwi do sector a SUL de N%.0f (o extremo SW que o gestor deu): %.2f ha"
      % (A[1], hs))
print("  ou seja %.0f %% da area medida como «B1» esta fora do segmento que o"
      % (100*hs/tot))
print("  gestor delimitou como B1.")
print()
# corredor de 150 m em torno do eixo
for r in (100.0, 150.0, 200.0):
    cor = eixo.buffer(r)
    h = sum(g.intersection(cor).area/1e4 for g in GEO.values())
    print("  dentro de %3.0f m do eixo do gestor: %5.2f ha de %5.2f (%.0f %%)"
          % (r, h, tot, 100*h/tot))
print()
print("="*96)
print("E os rotulos «B1 Cn» — ha prova de que C1, C3 e C4 sao deste sector?")
print("="*96)
print("""
  NAO ha, e o proprio registo tem o contra-exemplo. A R2 G35 enumera oito
  parcelas SOLTAS, com area e SEM posicao — e duas delas chamam-se
  **B1C5** e **B1C6** (`CAMADA_0_REVISAO_R2.md`, linhas 220-221). Portanto a
  numeracao «B1 Cn» da exploracao inclui parcelas cuja posicao o proprio
  dossie declara desconhecida. Nada no corpus liga C1, C3 ou C4 a uma valvula,
  a um poligono ou a uma coordenada: a unica ligacao e o prefixo do rotulo.

  A tabela de colocacao da C3 assume-o explicitamente e assume-o como nota, nao
  como prova — `c3_07_georreferenciar.py`:
      "B1 C1": (None, None, "FORA DA BANDA", "sub-parcelas do B1 sem posicao")
  «sub-parcelas do B1» e a conclusao, nao o dado.
""")
