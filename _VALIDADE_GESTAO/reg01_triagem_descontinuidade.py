# -*- coding: utf-8 -*-
"""Triagem: que blocos da REG-01 têm uma MUDANÇA DE USO dentro da linha de base?

O QUE FALHOU, E COMO SE SOUBE
------------------------------
A REG-01 definiu o degrau como

    média do desvio em 2025-26  −  média do desvio em 2017-2024

e pôs cinco blocos do ENT 297313 no fundo, −0,21 a −0,40, «duas a quatro vezes
piores do que os focos de Ganfei». A replicação em Landsat confirmou a ordenação
(ρ = +0,890) e eu escrevi que o facto tinha finalmente instrumento independente.

**A ordenação replicava porque os dois instrumentos estavam a medir a mesma
coisa errada.** A ortofoto de 2025 mostrou 14 a 44 % de cada um dos cinco sem
coberto, contra 0–2 % nos doze blocos do mesmo dono. E a série anual do Landsat
datou-a:

    ano     CINCO    DOZE
    2023    0,869    0,839
    2024    0,433    0,829     <- cai aqui, num ano
    2025    0,482    0,791
    2026    0,449    0,821

**O colapso é de 2024, e 2024 estava do lado PRÉ da minha fronteira.** Uma
mudança de uso a cavalo da fronteira dos períodos produz exactamente o degrau que
eu medi, sem que nada tenha declinado em 2025-26. E 0,43–0,48 não é copado em
sofrimento: é solo com vegetação esparsa.

É precisamente a ressalva que a guarda de cultura escreve — a declaração do IFAP
cobre uma campanha, e **a continuidade da cultura ao longo da linha de base não
está verificada.** Estava escrita no código e eu publiquei o resultado à mesma.

O QUE ESTE FICHEIRO FAZ
-----------------------
Deixa de confiar na fronteira dos períodos e olha para a **forma da série**. Para
cada bloco, com as cenas de Verão do Landsat, ano a ano:

    · nível de cada ano;
    · maior queda entre dois anos CONSECUTIVOS dentro de 2017-2024;
    · se o nível pós-queda fica no domínio de solo (< 0,60).

CRITÉRIO DE EXCLUSÃO, fixado antes de correr
---------------------------------------------
    X1 · queda >= 0,25 entre dois anos consecutivos **dentro de 2017-2024**, e
    X2 · nível médio depois da queda < 0,60,
    -> o bloco NÃO é uma unidade válida para a REG-01: a sua linha de base não é
       a mesma cultura. Sai, e diz-se qual e porquê. Não se corrige, não se
       reconcilia, não se pondera.

    O limiar 0,60 vem da série NU21 já certificada neste caso: solo lavrado neste
    tipo de parcela lê 0,49 a 0,61. Não é um limiar inventado agora.

E DEPOIS
--------
Recalcula-se a REG-01 só com os blocos que sobrevivem, e vê-se onde caem os
focos de Ganfei. **Se o resultado mudar de lado, muda — não se procura maneira
de o manter.**
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
S2D = r"C:\Users\Jackster2\Downloads\ganfei_s2"
C = os.path.join(VG, "_reg01_landsat_cache")
QUEDA_MIN, CHAO = 0.25, 0.60

S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                   encoding="utf-8"))
R = json.load(open(os.path.join(VG, "reg01_landsat.json"), encoding="utf-8"))
DEG_S2 = {int(b["cul"]): b["degrau"] for b in S["blocos"]}
DEG_L = {int(k): v for k, v in R["degrau_landsat_ndvi"].items()}
ENT = {int(k): v for k, v in R["ent"].items()}
HA = {int(k): v for k, v in R["ha"].items()}

bl = S["blocos"]
xs = [b["E"] for b in bl]
ys = [b["N"] for b in bl]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)
NC, NL = int((BB[2] - BB[0]) / 30), int((BB[3] - BB[1]) / 30)
EE, NN = np.meshgrid(BB[0] + (np.arange(NC) + .5) * 30.,
                     BB[3] - (np.arange(NL) + .5) * 30.)
pts = np.column_stack([EE.ravel(), NN.ravel()])

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
M = {}
for ft in KF:
    c = int(ft["properties"]["CUL_ID"])
    if c not in DEG_L:
        continue
    g = para(shape(ft["geometry"])).buffer(0)
    M[c] = MP(np.array(list(g.exterior.coords))
              ).contains_points(pts).reshape(NL, NC)
print("blocos a triar: %d" % len(M))

# ---- os dois focos de Ganfei, nas mesmas cenas e na mesma grelha
g = json.load(open(os.path.join(S2D, "sentinel", "masks_geograficas.json")))
b10 = lambda k: np.array([[ch == "1" for ch in L] for L in g[k]], bool)
POMAR, ZONA0 = b10("pomar_bits"), b10("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
AOI = (529950, 4654600, 531950, 4655600)
E10, N10 = np.meshgrid(AOI[0] + (np.arange(200) + .5) * 10.,
                       AOI[3] - (np.arange(100) + .5) * 10.)


def para30(m10, cob=5):
    cnt = np.zeros((NL, NC), int)
    ii = ((BB[3] - N10[m10]) / 30).astype(int)
    jj = ((E10[m10] - BB[0]) / 30).astype(int)
    k = (ii >= 0) & (ii < NL) & (jj >= 0) & (jj < NC)
    np.add.at(cnt, (ii[k], jj[k]), 1)
    return cnt >= cob


FOCOS = {"foco OCIDENTAL": para30((np.hypot(E10 - 530485., N10 - 4655053.) <= 90)
                                  & POMAR & COM),
         "foco ORIENTAL": para30(ZONA0 & COM)}

cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"),
                     encoding="utf-8"))
fich = {}
for x in os.listdir(C):
    fich.setdefault(x[:10], x)

ANOS = [str(a) for a in range(2017, 2027)]
serie = {c: {a: [] for a in ANOS} for c in list(M) + list(FOCOS)}
med_ano = {a: [] for a in ANOS}
for r in cen:
    fx = fich.get(r["data"])
    if not fx:
        continue
    nd = np.load(os.path.join(C, fx))["ndvi"]
    a = r["data"][:4]
    vals = {}
    for c, m in M.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * m.sum()):
            vals[c] = float(np.median(v))
    if len(vals) < 0.7 * len(M):
        continue
    med_ano[a].append(float(np.median(list(vals.values()))))
    for c, v in vals.items():
        serie[c][a].append(v)
    for nome, m in FOCOS.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * m.sum()):
            serie[nome][a].append(float(np.median(v)))

NIV = {c: {a: (float(np.median(v)) if v else np.nan)
           for a, v in d.items()} for c, d in serie.items()}
MEDR = {a: (float(np.median(v)) if v else np.nan) for a, v in med_ano.items()}

print()
print("=" * 104)
print("TRIAGEM — queda >= %.2f entre anos consecutivos DENTRO de 2017-2024, e nivel depois < %.2f"
      % (QUEDA_MIN, CHAO))
print("=" * 104)
print()
print("%-10s %7s %7s %s  %s" % ("CUL_ID", "ENT", "ha",
                                " ".join("%6s" % a for a in ANOS), "veredicto"))
FORA, DENTRO = [], []
for c in sorted(M, key=lambda z: DEG_L[z]):
    n = [NIV[c][a] for a in ANOS]
    pior, ondes = 0.0, None
    for i in range(len(ANOS) - 1):
        if ANOS[i + 1] > "2024":
            break
        if np.isfinite(n[i]) and np.isfinite(n[i + 1]):
            d = n[i] - n[i + 1]
            if d > pior:
                pior, ondes = d, ANOS[i + 1]
    depois = np.nan
    if ondes:
        k = ANOS.index(ondes)
        v = [x for x in n[k:] if np.isfinite(x)]
        depois = float(np.mean(v)) if v else np.nan
    exclui = pior >= QUEDA_MIN and np.isfinite(depois) and depois < CHAO
    (FORA if exclui else DENTRO).append(c)
    print("%-10d %7s %7.2f %s  %s"
          % (c, ENT[c], HA[c],
             " ".join("     ." if not np.isfinite(x) else "%6.3f" % x for x in n),
             "FORA — cai %.2f em %s, fica em %.2f" % (pior, ondes, depois)
             if exclui else ""))

print()
print("excluidos: %d   ·   ficam: %d" % (len(FORA), len(DENTRO)))
print("os excluidos: %s" % ", ".join("%d (ENT %s)" % (c, ENT[c]) for c in FORA))

# ------------------------------------------- REG-01 refeita, so com os validos
print()
print("=" * 104)
print("REG-01 REFEITA — so com os blocos de linha de base continua")
print("=" * 104)
dev = {c: {"pre": [], "pos": []} for c in DENTRO + list(FOCOS)}
for r in cen:
    fx = fich.get(r["data"])
    if not fx:
        continue
    nd = np.load(os.path.join(C, fx))["ndvi"]
    vals = {}
    for c in DENTRO:
        v = nd[M[c]]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * M[c].sum()):
            vals[c] = float(np.median(v))
    if len(vals) < 0.7 * len(DENTRO):
        continue
    med = float(np.median(list(vals.values())))
    alvo = "pos" if r["data"] >= "2025" else "pre"
    for c, v in vals.items():
        dev[c][alvo].append(v - med)
    for nome, m in FOCOS.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * m.sum()):
            dev[nome][alvo].append(float(np.median(v)) - med)

DEG = {}
for c, d in dev.items():
    if len(d["pre"]) >= 5 and len(d["pos"]) >= 2:
        DEG[c] = float(np.mean(d["pos"]) - np.mean(d["pre"]))
blocos = {c: v for c, v in DEG.items() if c in DENTRO}
arr = np.array(sorted(blocos.values()))
print()
print("%-16s %11s %11s" % ("", "degrau", "percentil"))
for c in sorted(blocos, key=lambda z: blocos[z])[:6]:
    print("%-16d %+11.4f %10.0f %%"
          % (c, blocos[c], 100 * np.mean(arr <= blocos[c])))
print("   ...")
print()
for nome in FOCOS:
    if nome in DEG:
        p = 100 * np.mean(arr <= DEG[nome])
        print("%-16s %+11.4f %10.0f %%   <-- Ganfei   %s"
              % (nome, DEG[nome], p,
                 "ACIMA do percentil 10" if p > 10 else "NA CAUDA EXTREMA"))

json.dump(dict(excluidos=FORA, mantidos=DENTRO,
               nivel_anual={str(k): v for k, v in NIV.items()},
               mediana_regional_anual=MEDR, degrau_refeito=DEG),
          open(os.path.join(VG, "reg01_triagem.json"), "w"), indent=1)
print()
print("escrito reg01_triagem.json")
