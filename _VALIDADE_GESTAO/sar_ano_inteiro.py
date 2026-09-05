# -*- coding: utf-8 -*-
"""SAR do ANO INTEIRO, agregado em POTENCIA LINEAR, com teste de encharcamento.

O QUE A BUSCA ENCONTROU ANTES DE ESCREVER ISTO
-----------------------------------------------
Feita a 06-09-2026 sobre as tres arvores, por conteudo e nao por nome — porque
o `ja_existe.py` ja falhou nisto uma vez (ordena por frequencia do termo, e o
ficheiro que tinha a resposta era o que menos dizia «sar»).

  · SAR de INVERNO, dez invernos incluindo 2025-26 -> **JA EXISTE**:
    `SAIDA_C1/c1_13_sar_serie.csv`, 441 linhas, escrito a 28-08-2026. **Os
    numeros do inverno em questao estao em disco desde entao.** Isto nao e um
    pre-registo cego: e uma reanalise com desvio declarado.
  · SAR de VERAO ou de ano inteiro -> **NAO EXISTE**. Todos os guioes usam
    janelas de inverno, herdadas sem interrogacao desde o `c1_09`.
  · Agregacao em POTENCIA LINEAR -> **NAO EXISTE**. Todos fazem `nanmean` de dB.
  · Teste de encharcamento/drenagem -> o **metodo** existe (`ganfei_s2/secagem.py`,
    taxa de secagem contra dias-desde-chuva da open-meteo) mas corre sobre as
    mascaras CIRCULARES RETIRADAS (`manchaW = pomar & nd2026 < 0,76`) e para em
    2025-04-30, antes do inverno em causa.

AS TRES CORRECCOES, E PORQUE CADA UMA
--------------------------------------
**1 · Ano inteiro, nao inverno.** A janela de inverno veio do `c1_09` e ninguem
perguntou porque. O SAR nao depende de nuvem nem de luz: nao ha razao para a
restringir. E ha uma razao forte para nao o fazer — **em Janeiro o kiwi nao tem
folha**, logo um numero de inverno nao mede copado: mede estrutura (postes,
arames, cordoes, tronco) e solo. Verao e Inverno respondem a perguntas
diferentes, e o par separa o que esta aberto: **copado ausente com estrutura de
pe e declinio; estrutura tambem ausente e arranque.**

**2 · Potencia linear.** `nanmean` de dB e media geometrica de potencia. O
adversario quantificou o que isso custa: uma unidade que fique mais heterogenea
**sem perder potencia media** produz uma queda aparente de **-0,58 dB** — 49 %
do Delta observado numa orbita e 67 % na outra. E aponta no mesmo sentido da
hipotese, portanto nunca discorda e nenhum controlo o apanha.

Aqui: `10*log10(nanmean(potencia))`. E guarda-se o **desvio-padrao espacial em
dB por unidade e por cena**, para o artefacto de textura ficar diagnosticavel em
vez de silencioso. E o `n_validas`, que o `c1_09` prometia auditar e nao guardava.

**3 · O encharcamento, que e a explicacao concorrente benigna.** O foco oeste e
o ponto mais baixo da exploracao, a 13,4 m da drenagem. **Agua parada da
retrodifusao BAIXA por reflexao especular.** Um inverno humido com encharcamento
ali produz exactamente o padrao observado — sem acontecimento nenhum no pomar.
Testa-se com dias-desde-chuva: se for encharcamento, a anomalia do oeste tem de
**depender da chuva recente**; se for perda de copado, nao tem.

O QUE NAO MUDA
--------------
Orbitas **sempre** em separado — geometrias de vista diferentes tornam gamma0
nao comparavel. Unidades geometricas puras, nenhuma derivada de NDVI.
"""
import csv
import datetime as dt
import io
import json
import os
import sys

import numpy as np
import requests
import rasterio
from rasterio.windows import from_bounds
from concurrent.futures import ThreadPoolExecutor

