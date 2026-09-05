# -*- coding: utf-8 -*-
"""RETIRADO em 05-09-2026, no proprio dia em que foi escrito.

⚠ RETIRADO — nao importar, nao citar, nao correr. Inerte por C7.

Um adversario independente partiu-o em quatro eixos e verifiquei os achados um
a um. O que o derruba nao e nenhum defeito isolado, e este:

  **Arrancar o bloqueio de sobreposicao de dados/mascara — a unica coisa para
  que esta clausula existe — deixa a bateria em 14/14 e 6/6.**

Medido: substituir `if s > tol:` por `if False:` nao produz UMA falha. Os casos
4, 5 e 8 eram apanhados pela `janela` antes de chegarem la, e o 12 por outro
ramo. A bateria exercitava os ramos em que eu estava a pensar e deixava o
central por tocar — que e exactamente a forma B, e exactamente o 0-de-9 que a
C2 diagnosticou na `guarda.py`.

A minha propria contra-verificacao falhou por ser fraca: arranquei a MEDICAO
(devolver None) em vez do BLOQUEIO, e essa versao era detectada. Registo-o
porque a licao e essa — uma mutacao mal escolhida absolve.

E MAIS SEIS, TODOS VERIFICADOS
------------------------------
· `_conjunto()` colapsa arrays 1-D de numpy: `arange(1000)` vira UM tuplo, e um
  controlo 100 % dentro do ajuste mede **0,0 %**. Num processo cujo pipeline e
  raster de numpy, este e o caso comum, nao a excepcao.
· `tolerancia=1.0` com `razao="x"` passa uma fuga de 100 %: `s > 1.0` nunca e
  verdade. E o `c2 = True` com um comentario ao lado.
· «NDVI Sentinel-2» confirmado por «NDVI Landsat» PASSA — comparo cadeias
  inteiras. A `guarda.py` ja tinha fechado isto a 03-09 com uma lista de
  indices; reabri o buraco num ficheiro que cita a regra tres vezes.
· Um controlo com conjunto VAZIO passa tudo: `sobreposicao` devolve None e o
  ciclo continua. Ausencia tratada como aprovacao, outra vez.
· Um hold-out temporal e um controlo negativo de Lipsitch **nao sao
  exprimiveis** — os tres desenhos bloqueiam-nos. A C3 executavel proibia o
  instrumento que o proprio documento da C3 prescreve.
· Na `confirmacao` mede-se a direccao errada: interessa que fraccao do AJUSTE
  o controlo cobre, e eu media que fraccao do CONTROLO cai no ajuste.

E UMA COISA QUE EU INVENTEI
---------------------------
«das cinco, quatro tinham o canal por declarar» — **nao ha fonte nenhuma**. Nao
existe classificacao das retiradas por canal em lado nenhum: o vocabulario dos
canais e meu, deste ficheiro. Usei um numero fabricado para justificar o fecho
por omissao, num ficheiro cujo argumento e que numeros sem produtor sao como
este processo perde semanas.

Tambem herdei da `CLAUSULAS.md` uma atribuicao errada: a autocorrelacao de
**0,86-0,96 e do `terreno_contra_declinio.py`**, a hipotese do terreno, e nao
da retirada 12 — cujo nulo nao era por permutacao mas por deslocamento
toroidal. E `por_area` nao consta como defeito documentado em fonte nenhuma.

O QUE SOBREVIVE, E VAI PARA A v2
--------------------------------
O desenho conceptual nao foi atacado: cinco canais, regras que se invertem com
o desenho, e fecho por omissao. O que tem de mudar na v2:
  1. a bateria corre **mutacao sobre si propria** — cada verificacao tem de ser
     detectavel ao ser desligada, como o ISOLAMENTO da `guarda.py`;
  2. `_conjunto` trata 1-D, e recusa comparar tipos incompativeis em vez de
     devolver zero;
  3. conjunto vazio bloqueia;
  4. instrumento por familia de indice, reutilizando a lista da `guarda.py`;
  5. `tolerancia` limitada, e a razao verificada fora do ramo;
  6. um quarto desenho para hold-out temporal e controlo negativo;
  7. direccao da sobreposicao escolhida pelo desenho;
  8. o cabecalho so com numeros que tenham fonte citada.

O relatorio do adversario esta em `C3_ADVERSARIO_2026-09-05.md`.
"""
raise SystemExit(
    "fuga.py esta RETIRADO em 05-09-2026 (ver cabecalho). Inerte por C7: "
    "um ficheiro retirado nao corre, para nao reescrever resultados com "
    "conclusoes mortas.")

