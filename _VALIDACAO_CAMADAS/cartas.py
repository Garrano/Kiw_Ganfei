# -*- coding: utf-8 -*-
"""C11 executavel — o que uma carta pode dizer, e como o diz.

PORQUE EXISTE
-------------
06-09-2026. Foi-me dito, por escrito, que as perguntas pertencem ao corpo do
email. Corrigi a P13 e **a seguir repeti a falta na P14**. Escrevi esta
verificacao. E na prancha a seguir voltei a falhar por outras tres vias, todas
elementares:

  · rotulei uma classe como «o talhao por que perguntamos» — que descreve a
    NOSSA relacao com a feicao, nao a feicao;
  · anotei «o talhao em causa» sobre o mapa, duplicando o que a legenda ja
    dizia;
  · deixei na legenda «as outras valvulas» depois de remover a classe com que
    esse «outras» contrastava — uma entrada de legenda sem referente.

Nenhuma destas e materia de gosto. Sao as regras basicas da portrayal
cartografica, e passam a ser verificadas.

AS OITO CONDICOES
-----------------
Sobre o texto DESENHADO, lido por `ast` — so o que entra em `.text()` e
`.annotate()`, para que um comentario possa explicar a regra sem a violar.

  1. **Nenhuma interrogacao desenhada.** A pergunta vive no corpo do email; a
     carta serve-a tornando-a mais clara. Quando a peca tem mesmo de colher uma
     resposta, o dispositivo e **forma, nao frase**: uma caixa vazia junto de um
     rotulo. Distingue-se da interrogacao o **rotulo interrogado** — `N?` em
     italico, atributo inferido, norma centenaria em geologia e arqueologia. Uma
     frase que FECHA em `?` interroga; um `?` colado a rotulo curto qualifica.

  2. **Titulo nominal, no registo institucional da familia:** `GANFEI · <sintagma>`.

  3. **Nada do nosso processo na prancha** — metodo, ressalva, estatuto,
     vocabulario interno. As FONTES sao a excepcao: nomear o instrumento e
     proveniencia, nao metodo.

  4. **FONTES declaradas** em estilo proprio.

  5. **Sem deixis.** Nenhuma primeira nem segunda pessoa no texto desenhado.
     Uma legenda nomeia o FENOMENO, nao a relacao do autor com ele. «o talhao
     por que perguntamos», «na posicao que temos», «as que nos indicou» — todas
     erradas pela mesma razao: poem o autor dentro da legenda. O registo e
     impessoal e nominal.

  6. **Nenhuma classe nomeada por contraste.** «as outras valvulas», «os
     restantes sectores» — uma entrada de legenda define-se pelo que E, nao pelo
     que nao e. E o termo relativo sobrevive a remocao do seu contraste sem dar
     erro nenhum, que foi exactamente o que aconteceu: tirei a classe destacada
     e o «outras» ficou la, a apontar para nada.

  7. **A anotacao sobre o mapa e para NOMES e VALORES.** Toponimos, codigos de
     sector, medidas. **A identidade de classe pertence a legenda** — anotar
     «o talhao em causa» sobre a feicao duplica a legenda e desalinha-se dela na
     primeira edicao. Heuristica: uma anotacao no eixo do mapa que comeca por
     minuscula e tem duas ou mais palavras e descricao, nao nome.

  8. **So os nomes do gestor.** Uma peca designa as coisas pelos nomes que quem
     a recebe usa todos os dias — B1, B2, B3, B4, Erica Novo, Viveiro, B3C3,
     valvula 14 — e nunca pela geografia analitica que nos inventamos.
     «Talhao a nascente» nao quer dizer nada para quem tem os talhoes com nome;
     e «Zona 0» e pior, porque e uma palavra DELE que nos aplicamos a outro
     sitio.

O QUE NAO VERIFICA
------------------
Nao ve o PNG. Corpo pequeno, sobreposicao, rotulo cortado, e sobretudo
**correspondencia legenda-mapa por instanciacao** — se uma classe da legenda tem
mesmo ocorrencias no desenho — passam-lhe ao lado. **A prancha tem de ser olhada
depois de gerada, e a legenda lida contra o que aparece.**
"""
import ast
import io
import os
import re
import sys

