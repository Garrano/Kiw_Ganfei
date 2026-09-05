# PRÉ-REGISTO — SAR, Outubro a Abril. O instrumento que não depende de folha.

**Escrito a 05-09-2026, antes de descarregar nada.**

> **Vai a um adversário independente e ESPERA-SE pela resposta antes de correr.**
> À primeira não houve adversário; à segunda lancei-o e corri sem esperar; à
> terceira esperei e ele partiu o critério antes de custar alguma coisa. É essa
> a ordem.

---

## 1 · Porque este instrumento, e não mais NDVI

O `p8` preencheu o vão com 49 cenas ópticas e **não pôde decidir** quantas
transições houve. A razão não foi amostragem: foi que **Novembro a Fevereiro não
é legível em NDVI** — o kiwi é caducifólio e o contraste passa a medir cobertura
de solo sob pérgola nua. E o portão bloqueia na condição 2: oito ou quarenta e
nove cenas de Sentinel-2 não confirmam Sentinel-2.

O radar não depende de folha nem de luz solar. **É física diferente, e é o que a
condição 2 exige.** A série existente pára no inverno de **2024-25** por escolha
do desenho, não por falta de dados — precisamente o inverno anterior à janela em
questão.

## 2 · A pergunta, fixada

**Unidade:** célula de 10 m agregada em unidades **geométricas** — as mesmas do
`c1_09_sar.py`, derivadas de ortofoto DGT e do polígono `zona0`. **Nenhuma usa
NDVI**, e o cabeçalho desse ficheiro documenta que as máscaras anteriores eram
circulares e foram substituídas por isso.
**Tipo de facto:** medição.
**Grandeza:** γ⁰ em dB, VV e VH, **contraste foco-menos-referência**.
**Janela:** **1 de Outubro a 30 de Abril**, e aplicada aos **quatro** invernos —
2022-23, 2023-24, 2024-25 e 2025-26. Não só ao novo: comparar sete meses do novo
com cinco meses dos antigos seria a janela a decidir em silêncio, que é a forma C
e foi o que matou o `p2`.

**Hipótese fixa:** *se houve um acontecimento que afectou a estrutura do copado
entre Outubro de 2025 e Abril de 2026, o contraste foco-menos-referência em γ⁰
desloca-se no inverno de 2025-26 face aos três invernos anteriores, **no mesmo
sentido nas duas órbitas**.*

## 3 · Órbitas nunca se misturam

Órbitas 125 e 147 tratam-se em separado, sempre. Geometrias de vista diferentes
tornam γ⁰ não comparável. **Um deslocamento numa órbita só não conta como
resultado** — conta como artefacto de geometria, e diz-se isso.

É a única maneira de este desenho ter uma réplica interna: duas geometrias
independentes sobre o mesmo terreno, no mesmo período.

## 4 · SEVERIDADE — e a minha primeira versão estava errada por 2,5 a 5,7×

**Corrigido a 05-09-2026, em auto-verificação antes de submeter.** A primeira
versão deste parágrafo calculava o MDE tratando **cenas** como réplicas
independentes: 0,27 a 0,42 dB. Está errado. A humidade do solo, que é a ameaça
principal deste desenho, é **comum dentro de um inverno** — logo a unidade de
replicação é o **inverno**, e há três.

Medido no `c1_09_sar_geografico.csv`, contraste foco-oeste menos referência:

| órbita | pol | sd DENTRO | sd ENTRE invernos | rácio |
|---|---|---|---|---|
| 125 | VV | 0,500 | 0,168 | 0,3× |
| 125 | VH | 0,301 | 0,161 | 0,5× |
| 147 | VV | 0,349 | 0,281 | **0,8×** |
| 147 | VH | 0,390 | 0,378 | **1,0×** |

Na órbita 147 a variância entre invernos **iguala** a variância entre cenas.
Agrupar 35 cenas como se fossem 35 réplicas infla o n por um factor de ~12.

**MDE correcto** (inverno como unidade, 3 de base contra 1 novo, t com 2 g.l.):

| órbita | pol | SE | **MDE** | (versão errada) |
|---|---|---|---|---|
| 125 | VV | 0,194 | **1,04 dB** | ~~0,42~~ |
| 125 | VH | 0,186 | **1,00 dB** | ~~0,27~~ |
| 147 | VV | 0,325 | **1,74 dB** | ~~0,35~~ |
| 147 | VH | 0,437 | **2,34 dB** | ~~0,41~~ |

**Consequência, dita antes:** uma perda de copado move o VV 1 a 3 dB. Escrevi que
havia «folga de um factor de 3 a 7». **Não há folga.** O desenho fica em cima do
limiar: detecta uma perda severa de copado e **não detecta uma moderada**. Um
resultado negativo aqui é fraco, e tem de ser relatado como fraco.

## 4b · A linha de base já está em tendência — e isto é o que mais me preocupa

Médias por inverno, contraste foco-oeste menos referência:

```
orb 125  vv   -0,030 -> +0,056 -> -0,268     declive -0,119 dB/inverno
orb 125  vh   +0,044 -> -0,141 -> -0,277     declive -0,161 dB/inverno
orb 147  vv   +0,097 -> -0,216 -> -0,465     declive -0,281 dB/inverno
orb 147  vh   +0,121 -> +0,193 -> -0,495     declive -0,308 dB/inverno
```

**As quatro descem, nas duas órbitas e nas duas polarizações.** Um quarto inverno
que continue esta tendência produz um Δ de −0,12 a −0,31 dB **sem acontecimento
nenhum**.

