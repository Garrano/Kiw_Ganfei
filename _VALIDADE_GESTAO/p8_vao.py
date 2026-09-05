# -*- coding: utf-8 -*-
"""P8 — as 49 cenas do vao. Quantas transicoes, e entre que datas?

CRITERIO PRE-REGISTADO, e foi a um adversario ANTES da corrida:
`_VALIDACAO_CAMADAS/PRE_REGISTO_VAO.md`. E a clausula C9, cumprida pela
primeira vez neste processo.

O QUE ISTO SUBSTITUI
--------------------
O `p2_onze_cenas.py`, retirado pelo Controlo 4 de 05-09-2026. O defeito nao era
de execucao: a linha 76 filtrava `182 <= doy <= 244` sobre uma janela que so
intersecta esse intervalo nas duas pontas, pelo que **nenhum resultado possivel
podia seleccionar um ramo da tabela de decisao**. O vao passou de 347 para 310
dias. As 49 cenas limpas que o atravessam estavam inventariadas no
`t2_cenas_descartadas.json` — ficheiro que o proprio p2 abria.

AS TRES CORRECCOES QUE O CONTROLO 4 OBRIGA
------------------------------------------
1 · **Sem filtro de dia-do-ano.** Todas as datas limpas do intervalo.
2 · **Mascara de nuvem por pixel (SCL).** Sem ela, a correlacao entre fraccao de
    nuvem e contraste era +0,86 em Ago-2025 e +0,99 em Jul-2026 — o artefacto
    operava sobre a propria grandeza que o contraste devia proteger. Uma cena so
    entra se CADA unidade tiver >= 60 % de pixeis validos.
3 · **Nivel absoluto de cada unidade impresso ao lado do contraste**, para a
    fenologia ficar visivel. O p2 so publicou medias de aglomerado, e por isso o
    seu «patamar» de 2026 — que se move 0,099 em 23 dias — passou por patamar.

DUAS COISAS DE DESENHO
----------------------
**Guarda as matrizes por data** em `p8_cache/`. Se o adversario mandar mudar o
limiar dos 60 %, as classes de SCL ou a definicao de transicao, reagrega-se sem
voltar a descarregar. Uma regra que so se pode testar redescarregando nao se
testa.

**Nao decide nada aqui.** Este ficheiro MEDE. A classificacao em ramos faz-se
contra a tabela pre-registada, num passo separado e depois de o adversario
responder — para que a regra nao seja afinada contra os numeros que ja se viram.
"""
import io
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

