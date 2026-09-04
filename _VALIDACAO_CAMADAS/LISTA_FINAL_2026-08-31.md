# Lista final — o que sobrevive, depois de tudo

**31-08-2026.** Reconstruída depois do Controlo 3, das cinco retiradas dele, e
das duas retiradas minhas de hoje. **Cada linha leva o instrumento que a
confirma, ou a marca de que não tem.**

---

## A · O QUE SOBREVIVE COM INSTRUMENTO INDEPENDENTE

**Três factos. São o núcleo do caso.**

**A1 · Houve um acontecimento em 2025-26 em duas posições do pomar, e não no
resto.**
Contraste foco-menos-controlo, medido nas mesmas cenas e no mesmo
processamento: **−0,115** (ocidental) e **−0,110** (oriental), ±0,02–0,03.
*Confirmado por:* **Landsat 8/9** — outra agência, outro sensor, outra correcção
atmosférica — que replica **direcção e datação** com p exacto **0,0110 = 1/91**,
o mínimo que catorze anos permitem, e dá **−0,001 (p = 0,98)** no controlo.
*n do Landsat:* 35 píxeis (12 inteiros) no ocidental, 27 (2 inteiros) no
oriental. **As magnitudes não replicam, e não se diz que replicam.**

**A2 · O radar vê o mesmo, no foco ocidental.**
γ⁰ VV do foco menos o pomar inteiro: nove Invernos entre −0,17 e +0,48 (órbita
125) e −0,30 e +0,37 (órbita 147); em 2025-26, **−1,107 e −0,775 dB** — fora da
banda nas duas órbitas.
*Confirmado por:* é ele próprio o instrumento independente do óptico — física
diferente, 441 cenas, reproduzidas da C1 à terceira casa.
*No foco oriental o radar NÃO distingue*, e sabe-se porquê: metade dele é chão,
e chão já era baixo no radar nos dez Invernos.

**A3 · Entre as unidades com linha de base contínua, os dois focos estão no
fundo da região — mas «o pior e o segundo pior» depende de duas escolhas de
análise, e numa delas cai.**
REG-01 refeita a 01-09 depois da triagem de descontinuidade: **8 dos 37 blocos
saem** — cinco do ENT 297313, desmatados em 2024 com ortofoto a datá-lo, e três
do ENT 472062 que **não têm cultura na linha de base** (campo aberto em 2012,
2018 e 2021; pérgola nova em 2025; o 8845731 *ganhou* coberto, de 97,3 % sem
copado em 2021 para 23,7 % em 2025).
Dos 29 que ficam, na ordenação conjunta de 31: foco **OCIDENTAL −0,0839
(1.º, percentil 3,2 %)** e **ORIENTAL −0,0869 (2.º, 6,5 %)**, contra −0,0638 do
melhor bloco sobrevivente. Margem **0,0200** — a do ocidental, que é quem a
governa.

> ### **AS DUAS INCERTEZAS, e vão ao lado da frase, nunca em rodapé**
>
> **1 · amostragem.** Bootstrap de cenas: 1.º e 2.º em **91,4 %**, P(margem ≤ 0)
> = **0,072**. Bootstrap de **anos** — o correcto, porque o pós tem 29 cenas mas
> **dois anos** — **74,6 %**, **P = 0,252**. Jackknife: **retirado 2026, o foco
> ocidental sai do topo**. A conclusão assenta nas dez cenas de 2026, e o **B4**
> já regista que Julho de 2026 não é estável. **São o mesmo facto.**
>
> **2 · agregação — eixo novo, achado a 03-09 pelo Controlo 3.** O degrau
> publicado é **média**(2025-26) − **média**(2017-24). A **mediana** é tão
> defensável — é o que esta cadeia usa em todo o lado — e a janela de base é uma
> escolha, não um dado. Em **oito corridas** (4 janelas × 2 estatísticas) os dois
> focos são 1.º e 2.º em **quatro**. Margem: mínimo **−0,0245**, **mediana
> −0,0003**, máximo +0,0218.
> Quem entra pelo meio é sempre **6705424** (ENT 297313): maduro desde 2017
> (0,851), declive −0,004/ano, passa todos os rastreios. **Não é um bloco
> suspeito a entrar por uma porta lateral — é um competidor legítimo que a
> escolha da média estava a esconder.**