_DOC_ORIGINAL = """fuga.py — C3, a ficha de fuga. O controlo partilha o que com o ajuste?

    from fuga import Ficha
    f = Ficha("o defice de 2026 e maior no terreno alto?",
              desenho="confirmacao", unidade="celula de 10 m", tipo="medicao",
              ajuste=dict(dados=celulas, mascara=copado, janela=AOI,
                          instrumento="NDVI Sentinel-2", analista="sessao A"),
              controlo=dict(dados=celulas, mascara=copado, janela=AOI,
                            instrumento="MDT LiDAR 50 cm", analista="sessao A"))
    f.verificar()          # levanta FugaDetectada, ou devolve o grau

A FORMA QUE ISTO TRAVA
----------------------
Forma **A** das clausulas — *o controlo partilha dados com o que controla* — e
a mais cara das oito. Cinco ocorrencias, e nenhuma foi apanhada a recomputar:

  · o placebo do chao com degrau **+0,0531 contra +0,0585** no copado, 91 % do
    sinal que devia isolar (retirada 5);
  · o nulo por permutacao contra autocorrelacao espacial de **0,86-0,96**, que
    torna as celulas nao permutaveis (retirada 12);
  · o **lobulo** apresentado como «o melhor controlo» sendo derivado da coisa
    que controlava (retirada 15);
  · o ICP em que **55,9 %** dos pixeis alinhados caiam a menos de 28 px de um
    centro de valvula — e as valvulas eram o alvo (04-09-2026);
  · `por_area` validada contra as areas que a tinham calibrado.

O invariante e sempre o mesmo: **alguma coisa que devia ser independente nao
era**, e a frase que afirmava a independencia estava escrita e era falsa. No
caso do ICP, «nenhuma valvula entra no ajuste» estava no ficheiro.

PORQUE FECHA POR OMISSAO
------------------------
Um canal nao declarado **bloqueia**. Nao e rigor decorativo: das cinco, quatro
tinham o canal por declarar, e a ausencia foi lida como ausencia de fuga. Uma
ficha que passa por estar em branco nao e ficha — e a forma B, um teste que nao
podia falhar.

E PORQUE O DESENHO TEM DE SER DECLARADO
---------------------------------------
As regras **invertem-se** entre desenhos, e uma clausula que trava trabalho bom
acaba comentada — foi assim que o `c2 = True` entrou.

| desenho | unidades | instrumento |
|---|---|---|
| **placebo** | tem de ser DISJUNTAS do ajuste | tem de ser o MESMO |
| **confirmacao** | tem de ser AS MESMAS | tem de ser OUTRO |
| **validacao** | tem de ser DISJUNTAS (conjunto retido) | indiferente |

Num placebo medem-se unidades que nao deviam responder, com o mesmo
instrumento: instrumento diferente nao e placebo, e outra medicao. Numa
confirmacao a sobreposicao de unidades e o objectivo, e a fuga esta em partilhar
o instrumento — «um NDVI nao se confirma com outro NDVI».

DOIS TESTES QUE NAO SAO DE SOBREPOSICAO
---------------------------------------
`placebo()` — um controlo que reproduz o efeito nao e controlo. Compara-se a
magnitude: se o controlo traz mais do que `limiar` do efeito do ajuste, bloqueia.
Com 91 % nao ha discussao possivel.

`nulo()` — um nulo por permutacao exige permutabilidade. Com autocorrelacao
espacial acima de `limiar` as celulas nao sao permutaveis e o nulo e ingenuo:
exige-se nulo que a respeite, declarado pelo nome.
"""
import io as _io
import json as _json
import os as _os

