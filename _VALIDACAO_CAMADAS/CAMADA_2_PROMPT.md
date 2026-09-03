# Camada 2 — Sinal vegetal

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a camada C2 de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md` e `CONTROLOS.md` — os três
controlos aplicam-se-te por inteiro.

**Nota de proveniência deste prompt:** foi escrito pela sessão principal, não
pela C1. A C1 terminou o certificado e as figuras mas parou antes de escrever
o prompt seguinte. O conteúdo abaixo sai do `CAMADA_1_CERTIFICADO.md` e da
`CAMADA_0_REVISAO_R2.md`; se discordares de alguma transcrição, vai à fonte.

## O que herdas — e só isto

Duas listas fechadas, por esta ordem de precedência:

1. `CAMADA_0_REVISAO_R2.md` — **substitui** a secção PASSA PARA CIMA do
   `CAMADA_0_CERTIFICADO.md`. Oito dos vinte e quatro factos originais foram
   corrigidos e dois retirados. Onde o certificado e a R2 discordarem, **a R2
   ganha**.
2. `CAMADA_1_CERTIFICADO.md`, secção PASSA PARA CIMA — S1 a S19.

E o `REGISTO_DE_NOMES.md`, com uma correcção que a C1 já assinalou: **as
tabelas de válvulas desse ficheiro estão desactualizadas — usar
`ganfei_s2\valvulas_por_area.json`.**

## Vocabulário — não uses outro

Os dois focos identificam-se por coordenada. A nomenclatura esteve invertida
durante semanas e isso já custou tempo.

| | FOCO OESTE | FOCO ESTE |
|---|---|---|
| centro | E530485 N4655053 | E530977 N4655117 |
| nome da exploração | **«Zona 0»** | por confirmar; o ajuste põe-no em B3 |
| válvulas | 8 (a 34 m), 9 | 13 (81 m), 14 (93 m) |
| cota mediana | 6,64 m — ponto baixo | 7,83 m — ponto alto |
| distância à drenagem | 13,4 m | 55,8 m |
| solo | carência de cálcio confirmada em duas matrizes | o mais pobre da exploração |
| radar, dez Invernos | nunca anómalo, **até 2025-26** | sempre −0,95 a −1,11 dB |
| amostras | 4 ITS + «Kiwi 1000» | só nemátodos (as contagens mais baixas) |

## O que a tua camada tem de fazer

**A tarefa central: refazer a série com as máscaras geográficas e dizer o que
sobrevive.** O conjunto operativo é `ganfei_s2\sentinel\masks_geograficas.json`.
O antigo `masks.json` era circular (`pomar` = `nd2026 > 0,78`, `manchaW` =
`nd2026 < 0,76`) e fica só como histórico.

Especificamente:

1. **A grandeza é a magnitude**, não a fracção (R2 G31). A fracção satura — o
   foco ESTE chega a 100 % em 2026 — e deixa de distinguir. Reporta sempre a
   magnitude *com o nível absoluto ao lado*, porque a referência sistemática
   está ela própria a descer (−0,00395/ano) e um fosso constante contra uma
   referência que desce é uma afirmação diferente de «isto declina».

2. **Datar o evento, e testar a datação.** O défice do polígono faz 8,08 ha
   (2017) → 4,05 (2020) → 2,91 (2024) → 5,43 (2025) → 7,86 (2026). Seis anos a
   melhorar e dois a duplicar. Isso é o achado central do caso: verifica-o,
   ataca-o, e diz se aguenta.

3. **O cruzamento que ninguém fez ainda, e é teu.** A C1 encontrou no radar
   (S15) que o foco OESTE **nunca esteve anómalo em dez Invernos e cai para
   −1,107 dB no Inverno de 2025-26** — o maior desvio da série — enquanto o
   pomar inteiro está no seu menor desvio. Se o NDVI e o SAR datarem o mesmo
   evento no mesmo sítio por instrumentos independentes, isso é a verificação
   mais forte que este caso pode produzir. **Mas a C1 avisa que o *lugar* é
   circular** — o disco do radar foi centrado onde o NDVI caiu. Desenha o
   teste que separa o momento do lugar, e se não conseguires, diz que não
   conseguiste.

4. **A Mancha W emerge sozinha** (R2 G29): 2,69 ha em 2026, centrada a 7 m do
   centro da máscara antiga, e **ausente em 2024**. Confirma, e testa a
   sensibilidade ao limiar e ao elemento estruturante.

5. **A parte plantada do foco ESTE** cai −0,0150/ano com p = 0,032 depois de
   se lhe remover o chão lavrado de 2021 (R2 G30, C1 S12). Refaz e diz se a
   significância aguenta com a definição de défice fixada.

## O que NÃO podes fazer

**Nenhuma série do B1.** Foram três tentativas e as três estão contaminadas:
pelo invólucro do controlo (46 % das células com variabilidade inter-anual
acima do p90 do kiwi — culturas em rotação misturadas), pela rede a entrar e a
sair (só o B1 teve rede, no período do Enza Gold, e a remoção coincide com a
enxertia de ~2020), e pelas duas sobre-enxertias de 2016 e 2020. As três
explicações estão em cima da mesa e nenhuma série actual as separa.

**Não comparar níveis de NDVI entre B1 e corpo principal**, pela mesma razão.

**Não ressuscitar a linha térmica.** A C1 retirou-a com números novos (S17): o
acoplamento ΔT–ΔNDVI é **−0,925 no controlo interno fora do pomar**, portanto
é genérico da superfície, e o «r = −0,756» que circulava era o Spearman do
foco ESTE sozinho. Só volta com LST nocturno ou temperatura de solo medida.

**Não teorizar sobre patogénios nem sobre causa.** Isso é C3 e C4.

## Erros já cometidos nesta matéria — não os repitas

- **Máscaras derivadas do sinal que se vai medir.** Foi o erro central. Quatro
  auditorias passaram por cima dele porque ninguém leu o docstring e o código
  juntos.
- **Referência escolhida por parecer sã.** Media a distância ao melhor caso, e
  subia por construção.
- **A fracção de píxeis como teste.** Satura e esconde a mudança.
- **Comparar brilho de ortofotos entre épocas.** Radiometrias incomparáveis;
  produziu um achado que teve de ser retirado.
- **Classificar como «nunca esteve são» o que estava em défice na primeira
  cena.** A ortofoto a 25 cm mostrou linhas de pomar contínuas lá.

## O que entregar

1. `CAMADA_2_CERTIFICADO.md`, as cinco secções do protocolo. A secção PASSA
   PARA CIMA é uma lista fechada — sê avaro.
2. `CAMADA_3_PROMPT.md` (biologia), seguindo `MODELO_PROMPT.md`.
3. Código e figuras em `SAIDA_C2\`.

Reporta as quantidades-âncora do `CONTROLOS.md` mais as que a R2 e a C1
fixaram: `pomar` 30,31 ha, referência sistemática 1,10 ha / 110 células, banda
contígua 27,30 ha, tabela total 44,93 ha, MDT em `SAIDA_C1\c1_03_dem50.npy`.

**A tua camada leva adversário** (`ADVERSARIO_PROMPT.md`), como a C0. É uma
das duas com raio de explosão grande. Escreve o certificado a contar com isso.

Não modifiques nada em `Downloads\ganfei_s2\`.