FIGURAS = os.environ.get(
    "GANFEI_FIGURAS",
    r"C:/Users/Jackster2/Downloads/ganfei_s2/figuras")

# 3 · vocabulario do nosso processo
# 06-09: a versao anterior dizia `ressalva\b` e NAO apanhava «ressalvas». A P11
# trazia «Método e ressalvas em FIGURAS_ABSTRACTS.md» — processo nosso na
# prancha, e a apontar para um ficheiro interno — e passou verde. Todas as
# entradas levam agora sufixo livre, e junta-se o nome de ficheiro interno, que
# e a forma mais crua de falar de nos a quem recebe a carta.
INTERNO = re.compile(
    r"\b(ressalva\w*|método\w*|metodolog\w*|MDE|NDVI|certificad\w*|"
    r"adversári\w*|auditori\w*|p-valor|desvio-padrão|máscara\w*|píxel\w*|"
    r"pixel\w*|limiar\w*|amostragem\w*|estatístic\w*|reprodutib\w*|"
    r"hipótese\w*|multivers\w*)\b"
    r"|\b\w+\.(md|py|json|csv|npz|npy)\b", re.I)

# 5 · deixis: primeira e segunda pessoa. Uma legenda nao fala de quem a fez.
DEIXIS = re.compile(
    r"\b(nós|nosso|nossa|nossos|nossas|"
    r"\w*[áa]mos|\w+[ei]mos|"
    r"indicou|enviou|referiu|disse|assinale|riscar)\b", re.I)

# 6 · classes nomeadas por contraste em vez de por identidade
RELATIVO = re.compile(r"\b(outr[ao]s?|restantes|demais|remanescentes)\b", re.I)

TITULO_FAMILIA = re.compile(r"^GANFEI · [A-ZÀ-Ú0-9]")

# 8 · SO OS NOMES DO GESTOR.
#
# Uma peca que sai daqui designa as coisas pelos nomes que quem a recebe usa
# todos os dias — B1, B2, B3, B4, Erica Novo, Viveiro, B3C3, valvula 14. Nunca
# pela geografia analitica que nos inventamos para trabalhar.
#
# «Talhao a nascente» nao quer dizer nada para quem tem os talhoes com nome. E
# «Zona 0» e pior do que nada: e uma palavra DELE, aplicada por nos a outro
# sitio — o gestor escreveu que a Zona 0 sao as valvulas 8, 9 e 10, a poente, e
# a prancha imprimia-a sobre o talhao nascente. Contradizia-o sem o dizer.
#
# Regra dada por escrito, e falhada na mesma. Passa a bloquear.
NOSSA_GEOGRAFIA = re.compile(
    r"\bfocos?\b|\blobo\b|\bAOI\b|\bnu2021\b|\bzona\s*0\b|\bcomparador\w*\b|"
    r"\bâncora\w*\b|\bancora\w*\b|"
    r"\b(talh[ãa]o|bloco|sector|zona|parcela)\s+(a\s+|do\s+|de\s+)?"
    r"(nascente|poente|oriental|ocidental|este|oeste)\b", re.I)

# metodos que poem texto no papel. `legenda` e da `carta_base` e foi o buraco.
DESENHAM = ("text", "annotate", "legenda", "set_title", "suptitle", "fontes")
TEXTO_KW = ("nota", "notas", "texto", "titulo", "label", "sub", "s", "linhas")


def interroga(t):
    """A pergunta ao leitor, distinguida do rotulo interrogado."""
    s = t.strip().rstrip(u"»\"')")
    return s.endswith("?") and len(s.split()) > 1


def descreve_em_vez_de_nomear(t):
    """Anotacao de mapa que e descricao e nao nome/valor."""
    s = t.strip()
    if not s or not s[0].islower():
        return False
    return len(s.split()) >= 2


