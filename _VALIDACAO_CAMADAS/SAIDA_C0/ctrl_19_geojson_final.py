# -*- coding: utf-8 -*-
"""CTRL-19. GeoJSON final dos candidatos a controlo externo.

Junta a geometria (CTRL-13 / CTRL-10) as metricas (CTRL-14), ao compasso
(CTRL-16), as distancias ao poligono `pomar` (CTRL-18) e a leitura de margem
(CTRL-17), e escreve a proveniencia de cada lado de cada poligono e o que
cada bloco controla e nao controla.

Nenhum campo deste ficheiro foi obtido de NDVI ou de qualquer indice.
"""
import json
import os

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
gj = json.load(open(os.path.join(OUT, "controlos.geojson"), encoding="utf-8"))
comp = json.load(open(os.path.join(OUT, "ctrl_16_compasso.json")))
dist = json.load(open(os.path.join(OUT, "ctrl_18_distancias.json")))

LADOS = {
    "C1a": {
        "NO": "caminho de terra sobre o dique/galeria ripicola da margem "
              "esquerda do Minho (visivel nas 7 epocas)",
        "NE": "cabeceira norte da parcela, contra campo lavrado; e o lado "
              "com maior incerteza (+-10 m) porque o solo nu seco entra na "
              "mascara de material claro",
        "SE": "estrada municipal empedrada que sobe do lugar em direccao "
              "a NNE (limite fisico nitido nas 7 epocas)",
        "SO": "cabeceira sul, contra faixa de pousio de ~25 m",
    },
    "C1b": {
        "NO": "mesmo caminho ripicola da margem esquerda",
        "NE": "cabeceira norte contra a faixa de pousio que a separa de C1a",
        "SE": "mesma estrada municipal",
        "SO": "caminho transversal que desce ao lugar; galeria arborea",
    },
    "C1c": {
        "N": "caminho transversal",
        "O": "galeria ripicola e caminho de margem",
        "S": "nucleo edificado do lugar (armazens e habitacao) — o contorno "
             "inclui telhados claros, +-0,3 ha",
        "E": "estrada",
    },
    "C2": {
        "todos": "limite da mancha de periodicidade linear; a O e a N um "
                 "caminho de terra, a E e a S a galeria ripicola do Minho e "
                 "de um braco secundario",
    },
    "C3": {
        "todos": "limite da mancha de periodicidade linear; a N e a E "
                 "caminhos de terra e um conjunto de armazens, a O e a S "
                 "cabeceiras contra campo aberto",
    },
}

