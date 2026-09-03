# -*- coding: utf-8 -*-
"""T1 — o rácio degrau/recta é um achado ou uma escolha?

A acusação, textual
-------------------
`CAMADA_2_ADVERSARIO_R2.md`, R2:

  «`TARDIO = d >= "2025"` é uma constante escrita à mão. O ponto de quebra não
  foi ajustado: foi escolhido depois de se ver onde a série cai. Um modelo de
  degrau com ponto de quebra livre tem TRÊS parâmetros.»

O teste
-------
Três coisas, e a terceira é a que decide:

1. **O perfil completo.** Razão SQR(recta)/SQR(degrau) para TODOS os pontos de
   quebra possíveis da série de nove cenas. Se 2024|2025 for o máximo — e vai
   ser — o número publicado é o máximo de uma família, não um valor.

2. **AIC com o parâmetro escondido contabilizado.** Recta = 2 parâmetros.
   Degrau com quebra escolhida = **3**. AIC de segunda ordem (AICc), porque
   n = 9 é pequeno e o AIC simples é enviesado a essa dimensão.

3. **A distribuição nula do MÁXIMO.** Permuta-se a ordem das nove cenas 20 000
   vezes; em cada permutação procura-se o melhor ponto de quebra e guarda-se a
   razão máxima. Assim a estatística nula tem a mesma liberdade de escolha que
   a observada. **É esta que responde à acusação**: pergunta com que frequência
   uma série sem estrutura temporal produz, ao procurar o melhor corte, uma
   razão tão boa como a nossa.

Permutar a ordem destrói a estrutura temporal e mantém os valores — é o nulo
certo para «existe um corte no tempo».
"""
import itertools
import json
import os

import numpy as np
from scipy import stats

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
DR = json.load(open(os.path.join(VG, "degrau_vs_recta_pergola.json")))
DATAS = DR["datas"]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])
n = len(DATAS)
RNG = np.random.default_rng(20260831)
NPERM = 20000

# pontos de quebra interiores: pelo menos 2 cenas de cada lado
CORTES = list(range(2, n - 1))


def sqr_recta(x, v):
    lr = stats.linregress(x, v)
    return float(np.sum((v - (lr.intercept + lr.slope * x)) ** 2))


def sqr_degrau(v, k):
    """k = indice da primeira cena do segundo patamar."""
    a, b = v[:k].mean(), v[k:].mean()
    aj = np.concatenate([np.full(k, a), np.full(len(v) - k, b)])
    return float(np.sum((v - aj) ** 2))


def aicc(sqr, n_, p):
    if sqr <= 0:
        sqr = 1e-12
    a = n_ * np.log(sqr / n_) + 2 * p
    corr = (2 * p * (p + 1)) / (n_ - p - 1) if n_ - p - 1 > 0 else np.inf
    return float(a + corr)


SERIES = {k: DR["unidades"][k]["NIVEL ABSOLUTO"]["serie"] for k in DR["unidades"]}

# B1 — o lobulo sudoeste. E kiwi da mesma exploracao (G39: 12,64 ha declarados,
# todo do ENT 472062) e nao pode ficar de fora por ser inconveniente: e a
# terceira unidade de kiwi do caso, tem serie nas mesmas nove datas, e a sua
# forma e a de uma curva de recuperacao — que e exactamente o contra-exemplo
# que este teste precisa de ter dentro.
LO = json.load(open(os.path.join(VG, "lobulo_oeste_degrau.json")))
for k, v in LO["A"].items():
    if k.startswith("B1"):
        SERIES["B1 · lóbulo SW (kiwi, mesma exploração)"] = v["serie"]

UN = list(SERIES)
saida = {"cortes": [DATAS[k] for k in CORTES], "unidades": {}}

print("=" * 92)
print("T1 · PERFIL DE TODOS OS PONTOS DE QUEBRA")
print("=" * 92)
print()
print("%-36s %s" % ("", "  ".join("|%s" % DATAS[k][2:7] for k in CORTES)))
for nome in UN:
    v = np.array(SERIES[nome])
    sl = sqr_recta(anos, v)
    razoes = [sl / sqr_degrau(v, k) for k in CORTES]
    kbest = CORTES[int(np.argmax(razoes))]
    print("%-36s %s   melhor: |%s"
          % (nome, "  ".join("%6.2f" % r for r in razoes), DATAS[kbest][2:7]))
    saida["unidades"][nome] = dict(razoes=razoes, melhor=DATAS[kbest],
                                   sqr_recta=sl)

print()
print("=" * 92)
print("T1b · AICc COM O PARÂMETRO ESCONDIDO CONTABILIZADO")
print("=" * 92)
print()
print("%-36s %10s %10s %10s %s"
      % ("", "AICc recta", "AICc degr.", "ΔAICc", "vence"))
for nome in UN:
    v = np.array(SERIES[nome])
    ar = aicc(sqr_recta(anos, v), n, 2)
    k26 = DATAS.index("2025-08-14")
    ad = aicc(sqr_degrau(v, k26), n, 3)          # 3: duas medias + a quebra
    d = ad - ar
    saida["unidades"][nome].update(aicc_recta=ar, aicc_degrau=ad, delta=d)
    print("%-36s %10.2f %10.2f %+10.2f %s"
          % (nome, ar, ad, d,
             "DEGRAU" if d < -2 else ("recta" if d > 2 else "indistintos")))

print()
print("=" * 92)
print("T1c · NULO DO MÁXIMO — a estatística nula procura o corte, tal como nós")
print("=" * 92)
print()
print("%-36s %10s %12s %10s" % ("", "razão obs.", "máx. do nulo", "p"))
for nome in UN:
    v = np.array(SERIES[nome])
    obs = max(sqr_recta(anos, v) / sqr_degrau(v, k) for k in CORTES)
    cnt = 0
    maxs = []
    for _ in range(NPERM):
        w = RNG.permutation(v)
        r = max(sqr_recta(anos, w) / sqr_degrau(w, k) for k in CORTES)
        maxs.append(r)
        if r >= obs:
            cnt += 1
    p = (cnt + 1) / (NPERM + 1.0)
    maxs = np.array(maxs)
    saida["unidades"][nome].update(razao_max_obs=float(obs), p_max=float(p),
                                   nulo_p95=float(np.percentile(maxs, 95)))
    print("%-36s %10.2f %12.2f %10.4f%s"
          % (nome, obs, np.percentile(maxs, 95), p, "  *" if p < 0.05 else ""))

print()
print("=" * 92)
print("VEREDICTO SOBRE R2")
print("=" * 92)
print()
foco = [k for k in UN if "resto" not in k]
ctrl = [k for k in UN if "resto" in k]
print("Focos:")
for k in foco:
    u = saida["unidades"][k]
    print("  %-34s razão máx %5.2f  p do máximo %.4f  ΔAICc %+.2f"
          % (k, u["razao_max_obs"], u["p_max"], u["delta"]))
print("Controlo:")
for k in ctrl:
    u = saida["unidades"][k]
    print("  %-34s razão máx %5.2f  p do máximo %.4f  ΔAICc %+.2f"
          % (k, u["razao_max_obs"], u["p_max"], u["delta"]))

json.dump(saida, open(os.path.join(VG, "t1_ponto_de_quebra.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito t1_ponto_de_quebra.json")