**O que sobrevive às oito corridas:** os dois focos estão sempre no fundo da
distribuição. **O que não sobrevive:** a ordinalidade exacta. A frase defensável
é «entre as piores da região», não «o pior e o segundo pior».

*Confirmado por:* ortofoto DGT — **cinco** blocos datados a 01-09, **três** a
03-09 com outra leitura — e série anual do Landsat. Critério de exclusão fixado
antes da corrida e aplicado uniformemente aos 37, robusto num planalto de
limiares de 0,15–0,40 (queda) × 0,51–0,80 (chão). *(Não se escreve «aplicado
cego»: a forense de datas NTFS mostra que o critério foi escrito **123 s depois**
de a ortofoto já ter identificado os cinco blocos.)*
*A magnitude não é reportável:* −0,0730 a −0,1526 conforme a definição da
mediana — **82 % de amplitude**. **A ordem é grosseiramente estável; o número
não.**
*A forma separa:* os cinco caem 0,43 **num ano**, do valor mais alto da sua série
(0,854-0,877 em 2023 → 0,42 em 2024) e param no domínio do solo. Os focos descem
0,17 em **dois passos** e estão em **0,72**.

## B · O QUE SOBREVIVE SEM INSTRUMENTO INDEPENDENTE

**Sete factos.** Pelo controlo 1, deviam estar em NÃO TESTÁVEL. Ficam com a
marca à vista, e não diluída.

| | facto | instrumento |
|---|---|---|
| **B1** | O sinal e a ordenação do degrau são invariantes em **43 corridas aninhadas** — 5 unidades × 3 raios × 5 limiares. Nenhuma muda de sinal; focos e controlo não se tocam. | Sentinel-2 |
| **B2** | O degrau bate a recta com o ponto de quebra contabilizado: **ΔAICc −6,6 a −7,6** nos focos, **+6,4 no controlo**; p do máximo 0,003 a 0,023 contra 0,37. | decomposição interna |
| **B3** | **São dois passos, não um.** Contraste ocidental: **−0,050** em Agosto de 2025 (seis cenas em treze dias, amplitude 0,005) e **−0,13 a −0,23** em Julho de 2026. | Sentinel-2 |
| **B4** | **Julho de 2026 não é estável.** O contraste vai de −0,229 (2 de Julho) a −0,130 (25 de Julho) — a escolha da cena muda o número por **1,7×**. **É o mesmo facto que o intervalo do A3:** retirado 2026, o A3 cai. | Sentinel-2 |
| **B5** | A correcção de dia-do-ano é **≤ 0,0011** e é um limite superior. | Sentinel-2 |
| **B6** | A referência sistemática tinha **14 a 18 células dentro dos discos** (14 pela definição da C2 R3, 18 pela da C3 B10 — centros diferentes). Os fossos são conservadores. | contagem geométrica |
| **B7** | Os três núcleos destacados tinham **base 2017-24 normal** (0,878 · 0,872 · 0,901) e desceram já em 2025. **No seu próprio estrato de distância não se distinguem** (percentis 9,6 / 14,2 / 29,2 %), e o #1 está dentro do disco do foco. | Sentinel-2 |

## C · O QUE SOBREVIVE DA GEOMETRIA E DOS DOCUMENTOS

**C1 · O voo LiDAR é de 06-07-2025, 14:34:53–14:51:08 UTC.** Um só dia, 0,27 h
de amplitude, `global_encoding` bit 0 = 1. *Cálculo em disco desde hoje.*

**C2 · A partição pérgola/chão é PÓS-TRATAMENTO** — o voo cai dentro da janela
do acontecimento. Toda a leitura que dela dependa herda isto.

**C3 · O bloco sudoeste é da mesma exploração:** 19,00 ha em 16 parcelas, 13,23
ha do ENT 472062, e **12,64 ha de kiwi declarado, todo dele**. *Instrumento
independente: o parcelário, documento de outra entidade.*
**Não há controlo externo contemporâneo de kiwi neste caso** — e agora é
medição, não omissão.

