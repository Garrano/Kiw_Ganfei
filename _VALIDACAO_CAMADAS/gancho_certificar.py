# -*- coding: utf-8 -*-
"""Invólucro do gancho: corre a certificação e devolve JSON ao Claude Code.

PORQUE UM INVÓLUCRO E NÃO O SCRIPT DIRECTO
-------------------------------------------
Um gancho `Stop` só mostra alguma coisa ao utilizador se escrever em stdout um
JSON com `systemMessage`. O `certificar.py` escreve texto para uma pessoa ler no
terminal. Este ficheiro faz a tradução, e só isso.

Também absorve o que um gancho nunca deve fazer: **rebentar**. Se a certificação
falhar por razão técnica — Python trocado, ficheiro em falta, disco ocupado — o
gancho diz-o em vez de bloquear o turno com um traceback.

O QUE APARECE
-------------
  · cadeia limpa  -> nada. Silêncio é o estado normal.
  · cadeia suja   -> uma mensagem com as falhas, ao fim do turno.
  · avisos só     -> nada no ecrã (os avisos não são falhas), excepto se
                     `--avisos` for passado.

**Não bloqueia o turno.** `continue` fica a true de propósito: a certificação
diz que alguma coisa não bate, não decide que o trabalho pára. Quem decide é
quem está a ler.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(AQUI, "certificar.py")
MOSTRA_AVISOS = "--avisos" in sys.argv


def main():
    try:
        sys.stdin.read()          # o gancho recebe JSON; não é preciso, mas drena
    except Exception:
        pass
    if not os.path.exists(CERT):
        print(json.dumps({"systemMessage":
                          "certificar.py não está em %s — a cadeia não foi "
                          "verificada." % AQUI}))
        return
    try:
        p = subprocess.run([sys.executable, CERT, "--silencio"],
                           capture_output=True, timeout=180,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                           cwd=AQUI)
    except subprocess.TimeoutExpired:
        print(json.dumps({"systemMessage":
                          "A certificação da cadeia excedeu 180 s e foi "
                          "interrompida. Corre certificar.py à mão."}))
        return
    except Exception as e:
        print(json.dumps({"systemMessage":
                          "A certificação da cadeia não correu: %s"
                          % type(e).__name__}))
        return

    saida = (p.stdout or b"").decode("utf-8", "replace").strip()
    if p.returncode == 0 and not (MOSTRA_AVISOS and saida):
        return                     # limpa: silêncio
    if not saida:
        saida = ((p.stderr or b"").decode("utf-8", "replace").strip()
                 or "a certificação saiu com código %d sem dizer porquê"
                 % p.returncode)
    cab = ("CADEIA NÃO CERTIFICADA" if p.returncode else "certificação — avisos")
    # ensure_ascii=True (o omissivo): a consola do Windows e cp1252 e um JSON
    # com acentos crus sai mutilado — "NAO" aparecia como "N?O". Com escapes
    # unicode o JSON fica ASCII puro e chega intacto a qualquer leitor.
    print(json.dumps({"systemMessage": "%s\n%s" % (cab, saida[:3000])}))


if __name__ == "__main__":
    main()
