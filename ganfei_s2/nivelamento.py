"""Houve nivelamento de terreno (corte/aterro do emparcelamento)?
Superficie nivelada = anormalmente planar, com quebras nitidas nos limites.
Corte remove horizonte superficial -> candidato a causa de mancha."""
import json, numpy as np, rasterio
from scipy import ndimage
from rasterio.warp import transform as tr
from matplotlib.path import Path as MP
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
d0 = np.load("lidar/t2_dem1m.npy"); meta = json.load(open("lidar/t2_dem1m.json"))
T0 = rasterio.Affine(*meta["transform"])
# recorte 3,4 x 2,2 km centrado no pomar — o resto do mosaico nao entra na conta
R0, R1, C0, C1 = 900, 3100, 1900, 5300
d = d0[R0:R1, C0:C1]
T = rasterio.Affine(T0.a, 0, T0.c + C0*T0.a, 0, T0.e, T0.f + R0*T0.e)
H, W = d.shape
print("recorte", d.shape)
val = ~np.isnan(d); terr = val & (d > 3) & (d < 12)
z = np.nan_to_num(d, nan=0.0)

def loc(a, m, s):
    num = ndimage.uniform_filter(np.where(m, a, 0.0), size=s)
    den = ndimage.uniform_filter(m.astype("float32"), size=s)
    return np.where(den > 0.05, num/np.maximum(den, 1e-6), np.nan)

# rugosidade: dp local a 25 m (planaridade da superficie)
m25 = loc(z, terr, 25)
rug = np.sqrt(np.maximum(loc((z - np.nan_to_num(m25))**2, terr, 25), 0))
rug[~terr] = np.nan
# residuo a 150 m: bancadas de corte/aterro
r150 = np.where(terr, d - loc(z, terr, 151), np.nan)

masks = json.load(open("sentinel/masks.json"))
gy, gx = np.mgrid[0:H, 0:W]; gp = np.vstack((gx.ravel(), gy.ravel())).T
def para(p):
    ux = [AOI[0] + q[0]*10 for q in p]; uy = [AOI[3] - q[1]*10 for q in p]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
mk = {k: MP(para(v)).contains_points(gp).reshape(H, W) for k, v in masks.items()}
mk["saudavel"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]
# terraco de referencia: fora do pomar, mais de 100 m dele
dist_pom = ndimage.distance_transform_edt(~mk["pomar"])
fora = terr & (dist_pom > 100)
print(f"{'zona':22s} {'rugosidade 25 m':>16s} {'residuo 150 m':>15s} {'n (ha)':>9s}")
for nm, m in (("terraco fora do pomar", fora), ("pomar", mk["pomar"] & terr),
              ("saudavel", mk["saudavel"] & terr), ("manchaW", mk["manchaW"] & terr),
              ("zona0", mk["zona0"] & terr)):
    a = rug[m]; a = a[~np.isnan(a)]; b = r150[m]; b = b[~np.isnan(b)]
    print(f"{nm:22s} {np.median(a):16.3f} {np.median(b):+15.3f} {m.sum()/1e4:9.1f}")

print("\nRugosidade — distribuicao (m):")
for nm, m in (("terraco fora", fora), ("pomar", mk["pomar"] & terr)):
    a = rug[m]; a = a[~np.isnan(a)]
    print(f"  {nm:14s} p10={np.percentile(a,10):.3f} p50={np.percentile(a,50):.3f} "
          f"p90={np.percentile(a,90):.3f}")

fig, axs = plt.subplots(1, 2, figsize=(22, 10))
im = axs[0].imshow(rug, cmap="magma", vmin=0, vmax=0.35)
axs[0].set_title("Rugosidade local (dp a 25 m) — escuro = superfície planar", fontsize=12)
fig.colorbar(im, ax=axs[0], shrink=.7, label="m")
im = axs[1].imshow(r150, cmap="RdBu", vmin=-0.6, vmax=0.6)
axs[1].set_title("Resíduo a 150 m — bancadas de corte (vermelho) e aterro (azul)", fontsize=12)
fig.colorbar(im, ax=axs[1], shrink=.7, label="m")
for ax in axs:
    for k, c in (("pomar","k"),("saudavel","#00b0a0"),("manchaW","#C2451E"),("zona0","#E4A11B")):
        ax.contour(mk[k], levels=[.5], colors=c, linewidths=1.8)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig("nivelamento.png", dpi=140, bbox_inches="tight")
print("\n-> nivelamento.png")
