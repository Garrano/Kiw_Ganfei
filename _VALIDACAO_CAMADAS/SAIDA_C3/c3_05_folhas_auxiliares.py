"""C3 · despejo integral das folhas auxiliares do livro PT (e do EN onde difere).

Matriz de Fitopatologia, Contagens de Nematodos, Diversidade ITS, Becrop,
Registo Drone-NDVI, Pontos a Esclarecer, LEIA-ME. Sem interpretacao.
"""
from pathlib import Path

import pandas as pd

DL = Path(r"C:\Users\Jackster2\Downloads")
PT = DL / "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx"
EN = DL / "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx"

pd.set_option("display.max_colwidth", 200)
pd.set_option("display.width", 250)

for cam, folhas in ((PT, ["LEIA-ME", "Matriz Fitopatologia", "Contagens Nemátodos",
                          "Diversidade ITS", "Relatorios Becrop",
                          "Registo Drone-NDVI", "Pontos a Esclarecer"]),
                    (EN, ["Pathology Matrix"])):
    for f in folhas:
        df = pd.read_excel(cam, sheet_name=f)
        print("\n" + "=" * 100)
        print(f"### {cam.name[:20]} :: {f}   ({df.shape[0]}x{df.shape[1]})")
        print("=" * 100)
        for i, r in df.iterrows():
            print(f"-- linha {i}")
            for c in df.columns:
                v = r[c]
                if pd.isna(v):
                    v = ""
                print(f"     {str(c)[:60]:60s} : {str(v)[:200]}")
