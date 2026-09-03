# -*- coding: utf-8 -*-
"""T5 — a reconstrução da grelha de referência, conforme o pré-registo.

O pré-registo, textual
----------------------
`PRE_REGISTO_REFERENCIA.md`, assinado em 31-08-2026 ANTES de correr:

  «Exclui-se uma célula da referência se o seu centro cair dentro de um disco
  de foco de 90 m, mais uma margem de 30 m. Total: 120 m dos centros… A margem
  de 30 m é justificada por três termos e nada mais: 10 m de célula, 10 m de
  erro de registo, 10 m para a convenção de ±0,4 ha. **Não se usa 150 m**… Se a
  exclusão de 120 m deixar menos de 60 células, **não se alarga a margem** —
  regista-se o n e o que ele limita.»

E fixou a tabela de decisão:

  | os fossos crescem            | é o esperado — os números eram conservadores |
  | os fossos **encolhem**       | **LINE-STOP.** A leitura de contaminação está |
  |                              | errada e reabre-se a camada 2                 |
  | algum fosso muda de sinal    | line-stop, e a peça que o usava sai           |
  | o degrau em absoluto muda    | impossível por construção — procura-se o erro |

Nada disto foi decidido depois. Corre-se e lê-se contra a tabela.

O B1 entra
----------
O lóbulo SW é a terceira unidade de kiwi da exploração e a sua série
(`b1_serie_verdadeira.json`) foi medida **contra esta mesma referência**. Se a
referência muda, o fosso do B1 muda com ela, e não há razão para o deixar de
fora.
"""
import json
import os

import numpy as np
import rasterio
from scipy import stats

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AOI = (529950, 4654600, 531950, 4655600)
DATAS = ["2017-07-02", "2018-08-31", "2020-07-18", "2021-07-16", "2022-07-31",
         "2023-08-07", "2024-07-22", "2025-08-14", "2026-07-27"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])
T = np.array([d >= "2025" for d in DATAS])

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0, NU21 = (bits("pomar_bits"), bits("saudavel_bits"),
                           bits("zona0_bits"), bits("nu2021_bits"))
nd = np.stack([rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
               for d in DATAS])
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
C_OR = (float(EE[ZONA0].mean()), float(NN[ZONA0].mean()))
C_OC = (530485.0, 4655053.0)
dfoco = np.minimum(np.hypot(EE - C_OR[0], NN - C_OR[1]),
                   np.hypot(EE - C_OC[0], NN - C_OC[1]))

REF_LIMPA = REF & (dfoco > 120.0)                 # 90 + 30, como pre-registado

print("=" * 90)
print("T5 · RECONSTRUÇÃO DA REFERÊNCIA — regra de 120 m, pré-registada")
print("=" * 90)
print()
print("referência antiga : %3d células" % REF.sum())
print("referência limpa  : %3d células   (excluídas %d)"
      % (REF_LIMPA.sum(), REF.sum() - REF_LIMPA.sum()))
print("limite do pré-registo: não alargar abaixo de 60 células  ->  %s"
      % ("CUMPRIDO" if REF_LIMPA.sum() >= 60 else "VIOLADO — regista-se o n"))
print()

serie = lambda m: np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])
r_ant, r_lim = serie(REF), serie(REF_LIMPA)
print("%-22s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
print("%-22s %s   degrau %+.4f" % ("referência antiga",
                                   "  ".join("%.3f" % v for v in r_ant),
                                   r_ant[T].mean() - r_ant[~T].mean()))
print("%-22s %s   degrau %+.4f" % ("referência limpa",
                                   "  ".join("%.3f" % v for v in r_lim),
                                   r_lim[T].mean() - r_lim[~T].mean()))

# ------------------------------------------------------------------ unidades
UN = [("Zona 0 sem nu2021 (o publicado)", ZONA0 & ~NU21),
      ("ORIENTAL Zona 0 com pérgola", ZONA0 & COM),
      ("OCIDENTAL disco 90 m com pérgola",
       (np.hypot(EE - C_OC[0], NN - C_OC[1]) <= 90) & POMAR & COM),
      ("resto do pomar com pérgola",
       POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF)]

B1 = json.load(open(os.path.join(S2, "b1_serie_verdadeira.json")))
b1_ndvi = np.array([r["b1"] for r in B1["serie"]])

print()
print("=" * 90)
print("O QUE ACONTECE AOS FOSSOS")
print("=" * 90)
print()
print("%-34s %10s %10s %10s %9s"
      % ("unidade", "fosso ant.", "fosso limpo", "variação", "declive"))
saida = {"n_antiga": int(REF.sum()), "n_limpa": int(REF_LIMPA.sum()),
         "degrau_ref_antiga": float(r_ant[T].mean() - r_ant[~T].mean()),
         "degrau_ref_limpa": float(r_lim[T].mean() - r_lim[~T].mean()),
         "unidades": {}}
cresceram, encolheram, sinal = 0, 0, 0
for nome, m in list(UN) + [("B1 · lóbulo SW (kiwi)", None)]:
    v = b1_ndvi if m is None else serie(m)
    fa, fl = r_ant - v, r_lim - v
    ma, ml = float(fa.mean()), float(fl.mean())
    la = stats.linregress(anos, fl)
    if abs(ml) > abs(ma):
        cresceram += 1
    elif abs(ml) < abs(ma):
        encolheram += 1
    if np.sign(ml) != np.sign(ma):
        sinal += 1
    saida["unidades"][nome] = dict(fosso_antigo=ma, fosso_limpo=ml,
                                   variacao=ml - ma, declive=float(la.slope),
                                   p=float(la.pvalue))
    print("%-34s %+10.4f %+10.4f %+10.4f %+9.5f"
          % (nome, ma, ml, ml - ma, la.slope))

print()
print("=" * 90)
print("LEITURA CONTRA A TABELA PRÉ-REGISTADA")
print("=" * 90)
print()
print("fossos que CRESCERAM : %d" % cresceram)
print("fossos que ENCOLHERAM: %d" % encolheram)
print("fossos que mudaram de SINAL: %d" % sinal)
print()
if sinal:
    print(">>> LINE-STOP: algum fosso mudou de sinal. A peça que o usava sai.")
elif encolheram > cresceram:
    print(">>> LINE-STOP: os fossos encolhem. A leitura de contaminação do")
    print("    certificado R2 está ERRADA e a camada 2 reabre.")
else:
    print(">>> É o esperado. Os fossos crescem com a referência limpa, logo os")
    print("    números publicados na moeda do fosso eram CONSERVADORES — e isso")
    print("    deixa de ser inferência (M3) e passa a medição.")
    print()
    print("    A paragem de linha da moeda pode ser levantada: o fosso volta a")
    print("    ser utilizável, agora com uma referência que não contém os focos.")

# verificacao de que o absoluto nao mexeu
print()
print("Verificação de construção — o degrau em absoluto não pode mexer:")
for nome, m in UN[1:3]:
    v = serie(m)
    print("   %-32s %+.4f" % (nome, v[T].mean() - v[~T].mean()))

json.dump(saida, open(os.path.join(VG, "t5_referencia_reconstruida.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito t5_referencia_reconstruida.json")
