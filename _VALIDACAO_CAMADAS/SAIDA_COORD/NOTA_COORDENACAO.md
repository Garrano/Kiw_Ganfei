# Nota de coordenação — a re-derivação que a C5 não chegou a fazer

29-08-2026. **Isto não é um certificado e não entra em nenhuma lista fechada.**
É trabalho do coordenador a substituir uma camada que não pôde correr.

## Porque existe

O `CAMADA_5_ADVERSARIO.md` acusou a `c5_01_reetiquetagem.py` de descrever no
cabeçalho uma árvore que lê os campos de evidência e de, no código, não ler
nenhum deles. **Verifiquei, e é verdade.**

O CSV de entrada da C4 tem as colunas

```
ambito · prova (certificado e numero) · instrumento independente ·
margem e leitura · o que a fecharia
```

e o código da C5 lê `id`, `classe`, `causa`, `estatuto`, e depois chaves que
são as suas próprias colunas de **saída** — um dicionário escrito à mão. E o
CSV que produz **deita fora as cinco colunas de evidência**: o rasto de prova
corta-se na última camada, que é onde sai para o mundo.

**É a estrutura exacta do `fazer_masks_v2.py`** — docstring a dizer uma coisa,
código a fazer outra —, que é o erro que deu origem a esta cadeia.

A C5 foi mandada refazer e **bateu no limite de sessão**. Isto substitui-a
apenas nesta tarefa, e fica marcado como coordenação.

## O que se fez

`coord_reetiquetagem.py` aplica a árvore que a **própria C5 declarou**, com
regras explícitas sobre os campos de evidência, **cada linha a citar o campo e
o excerto que disparou a regra**. As regras saíram de um levantamento prévio
dos padrões que existem mesmo no texto, não de suposição.

Saída: `coord_reetiquetagem.csv`, **com as colunas `prova` e `instrumento`
repostas**.

## O que se conclui — e o que NÃO se conclui

**Não se conclui que 36 etiquetas estejam erradas.** Divergem 36, e a maior
parte da divergência é **a minha regra a ser mais grosseira do que o juízo da
C5**, não o contrário:

- **13 divergências** são a regra R6 devolver `COM INSTRUMENTO INDEPENDENTE`,
  que **não é um estatuto** — é um facto ortogonal e não decide entre excluída
  e sustentada.
- **5 divergências** são eu derivar `NUNCA PROCURADA` onde a C5 escreve
  `SÓ FORA DE GANFEI`. **A dela é melhor:** diz onde foi procurada.

**Armadilha em que o coordenador caiu, e fica registada.** A regra R6 dispara
quando o campo `instrumento independente` **começa por «SIM»**. Para a
**INS-01** começa — e o adversário já estabelecera que o que se segue são
«quatro corridas independentes com personas diferentes», isto é **analistas,
não instrumentos**. Confiei na etiqueta do campo sem ler o que vinha a seguir.

## O que se confirma

- **As nove `ENCONTRADA SEM PAR` derivam-se sozinhas do texto.** São os nove
  organismos do «Kiwi 1000» / informe 331/2025. O núcleo é sólido.
- **O bloco das `NUNCA PROCURADA` bate quase todo** (17 derivadas contra 18
  escritas).

## As divergências substantivas — três, e coincidem com o adversário

**1 · BIO-13.** O `ambito` diz «nenhum ponto»; a C5 escreve `ENCONTRADA SEM
ENSAIO`. O adversário apontou a mesma linha porque o campo `resultado` diz
**«por confirmar»**. É contada como encontrada e não está confirmada.

**2 · As quatro `EXCLUÍDA-LOCAL` — BIO-10, BIO-11, BIO-12, BIO-14.** Da
evidência textual **não sai exclusão em nenhuma**: sai «medida sem poder»,
«negativo com poder por declarar», «par por verificar», e uma que o texto não
determina. Coincide com o adversário: três declaram instrumento «nenhum» e a
quarta declara um número de expediente, que é proveniência e não instrumento.

**3 · INS-01.** Já retirada pelo adversário pela mesma razão por outro caminho.

## O achado principal

> **Quinze das 59 etiquetas não são deriváveis do texto do livro-razão.**

Nessas, a etiqueta é **juízo puro**. Pode estar certa — o juízo é o produto
desta camada e a C5 diz isso no cabeçalho — mas **não é auditável a partir do
que está escrito**, e um livro-razão que sai para o mundo tem de dizer quais
são as quinze.

São: BIO-11, ABI-04, ABI-05, ABI-09, ABI-12, GES-04, GES-06, GES-07, REG-01,
REG-02, REG-03, INS-02, INS-04, INS-05, INS-06.

## O que fica por fazer, e é da C5

1. Reescrever a `c5_01_reetiquetagem.py` para **ler mesmo** os campos de
   evidência, e transportar `prova` e `instrumento independente` para a saída.
2. Declarar as quinze linhas de juízo puro **como tal**, no livro-razão.
3. Corrigir BIO-13 e reabrir as quatro `EXCLUÍDA-LOCAL`.
4. Os quatro defeitos do desenho de amostragem: **zero amostras de folha**, a
   segunda radial a 90° marcada «opcional», a U2 sem controlo de proximidade no
   B3, e a REG-01 que é raiz da árvore e não é condição de arranque.
5. Certificar a série Landsat, que **cinco certificados consecutivos declararam
   sem certificar**.

## Ficheiros

```
coord_reetiquetagem.py    a derivacao, com as regras explicitas
coord_reetiquetagem.csv   59 linhas, com prova e instrumento repostos
```
