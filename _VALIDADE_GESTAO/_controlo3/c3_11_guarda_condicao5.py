# -*- coding: utf-8 -*-
"""Q6 — o que a condicao 5 do `guarda.py` ainda deixa passar.

Nao se responde a esta pergunta lendo o codigo. Responde-se pondo o portao a
julgar a afirmacao DE HOJE — «os dois focos de Ganfei sao o pior e o segundo
pior da regiao» — com tudo o que a REG-01 refeita tem, e vendo se ele a deixa
sair. Se deixar, a condicao 5 nao cobre o proximo erro.
"""
import os
import sys

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS")
from guarda import Facto, FactoNaoValidado

print("=" * 96)
print("1 · A AFIRMACAO DE HOJE, apresentada ao portao com tudo o que ela tem")
print("=" * 96)
f = Facto("os dois focos de Ganfei sao o pior e o segundo pior da regiao",
          instrumento="NDVI Landsat 8/9, degrau 2025-26 menos 2017-24, 29 blocos",
          ficheiro="reg01_triagem_descontinuidade.py",
          comparacao_temporal=True)
f.confirmar_com("ortofoto DGT 2007-2025, fraccao sem coberto", concorda=True,
                nota="data a exclusao dos 5 do 297313")
f.confirmar_com("serie anual do Landsat", concorda=True, nota="o colapso e de 2024")
f.identidade_no_tempo("ortofoto DGT + serie anual",
                      nota="8 blocos com mudanca de uso saem")
try:
    print(f.veredicto("os focos de Ganfei sao o pior e o segundo pior"))
    print()
    print("  *** O PORTAO AUTORIZA. ***")
except FactoNaoValidado as e:
    print(str(e).rstrip())

print()
print("=" * 96)
print("2 · E autoriza, apesar de TUDO ISTO ser verdade ao mesmo tempo")
print("=" * 96)
for i, x in enumerate([
    "a identidade no tempo foi verificada para os 8 blocos EXCLUIDOS e para "
    "NENHUM dos 29 mantidos nem para os dois focos (c3_10: 13 dos 29 parecem "
    "pomar jovem, com nivel de 2017 entre 0,555 e 0,754);",
    "as duas unidades de Ganfei sao RECORTES INTERNOS de um pomar de 30 ha, "
    "escolhidos onde o problema esta; as 29 comparadoras sao parcelas inteiras, "
    "nenhuma recortada (c3_06);",
    "a mascara do foco ORIENTAL leva `& COM`, altura do CHM do voo de 06-07-2025, "
    "que a propria LISTA_FINAL (C2) declara POS-TRATAMENTO — e sem esse filtro o "
    "foco cai do 1.o para o 3.o lugar (c3_06);",
    "a mediana regional que serve de controlo tem 12 dos 29 blocos do PROPRIO "
    "dono do pomar em estudo (c3_04);",
    "a margem que sustenta «o segundo pior» e 0,0200, e o bootstrap de anos "
    "poe P(margem <= 0) = 0,252 (c3_03, c3_04).",
]):
    print("  %d · %s" % (i + 1, x))

print()
print("=" * 96)
print("3 · POR ONDE E QUE ELA PASSA — tres buracos, por ordem de gravidade")
print("=" * 96)
print("""
  A · `identidade_no_tempo(instrumento, ok=True)` — o `ok` tem valor por
      omissao VERDADEIRO. Basta escrever o nome de um instrumento para a
      condicao ficar cumprida. Nao ha teste: ha declaracao. As condicoes 3 e 4
      recebem NUMEROS (`ancoras` recebe duas amostras, `reproduz` recebe duas
      matrizes) e calculam. A 5 recebe uma cadeia de caracteres e acredita.
      Demonstra-se abaixo.

  B · `comparacao_temporal=False` por omissao, e quem o poe a True e o proprio
      analista. O A3 so e bloqueado no auto-teste porque o autor do auto-teste,
      que ja sabia a resposta, o construiu com a bandeira ligada. Um facto
      temporal declarado sem a bandeira passa pelas quatro condicoes antigas
      como se a quinta nao existisse.

  C · As cinco condicoes interrogam o INSTRUMENTO (1,2,3,4) e a UNIDADE NO
      TEMPO (5). Nenhuma interroga a UNIDADE NO ESPACO: de onde veio a mascara,
      e se ela foi derivada do sinal que se vai medir. Essa e a regra de higiene
      que a CLAUDE.md poe em primeiro lugar — «nunca derivar uma mascara do
      sinal que se vai medir», a licao do `fazer_masks_v2.py` — e e a unica das
      regras escritas do projecto que NAO tem condicao no portao.
""")

