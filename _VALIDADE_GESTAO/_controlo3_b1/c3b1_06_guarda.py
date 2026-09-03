# -*- coding: utf-8 -*-
"""Q5 · o portao posto a julgar o B1 — e o buraco que a condicao 5 reescrita
deixou aberto.

Nao se responde a isto a ler o codigo. Poe-se o portao a julgar.

T1 · a afirmacao 1 do B1 («o B1 nao tem o degrau»), com tudo o que ela tem hoje.
T2 · a mesma, com o instrumento independente a DISCORDAR.
T3 · o buraco: a condicao 5 aceita `reg01_triagem.json` como prova de
     identidade. Esse ficheiro nao tem chave `alerta`. As oito unidades que ele
     EXCLUI estao na sua chave `nivel_anual` — logo estao «cobertas» e nao estao
     «em alerta». Pergunta-se ao portao se as oito excluidas tem identidade
     continua.
T4 · o mesmo com `b1_como_unidade.json`, sobre as duas parcelas que o proprio
     script declara «FORA — plantacao nova».
"""
import os
import sys

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS")
from guarda import Facto, FactoNaoValidado          # noqa: E402

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
TRI = os.path.join(VG, "reg01_triagem.json")
B1J = os.path.join(VG, "b1_como_unidade.json")
VALIDOS = ["6476415", "6476420", "8845740", "6476425"]
EXCLUIDOS = ["6705420", "6705421", "6705422", "6705424", "6705427",
             "8845729", "8845731", "8845739"]


def julga(titulo, f, texto):
    print()
    print("--- %s" % titulo)
    try:
        print(f.veredicto(texto))
        print("  *** PASSOU ***")
        return True
    except FactoNaoValidado as e:
        print(str(e).rstrip())
        return False


print("=" * 96)
print("O PORTAO SOBRE O B1")
print("=" * 96)

f1 = Facto("o B1 nao tem o degrau de 2025-26, logo e comparador",
           instrumento="NDVI Landsat 8/9, 100 cenas, 6 parcelas do IFAP",
           ficheiro="b1_como_unidade.py")
f1.confirmar_com("NDVI Sentinel-2, 9 cenas, mascara C1a+C1b", concorda=True,
                 nota="a mesma subida, +0,085 no nivel absoluto")
f1.fronteira("poligonos do IFAP, entidade externa", derivada_do_sinal=False)
f1.identidade_no_tempo(TRI, nota=VALIDOS)
julga("T1 · a afirmacao 1 do B1 como esta escrita hoje", f1,
      "o B1 nao tem o degrau")

f2 = Facto("o B1 nao tem o degrau de 2025-26, logo e comparador",
           instrumento="NDVI Landsat 8/9, 100 cenas",
           ficheiro="b1_como_unidade.py")
f2.confirmar_com("ortofoto / testemunho sobre a continuidade da cultura",
                 concorda=False, nota="nao existe; nao foi tentado")
f2.fronteira("poligonos do IFAP", derivada_do_sinal=False)
f2.identidade_no_tempo(TRI, nota=VALIDOS)
julga("T2 · a mesma, com um instrumento independente a discordar", f2,
      "o B1 nao tem o degrau")

print()
print("=" * 96)
print("O BURACO — a condicao 5 aceita o proprio ficheiro que EXCLUI as unidades")
print("=" * 96)

f3 = Facto("as OITO unidades EXCLUIDAS pela triagem tem identidade continua",
           instrumento="NDVI Landsat", ficheiro="c3b1_06_guarda.py")
f3.confirmar_com("qualquer coisa", concorda=True)
f3.fronteira("poligonos do IFAP")
f3.identidade_no_tempo(TRI, nota=EXCLUIDOS)
ok3 = julga("T3 · pedir ao portao que certifique as OITO que a triagem excluiu",
            f3, "as oito excluidas tem linha de base continua")

f4 = Facto("as duas parcelas «plantacao nova» do B1 tem identidade continua",
           instrumento="NDVI Landsat", ficheiro="c3b1_06_guarda.py")
f4.confirmar_com("qualquer coisa", concorda=True)
f4.fronteira("poligonos do IFAP")
f4.identidade_no_tempo(B1J, nota=["8845729", "8845739"])
ok4 = julga("T4 · as duas que o `b1_como_unidade.py` declara plantacao nova",
            f4, "8845729 e 8845739 tem linha de base continua")

print()
print("=" * 96)
if ok3 or ok4:
    print("RESULTADO: a condicao 5 exige um FICHEIRO, e le-lhe as chaves `nivel`/")
    print("`nivel_anual` e `alerta`. `reg01_triagem.json` e `b1_como_unidade.json`")
    print("nao escrevem `alerta` nenhuma — escrevem `excluidos` e `validos`. Logo")
    print("`alerta` vem vazia e NENHUMA unidade e marcada. O ficheiro que existe")
    print("PARA dizer quais as unidades descontinuas e aceite como prova de que")
    print("nao ha nenhuma. A condicao 5 troca uma cadeia de caracteres por um")
    print("ficheiro, mas continua a nao LER o veredicto que o ficheiro contem.")
else:
    print("RESULTADO: o portao bloqueou os dois casos. Nao ha buraco por aqui.")
print("=" * 96)
