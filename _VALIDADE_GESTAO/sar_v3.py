# -*- coding: utf-8 -*-
"""sar_v3.py — a leitura, estritamente contra o CRITERIO_SAR_v3 + ADENDA.

Nao decide nada que o criterio nao tenha decidido antes. Cada constante aqui
tem a sua linha no documento, e o codigo nao contem nenhuma escolha nova.

  formula      contraste = zona0_vv_db - COMPARADOR_vv_db, media anual das cenas
  janela       Nov a Fev, ano hidrologico a comecar a 1 de Setembro
  plataforma   S1A, com acerto .upper()  <- IX-09: o literal esvazia o ano a testar
  comparadores resto E referencia, os dois publicados (alteracao 6)
  orbitas      125, 147 e a media das duas, as tres publicadas (alteracao 3)
  base         n=10 (com o meio-inverno de 2015-16) E n=9, as duas publicadas
  MDE          (t(0,975;n-2) + t(0,80;n-2)) * sd * sqrt(1 + 1/(n-1)), sd so na BASE
  direccao     bilateral
  posto        reportado SEM p, e NUNCA ao lado de um |D| < MDE
  portao       controlo resto-referencia contra o seu MDE, so na base
  modo comum   media das anomalias de nivel de referencia e resto, por orbita,
               limiar 0,5 dB (ASSERIDO, e assinalado como tal)
"""
import csv
import io
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS")
try:
    from proveniencia import guardar