def literais_desenhadas(arvore):
    """Devolve (todas, titulo, no_mapa). `no_mapa` = anotacoes no eixo `ax`."""
    todas, titulo, no_mapa = [], None, []
    for n in ast.walk(arvore):
        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute):
            continue
        if n.func.attr not in DESENHAM:
            continue
        recept = getattr(n.func.value, "id", "")
        cs = [a for a in n.args if isinstance(a, ast.Constant)
              and isinstance(a.value, str)]
        # Texto passado por PALAVRA-CHAVE. A P11 mandava «Método e ressalvas em
        # FIGURAS_ABSTRACTS.md» por `b.legenda(nota=...)` e passou verde, porque
        # eu so lia argumentos posicionais de .text/.annotate. A lista de
        # palavras e restrita de proposito: `.text()` leva family=, color= e
        # ha= que sao cadeias e nao sao texto desenhado.
        cs += [kw.value for kw in n.keywords
               if kw.arg in TEXTO_KW and isinstance(kw.value, ast.Constant)
               and isinstance(kw.value.value, str)]
        eh_titulo = any(isinstance(a, ast.Name) and a.id == "ytop"
                        for a in n.args[:2])
        for c in cs:
            todas.append(c.value)
            if recept == "ax":
                no_mapa.append(c.value)
            if eh_titulo and titulo is None and c.value.strip():
                titulo = c.value
    return todas, titulo, no_mapa


def verifica(caminho):
    nome = os.path.basename(caminho)
    fonte = io.open(caminho, encoding="utf-8").read()
    try:
        arvore = ast.parse(fonte)
    except SyntaxError as e:
        return ["%s nao compila (linha %s)" % (nome, e.lineno)]

    todas, titulo, no_mapa = literais_desenhadas(arvore)
    m = []
    curto = lambda t: repr(t.replace("\n", " ")[:58])

    for t in todas:
        if t != titulo and interroga(t):
            m.append("%s: interrogacao DESENHADA — %s. A pergunta vai no corpo "
                     "do email; aqui usa-se forma (caixa vazia)."
                     % (nome, curto(t)))
        a = INTERNO.search(t)
        if a:
            m.append("%s: vocabulario do nosso processo — %r em %s"
                     % (nome, a.group(0), curto(t)))
        a = DEIXIS.search(t)
        if a:
            m.append("%s: DEIXIS — %r em %s. Uma legenda nomeia o fenomeno, "
                     "nao a relacao do autor com ele; o registo e impessoal."
                     % (nome, a.group(0), curto(t)))
        a = NOSSA_GEOGRAFIA.search(t)
        if a:
            m.append("%s: NOME NOSSO em vez do nome do gestor — %r em %s. Uma "
                     "peça designa as coisas pelos nomes que quem a recebe usa: "
                     "B1, B2, B3, B4, Erica Novo, Viveiro, B3C3, válvula 14."
                     % (nome, a.group(0), curto(t)))
        a = RELATIVO.search(t)
        if a:
            m.append("%s: classe nomeada por CONTRASTE — %r em %s. Uma entrada "
                     "de legenda define-se pelo que e, e um termo relativo "
                     "sobrevive a remocao do seu contraste sem dar erro."
                     % (nome, a.group(0), curto(t)))

    for t in no_mapa:
        if descreve_em_vez_de_nomear(t):
            m.append("%s: DESCRICAO anotada sobre o mapa — %s. A anotacao e "
                     "para nomes e valores; a identidade de classe pertence a "
                     "legenda." % (nome, curto(t)))

    if titulo is None:
        m.append("%s: nao encontrei titulo ancorado em `ytop`" % nome)
    elif "?" in titulo:
        m.append("%s: TITULO INTERROGATIVO — %r. Um titulo e uma designacao, "
                 "nao uma fala." % (nome, titulo))
    elif not TITULO_FAMILIA.match(titulo):
        m.append("%s: titulo fora do registo da familia — %r. Esperado "
                 "'GANFEI · <sintagma nominal>', tom institucional."
                 % (nome, titulo))

    if not re.search(r"^\s*fontes\(", fonte, re.M):
        m.append("%s: sem bloco FONTES. Uma carta declara a proveniencia — "
                 "satelite, espectro, altimetria — em estilo proprio." % nome)
    return m


