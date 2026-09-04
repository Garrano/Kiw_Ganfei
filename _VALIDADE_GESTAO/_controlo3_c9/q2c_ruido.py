# -*- coding: utf-8 -*-
"""Q2c - o contraste de 0,312 m no GLO-30 esta acima do ruido do GLO-30?"""
import os, sys
import numpy as np, rasterio
from scipy import stats
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1")
from c1_00_comum import *
g=dict(np.load(os.path.join(SAIDA,"c1_03_grelha.npz")))
masc,_=carrega_mascaras(); pomar,saud=masc["pomar"],masc["saudavel"]
do,de=discos_dos_focos(pomar); resto=pomar&~do&~de
E29,N29=centros_celulas()
with rasterio.open(os.path.join(RAIZ,"lidar","_glo30.tif")) as s:
    glo=s.read(1).astype("float64"); Tg=s.transform; glo[glo<=-1000]=np.nan
lon,lat=T_29_TO_WGS.transform(E29.ravel(),N29.ravel())
cg=((np.asarray(lon)-Tg.c)/Tg.a).astype(int).reshape(E29.shape)
rg=((np.asarray(lat)-Tg.f)/Tg.e).astype(int).reshape(E29.shape)
gl=np.full(E29.shape,np.nan); gl[:]=glo[rg,cg]

def px(m):  # valores dos pixeis GLO-30 DISTINTOS sob a mascara
    d={}
    for i,j in zip(*np.nonzero(m)):
        d[(rg[i,j],cg[i,j])]=glo[rg[i,j],cg[i,j]]
    v=np.array(list(d.values())); return v[np.isfinite(v)]
O,E_,R,S=px(do),px(de),px(resto),px(saud)
for n,v in (("OCIDENTAL",O),("ORIENTAL",E_),("referencia",S),("resto",R)):
    print("  GLO-30 %-11s n_px=%3d  mediana %.3f  media %.3f  dp %.3f  EP da media %.3f"
          % (n,len(v),np.median(v),v.mean(),v.std(ddof=1),v.std(ddof=1)/np.sqrt(len(v))))
d=np.median(E_)-np.median(O)
sp=np.sqrt(((len(O)-1)*O.var(ddof=1)+(len(E_)-1)*E_.var(ddof=1))/(len(O)+len(E_)-2))
se=sp*np.sqrt(1/len(O)+1/len(E_))
print("\n  contraste GLO-30 ORIENTAL-OCIDENTAL = %+.3f m" % d)
print("  dp intra-unidade combinado = %.3f m  |  EP da diferenca = %.3f m" % (sp,se))
print("  d de Cohen = %.2f   (no LiDAR era 3.93)" % (d/sp))
t,p=stats.mannwhitneyu(E_,O,alternative="two-sided")
print("  Mann-Whitney ao nivel do PIXEL GLO-30 (n=%d vs %d): p = %.4f" % (len(E_),len(O),p))
print("  IC95 aprox. do contraste GLO-30: %+.3f .. %+.3f m" % (d-1.96*se, d+1.96*se))
print("\n  o limiar do script c1_10 era dg > 0.300 -> passou por %.3f m." % (d-0.300))
print("  O IC95 %s o limiar de 0,300 m." % ("CONTEM" if (d-1.96*se)<0.300<(d+1.96*se) else "NAO contem"))
