"""A componente difusa: metade do defice de 2026 esta fora dos dois focos.
E bordadura estrutural ou sao focos novos? Discriminador: distancia ao bordo
do pomar. Pixel misto de 10 m vive no bordo; foco real forma nucleo interior."""
import json, glob, os, csv, numpy as np, rasterio
from scipy import ndimage
from matplotlib.path import Path as MP
from rasterio.warp import transform as tr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"]|mk["saudavel_2"]|mk["saudavel_3"]
pom = mk["pomar"]; focos = mk["manchaW"] | mk["zona0"]
dbordo = ndimage.distance_transform_edt(pom)      # px ate ao bordo do pomar

def defice(d):
    with rasterio.open(f"sentinel/{d}.tif") as ds: nd = ds.read(1)
    ref = float(np.nanmean(nd[sau]))
    return (nd < ref-0.05) & pom, nd, ref

print("=== estrutura do defice FORA dos dois focos, por distancia ao bordo ===")
print(f"{'data':12s} " + " ".join(f"{f'{a}-{b}px':>9s}" for a,b in ((0,1),(1,2),(2,3),(3,99))))
for d in sorted(os.path.basename(p)[:-4] for p in glob.glob("sentinel/*.tif")):
    m,_,_ = defice(d); f = m & ~focos
    linha = []
    for a,b in ((0,1),(1,2),(2,3),(3,99)):
        linha.append(((dbordo > a) & (dbordo <= b) & f).sum()/100)
    print(f"{d:12s} " + " ".join(f"{v:8.2f}ha" for v in linha))
tot = (pom & (dbordo <= 1)).sum()/100
print(f"\n(area do pomar a <=1 px do bordo: {tot:.2f} ha de {pom.sum()/100:.2f} ha)")

# --- defice NOVO (2026 e nao 2024), fora dos focos, interior ---------------
m24,_,_ = defice("2024-07-22"); m26,_,_ = defice("2026-07-27")
novo = m26 & ~m24 & ~focos
interior = novo & (dbordo > 2)
print(f"\ndefice NOVO 2024->2026 fora dos focos: {novo.sum()/100:.2f} ha")
print(f"   do qual INTERIOR (>2 px do bordo): {interior.sum()/100:.2f} ha")
lab, n = ndimage.label(ndimage.binary_opening(interior, np.ones((2,2))))
print(f"\nnucleos interiores novos com >=0,15 ha:")
rows=[]
for i in range(1, n+1):
    m = lab == i
    if m.sum() < 15: continue
    ys, xs = np.where(m)
    E = AOI[0]+xs.mean()*10; N = AOI[3]-ys.mean()*10
    lo, la = tr("EPSG:32629","EPSG:4326",[E],[N])
    dW = np.hypot(xs.mean()-53.6, ys.mean()-54.8)*10   # ao centro da manchaW
    dZ = np.hypot(xs.mean()-102.1, ys.mean()-48.1)*10  # ao centro da zona0
    rows.append({"id":len(rows)+1,"ha":round(m.sum()/100,2),
        "centro_x":round(xs.mean(),1),"centro_y":round(ys.mean(),1),
        "UTM_E":round(E),"UTM_N":round(N),
        "lon":round(lo[0],6),"lat":round(la[0],6),
        "dist_manchaW_m":round(dW),"dist_zona0_m":round(dZ)})
    print(f"   #{rows[-1]['id']}  {rows[-1]['ha']:.2f} ha  E{rows[-1]['UTM_E']} N{rows[-1]['UTM_N']}"
          f"  ({rows[-1]['lon']:.5f}, {rows[-1]['lat']:.5f})"
          f"  a {dW:.0f} m da manchaW, {dZ:.0f} m da zona0")
if rows:
    with open("difusa_nucleos.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

with rasterio.open("sentinel/2026-07-27.tif") as ds: nd26 = ds.read(1)
fig, axs = plt.subplots(2,1,figsize=(17,11))
axs[0].imshow(nd26, cmap="RdYlGn", vmin=0.4, vmax=0.95, interpolation="bilinear")
axs[0].imshow(np.where(novo,1,np.nan), cmap="cool", vmin=0, vmax=1.6, interpolation="nearest")
axs[0].set_title("Defice NOVO 2024->2026 fora dos dois focos (ciano) sobre NDVI 2026", fontsize=12)
axs[1].imshow(np.where(interior,1,np.nan), cmap="autumn_r", vmin=0, vmax=1.4, interpolation="nearest")
axs[1].set_title("So a parte INTERIOR (>2 px do bordo) — candidatos a foco novo", fontsize=12)
for ax in axs:
    for k,c in (("pomar","k"),("manchaW","#C2451E"),("zona0","#E4A11B")):
        ax.contour(mk[k], levels=[.5], colors=c, linewidths=1.8)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("difusa.png", dpi=150, bbox_inches="tight")
print("\n-> difusa.png, difusa_nucleos.csv")
