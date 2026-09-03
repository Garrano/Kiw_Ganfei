# -*- coding: utf-8 -*-
"""LACUNA 1 — a referência nunca foi rastreada quanto a descontinuidade.

PORQUE ISTO É A LACUNA MAIS PERIGOSA DA CADEIA
-----------------------------------------------
A retirada do A3 mostrou que uma unidade que **muda de natureza a meio da linha
de base** produz um degrau que não é sintoma, e que dois instrumentos
independentes concordam alegremente com ele.

A referência é a unidade contra a qual **tudo** neste caso é medido: o contraste
foco-menos-controlo do A1, o fosso do B6, as âncoras da prominência da C4-C6, a
mediana das 43 corridas aninhadas do B1. **Se ela tiver uma descontinuidade, o
erro não fica num facto: fica em todos.**

E nunca ninguém perguntou. A C2 R3 e a C3 B10 trataram da *contaminação
geométrica* da referência — células dela dentro dos discos dos focos. Isso é
outra coisa. Ninguém perguntou se a referência foi **replantada, arrancada ou
mudou de gestão** entre 2017 e 2026.

O QUE MUDA EM RELAÇÃO À TRIAGEM DOS BLOCOS
-------------------------------------------
No `reg01_triagem_descontinuidade.py` a pergunta era «isto virou chão?», e o
critério era assimétrico: queda grande **e** nível final baixo. Aqui a pergunta
é mais larga, porque uma referência estragada de qualquer maneira estraga tudo:

  · uma **queda** na referência **encolhe** artificialmente o fosso dos focos;
  · uma **subida** na referência **aumenta-o** artificialmente — e o certificado
    da C2 já registou, na linha 66, que o controlo subiu. Nunca se perguntou se
    essa subida é fenologia ou é replantação a encher.

Por isso mede-se a variação ano-a-ano **nos dois sentidos**, e reporta-se a
maior de cada, com a variação típica da própria série como escala.

CRITÉRIO, fixado antes de correr
--------------------------------
    R1 · variação ano-a-ano em módulo >= 0,10 dentro de 2017-2024
         -> DESCONTINUIDADE A EXPLICAR. Não é exclusão automática: a referência
            não se exclui, explica-se ou cai a cadeia.
    R2 · o ruído típico é o desvio absoluto mediano das variações ano-a-ano.
         Uma variação acima de 3x esse ruído é anómala mesmo abaixo de 0,10.
    R3 · a mesma medida corre em TODAS as unidades de Ganfei, não só na
         referência — para que a referência seja julgada contra as suas vizinhas
         e não contra um limiar solto.

    Se a referência tiver descontinuidade e as outras unidades não, é
    **line-stop**: nenhum fosso publicado sobrevive sem ser recalculado.
"""
import json
import os
import sys

import numpy as np

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
S2D = r"C:\Users\Jackster2\Downloads\ganfei_s2"
C = os.path.join(VG, "_reg01_landsat_cache")
LIM, RUIDO_X = 0.10, 3.0

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import carrega_mascaras, discos_dos_focos   # noqa

masc, _ = carrega_mascaras()
POMAR, REF = masc["pomar"], masc["saudavel"]
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
SEM = np.isfinite(h) & (h < 0.5)
do, de = discos_dos_focos(POMAR)

UN = [("REFERENCIA", REF),
      ("foco OCIDENTAL", do & POMAR & COM),
      ("foco ORIENTAL", de & POMAR & COM),
      ("ORI sem pergola", de & POMAR & SEM),
      ("resto do pomar", POMAR & COM & ~do & ~de & ~REF),
      ("pomar inteiro", POMAR)]

