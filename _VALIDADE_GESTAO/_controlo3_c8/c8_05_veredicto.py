# -*- coding: utf-8 -*-
"""C8-05 · o adversario sobre o C8. Cinco verificacoes, todas corridas.

  V1 · reproduzir o F1 do `valvulas_1a5_o_troco_que_falta.py` e mostrar de onde
       vem a uniao «v6..v17». O ficheiro que ele le como «0 valvulas» tem as
       valvulas 1 a 5 com coordenada UTM.
  V2 · o «11/11 dentro do nulo»: contar as unidades e as cenas do teste.
  V3 · a janela do teste contra a caixa do B1 do IFAP.
  V4 · a tabela de areas do gestor: quanta area da exploracao entrou na
       particao por valvula, e quanta ficou fora.
  V5 · a incerteza de +-150 m aplicada a frase corrigida do C8.
"""
import json
import os

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
G2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
AQUI = os.path.dirname(os.path.abspath(__file__))
S = {}


def carrega(p):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.load(open(p, encoding=enc))
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise IOError(p)


L = "=" * 84
# ───────────────────────────────────────────────────────────────────── V1
print(L)
print("V1 - o F1 do C8: as valvulas 1-5 estao mesmo fora de TODAS?")
print(L)
FONTES = ("valvulas_por_area.json", "valvulas_v6.json", "valvulas_v4.json",
          "valvulas_por_linha.json")
# a) exactamente o leitor do C8, linha por linha
TODAS_C8 = set()
for f in FONTES:
    d = carrega(os.path.join(G2, f))
    ch = d.get("valvulas", d.get("metros_por_linha", d))
    vs = sorted((str(k).lstrip("v") for k in ch
                 if str(k).lstrip("v").isdigit()), key=int)
    TODAS_C8 |= {"v" + v for v in vs}
    print("  leitor do C8   %-26s -> %2d valvulas" % (f, len(vs)))
print("  uniao do leitor do C8: %s"
      % " ".join(sorted(TODAS_C8, key=lambda k: int(k[1:]))))

# b) o que os ficheiros contem de facto, lidos pela estrutura real de cada um
#    (o mesmo criterio que `c4_r2_01_multiverso_das_valvulas.py` ja usava)
print()
real = {}
for f in FONTES:
    d = carrega(os.path.join(G2, f))
    out = {}
    if f == "valvulas_por_area.json":
        out = {k: (v["E"], v["N"]) for k, v in d.items()
               if isinstance(v, dict) and "E" in v}
    elif f == "valvulas_v6.json":
        out = {k: tuple(v) for k, v in d.get("valvulas", {}).items()}
    elif f == "valvulas_v4.json":
        for chave in ("corpo", "lobo_oeste"):
            for k, v in d.get(chave, {}).items():
                out[k] = tuple(v)
    elif f == "valvulas_por_linha.json":
        import re
        for r in d.get("valvulas", []):
            for n_ in re.findall(r"\d+", r.get("valvulas", "")):
                out[n_] = (r["E"], r["N"])
    real[f] = out
    print("  estrutura real %-26s -> %2d valvulas: %s"
          % (f, len(out), " ".join(sorted(out, key=int))))
uni = set()
for v in real.values():
    uni |= set(v)
falta = [str(i) for i in range(1, 6) if str(i) not in uni]
print()
print("  uniao real: %s" % " ".join(sorted(uni, key=int)))
print("  valvulas 1-5 ausentes de TODAS as reconstrucoes: %s"
      % (", ".join(falta) if falta else "NENHUMA — estao em valvulas_v4.json"))
v4 = carrega(os.path.join(G2, "valvulas_v4.json"))
lo = v4["lobo_oeste"]
Es = [p[0] for p in lo.values()]
Ns = [p[1] for p in lo.values()]
print("  valvulas_v4.json['lobo_oeste'] = %s, caixa E %.0f..%.0f N %.0f..%.0f"
      % (" ".join(sorted(lo, key=int)), min(Es), max(Es), min(Ns), max(Ns)))
print("  incerteza declarada nesse ficheiro: corpo +-%d m, lobo +-%d m"
      % (v4["_incerteza_corpo_m"], v4["_incerteza_lobo_m"]))
