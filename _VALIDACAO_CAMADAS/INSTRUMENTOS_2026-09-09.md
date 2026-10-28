# Instrumentos · o que está validado, e o que falta construir

**09-09-2026.** Inventário do que este processo pode usar, do terreno à biologia,
com o estatuto real de cada instrumento — não o pretendido. Estatuto por
`estatuto.py`; auditorias em `AUDITORIAS.csv`; contagens por
`indice_inteligencia.py`.

**Regra que governa a tabela:** um instrumento só é **CITÁVEL** se passou pela
certificação *e* por adversário independente. Um instrumento sem estatuto não é
falso — é de estatuto desconhecido, e para efeitos de citação dá no mesmo.

---

## 0 · Três factos de tipo 1 entrados hoje, e o que movem

1. **A primeira mancha a aparecer foi a mais oriental** — B3, válvulas 12-15.
   `DEC-06` fecha nesse sentido. **Consequência de vocabulário, e é séria:** o
   gestor chama «Zona 0» às válvulas 8, 9 e 10, que são a mancha **ocidental**.
   Logo **«Zona 0» e «origem» não são a mesma coisa neste processo**, e nenhuma
   peça pode usá-los como sinónimos. O §10 do enquadramento assume que são.
2. **A amostra de raiz retida não existe** (`DEC-07`). O `§9` chamava-lhe *«o
   activo físico de maior prioridade do caso»*. Sem ela, **toda a confirmação
   biológica passa a depender de colheita nova** — o plano de amostragem sobe de
   «útil» a **único caminho**.
3. **As covas de perfil abrem-se durante a ida ao terreno** (`DEC-08`), no mesmo
   ponto onde se colhe raiz e solo — o que permite cruzar o factor abiótico com
   o biótico planta a planta, coisa que nenhuma campanha anterior fez.

---

## 1 · O que está CERTIFICADO **e** AUDITADO — usável sem ressalva

| instrumento | o que mede | estatuto |
|---|---|---|
| **Altura de copado por LiDAR** (`altura_copado.py`, `chm_altura.npy`) | geometria: MDS−MDT, limiar 0,5 m, voo único de 06-07-2025 | **CITÁVEL** — certificado (CAMADA_2/4) e atacado (AUD-17); reproduzido dos ladrilhos brutos a **0,000e+00** |
| **Partição por sector** (carta do gestor) | que válvula pertence a que talhão; 44,9 ha | **TIPO 1** — testemunho, AUD-18. Não precisa de certificado |
| **Escala do esquema de rega** | 1,2572 m/px no raster embebido; 1:3500 @ A1 | **CITÁVEL** — AUD-19, três medições independentes dentro de ±1,1 % |
| **Série NDVI Sentinel-2 no foco ORIENTAL** (`c2_01/02/03`, `c1_14`) | vigor estival, polígono fixo | **PARCIAL, e limpo do lado que interessa** — AUD-10: reproduzem o disco exactamente e **o foco oriental é limpo**. É o foco que hoje sabemos ser a origem |
| **Perda de copado 2024→2025** | 2,20 ha; B3 1,02 · B2 0,33 · Erica Novo 0,01 | **CITÁVEL** — AUD-17 |

**São cinco.** De 191 guiões vivos, **45 são citáveis (24 %)**.

## 2 · O que está auditado mas com ressalva que viaja com o número

| instrumento | ressalva |
|---|---|
| **Família de máscaras** | AUD-09: a `saudavel` é limpa; o `pomar` (22,3 %) foi definido por ortofoto **posterior**; a `zona0` não tem produtor em código — e agora sabe-se que **está no foco oriental**, ou seja na origem |
| **Série NDVI no foco OCIDENTAL** | AUD-10: o centro está no percentil **0,17 de 2421 candidatos** — a **magnitude ocidental não é estimável**. Serve para dizer *que há mancha*, não *quanto* |
| **Piso óptico de Inverno** | a medição aguenta-se; **a inferência não** — uma pérgola sem copado deixa de dar sombra e a erva verdeja. Não persiste (+0,291 → −0,078) |
| **Boletins A2 de solo** | oito talhões, doze parâmetros de fertilidade. **Faltam CTC e saturação em bases; a profundidade é NÃO SABIDA.** Piso de ruído medido: 0,2 unidades de pH e mudança de classe textural entre duas datas no mesmo talhão |

## 3 · O que está fechado como não-instrumento