print("=" * 96)
print("4 · A DEMONSTRACAO do buraco A — a condicao 5 cumpre-se com uma mentira")
print("=" * 96)
g = Facto("os cinco blocos do 297313 sao 2 a 4x piores que Ganfei",
          instrumento="NDVI Sentinel-2", ficheiro="reg01_landsat.py",
          comparacao_temporal=True)
g.confirmar_com("NDVI Landsat 8/9, 100 cenas", concorda=True)
g.identidade_no_tempo("declaracao do IFAP, campanha 2026")
try:
    print(g.veredicto("ha blocos vizinhos muito piores"))
    print()
    print("  *** O A3 — o veredicto que a condicao 5 foi escrita para bloquear —")
    print("      passa outra vez, com UMA LINHA a mais e nenhum dado a mais.")
    print("      A declaracao do IFAP cobre uma campanha; a propria guarda de")
    print("      cultura de `reg01_landsat.py` escreve que ela NAO verifica a")
    print("      continuidade. Mesmo assim o portao aceita-a como verificacao. ***")
except FactoNaoValidado as e:
    print(str(e).rstrip())
    print("  o portao bloqueou — o buraco A nao existe.")

print()
print("=" * 96)
print("5 · O PROXIMO ERRO DA MESMA FAMILIA, escrito antes de acontecer")
print("=" * 96)
print("""
  A condicao 5 nasceu de: «dois instrumentos concordarem nao valida a
  DEFINICAO da unidade». O caso dela foi a unidade que mudou NO TEMPO.

  A mesma frase, com a outra metade: dois instrumentos concordarem nao valida
  o RECORTE da unidade NO ESPACO, nem a POPULACAO com que ela e comparada.

  O proximo erro, na forma em que vai aparecer:

    uma unidade recortada onde o sinal e pior — por sinal, por testemunho, ou
    por um filtro derivado de um instrumento datado DEPOIS do acontecimento —
    comparada com unidades administrativas inteiras que ninguem recortou, e
    declarada «a pior de N» com dois instrumentos a concordar.

  Os dois instrumentos concordam, porque ambos veem o mesmo recorte. As cinco
  condicoes passam todas. E o numero e um MAXIMO DE MUITOS de um lado e uma
  MEDIA de cada um do outro — que e a comparacao que a REG-01 refeita faz hoje.

  A condicao que falta, e o teste que ela teria de exigir:

    6 · SIMETRIA DE RECORTE. Quando o facto ordena unidades, ou todas as
        unidades sofreram o mesmo recorte, ou o recorte foi aplicado tambem as
        comparadoras e o facto sobrevive. Nao se declara: mede-se, como
        `ancoras()` e `reproduz()` medem. Assinatura possivel:

            f.simetria_de_recorte(alvo=deg_foco,
                                  comparadoras=[deg_k_piores_de_cada_bloco],
                                  como="as k piores celulas de cada bloco",
                                  fora_de_amostra=True)

        e bloqueia se a unidade-alvo nao bater as comparadoras recortadas da
        mesma maneira. Neste caso passaria (c3_06: fora de amostra os focos
        batem 9 de 10 e 22 de 24) — mas passaria MEDIDO, nao declarado.
""")
