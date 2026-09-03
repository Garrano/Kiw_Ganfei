"""Os tres ultimos por exportar: bacia contribuinte, rugosidade/nivelamento,
e degrau entre campanhas de voo LiDAR."""
import csv, json, glob, os, numpy as np, rasterio
from scipy import ndimage
from matplotlib.path import Path as MP
from rasterio.warp import transform as tr
from pysheds.grid import Grid
AOI = (529950, 4654600, 531950, 4655600)
masks = json.load(open("sentinel/masks.json"))
yy, xx = np.mgrid[0:100, 0:200]
pm = MP(masks["pomar"]).contains_points(
        np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)

# ---------- 1. BACIA CONTRIBUINTE (GLO-30 + pysheds) -----------------------
grid = Grid.from_raster("lidar/_glo30.tif")
dem = grid.read_raster("lidar/_glo30.tif")
dem = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(dem)))
fdir = grid.flowdir(dem); acc = np.asarray(grid.accumulation(fdir))
with rasterio.open("lidar/_glo30.tif") as ds: T = ds.transform
py, px = np.where(pm)
glo, gla = tr("EPSG:32629", "EPSG:4326", list(AOI[0]+px*10), list(AOI[3]-py*10))
cel = {}
for x, y in zip(glo, gla):
    c = int((x-T.c)/T.a); r = int((y-T.f)/T.e)
    if 0 <= r < acc.shape[0] and 0 <= c < acc.shape[1]: cel[(r, c)] = (acc[r, c], x, y)
top = sorted(cel.values(), key=lambda t: -t[0])[:40]
uni = np.zeros(acc.shape, bool)
for a, x, y in top:
    uni |= np.asarray(grid.catchment(x=x, y=y, fdir=fdir, xytype="coordinate"))
pomc = np.zeros(acc.shape, bool)
for (r, c) in cel: pomc[r, c] = True
ys, xs = np.where(uni)
lon = T.c + (xs+.5)*T.a; lat = T.f + (ys+.5)*T.e
TILES = {"158564":(-8.6404,42.0354,-8.6282,42.0445),"158565":(-8.6405,42.0444,-8.6283,42.0535),
         "159564":(-8.6283,42.0355,-8.6162,42.0445),"159565":(-8.6284,42.0445,-8.6162,42.0535),
         "160564":(-8.6162,42.0355,-8.6041,42.0446),"160565":(-8.6163,42.0445,-8.6042,42.0536)}
rows=[{"item":"bacia_total","valor_ha":round(uni.sum()*900/1e4,2),"nota":"uniao de 40 exutorios"},
      {"item":"fora_do_pomar","valor_ha":round((uni&~pomc).sum()*900/1e4,2),"nota":""},
      {"item":"celulas_30m_sobre_pomar","valor_ha":round(pomc.sum()*900/1e4,2),"nota":""}]
for k,(a,b,c,d) in sorted(TILES.items()):
    m=(lon>=a)&(lon<c)&(lat>=b)&(lat<d)
    if m.sum(): rows.append({"item":f"tile_{k}","valor_ha":round(m.sum()*900/1e4,2),
                             "nota":f"{100*m.sum()/uni.sum():.1f}% da bacia"})
