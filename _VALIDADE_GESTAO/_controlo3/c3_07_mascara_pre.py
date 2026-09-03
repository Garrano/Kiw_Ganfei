# -*- coding: utf-8 -*-
"""O teste decisivo do filtro de copado: fazer a mesma mascara com um instrumento PRE.

`ZONA0 & COM` usa o CHM do voo LiDAR de 06-07-2025 — que a C2 da LISTA_FINAL
declara POS-TRATAMENTO. Sem esse filtro o foco ORIENTAL cai do 1.o para o 3.o
lugar (c3_06). Portanto o lugar dele depende de uma mascara derivada do estado
DEPOIS do acontecimento.

Existe o instrumento PRE para fazer o mesmo trabalho: `nu2021_bits`, chao lavrado
dentro do pomar na ortofoto DGT de 2021 a 25 cm, 1,67 ha — e o proprio ficheiro
de mascaras diz que 41,4 % da `zona0` e chao lavrado em 2021.

Se `ZONA0 & ~NU2021` (mascara de 2021) puser o foco no mesmo lugar que
`ZONA0 & COM` (mascara de 2025), o filtro nao esta a importar informacao do
acontecimento e a conclusao aguenta. Se puser noutro lugar, esta.

E o mesmo para o foco OCIDENTAL, por simetria.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import carregar, matriz

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
S2D = r"C:\Users\Jackster2\Downloads\ganfei_s2"
C = os.path.join(VG, "_reg01_landsat_cache")
EXCL = {"6705427", "6705428", "6705429", "6705432", "6705442",
        "8845729", "8845731", "8845739"}

D = carregar()
datas, unid, V, PIX = matriz(D)
idx = {u: i for i, u in enumerate(unid)}
DENTRO = [u for u in unid if u.isdigit() and u not in EXCL]
D_i = np.array([idx[u] for u in DENTRO])

g = json.load(open(os.path.join(S2D, "sentinel", "masks_geograficas.json")))
b10 = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, ZONA0, NU21 = b10("pomar_bits"), b10("zona0_bits"), b10("nu2021_bits")
E10, N10, COM, p30 = D["E10"], D["N10"], D["COM"], D["para30"]
DISCO = np.hypot(E10 - 530485., N10 - 4655053.) <= 90

print("mascaras a 10 m:  zona0 %d · nu2021 %d · zona0 e nu2021 %d (%.1f %% da zona0)"
      % (ZONA0.sum(), NU21.sum(), (ZONA0 & NU21).sum(),
         100 * (ZONA0 & NU21).sum() / ZONA0.sum()))
print("                  COM (CHM 2025) retira %d celulas da zona0 (%.1f %%)"
      % ((ZONA0 & ~COM).sum(), 100 * (ZONA0 & ~COM).sum() / ZONA0.sum()))
print("                  concordancia entre os dois filtros dentro da zona0: %.1f %%"
      % (100 * np.mean((COM == ~NU21)[ZONA0])))

val = [k for k, d in enumerate(datas)
       if np.isfinite(V[k, D_i]).sum() >= 0.7 * len(D_i)]
MED = {k: float(np.median(V[k, D_i][np.isfinite(V[k, D_i])])) for k in val}
cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"), encoding="utf-8"))
fich = {}
for x in os.listdir(C):
    fich.setdefault(x[:10], x)
NDVI = {k: np.load(os.path.join(C, fich[datas[k]]))["ndvi"] for k in val}
PRE = [k for k in val if datas[k] < "2025"]
POS = [k for k in val if datas[k] >= "2025"]

DEG_BL = {}
for c in DENTRO:
    a = [V[k, idx[c]] - MED[k] for k in POS if np.isfinite(V[k, idx[c]])]
    b = [V[k, idx[c]] - MED[k] for k in PRE if np.isfinite(V[k, idx[c]])]
    DEG_BL[c] = float(np.mean(a) - np.mean(b))
ORD = sorted(DEG_BL.values())


def deg(m30):
    out = []
    for ii in (POS, PRE):
        acc = [float(np.median(NDVI[k][m30][np.isfinite(NDVI[k][m30])])) - MED[k]
               for k in ii
               if np.isfinite(NDVI[k][m30]).sum() >= max(3, 0.5 * m30.sum())]
        out.append(np.mean(acc) if acc else np.nan)
    return out[0] - out[1]


VARIANTES = [
    ("ORIENTAL · zona0 & COM (CHM 07-2025)  [a que a cadeia usa]", ZONA0 & COM),
    ("ORIENTAL · zona0 & ~nu2021 (ortofoto 2021)", ZONA0 & ~NU21),
    ("ORIENTAL · zona0 & ~nu2021 & COM (os dois)", ZONA0 & ~NU21 & COM),
    ("ORIENTAL · zona0 crua", ZONA0),
    ("OCIDENTAL · disco & pomar & COM  [a que a cadeia usa]", DISCO & POMAR & COM),
    ("OCIDENTAL · disco & pomar & ~nu2021", DISCO & POMAR & ~NU21),
    ("OCIDENTAL · disco & pomar", DISCO & POMAR),
]
print()
print("=" * 100)
print("%-58s %5s %9s %6s" % ("variante da mascara", "n30", "degrau", "lugar"))
print("=" * 100)
res = {}
for nome, m10 in VARIANTES:
    m = p30(m10)
    if m.sum() < 5:
        print("%-58s %5d   n30 < 5, nao se julga" % (nome, m.sum()))
        continue
    d = deg(m)
    lug = 1 + sum(1 for x in ORD if x < d)
    res[nome] = dict(n30=int(m.sum()), degrau=float(d), lugar=int(lug))
    print("%-58s %5d %+9.4f %5d de %d %s"
          % (nome, m.sum(), d, lug, len(ORD) + 1,
             "" if lug <= 2 else "  <== FORA DO TOP-2"))

print()
print("Leitura: se o lugar do foco depende de qual dos dois filtros de chao se usa,")
print("entao o lugar nao e uma medida do acontecimento — e uma escolha de mascara.")

json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "c3_07_mascara_pre.json"), "w"), indent=1)
