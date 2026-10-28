# Testemunho do analista, 06-09-2026 — a origem é o foco NASCENTE

**Quem:** o analista responsável pelo caso (CCDR-N).
**Quando:** 06-09-2026, em resposta directa ao mapa C (`P13`), que marcava dois
candidatos como **A · poente** e **B · nascente**.

> *«I know the answer to this. problem started in B»* · *«im telling you its B
> the eastern most part»*

**Tipo 1.** Não é medição nem inferência. Entra como dado, e — pela regra do
`CLAUDE.md` — **ganha a qualquer cálculo nosso, e o cálculo que derrubar é
retirado, não reconciliado.**

---

## O que fixa

**A origem do problema é o foco NASCENTE**, o que a `c1_00_comum.py:17` chama
`FOCO_ESTE` (E530977 N4655117), e que a partição em sectores dá como **B3**
— as válvulas 13 e 14 estão a 81 e 93 m dele.

## O que derruba, e é meu

A `TESTEMUNHO_GESTOR_2026-09-06.md` §2, escrita horas antes, afirmava que a
máscara `zona0` estava mal nomeada por estar no foco oriental. **Está retirada.**
O centróide da máscara cai a **26 m** do foco nascente: a máscara sempre esteve
no sítio certo, e a correcção é que era o erro.

**A forma G pela quinta vez, e desta com um agravante.** Não recebi «a origem é
ocidental» de ninguém. **Inferi-a**: tabela de válvulas do gestor → 8, 9, 10 são
B2 → B2, *nas coordenadas que nós próprios atribuímos às válvulas*, fica a
poente. Uma inferência sobre um georreferenciamento que já tinha morrido cinco
vezes — escrita debaixo do cabeçalho de um documento de testemunho, o que lhe
emprestou um estatuto que ela não tinha. **Um documento de tipo 1 não santifica
o que se escreve lá dentro.**

## O que NÃO fica resolvido, e é a pergunta 1 do email

O gestor escreveu, textualmente, *«zone 0 = valves 8, 9, 10»* e *«onde tudo
começou»*. Na nossa reconstrução essas válvulas ficam assim:

| válvula | sector (tabela do gestor) | ao foco poente | à origem (nascente) |
|---|---|---|---|
| 8 | B2 | **35 m** | 487 m |
| 9 | B2 | **98 m** | 400 m |
| 10 | Erica Novo | **171 m** | 325 m |
| 13 | B3 | 448 m | **81 m** |
| 14 | B3 | 546 m | **93 m** |

**Meio quilómetro de desacordo.** Uma de duas coisas está trocada: ou as
coordenadas que atribuímos às válvulas, ou a correspondência válvula→sector que
ele nos deu. **Não se resolve por cálculo** — as coordenadas são nossas e já
falharam cinco vezes, e a tabela é dele. Corrige-se perguntando outra vez a quem
sabe, e é a pergunta 1.

## O que muda a jusante

- **A leitura do SAR, o facto C2, o critério P3 e o `AUD-17`** mediram a máscara
  `zona0`. Como essa máscara está na origem, mediram **a origem** — que era o que
  o texto original dizia. A reescrita de 06-09 para «foco oriental» não fica
  errada (é o mesmo sítio) mas **deixou de ser correcção**.
- **As análises de solo de 2025**, que o gestor situa «na Zona 0, onde tudo
  começou», voltam a cair na unidade que temos vindo a medir — ao contrário do
  que a §2 retirada concluiu.
- **A `P13` deixa de ser um mapa de escolha.** A origem está fixada; o que passa
  a servir é mostrar a discrepância das válvulas.
