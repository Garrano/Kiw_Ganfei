# Resultado · escala do esquema de rega

**06-09-2026.** Critério em `PRE_REGISTO_ESCALA_REGA.md`, escrito antes de
qualquer corrida. Este documento diz o que passou e o que não passou.

---

## 1 · O que FECHA, e é aritmética sobre metadados

**O desenho está à escala declarada. O erro era nosso.**

| | |
|---|---|
| `MediaBox` do PDF | 842 × 596 pt = **297 × 210 mm** → é **A4** |
| imagem embebida | **2338 × 1654 px** → numa A4, **200 dpi exactos** |
| cartucho do desenho | **«1/3500 @ A1»** — lido no próprio desenho |
| redução A1 → A4 | 1/(2√2) = 0,353553 |
| escala efectiva na página | **1:9899** |
| **terreno por píxel embebido** | **1,2572 m** |
| **terreno por píxel a 400 dpi** | **0,6286 m** |

> **A frase que aqui estava — «não é medição, qualquer pessoa a refaz em dois
> minutos» — foi retirada pelo adversário, e com razão.** A conta assume que a
> folha A1 INTEIRA mapeia na página inteira. A moldura desenhada mede
> 1555,9 × 2229,7 px = 197,60 × 283,17 mm, razão de forma **1,4331**; a folha A1
> inteira daria 1,4158 e margens de 10–15 mm dariam 1,4303 e 1,4379. A hipótese
> assumida é a de **pior** ajuste do conjunto, e a banda que daí vem é de
> **−0,4 % a +5,6 %**. A aritmética não fecha sozinha.

**O que fecha é a concordância de três instrumentos independentes**, e é isto
que se cita, não a aritmética:

| origem | m/px (quadro embebido) | desvio |
|---|---|---|
| declarada — cartucho + `MediaBox` | 1,2572 | — |
| ajuste de forma do `c0_13` | 1,2435 | −1,1 % |
| **calibre do adversário contra o parcelário IFAP** | **1,2680** | **+0,9 %** |
| nota de retirada do `escala_do_desenho.py` | 1,263 | +0,5 % |

Três medições, todas dentro de ±1,1 %, e a do adversário é invariante a rotação
e translação — mede calibre, não emparelha pontos. **É esta a prova.**

E um facto de metadados que sobreviveu mais forte do que eu o tinha posto: a
matriz do XObject é `(841,680 · 0 · 0 · 595,440 · 0 · 0,560)`, ou seja
11,6900 × 8,2700 polegadas **exactas** — logo 2338/11,69 = **200,0000 dpi** e
1654/8,27 = **200,0000 dpi**. Os 200 dpi não são inferidos do tamanho da página:
saem da área que a imagem realmente ocupa, e dão exactos nos dois eixos.

### O que isto retira

O `valvulas_v4.json` afirma que *«o desenho NÃO está à escala declarada»*.
**Retirado.** E o mais notável é que o próprio ficheiro tinha o número certo:
diz que 1:3500 daria **0,629 m/px** — que é exactamente o valor correcto a
400 dpi, com a redução A1→A4 já dentro. Calculou bem e depois descartou-o a
favor de um «ajuste ancorado» de 0,788.

| | m/px | erro face ao correcto |
|---|---|---|
| **correcto (400 dpi)** | **0,6286** | — |
| `valvulas_v4.json`, ajuste ancorado | 0,7880 | **+25,4 %** |
| `valvulas_v6.json` | 0,6734 | **+7,1 %** |

