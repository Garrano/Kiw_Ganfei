# -*- coding: utf-8 -*-
"""T2 — o que existe entre 2025-08-14 e 2026-07-27, e que a regra descartou.

A pergunta que falta, textual
-----------------------------
`CAMADA_2_ADVERSARIO_R2.md`, transversal B:

  «Ninguém perguntou o que acontece ENTRE 2025-08-14 e 2026-07-27. O
  acontecimento inteiro está datado por duas cenas separadas por onze meses…
  Um acontecimento catastrófico único e dois declínios sucessivos são
  indistinguíveis neste desenho. Um degrau entre dois pontos a onze meses de
  distância é uma interpolação, não uma medição.»

E dizia o que era preciso, sem o ir buscar:

  «a contagem de cenas Sentinel-2 disponíveis entre 2025-08-14 e 2026-07-27 que
  a regra de plena estação descartou, e a sua distribuição por dia-do-ano.»

O que este teste faz
--------------------
Pergunta ao catálogo — o mesmo STAC público de onde veio toda a série — quantas
cenas existem no intervalo, com que nebulosidade e em que dia-do-ano.

**Não descarrega bandas e não calcula NDVI nenhum.** É uma contagem. Se houver
cenas de plena estação em 2026 antes de 27-07, ou em Agosto-Setembro de 2025
depois de 14-08, a pergunta é respondível sem dados novos — e isso muda o
desenho, não só a confiança.

O critério de plena estação, para se saber o que se está a contar: Julho e
Agosto, que é o que a série usa (DOY 183 a 243 nas nove cenas).
"""
import datetime as dt
import json
import os

import pystac_client

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI_LL = [-8.63713, 42.04283, -8.61489, 42.05185]     # bbox da AOI em WGS84
INI, FIM = "2025-08-15", "2026-07-26"                 # estritamente entre as duas

cat = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
itens = list(cat.search(collections=["sentinel-2-l2a"], bbox=AOI_LL,
                        datetime="%s/%s" % (INI, FIM)).items())

linhas = []
for it in itens:
    d = it.datetime
    linhas.append(dict(data=d.strftime("%Y-%m-%d"),
                       doy=d.timetuple().tm_yday,
                       cena=it.id,
                       plataforma=it.properties.get("platform", ""),
                       nuvens=float(it.properties.get("eo:cloud_cover", 99))))
linhas.sort(key=lambda r: r["data"])

print("=" * 88)
print("T2 · CENAS SENTINEL-2 ENTRE %s E %s" % (INI, FIM))
print("=" * 88)
print()
print("total no catálogo: %d" % len(linhas))
print()

LIMPAS = [r for r in linhas if r["nuvens"] < 20]
PLENA = [r for r in LIMPAS if 182 <= r["doy"] <= 244]

print("%-12s %5s %8s %-12s %s" % ("data", "DOY", "nuvens", "plataforma", "plena?"))
for r in LIMPAS:
    pl = 182 <= r["doy"] <= 244
    print("%-12s %5d %7.1f%% %-12s %s"
          % (r["data"], r["doy"], r["nuvens"], r["plataforma"].replace("sentinel-", "S"),
             "SIM" if pl else ""))

print()
print("com menos de 20 %% de nuvem : %d" % len(LIMPAS))
print("dessas, em plena estação   : **%d**" % len(PLENA))

print()
print("=" * 88)
print("VEREDICTO SOBRE A PERGUNTA QUE FALTA")
print("=" * 88)
print()
if PLENA:
    print("A pergunta É RESPONDÍVEL sem dados novos. Existem %d cenas de plena" % len(PLENA))
    print("estação entre as duas datas que a série usa:")
    for r in PLENA:
        print("   %s  (DOY %d, %.1f %% de nuvem, %s)"
              % (r["data"], r["doy"], r["nuvens"], r["plataforma"]))
    print()
    print("Com elas, distingue-se um acontecimento agudo de dois declínios")
    print("sucessivos — que é a diferença entre procurar o que aconteceu num")
    print("momento e desenhar contenção. NÃO se corre aqui: é análise nova, e")
    print("esta é a camada que a identifica, não a que a faz.")
else:
    print("Não há cenas de plena estação no intervalo com nuvem aceitável.")
    print("A pergunta NÃO é respondível com o critério actual, e a alternativa")
    print("é alargar a janela fenológica — o que muda a comparabilidade de toda")
    print("a série e não se faz de ânimo leve.")

json.dump(dict(intervalo=[INI, FIM], total=len(linhas), limpas=len(LIMPAS),
               plena_estacao=len(PLENA), cenas=LIMPAS),
          open(os.path.join(VG, "t2_cenas_descartadas.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito t2_cenas_descartadas.json")
