# -*- coding: utf-8 -*-
"""Ortofoto sobre os cinco blocos do ENT 297313 — declínio ou chão?

A PERGUNTA
----------
A REG-01 (Sentinel-2) e a sua replicação (Landsat, 100 cenas) puseram cinco
blocos de kiwi do ENT 297313 no fundo da distribuição regional, com degrau de
−0,24 a −0,32 (Landsat) e −0,21 a −0,40 (S2), duas a quatro vezes pior do que os
focos de Ganfei.

**Duas constelações concordarem não decide o que se está a ver.** Ambas veriam
solo lavrado da mesma maneira, e o NDMI baixo é compatível com solo nu. Um bloco
arrancado a meio da série produz exactamente este degrau — e não é sintoma
nenhum. É a ressalva que a guarda de cultura de `reg01_landsat.py` escreve: a
declaração do IFAP cobre uma campanha, e **a continuidade da cultura ao longo da
linha de base não está verificada.**

O QUE NÃO FOI POSSÍVEL, E PORQUÊ
--------------------------------
**O LiDAR está bloqueado.** As folhas MDS/MDT-50cm-157557-07-2025 existem no
catálogo da DGT (20,6 e 20,1 MB), mas o endpoint de descarga passou a redirigir
para autenticação (Keycloak, `auth.cdd.dgterritorio.gov.pt`). Falha inclusive na
folha 157563, que foi descarregada com sucesso a 29-08-2026. **Não se contornou.**
Fica registado como acesso perdido, não como teste negativo.

A ortofoto vem por outro serviço — o WMS público em
`cartografia.dgterritorio.gov.pt/wms/ortos<ano>`, que serve RGB **e IRG**, logo
NDVI a 25 cm. Anónimo, e é o que este ficheiro usa.

CRITÉRIOS, FIXADOS ANTES DE OLHAR PARA AS IMAGENS
--------------------------------------------------
    O1 · NÍVEL, dentro da MESMA imagem. Comparam-se os cinco blocos com os
         **outros doze blocos do mesmo dono** que não deram degrau. Se em 2025 os
         cinco caírem dentro do intervalo interquartil dos doze, havia coberto.
         Se caírem muito abaixo, o coberto já não estava lá.
         **Nunca se compara brilho entre épocas** — só dentro de cada imagem.

    O2 · QUANDO separam. Seis épocas: 2007, 2010, 2012, 2018, 2021, 2025. A
         época em que os cinco se destacam dos doze **data** a mudança. Se
         separarem já em 2018 ou 2021, a mudança é anterior ao degrau de 2025-26
         e o degrau não é o acontecimento.

    O3 · ÂNCORA DE CHÃO, dentro de cada imagem. Sem ela o nível não se
         interpreta — é a lição do P5: uma medida pode separar duas unidades por
         uma propriedade que não é a que dá nome ao facto. Usa-se o percentil 5
         do NDVI da janela (estradas, solo). **É uma âncora fraca e diz-se.**
         Se a âncora de chão e a de coberto não discriminarem numa época, essa
         época **não se lê**: escreve-se «instrumento não resolve».

    O4 · O QUE A ORTOFOTO NÃO PODE, escrito antes de correr. A mais recente é de
         2025. **O degrau maior é de Julho de 2026.** Nenhuma ortofoto vê o
         estado actual destes blocos. A ortofoto responde a «já estavam sem
         coberto antes?», não a «estão agora?».
"""
import io
import json
import os

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
CACHE = os.path.join(VG, "_orto297313")
os.makedirs(CACHE, exist_ok=True)

OS_CINCO = [6705427, 6705429, 6705428, 6705432, 6705442]
EPOCAS = [("2007", "Ortos2007-RGB", "Ortos2007-FalsaCor"),
          ("2010", "Ortos2010-RGB", "Ortos2010-FalsaCor"),
          ("2012", "Ortos2012-RGB", "Ortos2012-FalsaCor"),
          ("2018", "Ortos2018-RGB", "Ortos2018-IRG"),
          ("2021", "Ortos2021-RGB", "Ortos2021-IRG"),
          ("2025", "Ortos2025-RGB", "Ortos2025-IRG")]

