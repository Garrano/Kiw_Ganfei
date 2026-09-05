# Controlo 4 · P8 — o vão preenchido, e a regra de classificação retirada

**Data:** 05-09-2026 · **Alvo:** as 49 cenas do vão + a regra que as ia classificar
**Instrumentos:** portão, adversário sobre o pré-registo, **adversário sobre a
regra de classificação antes de a correr** — a C9 cumprida pela primeira vez.

---

## 1 · A C9, à terceira

Primeira tentativa: não houve adversário. Segunda: lancei-o e corri sem esperar
— **lançar não é ver**, e a primeira linha do pré-registo ficou falsa no
documento escrito para a honrar. Terceira: escrevi a regra, mandei-a, **esperei**,
e ela voltou partida. É por isso que ainda estava livre para mudar.

O adversário registou-o: *«a adenda foi escrita antes da classificação, e a
classificação não correu — `p8_ramos.json` não existe em disco.»*

## 2 · O que ele partiu, e verifiquei

**σ estava errado por 5,5×.** A adenda escreveu «σ ≈ 0,005». Medido pela receita
da própria adenda — desvio-padrão de pares a ≤ 5 dias no mesmo mês:

```
contraste_OC   n_pares=40   sd(dif)=0,0392   σ = 0,0277
contraste_OR   n_pares=40   sd(dif)=0,0329   σ = 0,0233
```

A grelha de δ que fixei julgando ir de **1σ a 20σ** vai de **0,2σ a 3,6σ**. A
regra de leitura — «um ramo que domina de 1σ a 10σ é robusto» — refere-se a uma
região que a grelha não contém: 10σ ≈ 0,28, quase o triplo do topo da grelha.

E o degrau é **~6σ**, não os ~34σ que eu implicava sem o dizer.

**A amplitude do degrau simulado do §6 nunca foi escrita.** É o defeito do δ
reencarnado uma secção depois de o corrigir: quem escolhe a amplitude escolhe
que δ ficam «sem potência», logo a região legível, logo a resposta.

**O δ máximo, 0,100, é o maior valor redondo ABAIXO do degrau de ~0,13 já
publicado.** O adversário anterior tinha apanhado o limiar dos 60 dias por ser o
menor redondo *acima* do observado. Repeti o padrão em espelho, no topo da
grelha, tendo escrito no §0 que já vira a série.

**Os dois controlos negativos são inválidos.** O N2 (`REF − CONTROLO`) assume o
nulo em vez de o conhecer — «ninguém alega que tenham tido acontecimento» é
**ausência tratada como aprovação**, a forma que este aparelho já fechou sete
vezes, reintroduzida na secção escrita para a fechar. E o próprio `guarda.py`
documenta que o pico de pérgola da REF **se moveu de 5,25 m para 9,88 m** — é
uma unidade que o processo já apanhou a mudar de natureza. O N1 gaussiano ignora
autocorrelação e caudas: excesso de curtose 6,07, eventos a |z|>3 a **oito vezes**
a taxa gaussiana.

**A regra fenológica reescrita continua cega à ameaça que nomeia.** O §7 original
dizia que o risco é o **foco** abrolhar de maneira diferente; o §5 interroga só o
**controlo**. No caso nomeado o controlo faz o que faz todos os anos, logo a
regra diz «não é fenológica» e mantém a transição. Corrigi a polaridade e mudei o
ponto cego de sítio.

E é **inexecutável em 47 % das posições**: o envelope sazonal de 2017-2024 só
existe para Junho-Setembro. Outubro, Março, Abril e Maio têm **zero** cobertura
histórica — a Primavera, que é a estação de maior mudança fenológica num
caducifólio, e exactamente aquela para que a regra existe.

**E o pior: um critério auto-anulante.** O §2 diz NÃO DECIDE se a lacuna exceder
o limite; a maior lacuna é 55 e o limite que derivei é 45. **O §2 selecciona NÃO
DECIDE.** O §4 diz a seguir que o DOIS+ fica indisponível no buraco mas
disponível fora dele. Duas secções, um conjunto de dados, saídas contraditórias,
e **nenhuma regra de precedência**.

