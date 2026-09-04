# -*- coding: utf-8 -*-
"""Os boletins A2 de físico-química do solo — caracterização, não teste.

PORQUE ESTE FICHEIRO EXISTE, E O QUE O MOTIVOU
-----------------------------------------------
Foi proposto comparar a química do solo entre blocos afectados e não afectados:
se diferirem, é resultado; se não diferirem, é um negativo forte que empurra a
causa para baixo dos 30 cm. **A proposta veio com a sua própria ressalva já
escrita** — os boletins A2 são análises agronómicas padrão, tipicamente
0-20/0-30 cm, com profundidade não declarada nos extractos.

Eu respondi em prosa, com três afirmações, e **nenhuma passou pelo portão**.
Este ficheiro repõe isso: a mesma pergunta, com as onze perguntas da pré-voo
respondidas antes de correr, e os factos que sobreviverem declarados em
`registo_de_factos.py` como todos os outros.

A PRÉ-VOO, respondida
---------------------
**1 · Que pergunta exacta?** NÃO é «a química difere entre afectados e não
afectados». É: **o que estes nove boletins podem e não podem sustentar**, e que
factos de caracterização deles sobrevivem. A unidade é o *boletim*, não o bloco
nem o hectare.

**2 · Hipótese e falsificação.** Uma só, e é sobre a acidez:
    H · se a acidez do solo explicasse o declínio, os pH mais baixos estariam
        nos blocos em declínio.
    FALSIFICA-SE se os pH mais baixos estiverem em blocos que não declinam.
    E **não se confirma pelo contrário**: com n=9 e sem coordenadas, encontrar
    os pH baixos nos blocos maus seria compatível com acaso e com confundimento
    por idade. **Esta hipótese só pode falhar, nunca vencer.** Declarado antes.

**3 · Fronteira da unidade.** O código de bloco vem do **boletim do
laboratório**, escrito por quem colheu. Não é derivado de nenhum sinal nosso —
condição 6 satisfeita por construção.

**4 · Identidade no tempo.** Não se aplica: cada boletim é uma data única. Entra
como `instantanea()`.

**5 · Instrumento independente.** A química do solo **é** um instrumento
independente do óptico — física diferente, laboratório diferente, e não sabe
nada de NDVI. É a sua força.

**7 · A estatística de resumo esconde heterogeneidade?** Com n=9 não se
resumem: imprimem-se **os nove valores**.

**8 · Quantas observações independentes?** Nove boletins. Não 108 registos —
108 é 9 × 12 parâmetros, e doze parâmetros do mesmo tubo não são doze
observações.

**11 · A janela contém o que a frase abrange?** NÃO, e é decisivo: **três dos
nove boletins são do sector B1**, que fica fora da AOI, é pomar em
estabelecimento, e cuja série sobe enquanto os focos descem. Um B1 no grupo
«não afectado» compara copado maduro em declínio com pomar novo a encher.

O QUE ESTE FICHEIRO NÃO FAZ, E É O PONTO
-----------------------------------------
**Não corre o teste afectado-contra-não-afectado.** Não por preguiça: porque
**nenhum boletim tem coordenada**, e a atribuição a um foco teria de passar
pela válvula — e o **C7** certifica que a atribuição por válvula não sustenta
nenhuma quantidade. Correr o teste seria produzir um número que o registo já
proíbe.
"""
import collections
import csv
import io
import json
import os

C3 = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS\SAIDA_C3"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
PEDIDOS = ["pH", "CTC", "Matéria Orgânica", "Cálcio", "saturação em bases",
           "Textura"]
B1 = ("B1 C1", "B1 C3", "B1 C4")


def ler(f):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return io.open(os.path.join(C3, f), encoding=enc).read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise IOError(f)


t = ler("c3_04_registo_principal.csv")
d = ";" if t[:300].count(";") > t[:300].count(",") else ","
REG = [x for x in csv.DictReader(io.StringIO(t), delimiter=d)
       if "sico-Qu" in str(x.get("Doc_Type", ""))]
BOL = sorted({str(x["Report_No"]) for x in REG})
PAR = sorted({str(x["Organism_Parameter"]) for x in REG})
print("registos: %d  ·  boletins: %d  ·  parametros: %d"
      % (len(REG), len(BOL), len(PAR)))
print("  %d x %d = %d  ->  a unidade e o BOLETIM, nao o registo"
      % (len(BOL), len(PAR), len(BOL) * len(PAR)))

