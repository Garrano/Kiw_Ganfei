# -*- coding: utf-8 -*-
"""C3 · o teste T1 que o adversario da C2 exigiu antes de a C3 arrancar.

O `CAMADA_2_ADVERSARIO.md`, parte 4, item T1, escreve:

  «REF & do, REF & de, REF & c2_05_defice_2026.npy, REF & c2_05_novo_m2.npy ...
   Se algum destes quatro numeros nao for zero, esta camada volta para tras
   inteira.»

E a condicao 2 do veredicto manda correr T1 antes de a C3 arrancar. Nao havia
saida de T1 em disco. Corre-se aqui, e mede-se a consequencia — nao basta dizer
que nao e zero, e preciso dizer quanto pesa.

Metodo: recalcular a serie da referencia sistematica (a) tal como esta e (b)
depois de retirar as celulas que caem dentro dos discos de 90 m dos dois focos,
e comparar a descida de 2024 para 2026. Se a descida encolher ao retirar as
celulas, entao parte do «a referencia esta a cair» e o proprio acontecimento
dentro do denominador.
"""
import json
import os
import sys

import numpy as np
import rasterio

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import (DATAS, LIMIAR, carrega_mascaras, discos_dos_focos,
                         mapa_defice)

RAIZ = r"C:\Users\Jackster2\Downloads\ganfei_s2"
C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
OUT = os.path.dirname(os.path.abspath(__file__))

masc, _ = carrega_mascaras()
pomar, saudavel = masc["pomar"], masc["saudavel"]
defice26 = np.load(os.path.join(C2, "c2_05_defice_2026.npy"))
novo = np.load(os.path.join(C2, "c2_05_novo_m2.npy"))
do, de = discos_dos_focos(pomar, raio=90.0)

# --------------------------------------------------- T1, os quatro numeros
T1 = {"REF_e_disco_OESTE": int((saudavel & do).sum()),
      "REF_e_disco_ESTE": int((saudavel & de).sum()),
      "REF_e_defice_2026": int((saudavel & defice26).sum()),
      "REF_e_novo_M2": int((saudavel & novo).sum()),
      "REF_total": int(saudavel.sum())}
print("T1 — os quatro numeros que o adversario pediu:")
for k in ("REF_e_disco_OESTE", "REF_e_disco_ESTE", "REF_e_defice_2026", "REF_e_novo_M2"):
    print(f"   {k:20s} = {T1[k]:3d}   ({100.0*T1[k]/T1['REF_total']:.1f} % das 110)")
print(f"   nenhum e zero. o adversario disse que isto manda a camada 2 para tras.")

# ------------------------------------- a referencia limpa dos dois focos
ref_suja = saudavel
ref_limpa = saudavel & ~do & ~de
print(f"\nreferencia declarada : {int(ref_suja.sum())} celulas")
print(f"referencia sem focos : {int(ref_limpa.sum())} celulas "
      f"({int((ref_suja & (do | de)).sum())} retiradas)")

nd = {d: rasterio.open(os.path.join(RAIZ, "sentinel", "%s.tif" % d)).read(1)
      for d in DATAS}

print("\ndata        ref declarada  ref sem focos   diferenca")
serie = {}
for d in DATAS:
    a = float(np.nanmedian(nd[d][ref_suja]))
    b = float(np.nanmedian(nd[d][ref_limpa]))
    serie[d] = {"ref_declarada": round(a, 4), "ref_sem_focos": round(b, 4),
                "dif": round(b - a, 4)}
    print(f"{d}   {a:.4f}        {b:.4f}       {b-a:+.4f}")

q24s, q26s = serie["2024-07-22"]["ref_declarada"], serie["2026-07-27"]["ref_declarada"]
q24l, q26l = serie["2024-07-22"]["ref_sem_focos"], serie["2026-07-27"]["ref_sem_focos"]
print(f"\ndescida 2024->2026 com a referencia declarada : {q26s - q24s:+.4f}")
print(f"descida 2024->2026 com a referencia sem focos : {q26l - q24l:+.4f}")
print(f"quanto da descida vem das celulas dentro dos focos: "
      f"{(q26l - q24l) - (q26s - q24s):+.4f}")

# ---------------------- consequencia no mapa de defice e nas areas
print("\nconsequencia nas areas (limiar 0,05, sem abertura para ser directo):")
areas = {}
for d in DATAS:
    rs = float(np.nanmedian(nd[d][ref_suja]))
    rl = float(np.nanmedian(nd[d][ref_limpa]))
    ms = mapa_defice(nd[d], pomar, rs)
    ml = mapa_defice(nd[d], pomar, rl)
    areas[d] = {"ha_ref_declarada": round(int(ms.sum()) / 100.0, 2),
                "ha_ref_sem_focos": round(int(ml.sum()) / 100.0, 2)}
    print(f"   {d}  {areas[d]['ha_ref_declarada']:5.2f} ha  ->  "
          f"{areas[d]['ha_ref_sem_focos']:5.2f} ha")

res = {"T1": T1,
       "ref_declarada_celulas": int(ref_suja.sum()),
       "ref_sem_focos_celulas": int(ref_limpa.sum()),
       "serie_mediana": serie,
       "descida_2024_2026_declarada": round(q26s - q24s, 4),
       "descida_2024_2026_sem_focos": round(q26l - q24l, 4),
       "areas_defice": areas,
       "leitura": ("Os quatro numeros de T1 nao sao zero. A referencia "
                   "sistematica contem celulas dos dois discos e do mapa de "
                   "defice de 2026. O sentido do vies e conservador — a "
                   "referencia cai com o acontecimento e as magnitudes ficam "
                   "amortecidas — mas o denominador nao esta limpo.")}
with open(os.path.join(OUT, "c3_08_controlo_referencia.json"), "w",
          encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print("\nescrito c3_08_controlo_referencia.json")
