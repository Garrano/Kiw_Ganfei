# -*- coding: utf-8 -*-
"""Testa uma previsao falsificavel contra um instrumento independente.

HIPOTESE (fixada antes de olhar para o resultado)
--------------------------------------------------
O desenho de rega ESTA a escala declarada, 1:3500 em A1. O PDF que temos e a
reducao A1->A4, logo a escala na pagina e 1:9899 e a 400 dpi da 0,6286 m/px.
O `valvulas_v4.json` usou 0,788 m/px, inflado 25,4 %.

Se assim for, as posicoes do LOBO OESTE — extrapoladas 1,3 km para la da ancora
— tem de estar deslocadas ~330 m PARA FORA da ancora, ou seja para sudoeste, e
uma contraccao uniforme de k = 0,6286/0,788 em torno de uma ancora situada no
CORPO tem de as trazer para cima do poligono B1 do IFAP.

O QUE FALSIFICA
---------------
· o deslocamento observado nao ser para sudoeste;
· a ancora implicada cair fora do corpo do pomar (seria um ajuste sem sentido
  fisico, e entao a explicacao da escala nao serve);
· a contraccao nao aproximar as valvulas do B1.

O B1 vem do parcelario IFAP. Nao partilha nada com o desenho de rega — e a
condicao que o `CLAUDE.md` exige: nenhum facto passa verificado so pelo
instrumento que o produziu.
"""
import io
import json
import math

BASE = r"C:/Users/Jackster2/Downloads/ganfei_s2"
m = json.load(io.open(BASE + "/figuras/base/base_sectores.json", encoding="utf-8"))
v4 = json.load(io.open(BASE + "/valvulas_v4.json", encoding="utf-8"))

K = 0.6286 / 0.788                       # contraccao prevista

lobo = {k: tuple(v) for k, v in v4["lobo_oeste"].items()}
corpo = {k: (v["E"], v["N"]) for k, v in m["valvulas"].items() if int(k) >= 6}

pts = [p for poly in m["b1"]["coordinates"] for ring in poly for p in ring]
b1c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
b1x = (min(p[0] for p in pts), max(p[0] for p in pts))
b1y = (min(p[1] for p in pts), max(p[1] for p in pts))

lc = (sum(p[0] for p in lobo.values()) / len(lobo),
      sum(p[1] for p in lobo.values()) / len(lobo))
cc = (sum(p[0] for p in corpo.values()) / len(corpo),
      sum(p[1] for p in corpo.values()) / len(corpo))

dx, dy = b1c[0] - lc[0], b1c[1] - lc[1]
dist = math.hypot(dx, dy)
rumo = (math.degrees(math.atan2(dx, dy)) + 360) % 360

print("centroide lobo (v4)     E%.0f N%.0f" % lc)
print("centroide B1 (IFAP)     E%.0f N%.0f" % b1c)
print("B1 caixa                E%.0f..%.0f  N%.0f..%.0f" % (b1x[0], b1x[1],
                                                            b1y[0], b1y[1]))
print("centroide corpo         E%.0f N%.0f" % cc)
print()
print("deslocamento lobo->B1   %.0f m, rumo %.0f graus  (o lobo esta a %s do B1)"
      % (dist, rumo, "SW" if dx > 0 and dy > 0 else "?"))
print("  previsto pela escala  ~330 m, para fora da ancora")
print()

# a ancora implicada por uma contraccao de K que leve o lobo ao B1
A = ((b1c[0] - K * lc[0]) / (1 - K), (b1c[1] - K * lc[1]) / (1 - K))
print("ancora implicada        E%.0f N%.0f" % A)
d_corpo = math.hypot(A[0] - cc[0], A[1] - cc[1])
print("  distancia ao corpo    %.0f m" % d_corpo)
dentro = (min(p[0] for p in corpo.values()) - 300 < A[0]
          < max(p[0] for p in corpo.values()) + 300
          and min(p[1] for p in corpo.values()) - 300 < A[1]
          < max(p[1] for p in corpo.values()) + 300)
print("  cai no corpo?         %s" % ("SIM" if dentro else "NAO"))
print()

print("valvulas 1-5 depois da contraccao em torno dessa ancora:")
dentro_b1 = 0
for k in sorted(lobo, key=int):
    p = lobo[k]
    q = (A[0] + K * (p[0] - A[0]), A[1] + K * (p[1] - A[1]))
    ok = b1x[0] <= q[0] <= b1x[1] and b1y[0] <= q[1] <= b1y[1]
    dentro_b1 += ok
    print("  v%-2s  E%.0f N%.0f  ->  E%.0f N%.0f   %s"
          % (k, p[0], p[1], q[0], q[1], "na caixa do B1" if ok else "fora"))
print()
print("VEREDICTO: %d de 5 caem na caixa do B1 apos correccao de escala."
      % dentro_b1)
