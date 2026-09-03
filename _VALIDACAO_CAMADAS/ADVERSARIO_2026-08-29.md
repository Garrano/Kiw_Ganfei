# Adversário do dia de 29-08-2026 — adenda de LiDAR e trabalho de gestão

Sessão adversarial. Alvo: `CAMADA_2_ADENDA_LIDAR.md` e todo o conteúdo de
`Downloads\_VALIDADE_GESTAO\`. Lidos: a adenda, `REGISTO.md`, `REGISTO_IFAP.md`,
`PROTOCOLO.md`, `CONTROLOS.md`, `CAMADA_2_ADVERSARIO.md`, os trechos citados do
`CAMADA_2_CERTIFICADO.md`, `c2_00_comum.py`, e os onze scripts e vinte e um JSON
da pasta de gestão. **Nada foi recomputado, nenhuma cena foi aberta, nenhum
LAZ foi lido.** Onde precisei de um dado para julgar, nomeio-o.

**Nota de abertura, para o registo ser honesto.** Este dia produziu a melhor
coisa que aconteceu ao caso: um instrumento que mede geometria e não
reflectância, e um documento administrativo que ninguém deste lado escreveu.
Duas peças são exemplares e digo-o antes de atacar. A primeira é a série
Landsat: proveniência genuinamente estranha, e o foco OESTE a ler fosso
0,000 ± 0,004 durante onze anos e depois 0,046 e 0,146 — é a verificação
independente que o certificado da C2 pediu em NÃO TESTÁVEL e não obteve. A
segunda é a retirada do teste de prominência em `REGISTO.md`, apanhada pela
calibração e não pela estatística, e escrita com a regra que dela sai.

O ataque que se segue é duro porque há material para atacar. **O achado
principal não é nenhum dos sete itens que o prompt desta sessão enumerou.** É
que a adenda inteira aplica uma partição de **um instante** — 06-07-2025 — a
onze anos de série para trás, declara o limite para a frente numa caixa no fim,
e nunca declara o limite para trás. Está na parte 3.

---

## 1. Factos a retirar

Oito retiradas. Como da vez anterior, quase nenhuma apaga uma medição: o que
cai é a frase que liga os números, e em três casos o número publicado não é o
número que o código escreveu.

---

### R1 · L6 e a figura F9 — «défice **exactamente zero** em 2022, 2023 e 2024»

**Retira-se o zero, e retira-se a leitura que dele se tira.**

**O que teria de ser verdade para isto estar errado.** Que
`mapa_defice(a, VIVO, r)` e `mapa_defice(a, LIMPO, r)` particionem
`mapa_defice(a, POMAR, r)`. Não particionam, e a razão está em
`c2_00_comum.py`:

```python
def mapa_defice(nd, pomar, ref_val, limiar=LIMIAR, abertura=ABERTURA):
    b = (nd < ref_val - limiar) & pomar
    if abertura:
        b = ndimage.binary_opening(b, np.ones(abertura))
    return b
