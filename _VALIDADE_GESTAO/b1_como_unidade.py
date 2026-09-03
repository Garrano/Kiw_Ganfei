# -*- coding: utf-8 -*-
"""O B1 medido como unidade — o sector que nunca entrou em análise nenhuma.

PORQUE ISTO FALTAVA, E NÃO ERA DISTRACÇÃO
------------------------------------------
O sector B1 — E 529 495–530 063 · N 4 653 832–4 654 477, = C1a + C1b, **12,63 ha
de kiwi declarado do MESMO dono** — foi localizado a 28-08-2026 por duas
coordenadas dadas pelo gestor (testemunho de tipo 1). Desde então apareceu na
`LISTA_FINAL` como **C3** («o bloco sudoeste é da mesma exploração») e na fila
como acção 4, e **nunca foi medido**.

A razão é estrutural: a AOI de 2 × 1 km em que tudo o resto foi calculado
começa em N 4 654 600, e o B1 acaba em N 4 654 477. **Fica 123 m a sul e 455 m a
oeste do canto.** Toda a análise construída sobre as máscaras herdou essa
fronteira sem a declarar.

Não confundir com a AOI `b1` (528400–529400, 4654900–4655700), que media tecido
urbano de Valença do outro lado do Minho e foi retirada com 49 ficheiros em
quarentena. **São duas coisas diferentes com o mesmo nome.**

PORQUE É QUE ISTO DECIDE ALGUMA COISA
--------------------------------------
A C3 certifica que **não existe controlo externo contemporâneo de kiwi** neste
caso — e certifica-o *precisamente porque* C1a e C1b, que tinham sido propostos
como controlo externo, se revelaram ser o B1, da mesma exploração.

Mas «mesma exploração» não é «mesmo sítio». O B1 está a **meio quilómetro** do
corpo principal, noutro terreno. Se ele **não** tiver o degrau, é o comparador
mais próximo que este caso possui — dentro da mesma gestão e da mesma água, o
que exclui exactamente as explicações que um controlo externo não excluiria. Se
ele **tiver** o degrau, o acontecimento não está confinado às duas zonas, e a
frase central do caso muda.

HIPÓTESE E CRITÉRIO, FIXADOS ANTES DE CORRER
---------------------------------------------
    H1 · o B1 não tem o degrau de 2025-26.
    H0 · tem-no, em grau comparável ao dos focos.

    CRITÉRIO: o degrau mediano das parcelas do B1 com linha de base contínua,
    contra os dois focos (−0,084 e −0,087, na moeda da REG-01):
      · se |degrau B1| < 1/3 do degrau dos focos  -> H1, e o B1 é comparador;
      · se > 2/3  -> H0, e o acontecimento é mais largo do que duas zonas;
      · entre 1/3 e 2/3 -> NÃO DECIDE, e diz-se.

A CONDIÇÃO 5 APLICA-SE AQUI COM FORÇA
--------------------------------------
Sabe-se de antemão que **parte do B1 é plantação nova**: o Controlo 3 foi à
ortofoto da DGT e verificou que 8845729, 8845731 e 8845739 são campo aberto em
2012, 2018 **e** 2021, com pérgola nova em 2025. Uma parcela sem cultura na
linha de base **não é comparador, é ruído** — e entra aqui a mesma triagem de
descontinuidade que retirou o A3.

O INSTRUMENTO, e o que ele não é
---------------------------------
Landsat 8/9 (100 cenas, cache regional já em disco) **e** Sentinel-2 (9 cenas,
cache regional). O B1 cabe na janela regional das duas, ao contrário da AOI de
Ganfei. Não se descarrega nada.

Isto **não** é instrumento independente para o sinal: é óptico dos dois lados.
O que é independente são as **fronteiras** — os polígonos do IFAP, de outra
entidade — e a **localização**, que veio do gestor e não de nenhum cálculo
nosso.
"""
import json
import os

import numpy as np
from matplotlib.path import Path as MP
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CL = os.path.join(VG, "_reg01_landsat_cache")
CS = os.path.join(VG, "_reg01_cache")
CUL_B1 = [6476415, 8845729, 6476420, 8845739, 8845740, 6476425]
QUEDA_MIN, CHAO = 0.25, 0.60
FOCOS = {"foco OCIDENTAL": -0.0839, "foco ORIENTAL": -0.0869}

