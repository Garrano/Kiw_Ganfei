# ADENDA ao CRITÉRIO v3 — as quatro que o adversário exigiu, e nada mais

**06-09-2026, antes de ler.** O adversário deu o v3 por **substancialmente
melhor do que os três anteriores**, mandou **não** reescrever, e prescreveu
quatro linhas. Escritas estas, autorizou a leitura.

Cada uma abaixo é dele. Onde acrescento, digo que acrescento.

---

## 1 · A regra de veredicto — que o §4 tinha apagado sem substituir

O §4 tornou «Δ contra o MDE» primária e **apagou a tabela da v2 sem pôr outra**.
Volta, aplicada a **cada uma das seis células** (dois comparadores × três
tratamentos de órbita):

| | frase que se segue |
|---|---|
| **\|Δ\| ≥ MDE** | *«nesta célula o radar distingue o ano de tratamento dos dez anteriores»* |
| **\|Δ\| < MDE** | *«nesta célula o deslocamento fica abaixo da resolução deste instrumento nesta unidade»* — **e não «não houve acontecimento»** |

**Órbitas em desacordo:** publicam-se as três, sem síntese. Uma célula que
distingue e outra que não é **o resultado**, e escreve-se assim.

**Proibição explícita**, e é a que o adversário pediu por ser a porta que ficava
aberta: **um Δ abaixo do MDE não pode ser acompanhado da frase do posto.** Nem
«é o mais extremo dos onze», nem nenhuma variante. Abaixo do MDE, a única frase
permitida é a da linha 2.

## 2 · A fórmula do MDE, numa linha — e o MDE do controlo só na base

```
MDE = ( t(0,975 ; n-2) + t(0,80 ; n-2) ) · sd · sqrt(1 + 1/(n-1))
```

α = 0,05 **bilateral**, potência 80 %, `sd` = desvio entre médias anuais dos
**anos de base**, `n` = número desses anos. Mesma fórmula e mesmo `n` para as
seis células **e para o controlo**.

**Correcção que o adversário apanhou e verifiquei:** o MDE do portão de abortar
que publiquei — **0,55 / 0,44** — tinha o ano de tratamento **dentro do seu
próprio nulo**. Recomputado só na base:

| controlo `resto − referencia` | com 2025-26 dentro | **só base** |
|---|---|---|
| orb 125 | 0,55 | **0,53** |
| orb 147 | 0,44 | **0,41** |
| média das órbitas | *(não existia)* | **0,44** |

A terceira linha é a que faltava: **o §3 mandava publicar a série da média e o
portão não tinha limiar para ela.** Era a forma exacta do bloqueante (a) da v2,
dentro do elemento retomado para o corrigir.

## 3 · A estatística do modo comum — unidades, série, estatística, e o que faz

O v3 nomeava as unidades e não a estatística. E acrescentava a `zona0` — a
unidade **sob teste** — a um critério destinado a detectar deslocamento comum,
o que o move na direcção da forma A. **Volta como estava na v2:**

- **unidades: duas**, `referencia` e `resto`. **A `zona0` sai.**
- **série:** nível absoluto em dB, VV, Nov-Fev, S1A, por órbita.
- **estatística:** anomalia de cada unidade = média do ano de tratamento menos
  média dos anos de base. O **deslocamento comum** é a **média das duas
  anomalias**, calculada em cada órbita em separado.
- **limiar: ≥ 0,5 dB** — é da v2 §8.5, mantido, e assinalo que **é asserido**:
  não tem medição atrás e o adversário tem razão em o dizer.
- **o que faz quando dispara:** o resultado é rotulado **«modo comum não
  separável»**, publica-se com esse rótulo, e **não se lê como acontecimento na
  `zona0`**. Não anula a leitura — qualifica-a.

## 4 · A base e a plataforma

**Plataforma: o acerto é `.upper()`.** Verificado, e é armadilha silenciosa:

```
plataforma == 'SENTINEL-1A'          -> ano de tratamento:  0 cenas de inverno
plataforma.upper() == 'SENTINEL-1A'  -> ano de tratamento: 19 cenas de inverno
```

O campo vem `SENTINEL-1A` na base e `sentinel-1a` no ano de tratamento. Um
guião escrito ingenuamente a partir do v3 **esvaziava o ano de tratamento sem
dar erro nenhum**.

**Base: publicam-se as duas.** O meio-inverno de 2015-16 (10 cenas, sem Nov nem
Dez) move os MDE até 10 %, e o adversário mediu que numa célula isso atravessa o
tecto de copado. Não escolho: **corre com n = 10 e com n = 9, e publicam-se as
duas**, que é a cláusula C5. Se a frase do §0 mudar entre elas, isso é o
resultado.

---

## 5 · O que fica por corrigir, e vai na redacção do resultado

O adversário classificou estes como «de honestidade da redacção, não da
leitura». Ficam escritos aqui para não se perderem:

- **O mecanismo do §0 está errado.** Eu escrevi «202 células contra 2411». Mas a
  `referencia` tem **110** células — menos que as 202 da `zona0` — e mesmo assim
  `zona0 − referencia` é o contraste **menos** ruidoso. **Não é contagem de
  células.** O achado do §0 mantém-se inteiro; a explicação que lhe dei não.
- **O tecto de copado está contaminado.** O `nu2021` só é chão nu **depois de
  2021**. Partido por período: **+1,19 / +2,25 dB (2015-20)** contra
  **+0,72 / +1,57 (2021-24)**. No período correcto, **o MDE excede o tecto em
  35 a 70 % na órbita 125** — a frase honesta não é «no limite do detectável», é
  que nesta unidade e nesta órbita **a perda total do copado é indistinguível de
  zero**.
- **Os 332,7 mm não reconciliam** — são 352,3 (todas as plataformas) ou 339,4
  (S1A). O «2.º mais chuvoso dos onze» reproduz-se.
- **O P3 na forma barata não é barato em potência.** MDE do VH: 1,49–1,55 dB na
  órbita 125 contra o sinal estrutural de +1,4 a +2,3 que o §8 invoca. É
  marginal, e o §8 dizia «zero dados adicionais» sem dizer isto.
- **O §8 é promessa sem critério** — sem data, sem hipótese pré-registada, sem
  definição de «publicar». É prosa, e a C10 já mediu o que a prosa vale aqui.
- **IX-02 está mal diagnosticado.** A causa que lá escrevi — convenção de ano —
  está errada: para Nov-Fev as duas convenções dão a **mesma partição**, dígito
  a dígito. A diferença 0,168/0,157 é **11 anos contra 10**. Corrigido no
  registo.
- **A garantia do §0 do v3 não tem verificador.** «As sete alterações» só
  existem no cartucho do documento que elas refutaram; a lista é reconstrução
  minha. Seis das sete reconstroem-se sem esforço, mas a garantia é
  inauditável, e é justo que fique dito.

## 6 · E o que o portão continua a não ver

- **autoriza SAR confirmado por SAR** — e é pior do que eu escrevi: não é que a
  lista de índices seja óptica, é que **a ausência de acerto desliga a
  verificação** em vez de bloquear;
- **não vê potência.** Nada nele compara Δ com um MDE, nem vê que o MDE excede o
  tecto físico. Um Δ abaixo do MDE relatado como «o mais extremo dos onze»
  passa o portão inteiro;
- **não vê sobreposição de unidades** — a C3 continua em prosa;
- **a condição 6 é uma auto-declaração booleana**: não distingue «não derivada
  do sinal» de «não sabemos quem a escreveu», que é o caso da `zona0`;
- **a condição 5 tem saída assinada**, portanto «declara-se em vez de se
  contornar» e «contorna-se com razão assinada» são, no código, o mesmo gesto.
