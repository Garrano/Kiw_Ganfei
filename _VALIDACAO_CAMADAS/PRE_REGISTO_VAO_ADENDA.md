> # ⚠ RETIRADO em 05-09-2026, antes de correr
> A regra de classificação aqui descrita **não se aplica**. O adversário da C9
> leu-a antes da corrida — que é o objectivo da cláusula — e mostrou que σ
> estava errado por **5,5×** (0,0277 medido contra «≈ 0,005» escrito), que a
> amplitude do degrau simulado do §6 nunca foi declarada, que os dois controlos
> negativos são inválidos, que a regra fenológica é inexecutável em 47 % das
> posições, e que o §2 e o §4 se contradizem **sem regra de precedência** — com
> o §2 a seleccionar NÃO DECIDE a partir do calendário, antes de qualquer
> medição.
> **Fica por ser o registo de nove constantes que entraram sem derivação.**
> O que sobrevive está em `C4_P8_RESULTADO.md` §4, e usa σ e o calendário.

# ADENDA ao pré-registo do vão — a regra de classificação

**Escrita a 05-09-2026, depois do adversário da C9 e ANTES de qualquer
classificação.** Corrige o `PRE_REGISTO_VAO.md` nos pontos que ele partiu.

> **Esta adenda vai a um adversário independente e espera-se pela resposta
> antes de correr.** Da última vez lancei o adversário e corri sem esperar —
> **lançar não é ver**, e a primeira linha do pré-registo ficou falsa no
> documento escrito para honrar a cláusula. Não se repete.

---

## 0 · O que o adversário partiu, e é aceite por inteiro

1. **`deslocamento` não tinha magnitude.** Com um degrau único simulado, o mesmo
   dado seleccionava os quatro ramos consoante um δ ausente do documento. O `p2`
   não podia decidir nada; o `p8` podia decidir qualquer coisa.
2. **Faltava o ramo de zero transições.**
3. **Não havia controlo negativo.** Com ruído puro e δ pequeno, a regra
   **inventa** acontecimentos (P ≈ 0,6 a 1,0).
4. **A severidade media alcançabilidade, não potência.** Com um degrau
   verdadeiro único, o desenho responderia «dois ou mais» ~60 % das vezes.
5. **O limiar dos 60 dias era o menor número redondo acima do observado**, e com
   a data de 17-06-2025 a margem é **zero** — a lacuna é exactamente 60.
6. **A regra fenológica §7 está ao contrário.** Fenologia pura cancela-se no
   contraste, logo a regra nunca dispara no caso que nomeia; dispara só quando o
   foco fez algo a mais, e descarta-o.
7. **A persistência «duas datas» não é estacionária** — vale 5 dias em Junho e
   70 em Outubro, um factor de 14.

E **eu já vi a série.** Não posso fixar o δ às cegas. É por isso que o que se
segue não escolhe um δ: publica todos.

---

## 1 · A curva de especificação substitui a escolha

Não se declara um δ. **Declara-se a gama, e publica-se o ramo em toda ela.**

```
δ ∈ {0,005 · 0,010 · 0,015 · 0,020 · 0,030 · 0,040 · 0,060 · 0,080 · 0,100}
```

O resultado é a **tabela ramo(δ)**, e é isso que entra no relatório — não uma
célula dela. É a cláusula C5: relatar a distribuição, não a corrida preferida.

**Referência de ruído, declarada e derivável:** σ = desvio-padrão agrupado do
contraste em pares de datas separadas por ≤ 5 dias, dentro do mesmo mês. Mede
ruído de medição sem apanhar fenologia. A gama acima vai de ~1σ a ~20σ para o σ
que se espera (≈ 0,005), e **a gama é fixa independentemente do σ medido** — se
σ sair fora dela, isso é resultado e diz-se, não se re-escala a gama.

**Como se lê a curva.** Um resultado que só aparece numa janela estreita de δ é
frágil e declara-se frágil. Um ramo que domina de 1σ a 10σ é robusto. Se não
houver ramo dominante, a conclusão é **«a resolução deste instrumento não
separa»**, e é uma resposta.

## 2 · Os ramos, agora cinco

| ramo | selecciona-se se |
|---|---|
| **ZERO** | nenhuma transição excede δ |
| **UM** | exactamente uma transição sustentada |
| **DOIS+** | duas ou mais, separadas por um patamar de **≥ 45 dias** sem transição |
| **NÃO É DEGRAU** | declive monótono significativo e nenhuma transição isolável |
| **NÃO DECIDE** | a máscara falha o §4, ou < 30 datas sobrevivem, ou a lacuna excede o limite do §4 desta adenda |

