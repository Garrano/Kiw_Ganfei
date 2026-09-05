# -*- coding: utf-8 -*-
"""Quinta tentativa. As quatro anteriores estão todas retiradas, e porquê.

    1. ICP global automático ....... RMS  70,3 m   segmentação via 8 de 13 bandas
    2. afim com pontos à vista ..... RMS 189,1 m   extremos do desenho casados
                                                   com extremos em UTM, e o
                                                   desenho está rodado 22°
    3. idem, ponta corrigida ....... RMS 112,4 m   a ponta oriental estava lida
                                                   600 px ao lado
    4. ICP por bloco ............... RMS  33,6 m   RETIRADO: 55,9 % dos píxeis
                                                   que o ICP alinhava eram os
                                                   círculos das válvulas, e a
                                                   inicialização do lobo era
                                                   feita de válvulas

O QUE MUDA AQUI, E CADA COISA CORRIGE UM DEFEITO NOMEADO
---------------------------------------------------------
**1 · A fonte da linha exclui as válvulas por geometria, não por cor.** Tentou-se
separar a tinta manuscrita da linha impressa pela cor: não separa — a mediana do
anel das válvulas é (144,84,102) e a da linha (188,145,162), e a regra mais
apertada ainda deixava 23 % junto às válvulas destruindo 72 % da linha. Portanto
**apagam-se todos os píxeis a menos de 32 px de um centro de válvula.** Perde-se
linha verdadeira perto das válvulas; ganha-se um controlo que é independente
**por construção** e não por afirmação.

**2 · O alvo são as fronteiras de CADA parcela, não a união.** O Controlo 3
mediu que 66,3 % do traço do desenho caía *dentro* do polígono dissolvido — o
desenho mostra as divisões internas, e a união apagou-as. Alinhar contra a união
era pedir ao ICP que puxasse o desenho para fora.

**3 · O lobo não é inicializado com válvulas.** Herda escala e rotação da banda
— que vêm de dois pontos de fronteira — e ajusta **só a translação**. Dois graus
de liberdade, nenhum deles tocado por uma válvula.

**4 · A escala é fixa no valor declarado.** 1:3500 em A1 = 1,259 m/px. É
testemunho, e não se estima. (Note-se que o «0,3 %» que publiquei era N = 1: a
ponta está em x ≈ 2138 e não 2160, o que dá 1,288 e portanto 2,3 %.)

O CRITÉRIO, E DESTA VEZ COM O PODER CALCULADO ANTES
----------------------------------------------------
O critério anterior não tinha poder: o Controlo 3 mostrou por Monte Carlo que,
mesmo com ruído quase nulo, a probabilidade de passar era 0,21 na banda e 0,06
no lobo. **Um limiar que quase nunca passa não é um teste, é um carimbo de
recusa.** E era binário sobre uma fronteira — uma válvula 2 m fora contava como
uma a 200 m.

    A · ÂNCORA DE TIPO 1, e é a que decide.
        O gestor nomeou «Zona 0 = válvulas 8, 9, 10». A Zona 0 é uma máscara
        geográfica de 2,02 ha, centro (530999, 4655102), que **não entra em
        nada** deste ajuste. O centróide das válvulas 8, 9 e 10 transformadas
        tem de cair a **≤ 60 m** desse centro.

    B · DISTÂNCIA CONTÍNUA, não binária.
        Mediana da distância das 17 válvulas à parcela de kiwi mais próxima
        **≤ 25 m**, e máximo ≤ 70 m.

    C · PODER, medido antes de olhar para o resultado.
        Perturba-se a transformação aceite com rotações de ±3° e translações de
        ±80 m e conta-se quantas vezes o critério passaria. **Se passar em mais
        de 20 % das perturbações, o critério não discrimina e não se usa.**

Falhando A ou B, não se publicam posições. Falhando C, não se publica nem se
usa o critério — reescreve-se.
"""
import sys as _s, os as _o
_s.path.insert(0, r'C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS')
from proveniencia import marca as _marca  # noqa: E402

import io
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from shapely.geometry import Point, shape

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = 841.0 / 2338 * 3.5                 # 1,259 m/px — 1:3500 em A1
RAIO_EXCL, MAX_PAR = 32.0, 110.0
LIM_ANCORA, LIM_MED, LIM_MAX, LIM_PODER = 60.0, 25.0, 70.0, 0.20

VALV = {1: (104, 781), 2: (195, 716), 3: (394, 722), 4: (257, 614), 5: (503, 616),
        6: (1051, 356), 7: (1138, 376), 8: (1213, 387), 9: (1265, 411),
        10: (1337, 378), 11: (1342, 521), 12: (1480, 414), 13: (1400, 398),
        14: (1623, 450), 15: (1726, 466), 16: (1820, 543), 17: (1969, 564)}
