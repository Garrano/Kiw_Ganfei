# -*- coding: utf-8 -*-
"""TRIAGEM DE FONTES — o que se consulta, o que já não, e onde está escrito porquê.

O PROBLEMA
----------
Mil duzentos e oitenta ficheiros em quatro árvores. Uma parte sustenta os 27
factos certificados; outra parte é a versão anterior dos mesmos, ou o cálculo
que uma retractação derrubou, ou uma exploração que não foi a lado nenhum.
**Todos parecem iguais na listagem da pasta.**

A PRIMEIRA VERSÃO DISTO ESTAVA ERRADA, E FICA ESCRITO
------------------------------------------------------
Corri-a às 12h20 de 04-09. Classificou **17 ficheiros como retirados, e 16
eram falsos positivos** — um regex sobre prosa que apanhava qualquer documento
que *mencionasse* uma retractação. Apanhou, entre outros, este próprio ficheiro,
porque o cabeçalho nomeia o `c1_02_costura.json` a três palavras de «morto».
E declarava 648 ficheiros «correntes» porque propagava alcançabilidade através
de prosa: **um `.md` que cita um ficheiro não o consome.**

É o erro de sempre num disfarce novo — um instrumento a concordar consigo
próprio, e uma ausência de discriminação tratada como resultado.

E o `c1_02_costura.json` **não está morto**: é lido pelo `c1_03_mdt.py`, e a
medição de costura que ele contém (+0,058 m) é o controlo em que a C9 assenta.
O que o Controlo 3 derrubou foi uma **frase dentro do certificado da C1** — que
os dois focos caem em campanhas de voo diferentes; é o mesmo voo, com 16 min de
intervalo. **Um ficheiro vivo pode conter uma linha morta.**

OS DOIS NÍVEIS, PORQUE UM SÓ NÃO CHEGA
---------------------------------------
**Nível ficheiro.** Um ficheiro é CORRENTE se houver um caminho de *consumo*
que o ligue ao registo de factos: o nome tem de aparecer junto de um `open`,
`load`, `read`, `glob`, `join` ou construção de caminho, e **fora do docstring
do módulo**, que é onde a prosa vive. Documentos não propagam.

**Excepção, e o Controlo 3 teve razão em exigi-la escrita.** A regra acima vale
para a *propagação*, **não para a semente**. Os ficheiros-semente — o registo, o
portão, o certificador — são lidos por inteiro, docstring incluído, porque ali
uma menção *é* uma citação de proveniência. O preço são **21 dos 145 correntes
que entraram por prosa da semente**, incluindo o `sar_invernos.py`, promovido
pelo comentário que diz que ele é exploratório. Está medido, não estimado — e
até 04-09 este cabeçalho afirmava o contrário.

**Nível afirmação.** Uma tabela declarada, à mão, das frases que foram
derrubadas e continuam escritas em ficheiros vivos. É a única coisa aqui que
não é automática, e é de propósito: quem derruba uma frase escreve-a aqui.

O QUE ESTA TRIAGEM RECUSA FAZER
--------------------------------
Adivinhar «substituído» por sufixos `_v2`, `_novo`, `_final`. Adivinhar
«retirado» por prosa. O que não for provável fica em **NÃO ALCANÇADO** — que
não é «lixo», é a categoria honesta: nada neste processo o liga a um facto
vivo. **Ausência de ligação não é prova de inutilidade** — é a mesma regra que
o portão aplica às confirmações.

COMO SE USA
-----------
Antes de abrir um ficheiro para uma análise nova, procura-o no
`TRIAGEM_DE_FONTES.md`. RETIRADO ou SUBSTITUÍDO: **não se consulta.** NÃO
ALCANÇADO: pergunta-se porquê antes de o usar como prova. E se estiver em
AFIRMAÇÕES DERRUBADAS, o ficheiro consulta-se, mas aquela linha não.
"""
import io
import json
import os
import re
import sys

