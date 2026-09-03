# Camada 0 — revisão R2 do certificado

28-08-2026, fim do dia. **Substitui a secção PASSA PARA CIMA do
`CAMADA_0_CERTIFICADO.md`.** A C1 não pode arrancar sobre a lista original:
oito dos vinte e quatro factos foram alterados ou retirados pelo trabalho que
veio depois dela, e um deles inverteu de sinal.

O que veio depois: a revisão adversarial, a delimitação do controlo externo, a
re-derivação geográfica das máscaras, a re-execução da série, e três
coordenadas dadas pela gestora — o armazém e as duas pontas do B1.

---

## MANTÉM-SE sem alteração

**G1** AOI (529950, 4654600, 531950, 4655600), EPSG:32629, grelha de 10 m,
200×100. As 11 imagens partilham exactamente essa grelha.

**G7** Série radiometricamente comparável, verificada em 7637 píxeis estáveis,
sem degrau em 2022.

**G8** Nenhuma data com nuvem dentro do polígono.

**G10** A composição fenológica da série continua sem justificação: mantém-se
o dia-do-ano 243 e exclui-se o 245.

**G18** O esquema mostra duas filas de válvulas, norte e sul de uma conduta, e
sectores como faixas transversais ao eixo.

**G20** MDT cobre o polígono; faltam-lhe os 198 m mais a leste da AOI.

**G21** `bacia.json` inutilizável como está.

**G23** Traço de 1995 consistente; usar os centróides medidos, não os do CSV.

**G24** Quarentena da AOI 528400–529400. Mantém-se, e agora com explicação
completa: aquela área é tecido urbano de Valença, e o B1 verdadeiro fica a
1,1 km a sul dela.

## REFORÇADO

**G9** Os identificadores não só batem como os píxeis foram subtraídos contra a
cena recalculada do AWS: **19.964 píxeis válidos idênticos ao bit, diferença
máxima 0,000**, NaN nos mesmos sítios. As 11 datas têm a janela exacta da AOI.
O nome do ficheiro não estava a fazer de prova.

## CORRIGIDO

**G2 → 30,31 ha.** O polígono `pomar` passa a ser a máscara geográfica
derivada da ortofoto por periodicidade de compasso (5,0 m), não `nd2026 >
0,78`. IoU 0,844 com o antigo. *(±10 m no contorno)*

**G3 → azimute 70,3°, comprimento 1458 m.** Medido na máscara nova, por
caminho independente do da C0, que dava 70,0° e 1445 m.

**G4 → novas áreas.** `pomar` 30,31 ha · `saudavel` **1,10 ha** (rede
sistemática de 110 células, não escolhidas por aparência) · `zona0` 2,02 ha ·
**`manchaW` deixa de existir como máscara.**

**G5 → resolvido.** A circularidade foi corrigida. O conjunto operativo é
`sentinel/masks_geograficas.json`. O antigo `masks.json` fica só como
histórico.

**G6 → INVERTE DE SINAL.** A referência antiga subia (+0,0038/ano) porque
tinha sido escolhida por ter NDVI alto na última cena. A referência
sistemática **desce**: 0,8884 → 0,8425, **−0,00395/ano**. Toda a série tinha
uma inclinação artificial de cerca de 0,09 NDVI embutida. *Este é o facto mais
importante desta revisão.*

**G11 → muda de leitura.** Os ~8 ha abaixo da referência na primeira cena são
reais e espacialmente robustos (IoU 0,78–0,93 entre cinco cenas de 2017, núcleo
comum de 7,22 ha). Mas com máscaras limpas o défice **recupera** de 8,08 ha
(2017) para 2,91 ha (2024) antes de saltar para 7,86 ha (2026). Isso é copado
a fechar, não declínio antigo. **Retira-se a afirmação «a série começa depois
do início do declínio».**

**G12 → substituído** pela série re-executada.

**G16 e G17 → a georreferenciação não está estabelecida.** A gestora deu a
coordenada do armazém (E530360 N4654848); a colocação por contagem de fileiras
punha a linha 222 — «conduta principal à saída do armazém» — a **321 m** de
lá. A âncora nos extremos da parcela era suposição imposta. Continua válido, e
reforçado, que **nenhum ponto do terreno pode ser atribuído a uma válvula**.

**G19 → RESOLVIDO.** O bloco de ~16 ha a sudoeste **é o B1**. A gestora deu as
duas pontas: E529500 N4654010 a E530054 N4654413, 685 m, azimute 54°, a 526 m
do corpo principal. Cai exactamente sobre os polígonos C1a e C1b que a sessão
do controlo tinha delimitado sem nunca olhar para NDVI.

## RETIRADO

