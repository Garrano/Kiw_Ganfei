# Gestão ou fisiologia — o teste, e o que dele fica

29-08-2026.

## Porque se fez

Três linhas independentes convergiram na mesma lacuna no mesmo dia:

1. **O gestor:** «poda ou arranque de linhas podem ser verificáveis com imagens
   em datas próximas».
2. **O analista independente A**, ao declarar o que não conseguiu determinar:
   não há uma única observação de terreno, e poda ou arranque dariam
   exactamente o mesmo sinal que doença.
3. **O adversário da C2:** a camada perguntou «aquilo era pomar?» ao ramo
   descendente e nunca ao ramo **ascendente**. Faltavam duas linhas para saber
   se as 3,58 ha de declínio novo ainda têm fileiras.

É a distinção entre **fiabilidade** e **validade** que este projecto tem por
regra: medimos com estabilidade, nunca estabelecemos que o que medimos é
doença.

## O que se retira

**O teste de prominência 2021→2025 fica retirado.** Foi mal desenhado.

A prominência da autocorrelação radial mede periodicidade e é imune ao
equilíbrio de um JPEG — foi por isso que a escolhi, e a C2 tinha razão nesse
ponto. Mas **não é imune a material novo no chão**. A ortofoto de 2025 mostra
o pomar inteiro coberto por faixas brancas reflectoras ao longo de todas as
fileiras; a de 2021 não as tem. A prominência sobe sete vezes em toda a
imagem, referência incluída. Isso não é deriva de captação: é o material.

Duas correcções encadeadas, ambas registadas porque ambas ensinam:

- A primeira passagem corrigiu a diferença entre imagens **subtraindo uma
  constante**. A relação não é aditiva — a referência passa de 0,0449 para
  0,3293, um factor de sete. A calibração contra solo nu denunciou-o ao
  devolver «−137 % acima do chão», valor impossível. **Foi a calibração que
  apanhou o erro, não a estatística.**
- A segunda passagem, por posto percentual, é invariante a transformação
  monótona e por isso sobrevive a esse erro — mas não sobrevive ao anterior:
  se o material branco entra em datas diferentes em sítios diferentes, o posto
  mede a instalação do material.

**Regra que daqui sai, para juntar às de higiene:** uma medida de estrutura é
imune à radiometria, **não é imune a estrutura nova**. Antes de comparar
estrutura entre épocas, olhar para as duas imagens.

## O que fica de pé

**Arranque de linhas fica excluído por observação directa.** Na ortofoto de
2025 a 25 cm, as fileiras estão todas presentes, contínuas e ao compasso em
todo o pomar, dentro dos dois focos inclusive. Não há quarteirão arrancado,
rectângulo lavrado nem falha no compasso. É observação visual em imagem de
alta resolução — instrumento independente de qualquer índice.

**As faixas brancas não explicam o sinal do Sentinel-2.** O analista C tratou-as
como hipótese primária de artefacto e rejeitou-a por dois caminhos:

- brilho do bloco em época de dormência (Dez–Fev, 71 cenas): **sem degrau**;
- assinatura espectral 2024→2026: azul **+1,4 %**, verde **+0,6 %** (ambos não
  significativos), NIR **−13,8 %**. Uma cobertura branca sobe o azul e o
  verde. O que se observa é perda de área foliar.

## O que fica em aberto

**Poda.** Só a série densa intra-estação a separa de fisiologia, e por isso é
que ela é o teste que interessa: com intervalo mediano de 2 a 3 dias, uma
queda abrupta seguida de recuperação é poda, uma queda que não recupera é
arranque, e um declive sem descontinuidade é fisiológico. Corre em
`serie_densa_descontinuidades.py`.

**Pergunta nova para o gestor, que não é nossa e não conseguimos datar:** que
material branco é aquele ao longo das fileiras na ortofoto de 2025, e quando
foi instalado? Se é recente, é uma alteração de gestão dentro da janela em
análise, e nenhuma das nossas séries a conhece.

## Ficheiros

```
fileiras_2021_2025.py   teste retirado — mantido pelo registo do erro
calibrar_nu.py          a calibração que apanhou o erro aditivo
postos.py               versão por posto; retirada pela razão acima
recortes.py             janelas de 80 m nos quatro alvos, 2021 e 2025
vista_larga.py          420 m, as duas épocas — é aqui que se vê o material
```

---

# O LiDAR — 6 de Julho de 2025

Acrescentado no mesmo dia, depois de o gestor propor «ou talvez LiDAR de
superfície?». Foi a melhor proposta da sessão.

## Porque este instrumento é diferente de todos os outros

Tudo o que este caso usou até aqui mede **reflectância**: NDVI, NDRE, ortofoto,
periodicidade, e até o radar, que mede retrodifusão. O LiDAR mede **geometria**.
É a primeira vez neste caso que existe um instrumento verdadeiramente
independente, e a regra do projecto — nenhum facto passa adiante verificado só
pelo instrumento que o produziu — pôde finalmente ser cumprida.