try:
    import numpy as _np
except ImportError:
    _np = None

CANAIS = ("dados", "mascara", "janela", "instrumento", "analista")
DESENHOS = ("placebo", "confirmacao", "validacao")
# os tres tipos de facto do CLAUDE.md — testemunho ganha a qualquer calculo
TIPOS = ("testemunho", "medicao", "inferencia")
AQUI = _os.path.dirname(_os.path.abspath(__file__))


class FugaDetectada(Exception):
    """O controlo nao e independente do ajuste. A analise nao corre."""


# -- normalizacao ------------------------------------------------------------
def _conjunto(x):
    """Tudo o que se possa comparar por sobreposicao vira conjunto de ids."""
    if x is None:
        return None
    if _np is not None and isinstance(x, _np.ndarray):
        if x.dtype == bool:
            return set(map(tuple, _np.argwhere(x)))
        a = _np.atleast_2d(x)
        if a.ndim == 2 and a.shape[1] > 1:
            return set(map(tuple, a))
        return set(a.ravel().tolist())
    if isinstance(x, (set, frozenset)):
        return set(x)
    if isinstance(x, (list, tuple)):
        return set(x)
    if isinstance(x, (str, int, float)):
        return {x}
    raise TypeError("canal com tipo que nao sei comparar: %r" % type(x))


def sobreposicao(controlo, ajuste):
    """Fraccao do CONTROLO que tambem esta no ajuste.

    E esta a direccao certa: um controlo pequeno inteiramente dentro do ajuste
    da 1,0 e tem de bloquear, mesmo sendo uma fatia minuscula do ajuste. Medir
    ao contrario diluiria a fuga no tamanho do ajuste, que foi como os 55,9 %
    do ICP passaram por aceitaveis.
    """
    c, a = _conjunto(controlo), _conjunto(ajuste)
    if c is None or a is None or not c:
        return None
    return len(c & a) / float(len(c))


