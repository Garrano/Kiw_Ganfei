# -*- coding: utf-8 -*-
"""O lóbulo oeste (B1) leva o teste do degrau. A corrida que pode desmentir a frase.

Porque esta corrida vem antes da P01
------------------------------------
A frase central da apresentacao e «um acontecimento, DOIS sitios». O B1 e um
bloco da mesma exploracao, com a mesma origem de agua e a mesma gestao, mas
**fisicamente separado — 526 m do corpo principal**. Nunca lhe correu o teste
do degrau, porque vive noutra AOI e ficou de fora da reexecucao geografica.

  Se o degrau de 2025-26 estiver la, sao TRES sitios e a frase esta errada.
  Se nao estiver, o B1 e o melhor controlo que este caso tem: mesma agua,
  mesma gestao, mesma origem de material — e sem acontecimento.

Nenhum dos dois desfechos e mau. O que seria mau era imprimir a palavra «dois»
sem ter corrido isto.

O B1 obriga a uma variante do teste, e a razao interessa
-------------------------------------------------------
Os focos e o controlo do corpo principal sao series PLANAS ate 2024. O B1 nao
e: sobe de 0,560 para 0,685 entre 2017 e 2024. **Um bloco em subida pode
absorver um degrau e continuar a subir**, e o teste de diferenca de medias nao
o veria.

Por isso corre-se o teste em duas versoes:

  A. DIFERENCA DE MEDIAS, como nas outras unidades — comparavel linha a linha.
  B. DESVIO A TENDENCIA PROPRIA: ajusta-se a recta so a 2017-2024, extrapola-se
     para 2025 e 2026, e mede-se quanto o observado fica ABAIXO do previsto.
     E este que responde a pergunta no B1.

A versao B corre em TODAS as unidades, nao so no B1 — uma variante que so se
aplicasse a unidade inconveniente seria escolha de teste.

Proveniencia da mascara do B1, e e boa
--------------------------------------
Os poligonos C1a e C1b foram delimitados na ortofoto por uma sessao de
controlo externo que **nunca olhou para NDVI nenhum**, antes de se saber que
eram o B1. E o oposto exacto do defeito que originou toda esta cadeia.

O QUE ESTA CORRIDA NAO PODE FAZER, e vai dito
---------------------------------------------
**Nao ha particao pergola/chao para o B1.** As 21 folhas de MDS e MDT
descarregadas cobrem a AOI do corpo principal, e o B1 fica fora dela. Logo o
B1 entra sem restricao de copado, ao contrario de todas as outras unidades da
apresentacao. Isso torna-o conservador para a leitura de controlo — se houvesse
chao la dentro, ele puxaria a serie para baixo, nao para cima.
"""
import json
import os

import numpy as np
from scipy import stats

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"

B = json.load(open(os.path.join(S2, "b1_serie_verdadeira.json")))
MV = json.load(open(os.path.join(VG, "multiverso_degrau.json")))
DR = json.load(open(os.path.join(VG, "degrau_vs_recta_pergola.json")))

DATAS = [r["data"] for r in B["serie"]]
anos = np.array([float(d[:4]) + (int(d[5:7]) - 1) / 12 for d in DATAS])
T = np.array([d >= "2025" for d in DATAS])

print("=" * 84)
print("O LÓBULO OESTE (B1) — %s ha, %s"
      % (B["_area_ha"], B["_mascara"]))
print("=" * 84)
print()
print("coordenadas do gestor: E%d N%d  ->  E%d N%d"
      % tuple(B["_b1_coordenadas"]["inicio"] + B["_b1_coordenadas"]["fim"]))
print()


def unidades():
    b1 = np.array([r["b1"] for r in B["serie"]])
    or_ = np.array([r["degrau"] for r in MV["unidades"]
                    if r["foco"] == "ORIENTAL" and r["unidade"] == "poligono Zona 0"
                    and r["limiar"] == 0.5][:1])  # so para falhar cedo se mudar
    del or_
    def sr(foco, unid):
        for r in MV["unidades"]:
            if r["foco"] == foco and r["unidade"] == unid and r["limiar"] == 0.5:
                return np.array(r["serie"])
        raise KeyError(unid)
    ctrl = np.array(DR["unidades"]["resto do pomar com pergola"]["NIVEL ABSOLUTO"]["serie"])
    return [("B1 · lóbulo oeste  (SEM restrição de copado)", b1),
            ("foco ORIENTAL · Zona 0 com pérgola", sr("ORIENTAL", "poligono Zona 0")),
            ("foco OCIDENTAL · disco 90 m com pérgola", sr("OCIDENTAL", "disco 90 m")),
            ("resto do pomar · CONTROLO", ctrl)]


