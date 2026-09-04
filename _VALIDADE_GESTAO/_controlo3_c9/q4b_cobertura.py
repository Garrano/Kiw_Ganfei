# -*- coding: utf-8 -*-
"""Q4b - o MDT tem DADO sobre a parte do B1 que cai dentro da sua caixa?"""
import os, json
import numpy as np
from pyproj import Transformer
from shapely.geometry import shape, box, Point
from shapely.ops import transform as sht, unary_union
from matplotlib.path import Path as MPath

VC=r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
H2=r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
DEMJ=json.load(open(os.path.join(VC,"SAIDA_C1","c1_03_dem50.json"),encoding="utf-8"))
t=DEMJ["transform"]; ny,nx=DEMJ["shape"]; L,T0,px=t[2],t[5],t[0]
dem=np.load(os.path.join(VC,"SAIDA_C1","c1_03_dem50.npy"), mmap_mode="r")
camp=np.load(os.path.join(VC,"SAIDA_C1","c1_03_camp50.npy"), mmap_mode="r")
print("DEM %s  |  NaN global: %.2f %%" % (dem.shape, 100*np.isnan(np.array(dem[::7,::7])).mean()))

tr29_3763=Transformer.from_crs("EPSG:32629","EPSG:3763",always_xy=True)
trw=Transformer.from_crs("EPSG:4326","EPSG:32629",always_xy=True)
CUL_B1={6476415,8845729,6476420,8845739,8845740,6476425}
K=json.load(open(os.path.join(H2,"ifap_kiwi_largo.json"),encoding="utf-8"))
KF=K["features"] if isinstance(K,dict) else K
polys=[]
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL_B1:
        polys.append((int(f["properties"]["CUL_ID"]),
                      sht(lambda x,y,z=None: trw.transform(x,y), shape(f["geometry"])).buffer(0)))
U=unary_union([p for _,p in polys])

# amostrar o B1 numa malha de 2 m em UTM, converter a 3763, ler o DEM
b=U.bounds
ex=np.arange(b[0], b[2], 2.0); ny_=np.arange(b[1], b[3], 2.0)
EX,NY=np.meshgrid(ex,ny_)
dentro=np.zeros(EX.shape,bool)
for _,p in polys:
    pth=MPath(np.array(p.exterior.coords))
    dentro |= pth.contains_points(np.c_[EX.ravel(),NY.ravel()]).reshape(EX.shape)
print("pontos de amostra dentro do B1 (malha 2 m): %d  = %.2f ha" % (dentro.sum(), dentro.sum()*4/1e4))

X,Y=tr29_3763.transform(EX[dentro],NY[dentro])
c=np.round((np.asarray(X)-L)/px-0.5).astype(int)
r=np.round((T0-np.asarray(Y))/px-0.5).astype(int)
dentro_caixa=(c>=0)&(c<nx)&(r>=0)&(r<ny)
print("  dos quais dentro da CAIXA do DEM      : %d  (%.1f %%)  = %.2f ha"
      % (dentro_caixa.sum(), 100*dentro_caixa.mean(), dentro_caixa.sum()*4/1e4))
z=np.full(c.shape,np.nan)
if dentro_caixa.any():
    z[dentro_caixa]=np.array(dem)[r[dentro_caixa],c[dentro_caixa]]
com=np.isfinite(z)
print("  dos quais com COTA valida no MDT      : %d  (%.1f %%)  = %.2f ha"
      % (com.sum(), 100*com.mean(), com.sum()*4/1e4))
if com.any():
    print("  cota do B1 coberto: mediana %.3f m  p5 %.3f  p95 %.3f  (n=%d)"
          % (np.nanmedian(z[com]), np.nanpercentile(z[com],5), np.nanpercentile(z[com],95), com.sum()))
    cc=np.array(camp)[r[dentro_caixa],c[dentro_caixa]]
    import collections
    print("  campanha de voo dessas celulas:", dict(collections.Counter(cc.tolist())))
    # por parcela
    print("\n  por parcela CUL_ID:")
    for cid,p in polys:
        pth=MPath(np.array(p.exterior.coords))
        sel=pth.contains_points(np.c_[EX[dentro],NY[dentro]])
        n=sel.sum(); nc=(com&sel).sum()
        print("    %-9d  %.2f ha  cobertura MDT %5.1f %%   cota mediana %s"
              % (cid, p.area/1e4, 100*nc/max(n,1),
                 ("%.2f m"%np.nanmedian(z[sel&com])) if nc else "-"))
