"""C3 · tarefa 7 — Rosellinia de campo contra o negativo molecular, e as notas de campo.

Despeja integralmente os registos da nota de visita e todos os registos em que
'Rosellinia' aparece, nos dois livros, com todas as colunas.
"""
from pathlib import Path

import pandas as pd

DL = Path(r"C:\Users\Jackster2\Downloads")
OUT = Path(__file__).parent
EN_COLS = ['Record_ID', 'Source_File', 'Doc_Type', 'Report_No', 'Client_Titular',
           'Terrain_Block_Parcel', 'Parish_Municipality', 'Parcelario_No',
           'Sample_Date', 'Received_Date', 'Result_Date', 'Matrix',
           'Test_Category', 'Method', 'Organism_Parameter', 'Result', 'Value',
           'Unit', 'Interpretation', 'Lab_Provider', 'Location_Confidence', 'Notes']

pt = pd.read_excel(DL / "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx",
                   sheet_name="Registo Principal")
pt.columns = EN_COLS
en = pd.read_excel(DL / "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx",
                   sheet_name="Master Log")


def mostra(df, idx, etiqueta):
    for i in idx:
        r = df.loc[i]
        print("\n" + "-" * 92)
        print(f"[{etiqueta}] Record_ID {r['Record_ID']}")
        for c in df.columns:
            v = r[c]
            if pd.isna(v) or str(v).strip() == "":
                continue
            print(f"   {str(c)[:22]:22s}: {str(v)}")


print("#" * 92)
print("# NOTAS DE CAMPO (visita tecnica) — livro PT")
print("#" * 92)
mostra(pt, pt.index[pt["Doc_Type"].astype(str).str.contains("Nota de Campo", na=False)], "PT")

print("\n\n" + "#" * 92)
print("# TODOS OS REGISTOS COM 'Rosellinia' — livro PT")
print("#" * 92)
m = pt.apply(lambda r: r.astype(str).str.contains("osellinia", case=False,
                                                  na=False).any(), axis=1)
mostra(pt, pt.index[m], "PT")

print("\n\n" + "#" * 92)
print("# TODOS OS REGISTOS COM 'Rosellinia' — livro EN (para comparar as notas)")
print("#" * 92)
m2 = en.apply(lambda r: r.astype(str).str.contains("osellinia", case=False,
                                                   na=False).any(), axis=1)
mostra(en, en.index[m2], "EN")

print("\n\n" + "#" * 92)
print("# REPORT_NO distintos, para datar cada informe")
print("#" * 92)
for k, v in pt["Report_No"].astype(str).value_counts().items():
    sub = pt[pt["Report_No"].astype(str) == k]
    print(f"  {v:4d}  {k[:56]:56s} | amostragem {sorted(set(sub['Sample_Date'].astype(str)))}")
