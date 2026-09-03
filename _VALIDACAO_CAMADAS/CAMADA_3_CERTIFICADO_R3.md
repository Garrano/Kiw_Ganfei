# Camada 3 — Biologia · re-execução R3

**Data:** 31-08-2026 · **Responde a:** `CAMADA_3_PROMPT_R2.md`
**Herda:** C0 (+R2, +R3) e C2 (+R2, +adversário R2, +`CAMADA_2_TESTES_T1_T5`).
**Precedência:** ganha sobre `CAMADA_3_CERTIFICADO_R2.md` só onde o contradiz.
Onde não o contradiz, **mantém-se** — e o prompt mandou dizê-lo assim.

**Saldo em três linhas.** As três tarefas foram corridas. **Nenhuma conclusão
biológica muda.** Uma fica mais forte, duas eram inaplicáveis por bom motivo, e
o delta da camada 2 revelou que **esta camada já tinha encontrado, dois dias
antes, o achado que a camada 2 apresentou como novo**.

---

## TAREFA 1 · As amostras contra a partição do LiDAR — **B7 fica MAIS forte**

Reproduzida a partição de Voronoi da C3 a partir do mesmo
`valvulas_por_area.json`, e **verificada contra as contagens publicadas antes de
qualquer cruzamento**: B3 992/992, B4 417/417, Erica Novo 535/535. Bate. Só
depois se cruzou com a altura do voo de 06-07-2025.

| unidade ensaiada | ha | altura mediana | **% sem pérgola (LiDAR)** | % `nu2021` |
|---|---|---|---|---|
| **B3** — a única do lado oriental | 9,92 | 2,22 m | **28,1 %** | 16,3 % |
| B4 | 4,17 | 2,31 m | 15,3 % | 1,2 % |
| B2 | 10,87 | 2,30 m | 3,0 % | 0,0 % |
| V7 (a válvula com 45,9 % do esforço) | 3,25 | 2,31 m | **0,3 %** | 0,0 % |
| Erica Novo | 5,35 | 2,33 m | 0,2 % | 0,0 % |

**Resposta à pergunta, e é preciso ser exacto sobre o que ela pode significar.**

*Nenhuma amostra de raiz pode ter vindo de chão* — uma raiz implica uma planta.
A pergunta do prompt, tomada à letra, tem resposta trivial e não é a que
interessa.

**O que interessa é o que a B7 já dizia, e que agora tem um número maior:** a
única amostra do lado oriental é **um composto sobre 9,92 ha**, e a fracção
dessa área que não tem pomar passa de **16,3 % (ortofoto 2021)** para **28,1 %
(LiDAR 2025)**. O instrumento novo, medindo estrutura em vez de solo lavrado,
encontra **quase o dobro** de área sem planta dentro da unidade a que o
positivo está atribuído.

**B7 mantém-se e reforça-se:** «a contagem de 28/37 não pode ser atribuída a
plantas do foco ESTE» era verdade com 16,3 % e é mais verdade com 28,1 %.

**E aparece um contraste que a C3 não tinha:** a unidade que concentra 45,9 %
de todo o esforço de amostragem — a **v7** — tem **0,3 % sem pérgola**, e a
única unidade oriental tem **28,1 %**. O esforço está concentrado onde o
substrato é homogéneo, e é escasso onde não é.

## TAREFA 2 · O Landsat não muda nada nesta camada — **e a razão é boa**

Procurada, no `CAMADA_3_CERTIFICADO_R2.md`, qualquer afirmação sobre o foco
oriental que dependesse de não haver segundo instrumento: «não confirmado»,
«sem instrumento», «não há segundo instrumento». **Zero ocorrências.**

**Porquê.** A limitação da C3 sobre o oriental nunca foi instrumental — é de
**resolução de amostra**. B7 não diz «não sabemos porque só temos um sensor»;
diz «o positivo está atribuído a 9,92 ha, dos quais parte não tem planta». Um
segundo satélite não desloca uma amostra composta.

**Mantém-se, sem alteração.** E fica registado como caso em que o delta de uma
camada abaixo, sendo real e importante, **não toca** a camada de cima — o que é
informação e não ausência dela.

## TAREFA 3 · Não aplicável, e por cumprimento da regra 5

Procurada qualquer hipótese biológica desta camada que dependesse da forma
espacial da propagação: «propagação», «contacto de raízes», «radial»,
«contíguo». **Zero ocorrências nos onze factos que a C3 passa para cima.**

A C3 **não faz** afirmações de propagação. A regra 5 do protocolo — «a C3 não
opina sobre a causa» — foi cumprida, e por isso a ausência de gradiente não tem
onde bater.

**Declaro NÃO APLICÁVEL**, que o prompt admitia explicitamente como saída, em
vez de especular. A frase «favorece ou desfavorece propagação por contacto de
raízes» é uma pergunta de camada 4.

---

## CONFIRMADO

