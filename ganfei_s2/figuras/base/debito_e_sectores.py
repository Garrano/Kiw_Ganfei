# -*- coding: utf-8 -*-
"""As letras A–N cobrem só a banda, e o débito prova-o.

DE ONDE VEIO ESTA PERGUNTA
--------------------------
O gestor leu «sector M» na válvula 16 e propôs 17=A, 16=M, 15=N, 14=B, 13=D.
Eu tinha lido G, F, E, D nas válvulas 6, 7, 8 e 9. Duas coisas não batiam: o
13=D dele colide com o 9=D meu, e as 13 letras têm de chegar para 17 válvulas.

Havia uma quantidade por usar. O esquema traz, na sua própria legenda, o
**débito de cada sector impresso** em m³ — treze números que nada têm a ver com
a leitura das etiquetas. Se a atribuição estiver certa, o débito de cada bloco
tem de ser proporcional à sua área.

**É uma verificação independente da leitura**, e é a primeira coisa neste
ficheiro que não depende de conseguir ver texto de três píxeis.

> **RESSALVA POSTA A 04-09, e pode derrubar a conclusão principal.**
> Este ficheiro concluiu que as 13 letras A–N cobrem **só a banda**, e que o B1
> está fora do sistema de letras — apoiado em a dotação bater a 1,2 % nessa
> hipótese e falhar por 44,5 % na outra.
>
> Depois disso, o recorte `_esquema_rega/GRELHA_lobo.png`, lido a 04-09, mostra
> **etiquetas de sector impressas nas bandas do lobo do B1** — lê-se «sector H»
> junto à válvula 5. Se assim for, **as letras entram no B1 e a conclusão deste
> ficheiro cai**, e com ela o número de 38,0 m³/ha que serve de alvo à busca.
>
> O gestor leu, de forma independente, **4 = I** e **5 = H** — o que aponta no
> mesmo sentido. Está por confirmar, e enquanto não estiver **nada daqui entra
> em peça nenhuma**.

O QUE SE DECIDE, E O QUE NÃO
----------------------------
Decide-se **se as letras cobrem a exploração toda ou só a banda contígua** —
porque as duas hipóteses dão taxas de rega que diferem por 46 %, e a leitura
já feita distingue-as sem ambiguidade.

Não se decide a atribuição letra a letra: a busca deixa oito soluções quase
equivalentes. O que ela faz é dizer **qual a leitura que vale mais a pena
pedir a seguir** — a que separa as oito.

A RESSALVA, e vai à frente
--------------------------
Tudo o que sai daqui é **inferência aritmética**, não leitura. Uma letra que
esta busca proponha entra na carta a tracejado, como qualquer outra coisa
nossa. O que a busca certifica é o contrário: que a leitura G+F+E+D **já feita**
é coerente com um número que não a produziu.
"""
import io
import json
import os
from itertools import combinations

AQUI = os.path.dirname(os.path.abspath(__file__))

# débito dos 13 sectores impressos, da caixa «Débito dos Sectores» do esquema
DEB = {"A": 65.0, "B": 85.0, "C": 90.5, "D": 95.8, "E": 87.6, "F": 79.1,
       "G": 99.9, "H": 91.5, "I": 78.5, "J": 71.6, "L": 55.8, "M": 55.3,
       "N": 82.7}
# áreas declaradas pelo gestor, e número de válvulas por bloco
AREA = {"B1": 12.63, "B2": 9.65, "Erica Novo": 4.87, "B3": 9.01, "B4": 3.78}
NV = {"B1": 5, "B2": 4, "Erica Novo": 2, "B3": 4, "B4": 2}
LIDO_B2 = ["G", "F", "E", "D"]          # válvulas 6, 7, 8, 9

TOT = sum(DEB.values())
BANDA = sum(a for b, a in AREA.items() if b != "B1")
TUDO = sum(AREA.values())
print("débito total dos 13 sectores: %.1f m³" % TOT)
print()

# ── 1 · as letras cobrem tudo, ou só a banda? ───────────────────────────────
gfed = sum(DEB[k] for k in LIDO_B2)
taxa_b2 = gfed / AREA["B2"]
print("=" * 74)
print("H1 · as 13 letras cobrem a exploração toda   -> %.1f m³/ha" % (TOT / TUDO))
print("H2 · as 13 letras cobrem só a banda (v6-17)  -> %.1f m³/ha" % (TOT / BANDA))
print("-" * 74)
print("leitura já feita: B2 = G+F+E+D = %.1f m³ em %.2f ha = %.1f m³/ha"
      % (gfed, AREA["B2"], taxa_b2))
