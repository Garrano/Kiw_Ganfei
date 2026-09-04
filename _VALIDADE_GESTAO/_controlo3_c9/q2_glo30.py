# -*- coding: utf-8 -*-
"""Q2 - o GLO-30 confirma, e com que forca?"""
import os, sys, json, itertools
import numpy as np, rasterio
from scipy import stats
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1")
from c1_00_comum import *

g=dict(np.load(os.path.join(SAIDA,"c1_03_grelha.npz")))
masc,_=carrega_mascaras()
pomar,saud,zona0,nu2021=masc["pomar"],masc["saudavel"],masc["zona0"],masc["nu2021"]
do,de=discos_dos_focos(pomar); resto=pomar&~do&~de
E29,N29=centros_celulas()

with rasterio.open(os.path.join(RAIZ,"lidar","_glo30.tif")) as s:
    glo=s.read(1).astype("float64"); Tg=s.transform; glo[glo<=-1000]=np.nan
    print("GLO-30: %s  px %.6f deg = %.1f m  crs %s" % (glo.shape, Tg.a, Tg.a*111320*np.cos(np.radians(42.05)), s.crs))
lon,lat=T_29_TO_WGS.transform(E29.ravel(),N29.ravel())
cg=((np.asarray(lon)-Tg.c)/Tg.a).astype(int).reshape(E29.shape)
rg=((np.asarray(lat)-Tg.f)/Tg.e).astype(int).reshape(E29.shape)
ok=(cg>=0)&(cg<glo.shape[1])&(rg>=0)&(rg<glo.shape[0])
gl=np.full(E29.shape,np.nan); gl[ok]=glo[rg[ok],cg[ok]]

U=[("foco OCIDENTAL",do),("foco ORIENTAL",de),("referencia",saud),("resto do pomar",resto)]
print("\n%-18s %5s %9s %9s %10s" % ("unidade","n","LiDAR","GLO-30","px GLO-30"))
L={};G={};NPX={}
for nome,m in U:
    a=np.nanmedian(g["cota"][m]); b=np.nanmedian(gl[m])
    npx=len(set(zip(rg[m].tolist(),cg[m].tolist())))
    L[nome]=a;G[nome]=b;NPX[nome]=npx
    print("%-18s %5d %9.3f %9.3f %10d" % (nome,m.sum(),a,b,npx))

nomes=[n for n,_ in U]
oL=sorted(nomes,key=lambda k:L[k]); oG=sorted(nomes,key=lambda k:G[k])
print("\nordenacao LiDAR  (baixo->alto): %s" % " < ".join(oL))
print("ordenacao GLO-30 (baixo->alto): %s" % " < ".join(oG))
print("as duas ordenacoes coincidem? %s" % (oL==oG))
rho,prho=stats.spearmanr([L[n] for n in nomes],[G[n] for n in nomes])
print("Spearman entre as 4 unidades: rho=%+.3f  p=%.3f  (4 pontos: p minimo possivel = %.4f)"
      % (rho,prho,2/24))

print("\n--- probabilidade de coincidencia por acaso ---")
print("  4 unidades -> 4! = 24 ordenacoes. P(ordenacao exacta ao acaso) = 1/24 = %.4f" % (1/24))
print("  Mas so o SINAL este-menos-oeste e que a peca cita: 2 unidades -> P = 1/2 = 0.5000")
print("  E o teste do proprio script c1_10 e `dg > 0.3 and abs(dg-dl) < 1.5`.")
dl=L["foco ORIENTAL"]-L["foco OCIDENTAL"]; dg=G["foco ORIENTAL"]-G["foco OCIDENTAL"]
print("  dg = %.4f m  contra o limiar 0.300 -> margem de %.4f m (%.1f %%)" % (dg,dg-0.3,100*(dg-0.3)/0.3))
print("  dl = %.4f m  |  razao dg/dl = %.3f  (o GLO-30 ve %.0f %% do contraste)" % (dl,dg/dl,100*dg/dl))

print("\n--- e as OUTRAS 3 diferencas entre pares? ---")
for a,b in itertools.combinations(nomes,2):
    sL=np.sign(L[a]-L[b]); sG=np.sign(G[a]-G[b])
    print("  %-18s vs %-18s  LiDAR %+7.3f  GLO-30 %+7.3f   sinal %s"
          % (a,b,L[a]-L[b],G[a]-G[b],"IGUAL" if sL==sG else "*** INVERTIDO ***"))

print("\n--- n efectivo da correlacao r=0.452 ---")
m=pomar&~np.isnan(gl)&~np.isnan(g["cota"])
r,p=stats.pearsonr(g["cota"][m],gl[m])
npx=len(set(zip(rg[m].tolist(),cg[m].tolist())))
print("  celulas de 10 m: %d  ->  p reportado %.1e" % (m.sum(),p))
print("  pixeis GLO-30 DISTINTOS por tras dessas celulas: %d" % npx)
# recalcular ao nivel do pixel GLO-30
import collections
acc=collections.defaultdict(list)
for i,j in zip(*np.nonzero(m)):
    acc[(rg[i,j],cg[i,j])].append(g["cota"][i,j])
xs=np.array([np.mean(v) for v in acc.values()])
ys=np.array([glo[k[0],k[1]] for k in acc.keys()])
q=np.isfinite(xs)&np.isfinite(ys)
r2,p2=stats.pearsonr(xs[q],ys[q])
print("  agregando ao pixel GLO-30 (n=%d): r=%+.3f  p=%.3f" % (q.sum(),r2,p2))