**C4 · ORI-COM tinha pérgola madura em 2010 (111 %) e 2012 (79 %).** Instrumento
a discriminar nas duas, e o meu código a **reproduzir os mapas certificados da
C2 a diferença máxima 0,00e+00** em 2 858 células. *Confirmado por:* o mapa
certificado, independente do meu cálculo.

**C5 · ORI-SEM nunca teve pérgola.** Pico a 2,25 m (2012) e 2,12 m (2021), longe
do compasso de 5,25 m.

**C6 · A pérgola apareceu no pomar entre 2007 e 2010.** Em 1995, 2004-06 e 2007
a prominência é negativa em **todas** as unidades, incluindo a referência — não
havia pérgola em sítio nenhum. Consistente com a coorte de plantação já
certificada pela C0.

**C7 · A atribuição de válvulas não sustenta nenhuma quantidade.** O contraste
entre as duas posições sobrevive às quatro reconstruções do esquema; **a área
atribuída a qualquer válvula varia até 50×**. Nenhuma peça pode escrever uma
área por válvula.


**C8 · A hipótese «rede de rega sobre-estendida» foi fechada por um teste que
não alcançava o troço que a torna sobre-estendida.**
A P06 dá-a por fechada — «partição por válvula contra 200 partições rodadas da
mesma geometria · dentro do nulo 11/11». Mas **as quatro reconstruções do
esquema contêm as válvulas 6 a 17, doze, todas no corpo principal.** As
**válvulas 1 a 5 não estão em nenhuma**, e estão registadas como *«POR
COLOCAR»* — com um fundamento que invoca «o lóbulo oeste», o objecto **retirado
a 28-08** com 49 ficheiros em quarentena.
*Confirmado por:* **o próprio esquema de rega** — o PDF mostra as válvulas 1 a
5 num lóbulo fisicamente separado ao extremo oeste, ligado por conduta de 3 e 4
polegadas, rotulado **«B1»**, e as notas manuscritas do projectista falam de
«campo **B1 C3**», «**B1 C2**» e «o B1». **Isto fecha a nomenclatura**: os
boletins de solo rotulados B1 C1 / C3 / C4 são sub-campos deste lóbulo.
*E por* **testemunho de tipo 1** — «B1 = válvulas 1-5», gestor, 03-09-2026.

> **CORRIGIDO em 03-09, e a correcção é minha.** Escrevi primeiro que o bloco do
> **G19** (E529350–530085 / N4653700–4654478) e o **B1** do IFAP
> (E529495–530063 / N4653832–4654477) «batem a 1 metro no bordo norte». É
> verdade dos números registados e **é enganador**: o G19 vem de uma
> extrapolação de ~1200 px além do troço ajustado, com **erro declarado de
> ±150 m** e resíduo mediano do ajuste de **64 m** (`c0_13_georref.json`).
> Concordarem a 1 m dentro de um envelope de ±150 m é coincidência de
> arredondamento, não precisão. **O que é sólido é o contido:** o B1 do IFAP
> cai inteiramente dentro da caixa do G19, e as duas derivações são
> independentes — mas com a incerteza do esquema à vista.
*E fecha o «pertença NÃO confirmada» do G19:* o C3 já certifica que 12,64 ha de
kiwi ali são todos do ENT 472062.
**O esquema anota 1,77 ha para o B1; o IFAP dá 12,63 ha — factor 7,1×.** É uma
instância concreta do C7.

> **A hipótese passa de FECHADA a fechada só para o corpo principal.** Cinco
> válvulas servem um sector 500 m a sudoeste, fora da janela em que todo o teste
> correu. **Reabrir não é confirmar:** não se conclui que a rega explica o
> declínio, conclui-se que a hipótese não foi testada onde teria de ser.
## D · O QUE SOBREVIVE DA BIOLOGIA

**D1 · A matriz de diagnóstico tem uma coluna.** Das 20 linhas organismo ×
matriz, **13 assentam numa única amostra composta**, num sítio, num dia.

**D2 · O único organismo com posição é o *M. hapla*,** positivo em 4/4 unidades
colocadas — e **anticorrelaciona** com o défice (ρ = −0,40 no solo, −0,80 na
raiz; n = 4). Excluído como explicação do contraste; não excluído como fundo.

