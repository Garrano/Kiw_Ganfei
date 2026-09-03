# -*- coding: utf-8 -*-
"""REG-01 · LANDSAT · R3 — onde caem os dois focos de Ganfei, no outro instrumento.

O R1 e o R2 correram em `reg01_landsat.py` e replicaram. Falta o R3, que é o
critério sobre Ganfei, e falta porque exige duas coisas que o ficheiro anterior
não guardou: a **mediana regional por cena** e as máscaras dos focos na grelha
de 30 m.

O N DOS FOCOS, E PORQUE A PRIMEIRA CONTAGEM ESTAVA ERRADA
----------------------------------------------------------
A primeira tentativa marcava uma célula de 30 m se **qualquer** célula de 10 m
do foco lhe caísse dentro. Isso dá 33 e 18 células para focos de 2,18 e 0,76 ha
— ou seja 2,97 e 1,62 ha, mais área do que os focos têm. Inflaciona o n e
mistura vizinhança com foco.

Aqui exige-se **cobertura >= 5 das 9 células de 10 m**. É a regra que o
`landsat_independente.py` prometia no cabeçalho e nunca cumpriu.

O foco oriental tem 0,76 ha = oito células de 30 m no melhor dos casos. **Se
sobrarem menos de cinco, o R3 não se julga para ele: escreve-se que o
instrumento não o resolve.** Declarado antes de correr.
"""
import json
import os

import numpy as np

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
S2D = r"C:\Users\Jackster2\Downloads\ganfei_s2"
C = os.path.join(VG, "_reg01_landsat_cache")
N_MIN_FOCO = 5

S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                   encoding="utf-8"))
R = json.load(open(os.path.join(VG, "reg01_landsat.json"), encoding="utf-8"))
DEG_L = {int(k): v for k, v in R["degrau_landsat_ndvi"].items()}
DEG_LM = {int(k): v for k, v in R["degrau_landsat_ndmi"].items()}

bl = S["blocos"]
xs = [b["E"] for b in bl]
ys = [b["N"] for b in bl]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)
NC = int((BB[2] - BB[0]) / 30)
NL = int((BB[3] - BB[1]) / 30)

# --------------------------------- as máscaras dos blocos, refeitas a 30 m
from shapely.geometry import shape
from shapely.ops import transform as sht
from pyproj import Transformer
from matplotlib.path import Path as MP

H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para_utm = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K

# --- guarda de cultura -------------------------------------------------------
# Este script confia no NOME do ficheiro para saber que os blocos sao kiwi. O
# filtro real vive noutro sitio (SAIDA_H2_patologista/03_ifap_largo.py, linha
# `PUN_CUL_COD != "124" -> salta`). Se esse ficheiro for regerado com outro
# filtro, nada aqui daria por isso -- e o mesmo modo de falha do cabecalho de
# `fazer_masks_v2.py`. Verifica-se o codigo declarado, poligono a poligono.
_maus = sorted({str(f["properties"].get("PUN_CUL_COD")) for f in KF} - {"124"})
if _maus:
    raise SystemExit(
        "ifap_kiwi_largo.json contem culturas nao-kiwi: %s. Esperado so "
        "PUN_CUL_COD 124 (KIWI). Regerar com 03_ifap_largo.py." % ", ".join(_maus))
_camp = sorted({str(f["properties"].get("CUL_CAMPANHA")) for f in KF})
print("guarda de cultura: %d poligonos, todos PUN_CUL_COD 124 (KIWI), "
      "campanha(s) %s" % (len(KF), "/".join(_camp)))
print("  RESSALVA: a declaracao do IFAP cobre so a(s) campanha(s) acima. A "
      "continuidade da cultura ao longo da linha de base NAO esta verificada;")
print("  um bloco arrancado ou replantado a meio da serie produz um degrau que "
      "nao e sintoma. Ver REGISTO_REG01_GUARDA_2026-09-01.md.")

EE, NN = np.meshgrid(BB[0] + (np.arange(NC) + .5) * 30.,
                     BB[3] - (np.arange(NL) + .5) * 30.)
pts = np.column_stack([EE.ravel(), NN.ravel()])
MB = {}
for ft in KF:
    cul = ft["properties"].get("CUL_ID")
    if cul is None or int(cul) not in DEG_L:
        continue
    g = para_utm(shape(ft["geometry"])).buffer(0)
    m = MP(np.array(list(g.exterior.coords))).contains_points(pts).reshape(NL, NC)
    if m.sum():
        MB[int(cul)] = m
print("blocos com mascara a 30 m: %d" % len(MB))

# ------------------------------------ os focos, com cobertura >= 5 de 9
g = json.load(open(os.path.join(S2D, "sentinel", "masks_geograficas.json")))
b10 = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, ZONA0 = b10("pomar_bits"), b10("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
AOI = (529950, 4654600, 531950, 4655600)
E10, N10 = np.meshgrid(AOI[0] + (np.arange(200) + .5) * 10.,
                       AOI[3] - (np.arange(100) + .5) * 10.)
DOC = (np.hypot(E10 - 530485., N10 - 4655053.) <= 90) & POMAR & COM
DOR = ZONA0 & COM


def para30(m10, cobertura=5):
    cnt = np.zeros((NL, NC), int)
    ii = ((BB[3] - N10[m10]) / 30).astype(int)
    jj = ((E10[m10] - BB[0]) / 30).astype(int)
    k = (ii >= 0) & (ii < NL) & (jj >= 0) & (jj < NC)
    np.add.at(cnt, (ii[k], jj[k]), 1)
    return cnt >= cobertura


UN = [("foco OCIDENTAL", DOC, 2.18), ("foco ORIENTAL", DOR, 0.76),
      ("pomar inteiro", POMAR, 30.31)]
MF = {}
print()
for nome, m10, ha in UN:
    m = para30(m10)
    MF[nome] = m
    print("%-16s %5.2f ha  ->  n30 = %3d celulas (cobertura >= 5/9)  = %.2f ha"
          % (nome, ha, m.sum(), m.sum() * 0.09))

# ------------------------------------------------------- percorrer as cenas
cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"),
                     encoding="utf-8"))
