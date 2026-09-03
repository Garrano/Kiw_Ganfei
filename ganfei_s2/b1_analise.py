"""Serie do lobulo oeste (B1) contra a referencia sa do corpo principal."""
import json, csv, glob, os, numpy as np, rasterio
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

with rasterio.open("sentinel_b1/2026-07-27.tif") as ds: n26 = ds.read(1)
dist = ndimage.distance_transform_edt(~(n26 < 0.25))
cop = ndimage.binary_opening((n26 > 0.78) & (dist > 5), np.ones((2,2)))
lab, n = ndimage.label(cop)
tam = ndimage.sum(cop, lab, range(1, n+1))
B1 = lab == (1 + int(np.argmax(tam)))
B1 = ndimage.binary_fill_holes(ndimage.binary_closing(B1, np.ones((5,5))))
print(f"mascara B1: {B1.sum()/100:.2f} ha")
# referencia interna do B1: nucleo uniforme, >=3 px do bordo
interior = ndimage.binary_erosion(B1, np.ones((7,7)))
ref_int = interior & (n26 > 0.87)
l2, n2 = ndimage.label(ref_int)
if n2:
    t2 = ndimage.sum(ref_int, l2, range(1, n2+1))
    ref_int = l2 == (1 + int(np.argmax(t2)))
print(f"referencia interna B1: {ref_int.sum()/100:.2f} ha")

principal = {r["data"]: r for r in csv.DictReader(open("expansao.csv", encoding="utf-8"))}
datas = sorted(os.path.basename(p)[:-4] for p in glob.glob("sentinel_b1/*.tif"))
linhas = []
print(f"\n{'data':12s} {'B1 NDVI':>8s} {'ref principal':>14s} {'B1 - ref':>9s} "
      f"{'pomar principal':>16s} {'manchaW':>8s} {'defice B1':>10s}")
for d in datas:
    with rasterio.open(f"sentinel_b1/{d}.tif") as ds: nd = ds.read(1)
    v = nd[B1]; v = v[~np.isnan(v)]
    ref = float(principal[d]["ref_saudavel_media"])
    pom = float(principal[d]["pomar_ndvi_medio"]); mw = float(principal[d]["manchaW_ndvi_medio"])
    dfm = float(np.nansum(nd[B1] < ref - 0.05))/100
    r = {"data": d, "b1_ndvi_medio": round(float(v.mean()), 4),
         "b1_ndvi_mediana": round(float(np.median(v)), 4),
         "ref_saudavel_principal": ref, "b1_menos_ref": round(float(v.mean())-ref, 4),
         "b1_defice_moderado_ha": round(dfm, 2),
         "b1_defice_moderado_pct": round(100*dfm/(B1.sum()/100), 1),
         "pomar_principal_ndvi": pom, "manchaW_ndvi": mw}
    linhas.append(r)
    print(f"{d:12s} {r['b1_ndvi_medio']:8.3f} {ref:14.3f} {r['b1_menos_ref']:+9.3f} "
          f"{pom:16.3f} {mw:8.3f} {r['b1_defice_moderado_pct']:9.1f}%")
with open("expansao_b1.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)

xs = [r["data"] for r in linhas]
fig, axs = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
axs[0].plot(xs, [r["ref_saudavel_principal"] for r in linhas], "-o", color="#2f6e26",
            lw=2, label="zona sa (corpo principal)")
axs[0].plot(xs, [r["pomar_principal_ndvi"] for r in linhas], "-o", color="#5B6152",
            lw=2, label="pomar (corpo principal)")
axs[0].plot(xs, [r["b1_ndvi_medio"] for r in linhas], "-o", color="#1f4fd8", lw=2.5,
            label="B1 (lobulo oeste)")
axs[0].plot(xs, [r["manchaW_ndvi"] for r in linhas], "-o", color="#C2451E", lw=2,
            label="manchaW")
axs[0].set_ylabel("NDVI medio"); axs[0].grid(alpha=.25); axs[0].legend(frameon=False, ncol=2)
axs[0].set_title("B1 (lobulo oeste, fora da AOI original) contra o corpo principal")
axs[1].bar(xs, [r["b1_defice_moderado_pct"] for r in linhas], color="#1f4fd8")
axs[1].set_ylabel("% do B1 abaixo de ref-0,05"); axs[1].grid(alpha=.25, axis="y")
plt.xticks(rotation=45, ha="right"); fig.tight_layout(); fig.savefig("b1_serie.png", dpi=150)
print("\n-> expansao_b1.csv, b1_serie.png")
