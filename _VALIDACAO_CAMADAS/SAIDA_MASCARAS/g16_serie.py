# -*- coding: utf-8 -*-
"""G16 — reexecucao da serie NDVI com as mascaras geograficas, e o desvio.

Corre tudo duas vezes: com as mascaras antigas (`sentinel/masks.json`) e com as
novas. Assim o desvio e medido quantidade a quantidade e no mesmo codigo — a
diferenca vem so das mascaras.

Regra de defice mantida igual a da analise suspensa, para o desvio ser
atribuivel as mascaras e nao a uma mudanca de regra:
    celula em defice numa data  <=>  NDVI < referencia_dessa_data - 0,05

As manchas deixam de ser mascara. Em cada data extraem-se as componentes ligadas
de celulas em defice com >= 0,20 ha, e reporta-se a maior e o total. Uma mancha
passa a ser um resultado do mapa, e nao a coisa que define o mapa.
"""
import os
import json
import glob
import numpy as np
import rasterio
from scipy import ndimage, stats
from matplotlib.path import Path as MP

SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
LIM_DEF = 0.05
PLENA = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


def carrega_cenas():
    fich = sorted(glob.glob(os.path.join(GAN, "sentinel", "*.tif")))
    datas, arrs = [], []
    for f in fich:
        d = os.path.basename(f)[:10]
        with rasterio.open(f) as ds:
            arrs.append(ds.read(1).astype("float64"))
        datas.append(d)
    return datas, np.stack(arrs)


def manchas(defmap, minimo=20):
    lab, n = ndimage.label(defmap, structure=np.ones((3, 3)))
    if not n:
        return 0, 0.0, 0.0
    tam = ndimage.sum(defmap, lab, range(1, n + 1))
    tam = tam[tam >= minimo]
    if not len(tam):
        return 0, 0.0, 0.0
    return len(tam), tam.max() / 100, tam.sum() / 100


def corre(nome, pomar, ref, z0, datas, nd):
    print("\n" + "=" * 78)
    print("SERIE COM MASCARAS: %s" % nome)
    print("  pomar %.2f ha (%d celulas) | referencia %.2f ha (%d) | zona0 %.2f ha (%d)"
          % (pomar.sum() / 100, pomar.sum(), ref.sum() / 100, ref.sum(),
             z0.sum() / 100, z0.sum()))
    print("=" * 78)
    print("data        refNDVI    ep   pomarNDVI  zona0NDVI  defZ0   %defice  "
          "areaDef  maiorMancha  nManchas")
    r = {"nome": nome, "datas": datas, "ref": [], "ref_ep": [], "pomar": [],
         "zona0": [], "def_z0": [], "frac_def": [], "area_def": [],
         "maior_mancha": [], "n_manchas": [], "pomar_mediana": []}
    for k, d in enumerate(datas):
        a = nd[k]
        vr = a[ref]
        m_ref = float(np.nanmean(vr))
        ep = float(np.nanstd(vr) / np.sqrt(np.isfinite(vr).sum()))
        m_pom = float(np.nanmean(a[pomar]))
        med_pom = float(np.nanmedian(a[pomar]))
        m_z0 = float(np.nanmean(a[z0]))
        dmap = pomar & (a < m_ref - LIM_DEF)
        nman, maior, tot = manchas(dmap)
        for key, val in (("ref", m_ref), ("ref_ep", ep), ("pomar", m_pom),
                         ("zona0", m_z0), ("def_z0", m_ref - m_z0),
                         ("frac_def", 100 * dmap.sum() / pomar.sum()),
                         ("area_def", dmap.sum() / 100), ("maior_mancha", maior),
                         ("n_manchas", nman), ("pomar_mediana", med_pom)):
            r[key].append(val)
        print("%s  %6.4f  %.4f  %7.4f   %7.4f   %+6.4f  %6.2f%%  %6.2f ha  "
              "%6.2f ha    %2d"
              % (d, m_ref, ep, m_pom, m_z0, m_ref - m_z0,
                 100 * dmap.sum() / pomar.sum(), dmap.sum() / 100, maior, nman))

    ip = [i for i, d in enumerate(datas) if d in PLENA]
    x = np.array([int(datas[i][:4]) + (int(datas[i][5:7]) - 1) / 12 for i in ip])
    for nm in ("ref", "zona0", "pomar", "def_z0"):
        y = np.array(r[nm])[ip]
        s = stats.linregress(x, y)
        print("  declive %-8s %+.5f/ano  p=%.4f  r2=%.3f"
              % (nm, s.slope, s.pvalue, s.rvalue ** 2))
        r["declive_" + nm] = [s.slope, s.pvalue, s.rvalue ** 2]
    return r


