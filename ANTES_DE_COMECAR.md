# ANTES DE COMEÇAR

**Ler antes de qualquer análise neste caso. Não é um resumo — é a lista das
maneiras como este processo já se enganou, e do que se faz para não repetir.**

Compilado em 03-09-2026 a partir de: `CLAUDE.md`, `CONTROLOS.md`, `PROTOCOLO.md`,
os certificados C0–C5 e as suas revisões, os adversários de cada camada, os dois
relatórios do **Controlo 3**, as retractações `P5_RETRACCAO_DO_REPLANTADO.md`,
`REG01_RETRACCAO_A3.md` e `C4_ADENDA_RAZAO_2026-09-03.md`, e as notas deixadas
pela sessão paralela nos cabeçalhos do código.

**Dezanove veredictos retirados em seis dias.** Nenhum foi apanhado por
recomputação. Todos por ir a um instrumento diferente.


> **Dois documentos companheiros, e vêm carregados no arranque com este.**
>
> · **`HIPOTESES_FECHADAS.md`** — o que já foi testado e fechado. A triagem
>   é cega ao negativo por construção, e a 04-09 isso custou a repetição de um
>   estudo de onze cenas. Ler antes de desenhar um teste novo.
>
> · **`CLAUSULAS.md`** — as oito formas que as vinte e três retiradas tomaram,
>   o invariante que as une (*alguma coisa que devia ser independente não era*),
>   e as nove cláusulas que as travam — quatro delas já executáveis.

---

## 0 · A PRÉ-VOO — onze perguntas, antes de escrever a primeira linha de código

Se alguma resposta for «não sei», **isso é o trabalho**, não um pormenor a
resolver depois.

| | pergunta | quem já morreu por não a fazer |
|---|---|---|
| **1** | **Que pergunta exacta?** Unidade de análise, tipo, fronteiras, termos definidos — fixados por escrito. | Kummerfeld & Jones 2023: pergunta aberta garante divergência não interpretável |
| **2** | **Qual é a hipótese, e o que a falsifica?** Escritas antes de correr, com o limiar. | a REG-01 deu o contrário do esperado; só se pôde dizê-lo porque o critério estava escrito antes |
| **3** | **De onde vem a fronteira da unidade?** Foi derivada do sinal que vou medir? | `fazer_masks_v2.py`: `pomar := nd2026 > 0,78`, e media-se a evolução até 2026. Quatro auditorias passaram por cima |
| **4** | **A unidade era a mesma coisa durante todo o intervalo?** | retirada 19: cinco blocos «duas a quatro vezes piores» estavam desmatados desde 2024 |
| **5** | **Que instrumento INDEPENDENTE vai confirmar isto?** Se não houver, digo-o. | retiradas 9, 10, 15, 16, 18 — todas por concluir de um instrumento só |
| **6** | **As âncoras discriminam NESTA medição?** E o pico está na escala que julgo? | retirada 16: em 2021 nem a referência tinha o pico no compasso da pérgola |
| **7** | **A minha estatística de resumo esconde heterogeneidade?** | a mediana sobre 300 mil píxeis dos cinco blocos não viu 14 a 44 % de solo nu |
| **8** | **Quantas observações independentes, mesmo?** Não cenas — *n*. | 29 cenas de 2025-26 são **dois anos**; seis cenas em treze dias não são seis observações |
| **9** | **O que é que este teste NÃO decide?** Escrito à frente, não em rodapé. | — |
| **10** | **Se isto falhar, como saberei?** | um aviso teria sido ignorado das três vezes. Por isso o portão levanta excepção |
| **11** | **A minha janela contém tudo o que a frase abrange?** Uma AOI é uma decisão, não um dado. | **o sector B1** — 12,63 ha de kiwi do mesmo dono — cai 123 m a sul e 455 m a oeste da AOI, e por isso **nenhuma figura o mostrava** |

---

## 1 · AS SEIS CONDIÇÕES DO PORTÃO — `guarda.py`