D = r"C:/Users/Jackster2/Downloads"
ARVORES = ["_VALIDACAO_CAMADAS", "_VALIDADE_GESTAO", "ganfei_s2", "_MULTIVERSO"]
EXT = (".py", ".json", ".md", ".csv", ".npy", ".geojson", ".txt")
IGNORA = ("__pycache__", "cache", ".git", "lidar", "ortos", "tiles")
VC = os.path.join(D, "_VALIDACAO_CAMADAS")

TOKEN = re.compile(r"[A-Za-z0-9_\-.]+\.(?:py|json|csv|md|npy|geojson|txt|pdf)")
# consumo: o nome tem de aparecer proximo de uma destas construcoes
CONSOME = re.compile(
    r"(?:open|load|loads|read|read_csv|read_json|loadtxt|genfromtxt|glob|iglob"
    r"|join|Path|imread|imopen|exists|isfile|listdir|savefig|dump|to_csv)\s*\(",
    re.I)

# ── AFIRMAÇÕES DERRUBADAS — declaradas à mão. Ficheiro vivo, linha morta.
DERRUBADAS = [
    dict(ficheiro="_VALIDACAO_CAMADAS/CAMADA_1_CERTIFICADO.md",
         afirmacao="«Os dois focos caem em mosaicos de campanhas de voo "
                   "diferentes» (OESTE 2025-08-02, ESTE 2026-01-15)",
         porque="é o MESMO voo, com 16 min de intervalo — tempo GPS do LAS",
         quem="C9_CONTROLO3_ADVERSARIO.md, 04-09-2026",
         efeito="a S2 da C1 cai; a medição de costura (+0,058 m, linha "
                "seguinte) sobrevive e é o que a C9 usa"),
    dict(ficheiro="ganfei_s2/figuras/p10_braudel_mapa.py",
         afirmacao="«as duas manchas estão nos extremos opostos do terreno» / "
                   "«B1: SEM cota, SEM dreno, SEM declive» / «445 m a sul»",
         porque="o B1 está 0,58 m ABAIXO dos dois focos; duas folhas MDT "
                "cobrem-no desde 29-08; a folga real é −200 m",
         quem="C9_CONTROLO3_ADVERSARIO.md + b1_terreno.py, 04-09-2026",
         efeito="corrigido no ficheiro em 04-09; fica listado porque a versão "
                "errada circulou em PNG"),
    dict(ficheiro="_VALIDADE_GESTAO/valvulas_1a5_o_troco_que_falta.py",
         afirmacao="«o esquema anota 1,77 ha para o B1; o IFAP dá 12,63 ha "
                   "— factor 7,1×»",
         porque="a retirada 21 tirou-a: o «1,77 ha» não está na tinta do "
                "esquema; é uma leitura nossa, não uma anotação dele",
         quem="C8_CONTROLO3_ADVERSARIO.md · retirada 21 da LISTA_FINAL",
         efeito="continua escrita no script e é gravada para dentro do "
                "`valvulas_1a5.json` (campo `area_esquema_ha`), que a triagem "
                "dá como CORRENTE — apanhado pelo Controlo 3 em 04-09"),
    dict(ficheiro="_VALIDACAO_CAMADAS/P3_ORIENTAL_REPLANTADO.md",
         afirmacao="§2 e §3 — «o foco oriental foi REPLANTADO»",
         porque="assentava só na prominência de pérgola, o instrumento "
                "que a produziu; o nível absoluto de NDVI não tem cova",
         quem="P5_RETRACCAO_DO_REPLANTADO.md, 31-08-2026",
         efeito="§1, §4 e §5 mantêm-se. O documento NÃO leva "
                "cartucho total — marcar a mais apagava prova boa. Sem "
                "cartucho, a verificação 3 contava-o entre os vivos: "
                "apanhado pelo Controlo 3 em 04-09"),
]


def ler(p):
    for cod in ("utf-8", "cp1252", "latin-1"):
        try:
            return io.open(p, encoding=cod).read()
        except (UnicodeDecodeError, OSError):
            continue
    return ""


def sem_docstring(t):
    """Corta o docstring do módulo — é lá que a prosa nomeia ficheiros mortos."""
    i = t.find('"""')
    if i < 0 or i > 400:
        return t
    j = t.find('"""', i + 3)
    return t[j + 3:] if j > 0 else t


