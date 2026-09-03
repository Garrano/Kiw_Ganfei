# -*- coding: utf-8 -*-
"""C2-03 — a definicao de defice: robustez, e «os dois 8 ha sao o mesmo objecto?»

A curva em U assenta em duas pontas de valor quase igual: 8,08 ha em 2017 e
7,86 ha em 2026. A frase «o pomar melhora seis anos e duplica em dois» so faz
sentido se as duas pontas medirem a mesma coisa. Aqui testa-se isso de tres
maneiras, e testa-se a definicao de defice de duas.

  1. PROFUNDIDADE. O defice e «abaixo da referencia menos 0,05». Um copado por
     fechar e um copado a morrer podem dar a mesma AREA a esse limiar e areas
     completamente diferentes a limiares mais fundos.
  2. LUGAR. Sobreposicao (IoU) entre os mapas de defice de anos diferentes.
     Se 2017 e 2026 nao se sobrepoem, nao ha «recuperacao e recaida»: sao dois
     acontecimentos em sitios diferentes.
  3. FORMA DA DISTRIBUICAO. A area em defice pode crescer porque o pomar todo
     desce (deslocacao) ou porque uma parte se descola (dispersao). Sao
     afirmacoes diferentes e separam-se.

  4. e 5. SENSIBILIDADE ao limiar e ao elemento estruturante da abertura.
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2_00_comum import *  # noqa

masc, _ = carrega_mascaras()
POMAR, REF, NU21 = masc["pomar"], masc["saudavel"], masc["nu2021"] & masc["pomar"]
SERIE = sorted(DATAS + ["2019-09-02"])   # 2019 reposto: ver c2_02 e R2 G10
nd = carrega_ndvi(TODAS)
REFV = {d: float(np.nanmean(nd[d][REF])) for d in TODAS}
res = {}

print("=" * 78)
print("1) PROFUNDIDADE — area em defice por limiar (ha)")
print("=" * 78)
LIM = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
print("%-12s %4s %s" % ("data", "DOY", "".join("%8.2f" % t for t in LIM)))
tab = {}
for d in SERIE:
    v = [mapa_defice(nd[d], POMAR, REFV[d], limiar=t).sum() / 100.0 for t in LIM]
    tab[d] = v
    print("%-12s %4d %s" % (d, doy(d), "".join("%8.2f" % x for x in v)))
res["por_limiar"] = {d: [float(x) for x in v] for d, v in tab.items()}

print("\n  2017 contra 2026, o par que sustenta a curva em U:")
for i, t in enumerate(LIM):
    a, b = tab["2017-07-02"][i], tab["2026-07-27"][i]
    print("    limiar %.2f:  2017 %5.2f ha | 2026 %5.2f ha | racio 2017/2026 %.2f"
          % (t, a, b, a / b if b else float("nan")))
print("\n  E 2024, o minimo:")
for i, t in enumerate(LIM):
    print("    limiar %.2f:  2024 %5.2f ha" % (t, tab["2024-07-22"][i]))

print()
print("=" * 78)
print("2) LUGAR — sobreposicao dos mapas de defice (IoU)")
print("=" * 78)
M = {d: mapa_defice(nd[d], POMAR, REFV[d]) for d in SERIE}


def iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else float("nan")


print("%-12s %s" % ("", "".join("%8s" % d[2:7] for d in SERIE)))
IOU = {}
for a in SERIE:
    row = [iou(M[a], M[b]) for b in SERIE]
    IOU[a] = row
    print("%-12s %s" % (a[:10], "".join("%8.2f" % x for x in row)))
res["iou"] = {a: [float(x) for x in IOU[a]] for a in SERIE}

i17, i26, i24 = SERIE.index("2017-07-02"), SERIE.index("2026-07-27"), SERIE.index("2024-07-22")
print("\n  IoU(2017, 2026) = %.2f   <- as duas pontas da curva em U" % IOU["2017-07-02"][i26])
print("  IoU(2024, 2026) = %.2f   <- o salto" % IOU["2024-07-22"][i26])
print("  IoU(2017, 2024) = %.2f" % IOU["2017-07-02"][i24])
a17, a26 = M["2017-07-02"], M["2026-07-27"]
print("\n  Das %d celulas em defice em 2017, %d (%.0f%%) estao em defice em 2026."
      % (a17.sum(), (a17 & a26).sum(), 100.0 * (a17 & a26).sum() / a17.sum()))
print("  Das %d celulas em defice em 2026, %d (%.0f%%) estavam em defice em 2017."
      % (a26.sum(), (a17 & a26).sum(), 100.0 * (a17 & a26).sum() / a26.sum()))
print("  Celulas em defice em 2026 que NUNCA estiveram em defice de 2017 a 2024: %d (%.2f ha)"
      % ((a26 & ~np.any([M[d] for d in SERIE if d < "2025"], axis=0)).sum(),
         (a26 & ~np.any([M[d] for d in SERIE if d < "2025"], axis=0)).sum() / 100.0))

print("\n  Sobreposicao do defice de 2017 com o chao lavrado de 2021 (nu2021):")
print("    %d das %d celulas de nu2021 (%.0f%%) estavam em defice em 2017."
      % ((a17 & NU21).sum(), NU21.sum(), 100.0 * (a17 & NU21).sum() / NU21.sum()))
print("    contra %.0f%% do pomar em geral." % (100.0 * a17.sum() / POMAR.sum()))

print()
print("=" * 78)
print("3) FORMA — deslocacao ou dispersao?")
print("=" * 78)
print("  Distribuicao de (NDVI - referencia da data) sobre o pomar.")
print("%-12s %8s %8s %8s %8s %8s %9s" %
      ("data", "media", "mediana", "sd", "assim.", "p05", "defice ha"))
forma = {}
for d in SERIE:
    x = nd[d][POMAR] - REFV[d]
    x = x[~np.isnan(x)]
    forma[d] = dict(media=float(x.mean()), mediana=float(np.median(x)),
                    sd=float(x.std()), skew=float(stats.skew(x)),
                    p05=float(np.percentile(x, 5)))
    print("%-12s %8.4f %8.4f %8.4f %8.2f %8.3f %9.2f"
          % (d, x.mean(), np.median(x), x.std(), stats.skew(x),
             np.percentile(x, 5), M[d].sum() / 100.0))
res["forma"] = forma

print("\n  Contrafactual: se de 2024 para 2026 SO a media tivesse mudado")
print("  (mesma forma, deslocada), quanta area estaria em defice?")
x24 = nd["2024-07-22"][POMAR] - REFV["2024-07-22"]
x26 = nd["2026-07-27"][POMAR] - REFV["2026-07-27"]
x24, x26 = x24[~np.isnan(x24)], x26[~np.isnan(x26)]
desl = x24 + (x26.mean() - x24.mean())
print("    observado 2024: %.2f ha | observado 2026: %.2f ha"
      % ((x24 < -0.05).sum() / 100.0, (x26 < -0.05).sum() / 100.0))
print("    2024 deslocado para a media de 2026: %.2f ha" % ((desl < -0.05).sum() / 100.0))
print("    -> a deslocacao explica %.0f%% do aumento; o resto e dispersao."
      % (100.0 * ((desl < -0.05).sum() - (x24 < -0.05).sum())
         / max(1, ((x26 < -0.05).sum() - (x24 < -0.05).sum()))))
res["contrafactual_2024_2026"] = dict(
    obs24=float((x24 < -0.05).sum() / 100.0), obs26=float((x26 < -0.05).sum() / 100.0),
    deslocado=float((desl < -0.05).sum() / 100.0))

print("\n  E o mesmo contrafactual para o ramo 2017 -> 2024:")
x17 = nd["2017-07-02"][POMAR] - REFV["2017-07-02"]
x17 = x17[~np.isnan(x17)]
desl17 = x17 + (x24.mean() - x17.mean())
print("    observado 2017: %.2f ha | observado 2024: %.2f ha"
      % ((x17 < -0.05).sum() / 100.0, (x24 < -0.05).sum() / 100.0))
print("    2017 deslocado para a media de 2024: %.2f ha" % ((desl17 < -0.05).sum() / 100.0))

print()
print("=" * 78)
print("4) SENSIBILIDADE AO ELEMENTO ESTRUTURANTE")
print("=" * 78)
ELEM = [("nenhum", None), ("2x2 (usado)", (2, 2)), ("3x3", (3, 3)),
        ("cruz 3x3", "cruz")]
print("%-12s %s" % ("data", "".join("%14s" % n for n, _ in ELEM)))
sens = {}
for d in SERIE:
    v = []
    for n, e in ELEM:
        if e == "cruz":
            b = ndimage.binary_opening((nd[d] < REFV[d] - LIMIAR) & POMAR,
                                       ndimage.generate_binary_structure(2, 1))
        else:
            b = mapa_defice(nd[d], POMAR, REFV[d], abertura=e)
        v.append(b.sum() / 100.0)
    sens[d] = v
    print("%-12s %s" % (d, "".join("%14.2f" % x for x in v)))
res["por_elemento"] = {d: [float(x) for x in v] for d, v in sens.items()}
print("\n  A curva em U sobrevive a todos? min/max do racio 2026/2024 por elemento:")
for i, (n, _) in enumerate(ELEM):
    print("    %-12s 2017 %5.2f  2024 %5.2f  2026 %5.2f  racio 2026/2024 %.2f"
          % (n, sens["2017-07-02"][i], sens["2024-07-22"][i], sens["2026-07-27"][i],
             sens["2026-07-27"][i] / sens["2024-07-22"][i]))

print()
print("=" * 78)
print("5) A FRACCAO SATURA? (R2 G31)")
print("=" * 78)
ZONA0 = masc["zona0"]
do, de = discos_dos_focos(POMAR)
print("%-12s %10s %10s %10s %12s %12s" %
      ("data", "f ESTE", "f OESTE", "f pomar", "mag ESTE", "mag OESTE"))
for d in SERIE:
    fe = float(np.nanmean(nd[d][de] < REFV[d] - LIMIAR))
    fo = float(np.nanmean(nd[d][do] < REFV[d] - LIMIAR))
    fz = float(np.nanmean(nd[d][ZONA0] < REFV[d] - LIMIAR))
    fp = float(np.nanmean(nd[d][POMAR] < REFV[d] - LIMIAR))
    me = REFV[d] - float(np.nanmean(nd[d][de]))
    mo = REFV[d] - float(np.nanmean(nd[d][do]))
    print("%-12s %9.0f%% %9.0f%% %9.0f%% %12.3f %12.3f"
          % (d, 100 * fe, 100 * fo, 100 * fp, me, mo))
    res.setdefault("fraccoes", {})[d] = dict(este=fe, oeste=fo, zona0=fz, pomar=fp,
                                             mag_este=me, mag_oeste=mo)

json.dump(res, open(os.path.join(SAIDA, "c2_03_defice.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c2_03_defice.json")
