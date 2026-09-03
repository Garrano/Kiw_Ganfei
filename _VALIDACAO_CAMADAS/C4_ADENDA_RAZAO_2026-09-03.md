# Adenda ao livro-razão da C4 — duas linhas corrigidas

**03-09-2026.** Corrige `SAIDA_C4\c4_razao_exclusoes.csv`, linhas **BIO-24**,
**BIO-25** e **INS-04**. **O CSV não é editado** — a convenção desta cadeia é que
um certificado se revê por documento novo, nunca em sítio. Quem ler o CSV tem de
ler isto ao lado.

---

## 1 · BIO-24 e BIO-25 — a PSA não é uma lacuna. É uma exclusão clínica.

**O que o livro-razão diz hoje:**

> BIO-24 · *Pseudomonas syringae* pv. *actinidiae* (PSA) e cancro bacteriano ·
> NÃO TESTADA · «NÃO EXISTE UMA ÚNICA LINHA BACTERIANA EM TODA A MATRIZ. O
> patógeno de referência do kiwi na Europa nunca foi procurado neste caso, com
> ou sem posição. **Isto não é um resultado negativo; é a ausência do ensaio.**»

**O que está errado:** a frase descreve um esquecimento. Não foi um esquecimento.

> ### **Testemunho de tipo 1, recebido em 01-09-2026**
> **Ninguém encomendou nem testou nada para PSA porque a sintomatologia das
> plantas não era compatível.**

Pela regra dos três tipos de facto da `CLAUDE.md`, isto é **testemunho directo**:
não é medição nem inferência, **entra como dado**, e ganha a qualquer cálculo
nosso. O que ele derruba não se reconcilia — retira-se.

**A redacção certa:** *PSA não ensaiada por **exclusão clínica**: a
sintomatologia observada no terreno não era compatível. A ausência da linha
bacteriana na matriz é **consequência de uma decisão**, não omissão.*

### O que este testemunho NÃO diz, e fica em branco à vista

| | |
|---|---|
| **quem observou** | **não sabido** |
| **quando observou** | **não sabido** |
| **que sintomas** foram considerados incompatíveis, e com que critério | **não sabido** |
| ficou escrito em algum lado à data? | **não** — é por isso que quatro documentos a trataram como lacuna |

**Não se preenche nenhum destes por inferência.** Um testemunho de tipo 1
corrige-se perguntando outra vez a quem sabe, não replicando.

**O que muda:** o **D6** da `LISTA_FINAL` deixa de ser «zero ensaios bacterianos»
como lacuna e passa a ser «zero ensaios bacterianos, por exclusão clínica
declarada, com o registo dessa decisão em falta». **O que a fecharia** deixa de
ser «um ensaio bacteriológico» e passa a ser **«a nota clínica: quem, quando, que
sintomas»** — e, se essa nota não existir, então sim, o ensaio.

**A ressalva que sobrevive, e é real:** a exclusão clínica é uma decisão de campo
tomada por sintomas, e a PSA tem formas pouco expressivas. Que a decisão exista e
seja legítima **não a torna verificada**. Fica em NÃO TESTÁVEL com o teste
nomeado, como qualquer outra coisa aqui.

---

## 2 · INS-04 — confirma-se, e é maior do que dizia; mas 60 % é o B6

**O que o livro-razão diz:**

> INS-04 · a referência sistemática está em declínio · SUSTENTADA ·
> «0,8884 → 0,8425, −0,00395/ano (…) média a cair 0,0548 contra 0,0219 da
> mediana, afastamento a alargar **31 vezes** — é um **subconjunto de células da
> referência a colapsar**, e não é sensor.»

Medido hoje em **301 cenas de Verão** (`ins04_media_contra_mediana.py`), nas
mesmas células:

| estatística | declive 2017-24 | declive 2017-26 | queda total |
|---|---|---|---|
| mediana | −0,00063 | −0,00158 | 0,020 |
| **média** | −0,00147 | **−0,00507** | 0,064 |
| **percentil 10** | −0,00357 | **−0,01614** | **0,198** |

Afastamento mediana−média: **+0,0001 (2017) → +0,0438 (2026)**. O T4 dizia 31×;
com 301 cenas são **724×**. **O INS-04 confirma-se e subestimava-se.**

### E a alternativa óbvia, testada antes de se concluir

O **B6** já tinha certificado que **18 das 110 células da referência caem dentro
dos discos dos focos**. O decil inferior são onze células. Logo o colapso do p10
podia ser, simplesmente, essas células.

| | 2017 | 2024 | 2025 | 2026 | queda |
|---|---|---|---|---|---|
| REF toda (110) | 0,8912 | 0,8564 | 0,7946 | 0,6931 | **0,198** |
| **REF limpa (92)** | 0,8924 | 0,8784 | 0,8835 | 0,8136 | **0,079** |
| REF dentro dos discos (18) | 0,8918 | 0,7987 | 0,6886 | 0,6101 | 0,282 |

> **Sessenta por cento do colapso são as 18 células contaminadas.** O INS-04 e o
> B6 estavam a descrever **o mesmo fenómeno** sem se citarem: o «subconjunto da
> referência a colapsar» é, na sua maior parte, o pedaço da referência que está
> geograficamente dentro dos focos.

**O que sobra é real e é menor:** a referência limpa perde **0,079** no seu decil
inferior até 2026, contra 0,020 na mediana. Quase tudo em 2026 (0,8835 → 0,8136).

### As consequências, e são três

1. **A conclusão operativa do INS-04 mantém-se e agora está medida:** toda a
   magnitude expressa como fosso à referência é um **limite inferior**. Não por
   asserção — por decomposição.
2. **A minha frase de ontem precisa de uma palavra.** «A referência passa o
   rastreio» é verdade **da mediana**, e a mediana é cega por construção a uma
   minoria de células a cair. `triagem_referencia_densa.py` mede medianas.
   **A lacuna 1 continua fechada** — não há descontinuidade na linha de base em
   nenhuma das três estatísticas — mas fecha-se com a estatística declarada.
3. **O que o INS-04 dizia que o fecharia não é possível.** Ele nomeia
   «certificar a série Landsat da referência — o único instrumento verdadeiramente
   externo». **O Landsat não resolve a referência:** 110 células de 10 m, **zero
   píxeis de 30 m** com o crivo de contenção. Está medido em
   `triagem_referencia.py`, e o próprio `landsat_independente.py` já escrevia que
   «a série da referência não deve circular de todo».
   **O teste que o INS-04 nomeia tem de ser substituído**, e o substituto óbvio é
   a ortofoto de 2025 sobre as 92 células limpas — outro instrumento, e resolve.

---

## 3 · O que isto acrescenta à fila

| | acção | custo | decide |
|---|---|---|---|
| **1** | pedir a **nota clínica da PSA** — quem, quando, que sintomas | nenhum | se a exclusão está documentada ou só lembrada |
| **2** | ortofoto de 2025 sobre as **92 células limpas** da referência | baixo | se o resíduo de 0,079 é copado a rarear ou é chão |
| — | ~~certificar a série Landsat da referência~~ | — | **impossível: o Landsat não a resolve** |