Cada uma existe porque alguma coisa passou sem ela. **Correr `guarda.py` é o
auto-teste: sete casos históricos têm de bloquear e o controlo positivo tem de
passar.**

| | condição | a cicatriz |
|---|---|---|
| **1** | instrumento declarado | sem isto não há o que auditar |
| **2** | **instrumento independente que concorde**, ou `nao_testavel()` explícito | controlo 1 do `CONTROLOS.md`, escrito a 28-08 e violado três vezes em três dias |
| **3** | **âncoras que discriminem** *e* **pico na escala esperada** | separar não é medir o que se julga: em 2021 a prominência separava, mas já não media pérgola |
| **4** | **reprodução** de um cálculo certificado, quando exista | — |
| **5** | **identidade da unidade no tempo** — e **exige o ficheiro do rastreio**, não uma frase | o Controlo 3 reconstruiu o A3 retirado, acrescentou `identidade_no_tempo("declaracao do IFAP")` e **o portão autorizou-o outra vez** |
| **6** | **fronteira da unidade** não derivada do sinal | o `fazer_masks_v2.py` |

**O omissivo é «temporal».** Quem se esquece da bandeira é exactamente quem
precisa dela; para dispensar a condição 5 é preciso escrever `instantanea(porque)`
e assinar a razão.

---

## 2 · A TAXONOMIA — as dezanove, em quatro famílias

Reconhecer a família é reconhecer o erro **antes** de o cometer.

### A · Concluí de um instrumento só *(cinco)*
A AOI «lóbulo oeste B1» · o «núcleo em declínio, p < 0,0005» · «o lóbulo é o
melhor controlo» · «o foco oriental foi replantado» · «o B1 é o comparador sem
degrau».
**Sinal de alarme:** a frase e a prova usam o mesmo sensor.
**Antídoto:** condição 2. *Um NDVI não se confirma com outro NDVI.*

### B · A unidade não era o que o nome dizia *(quatro)*
A designação dos dois focos invertida · a AOI do outro lado do rio, aceite porque
a pasta se chamava `sentinel_b1` · a distância de «1,06 km», que media uma
entidade inexistente · «blocos vizinhos 2 a 4× piores», desmatados em 2024.
**O caso mais caro desta família, e ainda vivo: HÁ DOIS «B1».**

| | o que é | estado |
|---|---|---|
| a **AOI** `b1` (528400–529400, 4654900–4655700) | tecido urbano de Valença, do outro lado do Minho | **retirada** a 28-08, 49 ficheiros em quarentena |
| o **sector B1** | E 529 495–530 063 · N 4 653 832–4 654 477 · = C1a + C1b · **12,63 ha de kiwi do mesmo dono** | **real**, localizado por duas coordenadas do gestor — testemunho de tipo 1, 28-08 |

Retirar a AOI **não retira o sector**. Confundi os dois e, durante toda a série de peças, chamei ao sector «o bloco sudoeste» e nunca o desenhei — enquanto a P01 dizia «44 hectares declarados» e mostrava um mapa de 30,3. **A diferença era exactamente o B1.** Foi preciso o gestor dizê-lo duas vezes.

E a razão de fundo não era distracção: **a AOI de 2 × 1 km exclui o B1 por construção**, e toda a figura desenhada em células de máscara herda essa cegueira sem o dizer. Uma janela é uma escolha; quando uma frase abrange mais do que a janela, a frase e o desenho deixam de bater certo.

**Sinal de alarme:** o nome do ficheiro, da pasta ou da coluna está a fazer
trabalho de prova. Ou: a área que o texto afirma não é a área que o mapa mostra.
**Antídoto:** condições 4, 5 e 6. E a guarda de cultura, que verifica o código
declarado polígono a polígono em vez de confiar no nome do ficheiro.