with open("pendente_bacia.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["item","valor_ha","nota"]); w.writeheader(); w.writerows(rows)
print(f"bacia: {rows[0]['valor_ha']} ha ({rows[1]['valor_ha']} fora do pomar)")

# ---------- 2. RUGOSIDADE / NIVELAMENTO -------------------------------------
d0 = np.load("lidar/t2_dem1m.npy"); meta = json.load(open("lidar/t2_dem1m.json"))
T0 = rasterio.Affine(*meta["transform"])
R0,R1,C0,C1 = 900,3100,1900,5300
d = d0[R0:R1, C0:C1]
T2 = rasterio.Affine(T0.a,0,T0.c+C0*T0.a,0,T0.e,T0.f+R0*T0.e)
H,W = d.shape; val = ~np.isnan(d); terr = val & (d>3) & (d<12)
z = np.nan_to_num(d)
def loc(a,m,s):
    num=ndimage.uniform_filter(np.where(m,a,0.0),size=s)
    den=ndimage.uniform_filter(m.astype("float32"),size=s)
    return np.where(den>0.05,num/np.maximum(den,1e-6),np.nan)
m25=loc(z,terr,25)
rug=np.sqrt(np.maximum(loc((z-np.nan_to_num(m25))**2,terr,25),0)); rug[~terr]=np.nan
r150=np.where(terr, d-loc(z,terr,151), np.nan)
gy,gx=np.mgrid[0:H,0:W]; gp=np.vstack((gx.ravel(),gy.ravel())).T
def para(p):
    ux=[AOI[0]+q[0]*10 for q in p]; uy=[AOI[3]-q[1]*10 for q in p]
    ex,ny=tr("EPSG:32629","EPSG:3763",ux,uy)
    return [[(x-T2.c)/T2.a,(y-T2.f)/T2.e] for x,y in zip(ex,ny)]
mk={k:MP(para(v)).contains_points(gp).reshape(H,W) for k,v in masks.items()}
mk["saudavel"]=mk["saudavel"]|mk["saudavel_2"]|mk["saudavel_3"]
fora = terr & (ndimage.distance_transform_edt(~mk["pomar"])>100)
rows=[]
for nm,m in (("terraco_fora_do_pomar",fora),("pomar",mk["pomar"]&terr),
             ("saudavel",mk["saudavel"]&terr),("manchaW",mk["manchaW"]&terr),
             ("zona0",mk["zona0"]&terr)):
    a=rug[m]; a=a[~np.isnan(a)]; b=r150[m]; b=b[~np.isnan(b)]
    rows.append({"zona":nm,"ha":round(m.sum()/1e4,2),
        "rugosidade_25m_p10":round(float(np.percentile(a,10)),3),
        "rugosidade_25m_mediana":round(float(np.median(a)),3),
        "rugosidade_25m_p90":round(float(np.percentile(a,90)),3),
        "residuo_150m_mediana_m":round(float(np.median(b)),3)})
with open("pendente_nivelamento.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(f"rugosidade {r['zona']:22s} p10-p90 {r['rugosidade_25m_p10']}-{r['rugosidade_25m_p90']}"
                     f" | residuo150 {r['residuo_150m_mediana_m']:+.3f}")

# ---------- 3. DEGRAU ENTRE CAMPANHAS DE VOO --------------------------------
import urllib.request, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
u=("https://dgt-be.a.incd.pt:8081/collections/MDT-50cm/items?f=json&limit=400"
   "&bbox=-8.660,42.035,-8.600,42.058")
with urllib.request.urlopen(u,timeout=120,context=ctx) as r: meta2=json.load(r)
voo={f["id"]:f["properties"]["datetime"][:10] for f in meta2.get("data",meta2)["features"]}
info={}
for p in sorted(glob.glob("lidar/MDT-50cm-*.tif")):
    t=os.path.basename(p).replace("_v02.tif","")
    with rasterio.open(p) as ds: info[t]=(tuple(ds.bounds),voo.get(t,"?"),p)
def edge(p,s):
    with rasterio.open(p) as ds:
        w={"R":((0,ds.height),(ds.width-1,ds.width)),"L":((0,ds.height),(0,1)),
           "B":((ds.height-1,ds.height),(0,ds.width)),"T":((0,1),(0,ds.width))}[s]
        a=ds.read(1,window=w).astype("float32")
    a[a==-999]=np.nan; return a.ravel()
rows=[]
for a,(ba,da,pa) in info.items():
    for b,(bb,db,pb) in info.items():
        if a>=b: continue
        if abs(ba[2]-bb[0])<1 and not (ba[3]<=bb[1] or ba[1]>=bb[3]):
            v1,v2=edge(pa,"R"),edge(pb,"L"); tipo="vertical"
        elif abs(ba[1]-bb[3])<1 and not (ba[2]<=bb[0] or ba[0]>=bb[2]):
            v1,v2=edge(pa,"B"),edge(pb,"T"); tipo="horizontal"
        else: continue
        n=min(v1.size,v2.size); dif=v2[:n]-v1[:n]; m=~np.isnan(dif)
        if m.sum()<200: continue
        rows.append({"tile_a":a[-13:-8],"tile_b":b[-13:-8],"voo_a":da,"voo_b":db,
            "mesma_campanha":da==db,"tipo":tipo,"n_px":int(m.sum()),
            "costura_completa":int(m.sum())>=1900,
            "mediana_dif_m":round(float(np.median(dif[m])),4),
            "dp_dif_m":round(float(np.std(dif[m])),4)})
with open("pendente_degrau_campanhas.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
comp=[r for r in rows if r["costura_completa"]]
mesma=[r["mediana_dif_m"] for r in comp if r["mesma_campanha"]]
outra=[r["mediana_dif_m"] for r in comp if not r["mesma_campanha"]]
print(f"\ndegrau (so costuras completas): mesma campanha n={len(mesma)} mediana "
      f"{np.median(mesma):+.4f} m | campanhas diferentes n={len(outra)} mediana {np.median(outra):+.4f} m")
