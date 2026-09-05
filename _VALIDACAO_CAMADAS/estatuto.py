# -*- coding: utf-8 -*-
"""estatuto.py — C10: isto passou pela certificacao E pelo adversario?

    python estatuto.py p1_pergola_oriental_2025.py
    python estatuto.py --tudo          # o roquete: quanto ha fora do aparelho

PORQUE ISTO EXISTE
------------------
A 05-09-2026 media-se o corpo de trabalho escrito DEPOIS do encerramento de
31-08: **88 guioes dentro do aparelho, 29 fora de qualquer verificacao**. Entre
os 29 estavam os dois que atacam as maiores condicoes abertas do caso:

  · `p1_pergola_oriental_2025.py` — declinio contra arranque no foco oriental;
  · `p2_onze_cenas.py` — «um acontecimento ou dois?», que a LISTA_FINAL diz
    textualmente que o relatorio NAO PODE afirmar.

Ambos correram a 01-09, escreveram JSON, e nenhum importa o `guarda.py` nem
aparece em certificado ou adversario nenhum. **O aparelho parou a 31-08 e o
trabalho continuou.** Um resultado assim nao e falso — e de estatuto
desconhecido, que para efeitos de citacao e a mesma coisa.

A OBRIGACAO
-----------
**So entra no relatorio o que passou pelas DUAS: certificacao e auditoria
independente.** Nao uma ou outra. A certificacao diz que o procedimento se
aguenta; o adversario diz que alguem que nao o escreveu tentou parti-lo. O
Controlo 3 pagou-se na primeira leitura com duas coisas que a
auto-adversarialidade **nao podia** ver — o tecto da auto-critica e real e
mede-se.

E e auto-perpetuante: corre a seguir a **cada resultado gerado**, pelo roquete
em `certificar.py`. Nao se pergunta se e preciso; pergunta-se sempre.

O QUE CONTA COMO CADA UMA
-------------------------
| | conta se |
|---|---|
| **certificado** | esta no registo dos factos vivos, ou e citado pelo nome num `*_CERTIFICADO*.md` / adenda que esteja CORRENTE |
| **auditado** | e citado pelo nome num `*_ADVERSARIO*.md` ou `*CONTROLO3*.md` |
| **portao** | importa o `guarda.py` — nao substitui as outras duas, mas conta |

Um ficheiro RETIRADO ou SUBSTITUIDO **nunca** e citavel, tenha o que tiver.

O QUE ISTO NAO FAZ
------------------
Nao diz que o resultado esta certo. Diz que passou pelos instrumentos que este
processo tem. Um numero pode ter as duas marcas e estar errado — foi o que
aconteceu ao A3, certificado e replicado antes de a ortofoto o derrubar. O
estatuto e condicao necessaria, nunca suficiente.
"""
import io
import json
import os
import re
import sys

D = r"C:/Users/Jackster2/Downloads"
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "estatuto_base.json")
ARVORES = ("_VALIDADE_GESTAO", "_VALIDACAO_CAMADAS", "ganfei_s2")
IGNORA = ("__pycache__", ".git", "_bak", "cache", "lidar", "ortos", "tiles",
          "Kiw_Ganfei", "node_modules")

# escreve resultado -> emite inteligencia -> tem de ter estatuto
ESCREVE = re.compile(r"json\.dump|to_csv|savetxt|\.to_json|guardar\s*\(")
# pranchas e ferramenta nao emitem veredicto
FIGURA = re.compile(r"(?i)^(p\d+_|f\d+_|carta_|fig|plot_|.*_figura)")


def _ler(p, n=200000):
    for cod in ("utf-8", "cp1252", "latin-1"):
        try:
            return io.open(p, encoding=cod).read(n)
        except (UnicodeDecodeError, OSError):
            continue
    return ""