if __name__ == "__main__":
    datas, nd = carrega_cenas()
    print("cenas: %d | plena estacao: %d" % (len(datas), len(PLENA)))

    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))
    p_ant = raster(ant["pomar"])
    ref_ant = raster(ant["saudavel"]) | raster(ant["saudavel_2"]) | raster(ant["saudavel_3"])
    z0_ant = raster(ant["zona0"])
    mw_ant = raster(ant["manchaW"])

    p_new = np.load(os.path.join(SAI, "pomar.npy"))
    ref_new = np.load(os.path.join(SAI, "saudavel.npy"))
    z0_new = np.load(os.path.join(SAI, "zona0.npy"))

    ra = corre("ANTIGAS (semeadas por NDVI de 2026-07-27)", p_ant, ref_ant, z0_ant, datas, nd)
    rn = corre("NOVAS (geograficas, ortofoto DGT)", p_new, ref_new, z0_new, datas, nd)

    # serie da manchaW antiga, para registo (nao ha equivalente novo por desenho)
    print("\nmanchaW antiga (mascara retirada nas novas) — NDVI medio por data:")
    for k, d in enumerate(datas):
        print("  %s  %.4f" % (d, float(np.nanmean(nd[k][mw_ant]))))

    json.dump({"antigas": ra, "novas": rn},
              open(os.path.join(SAI, "serie.json"), "w"), indent=1)

    print("\n" + "=" * 78)
    print("DESVIO, quantidade a quantidade")
    print("=" * 78)
    def linha(nome, a, b, fmt="%.4f", un=""):
        print("  %-42s %10s %10s %10s"
              % (nome, fmt % a, fmt % b, ("%+.4f" % (b - a)) if isinstance(a, float) else ""))
    print("  %-42s %10s %10s %10s" % ("quantidade", "antigo", "novo", "desvio"))
    linha("pomar (ha)", p_ant.sum() / 100, p_new.sum() / 100, "%.2f")
    linha("referencia (ha)", ref_ant.sum() / 100, ref_new.sum() / 100, "%.2f")
    linha("zona0 (ha)", z0_ant.sum() / 100, z0_new.sum() / 100, "%.2f")
    for nm, rot in (("ref", "NDVI referencia"), ("zona0", "NDVI zona0"),
                    ("pomar", "NDVI pomar"), ("frac_def", "%% do pomar em defice"),
                    ("area_def", "area em defice (ha)"),
                    ("maior_mancha", "maior mancha (ha)")):
        for k, d in ((0, datas[0]), (len(datas) - 1, datas[-1])):
            linha("%s, %s" % (rot, d), ra[nm][k], rn[nm][k],
                  "%.4f" if nm.startswith(("ref", "zona", "pomar")) else "%.2f")
    for nm in ("ref", "zona0", "pomar", "def_z0"):
        linha("declive %s (/ano, 9 cenas)" % nm, ra["declive_" + nm][0],
              rn["declive_" + nm][0], "%.5f")
        linha("   p do declive %s" % nm, ra["declive_" + nm][1],
              rn["declive_" + nm][1], "%.4f")
