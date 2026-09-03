# O parcelário IFAP, o Landsat e o plástico branco

29-08-2026.

---

## 1 · O parcelário — e porque não é uma medição nossa

Fonte: WFS do **AgroDigital da CCDR-N** (`IfapWfsProxy.ashx`), camadas
`parcelas.2025jun10` e `culturas.2025jun10` — campanha de **2025**, retrato de
**10 de Junho de 2025**. Endereço indicado pelo gestor.

**Isto é um documento, não sensoriamento remoto.** É o que o beneficiário
declarou e a administração aceitou. Entra no dossiê como **facto de tipo 1 —
testemunho**, e o seu modo de falha não é ruído de sensor: é desfasamento entre
o **declarado** e o **instalado**.

Beneficiário: **ENT_ID 472062**, 18 parcelas, 49,76 ha de área de parcela,
49,30 ha de cultura declarada.

### 1.1 · O total bate com a tabela do gestor

| | ha de kiwi |
|---|---|
| **declarado ao IFAP, campanha 2025** | **44,36** |
| **tabela de válvulas do gestor** | **44,93** |
| diferença | 0,57 ha — **1,3 %** |

Dois documentos independentes — um interno da exploração, outro entregue ao
Estado — a 1,3 % um do outro. É a validação externa mais forte que a geometria
deste caso alguma vez teve.

**Método, e o erro que quase cometi.** À primeira associei cada polígono de
cultura à parcela de centróide mais próximo dentro de 250 m; isso somou 88,73
ha de culturas a parcelas que totalizam 49,76 — estava a apanhar polígonos de
vizinhos. Refeito por **contenção geométrica** (mais de 50 % da área do
polígono dentro da parcela), dá 49,30 ha, coerente com a área das parcelas.
O total de kiwi não mudou; os outros mudaram todos.

### 1.2 · O B1 deixa de estar sem documento

A cadeia tinha o B1 como «inteiramente fora da extensão dos rasters
fornecidos», e os três analistas independentes disseram o mesmo. Continua fora
do raster — mas já não está por documentar.

Quatro parcelas a sudoeste, entre E529592 e E529864, N4653920 e N4654362:

| parcela | centro | kiwi |
|---|---|---|
| 1575632754001 | E529592 N4653920 | 1,27 ha |
| 1575639735008 | E529681 N4654053 | 3,10 ha |
| 1575639735003 | E529756 N4654163 | 2,50 ha |
| 1585631057002 | E529864 N4654362 | 5,76 ha |
| | **total** | **12,63 ha** |

A tabela do gestor dá ao B1 as válvulas 1-5 (9,01 ha) mais B1C5 e B1C6
(4,00 ha) = **13,01 ha**. Diferença de **2,9 %**. E as coordenadas caem dentro
do segmento que o gestor deu de memória: de E529500 N4654010 a E530054
N4654413.

### 1.3 · O documento confirma o LiDAR, unidade a unidade

| unidade | ha | % declarada KIWI | % sem declaração |
|---|---|---|---|
| polígono do pomar | 30,31 | **95,2 %** | 2,5 % |
| referência sistemática | 1,10 | **100,0 %** | 0 % |
| **com pérgola (LiDAR)** | 26,54 | **99,4 %** | 0,3 % |
| **SEM pérgola (LiDAR)** | 3,77 | **65,0 %** | **18,3 %** |
| N1 foco OESTE | 1,52 | 100,0 % | 0 % |
| N3 leste | 1,43 | 90,2 % | 9,1 % |

**Todas as declarações de cultura anual dentro do nosso polígono caem na zona
sem pérgola**: consociações forrageiras 0,38 ha, prados temporários 0,14,
azevém 0,07, aveia 0,02, milho 0,02 — mais 0,69 ha sem declaração nenhuma.

Onde o LiDAR não vê pérgola, o beneficiário declarou erva, forragem ou nada.
**Um instrumento geométrico e um documento administrativo, sem contacto entre
si, a marcar o mesmo terreno.**

### 1.4 · A discordância, que é o achado

**O N3 está declarado KIWI (90,2 %, 1,29 ha) a 10 de Junho de 2025.**
**Três semanas depois, a 6 de Julho de 2025, o LiDAR mede-lhe 0,27 m.**

Declarado e instalado divergem. As leituras possíveis:

- **replantação** — kiwi novo, legitimamente declarado, ainda sem dois metros.
  É a que a amplitude sazonal sustenta: **0,10 em 2025** (não folia) e **0,65
  em 2026** (volta a foliar). Videira jovem.
- desfasamento entre a declaração e o terreno.

**A primeira é coerente com tudo o resto e a segunda não explica o regresso da
amplitude em 2026.** Mas nenhuma se decide daqui: **pergunta-se ao gestor a
data da replantação do N3.** É facto de tipo 1 e corrige-se perguntando.

---

