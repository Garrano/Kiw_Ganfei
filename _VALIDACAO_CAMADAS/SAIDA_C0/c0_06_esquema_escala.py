# -*- coding: utf-8 -*-
"""C0-06. O esquema de rega tem escala declarada? E proporcional?

O bloco de titulo do PDF diz  ESC: 1/3500 @ A1.  Se o desenho de base for um
plano CAD impresso (e nao um esboco a mao), entao E proporcional, e a
afirmacao contraria em m1_valvulas.py cai.

Este script:
 1. mede a moldura do desenho em pixeis e converte para mm da folha;
 2. deduz o factor de reducao A1 -> folha digitalizada e a escala efectiva;
 3. extrai a linha «Limites do terreno» (rosa/magenta) e o comprimento
    da parcela desenhada, em metros a escala deduzida;
 4. compara com o comprimento da parcela real medida na ortofoto/Sentinel.
"""
import os
import numpy as np
import fitz
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
PDF = r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf"
DPI = 300

doc = fitz.open(PDF)
pg = doc[0]
pix = pg.get_pixmap(dpi=DPI)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width,
                                                         pix.n)[:, :, :3]
H, W = img.shape[:2]
pxmm = DPI / 25.4
print("render %dx%d px @ %d dpi = %.4f px/mm ; folha %.1f x %.1f mm"
      % (W, H, DPI, pxmm, W / pxmm, H / pxmm))

# ------------------------------------------------------- 1. moldura do desenho
g = img.mean(2)
escuro = g < 140
# linhas verticais/horizontais longas
colh = escuro.sum(0)
linh = escuro.sum(1)
cand_v = np.where(colh > 0.55 * H)[0]
cand_h = np.where(linh > 0.55 * W)[0]
print("colunas com >55%% de pixeis escuros:", cand_v[:20], "...", cand_v[-10:]
      if len(cand_v) else "")
print("linhas  com >55%% de pixeis escuros:", cand_h[:20], "...", cand_h[-10:]
      if len(cand_h) else "")
if len(cand_v) >= 2 and len(cand_h) >= 2:
    x0, x1 = cand_v.min(), cand_v.max()
    y0, y1 = cand_h.min(), cand_h.max()
    lm = (x1 - x0) / pxmm
    am = (y1 - y0) / pxmm
    print("moldura: x %d..%d  y %d..%d  =>  %.1f x %.1f mm  (racio %.4f)"
          % (x0, x1, y0, y1, lm, am, lm / am))
    print("A1 util tipico 811x554 mm (racio 1.464) ; A1 folha 841x594 "
          "(racio 1.416)")
    for nome, (LA, AA) in (("A1 folha 841x594", (841.0, 594.0)),
                           ("A1 util 811x554", (811.0, 554.0))):
        red = LA / lm
        print("  se a moldura for %s -> reducao x%.4f -> escala efectiva "
              "1:%.0f  =>  1 mm da folha = %.3f m no terreno"
              % (nome, red, 3500 * red, 3500 * red / 1000.0))

# ------------------------------------------------- 2. cores presentes no plano
R, G, B = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
rosa = (R > 150) & (R - G > 35) & (R - B > 10) & (G > 80)
azulcan = (B - R > 40) & (B > 130)
verde = (G - R > 25) & (G - B > 20)
print()
print("pixeis por cor: rosa/magenta=%d  azul-caneta=%d  verde=%d"
      % (rosa.sum(), azulcan.sum(), verde.sum()))

# restringir a zona do desenho (metade superior, sem legenda nem titulo)
zona = np.zeros((H, W), bool)
zona[int(0.10 * H):int(0.50 * H), int(0.03 * W):int(0.90 * W)] = True
rz = rosa & zona
ys, xs = np.where(rz)
print("linha do terreno (rosa) na zona do desenho: %d px, "
      "x %d..%d (%d px), y %d..%d (%d px)"
      % (rz.sum(), xs.min(), xs.max(), xs.max() - xs.min(),
         ys.min(), ys.max(), ys.max() - ys.min()))

if len(cand_v) >= 2:
    for nome, LA in (("A1 folha 841", 841.0), ("A1 util 811", 811.0)):
        mpm = 3500 * (LA / lm) / 1000.0          # metros por mm de folha
        comp = (xs.max() - xs.min()) / pxmm * mpm
        alt = (ys.max() - ys.min()) / pxmm * mpm
        print("  com %s: parcela desenhada = %.0f m (E-W) x %.0f m (N-S)"
              % (nome, comp, alt))

fig, ax = plt.subplots(1, 2, figsize=(20, 7), dpi=130)
ax[0].imshow(img)
ax[0].set_title("esquema, render %d dpi" % DPI, fontsize=9)
ax[1].imshow(rz, cmap="gray_r")
ax[1].set_title("mascara «Limites do terreno» (rosa) na zona do desenho",
                fontsize=9)
for a in ax:
    a.set_xticks([]); a.set_yticks([])
fig.savefig(os.path.join(OUT, "c0_06_esquema_rosa.png"), bbox_inches="tight")
plt.close(fig)
Image.fromarray(img).save(os.path.join(OUT, "c0_06_esquema_300dpi.png"))
print("\n-> c0_06_esquema_rosa.png, c0_06_esquema_300dpi.png")
