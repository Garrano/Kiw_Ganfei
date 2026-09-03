# -*- coding: utf-8 -*-
"""P2 — as onze cenas que ninguém olhou. Um acontecimento ou dois?

A lacuna, e quem a nomeou
-------------------------
`CAMADA_2_ADVERSARIO_R2.md`, transversal B, confirmada pelo T2:

  «O acontecimento inteiro está datado por DUAS cenas separadas por onze meses.
  Um acontecimento agudo único e dois declínios sucessivos são indistinguíveis
  neste desenho. Um degrau entre dois pontos a onze meses de distância é uma
  INTERPOLAÇÃO, não uma medição.»

O T2 contou o que existe no intervalo: **onze cenas de plena estação** com
nuvem aceitável — sete em Agosto de 2025 e quatro em Julho de 2026.

O que isto faz
--------------
Descarrega essas onze, aplica-lhes o mesmo processamento das nove da série, e
mede as mesmas unidades. Com as duas cenas originais dão **treze pontos** dentro
da janela, em vez de dois.

O que se procura, e está fixado antes de correr:

  · se o nível em Agosto de 2025 já estiver no patamar baixo e lá ficar até
    Julho de 2026 -> **um acontecimento**, antes ou durante Agosto de 2025;
  · se descer em Agosto de 2025, estabilizar, e descer OUTRA VEZ em 2026 ->
    **dois**;
  · se descer progressivamente ao longo das treze -> **não é degrau**, e o
    ajuste degrau-contra-recta do T1 tem de ser refeito nesta resolução.

Ressalva que viaja com o resultado
----------------------------------
As onze cenas atravessam a fronteira S2A/S2B/S2C, e o V10 da C2 diz que as
duas cenas mais baixas da série são as duas únicas do S2C. Por isso mede-se
**o contraste foco-menos-controlo**, que é a grandeza que a R3 certificou, e
não o nível absoluto: um desvio de plataforma comum às unidades cancela-se.
A plataforma de cada cena vai impressa.
"""
import json
import os

import numpy as np
import planetary_computer  # noqa  (nao usado; mantido por simetria de ambiente)
import pystac_client
import rasterio
from rasterio.warp import Resampling as RS
from rasterio.warp import reproject
from rasterio.transform import from_origin
from rasterio.windows import from_bounds
from pyproj import Transformer

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
NL, NC = 100, 200
DEST = from_origin(AOI[0], AOI[3], 10.0, 10.0)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
EE, NN = np.meshgrid(AOI[0] + (np.arange(NC) + .5) * 10.,
                     AOI[3] - (np.arange(NL) + .5) * 10.)
C_OC = (530485.0, 4655053.0)
DOC = (np.hypot(EE - C_OC[0], NN - C_OC[1]) <= 90) & POMAR & COM
DOR = ZONA0 & COM
dfoco = np.minimum(np.hypot(EE - C_OC[0], NN - C_OC[1]),
                   np.hypot(EE - float(EE[ZONA0].mean()), NN - float(NN[ZONA0].mean())))
CTRL = POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF

UN = [("OCIDENTAL", DOC), ("ORIENTAL", DOR), ("CONTROLO", CTRL)]

CENAS = json.load(open(os.path.join(VG, "t2_cenas_descartadas.json"),
                       encoding="utf-8"))["cenas"]
ALVO = sorted({c["data"] for c in CENAS if 182 <= c["doy"] <= 244})
print("cenas de plena estação a descarregar: %d  %s" % (len(ALVO), ALVO))

cat = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1])
lo2, la2 = tr.transform(AOI[2], AOI[3])
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")


def le(href):
    with rasterio.Env(**ENV), rasterio.open(href) as ds:
        W = ds.window(*rasterio.warp.transform_bounds("EPSG:32629", ds.crs, *AOI))
        arr = ds.read(1, window=W).astype("float32")
        out = np.full((NL, NC), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(W), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=RS.nearest)
    return out


linhas = []
for d in ALVO:
    itens = list(cat.search(collections=["sentinel-2-l2a"], bbox=[lo, la, lo2, la2],
                            datetime="%sT00:00:00Z/%sT23:59:59Z" % (d, d)).items())
    for it in itens:
        try:
            a = it.assets
            red, nir = le(a["red"].href), le(a["nir"].href)
            ndvi = (nir - red) / (nir + red)
            if not np.isfinite(ndvi[REF]).any():
                continue
            r = float(np.nanmean(ndvi[REF]))
            if not (0.2 < r < 1.0):
                continue
            linha = dict(data=d, cena=it.id,
                         plataforma=it.properties.get("platform", ""),
                         nuvens=float(it.properties.get("eo:cloud_cover", 99)))
            for nome, m in UN:
                linha[nome] = float(np.nanmean(ndvi[m]))
            linha["contraste_OC"] = linha["OCIDENTAL"] - linha["CONTROLO"]
            linha["contraste_OR"] = linha["ORIENTAL"] - linha["CONTROLO"]
            linhas.append(linha)
            print("  %s  %-12s nuvem %4.1f %%   OC %.3f  OR %.3f  CTRL %.3f"
                  % (d, linha["plataforma"], linha["nuvens"],
                     linha["OCIDENTAL"], linha["ORIENTAL"], linha["CONTROLO"]))
            break
        except Exception as e:
            print("  %s  falhou: %s" % (d, str(e)[:60]))

# as duas cenas originais da janela, para ancorar
for d in ("2025-08-14", "2026-07-27"):
    a = rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
    linha = dict(data=d, cena="(série original)", plataforma="", nuvens=np.nan)
    for nome, m in UN:
        linha[nome] = float(np.nanmean(a[m]))
    linha["contraste_OC"] = linha["OCIDENTAL"] - linha["CONTROLO"]
    linha["contraste_OR"] = linha["ORIENTAL"] - linha["CONTROLO"]
    linhas.append(linha)

linhas.sort(key=lambda r: r["data"])

print()
print("=" * 96)
print("A JANELA, CENA A CENA — contraste foco menos controlo")
print("=" * 96)
print()
print("%-12s %-12s %8s %10s %10s %12s %12s"
      % ("data", "plataforma", "nuvem", "OCIDENTAL", "ORIENTAL", "contr. OC", "contr. OR"))
for r in linhas:
    marca = "  <-- série" if r["cena"] == "(série original)" else ""
    print("%-12s %-12s %7.1f%% %10.3f %10.3f %+12.4f %+12.4f%s"
          % (r["data"], r["plataforma"].replace("sentinel-", "S"),
             r["nuvens"] if np.isfinite(r["nuvens"]) else -1,
             r["OCIDENTAL"], r["ORIENTAL"],
             r["contraste_OC"], r["contraste_OR"], marca))

json.dump(linhas, open(os.path.join(VG, "p2_onze_cenas.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito p2_onze_cenas.json  (%d cenas)" % len(linhas))
