"""C3 · perfil do livro-fonte (PT, 221 registos) antes de georreferenciar.

Lista o que la esta: tipos de documento, matrizes, categorias de ensaio,
talhoes declarados, graus de confianca de localizacao, laboratorios, datas.
Nao interpreta. Serve para a tarefa 2 e para a tarefa 8 (proveniencia duvidosa).
"""
import json
from pathlib import Path

import pandas as pd

DL = Path(r"C:\Users\Jackster2\Downloads")
OUT = Path(__file__).parent

EN_COLS = ['Record_ID', 'Source_File', 'Doc_Type', 'Report_No', 'Client_Titular',
           'Terrain_Block_Parcel', 'Parish_Municipality', 'Parcelario_No',
           'Sample_Date', 'Received_Date', 'Result_Date', 'Matrix',
           'Test_Category', 'Method', 'Organism_Parameter', 'Result', 'Value',
           'Unit', 'Interpretation', 'Lab_Provider', 'Location_Confidence',
           'Notes']

pt = pd.read_excel(DL / "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx",
                   sheet_name="Registo Principal")
pt.columns = EN_COLS
pt.to_csv(OUT / "c3_04_registo_principal.csv", index=False, encoding="utf-8")

for col in ["Doc_Type", "Matrix", "Test_Category", "Terrain_Block_Parcel",
            "Location_Confidence", "Lab_Provider", "Client_Titular",
            "Parish_Municipality", "Sample_Date", "Parcelario_No"]:
    print("\n=== %s ===" % col)
    vc = pt[col].astype(str).value_counts(dropna=False)
    for k, v in vc.items():
        print(f"  {v:4d}  {k[:118]}")

print("\n=== ficheiros de origem x talhao declarado ===")
t = pt.groupby([pt["Source_File"].astype(str),
                pt["Terrain_Block_Parcel"].astype(str),
                pt["Location_Confidence"].astype(str)]).size()
for (f, b, c), n in t.items():
    print(f"  {n:4d}  {f[:46]:46s} | {b[:26]:26s} | {c[:34]}")

res = {c: {str(k): int(v) for k, v in
           pt[c].astype(str).value_counts(dropna=False).items()}
       for c in ["Doc_Type", "Matrix", "Test_Category",
                 "Terrain_Block_Parcel", "Location_Confidence",
                 "Lab_Provider", "Client_Titular", "Parish_Municipality"]}
res["n_registos"] = len(pt)
(OUT / "c3_04_perfil.json").write_text(
    json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nescrito c3_04_perfil.json e c3_04_registo_principal.csv")
