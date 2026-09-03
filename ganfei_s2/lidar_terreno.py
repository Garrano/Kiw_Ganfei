"""Micro-topografia: depressoes fechadas e relevo relativo sobre as mascaras."""
import json, numpy as np
from scipy import ndimage
from skimage.morphology import reconstruction
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

dem = np.load("lidar/dem_aoi.npy")
mk = np.load("lidar/masks_mdt.npy")
nomes = ["pomar", "saudavel", "manchaW", "zona0"]
pom = mk[0]
ys, xs = np.where(pom)
m0, m1 = max(0, ys.min()-300), min(dem.shape[0], ys.max()+300)
n0, n1 = max(0, xs.min()-300), min(dem.shape[1], xs.max()+300)
d = dem[m0:m1, n0:n1]; mks = mk[:, m0:m1, n0:n1]
d = d[::2, ::2]; mks = mks[:, ::2, ::2]          # 1 m chega para micro-relevo
print("janela de analise", d.shape, "@ 1 m")

val = ~np.isnan(d)
w = d.copy(); w[~val] = np.nanmax(d)             # nodata nao pode agir como sumidouro

# --- depressoes fechadas: enchimento por reconstrucao morfologica ---
sem = w.copy()
sem[1:-1, 1:-1] = w.max()
cheio = reconstruction(sem, w, method="erosion")
prof = cheio - w                                  # profundidade da depressao
prof[~val] = np.nan
print(f"depressoes: {np.nansum(prof > 0.05)/1e4:.2f} ha com >5 cm de profundidade")

# --- relevo relativo: cota menos a cota media num raio de 50 m ---
suave = ndimage.uniform_filter(np.nan_to_num(w, nan=np.nanmean(w)), size=101)
rel = d - suave
rel[~val] = np.nan

print(f"\n{'mascara':10s} {'cota media':>11s} {'relevo rel.':>12s} {'% em depressao':>15s} "
      f"{'prof. media':>12s}")
for i, nm in enumerate(nomes):
    m = mks[i] & val
    if not m.sum(): continue
    pd = prof[m]; pd = pd[~np.isnan(pd)]
    print(f"{nm:10s} {np.nanmean(d[m]):11.3f} {np.nanmean(rel[m]):+12.3f} "
          f"{100*(pd > 0.05).mean():15.1f} {pd[pd > 0.05].mean() if (pd>0.05).any() else 0:12.3f}")

fig, axs = plt.subplots(3, 1, figsize=(16, 15))
for ax, arr, kw, t in (
    (axs[0], d, dict(cmap="terrain"), "MDT 50 cm (cota, m)"),
    (axs[1], rel, dict(cmap="RdBu_r", vmin=-0.6, vmax=0.6), "Relevo relativo (cota - media 100 m)"),
    (axs[2], np.where(prof > 0.05, prof, np.nan), dict(cmap="Blues", vmin=0, vmax=0.5),
     "Depressoes fechadas (profundidade, m)")):
    im = ax.imshow(arr, **kw, interpolation="nearest")
    for i, (nm, c) in enumerate(zip(nomes, ("k", "#00b0a0", "#C2451E", "#E4A11B"))):
        ax.contour(mks[i], levels=[0.5], colors=c, linewidths=1.6)
    ax.set_title(t, fontsize=11); ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(im, ax=ax, shrink=.8)
fig.suptitle("Ganfei — micro-topografia LiDAR (preto=pomar, verde=sa, vermelho=manchaW, "
             "amarelo=zona0)", fontsize=12)
fig.tight_layout(); fig.savefig("lidar_terreno.png", dpi=140, bbox_inches="tight")
print("\n-> lidar_terreno.png")
