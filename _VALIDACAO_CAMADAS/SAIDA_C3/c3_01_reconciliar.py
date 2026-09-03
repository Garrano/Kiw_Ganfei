"""C3 · tarefa 1 — reconciliar os dois livros.

`Master Log` (EN) contra `Registo Principal` (PT). O prompt da C3 diz 212 contra
222; o inventario da c3_00 le 212 contra 221. Este script estabelece quantos
registos ha de facto, quais sao os que estao a mais, e qual dos dois e a fonte.

Metodo: alinhar por Record_ID / N Registo, e para os IDs comuns comparar as
colunas invariantes a lingua (Source_File, Report_No, Sample_Date, Value).
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

# mapa de colunas PT -> EN, pela ordem (as duas folhas tem 22 colunas na mesma ordem)
assert len(en.columns) == len(pt.columns) == 22
pt_ren = pt.copy()
pt_ren.columns = list(en.columns)

print("linhas EN :", len(en))
print("linhas PT :", len(pt_ren))

# --- linhas totalmente vazias? ---
en_vazias = int(en.isna().all(axis=1).sum())
pt_vazias = int(pt_ren.isna().all(axis=1).sum())
print("linhas totalmente vazias  EN:", en_vazias, " PT:", pt_vazias)

en_id = en["Record_ID"]
pt_id = pt_ren["Record_ID"]
print("Record_ID nao nulos  EN:", int(en_id.notna().sum()),
      " PT:", int(pt_id.notna().sum()))
print("Record_ID duplicados EN:", int(en_id.duplicated().sum()),
      " PT:", int(pt_id.duplicated().sum()))

sen = set(en_id.dropna().astype(int))
spt = set(pt_id.dropna().astype(int))
so_en = sorted(sen - spt)
so_pt = sorted(spt - sen)
print("IDs so em EN:", so_en)
print("IDs so em PT:", so_pt)
print("intervalo EN:", min(sen), "-", max(sen), " n =", len(sen))
print("intervalo PT:", min(spt), "-", max(spt), " n =", len(spt))

# --- as linhas PT sem Record_ID ---
pt_sem_id = pt_ren[pt_id.isna()]
print("\nlinhas PT sem Record_ID:", len(pt_sem_id))
for i, r in pt_sem_id.iterrows():
    print("   linha", i, "|", str(r["Source_File"])[:60], "|",
          str(r["Organism_Parameter"])[:40], "|", str(r["Result"])[:30])

# --- as linhas PT com ID que EN nao tem ---
print("\nlinhas PT com ID ausente do EN:")
for rid in so_pt:
    r = pt_ren[pt_ren["Record_ID"] == rid].iloc[0]
    print("   ID", rid, "|", str(r["Source_File"])[:55], "|",
          str(r["Doc_Type"])[:22], "|", str(r["Organism_Parameter"])[:38],
          "|", str(r["Result"])[:26])

print("\nlinhas EN com ID ausente do PT:")
for rid in so_en:
    r = en[en["Record_ID"] == rid].iloc[0]
    print("   ID", rid, "|", str(r["Source_File"])[:55], "|",
          str(r["Doc_Type"])[:22], "|", str(r["Organism_Parameter"])[:38],
          "|", str(r["Result"])[:26])

# --- para os IDs comuns, as colunas invariantes batem? ---
comuns = sorted(sen & spt)
e = en.set_index("Record_ID").loc[comuns]
p = pt_ren.set_index("Record_ID").loc[comuns]
invariantes = ["Source_File", "Report_No", "Sample_Date", "Received_Date",
               "Result_Date", "Value", "Parcelario_No"]
divs = {}
for c in invariantes:
    a, b = e[c], p[c]
    dif = ~((a.astype(str) == b.astype(str)) | (a.isna() & b.isna()))
    divs[c] = sorted(int(x) for x in dif[dif].index)
    print(f"  {c:16s} divergem em {int(dif.sum()):3d} registos"
          + (f"  ex: {divs[c][:6]}" if int(dif.sum()) else ""))

# um exemplo de cada divergencia
for c, ids in divs.items():
    if ids:
        rid = ids[0]
        print(f"\n  exemplo {c} ID {rid}: EN={e.loc[rid, c]!r}  PT={p.loc[rid, c]!r}")

res = {
    "linhas_EN": len(en), "linhas_PT": len(pt_ren),
    "vazias_EN": en_vazias, "vazias_PT": pt_vazias,
    "ids_EN": len(sen), "ids_PT": len(spt),
    "so_em_EN": so_en, "so_em_PT": so_pt,
    "PT_sem_record_id": int(pt_id.isna().sum()),
    "PT_sem_id_ficheiros": [str(x) for x in pt_sem_id["Source_File"].tolist()],
    "comuns": len(comuns),
    "divergencias_invariantes": {k: v for k, v in divs.items()},
}
(OUT / "c3_01_reconciliar.json").write_text(
    json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nescrito c3_01_reconciliar.json")
