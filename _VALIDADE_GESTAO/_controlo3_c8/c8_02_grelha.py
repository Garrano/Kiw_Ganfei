# -*- coding: utf-8 -*-
"""C8-02 · varre o desenho em mosaicos ampliados, para LER, nao para medir.

A C0 renderizou a 300 dpi um scan que existe a 200 dpi. Aqui trabalha-se sobre
a imagem nativa e amplia-se com Lanczos so para leitura visual — nenhum numero
sai deste ficheiro.
"""
import os
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(AQUI, "esquema_nativo.jpeg")).convert("RGB")
W, H = im.size

# a zona do desenho (sem o titulo lateral nem a moldura exterior)
TILES = {
    "T1_oeste_lobo":   (60, 380, 420, 800),
    "T2_v5_v6_meio":   (330, 300, 760, 720),
    "T3_vazio_meio":   (330, 230, 1120, 700),
    "T4_v6_v9":        (980, 200, 1360, 560),
    "T5_v9_v13":       (1250, 200, 1620, 560),
    "T6_v13_v16":      (1500, 280, 1880, 620),
    "T7_v16_v18":      (1780, 320, 2200, 680),
    "T8_notas_topo_e": (1400, 130, 2100, 380),
    "T9_notas_topo_w": (100, 20, 620, 400),
    "T10_caixa_topo":  (1650, 0, 2180, 180),
    "T11_notas_base":  (280, 830, 1400, 1100),
    "T12_notas_base2": (280, 1050, 1400, 1300),
    "T13_cartucho":    (90, 990, 320, 1520),
    "T14_v17_nota":    (1850, 580, 2250, 800),
}
Z = 4
for nome, box in TILES.items():
    cr = im.crop(box)
    cr = cr.resize((cr.width * Z, cr.height * Z), Image.LANCZOS)
    if cr.width > 2400:
        f = 2400.0 / cr.width
        cr = cr.resize((int(cr.width * f), int(cr.height * f)), Image.LANCZOS)
    cr.save(os.path.join(AQUI, "%s.png" % nome))
    print("%-18s %s -> %dx%d" % (nome, box, cr.width, cr.height))
