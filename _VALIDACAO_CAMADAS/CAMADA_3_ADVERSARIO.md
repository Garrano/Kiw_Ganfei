# Camada 3 — adversário do certificado

29-08-2026. Sessão adversarial. Lidos: `CAMADA_3_CERTIFICADO.md`, `PROTOCOLO.md`,
`CONTROLOS.md`, `ADVERSARIO_PROMPT.md`, `CAMADA_3_PROMPT.md`,
`CAMADA_0_REVISAO_R2.md` (+ suplemento G34–G37), `CAMADA_1_CERTIFICADO.md`,
`CAMADA_2_CERTIFICADO.md` nos trechos citados, `CAMADA_2_ADVERSARIO.md`,
`CAMADA_2_ADENDA_LIDAR.md` (nas duas versões — a que a C3 leu e a que hoje traz
o aviso de retirada), `ADVERSARIO_2026-08-29.md`, e os doze scripts, oito JSON e
dois CSV de `SAIDA_C3\`, mais `c2_00_comum.py` e `c1_06_solo_colocado.csv`.

**Nenhuma cena foi aberta, nenhum LAZ foi lido, nenhuma análise foi refeita.** O
que se leu além do código foram as folhas dos dois livros-fonte tal como a
própria camada as despejou em `c3_05_folhas.txt` e `c3_04_registo_principal.csv`
— isto é, os documentos que sustentam a paragem de linha, que não se podem
julgar sem ver.

---

**Nota de abertura, para o registo ser honesto.** Esta camada faz duas coisas
que nenhuma anterior fez. Correu o **T1** que o adversário da C2 pôs como
condição de arranque e que ninguém tinha corrido — e correu-o contra si própria,
porque o resultado obriga a mexer no denominador de toda a C2. E escreveu uma
secção **NÃO TESTÁVEL** com oito entradas, cada uma com o pedido concreto que a
fecharia, o que é a coisa mais rara neste processo. A `Rosellinia` (B9) é o
melhor facto produzido em qualquer camada desde o início: duas datas, dois
campos separados, uma inversão de sentido, e nenhuma inferência por cima.

O ataque que se segue é duro porque há material para atacar. **O achado
principal não é nenhum dos quatro que a C3 nomeou na sua «Nota ao adversário que
não vou ter».** São dois, e estão nas partes 1 (R1) e 3.

---

## 0 · A PARAGEM DE LINHA — veredicto primeiro

O prompt desta sessão diz que uma paragem de linha mal fundamentada é tão grave
como uma afirmação mal fundamentada, e manda atacar nas duas direcções. Aqui
está o resultado das duas.

### 0.1 · O facto: a rejeição está certa, e por razões melhores do que as dadas

Fui verificar os **três sítios independentes** que o certificado invoca. Existem
todos os três e dizem o que o certificado diz que dizem:

1. Coluna `Location_Confidence`: **20** registos com «DESCONHECIDO — alerta:
   código da amostra não associado a nenhum talhão/parcela nos ficheiros
   revistos» (as quatro ITS, cinco linhas cada) e **15** com «DESCONHECIDO —
   alerta: sem código de terreno/talhão no documento de origem» (o «Kiwi 1000»).
   35 no total. *(`c3_04_perfil.json`)*
2. Rodapé da folha `Diversidade ITS`: «ALERTA: nenhuma destas 4 amostras tem
   código de talhão/terreno nas páginas do relatório extraídas.»
   *(`c3_05_folhas.txt`)*
3. `Pontos a Esclarecer`, linhas 1 e 2 — o «Kiwi 1000» («NÃO tem qualquer código
   de talhão/terreno») e as ITS («nenhum indica talhão, freguesia ou data de
   amostragem»). *(idem)*

**Mas «três sítios independentes» é a descrição errada, e a camada devia
sabê-lo.** São três anotações do mesmo compilador dentro do mesmo livro,
escritas com a mesma ressalva («nas páginas **extraídas**», «nos ficheiros
**revistos**»), e reduzem-se todas a uma só observação de origem: *as páginas
extraídas dos PDF não têm código de talhão*. Isso é **um** instrumento com três
frases. Aplicar-lhe a etiqueta «independente» é a violação de controlo 1 que o
adversário da C2 apanhou na V4 e que esta camada não escapou.

**E ao mesmo tempo a evidência real é mais forte do que a citada.** O que os
dados mostram, e o certificado não escreve, é que nas vinte linhas das ITS
**todos os campos de identificação estão vazios ao mesmo tempo**:

```
Terrain_Block_Parcel : NÃO ESPECIFICADO — não foi encontrado código de talhão
Sample_Date          : Not stated in extracted pages
Lab_Provider         : Not identified in extracted pages
Parish_Municipality  : Not stated in extracted pages (orchard context = Ganfei,
                       Valença, PRESUMED)
