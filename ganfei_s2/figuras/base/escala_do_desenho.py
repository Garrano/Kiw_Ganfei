# -*- coding: utf-8 -*-
"""O esquema não tem UMA escala — e é por isso que nada o consegue rectificar.

O QUE ISTO FECHA
----------------
Quatro reconstruções das posições das válvulas discordaram entre 92 e 398 m.
Duas tentativas minhas de georreferenciar o desenho falharam: ICP automático
com **RMS 70,3 m**, e ajuste afim com pontos escolhidos à vista com **RMS
189,1 m** — sete vezes o chão de leitura (±25 m).

Quando o resíduo é muito maior do que o erro de medição, o problema não é a
medição: é o **modelo**. E o modelo era «existe uma transformação global que
leva o desenho ao terreno».

O TESTE, que é o mais simples possível
--------------------------------------
Se o desenho tivesse uma escala, **a razão metros/píxel seria a mesma entre
quaisquer dois pontos**. Mede-se par a par, com pontos que existem nos dois
lados, e vê-se.

Só se usam pares **longos** — acima de 400 px — porque num par curto o erro de
leitura domina e o resultado não diz nada.
"""
import io
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
MIN_PX = 400.0

P = {
    "B1 oeste":    ((74, 770),    (529495, 4653955)),
    "B1 sul":      ((126, 819),   (529574, 4653832)),
    "B1 este":     ((583, 605),   (530063, 4654416)),
    "B1 norte":    ((328, 567),   (529729, 4654477)),
    "banda oeste": ((1044, 481),  (530128, 4654997)),
    "banda este":  ((1562, 591),  (531536, 4655439)),
}
ks = list(P)
linhas = []
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = ks[i], ks[j]
        dpx = float(np.hypot(*(np.array(P[a][0], float) - np.array(P[b][0], float))))
        dm = float(np.hypot(*(np.array(P[a][1], float) - np.array(P[b][1], float))))
        onde = ("no lobo B1" if a.startswith("B1") and b.startswith("B1")
                else "na banda" if a.startswith("banda") and b.startswith("banda")
                else "entre os dois")
        linhas.append(dict(de=a, para=b, px=dpx, m=dm, m_px=dm / dpx, onde=onde))

longos = [l for l in linhas if l["px"] >= MIN_PX]
print("pares com mais de %.0f px (abaixo disso o erro de leitura domina): %d de %d"
      % (MIN_PX, len(longos), len(linhas)))
print()
print("%-13s %-13s %7s %7s %8s   %s" % ("de", "para", "px", "m", "m/px", "onde"))
for l in sorted(longos, key=lambda x: x["m_px"]):
    print("%-13s %-13s %7.0f %7.0f %8.2f   %s"
          % (l["de"], l["para"], l["px"], l["m"], l["m_px"], l["onde"]))

r = np.array([l["m_px"] for l in longos])
print()
print("escala aparente: %.2f a %.2f m/px  ->  variação de %.1f×"
      % (r.min(), r.max(), r.max() / r.min()))
for onde in ("no lobo B1", "entre os dois", "na banda"):
    v = [l["m_px"] for l in longos if l["onde"] == onde]
    if v:
        print("   %-14s n=%d  mediana %.2f m/px" % (onde, len(v), np.median(v)))
vl = [l["m_px"] for l in longos if l["onde"] == "no lobo B1"]
vb = [l["m_px"] for l in longos if l["onde"] == "na banda"]

print()
print("=" * 74)
if r.max() / r.min() > 1.5:
    print("O DESENHO NÃO ESTÁ A UMA ESCALA ÚNICA.")
    print()
    print("A escala aparente varia por %.1f× entre pares longos, muito acima do"
          % (r.max() / r.min()))
    print("que o erro de leitura explica. O lobo do B1 está desenhado a cerca de")
    if vl and vb:
        print("%.2f m/px e a banda contígua a %.2f m/px — a banda vai COMPRIMIDA"
              % (np.median(vl), np.median(vb)))
        print("por um factor de %.1f× em relação ao lobo." % (np.median(vb) / np.median(vl)))
    print()
    print("Consequência: **nenhuma transformação global — semelhança, afim ou")
    print("projectiva — pode rectificar este desenho**, porque não há uma escala")
    print("para acertar. É um esquema de topologia com uma planta por baixo, não")
    print("uma planta. Isto explica de uma vez:")
    print("   · as quatro reconstruções a discordar 92–398 m;")
    print("   · o ICP automático a dar RMS 70,3 m;")
    print("   · o ajuste afim manual a dar RMS 189,1 m;")
    print("   · e a nota do próprio valvulas_v4.json: «o desenho NÃO está à")
    print("     escala declarada».")
    print()
    print("O QUE RESTA, e não passa por rectificar o desenho:")
    print("   1. as LINHAS. O gestor anota cada válvula por número de fileira")
    print("      (130-131, 267-268, 306-307, 336-337, 353, 409, 423). As fileiras")
    print("      são visíveis na ortofoto e no LiDAR, e o compasso já foi medido")
    print("      (30,31 ha de pérgola). Contar fileiras dá posição em metros sem")
    print("      tocar no desenho. É o caminho por explorar.")
    print("   2. perguntar ao gestor — que é a pergunta 2 da lista.")
else:
    print("a escala é consistente; o problema é outro.")
print("=" * 74)

json.dump(dict(min_px=MIN_PX, pares=longos,
               escala_min=float(r.min()), escala_max=float(r.max()),
               variacao=float(r.max() / r.min()),
               mediana_lobo=float(np.median(vl)) if vl else None,
               mediana_banda=float(np.median(vb)) if vb else None,
               veredicto="o desenho não tem uma escala única; nenhuma "
                         "transformação global o rectifica"),
          io.open(os.path.join(AQUI, "escala_do_desenho.json"), "w",
                  encoding="utf-8"), indent=1, ensure_ascii=False)
print()
print("escrito escala_do_desenho.json")
