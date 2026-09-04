# -*- coding: utf-8 -*-
"""Georreferenciar o esquema BLOCO A BLOCO, com a escala declarada como âncora.

O QUE JÁ SE SABE, E QUE ESTE FICHEIRO USA
------------------------------------------
1. **A escala é 1:3500 em A1** — testemunho do gestor. Num scan de 2338 px isso
   dá **1,259 m/px**. É um número previsto, não ajustado, e serve de controlo.
2. A banda contígua, medida entre dois pontos escolhidos por forma, dá **1,263
   m/px** — 0,3 % da declarada. **O desenho está à escala.**
3. Mas o **lobo do B1 está desenhado deslocado** em relação à banda: com a
   transformação da banda, as válvulas do lobo caem 155 a 379 m fora. É o que
   um desenhador faz para meter um lobo distante e 1,5 km de banda numa folha.

PORQUE ISTO PODE CORRER BEM ONDE AS TRÊS TENTATIVAS ANTERIORES FALHARAM
------------------------------------------------------------------------
Um ICP global falhou (RMS 70,3 m) porque **arrancava de lado nenhum** e com uma
segmentação que via 8 de 13 bandas. Aqui o ICP arranca de uma semelhança já
correcta a 0,3 % na escala, é **restringido a uma semelhança** (não deixa a
escala fugir), corre **por bloco**, e só empareja pontos a menos de 120 m.

Um ICP local bem inicializado é uma ferramenta diferente de um ICP global.

O CRITÉRIO, ESCRITO ANTES DE CORRER
-----------------------------------
Por bloco, e os três têm de passar:

    1. **RMS do ajuste < 30 m** contra a fronteira do IFAP.
    2. **A escala ajustada fica a menos de 10 % de 1,259 m/px.** Esta é a
       condição forte: vem de testemunho e não do ajuste, e é o que impede o
       ICP de comprar resíduo baixo à custa de encolher o desenho.
    3. Controlo independente — nenhuma válvula entra no ajuste:
         · banda: **≥ 8 das 12** válvulas dentro das parcelas de kiwi;
         · lobo:  **≥ 4 das 5** dentro do B1.

Falhando qualquer um num bloco, **esse bloco não publica posições**. O outro
pode publicar, e diz-se qual é qual.

EMENDA DE 04-09, ESCRITA ANTES DA SEGUNDA CORRIDA
--------------------------------------------------
A primeira corrida falhou o critério nos dois blocos, e **falhou pela razão
certa**: a escala fugiu de 1,263 (a estimativa inicial, a 0,3 % da declarada)
para **1,148 na banda e 1,130 no lobo** — o ICP estava a encolher o desenho
para comprar resíduo baixo. A condição 2 foi escrita para apanhar isso, e
apanhou.

A emenda não é afrouxar o critério; é aplicar a doutrina do projecto. **A
escala é testemunho directo do gestor — tipo 1 — e testemunho ganha ao
cálculo.** Logo a escala **fixa-se em 1,259 m/px** e o ICP passa a ajustar só
rotação e translação. Um grau de liberdade a menos, e o que sobra é geometria
rígida.

Os limiares de RMS e de válvulas dentro **não mudam**. A condição da escala
deixa de se aplicar porque a escala deixa de ser estimada.

RESSALVA QUE NÃO SE RESOLVE COM MÉTODO NENHUM
----------------------------------------------
O desenho é de **Julho de 2009**; o parcelário do IFAP é de **2025**. Dezasseis
anos de replantação e de redesenho de parcelas põem um chão no resíduo que não
é erro de ajuste. Por isso o critério é 30 m e não 10.
"""
import io
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from shapely.geometry import Point, shape
from shapely.ops import unary_union

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC_DEC = 841.0 / 2338 * 3.5          # 1.259 m/px
LIM_RMS, LIM_ESC, MAX_PAR = 30.0, 0.10, 120.0

