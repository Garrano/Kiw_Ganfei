# -*- coding: utf-8 -*-
"""G06 — candidato a `pomar` pela assinatura de COMPASSO DE 5 m.

O que se aprendeu ate aqui, e que justifica esta escolha:

  tentativa 1 (desvio padrao local)      -> 42,99 ha, alastrou para sebes. FALHOU
  tentativa 2 (textura alta e homogenea) -> 14,45 ha, IoU 0,000. FALHOU
  G03 (fraccao de potencia numa banda)   -> mapa ruidoso, sem separacao. FALHOU
  G04 (max da autocorrelacao no anel)    -> mede suavidade, nao compasso. FALHOU
  G05 (PROMINENCIA do pico + compasso)   -> em 2025 e em 2012 aparece uma regiao
                                            coerente de COMPASSO 5,0 m que tem a
                                            forma do bloco e mais nada na AOI a
                                            tem. E este o sinal.

Fisicamente: a pergola de kiwi tem as fiadas a 5 m. Em 2025 a cobertura branca
poe as fiadas em altissimo contraste; em 2012, com o copado ainda aberto, as
fiadas jovens tambem se resolvem. A vinha da compassos de 2-3 m, as estufas
7-9 m, o campo lavrado nao da pico nenhum. Nenhum destes calculos toca em NDVI.

Duas epocas independentes, com estados de coberto opostos (fiada nua em 2012,
fiada coberta em 2025), que concordam na mesma geometria — e isso que da
confianca, nao o valor do limiar.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
COMP_MIN, COMP_MAX = 4.4, 5.6        # compasso de kiwi em pergola, metros


def assinatura(ano, lim_prom):
    d = np.load(os.path.join(SAI, "prom_%s.npz" % ano))
    return (d["dpico"] >= COMP_MIN) & (d["dpico"] <= COMP_MAX) & (d["prom"] > lim_prom), d


def limpa(m, abre=2, fecha=3, buraco=6):
    """abre (tira pontos soltos), fecha (une fiadas), tapa so buracos pequenos."""
    m = ndimage.binary_opening(m, np.ones((abre, abre)))
    m = ndimage.binary_closing(m, np.ones((fecha, fecha)))
    inv, n = ndimage.label(~m)
    if n:
        tam = ndimage.sum(~m, inv, range(1, n + 1))
        for k in range(1, n + 1):
            if tam[k - 1] <= buraco:
                # so tapa se o buraco nao toca o bordo da AOI
                ys, xs = np.where(inv == k)
                if ys.min() > 0 and xs.min() > 0 and ys.max() < m.shape[0] - 1 \
                        and xs.max() < m.shape[1] - 1:
                    m[inv == k] = True
    return m


def maiores(m, n=4, minimo=15):
    lab, k = ndimage.label(m, structure=np.ones((3, 3)))
    if not k:
        return m
    tam = ndimage.sum(m, lab, range(1, k + 1))
    ordem = np.argsort(tam)[::-1][:n]
    out = np.zeros_like(m)
    for i in ordem:
        if tam[i] >= minimo:
            out |= (lab == i + 1)
    return out


if __name__ == "__main__":
    a25, d25 = assinatura("2025", 0.45)
    a12, d12 = assinatura("2012", 0.30)
    a10, d10 = assinatura("2010", 0.30)
    print("celulas com compasso 4,4-5,6 m e prominencia acima do limiar:")
    for nm, a in (("2010", a10), ("2012", a12), ("2025", a25)):
        print("  %s: %4d celulas = %5.2f ha" % (nm, a.sum(), a.sum() / 100))

    uniao = a25 | a12 | a10
    cand = maiores(limpa(uniao))
    print("uniao das tres epocas, limpa: %d celulas = %.2f ha" % (cand.sum(), cand.sum() / 100))
    np.save(os.path.join(SAI, "cand_pomar.npy"), cand)
    for nm, a in (("2010", a10), ("2012", a12), ("2025", a25)):
        np.save(os.path.join(SAI, "assin_%s.npy" % nm), a)

    # ---- inspeccao visual obrigatoria: contorno sobre a ortofoto -------------
    for ano in ("2012", "2021", "2025"):
        orto = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        rgb = np.clip(np.transpose(orto[:3], (1, 2, 0)) / 255.0, 0, 1)
        fig, ax = plt.subplots(figsize=(22, 11), dpi=110)
        ax.imshow(rgb, extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.contour(cand.astype(float), levels=[0.5], colors="yellow", linewidths=1.6,
                   extent=[AOI[0], AOI[2], AOI[1], AOI[3]], origin="upper")
        ax.set_title("candidato a `pomar` (compasso 5 m, 2010+2012+2025) sobre ortofoto %s "
                     "— %.2f ha" % (ano, cand.sum() / 100), fontsize=13)
        ax.tick_params(labelsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(SAI, "v06_cand_sobre_%s.png" % ano), dpi=110)
        plt.close(fig)
        print("-> v06_cand_sobre_%s.png" % ano)

    # comparacao com a mascara antiga
    from matplotlib.path import Path as MP
    antigas = json.load(open(r"C:\Users\Jackster2\Downloads\ganfei_s2\sentinel\masks.json"))
    yy, xx = np.mgrid[0:100, 0:200]
    pts = np.vstack((xx.ravel(), yy.ravel())).T
    velho = MP(antigas["pomar"]).contains_points(pts).reshape(100, 200)
    inter = (cand & velho).sum()
    print("\nantigo %.2f ha | novo %.2f ha | interseccao %.2f ha | IoU %.3f"
          % (velho.sum() / 100, cand.sum() / 100, inter / 100,
             inter / max((cand | velho).sum(), 1)))
    print("so no antigo %.2f ha | so no novo %.2f ha"
          % ((velho & ~cand).sum() / 100, (cand & ~velho).sum() / 100))
    np.save(os.path.join(SAI, "pomar_antigo.npy"), velho)
