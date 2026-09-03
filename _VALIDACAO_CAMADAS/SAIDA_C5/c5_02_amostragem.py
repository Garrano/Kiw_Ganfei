# -*- coding: utf-8 -*-
"""C5 · Desenho de amostragem — a coluna que falta, e o transecto.

A RESTRICAO QUE DETERMINA TUDO
------------------------------
A matriz de diagnostico deste caso tem UMA COLUNA. Das 20 linhas organismo x
matriz, 2 foram ensaiadas numa unidade com posicao, 15 tem algum lugar
declarado, e 13 tem como unica fonte UTILIZAVEL de Ganfei uma so amostra
composta — o informe 331/2025 («Kiwi 1000»), colhida em 2025-06-06, num sitio,
num dia, sem replicado (D6).

  ATENCAO AO NUMERO, porque atravessa cinco documentos da cadeia com o valor
  errado: o campo `linhas_com_lugar_mas_sem_par_de_comparacao` do
  `c4_01_numeros.json` diz **10**. O 13 soma-lhe as tres linhas cuja segunda
  fonte e o material espanhol de Ribadumia (240/2023), que esta REJEITADO — e
  essas tres sao precisamente as que carregam os resultados NEGATIVOS.
  Le-se: **10 tem o granel como unica fonte; 13 tem-no como unica fonte
  utilizavel de Ganfei.** Este ficheiro le os dois numeros do JSON.

O QUE MUDOU EM 29-08, E MUDA O DESENHO
--------------------------------------
Perguntou-se ao gestor se identificou o «maior vazio circular» no terreno ou
numa imagem nossa. **Resposta: no terreno.** Duas consequencias:

1. A colocacao do «Kiwi 1000» no lado oeste do vazio deixa de ser circular. E
   testemunho INDEPENDENTE do nosso sensoriamento remoto. Continua a ser ZONA e
   nao ponto, e a colheita continua a ser de 2025-06-06.
2. O dossie deixa de ter zero observacoes de terreno. Passa a ter UMA: um vazio
   aproximadamente circular, visivel no terreno, no interior do talhao, que NAO
   respeita fronteira de parcela nem de valvula.

**Um vazio com forma pede um TRANSECTO, nao um par de pontos.** Um contraste de
dois pontos diz «aqui sim, ali nao». Um transecto do centro para fora, com
ponto dentro, na orla e fora, diz se ha GRADIENTE — e um gradiente sobre
distancia e muito mais dificil de explicar por confundimento de bloco, de
valvula ou de gestao do que um contraste de dois pontos. Nenhum dos nove ensaios
ja feitos neste pomar permite isso.

TRES AVISOS QUE ACOMPANHAM O TRANSECTO E QUE NAO SE SUAVIZAM
-----------------------------------------------------------
· **O transecto NAO e justificado pela geometria de avanco radial do satelite.**
  Os aneis concentricos e os «~37 m por ano» foram RETIRADOS pelo adversario da
  ronda H1 (o centro era definido como o centroide da propria classe, logo o
  rho = 0,77 era garantido num campo com I de Moran 0,9). O transecto e
  justificado pela OBSERVACAO DE CAMPO, que e outro instrumento e chegou depois.
  Se as duas apontarem no mesmo sentido, isso e convergencia entre um
  instrumento retirado e um instrumento novo — e so o novo conta.
· **A forma e testemunho, nao medicao nossa.** «Aproximadamente circular» e a
  descricao do gestor. NAO se lhe atribui area, raio nem centro. Em particular
  NAO se lhe atribui o centro E530476 N4655046 nem as 3,98 ha: isso e o nucleo
  n.o 22 da corrida B, delimitado por anomalia de NDVI e NDMI, com
  first = 2026-07-27. **Sao dois objectos com o mesmo nome e a ligacao entre
  eles esta POR ESTABELECER.**
· **Forma circular e compativel com varios agentes de solo e nao identifica
  nenhum.** Armillaria, Rosellinia e Phytophthora produzem todos manchas
  grosseiramente circulares por propagacao raiz-a-raiz. A forma NAO exclui nada
  e NAO promove nada — e o erro que o livro-razao existe para nao cometer.

E O TESTE QUE SAI DE GRACA
--------------------------
Se o vazio de terreno e o nucleo de satelite forem o mesmo objecto, o transecto
di-lo: basta registar GPS no centro e na orla que o gestor apontar, e comparar
DEPOIS com o poligono do nucleo. **E uma verificacao de identidade de objecto
por instrumento independente — testemunho de campo contra anomalia optica — e
custa duas leituras de GPS.** E exactamente a pergunta que nunca se fez a
«sentinel_b1\\»: o que e este sitio?

PORQUE E QUE O DESENHO NAO VEM DA ARVORE QUE JA EXISTE
------------------------------------------------------
A F5/F6 do `_pacote_cowork\\` desenham a amostragem contra uma arvore construida
sobre factos entretanto retirados — avanco radial, «Zona 0 = o foco mais
antigo» (invertido pela G34), «valvula 27» (nao existe nos dois livros, R7 da
C3), «M. hapla em 5 de 5 blocos» (sao 4 unidades COM POSICAO). Desenhar a
amostragem a partir dessa arvore e depois concluir que a causa e um dos ramos
que la estavam e a forma exacta do erro da mascara derivada do sinal. Este
desenho vem do livro-razao re-etiquetado (`c5_reetiquetagem.csv`) e da
observacao de campo.

NENHUMA COORDENADA DE PLANTA E INVENTADA AQUI. Cada unidade e um ALVO com raio;
a coordenada de cada planta e produzida no terreno e e o produto principal desta
campanha, porque nenhuma das 221 amostras deste caso tem uma.
"""
import csv
import io
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
C4 = os.path.join(os.path.dirname(AQUI), "SAIDA_C4", "c4_01_numeros.json")
VALV = r"C:\Users\Jackster2\Downloads\ganfei_s2\valvulas_por_area.json"
SAIDA = os.path.join(AQUI, "c5_amostragem.csv")

