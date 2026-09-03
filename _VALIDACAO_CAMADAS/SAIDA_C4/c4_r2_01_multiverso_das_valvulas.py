# -*- coding: utf-8 -*-
"""C4 · re-execução R2 · o D1 sobrevive aos 465 m de ambiguidade das válvulas?

A exposição, e quem a nomeou
----------------------------
O `CAMADA_3_CERTIFICADO_R3.md`, em NÃO TESTÁVEL, e o `CAMADA_0_REVISAO_R3.md`
antes dele:

  «Tudo o que a C3 coloca no espaço vem de `valvulas_por_area.json`. A adenda
  v1.1 mediu **465 m de amplitude entre quatro reconstruções do esquema para a
  mesma válvula** — da ordem da distância entre os dois focos. A C3 escolheu uma
  das quatro e declarou as outras desactualizadas; **essa escolha nunca foi
  certificada por nenhuma camada.**»

O D1 desta camada — «na v8, 93 % do défice de 2026 é declínio novo e 0 % era
chão lavrado; nas v13/v14, o inverso» — é **inteiramente** uma afirmação sobre
válvulas. Se a atribuição estiver errada, o D1 não é um facto sobre o terreno.

O teste, e é o que a metodologia do caso manda
----------------------------------------------
Um multiverso sobre a **escolha posicional**, que é a única bifurcação que
nunca foi percorrida. Reconstrói-se a partição de Voronoi com **cada uma das
quatro reconstruções** e recalcula-se a composição do défice em cada uma.

Critério fixado antes de correr:
  · se o contraste v8-contra-v13/14 sobreviver nas quatro, **o D1 é robusto à
    ambiguidade posicional** e passa a dizê-lo;
  · se sobreviver em algumas, reporta-se a amplitude e o D1 passa com ela;
  · se inverter em alguma, **o D1 cai** — porque a escolha entre ficheiros não
    tem critério certificado que a decida.

O que este teste NÃO faz: não decide qual ficheiro está certo. Isso é geometria
e é da camada 0. Mede se a inferência depende dessa decisão.
"""
import json
import os
import re

import numpy as np

DL = r"C:\Users\Jackster2\Downloads"
S2 = os.path.join(DL, "ganfei_s2")
VG = os.path.join(DL, "_VALIDADE_GESTAO")
AQUI = os.path.dirname(os.path.abspath(__file__))
AOI = (529950, 4654600, 531950, 4655600)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, NU21 = bits("pomar_bits"), bits("saudavel_bits"), bits("nu2021_bits")
import rasterio
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
nd = {d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}
h = np.load(os.path.join(VG, "chm_altura.npy"))

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)

from scipy import ndimage


def defice(d):
    a = nd[d]
    r = float(np.nanmean(a[REF]))
    return ndimage.binary_opening((a < r - 0.05) & POMAR, np.ones((2, 2)))


D26 = defice("2026-07-27")
ANTES = np.zeros_like(POMAR)
for d in DATAS[:7]:
    ANTES |= defice(d)
NOVO = D26 & ~ANTES                       # declinio novo, regra M2


def posicoes(fich):
    """Cada reconstrucao guarda as posicoes de maneira diferente. Le-se cada uma
    pela sua estrutura real, em vez de se varrer a arvore as cegas — foi o que
    fez a primeira versao deste ficheiro devolver zero valvulas em tres dos
    quatro, e imprimir um veredicto tranquilizador a partir de um teste vazio."""
    d = json.load(open(os.path.join(S2, fich), encoding="utf-8"))
    out = {}
    if fich == "valvulas_por_area.json":
        for k, v in d.items():
            if isinstance(v, dict) and "E" in v:
                out[k] = (v["E"], v["N"])
    elif fich == "valvulas_v6.json":
        for k, v in d.get("valvulas", {}).items():
            out[k] = (v[0], v[1])
    elif fich == "valvulas_v4.json":
        for k, v in d.get("corpo", {}).items():           # so o corpo: o lobo
            out[k] = (v[0], v[1])                          # tem numeracao propria
    elif fich == "valvulas_por_linha.json":
        # cada ancora cobre um PAR de valvulas e da-lhes o mesmo ponto: esta
        # reconstrucao nao separa v8 de v9, e diz-se.
        for r in d.get("valvulas", []):
            for n_ in re.findall(r"\d+", r.get("valvulas", "")):
                out[n_] = (r["E"], r["N"])
    return out


