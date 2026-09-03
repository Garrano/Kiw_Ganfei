# Camada 3 — Biologia

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada C3 de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md` e depois `CONTROLOS.md` — os
controlos 1 e 2 aplicam-se-te por inteiro (o controlo 3, o adversário, só corre
em C0 e C2, portanto não levas adversário; escreve na mesma como se levasses).

A tua camada é a biologia: os 212 registos de laboratório, a sua
georreferenciação, os nemátodes, o «Kiwi 1000», as ITS e a qualidade de leitura,
os relatórios Becrop, e a *Rosellinia* de campo contra o negativo molecular.

**A razão de a biologia vir depois do sinal vegetal, e não antes.** A biologia
deste caso não decide nada isolada: doze resultados positivos sem padrão
espacial não distinguem coisa nenhuma — foi o que aconteceu com *M. hapla*,
positivo em todos os blocos amostrados. A biologia torna-se informativa quando
se pode perguntar «isto está onde o padrão está, ou está em todo o lado?». O
padrão está agora validado, e é isso que herdas.

## O que herdas — e só isto

Três listas fechadas, por esta ordem de precedência. Trata-as como dados, não as
revalides, e não uses nada que não esteja aqui.

### Da camada C0, ficheiro `CAMADA_0_REVISAO_R2.md` (que substitui o certificado C0)

**G1** AOI (529950, 4654600, 531950, 4655600), EPSG:32629, grelha de 10 m,
200×100. *(exacta)*

**G2** O polígono `pomar` tem **30,31 ha** e é a máscara geográfica derivada da
ortofoto por periodicidade de compasso (5,0 m). *(±10 m no contorno)*

**G3** Eixo do pomar: azimute **70,3°**, comprimento **1458 m**. *(medido por
dois caminhos)*

**G4** Áreas: `pomar` 30,31 ha · referência sistemática **1,10 ha / 110
células** · `zona0` 2,02 ha. **`manchaW` não existe como máscara.**

**G5** O conjunto operativo de máscaras é `sentinel\masks_geograficas.json`. O
antigo `masks.json` era circular e fica só como histórico.

**G16/G17 → substituídos pela G35.** **G19/G36** O bloco de ~16 ha a sudoeste é
o **B1**: válvulas 1 a 5, **9,01 ha**, entre E529500 N4654010 e E530054
N4654413, a **526 m** do corpo principal. Porta-enxerto **Summer Kiwi** nas
válvulas 2-5, sobre-enxertado com Enza Gold em 2016 e com Erica por volta de
2020; a válvula 1 e **todo o corpo principal** são pé franco de **Erica**. É o
único contraste de porta-enxerto do caso.

**G24** Quarentena da AOI 528400–529400: é tecido urbano de Valença.

**G26** **Não existe controlo externo de kiwi contemporâneo neste aluvião.**
Varrimento de ~3 km, 13 candidatos, 11 falsos positivos. Com dados de satélite
este caso não distingue «esta parcela declina» de «todo o kiwi deste aluvião fez
isto». Isto não é lacuna de busca; é resultado.

**G32** **Houve rede, e só no B1**, no período do Enza Gold. As datas de
instalação e remoção estão por dar.

**G34** Os focos identificam-se por **coordenada**. A nomenclatura esteve
invertida durante semanas.

| | FOCO OESTE | FOCO ESTE |
|---|---|---|
| centro | **E530485 N4655053** | **E530977 N4655117** |
| nome da exploração | **«Zona 0»** | por confirmar; o ajuste põe-no em B3 |
| bloco / válvulas | B2, válvulas **8** (a 35 m) e 9 (98 m) | B3, válvulas **13** (81 m) e **14** (93 m) |
| amostras | as **quatro ITS** (ISFBV0314–17) **e** o «Kiwi 1000» | só nemátodes (340/2026), as contagens **mais baixas** dos cinco blocos |

**É o foco OESTE que está mais amostrado, e é o ESTE que só tem contagens de
nemátodes.** A frase inversa circulou durante semanas e está morta.

**G35** As válvulas 6 a 17 estão colocadas por área acumulada. Banda contígua
**27,30 ha**; total da tabela 44,93 ha. **Posições em
`ganfei_s2\valvulas_por_area.json`** — e **as tabelas de válvulas do
`REGISTO_DE_NOMES.md` estão desactualizadas**, não as uses. Fora da banda
contígua, oito parcelas soltas (17,66 ha) têm área e **não têm posição**.

### Da camada C1, `CAMADA_1_CERTIFICADO.md`, secção PASSA PARA CIMA

**S3.** **O foco ESTE é o ponto alto e o foco OESTE o ponto baixo.** Cota
mediana: OESTE 6,638 m (percentil 30 do pomar), referência 6,798 m (38), ESTE
7,842 m (84). Diferença **+1,204 m**, confirmada por Copernicus GLO-30. *(±0,06 m)*

**S4.** É um **alto local**, não o efeito do declive geral: contra o perfil
longitudinal, o ESTE está +0,589 m acima e o OESTE −0,198 m abaixo. *(±0,10 m)*

**S5.** **Os focos não diferem em inclinação.** Declive de forma a 50 m: 0,336°,
0,406° e 0,427°, p = 0,20. Toda a parcela abaixo de 0,5°. **Qualquer afirmação
de «encosta» é falsa.** *(p declarado)*

**S6.** **A posição hidráulica dos dois focos é oposta.** Altura sobre a
drenagem: OESTE 0,130 m, referência 0,150 m, ESTE 0,353 m. Distância à
drenagem: **13,4 / 23,6 / 55,8 m**. Fracção sobre linha de drenagem: 1,99 % /
1,01 % / 0,33 %. **O foco OESTE recebe água concentrada; o ESTE não recebe
nenhuma.** *(limiar declarado)*

**S8.** **O bloco do foco ESTE (B3, válvulas 12-15) tem o solo mais pobre da
exploração**: CaO < 154 mg/kg (abaixo da detecção), MgO 36,0, K₂O 74,7, P₂O₅
107, C:N 5,9, pH 5,6 — mínimo de nove boletins em cinco de sete parâmetros. Os
vizinhos imediatos são muito mais ricos: `Erica Novo` (válvulas 10-11) CaO 879 e
1200; `B4` (válvulas 16-17) CaO 1100. **É um buraco, não um gradiente.** *(n = 1
boletim — ver S9)*

**S9.** **Um boletim não caracteriza um bloco.** Dentro do B1, três sub-parcelas
dão CaO **314, 439 e 4700** mg/kg. O mesmo `B2 - V7`, a três meses de distância,
dá 264 e 505 **e texturas diferentes** («Franca» / «Argilosa»). **Nenhuma
diferença química entre blocos abaixo de um factor de 2 é interpretável com
estes dados.** *(declarado)*

**S10.** **O bloco do foco OESTE está confirmadamente carente de cálcio, por
duas matrizes.** Solo em `B2 - V7` (a 111 m do foco): CaO 264 e 505 mg/kg.
Folha do mesmo bloco, Junho/2026: **Ca 2,2 % contra referência 3–4,7 %,
«Baixo»**. **Não existe análise foliar para o B3.** *(leitura directa)*

**S12.** **O chão lavrado de 2021 (1,67 ha) está 60 % dentro do foco ESTE e 0 %
no foco OESTE e na referência.** 45,0 % do polígono `zona0` é chão lavrado.
*(±1 célula)*

**S13.** **A distinção física daquele chão é anterior a 2021.** Em VV de
Sentinel-1 está 1,2 a 3,5 dB abaixo da referência em **todos os dez Invernos
desde 2016-17**. **A lavra de 2021 não criou o contraste.** *(±0,3 dB)*

**S15.** **No radar, o foco ESTE está sempre abaixo da referência e o foco OESTE
nunca esteve — até ao Inverno de 2025-26**, em que cai para −1,107 dB (órbita
125) e −0,775 dB (órbita 147), o maior desvio da série, enquanto o pomar inteiro
está no seu menor desvio. *(±0,25 dB)*

**S16.** **A precipitação é inútil como discriminante espacial.** Nenhum produto
disponível resolve 496 m. Inverno mais seco 2021-22 (663,6 mm); mais húmidos
2022-23 (1809,3) e 2023-24 (1807,8). *(±25 mm)*

**S17.** **A linha térmica fica retirada.** O acoplamento ΔT–ΔNDVI é **−0,925 no
controlo interno fora do pomar** — é genérico da superfície. O «r = −0,756» que
circula é o Spearman do foco ESTE sozinho. **Não ressuscitar sem LST nocturno ou
temperatura de solo medida.** *(r declarado)*

**S18.** **O pomar é duas vezes mais plano que o envolvente** (0,0355 m contra
0,0703 m de resíduo de plano a 60 m, p = 3,2e-10). Compatível com terraplanagem
de emparcelamento; **não é prova**, e a truncatura de horizontes continua por
medir. *(±0,01 m)*

**S19.** **A rugosidade a 25 m do foco ESTE excede a referência dentro da mesma
campanha de voo** (+0,0379 m, p = 1,3e-18); a do OESTE não (+0,0016 m,
p = 0,058). *(±0,008 m)*

**S20. Síntese da C1: os dois focos têm substratos opostos em todas as variáveis
que os separam.** O ESTE é alto, afastado da drenagem, sem escoamento a
chegar-lhe, com o solo mais pobre em bases da exploração, o micro-relevo mais
rugoso, retrodifusão de Inverno permanentemente baixa desde 2016, e 40 % da área
lavrada em 2021 sobre terreno que já era distinto antes disso. O OESTE é baixo,
sobre linhas de drenagem, com o dobro da água concentrada da referência,
indistinguível dela em terreno, rugosidade e radar durante nove Invernos.
**Não há uma única variável de substrato em que os dois focos se pareçam.**
*(consequência de S3–S6, S8, S12–S15, S19)*

### Da camada C2, `CAMADA_2_CERTIFICADO.md`, secção PASSA PARA CIMA

**V1.** O défice define-se como **NDVI abaixo da referência sistemática da
própria data menos 0,05, com abertura 2×2**. A série de plena estação tem **dez**
cenas (as nove anteriores mais 2019-09-02). *(exacta)*

**V2. O acontecimento é de 2025-2026 e atinge os dois focos ao mesmo tempo e na
mesma medida.** Contra o patamar de 2017-2024, o NDVI dá um degrau de **−0,1426
no foco OESTE** e **−0,1439 na parte plantada do foco ESTE**, contra **−0,0204**
no resto do pomar. Até 2024 nenhum dos dois focos tem tendência significativa.
**A frase «o foco ESTE declina desde 2020» é falsa para plantas.** *(±0,01 NDVI;
o degrau do foco ESTE é de um só instrumento — ver adiante)*

**V3. NDVI e SAR datam o mesmo acontecimento nos mesmos sítios.** Sobre 81
mosaicos de 60 m definidos por geometria pura, a queda de NDVI 2024→2026
correlaciona com a anomalia de VV do Inverno de 2025-26 a **ρ = +0,57 a +0,60**
(permutação p < 0,0002). Nos nove Invernos anteriores ρ ∈ [−0,22, +0,31]; três
placebos de NDVI dão −0,05, +0,27, +0,11. **Retirando os mosaicos a menos de
130 m dos dois focos, sobrevive: ρ = +0,429, p = 0,0010.** *(ρ e p declarados)*

**V4. A válvula 8 destaca-se sozinha, nos dois instrumentos.** Sobre a partição
das doze posições de `valvulas_por_area.json`, a v8 tem a maior anomalia
negativa de VV do Inverno de 2025-26 (**−0,660 dB**, contra −0,135 da segunda) e
a maior queda de NDVI 2024→2026 (**−0,0822**). *(±10 m sobre a G35)*

**V5. Os 8,08 ha em défice de 2017 e os 7,86 ha de 2026 não são o mesmo
objecto.** Ao limiar 0,25 são **5,37 e 0,32 ha**; IoU entre os dois mapas
**0,29**. **O acontecimento de 2025-2026 é extenso e moderado: acrescenta muita
área a profundidade média e nenhuma a profundidade grave.** Não uses 2017 como
linha de base de saúde. *(±1 célula)*

**V6. Pelo menos 5,37 ha do polígono `pomar` (18 %) foram plantados depois de
2012.** Não têm assinatura de pérgola nas ortofotos de 2010 nem de 2012
(p = 7e-59 e 2e-61) e têm-na em 2021; o NDVI vai de 0,498 em Julho de 2017 a
0,753 treze meses depois. **O pomar tem pelo menos duas idades de plantação
separadas por nove anos ou mais**, e a mais nova está a **E530600–530800**,
entre os dois focos. *(a data exacta de plantação está por dar)*

**V7. O chão lavrado de 2021 já estava despido em 2017**, no óptico: 166 das 167
células (99 %) em défice na cena de 2017, contra 27 % do pomar. Estende ao
óptico, e recua a 2017, a datação negativa que a C1 fez por radar (S13). *(±1
célula)*

**V8. 3,58 ha passam a regra M2 — declínio novo sobre terreno comprovadamente
são.** Das 7,86 ha em défice em 2026, 3,58 ha nunca estiveram em défice em
nenhuma das oito cenas de 2017-2024 (2,60 ha no critério duro). Repartem-se em
**2,02 ha a 24 m do foco OESTE** e **1,41 ha em três manchas a 62, 72 e 167 m do
foco ESTE**. **É esta a área sobre a qual faz sentido perguntar por uma causa
recente**; as outras 4,28 ha têm história anterior. *(±0,15 ha)*

**V9. A grandeza operativa é a magnitude, não a fracção** — a fracção do disco
ESTE vai de 54 % a 94 % com a magnitude constante. Reporta sempre a magnitude
**com o nível absoluto ao lado**. *(exacta)*

**V10. O nível absoluto não pode carregar uma afirmação sobre o pomar todo.** As
duas cenas de NDVI mais baixo da série são as duas únicas do S2C e o degrau
delas aparece igualmente fora do pomar. Corrigida por um alvo estável externo, a
descida da referência é **−0,0028/ano, p = 0,16** — não significativa. *(±0,01
NDVI)*

**V11. A barra de erro da série é ~3 ha, e vem medida.** Entre 2018-08-31 e
2019-09-02 — dois dias de dia-do-ano — o défice varia **3,13 ha**. O salto de
2024 (2,91) para 2026 (7,86) é de 4,95 ha e sobrevive; nenhum degrau isolado do
patamar de 2019-2024 sobrevive. **A fenologia não é a explicação:** 58 dias
medidos dentro de 2025 valem −0,39 ha. *(±0,4 ha)*

## O que ficou por resolver abaixo de ti

Cada uma destas afecta-te directamente. Não as resolvas por suposição.

1. **A queda do foco ESTE em 2025-2026 é de um só instrumento** (C2). O radar de
   Inverno positivamente não a vê: as válvulas do B3 têm anomalias de VV
   **positivas** nesse Inverno. Não é refutação — o kiwi é caduco e o VV de
   Inverno mede solo, pérgola e lenho — mas **se a tua camada tiver qualquer
   observação datada no foco ESTE, ela vale muito**, porque é o segundo
   instrumento que falta.
2. **Um boletim não caracteriza um bloco** (C1 S9). Factor 15 dentro do B1,
   factor 2 e mudança de textura no mesmo ponto a três meses. **Não construas
   contraste químico entre blocos com n = 1.**
3. **Nenhum ponto do B1 tem posição** (R2 G35/G36): dentro dele não se sabe onde
   acaba cada válvula, incluindo a fronteira do porta-enxerto. Os três boletins
   do B1 ficam com a posição de conjunto e um raio de incerteza de **343 m**.
4. **`Erica 2016 R/E` é o mesmo bloco que `Erica Novo`?** É inferência, não
   prova. Se estiver errada, dois dos nove boletins mudam de sítio.
5. **`Parcela B4`: onde foi colhido?** B4 tem válvulas 16-17 na banda contígua
   **e** a parcela solta B4C3, sem posição.
6. **Não existe controlo externo de kiwi contemporâneo** (G26). Um positivo sem
   um negativo comparável não é discriminante.
7. **Não há data de plantação** para as 5,37 ha novas (V6). Se alguma amostra
   vier de lá, a interpretação muda: planta de 10 anos não é planta de 25.

## O que foi rejeitado, e não podes usar

Isto é tão importante como o que passa. Impede que um facto morto volte a entrar
pela porta do lado.

- **`lidar\bacia.json`** (C1). Produzido sem `resolve_flats`; a acumulação
  máxima fica 70 vezes menor que a real.
- **A leitura «a lavra de 2021 mudou aquele solo»** (C1). A assinatura já lá
  estava em 2016-17 no radar e em 2017 no óptico.
- **A linha térmica como sinal independente** (C1 S17). Não a ressuscites.
- **«O foco ESTE está numa encosta»** (C1). Não está: 0,427° de declive de
  forma.
- **Qualquer série do B1, e qualquer comparação de nível de NDVI entre o B1 e o
  corpo principal** (R2). Três tentativas, três contaminações: invólucro do
  controlo, rede a entrar e a sair, e duas sobre-enxertias.
- **Comparação de brilho de ortofotos entre épocas** (R2 G13/G37) — e agora
  também **dentro** de uma só época (C2): o NDVI da ortofoto de 2025 dá 0,09
  sobre copado fechado e a ordenação das unidades está invertida face ao
  Sentinel-2 (ρ = −0,62). **Nenhuma percentagem de cobertura tirada de ortofoto
  é utilizável.** O que sobrevive da ortofoto é a estrutura (periodicidade de
  pérgola), não o nível.
- **A curva em U do défice como objecto único**, e 2017 como linha de base de
  saúde (C2 V5).
- **«O foco ESTE declina desde 2020»** enquanto afirmação sobre plantas (C2 V2).
  O que existe ali desde antes da série é chão sem copado.
- **A taxa de −0,0150/ano da parte plantada do foco ESTE** como taxa de declínio
  (C2). O número existe, mas o modelo linear perde 4,35 : 1 contra um degrau; não
  há nenhum ano em que aquela unidade tenha caído 0,015.

## Materiais

Só estes. Os ficheiros de padrão espacial estão listados porque a tua pergunta
central é de sobreposição, não porque os devas reanalisar.

**Da tua camada:**

```
Downloads\Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx
    README                       25 linhas   convenções e avisos do próprio livro
    Master Log                  212 registos  Record_ID, Source_File, Doc_Type,
                                 Report_No, Client_Titular, Terrain_Block_Parcel,
                                 Parish_Municipality, Parcelario_No, Sample_Date,
                                 Received_Date, Result_Date, Matrix, Test_Category,
                                 Method, Organism_Parameter, Result, Value, Unit,
                                 Interpretation, Lab_Provider, Location_Confidence,
                                 Notes
    Pathology Matrix             26 organismos × 8 colunas de amostra, incluindo
                                 uma coluna «UNSPECIFIED — composite/bulk»
    Nematode Counts               B1, B3, B4 · solo (J2+ovos/200 cc) e raiz (/g)
    Soil Chemistry by Block      11 boletins
    ITS Diversity                 ISFBV0314–0317: leituras totais/filtradas,
                                 riqueza de ASV, equitabilidade de Pielou
    Becrop Reports                2 relatórios (Ago/2023 e Jan/2024)
    Drone-NDVI Log                3 capturas de ecrã da plataforma Becrop
    Traceability Gaps             o que o próprio livro assinala como por resolver
