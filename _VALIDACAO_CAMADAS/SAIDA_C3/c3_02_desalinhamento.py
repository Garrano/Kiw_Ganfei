"""C3 · tarefa 1 (continuacao) — a natureza da divergencia entre os dois livros.

A c3_01 mostrou que os IDs 1-212 sao comuns mas que 119 de 212 tem `Value`
diferente. Isso nao e traducao: e conteudo diferente no mesmo numero de registo.
Aqui pergunta-se se ha um desfasamento de linhas (a mesma informacao com IDs
deslocados) ou se sao de facto livros diferentes.
"""
import json
from pathlib import Path

import pandas as pd

DL = Path(r"C:\Users\Jackster2\Downloads")
OUT = Path(__file__).parent

en = pd.read_excel(DL / "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx",
                   sheet_name="Master Log")
pt = pd.read_excel(DL / "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx",
                   sheet_name="Registo Principal")
pt.columns = list(en.columns)

# 1 · o conjunto de VALORES e o mesmo, so que noutra ordem?
ven = en["Value"].astype(str).str.strip()
vpt = pt["Value"].astype(str).str.strip()
sen, spt = set(ven), set(vpt)
print("valores distintos EN:", len(sen), " PT:", len(spt))
print("valores EN que NAO existem em lado nenhum do PT:", len(sen - spt))
print("valores PT que NAO existem em lado nenhum do EN:", len(spt - sen))

# 2 · procurar desfasamento: para cada deslocamento k, quantos Value batem?
print("\ndeslocamento k | Value coincidentes (de 212)")
melhor = (0, -1)
for k in range(-12, 13):
    n = 0
    for i in range(len(en)):
        j = i + k
        if 0 <= j < len(pt) and ven.iat[i] == vpt.iat[j]:
            n += 1
    if n > melhor[1]:
        melhor = (k, n)
    if abs(k) <= 12:
        print(f"   k = {k:+3d}      {n:4d}")
print("melhor deslocamento:", melhor)

# 3 · onde comeca a divergir? primeira linha com Value diferente
prim = None
for i in range(len(en)):
    if ven.iat[i] != vpt.iat[i]:
        prim = i
        break
print("\nprimeira linha (0-based) com Value diferente:", prim,
      "-> Record_ID", int(en['Record_ID'].iat[prim]))

# 4 · perfil por blocos de Source_File: o EN e o PT cobrem os mesmos ficheiros?
fen = set(en["Source_File"].dropna().astype(str))
fpt = set(pt["Source_File"].dropna().astype(str))
print("\nficheiros de origem distintos  EN:", len(fen), " PT:", len(fpt))
print("so em EN:", sorted(fen - fpt))
print("so em PT:", sorted(fpt - fen))

# 5 · contagem de registos por ficheiro de origem, lado a lado
cen = en["Source_File"].astype(str).value_counts()
cpt = pt["Source_File"].astype(str).value_counts()
tab = pd.DataFrame({"EN": cen, "PT": cpt}).fillna(0).astype(int)
tab["dif"] = tab["PT"] - tab["EN"]
tab = tab.sort_values("dif")
print("\ncontagem por ficheiro de origem (so onde difere):")
print(tab[tab["dif"] != 0].to_string())
print("\ntotal EN", int(tab['EN'].sum()), " total PT", int(tab['PT'].sum()))

# 6 · o mesmo ficheiro + o mesmo organismo dao o mesmo valor nos dois livros?
#     chave semantica em vez de Record_ID
def chave(df):
    return (df["Source_File"].astype(str).str.strip() + " || "
            + df["Organism_Parameter"].astype(str).str.strip())

en2 = en.assign(k=chave(en))
pt2 = pt.assign(k=chave(pt))
# o Organism_Parameter esta traduzido, portanto so a parte do ficheiro serve
print("\nchaves (ficheiro||organismo) coincidentes entre livros:",
      len(set(en2['k']) & set(pt2['k'])), "de", len(set(en2['k'])))

res = {
    "valores_distintos_EN": len(sen), "valores_distintos_PT": len(spt),
    "valores_EN_ausentes_do_PT": len(sen - spt),
    "valores_PT_ausentes_do_EN": len(spt - sen),
    "melhor_deslocamento_k": melhor[0], "coincidencias_no_melhor_k": melhor[1],
    "primeira_linha_divergente_0based": int(prim),
    "ficheiros_so_EN": sorted(fen - fpt), "ficheiros_so_PT": sorted(fpt - fen),
    "contagem_por_ficheiro": {i: {"EN": int(r.EN), "PT": int(r.PT)}
                              for i, r in tab.iterrows()},
}
(OUT / "c3_02_desalinhamento.json").write_text(
    json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nescrito c3_02_desalinhamento.json")
