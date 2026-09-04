# -*- coding: utf-8 -*-
"""Georreferenciar o esquema por pontos de controlo escolhidos à vista.

PORQUE UMA SEGUNDA TENTATIVA
----------------------------
A primeira (`georreferenciar_esquema.py`) deixou um algoritmo escolher os
pontos: segmentava as bandas por cor e alinhava as duas nuvens por ICP. Deu
**RMS 70,3 m** e falhou o critério. O erro não foi a ideia — foi eu ter
delegado a escolha dos pontos a uma segmentação que só apanhava 8 das 13
bandas.

Aqui os pontos são escolhidos **à vista**, em feições que existem nos dois
lados e são inequívocas: os extremos do lobo do B1 e os extremos da banda
contígua. São feições de fronteira, não de sinal.

A INCERTEZA, declarada antes
----------------------------
A escala sai a ≈1,7 m por píxel do scan. A minha leitura de uma feição no
desenho tem uns **±15 px**, ou seja **±25 m**. Isso é o chão do método: nenhum
ajuste pode sair melhor do que isso, e um que saia é suspeito.

Contra um espaçamento entre válvulas de 98 m, ±25 m serve para dizer **em que
sector cai cada válvula** e não serve para dizer onde ela está dentro do
sector.

O CRITÉRIO, escrito antes de correr
-----------------------------------
    1. RMS do ajuste **< 45 m** — o dobro do chão de leitura. Acima disso o
       desenho não é rectificável por uma transformação global.
    2. **≥ 15 das 17 válvulas** caem dentro das parcelas de kiwi do IFAP.
       É um controlo independente: nenhuma válvula entrou no ajuste.

Falhando qualquer um, não se publicam posições — como da primeira vez.
"""
import io
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage
from shapely.geometry import Point, shape
from shapely.ops import unary_union

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
LIM_RMS = 45.0
MIN_DENTRO = 15

# ── pontos de controlo: (x, y) no scan  ->  (E, N) em UTM 29N ───────────────
#   Lidos na `GRELHA_esboco.png` contra o parcelário da `GRELHA_parcelario.png`.
#   Só feições de fronteira, e só as que não têm gémeas próximas.
CP = [
    ((74, 770), (529495, 4653955), "B1 · extremo OESTE (bico do rabo-de-peixe)"),
    ((126, 819), (529574, 4653832), "B1 · extremo SUL"),
    ((583, 605), (530063, 4654416), "B1 · extremo ESTE (canto da parcela grande)"),
    ((328, 567), (529729, 4654477), "B1 · extremo NORTE"),
    ((1044, 481), (530128, 4654997), "banda · extremo OESTE (início do sector G)"),
    ((1562, 591), (531536, 4655439), "banda · extremo ESTE"),
]
X = np.array([c[0] for c in CP], float)
Y = np.array([c[1] for c in CP], float)


def ajusta(X, Y, modo):
    """Semelhança (4 gl) ou afim (6 gl), por mínimos quadrados."""
    n = len(X)
    if modo == "afim":
        A = np.zeros((2 * n, 6))
        b = np.zeros(2 * n)
        for i, (p, q) in enumerate(zip(X, Y)):
            A[2 * i] = [p[0], p[1], 1, 0, 0, 0]
            A[2 * i + 1] = [0, 0, 0, p[0], p[1], 1]
            b[2 * i], b[2 * i + 1] = q
        s = np.linalg.lstsq(A, b, rcond=None)[0]
        M = np.array([[s[0], s[1]], [s[3], s[4]]])
        t = np.array([s[2], s[5]])
    else:
        A = np.zeros((2 * n, 4))
        b = np.zeros(2 * n)
        for i, (p, q) in enumerate(zip(X, Y)):
            A[2 * i] = [p[0], -p[1], 1, 0]
            A[2 * i + 1] = [p[1], p[0], 0, 1]
            b[2 * i], b[2 * i + 1] = q
        s = np.linalg.lstsq(A, b, rcond=None)[0]
        M = np.array([[s[0], -s[1]], [s[1], s[0]]])
        t = np.array([s[2], s[3]])
    return M, t


def aplica(M, t, P):
    return (M @ np.atleast_2d(P).T).T + t


