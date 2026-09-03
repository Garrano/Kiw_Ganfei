# -*- coding: utf-8 -*-
"""C5 · Re-derivacao do estatuto das 59 linhas do livro-razao da C4.

PORQUE EXISTE
-------------
O `c4_razao_exclusoes.csv` marca 41 linhas como NAO TESTADA, e a legenda que a
C4 imprime para esse estatuto e «ninguem procurou». O adversario da C4 (3.2)
verificou-as e concluiu que **pelo menos dezasseis estao mal rotuladas e que
para nove delas o inverso e verdade: foram procuradas e ENCONTRADAS**. Uma C5
que leia a etiqueta vai orcamentar PRIMEIROS ensaios onde o que falta e um
SEGUNDO ponto de comparacao.

O adversario da C4 exigiu, como condicao de arranque desta camada, que a coluna
`estatuto` fosse partida em `estatuto` + `procurado_onde`, e que o CSV levasse
uma coluna `n` e uma coluna `poder`. E o que este ficheiro faz.

REGRA DE DERIVACAO — a etiqueta nova sai dos CAMPOS DE EVIDENCIA, nao da antiga
------------------------------------------------------------------------------
Para cada linha le-se `ambito`, `prova`, `instrumento independente`,
`margem e leitura` e `o que a fecharia`, e aplica-se:

  houve ensaio em Ganfei?  -- nao --> NUNCA PROCURADA
                           |
                           +-- so em Espanha (240/2023, rejeitado)
                           |        --> SO FORA DE GANFEI
                           +-- sim, POSITIVO, um ponto, sem par
                           |        --> ENCONTRADA SEM PAR
                           +-- sim, POSITIVO em todas as unidades
                           |        --> ENCONTRADA SEM NIVEL NORMAL
                           +-- sim, e o desenho nao podia rejeitar
                                    --> MEDIDA SEM PODER / INCONCLUSIVA

E do lado das exclusoes e dos apoios aplica-se a assimetria que o adversario da
C4 apanhou em R10: o livro tinha EXCLUIDA-LOCAL e nao tinha SUSTENTADA-LOCAL.
Cria-se SUSTENTADA-LOCAL, e o qualificador de ambito passa a valer dos dois
lados.

AS DEZ ALTERACOES OBRIGATORIAS DO ADVERSARIO DA C4 estao aplicadas e marcadas
na coluna `origem_da_alteracao`.

NENHUM VALOR NUMERICO E TRANSCRITO A MAO. As contagens sao calculadas do CSV de
entrada e do CSV de saida. O unico conteudo escrito aqui e JUIZO — que e o
produto desta camada — e cada juizo cita o campo que o sustenta.
"""
import csv
import io
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(os.path.dirname(AQUI), "SAIDA_C4", "c4_razao_exclusoes.csv")
SAIDA = os.path.join(AQUI, "c5_reetiquetagem.csv")

# ---------------------------------------------------------------------------
# A re-derivacao. Chave: id.
# campos: estatuto_C5, procurado_onde, resultado, n, poder_do_desenho,
#         o_que_falta, custo, consequencia, decisao_C5, origem_da_alteracao
# custo:  NULO (ler ficheiro ou perguntar) | BAIXO (linha num ensaio ja pago)
#         MEDIO (campanha) | ALTO (obra, instrumento, segundo voo)
# ---------------------------------------------------------------------------
GRANEL = ("1 ponto - granel 331/2025, zona do testemunho (metade ocidental de "
          "um nucleo de 2,4-4,0 ha adjacente ao foco OESTE), colheita 2025-06-06")
FALTA_PAR = ("um segundo ponto ensaiado nas mesmas linhas, no mesmo laboratorio: "
             "um em terreno sem historico de defice e um no lado oriental")
MARGEM_ZONA = ("zona, nao ponto; geometria de 2026 aplicada a colheita de 2025; "
               "nenhuma distancia a um foco pode ser citada para esta amostra")

R = {}


def p(i, **kw):
    R[i] = kw


for i, org in ((1, "Fusarium cerealis (madeira)"), (2, "Fusarium equiseti (madeira)"),
               (3, "Fusarium oxysporum (madeira)"), (4, "Neofusicoccum parvum (madeira)")):
    p("BIO-%02d" % i, estatuto="ENCONTRADA SEM PAR", procurado_onde=GRANEL,
      resultado="POSITIVO", n="1", poder="nulo para causa: amostra composta, "
      "sem replicado, sem par", falta=FALTA_PAR, custo="BAIXO",
      consequencia="MEDIA", decisao="PROCURAR",
      nota="patogenio de madeira; a decisao de gestao esta na raiz. Entra por ser "
           "a mesma linha do mesmo painel e por custar zero a mais. " + MARGEM_ZONA,
      origem="reetiquetagem C5 (era NAO TESTADA; adversario da C4 3.2)")

for i, org in ((5, "Ceratobasidium sp. (raiz)"), (6, "Fusarium oxysporum (raiz)"),
               (7, "Fusarium solani (raiz)"), (8, "Neofusicoccum parvum (raiz)")):
    p("BIO-%02d" % i, estatuto="ENCONTRADA SEM PAR", procurado_onde=GRANEL,
      resultado="POSITIVO", n="1", poder="nulo para causa: amostra composta, "
      "sem replicado, sem par", falta=FALTA_PAR, custo="BAIXO",
      consequencia="ALTA", decisao="PROCURAR",
      nota="patogenio de RAIZ: e onde a decisao de gestao se joga. " + MARGEM_ZONA,
      origem="reetiquetagem C5 (era NAO TESTADA; adversario da C4 3.2)")

p("BIO-09", estatuto="ENCONTRADA SEM PAR", procurado_onde=GRANEL,
  resultado="POSITIVO", n="1", poder="nulo para causa", falta=FALTA_PAR,
  custo="BAIXO", consequencia="ALTA", decisao="PROCURAR",
  nota="e um OOMICETA e e POSITIVO na RAIZ da mesma amostra cujo solo da "
       "negativo a oomicetas (BIO-14). O negativo de solo nao cobre isto. "
       + MARGEM_ZONA,
  origem="reetiquetagem C5 (era NAO TESTADA; adversario da C4 3.2)")

p("BIO-10", estatuto="EXCLUIDA-LOCAL", procurado_onde=GRANEL + "; matriz RAIZ",
  resultado="NEGATIVO", n="1", poder="suficiente para a zona e a data, nulo para "
  "o pomar", falta="repeticao noutro ponto e noutra data", custo="BAIXO",
  consequencia="MEDIA", decisao="PROCURAR (vem no mesmo painel)",
  nota="mantida. O adversario da C4 chama as quatro EXCLUIDA-LOCAL o melhor "
       "trabalho do livro-razao. Unica correccao: a zona e uma zona de 2026.",
  origem="mantida; ambito corrigido (R2 do adversario da C4)")

p("BIO-11", estatuto="EXCLUIDA-LOCAL", procurado_onde=GRANEL + "; matriz SOLO",
  resultado="NEGATIVO", n="1", poder="idem BIO-10", falta="repeticao noutro "
  "ponto e noutra data; e a sensibilidade declarada de um composto de solo para "
  "organismo de distribuicao em manchas, que nao existe em lado nenhum",
  custo="BAIXO", consequencia="MEDIA", decisao="PROCURAR (vem no mesmo painel)",
  nota="o segundo negativo desta linha e o informe 240/2023, Ribadumia, REJEITADO.",
  origem="mantida; ambito corrigido (R2)")

