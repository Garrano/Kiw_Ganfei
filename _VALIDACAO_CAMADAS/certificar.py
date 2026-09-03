# -*- coding: utf-8 -*-
"""certificar.py — a cadeia de camadas e controlos, corrida em vez de lembrada.

O PROBLEMA QUE ISTO RESOLVE
---------------------------
Os controlos deste processo estão todos escritos, e todos foram violados:

  · o controlo 1 (instrumento independente) está na `CONTROLOS.md` desde 28-08 e
    foi violado três vezes em três dias — o B1, o S9, o P3;
  · a guarda de cultura está no cabeçalho do `reg01_landsat.py`, com a frase
    exacta que descrevia o erro que eu ia cometer, e eu corri o ficheiro e
    publiquei o resultado à mesma;
  · a `LISTA_FINAL` é prosa, e prosa não é verificada por ninguém quando chega um
    facto novo.

**Uma regra que só existe em prosa cumpre-se quando dá jeito.** O `guarda.py`
tornou executável o controlo 1. Isto torna executável o resto: correr este
ficheiro **é** a certificação, e falha com código ≠ 0 quando alguma coisa não
bate.

O QUE VERIFICA
--------------
  1 · **O portão sobre todos os factos** — `registo_de_factos.py`, as cinco
      condições aplicadas a cada facto da LISTA_FINAL.
  2 · **A prosa não derivou do registo** — o conjunto de códigos de facto na
      `LISTA_FINAL.md` tem de ser igual ao do registo executável. É esta
      verificação que impede a lista de dizer uma coisa e o portão outra.
  3 · **Nenhum documento vivo cita um documento retirado.** Ontem havia dois
      documentos a afirmar o contrário da lista, no mesmo directório, sem marca.
  4 · **Os ficheiros que produzem os factos existem** — um facto cujo script
      desapareceu não é reproduzível.
  5 · **O rastreio de descontinuidade está fresco** — se os dados mudaram depois
      da última triagem, a prova de identidade das unidades está velha e todos os
      factos temporais assentam nela.
  6 · **O auto-teste do portão passa** — inclui as quatro retiradas históricas e
      o controlo positivo. Se o portão se estragar, tudo o resto é teatro.

MODOS
-----
    python certificar.py            rápido: 1-6, sem descarregar nada
    python certificar.py --completo além disso, volta a correr o rastreio de
                                    descontinuidade (descarrega, demora)
    python certificar.py --silencio só imprime se houver falha (para o gancho)

O QUE ISTO NÃO É
----------------
**Não é o pipeline.** Não recalcula NDVI, não refaz a triagem no modo rápido, e
não substitui o adversário nem o Controlo 3 — que são humanos ou sessões
independentes por desenho, e cuja função é encontrar premissas falsas
partilhadas, coisa que nenhum teste automático faz.
"""
import io
import os
import re
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"
LISTA = os.path.join(AQUI, "LISTA_FINAL_2026-08-31.md")
REGISTO = os.path.join(AQUI, "registo_de_factos.py")
GUARDA = os.path.join(AQUI, "guarda.py")
TRIAGEM = os.path.join(VG, "triagem_referencia_densa.json")
TRIAGEM_ALT = os.path.join(VG, "triagem_referencia.json")
FRESCO_DIAS = 30
# onde um facto pode ter o seu produtor. A C1 e a C2 puseram os seus em
# SAIDA_*, e ha scripts exploratorios em ganfei_s2.
DIRS_FACTOS = [VG, AQUI, os.path.join(AQUI, "SAIDA_C1"),
               os.path.join(AQUI, "SAIDA_C2"),
               "C:/Users/Jackster2/Downloads/ganfei_s2"]

COMPLETO = "--completo" in sys.argv
SILENCIO = "--silencio" in sys.argv
FALHAS, AVISOS = [], []
LINHAS = []


def diz(s=""):
    LINHAS.append(s)


