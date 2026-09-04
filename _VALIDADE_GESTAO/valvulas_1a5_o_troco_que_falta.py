# -*- coding: utf-8 -*-
"""As válvulas 1-5 — o troço da rede que nenhum teste alcançou.

O QUE MOTIVOU ISTO, E É TESTEMUNHO DE TIPO 1
---------------------------------------------
«B1 = válvulas 1-5.» Dito pelo gestor, 03-09-2026. Pela regra dos três tipos de
facto, **entra como dado e ganha a qualquer cálculo nosso**.

E obriga a revisitar uma hipótese que este dossiê dá por **fechada**. A P06
lista, na coluna JÁ FECHADO:

    «Rede de rega sobre-estendida · partição por válvula contra 200 partições
     rodadas da mesma geometria · a válvula não explica nada que a geografia já
     não explique · dentro do nulo 11/11»

A PERGUNTA, e é uma só
----------------------
**O teste que fechou essa hipótese alcançava o troço que a torna
sobre-estendida?**

Não é uma pergunta sobre a estatística — a partição rodada é um bom nulo e não
está em causa. É a pergunta 11 da pré-voo: **a janela contém o que a frase
abrange?**

O QUE SE VERIFICA, e nada disto é recalculado
----------------------------------------------
    F1 · que válvulas entraram em cada uma das quatro reconstruções do esquema
    F2 · o que está registado sobre as válvulas 1 a 5, e com que fundamento
    F3 · se o bloco do **G19** e o sector **B1** são o mesmo objecto
    F4 · o que daqui sai para a hipótese fechada

CRITÉRIO, fixado antes de correr
---------------------------------
    Se as válvulas 1-5 estiverem em **alguma** das quatro reconstruções, a
    hipótese continua fechada e este ficheiro não serve para nada.

    Se não estiverem em **nenhuma**, a hipótese foi fechada por um teste cuja
    janela excluía o troço em causa — e passa de FECHADA a **fechada só para o
    corpo principal**, que é uma coisa diferente e mais fraca.

O QUE ISTO NÃO DECIDE
---------------------
**Não diz que a rega explica o declínio.** Diz que a hipótese não foi testada
onde teria de ser testada. Reabrir não é confirmar, e o custo de reabrir é zero:
volta para a coluna do que falta saber.
"""
import json
import os

VC = r"C:\Users\Jackster2\Downloads\_VALIDACAO_CAMADAS"
G2 = r"C:\Users\Jackster2\Downloads\ganfei_s2"
VG = r"C:\Users\Jackster2\Downloads\_VALIDADE_GESTAO"


def carrega(p):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.load(open(p, encoding=enc))
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise IOError(p)


# ── F1 · que válvulas entraram nas quatro reconstruções
MV = carrega(os.path.join(VC, "SAIDA_C4", "c4_r2_01_multiverso_valvulas.json"))
print("=" * 92)
print("F1 · as quatro reconstrucoes do esquema, e que valvulas cada uma tem")
print("=" * 92)
print()
print("criterio do multiverso: %s" % str(MV.get("criterio"))[:80])
print()
# CORRIGIDO: a primeira versao lia `r["unidades"]` do multiverso e concluia que
# a uniao era «v8, v13+v14». Isso e o que o ficheiro SERIALIZOU — so as unidades
# do contraste — nao o que foi analisado. O `n` de cada reconstrucao diz 12.
# A prova de que as 1-5 estao fora tem de vir dos ficheiros de valvulas.
TODAS = set()
FONTES = ("valvulas_por_area.json", "valvulas_v6.json", "valvulas_v4.json",
          "valvulas_por_linha.json")
for nome, r in MV["reconstrucoes"].items():
    print("  %-26s n=%-3s  (o json guarda so as unidades do contraste: %s)"
          % (nome, r.get("n"), " ".join(sorted(r.get("unidades", {})))))
print()
print("  as valvulas REAIS de cada ficheiro de origem:")
for f in FONTES:
    cam = os.path.join(G2, f)
    if not os.path.exists(cam):
        print("    %-26s (nao existe)" % f)
        continue
    d = carrega(cam)
    ch = d.get("valvulas", d.get("metros_por_linha", d))
    # so contam as chaves que SAO um numero de valvula. `valvulas_v4.json` tem
    # «corpo»/«lobo_oeste» e `valvulas_por_linha.json` tem ancoras de linha —
    # nenhuma delas enumera valvulas, e enfiá-las na uniao dava lixo.
    vs = sorted((str(k).lstrip("v") for k in ch
                 if str(k).lstrip("v").isdigit()), key=int)
    if vs:
        TODAS |= {"v" + v for v in vs}
        print("    %-26s %2d valvulas: %s" % (f, len(vs), " ".join(vs)))
    else:
        print("    %-26s  0 valvulas enumeradas (chaves: %s)"
              % (f, ", ".join(str(k)[:16] for k in list(ch)[:3])[:52]))