p("BIO-12", estatuto="EXCLUIDA-LOCAL", procurado_onde=GRANEL + "; matriz SOLO",
  resultado="NEGATIVO", n="1", poder="idem BIO-10", falta="envio da amostra de "
  "raiz colhida em 2026-08-04 e nunca enviada", custo="NULO",
  consequencia="ALTA", decisao="PROCURAR",
  nota="NAO toca a observacao de campo de 2026-08-04, que e RAIZ, outra planta, "
       "catorze meses DEPOIS (B9). Ver BIO-13.",
  origem="mantida; ambito corrigido (R2)")

p("BIO-13", estatuto="ENCONTRADA SEM ENSAIO",
  procurado_onde="1 ponto - observacao macroscopica de campo, 2026-08-04, uma "
  "planta arrancada, local NAO especificado; amostra colhida e NAO enviada",
  resultado="POSITIVO macroscopico, por confirmar", n="1",
  poder="nenhum: identificacao macroscopica, sem confirmacao molecular",
  falta="enviar a amostra que ja esta colhida, e registar a coordenada da planta",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="e o UNICO organismo que um observador de campo nomeou neste caso. A "
       "linha RAIZ nao existe na matriz: o unico negativo que se lhe pode opor e "
       "de SOLO e de catorze meses ANTES. Custo de um envelope. "
       "CONTEXTO NOVO DE 29-08, E NAO E PROMOCAO: o gestor confirmou que "
       "identificou NO TERRENO um vazio aproximadamente circular no interior do "
       "talhao, que nao respeita fronteira de parcela nem de valvula. Forma "
       "circular e compativel com Armillaria, Rosellinia e Phytophthora e NAO "
       "DISTINGUE ENTRE ELES: nao promove esta linha nem exclui nenhuma outra. O "
       "que muda e que a amostra vale mais se se souber ONDE estava a planta "
       "arrancada em relacao ao vazio — e isso e uma pergunta de uma linha ao "
       "mesmo observador. Enviar a amostra E perguntar a posicao.",
  origem="reetiquetagem C5: nao e 'ninguem procurou' - alguem procurou, no campo, "
         "e encontrou; o que falta e o ensaio")

p("BIO-14", estatuto="EXCLUIDA-LOCAL", procurado_onde=GRANEL + "; matriz SOLO",
  resultado="NEGATIVO", n="1", poder="idem BIO-10", falta="ensaio de oomicetas "
  "em RAIZ, em Ganfei", custo="BAIXO", consequencia="ALTA",
  decisao="PROCURAR (a perna RAIZ, que e BIO-23)",
  nota="NAO cobre o compartimento raiz: e na RAIZ que a MESMA amostra da POSITIVO "
       "a Globisporangium intermedium, que e um oomiceta (BIO-09).",
  origem="mantida; ambito corrigido (R2)")

for i in (15, 18, 19, 20, 21):
    p("BIO-%d" % i, estatuto="SO FORA DE GANFEI",
      procurado_onde="0 pontos de Ganfei; 1 ponto em Ribadumia (informe 240/2023, "
      "Kiwi Atlantico), fonte REJEITADA",
      resultado="POSITIVO em Espanha; ZERO informacao sobre Ganfei em qualquer sentido",
      n="0 em Ganfei", poder="nulo: nao ha ensaio de Ganfei nesta linha",
      falta="ensaio destas linhas em Ganfei", custo="BAIXO",
      consequencia="ALTA" if i in (15, 18, 20) else "MEDIA",
      decisao="PROCURAR (vem no mesmo painel de raiz)",
      nota="ARMADILHA DE NOME ACTIVA: o talhao espanhol chama-se 'B-3/C-3' e o "
           "bloco do foco ESTE chama-se 'B3'. Ler um resultado espanhol como "
           "Ganfei exclui organismos do lado oriental sem nenhum dado de Ganfei.",
      origem="reetiquetagem C5 (era NAO TESTADA; adversario da C4 3.2)")

p("BIO-16", estatuto="INCONCLUSIVA",
  procurado_onde="4 unidades com posicao (B3, B4, V7, Erica Novo E), 2026-05-06",
  resultado="POSITIVO em 4/4; rho(defice,solo) = -0,40 e rho(defice,raiz) = -0,80 "
  "- sinal NEGATIVO, mais nematodes onde ha MENOS defice",
  n="4", poder="NULO POR DESENHO: com n=4 o p exacto de |rho|=1 e 2/4! = 0,083; "
  "o desenho nao podia produzir significancia em nenhum sentido, quaisquer que "
  "fossem os dados. E as 4 unidades misturam DUAS particoes (tres blocos de "
  "4,17-9,92 ha e uma valvula de 3,25 ha da particao de Voronoi)",
  falta="as mesmas contagens em >= 8 unidades comparaveis da MESMA particao, ou o "
  "mesmo par em terreno sem historico de defice",
  custo="MEDIO", consequencia="BAIXA", decisao="NAO PROCURAR - ver BIO-17",
  nota="ERA EXCLUIDA. O verbo 'excluido' cai: um ensaio que nao pode rejeitar "
       "nao e um ensaio. O que aguenta e o SINAL - nao ha gradiente na direccao "
       "causal, e a carga mais alta (250/200 cc) esta no B1, que NAO TEM POSICAO.",
  origem="R5 do adversario da C4 - alteracao obrigatoria 5")

p("BIO-17", estatuto="ENCONTRADA SEM NIVEL NORMAL",
  procurado_onde="5 unidades (4 com posicao + B1 sem posicao), 2026-05-06",
  resultado="POSITIVO em todas", n="5 unidades / 6 amostras",
  poder="mede presenca; nao mede se a presenca e anormal",
  falta="um NIVEL DE REFERENCIA EXTERNO - que contagem e normal em kiwi sao "
  "desta regiao. G26 diz que nao ha kiwi de controlo a 3 km, logo NAO se resolve "
  "com mais contagens locais: resolve-se com literatura ou com a prevalencia do "
  "proprio laboratorio",
  custo="NULO", consequencia="MEDIA",
  decisao="PROCURAR, mas por PERGUNTA e nao por campanha",
  nota="Um organismo presente em todas as unidades e exactamente o que produziria "
       "uma perda EM BLOCO (REG-02) em vez de um contraste. BIO-16 nao diz nada "
       "sobre isto.",
  origem="reetiquetagem C5 (era NAO TESTADA; adversario da C4 3.2)")

p("BIO-22", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos com posicao. A unica mencao esta na coluna Notes do "
  "registo 79 (Becrop 2023-08), relatorio SEM PARCELA ASSOCIADA, noutra freguesia",
  resultado="mencao documental sem lugar", n="0",
  poder="nulo", falta="ensaio dirigido, com posicao", custo="BAIXO",
  consequencia="BAIXA", decisao="NAO PROCURAR DIRIGIDO - cobre-se por BIO-23",
  nota="O CONTROLOS.md lista este organismo como o SEGUNDO dos tres erros que "
       "custaram semanas a este processo. Nomea-lo num pedido de analise e "
       "reintroduzi-lo. O isolamento selectivo de oomicetas em raiz (BIO-23) "
       "encontra-o se la estiver, sem o nomear. NAO PROMOVER.",
  origem="reetiquetagem C5: rotulo confirmado, decisao invertida")

p("BIO-23", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos de Ganfei em matriz RAIZ ou COLO. O unico negativo de "
  "oomicetas com lugar e em SOLO (BIO-14)",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="isolamento selectivo de oomicetas em raiz e colo",
  custo="BAIXO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="A MESMA amostra que da negativo a oomicetas em solo da POSITIVO a um "
       "oomiceta na raiz. Ler o negativo de solo como exclusao de Phytophthora e "
       "um dos rejeitados explicitos da C4.",
  origem="reetiquetagem C5: rotulo confirmado")

