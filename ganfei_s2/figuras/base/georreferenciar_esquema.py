# -*- coding: utf-8 -*-
"""Georreferenciar o «Esquema de rega retificado» contra o parcelário do IFAP.

PORQUE ISTO É NECESSÁRIO
------------------------
Há quatro reconstruções das posições das válvulas em disco. **Discordam entre
92 e 398 m**, e o espaçamento entre válvulas vizinhas é de 98 m — ou seja, a
discordância é maior do que a distância entre válvulas. Só a `por_area` passa o
teste das áreas declaradas, **e esse teste é circular**: a `por_area` foi
construída por área acumulada para bater com as áreas declaradas, portanto
compará-la com elas reproduz a calibração em vez de a verificar.

E o desenho mostra por que razão nenhuma delas podia acertar: **há duas fiadas
de válvulas na mesma estação de linha** — 10 e 13 de um lado da conduta, 11 e
12 do outro, todas anotadas «306 a 307». Qualquer reconstrução que espalhe as
válvulas ao longo de um eixo tem de errar.

O QUE ISTO FAZ EM VEZ DISSO
---------------------------
Ajusta uma transformação de semelhança (rotação, escala, translação) do desenho
para o terreno, usando as fronteiras: o **limite do terreno impresso** contra a
**união das parcelas de kiwi do IFAP**. As válvulas vêm depois, arrastadas pela
transformação — não são o que a define.

A FALSIFICAÇÃO, FIXADA ANTES DE CORRER
---------------------------------------
    1. **RMS do ajuste < 20 m.** Acima disso o desenho não é rectificável por
       semelhança e o problema é outro (distorção do papel, ou o desenho não é
       a escala uniforme — o `valvulas_v4.json` já suspeitava disso: «o desenho
       NÃO está à escala declarada»).
    2. **As 17 válvulas caem dentro das parcelas de kiwi.** É um controlo
       independente do ajuste: nada nele usa as válvulas.

Se qualquer das duas falhar, **não se publica posição de válvula nenhuma** e a
camada de rega desenha só o que o esquema fixa sem geometria: que válvula serve
que sector, e o débito de cada sector.
"""
import io
import json
import os

import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape, Point
from shapely.ops import transform as sht, unary_union
from scipy import ndimage

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(D, "_esquema_rega", "scan.jpeg")
LIM_RMS = 20.0

A = np.array(Image.open(SCAN).convert("RGB")).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]
mx, mn = A.max(2), A.min(2)
sat = mx - mn
print("scan %d x %d" % (W, H))

# ── 1 · as bandas de sector: pastéis claros e saturados, sem ser tinta ──────
banda = (sat > 22) & (mx > 140) & (mn > 70)
banda = ndimage.binary_opening(banda, np.ones((3, 3)))
banda = ndimage.binary_closing(banda, np.ones((15, 15)))
lab, n = ndimage.label(banda)
if n:
    tam = np.bincount(lab.ravel())
    tam[0] = 0
    manter = np.nonzero(tam > 4000)[0]
    banda = np.isin(lab, manter)
print("bandas de sector: %.2f %% do scan, %d manchas" % (100 * banda.mean(),
                                                         len(manter) if n else 0))

# ── 2 · os círculos vermelhos escritos à mão = as válvulas ──────────────────
vermelho = (R > 90) & (R - G > 45) & (R - B > 35) & (G < 150)
vermelho = ndimage.binary_closing(vermelho, np.ones((9, 9)))
lab, n = ndimage.label(vermelho)
tam = np.bincount(lab.ravel())
tam[0] = 0
cand = [i for i in np.nonzero(tam > 400)[0]]
cent = ndimage.center_of_mass(vermelho, lab, cand)
print("manchas vermelhas com >400 px: %d" % len(cand))

