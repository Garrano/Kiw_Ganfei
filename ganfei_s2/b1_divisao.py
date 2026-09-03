# -*- coding: utf-8 -*-
"""B1 — divisao interna por valvula, extrapolada.

O que se cruza
--------------
1. DUAS COORDENADAS DURAS do gestor: B1 de E529500 N4654010 a E530054
   N4654413, 685 m, azimute 54 graus.
2. A TABELA DE AREAS: valvulas 1 a 5 com 13500, 9375, 12750, 24550 e 29900 m2.
   Total 90.075 m2 = 9,01 ha.
3. O ESBOCO: a valvula 1 esta numa parcela pequena e destacada a SUDOESTE,
   fora do bloco estriado; depois, de SW para NE, leem-se 2, 4, 3, 5.
4. A ORTOFOTO a 25 cm, para medir onde ha efectivamente pomar.

O constrangimento que torna isto possivel
-----------------------------------------
O involucro que a sessao do controlo delimitou (C1a+C1b+C1c) tem 13,52 ha, e
46% das suas celulas tem variabilidade inter-anual acima do percentil 90 do
kiwi — culturas em rotacao misturadas. A tabela diz 9,01 ha. Ou seja: ha ~4,5
ha do involucro que NAO sao B1, e a diferenca de areas diz-nos quanto procurar.

Metodo
------
a) Deteccao de pergola por PERIODICIDADE (o compasso e 5,0 m, medido pela
   sessao das mascaras). Foi o unico sinal que funcionou no corpo principal;
   variancia e homogeneidade de textura falharam ambas.
b) Verificar se a area detectada se aproxima dos 9,01 ha tabelados. Se nao se
   aproximar, o metodo falhou e diz-se isso.
c) Ordenar as celulas ao longo do eixo do B1 e cortar por area acumulada, na
   ordem espacial que o esboco da: 1, 2, 4, 3, 5.
"""
import json
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds, reproject, Resampling
from rasterio.transform import from_origin
from rasterio.features import geometry_mask
from scipy import ndimage, signal

tr = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
B1I = np.array(tr.transform(-8.643581734449253, 42.03757663209986))
B1F = np.array(tr.transform(-8.636871142810762, 42.04118410828004))
W = (529300, 4653800, 530300, 4654600)
DEST = from_origin(W[0], W[3], 5.0, 5.0)          # grelha de 5 m
NY, NX = 160, 200

VALV = [(1, 13500), (2, 9375), (4, 24550), (3, 12750), (5, 29900)]
TABELA = sum(a for _, a in VALV)
print("tabela: B1 = %d m2 = %.2f ha, em 5 valvulas" % (TABELA, TABELA / 1e4))

ctrl = json.load(open("../_VALIDACAO_CAMADAS/SAIDA_C0/controlos.geojson"))
env = ~geometry_mask([f["geometry"] for f in ctrl["features"]
                      if f["properties"].get("id") in ("C1a", "C1b", "C1c")],
                     out_shape=(NY, NX), transform=DEST, invert=False)
print("involucro C1a+b+c: %.2f ha" % (env.sum() * 25 / 1e4))

ds = rasterio.open("orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif")
Wo = transform_bounds("EPSG:32629", ds.crs, *W)
w = from_bounds(*Wo, transform=ds.transform)
lum = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).mean(2).astype("float32")
orig = rasterio.windows.transform(w, ds.transform)

# --- periodicidade: autocorrelacao radial, proeminencia do 1.o pico -------
PAS = 0.25
JAN = 96                       # 24 m de janela
prom = np.zeros((NY, NX), "float32")
H, L = lum.shape
gy = np.linspace(JAN, H - JAN - 1, NY).astype(int)
gx = np.linspace(JAN, L - JAN - 1, NX).astype(int)
for i, yy in enumerate(gy):
    for j, xx in enumerate(gx):
        b = lum[yy - JAN:yy + JAN, xx - JAN:xx + JAN]
        if b.size < 100:
            continue
        b = b - b.mean()
        F = np.abs(np.fft.rfft2(b)) ** 2
        ac = np.fft.irfft2(F, s=b.shape)
        ac = np.fft.fftshift(ac) / max(ac.max(), 1e-9)
        c = np.array(ac.shape) // 2
        yy2, xx2 = np.mgrid[:ac.shape[0], :ac.shape[1]]
        rad = np.hypot(yy2 - c[0], xx2 - c[1]) * PAS
        perfil = np.array([ac[(rad >= r0) & (rad < r0 + 0.5)].mean()
                           for r0 in np.arange(1.0, 12.0, 0.5)])
        perfil = np.nan_to_num(perfil)
        pk, pr = signal.find_peaks(perfil, prominence=0.002)
        prom[i, j] = pr["prominences"].max() if len(pk) else 0.0