num = json.load(io.open(C4, encoding="utf-8"))
val = json.load(io.open(VALV, encoding="utf-8"))
OESTE = tuple(num["_coordenadas"]["foco_OESTE"])
ESTE = tuple(num["_coordenadas"]["foco_ESTE"])
N3 = tuple(num["_coordenadas"]["nucleo_N3"])
porv = num["por_valvula"]

CAMPO = ("A PRODUZIR NO TERRENO — obrigatoria. Nenhuma das 221 amostras deste "
         "caso tem coordenada, e e esse o defeito que as torna inutilizaveis.")
PERG = ("A REGISTAR NO TERRENO — ha pergola por cima desta planta? Custa zero e "
        "re-certifica a particao de altura de 06-07-2025 no ano que interessa.")


def d(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def pt(v):
    return (val[v]["E"], val[v]["N"])


# ---------------------------------------------------------------------------
# T1 — o transecto. Ancorado na OBSERVACAO DE CAMPO, nao numa coordenada nossa.
# ---------------------------------------------------------------------------
MARGEM_T1 = (
    "O ANCORAMENTO E DE CAMPO E NAO NOSSO. O centro do transecto e o centro que "
    "o GESTOR aponta no terreno, no dia, e a orla e onde ele diz que o vazio "
    "acaba. NAO se usa o centro E530476 N4655046 nem as 3,98 ha: esse e o nucleo "
    "n.o 22 da corrida B, delimitado por ANOMALIA de NDVI e NDMI, com "
    "first = 2026-07-27 — geometria de 2026 sobre uma colheita de 2025-06-06 — e "
    "com 30 m de dispersao de centro entre derivacoes independentes. Os «11,4 m "
    "do centro do foco» que circularam sao a distancia entre DUAS ESTIMATIVAS DO "
    "MESMO CENTROIDE PELO MESMO INSTRUMENTO: informacao locacional zero, e "
    "precisao falsa a 1,14 celulas de 10 m. NAO CITAR. "
    "O foco OESTE da cadeia (E530485 N4655053) entra aqui so como verificacao "
    "POSTERIOR, nunca como alvo. "
    "MARGEM SOBRE O PROPRIO TESTEMUNHO: o gestor esta em dialogo com este "
    "processo ha semanas. Confirmou que identificou o vazio no TERRENO; fica por "
    "perguntar se alguma vez lhe foram mostrados os nossos mapas de NDVI. E uma "
    "linha, e e a diferenca entre observacao independente e observacao ancorada.")

TRANSECTO = [
    dict(pos="T1a", papel="CENTRO do vazio de terreno",
         alvo_txt="centro apontado pelo gestor, no terreno, no dia",
         tipo="sintomatica (ou planta morta/ausente — registar qual)",
         porque=(
             "No centro espera-se sobretudo colonizador secundario, e e por isso "
             "que ele e informativo: se o agente primario estiver na ORLA e nao "
             "no CENTRO, isso e a assinatura de propagacao radial. As colheitas "
             "anteriores deste caso amostraram o centro e so o centro — a planta "
             "arrancada de 2026-08-04 veio do centro de um foco — e por isso "
             "nunca puderam ver a diferenca.")),
    dict(pos="T1b", papel="ORLA — a frente, onde o gestor diz que o vazio acaba",
         alvo_txt="orla apontada pelo gestor, no terreno, no dia",
         tipo="sintomatica, planta ainda viva e com sintoma",
         porque=(
             "E o ponto que decide. Uma planta viva com sintoma na frente e onde "
             "um agente primario ainda esta activo; e o unico compartimento deste "
             "desenho onde um patogenio radicular em propagacao TEM de aparecer "
             "se for isso que se passa.")),
    dict(pos="T1c", papel="FORA — copado aparentemente sao, >= 20 m alem da orla",
         alvo_txt="mesma direccao radial, >= 20 m para la da orla, na mesma fila "
                  "sempre que a fila o permita",
         tipo="assintomatica",
         porque=(
             "Controlo de PROXIMIDADE: mesma fila, mesma valvula, mesma gestao, "
             "mesmo solo, a metros de distancia. Se o agente aparecer aqui "
             "tambem, nao explica o vazio. Distingue-se de U3/U4, que sao "
             "controlos de TERRENO a centenas de metros.")),
]

# ---------------------------------------------------------------------------
UNIDADES = [
    dict(
        id="U2", papel="FOCO — oriental",
        alvo=ESTE, raio_m=90,
        ancora="foco ESTE, E530977 N4655117 (G34); disco de 90 m RESTRITO as "
               "celulas com altura mediana >= 0,5 m em 06-07-2025",
        valvulas="v13 (ponto de valvula a 80,8 m) e v14 (93,2 m), bloco B3",
        plantas=3, tipo="sintomaticas",
        porque=(
            "Nao existe biologia do lado oriental. A unica amostra e um composto "
            "de bloco sobre 9,92 ha dos quais 16,3 % eram chao lavrado em 2021, e "
            "a contagem 28/37 NAO pode ser atribuida a plantas do foco ESTE (B7). "
            "Sem esta unidade nao se pode dizer se os dois focos sao um problema "
            "ou dois — e D1 e S20 ja dizem que os dois terrenos tem historias "
            "OPOSTAS."),
        margem=(
            "NAO HA VAZIO DE TERRENO DECLARADO DESTE LADO, e essa assimetria e "
            "ela propria informacao. PERGUNTA DE UMA LINHA, A FAZER ANTES DA "
            "CAMPANHA: «ve deste lado um vazio comparavel ao do lado poente?» Se "
            "a resposta for nao, os dois focos sao fenomenos diferentes e "
            "sabe-se por uma pergunta em vez de por uma campanha. "
            "METADE DO DISCO NAO E COPADO: 0,47 m de altura mediana, 50,2 % das "
            "celulas abaixo de 0,5 m em 06-07-2025; o limiar operativo de 0,5 m "
            "cai a 0,03 m da mediana da propria unidade — corta-a pelo centro — e "
            "o IFAP declara KIWI em 65 % do terreno abaixo dele. A particao vale "
            "A 06-07-2025 e e HIPOTESE para 2026. "
            "E 52,4 % do defice de 2026 no disco de 120 m ja estava em defice "
            "continuo desde 2024 ou antes: esta unidade esta CONFUNDIDA com "
            "operacoes de gestao ate o registo de operacoes chegar (GES-04)."),
        positivo=(
            "MESMO agente que T1: um problema com duas expressoes, e a cronologia "
            "pode manter-se numa faixa unica. AGENTE DIFERENTE: dois problemas "
            "distintos, o dossie separa-se em dois, e e o resultado que mais muda "
            "o relatorio."),
        negativo=(
            "com T1 positivo, o lado oriental deixa de ter suporte biotico e a "
            "hipotese de operacao de gestao (GES-04) sobe sozinha ao topo — sem "
            "que se tenha gasto um euro a testa-la."),
    ),
    dict(
        id="U3", papel="PAR SAO — ocidental (o controlo que nunca existiu)",
        alvo=pt("6"), raio_m=40,
        ancora="ponto da valvula 6, bloco B2 (ficheiro operativo "
               "valvulas_por_area.json, G35)",
        valvulas="v6",
        plantas=3, tipo="assintomaticas",
        porque=(
            "E a unica unidade do bloco B2 com os TRES indicadores a zero: 0,0 % "
            "de defice em 2026, 0,0 % de declinio novo M2 e 0,0 % de chao lavrado "
            "em 2021. Mesmo bloco, mesma fila de valvulas, MESMA ORIGEM DE AGUA e "
            "mesmo material vegetal que T1 — o corpo principal e todo pe franco "
            "de Erica (G19/G36). Emparelha com T1 em tudo excepto no defice, que "
            "e a definicao de um controlo. NENHUMA COLHEITA DESTE CASO TEVE "
            "ALGUMA VEZ UM ASSINTOMATICO."),
        margem=(
            "DUAS CONDICOES, E NAO SAO OPCIONAIS. (1) «0 % em defice» quer dizer "
            "«nunca abaixo da referencia menos 0,05», e a referencia esta ELA "
            "PROPRIA a cair (INS-04): isto e «demonstravelmente nao pior do que a "
            "referencia», que e mais fraco do que «sao». (2) A data de plantacao "
            "TEM de ser confirmada antes (GES-08): pelo menos 5,37 ha do poligono "
            "nao tinham fiada em 2010 nem em 2012 e tinham-na em 2021, a "
            "localizacao exacta dessas hectares NAO esta estabelecida, e o "
            "enchimento de uma pergola nova vale +0,06 a +0,11 NDVI/ano — varias "
            "vezes o efeito procurado. UMA UNIDADE JOVEM PARECE SA E NAO E "
            "CONTROLO. Escolher o controlo pela aparencia do que se vai medir e a "
            "mascara derivada do sinal outra vez."),
        positivo=(
            "o agente esta tambem no terreno sem defice: DEIXA DE EXPLICAR O "
            "PADRAO e sai da lista de causas. E o desfecho que ja aconteceu ao "
            "M. hapla, e e o desfecho MAIS PROVAVEL para os Fusaria, que sao "
            "comuns em solo e madeira de pomar. E precisamente por isso que tem "
            "de correr: e o unico ensaio deste desenho que pode BAIXAR o numero "
            "de candidatos."),
        negativo=(
            "com T1 positivo, o organismo passa a ser o PRIMEIRO deste caso com "
            "contraste de lugar A DUAS ESCALAS — orla contra fora-proximo (T1c) e "
            "foco contra terreno sao (U3). Nao e causa; passa a ser a linha que "
            "merece uma segunda epoca, e a unica que a merece."),
    ),
    dict(
        id="U4", papel="PAR SAO — oriental",
        alvo=pt("17"), raio_m=40,
        ancora="ponto da valvula 17, bloco B4 (ficheiro operativo, G35)",
        valvulas="v17",
        plantas=3, tipo="assintomaticas",
        porque=(
            "Os dois lados tem substratos OPOSTOS em todas as variaveis que os "
            "separam (S20): cota, posicao hidraulica, distancia a drenagem, "
            "historia de lavra, rugosidade. Um so par sao, do lado ocidental, "
            "confundiria BLOCO com TERRENO. A v17 tem os mesmos tres indicadores "
            "a zero e e a escolha dentro do B4 — a v16, no mesmo bloco, tem "
            "13,0 % de defice."),
        margem=(
            "As mesmas duas condicoes de U3, e uma terceira: o B4 e um bloco "
            "diferente do B3, logo este par controla o TERRENO oriental e nao a "
            "GESTAO do B3. Fica a 474 m do foco ESTE — e um par de regiao, nao de "
            "vizinhanca."),
        positivo="idem U3, para o lado oriental.",
        negativo="idem U3, para o lado oriental.",
    ),
]

MATRIZES = ["raiz fina", "colo/tronco", "solo 0-30 cm", "solo 40-80 cm"]
PAINEIS = [
    ("as 20 linhas organismo x matriz do informe 331/2025",
     "todas as matrizes",
     "e a COLUNA QUE FALTA. Mesmo laboratorio (Areeiro), mesmo metodo, mesma "
     "data. Um laboratorio diferente transforma um contraste de LUGAR num "
     "contraste de LABORATORIO."),
    ("bacteriologia: Pseudomonas syringae pv. actinidiae e bacterias de vaso",
     "raiz fina, colo/tronco",
     "BIO-24/25. NAO EXISTE UMA UNICA LINHA BACTERIANA EM TODA A MATRIZ deste "
     "caso: os 15 taxa sao fungos, oomicetas e um nematode. A PSA e o patogeno de "
     "referencia do kiwi na Europa e nunca foi procurada, em nenhuma matriz, em "
     "nenhuma data. Custo baixo, consequencia alta, e e a UNICA linha do livro "
     "comparavel com um valor de fora do caso sem campanha nenhuma."),
    ("isolamento selectivo de oomicetas em raiz e colo",
     "raiz fina, colo/tronco",
     "BIO-23. O unico negativo de oomicetas com lugar e em SOLO, e a MESMA "
     "amostra da POSITIVO a um oomiceta na RAIZ (Globisporangium intermedium). "
     "Cobre o Phytophthora sem o nomear — nomea-lo e como o P. sojae entrou."),
    ("nematologia de espectro largo",
     "solo 0-30 cm, solo 40-80 cm",
     "BIO-27. Os cinco informes 339-343/2026 contam J2+ovos de M. hapla e mais "
     "nada. E a unica via pela qual «M. hapla esta em todo o lado» se pode re-ler."),
    ("analise foliar, Ca e macronutrientes",
     "folha",
     "ABI-11/ABI-12. A perna foliar de ABI-11 e a UNICA vez em toda a cadeia em "
     "que um numero deste caso e comparado com um padrao EXTERNO (Ca 2,2 % contra "
     "referencia analitica 3-4,7 %) em vez de com outra parte da mesma parcela. E "
     "NAO EXISTE analise foliar para o B3."),
]

FOSSAS = [dict(id="P1", em="T1b (orla)", firme=True),
          dict(id="P2", em="U3", firme=True),
          dict(id="P3", em="U2", firme=False),
          dict(id="P4", em="U4", firme=False)]

# ---------------------------------------------------------------------------
linhas = []
for i, t in enumerate(TRANSECTO, 1):
    for m in MATRIZES:
        linhas.append(dict(
            unidade="T1", papel="TRANSECTO — foco ocidental, vazio de terreno",
            posicao=t["pos"], papel_do_ponto=t["papel"],
            alvo_E="ancorado no terreno", alvo_N="ancorado no terreno",
            raio_m="-", ancora=t["alvo_txt"],
            valvulas="v8 / v9 / v7 — a determinar pelo GPS de campo, nao a priori",
            planta="%s" % t["pos"], tipo=t["tipo"], matriz=m,
            d_foco_OESTE_m="a calcular DEPOIS do GPS de campo",
            d_foco_ESTE_m="a calcular DEPOIS do GPS de campo",
            coordenada_da_planta=CAMPO, pergola_por_cima=PERG,
            porque=t["porque"], margem=MARGEM_T1,
            se_positivo=(
                "GRADIENTE centro>orla>fora ou orla>centro: assinatura de agente "
                "de solo em propagacao. NAO identifica qual — forma circular e "
                "compativel com Armillaria, Rosellinia e Phytophthora e nao "
                "distingue entre eles. SEM GRADIENTE, positivo em todos: nao ha "
                "propagacao a medir, e o vazio e outra coisa."),
            se_negativo=(
                "as linhas do 331/2025 nao reproduzem no proprio vazio que o "
                "gestor ve, com o mesmo laboratorio. A unica coluna da matriz nao "
                "e estavel, D7 passa a achado isolado, e para-se de tratar as "
                "nove presencas como material de trabalho. E um resultado FORTE."),
        ))
for u in UNIDADES:
    do, de = d(u["alvo"], OESTE), d(u["alvo"], ESTE)
    for pl in range(1, u["plantas"] + 1):
        for m in MATRIZES:
            linhas.append(dict(
                unidade=u["id"], papel=u["papel"], posicao="%s-P%d" % (u["id"], pl),
                papel_do_ponto=u["tipo"],
                alvo_E="%.1f" % u["alvo"][0], alvo_N="%.1f" % u["alvo"][1],
                raio_m=u["raio_m"], ancora=u["ancora"], valvulas=u["valvulas"],
                planta="%s-P%d" % (u["id"], pl), tipo=u["tipo"], matriz=m,
                d_foco_OESTE_m="%.1f" % do, d_foco_ESTE_m="%.1f" % de,
                coordenada_da_planta=CAMPO, pergola_por_cima=PERG,
                porque=u["porque"], margem=u["margem"],
                se_positivo=u["positivo"], se_negativo=u["negativo"]))

with io.open(SAIDA, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(linhas)

# ------------------------------------------------------------------- relatorio
print("=" * 76)
print("C5 · DESENHO DE AMOSTRAGEM — a coluna que falta, e o transecto")
print("=" * 76)
mr = num["matriz_resumo"]
print("\nA restricao, lida do c4_01_numeros.json:")
print("  linhas organismo x matriz ........................ %d" % mr["linhas_organismo_x_matriz"])
print("  ensaiadas numa unidade COM POSICAO ............... %d" % mr["ensaiadas_em_unidade_colocada"])
print("  com algum lugar declarado ........................ %d" % mr["ensaiadas_com_algum_lugar_declarado"])
print("  com o granel 331/2025 como UNICA fonte ........... %d   <- campo do JSON"
      % mr["linhas_com_lugar_mas_sem_par_de_comparacao"])
print("  ... mais as 3 cuja 2.a fonte e Ribadumia (rejeitada) = %d  <- o «13»"
      % (mr["linhas_com_lugar_mas_sem_par_de_comparacao"] + 3))
print("  linhas sem QUALQUER fonte de Ganfei .............. %d"
      % len(mr["linhas_sem_qualquer_fonte_de_Ganfei"]))
print("  linhas com algum NEGATIVO ........................ %d, das quais %d vem"
      % (mr["linhas_com_algum_NEGATIVO"],
         mr["linhas_com_NEGATIVO_a_partir_de_amostra_com_lugar"]))
print("     de amostra com lugar — e as 4 sao do MESMO granel.")
print("  taxa distintos ................................... %d (fungos, oomicetas"
      % mr["taxa_distintos"])
print("     e um nematode; ZERO bacterias, ZERO virus)")

print("\nT1 · TRANSECTO — ancorado na OBSERVACAO DE CAMPO, nao numa coordenada nossa")
for t in TRANSECTO:
    print("  %-5s %s" % (t["pos"], t["papel"]))
print("  centro e orla sao apontados pelo gestor NO TERRENO, no dia; GPS em cada")
print("  ponto. Segunda radial a ~90 graus: opcional, e o upgrade mais barato que")
print("  este desenho tem — duplica a forca do gradiente sem deslocar equipa.")
print("\n  TESTE DE IDENTIDADE DE OBJECTO, que sai de graca:")
print("  registar GPS no centro e na orla e comparar DEPOIS com o poligono do")
print("  nucleo n.o 22 da corrida B. Testemunho de campo contra anomalia optica —")
print("  dois instrumentos independentes sobre a pergunta «e o mesmo sitio?».")
print("  Hoje sao dois objectos com o mesmo nome e a ligacao esta POR ESTABELECER.")

print("\nUNIDADES COM ALVO NOSSO — por coordenada, sempre")
print("%-4s %-40s %11s %12s %8s %8s" %
      ("id", "papel", "E", "N", "d-OESTE", "d-ESTE"))
for u in UNIDADES:
    print("%-4s %-40s %11.1f %12.1f %7.1fm %7.1fm" %
          (u["id"], u["papel"][:40], u["alvo"][0], u["alvo"][1],
           d(u["alvo"], OESTE), d(u["alvo"], ESTE)))
print("\n  (o nucleo N3, E531068 N4655145, NAO e unidade de amostragem: esta a")
print("   %.1f m do foco ESTE, FORA do disco de 90 m, e a pergunta que o separa —"
      % d(N3, ESTE))
print("   replantacao contra chao limpo mantido — fecha-se com uma VISITA ou um")
print("   segundo voo, nao com um painel de laboratorio.)")

print("\n  indicadores das duas unidades sas escolhidas, lidos do c4_01_numeros.json:")
print("  %-5s %7s %10s %10s %12s" % ("valv", "ha", "defice26", "novo M2", "chao 2021"))
for v in ("6", "17", "16"):
    b = porv["v" + v]
    marca = "  <- escolhida" if v in ("6", "17") else "  <- rejeitada (defice)"
    print("  v%-4s %7.2f %9.1f%% %9.1f%% %11.1f%%%s" %
          (v, b["ha"], b["pct_defice_2026"], b["pct_novo_M2"],
           b["pct_nu2021_chao_lavrado"], marca))

print("\nPAINEIS — os mesmos em TODAS as unidades e em TODOS os pontos")
for nome, mats, _ in PAINEIS:
    print("  · %-62s [%s]" % (nome, mats))

npl = len(TRANSECTO) + sum(u["plantas"] for u in UNIDADES)
print("\nEFECTIVOS")
print("  unidades ................. %d  (1 transecto de 3 pontos + 1 foco + 2 pares saos)"
      % (1 + len(UNIDADES)))
print("  plantas .................. %d" % npl)
print("  amostras de planta ....... %d  (%d plantas x %d matrizes)"
      % (len(linhas), npl, len(MATRIZES)))
assert len(linhas) == npl * len(MATRIZES)
print("  fossas de perfil ......... %d firmes (%s) + %d condicionais (%s)"
      % (sum(1 for f in FOSSAS if f["firme"]),
         ", ".join(f["em"] for f in FOSSAS if f["firme"]),
         sum(1 for f in FOSSAS if not f["firme"]),
         ", ".join(f["em"] for f in FOSSAS if not f["firme"])))
print("     (ABI-10 e ABI-13: NAO EXISTE UMA UNICA DESCRICAO DE PERFIL DE SOLO em")
print("      todo o caso. As condicionais so sao interpretaveis DEPOIS do registo")
print("      de operacoes, porque o lado oriental esta confundido com gestao.)")
print("  agua ..................... 1 amostra da origem unica (ABI-06)")
print("  uma data, um laboratorio.")

print("""
PORQUE TRES PONTOS POR UNIDADE E NAO SEIS
  Nao e uma escolha de potencia — e uma escolha sobre o que muda. Fora do foco,
  o n actual e ZERO: nenhuma das 13 linhas foi alguma vez ensaiada em mais
  nenhum ponto, nem doente nem sao. Passar de 0 para 3 muda o que se pode
  dizer; passar de 3 para 6 nao muda, nesta fase, porque a pergunta ainda e
  «existe contraste, e existe gradiente?» e nao «qual e a sua dimensao?». Se
  houver contraste, e a segunda epoca que precisa de efectivos.

O QUE ESTE DESENHO NAO PODE FAZER, E TEM DE IR ESCRITO NO RELATORIO
  · Nao estabelece causalidade. Um contraste numa data nao satisfaz os
    postulados de Koch nem nada que se lhes pareca.
  · Nao identifica o agente pela forma. Circular e compativel com varios
    agentes de solo e nao distingue nenhum.
  · Nao distingue LOCAL de REGIONAL. As quatro unidades estao dentro da mesma
    exploracao, com a mesma origem de agua e a mesma gestao. Se a causa for
    regional, as quatro dao o mesmo resultado e isso NAO sera informativo.
    Essa pergunta e a REG-01 e resolve-se fora desta campanha.
  · Nao interpreta 2026 sem o registo de operacoes. Se o B2 ou o B3 tiveram
    arranque, replantacao ou poda severa em 2024-2026, a amostragem pode cair
    sobre replantacao e nao sobre declinio — e nada no material diz que parte.

CONDICOES DE ARRANQUE — e desta vez verifica-se que foram cumpridas antes de as
dar por cumpridas, porque o T3 do adversario da C2 foi posto como condicao,
nunca correu, ninguem registou que nao, e tres camadas construiram por cima.
  1. GES-08 — data de plantacao por talhao. Sem ela nao ha par sao valido.
  2. GES-03/GES-04/ABI-05 — registo de operacoes do B2 e do B3, 2024-2026.
     Sem ele nenhum resultado de 2026 e interpretavel.
  3. T3 — prominencia de pergola sobre a ortofoto de 2025.
  4. As duas perguntas de campo, que custam uma chamada: «ve do lado nascente um
     vazio comparavel?» e «onde estava a planta arrancada de 2026-08-04, em
     relacao ao vazio?».
  Nenhuma das quatro e uma analise.
""")
print("gravado: %s  (%d linhas)" % (SAIDA, len(linhas)))
