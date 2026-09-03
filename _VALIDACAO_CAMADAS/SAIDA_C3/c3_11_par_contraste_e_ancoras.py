# -*- coding: utf-8 -*-
"""C3 · o par de contraste v8/B2 contra v10-v11 (Erica Novo), e as ancoras.

A adenda de LiDAR manda concentrar a biologia no v8/B2 e no seu par de contraste
v10-v11, que estao no mesmo bloco geografico, na mesma origem de agua, e
MELHORARAM. Aqui poe-se lado a lado tudo o que a biologia tem sobre os dois.

E reportam-se as quantidades-ancora do CONTROLOS.md mais as que as camadas
abaixo fixaram, mais as tres da C3.
"""
import json
import os

import numpy as np
import pandas as pd

DL = r"C:\Users\Jackster2\Downloads"
C1 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C1"
OUT = os.path.dirname(os.path.abspath(__file__))

col = pd.read_csv(os.path.join(OUT, "c3_07_registos_colocados.csv"))
with open(os.path.join(OUT, "c3_07_georreferenciacao.json"), encoding="utf-8") as f:
    GEO = json.load(f)

print("=" * 96)
print("O PAR DE CONTRASTE: B2 (v6-v9, contem o FOCO OESTE na v8) x Erica Novo (v10-v11)")
print("=" * 96)
for nome in ("B2", "Erica Novo"):
    u = GEO["por_bloco"][nome]
    print(f"\n{nome}  (v{'|'.join(u['valvulas'])})  {u['ha']:.2f} ha")
    print(f"   defice 2026 {u['pct_defice_2026']:.1f} % | declinio novo M2 "
          f"{u['pct_novo_M2']:.1f} % | chao lavrado {u['pct_nu2021_chao_lavrado']:.1f} %")
    print(f"   distancia ao FOCO OESTE {u['d_foco_OESTE_m']:.0f} m, ao FOCO ESTE "
          f"{u['d_foco_ESTE_m']:.0f} m")
    sub = col[col["unidade"] == nome]
    subv = col[col["unidade"].isin([f"v{k}" for k in u["valvulas"]])]
    print(f"   registos colocados no bloco: {len(sub)} | nas valvulas: {len(subv)}"
          f" ({sorted(set(subv['unidade']))})")

print("\n--- o que a biologia tem, lado a lado ---")
biol = col[col["Doc_Type"].astype(str).str.contains("Nematologia|Fitopatologia", na=False)]
for nome, unids in (("B2 / v7", ["v7"]), ("Erica Novo", ["Erica Novo"])):
    s = biol[biol["unidade"].isin(unids)]
    print(f"\n{nome}: {len(s)} registos de nematologia/fitopatologia")
    for _, r in s.iterrows():
        print(f"   {str(r['Sample_Date'])[:10]} {str(r['Matrix'])[:6]:6s} "
              f"{str(r['Organism_Parameter'])[:34]:34s} {str(r['Result'])[:24]}")

print("\n--- quimica de solo dos dois (dos nove boletins colocados pela C1) ---")
solo = pd.read_csv(os.path.join(C1, "c1_06_solo_colocado.csv"))
for _, r in solo.iterrows():
    if r["bloco"] in ("B2", "Erica Novo"):
        print(f"   {r['amostra'][:34]:34s} {r['bloco']:<11s} conf={r['confianca']:<16s}"
              f" pH {r['pH']:.1f} CaO {r['CaO']:7.1f} MgO {r['MgO']:6.1f} "
              f"K2O {r['K2O']:6.1f} textura {r['textura']}")
cao_b2 = [264.0, 505.0]
cao_en = [879.0, 1200.0]
print(f"\n   CaO: B2/V7 {cao_b2} · Erica Novo {cao_en}")
raz = min(cao_en) / max(cao_b2)
print(f"   razao entre os extremos mais proximos: {raz:.1f}x")
print(f"   a C1 S9 fixa que 'nenhuma diferenca quimica abaixo de um factor de 2 e")
print(f"   interpretavel com estes dados'. Esta fica em {raz:.1f}x — ABAIXO do limiar.")
print(f"   Logo o contraste de CaO entre o par NAO e interpretavel, e a leitura")
print(f"   que o compara pelas medias (382 contra 1040) escolhe o par de valores")
print(f"   mais favoravel. Com n = 2 de cada lado, e com um factor de 15 dentro do")
print(f"   B1 como escala do ruido, isto nao passa.")