**D3 · A única amostra do lado oriental é um composto sobre 9,92 ha**, dos quais
**28,1 % não têm pérgola** pelo LiDAR (16,3 % de chão lavrado pela ortofoto). A
contagem não pode ser atribuída a plantas do foco oriental.

**D4 · O esforço de amostragem é inverso à heterogeneidade do substrato:**
45,9 % dos registos numa unidade com 0,3 % de área sem pérgola; a única unidade
oriental, com 28,1 %, ficou com 14,4 %.

**D5 · Nenhuma amostra com posição é anterior ao acontecimento.** Todas as doze
são posteriores a Março de 2026.

**D6 · Zero ensaios bacterianos ou virais.** *E a razão existe, e é de tipo 1:*
**a PSA nunca foi encomendada porque os sintomas das plantas não eram
compatíveis.** Falta escrevê-la no livro-razão — é a ausência dessa linha que
fez quatro documentos tratarem isto como lacuna.


**D7 · Os boletins A2 não podem testar afectado contra não afectado.**
São **oito talhões, não nove boletins**: «B2 - V7» (Março) e «B2 - Zona 1 (V7)»
(Junho) são o mesmo talhão, a mesma válvula, colocados na mesma coordenada.
A colocação que existe é **INFERIDA, não medida**, e o **C7** proíbe a
atribuição por válvula — que era a única via que restaria.
*E o talhão repetido vale mais do que a contagem:* é o **único piso de ruído
medido** deste conjunto — **0,2 unidades de pH** entre as duas datas, e a
**textura muda de classe** (Franca → Argilosa).
*(As três razões que eu tinha escrito — «zero têm coordenada», «três de nove são
do B1», «nove boletins» — foram todas corrigidas pelo Controlo 3 a 04-09. O
«zero» era um literal escrito à mão: o script nunca abriu o ficheiro que o
próprio facto nomeia como fonte, e esse ficheiro coloca **seis** dos nove.)*

**D9 · Faltam a CTC e a saturação em bases. A profundidade é NÃO SABIDA, não
ausente.** Os 12 parâmetros são pH, textura, MO, C:N, N, P₂O₅, K₂O, CaO, MgO, S,
Fe, Mn — fertilidade, **nada do complexo de troca**. Essa ausência é documental e
verificável.
**A profundidade não.** Os cinco campos que interroguei **não podiam contê-la**,
os nove PDF de origem **não estão nesta máquina**, e o livro em inglês marca nove
células «page 2 not extracted» onde o português tem números. *«Não sabido» e
«ausente» são coisas diferentes, e este dossiê já foi apanhado a confundi-las.*

---

## E · O QUE FOI RETIRADO — vinte e uma

As quinze da P06, mais três de 31-08, mais a de 01-09:

**19 ·** «Há blocos vizinhos com degrau 2 a 4× maior que os focos de Ganfei» —
os cinco blocos do ENT 297313 tinham sido **desmatados em 2024**, e a queda caía
do lado PRÉ da fronteira dos períodos. **Tinha passado o `guarda.py` com dois
instrumentos independentes concordantes e ρ = +0,890** — porque ambos mediam a
mesma coisa errada. O portão ganhou por isso uma quinta condição,
`identidade_no_tempo()`. Ver `REG01_RETRACCAO_A3.md`.

**16 ·** «O foco oriental foi replantado» — concluído da prominência sozinha;
derrubado pelo NDVI (nenhuma cova em treze anos) e pelo perfil radial (em 2021
nem a referência tem o pico no compasso da pérgola).

**17 ·** «Os fossos são conservadores, medido pelo T5» — o T5 é uma identidade
algébrica: limpar a referência desloca todos os fossos pela mesma constante,
+0,008430, idêntica à nona casa. O ramo do *line-stop* era inalcançável.

**18 ·** «O B1 é o comparador sem degrau» — zero instrumentos independentes, a
recta ganha porque o bloco está em subida, e o veredicto dependia de um limiar
inventado.

**20 ·** «A acidez do solo não acompanha o declínio» (D8) — **retirado no mesmo
dia em que entrou.** Assentava num degrau de +0,092 que o Controlo 3 **rejeitou
a 03-09 às 23:07:55**, e o script que o usou foi escrito **9,3 horas depois**.
E o número não sustenta nada: P(os dois mais baixos serem de um grupo de três) =
**1/12**; Mann-Whitney exacto **p = 0,25**; os postos do B1 são **1, 2 e nove** —
cobre o intervalo inteiro. O piso de ruído medido é **0,2 de pH** e o facto
assentava em 0,3. **E nos seis boletins com posição a relação inverte-se**
(ρ = −1,000, p = 0,042).

