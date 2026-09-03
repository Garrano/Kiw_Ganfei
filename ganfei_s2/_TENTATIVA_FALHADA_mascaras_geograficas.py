# -*- coding: utf-8 -*-
"""Mascaras GEOGRAFICAS, derivadas da ortofoto — nao do NDVI que se vai medir.

Porque existe
-------------
`fazer_masks_v2.py` declara no seu cabecalho "poligonos GEOGRAFICOS e ESTATICOS;
nenhum e re-derivado por data" e depois faz exactamente o contrario:

    copado = binary_opening((nd > 0.78) & (dist > 5), ...)   # nd = 2026-07-27
    mw     = pomar & (nd < 0.76) & jw

O `pomar` e o NDVI de 2026 acima de 0,78. A `manchaW` e o NDVI de 2026 abaixo
de 0,76. Medir depois como o NDVI da manchaW evoluiu ate 2026 e circular: a
mancha foi seleccionada por ter NDVI baixo em 2026, e a queda ate 2026 fica
garantida por construcao, nem que seja por regressao a media. A `saudavel`
depende do `pomar`, portanto a referencia tambem foi escolhida sobre a ultima
cena da serie que ela propria calibra.

O que este script faz de diferente
----------------------------------
1. INSTRUMENTO INDEPENDENTE. A geometria sai da ortofoto DGT de 2021 a 25 cm
   (EPSG:3763), que nao entra em nenhuma medicao de NDVI.

2. ASSINATURA FISICA, NAO DE VIGOR. O kiwi em pergola tem uma assinatura
   propria na ortofoto: postes e cabos aparecem como pontos claros em malha
   regular sobre copado escuro. Deteta-se por TEXTURA — desvio padrao local a
   escala do compasso — e nao por quao verde esta. Uma planta debilitada
   continua a ter postes.

3. REFERENCIA POR AMOSTRAGEM SISTEMATICA. A `saudavel` deixa de ser "as
   manchas que parecem sas". Passa a ser uma grelha regular de celulas
   distribuidas por todo o pomar. Nao se escolhe nenhuma por estar boa: uma
   referencia escolhida por estar boa mede a distancia ao melhor caso, nao a
   um estado normal, e desloca-se sozinha quando o pomar inteiro desce.

4. A `manchaW` DEIXA DE EXISTIR como mascara. Uma mancha nao e um lugar fixo:
   e um resultado. Fica so `pomar` (onde ha kiwi), `saudavel` (a referencia
   sistematica) e `zona0` (unica que ja era geografica no ficheiro antigo).
   As manchas passam a emergir do mapa de defice, em vez de o definirem.
"""
import json
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)      # EPSG:32629
ORTO = "orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"
PASSO = 40          # subamostragem: 25 cm -> 10 m, igual a grelha Sentinel

ds = rasterio.open(ORTO)
W = transform_bounds("EPSG:32629", ds.crs, *AOI)
w = from_bounds(*W, transform=ds.transform)
rgb = np.dstack([ds.read(i, window=w).astype("float32") for i in (1, 2, 3)])
H, L = rgb.shape[:2]
print("ortofoto lida: %d x %d px a 25 cm (EPSG:3763)" % (L, H))

lum = rgb.mean(2)

# --- textura: postes claros em malha regular -------------------------------
# desvio padrao local numa janela de ~3 m (12 px). O copado de pergola tem
# pontos claros regulares sobre fundo escuro -> DP alto. Culturas rasteiras,
# solo lavrado e prado tem DP baixo a esta escala.
J = 12
med = ndimage.uniform_filter(lum, J)
med2 = ndimage.uniform_filter(lum * lum, J)
dp = np.sqrt(np.maximum(med2 - med * med, 0))

# --- reprojectar para a GRELHA EXACTA do Sentinel --------------------------
# nao basta subamostrar: a janela em EPSG:3763 nao esta alinhada com a AOI em
# EPSG:32629. Uma mascara desalinhada e pior do que uma mascara circular.
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin

DESTINO = from_origin(AOI[0], AOI[3], 10.0, 10.0)     # 10 m, canto NO da AOI
origem = rasterio.windows.transform(w, ds.transform)


def para_grelha(a):
    fora = np.zeros((100, 200), "float32")
    reproject(a.astype("float32"), fora,
              src_transform=origem, src_crs=ds.crs,
              dst_transform=DESTINO, dst_crs="EPSG:32629",
              resampling=Resampling.average)
    return fora


