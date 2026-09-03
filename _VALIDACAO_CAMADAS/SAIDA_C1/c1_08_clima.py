# -*- coding: utf-8 -*-
"""C1-08 — precipitacao: verificar `pendente_precipitacao.csv` e testar com um
segundo produto.

`pendente_precipitacao.csv` foi produzido com ERA5-Land via Open-Meteo. Repetir
a mesma consulta so testa se o script corre. O instrumento independente aqui e
**outro produto de reanalise**: ERA5 (0,25 grau, modelo global) e, quando
disponivel, CERRA (reanalise regional europeia a 5,5 km, assimilacao propria).
Se dois produtos com nucleos diferentes derem a mesma ordenacao dos Invernos,
a ordenacao e um facto; se divergirem, e artefacto do produto.
"""
import os, sys, json, csv
import numpy as np
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

LAT, LON = 42.047, -8.626
URL = "https://archive-api.open-meteo.com/v1/archive"


def puxa(modelo):
    p = {"latitude": LAT, "longitude": LON, "start_date": "2016-09-01",
         "end_date": "2026-08-20", "daily": "precipitation_sum", "timezone": "UTC"}
    if modelo:
        p["models"] = modelo
    r = requests.get(URL, params=p, timeout=300)
    r.raise_for_status()
    j = r.json()
    d = np.array(j["daily"]["time"], dtype="datetime64[D]")
    v = np.array([x if x is not None else np.nan for x in j["daily"]["precipitation_sum"]], float)
    return d, v


def invernos(d, p):
    out = {}
    for a in range(2016, 2026):
        m = (d >= np.datetime64("%d-10-01" % a)) & (d <= np.datetime64("%d-03-31" % (a + 1)))
        m2 = (d >= np.datetime64("%d-04-01" % (a + 1))) & (d <= np.datetime64("%d-06-15" % (a + 1)))
        out["%d-10 a %d-03" % (a, a + 1)] = (float(np.nansum(p[m])), int(np.nansum(p[m] >= 20)),
                                             float(np.nansum(p[m2])))
    return out


prod = {}
for etiq, mod in (("era5_land", None), ("era5", "era5"), ("cerra", "cerra")):
    try:
        d, p = puxa(mod)
        prod[etiq] = invernos(d, p)
        print("%s: ok (%d dias, %.0f mm no total)" % (etiq, len(d), np.nansum(p)))
    except Exception as e:
        print("%s: indisponivel — %s %s" % (etiq, type(e).__name__, str(e)[:120]))

# ---- comparar com o ficheiro herdado ----
ref = {}
with open(os.path.join(RAIZ, "pendente_precipitacao.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ref[r["inverno"]] = (float(r["precip_out_mar_mm"]), int(r["dias_ge_20mm"]),
                             float(r["precip_abr_15jun_mm"]))

print("\n=== Out-Mar (mm) por produto ===")
cab = "%-18s %10s" % ("inverno", "herdado") + "".join("%12s" % k for k in prod)
print(cab)
difs = {k: [] for k in prod}
ordem = {}
for k in sorted(ref):
    lin = "%-18s %10.1f" % (k, ref[k][0])
    for pr in prod:
        v = prod[pr].get(k, (np.nan,))[0]
        lin += "%12.1f" % v
        if pr == "era5_land":
            difs[pr].append(v - ref[k][0])
        else:
            difs[pr].append(v)
    print(lin)
    ordem[k] = ref[k][0]

if "era5_land" in prod:
    dd = np.array(difs["era5_land"])
    print("\nreproducao do ERA5-Land herdado: dif max %.2f mm, media %.2f mm  => %s"
          % (np.abs(dd).max(), dd.mean(),
             "REPRODUZIDO" if np.abs(dd).max() < 1.0 else "DIVERGE"))

# concordancia de ordenacao entre produtos (Spearman)
from scipy import stats
ks = sorted(ref)
a = np.array([ref[k][0] for k in ks])
for pr in prod:
    if pr == "era5_land":
        continue
    b = np.array([prod[pr][k][0] for k in ks])
    val = b > 0          # CERRA termina em 2021: fora disso devolve zeros
    if val.sum() < len(b):
        print("   (%s so cobre %d dos %d Invernos — comparacao restrita a esses)"
              % (pr, val.sum(), len(b)))
    a_, b_ = a[val], b[val]
    if len(a_) < 3:
        print("   %s: cobertura insuficiente, nao testavel" % pr)
        continue
    a, b, a_guardado = a_, b_, a
    ks_ = [k for k, v in zip(ks, val) if v]
    rs, ps = stats.spearmanr(a, b)
    rp, _ = stats.pearsonr(a, b)
    print("ordenacao ERA5-Land vs %-6s: Spearman %+.3f (p=%.1e) | Pearson %+.3f | vies medio %+.0f mm"
          % (pr, rs, ps, rp, (b - a).mean()))
    print("   Invernos mais secos por %s: %s" % (pr, [ks_[i] for i in np.argsort(b)[:2]]))
    print("   Invernos mais humidos por %s: %s" % (pr, [ks_[i] for i in np.argsort(b)[-2:]]))
    a = a_guardado

print("\nInvernos mais secos (herdado): %s" % [ks[i] for i in np.argsort(a)[:2]])
print("Invernos mais humidos (herdado): %s" % [ks[i] for i in np.argsort(a)[-2:]])

print("\n=== NOTA DE ESCALA ===")
print("Todos estes produtos dao UM valor para o pixel que contem o pomar")
print("(ERA5-Land ~9 km, ERA5 ~28 km, CERRA ~5,5 km). Nenhum distingue o foco")
print("OESTE do foco ESTE: os dois estao a 492 m um do outro, muito abaixo da")
print("resolucao de qualquer um. A precipitacao NAO pode explicar contraste")
print("entre focos; so pode datar anos.")

json.dump({"produtos": prod, "herdado": ref},
          open(os.path.join(SAIDA, "c1_08_precipitacao.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_08_precipitacao.json")
