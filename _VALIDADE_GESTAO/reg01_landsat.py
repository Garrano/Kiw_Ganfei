# -*- coding: utf-8 -*-
"""REG-01 · LANDSAT — a repetição da comparação regional com o segundo instrumento.

PORQUE ESTE FICHEIRO EXISTE
---------------------------
A REG-01 correu em Sentinel-2 e deu um resultado grande: cinco blocos de kiwi de
outra exploração (ENT 297313) com degrau de −0,21 a −0,40, duas a quatro vezes
pior do que os focos de Ganfei. **Um instrumento só.** Pelo controlo 1 do
`CONTROLOS.md` isso é NÃO TESTÁVEL, e o `guarda.py` bloqueou o veredicto causal.
Isto é a acção 1 da fila: dar-lhe o segundo instrumento.

NOTA DE 1 DE SETEMBRO DE 2026 — o parágrafo acima diz «duas a quatro vezes
pior do que os focos de Ganfei» e isso, tal como está, atribui o acontecimento
errado. O censo do ano da quebra (REG-01 S2, `quebra_ano`) mostra que os cinco
blocos do ENT 297313 quebram em **2024**, não em 2025-26: são um acontecimento
diferente, um ano antes e maior. O degrau é média(2025-26) menos média(2017-24),
por isso um colapso em 2024 entra na própria linha de base, dilui-se, e ainda
assim encabeça a tabela. O que este ficheiro replica é a MEDIÇÃO — e replica bem
(R1 5/5, rho = 0,89) — não a atribuição. Ver
`REGISTO_REG01_GUARDA_2026-09-01.md` §2 e §6.

Landsat 8/9 é independente por construção: outra agência (USGS/NASA), outro
sensor (OLI/OLI-2), outra correcção atmosférica (LaSRC, não Sen2Cor), outra
órbita e outra hora de passagem. Partilha com o Sentinel-2 apenas o princípio
físico. Preço: 30 m em vez de 10.

CRITÉRIOS DE REPLICAÇÃO, FIXADOS ANTES DE CORRER
------------------------------------------------
    R1 · OS CINCO. Os cinco blocos do ENT 297313 que o S2 põe no fundo
         (6705427, 6705429, 6705428, 6705432, 6705442) têm de aparecer entre os
         OITO piores dos 38 também no Landsat — pelo menos quatro deles. Se se
         espalharem pelo meio da distribuição, o resultado do S2 NÃO replica e a
         REG-01 reabre.

    R2 · A ORDEM. Correlação de Spearman entre o degrau do S2 e o do Landsat,
         nos blocos comuns, >= 0,50. Abaixo disso os dois instrumentos não
         concordam na ordenação e nenhum número regional pode circular.

    R3 · GANFEI. Os focos de Ganfei ficam ACIMA do percentil 10 — a mesma
         conclusão do S2, medida no outro instrumento.

    Falsificação: R1 é a condição principal. Se falhar, este ficheiro escreve
    que o resultado do S2 não replica, e não se procura reconciliação.

O QUE O S2 E O LANDSAT NÃO PARTILHAM, E É DE PROPÓSITO
-------------------------------------------------------
As CENAS. O S2 usou nove datas escolhidas; aqui usam-se TODAS as cenas Landsat
8/9 de Junho a Setembro com nuvem < 40 %, 2017-2026, e a média por período. Se
o resultado dependesse da escolha das nove datas, isto apanha-o.

O QUE É COMUM, E TEM DE SER
---------------------------
As FRONTEIRAS: os mesmos polígonos do parcelário do IFAP, sem re-selecção.
A ESTATÍSTICA: degrau = média do desvio à mediana regional em 2025-26 menos a
média em 2017-2024. Idêntica à do S2.

O N, QUE DESTA VEZ SAI IMPRESSO
-------------------------------
`landsat_independente.py` tinha um cabeçalho a prometer «só píxeis inteiramente
dentro da unidade, e reporta-se o n» e um código que não fazia nem uma coisa
nem outra. Aqui:

  · trabalha-se numa grelha de **30 m**, não numa de 10 m com cada píxel
    repetido nove vezes;
  · n = células de 30 m com centro dentro do bloco, **impresso por bloco**;
  · blocos com n < 6 (0,54 ha) não entram — declarado antes de correr.

E mesmo assim: essas células são da NOSSA grelha, não os píxeis nativos do
Landsat. A reamostragem por vizinho mais próximo alinha-os; um píxel nativo
pode cair em duas células ou em nenhuma. **O n impresso é um limite superior do
número de observações independentes.** Diz-se, não se dilui.
"""
import json
import os