p("BIO-24", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos, 0 datas, 0 matrizes - em todo o caso",
  resultado="sem ensaio", n="0",
  poder="nulo. NAO EXISTE UMA UNICA LINHA BACTERIANA EM TODA A MATRIZ: os 15 taxa "
  "sao fungos, oomicetas e um nematode",
  falta="um ensaio bacteriologico, em qualquer ponto", custo="BAIXO",
  consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="A PSA e o patogeno de referencia do kiwi na Europa e tem prevalencia "
       "regional conhecida na literatura - e a UNICA linha deste livro que se "
       "pode comparar com um valor de fora do caso sem campanha nenhuma. "
       "Isto nao e um resultado negativo; e a ausencia do ensaio.",
  origem="reetiquetagem C5: rotulo confirmado")

p("BIO-25", estatuto="NUNCA PROCURADA", procurado_onde="0 pontos",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="um ensaio bacteriologico", custo="BAIXO", consequencia="MEDIA",
  decisao="PROCURAR (vem com BIO-24)",
  nota="idem BIO-24.", origem="reetiquetagem C5: rotulo confirmado")

p("BIO-26", estatuto="NUNCA PROCURADA", procurado_onde="0 pontos",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="serologia ou RT-PCR dirigida", custo="MEDIO", consequencia="BAIXA",
  decisao="NAO PROCURAR NESTA RONDA",
  nota="Nenhum sintoma descrito no caso aponta para virose, e nao ha linha de "
       "base. CONTINUA NAO EXCLUIDA e o relatorio tem de a levar assim.",
  origem="reetiquetagem C5: rotulo confirmado")

p("BIO-27", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos para generos que nao Meloidogyne. Os cinco informes "
  "339-343/2026 contam J2+ovos de M. hapla e mais nada",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="analise nematologica de espectro largo", custo="BAIXO",
  consequencia="MEDIA", decisao="PROCURAR (linha a mais nas mesmas amostras)",
  nota="E a unica via pela qual o achado 'M. hapla esta em todo o lado' se pode "
       "re-ler: se outro genero tiver gradiente, o quadro nematologico muda.",
  origem="reetiquetagem C5: rotulo confirmado")

# ------------------------------------------------------------------ ABIOTICO
p("ABI-01", estatuto="EXCLUIDA", procurado_onde="todo o poligono",
  resultado="0,336 / 0,406 / 0,427 graus, p = 0,20; tudo abaixo de 0,5",
  n="~3031 celulas", poder="sobra",
  falta="nada", custo="-", consequencia="-", decisao="FECHADA",
  nota="LiDAR/MDT contra serie optica: instrumento independente a serio. "
       "'Encosta' e categoricamente falso para os dois focos.",
  origem="mantida - uma das tres exclusoes genuinas do livro")

p("ABI-02", estatuto="EXCLUIDA",
  procurado_onde="as onze cenas, todo o poligono",
  resultado="rho da cota NEGATIVO nas onze cenas (-0,20 a -0,46, p < 1e-24): o "
  "defice esta no terreno ALTO, nao no baixo",
  n="~2200 celulas", poder="sobra",
  falta="nada para a versao global. A PERNA DO TWI e outra coisa: sobre pomar "
  "nivelado o ln(a/tan b) nao tem gama, logo rho ~ 0 nao e informacao. Essa "
  "sub-linha e NUNCA PROCURADA por falta de gama do instrumento, e o log que "
  "imprimia o intervalo do TWI nao foi guardado",
  custo="-", consequencia="-", decisao="FECHADA (excepto a perna do TWI)",
  nota="Hipotese fixada ANTES de correr, na direccao certa, e CONTRADITA. E o "
       "modelo do que uma exclusao deve ser. A ressalva do TWI estava no campo de "
       "texto livre e a coluna dizia EXCLUIDA - passa a estar na coluna.",
  origem="mantida; perna do TWI separada (adversario da C4 3.1 e 3.3)")

p("ABI-03", estatuto="SUSTENTADA-LOCAL",
  procurado_onde="foco OESTE E530485 N4655053 e foco ESTE E530977 N4655117; "
  "LiDAR, uma campanha de voo",
  resultado="altura sobre a drenagem 0,130 m (OESTE) / 0,150 (referencia) / "
  "0,353 (ESTE); distancia a drenagem 13,4 / 23,6 / 55,8 m",
  n="uma campanha", poder="suficiente para o contraste ESTE, insuficiente para o "
  "contraste OESTE",
  falta="uma margem vertical declarada para o MDT, que nao existe em lado nenhum; "
  "e sonda de humidade de solo instalada no foco OESTE e na referencia",
  custo="MEDIO", consequencia="MEDIA",
  decisao="NAO PROCURAR NESTA RONDA (sondas); REESCREVER a linha",
  nota="REESCRITA. O titulo antigo era 'agua concentrada no foco OESTE' e "
       "assentava num contraste OESTE-contra-referencia de 0,020 m - dois "
       "centimetros, uma ordem de grandeza abaixo da exactidao vertical tipica de "
       "um MDT LiDAR agricola, sem margem declarada. O que S6 sustenta e o OUTRO "
       "lado: o foco ESTE esta sensivelmente mais alto sobre a drenagem (0,353 "
       "contra 0,130/0,150), contraste de mais de 2x que sobrevive a qualquer "
       "margem razoavel. E facto de SUBSTRATO, nao causa.",
  origem="M8 do adversario da C4 + R10 (cria-se SUSTENTADA-LOCAL)")

p("ABI-04", estatuto="EXCLUIDA-INTERNA",
  procurado_onde="as onze cenas, agrupamento por valvula",
  resultado="o agrupamento fica dentro do nulo rodado em todas as onze cenas "
  "(p 0,175 a 0,64)",
  n="12 valvulas x 11 cenas", poder="declarado antes de correr e cumprido",
  falta="nada para o AGRUPAMENTO", custo="-", consequencia="-",
  decisao="FECHADA para agrupamento; NAO cobre ABI-05",
  nota="SEM INSTRUMENTO INDEPENDENTE - e a mesma serie optica reagrupada, e o "
       "proprio campo do CSV di-lo. O Controlo 1 manda que um facto sem "
       "instrumento independente nao passe como excluido sem marca. A marca vai "
       "agora na coluna: e uma exclusao INTERNA a serie optica. Importa porque e "
       "numa valvula que esta a maior anomalia de radar do caso (ABI-05).",
  origem="R8 do adversario da C4 - alteracao obrigatoria 8")