Downloads\Dossie_Rastreabilidade_Declinio_Kiwi_Ganfei_PT.xlsx
    a versão portuguesa do mesmo livro, com 222 linhas no «Registo Principal»
    contra 212 no «Master Log» — a diferença NÃO está explicada e é a primeira
    coisa a verificar
```

**Para relacionar com o padrão (lê, não recalcules):**

```
Downloads\ganfei_s2\valvulas_por_area.json          posições das válvulas 6-17
Downloads\ganfei_s2\sentinel\masks_geograficas.json máscaras operativas
Downloads\_VALIDACAO_CAMADAS\SAIDA_C2\c2_05_novo_m2.npy
    booleano 100×200 na grelha da G1: as 3,58 ha de declínio novo da V8
Downloads\_VALIDACAO_CAMADAS\SAIDA_C2\c2_05_defice_2026.npy
    booleano 100×200: o mapa de défice de 2026 (7,86 ha)
Downloads\_VALIDACAO_CAMADAS\SAIDA_C2\c2_00_comum.py
    grelha, centros de célula, discos dos focos — usa estas funções
Downloads\_VALIDACAO_CAMADAS\SAIDA_C1\c1_06_solo_colocado.csv
    os nove boletins A2 já ligados a posição, com grau de confiança
```

**Não abras `ganfei_s2\_pacote_cowork\`.** Contém figuras e notas de camadas
acima da tua (matriz de diagnóstico, livro-razão de exclusões, árvore de
decisão). Ver essas conclusões antes de fazeres o teu trabalho contamina-o.

## Tarefas

1. **Reconciliar os dois livros.** `Master Log` tem 212 registos e `Registo
   Principal` tem 222. Diz quantos registos há de facto, quais são os dez a mais
   ou a menos, e qual dos dois é a fonte. Enquanto isto não estiver resolvido,
   nenhuma contagem de resultados é citável.

2. **Georreferenciar o que for georreferenciável, e dizer o que não é.** Para
   cada registo do `Master Log`, usando `Terrain_Block_Parcel` e a coluna
   `Location_Confidence` contra `valvulas_por_area.json`: dá-lhe uma posição na
   banda contígua, ou declara-o sem posição. **Reporta a contagem dos dois
   grupos.** Lembra-te de que 17,66 ha (oito parcelas soltas) e todo o B1 não
   têm posição — não lhes inventes uma.

3. **A pergunta central da tua camada: os positivos estão onde o padrão está?**
   Para cada organismo da `Pathology Matrix` e para as contagens de
   `Nematode Counts`, cruza a posição da amostra com os dois booleanos de
   `SAIDA_C2\` (o défice de 2026 e as 3,58 ha de declínio novo) e com os dois
   focos por coordenada. **A resposta que interessa é uma de três: «está onde o
   padrão está», «está em todo o lado», ou «não tem posição para se poder
   dizer».** Diz qual delas, organismo a organismo. Não faças a pergunta ao
   contrário — não procures o organismo que explica o padrão.

4. **A discrepância da amostragem, e o que ela vale.** O foco OESTE tem as
   quatro ITS e o «Kiwi 1000»; o foco ESTE tem só contagens de nemátodes, e são
   **as mais baixas dos cinco blocos** (28 no solo, 37 na raiz, contra 250/65 no
   B1 e 46/156 no B4). Os dois focos caem juntos em 2025-2026 (V2). Diz o que
   esta assimetria de esforço permite e o que impede.

5. **O «Kiwi 1000».** A folha `Traceability Gaps` diz que a amostra a granel não
   é atribuível a um bloco. Localiza tudo o que o livro diz sobre ela e conclui
   se pode ou não ser posta no mapa. Se não puder, **todos os organismos que só
   aparecem nessa coluna ficam sem posição**, e isso tem de ser dito no
   certificado, não em nota de rodapé.

6. **A qualidade de leitura das ITS.** As quatro amostras dão 29 %, 3 %, 4 % e
   10 % de leituras filtradas sobre totais. Diz se as quatro são comparáveis
   entre si, e se a riqueza de ASV (281, 171, 129, 219) é interpretável com
   profundidades de leitura tão diferentes. Se não for, a diversidade não entra
   em nenhuma conclusão.

7. **A *Rosellinia* de campo contra o negativo molecular.** Os registos 2 e
   seguintes do `Master Log` marcam «POSITIVE (macroscopic ID only)» com uma nota
   de contradição molecular posterior, e a `Traceability Gaps` assinala que as
   datas de amostra são diferentes. Estabelece o que está estabelecido: houve
   duas amostras ou uma? De que data cada uma? O negativo molecular é da mesma
   planta?

8. **A contaminação do caso Kiwi Atlántico e a válvula 27.** Localiza no livro
   todos os registos que não são desta exploração ou cuja proveniência é dúbia,
   e retira-os das contagens. Diz quantos são. Uma válvula 27 não existe na
   tabela do gestor, que vai da 1 à 17.

9. **Os relatórios Becrop.** Dois relatórios, Ago/2023 e Jan/2024, com 856 e 720
   espécies e pontuações de «biosostenibilidad» de 41 e 82. Diz se as duas datas
   são comparáveis entre si (época, matriz, método) e o que a diferença de
   pontuação mede. Se não forem comparáveis, di-lo — é resultado.

10. **Se tudo isto te deixar sem discriminante, di-lo.** «A biologia disponível
    não distingue os dois focos» é uma saída válida e obrigatória se for o caso.
    O protocolo trata a dúvida assinalada como resultado; um facto inventado
    destrói a cadeia inteira.

## Onde já se errou nesta matéria

- **Nomes de focos trocados.** Durante semanas «Zona 0» significou dois sítios a
  500 m um do outro, conforme quem escrevia. Por isso os focos se identificam
  por coordenada. Se encontrares «Zona 0» num ficheiro, traduz e **declara a
  tradução no teu script**, como a C1 e a C2 fizeram.
- **Tabelas de válvulas desactualizadas.** O `REGISTO_DE_NOMES.md` e
  `valvulas_v6.json` dão posições que a G35 substituiu. Usa
  `valvulas_por_area.json` e mais nada.
- **Um positivo tratado como discriminante.** *M. hapla* deu positivo em todos
  os blocos amostrados e chegou a ser tratado como achado. Um organismo presente
  em todo o lado não distingue nada, e o caso já perdeu tempo com isso.
- **Um patogénio atribuído ao corpo em declínio sem posição.** Aconteceu com
  *P. sojae*. A coluna `Location_Confidence` existe precisamente para isto:
  respeita-a.
- **Uma máscara derivada do sinal que se ia medir.** Foi o erro central de todo
  o processo e passou por quatro auditorias. O equivalente na tua camada seria
  escolher as amostras a analisar por elas estarem onde o padrão está e depois
  concluir que o padrão e a biologia coincidem. Não o faças; e se a amostragem
  original o fez, **isso é um achado teu e tem de ir para o certificado**.

## O que entregar

1. `CAMADA_3_CERTIFICADO.md`, com as cinco secções do protocolo — CONFIRMADO,
   CORRIGIDO, REJEITADO, NÃO TESTÁVEL, PASSA PARA CIMA. A secção PASSA PARA CIMA
   é uma **lista fechada**: sê avaro. Cada facto leva o ficheiro e o cálculo que
   o prova, o **instrumento independente** que o confirma (controlo 1) e a
   margem.
2. `CAMADA_4_PROMPT.md` (inferência), seguindo `MODELO_PROMPT.md`.
3. Código em `SAIDA_C3\`.

Reporta as **quantidades-âncora** do `CONTROLOS.md` mais as que as camadas
abaixo fixaram: `pomar` 30,31 ha, referência sistemática 1,10 ha / 110 células,
banda contígua 27,30 ha, total da tabela 44,93 ha, chão lavrado 1,67 ha, défice
de 2026 7,86 ha, declínio novo pela regra M2 3,58 ha. E acrescenta as tuas:
número de registos, número de registos com posição, número de organismos
distintos.

**Não teorizes acima da tua camada.** Não escrevas diagnóstico diferencial, não
excluas causas, não proponhas etiologia — isso é C4. Se um resultado te sugerir
uma causa, guarda-a: escrevê-la contamina quem vier a seguir.

**Não modifiques nada em `Downloads\ganfei_s2\`.**

Se rejeitares um facto herdado, **pára** e devolve. Não construas por cima.
