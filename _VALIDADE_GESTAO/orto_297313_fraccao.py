# -*- coding: utf-8 -*-
"""A fracção sem coberto, bloco a bloco — o que a média dos cinco escondeu.

PORQUE ESTE FICHEIRO EXISTE
---------------------------
`orto_297313.py` comparou os cinco blocos com os doze do mesmo dono usando
p25/mediana/p75 sobre 300 mil píxeis, e concluiu «nunca separam, em nenhuma
época». **Estava errado por agregação.** A imagem de 2025 ao perto mostra a
metade norte dos cinco desmatada e a metade sul com coberto — e uma mediana
sobre os dois pedaços não vê nem um nem outro.

É o mesmo modo de falha que este projecto já registou duas vezes: uma estatística
de resumo aplicada a uma unidade que não é homogénea. A resposta não é olhar
melhor: é **medir a fracção**, que é a grandeza que distingue «tudo pior» de
«uma parte desapareceu».

A MEDIDA, e porque é imune ao esticamento do WMS
-------------------------------------------------
O WMS devolve uma imagem **renderizada** — 8 bits, JPEG, com esticamento de
contraste desconhecido e diferente entre épocas. **O valor não é NDVI** e não se
compara entre imagens.

Por isso a medida é um **quantil dentro da mesma imagem**: para cada época,
    limiar = percentil 10 do índice nos DOZE blocos de controlo do mesmo dono
    fracção = % de píxeis de cada bloco abaixo desse limiar
Um esticamento global monótono move o limiar e os píxeis juntos e **cancela-se**.
O que não cancela é a mudança relativa entre unidades da mesma imagem.

CRITÉRIO, fixado antes de correr
--------------------------------
    F1 · Se a fracção sem coberto dos cinco saltar numa época e ficar, essa
         época data um **desmatamento**, e o degrau de 2025-26 do satélite deixa
         de ser sintoma de declínio nessa parte.
    F2 · O salto tem de ser **específico**: se os doze subirem igual, é a imagem
         que mudou, não o terreno. Por isso os doze vão na mesma tabela.
    F3 · Bloco a bloco, nunca só a média dos cinco. Foi a média que falhou.
"""
import json
import os

import numpy as np
from PIL import Image
from matplotlib.path import Path as MP
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

Image.MAX_IMAGE_PIXELS = None
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
C = os.path.join(VG, "_orto297313")

OS_CINCO = [6705427, 6705429, 6705428, 6705432, 6705442]
CAM = {"2007": "Ortos2007-FalsaCor", "2010": "Ortos2010-FalsaCor",
       "2012": "Ortos2012-FalsaCor", "2018": "Ortos2018-IRG",
       "2021": "Ortos2021-IRG", "2025": "Ortos2025-IRG"}
ANOS = ["2007", "2010", "2012", "2018", "2021", "2025"]

tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
P = json.load(open(os.path.join(H2, "ifap_parcelas_largo.json"), encoding="utf-8"))
PF = P["features"] if isinstance(P, dict) else P
parc = [(para(shape(f["geometry"])).buffer(0), f["properties"].get("ENT_ID"))
        for f in PF]

BL = []
for ft in KF:
    g = para(shape(ft["geometry"])).buffer(0)
    if g.is_empty or g.area / 1e4 < 0.5:
        continue
    c = g.centroid
    ent = next((e for pg, e in parc if pg.contains(c)), None)
    if ent == 297313:
        BL.append(dict(cul=int(ft["properties"]["CUL_ID"]), geom=g,
                       ha=g.area / 1e4, cinco=int(ft["properties"]["CUL_ID"]) in OS_CINCO))

xs = [v for b in BL for v in (b["geom"].bounds[0], b["geom"].bounds[2])]
ys = [v for b in BL for v in (b["geom"].bounds[1], b["geom"].bounds[3])]
BB = (min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40)
PX = 0.5
NCx, NLy = int((BB[2] - BB[0]) / PX), int((BB[3] - BB[1]) / PX)
EE, NN = np.meshgrid(BB[0] + (np.arange(NCx) + .5) * PX,
                     BB[3] - (np.arange(NLy) + .5) * PX)
pts = np.column_stack([EE.ravel(), NN.ravel()])
for b in BL:
    b["m"] = MP(np.array(list(b["geom"].exterior.coords))
                ).contains_points(pts).reshape(NLy, NCx)
    b["n"] = int(b["m"].sum())
CTRL = np.any([b["m"] for b in BL if not b["cinco"]], axis=0)
print("blocos do ENT 297313: %d  (cinco do degrau: %d · controlo: %d)"
      % (len(BL), sum(b["cinco"] for b in BL), sum(not b["cinco"] for b in BL)))

FR = {}
for a in ANOS:
    irg = np.array(Image.open(os.path.join(C, "%s_%s.png" % (a, CAM[a]))
                              ).convert("RGB")).astype("float32")
    ir, rd = irg[..., 0], irg[..., 1]
    v = np.where(ir + rd > 8, (ir - rd) / np.maximum(ir + rd, 1e-6), np.nan)
    lim = float(np.nanpercentile(v[CTRL], 10))
    FR[a] = dict(lim=lim, blocos={})
    for b in BL:
        x = v[b["m"]]
        x = x[np.isfinite(x)]
        FR[a]["blocos"][b["cul"]] = float(100.0 * np.mean(x < lim))

print()
print("=" * 88)
print("FRACCAO DE PIXEIS ABAIXO DO PERCENTIL 10 DOS DOZE, dentro de cada imagem (%)")
print("=" * 88)
print()
print("%-10s %6s %5s %s" % ("CUL_ID", "ha", "", "  ".join("%7s" % a for a in ANOS)))
for b in sorted(BL, key=lambda z: (not z["cinco"], z["cul"])):
    marca = "CINCO" if b["cinco"] else "  -  "
    print("%-10d %6.2f %5s %s"
          % (b["cul"], b["ha"], marca,
             "  ".join("%6.1f%%" % FR[a]["blocos"][b["cul"]] for a in ANOS)))

c5 = np.array([[FR[a]["blocos"][b["cul"]] for a in ANOS]
               for b in BL if b["cinco"]])
c12 = np.array([[FR[a]["blocos"][b["cul"]] for a in ANOS]
                for b in BL if not b["cinco"]])
print()
print("%-23s %s" % ("mediana dos CINCO",
                    "  ".join("%6.1f%%" % v for v in np.median(c5, 0))))
print("%-23s %s" % ("mediana dos DOZE (F2)",
                    "  ".join("%6.1f%%" % v for v in np.median(c12, 0))))
print()
print("F2 · o salto e especifico dos cinco?  ", end="")
sub5 = np.median(c5, 0)[-1] - np.median(c5, 0)[-2]
sub12 = np.median(c12, 0)[-1] - np.median(c12, 0)[-2]
print("cinco +%.1f pp de 2021 para 2025, doze %+.1f pp  ->  %s"
      % (sub5, sub12, "SIM" if sub5 > 3 * max(sub12, 1) else "nao"))

json.dump(FR, open(os.path.join(VG, "orto_297313_fraccao.json"), "w"), indent=1)
print()
print("escrito orto_297313_fraccao.json")