p("ABI-05", estatuto="NUNCA PROCURADA",
  procurado_onde="v8, 2,78 ha, bloco B2, ponto de valvula a 34,5 m do foco OESTE",
  resultado="a v8 tem a maior anomalia negativa de VV do Inverno de 2025-26 por "
  "um factor de cinco (-0,660 dB contra -0,135 da segunda) - UM instrumento",
  n="1 unidade", poder="ABI-04 testa AGRUPAMENTO e um teste de agrupamento nao "
  "ve uma unidade isolada; o teste de 'ordem na rede' e invalido por desenho (a "
  "origem esta a 240 m do foco OESTE, logo 'distancia a origem' e quase "
  "'distancia ao foco')",
  falta="o registo de operacoes e de avarias de rega do B2 em 2024-2026",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="Uma valvula e uma unidade DE GESTAO, nao uma unidade biologica. E na v8 "
       "que 93 % do defice de 2026 e declinio NOVO sobre 0 % de chao lavrado em "
       "2021 - o unico sitio do caso onde o confundente da taxa de base nao "
       "existe. Fecha-se com um documento, nao com uma analise.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-06", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos - nenhum ensaio de agua existe no caso",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="uma analise de agua da origem", custo="BAIXO", consequencia="MEDIA",
  decisao="PROCURAR",
  nota="A origem e UNICA e esta declarada na C1. Uma causa na agua produziria "
       "perda EM BLOCO (REG-02, SUSTENTADA-LOCAL) e nao um contraste entre focos "
       "- que e exactamente o padrao que o caso tem por explicar. Uma analise.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-07", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos. A linha termica DIURNA esta RETIRADA (S17): o "
  "acoplamento dT-dNDVI e -0,925 no controlo interno FORA do pomar, logo e "
  "generico da superficie",
  resultado="sem ensaio da causa", n="0",
  poder="nulo. Caiu o INSTRUMENTO, nao a causa",
  falta="LST nocturno, ou temperatura de solo medida", custo="ALTO",
  consequencia="BAIXA", decisao="NAO PROCURAR NESTA RONDA",
  nota="S5 e S6 estabelecem que os dois focos tem substratos OPOSTOS em todas as "
       "variaveis que os separam; um forcante climatico comum e mau candidato a "
       "discriminante. CONTINUA NAO EXCLUIDA. NAO RESSUSCITAR a linha termica "
       "diurna em nenhuma forma.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-08", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos. Nenhum produto de precipitacao disponivel RESOLVE os "
  "496 m que separam os dois focos",
  resultado="sem ensaio a esta escala", n="0",
  poder="nulo: a limitacao e do instrumento, nao um facto sobre a chuva",
  falta="um udometro em cada foco, ou radar meteorologico a 1 km com composicao "
  "sub-horaria", custo="ALTO", consequencia="BAIXA",
  decisao="NAO PROCURAR",
  nota="ERA EXCLUIDA. A premissa que teria de ser verdade e que a precipitacao "
       "NAO VARIA a 496 m; o que esta medido e que nenhum produto a MOSTRA a "
       "496 m. Celula convectiva de Verao varia bem abaixo do quilometro. Isto e, "
       "literalmente, 'nao temos instrumento a esta escala, logo a causa esta "
       "excluida' - a operacao que este livro-razao existe para impedir. Dois "
       "udometros so diriam alguma coisa daqui a anos e o acontecimento e de "
       "2025-2026. CONTINUA NAO EXCLUIDA.",
  origem="R6 do adversario da C4 - alteracao obrigatoria 6")

p("ABI-09", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos. ABI-08 exclui a chuva como discriminante ENTRE "
  "FOCOS; nao diz nada sobre o ANO",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="o controlo externo de REG-01", custo="-", consequencia="ALTA",
  decisao="PROCURAR POR VIA DE REG-01 (nao tem via propria)",
  nota="Sem controlo externo (G26) um ano mau da regiao e indistinguivel de um "
       "ano mau da parcela. A medicao de paisagem de 29-08 aperta isto - a mata "
       "madura nao caiu - mas nao o fecha, porque a classe 'kiwi' dessa medicao "
       "CONTEM Ganfei. Ver REG-01 e REG-03.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-10", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos. NAO EXISTE UMA UNICA DESCRICAO DE PERFIL DE SOLO EM "
  "TODO O CASO",
  resultado="S18 e S19 medem FORMA DA SUPERFICIE, nao perfil: o pomar e duas "
  "vezes mais plano que o envolvente (p = 3,2e-10) e a rugosidade a 25 m do foco "
  "ESTE excede a referencia (+0,0379 m, p = 1,3e-18) enquanto a do OESTE nao "
  "(p = 0,058)",
  n="0 perfis", poder="nulo para a causa; a propria S18 diz 'compativel, nao e "
  "prova'",
  falta="duas fossas de perfil - uma no foco, uma no par sao",
  custo="MEDIO", consequencia="ALTA", decisao="PROCURAR",
  nota="'Solo truncado logo enraizamento superficial' e a INFERENCIA; o que esta "
       "medido e a forma da superficie. E a hipotese abiotica que melhor "
       "acomodaria ao mesmo tempo REG-02 (perda em bloco) e um contraste "
       "leste-oeste, e nenhum instrumento lhe tocou. Nota de sequencia: a prova "
       "de S19 esta do lado ORIENTAL, que e o lado confundido com operacoes "
       "(GES-04) - as fossas orientais so sao interpretaveis DEPOIS do registo de "
       "operacoes.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-11", estatuto="SUSTENTADA-LOCAL",
  procurado_onde="bloco do foco OESTE (rotulo 'B2 - V7'); solo 2026-03-03 e "
  "folha 2026-06. NAO EXISTE analise foliar para o B3",
  resultado="PERNA FOLIAR (aguenta): Ca 2,2 % contra intervalo de referencia "
  "analitico 3-4,7 %, classificado 'Baixo'. PERNA DE SOLO (nao aguenta): CaO 264 "
  "e 505 mg/kg",
  n="2 boletins de solo, 1 foliar, 1 bloco, sem comparacao",
  poder="a perna de solo NAO tem poder: 264 contra 505 e um factor de 1,9 DENTRO "
  "do mesmo bloco, e a S9 - invocada uma linha antes para tornar ABI-12 "
  "inconclusiva - fixa o factor de 2 como limiar de interpretabilidade. Dentro "
  "do B1, tres sub-parcelas dao CaO 314, 439 e 4700: dispersao intra-bloco de 15x",
  falta="analise foliar no B3 e num terreno sem historico, na mesma data",
  custo="BAIXO", consequencia="ALTA", decisao="PROCURAR o par foliar",
  nota="ERA SUSTENTADA. Sustentada contra o que? Nao ha bloco de comparacao - e a "
       "mesma estrutura de prova das nove linhas BIO-01..09, e essas estavam em "
       "NAO TESTADA. O que sobrevive intacto e a FOLHA, e sobrevive por uma razao "
       "que vale mais do que a linha: e a UNICA vez em toda a cadeia em que um "
       "numero deste caso e comparado com um PADRAO EXTERNO em vez de com outra "
       "parte da mesma parcela.",
  origem="R9 do adversario da C4 - alteracao obrigatoria 9")

p("ABI-12", estatuto="INCONCLUSIVA", procurado_onde="B3, 9,92 ha, 1 boletim",
  resultado="minimo de nove boletins em cinco de sete parametros (S8) contra "
  "'um boletim nao caracteriza um bloco' (S9)",
  n="1 boletim", poder="nulo: n = 1 contra uma regra que exige factor de 2 e uma "
  "dispersao intra-bloco documentada de 15x",
  falta="tres boletins no B3 em vez de um", custo="BAIXO", consequencia="MEDIA",
  decisao="PROCURAR (simetrico de ABI-11)",
  nota="S8 e S9 sao da mesma camada e nunca foram arbitradas. Nao e excluida e "
       "nao e sustentada.",
  origem="mantida")