DP = para_grelha(dp)
LUM = para_grelha(lum)
ny, nx = DP.shape
print("reprojectado para a grelha Sentinel: %d x %d celulas de 10 m" % (nx, ny))
print("  (mesma origem %d, %d e mesmo passo dos ficheiros sentinel/*.tif)"
      % (AOI[0], AOI[3]))

# --- discriminar pergola de sebe -------------------------------------------
# A primeira tentativa usou so "DP alto" e falhou a inspeccao visual: alastrou
# para as parcelas pequenas a sul, que tem sebes e arvores dispersas — tambem
# textura alta — e perdeu a parte oriental do bloco. DP alto nao chega.
#
# A pergola distingue-se por ser textura ALTA e UNIFORME em grande area: postes
# em malha regular ao longo de hectares. Sebes e pomares mistos dao textura alta
# mas IRREGULAR — linear, aos bocados. Logo: media alta de DP numa janela de
# 50 m E desvio baixo de DP na mesma janela.
K = 5                                     # 50 m
mDP = ndimage.uniform_filter(DP, K)
sDP = np.sqrt(np.maximum(ndimage.uniform_filter(DP * DP, K) - mDP * mDP, 0))
homog = sDP / np.maximum(mDP, 1e-6)       # coeficiente de variacao da textura

lim_m = float(np.percentile(mDP, 55))
lim_h = float(np.percentile(homog, 45))
pergola = (mDP > lim_m) & (homog < lim_h)
pergola = ndimage.binary_closing(pergola, np.ones((3, 3)))
pergola = ndimage.binary_opening(pergola, np.ones((3, 3)))
pergola = ndimage.binary_fill_holes(pergola)
lab, n = ndimage.label(pergola)
if n:
    tam = ndimage.sum(pergola, lab, range(1, n + 1))
    pergola = lab == (int(np.argmax(tam)) + 1)
print("textura media > %.2f e CV < %.3f -> pomar %d celulas = %.2f ha"
      % (lim_m, lim_h, pergola.sum(), pergola.sum() / 100))

# --- referencia por amostragem sistematica ---------------------------------
# grelha regular de celulas 2x2 (20 m) de 8 em 8 celulas (80 m), so onde a
# celula inteira cai dentro do pomar e a 30 m da bordadura. Nenhuma e
# escolhida por aparencia.
interior = ndimage.binary_erosion(pergola, np.ones((7, 7)))
ref = np.zeros_like(pergola)
for i in range(2, ny - 2, 8):
    for j in range(2, nx - 2, 8):
        if interior[i:i + 2, j:j + 2].all():
            ref[i:i + 2, j:j + 2] = True
print("referencia sistematica: %d celulas = %.2f ha em %d blocos"
      % (ref.sum(), ref.sum() / 100, ref.sum() // 4))

antigas = json.load(open("sentinel/masks.json"))
saida = {
    "_metodo": "geografica, derivada da ortofoto DGT 2021 a 25 cm; NENHUMA "
               "mascara usa NDVI de nenhuma data",
    "_instrumento": ORTO,
    "_aoi_utm29n": list(AOI),
    "_grelha": "100 x 200 celulas de 10 m, alinhada com sentinel/*.tif",
    "pomar_bool": pergola.tolist(),
    "saudavel_bool": ref.tolist(),
    "zona0": antigas["zona0"],
    "_nota_zona0": "unica mascara do ficheiro antigo que era geografica; "
                   "mantida como estava",
    "_manchaW": "REMOVIDA. Era `pomar & (nd2026 < 0.76)` — definia a mancha "
                "pelo sinal que depois se media. As manchas passam a emergir "
                "do mapa de defice.",
}
with open("sentinel/masks_geograficas.json", "w", encoding="utf-8") as f:
    json.dump(saida, f)
print("\nsentinel/masks_geograficas.json gravado")

from matplotlib.path import Path as MP
yy, xx = np.mgrid[0:100, 0:200]
pts = np.vstack((xx.ravel(), yy.ravel())).T
velho = MP(antigas["pomar"]).contains_points(pts).reshape(100, 200)
inter = (pergola & velho).sum()
print("\nCOMPARACAO com a mascara antiga (circular):")
print("  pomar antigo   %.2f ha" % (velho.sum() / 100))
print("  pomar novo     %.2f ha" % (pergola.sum() / 100))
print("  interseccao    %.2f ha  (IoU %.3f)"
      % (inter / 100, inter / max((pergola | velho).sum(), 1)))
print("  so no antigo   %.2f ha" % ((velho & ~pergola).sum() / 100))
print("  so no novo     %.2f ha" % ((pergola & ~velho).sum() / 100))
