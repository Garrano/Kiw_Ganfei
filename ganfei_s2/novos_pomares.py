"""A conduta foi prolongada para NOVOS pomares. Quando entraram ao servico?
Deteccao por satelite: blocos que passaram de uso anual/variavel a copado
permanente de vigor alto, e o ano em que isso aconteceu."""
import json, requests, numpy as np, rasterio
from concurrent.futures import ThreadPoolExecutor
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

W = (528200, 4653800, 532600, 4656200)      # 4,4 x 2,4 km em torno da exploracao
E = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
prov = json.load(open("sentinel/proveniencia.json"))
anuais = [c for c in prov["cenas"] if c["data"][:4] != "2025" or c["data"] == "2025-08-14"]

def uma(c):
    a = requests.get("https://earth-search.aws.element84.com/v1/collections/"
                     f"sentinel-2-l2a/items/{c['cena']}", timeout=90).json()["assets"]
    def rd(k, shape=None):
        with rasterio.Env(**E), rasterio.open(a[k]["href"]) as ds:
            w = from_bounds(*W, transform=ds.transform)
            if shape is None: return ds.read(1, window=w).astype("float32")
            return ds.read(1, window=w, out_shape=shape,
                           resampling=Resampling.nearest).astype("float32")
    nir = rd("nir"); red = rd("red"); scl = rd("scl", nir.shape)
    with np.errstate(invalid="ignore", divide="ignore"):
        nd = (nir-red)/(nir+red)
    nd[np.isin(scl.astype(int), [0,1,3,8,9,10])] = np.nan
    return c["data"][:4], nd

with ThreadPoolExecutor(max_workers=6) as ex:
    res = dict(ex.map(uma, anuais))
anos = sorted(res)
cubo = np.stack([res[a] for a in anos])
print("anos:", anos, "| janela", cubo.shape[1:])

# copado permanente: NDVI de verao > 0.80
cop = cubo > 0.80
# "novo" = <=1 ano com copado nos primeiros 4 anos, e >=3 dos ultimos 4 com copado
antes = cop[:4].sum(0); depois = cop[-4:].sum(0)
novo = (antes <= 1) & (depois >= 3)
novo = ndimage.binary_opening(novo, np.ones((3,3)))
lab, n = ndimage.label(novo)
print(f"\nblocos NOVOS de copado permanente (>=0,5 ha):")
tot = 0
for i in range(1, n+1):
    m = lab == i
    if m.sum() < 50: continue
    # primeiro ano em que passou a copado de forma sustentada
    serie = [float(np.nanmean(cubo[k][m])) for k in range(len(anos))]
    prim = next((anos[k] for k in range(len(anos))
                 if all(serie[j] > 0.78 for j in range(k, min(k+3, len(anos))))), "?")
    ys, xs = np.where(m); tot += m.sum()
    print(f"  {m.sum()/100:5.2f} ha  entra em {prim}  "
          f"E {W[0]+xs.min()*10:.0f}..{W[0]+xs.max()*10:.0f} "
          f"N {W[3]-ys.max()*10:.0f}..{W[3]-ys.min()*10:.0f}")
    print(f"        NDVI por ano: " + " ".join(f"{a[2:]}={v:.2f}" for a, v in zip(anos, serie)))
print(f"\nTOTAL de copado novo: {tot/100:.2f} ha")
fig, ax = plt.subplots(figsize=(15, 8))
ax.imshow(cubo[-1], cmap="RdYlGn", vmin=0.3, vmax=0.95)
ax.contour(novo, levels=[.5], colors="blue", linewidths=1.8)
ax.set_title("Copado permanente NOVO (azul) sobre NDVI 2026", fontsize=12)
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("novos_pomares.png", dpi=145, bbox_inches="tight")
print("-> novos_pomares.png")