### C · A estatística era artefacto do meu próprio processamento *(cinco)*
Viés de calibração do S2C · «zero défice em 2022-24», da abertura morfológica
aplicada depois de intersectar · o rio a ler NDVI +0,314 · a correcção de deriva
aditiva numa relação multiplicativa · o T5, que era **uma identidade algébrica**:
limpar a referência deslocava todos os fossos pela mesma constante, +0,008430,
idêntica à nona casa.
**Sinal de alarme:** o resultado é suspeitosamente limpo, ou repete-se.
**Antídoto:** perguntar o que o teste faria se a hipótese fosse falsa. Se a
resposta for «a mesma coisa», não é um teste.

### D · Estatística correcta, morta por um teste melhor *(cinco)*
O halo com decaimento (ρ ingénuo p = 2×10⁻⁹; por deslocamento toroidal p = 0,55)
· o declive oriental como «declínio crónico» · três achados mortos pela mesma
curva de saturação · o placebo do degrau em chão · a «convergência» que comparava
NDRE com NDVI.
**Sinal de alarme:** o p é muito pequeno e o nulo é ingénuo.
**Antídoto:** um nulo que respeite a estrutura dos dados — autocorrelação
espacial, saturação, escala.

---

## 3 · AS DUAS REGRAS DE HIGIENE QUE JÁ CUSTARAM CARO

**Nunca derivar uma máscara do sinal que se vai medir.** E **ler sempre o
cabeçalho e o código juntos** — o `fazer_masks_v2.py` afirmava «polígonos
geográficos e estáticos» e o `landsat_independente.py` prometia «só píxeis
inteiramente dentro da unidade, e reporta-se o n», e nenhum dos dois fazia o que
dizia.

**Nenhum facto passa verificado só pelo instrumento que o produziu.** Confirma-se
contra ortofoto, SAR, LiDAR, documento, fotografia de campo ou testemunho. Se não
houver instrumento independente, fica **registado como não verificado** — não se
dilui numa ressalva.

---

## 4 · OS TRÊS TIPOS DE FACTO

**1 · Testemunho directo.** Alguém esteve lá e sabe. **Entra como dado**, ganha a
qualquer cálculo nosso, e **o cálculo que ele derrubar é retirado, não
reconciliado.** Corrige-se perguntando outra vez, nunca replicando.
*Exemplo vivo:* «a PSA nunca foi encomendada porque a sintomatologia não era
compatível» — que transformou uma lacuna de quatro documentos numa exclusão
clínica. **E o que o testemunho não diz fica em branco à vista:** quem observou,
quando, com que critério — **não sabido**, e não se preenche por inferência.

**2 · Medição.** Tem erro declarável. Replica-se — **mas uma réplica no mesmo
directório reproduz as armadilhas do directório**, não só a análise.

**3 · Inferência.** É aqui, e só aqui, que a literatura do multiverso se aplica.

**Etiquetar cada afirmação com o seu tipo antes de a usar.**

---

## 5 · VARIABILIDADE ANALÍTICA — o que a literatura obriga

Referências com DOI em `REFERENCIAS_MULTIVERSO.md`.

- **Equipas independentes com os mesmos dados chegam a conclusões opostas**
  (Silberzahn 2018; Breznau 2022).
- **Não se corrige com melhores analistas** — perícia e revisão por pares não
  explicam a variação.
- **Boa parte da divergência é por se responder a perguntas diferentes.** Fixar
  a pergunta antes de replicar.
- **Agregar funciona; escolher não** (Botvinik-Nezer 2020).
- **Agentes de IA reproduzem isto e são direccionáveis** (Bertran 2026): trocar
  persona ou modelo desloca a distribuição **mesmo entre corridas sólidas**.

**Daqui sai:** N = 1 não é verificação · hipótese fixa antes de replicar ·
auditor separado · variar persona e prompt de propósito e registar qual foi qual
· **relatar a distribuição, não a corrida preferida** · divulgar os prompts com
o mesmo estatuto do código.

---

## 6 · AS SESSÕES PARALELAS — como se usam, e como não