print()
print("  CAUSA: o leitor do C8 faz  d.get('valvulas', d.get('metros_por_linha', d))")
print("  O `valvulas_v4.json` nao tem nenhuma das duas chaves, logo cai no `d`")
print("  de topo, cujas chaves sao '_metodo', 'corpo', 'lobo_oeste', ... —")
print("  nenhuma e um digito. O comentario do proprio ficheiro afirma que")
print("  «nenhuma delas enumera valvulas»; as duas enumeram.")
print()
print("  E o criterio pre-registado do C8 diz, textualmente: «Se as valvulas")
print("  1-5 estiverem em ALGUMA das quatro reconstrucoes, a hipotese continua")
print("  fechada e este ficheiro nao serve para nada.»")
S["V1"] = dict(uniao_leitor_c8=sorted(TODAS_C8), uniao_real=sorted(uni, key=int),
               v1a5_ausentes=falta,
               lobo_oeste_v4={k: list(v) for k, v in lo.items()},
               criterio_do_c8_accionado=("hipotese continua fechada"
                                         if not falta else "reaberta"))

# ───────────────────────────────────────────────────────────────────── V2
print()
print(L)
print("V2 - o «11/11 dentro do nulo»: 11 do que?")
print(L)
RR = carrega(os.path.join(VG, "rede_de_rega.json"))
cenas = sorted(RR["agrupamento"])
valv = sorted(RR["por_valvula"], key=int)
dentro = [d for d in cenas if RR["agrupamento"][d]["p"] > 0.05]
print("  cenas no teste de agrupamento: %d  (%s ... %s)"
      % (len(cenas), cenas[0], cenas[-1]))
print("  cenas com p > 0,05 (dentro do nulo): %d de %d" % (len(dentro), len(cenas)))
print("  UNIDADES da particao: %d valvulas — %s"
      % (len(valv), " ".join(valv)))
print("  n do teste de ordem na rede: %s"
      % sorted({v["n"] for v in RR["ordem"].values()}))
print()
print("  => o «11» sao CENAS, nao valvulas. O teste correu sobre 12 valvulas")
print("     em 11 cenas. O C8 escreve «correu sobre 11 a 12 valvulas»:")
print("     confunde a contagem de cenas com a contagem de unidades.")
print("  => e o C8 acerta no essencial: as 12 sao 6..17, todas do corpo.")
S["V2"] = dict(n_cenas=len(cenas), n_dentro_do_nulo=len(dentro),
               n_valvulas=len(valv), valvulas=valv)

# ───────────────────────────────────────────────────────────────────── V3
print()
print(L)
print("V3 - a janela do teste alcanca o B1?")
print(L)
AOI = (529950, 4654600, 531950, 4655600)     # rede_de_rega.py, via c2_00_comum
B1 = (529495, 4653832, 530063, 4654477)      # IFAP, C1a+C1b
G19 = (529350, 4653700, 530085, 4654478)     # C0, G19
print("  AOI do teste por valvula: E %d..%d  N %d..%d" % (AOI[0], AOI[2], AOI[1], AOI[3]))
print("  sector B1 (IFAP):         E %d..%d  N %d..%d" % (B1[0], B1[2], B1[1], B1[3]))
sobrepoe = not (B1[2] < AOI[0] or B1[0] > AOI[2]
                or B1[3] < AOI[1] or B1[1] > AOI[3])
print("  sobrepoem-se: %s" % sobrepoe)
print("  o B1 fica %d m a sul do bordo sul da AOI e %d m a oeste do bordo oeste"
      % (AOI[1] - B1[3], AOI[0] - B1[2]))
print("  => a particao por valvula nunca teve celula nenhuma no B1. O nucleo")
print("     do C8 — «o teste nao alcancava o troco» — CONFIRMA-SE, e por")
print("     geometria da AOI, que e independente do esquema de rega.")
S["V3"] = dict(aoi=AOI, b1=B1, sobrepoe=bool(sobrepoe),
               m_a_sul=AOI[1] - B1[3], m_a_oeste=AOI[0] - B1[2])

# ───────────────────────────────────────────────────────────────────── V4
print()
print(L)
print("V4 - a tabela de areas do gestor: que fraccao da exploracao foi testada?")
print(L)
# transcrita de ganfei_s2/figuras/m1_v8_implantacao.py (TAB e SOLTAS) e de
# ganfei_s2/b1_divisao.py (VALV). Fonte primaria: tabela do gestor, tipo 1.
BANDA = [("B2", 6, 25000), ("B2", 7, 25100), ("B2", 8, 28200), ("B2", 9, 18200),
         ("Erica Novo", 10, 24000), ("Erica Novo", 11, 24650),
         ("B3", 12, 27500), ("B3", 13, 25300), ("B3", 14, 25850),
         ("B3", 15, 11400), ("B4", 16, 17300), ("B4", 17, 20500)]
SOLTAS = [("B4C3", "18", 5500), ("B5", "19", 12500), ("B1C5", "20", 23000),
          ("B3C4", "21", 2300), ("Viveiro", "22", 10400),
          ("Viveiro", "23", 1500), ("B1C6", "24-25", 17000),
          ("B3C3", "27", 14000)]
