# -*- coding: utf-8 -*-
"""A segunda constelacao, na moeda nova: degrau em NIVEL ABSOLUTO no Landsat.

O que mudou, e porque isto agora se pode fazer
----------------------------------------------
Enquanto a moeda foi «fosso a referencia», o Landsat era dificil de usar: a
referencia do Landsat cai 0,026 e a do Sentinel-2 cai 0,054 nas mesmas
celulas, e comparar dois fossos medidos contra duas referencias que se movem
de maneiras diferentes nao prova grande coisa.

Em nivel absoluto o problema desaparece, porque **o teste passa a ser dentro
de cada constelacao**. Nao se compara o valor do Landsat com o valor do
Sentinel-2 — o que exigiria calibracao cruzada e seria atacavel. Compara-se o
DEGRAU medido pelo Landsat com o DEGRAU medido pelo Sentinel-2, cada um na
sua propria escala, cada um com o seu proprio controlo interno.

Duas agencias, dois sensores, duas cadeias de correccao atmosferica, duas
orbitas. Se as duas virem o mesmo degrau nos mesmos sitios e nada no controlo,
a pergunta «isto e o vosso processamento ou e o campo?» fica respondida com
dados.

O teste, fixado antes de correr
-------------------------------
    H0 : o nivel absoluto de NDVI Landsat nas unidades de foco nao muda entre
         2013-2024 e 2025-2026.
    H1 : desce.

Agrega-se por ANO (mediana das cenas do ano) antes de testar, porque o numero
de cenas por ano varia de 4 a 30 e sem agregar os anos com mais cenas pesavam
mais. Permutacao da etiqueta de ano: 14 anos, 2 tardios, C(14,2) = 91 divisoes
possiveis — logo o p minimo atingivel e 1/91 = 0,011, e diz-se.

O CONTROLO e a peca central do teste, nao um acessorio: se o resto do pomar
tambem descesse no Landsat, o degrau seria da atmosfera, do sensor ou do
arquivo, e nao do sitio.
"""
import itertools
import json
import os

import numpy as np

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
D = json.load(open(os.path.join(VG, "landsat.json")))

UN = [("ORIENTAL com pergola", "ESTE com pergola", True),
      ("ORIENTAL sem pergola  (controlo de chao)", "ESTE sem pergola", True),
      ("OCIDENTAL com pergola", "OESTE com pergola", False),
      ("resto do pomar  (CONTROLO)", "resto do pomar", True),
      ("referencia sistematica", "referencia", True)]

anos = sorted({int(r["data"][:4]) for r in D})
TARDIO = np.array([a >= 2025 for a in anos])
print("anos: %s   (%d cenas)" % (", ".join(str(a) for a in anos), len(D)))
print("cenas por ano: %s"
      % "  ".join("%d:%d" % (a, sum(1 for r in D if int(r["data"][:4]) == a))
                  for a in anos))
print()

# p exacto: enumeram-se TODAS as divisoes de 14 anos em 2, nao se amostra
idx = list(range(len(anos)))
TODAS = list(itertools.combinations(idx, int(TARDIO.sum())))
print("divisoes possiveis de %d anos em %d tardios: %d  ->  p minimo = %.4f"
      % (len(anos), int(TARDIO.sum()), len(TODAS), 1.0 / len(TODAS)))
print()


def serie_anual(chave):
    v = []
    for a in anos:
        x = [r[chave] for r in D if int(r["data"][:4]) == a and r.get(chave) is not None]
        v.append(float(np.median(x)) if x else np.nan)
    return np.array(v)


def degrau_exacto(v):
    """p exacto por enumeracao completa das divisoes de anos."""
    obs = v[TARDIO].mean() - v[~TARDIO].mean()
    c = 0
    for comb in TODAS:
        s = np.zeros(len(v), bool)
        s[list(comb)] = True
        if abs(v[s].mean() - v[~s].mean()) >= abs(obs) - 1e-12:
            c += 1
    return float(obs), c / float(len(TODAS))


print("=" * 90)
print("LANDSAT 8/9 — NIVEL ABSOLUTO DE NDVI, mediana anual")
print("=" * 90)
print()
print("%-42s %s" % ("", "  ".join("%4d" % a for a in anos)))
saida = {"anos": anos, "n_cenas": len(D), "divisoes": len(TODAS), "unidades": {}}
for nome, chave, indep in UN:
    v = serie_anual(chave)
    print("%-42s %s" % (nome, "  ".join("%.3f" % x for x in v)))
    d, p = degrau_exacto(v)
    saida["unidades"][nome] = dict(serie=[float(x) for x in v], degrau=d,
                                   p=p, fronteira_independente=indep)

print()
print("%-42s %9s %9s %s" % ("", "degrau", "p exacto", "fronteira"))
for nome, chave, indep in UN:
    r = saida["unidades"][nome]
    print("%-42s %+9.4f %9.4f %s%s"
          % (nome, r["degrau"], r["p"],
             "independente" if indep else "CENTRO DO SINAL",
             "  *" if r["p"] < 0.05 else ""))

print()
print("=" * 90)
print("AS DUAS CONSTELACOES, LADO A LADO")
print("=" * 90)
print()
S2 = {"ORIENTAL com pergola": -0.1236, "OCIDENTAL com pergola": -0.1288,
      "resto do pomar  (CONTROLO)": -0.0136}
print("%-42s %12s %12s" % ("", "Sentinel-2", "Landsat"))
for nome in ("ORIENTAL com pergola", "OCIDENTAL com pergola",
             "resto do pomar  (CONTROLO)"):
    print("%-42s %+12.4f %+12.4f"
          % (nome, S2[nome], saida["unidades"][nome]["degrau"]))
print()
print("Nao se comparam NIVEIS entre constelacoes — escalas diferentes, cadeias")
print("de correccao diferentes. Compara-se o DEGRAU que cada uma mede na sua")
print("propria escala, e o CONTROLO que cada uma mede na sua propria escala.")

r_or = saida["unidades"]["ORIENTAL com pergola"]
r_ct = saida["unidades"]["resto do pomar  (CONTROLO)"]
print()
print("VEREDICTO")
ok = r_or["p"] < 0.05 and r_ct["p"] > 0.05 and r_or["degrau"] < 0
print("  foco oriental desce e e significativo : %s  (%+.4f, p=%.4f)"
      % ("SIM" if (r_or["degrau"] < 0 and r_or["p"] < 0.05) else "NAO",
         r_or["degrau"], r_or["p"]))
print("  controlo NAO desce significativamente : %s  (%+.4f, p=%.4f)"
      % ("SIM" if r_ct["p"] > 0.05 else "NAO", r_ct["degrau"], r_ct["p"]))
print("  => replicacao independente do degrau  : %s" % ("SIM" if ok else "NAO"))
saida["veredicto_replicacao"] = bool(ok)

json.dump(saida, open(os.path.join(VG, "landsat_degrau_absoluto.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito landsat_degrau_absoluto.json")
