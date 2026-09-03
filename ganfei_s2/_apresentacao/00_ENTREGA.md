# 00 · ENTREGA — sessão Claude Code (local) para sessão Cowork

**Data:** 31-08-2026 · **Estado:** ponto 1 e 2 da ordem de execução feitos ·
**Memo de referência:** `MEMO_INFOGRAFIA.md` v1.0

---

## §4 · DESACORDOS — LEIA ESTA SECÇÃO ANTES DAS OUTRAS

O memo diz que onde ele colidir com o disco, o disco ganha. Colide em cinco
sítios, e **o primeiro é grave o suficiente para parar a produção**.

### D1 · A §3.2 tem a identidade dos focos INVERTIDA

O memo atribui:

> **Foco ORIENTAL** (Zona 0, válvulas 8–10) → azul `#2a78d6`
> **Foco OCIDENTAL** (Mancha W) → laranja `#eb6834`

O ficheiro operativo `valvulas_por_area.json` (G35, o mesmo que o memo cita em
§A11) diz:

| válvula | coordenada E | lado |
|---|---|---|
| v6 | 530 260 | ocidental |
| v7 | 530 398 | ocidental |
| **v8** | **530 500** | **ocidental** |
| v9 | 530 583 | ocidental |
| v10 | 530 654 | ocidental |
| v13 | 530 917 | oriental |
| v14 | 531 010 | oriental |

**As válvulas 8 a 10 estão todas a oeste.** O foco ocidental é v8/B2, centro
E530485 N4655053. O oriental é v13-v14/B3, centro E530977 N4655117.

**Isto não é um lapso de escrita do memo — é a inversão que este processo já
pagou.** A designação «Zona 0 / Mancha W» esteve trocada durante semanas,
sobreviveu a quatro auditorias, e é a razão de existir o `REGISTO_DE_NOMES.md`.
Construir doze peças sobre a §3.2 rotularia os dois focos ao contrário em toda
a apresentação.

**Adoptado, e o resto do memo mantém-se:** azul `#2a78d6` = **ocidental,
v8/B2**; laranja `#eb6834` = **oriental, v13-14/B3**; água `#1baf7a` = lóbulo
B1. Todas as peças levam coordenada ao lado do nome, sem excepção.

### D2 · «O oriental está lá desde a primeira cena» mede, em parte, chão

O memo dá como o número mais forte do processo o fosso da Zona 0 **sem solo nu
de 2021** à referência: **+0,01103/ano, p = 0,0162**.

O LiDAR de 06-07-2025, que o memo ainda não tinha visto, mede nesse disco:

- altura mediana **0,47 m**;
- **50,2 %** das células abaixo de 0,5 m;
- e **22,7 %** do que a máscara `~nu2021` classificava como «plantado» **não
  tem pérgola nenhuma**.

A máscara `nu2021` vem da ortofoto de 2021 e sub-capta. **O declive de
+0,01103/ano continua a ser um resultado**, mas o que ele mede é em parte
ausência de planta, e a figura que o publicar tem de o dizer. O termo «foco»
aplicado ao lado oriental sem essa ressalva promete mais do que mede.

### D3 · Quatro figuras existem e não têm lugar na sequência

O memo diz «só vi F8, F13 e F14». Existem mais quatro, e **duas delas são a
prova mais forte do dossiê**:

| figura | o que é | porque tem de entrar |
|---|---|---|
| **F10** altura de copado | mapa LiDAR, MDS−MDT | É a peça que **separa o caso em dois**. Sem ela, a §0.3 do memo («dois focos com data») não se sustenta. Único instrumento não-óptico. |
| **F12** Landsat, 140 cenas | 2013–2026, USGS/NASA | **Único instrumento independente do Sentinel-2 em todo o caso.** Onze anos dentro de ±0,004 e depois 0,046 e 0,146. Traz o seu próprio controlo negativo. |
| **F11** matriz de diagnóstico | 20 linhas organismo × matriz | É a **justificação do pedido**: 13 de 20 numa amostra composta, 2 com posição, zero linhas bacterianas. |
| **F9** série separada | défice partido pelo LiDAR | Mostra o que muda quando se separam as duas coisas. |

**Proposta de sequência revista — treze peças, e a A00 muda de números-herói.**
Ver §1.

### D4 · Números que o memo dá por sem-fonte já a têm

§8.1 diz que «44,9 ha existe só em prosa e não tem script». Passou a ter duas
fontes independentes:

- **tabela de válvulas do gestor:** 44,93 ha;
- **parcelário IFAP, campanha 2025, ENT 472062:** **44,36 ha** de kiwi
  declarado, por WFS aberto da CCDR-N.

