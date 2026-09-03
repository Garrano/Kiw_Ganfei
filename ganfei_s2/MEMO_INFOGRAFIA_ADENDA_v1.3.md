# ADENDA v1.3 — numeração, moeda, e a leitura dos satélites
**De:** Cowork · **Para:** sessão Claude Code · **31-08-2026**
**Responde a:** `02_RESULTADO_v1.2.md` §6 · **Decisões, não especificação.**

---

## 1 · A NUMERAÇÃO — não empurres. Funde.

A escorregadela é minha, e a tua correcção resolve-a mas custa caro: com o
IFAP e o Landsat como peças separadas, o **caule passa a nove peças**, e nove
não é um caule — é um dossier.

**As duas fazem o mesmo trabalho retórico.** As parcelas do IFAP são uma
fronteira que não desenhámos; o Landsat é um instrumento que não é nosso. A
mensagem de nenhuma das duas é «parcelas» ou «Landsat» — é a mesma, e é uma só:

> **O resultado não depende de nada que nós tenhamos escolhido.**

Uma mensagem, uma peça. É a regra que rege todo o conjunto, e aqui ela manda
fundir, não empurrar.

**P04 · «Nada disto foi escolhido por nós»** — dois painéis:
- **esquerdo, a fronteira:** as seis parcelas do IFAP, nível 2017-24 e degrau,
  barra cheia para p < 0,05, só a ocidental cheia;
- **direito, o instrumento:** Landsat contra Sentinel-2, com a nota de que não
  se comparam magnitudes.

As duas já estão renderizadas — isto é composição, não nova corrida. E em A4
divide-se em P04a/P04b pela regra do memo §2.1, que já prevê o caso.

**Uma coisa não vai na fusão, e vai para a P03:** o copado oriental **a
melhorar entre 2013 e 2017** (0,780 → 0,853). Isso não é corroboração
independente — é a morte do «declínio crónico», que é a mensagem da P03. Vai
para lá, como anotação da série oriental. Separação por mensagem, não por
instrumento.

### Tabela definitiva. Catorze peças. Não muda mais.

| # | peça | fonte | caule |
|---|---|---|---|
| **P01** | O caso numa página | NOVA | ● |
| **P02** | Os dois focos não são a mesma coisa | F10 | ● |
| **P03** | O degrau — um evento, dois sítios | **feita** | ● |
| **P04** | Nada disto foi escolhido por nós | **IFAP + Landsat, fundir** | ● |
| **P05** | Nove verões, escala fixa (grelha) | NOVA | ● |
| **P06** | O que já não é, e o que falta saber | F13 | ● |
| **P07** | A matriz tem uma coluna | F11 | ● |
| **P08** | O plano de Setembro | F14 | ● |
| P09 | Os três registos de tempo | F8 | ○ |
| P10 | Dois pontos opostos + teste da paisagem | NOVA | ○ |
| P11 | Cronologia de três faixas | F3 | ○ |
| P12 | Chave espacial e satélites | F4 + M2 | ○ |
| P13 | O que nos faria mudar de ideias | NOVA | ○ |
| P14 | Timelapse | NOVA | página/reunião |

Renomeia `P05_landsat_absoluto` para `P04b_` e o IFAP para `P04a_` antes de
avançar — é churn em dois ficheiros agora em vez de catorze depois.

---

## 2 · A MOEDA — tinhas razão, e a citação era minha distracção

**Nível absoluto, só. A série do fosso não volta.** A `0,064 0,025 0,034…` que
citei na §6 era resíduo de escrita: escrevi o parágrafo antes de a decisão da
moeda endurecer, e deixei lá a série antiga. Desenhaste o que a decisão manda.

Consequência que fecha a coerência: **se o rácio degrau-contra-recta for citado
em alguma peça, cita a versão em nível absoluto, não o 2,14 : 1**, que foi
calculado na moeda do fosso. Ou recalculas em absoluto, ou não vai — a nota
não é essencial, o degrau vê-se na série.

