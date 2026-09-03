# Adversário da Camada 4 — Inferência

29-08-2026. Ataque ao `CAMADA_4_CERTIFICADO.md`, ao código de `SAIDA_C4\` e ao
`CAMADA_5_PROMPT.md` que a camada escreveu.

**Veredicto em uma linha:** o certificado **segue com dez retiradas e sete
margens alargadas**; o `CAMADA_5_PROMPT.md` **não pode arrancar como está** —
tem três defeitos de uma frase cada, e um deles manda a C5 gastar dinheiro a
procurar organismos que já foram encontrados.

**O que li:** o certificado, `c4_01_numeros.py`/`.json`, `c4_02_razao.py`,
`c4_razao_exclusoes.csv` linha a linha, `c4_02_contagem.json`, o
`CAMADA_5_PROMPT.md`, e — para verificar herança — `PROTOCOLO.md`,
`CONTROLOS.md`, `_MULTIVERSO\ADVERSARIO_H1.md` §5.3 e §5.4,
`_MULTIVERSO\AGREGACAO_H1.md`, `_MULTIVERSO\SAIDA_B\cache\nucleos.json`, as
secções C e D dos adversários da C0, C2, C3 e da adenda, e as tabelas-âncora da
C1, C2 e C3-R2.

**O que não fiz:** não corri nenhuma análise, não abri os dados brutos, não
recomputei nenhum resultado de camada nenhuma. As duas únicas aritméticas que
fiz estão declaradas onde aparecem (R2 e R4) e correm sobre números que o
próprio certificado publica.

**O que peço e não fui buscar:** a proveniência documentada de `3,98 ha` e de
`E530476 N4655046` — ver R2, que é a retirada mais grave deste documento.

---

## SUMÁRIO EXECUTIVO — o que muda no PASSA PARA CIMA

| facto | veredicto |
|---|---|
| **D1** composição do défice | **passa com margem alargada.** As proveniências são **duas**, não três. |
| **D2** acontecimento recente partilhado | **passa com margem alargada.** O instrumento independente que cita (V3) tem uma permutação por correr que o prompt da C4 lhe entregou e ela não transportou. |
| **D3** argumento geométrico só na v8 | **passa com margem alargada.** O «2,60 ha» não está no ficheiro citado como prova, e colide com outro 2,60 que lá está. A razão 2,68× move-se para 4,54× com o outro número que o mesmo certificado publica. |
| **D4** tudo em fosso é limite inferior | **passa com margem alargada e com uma frase retirada.** A direcção aguenta; «a explicação concorrente desapareceu» é falso contra a fonte citada. |
| **D5** *M. hapla* excluído como discriminante | **RETIRA-SE o verbo «excluído».** Passa como «sem gradiente causal e com sinal invertido», que é o que o teste sustenta. |
| **D6** a matriz tem uma coluna | **PASSA, e é o melhor trabalho da camada.** Só o número **13** precisa de definição ao lado. |
| **D7** nove presenças localizadas | **passa com a localização reescrita.** A zona é uma zona de 2026 aplicada a uma amostra de 2025. |
| **D8** zero linhas bacterianas e virais | **PASSA inteiro.** Verificado contra o JSON. |
| **livro-razão** 59 / 41 / 7 / 5 / 4 / 2 | **três estatutos mudam** e o rótulo das 41 tem de ser reescrito antes de a C5 lhe tocar. |

---

# PARTE 1 · FACTOS A RETIRAR DO PASSA PARA CIMA

---

## R1 · O «13» não está no JSON. O JSON diz **10**, com essas palavras exactas.

**É a retirada mais fácil de verificar de todo este documento e atravessa cinco
sítios do certificado.**

`c4_01_numeros.json` → `matriz_resumo` tem dois campos:

```
"linhas_cuja_unica_fonte_e_o_granel_331_2025": [ ...dez organismos... ]
"linhas_com_lugar_mas_sem_par_de_comparacao": 10
```

**Dez.** O certificado publica **treze**, cinco vezes, com a mesma formulação
que o campo do JSON:

- I3: «das quais: assentam SÓ no granel 331/2025 … **13**»
- D6: «**13 assentam numa única amostra composta**»
- §4: «as **treze** linhas»
- NÃO TESTÁVEL 4: «As **treze** linhas que agora têm lugar»
- §8, âncoras: «**13** assentam numa só amostra»

E o `CAMADA_5_PROMPT.md` propaga-o três vezes (linhas 268, 549, 659).

**De onde vem o 13.** Das quinze linhas com algum lugar, dez têm o granel como
**única** fonte; três — *Armillaria* (solo), *Rosellinia* (solo), Oomicetas
(solo) — têm o granel **e** o material espanhol; duas são o *M. hapla*. O 13
sai de somar as três espanholas às dez, com o argumento tácito de que o material
de Ribadumia está rejeitado e portanto a única fonte **utilizável** é o granel.

**Esse argumento é bom. Não está escrito em lado nenhum.** E a aritmética de I3
apresenta-o como se saísse do mesmo campo que dá 10:

```
com algum lugar declarado ...... 15
   das quais: assentam SO no granel ... 13   <- o JSON diz 10
   das quais: com contraste multi-unidade 2
```

**O que teria de ser verdade para isto estar errado:** que «assentam só no
granel» e «a única fonte de Ganfei é o granel» sejam a mesma frase. Não são, e
a diferença é exactamente as três linhas que **carregam os negativos** — que é
a metade do argumento de D6 que mais trabalho faz.

**Teste de cinco minutos:** abrir o JSON e ler o campo. Feito.

**O que cai com ele:** nada de substância. D6 sobrevive inteira. Cai a
apresentação: **um número publicado cinco vezes sob o nome de um campo que dá
outro valor**, numa cadeia cujo controlo 2 existe precisamente para isto.

> **Correcção exigida:** onde estiver «13 assentam numa só amostra composta»,
> escrever «**10 têm o granel como única fonte; 13 têm-no como única fonte de
> Ganfei** — as outras três só têm, além dele, o material espanhol rejeitado».
> Duas linhas. Sem isto, D6 entra na C5 com um número que o seu próprio ficheiro
> de prova contradiz.

---

## R2 · O «maior vazio circular» não é um objecto do testemunho. É o núcleo n.º 22 da corrida B, e o código chama-lhe testemunho de tipo 1.

**Esta é a retirada grave. É o mesmo movimento que produziu o «B1».**

`c4_01_numeros.py`, linhas 36–41:

```python
# ZONA declarada pelo gestor para a amostra "Kiwi 1000" / informe 331/2025:
# "lado oeste do maior vazio circular". O maior vazio e o nucleo redondo de
# 3,98 ha com centro em E530476 N4655046. TESTEMUNHO DIRECTO, tipo 1.
VAZIO_MAIOR = (530476.0, 4655046.0)
VAZIO_MAIOR_HA = 3.98
```

O comentário rotula **a coordenada e a área** como testemunho de tipo 1. Não
são. O testemunho é a frase «lado oeste do maior vazio circular». A coordenada
vem de outro sítio, e o certificado nunca diz qual.

**Onde ela está:** `_MULTIVERSO\SAIDA_B\cache\nucleos.json`, primeiro registo:

```json
{ "id": 22, "E": 530476, "N": 4655046, "ha": 3.98, "first": "2026-07-27",
  "anom": { ... "2024-07-22": -0.03, "2025-08-14": -0.057, "2026-07-27": -0.164 } }
