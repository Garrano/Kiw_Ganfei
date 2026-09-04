# -*- coding: utf-8 -*-
"""O registo executável dos factos — a LISTA_FINAL que corre em vez de se ler.

PORQUE EXISTE
-------------
A `LISTA_FINAL_2026-08-31.md` é prosa. Prosa não é verificada por ninguém quando
um facto novo chega, e foi assim que o A3 passou: as condições estavam escritas,
o `guarda.py` existia, e mesmo assim publiquei um facto cuja unidade tinha mudado
de natureza a meio da linha de base.

Este ficheiro declara **cada facto sobrevivente** como um `guarda.Facto`, com o
seu instrumento, os seus confirmadores e — quando compara unidades ao longo do
tempo — a prova de que a unidade não mudou. Correr o ficheiro **é** a
certificação. Se algum facto deixar de cumprir, o processo falha com código de
saída diferente de zero e diz qual.

A LACUNA 2, resolvida aqui
--------------------------
A condição 5 (`identidade_no_tempo`) foi acrescentada ao portão a 01-09, à
medida do erro do A3, e **nunca foi aplicada aos factos que já lá estavam**.
A1, A2 e todo o bloco B são comparações temporais e nenhum a tinha declarado.
Este registo aplica-a a todos, retroactivamente.

DE ONDE VEM A PROVA DE IDENTIDADE
----------------------------------
De `_VALIDADE_GESTAO\triagem_referencia_densa.json` — o rastreio de
descontinuidade de todas as unidades de Ganfei numa série densa de Verão,
2017-2026. **O acoplamento é de propósito:** se a referência falhar o rastreio,
todos os factos temporais bloqueiam de uma vez, porque todos a usam como
denominador. Não há maneira de salvar um sem salvar o rastreio.

O QUE ESTE FICHEIRO NÃO FAZ
---------------------------
Não recalcula os números. Os valores aqui são os certificados; se um deles
mudar, o ficheiro que o produziu é que tem de ser corrido outra vez. Isto é o
**portão**, não o pipeline.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guarda import Facto, FactoNaoValidado    # noqa

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"

# ---------------------------------------------------------- a prova de identidade
DENSA = os.path.join(VG, "triagem_referencia_densa.json")
ESPARSA = os.path.join(VG, "triagem_referencia.json")
if os.path.exists(DENSA):
    T = json.load(open(DENSA, encoding="utf-8"))
    FONTE = ("rastreio de descontinuidade, série densa Sentinel-2 "
             "(%d cenas de Verão, 2017-2026)" % T.get("n_cenas", 0))
elif os.path.exists(ESPARSA):
    T = json.load(open(ESPARSA, encoding="utf-8"))
    T["referencia_ok"] = not any(a[0] == "REFERENCIA" for a in T.get("alerta", []))
    FONTE = "rastreio de descontinuidade, série esparsa (9 cenas) — PODER BAIXO"
else:
    raise SystemExit("Sem rastreio de descontinuidade em disco. Corre primeiro "
                     "triagem_referencia_densa.py — sem ele nenhum facto "
                     "temporal pode ser certificado.")

PROVA = DENSA if os.path.exists(DENSA) else ESPARSA
PROVA_REG = os.path.join(VG, "reg01_triagem.json")


def temporal(f, unidades=("REFERENCIA",), prova=None):
    """Liga o facto ao FICHEIRO de rastreio, e às unidades que ele usa.

    Reescrito a 03-09 com a condição 5 nova. Antes passava-se aqui uma frase
    e o portão acreditava; o Controlo 3 mostrou que uma linha inventada fazia
    o A3 retirado voltar a passar. Agora passa-se o caminho da prova, e é o
    portão que a lê, confirma que cobre cada unidade nomeada, e reprova se
    alguma estiver em alerta ou simplesmente não tiver sido rastreada.
    """
    return f.identidade_no_tempo(prova or PROVA, nota=list(unidades))


GANFEI = ("REFERENCIA", "foco OCIDENTAL", "foco ORIENTAL", "resto do pomar")

# ══════════════════════════════════════════════════════════════════ os factos
FACTOS = []


def reg(f, texto):
    FACTOS.append((f, texto))
    return f


# ---- A · com instrumento independente ------------------------------------
reg(temporal(
    Facto("A1 · acontecimento em 2025-26 em duas posições e não no resto",
          instrumento="contraste foco-menos-controlo, Sentinel-2",
          ficheiro="serie_oriental_pergola.py", comparacao_temporal=True)
    .confirmar_com("Landsat 8/9 (USGS/NASA, OLI, LaSRC)", True,
                   "replica direcção e datação, p exacto 0,0110 = 1/91; "
                   "controlo −0,001 (p = 0,98); magnitudes NÃO replicam"),
    GANFEI), "−0,115 (ocidental) e −0,110 (oriental), ±0,02–0,03")

reg(temporal(
    Facto("A2 · o radar vê o mesmo, no foco ocidental",
          instrumento="γ⁰ VV Sentinel-1, 441 cenas, duas órbitas",
          # A proveniencia estava errada: apontava para ganfei_s2/sar_invernos.py,
          # que e exploratorio. O numero -1,107 sai de c1_09_sar.py -> c1_09_sar.json
          # e foi reverificado por c2_09_sar_verificacao.py. Apanhado pela
          # verificacao 4 do certificar.py, na sua primeira corrida.
          ficheiro="SAIDA_C1/c1_09_sar.py", comparacao_temporal=True)
    .confirmar_com("é ele próprio o independente do óptico — física diferente",
                   True, "reverificado por SAIDA_C2/c2_09_sar_verificacao.py"),
    ("REFERENCIA", "foco OCIDENTAL")), "−1,107 e −0,775 dB, fora da banda de nove Invernos")

reg(temporal(
    Facto("A3 · entre unidades de linha de base contínua, é o pior da região",
          instrumento="Landsat 8/9, 100 cenas, 29 blocos triados",
          ficheiro="reg01_triagem_descontinuidade.py", comparacao_temporal=True)
    .confirmar_com("Sentinel-2, mesma triagem", True, "mesma ordenação")
    .confirmar_com("ortofoto DGT 2007-2025 e 03-09", True,
                   "cinco datados a 01-09; três a 03-09, com outra leitura")
    .fronteira("parcelário do IFAP (outra entidade) e discos pré-registados"),
    # A prova de identidade dos FOCOS e o rastreio denso de Ganfei, que os
    # cobre e os lista como continuos. Apontava para o rastreio REGIONAL, que
    # enumera blocos por CUL_ID e nao contem os focos — e so passava porque a
    # condicao 5 tratava ausencia como aprovacao. Apanhado pelo Controlo 3.
    ("foco OCIDENTAL", "foco ORIENTAL"), PROVA),
    "ocidental −0,0839 (1.º) e oriental −0,0869 (2.º) de 31; margem 0,0200; "
    "P(ordenação errada) = 0,07 por cenas e 0,25 por anos")

# ---- B · sem instrumento independente ------------------------------------
B = [("B1", "invariante em 43 corridas aninhadas (5 unidades × 3 raios × 5 limiares)",
      "Sentinel-2", "multiverso_degrau.py", GANFEI),
     ("B2", "o degrau bate a recta com o ponto de quebra contabilizado",
      "decomposição interna, ΔAICc", "degrau_vs_recta_pergola.py", GANFEI),
     ("B3", "são dois passos, não um: −0,050 em Ago-2025 e −0,13 a −0,23 em Jul-2026",
      "Sentinel-2", "satelites_degrau.py", GANFEI),
     ("B4", "Julho de 2026 não é estável: −0,229 a −0,130, factor 1,7",
      "Sentinel-2", "satelites_sem_2026.py", ("REFERENCIA", "foco OCIDENTAL")),
     ("B5", "a correcção de dia-do-ano é ≤ 0,0011, e é limite superior",
      "Sentinel-2", "fenologia_por_unidade.py", GANFEI),
     ("B7", "os três núcleos destacados não se distinguem no seu estrato de distância",
      "Sentinel-2", "halo_distancia.py", GANFEI)]
for cod, txt, inst, fich, un in B:
    reg(temporal(
        Facto("%s · %s" % (cod, txt), instrumento=inst, ficheiro=fich,
              comparacao_temporal=True)
        .nao_testavel("um instrumento só — controlo 1 à vista, não diluído"),
        un), txt)

# B6 é contagem geométrica num instante: não é comparação temporal
reg(Facto("B6 · a referência tinha 14 a 18 células dentro dos discos",
          instrumento="contagem geométrica", ficheiro="PRE_REGISTO_REFERENCIA.md")
    .instantanea("contagem geométrica num instante, não há intervalo a comparar")
    .nao_testavel("geometria, não medição — não há segundo instrumento a pedir"),
    "os fossos são conservadores")

# ---- C · geometria e documentos ------------------------------------------
reg(Facto("C1 · o voo LiDAR é de 06-07-2025, 14:34:53–14:51:08 UTC",
          instrumento="tempo GPS do LAS", ficheiro="l1_data_do_voo.py")
    .instantanea("uma data, lida do cabeçalho do LAS")
    .confirmar_com("global_encoding bit 0 = 1", True,
                   "Adjusted Standard GPS confirmado no cabeçalho"),
    "um só dia, 0,27 h de amplitude")

reg(Facto("C2 · a partição pérgola/chão é PÓS-TRATAMENTO",
          instrumento="data do voo contra a janela do acontecimento",
          ficheiro="CAMADA_2_ADENDA_LIDAR.md")
    .instantanea("é uma afirmação sobre a data do voo, não uma medição comparada")
    .confirmar_com("C1, calculado em disco", True),
    "toda a leitura que dela dependa herda isto")

reg(Facto("C3 · o bloco sudoeste é da mesma exploração",
          instrumento="parcelário IFAP", ficheiro="g19_parcelario.py")
    .instantanea("o parcelário é de uma campanha e é assim que é usado")
    .confirmar_com("documento de outra entidade, desenhado para pagamentos", True,
                   "19,00 ha em 16 parcelas, 12,64 ha de kiwi, todo do ENT 472062"),
    "não há controlo externo contemporâneo de kiwi — é medição, não omissão")

reg(Facto("C4 · ORI-COM tinha pérgola madura em 2010 (111 %) e 2012 (79 %)",
          instrumento="prominência de pérgola, ortofoto",
          ficheiro="p3_pergola_2010_2012.py")
    .instantanea("prominência medida DENTRO de cada imagem, nunca entre épocas")
    .confirmar_com("mapa certificado da C2", True,
                   "máx dif 0,00e+00 em 2 858 células"),
    "instrumento a discriminar nas duas épocas")

reg(Facto("C5 · ORI-SEM nunca teve pérgola",
          instrumento="prominência de pérgola, ortofoto",
          ficheiro="p3_pergola_2010_2012.py")
    .instantanea("prominência medida DENTRO de cada imagem")
    .nao_testavel("um instrumento só; o pico a 2,2 m longe do compasso de 5,25 m "
                  "é consistente mas não confirmado por outro instrumento"),
    "pico a 2,25 m (2012) e 2,12 m (2021)")

reg(temporal(
    Facto("C6 · a pérgola apareceu no pomar entre 2007 e 2010",
          instrumento="prominência de pérgola, seis épocas de ortofoto",
          ficheiro="p4_quando_foi_arrancada.py", comparacao_temporal=True)
    .confirmar_com("coorte de plantação certificada pela C0", True,
                   "documental, independente da imagem"),
    ("REFERENCIA",)), "prominência negativa em todas as unidades até 2007")

reg(Facto("C7 · a atribuição de válvulas não sustenta nenhuma quantidade",
          instrumento="quatro reconstruções do esquema de rega",
          ficheiro="lobulo_oeste_degrau.py")
    .instantanea("resultado negativo sobre o instrumento, sem eixo temporal")
    .nao_testavel("é um resultado negativo sobre o próprio instrumento: "
                  "a área por válvula varia até 50×"),
    "nenhuma peça pode escrever uma área por válvula")

# ---- D · biologia --------------------------------------------------------
D = [("D1", "a matriz de diagnóstico tem uma coluna: 13 de 20 linhas numa só amostra"),
     ("D2", "o único organismo com posição é o M. hapla, e anticorrelaciona com o défice"),
     ("D3", "a única amostra oriental é um composto sobre 9,92 ha, 28,1 % sem pérgola"),
     ("D4", "o esforço de amostragem é inverso à heterogeneidade do substrato"),
     ("D5", "nenhuma amostra com posição é anterior ao acontecimento")]
for cod, txt in D:
    reg(Facto("%s · %s" % (cod, txt), instrumento="relatório laboratorial",
              ficheiro="CAMADA_4_CERTIFICADO_R2.md")
        .instantanea("uma campanha de amostragem, sem série")
        .nao_testavel("uma campanha, um laboratório — não há segundo ensaio"), txt)

reg(Facto("D6 · a PSA nunca foi encomendada porque os sintomas não eram compatíveis",
          instrumento="testemunho directo (tipo 1)", ficheiro="LISTA_FINAL")
    .instantanea("testemunho sobre uma decisão, não uma série")
    .nao_testavel("testemunho não se corrige com réplica; corrige-se perguntando "
                  "outra vez a quem sabe. FALTA a linha no livro-razão"),
    "exclusão clínica, não lacuna")

# ---- D7-D9 · os boletins A2 de fisico-quimica do solo -----------------------
# Nove boletins x 12 parametros. A unidade e o BOLETIM, nao o registo: doze
# parametros do mesmo tubo nao sao doze observacoes.
reg(Facto("D7 · os boletins A2 não podem testar afectado contra não afectado",
          instrumento="9 boletins de físico-química do solo",
          ficheiro="a2_solo_caracterizacao.py")
    .instantanea("cada boletim é uma data única; não há série a comparar")
    .fronteira("código de bloco escrito pelo laboratório, não derivado de "
               "sinal nosso")
    .nao_testavel("nenhum boletim tem coordenada; 3 de 9 são do sector B1, fora "
                  "da AOI e em estabelecimento; e o C7 proíbe a atribuição por "
                  "válvula"),
    "0 de 9 com coordenada · 0 dentro de um foco · 3 de 9 no B1")

reg(Facto("D8 · a acidez do solo não acompanha o declínio",
          instrumento="pH(H2O) em 9 boletins — química, não óptica",
          ficheiro="a2_solo_caracterizacao.py")
    .instantanea("pH de uma colheita, sem série")
    .fronteira("código de bloco do laboratório")
    .confirmar_com("série óptica do B1 (Landsat 100 cenas + Sentinel-2)", True,
                   "os dois pH mais baixos, 5,2 e 5,3, são do B1, que SOBE "
                   "+0,092 enquanto os focos descem −0,085"),
    "hipótese pré-registada que só podia falhar, e falhou")

reg(Facto("D9 · faltam a CTC e a saturação em bases, e a profundidade não está "
          "declarada em campo nenhum",
          instrumento="inventário dos 12 parâmetros e de 5 campos de metadados",
          ficheiro="a2_solo_caracterizacao.py")
    .instantanea("é um inventário, não uma medição")
    .nao_testavel("é uma ausência documental: não há segundo instrumento a pedir"),
    "a química que existe é de acima da camada que se suspeita")

# ---- C8 · o troco de rede que nenhum teste alcancou -------------------------
reg(Facto("C8 · a hipótese da rede sobre-estendida foi fechada por um teste que "
          "não alcançava o troço oeste",
          instrumento="inventário das quatro reconstruções do esquema de rega",
          ficheiro="valvulas_1a5_o_troco_que_falta.py")
    .instantanea("é um inventário do que entrou no teste, não uma medição no tempo")
    .fronteira("o esquema de rega é documento do explorador, anterior a "
               "qualquer cálculo nosso")
    .confirmar_com("testemunho do gestor, tipo 1, 03-09-2026", True,
                   "«B1 = válvulas 1-5»")
    .confirmar_com("geometria independente", True,
                   "o bloco do G19 (C0, por extrapolação do esquema) e o B1 "
                   "(IFAP, via coordenadas do gestor) batem a 1 m no bordo norte"),
    "válvulas 1-5 ausentes das quatro reconstruções; o teste correu 12, todas "
    "no corpo principal")

# ══════════════════════════════════════════════════════════════════ o portão
if __name__ == "__main__":
    print("=" * 96)
    print("REGISTO DE FACTOS — %d factos pelo portão" % len(FACTOS))
    print("=" * 96)
    print()
    print("prova de identidade em uso — ficheiros, nao afirmacoes:")
    print("  Ganfei : %s  (%d cenas)" % (os.path.basename(PROVA),
                                         T.get("n_cenas", 0)))
    print("  regiao : %s" % os.path.basename(PROVA_REG))
    print()
    passa, bloqueia = [], []
    for f, texto in FACTOS:
        cod = f.nome.split(" ·")[0]
        try:
            f.veredicto(texto)
            marca = "temporal" if f.comparacao_temporal else "        "
            print("  OK      %-4s %s  %s" % (cod, marca, f.nome.split("· ", 1)[-1][:64]))
            passa.append(cod)
        except FactoNaoValidado as e:
            print("  BLOQUEIA %-4s %s" % (cod, f.nome.split("· ", 1)[-1][:64]))
            for l in str(e).splitlines():
                if l.strip().startswith("·"):
                    print("           %s" % l.strip())
            bloqueia.append(cod)
    print()
    print("passam: %d   ·   bloqueiam: %d" % (len(passa), len(bloqueia)))
    if bloqueia:
        print("BLOQUEADOS: %s" % ", ".join(bloqueia))
        raise SystemExit(1)
    print("Todos os factos da LISTA_FINAL cumprem as cinco condições do portão.")