**Não se duplicam sessões com o mesmo prompt.** Duas sessões com os mesmos dados
e o mesmo vocabulário cometem **erros correlacionados**: uma segunda sessão teria
olhado para a pasta `sentinel_b1/` e concluído exactamente o mesmo, ao decimal, e
ambas estariam erradas. A duplicação apanha lapsos de execução; **não apanha
premissas falsas partilhadas**, que é a classe que aqui custou semanas.

**O Controlo 3 é outra coisa:** uma sessão independente, com o mandato de
*procurar o erro*, com perguntas fixadas por quem a lança e obrigação de correr
código. Correu para a C0, a C2 e a REG-01. Matou o S9, o T5 e cinco afirmações
mais, e obrigou a reescrever o portão duas vezes.

**Onde o certificado e o adversário discordarem, ganha o adversário.**

**A sessão paralela de Cowork reescreve a árvore de trabalho a meio do turno.**
Nunca `git add -A`; reconfirmar o estado antes de preparar qualquer coisa. As
notas dela chegam nos cabeçalhos do código — a guarda de cultura do
`reg01_landsat.py` descrevia exactamente o erro que eu ia cometer, e eu corri o
ficheiro e publiquei o resultado à mesma. **Ler os cabeçalhos que mudaram.**

---

## 7 · AS ARMADILHAS MECÂNICAS DESTA MÁQUINA

Custaram horas, e nenhuma é interessante.

- **Heredocs comem barras invertidas.** Um `\n` dentro de uma cadeia Python
  escrita por heredoc chega como quebra de linha real e parte o ficheiro.
  **Usar as ferramentas Write/Edit, ou `chr(10)`.** Nunca escapes.
- **Ao fugir das barras invertidas, não escrever em ASCII.** Uma peça saiu com
  «Ha 91 maneiras», «chao», «ja era baixo» — reintroduzindo o defeito que a
  sequência começou por corrigir.
- **JSON em cp1252.** Ficheiros escritos com `ensure_ascii=False` no Windows não
  abrem como utf-8. Cadeia de recurso: utf-8 → cp1252 → latin-1.
- **A consola é cp1252.** Um JSON com acentos crus sai mutilado; para saída de
  máquina, `ensure_ascii=True`.
- **`print("ok")` incondicional depois de um `replace`.** Um script anunciou
  sucesso enquanto a substituição nunca coincidiu. **`assert` antes de escrever.**
- **Contar o que a saída diz, não o que se espera.** Um multiverso imprimiu
  «utilizáveis: 1 de 4» e o veredicto por baixo dizia «não inverte em nenhuma
  reconstrução».

---

## 8 · O QUE CORRER, E QUANDO

```bash
python certificar.py
```

Sete verificações, código de saída ≠ 0 quando falha: o auto-teste do portão · os
23 factos · a prosa contra o registo · nenhum documento vivo a citar um retirado
· os scripts dos factos existem · o rastreio está fresco · **as figuras não são
mais velhas que a lista de factos**. Corre sozinho ao fim de cada turno pelo
gancho `Stop`.

**Antes de qualquer comparação entre parcelas:**
`reg01_triagem_descontinuidade.py` — leva minutos e evita repetir a retirada 19.

**Ao acrescentar um facto:** declará-lo em `registo_de_factos.py`. Se não passar
as seis condições, **não entra na `LISTA_FINAL`**. A verificação 3 impede a prosa
e o registo de divergirem.

---

## 9 · A REGRA QUE RESUME TUDO

> **Uma regra que só existe em prosa é uma regra que se cumpre quando dá jeito.**

O controlo 1 estava escrito e foi violado três vezes. A guarda de cultura estava
no cabeçalho do ficheiro que eu corri. A ressalva sobre a continuidade da cultura
descrevia o erro antes de ele acontecer.

**Por isso é que o portão levanta excepção em vez de avisar, e por isso é que a
condição 5 passou a exigir um ficheiro em vez de uma frase.** O que não for
executável será ignorado no dia em que der jeito ignorá-lo — e esse é sempre o
dia em que interessava.
