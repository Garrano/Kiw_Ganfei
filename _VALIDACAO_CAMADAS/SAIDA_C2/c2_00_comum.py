# -*- coding: utf-8 -*-
"""Modulo comum da camada C2 — SINAL VEGETAL.

Geometria e mascaras herdadas da R2 (G2, G4, G5) e da C1. Vocabulario do
REGISTO_DE_NOMES.md: os focos identificam-se por coordenada.

  FOCO OESTE  E530485 N4655053   («Zona 0» da exploracao; B2, valvulas 8-9)
  FOCO ESTE   E530977 N4655117   (B3, valvulas 13-14)

Traducao do vocabulario antigo, declarada como a C1 declarou:
  mascara `zona0` do ficheiro   = FOCO ESTE
  mascara `manchaW` (RETIRADA)  = FOCO OESTE

O conjunto operativo de mascaras e `sentinel/masks_geograficas.json`, derivado
das ortofotos por periodicidade de compasso. O antigo `masks.json` era circular
(`pomar` = nd2026 > 0,78; `manchaW` = nd2026 < 0,76) e NAO e usado aqui em
nenhum calculo — so e lido, uma vez, para medir a circularidade (c2_01).
"""
import json
import os

import numpy as np
import rasterio
from scipy import ndimage

RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
SAIDA = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
C1 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1"
os.makedirs(SAIDA, exist_ok=True)

# --- G1: grelha de analise ---
AOI = (529950.0, 4654600.0, 531950.0, 4655600.0)
NL, NC, PASSO = 100, 200, 10.0
ORIGEM_NO = (529950.0, 4655600.0)

# --- R2 G34: os dois focos, por coordenada ---
FOCO_OESTE = (530485.0, 4655053.0)
FOCO_ESTE = (530977.0, 4655117.0)

# --- A serie de plena estacao (9 datas). 2019-09-02 sai por fenologia (G10),
#     2025-06-17 sai por ser de inicio de estacao. As duas sao usadas em
#     c2_02 precisamente como sondas de fenologia. ---
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
TODAS = sorted(DATAS + ["2019-09-02", "2025-06-17"])

# --- A definicao de defice, fixada aqui e usada em toda a camada ---
LIMIAR = 0.05          # abaixo da referencia da propria data
ABERTURA = (2, 2)      # elemento estruturante da abertura morfologica
MIN_NUCLEO = 15        # celulas (0,15 ha) para um nucleo ser listado


def anos_decimais(datas):
    return np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12.0 for d in datas])


def doy(d):
    import datetime as _dt
    x = _dt.date(int(d[:4]), int(d[5:7]), int(d[8:10]))
    return x.timetuple().tm_yday


def centros_celulas():
    e = ORIGEM_NO[0] + (np.arange(NC) + 0.5) * PASSO
    n = ORIGEM_NO[1] - (np.arange(NL) + 0.5) * PASSO
    return np.meshgrid(e, n)


def carrega_mascaras():
    with open(os.path.join(RAIZ, "sentinel", "masks_geograficas.json"),
              encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for k in ("pomar", "saudavel", "zona0", "nu2021"):
        out[k] = np.array([[c == "1" for c in linha] for linha in d[k + "_bits"]])
    return out, d


def carrega_ndvi(datas=None):
    datas = datas or DATAS
    return {d: rasterio.open(os.path.join(RAIZ, "sentinel", "%s.tif" % d)).read(1)
            for d in datas}


def discos_dos_focos(pomar, raio=90.0):
    E, N = centros_celulas()
    do = ((E - FOCO_OESTE[0]) ** 2 + (N - FOCO_OESTE[1]) ** 2) <= raio ** 2
    de = ((E - FOCO_ESTE[0]) ** 2 + (N - FOCO_ESTE[1]) ** 2) <= raio ** 2
    return (do & pomar), (de & pomar)


def mapa_defice(nd, pomar, ref_val, limiar=LIMIAR, abertura=ABERTURA):
    """Mapa booleano de defice: NDVI abaixo de (referencia da data - limiar)."""
    b = (nd < ref_val - limiar) & pomar
    if abertura:
        b = ndimage.binary_opening(b, np.ones(abertura))
    return b


def nucleos(defice, minimo=MIN_NUCLEO):
    """Nucleos contiguos do mapa de defice: (ha, E do centroide, N, celulas)."""
    lab, n = ndimage.label(defice, np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        m = lab == i
        c = int(m.sum())
        if c < minimo:
            continue
        ys, xs = np.where(m)
        # Convencao herdada de `serie_mascaras_geograficas.py`: E = AOI[0] +
        # coluna*10, isto e, o CANTO NO da celula, nao o centro. Mantida para
        # os numeros serem comparaveis com a R2 G29 e com `_serie_geografica.txt`.
        # O centro da celula fica +5 m a E e -5 m a N destes valores.
        out.append((c / 100.0,
                    AOI[0] + xs.mean() * 10,
                    ORIGEM_NO[1] - ys.mean() * 10,
                    c))
    out.sort(reverse=True)
    return out


def fmt(x, n=3):
    return ("{:." + str(n) + "f}").format(x).replace(".", ",")