# ── 1 · inventário
INV, POR_BASE = {}, {}
for a in ARVORES:
    raiz = os.path.join(D, a)
    if not os.path.isdir(raiz):
        continue
    for dp, dn, fn in os.walk(raiz):
        dn[:] = [x for x in dn if not any(i in x.lower() for i in IGNORA)]
        for f in fn:
            if not f.lower().endswith(EXT):
                continue
            rel = os.path.relpath(os.path.join(dp, f), D).replace("\\", "/")
            INV[rel] = dict(base=f, arvore=a)
            POR_BASE.setdefault(f, []).append(rel)
print("inventário: %d ficheiros em %d árvores" % (len(INV), len(ARVORES)))

# ── 2 · consumo: só de .py, só fora do docstring, só junto de uma construção
CONSUMO = {}
for rel, d in INV.items():
    d["texto"] = ler(os.path.join(D, rel)) if not rel.endswith(".npy") else ""
    alvos = set()
    if rel.endswith(".py"):
        corpo = sem_docstring(d["texto"])
        for m in TOKEN.finditer(corpo):
            b = m.group(0)
            if b not in POR_BASE or b == d["base"]:
                continue
            if CONSOME.search(corpo[max(0, m.start() - 200):m.start()]):
                alvos.add(b)
    CONSUMO[rel] = alvos

# ── 2b · CÓPIAS ARRUMADAS, decididas ANTES do fecho.
#       Uma pasta chamada `_bak_...` é uma cópia arrumada — é o nome que quem a
#       criou lhe deu, não uma adivinha por sufixo. Tem de valer antes, porque
#       a regra do produtor promovia o `_bak_20260901/reg01_landsat.py` a
#       corrente: escreve o mesmo nome de ficheiro que o original.
CONV_SUB = ("_bak", "_superseded", "_old", "_antigo", "_v1_")
ARRUMADO = {rel: "está em `%s/` — cópia arrumada por convenção" % parte
            for rel in INV
            for parte in rel.split("/")[:-1]
            if parte.lower().startswith(CONV_SUB)}
print("cópias arrumadas por convenção de directório: %d" % len(ARRUMADO))

# ── 3 · semente. O registo é um MANIFESTO: ali `ficheiro=` e o dicionário `PV`
#       de caminhos SÃO citações, e contam sem precisarem de um `open()` ao lado.
#       As onze peças entram porque o `certificar.py` as verifica por regra de
#       directório (`^P\d+[a-z]?_`), não por nome — a mesma regra que já foi cega
#       à P10 uma vez, e por isso está aqui escrita e não implícita.
SEMENTE = {r for f in ("registo_de_factos.py", "guarda.py", "certificar.py",
                       "triagem_de_fontes.py")
           for r in POR_BASE.get(f, [])}
if not SEMENTE:
    sys.exit("não encontrei o registo — a triagem não tem semente")
for r in list(SEMENTE):
    if INV[r]["base"] in ("registo_de_factos.py", "certificar.py"):
        for m in TOKEN.finditer(INV[r]["texto"]):
            SEMENTE |= set(POR_BASE.get(m.group(0), []))
FIGP = re.compile(r"^P\d+[a-z]?_.*\.py$", re.I)
SEMENTE |= {r for r in INV if FIGP.match(INV[r]["base"])
            and "figuras" in r.lower()}
# LS-5 do Controlo 3: o `CAMADA_1_CERTIFICADO.md` saia NAO_ALCANCADO — o mesmo
# documento mandava consulta-lo (esta na tabela DERRUBADAS) e desaconselhava-o.
# O que a tabela nomeia, e quem a sustenta, e corrente por definicao.
SEMENTE |= {x["ficheiro"] for x in DERRUBADAS if x["ficheiro"] in INV}
for _x in DERRUBADAS:
    for _b in TOKEN.findall(_x.get("quem", "")):
        SEMENTE |= set(POR_BASE.get(_b, []))
