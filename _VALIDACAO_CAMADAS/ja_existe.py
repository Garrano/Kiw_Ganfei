# -*- coding: utf-8 -*-
"""ja_existe.py — procurar antes de criar. Um comando, e obrigatório.

    python ja_existe.py rede rega
    python ja_existe.py b1 cota
    python ja_existe.py escala desenho

PORQUE ISTO EXISTE
------------------
A 04-09-2026 re-derivei, num turno, três coisas que já estavam em disco: a
análise do B1, a leitura do esquema de rega, e o teste da rede de rega — este
último um estudo de **onze cenas com critério pré-registado, refutado duas
vezes**. Das três, quem me travou foi o gestor, não a máquina.

**A causa não foi a árvore estar desarrumada. Foi eu não ter procurado.**
Arrumar 1 282 ficheiros não corrige isso: uma árvore arrumada que não se
consulta falha exactamente como uma desarrumada.

O QUE A PRÁTICA DE TOPO FAZ COM ÁRVORES GRANDES
------------------------------------------------
Não as indexa. Nenhuma base de código séria foi lida por inteiro por ninguém, e
funcionam. O que fazem é **tornar a procura barata e torná-la hábito** — grep
primeiro, escrever depois. O índice completo é caro de manter e envelhece; a
procura não envelhece.

E há uma coisa que a procura crua não faz e esta faz: **diz-te o estado do que
encontrou**. Um resultado que está RETIRADO, ou que corresponde a uma hipótese
já fechada, tem de aparecer marcado — senão vais lê-lo como se estivesse vivo,
que é a forma F das cláusulas.

O QUE ESTA PROCURA DIZ DE CADA ACERTO
--------------------------------------
    · o caminho e a primeira linha do cabeçalho
    · a classe da triagem — CORRENTE, RETIRADO, SUBSTITUIDO, NAO_ALCANCADO
    · se o ficheiro pré-registou uma falsificação (é trabalho com critério)
    · se já está no registo de HIPÓTESES FECHADAS

Ordena pelo que mais interessa antes de começar: **primeiro as hipóteses
fechadas**, depois o que tem critério pré-registado, depois o resto.
"""
import io
import json
import os
import re
import sys
import unicodedata

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
ARVORES = ["_VALIDACAO_CAMADAS", "_VALIDADE_GESTAO", "ganfei_s2", "_MULTIVERSO",
           "_esquema_rega", "Rings"]
# Os ficheiros SOLTOS na raiz das transferencias entram tambem, mas sem descer:
# e onde estava o `Esquema de rega retificado.pdf`, a fonte que eu media mal.
# Pos "." nas arvores primeiro e isso varreu tudo tres vezes — 428 acertos
# repetidos para «parcelas». Uma busca ruidosa nao se le, e uma busca que nao se
# le e igual a nao ter busca.
RAIZ_SOLTOS = True
# 06-09-2026 — ALARGADO, e a razao e concreta.
#
# A lista era (".py", ".md", ".json", ".csv"). Nesse dia falhei tres vezes o que
# esta ferramenta existe para travar, e as TRES estavam em extensoes que ela nao
# varria:
#     parcelas_ent.wkt          a geometria de referencia de que eu precisava
#     Esquema de rega ....pdf   a fonte que eu andava a medir mal
#     _esquema_rega/*.png       recortes do scan, ja feitos a 04-09
#
# A ferramenta correu-me pelos dedos por causa de uma tupla. **A inteligencia
# anterior deste caso vive em dados, nao em codigo** — e era exactamente essa a
# metade que nao se procurava.
EXT = (".py", ".md", ".json", ".csv",
       ".wkt", ".geojson", ".gpkg", ".shp",         # vector
       ".pdf", ".xlsx", ".txt",                     # documento
       ".npy", ".npz", ".tif", ".tiff",             # raster e matriz
       ".png", ".jpg", ".jpeg", ".svg")             # imagem e prancha
IGNORA = ("__pycache__", "cache", ".git", "lidar", "ortos", "tiles", "Kiw_Ganfei")
CRITERIO = re.compile(r"(?i)falsifica|hip[oó]tese fixa|crit[eé]rio.{0,40}antes|"
                      r"pr[eé]-registad|escrito antes de correr")


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn").lower()


def ler(p, n=12000):
    for cod in ("utf-8", "cp1252", "latin-1"):
        try:
            return io.open(p, encoding=cod).read(n)
        except (UnicodeDecodeError, OSError):
            continue
    return ""


def cabecalho(t):
    i = t.find('"""')
    if 0 <= i < 400:
        j = t.find("\n", i + 3)
        if j > 0:
            return t[i + 3:j].strip() or t[j + 1:t.find("\n", j + 1)].strip()
    for l in t.splitlines():
        l = l.strip().lstrip("#").strip()
        if len(l) > 12 and not l.startswith(("-*-", "import", "from")):
            return l
    return ""


