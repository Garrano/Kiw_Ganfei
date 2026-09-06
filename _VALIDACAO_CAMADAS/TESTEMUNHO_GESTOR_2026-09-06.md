# Testemunho do gestor, 06-09-2026 — tipo 1, e derruba coisas

**Regra que governa esta página, e vem do `CLAUDE.md`:** testemunho directo *«não
é medição nem inferência — entra como dado (…) quando existir, ganha a qualquer
cálculo nosso — e o cálculo que ele derrubar é **retirado, não reconciliado**.»*

Fonte: respostas do gestor da exploração, 06-09-2026, mais a tabela de válvulas
por sector que as acompanha.

---

## 1 · A tabela de válvulas, e agora está fixada por quem sabe

| sector | válvulas |
|---|---|
| **B1** | **1, 2, 3, 4, 5** |
| **B2** | 6, 7, 8, 9 |
| **Erica Novo** | 10, 11 |
| **B3** | 12, 13, 14, 15 |
| B4 | 16, 17 · B4C3 18 · B5 19 · B1C5 20 · B3C4 21 |
| Viveiro | 22, 23 · B1C6 24 e 25 · **B3C3 27** |

Total 449 275 m². **Isto fecha, por testemunho, a lista de letras de sector por
válvula que estava aberta desde 04-09** — e fecha-a sem o georreferenciamento
que morreu em cinco tentativas.

## 2 · A máscara chamada `zona0` NÃO é a Zona 0. **Retirada de nome.**

> **Gestor: «zone 0 = valves 8, 9, 10».** E, sobre as análises de solo de 2025:
> *«de uma zona a qual nós chamamos de Zona 0, onde tudo começou, ou seja, no
> buraco que se vê nas imagens.»*

Válvulas 8 e 9 são **B2**; a 10 é **Erica Novo**. E o código, em
`c1_00_comum.py:17`, já dizia:

```python
FOCO_OESTE = (530485.0, 4655053.0)   # exploracao chama-lhe "Zona 0"; B2, valvulas 8-9
FOCO_ESTE  = (530977.0, 4655117.0)   # B3, valvulas 13-14
```

**O código estava certo. A máscara é que tem o nome trocado.** Medido:

```
centroide da mascara `zona0_bits` :  E530999 N4655102
    distancia ao FOCO_OESTE (= Zona 0 do gestor) :  516 m
    distancia ao FOCO_ESTE                       :   26 m
```

> **A máscara `zona0` está no foco ORIENTAL. A Zona 0 do gestor é o foco
> OCIDENTAL.** Forma G, e a `CLAUSULAS` já a tinha aberta: *«a designação dos
> focos invertida por quatro auditorias».*

### O que isto derruba, e é muito

- **Toda a leitura do SAR de hoje** usou a `zona0` como **unidade primária** e
  chamou-lhe repetidamente «a unidade». As medições estão certas — são de um
  polígono geográfico fixo — mas **descrevem o foco oriental**, e o texto diz
  Zona 0. Corrige-se o **nome**, não os números.
- **O mesmo para o facto C2**, para o critério P3, e para o `AUD17`.
- **E inverte a leitura das análises de solo de 2025:** são da Zona 0 = foco
  **OCIDENTAL**, «onde tudo começou», e não da unidade que eu tenho vindo a medir.

**Acção: a máscara passa a chamar-se `foco_oriental` em toda a prosa nova, e as
páginas existentes levam nota.** Não se renomeia o ficheiro — renomear
partia vinte consumidores — mas nenhuma frase nova lhe chama Zona 0.

## 3 · O B1 foi cortado à base e enxertado DUAS vezes. **Não é comparador.**

> **Gestor:** *«b1 had varietal changes»* · *«valves 2,3,4,5 — summerkiwi base,
> cut in 2016, grafted with enza gold until 2020 more or less and then cut again
> and grafted with erica»* · *«b1 is valves 1,2,3,4,5»*

**Quatro das cinco válvulas do B1 foram cortadas à base e reenxertadas em 2016 e
outra vez por volta de 2020.** Duas descontinuidades estruturais, por
construção, no meio da série.

O B1 foi usado neste processo como **comparador** — a COMP-01 da Camada 5 era uma
condição de arranque baseada nele, e o `b1_como_unidade.py` mediu-o como unidade.
O Controlo 3 já lhe tinha tirado o estatuto de comparador por não ter
instrumentos independentes; **este testemunho fecha a questão por outra via e de
forma mais forte: uma unidade cortada à base duas vezes não tem linha de base.**

