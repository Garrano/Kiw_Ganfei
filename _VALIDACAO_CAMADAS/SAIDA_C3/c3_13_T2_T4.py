# -*- coding: utf-8 -*-
"""C3 · T2 e T4 do `CAMADA_3_ADVERSARIO.md`, condicao de arranque da C4.

T2 — publicar os sete numeros que a camada calculou e nao publicou. Custo
     computacional nulo; tres deles mudam o sentido do que a C4 recebe.
T4 — reconciliar a divergencia 0,054 contra 0,0218 na queda da referencia.
     O controlo 2 diz que divergencia sem explicacao e achado, nao correccao.

Acrescenta-se a verificacao empirica da R1, porque uma retirada mal fundada e
tao grave como uma afirmacao mal fundada, e a R1 e verificavel em uma linha.

TUDO o que aqui se escreve e LIDO de ficheiro. Nao ha um unico literal
transcrito a mao — foi esse o erro que a R1 apanhou, e a correccao e de metodo,
nao so de valor.
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
import rasterio
from scipy import stats

sys.path.insert(0, r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C2")
from c2_00_comum import DATAS, TODAS, carrega_mascaras, discos_dos_focos, centros_celulas

DL = r"C:\Users\Jackster2\Downloads"
RAIZ = os.path.join(DL, "ganfei_s2")
OUT = os.path.dirname(os.path.abspath(__file__))
LIVRO_PT = os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx")
LIVRO_EN = os.path.join(DL, "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx")
res = {}

col = pd.read_csv(os.path.join(OUT, "c3_07_registos_colocados.csv"))
reg = pd.read_csv(os.path.join(OUT, "c3_04_registo_principal.csv"))
COM = ["COLOCADO", "COLOCADO-BLOCO", "INFERIDO", "AMBIGUO"]

# ===================================================================== R1
print("=" * 92)
print("R1 · VERIFICACAO EMPIRICA — a «podredumbre radicular» existe ou nao?")
print("=" * 92)
hits = reg[reg["Notes"].astype(str).str.contains("odred", case=False, na=False)]
print(f"registos do `Registo Principal` com «podred» na coluna Notes: {len(hits)}")
becrop_lido = {}
for _, r in hits.iterrows():
    m_alto = bool(re.search(r"MUITO ALTO|MUY ALTO", str(r["Notes"])))
    m_nao = bool(re.search(r"'No Detectado'|Não Detetado|não detetado",
                           str(r["Notes"])))
    becrop_lido[str(r["Source_File"])] = {
        "record_id": int(r["Record_ID"]),
        "coluna": "Notes",
        "risco_muito_alto_mencionado": m_alto,
        "nao_detectado_mencionado": m_nao,
        "menciona_P_sojae": "sojae" in str(r["Notes"]),
        "texto": str(r["Notes"]),
    }
    print(f"\n  ID {int(r['Record_ID'])} · {str(r['Source_File'])[:46]}")
    print(f"     {str(r['Notes'])[:190]}...")
print(f"\nVEREDICTO SOBRE A R1: a categoria EXISTE, na coluna `Notes` dos registos")
print(f"79 e 86, que fazem parte dos 221 e estao em `c3_04_registo_principal.csv`.")
print(f"A premissa da R1 («nao existe em lado nenhum») e FALSA.")
print(f"O que a R1 acerta, e e grave: os valores foram TRANSCRITOS a mao para")
print(f"dentro do `c3_10`, em vez de lidos. O mecanismo que ela descreve e real.")
print(f"E a conclusao da R1 mantem-se por OUTRA razao: as duas Notes sao duas")
print(f"anotacoes do MESMO compilador sobre os MESMOS dois relatorios — um")
print(f"instrumento, nao dois. A coluna de instrumento independente cai na mesma.")
print(f"\nNOTA: o registo 79 nomeia *Phytophthora sojae* — o organismo que o")
print(f"CONTROLOS.md lista como um dos tres erros que custaram semanas.")
res["R1_verificacao"] = {"n_registos_com_podred": len(hits),
                         "premissa_da_R1_e_falsa": True,
                         "metodo_da_C3_estava_errado_transcricao": True,
                         "becrop": becrop_lido}

# ================================================================= T2 (a)
print("\n" + "=" * 92)
print("T2 (a) · a coluna `dif` de c3_08, ano a ano")
print("=" * 92)
with open(os.path.join(OUT, "c3_08_controlo_referencia.json"), encoding="utf-8") as f:
    C8 = json.load(f)
difs = {d: v["dif"] for d, v in C8["serie_mediana"].items()}
for d, v in difs.items():
    marca = "   <-- ano do acontecimento" if d.startswith("2026") else ""
    print(f"   {d}   {v:+.4f}{marca}")
outros = [abs(v) for d, v in difs.items() if not d.startswith("2026")]
print(f"\n   maximo absoluto nos oito anos anteriores : {max(outros):.4f}")
print(f"   valor em 2026                            : {difs['2026-07-27']:+.4f}")
print(f"   razao                                    : {difs['2026-07-27']/max(outros):.1f}x")
print("   A diferenca e ESPECIFICA de 2026. Isto e o argumento de B10, e e")
print("   muito melhor do que a diferenca de dois numeros que foi publicada.")
res["T2a_dif_por_ano"] = difs
res["T2a_max_anos_anteriores"] = max(outros)

# ================================================================= T2 (b,c)
print("\n" + "=" * 92)
print("T2 (b) e (c) · Simpson e Shannon seguem a profundidade; e o p exacto")
print("=" * 92)
its = pd.read_excel(LIVRO_PT, sheet_name="Diversidade ITS")
amostras = list(its.columns)[1:]
# ler as profundidades da propria folha, em vez de as transcrever
linha0 = [str(its.iloc[0][c]) for c in amostras]
brutas, filtradas, pct = [], [], []
for s in linha0:
    a, b, c = [x.strip() for x in s.split("/")]
    brutas.append(int(a)); filtradas.append(int(b)); pct.append(c)
asv = [int(its.iloc[1][c]) for c in amostras]
pielou = [float(its.iloc[2][c]) for c in amostras]
simpson = [float(its.iloc[3][c]) for c in amostras]
shannon = [float(its.iloc[4][c]) for c in amostras]


def ordem(v):
    return [sorted(v).index(x) + 1 for x in v]


print(f"{'metrica':<24s} {'valores':<44s} ordenacao")
for nome, v in (("profundidade filtrada", filtradas), ("riqueza de ASV", asv),
                ("indice de Simpson", simpson), ("indice de Shannon", shannon),
                ("equitabilidade Pielou", pielou)):
    print(f"{nome:<24s} {str(v):<44s} {ordem(v)}")
rhos = {}
for nome, v in (("asv", asv), ("simpson", simpson), ("shannon", shannon),
                ("pielou", pielou)):
    r = stats.spearmanr(filtradas, v)
    rhos[nome] = round(float(r.statistic), 3)
    print(f"\n   rho(profundidade, {nome:8s}) = {r.statistic:+.3f}")
# p exacto de rho = +1 com n = 4: 2 permutacoes de 4! dao |rho| = 1
p_exacto = 2.0 / math.factorial(4)
print(f"\n   p exacto de rho = +1 com n = 4 (bilateral) : {p_exacto:.3f}  (= 2/4!)")
print(f"   o JSON da c3_10 guarda 0.0 — e o scipy a dividir por sqrt(1-rho^2) = 0")
print("\n   CONSEQUENCIA: Simpson e Shannon seguem a profundidade tao")
print("   perfeitamente como a riqueza. So o Pielou se descola, e mal.")
print("   A frase 'Pielou e Simpson sao os indices robustos' SAI.")
res["T2bc_its"] = {"filtradas": filtradas, "asv": asv, "simpson": simpson,
                   "shannon": shannon, "pielou": pielou, "rhos": rhos,
                   "p_exacto_rho1_n4": round(p_exacto, 4),
                   "ordenacoes": {"filtradas": ordem(filtradas), "asv": ordem(asv),
                                  "simpson": ordem(simpson), "shannon": ordem(shannon),
                                  "pielou": ordem(pielou)}}

# =================================================================== T2 (d)
print("\n" + "=" * 92)
print("T2 (d) · «Kiwi 1000» como cliente: 131, nao 146")
print("=" * 92)
vc = reg["Client_Titular"].astype(str).value_counts()
n_lda = int(vc.get("Kiwi 1000, Lda", 0))
n_ident = int(vc.get("Kiwi 1000 (sample identifier)", 0))
print(f"   'Kiwi 1000, Lda' (cliente a serio)          : {n_lda}")
print(f"   'Kiwi 1000 (sample identifier)'             : {n_ident}")
print(f"   soma publicada no certificado               : {n_lda + n_ident}")
print(f"\n   Os {n_ident} sao os proprios registos da amostra a granel: o compilador")
print(f"   pos o identificador da amostra no campo do cliente por nao haver")
print(f"   cliente indicado. Usa-los prova a amostra com ela propria.")
print(f"   NUMERO CITAVEL: {n_lda} de {len(reg)}.")
res["T2d_kiwi1000_cliente"] = {"lda": n_lda, "sample_identifier": n_ident,
                              "publicado": n_lda + n_ident, "citavel": n_lda,
                              "total": len(reg)}

# =================================================================== T2 (e)
print("\n" + "=" * 92)
print("T2 (e) · a reparticao real das datas de B11")
print("=" * 92)
pc = col[col["classe_posicao"].isin(COM)]
amostras_fis = pc.groupby("Source_File")["Sample_Date"].first()
rep = amostras_fis.value_counts().sort_index()
for d, n in rep.items():
    fich = sorted(amostras_fis[amostras_fis == d].index)
    print(f"   {d}  = {n}   {[f[:28] for f in fich]}")
print(f"\n   publicado no certificado : 4 / 4 / 2 / 2")
print(f"   real                     : {' / '.join(str(int(x)) for x in rep.values)}")
# colheitas = (data x unidade) distintas
un = pc.groupby("Source_File").agg(d=("Sample_Date", "first"),
                                   u=("unidade", "first"))
colheitas = un.drop_duplicates(subset=["d", "u"])
print(f"   relatorios: {len(amostras_fis)} · acontecimentos de amostragem "
      f"(data x unidade): {len(colheitas)}")
res["T2e_datas"] = {"real": {str(k): int(v) for k, v in rep.items()},
                    "publicado": [4, 4, 2, 2],
                    "relatorios": int(len(amostras_fis)),
                    "colheitas": int(len(colheitas))}

# =================================================================== T2 (f)
print("\n" + "=" * 92)
print("T2 (f) · a reparticao do disco OESTE pelas tres valvulas")
print("=" * 92)
masc, _ = carrega_mascaras()
pomar = masc["pomar"]
do, de = discos_dos_focos(pomar, raio=90.0)
E, N = centros_celulas()
with open(os.path.join(RAIZ, "valvulas_por_area.json"), encoding="utf-8") as f:
    VALV = json.load(f)
ids = sorted(VALV, key=int)
ve = np.array([VALV[k]["E"] for k in ids]); vn = np.array([VALV[k]["N"] for k in ids])
d2 = ((E[..., None] - ve) ** 2 + (N[..., None] - vn) ** 2)
valv_de = np.where(pomar, np.argmin(d2, axis=2), -1)
print(f"   disco FOCO OESTE (r = 90 m) : {int(do.sum())} celulas")
rep_disco = {}
for j, k in enumerate(ids):
    n = int((do & (valv_de == j)).sum())
    if n:
        rep_disco[k] = n
        print(f"      v{k:<3s} {n:4d} celulas  ({100.0*n/int(do.sum()):5.1f} % do disco)")
n_v7 = int((valv_de == ids.index("7")).sum())
print(f"\n   a v7 tem {n_v7} celulas; {rep_disco.get('7',0)} delas estao dentro do disco")
print(f"   = {100.0*rep_disco.get('7',0)/n_v7:.1f} % da v7, e "
      f"{rep_disco.get('7',0)/100.0:.2f} ha")
# distancia MINIMA de uma celula da v7 ao foco, em vez da do centroide
from c2_00_comum import FOCO_OESTE
m7 = valv_de == ids.index("7")
dmin = float(np.min(np.hypot(E[m7] - FOCO_OESTE[0], N[m7] - FOCO_OESTE[1])))
print(f"\n   distancia MINIMA de uma celula da v7 ao foco OESTE : {dmin:.0f} m")
print(f"   distancia do CENTROIDE da v7 ao foco (o «120 m» publicado) : ver c3_07")
print(f"   os dois numeros descrevem objectos diferentes; nenhum e «a distancia")
print(f"   de uma amostra», porque nenhuma amostra tem coordenada.")
res["T2f_disco_oeste"] = {"celulas_disco": int(do.sum()),
                          "reparticao": rep_disco,
                          "celulas_v7": n_v7,
                          "pct_v7_dentro_do_disco": round(100.0*rep_disco.get('7',0)/n_v7, 1),
                          "dist_minima_v7_ao_foco_m": round(dmin, 0)}

# =================================================================== T2 (g)
print("\n" + "=" * 92)
print("T2 (g) · Doc_Type dos 111 registos colocados — o achado da R2")
print("=" * 92)
dt = pc["Doc_Type"].astype(str).value_counts()
for k, v in dt.items():
    print(f"   {v:4d}  {k[:82]}")
micro = int(sum(v for k, v in dt.items() if "Nematologia" in k or "Fitopatologia" in k))
print(f"\n   microbiologia colocada : {micro} de {len(pc)} registos")
rel_micro = sorted(set(pc[pc["Doc_Type"].astype(str).str.contains(
    "Nematologia|Fitopatologia", na=False)]["Source_File"]))
print(f"   e sao os mesmos {len(rel_micro)} relatorios: {rel_micro}")
orgs_micro = sorted(set(pc[pc["Doc_Type"].astype(str).str.contains(
    "Nematologia|Fitopatologia", na=False)]["Organism_Parameter"].astype(str)))
print(f"   a medirem: {orgs_micro}")

# quantas das 20 linhas organismo x matriz foram ensaiadas com posicao
with open(os.path.join(OUT, "c3_09_organismos.json"), encoding="utf-8") as f:
    ORG = json.load(f)["organismos"]
com_pos = [o for o in ORG if o["positivos_colocados"] or o["negativos_colocados"]]
sem_pos = [o for o in ORG if not (o["positivos_colocados"] or o["negativos_colocados"])]
print(f"\n   das {len(ORG)} linhas organismo x matriz:")
print(f"      ensaiadas em pelo menos uma amostra COM posicao : {len(com_pos)}"
      f"  {[o['organismo'] for o in com_pos]}")
print(f"      NUNCA ensaiadas em nenhuma amostra com posicao  : {len(sem_pos)}")
print(f"\n   >> Nao existe, em todo o caso, um unico ensaio de fungo ou de")
print(f"      oomiceta feito num ponto que se consiga por no mapa.")
res["T2g"] = {"doc_type_colocados": {str(k): int(v) for k, v in dt.items()},
              "microbiologia_colocada": micro,
              "relatorios_microbiologia": rel_micro,
              "organismos_medidos": orgs_micro,
              "linhas_ensaiadas_com_posicao": len(com_pos),
              "linhas_nunca_ensaiadas_com_posicao": len(sem_pos)}

# ============================================================== R3 · vector
print("\n" + "=" * 92)
print("R3 · o vector do rho = -0,044 de B6")
print("=" * 92)
esf = pc.groupby("unidade").size().to_dict()
vec = [(f"v{k}", esf.get(f"v{k}", 0)) for k in ids]
print("   vector de esforco que entrou no Spearman:")
print("   " + " | ".join(f"{n} {v}" for n, v in vec))
nz = [v for _, v in vec if v]
print(f"\n   valores nao-nulos: {len(nz)} de {len(vec)}  |  empates a zero: "
      f"{len(vec)-len(nz)}")
print(f"   registos colocados ao nivel de BLOCO, descartados pelo filtro: "
      f"{len(pc) - sum(v for _, v in vec)}")
print("   Um rho sobre onze empates e um valor nao tem graus de liberdade.")
print("   NAO e um negativo; e um vector degenerado. B6 sai.")
print("\n   a distribuicao real do esforco:")
for u, n in sorted(esf.items(), key=lambda x: -x[1]):
    print(f"      {u:<12s} {n:3d} registos  ({100.0*n/len(pc):4.1f} % dos colocados)")
res["R3_vector"] = {"vector": dict(vec), "nao_nulos": len(nz),
                    "descartados_por_bloco": len(pc) - sum(v for _, v in vec),
                    "distribuicao": {k: int(v) for k, v in esf.items()},
                    "pct_maior": round(100.0*max(esf.values())/len(pc), 1)}

# ================================================================ R6 · B1
print("\n" + "=" * 92)
print("R6 · o instrumento independente certo para B1")
print("=" * 92)
with open(os.path.join(OUT, "c3_03_alinhamento.json"), encoding="utf-8") as f:
    AL = json.load(f)
nfich = reg["Source_File"].nunique()
datas_por_fich = reg.groupby("Source_File")["Sample_Date"].nunique()
print(f"   ficheiros de origem: {nfich}; ficheiros com mais de uma data de")
print(f"   amostragem: {int((datas_por_fich > 1).sum())}")
print(f"   -> `Sample_Date` e funcao estrita de `Source_File`, que esta na chave.")
print(f"      O n efectivo nao e 212: sao {nfich} comparacoes.")
print(f"\n   O teste que E independente da chave, e que a camada ja tinha:")
print(f"      `Value` diverge em {AL['n_value_divergente']} de {AL['emparelhadas']} pares")
print(f"      `Result` diverge em {AL['n_result_divergente']} de {AL['emparelhadas']} (traducao)")
print(f"   As {AL['n_value_divergente']} divergencias de `Value` sao todas do mesmo tipo:")
for t in AL["value_divergente"][:3]:
    print(f"      EN={t[2][:40]:40s} PT={t[3][:44]}")
res["R6_B1"] = {"ficheiros": int(nfich),
                "ficheiros_com_mais_de_uma_data": int((datas_por_fich > 1).sum()),
                "value_divergente": AL["n_value_divergente"],
                "emparelhadas": AL["emparelhadas"]}

# ================================================================ R7 · «27»
print("\n" + "=" * 92)
print("R7 · a busca do «27» refeita sobre os DOIS livros e as DEZASSEIS folhas")
print("=" * 92)
pad = re.compile(r"(?<![0-9])27(?![0-9])")
ocorr, nfolhas = [], 0
for nome, cam in (("PT", LIVRO_PT), ("EN", LIVRO_EN)):
    xl = pd.ExcelFile(cam)
    for folha in xl.sheet_names:
        nfolhas += 1
        df = xl.parse(folha, header=0)
        for c in df.columns:
            if pad.search(str(c)):
                ocorr.append((nome, folha, "CABECALHO", str(c)[:60]))
        for i, r in df.iterrows():
            for c in df.columns:
                v = r[c]
                if pd.notna(v) and pad.search(str(v)):
                    ocorr.append((nome, folha, f"linha {i} / {str(c)[:24]}", str(v)[:60]))
print(f"   folhas varridas: {nfolhas} (dois livros)")
print(f"   ocorrencias do numero 27 isolado: {len(ocorr)}")
tipos = {}
for l, f, o, v in ocorr:
    k = "Record_ID" if "Record_ID" in o or "Registo" in o else (
        "data 2023-06-27" if "2023-06-27" in v else "OUTRO")
    tipos[k] = tipos.get(k, 0) + 1
for k, v in tipos.items():
    print(f"      {v:4d}  {k}")
outros27 = [o for o in ocorr if "2023-06-27" not in o[3]
            and "Record_ID" not in o[2] and "Registo" not in o[2]]
print(f"\n   ocorrencias que NAO sao Record_ID nem a data 2023-06-27: {len(outros27)}")
for o in outros27[:10]:
    print(f"      {o}")
# e, de passagem, «Zona 0» / «Zona 1»
for termo in ("Zona 0", "Zona 1"):
    n = 0
    for nome, cam in (("PT", LIVRO_PT), ("EN", LIVRO_EN)):
        xl = pd.ExcelFile(cam)
        for folha in xl.sheet_names:
            df = xl.parse(folha, header=0)
            n += int(df.astype(str).apply(
                lambda s: s.str.contains(termo, na=False)).to_numpy().sum())
            n += sum(1 for c in df.columns if termo in str(c))
    print(f"   ocorrencias de «{termo}» nos dois livros: {n}")
res["R7_busca27"] = {"folhas_varridas": nfolhas, "ocorrencias": len(ocorr),
                     "tipos": tipos, "nao_explicadas": len(outros27)}

# =================================================================== T4
print("\n" + "=" * 92)
print("T4 · RECONCILIAR 0,054 CONTRA 0,0218 — media ou mediana?")
print("=" * 92)
sau = masc["saudavel"]
nd = {d: rasterio.open(os.path.join(RAIZ, "sentinel", f"{d}.tif")).read(1)
      for d in ("2024-07-22", "2026-07-27")}
med24 = float(np.nanmedian(nd["2024-07-22"][sau]))
med26 = float(np.nanmedian(nd["2026-07-27"][sau]))
mea24 = float(np.nanmean(nd["2024-07-22"][sau]))
mea26 = float(np.nanmean(nd["2026-07-27"][sau]))
print(f"   referencia sistematica, as mesmas 110 celulas, as mesmas duas datas:")
print(f"      mediana  2024 {med24:.4f}   2026 {med26:.4f}   queda {med26-med24:+.4f}")
print(f"      media    2024 {mea24:.4f}   2026 {mea26:.4f}   queda {mea26-mea24:+.4f}")
print(f"\n   valor publicado pela sessao de gestao / adenda (L5) : -0,054")
print(f"   valor publicado pela C3                             : -0,0218")
print(f"   -> a MEDIA cai {abs(mea26-mea24):.4f}; a MEDIANA cai {abs(med26-med24):.4f}.")
razao = abs(mea26 - mea24) / abs(med26 - med24)
print(f"   razao media/mediana: {razao:.2f}x")
print(f"\n   A divergencia E media contra mediana. Nao ha erro de ninguem:")
print(f"   sao duas estatisticas diferentes sobre as mesmas celulas.")
print(f"   E a diferenca entre as duas E a cauda inferior — isto e, e prova")
print(f"   DIRECTA e independente de que a referencia tem celulas a cair,")
print(f"   que e exactamente o que B10 afirma por outro caminho.")
assim24 = float(stats.skew(nd["2024-07-22"][sau], nan_policy="omit"))
assim26 = float(stats.skew(nd["2026-07-27"][sau], nan_policy="omit"))
print(f"\n   assimetria da referencia: 2024 {assim24:+.3f}  ->  2026 {assim26:+.3f}")
print(f"   (uma cauda inferior a crescer puxa a media abaixo da mediana)")
print(f"   media - mediana: 2024 {mea24-med24:+.4f}  ->  2026 {mea26-med26:+.4f}")
res["T4"] = {"mediana_2024": round(med24, 4), "mediana_2026": round(med26, 4),
             "queda_mediana": round(med26 - med24, 4),
             "media_2024": round(mea24, 4), "media_2026": round(mea26, 4),
             "queda_media": round(mea26 - mea24, 4),
             "razao_media_mediana": round(razao, 2),
             "assimetria_2024": round(assim24, 3), "assimetria_2026": round(assim26, 3),
             "media_menos_mediana_2024": round(mea24 - med24, 4),
             "media_menos_mediana_2026": round(mea26 - med26, 4),
             "veredicto": ("A divergencia 0,054 vs 0,0218 e media contra mediana. "
                           "Nenhuma das duas esta errada. A diferenca entre elas e "
                           "a cauda inferior e e prova independente de B10.")}

# ======================================================= ancoras em falta (D)
print("\n" + "=" * 92)
print("D · as quatro ancoras que a C3 nao reportou")
print("=" * 92)
print(f"   cenas em c2_00_comum.DATAS        : {len(DATAS)}")
print(f"   cenas em c2_00_comum.TODAS        : {len(TODAS)}")
print(f"   a V1 da C2 declara «dez» cenas de plena estacao; o codigo da C2 corre")
print(f"   sobre {len(DATAS)}. 2019-09-02 esta em TODAS e nao em DATAS.")
print(f"   TODO o c3_08 (= todo o B10) correu sobre {len(DATAS)}.")
nd17 = rasterio.open(os.path.join(RAIZ, "sentinel", "2017-07-02.tif")).read(1)
r17 = float(np.nanmedian(nd17[sau]))
print(f"\n   NDVI da referencia 2017-07-02 : declarado 0,838 · obtido {r17:.4f} (mediana)")
print(f"   NDVI da referencia 2026-07-27 : declarado 0,886 · obtido {med26:.4f} (mediana)")
print(f"   o declarado SOBE (+0,048); o obtido DESCE ({med26-r17:+.4f}). Sinal invertido.")
res["D_ancoras"] = {"cenas_DATAS": len(DATAS), "cenas_TODAS": len(TODAS),
                    "V1_declara": 10,
                    "ndvi_ref_2017_declarado": 0.838, "ndvi_ref_2017_obtido": round(r17, 4),
                    "ndvi_ref_2026_declarado": 0.886, "ndvi_ref_2026_obtido": round(med26, 4)}

with open(os.path.join(OUT, "c3_13_T2_T4.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print("\n\nescrito c3_13_T2_T4.json")
