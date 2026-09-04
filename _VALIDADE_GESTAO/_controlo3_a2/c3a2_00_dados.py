# -*- coding: utf-8 -*-
"""C3/A2 · 00 — leitura crua dos registos de fisico-quimica, sem filtro do alvo."""
import csv, io, os, json, collections

C3 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C3"
OUT = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO\_controlo3_a2"

def ler(f, base=C3):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return io.open(os.path.join(base, f), encoding=enc).read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise IOError(f)

def carrega(f, base=C3):
    t = ler(f, base)
    d = ";" if t[:300].count(";") > t[:300].count(",") else ","
    return list(csv.DictReader(io.StringIO(t), delimiter=d))

if __name__ == "__main__":
    A = carrega("c3_04_registo_principal.csv")
    print("registo principal: %d linhas, %d colunas" % (len(A), len(A[0])))
    print()
    print("--- todos os Doc_Type distintos ---")
    for k, n in collections.Counter(x["Doc_Type"] for x in A).most_common():
        print("  %4d  %s" % (n, k))
    print()
    R = [x for x in A if "sico-Qu" in str(x.get("Doc_Type",""))]
    print("filtro 'sico-Qu': %d" % len(R))
    print()
    print("--- Source_File dos fisico-quimicos ---")
    for k, n in sorted(collections.Counter(x["Source_File"] for x in R).items()):
        print("  %4d  %s" % (n, k))
    print()
    print("--- Report_No x Terrain_Block_Parcel x Source_File ---")
    seen = {}
    for x in R:
        key = (x["Report_No"], x["Terrain_Block_Parcel"], x["Source_File"],
               x["Sample_Date"], x["Client_Titular"], x["Parcelario_No"],
               x["Parish_Municipality"])
        seen.setdefault(key, 0)
        seen[key] += 1
    for k, n in sorted(seen.items()):
        print("  n=%2d  rep=%s | bloco=%r | src=%s" % (n, k[0], k[1], k[2]))
        print("        data=%s | titular=%r | parcelario=%r | freg=%r"
              % (k[3], k[4], k[5], k[6]))
    print()
    print("--- parametros por boletim ---")
    per = collections.defaultdict(list)
    for x in R:
        per[x["Report_No"]].append(x["Organism_Parameter"])
    for b in sorted(per):
        print("  %s : %d" % (b, len(per[b])))