```

É o **N1 da corrida B** da ronda H1. `ADVERSARIO_H1.md` linha 746 dá-lhe a
receita: «periodicidade de linhas na ortofoto, 31,82 ha | **NDVI + NDMI** |
anomalia ≤ −0,06, queen, ≥ 0,08 ha».

**Cinco consequências, por ordem de gravidade:**

**(a) O 11,4 m é a distância entre duas estimativas do mesmo centro, e é menor
do que a dispersão conhecida dessas estimativas.** `AGREGACAO_H1.md` publica os
três centros do foco OESTE: A **E530471 N4655044**, B **E530476 N4655046**, C
**E530500 N4655051** — e escreve, em negrito, «**Trinta metros de dispersão
máxima**». O foco OESTE oficial da cadeia (G34) é E530485 N4655053. Medir
11,4 m entre G34 e a estimativa de B **não mede onde está a amostra**: mede a
discordância entre duas derivações do mesmo centróide, num caso em que essa
discordância vale até 30 m. **O 11,4 m tem informação locacional zero.**

**(b) Os dois extremos do 11,4 m saem do mesmo instrumento.** I6 declara
«*Instrumento independente:* **SIM** — testemunho e partição documental são duas
proveniências». A partição documental (`valvulas_por_area.json`) **não entra no
cálculo do 11,4 m** — entra só no passo seguinte, o do ponto da v7 na faixa E.
O 11,4 m é centróide-NDVI contra centróide-NDVI. **Controlo 1 não está
cumprido para o número que carrega D7 e I6.**

**(c) A precisão é falsa por duas ordens de grandeza.** 11,4 m é 1,14 células
de uma grelha de 10 m, publicado a 0,1 m, entre dois centróides sem margem
declarada, cuja dispersão entre corridas é 30 m.

**(d) O objecto é de 2026 e a amostra é de 2025.** O campo `first` do núcleo 22
é **2026-07-27**: é o ano em que o aglomerado passa a qualificar. A série de
anomalia dele é −0,03 (2024), −0,057 (2025), −0,164 (2026). E a própria datação
da C4 mede o défice do disco OESTE a ir de **0,09 ha (2024) → 1,02 (2025) →
1,49 (2026)**. **A amostra é de 2025-06-06.** O gestor foi ouvido em 29-08-2026
e descreveu o vazio que vê **agora**. Entre a colheita e o testemunho o vazio
cresceu por um factor grande, e o «lado oeste» de 2026 não é o mesmo terreno que
o «lado oeste» de Junho de 2025 — se é que havia um vazio a que chamar o maior
nessa data.

> Isto é exactamente o modo de falha que o `CLAUDE.md` nomeia para o tipo 1:
> «memória, ambiguidade de referência, ou **mudança desde a data a que a pessoa
> se refere**». As quatro cautelas de §0.1 cobrem as duas primeiras. **Não
> cobrem a terceira, que é a que aqui manda.**

**(e) A área 3,98 ha é o topo de uma gama, usada como se fosse uma medição.**
`ADVERSARIO_H1.md` linha 1224: «o foco OESTE, **2,38-3,98 ha**, 45-80 % da área
de núcleo de cada corrida». C4 toma o máximo, deriva r = 112,6 m, e deriva daí
a faixa E530363–E530476 que sustenta o argumento da v7. Com 2,38 ha, r = 87,0 m
e a faixa é E530389–E530476.
*(O argumento da v7 sobrevive nas duas: o ponto da v7 está a E530397,5, dentro
das duas faixas. Digo-o porque é verdade.)*

**E uma nota que não acuso, registo:** a corrida B é a corrida cujo **z = +12,3
o coordenador mandou fora da agregação**. A cadeia foi buscar-lhe uma
coordenada para ancorar a arbitragem mais consequente da camada, sem a nomear.
Um centróide não é o z, e não digo que esteja contaminado. Digo que **a fonte
tinha de estar escrita**.

**Teste de cinco minutos:** perguntar ao gestor «o vazio de que falou já era o
maior em Junho de 2025?» e «consegue apontá-lo numa ortofoto?». Uma pergunta.

**O que cai com ele:** o **número** 11,4 m sai de I6, de D7, de §0.1, de §4 e
das nove linhas BIO-01..09 do livro-razão, onde aparece no campo `ambito`
gerado pela constante `ZONA` de `c4_02_razao.py`. **A localização não cai** —
sobrevive como «metade ocidental de um núcleo de 2,4 a 4,0 ha, adjacente ao foco
OESTE, geometria de 2026 aplicada a uma colheita de 2025-06-06». É menos, e é
o que há.

---

## R3 · «Todas ≈ zero», escrito por baixo de uma tabela cuja primeira linha diz −0,056. E a corrida A mediu o NDVI — o certificado apagou a linha.

**O §9.5 pediu-me este teste. Fi-lo, e o resultado é misto: a conclusão está
certa e a transcrição está errada.**

O que o certificado imprime (§0.4):

```
corrida A (H1)        -0,056 em NDRE, e diz explicitamente que o NDVI nao tem vies
corrida C (H1)        +0,0007 / +0,0045   -> chamou-lhe nulo
ceptico   (H2)        +0,000  / +0,004
patologista (H2)      +0,012
```

E logo abaixo: «**Todas ≈ zero.**»

O que a fonte (`ADVERSARIO_H1.md` §5.3) tem, em cinco linhas e não quatro:

| corrida | o que mediu | resultado |
|---|---|---|
| A | coeficiente S2C no **NDRE** | −0,056, p = 1,3e-15 |
| **A** | **coeficiente S2C no NDVI** | **+0,005 (2026), −0,014 (2025), n.s., sinais opostos** |
| C | \|S2C−S2A\| no NDVI | +0,0007 / +0,0045, n.s. |
| céptico H2 | viés no NDVI, na mata | +0,000 / +0,004 |
| patologista H2 | idem, emparelhado, n = 43 | +0,012 ± 0,008 |

**O certificado apagou a linha que tornaria a sua própria frase verdadeira** — a
medição de NDVI da corrida A — e pôs no lugar dela a medição de **NDRE**, que é
**outro índice** e vale **−0,056**, maior em módulo do que o −0,048 que está a
ser rejeitado. Escrever «todas ≈ zero» por cima de um −0,056 é a classe de erro
que esta cadeia apanhou três vezes.

**São as quatro corridas independentes?** Duas coisas:

1. **A ronda H2 correu com o −0,048 como facto de especificação.** O próprio
   certificado escreve isso na tabela CORRIGIDO. Duas das quatro corridas são
   **a jusante** do erro de agregação da H1. Não são independentes dele.
2. **Mas a contaminação empurra na direcção contrária ao achado.** Uma corrida
   avisada de que deve encontrar −0,048 e que encontra zero é prova mais forte,
   não mais fraca. **O achado aguenta apesar da não-independência**, e digo-o
   com a mesma clareza com que digo o resto.

**Também são emparelhadas?** Sim, e todas do mesmo lado: as quatro medem
**fora do pomar** (máscara de referência, mata, envolvente). Nenhuma mede o
efeito sobre a cauda dentro do pomar. **A C4 regista isso correctamente em NÃO
TESTÁVEL 14 e em INS-06**, e esse trabalho é bom.

**Retira-se:** a frase «Todas ≈ zero» sobre aquela tabela, e a contagem
«**quatro** medições em NDVI», repetida em §0.4, I5, D4, REJEITADO e na tabela
de âncoras. São **quatro medições em NDVI de quatro corridas**, sim — mas só
depois de se substituir a linha de A pelo valor de A em NDVI. **Como está
escrito, são três em NDVI e uma em NDRE que contradiz a legenda.**

*(Nota operacional: o `CAMADA_5_PROMPT.md` já corrigiu isto por conta própria —
escreve «A: sem viés em NDVI». O prompt está certo e o certificado, que é o
documento de arquivo, está errado. Alinhá-los.)*

---

## R4 · «A explicação concorrente acabou de desaparecer» é falso contra a fonte que o certificado cita, e o concorrente está registado duas secções mais à frente pela própria camada.

§0.4, em citação destacada:

> «A queda da referência tinha uma explicação concorrente, e essa explicação
> acabou de desaparecer. O que resta no lugar dela é medição.»

E I5: «O viés do S2C era **a única coisa que competia** com esta leitura».

O `ADVERSARIO_H1.md` §5.3, na frase imediatamente a seguir à retirada do viés:

> «A queda da referência é ou **efeito de ano real**, ou **efeito de
> paisagem** — que é precisamente a pergunta que falta.»

E dez linhas depois: «**Trocar “é calibração” por “é um efeito de paisagem por
explicar” não enfraquece a cadeia: transfere um problema fechado por engano
para a lista dos abertos.**»

**A fonte diz o contrário do que o certificado lhe atribui.** O que
desapareceu foi **uma** explicação concorrente — a instrumental. Ficaram
**duas**, e a camada regista uma delas, por escrito, em **NÃO TESTÁVEL 13** e na
linha **REG-03** do livro-razão: a corrida B mede a paisagem envolvente a cair
**0,075 entre 2024 e 2026, o dobro da queda do bloco**.

**Portanto: no mesmo documento, a camada escreve que o concorrente desapareceu
(§0.4, I5) e regista o concorrente (NT 13, REG-03), e nunca junta as duas
páginas.** É a sexta pergunta de §7 — «se o que se está a medir é o pomar ou a
paisagem» — a contradizer §0.4.

E a direcção do erro é a que §9.5 previu: **para o lado que lhe convinha.**

**Retira-se:** de I5 e de §0.4, «a única coisa que competia» e «acabou de
desaparecer». **Mantém-se em D4** a formulação que já está correcta —
«a explicação **instrumental** que competia com isto está excluída» — com o
acrescento obrigatório: «e ficam duas explicações não instrumentais por testar,
efeito de ano e efeito de paisagem (NT 13 / REG-03)».

---

## R5 · D5 · «Excluído» é forte de mais para um teste que não podia ter sido significativo.

`M_hapla_contra_defice` corre sobre **n = 4**. O próprio JSON escreve: «com n=4
o p exacto de |rho|=1 é 2/4! = 0,083; nenhum destes valores é significativo em
nenhum critério».

**Leia-se o que isso quer dizer.** Com n = 4, a correlação de Spearman
**máxima possível** tem p = 0,083. O desenho **não podia produzir um resultado
significativo em nenhum sentido, quaisquer que fossem os dados.** Um ensaio que
não pode rejeitar não é um ensaio; é uma medição sem poder. Escrever
`estatuto = EXCLUIDA` e `o que a fecharia = nada - esta fechada para esta
pergunta` por cima de um desenho de poder nulo é **converter ausência de ensaio
em ausência de causa** — que é a definição do artefacto que esta camada foi
escrita para produzir com segurança.

**Três problemas a mais, e nenhum está declarado:**

1. **As quatro unidades não são comensuráveis.** `c4_01_numeros.py` linhas
   191–202 vai buscar o défice de B3, B4 e Erica Novo a `por_bloco` e o da V7 a
   `por_valvula`. Três blocos de 4,17 a 9,92 ha e **uma válvula de 3,25 ha da
   partição de Voronoi**. São dois esquemas de partição diferentes dentro de uma
   correlação de quatro pontos.
2. **`"Erica Novo E"` é ligado ao bloco `"Erica Novo"` por igualdade de nome
   aproximada** (linha 192). Numa cadeia que abriu com o «B1» e que catalogou a
   armadilha «B-3/C-3 contra B3» na linha BIO-15 do seu próprio livro-razão,
   uma identidade de unidade por prefixo de nome tem de ser declarada.
3. **O contraponto mais forte é o B1, e o B1 não tem posição** — o próprio
   certificado di-lo. A carga mais alta (250/200 cc) está fora da banda.

**O que aguenta, e aguenta bem:** o **sinal**. Positivo em 4/4 unidades
colocadas, com a contagem mais baixa no bloco mais afectado e a mais alta num
bloco sem posição. **Não há gradiente na direcção causal.** Isso é informação
real e é o achado.

**Retira-se o verbo.** D5 passa reescrita:

> **D5.** O *M. hapla* está presente em 4/4 unidades colocadas e **não mostra
> gradiente no sentido causal**: ρ(défice, solo) = −0,40, ρ(défice, raiz) =
> −0,80, contagem mais baixa no bloco mais afectado, contagem mais alta no B1
> sem posição. **Não sustenta o contraste entre os focos.** Não está excluído
> como discriminante: **o desenho (n = 4, uma data, um método, duas partições
> misturadas) não tem poder para excluir nada.**

E no livro-razão, **BIO-16 passa de EXCLUÍDA a INCONCLUSIVA**, com
`o que a fecharia` = «as mesmas contagens em ≥ 8 unidades comparáveis da mesma
partição, ou o mesmo par em terreno comprovadamente são».

---

## R6 · ABI-08 · «Nenhum produto de precipitação resolve 496 m» é uma limitação do instrumento, não um facto sobre a chuva.

Linha do livro-razão, estatuto **EXCLUÍDA**, âmbito «os 496 m que separam os
dois focos», prova «C1 S16: nenhum produto de precipitação resolve 496 m».

**A premissa que teria de ser verdade:** que a precipitação **não varia** a
496 m. O que está medido é outra coisa: que **nenhum produto disponível a
mostra** a 496 m. Célula convectiva de Verão varia bem abaixo do quilómetro; o
ERA5-Land é que não a vê.

Isto é, literalmente, «não temos instrumento a esta escala, logo a causa está
excluída». É a operação que este livro-razão existe para impedir.

**Retira-se o estatuto.** ABI-08 passa a **NÃO TESTADA**, com o âmbito
reescrito — «nenhum produto de precipitação disponível resolve 496 m; a causa
não foi ensaiada a esta escala» — e `o que a fecharia` = «um udómetro em cada
foco, ou radar meteorológico a 1 km com composição sub-horária».

*(A frase de S16 continua verdadeira e continua útil: diz que **este** caso não
pode atribuir o contraste à chuva com **estes** dados. Isso é o âmbito. Não é
uma exclusão.)*

---

## R7 · INS-02 · Uma exclusão que assenta numa cena que a camada de baixo mandou excluir e que nunca foi re-certificada.

A margem da própria linha diz tudo:

> «A V11 assenta inteiramente na cena de 2019-09-02, que a R2 G10 mandou
> excluir e que a C2 **repôs sem paragem de linha**. A C0 nunca re-certificou a
> G10 (condição 1 do adversário da C2, **por cumprir**).»

**Uma linha cuja margem declara que a sua prova está por certificar não pode ter
estatuto EXCLUÍDA.** A disciplina está no campo de texto livre; a coluna que a
C5 vai ler diz `EXCLUIDA`.

**Retira-se para condicional.** INS-02 passa a **EXCLUÍDA-CONDICIONAL** — ou,
se se preferir não inventar um sexto estatuto, a **INCONCLUSIVA** — com o texto
«excluída **sob condição** de a C0 re-certificar a G10; se a cena de 2019-09-02
sair, a barra de erro de V11 tem de ser refeita e esta linha reabre».

---

## R8 · ABI-04 · Exclusão com o campo «instrumento independente» a dizer «nenhum».

`instrumento independente: nenhum - e a mesma serie optica reagrupada`.
Estatuto: **EXCLUÍDA**.

O Controlo 1 é explícito: «**Se não houver instrumento independente disponível,
o facto vai para NÃO TESTÁVEL, não para PASSA PARA CIMA.**»

Não retiro a linha — o critério de falsificação foi escrito antes de correr e
foi cumprido, o que é boa prática e raro nesta cadeia — mas **o estatuto tem de
levar a marca**. A exclusão do agrupamento por válvula é uma exclusão **dentro
do instrumento óptico**, e a C5 tem de a ler assim, porque é numa válvula que
está a maior anomalia de radar do caso (ABI-05, NÃO TESTADA).

**Correcção:** manter EXCLUÍDA, acrescentar ao âmbito «**sem instrumento
independente — exclusão interna à série óptica**».

---

## R9 · ABI-11 e ABI-12 · A mesma regra dá SUSTENTADA a oeste e INCONCLUSIVA a leste.

**Esta é a inconsistência mais nítida do livro-razão e é a que mais me
preocupa, porque corre na direcção do achado da camada.**

- **ABI-12** (solo pobre no B3, bloco do foco **ESTE**) → **INCONCLUSIVA**.
  Razão: «S9 fixa o factor de 2 como limiar de interpretabilidade e **S8 corre
  sobre n = 1 boletim**. Dentro do B1 três sub-parcelas dão CaO **314, 439 e
  4700**.»
- **ABI-11** (carência de cálcio no bloco do foco **OESTE**) → **SUSTENTADA**.
  Prova: «solo CaO **264 e 505** mg/kg; folha Ca 2,2 % contra referência 3–4,7 %».

**264 e 505 é um factor de 1,9 dentro do mesmo bloco.** A regra S9, invocada
uma linha antes para tornar o lado oriental inconclusivo, diz que abaixo de um
factor de 2 nada é interpretável, e que a dispersão intra-bloco documentada
chega a **15×**. Aplicada a ABI-11, a mesma regra dá o mesmo resultado que deu a
ABI-12.

A margem de ABI-11 confessa metade disto — «o contraste de CaO **entre** blocos
está retirado» e «**NÃO EXISTE análise foliar para o B3**» — e ainda assim a
linha fica SUSTENTADA. Sustentada contra o quê? **Não há bloco de comparação.**
É a mesma estrutura de prova das nove linhas BIO-01..09 (positivo num sítio, sem
par), e essas estão em NÃO TESTADA.

**Retira-se.** ABI-11 passa a **INCONCLUSIVA** (ou, se se mantiver a assimetria
de estatutos, a «SUSTENTADA-LOCAL» — ver R10). O que sobrevive intacto é a
folha: Ca 2,2 % contra referência 3–4,7 % é um contraste **contra referência
externa**, e é a metade boa da linha. **A metade do solo não sustenta nada.**

---

## R10 · O livro-razão dá qualificador de âmbito às exclusões e nenhum aos apoios. Num livro de exclusões, isso é enviesamento estrutural.

Os cinco estatutos, tal como `c4_02_razao.py` os define:

```
SUSTENTADA        - o material apoia-a como contribuinte
EXCLUIDA          - o material exclui-a como explicacao do padrao
EXCLUIDA-LOCAL    - excluida so numa zona, numa data e numa matriz, n = 1
INCONCLUSIVA      - foi testada e o teste nao decidiu
NAO TESTADA       - ninguem procurou
```

**Há EXCLUÍDA-LOCAL. Não há SUSTENTADA-LOCAL.** O certificado justifica os
cinco estatutos com um argumento correcto — «o âmbito é a diferença entre um
resultado e uma exclusão» — e depois **aplica o âmbito só de um lado**.

O que isso produz, medido nas cinco SUSTENTADAS:

| linha | n / desenho | instrumento independente (campo do próprio CSV) |
|---|---|---|
| ABI-03 água concentrada no foco OESTE | LiDAR, uma campanha | SIM |
| ABI-11 carência de cálcio | 2 boletins, um bloco, **sem comparação** | SIM (contestado — R9) |
| **REG-02** perda em bloco desde 2023 | **UMA corrida, UM instrumento óptico** | **«NÃO na lista fechada»** |
| INS-03 referência contaminada | 110 células, sem bootstrap | SIM |
| **INS-04** a referência está em declínio | herdado | **«NÃO — falta a série Landsat»** |

**Duas das cinco SUSTENTADAS declaram, no seu próprio campo, que não têm
instrumento independente.** Uma delas — **INS-04** — é a linha que sustenta
**D4**, que está na lista fechada. O `CONTROLOS.md` diz que um facto sem
instrumento independente **vai para NÃO TESTÁVEL, não para PASSA PARA CIMA**.
D4 declara «*Instrumento independente:* herdado de B10» — mas B10/INS-03
sustenta que a referência está **geometricamente contaminada**, e o que D4
afirma é a proposição de **INS-04**, que a referência **está em declínio**.
**D4 empresta a INS-04 o instrumento de INS-03.**

E **REG-02** é N = 1 numa cadeia cujo próprio `CLAUDE.md` escreve «**N = 1 não é
verificação**… para inferência, três a cinco corridas independentes». A camada
sabe-o: §9.4 confessa-o. E marcou-a SUSTENTADA na mesma.

**Portanto, e é o achado estrutural desta parte:**

> Um resultado **negativo** de laboratório, n = 1, uma zona, uma data → o livro
> inventa um estatuto para o qualificar: **EXCLUÍDA-LOCAL**.
> Um resultado **positivo** de uma corrida, n = 1, um instrumento, sem
> instrumento independente → **SUSTENTADA**, sem qualificador nenhum.

Isto não é má fé; é a assimetria natural de quem escreve um livro de exclusões
e vigia sobretudo o lado das exclusões. Mas o efeito líquido é fazer a prova
negativa parecer mais fraca e a positiva mais forte do que o material aguenta,
e é precisamente esse enviesamento que a C5 vai herdar e converter em desenho
de amostragem.

**Correcção exigida:** criar **SUSTENTADA-LOCAL** e reclassificar ABI-11 e
REG-02 — ou, alternativa mais barata e igualmente boa, acrescentar uma coluna
`n` e uma coluna `poder` ao CSV e deixar os estatutos como estão. **Uma coluna
com o n de cada linha resolve metade das objecções deste documento.**

---

# PARTE 2 · FACTOS A MANTER, COM MARGEM MAIOR

---

## M1 · D1 · São **duas** proveniências, não três — e a terceira não é uma medição, é uma partição.

I1 e D1 declaram «**SIM, três proveniências que não se produzem umas às
outras** — a tabela de áreas do gestor (documento) para a partição, a ortofoto
de 2021 (estrutura) para o chão lavrado, e a série Sentinel-2 para o défice e
para a regra M2».

**Verifiquei, e uma delas aguenta muito bem.** O `nu2021` é genuinamente
independente: a C1 estabelece que vem da ortofoto de 25 cm de 2021 por
comparação **dentro de uma só imagem**, e que o **SAR** — instrumento activo,
banda C, posterior e sem relação com a óptica — separa a mesma área em todos os
dez Invernos, com 1,2 a 3,5 dB de diferença. **Isso é a regra do instrumento
independente cumprida a sério, e é o melhor pedaço de D1.**

**As outras duas não são duas:**

- O quociente que carrega o título — **93 % na v8 contra 36 %/34 % nas
  v13/v14** — é `pct_novo_M2 / pct_defice_2026`. **Numerador e denominador saem
  da mesma série Sentinel-2, do mesmo limiar e da mesma máscara.** É um
  instrumento.
- A terceira coluna — **3,5 % contra 52,4 %** de histórico anterior a 2025 —
  sai de `datacao_focos`, que é **a mesma série Sentinel-2 outra vez**, num
  disco de 120 m centrado em centróides derivados dessa mesma série.
- A «tabela de áreas do gestor» **não mede nada**. Fatia. E o que fatia é uma
  partição de Voronoi que o próprio certificado descreve, em §9.2, como «uma
  partição de Voronoi cuja arbitrariedade a C3 declarou e que eu herdei sem
  testar». **Um documento que restringe uma construção geométrica não é uma
  proveniência de medição.**

**E há uma dependência algébrica não declarada entre as duas colunas que
sobram.** Uma célula em défice em 2021 **não pode**, por construção da regra M2,
contar como «declínio novo» em 2026. Logo `pct_nu2021` alto **força**
`novo/défice` baixo. A implicação não é total — a v9 tem 0 % de chão lavrado e
0,23 de fracção nova, o que prova que a coluna do S2 tem informação própria —
mas metade da coerência entre as duas colunas é aritmética, não confirmação.

**D1 mantém-se.** O contraste é real e é o achado mais sólido da camada a
seguir a D6. **A margem tem de dizer: duas proveniências (Sentinel-2 e
ortofoto/SAR), uma partição documental, e uma implicação algébrica parcial entre
as duas colunas.**

---

## M2 · D3 · O «2,60 ha» não está no ficheiro citado como prova — e há **outro** 2,60 ha nesse ficheiro, que é outro objecto.

D3 escreve: «Números: **2,60 ha defensável, 3,58 ha tecto** … *Prova:*
`c2_05_manchas.json` → `m2`».

O que `m2` tem, verbatim do JSON da própria camada:

```json
"m2": { "sao_antes_ha": 20.97, "defice26_ha": 7.86,
        "novo26_ha": 3.58, "novo25_ha": 1.98 }
