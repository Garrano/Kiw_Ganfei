# -*- coding: utf-8 -*-
"""Q3 - a dispersao INTRA-unidade da cota, contra o contraste de 1,20 m."""
import os, sys, json
import numpy as np
sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1")
from c1_00_comum import *
from scipy import stats

g = dict(np.load(os.path.join(SAIDA, "c1_03_grelha.npz")))
masc, _ = carrega_mascaras()
pomar, saud, zona0, nu2021 = masc["pomar"], masc["saudavel"], masc["zona0"], masc["nu2021"]
do, de = discos_dos_focos(pomar)
resto = pomar & ~do & ~de
cot = g["cota"]

print("=== Q3a - dispersao da cota DENTRO de cada unidade (celulas de 10 m) ===")
print("%-26s %5s %8s %8s %8s %8s %8s %8s" % ("unidade","n","mediana","media","dp","p5","p95","amplitude"))
U = [("foco OESTE (disco)", do), ("foco ESTE (disco)", de),
     ("referencia sistematica", saud), ("resto do pomar", resto), ("pomar inteiro", pomar)]
S = {}
for nome, m in U:
    v = cot[m]; v = v[~np.isnan(v)]
    S[nome] = v
    print("%-26s %5d %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"
          % (nome, len(v), np.median(v), v.mean(), v.std(ddof=1),
             np.percentile(v,5), np.percentile(v,95), v.max()-v.min()))

o, e = S["foco OESTE (disco)"], S["foco ESTE (disco)"]
d = np.median(e) - np.median(o)
sp = np.sqrt(((len(o)-1)*o.var(ddof=1) + (len(e)-1)*e.var(ddof=1)) / (len(o)+len(e)-2))
print("\ncontraste ESTE-OESTE (medianas)      : %+.3f m" % d)
print("dp intra-unidade combinado (pooled)  :  %.3f m" % sp)
print("d de Cohen                           :  %.2f" % (d/sp))
print("sobreposicao das distribuicoes       :  %.1f%% das celulas OESTE acima da mediana ESTE"
      % (100*(o > np.median(e)).mean()))
print("                                        %.1f%% das celulas ESTE abaixo da mediana OESTE"
      % (100*(e < np.median(o)).mean()))
# AUC / prob. de superioridade
auc = (e[:,None] > o[None,:]).mean()
print("prob. de uma celula ESTE ser mais alta que uma OESTE (AUC): %.3f" % auc)
u,p = stats.mannwhitneyu(e,o,alternative="two-sided")
print("Mann-Whitney p = %.2e" % p)

print("\n=== Q3b - n EFECTIVO: as celulas de 10 m sao independentes? ===")
E29,N29 = centros_celulas()
for nome, m in (("foco OESTE", do), ("foco ESTE", de)):
    v = cot[m]; ok=~np.isnan(v)
    print("  %s: %d celulas de 10 m num disco de raio 90 m = %.2f ha."
          % (nome, ok.sum(), ok.sum()/100))
print("  O terreno tem autocorrelacao a centenas de metros: o n EFECTIVO de")
print("  unidades independentes e ~1 por disco, nao 248/255.")

print("\n=== Q3c - dp da cota a 50 cm dentro de cada disco (do .npy) ===")
DEMJ = json.load(open(os.path.join(SAIDA,"c1_03_dem50.json"), encoding="utf-8"))
t=DEMJ["transform"]; ny,nx=DEMJ["shape"]; L,T0,px = t[2],t[5],t[0]
dem = np.load(os.path.join(SAIDA,"c1_03_dem50.npy"), mmap_mode="r")
def disco_50(centro_utm, raio=90.0):
    X,Y = T_29_TO_3763.transform(*centro_utm)
    c0=int((X-raio-L)/px); c1=int((X+raio-L)/px)
    r0=int((T0-(Y+raio))/px); r1=int((T0-(Y-raio))/px)
    sub = np.array(dem[r0:r1, c0:c1], dtype="float64")
    yy,xx = np.mgrid[r0:r1, c0:c1]
    XX = L + (xx+0.5)*px; YY = T0 - (yy+0.5)*px
    m = ((XX-X)**2 + (YY-Y)**2) <= raio**2
    v = sub[m]; return v[np.isfinite(v)]
vo = disco_50(FOCO_OESTE); ve = disco_50(FOCO_ESTE)
for nome,v in (("OESTE",vo),("ESTE",ve)):
    print("  disco %s a 50 cm: n=%d  mediana %.3f  dp %.3f  p5 %.3f  p95 %.3f  amplitude %.3f"
          % (nome, len(v), np.median(v), v.std(ddof=1), np.percentile(v,5), np.percentile(v,95), v.max()-v.min()))
print("  NOTA: estes discos NAO estao intersectados com o pomar (incluem tudo).")
