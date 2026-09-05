# C3 · adversário — a cláusula executável durou um dia

**Data:** 05-09-2026 · **Alvo:** `fuga.py`, escrito hoje para tornar a C3
executável · **Instrumento:** adversário independente, sessão separada, prompt
divulgado abaixo · **Resultado:** `fuga.py` **RETIRADO** e inerte no mesmo dia.

A `fuga.py` foi entregue a certificar em **14 casos que bloqueiam · 6 positivos
que passam**, e ligada à cadeia como verificação 10. Esse número não era prova
de nada.

---

## 1 · O achado que a derruba

**Arrancar o bloqueio de sobreposição de dados/máscara — a única coisa para que
a cláusula existe — deixa a bateria em 14/14 e 6/6.**

Substituir `if s > tol:` por `if False:` não produz **uma** falha:

```
mutado: o bloqueio de dados/mascara nunca dispara
bloqueiam 14/14 · passam 6/6 · falhas 0
```

Os casos 4, 5 e 8 eram apanhados pela `janela` antes de chegarem ao teste que os
nomeava; o 12 por outro ramo. A bateria exercitava os ramos em que o autor
estava a pensar e deixava o central por tocar — **a forma B**, e exactamente o
0-de-9 que a cláusula C2 diagnosticou na `guarda.py` a 04-09.

**A contra-verificação do autor falhou por ser fraca.** Arranquei a *medição*
(`sobreposicao` a devolver `None`) em vez do *bloqueio*, e essa mutação **era**
detectada — 4 casos caem. Fiquei convencido de que o adversário se enganava.
Enganava-me eu: a mutação certa é a dele. **Uma mutação mal escolhida absolve.**

---

## 2 · Os seis defeitos mecânicos, todos verificados por mim

| | defeito | medido |
|---|---|---|
| **A1** | `_conjunto()` colapsa arrays 1-D de numpy — `arange(1000)` vira **um** tuplo | `sobreposicao(arange(300), arange(1000))` = **0,0**; real 1,0 |
| **A3** | `tolerancia=1.0` com `razao="x"` passa fuga de 100 % | `1.0 > 1.0` = `False`; o ramo nunca dispara |
| **A5** | instrumento comparado por cadeia inteira | `{'NDVI Sentinel-2'} & {'NDVI Landsat'}` = `set()` — **passa** |
| **A6** | controlo com conjunto vazio | `sobreposicao(frozenset(), …)` = `None` → `continue` → passa |
| **B3** | direcção errada na `confirmacao` | mede-se que fracção do controlo cai no ajuste; interessa a inversa |
| **B1/B2** | hold-out temporal e controlo negativo de Lipsitch **não são exprimíveis** | os três desenhos bloqueiam-nos |

Sobre **A1**: num processo cujo pipeline é raster de numpy, este é o caso
comum, não a excepção. E falsifica o docstring da própria função, que promete
*«um controlo pequeno inteiramente dentro do ajuste dá 1,0 e tem de bloquear»*.

Sobre **A5**: a `guarda.py` fechou este buraco a 03-09 com uma lista de índices,
depois de o Controlo 3 o apanhar no B1. A `fuga.py` reabriu-o **num ficheiro que
cita a regra três vezes**.

Sobre **B2**: a `CLAUSULAS.md` §2 nomeia os controlos negativos de Lipsitch como
o dispositivo da literatura que **fecha a forma A**. A forma executável da C3
proibia o instrumento que o documento da C3 prescreve.

Sobre **B1**, e é o mais fino: a única maneira de declarar um hold-out temporal
que a ficha aceitasse era pôr o ano no identificador — **que é exactamente a
evasão que deixa passar uma fuga real**. O critério não distingue as duas, e
premeia a evasão.

---

## 3 · Um número que eu inventei

> «das cinco, quatro tinham o canal por declarar»

**Não há fonte nenhuma.** Não existe classificação das retiradas por canal em
lado nenhum das duas árvores: o vocabulário dos canais é da `fuga.py`, escrito
hoje. Usei uma estatística fabricada para justificar o fecho por omissão, num
ficheiro cujo argumento central é que números sem produtor são como este
processo perde semanas. Verificado por `grep`: zero acertos fora da `fuga.py`.

E duas atribuições herdadas da `CLAUSULAS.md`, que a `fuga.py` endureceu ao
metê-las numa **mensagem de excepção que imprime ao utilizador**:

- **autocorrelação 0,86–0,96** é do `terreno_contra_declinio.py` — a hipótese do
  terreno, refutada e invertida — e **não da retirada 12**, cujo nulo não era
  por permutação mas por **deslocamento toroidal** (ρ = −0,1233, p assintótico
  2,23 × 10⁻⁹ corrigido para 0,5547);
- **`por_area`** não consta como defeito documentado em fonte nenhuma; é a única
  das cinco na `CLAUSULAS.md` sem número de retirada.

O lóbulo (retirada 15) tem o número certo mas a caracterização **invertida**: as
fontes dizem AOI errada, sem sobreposição, com o rio Minho entre as duas — o
oposto da forma A.

**Sobrevivem sem reserva** dois dos cinco: o placebo do chão (+0,0531 contra
+0,0585, 91 %, verbatim em `ADVERSARIO_2026-08-29.md:124`) e os 55,9 % a 28 px
do ICP (`GEORREF_CONTROLO3_ADVERSARIO.md`).

---

## 4 · O que sobrevive, e a v2

O desenho conceptual **não foi atacado**: cinco canais, regras que se invertem
com o desenho, fecho por omissão. O que muda:

1. **a bateria corre mutação sobre si própria** — cada verificação tem de ser
   detectável ao ser desligada, como o ISOLAMENTO da `guarda.py`. Sem isto,
   nada do resto conta;
2. `_conjunto` trata 1-D, e **recusa** comparar tipos incompatíveis em vez de
   devolver zero;
3. conjunto vazio **bloqueia**;
4. instrumento por família de índice, reutilizando a lista da `guarda.py`;
5. `tolerancia` limitada, e a razão verificada **fora** do ramo;
6. um quarto desenho, para hold-out temporal e controlo negativo;
7. direcção da sobreposição escolhida pelo desenho;
8. o cabeçalho só com números que tenham fonte citada.

---

## 5 · A lição, e não é sobre esta cláusula

O invariante que a `CLAUSULAS.md` nomeia — *alguma coisa que devia ser
independente não era* — aplica-se ao artefacto: **a bateria não era independente
do ficheiro que certificava.** Saiu da mesma leitura dos mesmos cinco defeitos,
pela mesma mão, no mesmo turno.

14/14 e 6/6 não era prova. Era a mesma mão a corrigir o seu próprio exame — que
é a coisa que a `verificar()` regista como nota e depois **decide não bloquear**.

O que apanhou isto foi ir a um instrumento diferente. Como as dezanove
anteriores.