```

Cinco colunas, todas vazias, e o próprio livro a marcar a atribuição ao pomar
como **presumida**. Isso é muito mais do que «não têm código de talhão». **A
rejeição da linha «amostras» da G34 aguenta, e aguenta com folga.**

Uma correcção de sentido inverso, porque a camada não a fez e ela limita a
rejeição: o `Client_Titular` das quatro ITS é **«Fauna Útil SL (titular/
submitting org)»** — que é **exactamente** o mesmo titular submissor dos cinco
informes de nemátodes 339–343/2026, os únicos com código de talhão do caso. As
ITS partilham submissor com as amostras colocadas. Isso não lhes dá talhão, mas
torna insustentável a frase «não podem ser atribuídas ao foco OESTE **nem a lado
nenhum**». Não podem ser atribuídas a um **talhão**. A atribuição ao pomar é
presumida, como o livro diz, e é plausível.

### 0.2 · O procedimento: a paragem de linha está mal fundamentada, e por dois motivos

**Motivo 1 — a razão dada para não parar é falsa pelos números da própria
camada.**

O certificado escreve: «Não há nada por cima que dependa da linha rejeitada e
que eu esteja a construir: a rejeição é o produto.» Isto não é verdade. Quatro
dos onze factos da lista fechada são construídos **em cima** da rejeição:

| facto | como depende |
|---|---|
| **B5** | «A v8 tem **zero** registos.» Se a linha da G34 estivesse certa, as vinte linhas das ITS estariam no foco OESTE e a v8 teria vinte registos. B5 é a rejeição outra vez, com outro nome. |
| **B4** | «Nove dos vinte resultados vêm de uma amostra **sem posição**.» Cai inteiro se o «Kiwi 1000» tiver lugar. |
| **B3** | Nove das vinte linhas classificadas «sem posição» são **as nove do Kiwi 1000**. |
| **B2** | Dos 110 sem posição, 53 são «sem posição declarada» — 35 dos quais são as ITS e o Kiwi 1000. |

A regra 2 do protocolo é literal: «Se uma sessão rejeitar um facto certificado
por uma camada abaixo, **pára**. Não continua a construir por cima.» A C3
rejeitou, e depois construiu quatro factos por cima, escreveu-os numa lista
fechada, **e escreveu o `CAMADA_4_PROMPT.md`**, que já os transporta verbatim
(linhas 244, 252, 257 desse ficheiro). Não é uma paragem de linha parcial. É uma
rejeição seguida de continuação normal, com uma caixa de aviso em cima.

**Motivo 2 — o instrumento não alcança o facto, e a acusação vale nos dois
sentidos.**

O certificado acusa a C0, correctamente, de «asseverar um facto de biologia com
um instrumento que não o alcança». Mas repare-se na simetria. A G34 aparece no
**suplemento** da R2, sob o cabeçalho «três coisas vieram do gestor», ao lado da
G35 (a tabela de áreas do gestor) e da G36 (as coordenadas do B1 dadas pela
gestora). Se a linha «amostras» veio da mesma origem que as outras três, então é
**testemunho directo** — a classe de facto que o `CLAUDE.md` deste projecto
define como «alguém esteve lá e sabe», e sobre a qual escreve: «Não se corrige
com réplica; corrige-se **perguntando outra vez a quem sabe**.»

E o instrumento com que a C3 a derruba é o **silêncio de um documento**. Um
livro que não regista o talhão não prova que ninguém saiba o talhão; prova que
as páginas extraídas não o dizem — que é literalmente o que as três anotações
declaram. Derrubar testemunho com ausência documental é a operação exactamente
inversa à que a regra do projecto manda.

**A C3 nunca pergunta de onde veio a linha.** Não está em NÃO TESTÁVEL, não está
na paragem de linha, não está no prompt da C4. A pergunta «quem disse que as
quatro ITS são do foco OESTE, e com base em quê?» não aparece em lado nenhum, e
é de uma linha.

### 0.3 · Veredicto sobre a paragem de linha

**A paragem de linha mantém-se quanto ao facto e altera-se quanto ao
dispositivo.**

- **Mantém-se** que **nada nos dois livros coloca as quatro ITS ou o «Kiwi 1000»
  num talhão**, e que a G34 não podia ter escrito o contrário com o material que
  tinha. Isto está estabelecido, com evidência mais forte do que a citada
  (§0.1), e nenhuma frase da G34 sobre esforço de amostragem pode ser usada pela
  C4.
- **Altera-se** o estatuto: de **REJEITADO** para **NÃO RESOLVIDO — conflito
  entre relato e documento, com a precedência por decidir**. Uma afirmação
  documental negativa não refuta testemunho directo; suspende-o. A diferença não
  é semântica: com «REJEITADO», B5 lê-se «a v8 nunca foi amostrada»; com «NÃO
  RESOLVIDO», lê-se «a v8 não tem nenhuma amostra que os documentos consigam lá
  pôr», que é uma afirmação bastante mais fraca e é a que os dados suportam.
- **A paragem de linha está mal executada.** Quatro factos foram construídos por
  cima do facto rejeitado, e o prompt da camada seguinte foi escrito e entregue.
  A frase «não há nada por cima que dependa da linha rejeitada» tem de sair.
- **O reinício formal em C0 é de uma linha e deve correr**, com uma pergunta
  única ao gestor: *de onde veio a atribuição das ISFBV0314–17 e do «Kiwi 1000»
  ao foco OESTE?* Se a resposta for «da minha memória», a linha volta como
  testemunho e a C3 reescreve B3, B4 e B5. Se for «de nenhum lado, foi
  inferido», a rejeição consolida-se e a C3 reescreve na mesma B5, porque a
  ausência continua a ser documental e não física.

---

## 1 · Factos a retirar do PASSA PARA CIMA

Oito retiradas. Como nas duas sessões anteriores, quase nenhuma apaga uma
medição: o que cai é a frase que liga os números. **Duas são de outra
natureza** — R1 é um facto sem origem nenhuma, e R2 é uma afirmação que o
próprio código não consegue produzir ao contrário.

---

### R1 · A linha Becrop do CONFIRMADO — **um facto que não existe em lado nenhum**

**Retira-se a coluna de instrumento independente inteira.**

O certificado dá, como instrumento independente da linha «os dois Becrop não são
comparáveis»:

> «os próprios relatórios: a categoria «podredumbre radicular» passa de **risco
> MUITO ALTO detectado** a **«No Detectado»** nos mesmos 163 dias, o que mede a
> instabilidade do instrumento e não do pomar»

**Esta categoria não existe.** A folha `Relatorios Becrop` do livro PT tem nove
linhas e nenhuma delas é podridão radicular:

```
0  Total de espécies detectadas                 856 | 720
1  Biosostenibilidad                            MEDIO (41) | MUY ALTO (82)
2  Biodiversidad / Funcionalidad / Resiliencia
3  Estado de salud del cultivo / Biocontrol     Salud: Muy bajo | Salud: Alto
4  Principais filos fúngicos
5  Principais filos bacterianos
6  Ratio Hongo-Bactéria / Arbuscular-Ectomicorriza
7  (vazia)
8  ALERTA: 'No hay parcela asociada' ...
```

Procurei «podred», «podrid», «root rot», «radicular», «No Detectado» e «MUITO
ALTO» em `c3_05_folhas.txt` (que é o despejo integral das folhas auxiliares dos
dois livros), no `c3_04_registo_principal.csv` (os 221 registos, 22 colunas), e
em todo o `_VALIDACAO_CAMADAS\`. **Contagem: zero, em todo o lado, excepto em
dois sítios** — a linha do certificado, e isto, escrito à mão dentro de
`c3_10_esforco_its_becrop.py`:

```python
res["becrop"] = {
    "A32A0C": {..., "podridao_radicular": "risco MUITO ALTO detectado"},
    "A32A0B": {..., "podridao_radicular": "No Detectado"},
```

Nenhuma dessas duas cadeias é lida de nenhum ficheiro. São literais de código.
Foram gravadas no `c3_10_esforco_its_becrop.json`, e o certificado cita depois o
JSON. **A regra 3 do protocolo foi satisfeita cosmeticamente: há um ficheiro e
há um cálculo, e o cálculo é o script a escrever o que alguém lhe escreveu.**

Registe-se o que isto é, com o nome que o `CONTROLOS.md` já lhe deu. É o
mecanismo do «B1»: um valor sem origem entra numa saída, a saída passa a ser a
prova do valor, e a partir daí ninguém volta a perguntar de onde veio. A
diferença é que o «B1» demorou semanas a ser apanhado e este está a uma linha de
`grep`.

Todos os outros valores Becrop do mesmo dicionário (856/720, 41/82, «Muy
bajo»/«Alto») **estão** na folha e estão certos; foram transcritos à mão em vez
de lidos, o que é mau mas é outro problema. Só a podridão radicular não tem
origem.

**Como se testa em cinco minutos.** Já está testado: `grep -i podred` sobre a
pasta e sobre os dois despejos. Se o valor existir, existe nos PDF originais da
Becrop, que não foram entregues a esta camada — e nesse caso é um facto trazido
de fora do material, o que o protocolo também proíbe.

**Se cair, o que cai com ele.** A conclusão «os dois Becrop não são comparáveis»
**não cai**: aguenta-se nas 163 dias entre épocas opostas, no n = 1 por data, no
«No hay parcela asociada» e na freguesia declarada — tudo verificável na folha.
Cai a coluna de instrumento independente, e a linha passa a ter **nenhum**, que
é o que tem. E cai a frase sobre «instabilidade do instrumento», que era a única
coisa que aquele número media.

---

### R2 · B3 — «Nenhum organismo está onde o padrão está»

**Retira-se a formulação. O conteúdo é verdadeiro e não é sobre o pomar: é sobre
o painel de ensaios.**

Percorri a `Matriz Fitopatologia` linha a linha contra
`c3_09_organismos_contra_padrao.py`. **A classificação está certa**, e digo-o com
clareza: 20 linhas organismo × matriz, e a repartição 9 sem posição / 5 fora do
conjunto / 4 negativos / 2 em todo o lado reproduz-se exactamente, linha a
linha, sem uma única discordância. As nove sem posição são as quatro de madeira,
*Ceratobasidium*, *F. oxysporum* (raiz), *F. solani*, *N. parvum* (raiz) e
*Globisporangium*; as cinco de fora são *Dactylonectria*, *Fusarium* sp.,
*I. liriodendri*, *R. solani* e os oomicetas de raiz; os quatro negativos são
*Armillaria* nas duas matrizes, *Rosellinia* no solo e os oomicetas de solo; os
dois em todo o lado são o *M. hapla* nas duas matrizes. **A aritmética passa.**

**O problema é a frase, e é grande.**

**Primeiro: a categoria «está onde o padrão está» não existe no código.** As
saídas possíveis de `c3_09` são cinco — `FORA DO CONJUNTO`, `NEGATIVO (nada a
localizar)`, `SEM POSICAO`, `EM TODO O LADO` e `COLOCADO — ver detalhe`. Não há
nenhum ramo que emita «ONDE O PADRÃO ESTÁ». Mesmo um organismo positivo numa só
unidade colocada com 90 % de défice sairia como «COLOCADO — ver detalhe».
Publicar «**Zero** na categoria "está onde o padrão está"» sobre uma categoria
que o classificador não pode produzir é uma afirmação que não podia falhar.

**Segundo, e pior: dezoito das vinte linhas nunca foram ensaiadas em nenhuma
amostra com posição.** A própria folha declara a convenção, no seu rodapé:

> «Célula em branco = esse organismo **não foi testado** nessa amostra (não é o
> mesmo que um resultado negativo).»

Esta frase não aparece no certificado nem em nenhum dos doze scripts. O código
trata as células vazias correctamente (`if v in ("", "NAN"): continue`) e o texto
depois lê o resultado como se fossem procuras falhadas. Os números:

```
das 20 linhas organismo x matriz,
   ensaiadas em pelo menos uma amostra COM posicao :  2   (M. hapla solo e raiz)
   nunca ensaiadas em nenhuma amostra com posicao  : 18
```

**Terceiro, a consequência disso em todo o caso**, que é o número mais forte que
esta camada tinha à mão e não escreveu. Dos **111 registos com posição**:

```
Físico-Química do Solo (boletim A2)      72
Nematologia                              16   <- toda a microbiologia colocada
Painel de Saúde do Solo (regenerativa)   12
Análise Foliar                           11
```

e os 16 de nematologia são **os mesmos quatro relatórios** (340–343/2026) a
medirem **um só organismo**, o *M. hapla*. Do outro lado, os 110 sem posição
contêm **toda** a fitopatologia fúngica do caso: as 20 linhas de ITS, os 15 do
«Kiwi 1000», os 14 da Becrop, os 16 de Espanha.

> **Nunca se procurou um fungo ou um oomiceta em nenhum ponto deste caso que se
> consiga pôr no mapa.** Nem uma vez.

**Como se testa em cinco minutos.** `col[com].Doc_Type.value_counts()` sobre o
CSV que a camada já escreveu. Quatro segundos.

**Formulação que aguenta, e é mais útil do que a retirada:** *o único ensaio
microbiológico com posição em todo o caso é o* M. hapla*, positivo em 5/5
unidades colocadas; nenhum ensaio de fungo ou oomiceta tem posição, e por isso a
pergunta «está onde o padrão está?» não tem, para 18 das 20 linhas, dados que a
possam responder em qualquer sentido.*

**Se cair, o que cai com ele.** B3 tal como está escrito. **E é grave que caia
agora**, porque o `CAMADA_4_PROMPT.md` já leva a frase original, e a C4 é a
camada da exclusão: ler «nenhum organismo está onde o padrão está» com margem
«categórica» num livro-razão de exclusões é transformar um vazio de amostragem
numa exclusão etiológica. É a mesma classe do *P. sojae* atribuído ao corpo em
declínio, que o `CONTROLOS.md` lista como o segundo dos três erros que custaram
semanas.

---

### R3 · B6 — o ρ = −0,044 «a amostragem não foi dirigida pelo padrão»

**Retira-se o teste. Retira-se a conclusão. O contrário é que está medido.**

O certificado apresenta B6 como «**o negativo que interessa**»: Spearman entre o
défice de 2026 da válvula e o número de registos colocados nela, ρ = −0,044,
p = 0,89, n = 12.

Vejamos o segundo vector. `c3_10` constrói-o a partir de `esf`, que agrupa por
`unidade` — e as unidades de bloco (`B3`, `B4`, `Erica Novo`) **não são
válvulas**. O filtro `if n.startswith("v")` retém as doze válvulas e descarta os
sessenta registos colocados ao nível de bloco. O vector que entra no Spearman é,
integralmente:

```
v6 0 | v7 51 | v8 0 | v9 0 | v10 0 | v11 0 | v12 0
v13 0 | v14 0 | v15 0 | v16 0 | v17 0
```

**Um valor não-nulo e onze empates a zero.** Um ρ sobre isto é uma função só do
lugar da v7 na ordenação do défice — nada mais entra. Com onze empates, o
coeficiente não tem graus de liberdade para ter sinal, e o p = 0,89 é o p de não
haver informação nenhuma. **Não é um negativo; é um vector degenerado.**

E a conclusão que dele se tira está ao contrário do que os mesmos dados mostram.
A distribuição real do esforço, por unidade, está no `c3_10_esforco_its_becrop.json`:

```
v7           51 registos   5 relatorios   3 datas   defice26 21,2 %
Erica Novo   28 registos   3 relatorios   2 datas   defice26  2,8 %
B3           16 registos   2 relatorios   2 datas   defice26 46,9 %
B4           16 registos   2 relatorios   2 datas   defice26  6,2 %
todas as outras oito valvulas : 0
```

**Quarenta e seis por cento de todos os registos colocados do caso estão numa
única válvula**, e essa válvula é a vizinha imediata do foco OESTE, dentro do
mesmo bloco B2. Chamar a isto «não há selecção» é o inverso da leitura. Há
selecção total; simplesmente não é a selecção pelo mapa de NDVI que o prompt
mandava procurar — é selecção por conveniência operacional, o que é uma
armadilha diferente e igualmente séria, porque também produz coincidência entre
biologia e lugar sem nenhuma causa comum.

**Como se testa em cinco minutos.** Contar os não-zeros do vector.

**O que sobrevive, e deve substituir B6:** *o esforço não está distribuído pelo
défice, está concentrado: 46 % dos registos colocados numa unidade de 3,25 ha,
oito das doze válvulas com zero, e nenhuma correlação estimável entre esforço e
padrão com estes dados.* Isso é honesto e continua a servir a C4.

**Se cair, o que cai com ele.** A frase «a coincidência entre biologia e padrão
não pode ser artefacto de selecção». Não cai a segunda metade — «também não há
cobertura onde o padrão está» — que é verdadeira e está medida noutro sítio.

---

### R4 · B5 — «a amostra colocada mais próxima está na v7, a **120 m**»

**Retira-se o número e retira-se a palavra «amostra». A ausência documental
mantém-se.**

Três problemas, em ordem de gravidade.

**1. Os 120 m não são a distância de uma amostra a nada.** São
`d_foco_OESTE_m` da entrada `v7` do `c3_07_georreferenciacao.json`, isto é, a
distância do **centróide da partição de Voronoi da v7** ao centro do foco. A
amostra não tem coordenada — é um rótulo de talhão sobre uma unidade de
3,25 ha. A própria camada escreve isto na sua nota 2 e depois publica «está a
120 m» na lista fechada.

**2. Parte da unidade que tem as amostras está dentro do foco.** O mesmo JSON
dá, para a v7, `pct_disco_OESTE = 11,7 %`. Sobre 325 células são **38 células =
0,38 ha da v7 dentro do disco de 90 m do foco OESTE**. E a repartição completa
do disco pelas três válvulas fecha exactamente:

```
disco FOCO OESTE, 248 celulas :  v8 166 (67 %) | v9 44 (18 %) | v7 38 (15 %)
```

Quinze por cento do foco OESTE está na válvula amostrada. A distância mínima da
unidade com amostras ao foco não é 120 m: é **zero**. «120 m» e «zero» são as
duas leituras honestas do mesmo objecto, e o certificado publica só a que faz o
buraco parecer maior.

**3. A C1 publicou 111 m para o mesmo objecto e a C3 não reconcilia.** O
`c1_06_solo_colocado.csv` coloca o boletim `B2 - V7` no ponto da própria válvula
(530397,5 · 4654985,2) com `dist_foco_oeste_m = 111,0` e — repare-se —
`raio_incerteza_m = 0,0`. A S10 do certificado da C1, que a C3 recebeu como
dado, escreve **«a 111 m do foco»**. A C3 escreve 120 m, com margem ±10 m, e não
diz que mudou de objecto. É a mesma falha que o adversário da C2 assinalou em
W6 para a v8 (34 / 35 / 43 m), agora com uma quarta e uma quinta entrada.

**O que sobrevive de B5, e é bastante.** *Nenhum registo dos 221 nomeia a válvula
8. Os rótulos existentes do B2 são `B2 - V7`, `B2 - Zona 1 (V7)`, `B2 - Zona 1`,
`B2.V7` e `V7` — cinquenta e um registos, todos na v7.* Isso é verdadeiro,
verificável e é o achado. Não precisa dos 120 m e não pode carregar a palavra
«amostra».

**Se cair, o que cai com ele.** O número. E a força retórica do fecho do
certificado, «a válvula 8 nunca foi amostrada», que passa a ser «nenhum
documento nomeia a válvula 8» — e que já estava, por §0.2, dependente da
paragem de linha.

---

### R5 · B10 e a linha CONFIRMADO da referência — duas classes de número misturadas

**Não se retira o achado. Retira-se a lista de quatro números como se fossem a
mesma coisa, e retira-se a margem declarada.**

Este é o achado com maior alcance da camada e merece ser separado com cuidado,
porque tem uma metade sólida e uma metade que não é o que parece.

**A metade sólida — e é mais sólida do que o certificado diz.** As 18 células da
referência dentro dos dois discos (12 OESTE + 6 ESTE, 16,4 % das 110) são
contaminação **geométrica**: a pertença ao disco não depende do sinal, e retirar
as células não é circular. E o `c3_08_controlo_referencia.json` guarda o
controlo que decide a questão, que o certificado **não publica**: a diferença
entre a mediana suja e a limpa, ano a ano.

```
2017 +0,0001 | 2018 +0,0004 | 2020 -0,0006 | 2021 -0,0001 | 2022 +0,0002
2023 +0,0005 | 2024 +0,0010 | 2025 +0,0023 | 2026 +0,0133
```

**Sete anos de placebo a zero à quarta casa, e depois um salto de treze vezes em
2026.** Isso é o argumento de B10, é muito melhor do que a diferença de dois
números que o certificado publica, e está no ficheiro. Publicá-lo passa B10 de
«dois medianos diferem» para «a diferença é específica do ano do
acontecimento» — que é uma afirmação de outra ordem.

**A metade que não é o que parece.** Os outros dois números da lista — «23
células do défice de 2026 e 19 do declínio novo M2» — **não são da mesma classe
e não medem contaminação**. O défice define-se, por V1, como
`nd < mediana_da_referência − 0,05`. Contar quantas células **da própria
referência** caem abaixo da mediana **da própria referência** menos 0,05 é medir
a dispersão interna da referência, não a intrusão do acontecimento. Uma
referência com qualquer espalhamento terá sempre uma cauda inferior abaixo desse
limiar, em todos os anos, com ou sem evento.

E o mesmo vale para as 19 do M2, com um agravante mecânico: M2 exige «nunca
esteve em défice em 2017-2024». As células da referência satisfazem essa
condição com mais frequência do que o pomar, precisamente por serem referência.
O resultado é visível no próprio JSON e ninguém o comenta: **a referência tem
17,3 % de declínio novo M2 contra 11,8 % do pomar inteiro** — mais do que a
média do terreno que o M2 devia estar a destacar. Isso não é a referência
contaminada pelo evento; é o M2 a preferir estruturalmente terreno com história
limpa.

**Não há linha de base para nenhum dos dois números.** `REF ∩ défice(a)` nunca
foi calculado para 2017, 2020, 2021, 2022, 2023, 2024 nem 2025 — só para 2026.
Sem essa coluna, «23 de 110» não é interpretável em nenhum sentido. É três
linhas de código sobre ficheiros que já estão em disco (teste **T1** da parte 4).

**A margem «±0,001 NDVI na mediana» não vem de lado nenhum.** Não há bootstrap,
não há intervalo, não há repetição. A grandeza é a diferença entre a mediana de
110 células e a mediana de 92 numa **única cena**, e essa cena é a **S2C** que a
V10 da C2 identificou como o maior confundente da série. Retirar 18 de 110
desloca a posição da mediana de sete postos; parte do +0,0133 é re-ordenação,
não sinal, e nada nesta camada separa as duas coisas.

**E o «56 %» arrasta um problema de âncora.** B10 escreve «o défice de 2026 sobe
de **9,47 para 10,32 ha**» sem dizer que esses são os valores **sem abertura
morfológica**, enquanto a tabela de âncoras da mesma página dá o défice de 2026
como **7,86 ha**. Três números para a mesma quantidade na mesma página, e a
qualificação («limiar 0,05, sem abertura») só aparece na secção CORRIGIDO, não
em B10. Quem ler a lista fechada — que é a única coisa que a C4 pode usar — vê
7,86 e 9,47 lado a lado sem explicação.

**Formulação que aguenta:** *16,4 % das células da referência sistemática (18 de
110) caem dentro dos discos de 90 m dos dois focos. A consequência é específica
de 2026: retirá-las desloca a mediana da referência em +0,0133 nessa cena e em
menos de 0,0025 em todas as oito anteriores. A queda 2024→2026 passa de −0,0218
para −0,0096. As contagens de «défice» e «M2» dentro da referência não entram
neste argumento até existir a série por ano.*

**Se cair, o que cai com ele.** A parte geométrica não cai e obriga a recalcular
tudo o que usou fosso à referência, como o certificado diz — com o sentido
conservador que ele correctamente identifica. Cai a lista de quatro números como
prova única, cai a margem, e cai a leitura de que a referência «não está limpa»
num sentido mais geral do que o geométrico.

---

### R6 · B1 e B4 — dois números de apoio que não medem o que dizem

**Retiram-se os dois números; os dois factos aguentam-se sem eles.**

**B1, «`Sample_Date` coincide em 212/212 — coluna que não entra na chave de
alinhamento e que portanto o testa».** A chave do `difflib` é
`Source_File || Organism_Parameter`. E `Sample_Date` é **função estrita de
`Source_File`**: nos 221 registos há 27 ficheiros de origem e cada um tem
exactamente uma data de amostragem, sem excepção. Como os pares emparelhados têm
`Source_File` idêntico por construção, a coincidência de `Sample_Date` é
**consequência da chave**, não um teste dela. O n efectivo não é 212: são 27
comparações, das quais 4 são «Not stated» e 1 é vazia — **22 datas reais**. O
teste não é nulo, mas está inflacionado por um factor de nove e está etiquetado
como instrumento independente, que não é.

*(O teste que teria sido independente estava a dois passos: `Result` diverge em
**159 de 212** pares, e é tradução — o que se lê no ficheiro. Um par a par sobre
`Value` nas 203 linhas comparáveis, ou sobre `Report_No`, teria dado
informação.)*

**B4, «Kiwi 1000 aparece como `Client_Titular` em 146 registos».** O
`c3_04_perfil.json` reparte assim: `Kiwi 1000, Lda` = **131**; `Kiwi 1000
(sample identifier)` = **15**. Os 15 são **os próprios registos da amostra a
granel**, onde o compilador pôs o identificador da amostra no campo do cliente
por não haver cliente indicado. Usá-los para provar que «Kiwi 1000 é um cliente
e não um lugar» é usar a amostra em causa como prova sobre si própria. O número
citável é **131 de 221** — que continua a ser maioria e continua a sustentar o
argumento. E o comentário do próprio `c3_09_organismos_contra_padrao.py` já diz
131. **Dois scripts da mesma camada dão dois números para a mesma contagem, e o
certificado publica o maior.**

---

### R7 · «A válvula 27 não existe em nenhum dos dois livros»

**Retira-se «nos dois livros». A afirmação sobrevive mais estreita.**

O certificado escreve: «Busca exaustiva pelo número 27 isolado **nos dois
livros**.» O código, em `c3_10` §8:

```python
busca27 = pt.apply(lambda r: r.astype(str).str.contains(r"(?<![0-9])27(?![0-9])", ...
```

`pt` é **uma** folha de **um** livro: o `Registo Principal` do dossiê PT. O
`Master Log` EN nunca é aberto neste script, e nenhuma das **sete folhas
auxiliares** — incluindo `Relatorios Becrop`, que é onde um código de parcela ou
de sector teria a maior probabilidade de aparecer — é varrida. E o que a saída
guarda não são as ocorrências mas os **nomes das colunas** onde houve alguma:
`["Record_ID", "Result_Date"]`.

Afirmações de ausência são as mais fáceis de fazer mal, e a camada tem razão em
dizer que «um número que ninguém consegue localizar é exactamente como o "B1"
entrou». Precisamente por isso, a busca tem de cobrir o que diz cobrir.

**Formulação que aguenta:** *o número 27 isolado não ocorre no `Registo
Principal` do livro PT senão como `Record_ID` e como parte da data 2023-06-27.
As folhas auxiliares e o livro EN não foram varridos.* E a entrada de NÃO
TESTÁVEL mantém-se e continua certa.

---

### R8 · B11 — a repartição das datas está errada em duas das quatro células

**Retira-se a repartição. O facto aguenta inteiro.**

B11 escreve: «As doze amostras físicas colocadas são de **2026-03-03 (4)**,
2026-05-06 (4), 2026-06-17 (2) e **2026-07-08 (2)**.» O
`c3_07_registos_colocados.csv`, agrupado como o próprio certificado manda:

```
2026-03-03   B2_V7__Marc_o_26 · B2_V7__Marc_o_26_Regenerativa · B3_7ha_Marc_o_26
             Erica_2016_E__Marc_o_26 · Erica_2016_R__Marc_o_26          = 5
2026-05-06   340_Kiwi · 341_Kiwi · 342_Kiwi · 343_Kiwi                  = 4
2026-06-17   B2_V7__Junho_26 · B2_V7__Folha__Junho_26                   = 2
2026-07-08   B4_Julho                                                   = 1
```

**5, 4, 2, 1.** O total de 12 está certo por compensação; duas das quatro
parcelas estão erradas. *(Os três boletins `B1_C*_Julho` da mesma data caem em
`FORA DA BANDA` e por isso não contam — é provavelmente daí que veio o «2».)*

E uma nota de margem sobre a palavra «amostras»: os 12 são **12 relatórios**,
não 12 colheitas. Colapsados por (data × unidade) são **10 acontecimentos de
amostragem** — em Março, o B2-V7 dá dois relatórios da mesma colheita (boletim +
painel regenerativo); em Junho, dá dois (solo + folha). A própria nota 3 do
certificado avisa que quem inferir densidade de amostragem a partir de 111 erra
por um factor de nove; quem a inferir a partir de 12 erra por 1,2.

**O núcleo de B11 não é tocado por nada disto, e é excelente.** Nenhuma amostra
com posição é anterior a Março de 2026; o degrau é de 2025-2026; as três únicas
amostras anteriores a 2026 do caso inteiro (o «Kiwi 1000» de 2025-06-06 e os dois
Becrop) são exactamente as que não têm posição. **Não há linha de base
biológica.** É o facto mais consequente que esta camada passa para cima e não
depende da paragem de linha.

---

## 2 · Factos a manter, com margem maior

### W1 · B9, a *Rosellinia* — **o melhor facto da cadeia até aqui**. Sem alteração de margem.

Verifiquei nos dois livros, registos 1–4 e 17. Campo: 2026-08-04, raiz, uma
planta arrancada, «local não especificado», identificação macroscópica, amostra
colhida e **não enviada** («não será necessário»). Molecular: informe 331/2025,
amostragem 2025-06-06, **solo**, composto «Kiwi 1000», resultado 2025-07-07.
Catorze meses **antes**, não depois. A `Location_Confidence` do registo 2 e a
nota do próprio livro dizem as duas «posteriores», e as duas estão erradas pelas
datas que o mesmo livro guarda três colunas ao lado.

Isto é o que uma camada deve fazer: uma contradição interna do material,
apanhada por leitura de campos, sem inferência por cima e sem teorizar acima da
camada. A palavra «contradito» sai, e sai bem.

**Uma correcção de higiene, não de conteúdo.** O instrumento independente
declarado é «as datas estão em campos separados dos dois livros e coincidem nos
dois». Mas **B1 estabelece que os dois livros são o mesmo livro**. Não pode ser
o mesmo certificado a provar que EN e PT são um só objecto e depois a usar a sua
concordância como segundo instrumento. O instrumento independente real é
outro e é melhor: **o número de informe do laboratório (331/2025) e o número de
expediente (2025045292) são atribuídos pelo laboratório na recepção e são
independentes do conteúdo do resultado** — que é, aliás, exactamente o argumento
que a própria camada usa em B11. Basta trocar a coluna.

### W2 · A linha do *M. hapla* — o melhor uso do controlo 1 nesta camada

«Positivo tanto na unidade com 2,8 % de défice (Erica Novo) como na de 46,9 %
(B3); é o satélite que estabelece que não discrimina.» Isto é um instrumento
genuinamente independente a fazer trabalho genuíno: o laboratório dá a presença,
o Sentinel-2 dá o contraste entre as unidades, e nenhum dos dois produziu o
outro. Nada a alargar.

**Uma margem a acrescentar, e é a que o certificado já quase escreve.** Seis
amostras, um laboratório, uma data (2026-05-06), um método. E a contagem mais
baixa dos cinco blocos está no bloco **mais** afectado (B3: 28/37 com 46,9 % de
défice). A leitura defensável é «não discrimina»; a leitura que não se pode
tirar é «está presente de forma uniforme», porque seis pontos numa data não
medem distribuição.

### W3 · B8, as ITS — sobrevive, e é **mais forte** do que o certificado diz

Confirmo tudo: profundidade filtrada de 4 964 a 25 078 (5,1x), qualificadas de
2,8 % a 29,2 % (10x), riqueza de ASV com a ordenação idêntica à da profundidade.
E acrescento três coisas que estão nos ficheiros e não no texto.

**Primeira: não é só a riqueza.** As ordenações das quatro amostras são

```
profundidade filtrada  25078  7119  4964  10688   ->  4 2 1 3
riqueza de ASV           281   171   129    219   ->  4 2 1 3
indice de Simpson     0,9797 0,9767 0,9614 0,9771 ->  4 2 1 3
indice de Shannon       6,82  6,25  5,61   6,59   ->  4 2 1 3
equitabilidade Pielou  0,838 0,8431 0,7996 0,8472 ->  2 3 1 4
```

**Simpson e Shannon seguem a profundidade com ρ = +1,000, exactamente como a
riqueza.** Só o Pielou se descola, e mal (ρ = +0,400, p = 0,60). O certificado
apresenta Pielou **e Simpson** como «os índices robustos à profundidade», e
Simpson não é robusto nestes dados: é o mesmo ordenamento.

**Segunda: o ρ do Simpson foi calculado, foi impresso, e não foi gravado.** O
`c3_10` corre `r_sim = stats.spearmanr(filtradas, simpson)` e imprime-o; o
dicionário `res["its"]` guarda `spearman_profundidade_x_asv` e
`_x_pielou` e **não guarda o do Simpson**. O único dos três números que
contraria a frase publicada é o único que não sobreviveu à escrita do JSON.

**Terceira: o p que está no JSON é impossível.** `spearman_profundidade_x_asv:
[1.0, 0.0]`. Com n = 4, um ρ de +1 tem probabilidade exacta 2/4! = **0,083** sob
a hipótese nula — uma em doze. O `0.0` é o `scipy` a dividir por
`sqrt(1 − ρ²) = 0` na aproximação t. O certificado publica ρ = +1,000 com margem
«ρ exacto» e sem p nenhum, o que é a escolha certa por sorte e não por método.

**Isto tudo reforça B8**, e por isso fica na parte 2 e não na parte 1: a
conclusão é **negativa** — a diversidade não entra em nenhuma conclusão — e
quatro métricas alinhadas com a profundidade em vez de uma tornam-na mais
segura, não menos. Só a frase sobre o Simpson tem de sair.

### W4 · B7 — aguenta, e a sua margem depende de um facto que foi retirado hoje

B7 verifica-se: B3 = 992 células = 9,92 ha, `nu2021` = 16,3 %, v13 = 22,6 %,
v14 = 13,8 %. A conclusão — a contagem 28/37 não pode ser atribuída a plantas do
foco ESTE — é correcta e é o segundo melhor facto da camada.

**A margem tem de mudar de justificação.** O certificado escreve que «a fracção
de chão é a de 2021, que a adenda de LiDAR mostra ser um sub-cálculo do que
havia em 06-07-2025». Isso apoia-se na **etiqueta** «sem pérgola / chão» da
adenda, e o `ADVERSARIO_2026-08-29.md` **retirou essa etiqueta** (R3): o limiar
operativo é 0,5 m e não os 1,5 m que a adenda justifica, e 0,5 m cai a **0,03 m
da mediana do foco ESTE** — corta a unidade pelo seu próprio centro. O mesmo
adversário regista que o IFAP declara **KIWI em 65 % do terreno que a adenda
chama «chão»**.

O que sobrevive é a **medição de altura**, que ninguém retirou: 0,47 m de
mediana no disco ESTE, 50,2 % das células abaixo de 0,5 m, contra 2,34 m e 99,2 %
na referência. B7 deve encostar a isso e à `nu2021` de 2021, e deixar cair a
palavra «pérgola».

### W5 · A `Erica Novo` como «par de contraste limpo» — 86 % dos seus registos são inferidos

A linha CONFIRMADO diz «5,35 ha, 2,8 % em défice, 0,7 % em declínio novo M2, 0 %
de chão lavrado», com margem «±10 m sobre a G35». Os números batem. **A margem
não.** Dos 28 registos colocados na Erica Novo:

```
INFERIDO         24   (Erica 2016 R e Erica 2016 E — a identificacao nao esta provada)
COLOCADO-BLOCO    4   (343_Kiwi, rotulo «Erica Novo E»)
```

Vinte e quatro em vinte e oito — **86 %** — assentam na identificação «Erica 2016
= Erica Novo», que a própria camada classifica como inferência e não prova, e
que o `c1_06_solo_colocado.csv` marca com `confianca = INFERIDA` e
`raio_incerteza_m = 43`. A secção CORRIGIDO diz isto bem («se a inferência
estiver errada, 21,6 % dos registos colocados mudam de sítio»), mas a linha
CONFIRMADO e o par de contraste não levam a ressalva, e é a linha CONFIRMADO que
sobe.

### W6 · O contraste de CaO — a correcção está certa e a razão publicada é a mais fraca das duas

1,7x confirma-se (879/505 = 1,74) e fica de facto abaixo do factor de 2 da C1
S9. Mas há uma segunda razão, independente e mais forte, que a camada tinha à
mão: **os dois boletins do lado Erica Novo são precisamente os dois INFERIDOS**.
Um contraste químico entre uma unidade confirmada e duas cuja atribuição de
bloco é inferência não passa, mesmo que o factor fosse 10.

**E um número órfão.** O certificado escreve «comparar pelas médias (**382**
contra 1040)». A média de [264, 505] é **384,5**; 1040 está certo
((879+1200)/2 = 1039,5). O 382 não existe em nenhum JSON, em nenhum CSV, nem no
`c1_06_solo_colocado.csv` — é um literal dentro de um `print` do
`c3_11_par_contraste_e_ancoras.py`.

**E uma coisa que cai a mais do que devia.** A S10 da C1 — «a carência de cálcio
no bloco do foco OESTE está confirmada por **duas matrizes**», solo (264, 505) e
**folha** (Ca 2,2 % contra referência 3–4,7 %) — é uma afirmação **diferente** da
que a C3 corrige. A C3 retira o *contraste entre blocos*; a S10 afirma um
*défice contra um intervalo de referência analítico*, e o seu instrumento
independente (a folha, outra matriz, outro método, outra data) não é tocado.
Como está escrito, um leitor da C4 arruma a S10 inteira com a correcção. Tem de
ficar dito que a S10 sobrevive.

### W7 · Herança: **nada da C3 cai com L4 ou L6**, e há uma exposição de vocabulário

Verifiquei directamente, por busca no certificado e nos doze scripts, os números
que o `ADVERSARIO_2026-08-29.md` retirou: `+0,0585`, `2,29 : 1`, `p = 0,368`,
`0,00 ha em 2022/2023/2024`, `1,32`, `4,03`, e as saídas
`refazer_c2_este` / `serie_separada`. **Zero ocorrências em todo o `SAIDA_C3\` e
em todo o `CAMADA_3_CERTIFICADO.md`.**

A C3 usa da adenda apenas L2/L3 (a partição de altura e «metade do disco ESTE
abaixo de meio metro») e **corrige** L5. Nenhum dos dois foi retirado — a L5 foi
mantida pelo mesmo adversário em W4 («correcta, conservadora, e incompleta»).
**Conclusão: a C3 não herdou nada de L4 nem de L6, e nada seu cai com eles.** É a
resposta directa à pergunta do prompt desta sessão.

Fica **uma** exposição, de palavra e não de número: a C3 escreve, na correcção
de âmbito e no docstring do `c3_07`, «não tinha **pérgola**» quando a etiqueta
«pérgola / chão» é o que a R3 do adversário retirou. A altura medida sobrevive;
a etiqueta não. Ver W4.

### W8 · O âmbito atribuído à adenda que a adenda não contém

O certificado abre com «**Correcção de âmbito recebida com a adenda, e
cumprida:** a biologia concentra-se no v8/B2 (…) e no seu par de contraste
**v10-v11, "Erica Novo"**», e o docstring do `c3_11` diz que «a adenda de LiDAR
manda concentrar a biologia no v8/B2 e no seu par de contraste v10-v11, que
estão no mesmo bloco geográfico, na mesma origem de água, e MELHORARAM».

Procurei na `CAMADA_2_ADENDA_LIDAR.md`, nas duas versões. **A adenda não contém
«v10», «v11», «Erica Novo», «par de contraste», nem nada sobre origem de água.**
A única nomenclatura que ela fixa é «onde esta adenda escreve foco OESTE,
leia-se v8/B2» — e essa frase só foi acrescentada hoje às 13h03, quarenta minutos
**depois** de o certificado da C3 estar escrito.

Não digo que a instrução seja errada — o par v8/B2 contra v10-v11 é um bom par.
Digo que ela **veio de fora dos materiais**, que a regra 3 do protocolo diz que
«está no dossiê» não é prova, e que ela conduz a linha CONFIRMADO da Erica Novo
e o `c3_11` inteiro. É prosa a fazer de herança.

### W9 · B2 — os números estão certos e a etiqueta de instrumento independente não

«111 com posição e 110 sem», e a repartição 53 / 40 / 16 / 1: reproduz-se toda
no CSV. O que não se sustenta é a coluna: «*Instrumento independente:* a
colocação usa `valvulas_por_area.json` (tabela documental do gestor), não o
sinal.» A tabela do gestor não **confirma** a colocação — a tabela do gestor
**é** a colocação. Não usar o sinal é uma virtude de desenho; não é um segundo
instrumento. B2 não tem instrumento independente, e o sítio certo para o dizer é
a própria coluna, como B8 faz honestamente.

---

## 3 · A pergunta que falta

*(transversal B)*

**A camada perguntou onde estão os positivos. Nunca perguntou o que foi alguma
vez procurado.**

Vale a pena ver a forma disto, porque é outra vez a forma do erro que abriu a
cadeia. O «B1» não foi um cálculo errado: foi uma pergunta de **identidade do
objecto** — *o que é este sítio?* — que ninguém fez à camada de baixo daquela
onde a inferência corria. A `Pathology Matrix` tem exactamente o mesmo problema
de identidade, e o próprio livro avisa, no rodapé da folha:

> «Célula em branco = esse organismo **não foi testado** nessa amostra (não é o
> mesmo que um resultado negativo).»

Uma matriz de presença e uma matriz de **cobertura de ensaio** parecem-se em
Excel e não são a mesma coisa. Toda a B3 assenta em ler a primeira onde está a
segunda.

Os números que fecham a pergunta estão no CSV que a camada escreveu:

- Das **20** linhas organismo × matriz, **2** foram alguma vez ensaiadas numa
  amostra com posição — o *M. hapla* no solo e na raiz. As outras **18** nunca.
- Dos **111** registos com posição, **16** são microbiologia, e são os mesmos
  quatro relatórios de nematologia a medirem o mesmo organismo. Os outros 95 são
  química de solo (72), painel regenerativo (12) e análise foliar (11).
- **Toda** a fitopatologia fúngica do caso — as 15 linhas do «Kiwi 1000», as 20
  das ITS, as 14 da Becrop, as 16 de Espanha — está do lado sem posição.

> **Não existe, em todo o caso, um único ensaio de fungo ou de oomiceta feito
> num ponto que se consiga pôr no mapa.**

Isto não é uma nota metodológica. É a diferença entre duas frases que a C4 vai
ler de maneiras opostas:

- «Nenhum organismo está onde o padrão está» → *procurámos e não encontrámos*.
  Lida assim, é uma exclusão, e entra num livro-razão de exclusões como tal.
- «Nenhum ensaio capaz de encontrar um fungo foi alguma vez feito onde o padrão
  está» → *não procurámos*. Lida assim, não exclui nada e é uma instrução de
  amostragem para a C5.

A camada escreve a primeira em B3, com margem «categórica», e escreve algo
próximo da segunda no último parágrafo — que não é uma das cinco secções do
protocolo e portanto não passa para cima. **A frase certificada é a errada e a
frase certa não é certificada.**

**E há uma segunda pergunta que falta, mais pequena e mais barata**, já
identificada em §0.2: *quem afirmou a linha «amostras» da G34, e com que base?*
A camada tratou-a como uma questão de documentos quando pode ser uma questão de
memória de uma pessoa. Se for testemunho, a regra deste projecto é explícita:
não se corrige com réplica, corrige-se perguntando outra vez.

**Porque é grave agora e não daqui a duas camadas.** O `CAMADA_4_PROMPT.md` já
está escrito, já foi entregue, e leva B3 e B5 verbatim. A C4 é a camada da
exclusão de causas. Uma exclusão fundada num vazio de amostragem é o *P. sojae*
outra vez, e o `CONTROLOS.md` lista esse como o segundo dos três erros que
custaram semanas a este processo. **A correcção de B3 tem de correr antes de a
C4 arrancar, não depois.**

---

## 4 · Os cinco testes de cinco minutos, por valor

Ordenados por confiança ganha por esforço. Três correm sobre ficheiros que já
estão em disco; dois são perguntas a pessoas, e são os que valem mais.

**T1 · A referência ano a ano.** *(três linhas; nada de novo em disco)*
`REF & mapa_defice(a)` e `REF & novo_M2` para as nove cenas, não só para 2026, e
a repetir a limiares 0,04 / 0,05 / 0,06. Decide se «23 de 110» é contaminação ou
se é a cauda inferior que uma referência com este espalhamento tem em qualquer
ano. **Enquanto este número não existir, dois dos quatro números de B10 não são
interpretáveis em nenhum sentido**, e são precisamente os dois que o certificado
apresenta como mais alarmantes. Segundo ponto do mesmo teste, e é o que
transforma B10 de bom em muito bom: **publicar a coluna `dif` por ano**, que já
está gravada — sete anos abaixo de 0,0025 e depois +0,0133.

**T2 · Publicar sete números que a camada já calculou.** *(zero computação)*
(a) a coluna `dif` de `c3_08`, acima; (b) ρ(profundidade, Simpson) = +1,000 e
ρ(profundidade, Shannon), calculados e não gravados; (c) o p exacto do ρ = +1
com n = 4 (0,083), em vez do `0.0` que está no JSON; (d) 131 em vez de 146;
(e) a repartição real de datas de B11 (5/4/2/1); (f) a repartição do disco
OESTE pelas três válvulas (166/44/38) e os 11,7 % da v7 dentro dele; (g)
`Doc_Type.value_counts()` sobre os 111 colocados. **Custo nulo, e corrige B3,
B4, B5, B8 e B11 antes de a C4 os usar como dados.**

**T3 · Três perguntas de uma linha, a duas pessoas.** *(um telefonema)*
1. Ao autor da G34: **de onde veio a atribuição das ISFBV0314–17 e do «Kiwi
   1000» ao foco OESTE?** Fecha ou consolida a paragem de linha, e é o único
   teste que a pode resolver.
2. À Areeiro, ou ao técnico que submeteu: **de que talhão foi colhida a amostra
   de madeira/raiz/solo de Junho de 2025 (informe 331/2025)?** São **nove das
   vinte** linhas organismo × matriz e é toda a patologia de madeira do caso.
3. À Fauna Útil SL: **o formulário de submissão que atribui os códigos ISFBV a
   talhão e data.**

Estas três estão todas na secção NÃO TESTÁVEL da própria camada, e valem mais
do que qualquer recomputação possível — pela mesma razão que o
`CONTROLOS.md` regista: os três erros que custaram semanas a este processo foram
todos apanhados por **ir a um instrumento diferente**, e nenhum por recalcular.

**T4 · Reconciliar 0,054 contra 0,0218.** *(cinco linhas)*
A C3 «corrige» a L5 dizendo que a referência desce **−0,0218** de 2024 para
2026, contra os **0,054** que a sessão de gestão mediu e que a adenda publica.
Um factor de 2,5 na mesma quantidade, sobre as mesmas células, entre duas
sessões — e a C3 declara-o corrigido sem investigar porquê. **Divergência sem
explicação é achado, não correcção** (controlo 2). A hipótese óbvia é média
contra mediana: se a média cair 0,054 e a mediana 0,022, a diferença **é** a
cauda inferior — o que seria prova directa e independente de B10, e a camada
tê-la-ia deitado fora ao chamar-lhe erro alheio. Calcular a média das mesmas 110
células nas mesmas duas datas resolve isto.

**T5 · A distância mínima, e a busca do 27 refeita.** *(duas linhas cada)*
(a) `min dist(célula da v7, foco OESTE)` sobre a partição, em vez da distância
do centróide: dá o número que falta a B5 e que hoje é «zero» por inspecção do
`pct_disco_OESTE`. Ao mesmo tempo, alinhar 34 / 35 / 43 / 46 m para a v8 e
111 / 120 m para a v7, e declarar qual é o objecto de cada um.
(b) repetir a busca do «27» sobre **os dois livros e as dezasseis folhas**, e
não sobre uma folha de um livro — e, de passagem, procurar «Zona 0» e «Zona 1»
como vocabulário do gestor, porque existem dois rótulos `B2 - Zona 1` no
registo e ninguém verificou se «Zona 0» aparece em algum lado.

---

## 5 · Transversais A, C, D — e veredicto

### A · A regra do instrumento independente

De onze factos e sete linhas de CONFIRMADO:

**Têm instrumento independente a sério — quatro.**
**B7** (ortofoto/estrutura × tabela do gestor × laboratório — três proveniências,
o melhor cumprimento do controlo 1 em toda a cadeia até aqui), **B10** (máscara
de estrutura × série de reflectância), **B11** (números de informe do
laboratório, atribuídos na recepção e independentes do conteúdo), e a linha do
***M. hapla*** (o satélite estabelece o contraste que o laboratório não vê).

**Declara honestamente que não tem — um.** **B8**, e explica porquê passa mesmo
assim (a conclusão é negativa: retira um dado, não o afirma). É a etiqueta mais
bem posta do certificado.

**Tem um instrumento que é o mesmo com outro nome — cinco.**
**B1** (`Sample_Date` é função de `Source_File`, que está na chave — R6);
**B3** (a coluna diz «cruza documentos de laboratório com `c2_05_*.npy`,
óptico»; o óptico não entra em nenhum dos cinco ramos do classificador, só
imprime percentagens ao lado — R2); **B2** e **B5** (a tabela do gestor produz a
colocação, não a confirma — W9); **B9** (usa «coincidem nos dois livros» depois
de B1 ter provado que os dois livros são um só — W1).

**Tem um instrumento que não existe — um.** A linha Becrop (R1).

**Tem um instrumento cuja estatística é vazia — um.** **B6** (as duas séries têm
proveniências distintas, e uma delas tem onze empates a zero — R3).

Cumprimento pior do que o da C2, e por um motivo estrutural que vale a pena
nomear: **nesta camada quase toda a prova é documental, e um documento não se
confirma consigo próprio.** Os únicos instrumentos genuinamente independentes
disponíveis — o satélite, a ortofoto, o LiDAR, e as pessoas — só entram em
quatro dos onze factos.

### C · Entrou alguma coisa pela porta do lado?

**Quatro itens, e um deles saiu em vez de entrar.**

1. **A «podredumbre radicular» (R1).** Não entrou por porta nenhuma: foi escrita
   à mão dentro do script, gravada no JSON, e citada a partir do JSON.
2. **A correcção de âmbito atribuída à adenda de LiDAR (W8).** A adenda não a
   contém, em nenhuma das suas duas versões. Conduz a linha CONFIRMADO da Erica
   Novo e o `c3_11` inteiro.
3. **O «382» do CaO (W6).** Prosa onde devia haver cálculo — o valor é 384,5.
4. **E uma coisa saiu.** O `CAMADA_4_PROMPT.md` foi escrito e entregue, com
   B1–B11 verbatim, **depois** de a camada declarar uma paragem de linha. A
   regra 2 diz «pára, escreve o que rejeitaste, e devolve». A camada rejeitou,
   construiu quatro factos por cima (§0.2) e passou o bastão.

### D · As quantidades-âncora

A tabela da C3 reporta oito das dez âncoras do `CONTROLOS.md` e acrescenta três
suas, o que é boa disciplina. **Quatro divergências não estão declaradas, e uma
delas é séria.**

1. **A série tem nove cenas, não dez.** `c2_00_comum.DATAS` contém nove datas;
   2019-09-02 está em `TODAS` e não em `DATAS`. Mas a **V1 da C2**, que a C3
   recebeu como dado, diz «A série de plena estação tem **dez** cenas (as nove
   anteriores mais 2019-09-02)». **Todo o `c3_08` — isto é, todo o B10 — corre
   sobre nove.** O código da camada de baixo contradiz o certificado da camada
   de baixo, o adversário da C2 já tinha assinalado essa cena como o item que
   voltava à C0 (condição 1 do seu veredicto), e a C3 herdou a versão sem ela
   sem reparar. As âncoras «cenas na série: 11» e «cenas de plena estação: 9»
   do `CONTROLOS.md` não aparecem na tabela da C3.
2. **O NDVI da referência.** As duas âncoras do `CONTROLOS.md` (0,838 em
   2017-07-02 e 0,886 em 2026-07-27) não são reportadas, e a C3 **tem-nas
   medidas** no seu próprio JSON: **0,8898** e **0,8766**. O sinal da variação
   inverte-se — o declarado sobe, o obtido desce. A R2 G6 já tinha estabelecido
   essa inversão, mas o controlo 2 manda reportar o valor obtido e assinalar a
   diferença, e não foi feito.
3. **Défice de 2026: três números, um reportado.** 7,86 ha (com abertura, na
   tabela de âncoras), 9,47 ha (sem abertura, em B10), 10,32 ha (sem abertura,
   referência limpa, em B10). B10 não leva a qualificação. Nota lateral: a
   diferença entre com e sem abertura é de **0,04 ha em 2017 e 1,61 ha em 2026**
   — o défice de 2026 perde 17 % da área à abertura 2×2 e o de 2017 perde 0,5 %.
   Isso é uma medição directa e independente da dispersão que a C2 afirmou em
   W3, está no `c3_08_controlo_referencia.json`, e ninguém a leu.
4. **A distância da v7 e da v8 ao foco OESTE.** 34 (G35, ponto da válvula), 35
   (C1), 43 (C2, centróide de Voronoi), **46** (C3, centróide de Voronoi) para a
   v8; **111** (C1, ponto da válvula, com raio de incerteza declarado 0,0 m) e
   **120** (C3, centróide de Voronoi) para a v7. O adversário da C2 já pedira
   que se declarasse qual é o objecto de cada número; a C3 acrescentou dois e
   não declarou nenhum. E o certificado descreve mal o seu próprio: «a v8 —
   E530499 N4655022, a 46 m do centróide da sua própria partição» — os 46 m são
   do centróide **ao foco**; da válvula ao seu centróide são 12 m.

### Sobre a «Nota ao adversário que não vou ter» da C3

Escrever uma é boa prática e deve manter-se. Mas os quatro pontos que ela
escolhe são todos os que a camada já sabe resolver, e nenhum é dos oito acima —
o mesmo padrão que o adversário da C2 observou no certificado anterior. Ponto a
ponto: **(1)** a arbitrariedade da partição de Voronoi está bem identificada e a
defesa («o que não herda a arbitrariedade é a ordenação») é boa, mas a camada
usa depois percentagens absolutas — 50,7 %, 46,9 %, 2,8 % — em três factos da
lista fechada; **(2)** «tudo o B5 depende de a v8 estar onde a G35 diz» está
certo e é **menos** grave do que o que R4 mostra, porque nem é preciso deslocar
uma válvula: 15 % do foco já está na v7; **(3)** «111 linhas não são 111
amostras» é o melhor dos quatro, e a camada erra na correcção que ela própria
propõe (12 relatórios são 10 colheitas — R8); **(4)** o B4 ambíguo é real e é o
menor dos quatro. Quem declara os seus pontos fracos declara melhor os que já
sabe resolver — pela segunda vez nesta cadeia.

---

## Veredicto

**O CERTIFICADO NÃO SEGUE COMO ESTÁ. Segue com as oito retiradas da parte 1, e
com a paragem de linha reformulada nos termos de §0.3.**

**Sobre a paragem de linha, que é a pergunta principal:** **mantém-se quanto ao
facto e reformula-se quanto ao dispositivo.** Nada nos dois livros coloca as
quatro ITS ou o «Kiwi 1000» num talhão — está estabelecido, com evidência mais
forte do que a citada, e nenhuma frase da G34 sobre esforço de amostragem pode
ser usada pela C4. Mas «três sítios independentes» são três frases do mesmo
compilador no mesmo livro; e uma ausência documental não refuta testemunho
directo, suspende-o. A linha passa de **REJEITADO** a **NÃO RESOLVIDO — relato
contra documento**, e o reinício em C0 é de uma pergunta, não de uma camada:
*de onde veio aquela atribuição?* **E a paragem de linha está mal executada:** a
razão dada para não parar — «não há nada por cima que dependa da linha
rejeitada» — é falsa por B3, B4, B5 e B2, e o prompt da C4 foi escrito e
entregue à mesma.

**Retiradas (parte 1):** R1 tira a «podredumbre radicular», que não existe em
nenhum material, e com ela a coluna de instrumento independente da linha Becrop;
R2 reescreve B3 como afirmação sobre cobertura de ensaio e não sobre o pomar;
R3 retira o ρ = −0,044 de B6 e a leitura de que não houve selecção; R4 tira os
120 m e a palavra «amostra» de B5; R5 separa as duas classes de número de B10 e
retira a margem ±0,001; R6 corrige 212/212 → 22 comparações efectivas e 146 →
131; R7 estreita a afirmação de ausência da válvula 27 ao que foi de facto
varrido; R8 corrige a repartição de datas de B11 para 5/4/2/1.

**Condição, e é uma só.** **T2 corre antes de a C4 arrancar** — são sete números
que já estão calculados, custam zero, e três deles (B3, B5, B6) mudam o sentido
do que a C4 vai receber. E, dentro dele, **a reformulação de B3 é obrigatória**:
não existe em todo o caso um único ensaio de fungo ou oomiceta com posição, e
deixar «nenhum organismo está onde o padrão está» entrar num livro-razão de
exclusões repete o erro do *P. sojae* com dados melhores.

**Sobre a herança:** verifiquei um a um os números de **L4** e **L6** retirados
pelo `ADVERSARIO_2026-08-29.md` e **nenhuma conclusão da C3 depende de nenhum
deles** — zero ocorrências no certificado e nos doze scripts. A C3 usa L2/L3 e
corrige L5, e nenhum desses foi retirado. Fica uma exposição de vocabulário («sem
pérgola», etiqueta retirada pela R3 do mesmo adversário), que se resolve
trocando a palavra pela altura medida.

**O que passa intacto, e é bastante:** **B9**, a *Rosellinia* — o melhor facto
produzido em qualquer camada desta cadeia, e o único que corrige o material de
origem sem inferir nada por cima; **B11** no seu núcleo — não há linha de base
biológica, e nenhuma comparação antes/depois é possível com estes materiais;
**B7** com a etiqueta corrigida; a linha do ***M. hapla***; **B8**, que sobrevive
mais forte do que foi escrito; e a metade geométrica de **B10**, que é real,
não é circular, é específica de 2026, e obriga mesmo a recalcular tudo o que usou
fosso à referência — no sentido conservador que a camada correctamente
identificou.

Este certificado sobrevive a um adversário sério. Sobrevive mais estreito, com
um facto inteiramente sem origem, dois factos que afirmam o contrário do que
medem, e cinco etiquetas erradas na coluna que o controlo 1 criou de propósito.
Isso é o que se espera que aconteça numa camada em que quase toda a prova é
documental — e o «sobrevive» é honesto.
