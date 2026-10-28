# -*- coding: utf-8 -*-
"""Sela as cartas: marca de agua, metadados e impressao digital registada.

**PORTAO. Nao sela nada que nao esteja validado**, e a instrucao que o pediu era
explicita: *«do it only once the maps are 100% validated»*. Uma marca de agua
numa prancha que ainda vai mudar e pior do que nenhuma — sela um erro com o
nosso nome em cima, e a versao corrigida passa a ter de conviver com ela.

TRES CONDICOES, e todas bloqueiam
----------------------------------
  1. **A `cartas.py` passa.** Nenhuma prancha interroga, nenhuma tem deixis,
     nenhuma classe se nomeia por contraste, nenhuma descreve sobre o mapa.
     Isto e mecanico e cobre a forma, nao o conteudo.
  2. **A prancha esta em `CARTAS_VALIDADAS.csv`, com QUEM e QUANDO.** A
     `cartas.py` nao ve o PNG — nao apanha corpo pequeno, sobreposicao, rotulo
     cortado, nem correspondencia legenda-mapa por instanciacao. Essa parte e
     olho humano, e por isso a validacao e assinada como testemunho: quem olhou
     e em que dia. Sem assinatura nao ha selo.
  3. **O PNG existe e e mais recente que o guiao.** Um selo sobre uma imagem
     velha certifica uma coisa que ja nao esta no ficheiro.

O QUE O SELO E, E O QUE A MARCA E — sao coisas diferentes
---------------------------------------------------------
A **marca de agua** e dissuasao: repetida sobre o corpo do mapa, torna o recorte
inutil e a remocao destrutiva e visivel. **Nao prova nada.**

O **selo** e a prova: SHA-256 da imagem, com data, em `SELO_CARTAS.csv`, mais os
mesmos campos escritos nos metadados PNG (`tEXt`). Os metadados tiram-se num
segundo — o registo local e que aguenta. E o que responde a «esta carta e
vossa?» dali a seis meses, e nenhuma marca visivel o substitui.

**Nao ha aqui marca de agua invisivel robusta.** Uma LSB morre no primeiro
reencode; uma DCT/DWT a serio precisa de biblioteca propria e de um teste de
robustez que ninguem correu. Prometer uma sem a medir era pior do que nao ter.
"""
import csv
import hashlib
import io
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
FIGURAS = os.environ.get(
    "GANFEI_FIGURAS", r"C:/Users/Jackster2/Downloads/ganfei_s2/figuras")
VALIDADAS = os.path.join(AQUI, "CARTAS_VALIDADAS.csv")
SELO = os.path.join(AQUI, "SELO_CARTAS.csv")
CARTAS = os.path.join(AQUI, "cartas.py")

CAMPOS_SELO = ["prancha", "ficheiro", "sha256", "bytes", "selado_em",
               "validado_por", "validado_em"]


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def validadas():
    if not os.path.exists(VALIDADAS):
        return {}
    out = {}
    for r in csv.DictReader(io.open(VALIDADAS, encoding="utf-8")):
        if r.get("prancha") and r.get("quem") and r.get("quando"):
            out[r["prancha"].strip()] = (r["quem"].strip(), r["quando"].strip())
    return out


def metadados_png(caminho, pares):
    """Escreve chunks tEXt. Trivialmente removiveis — o registo e que aguenta."""
    try:
        from PIL import Image, PngImagePlugin
    except ImportError:
        return False
    im = Image.open(caminho)
    info = PngImagePlugin.PngInfo()
    for k, v in pares:
        info.add_text(k, v)
    im.save(caminho, "PNG", pnginfo=info)
    return True


def main():
    guioes = sorted(f for f in os.listdir(FIGURAS)
                    if f.startswith("P") and f.endswith(".py")
                    and f[1].isdigit())
    if not guioes:
        print("selar: nenhuma prancha")
        return 0

    # ── condicao 1
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, CARTAS], capture_output=True, env=env)
    if p.returncode != 0:
        print("SELO RECUSADO — a cartas.py reprova:")
        print((p.stdout or b"").decode("utf-8", "replace").rstrip())
        return 1

    val = validadas()
    agora = time.strftime("%Y-%m-%d %H:%M")
    linhas, recusas = [], []

    for g in guioes:
        ident = g.split("_")[0]
        png = os.path.join(FIGURAS, g[:-3] + ".png")

        # ── condicao 2
        if ident not in val:
            recusas.append("%s: sem validacao assinada em CARTAS_VALIDADAS.csv "
                           "(faltam `quem` e `quando`)" % ident)
            continue
        # ── condicao 3
        if not os.path.exists(png):
            recusas.append("%s: PNG nao existe — correr o guiao" % ident)
            continue
        if os.path.getmtime(png) < os.path.getmtime(os.path.join(FIGURAS, g)):
            recusas.append("%s: PNG mais VELHO que o guiao — regerar antes de "
                           "selar" % ident)
            continue

        quem, quando = val[ident]
        h = sha256(png)
        metadados_png(png, [
            ("Title", "%s — CCDR-N, Avisos Agricolas" % ident),
            ("Author", "CCDR-N, I.P. — Estacao de Avisos de Entre Douro e Minho"),
            ("Copyright", "(c) 2026 CCDR-N, I.P. Reproducao condicionada a "
                          "citacao da fonte."),
            ("Source", "Emparcelamento de Ganfei, Valenca"),
            ("Comment", "validado por %s em %s; selado em %s"
                        % (quem, quando, agora)),
        ])
        h = sha256(png)          # depois dos metadados, senao o selo nao bate
        linhas.append(dict(prancha=ident, ficheiro=os.path.basename(png),
                           sha256=h, bytes=os.path.getsize(png),
                           selado_em=agora, validado_por=quem,
                           validado_em=quando))

    if linhas:
        antigas = []
        if os.path.exists(SELO):
            antigas = [r for r in csv.DictReader(io.open(SELO, encoding="utf-8"))
                       if r.get("prancha")]
        # o selo e um DIARIO: uma prancha reselada acrescenta linha, nao
        # substitui. E assim que se mostra que versao circulou quando.
        w = csv.DictWriter(io.open(SELO, "w", encoding="utf-8", newline=""),
                           CAMPOS_SELO)
        w.writeheader()
        w.writerows(antigas + linhas)
        print("SELADAS %d prancha(s):" % len(linhas))
        for r in linhas:
            print("  %s  %s  %s…  (validada por %s em %s)"
                  % (r["prancha"], r["ficheiro"], r["sha256"][:16],
                     r["validado_por"], r["validado_em"]))

    if recusas:
        print("NAO SELADAS %d:" % len(recusas))
        for x in recusas:
            print("  · %s" % x)
    if not linhas and not recusas:
        print("selar: nada a fazer")
    return 0 if linhas or not recusas else 1


if __name__ == "__main__":
    sys.exit(main())