Com três pontos de base, ajustar a tendência deixa **1 grau de liberdade**. Não
chega. Portanto, declarado antes:

> **Este desenho, como está, NÃO separa «acontecimento» de «continuação de
> tendência».** É a forma D — degrau lido onde há declive — e foi uma retirada
> desta cadeia.

**Duas saídas, e a escolha vai ao adversário antes de correr:**

**(a) Alargar a linha de base.** O Sentinel-1 cobre desde 2014. Oito invernos
dariam df = 7 para o declive e permitiriam testar **desvio da tendência**, não
desvio da média. **Mas introduz uma descontinuidade de plataforma:** o S1B falhou
em Dezembro de 2021, pelo que os invernos anteriores a 2022 têm S1A+S1B e os
posteriores não — revisita e possivelmente calibração diferentes. Trocar um
problema por outro, e o outro é a forma C.

**(b) Aceitar que o desenho só responde a uma pergunta mais fraca:**
*o inverno de 2025-26 desvia-se da tendência dos três anteriores por mais do que
o MDE?* Com o MDE corrigido, isso só detecta uma perda severa.

**Não escolho aqui.** Vai a adversário, e a escolha é registada com a razão.

## 5 · A tabela de decisão

| ramo | selecciona-se se |
|---|---|
| **DESLOCAMENTO CONFIRMADO** | \|Δ\| ≥ MDE nas **duas** órbitas, **mesmo sentido**, em VV ou VH |
| **UMA ÓRBITA SÓ** | \|Δ\| ≥ MDE numa órbita e não na outra → **artefacto de geometria**, não resultado |
| **SEM DESLOCAMENTO** | \|Δ\| < MDE nas duas |
| **NÃO DECIDE** | < 8 cenas por órbita no inverno novo, ou o controlo negativo do §6 falhar, ou o Δ ficar entre o declive da tendência e o MDE |

**E o ramo SEM DESLOCAMENTO não significa «não houve acontecimento».** O radar
mede estrutura e humidade. Um declínio fisiológico sem alteração de estrutura é
invisível ao SAR. Está escrito antes de correr para não ser negociado depois:
**«sem deslocamento» é sobre o radar, não sobre o pomar.**

## 6 · A ameaça principal, e o controlo negativo

**Humidade do solo.** A retrodifusão de inverno é dominada pela chuva. Um inverno
mais húmido desloca tudo. O contraste cancela o que é comum — mas o foco
ocidental está **no ponto mais baixo da exploração, a 13,4 m da drenagem**, e a
referência não. **A humidade pode não cancelar, e é a ameaça que este desenho
tem de vencer.**

**Controlo negativo, e corre antes da leitura.** Corrigido em auto-verificação:
a primeira versão propunha `resto do pomar`, e o `c1_09_sar.py` **não calcula
essa unidade** — calcula `pomar`, que **inclui os dois focos**. Um nulo que
contém aquilo que controla é a forma A, e teria entrado por eu ter escrito o
nome de uma unidade sem confirmar que existe.

A unidade tem de ser **construída**: `pomar` menos os dois discos de 90 m menos
`zona0` menos `referencia` — o análogo exacto do CONTROLO do lado óptico.
Contraste **`resto` − `referência`**: duas unidades de kiwi vivo, mesma
exploração, mesma chuva, e ninguém alega acontecimento em nenhuma. Nos quatro
invernos, mesmas órbitas, mesmo tratamento.

**Ressalva que viaja com ela, e vem da lição do lado óptico:** «ninguém alega»
não é o mesmo que «sabe-se que não houve». É um nulo assumido, não conhecido. Se
o adversário souber construir um nulo conhecido a partir do que há em disco,
esse ganha.

**Pré-registado:** se o controlo negativo se deslocar ≥ MDE em 2025-26, **a
leitura não se faz** — o que estamos a ver é o inverno, não o pomar. O ramo é
NÃO DECIDE.

Corre-se também o **`nu2021`** — chão lavrado, sem copado nenhum — como segundo
nulo: se ele se deslocar, é solo, não vegetação.

## 7 · O que este desenho NÃO faz

- **Não diz a causa.**
- **Não estabelece a natureza da unidade oriental** — declínio contra arranque
  continua aberto e é anterior a isto.
- **Não usa `COM`.** As unidades são geométricas puras, o que evita o problema do
  voo LiDAR de 2025-07-06 estar dentro da janela. Consequência aceite: as
  unidades incluem chão dentro dos discos, e o sinal é mais diluído.
- **Não é confirmação do NDVI se discordar.** Se o radar disser uma coisa e o
  óptico outra, isso é um conflito a registar, não um a reconciliar.

## 8 · O que sai no portão

Se o deslocamento for confirmado nas duas órbitas, este é o **primeiro
instrumento independente** a cobrir a janela: fecha a condição 2, que nem o `p2`
nem o `p8` podiam fechar. O veredicto passaria de NÃO TESTÁVEL a testável.

Se não for, o facto continua NÃO TESTÁVEL — mas passa a sê-lo **com um limite
superior medido** em vez de por ausência de instrumento, o que é diferente e
melhor.

## 9 · Ficheiros

`sar_out_abr.py` → `sar_out_abr.json` + `sar_out_abr.csv` (uma linha por cena,
para o ruído ser auditável). Carimbo de produtor. **Nenhum ficheiro existente é
alterado**; o `c1_09_sar.py` fica como está.
