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

**Mostra** a exploração inteira — 42,6 ha na partição — sobre o terreno, a
drenagem e o cadastro. Os sectores levam **os nomes do gestor: B1, B2, Erica
Novo, B3, B4.** É a folha em que todas as vistas seguintes assentam.

**Instrumento.** MDT LiDAR de 50 cm da DGT (7 folhas, EPSG:3763, reamostrado a
1 m em UTM 29N); parcelário IFAP 2025, cultura 124 (KIWI); tabela de válvulas e
nomes de sector do gestor; códigos de bloco dos boletins A2.

**Escoamento.** pysheds sobre o MDT de 1 m, com `resolve_flats`. Sem esse passo
a acumulação máxima cai por um factor de 70 neste terreno — 33 % das células
são planas. Desenham-se só os canais (acumulação ≥ 5 ha e ≥ 20 ha), e o leito
do rio é excluído: com limiar baixo a camada pinta 3 % da carta e lê-se como
água parada, que é o contrário do que mede.

**A geografia, que é o essencial.** Os cinco sectores estão todos numa
plataforma aluvial entre **5 e 9 m**, ao longo de 2,4 km da margem esquerda do
Minho. A sudeste o terreno sobe até 155 m; a noroeste está o leito do rio, e
para lá dele acaba a cobertura LiDAR nacional. O **B1 é o sector mais baixo**
(mediana 6,06 m) e fica isolado, cerca de 1 km a sudoeste do resto.

**O rio Minho** é identificado pela mancha contínua abaixo de 2,5 m (59,8 ha na
caixa, centro em 8,634 W / 42,046 N) coincidente com o limite da cobertura
LiDAR nacional a noroeste — dois indicadores de origem diferente. Nenhum deles
sozinho bastaria.

**A partição, e a ressalva que a acompanha.** Cada ponto pertence ao sector da
válvula mais próxima; o B1 é a união das suas seis parcelas do IFAP. As áreas
que a partição dá batem com as declaradas pelo gestor dentro de **17,7 % (B2)**,
com o critério de rejeição fixado em 25 % antes de correr.

**Esse teste é circular, e fica dito.** A reconstrução usada — `por_area` — foi
construída por área acumulada precisamente para bater com as áreas declaradas:
compará-la com elas reproduz a calibração em vez de a verificar. Corridas as
outras três reconstruções pelo mesmo teste, **as três falsificam** (desvios de
82 %, 100 % e 114 %), e as quatro só concordam em **26,1 % da banda**.

**Mas há uma verificação que NÃO é circular, e foi encontrada tarde.** O
cabeçalho do `m1_v8_implantacao.py` regista-a: o gestor nomeou «**Zona 0 =
válvulas 8, 9, 10**», e a colocação por área acumulada põe a válvula 8 a
**34 m** desse ponto — com essa frase fora do cálculo. Contra um espaçamento
entre válvulas de 98 m, é uma âncora de **testemunho directo** a validar, e
distingue a `por_area` das outras três, que falharam por 71 % de escala, 64 m e
321 m respectivamente.

Ou seja: a `por_area` não é apenas «a que passa a sua própria calibração». Ao
nível do sector a partição serve, e tem esse apoio independente; ao nível da
válvula individual continua sem resolução suficiente, e por isso **a carta não
desenha válvula nenhuma** — 34 m de erro numa malha de 98 m chega para o
sector e não chega para a célula.

**Não se conclui daqui** nada sobre o declínio. A carta é sobre estrutura.

---

## P12 · Camada do esquema de rega

**Duas saídas do mesmo desenho:** `P12_camada_rega.png`, de fundo transparente
e registada célula a célula com a P11 — papel vegetal, para sobrepor; e
`P12_camada_rega_isolada.png`, a mesma em papel e com legenda, para se ler
sozinha.

**Mostra** o que o «Esquema de rega retificado» (PRDLUX, Jul-09) fixa, com as
anotações manuscritas do gestor: as 17 válvulas repartidas pelos cinco sectores
dele, a estação de linha de cada grupo, os 13 sectores impressos A–N com o
débito de cada um, e as notas de rede — conduta principal a sair do armazém na
linha 222, linha da bomba 229, condutas de 2,5″/3″/4″/6″, **uma válvula
desactivada na linha 185**, «4 novas válvulas» sem número atribuído, e origem
de água única para toda a exploração.