# ── 3 · o alvo: união das parcelas de kiwi ──────────────────────────────────
T = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
K = json.load(io.open(os.path.join(D, "_MULTIVERSO/SAIDA_H2_patologista/ifap_kiwi_largo.json"),
                      encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
META = json.load(io.open(os.path.join(AQUI, "base_sectores.json"), encoding="utf-8"))
ALVO = unary_union([shape(META["b1"]), shape(META["banda"])])
print("alvo: %.2f ha" % (ALVO.area / 1e4))


def nuvem(mask, passo=3):
    ys, xs = np.nonzero(mask)
    return np.column_stack([xs[::passo], ys[::passo]]).astype(float)


def momentos(P):
    c = P.mean(0)
    Q = P - c
    u, s, vt = np.linalg.svd(Q, full_matrices=False)
    return c, s / np.sqrt(len(P)), vt


def contorno(geo, passo=4.0):
    gs = geo.geoms if geo.geom_type == "MultiPolygon" else [geo]
    pts = []
    for g in gs:
        L = g.exterior.length
        pts += [g.exterior.interpolate(t).coords[0]
                for t in np.arange(0, L, passo)]
    return np.array(pts)


ORIG = nuvem(banda, 3)
# o alvo em nuvem: pontos dentro das parcelas, amostrados na mesma densidade
minx, miny, maxx, maxy = ALVO.bounds
gx, gy = np.meshgrid(np.arange(minx, maxx, 4.0), np.arange(miny, maxy, 4.0))
dentro = np.array([ALVO.contains(Point(x, y)) for x, y in zip(gx.ravel(), gy.ravel())])
DEST = np.column_stack([gx.ravel()[dentro], gy.ravel()[dentro]])
print("nuvens: desenho %d pontos · terreno %d pontos" % (len(ORIG), len(DEST)))

c1, s1, v1 = momentos(ORIG)
c2, s2, v2 = momentos(DEST)
esc = s2[0] / s1[0]
a1 = np.arctan2(v1[0][1], v1[0][0])
a2 = np.arctan2(v2[0][1], v2[0][0])


def semelhanca(ang, esc, c1, c2, espelho=False):
    Rm = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    Fm = np.diag([1.0, -1.0]) if espelho else np.eye(2)
    M = esc * Rm @ Fm
    return M, c2 - M @ c1


def aplica(M, t, P):
    return (M @ P.T).T + t


# o scan tem y para baixo: a hipotese de espelho tem de ser testada, nao assumida
from scipy.spatial import cKDTree
arv = cKDTree(DEST)
melhor = None
for espelho in (True, False):
    for dang in (0.0, np.pi):
        M, t = semelhanca(a2 - a1 * (-1 if espelho else 1) + dang, esc, c1, c2, espelho)
        P = aplica(M, t, ORIG)
        d = arv.query(P)[0]
        rms = float(np.sqrt((d ** 2).mean()))
        print("  arranque espelho=%-5s giro=%3.0f°  RMS %7.1f m" % (espelho,
                                                                    np.degrees(dang), rms))
        if melhor is None or rms < melhor[0]:
            melhor = (rms, M, t, espelho)
rms, M, t, espelho = melhor

# ── 4 · ICP ─────────────────────────────────────────────────────────────────
P = aplica(M, t, ORIG)
for it in range(60):
    d, idx = arv.query(P)
    keep = d < np.percentile(d, 80)
    X, Y = P[keep], DEST[idx[keep]]
    cx, cy = X.mean(0), Y.mean(0)
    Hh = (X - cx).T @ (Y - cy)
    U, S, Vt = np.linalg.svd(Hh)
    Rr = Vt.T @ U.T
    if np.linalg.det(Rr) < 0:
        Vt[-1] *= -1
        Rr = Vt.T @ U.T
    ss = S.sum() / ((X - cx) ** 2).sum()
    P = (ss * Rr @ (P - cx).T).T + cy
    M = ss * Rr @ M
    t = cy - (ss * Rr @ cx) + (ss * Rr @ (t - t))  # recomposto abaixo
    t = P.mean(0) - (M @ ORIG.mean(0))
rms = float(np.sqrt((arv.query(aplica(M, t, ORIG))[0] ** 2).mean()))
escala_m_px = float(np.sqrt(abs(np.linalg.det(M))))
ang = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
print()
print("ajuste final: RMS %.1f m · escala %.4f m/px · rotação %.2f°%s"
      % (rms, escala_m_px, ang, "  (espelhado)" if espelho else ""))

# ── 5 · as válvulas arrastadas, e o controlo independente ───────────────────
VAL = [aplica(M, t, np.array([[c[1], c[0]]]))[0] for c in cent]
dentro_n = sum(1 for p in VAL if ALVO.contains(Point(*p)))
print("manchas vermelhas dentro das parcelas de kiwi: %d de %d"
      % (dentro_n, len(VAL)))

print()
print("=" * 76)
ok1 = rms < LIM_RMS
print("1 · RMS %.1f m < %.0f m ................. %s" % (rms, LIM_RMS,
                                                        "PASSA" if ok1 else "FALHA"))
print("2 · válvulas dentro do kiwi ............. %d/%d" % (dentro_n, len(VAL)))
if not ok1:
    print()
    print("-> NÃO se publica posição de válvula. A camada de rega desenha só o")
    print("   que o esquema fixa sem geometria: válvula→sector e débito.")
else:
    print("-> transformação aceite.")
print("=" * 76)

json.dump(dict(rms_m=rms, escala_m_px=escala_m_px, rotacao_graus=ang,
               espelhado=bool(espelho), aceite=bool(ok1),
               M=[list(map(float, r)) for r in M], t=list(map(float, t)),
               n_manchas_vermelhas=len(VAL),
               manchas_dentro=int(dentro_n),
               limiar_rms=LIM_RMS),
          io.open(os.path.join(AQUI, "georref_esquema.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("escrito georref_esquema.json")