sys.path.insert(0, r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS")
try:
    from proveniencia import guardar
except ImportError:
    def guardar(d, c, **k):
        json.dump(d, io.open(c, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        return c

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
CACHE = os.path.join(VG, "p8_cache")
os.makedirs(CACHE, exist_ok=True)

AOI = (529950, 4654600, 531950, 4655600)
NL, NC = 100, 200
DEST = from_origin(AOI[0], AOI[3], 10.0, 10.0)

# SCL a excluir: 3 sombra de nuvem, 8 nuvem media, 9 nuvem alta, 10 cirrus,
# 11 neve. Declarado no pre-registo §4.
SCL_MAU = (3, 8, 9, 10, 11)
VALIDO_MIN = 0.60          # por unidade, por cena
NUVEM_MAX = 20.0           # o corte do inventario T2

# ── unidades: as certificadas, sem alteracao ────────────────────────────────
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
                   np.hypot(EE - float(EE[ZONA0].mean()),
                            NN - float(NN[ZONA0].mean())))
CTRL = POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF
UN = [("OCIDENTAL", DOC), ("ORIENTAL", DOR), ("CONTROLO", CTRL)]

# ── as datas: TODAS as limpas do intervalo, sem filtro de dia-do-ano ────────
CENAS = json.load(io.open(os.path.join(VG, "t2_cenas_descartadas.json"),
                          encoding="utf-8"))["cenas"]
ALVO = sorted({c["data"] for c in CENAS if c["nuvens"] < NUVEM_MAX})
# as da serie que ficam dentro ou a beira do intervalo, incluindo a de Junho de
# 2025 que o p2 tinha na mesma pasta e nao abriu
for d in ("2025-06-17", "2025-08-14", "2026-07-27"):
    if d not in ALVO:
        ALVO.append(d)
ALVO = sorted(ALVO)
print("datas unicas a processar: %d  (de %s a %s)" % (len(ALVO), ALVO[0], ALVO[-1]))

cat = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
tr = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
lo, la = tr.transform(AOI[0], AOI[1])
lo2, la2 = tr.transform(AOI[2], AOI[3])
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", AWS_NO_SIGN_REQUEST="YES")


def le(href, nn=RS.nearest):
    with rasterio.Env(**ENV), rasterio.open(href) as ds:
        W = ds.window(*transform_bounds("EPSG:32629", ds.crs, *AOI))
        arr = ds.read(1, window=W).astype("float32")
        out = np.full((NL, NC), np.nan, "float32")
        reproject(arr, out, src_transform=ds.window_transform(W), src_crs=ds.crs,
                  dst_transform=DEST, dst_crs="EPSG:32629",
                  src_nodata=0, dst_nodata=np.nan, resampling=nn)
    return out


def do_disco(d):
    """A serie ja em disco, para as tres datas que existem como .tif."""
    p = os.path.join(S2, "sentinel", "%s.tif" % d)
    if not os.path.exists(p):
        return None
    return rasterio.open(p).read(1).astype("float32")


linhas, falhas = [], []
for i, d in enumerate(ALVO, 1):
    npz = os.path.join(CACHE, "%s.npz" % d)
    if os.path.exists(npz):
        z = np.load(npz)
        ndvi, scl, meta = z["ndvi"], z["scl"], json.loads(str(z["meta"]))
    else:
        ndvi = scl = None
        meta = {"cena": "", "plataforma": "", "nuvens": float("nan")}
        pre = do_disco(d)
        if pre is not None:
            ndvi = pre
            scl = np.zeros((NL, NC), "float32")     # sem SCL: trata-se abaixo
            meta = {"cena": "(serie em disco)", "plataforma": "",
                    "nuvens": float("nan")}
        else:
            try:
                itens = list(cat.search(
                    collections=["sentinel-2-l2a"], bbox=[lo, la, lo2, la2],
                    datetime="%sT00:00:00Z/%sT23:59:59Z" % (d, d)).items())
            except Exception as e:
                falhas.append((d, "procura: %s" % type(e).__name__)); continue
            melhor = None
            for it in itens:
                n = it.properties.get("eo:cloud_cover", 100.0)
                if melhor is None or n < melhor[0]:
                    melhor = (n, it)
            if melhor is None:
                falhas.append((d, "sem item")); continue
            n, it = melhor
            try:
                a = it.assets
                red, nir = le(a["red"].href), le(a["nir"].href)
                scl = le(a["scl"].href)
                ndvi = (nir - red) / (nir + red)
                meta = {"cena": it.id,
                        "plataforma": it.properties.get("platform", ""),
                        "nuvens": float(n)}
            except Exception as e:
                falhas.append((d, "leitura: %s" % type(e).__name__)); continue
        np.savez_compressed(npz, ndvi=ndvi, scl=scl,
                            meta=np.array(json.dumps(meta)))

    # ── mascara por pixel. Para as .tif da serie nao ha SCL: marca-se.
    tem_scl = bool(np.nanmax(scl)) if scl is not None else False
    mau = np.isin(scl.astype("int16"), SCL_MAU) if tem_scl \
        else np.zeros((NL, NC), bool)
    bom = np.isfinite(ndvi) & ~mau

    lin = {"data": d, "cena": meta["cena"], "plataforma": meta["plataforma"],
           "nuvens_cena": meta["nuvens"], "scl_disponivel": bool(tem_scl)}
    ok = True
    for nome, m in UN:
        v = ndvi[m & bom]
        frac = float((m & bom).sum()) / float(m.sum())
        lin["%s_valido" % nome] = round(frac, 4)
        lin[nome] = float(np.median(v)) if v.size else float("nan")
        if frac < VALIDO_MIN:
            ok = False
    lin["retida"] = ok
    lin["contraste_OC"] = lin["OCIDENTAL"] - lin["CONTROLO"]
    lin["contraste_OR"] = lin["ORIENTAL"] - lin["CONTROLO"]
    linhas.append(lin)
    print("  %3d/%d  %s  %-28s ret=%s  cOC=%+.4f  cOR=%+.4f"
          % (i, len(ALVO), d, meta["cena"][:28], "sim" if ok else "NAO",
             lin["contraste_OC"], lin["contraste_OR"]))

guardar({"pre_registo": "_VALIDACAO_CAMADAS/PRE_REGISTO_VAO.md",
         "criterio": {"scl_excluidas": list(SCL_MAU),
                      "valido_min_por_unidade": VALIDO_MIN,
                      "nuvem_max_inventario": NUVEM_MAX,
                      "filtro_dia_do_ano": None},
         "n_datas": len(ALVO), "n_medidas": len(linhas),
         "n_retidas": sum(1 for l in linhas if l["retida"]),
         "falhas": falhas, "serie": linhas},
        os.path.join(VG, "p8_vao.json"))
print()
print("medidas %d · retidas %d · falhas %d"
      % (len(linhas), sum(1 for l in linhas if l["retida"]), len(falhas)))
print("escrito p8_vao.json — a classificacao em ramos e um passo SEPARADO,")
print("depois do adversario responder ao pre-registo.")
