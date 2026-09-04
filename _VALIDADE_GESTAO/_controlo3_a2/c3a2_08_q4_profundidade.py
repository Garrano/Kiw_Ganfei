# -*- coding: utf-8 -*-
"""C3/A2 · 08 — Q4: «nao esta no CSV» contra «nao foi medida».

O D9 verificou CINCO campos do `c3_04_registo_principal.csv`. Este ficheiro
pergunta se eram os campos certos, e vai a montante: aos dois livros de
Excel de que o CSV foi extraido, e depois procura os nove PDF de origem.
"""
import os, re, sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3a2_00_dados import carrega

DL = r"C:\Users\Jackster2\Downloads"
PT = os.path.join(DL, "Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx")
EN = os.path.join(DL, "Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx")
PDFS = ["B1_C1_Julho.pdf","B1_C3_Julho.pdf","B1_C4_Julho.pdf",
        "B2_V7__Junho_26.pdf","B2_V7__Marc_o_26.pdf","B3_7ha_Marc_o_26.pdf",
        "B4_Julho.pdf","Erica_2016_E__Marc_o_26.pdf","Erica_2016_R__Marc_o_26.pdf"]

print("="*100)
print("A · os CINCO campos do D9 — o que continham, mesmo")
print("="*100)
A = carrega("c3_04_registo_principal.csv")
R = [x for x in A if "sico-Qu" in str(x.get("Doc_Type",""))]
for c in ("Notes","Matrix","Method","Test_Category","Interpretation"):
    v = {str(x.get(c,"")) for x in R}
    vaz = sum(1 for x in R if not str(x.get(c,"")).strip())
    print("  %-15s distintos=%-3d vazios=%-4d  exemplo: %s"
          % (c, len(v), vaz, sorted(v)[0][:60] if v else ""))
print("""
  `Notes` esta VAZIO nos 108 registos — 108 de 108. `Matrix` tem um unico
  valor («Solo»), `Test_Category` um unico («Fisico-quimica»), `Interpretation`
  e o nome do parametro, `Method` e a norma analitica. **Nenhum dos cinco e um
  campo de metadados de COLHEITA.** Nao ha, no esquema do CSV, coluna nenhuma
  onde uma profundidade pudesse estar. Procurar profundidade nestes cinco e um
  teste sem ramo de refutacao: nao podia ter encontrado, e nao encontrou.
""")

print("="*100)
print("B · a montante: os dois livros de Excel, e o que o D9 nao abriu")
print("="*100)
alvo = re.compile(r"profund|depth|\bcm\b|0\s*[-–]\s*(20|30)|20\s*cm|30\s*cm", re.I)
for f, nome in ((PT, "PT"), (EN, "EN")):
    x = pd.ExcelFile(f)
    achados = []
    for sh in x.sheet_names:
        d = pd.read_excel(f, sheet_name=sh).astype(str)
        for c in d.columns:
            if alvo.search(str(c)): achados.append((sh, "coluna", str(c)[:70]))
            for v in d[c].unique():
                if alvo.search(v): achados.append((sh, c[:22], v[:70]))
    print("  %s — %d celulas com mencao a profundidade em %d folhas"
          % (nome, len(achados), len(x.sheet_names)))
    for a in achados[:12]: print("     %s | %s | %s" % a)

print()
print("="*100)
print("C · A FOLHA QUE O D9 NAO LEU, e o que ela mostra")
print("="*100)
pt = pd.read_excel(PT, sheet_name="Fisico-Quimica por Talhao").astype(str)
en = pd.read_excel(EN, sheet_name="Soil Chemistry by Block").astype(str)
print("  PT «Fisico-Quimica por Talhao» : %d parametros x %d talhoes"
      % (pt.shape[0], pt.shape[1]-1))
print("  EN «Soil Chemistry by Block»   : %d parametros x %d talhoes"
      % (en.shape[0], en.shape[1]-1))
falta_en = set(pt.iloc[:,0]) - set(en.iloc[:,0])
print("  parametro que so a PT tem: %s" % (falta_en or "nenhum"))
npage = 0
for c in en.columns[1:]:
    for i, v in enumerate(en[c]):
        if "page 2 not extracted" in v:
            npage += 1
            print("     EN diz «page 2 not extracted»: %-22s %-30s | PT diz: %s"
                  % (en.iloc[i,0][:22], c[:30],
                     str(pt[pt.iloc[:,0]==en.iloc[i,0]][c].values[:1])[:34]))
print()
print("  celulas que a extraccao EN marca como NAO EXTRAIDAS: %d" % npage)
print("""
  ISTO E O PONTO. **Existe uma pagina 2 nestes boletins que pelo menos uma
  extraccao nao leu**, e a outra extraccao poe la numeros. O `c3_03` ja tinha
  registado o mesmo para o Azoto Total (nove linhas em falta no livro EN).
  Um boletim de laboratorio A2 declara a profundidade de colheita no
  cabecalho da amostra — que e exactamente o material que nao passou para
  nenhuma tabela. Portanto:

    · «a profundidade nao esta em campo nenhum do CSV»  -> VERDADE, e trivial:
      o CSV nao tem campo de colheita nenhum.
    · «a profundidade nao esta declarada»               -> NAO SABIDO. Ha
      pagina por ler, e ha prova de que ha pagina por ler.
""")
print("="*100)
print("D · os nove PDF de origem estao em disco?")
print("="*100)
achou = []
for raiz in (DL, r"C:\Users\Jackster2\Documents", r"C:\Users\Jackster2\Desktop"):
    for dp, dn, fn in os.walk(raiz):
        for f in fn:
            if f in PDFS: achou.append(os.path.join(dp, f))
        if len(achou) >= 9: break
print("  encontrados: %d de 9" % len(achou))
for a in achou: print("   ", a)
if not achou:
    print("""
  NENHUM. Os nove PDF nao estao nesta maquina — so as duas extraccoes em
  Excel e o CSV derivado delas. **Nao posso decidir a Q4 por leitura do
  original, e ninguem pode com o que esta em disco.** O D9 tambem nao podia,
  e nao o diz: escreve a ausencia como se fosse uma verificacao do documento.
""")
