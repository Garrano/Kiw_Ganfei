# -*- coding: utf-8 -*-
"""guarda.py — o portão que impede um veredicto de sair sem o que a regra exige.

Porque este ficheiro existe
---------------------------
Em três dias, três conclusões deste caso foram retiradas pela MESMA razão:

  · o «lóbulo oeste B1» — uma AOI que media vegetação urbana, aceite porque a
    pasta se chamava `sentinel_b1`;
  · o **S9** — o B1 como comparador «sem degrau», com zero instrumentos
    independentes, derrubado pelo Controlo 3;
  · o **P3** — «o foco oriental foi replantado», concluído da prominência
    sozinha, derrubado pelo NDVI e pelo perfil radial uma hora depois.

A regra que as três violam está escrita na `CLAUDE.md` do projecto e no
controlo 1 do `CONTROLOS.md`:

  «Nenhum facto entra na secção PASSA PARA CIMA se só foi verificado com o
   mesmo instrumento que o produziu.»

Está escrita, e foi violada três vezes. **Uma regra que só existe em prosa é
uma regra que se cumpre quando dá jeito.** Este ficheiro torna-a executável.

Como se usa
-----------
    from guarda import Facto

    f = Facto("o foco oriental foi replantado",
              instrumento="prominência de pérgola, ortofoto",
              ficheiro="p3_pergola_2010_2012.py")
    f.ancoras(alta=P[REF], baixa=P[NU21], nome_alta="REF", nome_baixa="chão")
    f.confirmar_com("NDVI Sentinel-2", concorda=False)   # <- aqui morre
    print(f.veredicto("ORI-COM foi replantado"))

O `veredicto()` **levanta excepção** se faltar alguma das condições. Não avisa:
impede. Um aviso teria sido ignorado das três vezes.

As quatro condições
-------------------
1. **Instrumento declarado.** Sem isto não há sequer o que auditar.
2. **Instrumento independente**, ou `nao_testavel()` explícito. A regra do
   controlo 1, sem excepção silenciosa.
3. **Âncoras separadas**, quando o facto vem de uma medida com âncoras. Foi o
   que faltou ao P3: em 2021 a referência já não tinha o pico no compasso da
   pérgola, e ninguém verificou antes de concluir.
4. **Reprodução**, quando existe um cálculo certificado do mesmo. Se existe e
   não bate, o veredicto não sai.
"""
import numpy as np


class FactoNaoValidado(Exception):
    """Levantada quando se pede um veredicto sem cumprir as condições."""


