# -*- coding: utf-8 -*-
"""C8-01 · extrai a imagem nativa do PDF do esquema e produz recortes.

Nao recalcula nada. So poe o documento a vista, na resolucao a que ele existe.
O PDF tem UMA imagem embebida (2338x1654, DCTDecode) numa pagina A4 landscape.
Renderizar a 300 dpi como fez a C0 INTERPOLA — nao acrescenta informacao.
"""
import os
import json
import fitz
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PDF = r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf"

doc = fitz.open(PDF)
pg = doc[0]
xref = pg.get_images(full=True)[0][0]
info = doc.extract_image(xref)
print("imagem embebida: %s, %d bytes, %dx%d, %s"
      % (info["ext"], len(info["image"]), info["width"], info["height"],
         info["colorspace"]))
raw = os.path.join(AQUI, "esquema_nativo.%s" % info["ext"])
open(raw, "wb").write(info["image"])
im = Image.open(raw).convert("RGB")
W, H = im.size
print("nativo %dx%d px sobre pagina %.1f x %.1f pt (%.1f x %.1f mm)"
      % (W, H, pg.rect.width, pg.rect.height,
         pg.rect.width * 25.4 / 72, pg.rect.height * 25.4 / 72))
print("=> resolucao efectiva do scan: %.1f px/mm  (%.0f dpi)"
      % (W / (pg.rect.width * 25.4 / 72),
         W / (pg.rect.width / 72.0)))

# ampliacao x3 (Lanczos) so para leitura visual dos recortes
Z = 3
RECORTES = {
    # nome            x0    y0    x1    y1   (fraccoes da imagem nativa)
    "A_lobo_oeste":  (0.00, 0.28, 0.20, 0.72),
    "B_corpo_oeste": (0.16, 0.28, 0.44, 0.72),
    "C_corpo_meio":  (0.40, 0.24, 0.68, 0.66),
    "D_corpo_este":  (0.64, 0.20, 1.00, 0.62),
    "E_faixa_baixa": (0.00, 0.60, 0.50, 1.00),
    "F_faixa_baixa2": (0.50, 0.58, 1.00, 1.00),
    "G_topo":        (0.00, 0.00, 1.00, 0.30),
}
meta = {}
for nome, (a, b, c, d) in RECORTES.items():
    box = (int(a * W), int(b * H), int(c * W), int(d * H))
    cr = im.crop(box)
    cr = cr.resize((cr.width * Z, cr.height * Z), Image.LANCZOS)
    p = os.path.join(AQUI, "rec_%s.png" % nome)
    cr.save(p)
    meta[nome] = dict(box=box, saida=os.path.basename(p),
                      tamanho=[cr.width, cr.height])
    print("  %-16s px %s -> %s" % (nome, box, os.path.basename(p)))

json.dump(dict(nativo=[W, H], pagina_mm=[pg.rect.width * 25.4 / 72,
                                         pg.rect.height * 25.4 / 72],
               px_por_mm=W / (pg.rect.width * 25.4 / 72),
               recortes=meta),
          open(os.path.join(AQUI, "c8_01_extrai.json"), "w"), indent=1)
print("\nescrito c8_01_extrai.json")