SEMENTE -= set(ARRUMADO)
CORRENTE, CADEIA, fila = set(), {}, [(s, [s]) for s in sorted(SEMENTE)]
while fila:
    rel, cam = fila.pop(0)
    if rel in CORRENTE:
        continue
    CORRENTE.add(rel)
    CADEIA[rel] = cam
    for b in sorted(CONSUMO.get(rel, ())):
        for alvo in POR_BASE[b]:
            if alvo not in CORRENTE and alvo not in ARRUMADO:
                fila.append((alvo, cam + [alvo]))
print("alcançáveis POR CONSUMO a partir do registo: %d" % len(CORRENTE))

# ── 3b · O PRODUTOR DE UM DADO VIVO ESTÁ VIVO.
#       O `b1_terreno.json` era corrente e o `b1_terreno.py` que o escreve não
#       era — e sem o produtor o dado não é reproduzível, que é a verificação 4
#       do certificar. Um `.py` é produtor se escreve o nome do ficheiro junto
#       de um verbo de escrita.
ESCREVE = re.compile(r"(?:dump|dumps|savefig|savez|save|to_csv|to_json|write"
                     r"|writer|\"w\"|'w')", re.I)
antes = len(CORRENTE)
for _ in range(3):
    novos = set()
    for rel in list(CORRENTE):
        if not rel.endswith((".json", ".csv", ".npy", ".txt", ".geojson")):
            continue
        b = INV[rel]["base"]
        for cand, d in INV.items():
            if not cand.endswith(".py") or cand in CORRENTE or cand in ARRUMADO:
                continue
            corpo = sem_docstring(d["texto"])
            for m in re.finditer(re.escape(b), corpo):
                if ESCREVE.search(corpo[max(0, m.start() - 260):m.start() + 40]):
                    novos.add(cand)
                    CADEIA[cand] = CADEIA.get(rel, [rel]) + [cand]
                    break
    if not novos:
        break
    CORRENTE |= novos
print("  + produtores dos dados vivos: %d" % (len(CORRENTE) - antes))

# ── 4 · RETIRADO — só o cabeçalho explícito. Sem regex sobre prosa.
RETIRADO = {r: "traz o cabeçalho «⚠ RETIRADO»" for r, d in INV.items()
            if d["texto"].lstrip().startswith("> # ⚠ RETIRADO")}

# ── 5 · SUBSTITUÍDO — só quando um ficheiro CORRENTE o diz, com o verbo à mão
# Duas fontes, ambas declaradas: uma convenção de directório (uma pasta chamada
# `_bak_...` É uma cópia arrumada, e isso não é adivinhar por sufixo de ficheiro
# — é ler o nome que quem a criou lhe deu), e a frase escrita num ficheiro vivo.
RE_SUB = re.compile(r"(?:substitui|substituiu|em vez d[eo]|sucede a)\s+[«\"'`]?"
                    r"([A-Za-z0-9_\-.]+\.(?:py|json|csv|md|npy))", re.I)
SUBST = {r: v for r, v in ARRUMADO.items() if r not in RETIRADO}
for rel in sorted(CORRENTE):
    for m in RE_SUB.finditer(INV[rel]["texto"]):
        b = m.group(1)
        if b in POR_BASE and b != INV[rel]["base"]:
            for alvo in POR_BASE[b]:
                if alvo not in RETIRADO and alvo not in CORRENTE:
                    SUBST.setdefault(alvo, "%s diz que o substitui" % INV[rel]["base"])

# ── 6 · classificação. Retirado ganha a corrente: um ficheiro pode estar
#       retirado E continuar a ser lido, que é o caso que isto existe para ver.
CLASSE, CONFLITO = {}, []
for rel in sorted(INV):
    if rel in RETIRADO:
        CLASSE[rel] = "RETIRADO"
        if rel in CORRENTE:
            CONFLITO.append((rel, RETIRADO[rel]))
    elif rel in SUBST:
        CLASSE[rel] = "SUBSTITUIDO"
    elif rel in CORRENTE:
        CLASSE[rel] = "CORRENTE"
    else:
        CLASSE[rel] = "NAO_ALCANCADO"
C = {}
for v in CLASSE.values():
    C[v] = C.get(v, 0) + 1
