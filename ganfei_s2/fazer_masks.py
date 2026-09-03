"""Rascunho de sentinel/masks.json sobre o recorte de 2026, segundo as regras
acordadas. Poligonos em coordenadas de PIXEL, como o process_sentinel.py espera.
NOTA: o process_sentinel.py aceita UM poligono por chave, sem buracos — a
exclusao de caminhos finos interiores nao e representavel; ver relatorio."""
import json, numpy as np, rasterio
from scipy import ndimage
from skimage import measure

with rasterio.open("sentinel/2026-07-27.tif") as ds:
    nd = ds.read(1)

agua = nd < 0.25
dist = ndimage.distance_transform_edt(~agua)          # px ate a agua
copado = ndimage.binary_opening((nd > 0.78) & (dist > 5), np.ones((2, 2)))
lab, n = ndimage.label(copado)

# componentes do pomar: lente + escada NE (ver relatorio de segmentacao)
ALVO = [(68, 51), (125, 32), (139, 24), (153, 17)]     # centros aproximados
sel = np.zeros_like(copado)
for cx, cy in ALVO:
    ys, xs = np.where(lab > 0)
    i = lab[int(cy), int(cx)]
    if i == 0:                                          # apanhar vizinho
        jj = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
        i = lab[ys[jj], xs[jj]]
    sel |= (lab == i)

def disco(r):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    return x*x + y*y <= r*r

# fechar para unir talhoes e engolir as manchas interiores; reimpor a galeria fora
pomar = ndimage.binary_closing(sel, disco(6))
pomar = ndimage.binary_fill_holes(pomar) & (dist > 4)
l2, n2 = ndimage.label(pomar)
pomar = l2 == (1 + np.argmax(ndimage.sum(pomar, l2, range(1, n2 + 1))))
pomar = ndimage.binary_fill_holes(pomar)
print(f"pomar: {pomar.sum()} px = {pomar.sum()/100:.1f} ha")

def contorno(m, tol=1.2):
    c = max(measure.find_contours(m.astype(float), 0.5), key=len)
    p = measure.approximate_polygon(c, tolerance=tol)
    return [[round(float(x), 1), round(float(y), 1)] for y, x in p]

# --- saudavel: dentro do copado, centro-este da lente, >=3 px de bordadura ---
nucleo = pomar & (nd > 0.85)
nucleo &= ndimage.binary_erosion(pomar, disco(3))      # >=30 m de qualquer bordo
janela = np.zeros_like(nucleo); janela[38:53, 60:92] = True   # faixa norte, centro-este
cand_bruto = nucleo & janela

# --- manchaW: nucleo palido oeste-central, margem de 3 px ---
baixo = pomar & (nd < 0.76)
jw = np.zeros_like(baixo); jw[44:68, 36:72] = True
mw = baixo & jw
l4, n4 = ndimage.label(mw)
mw = l4 == (1 + np.argmax(ndimage.sum(mw, l4, range(1, n4 + 1))))
mw = ndimage.binary_dilation(mw, disco(3)) & pomar
print(f"manchaW: {mw.sum()} px = {mw.sum()/100:.2f} ha")

# --- zona0: baixo vigor no extremo este da lente + faixa adjacente ---
jz = np.zeros_like(baixo); jz[46:72, 74:102] = True
z0 = (pomar & (nd < 0.80)) & jz
l5, n5 = ndimage.label(z0)
z0 = l5 == (1 + np.argmax(ndimage.sum(z0, l5, range(1, n5 + 1))))
z0 = ndimage.binary_dilation(z0, disco(3)) & pomar
print(f"zona0:   {z0.sum()} px = {z0.sum()/100:.2f} ha")

# saudavel: >=5 px de qualquer mancha (regra acordada: longe das duas)
longe = ~ndimage.binary_dilation(mw | z0, disco(5))
cand = cand_bruto & longe
l3, n3 = ndimage.label(cand)
cand = l3 == (1 + np.argmax(ndimage.sum(cand, l3, range(1, n3 + 1))))
print(f"saudavel: {cand.sum()} px, NDVI medio {np.nanmean(nd[cand]):.3f}, "
      f"dp {np.nanstd(nd[cand]):.3f}, limiar que gera = "
      f"{np.nanmean(nd[cand]) - 2*np.nanstd(nd[cand]):.3f}")

masks = {"pomar": contorno(pomar), "saudavel": contorno(cand, 0.8),
         "manchaW": contorno(mw, 0.8), "zona0": contorno(z0, 0.8)}
for k, v in masks.items(): print(f"  {k}: {len(v)} vertices")
json.dump(masks, open("sentinel/masks.json", "w"), indent=1)
print("-> sentinel/masks.json")
