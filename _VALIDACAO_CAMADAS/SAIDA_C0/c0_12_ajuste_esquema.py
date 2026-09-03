# -*- coding: utf-8 -*-
"""C0-12. Pode o esquema de rega ser georreferenciado sem as ancoras de ouvido?

Teste: se o troco ESTE do desenho (os sectores coloridos, valvulas 6-18)
corresponder a parcela medida, entao o comprimento, a largura e o angulo do
eixo tem de bater a escala declarada (1/3500 @ A1, reduzido para esta folha).
Se baterem, o desenho E proporcional e a georreferenciacao pode fazer-se por
ajuste de forma, sem depender de duas indicacoes verbais.
"""
import json
import os
import numpy as np
import fitz
from scipy import ndimage

OUT = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C0"
eixo = json.load(open(os.path.join(OUT, "c0_11_eixo.json")))

doc = fitz.open(r"C:\Users\Jackster2\Downloads\Esquema de rega retificado.pdf")
pix = doc[0].get_pixmap(dpi=300)
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    pix.height, pix.width, pix.n)[:, :, :3]
H, W = img.shape[:2]
R, G, B = (img[:, :, i].astype(int) for i in range(3))

# «Limites do terreno» rosa, na zona do desenho, sem as anotacoes a mao
rosa = (R > 140) & (R - G > 30) & (R - B > 5) & (G > 70) & (B > 70)
zona = np.zeros((H, W), bool)
zona[380:1320, 120:3260] = True
rz = rosa & zona
rz = ndimage.binary_opening(rz, np.ones((2, 2)))
ys, xs = np.where(rz)
print("linha rosa filtrada: %d px  x %d..%d  y %d..%d"
      % (rz.sum(), xs.min(), xs.max(), ys.min(), ys.max()))


def pca(sel, rot):
    a = xs[sel].astype(float)
    b = ys[sel].astype(float)
    P = np.column_stack([a, -b])                # y para cima
    Pc = P - P.mean(0)
    _, s, vt = np.linalg.svd(Pc, full_matrices=False)
    ang = np.degrees(np.arctan2(vt[0, 1], vt[0, 0])) % 180
    if ang > 90:
        ang -= 180
    p1 = Pc @ vt[0]
    p2 = Pc @ vt[1]
    print("  %-28s n=%6d  eixo %+6.2f graus  comp=%6.0f px  larg=%5.0f px  "
          "(x %d..%d)" % (rot, sel.sum(), ang, p1.max() - p1.min(),
                          np.percentile(p2, 97) - np.percentile(p2, 3),
                          a.min(), a.max()))
    return ang, p1.max() - p1.min(), np.percentile(p2, 97) - np.percentile(p2, 3)


print()
print("PCA por troco do desenho (x em px do render a 300 dpi):")
res = {}
for rot, sel in (("desenho inteiro", np.ones_like(xs, bool)),
                 ("troco OESTE  x<600", xs < 600),
                 ("meio branco 600-1450", (xs >= 600) & (xs < 1450)),
                 ("troco ESTE   x>=1450", xs >= 1450),
                 ("troco ESTE   x>=1500", xs >= 1500)):
    res[rot] = pca(sel, rot)

# escalas candidatas: m por px a 300 dpi
ESCALAS = {"1/3500@A1, moldura=811mm": 0.8425,
           "1/3500@A1, moldura=831mm": 0.8633,
           "1/3500@A1, moldura=841mm": 0.8737,
           "ancoras de m1_valvulas.py": 1.0787}

print()
print("=" * 78)
print("COMPARACAO COM A PARCELA MEDIDA")
print("  parcela medida (poligono `pomar`): comprimento %.0f m, largura %.0f m,"
      " eixo %+.1f graus acima de E-W"
      % (eixo["comprimento_m"], eixo["largura_m"], 90 - eixo["azimute_deg"]))
print("=" * 78)
ang_e, comp_e, larg_e = res["troco ESTE   x>=1450"]
for nome, mpx in ESCALAS.items():
    print("  %-28s comprimento do troco ESTE = %6.0f m   largura = %5.0f m"
          % (nome, comp_e * mpx, larg_e * mpx))
    print("      erro no comprimento: %+.1f %%   erro na largura: %+.1f %%"
          % (100 * (comp_e * mpx / eixo["comprimento_m"] - 1),
             100 * (larg_e * mpx / eixo["largura_m"] - 1)))
print()
print("  angulo do eixo: desenho (troco ESTE) %+.2f graus ; "
      "parcela medida %+.2f graus ; diferenca %+.2f graus"
      % (ang_e, 90 - eixo["azimute_deg"], ang_e - (90 - eixo["azimute_deg"])))

# escala que o proprio ajuste de forma implica
esc_impl = eixo["comprimento_m"] / comp_e
print()
print("  ESCALA IMPLICADA pelo ajuste de forma (troco ESTE -> parcela): "
      "%.4f m/px" % esc_impl)
print("  ancoras de m1_valvulas.py: 1.0787 m/px  ->  %+.1f %% de erro"
      % (100 * (1.0787 / esc_impl - 1)))
for nome, mpx in ESCALAS.items():
    if "ancoras" in nome:
        continue
    print("  %-28s %.4f m/px -> %+.1f %%" % (nome, mpx,
                                             100 * (mpx / esc_impl - 1)))

json.dump({"pca_por_troco": {k: [float(x) for x in v] for k, v in res.items()},
           "escala_implicada_m_por_px": float(esc_impl),
           "escalas_candidatas": ESCALAS},
          open(os.path.join(OUT, "c0_12_ajuste.json"), "w"), indent=1)
print("\n-> c0_12_ajuste.json")