LOBO_V, BANDA_V = [1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
# dois pontos de FRONTEIRA, nenhum é válvula
INIC_BANDA = (((996, 470), (530128, 4654997)), ((2138, 566), (531536, 4655439)))

MET = json.load(io.open(os.path.join(AQUI, "base_sectores.json"), encoding="utf-8"))
Z0 = json.load(io.open(os.path.join(AQUI, "zona0.json"), encoding="utf-8"))
LOBO_G, BANDA_G = shape(MET["b1"]), shape(MET["banda"])


def bordos(g, passo=2.5):
    """Fronteiras de CADA parcela, incluindo as divisões internas."""
    gs = g.geoms if g.geom_type == "MultiPolygon" else [g]
    P = []
    for p in gs:
        for anel in [p.exterior] + list(p.interiors):
            L = anel.length
            P += [anel.interpolate(t).coords[0] for t in np.arange(0, L, passo)]
    return np.array(P)


# ── a linha do desenho, SEM as válvulas ────────────────────────────────────
A = np.array(Image.open(os.path.join(D, "_esquema_rega/scan.jpeg")).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
linha = (R - G > 18) & (R - B > 6) & (R > 90) & (R < 215) & (G < 175)
linha &= ~(B - R > 25)
linha = ndimage.binary_opening(linha, np.ones((2, 2)))
H, W = R.shape
yy, xx = np.mgrid[0:H, 0:W]
excl = np.zeros((H, W), bool)
for (cx, cy) in VALV.values():
    excl |= ((xx - cx) ** 2 + (yy - cy) ** 2) < RAIO_EXCL ** 2
antes = (linha & (yy < 900)).sum()
linha &= ~excl
ys, xs = np.nonzero(linha & (yy < 900))
DES = np.column_stack([xs, ys]).astype(float)
C = np.array(list(VALV.values()), float)
d0 = np.min(np.linalg.norm(DES[:, None, :] - C[None, :, :], axis=2), axis=1)
print("linha: %d px antes, %d depois de excluir as válvulas (−%.1f %%)"
      % (antes, len(DES), 100 * (1 - len(DES) / antes)))
print("  distância mínima de um píxel a um centro de válvula: %.1f px  (exigido > %.0f)"
      % (d0.min(), RAIO_EXCL))
assert d0.min() >= RAIO_EXCL - 1, "a exclusão não funcionou"


def sem2(a1, a2, b1, b2, esc=None):
    a1 = np.array([a1[0], -a1[1]], float); a2 = np.array([a2[0], -a2[1]], float)
    b1, b2 = np.array(b1, float), np.array(b2, float)
    da, db = a2 - a1, b2 - b1
    s = esc or np.linalg.norm(db) / np.linalg.norm(da)
    th = np.arctan2(db[1], db[0]) - np.arctan2(da[1], da[0])
    M = s * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return M, b1 - M @ a1


def ap(M, t, P):
    P = np.atleast_2d(P).astype(float)
    return (M @ np.column_stack([P[:, 0], -P[:, 1]]).T).T + t


def icp(M, t, fonte, alvo, so_translacao=False, n=150):
    arv = cKDTree(alvo)
    for _ in range(n):
        P = ap(M, t, fonte)
        d, idx = arv.query(P)
        k = d < MAX_PAR
        if k.sum() < 40:
            break
        X = np.column_stack([fonte[k][:, 0], -fonte[k][:, 1]])
        Y = alvo[idx[k]]
        if so_translacao:
            # FIXA a translação, não a acumula. Somá-la a cada iteração fazia o
            # lobo divergir para coordenadas na casa dos milhões.
            t = (Y - (M @ X.T).T).mean(0)
            continue
        cx, cy = X.mean(0), Y.mean(0)
        Xc, Yc = X - cx, Y - cy
        U, S, Vt = np.linalg.svd(Xc.T @ Yc)
        Rr = Vt.T @ U.T
        if np.linalg.det(Rr) < 0:
            Vt[-1] *= -1
            Rr = Vt.T @ U.T
        M = ESC * Rr
        t = cy - M @ cx
    P = ap(M, t, fonte)
    d = arv.query(P)[0]
    k = d < MAX_PAR
    return M, t, float(np.sqrt((d[k] ** 2).mean())), int(k.sum())


# ── banda ──────────────────────────────────────────────────────────────────
(p1, q1), (p2, q2) = INIC_BANDA
M0, t0 = sem2(p1, p2, q1, q2, esc=ESC)
P0 = ap(M0, t0, DES)
selb = DES[np.array([BANDA_G.distance(Point(*p)) for p in P0]) < 240]
Mb, tb, rmsb, nb = icp(M0, t0, selb, bordos(BANDA_G))
print()
print("BANDA  %d px · RMS %.1f m · rotação %.2f°"
      % (nb, rmsb, np.degrees(np.arctan2(Mb[1, 0], Mb[0, 0]))))

# ── lobo: herda escala e rotação da banda, ajusta SÓ translação ────────────
# O arranque do lobo NÃO toca em válvulas: toma os píxeis de linha que caem na
# zona do lobo no PRÓPRIO desenho (x < 720, y > 440 — o canto onde ele está
# desenhado) e translada-os para o centróide do lobo real. Só layout e linha.
mlobo = (DES[:, 0] < 720) & (DES[:, 1] > 440)
if mlobo.sum() < 100:
    raise SystemExit("sem píxeis de linha na zona do lobo")
tl = tb + (np.array(LOBO_G.centroid.coords[0]) - ap(Mb, tb, DES[mlobo]).mean(0))
sell = DES[mlobo]
Ml, tl, rmsl, nl = icp(Mb, tl, sell, bordos(LOBO_G), so_translacao=True)
print("LOBO   %d px · RMS %.1f m · só translação" % (nl, rmsl))


def avalia(Mb, tb, Ml, tl):
    U = {}
    for v in BANDA_V:
        U[v] = ap(Mb, tb, np.array([VALV[v]]))[0]
    for v in LOBO_V:
        U[v] = ap(Ml, tl, np.array([VALV[v]]))[0]
    c = np.mean([U[v] for v in (8, 9, 10)], axis=0)
    anc = float(np.hypot(*(c - np.array(Z0["centro"]))))
    dd = []
    for v, p in U.items():
        g = LOBO_G if v in LOBO_V else BANDA_G
        dd.append(g.distance(Point(*p)))
    return U, anc, float(np.median(dd)), float(np.max(dd))


U, anc, med, mx = avalia(Mb, tb, Ml, tl)
print()
print("A · centróide das válvulas 8,9,10 -> %.0f m do centro da Zona 0" % anc)
print("B · distância à parcela: mediana %.1f m · máximo %.1f m" % (med, mx))

# ── C · o poder do critério, antes de julgar ───────────────────────────────
rng = np.random.default_rng(7)
passa = 0
N = 400
for _ in range(N):
    th = np.radians(rng.uniform(-3, 3))
    Rr = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    dt = rng.uniform(-80, 80, 2)
    _, a2, m2, x2 = avalia(Rr @ Mb, tb + dt, Rr @ Ml, tl + dt)
    if a2 <= LIM_ANCORA and m2 <= LIM_MED and x2 <= LIM_MAX:
        passa += 1
poder = passa / N
print("C · sob perturbação (±3°, ±80 m) o critério passaria %.0f %% das vezes"
      % (100 * poder))

ok_a, ok_b, ok_c = anc <= LIM_ANCORA, (med <= LIM_MED and mx <= LIM_MAX), poder <= LIM_PODER
print()
print("=" * 74)
print("A · âncora Zona 0    %5.0f m <= %.0f ............ %s" % (anc, LIM_ANCORA, "PASSA" if ok_a else "FALHA"))
print("B · mediana %.1f <= %.0f e máximo %.1f <= %.0f ... %s"
      % (med, LIM_MED, mx, LIM_MAX, "PASSA" if ok_b else "FALHA"))
print("C · poder: passa em %.0f %% <= %.0f %% ........... %s"
      % (100 * poder, 100 * LIM_PODER, "PASSA" if ok_c else "FALHA — critério não discrimina"))
print("-" * 74)
print("-> %s" % ("POSIÇÕES PUBLICÁVEIS, com incerteza declarada de ±%.0f m" % max(med, 20)
                 if (ok_a and ok_b and ok_c) else "NÃO SE PUBLICAM POSIÇÕES"))
print("=" * 74)
for v in sorted(U):
    g = LOBO_G if v in LOBO_V else BANDA_G
    dv = g.distance(Point(*U[v]))
    print("   v%-2d  E %.0f  N %.0f   %s" % (v, U[v][0], U[v][1],
          "dentro" if dv == 0 else "a %.0f m" % dv))

json.dump(dict(_produtor=_marca(), escala=ESC, raio_exclusao_px=RAIO_EXCL,
               px_linha_apos_exclusao=int(len(DES)),
               dist_min_valvula_px=float(d0.min()),
               rms_banda=rmsb, rms_lobo=rmsl,
               ancora_zona0_m=anc, mediana_m=med, maximo_m=mx, poder=poder,
               limiares=dict(ancora=LIM_ANCORA, mediana=LIM_MED, maximo=LIM_MAX,
                             poder=LIM_PODER),
               aceite=bool(ok_a and ok_b and ok_c),
               posicoes={str(v): [float(U[v][0]), float(U[v][1])] for v in U},
               M_banda=[list(map(float, r)) for r in Mb], t_banda=list(map(float, tb)),
               M_lobo=[list(map(float, r)) for r in Ml], t_lobo=list(map(float, tl))),
          io.open(os.path.join(AQUI, "georref_v5.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print()
print("escrito georref_v5.json")
