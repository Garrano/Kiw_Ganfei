# -*- coding: utf-8 -*-
"""A partição da carta-base sobrevive a trocar de reconstrução do esquema?

PORQUE ISTO TEM DE CORRER ANTES DA CAMADA DE REGA
--------------------------------------------------
Há **quatro** reconstruções das posições das válvulas em disco, feitas do mesmo
desenho por métodos diferentes: `valvulas_por_area.json` (a que o
`c1_00_comum.valvulas()` devolve e a carta-base usou), `valvulas_v4.json`,
`valvulas_v6.json` e `valvulas_por_linha.json`.

**Discordam entre 92 e 398 m.** O espaçamento entre válvulas vizinhas ao longo
da banda é de 90 a 100 m. Ou seja: a discordância é **maior do que a distância
entre válvulas**, e em `v6` a ordem de duas delas (12 e 13) chega a inverter-se.

A carta-base parte cada ponto para o sector da **válvula mais próxima**. Se essa
partição depender de qual reconstrução se escolheu, então a P11 desenha uma
escolha nossa e não uma estrutura — que é exactamente a falha que este processo
já retirou dezanove vezes.

A HIPÓTESE, FIXADA ANTES DE CORRER
-----------------------------------
    H · a partição por sector é robusta à escolha de reconstrução.

    FALSIFICA-SE se, em qualquer das quatro, algum sector se afastar mais de
    **25 %** da área que o gestor declara — o mesmo limiar que o
    `preparar_base.py` já usou, e pela mesma razão: é o critério que estava
    escrito antes de se ver o resultado.

    Segunda medida, que é a que importa para a camada de rega: **que fracção
    da área muda de sector** entre reconstruções. Se for pequena, a camada
    pode desenhar sectores; se for grande, desenha só válvulas.
"""
import io
import json
import os
import re

import numpy as np

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEM = ["B1", "B2", "Erica Novo", "B3", "B4"]
DECLARADO = {"B1": 12.63, "B2": 9.65, "Erica Novo": 4.87, "B3": 9.01, "B4": 3.78}


def carrega():
    R = {}
    p = json.load(io.open(os.path.join(D, "_VALIDACAO_CAMADAS/valvulas_por_area.json"),
                          encoding="utf-8"))
    R["por_area"] = {int(k): (v["E"], v["N"]) for k, v in p.items()}
    BLOCO = {int(k): v["bloco"] for k, v in p.items()}
    v4 = json.load(io.open(os.path.join(D, "ganfei_s2/valvulas_v4.json"), encoding="utf-8"))
    R["v4"] = {int(k): tuple(v) for k, v in v4["corpo"].items()}
    v6 = json.load(io.open(os.path.join(D, "ganfei_s2/valvulas_v6.json"), encoding="utf-8"))
    R["v6"] = {int(k): tuple(v) for k, v in v6["valvulas"].items()}
    L = json.load(io.open(os.path.join(D, "_VALIDACAO_CAMADAS/valvulas_por_linha.json"),
                          encoding="utf-8"))
    pl = {}
    for r in L["valvulas"]:
        for n in re.findall(r"\d+", r["valvulas"]):
            pl.setdefault(int(n), (r["E"], r["N"]))
    R["por_linha"] = pl
    return R, BLOCO


REC, BLOCO = carrega()
d = np.load(os.path.join(AQUI, "base_terreno.npz"))
Z, SEC, bb, pix = d["Z"], d["sector"], tuple(d["bb"]), float(d["pix"])
NL, NC = Z.shape
META = json.load(io.open(os.path.join(AQUI, "base_sectores.json"), encoding="utf-8"))
COD = META["codigo"]
E, N = np.meshgrid(bb[0] + (np.arange(NC) + .5) * pix,
                   bb[3] - (np.arange(NL) + .5) * pix)
KIWI = SEC > 0
BANDA = KIWI & (SEC != COD["B1"])
print("área de kiwi na banda: %.2f ha  ·  B1: %.2f ha"
      % (BANDA.sum() * pix * pix / 1e4,
         (SEC == COD["B1"]).sum() * pix * pix / 1e4))
print()

# ── quem discorda de quem, em metros ────────────────────────────────────────
base = REC["por_area"]
print("discordância contra `por_area`, por válvula (m):")
print("  %-5s %8s %8s %8s" % ("v", "v4", "v6", "por_linha"))
for k in sorted(base):
    fs = []
    for nome in ("v4", "v6", "por_linha"):
        o = REC[nome].get(k)
        fs.append(np.hypot(*(np.array(base[k]) - np.array(o))) if o else np.nan)
    print("  v%-4d %8.0f %8.0f %8.0f" % (k, *fs))
esp = sorted(np.hypot(np.diff([base[k][0] for k in sorted(base)]),
                      np.diff([base[k][1] for k in sorted(base)])))
print("  espaçamento entre válvulas consecutivas: mediana %.0f m (min %.0f, máx %.0f)"
      % (np.median(esp), esp[0], esp[-1]))
print()