```

A abertura morfológica 2×2 é aplicada **depois** da intersecção com a máscara
recebida. Uma célula de copado em défice só sobrevive se pertencer a um bloco
2×2 inteiramente em défice **e inteiramente dentro de VIVO**. Como VIVO e LIMPO
são um corte pela mediana de um campo de altura a 10 m dentro do mesmo disco,
as duas classes estão interdigitadas: partir a máscara parte os aglomerados
exactamente na costura, e a abertura apaga o que ficou solto.

**O que o JSON diz, e o texto não.** Somando as duas sub-séries de
`serie_separada.json` contra o total da mesma linha:

```
ano      total   vivo + limpo   perdido na costura
2017      8,08    4,89 + 1,81    1,38 ha  (17,1 %)
2019      3,77    0,85 + 1,73    1,19 ha  (31,6 %)
2021      3,34    0,16 + 1,81    1,37 ha  (41,0 %)
2022      3,16    0,00 + 1,92    1,24 ha  (39,2 %)
2023      3,08    0,00 + 2,14    0,94 ha  (30,5 %)
2024      2,91    0,00 + 1,92    0,99 ha  (34,0 %)
2025-08   5,43    1,32 + 2,61    1,50 ha  (27,6 %)
2026      7,86    4,03 + 2,61    1,22 ha  (15,5 %)
```

E não há categoria residual onde arrumar isto: `ifap_cruzamento.json` dá
26,54 + 3,77 = 30,31 ha, o polígono inteiro. **`SEMDADOS` é zero.** Tudo o que
falta foi apagado pela abertura.

Repare-se em qual é o padrão. **Os três anos que leem zero são os três anos com
maior perda proporcional na costura** — 39 %, 31 %, 34 %. Não é coincidência: é
o mecanismo. Quando o défice de copado é pequeno e disperso ao longo da
fronteira com o chão, partir a máscara destrói-o por inteiro.

**Como se testa em cinco minutos.** Contar `(nd < r − 0,05) & VIVO` **sem
abertura**, nos três anos, e repetir a limiares 0,04 / 0,05 / 0,06. O número não
existe em nenhum JSON. Nota lateral que agrava: `dv = mapa_defice(a, VIVO, r)`
inclui as 110 células da própria referência, que por construção não podem estar
em défice, enquanto o `fv` da linha seguinte as exclui — as duas grandezas da
mesma linha usam conjuntos diferentes.

**E a leitura que se retira com o número.** A adenda escreve que «o degrau
sanitário **parte de zero**, não de 2,91 — é mais limpo, não mais fraco». É o
contrário. Uma série encostada ao chão do seu intervalo durante três anos tem
variância nula: deixa de ser possível estimar dela o ruído da linha de base, e
portanto deixa de ser possível dizer o que 4,03 ha tem de surpreendente. A V11
do certificado declarou uma barra de ~3 ha para a série e ela nunca foi
propagada. **4,03 ha com barra de ±3 ha e uma base de exactamente 0,00 não é
mais limpo; é uma série cuja barra já não se pode estimar da base.** Zero é o
piso de uma variável censurada, não uma medição.

**Formulação que aguenta:** *dentro do copado, o défice em aglomerados de pelo
menos 2×2 células é indistinguível de zero em 2022–2024, sobe a 1,32–1,37 ha em
2025 e a 4,03 ha em 2026.* Com a contagem sem abertura ao lado.

**Se cair, o que cai com ele.** L6 por inteiro, a linha 4 do quadro CORRIGE, e
a figura F9. Não cai a separação como ideia, nem o crescimento de 2026.

---

### R2 · L4 — «existe em copado (p = 0,042) e **não existe** em chão (p = 0,368)»

**Retira-se. O placebo não passou; foi lido como tendo passado por ser mais
ruidoso.**

Esta é a linha que a adenda apresenta como o seu melhor argumento — «o
teste-placebo que a C2 não podia correr: o sinal está onde estão as plantas e
não está onde elas não estão». O `refazer_c2_este.json` diz outra coisa.

```
ESTE com pergola (LiDAR)  1,27 ha   degrau +0,05854   SQR_deg 0,00209   p 0,0416
ESTE sem pergola (LiDAR)  1,28 ha   degrau +0,05310   SQR_deg 0,04744   p 0,3683
```

**O degrau no chão é +0,0531 contra +0,0585 no copado: 91 % do tamanho.** O que
difere não é o efeito — é a variância residual, vinte e três vezes maior no
chão. Os dois p separam-se por causa do denominador, não do numerador. Um
controlo negativo que mede o mesmo efeito e falha a significância por ruído
**não é um controlo negativo**: é uma unidade sem potência.

**O degrau de +0,0531 não aparece em lado nenhum do texto.** A adenda publica
«1,06 : 1, p = 0,368» e a frase «nada acontece em 2025». O número que
contradiz a frase está no ficheiro que a própria sessão escreveu.

**Agrava-se com a estatística.** `t = stats.ttest_ind(f[tardio], f[~tardio],
equal_var=False)` com `tardio = d >= "2025"` — Welch de **2 contra 8** pontos. O
adversário anterior escreveu, sobre exactamente esta classe de teste em
`c2_06_este.json`: «com n = 2 depois da quebra, nenhum t-test pode dar
significância». A adenda usa o mesmo teste, obtém 0,042 do lado que lhe
convém, e trata-o como prova. Com n = 2, o desvio-padrão do grupo pequeno vem
de uma única diferença; p = 0,042 e p = 0,368 são a mesma estatística com o
ruído a decidir.

**Como se testa em cinco minutos.** Repetir o contraste a limiares de altura de
0,3 / 0,5 / 1,0 / 1,5 m. Se o «existe/não existe» não sobreviver ao
deslocamento do corte, L4 é uma propriedade do corte.

**O que sobrevive e deve substituir L4.** A linha que o ficheiro contém e o
texto ignora:

```
resto do pomar, com pergola  22,20 ha  degrau -0,03165  razao 0,29  p 0,0082
```

**O resto do pomar fecha o fosso enquanto os dois focos o abrem**, com p = 0,008
sobre uma unidade de 22 ha e um modelo linear a ganhar ao degrau. Isso é
especificidade a sério, é a única linha do ficheiro com potência, e não está
publicada.

**Se cair, o que cai com ele.** L4 e a frase «SAI DE NÃO TESTÁVEL» na parte que
diz «a parte sem planta não tem degrau». Não cai L7, não cai o degrau em
copado — cai a afirmação de que ele foi controlado.

---

### R3 · A própria partição — o limiar documentado não é o limiar operativo

**Retira-se a etiqueta «sem pérgola» / «chão». Mantém-se a medição de altura.**

**O que teria de ser verdade para isto estar errado.** Que a partição seja
feita ao limiar que a adenda justifica. Não é.

A adenda escreve, três vezes, que a grandeza é «a fracção de píxeis de 50 cm
acima de **1,5 m**, limiar que fica abaixo da pérgola de kiwi (1,8–2 m) e acima
de qualquer coberto herbáceo». O `altura_copado.py` calcula isso. Mas a
partição que decide tudo está em `refazer_c2_este.py`, `serie_separada.py`,
`landsat_independente.py`, `terreno_contra_declinio.py`, `rede_de_rega.py` e
`ifap_cruzamento.py`, e é sempre esta:

```python
h = np.load("chm_altura.npy")          # mediana das alturas na celula de 10 m
COM = np.isfinite(h) & (h >= 0.5)      # "tinha pergola em 06-07-2025"
SEM = np.isfinite(h) & (h <  0.5)
```

**Meio metro, sobre a mediana da célula.** Uma célula cuja altura mediana é
0,6 m — que não é pérgola nenhuma — entra em «com pérgola». A justificação
escrita (1,5 m fica abaixo da pérgola e acima do coberto herbáceo) não é
justificação nenhuma de 0,5 m, que fica dentro do alcance de silvado, de
rebentação e de erva alta num voo de Julho. **O texto justifica um limiar e o
código usa outro, e o outro nunca é declarado.** É a forma exacta do erro de
higiene que o `CLAUDE.md` deste projecto manda evitar — ler o cabeçalho e o
código juntos.

**E o corte cai no pior sítio possível.** `altura_focos.json` dá ao foco ESTE
altura mediana **0,47 m**. O limiar é 0,50 m. **O corte passa pela mediana da
unidade que ele parte** — daí os 50,2 % de um lado e 49,8 % do outro, que a
adenda apresenta como achado («metade do disco ESTE está abaixo de meio
metro») quando é o resultado quase aritmético de cortar uma distribuição no seu
centro. As duas metades de L4 não são «com planta» e «sem planta»: são a metade
de cima e a metade de baixo do mesmo campo contínuo.

**O documento contradiz a etiqueta.** `ifap_cruzamento.json`:

```
SEM pergola (LiDAR)   3,77 ha   pct_kiwi 64,99   pct_sem_declaracao 18,30
```

**Dois terços do terreno que a adenda chama «chão» estão declarados KIWI ao
IFAP a 10-06-2025**, três semanas antes do voo. O `REGISTO_IFAP.md` §1.3
escreve, sobre esta mesma linha, «Onde o LiDAR não vê pérgola, o beneficiário
declarou erva, forragem ou nada» — e as culturas anuais que lista somam 0,63 ha
e a área sem declaração 0,69 ha, de 3,77. A frase é falsa para 65 % da área que
descreve, e o número que a torna falsa está na linha acima dela no seu próprio
JSON.

**Consequência, e é grande.** O `serie_separada.py` fecha com «'sem pérgola'
não é doença: é terreno onde a planta foi retirada». Essa é a inferência que
transforma 40,7 % do défice de 2026 em «decisão de gestão» em vez de «facto
sanitário», e ela assenta em altura < 0,5 m ⇒ sem planta ⇒ gestão. O documento
diz kiwi em dois terços daquilo. As duas leituras restantes — replantação
recente, ou desfasamento declarado/instalado — são as duas que o próprio
`REGISTO_IFAP.md` §1.4 lista para o N3, **e a primeira devolve essas hectares à
história sanitária**, porque uma replantação é a resposta a uma morte.

**Formulação que aguenta:** *3,77 ha do polígono tinham altura mediana inferior
a 0,5 m em 06-07-2025.* Sem «pérgola», sem «chão», sem «planta retirada».

**Se cair, o que cai com ele.** L2, L3, e a etiqueta de todas as unidades de
L4–L7. Não cai a medição de altura, que é boa e é nova.

---

### R4 · CORRIGE, linha 3 — a adenda atribui ao LiDAR uma correcção que o LiDAR não fez

A adenda escreve: as fracções de chão de V10 «vinham de `nu2021`, uma máscara de
2021 aplicada a dez anos; substituem-se» por 74,5 / 75,7 / 75,6 / 53,4 %.

Só que o `refazer_c2_este.py` calcula **as duas colunas**, e a coluna `nu2021`
recomputada não é a que o certificado publicou:

```
                2020   2022   2024   2026
