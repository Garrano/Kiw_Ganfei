"""Mosaico dos tiles MDT 50 cm em EPSG:3763, recorte a AOI, mascaras reprojectadas.
Trabalha no CRS nativo do LiDAR — reprojectar o MDT suavizaria o micro-relevo."""
import json, glob, numpy as np, rasterio
from rasterio.merge import merge
from rasterio.warp import transform_bounds, transform as tr
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
srcs = [rasterio.open(p) for p in sorted(glob.glob("lidar/MDT-50cm-*.tif"))]
mos, trf = merge(srcs, nodata=-999.0)
mos = mos[0]
print(f"mosaico {mos.shape} @ {trf.a:.2f} m")

b3763 = transform_bounds("EPSG:32629", "EPSG:3763", *AOI)
c0 = int((b3763[0] - trf.c) / trf.a); c1 = int((b3763[2] - trf.c) / trf.a)
r0 = int((b3763[3] - trf.f) / trf.e); r1 = int((b3763[1] - trf.f) / trf.e)
c0, c1 = max(0, c0), min(mos.shape[1], c1)
r0, r1 = max(0, r0), min(mos.shape[0], r1)
dem = mos[r0:r1, c0:c1].astype("float32")
T = rasterio.Affine(trf.a, 0, trf.c + c0*trf.a, 0, trf.e, trf.f + r0*trf.e)
dem[dem == -999.0] = np.nan
print(f"recorte AOI {dem.shape}  nodata {100*np.isnan(dem).mean():.2f}%")
H, W = dem.shape

# mascaras: pixel da grelha S2 -> UTM29N -> EPSG:3763 -> pixel do MDT
masks = json.load(open("sentinel/masks.json"))
def para_mdt(poly):
    ux = [AOI[0] + p[0]*10 for p in poly]; uy = [AOI[3] - p[1]*10 for p in poly]
    ex, ny = tr("EPSG:32629", "EPSG:3763", ux, uy)
    return [[(x - T.c)/T.a, (y - T.f)/T.e] for x, y in zip(ex, ny)]
yy, xx = np.mgrid[0:H, 0:W]; pts = np.vstack((xx.ravel(), yy.ravel())).T
mk = {k: MP(para_mdt(v)).contains_points(pts).reshape(H, W) for k, v in masks.items()}
mk["saudavel_uniao"] = mk["saudavel"] | mk["saudavel_2"] | mk["saudavel_3"]

print(f"\n{'mascara':15s} {'px':>9s} {'ha':>6s} {'nodata %':>9s} {'altitude media':>15s} {'dp':>6s}")
for k in ("pomar", "saudavel_uniao", "manchaW", "zona0"):
    m = mk[k]; v = dem[m]
    nn = np.isnan(v).mean()*100
    vv = v[~np.isnan(v)]
    print(f"{k:15s} {m.sum():9d} {m.sum()*0.25/1e4:6.2f} {nn:9.2f} "
          f"{vv.mean():15.3f} {vv.std():6.3f}")
np.save("lidar/dem_aoi.npy", dem)
json.dump({"transform": [T.a, T.b, T.c, T.d, T.e, T.f], "shape": list(dem.shape),
           "crs": "EPSG:3763"}, open("lidar/dem_aoi.json", "w"))
np.save("lidar/masks_mdt.npy", np.stack([mk[k] for k in
        ("pomar", "saudavel_uniao", "manchaW", "zona0")]))
print("\n-> lidar/dem_aoi.npy + masks_mdt.npy")
