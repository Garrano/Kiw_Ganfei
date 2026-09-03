# -*- coding: utf-8 -*-
"""O parcelario IFAP contra o que medimos.

O que isto e, e porque nao e mais uma medicao
---------------------------------------------
O parcelario do IFAP nao e sensoriamento remoto: e o que o beneficiario
**declarou** e a administracao aceitou, parcela a parcela, com codigo de
cultura. E um documento, e por isso entra no dossie como **facto de tipo 1 —
testemunho** — nao como medicao nossa. O modo de falha nao e ruido de sensor;
e desfasamento entre o declarado e o instalado.

Fonte: WFS do AgroDigital da CCDR-N (camadas `culturas.2025jun10` e
`parcelas.2025jun10`), campanha de **2025**, retrato de **10 de Junho de 2025**.
Endereco dado pelo utilizador.

As perguntas
------------
1. Quanto do nosso poligono de 30,31 ha esta declarado como KIWI (codigo 124)?
2. As 3,77 ha que o LiDAR encontrou **sem pergola** em 06-07-2025 estao
   declaradas como kiwi, ou como outra coisa?
3. O que esta declarado no N3, o nucleo que o analista B diz ter sido cortado
   em Julho de 2024?

A terceira e a que mais importa. O retrato do parcelario e de 10-06-2025, ou
seja **onze meses depois** do corte que o satelite data. Se o N3 continuar
declarado como kiwi, o declarado e o instalado divergem. Se estiver declarado
como outra coisa, o parcelario confirma o corte por via administrativa — um
instrumento que nao e optico, nem radar, nem LiDAR.
"""
import json
import os
import sys
from collections import defaultdict

import numpy as np
import requests
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.transform import from_origin

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import *  # noqa

AQUI = os.path.dirname(os.path.abspath(__file__))
B = ("https://agrodigital.ccdr-n.pt/MapasLeft_Net_para_servidor/"
     "MapasLeft_Net_para_servidor/MapasLeft_Net/MapaComCAOP/IfapWfsProxy.ashx")

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(AQUI, "chm_altura.npy"))
COM, SEM = np.isfinite(h) & (h >= 0.5), np.isfinite(h) & (h < 0.5)
do, de = discos_dos_focos(POMAR)


def disco(x, y, r=70.0):
    yy, xx = np.mgrid[:NL, :NC]
    return np.hypot(AOI[0] + (xx + .5) * PASSO - x,
                    AOI[3] - (yy + .5) * PASSO - y) <= r


N1 = disco(530476, 4655046) & POMAR
N3 = disco(531068, 4655145) & POMAR

t = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)
ti = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)
lo, la = t.transform(AOI[0] - 400, AOI[1] - 400)
lo2, la2 = t.transform(AOI[2] + 400, AOI[3] + 400)
d = requests.get(B, params={"layer": "culturas.2025jun10", "max": 20000,
                            "bbox": "%.6f,%.6f,%.6f,%.6f" % (lo, la, lo2, la2)},
                 timeout=240).json()
feats = d["features"]
print("poligonos de cultura na campanha 2025: %d" % len(feats))

DEST = from_origin(AOI[0], AOI[3], PASSO, PASSO)


def para_utm(g):
    def conv(anel):
        return [list(ti.transform(x, y)) for x, y in anel]
    if g["type"] == "Polygon":
        return {"type": "Polygon", "coordinates": [conv(a) for a in g["coordinates"]]}
    return {"type": "MultiPolygon",
            "coordinates": [[conv(a) for a in p] for p in g["coordinates"]]}


# um raster de codigo de cultura na nossa grelha
codigos, nomes = {}, {}
formas = []
for i, f in enumerate(feats, start=1):
    p = f["properties"]
    cod = p.get("PUN_CUL_COD")
    if not cod:
        continue
    c = int(cod)
    codigos[i] = c
    nomes[c] = p.get("PUN_CUL_DESC")
    formas.append((para_utm(f["geometry"]), i))
idx = rasterize(formas, out_shape=(NL, NC), transform=DEST, fill=0,
                all_touched=False, dtype="int32")
CUL = np.zeros((NL, NC), "int32")
for i, c in codigos.items():
    CUL[idx == i] = c
print("celulas com cultura declarada: %d (%.2f ha)"
      % ((CUL > 0).sum(), (CUL > 0).sum() / 100.0))

KIWI = CUL == 124
res = {}
print("\n%-26s %7s %10s %12s" % ("", "ha", "% KIWI", "% sem decl."))
for nome, m in [("poligono do pomar", POMAR),
                ("referencia sistematica", REF),
                ("com pergola (LiDAR)", POMAR & COM),
                ("SEM pergola (LiDAR)", POMAR & SEM),
                ("N1 foco OESTE", N1),
                ("N3 leste (cortado 2024?)", N3),
                ("foco ESTE, disco todo", de & POMAR)]:
    if m.sum() == 0:
        continue
    pk = 100.0 * (m & KIWI).sum() / m.sum()
    ps = 100.0 * (m & (CUL == 0)).sum() / m.sum()
    res[nome] = dict(ha=m.sum() / 100.0, pct_kiwi=pk, pct_sem_declaracao=ps)
    print("%-26s %7.2f %9.1f %% %10.1f %%" % (nome, m.sum() / 100.0, pk, ps))

print("\nCULTURAS DECLARADAS DENTRO DO NOSSO POLIGONO")
cont = defaultdict(int)
for c in np.unique(CUL[POMAR]):
    cont[int(c)] = int((CUL[POMAR] == c).sum())
for c, n in sorted(cont.items(), key=lambda kv: -kv[1]):
    print("   %-5s %-42s %6.2f ha" % (c or "—", nomes.get(c, "(sem declaracao)"),
                                      n / 100.0))

print("\nCULTURAS NAS 3,77 ha SEM PERGOLA")
sub = CUL[POMAR & SEM]
for c in sorted(set(sub.tolist()), key=lambda z: -(sub == z).sum()):
    print("   %-5s %-42s %6.2f ha" % (c or "—", nomes.get(c, "(sem declaracao)"),
                                      (sub == c).sum() / 100.0))

print("\nCULTURAS NO N3")
sub = CUL[N3]
for c in sorted(set(sub.tolist()), key=lambda z: -(sub == z).sum()):
    print("   %-5s %-42s %6.2f ha" % (c or "—", nomes.get(c, "(sem declaracao)"),
                                      (sub == c).sum() / 100.0))

np.save(os.path.join(AQUI, "ifap_cultura.npy"), CUL)
json.dump(dict(unidades=res, nomes={str(k): v for k, v in nomes.items()}),
          open(os.path.join(AQUI, "ifap_cruzamento.json"), "w"), indent=1)
