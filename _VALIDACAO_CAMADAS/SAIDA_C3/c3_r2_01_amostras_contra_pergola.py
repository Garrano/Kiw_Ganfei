# -*- coding: utf-8 -*-
"""C3 · re-execução R2 · tarefa 1 — as amostras contra a partição do LiDAR.

A pergunta, textual
-------------------
`CAMADA_3_PROMPT_R2.md`, tarefa 1:

  «Qualquer amostra, ensaio ou unidade tua que se localize "no foco ESTE
  plantado" pode estar em chão. Reverifica a posição de cada uma contra a
  partição nova. **Pergunta: alguma amostra do lado oriental caiu em célula sem
  pérgola?** Se caiu, o que ela mede não é raiz de videira.»

O que a C3 tinha
----------------
Quatro unidades com posição — **B3, B4, V7, Erica Novo** — obtidas por Voronoi
sobre `valvulas_por_area.json`, que a R2 G35 nomeou como a tabela boa. É nelas
que assenta o único organismo localizável do caso: *Meloidogyne hapla*,
positivo em 4/4.

Método
------
1. Reproduz-se a partição de Voronoi da C3 a partir do mesmo ficheiro.
2. **Verifica-se contra as contagens que a C3 publicou** (992, 417, 325, 535
   células). Se não baterem, o resto não se corre — seria outra partição.
3. Cruza-se com a altura MDS−MDT do voo de 06-07-2025 (G38), que é o dado que a
   camada 2 passou para cima.

A ressalva que viaja com tudo isto, e é da camada 0
---------------------------------------------------
A adenda v1.1 mediu **465 m de amplitude entre quatro reconstruções do esquema
para a MESMA válvula**. A C3 usou uma delas e declarou as outras desactualizadas
— decisão dela, não certificada. **Tudo o que este ficheiro diz sobre posição
herda essa incerteza**, e ela é da ordem da própria distância entre focos. O que
se mede aqui é «na partição que a C3 usou», não «no terreno».
"""
import json
import os

import numpy as np

DL = r"C:\Users\Jackster2\Downloads"
S2 = os.path.join(DL, "ganfei_s2")
VG = os.path.join(DL, "_VALIDADE_GESTAO")
AQUI = os.path.dirname(os.path.abspath(__file__))
AOI = (529950, 4654600, 531950, 4655600)

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, ZONA0, NU21 = bits("pomar_bits"), bits("zona0_bits"), bits("nu2021_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
FIN = np.isfinite(h)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)

VALV = json.load(open(os.path.join(S2, "valvulas_por_area.json"), encoding="utf-8"))
GEO = json.load(open(os.path.join(AQUI, "c3_07_georreferenciacao.json"),
                     encoding="utf-8"))
BL = GEO["por_bloco"]

# --- posicoes das valvulas, tal como a C3 as leu -------------------------
pos = {}
for k, v in GEO["por_valvula"].items():
    pos[k] = (v["E_valvula"], v["N_valvula"])
ids = sorted(pos, key=lambda z: int(z))
PE = np.array([pos[k][0] for k in ids])
PN = np.array([pos[k][1] for k in ids])

# --- Voronoi sobre o poligono do pomar ----------------------------------
d2 = ((EE[..., None] - PE) ** 2 + (NN[..., None] - PN) ** 2)
qual = np.argmin(d2, axis=2)
val_de_cel = np.array(ids)[qual]

bloco_de_valv = {}
for b, u in BL.items():
    for k in u["valvulas"]:
        bloco_de_valv[k] = b

print("=" * 90)
print("C3 R2 · TAREFA 1 — AS UNIDADES COM POSIÇÃO CONTRA A PARTIÇÃO DO LiDAR")
print("=" * 90)
print()
print("VERIFICAÇÃO da reprodução da partição da C3")
print()
print("%-14s %10s %10s %s" % ("bloco", "C3 publica", "reproduzido", ""))
ok = True
MASC = {}
for b, u in BL.items():
    m = POMAR & np.isin(val_de_cel, [k for k in u["valvulas"]])
    MASC[b] = m
    bate = abs(int(m.sum()) - u["celulas"]) <= 2
    ok &= bate
    print("%-14s %10d %10d %s" % (b, u["celulas"], m.sum(),
                                  "ok" if bate else "DIVERGE"))

if not ok:
    print()
    print("A partição não se reproduz. Não se corre o resto — seria outra coisa.")
    raise SystemExit(1)

print()
print("=" * 90)
print("O CRUZAMENTO")
print("=" * 90)
print()
print("%-14s %7s %9s %10s %11s %11s"
      % ("unidade", "ha", "altura", "% < 0,5 m", "% > 1,5 m", "% nu2021"))
saida = {"nota_posicao": "posições de valvulas_por_area.json; amplitude entre "
                         "quatro reconstruções = 465 m (adenda v1.1)",
         "unidades": {}}
for b in ("B2", "B3", "Erica Novo", "B4"):
    m = MASC[b]
    k = m & FIN
    sem = float(100 * np.mean(h[k] < 0.5))
    alto = float(100 * np.mean(h[k] > 1.5))
    nu = float(100 * np.mean(NU21[m]))
    saida["unidades"][b] = dict(ha=m.sum() / 100.0,
                                altura_mediana=float(np.median(h[k])),
                                pct_sem_pergola=sem, pct_alto=alto,
                                pct_nu2021=nu, celulas=int(m.sum()))
    print("%-14s %7.2f %7.2f m %9.1f %% %10.1f %% %10.1f %%"
          % (b, m.sum() / 100.0, np.median(h[k]), sem, alto, nu))

print()
print("V7 — a válvula ensaiada isoladamente:")
m7 = POMAR & (val_de_cel == "7")
k7 = m7 & FIN
print("%-14s %7.2f %7.2f m %9.1f %% %10.1f %%"
      % ("V7", m7.sum() / 100.0, np.median(h[k7]),
         100 * np.mean(h[k7] < 0.5), 100 * np.mean(h[k7] > 1.5)))
saida["unidades"]["V7"] = dict(ha=m7.sum() / 100.0,
                               pct_sem_pergola=float(100 * np.mean(h[k7] < 0.5)),
                               celulas=int(m7.sum()))

print()
print("=" * 90)
print("RESPOSTA À TAREFA 1")
print("=" * 90)
print()
b3 = saida["unidades"]["B3"]
print("A única unidade oriental ensaiada é o **B3** (válvulas 12-15, 9,92 ha),")
print("a 67 m do centro do foco oriental.")
print()
print("  %.1f %% da sua área NÃO TEM PÉRGOLA no LiDAR de 06-07-2025." % b3["pct_sem_pergola"])
print("  %.1f %% está acima de 1,5 m." % b3["pct_alto"])
print("  altura mediana: %.2f m" % b3["altura_mediana"])
print()
print("Comparação com as outras três unidades ensaiadas:")
for b in ("B2", "Erica Novo", "B4"):
    print("  %-12s %5.1f %% sem pérgola" % (b, saida["unidades"][b]["pct_sem_pergola"]))

json.dump(saida, open(os.path.join(AQUI, "c3_r2_01_amostras.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito c3_r2_01_amostras.json")