> **CORRIGIDO pelo adversário, 06-09.** Eu tinha escrito aqui que *«o campo
> chama-se `m_por_pixel_400dpi` e contém um valor que não corresponde a 400 dpi
> nenhuns — foi o nome que escondeu o erro»*. **É falso, e mandava a próxima
> sessão para o sítio errado.** O adversário reconstruiu a ancoragem: os
> centróides dos círculos manuscritos v6 (1052,0 · 362,2) e v17 (1968,1 · 561,6)
> distam 937,6 px a 200 dpi = 1875,2 px a 400 dpi; o v4 atribui a esse vão os
> 1457,5 m do `valvulas_por_linha.json`, o que dá **0,7773 m/px a 400 dpi** —
> reproduz o 0,788 a 1,4 %. **O valor está no quadro que o nome declara. O campo
> está bem nomeado.**
>
> **A causa verdadeira é outra e é pior:** os círculos 6 e 17 cobrem **80,5 %**
> do talhão (937,6 px de 1164,2). O v4 esticou o comprimento inteiro da parcela
> sobre um vão que é quatro quintos dela — 1164,2/937,6 = **1,242, ou +24,2 %**.
> **O número estava certo; o diagnóstico estava errado.**

## 2 · O que NÃO fecha, e as duas corridas que falharam

A georreferenciação completa das válvulas **não fechou**. Duas corridas, ambas
falhadas em **pré-condição**, antes sequer de os critérios A–E poderem ser
avaliados.

**Corrida 1** — máscara dos sectores coloridos, fecho morfológico 9 × 9.
Partiu-se em **11 componentes**: os sectores estão separados por traço preto e
papel branco, e a «componente maior» era um sector isolado, não o corpo do
pomar. O ajuste que se seguiu (escala −25 %, rotação −40,8°, teste cego 0 %)
mede uma coisa sem sentido e **não conta como resultado**.

**Corrida 2** — fecho 21 × 21 e preenchimento de buracos. Melhorou, e revelou
o erro de fundo: **os sectores coloridos não são o pomar.** Muitas parcelas
ficam por colorir no desenho; o corpo continua partido em dois grupos (válvulas
6–9 a azul, 12–16 a vermelho) porque as parcelas do meio não têm cor. Comparar
essa mancha com o polígono `banda` do IFAP é comparar entidades diferentes, e
nenhum ajuste sobre ela significa o que quer que seja.

> **Parei aqui, e a razão importa.** A referência correcta seria a linha fina
> «Limites do terreno» da legenda — mas essa é vermelha, e os círculos
> manuscritos das válvulas também. Separá-las é trabalho a sério, não um
> afinamento. **Afinar uma terceira vez depois de ver dois resultados é escolher
> o caminho pelo resultado**, que é precisamente o que a literatura do
> multiverso descreve e o que este aparelho existe para travar.

## 3 · Estatuto de cada afirmação

| afirmação | estatuto |
|---|---|
| o desenho está a 1:3500 em A1, reduzido a A4 | **fecha** — cartucho + `MediaBox` |
| 0,6286 m/px a 400 dpi; 1,2572 m/px na imagem embebida | **fecha** — aritmética |
| o v4 está inflado +25,4 %; o v6 +7,1 % | **fecha** — aritmética |
| «o desenho não está à escala» | **RETIRADO** |
| posição correcta das válvulas 1–27 | **NÃO FECHA** — duas corridas falhadas |
| as válvulas 1–5 estão onde o v4 diz | **NÃO** — 662 m do B1 do IFAP |
| onde as válvulas 1–5 estão de facto | **desconhecido** |

## 4 · O que fecharia, e custa o que custa

Por ordem de força:

1. **Leitura de campo com GPS** em meia dúzia de válvulas do corpo. Fecha tudo,
   é testemunho de tipo 1, e resolve de uma vez o v4-contra-v6.
2. **Extracção da linha «Limites do terreno»** separando-a do manuscrito, e
   ajuste de forma contra o parcelário. É tratável, mas é uma tarefa própria
   com pré-registo próprio — não a cauda desta.
3. **Pontos de controlo escolhidos à mão**, com o teste cego do lobo como
   guarda. Aceitável *porque* o teste cego não depende da escolha; mas é forma
   G na origem, e tem de ir com dupla leitura.

**Enquanto nenhuma correr, a incerteza de ~150 m fica declarada na legenda das
cartas, que é o que a P15 já faz.**