def _corpus():
    """Junta o texto dos certificados e dos adversarios, separados."""
    cert, adv = [], []
    raiz = os.path.join(D, "_VALIDACAO_CAMADAS")
    for f in sorted(os.listdir(raiz)):
        if not f.endswith(".md"):
            continue
        u = f.upper()
        t = _ler(os.path.join(raiz, f))
        if "ADVERSARIO" in u or "CONTROLO3" in u:
            # Um adversario que ataca uma CLAUSULA nao auditou o CASO. O
            # C3_ADVERSARIO de 05-09 rotula os seus proprios achados A1, A2,
            # A3 — e contaminava a contagem dos factos com esses nomes.
            if f.startswith("C3_ADVERSARIO"):
                continue
            adv.append((f, t))
        elif "CERTIFICADO" in u or "ADENDA" in u or "LISTA_FINAL" in u \
                or "ENCERRAMENTO" in u:
            cert.append((f, t))
    return cert, adv


def _triagem():
    p = os.path.join(AQUI, "triagem_de_fontes.json")
    if not os.path.exists(p):
        return {}
    return json.load(io.open(p, encoding="utf-8"))["classe"]


def _factos():
    p = os.path.join(AQUI, "registo_manifesto.json")
    if not os.path.exists(p):
        return set()
    m = json.load(io.open(p, encoding="utf-8"))
    return {os.path.basename(f["ficheiro"]): f["codigo"]
            for f in m.get("factos", [])}


def estatuto(rel, cert=None, adv=None, CL=None, FA=None):
    """Devolve o dicionario de estatuto de UM ficheiro (caminho relativo a D)."""
    if cert is None:
        cert, adv = _corpus()
    if CL is None:
        CL = _triagem()
    if FA is None:
        FA = _factos()

    b = os.path.basename(rel)
    t = _ler(os.path.join(D, rel))
    classe = CL.get(rel.replace("\\", "/"), "?")
    cod = FA.get(b)

    # Duas forcas de prova, e mostram-se separadas: ser NOMEADO num adversario
    # e mais forte do que o CODIGO do facto la aparecer. Cinco dos factos vivos
    # nascem de um certificado e nao tem .py produtor para nomear — para esses
    # o codigo e a unica via possivel, e por isso conta.
    por_nome = [f for f, x in adv if b in x]
    por_cod = []
    if cod:
        pad = re.compile(r"(\*\*%s\*\*|%s\s*[·—–:]|\|\s*%s)"
                         % (cod, cod, cod))
        por_cod = [f for f, x in adv if pad.search(x) and f not in por_nome]

    return {
        "ficheiro": rel,
        "codigo": cod,
        "classe": classe,
        "morto": classe in ("RETIRADO", "SUBSTITUIDO"),
        "portao": ("import guarda" in t) or ("from guarda" in t),
        "no_registo": bool(cod),
        "certificados": [f for f, x in cert if b in x],
        "adversarios": por_nome,
        "adv_por_codigo": por_cod,
    }


def citavel(e, tipo=None, quem=None, quando=None):
    """As DUAS, e vivo. Devolve (bool, razao).

    **Testemunho tem outra barra, e tem de ter.** Um facto de tipo 1 nao se
    certifica com o `guarda.py` nem se ataca com um adversario: certifica-se
    dizendo QUEM disse e QUANDO, e corrige-se perguntando outra vez a quem sabe.
    Exigir-lhe certificado e adversario bloqueava a decisao clinica da PSA — e
    uma regra que trava testemunho valido e uma regra que se acaba por desligar,
    que foi como o `c2 = True` entrou.
    """
    if e["morto"]:
        return False, "esta %s — nunca citavel" % e["classe"]
    if tipo == "testemunho":
        if quem and quando:
            return True, "testemunho de %s em %s — tipo 1, ganha ao calculo"                 % (quem, quando)
        falta = [n for n, v in (("quem", quem), ("quando", quando)) if not v]
        return False, "testemunho sem %s" % " nem ".join(falta)
    tem_cert = e["no_registo"] or bool(e["certificados"])
    tem_adv = bool(e["adversarios"]) or bool(e.get("adv_por_codigo"))
    if tem_cert and tem_adv:
        return True, "certificado e atacado por adversario independente"
    falta = []
    if not tem_cert:
        falta.append("certificacao")
    if not tem_adv:
        falta.append("auditoria independente")
    return False, "falta " + " e ".join(falta)


