# -*- coding: utf-8 -*-
"""C8-08 · o «1,77 ha» — existe no desenho, e a que se refere?

PERGUNTA FIXA
-------------
O C8 escreve: «O esquema anota 1,77 ha para o B1; o IFAP da 12,63 ha — factor
7,1x.» Tres coisas tem de ser verdade para essa frase valer:

  (a) o desenho anota mesmo «1,77 ha»;
  (b) a anotacao refere-se ao B1 inteiro, e nao a uma sua parte;
  (c) o numerador e o denominador medem a mesma grandeza.

Nenhuma das tres foi verificada quando a frase entrou. Aqui verifica-se (a)
por varrimento da tinta, e (b)/(c) contra a tabela de areas do gestor.

CADEIA DA AFIRMACAO, por datas de ficheiro
------------------------------------------
  CAMADA_0_ADVERSARIO.md, 28-08, §4 da lista de testes por correr:
      «O desenho escreve "1 ha" sobre o viveiro e "1,77 ha" sobre o bloco
       oeste. Medir as duas areas em pixeis ... Custo: cinco minutos.»
  — proposto como TESTE. Nao consta que tenha sido corrido.
  E o mesmo documento manda, no veredicto:
      «retirar da M1 v2 os rotulos "valvulas 1-5 / B1 / 1,77 ha" ... que sao
       prosa a viajar num mapa que sai para fora.»
"""
import os
import json

AQUI = os.path.dirname(os.path.abspath(__file__))
G2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"

tinta = json.load(open(os.path.join(AQUI, "c8_03_tinta.json")))
print("=" * 80)
print("(a) o desenho anota «1,77 ha»?")
print("=" * 80)
print("  aglomerados de tinta vermelha com >=120 px: %d" % len(tinta))
larg = max(g["larg"] for g in tinta)
print("  largura maxima de um aglomerado: %d px" % larg)
b1 = [g for g in tinta if 320 < g["x0"] < 360 and 840 < g["y0"] < 880]
if b1:
    print("  o aglomerado «B1» (duas letras) mede %d px de largura"
          % b1[0]["larg"])
    print("  => ~%.0f px por caracter a esta caligrafia" % (b1[0]["larg"] / 2.0))
    print("  => «1,77 ha» (7 caracteres) mediria ~%.0f px"
          % (7 * b1[0]["larg"] / 2.0))
print("  NENHUM aglomerado de tinta vermelha na folha inteira excede %d px de"
      % larg)
print("  largura. Nao ha, a vermelho, cadeia nenhuma com o comprimento de")
print("  «1,77 ha». Os 17 aglomerados sao circulos de valvula e o «B1».")
print()
print("  NAO ENCONTRADO no varrimento. Limite do metodo, declarado: a imagem")
print("  embebida tem 2338x1654 px (200 dpi); uma anotacao a lapis, a azul")
print("  claro ou muito fina pode ficar abaixo do limiar. Diz-se «nao")
print("  encontrado», nao «nao existe».")

print()
print("=" * 80)
print("(b) e (c) · 1,77 ha contra a tabela de areas do gestor")
print("=" * 80)
B1V = [(1, 13500), (2, 9375), (3, 12750), (4, 24550), (5, 29900)]
tot = sum(a for _, a in B1V)
print("  tabela do gestor, B1 = valvulas 1 a 5 (`ganfei_s2\\b1_divisao.py`):")
for k, a in B1V:
    print("     v%-2d %7d m2 = %.2f ha" % (k, a, a / 1e4))
print("     " + "-" * 34)
print("     B1  %7d m2 = %.2f ha  em 5 valvulas" % (tot, tot / 1e4))
print()
print("  1,77 ha contra:")
print("     o B1 da tabela do gestor (%.2f ha) ....... %.0f %% dele"
      % (tot / 1e4, 100.0 * 1.77e4 / tot))
print("     a media por valvula do B1 (%.2f ha) ...... %.0f %%"
      % (tot / 5e4, 100.0 * 1.77 / (tot / 5e4)))
print("     a valvula 1, a mais pequena (%.2f ha) .... %.0f %%"
      % (B1V[0][1] / 1e4, 100.0 * 1.77e4 / B1V[0][1]))
print("     o kiwi declarado ao IFAP no bloco (12,64 ha) %.0f %%"
      % (100.0 * 1.77 / 12.64))
print()
print("  nenhuma valvula do B1 tem 1,77 ha. A media por valvula da 1,80 ha —")
print("  proxima, e nada mais do que isso: n=5 e as areas vao de 0,94 a 2,99.")
print()
print("  E O DEFEITO DE FUNDO NAO E O NUMERADOR. Um sector de rega e uma")
print("  unidade hidraulica; uma parcela do IFAP e uma unidade administrativa;")
print("  o bloco do G19 e uma assinatura de textura em ortofoto. Dividir uma")
print("  pela outra nao mede discrepancia nenhuma — mede a diferenca entre")
print("  tres definicoes de unidade. E o proprio C7 ja diz que a area por")
print("  valvula nao sustenta quantidade nenhuma.")
print()
print("  a comparacao que SE PODE escrever, se alguma:")
print("     B1 pela tabela do gestor  %.2f ha  (tipo 1)" % (tot / 1e4))
print("     B1 pelo IFAP (C1a+C1b)    12,63 ha  (documento)")
print("     razao %.2fx — e mesmo esta compara area regada com area declarada."
      % (12.63 / (tot / 1e4)))

json.dump(dict(aglomerados_vermelhos=len(tinta), largura_max_px=larg,
               encontrado_177=False,
               b1_tabela_gestor_ha=tot / 1e4,
               media_por_valvula_ha=tot / 5e4,
               valvula_1_ha=B1V[0][1] / 1e4,
               factor_c8=round(12.63 / 1.77, 1),
               factor_com_tabela_do_gestor=round(12.63 / (tot / 1e4), 2)),
          open(os.path.join(AQUI, "c8_08_o_177.json"), "w"), indent=1)
print()
print("escrito c8_08_o_177.json")
