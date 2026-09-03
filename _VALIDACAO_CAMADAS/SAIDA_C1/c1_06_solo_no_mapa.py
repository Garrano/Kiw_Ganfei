# -*- coding: utf-8 -*-
"""C1-06 — pôr a quimica do solo no mapa, pela primeira vez.

Ate a R2 G35 os boletins A2 so tinham codigo de bloco. Com as valvulas 6-17
colocadas por area acumulada, os blocos da banda contigua passam a ter
posicao. Este script:
  1. le a folha "Soil Chemistry by Block" e converte os textos em numeros;
  2. liga cada boletim a uma posicao, declarando o nivel de confianca;
  3. mede a distancia de cada boletim a cada um dos dois focos (R2 G34);
  4. cruza a quimica com a cota do MDT (C1-03).
"""
import os, sys, json, re
import numpy as np
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

XLSX = r"C:\Users\Jackster2\Downloads\Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx"
V = valvulas()
BLOCO_VALV = {}
for k, v in V.items():
    BLOCO_VALV.setdefault(v["bloco"], []).append(int(k))
print("blocos da banda contigua (R2 G35):")
for b, vs in sorted(BLOCO_VALV.items()):
    a = sum(V[str(x)]["area_m2"] for x in vs)
    print("  %-10s valvulas %-16s %6.2f ha  E%.0f..%.0f"
          % (b, sorted(vs), a / 1e4,
             min(V[str(x)]["E"] for x in vs), max(V[str(x)]["E"] for x in vs)))
tot = sum(v["area_m2"] for v in V.values())
print("  TOTAL banda: %.2f ha  (R2 G35 declara 27,30 ha)" % (tot / 1e4))

# ------- colocacao declarada, com confianca -------
# B1 fica fora da banda: R2 G36 da-lhe as duas pontas, E529500 N4654010 a
# E530054 N4654413. Dentro do B1 nao se sabe onde acaba cada valvula.
B1_A, B1_B = (529500.0, 4654010.0), (530054.0, 4654413.0)
B1_C = ((B1_A[0] + B1_B[0]) / 2, (B1_A[1] + B1_B[1]) / 2)

COLOCACAO = {
 "Erica 2016 R (2026-03-03)": dict(bloco="Erica Novo", valvulas=[10, 11],
    conf="INFERIDA", nota="'Erica 2016' identificado com o bloco 'Erica Novo' da tabela de valvulas; sub-bloco R sem posicao"),
 "Erica 2016 E (2026-03-03)": dict(bloco="Erica Novo", valvulas=[10, 11],
    conf="INFERIDA", nota="idem; o sufixo E reaparece no boletim de nematodes 343 ('Erica Novo E'), o que reforca a identificacao mas nao a prova"),
 "B2 - V7 (2026-03-03)": dict(bloco="B2", valvulas=[7],
    conf="CONFIRMADA", nota="numero de valvula explicito no boletim"),
 "B3 - 7 ha (2026-03-03)": dict(bloco="B3", valvulas=[12, 13, 14, 15],
    conf="CONFIRMADA-BLOCO", nota="bloco explicito; ponto dentro do bloco desconhecido. Atencao: a tabela da 9,01 ha ao B3 da banda, o boletim diz 7 ha"),
 "B2 - Zona 1 (V7) (2026-06-17)": dict(bloco="B2", valvulas=[7],
    conf="CONFIRMADA", nota="mesma valvula que o de Marco; textura discordante"),
 "B1 C1 (2026-07-08)": dict(bloco="B1", valvulas=[], conf="FORA DA BANDA",
    nota="B1 tem posicao de conjunto (R2 G36) mas as sub-parcelas C1/C3/C4 nao"),
 "B1 C3 (2026-07-08)": dict(bloco="B1", valvulas=[], conf="FORA DA BANDA", nota="idem"),
 "B1 C4 (2026-07-08)": dict(bloco="B1", valvulas=[], conf="FORA DA BANDA", nota="idem"),
 "Parcela B4 (2026-07-08)": dict(bloco="B4", valvulas=[16, 17], conf="AMBIGUA",
    nota="B4 tem valvulas 16-17 na banda E a parcela solta B4C3 sem posicao; o boletim nao distingue"),
}

def num(s):
    """extrai o valor numerico de celulas como '<154 mg/kg CaO (Muito baixo)'."""
    if s is None:
        return np.nan, ""
    t = str(s)
    if t.startswith("n/a"):
        return np.nan, "nao extraido"
    m = re.search(r"(<?)\s*(\d+(?:[.,]\d+)?)", t)
    if not m:
        return np.nan, t
    v = float(m.group(2).replace(",", "."))
    return v, ("censurado <" if m.group(1) else "")

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb["Soil Chemistry by Block"]
linhas = list(ws.iter_rows(values_only=True))
cabec = linhas[0]
amostras = list(cabec[1:])
dados = {}
for lin in linhas[1:]:
    dados[str(lin[0])] = list(lin[1:])

g = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))
masc, _ = carrega_mascaras()
E29, N29 = centros_celulas()

def cota_em(e, n, raio=40.0):
    d = (E29 - e) ** 2 + (N29 - n) ** 2
    m = (d <= raio ** 2) & masc["pomar"]
    return float(np.nanmedian(g["cota"][m])) if m.sum() else np.nan

