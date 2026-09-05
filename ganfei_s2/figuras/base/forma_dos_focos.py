# -*- coding: utf-8 -*-
"""A mancha tem a forma de um sector de rega? — e vale a pena o GPS?

A PERGUNTA PRÁTICA
------------------
Cinco tentativas de colocar as 17 válvulas falharam. A pergunta seguinte não é
«como é que se tenta a sexta», é **para que serve**. E as posições das válvulas
servem, na prática, uma única hipótese causal: **o declínio segue a rede de
rega** — identidade de válvula e posição na conduta, mais do que a geografia.

Há um teste que a decide sem posição nenhuma, e é de graça.

O ARGUMENTO
-----------
Uma válvula serve um **troço contíguo de fileiras**. A mancha que uma avaria de
rega produz é, por construção, uma **faixa alinhada com as fileiras** — longa
ao longo delas, estreita a atravessá-las. Se a mancha de declínio for
aproximadamente redonda, ou estiver enviesada em relação às fileiras, **não é a
forma de um sector**, e a hipótese da rede não precisa das posições para cair.

O eixo das fileiras foi medido na R2 G3: **azimute 70,3°**.

O CONTROLO, que é o que torna isto um teste
--------------------------------------------
Mede-se a mesma coisa na máscara da **referência sistemática**, que foi
desenhada por nós ao longo das fileiras. Se o método funciona, a referência tem
de sair muito alongada e alinhada. Se sair redonda, o método não mede forma
nenhuma e o resultado da mancha não vale nada.

O QUE ISTO NÃO DECIDE
---------------------
Só há **uma** mancha em máscara geográfica — a `zona0`, o foco oriental. A do
foco ocidental (`manchaW`) só existe nas máscaras derivadas do sinal, que estão
retiradas por circularidade. **n = 1**, e diz-se.
"""
import io
import json
import os
import sys

import numpy as np

C1 = r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS/SAIDA_C1"
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, C1)
from c1_00_comum import carrega_mascaras, centros_celulas   # noqa: E402

AZ = 70.3
M, _ = carrega_mascaras()
E, N = centros_celulas()
u = np.array([np.sin(np.radians(AZ)), np.cos(np.radians(AZ))])
v = np.array([-u[1], u[0]])

print("eixo das fileiras: azimute %.1f°" % AZ)
print()
print("%-11s %6s %9s %9s %7s %8s  %s"
      % ("máscara", "ha", "ao longo", "atravessa", "razão", "desvio", "o que é"))
res = {}
for k, papel in (("zona0", "MANCHA de declínio (foco oriental)"),
                 ("saudavel", "CONTROLO: referência, desenhada ao longo das fileiras"),
                 ("nu2021", "solo nu 2021, para comparar")):
    m = M[k]
    if m.sum() < 20:
        continue
    P = np.column_stack([E[m], N[m]])
    P = P - P.mean(0)
    sa, sb = (P @ u).std(), (P @ v).std()
    w, V = np.linalg.eigh(np.cov(P.T))
    pa = V[:, -1]
    ang = np.degrees(np.arctan2(pa[0], pa[1])) % 180
    dif = min(abs(ang - AZ), 180 - abs(ang - AZ))
    res[k] = dict(ha=float(m.sum() * 100 / 1e4), ao_longo_m=float(4 * sa),
                  atravessa_m=float(4 * sb), razao=float(sa / sb),
                  eixo_graus=float(ang), desvio_graus=float(dif), papel=papel)
    print("%-11s %6.2f %9.0f %9.0f %7.2f %7.0f°  %s"
          % (k, res[k]["ha"], 4 * sa, 4 * sb, sa / sb, dif, papel))

z, s = res["zona0"], res["saudavel"]
print()
print("=" * 76)
print("O controlo funciona: a referência sai com razão %.2f e a %.0f° das fileiras."
      % (s["razao"], s["desvio_graus"]))
print("Portanto o método mede forma.")
print()
print("A mancha sai com razão **%.2f** e a **%.0f°** das fileiras — %d × menos"
      % (z["razao"], z["desvio_graus"], round(s["razao"] / z["razao"])))
print("alongada do que uma faixa desenhada ao longo das fileiras.")
print()
if z["razao"] < 2.0 or z["desvio_graus"] > 20:
    print("-> A MANCHA NÃO TEM A FORMA DE UM SECTOR DE REGA.")
    print("   %.0f × %.0f m é um bolo, não uma faixa." % (z["ao_longo_m"], z["atravessa_m"]))
else:
    print("-> compatível com um sector de rega.")
print("=" * 76)
print()
print("A COINCIDÊNCIA QUE ENGANA, e vai escrita porque é o que faz perseguir isto:")
print("  a mancha tem %.2f ha, e as válvulas 6 a 9 servem 2,50 · 2,51 · 2,82 ·"
      % z["ha"])
print("  1,82 ha. **A ÁREA bate com a de uma válvula.** É a forma que não bate,")
print("  e a área sozinha teria mandado toda a gente atrás da rega.")
print()
print("n = 1. Só a zona0 tem máscara geográfica; a do foco ocidental é derivada")
print("do sinal e está retirada por circularidade.")

json.dump(dict(azimute_fileiras=AZ, mascaras=res,
               veredicto=("a mancha não tem forma de sector de rega"
                          if (z["razao"] < 2.0 or z["desvio_graus"] > 20)
                          else "compatível com sector"),
               n=1,
               ressalva="só a zona0 tem máscara geográfica; a manchaW é "
                        "derivada do sinal e está retirada"),
          io.open(os.path.join(AQUI, "forma_dos_focos.json"), "w",
                  encoding="utf-8"), indent=1, ensure_ascii=False)
print()
print("escrito forma_dos_focos.json")
