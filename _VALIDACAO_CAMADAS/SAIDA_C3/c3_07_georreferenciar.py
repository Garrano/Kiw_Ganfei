# -*- coding: utf-8 -*-
"""C3 · tarefas 2 e 3 — georreferenciacao dos registos e cruzamento com o padrao.

FONTE: `Registo Principal` do livro PT (221 registos). A c3_03 estabeleceu que o
`Master Log` EN e o mesmo livro com 18 registos incompletos (nove linhas de
Azoto Total em falta, nove valores substituidos por «page 2 not extracted»).

TRADUCAO DE VOCABULARIO, declarada como a C1 e a C2 declararam:
  FOCO OESTE  E530485 N4655053  (B2, valvula 8 a 35 m; e a «Zona 0» da exploracao)
  FOCO ESTE   E530977 N4655117  (B3, valvulas 13 e 14)
  mascara `zona0` do ficheiro   = FOCO ESTE
AVISO (adenda LiDAR, 29-08-2026): metade do disco do FOCO ESTE nao tinha pergola
em 06-07-2025 (0,47 m de altura mediana). Qualquer leitura biologica do lado
oriental corre o risco de ser sobre solo. Por isso este script reporta, para
cada unidade, a fraccao de `nu2021` (chao lavrado) alem do defice.

Posicoes: SO `ganfei_s2\valvulas_por_area.json` (R2 G35). O
`REGISTO_DE_NOMES.md` e o `valvulas_v6.json` estao desactualizados.

Particao: cada celula do poligono `pomar` e atribuida a valvula mais proxima
(mesma particao que a C2 usou em c2_08). O rotulo de bloco de cada valvula vem
do proprio `valvulas_por_area.json`.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import (AOI, FOCO_ESTE, FOCO_OESTE, NC, NL, ORIGEM_NO, PASSO,
                         carrega_mascaras, centros_celulas, discos_dos_focos)

DL = r"C:\Users\Jackster2\Downloads"
C2 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2"
OUT = os.path.dirname(os.path.abspath(__file__))
EN_COLS = ['Record_ID', 'Source_File', 'Doc_Type', 'Report_No', 'Client_Titular',
           'Terrain_Block_Parcel', 'Parish_Municipality', 'Parcelario_No',
           'Sample_Date', 'Received_Date', 'Result_Date', 'Matrix',
           'Test_Category', 'Method', 'Organism_Parameter', 'Result', 'Value',
           'Unit', 'Interpretation', 'Lab_Provider', 'Location_Confidence', 'Notes']

# ---------------------------------------------------------------- geometria
masc, _ = carrega_mascaras()
pomar, saudavel, zona0, nu2021 = (masc["pomar"], masc["saudavel"],
                                  masc["zona0"], masc["nu2021"])
defice26 = np.load(os.path.join(C2, "c2_05_defice_2026.npy"))
novo_m2 = np.load(os.path.join(C2, "c2_05_novo_m2.npy"))
disco_o, disco_e = discos_dos_focos(pomar, raio=90.0)
E, N = centros_celulas()

with open(os.path.join(DL, "ganfei_s2", "valvulas_por_area.json"),
          encoding="utf-8") as f:
    VALV = json.load(f)

# --- controlo T1 do adversario da C2: a referencia sistematica esta limpa? ---
ctrl = {
    "REF_e_disco_OESTE": int((saudavel & disco_o).sum()),
    "REF_e_disco_ESTE": int((saudavel & disco_e).sum()),
    "REF_e_defice_2026": int((saudavel & defice26).sum()),
    "REF_e_novo_M2": int((saudavel & novo_m2).sum()),
    "REF_e_nu2021": int((saudavel & nu2021).sum()),
    "REF_celulas": int(saudavel.sum()),
}
print("== controlo herdado (T1 do adversario da C2): interseccoes da referencia ==")
for k, v in ctrl.items():
    print(f"   {k:22s} = {v}")

# --- particao por valvula mais proxima, sobre o poligono `pomar` ---
ids = sorted(VALV, key=int)
ve = np.array([VALV[k]["E"] for k in ids])
vn = np.array([VALV[k]["N"] for k in ids])
d2 = ((E[..., None] - ve) ** 2 + (N[..., None] - vn) ** 2)
maisperto = np.argmin(d2, axis=2)
valv_de = np.where(pomar, maisperto, -1)

bloco_de_valv = {k: VALV[k]["bloco"] for k in ids}
blocos = sorted(set(bloco_de_valv.values()))


def unidade(mask, nome):
    n = int(mask.sum())
    if n == 0:
        return None
    ce, cn = float(E[mask].mean()), float(N[mask].mean())
    return {
        "unidade": nome, "celulas": n, "ha": round(n / 100.0, 2),
        "E": round(ce, 1), "N": round(cn, 1),
        "d_foco_OESTE_m": round(float(np.hypot(ce - FOCO_OESTE[0], cn - FOCO_OESTE[1])), 0),
        "d_foco_ESTE_m": round(float(np.hypot(ce - FOCO_ESTE[0], cn - FOCO_ESTE[1])), 0),
        "pct_defice_2026": round(100.0 * float((mask & defice26).sum()) / n, 1),
        "pct_novo_M2": round(100.0 * float((mask & novo_m2).sum()) / n, 1),
        "pct_nu2021_chao_lavrado": round(100.0 * float((mask & nu2021).sum()) / n, 1),
        "pct_disco_OESTE": round(100.0 * float((mask & disco_o).sum()) / n, 1),
        "pct_disco_ESTE": round(100.0 * float((mask & disco_e).sum()) / n, 1),
    }


print("\n== unidades de referencia (padrao herdado da C2) ==")
ref_units = {}
for nome, m in (("poligono pomar", pomar), ("referencia sistematica", saudavel),
                ("disco FOCO OESTE r=90", disco_o), ("disco FOCO ESTE r=90", disco_e),
                ("chao lavrado nu2021", nu2021)):
    u = unidade(m, nome)
    ref_units[nome] = u
    print(f"   {nome:24s} {u['ha']:5.2f} ha | defice26 {u['pct_defice_2026']:5.1f}% |"
          f" novoM2 {u['pct_novo_M2']:5.1f}% | chao {u['pct_nu2021_chao_lavrado']:5.1f}%")

print("\n== particao por valvula (celulas do pomar atribuidas a valvula mais proxima) ==")
uni_valv = {}
for j, k in enumerate(ids):
    m = valv_de == j
    u = unidade(m, "v%s" % k)
    u["bloco"] = bloco_de_valv[k]
    u["E_valvula"], u["N_valvula"] = VALV[k]["E"], VALV[k]["N"]
    uni_valv[k] = u
    print(f"   v{k:<3s} {u['bloco']:<11s} {u['ha']:5.2f} ha | dO {u['d_foco_OESTE_m']:4.0f} m"
          f" dE {u['d_foco_ESTE_m']:4.0f} m | defice26 {u['pct_defice_2026']:5.1f}%"
          f" | novoM2 {u['pct_novo_M2']:5.1f}% | chao {u['pct_nu2021_chao_lavrado']:5.1f}%")

print("\n== particao por bloco ==")
uni_bloco = {}
for b in blocos:
    js = [j for j, k in enumerate(ids) if bloco_de_valv[k] == b]
    m = np.isin(valv_de, js) & pomar
    u = unidade(m, b)
    u["valvulas"] = [k for k in ids if bloco_de_valv[k] == b]
    uni_bloco[b] = u
    print(f"   {b:<11s} v{'|'.join(u['valvulas']):<12s} {u['ha']:5.2f} ha |"
          f" dO {u['d_foco_OESTE_m']:4.0f} m dE {u['d_foco_ESTE_m']:4.0f} m |"
          f" defice26 {u['pct_defice_2026']:5.1f}% | novoM2 {u['pct_novo_M2']:5.1f}%"
          f" | chao {u['pct_nu2021_chao_lavrado']:5.1f}%")

# ------------------------------------------------------- colocar os registos
pt = pd.read_excel(os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx"),
                   sheet_name="Registo Principal")
pt.columns = EN_COLS

# Regras de colocacao, uma por rotulo `Terrain_Block_Parcel` tal como esta no
# livro. Nenhum rotulo e adivinhado: os que nao mapeiam ficam sem posicao.
#   unidade  = chave em uni_bloco ou uni_valv
#   classe   = COLOCADO | SEM POSICAO | FORA DA BANDA | FORA DO CONJUNTO | NAO E AMOSTRA
REGRAS = {
    "B2 - V7":            ("valv", "7",  "COLOCADO", "numero de valvula explicito"),
    "B2 - Zona 1 (V7)":   ("valv", "7",  "COLOCADO", "numero de valvula explicito"),
    "B2 - Zona 1":        ("valv", "7",  "COLOCADO", "mesmo talhao nominal, folha; V7 no nome do ficheiro"),
    "B2.V7":              ("valv", "7",  "COLOCADO", "numero de valvula explicito"),
    "V7":                 ("valv", "7",  "COLOCADO", "numero de valvula explicito"),
    "B3":                 ("bloco", "B3", "COLOCADO-BLOCO", "bloco explicito; ponto dentro do bloco desconhecido"),
    "B3 - 7 ha":          ("bloco", "B3", "COLOCADO-BLOCO", "bloco explicito; a tabela da 9,01 ha ao B3 e o boletim diz 7 ha"),
    "Erica Novo E":       ("bloco", "Erica Novo", "COLOCADO-BLOCO", "rotulo de bloco da tabela de valvulas"),
    "Erica 2016 R":       ("bloco", "Erica Novo", "INFERIDO", "'Erica 2016' identificado com 'Erica Novo' — inferencia da C1, nao prova"),
    "Erica 2016 E":       ("bloco", "Erica Novo", "INFERIDO", "idem; sufixo E reaparece em 343_Kiwi ('Erica Novo E')"),
    "B4":                 ("bloco", "B4", "AMBIGUO", "B4 tem v16-17 na banda E a parcela solta B4C3 sem posicao"),
    "Parcela B4":         ("bloco", "B4", "AMBIGUO", "idem"),
    "B1":                 (None, None, "FORA DA BANDA", "B1 e o bloco a sudoeste, v1-5, fora da banda contigua; raio 343 m"),
    "B1 C1":              (None, None, "FORA DA BANDA", "sub-parcelas do B1 sem posicao"),
    "B1 C3":              (None, None, "FORA DA BANDA", "idem"),
    "B1 C4":              (None, None, "FORA DA BANDA", "idem"),
}


def coloca(rot, cliente, freguesia):
    rot = str(rot)
    if "Kiwi Atl" in str(cliente) or "Ribadumia" in str(freguesia):
        return (None, None, "FORA DO CONJUNTO", "outro cliente e outro concelho (Espanha)")
    if rot.startswith("n/d - literatura"):
        return (None, None, "NAO E AMOSTRA", "ficha tecnica de produto")
    if rot in REGRAS:
        return REGRAS[rot]
    if rot.startswith("NÃO ESPECIFICADO") or rot.startswith("Code A32A0"):
        return (None, None, "SEM POSICAO", "o proprio documento nao indica talhao")
    if rot.startswith("Pomar completo") or rot.startswith("Whole orchard"):
        return (None, None, "SEM POSICAO", "observacao ao nivel do pomar inteiro (~50 ha)")
    if "local n" in rot:
        return (None, None, "SEM POSICAO", "o proprio documento diz 'local nao especificado'")
    return (None, None, "SEM POSICAO", "rotulo nao mapeavel para a tabela de valvulas")


linhas = []
for _, r in pt.iterrows():
    tipo, chave, classe, nota = coloca(r["Terrain_Block_Parcel"],
                                       r["Client_Titular"], r["Parish_Municipality"])
    u = None
    if tipo == "valv":
        u = uni_valv[chave]
    elif tipo == "bloco":
        u = uni_bloco[chave]
    linhas.append({
        "Record_ID": int(r["Record_ID"]),
        "Source_File": r["Source_File"],
        "Doc_Type": r["Doc_Type"],
        "Terrain_Block_Parcel": r["Terrain_Block_Parcel"],
        "Sample_Date": r["Sample_Date"],
        "Matrix": r["Matrix"],
        "Organism_Parameter": r["Organism_Parameter"],
        "Result": r["Result"],
        "classe_posicao": classe,
        "unidade": (u["unidade"] if u else ""),
        "nota_colocacao": nota,
        "E": (u["E"] if u else ""), "N": (u["N"] if u else ""),
        "d_foco_OESTE_m": (u["d_foco_OESTE_m"] if u else ""),
        "d_foco_ESTE_m": (u["d_foco_ESTE_m"] if u else ""),
        "pct_defice_2026": (u["pct_defice_2026"] if u else ""),
        "pct_novo_M2": (u["pct_novo_M2"] if u else ""),
        "pct_nu2021": (u["pct_nu2021_chao_lavrado"] if u else ""),
    })
col = pd.DataFrame(linhas)
col.to_csv(os.path.join(OUT, "c3_07_registos_colocados.csv"), index=False,
           encoding="utf-8")

print("\n== contagem por classe de posicao (de %d registos) ==" % len(col))
for k, v in col["classe_posicao"].value_counts().items():
    print(f"   {v:4d}  {k}")
com = col["classe_posicao"].isin(["COLOCADO", "COLOCADO-BLOCO", "INFERIDO", "AMBIGUO"])
print(f"\n   COM posicao na banda contigua : {int(com.sum())}")
print(f"   SEM posicao                    : {int((~com).sum())}")
print("   dos quais:")
for k in ["FORA DA BANDA", "SEM POSICAO", "FORA DO CONJUNTO", "NAO E AMOSTRA"]:
    print(f"      {int((col['classe_posicao'] == k).sum()):4d}  {k}")

res = {"controlo_T1_referencia": ctrl, "unidades_referencia": ref_units,
       "por_valvula": uni_valv, "por_bloco": uni_bloco,
       "n_registos": len(col),
       "por_classe": {k: int(v) for k, v in col["classe_posicao"].value_counts().items()},
       "com_posicao": int(com.sum()), "sem_posicao": int((~com).sum())}
with open(os.path.join(OUT, "c3_07_georreferenciacao.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print("\nescrito c3_07_georreferenciacao.json e c3_07_registos_colocados.csv")