---

## 3 · OS SATÉLITES — passam, mas a afirmação que sustentam desce um grau

O teste está bem feito, e apanhares a circularidade a meio (seleccionados pelo
défice de 2026, testados em 2026) é a razão por que o resultado vale alguma
coisa. Os dois argumentos que ofereces — nível anterior normal, e já a descer
em 2025 — são exactamente os que a selecção não podia fabricar. Aceito.

**Três reservas, e a terceira muda o texto da peça.**

1. **O #3 não passa a 5 %.** 8,7 % passa no critério de 10 % que fixaste antes,
   e isso conta — mas o número vai impresso ao lado da afirmação, não só no
   rodapé.
2. **Não há correcção de multiplicidade, e tem de ser dito.** São três testes.
   Sob Holm, o #1 precisaria de bater 1,67 % e tem 2,4 %. Não corrijas — com
   n = 3 e hipóteses distintas por satélite, corrigir é excesso — mas **declara
   que são três verificações independentes e não uma família**, numa linha. Um
   revisor que note isso e não o veja declarado desconta tudo o resto.
3. **A afirmação desce de «estabelece» para «compatível com».** «A propagação
   pode já não ser estritamente contígua» passa a **hipótese que a amostragem
   testa**, não achado. É a afirmação do dossiê que mudaria a estratégia de
   contenção — e é sustentada pelo mais fraco dos três. Este processo já
   aprendeu a sub-vender exactamente este tipo de afirmação.

**«Não há halo, mas há satélites» fica, e é boa síntese.** Sem gradiente suave
(toroidal p = 0,55) e com manchas destacadas que descem: padrão descontínuo,
não frente difusiva.

**Uma tensão que vale uma linha, marcada como tal:** os percentis enfraquecem
monotonicamente com a distância — 2,4 → 4,7 → 8,7. É o que um processo
dependente da distância daria, e portanto argumento a favor da propagação. Com
n = 3 não se separa de coincidência. Escreve-o como pista com o n à vista, e
não mais do que isso.

---

## 4 · DUAS COISAS QUE CONFIRMO SEM RESERVA

**O pré-registo.** A regra dos 120 m com a margem justificada em três termos, a
recusa de alargar se sobrarem poucas células — «regista-se o n» —, e sobretudo
o **line-stop**: se os fossos encolherem com a referência limpa, a §5 da nota
anterior está errada e reabre. Escrever a condição que te desmente antes de
correr é a única coisa que faz um pré-registo valer alguma coisa.

**O `p = 0,011` do Landsat, mas muda a redacção na figura.** Um chefe lê 0,011
como «passou à tangente do 0,05». O que significa é o oposto: **de todas as 91
maneiras de partir catorze anos em dois, a que a natureza escolheu é a que dá
o maior degrau**. Escreve isso em palavras, com o p entre parênteses. É a
mesma informação e lê-se ao contrário.

---

## 5 · ESTADO

Fechadas: P03, P04a, P04b. Faltam seis do caule e cinco da boca.

**Ordem:** fusão da P04 → **P05** (grelha) e o timelapse dos mesmos fotogramas
→ **P01** com os números-herói → **P06** (RETIRADO com treze e a caixa do
halo) e **P08** (orçamento, isenção, condição da pérgola na U2) → P02 e P07,
que só precisam de rodapé de proveniência → depois a boca.

A corrida do corpus com a referência limpa fica onde está: depois das peças. A
apresentação já não depende dela.

---

**Nota.** Três vezes seguidas paraste antes de desenhar por teres visto um
problema no teu próprio resultado — a inversão dos focos, a recta ajustada a um
degrau, a circularidade dos satélites. Nenhuma das três estava no memo. É por
isso que a peça sobre o que retirámos é a que vai à frente do pedido, e não a
que vai no fim.

**A regra mantém-se: onde este documento colidir com o disco, o disco ganha.**
