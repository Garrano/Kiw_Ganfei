"""masks.json v2 — regras D1-D3 da sessao de 28/08/2026.

Principios:
 * poligonos GEOGRAFICOS e ESTATICOS; nenhum e re-derivado por data.
 * `pomar` = copado 2026 dentro da AOI (nao tenta reconciliar com as 44,9 ha
   da tabela de valvulas: essas incluem parcelas satelite, caminhos, cabeceiras
   e area de projecto de rega). Tudo se reporta em % desta mascara.
 * `saudavel` em 3 manchas dispersas (>=3 ha no total) para a referencia ter
   variabilidade real — a regra media-2DP morreu por causa disso.
   process_sentinel.py so le "saudavel"; o pos-processamento une as tres.
 * `zona0` = sub-parcela de linhas no extremo ESTE da lente, a oeste do caminho
   que a separa da escada NE. Definida pela geometria, nao por limiar.
"""
import json, numpy as np, rasterio
from scipy import ndimage
from skimage import measure
from matplotlib.path import Path as MP

with rasterio.open("sentinel/2026-07-27.tif") as ds:
    nd = ds.read(1)
H, W = nd.shape
dist = ndimage.distance_transform_edt(~(nd < 0.25))
copado = ndimage.binary_opening((nd > 0.78) & (dist > 5), np.ones((2, 2)))
lab, _ = ndimage.label(copado)

def disco(r):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    return x*x + y*y <= r*r

def contorno(m, tol=1.0):
    c = max(measure.find_contours(m.astype(float), 0.5), key=len)
    p = measure.approximate_polygon(c, tolerance=tol)
    return [[round(float(x), 1), round(float(y), 1)] for y, x in p]

def rasteriza(poly):
    yy, xx = np.mgrid[0:H, 0:W]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(H, W)

# zona0: sub-parcela de linhas no extremo ESTE da lente, a oeste do caminho que
# a separa da escada NE. Poligono fixo, tracado sobre a geometria — nao por limiar.
Z0 = [[97, 43], [112, 43], [115, 48], [113, 54], [106, 57], [99, 56], [95, 49]]

# ---- pomar: lente + escada NE + zona0, galeria ripicola fora -----------------
sel = np.zeros_like(copado)
for cy, cx in ((51, 68), (32, 125), (24, 139), (17, 153)):
    i = lab[cy, cx]
    if i == 0:
        ys, xs = np.where(lab > 0)
        j = np.argmin((xs - cx)**2 + (ys - cy)**2); i = lab[ys[j], xs[j]]
    sel |= (lab == i)
# a Zona 0 e pomar: linhas mortas, NDVI baixo, logo fora do `copado` — entra
# explicitamente, senao a mascara do pomar exclui justamente a origem do declinio
pomar = ndimage.binary_closing(sel | rasteriza(Z0), disco(6))
pomar = ndimage.binary_fill_holes(pomar) & (dist > 4)
l2, n2 = ndimage.label(pomar)
pomar = ndimage.binary_fill_holes(l2 == 1 + np.argmax(ndimage.sum(pomar, l2, range(1, n2+1))))
z0 = rasteriza(Z0) & pomar

# ---- manchaW: footprint 2026, oeste-central (limitacao registada, D5) --------
jw = np.zeros_like(pomar); jw[44:68, 36:72] = True
mw = pomar & (nd < 0.76) & jw
l4, n4 = ndimage.label(mw)
mw = l4 == 1 + np.argmax(ndimage.sum(mw, l4, range(1, n4+1)))
mw = ndimage.binary_dilation(mw, disco(3)) & pomar

# ---- zona0: geometrica, extremo este da lente, a oeste do caminho -----------

# ---- saudavel: 3 manchas dispersas dentro do copado -------------------------
CAND = {"saudavel":   [[72, 40], [90, 40], [90, 56], [72, 56]],    # centro-este da lente
        "saudavel_2": [[90, 32], [110, 32], [110, 38], [90, 38]],  # lobo nordeste da lente
        "saudavel_3": [[133, 21], [145, 21], [145, 31], [133, 31]]}  # talhao da escada NE
interior = ndimage.binary_erosion(pomar, disco(3))       # >=30 m de qualquer bordo
longe = ~ndimage.binary_dilation(mw | z0, disco(5))
sau = {}
for k, poly in CAND.items():
    m = rasteriza(poly) & interior & longe & copado
    sau[k] = m
    v = nd[m]
    print(f"{k:11s} {m.sum():4d} px = {m.sum()/100:4.2f} ha  "
          f"NDVI {v.mean():.4f} +- {v.std():.4f}")
uni = np.zeros_like(pomar)
for m in sau.values(): uni |= m
v = nd[uni]
print(f"{'UNIAO':11s} {uni.sum():4d} px = {uni.sum()/100:4.2f} ha  "
      f"NDVI {v.mean():.4f} +- {v.std():.4f}")

for nm, m in (("pomar", pomar), ("manchaW", mw), ("zona0", z0)):
    print(f"{nm:11s} {m.sum():4d} px = {m.sum()/100:5.2f} ha")

masks = {"pomar": contorno(pomar)}
for k, m in sau.items(): masks[k] = contorno(m, 0.6)
masks["manchaW"] = contorno(mw, 0.8)
masks["zona0"] = contorno(z0, 0.6)
json.dump(masks, open("sentinel/masks.json", "w"), indent=1)
print("\n-> sentinel/masks.json  (chaves:", ", ".join(masks), ")")