B1V = [(1, 13500), (2, 9375), (3, 12750), (4, 24550), (5, 29900)]
a_banda = sum(a for _, _, a in BANDA)
a_soltas = sum(a for _, _, a in SOLTAS)
a_b1 = sum(a for _, a in B1V)
tot = a_banda + a_soltas + a_b1
print("  banda contigua, valvulas 6-17 .......... %2d valvulas  %8.2f ha"
      % (len(BANDA), a_banda / 1e4))
print("  B1, valvulas 1-5 ....................... %2d valvulas  %8.2f ha"
      % (len(B1V), a_b1 / 1e4))
print("  parcelas soltas, valvulas 18-25 e 27 ... %2d entradas  %8.2f ha"
      % (len(SOLTAS), a_soltas / 1e4))
print("  " + "-" * 62)
print("  total tabelado ......................... %2d entradas  %8.2f ha"
      % (len(BANDA) + len(B1V) + len(SOLTAS), tot / 1e4))
print()
print("  a particao do teste por valvula usou as %d da banda contigua:"
      % len(BANDA))
print("    %.2f ha de %.2f ha = %.1f %% da area tabelada da exploracao."
      % (a_banda / 1e4, tot / 1e4, 100.0 * a_banda / tot))
print("    ficaram fora %.2f ha (%.1f %%), em %d unidades de valvula."
      % ((a_b1 + a_soltas) / 1e4, 100.0 * (a_b1 + a_soltas) / tot,
         len(B1V) + len(SOLTAS)))
print()
print("  => o C8 diz «um troco que falta». Sao DOIS: o B1 (5 valvulas,")
print("     %.2f ha) e as parcelas soltas (18-25 e 27, %.2f ha)."
      % (a_b1 / 1e4, a_soltas / 1e4))
print("  => e a area do B1 pela tabela do gestor e %.2f ha, nao 1,77 ha."
      % (a_b1 / 1e4))
print("     a valvula 1, sozinha, tem %.2f ha." % (B1V[0][1] / 1e4))
S["V4"] = dict(ha_banda=a_banda / 1e4, ha_b1=a_b1 / 1e4,
               ha_soltas=a_soltas / 1e4, ha_total=tot / 1e4,
               pct_testado=100.0 * a_banda / tot,
               n_valvulas_fora=len(B1V) + len(SOLTAS))

# ───────────────────────────────────────────────────────────────────── V5
print()
print(L)
print("V5 - a frase corrigida do C8 dentro do envelope de +-150 m")
print(L)
GEO = carrega(os.path.join(VC, "SAIDA_C0", "c0_13_georref.json"))
print("  c0_13_georref.json: residuo mediano %.1f m, p90 %.1f m"
      % (GEO["residuo_mediano_m"], GEO["residuo_p90_m"]))
print("  valvulas.json v4: incerteza declarada do lobo +-%d m" % v4["_incerteza_lobo_m"])
folgas = dict(oeste=B1[0] - G19[0], este=G19[2] - B1[2],
              sul=B1[1] - G19[1], norte=G19[3] - B1[3])
print()
print("  folga do B1 dentro da caixa do G19, bordo a bordo:")
for k in ("oeste", "este", "sul", "norte"):
    print("    %-6s %5d m   %s" % (k, folgas[k],
                                   "MENOR que 150 m" if folgas[k] < 150 else "ok"))
n_frageis = sum(1 for v in folgas.values() if v < 150)
print()
print("  %d dos 4 bordos tem folga inferior a incerteza declarada." % n_frageis)
print("  Deslocar a caixa do G19 de 150 m em qualquer direccao — o que o")
print("  proprio erro declarado permite — destroi a continencia. A frase")
print("  «o B1 do IFAP cai inteiramente dentro da caixa do G19» tem")
print("  EXACTAMENTE o defeito da frase que substituiu: e verdadeira dos")
print("  numeros registados e nao sobrevive a incerteza deles.")
print()
print("  O que sobrevive sem a georreferenciacao: as DUAS coordenadas duras do")
print("  gestor (E529500 N4654010 -> E530054 N4654413, testemunho de tipo 1),")
print("  que localizam o B1 sem passar pelo esquema. E foi assim que o G36 o")
print("  localizou a 28-08.")
S["V5"] = dict(residuo_mediano_m=GEO["residuo_mediano_m"],
               residuo_p90_m=GEO["residuo_p90_m"],
               incerteza_lobo_m=v4["_incerteza_lobo_m"],
               folgas_m=folgas, bordos_com_folga_menor_que_incerteza=n_frageis)

json.dump(S, open(os.path.join(AQUI, "c8_05_veredicto.json"), "w"), indent=1)
print()
print("escrito c8_05_veredicto.json")