## 2 · Landsat 8/9 — a medição óptica independente que a C2 pediu

140 cenas, **2013-2026**. Outra agência, outro sensor, outra correcção
atmosférica, outra hora de passagem. Imune por construção ao viés do S2C.

Fosso à referência, **NDVI**:

| | 2013-2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| OESTE com pérgola | −0,004 a +0,004 | 0,004 | **0,046** | **0,146** |
| ESTE com pérgola | 0,036 a 0,070 | **0,074** | **0,100** | **0,138** |
| ESTE sem pérgola | 0,058 a 0,313, sem tendência | 0,218 | 0,204 | 0,163 |
| resto do pomar | 0,023 → 0,001 | 0,001 | 0,001 | −0,004 |

**Onze anos com o foco OESTE indistinguível da referência.** O leste desloca-se
**um ano antes** do oeste.

E uma grandeza que esta cadeia nunca mediu — **NDMI**, água no copado, da banda
SWIR:

| fosso NDMI | 2024 | 2025 | 2026 |
|---|---|---|---|
| OESTE com pérgola | 0,004 | 0,055 | **0,199** |
| ESTE com pérgola | 0,090 | 0,124 | **0,201** |

**Os dois focos perdem mais água do que verdura** (0,199 contra 0,146; 0,201
contra 0,138). Desfolha simples moveria os dois na mesma proporção. Perder mais
água do que folha aponta para problema hidráulico ou vascular.

**Ressalva:** o fosso do OESTE em ~0,000 durante onze anos é em parte
**saturação** do NDVI sobre copado fechado. A linha de base vale como «era
indistinguível», não como «não havia variação pequena».

---

## 3 · O plástico branco tem nome

**Cobertura reflectora de solo** — Extenday e congéneres, prática corrente em
kiwi. A literatura estabelece:

- a luz reflectida dentro do copado é **cinco vezes maior** com filme
  reflector do que sem;
- na entrelinha, a luz acima de erva é **20 a 40 % menor** do que acima de
  filme;
- rendimento até **+13 %** em kiwi;
- maturação antecipada até **10 dias** na fruta do copado inferior.

Referências: [Acta Hort. 610_17](https://www.actahort.org/books/610/610_17.htm) ·
[ISHS 1332_55](https://ishs.org/ishs-article/1332_55/) ·
[Harvesting light with reflective ground covers](https://www.researchgate.net/publication/283859933_Harvesting_light_in_persimmon_and_kiwifruit_orchards_with_reflective_ground_covers)

**Consequência para o caso:** é uma **intensificação de gestão**, não um
sintoma. Mas entra na conjuntura, e a sua data é desconhecida — não aparece em
2021 e aparece em 2025. **Pergunta ao gestor.**

### 3.1 · A data da ortofoto de 2025, e uma retirada que se mantém

Registo SNIG da campanha ORTOS-2025: **Lote 1 voado de 31/03/2025 a
26/07/2025** (câmara Vexcel UltraCam Eagle M4-f90).

Testei se a C2 tinha retirado a G14 por premissa errada — se o NDVI da
ortofoto dava 0,09 por o pomar estar sem folha, e não por avaria. **Não. A C2
tinha razão.** O controlo que decide é a água:

| NDVI da própria ortofoto | mata NO | mata SE | mata S | **rio Minho** | pomar |
|---|---|---|---|---|---|
| 2021 | 0,312 | 0,083 | 0,182 | **+0,314** | 0,309 |
| 2025 | 0,241 | 0,336 | 0,372 | **+0,187** | 0,097 |

**O rio lê NDVI positivo nas duas épocas.** Água não pode. O instrumento falha
o seu próprio controlo e a retirada da G14 mantém-se por inteiro.

**A data resolve-se por outro caminho:** o LiDAR de 06-07-2025 mede 2,32 m e
99,2 % de cobertura no pomar. Se a ortofoto fosse de Julho, o pomar apareceria
fechado. Aparece com fileiras abertas. Logo é **da parte inicial da janela —
Primavera de 2025** — deduzido de um instrumento independente, não da imagem
suspeita.

---

## 4 · Perguntas ao gestor que saem daqui

1. **Data da replantação do N3** (E531068 N4655145) e das restantes áreas
   limpas a leste.
2. **Que material é a cobertura clara ao longo das fileiras, e quando foi
   instalada.**
3. Confirmação de que a exploração é o ENT_ID 472062 e de que as 18 parcelas
   são todas.

---

## Ficheiros

```
landsat_independente.py   140 cenas Landsat 8/9, NDVI e NDMI, 2013-2026
landsat.json              a serie, cena a cena
ifap_cruzamento.py        parcelario contra as mascaras do LiDAR
ifap_cruzamento.json      ifap_cultura.npy
ifap_exploracao_total.json  as 18 parcelas do ENT 472062, por cultura
data_da_orto.py           o controlo de agua que mantem a retirada da G14
```
