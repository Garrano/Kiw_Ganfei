# Camada 5 — Decisão · re-execução R2

**Data:** 31-08-2026
**Herda:** C0 (+R2, +R3), C1, C2 (+R2, +adversário R2, +T1–T5), C3 (+R2, +R3),
C4 (+R2).
**Responde a:** `CAMADA_5_ADVERSARIO.md`, R1–R10, **que nunca tinham sido
respondidas.**
**Precedência:** pela emenda de 29-08 à regra 1, **onde o adversário discorda,
ganha o adversário.** As dez são aceites. O que segue é o que muda.

---

## 1 · AS DEZ RETIRADAS, ACEITES

| | o que cai | o que fica no lugar |
|---|---|---|
| **R1** | «a re-etiquetagem é uma re-derivação» — o código não lê os campos que o cabeçalho diz ler | é uma **re-classificação por regras sobre texto**, e chama-se assim |
| **R2** | «24 mal rotuladas, 11 encontradas» | **18 e 10 + 1** |
| **R3** | três exclusões | **duas.** A INS-01 não tem instrumento independente |
| **R4** | «ABI-04 · JÁ FECHADA» | ABI-04 é **categoria intermédia**, e lê-se como aberta |
| **R5** | o verbo «excluída» nas quatro EXCLUÍDA-LOCAL | **«sem suporte local»** — BIO-10 e BIO-11 não têm instrumento independente nenhum |
| **R6** | o transecto como prova de propagação | **não distingue propagação radial de mancha estática**, que era a única coisa que o justificava |
| **R7** | o painel foliar do §2.3 | **não existe no ficheiro.** `MATRIZES` tem quatro entradas e nenhuma é folha; 12 plantas × 4 = 48, zero folhas |
| **R8** | U2 com controlo suficiente | **U2 não tem controlo de proximidade.** O ocidental tem dois (T1c e U3); o oriental tem um, a 474 m e **noutro bloco** |
| **R9** | «a medição de paisagem estabelece com força o negativo» | é ao contrário: **o negativo é a parte fraca** |
| **R10** | REG-01 fora das condições de arranque | **REG-01 é a raiz da árvore, custa BAIXO, e passa a condição de arranque** |

**A R7 é a mais operacional, e corrige-se de uma de duas maneiras — não das
duas.** Ou a folha entra como quinta matriz e o orçamento passa de 48 para
**60 amostras**, ou o painel foliar sai do texto. **Decide-se pela primeira:**
Ca e macronutrientes são o único painel que distingue carência de patologia, e
sai barato numa colheita que já vai ao terreno.

## 2 · O QUE O DELTA DAS CAMADAS ABAIXO MUDA NO DESENHO

### 2.1 · Nenhum ponto de amostragem pode ser especificado por válvula

O **D9** da C4 é uma proibição, não uma ressalva: a área atribuída a qualquer
válvula varia até **50×** entre as quatro reconstruções do esquema, e na
`por_linha` a «v8» fica 300 m a leste de onde a `por_area` a põe.

> **Todos os pontos passam a coordenadas UTM.** Nenhuma folha de campo, nenhuma
> etiqueta de amostra e nenhuma linha de orçamento nomeia uma válvula. Onde a
> válvula for útil como referência de campo para quem lá vai, entra **depois**
> da coordenada e com a amplitude ao lado.

### 2.2 · O desenho tem de servir duas hipóteses, não uma

O **D2** da C4 já não diz «um acontecimento»: diz «pelo menos um», com a forma
não observada. E o **T2** mostrou que existem **onze cenas de plena estação por
olhar** entre as duas datas que o datam.

Um acontecimento agudo e dois declínios sucessivos pedem colheitas diferentes —
o primeiro pede procurar o que passou num momento, o segundo pede uma frente.
**Enquanto isso não se souber, o desenho não pode optimizar para nenhum dos
dois.**

### 2.3 · O esforço estava invertido, e mede-se

O **B12** da C3: 45,9 % dos registos colocados numa unidade com **0,3 %** de
área sem pérgola; a única unidade oriental, com **28,1 %**, ficou com 14,4 %.

> A alocação nova inverte isto. **A heterogeneidade do substrato é critério de
> alocação**, não um incómodo: onde metade do chão não tem planta, é preciso
> mais pontos para dizer alguma coisa sobre plantas.

### 2.4 · A restrição da U2 deixa de ser desenho e passa a condição

A C3 R3 quantificou: **28,1 % da unidade oriental ensaiada não tem pérgola**
(era 16,3 % pela ortofoto). Sem a restrição «só onde há pérgola», mais de um
quarto das plantas candidatas não existe.

> **U2: 3 plantas, só em células com altura MDS−MDT ≥ 0,5 m, coordenadas fixadas
> antes da ida ao terreno.** Vai em texto visível na peça, com o número.

## 3 · A ÁRVORE DE ACÇÕES, REFEITA

Três acções passam a **condição de arranque**. As duas primeiras não vão ao
terreno e não custam dinheiro.

| ordem | acção | custo | o que decide |
|---|---|---|---|
| **1** | **TEMP-01 · olhar as onze cenas.** Sete de Agosto de 2025 (DOY 228–238) e quatro de Julho de 2026 (DOY 183–206), todas com nuvem aceitável, inventariadas em `t2_cenas_descartadas.json`. | **nenhum** — os dados são públicos e já identificados | **Um acontecimento ou dois.** Muda o desenho da colheita, não a confiança nele. |
| **2** | **REG-01 · a comparação regional.** 1 054 ha de kiwi declarado por 204 beneficiários, por serviço aberto. | BAIXO | **Local ou regional.** Se for regional, quase todas as medidas de parcela são inúteis — a própria C5 escreveu-o em quatro sítios e não o fez condição. Agora é. |
| **3** | **COMP-01 · o comparador interno.** 12,64 ha de kiwi da mesma exploração a 750 m (G39), que **nenhuma medição deste dossiê tocou**, e que por três testes independentes **não tem degrau** (S9: ΔAICc +9,57 a favor da recta; fosso a fechar −0,020/ano; desvio à tendência própria +0,012, p = 0,76). | BAIXO | **Se a mesma gestão, a mesma água declarada e o mesmo material dão um bloco sem acontecimento a 750 m, a explicação tem de ser local ao sítio e não à exploração.** |

