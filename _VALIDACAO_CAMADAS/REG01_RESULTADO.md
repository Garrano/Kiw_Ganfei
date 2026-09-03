> # ⚠ RETIRADO em 01-09-2026
> Este documento sustenta o **A3**, que foi retirado: os cinco blocos do
> ENT 297313 tinham sido **desmatados em 2024**, e a queda caía do lado PRÉ da
> fronteira dos períodos. A conclusão da REG-01 **inverteu-se** — os focos de
> Ganfei são o pior e o segundo pior da região entre unidades de linha de base
> contínua (percentil 0 %).
> **Fica por ser o registo do erro e da sua descoberta.** O que vale está em
> `REG01_RETRACCAO_A3.md`. Não citar daqui.

# REG-01 · CORRIDA — o acontecimento não é exclusivo desta exploração

**Data:** 31-08-2026 · **Ficheiro:** `reg01_local_ou_regional.py` → `.json`
**Estado da condição de arranque da C5: FECHADA.**
**Passou pelo `guarda.py`** — que bloqueou «a causa é regional» por falta de
instrumento independente, e só deixou sair a afirmação medida.

---

## O critério, fixado antes de correr

> **H1** · o degrau de 2025-26 é específico dos dois focos desta exploração.
> **H0** · é regional.
>
> **Se os focos de Ganfei caírem acima do percentil 10 da distribuição regional,
> H1 cai.**

**Caíram no percentil 13. H1 cai.**

## O desenho, e porque é auto-controlado

38 blocos de kiwi declarado ao IFAP, 87,1 ha, **21,7 × 17,1 km**, sete
beneficiários. Para cada bloco e cada cena mede-se o NDVI e depois o **desvio à
mediana regional dessa cena** — a região é o seu próprio controlo, e um degrau
de plataforma, uma anomalia meteorológica ou um efeito de dia-do-ano comuns
cancelam-se.

**As cenas são as mesmas nove da série certificada**, pelos IDs do
`proveniencia.json`. Não se escolheram cenas novas: seria mudar duas coisas ao
mesmo tempo.

## O resultado

| unidade | ha | degrau | percentil |
|---|---|---|---|
| **foco OCIDENTAL** | 2,18 | **−0,1060** | **13 %** |
| **foco ORIENTAL** | 0,76 | **−0,1008** | **13 %** |
| pomar inteiro de Ganfei | 30,31 | −0,0102 | 37 % |

**E os cinco piores da região não são de Ganfei:**

| CUL_ID | ENT | ha | degrau |
|---|---|---|---|
| 6705427 | **297313** | 1,28 | **−0,4021** |
| 6705429 | **297313** | 2,28 | **−0,3820** |
| 6705428 | **297313** | 1,02 | **−0,3486** |
| 6705432 | **297313** | 2,30 | **−0,3211** |
| 6705442 | **297313** | 0,62 | **−0,2081** |

São blocos de **0,62 a 2,30 ha** — a mesma ordem de grandeza dos focos de
Ganfei, logo a comparação é de escala comparável e não diluída.

> ### **Duas a quatro vezes piores do que o pior sítio de Ganfei, na mesma
> cultura, na mesma região, a cerca de 8 km — e todos da mesma exploração
> vizinha, o ENT 297313.**

E a exploração de Ganfei, **como um todo, está no percentil 37** — indistinguível
do meio da distribuição regional.

## O que isto decide, e o que não decide

**Decide:** o acontecimento de 2025-26 **não é exclusivo desta exploração**.
Existe pelo menos uma outra, próxima, com blocos de kiwi a perder duas a quatro
vezes mais. A C5 escreveu em quatro sítios que «se a causa for regional, quase
todas as medidas de parcela que se possam recomendar são inúteis» e que «enquanto
REG-01 estiver por fechar, nenhuma medida irreversível». **A condição está fechada, e fecha contra a exclusividade** — não «para uma
causa regional», que é coisa que este teste não mede.

**Não decide** que seja *a mesma* causa. Dois sítios com o mesmo sintoma podem
ter causas diferentes — e é precisamente isso que uma campanha desenhada só para
Ganfei nunca poderia distinguir.

**Não decide** que seja «toda a região». «Regional» aqui significa **pelo menos
duas explorações**, não «em todo o lado»: os outros cinco beneficiários têm
pouca área e ficam no meio da distribuição.

## As ressalvas, e vão à frente e não no rodapé

- **Um instrumento só.** É Sentinel-2, como quase tudo neste caso. **Não há
  instrumento independente para este facto.** Pelo controlo 1, isto devia ir
  para NÃO TESTÁVEL, e vai com a marca à vista. **O que é independente são as
  fronteiras:** todos os 38 blocos, incluindo os de comparação, vêm do
  parcelário do IFAP — desenhados por outra entidade, para pagamentos, sem
  saber nada de NDVI.
- **O teste é directamente repetível com o Landsat**, que é a segunda
  constelação que este caso já usa. É a acção óbvia a seguir, e é barata.
- **A mediana regional é dominada pelo ENT 297313 e pelo 472062**, que juntos
  têm 30 dos 38 blocos. Uma mediana com poucos donos independentes é um
  controlo mais fraco do que o n sugere.
- **A composição de cada bloco não foi verificada.** Em Ganfei sabe-se, pelo
  LiDAR, que parte do polígono não tem pérgola. Nos blocos do 297313 não se
  sabe: uma parte do degrau deles pode ser chão, arranque ou replantação, e não
  declínio. **Isto não se corrige com satélite — corrige-se olhando.**

## O que muda na decisão

| era | passa a ser |
|---|---|
| REG-01 · condição de arranque por correr | **FECHADA — o degrau não é exclusivo desta exploração** |
| «o caso é de uma exploração» | **é de pelo menos duas, e a outra está pior** |
| a campanha de Setembro desenhada só para Ganfei | **desenhada para Ganfei é metade de um desenho.** Sem um ponto no 297313 não se distingue causa partilhada de coincidência |
| «nenhuma medida irreversível antes da REG-01» | a condição levantou-se, e a resposta **não** autoriza medidas de parcela: aponta ao contrário |

## A fila, refeita

| | acção | custo | decide |
|---|---|---|---|
| **1** | **repetir a REG-01 com o Landsat** | baixo | se o resultado tem segundo instrumento |
| **2** | **contactar o ENT 297313** — ou quem o acompanhe na CCDR-N | nenhum | se há sintoma no terreno, e qual |
| **3** | LiDAR ou ortofoto sobre os cinco blocos do 297313 | baixo | se o degrau deles é declínio ou é chão |
| 4 | escrever a linha da PSA no livro-razão | nenhum | fecha a lacuna que consumiu quatro documentos |
| 5 | a campanha de Setembro, **com pontos nas duas explorações** | alto | a etiologia |

---

**Nota.** Este resultado é o contrário do que eu esperava, e é por isso que o
critério foi escrito antes de correr. Se tivesse sido escrito depois, «percentil
13» tinha-se lido como «na cauda, logo local» com a mesma facilidade com que
agora se lê «acima do percentil 10, logo H1 cai».
