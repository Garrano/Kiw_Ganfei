# -*- coding: utf-8 -*-
"""G02 — recortes a 0,5 m para ver a assinatura de pergola de perto.

Nao mede nada. Serve para eu decidir, a olho, qual e a assinatura fisica
que separa a pergola de kiwi das sebes, vinha, estufas e campo lavrado.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"

JANELAS = {
    "A_nucleo_lente":   (530400, 530700, 4655050, 4655250),
    "B_escada_NE":      (531150, 531500, 4655150, 4655400),
    "C_parcelas_sul":   (530400, 530700, 4654680, 4654880),
    "D_extremo_SW":     (530150, 530450, 4654880, 4655080),
    "E_meio_leste":     (530900, 531200, 4655000, 4655250),
    "F_vinha_SW":       (530250, 530550, 4654600, 4654800),
}
ANOS = ["2004", "2010", "2012", "2021", "2025"]


def recorta(a, jan):
    e0, e1, n0, n1 = jan
    c0 = int((e0 - AOI[0]) / 0.5); c1 = int((e1 - AOI[0]) / 0.5)
    l0 = int((AOI[3] - n1) / 0.5); l1 = int((AOI[3] - n0) / 0.5)
    return a[:3, l0:l1, c0:c1]


if __name__ == "__main__":
    dados = {an: np.load(os.path.join(SAI, "orto_%s_50cm.npy" % an)) for an in ANOS}
    for nome, jan in JANELAS.items():
        fig, axes = plt.subplots(1, len(ANOS), figsize=(4.2 * len(ANOS), 4.6), dpi=130)
        for ax, an in zip(axes, ANOS):
            r = recorta(dados[an], jan)
            ax.imshow(np.transpose(r, (1, 2, 0)) / 255.0,
                      extent=[jan[0], jan[1], jan[2], jan[3]], origin="upper")
            ax.set_title("%s" % an, fontsize=11)
            ax.tick_params(labelsize=6)
        fig.suptitle("%s   E %d-%d  N %d-%d" % ((nome,) + jan), fontsize=12)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v02_%s.png" % nome), dpi=130)
        plt.close(fig)
        print("-> v02_%s.png" % nome)
