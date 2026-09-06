# AUD-17 — o LiDAR aguenta-se, e não responde à pergunta. E há duas perdas, não uma.

**06-09-2026.** Certificação e auditoria independente de dois guiões que correram
a 29-08 e nunca tinham passado por nenhuma das duas. Forma H, quarta vez no dia.

---

## 1 · O LiDAR é um instrumento sólido, e é o primeiro genuinamente independente

O adversário reproduziu o `chm_altura.npy` **a partir dos ladrilhos brutos**:
19 958 células, **dif. máxima 0,000e+00**, os mesmos 42 NaN.

E a datação, que era a ressalva do próprio ficheiro, **resolve-se e melhora**: as
duas folhas LAZ dão **06-07-2025, 14:34 a 14:51 UTC**, um só dia — e **100 % das
células de todas as unidades** caem nas duas folhas datadas. O aviso do cabeçalho
sobre «catorze meses» é **texto morto, não ressalva viva**, e deve sair.

As âncoras discriminam, e discriminam **melhor depois de limpas**: referência
p25 = 0,986 contra chão nu p75 = 0,000. E há uma verificação bonita: a
correlação célula a célula entre a altura LiDAR e o NDVI de Verão sobe
monotonamente à medida que se aproxima da data do voo — 0,225 em 2017, 0,455 em
2021, 0,733 em 2025. **Um instrumento partido não se ordenaria pelo tempo.**

> **Fecha a condição 2 do portão para factos instantâneos.** É o que o SAR não
> fez. `guarda.py`: um facto NDVI confirmado pelo LiDAR, com `instantanea()`
> assinada, é **AUTORIZADO**.

## 2 · E não pode responder à pergunta que lhe fizemos

A pérgola nua são postes e arames a ~2 m. Se o LiDAR os contasse, não distinguia
«pérgola sem planta» de «pérgola com planta». **Conta-os? Não — e é pior.**

À densidade medida (16,6 e 17,8 pontos/m²), uma pérgola intacta **sem planta
nenhuma** move a estatística em:

```
postes + arame  ->  0,018 de fraccao alta
desvio entre celulas do chao nu  ->  0,135
```

**Sete vezes abaixo de um desvio.** E confirmado empiricamente: nas células
«vazias», os pontos entre 1,5 e 2,5 m são 5,15 % em N3 contra 4,46 % em chão
lavrado, e **todos os pontos acima de 1,5 m em todas as unidades classificam
como vegetação** — zero retornos estruturais em lado nenhum.

> **O LiDAR mede folha, não estrutura. Não separa «instalação removida» de
> «instalação de pé, planta morta ou arrancada» — as duas leem baixo.**
>
> É a resposta a declínio-contra-arranque: **este instrumento não a dá**, e
> nenhuma reescrita o muda.

## 3 · Mas dá outra coisa, e é o achado do dia

Os 3,77 ha sem pérgola **não são uma coisa só**. Verificado por mim:

| | ha | NDVI Jul-2024 | Jul-2025 | Jul-2026 |
|---|---|---|---|---|
| já em `nu2021` — **nunca teve copado** | **1,57** | 0,594 | 0,592 | 0,616 |
| **fora** do `nu2021` — **perdeu copado** | **2,20** | **0,829** | 0,720 | 0,650 |
| pomar com pérgola | — | 0,898 | 0,874 | 0,874 |

> **2,20 ha tinham copado em Julho de 2024, ao nível do pomar (0,83 contra 0,90),
> e não tinham nenhum em Julho de 2025.**

Isto é uma perda **datada por geometria**, e cai **antes** da janela que o `p8`
enquadrou para o declínio ocidental (meados de Outubro de 2025 a finais de Abril
de 2026).

## 4 · O piso de Inverno: a medição aguenta-se, a inferência não

**A medição sobrevive à disciplina de modo comum** — que era a minha suspeita ao
ler a tabela, e estava errada. Contraste contra a média dos controlos, sd dos
**oito outros invernos** (o ano de tratamento fora do seu próprio nulo):

| unidade | MDE | 2024/25 | |
|---|---|---|---|
| **N3 leste** | 0,124 | **+0,291** | **2,35× o MDE** |
| **foco ESTE** | 0,115 | **+0,202** | 1,76× |
| N2 leste | 0,137 | +0,138 | 1,01× — na linha |
| N1 foco OESTE | 0,075 | +0,076 | 1,01× — na linha |
| referência / resto | 0,017 | ∓0,005 | controlos quietos |

E não é uma imagem nem composição da janela: **cinco cenas consecutivas de
Janeiro-Fevereiro a +0,27 a +0,36**, depois de Dezembro a zero.

**A inferência é que não se aguenta**, e por duas razões:

- **A premissa não discrimina.** «Piso alto ⇒ verde permanente ⇒ as videiras não
  estão lá» tem uma explicação concorrente igualmente boa: **uma pérgola que
  perdeu copado deixa de dar sombra, e erva num Inverno português fica verde.**
  As duas hipóteses prevêem piso alto.