fich = {}
for f in os.listdir(C):
    fich.setdefault(f[:10], f)

dev = {n: {"pre": [], "pos": []} for n, _, _ in UN}
devM = {n: {"pre": [], "pos": []} for n, _, _ in UN}
nc = 0
for r in cen:
    f = fich.get(r["data"])
    if not f:
        continue
    z = np.load(os.path.join(C, f))
    nd, nm = z["ndvi"], z["ndmi"]
    vb = [np.nanmedian(nd[m]) for m in MB.values()]
    wb = [np.nanmedian(nm[m]) for m in MB.values()]
    med_v = float(np.nanmedian(vb))
    med_w = float(np.nanmedian(wb))
    if not np.isfinite(med_v):
        continue
    nc += 1
    alvo = "pos" if r["data"] >= "2025" else "pre"
    for nome, _, _ in UN:
        m = MF[nome]
        for arr, med, d in ((nd, med_v, dev), (nm, med_w, devM)):
            a = arr[m]
            a = a[np.isfinite(a)]
            if a.size >= max(3, 0.5 * m.sum()):
                d[nome][alvo].append(float(np.median(a)) - med)

print()
print("cenas usadas: %d   (2017-24: %d · 2025-26: %d)"
      % (nc, len(dev["pomar inteiro"]["pre"]), len(dev["pomar inteiro"]["pos"])))

ordem = sorted(DEG_L, key=lambda c: DEG_L[c])
degraus = np.array([DEG_L[c] for c in ordem])
degM = np.array([DEG_LM[c] for c in ordem])

print()
print("=" * 92)
print("R3 · onde caem os focos de Ganfei na distribuicao regional do LANDSAT")
print("=" * 92)
print()
print("%-16s %5s %11s %11s %11s %11s"
      % ("", "n30", "degrau L", "percentil", "degrau S2", "pct S2"))
S2FOCOS = {"foco OCIDENTAL": -0.1060, "foco ORIENTAL": -0.1008,
           "pomar inteiro": -0.0102}
S2PCT = {"foco OCIDENTAL": 13, "foco ORIENTAL": 13, "pomar inteiro": 37}
res = {}
for nome, _, _ in UN:
    n30 = int(MF[nome].sum())
    d = dev[nome]
    if len(d["pre"]) < 5 or len(d["pos"]) < 2 or n30 < N_MIN_FOCO:
        print("%-16s %5d   INSTRUMENTO NAO RESOLVE (n30 < %d ou cenas a menos)"
              % (nome, n30, N_MIN_FOCO))
        continue
    deg = float(np.mean(d["pos"]) - np.mean(d["pre"]))
    pct = 100.0 * np.mean(degraus <= deg)
    res[nome] = (deg, pct, n30)
    print("%-16s %5d %+11.4f %10.0f %% %+11.4f %10d %%"
          % (nome, n30, deg, pct, S2FOCOS[nome], S2PCT[nome]))

print()
print("veredicto do R3 (criterio a priori: acima do percentil 10):")
for nome, (deg, pct, n30) in res.items():
    print("   %-16s percentil %.0f %%  ->  %s"
          % (nome, pct, "acima de 10 — a conclusao do S2 mantem-se"
             if pct > 10 else "NA CAUDA EXTREMA — contradiz o S2"))

# ----------------------------------------------------- NDMI, o extra
print()
print("=" * 92)
print("EXTRA · NDMI — agua no copado. NAO faz parte dos criterios pre-registados.")
print("=" * 92)
print()
print("os cinco do 297313, em NDMI:")
CINCO = [6705427, 6705429, 6705428, 6705432, 6705442]
ordM = sorted(DEG_LM, key=lambda c: DEG_LM[c])
posM = {c: i for i, c in enumerate(ordM)}
for c in CINCO:
    print("   %d  degrau NDMI %+.4f   lugar %d de %d"
          % (c, DEG_LM[c], posM[c] + 1, len(ordM)))
for nome, _, _ in UN:
    d = devM[nome]
    if len(d["pre"]) >= 5 and len(d["pos"]) >= 2:
        deg = float(np.mean(d["pos"]) - np.mean(d["pre"]))
        pct = 100.0 * np.mean(degM <= deg)
        print("   %-16s degrau NDMI %+.4f   percentil %.0f %%" % (nome, deg, pct))

json.dump(dict(focos={k: dict(degrau=v[0], percentil=v[1], n30=v[2])
                      for k, v in res.items()}, n_cenas=nc),
          open(os.path.join(VG, "reg01_landsat_r3.json"), "w"), indent=1)
print()
print("escrito reg01_landsat_r3.json")
