# PRÉ-REGISTO · reconstrução da grelha de referência

**Escrito em 31-08-2026, ANTES de correr.** Nenhum número deste documento foi
obtido com a grelha nova. Se algo aqui mudar depois de ver resultados, a
alteração vai datada e por baixo, nunca por cima.

Exigido pela adenda v1.2 §5. Motivo: uma reconstrução de rubrica sem
pré-registo é um jardim de caminhos que se bifurcam, e este processo já sabe
o que isso custa.

---

## 1 · O defeito, medido

A grelha de referência tem 110 células, escolhidas em 2010/2012 sobre pérgola
detectada por ortofoto, em malha regular de 30 m, a ≥ 20 m de qualquer bordo.
Nenhuma foi escolhida por valor radiométrico. **O desenho está correcto; o que
falhou foi não impor distância aos focos.**

| | n | degrau 2025-26 |
|---|---|---|
| grelha inteira | 110 | −0,0401 |
| células **dentro** de um disco de foco | 14 | **−0,1458** |
| células a 90–150 m | 23 | −0,0448 |
| células a 150–250 m | 52 | −0,0178 |
| células a mais de 250 m | 14 | −0,0099 |

Catorze células estão dentro dos discos. A mais próxima está a **10 m** de um
centro. Cinco estão dentro do próprio polígono da Zona 0. Essas catorze não
são referência: são foco.

## 2 · A regra de exclusão, e porque não é maior

**Exclui-se uma célula da referência se o seu centro cair dentro de um disco
de foco de 90 m, mais uma margem de 30 m.** Total: 120 m dos centros
E530 999/N4 655 102 (centróide do polígono oriental) e E530 485/N4 655 053.

A margem de 30 m é justificada por três termos e nada mais:
- 10 m de célula da grelha de análise;
- 10 m de erro de registo entre a ortofoto que definiu a pérgola e a grelha;
- 10 m para a convenção de ±0,4 ha já em uso no dossiê.

**Não se usa 150 m, e a razão é um resultado negativo nosso.** O teste de halo
procurou efeito de proximidade e não o encontrou: os anéis não decaem (o do
meio é positivo, +0,015), e o ρ de Spearman de −0,123 tem p toroidal de 0,55
contra p ingénuo de 2×10⁻⁹. **Sem efeito de vizinhança demonstrado, uma
margem grande seria selecção conveniente da referência.** O negativo do halo
tem exactamente este uso operacional: impedir que a margem cresça.

Se a exclusão de 120 m deixar menos de 60 células, **não se alarga a margem** —
regista-se o n e o que ele limita.

## 3 · O que se corre, e por que ordem

Toda a série na moeda «fosso à referência» é recorrida do princípio, corpus
inteiro. **Não se remendam registos**: patching destrói a comparabilidade
longitudinal em que a afirmação assenta.

Não é afectado, e não se recorre: tudo o que está em **nível absoluto** — P03,
P04, P05, o multiverso das 43 análises, os satélites. Foi essa a razão de
mudar de moeda.

## 4 · Que resultado mudaria que conclusão

Fixado agora, para não ser fixado depois:

| se acontecer | então |
|---|---|
| os fossos crescem (referência limpa desce menos) | **é o esperado** — confirma que os números publicados eram conservadores. Não é achado novo; é a correcção de um viés já identificado. |
| os fossos **encolhem** | a referência estava a *inflacionar* os focos e não a atenuá-los. Contradiz a §5 do `01_RESULTADO_D2`. **Line-stop**: publica-se antes de qualquer figura e reabre-se a leitura. |
| algum fosso muda de sinal | line-stop, e a peça que o usava sai da sequência. |
| o degrau em nível absoluto muda | **impossível por construção** — não usa referência. Se mudar, há erro de código, e procura-se o erro em vez de se reportar o número. |

## 5 · O que este pré-registo não cobre

A referência continua a ser **interna**: mede contraste espacial dentro do
mesmo pomar. Reconstruí-la não a torna capaz de detectar declínio uniforme de
toda a exploração. Essa limitação é anterior a este defeito e mantém-se
depois dele — e é uma das razões por que a moeda passou a ser o nível
absoluto.

Também não cobre a escolha do raio de 90 m para o disco de foco, que é
herdada e não re-derivada aqui. O multiverso já mostrou que o degrau em nível
absoluto sobrevive a 60, 90 e 120 m; o mesmo não foi verificado para o fosso.

---

**Assinado antes de correr.** Ficheiros a produzir:
`referencia_reconstruida.py` → `referencia_reconstruida.json`, e um
`DIFF_REFERENCIA.md` que ponha lado a lado cada número publicado na moeda
antiga e o seu substituto.
