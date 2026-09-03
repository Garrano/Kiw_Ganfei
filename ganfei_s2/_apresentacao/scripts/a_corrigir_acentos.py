# -*- coding: utf-8 -*-
"""Ponto 1 da ordem de execucao do memo: acentos no texto DESENHADO.

O memo assinala que a F8 esta sem diacriticos. Verificado e confirmado: quinze
strings desenhadas em ASCII, escritas como se fossem docstring. A F9 tem dez.
Nas restantes figuras o que um scanner ingenuo apanha sao **chaves de
dicionario** — `"OESTE com pergola"` e chave do `landsat.json` e nao pode ser
alterada sem partir a leitura.

Corrige-se so o texto que e desenhado. Cada substituicao e literal e explicita.
"""
import io
import os

FIG = r"C:\Users\Jackster2\Downloads\ganfei_s2\figuras"

F8 = [
    ("tempo quase imovel", "tempo quase imóvel"),
    ("terraco aluvial da margem esquerda do Minho  ·  ",
     "terraço aluvial da margem esquerda do Minho  ·  "),
    ("clima atlantico, Entre Douro e Minho  ·  origem de agua unica",
     "clima atlântico, Entre Douro e Minho  ·  origem de água única"),
    ("O que a exploracao decidiu. Trinta e cinco anos de emparcelamento, ",
     "O que a exploração decidiu. Trinta e cinco anos de emparcelamento, "),
    ('"porta-enxertos e plantacoes."', '"porta-enxertos e plantações."'),
    ('"decadas"', '"décadas"'),
    ("o resto do pomar fecha o fosso a referencia:  ",
     "o resto do pomar fecha o fosso à referência:  "),
    ("Cada faixa tem a sua propria escala. E a razao entre elas que e o argumento: ",
     "Cada faixa tem a sua própria escala. E a razão entre elas que é o argumento: "),
    ("o acontecimento ocupa dois anos, a conjuntura que o hospeda ocupa trinta e cinco, ",
     "o acontecimento ocupa dois anos, a conjuntura que o hospeda ocupa trinta e cinco, "),
    ("e a estrutura nao tem data.", "e a estrutura não tem data."),
    ("Companheira da F3, nao substituta: a F3 poe os mesmos factos num so eixo, para ver coincidencias de data.",
     "Companheira da F3, não substituta: a F3 põe os mesmos factos num só eixo, para ver coincidências de data."),
    ("A estrutura nao causa o acontecimento \u2014 condiciona-o: as duas manchas ocupam posicoes hidraulicas opostas ",
     "A estrutura não causa o acontecimento \u2014 condiciona-o: as duas manchas ocupam posições hidráulicas opostas "),
    ("e comportam-se de maneira diferente.", "e comportam-se de maneira diferente."),
    ("Fonte de cada registo: estrutura \u2014 MDT LiDAR 50 cm, analises de solo, SAR de dez Invernos.  ",
     "Fonte de cada registo: estrutura \u2014 MDT LiDAR 50 cm, análises de solo, SAR de dez Invernos.  "),
    ("conjuntura \u2014 testemunho do gestor e tabela de valvulas.  acontecimento \u2014 Sentinel-2, LiDAR de 06-07-2025, ERA5-Land.",
     "conjuntura \u2014 testemunho do gestor e tabela de válvulas.  acontecimento \u2014 Sentinel-2, LiDAR de 06-07-2025, ERA5-Land."),
    ("Pergola ainda a instalar-se", "Pérgola ainda a instalar-se"),
    ("visivel nas ortofotos de 2010 e 2012", "visível nas ortofotos de 2010 e 2012"),
    ("valvulas 2-5 (B1), sobre raiz de Summer Kiwi", "válvulas 2-5 (B1), sobre raiz de Summer Kiwi"),
    ("as mesmas valvulas 2-5  ·  a rede existiu so no B1",
     "as mesmas válvulas 2-5  ·  a rede existiu só no B1"),
    ("+11,16 ha de pomar novo em quatro anos", "+11,16 ha de pomar novo em quatro anos"),
    ("4,09  ·  2,85  ·  1,50  ·  2,72 ha  —  toda a agua da mesma origem",
     "4,09  ·  2,85  ·  1,50  ·  2,72 ha  —  toda a água da mesma origem"),
    ("22-07 a 09-08-2024  ·  0,875 \u2192 0,741\\ncom o resto do bloco imovel",
     "22-07 a 09-08-2024  ·  0,875 \u2192 0,741\\ncom o resto do bloco imóvel"),
    ("N3 a +0,296 da referencia\\n(estava a \u22120,046 em 2022/23)",
     "N3 a +0,296 da referência\\n(estava a \u22120,046 em 2022/23)"),
    ("N3 a 0,27 m  ·  OESTE a 2,17 m\\no unico instrumento nao-optico",
     "N3 a 0,27 m  ·  v8/B2 a 2,17 m\\no único instrumento não-óptico"),
    ("1,32 ha, depois de tres anos a 0,00", "1,32 ha, depois de sete anos a descer"),
    ("a videira abre a um terco do pomar sao\\nJul-Ago de 2026 o mais humido da decada",
     "a videira abre a um terço do pomar são\\nJul-Ago de 2026 o mais húmido da década"),
    ("cota mediana 6,64 m", "cota mediana 6,64 m"),
    ("carencia de calcio", "carência de cálcio"),
    ("confirmada em duas matrizes", "confirmada em duas matrizes"),
    ("o solo mais pobre da exploracao", "o solo mais pobre da exploração"),
    ("radar sempre anomalo, dez Invernos", "radar sempre anómalo, dez Invernos"),
    ("500 m  ·  hidraulicamente opostos", "500 m  ·  hidraulicamente opostos"),
    ("os dois primeiros sao medidos no proprio voo",
     "os dois primeiros são medidos no próprio voo"),
    ("O que nao muda. Nao tem data, e e o registo mais solido do dossie.",
     "O que não muda. Não tem data, e é o registo mais sólido do dossiê."),
    ("O que se mede. Dois anos, ao dia. E o registo mais fragil: e o que mais mudou de leitura em quarenta e oito horas.",
     "O que se mede. Dois anos, ao dia. É o registo mais frágil: é o que mais mudou de leitura em quarenta e oito horas."),
    ("ampliado acima", "ampliado acima"),
    ("Defice de copado", "Défice de copado"),
]

