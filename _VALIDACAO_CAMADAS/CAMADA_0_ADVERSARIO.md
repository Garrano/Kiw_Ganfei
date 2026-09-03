# Camada 0 — ADVERSÁRIO do certificado

Sessão adversarial, 28-08-2026. Não recomputei nada. Não abri `masks.json`, os
GeoTIFF, as ortofotos nem o PDF do esquema. Li o certificado, o `PROTOCOLO.md`,
os `CONTROLOS.md` e os dezasseis scripts de `SAIDA_C0\`, mais os seus JSON de
saída (`c0_02_mascaras.json`, `c0_11_eixo.json`, `c0_12_ajuste.json`,
`c0_13_georref.json`, `c0_03_proveniencia.json`), que são produto da própria C0
e não dados brutos.

**Leitura geral, dita já:** este certificado é muito melhor do que aquilo que
substituiu. Encontra o seu próprio erro de escala, prova a origem aritmética da
AOI «b1», declara a circularidade das máscaras, e regista uma contaminação que
ninguém o obrigava a declarar. Nada do que se segue põe isso em causa. O que se
segue diz que **cinco factos da lista fechada não aguentam a forma como estão
escritos**, que **quatro têm margem optimista**, e que há **um número já
calculado pela própria C0, e não reportado, que decide sozinho o facto mais
consequente do certificado** (o G11).

---

## Transversais, primeiro

### A. A regra do instrumento independente foi cumprida?

**Não, e o certificado nem sequer tem a coluna.** O `CONTROLOS.md` §1 fixa o
formato em quatro colunas — `facto | ficheiro e cálculo | INSTRUMENTO
INDEPENDENTE usado | margem`. O certificado usa três. Não é formalismo: é a
coluna que obriga a escrever «nenhum» quando é o caso.

Fazendo a contagem à mão sobre os 24 factos de PASSA PARA CIMA:

- **Com instrumento genuinamente independente (7):** G2 (a ortofoto DGT — outro
  sensor, outro fornecedor, outro CRS — mostra assinatura de rede em ~24 das
  29 ha do polígono; a C0 mediu isto em `c0_09` e **não o reclamou** como a
  confirmação independente da georreferenciação, que é o que é), G15 e G18 (o
  PDF é um documento, independente do satélite), G19 (ortofoto), G22 (cabeçalhos
  de ficheiros de outro produtor), G23 (ortofoto de 1995), G24 (SCL descarregado
  do AWS + ortofoto + aritmética do desenho — três instrumentos a dizer o
  mesmo; é o facto mais bem estabelecido do certificado).
- **Verificados só pelo instrumento que os produziu (13):** G1, G3, G4, G5, G6,
  G7, G8, G9, G10, G11 (primeira metade), G12, G16, G17. NDVI confirmado com
  NDVI; a grelha do ficheiro confirmada com o cabeçalho do ficheiro; o eixo da
  parcela confirmado por PCA da máscara que o NDVI semeou; o ajuste de forma
  confirmado por resíduo contra o polígono a que foi ajustado.
- **Sem instrumento nenhum nesta camada (1):** G14, herdado da ADENDA e assim
  declarado.

Aplicar a regra à letra mandaria treze factos para NÃO TESTÁVEL e esvaziaria o
certificado. Não é isso que proponho: para um facto como G1 («os onze ficheiros
partilham a mesma transformação afim») não existe segundo instrumento nem faz
sentido exigi-lo. Proponho o que a regra realmente quer: **que a coluna exista e
diga a verdade**, para que a camada de cima saiba, facto a facto, se está a
receber uma medição corroborada ou um ficheiro a falar de si próprio. Neste
momento G7 e G9 lêem-se, no certificado, como se tivessem corroboração externa.
Não têm — ver removals abaixo.

### C. Entrou alguma coisa pela porta do lado?

Sim, seis coisas. Por ordem de gravidade:

1. **As «44,9 ha» da exploração.** Não aparecem em nenhum dos dezasseis scripts
   (`grep` em `SAIDA_C0\*.py`: zero ocorrências). Vêm da prosa. E é sobre elas
   que assenta o argumento de «lacuna de área» que dá força ao G19:
   «44,9 − 29,0 = 15,9 ha, contra 16,4 ha medidos… é forte». Uma coincidência
   entre um número medido e um número sem proveniência não é forte: é uma
   coincidência com metade dos termos por verificar.
2. **«válvulas 1–5», «o "B1" do seu esquema», «1,77 ha».** O certificado declara
   em NÃO TESTÁVEL que **não consegue ler a numeração das válvulas**. Depois usa
   essa numeração no G19, e o `c0_15_mapas.py` imprime-a no mapa que vai para a
   gestora («As válvulas 1–5 (o "B1" do seu esquema, anotado 1,77 ha)…»). O
   detector encontrou **dois** anéis a oeste (`c0_13_georref.json`, x = 296 e
   x = 600), não cinco. Os rótulos são da prosa.
3. **O nome «B1» a reentrar.** O G24 põe o nome em quarentena e diz «não reentra
   por nenhuma porta». O G19 e a M1 v2 reintroduzem-no, referido a outro objecto
   (a anotação do desenho). Pode ser legítimo que sejam dois objectos — mas é
   exactamente esta homonímia que já custou semanas, e reaparece na única peça
   que sai para fora da equipa.
4. **«cerca de 1 km a sudoeste», na M1 v2.** O certificado ordena retirar a
   distância de 1,06 km e **não a substituir por outra**. A M1 v2 escreve «cerca
   de 1 km». Pela georreferenciação adoptada, do anel oeste ao vértice mais
   próximo do polígono são ~940 m e ao centróide ~1550 m; a frase é defensável
   como distância de bordo, mas vai sem dizer qual das duas é, e sem os ±150 m
   de erro de extrapolação que a própria C0 declara.
5. **G14 inteiro.** Herdado da ADENDA, sem instrumento nesta camada. Ver
   remoção 1.
6. **A contaminação declarada.** Está bem que tenha sido declarada, mas note-se
   *onde* caiu: as linhas lidas eram «sobre o comportamento do bloco "B1" em
   Ago/2025» e «números do dossiê» — isto é, precisamente sobre os dois assuntos
   em que o certificado depois toma as suas decisões mais fortes (rejeitar o B1,
   e usar 44,9 ha). Não digo que enviesou. Digo que a contaminação não caiu num
   sítio inócuo, e que o 44,9 é um forte candidato a ter entrado por aí.

**E uma incoerência interna, da mesma família:** a nota de abertura diz «não
abri o dossiê, as figuras F1–F7, nem qualquer PNG/SVG de saída». Mas cinco
factos do certificado são leituras visuais de PNG de saída: o bloco de título
(`c0_rega_D_titulo.png`), as duas filas de válvulas (`c0_rega_B_centro.png`), a
feição linear de 1995 (`c0_14_traco1995.png`), «campos e mata, não pomar com
rede» (`c0_09_rede_2025.png`) e «linhas de pomar contínuas» nos 8,21 ha. Ou a
declaração está errada, ou as leituras não aconteceram. É preciso dizer qual —
porque estas são as únicas cinco confirmações por instrumento verdadeiramente
diferente que o certificado tem, e a sua proveniência tem de ser auditável.

### D. As quantidades-âncora batem certo?

**Batem todas as dez.** Verifiquei contra `c0_02_mascaras.json`:

| Âncora | Declarado | Medido pela C0 | |
|---|---|---|---|
| AOI | 529950, 4654600, 531950, 4655600 | idem | ✓ |
| `pomar` px | 2903 | 2903 | ✓ |
| `pomar` ha | 29,0 | 29,03 | ✓ |
| referência (3 manchas) | 454 | 264+119+71 = 454 | ✓ |
| `manchaW` | 427 | 427 | ✓ |
| `zona0` | 220 | 220 | ✓ |
| cenas | 11 | 11 | ✓ |
| plena estação | 9 | 9 | ✓ |
| NDVI ref. 2017-07-02 | 0,838 | 0,8379 | ✓ |
| NDVI ref. 2026-07-27 | 0,886 | 0,8862 | ✓ |

O conflito conhecido (2906/446/423/219) está resolvido e bem resolvido: as
contagens booleanas reproduzidas batem ao píxel com os valores da prosa
(`contagens_booleanas` no JSON: 2906, 446, 423, 219). Isto é um resultado
sólido e deve ser lido como tal.

**Mas as duas últimas âncoras não são reportadas no certificado.** Estavam
calculadas e gravadas; reportá-las custava uma linha. O `CONTROLOS.md` §2 diz
«todas as camadas reportam, sempre, mesmo que não lhes tenham tocado». Corrigir
antes de passar à C1: sem isso, a C1 não tem contra o que comparar.

---

## 1 · Factos a retirar do PASSA PARA CIMA

### R1 — G14 («negativo registado» sobre a cobertura/rede)

**Porquê.** Não foi medido nesta camada. O próprio texto diz «este teste não foi
refeito nesta camada; é herdado da ADENDA». O `PROTOCOLO.md` §3 é explícito:
«"Foi verificado numa sessão anterior" não é prova». Um negativo registado é a
coisa mais perigosa de herdar sem verificação, porque a sua função é impedir
que alguém volte a testar.

**Premissa que teria de ser falsa.** Que a ADENDA mediu a máscara de cobertura
com a mesma definição de Mancha W, Zona 0 e referência que esta camada acabou
de certificar. Não há nada que o garanta — e sabemos que os números da ADENDA
não reproduzem: a própria C0, ao tentar reproduzir a outra medição da ADENDA
(8/9/21 %), obteve 5,1/2,3/16,4 %.

**Teste de cinco minutos.** Não há atalho: refazer a intersecção da máscara de
cobertura com as três máscaras actuais e comparar médias de NDVI sob e fora de
cobertura numa data. É meia hora, não cinco minutos.

**O que cai com ele.** Nada, no imediato — mas a hipótese «a rede explica o
padrão» volta a estar aberta para a C2 e a C4, e é melhor que esteja aberta do
que fechada com um cadeado sem chave.

**Recomendação:** mover para NÃO TESTÁVEL com a redacção «a ADENDA dá este
teste por feito; a C0 não o verificou».

### R2 — G13 («houve alteração física do coberto entre 2021 e 2025»)

**Porquê.** O que `c0_09_copado_orto.py` §3 mede é a fracção de píxeis com
luminância > 170 em três ortofotos de épocas, sensores, resoluções nativas e
cadeias de processamento diferentes, **sem qualquer normalização radiométrica
entre elas**. É o erro que a mesma sessão soube evitar no Sentinel — onde foi
buscar alvos estáveis por SCL antes de comparar datas — e não aplicou aqui.

**Premissa que teria de ser falsa.** Que a luminância absoluta de uma ortofoto
DGT de 2025 a 25 cm é comparável à de 2021 a 25 cm e à de 2010 a 50 cm. Os
próprios números dizem que não é: **2010 dá 5,1 % e 2021 dá 2,3 %** — o «coberto
claro» *desceu* para menos de metade entre 2010 e 2021 e depois multiplicou por
sete. Uma métrica que não é monótona onde não deveria haver salto é uma métrica
que está a medir a imagem tanto quanto o terreno.

**Teste de cinco minutos.** A mesma estatística, nas mesmas três ortofotos, numa
janela que seguramente não mudou — um troço de estrada asfaltada, um telhado, o
leito do rio. Se o «controlo» também saltar em 2025, o G13 morre como está
escrito. É o teste nº 2 da lista abaixo.

**O que cai com ele.** É facto isolado dentro da C0, mas é exactamente o tipo de
facto que a C2 e a C4 usarão para datar uma intervenção («houve replantação /
instalação de rede entre 2021 e 2025»). Passar isto por medido, quando é uma
diferença de brilho não calibrada, é fabricar uma data.

**Recomendação:** retirar a formulação causal. Se quiserem manter alguma coisa,
mantenha-se «a fracção de píxeis claros difere entre as três ortofotos nesta
janela: 5,1 / 2,3 / 16,4 %» — que é facto de ficheiro, e é o que está medido —
com a nota de que a comparação entre épocas não está normalizada.

### R3 — a atribuição cardinal do G18 («duas filas, **uma a norte e outra a sul**»)

**Porquê.** A transformação de `c0_13_georref.py` é uma semelhança pura
estimada por: centróide → centróide, comprimento → comprimento, ângulo do eixo
principal → ângulo do eixo principal. Quatro parâmetros, todos vindos do alvo.
**Não há nada nesse ajuste que resolva a reflexão sobre o eixo maior.** Para uma
mancha alongada e aproximadamente simétrica, o resíduo — distância de cada
ponto ao segmento mais próximo do contorno — é praticamente igual com e sem
espelho. E o certificado diz, com razão, que a folha não está com o norte para
cima. Logo «norte» e «sul», no desenho, são norte e sul *da folha*; qual deles
cai a norte no terreno é uma pergunta a que a georreferenciação adoptada não
responde.

**Premissa que teria de ser falsa.** Que a folha não está espelhada em relação
ao terreno, e que a correspondência entre a metade superior do desenho e o lado
norte da parcela foi verificada. Não foi.

**Teste de cinco minutos.** Refazer o ajuste com o desenho reflectido em torno
do eixo maior e comparar a mediana e o p90 do resíduo. Se as duas soluções
ficarem a menos de ~10 m uma da outra, a atribuição norte/sul é indeterminada e
tem de sair.

**O que cai com ele.** A pergunta 2 da M1 v2 («o seu esquema mostra duas filas,
uma a norte e outra a sul da conduta. Confirma que é assim no terreno?») deixa
de ser neutra e passa a induzir a resposta — o mesmo defeito que o certificado
identificou e corrigiu na pergunta 5 da versão anterior. E qualquer leitura
futura de tipo «a fila norte alimenta a Zona 0» nasce morta.

**Recomendação:** manter «duas filas, uma de cada lado da conduta» e «faixas
transversais ao eixo»; retirar norte e sul até haver o teste do espelho ou a
confirmação da gestora.

### R4 — o G9, como está redigido («os identificadores batem, e a janela lida corresponde à AOI»)

**Porquê.** É o único ponto do certificado em que reproduz, sem se aperceber, a
estrutura exacta do erro que abriu esta cadeia. O que `c0_03_proveniencia.py`
faz é: ler os IDs de `proveniencia.json`, perguntar ao catálogo se existem,
comparar `properties.datetime[:10]` com o **nome do ficheiro**, e testar um
ponto contra o *bounding box* do `geometry`. **Nada liga os píxeis entregues em
`sentinel/*.tif` a esses identificadores.** Se um ficheiro tiver dentro a data
errada, a cena errada, ou uma janela deslocada, todos estes testes passam. É a
mesma premissa do B1 — «chama-se assim, logo é isso» — aplicada à série
principal.

Duas imprecisões concretas de prosa-contra-código, na mesma linha:

- o certificado diz «teste ponto-em-polígono do `geometry`»; o código faz
  `min(xs) < LON < max(xs) and min(ys) < LAT < max(ys)`, que é o *bounding box*,
  não o polígono — e os *footprints* Sentinel-2 são frequentemente não
  rectangulares;
- diz «a AOI cai dentro do *footprint* de todas»; o código testa **um ponto**
  fixo (−8,62601, 42,04734 — o centro da AOI), não a AOI.

**Teste de cinco minutos, e é o mais importante do documento.** A C0 **já tem
em disco** a cena 2017-07-02 descarregada e recalculada de forma independente a
partir do AWS: `SAIDA_C0\cenas_extra\2017-07-02_S2B_29TNG_20170702_0_L2A.tif`,
produzida por `c0_04_cena2017.py`. Comparar essa matriz com
`sentinel/2017-07-02.tif` é uma subtracção. Se o máximo da diferença absoluta
for ~0, a proveniência da série está confirmada por instrumento independente
para essa data, e o argumento estende-se por construção às outras (mesmo
produtor, mesma cadeia). Se não for, a cadeia pára aqui.

**O que cai com ele se estiver errado.** Tudo. G1, G6, G7, G8, G10, G11, G12 e a
totalidade da C2.

**Recomendação:** retirar «a janela lida corresponde à AOI» (não foi medido) e
reescrever o G9 como «os onze identificadores existem no catálogo e a sua data
coincide com o nome do ficheiro; a correspondência entre os píxeis entregues e
esses identificadores NÃO foi verificada». Ou correr o teste — cinco minutos — e
escrever o facto forte.

### R5 — o G12 (3,75 ha «que passou de sã a deficitária durante a série»)

**Porquê.** Três razões que se somam, todas com a direcção conhecida:

1. **Ruído de amostragem de uma cena por ano.** A própria C0 mostra que, *dentro
   de 2017*, mudar de cena move a área em défice entre 7,65 e 8,21 ha — 7 % de
   variação por escolha de data. A regra da M2 exige «dois anos consecutivos em
   défice» aplicada a **uma amostra por ano**. O G12 é a diferença entre duas
   grandezas ruidosas.
2. **O enviesamento da referência tem duas consequências e o certificado só
   declara uma.** A referência é escolhida por NDVI alto **na última cena**.
   Isso não só levanta a referência no fim (o que a C0 diz) como levanta o
   limiar `ref − 0,05` no fim, o que **infla a área classificada como défice
   nos últimos anos** — e portanto infla o G12 e as manifestações tardias da
   M2. Esta segunda consequência não está escrita em lado nenhum.
3. **A margem ±0,6 ha é emprestada.** O certificado diz «±0,6 ha, pela mesma
   razão» — a razão do G11. Mas o `c0_04_cena2017.py` §c2 **imprime a
   sensibilidade própria do G12** («declinou = X ha») para cada cena alternativa
   de 2017, e esses números não foram reportados. A margem existe medida e não
   foi usada.

**Premissa que teria de ser falsa.** Que uma cena por ano representa o ano, e
que a referência não se move com o que se está a medir.

**Teste de cinco minutos.** Reportar os cinco valores de «declinou» já impressos
por `c0_04` §c2. Se variarem mais do que ±0,6 ha, a margem está errada e sabe-se
por quanto.

**O que cai com ele.** A escada de anos da M2 v2 — que é a peça que a C4 usará
para cruzar cronologia com etiologia.

**Recomendação:** não passa como número até a sensibilidade já calculada estar
reportada. Passa como «entre ~3 e ~5 ha, com o enviesamento da referência a
actuar no sentido de aumentar este valor».

---

## 2 · Factos a manter, com margem maior

### M1 — G11 (8,21 ha «já em défice na primeira cena») — **o mais consequente do certificado, e o mais frágil**

Este facto sobrevive à crítica que a C0 lhe fez (a escolha da data) e não
sobrevive à que ela não lhe fez. Ponho-o aqui e não nas remoções porque acho
provável que esteja certo — mas a confiança declarada não é a que os números
suportam.

**O que a C0 mediu e não juntou.** Duas coisas, ambas no seu próprio
certificado:

- a referência sã tem desvio-padrão **0,111 em 2017-07-02** contra **0,014–0,040
  em 2018–2026**, e as outras quatro cenas de 2017 dão 0,065–0,099 — isto é,
  *todo* o ano de 2017 é 3 a 7 vezes mais disperso;
- a regra de défice é um **desvio fixo** de −0,05 abaixo da média da referência.

Um limiar de desvio fixo aplicado a uma distribuição alargada apanha
mecanicamente mais área. Com σ = 0,111, o limiar está a 0,45 σ da média:
esperam-se ~33 % de píxeis abaixo dele só por dispersão. Com σ = 0,03 (2026),
está a 1,7 σ: esperam-se ~5 %. **A fracção observada em 2017 é 28–29 %.** A
ordem de grandeza da hipótese nula «isto é a cauda de uma cena ruidosa» é a
mesma da medição. Não prova que seja artefacto; prova que o certificado não
distinguiu as duas hipóteses.

E o teste de robustez que a C0 fez — repetir com as outras quatro cenas de 2017
— **não testa isto**, porque as cinco cenas partilham a anomalia de 2017. Testa
a escolha da data dentro do ano; não testa o ano.

Note-se ainda o padrão cruzado nas duas tabelas do certificado: em 2017 o alvo
estável (SCL 5, NDVI baixo) lê **0,236**, dentro da normalidade dos outros anos
(0,212–0,241), enquanto o copado (NDVI alto) lê **0,838**, 0,05 abaixo de todos
os outros anos (0,881–0,919). O G7 declara a série radiometricamente comparável
com base apenas no alvo de NDVI baixo. Sobre alvos de NDVI alto — que é onde a
medição se faz — 2017 comporta-se de outra maneira, e a média desloca-se
exactamente o valor do limiar de défice. A média cancela (o limiar é relativo à
referência da própria cena); **a variância não cancela**, e a regra é
sensível à variância.

**O número que decide isto já está calculado.** `c0_04_cena2017.py` imprime a
**matriz de IoU entre as máscaras de défice das cinco cenas de 2017**. Se o IoU
for alto (≳0,7), os 8,21 ha são uma mancha espacialmente coerente que reaparece
em cinco datas ao longo de dois meses, e o G11 passa a estar solidamente
estabelecido — mais do que está agora. Se for baixo (~0,4), a área é estável mas
a *localização* não é, e então o que se mediu é a cauda de uma distribuição
ruidosa e o G11 cai com o G12 atrás. **Este número não está no certificado.**

**Segunda ressalva, mais pequena mas verificável agora:** os dois conjuntos de
valores da linha do CONFIRMADO não são consistentes entre si. Áreas
8,21 / 7,88 / 7,83 / 8,20 / 7,65 ha sobre um `pomar` de 29,03 ha dão fracções
de 28,3 / 27,1 / 27,0 / 28,2 / 26,3 %. O certificado escreve
29,4 / 28,1 / 29,9 / 30,8 / 29,7 %. No código, as duas grandezas saem da mesma
linha do mesmo `print`, logo o erro é de transcrição — mas 8,21 ha é o número
de cabeçalho do G11 e não se sabe qual dos dois é o que a máquina imprimiu.

**Margem honesta:** ±0,6 ha cobre a escolha da data dentro de 2017. Não cobre o
limiar (−0,05), não cobre a anomalia de 2017, não cobre a definição da
referência. Enquanto o IoU não for reportado, o G11 deve passar como «entre 6 e
9 ha, com uma hipótese alternativa por excluir (a dispersão anómala de 2017)».

**E a segunda metade do G11 — «não é falha de copado» — não tem medição
nenhuma.** É uma leitura visual, de um PNG que a nota de abertura diz não ter
sido aberto, sem nenhum script que sobreponha a máscara dos 8,21 ha à ortofoto.
`c0_09` detecta assinatura de rede na *janela toda*, não nessa máscara. É a
afirmação que inverte a cronologia do caso inteiro e é a que tem menos suporte
escrito. Teste: sobrepor a máscara de défice de 2017 à ortofoto de 2025 e medir
que fracção dela tem assinatura de rede — cinco minutos, e o código já existe
todo em `c0_09`.

### M2 — G15 (o esquema «é proporcional», ±3 %)

A escala declarada está verificada (o bloco de título lê 1/3500 @ A1 — confirmado
independentemente). O que não está verificado é a proporcionalidade, e os
números da própria C0 dizem-no:

| | desenho (troço este) | à escala declarada | parcela medida | erro |
|---|---|---|---|---|
| comprimento | 1742,8 px | 1468–1523 m | 1445 m | +1,6 a +5,4 % |
| largura | 343,9 px | 290–300 m | 328 m | −8 a −12 % |

O rácio desenhado é 5,07; o medido é 4,40. **Diferença de forma de 15 %, que
nenhuma escala corrige.** As duas dimensões implicam duas escalas diferentes:
0,829 m/px pelo comprimento, 0,954 m/px pela largura. O certificado escolhe a
dimensão que concorda e declara ±3 %.

Há ainda um problema de estimador: em `c0_12_ajuste_esquema.py`, o comprimento é
`p1.max() - p1.min()` (sensível a um único píxel rosa perdido — uma anotação,
uma cauda de seta, o halo anti-serrilhado de um anel de válvula) e a largura é
`percentile(p2, 97) - percentile(p2, 3)` (aparado). Os dois números são
comparados como se fossem homogéneos e não são. Recalcular ambos com ambos os
estimadores é um minuto.

E há uma consequência física que ninguém apontou: sob a georreferenciação
adoptada (0,829 m/px) a largura desenhada do **terreno** dá 285 m, enquanto o
**copado** medido tem 328 m. O limite de propriedade desenhado passaria ~21 m
*dentro* do copado, dos dois lados, ao longo de 1,4 km. Ou o polígono `pomar`
transborda a parcela (plausível: um limiar de NDVI apanha sebes e bordadura), ou
o desenho não é desta parcela. A primeira hipótese abre uma ressalva ao G2
(ver M3); a segunda seria grave. Distinguem-se com o mesmo teste do espelho e
com o teste das áreas anotadas (teste 3 abaixo).

**Margem honesta:** ±8 % na escala, não ±3 %. E a redacção deve dizer
«proporcional no comprimento; discrepante em 15 % na forma».

### M3 — G2 (29,03 ha) e G4 (as áreas das máscaras)

As contagens são exactas e reproduzidas — isso está estabelecido. O que está
optimista é a tradução em área.

«±10 m no contorno» e «±0,01 ha por píxel de bordo» são verdadeiras e
inutilizáveis, porque não dizem quantos píxeis de bordo há. Um polígono de
1445 × 328 m tem perímetro ≳3,5 km, ou seja ≳350 píxeis de bordo. Um deslocamento
sistemático de meio píxel no limiar move a área **±1,5 a 2 ha (5 a 7 %)**, e o
limiar é um NDVI de 2026 sobre um copado que, em 29,9 % do polígono, já está
abaixo desse limiar e só lá entrou pelo fecho morfológico. Toda a fracção
publicada (8,21/29,03; 3,75/29,03) herda esta incerteza no denominador, e
nenhuma a declara.

Acresce a ressalva registada no CORRIGIDO e não propagada ao G4: o polígono
`saudavel` tem 454 px contra 446 da booleana, isto é **8 píxeis (1,8 %) da
referência não cumprem os critérios da própria referência** (`copado`,
`interior`, `longe`). «Longe» é o critério de afastamento da Mancha W e da
Zona 0: se algum desses 8 píxeis estiver junto à mancha, a referência está a
seguir parcialmente aquilo que devia medir, e o défice fica subestimado. Cinco
minutos: a série da referência com 446 px contra a série com 454 px, por data.

**Margem honesta:** área do `pomar` 29,0 ± 1,5 ha; áreas das máscaras com a
mesma percentagem.

### M4 — G16 e G17 (georreferenciação, ±60–100 m)

Concordo com a conclusão e com a ordem de grandeza, e o G17 («nenhum ponto do
terreno pode ser atribuído a uma válvula ou a um sector») é a melhor decisão do
certificado. Duas correcções à natureza do número:

- **O resíduo é dentro da amostra.** Os pontos com que se mede o resíduo são
  exactamente os pontos com que se estimou a transformação. Não há validação
  cruzada, nem sequer o barato: ajustar com metade do troço e medir na outra.
- **O resíduo mistura duas coisas.** Distância entre o limite do *terreno*
  desenhado e o contorno do *copado* medido — dois objectos que não têm de
  coincidir, como o próprio certificado diz em NÃO TESTÁVEL. Portanto 64 m não é
  o erro de georreferenciação: é um limite superior de composição desconhecida.
  Pode ser melhor no interior e é seguramente pior na extrapolação.
- Para o G19, onde se extrapola ~1200 px (≈1 km) para lá do troço ajustado, os
  ±150 m declarados assumem que o erro angular é ±1,5°; com a incerteza de forma
  de 15 % apurada em M2, o intervalo defensável é **±150 a 250 m**.

Uma ressalva de código que afecta os três: a máscara `rosa` de `c0_12`, `c0_13`
e `c0_14` é só uma gama de cor mais uma caixa. A docstring diz «sem as anotações
a mão». Os filtros `G > 70` e `B > 70` de facto excluem tinta vermelha e laranja
vivas — mas **não excluem o halo anti-serrilhado dos treze anéis de válvula
vermelho-escuros**, que passa por rosa claro e cai dentro da zona do desenho.
Repare-se que o `c0_15_mapas.py`, ao desenhar o mesmo objecto, **acrescenta** um
limite superior (`r - b < 0.34`) que os scripts de medição não têm: o mesmo
autor, duas definições do mesmo objecto, e a mais permissiva é a que fixa a
escala, a rotação e o centróide de que tudo depende. Cinco minutos: contar as
componentes conexas da máscara rosa e ver se são a linha do terreno ou a linha
mais treze halos.

### M5 — G7 (comparabilidade radiométrica, ±0,015)

O método está certo — alvos escolhidos pelo SCL e não adivinhados, e é a melhor
verificação de proveniência do certificado. A margem é que não sobrevive aos
próprios números: **2021 dá 0,241 e 2022 dá 0,212**, uma diferença de 0,029
entre anos consecutivos, sobre o mesmo alvo estável, e é exactamente na
transição que se está a testar. Declarar ±0,015 e reportar uma oscilação de
0,029 é incoerente.

Isto **não** contamina a medição de défice, porque o limiar é relativo à
referência da mesma cena e um viés aditivo cancela — vale a pena dizê-lo
explicitamente à C2, que é quem vai usar isto. Mas contamina qualquer
comparação de NDVI absoluto entre datas, e o próprio G6 é uma dessas.

**Margem honesta: ±0,03.** E acrescentar a frase que falta: «o desvio entre
datas sobre alvo estável é de 0,03, contra um limiar de défice de 0,05; qualquer
grandeza absoluta comparada entre datas tem de ser lida com essa escala».

### M6 — o que está bem estabelecido, e deve ser dito com a mesma clareza

- **G24 (a quarentena do «b1»)** é o facto mais forte do documento. Três
  instrumentos independentes: SCL descarregado directamente do AWS sobre a
  janela (63 % vegetação de jardim, 0 % água), a ortofoto DGT que cobre a
  janela, e a aritmética que reconstrói o erro a partir da escala das âncoras.
  Não tenho ataque a fazer-lhe. Uma ressalva só de perímetro: o inventário de 49
  ficheiros varre duas raízes e cinco extensões de texto (`.py .csv .json .md
  .txt`). Não vê dentro de `.docx`, `.xlsx`, `.pdf`, `.zip`, notebooks, nem
  legendas de figuras — e a própria nota de contaminação prova que existe pelo
  menos um ficheiro relevante numa **terceira** raiz
  (`AUDITORIA_COWORK_2026-08-28.md`). «Inventário fechado» deve ler-se
  «inventário fechado sobre duas pastas e cinco extensões».
- **G21 (`bacia.json`)** é aritmética verificável e a observação de que
  29,03 + 7,88 = 36,91 é excelente trabalho detectivesco.
- **A arbitragem 2906/2903** está resolvida ao píxel e encerra um falso defeito
  que andava a circular. Sólido.
- **G10 (a regra de fenologia)** é auto-crítica correcta e bem documentada;
  passa como está.
- **G5 (circularidade das máscaras)** é o facto que mais falta fazia e está bem
  escrito — inclusive a distinção de que só a `zona0` escapa.
- **G1, G8, G20, G22** são propriedades de ficheiro, verificadas contra os
  ficheiros. Não têm segundo instrumento nem precisam — desde que o G9 fique
  resolvido, porque é ele que garante que os ficheiros são o que dizem ser.

---

## 3 · A pergunta que falta

> **Contra o que é que este pomar está a ser comparado?**

A cadeia inteira nasceu de um controlo falso. O «B1» sobreviveu semanas não
porque ninguém verificasse contas, mas porque **fazia falta**: era o bloco são
contra o qual o bloco doente se destacava. A C0 fez o trabalho certo e
removeu-o. E depois **não perguntou o que fica no lugar dele** — e o certificado
não regista essa ausência em lado nenhum, nem em NÃO TESTÁVEL.

Repare-se no que sobra depois da quarentena. Todas as grandezas da lista fechada
são internas a um polígono de 29 ha: o défice é medido contra 4,54 ha de
referência **dentro do mesmo polígono**, escolhidos por NDVI alto **na última
cena da mesma série**, sobre **as mesmas onze imagens**. Não há uma única
grandeza no PASSA PARA CIMA que permita distinguir «esta parcela está em
declínio» de «tudo o que é kiwi neste aluvião se comportou assim nestes nove
anos» — nem de «estas nove cenas comportaram-se assim». Um declínio regional,
uma sequência de anos secos, uma mudança de prática comum à zona, ou um
problema de correcção atmosférica com assinatura sazonal, entram todos por esta
porta e saem indistinguíveis de patologia local.

E o mais duro: **a C0 teve o controlo nas mãos e usou-o para outra coisa.**
Mediu 16,4 ha de pomar com rede a 750 m a sudoeste (G19) e 13,36 ha de
assinatura de rede dentro da AOI e fora do polígono. São kiwi, ou parecem-no; são
cobertos pelas mesmas onze cenas, com a mesma grelha, o mesmo sensor e as mesmas
datas; e o custo de extrair a série de NDVI de qualquer um deles é o mesmo custo
de extrair a do polígono principal — o código está escrito. A única pergunta que
a C0 fez sobre o bloco sudoeste foi «será da exploração?». A pergunta que
faltava era **«e se não for da exploração — melhor ainda: como se comporta?»**

Isto é uma pergunta da C0 e não da C2, por duas razões. Primeira, é geometria:
delimitar um polígono de controlo é exactamente o trabalho desta camada, e é a
camada que sabe agora onde ele está e como se mede. Segunda, e mais importante:
se a delimitação do controlo for feita pela camada que depois o vai usar para
provar alguma coisa, ela vai desenhá-lo — inconscientemente — onde lhe convém.
Foi assim que se chegou ao B1: uma AOI escolhida por uma sessão que precisava de
que existisse.

Uma segunda pergunta, mais pequena e do mesmo feitio, para não a perder: **qual é
o objecto de estudo, e quem lhe traçou a fronteira?** O certificado herda «44,9 ha
de exploração» da prosa, mede 29,03 ha de copado com NDVI de 2026 e trata a
diferença como um mistério de localização. Mas a fronteira de 29,03 ha não é a
fronteira de uma exploração: é o contorno da vegetação que ainda estava viva na
última imagem da série. Um pomar que tenha morrido completamente antes de 2026
não está na máscara, não está no denominador, não está em nenhuma fracção e não
existe para nenhuma camada acima. O certificado diz isto em NÃO TESTÁVEL («não
consegui quantificar o que ficou fora») — mas então o G2 não devia passar como
«o polígono `pomar` tem 29,03 ha» e sim como **«o copado vivo em Julho de 2026
tem 29,03 ha; a área plantada é desconhecida e é ≥ este valor»**. É uma
diferença de uma linha, e é a diferença entre a C2 medir uma fracção com
denominador certo e medi-la com um denominador que exclui, por construção, o
caso mais grave.

---

## 4 · Os cinco testes de cinco minutos, por valor

**1. Identidade dos píxeis (fecha a classe de erro que abriu esta cadeia).**
`np.nanmax(np.abs(a - b))` entre `ganfei_s2\sentinel\2017-07-02.tif` e
`SAIDA_C0\cenas_extra\2017-07-02_S2B_29TNG_20170702_0_L2A.tif`. Os dois
ficheiros já estão em disco; o segundo foi calculado a partir do AWS por
`c0_04`. Repetir para 2026-07-27 descarregando a cena (o código de `baixa()`
já existe). Custo: dois minutos. Ganho: transforma o G9 de asserção de nome em
facto medido, e fecha, para a série principal, exactamente a pergunta que
ninguém fez sobre a `sentinel_b1\`.

**2. A matriz de IoU de 2017, que já está calculada.**
`c0_04_cena2017.py` imprime a concordância espacial entre as máscaras de défice
das cinco cenas de 2017. Basta reler o `stdout` — ou correr o script, que tem as
cenas em cache. Custo: zero. Ganho: decide entre «os 8,21 ha são uma mancha
real» e «os 8,21 ha são a cauda de uma cena três vezes mais dispersa», que é a
diferença entre a cronologia do caso mudar de sentido e não mudar. É o número
com maior razão valor/esforço do documento inteiro.

**3. Controlo radiométrico das ortofotos (mata ou salva o G13).**
A mesma estatística de `c0_09` §3 (fracção de luminância > 170, média, p90) nas
ortofotos de 2010, 2021 e 2025, numa janela que não pode ter mudado — asfalto,
telhado, leito do rio. Custo: cinco minutos, o código está escrito, só muda a
janela. Ganho: se o controlo saltar em 2025 como a janela da ADENDA saltou, o
G13 é brilho e não coberto. Se não saltar, o G13 passa a ser um dos factos mais
fortes do certificado, com instrumento independente a sério.

**4. As áreas que o próprio desenho anota (testa a escala e mata um rótulo).**
O desenho escreve «1 ha» sobre o viveiro e «1,77 ha» sobre o bloco oeste.
Medir as duas áreas em píxeis do render a 300 dpi e converter a 0,8290 m/px.
Custo: cinco minutos, com a máscara rosa já feita. Ganho duplo: (a) é a única
verificação **interna** da escala declarada, independente da suposição de que a
moldura detectada é a moldura A1 de 811–841 mm — que hoje é a única fundação do
«1/3500 @ A1» ser accionável; (b) o troço oeste do desenho tem 476 × 257 px, ou
seja ~394 × 213 m ≈ 8 ha de caixa envolvente à escala adoptada. Se a anotação
diz 1,77 ha, então «válvulas 1–5 = B1 = 1,77 ha = o bloco de 16,4 ha» não pode
ser tudo a mesma coisa, e o G19 tem de escolher qual das identificações mantém.

**5. O teste do espelho na georreferenciação (decide o G18).**
Refazer o ajuste de `c0_13` com a fonte reflectida em torno do eixo maior e
comparar mediana e p90 do resíduo com os 64 m / 110 m actuais. Custo: três
linhas. Ganho: se as duas soluções empatarem, «norte» e «sul» saem do G18 e a
pergunta 2 da M1 v2 é reescrita antes de ir para a gestora — que é a última
oportunidade de não pedir a uma testemunha que confirme aquilo que já lhe
sugerimos.

*Ficam de fora por pouco, e são todos baratos:* a composição da máscara rosa
(quantas componentes conexas, e são halos de válvula?); a série da referência
com 446 px contra 454 px; os cinco valores de «declinou» do `c0_04` §c2 que
dariam a margem verdadeira do G12; a direcção das linhas de plantação medida na
ortofoto de 25 cm, que daria ao G3 (azimute 70°) o instrumento independente que
não tem; e reportar a tabela de disponibilidade de cenas que o `c0_03` já
produziu — há **mais de cem cenas com menos de 10 % de nuvem entre Junho e
Setembro** no `c0_03_proveniencia.json` (por exemplo 2019: quatro em Julho e
oito em Agosto, e a série usa 2019-09-02, que depois é excluída por fenologia).
A C0 correu essa consulta, gravou-a, e não a reportou. Muda a natureza do
problema do G10: a incoerência fenológica não é uma limitação da série, é uma
escolha reversível — há cenas para fixar uma janela de dia-do-ano igual em todos
os anos, e há cenas suficientes para substituir a amostra pontual anual por uma
média de época, que é o que faria desaparecer metade do ruído em que assentam o
G11 e o G12.

---

## 5 · Veredicto

**Segue para a camada seguinte com as retiradas indicadas — e com quatro itens
devolvidos à C0 para uma correcção limitada, não para reexecução.**

Fundamentação:

- **Não há paragem de linha.** Não rejeito nenhum facto de fundação. A geometria
  (G1, G2, G3, G20, G21, G22), a quarentena (G24) e a arbitragem das máscaras
  estão bem estabelecidas, e é isso que a **C1** precisa. A C1 pode arrancar
  hoje.
- **Retirar antes de passar:** G14 (para NÃO TESTÁVEL), a formulação causal do
  G13, a atribuição norte/sul do G18, a segunda metade do G9 («a janela lida
  corresponde à AOI»), e o número do G12 enquanto a sua sensibilidade — já
  calculada — não for reportada.
- **Reescrever com margem maior:** G7 (±0,03), G15 (±8 %, e «proporcional só no
  comprimento»), G2/G4 (±1,5 ha na área, e «copado vivo em 2026», não
  «exploração»), G16 (resíduo dentro da amostra, de composição desconhecida),
  G11 (6–9 ha, com a hipótese alternativa da dispersão de 2017 por excluir, e a
  segunda metade — «não é falha de copado» — marcada como leitura visual sem
  registo).
- **Corrigir por dever de forma:** acrescentar a coluna do instrumento
  independente; reportar as duas âncoras de NDVI que faltam; resolver a
  contradição entre «não abri nenhum PNG de saída» e os cinco factos que são
  leituras de PNG de saída; resolver a discrepância aritmética entre as áreas e
  as fracções do G11; retirar da M1 v2 os rótulos «válvulas 1–5 / B1 / 1,77 ha»
  e o «cerca de 1 km», que são prosa a viajar num mapa que sai para fora.
- **Bloqueio único, e é sobre a C2, não sobre a C1:** a **C2 não deve começar
  antes dos testes 1 e 2**. O teste 1 porque a C2 mede NDVI sobre ficheiros cuja
  ligação aos identificadores nunca foi verificada, e é a mesma premissa que
  criou o «b1». O teste 2 porque o facto central que a C2 vai herdar — o início
  do declínio ser anterior à série — depende de um número que está calculado, não
  está reportado, e pode inverter a conclusão. Ambos custam menos de dez minutos
  somados.
- **E antes da C2, a pergunta da secção 3 tem de ter dono:** delimitar pelo
  menos um polígono de controlo externo (o bloco sudoeste é o candidato óbvio, e
  a sua pertença à exploração é irrelevante para esta função — se não for da
  exploração, é ainda melhor controlo) e passá-lo para cima como geometria
  certificada. Sem isso, a C2 vai medir um declínio contra si próprio, que é a
  forma educada de dizer que não o vai medir.

Um certificado que resiste a isto vale muito. Este resiste na fundação — que é
onde interessa, e é onde a cadeia falhou da última vez.