# ── válvulas lidas à vista nos recortes com grelha (scan px) ────────────────
VALV = {1: (104, 781), 2: (195, 716), 3: (394, 722), 4: (257, 614), 5: (503, 616),
        6: (1051, 356), 7: (1138, 376), 8: (1213, 387), 9: (1265, 411),
        10: (1337, 378), 11: (1342, 521), 12: (1480, 414), 13: (1400, 398),
        14: (1623, 450), 15: (1726, 466), 16: (1820, 543), 17: (1969, 564)}
LOBO_V = [1, 2, 3, 4, 5]
BANDA_V = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# ── inicialização por bloco: DOIS pontos escolhidos por FORMA ──────────────
INIC = {
    "banda": (((996, 470), (530128, 4654997)),      # início do sector G
              ((2160, 570), (531536, 4655439))),    # última parcela, a leste
    "lobo":  (((104, 781), (529593, 4653920)),      # v1, na parcela do papagaio
              ((380, 615), (529864, 4654362))),     # meio das v4/v5, parcela grande
}

MET = json.load(io.open(os.path.join(AQUI, "base_sectores.json"), encoding="utf-8"))
LOBO_G, BANDA_G = shape(MET["b1"]), shape(MET["banda"])
KIWI = unary_union([LOBO_G, BANDA_G])


def contorno(g, passo=3.0):
    gs = g.geoms if g.geom_type == "MultiPolygon" else [g]
    P = []
    for p in gs:
        L = p.exterior.length
        P += [p.exterior.interpolate(t).coords[0] for t in np.arange(0, L, passo)]
    return np.array(P)


