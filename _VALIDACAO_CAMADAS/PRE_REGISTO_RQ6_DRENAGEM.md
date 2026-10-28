# Pré-registo · RQ6 — as manchas seguem a água, ou espalham-se em raio?

**11-09-2026.** Escrito **antes** de correr, como a C9 exige.

---

## 1 · Porque é este o teste que falta

Tudo o resto está bloqueado em terceiros: o relatório do LNEG exige registo
institucional, as respostas do gestor dependem do email, o painel INIAV depende
da campanha. **A RQ6 não depende de ninguém** — usa só instrumentos que já
passaram pelas duas:

- **`PERDA`** — os 2,20 ha que perderam copado entre Jul-2024 e Jul-2025
  (AUD-17, reproduzido dos ladrilhos brutos a 0,000e+00);
- **`b.Z`** — cota do MDT LiDAR da DGT;
- **`b.ACUM`** — acumulação de fluxo derivada do mesmo MDT;
- **`pomar`** — a máscara do pomar.

Está no plano desde 28-08 (§B2 do enquadramento, pergunta 6 da lista ordenada).

## 2 · O que o teste separa — e NÃO é «biótico contra abiótico»

**Esta é a correcção mais importante deste documento, e é contra a formulação
que eu próprio andei a usar.**

Dizer «segue a drenagem ⇒ abiótico» está errado, porque **os oomicetas
dispersam-se por zoósporos que nadam**. *Phytophthora* e *Phytopythium* seguem a
água tanto quanto o encharcamento segue. Uma mancha alinhada com as linhas de
escoamento é compatível com **as duas** hipóteses húmidas.

O que o teste separa é outra coisa, e é útil na mesma:

| se a mancha… | favorece |
|---|---|
| **segue as linhas de escoamento** | hipóteses **mediadas por água** — hipoxia por encharcamento **ou** oomiceta disperso por zoósporo |
| **é radial e indiferente à água** | propagação por **contacto radicular** — *R. necatrix*, *Armillaria*, que avançam por raiz e rizomorfa |

> **É exactamente o eixo Rosellinia-contra-KVDS**, que é a dúvida central do
> caso. Não resolve dentro do ramo húmido; separa o ramo húmido do ramo seco.

## 3 · A pergunta, fixada

> As células que perderam copado estão em posições de **maior acumulação de
> fluxo** do que se esperaria de uma mancha da mesma forma e tamanho colocada ao
> acaso no pomar?

Unidade: **a célula de 10 m**. Fronteira: a máscara `pomar`. Estatística
declarada antes de ver: **mediana de log₁₀(1+ACUM) nas células PERDA**.

## 4 · O nulo, e porque tem de ser este

As células de PERDA são **espacialmente autocorrelacionadas** — estão em três
manchas. Tratá-las como n=220 independentes inflaciona tudo. E o pomar tem
**gradiente de cota**, logo qualquer mancha mais baixa terá mais acumulação sem
que isso signifique nada.

**Nulo por deslocação da própria mancha.** Para cada uma das **999** repetições:
rodar a máscara PERDA por um ângulo ao acaso e transladá-la para uma posição ao
acaso, exigindo que **≥ 95 % das suas células caiam dentro do `pomar`**.
Recalcular a estatística. Isto preserva **forma, tamanho e compacidade** — e
destrói só a **posição**, que é o que está em teste.

É o mesmo desenho que este processo já usou para a rede de rega («partição por
válvula contra 200 partições rodadas da mesma geometria»).

## 5 · Os critérios, todos antes de correr

| | critério | limiar |
|---|---|---|
| **R-A** | o nulo produz **≥ 500** colocações válidas | senão o pomar é estreito de mais para o teste e diz-se isso |
| **R-B** | **segue a água** se a mediana observada exceder o **percentil 95** do nulo | p unilateral ≤ 0,05 |
| **R-C** | **indiferente à água** se cair entre os percentis 5 e 95 | — |
| **R-D** | **evita a água** se ficar abaixo do percentil 5 | resultado inesperado, e regista-se como tal |
| **R-E** | **poder declarado**: qual o deslocamento de mediana que o nulo detectaria a 80 % | sem isto, um «não distingue» não é interpretável |

## 6 · A segunda leitura, independente da primeira

**Alongamento contra a direcção do escoamento.** Para cada mancha, comparar o
eixo maior (por momentos de segunda ordem) com a direcção média do fluxo nas
suas células. Se as manchas forem **alongadas ao longo** do fluxo, reforça R-B;
se forem **redondas**, reforça R-C. Entra como corroboração, **nunca sozinha**.

## 7 · O que falsifica o quê

- **R-C ou R-D** enfraquecem as duas hipóteses húmidas e **põem a propagação por
  contacto radicular à frente** — o que, dado que a *Rosellinia* assenta hoje na
  observação de **uma** planta, seria o primeiro apoio independente que ela teria.
- **R-B** não prova encharcamento: deixa a hipoxia e o oomiceta empatados, e
  **aumenta o valor do painel INIAV**, que é o que os separa.

