# -*- coding: utf-8 -*-
"""O teste que a triagem nao faz: a UNIDADE, no espaco.

Nao estava nas perguntas. Sai da sobreposicao medida em `c3_05`.

A comparacao da REG-01 refeita poe, do lado de Ganfei, DOIS RECORTES INTERNOS de
um pomar de 30 ha — 2,18 e 0,76 ha, escolhidos por ser ali que o problema esta —
e, do outro lado, VINTE E NOVE PARCELAS ADMINISTRATIVAS INTEIRAS, de 0,54 a
11,33 ha, nenhuma delas recortada. Uma parcela inteira e uma media sobre o bom e
o mau; um recorte e so o mau.

Duas coisas se medem aqui:

  A · O FILTRO DE COPADO. As mascaras dos focos levam `& COM`, isto e, altura do
      CHM >= 0,5 m — LiDAR de 06-07-2025, que a propria LISTA_FINAL (C2) declara
      POS-TRATAMENTO. Retira 62 % da `zona0`. E uma mascara derivada do estado
      DEPOIS do acontecimento, aplicada a uma serie de 2017 a 2026. Corre-se a
      REG-01 com e sem ele.

  B · O MESMO PRIVILEGIO PARA TODOS. Para cada bloco sobrevivente calcula-se o
      degrau CELULA A CELULA e toma-se a media das k piores celulas, com k igual
      ao n dos focos. Duas variantes:
        · em amostra — escolhem-se e avaliam-se as piores nas mesmas cenas.
          E um limite superior, e diz-se que e;
        · fora de amostra — escolhem-se as piores k celulas SO com as cenas de
          2025 e avalia-se o degrau SO com as de 2026. Esta e honesta.
"""
import collections
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c3_00_comum import carregar, matriz

VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
C = os.path.join(VG, "_reg01_landsat_cache")
EXCL = {"6705427", "6705428", "6705429", "6705432", "6705442",
        "8845729", "8845731", "8845739"}
FOCOS = ["foco OCIDENTAL", "foco ORIENTAL"]

D = carregar()
datas, unid, V, PIX = matriz(D)
idx = {u: i for i, u in enumerate(unid)}
BLOCOS = [u for u in unid if u.isdigit()]
DENTRO = [c for c in BLOCOS if c not in EXCL]
D_i = np.array([idx[u] for u in DENTRO])

E10, N10, POMAR, ZONA0, COM = D["E10"], D["N10"], D["POMAR"], D["ZONA0"], D["COM"]
p30 = D["para30"]
DISCO = np.hypot(E10 - 530485., N10 - 4655053.) <= 90

VAR = {
    "com COM (o que a cadeia usa)":
        {"foco OCIDENTAL": p30(DISCO & POMAR & COM), "foco ORIENTAL": p30(ZONA0 & COM)},
    "SEM COM (sem o LiDAR de 2025)":
        {"foco OCIDENTAL": p30(DISCO & POMAR), "foco ORIENTAL": p30(ZONA0)},
}

# --------------------------------------------------------------- cenas validas
val = [k for k, d in enumerate(datas)
       if np.isfinite(V[k, D_i]).sum() >= 0.7 * len(D_i)]
MED = {}
for k in val:
    v = V[k, D_i]
    MED[k] = float(np.median(v[np.isfinite(v)]))


def degrau_de_mascara(m, cenas_pre, cenas_pos):
    """mediana das celulas por cena, menos a mediana regional; media por periodo."""
    out = {}
    for nome, ii in (("pre", cenas_pre), ("pos", cenas_pos)):
        acc = []
        for k in ii:
            nd = NDVI[k]
            a = nd[m]
            a = a[np.isfinite(a)]
            if a.size >= max(3, 0.5 * m.sum()):
                acc.append(float(np.median(a)) - MED[k])
        out[nome] = np.mean(acc) if acc else np.nan
    return out["pos"] - out["pre"]


# carregar os rasters uma vez (100 x NL x NC float32)
cen = json.load(open(os.path.join(VG, "reg01_landsat_cenas.json"), encoding="utf-8"))
fich = {}
for x in os.listdir(C):
    fich.setdefault(x[:10], x)
NDVI = {}
for k, d in enumerate(datas):
    NDVI[k] = np.load(os.path.join(C, fich[d]))["ndvi"]

PRE = [k for k in val if datas[k] < "2025"]
POS = [k for k in val if datas[k] >= "2025"]
P25 = [k for k in val if datas[k][:4] == "2025"]
P26 = [k for k in val if datas[k][:4] == "2026"]

DEG_BL = {c: (np.nanmean([V[k, idx[c]] - MED[k] for k in POS
                          if np.isfinite(V[k, idx[c]])])
              - np.nanmean([V[k, idx[c]] - MED[k] for k in PRE
                            if np.isfinite(V[k, idx[c]])])) for c in DENTRO}

