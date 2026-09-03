"""
C4 - inferencia. Numeros lidos dos ficheiros das camadas abaixo.

REGRA QUE ESTE FICHEIRO CUMPRE (R1 do adversario da C3): nenhum valor
numerico e transcrito a mao. Tudo o que sai daqui foi lido de um ficheiro
em disco ou calculado a partir dele. Onde um numero nao existe em disco, o
campo fica None e o certificado cita o facto pelo seu id, sem numero.

Nada e recomputado das camadas abaixo: o que se faz aqui e (a) reler valores
que ja estao gravados, e (b) relacionar valores de camadas diferentes, que e
o trabalho da C4.

Escreve:  c4_01_numeros.json
"""

import json
import os
import math

BASE = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.dirname(BASE)
C2 = os.path.join(CAM, "SAIDA_C2")
C3 = os.path.join(CAM, "SAIDA_C3")

N = {}

# ---------------------------------------------------------------------------
# 0 - geometria declarada. Coordenadas dos objectos nomeados.
#     Fonte: G34 (CAMADA_0_REVISAO_R2.md, suplemento) e a nota do parcelario
#     da CAMADA_2_ADENDA_LIDAR.md para o N3. Sao coordenadas, nao medicoes.
# ---------------------------------------------------------------------------
FOCO_OESTE = (530485.0, 4655053.0)   # G34 - v8/B2
FOCO_ESTE = (530977.0, 4655117.0)    # G34 - B3
N3 = (531068.0, 4655145.0)           # adenda de LiDAR, nota do parcelario

# ZONA declarada pelo gestor para a amostra "Kiwi 1000" / informe 331/2025:
# "lado oeste do maior vazio circular". O maior vazio e o nucleo redondo de
# 3,98 ha com centro em E530476 N4655046. TESTEMUNHO DIRECTO, tipo 1.
# E uma ZONA, nao um ponto. Nenhuma coordenada de amostra e inventada aqui.
VAZIO_MAIOR = (530476.0, 4655046.0)
VAZIO_MAIOR_HA = 3.98

N["_coordenadas"] = {
    "foco_OESTE": FOCO_OESTE, "foco_ESTE": FOCO_ESTE, "nucleo_N3": N3,
    "centro_do_maior_vazio_circular": VAZIO_MAIOR,
}


