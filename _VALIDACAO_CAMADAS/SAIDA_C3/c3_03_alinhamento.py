"""C3 · tarefa 1 (fecho) — alinhamento de sequencia entre os dois livros.

A c3_02 mostrou: 27 ficheiros de origem nos dois, iguais; nove boletins de solo
com 11 linhas no EN e 12 no PT; divergencia de `Value` a comecar na linha 93.
A hipotese e insercao (nove linhas novas espalhadas), nao reescrita. Testa-se
com alinhamento de sequencia sobre a chave (ficheiro || organismo), e depois
compara-se `Value` par a par nas linhas efectivamente emparelhadas.
"""
import difflib
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


def chave(df):
    return (df["Source_File"].astype(str).str.strip() + "||"
            + df["Organism_Parameter"].astype(str).str.strip()).tolist()


ken, kpt = chave(en), chave(pt)
sm = difflib.SequenceMatcher(a=ken, b=kpt, autojunk=False)
pares, so_en, so_pt = [], [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        pares += [(i, j) for i, j in zip(range(i1, i2), range(j1, j2))]
    else:
        so_en += list(range(i1, i2))
        so_pt += list(range(j1, j2))

print("linhas emparelhadas :", len(pares))
print("so no EN            :", len(so_en))
print("so no PT            :", len(so_pt))

print("\nas linhas que existem so no PT:")
for j in so_pt:
    r = pt.iloc[j]
    print(f"  PT linha {j:3d} (ID {int(r['Record_ID'])}) | "
          f"{str(r['Source_File'])[:34]:34s} | {str(r['Organism_Parameter'])[:26]:26s} | "
          f"{str(r['Value'])[:44]}")
if so_en:
    print("\nas linhas que existem so no EN:")
    for i in so_en:
        r = en.iloc[i]
        print(f"  EN linha {i:3d} (ID {int(r['Record_ID'])}) | "
              f"{str(r['Source_File'])[:34]:34s} | {str(r['Organism_Parameter'])[:26]:26s} | "
              f"{str(r['Value'])[:44]}")

# --- nas linhas emparelhadas, o Value bate? ---
dif_val, dif_data, dif_res = [], [], []
for i, j in pares:
    a, b = en.iloc[i], pt.iloc[j]
    if str(a["Value"]).strip() != str(b["Value"]).strip():
        dif_val.append((int(a["Record_ID"]), int(b["Record_ID"]),
                        str(a["Value"]), str(b["Value"])))
    if str(a["Sample_Date"]).strip() != str(b["Sample_Date"]).strip():
        dif_data.append((int(a["Record_ID"]), int(b["Record_ID"]),
                         str(a["Sample_Date"]), str(b["Sample_Date"])))
    if str(a["Result"]).strip() != str(b["Result"]).strip():
        dif_res.append((int(a["Record_ID"]), int(b["Record_ID"]),
                        str(a["Result"]), str(b["Result"])))

print(f"\nemparelhadas com Value diferente      : {len(dif_val)} de {len(pares)}")
for t in dif_val[:15]:
    print(f"   EN{t[0]:>4}/PT{t[1]:>4}  EN={t[2][:46]:46s} PT={t[3][:46]}")
print(f"\nemparelhadas com Sample_Date diferente: {len(dif_data)} de {len(pares)}")
for t in dif_data[:12]:
    print(f"   EN{t[0]:>4}/PT{t[1]:>4}  EN={t[2][:30]:30s} PT={t[3][:30]}")
print(f"\nemparelhadas com Result diferente     : {len(dif_res)} de {len(pares)}")
for t in dif_res[:12]:
    print(f"   EN{t[0]:>4}/PT{t[1]:>4}  EN={t[2][:40]:40s} PT={t[3][:40]}")

res = {
    "emparelhadas": len(pares), "so_EN": len(so_en), "so_PT": len(so_pt),
    "linhas_so_PT": [{"linha": int(j), "record_id": int(pt.iloc[j]["Record_ID"]),
                      "ficheiro": str(pt.iloc[j]["Source_File"]),
                      "parametro": str(pt.iloc[j]["Organism_Parameter"]),
                      "valor": str(pt.iloc[j]["Value"])} for j in so_pt],
    "linhas_so_EN": [{"linha": int(i), "record_id": int(en.iloc[i]["Record_ID"]),
                      "ficheiro": str(en.iloc[i]["Source_File"]),
                      "parametro": str(en.iloc[i]["Organism_Parameter"]),
                      "valor": str(en.iloc[i]["Value"])} for i in so_en],
    "n_value_divergente": len(dif_val),
    "n_sample_date_divergente": len(dif_data),
    "n_result_divergente": len(dif_res),
    "value_divergente": dif_val,
    "sample_date_divergente": dif_data,
    "result_divergente": dif_res,
}
(OUT / "c3_03_alinhamento.json").write_text(
    json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nescrito c3_03_alinhamento.json")
