# -*- coding: utf-8 -*-
"""O teste que o adversário da C2 exigiu e que ninguém correu: fenologia POR UNIDADE.

A exigencia, textual
--------------------
`CAMADA_2_ADVERSARIO.md`, sobre a sonda A:

  «Um coeficiente medio aplicado a unidades com respostas de sinal contrario
  nao e uma calibracao. Repetir por unidade (referencia, dois focos, resto do
  pomar) e por limiar (0,05 a 0,30) diz se as 5,37 ha de defice grave da cena
  mais precoce da serie (DOY 183) sao em parte um efeito de dia-do-ano.»

E dá o motivo medido: entre DOY 168 e 226 de 2025 a referencia **desce** 0,0162
enquanto o foco ESTE **sobe** 0,050. Respostas de sinal contrario.

Porque isto me toca directamente
--------------------------------
O degrau que sustenta a apresentacao inteira compara duas cenas tardias com
sete anteriores, e os dois grupos **nao tem o mesmo dia-do-ano**:

  2017-24 : DOY 183 · 243 · 200 · 197 · 212 · 219 · 204   -> media 208,3
  2025-26 : DOY 226 · 208                                 -> media 217,0

Sao 8,7 dias de diferenca. Se a resposta ao DOY tiver o sinal que o adversario
mediu, ela empurra o degrau — e a direccao **nao e a mesma em todas as
unidades**, que e precisamente a objeccao dele.

Nunca foi corrido por unidade. Corre-se agora, com o unico par intra-anual que
o arquivo tem: 2025-06-17 (DOY 168) e 2025-08-14 (DOY 226), o MESMO ano, o
mesmo sensor, a mesma cadeia — logo a diferenca entre os dois e fenologia mais
tempo, nao calibracao.

O que este teste pode e nao pode fazer
--------------------------------------
PODE: dar o declive dNDVI/dia de cada unidade dentro de 2025, e com ele
corrigir o degrau para a diferenca de DOY entre os dois grupos.

NAO PODE: separar fenologia de declinio dentro de 2025, porque 2025 e um dos
anos do acontecimento. **Se a unidade estava a cair entre Junho e Agosto de
2025, o declive medido e fenologia MAIS queda**, e a correccao que dele sai e
por isso um LIMITE SUPERIOR do efeito fenologico. Diz-se, e usa-se nesse
sentido: se o degrau sobrevive a correccao maxima, sobrevive a qualquer.
"""
import json
import os

import numpy as np
import rasterio

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)

DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
DOY = {"2017-07-02": 183, "2018-08-31": 243, "2020-07-18": 200,
       "2021-07-16": 197, "2022-07-31": 212, "2023-08-07": 219,
       "2024-07-22": 204, "2025-08-14": 226, "2026-07-27": 208}
PAR = ("2025-06-17", "2025-08-14")          # DOY 168 e 226, o mesmo ano
T = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
C_OC, C_OR = (530485.0, 4655053.0), (530999.0, 4655102.0)
dsc = lambda c, r=90.: (((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r * r) & POMAR

UN = [("referência sistemática", REF),
      ("foco OCIDENTAL · disco 90 m c/ pérgola", dsc(C_OC) & COM),
      ("foco ORIENTAL · Zona 0 c/ pérgola", ZONA0 & COM),
      ("resto do pomar · CONTROLO", POMAR & COM & ~dsc(C_OC, 120)
       & ~dsc(C_OR, 120) & ~ZONA0 & ~REF)]

ler = lambda d: rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
nd = {d: ler(d) for d in DATAS}
p0, p1 = ler(PAR[0]), ler(PAR[1])
ddoy = DOY["2025-08-14"] - 168

print("=" * 88)
print("SONDA FENOLÓGICA POR UNIDADE — %s (DOY 168) contra %s (DOY 226), o mesmo ano"
      % PAR)
print("=" * 88)
print()
print("%-40s %9s %9s %10s %12s"
      % ("", "DOY 168", "DOY 226", "dif 58 dias", "dNDVI/dia"))
coef = {}
for nome, m in UN:
    a, b = float(np.nanmean(p0[m])), float(np.nanmean(p1[m]))
    coef[nome] = (b - a) / ddoy
    print("%-40s %9.4f %9.4f %+10.4f %+12.6f" % (nome, a, b, b - a, coef[nome]))

print()
print("O adversário mediu, na área agregada em défice: referência −0,0162 e")
print("foco ESTE +0,050 na mesma janela. Sinais contrários — e é por isso que")
print("um coeficiente médio não serve.")

print()
print("=" * 88)
print("O QUE ISTO FAZ AO DEGRAU")
print("=" * 88)
print()
doy = np.array([DOY[d] for d in DATAS], float)
d_cedo, d_tarde = doy[~T].mean(), doy[T].mean()
print("DOY médio 2017-24 = %.1f   ·   2025-26 = %.1f   ·   diferença = %+.1f dias"
      % (d_cedo, d_tarde, d_tarde - d_cedo))
print()
print("%-40s %10s %12s %10s"
      % ("", "degrau", "correcção", "corrigido"))
saida = {"par": list(PAR), "d_doy": ddoy, "doy_cedo": d_cedo,
         "doy_tarde": d_tarde, "unidades": {}}
for nome, m in UN:
    v = np.array([float(np.nanmean(nd[d][m])) for d in DATAS])
    deg = float(v[T].mean() - v[~T].mean())
    corr = coef[nome] * (d_tarde - d_cedo)
    saida["unidades"][nome] = dict(degrau=deg, coef_dia=coef[nome],
                                   correccao=float(corr),
                                   corrigido=float(deg - corr))
    print("%-40s %+10.4f %+12.4f %+10.4f" % (nome, deg, corr, deg - corr))

print()
o = saida["unidades"]["foco ORIENTAL · Zona 0 c/ pérgola"]
w = saida["unidades"]["foco OCIDENTAL · disco 90 m c/ pérgola"]
c = saida["unidades"]["resto do pomar · CONTROLO"]
print("Rácio foco/controlo antes da correcção : %.1f× e %.1f×"
      % (o["degrau"] / c["degrau"], w["degrau"] / c["degrau"]))
if abs(c["corrigido"]) > 1e-6:
    print("Rácio foco/controlo depois            : %.1f× e %.1f×"
          % (o["corrigido"] / c["corrigido"], w["corrigido"] / c["corrigido"]))

print()
print("LEMBRETE que vai com o número: 2025 é um ano do acontecimento, logo o")
print("declive medido em 2025 é fenologia MAIS queda. A correcção é por isso um")
print("LIMITE SUPERIOR do efeito fenológico — se o degrau sobrevive a ela,")
print("sobrevive a qualquer correcção menor.")

json.dump(saida, open(os.path.join(VG, "fenologia_por_unidade.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito fenologia_por_unidade.json")
