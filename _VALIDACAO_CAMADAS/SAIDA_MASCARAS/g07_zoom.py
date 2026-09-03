# -*- coding: utf-8 -*-
"""G07 — zoom sobre o candidato, para inspeccionar bordo a bordo.

Duas duvidas levantadas pela vista geral (v06_cand_sobre_2025.png):
 a) um lobulo a NORTE do rio Minho (E530080-530200, N4655330-4655560) entrou no
    candidato — e vinha na margem oposta, com compasso parecido. Tem de sair.
 b) dentro do contorno ha faixas verdes/castanhas em 2025 que podem ser parcelas
    sem cobertura, ou podem ser pomar descoberto. Ver de perto.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"

JAN = {
    "z1_norte_rio":  (530020, 530320, 4655280, 4655600),
    "z2_centro":     (530750, 531150, 4655000, 4655330),
    "z3_bordo_sul":  (530500, 530950, 4654850, 4655100),
    "z4_leste":      (531100, 531520, 4655130, 4655430),
}


def recorta(a, jan):
    e0, e1, n0, n1 = jan
    c0 = int((e0 - AOI[0]) / 0.5); c1 = int((e1 - AOI[0]) / 0.5)
    l0 = int((AOI[3] - n1) / 0.5); l1 = int((AOI[3] - n0) / 0.5)
    return a[..., l0:l1, c0:c1]


if __name__ == "__main__":
    cand = np.load(os.path.join(SAI, "cand_pomar.npy"))
    # candidato a 0,5 m para sobrepor sem interpolacao
    c50 = np.kron(cand.astype(float), np.ones((20, 20)))
    for nome, jan in JAN.items():
        fig, axes = plt.subplots(1, 3, figsize=(19, 6.4), dpi=125)
        for ax, ano in zip(axes, ("2012", "2021", "2025")):
            o = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
            r = recorta(o[:3], jan)
            ax.imshow(np.transpose(r, (1, 2, 0)) / 255.0,
                      extent=[jan[0], jan[1], jan[2], jan[3]], origin="upper")
            ax.contour(recorta(c50, jan), levels=[0.5], colors="yellow", linewidths=1.8,
                       extent=[jan[0], jan[1], jan[2], jan[3]], origin="upper")
            ax.set_title(ano, fontsize=11)
            ax.tick_params(labelsize=7)
        fig.suptitle("%s   E %d-%d  N %d-%d   (amarelo = candidato)" % ((nome,) + jan),
                     fontsize=12)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v07_%s.png" % nome), dpi=125)
        plt.close(fig)
        print("-> v07_%s.png" % nome)