p("ABI-13", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos - nenhuma medicao de resistencia, porosidade ou "
  "oxigenio existe no caso",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="penetrometro e descricao de perfil, no foco e no par sao",
  custo="BAIXO", consequencia="ALTA", decisao="PROCURAR (com ABI-10)",
  nota="A leitura 'os focos perdem agua antes de verdura' que apontava para aqui "
       "esta RETIRADA POR INTEIRO (INS-05) e nao pode ser ressuscitada. A causa "
       "continua por ensaiar - e o penetrometro vem de graca com as fossas.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-14", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos - nenhum ensaio existe, e o historico de aplicacoes "
  "nunca foi pedido",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="historico de aplicacoes (documental) + analise de residuos (ensaio)",
  custo="NULO a metade documental; MEDIO a analitica", consequencia="MEDIA",
  decisao="PROCURAR so a metade documental",
  nota="O historico de aplicacoes vem no MESMO pedido que o registo de operacoes "
       "(ABI-05, GES-03, GES-04) e custa zero. A analise de residuos nao entra: "
       "nenhum sintoma descrito aponta para fitotoxicidade e nao ha linha de "
       "base. A metade analitica CONTINUA NAO EXCLUIDA.",
  origem="reetiquetagem C5: rotulo confirmado")

p("ABI-15", estatuto="NUNCA PROCURADA",
  procurado_onde="0 pontos NESTA CADEIA - mas os boletins A2 ja existem e podem "
  "trazer condutividade nao reportada",
  resultado="sem ensaio reportado", n="0 reportados", poder="nulo",
  falta="reler os onze boletins A2 e extrair a condutividade, se estiver la",
  custo="NULO", consequencia="BAIXA", decisao="PROCURAR (documental)",
  nota="E possivel que o ensaio ja tenha sido feito e nunca tenha sido lido. "
       "Custa uma leitura dos boletins que ja estao no processo.",
  origem="reetiquetagem C5: rotulo confirmado")

# -------------------------------------------------------------------- GESTAO
p("GES-01", estatuto="CONTRADITA EM PARTE",
  procurado_onde="N3, E531068 N4655145 - que esta a 95,2 m do foco ESTE, ou seja "
  "FORA do disco de 90 m. NAO e o foco ESTE",
  resultado="A FAVOR: 0,27 m de altura em 06-07-2025 e IFAP a declarar KIWI a "
  "10-06-2025. CONTRA: o piso de Inverno do N3 DESCE (0,654 em 2024/25 -> 0,497 "
  "em 2025/26) e o pico de Verao DESCE (~0,71 -> ~0,65), ficando 0,20-0,26 abaixo "
  "da referencia",
  n="1 unidade, 2 instrumentos", poder="suficiente para contrariar, insuficiente "
  "para fechar",
  falta="um segundo voo LiDAR, ou uma visita. NAO mais analise",
  custo="NULO se for visita", consequencia="MEDIA", decisao="PROCURAR por VISITA",
  nota="Uma videira jovem a pegar FECHA sobre a referencia no Verao; esta "
       "AFASTA-SE. E a 'recuperacao a 0,65' de L8 e o DENOMINADOR a cair, nao o "
       "N3 a subir - a amplitude da referencia perde metade de si em 2024 e outra "
       "vez em 2026 (0,601 / 0,590 / 0,265 / 0,538 / 0,277).",
  origem="reetiquetagem C5: nao e 'ninguem procurou' - foi procurado e o unico "
         "instrumento que a pode datar contraria-a em parte")

p("GES-02", estatuto="FAVORECIDA SEM CONFIRMACAO",
  procurado_onde="N3, E531068 N4655145", resultado="piso de Inverno 0,654 em "
  "2024/25 contra 0,358 da referencia, e queda a 0,497 em 2025/26",
  n="1 unidade", poder="insuficiente para distinguir de GES-01",
  falta="a mesma visita que fecha GES-01", custo="NULO se for visita",
  consequencia="MEDIA", decisao="PROCURAR por VISITA",
  nota="E a leitura que os numeros favorecem sobre GES-01, e NAO esta confirmada. "
       "As duas sao mutuamente exclusivas e o material nao as separa. Nao gastar "
       "um painel de laboratorio numa pergunta que um passeio responde.",
  origem="reetiquetagem C5 (era NAO TESTADA)")

p("GES-03", estatuto="CONSTRANGIDA, NAO EXCLUIDA",
  procurado_onde="v8/B2, E530485 N4655053",
  resultado="CONSTRANGIDA POR: 2,25 m de altura mediana e 90,2 % de copado acima "
  "de 1,5 m no disco OESTE em 06-07-2025 (L3); pct_nu2021 = 0,0 % na v8; 93 % do "
  "defice de 2026 da v8 e declinio NOVO",
  n="1 data de LiDAR", poder="forte para 2025, NULO para 2026",
  falta="o registo de operacoes do B2 em 2024-2026, e correr o T3 (prominencia de "
  "pergola sobre a ortofoto de 2025)",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="O LiDAR e UMA data e nao cobre 2026, que e o ano em causa. O T3 do "
       "adversario da C2 era CONDICAO DE ARRANQUE DA C3 e NAO CORREU: nao existe "
       "c2_12_prom_2025.npy e a lista ORTOS de c2_12_pergola_2012.py continua sem "
       "2025. Tres camadas construiram por cima de uma condicao nao cumprida.",
  origem="reetiquetagem C5 (era NAO TESTADA)")

p("GES-04", estatuto="NUNCA PROCURADA",
  procurado_onde="B3, v12-v15, E530977 N4655117 - NENHUM instrumento para 2026",
  resultado="sem ensaio. O que se sabe do terreno: 22,6 % de chao lavrado na v13 "
  "e 13,8 % na v14 ja em 2021, e 52,4 % do defice de 2026 do disco de 120 m do "
  "foco ESTE ja estava em defice continuo desde 2024 ou antes",
  n="0", poder="nulo", falta="o registo de operacoes do B3 em 2024-2026 - PEDIDO "
  "DUAS VEZES, POR DUAS SESSOES INDEPENDENTES, E AINDA NAO FEITO",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="Uma parte deste lado e terreno operado ha muito e NADA NO MATERIAL DIZ "
       "QUAL PARTE. Sem isto nao se sabe se a amostragem de 2026 cai sobre plantas "
       "adultas, sobre replantacao, ou sobre chao - e NENHUM RESULTADO DE 2026 E "
       "INTERPRETAVEL. E a linha que mais barato fecha e mais caro custa deixar "
       "aberta.",
  origem="reetiquetagem C5: rotulo confirmado")

p("GES-05", estatuto="INCONCLUSIVA",
  procurado_onde="B1 contra corpo principal, janela 2021-2026",
  resultado="H2a SUPORTA que o B1 e o corpo divergem e que o B1 esta do lado bom "
  "(3/3 corridas, mais confirmacao por radar em duas orbitas). H2b NAO atribui a "
  "divergencia ao porta-enxerto",
  n="3 corridas para H2a; controlo interno NAO VALIDADO para H2b",
  poder="nulo para H2b: a valvula 1 nao esta identificada (3,5 m de altura e alto "
  "demais para pergola de kiwi; 9024 m2 contra 13500 declarados) e a "
  "sobre-enxertia de 2016/2020 absorve a maior parte do efeito",
  falta="o esquema de valvulas do B1 - quais os poligonos das valvulas 1 a 5",
  custo="NULO", consequencia="MEDIA", decisao="PROCURAR (documental)",
  nota="Resolve-se PERGUNTANDO, nao calculando. NENHUM ponto do B1 tem posicao, "
       "incluindo a fronteira do porta-enxerto, que e o unico contraste de "
       "porta-enxerto do caso. E la esta a contagem de nematodes mais alta de "
       "todas (250/200 cc).",
  origem="mantida")

