# -*- coding: utf-8 -*-
"""Colocar as valvulas pelos NUMEROS DE LINHA, nao pelo ajuste do desenho.

A ideia nao e minha: veio da pergunta "nao consegues extrapolar das notas a
mao?". As anotacoes do esquema nao dizem so que valvula e qual — dizem em que
LINHA fica cada uma. E as linhas sao as fileiras da pergola, que se contam na
ortofoto a 25 cm.

Leitura correcta das anotacoes
------------------------------
"valvula 6 e 7 / linhas 130 e 131" NAO significa a valvula 6 na linha 130 e a 7
na linha 131 — isso poria duas valvulas a 5 m uma da outra, e no desenho estao a
quase 100 m. Significa o PAR de valvulas (uma a norte e outra a sul da conduta,
como o esquema mostra em duas filas) assente entre as linhas 130 e 131.

Ancoras lidas no esquema:
    valvulas 6 e 7          linhas 130-131   -> linha 130,5
    valvulas 8 e 9          linhas 267-268   -> linha 267,5
    valvulas 10,11,12,13    linhas 306-307   -> linha 306,5
    valvulas 14 e 15        linhas 336-337   -> linha 336,5
    valvula 16              linha 409
    valvula 17              linha 423
    (valvulas 4 e 5         linhas 137 e 156 — numeracao do lobo oeste, que
     nao e continua com esta; ver nota no fim)

Porque e melhor que o ajuste da forma
-------------------------------------
O ajuste da forma do desenho a parcela dava residuo mediano de 64 m, maior que
os 49 m entre valvulas: nenhum ponto podia ser atribuido. As linhas sao
objectos FISICOS medidos na ortofoto, com compasso conhecido. A precisao passa
a ser a de contar fileiras.
"""
import json
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from scipy import ndimage, signal

AOI = (529950, 4654600, 531950, 4655600)
ORTO = "orto/ortos2021_cog_25cm_rgbi_jpg_002-3_v01.tif"

g = json.load(open("sentinel/masks_geograficas.json"))
POMAR = np.array([[c == "1" for c in L] for L in g["pomar_bits"]], bool)

# --- 1. eixo real da parcela ----------------------------------------------
ys, xs = np.where(POMAR)
E = AOI[0] + (xs + .5) * 10.0
N = AOI[3] - (ys + .5) * 10.0
P = np.column_stack([E - E.mean(), N - N.mean()])
w_, v_ = np.linalg.eigh(np.cov(P.T))
eixo = v_[:, np.argmax(w_)]
if eixo[0] < 0:
    eixo = -eixo                       # aponta para leste
az = (90 - np.degrees(np.arctan2(eixo[1], eixo[0]))) % 180
t = P @ eixo
COMP = float(np.percentile(t, 99) - np.percentile(t, 1))
print("eixo da parcela: azimute %.1f graus | comprimento util %.0f m" % (az, COMP))

# --- 2. compasso das fileiras, medido na ortofoto -------------------------
ds = rasterio.open(ORTO)
Wo = transform_bounds("EPSG:32629", ds.crs, *AOI)
w = from_bounds(*Wo, transform=ds.transform)
lum = np.dstack([ds.read(i, window=w) for i in (1, 2, 3)]).mean(2).astype("float32")
# roda para as fileiras ficarem verticais: as fileiras sao PERPENDICULARES ao
# eixo, logo roda-se de -az para as por a prumo
rot = ndimage.rotate(lum, -(90 - az), reshape=True, order=1, cval=np.nan)
h, l = rot.shape
faixa = rot[h // 2 - 400:h // 2 + 400, l // 2 - 1200:l // 2 + 1200]
perfil = np.nanmean(faixa, axis=0)
perfil = perfil - ndimage.uniform_filter1d(perfil, 120)
perfil = perfil[np.isfinite(perfil)]
ac = signal.correlate(perfil, perfil, mode="full")[len(perfil) - 1:]
ac /= ac[0]
lo, hi = int(2.0 / 0.25), int(12.0 / 0.25)          # procurar entre 2 e 12 m
k = lo + int(np.argmax(ac[lo:hi]))
COMPASSO = k * 0.25
print("compasso das fileiras medido por autocorrelacao: %.2f m (pico r=%.2f)"
      % (COMPASSO, ac[k]))

# --- 3. o teste: as linhas 130,5 a 423 cobrem a parcela? ------------------
ANCORAS = [(130.5, "válvulas 6 e 7"), (267.5, "válvulas 8 e 9"),
           (306.5, "válvulas 10, 11, 12 e 13"), (336.5, "válvulas 14 e 15"),
           (409.0, "válvula 16"), (423.0, "válvula 17")]
vao = ANCORAS[-1][0] - ANCORAS[0][0]
print("\nTESTE DE COERENCIA")
print("  linhas %.1f a %.1f = %.1f intervalos" % (ANCORAS[0][0], ANCORAS[-1][0], vao))
print("  x compasso medido %.2f m = %.0f m" % (COMPASSO, vao * COMPASSO))
print("  comprimento util da parcela   = %.0f m" % COMP)
err = abs(vao * COMPASSO - COMP) / COMP
print("  discrepancia: %.1f%%   -> %s" % (100 * err,
      "COERENTE: as linhas anotadas cobrem a parcela de ponta a ponta"
      if err < 0.08 else "INCOERENTE, a hipotese cai"))

# --- 4. colocar as valvulas ------------------------------------------------
if err < 0.08:
    t0 = float(np.percentile(t, 1))
    escala = COMP / vao                       # metros por linha, ancorado
    C = np.array([E.mean(), N.mean()])
    print("\nPOSICOES (%.2f m por linha, ancorado nos dois extremos medidos)" % escala)
    saida = []
    for lin, nome in ANCORAS:
        d = t0 + (lin - ANCORAS[0][0]) * escala
        p = C + eixo * d
        saida.append(dict(linha=lin, valvulas=nome,
                          E=round(float(p[0]), 1), N=round(float(p[1]), 1)))
        print("   linha %5.1f  %-26s E %.0f  N %.0f" % (lin, nome, p[0], p[1]))
    json.dump(dict(
        _metodo="posicao por numero de linha anotado no esquema; compasso "
                "medido na ortofoto por autocorrelacao; ancorado nos dois "
                "extremos da parcela",
        azimute_eixo=round(az, 1), compasso_m=round(COMPASSO, 2),
        metros_por_linha=round(escala, 3), comprimento_parcela_m=round(COMP),
        discrepancia_pct=round(100 * err, 1),
        incerteza_m="~10 m (contagem de fileiras + extremos da parcela), "
                    "contra 64 m do ajuste da forma",
        valvulas=saida),
        open("valvulas_por_linha.json", "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("\nvalvulas_por_linha.json gravado")
print("""
NOTA sobre as valvulas 1-5. O esquema anota "137 e 156" para as valvulas 4 e 5,
numeros que caem dentro do intervalo 130-423 usado aqui. Se a numeracao fosse
continua, as valvulas 4 e 5 ficariam ENTRE as 6-7 e as 8-9, o que contradiz o
desenho, onde estao num lobo separado a oeste. Conclusao: o lobo oeste tem
numeracao de linhas propria, e estas ancoras NAO o alcancam. As valvulas 1-5
continuam por colocar.
""")