def _emite_veredicto(cam, b):
    t = _ler(cam)
    if not ESCREVE.search(t):
        return False
    return not FIGURA.match(b)


def varrer():
    """Todos os guioes que emitem resultado e NAO sao citaveis."""
    cert, adv = _corpus()
    CL, FA = _triagem(), _factos()
    fora = []
    for a in ARVORES:
        raiz = os.path.join(D, a)
        if not os.path.isdir(raiz):
            continue
        for dp, dn, fn in os.walk(raiz):
            dn[:] = [x for x in dn
                     if not any(i in x.lower() for i in IGNORA)]
            for f in fn:
                if not f.endswith(".py"):
                    continue
                cam = os.path.join(dp, f)
                if not _emite_veredicto(cam, f):
                    continue
                rel = os.path.relpath(cam, D).replace("\\", "/")
                e = estatuto(rel, cert, adv, CL, FA)
                if e["morto"]:
                    continue          # morto e inerte, nao e divida
                ok, _ = citavel(e)
                if not ok:
                    fora.append(rel)
    P = pendentes()
    # o aparelho de verificacao nao e inteligencia sobre o caso
    APARELHO = ("estatuto.py", "indice_inteligencia.py", "certificar.py",
                "triagem_de_fontes.py", "proveniencia.py", "guarda.py",
                "registo_de_factos.py", "ja_existe.py", "sincronizar.py")
    return sorted(r for r in fora
                  if os.path.basename(r) not in P
                  and os.path.basename(r) not in APARELHO)


def _um(alvo):
    rel = alvo.replace("\\", "/")
    if not os.path.exists(os.path.join(D, rel)):
        achou = []
        for a in ARVORES:
            for dp, dn, fn in os.walk(os.path.join(D, a)):
                dn[:] = [x for x in dn
                         if not any(i in x.lower() for i in IGNORA)]
                if os.path.basename(alvo) in fn:
                    achou.append(os.path.relpath(
                        os.path.join(dp, os.path.basename(alvo)),
                        D).replace("\\", "/"))
        if not achou:
            print("nao encontrei: %s" % alvo)
            return 2
        rel = achou[0]
        if len(achou) > 1:
            print("(varios; uso o primeiro) %s" % ", ".join(achou))

    e = estatuto(rel)
    ok, razao = citavel(e)
    print()
    print(rel)
    print("  triagem              %s" % e["classe"])
    print("  portao (guarda.py)   %s" % ("importa" if e["portao"] else "nao importa"))
    print("  no registo de factos %s" % ("sim" if e["no_registo"] else "nao"))
    print("  certificado          %s" % (", ".join(e["certificados"][:3])
                                         if e["certificados"] else "nenhum"))
    if e["adversarios"]:
        print("  adversario           %s (nomeado)"
              % ", ".join(e["adversarios"][:3]))
    elif e.get("adv_por_codigo"):
        print("  adversario           %s (so pelo codigo %s — prova mais fraca)"
              % (", ".join(e["adv_por_codigo"][:2]), e["codigo"]))
    else:
        print("  adversario           nenhum")
    print()
    print("  => %s — %s" % ("CITAVEL" if ok else "NAO CITAVEL", razao))
    if not ok:
        print("     Nao entra no relatorio. Se for preciso, leva-se ao portao")
        print("     e a um adversario independente primeiro.")
    print()
    return 0 if ok else 1


AFIRM = os.path.join(AQUI, "afirmacoes.csv")
PEND = os.path.join(AQUI, "pendentes.csv")


def pendentes():
    """Guioes declarados EM CURSO — nome, data e razao escritas.

    O roquete tem de poder subir sem ser silenciado, senao a clausula acaba
    desligada — que e o padrao que este processo ja apanhou seis vezes. Mas
    tambem nao pode subir em silencio. A saida e declarar: um guiao novo sem
    estatuto entra aqui com data e razao, e sai quando for certificado e
    atacado. Declarar e um acto com nome; baixar a linha de base nao e.
    """
    import csv as _csv
    if not os.path.exists(PEND):
        return {}
    d = {}
    with io.open(PEND, encoding="utf-8") as f:
        for r in _csv.DictReader(f):
            if r.get("ficheiro"):
                d[r["ficheiro"].strip()] = r
    return d


