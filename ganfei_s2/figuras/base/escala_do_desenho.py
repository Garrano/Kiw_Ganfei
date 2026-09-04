"""RETIRADO — a conclusão deste ficheiro estava errada, e a razão fica escrita.

> # ⚠ RETIRADO
>
> **O que este ficheiro concluiu a 04-09:** «o desenho não está a uma escala
> única; a banda vai comprimida 1,9× em relação ao lobo; nenhuma transformação
> global o rectifica».
>
> **É falso, e a culpa é de uma leitura minha.** Eu tinha posto a ponta
> ORIENTAL do desenho em x = 1562 px. Está em **x ≈ 2160** — falhei-a por 600
> píxeis, ou seja **750 m**. Com a ponta errada, a banda media 517 px em vez de
> 1164, e claro que a escala saía a dobrar.
>
> **O gestor deu depois a escala: 1:3500 em A1.** Num scan de 2338 px isso
> prevê **1,259 m/px**. Medida outra vez com a ponta certa, a banda dá **1,263
> m/px — 0,3 % de desvio**. O desenho **está** à escala declarada.

O QUE FICA VERDADEIRO, e é o oposto do que eu escrevi
------------------------------------------------------
Levando ao terreno a semelhança tirada de dois pontos da banda escolhidos por
**forma** (o início do sector G e a última parcela), as válvulas caem assim:

    v17, v16, v15, v14      dentro, ou a 5 a 18 m das parcelas de kiwi
    v9, v10, v8, v7, v6     a 61 a 128 m, com deriva a crescer para oeste
    v1 a v5 (lobo B1)       a 155 a 379 m

Ou seja: **a escala está certa e a banda quase fecha**; o que não fecha é o
**lobo do B1**, que está desenhado deslocado em relação à banda — o que é o que
um desenhador faz quando tem de meter um lobo distante e a banda toda na mesma
folha A1.

Isso não é «sem escala»: é **duas plantas correctas com um desencontro de
implantação entre elas**, e resolve-se com uma transformação por bloco, não com
uma global. É trabalho por fazer, e é agora a via mais promissora.

A LIÇÃO, que é a mesma de sempre
--------------------------------
Duas vezes seguidas o resíduo do ajuste foi **a minha leitura**, não os dados:
primeiro uma segmentação automática que via 8 de 13 bandas, depois uma ponta
lida 600 px ao lado. E na terceira tentativa escolhi feições no desenho por
«mais à esquerda / mais em baixo» e casei-as com extremos em **UTM** — com o
desenho rodado 22°, não são os mesmos pontos.

**Um resíduo muito maior do que o erro de medição declarado é um sinal de que
o erro está em quem mede.** Eu li-o como sinal sobre o desenho, e escrevi uma
conclusão sobre o desenho. Era sobre mim.
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
