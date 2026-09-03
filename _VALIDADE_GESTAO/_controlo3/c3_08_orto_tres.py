# -*- coding: utf-8 -*-
"""Q3 — os tres blocos do ENT 472062 excluidos SEM ortofoto. Verificam-se aqui.

A triagem excluiu oito blocos. Cinco (ENT 297313) tem ortofoto a confirmar
desmatamento em 2024. Os outros tres — 8845729, 8845731, 8845739, do PROPRIO
dono do pomar em estudo — sairam so pela forma da serie, e o `REG01_RETRACCAO_A3`
descreve-os como «caem e recuperam, com forma de replantacao». Isso e uma
inferencia sobre a serie, feita com o mesmo instrumento que produziu a serie.
E exactamente o modo de falha que retirou o A3.

METODO — o mesmo de `orto_297313_fraccao.py`, para ser comparavel:
    limiar = percentil 10 do indice IR-R nos blocos de CONTROLO do mesmo dono,
             medido DENTRO de cada imagem (imune ao esticamento do WMS);
    fraccao = % de pixeis de cada bloco abaixo desse limiar.

CRITERIO, escrito antes de correr:
    T1 · se a fraccao sem coberto de um dos tres SALTAR na epoca que a serie
         Landsat aponta (2023 para 8845731 e 8845739, 2024 para 8845729) e o
         controlo do mesmo dono NAO saltar, a exclusao esta justificada;
    T2 · se nao saltar em nenhuma epoca, a exclusao NAO esta justificada por
         mudanca de uso e o bloco tem de voltar a distribuicao;
    T3 · se a ortofoto disponivel nao bracketar a quebra, escreve-se NAO
         TESTAVEL e nao se decide.

CONTROLO: os 12 blocos do ENT 472062 que NAO foram excluidos.
"""
import json
import os
import sys

import numpy as np
import requests
from PIL import Image
from matplotlib.path import Path as MP
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as sht

Image.MAX_IMAGE_PIXELS = None
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
H2 = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista"
OUT = os.path.join(VG, "_controlo3")
CACHE = os.path.join(OUT, "_orto472062")
os.makedirs(CACHE, exist_ok=True)

TRES = [8845729, 8845731, 8845739]
DONO = 472062
PX = 1.0
EPOCAS = [("2007", "Ortos2007-FalsaCor"), ("2010", "Ortos2010-FalsaCor"),
          ("2012", "Ortos2012-FalsaCor"), ("2018", "Ortos2018-IRG"),
          ("2021", "Ortos2021-IRG"), ("2025", "Ortos2025-IRG")]

tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
R = json.load(open(os.path.join(VG, "reg01_landsat.json"), encoding="utf-8"))
ENT = {int(k): v for k, v in R["ent"].items()}
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K

BL = []
for ft in KF:
    c = ft["properties"].get("CUL_ID")
    if c is None or int(c) not in ENT or ENT[int(c)] != DONO:
        continue
    g = para(shape(ft["geometry"])).buffer(0)
    BL.append(dict(cul=int(c), geom=g, ha=g.area / 1e4, alvo=int(c) in TRES))
print("blocos do ENT %d: %d   (alvos %d · controlo %d)"
      % (DONO, len(BL), sum(b["alvo"] for b in BL), sum(not b["alvo"] for b in BL)))

xs = [v for b in BL for v in (b["geom"].bounds[0], b["geom"].bounds[2])]
ys = [v for b in BL for v in (b["geom"].bounds[1], b["geom"].bounds[3])]
BB = (min(xs) - 30, min(ys) - 30, max(xs) + 30, max(ys) + 30)
NCx, NLy = int((BB[2] - BB[0]) / PX), int((BB[3] - BB[1]) / PX)
print("janela: %.0f x %.0f m -> %d x %d px a %.2f m" % (BB[2] - BB[0], BB[3] - BB[1],
                                                        NCx, NLy, PX))
EE, NN = np.meshgrid(BB[0] + (np.arange(NCx) + .5) * PX,
                     BB[3] - (np.arange(NLy) + .5) * PX)
pts = np.column_stack([EE.ravel(), NN.ravel()])
for b in BL:
    b["m"] = MP(np.array(list(b["geom"].exterior.coords))
                ).contains_points(pts).reshape(NLy, NCx)
    b["n"] = int(b["m"].sum())
CTRL = np.any([b["m"] for b in BL if not b["alvo"]], axis=0)
print("pixeis: alvos %d · controlo %d"
      % (sum(b["n"] for b in BL if b["alvo"]), int(CTRL.sum())))


