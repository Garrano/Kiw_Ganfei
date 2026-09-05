# -*- coding: utf-8 -*-
"""proveniencia.py — nenhum artefacto sem produtor, e a dívida não cresce.

    from proveniencia import guardar
    guardar(dados, "o_meu_resultado.json")

O QUE ISTO RESOLVE
------------------
O `valvulas_v6.json` traz uma lista de treze sectores por ordem espacial —
informação que ninguém mais tem — e **nenhum ficheiro em disco a escreve**. Não
há como saber quem a produziu, quando, nem de que leitura saiu. Quando o
adversário perguntou se ela corroborava a minha leitura das etiquetas, a
resposta honesta foi «não sei de onde vem», e por isso não pôde contar.

Um número sem produtor não é prova: é boato com casas decimais.

Medido a 05-09-2026: **52 dos 57 `.json` correntes** não trazem marca nenhuma
de quem os escreveu.

A REGRA 1 DE SANDVE
-------------------
«For every result, keep track of how it was produced.» É a primeira das dez
regras, e é a que o Sumatra automatiza: registar o contexto em que um guião
correu — parâmetros, ambiente, versão, e a ligação aos ficheiros de saída.

O ROQUETE, e é o que a torna praticável aqui
---------------------------------------------
Retroactivar os 52 significaria voltar a correr 52 guiões, alguns dos quais
descarregam dados. Caro, e arriscado num sítio onde mexer em caminhos já
partiu coisas.

A prática de topo para dívida herdada não é pagá-la de uma vez: é **impedir que
cresça**. Guarda-se a contagem actual como linha de base e o certificador
**falha se ela subir**. Cada guião que for tocado passa a usar `guardar()` e a
dívida desce sozinha, sem ninguém ter de a atacar de frente.
"""
import datetime as _dt
import io as _io
import json as _json
import os as _os
import subprocess as _sp
import sys as _sys


def _commit():
    try:
        r = _sp.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                    cwd=_os.path.dirname(_os.path.abspath(__file__)), timeout=8)
        return (r.stdout or b"").decode().strip() or None
    except Exception:
        return None


def marca(extra=None):
    """O carimbo: quem escreveu, quando, e de que estado do repositório."""
    m = {"script": _os.path.basename(getattr(_sys.modules.get("__main__"),
                                             "__file__", "?")),
         "quando": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
         "commit": _commit()}
    if extra:
        m.update(extra)
    return m


def guardar(dados, caminho, extra=None, **kw):
    """Escreve JSON com o carimbo do produtor em `_produtor`.

    Se `dados` não for um dicionário, embrulha-se em `{"_produtor":…, "dados":…}`
    — porque um artefacto sem sítio para o carimbo não é razão para o dispensar.
    """
    if isinstance(dados, dict):
        saida = dict(dados)
        saida["_produtor"] = marca(extra)
    else:
        saida = {"_produtor": marca(extra), "dados": dados}
    kw.setdefault("indent", 1)
    kw.setdefault("ensure_ascii", False)
    with _io.open(caminho, "w", encoding="utf-8") as f:
        _json.dump(saida, f, **kw)
    return caminho


# ── o roquete ───────────────────────────────────────────────────────────────
AQUI = _os.path.dirname(_os.path.abspath(__file__))
BASE = _os.path.join(AQUI, "proveniencia_base.json")
MARCAS = ("_produtor", "_metodo", "_script")


def sem_produtor(raiz=r"C:/Users/Jackster2/Downloads"):
    """Os .json CORRENTES que não trazem marca de quem os escreveu."""
    p = _os.path.join(AQUI, "triagem_de_fontes.json")
    if not _os.path.exists(p):
        return None
    C = _json.load(_io.open(p, encoding="utf-8"))["classe"]
    fora = []
    for k, v in C.items():
        if v != "CORRENTE" or not k.endswith(".json"):
            continue
        try:
            t = _io.open(_os.path.join(raiz, k), encoding="utf-8",
                         errors="ignore").read(3000)
        except OSError:
            continue
        if not any(m in t for m in MARCAS):
            fora.append(k)
    return sorted(fora)


if __name__ == "__main__":
    fora = sem_produtor()
    if fora is None:
        raise SystemExit("falta a triagem — corre triagem_de_fontes.py")
    n = len(fora)
    linha = _json.load(_io.open(BASE, encoding="utf-8"))["n"] \
        if _os.path.exists(BASE) else None
    print("artefactos correntes sem produtor: %d" % n)
    if linha is None:
        _json.dump({"n": n, "fixado": _dt.datetime.now().strftime("%Y-%m-%d"),
                    "nota": "linha de base do roquete: esta contagem NÃO pode "
                            "subir. Desce sozinha à medida que os guiões forem "
                            "tocados e passarem a usar guardar()."},
                   _io.open(BASE, "w", encoding="utf-8"), indent=1,
                   ensure_ascii=False)
        print("linha de base fixada em %d" % n)
    else:
        print("linha de base: %d" % linha)
        if n > linha:
            print("*** SUBIU %d — entrou artefacto novo sem produtor ***" % (n - linha))
            raise SystemExit(1)
        if n < linha:
            print("desceu %d; a baixar a linha de base" % (linha - n))
            _json.dump({"n": n, "fixado": _dt.datetime.now().strftime("%Y-%m-%d"),
                        "nota": "roquete: só desce."},
                       _io.open(BASE, "w", encoding="utf-8"), indent=1,
                       ensure_ascii=False)
        else:
            print("estável")
