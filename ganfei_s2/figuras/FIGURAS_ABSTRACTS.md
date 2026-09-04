# Resumos das peças

Uma entrada por figura: **o que mostra · com que instrumento · o que não se pode
concluir dela.** As pranchas não levam interpretação escrita; a interpretação
está aqui.

Ordem de leitura para quem chega agora: **P11** (onde é), **P01** (o caso),
**P02/P03** (o que aconteceu), **P04/P04a/P04b** (que não fomos nós a escolher),
**P05** (ver com os olhos), **P10** (a estrutura), **P06/P07** (o que falta),
**P08** (o que fazer em Setembro).

---

## P11 · Carta-base de Ganfei

**Mostra** a exploração inteira — 42,6 ha em cinco sectores — sobre o terreno,
a drenagem e o cadastro. Os sectores levam **os nomes do gestor: B1, B2, Erica
Novo, B3, B4.** É a folha em que todas as vistas seguintes assentam: esquema de
rega, tipo de solo, porta-enxertos, datas de plantação, manchas de mortalidade.

**Instrumento.** MDT LiDAR de 50 cm da DGT (7 folhas, EPSG:3763, reamostrado a
1 m em UTM 29N); parcelário IFAP 2025, cultura 124 (KIWI); tabela de válvulas e
nomes de sector do gestor; códigos de bloco dos boletins A2. Escoamento por
pysheds com `resolve_flats` — sem esse passo a acumulação máxima cai por um
factor de 70 neste terreno.

**A geografia, que é o essencial.** Os cinco sectores estão todos numa
plataforma aluvial entre **5 e 9 m**, ao longo de 2,4 km da margem esquerda do
Minho. A sudeste o terreno sobe até 155 m; a noroeste está o leito do rio. O
B1 é o sector **mais baixo** (mediana 6,06 m) e fica isolado, cerca de 1 km a
sudoeste do resto.

**Ressalvas, e são três.**
1. A **partição por válvula** é inferida, não cadastral: cada ponto pertence ao
   sector da válvula mais próxima. Foi testada contra as áreas que o gestor
   declara — desvio máximo 17,7 % (B2), com o critério de rejeição fixado em
   25 % **antes** de correr. O B1 é excepção: é a união das suas seis parcelas
   do IFAP e bate a 0,1 %.
2. **As válvulas 1 a 5 não estão desenhadas.** O gestor diz que o B1 são as
   válvulas 1–5; a reconstrução do esquema de rega põe-nas 365 a 555 m a oeste
   das parcelas do B1. A reconstrução não alcança o lobo oeste, e desenhá-las
   seria pôr na carta-base uma posição que o processo sabe estar errada.
3. O **rio Minho** é identificado pela mancha contínua abaixo de 2,5 m (59,8 ha
   na caixa) coincidente com o limite da cobertura LiDAR nacional a noroeste —
   dois indicadores de origem diferente. Nenhum deles sozinho bastaria.

**Não se conclui daqui** nada sobre o declínio. A carta é sobre estrutura; o
acontecimento entra nas peças que assentam nela.

---

## P01 · O caso numa página

**Mostra** o caso reduzido ao que se lê de certeza. O texto deriva da adenda
v1.4 §3 e **quatro afirmações dela foram corrigidas** contra o registo executável
antes de serem desenhadas — entre elas o «zero análises de doença», que é falso
(o D2 certifica quatro unidades colocadas, todas positivas a *M. hapla*). O zero
verdadeiro é outro: **nenhuma das doze amostras com posição é anterior ao
acontecimento** (D5).

**Não se conclui daqui** nenhum número novo; é uma síntese de factos
certificados noutras peças.

---

## P02 · Os dois focos não são a mesma coisa

**Mostra** que os «dois focos de declínio» tratados durante semanas como uma
coisa só são geometricamente diferentes: num há pérgola e videira viva, no outro
metade é chão.

**Instrumento** independente de todo o resto do dossiê: **MDS menos MDT** do voo
LiDAR da DGT de 06-07-2025. Mede geometria, não reflectância — tudo o resto mede
reflectância. Rampa sequencial de uma só cor, uma só grandeza (altura de copado).

**Não se conclui daqui** a causa da diferença, nem quando ela apareceu: é uma
única data.

---

## P03 · O degrau em nível absoluto

**A peça central.** Fecha por construção — não por argumento — a classe inteira
de ataques por circularidade: a grandeza é o **nível absoluto** de NDVI (não há
referência para contaminar), a partição planta/chão vem do LiDAR (outro
instrumento), as fronteiras são geográficas e de ficheiro anterior à análise, e
o **controlo** — o resto do pomar, nas mesmas cenas e no mesmo pipeline — está
desenhado ao lado, não escondido no rodapé.

