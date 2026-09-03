"""C3 · inventario dos dois livros.

Nao interpreta nada. So lista folhas, dimensoes e cabecalhos, para se saber
com o que se esta a lidar antes de reconciliar.
"""
import json
from pathlib import Path

import pandas as pd

DL = Path(r"C:\Users\Jackster2\Downloads")
EN = DL / "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx"
PT = DL / "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx"
OUT = Path(__file__).parent

res = {}
for nome, cam in (("EN", EN), ("PT", PT)):
    xl = pd.ExcelFile(cam)
    res[nome] = {"ficheiro": cam.name, "folhas": {}}
    for f in xl.sheet_names:
        df = xl.parse(f, header=0)
        res[nome]["folhas"][f] = {
            "linhas": int(df.shape[0]),
            "colunas": int(df.shape[1]),
            "cabecalhos": [str(c) for c in df.columns],
        }
        print(f"[{nome}] {f}: {df.shape[0]}x{df.shape[1]}")
        print("      ", list(df.columns)[:24])

(OUT / "c3_00_inventario.json").write_text(
    json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8"
)
print("\nescrito c3_00_inventario.json")
