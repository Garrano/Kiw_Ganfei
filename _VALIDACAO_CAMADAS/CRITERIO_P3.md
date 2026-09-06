> # ⚠ REFUTADO em 06-09-2026, ANTES de correr
>
> O adversario reproduziu todos os numeros do §2 e do §3 a tres decimais — a
> aritmetica esta certa. E depois mostrou que **a premissa fisica esta errada na
> metade que carrega o teste**, e que a celula «com potencia» nao tem potencia.
>
> **1 · O fosso nao mede estrutura.** `resto − nu2021` em VH orb147 mexe-se
> **0,887 dB DENTRO da estacao sem folha** — Nov +1,890, Jan +2,645, Mar +1,758 —
> com a estrutura constante. E 90 % do MDE da celula primaria. Uma grandeza que
> varia isso enquanto a estrutura nao muda **nao esta a medir a estrutura**: esta
> a medir cobertura do solo (erva de inverno contra lavra humedecida).
>
> **2 · O tecto estava ao dobro.** Eu usei `resto − nu2021` (+2,302). O que a
> unidade pode percorrer mede-se directamente e ja inclui a diluicao dos 45 %:
> **`zona0 − nu2021` = +1,164 dB (orb147) e +0,725 (orb125)**. O racio de 2,3×
> passa a **1,12× medido**, e o bootstrap da **P(racio < 1) = 0,17**.
>
> **3 · A celula falha o meu proprio criterio de admissao.** O §3 admite uma
> celula se o tecto exceder o MDE por mais do que a incerteza do tecto. Em bruto:
> 1,31 contra sd 0,733 = 1,8 sd, admitida. Corrigido: **0,17 contra 0,541 = 0,32
> sd**. Falha.
>
> **4 · E o veredicto ja esta decidido antes de correr.** O rotulo de modo comum
> dispara em VH orb147 a **+0,841 dB** — 72 % de todo o alcance corrigido. Pelo
> §5, o resultado sai rotulado «modo comum nao separavel» faca o que fizer.
>
> **Correr isto produzia uma linha predeterminada e nao interpretavel.**
>
> E ha uma armadilha de redaccao que ele apanhou e que eu nao tinha visto: com
> 33 % de potencia a 50 % de remocao, o teste cai quase sempre na linha 2 — que
> tem a palavra **DECLINIO** em maiusculas. **Um teste cuja saida quase certa e
> uma celula que nomeia a hipotese e a forma B com a polaridade invertida.**
>
> **Estatuto: REFUTADO. Nao correr.** Ver AUD-16.

# CRITÉRIO P3 — declínio ou arranque, nas mesmas cenas de inverno

**06-09-2026, antes de correr. Vai a adversário e espera-se pela resposta.**

Herda inteiro o aparelho do `CRITERIO_SAR_v3.md` + adenda, que passou adversário
e foi lido. **O que muda é a polarização e a pergunta; tudo o resto é o mesmo, de
propósito.**

---

## 1 · A pergunta, e porque o inverno a responde

Em Janeiro o kiwi não tem folha. **A retrodifusão de inverno não mede copado —
mede estrutura e solo**: postes, arames, cordões, tronco, e o chão por baixo.

> **Se a planta foi removida, a estrutura desapareceu com ela e o inverno tem de
> o mostrar. Se só se perdeu folha, o inverno não muda — porque no inverno nunca
> houve folha.**

É por isso que este teste corre nas **mesmas cenas** que a leitura já usou, sem
descarregar nada.

## 2 · O tecto estrutural, medido — e é o que define o alcance

A distância que uma remoção **total** da estrutura teria de percorrer é o nível
que separa pomar vegetado de chão nu, em inverno. Medido nos anos de base
(`resto − nu2021`, S1A, Nov-Fev):

| | tecto | sd entre anos |
|---|---|---|
| VV orb125 | +1,308 dB | 0,391 |
| VV orb147 | +2,022 dB | 0,796 |
| VH orb125 | +1,548 dB | 0,455 |
| **VH orb147** | **+2,302 dB** | 0,733 |

## 3 · E há UMA célula com potência. Uma só.

Cruzando o tecto do §2 com o MDE de cada contraste, medido nos anos de base:

| | tecto | MDE | **tecto / MDE** |
|---|---|---|---|
| VV orb125 | 1,31 | 0,99 – 1,24 | 1,1× |
| VV orb147 | 2,02 | 1,58 – 1,61 | 1,3× |
| VH orb125 | 1,55 | 1,51 – 1,57 | **1,0× — nenhuma** |
| **VH orb147** | **2,30** | **0,99 – 1,04** | **2,3×** |

> **Declarado antes de correr: a leitura primária é VH, órbita 147.** É a única
> célula em que o tecto excede o MDE por mais do que a incerteza do próprio
> tecto. As outras três correm e publicam-se, **marcadas «sem potência»**, e
> **nenhuma conclusão se apoia nelas**.

Isto é o oposto do que aconteceu na leitura em VV, em que **todas** as células
estavam no limite ou abaixo dele. A diferença não é acaso: o VH é mais sensível
à dispersão de volume dos elementos lenhosos, e a órbita 147 tem menos ruído
entre anos nesta unidade.

## 4 · A regra de veredicto

Aplicada à célula com potência, e só a ela:

| | leitura |
|---|---|
| **Δ ≤ −MDE** (a `zona0` aproxima-se do chão nu) | **ARRANQUE ou remoção de estrutura** |
| **\|Δ\| < MDE** | **a estrutura não mudou de forma detectável** — compatível com DECLÍNIO, e **só isso**: é ausência de prova de remoção, não prova de permanência |
| **Δ ≥ +MDE** (afasta-se do chão nu) | **INDETERMINADO** — nenhuma hipótese o previa |

**Bilateral**, como na leitura anterior, e pela mesma razão: já vi o inverno.

## 5 · O que é herdado sem alteração, e não se re-decide

Do `CRITERIO_SAR_v3` + adenda, tudo:

- fórmula `zona0 − comparador`, média anual das cenas, Nov-Fev, ano hidrológico
  a 1 de Setembro;
- **S1A com acerto `.upper()`** — IX-09, esvazia o ano de tratamento em silêncio;
- **os dois comparadores** publicados lado a lado;
- **as duas bases**, n = 10 e n = 9;
- `MDE = (t(0,975;n−2) + t(0,80;n−2)) · sd · √(1+1/(n−1))`, sd **só na base**;
- **o posto não acompanha um Δ abaixo do MDE**;
- **o portão de abortar** e o **rótulo de modo comum**, com as duas unidades de
  controlo e a `zona0` fora, limiar 0,5 dB **asserido**.

**Ressalva que vem da leitura de VV e tem de viajar:** naquela leitura o rótulo
de modo comum **disparou** a +0,764 e +0,774 dB. Se disparar também em VH, o
resultado é rotulado da mesma maneira e **não se lê como acontecimento na
`zona0`**.

## 6 · O que este teste NÃO faz

- **não data nada** — é uma comparação entre anos, não uma série;
- **não diz a causa;**
- **não distingue remoção da planta de remoção só da pérgola.** O tecto do §2 é
  a distância a chão nu, que é as duas coisas juntas;
- **não fecha a condição 2 do portão.** VH e VV são o mesmo sensor, o mesmo
  produto, a mesma cadeia. **Duas polarizações não são dois instrumentos**, e o
  `guarda.py` não o veria — a lista de índices é óptica e a ausência de acerto
  desliga a verificação em vez de bloquear. Declara-se;
- **não tem potência em três das quatro células**, e isso vai escrito ao lado de
  cada uma.

## 7 · A ameaça que me preocupa, e não sei resolver

A `zona0` é **45 % `nu2021`** — chão lavrado em 2021, sem copado em ano nenhum.
O tecto do §2 mede a distância entre pomar e chão nu; **quase metade da unidade
já está desse lado da distância**. Isso comprime o alcance disponível por um
factor que não sei estimar sem uma medição que não tenho.

**Consequência declarada: o tecto do §2 é um limite superior optimista para esta
unidade em particular, e o rácio de 2,3× é portanto optimista.** Se o adversário
souber quantificá-lo, o número dele substitui o meu.

## 8 · Ficheiros

`p3_estrutura.py` lê `sar_ano_inteiro_dedup.csv` e escreve `p3_estrutura.json`.
**Não existe, e não se escreve antes de o adversário responder.**
