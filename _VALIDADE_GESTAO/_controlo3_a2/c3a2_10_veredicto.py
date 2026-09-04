# -*- coding: utf-8 -*-
"""C3/A2 · 10 — o veredicto: o D7 contra o ficheiro que ele cita, e o piso de p.

Nao toca em nada fora de `_controlo3_a2\`. Replica o bloco F2 do
`a2_solo_caracterizacao.py` sem escrever o JSON dele.
"""
import collections, csv, io, itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

R = [x for x in carrega("c3_04_registo_principal.csv")
     if "sico-Qu" in str(x.get("Doc_Type",""))]

print("="*100)
print("A · o bloco F2 do a2_solo_caracterizacao.py, replicado tal e qual")
print("="*100)
campos = ("Notes","Matrix","Method","Test_Category","Interpretation")
for c in campos:
    v = collections.Counter(str(x.get(c,""))[:52] for x in R)
    vazios = sum(n for k,n in v.items() if not k.strip())
    prof = [k for k in v if any(s in k.lower()
            for s in ("cm","profund","0-2","0-3","20","30"))]
    print("  %-16s %d vazios de %d  ·  mencao a profundidade: %s"
          % (c, vazios, len(R), prof[:1] or "nenhuma"))
print("""
  O detector procura as cadeias «cm», «profund», «0-2», «0-3», «20» e «30».
  «20» e «30» sozinhos casam com qualquer numero — se o campo `Method` dissesse
  «ISO 10930» este teste teria imprimido «mencao a profundidade: sim». Nao e um
  detector de profundidade: e um detector de dois digitos, aplicado a cinco
  campos que nao sao de colheita. Passou por sorte, nao por desenho.
""")

print("="*100)
print("B · o D7 contra `c3_07_registos_colocados.csv`, que e o ficheiro que cita")
print("="*100)
t = io.open(r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C3"
            r"\c3_07_registos_colocados.csv", encoding="utf-8", errors="replace").read()
C = [x for x in csv.DictReader(io.StringIO(t)) if "sico-Qu" in x["Doc_Type"]]
seen = {}
for x in C:
    seen[x["Terrain_Block_Parcel"]] = (x["classe_posicao"], x["E"], x["N"],
                                       x["d_foco_OESTE_m"], x["d_foco_ESTE_m"],
                                       x["pct_defice_2026"])
RAIO = 90.0    # `c3_07_georreferenciar.py`: discos_dos_focos(pomar, raio=90.0)
print("  %-20s %-16s %10s %10s %8s %s" %
      ("boletim","classe","E","dOESTE","dESTE","defice26"))
ncoord = ndentro = 0
for b, (cl, E, N, dO, dE, df) in seen.items():
    tem = bool(str(E).strip()); ncoord += tem
    d = min([float(x) for x in (dO, dE) if str(x).strip()] or [1e9])
    dentro = tem and d <= RAIO; ndentro += dentro
    print("  %-20s %-16s %10s %10s %8s %6s%s"
          % (b, cl, E or "—", dO or "—", dE or "—", df or "—",
             "   <-- DENTRO do disco r=90 m" if dentro else ""))
print()
print("  boletins COM coordenada em disco : %d de 9   (o D7 escreve «0 de 9»)" % ncoord)
print("  boletins dentro de um disco r=90 : %d de 9   (o D7 escreve «0»)" % ndentro)
print("""
  O D7 diz «Zero tem coordenada, zero estao inequivocamente dentro de um foco».
  O ficheiro que ele nomeia como fonte poe SEIS dos nove numa posicao UTM e
  poe UM deles — `B3 - 7 ha`, o bloco do foco ORIENTAL — a 67 m do centro,
  dentro do disco de r = 90 m que toda a cadeia usa.

  A CONCLUSAO do D7 sobrevive: as seis posicoes sao de classe COLOCADO (2),
  COLOCADO-BLOCO (1), INFERIDO (2) e AMBIGUO (1), e as tres primeiras vem da
  particao por valvula que o C7 desqualifica para QUANTIDADES. Mas a razao
  escrita esta errada, e e uma razao verificavel contra um ficheiro.
""")

print("="*100)
print("C · o piso de p: este desenho podia ter dito alguma coisa?")
print("="*100)
print("""
  Com 9 boletins e um grupo de 3, ha C(9,3) = 84 atribuicoes. O p unilateral
  mais pequeno atingivel e 1/84 = 0,0119 — que sai se e so se os TRES boletins
  do grupo forem os tres valores mais baixos.

  Portanto o desenho NAO e impotente: podia ter produzido p = 0,012.
  O que aconteceu foi outra coisa — a configuracao real do B1 da p = 0,2500,
  porque o terceiro boletim do B1 e o MAIOR dos nove.

  Isto importa para a Q2: a hipotese «so podia falhar» nao e uma propriedade
  do desenho. E uma propriedade da INTERPRETACAO que se decidiu dar-lhe. O
  desenho tinha um ramo de confirmacao a p = 0,012 e ele nao foi accionado.
""")
print("="*100)
print("D · a coerencia interna do proprio dossie")
print("="*100)
print("""
  LISTA_FINAL, seccao E, retirada 18:
    «O B1 e o comparador sem degrau» — zero instrumentos independentes, a
    recta ganha porque o bloco esta em subida, e o veredicto dependia de um
    limiar inventado.
  LISTA_FINAL, seccao F (o que NAO se pode escrever):
    «que o B1 e comparador de coisa nenhuma».
  LISTA_FINAL, D8, publicado hoje:
    «Os dois pH mais baixos — 5,2 e 5,3 — sao do B1, QUE NAO DECLINA: sobe
     +0,092 enquanto os focos descem -0,085.»

  O D8 usa o B1 como comparador de nao-declinio. E a retirada 18, com outro
  instrumento a montante.
""")