**A convenção gráfica, que é o que a torna útil.** Traço contínuo e opaco: está
escrito numa fonte — no esquema, no IFAP, ou dito pelo gestor. Traço
interrompido a 55 %: é nosso, inferência ou leitura por confirmar. Metade do que
uma carta destas costuma afirmar não tem fonte, e sem esta distinção o leitor
não sabe qual metade. A prancha traz sete perguntas escritas para levar ao
gestor.

**Porque não há posições de válvula.** Tentou-se georreferenciar o próprio
desenho contra o parcelário do IFAP, com o critério escrito antes de correr —
**RMS < 20 m**, e as 17 válvulas a cair dentro das parcelas. Deu **RMS 70,3 m**
e 3 das 10 manchas detectadas dentro. Falhou, e não se publica posição nenhuma.

**E o desenho explica porque nenhuma reconstrução podia acertar:** há **duas
fiadas de válvulas na mesma estação de linha** — as 10 e 13 de um lado da
conduta, as 11 e 12 do outro, todas anotadas «306 a 307». Qualquer reconstrução
que espalhe as válvulas ao longo de um eixo tem de errar.

**O que o esquema corrige na nossa leitura anterior.** As válvulas 1 a 5 estão
desenhadas **dentro do B1**, com «149 → v1,2,3» e «137 e 156 → v4,5». A
pertença que o gestor afirmou está corroborada pelo desenho; o que estava errado
eram as reconstruções, que as punham 365 a 555 m a oeste. E a numeração de linha
do B1 é própria: as linhas 137 e 156 cairiam dentro do B2 na numeração da banda.

**As etiquetas de sector, e porque só quatro foram lidas.** Estão impressas em
texto vertical de cerca de 1,5 pt no original, dentro de um JPEG digitalizado.
Leram-se **G, F, E e D** — sobre as válvulas 6, 7, 8 e 9 — porque essas quatro
bandas são largas e a etiqueta apanhou pixéis suficientes; isso dá ao **B2** um
débito de **362,4 m³**, o único que se pode somar hoje.

As outras nove letras (A, B, C, H, I, J, L, M, N) cobrem treze válvulas — as 1 a
5 no B1 e as 10 a 17 na banda — e ficam por ler por três razões, todas do
ficheiro e não do método: bandas estreitas de mais para a etiqueta sobreviver à
digitalização, etiquetas tapadas pela caneta das anotações manuscritas, e
compressão JPEG a desfazer o traço. Ampliar mais não acrescenta informação —
os pixéis não existem.

Recortes a 900 dpi das três zonas em falta ficam em
`Downloads/_esquema_rega/decodificar_*.png`, prontos para quem conheça o
terreno os decodificar. **É a pergunta 1 da lista ao gestor.**

**E a cor não resolve o problema — foi testado.** Levantou-se a hipótese de
cada cor impressa corresponder a um sector, o que permitiria ler as etiquetas
todas sem as decifrar. Mediu-se a mediana RGB da trama em torno de cada válvula
com etiqueta conhecida: o **sector F** (válvula 7) e o **sector M** (válvula 16)
têm o **mesmo amarelo, ΔRGB 11,1**, em extremos opostos da folha e sem
ambiguidade de amostragem. A cor é **colorização de mapa** — escolhida para que
bandas vizinhas se distingam — e não uma chave de identidade.

Uma consequência útil fica: **localmente** a cor serve, porque bandas adjacentes
diferem. Ao decifrar um recorte pode contar-se as bandas com segurança; só não
se pode inferir a letra a partir da cor. Medições em
`figuras/base/cor_e_sector.json`.

**O que saiu da prancha em 04-09, e fica aqui.** O registo da P12 com a P11 é ao
**nível do sector**: a georreferenciação do desenho contra o parcelário do IFAP
falhou o critério pré-registado — RMS 70,3 m contra o limite de 20 m, e 3 das 10
manchas detectadas dentro das parcelas — e por isso a camada não traz posição de
válvula nenhuma. As quatro reconstruções discordam entre 92 e 398 m para um
espaçamento entre válvulas de 98 m. Nada disto vai escrito na carta: o traço
interrompido já o diz, e repeti-lo por extenso era anotar na carta do gestor uma
lacuna que é nossa.

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