Pior ainda: essa selecção depende **só da grelha de datas**, conhecida antes de
eu escrever a adenda. `55 > 45` não envolve δ, nem σ, nem medição nenhuma. **O
`p2` falhou porque nenhum ramo era alcançável; a minha adenda falha porque
exactamente um é alcançável, e sem olhar para a medição.** Mesma forma, sinal
oposto.

## 3 · O que aguentou

- **A máscara de nuvem funcionou** — r = −0,166 e −0,225 contra +0,86 e +0,99 no
  `p2`. É a correcção mais forte de todo o trabalho, e está verificada.
- **As quatro datas caídas caíram por razão pré-registada**, não por
  conveniência: três não têm SCL, uma tem zero píxeis válidos. A versão
  corrigida é **mais estrita** (47 contra 50), não mais permissiva — a correcção
  custou-me datas.
- **Publicar o ramo ao longo de uma grelha é o instrumento certo** (Simonsohn);
  o defeito foi a grelha estar mal especificada, não a ideia.
- **A persistência em dias fecha mesmo a não-estacionariedade** — «duas datas»
  valia 5 dias em Junho e 70 em Outubro.
- **CONTROLO e REF são mesmo disjuntos**, 90,02 m medidos.
- **O §7 é honesto** sobre os 76 de 202 px e sobre a máscara apagar a parte que
  o rastreio assinala com DESCONTINUIDADE.

## 4 · O que se aguenta afirmar, sem nenhuma das constantes contestadas

Retiro a regra de classificação. Não a conserto: o que ela ia produzir não
precisa dela. Isto usa **σ medido e o calendário**, e mais nada:

| | |
|---|---|
| ruído do contraste (receita declarada) | **σ = 0,028** |
| contraste OC, Agosto a Outubro de 2025 (16 cenas) | **≈ −0,055** |
| contraste OC, Maio a Julho de 2026 (14 cenas) | **≈ −0,21** |
| diferença | **≈ 0,16 ≈ 5,7 σ** |
| maior lacuna na série | **55 dias** (29-12-2025 a 22-02-2026) |
| período não legível para copado | **15-11 a 28-02** — o kiwi é caducifólio |

> **A mudança é real e está enquadrada entre meados de Outubro de 2025 e finais
> de Abril de 2026. Quantas transições a produziram NÃO é determinável com este
> instrumento** — o intervalo é simultaneamente o mais mal amostrado (lacuna de
> 55 dias) e o único em que o contraste não mede copado.

E o que se ganhou face ao `p2`, que é real: a interpolação passou de **310 dias
para ~190**, e **Setembro e Outubro de 2025 estão ao nível de Agosto**, com dez
cenas. Até meados de Outubro não tinha acontecido nada. Isso o `p2` não podia
dizer.

## 5 · Consequências para o registo

- **`AF-07` («houve UM acontecimento e não dois») mantém-se PRETENDIDA.** A
  resposta afirmativa não existe, e agora sabe-se porquê e com que resolução.
- A frase da `LISTA_FINAL` §F não muda.
- **Entra uma afirmação nova**, se passar o portão e o registo: o enquadramento
  do §4 acima.
- O que a desbloquearia não é mais NDVI. É um **instrumento independente** que
  cubra Outubro-Abril: SAR Sentinel-1, que não depende de folha nem de luz, e
  cuja série actual pára no inverno de 2024-25 por escolha, não por falta de
  dados.

## 6 · A lição

Construí uma curva de especificação, um controlo negativo, uma matriz de
potência e uma regra fenológica reescrita — e o adversário mostrou que **nove
constantes novas tinham entrado sem derivação**, três delas escolhidas em
relação a valores que eu já tinha visto. A maquinaria não estava a medir: estava
a cobrir o facto de a resposta ser estreita.

A resposta estreita cabe em cinco linhas e usa σ e o calendário.