def getmap(ano, camada):
    f = os.path.join(CACHE, "%s_%s_%dm.png" % (ano, camada, int(PX)))
    if os.path.exists(f) and os.path.getsize(f) > 5000:
        return np.array(Image.open(f).convert("RGB"))
    u = "https://cartografia.dgterritorio.gov.pt/wms/ortos%s" % ano
    p = {"service": "WMS", "request": "GetMap", "version": "1.1.1",
         "layers": camada, "styles": "", "srs": "EPSG:3763",
         "bbox": "%f,%f,%f,%f" % BB, "width": NCx, "height": NLy,
         "format": "image/png"}
    r = requests.get(u, params=p, timeout=900)
    if "image" not in (r.headers.get("Content-Type") or ""):
        raise IOError("%s %s: %s" % (ano, camada, r.text[:160]))
    open(f, "wb").write(r.content)
    return np.array(Image.open(f).convert("RGB"))


FR, falhas = {}, []
for ano, cam in EPOCAS:
    try:
        a = getmap(ano, cam).astype("float32")
    except Exception as e:
        print("  %s FALHOU: %s" % (ano, str(e)[:120]))
        falhas.append(ano)
        continue
    ir, rd = a[..., 0], a[..., 1]
    v = np.where(ir + rd > 8, (ir - rd) / np.maximum(ir + rd, 1e-6), np.nan)
    cob = float(np.isfinite(v[CTRL]).mean())
    if cob < 0.90:
        print("  %s cobertura do controlo so %.0f %% — cai" % (ano, 100 * cob))
        falhas.append(ano)
        continue
    lim = float(np.nanpercentile(v[CTRL], 10))
    FR[ano] = dict(lim=lim, cob=cob, blocos={})
    for b in BL:
        x = v[b["m"]]
        x = x[np.isfinite(x)]
        FR[ano]["blocos"][b["cul"]] = float(100.0 * np.mean(x < lim)) if x.size else np.nan
    print("  %s ok (limiar %.4f, cobertura do controlo %.0f %%)" % (ano, lim, 100 * cob))

ANOS = [a for a, _ in EPOCAS if a in FR]
print()
print("=" * 96)
print("FRACCAO DE PIXEIS ABAIXO DO PERCENTIL 10 DO CONTROLO, dentro de cada imagem (%)")
print("=" * 96)
print()
print("%-10s %6s %6s %s" % ("CUL_ID", "ha", "", "  ".join("%7s" % a for a in ANOS)))
for b in sorted(BL, key=lambda z: (not z["alvo"], z["cul"])):
    print("%-10d %6.2f %6s %s"
          % (b["cul"], b["ha"], "ALVO" if b["alvo"] else "  -  ",
             "  ".join("%6.1f%%" % FR[a]["blocos"][b["cul"]] for a in ANOS)))
ca = np.array([[FR[a]["blocos"][b["cul"]] for a in ANOS] for b in BL if b["alvo"]])
cc = np.array([[FR[a]["blocos"][b["cul"]] for a in ANOS] for b in BL if not b["alvo"]])
print()
print("%-24s %s" % ("mediana dos TRES", "  ".join("%6.1f%%" % v for v in np.median(ca, 0))))
print("%-24s %s" % ("mediana do CONTROLO", "  ".join("%6.1f%%" % v for v in np.median(cc, 0))))

print()
print("=" * 96)
print("O CRITERIO, julgado pelo que estava escrito antes de correr")
print("=" * 96)
QUEBRA = {8845729: "2024", 8845731: "2023", 8845739: "2023"}
i21 = ANOS.index("2021") if "2021" in ANOS else None
i25 = ANOS.index("2025") if "2025" in ANOS else None
ver = {}
for b in BL:
    if not b["alvo"]:
        continue
    c = b["cul"]
    if i21 is None or i25 is None:
        print("  %d  T3 · a ortofoto nao bracketa a quebra -> NAO TESTAVEL" % c)
        ver[c] = "NAO TESTAVEL"
        continue
    f21, f25 = FR[ANOS[i21]]["blocos"][c], FR[ANOS[i25]]["blocos"][c]
    d = f25 - f21
    dc = np.median(cc, 0)[i25] - np.median(cc, 0)[i21]
    ok = d > 5 and d > 3 * max(dc, 1)
    ver[c] = "JUSTIFICADA" if ok else "NAO JUSTIFICADA"
    print("  %d  quebra Landsat em %s · fraccao 2021 %.1f %% -> 2025 %.1f %% "
          "(%+.1f pp; controlo %+.1f pp)  ->  exclusao %s"
          % (c, QUEBRA[c], f21, f25, d, dc, ver[c]))

json.dump(dict(fraccao=FR, veredicto={str(k): v for k, v in ver.items()},
               falhas=falhas, px=PX),
          open(os.path.join(OUT, "c3_08_orto_tres.json"), "w"), indent=1)
print()
print("escrito c3_08_orto_tres.json")
