# -*- coding: utf-8 -*-
"""indice_inteligencia.py — o que ja foi medido, e se esta certificado.

    python indice_inteligencia.py            > INDICE_INTELIGENCIA.md

PORQUE E GERADO, E NAO ESCRITO
-------------------------------
Um indice escrito a mao envelhece e ninguem o corrige. Este le a triagem, o
registo de factos, os certificados e os adversarios, e diz de CADA analise:
o que mede, em que estacao, e se passou pelas DUAS — certificacao e auditoria
independente. E a clausula C10 aplicada ao corpo inteiro em vez de a um ficheiro.

O QUE ISTO TORNOU VISIVEL, A 06-09-2026
----------------------------------------
Que o corpo de trabalho se divide por ESTACAO, e que as duas metades tem
estatutos muito diferentes:

  · **Primavera e Verao** — o NDVI de plena estacao, filtro `182 <= doy <= 244`.
    E aqui que vive a analise substantiva: os degraus, os multiversos, o halo,
    a fenologia. **E a metade que carrega o relatorio.**
  · **Inverno** — o SAR, janela Nov-Mar herdada sem interrogacao desde o
    `c1_09`. Mede estrutura e solo, nao copado: em Janeiro o kiwi nao tem folha.

A coluna `estacao` sai do proprio codigo: procuram-se meses, dias-do-ano e
palavras de janela no ficheiro. Nao e declarada por ninguem — e inferida, e por
isso vem marcada com `?` quando nao ha sinal claro.
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from estatuto import estatuto, citavel, _corpus, _triagem, _factos, D, _ler

ARVORES = ("_VALIDACAO_CAMADAS", "_VALIDADE_GESTAO", "ganfei_s2")
IGNORA = ("__pycache__", ".git", "_bak", "cache", "lidar", "ortos", "tiles",
          "Kiw_Ganfei", "node_modules", "_superseded")
# o aparelho de verificacao nao e inteligencia SOBRE O CASO: mede o processo,
# nao o pomar. Aparecia na lista de trabalho e teria mandado atacar-se a si.
APARELHO = ("estatuto.py", "indice_inteligencia.py", "certificar.py",
            "triagem_de_fontes.py", "proveniencia.py", "guarda.py",
            "registo_de_factos.py", "ja_existe.py", "sincronizar.py",
            "fuga.py", "gancho_arranque.py", "gancho_certificar.py")
# um ficheiro que se declara falhado no proprio nome nao e trabalho pendente
MORTO_NO_NOME = ("_TENTATIVA_FALHADA", "_bak", "_old", "_superseded", "_rascunho")
# emite inteligencia: escreve resultado e nao e prancha
ESCREVE = re.compile(r"json\.dump|to_csv|writerows|writerow|savetxt|guardar\s*\(")
FIGURA = re.compile(r"(?i)^(p\d+_|f\d+_|carta_|fig|plot_|.*_figura|.*figuras)")

VERAO = re.compile(r"(?i)182\s*<=|<=\s*244|plena.{0,3}esta|"
                   r"\b0?[5-9]-\d\d\b|-0[5-9]-|doy|dia.do.ano|ver[aã]o")
INVERNO = re.compile(r"(?i)inverno|-1[012]-|-0[123]-|11-01|03-31|10-01|04-30")
ANUAL = re.compile(r"(?i)ano.inteiro|01-01|12-31|todas as datas|sem filtro")


def estacao(t):
    a, v, i = bool(ANUAL.search(t)), bool(VERAO.search(t)), bool(INVERNO.search(t))
    if a and v and i:
        return "ano inteiro"
    if v and i:
        return "ambas"
    if v:
        return "Primavera/Verão"
    if i:
        return "Inverno"
    return "?"


def instrumento(t):
    m = []
    if re.search(r"(?i)sentinel-1|gamma0|rtc|_vv_|vv_db", t):
        m.append("SAR S1")
    if re.search(r"(?i)sentinel-2|ndvi|red.*nir|nir.*red|l2a", t):
        m.append("NDVI S2")
    if re.search(r"(?i)landsat", t):
        m.append("Landsat")
    if re.search(r"(?i)lidar|chm|mdt|mds", t):
        m.append("LiDAR")
    if re.search(r"(?i)ortofoto|orto_|dgt", t):
        m.append("ortofoto")
    if re.search(r"(?i)ifap|parcelario|parcelário", t):
        m.append("IFAP")
    return " · ".join(m) or "—"


def auditorias():
    """As passagens de adversario ja feitas, com veredicto.

    Sem isto, cada sessao volta a atacar o que ja foi atacado, ou pior: nao
    ataca porque «ha um relatorio algures». O registo diz o que, quando, e com
    que resultado — e o «o_que_sobreviveu» e a coluna que evita a volta.
    """
    import csv as _csv
    p = os.path.join(AQUI, "AUDITORIAS.csv")
    if not os.path.exists(p):
        return []
    with io.open(p, encoding="utf-8") as f:
        return [r for r in _csv.DictReader(f) if r.get("id")]


def main():
    cert, adv = _corpus()
    CL, FA = _triagem(), _factos()
    linhas = []
    for a in ARVORES:
        raiz = os.path.join(D, a)
        if not os.path.isdir(raiz):
            continue
        for dp, dn, fn in os.walk(raiz):
            dn[:] = [x for x in dn if not any(i in x.lower() for i in IGNORA)]
            for f in sorted(fn):
                if not f.endswith(".py") or FIGURA.match(f):
                    continue
                if f in APARELHO or any(x in f for x in MORTO_NO_NOME):
                    continue
                cam = os.path.join(dp, f)
                t = _ler(cam)
                if not ESCREVE.search(t):
                    continue
                rel = os.path.relpath(cam, D).replace("\\", "/")
                e = estatuto(rel, cert, adv, CL, FA)
                ok, razao = citavel(e)
                linhas.append(dict(rel=rel, f=f, cod=e["codigo"] or "",
                                   classe=e["classe"], ok=ok, razao=razao,
                                   est=estacao(t), ins=instrumento(t),
                                   nomeado=bool(e["adversarios"]),
                                   porcod=bool(e["adv_por_codigo"]),
                                   reg=e["no_registo"]))

    vivos = [l for l in linhas if l["classe"] not in ("RETIRADO", "SUBSTITUIDO")]
    cit = [l for l in vivos if l["ok"]]
    print("# ÍNDICE DA INTELIGÊNCIA — o que foi medido, e se está certificado")
    print()
    print("**Gerado por `indice_inteligencia.py`.** Não editar à mão: corre outra vez.")
    print()
    print("| | |")
    print("|---|---|")
    print("| guiões que emitem resultado | **%d** |" % len(linhas))
    print("| vivos (não retirados) | **%d** |" % len(vivos))
    print("| **citáveis — passaram pelas DUAS** | **%d** |" % len(cit))
    print("| no registo dos factos vivos | %d |"
          % sum(1 for l in vivos if l["reg"]))
    print("| nomeados por um adversário | %d |"
          % sum(1 for l in vivos if l["nomeado"]))
    print()

    A = auditorias()
    if A:
        print("## Auditorias já feitas — não repetir sem razão nova escrita")
        print()
        print("| id | data | alvo | veredicto | o que sobreviveu |")
        print("|---|---|---|---|---|")
        for r in A:
            print("| %s | %s | %s | **%s** | %s |"
                  % (r["id"], r["data"], r["alvo"], r["veredicto"],
                     r["o_que_sobreviveu"]))
        print()

    print("## Por estação — e é aqui que a assimetria aparece")
    print()
    print("| estação | guiões vivos | citáveis | fracção |")
    print("|---|---|---|---|")
    for s in ("Primavera/Verão", "Inverno", "ambas", "ano inteiro", "?"):
        g = [l for l in vivos if l["est"] == s]
        if not g:
            continue
        c = sum(1 for l in g if l["ok"])
        print("| **%s** | %d | %d | %.0f %% |"
              % (s, len(g), c, 100.0 * c / len(g)))
    print()

    print("## Por instrumento")
    print()
    print("| instrumento | vivos | citáveis |")
    print("|---|---|---|")
    ins = {}
    for l in vivos:
        ins.setdefault(l["ins"], []).append(l)
    for k in sorted(ins, key=lambda x: -len(ins[x]))[:10]:
        print("| %s | %d | %d |"
              % (k, len(ins[k]), sum(1 for l in ins[k] if l["ok"])))
    print()

    print("## Os citáveis — passaram pelo portão E por adversário")
    print()
    print("| guião | facto | estação | instrumento |")
    print("|---|---|---|---|")
    for l in sorted(cit, key=lambda x: x["cod"]):
        print("| `%s` | %s | %s | %s |"
              % (l["rel"], l["cod"] or "—", l["est"], l["ins"]))
    print()

    print("## Os NÃO citáveis que emitem resultado — por estação")
    print()
    for s in ("Primavera/Verão", "Inverno", "ambas", "ano inteiro", "?"):
        g = [l for l in vivos if l["est"] == s and not l["ok"]]
        if not g:
            continue
        print("### %s — %d guiões" % (s, len(g)))
        print()
        print("| guião | o que falta | instrumento |")
        print("|---|---|---|")
        for l in sorted(g, key=lambda x: x["f"])[:40]:
            print("| `%s` | %s | %s |" % (l["rel"], l["razao"], l["ins"]))
        if len(g) > 40:
            print("| … e mais %d | | |" % (len(g) - 40))
        print()


if __name__ == "__main__":
    main()