- **SAR** — `DEC-03`. NÃO TESTÁVEL para declínio-contra-arranque: o efeito
  detectável excede o tecto de contraste de copado nas seis células. Falta de
  potência, não resultado negativo.
- **B1 como comparador** — `DEC-04`. Cortado à base e reenxertado duas vezes.
  **Mata a COMP-01 e deixa o processo sem controlo interno.**
- **Posição individual das válvulas** — `DEC-01` + IX-21. Duas reconstruções
  divergem até 398 m. Ao nível do **sector** está fixado; ao nível da **válvula**
  não existe.
- **Landsat** — 5 guiões vivos, **0 citáveis**; AUD-03 inverteu a conclusão.

## 4 · O buraco que mais custa

> **Ortofoto: 14 guiões vivos, ZERO citáveis.**

É o único instrumento que vê **estrutura** — fiadas, postes, arames — e portanto
o único que poderia separar *arranque* de *declínio* sem ir ao terreno. O
`p1_pergola_oriental_2025.py` tentou e **falhou o critério de âncoras do próprio
portão**: em 2025 o chão lavrado lê prominência 0,240, porque os regos também
são periódicos. `AF-06` continua pretendida.

E as leituras que existem são de **um só leitor**, sem guarda mecânica — a forma
G, a única das oito que continua sem cobertura executável.

---

## 5 · O que construir, do terreno à biologia

Por ordem de valor, e cada um com o que decide.

### T1 · Mapa de pontos de colheita — margem em avanço e par assintomático
**O único caminho que resta para a biologia** (`DEC-07`), e o que o utilizador
pediu: *«ideia exacta dos locais onde compensa colectar»*.

Produz, por mancha: pontos na **margem em avanço** — células com copado no ano
*t*−1 e sem copado em *t*, na fronteira com copado vivo — e, para cada um, um
**par assintomático a ≥20 m** no mesmo sector e na mesma cota. Saída em
**coordenadas navegáveis por GPS de mão**, mais prancha de campo.

Assenta em instrumentos da secção 1. **É construível hoje.**

### T2 · Locais das covas de perfil, no mesmo desenho
Por `DEC-08`. Três: margem da mancha oriental, uma célula do interior morto, e
um controlo são pareado. Escolhidos **sobre as linhas de escoamento do MDT**,
para que o perfil responda à pergunta de drenagem e não a outra.

### T3 · RQ6 — as manchas seguem a drenagem, ou espalham-se em raio?
Radial e independente da água = **biótico**. A seguir a acumulação de fluxo =
**abiótico**. Temos o MDT LiDAR, as linhas de escoamento e as máscaras datadas.
**É o único trabalho de gabinete que ainda pode mover o diagnóstico**, e informa
T1 dizendo *onde* fica a margem que interessa.

### T4 · Detector de estrutura em ortofoto sem folha — com âncora que discrimine
Fechar o buraco da secção 4. O método falhou por **âncora**, não por conceito:
usou-se `nu2021` como chão nu, e o `nu2021` lê 34 % de fiadas brilhantes. Uma
âncora nova — chão lavrado **fora** do pomar, ou uma parcela de cultura anual —
e o teste volta a ser possível. **Barato, e responde à pergunta 3 do email sem
depender da resposta.**

### T5 · Ficha de colheita e cadeia de custódia
O `§D1` diz que 13 das 20 linhas organismo×matriz assentam numa amostra
composta, num sítio, num dia; o `§D5` que nenhuma amostra com posição é anterior
ao acontecimento; e as ITS de 2025 não têm folhas de requisição. **Uma campanha
nova que repita isto não vale a deslocação.** A ficha fixa: ponto GPS, sector,
válvula, estado da planta, matriz colhida, hora, quem, e o par a que pertence.

### T6 · Segundo leitor para as chamadas visuais
A forma G continua aberta. Qualquer leitura de imagem que entre no relatório
precisa de dois leitores independentes ou de um instrumento que a confirme.

---

## 6 · O que NÃO construir

- **Mais georreferenciação de válvulas.** `DEC-01`. Fecha com GPS no terreno,
  durante a campanha — não com mais cálculo.
- **Mais SAR.** `DEC-03`. Nenhum reprocessamento recupera sinal abaixo da
  dispersão do instrumento.
- **Mais bibliografia.** O `§13` fechou-a a 28-08: *«Everything else now depends
  on DATA, not literature.»* Continua verdade onze dias depois.
- **Mais aparelho de verificação** sem uma falha medida que as onze cláusulas
  existentes não tenham apanhado.
