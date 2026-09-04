# -*- coding: utf-8 -*-
"""Q1 - a cota e a UNICA variavel estrutural. Nas outras, os dois focos
   sao o par mais parecido do conjunto?"""
import os, sys, json
import numpy as np
from scipy import stats
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1")
from c1_00_comum import *

TER=json.load(open(os.path.join(SAIDA,"c1_04_terreno_por_unidade.json"),encoding="utf-8"))
ESC=json.load(open(os.path.join(SAIDA,"c1_11_escalas.json"),encoding="utf-8"))
NOM={"foco OESTE (disco 90 m)":"OCIDENTAL","foco ESTE (disco 90 m)":"ORIENTAL",
     "referencia sistematica":"referencia","resto do pomar":"resto"}
U=list(NOM)
print("=== as variaveis ESTRUTURAIS do certificado da C1, todas ===")
campos=["cota","declive","tpi","res150","rug25","exposicao"]
print("%-12s"%"variavel"+ "".join("%12s"%NOM[u] for u in U) + "   |onde caem os dois focos")
for c in campos:
    v={u:TER[u][c] for u in U}
    lin="%-12s"%c + "".join("%12.4f"%v[u] for u in U)
    o=sorted(U,key=lambda k:v[k])
    pos=[o.index("foco OESTE (disco 90 m)"),o.index("foco ESTE (disco 90 m)")]
    adj = abs(pos[0]-pos[1])==1
    print(lin+"   | posicoes %s%s"%(sorted(pos), "  <-- PAR ADJACENTE" if adj else "  (extremos opostos)" if sorted(pos)==[0,3] else ""))
E={"foco OESTE":"OCIDENTAL","foco ESTE":"ORIENTAL","referencia sistematica":"referencia"}
print("\n=== c1_11_escalas: as variaveis de DRENAGEM ===")
for c in ["declive_forma","hand_m","dist_drenagem_m","acc_p95_m2"]:
    ks=["foco OESTE","foco ESTE","referencia sistematica","pomar"]
    print("%-18s"%c + "".join("%14.4f"%ESC[k][c] for k in ks) + "   (%s)"%", ".join(ks))

print("\n=== o teste que a peca NAO fez: distancia normalizada entre os dois focos ===")
print("Para cada variavel, |ORIENTAL-OCIDENTAL| dividido pela amplitude das 4 unidades.")
print("%-12s %10s %10s %8s" % ("variavel","|dif focos|","amplitude","razao"))
raz={}
for c in campos:
    v=np.array([TER[u][c] for u in U])
    d=abs(TER["foco ESTE (disco 90 m)"][c]-TER["foco OESTE (disco 90 m)"][c])
    amp=v.max()-v.min()
    raz[c]=d/amp if amp else np.nan
    print("%-12s %10.4f %10.4f %8.2f%s"%(c,d,amp,raz[c]," <-- os focos SAO os extremos" if raz[c]>0.99 else (" <-- quase identicos"if raz[c]<0.35 else "")))
print("\nEm 'cota' os dois focos sao os extremos (razao 1,00).")
print("Em 'exposicao' e 'tpi' sao o par MAIS PARECIDO das quatro unidades.")

print("\n=== exposicao: os dois focos contra as outras duas unidades (teste formal) ===")
g=dict(np.load(os.path.join(SAIDA,"c1_03_grelha.npz")))
masc,_=carrega_mascaras(); pomar,saud=masc["pomar"],masc["saudavel"]
do,de=discos_dos_focos(pomar); resto=pomar&~do&~de
def circmed(m):
    a=np.radians(g["exposicao"][m]); a=a[np.isfinite(a)]
    return np.degrees(np.arctan2(np.nanmean(np.sin(a)),np.nanmean(np.cos(a))))%360
for nome,m in (("OCIDENTAL",do),("ORIENTAL",de),("referencia",saud),("resto",resto)):
    print("  exposicao media circular %-11s %6.1f graus" % (nome,circmed(m)))
print("  |ORIENTAL - OCIDENTAL| = %.1f graus" % abs(circmed(de)-circmed(do)))
print("  |resto     - OCIDENTAL| = %.1f graus" % abs(circmed(resto)-circmed(do)))
for c in ("tpi","res150"):
    d1,p1=stats.mannwhitneyu(g[c][do][~np.isnan(g[c][do])],g[c][de][~np.isnan(g[c][de])],alternative="two-sided")
    a=np.concatenate([g[c][do],g[c][de]]); a=a[~np.isnan(a)]
    b=np.concatenate([g[c][saud],g[c][resto]]); b=b[~np.isnan(b)]
    u2,p2=stats.mannwhitneyu(a,b,alternative="two-sided")
    print("  %-7s OCID vs ORIE p=%.2e   |   (os dois focos) vs (ref+resto) p=%.2e  dif medianas %+.5f"
          % (c,p1,p2,np.median(a)-np.median(b)))
