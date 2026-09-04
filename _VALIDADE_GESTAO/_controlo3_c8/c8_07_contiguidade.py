# -*- coding: utf-8 -*-
"""C8-07 · «um lobulo fisicamente separado ao extremo oeste» — e?

PERGUNTA FIXA
-------------
O C8 descreve o troco das valvulas 1-5 como «um lobulo fisicamente separado».
No desenho, a linha «Limites do terreno» (rosa/magenta na legenda) e continua
entre os dois trocos, ou ha uma interrupcao?

  H0 (a falsificar): a linha de limite do troco oeste e a do corpo principal
  sao componentes conexas DISTINTAS na imagem.

Falsifica-se se as duas caem na mesma componente conexa depois de fechar
buracos de 1-2 px de compressao JPEG.

O QUE ISTO NAO DECIDE: nao diz que a rede e continua, nem que a agua passa.
Diz o que o DESENHO desenha. Continuidade de propriedade nao e continuidade
hidraulica — e a segunda continua em NAO TESTAVEL desde a R3 da C0.
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

# «Limites do terreno» = tracado rosa/magenta claro (na legenda e a ultima
# entrada). Distingue-se da tinta vermelha por ter B alto.
rosa = (R > 120) & (R - G > 25) & (B - G > -10) & (B > 90)
zona = np.zeros((H, W), bool)
zona[150:900, 60:2280] = True
m = rosa & zona
print("pixeis de limite (rosa): %d" % m.sum())

f = ndimage.binary_closing(m, np.ones((5, 5)))
lab, n = ndimage.label(f, np.ones((3, 3)))
tam = ndimage.sum(f, lab, range(1, n + 1))
i = 1 + int(np.argmax(tam))
ys, xs = np.where(lab == i)
print("componentes: %d ; a maior tem %d px, x %d..%d, y %d..%d"
      % (n, int(tam.max()), xs.min(), xs.max(), ys.min(), ys.max()))

# a maior componente estende-se do troco oeste ao corpo?
LOBO_X = 470
tem_oeste = bool((xs < LOBO_X).sum() > 200)
tem_corpo = bool((xs > 1500).sum() > 200)
print("  a maior componente toca o troco OESTE (x<%d): %s (%d px)"
      % (LOBO_X, tem_oeste, int((xs < LOBO_X).sum())))
print("  a maior componente toca o extremo ESTE (x>1500): %s (%d px)"
      % (tem_corpo, int((xs > 1500).sum())))
print()
if tem_oeste and tem_corpo:
    print("  H0 FALSIFICADA: o limite do terreno e UMA linha continua do troco")
    print("  oeste ao extremo este. O troco das valvulas 1-5 nao e uma ilha —")
    print("  e o extremo oeste da MESMA parcela desenhada, separado do corpo")
    print("  regado por parcelas sem tramado de sector (ver T3_vazio_meio.png).")
else:
    print("  H0 sobrevive: sao componentes distintas.")

# quanto vale a faixa sem sector, em fraccao do comprimento do desenho
cor = ((a.max(2) - a.min(2)) > 22) & (a.max(2) > 120) & zona
cor = ndimage.binary_opening(cor, np.ones((5, 5)))
col = cor.sum(0)
comx = np.where(col > 3)[0]
# maior intervalo em x sem tramado, dentro do desenho
vazio, ini, melhor = 0, None, (0, 0, 0)
for x in range(comx.min(), comx.max() + 1):
    if col[x] <= 3:
        if ini is None:
            ini = x
        vazio += 1
        if vazio > melhor[0]:
            melhor = (vazio, ini, x)
    else:
        ini, vazio = None, 0
print()
print("tramado de sector presente de x=%d a x=%d" % (comx.min(), comx.max()))
print("maior intervalo em x SEM tramado nenhum: %d px, de x=%d a x=%d"
      % melhor)
print("  = %.1f %% do comprimento desenhado"
      % (100.0 * melhor[0] / (comx.max() - comx.min())))

json.dump(dict(componentes=int(n), maior_px=int(tam.max()),
               maior_x=[int(xs.min()), int(xs.max())],
               toca_oeste=tem_oeste, toca_este=tem_corpo,
               tramado_x=[int(comx.min()), int(comx.max())],
               maior_vazio_px=int(melhor[0]),
               maior_vazio_x=[int(melhor[1]), int(melhor[2])]),
          open(os.path.join(AQUI, "c8_07_contiguidade.json"), "w"), indent=1)
print("\nescrito c8_07_contiguidade.json")