# ------------------------------------------------------------- os polígonos
tr = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
para = lambda g: sht(lambda x, y, z=None: tr.transform(x, y), g)
K = json.load(open(os.path.join(H2, "ifap_kiwi_largo.json"), encoding="utf-8"))
KF = K["features"] if isinstance(K, dict) else K
mau = sorted({str(f["properties"].get("PUN_CUL_COD")) for f in KF} - {"124"})
if mau:
    raise SystemExit("ifap_kiwi_largo.json tem culturas nao-kiwi: %s" % mau)

P = json.load(open(os.path.join(H2, "ifap_parcelas_largo.json"), encoding="utf-8"))
PF = P["features"] if isinstance(P, dict) else P
parc = [(para(shape(f["geometry"])).buffer(0), f["properties"].get("ENT_ID"))
        for f in PF]

BL = []
for ft in KF:
    cul = ft["properties"].get("CUL_ID")
    g = para(shape(ft["geometry"])).buffer(0)
    if g.is_empty or g.area / 1e4 < 0.5:
        continue
    c = g.centroid
    ent = next((e for pg, e in parc if pg.contains(c)), None)
    BL.append(dict(cul=int(cul), geom=g, ha=g.area / 1e4, ent=ent))

CINCO = [b for b in BL if b["cul"] in OS_CINCO]
DOZE = [b for b in BL if b["ent"] == 297313 and b["cul"] not in OS_CINCO]
print("os cinco: %d blocos, %.2f ha" % (len(CINCO), sum(b["ha"] for b in CINCO)))
print("controlo do MESMO dono (297313, sem degrau): %d blocos, %.2f ha"
      % (len(DOZE), sum(b["ha"] for b in DOZE)))

todos = CINCO + DOZE
xs = [v for b in todos for v in (b["geom"].bounds[0], b["geom"].bounds[2])]
ys = [v for b in todos for v in (b["geom"].bounds[1], b["geom"].bounds[3])]
BB = (min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40)
LARG, ALT = BB[2] - BB[0], BB[3] - BB[1]
PX = 0.5                                   # 50 cm: comum a todas as épocas
NCx, NLy = int(LARG / PX), int(ALT / PX)
print("janela: %.0f x %.0f m  ->  %d x %d px a %.2f m" % (LARG, ALT, NCx, NLy, PX))

EE, NN = np.meshgrid(BB[0] + (np.arange(NCx) + .5) * PX,
                     BB[3] - (np.arange(NLy) + .5) * PX)
pts = np.column_stack([EE.ravel(), NN.ravel()])


def masc(bloco):
    return MP(np.array(list(bloco["geom"].exterior.coords))
              ).contains_points(pts).reshape(NLy, NCx)


for b in todos:
    b["m"] = masc(b)
M5 = np.any([b["m"] for b in CINCO], axis=0)
M12 = np.any([b["m"] for b in DOZE], axis=0)
print("pixeis: cinco %d · doze %d" % (M5.sum(), M12.sum()))


# ------------------------------------------------------------------ o WMS
def getmap(ano, camada):
    f = os.path.join(CACHE, "%s_%s.png" % (ano, camada))
    if os.path.exists(f) and os.path.getsize(f) > 5000:
        # convert("RGB"): algumas epocas voltam em paleta e davam array 2-D,
        # que fazia `a[..., 0]` devolver uma linha em vez de uma banda.
        return np.array(Image.open(f).convert("RGB"))
    u = "https://cartografia.dgterritorio.gov.pt/wms/ortos%s" % ano
    p = {"service": "WMS", "request": "GetMap", "version": "1.1.1",
         "layers": camada, "styles": "", "srs": "EPSG:3763",
         "bbox": "%f,%f,%f,%f" % BB, "width": NCx, "height": NLy,
         "format": "image/png"}
    r = requests.get(u, params=p, timeout=600)
    if "image" not in (r.headers.get("Content-Type") or ""):
        raise IOError("%s %s: %s" % (ano, camada, r.text[:200]))
    open(f, "wb").write(r.content)
    return np.array(Image.open(f).convert("RGB"))


def ndvi_de(a):
    """IRG / FalsaCor: b1 = infravermelho, b2 = vermelho, b3 = verde."""
    ir = a[..., 0].astype("float32")
    rd = a[..., 1].astype("float32")
    v = (ir - rd) / np.maximum(ir + rd, 1e-6)
    return np.where((ir + rd) > 8, v, np.nan)      # fora da cobertura = NaN