def main(termos):
    if not termos:
        print(__doc__.split("PORQUE")[0].strip())
        return 2
    alvos = [sem_acento(t) for t in termos]

    # REGISTA A BUSCA. É isto que a torna um portão e não um conselho: a
    # `certificar.py` falha se houver guião tocado num dia sem busca nenhuma.
    # A ferramenta já existia a 04-09 e não impediu a repetição de 06-09,
    # porque estava disponível e nada a obrigava a correr.
    import csv as _csv
    import time as _time
    _b = os.path.join(AQUI, "BUSCAS.csv")
    _novo = not os.path.exists(_b)
    with io.open(_b, "a", encoding="utf-8", newline="") as _f:
        _w = _csv.writer(_f)
        if _novo:
            _w.writerow(["quando", "termos"])
        _w.writerow([_time.strftime("%Y-%m-%d %H:%M"), " ".join(termos)])

    # os registos que dizem «isto já foi decidido» ou «este ficheiro está mau»
    for _tit, _fic, _campos in (
            ("DECISÕES JÁ FECHADAS", "DECISOES_FECHADAS.csv",
             ("decisao", "porque", "nao_reabrir_sem")),
            ("INEXACTIDÕES REGISTADAS", "INEXACTOS.csv",
             ("ficheiro", "o_que_esta_errado", "accao"))):
        _p = os.path.join(AQUI, _fic)
        if not os.path.exists(_p):
            continue
        _hits = [r for r in _csv.DictReader(io.open(_p, encoding="utf-8"))
                 if any(t in sem_acento(" ".join((r.get(c) or "")
                                                 for c in _campos))
                        for t in alvos)]
        if _hits:
            print()
            print("== %s (%d)" % (_tit, len(_hits)))
            for r in _hits:
                print("   %-8s %s" % (r.get("id", "?"),
                                      (r.get(_campos[0]) or "")[:88]))
                print("            -> %s" % (r.get(_campos[-1]) or "")[:140])

    CL = {}
    p = os.path.join(AQUI, "triagem_de_fontes.json")
    if os.path.exists(p):
        CL = json.load(io.open(p, encoding="utf-8"))["classe"]
    fech = ler(os.path.join(AQUI, "HIPOTESES_FECHADAS.md"), 200000)

    acertos = []
    vistos = set()
    percursos = [(os.path.join(D, a), True) for a in ARVORES]
    if RAIZ_SOLTOS:
        percursos.append((D, False))
    for raiz, desce in percursos:
        if not os.path.isdir(raiz):
            continue
        for dp, dn, fn in os.walk(raiz):
            if not desce:
                dn[:] = []
            dn[:] = [x for x in dn if not any(i in x.lower() for i in IGNORA)]
            for f in fn:
                if not f.lower().endswith(EXT):
                    continue
                cam = os.path.join(dp, f)
                rel = os.path.relpath(cam, D).replace("\\", "/")
                if rel in vistos:
                    continue
                vistos.add(rel)
                txt = ler(cam)
                alvo = sem_acento(rel + "\n" + txt)
                n = sum(alvo.count(t) for t in alvos)
                if not all(t in alvo for t in alvos):
                    continue
                acertos.append(dict(
                    rel=rel, n=n, cab=cabecalho(txt)[:74],
                    classe=CL.get(rel, "?"),
                    criterio=bool(CRITERIO.search(txt)),
                    fechada=os.path.basename(rel) in fech))

    if not acertos:
        print("nada encontrado para: %s" % " ".join(termos))
        print("-> podes criar. Declara a pergunta e a falsificação antes de correr.")
        return 0

    def peso(h):
        return (0 if h["fechada"] else 1,
                0 if h["criterio"] else 1,
                {"RETIRADO": 0, "SUBSTITUIDO": 0, "CORRENTE": 1}.get(h["classe"], 2),
                -h["n"])
    acertos.sort(key=peso)

    print("%d acertos para «%s»" % (len(acertos), " ".join(termos)))
    print()
    fechadas = [h for h in acertos if h["fechada"]]
    criterio = [h for h in acertos if h["criterio"] and not h["fechada"]]
    if fechadas:
        print("*** JÁ FECHADO — lê antes de repetir ***")
        for h in fechadas[:8]:
            print("   %-56s %s" % (h["rel"][:56], h["classe"]))
            if h["cab"]:
                print("      %s" % h["cab"])
        print()
    if criterio:
        print("COM CRITÉRIO PRÉ-REGISTADO — é trabalho com falsificação escrita")
        for h in criterio[:10]:
            print("   %-56s %s" % (h["rel"][:56], h["classe"]))
            if h["cab"]:
                print("      %s" % h["cab"])
        print()
    resto = [h for h in acertos if not h["fechada"] and not h["criterio"]]
    if resto:
        print("OUTROS (%d) — os 12 com mais ocorrências" % len(resto))
        for h in resto[:12]:
            marca = "  <- MORTO" if h["classe"] in ("RETIRADO", "SUBSTITUIDO") else ""
            print("   %-56s %-14s %2d%s" % (h["rel"][:56], h["classe"], h["n"], marca))
    print()
    if fechadas:
        print("=> Há hipótese FECHADA nesta matéria. Se vais repetir, escreve")
        print("   primeiro o que mudou desde então que o justifica.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
