# -*- coding: utf-8 -*-
"""LACUNA 1, com poder a sério — a referência rastreada numa série densa.

PORQUE A PRIMEIRA CORRIDA NÃO CHEGA
------------------------------------
`triagem_referencia.py` correu e a referência passou: variação ano-a-ano máxima
0,024, ruído 0,0115, sem descontinuidade. **Mas com nove pontos, um por ano e
sem 2019.** Uma queda de um só ano entre 2018 e 2020 era invisível, e a
"variação ano-a-ano" era a diferença entre duas cenas únicas — logo confundida
com dia-do-ano, ângulo solar e um dia de nebulosidade fina.

Isto não é um pormenor de rigor. **A referência é o denominador de tudo**: do
contraste do A1, do fosso do B6, das âncoras da C4-C6, das 43 corridas do B1. Se
ela tiver uma descontinuidade, o erro está em todos os factos ao mesmo tempo. Um
teste sem poder sobre o denominador é pior do que nenhum, porque dá licença.

A janela de Ganfei tem 2 × 1 km. Descarregar todas as cenas de Verão de dez anos
custa pouco, e é a diferença entre «não vi nada» e «não há nada».

O QUE MUDA
----------
    · TODAS as cenas Sentinel-2 L2A de Junho a Setembro, 2017-2026, nuvem < 30 %
    · máscara de nuvem e sombra pela SCL, e exige-se 90 % da janela limpa
    · o ruído passa a ser medido DENTRO de cada ano (dispersão entre cenas do
      mesmo Verão), que é a escala certa para julgar uma diferença entre anos

CRITÉRIO, o mesmo de antes e fixado antes de correr
----------------------------------------------------
    R1 · variação entre medianas anuais >= 0,10 dentro de 2017-2024
         -> DESCONTINUIDADE A EXPLICAR.
    R2 · variação acima de 3x a dispersão INTRA-ANUAL é anómala mesmo abaixo
         de 0,10.
    R3 · corre em todas as unidades, não só na referência.

    Se a referência falhar, é **line-stop**: nenhum fosso publicado sobrevive
    sem recálculo. Se passar com este poder, a lacuna 1 fecha a sério.
"""
import json
import os
import sys

import numpy as np
import pystac_client
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject, transform_bounds
from pyproj import Transformer

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
CACHE = os.path.join(VG, "_densa_ganfei")
os.makedirs(CACHE, exist_ok=True)
AOI = (529950, 4654600, 531950, 4655600)
NCx, NLy = 200, 100
DEST = from_origin(AOI[0], AOI[3], 10.0, 10.0)
LIM, RUIDO_X, LIMPO_MIN = 0.10, 3.0, 0.90

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import carrega_mascaras, discos_dos_focos   # noqa

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM, SEM = np.isfinite(h) & (h >= 0.5), np.isfinite(h) & (h < 0.5)
do, de = discos_dos_focos(POMAR)
UN = {"REFERENCIA": REF,
      "foco OCIDENTAL": do & POMAR & COM,
      "foco ORIENTAL": de & POMAR & COM,
      "ORI sem pergola": de & POMAR & SEM,
      "resto do pomar": POMAR & COM & ~do & ~de & ~REF,
      "pomar inteiro": POMAR}
for n, m in UN.items():
    print("%-18s n10 = %4d  (%.2f ha)" % (n, m.sum(), m.sum() / 100))

tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1])
lo2, la2 = tr.transform(AOI[2], AOI[3])
cat = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
itens = list(cat.search(collections=["sentinel-2-l2a"], bbox=[lo, la, lo2, la2],
                        datetime="2017-01-01/2026-12-31",
                        query={"eo:cloud_cover": {"lt": 30}}).items())
itens = [i for i in itens if 6 <= i.datetime.month <= 9]
itens.sort(key=lambda i: i.datetime)
print()
print("cenas S2 de Jun-Set, nuvem < 30 %%, 2017-2026: %d" % len(itens))

ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")


def le(href, resample=RS.nearest):
    with rasterio.Env(**ENV), rasterio.open(href) as ds:
        W = ds.window(*transform_bounds("EPSG:32629", ds.crs, *AOI))
        arr = ds.read(1, window=W).astype("float32")
        out = np.full((NLy, NCx), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(W), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=resample)
    return out


SCL_MAU = {0, 1, 2, 3, 8, 9, 10, 11}      # nodata, defeito, sombra, nuvem, cirro, neve
serie = []
for k, it in enumerate(itens):
    d = it.datetime.strftime("%Y-%m-%d")
    cv = os.path.join(CACHE, "%s_%s.npy" % (d, it.id[-6:]))
    try:
        if os.path.exists(cv):
            nd = np.load(cv)
        else:
            scl = le(it.assets["scl"].href)
            limpo = np.isin(scl, list(SCL_MAU), invert=True) & np.isfinite(scl)
            if limpo.mean() < LIMPO_MIN:
                continue
            red, nir = le(it.assets["red"].href), le(it.assets["nir"].href)
            nd = np.where(limpo, (nir - red) / (nir + red + 1e-9), np.nan)
            np.save(cv, nd.astype("float32"))
    except Exception:
        continue
    linha = {"data": d}
    for n, m in UN.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= 0.7 * m.sum():
            linha[n] = float(np.median(v))
    if "REFERENCIA" in linha:
        serie.append(linha)
    if (k + 1) % 40 == 0:
        print("  %d/%d, %d validas" % (k + 1, len(itens), len(serie)))