falta15 = [v for v in ("v1", "v2", "v3", "v4", "v5") if v not in TODAS]
print()
print("  uniao de todas as reconstrucoes: %s" % " ".join(sorted(
    TODAS, key=lambda k: int(k[1:]) if k[1:].isdigit() else 99)))
print("  valvulas 1 a 5 AUSENTES de todas: %s"
      % (", ".join(falta15) if falta15 else "nenhuma — estao la"))

# ── F2 · o que está registado sobre elas
PL = carrega(os.path.join(G2, "valvulas_por_linha.json"))
nota = PL.get("_valvulas_1a5", "(sem registo)")
print()
print("=" * 92)
print("F2 · o que esta registado sobre as valvulas 1 a 5")
print("=" * 92)
print()
print("  _valvulas_1a5: %s" % nota)
print()
usa_lobo = "lobo" in str(nota).lower() or "lóbulo" in str(nota).lower()
print("  o fundamento invoca «o lobo/lobulo oeste»? %s" % ("SIM" if usa_lobo else "nao"))
if usa_lobo:
    print("  -> e o objecto RETIRADO a 28-08-2026: a AOI `b1` media tecido urbano")
    print("     de Valenca do outro lado do Minho, com 49 ficheiros em quarentena.")
    print("     A razao para nao colocar as valvulas 1-5 assenta num objecto que")
    print("     ja nao existe.")

# ── F3 · o bloco do G19 e o sector B1 são o mesmo objecto?
G19 = (529350, 4653700, 530085, 4654478)          # CAMADA_0_CERTIFICADO, G19
B1 = (529495, 4653832, 530063, 4654477)           # IFAP, medido em 03-09
dentro = (B1[0] >= G19[0] and B1[1] >= G19[1]
          and B1[2] <= G19[2] and B1[3] <= G19[3])
print()
print("=" * 92)
print("F3 · o bloco do G19 e o sector B1 sao o mesmo objecto?")
print("=" * 92)
print()
print("  G19 (C0, por extrapolacao do esquema): E %d..%d  N %d..%d"
      % (G19[0], G19[2], G19[1], G19[3]))
print("  B1  (IFAP, via coordenadas do gestor): E %d..%d  N %d..%d"
      % (B1[0], B1[2], B1[1], B1[3]))
print()
print("  B1 inteiramente dentro da caixa do G19: %s" % dentro)
print("  bordo norte: %d contra %d  ->  %d m de diferenca"
      % (G19[3], B1[3], abs(G19[3] - B1[3])))
print()
print("  duas derivacoes independentes — o esquema de rega extrapolado e os")
print("  poligonos do IFAP — a cairem no mesmo bordo a menos de um metro.")
print()
print("  areas: G19 diz 16,4 ha de bloco · C3 diz 12,64 ha de kiwi · o IFAP")
print("  hoje da 12,63 ha. **O esquema anota 1,77 ha para o mesmo B1** — %.1fx."
      % (12.63 / 1.77))

# ── F4 · o veredicto
print()
print("=" * 92)
print("F4 · o que sai daqui para a hipotese fechada")
print("=" * 92)
print()
if falta15:
    print("  As valvulas 1-5 nao entraram em NENHUMA das quatro reconstrucoes.")
    print("  O teste que fechou «rede sobre-estendida» correu sobre 11 a 12")
    print("  valvulas, todas no corpo principal, dentro da AOI.")
    print()
    print("  >>> A hipotese passa de FECHADA a **fechada so para o corpo")
    print("      principal**. O troco que a torna sobre-estendida — cinco")
    print("      valvulas a servir um sector 500 m a sudoeste, fora da janela —")
    print("      nunca foi testado.")
    ver = "reaberta para o troco oeste; fechada so para o corpo principal"
else:
    print("  As valvulas 1-5 estao nas reconstrucoes. A hipotese continua")
    print("  fechada e este ficheiro nao serve para nada.")
    ver = "mantem-se fechada"
print()
print("  E NAO se conclui que a rega explica o declinio. Conclui-se que a")
print("  hipotese nao foi testada onde teria de ser. Reabrir nao e confirmar.")

json.dump(dict(valvulas_nas_reconstrucoes=sorted(TODAS),
               valvulas_1a5_ausentes=falta15,
               nota_1a5=nota, fundamento_invoca_lobulo=usa_lobo,
               g19=G19, b1=B1, b1_dentro_de_g19=dentro,
               dif_bordo_norte_m=abs(G19[3] - B1[3]),
               area_esquema_ha=1.77, area_ifap_ha=12.63,
               factor=round(12.63 / 1.77, 1), veredicto=ver),
          open(os.path.join(VG, "valvulas_1a5.json"), "w"), indent=1)
print()
print("escrito valvulas_1a5.json")