- **E não persiste.** N3 passa de **+0,291 a −0,078** no inverno seguinte. Verde
  permanente onde devia estar pérgola adormecida **não regressa**. Sob a leitura
  do terceiro isto é contradição; sob a de perda de copado, não é.

E o maior sinal de piso alto do conjunto pertence ao **foco ocidental** — que é
justamente o que o terceiro exonera como «videiras vivas com vigor reduzido». **O
teste dá a mesma resposta ao talhão que devia ilibar.**

## 5 · Os dois concordam, e sobre uma coisa mais estreita do que qualquer um diz

As células de N3 que o LiDAR vê sem copado em Julho de 2025 **leem 0,871 de NDVI
em Julho de 2024** — nível de copado, não de chão. E a anomalia do piso de
Inverno aparece **entre 27-12-2024 e 16-01-2025**.

> **Os dois instrumentos enquadram a mesma perda pelo mesmo intervalo, de lados
> opostos:** o piso sobe quando o copado deixa de dar sombra; o LiDAR confirma
> seis meses depois que o copado não está lá.

**Mas concordam sobre perda de copado, não sobre a causa.** O LiDAR é cego à
estrutura por sete desvios; o piso não separa «não há videira» de «há videira que
não dá sombra». **Não há conflito a registar, e também não há resposta.**

## 6 · Um conflito verdadeiro, e confirma o que eu já tinha medido

O `p1_pergola_oriental_2025.py` lê a prominência de pérgola na ortofoto de 2025 e
conclui «postes SEM copado ⇒ é DECLÍNIO». **Falha o critério de âncoras do
próprio portão nessa época** — e é exactamente o que eu medi a 05-09:

```
2021: REF p25 = +0,0286   NU21 p75 = -0,0146   -> SEPARAM
2025: REF p25 = +0,2702   NU21 p75 = +0,4037   -> NAO SEPARAM
```

Chão lavrado lê prominência mediana de 0,240 em 2025 — **os regos também são
periódicos**. É a forma G, a mesma que retirou o P3.

> **`AF-06` mantém-se PRETENDIDA, e agora com razão escrita.**

## 7 · Duas coisas que mudam o mapa e precisam de verificação própria

O adversário abriu a ortofoto de 2025 — 25 cm, quatro bandas, **sem folha** — e
mediu a fracção de píxeis brilhantes de fiada por célula. Dois valores saltam:

- **N3 leste: 0,0 % de fiadas brilhantes, e zero copado.** Não é declínio sob
  pérgola de pé: **não há instalação nenhuma** na Primavera de 2025.
- **`nu2021`: 34,0 % — a mais alta de todas as unidades, acima da referência —
  com altura LiDAR de 0,09 m.** Fiadas instaladas, sem copado. **Isso não é
  «chão lavrado»: parece plantação nova ou jovem.** E fica no foco oriental.

Se o segundo se confirmar, **a âncora baixa de todo o caso não é chão nu**, e
isso explica os 15,2 % que o cabeçalho do `altura_copado` diz que deviam ser
zero, e explica o colapso das âncoras do `p1` em 2025.

> **Nenhuma das duas entra em lado nenhum antes de ser verificada por instrumento
> próprio e atacada.** Ficam registadas como o que são: leituras de um adversário
> sobre uma imagem, por um leitor só — e a `CLAUSULAS` diz que a designação dos
> focos já foi invertida por quatro auditorias.

## 8 · O que fecha a pergunta

Por ordem, e vem dele:

1. **Correr o método certificado de prominência na ortofoto sem folha de 2025,
   com uma âncora baixa que não seja o `nu2021`** — que é 84 % interior aos
   discos de teste e possivelmente plantação nova. Barato, em disco, e fecha a
   âncora falhada do `p1`.
2. **Um segundo leitor para a chamada visual.** A leitura de imagem por um só
   leitor não tem guarda mecânica nenhuma.
3. **O gestor, ou o parcelário.** *O bloco oriental foi arrancado, quando, e
   replantou-se alguma coisa?* Testemunho de tipo 1 — ganha a tudo o que está
   acima, e é **uma pergunta**.
4. **Segundo voo ou visita** para o que as imagens não resolverem. E agora há o
   número que o justifica: **1,8 % contra 15 % ± 13,5 %.** Nenhum reprocessamento
   recupera um sinal tão abaixo da dispersão do próprio instrumento.

## 9 · Uma décima encarnação, e é nova

O `confirmar_com()` verifica que a prova existe e contém a chave — e **nunca
compara a data do confirmador com a janela do facto**. Um LiDAR de Julho de 2025
confirma um facto de Janeiro de 2025 e o portão fica satisfeito. **Num caso que
gira todo à volta de datação, é um buraco que vale a pena fechar.**