print("pontos de controlo: %d" % len(CP))
res = {}
for modo in ("semelhanca", "afim"):
    M, t = ajusta(X, Y, modo)
    P = aplica(M, t, X)
    d = np.linalg.norm(P - Y, axis=1)
    rms = float(np.sqrt((d ** 2).mean()))
    esc = float(np.sqrt(abs(np.linalg.det(M))))
    ang = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
    res[modo] = (M, t, rms, d)
    print()
    print("── %s ── RMS %.1f m · escala %.3f m/px · rotação %.2f°"
          % (modo.upper(), rms, esc, ang))
    for (px, q, nome), e in zip(CP, d):
        print("   %-46s %5.1f m" % (nome, e))

modo = min(res, key=lambda k: res[k][2])
M, t, rms, d = res[modo]
print()
print("melhor: %s, RMS %.1f m" % (modo, rms))

# ── as válvulas: círculos vermelhos manuscritos ─────────────────────────────
A = np.array(Image.open(os.path.join(D, "_esquema_rega/scan.jpeg")).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
verm = (R > 80) & (R - G > 35) & (R - B > 28) & (G < 165)
verm = ndimage.binary_closing(verm, np.ones((11, 11)))
verm = ndimage.binary_fill_holes(verm)
lab, n = ndimage.label(verm)
tam = np.bincount(lab.ravel()); tam[0] = 0
# um círculo de válvula tem ~35-45 px de diâmetro no scan
cand = [i for i in np.nonzero((tam > 700) & (tam < 9000))[0]]
cent = ndimage.center_of_mass(verm, lab, cand)
VAL = np.array([[c[1], c[0]] for c in cent])       # (x, y)
# fora da zona das notas manuscritas em baixo e da caixa do título
k = (VAL[:, 1] < 900) & (VAL[:, 0] < 1900)
VAL = VAL[k]
print()
print("círculos vermelhos candidatos a válvula: %d" % len(VAL))

MET = json.load(io.open(os.path.join(AQUI, "base_sectores.json"), encoding="utf-8"))
KIWI = unary_union([shape(MET["b1"]), shape(MET["banda"])])
UTM = aplica(M, t, VAL)
dentro = [KIWI.contains(Point(*p)) for p in UTM]
print("caem dentro das parcelas de kiwi: %d de %d" % (sum(dentro), len(UTM)))
folga = [KIWI.distance(Point(*p)) for p in UTM]
print("distância ao kiwi dos que ficam fora: %s"
      % ", ".join("%.0f m" % f for f, dd in zip(folga, dentro) if not dd) or "—")

ok1, ok2 = rms < LIM_RMS, sum(dentro) >= MIN_DENTRO
print()
print("=" * 74)
print("1 · RMS %.1f m < %.0f m ............... %s" % (rms, LIM_RMS, "PASSA" if ok1 else "FALHA"))
print("2 · %d/%d válvulas dentro do kiwi (min %d) ... %s"
      % (sum(dentro), len(UTM), MIN_DENTRO, "PASSA" if ok2 else "FALHA"))
print("-> %s" % ("TRANSFORMAÇÃO ACEITE — posições publicáveis COM incerteza de "
                 "±%.0f m" % max(rms, 25) if ok1 and ok2 else
                 "REJEITADA — não se publicam posições"))
print("=" * 74)

json.dump(dict(modo=modo, rms_m=rms, limiar_rms=LIM_RMS,
               chao_de_leitura_m=25.0,
               M=[list(map(float, r)) for r in M], t=list(map(float, t)),
               pontos_controlo=[dict(scan=list(p), utm=list(q), nome=nome,
                                     residuo_m=float(e))
                                for (p, q, nome), e in zip(CP, d)],
               n_valvulas_detectadas=int(len(UTM)),
               n_dentro_kiwi=int(sum(dentro)),
               aceite=bool(ok1 and ok2),
               posicoes=[dict(x=float(a), y=float(b), E=float(e), N=float(f),
                              dentro=bool(g))
                         for (a, b), (e, f), g in zip(VAL, UTM, dentro)]),
          io.open(os.path.join(AQUI, "georref_manual.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("escrito georref_manual.json")
