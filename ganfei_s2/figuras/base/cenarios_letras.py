# -*- coding: utf-8 -*-
"""Três leituras das etiquetas, postas a competir pelo débito.

O QUE MUDOU
-----------
O `debito_e_sectores.py` concluiu que as 13 letras cobriam só a banda, e que o
B1 estava fora do sistema. Essa conclusão apoiava-se **inteiramente** na minha
leitura B2 = G+F+E+D.

O gestor leu depois **4 = I** e **5 = H** — válvulas do B1. Se estiver certo, as
letras entram no B1 e aquela conclusão cai. Também leu **9 = E** onde eu li D, e
propôs **8 = L**.

E há um padrão nas leituras dele que eu não tinha: **I, H, G, F nas válvulas 4,
5, 6, 7** é descendente e consecutivo. Junto com o meu E, D nas 8 e 9, dá uma
série única I→D ao longo de seis válvulas seguidas.

O TESTE
-------
O esquema dá o débito de cada sector. Se a atribuição estiver certa, a **dotação
— m³ por hectare — tem de ser parecida entre blocos**, porque um sistema de rega
projectado de uma vez não rega um bloco a metade do outro sem razão.

Mede-se a **dispersão relativa** da dotação entre os cinco blocos. A leitura
certa é a que a minimiza. É um critério único, escrito antes de correr, e
aplica-se igual aos três cenários.

O QUE ISTO NÃO DECIDE
---------------------
Não decide letra a letra. Decide **qual das leituras é coerente com um número
que nenhuma delas usou** — e, sobretudo, se o B1 está dentro ou fora do sistema
de letras, que é a pergunta que muda a estrutura toda.
"""
import io
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DEB = {"A": 65.0, "B": 85.0, "C": 90.5, "D": 95.8, "E": 87.6, "F": 79.1,
       "G": 99.9, "H": 91.5, "I": 78.5, "J": 71.6, "L": 55.8, "M": 55.3,
       "N": 82.7}
AREA = {"B1": 12.63, "B2": 9.65, "Erica Novo": 4.87, "B3": 9.01, "B4": 3.78}
BLOCO = {}
for b, vs in (("B1", (1, 2, 3, 4, 5)), ("B2", (6, 7, 8, 9)),
              ("Erica Novo", (10, 11)), ("B3", (12, 13, 14, 15)),
              ("B4", (16, 17))):
    for v in vs:
        BLOCO[v] = b

CENARIOS = {
 "S1 · a minha leitura, letras só na banda": {
     6: "G", 7: "F", 8: "E", 9: "D"},
 "S2 · a leitura do gestor tal como veio": {
     4: "I", 5: "H", 6: "G", 7: "F", 8: "L", 9: "E",
     13: "D", 14: "B", 15: "N", 16: "M", 17: "A"},
 "S3 · série descendente I→A, v4 a v12": {
     4: "I", 5: "H", 6: "G", 7: "F", 8: "E", 9: "D",
     10: "C", 11: "B", 12: "A", 14: "N", 15: "M", 16: "L", 17: "J"},
}


def avalia(nome, atrib):
    porbloco = {}
    for v, l in atrib.items():
        porbloco.setdefault(BLOCO[v], []).append(l)
    usadas = sorted(atrib.values())
    dup = [l for l in set(usadas) if usadas.count(l) > 1]
    print("=" * 78)
    print(nome)
    print("=" * 78)
    if dup:
        print("  ** letra repetida: %s — impossível" % ", ".join(dup))
    print("  %-12s %-22s %8s %8s %9s" % ("bloco", "letras", "m³", "ha", "m³/ha"))
    dot = {}
    for b in ("B1", "B2", "Erica Novo", "B3", "B4"):
        ls = sorted(porbloco.get(b, []))
        if not ls:
            print("  %-12s %-22s %8s %8.2f %9s"
                  % (b, "— sem letra —", "—", AREA[b], "—"))
            continue
        m3 = sum(DEB[l] for l in ls)
        dot[b] = m3 / AREA[b]
        print("  %-12s %-22s %8.1f %8.2f %9.1f"
              % (b, "+".join(ls), m3, AREA[b], dot[b]))
    sobra = sorted(set(DEB) - set(atrib.values()))
    print("  letras por atribuir: %s" % (", ".join(sobra) if sobra else "nenhuma"))
    v = np.array(list(dot.values()))
    cv = 100 * v.std(ddof=0) / v.mean() if len(v) > 1 else float("nan")
    amp = v.max() / v.min() if len(v) > 1 else float("nan")
    print("  -> dispersão da dotação: CV %.1f %%   ·   máx/mín %.2f×"
          % (cv, amp))
    print()
    return dict(nome=nome, dotacao={k: round(x, 1) for k, x in dot.items()},
                cv_pct=round(float(cv), 1), amplitude=round(float(amp), 2),
                sobra=sobra, repetidas=dup)


print("critério, escrito antes de correr: vence a leitura com MENOR dispersão")
print("relativa da dotação (m³/ha) entre blocos. Um sistema projectado de uma")
print("vez não rega um bloco a metade do outro sem razão declarada.")
print()
res = [avalia(k, v) for k, v in CENARIOS.items()]
val = [r for r in res if not r["repetidas"] and len(r["dotacao"]) > 1]
val.sort(key=lambda r: r["cv_pct"])
print("=" * 78)
print("ORDENAÇÃO")
print("=" * 78)
for r in val:
    print("  CV %5.1f %%  máx/mín %.2f×   %s" % (r["cv_pct"], r["amplitude"], r["nome"]))
print()
print("NOTA: o S1 só tem um bloco com letras, portanto não tem dispersão para")
print("medir — não compete aqui. O que ele afirmava (letras só na banda)")
print("cai assim que UMA letra for confirmada no B1.")

json.dump(dict(criterio="menor dispersão relativa da dotação entre blocos",
               cenarios=res),
          io.open(os.path.join(AQUI, "cenarios_letras.json"), "w",
                  encoding="utf-8"), indent=1, ensure_ascii=False)
print()
print("escrito cenarios_letras.json")