**G13 — a alteração de coberto entre 2021 e 2025 não se sustenta.** As
ortofotos têm radiometrias incomparáveis: luminância mediana 62,7 (2012),
109,0 (2021), 95,0 (2025), e o NDVI calculado das próprias ortofotos dá 0,361 /
0,055 / 0,173 sobre o mesmo pomar. São JPEG de 8 bits equilibrados para
visualização. **Qualquer comparação de brilho entre épocas é inválida**, e a
que produziu G13 era uma.

**G14 — os números caem, a conclusão sobrevive por outra via.** As fracções de
21/22/25 % vinham da mesma medição inválida. O teste refeito **dentro de uma só
imagem** (2025, radiometria comum) dá: referência 91,5 %, Mancha W 80,8 %,
Zona 0 64,2 %. As manchas têm **menos** superfície clara que a referência, não
mais. A conclusão «a cobertura não explica o padrão» mantém-se; a medição que
a sustentava é outra.

---

## ACRESCENTA-SE — factos novos, com instrumento

**G25.** **A referência sistemática desce.** Ver G6. Instrumento independente:
a máscara veio da ortofoto por periodicidade, sem NDVI; a tendência é medida no
Sentinel-2.

**G26.** **Não existe controlo externo de kiwi contemporâneo neste aluvião.**
Varrimento de ~3 km em imagem de 2021, 13 candidatos, 11 falsos positivos por
periodicidade de parcelas em faixa. O que existe é vinha (compasso 3,35 e
2,72 m), milho, túneis e estufas. O compasso do pomar do caso é 5,0 m, medido
por sessão independente. **Consequência: com dados de satélite, este caso não
consegue distinguir «esta parcela declina» de «todo o kiwi deste aluvião fez
isto».** Isto não é lacuna de busca; é resultado.

**G27.** **O único candidato a controlo era o B1**, e é a mesma exploração.
Confirmado pelas coordenadas da gestora.

**G28.** **O evento é de 2025.** Défice no polígono: 8,08 ha (2017) → 4,05
(2020) → 2,91 (2024) → 5,43 (2025) → 7,86 (2026). O pomar melhora seis anos e
duplica em dois.

**G29.** **A Mancha W emerge sozinha.** De um conjunto de máscaras que nunca
ouviu falar dela, um núcleo de 2,69 ha aparece em 2026 centrado em E530485 —
a 7 m do centro da máscara antiga — e está **ausente em 2024**. É a
verificação mais forte produzida neste processo.

**G30.** **A Zona 0 tem história física própria em 2021.** 45 % dela é solo
lavrado na ortofoto de 2021 (0,91 ha em 2,02), contra **0 %** da Mancha W e
**0 %** da referência. Removido esse solo, a parte plantada da Zona 0 está
plana de 2017 a 2024 e cai significativamente depois: −0,0150/ano, p = 0,032.

**G31.** **A grandeza operativa é a magnitude, não a fracção.** A fracção de
píxeis em défice satura (a Zona 0 chega a 100 % em 2026) e deixa de
distinguir. Toda a comparação temporal usa referência-menos-máscara, sempre
reportada com o nível absoluto ao lado.

**G32.** **Rede só no B1** (informação da gestora), no período do Enza Gold. O
corpo principal nunca teve. As duas datas de instalação e remoção estão por
dar, e sem elas a série do B1 tem dois degraus de posição desconhecida.

**G33.** **O B1 tem porta-enxerto diferente**: raízes de Summer Kiwi nas
válvulas 2–5, pé franco de Erica na válvula 1 e em todo o corpo principal.
É o único contraste de porta-enxerto do caso.

---

## O QUE A C1 NÃO PODE FAZER

**Não pode usar nenhuma série do B1 produzida hoje.** Foram três tentativas e
as três estão contaminadas: pelo invólucro do controlo (46 % das células com
variabilidade inter-anual acima do p90 do kiwi — culturas misturadas), pela
rede a entrar e sair, e pelas duas sobre-enxertias de 2016 e ~2020. As três
explicações estão em cima da mesa e nenhuma série actual as separa.

**Atribuição a válvulas: só na banda contígua.** Ver G35 — as válvulas 6 a 17
estão colocadas por área acumulada, com a válvula 8 a 34 m do ponto que o
gestor nomeou independentemente. Fora dessa banda, as oito parcelas soltas
(17,66 ha) continuam sem posição, e dentro do B1 não se sabe onde acaba cada
válvula — incluindo a fronteira do porta-enxerto.

**Não pode comparar níveis de NDVI entre B1 e corpo principal**, pela mesma
razão da rede.

---

# Suplemento à R2 — o que apareceu depois de ela ser escrita

Mesmo dia, algumas horas depois. Três coisas vieram do gestor e mudam a lista
outra vez. Fica em suplemento e não reescrito, para o rasto ser legível.