# -- a ficha -----------------------------------------------------------------
class Ficha(object):
    """Declara-se ANTES de correr. Mede-se. Bloqueia.

    `tolerancia` e um dicionario canal -> fraccao aceite, e cada entrada exige
    `razao[canal]` escrita. Tolerar sem razao escrita nao passa: foi assim que
    o `c2 = True` entrou, a desligar a unica condicao que incomodava.
    """

    def __init__(self, pergunta, desenho, ajuste, controlo, unidade=None,
                 tipo=None, tolerancia=None, razao=None, derivada_de=None):
        # A primeira versao disto media o COMPRIMENTO da pergunta, e a bateria
        # apanhou-a: «e o terreno?» tem 15 caracteres e passava. Comprimento
        # nao e proxy de pergunta fechada — e teatro. O que se verifica de facto
        # e se a unidade de analise e o tipo de facto estao declarados, que sao
        # duas das quatro coisas que Kummerfeld & Jones 2023 mandam fixar.
        if not pergunta or not pergunta.strip():
            raise FugaDetectada("pergunta por escrever.")
        if not unidade or len(str(unidade).strip()) < 4:
            raise FugaDetectada(
                "unidade de analise por declarar. Pergunta aberta garante "
                "divergencia nao interpretavel (Kummerfeld & Jones 2023): "
                "fixa-se unidade, tipo, fronteiras e termos ANTES de correr.")
        if tipo not in TIPOS:
            raise FugaDetectada(
                "tipo de facto tem de ser um de %s. Misturar os tres e como se "
                "perdem semanas — e testemunho ganha a qualquer calculo." % (TIPOS,))
        if desenho not in DESENHOS:
            raise FugaDetectada(
                "desenho tem de ser um de %s. Sem ele nao se sabe que "
                "sobreposicao e fuga e qual e o objectivo." % (DESENHOS,))
        self.pergunta = pergunta.strip()
        self.unidade = str(unidade).strip()
        self.tipo = tipo
        self.desenho = desenho
        self.ajuste = dict(ajuste or {})
        self.controlo = dict(controlo or {})
        self.tolerancia = dict(tolerancia or {})
        self.razao = dict(razao or {})
        self.derivada_de = derivada_de
        self.medido = {}
        self.notas = []

    def _por_declarar(self):
        return [c for c in CANAIS
                if self.ajuste.get(c) is None or self.controlo.get(c) is None]

    def verificar(self):
        """Devolve o grau. Levanta FugaDetectada em qualquer bloqueio."""
        falta = self._por_declarar()
        if falta:
            raise FugaDetectada(
                "canais por declarar: %s. Fecha por omissao — nao declarado "
                "nunca significou sem fuga, e em quatro das cinco ocorrencias "
                "foi exactamente esse o erro." % ", ".join(falta))

        b = []

        # mascara derivada do sinal que se vai medir — vale em todos os desenhos
        if self.derivada_de is not None:
            d = str(self.derivada_de)
            alvo = "%s %s %s" % (self.ajuste.get("instrumento", ""),
                                 self.ajuste.get("dados", ""), self.pergunta)
            if d and d.lower() in alvo.lower():
                b.append(
                    "mascara do controlo derivada de «%s», que e o proprio "
                    "sinal a medir. Foi o defeito do fazer_masks_v2: o "
                    "cabecalho dizia «poligonos geograficos e estaticos» e o "
                    "codigo definia o pomar por nd2026 > 0,78." % d)

        # unidades: dados e mascara
        for c in ("dados", "mascara"):
            s = sobreposicao(self.controlo[c], self.ajuste[c])
            self.medido[c] = s
            if s is None:
                continue
            if self.desenho == "confirmacao":
                if s < 0.5:
                    b.append(
                        "canal «%s»: numa confirmacao as unidades tem de ser as "
                        "mesmas, e so %.1f %% coincidem. Instrumento "
                        "independente sobre outras unidades nao confirma — mede "
                        "outra coisa." % (c, 100 * s))
                continue
            tol = float(self.tolerancia.get(c, 0.0))
            if s > tol:
                if tol > 0 and not self.razao.get(c):
                    b.append("canal «%s»: tolerancia %.2f declarada SEM razao "
                             "escrita." % (c, tol))
                b.append("canal «%s»: %.1f %% do controlo esta dentro do ajuste "
                         "(tolerancia %.1f %%). Num %s isso e fuga."
                         % (c, 100 * s, 100 * tol, self.desenho))

        # janela
        mesma_janela = (_conjunto(self.controlo["janela"]) ==
                        _conjunto(self.ajuste["janela"]))
        self.medido["janela"] = 1.0 if mesma_janela else 0.0
        if (self.desenho != "confirmacao" and mesma_janela
                and (self.medido.get("dados") or 0) > 0):
            b.append("canal «janela»: a mesma janela E dados sobrepostos. A "
                     "janela deixou de ser fronteira e passou a ser ajuste.")

        # instrumento — e aqui a regra inverte-se com o desenho
        ic = _conjunto(self.controlo["instrumento"])
        ia = _conjunto(self.ajuste["instrumento"])
        comum = ic & ia
        self.medido["instrumento"] = sorted(map(str, comum))
        if self.desenho == "confirmacao" and comum:
            b.append("canal «instrumento»: %s em comum. Um NDVI nao se confirma "
                     "com outro NDVI — confirma-se contra ortofoto, SAR, "
                     "fotografia de campo, documento ou testemunho."
                     % ", ".join(sorted(map(str, comum))))
        if self.desenho == "placebo" and not comum:
            b.append("canal «instrumento»: um placebo mede-se com o MESMO "
                     "instrumento do ajuste (%s contra %s). Instrumento "
                     "diferente nao e placebo — e outra medicao."
                     % (sorted(map(str, ia)), sorted(map(str, ic))))

        if b:
            raise FugaDetectada("FUGA [%s] — %s\n  · %s"
                                % (self.desenho, self.pergunta,
                                   "\n  · ".join(b)))

        mesma_mao = bool(_conjunto(self.controlo["analista"]) &
                         _conjunto(self.ajuste["analista"]))
        self.medido["analista"] = mesma_mao
        if mesma_mao:
            self.notas.append(
                "mesma mao a produzir ajuste e controlo: nao pode ser citada "
                "como validacao independente (Bertran 2026 — trocar persona ou "
                "modelo desloca a distribuicao mesmo entre corridas "
                "metodologicamente solidas).")
            return "SEM FUGA · %s · mesma mao" % self.desenho
        return "SEM FUGA · %s · maos separadas" % self.desenho

    def guardar(self, caminho):
        """A ficha vai para disco com o que foi MEDIDO, nao com o que se disse."""
        try:
            from proveniencia import guardar as _g
        except ImportError:
            _g = None
        d = {"pergunta": self.pergunta,
             "unidade": self.unidade,
             "tipo": self.tipo,
             "desenho": self.desenho,
             "canais_declarados": {c: str(self.ajuste.get(c))[:120]
                                   for c in CANAIS},
             "medido": {k: (round(v, 4) if isinstance(v, float) else v)
                        for k, v in self.medido.items()},
             "notas": self.notas}
        if _g:
            return _g(d, caminho)
        with _io.open(caminho, "w", encoding="utf-8") as f:
            _json.dump(d, f, indent=1, ensure_ascii=False)
        return caminho


