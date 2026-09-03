# -*- coding: utf-8 -*-
"""P3 — o foco oriental em 2010 e 2012: replantado, ou nunca plantado?

A pergunta
----------
O P1 estabeleceu que **em 2021 o foco oriental não tinha assinatura de pérgola,
incluindo a metade que o LiDAR de 2025 diz ter** — 14 % e 6 % do caminho entre
chão lavrado e referência, contra 80 % no resto do pomar. Logo a estrutura que
lá está apareceu depois de 2021.

Falta separar duas hipóteses que isso não distingue:

  A · **REPLANTADO** — havia pomar antes, foi arrancado, e replantou-se.
      Então em 2010 e/ou 2012 a assinatura de pérgola tem de lá estar.
  B · **NUNCA PLANTADO** até depois de 2021 — chão agrícola que só recebeu
      pomar recentemente. Então em 2010 e 2012 também não há assinatura.

São hipóteses com biologias e responsabilidades diferentes.

O que este ficheiro faz, e o que deliberadamente NÃO faz
-------------------------------------------------------
**Não recomputa nada.** A C2 já correu a prominência sobre as ortofotos de 2010,
2012 e 2021 e guardou os mapas por célula na grelha da análise —
`c2_12_prom_2010.npy`, `_2012`, `_2021`, com 3 031 células finitas cada, que é o
polígono do pomar inteiro. Este ficheiro **lê esses mapas e aplica-lhes as
máscaras do LiDAR**. É a mesma medição, noutras unidades.

E usa o mapa de 2021 deles como **verificação do meu próprio P1**: se os meus
números de 2021, calculados independentemente da ortofoto, baterem com os que
saem do mapa certificado, a minha implementação está boa.
"""
import json
import os

import numpy as np

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
ZONA0, NU21 = bits("zona0_bits"), bits("nu2021_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
FIN = np.isfinite(h)
COM, SEM = FIN & (h >= 0.5), FIN & (h < 0.5)

UN = [("ORI-COM  oriental, com pérgola em 2025", ZONA0 & COM),
      ("ORI-SEM  oriental, sem pérgola em 2025", ZONA0 & SEM),
      ("REF      referência sistemática", REF),
      ("RESTO    resto do pomar c/ pérgola", POMAR & COM & ~ZONA0 & ~REF),
      ("NU21     chão lavrado de 2021", NU21 & POMAR)]

EPOCAS = [("2010", "c2_12_prom_2010.npy"),
          ("2012", "c2_12_prom_2012.npy"),
          ("2021", "c2_12_prom_2021.npy")]

print("=" * 94)
print("P3 · PROMINÊNCIA DE PÉRGOLA EM 2010 E 2012 — mapas certificados da C2")
print("=" * 94)
print()

saida = {"fonte": "c2_12_prom_*.npy — mapas por célula da C2, sem recomputação",
         "epocas": {}}
for epoca, fich in EPOCAS:
    P = np.load(os.path.join(C2, fich))
    print("%s   (%d células finitas no mapa)" % (epoca, int(np.isfinite(P).sum())))
    print("%-40s %5s %10s %10s %10s"
          % ("", "n", "mediana", "p25", "p75"))
    linha = {}
    for nome, m in UN:
        v = P[m & np.isfinite(P)]
        if v.size < 5:
            print("%-40s %5d   poucas" % (nome, v.size))
            continue
        linha[nome] = dict(n=int(v.size), mediana=float(np.median(v)),
                           p25=float(np.percentile(v, 25)),
                           p75=float(np.percentile(v, 75)))
        print("%-40s %5d %10.4f %10.4f %10.4f"
              % (nome, v.size, np.median(v), np.percentile(v, 25),
                 np.percentile(v, 75)))
    # ancoras e posicao
    R = linha["REF      referência sistemática"]
    N = linha["NU21     chão lavrado de 2021"]
    sep = R["p25"] > N["p75"]
    print("  âncoras: REF %.4f  ·  NU21 %.4f  ·  IQR disjuntos: %s  ->  %s"
          % (R["mediana"], N["mediana"], sep,
             "DISCRIMINA" if sep else "não discrimina"))
    if sep:
        span = R["mediana"] - N["mediana"]
        for nome in linha:
            linha[nome]["posicao_pct"] = float(
                100 * (linha[nome]["mediana"] - N["mediana"]) / span)
        print("  posição entre chão lavrado (0 %) e referência (100 %):")
        for nome in linha:
            print("    %-38s %6.0f %%" % (nome[:38], linha[nome]["posicao_pct"]))
    saida["epocas"][epoca] = dict(discrimina=bool(sep), unidades=linha)
    print()

print("=" * 94)
print("VERIFICAÇÃO DA MINHA IMPLEMENTAÇÃO (P1) CONTRA O MAPA CERTIFICADO")
print("=" * 94)
print()
try:
    meu = json.load(open(os.path.join(VG, "p1_pergola_oriental_2025.json"),
                         encoding="cp1252"))["epocas"]["2021"]
    print("%-40s %12s %12s %10s" % ("unidade", "P1 (meu)", "C2 (mapa)", "difer."))
    for nome in [u[0] for u in UN]:
        a = [meu[k] for k in meu if k.startswith(nome.split()[0])]
        b = saida["epocas"]["2021"]["unidades"].get(nome)
        if a and b:
            d = a[0]["mediana"] - b["mediana"]
            print("%-40s %12.4f %12.4f %+10.4f" % (nome, a[0]["mediana"],
                                                   b["mediana"], d))
except Exception as e:
    print("não foi possível comparar: %s" % e)

print()
print("=" * 94)
print("VEREDICTO — replantado ou nunca plantado?")
print("=" * 94)
print()
for epoca in ("2010", "2012"):
    e = saida["epocas"][epoca]
    if not e["discrimina"]:
        print("%s: o instrumento não discrimina nesta imagem. Não decide." % epoca)
        continue
    oc = e["unidades"]["ORI-COM  oriental, com pérgola em 2025"]["posicao_pct"]
    os_ = e["unidades"]["ORI-SEM  oriental, sem pérgola em 2025"]["posicao_pct"]
    rt = e["unidades"]["RESTO    resto do pomar c/ pérgola"]["posicao_pct"]
    print("%s: ORI-COM %.0f %%   ORI-SEM %.0f %%   (resto do pomar %.0f %%)"
          % (epoca, oc, os_, rt))

json.dump(saida, open(os.path.join(VG, "p3_pergola_2010_2012.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito p3_pergola_2010_2012.json")