def corre(args, nome):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable] + args, capture_output=True, env=env,
                       cwd=os.path.dirname(args[0]) or AQUI)
    saida = (p.stdout or b"").decode("utf-8", "replace")
    erro = (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, saida, erro


# ── 6 · o portão a si próprio, primeiro: se ele estiver partido nada mais conta
rc, out, err = corre([GUARDA], "guarda")
if rc != 0:
    FALHAS.append("o auto-teste do guarda.py falhou (%s)" % err.strip()[-160:])
else:
    bloqueados = out.count("VEREDICTO BLOQUEADO")
    passou = "ORI-COM tinha pérgola madura em 2012" in out
    naoapanhou = "*** PASSOU" in out or "*** BLOQUEOU um facto bom" in out
    if bloqueados < 4 or not passou or naoapanhou:
        FALHAS.append("o auto-teste do guarda.py mudou de comportamento: "
                      "%d bloqueios (esperados >= 4), controlo positivo %s"
                      % (bloqueados, "passa" if passou else "FALHA"))
    else:
        diz("  guarda.py        %d retiradas históricas bloqueadas, controlo positivo passa"
            % bloqueados)

# ── 1 · o portão sobre todos os factos
rc, out, err = corre([REGISTO], "registo")
m = re.search(r"passam: (\d+)\s+·\s+bloqueiam: (\d+)", out)
if rc != 0 or not m:
    bloq = re.findall(r"BLOQUEIA (\S+)", out)
    FALHAS.append("o registo de factos falhou: %s"
                  % (", ".join(bloq) if bloq else err.strip()[-200:]))
    CODIGOS_REG = set()
else:
    diz("  registo          %s factos passam, %s bloqueiam" % (m.group(1), m.group(2)))
    if "PODER BAIXO" in out:
        AVISOS.append("a prova de identidade em uso é a série esparsa (9 cenas). "
                      "Corre triagem_referencia_densa.py.")
    CODIGOS_REG = set(re.findall(r"OK\s+([ABCD]\d)\b", out))

# ── 2 · a prosa não derivou do registo
if os.path.exists(LISTA):
    txt = io.open(LISTA, encoding="utf-8").read()
    vivo = txt.split("## E · O QUE FOI RETIRADO")[0]
    # Os factos do bloco B estao numa TABELA (`| **B1** | ...`) e nao levam "·".
    # A primeira versao deste regex exigia o ponto medio e dava sete falsos
    # positivos — o verificador a acusar deriva que nao existia.
    CODIGOS_MD = set(re.findall(r"\*\*([ABCD]\d)\*?\*?\s*(?:·|\|)", vivo))
    so_md = CODIGOS_MD - CODIGOS_REG
    so_reg = CODIGOS_REG - CODIGOS_MD
    if so_md:
        FALHAS.append("a LISTA_FINAL afirma factos que o registo não certifica: %s"
                      % ", ".join(sorted(so_md)))
    if so_reg:
        FALHAS.append("o registo certifica factos que a LISTA_FINAL não menciona: %s"
                      % ", ".join(sorted(so_reg)))
    if not so_md and not so_reg and CODIGOS_REG:
        diz("  prosa/registo    %d códigos coincidem, sem deriva" % len(CODIGOS_REG))
else:
    FALHAS.append("LISTA_FINAL não encontrada em %s" % LISTA)

# ── 3 · nenhum documento vivo cita um documento retirado
RETIRADOS, VIVOS = set(), {}
for f in sorted(os.listdir(AQUI)):
    if not f.endswith(".md"):
        continue
    t = io.open(os.path.join(AQUI, f), encoding="utf-8", errors="replace").read()
    # SO o cartucho conta. A primeira versao aceitava tambem um titulo comecado
    # por "# RETIRO", e classificava como retirados os proprios documentos DE
    # retractacao (REG01_RETRACCAO_A3.md, P5_RETRACCAO...), que estao vivos e
    # sao o que vale. Resultado: acusava a LISTA_FINAL de citar um doc morto.
    if t.lstrip().startswith("> # ⚠ RETIRADO"):
        RETIRADOS.add(f)
    else:
        VIVOS[f] = t
maus = []
for f, t in VIVOS.items():
    for r in RETIRADOS:
        # "RETIR" e nao "RETIRAD": o cabecalho de um documento de retractacao diz
        # "**Retira:** `X.md`" — sem D — e sem isto o proprio documento que faz a
        # retractacao era acusado de citar um morto.
        if r in t and "RETIR" not in t[max(0, t.find(r) - 220):t.find(r) + 60].upper():
            maus.append("%s cita %s" % (f, r))
if maus:
    FALHAS.append("documento vivo a citar retirado sem o marcar: %s" % "; ".join(maus[:5]))
else:
    diz("  coerência docs   %d vivos, %d retirados, nenhuma citação por marcar"
        % (len(VIVOS), len(RETIRADOS)))

# ── 4 · os ficheiros que produzem os factos existem
txt_reg = io.open(REGISTO, encoding="utf-8").read()
falta = []
for fich in sorted(set(re.findall(r'ficheiro="([^"]+\.py)"', txt_reg))):
    if not any(os.path.exists(os.path.join(d, fich)) for d in DIRS_FACTOS):
        falta.append(fich)
if falta:
    FALHAS.append("scripts de factos que já não existem: %s" % ", ".join(falta))
else:
    diz("  reprodutibilidade todos os scripts citados existem em disco")

# ── 5 · o rastreio de descontinuidade está fresco
alvo = TRIAGEM if os.path.exists(TRIAGEM) else (
    TRIAGEM_ALT if os.path.exists(TRIAGEM_ALT) else None)
if alvo is None:
    FALHAS.append("não há rastreio de descontinuidade em disco")
else:
    idade = (time.time() - os.path.getmtime(alvo)) / 86400.0
    novos = [f for f in os.listdir(VG)
             if f.endswith(".json") and not f.startswith("triagem")
             and os.path.getmtime(os.path.join(VG, f)) > os.path.getmtime(alvo)]
    if idade > FRESCO_DIAS:
        AVISOS.append("o rastreio de descontinuidade tem %.0f dias" % idade)
    if novos:
        AVISOS.append("há %d resultados mais recentes que o rastreio (%s%s) — "
                      "se algum trouxe unidades novas, o rastreio está velho"
                      % (len(novos), ", ".join(novos[:3]),
                         "..." if len(novos) > 3 else ""))
    diz("  rastreio         %s, %.1f dias" % (os.path.basename(alvo), idade))

# ── 7 · as figuras nao derivaram do registo
#
# Acrescentada a 03-09-2026. As verificacoes 1-6 garantem que a LISTA_FINAL e o
# registo executavel dizem o mesmo. Nao garantiam nada sobre as FIGURAS, que sao
# o que uma pessoa de fora vai ler. E a P06 estava a afirmar «quinze retiradas»
# quando ja eram dezanove, e a dar a REG-01 como «por fazer» dois dias depois de
# ela ter sido corrida e invertida. E a mesma classe de falha uma camada acima.
#
# Duas verificacoes, e a primeira apanha tudo o que a segunda nao preve:
#   7a · uma figura mais VELHA do que a lista de factos esta desactualizada;
#   7b · o numero de retiradas que a P06 desenha tem de bater com o da lista.
FIG = r"C:/Users/Jackster2/Downloads/ganfei_s2/figuras"
NUM = {14: "catorze", 15: "quinze", 16: "dezasseis", 17: "dezassete",
       18: "dezoito", 19: "dezanove", 20: "vinte", 21: "vinte e uma",
       22: "vinte e duas", 23: "vinte e tres"}
if os.path.isdir(FIG) and os.path.exists(LISTA):
    t_lista = os.path.getmtime(LISTA)
    velhas = []
    for f in sorted(os.listdir(FIG)):
        if not (f.lower().startswith("p0") and f.lower().endswith(".png")):
            continue
        alvo = os.path.join(FIG, f)
        fonte = os.path.join(FIG, f[:f.rfind(".")].lower() + ".py")
        t = os.path.getmtime(alvo)
        if t < t_lista:
            velhas.append("%s (mais velha que a LISTA_FINAL)" % f)
        elif os.path.exists(fonte) and t < os.path.getmtime(fonte):
            velhas.append("%s (mais velha que o seu script)" % f)
    if velhas:
        FALHAS.append("figuras desactualizadas: %s" % "; ".join(velhas[:6]))
    else:
        diz("  figuras          nenhuma mais velha que a lista de factos")

    p06 = os.path.join(FIG, "p06_hipoteses_e_retirado.py")
    if os.path.exists(p06):
        txt = io.open(p06, encoding="utf-8", errors="replace").read()
        bloco = txt[txt.find("RETIRADO = ["):]
        bloco = bloco[:bloco.find("\n]")]
        n_fig = bloco.count('\n    ("')
        vivo_e = io.open(LISTA, encoding="utf-8").read()
        cab = vivo_e[vivo_e.find("## E · O QUE FOI RETIRADO"):][:80]
        esperado = NUM.get(n_fig)
        if esperado and esperado not in cab.lower():
            FALHAS.append("a P06 desenha %d retiradas e a LISTA_FINAL diz «%s»"
                          % (n_fig, cab.split("—")[-1].strip()))
        else:
            diz("  P06/lista        %d retiradas nas duas" % n_fig)

# ── modo completo: volta a correr o rastreio
if COMPLETO:
    diz()
    diz("  --completo: a correr o rastreio de descontinuidade...")
    rc, out, err = corre([os.path.join(VG, "triagem_referencia_densa.py")], "densa")
    if rc != 0:
        FALHAS.append("o rastreio denso falhou: %s" % err.strip()[-200:])
    elif "LINE-STOP" in out:
        FALHAS.append("LINE-STOP no rastreio: a referência tem descontinuidade")
    else:
        diz("  rastreio denso   referência contínua")

# ────────────────────────────────────────────────────────────────── relatório
ok = not FALHAS
if not (SILENCIO and ok and not AVISOS):
    print("=" * 78)
    print("CERTIFICAÇÃO DA CADEIA — %s%s"
          % (time.strftime("%Y-%m-%d %H:%M"), "  (completo)" if COMPLETO else ""))
    print("=" * 78)
    for l in LINHAS:
        print(l)
    if AVISOS:
        print()
        print("AVISOS:")
        for a in AVISOS:
            print("  · %s" % a)
    print()
    if ok:
        print("CERTIFICADA. As SEIS condições do portão valem para todos os factos,")
        print("e a prosa não derivou do registo.")
    else:
        print("NÃO CERTIFICADA — %d falha(s):" % len(FALHAS))
        for f in FALHAS:
            print("  · %s" % f)
        print()
        print("Nada de novo entra na LISTA_FINAL enquanto isto não fechar.")
sys.exit(0 if ok else 1)
