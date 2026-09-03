# -*- coding: utf-8 -*-
"""G09 — diagnostico antes de voltar a escolher limiares.

Duas perguntas:
 1. Que luminancia tem, em 2021, o copado de pergola conhecido, e que luminancia
    tem o campo lavrado conhecido? O limiar 110 do G08 abriu buracos no meio do
    copado, logo esta errado.
 2. O teste de solo nu corre o risco de apagar justamente a area em declinio?
    Mede-se a luminancia de 2021 dentro da manchaW e da zona0 antigas. Se elas
    estivessem descobertas em 2021, o teste seria circular ao contrario — e nao
    se pode usar.
"""
import os
import json
import numpy as np
from matplotlib.path import Path as MP

SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
AOI = (529950, 4654600, 531950, 4655600)


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


def caixa(e0, e1, n0, n1):
    m = np.zeros((100, 200), bool)
    c0 = int((e0 - AOI[0]) / 10); c1 = int((e1 - AOI[0]) / 10)
    l0 = int((AOI[3] - n1) / 10); l1 = int((AOI[3] - n0) / 10)
    m[l0:l1, c0:c1] = True
    return m


def perc(a, m, nome):
    v = a[m]
    print("  %-28s n=%4d  p05 %6.1f  p25 %6.1f  p50 %6.1f  p75 %6.1f  p95 %6.1f"
          % (nome, len(v), *np.percentile(v, [5, 25, 50, 75, 95])))


if __name__ == "__main__":
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    velho = raster(ant["pomar"])
    mw = raster(ant["manchaW"])
    z0 = raster(ant["zona0"])

    for ano in ("2012", "2021", "2025"):
        a = np.load(os.path.join(SAI, "orto_%s_10m.npy" % ano)).astype("float32")
        lum = a[:3].mean(0)
        print("\n=== luminancia por celula de 10 m, ortofoto %s ===" % ano)
        # copado de pergola de referencia: nucleo da lente, longe de bordos
        perc(lum, caixa(530350, 530800, 4655050, 4655250) & velho, "nucleo da lente (pergola)")
        perc(lum, caixa(530950, 531080, 4655120, 4655280), "parcela lavrada interior")
        perc(lum, caixa(531280, 531450, 4655180, 4655330), "faixa NE (pergola)")
        perc(lum, caixa(530500, 530800, 4654680, 4654850), "parcelas pequenas a sul")
        perc(lum, mw, "manchaW antiga")
        perc(lum, z0, "zona0 antiga")
        perc(lum, velho, "pomar antigo inteiro")

    # quanto da manchaW/zona0 cairia com cada limiar em 2021
    lum21 = np.load(os.path.join(SAI, "orto_2021_10m.npy")).astype("float32")[:3].mean(0)
    print("\n=== fraccao excluida por limiar de solo nu (ortofoto 2021) ===")
    print("  limiar | manchaW | zona0 | pomar antigo")
    for L in (110, 120, 130, 140, 150, 160):
        print("   %5d | %6.1f%% | %5.1f%% | %6.1f%%"
              % (L, 100 * (lum21[mw] > L).mean(), 100 * (lum21[z0] > L).mean(),
                 100 * (lum21[velho] > L).mean()))