print()
for k in ("CORRENTE", "RETIRADO", "SUBSTITUIDO", "NAO_ALCANCADO"):
    print("  %-14s %4d" % (k, C.get(k, 0)))

# ── 7 · as afirmações derrubadas têm de apontar para ficheiros que existem
maus = [x["ficheiro"] for x in DERRUBADAS if x["ficheiro"] not in INV]
print()
print("afirmações derrubadas declaradas: %d%s"
      % (len(DERRUBADAS), "" if not maus else "  ⚠ ficheiro inexistente: %s" % maus))
if CONFLITO:
    print()
    print("CONFLITOS — retirado e consultado ao mesmo tempo (%d):" % len(CONFLITO))
    for rel, porque in CONFLITO:
        print("  · %s — %s" % (rel, porque))

# ── 8 · saída
json.dump(dict(inventario=len(INV), classe=CLASSE, cadeia=CADEIA,
               retirado=RETIRADO, substituido=SUBST, derrubadas=DERRUBADAS,
               conflitos=[dict(ficheiro=a, porque=b) for a, b in CONFLITO]),
          io.open(os.path.join(VC, "triagem_de_fontes.json"), "w",
                  encoding="utf-8"), indent=1, ensure_ascii=False)

L = ["# TRIAGEM DE FONTES", "",
     "Gerado por `triagem_de_fontes.py`. **Não editar à mão.**",
     "",
     "«Corrente» = há um caminho de **consumo** (`open`/`load`/`join`) do registo",
     "de factos até ele. Menção em prosa não conta.",
     "", "| classe | n | o que fazer |", "|---|---|---|",
     "| CORRENTE | %d | consulta-se |" % C.get("CORRENTE", 0),
     "| RETIRADO | %d | **não se consulta** |" % C.get("RETIRADO", 0),
     "| SUBSTITUIDO | %d | **não se consulta** — usa o sucessor |" % C.get("SUBSTITUIDO", 0),
     "| NAO_ALCANCADO | %d | nada o liga a um facto vivo; perguntar antes de usar |" % C.get("NAO_ALCANCADO", 0),
     "",
     "## Afirmações derrubadas — ficheiro vivo, linha morta", "",
     "O nível que a triagem por ficheiro não alcança. Declarado à mão.", ""]
for x in DERRUBADAS:
    L += ["### `%s`" % x["ficheiro"], "",
          "> %s" % x["afirmacao"], "",
          "- **porquê:** %s" % x["porque"],
          "- **quem:** %s" % x["quem"],
          "- **efeito:** %s" % x["efeito"], ""]
if CONFLITO:
    L += ["## ⚠ Retirado e consultado ao mesmo tempo", ""]
    L += ["- `%s` — %s" % (a, b) for a, b in CONFLITO] + [""]
for cl, tit, src in (("RETIRADO", "Retirados", RETIRADO),
                     ("SUBSTITUIDO", "Substituídos", SUBST)):
    itens = [r for r in sorted(CLASSE) if CLASSE[r] == cl]
    if itens:
        L += ["## %s" % tit, ""] + ["- `%s` — %s" % (r, src[r]) for r in itens] + [""]
L += ["## Correntes — e por que caminho de consumo se chega a cada um", ""]
for r in sorted(CLASSE):
    if CLASSE[r] == "CORRENTE":
        cam = CADEIA.get(r, [r])
        L.append("- `%s`%s" % (r, "" if len(cam) < 2 else "  ← %s"
                               % " → ".join(os.path.basename(x) for x in cam[:-1])))
L += ["", "## Não alcançados", "",
      "Nada os liga por consumo a um facto vivo. **Não é um veredicto sobre eles.**", ""]
L += ["- `%s`" % r for r in sorted(CLASSE) if CLASSE[r] == "NAO_ALCANCADO"]
io.open(os.path.join(VC, "TRIAGEM_DE_FONTES.md"), "w",
        encoding="utf-8").write("\n".join(L) + "\n")
print()
print("escritos TRIAGEM_DE_FONTES.md e triagem_de_fontes.json")
