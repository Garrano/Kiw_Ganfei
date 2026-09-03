# -*- coding: utf-8 -*-
"""As duas moedas medem o mesmo? Confirmar, nao assumir.

A afirmacao a testar
--------------------
«O fosso da C2 da 0,128 e 0,118; o absoluto com calibracao fenologica da 0,1281
e 0,1247. Concordam a 0,001 num foco e 0,007 no outro — isso e convergencia.»

Antes de isso entrar numa figura tem de se verificar que os dois numeros
respondem a **mesma pergunta**. Ha tres eixos em que podem nao responder:

  1. A GRANDEZA.   fosso = referencia menos unidade;  absoluto = so a unidade.
  2. O ESTIMANDO.  o adversario da C2 escreve «2024: 0,008 · 2026: 0,136 ·
                   subida de 0,128» — isso e **duas cenas isoladas**, 2024
                   contra 2026. O meu degrau e **media de 2025-26 contra media
                   de 2017-24**, nove cenas. Nao e a mesma conta.
  3. A UNIDADE.    «foco ESTE plantado» da C2 e Zona 0 sem `nu2021`, tirada da
                   ortofoto. A minha e Zona 0 restrita a pergola pelo LiDAR.

Este processo ja publicou uma «convergencia» que comparava NDRE com NDVI e teve
de a retirar. Duas quantidades proximas nao sao concordantes se responderem a
perguntas diferentes — sao uma coincidencia numerica.

O que se calcula
----------------
As quatro combinacoes de {fosso, absoluto} x {estimando C2, estimando degrau},
nas duas definicoes de unidade, para se ver o que emparelha com o que.

E ha uma relacao algebrica que a tabela tem de obedecer, e serve de verificacao
do proprio codigo:

    degrau_do_fosso  =  degrau_da_referencia  -  degrau_da_unidade

Se a referencia nao se mexesse, as duas moedas dariam o mesmo numero com sinal
trocado. Ela mexe-se — tem catorze celulas dentro dos focos — e e exactamente
por isso que a moeda foi mudada.
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
T = np.array([d >= "2025" for d in DATAS])
i24, i26 = DATAS.index("2024-07-22"), DATAS.index("2026-07-27")

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF = bits("pomar_bits"), bits("saudavel_bits")
ZONA0, NU21 = bits("zona0_bits"), bits("nu2021_bits")
nd = np.stack([rasterio.open(os.path.join(S2, "sentinel", "%s.tif" % d)).read(1)
               for d in DATAS])
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)

ny, nx = POMAR.shape
EE, NN = np.meshgrid(AOI[0] + (np.arange(nx) + .5) * 10.,
                     AOI[3] - (np.arange(ny) + .5) * 10.)
C_OC, C_OR = (530485.0, 4655053.0), (530999.0, 4655102.0)
dsc = lambda c, r=90.: (((EE - c[0]) ** 2 + (NN - c[1]) ** 2) <= r * r) & POMAR

UN = [("OCIDENTAL · disco 90 m (C2: «foco OESTE»)", dsc(C_OC)),
      ("OCIDENTAL · disco 90 m COM pérgola", dsc(C_OC) & COM),
      ("ORIENTAL · Zona 0 sem nu2021 (C2: «ESTE plantado»)", ZONA0 & ~NU21),
      ("ORIENTAL · Zona 0 COM pérgola", ZONA0 & COM),
      ("resto do pomar · controlo", POMAR & COM & ~dsc(C_OC) & ~dsc(C_OR)
       & ~ZONA0 & ~REF)]

serie = lambda m: np.array([float(np.nanmean(nd[i][m])) for i in range(len(DATAS))])
ref = serie(REF)

print("=" * 96)
print("AS QUATRO COMBINAÇÕES.  fosso = referência − unidade.")
print("=" * 96)
print()
print("%-52s %11s %11s %11s %11s"
      % ("", "ABS 24→26", "FOSSO 24→26", "ABS degrau", "FOSSO degrau"))
saida = {}
for nome, m in UN:
    v = serie(m)
    f = ref - v
    abs_c2 = float(v[i26] - v[i24])
    fos_c2 = float(f[i26] - f[i24])
    abs_dg = float(v[T].mean() - v[~T].mean())
    fos_dg = float(f[T].mean() - f[~T].mean())
    saida[nome] = dict(abs_c2=abs_c2, fosso_c2=fos_c2, abs_degrau=abs_dg,
                       fosso_degrau=fos_dg, serie=[float(x) for x in v],
                       fosso=[float(x) for x in f])
    print("%-52s %+11.4f %+11.4f %+11.4f %+11.4f"
          % (nome, abs_c2, fos_c2, abs_dg, fos_dg))

r_c2 = float(ref[i26] - ref[i24])
r_dg = float(ref[T].mean() - ref[~T].mean())
print()
print("%-52s %+11.4f %11s %+11.4f" % ("referência sistemática", r_c2, "—", r_dg))

print()
print("=" * 96)
print("VERIFICAÇÃO ALGÉBRICA:  degrau do fosso  =  degrau da referência − degrau da unidade")
print("=" * 96)
print()
ok = True
for nome in saida:
    s = saida[nome]
    esperado = r_dg - s["abs_degrau"]
    d = abs(esperado - s["fosso_degrau"])
    ok &= d < 1e-9
    print("%-52s esperado %+.4f   obtido %+.4f   %s"
          % (nome, esperado, s["fosso_degrau"], "ok" if d < 1e-9 else "DIVERGE"))
print()
print("identidade verificada: %s" % ok)

print()
print("=" * 96)
print("O EMPARELHAMENTO PROPOSTO, POSTO À PROVA")
print("=" * 96)
print()
print("Os números da C2 são «2024: 0,008 · 2026: 0,136 · subida de 0,128» (OESTE)")
print("e «2024: 0,038 · 2026: 0,156 · subida de 0,118» (ESTE plantado).")
print("Isso é FOSSO, estimando 24→26. A coluna que lhes corresponde é a segunda.")
print()
oc = saida["OCIDENTAL · disco 90 m (C2: «foco OESTE»)"]
or_ = saida["ORIENTAL · Zona 0 sem nu2021 (C2: «ESTE plantado»)"]
print("%-30s %12s %12s %12s" % ("", "C2 publica", "eu reproduzo", "diferença"))
print("%-30s %12.4f %12.4f %12.4f"
      % ("OESTE, fosso 24→26", 0.128, oc["fosso_c2"], abs(0.128 - oc["fosso_c2"])))
print("%-30s %12.4f %12.4f %12.4f"
      % ("ESTE plantado, fosso 24→26", 0.118, or_["fosso_c2"],
         abs(0.118 - or_["fosso_c2"])))
print()
ocp = saida["OCIDENTAL · disco 90 m COM pérgola"]
orp = saida["ORIENTAL · Zona 0 COM pérgola"]
print("E os meus números de degrau em ABSOLUTO, com pérgola, são:")
print("   OCIDENTAL %+.4f      ORIENTAL %+.4f"
      % (ocp["abs_degrau"], orp["abs_degrau"]))
print("Os mesmos em FOSSO, mesmo estimando, mesma unidade:")
print("   OCIDENTAL %+.4f      ORIENTAL %+.4f"
      % (ocp["fosso_degrau"], orp["fosso_degrau"]))
print()
print("A diferença entre as duas moedas, na MESMA unidade e no MESMO estimando,")
print("é o degrau da própria referência: %+.4f." % r_dg)

json.dump(dict(unidades=saida, ref_c2=r_c2, ref_degrau=r_dg,
               identidade_ok=bool(ok)),
          open(os.path.join(VG, "emparelhar_moedas.json"), "w"),
          indent=1, ensure_ascii=False)
print()
print("escrito emparelhar_moedas.json")
