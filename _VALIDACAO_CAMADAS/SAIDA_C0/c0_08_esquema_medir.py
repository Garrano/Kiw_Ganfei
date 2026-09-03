# -*- coding: utf-8 -*-
"""C0-08. Medicoes objectivas sobre o esquema de rega:
 a) moldura do desenho -> escala efectiva a partir do 1/3500 @ A1 declarado;
 b) posicao dos circulos das valvulas (aneis vermelho-escuro) por deteccao;
 c) a conduta principal (linha preta continua) e os lados N/S;
 d) eixo principal da parcela desenhada, por PCA da linha rosa.
Tudo em pixeis do render a 300 dpi, que e o sistema que m1_valvulas.py usa.
"""
import os
import numpy as np
import fitz
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3]
H, W = img.shape[:2]
pxmm = 300 / 25.4
R, G, B = (img[:, :, i].astype(int) for i in range(3))

# ---------------------------------------------------------------- a) moldura
esc = img.mean(2) < 150
lab, n = ndimage.label(esc, np.ones((3, 3)))
tam = ndimage.sum(esc, lab, range(1, n + 1))
i = 1 + int(np.argmax(tam))
ys, xs = np.where(lab == i)
print("maior componente escura: %d px, caixa x %d..%d  y %d..%d"
      % (len(xs), xs.min(), xs.max(), ys.min(), ys.max()))
lm = (xs.max() - xs.min()) / pxmm
am = (ys.max() - ys.min()) / pxmm
print("moldura = %.1f x %.1f mm na folha digitalizada (racio %.4f)"
      % (lm, am, lm / am))
print("A1 841x594 racio 1.4158 ; A1 com margem 811x554 racio 1.4639")
for nome, LA in (("moldura = 841 mm (A1 cheia)", 841.0),
                 ("moldura = 811 mm (A1 com margem)", 811.0),
                 ("moldura = 831 mm", 831.0)):
    red = LA / lm
    mpx = 3500 * red / 1000.0 / pxmm       # metros por pixel a 300 dpi
    print("  %-34s reducao x%.3f  escala 1:%.0f  %.4f m/px(300dpi)"
          % (nome, red, 3500 * red, mpx))

# --------------------------------------------------- b) circulos das valvulas
vermelho = (R > 90) & (R - G > 40) & (R - B > 30) & (R < 220) & (G < 150)
zona = np.zeros((H, W), bool)
zona[350:1350, 100:3300] = True
vm = vermelho & zona
vm = ndimage.binary_closing(vm, np.ones((5, 5)))
lab2, n2 = ndimage.label(vm, np.ones((3, 3)))
print()
print("componentes vermelho-escuro na zona do desenho: %d" % n2)
circ = []
for j in range(1, n2 + 1):
    m = lab2 == j
    s = m.sum()
    if not (400 < s < 12000):
        continue
    ys, xs = np.where(m)
    h = ys.max() - ys.min() + 1
    w = xs.max() - xs.min() + 1
    if not (18 < w < 95 and 18 < h < 95):
        continue
    if abs(w - h) > 0.45 * max(w, h):
        continue
    circ.append((float(xs.mean()), float(ys.mean()), int(s), w, h))
circ.sort()
print("candidatos a circulo de valvula: %d" % len(circ))
for k, (x, y, s, w, h) in enumerate(circ):
    print("  #%02d  x=%7.1f  y=%7.1f  area=%5d  %dx%d" % (k, x, y, s, w, h))

# ------------------------------------------------------- d) eixo da parcela
rosa = (R > 140) & (R - G > 30) & (R - B > 5) & (G > 70) & (B > 70)
rz = rosa & zona
ys, xs = np.where(rz)
P = np.column_stack([xs, ys - 0.0])
Pc = P - P.mean(0)
u, s, vt = np.linalg.svd(Pc, full_matrices=False)
ang = np.degrees(np.arctan2(-vt[0, 1], vt[0, 0]))   # y para baixo -> inverter
print()
print("eixo principal da linha rosa (PCA): %.2f graus acima da horizontal "
      "da folha" % ang)
proj = Pc @ vt[0]
print("comprimento ao longo do eixo: %.0f px ; largura: %.0f px"
      % (proj.max() - proj.min(), (Pc @ vt[1]).max() - (Pc @ vt[1]).min()))

fig, ax = plt.subplots(figsize=(22, 8), dpi=140)
ax.imshow(img[300:1350, 100:3300])
for x, y, s, w, h in circ:
    ax.add_patch(plt.Circle((x - 100, y - 300), 40, fill=False, color="lime",
                            lw=1.4))
    ax.text(x - 100, y - 340, "%d" % x, color="lime", fontsize=6, ha="center")
ax.set_title("circulos de valvula detectados, rotulados com o x absoluto "
             "(px 300 dpi)", fontsize=10)
fig.savefig(os.path.join(OUT, "c0_08_valvulas_detectadas.png"),
            bbox_inches="tight")
plt.close(fig)
print("-> c0_08_valvulas_detectadas.png")