print("=" * 100)
print("A · O FILTRO DE COPADO (`& COM`, CHM do voo de 06-07-2025)")
print("=" * 100)
print()
arr = np.array(sorted(DEG_BL.values()))
for nome, F in VAR.items():
    print("  %s" % nome)
    for f in FOCOS:
        m = F[f]
        g = degrau_de_mascara(m, PRE, POS)
        todos = sorted(list(DEG_BL.values()) + [g])
        lug = 1 + sum(1 for x in sorted(DEG_BL.values()) if x < g)
        print("     %-16s n30 = %3d (%.2f ha) · degrau %+0.4f · lugar %d de %d"
              % (f, m.sum(), m.sum() * 0.09, g, lug, len(DEG_BL) + 1))
    print()

print("  o que o filtro retira, em celulas de 10 m:")
print("     zona0            %3d -> %3d  (%.0f %% retirado)"
      % (ZONA0.sum(), (ZONA0 & COM).sum(),
         100 * (1 - (ZONA0 & COM).sum() / ZONA0.sum())))
print("     disco & pomar    %3d -> %3d  (%.0f %% retirado)"
      % ((DISCO & POMAR).sum(), (DISCO & POMAR & COM).sum(),
         100 * (1 - (DISCO & POMAR & COM).sum() / (DISCO & POMAR).sum())))

# ---------------------------------------------------------------- B sub-blocos
print()
print("=" * 100)
print("B · O MESMO PRIVILEGIO PARA TODOS — as k piores celulas de cada bloco")
print("=" * 100)


def cel_degrau(cenas_pre, cenas_pos):
    """degrau por celula de 30 m, para toda a grelha."""
    def m(ii):
        s = np.zeros(NDVI[val[0]].shape)
        n = np.zeros(NDVI[val[0]].shape)
        for k in ii:
            nd = NDVI[k] - MED[k]
            ok = np.isfinite(nd)
            s[ok] += nd[ok]
            n[ok] += 1
        return np.where(n >= 3, s / np.maximum(n, 1), np.nan)
    return m(cenas_pos) - m(cenas_pre)


G_IN = cel_degrau(PRE, POS)
G_SEL = cel_degrau(PRE, P25)          # escolha
G_AVA = cel_degrau(PRE, P26)          # avaliacao

M = D["M"]
FOC = VAR["com COM (o que a cadeia usa)"]
for K, ref in ((26, "foco OCIDENTAL"), (10, "foco ORIENTAL")):
    print()
    print("  --- k = %d celulas de 30 m (%.2f ha), o n do %s ---" % (K, K * 0.09, ref))
    gref_in = float(np.nanmean(G_IN[FOC[ref]]))
    gref_out = float(np.nanmean(G_AVA[FOC[ref]]))
    linhas = []
    for c in DENTRO:
        m = M[int(c)]
        if m.sum() < K:
            continue
        v = G_IN[m]
        v = v[np.isfinite(v)]
        if v.size < K:
            continue
        pior_in = float(np.mean(np.sort(v)[:K]))
        s = G_SEL[m]
        a = G_AVA[m]
        ok = np.isfinite(s) & np.isfinite(a)
        pior_out = np.nan
        if ok.sum() >= K:
            o = np.argsort(s[ok])[:K]
            pior_out = float(np.mean(a[ok][o]))
        linhas.append((c, int(m.sum()), DEG_BL[c], pior_in, pior_out))
    linhas.sort(key=lambda z: z[3])
    print("  %-10s %5s %11s %13s %14s" % ("bloco", "n30", "bloco todo",
                                          "k piores (em)", "k piores (fora)"))
    for c, n, dg, pin, pout in linhas[:8]:
        print("  %-10s %5d %+11.4f %+13.4f %+14s"
              % (c, n, dg, pin, "%.4f" % pout if np.isfinite(pout) else "."))
    print("  %-10s %5d %+11s %+13.4f %+14.4f   <== o foco"
          % (ref, int(FOC[ref].sum()), "-", gref_in, gref_out))
    n_pior_in = sum(1 for x in linhas if x[3] < gref_in)
    n_pior_out = sum(1 for x in linhas if np.isfinite(x[4]) and x[4] < gref_out)
    print()
    print("  blocos cujas k piores celulas batem o foco:  em amostra %d de %d  ·  "
          "fora de amostra %d de %d"
          % (n_pior_in, len(linhas), n_pior_out,
             sum(1 for x in linhas if np.isfinite(x[4]))))

json.dump(dict(nota="c3_06"), open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "c3_06_unidade.json"), "w"))
