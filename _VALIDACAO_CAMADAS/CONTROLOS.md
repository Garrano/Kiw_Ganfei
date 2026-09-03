# Controlos da cadeia

Adenda ao `PROTOCOLO.md`. Escrita em 28-08-2026, depois de a C0 já ter
arrancado — por isso está em ficheiro próprio, para não mexer no protocolo
que a sessão em curso está a usar. **Aplica-se a partir da C1**, e à revisão
adversarial da C0, que corre depois de ela devolver.

## Porque não duplicamos as sessões

A hipótese óbvia era correr cada camada duas vezes em paralelo e comparar os
valores. Não se faz, e a razão é o erro que motivou esta cadeia.

Duas sessões com o mesmo prompt, os mesmos dados e o mesmo vocabulário cometem
erros **correlacionados**. Uma segunda sessão teria olhado para uma pasta
chamada `sentinel_b1/`, um ficheiro `expansao_b1.csv` e um script
`b1_serie.py`, e teria concluído exactamente o mesmo: que aquilo era B1. Os
valores bateriam certo ao decimal, e ambas estariam erradas.

A duplicação apanha lapsos de execução. Não apanha premissas falsas
partilhadas — que é a classe de erro que já custou semanas a este processo:
o B1, o *P. sojae* atribuído ao corpo em declínio, a classificação de «falha
de copado» sobre pomar plantado.

E repare-se em como esses foram apanhados: nenhum por recomputação. Todos por
**ir a um instrumento diferente** — a imagem RGB, a ortofoto a 25 cm, uma
vista de satélite trazida pela gestora. A informação nova veio de fora do
cálculo. É isso que os controlos abaixo tentam institucionalizar.

## Controlo 1 — regra do instrumento independente

**Nenhum facto entra na secção PASSA PARA CIMA se só foi verificado com o
mesmo instrumento que o produziu.**

Um valor de NDVI não se confirma com outro cálculo de NDVI. Confirma-se contra
a ortofoto, contra o SAR, contra a fotografia de campo, contra um documento, ou
contra observação directa. Uma área medida em píxeis confirma-se contra o
cadastro ou contra a ortofoto, não contra a mesma máscara recontada.

Cada facto certificado leva, além da prova, o **instrumento de confirmação**:

```
facto | ficheiro e cálculo | INSTRUMENTO INDEPENDENTE usado | margem
```

Se não houver instrumento independente disponível, o facto vai para NÃO
TESTÁVEL, não para PASSA PARA CIMA. Esta regra, sozinha, teria apanhado o B1
no primeiro dia: bastava ter aberto a imagem RGB da AOI.

## Controlo 2 — quantidades-âncora

Um punhado de valores que **todas** as camadas reportam, sempre, na mesma
secção do certificado, mesmo que não lhes tenham tocado. Divergência entre
camadas salta sem ninguém comparar nada à mão.

Os valores abaixo são os **declarados** à data de abertura da cadeia. Não são
verdade estabelecida: a C0 está precisamente a verificá-los. Cada camada
reporta o valor que obtém, e assinala se difere do declarado.

| Âncora | Declarado | Unidade |
|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | EPSG:32629 |
| polígono `pomar` | 2903 | píxeis de 10 m |
| polígono `pomar` | 29,0 | ha |
| referência sã (3 manchas) | 454 | píxeis |
| máscara `manchaW` | 427 | píxeis |
| máscara `zona0` | 220 | píxeis |
| cenas na série | 11 | datas |
| cenas de plena estação | 9 | datas |
| NDVI médio da referência, 2017-07-02 | 0,838 | — |
| NDVI médio da referência, 2026-07-27 | 0,886 | — |

Há um conflito conhecido nesta tabela: contagens de máscara booleana
(2906 / 446 / 423 / 219) circularam na prosa em vez das do polígono. Se a
tua camada obtiver os valores booleanos, di-lo — não os corrijas em silêncio.

## Controlo 3 — adversário do certificado

Nas camadas com raio de explosão grande — **C0 e C2** — corre uma sessão
paralela **depois** de o certificado estar escrito, cujo único trabalho é
atacá-lo. Não recalcula nada e não vê os dados brutos.

Só C0 e C2 porque um erro nelas contamina tudo o que vem acima. Um erro em C5
estraga uma recomendação e vê-se de imediato; não justifica o mesmo escrutínio.

O prompt do adversário está em `ADVERSARIO_PROMPT.md`.

## O que fica de fora, e porquê

**Não se duplica nenhuma camada.** Ver acima.

**Não se corre adversário em C1, C3, C4, C5.** A C4 (inferência) é a tentação
óbvia, mas ela já é, por construção, uma camada crítica: recebe factos e
testa-os. Pôr-lhe um adversário é pôr um crítico a criticar um crítico, e o
custo não se justifica quando as fundações abaixo já foram atacadas.

**Não se compara «valores no fim de cada etapa» entre sessões**, porque grande
parte do produto de cada camada é juízo — «esta máscara é defensável?» — e
juízo não se compara por diferença numérica. O que se compara são as
quantidades-âncora, que são poucas e são números.
