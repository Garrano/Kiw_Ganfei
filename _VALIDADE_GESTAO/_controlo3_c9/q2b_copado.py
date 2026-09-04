# -*- coding: utf-8 -*-
"""Q2b - o contraste que o GLO-30 ve e do CHAO ou do COPADO?
GLO-30 e um MDS. Se a diferenca GLO30-LiDAR seguir a altura do copado,
a 'confirmacao' nao e do terreno."""
import os, sys, json
import numpy as np, rasterio
from scipy import stats
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1")
from c1_00_comum import *
VG=r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"

g=dict(np.load(os.path.join(SAIDA,"c1_03_grelha.npz")))
masc,_=carrega_mascaras(); pomar,saud=masc["pomar"],masc["saudavel"]
do,de=discos_dos_focos(pomar); resto=pomar&~do&~de
E29,N29=centros_celulas()
with rasterio.open(os.path.join(RAIZ,"lidar","_glo30.tif")) as s:
    glo=s.read(1).astype("float64"); Tg=s.transform; glo[glo<=-1000]=np.nan
lon,lat=T_29_TO_WGS.transform(E29.ravel(),N29.ravel())
cg=((np.asarray(lon)-Tg.c)/Tg.a).astype(int).reshape(E29.shape)
rg=((np.asarray(lat)-Tg.f)/Tg.e).astype(int).reshape(E29.shape)
ok=(cg>=0)&(cg<glo.shape[1])&(rg>=0)&(rg<glo.shape[0])
gl=np.full(E29.shape,np.nan); gl[ok]=glo[rg[ok],cg[ok]]

h=np.load(os.path.join(VG,"chm_altura.npy"))
print("chm_altura.npy: %s  finitos %.1f %%  mediana no pomar %.2f m"%(h.shape,100*np.isfinite(h).mean(),np.nanmedian(h[pomar])))
assert h.shape==gl.shape, (h.shape, gl.shape)
print("\n%-12s %8s %8s %8s %8s" % ("unidade","LiDAR","GLO-30","GLO-LiD","CHM"))
V={}
for nome,m in (("OCIDENTAL",do),("ORIENTAL",de),("referencia",saud),("resto",resto)):
    a=np.nanmedian(g["cota"][m]); b=np.nanmedian(gl[m]); c=np.nanmedian(h[m])
    V[nome]=(a,b,b-a,c)
    print("%-12s %8.3f %8.3f %8.3f %8.3f"%(nome,a,b,b-a,c))
print("\nORIENTAL menos OCIDENTAL:")
print("  no LiDAR (chao)          : %+.3f m" % (V["ORIENTAL"][0]-V["OCIDENTAL"][0]))
print("  no GLO-30 (superficie)   : %+.3f m" % (V["ORIENTAL"][1]-V["OCIDENTAL"][1]))
print("  no CHM (altura do copado): %+.3f m" % (V["ORIENTAL"][3]-V["OCIDENTAL"][3]))
print("  GLO-30 menos LiDAR       : %+.3f m de diferenca entre as duas unidades"
      % ((V["ORIENTAL"][2])-(V["OCIDENTAL"][2])))
print("\nSe o copado FOSSE a explicacao, o CHM teria de subir do OCIDENTAL para o")
print("ORIENTAL na ordem dos +0,3 m. Observado: %+.3f m." % (V["ORIENTAL"][3]-V["OCIDENTAL"][3]))
m=pomar&np.isfinite(gl)&np.isfinite(g["cota"])&np.isfinite(h)
r1,_=stats.pearsonr((gl-g["cota"])[m],h[m])
print("correlacao (GLO30-LiDAR) x CHM nas %d celulas do pomar: r=%+.3f"%(m.sum(),r1))