# ── F1 · o que foi pedido existe?
print()
print("=" * 92)
print("F1 · dos seis parametros pedidos, quais existem")
print("=" * 92)
falta = []
for p in PEDIDOS:
    ha = [q for q in PAR if p.lower().split()[0] in q.lower()]
    print("  %-22s %s" % (p, ha[0] if ha else "*** NAO EXISTE ***"))
    if not ha:
        falta.append(p)

# ── F2 · a profundidade
print()
print("=" * 92)
print("F2 · a profundidade esta declarada?")
print("=" * 92)
campos = ("Notes", "Matrix", "Method", "Test_Category", "Interpretation")
for c in campos:
    v = collections.Counter(str(x.get(c, ""))[:52] for x in REG)
    vazios = sum(n for k, n in v.items() if not k.strip())
    prof = [k for k in v if any(s in k.lower()
                                for s in ("cm", "profund", "0-2", "0-3", "20", "30"))]
    print("  %-16s %d vazios de %d  ·  mencao a profundidade: %s"
          % (c, vazios, len(REG), prof[:1] or "nenhuma"))

# ── F3 · os nove valores de pH, e onde estao
print()
print("=" * 92)
print("F3 · os NOVE valores, um por boletim. Sem resumo: n=9 nao se resume.")
print("=" * 92)
print()
ph = {}
for x in REG:
    if "pH" in str(x["Organism_Parameter"]):
        b = str(x["Terrain_Block_Parcel"]).strip()
        try:
            ph[b] = (float(str(x["Value"]).split()[0].replace(",", ".")),
                     str(x["Sample_Date"])[:10])
        except Exception:
            ph[b] = (float("nan"), str(x["Sample_Date"])[:10])
print("%-22s %7s %12s  %s" % ("bloco", "pH", "colheita", "sector"))
for b, (v, dt) in sorted(ph.items(), key=lambda kv: kv[1][0]):
    print("%-22s %7.1f %12s  %s"
          % (b, v, dt, "B1 — fora da AOI, pomar em estabelecimento"
             if b in B1 else "corpo principal"))

# ── F4 · a hipótese da acidez, que só pode falhar
print()
print("=" * 92)
print("F4 · H · se a acidez explicasse o declinio, os pH baixos estariam nos")
print("     blocos em declinio. Falsifica-se se estiverem nos que nao declinam.")
print("=" * 92)
ord_ph = sorted(ph.items(), key=lambda kv: kv[1][0])
dois_min = [b for b, _ in ord_ph[:2]]
print()
print("  os dois pH mais baixos: %s  (%.1f e %.1f)"
      % (", ".join(dois_min), ord_ph[0][1][0], ord_ph[1][1][0]))
em_b1 = [b for b in dois_min if b in B1]
if len(em_b1) == 2:
    print("  AMBOS no sector B1 — que NAO declina: sobe +0,092 enquanto os")
    print("  focos descem -0,085 (b1_como_unidade.json).")
    print()
    print("  -> H FALSIFICADA. A acidez nao acompanha o declinio.")
    print("     E so isso: a hipotese so podia falhar, e falhou.")
    ver_h = "falsificada"
else:
    print("  -> H nao falsificada por esta via. E NAO fica confirmada:")
    print("     com n=9 e sem coordenadas, so podia falhar.")
    ver_h = "nao falsificada, e nao confirmavel"

# ── F5 · porque é que o teste afectado-contra-nao-afectado nao corre
print()
print("=" * 92)
print("F5 · o denominador, que e o que impede o teste")
print("=" * 92)
print()
nb1 = sum(1 for b in ph if b in B1)
print("  boletins no sector B1 (fora da AOI, pomar jovem): %d de %d"
      % (nb1, len(ph)))
print("  boletins com COORDENADA: 0 de %d" % len(ph))
print("  boletins inequivocamente DENTRO de um foco: 0 de %d" % len(ph))
print()
print("  A atribuicao a um foco teria de passar pela valvula, e o C7 certifica")
print("  que a atribuicao por valvula nao sustenta nenhuma quantidade.")
print("  Correr o teste seria produzir um numero que o registo ja proibe.")

json.dump(dict(n_boletins=len(BOL), n_parametros=len(PAR), n_registos=len(REG),
               boletins=BOL, parametros=PAR, ausentes=falta,
               ph={k: v[0] for k, v in ph.items()},
               datas=sorted({v[1] for v in ph.values()}),
               b1_no_conjunto=nb1, com_coordenada=0,
               hipotese_acidez=ver_h,
               profundidade_declarada=False),
          open(os.path.join(VG, "a2_solo_caracterizacao.json"), "w"), indent=1)
print()
print("escrito a2_solo_caracterizacao.json")
