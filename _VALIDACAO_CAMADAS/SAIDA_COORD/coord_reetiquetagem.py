# -*- coding: utf-8 -*-
"""Re-derivacao a serio do estatuto das 59 causas — trabalho de coordenacao.

PORQUE EXISTE, E PORQUE NAO E TRABALHO DA CAMADA
------------------------------------------------
O adversario da C5 acusou a `c5_01_reetiquetagem.py` de descrever no cabecalho
uma arvore que le os campos de evidencia e de, no codigo, nao ler nenhum deles.
**Verifiquei e e verdade.** O CSV de entrada da C4 tem as colunas

    ambito · prova (certificado e numero) · instrumento independente ·
    margem e leitura · o que a fecharia

e o codigo da C5 le `id`, `classe`, `causa`, `estatuto` e depois chaves que sao
as suas proprias colunas de SAIDA — ou seja, um dicionario escrito a mao. E o
CSV que ela produz **deita fora as cinco colunas de evidencia**: o rasto de
prova corta-se na ultima camada, que e onde sai para o mundo.

E a estrutura exacta do `fazer_masks_v2.py`, o erro que deu origem a esta
cadeia inteira.

A C5 foi mandada refazer e nao pode: bateu no limite de sessao. **Isto e
trabalho do coordenador a substitui-la, e fica marcado como tal** — nao entra
em nenhuma lista fechada e nao substitui o certificado dela. Serve para
responder a uma pergunta: **quantas das 59 etiquetas mudam quando a derivacao e
real em vez de escrita a mao?**

O METODO
--------
Regras explicitas sobre os campos de evidencia, na ordem em que sao testadas.
**Cada linha do resultado cita o campo e o excerto que disparou a regra.** As
regras sairam de um levantamento previo dos padroes que existem mesmo no texto
— nao de suposicao.

Onde o texto nao determina, o resultado e **NAO DERIVAVEL DO TEXTO**, e isso e
resultado, nao falha: significa que a etiqueta da C5 naquela linha e juizo puro
e tem de o declarar.

A arvore e a que a propria C5 declarou no seu cabecalho:

  ensaio em Ganfei? nao ................. NUNCA PROCURADA
  so em Espanha (240/2023, rejeitado) ... SO FORA DE GANFEI
  positivo, um ponto, sem par ........... ENCONTRADA SEM PAR
  positivo em todas as unidades ......... ENCONTRADA SEM NIVEL NORMAL
  o desenho nao podia rejeitar .......... MEDIDA SEM PODER
"""
import csv
import io
import os
import re
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
C4 = os.path.join(BASE, "SAIDA_C4", "c4_razao_exclusoes.csv")
C5 = os.path.join(BASE, "SAIDA_C5", "c5_reetiquetagem.csv")

ev = list(csv.DictReader(io.open(C4, encoding="utf-8-sig"), delimiter=";"))
c5 = {x["id"]: x for x in
      csv.DictReader(io.open(C5, encoding="utf-8-sig"), delimiter=";")}
print("linhas no livro-razao da C4: %d" % len(ev))
print("linhas na re-etiquetagem da C5: %d\n" % len(c5))

A, M, I = "ambito", "margem e leitura", "instrumento independente"


def norm(s):
    return " ".join((s or "").split())


