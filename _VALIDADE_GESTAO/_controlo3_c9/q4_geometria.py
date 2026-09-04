# -*- coding: utf-8 -*-
"""Q4 - o bordo do MDT, o B1, e os '445 m'."""
import os, sys, json
import numpy as np
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely.ops import transform as sht, unary_union

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"

DEMJ = json.load(open(os.path.join(VC,"SAIDA_C1","c1_03_dem50.json"), encoding="utf-8"))
t=DEMJ["transform"]; ny,nx=DEMJ["shape"]; x0,y0,px=t[2],t[5],t[0]
print("DEM em EPSG:3763 : X %.1f .. %.1f   Y %.1f .. %.1f  (%d x %d px @ %.2f m)"
      % (x0, x0+nx*px, y0-ny*px, y0, ny, nx, px))

tr = Transformer.from_crs("EPSG:3763","EPSG:32629",always_xy=True)
# (1) como a P10 faz: so os 4 cantos
cx=[x0, x0+nx*px, x0, x0+nx*px]; cy=[y0,y0,y0-ny*px,y0-ny*px]
DX,DY = tr.transform(cx,cy)
BB_P10=(min(DX),min(DY),max(DX),max(DY))
print("\n(1) bbox pelos 4 CANTOS (metodo da P10):  E %.1f..%.1f  N %.1f..%.1f"
      % (BB_P10[0],BB_P10[2],BB_P10[1],BB_P10[3]))
# (2) densificando o bordo (o rectangulo em 3763 nao e rectangulo em 32629)
ss=np.linspace(0,1,2001)
bx=np.concatenate([x0+ss*nx*px, np.full_like(ss,x0+nx*px), x0+ss*nx*px, np.full_like(ss,x0)])
by=np.concatenate([np.full_like(ss,y0), y0-ss*ny*px, np.full_like(ss,y0-ny*px), y0-ss*ny*px])
EX,NY = tr.transform(bx,by)
BB_D=(min(EX),min(NY),max(EX),max(NY))
print("(2) bbox pelo bordo DENSIFICADO:          E %.1f..%.1f  N %.1f..%.1f"
      % (BB_D[0],BB_D[2],BB_D[1],BB_D[3]))
print("    diferenca canto-vs-denso: dN_sul %+.1f m  dN_norte %+.1f m  dE_oeste %+.1f  dE_este %+.1f"
      % (BB_D[1]-BB_P10[1], BB_D[3]-BB_P10[3], BB_D[0]-BB_P10[0], BB_D[2]-BB_P10[2]))

# --- o B1, pelos poligonos do IFAP ---
CUL_B1={6476415,8845729,6476420,8845739,8845740,6476425}
trw=Transformer.from_crs("EPSG:4326","EPSG:32629",always_xy=True)
K=json.load(open(os.path.join(H2,"ifap_kiwi_largo.json"),encoding="utf-8"))
KF=K["features"] if isinstance(K,dict) else K
gs=[]
for f in KF:
    if int(f["properties"]["CUL_ID"]) in CUL_B1:
        gs.append(sht(lambda x,y,z=None: trw.transform(x,y), shape(f["geometry"])).buffer(0))
U=unary_union(gs)
b=U.bounds
print("\nB1 (%d parcelas, %.2f ha): E %.1f..%.1f  N %.1f..%.1f"
      % (len(gs), U.area/1e4, b[0],b[2],b[1],b[3]))

print("\n=== os '445 m' ===")
print("  bordo SUL do DEM      N = %.1f" % BB_D[1])
print("  bordo NORTE do B1     N = %.1f" % b[3])
print("  bordo SUL   do B1     N = %.1f" % b[1])
print("  DEM_sul - B1_sul   = %+.1f m   <-- o numero da peca (445)" % (BB_D[1]-b[1]))
print("  DEM_sul - B1_norte = %+.1f m   <-- a folga REAL entre as duas caixas" % (BB_D[1]-b[3]))

# sobreposicao real
DEMBOX=box(BB_D[0],BB_D[1],BB_D[2],BB_D[3])
inter=U.intersection(DEMBOX)
print("\n  area do B1 dentro da CAIXA do DEM: %.3f ha de %.3f ha (%.1f %%)"
      % (inter.area/1e4, U.area/1e4, 100*inter.area/U.area))
print("  distancia geometrica B1 -> caixa do DEM: %.1f m" % U.distance(DEMBOX))