certificado C2    53     60     78     34     (c2_06_este_plantado.py)
nu2021 refeito  78,6   74,3   74,8   42,4     (refazer_c2_este.json)
LiDAR           74,5   75,7   75,6   53,4     (refazer_c2_este.json)
```

**As duas máscaras concordam entre si a poucos pontos em todos os anos.** A
divergência não é entre instrumentos — é entre a recomputação e o certificado.
Trocar `nu2021` por LiDAR quase não muda nada; o que mudou os números foi outra
coisa, dentro do cálculo, e a adenda não a nomeia porque não comparou as suas
duas colunas uma com a outra.

**Dado que preciso e não vou buscar:** a definição do denominador na secção
final de `c2_06_este_plantado.py` — se é o défice ∩ disco, ou o núcleo listado
por `nucleos()` com `MIN_NUCLEO = 15`.

**Se cair, o que cai com ele.** A frase «a história é a mesma e é mais estável
do que a publicada». A direcção de V10 aguenta — cerca de três quartos durante
oito anos e queda em 2025-26 — mas aguenta em **ambas** as máscaras, o que
significa que este item **não** satisfaz o Controlo 1: não é uma confirmação por
instrumento independente, é a mesma resposta com duas máscaras que concordam.

---

### R5 · O cruzamento IFAP — «a validação externa mais forte que a geometria deste caso alguma vez teve»

**Retira-se a frase e retira-se o estatuto de validação. Mantém-se o documento
como documento.**

O prompt desta sessão pede que se ataque a coincidência de 1,3 % com a mesma
suspeita com que se atacou a de 0,3 %. Atacada, não fica de pé, por quatro
razões independentes.

**Primeira: a entidade foi escolhida, e a escolha não está confirmada.** O
`REGISTO_IFAP.md` §4.3 lista como pergunta em aberto ao gestor: «Confirmação de
que a exploração é o ENT_ID 472062 e de que as 18 parcelas são todas.» As 44,36
ha saem de somar `por_cultura["124"]` sobre essa entidade. Só há uma maneira de
ter chegado ao 472062: procurar quem declara parcelas onde o gestor disse que
está o pomar. **Selecciona-se a entidade pela geografia que o gestor deu, e
depois compara-se a sua área com a tabela que o mesmo gestor deu.** Não são dois
documentos independentes; são a mesma exploração descrita duas vezes, com o
mesmo informador de um lado dos dois. É a forma exacta da suposição imposta.

**Segunda: o resíduo é menor do que uma escolha de contabilidade.** A diferença
é 0,57 ha. O `ifap_exploracao_total.json` tem, na mesma entidade, o código
**982 «CABECEIRAS CULT. PERMANENTES — ÁREA ÚTIL» = 0,35 ha** — cabeceira de
cultura permanente, que qualquer contabilista da exploração pode legitimamente
somar ou não somar ao kiwi. Somando: 44,71 contra 44,93, **0,5 %**. Uma
comparação cujo resíduo se move em 60 % por uma decisão de arrumação não valida
nada a 1,3 %.

**Terceira: só há um número de cada lado.** Um escalar contra um escalar é a
forma mais fraca de concordância que existe, porque erros de sinal contrário se
cancelam na soma. A única comparação desagregada que o registo faz — o B1 —
concorda **pior**: 12,63 contra 13,01, **2,9 %**. Se o B1 está 0,38 ha abaixo,
o resto tem de estar 0,19 ha acima para o total cair a 0,57 abaixo. O todo bate
melhor do que as partes, que é o que acontece quando se comparam dois números
que já se sabia serem quase iguais.

**Quarta: não houve tolerância declarada.** Nada diz, antes de correr, que
diferença teria sido lida como desacordo. Com 49,76 ha de parcela, 49,30 de
cultura e três códigos, 2 ou 3 % seriam explicados sem esforço. Um teste sem
critério de falha não é um teste.

**Nota de método, que é do mesmo lado.** `rasterize(..., all_touched=False)`
atribui cultura pelo centro da célula. A unidade «SEM pérgola» é 3,77 ha
dispersos com razão perímetro/área muito maior do que a unidade «com pérgola»
compacta — logo o contraste 18,3 % contra 0,3 % de «sem declaração» é em parte
efeito de fronteira. Não foi testado com `all_touched=True` nem com erosão de
uma célula.

**O que sobrevive, e é real.** *O parcelário de 2025 declara KIWI em 95,2 % do
polígono do pomar e em 99,4 % da área com altura ≥ 0,5 m, contra 65,0 % da área
abaixo desse limiar; e todas as declarações de cultura anual dentro do polígono
caem abaixo do limiar.* Isso é um documento a marcar uma fronteira que um
instrumento geométrico também marca, e é bom. Não é uma validação de área, e
não é «a mais forte de sempre» — a mais forte de sempre continua a ser o par de
instrumentos de V7.

**E, sem script, não é prova.** `ifap_exploracao.json` e
`ifap_exploracao_total.json` — de onde saem as 44,36 ha — **não são escritos por
nenhum ficheiro `.py` em disco**. O `ifap_cruzamento.py` escreve apenas
`ifap_cruzamento.json` e `ifap_cultura.npy`. Regra 3 do protocolo: um facto, uma
prova, com o ficheiro e o cálculo nomeados.

---

### R6 · «Os dois focos perdem mais água do que verdura» → «problema hidráulico ou vascular»

**Retira-se por dois motivos, e o segundo é de protocolo.**

**Primeiro, a comparação é inválida como está feita.** O `REGISTO_IFAP.md` §2
compara fossos absolutos entre dois índices: NDMI 0,199 contra NDVI 0,146 no
OESTE, 0,201 contra 0,138 no ESTE. Os dois índices têm níveis de referência
diferentes — NDVI ≈ 0,87, NDMI ≈ 0,50 — e comportamentos de saturação
diferentes. O parágrafo **imediatamente anterior** declara: «o fosso do OESTE em
~0,000 durante onze anos é em parte **saturação** do NDVI sobre copado
fechado.» Um índice saturado comprime as suas diferenças; um índice a meio da
gama não. Isso sozinho prevê um fosso absoluto maior no NDMI, sem fisiologia
nenhuma. **A ressalva de saturação é declarada para a linha de base e largada
na inferência que mais depende dela.**

**E o `landsat.json` mostra que a assimetria é a condição normal da unidade.**
No ESTE com pérgola, o fosso NDMI excede o NDVI em **todos** os catorze anos:
2015 dá 0,102 contra 0,066, 2020 dá 0,049 contra 0,036, 2013 dá 0,070 contra
0,070. Não é assinatura de 2026. Recolocado sobre **variações desde a base**,
que é a única forma defensável, o rácio é 1,53 no ESTE e 1,36 no OESTE — muito
menos do que a leitura sugere, e ainda por descontar da diferença de escala.

**Segundo: é uma afirmação de etiologia numa adenda da C2.** A regra 5 do
`PROTOCOLO.md` diz «não teorizar acima da própria camada». «Aponta para
problema hidráulico ou vascular» é C4. O `terreno_contra_declinio.py` importa-a
já como premissa no seu cabeçalho — «a perder água mais depressa do que folha
(...) Isso não é seca. É compatível com raiz que não consegue absorver havendo
água, que é o que asfixia radicular e *Phytophthora* produzem» — e desenha a
hipótese a partir dela. Uma inferência de camada errada entrou pela porta do
lado e passou a fundamentar o desenho experimental seguinte.

---

### R7 · A assinatura espectral — «a amplitude sazonal é a assinatura de classe do kiwi, +0,496 contra +0,092 do segundo»

**Retira-se. A tabela do próprio JSON refuta-a.**

**O que teria de ser verdade para isto estar errado.** Que todas as classes
tenham o mínimo em Dez-Fev e o máximo em Jul-Ago, porque o discriminante é
`amp = mediana(Jul, Ago) − mediana(Dez, Jan, Fev)`, uma janela fixa. Para o
milho é falso, e o `assinatura.json` di-lo em claro:

```
milho  Jan 0,790  Fev 0,755  Mar 0,760  Abr 0,477  Mai 0,124  Jun 0,345
       Jul 0,832  Ago 0,864  Set 0,531  Out 0,208  Nov 0,374  Dez 0,554