d1 = 100 * abs(taxa_b2 - TOT / TUDO) / (TOT / TUDO)
d2 = 100 * abs(taxa_b2 - TOT / BANDA) / (TOT / BANDA)
print("   desvio contra H1: %5.1f %%" % d1)
print("   desvio contra H2: %5.1f %%" % d2)
print()
vence = "H2" if d2 < d1 else "H1"
print("-> %s. %s" % (vence,
      "As letras param na banda; as válvulas 1 a 5 do B1 estão FORA do "
      "sistema de letras." if vence == "H2" else
      "As letras cobrem a exploração toda."))
print("   Bate com o B1 ter numeração de linha própria (149, 137, 156, 705),")
print("   que é outro sistema e já se sabia por outra via.")
print("=" * 74)

# ── 2 · o quarto sector do B2 é mesmo o D? ─────────────────────────────────
print()
alvo_b2 = AREA["B2"] * TOT / BANDA
gfe = sum(DEB[k] for k in ("G", "F", "E"))
print("a leitura do 9 é a mais fraca (a amostra de cor do 8 e do 9 deu a mesma")
print("banda). Que letra devia ser a quarta do B2, pelo débito?  alvo %.0f m³"
      % alvo_b2)
cand = sorted(((abs(gfe + DEB[k] - alvo_b2), k) for k in DEB
               if k not in ("G", "F", "E")))
for e, k in cand[:4]:
    print("   %s -> %.1f m³  (desvio %.1f %%)"
          % (k, gfe + DEB[k], 100 * e / alvo_b2))

# ── 3 · repartir as nove letras que sobram ──────────────────────────────────
print()
print("=" * 74)
print("as 9 letras que sobram, por Erica(2), B3(4), B4(2) — 1 letra fica sem válvula")
print("=" * 74)
resto = [k for k in DEB if k not in LIDO_B2]
alvo = {b: AREA[b] * TOT / BANDA for b in ("Erica Novo", "B3", "B4")}
sol = []
for e in combinations(resto, 2):
    r1 = [k for k in resto if k not in e]
    for b3 in combinations(r1, 4):
        r2 = [k for k in r1 if k not in b3]
        for b4 in combinations(r2, 2):
            s = {"Erica Novo": sum(DEB[k] for k in e),
                 "B3": sum(DEB[k] for k in b3),
                 "B4": sum(DEB[k] for k in b4)}
            erro = sum(abs(s[b] - alvo[b]) / alvo[b] for b in alvo) / 3
            sol.append((erro, e, b3, b4, [k for k in r2 if k not in b4]))
sol.sort()
print("%-7s %-10s %-18s %-10s %s" % ("erro", "Erica(2)", "B3(4)", "B4(2)", "sobra"))
for erro, e, b3, b4, sob in sol[:8]:
    print("%6.1f%% %-10s %-18s %-10s %s"
          % (100 * erro, "+".join(e), "+".join(b3), "+".join(b4), sob[0]))

# ── 4 · qual a leitura que separa as oito? ─────────────────────────────────
print()
print("=" * 74)
print("QUE LEITURA PEDIR A SEGUIR")
print("=" * 74)
top = sol[:8]
from collections import Counter
for bloco, idx in (("Erica Novo", 1), ("B3", 2), ("B4", 3)):
    c = Counter(tuple(sorted(s[idx])) for s in top)
    print("  %-11s %d combinações distintas nas 8 melhores: %s"
          % (bloco, len(c), " · ".join("+".join(k) for k in c)))
letras_erica = Counter(k for s in top for k in s[1])
print()
print("  o Erica Novo tem só duas válvulas (10 e 11) e aparece com %d "
      "combinações;" % len(Counter(tuple(sorted(s[1])) for s in top)))
print("  ler a etiqueta de UMA delas elimina a maior parte das soluções.")
print("  frequência das letras no Erica entre as 8 melhores: %s"
      % ", ".join("%s×%d" % (k, v) for k, v in letras_erica.most_common()))

json.dump(dict(
    debito=DEB, area=AREA, valvulas_por_bloco=NV,
    total_m3=TOT, area_banda_ha=BANDA, area_total_ha=TUDO,
    taxa_se_tudo=TOT / TUDO, taxa_se_banda=TOT / BANDA,
    leitura_b2=LIDO_B2, taxa_b2_lida=taxa_b2,
    desvio_h1_pct=d1, desvio_h2_pct=d2, hipotese_vencedora=vence,
    quarta_letra_b2=[dict(letra=k, desvio_pct=100 * e / alvo_b2)
                     for e, k in cand[:4]],
    melhores=[dict(erro_pct=100 * er, erica=list(e), b3=list(b3), b4=list(b4),
                   sobra=sob) for er, e, b3, b4, sob in sol[:8]],
    ressalva="a reparticao e INFERENCIA aritmetica, nao leitura. O que fica "
             "certificado e o inverso: a leitura G+F+E+D e coerente a 1,2 % "
             "com um numero que nao a produziu."),
    io.open(os.path.join(AQUI, "debito_e_sectores.json"), "w", encoding="utf-8"),
    indent=1, ensure_ascii=False)
print()
print("escrito debito_e_sectores.json")