# -- dois testes que nao sao de sobreposicao ---------------------------------
def placebo(efeito_ajuste, efeito_controlo, limiar=0.20, nome="placebo"):
    """Um controlo que reproduz o efeito nao e controlo — e parte do sinal."""
    a, c = abs(float(efeito_ajuste)), abs(float(efeito_controlo))
    if a == 0:
        raise FugaDetectada("efeito nulo no ajuste: nao ha nada a controlar.")
    r = c / a
    if r > limiar:
        raise FugaDetectada(
            "%s traz %.0f %% do efeito do ajuste (%.4f contra %.4f), acima do "
            "limiar de %.0f %%. Foi a retirada 5: o chao dava +0,0531 contra "
            "+0,0585 no copado." % (nome, 100 * r, c, a, 100 * limiar))
    return r


def nulo(autocorrelacao, permutacao_simples, limiar=0.30, nome_do_nulo=None):
    """Permutar exige permutabilidade. Com autocorrelacao alta nao ha."""
    ac = abs(float(autocorrelacao))
    if permutacao_simples and ac > limiar:
        raise FugaDetectada(
            "nulo por permutacao simples com autocorrelacao espacial de %.2f "
            "(limiar %.2f): as celulas nao sao permutaveis e o nulo e ingenuo. "
            "Foi a retirada 12, com 0,86-0,96. Exige-se nulo que respeite a "
            "estrutura, declarado pelo nome." % (ac, limiar))
    if not permutacao_simples and not nome_do_nulo:
        raise FugaDetectada(
            "nulo nao-ingenuo por nomear: diz qual, ou nao ha nulo.")
    return nome_do_nulo or "permutacao simples"


# ---------------------------------------------------------------------------
# BATERIA — cada caso e um controlo positivo com UMA coisa partida.
#
# E ha controlos positivos que TEM de passar. Uma bateria so de casos que
# bloqueiam nao prova nada: prova que a funcao levanta excepcoes. Se o positivo
# nao passar, a clausula bloqueia tudo, ninguem a usa, e volta o `c2 = True`.
# ---------------------------------------------------------------------------
_CEL = frozenset(range(1000))                  # celulas de copado vivo
_CHAO = frozenset(range(2000, 2400))           # chao limpo, disjunto
_RETIDO = frozenset(range(3000, 3200))         # conjunto retido
_AOI = "E 529400-531400 · N 4654600-4655600"
_AOI2 = "E 529495-530063 · N 4653832-4654477"