## G34 — A NOMENCLATURA ESTAVA INVERTIDA

Durante todo o processo correram dois vocabulários sem serem cruzados. **O que
a exploração chama «Zona 0» é o foco OCIDENTAL**; eu chamava «Zona 0» ao
oriental e «Mancha W» ao ocidental. Tudo o que se escreveu sobre «a Zona 0»
referia-se, conforme quem escrevia, a dois sítios a 500 m um do outro.

Os focos passam a identificar-se por coordenada. Ver `REGISTO_DE_NOMES.md`.

| | FOCO OESTE | FOCO ESTE |
|---|---|---|
| centro | E530485 N4655053 | E530977 N4655117 |
| área 2026 | 2,69 ha | 4,56 ha |
| nome da exploração | **«Zona 0»** | por confirmar |
| bloco | **B2**, válvulas 8 e 9 | **B3**, válvulas 13 e 14 |
| aparece na série | 2025; **ausente em 2024** | desde 2020 |
| amostras | as 4 ITS **e** o «Kiwi 1000» | só nemátodos (340/2026), as contagens **mais baixas** dos cinco blocos |

**Consequência que inverte uma afirmação central.** A frase «o foco mais antigo
é o menos analisado — só tem ITS, nunca teve painel» estava com os sujeitos
trocados. O foco OESTE é o **mais** amostrado. O foco ESTE é o maior, o mais
antigo na série, e o que só tem contagens de nemátodos.

**E fica em aberto uma discrepância entre relato e medição**, que é agora a
coisa mais interessante do caso: a exploração chama «Zona 0» ao sítio *onde o
declínio começou*, e esse foco **só aparece na série em 2025**. O outro está lá
desde 2020.

## G35 — AS VÁLVULAS ESTÃO COLOCADAS, POR ÁREA

O gestor deu a tabela válvula↔bloco↔**área**. Total 449.275 m² = 44,93 ha, que
fecha com o enquadramento. A banda contígua (válvulas 6 a 17) dá 27,30 ha
contra 30,31 ha de pérgola medida — a diferença são bermas e cabeceiras.

Método: integrar a área **medida** ao longo do eixo e cortar onde iguala a
área **tabelada**. Não usa o desenho, nem escala, nem leitura de píxeis.

Verificação independente: a **válvula 8 cai a 34 m** do centro do foco oeste,
que o gestor tinha nomeado como «Zona 0 = válvulas 8, 9, 10» — e essa frase
não entrou no cálculo. É o quarto método tentado e o primeiro que sobrevive.

Isto **substitui G16 e G17**: passa a haver atribuição ponto→válvula na banda
contígua. Fora dela não: as oito parcelas soltas (B4C3, B5, B1C5, B3C4,
viveiro, B1C6, B3C3 — 17,66 ha) têm área e não têm posição.

Posições em `valvulas_por_area.json`.

## G36 — B1: LOCALIZADO, COM PORTA-ENXERTO DIFERENTE, E COM REDE

B1 = válvulas 1 a 5 = **9,01 ha**, entre E529500 N4654010 e E530054 N4654413,
a 526 m do corpo principal. Raízes de **Summer Kiwi** nas válvulas 2-5,
sobre-enxertadas com Enza Gold em 2016 e com Erica por volta de 2020; a
válvula 1 (1,35 ha) e todo o corpo principal são **pé franco de Erica**.

**Houve rede, e só no B1**, no período do Enza Gold. Se saiu com ele, saiu por
volta de 2020 — o mesmo ano da enxertia da Erica. **Os dois efeitos coincidem
no tempo e têm sinais opostos**: tirar rede sobe o NDVI, cortar e enxertar
baixa-o. Nenhuma série que eu tenha os separa.

E as ortofotos não podem arbitrar: existem 2012 e 2021, **nenhuma entre elas**
— precisamente a janela em que a rede terá existido.

## G37 — RETIRADO: a medição de cobertura por ortofoto

As sete ortofotos têm radiometrias incomparáveis (luminância mediana 62,7 /
109,0 / 95,0 em 2012 / 2021 / 2025; NDVI próprio 0,361 / 0,055 / 0,173 sobre o
mesmo pomar). São JPEG de 8 bits equilibrados para visualização. **Qualquer
comparação de brilho entre épocas é inválida.** Isto retira o que restava de
G13 e o número de 83 % que chegou a entrar numa figura.

Comparações **dentro de uma só imagem** continuam válidas, e uma delas
sobrevive e importa: na ortofoto de 2021 o foco ESTE tinha 36 % de superfície
clara quando o resto do pomar tinha 3 %. Cruza com o outro achado de que 45 %
dele era solo lavrado nessa data.