S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                   encoding="utf-8"))
bl = S["blocos"]
xs = [b["E"] for b in bl]
ys = [b["N"] for b in bl]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
mau = sorted({str(f["properties"].get("PUN_CUL_COD")) for f in KF} - {"124"})
if mau:
    raise SystemExit("ifap_kiwi_largo.json tem culturas nao-kiwi: %s" % mau)

GEO = {}
for ft in KF:
    c = int(ft["properties"]["CUL_ID"])
    if c in CUL_B1:
        GEO[c] = para(shape(ft["geometry"])).buffer(0)
print("parcelas do B1: %d  ·  %.2f ha de kiwi declarado"
      % (len(GEO), sum(g.area / 1e4 for g in GEO.values())))


def malha(passo):
    nc = int((BB[2] - BB[0]) / passo)
    nl = int((BB[3] - BB[1]) / passo)
    E, N = np.meshgrid(BB[0] + (np.arange(nc) + .5) * passo,
                       BB[3] - (np.arange(nl) + .5) * passo)
    return nc, nl, np.column_stack([E.ravel(), N.ravel()])


def mascaras(passo):
    nc, nl, pts = malha(passo)
    M = {}
    for c, g in GEO.items():
        m = MP(np.array(list(g.exterior.coords))).contains_points(pts)
        M[c] = m.reshape(nl, nc)
    return M


M30 = mascaras(30.0)
M10 = mascaras(10.0)
print("celulas por parcela: 30 m %s"
      % "  ".join("%d:%d" % (c, M30[c].sum()) for c in CUL_B1))

# ─────────────────────────────────────────── nivel anual, e a triagem
cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"),
                     encoding="utf-8"))
fich = {}
for f in os.listdir(CL):
    fich.setdefault(f[:10], f)
ANOS = [str(a) for a in range(2017, 2027)]
serie = {c: {a: [] for a in ANOS} for c in CUL_B1}
med_reg = {a: [] for a in ANOS}
TR = json.load(open(os.path.join(VG, "reg01_triagem.json"), encoding="utf-8"))
MANTIDOS = [int(x) for x in TR["mantidos"]]
Mreg = mascaras.__self__ if False else None
# mediana regional: reusa os blocos mantidos da REG-01, mesma definicao
regm = {}
_nc, _nl, _pts = malha(30.0)
for ft in KF:
    c = int(ft["properties"]["CUL_ID"])
    if c in MANTIDOS:
        g = para(shape(ft["geometry"])).buffer(0)
        regm[c] = MP(np.array(list(g.exterior.coords))
                     ).contains_points(_pts).reshape(_nl, _nc)

dev = {c: {"pre": [], "pos": []} for c in CUL_B1}
for r in cen:
    f = fich.get(r["data"])
    if not f:
        continue
    nd = np.load(os.path.join(CL, f))["ndvi"]
    vals = [np.nanmedian(nd[m]) for m in regm.values()]
    med = float(np.nanmedian([v for v in vals if np.isfinite(v)]))
    if not np.isfinite(med):
        continue
    a = r["data"][:4]
    med_reg[a].append(med)
    alvo = "pos" if r["data"] >= "2025" else "pre"
    for c in CUL_B1:
        v = nd[M30[c]]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * M30[c].sum()):
            x = float(np.median(v))
            serie[c][a].append(x)
            dev[c][alvo].append(x - med)

NIV = {c: np.array([np.median(serie[c][a]) if serie[c][a] else np.nan
                    for a in ANOS]) for c in CUL_B1}

print()
print("=" * 100)
print("NIVEL ANUAL das parcelas do B1 (Landsat, mediana das cenas de Verao)")
print("=" * 100)
print()
print("%-10s %6s %s  %s" % ("CUL_ID", "n30", " ".join("%6s" % a for a in ANOS),
                            "triagem"))