import numpy as np
import planetary_computer as pc
import pystac_client
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject, transform_bounds
from rasterio.windows import from_bounds
from shapely.geometry import shape
from shapely.ops import transform as sht
from pyproj import Transformer
from matplotlib.path import Path as MP
from scipy.stats import spearmanr

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CACHE = os.path.join(VG, "_reg01_landsat_cache")
os.makedirs(CACHE, exist_ok=True)

ENT_POMAR = 472062
OS_CINCO = {6705427, 6705429, 6705428, 6705432, 6705442}
PASSO = 30.0
N_MIN = 6

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para_utm = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)

# ---------------------------------------------- os MESMOS blocos, sem escolher
S2R = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                     encoding="utf-8"))
DEG_S2 = {int(b["cul"]): b["degrau"] for b in S2R["blocos"]}

K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K

# --- guarda de cultura -------------------------------------------------------
# Este script confia no NOME do ficheiro para saber que os blocos sao kiwi. O
# filtro real vive noutro sitio (SAIDA_H2_patologista/03_ifap_largo.py, linha
# `PUN_CUL_COD != "124" -> salta`). Se esse ficheiro for regerado com outro
# filtro, nada aqui daria por isso -- e o mesmo modo de falha do cabecalho de
# `fazer_masks_v2.py`. Verifica-se o codigo declarado, poligono a poligono.
_maus = sorted({str(f["properties"].get("PUN_CUL_COD")) for f in KF} - {"124"})
if _maus:
    raise SystemExit(
        "ifap_kiwi_largo.json contem culturas nao-kiwi: %s. Esperado so "
        "PUN_CUL_COD 124 (KIWI). Regerar com 03_ifap_largo.py." % ", ".join(_maus))
_camp = sorted({str(f["properties"].get("CUL_CAMPANHA")) for f in KF})
print("guarda de cultura: %d poligonos, todos PUN_CUL_COD 124 (KIWI), "
      "campanha(s) %s" % (len(KF), "/".join(_camp)))
print("  RESSALVA: a declaracao do IFAP cobre so a(s) campanha(s) acima. A "
      "continuidade da cultura ao longo da linha de base NAO esta verificada;")
print("  um bloco arrancado ou replantado a meio da serie produz um degrau que "
      "nao e sintoma. Ver REGISTO_REG01_GUARDA_2026-09-01.md.")
P = json.load(open(os.path.join(H2, "ifap_parcelas_largo.json"), encoding="utf-8"))
PF = P["features"] if isinstance(P, dict) else P
parc = []
for ft in PF:
    try:
        parc.append((para_utm(shape(ft["geometry"])).buffer(0),
                     ft["properties"].get("ENT_ID")))
    except Exception:
        pass

BLOCOS = []
for ft in KF:
    cul = ft["properties"].get("CUL_ID")
    if cul is None or int(cul) not in DEG_S2:
        continue
    g = para_utm(shape(ft["geometry"])).buffer(0)
    c = g.centroid
    dono = None
    for pg, e in parc:
        if pg.contains(c):
            dono = e
            break
    BLOCOS.append(dict(cul=int(cul), geom=g, ha=g.area / 1e4, ent=dono,
                       E=c.x, N=c.y))
print("blocos herdados do S2 (sem re-seleccao): %d" % len(BLOCOS))

xs = [b["E"] for b in BLOCOS]
ys = [b["N"] for b in BLOCOS]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)
NC = int((BB[2] - BB[0]) / PASSO)
NL = int((BB[3] - BB[1]) / PASSO)
DEST = from_origin(BB[0], BB[3], PASSO, PASSO)
print("grelha regional a 30 m: %d x %d celulas" % (NC, NL))

EE, NN = np.meshgrid(BB[0] + (np.arange(NC) + .5) * PASSO,
                     BB[3] - (np.arange(NL) + .5) * PASSO)
