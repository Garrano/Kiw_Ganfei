# -*- coding: utf-8 -*-
"""REG-01 — o acontecimento de 2025-26 é local ou regional?

A pergunta, e quem a pôs à frente de tudo
-----------------------------------------
`CAMADA_5_CERTIFICADO.md` §3, e o adversário dela na R10:

  «se a causa for regional, quase todas as medidas de parcela que se possam
   recomendar são inúteis»; «enquanto REG-01 estiver por fechar, **nenhuma
   medida irreversível**».

A C5 escreveu isto em quatro sítios e não fez da REG-01 uma condição de
arranque. O adversário obrigou. Está por correr desde então.

HIPÓTESE FIXADA ANTES DE CORRER
-------------------------------
    H1 · o degrau de 2025-26 é **específico** dos dois focos desta exploração.
    H0 · é **regional** — uma fracção substancial do kiwi da região tem o mesmo.

    CRITÉRIO, a priori: se os dois focos de Ganfei caírem **acima do percentil
    10** da distribuição regional, H1 cai e o acontecimento é regional. Se
    caírem na cauda extrema, é local.

O DESENHO, e porque é auto-controlado
-------------------------------------
Para cada bloco e cada cena mede-se o NDVI médio, e depois o **desvio à mediana
regional dessa cena**. A região é o seu próprio controlo: um degrau de
plataforma, uma anomalia meteorológica ou um efeito de dia-do-ano comuns à
região **cancelam-se nesta diferença**. É a mesma lógica do contraste
foco-menos-controlo que a C2 R3 certificou, alargada.

Estatística: degrau = média do desvio em 2025-26 menos média em 2017-2024.

AS MESMAS CENAS, não outras
---------------------------
Usam-se os **IDs de cena do `proveniencia.json`** — as mesmas nove que a série
certificada usa. Não se escolhem cenas novas para a comparação: seria mudar
duas coisas ao mesmo tempo.

O QUE ESTE TESTE NÃO TEM
------------------------
**Instrumento independente para o sinal.** É Sentinel-2, como tudo o resto. O
que é independente são as **fronteiras**: todos os blocos, incluindo os de
comparação, vêm do parcelário do IFAP — documento de outra entidade, desenhado
para pagamentos. Declara-se, não se dilui.
"""
import json
import os

import numpy as np
import pystac_client
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject, transform_bounds
from shapely.geometry import shape
from shapely.ops import transform as sht
from pyproj import Transformer
from matplotlib.path import Path as MP

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CACHE = os.path.join(VG, "_reg01_cache")
os.makedirs(CACHE, exist_ok=True)

ENT_POMAR = 472062
tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
para_utm = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)

# --------------------------------------------------------------- os blocos
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
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
    g = para_utm(shape(ft["geometry"])).buffer(0)
    if g.is_empty or g.area / 1e4 < 0.5:          # menos de 0,5 ha nao entra
        continue
    c = g.centroid
    dono = None
    for pg, e in parc:
        if pg.contains(c):
            dono = e
            break
    BLOCOS.append(dict(cul=ft["properties"].get("CUL_ID"), geom=g,
                       ha=g.area / 1e4, ent=dono, E=c.x, N=c.y))
print("blocos de kiwi com >= 0,5 ha: %d  (%.1f ha)"
      % (len(BLOCOS), sum(b["ha"] for b in BLOCOS)))
print("  do ENT %d: %d   ·   de outros: %d beneficiários"
      % (ENT_POMAR, sum(1 for b in BLOCOS if b["ent"] == ENT_POMAR),
         len({b["ent"] for b in BLOCOS if b["ent"] != ENT_POMAR})))

xs = [b["E"] for b in BLOCOS]
ys = [b["N"] for b in BLOCOS]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)
NCx = int((BB[2] - BB[0]) / 10)
NLy = int((BB[3] - BB[1]) / 10)
DEST = from_origin(BB[0], BB[3], 10.0, 10.0)
print("janela regional: %.1f x %.1f km  (%d x %d células)"
      % ((BB[2] - BB[0]) / 1000, (BB[3] - BB[1]) / 1000, NCx, NLy))

# máscaras por bloco, na grelha regional
EE, NN = np.meshgrid(BB[0] + (np.arange(NCx) + .5) * 10.,
                     BB[3] - (np.arange(NLy) + .5) * 10.)
pts = np.column_stack([EE.ravel(), NN.ravel()])
for b in BLOCOS:
    ext = list(b["geom"].exterior.coords)
    b["mask"] = MP(np.array(ext)).contains_points(pts).reshape(NLy, NCx)
    b["cel"] = int(b["mask"].sum())
