# -*- coding: utf-8 -*-
"""Controlo 3 sobre o B1 — modulo comum.

Reconstroi de raiz, a partir da cache Landsat regional (100 cenas), a matriz
cena x unidade para:
  · os 37 blocos do IFAP da REG-01 (para saber quais sao os 29 mantidos);
  · as 6 parcelas do sector B1;
  · os dois focos de Ganfei (mesma definicao de `reg01_triagem_descontinuidade`).

Nao escreve nada fora de `_controlo3_b1\\`.
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
OUT = os.path.join(VG, "_controlo3_b1")
CL = os.path.join(VG, "_reg01_landsat_cache")
CUL_B1 = [6476415, 8845729, 6476420, 8845739, 8845740, 6476425]
ANOS = [str(a) for a in range(2017, 2027)]


def _carrega():
    S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                       encoding="utf-8"))
    R = json.load(open(os.path.join(VG, "reg01_landsat.json"), encoding="utf-8"))
    T = json.load(open(os.path.join(VG, "reg01_triagem.json"), encoding="utf-8"))
    return S, R, T


S, R, T = _carrega()
DEG_L = {int(k): v for k, v in R["degrau_landsat_ndvi"].items()}
ENT = {int(k): v for k, v in R["ent"].items()}
HA = {int(k): v for k, v in R["ha"].items()}
MANTIDOS = [int(x) for x in T["mantidos"]]
EXCLUIDOS = [int(x) for x in T["excluidos"]]

bl = S["blocos"]
BB = (min(b["E"] for b in bl) - 400, min(b["N"] for b in bl) - 400,
      max(b["E"] for b in bl) + 400, max(b["N"] for b in bl) + 400)
NC, NL = int((BB[2] - BB[0]) / 30), int((BB[3] - BB[1]) / 30)
EE, NN = np.meshgrid(BB[0] + (np.arange(NC) + .5) * 30.,
                     BB[3] - (np.arange(NL) + .5) * 30.)
PTS = np.column_stack([EE.ravel(), NN.ravel()])

_tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: _tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K

GEO = {}
for ft in KF:
    c = int(ft["properties"]["CUL_ID"])
    if c in DEG_L or c in CUL_B1:
        GEO[c] = para(shape(ft["geometry"])).buffer(0)

M = {c: MP(np.array(list(g.exterior.coords))).contains_points(PTS
                                                              ).reshape(NL, NC)
     for c, g in GEO.items()}

# ---- os dois focos, copiado literalmente de reg01_triagem_descontinuidade.py
_g = json.load(open(os.path.join(S2D, "sentinel", "masks_geograficas.json")))
_b10 = lambda k: np.array([[ch == "1" for ch in L] for L in _g[k]], bool)
POMAR, ZONA0 = _b10("pomar_bits"), _b10("zona0_bits")
_h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(_h) & (_h >= 0.5)
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

CENAS = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"),
                       encoding="utf-8"))
_fich = {}
for x in os.listdir(CL):
    _fich.setdefault(x[:10], x)


def matriz():
    """Devolve (datas, valores) com valores[unidade] = lista alinhada a datas.

    Uma unidade sem cobertura suficiente numa cena entra como NaN.
    """
    uni = list(M) + list(FOCOS)
    datas, val = [], {u: [] for u in uni}
    for r in CENAS:
        fx = _fich.get(r["data"])
        if not fx:
            continue
        nd = np.load(os.path.join(CL, fx))["ndvi"]
        linha = {}
        for c, m in M.items():
            v = nd[m]
            v = v[np.isfinite(v)]
            linha[c] = float(np.median(v)) if v.size >= max(3, .5 * m.sum()) else np.nan
        for nome, m in FOCOS.items():
            v = nd[m]
            v = v[np.isfinite(v)]
            linha[nome] = float(np.median(v)) if v.size >= max(3, .5 * m.sum()) else np.nan
        datas.append(r["data"])
        for u in uni:
            val[u].append(linha[u])
    return np.array(datas), {u: np.array(v, float) for u, v in val.items()}


def anual(datas, s):
    a = np.array([d[:4] for d in datas])
    return np.array([np.nanmedian(s[a == y]) if np.isfinite(s[a == y]).any()
                     else np.nan for y in ANOS])


if __name__ == "__main__":
    d, V = matriz()
    print("cenas lidas: %d" % len(d))
    print("unidades: %d blocos IFAP (%d da REG-01, %d do B1) + %d focos"
          % (len(M), len(DEG_L), len(CUL_B1), len(FOCOS)))
    for c in CUL_B1:
        print("  B1 %-8d n30=%3d ha=%5.2f  %s"
              % (c, M[c].sum(), GEO[c].area / 1e4,
                 " ".join("%5.3f" % x if np.isfinite(x) else "  .  "
                          for x in anual(d, V[c]))))
