"""A Mancha W cresceu a partir de um nucleo, ou apareceu de uma vez dentro de
um limite recto? Discrimina propagacao biotica de falha hidraulica/gestao."""
import json, numpy as np, rasterio
from scipy import ndimage
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(v).contains_points(pts).reshape(100, 200) for k, v in masks.items()}
sau = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
DATAS = ["2024-07-22", "2025-06-17", "2025-08-14", "2026-07-27"]
pom = mk["pomar"]

def defice(dt, off=0.05):
    with rasterio.open(f"sentinel/{dt}.tif") as ds: nd = ds.read(1)
    ref = np.nanmean(nd[sau])
    return (nd < ref - off) & pom, nd, ref

print(f"{'data':12s} {'area defice no pomar':>21s} {'n manchas':>10s} "
      f"{'maior mancha':>13s} {'circularidade':>14s}")
info = {}
for dt in DATAS:
    m, nd, ref = defice(dt)
    m = ndimage.binary_opening(m, np.ones((2, 2)))
    lab, n = ndimage.label(m)
    if n == 0: continue
    tam = ndimage.sum(m, lab, range(1, n+1))
    i = 1 + int(np.argmax(tam)); big = lab == i
    per = big.sum() - ndimage.binary_erosion(big).sum()
    circ = 4*np.pi*big.sum()/max(per**2, 1)
    ys, xs = np.where(big)
    info[dt] = (m, big, xs.mean(), ys.mean())
    print(f"{dt:12s} {m.sum()/100:19.2f}ha {n:10d} {big.sum()/100:11.2f}ha {circ:14.3f}")

print("\ncentroide da maior mancha (pixel de 10 m) e deslocamento:")
prev = None
for dt in DATAS:
    if dt not in info: continue
    _, _, cx, cy = info[dt]
    dsl = "" if prev is None else f"  deslocou {np.hypot(cx-prev[0], cy-prev[1])*10:5.0f} m"
    print(f"  {dt}  centro=({cx:5.1f},{cy:5.1f}){dsl}")
    prev = (cx, cy)

# o crescimento e radial a partir do nucleo de 2025-06?
nuc = info["2025-06-17"][1]
dnuc = ndimage.distance_transform_edt(~nuc) * 10          # metros ate ao nucleo
print("\nDistancia ao nucleo de Jun/2025 dos pixels que passaram a defice depois:")
for dt in ("2025-08-14", "2026-07-27"):
    novo = info[dt][0] & ~info["2025-06-17"][0]
    dd = dnuc[novo]
    print(f"  {dt}: {novo.sum()/100:5.2f} ha novos | mediana {np.median(dd):5.0f} m "
          f"| p90 {np.percentile(dd,90):5.0f} m | adjacentes(<=20 m) {100*(dd<=20).mean():4.1f}%")

fig, axs = plt.subplots(1, 4, figsize=(24, 6))
for ax, dt in zip(axs, DATAS):
    if dt not in info: continue
    m = info[dt][0]
    ax.imshow(np.where(pom, 0.25, np.nan), cmap="Greys", vmin=0, vmax=1)
    ax.imshow(np.where(m, 1, np.nan), cmap="autumn_r", vmin=0, vmax=1.4)
    ax.contour(mk["manchaW"], levels=[.5], colors="#C2451E", linewidths=1.4)
    ax.contour(mk["zona0"], levels=[.5], colors="#E4A11B", linewidths=1.4)
    ax.contour(pom, levels=[.5], colors="k", linewidths=1.2)
    ax.set_title(f"{dt}  —  {m.sum()/100:.1f} ha", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Défice moderado (NDVI < ref−0,05) dentro do pomar", fontsize=13)
fig.tight_layout(); fig.savefig("espalhamento.png", dpi=145, bbox_inches="tight")
print("\n-> espalhamento.png")