# ── a linha «Limites do terreno» do desenho ────────────────────────────────
A = np.array(Image.open(os.path.join(D, "_esquema_rega/scan.jpeg")).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
mx, mn = A.max(2), A.min(2)
# rosa/vinho fino: avermelhado, medianamente escuro, e NAO a caneta azul
linha = (R - G > 18) & (R - B > 6) & (R > 90) & (R < 215) & (G < 175)
linha &= ~((B - R > 25))
linha = ndimage.binary_opening(linha, np.ones((2, 2)))
ys, xs = np.nonzero(linha)
k = ys < 900
DES = np.column_stack([xs[k], ys[k]]).astype(float)
print("píxeis da linha de limite extraídos: %d" % len(DES))


def sem2(a1, a2, b1, b2):
    a1 = np.array([a1[0], -a1[1]], float); a2 = np.array([a2[0], -a2[1]], float)
    b1 = np.array(b1, float); b2 = np.array(b2, float)
    da, db = a2 - a1, b2 - b1
    s = np.linalg.norm(db) / np.linalg.norm(da)
    th = np.arctan2(db[1], db[0]) - np.arctan2(da[1], da[0])
    M = s * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return M, b1 - M @ a1


def ap(M, t, P):
    P = np.atleast_2d(P).astype(float)
    Q = np.column_stack([P[:, 0], -P[:, 1]])
    return (M @ Q.T).T + t


def icp(M, t, fonte, alvo, n=120, escala_fixa=None):
    """ICP rígido: rotação e translação, com a escala FIXA no valor declarado.

    Com a escala livre, o ICP encolhia o desenho 9-10 % para baixar o resíduo.
    A escala vem de testemunho e não se estima.
    """
    arv = cKDTree(alvo)
    for _ in range(n):
        P = ap(M, t, fonte)
        d, idx = arv.query(P)
        k = d < MAX_PAR
        if k.sum() < 30:
            break
        X = np.column_stack([fonte[k][:, 0], -fonte[k][:, 1]])
        Y = alvo[idx[k]]
        cx, cy = X.mean(0), Y.mean(0)
        Xc, Yc = X - cx, Y - cy
        H = Xc.T @ Yc
        U, S, Vt = np.linalg.svd(H)
        Rr = Vt.T @ U.T
        if np.linalg.det(Rr) < 0:
            Vt[-1] *= -1
            Rr = Vt.T @ U.T
        s = escala_fixa if escala_fixa else S.sum() / (Xc ** 2).sum()
        M = s * Rr
        t = cy - M @ cx
    P = ap(M, t, fonte)
    d = arv.query(P)[0]
    k = d < MAX_PAR
    return M, t, float(np.sqrt((d[k] ** 2).mean())), int(k.sum())


RES = {}
for bloco, geo, vs, cx in (("banda", BANDA_G, BANDA_V, 1),
                           ("lobo", LOBO_G, LOBO_V, 0)):
    (p1, q1), (p2, q2) = INIC[bloco]
    M0, t0 = sem2(p1, p2, q1, q2)
    # só os píxeis do desenho perto do bloco, na transformação inicial
    P0 = ap(M0, t0, DES)
    dd = np.array([geo.distance(Point(*p)) for p in P0])
    sel = DES[dd < 260]
    ALVO = contorno(geo)
    M, t, rms, npar = icp(M0, t0, sel, ALVO, escala_fixa=ESC_DEC)
    esc = float(np.sqrt(abs(np.linalg.det(M))))
    dev = abs(esc - ESC_DEC) / ESC_DEC
    U = ap(M, t, np.array([VALV[v] for v in vs]))
    dentro = [geo.distance(Point(*p)) == 0 for p in U]
    dist = [geo.distance(Point(*p)) for p in U]
    print()
    print("=" * 74)
    print("%s — %d píxeis de linha seleccionados, %d emparelhados" % (bloco.upper(), len(sel), npar))
    print("=" * 74)
    print("  RMS %.1f m   ·   escala %.3f m/px (declarada %.3f, desvio %.1f %%)"
          % (rms, esc, ESC_DEC, 100 * dev))
    for v, u, dd_ in zip(vs, U, dist):
        print("     v%-2d -> E %.0f N %.0f   %s"
              % (v, u[0], u[1], "dentro" if dd_ == 0 else "a %.0f m" % dd_))
    RES[bloco] = dict(rms=rms, escala=esc, desvio_escala=dev,
                      dentro=int(sum(dentro)), n=len(vs),
                      M=[list(map(float, r)) for r in M], t=list(map(float, t)),
                      posicoes={str(v): [float(a), float(b)] for v, (a, b) in zip(vs, U)},
                      distancias={str(v): float(x) for v, x in zip(vs, dist)})

MIN_DENTRO = {"banda": 8, "lobo": 4}
print()
print("=" * 74)
print("CRITÉRIO (escrito antes de correr)")
print("=" * 74)
ok_total = {}
for b, r in RES.items():
    c1 = r["rms"] < LIM_RMS
    c2 = True   # escala fixa no valor declarado; deixou de ser estimada
    c3 = r["dentro"] >= MIN_DENTRO[b]
    ok_total[b] = c1 and c2 and c3
    print("%-6s  RMS %5.1f<%.0f %-5s · escala %+5.1f%%<%.0f%% %-5s · %d/%d dentro (min %d) %-5s -> %s"
          % (b, r["rms"], LIM_RMS, "OK" if c1 else "FALHA",
             100 * r["desvio_escala"], 100 * LIM_ESC, "OK" if c2 else "FALHA",
             r["dentro"], r["n"], MIN_DENTRO[b], "OK" if c3 else "FALHA",
             "PUBLICA" if ok_total[b] else "NÃO PUBLICA"))
print("=" * 74)

json.dump(dict(escala_declarada=ESC_DEC, limiares=dict(rms=LIM_RMS, escala=LIM_ESC,
                                                       min_dentro=MIN_DENTRO,
                                                       max_emparelhamento=MAX_PAR),
               blocos=RES, aceite={k: bool(v) for k, v in ok_total.items()},
               ressalva="desenho de Jul-2009 contra parcelário de 2025; parte do "
                        "resíduo é mudança real de fronteira, não erro de ajuste"),
          io.open(os.path.join(AQUI, "georref_por_bloco.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("escrito georref_por_bloco.json")