p("GES-06", estatuto="NAO E CAUSA CANDIDATA NO CORPO PRINCIPAL",
  procurado_onde="B1, valvulas 2-5 - e SO ali",
  resultado="confundimento declarado", n="-", poder="-",
  falta="datas de enxertia por valvula", custo="NULO", consequencia="BAIXA",
  decisao="NAO PROCURAR COMO CAUSA; recolher as datas se o esquema do B1 vier",
  nota="Entra no livro porque e o confundimento que impede GES-05 de ser "
       "decidida, nao porque possa explicar o padrao. Inflaciona a contagem de 59 "
       "candidatas sem ser candidata.",
  origem="reetiquetagem C5 (era NAO TESTADA)")

p("GES-07", estatuto="NAO E CAUSA CANDIDATA NO CORPO PRINCIPAL",
  procurado_onde="B1 apenas, no periodo do Enza Gold. O corpo principal NUNCA "
  "teve rede - testemunho de tipo 1",
  resultado="-", n="-", poder="-",
  falta="as duas datas, instalacao e remocao", custo="NULO",
  consequencia="BAIXA", decisao="NAO PROCURAR COMO CAUSA",
  nota="Nao pode explicar nada no corpo principal, por nunca la ter existido. Sem "
       "as duas datas a serie do B1 tem dois degraus de posicao desconhecida - e "
       "por isso que qualquer serie do B1 esta rejeitada.",
  origem="reetiquetagem C5 (era NAO TESTADA)")

p("GES-08", estatuto="NUNCA PROCURADA",
  procurado_onde="as 5,37 ha sem estrutura de fiada em 2010 nem em 2012 e com ela "
  "em 2021 - localizacao exacta NAO estabelecida (a frase 'concentrada a "
  "E530600-530800' e prosa, nao esta em nenhum ficheiro)",
  resultado="sem data", n="0", poder="nulo",
  falta="a data de plantacao, por talhao", custo="NULO", consequencia="ALTA",
  decisao="PROCURAR - PRIORIDADE 1, E E CONDICAO DE ARRANQUE DA AMOSTRAGEM",
  nota="O enchimento de uma pergola nova vale +0,06 a +0,11 NDVI/ano - VARIAS "
       "VEZES o efeito procurado. Uma unidade jovem PARECE sa e nao e controlo. "
       "Sem esta data nao se pode escolher um par sao, e o desenho de amostragem "
       "fica exposto ao mesmo erro que a mascara derivada do sinal: escolher o "
       "controlo pela aparencia do que se vai medir.",
  origem="reetiquetagem C5: rotulo confirmado, prioridade elevada")

# ------------------------------------------------------------------ REGIONAL
p("REG-01", estatuto="NUNCA PROCURADA COM O INSTRUMENTO CERTO",
  procurado_onde="varrimento de ~3 km em IMAGEM (G26): 13 candidatos, 11 falsos "
  "positivos, nenhum kiwi contemporaneo. O PARCELARIO nunca foi usado para "
  "procurar beneficiarios de kiwi na regiao",
  resultado="G26: com dados de satelite este caso NAO DISTINGUE 'esta parcela "
  "declina' de 'todo o kiwi deste aluviao fez isto', e isso e RESULTADO. H2-4 "
  "acrescenta um dado positivo: ENT 297313, 76,22 ha, a 8,1 km, com colapso em "
  "degrau em 2024 - UMA corrida, UMA medicao, NAO VERIFICADO INDEPENDENTEMENTE",
  n="1 alvo nao verificado", poder="nulo",
  falta="medir o ENT 297313 numa segunda corrida independente, e localizar mais "
  "dois ou tres beneficiarios de kiwi da regiao PELO PARCELARIO",
  custo="BAIXO", consequencia="ALTA - A MAIOR DO LIVRO",
  decisao="PROCURAR - PRIORIDADE 1 ABSOLUTA",
  nota="E a causa candidata de maior consequencia e a menos testada de todo o "
       "livro. Se for regional, quase todas as medidas de parcela que se possam "
       "recomendar sao inuteis. O custo BAIXOU: a medicao de paisagem de 29-08 "
       "demonstra que a consulta ao parcelario IFAP e programavel e ja corre "
       "(paisagem.py, layer culturas.2025jun10). Mas essa medicao NAO fecha esta "
       "linha - a classe 'kiwi' dela CONTEM Ganfei, e uma mistura que contem o "
       "caso nao pode controlar o caso.",
  origem="reetiquetagem C5 (era NAO TESTADA): nao e que ninguem tenha procurado, "
         "e que se procurou com o instrumento que nao resolve")

p("REG-02", estatuto="SUSTENTADA-LOCAL",
  procurado_onde="corpo principal, janela 2021-2026",
  resultado="-0,054 NDVI em cinco anos com 98,5 % dos pixeis a participar; "
  "sobrevive a bordadura, vizinhanca, densidade, escolha de referencia, "
  "plataforma, indice, sobrevivencia e gradiente de paisagem",
  n="UMA corrida", poder="uma corrida, UM instrumento optico",
  falta="a serie Landsat da referencia, que JA ESTA EM DISCO "
  "(_VALIDADE_GESTAO\\landsat.json) e nunca foi certificada",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR (certificar o Landsat)",
  nota="ERA SUSTENTADA sem qualificador, e o proprio campo de instrumento "
       "independente do CSV diz 'NAO na lista fechada'. O CLAUDE.md deste projecto "
       "escreve 'N = 1 nao e verificacao; para inferencia, tres a cinco corridas "
       "independentes'. REENQUADRA O CASO: nao sao duas manchas num pomar sao; e "
       "um bloco a descer com manchas por cima. Por isso e que precisa de "
       "instrumento independente e nao de mais uma corrida optica.",
  origem="R10 do adversario da C4 - alteracao obrigatoria 10 (cria-se "
         "SUSTENTADA-LOCAL)")

p("REG-03", estatuto="RESOLVIDA - ERA DIVERGENCIA DE DEFINICAO",
  procurado_onde="janela de 4,0 x 2,5 km (528600-532600 E, 4653400-4655900 N), "
  "35 cenas Sentinel-2 de Jun-Ago de 2024 e 2026, AS MESMAS CENAS PARA TODAS AS "
  "CLASSES, rotulos do parcelario IFAP e da altura LiDAR",
  resultado="mata alta >5 m -0,0035 (p = 0,81) | mato 0,5-5 m +0,0097 (p = 0,14) "
  "| kiwi declarado -0,0043 (p = 0,56) | vinha -0,0166 (p = 0,63) | "
  "pastagem/prado -0,0334 (p = 0,12) | milho -0,0769 (p = 0,36)",
  n="18 cenas em 2024, 17 em 2026",
  poder="NENHUMA das variacoes e significativa com estes efectivos, e as cenas "
  "de um mesmo Verao sao autocorrelacionadas, logo o n efectivo e menor que 18. "
  "O que a medicao estabelece com forca e o NEGATIVO (a mata nao caiu) e a "
  "ORDENACAO (ciclo curto cai, lenhoso nao). E o desenho PODIA ter dado positivo: "
  "deu, no milho, -0,0769",
  falta="um adversario. E de uma so sessao",
  custo="-", consequencia="ALTA", decisao="RESOLVIDA - registar, nao repetir",
  nota="AS DUAS CORRIDAS ESTAVAM CERTAS SOBRE COISAS DIFERENTES. 'Vegetacao "
       "envolvente' na corrida B incluia coberto de ciclo curto, que responde ao "
       "ano meteorologico; 'referencia estavel' na corrida C era lenhoso perene, "
       "que nao responde. O kiwi e lenhoso perene: a comparacao certa e com a "
       "mata, e a mata esta parada. NAO e um ano mau para tudo com o pomar a "
       "aguentar melhor - o enquadramento do caso AGUENTA. MARGEM QUE NAO SE "
       "SUAVIZA: a janela inclui o proprio pomar, logo a linha 'kiwi' NAO e um "
       "controlo externo e NAO fecha REG-01; e a faixa oeste da janela entra na "
       "zona de quarentena da G24 (tecido urbano de Valenca), o que e uma margem "
       "sobre a classe 'mata alta'.",
  origem="medicao do coordenador de 29-08-2026, verificada por esta camada contra "
         "paisagem_resultado.json e contra o codigo de paisagem.py (cabecalho e "
         "codigo lidos juntos: as mascaras vem de IFAP e de LiDAR, NENHUMA vem do "
         "sinal medido)")

