# -*- coding: utf-8 -*-
"""C1-07 — verificar a retirada da linha termica.

A afirmacao a verificar: "a linha termica foi retirada como sinal independente
porque dT correlaciona com dNDVI a r = -0,756". Nao se ressuscita a linha sem
prova nova; o que se faz aqui e confirmar que a retirada esta bem fundada, e
declarar o que ela nao prova.

Fonte: `audit_termico.csv` (137 cenas Landsat 8/9, Abr-Set 2017-2026, nuvens
< 25 %). Atencao: as mascaras desse ficheiro sao as antigas de `masks.json`,
e o vocabulario esta invertido — `manchaW` = FOCO OESTE, `zona0` = FOCO ESTE.
"""
import os, sys, csv, json
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c1_00_comum import *

f = os.path.join(RAIZ, "audit_termico.csv")
rows = list(csv.DictReader(open(f, encoding="utf-8")))
print("cenas no ficheiro: %d | primeira %s | ultima %s"
      % (len(rows), rows[0]["data"], rows[-1]["data"]))
CH = ["saudavel_st", "saudavel_ndvi", "manchaW_st", "manchaW_ndvi",
      "zona0_st", "zona0_ndvi", "controlo_st", "controlo_ndvi", "t_ar", "nuvens"]
n0 = len(rows)
rows = [r for r in rows if all(str(r.get(k, "")).strip() not in ("", "nan") for k in CH)]
print("cenas com todas as colunas: %d (descartadas %d incompletas)" % (len(rows), n0 - len(rows)))
col = lambda k: np.array([float(r[k]) for r in rows])
data = np.array([r["data"] for r in rows])
ano = np.array([int(r["data"][:4]) for r in rows])
doy = np.array([(np.datetime64(r["data"]) - np.datetime64(r["data"][:4] + "-01-01")).astype(int) + 1
                for r in rows])

sau_t, sau_n = col("saudavel_st"), col("saudavel_ndvi")
# vocabulario corrigido (R2 G34 / REGISTO_DE_NOMES)
oes_t, oes_n = col("manchaW_st"), col("manchaW_ndvi")
est_t, est_n = col("zona0_st"), col("zona0_ndvi")
ctl_t, ctl_n = col("controlo_st"), col("controlo_ndvi")
tar = col("t_ar")

print("\n=== (1) a correlacao que justifica a retirada ===")
for nome, t, n in (("FOCO OESTE (ex-manchaW)", oes_t, oes_n),
                   ("FOCO ESTE  (ex-zona0)", est_t, est_n),
                   ("controlo interno", ctl_t, ctl_n)):
    dT, dN = t - sau_t, n - sau_n
    r, p = stats.pearsonr(dT, dN)
    rs, ps = stats.spearmanr(dT, dN)
    b = stats.linregress(dN, dT)
    print("%-24s n=%3d  Pearson r=%+.3f (p=%.1e)  Spearman=%+.3f  declive %.2f K por unidade de NDVI  r2=%.3f"
          % (nome, len(dT), r, p, rs, b.slope, b.rvalue ** 2))

# a agregacao das duas manchas, que e o que a afirmacao original media
dT_all = np.concatenate([oes_t - sau_t, est_t - sau_t])
dN_all = np.concatenate([oes_n - sau_n, est_n - sau_n])
r_all, p_all = stats.pearsonr(dT_all, dN_all)
print("\nas duas manchas juntas: r = %+.3f (p=%.1e), n=%d" % (r_all, p_all, len(dT_all)))
print("valor declarado na retirada: -0,756")
print("=> reproduzido? %s" % ("SIM, dentro de 0,05" if abs(abs(r_all) - 0.756) < 0.05 else
                              "NAO exactamente — ver abaixo"))

# ---- variantes, para saber quao robusta e a correlacao ----
print("\n=== (2) robustez: a mesma correlacao noutras janelas ===")
sel = {"todas": np.ones(len(rows), bool),
       "plena estacao (doy 150-260)": (doy >= 150) & (doy <= 260),
       "nuvens < 10 %": col("nuvens") < 10,
       "2017-2021": ano <= 2021, "2022-2026": ano >= 2022}
for nome, m in sel.items():
    dT = np.concatenate([(oes_t - sau_t)[m], (est_t - sau_t)[m]])
    dN = np.concatenate([(oes_n - sau_n)[m], (est_n - sau_n)[m]])
    if len(dT) < 8:
        continue
    r, p = stats.pearsonr(dT, dN)
    print("  %-28s n=%3d  r=%+.3f  p=%.1e" % (nome, len(dT), r, p))

print("\n=== (3) resta sinal termico depois de tirar o NDVI? ===")
# residuo de dT depois de regredir em dNDVI: tem tendencia temporal?
for nome, t, n in (("FOCO OESTE", oes_t, oes_n), ("FOCO ESTE", est_t, est_n)):
    dT, dN = t - sau_t, n - sau_n
    b = stats.linregress(dN, dT)
    res = dT - (b.slope * dN + b.intercept)
    anos = ano + doy / 365.25
    tr = stats.linregress(anos, res)
    print("  %-11s residuo de dT|dNDVI: dp %.3f K | tendencia %+.4f K/ano (p=%.2f, r2=%.3f)"
          % (nome, res.std(), tr.slope, tr.pvalue, tr.rvalue ** 2))
    # o residuo depende da temperatura do ar? (controlo de condicoes)
    ra, pa = stats.pearsonr(res, tar)
    print("  %-11s residuo vs temperatura do ar: r=%+.3f (p=%.2f)" % ("", ra, pa))

print("\n=== (4) niveis absolutos, para o registo ===")
print("%-12s %8s %8s %8s" % ("", "dT medio", "dp", "dNDVI medio"))
for nome, t, n in (("FOCO OESTE", oes_t, oes_n), ("FOCO ESTE", est_t, est_n),
                   ("controlo", ctl_t, ctl_n)):
    print("%-12s %+8.3f %8.3f %+8.4f" % (nome, (t - sau_t).mean(), (t - sau_t).std(),
                                          (n - sau_n).mean()))
print("LST da referencia: %.2f..%.2f C (mediana %.2f) | t_ar %.1f..%.1f C"
      % (sau_t.min(), sau_t.max(), np.median(sau_t), tar.min(), tar.max()))

print("\n=== (5) o que a retirada NAO prova ===")
print("A correlacao dT~dNDVI diz que as duas medidas nao sao independentes na")
print("mesma cena. Nao diz que a temperatura de superficie e irrelevante: diz")
print("que, com estes dados, nao acrescenta informacao ao NDVI. Um teste que a")
print("separasse precisaria de LST nocturna (sem forcamento solar directo do")
print("copado) ou de medicao de temperatura do solo no terreno. Nem uma nem")
print("outra existe neste conjunto.")

json.dump({"n_cenas": len(rows), "r_pearson_agregado": float(r_all),
           "r_declarado": -0.756,
           "r_foco_oeste": float(stats.pearsonr(oes_t - sau_t, oes_n - sau_n)[0]),
           "r_foco_este": float(stats.pearsonr(est_t - sau_t, est_n - sau_n)[0])},
          open(os.path.join(SAIDA, "c1_07_termico.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nescrito c1_07_termico.json")