## 8 · O que este teste NÃO pode fazer

- **Não estabelece causa.** É geometria contra geometria.
- **Não vê a estrutura**: a `PERDA` vem do LiDAR, que mede folha. Uma célula
  pode estar lá por a planta ter sido arrancada (`IX-25` e a condição 2 da
  AUD-20).
- **Não separa hipoxia de oomiceta** (§2).
- **O ACUM é derivado do MDT de 2025**, posterior ao acontecimento. Se houve
  movimento de terras entretanto, a drenagem que se mede não é a que actuou.
  **Isto é uma ressalva viva** e viaja com o resultado.

---

# 9 · Corrida 1 · 11-09-2026 — **PAROU EM R-A**, como estava previsto

```
pomar   3031 celulas · PERDA 220 celulas
nulo:   15 colocacoes validas em 59 940 tentativas
```

**R-A exigia ≥ 500 e obteve 15.** O teste **não correu**.

**Porquê, e é geometria, não azar:** a máscara `PERDA` abrange **três manchas**
distribuídas pela faixa do pomar. A sua caixa envolvente é quase tão grande como
o próprio pomar, que é uma tira estreita ao longo do rio. Rodar e transladar
essa constelação inteira quase nunca deixa 95 % das células dentro.

## 9.1 Dois números que a corrida imprimiu antes de parar

| | PERDA | resto do pomar |
|---|---|---|
| mediana de log₁₀(1+ACUM) | **0,477** | **0,477** |
| cota mediana | **7,75 m** | **6,99 m** |

**Não se lê nada disto ainda.** É a comparação crua que o nulo existia para
julgar, e sem nulo não tem p nem poder. Regista-se porque vai ser tentador
esquecer que apareceu — e porque, se sobreviver ao nulo certo, aponta na direcção
**contrária** à do encharcamento: acumulação igual, e a perda em terreno **mais
alto**, não mais baixo.

---

# 10 · Pré-registo da corrida 2 — nulo POR MANCHA

**Escrito depois de ver a corrida 1 falhar em R-A, e antes de correr a 2.**
A corrida 1 fica no registo. Isto é um teste **diferente**, não um afinamento.

## 10.1 O que muda, e porquê é a pergunta certa

A pergunta é **onde cada mancha se senta em relação à drenagem** — não qual é a
configuração conjunta das três. Deslocá-las rigidamente em bloco testa uma
hipótese muito mais apertada, e é a que rebentou a geometria.

**Nulo novo:** cada mancha é deslocada **independentemente** — rodada e
transladada — exigindo ≥ 95 % das suas células dentro do `pomar`. A estatística
de cada repetição é a mediana das três manchas deslocadas em conjunto.

Isto preserva a **forma e o tamanho de cada mancha** e destrói a **posição de
cada uma**, que é o que está em teste.

## 10.2 Critérios — os mesmos, e um novo

| | critério | limiar |
|---|---|---|
| **R-A2** | ≥ 500 repetições válidas, **e ≥ 200 colocações válidas por mancha** | senão pára outra vez e diz-se |
| **R-B2 / C2 / D2** | como R-B, R-C, R-D | percentis 5 e 95 |
| **R-E2** | poder declarado | deslocamento detectável a 80 % |
| **R-F2 · NOVO** | a **cota** entra como covariável declarada: repete-se o teste com o nulo restrito a colocações cuja **cota mediana** esteja dentro de ±0,5 m da observada | se o veredicto mudar, é a cota que manda e não a água |

O **R-F2** existe porque a corrida 1 mostrou que PERDA e resto do pomar diferem
**0,76 m de cota mediana**. Num terraço com 2 m de amplitude total, isso não é
pequeno, e um nulo que ignore a cota compara a mancha com sítios que não são
comparáveis.

---

# 11 · Corrida 2 · 11-09-2026 — correu, e **falhou em R-E**

O nulo por mancha resolveu a geometria: **seis manchas** (68, 23, 20, 12, 10, 9
células), **300 colocações válidas em 300 tentativas** por cada uma, **999
repetições válidas em 999**. O R-A2 passa com folga.

E depois:

```
nulo   mediana 0,477 · p05 0,301 · p95 0,477
obs    0,477
p unilateral 0,5536
R-E · deslocamento detectável: 0,000 log10  (=1,00x)
```

## 11.1 O veredicto é NÃO TESTÁVEL — e não «indiferente à água»

A mediana do nulo e o seu p95 são **o mesmo número**. A estatística não tem
resolução, e a razão está na distribuição da acumulação dentro do pomar:

| p5 | p25 | **p50** | p75 | p90 | p95 | p100 |
|---|---|---|---|---|---|---|
| 1 | 1 | **2** | 4 | 241 | 607 | 14 721 |

**62,8 % das células têm acumulação ≤ 2.** O pomar é um terraço plano: o
escoamento é quase nulo em quase todo o lado e enorme em meia dúzia de células de
linha de água. **A mediana de um campo assim está presa no valor mais comum e não
se move.**