# ---------------------------------------------------------------- INSTRUMENTO
p("INS-01", estatuto="EXCLUIDA",
  procurado_onde="fora do pomar, em quatro corridas independentes com personas e "
  "desenhos diferentes",
  resultado="quatro medicoes emparelhadas em NDVI: A +0,005 (2026) / -0,014 "
  "(2025), n.s. e de sinais opostos | C +0,0007 / +0,0045, n.s. | ceptico H2 "
  "+0,000 / +0,004 | patologista H2 +0,012 +- 0,008. Todas ~ zero",
  n="4 corridas", poder="suficiente: quatro desenhos emparelhados, duas rondas",
  falta="nada para o NIVEL. NAO cobre INS-06",
  custo="-", consequencia="-", decisao="FECHADA para o nivel",
  nota="DUAS CORRECCOES DE APRESENTACAO QUE NAO ALTERAM A CONCLUSAO. (1) A linha "
       "'-0,056' da corrida A e NDRE, outro indice, e nao pertence a esta tabela; "
       "escrever 'todas ~ zero' por cima de um -0,056 e a classe de erro que esta "
       "cadeia ja apanhou tres vezes. A corrida A TEM medicao de NDVI e e a que "
       "esta acima. (2) Duas das quatro corridas correram com o -0,048 como facto "
       "de especificacao, logo sao a jusante do erro que testam - mas a "
       "contaminacao empurra CONTRA o achado: uma corrida avisada de que deve "
       "encontrar -0,048 e que encontra zero e prova mais forte, nao mais fraca. "
       "O -0,048 vinha de um degrau de nivel medido FORA do pomar, com sensor "
       "confundido com ano.",
  origem="mantida; tabela corrigida (R3 do adversario da C4 - alteracao 3)")

p("INS-02", estatuto="EXCLUIDA-CONDICIONAL",
  procurado_onde="o salto de 2024 para 2026",
  resultado="a barra de erro da serie e ~3 ha e vem MEDIDA; o salto de 2,91 para "
  "7,86 ha e de 4,95 ha e sobrevive",
  n="9 ou 10 cenas - divergencia por resolver",
  poder="suficiente SE a cena de 2019-09-02 for legitima",
  falta="a re-certificacao da G10 pela C0 - UMA LINHA",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR (uma linha a C0)",
  nota="ERA EXCLUIDA. A margem da propria linha diz que a V11 assenta INTEIRAMENTE "
       "na cena de 2019-09-02, que a R2 G10 mandou excluir e que a C2 REPOS SEM "
       "PARAGEM DE LINHA, e que a C0 nunca re-certificou (condicao 1 do adversario "
       "da C2, POR CUMPRIR). Uma linha cuja margem declara que a sua prova esta "
       "por certificar nao pode ter estatuto EXCLUIDA na coluna que a camada "
       "seguinte le. Se a cena sair, a barra de erro de V11 tem de ser refeita e "
       "esta linha REABRE.",
  origem="R7 do adversario da C4 - alteracao obrigatoria 7")

p("INS-03", estatuto="SUSTENTADA",
  procurado_onde="as 110 celulas da referencia sistematica; efeito em 2026",
  resultado="18 de 110 (16,4 %) caem nos discos de 90 m dos dois focos; retira-las "
  "desloca a mediana +0,0133 em 2026 e menos de 0,0025 em todas as oito cenas "
  "anteriores (maximo 0,0010 ate 2024). Segunda via: a media cai 0,0548 contra "
  "0,0219 da mediana, e a distancia entre as duas passa de -0,0011 (2024) a "
  "-0,0340 (2026)",
  n="110 celulas, 9 cenas", poder="suficiente para a direccao; sem bootstrap",
  falta="um bootstrap sobre as 110 celulas, ou a repeticao noutra cena de 2026",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR (o bootstrap)",
  nota="Contaminacao GEOMETRICA: a pertenca ao disco nao depende do sinal, logo "
       "retirar as celulas nao e circular. Duas vias independentes, o mesmo "
       "resultado. O SENTIDO E CONSERVADOR: limpar a referencia torna o "
       "acontecimento MAIOR. MARGEM NAO DECLARADA - nao ha bootstrap e a cena de "
       "2026 e a S2C; parte do +0,0133 pode ser re-ordenacao da mediana e nada "
       "nesta cadeia separa as duas coisas.",
  origem="mantida")

p("INS-04", estatuto="SUSTENTADA-LOCAL",
  procurado_onde="as 110 celulas da referencia, 2017-2026",
  resultado="a referencia sistematica DESCE, 0,8884 -> 0,8425, -0,00395/ano "
  "(G6/G25), com concordancia do T4 da C3 e de REG-02",
  n="9 cenas, um instrumento", poder="direccao sim, dimensao nao",
  falta="certificar a serie Landsat da referencia - outra agencia, outro sensor, "
  "outra cadeia de correccao. ESTA EM DISCO e mede a referencia a cair 0,888 -> "
  "0,874 -> 0,862, ou seja -0,026 contra os -0,054 do Sentinel-2",
  custo="BAIXO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="ERA SUSTENTADA, e o proprio campo de instrumento independente do CSV diz "
       "'NAO - falta a serie Landsat'. O Controlo 1 e explicito: sem instrumento "
       "independente o facto vai para NAO TESTAVEL, nao para PASSA PARA CIMA. E o "
       "D4 - que esta na lista fechada - declara 'instrumento herdado de B10', mas "
       "B10/INS-03 sustenta que a referencia esta CONTAMINADA, e o que D4 afirma e "
       "a proposicao de INS-04, que a referencia esta EM DECLINIO. D4 empresta a "
       "INS-04 o instrumento de INS-03. E a unica coisa a corrigir em D4 e "
       "fecha-se certificando um ficheiro que ja existe.",
  origem="R10 do adversario da C4 - alteracao obrigatoria 10")

p("INS-05", estatuto="LEITURA RETIRADA - NAO E CAUSA CANDIDATA",
  procurado_onde="nenhum - a leitura esta retirada por inteiro",
  resultado="RETIRADA", n="-", poder="-",
  falta="nada: a linha nao existe", custo="-", consequencia="-",
  decisao="NAO USAR EM NENHUMA FORMA",
  nota="A comparacao de fossos ABSOLUTOS entre dois indices com niveis de "
       "referencia diferentes (NDVI ~0,87, NDMI ~0,50) e saturacao diferente nao e "
       "valida; e a assimetria existe em TODOS os catorze anos (2015: 0,102 contra "
       "0,066). Recolocada sobre variacoes desde a base, a razao e 1,53 (ESTE) e "
       "1,36 (OESTE). Era alem disso uma afirmacao de etiologia dentro de uma "
       "adenda da C2 - C4 a correr dentro da C2. Inflaciona a contagem de 59 "
       "candidatas sem ser candidata.",
  origem="reetiquetagem C5 (era NAO TESTADA)")