except ImportError:
    def guardar(d, c, **k):
        json.dump(d, io.open(c, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        return c

VG = r"C:/Users/Jackster2/Downloads/_VALIDADE_GESTAO"
CSV = os.path.join(VG, "sar_ano_inteiro_dedup.csv")
INV = (11, 12, 1, 2)
TRAT = 2025                      # ano hidrologico do tratamento
LIM_MODO_COMUM = 0.5             # ASSERIDO — v2 §8.5, sem medicao atras

R = [r for r in csv.DictReader(io.open(CSV, encoding="utf-8"))]
A = [r for r in R if r["plataforma"].upper() == "SENTINEL-1A"]


def f(r, k):
    v = r.get(k, "")
    return float(v) if v not in ("", "nan") else float("nan")


def hy(d):
    a, m = int(d[:4]), int(d[5:7])
    return a if m >= 9 else a - 1


def serie(col_a, col_b, orb):
    """Media anual do contraste col_a - col_b. orb='media' junta as duas."""
    por = {}
    for r in A:
        if int(r["data"][5:7]) not in INV:
            continue
        if orb != "media" and r["orbita"] != orb:
            continue
        v = f(r, col_a) - (f(r, col_b) if col_b else 0.0)
        if v == v:
            por.setdefault((hy(r["data"]), r["orbita"]), []).append(v)
    if orb == "media":
        ano = {}
        for (h, o), v in por.items():
            ano.setdefault(h, []).append(np.mean(v))
        return {h: float(np.mean(v)) for h, v in ano.items() if len(v) == 2}
    return {h: float(np.mean(v)) for (h, o), v in por.items()}


def mde(sd, n):
    return float((stats.t.ppf(0.975, n - 2) + stats.t.ppf(0.80, n - 2))
                 * sd * np.sqrt(1 + 1.0 / (n - 1)))


def celula(comp, orb, base_min):
    s = serie("zona0_vv_db", "%s_vv_db" % comp, orb)
    base = {h: v for h, v in s.items() if h < TRAT and h >= base_min}
    if TRAT not in s or len(base) < 5:
        return None
    y = np.array([base[h] for h in sorted(base)])
    n = len(y)
    d = s[TRAT] - y.mean()
    m = mde(y.std(ddof=1), n)
    todos = sorted(list(y) + [s[TRAT]])
    posto = todos.index(s[TRAT]) + 1
    return dict(comparador=comp, orbita=orb, n_base=n,
                contraste_trat=round(s[TRAT], 4),
                media_base=round(float(y.mean()), 4),
                sd_base=round(float(y.std(ddof=1)), 4),
                delta=round(float(d), 4), mde=round(m, 4),
                distingue=bool(abs(d) >= m),
                posto=posto, de=len(todos))


print("=" * 78)
print("LEITURA v3 — SAR, inverno, VV, S1A, zona0")
print("=" * 78)
print("cenas S1A no ficheiro: %d   (acerto .upper(), IX-09)" % len(A))

# ── o portão de abortar, ANTES de tudo ──────────────────────────────────────
print()
print("PORTAO DE ABORTAR — o controlo contra o seu proprio MDE, nas DUAS bases")
# D2: a adenda §2 manda "mesma formula e mesmo n para as seis celulas E para o
# controlo", e a §4 manda publicar as duas bases. A versao anterior fixava n=10
# aqui e no modo comum — e o modo comum e a UNICA estatistica calculada sobre
# NIVEIS, onde um meio-inverno sem Nov nem Dez nao se cancela.
portao, abortar = {}, False
for orb, bmin in [(o, b) for o in ("125", "147", "media") for b in (2015, 2016)]:
    s = serie("resto_vv_db", "referencia_vv_db", orb)
    base = np.array([s[h] for h in sorted(s) if h < TRAT and h >= bmin])
    d = s[TRAT] - base.mean()
    m = mde(base.std(ddof=1), len(base))
    ok = abs(d) < m
    abortar = abortar or not ok
    portao["%s_n%d" % (orb, len(base))] = dict(
        delta=round(float(d), 4), mde=round(m, 4), n_base=len(base), passa=bool(ok))
    print("   orb%-6s n=%2d  D=%+.3f   MDE=%.2f   %s" %
          (orb, len(base), d, m, "passa" if ok else "*** ABORTA ***"))

if abortar:
    # D1, apanhado pelo adversario do resultado: a versao anterior punha
    # `abortar = True` e NUNCA a lia. Forma B — um teste que nao podia falhar,
    # dentro do elemento retomado para fechar exactamente essa forma.
    guardar({"abortado": True, "portao": portao,
             "razao": "o contraste de controlo excede o seu proprio MDE no ano "
                      "de tratamento: o que se ve e o ano, nao a unidade"},
            os.path.join(VG, "sar_v3.json"))
    raise SystemExit("*** LEITURA ABORTADA pelo portao do §5. Nada foi lido. ***")

# ── modo comum ──────────────────────────────────────────────────────────────
print()
print("MODO COMUM — media das anomalias de NIVEL de referencia e resto (a zona0 sai)")
modo = {}
for orb, bmin in [(o, b) for o in ("125", "147") for b in (2015, 2016)]:
    an, niv = [], {}
    for u in ("referencia", "resto"):
        s = serie("%s_vv_db" % u, None, orb)
        base = np.array([s[h] for h in sorted(s) if h < TRAT and h >= bmin])
        an.append(s[TRAT] - base.mean())
        # D4: a §5 mandava publicar os NIVEIS ABSOLUTOS e nao estavam em lado nenhum
        niv[u] = dict(tratamento=round(s[TRAT], 3),
                      media_base=round(float(base.mean()), 3), n_base=len(base))
    mc = float(np.mean(an))
    k = "%s_n%d" % (orb, niv["resto"]["n_base"])
    modo[k] = dict(anomalia_referencia=round(an[0], 3),
                   anomalia_resto=round(an[1], 3), comum=round(mc, 3),
                   niveis_absolutos=niv,
                   dispara=bool(abs(mc) >= LIM_MODO_COMUM))
    print("   orb%-4s n=%2d  referencia %+.3f   resto %+.3f   COMUM %+.3f   %s" %
          (orb, niv["resto"]["n_base"], an[0], an[1], mc,
           "*** DISPARA (>= 0,5) ***" if abs(mc) >= LIM_MODO_COMUM else "abaixo de 0,5"))

# ── as seis células, nas duas bases ─────────────────────────────────────────
saida = {"portao": portao, "modo_comum": modo, "celulas": []}
for base_min, rot in ((2015, "n=10 (com o meio-inverno de 2015-16)"),
                      (2016, "n=9 (sem o meio-inverno)")):
    print()
    print("-" * 78)
    print("BASE %s" % rot)
    print("-" * 78)
    print("%-12s %-6s %2s %9s %8s %8s %-11s %s"
          % ("comparador", "orb", "n", "D", "MDE", "sd", "distingue", "posto"))
    for comp in ("resto", "referencia"):
        for orb in ("125", "147", "media"):
            c = celula(comp, orb, base_min)
            if not c:
                continue
            c["base"] = rot
            # D3: a adenda §1 proibe o posto ao lado de um |D| < MDE, e a versao
            # anterior suprimia-o no ecra e escrevia-o no JSON — que e o
            # artefacto duravel. A porta fechada em prosa ficava aberta no ficheiro.
            if not c["distingue"]:
                c["posto"] = None
                c["posto_suprimido"] = "adenda §1: |D| < MDE"
            saida["celulas"].append(c)
            # a proibicao da adenda §1: o posto NAO acompanha um |D| < MDE
            po = ("%d de %d" % (c["posto"], c["de"])) if c["distingue"] else "—"
            print("%-12s %-6s %2d %+9.3f %8.2f %8.3f %-11s %s"
                  % (comp, orb, c["n_base"], c["delta"], c["mde"], c["sd_base"],
                     "SIM" if c["distingue"] else "nao", po))

guardar({"criterio": "CRITERIO_SAR_v3.md + CRITERIO_SAR_v3_ADENDA.md",
         "limiar_modo_comum_ASSERIDO": LIM_MODO_COMUM, **saida},
        os.path.join(VG, "sar_v3.json"))
print()
print("escrito sar_v3.json")
