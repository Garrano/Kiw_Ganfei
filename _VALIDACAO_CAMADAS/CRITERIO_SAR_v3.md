# CRITÉRIO v3 — escrito CONTRA as sete alterações, e mais nada

**06-09-2026. Vai a adversário e espera-se pela resposta antes de ler.**

> **Regra que governa este documento:** cada elemento traça-se a **uma das sete
> alterações** que o adversário exigiu, ou a **uma medição feita nos anos de
> base**. Não acrescentei nada de minha lavra. Onde uma constante aparece sem
> medição atrás, é defeito e assinalo-o eu próprio.
>
> A regra vem da refutação da AUD-13: **as constantes derivadas de uma medição
> aguentaram todas; as asseridas partiram todas, em três versões.**

---

## 0 · Um achado novo, e ele muda a escala de tudo o que escrevi antes

Ao derivar a escala para a alteração 5, medi o desvio entre anos de base do
contraste **que a pergunta usa**, e não do controlo:

| contraste | órb | n | sd entre anos | **MDE** |
|---|---|---|---|---|
| `zona0 − resto` | 125 | 10 | 0,369 | **1,24 dB** |
| `zona0 − resto` | 147 | 10 | 0,479 | **1,61 dB** |
| `zona0 − resto` | média | 10 | 0,376 | **1,26 dB** |
| `zona0 − referencia` | 125 | 10 | 0,293 | **0,99 dB** |
| `zona0 − referencia` | 147 | 10 | 0,469 | **1,58 dB** |
| `zona0 − referencia` | média | 10 | 0,334 | **1,12 dB** |

**Todos os MDE que publiquei — 0,39 a 0,55 dB — foram calculados no
`resto − referencia`, que é o CONTROLO.** A `zona0` tem 202 células contra 2411
do `resto`, e o seu contraste é **duas a três vezes mais ruidoso**. O MDE
verdadeiro da pergunta é **0,99 a 1,61 dB**.

Registado como **IX-08**. Consequência imediata, e é grande: o tecto físico do
sinal de copado é **+1,02 dB (orb125) e +2,05 (orb147)**. Na órbita 125 o MDE
(0,99–1,24) **iguala ou excede o tecto**. Ou seja: mesmo a perda total do copado
está no limite do detectável nesta unidade e nesta órbita.

**Isto tem de ir na leitura, seja qual for o resultado.**

---

## 1 · A fórmula, escrita (alteração 1)

```
contraste(cena)  =  zona0_vv_db  −  COMPARADOR_vv_db
contraste(ano)   =  média das cenas do ano hidrológico, Nov a Fev
Δ                =  contraste(2025-26)  −  média dos contrastes dos anos de base
```

**É contraste, não nível.** VV. S1A. Nov-Fev. Ano hidrológico a começar a 1 de
Setembro — verificado inerte para Nov-Fev, mas declarado.

`COMPARADOR` toma os **dois** valores, e ambos se publicam (alteração 6).

## 2 · A direcção (alteração 2)

**Bilateral.** Não unilateral.

A razão não é estatística, é de honestidade: o §0 do critério anterior declara
que eu **já vi** o contraste de inverno da `zona0` na agregação antiga. Não posso
reclamar uma previsão direccional cega depois disso. O bilateral custa um factor
de 2 e é o que a minha posição permite.

## 3 · Agregação e órbitas (alteração 3)

- **agregação anual: média** das cenas do ano. Não mediana.
- **órbitas: publicam-se as três** — 125, 147, e a média das duas. O adversário
  mediu que a escolha vale até 4 posições de posto; publicar as três remove a
  escolha em vez de a esconder.

Com os dois comparadores, são **seis células** publicadas. Todas, sempre.

## 4 · O nulo — e o posto **deixa de ter p** (alteração 4)

Medido no controlo, anos de base: **ACF(1) = +0,233 (orb125) e +0,429 (orb147)**.
Os onze anos **não são permutáveis**, e o «chão atingível de 1/11 ≈ 0,09» está
errado por 2 a 4× no sentido alto.

E a prova directa que o adversário produziu, sobre o **controlo** — onde ninguém
alega acontecimento: a regra do posto atinge o extremo em **31 de 72
especificações defensáveis**, 43 %.

> **Pré-registado: o posto reporta-se SEM p, e explicitamente como não-evidencial.**
> A frase permitida é *«é o k-ésimo de onze»*. A frase proibida é qualquer coisa
> com «significativo», «p =» ou «improvável».

**A estatística primária passa a ser o Δ contra o MDE derivado do §0** — que tem
escala, e foi a escala que eu tinha deitado fora ao trocar o limiar pelo posto.

## 5 · O portão de abortar e o rótulo de modo comum, retomados (alteração 5)

Ambos vinham da v2 e eu perdi-os ao simplificar. Voltam como estavam, com o
número que o adversário mandou registar:

> **Registado antes de ler:** no ano de tratamento, o contraste
> `resto − referencia` está em **+0,253 dB (orb125) e +0,230 (orb147)** acima da
> média da base — **1,6 e 1,9 desvios, posto 11 de 11 nas duas órbitas**.
> **O comparador está, ele próprio, na sua posição mais extrema em onze anos,
> exactamente no ano que se vai testar.**

- **Portão de abortar:** se `resto − referencia` exceder o seu próprio MDE no ano
  de tratamento, a leitura não se faz. *Verificado: +0,25/+0,23 contra MDE de
  0,55/0,44 — não excede, e a leitura pode correr.*
- **Rótulo de modo comum:** publicam-se os **níveis absolutos** de `zona0`,
  `resto` e `referencia` no ano de tratamento contra a distribuição de base. **Se
  o deslocamento comum às três for ≥ 0,5 dB, o resultado é rotulado «modo comum
  não separável»** e não se lê como acontecimento na `zona0`.

## 6 · Os dois comparadores, lado a lado (alteração 6)

O argumento com que expulsei a `referencia` — «o nível move-se 0,91 dB entre anos
de base» — **não a distingue do `resto`, que move 0,87**. E eu citei só a órbita
boa: em orb125 a `referencia` move-se **2,15 dB** e o `resto` 1,84. **Nenhuma das
duas é âncora estável de nível.**

> **Pré-registado: publicam-se `zona0 − resto` e `zona0 − referencia` lado a lado,
> nas três órbitas.** Se discordarem, isso é o resultado — não se escolhe.

## 7 · Atribuições e n, corrigidos (alteração 7)

- **O «rank 61 de 2421» é do `este`** — disco de 90 m centrado em `FOCO_ESTE` —
  e eu atribuí-o à `zona0`. São 87 % o mesmo conjunto, **não são a mesma unidade**,
  e o percentil 2,5 % **não é neutro**: é menos extremo do que o `oeste` (0,17 %),
  não é ausência de selecção. Registado como IX-07.
- **A `zona0` não tem verificação de posição própria.** O que tem é a proveniência:
  polígono de sete vértices escrito à mão, fixo, anterior ao acontecimento. Vale
  como fronteira não derivada do sinal **por proveniência, não por medição**, e a
  auditoria das máscaras assinalou que ele não tem produtor em código nenhum.
- **n = 11 anos, e o primeiro é meio inverno.** O ficheiro começa a 2016-01-01,
  logo 2015-16 não tem Novembro nem Dezembro: 10 cenas contra 16-20 nos outros,
  com composição sazonal diferente.
- **IX-06:** as 39 cenas anteriores a 2016-09-10 têm chuva a **zero por ausência**.
  Não afecta esta leitura (não usa chuva), afecta o P4.

## 8 · O que sai daqui, e sai por indicação do adversário

**Não são adiamentos meus — são correcções de rumo dele, e ficam escritas para
não virarem «se der jeito»:**

- **O P3 na forma barata não precisa de Verão nenhum.** O VV vê a folha; o VH vê
  a estrutura em **todas** as estações (+1,4 a +2,3 dB, p < 1e-5). Perda de folha
  moveria o VV e não o VH; remoção da planta moveria os dois. **Corre sobre as
  mesmas cenas de inverno, com zero dados adicionais.** O que tem de sair é o
  *Verão* — 3 e 2 cenas S1A em Jun-Ago de 2026 — não o P3.
- **O P2 é o instrumento da condição 5 do portão.** «A unidade era a mesma coisa
  ao longo do intervalo?» foi a falha que retirou o A3, e num inverno atlântico
  só o SAR responde. **Como está, esta leitura não passa a condição 5**, e isso
  declara-se em vez de se contornar.
- **O P4 é gratuito e o inverno é o 2.º mais chuvoso dos onze** (332,7 mm de
  `chuva_30d` médio contra 219 na base). Publicar «o mais extremo dos onze» sem
  tocar na explicação benigna, nesse inverno, num sítio a 13,4 m da drenagem,
  não é sequenciação prudente.

> **Compromisso, e é o que impede o jardim de caminhos:** os três correm a
> seguir a este, por esta ordem, **e publicam-se haja o que houver**.

## 9 · O que esta leitura não fecha

- **não fecha a condição 2 do portão.** Duas órbitas a r = +0,90 não são
  instrumento independente uma da outra, e o `guarda.py` autorizaria na mesma
  porque a lista `INDICES` é óptica. Declara-se.
- **não passa a condição 5** — ver §8.
- **não estima magnitude ocidental.**
- **e, pelo §0, pode não ter potência para detectar nem a perda total do copado
  na órbita 125.**

## 10 · Ficheiros

`sar_v3.py` lê `sar_ano_inteiro_dedup.csv` e escreve `sar_v3.json`.
**Não existe, e não se escreve antes de o adversário responder.**