**1,3 % de diferença.** *Ressalva registada:* as duas fontes não são
independentes uma da outra — o ENT_ID foi seleccionado pela geografia que o
gestor deu e compara-se com uma tabela do mesmo gestor. Vale como concordância,
não como validação cruzada.

### D5 · A comparação regional já não está «por fazer» na totalidade

§11.5 põe-na como incógnita que empurraria a sequência. Estado real:

- **feito:** o teste de paisagem correu. 35 cenas, seis classes de coberto com
  rótulos do IFAP e do LiDAR. **A mata madura não se mexeu: −0,0035, p = 0,81.**
  O que cai é o ciclo curto — milho −0,077. **O enquadramento do caso aguenta.**
- **feito:** o inventário existe — **1 054 ha de kiwi declarado por 204
  beneficiários**, e uma exploração a **8,1 km** com 76 ha declarados onde uma
  análise independente encontrou sinal semelhante com degrau em 2024.
- **por fazer:** o painel exploração-a-exploração. É agora barato e programável.

### D6 · Correcções menores ao memo

- **§A11:** «o rótulo T1 colide com U1» — **não existe U1**. As unidades são
  T1, U2, U3, U4. A sobreposição de «PAR SÃO ocidental» com «âncora de CAMPO»
  **já foi corrigida**; a regra dos 3 mm passa a ser verificada por render.
