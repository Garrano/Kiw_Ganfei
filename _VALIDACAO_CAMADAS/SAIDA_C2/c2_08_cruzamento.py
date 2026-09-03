# -*- coding: utf-8 -*-
"""C2-08 — O CRUZAMENTO. Separar o MOMENTO do LUGAR.

O problema, posto pela C1 (S15 e NAO TESTAVEL):

  «o disco OESTE esta centrado numa coordenada que foi escolhida por o NDVI ter
   caido ali. O MOMENTO nao e circular — nove Invernos anteriores servem de
   controlo interno —, mas o LUGAR e.»

E a C1 diz mesmo qual seria o teste: «repetir a medicao sobre uma particao do
pomar que nao conheca os focos (p. ex. por valvula), e ver se a valvula 8 se
destaca sozinha.»

O desenho executado aqui vai um passo mais longe, porque uma unidade que se
destaca sozinha ainda e um teste de um ponto. Em vez disso:

  1. Particiona-se o pomar por unidades que NAO conhecem nem o NDVI nem as
     coordenadas dos focos. Duas particoes, de proveniencias diferentes:
       P1  VALVULAS — Voronoi sobre as 12 posicoes de `valvulas_por_area.json`,
           colocadas pela tabela de areas do gestor (R2 G35). Proveniencia
           externa a todo o sensoriamento remoto.
       P2  QUADRICULA — mosaicos de 60 m com origem no canto da AOI. Geometria
           pura, sem nenhuma escolha.
  2. Em cada unidade mede-se, com instrumentos independentes:
       X_u = queda de NDVI 2024 -> 2026, relativa a queda do pomar inteiro
             (Sentinel-2, optico)
       Y_u(w) = anomalia de VV da unidade no Inverno w, relativa ao pomar
             inteiro no mesmo Inverno (Sentinel-1, radar activo banda C)
  3. Correlaciona-se X com Y **em cada um dos dez Invernos, separadamente**.

O que cada resultado significa:
  - Se a correlacao for nula nos nove primeiros Invernos e saltar no de
    2025-26, entao dois instrumentos independentes datam o mesmo evento nos
    mesmos sitios, e nem o momento nem o lugar foram escolhidos por ninguem.
    E a verificacao mais forte que este caso pode produzir.
  - Se a correlacao for alta em todos os Invernos, ha uma diferenca ESTRUTURAL
    permanente entre unidades que o radar ve desde sempre, e o cruzamento nao
    data nada.
  - Se nao houver correlacao nenhuma, o cruzamento falha e diz-se que falhou.

PLACEBO: repete-se tudo com X' = queda de NDVI 2022 -> 2024, um par de anos em
que nao ha evento. Se X' tambem correlacionar com o Inverno de 2025-26, o teste
nao vale nada.
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
nd = carrega_ndvi(TODAS)
E, N = centros_celulas()

pilha = np.load(os.path.join(SAIDA, "c2_07_sar_pilha.npy"))
meta = json.load(open(os.path.join(SAIDA, "c2_07_sar_cenas.json"), encoding="utf-8"))
inv = np.array([m["inverno"] for m in meta])
orb = np.array([m["orbita"] if m["orbita"] is not None else -1 for m in meta])
INVS = sorted(set(inv))
print("pilha SAR: %s | %d Invernos | orbitas %s"
      % (pilha.shape, len(INVS), sorted(set(orb))))

# ---------------------------------------------------------------- particoes
val = json.load(open(os.path.join(RAIZ, "valvulas_por_area.json"), encoding="latin-1"))
chaves = sorted(val, key=int)
vx = np.array([val[k]["E"] for k in chaves])
vy = np.array([val[k]["N"] for k in chaves])
d2 = (E[..., None] - vx) ** 2 + (N[..., None] - vy) ** 2
prox = np.argmin(d2, axis=-1)
dmin = np.sqrt(np.min(d2, axis=-1))
P1 = {}
for i, k in enumerate(chaves):
    m = POMAR & (prox == i) & (dmin < 150.0)
    if m.sum() >= 30:
        P1["v%s" % k] = m
print("P1 valvulas: %d unidades com >=30 celulas" % len(P1))

LADO = 6           # 60 m
P2 = {}
for i0 in range(0, NL, LADO):
    for j0 in range(0, NC, LADO):
        m = np.zeros((NL, NC), bool)
        m[i0:i0 + LADO, j0:j0 + LADO] = True
        m &= POMAR
        if m.sum() >= 20:
            P2["q%02d_%02d" % (i0, j0)] = m
print("P2 quadricula 60 m: %d unidades com >=20 celulas" % len(P2))


def ndvi_unid(m, a, b):
    """Queda de NDVI de a para b na unidade, relativa a queda do pomar."""
    da = float(np.nanmean(nd[b][m]) - np.nanmean(nd[a][m]))
    dp = float(np.nanmean(nd[b][POMAR]) - np.nanmean(nd[a][POMAR]))
    return da - dp


def sar_unid(m, w, orbita=None):
    """VV mediano da unidade no Inverno w, menos o do pomar no mesmo Inverno."""
    sel = inv == w
    if orbita is not None:
        sel = sel & (orb == orbita)
    if sel.sum() < 3:
        return np.nan
    sub = pilha[sel]
    with np.errstate(invalid="ignore"):
        u = np.nanmedian(np.nanmean(sub[:, m], axis=1))
        p = np.nanmedian(np.nanmean(sub[:, POMAR], axis=1))
    return float(u - p)


def corre(P, X, w, orbita=None):
    ks = sorted(P)
    x = np.array([X[k] for k in ks])
    y = np.array([sar_unid(P[k], w, orbita) for k in ks])
    ok = ~(np.isnan(x) | np.isnan(y))
    if ok.sum() < 6:
        return np.nan, np.nan, int(ok.sum())
    r, p = stats.spearmanr(x[ok], y[ok])
    return float(r), float(p), int(ok.sum())


res = {}
for nome_p, P in [("P1 valvulas", P1), ("P2 quadricula 60 m", P2)]:
    print()
    print("=" * 78)
    print("%s — %d unidades" % (nome_p, len(P)))
    print("=" * 78)
    X = {k: ndvi_unid(m, "2024-07-22", "2026-07-27") for k, m in P.items()}
    XP = {k: ndvi_unid(m, "2022-07-31", "2024-07-22") for k, m in P.items()}
    print("  X  = dNDVI 2024->2026 relativa ao pomar   (o evento)")
    print("  X' = dNDVI 2022->2024 relativa ao pomar   (o placebo)")
    print()
    print("  %-10s %22s %22s" % ("Inverno", "X vs VV (rho, p)", "X' vs VV (rho, p)"))
    for w in INVS:
        r, p, n = corre(P, X, w)
        r2, p2, _ = corre(P, XP, w)
        est = "  <<<" if (not np.isnan(p) and p < 0.05 and r > 0) else ""
        print("  %-10s   rho %+.3f  p %7.4f      rho %+.3f  p %7.4f  (n=%d)%s"
              % (w, r, p, r2, p2, n, est))
        res.setdefault(nome_p, {})[w] = dict(rho=r, p=p, rho_placebo=r2,
                                             p_placebo=p2, n=n)

    print()
    print("  --- por orbita, so o Inverno de 2025-26 contra a media dos anteriores ---")
    for o in sorted(set(orb)):
        if (orb == o).sum() < 30:
            continue
        r, p, n = corre(P, X, "2025-26", o)
        ante = [corre(P, X, w, o)[0] for w in INVS if w != "2025-26"]
        ante = [a for a in ante if not np.isnan(a)]
        print("    orbita %3d: 2025-26 rho %+.3f (p=%.4f, n=%d) | "
              "media dos 9 anteriores rho %+.3f (max %+.3f)"
              % (o, r, p, n, np.mean(ante) if ante else np.nan,
                 max(ante) if ante else np.nan))
        res.setdefault(nome_p + "_orbitas", {})[str(o)] = dict(
            rho2526=r, p2526=p, rho_anteriores=float(np.mean(ante)) if ante else None,
            rho_max_anterior=float(max(ante)) if ante else None)

print()
print("=" * 78)
print("A VALVULA 8 DESTACA-SE SOZINHA? (o teste que a C1 pediu)")
print("=" * 78)
print("  Ordenacao das 12 valvulas pela anomalia de VV do Inverno de 2025-26,")
print("  e pela queda de NDVI 2024->2026. Nenhuma das duas conhece os focos.")
ks = sorted(P1, key=lambda k: int(k[1:]))
tab = []
for k in ks:
    m = P1[k]
    ce, cn = E[m].mean(), N[m].mean()
    tab.append(dict(
        valvula=k, n=int(m.sum()),
        d_oeste=float(np.hypot(ce - FOCO_OESTE[0], cn - FOCO_OESTE[1])),
        d_este=float(np.hypot(ce - FOCO_ESTE[0], cn - FOCO_ESTE[1])),
        dndvi=ndvi_unid(m, "2024-07-22", "2026-07-27"),
        vv2526=sar_unid(m, "2025-26"),
        vv_base=float(np.nanmean([sar_unid(m, w) for w in INVS if w != "2025-26"])),
        ndvi26=float(np.nanmean(nd["2026-07-27"][m])),
    ))
for t in tab:
    t["vv_anom"] = t["vv2526"] - t["vv_base"]
print("  %-6s %5s %8s %9s %9s %9s %9s %8s" %
      ("valv", "n", "NDVI26", "dNDVI", "VV 25-26", "VV base", "anomalia", "d.OESTE"))
for t in sorted(tab, key=lambda t: t["vv_anom"]):
    print("  %-6s %5d %8.3f %+9.4f %+9.3f %+9.3f %+9.3f %8.0f"
          % (t["valvula"], t["n"], t["ndvi26"], t["dndvi"], t["vv2526"],
             t["vv_base"], t["vv_anom"], t["d_oeste"]))
res["valvulas"] = tab

x = np.array([t["dndvi"] for t in tab])
y = np.array([t["vv_anom"] for t in tab])
r, p = stats.spearmanr(x, y)
print("\n  Spearman (dNDVI 24->26) x (anomalia de VV 25-26) nas 12 valvulas:"
      "  rho=%+.3f  p=%.4f" % (r, p))
ordem_vv = sorted(tab, key=lambda t: t["vv_anom"])
ordem_nd = sorted(tab, key=lambda t: t["dndvi"])
print("  Valvula com a maior anomalia NEGATIVA de VV: %s" % ordem_vv[0]["valvula"])
print("  Valvula com a maior queda de NDVI:           %s" % ordem_nd[0]["valvula"])
res["spearman_valvulas"] = dict(rho=float(r), p=float(p),
                                pior_vv=ordem_vv[0]["valvula"],
                                pior_ndvi=ordem_nd[0]["valvula"])

json.dump(res, open(os.path.join(SAIDA, "c2_08_cruzamento.json"), "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito c2_08_cruzamento.json")
