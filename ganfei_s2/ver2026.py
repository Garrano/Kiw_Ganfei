import numpy as np, rasterio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
with rasterio.open("sentinel/2026-07-27.tif") as ds:
    nd = ds.read(1)
print("shape", nd.shape)
fig, ax = plt.subplots(figsize=(26, 14))
ax.imshow(nd, cmap="RdYlGn", vmin=0.35, vmax=0.95, interpolation="nearest")
h, w = nd.shape
ax.set_xticks(range(0, w+1, 10)); ax.set_yticks(range(0, h+1, 5))
ax.grid(color="k", lw=.35, alpha=.45)
ax.tick_params(labelsize=7)
# contornos de apoio
ax.contour(nd, levels=[0.55, 0.75, 0.85], colors=["k","b","w"], linewidths=.6)
ax.set_title("2026-07-27 NDVI — coordenadas de PIXEL (x=coluna, y=linha) — contornos 0.55/0.75/0.85", fontsize=11)
fig.savefig("ndvi2026_pixels.png", dpi=145, bbox_inches="tight")
