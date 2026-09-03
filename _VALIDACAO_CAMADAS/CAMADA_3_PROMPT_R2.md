# Camada 3 — Biologia · re-execução R2

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada 3 de uma cadeia de validação, numa **re-execução**. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md`, incluindo a emenda de 29-08 à
regra 1: **herdas também os adversários, e onde um certificado e o seu
adversário discordarem, ganha o adversário.**

Já existe uma `CAMADA_3_CERTIFICADO_R2.md` tua. **Não a deites fora.** Esta
re-execução é para responder a uma coisa só: **a camada 2 foi revista, e o
padrão a que a tua biologia se relaciona mudou de forma.**

## O DELTA — o que mudou por baixo de ti, e só isto

Onze factos (V1–V11) passaram-te da C2 em 29-08. A `CAMADA_2_CERTIFICADO_R2.md`
de 31-08 mexe em quatro deles e acrescenta cinco. **Os restantes sete mantêm-se
inteiros e não precisas de os revisitar.**

| era | passa a ser | porque te toca |
|---|---|---|
| **V2** — o acontecimento atinge os dois focos «na mesma medida», −0,1426 e −0,1439 | **O contraste foco-menos-controlo é −0,1152 e −0,1100**, e é essa a quantidade que sobe. A magnitude absoluta inclui até −0,025 de efeito de plataforma (V10). O rácio degrau/recta foi RETIRADO pelo adversário: o ponto de quebra foi escolhido depois de ver a série. O que passa é a forma da série sem modelo — sete cenas entre 0,824 e 0,879, e duas em 0,756 e 0,693. | Se escreveste «a mesma quantidade», continua verdade **como contraste**. O número muda; a simetria não. |
| **a partição planta/chão do foco oriental** vinha de `nu2021` (ortofoto 2021) | **Passa a ser altura MDS−MDT ≥ 0,5 m** do voo de 06-07-2025. 22,7 % do que a `nu2021` deixava passar como plantado não tem pérgola; metade do disco oriental está abaixo de 0,5 m. | **É a mudança que mais te toca.** Qualquer amostra, ensaio ou unidade tua que se localize «no foco ESTE plantado» pode estar em chão. Reverifica a posição de cada uma contra a partição nova. |
| **não havia instrumento independente para o foco oriental** | **Passa a haver — o Landsat**, −0,0791 com p exacto 0,0110. E fica escrito que o **radar não distingue o oriental**: ele está dentro da sua própria banda de nove Invernos nas duas órbitas, porque metade dele é chão. | A tua camada podia estar a tratar a ausência de instrumento como incerteza sobre o oriental. Deixa de ser. |
| **V10** — o nível absoluto não pode carregar afirmação sobre o pomar todo | **Mantém-se, e ganhou aplicação:** foi ele que obrigou a passar do valor absoluto para o contraste. | Se citaste níveis absolutos, cita contrastes. |

**Acrescenta-se, e é novo para ti:**

- **S5** — três núcleos satélite a 79, 82 e 143 m descem já em 2025 (cena que
  não entrou na sua selecção), com **base 2017-24 normal — 0,878 · 0,872 · 0,901**, contra
  0,867–0,892 nas parcelas do IFAP. **Os percentis foram RETIRADOS pelo
  adversário:** a nula é sorteada a >120 m e dois dos alvos estão a 83 e 112 m.
  O que passa é a base normal e a descida em 2025 — medições directas.
- **S7** — **não há halo.** Sem gradiente contínuo com a distância (p toroidal
  0,55; os anéis não decaem, o do meio é positivo). O padrão compatível é
  o NEGATIVO, e só ele: não há gradiente contínuo. A leitura «descontínuo» é inferência e não desce daqui.
- **S6** — a referência sistemática tem 14 das 110 células dentro dos focos
  (contagem exacta). Que daí resulte serem os números do fosso conservadores é
  **inferência, não medição** — mede-o a reconstrução pré-registada, por correr.
- **G39/G40** (camada 0, R3) — o bloco sudoeste é da mesma exploração: **12,64
  ha de kiwi, todo do ENT 472062**, e coincide com C1a+C1b. **Não há controlo
  externo contemporâneo de kiwi neste caso.**
- **G38** — o voo LiDAR é de 06-07-2025, 14:34:53–14:51:08 UTC, com cálculo em
  disco. A paragem de linha de 29-08 que bloqueava tudo o que dele dependia está
  descarregada.

## O QUE FOI REJEITADO, e não pode voltar

- **O halo.** ρ ingénuo p = 2×10⁻⁹, toroidal 0,55. Não escrevas propagação
  difusiva com base em distância.
- **«O radar confirma os dois focos.»** Confirma um.
- **Qualquer «convergência» entre a moeda do fosso e a do nível absoluto.** Os
  números aproximam-se por compensação de dois enviesamentos opostos; na mesma
  unidade e mesmo estimando diferem exactamente pelo degrau da referência.
- Tudo o que já estava rejeitado em 29-08 continua rejeitado.

## AS TUAS TAREFAS — três, e nomeiam ficheiro

1. **Reposicionar cada amostra biológica contra a partição nova.**
   Ficheiros: `SAIDA_C3\c3_09_organismos.json` e o que localiza as unidades
   ensaiadas; partição em `_VALIDADE_GESTAO\chm_altura.npy` (altura ≥ 0,5 m) e
   `serie_oriental_pergola.json`. **Pergunta: alguma amostra do lado oriental
   caiu em célula sem pérgola?** Se caiu, o que ela mede não é raiz de videira.

2. **Reavaliar se a tua leitura do foco oriental dependia de ele não ter
   instrumento independente.** Ficheiro: a tua `CAMADA_3_CERTIFICADO_R2.md`,
   secções sobre o oriental. **Pergunta: alguma frase tua diz «não confirmado»
   sobre o oriental por falta de segundo instrumento?** Agora há um.

3. **Dizer se a AUSÊNCIA de gradiente com a distância muda alguma hipótese
   biológica tua.** (Não te é dado «padrão descontínuo» — isso é inferência, e
   a camada 2 não tem competência para a fazer.)
   Ficheiros: `_VALIDADE_GESTAO\satelites_sem_2026.json`,
   `halo_distancia.json`. **Pergunta: a ausência de gradiente com manchas
   destacadas favorece ou desfavorece propagação por contacto de raízes?**
   Responde ou declara não testável — não especules.

## O QUE NÃO É TAREFA TUA

Não reabras a etiologia, não opines sobre a causa, e **não voltes a correr o
que já corres-te em 29-08.** Se uma conclusão tua sobrevive ao delta, escreve
«mantém-se» e o número, e passa à frente. A cadeia não precisa de mais
análise; precisa de saber o que ainda é verdade.

---

## AVISO AO ADVERSÁRIO DESTA CAMADA

A `CAMADA_2_CERTIFICADO_R2.md` **foi escrita pela mesma sessão que produziu os
factos que ela certifica**, e o seu adversário (`CAMADA_2_ADVERSARIO_R2.md`)
**também**. O controlo 3 exige sessão paralela e não houve: o adversário apanha
lapsos de execução, não a premissa falsa partilhada. Três coisas por auditar:

1. o controlo tem três valores conforme a exclusão (−0,0136 / −0,0096 /
   −0,0017), e o rácio foco/controlo varia de 9× a 17× conforme a linha; foi
   fixado o mais conservador, e a escolha é do autor;
2. o disco ocidental tem centro lido do défice de 2026, e é o número que a
   maioria das peças cita;
3. a reconstrução da referência está **pré-registada e por correr**, com
   *line-stop* declarado: se os fossos encolherem com a referência limpa, a
   leitura de contaminação está errada e a camada 2 reabre.

**Ataca isto primeiro.**
