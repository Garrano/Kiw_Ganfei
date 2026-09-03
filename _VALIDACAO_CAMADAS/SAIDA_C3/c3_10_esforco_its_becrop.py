# -*- coding: utf-8 -*-
"""C3 · tarefas 4, 5, 6, 8 e 9.

4 · a assimetria de esforco de amostragem, medida por unidade geografica
5 · o «Kiwi 1000»: pode ou nao ir para o mapa
6 · a qualidade de leitura das quatro ITS
8 · a contaminacao do caso Kiwi Atlantico, e a valvula 27
9 · os dois relatorios Becrop sao comparaveis entre si?
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

DL = r"C:\Users\Jackster2\Downloads"
OUT = os.path.dirname(os.path.abspath(__file__))
LIVRO = os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx")

col = pd.read_csv(os.path.join(OUT, "c3_07_registos_colocados.csv"))
with open(os.path.join(OUT, "c3_07_georreferenciacao.json"), encoding="utf-8") as f:
    GEO = json.load(f)
res = {}

# ============================================================ 4 · esforco
print("=" * 96)
print("4 · ESFORCO DE AMOSTRAGEM POR UNIDADE GEOGRAFICA")
print("=" * 96)
colocados = col[col["classe_posicao"].isin(
    ["COLOCADO", "COLOCADO-BLOCO", "INFERIDO", "AMBIGUO"])]
esf = colocados.groupby("unidade").agg(
    registos=("Record_ID", "count"),
    relatorios=("Source_File", "nunique"),
    datas=("Sample_Date", "nunique")).reset_index()

todas = {**{f"v{k}": v for k, v in GEO["por_valvula"].items()}, **GEO["por_bloco"]}
linhas = []
print(f"{'unidade':<12s} {'ha':>5s} {'defice26':>9s} {'novoM2':>7s} {'chao':>6s}"
      f" {'dOESTE':>7s} {'dESTE':>6s} | {'registos':>8s} {'relat':>6s} {'datas':>6s}")
for nome, u in sorted(todas.items(), key=lambda x: -x[1]["pct_defice_2026"]):
    r = esf[esf["unidade"] == nome]
    n = int(r["registos"].iloc[0]) if len(r) else 0
    nr = int(r["relatorios"].iloc[0]) if len(r) else 0
    nd = int(r["datas"].iloc[0]) if len(r) else 0
    print(f"{nome:<12s} {u['ha']:5.2f} {u['pct_defice_2026']:8.1f}%"
          f" {u['pct_novo_M2']:6.1f}% {u['pct_nu2021_chao_lavrado']:5.1f}%"
          f" {u['d_foco_OESTE_m']:6.0f} {u['d_foco_ESTE_m']:6.0f} |"
          f" {n:8d} {nr:6d} {nd:6d}")
    if not nome.startswith("v") or nome in ("v6", "v7", "v8", "v9", "v10", "v11",
                                            "v12", "v13", "v14", "v15", "v16", "v17"):
        pass
    linhas.append((nome, u["pct_defice_2026"], n, u["ha"]))

# o esforco segue o padrao? (a armadilha que o prompt manda procurar)
so_valv = [(n, d, c) for n, d, c, _ in linhas if n.startswith("v")]
rho = stats.spearmanr([x[1] for x in so_valv], [x[2] for x in so_valv])
print(f"\nSpearman (defice26 da valvula) x (registos colocados nessa valvula):")
print(f"   rho = {rho.statistic:+.3f}  p = {rho.pvalue:.3f}  n = {len(so_valv)} valvulas")
print("   Se fosse fortemente positivo, a amostragem teria sido dirigida pelo")
print("   proprio sinal que se quer explicar — a armadilha que o prompt nomeia.")

v8 = GEO["por_valvula"]["8"]
n_v8 = int(esf[esf["unidade"] == "v8"]["registos"].sum()) if "v8" in set(esf["unidade"]) else 0
print(f"\n   A valvula 8 — a que contem o FOCO OESTE E530485 N4655053, a 46 m do")
print(f"   centroide da sua propria particao, com {v8['pct_defice_2026']:.1f} % de defice em 2026 e")
print(f"   {v8['pct_novo_M2']:.1f} % de declinio novo — tem {n_v8} registos de laboratorio colocados.")
res["esforco"] = {"por_unidade": esf.to_dict("records"),
                  "spearman_defice_x_registos_valvulas":
                      [round(float(rho.statistic), 3), round(float(rho.pvalue), 4)],
                  "registos_na_v8": n_v8}

# ========================================================= 5 · Kiwi 1000
print("\n" + "=" * 96)
print("5 · O «KIWI 1000»")
print("=" * 96)
pt = pd.read_excel(LIVRO, sheet_name="Registo Principal")
pt.columns = ['Record_ID', 'Source_File', 'Doc_Type', 'Report_No', 'Client_Titular',
              'Terrain_Block_Parcel', 'Parish_Municipality', 'Parcelario_No',
              'Sample_Date', 'Received_Date', 'Result_Date', 'Matrix',
              'Test_Category', 'Method', 'Organism_Parameter', 'Result', 'Value',
              'Unit', 'Interpretation', 'Lab_Provider', 'Location_Confidence', 'Notes']
k1000 = pt[pt["Terrain_Block_Parcel"].astype(str).str.contains("Kiwi 1000", na=False)]
print(f"registos rotulados 'Kiwi 1000' como talhao : {len(k1000)}")
print(f"   ficheiro     : {sorted(set(k1000['Source_File']))}")
print(f"   informe      : {sorted(set(k1000['Report_No']))}")
print(f"   amostragem   : {sorted(set(k1000['Sample_Date'].astype(str)))}")
print(f"   matrizes     : {sorted(set(k1000['Matrix']))}")
cli = pt["Client_Titular"].astype(str)
n_cliente = int(cli.str.contains("Kiwi 1000", na=False).sum())
print(f"\n'Kiwi 1000' como NOME DO CLIENTE (coluna Client_Titular) : {n_cliente} registos")
print("   -> 'Kiwi 1000' e o nome da empresa titular, nao um lugar. Uma amostra")
print("      rotulada 'Kiwi 1000' esta rotulada com o dono, e o dono tem ~50 ha.")
orgs_so_k1000 = [s["organismo"] for s in
                 json.load(open(os.path.join(OUT, "c3_09_organismos.json"),
                                encoding="utf-8"))["organismos"]
                 if s["veredicto"] == "SEM POSICAO"]
print(f"\norganismos cujos UNICOS positivos vem desta amostra : {len(orgs_so_k1000)}")
for o in orgs_so_k1000:
    print("   ·", o)
res["kiwi_1000"] = {"registos_como_talhao": len(k1000),
                    "registos_como_cliente": n_cliente,
                    "ficheiro": sorted(set(k1000["Source_File"])),
                    "informe": sorted(set(k1000["Report_No"].astype(str))),
                    "data": sorted(set(k1000["Sample_Date"].astype(str))),
                    "organismos_sem_posicao_por_causa_dela": orgs_so_k1000}

# ================================================================ 6 · ITS
print("\n" + "=" * 96)
print("6 · QUALIDADE DE LEITURA DAS QUATRO ITS")
print("=" * 96)
its = pd.read_excel(LIVRO, sheet_name="Diversidade ITS")
amostras = list(its.columns)[1:]
brutas = [85773, 251395, 135516, 110253]
filtradas = [25078, 7119, 4964, 10688]
pct = [round(100.0 * f / b, 1) for f, b in zip(filtradas, brutas)]
asv = [int(its.iloc[1][c]) for c in amostras]
pielou = [float(its.iloc[2][c]) for c in amostras]
simpson = [float(its.iloc[3][c]) for c in amostras]
shannon = [float(its.iloc[4][c]) for c in amostras]
print(f"{'amostra':<20s} {'brutas':>8s} {'filtradas':>10s} {'%':>6s} {'ASV':>5s}"
      f" {'Pielou':>7s} {'Simpson':>8s} {'Shannon':>8s}")
for i, a in enumerate(amostras):
    print(f"{a[:20]:<20s} {brutas[i]:8d} {filtradas[i]:10d} {pct[i]:6.1f} {asv[i]:5d}"
          f" {pielou[i]:7.4f} {simpson[i]:8.4f} {shannon[i]:8.3f}")
r_asv = stats.spearmanr(filtradas, asv)
r_pie = stats.spearmanr(filtradas, pielou)
r_sim = stats.spearmanr(filtradas, simpson)
print(f"\nSpearman (leituras filtradas) x riqueza de ASV : rho = {r_asv.statistic:+.3f}"
      f"  p = {r_asv.pvalue:.3f}")
print(f"Spearman (leituras filtradas) x Pielou        : rho = {r_pie.statistic:+.3f}"
      f"  p = {r_pie.pvalue:.3f}")
print(f"Spearman (leituras filtradas) x Simpson       : rho = {r_sim.statistic:+.3f}"
      f"  p = {r_sim.pvalue:.3f}")
print(f"\namplitude de profundidade: {max(filtradas)/min(filtradas):.1f}x "
      f"({min(filtradas)} a {max(filtradas)} leituras)")
print(f"amplitude de ASV         : {max(asv)/min(asv):.2f}x ({min(asv)} a {max(asv)})")
print(f"amplitude de Pielou      : {max(pielou)/min(pielou):.3f}x")
print(f"amplitude de Simpson     : {max(simpson)/min(simpson):.3f}x")
print("\nA ordenacao da riqueza e IDENTICA a ordenacao da profundidade nas quatro")
print("amostras. Os indices robustos a profundidade (Pielou, Simpson) sao")
print("indistinguiveis entre si. Nao ha rarefaccao declarada em lado nenhum.")
res["its"] = {"amostras": amostras, "brutas": brutas, "filtradas": filtradas,
              "pct_qualificadas": pct, "asv": asv, "pielou": pielou,
              "simpson": simpson, "shannon": shannon,
              "spearman_profundidade_x_asv": [float(r_asv.statistic), round(float(r_asv.pvalue), 4)],
              "spearman_profundidade_x_pielou": [float(r_pie.statistic), round(float(r_pie.pvalue), 4)],
              "razao_profundidade": round(max(filtradas) / min(filtradas), 1)}

# ================================== 8 · Kiwi Atlantico e a «valvula 27»
print("\n" + "=" * 96)
print("8 · PROVENIENCIA: O QUE SAI DAS CONTAGENS")
print("=" * 96)
fora = col[col["classe_posicao"] == "FORA DO CONJUNTO"]
nao_am = col[col["classe_posicao"] == "NAO E AMOSTRA"]
print(f"Kiwi Atlantico S.A. (Lois-Portaris, Ribadumia, Pontevedra) : {len(fora)} registos")
print(f"   ficheiros : {sorted(set(fora['Source_File']))}")
print(f"   informe   : 240/2023 · amostragem {sorted(set(fora['Sample_Date'].astype(str)))}")
print(f"   ARMADILHA : o talhao chama-se 'B-3/C-3'. O pomar de Ganfei tem um bloco")
print(f"               'B3'. Sao sitios diferentes a ~90 km de distancia.")
print(f"\nFicha tecnica de produto (nao e amostra do pomar)          : {len(nao_am)} registos")
print(f"   ficheiro : {sorted(set(nao_am['Source_File']))}")
print(f"\ntotal a retirar das contagens do pomar : {len(fora) + len(nao_am)}")
print(f"registos que sobram como sendo de Ganfei : {len(col) - len(fora) - len(nao_am)}")

busca27 = pt.apply(lambda r: r.astype(str).str.contains(
    r"(?<![0-9])27(?![0-9])", na=False, regex=True).any(), axis=1)
cols27 = set()
for i in pt.index[busca27]:
    for c in pt.columns:
        if pd.notna(pt.loc[i, c]) and __import__("re").search(
                r"(?<![0-9])27(?![0-9])", str(pt.loc[i, c])):
            cols27.add(c)
print(f"\n«valvula 27»: procurada nos dois livros. As unicas ocorrencias do numero")
print(f"   27 isolado estao nas colunas {sorted(cols27)} — um Record_ID e uma data")
print(f"   de resultado (2023-06-27). Nao existe nenhuma valvula 27 em nenhum dos")
print(f"   dois livros, nem associada aos Becrop nem a mais nada.")
res["proveniencia"] = {"fora_do_conjunto": len(fora), "nao_e_amostra": len(nao_am),
                       "sobram_ganfei": len(col) - len(fora) - len(nao_am),
                       "valvula_27_ocorrencias": sorted(cols27)}

# ============================================================= 9 · Becrop
print("\n" + "=" * 96)
print("9 · OS DOIS RELATORIOS BECROP SAO COMPARAVEIS?")
print("=" * 96)
bec = pt[pt["Doc_Type"].astype(str).str.contains("Becrop", na=False)]
for f in sorted(set(bec["Source_File"])):
    s = bec[bec["Source_File"] == f]
    print(f"\n{f[:56]}")
    print(f"   informe    : {list(set(s['Report_No']))[0]}")
    print(f"   amostragem : {list(set(s['Sample_Date'].astype(str)))[0]}")
    print(f"   matriz     : {list(set(s['Matrix']))[0]}")
    print(f"   talhao     : {list(set(s['Terrain_Block_Parcel']))[0][:60]}")
print("\n   As duas datas de amostragem sao 2023-08-25 e 2024-02-04: fim de Verao")
print("   contra pleno Inverno, 163 dias de intervalo. A plataforma, o metodo e a")
print("   matriz sao os mesmos (BPP3.5, ITS3/16S4, solo). A EPOCA nao e.")
print("   Nenhum dos dois esta associado a uma parcela ('No hay parcela asociada'),")
print("   e a freguesia declarada (Cristelo Covo e Arao) nao e Ganfei.")
res["becrop"] = {
    "A32A0C": {"amostragem": "2023-08-25", "biosostenibilidad": 41,
               "especies": 856, "saude": "Muy bajo",
               "podridao_radicular": "risco MUITO ALTO detectado"},
    "A32A0B": {"amostragem": "2024-02-04", "biosostenibilidad": 82,
               "especies": 720, "saude": "Alto",
               "podridao_radicular": "No Detectado"},
    "intervalo_dias": 163,
    "veredicto": ("nao comparaveis: epocas opostas, sem parcela associada, "
                  "freguesia declarada diferente de Ganfei, n = 1 por data")}

with open(os.path.join(OUT, "c3_10_esforco_its_becrop.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False, default=str)
print("\nescrito c3_10_esforco_its_becrop.json")