```

**Não há 2,60.** O 2,60 vem de W2, do adversário da C2, e I8 di-lo («critério
duro»). O campo *Prova* de D3 aponta para o sítio errado.

**E é pior do que um erro de citação, porque o número existe no ficheiro com
outro significado.** `datacao_resumo.OESTE.ha_em_defice_2026_no_disco_120m` =
**2,60**. Quem for verificar D3 encontra 2,60 no ficheiro citado, dá o número
por confirmado, e confirmou um objecto diferente — a área em défice no disco de
120 m do foco OESTE, que nada tem a ver com o critério duro de M2 sobre o pomar
inteiro.

**É a mesma armadilha de colisão que esta cadeia já pagou três vezes**
(34/35/43/46 m; dois «0,048» de sinal oposto; três números para o défice de
2026). **Corrigir o campo *Prova* de D3 e nomear os dois 2,60.**

## M3 · D3 · A razão de 2,68× move-se para 4,54× com o outro número que o mesmo certificado publica.

`taxa_de_base` calcula-se assim (`c4_01_numeros.py`, 147–156):

```
defice sobre terreno sao       = 100 * novo26 / sao_antes = 100*3,58/20,97 = 17,1 %
defice sobre terreno historico = 100 * (defice26 - novo26) / (30,31 - sao_antes)
                               = 100*(7,86-3,58)/9,34     = 45,8 %
