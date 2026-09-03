"""Secagem SAR, bacia e escoamento — os restantes nao exportados."""
import csv, json, glob, requests, numpy as np, rasterio, datetime as dt
from scipy import ndimage
from matplotlib.path import Path as MP
from rasterio.merge import merge
from rasterio.warp import transform as tr
from pysheds.grid import Grid

# ---------- 1. secagem do solo por SAR --------------------------------------
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    "latitude": 42.047, "longitude": -8.626, "start_date": "2022-10-01",
    "end_date": "2025-04-30", "daily": "precipitation_sum", "timezone": "UTC"},
    timeout=180).json()["daily"]
chuva = {dt.date.fromisoformat(a): (b or 0.0) for a, b in
         zip(r["time"], r["precipitation_sum"])}
def dias_desde(d, lim=5.0):
    for k in range(0, 30):
        if chuva.get(d - dt.timedelta(days=k), 0) >= lim: return k
    return 30
sar = list(csv.DictReader(open("sar_invernos.csv", encoding="utf-8")))
for x in sar:
    x["dias_desde_chuva5mm"] = dias_desde(dt.date.fromisoformat(x["data"]))
with open("pendente_sar_secagem.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(sar[0].keys())); w.writeheader(); w.writerows(sar)
rows=[]
for nm in ("saudavel","manchaW","zona0"):
    for orb in ("125","147"):
        s=[x for x in sar if x["orbita"]==orb]
        d=np.array([x["dias_desde_chuva5mm"] for x in s],float)
        v=np.array([float(x[f"{nm}_vv_db"]) for x in s])
        m=d<=14
        A=np.polyfit(d[m],v[m],1)
        rows.append({"mascara":nm,"orbita":orb,"n":int(m.sum()),
            "declive_dB_por_dia":round(float(A[0]),4),
            "r":round(float(np.corrcoef(d[m],v[m])[0,1]),3),
            "vv_0a1dia":round(float(v[d<=1].mean()),2) if (d<=1).any() else "",
            "vv_ge7dias":round(float(v[d>=7].mean()),2) if (d>=7).any() else ""})
with open("pendente_sar_declives.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("secagem SAR:", " | ".join(f"{r['mascara']}/{r['orbita']}={r['declive_dB_por_dia']}" for r in rows))

# ---------- 2. escoamento sobre o MDT LiDAR ---------------------------------
AOI=(529950,4654600,531950,4655600)
srcs=[rasterio.open(p) for p in sorted(glob.glob("lidar/MDT-50cm-*.tif"))]
mos,T0=merge(srcs,nodata=-999.0)
d=mos[0][::2,::2].astype("float32"); T=rasterio.Affine(T0.a*2,0,T0.c,0,T0.e*2,T0.f)
d[d==-999.0]=np.nan; d=np.where(np.isnan(d),np.nanmax(d)+5,d)
with rasterio.open("lidar/_mdt1m.tif","w",driver="GTiff",height=d.shape[0],width=d.shape[1],
                   count=1,dtype="float32",crs="EPSG:3763",transform=T,nodata=-9999.0) as o:
    o.write(d,1)
grid=Grid.from_raster("lidar/_mdt1m.tif"); dem=grid.read_raster("lidar/_mdt1m.tif")
dem=grid.resolve_flats(grid.fill_depressions(grid.fill_pits(dem)))
acc=np.asarray(grid.accumulation(grid.flowdir(dem)))
masks=json.load(open("sentinel/masks.json"))
H,W=acc.shape; gy,gx=np.mgrid[0:H,0:W]; gp=np.vstack((gx.ravel(),gy.ravel())).T
def para(p):
    ux=[AOI[0]+q[0]*10 for q in p]; uy=[AOI[3]-q[1]*10 for q in p]
    ex,ny=tr("EPSG:32629","EPSG:3763",ux,uy)
    return [[(x-T.c)/T.a,(y-T.f)/T.e] for x,y in zip(ex,ny)]
mk={k:MP(para(v)).contains_points(gp).reshape(H,W) for k,v in masks.items()}
mk["saudavel"]=mk["saudavel"]|mk["saudavel_2"]|mk["saudavel_3"]
rows=[]
for k in ("pomar","saudavel","manchaW","zona0"):
    m=mk[k]; a=acc[m]
    rows.append({"mascara":k,"ha":round(m.sum()/1e4,2),
        "pct_em_linha_drenagem_2000m2":round(float(100*(a>2000).mean()),2),
        "acumulacao_mediana_m2":int(np.median(a)),
        "acumulacao_p95_m2":int(np.percentile(a,95)),
        "acumulacao_max_m2":int(a.max())})
with open("pendente_escoamento.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(f"escoamento {r['mascara']:9s} {r['pct_em_linha_drenagem_2000m2']:5.2f}% em linha")