class Facto:
    def __init__(self, nome, instrumento=None, ficheiro=None,
                 comparacao_temporal=True):
        # O OMISSIVO INVERTEU-SE a 03-09-2026, por exigencia do Controlo 3.
        # Era False: um facto so era interrogado sobre a identidade da unidade
        # se o analista se lembrasse de ligar a bandeira -- e quem se esquece e
        # exactamente quem precisa dela. Agora todo o facto e temporal ate
        # alguem declarar `instantanea(porque)` e assinar a razao.
        self.nome = nome
        self.instrumento = instrumento
        self.ficheiro = ficheiro
        self.comparacao_temporal = bool(comparacao_temporal)
        self._independentes = []      # [(nome, concorda)]
        self._ancoras = None          # (ok, detalhe)
        self._reproducao = None       # (ok, detalhe)
        self._nao_testavel = None
        self._identidade = None       # (ok, detalhe)
        self._fronteira = None        # (ok, detalhe) — condicao 6
        self._instantanea = None      # razao para dispensar a condicao 5

    # ------------------------------------------------------------------ 2
    def confirmar_com(self, instrumento, concorda=True, nota=""):
        """Regista um instrumento independente e se ele CONCORDA.

        `concorda=False` não é um aviso: é o que impede o veredicto de sair.
        """
        self._independentes.append((instrumento, bool(concorda), nota))
        return self

    def nao_testavel(self, porque):
        """Saída válida e obrigatória quando não há instrumento independente."""
        self._nao_testavel = porque
        return self

    # ------------------------------------------------------------------ 3
    def ancoras(self, alta, baixa, nome_alta="âncora alta", nome_baixa="âncora baixa"):
        """Verifica que o instrumento DISCRIMINA nesta medição.

        Critério: os intervalos interquartis das duas âncoras não se tocam.
        É o teste que o P1 fez para 2025 (e falhou, e por isso não concluiu) e
        que o P3 NÃO fez para 2021 (e por isso concluiu mal).
        """
        a, b = np.asarray(alta, float), np.asarray(baixa, float)
        a, b = a[np.isfinite(a)], b[np.isfinite(b)]
        if a.size < 5 or b.size < 5:
            self._ancoras = (False, "menos de 5 valores numa das âncoras")
            return self
        a25, b75 = np.percentile(a, 25), np.percentile(b, 75)
        ok = bool(a25 > b75)
        self._ancoras = (ok, "%s p25=%.4f contra %s p75=%.4f"
                         % (nome_alta, a25, nome_baixa, b75))
        return self

    # ------------------------------------------------------------- 3-bis
    def escala(self, pico_medido, pico_esperado, tol_m=1.0, unidade="m"):
        """O instrumento está a medir NA ESCALA que se julga?

        Esta é a verificação que faltou ao P3, e a lição mais fina das três
        retiradas. Em 2021 as âncoras SEPARAVAM-SE — o teste `ancoras()` teria
        passado. O que falhou foi outra coisa: **o pico da referência tinha-se
        movido de 5,25 m para 9,88 m**, ou seja a medida já não estava a medir
        o compasso da pérgola em unidade nenhuma.

        Separar não é o mesmo que medir o que se pensa. Uma medida pode
        discriminar duas unidades por uma propriedade que não é a que dá nome
        ao facto.
        """
        d = abs(float(pico_medido) - float(pico_esperado))
        ok = d <= tol_m
        self._ancoras = (ok and (self._ancoras[0] if self._ancoras else True),
                         "pico a %.2f %s contra %.2f esperado (dif %.2f)%s"
                         % (pico_medido, unidade, pico_esperado, d,
                            "" if ok else " — FORA DA ESCALA"))
        return self

    # ------------------------------------------------------------------ 4
    def reproduz(self, meu, certificado, tol=1e-9, nome=""):
        """Compara com um cálculo já certificado do mesmo, célula a célula."""
        m, c = np.asarray(meu, float), np.asarray(certificado, float)
        k = np.isfinite(m) & np.isfinite(c)
        if k.sum() == 0:
            self._reproducao = (False, "nenhuma célula comparável")
            return self
        d = float(np.abs(m[k] - c[k]).max())
        self._reproducao = (d <= tol, "n=%d, |máx dif| = %.2e contra %s"
                            % (int(k.sum()), d, nome or "o certificado"))
        return self

    # ------------------------------------------------------------------ 6
    def fronteira(self, origem, derivada_do_sinal=False, nota=""):
        """De onde vem o CONTORNO da unidade — e foi derivado do que se mede?

        Acrescentado a 03-09-2026. O Controlo 3 notou que nenhuma das cinco
        condicoes anteriores interroga a unidade no ESPACO, e que a regra de
        higiene que a CLAUDE.md deste projecto poe em primeiro lugar --
        «nunca derivar uma mascara do sinal que se vai medir» -- era a unica
        sem condicao no portao.

        Foi o `fazer_masks_v2.py`: o cabecalho dizia «poligonos geograficos e
        estaticos» e o codigo definia `pomar` como `nd2026 > 0,78`, para depois
        medir a evolucao ate 2026. Quatro auditorias passaram por cima.

        `derivada_do_sinal=True` bloqueia o veredicto. Nao ha excepcao: se a
        fronteira saiu do sinal, o facto e circular por construcao.
        """
        self._fronteira = (not derivada_do_sinal,
                           "%s%s" % (origem, (" — " + nota) if nota else ""))
        return self

    def instantanea(self, porque):
        """Declara que o facto NAO compara unidades ao longo do tempo.

        Saida explicita da condicao 5, com a razao assinada. Existe porque o
        omissivo passou a ser «temporal»: esquecer-se agora bloqueia, e
        dispensar-se exige escrever porque.
        """
        self.comparacao_temporal = False
        self._instantanea = porque
        return self

    # ------------------------------------------------------------------ 5
    def identidade_no_tempo(self, instrumento, ok=True, nota=""):
        """A unidade era A MESMA COISA ao longo de todo o intervalo comparado?

        Acrescentado a 01-09-2026, depois da retirada do A3. Cinco blocos de
        kiwi do ENT 297313 apareceram como «duas a quatro vezes piores do que
        Ganfei» em Sentinel-2 e replicaram em Landsat com rho = +0,890 — e
        tinham sido **desmatados em 2024**, com a queda a cair do lado PRE da
        fronteira dos periodos.

        As quatro condicoes anteriores nao apanhavam isto e nao podiam: todas
        interrogam o INSTRUMENTO. **Dois instrumentos independentes concordarem
        nao valida a definicao da unidade.** Quando o facto compara unidades ao
        longo do tempo, alguem tem de ter verificado que a unidade nao mudou de
        natureza no intervalo — por imagem, por documento ou por testemunho.

        REESCRITA A 03-09-2026, e a razao esta no relatorio do Controlo 3.
        --------------------------------------------------------------------
        A primeira versao recebia uma **cadeia de caracteres** e acreditava
        nela. O adversario reconstruiu o A3 retirado, acrescentou-lhe

            g.identidade_no_tempo("declaracao do IFAP, campanha 2026")

        -- uma linha a mais, zero dados a mais -- e **o portao autorizou outra
        vez** o decimo nono veredicto retirado. Com uma «verificacao» que o
        cabecalho de `reg01_landsat.py` explicitamente declara nao ser uma.

        Agora exige-se **prova em disco**: o caminho de um rastreio de
        descontinuidade, e a lista das unidades que o facto usa. Uma unidade
        que o rastreio nao cobre **nao esta verificada** -- e o silencio deixa
        de contar como aprovacao.
        """
        import json as _json
        import os as _os
        import time as _time

        unidades = nota if isinstance(nota, (list, tuple)) else None
        if unidades is None:
            unidades = getattr(self, "_unidades_pedidas", None)

        # 1 · a prova tem de existir em disco
        if not (isinstance(instrumento, str) and _os.path.exists(instrumento)):
            self._identidade = (
                False,
                "«%s» nao e um ficheiro de rastreio. A condicao 5 deixou de "
                "aceitar uma afirmacao: exige o caminho de um rastreio de "
                "descontinuidade. Foi assim que o A3 retirado voltou a passar."
                % str(instrumento)[:70])
            return self

        try:
            R = _json.load(open(instrumento, encoding="utf-8"))
        except Exception as e:
            self._identidade = (False, "rastreio ilegivel (%s)" % type(e).__name__)
            return self

        cobertas = set(R.get("nivel", {}) or R.get("nivel_anual", {}))
        alerta = {a[0] if isinstance(a, (list, tuple)) else a
                  for a in R.get("alerta", [])}
        pedidas = set(unidades or [])

        # 2 · uma unidade que o rastreio nao cobre NAO esta verificada
        fora = pedidas - cobertas
        maus = pedidas & alerta
        idade = (_time.time() - _os.path.getmtime(instrumento)) / 86400.0
        det = ("%s, %d cenas, %d unidades, %.1f dias"
               % (_os.path.basename(instrumento), R.get("n_cenas", 0),
                  len(cobertas), idade))
        if fora:
            self._identidade = (False, "%s — NAO cobre: %s"
                                % (det, ", ".join(sorted(fora))))
        elif maus:
            self._identidade = (False, "%s — com descontinuidade: %s"
                                % (det, ", ".join(sorted(maus))))
        elif not pedidas:
            self._identidade = (False, "%s — nenhuma unidade declarada; a "
                                "condicao 5 precisa de saber o que verificar" % det)
        else:
            self._identidade = (bool(ok), "%s — verificadas: %s"
                                % (det, ", ".join(sorted(pedidas))))
        return self

    # ------------------------------------------------------------------ 1
    def veredicto(self, texto):
        faltas = []
        if not self.instrumento:
            faltas.append("instrumento não declarado")

        concordantes = [i for i in self._independentes if i[1]]
        discordantes = [i for i in self._independentes if not i[1]]
        if discordantes:
            faltas.append("instrumento independente DISCORDA: %s"
                          % "; ".join("%s%s" % (i[0], (" — " + i[2]) if i[2] else "")
                                      for i in discordantes))
        elif not concordantes and not self._nao_testavel:
            faltas.append("sem instrumento independente e sem nao_testavel() "
                          "— controlo 1 do CONTROLOS.md")

        if self._ancoras is not None and not self._ancoras[0]:
            faltas.append("as âncoras não discriminam (%s)" % self._ancoras[1])

        if self._reproducao is not None and not self._reproducao[0]:
            faltas.append("não reproduz o certificado (%s)" % self._reproducao[1])

        if self._fronteira is not None and not self._fronteira[0]:
            faltas.append("a FRONTEIRA da unidade foi derivada do sinal que se "
                          "mede (%s) — e o `fazer_masks_v2.py` outra vez"
                          % self._fronteira[1])

        if self.comparacao_temporal:
            if self._identidade is None:
                faltas.append("compara unidades ao longo do tempo e não declarou "
                              "identidade_no_tempo() — a falha que retirou o A3")
            elif not self._identidade[0]:
                faltas.append("a unidade MUDOU no intervalo comparado (%s)"
                              % self._identidade[1])

        if faltas:
            raise FactoNaoValidado(
                "VEREDICTO BLOQUEADO — «%s»\n  facto: %s\n  ficheiro: %s\n%s"
                % (texto, self.nome, self.ficheiro or "?",
                   "".join("  · %s\n" % f for f in faltas)))

        linhas = ["VEREDICTO: %s" % texto,
                  "  instrumento    : %s" % self.instrumento]
        for nome, _, nota in concordantes:
            linhas.append("  confirmado por : %s%s" % (nome, (" — " + nota) if nota else ""))
        if self._nao_testavel:
            linhas.append("  SEM instrumento independente: %s" % self._nao_testavel)
        if self._ancoras:
            linhas.append("  âncoras        : discriminam (%s)" % self._ancoras[1])
        if self._reproducao:
            linhas.append("  reprodução     : %s" % self._reproducao[1])
        if self._identidade:
            linhas.append("  unidade no tempo: %s" % self._identidade[1])
        if self._instantanea:
            linhas.append("  NAO temporal   : %s" % self._instantanea)
        if self._fronteira:
            linhas.append("  fronteira      : %s" % self._fronteira[1])
        return "\n".join(linhas)