RES = {}
print()
for ano, cr, ci in EPOCAS:
    try:
        rgb = getmap(ano, cr)
        irg = getmap(ano, ci)
    except Exception as e:
        print("%s  FALHOU: %s" % (ano, str(e)[:110]))
        continue
    nd = ndvi_de(irg)
    val = np.isfinite(nd)
    cob = float(val.mean())
    if cob < 0.5:
        print("%s  cobertura da janela %.0f %% — nao se le" % (ano, 100 * cob))
        continue
    v5 = nd[M5 & val]
    v12 = nd[M12 & val]
    chao = float(np.nanpercentile(nd[val], 5))
    copa = float(np.nanpercentile(nd[val], 95))
    if len(v5) < 500 or len(v12) < 500:
        print("%s  pixeis a menos" % ano)
        continue
    RES[ano] = dict(
        cinco=[float(np.percentile(v5, q)) for q in (25, 50, 75)],
        doze=[float(np.percentile(v12, q)) for q in (25, 50, 75)],
        chao=chao, copa=copa, n5=int(v5.size), n12=int(v12.size),
        rgb=rgb, ndvi=nd)
    print("%s  lido  (n cinco %d · n doze %d · cobertura %.0f %%)"
          % (ano, v5.size, v12.size, 100 * cob))

print()
print("=" * 94)
print("O1 e O2 — nivel de NDVI DENTRO de cada imagem, cinco contra doze do mesmo dono")
print("=" * 94)
print()
print("%-6s %26s %26s %10s %10s %s"
      % ("epoca", "os CINCO  p25 med p75", "os DOZE  p25 med p75",
         "chao p5", "copa p95", "separam?"))
for ano in sorted(RES):
    r = RES[ano]
    disc = r["copa"] - r["chao"] > 0.15         # a ancora discrimina?
    sep = r["cinco"][2] < r["doze"][0]           # IQR disjuntos, cinco abaixo
    print("%-6s  %7.3f %7.3f %7.3f    %7.3f %7.3f %7.3f  %9.3f %9.3f   %s"
          % (ano, r["cinco"][0], r["cinco"][1], r["cinco"][2],
             r["doze"][0], r["doze"][1], r["doze"][2], r["chao"], r["copa"],
             ("SIM, cinco abaixo" if sep else "nao")
             if disc else "ANCORA NAO DISCRIMINA — nao se le"))

json.dump({a: {k: v for k, v in r.items() if k not in ("rgb", "ndvi")}
           for a, r in RES.items()},
          open(os.path.join(VG, "orto_297313.json"), "w"), indent=1)

# ------------------------------------------------------------------ figura
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

anos = sorted(RES)
fig, axs = plt.subplots(2, len(anos), figsize=(3.1 * len(anos), 6.6))
if len(anos) == 1:
    axs = axs.reshape(2, 1)
for j, ano in enumerate(anos):
    r = RES[ano]
    axs[0, j].imshow(r["rgb"][..., :3])
    axs[0, j].set_title(ano, fontsize=12, fontweight="bold")
    axs[1, j].imshow(r["ndvi"], cmap="RdYlGn", vmin=0.0, vmax=0.8)
    for ax in axs[:, j]:
        for b in CINCO:
            xy = np.array(list(b["geom"].exterior.coords))
            ax.plot((xy[:, 0] - BB[0]) / PX, (BB[3] - xy[:, 1]) / PX,
                    color="#eb6834", lw=1.6)
        for b in DOZE:
            xy = np.array(list(b["geom"].exterior.coords))
            ax.plot((xy[:, 0] - BB[0]) / PX, (BB[3] - xy[:, 1]) / PX,
                    color="#2a78d6", lw=1.0, alpha=.75)
        ax.set_xticks([])
        ax.set_yticks([])
axs[0, 0].set_ylabel("RGB", fontsize=11)
axs[1, 0].set_ylabel("NDVI", fontsize=11)
fig.suptitle("ENT 297313 — os cinco blocos do degrau (laranja) contra os doze do "
             "mesmo dono sem degrau (azul)", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(VG, "orto_297313.png"), dpi=125)
print()
print("escrito orto_297313.png e orto_297313.json")
