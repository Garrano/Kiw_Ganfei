# -*- coding: utf-8 -*-
"""P11 — CARTA-BASE DE GANFEI. O substrato, sem interpretação nenhuma.

A P10 argumenta. **Esta não.** É a folha onde as outras assentam: o terreno, a
água, o cadastro, e os cinco sectores com os nomes que o gestor lhes dá. Quem
quiser saber o que isto significa vai ao `FIGURAS_ABSTRACTS.md`; a prancha só
mostra o que lá está.

PARA QUE SERVE
--------------
Todas as vistas seguintes — esquema de rega, tipo de solo, porta-enxertos,
datas de plantação, manchas de mortalidade — desenham-se **por cima desta**,
importando o `carta_base.py`. Assim a geometria, a projecção e os nomes são os
mesmos em todas, e duas figuras nunca dizem coisas diferentes por estarem
desenhadas de maneiras diferentes.

OS NOMES
--------
**B1 · B2 · Erica Novo · B3 · B4.** São os do gestor. Vêm da tabela de válvulas
dele e dos boletins A2, que trazem o código de bloco escrito. Este processo
usou durante semanas «foco OESTE» e «foco ESTE» — que são unidades de análise,
não sectores — e o resultado foi o B1 desaparecer de figura após figura.
**A carta-base existe para que isso não volte a acontecer.**

A PRÉ-VOO
---------
**1 · pergunta.** Onde ficam os cinco sectores do gestor, e o que há por baixo?
**3 · fronteira derivada do sinal?** Não. MDT LiDAR, parcelário IFAP, tabela de
válvulas. Nada aqui sai de um índice de vegetação.
**5 · instrumento independente.** A partição por válvula foi confrontada com as
áreas que o gestor declara — desvio máximo 17,7 %, critério pré-registado 25 %.
**11 · a janela contém o que a frase abrange?** Sim, e foi por isso que se
alargou: a caixa da C1 cortava o B1 fora. Esta cobre os cinco sectores.
"""
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "base"))
from carta_base import Base, PAPEL, TINTA, TINTA2, TINTA3, virg   # noqa: E402

b = Base()
fig, ax, axl = b.figura(larg=16.0)

b.terreno(ax)
b.cadastro(ax)
b.sectores(ax)
b.valvulas(ax)
b.rotulos(ax)
b.toponimos(ax)
b.moldura(ax)

# ── cartela ─────────────────────────────────────────────────────────────────
fig.text(0.035, 0.972, "GANFEI · CARTA-BASE", fontsize=21, weight="bold",
         color=TINTA, va="top", ha="left")
fig.text(0.035, 0.930,
         "Emparcelamento de Ganfei, Valença  ·  os cinco sectores com os nomes "
         "do gestor, sobre o terreno e a drenagem",
         fontsize=10.5, color=TINTA2, va="top", ha="left")

tot = sum(b.areas.values())
sp = b.sem_posicao()
fig.text(0.955, 0.972,
         "%s ha na partição  ·  5 sectores  ·  %d de 17 válvulas posicionadas"
         % (virg(tot), 17 - len(sp)),
         fontsize=10.5, color=TINTA2, va="top", ha="right")
fig.text(0.955, 0.938, "ETRS89 / UTM 29N (EPSG:32629)  ·  quadrícula 250 m",
         fontsize=8.2, color=TINTA3, va="top", ha="right")

b.legenda(
    axl,
    nota="FONTES   MDT LiDAR 50 cm, DGT (7 folhas, EPSG:3763, reamostrado a 1 m).\n"
         "Parcelário IFAP 2025, cultura 124 (KIWI). Tabela de válvulas e nomes\n"
         "de sector do gestor; boletins A2 para os códigos de bloco.\n\n"
         "SECTORES   Partição por válvula mais próxima dentro da área de kiwi;\n"
         "o B1 é a união das suas seis parcelas do IFAP. A partição foi testada\n"
         "contra as áreas declaradas pelo gestor: desvio máximo 17,7 % (B2),\n"
         "critério de rejeição fixado em 25 % antes de correr.\n\n"
         "ESCOAMENTO   pysheds sobre o MDT de 1 m, com resolve_flats. Sem esse\n"
         "passo a acumulação máxima cai por um factor de 70 neste terreno.\n\n"
         "Gerado por P11_base_ganfei.py  ·  " + time.strftime("%Y-%m-%d"))

fora = os.path.join(AQUI, "P11_base_ganfei.png")
fig.savefig(fora, dpi=200)
fig.savefig(fora.replace(".png", ".pdf"))
print("escrita %s" % fora)
print("sectores: %s" % ", ".join("%s %.1f ha" % (k, v) for k, v in b.areas.items()))