razao = 2,68
```

O numerador do primeiro é **3,58**, que o próprio D3 declara **tecto** na frase
anterior. Se se usar o número que D3 chama **defensável** — 2,60 —, sai:

```
sobre terreno sao       = 100*2,60/20,97 = 12,4 %
sobre terreno historico = 100*(7,86-2,60)/9,34 = 56,3 %
razao = 4,54
```

**Um documento que publica os dois números publica implicitamente as duas
razões, e só reporta uma.** *(Aritmética minha, sobre números do certificado.)*

**Não é fatal e é conservador para a conclusão** — 4,54× reforça D3, não a
enfraquece. Mas o valor 2,68 entra na C5 como se fosse um facto medido, e não
tem margem nenhuma declarada. **Reportar «2,7× a 4,5×, conforme se tome o
critério duro ou o tecto de M2».**

E uma terceira sensibilidade que ninguém corre: `defice26_ha = 7,86` é a versão
**com abertura morfológica 2×2**. Existem 9,47 e 10,32. A razão move-se outra
vez.

---

## M4 · D4/I5 · A derivação do limite inferior está certa, e desliza entre média e mediana no passo que decide a dimensão.

**A derivação, verificada:** a moeda é o fosso à referência da mesma data; o
limiar do défice é `mediana da referência − 0,05`. Se a referência cai, o limiar
cai com ela e menos células qualificam. **Logo, contra uma referência sã fixa,
tanto a magnitude em fosso como a área em défice são limites inferiores.**
**A lógica é válida e a direcção está certificada.** Concordo com D4.

**Mas o que governa a dimensão é a queda da MEDIANA, e o que o certificado
exibe é a queda da MÉDIA.** As duas metades do argumento puxam a mesma
estatística em sentidos opostos:

- A perna «a área é limite inferior» precisa que a **mediana** desça — e o T4
  mede-a a descer **0,0219**.
- A perna «é um subconjunto de células a colapsar, não é sensor» precisa que a
  **mediana** seja robusta enquanto a **média** cai — e é isso que o afastamento
  a alargar 31× diz.

O certificado cita repetidamente o **0,0548 da média** ao lado da conclusão
sobre a área. **A média não entra no limiar.** O efeito real sobre a área é
governado pelos 0,0219 — que ainda assim é 44 % da folga de 0,05 do limiar e
continua a ser substancial. **Não muda a conclusão; muda o número que a
sustenta, e nenhum dos dois está escrito ao lado da afirmação certa.**

## M5 · D4/I5 · Há **três** pares de números para «a referência em 2017 e 2026», e a C2 já tinha resolvido a questão que a C4 reabre.

- **Referência das três manchas** (a do `CONTROLOS.md`): 0,8379 → 0,8862.
  **Sobe +0,048.**
- **Referência sistemática** (G6/G25, citada por D4 como prova): 0,8884 →
  0,8425. **Desce 0,046.**
- **Tabela de âncoras da C4** (§8): 0,8898 → 0,8766. **Desce 0,013.**

O certificado da C2 **resolveu isto explicitamente**: «A inversão de sinal da R2
G6/G25 confirma-se: **não é divergência, são objectos diferentes.**» A C4 §8
reporta a linha como «divergência — e o sinal inverte-se», sem citar a
resolução, **e com um terceiro par que não é nenhum dos dois** e que a C4 não
calculou (o `c4_01_numeros.py` não toca em séries de NDVI; o par vem do JSON da
C3, via a secção D do adversário da C3).

**Isto importa para D4 e não é cosmético.** D4 diz «direcção certificada,
dimensão não». O mesmo certificado publica duas dimensões para a mesma queda —
**0,046 e 0,013, um factor de 3,5** — e não as reconcilia nem as nomeia como
objectos distintos. Quem quantificar o limite inferior de D4 a partir da tabela
de âncoras obtém um terço do que obtém a partir do campo *Prova* de D4.

**Manter D4. Alargar a margem para: «a queda da referência vale 0,013 a 0,046
conforme o objecto de referência; os três objectos têm de ser nomeados antes de
qualquer quantificação».** *(E o `ADVERSARIO_H1.md` já tinha pedido isto: «Dois
“0,048” de significado oposto a circular no mesmo caso é um risco de colisão do
género que já custou tempo aqui com o “B1”. **Convém nomeá-los.**» Não foram
nomeados.)*

---

## M6 · D7 e I6 · A zona do testemunho está metade fora do disco do foco, e a frase «a amostra está no foco ocidental» não sai destes números.

§0.2 escreve, em negrito: «**Portanto: a amostra está no foco ocidental e não se
pode atribuir a uma válvula.**»

A segunda metade da frase é impecável. A primeira não sai da geometria que a
própria camada publica. Com os números do certificado — vazio de 3,98 ha, centro
E530476 N4655046, raio equivalente 112,6 m, foco OESTE em E530485 N4655053,
disco de 90 m:

```
metade ocidental do vazio dentro do disco de 90 m do foco OESTE ....... 55,7 %
distancia de um ponto da zona ao centro do foco ................. 9 m a 124 m
```

*(Integração numérica minha sobre os números publicados; com a área alternativa
de 2,38 ha da gama do `ADVERSARIO_H1.md` dá 90,2 % e 9–98 m.)*

**A zona declarada está, na melhor leitura, 56 % dentro do foco.** E é aí que o
11,4 m faz o trabalho retórico que §9.1 mandou procurar: colocado ao lado da
palavra «amostra» — §4, «uma amostra composta colhida em 2025-06-06 no lado
oeste do maior vazio circular, **a 11,4 m do centro do foco OESTE**» — converte
uma zona de dois hectares num ponto. **É a conversão que a camada foi instruída
a não fazer, e ela vigiou-a na cautela 1 e depois praticou-a na prosa.**

**D7 mantém-se** — as nove presenças são reais, o aviso é correcto e a advertência
sobre o *P. sojae* é o melhor parágrafo do certificado. **A localização
reescreve-se:**

> zona: metade ocidental de um núcleo de 2,4 a 4,0 ha adjacente ao foco OESTE,
> delimitado por anomalia óptica em 2026; **cerca de metade dessa zona cai fora
> do disco de 90 m do foco**; a amostra é de **2025-06-06**, catorze meses antes
> da geometria que a localiza. **Nenhuma distância a um foco pode ser citada
> para esta amostra.**

## M7 · D2 · O instrumento independente de D2 é o V3, e o prompt da C4 entregou-lhe a informação de que a permutação do V3 não correu.

`CAMADA_4_PROMPT.md`, lista de lacunas, item 7:

> «**A permutação de V3 sobre os 56 mosaicos não correu** (R2 do adversário).»

`CAMADA_4_CERTIFICADO.md`, I7: «a co-datação NDVI×SAR sobre 81 mosaicos de
geometria pura (V3, ρ = +0,57 a +0,60, permutação p < 0,0002). **Isso é real e
aguenta.**» E D2: «*Instrumento independente:* óptico × radar (V3)».

**A lacuna não aparece em nenhuma das quinze entradas de NÃO TESTÁVEL da C4, e
não aparece no `CAMADA_5_PROMPT.md`.** A C4 recebeu-a, usou o facto, e
não a transportou. Isto é a **décima sexta** ocorrência do padrão que a própria
camada denuncia — e é a primeira cometida pela camada que o descobriu. Ver a
transversal E.

**D2 mantém-se** (o ρ e o p publicados são sobre 81 mosaicos e existem), **com a
margem: a permutação pedida sobre o subconjunto de 56 continua por correr, e
com ela a frase «retirando os mosaicos a menos de 130 m, sobrevive», que já está
em NÃO TESTÁVEL.**

## M8 · ABI-03 · Uma diferença de **2 cm** a sustentar «água concentrada no foco OESTE».

`C1 S6: altura sobre a drenagem 0,130 m (OESTE) / 0,150 (ref) / 0,353 (ESTE)`.

O contraste OESTE-contra-referência é **0,020 m**. É uma ordem de grandeza
abaixo da exactidão vertical típica de um MDT LiDAR agrícola, e nenhuma margem
vertical está declarada em lado nenhum da linha.

**O que S6 sustenta é o lado ESTE** — 0,353 contra 0,130/0,150 é um contraste de
mais de 2× e sobrevive a qualquer margem razoável. **O que não sustenta é o
título da linha.** ABI-03 mantém-se SUSTENTADA se for reescrita como «**o foco
ESTE está sensivelmente mais alto sobre a drenagem do que o OESTE e do que a
referência**»; como «água concentrada no foco OESTE» não se aguenta.

---

# PARTE 3 · O LIVRO-RAZÃO — o ataque que o prompt pediu primeiro

## 3.1 · As 7 EXCLUÍDAS e as 4 EXCLUÍDA-LOCAL, linha a linha

**Aguentam limpas (2):**

- **ABI-01 · declive.** 0,336/0,406/0,427 graus, tudo abaixo de 0,5. LiDAR/MDT
  contra série óptica. «Encosta» é categoricamente falso. **Boa exclusão.**
- **ABI-02 · posição topográfica húmida.** Hipótese fixada antes de correr, na
  direcção certa, contradita com ρ da cota negativo em **todas** as onze cenas,
  p < 1e-24, potência com ~2 200 células, MDT contra Sentinel-2. **É a melhor
  exclusão do livro** e é o modelo do que uma exclusão deve ser.
  *(Uma ressalva, que a própria linha faz: «O TWI não tem gama sobre pomar
  nivelado e devia ter ficado em NÃO TESTÁVEL, não em retirada.» Está no campo
  de texto livre; a coluna diz EXCLUÍDA. Ver 3.3.)*

**Não aguentam o estatuto (3):** BIO-16 (R5), ABI-08 (R6), INS-02 (R7).

**Aguenta com marca (1):** ABI-04 (R8) — exclusão sem instrumento independente.

**Aguenta com a legenda corrigida (1):** INS-01 (R3) — a conclusão é boa, a
tabela que a sustenta está mal transcrita e duas das quatro corridas são a
jusante do erro que testam.

**As quatro EXCLUÍDA-LOCAL — BIO-10, 11, 12, 14 — são o melhor trabalho do
livro-razão e não lhes toco.** O âmbito está escrito com precisão («uma zona,
uma data, uma matriz, n = 1»), a de BIO-14 nomeia a razão pela qual o negativo
de solo não cobre a raiz onde a **mesma amostra** dá positivo a um oomiceta, e a
de BIO-12 protege explicitamente a observação de campo de 2026-08-04. **É
exactamente a operação que o prompt pedia.** A única correcção é a de R2: a zona
é uma zona de 2026.

> **Resposta à pergunta que me foi feita:** sim, há exclusões que são não-testadas
> disfarçadas. São **três** — BIO-16, ABI-08 e INS-02 — e nenhuma delas é uma das
> quatro EXCLUÍDA-LOCAL. **O erro do *P. sojae* não se repetiu no sítio onde a
> camada estava a olhar. Repetiu-se nos três sítios onde não estava.**

## 3.2 · As 41 NÃO TESTADAS — o rótulo está errado para pelo menos 16 delas, e é o defeito que trava a C5

A legenda, tal como `c4_02_razao.py` a define e o certificado a imprime:

> **NÃO TESTADA — ninguém procurou. 41.**

Percorrida linha a linha, essa frase é falsa para:

| linhas | quantas | o que realmente aconteceu |
|---|---|---|
| BIO-01 … BIO-09 | **9** | **procurado e ENCONTRADO.** POSITIVO no granel 331/2025. |
| BIO-15, 18, 19, 20, 21 | **5** | procurado em Espanha e **POSITIVO lá**; zero informação de Ganfei. |
| BIO-17 | 1 | *M. hapla* medido em **cinco** unidades, positivo em todas; falta é o nível de referência externo. |
| GES-01 | 1 | corrida e **parcialmente CONTRADITA** pelos dados de piso de Inverno. |
| INS-05 | 1 | não é uma causa candidata: é **uma leitura retirada**, com âmbito «nenhum». |
| **total mal rotulado** | **≥ 17** | |

Acrescente-se GES-06 e GES-07, que a própria margem declara incapazes de
explicar seja o que for no corpo principal («só existe no B1»; «não pode
explicar nada no corpo principal, por nunca lá ter existido») — e que portanto
inflacionam o 41 e o 59 sem serem candidatas ao padrão.

**O que isto faz à C5, em concreto.** O `CAMADA_5_PROMPT.md` escreve, duas
vezes:

> «É a lista do que **ninguém procurou**.» (linha 367)
> «Tarefa 2 · `c4_razao_exclusoes.csv` tem 41 causas que **ninguém procurou**.
> Ordena-as por consequência × custo.» (linha 558)

Uma C5 que faça isso literalmente vai orçamentar ensaios para procurar
*Fusarium oxysporum*, *Neofusicoccum parvum*, *Ceratobasidium* e
*Globisporangium intermedium* **como se nunca tivessem sido procurados**, quando
o que falta para essas nove linhas não é um primeiro ensaio: é **um segundo
ponto**. E a tarefa 1 do mesmo prompt sabe-o («a primeira coisa que qualquer
amostragem tem de produzir é a coluna que falta»). **As tarefas 1 e 2 do prompt
da C5 dão à mesma pessoa duas leituras incompatíveis das mesmas nove linhas.**

**Correcção exigida, e é a que trava o arranque da C5.** Ou se parte a coluna
`estatuto` em duas — `estatuto` e `procurado_onde` — ou se partem as 41 em três
rótulos:

```
NUNCA PROCURADA          - 24   (BIO-22..27, ABI-05..15 excepto testadas, GES-02..04, GES-08, REG-01, REG-03, INS-06 ...)
ENCONTRADA SEM COMPARACAO -  9   (BIO-01..09)  <- precisa de um SEGUNDO ponto, nao de um primeiro
PROCURADA FORA DE GANFEI  -  5   (BIO-15, 18, 19, 20, 21)
+ os casos avulsos: BIO-17, GES-01, INS-05
```

**Custo: reetiquetar uma coluna num CSV que já está escrito.**

> **Resposta à segunda metade da pergunta que me foi feita:** perguntou-se-me se
> as 41 estão apresentadas de forma que a C5 as possa ler como excluídas. **O
> risco é o inverso e é maior.** A C5 vai lê-las como «nunca procuradas», e nove
> delas são presenças confirmadas de patogénio no foco. **Um livro-razão que
> etiqueta um positivo de laboratório como “ninguém procurou” não converte
> ausência de ensaio em ausência de causa — converte um achado em ausência de
> ensaio.** É o mesmo mecanismo a andar para trás, e faz-se com a mesma coluna.

## 3.3 · O defeito de desenho que atravessa o CSV inteiro: a disciplina está no texto livre, o estatuto está na coluna

Em ABI-02, o «devia ter ficado em NÃO TESTÁVEL» está no campo *margem*. Em
INS-02, o «a C0 nunca re-certificou a G10» está no campo *margem*. Em ABI-11, o
«não existe análise foliar para o B3» está no campo *margem*. Em REG-02, o «UMA
corrida, UM instrumento» está no campo *margem*. Em INS-04, o «NÃO — falta a
série Landsat» está no campo *instrumento independente*.

**Em todos os cinco casos, a coluna `estatuto` diz o contrário do que o campo de
texto diz.** E `estatuto` é a única coluna que um leitor apressado, um resumo,
uma tabela dinâmica ou uma camada seguinte vão ler. `c4_02_contagem.json`
agrega por `estatuto` e por `classe` — e é essa agregação, «59 / 41 / 7 / 5 / 4
/ 2», que o certificado publica como âncora, que o `PROTOCOLO.md` copiou para o
seu quadro de estado, e que o `CAMADA_5_PROMPT.md` entrega à C5.

**Um livro-razão de exclusões é perigoso exactamente por isto: a prosa cuidada
não sobrevive à agregação, e é a agregação que viaja.**

Uma coluna `n` e uma coluna `poder` — e um qualificador `-LOCAL` do lado
positivo — resolveriam mais objecções deste documento do que qualquer análise
adicional.

---

# PARTE 4 · AS QUATRO TRANSVERSAIS, MAIS UMA

## A · A regra do instrumento independente foi cumprida?

**Contagem sobre as oito linhas do PASSA PARA CIMA:**

| | instrumento independente a sério | com nome mas sem substância | nenhum, e declarado |
|---|---|---|---|
| D1 | ortofoto/SAR para `nu2021` | «três proveniências» são duas e uma partição (M1) | |
| D2 | óptico × radar (V3) | permutação por correr (M7) | |
| D3 | herda D1 | idem | |
| D4 | | **empresta o instrumento de INS-03 a uma afirmação de INS-04** (R10) | INS-04 declara «NÃO» |
| D5 | laboratório × Sentinel-2 — **cumprido** | | |
| D6 | | | nenhum, correctamente declarado (conclusão negativa) |
| D7 | | testemunho × partição **não sustenta o 11,4 m** (R2) | nenhum para o resultado, declarado |
| D8 | | | nenhum, correctamente declarado |

**Duas linhas cumprem a regra a sério: D5 e a perna `nu2021` de D1.** Duas
declaram honestamente não ter (D6, D8) e passam pela razão certa — são
conclusões negativas que retiram um dado. **Duas invocam um instrumento que não
cobre a afirmação que fazem (D4, D7).** E o único instrumento verdadeiramente
externo que o caso produziu — a **série Landsat**, outra agência, outro sensor,
outra cadeia de correcção — continua **fora de todas as listas fechadas**, pela
terceira camada consecutiva, depois de o adversário da adenda lhe ter chamado «o
melhor trabalho do dia» e ter dito que devia entrar.

## B · O que é que a camada NÃO se perguntou?

Está na Parte 5.

## C · Entrou alguma coisa pela porta do lado?

**Quatro itens, e o primeiro é o grave.**

1. **`E530476 N4655046` e `3,98 ha`** entraram como constantes literais em
   `c4_01_numeros.py` com um comentário que lhes chama **testemunho de tipo 1**,
   e o certificado nunca nomeia a fonte. São da corrida B da ronda H1. **R2.**
2. **O par `0,8898 / 0,8766`** aparece na tabela de âncoras da C4 sem sair de
   nenhum ficheiro que a C4 produziu, e não corresponde a nenhum dos dois
   objectos que a C2 tinha resolvido. **M5.**
3. **O «13»** entrou por aritmética manual sob o nome de um campo do JSON que dá
   10. **R1.**
4. **E uma coisa saiu:** a lacuna da permutação de V3, entregue pelo prompt e
   ausente de todas as saídas da camada. **M7.**

**E um contra-exemplo que registo porque é bom:** o cabeçalho de
`c4_01_numeros.py` declara a regra R1 do adversário da C3 — «nenhum valor
numérico é transcrito à mão» — e o corpo do ficheiro **infringe-a seis vezes**
(as quatro coordenadas de objectos, `VAZIO_MAIOR_HA`, `POMAR_HA`), declarando
apenas **uma** («o único valor que não vem destes JSON»). **O cabeçalho e o
código não batem certo, que é a segunda regra de higiene do `CLAUDE.md`
(«ler sempre os dois»), aqui em ponto pequeno mas no ficheiro que produz o
número mais consequente da camada.**

## D · As quantidades-âncora batem certo?

**A tabela de §8 é a mais honesta da cadeia até aqui** — declara nove
divergências, reporta os três objectos do défice de 2026, e assinala «nove cenas
no código, dez no certificado» sem a resolver, como o protocolo manda. Duas
observações:

1. **A coluna «declarado» já não é a do `CONTROLOS.md`.** Onde o controlo diz
   `polígono pomar = 2903 px / 29,0 ha`, a C4 escreve `declarado 30,31 ha`. A
   C1 e a C2 fizeram isto bem: a C1 declarou 2903/29,0 e obteve 3031/30,31 com
   a explicação; a C2 reportou **as duas linhas**. A partir da C3, o «declarado»
   passou a ser o valor da camada anterior. **A âncora deixou de ancorar em
   nada fixo** — que é a única coisa que o Controlo 2 tinha de garantir.
2. **A linha do NDVI da referência é uma divergência já resolvida, reaberta com
   um terceiro par de números.** **M5.**

## E · TRANSVERSAL DA CADEIA — quantas vezes é que um facto corrigido a montante chegou acima sem a correcção?

**A pergunta que me foi feita era se isto é padrão ou acidente. É padrão, é
estrutural, e o `PROTOCOLO.md` prescreve-o na regra 1.**

**Inventário do que está documentado nos próprios ficheiros da cadeia:**

| # | o que se corrigiu | onde se corrigiu | chegou acima? | quem apanhou |
|---|---|---|---|---|
| 1 | G10 / cena de 2019-09-02 mandada excluir | R2 da C0 | **não** — a C2 repôs a cena por leitura deslocada da cláusula e declarou «não há paragem de linha»; a C0 nunca re-certificou | adversário da C2, ainda aberto na C4 |
| 2 | nove cenas no código contra dez no certificado | `c2_00_comum.DATAS` | **não** — a C3 correu todo o B10 sobre nove | adversário da C3, ainda aberto na C4 |
| 3 | o **−0,048** do S2C | nunca foi medido por ninguém | **quatro saltos**: prosa da C2 → L5 (lista fechada) → agregação da H1 («A e C mediram-no») → especificação da H2 → veredicto da H2 a corrigir um número que não existia | adversário da H1 |
| 4 | L4 e L6 retirados | adversário da adenda | **sim** | — *(o único caso limpo)* |
| 5 | L7, dois acertos de W2 | adversário da adenda | **não** | a própria C4 |
| 6 | L8, 251 cenas e sem «recuperação» (R8) | adversário da adenda | **não** — e a tarefa 2 do prompt da C4 mandava usar a recuperação como prova | a própria C4 |
| 7 | R6, a leitura NDMI retirada por inteiro | adversário da adenda | **não** — a tarefa 6 inteira do prompt da C4 estava construída sobre ela | a própria C4 |
| 8 | **T3**, condição de arranque da C3 | adversário da C2 | **nunca correu e nunca foi registado**; três camadas construíram por cima | a C4 |
| 9 | a série Landsat devia entrar na lista fechada (W1) | adversário da adenda | **não entrou**; continua fora na C5 | a C4 |
| 10 | permutação de V3 sobre os 56 mosaicos | R2 de um adversário | **entregue à C4 e não transportada por ela** | **este documento** |
| 11 | correcção de âmbito atribuída à adenda de LiDAR (W8), que a adenda não contém | — | conduz uma linha CONFIRMADO e o `c3_11` inteiro | adversário da C3 |
| 12 | o prompt da C4 foi escrito e entregue **depois** de a C3 declarar paragem de linha | regra 2 do protocolo | a C3 rejeitou, construiu quatro factos por cima e passou o bastão | adversário da C3 |
| 13 | a adenda de LiDAR não reporta **nenhuma** âncora | Controlo 2 | um documento com lista fechada (L1–L8) que alimentou a C4 sem nenhum controlo 2 | adversário da adenda |
| 14 | três raios de disco (70/90/120 m) | — | nunca declarado como divergência até ao adversário da adenda | adversário da adenda / C4 |
| 15 | secção C de `c2_05_manchas.py` corre, dá nulo, e não aparece em nenhuma das cinco secções do certificado da C2 | regra 4 do protocolo | resultado desaparecido | adversário da C2 |
| 16 | a resolução da C2 sobre o NDVI da referência («são objectos diferentes») | certificado da C2 | perdida pela C3 e pela C4, que a reabrem como divergência com um terceiro par | **este documento** |

**Dezasseis instâncias contra um caso limpo, ao longo de cinco camadas, quatro
adversários e duas rondas de multiverso.**

**E o padrão dentro do padrão, que é o que interessa:** contando quem apanhou
cada uma — **quinze das dezasseis foram apanhadas por um adversário ou pela
camada seguinte a ler ficheiros que não eram os do seu prompt. Nenhuma foi
apanhada pela camada que a recebeu, a ler o seu próprio prompt.** Não pode ser,
porque o prompt não contém a informação.

**A causa é o `PROTOCOLO.md`, regra 1, e está escrita em letra de forma:**

> «Cada sessão recebe: o certificado de todas as camadas abaixo, e os dados
> brutos da sua própria camada. **Mais nada.**»

**Os documentos `*_ADVERSARIO.md` não são certificados.** Pela regra 1 da
herança fechada, **as correcções são a única classe de documento da cadeia que
nenhuma camada tem autorização para herdar.** Chegam acima só se a camada
anterior as copiar à mão para dentro do prompt — o que é precisamente o
mecanismo que falhou dez das dezasseis vezes acima.

E o `CAMADA_5_PROMPT.md` reproduz o defeito na íntegra: «**O que herdas — e só
isto:** Seis listas fechadas». Nenhum adversário está na lista. As quatro
correcções que lá aparecem estão numa caixa manual à cabeça, escritas pela C4,
**e ela própria falhou uma (a permutação de V3)**.

> **A correcção não é analítica e é de uma linha no `PROTOCOLO.md`:**
>
> > «Cada sessão recebe: o certificado de todas as camadas abaixo, **os
> > documentos adversariais de todas as camadas abaixo, que ganham ao
> > certificado que atacam**, e os dados brutos da sua própria camada.»
>
> **Esta é a alteração de maior valor que este documento produz**, e vale mais
> do que todas as retiradas das Partes 1 e 2 somadas — porque essas corrigem
> factos e esta corrige o mecanismo que os corrompe.

---

# PARTE 5 · A PERGUNTA QUE FALTA

Faço três candidatas e escolho uma.

**Candidata A — «e se o vazio de que o gestor fala não for este vazio?»** É boa,
é o R2, e fecha-se com uma pergunta ao gestor.

**Candidata B — «quanto do padrão é do pomar e quanto é da paisagem?»** É a NT
13 e a REG-03. A camada já a fez e não a resolveu; não é uma pergunta que falta,
é uma que está registada.

**A que escolho, porque é a que ninguém em cinco camadas fez:**

> ## «Qual é o nível normal disto?»
>
> Toda a cadeia mede **contrastes internos**: foco contra referência, v8 contra
> v13, novo contra antigo, 2026 contra 2017. **Não existe um único número neste
> caso que diga o que é normal para um kiwi adulto em Entre Douro e Minho.**

Isto atravessa tudo e ninguém lhe tocou:

- **Na biologia.** *Fusarium oxysporum*, *F. solani*, *Ceratobasidium*,
  *Neofusicoccum parvum* são organismos **comuns em solo e madeira de pomar**.
  A linha BIO-17 quase lá chega — «sem controlo externo não há nível de
  referência para nenhuma destas contagens» — e depois aplica-o **só ao
  *M. hapla***. As nove presenças de D7 têm exactamente o mesmo problema: **não
  se sabe se são achado ou fundo.** A pergunta que falta não é «estão só aqui?»
  (NT 4). É **«que fracção dos pomares de kiwi saudáveis da região dá positivo a
  estes nove organismos?»** — e essa não se responde com um segundo ponto neste
  pomar. Responde-se com literatura, ou com um prevalência de laboratório, e
  **custa uma pergunta ao Areeiro, não uma campanha.**
- **No sinal.** A G26 diz que não há controlo de kiwi contemporâneo neste
  aluvião. Mas «qual é a trajectória de NDVI normal de um kiwi de vinte anos com
  pérgola» é uma pergunta de **literatura e de parcelário**, não de varrimento
  espacial, e nunca foi feita. A H2-4 tropeçou num candidato a 8,1 km por
  acaso.
- **No cálcio.** ABI-11 declara «Baixo» segundo uma referência de 3–4,7 % —
  **essa é a única vez em toda a cadeia em que um número é comparado com um
  padrão externo em vez de com outra parte da mesma parcela.** E é, por isso, a
  metade da linha que aguenta.

**Porque é que ninguém a fez:** porque a arquitectura da cadeia proíbe. Cada
camada só pode usar o que a de baixo certificou, e **nenhuma camada tem
autorização para ir buscar um valor de fora do caso**. O `CONTROLOS.md` mandou
institucionalizar «ir a um instrumento diferente» e a cadeia cumpriu-o **dentro
do caso** — ortofoto, SAR, LiDAR, laboratório. **Nunca saiu do caso.** A regra
que apanhou o «B1» — abrir a imagem RGB — foi a regra de ir ver **fora**, e é
a que a herança fechada tornou impossível.

**O que isto faz ao produto principal.** As 41 NÃO TESTADAS estão ordenadas,
implicitamente, por «o que falta ensaiar aqui». Ordenadas por **«o que
distinguiria este pomar de um pomar normal»**, a lista fica diferente: BIO-24
(PSA) sobe, porque tem prevalência regional conhecida; as nove de BIO-01..09
descem, porque um segundo ponto neste pomar não diz se são fundo; e REG-01 passa
a ser a primeira, que é o que a própria C4 escreve em §7 e não reflecte no
livro.

---

# PARTE 6 · OS CINCO TESTES DE CINCO MINUTOS

Ordenados por confiança ganha por esforço. **Nenhum é análise nova; três são
leituras de ficheiros que já estão em disco.**

**1 · Ler o campo `linhas_com_lugar_mas_sem_par_de_comparacao` do
`c4_01_numeros.json` e corrigir o «13» em cinco sítios do certificado e três do
prompt da C5.** *(dois minutos)* Resolve R1. É o número mais citado da camada e
o seu próprio ficheiro de prova dá outro.

**2 · Perguntar ao gestor duas coisas: «o vazio que descreveu já era o maior em
Junho de 2025?» e «consegue apontá-lo numa ortofoto?».** *(uma pergunta)*
Resolve R2, que é a retirada mais grave. Sem isto, uma geometria de 2026 está a
localizar uma colheita de 2025 e nove linhas do livro-razão trazem no seu campo
`ambito` uma distância que não mede o que diz medir.

**3 · Correr `datacao_focos` a 90 m em vez de 120 m.** *(duas linhas, sobre
ficheiros em disco — a própria camada di-lo em §9.3 e escolheu não o fazer)*
O 3,5 % contra 52,4 % é uma das três colunas de D1 e corre num raio que a maior
parte da cadeia não usa. Enquanto isso não correr, D1 tem uma coluna cujo
objecto é diferente do das outras duas.

**4 · Medir o desvio-padrão e a assimetria das células fora do pomar nas duas
cenas S2C.** *(três linhas, ficheiros em disco — a própria camada di-lo em NT
14 e em INS-06)* **Todas** as grandezas-título desta cadeia são estatísticas de
cauda e o único controlo instrumental existente corre sobre a média. É o teste
com maior raio de explosão dos cinco: se a cauda se alargar, o défice de 2026, a
regra M2, a dispersão e as 2,60/3,58 ha movem-se todos ao mesmo tempo.

**5 · Acrescentar duas colunas ao `c4_razao_exclusoes.csv`: `n` e
`procurado_onde`.** *(uma passagem pelo CSV)* Resolve R5, R9, R10 e 3.2 de uma
vez, e é a única coisa que impede a C5 de ler «41 causas que ninguém procurou»
sobre nove positivos de laboratório.

*(Um sexto, fora da conta porque não é de cinco minutos e é o mais valioso de
todos: **certificar a série Landsat**. É o único instrumento externo do caso,
está em disco, foi pedido por um adversário há duas camadas, e é exactamente o
que falta para certificar D4 e a componente (b) de I7. Enquanto não entrar, a
camada mais forte da C4 apoia-se na camada menos certificada dela.)*

---

# PARTE 7 · VEREDICTO

## O certificado

**Segue para cima com as retiradas e as margens acima.** Não volta à camada de
origem: não encontrei nenhum facto certificado abaixo que a C4 tenha aceite
indevidamente, nem nenhuma paragem de linha por declarar. O que encontrei foi
**apresentação a exceder a medição**, e a camada avisou-me de quatro dos sítios
onde isso aconteceria — acertou em três (§9.1 o D7, §9.3 os 120 m, §9.5 a
correcção aceite sem atacar) e falhou em dizer onde estava o quarto.

**Obrigatório antes de a C5 tocar no material:**

| | acção |
|---|---|
| **1** | corrigir o **13 → 10/13 com definição** (R1) |
| **2** | reescrever a localização de D7/I6 **sem o 11,4 m** e com a data da geometria (R2, M6) |
| **3** | corrigir a tabela de §0.4 e a contagem «quatro em NDVI» (R3) |
| **4** | retirar «a única coisa que competia … desapareceu» de I5 e §0.4 (R4) |
| **5** | **D5 perde o verbo «excluído»; BIO-16 passa a INCONCLUSIVA** (R5) |
| **6** | **ABI-08 passa a NÃO TESTADA** (R6) |
| **7** | **INS-02 passa a condicional em G10** (R7) |
| **8** | ABI-04 leva a marca «sem instrumento independente» (R8) |
| **9** | **ABI-11 passa a INCONCLUSIVA**, sobrevive só a perna foliar (R9) |
| **10** | reetiquetar as 41 (3.2) e acrescentar as colunas `n` e `procurado_onde` (R10) |

**Margens a alargar antes de passar:** M1 (duas proveniências, não três), M2 (o
2,60 e a colisão), M3 (2,7× a 4,5×), M4 (média contra mediana), M5 (três pares
para a referência), M6, M7 (a permutação de V3), M8 (2 cm).

**Passa intacto, e digo-o com a mesma clareza:** **D6 e D8.** Verifiquei D6 linha
a linha contra o JSON e contra o código que o produz: as vinte linhas, os cinco
negativos, os quatro que vêm do mesmo granel, o um que só existe em Espanha, a
enumeração dos quinze taxa, a ausência total de bactérias e vírus, e a
verificação de que a classe contrária **é emissível e tem duas ocorrências** —
que é o teste de falsificabilidade que quase nenhuma outra linha desta cadeia
faz. **«A matriz de diagnóstico tem uma coluna» não é exagero. É o achado mais
consequente da camada e passa com o peso todo.** Só o número 13 precisa de
definição ao lado.

E **as quatro EXCLUÍDA-LOCAL** são, na minha leitura, o melhor trabalho técnico
do livro-razão.

## O `CAMADA_5_PROMPT.md`

**NÃO PODE ARRANCAR COMO ESTÁ.** Três defeitos, todos de uma frase:

**1 · «É a lista do que ninguém procurou» (linha 367) e «41 causas que ninguém
procurou» (tarefa 2, linha 558).** Falso para pelo menos dezasseis das
quarenta e uma, e para nove delas o inverso é verdade: foram procuradas e
encontradas. A tarefa 2 e a tarefa 1 do mesmo prompt dão à C5 leituras
incompatíveis das mesmas nove linhas, e a tarefa 2 leva-a a orçamentar primeiros
ensaios onde o que falta é um segundo ponto. **Correcção: reescrever as duas
frases e entregar o CSV reetiquetado.**

**2 · A tabela de nomenclatura, linha 27:**
`| maior vazio circular | centro E530476 N4655046, 3,98 ha | a 11,4 m do centro
do foco OESTE |` — entregue ao lado das coordenadas G34, com o mesmo estatuto, e
sem uma palavra de proveniência. É o núcleo n.º 22 da corrida B, delimitado por
anomalia NDVI/NDMI, com `first = 2026-07-27`, área entre 2,38 e 3,98 ha conforme
a corrida, centro com 30 m de dispersão entre derivações, e a amostra que
localiza é de **2025-06-06**. **A C5 vai tratá-lo como geometria.** É o «B1» com
melhor sorte: desta vez o objecto está no sítio certo, mas foi construído da
mesma maneira e entregue com a mesma confiança. **Correcção: retirar o 11,4 m da
tabela e acrescentar a proveniência e a data do objecto.**

**3 · «13 assentam numa só amostra composta»**, três vezes (268, 549, 659).
**R1.**

**Dois defeitos menores que valem uma linha cada:** a lacuna da permutação de V3
não foi transportada (M7); e o prompt tem dois «41» diferentes a circular — as
41 NÃO TESTADAS e a «subida de 41 para 82 dos Becrop» da linha 495 — numa cadeia
que já pagou três vezes por colisões de número.

**Com essas três frases corrigidas, o prompt arranca.** E é preciso dizer o
resto: é um bom prompt. A tarefa 1 identifica correctamente a restrição que
determina tudo; a tarefa 2 obriga a C5 a declarar o que decide **não** procurar
e a levar isso para o relatório; a tarefa 5 obriga cada ramo do Pilar D a nomear
a linha do livro-razão que o sustenta e o estatuto dela; a tarefa 8 dá-lhe
autorização explícita para não fechar. **A tarefa 5 é a melhor instrução escrita
nesta cadeia** — e é também a razão pela qual os estatutos têm de estar certos
antes de ela correr, porque é ela que os converte em decisões.

## E a recomendação que não é sobre esta camada

**Alterar a regra 1 do `PROTOCOLO.md` para que os documentos adversariais sejam
herdáveis** (transversal E). Dezasseis correcções perdidas contra uma
transportada, ao longo de cinco camadas, não é uma sucessão de descuidos: é o
comportamento previsto de um sistema em que a única classe de documento que
corrige factos é a única classe que a regra de herança exclui.