pts = np.column_stack([EE.ravel(), NN.ravel()])
for b in BLOCOS:
    ext = list(b["geom"].exterior.coords)
    b["mask"] = MP(np.array(ext)).contains_points(pts).reshape(NL, NC)
    b["n"] = int(b["mask"].sum())

caidos = [b for b in BLOCOS if b["n"] < N_MIN]
BLOCOS = [b for b in BLOCOS if b["n"] >= N_MIN]
print("blocos com n >= %d celulas de 30 m: %d   (caem %d: %s)"
      % (N_MIN, len(BLOCOS), len(caidos),
         ", ".join("%d n=%d" % (b["cul"], b["n"]) for b in caidos) or "nenhum"))
falta = OS_CINCO - {b["cul"] for b in BLOCOS}
if falta:
    print("AVISO: dos cinco do 297313 caem por n pequeno: %s" % sorted(falta))

# ----------------------------------------------------------------- as cenas
cat = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace)
lo, la = tr.transform(BB[0], BB[1], direction="INVERSE")
lo2, la2 = tr.transform(BB[2], BB[3], direction="INVERSE")
itens = list(cat.search(collections=["landsat-c2-l2"], bbox=[lo, la, lo2, la2],
                        datetime="2017-01-01/2026-12-31",
                        query={"eo:cloud_cover": {"lt": 40},
                               "platform": {"in": ["landsat-8", "landsat-9"]}}
                        ).items())
itens = [i for i in itens if 6 <= i.datetime.month <= 9]
itens.sort(key=lambda i: i.datetime)
print("cenas Landsat 8/9, Jun-Set, nuvem < 40 %%, 2017-2026: %d" % len(itens))

_bc = {}


def _bnd(crs):
    k = str(crs)
    if k not in _bc:
        _bc[k] = transform_bounds("EPSG:32629", crs, *BB)
    return _bc[k]


def le(item, chave):
    a = item.assets[chave]
    with rasterio.open(a.href) as ds:
        w = from_bounds(*_bnd(ds.crs), transform=ds.transform)
        arr = ds.read(1, window=w).astype("float32")
        out = np.full((NL, NC), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(w), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=RS.nearest)
    return out


esc = lambda a: a * 0.0000275 - 0.2
serie = []          # uma linha por cena valida
print()
for k, it in enumerate(itens):
    d = it.datetime.strftime("%Y-%m-%d")
    cv = os.path.join(CACHE, "%s_%s.npz" % (d, it.id[-8:]))
    try:
        if os.path.exists(cv):
            z = np.load(cv)
            ndvi, ndmi = z["ndvi"], z["ndmi"]
        else:
            qa = le(it, "qa_pixel")
            q = qa.astype("int32")
            limpo = np.isfinite(qa) & ((q & 0b11000) == 0) & ((q & 0b10) == 0)
            if limpo.mean() < 0.60:      # criterio a priori: 60 % da regiao limpa
                print("  %s  nuvem/sombra em %.0f %% da regiao — cai"
                      % (d, 100 * (1 - limpo.mean())))
                continue
            red, nir = esc(le(it, "red")), esc(le(it, "nir08"))
            sw1 = esc(le(it, "swir16"))
            ndvi = np.where(limpo, (nir - red) / (nir + red + 1e-9), np.nan)
            ndmi = np.where(limpo, (nir - sw1) / (nir + sw1 + 1e-9), np.nan)
            np.savez_compressed(cv, ndvi=ndvi.astype("float32"),
                                ndmi=ndmi.astype("float32"))
    except Exception as e:
        print("  %s  ERRO %s" % (d, type(e).__name__))
        continue
    linha = {"data": d, "plat": it.properties.get("platform"), "v": {}, "w": {}}
    for b in BLOCOS:
        a1, a2 = ndvi[b["mask"]], ndmi[b["mask"]]
        a1, a2 = a1[np.isfinite(a1)], a2[np.isfinite(a2)]
        if a1.size >= max(3, 0.5 * b["n"]):
            linha["v"][b["cul"]] = float(np.median(a1))
            linha["w"][b["cul"]] = float(np.median(a2))
    if len(linha["v"]) >= 0.7 * len(BLOCOS):
        serie.append(linha)
    if (k + 1) % 25 == 0:
        print("  %d/%d cenas, %d validas" % (k + 1, len(itens), len(serie)))