## Proveniência e data

Centro de Dados da DGT, autenticado com a conta do utilizador em 29-08-2026.
21 folhas MDS-50cm e 2 nuvens LAZ (LO-158565, LO-159565), 586 MB.

**A data do voo veio do tempo GPS dos pontos, não dos metadados.** O registo do
Lote I dá uma janela de catorze meses (12-05-2024 a 23-07-2025), inútil. Os
pontos dão o dia:

> **6 de Julho de 2025, das 14h34m53s às 14h51m08s UTC.** As duas folhas, na
> mesma passagem. LAS 1.4, 16,6 e 17,8 milhões de pontos.

Isso põe o voo **onze meses depois** do evento que o analista B data entre 22
de Julho e 9 de Agosto de 2024, e **em plena folha**. A leitura deixa de ser
condicional.

Classificação das nuvens, classe 5 «vegetação alta acima de 2 m»: **46,6 %** na
folha do foco OESTE, **27,3 %** na folha do foco ESTE.

## A medição

`MDS − MDT`, reamostrado para a grelha de 10 m. A grandeza é a fracção de
píxeis de 50 cm acima de 1,5 m — abaixo da pérgola de kiwi (1,8 a 2 m) e acima
de qualquer coberto herbáceo.

| unidade | altura mediana | % acima de 1,5 m |
|---|---|---|
| referência sistemática | 2,34 m | 99,2 % |
| resto do pomar | 2,32 m | 99,2 % |
| foco OESTE da cadeia | 2,25 m | 90,2 % |
| declínio NOVO de 2026 | 2,17 m | 79,9 % |
| N1 do analista B (oeste) | 2,17 m | 72,9 % |
| N2 do analista B (leste) | 1,86 m | 55,0 % |
| **foco ESTE da cadeia** | **0,47 m** | **35,0 %** |
| **N3 do analista B (leste)** | **0,27 m** | **30,2 %** |
| *nu2021, lavrado em 2021* | *0,09 m* | *15,2 %* |

## O que fica estabelecido

**O foco OESTE é pomar vivo.** 2,25 m de pérgola, 90,2 % de cobertura, só
12,1 % das células abaixo de meio metro. Há videira, e ela está a definhar —
não foi arrancada. É aqui que estão as amostras de ITS e o «Kiwi 1000».

**Metade do foco ESTE não tem pérgola nenhuma.** 0,47 m de altura mediana e
**50,2 % das células abaixo de 0,5 m**, contra 15,2 % no terreno que sabemos
lavrado. O N3 chega a 0,27 m. Em 6 de Julho de 2025 aquilo era chão.

**As 3,58 ha de «declínio novo» de 2026 tinham pérgola completa em Julho de
2025** — 2,17 m e 79,9 %. É a resposta à pergunta que o adversário da C2 disse
que ninguém tinha feito ao ramo ascendente: não é terreno arrancado.

**Do pomar inteiro, 3,77 ha de 30,31 (12,4 %) não tinham pérgola nessa data.**

## A retirada que isto obriga

**Do défice de 7,86 ha de 2026, 40,7 % é terreno sem pérgola.** A série do
défice conflaciona duas coisas que não são a mesma: copado a declinar a oeste,
e chão limpo a leste. Toda a afirmação que trate as 7,86 ha como uma grandeza
única fica por rever — incluindo o degrau, a duplicação 2024→2026, e o
cruzamento com o radar no foco ESTE.

Isto não invalida o caso; separa-o em dois. E era exactamente a distinção entre
fiabilidade e validade que faltava.

## Ficheiros

```
altura_copado.py     MDS-MDT, agregacao a 10 m, por unidade
chm_50cm.npy         modelo de altura a 50 cm sobre a AOI
chm_frac_alto.npy    fraccao acima de 1,5 m por celula de 10 m
chm_altura.npy       altura mediana por celula de 10 m
sem_pergola.npy      as 3,77 ha sem pergola em 06-07-2025
altura_copado.json   altura_focos.json
ganfei_s2\lidar\laz\ as duas nuvens classificadas
```

---

# Adenda ao certificado da C2

O que a C2 publicou sobre o foco ESTE foi refeito com a particao do LiDAR e
esta em `Downloads\_VALIDACAO_CAMADAS\CAMADA_2_ADENDA_LIDAR.md`, que substitui
partes do `CAMADA_2_CERTIFICADO.md` pela mesma regra que a R2 usou com a C0:
onde discordarem, ganha a adenda.

Resumo de uma linha: **V8 e a direccao de V10 aguentam por inteiro; V2 perde
mais de metade da magnitude publicada, que era a referencia a cair; e o degrau
do foco ESTE ganha o controlo negativo que lhe faltava** — existe em copado
(p=0,042) e nao existe em chao (p=0,368).