```

**A amplitude sazonal real do milho é 0,124 → 0,864 = 0,740**, maior do que a do
kiwi (0,390 → 0,886 = 0,496). O valor publicado, +0,092, sai de tomar como
«piso» a mediana de Dez-Jan-Fev, que num sistema de milho é a **cultura de
Inverno** — azevém, consociação forrageira — a ler 0,75-0,79. A grandeza que
separa não é a amplitude: é o **piso de Dez-Fev**. O kiwi está em 0,39 e todas
as outras classes entre 0,66 e 0,88.

**E a `vinha` não mede vinha.** `amp = −0,136`, com «pico» (0,560) abaixo do
«piso» (0,696), e Novembro (0,752) acima de Agosto (0,472). Uma vinha caduca não
lê mais em Novembro do que em Agosto: o que está a ser medido é o enrelvamento
da entrelinha em parcelas pequenas. A classe de comparação está contaminada e
não pode sustentar «contra +0,092 do segundo».

**Há um mecanismo concreto que produz isto.** As etiquetas são da campanha de
**2025** (`culturas.2025jun10`), e a climatologia é calculada sobre **2025 e
2026 juntos** (`for ano in (2025, 2026)`, com `mens[nome][mês]` a agregar os dois
anos). Culturas anuais rodam. Metade das observações das classes milho, prado e
pastagem é de outra cultura. Para o kiwi, que é permanente, o problema não
existe — o que significa que a comparação está enviesada exactamente na
direcção que favorece a conclusão.

**Terceiro item, menor:** `mes_subida` dá 5 para o kiwi **e 5 para a vinha**. O
segundo discriminante declarado no cabeçalho — «o kiwi abrolha TARDE» — também
não separa. Dos dois discriminantes propostos, um não separa e o outro é uma
janela mal posta.

**O que sobrevive, e é utilizável:** *o piso de NDVI de Dez-Fev separa o kiwi
(0,39) de todas as outras classes desta janela (0,66–0,88), com rótulos que não
são nossos.* Formulado assim, o facto é bom e é novo. Formulado como
«amplitude», está errado.

---

### R8 · L8 — «276 cenas», e a normalização que não existe em código

Dois itens pequenos e um grande.

**As 276 cenas são 251.** `amplitude.log`: «cenas 2022-2026 com nuvem <30 %:
276 (...) válidas: 251». `amplitude_serie.json` tem 251 entradas. 276 é o
número encontrado, 251 o número usado. A adenda escreve «medida em 276 cenas».

**Os números de L8 não estão em nenhum JSON.** `amplitude.py` escreve amplitudes
**absolutas**; L8 publica razões à referência (0,97 / 0,95 / 0,76 / 0,54 / 0,30
para o OESTE; 0,10 e 0,65 para o N3). A divisão reproduz-se de
`amplitude.json`, mas **não está em código nenhum** — foi feita fora do
registo.

**E o denominador é instável, o que é o item grande.** As amplitudes absolutas
da referência, de 2022 a 2026: **0,601 · 0,590 · 0,265 · 0,538 · 0,277**. A
referência perde metade da sua própria amplitude em 2024 e outra vez em 2026 —
e o `piso_inverno_tabela.json`, da mesma sessão, mostra porquê: no Inverno de
2023/24 **todas** as unidades sobem o piso em bloco (referência 0,529, resto do
pomar 0,514, contra 0,30-0,33 em todos os Invernos anteriores), e em 2025/26
outra vez (0,575 e 0,573). É um efeito de época e de amostragem — de que meses
tiveram cena limpa e de quão verde estava o coberto — não das plantas.

Com isso, o número mais citado de L8 desfaz-se. **A «recuperação» do N3 a 0,65
em 2026 é o denominador a cair, não o N3 a subir.** Em absoluto: N3 vai de
0,052 para 0,180 enquanto a referência vai de 0,538 para 0,277. Contra um
denominador estável (~0,60) o N3 leria 0,30, não 0,65. E a componente que se
moveu é a errada para a leitura que dela se tira: o piso de Inverno do N3 desceu
de 0,654 para 0,497, enquanto o pico de Verão **desceu** de ~0,71 para ~0,65 e
continua 0,20-0,26 abaixo da referência. **Uma videira jovem a pegar fecha-se
sobre a referência no Verão. Esta afasta-se.** O que os números descrevem é
terreno que tinha coberto verde no Inverno de 2024/25 e deixou de o ter — chão
limpo mantido, não replantação.

**Se cair, o que cai com ele.** A segunda leitura de `REGISTO_IFAP.md` §1.4 («é
a que a amplitude sazonal sustenta: videira jovem») e o valor 0,65. **Não cai** o
0,10 de 2025, que é enorme em qualquer normalização, nem a monotonia do OESTE,
cuja direcção é robusta ao denominador ainda que os valores não sejam.

---

## 2. Factos a manter, com margem maior

### W1 · O Landsat é o melhor trabalho do dia — e não está no PASSA PARA CIMA

Registo-o com a clareza com que ataquei o resto. `landsat.json` dá, para o foco
OESTE com pérgola, fosso à referência de **−0,004 a +0,004 em onze anos
consecutivos** e depois 0,046 e 0,146; e o nível da própria referência a cair
0,888 → 0,874 → 0,862, isto é, **−0,026 contra os −0,054 do Sentinel-2**. Isso é
uma quantificação independente de quanto da queda da referência é real e quanto
é o viés do S2C, e responde ao pedido que o certificado da C2 deixou escrito em
NÃO TESTÁVEL. É outra agência, outro sensor, outra cadeia de correcção.

**E não aparece em L1–L8.** A lista fechada que passa para cima não contém o
resultado mais forte que a sessão produziu. Isso é, ao contrário, uma coisa a
sair pela porta do lado.

**Três margens que têm de alargar, e a primeira é séria.**

1. **O cabeçalho promete dois resguardos que o código não tem.** Diz: «por isso
   só se usam píxeis **inteiramente dentro** da unidade, e reporta-se o n». Não
   há filtro de pureza nenhum e não há `n` nenhum. O que o código faz é
   reprojectar 30 m para a grelha de 10 m com `RS.nearest` e depois indexar as
   máscaras. Cada píxel Landsat replica-se em ~9 células. «ESTE com pérgola»
   (1,27 ha) e «ESTE sem pérgola» (1,28 ha) são um corte pela mediana de um
   campo de altura dentro do **mesmo disco de 90 m** — logo interdigitados a 10 m
   e, a 30 m, **em grande parte os mesmos fotões**. Qualquer contraste entre as
   duas está atenuado para zero e qualquer concordância está fabricada. É a
   segunda vez neste corpo de trabalho que um cabeçalho afirma um resguardo que
   o código a seguir não implementa.

2. **±0,004 em onze anos é bom demais.** Ruído de NDVI de reflectância de
   superfície entre duas unidades, com 6 cenas em 2019 e 6 em 2021, não fica
   estável a 0,4 %. A explicação natural é a mesma: a referência sistemática é
   1,10 ha espalhada sobre 30 ha e, a 30 m, muitos dos seus píxeis são os
   mesmos píxeis do resto do pomar e possivelmente do disco OESTE. **Isto não
   destrói o resultado** — o salto de 2025-26 é grande de mais para ser
   partilha de píxeis — mas destrói a linha de base como medida de estabilidade.
   A ressalva de saturação já está declarada em `REGISTO_IFAP.md` e é correcta;
   a de partilha de píxeis não está e é maior.

3. **A série atravessa L8 → L9.** 101 cenas de landsat-8 e 39 de landsat-9, e o
   campo `plataforma` está gravado cena a cena. O cabeçalho declara imunidade ao
   viés do S2C, o que é verdade, e não menciona que introduz a sua própria
   transição de sensor a meio — o confundente que esta cadeia identificou como o
   maior de todos. É uma linha de código verificar.

**E uma defesa que a sessão tinha e não usou.** O NDMI da referência lê 0,470 a
0,516 em catorze anos, isto é, a meio da gama e longe de saturar, e conta a
mesma história ano a ano. Isso é a resposta directa à objecção de saturação do
NDVI, e é mais forte do que a ressalva que o registo escreveu. Fica por dizer
que NDVI e NDMI partilham a banda NIR e não são independentes um do outro.

### W2 · L7 e as manchas de V8 — aguentam, com dois acertos

`refazer_c2_este.json` reproduz as três manchas junto ao foco ESTE a 0,55 /
0,61 / 0,25 ha com 71 / 87 / 92 % de pérgola. **Aguenta**, e é a resposta boa à
pergunta que o adversário anterior disse faltar ao ramo ascendente.

Dois acertos. O texto escreve «0,55 / 0,61 / 0,25 ha a 60, 75 e 166 m»; o JSON
tem 0,55 ha a **74,7 m** e 0,61 ha a **60,0 m** — áreas e distâncias trocadas. E
a mancha de 0,55 ha tem altura mediana **1,466 m**, abaixo do próprio limiar de
1,5 m com que a adenda define presença de pérgola. «Não é chão» está certo;
«tinham pérgola completa» não está, para essa mancha.

### W3 · L1, a data do voo — plausível, e hoje não é falsificável

A derivação pelo tempo GPS dos pontos é a coisa certa a fazer, e o aviso de que
o `datetime` da API é geração de produto e não voo é um bom aviso. Mas:

- **não há script.** Nenhum ficheiro em `_VALIDADE_GESTAO\` lê um LAZ; o
  `laz_ids.json` só tem nomes de folha;
- **a resposta coincide com o nome do ficheiro.** As folhas chamam-se
  `MDT-50cm-LO-158565-**07-2025**` e o `obter_mds.py` procura literalmente
  `-07-2025` na regex. Uma data derivada que cai dentro do que o nome do
  ficheiro já dizia, sem cálculo em disco, é a configuração que abriu esta
  cadeia — uma pasta chamada `sentinel_b1\`;
- **a premissa concreta que ninguém nomeou:** em LAS 1.4 o campo de tempo é
  GPS Week Time ou Adjusted Standard GPS Time consoante o bit 0 do
  `global_encoding`. Lido como o outro, o dia sai errado por muito.

**Dado que preciso e não vou buscar:** `laspy.read(LO-158565).header.
global_encoding` e o mínimo e máximo de `gps_time`, com a conversão escrita.
Duas linhas fecham isto e transformam L1 de asserção em prova. Até lá, L1 é
provável e não é certificável — e é dele que dependem L2 a L7.

### W4 · L5, a moeda do fosso — correcta, conservadora, e incompleta

Passar de nível absoluto para fosso é exactamente o que o adversário anterior
pediu em R3, e a adenda fá-lo e declara honestamente que o degrau do OESTE em
copado **perde significância** (p = 0,091) — uma declaração que não a favorece.
Bom.

Falta publicar a linha que a acompanha e que é a mais forte do ficheiro
(«resto do pomar, com pérgola»: degrau **−0,0316**, razão 0,29, **p = 0,0082**),
e falta notar que, nas duas unidades que a adenda classifica «DEGRAU», o modelo
**linear** tem p menor do que o degrau: ESTE com pérgola p_b = 0,015 contra
p_degrau = 0,042; ESTE «plantado» p_b = 0,0069 contra 0,029. A razão de somas de
quadrados escolhe o degrau; o teste de declive prefere a recta. Os dados não
separam «degrau» de «declínio a acelerar», e o certificado só publica a métrica
que escolhe.

### W5 · As duas retiradas — **ambas legítimas**, e ambas enterram um resultado

O prompt pergunta se as retiradas se sustentam ou se os testes não tinham
potência. Respondo item a item, porque a resposta difere.

**`terreno_contra_declinio.py` — a retirada é sólida, e mais do que sólida.** A
hipótese foi fixada antes de correr, na direcção certa, e o `terreno_declinio.
json` não a deixa por confirmar: **contradiz-a**. O ρ da cota é negativo nas
onze cenas (−0,20 a −0,46, p < 1e-24) — o défice está no terreno **alto** — e
nada emerge em 2025-26; a área drenante, que era positiva e significativa até
2024, **cai para zero** nos anos do evento. Potência sobra: efeitos de |ρ| ≈ 0,2
detectados sobre ~2 200 células. A retirada está bem fundamentada.

Duas ressalvas, e nenhuma a inverte. (a) **O TWI não tem gama.** Sobre um pomar
nivelado, ln(a/tan b) varia pouco e o ρ ≈ 0 não é informação — essa linha devia
ser NÃO TESTÁVEL, não retirada. O log do script imprimia o intervalo do TWI e
**não foi guardado**. (b) **O nulo honesto foi desenhado e nunca implementado.**
O cabeçalho diz, correctamente, que com autocorrelação de 0,86-0,96 permutar
células torna tudo significativo, e que o nulo é a própria série. O código
reporta na mesma o p assintótico do `spearmanr` e deixa a comparação entre anos
ao olho.

E o olho, aplicado à linha certa, vê uma coisa que não foi reportada: **dentro
do foco OESTE, a área drenante inverte de sinal e emerge nos anos do evento** —
+0,116 · +0,122 · +0,144 · +0,069 · +0,203 · +0,009 · −0,122 · −0,201 · −0,163 ·
−0,252 · −0,226. Pelo critério de leitura que o próprio script imprime
(«Emerge só em 2025-26 → o evento tem assinatura topográfica»), essa linha
emergiu, com o sinal contrário ao da hipótese. Com autocorrelação e ~200
células é uma pista, não um facto — mas retirar a hipótese e arquivar a corrida
deita fora a pista.

**`rede_de_rega.py` — a retirada é legítima quanto a 2026, e o teste é
inconclusivo por desenho.** O agrupamento por válvula fica dentro do nulo
rodado em todas as onze cenas (p de 0,175 a 0,64) e não emerge; o critério de
falsificação escrito no cabeçalho cumpriu-se. Até aqui, correcto.

Mas o segundo teste — «ordem na rede» — não pode responder ao que pergunta.
`ORIG = (530360, 4654848)` fica a **240 m do foco OESTE**, dentro da metade
ocidental de uma parcela de 1 458 m. **«Distância à origem» é, nesta geometria,
quase «distância ao foco OESTE».** Em 2026 o foco OESTE é a pior área; logo o
mais próximo da origem é o pior; logo ρ tem de ser negativo. É −0,140. O
resultado é uma consequência mecânica da posição da origem, não um teste de
topologia de rega. E o mesmo desenho produz, sem explicação e sem publicação,
**ρ = +0,909 (p < 0,001) em 2021 e +0,874 em 2022** sobre n = 12 — que é,
igualmente, o gradiente oeste-leste a dizer-se por outras palavras.

Acrescento que a topologia existia em disco e não foi usada:
`_VALIDACAO_CAMADAS\valvulas_por_linha.json` dá posição por número de linha do
esquema de rega, com `_incerteza_m: 25` e a nota de que as válvulas 1-5 estão
«POR COLOCAR». O script carrega `valvulas_por_area.json`, uma quarta derivação
das posições das válvulas — e o adversário anterior já tinha assinalado, em W6,
que 34 / 35 / 43 m circulavam sem explicação para a mesma válvula.

**Veredicto sobre as retiradas: nenhuma das duas é uma retirada mal fundada.**
Uma delas (terreno) é exemplar. A crítica é outra e é menor em gravidade: uma
retirada não deve fechar o ficheiro sobre resultados que a corrida produziu, e
nenhuma das duas está registada em documento nenhum — os dois scripts correm às
11h52 e 11h54, depois de a adenda estar escrita às 11h20, e não existe registo
que os cubra.

### W6 · O piso de Inverno — o melhor resultado não publicado da sessão

`piso_inverno_tabela.json` mede o piso de Dez-Fev por unidade em nove Invernos.
No Inverno de **2024/25** o N3 lê **0,654** contra **0,358** da referência e
0,367 do resto do pomar — trinta pontos de NDVI acima do pomar, na estação em
que a videira caduca está nua. Nos Invernos de 2018/19 a 2022/23 o N3 estava em
0,25-0,34, indistinguível de todos os outros. Em 2025/26 volta a 0,497 contra
0,575 da referência.

Isto é uma medição **de Inverno**, que é a estação certa para separar videira
caduca de coberto permanente, é feita sobre 8 e 6 cenas, corrobora
independentemente os 0,27 m que o LiDAR mede no N3, **e data a transição**: o N3
ficou verde no Inverno de 2024/25 e deixou de o estar em 2025/26. É melhor
prova do que a amplitude de Verão de L8 e não é citada em lado nenhum.

---

## 3. A pergunta que falta

*(transversal B)*

**A adenda declara, numa caixa, o limite para a frente da sua partição. Nunca
declara o limite para trás — e é para trás que ela a usa.**

O aviso final está escrito e está certo: «A partição vale até 06-07-2025 e é
hipótese depois disso. (...) nada aqui prova que a mantiveram em Julho de
2026.» Excelente. Só que a partição é aplicada muito mais vezes na outra
direcção, e essa direcção nunca aparece.

`refazer_c2_este.py`, V10 refeito, calcula `dfc & SEM` para **2017**. Isto é:
classifica o défice de 2017 como «sem pérgola» com base numa medição de altura
feita oito anos depois. `serie_separada.py` faz o mesmo com toda a série:
`LIMPO = POMAR & (h < 0.5)` é fixo, e a mesma máscara de 2025 decide o que era
«chão limpo» em 2017, 2018, 2019.

**O que teria de ser verdade para isto estar errado.** Que alguma parte dessas
3,77 ha tenha tido copado durante a janela e o tenha perdido dentro dela. Não é
uma possibilidade remota: é a hipótese central do caso. Se um talhão tinha
pérgola em 2017, entrou em défice em 2020, morreu, e foi limpo em 2023, então:

- em 2017 ele é copado são e a partição chama-lhe «chão limpo»;
- todo o seu percurso de declínio é retirado da série sanitária e arrumado em
  «decisão de gestão»;
- **a série «só onde havia pérgola» apaga exactamente a mortalidade que já se
  completou**, e conserva apenas a que ainda está a decorrer.

Isso não enfraquece o «parte de zero» de L6. **Explica-o.** Uma série construída
para conter apenas o que ainda estava vivo em 2025 tende, por construção, a ler
baixo nos anos intermédios — porque tudo o que morreu antes disso foi
reclassificado como gestão. E a taxa de base que o adversário anterior calculou
em W2 aponta na mesma direcção: o défice de 2026 é 2,7 vezes mais provável sobre
terreno com histórico.

**Porque é que a sessão podia ter perguntado, e não perguntou.** Tinha os dois
instrumentos na mesa. `piso_inverno_tabela.json` dá o piso de Inverno por
unidade desde 2016/17: uma unidade que era videira caduca e passou a coberto
permanente muda o piso, e o N3 mostra que a assinatura é visível e datável.
`amplitude_serie.json` tem 251 cenas de 2022 a 2026 sobre as mesmas unidades. O
que falta é uma linha: **correr a curva de amplitude e o piso de Inverno sobre
as 3,77 ha de `h < 0,5`, ano a ano desde 2016**, e ver em que ano cada pedaço
deixou de foliar. Se todas deixaram antes de 2017, a partição retroactiva é
segura e a adenda ganha o argumento por inteiro. Se alguma deixou em 2019 ou
2021, a série sanitária de F9 está retro-ajustada e L6 muda de sinal.

**Há um sinal no próprio material que torna a pergunta obrigatória.** O
`serie_separada.json` mostra `limpo_ha` entre 1,32 e 2,61 ha em **todos** os
anos, incluindo 1,81 ha em 2017, com `fosso_limpo` já em 0,2525 nesse ano. Uma
parte daquele terreno estava, de facto, despida desde o início — o que é a boa
notícia para a adenda. Mas a área varia 1,32 → 2,61 ao longo da série, e a
variação é quase toda entre 2024 e 2025 (1,92 → 2,59). **Alguma coisa naquela
área mudou dentro da janela**, e a partição, sendo estática, não pode dizer o
quê. A `nu2021` — a máscara que a adenda substitui — era de 2021 e dava a
mesma resposta para 2017-2024 a poucos pontos (R4). O que faz falta não é uma
máscara melhor: é **uma segunda data**.

**Porque é grave agora.** O `CAMADA_3_PROMPT.md` está escrito e a C3 vai
georreferenciar 212 registos de laboratório contra este padrão. Se a área de
amostragem for definida por «copado vivo em 06-07-2025», a C3 procura patogénio
onde a planta sobreviveu e **não** onde ela morreu — que é o desenho de
amostragem exactamente ao contrário. Uma única linha na lista de perguntas ao
gestor resolve o essencial, e é da mesma família das três que
`REGISTO_IFAP.md` §4 já faz: **em que anos foi arrancado cada talhão a leste, e
o que lá estava antes.** É facto de tipo 1 e corrige-se perguntando.

---

## 4. Os cinco testes de cinco minutos, por valor

Ordenados por confiança ganha por esforço. Todos correm sobre ficheiros já em
disco, excepto o T5, que precisa de abrir dois ficheiros já descarregados.

**T1 · A contagem sem abertura.** *(três linhas)*
`((nd < r − 0,05) & VIVO).sum()` para 2022, 2023 e 2024, sem
`binary_opening`, e depois aos limiares 0,04 / 0,05 / 0,06. Decide L6 e a
figura F9 de uma vez. Se o zero se mantiver sem abertura e resistir a mover o
limiar, é um facto e passa com honra; se se transformar em 0,5-1,0 ha, o «parte
de zero» sai e a série publicada tem de trazer a coluna «perdido na costura».
Primeiro lugar porque L6 é o item mais citável de toda a adenda e o mais frágil.

**T2 · A varredura do limiar de altura.** *(um ciclo sobre `chm_altura.npy`)*
Repetir o contraste de L4 — degrau, razão e p em copado e em chão — a 0,3 /
0,5 / 1,0 / 1,5 m, e reportar as quatro linhas lado a lado. Com o limiar
operativo a cair a 0,03 m da mediana da unidade que parte, isto diz se L4 é um
facto sobre o pomar ou uma propriedade do corte. Reportar também, em qualquer
dos casos, o degrau de **+0,0531** que o chão dá hoje.

**T3 · Os píxeis distintos do Landsat.** *(dez linhas)*
Contar quantos píxeis Landsat de 30 m distintos contribuem para cada unidade, e
quantos são partilhados entre pares de unidades — em particular entre
«referência» e «resto do pomar», e entre «ESTE com pérgola» e «ESTE sem
pérgola». É o `n` que o cabeçalho promete e não entrega. Decide se «onze anos
indistinguíveis» é uma medição ou uma consequência de partilha de píxeis, e
decide se o par com/sem pérgola do Landsat mede duas coisas ou uma.

**T4 · Publicar o piso de Inverno, e estendê-lo às 3,77 ha.** *(quase nada a
computar)*
A tabela dos nove Invernos por unidade já existe em
`piso_inverno_tabela.json` e não está publicada. Acrescentar-lhe uma unidade —
`POMAR & (h < 0,5)` — e uma coluna com a diferença à referência. Isto ataca
directamente a pergunta da parte 3, data a transição do N3 melhor do que a
amplitude de Verão, e custa uma máscara.

**T5 · Duas linhas de proveniência.** *(dois `open`)*
`rasterio.open(<uma folha MDS>).nodata` — para saber se o `nodata=-999.0`
imposto no `merge` corresponde ao nodata nativo das folhas DGT. Se não
corresponder, píxeis sem dados passam com o mesmo valor no MDS e no MDT, a
subtracção dá **0,00 m**, `np.isfinite` aceita-os, e vazios de LiDAR entram como
«sem pérgola» — um caminho directo do vazio para a conclusão. O log do
`altura_copado.py`, que imprimia «% com dados» e a mediana do CHM, **não está em
disco**. E `laspy.read(LO-158565).header.global_encoding`, com a conversão de
tempo GPS escrita, para L1 deixar de ser asserção.

---

## 5. Transversais A, C, D — e veredicto

**A · A regra do instrumento independente.** Este é o dia em que a regra podia
finalmente cumprir-se, e cumpre-se em parte.

*Cumprem a sério:* **o foco OESTE como copado vivo** (LiDAR contra Landsat
contra NDVI: geometria, óptico de outra agência, e a série própria, três
proveniências a dizer o mesmo); **a fronteira com/sem pérgola** (LiDAR contra
parcelário IFAP — geometria contra documento, sem contacto entre si, e é a
melhor peça do `REGISTO_IFAP.md`); **o N3** (LiDAR a 0,27 m contra piso de
Inverno a 0,654, se o T4 correr).

*Têm um instrumento com outro nome:* **L4**, cujas duas metades vêm do mesmo
campo de altura cortado ao meio e cuja série é a mesma série de NDVI; **L8**,
que a adenda diz «independente do LiDAR» — é, mas é Sentinel-2 NDVI, o
instrumento que produziu tudo o que se está a verificar; **R4/V10**, onde as
duas máscaras concordam entre si e a divergência é com o certificado.

*Não têm nenhum, e a adenda não o declara:* **L6**, que é uma reorganização
aritmética de uma só série; **L2**, cuja etiqueta o único documento disponível
contradiz em 65 %.

**C · Entrou alguma coisa pela porta do lado?** Quatro itens, e um deles é o
inverso.

1. **Quatro saídas sem código.** `altura_focos.json` (que contém L2 e L3),
   `sem_pergola.npy`, `ifap_exploracao.json` e `ifap_exploracao_total.json` (que
   contém as 44,36 ha) não são escritos por nenhum `.py` em disco. A data do
   voo e a normalização de L8 também não. Regra 3 do protocolo.
2. **A inferência hidráulica/vascular** entrou do `REGISTO_IFAP.md` §2 para o
   cabeçalho do `terreno_contra_declinio.py` como premissa de desenho, sem
   passar por camada nenhuma. É C4 a correr dentro da C2.
3. **A frase «Onde o LiDAR não vê pérgola, o beneficiário declarou erva,
   forragem ou nada»** contradiz a linha do seu próprio JSON (65,0 % KIWI).
4. **E uma coisa boa saiu pela porta do lado:** o Landsat, com o melhor
   resultado do dia, não está em L1–L8.

**D · As quantidades-âncora.** **A adenda não reporta nenhuma.** O Controlo 2
exige que todas as camadas reportem as dez, sempre, mesmo sem lhes tocar. As
que se conseguem extrair dos scripts batem com a C2 (polígono 3 031 células /
30,31 ha; referência 110 células / 1,10 ha), continuam a divergir do
`CONTROLOS.md` (2 903 / 29,0 / 454) pela rederivação geográfica já explicada
em camadas anteriores, e aparecem agora com uma âncora nova por declarar: a
partição 26,54 + 3,77 = 30,31 ha. **Acrescento uma divergência que ninguém
declarou:** o `altura_copado.py` usa discos de **raio 70 m** para N1/N2/N3
enquanto `discos_dos_focos` usa **90 m**, e o quadro da adenda mistura as duas
famílias na mesma coluna — «foco ESTE da cadeia» (90 m, 2,55 ha, 0,47 m) e «N3
do analista B» (70 m, 1,43 ha, 0,27 m) — sendo que, como o próprio
`amplitude.py` declara no seu cabeçalho, **o N3 está a 95 m do foco ESTE, fora
do disco**. São objectos distintos apresentados como aninhados.

---

## Veredicto

**A adenda não pode substituir partes do certificado da C2 como está. Volta à
origem em dois pontos, segue com retiradas nos restantes.**

*Volta à origem:*
**L4** e **L6**. As duas são as afirmações mais fortes do documento e as duas
caem por mecanismos internos, não por dúvida geral: L4 porque o placebo mediu
+0,0531 contra +0,0585 e foi lido como nulo por ruído; L6 porque a abertura
morfológica apaga 30-41 % do défice na costura da partição precisamente nos anos
que leem zero. **T1 e T2 decidem as duas em dez minutos.** Até lá não passam, e
a figura F9 não deve circular.

*Segue com as retiradas de R3 a R8:* a etiqueta «pérgola / chão» passa a
«altura mediana ≥ ou < 0,5 m»; a linha 3 do CORRIGE deixa de atribuir ao LiDAR
uma correcção que ele não fez; o cruzamento IFAP passa como fronteira
qualitativa e não como validação de área, e a frase «a mais forte de sempre»
sai; a leitura água-contra-verdura sai por completo, com a inferência etiológica
que dela deriva; a assinatura espectral passa como **piso de Dez-Fev** e não
como amplitude; L8 passa com o denominador declarado, 251 cenas e sem a leitura
de «recuperação» do N3.

*Não passa nada que dependa de L1 enquanto L1 não tiver o cálculo em disco.* São
duas linhas de `laspy`. Enquanto não existirem, o facto fundador desta adenda
tem o mesmo estatuto epistémico que a pasta `sentinel_b1\` tinha em 27 de
Agosto: provavelmente certo, e sem prova.

*O que passa intacto, e é bastante:*
**A série Landsat** — que deve entrar na lista fechada, com a ressalva de
partilha de píxeis e a de L8→L9, porque é a resposta ao pedido que o
certificado da C2 deixou em NÃO TESTÁVEL e é a única peça do dia com
proveniência genuinamente externa.
**A altura de copado como medição** — 2,34 m e 99,2 % na referência contra
0,09 m no terreno lavrado é um contraste que nenhum limiar entre os dois estraga,
e é a primeira vez que este caso mede geometria.
**A fronteira LiDAR × parcelário** — 99,4 % de kiwi declarado acima do limiar
contra 65,0 % abaixo, e todas as culturas anuais do lado de baixo. É geometria
contra documento e é limpo.
**L7** — as manchas de declínio novo têm pérgola, com o acerto de W2.
**As duas retiradas de hipótese**, ambas legítimas, uma delas exemplar.
**A retirada do teste de prominência** em `REGISTO.md`, e a regra que dela sai.
**O aviso final da adenda** — que a partição é uma data — que está certo, é
raro, e cujo único defeito é apontar só para um dos lados.

Este dia produziu mais prova nova do que qualquer dia anterior desta cadeia. Se
sobrevive mais estreito, é porque o instrumento novo permitiu, pela primeira
vez, perguntas que antes não se podiam fazer — e algumas delas voltaram-se
contra quem as fez, que é o que se espera de um instrumento a sério.