- **F5 e F6** (desenho de amostragem e árvore do Pilar D do `_pacote_cowork\`)
  **foram rejeitadas** pela camada de decisão da cadeia de validação: assentam
  em factos retirados — avanço radial de 15–40 m/ano, centróide a ±17 m, «Zona 0
  = foco mais antigo», «válvula 27», «*M. hapla* em 5 de 5 blocos». Cinco das
  seis regras do painel C da F5 foram salvas e re-justificadas; o resto sai.
  **Não podem circular.**
- **§3.5, lista de RETIRADO:** o memo pede quatro linhas. Tenho onze, e três
  são de peso. Ver §5.

---

## §1 · MAPEAMENTO — A00 a A12

Treze lugares, não doze. As três peças novas são D3.

| lugar | fonte | estado | justificação |
|---|---|---|---|
| **A00** o caso numa página | NOVA | por fazer | Números-herói revistos: **7 fechadas · 3 por abrir · 0 ensaios com posição na v8**. |
| **A01** três registos de tempo | **F8** | **acentos corrigidos** | Falta: etiquetas de estado §3.5, faixa de conjuntura como incompleta, fonte do dreno e do cálcio. |
| **A02** dois pontos hidraulicamente opostos | NOVA | por fazer | Do banda inferior da F8. Escopo «dentro do copado» obrigatório no título. |
| **A03** cronologia de três faixas | F3 | por corrigir | Retirar a seta causal da diluição; anotar «ano de detecção». |
| **A04** as manchas emergem sozinhas | NOVA | **prioridade** | Fecha a acusação de circularidade. |
| **A05** timelapse | NOVA | por fazer | Especificação §6 do memo, sem alterações. |
| **A06** gémeo estático | NOVA | por fazer | É a que vai impressa. |
| **A07** chave espacial e satélites | F4 + M2 | por corrigir | Resolver a convenção angular antes de afirmar seja o que for sobre o L1. |
| **A08** o que já não é | **F13** | **pronta** | Falta só o terceiro bloco RETIRADO. |
| **A09** livro-razão | F2 | **proposta: sai** | Ver §3. |
| **A10** o que nos faria mudar de ideias | NOVA | por fazer | Ao nível do modelo; a F14 fá-lo por ponto. |
| **A11** o plano de Setembro | **F14** | **quase pronta** | Falta orçamento e via de isenção no rodapé. |
| **A12** *(novo)* a prova independente | **F12** | **pronta** | Landsat, 140 cenas. Ver D3. |

**E dois lugares que proponho inserir antes de A01, porque a sequência actual
não sobrevive sem eles:**

- **A00b · os dois focos não são a mesma coisa** — a **F10**. Tem de vir logo a
  seguir à A00, porque toda a narrativa a jusante depende dela.
- **A08b · a matriz tem uma coluna** — a **F11**. Vem imediatamente antes do
  pedido, porque é a sua justificação.

A **F9** entra como painel de apoio dentro da A04, não como peça própria: diz a
mesma coisa que a A04 por outra via e não merece uma página.

---

## §2 · FEITO

```
_apresentacao\scripts\a_corrigir_acentos.py
figuras\f8_braudel.py        20 substituições + 6 finais · re-renderizada
figuras\f9_serie_separada.py 12 substituições + 2 finais · re-renderizada
figuras\f*.py                cabeçalho de rcParams do §2.4 nas catorze
```

**Verificação dos acentos (§8.4.1):** varredura por AST sobre todas as strings
constantes que **não** são docstring, contra dezanove formas sem diacrítico.
Zero ocorrências restantes em texto desenhado. As que um `grep` ingénuo apanha
noutras figuras são **chaves de dicionário** — `"OESTE com pergola"` é chave do
`landsat.json` e alterá-la parte a leitura.

---

## §3 · NÃO FEITO, E PORQUÊ

Tudo o resto. A ordem de execução do memo põe os acentos e o mapeamento
primeiro, e foi até aí que cheguei. **Nada foi desenhado ainda**, e é
deliberado: a D1 obrigaria a refazer o que fosse feito antes de a resolver.

**Decisão pedida em §A09 — a F2 sai da sequência.** A F13 cobre o que ela fazia
e melhor, com a gramática «hipótese fixada antes de correr · instrumento ·
resultado», e a F2 traz uma seta «⇒ 40–80 cm» cujo alvo honesto é o perfil
completo. Passa a anexo técnico. A09 fica vazio; a sequência tem doze peças
mais as duas inserções.

---

## §5 · A LISTA DE «RETIRADO» — o memo pede quatro, tenho onze

Para a A08. As três primeiras são as de peso, e nenhuma delas estava na lista
do memo.

1. **A designação dos dois focos esteve invertida**, e sobreviveu a quatro
   auditorias.
2. **O viés de calibração do Sentinel-2C** de −0,048 NDVI, citado por todo o
   processo. Quatro medições emparelhadas de quatro análises independentes dão
   **≈ zero**. Vinha de um degrau medido *fora* do pomar, com sensor e ano
   confundidos.
3. **«Os focos perdem água antes de verdura»** — a leitura NDMI contra NDVI, e
   com ela a inferência hidráulica ou vascular que dela saía.
4. O sinal térmico como «primeira detecção fisiológica» — é contabilidade de
   copado.
5. A narrativa de alastramento concêntrico a partir do foco oriental.
6. **A radiometria das ortofotos DGT** — o rio Minho lê NDVI **+0,314 em 2021 e
   +0,187 em 2025**, e água não pode ter NDVI positivo.
7. As máscaras derivadas do NDVI de 2026.
8. **A hipótese do encharcamento por posição no terreno** — o défice está no
   terreno alto, nas onze cenas.
9. **A hipótese da rede de rega sobre-estendida** — dentro do nulo em 11 de 11.
10. **A hipótese do porta-enxerto** como explicação da divergência do B1.
11. Os «zeros» da série sanitária em 2022-24 — eram artefacto de abertura
    morfológica aplicada dentro de subconjuntos. O piso real é 0,66 ha.

---

## §6 · TESTE DO L1 (A07) — não corrido

Fica para quando a A07 for construída. **Não afirmo alinhamento nem
não-alinhamento** — a convenção angular do `regionprops` não está resolvida, e o
memo tem razão em exigir que se resolva primeiro.

## §7 · O NÚCLEO INTERNO DO LÓBULO OESTE — não determinado

Há material novo que o memo não tinha e que muda a pergunta. Três análises
independentes sobre a hipótese do porta-enxerto concluíram: **o B1 e o corpo
principal divergem entre 2021 e 2026, com o B1 do lado bom** (confirmado por
radar em duas órbitas), **mas a divergência não se atribui à raiz** — 64 % do
ganho faz-se no primeiro passo, que é a curva de recuperação da re-enxertia a
saturar. A hipótese (b) do memo — «efeito das duas decotes/enxertias» — é a que
os dados favorecem. **Não construo a peça sem confirmação.**

## §8 · VERIFICAÇÕES

Dos dez pontos de §8.4, corri **um**: o dos acentos, e passa. Os outros nove
correm quando houver figuras novas para verificar.

## §9 · PERGUNTAS

1. **Confirma a inversão da §3.2?** É a única coisa que me impede de arrancar
   com as doze peças. Se o memo estiver a usar outra convenção de nomes que eu
   desconheço, preciso de a saber antes de desenhar.
2. **A F10 e a F12 entram na sequência conduzida ou nos cartões expansíveis?**
   Defendo o caule: sem a F10 a tese não se sustenta, e a F12 é a única prova
   independente que temos.
3. O timelapse tem público? Se não houver data de reunião, proponho adiar a A05
   e fazer só a A06, que é a que vai impressa.
