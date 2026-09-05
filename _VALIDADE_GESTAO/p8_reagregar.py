# -*- coding: utf-8 -*-
"""P8b — reagrega do cache com a geometria do controlo CORRIGIDA.

Nao descarrega nada. E para isto que o `p8_cache/` existe: o adversario da C9
mostrou que a fronteira do controlo estava errada, e a correccao custa segundos
em vez de uma hora de rede.

O QUE ESTAVA ERRADO, e vinha herdado do p2 sem ninguem verificar
----------------------------------------------------------------
O pre-registo §2 diz que o CONTROLO fica «a > 90 m dos dois focos». O codigo
media a distancia ao **centroide** do poligono `zona0`, nao ao poligono. Medido:

    CTRL total                       : 2247 px
    CTRL a MENOS de 90 m do poligono :  220 px  (9,8 %)
    distancia real minima no CTRL    :   10 m   <- uma celula de distancia

Ou seja, quase um decimo do controlo encosta ao foco oriental. E forma A — o
controlo partilha vizinhanca com o que controla — e envenena a regra §7 duas
vezes: um controlo que se move com o foco faz um acontecimento real ler-se como
«fenologico».

Aqui a distancia e ao POLIGONO, celula a celula.

A SEGUNDA CORRECCAO: as tres cenas da serie em disco
-----------------------------------------------------
`2025-06-17`, `2025-08-14` e `2026-07-27` vem de `.tif` sem banda SCL. Na
primeira corrida entravam com a mascara §4 **desligada** e com `nuvens = NaN`,
o que as punha tambem fora da verificacao de correlacao obrigatoria. Sao dois
caminhos de codigo outra vez — exactamente o defeito 5 que o Controlo 4 registou
no p2, reproduzido no ficheiro escrito para o corrigir.

Aqui vao marcadas e **contam-se em separado**. A serie principal e so a das
cenas com SCL; as tres aparecem a parte, para o leitor ver o que mudaria.
"""
import io
import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Jackster2/Downloads/_VALIDACAO_CAMADAS")
try:
    from proveniencia import guardar
except ImportError:
    def guardar(d, c, **k):
        json.dump(d, io.open(c, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        return c

S2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
CACHE = os.path.join(VG, "p8_cache")
AOI = (529950, 4654600, 531950, 4655600)
NL, NC = 100, 200
SCL_MAU = (1, 2, 3, 7, 8, 9, 10, 11)   # + 1 saturado, 2 sombra topografica,
VALIDO_MIN = 0.60                      #   7 nao classificado — sombra de sol
                                       #   baixo a 42 N, que era o que faltava

g = json.load(open(os.path.join(S2, "sentinel", "masks_geograficas.json")))
bits = lambda k: np.array([[c == "1" for c in L] for L in g[k]], bool)
POMAR, REF, ZONA0 = bits("pomar_bits"), bits("saudavel_bits"), bits("zona0_bits")
h = np.load(os.path.join(VG, "chm_altura.npy"))
COM = np.isfinite(h) & (h >= 0.5)
EE, NN = np.meshgrid(AOI[0] + (np.arange(NC) + .5) * 10.,
                     AOI[3] - (np.arange(NL) + .5) * 10.)
C_OC = (530485.0, 4655053.0)

# ── distancia ao POLIGONO, nao ao centroide ─────────────────────────────────
ze, zn = EE[ZONA0], NN[ZONA0]
d_ori = np.empty((NL, NC))
for i in range(NL):
    for j in range(NC):
        d_ori[i, j] = np.min(np.hypot(EE[i, j] - ze, NN[i, j] - zn))
d_oc = np.hypot(EE - C_OC[0], NN - C_OC[1])
dfoco = np.minimum(d_oc, d_ori)

DOC = (d_oc <= 90) & POMAR & COM
DOR = ZONA0 & COM
CTRL = POMAR & COM & (dfoco > 90) & ~ZONA0 & ~REF
UN = [("OCIDENTAL", DOC), ("ORIENTAL", DOR), ("CONTROLO", CTRL)]

print("geometria corrigida:")
print("  OCIDENTAL %4d px · ORIENTAL %4d px · CONTROLO %4d px"
      % (DOC.sum(), DOR.sum(), CTRL.sum()))
print("  distancia minima do CTRL ao poligono oriental: %.0f m" % dfoco[CTRL].min())
print()

linhas = []
for f in sorted(os.listdir(CACHE)):
    if not f.endswith(".npz"):
        continue
    d = f[:-4]
    z = np.load(os.path.join(CACHE, f))
    ndvi, scl = z["ndvi"], z["scl"]
    meta = json.loads(str(z["meta"]))
    tem_scl = bool(np.nanmax(scl))
    mau = np.isin(np.nan_to_num(scl, nan=0).astype("int16"), SCL_MAU) \
        if tem_scl else np.zeros((NL, NC), bool)
    bom = np.isfinite(ndvi) & ~mau

    lin = {"data": d, "cena": meta["cena"], "plataforma": meta["plataforma"],
           "nuvens_cena": meta["nuvens"], "scl": bool(tem_scl)}
    ok = tem_scl                      # sem SCL nao entra na serie principal
    for nome, m in UN:
        v = ndvi[m & bom]
        frac = float((m & bom).sum()) / float(m.sum())
        lin["%s_valido" % nome] = round(frac, 4)
        lin[nome] = float(np.median(v)) if v.size else float("nan")
        if frac < VALIDO_MIN:
            ok = False
    lin["retida"] = bool(ok)
    lin["contraste_OC"] = lin["OCIDENTAL"] - lin["CONTROLO"]
    lin["contraste_OR"] = lin["ORIENTAL"] - lin["CONTROLO"]
    linhas.append(lin)

ret = [l for l in linhas if l["retida"]]
sem = [l for l in linhas if not l["scl"]]
caiu = [l for l in linhas if l["scl"] and not l["retida"]]

# ── a verificacao obrigatoria do §4, agora sobre a serie principal ──────────
n = np.array([l["nuvens_cena"] for l in ret])
r = {}
for k in ("contraste_OC", "contraste_OR"):
    v = np.array([l[k] for l in ret])
    r[k] = float(np.corrcoef(n, v)[0, 1])
    print("%s  r(nuvem, contraste) = %+.3f  (n=%d)" % (k, r[k], len(v)))
print("§4 exige |r| <= 0,40")
print()
print("na serie principal: %d datas · sem SCL (a parte): %d · caidas pelos 60 %%: %d"
      % (len(ret), len(sem), len(caiu)))
print("  sem SCL :", [l["data"] for l in sem])
print("  caidas  :", [l["data"] for l in caiu])

guardar({"corrige": "p8_vao.json — fronteira do controlo ao POLIGONO, nao ao "
                    "centroide; SCL alargada a 1,2,7; cenas sem SCL a parte",
         "geometria": {"OCIDENTAL_px": int(DOC.sum()),
                       "ORIENTAL_px": int(DOC.sum() * 0 + DOR.sum()),
                       "CONTROLO_px": int(CTRL.sum()),
                       "min_dist_ctrl_ao_poligono_m": float(dfoco[CTRL].min())},
         "scl_excluidas": list(SCL_MAU), "valido_min": VALIDO_MIN,
         "r_nuvem_contraste": r,
         "n_principal": len(ret), "n_sem_scl": len(sem), "n_caidas": len(caiu),
         "serie": linhas},
        os.path.join(VG, "p8_reagregado.json"))
print()
print("escrito p8_reagregado.json")