# ── a partição, em cada reconstrução ────────────────────────────────────────
MAPAS = {}
for nome, P in REC.items():
    vk = [k for k in sorted(P) if BLOCO.get(k) and BLOCO[k] != "B1"]
    if len(vk) < 8:
        print("%-10s só tem %d válvulas da banda — não se compara" % (nome, len(vk)))
        continue
    dv = np.stack([np.hypot(E - P[k][0], N - P[k][1]) for k in vk])
    perto = np.array(vk)[np.argmin(dv, axis=0)]
    S = np.zeros((NL, NC), "int8")
    S[SEC == COD["B1"]] = COD["B1"]
    for k in vk:
        S[BANDA & (perto == k) & (S == 0)] = COD[BLOCO[k]]
    MAPAS[nome] = S

print("%-12s %s" % ("reconstrução", "  ".join("%11s" % b for b in ORDEM)))
print("%-12s %s" % ("declarado", "  ".join("%8.2f ha" % DECLARADO[b] for b in ORDEM)))
print("-" * 78)
falsifica = []
for nome, S in MAPAS.items():
    linha, mau = [], False
    for b in ORDEM:
        a = (S == COD[b]).sum() * pix * pix / 1e4
        dif = 100 * (a - DECLARADO[b]) / DECLARADO[b]
        linha.append("%8.2f ha" % a)
        if abs(dif) > 25:
            mau = True
    print("%-12s %s   %s" % (nome, "  ".join(linha), "FALSIFICA" if mau else ""))
    if mau:
        falsifica.append(nome)

print()
print("desvio máximo contra o declarado, por reconstrução:")
for nome, S in MAPAS.items():
    pior = max(abs(100 * ((S == COD[b]).sum() * pix * pix / 1e4 - DECLARADO[b])
                   / DECLARADO[b]) for b in ORDEM)
    print("  %-12s %5.1f %%" % (nome, pior))

# ── quanto da área muda de sector ───────────────────────────────────────────
print()
print("fracção da BANDA que muda de sector, entre pares de reconstruções:")
nomes = list(MAPAS)
pior_par, pior_v = None, 0.0
for i in range(len(nomes)):
    for j in range(i + 1, len(nomes)):
        a, b = MAPAS[nomes[i]], MAPAS[nomes[j]]
        muda = 100 * np.mean(a[BANDA] != b[BANDA])
        print("  %-11s vs %-11s %5.1f %%" % (nomes[i], nomes[j], muda))
        if muda > pior_v:
            pior_v, pior_par = muda, (nomes[i], nomes[j])
estavel = np.ones(BANDA.shape, bool)
for nome in nomes[1:]:
    estavel &= (MAPAS[nome] == MAPAS[nomes[0]])
estavel &= BANDA
print()
print("  concordam as %d reconstruções em %.1f %% da banda (%.2f ha de %.2f ha)"
      % (len(nomes), 100 * estavel.sum() / BANDA.sum(),
         estavel.sum() * pix * pix / 1e4, BANDA.sum() * pix * pix / 1e4))

print()
print("=" * 78)
if falsifica:
    print("H FALSIFICADA em: %s" % ", ".join(falsifica))
    print("-> a camada de rega NAO desenha sectores por válvula.")
else:
    print("H NAO falsificada: nenhuma reconstrução afasta um sector mais de 25 %%")
    print("   da área declarada. A partição POR SECTOR aguenta a troca.")
print("   Mas a atribuição POR VÁLVULA muda em %.1f %% da banda no pior par (%s)."
      % (pior_v, " vs ".join(pior_par)))
print("   Espaçamento mediano %.0f m contra discordância até %.0f m: a célula de"
      % (np.median(esp),
         max(np.hypot(*(np.array(base[k]) - np.array(REC[n][k])))
             for n in ("v4", "v6", "por_linha") for k in base if k in REC[n])))
print("   uma válvula individual NAO e' um objecto resolvido, e nao se desenha.")
print("=" * 78)

json.dump(dict(discordancia_max_m=float(max(
    np.hypot(*(np.array(base[k]) - np.array(REC[n][k])))
    for n in ("v4", "v6", "por_linha") for k in base if k in REC[n])),
    espacamento_mediano_m=float(np.median(esp)),
    reconstrucoes=list(MAPAS),
    falsifica=falsifica,
    muda_pior_par_pct=float(pior_v),
    pior_par=list(pior_par),
    concordancia_total_pct=float(100 * estavel.sum() / BANDA.sum()),
    areas={n: {b: round(float((S == COD[b]).sum() * pix * pix / 1e4), 2)
               for b in ORDEM} for n, S in MAPAS.items()}),
    io.open(os.path.join(AQUI, "rega_multiverso.json"), "w", encoding="utf-8"),
    indent=1, ensure_ascii=False)
np.savez_compressed(os.path.join(AQUI, "rega_estavel.npz"),
                    estavel=estavel, **{n: S for n, S in MAPAS.items()})
print()
print("escritos rega_multiverso.json e rega_estavel.npz")