def afirmacoes():
    """O ponto de aplicacao real: cada afirmacao do relatorio contra a sua fonte.

    O roquete de `--tudo` conta guioes, e inclui passos intermedios do pipeline
    que escrevem JSON sem emitirem veredicto nenhum: como numero de trabalho nao
    diz nada. **A obrigacao nao e sobre ficheiros, e sobre frases.** Aqui cada
    linha do relatorio nomeia a sua fonte, e a fonte tem de estar CITAVEL.

    Devolve (linhas_ok, problemas).
    """
    import csv
    if not os.path.exists(AFIRM):
        return 0, ["nao existe afirmacoes.csv — nenhuma afirmacao rastreada"]
    cert, adv = _corpus()
    CL, FA = _triagem(), _factos()
    ok, mal, pend = 0, [], []
    with io.open(AFIRM, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not r.get("id"):
                continue
            # PRETENDIDA: o relatorio QUER dizer isto e ainda nao pode. Nao e
            # falha — e a fila. A LISTA_FINAL ja tinha esta lista em prosa
            # («o que nao se pode escrever»); aqui ela liga-se a fonte que a
            # desbloquearia, e passa a afirmada sozinha quando essa fonte for
            # certificada e atacada.
            if (r.get("estado") or "afirmada").strip() == "pretendida":
                pend.append("%s <- %s" % (r["id"], (r.get("fonte") or "?")))
                continue
            fonte = (r.get("fonte") or "").strip()
            if not fonte:
                mal.append("%s sem fonte" % r["id"])
                continue
            rel = None
            for a in ARVORES:
                for dp, dn, fn in os.walk(os.path.join(D, a)):
                    dn[:] = [x for x in dn
                             if not any(i in x.lower() for i in IGNORA)]
                    if fonte in fn:
                        rel = os.path.relpath(os.path.join(dp, fonte),
                                              D).replace("\\", "/")
                        break
                if rel:
                    break
            if not rel:
                mal.append("%s: fonte «%s» nao existe em disco" % (r["id"], fonte))
                continue
            e = estatuto(rel, cert, adv, CL, FA)
            bom, razao = citavel(e, (r.get("tipo") or "").strip(),
                                 (r.get("quem") or "").strip(),
                                 (r.get("quando") or "").strip())
            if bom:
                ok += 1
            else:
                mal.append("%s (%s): %s" % (r["id"], fonte, razao))
    return ok, mal, pend


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg and arg[0] == "--afirmacoes":
        ok, mal, pend = afirmacoes()
        print("afirmacoes com fonte citavel: %d" % ok)
        for x in mal:
            print("  NAO CITAVEL  %s" % x)
        for x in pend:
            print("  PRETENDIDA   %s" % x)
        sys.exit(1 if mal else 0)
    if arg and arg[0] != "--tudo":
        sys.exit(_um(arg[0]))

    fora = varrer()
    n = len(fora)
    linha = json.load(io.open(BASE, encoding="utf-8"))["n"] \
        if os.path.exists(BASE) else None
    print("guioes que emitem resultado e NAO sao citaveis: %d" % n)
    for r in fora[:14]:
        print("   %s" % r)
    if n > 14:
        print("   ... e mais %d" % (n - 14))

    try:
        from proveniencia import guardar as _g
    except ImportError:
        def _g(d, c):
            json.dump(d, io.open(c, "w", encoding="utf-8"), indent=1,
                      ensure_ascii=False)
            return c

    if linha is None:
        _g({"n": n, "nota": "linha de base do roquete C10: esta contagem NAO "
                            "pode subir. Desce a medida que os guioes forem "
                            "certificados e atacados."}, BASE)
        print("linha de base fixada em %d" % n)
    elif n > linha:
        print("*** SUBIU %d — entrou resultado novo sem estatuto ***"
              % (n - linha))
        sys.exit(1)
    elif n < linha:
        print("desceu %d; a baixar a linha de base" % (linha - n))
        _g({"n": n, "nota": "roquete C10: so desce."}, BASE)
    else:
        print("linha de base: %d — estavel" % linha)
