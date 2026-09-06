# SAR — o instrumento é compatível com a perda TOTAL do copado e com nada, e não os distingue

**06-09-2026 · revisto no mesmo dia depois da auditoria independente (AUD-15).**
Lido contra `CRITERIO_SAR_v3.md` + adenda, autorizado por adversário antes da
corrida (AUD-14). Produzido por `sar_v3.py` → `sar_v3.json`.

**Estatuto: NÃO TESTÁVEL por falta de potência.** Autorizado pelo portão nessa
forma e só nessa; certificação e auditoria independente **ambas feitas**.

> ## O que a auditoria mudou, e mudou para melhor
>
> A primeira versão desta página dizia «nenhuma célula distingue» e parava aí.
> O adversário reproduziu **os doze Δ, os doze MDE, o portão e o modo comum ao
> último dígito publicado — zero discrepâncias** — confirmou que o nulo é real e
> não fabricado, e depois mostrou que **eu tinha subestimado o próprio achado**
> e que o tecto que usei estava na escala errada.
>
> Corrigiu também quatro defeitos no meu código e três frases minhas.

---

## 1 · O que o instrumento consegue, e é isto que governa tudo

Eu comparei o MDE com uma **amplitude sazonal** (Verão menos Inverno). Está
errado: a pergunta lê-se **no inverno**, e o que interessa é quanto vale o
copado *nessa janela*. Isso mede-se directamente — `zona0 − nu2021`, contraste
de inverno contra chão nu, média dos anos de base:

| | tecto de inverno | |
|---|---|---|
| orb 125 | **+0,484 dB** | é tudo o que a unidade vale em copado |
| orb 147 | **+0,994 dB** | |

E contra ele, os MDE:

| célula | MDE | tecto | |
|---|---|---|---|
| orb125 `zona0−resto` | 1,244 | 0,484 | **2,57×** |
| orb125 `zona0−referencia` | 0,986 | 0,484 | **2,04×** |
| orb125 `zona0−nu2021` | 0,817 | 0,484 | **1,69×** |
| orb147 `zona0−resto` | 1,612 | 0,994 | **1,62×** |
| orb147 `zona0−referencia` | 1,578 | 0,994 | **1,59×** |
| orb147 `zona0−nu2021` | 1,544 | 0,994 | **1,55×** |

> **O MDE excede o tecto de copado de inverno em TODAS as seis células, nas duas
> órbitas, por 1,55 a 2,57 vezes.** Não é «no limite do detectável» numa órbita,
> como escrevi. **Nesta unidade e nesta janela, a perda total do copado é
> indistinguível de zero, em toda a parte.**

## 2 · E o que a unidade fez, que eu não tinha escrito

| | base | tratamento S1A | **S1C** | deslocamento |
|---|---|---|---|---|
| orb125 `zona0−nu2021` | +0,484 | **−0,017** | +0,086 | **−0,501 = −104 % do tecto** |
| orb147 `zona0−nu2021` | +0,994 | **−0,058** | +0,078 | **−1,052 = −106 % do tecto** |

**No inverno de 2025-26 a `zona0` está ao nível do chão nu**, nas duas órbitas,
e o Sentinel-1C — que o critério exclui, e que é por isso uma verificação
parcialmente independente do ano de tratamento — concorda a menos de 0,26 dB.

**E está abaixo do MDE (0,817 e 1,544). Não é distinguível de zero.**

> **A leitura honesta é esta: o instrumento é compatível com a perda total do
> copado e é compatível com não ter havido nada, e não sabe qual das duas.**
>
> É muito mais útil ao leitor do que «nada se viu», e é o mesmo dado.

## 3 · As doze células, e nenhuma distingue

Δ de −0,771 a +0,178, MDE de 0,99 a 1,61, nas duas bases. **Nenhuma célula
distingue.** As órbitas discordam em sinal no comparador `referencia`: −0,518 na
125 e +0,097 na 147 — publicado sem síntese, como o §1 manda. O posto não vai
publicado em célula nenhuma.

Detalhe que o adversário mandou registar e é honesto: em orb125 o Δ é **−0,52 a
−0,77 — a mesma direcção do declínio óptico**, a 40-60 % do MDE; em orb147 é
**+0,10/+0,18, a direcção oposta**. Duas órbitas, dois sinais, nenhum a chegar à
resolução.

