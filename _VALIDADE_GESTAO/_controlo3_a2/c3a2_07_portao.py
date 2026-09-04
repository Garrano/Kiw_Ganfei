# -*- coding: utf-8 -*-
"""C3/A2 · 07 — Q6: o portao posto a julgar o D7, o D8 e o D9, e atacado.

Reconstroi os tres factos exactamente como estao em `registo_de_factos.py` e
depois corre seis ataques.
"""
import json, os, sys
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS")
from guarda import Facto, FactoNaoValidado

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
TRI = os.path.join(VG, "reg01_triagem.json")
T = json.load(open(TRI, encoding="utf-8"))
print("reg01_triagem.json  mantidos=%d  excluidos=%d"
      % (len(T.get("mantidos", [])), len(T.get("excluidos", []))))
print("  excluidos:", T.get("excluidos"))
print()
B1_SEIS = ["6476415","8845729","6476420","8845739","8845740","6476425"]
B1_QUATRO = ["6476415","6476420","8845740","6476425"]

def corre(titulo, f, texto):
    print("-"*92)
    print(titulo)
    try:
        print(f.veredicto(texto))
        print(">>> PASSOU")
        return True
    except FactoNaoValidado as e:
        print(str(e))
        print(">>> BLOQUEOU")
        return False

def D8(**kw):
    f = Facto("D8 · a acidez do solo nao acompanha o declinio",
              instrumento=kw.get("instr", "pH(H2O) em 9 boletins — quimica, nao optica"),
              ficheiro="a2_solo_caracterizacao.py")
    if kw.get("inst", True):
        f.instantanea("pH de uma colheita, sem serie")
    f.fronteira("codigo de bloco do laboratorio")
    f.confirmar_com(kw.get("conf", "serie optica do B1 (Landsat 100 cenas + Sentinel-2)"),
                    kw.get("concorda", True),
                    "os dois pH mais baixos, 5,2 e 5,3, sao do B1, que SOBE "
                    "+0,092 enquanto os focos descem -0,085")
    if kw.get("unid"):
        f.identidade_no_tempo(TRI, nota=kw["unid"])
    return f

print("="*92); print("T0 · os tres factos como estao no registo"); print("="*92)
d7 = Facto("D7 · os boletins A2 nao podem testar afectado contra nao afectado",
           instrumento="9 boletins de fisico-quimica do solo",
           ficheiro="a2_solo_caracterizacao.py") \
    .instantanea("cada boletim e uma data unica; nao ha serie a comparar") \
    .fronteira("codigo de bloco escrito pelo laboratorio") \
    .nao_testavel("nenhum boletim tem coordenada; 3 de 9 sao do sector B1")
corre("D7", d7, "0 de 9 com coordenada")
corre("D8", D8(), "hipotese pre-registada que so podia falhar, e falhou")
d9 = Facto("D9 · faltam CTC e saturacao em bases",
           instrumento="inventario dos 12 parametros e de 5 campos",
           ficheiro="a2_solo_caracterizacao.py") \
    .instantanea("e um inventario, nao uma medicao") \
    .nao_testavel("e uma ausencia documental")
corre("D9", d9, "a quimica que existe e de acima da camada suspeita")

print()
print("="*92)
print("T1 · o confirmador do D8 e um instrumento independente, ou e a OUTRA")
print("     METADE da propria afirmacao?")
print("="*92)
print("""
  A frase do D8 tem duas partes:
    (a) os dois pH mais baixos sao 5,2 e 5,3, e sao do B1  <- quimica
    (b) o B1 nao declina                                    <- NDVI
  A conclusao «a acidez nao acompanha o declinio» so existe se AMBAS forem
  verdadeiras. O confirmador nao esta a REPETIR (a) com outra fisica: esta a
  FORNECER (b). Nao ha corroboracao nenhuma — ha uma premissa a ser contada
  como confirmacao. O portao nao distingue as duas coisas, e nao tem como.
""")
print("  PROVA de que o portao nao olha para o conteudo: troco o confirmador")
print("  por um instrumento inventado e a passagem e identica.")
corre("T1a · confirmador substituido por 'contagem de nuvens em 1997'",
      D8(conf="contagem de nuvens sobre Braga em 1997"),
      "hipotese pre-registada que so podia falhar")

print()
print("="*92)
print("T2 · e se o confirmador se chamasse NDVI, que e o que ele e?")
print("="*92)
corre("T2a · confirmador = 'NDVI Landsat + NDVI Sentinel-2'",
      D8(conf="NDVI Landsat 100 cenas + NDVI Sentinel-2"),
      "idem")
print("""
  Passa. O bloqueio de indice igual do `veredicto()` so dispara quando o
  instrumento DO FACTO contem NDVI/NDMI/NDRE/EVI/SAVI/NDWI. O do D8 e quimica,
  por isso a regra nem chega a ser avaliada. E correcto para o caso geral —
  quimica confirmada por optica E cruzamento de fisicas. Nao e correcto aqui,
  porque o que a optica confirma nao e o pH: e a outra metade da frase.
""")

print("="*92)
print("T3 · o `instantanea()` do D8 e legitimo?")
print("="*92)
print("""
  O D8 assina «pH de uma colheita, sem serie» e com isso dispensa a condicao 5.
  Mas a proposicao que ele publica — «o B1 NAO DECLINA enquanto os focos
  descem» — e uma comparacao de 2017-24 contra 2025-26 sobre seis parcelas.
  A parte instantanea e a que nao precisa da condicao 5; a parte que precisa
  entrou pelo `confirmar_com`, que nao a interroga.

  Prova: se a condicao 5 fosse aplicada as unidades que a frase usa —
""")
for lista, nome in ((B1_SEIS, "as SEIS parcelas do sector B1"),
                    (B1_QUATRO, "as QUATRO que a triagem manteve")):
    corre("T3 · D8 temporal, com %s" % nome,
          D8(inst=False, unid=lista), "idem")

print()
print("="*92)
print("T4 · o D7 e o D9: o `instantanea()` deles e legitimo?")
print("="*92)
print("""
  D9 · SIM, sem reserva. E um inventario de um conjunto fixo de documentos.
  D7 · SIM na letra, mas a razao assinada esta errada: «cada boletim e uma
       data unica; nao ha serie a comparar». Ha: `B2 - V7` (2026-03-03) e
       `B2 - Zona 1 (V7)` (2026-06-17) sao o MESMO talhao em duas datas —
       mesma valvula 7, ficheiros `B2_V7__Marc_o_26.pdf` e
       `B2_V7__Junho_26.pdf`. O conjunto tem 8 talhoes e 9 boletins.
       A conclusao do D7 nao muda; a razao tem de mudar, e o «n = 9» tambem.
""")