p("INS-06", estatuto="NUNCA PROCURADA",
  procurado_onde="as duas cenas S2C, fora do pomar - o unico controlo de cena "
  "existente corre sobre a MEDIA",
  resultado="sem ensaio", n="0", poder="nulo",
  falta="medir o desvio-padrao e a assimetria das celulas FORA do pomar nas duas "
  "cenas S2C - TRES LINHAS sobre ficheiros que ja estao em disco",
  custo="NULO", consequencia="ALTA", decisao="PROCURAR - PRIORIDADE 1",
  nota="Um degrau de sensor NAO E UNIFORME em NDVI: uma diferenca de bandas ou de "
       "correccao atmosferica actua de forma diferente a 0,89 e a 0,70, e o que "
       "isso produz e um alargamento da cauda inferior. TODAS as grandezas-titulo "
       "desta cadeia - area em defice, dispersao, fraccao, M2, as 2,60/3,58 ha - "
       "SAO ESTATISTICAS DE CAUDA. INS-01 fecha a media e NAO fecha isto. E o "
       "teste com maior raio de explosao de toda a cadeia por unidade de esforco: "
       "se a cauda se alargar, todos os numeros-titulo movem-se ao mesmo tempo.",
  origem="reetiquetagem C5: rotulo confirmado, prioridade elevada")

# ---------------------------------------------------------------------------
with io.open(ENTRADA, encoding="utf-8-sig", newline="") as f:
    orig = list(csv.DictReader(f, delimiter=";"))

falta = [r["id"] for r in orig if r["id"] not in R]
extra = [k for k in R if k not in {r["id"] for r in orig}]
assert not falta, "sem re-derivacao: %s" % falta
assert not extra, "id inventado: %s" % extra

def curta(txt):
    """Normaliza a decisao em quatro classes contaveis.

    A decisao longa fica na coluna ao lado. Esta coluna existe porque foi
    exactamente a agregacao por uma coluna de texto livre que produziu o
    '41 = ninguem procurou' que esta camada teve de desfazer: a prosa cuidada
    nao sobrevive a agregacao, e e a agregacao que viaja.
    """
    t = txt.upper()
    if t.startswith("NAO PROCURAR") or t.startswith("NAO USAR"):
        return "NAO PROCURAR"
    if t.startswith("PROCURAR"):
        return "PROCURAR"
    if t.startswith("FECHADA"):
        return "JA FECHADA"
    if t.startswith("RESOLVIDA"):
        return "JA FECHADA"
    raise ValueError(txt)


COLS = ["id", "classe", "causa", "estatuto_C4", "estatuto_C5", "procurado_onde",
        "resultado", "n", "poder_do_desenho", "o_que_falta", "custo",
        "consequencia", "decisao_C5", "decisao_detalhe", "nota_C5",
        "origem_da_alteracao"]
with io.open(SAIDA, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(COLS)
    for r in orig:
        d = R[r["id"]]
        w.writerow([r["id"], r["classe"], r["causa"], r["estatuto"],
                    d["estatuto"], d["procurado_onde"], d["resultado"], d["n"],
                    d["poder"], d["falta"], d["custo"], d["consequencia"],
                    curta(d["decisao"]), d["decisao"], d["nota"], d["origem"]])

# ------------------------------------------------------------------ contagens
c4 = Counter(r["estatuto"] for r in orig)
c5 = Counter(R[r["id"]]["estatuto"] for r in orig)
nt = [r["id"] for r in orig if r["estatuto"] == "NAO TESTADA"]
nt5 = Counter(R[i]["estatuto"] for i in nt)
dec = Counter(curta(R[r["id"]]["decisao"]) for r in orig)
nunca = c5.get("NUNCA PROCURADA", 0) + c5.get("NUNCA PROCURADA COM O INSTRUMENTO CERTO", 0)

print("=" * 74)
print("C5 · RE-ETIQUETAGEM DO LIVRO-RAZAO — contagens calculadas dos ficheiros")
print("=" * 74)
print("\nlinhas de entrada: %d   linhas de saida: %d\n" % (len(orig), len(orig)))

print("ESTATUTO DA C4 (o que viajou para cima)")
for k, v in c4.most_common():
    print("  %-28s %3d" % (k, v))

print("\nESTATUTO RE-DERIVADO PELA C5 (dos campos de evidencia)")
for k, v in c5.most_common():
    print("  %-42s %3d" % (k, v))

print("\nAS %d LINHAS QUE A C4 ROTULOU 'NAO TESTADA' = 'ninguem procurou'" % len(nt))
for k, v in nt5.most_common():
    print("  %-42s %3d" % (k, v))
genuinas = nt5.get("NUNCA PROCURADA", 0)
print("  %s" % ("-" * 46))
print("  genuinamente nunca procuradas .............. %3d de %d" % (genuinas, len(nt)))
print("  MAL ROTULADAS .............................. %3d de %d" % (len(nt) - genuinas, len(nt)))
achadas = (nt5.get("ENCONTRADA SEM PAR", 0) + nt5.get("ENCONTRADA SEM ENSAIO", 0)
           + nt5.get("ENCONTRADA SEM NIVEL NORMAL", 0))
print("  dessas, PROCURADAS E ENCONTRADAS em Ganfei . %3d" % achadas)
print("  dessas, procuradas so FORA de Ganfei ....... %3d" % nt5.get("SO FORA DE GANFEI", 0))

exc = c5.get("EXCLUIDA", 0)
print("\nO NUMERO QUE O RELATORIO TEM DE LEVAR")
print("  das %d causas candidatas, com instrumento independente e desenho" % len(orig))
print("  falsificavel, estao excluidas: %d  (a C4 publicava 7)" % exc)
naocand = (c5.get("NAO E CAUSA CANDIDATA NO CORPO PRINCIPAL", 0)
           + c5.get("LEITURA RETIRADA - NAO E CAUSA CANDIDATA", 0))
print("  linhas que nao sao candidatas no corpo principal: %d" % naocand)
print("  candidatas efectivas: %d" % (len(orig) - naocand))

print("\nDECISAO DA C5 (coluna normalizada `decisao_C5`)")
for k, v in dec.most_common():
    print("  %-28s %3d" % (k, v))
print("\n  «45 a procurar» NAO sao 45 campanhas. Repartidas por custo:")
cw = Counter(R[r["id"]]["custo"].split()[0] for r in orig
             if curta(R[r["id"]]["decisao"]) == "PROCURAR")
for k in ("NULO", "BAIXO", "MEDIO", "ALTO", "-"):
    if cw.get(k):
        r = ("sem custo proprio: corre por dentro de outra linha"
             if k == "-" else "")
        print("    custo %-6s %3d  %s" % (k, cw[k], r))
assert sum(cw.values()) == dec["PROCURAR"], "a reparticao por custo nao fecha"
print("    (NULO = ler um ficheiro ou fazer uma pergunta; BAIXO = mais uma")
print("     linha num ensaio que ja vai ser pago; MEDIO = campanha propria)")

print("\n  Das que decido NAO procurar, TODAS continuam NAO EXCLUIDAS,")
print("  e o relatorio tem de as levar assim:")
for r in orig:
    d = R[r["id"]]
    if curta(d["decisao"]) == "NAO PROCURAR":
        print("    %-8s %-46s [%s]" % (r["id"], r["causa"][:46], d["estatuto"]))

print("\ngravado: %s" % SAIDA)
