# -*- coding: utf-8 -*-
"""Gancho SessionStart — injecta o que não pode ser esquecido no arranque.

PORQUE SÃO DOIS FICHEIROS E NÃO UM
-----------------------------------
O `ANTES_DE_COMECAR.md` diz **como** trabalhar: a pré-voo, as condições do
portão, a taxonomia das retiradas. Chega para não repetir um *método* errado.

Não chega para não repetir um *trabalho* já feito. A 04-09-2026 re-derivei, num
turno, a análise do B1 e o teste da rede de rega — este último um estudo de onze
cenas com critério pré-registado, refutado duas vezes. A pré-voo estava
carregada e não o impediu, porque a pré-voo é sobre método.

O `HIPOTESES_FECHADAS.md` diz **o que já foi tentado**. E tem de vir por aqui
porque a triagem é cega ao negativo por construção: classifica como corrente o
que sustenta um facto certificado, e uma hipótese refutada não sustenta facto
nenhum, portanto some.

Se um destes ficheiros faltar, isso é dito em vez de passar em silêncio — uma
ausência tratada como aprovação é o defeito que este projecto mais repetiu.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
FICHEIROS = [
    ("ANTES DE COMEÇAR — como trabalhar", "ANTES_DE_COMECAR.md"),
    ("HIPÓTESES FECHADAS — o que já foi tentado", "HIPOTESES_FECHADAS.md"),
    ("CLÁUSULAS — porque os padrões se repetiram, e o que os trava",
     "CLAUSULAS.md"),
]

partes = []
for titulo, nome in FICHEIROS:
    p = os.path.join(AQUI, nome)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            partes.append("=" * 78 + "\n" + titulo + "\n" + "=" * 78 + "\n\n"
                          + f.read())
    else:
        partes.append("*** EM FALTA: %s — o arranque está incompleto e isso "
                      "não é aprovação. ***" % nome)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "\n\n".join(partes)}}))