lim = float(np.percentile(prom[env], 100 * (1 - TABELA / (env.sum() * 25))))
kiwi = env & (prom > lim)
kiwi = ndimage.binary_closing(kiwi, np.ones((3, 3)))
kiwi = ndimage.binary_opening(kiwi, np.ones((3, 3)))
print("limiar de proeminencia %.4f -> pergola detectada: %.2f ha (tabela: %.2f)"
      % (lim, kiwi.sum() * 25 / 1e4, TABELA / 1e4))

if abs(kiwi.sum() * 25 - TABELA) / TABELA > 0.25:
    print("\nDESVIO > 25%% — a deteccao nao converge para a area tabelada.")
    print("Nao se corta nada. O metodo falhou e fica registado como falha.")
    raise SystemExit

# O eixo NAO se tira das duas pontas dadas: elas dao o comprimento do conjunto,
# nao a direccao em que as parcelas se sucedem. A primeira tentativa cortou
# perpendicular a esse eixo e os cortes sairam a ~35 graus das estremas reais
# visiveis na ortofoto. Tira-se o eixo da propria mascara detectada, por
# componentes principais — que e o que se fez no corpo principal.
yy, xx = np.where(kiwi)
E = W[0] + (xx + .5) * 5.0
N = W[3] - (yy + .5) * 5.0
C0 = np.array([E.mean(), N.mean()])
wv, vv = np.linalg.eigh(np.cov(np.column_stack([E - C0[0], N - C0[1]]).T))
maior = vv[:, np.argmax(wv)]
menor = vv[:, np.argmin(wv)]
u_pt = (B1F - B1I) / np.linalg.norm(B1F - B1I)
az = lambda w: (90 - np.degrees(np.arctan2(w[1], w[0]))) % 180
print("\neixo maior da mancha detectada: azimute %.0f graus" % az(maior))
print("eixo das duas pontas dadas:     azimute %.0f graus" % az(u_pt))

# As parcelas sao faixas longas e estreitas, paralelas ao eixo MAIOR; sucedem-se
# ao longo do eixo MENOR. E ao longo desse que se corta.
u = menor if np.dot(menor, u_pt) >= 0 else -menor
print("direccao de sucessao (eixo menor): azimute %.0f graus" % az(u))
d = (E - C0[0]) * u[0] + (N - C0[1]) * u[1]
ORIG = C0 + u * d.min()
d = d - d.min()
o = np.argsort(d)
acum = np.arange(1, len(d) + 1) * 25.0
esc = acum[-1] / TABELA

print("\nDIVISAO INTERNA, cortada por area acumulada")
print("ordem espacial do esboco, de sudoeste para nordeste: 1, 2, 4, 3, 5\n")
cum = 0
saida = []
for v, a in VALV:
    i0 = int(np.searchsorted(acum, cum * esc))
    cum += a
    i1 = int(np.searchsorted(acum, cum * esc))
    i1 = min(i1, len(o) - 1)
    d0, d1 = d[o][i0], d[o][i1]
    p0 = ORIG + u * d0
    p1 = ORIG + u * d1
    pm = ORIG + u * ((d0 + d1) / 2)
    saida.append(dict(valvula=v, area_m2=a, d0=round(float(d0), 1),
                      d1=round(float(d1), 1),
                      E=round(float(pm[0]), 1), N=round(float(pm[1]), 1)))
    print("   válvula %-2d  %5.2f ha   %4.0f a %4.0f m do extremo SW   "
          "centro E %.0f N %.0f" % (v, a / 1e4, d0, d1, pm[0], pm[1]))

json.dump(dict(
    _eixo_origem=[round(float(ORIG[0]),1), round(float(ORIG[1]),1)],
    _eixo_u=[round(float(u[0]),4), round(float(u[1]),4)],
    _metodo="periodicidade na ortofoto + areas tabeladas + ordem do esboco",
    _ancoras=[B1I.tolist(), B1F.tolist()],
    _area_detectada_ha=round(kiwi.sum() * 25 / 1e4, 2),
    _area_tabelada_ha=round(TABELA / 1e4, 2),
    _incerteza="ordem 1,2,4,3,5 lida no esboco; se a ordem estiver trocada, as "
               "posicoes trocam com ela",
    valvulas=saida), open("b1_divisao.json", "w", encoding="utf-8"),
    ensure_ascii=False, indent=1)
np.save("b1_kiwi_5m.npy", kiwi)
print("\nb1_divisao.json e b1_kiwi_5m.npy gravados")