| facto | ficheiro e cálculo | instrumento independente | margem |
|---|---|---|---|
| **A partição de blocos da C3 reproduz-se exactamente** a partir de `valvulas_por_area.json`: 992, 417, 535 células, sem desvio. | `c3_r2_01_amostras_contra_pergola.py`, verificação antes do cruzamento | — (é reprodução, não facto de terreno) | 0 células |
| **A unidade oriental ensaiada tem 28,1 % de área sem pérgola** — 2,79 das 9,92 ha —, contra 16,3 % pela ortofoto de 2021. Altura mediana 2,22 m; 67,4 % acima de 1,5 m. | idem, cruzamento com `chm_altura.npy` (G38) | **LiDAR contra ortofoto**: dois instrumentos, duas épocas, duas grandezas — solo lavrado contra estrutura acima do chão. Concordam no sinal e diferem na magnitude | ±1 célula |
| **O esforço de amostragem é inverso à heterogeneidade do substrato.** A v7 concentra 45,9 % dos registos colocados e tem 0,3 % sem pérgola; o B3 tem 14,4 % dos registos e 28,1 % sem pérgola. | `c3_r2_01_amostras.json` + B6 do certificado anterior | LiDAR para o substrato, livro do laboratório para o esforço | — |

## CORRIGIDO

| o que se dizia | o que está certo | o que muda acima |
|---|---|---|
| **B7:** «9,92 ha, dos quais **16,3 %** são chão lavrado». | O número pela ortofoto está certo. **Pelo LiDAR, e é a partição operativa desde a C2 R2, são 28,1 %.** Os dois convivem: medem coisas diferentes na mesma unidade. | B7 fica mais forte. Onde for citada, cita-se **28,1 % (LiDAR 2025)** com o 16,3 % (ortofoto 2021) ao lado. |
| **A camada 2 (S6) apresentou como achado que «14 das 110 células da referência caem dentro dos discos».** | **Esta camada já o tinha certificado em 29-08, no B10, e conta 18 — doze no ocidental e seis no oriental.** A diferença é o centro do disco oriental: a C3 usa E530977 N4655117, a C2 R2 usa o centróide da Zona 0, E530999 N4655102. **Os dois estão certos para a sua definição.** | **A prioridade é da C3.** A C2 não podia herdar da C3 — a cadeia só herda para cima —, mas o achado não é novo, e o número que sobe deve ser **o par 18/14 com a definição de cada um**, não um deles sozinho. |

## REJEITADO

Nada. Nenhum facto da C3 cai com o delta da camada 2.

## NÃO TESTÁVEL

- **A posição real de qualquer amostra desta camada.** Tudo o que a C3 coloca
  no espaço vem de `valvulas_por_area.json`. A adenda v1.1 mediu **465 m de
  amplitude entre quatro reconstruções do esquema para a mesma válvula** — da
  ordem da distância entre os dois focos. A C3 escolheu uma das quatro e
  declarou as outras desactualizadas; **essa escolha nunca foi certificada por
  nenhuma camada.** Tudo o que este certificado diz sobre posição é «na
  partição que a C3 usou», não «no terreno».
- **Se o positivo de *M. hapla* do B3 veio de dentro ou de fora do foco.** O
  B3 tem 9,92 ha e só **25,7 %** dele cai no disco oriental. A amostra é
  composta e não tem ponto.
- **A forma do acontecimento entre 2025-08-14 e 2026-07-27** (herdado da C2:
  onze cenas de plena estação por olhar). Toca a esta camada porque **todas as
  doze amostras com posição são posteriores a Março de 2026** (B11) — se
  houve dois declínios em vez de um, nenhuma amostra viu o primeiro.

## PASSA PARA CIMA

**Mantêm-se, sem alteração, os onze factos B1–B11 da `CAMADA_3_CERTIFICADO_R2`**,
com duas emendas:

**B7 · reforçado.** A unidade oriental ensaiada tem **28,1 % de área sem
pérgola pelo LiDAR de 2025** (16,3 % de chão lavrado pela ortofoto de 2021).
A contagem de 28/37 continua a não poder ser atribuída a plantas do foco ESTE.

**B10 · com prioridade e com o par de números.** A contaminação geométrica da
referência foi estabelecida **por esta camada, em 29-08**: 18 de 110 células
dentro dos discos, 12 no ocidental e 6 no oriental. A camada 2 chegou ao mesmo
com outra definição de centro e contou 14. **Sobe o par, com as definições.**

**B12 · NOVO.** **O esforço de amostragem é inverso à heterogeneidade do
substrato:** 45,9 % dos registos colocados estão numa unidade com 0,3 % de área
sem pérgola; a única unidade oriental, com 28,1 %, tem 14,4 %. *(medido;
`c3_r2_01_amostras.json`)*

---

## NOTA AO ADVERSÁRIO DA CAMADA 4

Duas coisas que esta camada não consegue resolver e que a de cima vai ter de
tratar como limite, não como detalhe:

1. **Toda a geografia biológica deste caso assenta num ficheiro de válvulas que
   nunca foi certificado**, e cujas alternativas divergem 465 m. Se essa
   escolha estiver errada, os onze factos mantêm-se como contagens e perdem-se
   como localizações.
2. **Nenhuma amostra com posição é anterior ao acontecimento**, e agora sabe-se
   que o acontecimento pode ter sido dois. A camada 4 não pode escrever
   «antes e depois» com este material.
