# Encerramento da auditoria — ciclo de 31-08-2026

**Estado: FECHADO com condições.** A cadeia foi retomada, percorrida de C0 a
C5, atacada por um adversário independente em Controlo 3, e as decisões dele
foram aplicadas. Fica um documento que diz o que se pode escrever, o que não se
pode, e o que falta.

---

## 1 · O QUE ESTE CICLO PRODUZIU

| documento | o que faz |
|---|---|
| `CAMADA_0_REVISAO_R3` | fecha duas NÃO TESTÁVEIS: a data do voo (com cálculo em disco) e a pertença do bloco sudoeste |
| `CAMADA_2_CERTIFICADO_R3` | **o certificado operativo.** Substitui a R2 e o `T1_T5`, que eram duas listas com o mesmo nome |
| `CAMADA_2_ADVERSARIO_R2` | o adversário interno — apanhou quatro coisas, e não podia apanhar mais |
| `CAMADA_2_CONTROLO3_ADVERSARIO` | **o adversário independente.** Apanhou seis, incluindo duas que o interno não podia ver |
| `CAMADA_3_CERTIFICADO_R3` | biologia: nada muda, B7 reforça-se, e o esforço de amostragem estava invertido |
| `CAMADA_4_CERTIFICADO_R2` | inferência: o D1 passa a coordenadas; a atribuição de válvulas não sustenta quantidades |
| `CAMADA_5_CERTIFICADO_R2` | decisão: dez retiradas aceites, e a campanha redesenhada |
| oito scripts | `l1`, `t1`–`t5`, `c3_r2_01`, `c4_r2_01` |

## 2 · O QUE O CONTROLO 3 DERRUBOU, E QUE SOBE

O adversário independente retirou cinco coisas. Duas delas **eu não podia ter
apanhado**, e é exactamente por isso que o controlo existe:

**O T5 era um teste que não podia falhar.** O fosso é `referência − unidade`,
logo limpar a referência desloca todos os fossos pela mesma constante. As cinco
variações são **+0,008430**, idênticas à nona casa. Escrevi «cinco fossos
cresceram, nenhum encolheu» como cinco confirmações; é um número repetido cinco
vezes. **O ramo do *line-stop* era inalcançável por construção.**

**O B1 não é comparador.** Zero instrumentos independentes, e a recta ganha
porque o bloco está em subida — não porque não houve evento. E o veredicto
dependia de um limiar `> -0.03` que inventei sem justificação.

E confirmou o que já se sabia e nunca fora corrigido: **o cabeçalho do
`landsat_independente.py` prometia um filtro que o código não tem**. Apanhado
pelo adversário interno, contado pelo T4, e só agora corrigido no ficheiro.

## 3 · A PROPAGAÇÃO PARA CIMA — o que cai nas camadas 4 e 5

| onde | o que cai | porquê |
|---|---|---|
| **C4 · D4** | «os fossos são limite inferior — **medido** pelo T5» | volta a **inferência**. O T5 não o mediu. A conclusão mantém-se (a C0 já a tinha), o estatuto não. |
| **C5 · COMP-01** | a terceira condição de arranque da campanha, baseada no B1 | **cai com S9.** O bloco sudoeste continua a ser a única outra unidade de kiwi da exploração e continua por medir — mas **não é um comparador**, é uma lacuna. Passa de condição de arranque a **acção de valor desconhecido**. |
| **C5 · árvore** | ficam **duas** condições de arranque, não três | TEMP-01 (as onze cenas, custo zero) e REG-01 (a comparação regional, custo baixo) |

**Nada mais cai.** As dez retiradas da C5, a reformulação do D1 em coordenadas,
o D9 e as correcções da campanha — 60 amostras com folha, controlo de
proximidade no oriental, painel bacteriano — mantêm-se inteiras.

## 4 · O QUE O RELATÓRIO PODE AFIRMAR

Com a moeda reposta — **o fosso é a moeda de registo, e é conservador**:

1. Houve **pelo menos um acontecimento** entre Agosto de 2025 e Julho de 2026,
   que atingiu duas posições do pomar e não o resto dele.
2. O contraste foco-menos-controlo é **−0,115** e **−0,110**, ±0,02–0,03, e o
   sinal e a ordenação sobrevivem a **43 corridas** e a **quatro reconstruções**
   independentes da geometria de rega.
3. **O degrau bate a recta** com o ponto de quebra contabilizado: ΔAICc −6,6 a
   −7,6 nos focos, **+6,4 no controlo**.