UN = unidades()

RNG = np.random.default_rng(20260831)
NPERM = 20000


def perm_p(v, obs):
    k, n, c = int(T.sum()), len(v), 0
    for _ in range(NPERM):
        s = np.zeros(n, bool)
        s[RNG.permutation(n)[:k]] = True
        if abs(v[s].mean() - v[~s].mean()) >= abs(obs):
            c += 1
    return (c + 1) / (NPERM + 1.)


print("A SÉRIE, cena a cena")
print()
print("%-44s %s" % ("", "  ".join(d[2:7] for d in DATAS)))
for nome, v in UN:
    print("%-44s %s" % (nome, "  ".join("%.3f" % x for x in v)))

print()
print("=" * 84)
print("VERSÃO A — diferença de médias, como nas outras unidades")
print("=" * 84)
print()
print("%-44s %10s %9s" % ("", "degrau", "p perm"))
saida = {"b1": dict(area_ha=B["_area_ha"], mascara=B["_mascara"],
                    coordenadas=B["_b1_coordenadas"]),
         "datas": DATAS, "A": {}, "B": {}}
for nome, v in UN:
    d = float(v[T].mean() - v[~T].mean())
    p = perm_p(v, d)
    saida["A"][nome] = dict(degrau=d, p=p, serie=[float(x) for x in v])
    print("%-44s %+10.4f %9.4f%s" % (nome, d, p, "  *" if p < 0.05 else ""))

print()
print("=" * 84)
print("VERSÃO B — desvio à TENDÊNCIA PRÓPRIA de 2017-2024")
print("=" * 84)
print()
print("recta ajustada só a 2017-2024, extrapolada para 2025 e 2026.")
print("desvio = observado menos previsto. Negativo = caiu abaixo do seu rumo.")
print()
print("%-44s %11s %9s %10s %10s %9s"
      % ("", "b/ano 17-24", "p(b)", "prev 25-26", "obs 25-26", "desvio"))
for nome, v in UN:
    lr = stats.linregress(anos[~T], v[~T])
    prev = lr.intercept + lr.slope * anos[T]
    desvio = float(v[T].mean() - prev.mean())
    # p do desvio: residuos de 2017-24 reamostrados para a incerteza da extrapolacao
    res = v[~T] - (lr.intercept + lr.slope * anos[~T])
    nulos = []
    for _ in range(NPERM // 2):
        sim = (lr.intercept + lr.slope * anos[~T]
               + RNG.choice(res, size=int((~T).sum()), replace=True))
        l2 = stats.linregress(anos[~T], sim)
        pr = l2.intercept + l2.slope * anos[T]
        ru = RNG.choice(res, size=int(T.sum()), replace=True)
        nulos.append(float((pr + ru).mean() - pr.mean()))
    nulos = np.array(nulos)
    p = float(np.mean(np.abs(nulos) >= abs(desvio)))
    saida["B"][nome] = dict(b=float(lr.slope), p_b=float(lr.pvalue),
                            previsto=float(prev.mean()),
                            observado=float(v[T].mean()), desvio=desvio, p=p)
    print("%-44s %+11.5f %9.4f %10.3f %10.3f %+9.4f%s"
          % (nome, lr.slope, lr.pvalue, prev.mean(), v[T].mean(), desvio,
             "  *" if p < 0.05 else ""))

print()
print("=" * 84)
print("VEREDICTO SOBRE A PALAVRA «DOIS»")
print("=" * 84)
print()
a = saida["A"]["B1 · lóbulo oeste  (SEM restrição de copado)"]
b = saida["B"]["B1 · lóbulo oeste  (SEM restrição de copado)"]
print("B1, diferença de médias : %+.4f  (p = %.4f)" % (a["degrau"], a["p"]))
print("B1, desvio à tendência  : %+.4f  (p = %.4f)" % (b["desvio"], b["p"]))
print()
if a["degrau"] > 0 and b["desvio"] > -0.03:
    print("O B1 NÃO tem o degrau. Continuam a ser dois sítios, e o B1 passa a ser")
    print("o melhor controlo do caso: mesma exploração, mesma água, mesma gestão,")
    print("526 m de distância — e sem acontecimento.")
else:
    print("O B1 TEM sinal. A palavra «dois» sai da apresentação e a P01 refaz-se.")
saida["veredicto_dois_sitios"] = bool(a["degrau"] > 0 and b["desvio"] > -0.03)

json.dump(saida, open(os.path.join(VG, "lobulo_oeste_degrau.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito lobulo_oeste_degrau.json")
