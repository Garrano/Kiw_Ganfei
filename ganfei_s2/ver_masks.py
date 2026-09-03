import json, numpy as np, rasterio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
with rasterio.open("sentinel/2026-07-27.tif") as ds:
    nd = ds.read(1)
m = json.load(open("sentinel/masks.json"))
cores = {"pomar": "#1f4fd8", "saudavel": "#00b0a0", "manchaW": "#C2451E", "zona0": "#E4A11B"}
fig, ax = plt.subplots(figsize=(20, 10))
ax.imshow(nd, cmap="RdYlGn", vmin=0.35, vmax=0.95, interpolation="bilinear")
for k, pts in m.items():
    ax.add_patch(Polygon(pts, closed=True, fill=False, ec=cores[k], lw=2.4 if k=="pomar" else 2.0,
                         ls="-" if k != "saudavel" else "--", label=k))
ax.legend(loc="lower right", fontsize=11, framealpha=.9)
ax.set_title("Rascunho das mascaras sobre NDVI 2026-07-27 (AOI 2x1 km)", fontsize=13)
ax.set_xticks(range(0, 201, 20)); ax.set_yticks(range(0, 101, 10)); ax.grid(alpha=.2, lw=.4)
fig.tight_layout(); fig.savefig("masks_2026.png", dpi=160, bbox_inches="tight")
print("ok")