**Não se conclui daqui** a causa. Um degrau em nível absoluto diz que
aconteceu, não porquê.

---

## P04 · Nada disto foi escolhido por nós

**Mostra** a fusão de duas provas com a mesma mensagem: uma **fronteira** que
outra entidade desenhou para pagamentos da PAC, anos antes, e um **instrumento**
de outra agência. Duas maneiras de tirar a nossa mão do resultado.

**P04a — as parcelas do IFAP.** Todas as outras unidades do dossiê têm uma
fronteira que alguém aqui desenhou. Estas não: são verificáveis por terceiros no
parcelário que a própria CCDR-N tem. A única escolha que sobra é *qual* parcela,
e essa é feita pela geografia — a que contém o ponto — não pelo valor.

**P04b — catorze anos de Landsat.** Responde à primeira pergunta de um revisor
hostil, que não é sobre estatística: *«isto é o vosso processamento ou é o
campo?»* USGS/NASA em vez de ESA, OLI em vez de MSI, LaSRC em vez de Sen2Cor,
outra órbita, outra hora de passagem. Partilha com o Sentinel-2 apenas o
princípio físico.

**Não se conclui daqui** que os dois instrumentos sejam independentes em tudo:
partilham o princípio físico, e por isso confirmam a **datação e o sentido**, não
a magnitude.

---

## P05 · Nove verões, a mesma escala

**Mostra** sem números o que a P03 prova com números, e mostra uma coisa que uma
série temporal não pode mostrar: **onde**. Uma só rampa, uma só barra de cor, os
mesmos limites nos nove mapas. É o único argumento da apresentação que não
depende de aceitar um método.

**Não se conclui daqui** magnitude: a leitura é visual e a escala é comum de
propósito.

---

## P10 · O mapa de Braudel

**Mostra** que a ordenação por cota e a ordenação por desfecho **não coincidem
em ponto nenhum**: foco oriental 7,84 m, resto do pomar 6,98 m, referência
6,80 m, foco ocidental 6,64 m, e o B1 a 6,06 m — o mais baixo, e o único que
sobe.

**É uma observação, não um silogismo.** Substitui a primeira versão desta peça,
que argumentava «posições opostas ⇒ a causa não vem da posição» — inferência
frágil, porque um lençol freático ou um agente que se propague por raiz não
precisam de tratar o alto e o baixo de forma diferente.

**Três afirmações desta peça já foram falsas** e estão listadas no seu próprio
cabeçalho, incluindo «B1: sem cota, sem dreno, sem declive» — que era falso
desde 29-08, e cuja correcção foi anunciada por um `print` cuja substituição
falhou em silêncio.

---

## P06 · O que já não é, o que está confundido, o que falta saber

**Mostra** três estados, e uma quarta coluna com **vinte e uma retiradas**. O
porta-enxerto sai de «fechado» para **testado e confundido**: entre blocos as
trajectórias diferem e o radar confirma em duas órbitas, mas a janela não isola
a raiz — os dois braços diferem na raiz *e* nos anos desde a enxertia, e o
segundo domina.

**Não se conclui daqui** que o porta-enxerto não conte. Conclui-se que o desenho
actual não o consegue separar.

---

## P07 · A matriz de diagnóstico tem uma coluna

**Mostra** que quase tudo o que se poderia ter testado não foi testado. Uma
afirmação da versão anterior **não passou a pré-voo**: dizer que a PSA «nunca foi
procurada» descreve um esquecimento, e não foi um esquecimento — **testemunho de
tipo 1**, recebido a 01-09-2026: ninguém encomendou ensaio para PSA porque a
sintomatologia não era compatível. Testemunho directo entra como dado e ganha ao
cálculo; o que ele derruba retira-se, não se reconcilia.

---

## P08 · O plano de Setembro

**Mostra** onde ir, o que colher, e o que cada ponto decide. Uma linha da versão
anterior não passou: a pergunta regional estava listada como condição de
arranque e **está fechada desde 01-09-2026** — e fechou duas vezes, a segunda
invertida, quando a ortofoto mostrou que cinco dos blocos comparados tinham sido
desmatados em 2024.

**Estado final**, com 29 blocos de linha de base contínua: os dois focos são o
pior e o segundo pior da região — **mas só em 4 de 8 agregações defensáveis**, e
a margem mediana é −0,0003. Vai com o intervalo, porque sem ele não é um facto.