PAPEL = {
    "C1a": dict(
        margem="esquerda (mesma do pomar do caso; 0 travessias de agua)",
        estrutura_por_epoca={
            "2004": "campo aberto, sem estrutura",
            "2007": "campo aberto, sem estrutura",
            "2010": "bloco implantado, cobertura clara em linhas",
            "2012": "copado continuo escuro com pontos claros regulares — "
                    "compativel com latada coberta",
            "2021": "linhas separadas por entrelinha aberta + plastico",
            "2023": "linhas separadas por entrelinha aberta (OrtoSat2023)",
            "2025": "camalhoes com tunel/cobertura de plastico continua"},
        controla=["substrato: mesmo aluviao do Minho, margem esquerda",
                  "cota e amplitude de cota semelhantes (6,4 m vs 6,1 m no "
                  "rectangulo do caso)",
                  "clima local e regime de nevoeiro do vale",
                  "posicao ribeirinha e distancia a margem da mesma ordem "
                  "(218 m vs a frente do proprio pomar)",
                  "coorte de plantacao: implantado entre 2007 e 2010, tal "
                  "como o pomar do caso"],
        nao_controla=["especie e cultura actual: entre 2012 e 2021 deixou de "
                      "ter copado fechado e passou a linhas com camalhao e "
                      "cobertura de plastico; a serie 2017-2026 nao e "
                      "comparavel com a de um pomar de latada mantido",
                      "gestao, rega, fertilizacao, tratamentos: proprietario "
                      "desconhecido",
                      "origem da agua: nao determinada; nao ha reservatorio "
                      "nem valvula visivel dentro do bloco na ortofoto",
                      "historico de nivelamento e de movimentacao de terras"],
        veredicto="NAO serve como controlo contemporaneo de kiwi. Serve "
                  "apenas como controlo HISTORICO 2010-2012, e mesmo esse "
                  "com a reserva de a especie nao estar provada."),
    "C1b": dict(
        margem="esquerda (0 travessias)",
        estrutura_por_epoca="igual a C1a",
        controla=["o mesmo que C1a"],
        nao_controla=["o mesmo que C1a; alem disso esta 781 m do bordo do "
                      "pomar, ja fora da mesma unidade de escorrencia"],
        veredicto="igual a C1a."),
    "C1c": dict(
        margem="esquerda (0 travessias)",
        estrutura_por_epoca="estufas permanentes; cobertura fixa",
        controla=["nada de util: e horticultura protegida"],
        nao_controla=["tudo o que interessa a um pomar de latada ao ar livre"],
        veredicto="REJEITADO. Fica delimitado so para nao ser confundido "
                  "com C1b em trabalhos futuros."),
    "C2": dict(
        margem="DIREITA — margem oposta a do pomar do caso. O segmento recto "
               "entre o centroide de C2 e o centroide do pomar atravessa "
               "250 m de agua do Minho. Do lado de Tui.",
        estrutura_por_epoca="vinha/bardo com compasso de 3,35 m em todas as "
                            "epocas verificadas",
        controla=["nada que sirva o caso"],
        nao_controla=["margem, pais, jurisdicao, gestao, origem de agua, "
                      "cultura e compasso — difere em todos"],
        veredicto="REJEITADO, e assinalado a vermelho: e exactamente o tipo "
                  "de bloco que o erro «B1» apanhou. Esta a 293 m do bordo "
                  "do poligono `pomar` e a 2 m do bordo do rectangulo "
                  "declarado, e mesmo assim esta do outro lado do rio."),
    "C3": dict(
        margem="esquerda (0 travessias)",
        estrutura_por_epoca="vinha/bardo com compasso de 2,72 m",
        controla=["substrato aluvionar e clima local, a 87 m do bordo do "
                  "pomar",
                  "serve de par contemporaneo para separar um efeito de "
                  "sitio de um efeito de especie: se o declinio fosse do "
                  "sitio, uma vinha a 87 m no mesmo aluviao devia acusa-lo"],
        nao_controla=["especie (Vitis, nao Actinidia), sistema de conducao, "
                      "compasso, profundidade radicular, exigencia hidrica, "
                      "calendario de rega",
                      "origem da agua: nao determinada"],
        veredicto="Nao e controlo de kiwi. E o unico par contemporaneo util "
                  "para uma pergunta diferente e mais fraca — «o sitio esta "
                  "a degradar-se para qualquer cultura perene?»."),
}

for f in gj["features"]:
    i = f["properties"]["id"]
    if i == "REF":
        f["properties"]["nota"] = ("caixa envolvente dada no enunciado. Nao "
                                   "foi analisada. 19,6 % da sua area e agua "
                                   "do rio; o poligono `pomar` de masks.json, "
                                   "esse, tem 0 % de agua.")
        continue
    f["properties"].update(comp.get(i, {}))
    f["properties"].update(dist.get(i, {}))
    f["properties"]["proveniencia_por_lado"] = LADOS.get(i, {})
    f["properties"].update(PAPEL.get(i, {}))

gj["nota"] = ("Delimitacao feita so a partir de estrutura visivel na "
              "ortofoto (periodicidade de linhas, material de cobertura) e "
              "de geometria (LiDAR, agua, distancias). Nenhum indice de "
              "vegetacao foi lido em nenhuma fase.")
gj["fontes"] = [
    "ortofotos DGT 2004/2006, 2007, 2010, 2012, 2021, 2025 — mosaico 002-3, "
    "EPSG:3763, lidas em janela e reprojectadas para EPSG:32629",
    "OrtoSat2023 (DGT), WMS publico ortos.dgterritorio.gov.pt/wms/ortosat2023",
    "MDT LiDAR DGT 50 cm, 21 mosaicos, EPSG:3763",
    "STAC DGT dgt-be.a.incd.pt:8081 (datas do voo de 2025)"]
json.dump(gj, open(os.path.join(OUT, "controlos.geojson"), "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("-> controlos.geojson  %d feicoes" % len(gj["features"]))
for f in gj["features"]:
    p = f["properties"]
    print("   %-5s %6.2f ha  d_bordo=%s m  compasso=%s m"
          % (p["id"], p["area_ha"], p.get("d_bordo_pomar_m", "-"),
             p.get("compasso_m", "-")))
