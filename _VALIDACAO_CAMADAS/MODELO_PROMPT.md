# Modelo do prompt de cada camada

Cada sessão, ao terminar, escreve o prompt da camada seguinte usando este
modelo. Não é um formulário a preencher às cegas: os conteúdos concretos —
que ficheiros, que factos herdados, que perguntas — mudam de camada para
camada e são responsabilidade de quem escreve.

Regra que atravessa tudo: **nunca metas no prompt seguinte uma conclusão de
uma camada acima.** Se souberes, por teres visto algures, o que a inferência
final diz, não o passes. Contamina.

---

```markdown
# Camada N — <nome da camada>

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada N de uma cadeia de validação. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md`.

## O que herdas — e só isto

Estes factos foram certificados pelas camadas abaixo. Trata-os como dados,
não os revalides, e não uses nada que não esteja nesta lista.

<colar aqui, na íntegra, a secção PASSA PARA CIMA de cada certificado
 anterior, identificando a camada de origem e a margem de erro de cada facto>

## O que ficou por resolver abaixo de ti

<lacunas que as camadas anteriores marcaram como NÃO TESTÁVEL e que podem
 afectar o teu trabalho. Diz porque é que cada uma te afecta.>

## O que foi rejeitado, e não podes usar

<a secção REJEITADO das camadas anteriores. Isto é tão importante como o que
 passa: impede que um facto morto volte a entrar pela porta do lado.>

## Materiais

<caminhos exactos dos dados desta camada, e só desta camada>

## Tarefas

<numeradas, concretas, cada uma nomeando o ficheiro a examinar e a pergunta
 a responder. Uma tarefa que não nomeia ficheiro não é uma tarefa.>

## Onde já se errou nesta matéria

<erros conhecidos e correcções já feitas nesta camada, para não se perder
 tempo a redescobrir. Se não houver, diz que não há.>

## O que entregar

1. `CAMADA_N_CERTIFICADO.md`, com as cinco secções do protocolo.
2. `CAMADA_N+1_PROMPT.md`, seguindo este modelo.
3. Código em `SAIDA_CN\`.

Não teorizes acima da tua camada. Se um resultado te sugerir uma causa,
guarda-a para ti: não é a tua pergunta, e escrevê-la contamina quem vier a
seguir.

Se rejeitares um facto herdado, **pára** e devolve. Não construas por cima.
```

---

## Nota sobre a sequência

A ordem é C0 → C1 → C2 → C3 → C4 → C5, e a razão de C2 (sinal vegetal) vir
antes de C3 (biologia) é esta: a biologia deste caso não tem quase nenhum
valor isolada. Doze resultados positivos sem padrão espacial não decidem nada
— foi o que aconteceu com *M. hapla*, positivo em todos os blocos amostrados.
A biologia só se torna informativa quando se pode perguntar «isto está onde o
padrão está, ou está em todo o lado?». Para isso o padrão tem de estar
validado primeiro.

Se em alguma camada se perceber que a ordem está errada, isso é um achado —
regista-o e diz qual devia ser.
