# PRÉ-REGISTO — as 49 cenas do vão. Quantos acontecimentos, e quando?

**Escrito a 05-09-2026, ANTES de descarregar ou correr coisa nenhuma.**
Substitui o desenho do `p2_onze_cenas.py`, corrigido pelo Controlo 4.

> **Este documento vai a um adversário independente antes da corrida.** É a
> cláusula C9, que estava em prosa e nunca tinha sido cumprida — e é a que teria
> apanhado o `p2` numa leitura da linha 76.

---

## 1 · A pergunta, fixada

**Unidade de análise:** célula de 10 m, agregada por mediana em três unidades
geográficas fixas.
**Tipo de facto:** medição.
**Fronteiras temporais:** 2025-06-01 a 2026-07-31, sem filtro de dia-do-ano.
**Termos:** *acontecimento* = uma transição sustentada no contraste
foco-menos-controlo, isto é, um deslocamento que persiste em pelo menos duas
datas consecutivas seguintes e não regressa ao nível anterior.

**Pergunta:** dentro deste intervalo, **quantas transições sustentadas há no
contraste, e entre que pares de datas cai cada uma?**

## 2 · As unidades, e são as certificadas

| | definição | origem |
|---|---|---|
| OCIDENTAL | disco de 90 m em (530485, 4655053) ∩ pomar ∩ COM | R2 G34 |
| ORIENTAL | polígono `zona0` ∩ COM | ortofoto DGT |
| CONTROLO | pomar ∩ COM, a > 90 m dos dois focos, menos `zona0` e menos REF | idem |

`COM = chm_altura ≥ 0,5` — **e é aqui que está a maior fraqueza deste desenho,
declarada à cabeça:** vem de um voo LiDAR de **2025-07-06**, que cai dentro da
janela. «Ter pérgola» é estado pós-tratamento e é a maior condição aberta do
processo (`ENCERRAMENTO` §6). Isto não se resolve aqui. **Consequência aceite:
as unidades são as de Julho de 2025, e o resultado descreve o que aconteceu a
essas unidades, não a unidades definidas antes do acontecimento.**

## 3 · O que se mede

**Contraste foco-menos-controlo**, a grandeza que a R3 certificou — não o nível
absoluto. Um desvio comum às unidades cancela-se em primeira ordem: plataforma,
calibração, e a maior parte da fenologia.

**E o nível absoluto de cada unidade vai impresso ao lado**, para o leitor ver a
fenologia que o contraste está a cancelar. O `p2` não o fez e por isso o seu
«patamar» de 2026 passou por patamar.

## 4 · Máscara de nuvem — a correcção que o Controlo 4 obriga

O `p2` não mascarou nuvem por píxel, e a correlação entre fracção de nuvem e
contraste ficou em **+0,86** (Ago-2025) e **+0,99** (Jul-2026): mais nuvem,
contraste menos negativo. Artefacto do instrumento sobre a própria grandeza.

Aqui: **máscara SCL por píxel** (excluir 3 sombra, 8/9 nuvem, 10 cirrus, 11
neve), e uma cena só entra se **cada uma das três unidades tiver ≥ 60 % de
píxeis válidos**. A fracção válida por unidade vai no ficheiro.

**Verificação obrigatória a seguir à corrida:** recalcular a correlação entre
fracção de nuvem e contraste. **Se |r| > 0,4, o resultado não se interpreta** —
a máscara não fez o trabalho.

## 5 · A tabela de decisão — quatro ramos, e o quarto é o que faltava

| ramos | selecciona-se se |
|---|---|
| **UM acontecimento** | há exactamente **uma** transição sustentada em todo o intervalo |
| **DOIS ou mais** | há **duas ou mais** transições sustentadas, separadas por um patamar de ≥ 3 datas sem deslocamento |
| **NÃO É DEGRAU** | o contraste desce de forma monótona sem patamar identificável — declive significativo e nenhuma transição isolável |
| **NÃO DECIDE** | a maior lacuna entre datas consecutivas retidas excede **60 dias**, ou a máscara falha o teste do §4, ou menos de 30 datas sobrevivem |

O quarto ramo é a saída que o `p2` não tinha. **Um pré-registo sem saída de «não
decide» obriga a escolher entre três respostas quando a resposta pode ser
nenhuma.**

## 6 · SEVERIDADE — calculada ANTES, e é isto que o `p2` não fez

A cláusula C1 diz que nenhum critério conta sem a probabilidade de falhar sob
uma perturbação do tamanho que interessa. Medido no inventário, antes de
descarregar:

```
cenas limpas (<20 % nuvem) dentro do vão 2025-09-01..2026-06-30 : 49
    -> datas únicas                                             : 40
datas únicas limpas em todo o intervalo do estudo               : 48
maior intervalo entre datas consecutivas                        : 55 dias
mediana dos intervalos                                          : 3 dias
```

**Cada ramo é alcançável, e diz-se com que resolução:**

- uma transição fica localizada entre duas datas consecutivas — **3 dias na
  mediana, 55 dias no pior caso** (o buraco de Janeiro de 2026);
- «dois acontecimentos» exige um patamar de ≥ 3 datas entre transições: com
  mediana de 3 dias entre datas, um patamar de duas semanas é detectável;
- **o ramo «não decide» dispara sozinho a 60 dias**, e a maior lacuna medida é
  55 — ou seja, o desenho passa por **cinco dias de margem**. Isto é uma
  advertência, não um conforto: se a máscara de nuvem eliminar as duas cenas
  certas de Dezembro ou Fevereiro, a lacuna passa dos 60 e o resultado é «não
  decide». **Está pré-registado que nesse caso não se interpreta.**

Comparação com o desenho que isto substitui: no `p2`, a maior lacuna era de
**310 dias** e nenhum dos três ramos era alcançável por construção. A
probabilidade de o critério falhar era **zero**.

## 7 · Ameaça principal, e o que se faz com ela

**A fenologia não cancela por inteiro.** O contraste cancela o que é comum às
unidades; uma unidade em declínio pode abrolhar e cair de folha de maneira
diferente do controlo. Num intervalo que atravessa o Inverno, com o kiwi sem
folha, isto é grande.

Pré-registado: **uma transição só conta se o contraste se deslocar E o controlo
não se deslocar correspondentemente**. O nível absoluto do controlo vai impresso
em todas as datas, e qualquer transição em que o controlo se mova na mesma
direcção e ordem de grandeza é marcada **«fenológica, não interpretável»** — não
é contada como acontecimento.

Consequência aceite: transições no Inverno profundo podem ficar por classificar,
e isso vai dito em vez de resolvido.

## 8 · O que este desenho NÃO responde

- **não diz a causa.** Nenhuma;
- **não estabelece a natureza da unidade oriental** — declínio contra arranque
  continua aberto, e é anterior a isto;
- **não é instrumento independente.** Continua a ser NDVI Sentinel-2. Sai como
  **NÃO TESTÁVEL** no portão, tal como o `p2`, por muito bem que corra. O que
  muda não é o estatuto — é que passa a haver uma **datação** em vez de uma
  interpolação sobre 310 dias.

## 9 · Ficheiros

`p8_vao.py` produz `p8_vao.json`, com carimbo de produtor (S2). Nenhum ficheiro
existente é alterado.