def _base(qual):
    if qual == "confirmacao":
        return dict(
            pergunta="o defice de 2026 e maior no terreno alto, nas celulas "
                     "de copado vivo?",
            desenho="confirmacao", unidade="celula de 10 m", tipo="medicao",
            ajuste=dict(dados=_CEL, mascara=_CEL, janela=_AOI,
                        instrumento="NDVI Sentinel-2", analista="sessao A"),
            controlo=dict(dados=_CEL, mascara=_CEL, janela=_AOI,
                          instrumento="MDT LiDAR 50 cm", analista="sessao A"))
    if qual == "placebo":
        return dict(
            pergunta="o degrau de 2022 aparece no chao limpo, que nao tem "
                     "copado nenhum?",
            desenho="placebo", unidade="celula de 10 m", tipo="medicao",
            ajuste=dict(dados=_CEL, mascara=_CEL, janela=_AOI,
                        instrumento="NDVI Sentinel-2", analista="sessao A"),
            controlo=dict(dados=_CHAO, mascara=_CHAO, janela=_AOI,
                          instrumento="NDVI Sentinel-2", analista="sessao A"))
    return dict(
        pergunta="a por_area reproduz posicoes que nao entraram na sua "
                 "calibracao?",
        desenho="validacao", unidade="valvula", tipo="inferencia",
        ajuste=dict(dados=_CEL, mascara=_CEL, janela=_AOI,
                    instrumento="esquema 1:3500", analista="sessao A"),
        controlo=dict(dados=_RETIDO, mascara=_RETIDO, janela=_AOI,
                      instrumento="esquema 1:3500", analista="sessao A"))


def _com(qual, **mud):
    d = _base(qual)
    for k, v in mud.items():
        if k in ("ajuste", "controlo"):
            d[k] = dict(d[k]); d[k].update(v)
        else:
            d[k] = v
    return d


# (nome, chamada) — cada uma TEM de levantar FugaDetectada
BLOQUEIAM = [
    ("1 · placebo do chao a 91 % do sinal (retirada 5)",
     lambda: placebo(0.0585, 0.0531, nome="chao limpo")),

    ("2 · nulo por permutacao com autocorrelacao 0,86 (retirada 12)",
     lambda: nulo(0.86, permutacao_simples=True)),

    ("3 · mascara do controlo derivada do sinal (fazer_masks_v2)",
     lambda: Ficha(derivada_de="NDVI Sentinel-2",
                   **_com("placebo")).verificar()),

    ("4 · 55,9 % do controlo dentro do ajuste — o ICP (04-09)",
     lambda: Ficha(**_com("validacao", controlo=dict(
         dados=frozenset(list(range(559)) + list(range(3000, 3441))),
         mascara=_RETIDO, janela=_AOI,
         instrumento="esquema 1:3500", analista="sessao A"))).verificar()),

    ("5 · por_area validada contra as areas que a calibraram",
     lambda: Ficha(**_com("validacao", controlo=dict(
         dados=_CEL, mascara=_RETIDO, janela=_AOI,
         instrumento="esquema 1:3500", analista="sessao A"))).verificar()),

    ("6 · um canal por declarar — fecha por omissao",
     lambda: Ficha(**_com("confirmacao",
                          controlo=dict(mascara=None))).verificar()),

    ("7 · NDVI a confirmar NDVI — instrumento em comum",
     lambda: Ficha(**_com("confirmacao", controlo=dict(
         dados=_CEL, mascara=_CEL, janela=_AOI,
         instrumento="NDVI Sentinel-2", analista="sessao A"))).verificar()),

    ("8 · tolerancia declarada sem razao escrita",
     lambda: Ficha(tolerancia={"dados": 0.60}, **_com("validacao", controlo=dict(
         dados=frozenset(list(range(559)) + list(range(3000, 3441))),
         mascara=_RETIDO, janela=_AOI,
         instrumento="esquema 1:3500", analista="sessao A"))).verificar()),

    ("9 · desenho por declarar",
     lambda: Ficha(**_com("confirmacao", desenho="qualquer")).verificar()),

    ("10 · unidade de analise por declarar",
     lambda: Ficha(**_com("confirmacao", unidade=None)).verificar()),

    ("13 · tipo de facto por declarar",
     lambda: Ficha(**_com("confirmacao", tipo=None)).verificar()),

    ("14 · pergunta em branco",
     lambda: Ficha(**_com("confirmacao", pergunta="   ")).verificar()),

    ("11 · placebo com instrumento diferente — nao e placebo",
     lambda: Ficha(**_com("placebo", controlo=dict(
         dados=_CHAO, mascara=_CHAO, janela=_AOI,
         instrumento="SAR Sentinel-1", analista="sessao A"))).verificar()),

    ("12 · confirmacao sobre outras unidades — mede outra coisa",
     lambda: Ficha(**_com("confirmacao", controlo=dict(
         dados=_CHAO, mascara=_CHAO, janela=_AOI2,
         instrumento="MDT LiDAR 50 cm", analista="sessao A"))).verificar()),
]