print("\n=== boletins A2 colocados ===")
saida = []
for a in amostras:
    c = COLOCACAO[a]
    vs = c["valvulas"]
    if vs:
        e = float(np.mean([V[str(x)]["E"] for x in vs]))
        n = float(np.mean([V[str(x)]["N"] for x in vs]))
        raio = 0.0 if len(vs) == 1 else float(max(
            np.hypot(V[str(x)]["E"] - e, V[str(x)]["N"] - n) for x in vs))
    elif c["bloco"] == "B1":
        e, n = B1_C; raio = np.hypot(B1_B[0] - B1_A[0], B1_B[1] - B1_A[1]) / 2
    else:
        e = n = np.nan; raio = np.nan
    do_ = np.hypot(e - FOCO_OESTE[0], n - FOCO_OESTE[1])
    de_ = np.hypot(e - FOCO_ESTE[0], n - FOCO_ESTE[1])
    ph, _ = num(dados["pH (H2O)"][amostras.index(a)])
    cao, cflag = num(dados["Cálcio (CaO)"][amostras.index(a)])
    mgo, _ = num(dados["Magnésio (MgO)"][amostras.index(a)])
    p2o5, _ = num(dados["Fósforo (P2O5)"][amostras.index(a)])
    k2o, _ = num(dados["Potássio (K2O)"][amostras.index(a)])
    mo, _ = num(dados["Matéria Orgânica (MO)"][amostras.index(a)])
    cn, _ = num(dados["Razão C:N"][amostras.index(a)])
    tex = str(dados["Textura"][amostras.index(a)])
    r = dict(amostra=a, bloco=c["bloco"], valvulas=vs, confianca=c["conf"],
             nota=c["nota"], E=None if np.isnan(e) else round(e, 1),
             N=None if np.isnan(n) else round(n, 1),
             raio_incerteza_m=None if np.isnan(raio) else round(raio, 0),
             dist_foco_oeste_m=None if np.isnan(do_) else round(do_, 0),
             dist_foco_este_m=None if np.isnan(de_) else round(de_, 0),
             pH=ph, CaO=cao, CaO_censurado=bool(cflag), MgO=mgo, P2O5=p2o5,
             K2O=k2o, MO_pct=mo, CN=cn, textura=tex,
             cota_mdt_m=None if np.isnan(e) else cota_em(e, n))
    saida.append(r)
    print("%-30s %-11s %-15s pH %.1f  CaO %6s  MgO %5.1f  MO %.1f%%  C:N %4.1f  %-13s"
          % (a[:30], c["bloco"], c["conf"], ph,
             ("<%d" % cao) if cflag else ("%d" % cao if not np.isnan(cao) else "n/a"),
             mgo, mo, cn, tex.split(" ")[0]))
    print("%32s d(OESTE)=%s m  d(ESTE)=%s m  cota=%s m  raio=%s m" %
          ("", r["dist_foco_oeste_m"], r["dist_foco_este_m"],
           None if r["cota_mdt_m"] is None or (isinstance(r["cota_mdt_m"], float) and np.isnan(r["cota_mdt_m"])) else round(r["cota_mdt_m"], 2),
           r["raio_incerteza_m"]))

# ---- qual e o boletim mais proximo de cada foco? ----
print("\n=== o que ha de quimica em cada foco ===")
for nome, dk in (("FOCO OESTE", "dist_foco_oeste_m"), ("FOCO ESTE", "dist_foco_este_m")):
    cand = [r for r in saida if r[dk] is not None]
    cand.sort(key=lambda r: r[dk])
    print("%s: mais proximo = %s (%s), a %d m" % (nome, cand[0]["amostra"], cand[0]["confianca"], cand[0][dk]))
    for r in cand[:3]:
        print("    %-30s %5d m  pH %.1f  CaO %s  MgO %.1f" %
              (r["amostra"][:30], r[dk], r["pH"],
               ("<%d" % r["CaO"]) if r["CaO_censurado"] else "%d" % r["CaO"], r["MgO"]))

# o foco ESTE cai dentro de que bloco?
for nome, foco in (("FOCO OESTE", FOCO_OESTE), ("FOCO ESTE", FOCO_ESTE)):
    dists = {int(k): np.hypot(v["E"] - foco[0], v["N"] - foco[1]) for k, v in V.items()}
    perto = sorted(dists.items(), key=lambda kv: kv[1])[:3]
    print("%s: valvulas mais proximas %s"
          % (nome, ["v%d (%s) %.0f m" % (k, V[str(k)]["bloco"], d) for k, d in perto]))

# ---- contraste quimico entre os blocos dos dois focos ----
b2 = [r for r in saida if r["bloco"] == "B2"]
b3 = [r for r in saida if r["bloco"] == "B3"]
print("\n=== bloco do foco OESTE (B2, v7) contra bloco do foco ESTE (B3) ===")
for campo in ("pH", "CaO", "MgO", "P2O5", "K2O", "MO_pct", "CN"):
    v2 = [r[campo] for r in b2]; v3 = [r[campo] for r in b3]
    print("  %-7s B2: %-16s | B3: %s" % (campo, ", ".join("%.4g" % x for x in v2),
                                          ", ".join("%.4g" % x for x in v3)))

# ---- amplitude da holding, e onde caem os extremos ----
cao_all = [(r["CaO"], r["amostra"], r["bloco"], r["CaO_censurado"]) for r in saida]
cao_all.sort()
print("\nCaO em todo o conjunto (mg/kg): %s ... %s"
      % ("<%d (%s)" % (cao_all[0][0], cao_all[0][2]), "%d (%s)" % (cao_all[-1][0], cao_all[-1][2])))
print("ordem crescente:", ", ".join("%s%d %s" % ("<" if c else "", v, b) for v, a, b, c in cao_all))

json.dump(saida, open(os.path.join(SAIDA, "c1_06_solo_colocado.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
import csv
with open(os.path.join(SAIDA, "c1_06_solo_colocado.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0].keys()))
    w.writeheader()
    for r in saida:
        w.writerow({k: (v if not isinstance(v, list) else "|".join(map(str, v))) for k, v in r.items()})
print("\nescrito c1_06_solo_colocado.json/.csv")