# ---------------------------------------------------------------------------
# PORQUE ISTO CORRE A 10 m E NAO NO LANDSAT
# ---------------------------------------------------------------------------
# A primeira versao deste ficheiro correu no Landsat e devolveu a serie da
# REFERENCIA inteiramente vazia. Nao e um erro: e o T4 outra vez. A referencia
# tem 110 celulas de 10 m mas **zero pixeis de 30 m inteiramente contidos**, e
# com o crivo de cobertura >= 5/9 nao sobra nada. O proprio
# `landsat_independente.py` ja tinha escrito que «a serie da referencia nao deve
# circular de todo».
#
# Logo o rastreio da referencia **tem de ser a 10 m**, no Sentinel-2. Preco: 9
# cenas (uma por ano, sem 2019) em vez de 100. Diz-se, nao se dilui: o poder
# para detectar uma descontinuidade e muito menor, e uma queda de um so ano
# entre 2018 e 2020 seria invisivel porque 2019 nao existe na serie.
# ---------------------------------------------------------------------------

# ---- passar as máscaras de 10 m para a grelha regional de 30 m do Landsat
S = json.load(open(os.path.join(VG, "reg01_local_ou_regional.json"),
                   encoding="utf-8"))
bl = S["blocos"]
xs = [b["E"] for b in bl]
ys = [b["N"] for b in bl]
BB = (min(xs) - 400, min(ys) - 400, max(xs) + 400, max(ys) + 400)
NC, NL = int((BB[2] - BB[0]) / 30), int((BB[3] - BB[1]) / 30)
AOI = (529950, 4654600, 531950, 4655600)
E10, N10 = np.meshgrid(AOI[0] + (np.arange(200) + .5) * 10.,
                       AOI[3] - (np.arange(100) + .5) * 10.)


def para30(m10, cob=5):
    cnt = np.zeros((NL, NC), int)
    ii = ((BB[3] - N10[m10]) / 30).astype(int)
    jj = ((E10[m10] - BB[0]) / 30).astype(int)
    k = (ii >= 0) & (ii < NL) & (jj >= 0) & (jj < NC)
    np.add.at(cnt, (ii[k], jj[k]), 1)
    return cnt >= cob


M = {n: m for n, m in UN}
print("unidades de Ganfei, a 10 m:")
for nome, m10 in UN:
    n30 = int(para30(m10).sum())
    print("  %-18s %6.2f ha  ·  n10 = %4d  ·  n30 seria %3d %s"
          % (nome, m10.sum() / 100, int(m10.sum()), n30,
             "  <-- o Landsat NAO a resolve" if n30 < 5 else ""))

# a cache regional de 10 m, recortada na janela de Ganfei
C10 = os.path.join(VG, "_reg01_cache")
c0 = int(round((AOI[0] - BB[0]) / 10))
r0 = int(round((BB[3] - AOI[3]) / 10))
ANOS = [str(a) for a in range(2017, 2027)]
serie = {n: {a: [] for a in ANOS} for n in M}
NCE_D = {a: 0 for a in ANOS}
for f in sorted(os.listdir(C10)):
    if not f.startswith("ndvi_"):
        continue
    data = f[5:15]
    a = data[:4]
    if a not in serie["REFERENCIA"]:
        continue
    nd = np.load(os.path.join(C10, f))[r0:r0 + 100, c0:c0 + 200]
    NCE_D[a] += 1
    for n, m in M.items():
        v = nd[m]
        v = v[np.isfinite(v)]
        if v.size >= max(3, 0.5 * m.sum()):
            serie[n][a].append(float(np.median(v)))

NIV = {n: np.array([np.median(d[a]) if d[a] else np.nan for a in ANOS])
       for n, d in serie.items()}
NCE = {n: [len(d[a]) for a in ANOS] for n, d in serie.items()}
NCE["REFERENCIA"] = [NCE_D[a] for a in ANOS]

print()
print("=" * 100)
print("NIVEL ANUAL (Sentinel-2 a 10 m, mediana das cenas)  ·  n de cenas por ano em baixo")
print("=" * 100)
print()
print("%-18s %s" % ("", " ".join("%6s" % a for a in ANOS)))
for n in M:
    print("%-18s %s" % (n, " ".join("     ." if not np.isfinite(v) else "%6.3f" % v
                                    for v in NIV[n])))