C1 = r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS/SAIDA_C1"
VG = r"C:/Users/Jackster2/Downloads/_VALIDADE_GESTAO"
sys.path.insert(0, C1)
sys.path.insert(0, r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS")
from c1_00_comum import (AOI, NL, NC, carrega_mascaras, discos_dos_focos,
                         centros_celulas, FOCO_OESTE, FOCO_ESTE)
try:
    from proveniencia import guardar
except ImportError:
    def guardar(d, c, **k):
        json.dump(d, io.open(c, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        return c

SAIDA_CSV = os.path.join(VG, "sar_ano_inteiro.csv")
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")

# ── unidades: geometricas, nenhuma usa NDVI ────────────────────────────────
masc, _ = carrega_mascaras()
pomar, saud, zona0, nu2021 = (masc["pomar"], masc["saudavel"],
                              masc["zona0"], masc["nu2021"])
do, de = discos_dos_focos(pomar)
# o `resto`: o analogo do CONTROLO optico. O `pomar` inteiro NAO serve de nulo
# porque contem os dois focos — seria a forma A.
resto = pomar & ~do & ~de & ~zona0 & ~saud
ALVO = {"referencia": saud, "oeste": do, "este": de, "zona0": zona0,
        "nu2021": nu2021 & pomar, "resto": resto, "pomar": pomar}
for k, v in ALVO.items():
    print("%-12s %5d celulas = %.2f ha" % (k, v.sum(), v.sum() / 100.0))

# ── chuva, para o teste de encharcamento ───────────────────────────────────
print("\na descarregar precipitacao diaria (open-meteo)...")
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": 42.047, "longitude": -8.626,
    "start_date": "2016-09-01", "end_date": "2026-09-05",
    "daily": "precipitation_sum", "timezone": "UTC"}, timeout=180).json()
CHUVA = {dt.date.fromisoformat(d): (p or 0.0)
         for d, p in zip(r["daily"]["time"], r["daily"]["precipitation_sum"])}
print("  %d dias de chuva" % len(CHUVA))


def dias_desde(d, lim=5.0):
    for k in range(0, 31):
        if CHUVA.get(d - dt.timedelta(days=k), 0) >= lim:
            return k
    return 31


def chuva_acum(d, n):
    return sum(CHUVA.get(d - dt.timedelta(days=k), 0) for k in range(n))


# ── catalogo: ANO INTEIRO, dez anos ────────────────────────────────────────
tok = requests.get("https://planetarycomputer.microsoft.com/api/sas/v1/token/"
                   "sentinel-1-rtc", timeout=60).json()["token"]
feats, vistos = [], set()
for ano in range(2016, 2027):
    a, b = "%d-01-01" % ano, "%d-12-31" % ano
    try:
        r = requests.post(
            "https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
                "collections": ["sentinel-1-rtc"],
                "intersects": {"type": "Point", "coordinates": [-8.626, 42.047]},
                "datetime": "%sT00:00:00Z/%sT23:59:59Z" % (a, b), "limit": 500},
            timeout=240).json().get("features", [])
    except Exception as e:
        print("  %d: falhou (%s)" % (ano, type(e).__name__)); continue
    for f in r:
        # DESDUPLICAR por (data, orbita): o c1_13 conta molduras adjacentes da
        # mesma passagem como duas observacoes — 22 e 23 duplicados em 2018-19
        # e 2019-20. Nao sao replicas.
        ch = (f["properties"]["datetime"][:10],
              f["properties"].get("sat:relative_orbit"))
        if ch in vistos:
            continue
        vistos.add(ch)
        feats.append(f)
    print("  %d: %d cenas unicas acumuladas" % (ano, len(feats)))
print("\ncenas Sentinel-1 RTC unicas (data x orbita): %d" % len(feats))

# ── retomar de onde ficou ──────────────────────────────────────────────────
feitas = set()
if os.path.exists(SAIDA_CSV):
    for x in csv.DictReader(io.open(SAIDA_CSV, encoding="utf-8")):
        feitas.add((x["data"], x["orbita"]))
    print("ja em disco: %d" % len(feitas))

