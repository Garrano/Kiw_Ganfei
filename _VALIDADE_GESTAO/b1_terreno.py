# -*- coding: utf-8 -*-
"""O terreno do B1 — os dados estavam em disco e ninguém os usou.

O QUE MOTIVOU ISTO
------------------
A **P10** afirma, sobre o sector B1: *«SEM cota, SEM dreno, SEM declive»*. A
razão dada é que o MDT de 50 cm da Camada 1 pára **445 m a norte** dele.

Isso é verdade **do mosaico recortado** — o `c1_03_dem50.json` declara
`folga_m: 300,0`, ou seja foi cortado à AOI mais 300 m. Não é verdade **dos
dados**. Duas folhas locais cobrem o B1 por inteiro desde 29-08-2026:

    MDT-50cm-157564-07-2025   E 528761..529771  N 4653761..4654771
    MDT-50cm-158564-07-2025   E 529761..530770  N 4653771..4654781
    B1 (IFAP)                 E 529495..530063  N 4653832..4654477

**O recorte não é a fronteira do conhecimento; é uma escolha de quem recortou.**
É a quarta vez neste caso que uma janela decide em silêncio o que pode ser
sabido, e a primeira em que a resposta é «os dados estão aí, usa-os».

A PRÉ-VOO
---------
**1 · pergunta.** Onde fica o B1 na estrutura, em relação aos dois focos?
**2 · hipótese e falsificação.**
    H · o B1 não acrescenta nada à leitura do C9.
    FALSIFICA-SE se a cota do B1 cair **fora** do intervalo [6,64 ; 7,84] dos
    dois focos — porque então há uma terceira posição na estrutura, e a
    afirmação «as duas manchas estão nos extremos» deixa de ser verdadeira.
**3 · fronteira.** Polígonos do IFAP. Não sai de sinal nenhum nosso.
**5 · instrumento independente.** **Não há**, e diz-se: é o mesmo MDT, o mesmo
voo, a mesma resolução. Isso é uma força para a comparabilidade e uma
fraqueza para a verificação — as duas coisas ao mesmo tempo.
**7 · a média esconde?** Reporta-se média, mediana, desvio e intervalo.
**8 · n.** Células de 50 cm dentro dos polígonos, impresso.

A COSTURA, que é o risco real
------------------------------
A C1 mediu um degrau de **0,058 m** na costura entre campanhas de voo dentro da
AOI. As folhas do B1 são de outra parte do mosaico. **Se a costura entre elas e
as do pomar for maior do que o contraste que se quer ler, não se lê.** Mede-se,
não se assume.
"""
import glob
import json
import os

import numpy as np
import rasterio
from rasterio.windows import from_bounds
from matplotlib.path import Path as MP
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

LID = r"C:\Users\Jackster2\Downloads\ganfei_s2\lidar"
VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
CUL_B1 = {6476415, 8845729, 6476420, 8845739, 8845740, 6476425}

# ── as cotas certificadas dos focos, para comparar. Nao recalculadas.
TER = json.load(open(os.path.join(VC, "SAIDA_C1", "c1_04_terreno_por_unidade.json"),
                     encoding="utf-8"))
FOCOS = {"foco ORIENTAL": TER["foco ESTE (disco 90 m)"]["cota"],
         "resto do pomar": TER["resto do pomar"]["cota"],
         "referencia": TER["referencia sistematica"]["cota"],
         "foco OCIDENTAL": TER["foco OESTE (disco 90 m)"]["cota"]}
lo, hi = min(FOCOS.values()), max(FOCOS.values())
print("cotas certificadas da C1 (nao recalculadas):")
for k, v in sorted(FOCOS.items(), key=lambda kv: -kv[1]):
    print("   %-16s %.3f m" % (k, v))
print("   intervalo dos focos: %.3f .. %.3f m" % (lo, hi))

# ── os poligonos do B1, em EPSG:3763 (o CRS das folhas)
tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
GEO = {}
for f in KF:
    c = int(f["properties"]["CUL_ID"])
    if c in CUL_B1:
        GEO[c] = sht(lambda x, y, z=None: tr.transform(x, y),
                     shape(f["geometry"])).buffer(0)
xs = [v for g in GEO.values() for v in (g.bounds[0], g.bounds[2])]
ys = [v for g in GEO.values() for v in (g.bounds[1], g.bounds[3])]
BB = (min(xs) - 20, min(ys) - 20, max(xs) + 20, max(ys) + 20)
print()
print("B1 em EPSG:3763: E %.0f..%.0f  N %.0f..%.0f" % (BB[0], BB[2], BB[1], BB[3]))

# ── ler as folhas que tocam
folhas = []
for p in sorted(glob.glob(os.path.join(LID, "MDT-50cm-*.tif"))):
    with rasterio.open(p) as ds:
        b = ds.bounds
        if not (b.right < BB[0] or b.left > BB[2]
                or b.top < BB[1] or b.bottom > BB[3]):
            folhas.append(p)
print("folhas MDT que cobrem o B1: %d" % len(folhas))
for p in folhas:
    print("   %s" % os.path.basename(p))
if not folhas:
    raise SystemExit("nenhuma folha cobre o B1")

