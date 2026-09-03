# -*- coding: utf-8 -*-
"""C3 · tarefa 3 — os positivos estao onde o padrao esta?

Para cada organismo da Matriz de Fitopatologia e para as Contagens de Nematodos,
cruza a posicao da amostra com o defice de 2026, com as 3,58 ha de declinio novo
(M2) e com os dois focos por coordenada.

A resposta e uma de tres, e so uma:
  ONDE O PADRAO ESTA | EM TODO O LADO | SEM POSICAO
mais duas categorias que a proveniencia obriga a abrir:
  FORA DO CONJUNTO (outro pomar)

A pergunta NAO se faz ao contrario: nao se procura o organismo que explica o
padrao. Percorrem-se todos, e diz-se de cada um o que ha.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

DL = r"C:\Users\Jackster2\Downloads"
OUT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(OUT, "c3_07_georreferenciacao.json"), encoding="utf-8") as f:
    GEO = json.load(f)
UB, UV = GEO["por_bloco"], GEO["por_valvula"]

# Cada coluna da Matriz de Fitopatologia -> unidade geografica, ou nao.
COLUNA_PARA_UNIDADE = {
    "NÃO ESPECIFICADO": (None, "SEM POSICAO",
                         "amostra composta 'Kiwi 1000'; 'Kiwi 1000, Lda' e o nome do "
                         "cliente em 131 registos, nao um lugar"),
    "B1": (None, "SEM POSICAO",
           "B1 e o bloco a sudoeste, fora da banda contigua; R2 G36 da-lhe posicao "
           "de conjunto com raio de incerteza de 343 m, e nao ha ponto dentro dele"),
    "B3": (UB["B3"], "COLOCADO-BLOCO", "bloco B3, valvulas 12-15"),
    "B4": (UB["B4"], "COLOCADO-BLOCO", "bloco B4, valvulas 16-17 (ambiguo: existe "
                                       "tambem a parcela solta B4C3 sem posicao)"),
    "V7": (UV["7"], "COLOCADO", "valvula 7 explicita"),
    "Erica Novo E": (UB["Erica Novo"], "COLOCADO-BLOCO", "bloco Erica Novo, valvulas 10-11"),
    "B-3/C-3": (None, "FORA DO CONJUNTO",
                "Kiwi Atlantico S.A., Lois-Portaris, Ribadumia, Pontevedra (Espanha)"),
}


def unidade_da_coluna(nome):
    for pref, v in COLUNA_PARA_UNIDADE.items():
        if str(nome).startswith(pref):
            return v
    return (None, "SEM POSICAO", "rotulo nao mapeavel")


mat = pd.read_excel(os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx"),
                    sheet_name="Matriz Fitopatologia")
cols = list(mat.columns)[1:]
mat = mat[mat[mat.columns[0]].notna()]
mat = mat[~mat[mat.columns[0]].astype(str).str.startswith("Ler da esquerda")]

print("colunas da matriz e o que cada uma vale geograficamente:")
for c in cols:
    u, cl, nota = unidade_da_coluna(c)
    extra = ""
    if u:
        extra = (f" | {u['ha']:.2f} ha | defice26 {u['pct_defice_2026']:.1f}%"
                 f" | novoM2 {u['pct_novo_M2']:.1f}% | dO {u['d_foco_OESTE_m']:.0f} m"
                 f" dE {u['d_foco_ESTE_m']:.0f} m")
    print(f"   {str(c)[:34]:34s} -> {cl:16s}{extra}")

print("\n" + "=" * 96)
print("ORGANISMO A ORGANISMO")
print("=" * 96)
saidas = []
for _, r in mat.iterrows():
    org = str(r[mat.columns[0]]).strip()
    pos_colocadas, pos_sem, pos_fora, neg_colocadas, neg_sem, neg_fora = [], [], [], [], [], []
    for c in cols:
        v = str(r[c]).strip().upper()
        if v in ("", "NAN"):
            continue
        u, cl, _ = unidade_da_coluna(c)
        alvo = (pos_colocadas if v.startswith("POSITIV") else neg_colocadas)
        alvo2 = (pos_sem if v.startswith("POSITIV") else neg_sem)
        alvo3 = (pos_fora if v.startswith("POSITIV") else neg_fora)
        if cl == "FORA DO CONJUNTO":
            alvo3.append(str(c)[:14])
        elif u is None:
            alvo2.append(str(c)[:14])
        else:
            alvo.append((str(c)[:14], u))

    n_testes_ganfei = (len(pos_colocadas) + len(neg_colocadas)
                       + len(pos_sem) + len(neg_sem))
    if n_testes_ganfei == 0:
        veredicto = "FORA DO CONJUNTO"
        just = "so testado no pomar de Kiwi Atlantico (Espanha)"
    elif not pos_colocadas and not pos_sem:
        veredicto = "NEGATIVO (nada a localizar)"
        just = "sem nenhum positivo em amostra de Ganfei"
    elif not pos_colocadas:
        veredicto = "SEM POSICAO"
        just = ("os unicos positivos vem de amostras que o proprio livro marca "
                "sem codigo de talhao")
    else:
        n_uni = len(pos_colocadas) + len(neg_colocadas)
        if len(pos_colocadas) == n_uni and n_uni >= 3:
            veredicto = "EM TODO O LADO"
            just = f"positivo em {n_uni}/{n_uni} unidades colocadas testadas"
        else:
            defs = [u["pct_defice_2026"] for _, u in pos_colocadas]
            veredicto = "COLOCADO — ver detalhe"
            just = (f"positivo em {len(pos_colocadas)} de {n_uni} unidades; "
                    f"defice26 dos positivos {defs}")

    print(f"\n{org}")
    print(f"   VEREDICTO: {veredicto}  ({just})")
    if pos_colocadas:
        for nome, u in pos_colocadas:
            print(f"      + POSITIVO {nome:14s} defice26 {u['pct_defice_2026']:5.1f}% "
                  f"novoM2 {u['pct_novo_M2']:5.1f}% chao {u['pct_nu2021_chao_lavrado']:5.1f}% "
                  f"dO {u['d_foco_OESTE_m']:4.0f} m dE {u['d_foco_ESTE_m']:4.0f} m")
    if pos_sem:
        print(f"      + POSITIVO sem posicao : {pos_sem}")
    if neg_colocadas:
        print(f"      - negativo colocado    : {[n for n, _ in neg_colocadas]}")
    if neg_sem:
        print(f"      - negativo sem posicao : {neg_sem}")
    if pos_fora or neg_fora:
        print(f"      ~ fora do conjunto     : +{pos_fora} -{neg_fora}")

    saidas.append({"organismo": org, "veredicto": veredicto, "justificacao": just,
                   "positivos_colocados": [n for n, _ in pos_colocadas],
                   "positivos_sem_posicao": pos_sem,
                   "negativos_colocados": [n for n, _ in neg_colocadas],
                   "negativos_sem_posicao": neg_sem,
                   "positivos_fora_do_conjunto": pos_fora,
                   "negativos_fora_do_conjunto": neg_fora})

print("\n" + "=" * 96)
print("RESUMO DOS VEREDICTOS")
print("=" * 96)
vc = pd.Series([s["veredicto"] for s in saidas]).value_counts()
for k, v in vc.items():
    print(f"   {v:3d}  {k}")

# ------------------------------------------------- contagens de nematodos
print("\n" + "=" * 96)
print("CONTAGENS DE NEMATODOS contra o padrao")
print("=" * 96)
nem = pd.read_excel(os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx"),
                    sheet_name="Contagens Nemátodos")
nem = nem[nem[nem.columns[0]].notna()]
nem = nem[~nem[nem.columns[0]].astype(str).str.startswith(("MÉDIA", "MÁXIMO"))]
MAPA_NEM = {"B1": None, "B3": UB["B3"], "B4": UB["B4"], "V7": UV["7"],
            "Erica Novo E": UB["Erica Novo"]}
xs, ys_solo, ys_raiz, nomes = [], [], [], []
print(f"{'talhao':<14s} {'solo':>6s} {'raiz':>6s} | {'ha':>5s} {'defice26':>9s}"
      f" {'novoM2':>7s} {'chao':>6s} {'dOESTE':>7s} {'dESTE':>6s}")
for _, r in nem.iterrows():
    b = str(r[nem.columns[0]]).strip()
    u = MAPA_NEM.get(b, "?")
    s, ra = float(r[nem.columns[1]]), float(r[nem.columns[2]])
    if u is None:
        print(f"{b:<14s} {s:6.0f} {ra:6.0f} | SEM POSICAO (bloco a sudoeste, "
              f"raio 343 m, porta-enxerto diferente)")
        continue
    print(f"{b:<14s} {s:6.0f} {ra:6.0f} | {u['ha']:5.2f} {u['pct_defice_2026']:8.1f}%"
          f" {u['pct_novo_M2']:6.1f}% {u['pct_nu2021_chao_lavrado']:5.1f}%"
          f" {u['d_foco_OESTE_m']:6.0f} {u['d_foco_ESTE_m']:6.0f}")
    xs.append(u["pct_defice_2026"]); ys_solo.append(s); ys_raiz.append(ra); nomes.append(b)

rs = stats.spearmanr(xs, ys_solo)
rr = stats.spearmanr(xs, ys_raiz)
print(f"\nSpearman defice26 x contagem no solo : rho = {rs.statistic:+.3f}  p = {rs.pvalue:.3f}  (n = {len(xs)})")
print(f"Spearman defice26 x contagem na raiz : rho = {rr.statistic:+.3f}  p = {rr.pvalue:.3f}  (n = {len(xs)})")
print("n = 4 nao tem poder nenhum. O sinal do rho reporta-se como direccao, nao como resultado.")

res = {"organismos": saidas,
       "resumo_veredictos": {str(k): int(v) for k, v in vc.items()},
       "nematodos": {"unidades": nomes, "defice26_pct": xs,
                     "solo": ys_solo, "raiz": ys_raiz,
                     "spearman_solo": [round(float(rs.statistic), 3), round(float(rs.pvalue), 4)],
                     "spearman_raiz": [round(float(rr.statistic), 3), round(float(rr.pvalue), 4)],
                     "n": len(xs)}}
with open(os.path.join(OUT, "c3_09_organismos.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print("\nescrito c3_09_organismos.json")