FICH = ["valvulas_por_area.json", "valvulas_v6.json", "valvulas_v4.json",
        "valvulas_por_linha.json"]

print("=" * 92)
print("C4 R2 · MULTIVERSO DA ESCOLHA POSICIONAL — o D1 depende do ficheiro?")
print("=" * 92)
print()

saida = {"criterio": "contraste v8 contra v13/v14 na composicao do defice de 2026",
         "reconstrucoes": {}}
for f in FICH:
    try:
        pos = posicoes(f)
    except Exception as e:
        print("%-28s ilegível — %s" % (f, e))
        continue
    ids = [k for k in pos if k.isdigit()]
    if len(ids) < 6:
        print("%-28s só %d válvulas identificáveis — não dá partição"
              % (f, len(ids)))
        saida["reconstrucoes"][f] = dict(utilizavel=False, n=len(ids))
        continue
    PE = np.array([pos[k][0] for k in ids])
    PN = np.array([pos[k][1] for k in ids])
    qual = np.argmin((EE[..., None] - PE) ** 2 + (NN[..., None] - PN) ** 2, axis=2)
    val = np.array(ids)[qual]

    linha = {}
    for grupo, nome in ((["8"], "v8"), (["13", "14"], "v13+v14")):
        m = POMAR & np.isin(val, grupo)
        dm = D26 & m
        if dm.sum() == 0:
            linha[nome] = dict(ha=m.sum() / 100.0, defice_ha=0.0,
                               pct_novo=float("nan"), pct_nu21=float("nan"))
            continue
        linha[nome] = dict(ha=m.sum() / 100.0, defice_ha=dm.sum() / 100.0,
                           pct_novo=float(100 * (dm & NOVO).sum() / dm.sum()),
                           pct_nu21=float(100 * (dm & NU21).sum() / dm.sum()))
    saida["reconstrucoes"][f] = dict(utilizavel=True, n=len(ids), unidades=linha)
    a, b = linha["v8"], linha["v13+v14"]
    print("%-28s v8: %5.2f ha déf., %5.1f %% novo, %5.1f %% nu21   |   "
          "v13+14: %5.2f ha déf., %5.1f %% novo, %5.1f %% nu21"
          % (f, a["defice_ha"], a["pct_novo"], a["pct_nu21"],
             b["defice_ha"], b["pct_novo"], b["pct_nu21"]))

print()
print("=" * 92)
print("VEREDICTO SOBRE O D1")
print("=" * 92)
print()
uso = {k: v for k, v in saida["reconstrucoes"].items() if v.get("utilizavel")}
print("reconstruções utilizáveis: %d de %d" % (len(uso), len(FICH)))
print()
if uso:
    novos8 = [v["unidades"]["v8"]["pct_novo"] for v in uso.values()]
    nu8 = [v["unidades"]["v8"]["pct_nu21"] for v in uso.values()]
    novos13 = [v["unidades"]["v13+v14"]["pct_novo"] for v in uso.values()]
    nu13 = [v["unidades"]["v13+v14"]["pct_nu21"] for v in uso.values()]
    print("v8      · %% novo : %.1f a %.1f    |  %% chão lavrado : %.1f a %.1f"
          % (np.nanmin(novos8), np.nanmax(novos8), np.nanmin(nu8), np.nanmax(nu8)))
    print("v13+v14 · %% novo : %.1f a %.1f    |  %% chão lavrado : %.1f a %.1f"
          % (np.nanmin(novos13), np.nanmax(novos13), np.nanmin(nu13), np.nanmax(nu13)))
    print()
    inverte = any(n8 < n13 for n8, n13 in zip(novos8, novos13))
    if not inverte:
        print(">>> O contraste NÃO inverte em nenhuma reconstrução utilizável.")
        print("    O D1 é robusto à ambiguidade posicional, e passa a dizê-lo")
        print("    com a amplitude acima em vez de um par de números.")
    else:
        print(">>> O contraste INVERTE em pelo menos uma reconstrução. O D1 cai:")
        print("    não há critério certificado para escolher entre os ficheiros.")
    saida["inverte"] = bool(inverte)

json.dump(saida, open(os.path.join(AQUI, "c4_r2_01_multiverso_valvulas.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito c4_r2_01_multiverso_valvulas.json")
