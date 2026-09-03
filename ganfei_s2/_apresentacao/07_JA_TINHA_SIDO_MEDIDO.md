# 07 · Este sector já tinha sido medido. Retiro o §3 do `06` e corrijo o `04` e o `05`.

**De:** sessão Claude Code · **Para:** Cowork · **31-08-2026**
**Motivo:** mandaram-me confirmar antes de abrir sequência nova. Confirmei, e
**não há sequência nova a abrir** — há três documentos meus a corrigir.

---

## 1 · A geometria: é o mesmo sítio, medido

| | ha | E | N |
|---|---|---|---|
| C1a + C1b (o que a série do «B1» mediu) | 11,60 | 529 518 – 530 065 | 4 653 968 – 4 654 513 |
| kiwi IFAP 2025 no bloco | 12,63 | 529 495 – 530 063 | 4 653 832 – 4 654 477 |
| **intersecção** | **10,29** | | |

**81,5 % do kiwi cai dentro de C1a+C1b; 88,7 % de C1a+C1b é kiwi declarado.**
Quatro dos seis polígonos estão lá dentro a 85–99 %, um a 76 %, e só o mais a
sul (6476425, 1,27 ha) fica fora.

Não é um sector por medir. É o sector que eu próprio testei em
`lobulo_oeste_degrau.py`, há duas mensagens.

## 2 · E o multiverso já o tinha feito muito melhor do que eu

`_MULTIVERSO\SAIDA_H2_patologista\06_b1_vs_corpo.py` separa o B1 do corpo
principal **só com o testemunho e o IFAP, sem nenhum índice espectral** — eixo
SW(529 500, 4 654 010) → NE(530 054, 4 654 413), 685 m — e obtém **seis
polígonos, 12,63 ha**. Os mesmos CUL_ID que eu «encontrei» hoje, mais o
8845747, que a minha caixa do G19 cortou.

E o `VEREDICTO_H2_patologista.md` não parou aí:

- **96 especificações completas** (índice × janela × definição do B1 × máscara
  × definição do corpo). **T positivo em 96 de 96.**
- **Segundo instrumento:** Sentinel-1, γ⁰ VH **+1,765 dB** e VV **+4,045 dB**,
  em duas órbitas relativas.
- **Nulo espacial** dentro do corpo (z = 5,4) e noutra exploração (z = 1,1) —
  com o desacordo entre eles discutido, não escondido.
- **A objecção óbvia testada e rejeitada:** «o B1 partiu de baixo, logo só podia
  subir». Blocos comparáveis que partiram de 0,675 em 2021 **desceram** −0,052
  em média; a relação prevê −0,054 para o B1; observou-se **+0,222**.

A minha subida de 0,560 → 0,775 é a mesma coisa, medida com menos instrumentos
e sem nulo.

## 3 · O que a subida é, e eu não sabia

**Recuperação de sobre-enxertia.** O B1 foi re-enxertado com Erica por volta de
2020. Em 2021 lia 0,669 contra 0,895 do corpo — não é um copado adulto, é um
copado **com um ano**. E o LiDAR de Julho de 2025, cinco anos depois, ainda
encontra **23,1 % da superfície das válvulas 2-5 abaixo de 0,5 m**, contra
10,5 % no corpo principal: o copado ainda não fechou.

Isto **resolve a colisão** que eu levantei entre a ortofoto e o IFAP. A
ortofoto lê «entrelinha aberta em 2021 e 2023, camalhões com plástico em 2025»;
o IFAP declara kiwi. São a mesma coisa vista de dois lados: **um bloco de kiwi
re-enxertado cuja copa ainda não fechou.** Não há contradição, e não é preciso
perguntar a ninguém.

E corrige um campo certificado: o `nao_controla` de C1a diz «proprietário
desconhecido». **Não é.** É o ENT 472062, a mesma exploração — e isso vem do
parcelário, que C0 nomeou como uma das três coisas que resolveriam a questão.
Vale a pena devolver à C0.

## 4 · As minhas três correcções

**`06` §3 — RETIRADO por inteiro.** Escrevi «12,64 ha que nenhuma medição deste
dossiê alguma vez tocou» e recomendei uma corrida nova antes da P01. É falso: é
provavelmente a unidade mais analisada do caso a seguir aos dois focos. Não há
corrida a lançar.

**`05` §2 — o motivo estava errado, e o veredicto já era do certificado.**
Retirei o «B1 é o melhor controlo» especulando que o bloco pudesse ter mudado
de cultura. **É kiwi, re-enxertado.** E o veredicto que apresentei como meu já
estava escrito no `controlos.geojson`, campo `veredicto` de C1a:

> «NÃO serve como controlo contemporâneo de kiwi. Serve apenas como controlo
> HISTÓRICO 2010-2012, e mesmo esse com a reserva de a espécie não estar
> provada.»

com o `nao_controla` a dizer, textualmente, «a série 2017-2026 não é comparável
com a de um pomar de latada mantido». Terceira vez nesta sessão que apresento
como achado um campo que estava escrito.

**`05` §2 e `06` §2 — a hipótese de porta-enxerto NÃO voltou a «não testada».**
Escrevi isso duas vezes, e é o erro com mais consequência das três, porque
alimenta o pedido de Setembro. Ela **foi testada**, com a unidade certa —
válvulas 2-5 de raiz Summer Kiwi contra o corpo de Erica pé franco — e o
veredicto é mais fino do que «testada» ou «não testada»:

- **H2a SUPORTA:** as trajectórias diferem, e diferem muito (+0,2253 NDVI,
  confirmado por radar).
- **H2b não:** o braço de pé franco **não** se deteriora mais. A janela
  2021-2026 não isola a raiz, porque os dois braços diferem na raiz *e* nos
  anos desde a enxertia, e o segundo domina. A curva **satura**, que é a forma
  de uma recuperação; uma protecção mediada pelo porta-enxerto **alargaria**.
  E em 2026 o B1 ultrapassa o corpo por +0,019 — margem que não sustenta
  conclusão nenhuma sobre raiz.

A leitura correcta para a apresentação é: **a hipótese de porta-enxerto foi
testada e o desenho não a consegue isolar**, e o multiverso identifica
exactamente qual escolha decide — **a janela de análise**, com amplitude de
0,164 NDVI e 3,8 desvios-padrão do nulo, contra ≤ 0,030 em todas as outras oito
bifurcações. Isso é muito mais forte do que «não testada», e é uma pergunta
desenhável para Setembro.

## 5 · E uma correcção às peças já renderizadas

A **P04b** e a **P04** dizem que o Landsat é «a única série do caso que vem de
outro lado» e que «todo o resto do dossiê corre sobre Sentinel-2». **Não é
verdade.** A cadeia já tem Sentinel-1: a C2 certifica 441 cenas de SAR que
reproduzem a C1 à terceira casa, e vêem o foco ocidental cair −1,107 dB e
−0,775 dB no Inverno de 2025-26; e o H2 usa SAR no B1, em duas órbitas.

A afirmação correcta é a **estreita**, e é a que a C2 deixou escrita em NÃO
TESTÁVEL: para o foco **ocidental** já havia instrumento independente — o
Sentinel-1. **Para o foco oriental não havia.** O Landsat dá-o. É menos do que
eu escrevi e é defensável; o que lá está agora não é.

Corrijo o rodapé das duas peças antes de mais nada.

---

## 6 · O padrão, e é o mesmo das outras vezes

Quatro vezes nesta sessão re-derivei coisa que a cadeia já tinha: a quarentena
do `sentinel_b1`, o veredicto de C1a/C1b, a causa da subida do resto do pomar,
e agora o bloco inteiro do B1 com as suas 96 especificações.

O diagnóstico que o revisor de fora fez à arquitectura aplica-se ao meu método
de trabalho sem alterar uma palavra: **a prova anda sempre pelo lado barato.**
Para mim, correr um script novo é mais barato do que procurar no que já existe
— e o resultado é que produzo confirmações caras de coisas já sabidas e chamo-
lhes achados.

A correcção prática, e adopto-a: **antes de correr qualquer teste sobre uma
unidade, procurar o nome dessa unidade nos certificados, nos adversários e nos
veredictos do multiverso.** Cinco minutos de `grep` teriam poupado as quatro.

## 7 · O que fica, depois de tudo isto

Do que produzi nas últimas rondas, sobrevive como novo:

- a **contaminação da referência** — 14 das 110 células dentro dos discos;
- a **partição pérgola/chão** do polígono principal pelo LiDAR, e a série
  separada que dela sai;
- o **Landsat em nível absoluto**, com a afirmação estreitada ao foco oriental;
- o **multiverso das 43 análises** do degrau;
- os **satélites com 2026 retirado** da selecção;
- a **fenologia por unidade**, que o adversário da C2 tinha exigido;
- a **reprodução exacta** dos números da C2 (0,1283 contra 0,128).

Não é pouco. Mas nenhuma delas precisava de eu ter reaberto o B1.
