# Variabilidade analítica — referências e o que cada uma estabelece

Consultado em 29-08-2026, para desenhar a réplica independente da cadeia de
validação do caso de Ganfei.

**Nota de honestidade sobre o acesso.** Não li todos estes artigos linha a
linha. O que li está marcado. Os que estão atrás de paywall entram com resumo
integral e sínteses secundárias, e isso está assinalado em cada entrada.

---

## 1. Silberzahn et al. 2018 — o estudo fundador

Silberzahn, R., Uhlmann, E. L., Martin, D. P., Anselmi, P., Aust, F., Awtrey,
E., Bahník, Š., Bai, F., Bannard, C., Bonnier, E., … Nosek, B. A. (2018).
**Many analysts, one dataset: Making transparent how variations in analytical
choices affect results.** *Advances in Methods and Practices in Psychological
Science*, 1(3), 337–356.
**DOI: 10.1177/2515245917747646**
Aberto em: https://eprints.whiterose.ac.uk/145795/

*Lido: metadados completos, desenho e resultados quantitativos. Não o corpo
integral.*

- 29 equipas, 61 analistas, os mesmos dados, a mesma pergunta.
- **20 equipas encontraram efeito significativo, 9 não.**
- Dimensões de efeito de 0,89 a 2,93 em razão de possibilidades, mediana 1,31.
- 29 análises usaram **21 combinações distintas de covariáveis**.
- **O achado que mais importa para nós:** nem as crenças prévias dos analistas,
  nem o seu nível de perícia, nem a qualidade da análise avaliada por pares
  explicaram a variação nos resultados.

> Consequência operacional: **não se corrige a dispersão escolhendo um analista
> melhor.** Ela não é ruído de competência.

---

## 2. Botvinik-Nezer et al. 2020 — NARPS, e a agregação funciona

Botvinik-Nezer, R., Holzmeister, F., Camerer, C. F., Dreber, A., Huber, J.,
Johannesson, M., Kirchler, M., Iwanir, R., Mumford, J. A., Adcock, R. A., …
Schonberg, T. (2020). **Variability in the analysis of a single neuroimaging
dataset by many teams.** *Nature*, 582(7810), 84–88.
**DOI: 10.1038/s41586-020-2314-9**

*Lido: resumo e resultados. Não o corpo integral.*

- 70 equipas independentes, o mesmo conjunto de dados, **as mesmas nove
  hipóteses declaradas à partida**.
- **Nenhuma dupla de equipas escolheu o mesmo fluxo de trabalho.**
- A variação nos testes de hipótese persistiu **mesmo entre equipas cujos mapas
  estatísticos estavam altamente correlacionados em fases intermédias** — ou
  seja, dois pipelines podem concordar a meio e divergir no fim.
- **E o resultado construtivo:** uma abordagem meta-analítica que agregou a
  informação entre equipas produziu consenso significativo.

> Consequência operacional: **agregar, não escolher.** E hipóteses fixas à
> partida — foi assim que este estudo se tornou interpretável.

---

## 3. Breznau et al. 2022 — a variação não se explica pelas escolhas visíveis

Breznau, N., Rinke, E. M., Wuttke, A., Nguyen, H. H. V., Adem, M., Adriaans,
J., Alvarez-Benjumea, A., Andersen, H. K., Auer, D., Azevedo, F., … Żółtak, T.
(2022). **Observing many researchers using the same data and hypothesis reveals
a hidden universe of uncertainty.** *PNAS*, 119(44), e2203150119.
**DOI: 10.1073/pnas.2203150119**
Correcção: **DOI: 10.1073/pnas.2410677121**

*Lido: resumo e resultados. Não o corpo integral.*

- 161 investigadores em 73 equipas, os mesmos dados, a mesma hipótese.
- Os resultados variaram **de efeitos negativos grandes a positivos grandes**.
- **As escolhas de desenho do teste estatístico explicam muito pouco dessa
  variação.** Fica um universo de incerteza por explicar.

> Consequência operacional: registar as escolhas não chega para prever a
> conclusão. A variação é em boa parte idiossincrática.

---

## 4. Kummerfeld & Jones 2023 — a causa está antes da análise

Kummerfeld, E., & Jones, G. L. (2023). **One data set, many analysts:
Implications for practicing scientists.** *Frontiers in Psychology*, 14,
1094150.
**DOI: 10.3389/fpsyg.2023.1094150**

*Lido: integral — é acesso aberto.*

- Argumenta que a variabilidade vem sobretudo de **três problemas evitáveis
  anteriores à análise estatística**, não de subjectividade inevitável.
- A tese central: equipas diferentes chegam a conclusões diferentes em larga
  medida porque **estão a responder a perguntas diferentes (Q\*)**, não porque
  a análise seja inerentemente variável.
- Recomendações concretas: especificar a pergunta de forma accionável (unidade
  de análise clara, tipo de pergunta definido, fronteiras contextuais
  explícitas, **termos bem definidos e acordados**); formular explicitamente a
  pergunta matematicamente precisa que se está a responder, com as suas
  suposições; e cobrir com a equipa o máximo de áreas de perícia relevantes.