VALIDOS = []
for c in CUL_B1:
    v = NIV[c]
    k = ANOS.index("2024")
    d = np.diff(v[:k + 1])
    ok = np.isfinite(d)
    fora, pior, onde = False, 0.0, None
    if ok.sum() >= 3:
        for i in range(len(d)):
            if ok[i] and -d[i] > pior:
                pior, onde = -d[i], ANOS[i + 1]
        if onde:
            j = ANOS.index(onde)
            dep = [x for x in v[j:] if np.isfinite(x)]
            fora = pior >= QUEDA_MIN and dep and float(np.mean(dep)) < CHAO
    base = [x for x in v[:ANOS.index("2024") + 1] if np.isfinite(x)]
    jovem = bool(base) and float(np.mean(base)) < CHAO
    if not fora and not jovem:
        VALIDOS.append(c)
    print("%-10d %6d %s  %s"
          % (c, M30[c].sum(),
             " ".join("     ." if not np.isfinite(x) else "%6.3f" % x for x in v),
             "FORA — cai %.2f em %s" % (pior, onde) if fora
             else ("FORA — base media %.2f < %.2f (plantacao nova)"
                   % (float(np.mean(base)), CHAO) if jovem else "fica")))

print()
print("parcelas com linha de base continua: %d de %d  ->  %s"
      % (len(VALIDOS), len(CUL_B1), VALIDOS or "nenhuma"))

# ─────────────────────────────────────────── o degrau, e o criterio
print()
print("=" * 100)
print("O DEGRAU DO B1, na moeda da REG-01 (desvio a mediana regional)")
print("=" * 100)
print()
DEG = {}
for c in CUL_B1:
    d = dev[c]
    if len(d["pre"]) >= 5 and len(d["pos"]) >= 2:
        DEG[c] = float(np.mean(d["pos"]) - np.mean(d["pre"]))
        print("%-10d %s  degrau %+.4f  (pre %d cenas, pos %d)"
              % (c, "VALIDA " if c in VALIDOS else "excluida",
                 DEG[c], len(d["pre"]), len(d["pos"])))

dv = [DEG[c] for c in VALIDOS if c in DEG]
print()
if not dv:
    print("Nenhuma parcela valida com serie suficiente. O B1 NAO E TESTAVEL")
    print("com este instrumento, e diz-se em vez de se inventar.")
    raise SystemExit(0)

med_b1 = float(np.median(dv))
alvo = float(np.mean(list(FOCOS.values())))
# CORRIGIDO: a primeira versao era `abs(med_b1)/abs(alvo)`, e por isso um
# degrau POSITIVO da mesma magnitude disparava «H0 · o B1 TEM o degrau».
# Um criterio que nao distingue melhoria de declinio nao e um criterio.
# Agora a razao so e comparavel quando o SINAL coincide.
mesmo_sinal = (med_b1 < 0) == (alvo < 0)
razao = (abs(med_b1) / abs(alvo)) if mesmo_sinal else 0.0
print("degrau mediano do B1 valido : %+.4f  (n = %d parcelas)" % (med_b1, len(dv)))
print("degrau medio dos dois focos : %+.4f" % alvo)
print("razao |B1| / |focos|        : %.2f" % razao)
print()
if not mesmo_sinal:
    ver = ("H1, e por margem larga: o B1 nao so nao desce como SOBE (%+.4f) "
           "enquanto os focos descem (%+.4f). Sinais opostos." % (med_b1, alvo))
elif razao < 1 / 3.0:
    ver = ("H1 · o B1 NAO tem o degrau. E o comparador mais proximo que este "
           "caso possui — mesma gestao, mesma agua, meio quilometro de "
           "distancia.")
elif razao > 2 / 3.0:
    ver = ("H0 · o B1 TEM o degrau. O acontecimento nao esta confinado as duas "
           "zonas, e a frase central do caso muda.")
else:
    ver = ("NAO DECIDE. A razao cai entre 1/3 e 2/3, que foi declarado antes de "
           "correr como zona onde nao se conclui.")
print("VEREDICTO: %s" % ver)

json.dump(dict(cul_b1=CUL_B1, validos=VALIDOS, degrau=DEG,
               nivel_anual={str(c): [None if not np.isfinite(x) else float(x)
                                     for x in NIV[c]] for c in CUL_B1},
               anos=ANOS, degrau_mediano_b1=med_b1, degrau_focos=alvo,
               razao=razao, veredicto=ver),
          open(os.path.join(VG, "b1_como_unidade.json"), "w"), indent=1)
print()
print("escrito b1_como_unidade.json")
