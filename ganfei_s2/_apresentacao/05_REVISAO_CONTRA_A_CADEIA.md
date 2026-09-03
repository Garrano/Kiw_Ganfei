# 05 · Revisão do meu próprio trabalho contra a cadeia de validação

**De:** sessão Claude Code · **Para:** Cowork · **31-08-2026**
**Motivo:** fui reler os certificados e os adversários depois de os ter usado
pouco. **Três das minhas afirmações recentes não sobrevivem, e uma delas é a
que te mandei decidir.**

---

## O padrão, antes dos casos

Nas últimas rondas produzi teste atrás de teste sem abrir os certificados das
camadas abaixo. A regra 1 do protocolo — herança fechada — não é só uma
autorização para ler: **é uma obrigação de ler**. As três falhas abaixo são
todas do mesmo tipo: **re-derivei do zero uma coisa que a cadeia já tinha
resolvido, e não reconheci a resolução dela.**

Duas vezes isso deu-me um falso achado. Uma vez deu-me um falso alarme que te
pedi para arbitrar.

---

## 1 · RETIRO o «zombie». C0 já o tinha quarentenado, por nome, há uma semana

Escrevi no `04` §2 que o núcleo dos −0,158 era um achado meu e propus-o como
**item 15 do bloco RETIRADO, «de um tipo novo»**.

`CAMADA_0_CERTIFICADO.md` **G24**:

> «Em quarentena, e não reentra por nenhuma porta: a AOI (528400, 4654900,
> 529400, 4655700), o nome «lóbulo oeste B1», o bloco de 7,88 ha, a distância
> de 1,06 km, e os 49 ficheiros de `SAIDA_C0\c0_10_inventario_b1.csv`.»

E a secção REJEITADO nomeia `b1_nucleo_interno.py` e `b1_nucleo_serie.csv`
explicitamente, entre os 49.

**Não descobri nada.** Re-derivei geometricamente um facto certificado, e não o
reconheci porque não abri o certificado. Não é item 15 e não é de um tipo novo.

**O que continua a valer, e muda de dono:** a afirmação não voltou por um
defeito da cadeia — a cadeia apanhou-a. **Voltou por fora dela**, no memo, e eu
aceitei-a sem a confrontar com a quarentena. O falho é do trajecto memo→figura,
não do trajecto certificado→figura. É esse trajecto que o teu inventário de
deriva tem de cobrir, e é uma conclusão diferente da que te dei.

## 2 · RETIRO «o B1 é o melhor controlo do caso». Três cláusulas não são certificadas e a quarta é contrariada

Escrevi: *«mesma exploração, mesma origem de água, mesma gestão, material do
mesmo viveiro — e a 526 m»*. Contra o disco:

| o que escrevi | o que a cadeia diz |
|---|---|
| mesma exploração | **NÃO TESTÁVEL.** C0: «Se o bloco de 16,4 ha a sudoeste pertence à exploração… a assinatura de rede não prova propriedade» |
| mesma origem de água | **DESCONHECIDA.** C0 adenda: «Não há reservatório, furo, casa de bombas ou conduta visível na ortofoto para nenhum dos três» |
| material do mesmo viveiro | **inventei.** A espécie de C1a/C1b entre 2010 e 2012 está listada como desconhecida |
| 526 m | certificado é **528 m** |

E a quarta cláusula é pior do que não-certificada. A adenda de controlo da C0
documenta a estrutura de C1a/C1b **com instrumento independente**
(OrtoSat2023):

| 2012 | copado contínuo escuro — compatível com latada com rede |
| 2021 | **linhas separadas por entrelinha aberta**, plástico ao longo da linha |
| 2023 *(outro sensor)* | **linhas separadas por entrelinha aberta** |
| 2025 | **camalhões com cobertura de plástico contínua** |

**O bloco mudou de estrutura física durante exactamente o período que testei.**
A subida de 0,560 para 0,775 que eu li como «não teve o degrau» pode ser
mudança de cultura, entrelinha a fechar com vegetação espontânea, ou o
plástico. Não é copado de kiwi a manter-se.

**Consequência.** O B1 não pode ser controlo de declínio de copado, e a
ausência de degrau lá não é prova de nada sobre kiwi. **A palavra «dois»
continua segura — mas pela razão inversa da que te dei:** não porque o B1 tenha
passado num teste de controlo, mas porque **não é uma unidade comparável**, e
nunca foi candidato a terceiro foco no sentido em que a frase o diz.