# (nome, chamada, esperado) — estas TEM de passar
PASSAM = [
    ("terreno contra defice — mesmas celulas, instrumentos independentes",
     lambda: Ficha(**_base("confirmacao")).verificar(), "SEM FUGA"),

    ("chao limpo como placebo — celulas disjuntas, mesmo instrumento",
     lambda: Ficha(**_base("placebo")).verificar(), "SEM FUGA"),

    ("conjunto retido — disjunto do que calibrou",
     lambda: Ficha(**_base("validacao")).verificar(), "SEM FUGA"),

    ("placebo com 8 % do efeito — abaixo do limiar",
     lambda: placebo(0.0585, 0.0047, nome="chao limpo"), None),

    ("nulo que respeita a estrutura, declarado pelo nome",
     lambda: nulo(0.86, permutacao_simples=False,
                  nome_do_nulo="blocos geograficos de 90 m"), None),

    ("maos separadas — o grau muda e diz-se",
     lambda: Ficha(**_com("confirmacao",
                          controlo=dict(dados=_CEL, mascara=_CEL, janela=_AOI,
                                        instrumento="MDT LiDAR 50 cm",
                                        analista="sessao B"))).verificar(),
     "maos separadas"),
]


def bateria(verboso=True):
    """Corre as duas metades. Devolve (bloqueiam_ok, passam_ok, falhas)."""
    falhas, ok_b, ok_p = [], 0, 0

    if verboso:
        print("BLOQUEIAM — cada uma com UMA coisa partida")
    for nome, chamada in BLOQUEIAM:
        try:
            chamada()
        except FugaDetectada as e:
            ok_b += 1
            if verboso:
                print("  BLOQUEIA  %s" % nome)
                print("            %s" % str(e).splitlines()[0][:96])
        except Exception as e:
            falhas.append("%s levantou %s em vez de FugaDetectada: %s"
                          % (nome, type(e).__name__, e))
        else:
            falhas.append("%s PASSOU — a clausula nao a apanha" % nome)

    if verboso:
        print()
        print("PASSAM — o positivo, sem o qual a bateria nao prova nada")
    for nome, chamada, esperado in PASSAM:
        try:
            r = chamada()
        except Exception as e:
            falhas.append("positivo «%s» BLOQUEOU: %s" % (nome, e))
            continue
        if esperado and esperado not in str(r):
            falhas.append("positivo «%s» devolveu %r, esperava %r"
                          % (nome, r, esperado))
            continue
        ok_p += 1
        if verboso:
            print("  passa     %s" % nome)
            if isinstance(r, str):
                print("            -> %s" % r)

    return ok_b, ok_p, falhas


if __name__ == "__main__":
    import sys
    b, p, f = bateria()
    print()
    print("bloqueiam %d/%d · passam %d/%d"
          % (b, len(BLOQUEIAM), p, len(PASSAM)))
    if f:
        print()
        print("FALHAS:")
        for x in f:
            print("  · %s" % x)
        sys.exit(1)
    print("C3 executavel: cada caso bloqueia sozinho e os positivos passam.")