print("%-18s %s" % ("(n de cenas)", " ".join("%6d" % v for v in NCE["REFERENCIA"])))

print()
print("=" * 100)
print("R1-R3 · variacao ano-a-ano DENTRO de 2017-2024, nos dois sentidos")
print("=" * 100)
print()
print("%-18s %11s %11s %10s %10s  %s"
      % ("", "maior queda", "maior subida", "ruido", "3x ruido", "veredicto"))
ALERTA = []
for n in M:
    v = NIV[n]
    k = ANOS.index("2024")
    d = np.diff(v[:k + 1])
    ok = np.isfinite(d)
    if ok.sum() < 3:
        print("%-18s   serie curta de mais" % n)
        continue
    ruido = float(np.median(np.abs(d[ok] - np.median(d[ok]))))
    q, qi = float(np.min(d[ok])), int(np.argmin(np.where(ok, d, np.inf)))
    s, si = float(np.max(d[ok])), int(np.argmax(np.where(ok, d, -np.inf)))
    pior = max(abs(q), abs(s))
    grande = pior >= LIM
    anom = pior > RUIDO_X * max(ruido, 1e-4)
    ver = ("DESCONTINUIDADE" if grande else
           ("anomala face ao proprio ruido" if anom else "continua"))
    if grande or anom:
        ALERTA.append((n, pior, ver))
    print("%-18s %+7.3f(%s) %+7.3f(%s) %10.4f %10.4f  %s"
          % (n, q, ANOS[qi + 1], s, ANOS[si + 1], ruido, RUIDO_X * ruido, ver))

print()
if not ALERTA:
    print("Nenhuma unidade de Ganfei tem descontinuidade dentro de 2017-2024.")
    print("A REFERENCIA sobrevive ao rastreio. O denominador do A1, do A2 e do")
    print("bloco B mantem-se, e a lacuna 1 fecha.")
else:
    print("A EXPLICAR:")
    for n, p, ver in ALERTA:
        print("   %-18s variacao maxima %.3f  ·  %s" % (n, p, ver))
    if any(n == "REFERENCIA" for n, _, _ in ALERTA):
        print()
        print("   >>> LINE-STOP: a descontinuidade esta na REFERENCIA. Nenhum")
        print("       fosso publicado sobrevive sem recalculo.")

# ---------------------------------------------------- a subida do controlo
print()
print("=" * 100)
print("A SUBIDA DO CONTROLO que a C2 registou na linha 66 — quanto e, e onde")
print("=" * 100)
v = NIV["REFERENCIA"]
k = ANOS.index("2024")
print()
print("referencia 2017 -> 2024: %+.4f no total, %+.5f por ano"
      % (v[k] - v[0], (v[k] - v[0]) / (k)))
A = np.arange(k + 1, dtype=float)
b = np.isfinite(v[:k + 1])
if b.sum() < 3:
    raise SystemExit("a referencia tem menos de 3 anos com valor — nao se ajusta recta")
m, c = np.polyfit(A[b], v[:k + 1][b], 1)
res = v[:k + 1][b] - (m * A[b] + c)
print("recta ajustada: declive %+.5f por ano, residuo maximo %.4f"
      % (m, np.abs(res).max()))
print("Uma replantacao a encher da-se como declive positivo COM residuo pequeno;")
print("fenologia da-se como residuo da ordem do ruido interanual (%.4f)."
      % float(np.median(np.abs(np.diff(v[:k + 1][b])))))

json.dump(dict(anos=ANOS, nivel={n: [None if not np.isfinite(x) else float(x)
                                     for x in NIV[n]] for n in M},
               n10={n: int(M[n].sum()) for n in M},
               alerta=[[n, p, ver] for n, p, ver in ALERTA]),
          open(os.path.join(VG, "triagem_referencia.json"), "w"), indent=1)
print()
print("escrito triagem_referencia.json")