print("cenas validas: %d   (2017-24: %d · 2025-26: %d)"
      % (len(serie), sum(1 for r in serie if r["data"] < "2025"),
         sum(1 for r in serie if r["data"] >= "2025")))
json.dump([{k: r[k] for k in ("data", "plat")} for r in serie],
          open(os.path.join(VG, "reg01_landsat_cenas.json"), "w"), indent=1)

# ----------------------------------------------------------------- a medida
def degraus_de(chave):
    out = {}
    devs = {b["cul"]: {"pre": [], "pos": []} for b in BLOCOS}
    for r in serie:
        vals = r[chave]
        med = np.median(list(vals.values()))
        alvo = "pos" if r["data"] >= "2025" else "pre"
        for cul, v in vals.items():
            devs[cul][alvo].append(v - med)
    for cul, dd in devs.items():
        if len(dd["pre"]) >= 5 and len(dd["pos"]) >= 2:
            out[cul] = float(np.mean(dd["pos"]) - np.mean(dd["pre"]))
    return out


DEG_L = degraus_de("v")
DEG_LM = degraus_de("w")
print("blocos com degrau Landsat calculavel: %d" % len(DEG_L))

comuns = sorted(set(DEG_L) & set(DEG_S2))
gl = np.array([DEG_L[c] for c in comuns])
gs = np.array([DEG_S2[c] for c in comuns])
rho, pv = spearmanr(gs, gl)

info = {b["cul"]: b for b in BLOCOS}
ordem = sorted(DEG_L, key=lambda c: DEG_L[c])
pos = {c: i for i, c in enumerate(ordem)}

print()
print("=" * 96)
print("REG-01 · LANDSAT — a distribuicao regional do degrau (NDVI)")
print("=" * 96)
print()
print("%-10s %8s %6s %5s %10s %10s %11s %s"
      % ("CUL_ID", "ENT", "ha", "n30", "degrau L", "degrau S2", "percentil", ""))
for c in ordem:
    b = info[c]
    pct = 100.0 * (pos[c] + 1) / len(ordem)
    marca = ""
    if c in OS_CINCO:
        marca = "  <== um dos cinco"
    elif b["ent"] == ENT_POMAR:
        marca = "  <-- a exploracao"
    print("%-10d %8s %6.2f %5d %+10.4f %+10.4f %10.0f %%%s"
          % (c, b["ent"], b["ha"], b["n"], DEG_L[c],
             DEG_S2.get(c, float("nan")), pct, marca))

print()
print("=" * 96)
print("OS CRITERIOS, julgados pelo que estava escrito antes de correr")
print("=" * 96)
dentro = [c for c in OS_CINCO if c in pos and pos[c] < 8]
print()
print("R1 · dos cinco do 297313, %d de %d estao entre os OITO piores do Landsat"
      % (len(dentro), len([c for c in OS_CINCO if c in pos])))
for c in sorted(OS_CINCO):
    if c in pos:
        print("     %d  lugar %d de %d  (degrau %+.4f)"
              % (c, pos[c] + 1, len(ordem), DEG_L[c]))
    else:
        print("     %d  sem degrau calculavel no Landsat" % c)
print("     %s" % ("REPLICA" if len(dentro) >= 4 else "NAO REPLICA"))
print()
print("R2 · Spearman S2 contra Landsat, n=%d blocos:  rho = %+.3f  (p = %.4f)"
      % (len(comuns), rho, pv))
print("     %s" % ("REPLICA" if rho >= 0.50 else "NAO REPLICA — limiar era 0,50"))

json.dump(dict(rho=float(rho), p=float(pv), n_cenas=len(serie),
               degrau_landsat_ndvi=DEG_L, degrau_landsat_ndmi=DEG_LM,
               degrau_s2=DEG_S2,
               n30={b["cul"]: b["n"] for b in BLOCOS},
               ent={b["cul"]: b["ent"] for b in BLOCOS},
               ha={b["cul"]: b["ha"] for b in BLOCOS}),
          open(os.path.join(VG, "reg01_landsat.json"), "w"), indent=1)
print()
print("escrito reg01_landsat.json")
