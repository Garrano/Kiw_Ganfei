# -*- coding: utf-8 -*-
"""Teste negativo da guarda de cultura: tem de PASSAR no ficheiro real e
DISPARAR num poluido. Corre o bloco literal de cada script. Nao escreve nada."""
import io, json, copy

P = r"C:\Users\Jackster2\Downloads\_MULTIVERSO\SAIDA_H2_patologista\ifap_kiwi_largo.json"
REAL = json.load(open(P, encoding="utf-8"))
REAL = REAL["features"] if isinstance(REAL, dict) else REAL
FIM = 'REGISTO_REG01_GUARDA_2026-09-01.md.")'

def extrai(nome):
    txt = io.open(nome, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    i = txt.index("# --- guarda de cultura")
    j = txt.index(FIM, i) + len(FIM)
    return txt[i:j]

for nome in ("reg01_local_ou_regional.py", "reg01_landsat.py", "reg01_landsat_r3.py"):
    src = extrai(nome)
    ok, err = True, ""
    try:
        exec(compile(src, nome, "exec"), {"KF": REAL})
    except SystemExit as e:
        ok, err = False, str(e)
    mau = copy.deepcopy(REAL[:3])
    mau[1]["properties"]["PUN_CUL_COD"] = "231"          # vinha
    disparou, msg = False, ""
    try:
        exec(compile(src, nome, "exec"), {"KF": mau})
    except SystemExit as e:
        disparou, msg = True, str(e)
    print("RESULTADO %-30s real=%-6s poluido_dispara=%s"
          % (nome, "passa" if ok else "FALHA", disparou))
    if not ok:
        print("          FALSO POSITIVO: %s" % err)
    if disparou:
        print("          mensagem: %s" % msg.split(".")[0])