ANOS = [str(a) for a in range(2017, 2027)]
print()
print("cenas validas: %d" % len(serie))
print("por ano: %s" % "  ".join(
    "%s:%d" % (a, sum(1 for r in serie if r["data"][:4] == a)) for a in ANOS))
json.dump(serie, open(os.path.join(VG, "densa_ganfei.json"), "w"), indent=1)

NIV, DISP = {}, {}
for n in UN:
    NIV[n] = np.array([np.median([r[n] for r in serie
                                  if r["data"][:4] == a and n in r])
                       if any(r["data"][:4] == a and n in r for r in serie)
                       else np.nan for a in ANOS])
    d = []
    for a in ANOS:
        v = [r[n] for r in serie if r["data"][:4] == a and n in r]
        if len(v) >= 3:
            d.append(np.percentile(v, 75) - np.percentile(v, 25))
    DISP[n] = float(np.median(d)) if d else np.nan

print()
print("=" * 104)
print("NIVEL ANUAL (mediana das cenas de Verao de cada ano)")
print("=" * 104)
print()
print("%-18s %s %10s" % ("", " ".join("%6s" % a for a in ANOS), "IQR intra"))
for n in UN:
    print("%-18s %s %10.4f"
          % (n, " ".join("     ." if not np.isfinite(v) else "%6.3f" % v
                         for v in NIV[n]), DISP[n]))

print()
print("=" * 104)
print("R1-R3 · variacao entre anos consecutivos DENTRO de 2017-2024")
print("=" * 104)
print()
print("%-18s %13s %13s %10s %11s  %s"
      % ("", "maior queda", "maior subida", "IQR intra", "3x IQR", "veredicto"))
ALERTA = []
k = ANOS.index("2024")
for n in UN:
    v = NIV[n]
    dd = np.diff(v[:k + 1])
    ok = np.isfinite(dd)
    if ok.sum() < 3:
        print("%-18s serie curta de mais" % n)
        continue
    q, qi = float(np.min(dd[ok])), int(np.argmin(np.where(ok, dd, np.inf)))
    s, si = float(np.max(dd[ok])), int(np.argmax(np.where(ok, dd, -np.inf)))
    pior = max(abs(q), abs(s))
    ruido = DISP[n] if np.isfinite(DISP[n]) else 1e-4
    grande, anom = pior >= LIM, pior > RUIDO_X * ruido
    ver = ("DESCONTINUIDADE" if grande else
           ("anomala face a dispersao intra-anual" if anom else "continua"))
    if grande or anom:
        ALERTA.append((n, pior, ver))
    print("%-18s %+8.3f(%s) %+8.3f(%s) %10.4f %11.4f  %s"
          % (n, q, ANOS[qi + 1], s, ANOS[si + 1], ruido, RUIDO_X * ruido, ver))

print()
ref_mau = any(n == "REFERENCIA" for n, _, _ in ALERTA)
if ref_mau:
    print(">>> LINE-STOP: a REFERENCIA tem descontinuidade. Nenhum fosso")
    print("    publicado sobrevive sem recalculo.")
else:
    print("A REFERENCIA passa o rastreio com serie densa. O denominador do A1,")
    print("do A2 e do bloco B mantem-se. LACUNA 1 FECHADA.")
if ALERTA:
    print()
    print("outras unidades a explicar: %s"
          % "; ".join("%s (%.3f, %s)" % t for t in ALERTA if t[0] != "REFERENCIA"))

# ---------------------------------------------- a subida do controlo, C2 l.66
v = NIV["REFERENCIA"]
b = np.isfinite(v[:k + 1])
A = np.arange(k + 1, dtype=float)
m, c = np.polyfit(A[b], v[:k + 1][b], 1)
res = v[:k + 1][b] - (m * A[b] + c)
print()
print("=" * 104)
print("A SUBIDA DO CONTROLO (C2, linha 66) — medida com a serie densa")
print("=" * 104)
print("declive %+.5f por ano  ·  total 2017-2024 %+.4f  ·  residuo maximo %.4f"
      % (m, m * k, np.abs(res).max()))
print("contraste do foco ocidental, para escala: -0,115")
print("razao: a subida do controlo e %.0fx menor que o efeito que se mede."
      % (0.115 / max(abs(m * k), 1e-6)))

json.dump(dict(anos=ANOS, nivel={n: [None if not np.isfinite(x) else float(x)
                                     for x in NIV[n]] for n in UN},
               iqr_intra=DISP, n_cenas=len(serie),
               alerta=[[n, p, ver] for n, p, ver in ALERTA],
               referencia_ok=not ref_mau),
          open(os.path.join(VG, "triagem_referencia_densa.json"), "w"), indent=1)
print()
print("escrito triagem_referencia_densa.json e densa_ganfei.json")