def derivar(r):
    """Devolve (estatuto, regra, campo, excerto). Primeira regra que dispara."""
    a, m, i = norm(r[A]), norm(r[M]), norm(r[I])

    # R1 · nao houve ensaio em Ganfei — o ambito di-lo literalmente
    mo = re.search(r"nenhum ponto[^;.]*", a, re.I)
    if mo:
        return "NUNCA PROCURADA", "R1", A, mo.group(0)[:120]

    # R2 · houve ensaio, mas so em Espanha, e esse material esta rejeitado
    mo = re.search(r"(em Espanha[^;.]*|240/2023[^;.]*|Ribadumia[^;.]*)", m + " " + a, re.I)
    if mo:
        return "SO FORA DE GANFEI", "R2", M, mo.group(0)[:120]

    # R3 · positivo em todas as unidades colocadas — falta o nivel normal
    mo = re.search(r"(em todas as unidades[^;.]*|\d+/\d+ unidades[^;.]*)", m, re.I)
    if mo:
        return "ENCONTRADA SEM NIVEL NORMAL", "R3", M, mo.group(0)[:120]

    # R4 · positivo, um ponto, sem par de comparacao
    if re.search(r"\bPOSITIVO\b", m):
        mo = re.search(r"(SEM PAR[^;.]*|unica amostra composta[^;.]*|sem replicado[^;.]*)", m, re.I)
        if mo:
            return "ENCONTRADA SEM PAR", "R4", M, mo.group(0)[:120]
        return "ENCONTRADA, PAR POR VERIFICAR", "R4b", M, m[:120]

    # R5 · negativo cuja sensibilidade o proprio campo poe em causa
    if re.search(r"\bNEGATIVO\b", m):
        mo = re.search(r"(composta[^;.]*|n\s*=\s*\d+[^;.]*|Sensibilidade[^;.]*|"
                       r"NAO cobre[^;.]*)", m, re.I)
        if mo:
            return "MEDIDA SEM PODER", "R5", M, mo.group(0)[:120]
        return "NEGATIVO COM PODER POR DECLARAR", "R5b", M, m[:120]

    # R6 · tem instrumento independente declarado — sustenta ou exclui
    if re.match(r"\s*SIM\b", i):
        return "COM INSTRUMENTO INDEPENDENTE", "R6", I, i[:120]

    return "NAO DERIVAVEL DO TEXTO", "—", "", (a or m or i)[:120]


linhas, dif = [], []
for r in ev:
    est, regra, campo, exc = derivar(r)
    c = c5.get(r["id"], {})
    c5e = norm(c.get("estatuto_C5", "(ausente)"))
    linhas.append(dict(id=r["id"], classe=r["classe"], causa=norm(r["causa"])[:70],
                       estatuto_C4=r["estatuto"], derivado=est, regra=regra,
                       campo=campo, excerto=exc, estatuto_C5=c5e,
                       prova=norm(r["prova (certificado e numero)"])[:120],
                       instrumento=norm(r[I])[:120]))
    if est.split()[0] != c5e.split()[0] if c5e else True:
        dif.append(linhas[-1])

print("DERIVACAO A PARTIR DOS CAMPOS DE EVIDENCIA\n")
print("%-8s %-30s %-30s %s" % ("id", "derivado do texto", "escrito pela C5", "regra"))
for L in linhas:
    marca = "  <<<" if L in dif else ""
    print("%-8s %-30s %-30s %-4s%s"
          % (L["id"], L["derivado"][:29], L["estatuto_C5"][:29], L["regra"], marca))

print("\nRESUMO")
print("  derivado do texto  :", dict(Counter(L["derivado"] for L in linhas)))
print("  escrito pela C5    :", dict(Counter(L["estatuto_C5"] for L in linhas)))
nd = sum(1 for L in linhas if L["derivado"] == "NAO DERIVAVEL DO TEXTO")
print("\n  linhas em que a derivacao e a etiqueta da C5 divergem: %d de %d"
      % (len(dif), len(linhas)))
print("  linhas que o texto NAO determina: %d — nessas a etiqueta e juizo puro"
      % nd)

campos = ["id", "classe", "causa", "estatuto_C4", "estatuto_C5", "derivado",
          "regra", "campo", "excerto", "prova", "instrumento"]
with io.open(os.path.join(AQUI, "coord_reetiquetagem.csv"), "w",
             encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=campos, delimiter=";")
    w.writeheader()
    for L in linhas:
        w.writerow({k: L[k] for k in campos})
print("\nescrito coord_reetiquetagem.csv — COM as colunas de prova e de "
      "instrumento, que a C5 tinha deitado fora")