4. Um **segundo satélite**, de outra agência, data o mesmo acontecimento com p
   exacto no mínimo que catorze anos permitem — **direcção e datação, não
   magnitude**, com n = 35 e 27 píxeis.
5. O **radar** — outra física — distingue o disco ocidental.
6. A composição dos dois sítios é **oposta**, por coordenadas, e é robusta às
   quatro reconstruções.
7. **Nenhum ensaio bacteriano ou viral foi alguma vez feito.** A PSA nunca foi
   pedida a nenhum laboratório.

## 5 · O QUE O RELATÓRIO NÃO PODE AFIRMAR

- «**um** acontecimento» — o número não está estabelecido, e **é respondível
  hoje** com onze cenas já inventariadas;
- «**antes e depois**» com material biológico — todas as amostras com posição
  são posteriores a Março de 2026;
- **área por válvula** — varia até 50× entre reconstruções;
- **propagação não contígua** — no estrato correcto os núcleos estão nos
  percentis 9,6 / 14,2 / 29,2 %, e um deles está dentro do disco do próprio foco;
- «**não há halo**» — o nulo toroidal não tem potência declarada; é NÃO
  TESTÁVEL, não negativo;
- «**excluída**» para as quatro linhas EXCLUÍDA-LOCAL;
- que existe **controlo externo** — não existe, e é medição, não omissão;
- que o **B1** é comparador de coisa nenhuma.

## 6 · A CONDIÇÃO QUE FICA ABERTA, E É A MAIOR

> **O foco oriental é copado em declínio, ou copado arrancado e re-armado?**

A partição que sustenta toda a leitura — `altura ≥ 0,5 m` — vem de um voo que
cai **dentro da janela do acontecimento**. «Ter pérgola» é um estado
**pós-tratamento**. A C0 registou 41,4 % da `zona0` como chão lavrado em 2021,
1,04 ha no seu centro.

**O teste que separa as duas hipóteses está no `PROTOCOLO.md` como condição de
arranque desde a C2 original e nunca correu:** prominência de pérgola por
autocorrelação radial sobre a ortofoto de 2025, o mesmo método do
`c2_12_pergola_2012.py` que já separou unidades com p ~ 1e-200.

Enquanto não correr, **a C3 e a C4 estão a construir etiologia sobre uma unidade
cuja natureza não foi estabelecida** — que é, com outra roupa, o mesmo erro do
lóbulo oeste que abriu esta cadeia.

## 7 · A FILA, POR VALOR

| | acção | custo | decide |
|---|---|---|---|
| **1** | prominência de pérgola sobre a ortofoto de 2025 no foco oriental | baixo | **declínio contra arranque.** Fecha a maior condição aberta |
| **2** | TEMP-01 — as onze cenas de plena estação já inventariadas | **nenhum** | um acontecimento ou dois |
| **3** | REG-01 — a comparação regional, 1 054 ha por serviço aberto | baixo | local ou regional |
| 4 | potência do nulo toroidal | baixo | se «não há halo» é negativo ou lacuna |
| 5 | o bloco sudoeste em LiDAR, Landsat e SAR | médio | se é comparador ou lacuna |

**Nenhuma medida irreversível antes das três primeiras.**

---

## 8 · O QUE ESTA AUDITORIA APRENDEU SOBRE SI PRÓPRIA

Seis vezes neste ciclo apresentei como novo um facto já certificado — a
quarentena do `sentinel_b1`, o veredicto de C1a/C1b, a causa da subida do resto
do pomar, o bloco do B1 com as suas 96 especificações, a contaminação da
referência (duas vezes: C0 §3.2 e C3 B10). **Nenhuma foi apanhada por
recomputação. Todas por leitura de um documento que já existia.**

E o Controlo 3 pagou-se na primeira leitura, com duas coisas que a
auto-adversarialidade não podia ver: um teste que não podia falhar, e um
comparador sem instrumentos. **O tecto da auto-crítica é real e mede-se.**

A regra prática que sai daqui, e que vale mais do que qualquer dos números
acima: **antes de correr um teste sobre uma unidade, procurar o nome dessa
unidade nos certificados, nos adversários e nos veredictos.** Cinco minutos de
busca teriam poupado seis re-derivações.

---

**Auditoria encerrada em 31-08-2026.** Aberta em 28-08 pelo erro da AOI do
lóbulo oeste; fechada com a mesma classe de erro identificada num sítio novo — e
desta vez nomeada antes de chegar a uma conclusão.