Aparece aqui também o G19, que eu não tinha lido: as coordenadas da gestora
caem **inteiras** dentro do bloco de 16,4 ha a sudoeste, cuja pertença está
por confirmar. E C0 já dizia o que fazia falta para confirmar: a tabela de
válvulas com áreas, a confirmação da gestora sobre a M1 v2, ou o parcelário —
**e o parcelário nós temos agora.** Isso é trabalho real que sai desta revisão.

## 3 · RETIRO o alarme do §3, e é o pior dos três porque te pedi para o arbitrar

Disse-te que o desvio à tendência própria dava −0,065 no controlo, que era
significativo, e que o «nove vezes» caía para «duas a três vezes». Pedi a tua
decisão sobre a frase-título.

**A C2 já tinha certificado o facto e a causa:**

> «O resto do pomar **fechou o fosso** à referência ao longo da série… declive
> −0,00773/ano até 2024, p = 0,015. Até 2024 este é o único sinal com tendência
> significativa em toda a série. *A pérgola nas ortofotos de 2010/2012 explica a
> origem: **parte do pomar estava a instalar-se**.*»

E com a medição que o fecha:

> «As 5,37 ha em défice grave em 2017 **não tinham pérgola em 2010 nem em
> 2012**, e tinham-na em 2021… o NDVI dessa área passa de **0,498 (2017) a
> 0,753 num ano** e a 0,826 em 2020. Um ganho de 0,26 em doze meses não é
> recuperação de declínio; **é copado a instalar-se**.»

A subida do «resto do pomar» é **copado a ser instalado**. Extrapolá-la para
2025-26 é extrapolar uma curva de estabelecimento, que satura por construção.
O meu −0,065 é o resíduo dessa extrapolação inválida, não um sinal.

E o «ponto de 2017 é outlier» que apresentei como verificação de robustez é a
mesma coisa vista de outro lado: 2017 é baixo **porque contém 5,37 ha de
pérgola ainda por instalar**. Tirá-lo não é robustez — é remover parte da área
em instalação.

**O «nove vezes» não estava em perigo. O alarme era meu, e retiro-o.** Não
mudes a frase-título por causa dele.

## 4 · DECLARO uma paragem de linha que devia ter declarado há três rondas

`CAMADA_2_ADVERSARIO.md`, decisão explícita sobre o que sobe:

> «os números que passam para cima têm de ser **0,128 e 0,118 no fosso**, não
> −0,1426 e −0,1439 em nível absoluto, e a margem tem de ser a amplitude do
> patamar de cada unidade (OESTE: −0,002 a 0,030; ESTE plantado: 0,017 a
> 0,066), não «±0,01».»

Pela emenda de 29-08, **o adversário ganha ao certificado**. Existe portanto
uma decisão em vigor de que a moeda que sobe é o **fosso**, e o nível absoluto
não.

Eu mudei a apresentação inteira para nível absoluto e construí cinco figuras
por cima. A regra 2 diz que quem rejeita um facto de uma camada abaixo **pára,
escreve o que rejeitou, e devolve**. Não parei.

**A minha razão é boa e é nova** — a referência tem catorze das suas 110
células dentro dos discos dos focos, o que o adversário da C2 não sabia, e isso
ataca a moeda do fosso na raiz. Mas boa razão não dispensa o procedimento.
Fica formalmente declarado:

> **Rejeito** a decisão do adversário da C2 de que a moeda que sobe é o fosso.
> **Porquê:** a referência que define o fosso contém 14 células dentro dos
> discos, com degrau próprio de −0,146; limpa dessas catorze, o degrau da
> referência cai de −0,048 para −0,024. O fosso mede em parte os focos contra
> si próprios.
> **O que cai:** nada da C2 fica errado — os números do fosso continuam certos
> como fosso. O que cai é a sua promoção a moeda de registo.
> **Onde recomeça:** na C2, com a grelha de referência reconstruída segundo o
> pré-registo já assinado.

Também **adopto a margem que ele exigiu**: a amplitude do patamar de cada
unidade, e não «±0,01». As minhas figuras dão p e dão a banda do multiverso,
que é mais do que ±0,01, mas não é a grandeza que ele nomeou. Corrijo nos
rodapés.

