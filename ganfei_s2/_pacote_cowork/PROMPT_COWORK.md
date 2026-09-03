# Prompt para a sessão Cowork

*(copiar tudo a partir da linha abaixo)*

---

Duas tarefas sobre o caso do declínio do kiwi em Ganfei, Valença. A primeira é
para produzir; a segunda é para criticar. **Faz a segunda primeiro se tiveres
de escolher** — a primeira depende de números que a segunda pode invalidar.

Tudo o que precisas está neste computador:

```
Downloads\_FIGURAS_DOSSIE\           as seis figuras — png\, svg\, scripts\
                                     LEIA-ME.md, LACUNA_BIOTICA.md
Downloads\ganfei_s2\                 dados e código da análise de satélite
Downloads\ganfei_s2\_pacote_cowork\  AUDITORIA.md e o histórico de correcções
Downloads\Ganfei_Kiwi_Decline_Traceability_Workbook.xlsx
Downloads\tier1_framework_draft.md   o enquadramento Tier 1 (Pilares A–D)
Downloads\_GANFEI_REEXECUCAO_CEGA\SAIDA\   auditoria cega já concluída
```

---

## TAREFA 1 — fechar as lacunas de localização

**Lê primeiro `_FIGURAS_DOSSIE\LACUNA_BIOTICA.md`** e o §10 do
`tier1_framework_draft.md` (addenda v1.2 a v1.4). Uma versão anterior desta
tarefa partia do princípio de que nenhum resultado de laboratório estava
localizado. **Estava errada** — a tabela válvula↔bloco existe e o gestor já
localizou a maior parte do material. A tarefa é mais estreita do que parecia.

**O que continua em falta**, e é o que se pede:

1. **O ponto exacto do «Kiwi 1000»** (Areeiro `331/2025 V.1`, expediente
   2025045292, colheita 2025-06-06). É o painel etiológico mais completo do
   processo — catorze organismos em madeira, raiz e solo. O gestor localizou-o
   em v1.3 desenhando **uma oval à mão** sobre uma captura NDVI: flanco oeste
   da Mancha W, B1-este/B2-oeste. Falta o ponto. Perguntar também **se a
   amostra foi composta de vários pontos** e, se foi, quais e se as
   sub-amostras ficaram guardadas.

2. **Os pontos das quatro amostras ITS** (`ISFBV0314`–`0317`). Estão
   localizadas na Zona 0, mas foram colhidas por um parceiro sem folhas de
   requisição. O laboratório **não está identificado** no processo; aparece
   uma referência a *Nostoc Biotechnologies / UCM* — confirma se é a mesma
   entidade antes de escrever. Se não conseguires estabelecer o fornecedor,
   diz isso e propõe a quem perguntar. Acrescenta uma pergunta técnica: as
   taxas de leituras retidas são 29%, **3%**, **4%** e 10% — vale a pena
   perguntar se as amostras a 3% e 4% são consideradas válidas pelo próprio
   laboratório.

3. **As duas perguntas que o gestor saltou** — o §10 assinala que ficaram sem
   resposta na ronda anterior e têm de ser re-postas explicitamente:
   (a) a amostra de raiz retida da planta «Rosellinia» chegou alguma vez a ser
   enviada para PCR, e onde está agora?
   (b) de que bloco(s) veio o «Kiwi 1000» — agora parcialmente respondida, mas
   o ponto continua por dar.

4. **Ponto de colheita dos boletins A2** (`2601930`–`2601934`, `2606721`,
   `2606722`, `2607885`–`2607888`). Prioridade baixa, mas sai na mesma leva.
   Há uma inconsistência de textura registada em B2-V7 que o gestor resolveu
   como heterogeneidade intra-parcelar — confirmar o ponto GPS de cada amostra
   fecharia isso.

**Como pedir.** Uma carta por destinatário: Areeiro (Pontevedra, em castelhano
ou galego), o laboratório das ITS quando identificado, A2 Análises Químicas
(Guimarães, português). Curtas, cordiais, com as referências exactas e uma
pergunta única. Aceita-se, por ordem: coordenadas GPS; marcação em
ortofotomapa; código de bloco/válvula com croqui; ou o nome de quem colheu.
**Deixa explícito que uma resposta parcial tem valor** — o objectivo é não
perder o que possa estar num caderno de campo.

**Não envies nada.** Entrega os textos para revisão e envio manual.

## TAREFA 2 — revisão crítica das seis figuras

