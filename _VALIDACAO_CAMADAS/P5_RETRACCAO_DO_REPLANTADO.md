# P5 — RETIRO o «foco oriental foi replantado». Não há prova de arranque.

**Data:** 31-08-2026 · **Retira:** `P3_ORIENTAL_REPLANTADO.md`, §2 e §3.
**Motivo:** duas verificações que eu devia ter feito antes de concluir, e que a
instrução de manter a auditoria robusta obrigou a fazer.

---

## 1 · O QUE EU CONCLUÍ, E COM QUE

Escrevi que o ORI-COM foi **replantado**, a partir de **uma só coisa**: a
prominência de pérgola caiu de 111 % (2010) e 79 % (2012) para 14 % (2021).

Não confrontei essa leitura com mais nada. É a definição do erro que este
projecto tem escrito na sua própria `CLAUDE.md`: **nenhum facto passa verificado
só pelo instrumento que o produziu.**

## 2 · A PRIMEIRA VERIFICAÇÃO — o NDVI não tem cova nenhuma

Nível absoluto do ORI-COM, Sentinel-2:

| 2017 | 2018 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| 0,824 | 0,879 | 0,857 | **0,835** | 0,845 | 0,852 | 0,843 | 0,756 | 0,693 |

E o Landsat, desde 2013: 0,780 · 0,826 · 0,801 · 0,831 · 0,853 · 0,841 · 0,827 ·
0,850 · 0,850 · 0,831 · 0,835 · 0,812 · 0,769 · 0,728.

**Neste pomar, chão nu lê 0,49 a 0,61** (a série do `NU21`). **Um arranque
seguido de replantação deixa uma cova de vários anos.** Em treze anos de duas
constelações não há cova nenhuma: o ORI-COM está entre 0,78 e 0,88
continuamente até 2024, e só depois cai.

**Isto sozinho é incompatível com um arranque entre 2012 e 2021.**

## 3 · A SEGUNDA VERIFICAÇÃO — em 2021 o instrumento já não mede pérgola

O método procura o pico da autocorrelação radial **só na janela de 4,0 a 6,2 m**,
porque foi assim que o compasso do pomar foi medido. Nunca ninguém perguntou
**onde o pico realmente está**. Perguntei:

| unidade | pico em **2012** | pico em **2021** |
|---|---|---|
| REF · referência, tem pérgola de certeza | **5,25 m** | **9,88 m** |
| RESTO · resto do pomar | **5,25 m** | **9,88 m** |
| ORI-COM | **5,25 m** | 2,12 m |
| ORI-SEM | 2,25 m | 2,12 m |

> **Em 2021, a própria referência — que tem pérgola de certeza — já não tem o
> pico no compasso da pérgola.** Move-se de 5,25 m para 9,88 m.

Logo, na ortofoto de 2021, **a medida não está a medir a periodicidade da
pérgola em unidade nenhuma**. O adversário da C2 já tinha levantado que a
prominência colapsa entre épocas por um factor de cinco; a C2 defendeu-a
mostrando que ela ainda *separa* dentro de 2021 — e separa. **Mas o que separa
já não é «tem pérgola contra não tem».**

**O meu 14 % do ORI-COM em 2021 não é interpretável.** E era a única prova do
arranque.

## 4 · O QUE FICA DE PÉ

**Confirma-se, e é sólido:**
- **ORI-COM tinha pérgola madura em 2010 (111 %) e 2012 (79 %)**, com o
  instrumento a discriminar em ambas (IQR das âncoras disjuntos) e com o meu
  caminho de código a **reproduzir os mapas certificados da C2 a diferença
  máxima 0,00e+00** em 2 858 células.
- **ORI-SEM nunca teve pérgola:** pico a 2,25 m em 2012 e 2,12 m em 2021, longe
  do compasso, e 8 % de posição em 2012 com o instrumento bom.
- **O ORI-COM tem cobertura verde contínua de 2013 a 2024**, sem interrupção.

**Cai:**
- «o foco oriental foi replantado»;
- «o degrau de 2025-26 está a acontecer sobre uma replantação com menos de
  quatro anos»;
- e com elas, a reformulação que eu tinha proposto para o D1 da C4 e a unidade
  nova que tinha proposto para a campanha da C5.

**Volta a valer a leitura anterior:** a metade oriental com pérgola é copado
adulto, plantado com o resto do pomar entre 2007 e 2010, que **declinou em
2025-26**.

## 5 · AS ORTOFOTOS DE 2004 E 2007 — corridas, e não decidem

| época | resolução | âncoras (REF · NU21) | discrimina? |
|---|---|---|---|
| 1995 | 1 m, IRG | −0,0503 · −0,0730 | **não** |
| 2004-06 | 50 cm | −0,0467 · −0,0478 | **não** |
| 2007 | 50 cm | −0,0348 · −0,0420 | **não** |
| 2010 | 50 cm | +0,2530 · +0,0578 | sim |
| 2012 | 50 cm | +0,2199 · −0,0173 | sim |

Em 1995, 2004-06 e 2007 **a prominência é negativa em todas as unidades,
incluindo a referência** — não há periodicidade de 5 m em lado nenhum do
polígono. O instrumento não falha por qualidade de imagem: falha porque **a
âncora é falsa nessas datas**, ou seja **ainda não havia pérgola em sítio
nenhum**.

Isso é **consistente** com o que a C0 já tinha certificado — «coorte de
plantação: implantado entre 2007 e 2010» — e acrescenta que o ORI-COM foi
plantado **com o resto do pomar**, não antes nem depois.

## 6 · QUANDO FOI ARRANCADA — a resposta é que não foi

A pergunta assentava no meu erro. **Não há evidência de arranque**, e há treze
anos de cobertura verde contínua contra ele.

O que existia de estranho — a queda de prominência entre 2012 e 2021 — explica-se
pelo instrumento, não pelo terreno: em 2021 nem a referência tem o pico no
compasso da pérgola.

**Fica em NÃO TESTÁVEL, com o teste nomeado:** se se quiser mesmo saber se houve
alteração de estrutura entre 2012 e 2021, o caminho não é a prominência na
janela fixa — é o **perfil radial completo por unidade**, comparado dentro de
cada imagem, que é o que este ficheiro passou a fazer e que ninguém tinha feito.

---

## 7 · A NOTA QUE INTERESSA MAIS DO QUE O RESULTADO

Este é o **segundo veredicto meu retirado em duas mensagens**, e os dois pela
mesma razão: **conclui a partir de um instrumento só, sem o confrontar.**

O caso do lóbulo oeste que abriu esta cadeia foi exactamente isto. O
`fazer_masks_v2.py` foi exactamente isto. O S9 do B1, que o Controlo 3 derrubou
há uma hora, foi exactamente isto.

**A regra existe, está escrita na `CLAUDE.md` do projecto, e eu violei-a três
vezes em três dias.** O que a apanhou desta vez não foi um adversário: foi a
instrução de manter a auditoria robusta antes de eu ter acabado de escrever.
