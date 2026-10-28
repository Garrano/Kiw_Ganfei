# -*- coding: utf-8 -*-
"""S1 executável · o que já existe sobre isto, antes de escrever a primeira linha.

PORQUE EXISTE
-------------
06-09-2026. Numa só sessão, três vezes: comecei a produzir sobre um assunto que
já tinha trabalho em disco, e **foi o utilizador a dizer-mo de cada vez** —
o `valvulas_v4.json` e o `v6.json`, a pasta `_esquema_rega/` com os recortes do
scan já feitos, e o `parcelas_ent.wkt`, que era a geometria de referência que eu
andava a precisar enquanto comparava contra a errada.

A S1 já dizia «procurar é um comando, e vem antes de criar». Era prosa, e prosa
cumpre-se quando dá jeito.

COMO SE USA
-----------
    python antes.py valvulas rega escala

Imprime, por ordem de utilidade:

  · **ficheiros de dados** que casam com os termos, mais recentes primeiro —
    é onde vive a inteligência anterior, e é o que eu não vejo;
  · **guiões** que casam, com a data;
  · **decisões já fechadas** que tocam nos termos — a `DECISOES_FECHADAS.csv`,
    porque reabrir uma custa uma sessão;
  · **inexactidões registadas** — a `INEXACTOS.csv`, porque usar um ficheiro
    marcado é pior do que não o usar;
  · **auditorias** anteriores sobre o assunto.

E **regista a busca** em `BUSCAS.csv`. A `certificar.py` falha se apareceu
código novo num dia em que não houve busca nenhuma. É isso que a torna um
comando e não um conselho.
"""
import csv
import io
import os
import re
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.environ.get("GANFEI_RAIZ", r"C:/Users/Jackster2/Downloads")
BUSCAS = os.path.join(AQUI, "BUSCAS.csv")

DADOS = (".json", ".csv", ".wkt", ".geojson", ".npz", ".npy", ".tif", ".pdf",
         ".xlsx", ".shp", ".gpkg", ".jpeg", ".jpg", ".png")
CODIGO = (".py",)
NOTAS = (".md",)
IGNORAR = re.compile(r"[\\/](\.git|__pycache__|node_modules|_superseded|"
                     r"Kiw_Ganfei|CLAUDE CLONE)[\\/]", re.I)

REGISTOS = [
    ("DECISÕES JÁ FECHADAS — reabrir uma custa uma sessão",
     "DECISOES_FECHADAS.csv", ("decisao", "porque", "nao_reabrir_sem")),
    ("INEXACTIDÕES REGISTADAS — usar um ficheiro marcado é pior que não o usar",
     "INEXACTOS.csv", ("ficheiro", "o_que_esta_errado", "accao")),
    ("AUDITORIAS ANTERIORES",
     "AUDITORIAS.csv", ("alvo", "ficheiros", "veredicto")),
]


def casa(nome, termos):
    n = nome.lower()
    return sum(1 for t in termos if t in n)


def varre(termos, exts, limite=18):
    achados = []
    for base, dirs, ficheiros in os.walk(RAIZ):
        if IGNORAR.search(base + os.sep):
            dirs[:] = []
            continue
        if base.count(os.sep) - RAIZ.count(os.sep) > 5:
            dirs[:] = []
            continue
        for f in ficheiros:
            if not f.lower().endswith(exts):
                continue
            p = os.path.join(base, f)
            pontos = casa(f, termos)
            if not pontos:
                pontos = casa(os.path.basename(base), termos)
                if pontos:
                    pontos *= 0.5
            if pontos:
                try:
                    achados.append((pontos, os.path.getmtime(p),
                                    os.path.getsize(p), p))
                except OSError:
                    pass
    achados.sort(key=lambda x: (-x[0], -x[1]))
    return achados[:limite]


def mostra(titulo, achados):
    print()
    print("== %s (%d)" % (titulo, len(achados)))
    if not achados:
        print("   nada")
        return
    for _, mt, tam, p in achados:
        print("   %s  %8.0f kB  %s"
              % (time.strftime("%Y-%m-%d", time.localtime(mt)), tam / 1024.0,
                 os.path.relpath(p, RAIZ)))


def registos(termos):
    for titulo, ficheiro, campos in REGISTOS:
        p = os.path.join(AQUI, ficheiro)
        if not os.path.exists(p):
            continue
        linhas = []
        for r in csv.DictReader(io.open(p, encoding="utf-8")):
            texto = " ".join((r.get(c) or "") for c in campos).lower()
            if any(t in texto for t in termos):
                linhas.append(r)
        print()
        print("== %s (%d)" % (titulo, len(linhas)))
        if not linhas:
            print("   nada")
        for r in linhas:
            chave = r.get("id", "?")
            corpo = (r.get(campos[0]) or "")[:96]
            print("   %-8s %s" % (chave, corpo))
            extra = (r.get(campos[-1]) or "")[:150]
            if extra:
                print("            -> %s" % extra)


def main():
    termos = [t.lower() for t in sys.argv[1:] if not t.startswith("-")]
    if not termos:
        print(__doc__.strip().splitlines()[0])
        print()
        print("uso:  python antes.py <termo> [termo ...]")
        print("      python antes.py valvulas rega escala")
        return 2

    print("=" * 74)
    print("ANTES DE CRIAR — o que já existe sobre: %s" % ", ".join(termos))
    print("=" * 74)

    mostra("DADOS — é aqui que vive a inteligência anterior", varre(termos, DADOS))
    mostra("GUIÕES", varre(termos, CODIGO))
    mostra("NOTAS E REGISTOS", varre(termos, NOTAS))
    registos(termos)

    novo = not os.path.exists(BUSCAS)
    with io.open(BUSCAS, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["quando", "termos"])
        w.writerow([time.strftime("%Y-%m-%d %H:%M"), " ".join(termos)])

    print()
    print("-" * 74)
    print("Busca registada. Duas perguntas antes de escrever código:")
    print("  1 · alguma coisa acima já responde, ou responde em parte?")
    print("  2 · o que é que este trabalho novo desbloqueia a jusante?")
    print("Se a 2 não tiver resposta, não se faz.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