**Persistência em DIAS, não em datas:** uma transição conta se o novo nível se
mantém **≥ 21 dias** e não regressa ao anterior. Fecha a não-estacionariedade
do ponto 7.

## 3 · Controlo negativo — obrigatório, e corre ANTES

Cláusula da literatura (Lipsitch), nomeada na `CLAUSULAS.md` §2 como o remédio
das formas A e B, e ausente do desenho original.

**Duas séries nulas, com a grelha de datas real:**

- **N1 · ruído puro** — contraste constante mais ruído gaussiano de σ medido.
- **N2 · a própria referência** — o contraste `REF − CONTROLO`, duas unidades
  que ninguém alega terem tido acontecimento. É controlo negativo com os dados
  verdadeiros, incluindo a fenologia verdadeira.

**Pré-registado:** para cada δ, a fracção de corridas nulas que devolve ≠ ZERO é
a taxa de falsos positivos, e **publica-se na mesma tabela**. Um δ cuja taxa
nula excede 5 % está marcado como não utilizável, e **a leitura faz-se só na
região em que o nulo se comporta**.

## 4 · O limiar de lacuna — derivado da pergunta, e a fronteira vira eixo

Não se escolhe um número acima do observado. Deriva-se: **a pergunta é separar
um acontecimento de dois**, e dois acontecimentos separados por menos do que a
maior lacuna podem esconder-se como um. Fixando em §2 que um patamar precisa de
**45 dias**, o limite coerente é que a maior lacuna **não exceda 45 dias** — mais
apertado do que os 60 anteriores, e derivado do critério em vez do dado.

A maior lacuna medida é **55 ou 60 dias** conforme se inclua `2025-06-17`.
**Logo este critério não passa, e isso é o resultado, não um problema a
contornar.** A consequência pré-registada: **o ramo DOIS+ fica indisponível ao
longo do buraco de Novembro-Fevereiro**, e diz-se que a série não pode separar
dois acontecimentos aí. Pode separá-los fora dele.

E a fronteira dos 60 dias, em vez de limiar, **passa a eixo da curva**: publica-se
tudo com e sem `2025-06-17`.

## 5 · A regra fenológica, reescrita

A versão §7 era circular. Substituída pela que o adversário propôs, que julga o
controlo contra **a sua própria história**, não contra o foco:

> Uma transição é marcada **fenológica** se, na data em que ocorre, o nível
> absoluto do CONTROLO estiver **fora** do seu envelope sazonal de 2017-2024
> para aquele dia-do-ano. Se o controlo estiver a fazer o que faz todos os anos,
> a transição no contraste **não é** fenológica.

A série 2017-2024 já está em disco. E declara-se **a priori**, não caso a caso:

> **15 de Novembro a 28 de Fevereiro está fora de âmbito para datar
> acontecimentos.** O kiwi é caducifólio; nesse período o contraste mede a
> diferença entre coberturas de solo sob pérgola nua, não copado. Uma transição
> aí não se classifica — regista-se como **não datável**.

Isto é uma perda declarada em avanço, não uma saída de emergência aplicada
depois de se ver que transições incomodam.

## 6 · Severidade — potência, não alcançabilidade

Antes de classificar corre-se, e **publica-se**, a matriz de potência: para cada
δ e cada data de degrau simulada na grelha real, P(ZERO), P(UM), P(DOIS+),
P(NÃO É DEGRAU), e a incerteza de datação em dias.

**Pré-registado:** um δ em que um degrau verdadeiro único devolve «UM» menos de
**70 %** das vezes está marcado **sem potência** na tabela, e a leitura não se
apoia nele.

## 7 · O que continua a não mudar

- Não é instrumento independente. **NÃO TESTÁVEL no portão**, faça o que fizer.
- Não estabelece a natureza da unidade oriental.
- `COM` vem do voo de 2025-07-06, dentro da janela, e `ZONA0 ∩ COM` são **76 de
  202 px**: mede-se 38 % da zona oriental, e a máscara apaga justamente a parte
  que o rastreio assinala com DESCONTINUIDADE. **Declarado, não resolvido.**

## 8 · Ficheiros

`p8_ramos.py` lê `p8_reagregado.json` e escreve `p8_ramos.json`: a curva
ramo(δ), a taxa nula por δ, e a matriz de potência. **Não toca em dados.**