def main():
    if not os.path.isdir(FIGURAS):
        print("cartas: directorio de figuras nao encontrado (%s)" % FIGURAS)
        return 0
    guioes = sorted(f for f in os.listdir(FIGURAS)
                    if re.match(r"^P\d+_.*\.py$", f))
    if not guioes:
        print("cartas: nenhuma prancha encontrada")
        return 0

    mal = []
    for g in guioes:
        mal += verifica(os.path.join(FIGURAS, g))

    if mal:
        print("CARTAS: %d prancha(s) verificadas, %d falta(s)"
              % (len(guioes), len(mal)))
        for x in mal:
            print("  FALHA %s" % x)
        return 1
    print("CARTAS: %d pranchas · sem perguntas, sem deixis, sem classes por "
          "contraste, anotacao so de nomes, todas com FONTES" % len(guioes))
    return 0


# ── auto-teste. C2: cada condicao e a UNICA razao de reprovacao em pelo menos
#    um caso — senao ficar inerte e indetectavel, que e a forma B.
FT = '\nfontes(fig, ["x"])\n'
BOM = 'fig.text(0, ytop, "GANFEI · X")\n'
CASOS = [
    ("1 · titulo interrogativo",
     'fig.text(0, ytop, "ONDE FICA O B3?")' + FT, "TITULO INTERROGATIVO"),
    ("1 · pergunta na legenda",
     BOM + 'axl.text(0, 0, "Qual dos dois talhoes e o B3?")' + FT,
     "interrogacao DESENHADA"),
    ("2 · titulo fora do registo",
     'fig.text(0, ytop, "plantas perdidas")' + FT, "fora do registo da familia"),
    ("3 · processo na prancha",
     BOM + 'axl.text(0, 0, "ressalva: nao separa estrutura")' + FT,
     "vocabulario do nosso processo"),
    ("4 · sem fontes", BOM, "sem bloco FONTES"),
    ("5 · deixis na legenda",
     BOM + 'axl.text(0, 0, "o talhao por que perguntamos")' + FT, "DEIXIS"),
    ("6 · classe por contraste",
     BOM + 'axl.text(0, 0, "as outras valvulas")' + FT,
     "nomeada por CONTRASTE"),
    ("7 · descricao anotada no mapa",
     BOM + 'ax.text(0, 0, "o talhao em causa")' + FT,
     "DESCRICAO anotada sobre o mapa"),
    ("8 · nome nosso em vez do nome do gestor",
     BOM + 'axl.text(0, 0, "o talhao a nascente")' + FT,
     "NOME NOSSO em vez do nome do gestor"),
    ("8 · Zona 0 aplicada por nos",
     BOM + 'axl.text(0, 0, "Zona 0, inicio do declinio")' + FT,
     "NOME NOSSO em vez do nome do gestor"),
    # controlo positivo: rotulo interrogado, toponimo, codigo e medida passam
    ("controlo positivo",
     'fig.text(0, ytop, "GANFEI · ESQUEMA DE REGA")\n'
     'ax.text(0, 0, "RIO MINHO")\nax.text(0, 0, "B3")\n'
     'ax.text(0, 0, "500 m")\naxl.annotate("N?", (0, 0))\n'
     'axl.text(0, 0, "válvulas de rega")' + FT, None),
]


def auto_teste():
    import tempfile
    mau = []
    for nome, fonte, esperado in CASOS:
        p = os.path.join(tempfile.mkdtemp(), "P99_caso.py")
        io.open(p, "w", encoding="utf-8").write(fonte)
        saiu = verifica(p)
        if esperado is None:
            if saiu:
                mau.append("%s: devia PASSAR e reprovou — %s" % (nome, saiu[0]))
            else:
                print("  OK   %s" % nome)
            continue
        proprias = [x for x in saiu if esperado in x]
        if not proprias:
            mau.append("%s: a condicao NAO disparou (esperado %r)"
                       % (nome, esperado))
        elif len(saiu) > len(proprias):
            outras = [x for x in saiu if esperado not in x]
            mau.append("%s: nao isola — tambem reprovou por %r"
                       % (nome, outras[0][:80]))
        else:
            print("  OK   %s — bloqueia sozinha" % nome)
    if mau:
        print("AUTO-TESTE DAS CARTAS FALHOU:")
        for x in mau:
            print("  · %s" % x)
        return 1
    print("auto-teste: as 8 condicoes bloqueiam sozinhas, e o controlo positivo "
          "passa — desligar qualquer uma e detectavel")
    return 0


if __name__ == "__main__":
    if "--auto-teste" in sys.argv:
        sys.exit(auto_teste())
    sys.exit(main())