# ══════════════════════════════════════════ auto-teste: apanha os três casos?
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print("=" * 78)
    print("AUTO-TESTE — o portão teria apanhado as três retiradas?")
    print("=" * 78)

    casos = []

    # 1 · S9 — o B1 como comparador, zero instrumentos independentes
    f = Facto("o B1 não tem degrau, logo é comparador",
              instrumento="NDVI Sentinel-2", ficheiro="lobulo_oeste_degrau.py")
    casos.append(("S9 · o B1 como comparador", f, "o B1 é comparador sem degrau"))

    # 2 · P3 — prominência sozinha, e âncoras de 2021 que não discriminam
    f = Facto("o foco oriental foi replantado",
              instrumento="prominência de pérgola, ortofoto 2021",
              ficheiro="p3_pergola_2010_2012.py")
    f.ancoras(alta=rng.normal(0.045, 0.02, 110),      # REF em 2021
              baixa=rng.normal(-0.018, 0.03, 167),    # chão lavrado
              nome_alta="REF", nome_baixa="NU21")
    f.escala(pico_medido=9.88, pico_esperado=5.25, tol_m=1.0)   # a REF em 2021
    casos.append(("P3 · o oriental replantado — SÓ pelo teste de escala",
                  f, "ORI-COM foi replantado"))

    # 2b · o mesmo caso, agora com o instrumento independente a discordar
    f2 = Facto("o foco oriental foi replantado",
               instrumento="prominência de pérgola, ortofoto 2021",
               ficheiro="p3_pergola_2010_2012.py")
    f2.ancoras(alta=rng.normal(0.045, 0.02, 110),
               baixa=rng.normal(-0.018, 0.03, 167),
               nome_alta="REF", nome_baixa="NU21")
    f2.confirmar_com("NDVI Sentinel-2 2013-2024", concorda=False,
                     nota="não há cova; um arranque deixaria uma")
    casos.append(("P3 · o mesmo, pelo instrumento independente",
                  f2, "ORI-COM foi replantado"))

    # 2c · o A3 — dois instrumentos a concordar sobre uma unidade que mudou
    f3 = Facto("os cinco blocos do 297313 tem degrau 2 a 4x maior que Ganfei",
               instrumento="NDVI Sentinel-2, degrau 2025-26 menos 2017-24",
               ficheiro="reg01_landsat.py", comparacao_temporal=True)
    f3.confirmar_com("NDVI Landsat 8/9, 100 cenas, outra agencia", concorda=True,
                     nota="os mesmos cinco no fundo, Spearman rho = +0,890")
    f3.confirmar_com("NDMI Landsat, outra banda", concorda=True)
    casos.append(("A3 · dois instrumentos independentes, unidade nao verificada",
                  f3, "ha blocos vizinhos muito piores"))

    # 2d · a reconstrucao do Controlo 3: o A3 com uma STRING como identidade
    f4 = Facto("os cinco blocos do 297313 tem degrau 2 a 4x maior que Ganfei",
               instrumento="NDVI Sentinel-2, degrau 2025-26 menos 2017-24",
               ficheiro="reg01_landsat.py")
    f4.confirmar_com("NDVI Landsat 8/9, 100 cenas", concorda=True)
    f4.identidade_no_tempo("declaracao do IFAP, campanha 2026")
    casos.append(("A3 · a reconstrucao do Controlo 3, com uma string por prova",
                  f4, "ha blocos vizinhos muito piores"))

    # 2e · a mascara derivada do sinal — o fazer_masks_v2.py
    f5 = Facto("o pomar perdeu vigor entre 2017 e 2026",
               instrumento="NDVI Sentinel-2", ficheiro="fazer_masks_v2.py")
    f5.confirmar_com("ortofoto", concorda=True)
    f5.instantanea("nao aplicavel a este teste")
    f5.fronteira("pomar := nd2026 > 0,78", derivada_do_sinal=True)
    casos.append(("fazer_masks_v2 · mascara derivada do sinal que se mede",
                  f5, "o pomar perdeu vigor"))

    # 3 · o lóbulo B1 original — AOI aceite pelo nome da pasta
    f = Facto("o lóbulo oeste é um bloco de controlo são",
              instrumento="NDVI Sentinel-2 sobre sentinel_b1/",
              ficheiro="b1_serie.py")
    casos.append(("B1 original · a AOI do outro lado do rio",
                  f, "o B1 é um controlo são"))

    for titulo, f, texto in casos:
        print()
        print("--- %s" % titulo)
        try:
            print(f.veredicto(texto))
            print("  *** PASSOU — o portão NÃO apanhou este caso ***")
        except FactoNaoValidado as e:
            print(str(e).rstrip())

    # 4 · e deixa passar o que é bom: 2012, com tudo cumprido
    print()
    print("--- controlo positivo · a pérgola do ORI-COM em 2012")
    P = rng.normal(0.17, 0.05, 76)
    f = (Facto("ORI-COM tinha pérgola em 2012",
               instrumento="prominência de pérgola, ortofoto 2012",
               ficheiro="p3_pergola_2010_2012.py")
         .ancoras(alta=rng.normal(0.220, 0.02, 110),
                  baixa=rng.normal(-0.017, 0.015, 167),
                  nome_alta="REF", nome_baixa="NU21")
         .instantanea("prominencia medida DENTRO de uma imagem de 2012")
         .fronteira("mascara geografica da C2, anterior ao calculo")
         .reproduz(P, P, nome="c2_12_prom_2012.npy")
         .confirmar_com("mapa certificado da C2", concorda=True,
                        nota="máx dif 0,00e+00 em 2 858 células"))
    try:
        print(f.veredicto("ORI-COM tinha pérgola madura em 2012"))
    except FactoNaoValidado as e:
        print(str(e).rstrip())
        print("  *** BLOQUEOU um facto bom — o portão é apertado de mais ***")
