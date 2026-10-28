# Pré-registo · georreferenciação do esquema de rega

**06-09-2026.** Escrito **antes** de olhar para a imagem e antes de qualquer
ajuste, como a C9 exige. A C9 já foi violada duas vezes neste processo, as duas
por eu correr primeiro e escrever o critério depois.

---

## 1 · A pergunta, fixada

> Qual é a transformação da página do `Esquema de rega retificado.pdf` para
> ETRS89/UTM 29N (EPSG:32629), e onde ficam as **válvulas 1 a 27**?

Unidade de análise: **a válvula**, ponto. Fronteira: a folha única do PDF.
Termos: «posição» é o centro do símbolo de válvula tal como desenhado.

## 2 · O que já está estabelecido, e não se remede

- O PDF é **A4** (`MediaBox` 842 × 596 pt = 297 × 210 mm) — redução do A1
  original. A redução A1→A4 é 1/(2√2) = 0,353553.
- A escala declarada é **1:3500 em A1**, logo **1:9899 na página A4**.
- A imagem embebida é **2338 × 1654 px**, que numa A4 são **200 dpi** exactos.
- Daí, **1 px embebido = 1,2572 m no terreno**; num varrimento a 400 dpi,
  0,6286 m/px.

Isto é aritmética sobre metadados do ficheiro, não é medição. Não depende de
nada que eu vá ver a seguir.

## 3 · O método, fixado antes de correr

1. Extrair a imagem embebida, sem reamostragem.
2. Identificar **pontos de controlo** — feições presentes no desenho **e** no
   parcelário IFAP 2025, que é a fonte independente.
3. Ajustar uma **semelhança** (escala isotrópica, rotação, translação) por
   mínimos quadrados. Semelhança e não afim: a afim tem dois factores de escala
   e absorve o erro de escala em vez de o expor, que é precisamente o que aqui
   se quer medir.
4. Aplicar a transformação a todas as válvulas.

## 4 · A CEGUEIRA, e é o que dá poder ao teste

**As válvulas 1 a 5 — o lobo oeste — NÃO entram no ajuste.** Nenhum ponto de
controlo é retirado do lobo. Elas são o **teste fora da amostra**, e o polígono
B1 do IFAP que as julga não partilha nada com o desenho de rega.

É a condição do `CLAUDE.md`: nenhum facto passa verificado só pelo instrumento
que o produziu.

## 5 · Os critérios. Todos têm de passar, e bloqueiam sozinhos

| | critério | limiar | de onde vem o limiar |
|---|---|---|---|
| **A** | escala ajustada contra a declarada | dentro de **±3 %** de 1,2572 m/px | a escala declarada é independente do ajuste |
| **B** | RMSE dos resíduos nos pontos de controlo | **≤ 25 m** | é a incerteza que o próprio `valvulas_v4.json` declara para o corpo |
| **C** | válvulas 1–5 dentro do polígono B1 | **≥ 4 de 5** | teste fora da amostra, instrumento independente |
| **D** | RMSE de validação cruzada *leave-one-out* | **≤ 40 m** | não pode degradar-se mais de ~60 % fora da amostra |
| **E** | número de pontos de controlo | **≥ 6**, e não colineares | uma semelhança tem 4 parâmetros; 6 dá redundância |

**Se algum falhar, o resultado NÃO se publica e a matéria não fecha.** Escreve-se
o que falhou. Um resultado que falha um critério pré-registado não é um resultado
mau — é um resultado, e é o único tipo que este processo aceita.

## 6 · O que falsifica a hipótese da escala

A hipótese é *«o desenho está à escala declarada e o erro era nosso»*. Falsifica-a:

- o critério **A** falhar, ou seja a escala ajustada afastar-se mais de 3 % da
  declarada — nesse caso o desenho está mesmo fora de escala e eu estou errado;
- o critério **C** falhar com **A** a passar — nesse caso a escala está certa mas
  a colocação do lobo tem um segundo erro que a escala não explica, que foi
  exactamente o que a corrida anterior indicou.

**As duas hipóteses fazem previsões diferentes, e o teste separa-as.**

## 7 · O adversário

Corre **depois** do resultado, vê este documento **antes**, e tem mandato de o
partir. Perguntas que lhe são postas, e são estas e não outras:

1. Algum ponto de controlo foi escolhido *depois* de se ver o resíduo?
2. Algum ponto de controlo cai no lobo, ou perto dele, contaminando a cegueira?
3. A semelhança foi trocada por afim a meio, para melhorar o ajuste?
4. Os limiares desta tabela são os mesmos que aqui estão escritos?
5. O B1 do IFAP tocou no ajuste de alguma forma?
6. A escala «declarada» foi derivada de alguma coisa que o ajuste também usa?

## 8 · O que este teste NÃO fecha

Não valida a **identificação** dos símbolos de válvula na imagem — que número
está em que sítio. Isso é leitura visual por um só leitor, forma G, e continua
sem guarda mecânica. Fecha a **geometria**, não a **rotulagem**.