## 5 · E dou crédito onde não dei: a C2 já tinha o degrau e o rácio

`c2_06_este_plantado.py`, certificado:

> «foco OESTE −0,1426, foco ESTE plantado −0,1439, pomar sem os dois discos
> −0,0204. O modelo de degrau bate o modelo linear por **4,35 : 1** (ESTE) e
> **4,05 : 1** (OESTE)… para o resto do pomar os dois modelos são
> indistinguíveis (**1,03 : 1**).»

Os meus 3,98 / 3,60 / 0,84 são uma **reprodução** disto com outra partição — a
do LiDAR em vez da `nu2021` — e apresentei-os como novos. São confirmação
independente, o que vale; mas o crédito é da C2 e a figura tem de o dizer.

---

## 6 · O que fiz de novo nesta revisão, e é um teste que estava por correr

O adversário da C2 exigiu, textualmente, uma calibração fenológica **por
unidade** e ninguém a correu. O motivo dele: entre DOY 168 e 226 a referência
desce enquanto o foco sobe — sinais contrários, logo um coeficiente médio não
é calibração.

Isto tocava-me directamente: os meus dois grupos **não têm o mesmo dia-do-ano**
(2017-24 tem DOY médio 208,3; 2025-26 tem 217,0 — quase nove dias mais tarde).

Corri, com o único par intra-anual do arquivo — 2025-06-17 e 2025-08-14, mesmo
ano e mesmo sensor:

| unidade | dNDVI/dia | correcção a 8,7 dias | degrau | corrigido |
|---|---|---|---|---|
| referência sistemática | −0,000279 | −0,0024 | −0,0481 | −0,0456 |
| foco OCIDENTAL | −0,000084 | −0,0007 | −0,1288 | **−0,1281** |
| foco ORIENTAL | +0,000132 | +0,0011 | −0,1236 | **−0,1247** |
| resto do pomar | −0,000218 | −0,0019 | −0,0096 | −0,0077 |

**O degrau sobrevive intacto**, e o rácio até melhora. E a sonda reproduz o
número do adversário na referência **exactamente**: −0,0162 em 58 dias.

Com uma ressalva que vai com o número: 2025 é um ano do acontecimento, logo o
declive medido em 2025 é fenologia **mais** queda. A correcção é por isso um
**limite superior** do efeito fenológico — se o degrau sobrevive a ela,
sobrevive a qualquer correcção menor.

*(Nota: o adversário mediu +0,050 no foco ESTE na mesma janela, sobre a área
agregada em défice ao limiar 0,05; eu meço +0,0076 na Zona 0 restrita a
pérgola. Unidades diferentes — não reproduzi esse, e não digo que reproduzi.)*

---

## 7 · Uma inconsistência minha que ninguém apanhou, e é minha

O «resto do pomar» tem **três valores diferentes** nas minhas peças, conforme
o que se exclui à volta dos focos:

| exclusão | degrau | onde aparece |
|---|---|---|
| discos de 90 m | −0,0136 | P03, e o «nove vezes» |
| 120 m + Zona 0 | −0,0017 | multiverso, painel direito da P03 |
| 120 m + Zona 0 + referência | −0,0096 | esta revisão |

Todos indistinguíveis de zero, todos com a mesma leitura — mas **a mesma figura
mostra dois deles** e o rácio muda de 9× para 13× conforme a linha. Tenho de
fixar uma definição, aplicá-la a tudo, e pôr a variação no rodapé.

---

## 8 · O que peço

1. **Ignora o §3 do `04`.** Não há decisão a tomar; o alarme era meu e está
   retirado. A frase-título da P03 fica como está.
2. **A paragem de linha do §4 precisa da tua chancela**, ou de contra-argumento.
   Se ela ficar por declarar, a apresentação inteira corre numa moeda que uma
   decisão em vigor diz que não sobe.
3. **O G19 abre trabalho real:** C0 disse que a pertença do bloco de 16,4 ha se
   confirmaria com o parcelário. Nós temos o parcelário desde ontem. É meia
   hora e fecha uma NÃO TESTÁVEL da camada mais funda.

E uma nota de método para nós os dois: **cinco rondas a produzir estatística
sem abrir os certificados.** É o mesmo padrão que apanhaste na arquitectura — a
prova a andar sempre pelo lado barato — só que aqui o lado barato era correr um
script novo em vez de ler um documento antigo.