> **Isto é a mesma espécie do `DEC-03`: falta de poder, não resultado negativo.**
> Dizer «as manchas são indiferentes à água» com um teste que não distingue
> deslocamento nenhum seria inventar um achado a partir de um instrumento cego.

## 11.2 Um defeito meu no portão, e é da forma B

A primeira versão do bloco de veredicto **imprimiu «R-C · indiferente à água»**
com deslocamento detectável de 0,000. O `R-E` estava calculado e escrito no
critério — **e não era consultado antes de decidir**. Um teste sem poder devolve
sempre «não distingue», e o portão deixava isso passar como resultado.

**Corrigido:** o `R-E` decide primeiro. Abaixo de 0,05 log10 o guião devolve
**NÃO TESTÁVEL** e nomeia a razão.

## 11.3 O que a corrida 2 deixa de pé

**Nada sobre a hipótese.** Deixa duas coisas úteis:

1. **O nulo por mancha funciona** — 999 em 999, seis manchas, todas colocáveis.
   A máquina está boa; a estatística é que não presta.
2. **A caracterização do campo**: o pomar é plano ao ponto de a acumulação não
   discriminar. Isso é ele próprio um facto sobre o terreno.

## 11.4 A terceira tentativa precisa de pré-registo próprio

A estatística óbvia — **distância à linha de água mais próxima** — é contínua,
não tem cauda pesada, e mede o que a pergunta quer. **Mas escolhê-la agora, depois
de ver a mediana falhar, é o caminho que bifurca.** Fica para pré-registo
separado, escrito antes, e com o número de tentativas declarado: **esta será a
terceira**, e isso entra no cabeçalho.

---

# 12 · RQ6 FECHA COMO DUPLICADO — e o portão S1 apanhou-o

## 12.1 O que aconteceu

Escrevi a `rq6_drenagem.py` **sem correr a busca primeiro**. A `certificar.py`
recusou-se a certificar e nomeou a falta:

```
S1: 1 guiao tocado hoje (rq6_drenagem.py) e NENHUMA busca registada
```

Corrida a busca, o primeiro acerto é **`terreno_contra_declinio.py`**, de
**29-08-2026**, marcado **JÁ FECHADO**, com o título:
*«O declínio segue o terreno? — o teste que aponta a uma causa.»*

## 12.2 A resposta já existia, e é mais forte do que a minha seria

Da `HIPOTESES_FECHADAS.md`:

> **«O declínio segue o terreno» — REFUTADA E INVERTIDA.** O défice está no
> terreno **alto**: ρ da cota negativo **nas onze cenas, p < 0,001**. **Nenhuma
> métrica de humidade emerge em 2025-26**; a área drenante chega a **decair para
> zero** nos anos do evento.

E o desenho é melhor do que o meu em duas coisas:

| | o que eu fiz | o que já existia |
|---|---|---|
| estatística | mediana de log(1+acumulação) — **sem resolução num terraço plano** | **TWI** (`ln(a/tan b)`, com `resolve_flats`), cota, desvio local **e** acumulação |
| nulo | rodar e transladar a mancha | **a própria série**: o terreno é o mesmo em 2017 e em 2026, logo só conta o que **emerge** em 2025-26 |

O nulo pela série é claramente superior: dispensa a suposição de que uma mancha
deslocada é comparável, e responde directamente à pergunta que interessa —
*mudou alguma coisa no ano do acontecimento?*

## 12.3 Coerência, e é o único crédito das minhas duas corridas

O diagnóstico cru da corrida 1, antes de parar, deu **cota mediana 7,75 m na
PERDA contra 6,99 m no resto do pomar** — a perda em terreno **mais alto**.
**Aponta no mesmo sentido que o resultado de 29-08**, por instrumento diferente
(LiDAR de altura de copado, e não NDVI) e em janela diferente (2024→2025, e não
as onze cenas). Não é confirmação independente com estatuto — é coerência, e
regista-se como tal.

## 12.4 Estado

**RQ6 fecha como DUPLICADO.** As duas corridas ficam no registo como o que
foram: uma reinvenção, apanhada pelo portão que existe para isso. O
`rq6_drenagem.py` **não é citável** e a sua saída não entra em lado nenhum.

**O que a resposta que já existia faz ao caso:** enfraquece o ramo **húmido** —
hipoxia por encharcamento **e** oomiceta disperso por zoósporo, que ambos
precisam de água — e **põe à frente a propagação por contacto radicular**,
*R. necatrix* e *Armillaria*. Ou seja: **o diagnóstico de trabalho, que hoje
assenta na observação visual de UMA planta, tem afinal apoio espacial
independente** — e ninguém o tinha ligado.

**Isto tem de ir ao `tier1_framework_draft.md`**, cujo §2 diz que o KVDS é «o
melhor ajuste epidemiológico do processo». Continua a ser, pela apresentação
clínica — mas a geometria do declínio não o acompanha, e essa tensão tem de
ficar escrita em vez de resolvida por omissão.