Foram produzidas seis figuras estáticas para o dossiê. Quero-as **atacadas**,
não elogiadas. Estão em `Downloads\_FIGURAS_DOSSIE\` com os scripts que as
geram — os scripts lêem CSV e GeoTIFF a partir de
`Downloads\ganfei_s2\figuras\`, portanto tudo é verificável até à origem.

| Fig. | O que afirma |
|---|---|
| F1 | Matriz de diagnóstico diferencial — 13 hipóteses, estado e força de prova |
| F2 | Livro-razão das exclusões — 10 vias excluídas e o que a exclusão **não** cobre |
| F3 | Cronologia de três faixas — satélite × gestão × laboratório num só eixo |
| F4 | Chave espacial — focos, frente em avanço, onde amostrar |
| F5 | Desenho de amostragem para Setembro — estratos, compartimentos, seis regras |
| F6 | Árvore de decisão — os cinco desfechos do Pilar D + teste de geometria |

### As afirmações que mais interessa atacar

Por ordem de quanto estragam o dossiê se estiverem erradas:

1. **F6 — a coluna «a geometria diz».** É um acrescento meu ao Pilar D, e é a
   afirmação mais forte do conjunto: que a geometria medida já exclui quatro
   dos cinco ramos, e que o único compatível — alastramento radial por
   contacto — é o que nunca foi testado. **Isto é raciocínio, não medição.**
   Verifica se cada veredicto (COMPATÍVEL / PARCIAL / INCOMPATÍVEL) se sustenta
   na literatura sobre o modo de dispersão de cada agente, e diz-me quais
   estão a esticar a prova. Se algum estiver errado, a figura desmonta-se.

2. **F3 — o degrau de 2021 sem nada na faixa de gestão.** A leitura é que o
   primeiro degrau da Zona 0 precede os pomares novos (que começam em 2022) e
   portanto não pode ser diluição hidráulica. Isto depende inteiramente de a
   faixa de gestão estar completa para 2021. **Se houve alguma intervenção em
   2021 que não esteja registada, o argumento cai.** É a inferência causal
   mais carregada de todo o dossiê.

3. **F1 e F2 — a convergência para a subsuperfície.** Sete das dez exclusões
   deixam a mesma lacuna por cobrir, e as figuras concluem daí que 40–80 cm é
   o alvo. Verifica se essa convergência é real ou se é artefacto de eu ter
   escrito as dez linhas da coluna «o que a exclusão não cobre».

4. **F4 — a frente em avanço de 5,92 ha.** É a diferença entre o défice de
   2026 e o de 2024, com uma abertura morfológica. Verifica a sensibilidade ao
   elemento estruturante e ao limiar de défice. É o polígono que vai
   determinar onde 15 plantas são colhidas.

5. **F5 — a afirmação «zero amostras a 40–80 cm em nove colheitas».** Confirma
   no workbook. Se alguma amostra foi colhida mais fundo do que assumi, a
   figura tem de mudar.

### Contexto que deves ter

- **Já houve uma auditoria cega.** Uma sessão independente reimplementou os
  seis quadros a partir da especificação, sem ver o código. Está em
  `_GANFEI_REEXECUCAO_CEGA\SAIDA\`, com `AMBIGUIDADES.md` e `OBSERVACOES.md`.
  Lê antes de começar; não repitas o que já lá está.
- **Histórico de correcções** em `_pacote_cowork\AUDITORIA.md`. Onze erros já
  foram encontrados e corrigidos, incluindo dois desta semana. Não é para te
  intimidar — é para não gastares tempo nos já apanhados.
- **Quatro correcções de última hora**, todas de 28-08-2026, e todas por
  confirmar que não sobrou vestígio nos ficheiros:
  (a) as colunas `B-3/C-3` da folha `Pathology Matrix` **não são de Ganfei** —
  são do relatório 240/2023, titular Kiwi Atlántico S.A., um caso externo.
  *Dactylonectria*, *Ilyonectria liriodendri* e *Rhizoctonia solani* estão a
  um passo de serem citados como se fossem daqui. Atenção à colisão de
  rótulos: Ganfei **tem** um B3C3 real, que é a válvula 27.
  (b) o *P. sojae* do processo vem dos Becrop, que são da válvula 27 —
  **parcela isolada, não o corpo em declínio**. A F1 citava-o como evidência a
  favor da linha oomicetas/KVDS no corpo principal; foi retirado e a força da
  evidência desceu de Forte para Moderada. A F3 punha-o na faixa de
  laboratório sem distinguir a parcela; foi anotado.
  (c) **novo facto do gestor:** o corpo principal é Erica de **pé franco**.
  B1 são as válvulas 1–5, e as válvulas 2–5 foram cortadas e enxertadas duas
  vezes (Enza Gold 2016, Erica 2020). Entrou uma linha nova na F1 e a nota de
  B1 na F4 foi reescrita.
  (d) fica **por resolver** uma ambiguidade que muda a leitura: se B1 foi
  sobre-enxertado nos troncos existentes, as raízes de B1 também são de pé
  franco e B1 deixa de ser contraste de propagação. Se foi replantado com
  material enxertado, é. Diz-me qual das duas leituras a documentação
  sustenta, ou se é preciso perguntar ao gestor.

### Restrições de desenho, para a crítica ser justa

- Cor nunca sozinha: todo o estado tem glifo (forma) + cor + rótulo.
- Paleta validada para daltonismo; nenhum duplo eixo vertical.
- Português pré-Acordo Ortográfico.
- **Nada de precisão inventada.** A F4 recusa desenhar os sectores de válvulas
  (o esquema de rega é um desenho à mão sem coordenadas) e deixou de desenhar
  as parcelas dos 11,16 ha de pomar novo pela mesma razão. Se encontrares
  outro sítio onde eu tenha atribuído posição a coisa que não a tem, é achado
  de primeira ordem.

### O que entregar

Um ficheiro `REVISAO_FIGURAS.md`, com:

1. **Por figura:** o que está errado, o que está a esticar a prova, e o que
   está bem e deve ficar como está. Sê específico — número, linha, painel.
2. **Um veredicto por figura:** *usar como está* / *usar com correcção* /
   *não usar*. Se for «não usar», diz o que a substitui.
3. **A pergunta que nenhuma das seis responde.** Seis figuras é bastante; se
   houver um buraco no argumento que nenhuma cobre, é isso que quero saber.
4. **Se discordares de uma escolha de desenho, diz** — mas separa isso dos
   erros de facto. As duas coisas não têm o mesmo peso.

Se um número te parecer estranho, **não o corrijas**: regista-o. E se
concluíres que uma figura está certa, diz isso com a mesma clareza com que
dirias o contrário — um «está bem» verificado vale tanto como um erro
encontrado.