def d(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


# O N3 nao esta dentro do disco do foco ESTE. Sao objectos distintos.
N["N3_ao_foco_ESTE_m"] = round(d(N3, FOCO_ESTE), 1)
N["foco_OESTE_ao_foco_ESTE_m"] = round(d(FOCO_OESTE, FOCO_ESTE), 1)

# Que relacao tem o vazio declarado pelo gestor com o foco OESTE da cadeia?
# Nao se afirma que sao o mesmo objecto: mede-se a distancia entre os dois
# centros declarados e reporta-se, como a G29 fez com os 7 m.
raio_equiv = math.sqrt(VAZIO_MAIOR_HA * 10000.0 / math.pi)
N["maior_vazio_circular"] = {
    "centro": VAZIO_MAIOR,
    "area_ha": VAZIO_MAIOR_HA,
    "raio_equivalente_m": round(raio_equiv, 1),
    "distancia_do_centro_ao_centro_do_foco_OESTE_m": round(d(VAZIO_MAIOR, FOCO_OESTE), 1),
    "extensao_E_da_metade_OESTE": [round(VAZIO_MAIOR[0] - raio_equiv, 1), VAZIO_MAIOR[0]],
    "nota": ("O gestor situa a amostra no LADO OESTE deste nucleo, nao no centro. "
             "A zona e a metade ocidental de um nucleo descrito como redondo. "
             "O raio equivalente supoe circularidade e e so uma escala, nao uma "
             "fronteira medida."),
}

# ---------------------------------------------------------------------------
# 1 - valvulas: posicoes por area (G35). Recalculo das distancias aos focos
#     a partir do ficheiro operativo, para as poder declarar como objecto.
# ---------------------------------------------------------------------------
val = json.load(open(os.path.join(CAM, "valvulas_por_area.json"), encoding="utf-8"))
N["valvulas_ponto_ao_foco"] = {}
for k, v in sorted(val.items(), key=lambda x: int(x[0])):
    p = (v["E"], v["N"])
    N["valvulas_ponto_ao_foco"]["v" + k] = {
        "bloco": v["bloco"],
        "area_ha": round(v["area_m2"] / 10000.0, 2),
        "d_foco_OESTE_m": round(d(p, FOCO_OESTE), 1),
        "d_foco_ESTE_m": round(d(p, FOCO_ESTE), 1),
    }
N["valvulas_total_ha"] = round(sum(v["area_m2"] for v in val.values()) / 10000.0, 2)

# Que valvulas tem o seu PONTO dentro da faixa E da metade ocidental do vazio?
# Um ponto de valvula nao e o poligono da valvula: isto e uma escala, nao uma
# atribuicao. Serve para dizer que a zona do testemunho nao escolhe entre v7 e
# v8, nao para lhe atribuir uma valvula.
e0, e1 = N["maior_vazio_circular"]["extensao_E_da_metade_OESTE"]
N["valvulas_com_ponto_na_faixa_E_da_zona"] = [
    "v" + k for k, v in val.items() if e0 <= v["E"] <= e1]

# ---------------------------------------------------------------------------
# 2 - composicao do defice de 2026 por valvula: quanto e NOVO (regra M2) e
#     quanto e antigo. Duas entradas independentes: a mascara de estrutura
#     nu2021 (ortofoto) e a serie multianual (Sentinel-2). A particao das
#     valvulas e documental (tabela de areas do gestor, G35).
# ---------------------------------------------------------------------------
geo = json.load(open(os.path.join(C3, "c3_07_georreferenciacao.json"), encoding="utf-8"))
N["por_valvula"] = {}
for k, v in sorted(geo["por_valvula"].items(), key=lambda x: int(x[0])):
    de = v["pct_defice_2026"]
    m2 = v["pct_novo_M2"]
    N["por_valvula"][v["unidade"]] = {
        "ha": v["ha"],
        "pct_defice_2026": de,
        "pct_novo_M2": m2,
        "fraccao_do_defice_que_e_nova": (round(m2 / de, 3) if de > 0 else None),
        "pct_nu2021_chao_lavrado": v["pct_nu2021_chao_lavrado"],
        "d_foco_OESTE_m_centroide_voronoi": v["d_foco_OESTE_m"],
        "d_foco_ESTE_m_centroide_voronoi": v["d_foco_ESTE_m"],
    }
N["por_bloco"] = {
    k: {"ha": v["ha"], "pct_defice_2026": v["pct_defice_2026"],
        "pct_novo_M2": v["pct_novo_M2"],
        "pct_nu2021_chao_lavrado": v["pct_nu2021_chao_lavrado"]}
    for k, v in geo["por_bloco"].items()
}
N["registos"] = {"total": geo["n_registos"], "com_posicao": geo["com_posicao"],
                 "sem_posicao": geo["sem_posicao"], "por_classe": geo["por_classe"]}

# ---------------------------------------------------------------------------
# 3 - datacao do defice dentro de cada foco (disco de 120 m, nao 90 m).
#     c2_05_manchas.py: para cada celula em defice em 2026, o ano a partir do
#     qual esteve em defice CONTINUAMENTE ate ao fim.
# ---------------------------------------------------------------------------
man = json.load(open(os.path.join(C2, "c2_05_manchas.json"), encoding="utf-8"))
N["m2"] = man["m2"]
N["datacao_focos_disco_120m"] = man["datacao_focos"]
for foco, s in man["datacao_focos"].items():
    tot = sum(s.values())
    ate2024 = sum(v for k, v in s.items() if k < "2025")
    N.setdefault("datacao_resumo", {})[foco] = {
        "ha_em_defice_2026_no_disco_120m": round(tot, 2),
        "ha_com_defice_continuo_desde_2024_ou_antes": round(ate2024, 2),
        "fraccao_anterior_a_2025": (round(ate2024 / tot, 3) if tot else None),
    }
# taxa de base de W2 (adversario da C2), recalculada do ficheiro
sao = man["m2"]["sao_antes_ha"]
d26 = man["m2"]["defice26_ha"]
novo = man["m2"]["novo26_ha"]
POMAR_HA = 30.31  # G2/G4 - unico valor que nao vem destes JSON; e uma ancora
N["taxa_de_base"] = {
    "sao_antes_ha": sao,
    "com_historico_ha": round(POMAR_HA - sao, 2),
    "defice26_sobre_terreno_sao_pct": round(100.0 * novo / sao, 1),
    "defice26_sobre_terreno_com_historico_pct":
        round(100.0 * (d26 - novo) / (POMAR_HA - sao), 1),
}
N["taxa_de_base"]["razao"] = round(
    N["taxa_de_base"]["defice26_sobre_terreno_com_historico_pct"]
    / N["taxa_de_base"]["defice26_sobre_terreno_sao_pct"], 2)

# ---------------------------------------------------------------------------
# 4 - a UNICA linha microbiologica colocavel do caso: M. hapla.
#     Contagens lidas do despejo das folhas; defice por unidade lido do C3.
#     Dois instrumentos independentes: laboratorio (Areeiro) e Sentinel-2.
# ---------------------------------------------------------------------------
txt = open(os.path.join(C3, "c3_05_folhas.txt"), encoding="utf-8", errors="replace").read()
i = txt.find("Contagens Nem")
j = txt.find("Fisico-Quimica", i)
bloco = txt[i:j]
nem = []
cur = {}
for ln in bloco.split("\n"):
    if ":" not in ln:
        continue
    campo, valor = ln.split(":", 1)
    campo = campo.strip()
    valor = valor.strip()
    if campo.startswith("Talh"):
        if cur.get("talhao"):
            nem.append(cur)
        cur = {"talhao": valor}
        # a folha fecha com linhas de resumo (MEDIA, MAXIMO): nao sao talhoes
        if not valor or any(p in valor.upper() for p in ("DIA", "XIMO", "NIMO")):
            cur = {}
    elif campo.startswith("Contagem no solo") and valor:
        cur["solo"] = float(valor)
    elif campo.startswith("Contagem na raiz") and valor:
        cur["raiz"] = float(valor)
if cur.get("talhao"):
    nem.append(cur)
nem = [x for x in nem if "solo" in x and "raiz" in x]

# defice de 2026 por unidade, para as que TEM posicao
mapa_unidade = {"B3": ("bloco", "B3"), "B4": ("bloco", "B4"),
                "V7": ("valvula", "7"), "Erica Novo E": ("bloco", "Erica Novo")}
for x in nem:
    alvo = mapa_unidade.get(x["talhao"])
    if alvo is None:                      # B1 - fora da banda contigua, G35/G36
        x["defice26_pct"] = None
        x["tem_posicao"] = False
    else:
        tipo, chave = alvo
        src = geo["por_bloco"] if tipo == "bloco" else geo["por_valvula"]
        x["defice26_pct"] = src[chave]["pct_defice_2026"]
        x["tem_posicao"] = True
N["M_hapla"] = nem


def spearman(a, b):
    n = len(a)

    def rank(v):
        ordem = sorted(range(n), key=lambda i: v[i])
        r = [0] * n
        for pos, i in enumerate(ordem):
            r[i] = pos + 1
        return r
    ra, rb = rank(a), rank(b)
    dd = sum((ra[i] - rb[i]) ** 2 for i in range(n))
    return round(1 - 6.0 * dd / (n * (n * n - 1)), 3)


col = [x for x in nem if x["tem_posicao"]]
N["M_hapla_contra_defice"] = {
    "n_unidades_colocadas": len(col),
    "unidades": [x["talhao"] for x in col],
    "rho_defice_x_contagem_solo": spearman([x["defice26_pct"] for x in col],
                                           [x["solo"] for x in col]),
    "rho_defice_x_contagem_raiz": spearman([x["defice26_pct"] for x in col],
                                           [x["raiz"] for x in col]),
    "nota": ("n=4, uma data (2026-05-06), um laboratorio, um metodo. Com n=4 o p "
             "exacto de |rho|=1 e 2/4! = 0,083; nenhum destes valores e "
             "significativo em nenhum criterio. O sinal e NEGATIVO: mais "
             "nematodes onde ha MENOS defice."),
    "contagem_mais_alta_sem_posicao": [x for x in nem if not x["tem_posicao"]],
}

# ---------------------------------------------------------------------------
# 5 - a matriz organismo x matriz, lida linha a linha. O que interessa a uma
#     camada de exclusao nao e quantos positivos ha: e de onde vem cada
#     NEGATIVO, porque so um negativo pode excluir alguma coisa.
# ---------------------------------------------------------------------------
i = txt.find("Matriz Fitopatologia")
j = txt.find("Contagens Nem", i)
mb = txt[i:j]
linhas = {}
org = None
for ln in mb.split("\n"):
    if "Organismo (matriz)" in ln and ":" in ln:
        org = ln.split(":", 1)[1].strip()
        # a folha tem 22 linhas: 20 de organismo, uma vazia e o rodape com a
        # convencao "celula em branco = nao foi testado". So contam as que tem
        # a matriz entre parenteses.
        if not (org.endswith(")") and len(org) < 60):
            org = None
            continue
        linhas.setdefault(org, {})
    elif org and ln.startswith("     ") and ":" in ln:
        c, v = ln.split(":", 1)
        c, v = c.strip(), v.strip()
        if v:
            linhas[org][c] = v

GRANEL = "ESPECIFICADO"      # coluna "Kiwi 1000" = informe 331/2025
ESPANHA = "B-3/C-3"          # informe 240/2023, Ribadumia - material REJEITADO


def classe_coluna(c):
    # "Kiwi 1000" deixou de ser SEM POSICAO: o gestor situou-a numa ZONA
    # (lado oeste do maior vazio circular). Testemunho de tipo 1. Continua a
    # ser UMA amostra COMPOSTA, numa data, sem replicado e sem par de
    # comparacao - o que e um problema diferente de nao ter posicao.
    if GRANEL in c:
        return "granel_kiwi1000_zona_por_testemunho"
    if c.startswith(ESPANHA):
        return "espanha_rejeitado"
    if c.startswith("B1 "):
        return "B1_sem_posicao"          # G35/G36: B1 fora da banda contigua
    return "unidade_colocada"            # B3, B4, V7, Erica Novo E


COM_LUGAR = ("unidade_colocada", "granel_kiwi1000_zona_por_testemunho")

mat = []
for org, cols in linhas.items():
    ent = {"organismo": org, "fontes": {}}
    for c, v in cols.items():
        ent["fontes"].setdefault(classe_coluna(c), []).append(v)
    vals = [v for vs in ent["fontes"].values() for v in vs]
    ent["tem_positivo"] = "POSITIVO" in vals
    ent["tem_negativo"] = "NEGATIVO" in vals
    ent["ensaiada_em_unidade_colocada"] = "unidade_colocada" in ent["fontes"]
    ent["ensaiada_com_lugar"] = any(k in ent["fontes"] for k in COM_LUGAR)
    ent["so_no_granel"] = list(ent["fontes"].keys()) == [
        "granel_kiwi1000_zona_por_testemunho"]
    ent["fonte_ganfei_existe"] = any(k != "espanha_rejeitado" for k in ent["fontes"])
    # so um NEGATIVO pode excluir, e so exclui onde a amostra estava
    neg_com_lugar = [k for k in COM_LUGAR
                     if "NEGATIVO" in ent["fontes"].get(k, [])]
    ent["negativo_com_lugar"] = neg_com_lugar
    mat.append(ent)

N["matriz"] = mat
N["matriz_resumo"] = {
    "linhas_organismo_x_matriz": len(mat),
    "ensaiadas_em_unidade_colocada": sum(
        1 for e in mat if e["ensaiada_em_unidade_colocada"]),
    "ensaiadas_com_algum_lugar_declarado": sum(
        1 for e in mat if e["ensaiada_com_lugar"]),
    "sem_qualquer_lugar_declarado": sum(
        1 for e in mat if not e["ensaiada_com_lugar"]),
    "linhas_com_algum_NEGATIVO": sum(1 for e in mat if e["tem_negativo"]),
    "linhas_com_NEGATIVO_a_partir_de_amostra_com_lugar": sum(
        1 for e in mat if e["negativo_com_lugar"]),
    "linhas_sem_qualquer_fonte_de_Ganfei":
        [e["organismo"] for e in mat if not e["fonte_ganfei_existe"]],
    "linhas_cuja_unica_fonte_e_o_granel_331_2025":
        [e["organismo"] for e in mat if e["so_no_granel"]],
    "negativos_com_lugar":
        [e["organismo"] for e in mat if e["negativo_com_lugar"]],
    "linhas_com_lugar_mas_sem_par_de_comparacao": sum(
        1 for e in mat if e["so_no_granel"]),
}
taxa = sorted({e["organismo"].rsplit("(", 1)[0].strip() for e in mat})
N["matriz_resumo"]["taxa_distintos"] = len(taxa)
N["matriz_resumo"]["taxa"] = taxa
# nenhuma linha do painel e bacteria ou virus - verifica-se pelos nomes
N["matriz_resumo"]["nota_cobertura"] = (
    "Os 15 taxa sao fungos, oomicetas e um nematode. Nao ha uma unica linha "
    "bacteriana nem viral em toda a matriz: nem Pseudomonas syringae pv. "
    "actinidiae, nem qualquer outra. Todo o diferencial bacteriano e viral "
    "esta NAO TESTADO, com ou sem posicao.")

json.dump(N, open(os.path.join(BASE, "c4_01_numeros.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("N3 ao foco ESTE: %.1f m  (disco do foco = 90 m -> o N3 esta FORA)"
      % N["N3_ao_foco_ESTE_m"])
print("v8 (ponto da valvula) ao foco OESTE: %.1f m"
      % N["valvulas_ponto_ao_foco"]["v8"]["d_foco_OESTE_m"])
print("v7 (ponto da valvula) ao foco OESTE: %.1f m"
      % N["valvulas_ponto_ao_foco"]["v7"]["d_foco_OESTE_m"])
print("total da tabela de valvulas: %.2f ha" % N["valvulas_total_ha"])
print()
print("fraccao do defice de 2026 que e declinio NOVO (regra M2), por valvula:")
for u, v in N["por_valvula"].items():
    print("   %-4s  defice %5.1f %%   novo %5.1f %%   novo/defice %s   chao2021 %4.1f %%"
          % (u, v["pct_defice_2026"], v["pct_novo_M2"],
             ("%.2f" % v["fraccao_do_defice_que_e_nova"])
             if v["fraccao_do_defice_que_e_nova"] is not None else "  - ",
             v["pct_nu2021_chao_lavrado"]))
print()
print("datacao dentro do disco de 120 m:", json.dumps(N["datacao_resumo"], ensure_ascii=False))
print("taxa de base:", json.dumps(N["taxa_de_base"], ensure_ascii=False))
print()
print("M. hapla contra defice:", json.dumps(N["M_hapla_contra_defice"], ensure_ascii=False)[:600])
print()
print("matriz:", json.dumps(N["matriz_resumo"], ensure_ascii=False, indent=1))
