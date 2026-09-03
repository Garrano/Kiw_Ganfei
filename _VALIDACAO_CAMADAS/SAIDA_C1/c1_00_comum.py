# -*- coding: utf-8 -*-
"""Modulo comum da camada C1. Geometria herdada da C0/R2, sem NDVI."""
import json, os
import numpy as np
from pyproj import Transformer

RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
SAIDA = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1"
os.makedirs(SAIDA, exist_ok=True)

# --- G1: grelha de analise (EPSG:32629, 10 m, 200x100) ---
AOI = (529950.0, 4654600.0, 531950.0, 4655600.0)
NL, NC, PASSO = 100, 200, 10.0
ORIGEM_NO = (529950.0, 4655600.0)

# --- R2 G34: os dois focos, por coordenada ---
FOCO_OESTE = (530485.0, 4655053.0)   # exploracao chama-lhe "Zona 0"; B2, valvulas 8-9
FOCO_ESTE  = (530977.0, 4655117.0)   # B3, valvulas 13-14

T_29_TO_3763 = Transformer.from_crs("EPSG:32629", "EPSG:3763", always_xy=True)
T_3763_TO_29 = Transformer.from_crs("EPSG:3763", "EPSG:32629", always_xy=True)
T_29_TO_WGS  = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)


def centros_celulas():
    """Devolve (E, N) dos centros das 100x200 celulas de 10 m, em EPSG:32629."""
    e = ORIGEM_NO[0] + (np.arange(NC) + 0.5) * PASSO
    n = ORIGEM_NO[1] - (np.arange(NL) + 0.5) * PASSO
    return np.meshgrid(e, n)


def carrega_mascaras():
    """Mascaras geograficas operativas (R2 G5): masks_geograficas.json."""
    with open(os.path.join(RAIZ, "sentinel", "masks_geograficas.json"), encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for k in ("pomar", "saudavel", "zona0", "nu2021"):
        out[k] = np.array([[c == "1" for c in linha] for linha in d[k + "_bits"]])
    return out, d


def discos_dos_focos(pomar, raio=90.0):
    """Vizinhancas GEOMETRICAS de igual raio nos dois focos, intersectadas com pomar.

    Definicao puramente geometrica: nao usa NDVI, nao usa mapa de defice,
    e e simetrica entre os dois focos. Serve para comparar substrato.
    """
    E, N = centros_celulas()
    do = ((E - FOCO_OESTE[0]) ** 2 + (N - FOCO_OESTE[1]) ** 2) <= raio ** 2
    de = ((E - FOCO_ESTE[0]) ** 2 + (N - FOCO_ESTE[1]) ** 2) <= raio ** 2
    return (do & pomar), (de & pomar)


def valvulas():
    with open(os.path.join(RAIZ, "valvulas_por_area.json"), encoding="utf-8") as f:
        return json.load(f)


def fmt(x, n=3):
    return ("{:." + str(n) + "f}").format(x).replace(".", ",")