> **Qualquer leitura da série do B1 anterior a ~2021 mede enxertos diferentes.**
> É a condição 5 do portão — identidade da unidade no tempo — falhada por
> testemunho, não por cálculo.

## 4 · Plantações de 2008 a 2025 — e o `nu2021` pode ser plantação nova

> **Gestor:** *«the orchard grew and had changes. plantings from 2008-2025»*

O adversário do `AUD-17` tinha suspeitado, da ortofoto sem folha de 2025, que o
`nu2021` — a **âncora baixa de todo o caso**, o «chão lavrado de 2021» — lê
**34 % de fiadas brilhantes, a mais alta de todas as unidades, acima da própria
referência**, com altura LiDAR de 0,09 m. Fiadas instaladas, sem copado.

**O testemunho torna isso plausível em vez de especulativo:** houve plantações
até 2025. Um talhão lavrado em 2021 pode estar plantado em 2025.

Se se confirmar, explica de uma vez: os 15,2 % que o cabeçalho do
`altura_copado` diz que deviam ser zero; o colapso das âncoras do `p1` em 2025
(REF p25 +0,270 contra NU21 p75 +0,404); e o IX-04, o degrau de nível de +0,48 e
+0,70 dB no `nu2021` em 2021.

**Ainda não é facto — é hipótese com testemunho a favor.** Fecha-se com uma
pergunta ao gestor: *o talhão do `nu2021` foi plantado, e quando?*

## 5 · A PSA e a Phytophthora — o que está confirmado e o que não está

> **c) A detecção de *Phytophthora sojae* em 2023 chegou a ser confirmada por um
> laboratório de diagnóstico?**
> **Gestor:** *«O que tenho confirmado, foi o que lhe enviei.»*

**Não houve confirmação por laboratório de diagnóstico.** A detecção existe
apenas na metagenómica da Becrop. Isso não a apaga — mas fixa o seu estatuto, e
é o mesmo que a `LISTA_FINAL` exige: metagenómica não é diagnóstico.

E a melhoria entre os dois relatórios **tem causa declarada e não é artefacto de
amostragem**:

> **Gestor:** os dois relatórios são *«dos mesmos pontos e do mesmo sector»*, e a
> melhoria deve-se a *«aplicação de tricodermas e húmus líquido»*.

**Houve intervenção entre Agosto de 2023 e Fevereiro de 2024.** Isso é um
acontecimento datado no meio da série, e nenhuma análise nossa o tinha.

## 6 · A Becrop é a válvula 27 = B3C3. E o problema é em B2 e B3.

> **Gestor:** *«becrop analysis = valve 27»* · *«problem is in b2 and b3»*

A válvula 27 é o **B3C3**, 14 000 m². E os dois focos que o processo mediu caem
exactamente onde o gestor diz que está o problema: o ocidental em **B2**
(válvulas 8-9), o oriental em **B3** (13-14).

**Os dois focos são reais e são os certos. O que estava errado era o nome de um
deles.**

## 7 · Textura do B2-V7 — resolvido, e a resposta é a terceira

> **Gestor:** mesma parcela V7, **provavelmente não nos mesmos pontos**, e
> *«franco-argiloso deve considerar»*.

O conflito «Franca» (03-03-2026) contra «Argilosa» (17-06-2026) **não é erro de
talhão**: é variabilidade dentro da parcela. **A leitura a usar é
franco-argiloso.**

## 8 · Os perfis de solo ainda não foram abertos

> **Gestor:** *«Ainda não fiz.»*

Fica na fila, e é a única coisa desta página que ainda pode mudar a etiologia.

## 9 · O que fica por perguntar, e é curto

1. **O talhão do `nu2021` foi plantado? Quando?** — fecha a âncora baixa de todo
   o caso (§4).
2. **O bloco oriental (B3, válvulas 13-14) foi arrancado? Quando? Replantou-se?**
   — é a maior condição aberta, e o testemunho resolve-a onde quatro
   instrumentos não conseguiram.
3. **A aplicação de tricodermas e húmus foi só no sector da Becrop (B3C3) ou
   noutros?** — determina se há uma intervenção não modelada nos focos.
