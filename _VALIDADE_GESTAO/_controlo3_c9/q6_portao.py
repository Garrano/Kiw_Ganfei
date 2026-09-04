# -*- coding: utf-8 -*-
"""Q6 - a QUINTA encarnacao de «ausencia tratada como aprovacao».

Nao ataco a condicao 5 (ja exige ficheiro) nem a 2 (ja exige ficheiro).
Ataco o que NENHUMA das duas verifica: **que o ficheiro tenha alguma coisa a
ver com a afirmacao**. `os.path.exists` e tudo o que o portao pergunta.
"""
import json, os, sys
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS")
from guarda import Facto, FactoNaoValidado
AQUI = os.path.dirname(os.path.abspath(__file__))

print("="*90)
print("EXPLOIT 1 - a prova existe, e e o ficheiro do PROPRIO instrumento")
print("="*90)
print("O confirmador declarado e o GLO-30 (radar). A prova em disco e o")
print("c1_04_terreno_por_unidade.json - saida do LiDAR, ZERO GLO-30 la dentro.")
TER = r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS/SAIDA_C1/c1_04_terreno_por_unidade.json"
print("chaves do ficheiro de prova:", list(json.load(open(TER,encoding='utf-8'))
       ["foco ESTE (disco 90 m)"]))
print("contem 'glo' em qualquer chave/valor?",
      "glo" in open(TER,encoding='utf-8').read().lower())
f = (Facto("o terreno explica tudo", instrumento="MDT LiDAR 50 cm",
           ficheiro="inventado.py")
     .instantanea("longue duree")
     .fronteira("mascara geografica")
     .confirmar_com("GLO-30 - radar, outra plataforma", True,
                    "a ordenacao reproduz-se", prova=TER))
print()
print(f.veredicto("a estrutura decide o acontecimento"))
print("\n*** PASSOU. E EXACTAMENTE A LINHA VIVA DO C9 EM registo_de_factos.py:305.")

print()
print("="*90)
print("EXPLOIT 2 - o facto mais falso que consigo fazer passar")
print("="*90)
# um rastreio de identidade que eu proprio escrevo, agora, com duas linhas
RAST = os.path.join(AQUI, "rastreio_que_eu_inventei.json")
json.dump({"n_cenas": 999, "nivel": {"VALENCA_URBANO": 1.0, "POMAR": 1.0},
           "mantidos": ["VALENCA_URBANO", "POMAR"], "excluidos": []},
          open(RAST, "w", encoding="utf-8"))
# uma "prova" que e o ficheiro README de outra coisa qualquer
QUALQUER = r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS/MODELO_PROMPT.md"
print("prova apontada: %s (%d bytes, e um modelo de prompt em markdown)"
      % (os.path.basename(QUALQUER), os.path.getsize(QUALQUER)))
print("rastreio de identidade: escrito por mim ha 2 milissegundos, 4 chaves.")
g = (Facto("o tecido urbano de Valenca, do outro lado do rio Minho, tem o "
           "mesmo degrau que o pomar - logo o declinio e regional e nao agronomico",
           instrumento="razao entre o infravermelho proximo e o vermelho, "
                       "Sentinel-2, sobre a pasta sentinel_b1/",
           ficheiro="a_AOI_retirada_a_28_08.py")
     .confirmar_com("a mesma razao, calculada em Landsat 8/9", True,
                    "concordam a tres casas decimais", prova=QUALQUER)
     .identidade_no_tempo(RAST, nota=["VALENCA_URBANO", "POMAR"]))
print()
print(g.veredicto("o degrau e regional; nada em Ganfei o causou"))
print()
print("*** PASSOU. O facto e a RETIRADA NUMERO 1 deste dossie, palavra por palavra:")
print("    a AOI `b1` que media telhados de Valenca, 49 ficheiros em quarentena.")
print("    Tres razoes por que passou:")
print("      1. condicao 6 (fronteira) e OPCIONAL - nao a chamei, e nao disparou;")
print("      2. condicao 2 aceita QUALQUER caminho que exista em disco;")
print("      3. condicao 5 aceita um rastreio que EU escrevi, com as unidades")
print("         que EU quis listar como continuas.")
print("    E o guarda da MESMA GRANDEZA nao disparou porque escrevi 'razao entre")
print("    o infravermelho proximo e o vermelho' em vez da cadeia 'NDVI'.")
