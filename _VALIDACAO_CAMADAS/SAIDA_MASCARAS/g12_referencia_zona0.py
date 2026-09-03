# -*- coding: utf-8 -*-
"""G12 — `saudavel` por desenho espacial sistematico, e verificacao da `zona0`.

REFERENCIA
----------
A antiga `saudavel` eram tres manchas escolhidas por terem NDVI alto em
2026-07-27 — a ultima cena da serie que elas proprias calibram. Uma referencia
escolhida por parecer sa mede distancia ao MELHOR caso, nao distancia ao normal,
e desloca-se sozinha.

A nova e uma GRELHA REGULAR: celulas de 20 x 20 m colocadas de 60 em 60 m sobre
todo o `pomar_2012`, aceites apenas se o quadrado inteiro cair dentro do pomar e
a >= 30 m de qualquer bordo. Nenhuma celula e escolhida, aceite ou rejeitada por
causa de nenhum valor radiometrico, de nenhuma data. O unico criterio e a
posicao.

Restringe-se a `pomar_2012` (pergola instalada antes de 2017) para a referencia
nao apanhar plantacao nova, que sobe por crescimento e nao por sanidade — isso e
um criterio de idade da infraestrutura, nao de vigor.

LIMITE QUE E PRECISO DECLARAR: uma referencia interna mede contraste ESPACIAL.
Se o pomar inteiro descer, ela desce com ele e o defice nao muda. Nenhuma
referencia tirada de dentro do pomar pode detectar declinio uniforme. Para isso
seria preciso uma referencia externa — e foi exactamente uma referencia externa
mal georreferenciada (o bloco «B1») que originou esta cadeia de validacao.
Reporta-se por isso tambem a distribuicao do pomar inteiro, que e a alternativa.

ZONA 0
------
Unica mascara geografica do ficheiro antigo. Verifica-se: esta dentro do novo
`pomar`? corresponde a uma sub-parcela real na ortofoto?
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib.path import Path as MP

AOI = (529950, 4654600, 531950, 4655600)
SAI = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_MASCARAS"
GAN = r"C:\Users\Jackster2\Downloads\ganfei_s2"
PASSO, LADO, RECUO = 3, 1, 2          # celula de 10 m de 30 em 30 m, a >=20 m do bordo


def raster(poly):
    yy, xx = np.mgrid[0:100, 0:200]
    return MP(poly).contains_points(np.vstack((xx.ravel(), yy.ravel())).T).reshape(100, 200)


if __name__ == "__main__":
    pomar = np.load(os.path.join(SAI, "pomar.npy"))
    p2012 = np.load(os.path.join(SAI, "pomar_2012.npy"))
    ant = json.load(open(os.path.join(GAN, "sentinel", "masks.json")))

    # --- referencia sistematica ---------------------------------------------
    interior = ndimage.binary_erosion(p2012, np.ones((2 * RECUO + 1, 2 * RECUO + 1)))
    ref = np.zeros_like(pomar)
    blocos = 0
    for i in range(0, 100 - LADO + 1, PASSO):
        for j in range(0, 200 - LADO + 1, PASSO):
            if interior[i:i + LADO, j:j + LADO].all():
                ref[i:i + LADO, j:j + LADO] = True
                blocos += 1
    print("referencia sistematica: %d blocos de %dx%d m, %d celulas = %.2f ha"
          % (blocos, LADO * 10, LADO * 10, ref.sum(), ref.sum() / 100))
    ys, xs = np.where(ref)
    print("  cobre E %.0f-%.0f  N %.0f-%.0f (o eixo todo)"
          % (AOI[0] + 10 * xs.min(), AOI[0] + 10 * xs.max() + 10,
             AOI[3] - 10 * ys.max() - 10, AOI[3] - 10 * ys.min()))

    # --- zona0 ---------------------------------------------------------------
    z0_ant = raster(ant["zona0"])
    z0 = z0_ant & pomar
    print("\nzona0 antiga: %d celulas = %.2f ha" % (z0_ant.sum(), z0_ant.sum() / 100))
    print("  dentro do novo `pomar`: %d celulas (%.1f %%)"
          % (z0.sum(), 100 * z0.sum() / z0_ant.sum()))
    ys, xs = np.where(z0_ant)
    print("  extensao E %.0f-%.0f  N %.0f-%.0f"
          % (AOI[0] + 10 * xs.min(), AOI[0] + 10 * xs.max() + 10,
             AOI[3] - 10 * ys.max() - 10, AOI[3] - 10 * ys.min()))
    print("  intersecta a referencia? %s" % bool((z0 & ref).any()))
    mw_ant = raster(ant["manchaW"])
    print("  manchaW antiga dentro do novo pomar: %.1f %%"
          % (100 * (mw_ant & pomar).sum() / mw_ant.sum()))

    np.save(os.path.join(SAI, "saudavel.npy"), ref)
    np.save(os.path.join(SAI, "zona0.npy"), z0)

    # --- figura --------------------------------------------------------------
    orto = np.load(os.path.join(SAI, "orto_2021_50cm.npy"))
    rgb = np.clip(np.transpose(orto[:3], (1, 2, 0)) / 255.0, 0, 1)
    ext = [AOI[0], AOI[2], AOI[1], AOI[3]]
    fig, ax = plt.subplots(figsize=(22, 11), dpi=115)
    ax.imshow(rgb, extent=ext, origin="upper")
    ax.contour(pomar.astype(float), levels=[0.5], colors="yellow", linewidths=1.8,
               extent=ext, origin="upper")
    novo = np.load(os.path.join(SAI, "pomar_novo.npy"))
    ax.contourf(novo.astype(float), levels=[0.5, 1.5], colors=["#ff00ff"], alpha=0.35,
                extent=ext, origin="upper")
    ax.contourf(ref.astype(float), levels=[0.5, 1.5], colors=["#00ffff"], alpha=0.75,
                extent=ext, origin="upper")
    ax.contour(z0.astype(float), levels=[0.5], colors="#ff3300", linewidths=2.2,
               extent=ext, origin="upper")
    ax.set_title("amarelo `pomar` %.2f ha | magenta `pomar_novo` (estrutura so em 2025) "
                 "%.2f ha | ciano referencia sistematica %.2f ha | vermelho `zona0` %.2f ha"
                 % (pomar.sum() / 100, novo.sum() / 100, ref.sum() / 100, z0.sum() / 100),
                 fontsize=12)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v12_mascaras_novas.png"), dpi=115)
    plt.close(fig)
    print("-> v12_mascaras_novas.png")

    # zoom na zona0
    e0, e1, n0, n1 = 530850, 531200, 4654980, 4655230
    c0, c1 = int((e0 - AOI[0]) / 0.5), int((e1 - AOI[0]) / 0.5)
    l0, l1 = int((AOI[3] - n1) / 0.5), int((AOI[3] - n0) / 0.5)
    z50 = np.kron(z0.astype(float), np.ones((20, 20)))
    fig, axes = plt.subplots(1, 3, figsize=(19, 6.2), dpi=125)
    for ax, ano in zip(axes, ("2012", "2021", "2025")):
        o = np.load(os.path.join(SAI, "orto_%s_50cm.npy" % ano))
        ax.imshow(np.transpose(o[:3, l0:l1, c0:c1], (1, 2, 0)) / 255.0,
                  extent=[e0, e1, n0, n1], origin="upper")
        ax.contour(z50[l0:l1, c0:c1], levels=[0.5], colors="#ff3300", linewidths=2.0,
                   extent=[e0, e1, n0, n1], origin="upper")
        ax.set_title(ano, fontsize=11); ax.tick_params(labelsize=7)
    fig.suptitle("`zona0` sobre a ortofoto — verificacao geografica", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(SAI, "v12_zona0.png"), dpi=125)
    plt.close(fig)
    print("-> v12_zona0.png")
