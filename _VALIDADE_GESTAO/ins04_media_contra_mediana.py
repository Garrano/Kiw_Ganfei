# -*- coding: utf-8 -*-
"""INS-04 · a referência está em declínio? Média contra mediana, na série densa.

O CONFLITO, E PORQUE NÃO É UM CONFLITO
---------------------------------------
O livro-razão da C4 tem a linha **INS-04**, com estatuto SUSTENTADA:

  «a referência sistemática DESCE, 0,8884 -> 0,8425, -0,00395/ano (…) o que o T4
   mede — média a cair 0,0548 contra 0,0219 da mediana, afastamento entre as
   duas a alargar 31 vezes — é um SUBCONJUNTO de células da referência a
   colapsar, e não é sensor.»

E o `triagem_referencia_densa.py`, corrido hoje com 301 cenas, diz «REFERÊNCIA
contínua» e fechou a lacuna 1.

**As duas coisas podem ser verdadeiras ao mesmo tempo, e é isso que torna isto
perigoso.** O meu rastreio mede a **mediana** por unidade. Uma mediana é
insensível, por construção, a uma minoria de células a colapsar: enquanto menos
de metade cair, ela não se mexe. **Se o INS-04 estiver certo, a minha conclusão
de hoje é verdadeira e enganadora.**

O QUE ESTE FICHEIRO FAZ
-----------------------
Mede as duas estatísticas nas MESMAS cenas e nas MESMAS células.

CRITÉRIOS, fixados antes de correr
-----------------------------------
    I1 · Se a média cair significativamente mais do que a mediana, e o
         afastamento entre elas alargar, **o INS-04 confirma-se** e a minha
         frase de hoje tem de levar «da mediana» ao lado. O rastreio não muda:
         continua a não haver descontinuidade. Muda o que ele autoriza dizer.

    I2 · Se as duas caírem igual, **o INS-04 cai** — e cai por um instrumento
         mais denso, não por opinião.

    I3 · A magnitude do INS-04 (−0,00395/ano) tem de ser reproduzida ou
         corrigida com o seu número. A série densa dá −0,00158/ano na mediana;
         se a média der perto de −0,00395, a diferença era a estatística.

    Sem hipótese sobre qual ganha. O T4 é anterior e mais próximo do dado
    original; a série densa tem 33x mais cenas. **Nenhum dos dois é
    automaticamente melhor**, e é por isso que se mede em vez de se escolher.

O QUE ISTO NÃO DECIDE
---------------------
**Porque é que um subconjunto da referência cai.** Se cair, isso é uma pergunta
nova — e a resposta não está em mais NDVI, pelo mesmo princípio que já retirou
dezanove veredictos neste caso.
"""
import json
import os
import sys

import numpy as np

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C = os.path.join(VG, "_densa_ganfei")

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import carrega_mascaras, discos_dos_focos   # noqa

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
do, de = discos_dos_focos(POMAR)
UN = {"REFERENCIA": REF,
      "resto do pomar": POMAR & COM & ~do & ~de & ~REF,
      "foco OCIDENTAL": do & POMAR & COM}
print("celulas: %s" % "  ".join("%s %d" % (k, v.sum()) for k, v in UN.items()))

fich = sorted(f for f in os.listdir(C) if f.endswith(".npy"))
ANOS = [str(a) for a in range(2017, 2027)]
med = {u: {a: [] for a in ANOS} for u in UN}
mea = {u: {a: [] for a in ANOS} for u in UN}
p10 = {u: {a: [] for a in ANOS} for u in UN}
for f in fich:
    a = f[:4]
    if a not in ANOS:
        continue
    nd = np.load(os.path.join(C, f))
    for u, m in UN.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= 0.7 * m.sum():
            med[u][a].append(float(np.median(v)))
            mea[u][a].append(float(np.mean(v)))
            p10[u][a].append(float(np.percentile(v, 10)))

print("cenas por ano: %s" % "  ".join(
    "%s:%d" % (a, len(med["REFERENCIA"][a])) for a in ANOS))


def anual(d, u):
    return np.array([np.median(d[u][a]) if d[u][a] else np.nan for a in ANOS])


def declive(y, ate):
    k = ANOS.index(ate) + 1
    x = np.arange(k, dtype=float)
    b = np.isfinite(y[:k])
    if b.sum() < 3:
        return np.nan
    return float(np.polyfit(x[b], y[:k][b], 1)[0])


print()
print("=" * 96)
print("I1-I3 · a REFERENCIA, tres estatisticas nas mesmas celulas e nas mesmas cenas")
print("=" * 96)
print()
print("%-14s %s" % ("", " ".join("%7s" % a for a in ANOS)))
R = {}
for nome, d in (("mediana", med), ("media", mea), ("percentil 10", p10)):
    y = anual(d, "REFERENCIA")
    R[nome] = y
    print("%-14s %s" % (nome, " ".join("      ." if not np.isfinite(v) else "%7.4f" % v
                                       for v in y)))
print()
print("%-14s %14s %14s %12s" % ("", "declive 17-24", "declive 17-26", "queda total"))
for nome in ("mediana", "media", "percentil 10"):
    y = R[nome]
    b = np.isfinite(y)
    print("%-14s %+14.5f %+14.5f %12.4f"
          % (nome, declive(y, "2024"), declive(y, "2026"), y[b][0] - y[b][-1]))

print()
afast = R["mediana"] - R["media"]
b = np.isfinite(afast)
print("AFASTAMENTO mediana menos media (o que o T4 diz alargar 31x):")
print("   %s" % "  ".join("%s %+0.4f" % (a, v)
                          for a, v in zip(ANOS, afast) if np.isfinite(v)))
print("   primeiro %+0.4f  ->  ultimo %+0.4f  ·  razao %.1fx"
      % (afast[b][0], afast[b][-1],
         abs(afast[b][-1]) / max(abs(afast[b][0]), 1e-6)))

print()
print("=" * 96)
print("O VEREDICTO, pelos criterios escritos antes de correr")
print("=" * 96)
dm, dme = declive(R["mediana"], "2026"), declive(R["media"], "2026")
razao = dme / dm if dm else float("nan")
print()
print("I1/I2 · a media cai %.2fx o que a mediana cai (%+.5f contra %+.5f)"
      % (razao, dme, dm))
if razao > 1.5 and abs(afast[b][-1]) > 2 * abs(afast[b][0]):
    print("        -> INS-04 CONFIRMA-SE. A frase de hoje precisa de 'da mediana'.")
elif razao < 1.2:
    print("        -> INS-04 CAI: as duas estatisticas caem igual.")
else:
    print("        -> INTERMEDIO: nao decide. Fica NAO TESTAVEL com o numero a vista.")
print()
print("I3 · INS-04 declara -0,00395/ano. A serie densa da:")
print("        mediana %+0.5f   ·   media %+0.5f" % (dm, dme))

json.dump(dict(anos=ANOS, mediana=R["mediana"].tolist(), media=R["media"].tolist(),
               p10=R["percentil 10"].tolist(),
               declive_mediana_1726=dm, declive_media_1726=dme,
               declive_mediana_1724=declive(R["mediana"], "2024"),
               declive_media_1724=declive(R["media"], "2024")),
          open(os.path.join(VG, "ins04_media_contra_mediana.json"), "w"), indent=1)
print()
print("escrito ins04_media_contra_mediana.json")