**Só depois destas três é que a campanha de Setembro faz sentido**, e a razão
está no §3 do certificado anterior, que estava certo e não foi seguido:
«enquanto REG-01 estiver por fechar, nenhuma medida irreversível».

## 4 · A CAMPANHA, com as correcções do adversário aplicadas

- **60 amostras**, não 48: 12 plantas × **5** matrizes — raiz fina, colo/tronco,
  solo 0-30, solo 40-80, **folha** (R7).
- **U2 ganha controlo de proximidade** dentro do B3, mesma fila, coordenadas
  fixadas — o oriental deixa de ter só um controlo de terreno a 474 m e noutro
  bloco (R8).
- **Todos os pontos em coordenadas UTM** (D9).
- **Alocação corrigida pela heterogeneidade do substrato** (B12).
- **Painel bacteriano e viral incluído.** A *P. syringae* pv. *actinidiae* nunca
  foi pedida a nenhum laboratório, em nenhuma matriz, em nenhuma data (D8). É a
  principal doença do kiwi no mundo e **zero linhas do caso são bacterianas**.
- **O transecto sai** como prova de propagação (R6); se se mantiver, é para
  mapear extensão, e diz-se isso.

## 5 · O QUE O RELATÓRIO PODE E NÃO PODE AFIRMAR — revisto

**Pode:**
- que houve **pelo menos um acontecimento** entre Agosto de 2025 e Julho de
  2026, que atingiu duas posições do pomar e não o resto dele;
- que o contraste foco-menos-controlo é **−0,115** e **−0,110**, medido nas
  mesmas cenas e no mesmo processamento, e que o sinal e a ordenação sobrevivem
  a **43 corridas** e a **quatro reconstruções** da geometria de rega;
- que **um segundo satélite, de outra agência**, data o mesmo acontecimento com
  p exacto no mínimo que catorze anos permitem, e que o **radar** — outra física
  — o vê no foco ocidental;
- que a composição dos dois sítios é **oposta**, por coordenadas e não por
  válvula, e que isso é robusto às quatro reconstruções;
- que **nenhum ensaio bacteriano ou viral foi alguma vez feito**, e que a
  matriz de diagnóstico tem uma coluna.

**Não pode:**
- escrever «**um** acontecimento» — o número não está estabelecido;
- escrever «**antes e depois**» com material biológico: todas as amostras com
  posição são posteriores a Março de 2026;
- atribuir **área a qualquer válvula**;
- afirmar propagação **não contígua**: no estrato de distância correcto os
  núcleos destacados estão nos percentis 9,6 / 14,2 / 29,2 %, e um deles está
  dentro do disco do próprio foco;
- usar o verbo «**excluída**» para as quatro linhas EXCLUÍDA-LOCAL;
- dizer que existe **controlo externo** — não existe, e agora é medição e não
  omissão (G39/G40).

## 6 · A DECISÃO CONTINUA A NÃO FECHAR, e o que mudou é a lista

O certificado anterior nomeou sete coisas que o material não distingue. Depois
deste ciclo:

| | estado |
|---|---|
| Local contra regional | **aberta, e agora é condição de arranque** (R10) |
| Doença contra gestão no lado oriental | aberta |
| Replantação contra chão limpo no N3 | aberta |
| Degrau contra declínio a acelerar | **resolvida a favor do degrau** — T1, com o ponto de quebra contabilizado: ΔAICc −6,6 a −7,6 nos focos, +6,4 no controlo, **+9,6 no B1** |
| Qual organismo, se algum | aberta |
| Se o vazio do gestor e o núcleo do satélite são o mesmo objecto | aberta |
| Quanto é cauda do sensor | **quantificada**: até −0,025 do valor absoluto; o contraste é a quantidade a usar |
| **NOVA · um acontecimento ou dois** | **aberta, e respondível hoje sem dados novos** |

**Duas fecharam, uma nasceu, e a que nasceu é a mais barata de fechar.**

---

## PASSA PARA CIMA — não há camada acima. Esta lista é para o relatório.

1. Todos os pontos em **coordenadas**; nenhuma válvula em nenhuma etiqueta.
2. **60 amostras**, com folha e com painel bacteriano.
3. **Três condições de arranque** — TEMP-01, REG-01, COMP-01 — e nenhuma medida
   irreversível antes delas.
4. O relatório escreve «**pelo menos um acontecimento**» e nunca «antes e
   depois».
5. **Não há controlo externo**, e o comparador mais próximo é o próprio bloco
   sudoeste da exploração, que não tem degrau.

---

## NOTA FINAL

Este ciclo respondeu a dez retiradas que estavam por responder desde 29-08,
aplicou o delta de quatro camadas, e fechou duas das sete indistinções.

**E não teve adversário.** O controlo 3 só o exige em C0 e C2 — mas as C2 R2 e
o seu adversário foram escritos pela mesma sessão, e tudo o que veio acima
herdou dessa. **A cadeia está retomada e coerente; não está independentemente
auditada.** É a última coisa que falta, e não é pequena.