- Não trata pré-registo, nem agregação de resultados divergentes, nem critérios
  para quando vale a pena.

> Consequência operacional: **fixar a pergunta antes de replicar.** Uma
> pergunta aberta garante divergência não interpretável.

---

## 5. Bertran, Fogliato & Wu 2026 — o mesmo, com agentes

Bertran, M., Fogliato, R., & Wu, Z. S. (2026). **Many AI analysts, one dataset:
Navigating the agentic data science multiverse.** *PNAS*.
**DOI: 10.1073/pnas.2606495123**
Pré-publicação: arXiv:2602.18710, 21-02-2026 (v2 de 11-03-2026).
**DOI: 10.48550/arXiv.2602.18710**

*Lido: resumo integral e sínteses secundárias. O artigo está atrás de paywall
(403) e o PDF do arXiv não parseou. **Não li o corpo.***

Do resumo, verbatim nos pontos que importam:

- Analistas de IA autónomos reproduzem, barato e à escala, a diversidade
  analítica estruturada dos estudos humanos de muitos analistas.
- Desenho: **cada analista executa um pipeline completo sobre um conjunto de
  dados fixo e uma hipótese fixa; um auditor de IA separado rastreia cada
  corrida quanto a validade metodológica.**
- Três conjuntos de dados de domínios distintos; dispersão substancial em
  dimensões de efeito, valores p e conclusões.
- A dispersão traça-se a escolhas identificáveis em pré-processamento,
  especificação do modelo e inferência, que **variam sistematicamente com o LLM
  e com a persona**.
- **Os resultados são direccionáveis:** trocar a persona ou o modelo desloca a
  distribuição **mesmo entre corridas metodologicamente sólidas**.
- Norma proposta: relatório em estilo multiverso e **divulgação integral dos
  prompts, ao mesmo nível do código e dos dados**.

> Consequência operacional: quando análises defensáveis são baratas de gerar,
> a prova torna-se abundante e vulnerável a relato selectivo. **Uma réplica
> isolada não é verificação — é uma amostra de uma distribuição larga.**

---

## O que isto muda no desenho deste caso

**Separar por TIPO DE FACTO, e são três, não dois.**

**1 · Testemunho directo.** Alguém esteve lá e sabe. A coordenada do armazém,
as duas pontas do B1, a tabela de áreas por válvula, quais as válvulas com
raiz de Summer Kiwi, que a rede só existiu no B1. Isto **não é medição nem
inferência**: entra como dado. O modo de falha é outro — memória, ambiguidade
de referência, mudança desde a data a que a pessoa se refere — e **não se
corrige com réplica nenhuma. Corrige-se perguntando outra vez a quem sabe.**

**2 · Medição.** O que se calcula a partir de imagem ou de instrumento: a área
do polígono, a cota, a série de NDVI, o compasso das fileiras. Tem erro de
instrumento, e replica-se — mas com o aviso de que réplicas no mesmo
directório reproduzem as armadilhas do directório, não só a análise.

**3 · Inferência.** O que a prova sustenta: quando mudou, se é concentrada ou
uniforme, o que a explica. **É aqui, e só aqui, que a literatura do multiverso
se aplica.**

Isto descreve exactamente o que aconteceu neste caso em 28 e 29 de Agosto.
Todas as correcções grandes vieram da categoria 1 a entrar e a derrubar
trabalho das categorias 2 e 3: a coordenada do armazém desfez uma colocação por
contagem de fileiras que parecia bater a 0,3 %; as duas pontas do B1
localizaram um bloco que tinha estado perdido desde o início; a tabela de áreas
resolveu de uma vez o que quatro métodos geométricos não tinham resolvido; e a
correcção da nomenclatura desfez uma inversão que sobreviveu a quatro
auditorias. **Nenhuma quantidade de réplica das categorias 2 e 3 produz um
facto da categoria 1.**

**Para a categoria 3 — inferência — o desenho que a literatura sustenta:**

1. **Hipótese fixa e falsificável**, não pergunta aberta (Kummerfeld & Jones;
   Botvinik-Nezer).
2. **N maior que um.** Três a cinco. N = 1 dá concordância ou discordância sem
   escala para a interpretar (todos os cinco).
3. **Auditor separado** a rastrear cada corrida quanto a validade metodológica
   antes de entrar na distribuição (Bertran et al.). Instrumento já existente
   neste projecto: `ADVERSARIO_PROMPT.md`.
4. **Variar deliberadamente a persona e o prompt** entre corridas, porque é
   isso que gera a diversidade — e registar qual foi qual (Bertran et al.).
5. **Relatar a distribuição, não a corrida preferida.** E agregar, que é o que
   produziu consenso no NARPS (Botvinik-Nezer).
6. **Divulgar os prompts** com o mesmo estatuto do código e dos dados
   (Bertran et al.).

**E o que não fazer:** tentar reduzir a dispersão escolhendo analistas melhores.
Silberzahn mostra que perícia, crenças prévias e qualidade avaliada por pares
não explicam a variação.