## 4 · O modo comum disparou — nas duas bases, e não «o pomar inteiro»

| órbita | base | `referencia` | `resto` | **comum** |
|---|---|---|---|---|
| 125 | n=10 | +0,638 | +0,891 | **+0,764** |
| 125 | n=9 | +0,498 | +0,776 | **+0,637** |
| 147 | n=10 | +0,659 | +0,889 | **+0,774** |
| 147 | n=9 | +0,596 | +0,832 | **+0,714** |

**A frase correcta é «as duas unidades de controlo subiram 0,64 a 0,77 dB»** —
não «o pomar inteiro», que era uma afirmação sobre um conjunto que a estatística
não cobre. E é falsa para uma órbita: em orb125 a `zona0` subiu **+0,12** contra
+0,76 dos controlos.

O resultado fica rotulado **«modo comum não separável»** e não se lê como
acontecimento na `zona0`.

**A explicação pela chuva é hipótese, não leitura.** O inverno é o 2.º mais
chuvoso dos onze, e a associação chuva/nível existe nos anos de base — mas na
órbita 147 **deixa de ser significativa (p = 0,127)** quando se retira o ano
cuja chuva é **zero por ausência** (IX-06), e nessa órbita o ano de tratamento
fica **2,5 desvios acima do que a sua própria chuva prevê**. O §6 da versão
anterior chamava-lhe «evidência directa para o P4»; é um grau a mais.

## 5 · Quatro defeitos no meu código, apanhados pela auditoria

| | |
|---|---|
| **D1** | **o portão de abortar não podia abortar** — a variável era escrita e nunca lida. Forma B, dentro do elemento retomado para fechar essa forma. Corrigido: agora levanta `SystemExit` |
| **D2** | o portão e o modo comum corriam **numa base só**, quando a adenda manda as duas. E o modo comum é a única estatística sobre **níveis**, onde um meio-inverno sem Nov nem Dez não se cancela. Corrigido — e é a razão de o número passar a ser um intervalo |
| **D3** | **o posto ia suprimido no ecrã e escrito no JSON.** A porta que a adenda fechou em prosa estava aberta no artefacto durável. Corrigido |
| **D4** | os **níveis absolutos** que o §5 mandava publicar não estavam em lado nenhum. Corrigido |

## 6 · O portão

```
«o radar nao distingue», como veredicto positivo   -> BLOQUEADO
o mesmo, NAO TESTAVEL com a razao de potencia      -> AUTORIZADO
```

**A condição 2 continua aberta.** E o adversário nota que o portão **não vê
potência**: nada nele compara Δ com um MDE nem vê que o MDE excede o tecto. A
esta conclusão chegou-se por fora do aparelho.

## 7 · O que isto NÃO diz

- **não confirma nem contradiz o óptico.** Escrevi «não contradiz», e é vácuo:
  o critério pré-registou **bilateral**, portanto um nulo não pode contradizer
  coisa nenhuma. A frase certa é **«o SAR não tem potência para confirmar nem
  para contradizer»**;
- **não fecha declínio contra arranque** — o P3 corre a seguir;
- **não testa o encharcamento;**
- **não fecha a rota do SAR.** Fecha-a **para esta unidade**. O adversário
  encontrou, na mesma janela e com a mesma maquinaria, uma unidade em que o
  desenho **distingue nas seis células** — mas encontrou-a **depois** de ver este
  nulo, e por isso **não conta**: entra como candidata a pré-registo próprio, com
  a ficha de fuga da C3 preenchida antes, e não como resultado.

## 8 · Correcções de números

- **«1613 cenas» era o ficheiro que o IX-01 proíbe.** A série entregue tem
  **1013**. Eu tinha creditado o produto com o tamanho do ficheiro corrompido —
  o IX-01 a vazar de volta para jusante.
- **O tecto «+1,02 / +2,05» não tem produtor.** Não há guião em disco que o
  calcule; o adversário teve de o reconstruir por força bruta para descobrir que
  era uma amplitude sazonal. É a cláusula S2 — *um número sem produtor é boato
  com casas decimais* — e era a base inteira do argumento de potência.