F9 = [
    ("area em defice  (ha)", "área em défice  (ha)"),
    ("A serie publicada somava videira viva a definhar com chao onde a planta ja nao existe. ",
     "A série publicada somava videira viva a definhar com chão onde a planta já não existe. "),
    ("Separadas, o copado vivo desce sete anos ate um piso de 0,66 ha e multiplica por sete em dois.",
     "Separadas, o copado vivo desce sete anos até um piso de 0,66 ha e multiplica por sete em dois."),
    ("Criterio: altura MDS\u2212MDT \u2265 0,5 m na grelha de 10 m, voo LiDAR DGT de 06-07-2025 (data do tempo GPS dos pontos, nao dos metadados).  ",
     "Critério: altura MDS\u2212MDT \u2265 0,5 m na grelha de 10 m, voo LiDAR DGT de 06-07-2025 (data do tempo GPS dos pontos, não dos metadados).  "),
    ("Defice = NDVI abaixo da referencia da propria cena menos 0,05.",
     "Défice = NDVI abaixo da referência da própria cena menos 0,05."),
    ("A abertura morfologica 2\u00d72 corre UMA VEZ sobre o poligono e so depois se divide \u2014 as duas linhas somam exactamente a cinzenta em todas as cenas.  ",
     "A abertura morfológica 2\u00d72 corre UMA VEZ sobre o polígono e só depois se divide \u2014 as duas linhas somam exactamente a cinzenta em todas as cenas.  "),
    ("Uma versao anterior dividia primeiro e lia zeros que eram costura.",
     "Uma versão anterior dividia primeiro e lia zeros que eram costura."),
    ("VIES DE SOBREVIVENCIA: a particao e de 2025, logo 'copado vivo' e o que ainda estava vivo nessa data. Mortalidade consumada antes de 2025 conta como chao em toda a serie, ",
     "VIÉS DE SOBREVIVÊNCIA: a partição é de 2025, logo «copado vivo» é o que ainda estava vivo nessa data. Mortalidade consumada antes de 2025 conta como chão em toda a série, "),
    ("e a melhoria de 2017 a 2024 e medida so sobre sobreviventes.",
     "e a melhoria de 2017 a 2024 é medida só sobre sobreviventes."),
    ("A mascara vem do LiDAR e a serie e de NDVI \u2014 instrumentos independentes.  Niveis absolutos nao comparaveis entre plataformas (vies S2C \u22480,048 NDVI).",
     "A máscara vem do LiDAR e a série é de NDVI \u2014 instrumentos independentes.  Níveis absolutos não comparáveis entre plataformas."),
    ("com pergola em 06-07-2025  ·  26,54 ha  —  copado vivo",
     "com pérgola em 06-07-2025  ·  26,54 ha  —  copado vivo"),
    ("sem pergola  ·  3,77 ha  —  ausencia de planta, nao doenca",
     "sem pérgola  ·  3,77 ha  —  ausência de planta, não doença"),
    ("poligono inteiro  ·  30,31 ha  —  a serie publicada",
     "polígono inteiro  ·  30,31 ha  —  a série publicada"),
    ("piso 0,66 \u2013 0,67 ha", "piso 0,66 \u2013 0,67 ha"),
    ("Defice de copado em Ganfei", "Défice de copado em Ganfei"),
    ("a particao vem daqui", "a partição vem daqui"),
]

for nome, subs in (("f8_braudel.py", F8), ("f9_serie_separada.py", F9)):
    p = os.path.join(FIG, nome)
    s = io.open(p, encoding="utf-8").read()
    n = 0
    for a, b in subs:
        if a in s and a != b:
            s = s.replace(a, b); n += 1
    io.open(p, "w", encoding="utf-8").write(s)
    print("%-24s %2d substituições aplicadas" % (nome, n))

# garantia de renderizacao correcta do sinal menos e das fontes
CAB = ("import matplotlib\nmatplotlib.use(\"Agg\")\n")
NOVO = ("import matplotlib\nmatplotlib.use(\"Agg\")\n"
        "matplotlib.rcParams[\"font.family\"] = \"DejaVu Sans\"\n"
        "matplotlib.rcParams[\"axes.unicode_minus\"] = False\n"
        "matplotlib.rcParams[\"svg.fonttype\"] = \"path\"\n"
        "matplotlib.rcParams[\"pdf.fonttype\"] = 42\n")
import glob
for p in sorted(glob.glob(os.path.join(FIG, "f*.py"))):
    s = io.open(p, encoding="utf-8").read()
    if CAB in s and "axes.unicode_minus" not in s:
        io.open(p, "w", encoding="utf-8").write(s.replace(CAB, NOVO, 1))
        print("  cabeçalho de rcParams acrescentado a %s" % os.path.basename(p))