**21 ·** «As válvulas 1-5 não estão em nenhuma das quatro reconstruções» (C8) —
**estão.** O `valvulas_v4.json` tem-nas em `lobo_oeste`, com UTM; o meu leitor
procurava `valvulas`/`metros_por_linha`, caía no dicionário de topo e devolvia
zero — e eu escrevi por cima um comentário a afirmar que a chave «não enumera
válvulas». **O critério pré-registado dizia que, nesse caso, o ficheiro não
servia para nada. Publiquei contra o meu próprio critério.**
A conclusão sobrevive por outra via — a cobertura de **60,8 %** — o esquema de
rega sai da frase, e o «1,77 ha» sai também: **não está na tinta.** O
varrimento dá 44 px de largura máxima em vermelho, e a anotação é um traçado
vectorial sobreposto ao scan, de mão desconhecida.

---

## F · O QUE NÃO SE PODE ESCREVER

- «**um** acontecimento» — são dois passos (B3);
- um **valor único** para 2026 sem a amplitude ao lado (B4);
- «**antes e depois**» com material biológico (D5);
- **área por válvula** (C7);
- **propagação não contígua** (B7);
- «**não há halo**» — o nulo toroidal não tem potência declarada; é não
  testável, não negativo;
- que existe **controlo externo** (C3);
- que o **B1** é comparador de coisa nenhuma;
- que o oriental foi **replantado** ou **arrancado**.

---

## G · A FILA, POR VALOR

| | acção | custo | decide |
|---|---|---|---|
| ~~—~~ | ~~**REG-01**~~ · corrida 31-08 | — | **feita.** Não é exclusivo desta exploração |
| ~~—~~ | ~~**REG-01 no Landsat**~~ · corrida 01-09 | — | **feita** — e replicou um artefacto. Ver `REG01_RETRACCAO_A3.md` |
| ~~—~~ | ~~**ortofoto sobre os cinco blocos do 297313**~~ · corrida 01-09 | — | **feita.** Desmatados em 2024. O LiDAR não foi possível: acesso da DGT fechou |
| **1** | escrever no livro-razão a linha da **PSA** — exclusão clínica, quem observou, quando | nenhum | fecha uma lacuna que consumiu quatro documentos |
| **2** | correr a **triagem de descontinuidade** antes de qualquer comparação entre parcelas | nenhum | evita repetir o A3 |
| 3 | potência do nulo toroidal | baixo | se «não há halo» é negativo ou lacuna |
| 4 | o bloco sudoeste em LiDAR, Landsat e SAR | médio | se é comparador ou lacuna |
| 5 | perfil radial completo por unidade em todas as épocas | baixo | o que aconteceu à estrutura entre 2012 e 2021 |
| 6 | a campanha de Setembro, **nesta exploração** | alto | a etiologia |

---

## H · A CORRECÇÃO ESTRUTURAL

`guarda.py`, no mesmo directório. Um facto não emite veredicto sem:

1. instrumento declarado;
2. **instrumento independente que concorde**, ou `nao_testavel()` explícito;
3. **âncoras que discriminem** *e* **pico na escala esperada** — separar não é o
   mesmo que medir o que se julga;
4. **reprodução** de um cálculo certificado, quando exista.

O auto-teste replica as três retiradas históricas — o lóbulo oeste original, o
S9 e o P3 — e **bloqueia as três**, o P3 por duas vias independentes. E deixa
passar a pérgola de 2012, que cumpre as quatro.

5. **identidade da unidade no tempo**, quando o facto compara unidades ao longo
   de um intervalo — acrescentada a 01-09 depois da retirada do A3, porque as
   quatro anteriores interrogam todas o *instrumento* e **dois instrumentos
   independentes concordarem não valida a definição da unidade.**

O auto-teste inclui agora o caso do A3, e bloqueia-o.

**Levanta excepção, não avisa.** Um aviso teria sido ignorado das três vezes.