BLOCOS = [b for b in BLOCOS if b["cel"] >= 20]     # 0,20 ha de células inteiras
print("blocos com >= 20 células: %d" % len(BLOCOS))

# --------------------------------------------------------------- as cenas
def _abre(caminho):
    """Alguns ficheiros do projecto estao em cp1252, outros em utf-8."""
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.load(open(caminho, encoding=enc))
        except UnicodeDecodeError:
            continue
    raise IOError(caminho)


prov = _abre(os.path.join(S2, "sentinel", "proveniencia.json"))
CENAS = {c["data"]: c["cena"] for c in prov["cenas"]}
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
T = np.array([d >= "2025" for d in DATAS])

cat = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
lo, la = tr.transform(BB[0], BB[1], direction="INVERSE")
lo2, la2 = tr.transform(BB[2], BB[3], direction="INVERSE")
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")


def le_banda(href):
    with rasterio.Env(**ENV), rasterio.open(href) as ds:
        W = ds.window(*transform_bounds("EPSG:32629", ds.crs, *BB))
        arr = ds.read(1, window=W).astype("float32")
        out = np.full((NLy, NCx), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(W), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=RS.nearest)
    return out


print()
niveis = {}
for d in DATAS:
    cache = os.path.join(CACHE, "ndvi_%s.npy" % d)
    if os.path.exists(cache):
        ndvi = np.load(cache)
        print("  %s  (cache)" % d)
    else:
        alvo = CENAS[d]
        it = None
        for x in cat.search(collections=["sentinel-2-l2a"], bbox=[lo, la, lo2, la2],
                            datetime="%sT00:00:00Z/%sT23:59:59Z" % (d, d)).items():
            if x.id == alvo:
                it = x
                break
        if it is None:
            print("  %s  CENA %s NAO ENCONTRADA — salta" % (d, alvo))
            continue
        red, nir = le_banda(it.assets["red"].href), le_banda(it.assets["nir"].href)
        ndvi = (nir - red) / (nir + red)
        np.save(cache, ndvi)
        print("  %s  %s  descarregada" % (d, alvo))
    niveis[d] = ndvi

DATAS = [d for d in DATAS if d in niveis]
T = np.array([d >= "2025" for d in DATAS])

# --------------------------------------------------------------- a medida
for b in BLOCOS:
    b["serie"] = [float(np.nanmean(niveis[d][b["mask"]])) for d in DATAS]
BLOCOS = [b for b in BLOCOS if all(np.isfinite(b["serie"]))]
print("blocos com série completa: %d" % len(BLOCOS))

M = np.array([b["serie"] for b in BLOCOS])          # blocos x cenas
mediana_regional = np.median(M, axis=0)
print()
print("mediana regional por cena: %s"
      % "  ".join("%.3f" % v for v in mediana_regional))

for i, b in enumerate(BLOCOS):
    dev = M[i] - mediana_regional
    b["desvio"] = dev.tolist()
    b["degrau"] = float(dev[T].mean() - dev[~T].mean())

degraus = np.array([b["degrau"] for b in BLOCOS])
outros = np.array([b["degrau"] for b in BLOCOS if b["ent"] != ENT_POMAR])

print()
print("=" * 94)
print("A DISTRIBUIÇÃO REGIONAL DO DEGRAU  (desvio à mediana regional)")
print("=" * 94)
print()
print("todos os blocos (n=%d):  p10 %+.4f  p25 %+.4f  mediana %+.4f  p75 %+.4f  p90 %+.4f"
      % (len(degraus), *np.percentile(degraus, [10, 25, 50, 75, 90])))
print("só de OUTROS  (n=%d):  p10 %+.4f  p25 %+.4f  mediana %+.4f  p75 %+.4f  p90 %+.4f"
      % (len(outros), *np.percentile(outros, [10, 25, 50, 75, 90])))

print()
print("%-12s %8s %7s %10s %11s %s"
      % ("CUL_ID", "ENT", "ha", "degrau", "percentil", ""))
for b in sorted(BLOCOS, key=lambda z: z["degrau"]):
    pct = 100.0 * np.mean(degraus <= b["degrau"])
    marca = "  <-- a exploração" if b["ent"] == ENT_POMAR else ""
    print("%-12s %8s %7.2f %+10.4f %10.0f %%%s"
          % (b["cul"], b["ent"], b["ha"], b["degrau"], pct, marca))

json.dump(dict(datas=DATAS, mediana_regional=mediana_regional.tolist(),
               blocos=[{k: v for k, v in b.items() if k not in ("geom", "mask")}
                       for b in BLOCOS]),
          open(os.path.join(VG, "reg01_local_ou_regional.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito reg01_local_ou_regional.json")
