# -*- coding: utf-8 -*-
"""C8-03 · inventario da tinta VERMELHA no esquema — onde estao as anotacoes.

Objectivo: localizar TODAS as anotacoes a vermelho, para responder a uma
pergunta factual e so a ela: **o desenho anota «1,77 ha» nalgum sitio?**

Metodo: mascara de vermelho saturado (a tinta da caneta, distinta do rosa
claro dos «Limites do terreno» impressos e do tracejado dos sectores),
dilatacao para juntar tracos da mesma anotacao, e recorte de cada aglomerado.
Nao mede areas nem escalas — so poe cada anotacao a vista.
"""
import os
import json
import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(AQUI, "esquema_nativo.jpeg")).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape

# caneta vermelha: forte em R, fraca em G e B, e escura o suficiente para nao
# ser o rosa impresso dos limites (que tem G e B altos)
tinta = (R > 90) & (R - G > 55) & (R - B > 35) & (G < 150)
print("pixeis de tinta vermelha: %d (%.3f %% da folha)"
      % (tinta.sum(), 100.0 * tinta.sum() / tinta.size))

d = ndimage.binary_dilation(tinta, np.ones((9, 9)))
lab, n = ndimage.label(d, np.ones((3, 3)))
print("aglomerados brutos: %d" % n)

objs = ndimage.find_objects(lab)
grupos = []
for i, sl in enumerate(objs, start=1):
    m = (lab[sl] == i) & tinta[sl]
    s = int(m.sum())
    if s < 120:                      # ruido de compressao JPEG
        continue
    y0, y1 = sl[0].start, sl[0].stop
    x0, x1 = sl[1].start, sl[1].stop
    grupos.append(dict(id=len(grupos), px=s, x0=x0, x1=x1, y0=y0, y1=y1,
                       larg=x1 - x0, alt=y1 - y0))
grupos.sort(key=lambda g: g["x0"])
print("aglomerados com >=120 px de tinta: %d" % len(grupos))
print()
print("%3s %7s %6s %6s %6s %6s" % ("id", "px", "x0", "y0", "larg", "alt"))
Z = 8
for g in grupos:
    print("%3d %7d %6d %6d %6d %6d"
          % (g["id"], g["px"], g["x0"], g["y0"], g["larg"], g["alt"]))
    pad = 12
    box = (max(0, g["x0"] - pad), max(0, g["y0"] - pad),
           min(W, g["x1"] + pad), min(H, g["y1"] + pad))
    cr = im.crop(box)
    z = min(Z, max(2, int(900 / max(cr.width, 1))))
    cr = cr.resize((cr.width * z, cr.height * z), Image.LANCZOS)
    cr.save(os.path.join(AQUI, "tinta_%02d.png" % g["id"]))

json.dump(grupos, open(os.path.join(AQUI, "c8_03_tinta.json"), "w"), indent=1)
print("\nescrito c8_03_tinta.json e %d recortes tinta_NN.png" % len(grupos))