# ------------------------------------------------------------- ancoras
print("\n" + "=" * 96)
print("QUANTIDADES-ANCORA")
print("=" * 96)
u = GEO["unidades_referencia"]
ancoras = [
    ("AOI", "529950, 4654600, 531950, 4655600", "529950, 4654600, 531950, 4655600", "igual"),
    ("poligono pomar (ha)", "30,31", f"{u['poligono pomar']['ha']:.2f}".replace(".", ","), ""),
    ("referencia sistematica (ha / celulas)", "1,10 / 110",
     f"{u['referencia sistematica']['ha']:.2f} / {u['referencia sistematica']['celulas']}".replace(".", ","), ""),
    ("banda contigua (ha)", "27,30",
     f"{sum(b['ha'] for b in GEO['por_bloco'].values()):.2f}".replace(".", ","),
     "a minha e a area DENTRO do poligono pomar; a da G35 e a area da tabela do gestor"),
    ("total da tabela do gestor (ha)", "44,93", "nao recalculado", "documental, fora da minha camada"),
    ("chao lavrado nu2021 (ha)", "1,67", f"{u['chao lavrado nu2021']['ha']:.2f}".replace(".", ","), ""),
    ("defice de 2026 (ha)", "7,86", "7,86", "lido de c2_05_defice_2026.npy, nao recalculado"),
    ("declinio novo M2 (ha)", "3,58", "3,58", "lido de c2_05_novo_m2.npy, nao recalculado"),
]
import numpy as _np
d26 = _np.load(os.path.join(r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2",
                            "c2_05_defice_2026.npy"))
nm2 = _np.load(os.path.join(r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2",
                            "c2_05_novo_m2.npy"))
ancoras[6] = ("defice de 2026 (ha)", "7,86", f"{int(d26.sum())/100:.2f}".replace(".", ","), "")
ancoras[7] = ("declinio novo M2 (ha)", "3,58", f"{int(nm2.sum())/100:.2f}".replace(".", ","), "")

com = col["classe_posicao"].isin(["COLOCADO", "COLOCADO-BLOCO", "INFERIDO", "AMBIGUO"])
orgs = json.load(open(os.path.join(OUT, "c3_09_organismos.json"), encoding="utf-8"))

# taxa distintos = nome do organismo sem o sufixo de matriz entre parenteses
import re as _re
taxa = sorted({_re.sub(r"\s*\([^)]*\)\s*$", "", s["organismo"]).strip()
               for s in orgs["organismos"]})
print(f"\nlinhas organismo x matriz : {len(orgs['organismos'])}")
print(f"taxa distintos            : {len(taxa)}")
for t in taxa:
    print("   ·", t)

# amostras fisicas colocadas (um ficheiro de origem = uma submissao)
pc = col[com]
print(f"\namostras fisicas colocadas (ficheiros de origem distintos): "
      f"{pc['Source_File'].nunique()}")
print(f"datas de amostragem dessas amostras: "
      f"{sorted(set(pc['Sample_Date'].astype(str)))}")

ancoras += [
    ("registos (livro fonte PT)", "212 / 222 declarados", str(len(col)), "ver CORRIGIDO"),
    ("registos com posicao na banda contigua", "—", str(int(com.sum())), "novo da C3"),
    ("registos sem posicao", "—", str(int((~com).sum())), "novo da C3"),
    ("linhas organismo x matriz", "26 declarados", str(len(orgs["organismos"])), "ver CORRIGIDO"),
]
print(f"{'ancora':<42s} {'declarado':>24s} {'obtido':>12s}")
for a, d, o, n in ancoras:
    print(f"{a:<42s} {d:>24s} {o:>12s}  {n}")

with open(os.path.join(OUT, "c3_11_ancoras.json"), "w", encoding="utf-8") as f:
    json.dump({"ancoras": [{"ancora": a, "declarado": d, "obtido": o, "nota": n}
                           for a, d, o, n in ancoras],
               "CaO_B2_V7": cao_b2, "CaO_Erica_Novo": cao_en},
              f, indent=1, ensure_ascii=False)
print("\nescrito c3_11_ancoras.json")
