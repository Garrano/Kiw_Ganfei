# SAR — a leitura. O radar não decide, e sabe-se porquê e com que limite.

**06-09-2026.** Lido contra `CRITERIO_SAR_v3.md` + `CRITERIO_SAR_v3_ADENDA.md`,
autorizado por adversário independente antes da corrida (AUD-14).
Produzido por `sar_v3.py` → `sar_v3.json`.

**Estatuto: NÃO TESTÁVEL, por falta de potência. Autorizado pelo portão nessa
forma, e só nessa.** Falta a auditoria independente do resultado — até lá,
não citável.

---

## 1 · As doze células. Nenhuma distingue.

Contraste `zona0 − comparador`, VV, S1A, Nov-Fev, ano hidrológico a 1 de
Setembro. Δ = ano de tratamento menos média dos anos de base.

**Base n = 10** (com o meio-inverno de 2015-16):

| comparador | órb | Δ | MDE | distingue |
|---|---|---|---|---|
| `resto` | 125 | **−0,771** | 1,24 | não |
| `resto` | 147 | −0,133 | 1,61 | não |
| `resto` | média | −0,452 | 1,26 | não |
| `referencia` | 125 | **−0,518** | 0,99 | não |
| `referencia` | 147 | **+0,097** | 1,58 | não |
| `referencia` | média | −0,211 | 1,12 | não |

**Base n = 9** (sem o meio-inverno): Δ de −0,761 a +0,178, MDE de 0,99 a 1,52.
**Nenhuma célula distingue em nenhuma das duas bases.**

Pela regra de veredicto da adenda §1, a frase é:

> **Em todas as doze células o deslocamento fica abaixo da resolução deste
> instrumento nesta unidade.**

E **não** «não houve acontecimento». O posto não vai publicado em nenhuma
célula, porque a adenda §1 proíbe acompanhar um Δ abaixo do MDE com ele.

**As órbitas discordam em sinal** no comparador `referencia`: −0,518 na 125 e
+0,097 na 147. Publica-se sem síntese, que é o que o §1 manda.

## 2 · O rótulo de modo comum **disparou**, e é o achado que governa a leitura

| órbita | anomalia `referencia` | anomalia `resto` | **comum** | |
|---|---|---|---|---|
| 125 | +0,638 | +0,891 | **+0,764** | dispara |
| 147 | +0,659 | +0,889 | **+0,774** | dispara |

Limiar 0,5 dB. **O pomar inteiro subiu cerca de 0,77 dB no inverno de
2025-26** — as duas unidades de controlo, nas duas órbitas, na mesma direcção e
na mesma ordem de grandeza.

> **O resultado está rotulado «modo comum não separável» e não se lê como
> acontecimento na `zona0`.** O que este inverno tem de diferente é do ano, não
> da unidade — e o inverno é o **2.º mais chuvoso dos onze**.

O portão de abortar **passou** (+0,253 / +0,230 contra MDE de 0,53 / 0,41), o
que significa que o *contraste* de controlo se aguenta. É o **nível** que se
moveu, nas três unidades juntas. As duas coisas são compatíveis e é por isso que
o critério exigia as duas.

## 3 · E o instrumento não tinha potência para a pergunta

Isto vale independentemente do resultado, e estava escrito antes:

| | |
|---|---|
| MDE desta unidade | **0,99 a 1,61 dB** |
| tecto físico do sinal de copado, 2015-24 | +1,02 (orb125) · +2,05 (orb147) |
| tecto no período em que o `nu2021` **é mesmo** chão nu (2021-24) | **+0,72** (orb125) · +1,57 (147) |

**Na órbita 125 o MDE excede o tecto.** Ou seja: mesmo a perda **total** do
copado na `zona0` seria indistinguível de zero nessa órbita. Um resultado nulo
aqui não é informação sobre o pomar — é informação sobre o instrumento.

A causa é a unidade: a `zona0` tem 202 células e o seu contraste é 2 a 4× mais
ruidoso que o do controlo. *(O mecanismo que dei ao §0 do v3 — contagem de
células — está errado e registado como IX-10: a `referencia` tem 110 células,
menos, e é o contraste menos ruidoso. A causa verdadeira fica por estabelecer.)*

## 4 · O portão

```
A · «o radar nao distingue», como veredicto positivo   -> BLOQUEADO
      · sem instrumento independente e sem nao_testavel()
B · o mesmo, NAO TESTAVEL com a razao de potencia escrita  -> AUTORIZADO
```

O portão está certo nas duas. Um nulo sem potência declarada não é veredicto.

**E a condição 2 continua aberta.** Este era o instrumento que a devia fechar, e
não a fecha — não por os dados faltarem, mas por a unidade ser pequena de mais
para o ruído do radar. Fica NÃO TESTÁVEL **com limite superior medido**, que é
diferente e melhor do que NÃO TESTÁVEL por ausência de instrumento.

## 5 · O que isto NÃO diz

- **não contradiz o óptico.** O NDVI mede um contraste que caiu 0,16 (≈ 5,7 σ
  na sua própria escala); o SAR diz que, na sua escala, o deslocamento fica
  abaixo de 1 dB. **Dois instrumentos com sensibilidades diferentes, e nenhum
  conflito** — o radar simplesmente não chega lá;
- **não fecha declínio contra arranque.** O P3 continua por correr;
- **não testa o encharcamento.** O P4 continua por correr — e o §2 acabou de o
  tornar mais interessante, não menos: o inverno é o 2.º mais chuvoso dos onze e
  o pomar inteiro subiu 0,77 dB, que é o que a chuva faz;
- **não estima magnitude ocidental.**

## 6 · O que se ganhou, e é real

1. **Um limite superior medido** onde antes havia ausência de instrumento.
2. **A subida de modo comum de 0,77 dB**, que nenhuma leitura anterior tinha
   visto porque nenhuma publicava níveis absolutos — e que é evidência directa
   para o P4.
3. **A série de ano inteiro, 1613 cenas de 2016 a 2026 em potência linear**, que
   não existia e que serve o P3 e o P4 sem descarregar mais nada.
4. **A previsão do v1 §8 cumpriu-se textualmente:** *«se não for, o facto
   continua NÃO TESTÁVEL — mas passa a sê-lo com um limite superior medido em
   vez de por ausência de instrumento.»*

## 7 · O que falta antes de isto ser citável

**A auditoria independente do resultado.** Pela C10, certificação e adversário,
não uma ou outra. O portão está feito; o adversário está por fazer, e até lá
esta página não entra em relatório nenhum.