# ── mosaico local a 50 cm
P = 0.5
NC = int((BB[2] - BB[0]) / P)
NL = int((BB[3] - BB[1]) / P)
Z = np.full((NL, NC), np.nan, "float32")
proc = {}
for p in folhas:
    with rasterio.open(p) as ds:
        w = from_bounds(*BB, transform=ds.transform)
        a = ds.read(1, window=w, boundless=True, fill_value=np.nan).astype("float32")
        if ds.nodata is not None:
            a = np.where(a == ds.nodata, np.nan, a)
        a = a[:NL, :NC]
        m = np.isfinite(a) & ~np.isfinite(Z[:a.shape[0], :a.shape[1]])
        Z[:a.shape[0], :a.shape[1]][m] = a[m]
        proc[os.path.basename(p)] = a
print("mosaico: %d x %d celulas · %.1f %% com valor"
      % (NL, NC, 100 * np.isfinite(Z).mean()))

# ── a COSTURA entre as duas folhas, medida
if len(proc) == 2:
    (n1, a1), (n2, a2) = list(proc.items())
    k = np.isfinite(a1) & np.isfinite(a2)
    if k.sum() > 100:
        d = a1[k] - a2[k]
        print()
        print("COSTURA entre as duas folhas: n=%d celulas sobrepostas" % k.sum())
        print("   mediana %+.4f m · p90 |dif| %.4f m" % (np.median(d),
                                                         np.percentile(np.abs(d), 90)))
    else:
        print()
        print("COSTURA: as folhas nao se sobrepoem (%d celulas) — nao ha degrau"
              % k.sum())
        print("   a juncao e por adjacencia, e o risco de degrau fica NAO MEDIDO")

# ── mascaras e cota por parcela
E, N = np.meshgrid(BB[0] + (np.arange(NC) + .5) * P, BB[3] - (np.arange(NL) + .5) * P)
pts = np.column_stack([E.ravel(), N.ravel()])
print()
print("=" * 88)
print("A COTA DO B1, parcela a parcela")
print("=" * 88)
print()
print("%-10s %8s %9s %9s %8s %8s" % ("CUL_ID", "n50cm", "media", "mediana",
                                     "desvio", "p10-p90"))
tudo = []
for c, g in sorted(GEO.items()):
    m = MP(np.array(list(g.exterior.coords))).contains_points(pts).reshape(NL, NC)
    v = Z[m]
    v = v[np.isfinite(v)]
    if v.size < 50:
        print("%-10d %8d  celulas a menos" % (c, v.size))
        continue
    tudo.append(v)
    print("%-10d %8d %9.3f %9.3f %8.3f %8.3f"
          % (c, v.size, v.mean(), np.median(v), v.std(),
             np.percentile(v, 90) - np.percentile(v, 10)))
V = np.concatenate(tudo)
cota_b1 = float(np.mean(V))
print()
print("%-10s %8d %9.3f %9.3f %8.3f %8.3f"
      % ("B1 todo", V.size, V.mean(), np.median(V), V.std(),
         np.percentile(V, 90) - np.percentile(V, 10)))

# ── o criterio
print()
print("=" * 88)
print("H · o B1 nao acrescenta nada. Falsifica-se se a cota cair FORA de [%.2f ; %.2f]"
      % (lo, hi))
print("=" * 88)
print()
fora = cota_b1 < lo or cota_b1 > hi
print("   cota media do B1: %.3f m" % cota_b1)
if fora:
    onde = "ABAIXO" if cota_b1 < lo else "ACIMA"
    print("   -> %s do intervalo dos focos por %.3f m."
          % (onde, (lo - cota_b1) if cota_b1 < lo else (cota_b1 - hi)))
    print("   -> H FALSIFICADA. Ha uma TERCEIRA posicao na estrutura, e a frase")
    print("      «as duas manchas estao nos extremos» deixa de ser verdadeira.")
    ver = "o B1 fica %s do intervalo dos focos" % onde
else:
    print("   -> dentro do intervalo. H nao falsificada: o B1 nao acrescenta")
    print("      uma posicao nova, e o C9 mantem-se como esta.")
    ver = "o B1 fica dentro do intervalo dos focos"
print()
print("   RESSALVA, e vai a frente: e o MESMO instrumento e o MESMO voo. Nao ha")
print("   confirmacao independente desta cota, e diz-se em vez de se diluir.")

json.dump(dict(folhas=[os.path.basename(p) for p in folhas],
               cotas_focos=FOCOS, intervalo=[lo, hi],
               b1_media=cota_b1, b1_mediana=float(np.median(V)),
               b1_desvio=float(V.std()), n=int(V.size),
               por_parcela={str(c): float(np.mean(Z[MP(np.array(list(g.exterior.coords)))
                                                    .contains_points(pts).reshape(NL, NC)][
                   np.isfinite(Z[MP(np.array(list(g.exterior.coords)))
                                 .contains_points(pts).reshape(NL, NC)])]))
                            for c, g in GEO.items()},
               fora_do_intervalo=bool(fora), veredicto=ver),
          open(os.path.join(VG, "b1_terreno.json"), "w"), indent=1)
print()
print("escrito b1_terreno.json")