COLS = (["data", "orbita", "passagem", "plataforma", "dias_desde_chuva5",
         "chuva_7d_mm", "chuva_30d_mm"] +
        ["%s_%s_%s" % (u, p, s) for u in ALVO for p in ("vv", "vh")
         for s in ("db", "sd", "n")])


def uma(f):
    p = f["properties"]
    d, orb = p["datetime"][:10], str(p.get("sat:relative_orbit"))
    if (d, orb) in feitas:
        return None
    try:
        pot = {}
        for pol in ("vv", "vh"):
            if pol not in f["assets"]:
                return None
            with rasterio.Env(**ENV), \
                    rasterio.open(f["assets"][pol]["href"] + "?" + tok) as ds:
                w = from_bounds(*AOI, transform=ds.transform)
                a = ds.read(1, window=w, out_shape=(NL, NC),
                            resampling=rasterio.enums.Resampling.average
                            ).astype("float64")
            a[a <= 0] = np.nan
            pot[pol] = a                      # POTENCIA linear, nao dB
        dia = dt.date.fromisoformat(d)
        lin = {"data": d, "orbita": orb,
               "passagem": p.get("sat:orbit_state", "")[:10],
               "plataforma": p.get("platform", ""),
               "dias_desde_chuva5": dias_desde(dia),
               "chuva_7d_mm": round(chuva_acum(dia, 7), 1),
               "chuva_30d_mm": round(chuva_acum(dia, 30), 1)}
        for nome, m in ALVO.items():
            for pol in ("vv", "vh"):
                v = pot[pol][m]
                v = v[np.isfinite(v)]
                if v.size < 10:
                    lin["%s_%s_db" % (nome, pol)] = ""
                    lin["%s_%s_sd" % (nome, pol)] = ""
                    lin["%s_%s_n" % (nome, pol)] = 0
                    continue
                # A CORRECCAO: media em POTENCIA, log uma so vez no fim.
                lin["%s_%s_db" % (nome, pol)] = round(
                    float(10 * np.log10(np.mean(v))), 4)
                # e o desvio espacial em dB, para a textura ser diagnosticavel
                lin["%s_%s_sd" % (nome, pol)] = round(
                    float(np.std(10 * np.log10(v), ddof=1)), 4)
                lin["%s_%s_n" % (nome, pol)] = int(v.size)
        return lin
    except Exception:
        return None


novo = [f for f in feats
        if (f["properties"]["datetime"][:10],
            str(f["properties"].get("sat:relative_orbit"))) not in feitas]
print("por processar: %d\n" % len(novo))

escrever_cab = not os.path.exists(SAIDA_CSV)
fh = io.open(SAIDA_CSV, "a", encoding="utf-8", newline="")
w = csv.DictWriter(fh, fieldnames=COLS)
if escrever_cab:
    w.writeheader()

n_ok = 0
with ThreadPoolExecutor(max_workers=8) as ex:
    for i, lin in enumerate(ex.map(uma, novo), 1):
        if lin:
            w.writerow(lin)
            n_ok += 1
            if n_ok % 25 == 0:
                fh.flush()
                print("  %4d/%d  %s orb%s  oeste_vv=%s  ref_vv=%s"
                      % (i, len(novo), lin["data"], lin["orbita"],
                         lin["oeste_vv_db"], lin["referencia_vv_db"]))
fh.close()
print("\nescritas %d cenas novas em sar_ano_inteiro.csv" % n_ok)

guardar({"o_que_faz": "SAR do ano inteiro, potencia linear, com chuva",
         "correcoes": ["ano inteiro em vez de inverno",
                       "10*log10(mean(potencia)) em vez de mean(dB)",
                       "sd espacial em dB e n_validas por unidade e cena",
                       "desduplicacao por (data, orbita)"],
         "unidades": {k: int(v.sum()) for k, v in ALVO.items()},
         "n_cenas_catalogo": len(feats), "n_escritas": n_ok},
        os.path.join(VG, "sar_ano_inteiro.json"))
