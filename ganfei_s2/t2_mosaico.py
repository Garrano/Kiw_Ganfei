"""Mosaico T2 (21 tiles, 12,6 km2) a 1 m + verificacao de degrau entre as duas
campanhas de voo (Ago/2025 vs Jan/2026)."""
import json, glob, os, urllib.request, ssl, numpy as np, rasterio
from rasterio.merge import merge

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
u = ("https://dgt-be.a.incd.pt:8081/collections/MDT-50cm/items?f=json&limit=400"
     "&bbox=-8.660,42.035,-8.600,42.058")
with urllib.request.urlopen(u, timeout=120, context=ctx) as r: meta = json.load(r)
voo = {f["id"]: f["properties"]["datetime"][:10] for f in meta.get("data", meta)["features"]}

paths = sorted(glob.glob("lidar/MDT-50cm-*.tif"))
info = {}
for p in paths:
    tid = os.path.basename(p).replace("_v02.tif", "")
    with rasterio.open(p) as ds: info[tid] = (tuple(ds.bounds), voo.get(tid, "?"))
campanhas = {}
for t, (b, d) in info.items(): campanhas.setdefault(d, []).append(t)
print("campanhas de voo:")
for d in sorted(campanhas): print(f"  {d}: {len(campanhas[d])} tiles")

# --- degrau nas fronteiras entre campanhas diferentes -----------------------
print("\nfronteiras entre campanhas distintas (faixa de 20 m de cada lado):")
diffs = []
for a, (ba, da) in info.items():
    for b_, (bb, db) in info.items():
        if a >= b_ or da == db: continue
        # adjacencia horizontal: ba.right == bb.left
        if abs(ba[2] - bb[0]) < 1 and not (ba[3] <= bb[1] or ba[1] >= bb[3]):
            with rasterio.open(f"lidar/{a}_v02.tif") as d1, rasterio.open(f"lidar/{b_}_v02.tif") as d2:
                v1 = d1.read(1, window=((0, d1.height), (d1.width-40, d1.width))).astype("float32")
                v2 = d2.read(1, window=((0, d2.height), (0, 40))).astype("float32")
            v1[v1 == -999] = np.nan; v2[v2 == -999] = np.nan
            if np.isnan(v1).all() or np.isnan(v2).all(): continue
            dd = np.nanmean(v2) - np.nanmean(v1)
            diffs.append(dd); print(f"  {a}({da}) | {b_}({db})  delta = {dd:+.3f} m")
        if abs(ba[1] - bb[3]) < 1 and not (ba[2] <= bb[0] or ba[0] >= bb[2]):
            with rasterio.open(f"lidar/{a}_v02.tif") as d1, rasterio.open(f"lidar/{b_}_v02.tif") as d2:
                v1 = d1.read(1, window=((d1.height-40, d1.height), (0, d1.width))).astype("float32")
                v2 = d2.read(1, window=((0, 40), (0, d2.width))).astype("float32")
            v1[v1 == -999] = np.nan; v2[v2 == -999] = np.nan
            if np.isnan(v1).all() or np.isnan(v2).all(): continue
            dd = np.nanmean(v2) - np.nanmean(v1)
            diffs.append(dd); print(f"  {a}({da}) / {b_}({db})  delta = {dd:+.3f} m")
if diffs:
    print(f"\n  n={len(diffs)}  media {np.mean(diffs):+.3f} m  dp {np.std(diffs):.3f} m  "
          f"|max| {np.max(np.abs(diffs)):.3f} m")

srcs = [rasterio.open(p) for p in paths]
mos, T0 = merge(srcs, nodata=-999.0)
d = mos[0][::2, ::2].astype("float32")
T = rasterio.Affine(T0.a*2, 0, T0.c, 0, T0.e*2, T0.f)
d[d == -999.0] = np.nan
print(f"\nmosaico T2 @1 m: {d.shape} = {d.shape[1]/1000:.1f} x {d.shape[0]/1000:.1f} km"
      f"  nodata {100*np.isnan(d).mean():.1f}%")
print(f"cota {np.nanmin(d):.1f}..{np.nanmax(d):.1f} m")
np.save("lidar/t2_dem1m.npy", d)
json.dump({"transform": [T.a, T.b, T.c, T.d, T.e, T.f], "shape": list(d.shape),
           "crs": "EPSG:3763", "campanhas": {k: len(v) for k, v in campanhas.items()}},
          open("lidar/t2_dem1m.json", "w"))
print("-> lidar/t2_dem1m.npy")
