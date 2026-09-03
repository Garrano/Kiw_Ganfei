# -*- coding: utf-8 -*-
"""Controlo 3 / REG-01 — carregador comum.

Reconstroi EXACTAMENTE o estado de `reg01_triagem_descontinuidade.py`:
mascaras a 30 m dos 37 blocos, mascaras dos dois focos, e a matriz
cena x unidade do NDVI Landsat a partir da cache local. Nada se descarrega.

Guarda um .npz para os testes seguintes nao repetirem a leitura.
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
OUT = os.path.join(VG, "_controlo3")
CACHE = os.path.join(OUT, "_matriz.npz")

ANOS = [str(a) for a in range(2017, 2027)]


def carregar():
    S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                       encoding="utf-8"))
    R = json.load(open(os.path.join(VG, "reg01_landsat.json"), encoding="utf-8"))
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
    M, GEOM = {}, {}
    for ft in KF:
        c = int(ft["properties"]["CUL_ID"])
        if c not in DEG_L:
            continue
        g = para(shape(ft["geometry"])).buffer(0)
        GEOM[c] = g
        M[c] = MP(np.array(list(g.exterior.coords))
                  ).contains_points(pts).reshape(NL, NC)

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
             "foco ORIENTAL": para30(ZONA0 & COM),
             "pomar inteiro": para30(POMAR)}
    return dict(M=M, GEOM=GEOM, FOCOS=FOCOS, ENT=ENT, HA=HA, DEG_L=DEG_L,
                BB=BB, NL=NL, NC=NC, POMAR=POMAR, ZONA0=ZONA0, COM=COM,
                E10=E10, N10=N10, para30=para30)


def matriz(D, refazer=False):
    """cena x unidade -> mediana do NDVI. NaN quando a cobertura nao chega.

    Reproduz o crivo do original: v.size >= max(3, 0.5*n_celulas).
    """
    if os.path.exists(CACHE) and not refazer:
        z = np.load(CACHE, allow_pickle=True)
        return (list(z["datas"]), list(z["unid"]), z["V"], z["PIX"])
    cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"),
                         encoding="utf-8"))
    fich = {}
    for x in os.listdir(C):
        fich.setdefault(x[:10], x)
    unid = sorted(D["M"]) + list(D["FOCOS"])
    masc = {**{c: D["M"][c] for c in D["M"]}, **D["FOCOS"]}
    datas, linhas, pixs = [], [], []
    for r in cen:
        fx = fich.get(r["data"])
        if not fx:
            continue
        nd = np.load(os.path.join(C, fx))["ndvi"]
        row, npx = [], []
        for u in unid:
            m = masc[u]
            v = nd[m]
            v = v[np.isfinite(v)]
            npx.append(v.size)
            row.append(float(np.median(v))
                       if v.size >= max(3, 0.5 * m.sum()) else np.nan)
        datas.append(r["data"])
        linhas.append(row)
        pixs.append(npx)
    V = np.array(linhas, float)
    PIX = np.array(pixs, int)
    np.savez_compressed(CACHE, datas=np.array(datas), unid=np.array(
        [str(u) for u in unid]), V=V, PIX=PIX)
    return datas, [str(u) for u in unid], V, PIX


def degraus(datas, unid, V, dentro, alvos=None):
    """Reproduz a REG-01 refeita: mediana regional por cena sobre `dentro`.

    Devolve {unidade: degrau} para `dentro` + `alvos`.
    """
    idx = {u: i for i, u in enumerate(unid)}
    D_i = [idx[u] for u in dentro]
    alvos = alvos or []
    pre = {u: [] for u in list(dentro) + list(alvos)}
    pos = {u: [] for u in list(dentro) + list(alvos)}
    for k, d in enumerate(datas):
        row = V[k]
        vals = row[D_i]
        ok = np.isfinite(vals)
        if ok.sum() < 0.7 * len(D_i):
            continue
        med = float(np.median(vals[ok]))
        tgt = pos if d >= "2025" else pre
        for u in list(dentro) + list(alvos):
            x = row[idx[u]]
            if np.isfinite(x):
                tgt[u].append(x - med)
    out = {}
    for u in list(dentro) + list(alvos):
        if len(pre[u]) >= 5 and len(pos[u]) >= 2:
            out[u] = float(np.mean(pos[u]) - np.mean(pre[u]))
    return out


def nivel_anual(datas, unid, V):
    idx = {u: i for i, u in enumerate(unid)}
    N = {u: {} for u in unid}
    for u in unid:
        for a in ANOS:
            v = [V[k, idx[u]] for k, d in enumerate(datas)
                 if d[:4] == a and np.isfinite(V[k, idx[u]])]
            N[u][a] = float(np.median(v)) if v else np.nan
    return N


if __name__ == "__main__":
    D = carregar()
    datas, unid, V, PIX = matriz(D, refazer=True)
    print("cenas: %d   unidades: %d" % (len(datas), len(unid)))
    print("celulas 30 m por unidade:")
    for u in unid:
        m = D["M"].get(int(u)) if u.isdigit() else D["FOCOS"][u]
        print("   %-16s n30 = %3d" % (u, m.sum()))
