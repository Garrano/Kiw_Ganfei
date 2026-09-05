# HIPÓTESES FECHADAS — ler ANTES de desenhar um teste novo

**Porque este ficheiro existe.** A 04-09-2026, num único turno, re-derivei duas
coisas que já estavam em disco: a análise do B1 e o teste da rede de rega. Da
segunda, refiz uma versão mais fraca de um estudo de **onze cenas com critério
pré-registado**, e só soube porque o gestor mo disse. Foi a segunda vez que ele
teve de o dizer.

**E a triagem — construída para isto — não me salvou, porque é cega ao
negativo.** Ela classifica um ficheiro como CORRENTE se houver um caminho de
consumo até um **facto certificado**. Uma hipótese testada e **refutada** não
sustenta facto nenhum, portanto cai em `NAO_ALCANCADO` e desaparece da vista.
O `rede_de_rega.py` e o `rede_de_rega.json` estão os dois lá.

Uma triagem que optimiza para «o que sustenta o que afirmamos» esconde
activamente «o que já tentámos e não deu». É exactamente o inverso do que é
preciso consultar antes de começar.

**Regra:** nenhuma análise nova arranca sem passar os olhos por esta lista. Se a
pergunta já cá estiver, ou se lê o que se fez, ou se declara por escrito o que
mudou desde então que justifica repetir.

---

## Refutadas contra critério pré-registado

| hipótese | resultado | onde |
|---|---|---|
| **O declínio segue o terreno** — «as células em maior défice estão nas posições topograficamente mais húmidas» | **REFUTADA E INVERTIDA.** O défice está no terreno **alto**: ρ da cota negativo nas onze cenas, p < 0,001. Nenhuma métrica de humidade emerge em 2025-26; a área drenante chega a decair para zero nos anos do evento. | `terreno_contra_declinio.py` |
| **O declínio segue a rede de rega** — «o défice de 2025-26 organiza-se pela topologia da rega, identidade de válvula e posição na conduta» | **REFUTADA, e nas duas condições que ela própria escreveu.** (1) O agrupamento por válvula nunca excede o nulo geográfico em onze cenas (p 0,175 a 0,64) **e não emerge em 2025-26** — η² 0,142 e 0,204 contra nulos de 0,111 e 0,164. (2) A ordem na conduta correlaciona-se forte em **2021** (ρ 0,909, p 4e-5) e **2022** (ρ 0,874, p 2e-4), decai, e em **2026 é negativa** (ρ −0,140). Importava antes do acontecimento e deixou de importar. | `rede_de_rega.py` · `.json` |
| **O B1 não acrescenta nada à leitura do terreno** | **FALSIFICADA.** A cota do B1 (6,06 m) cai **fora** do intervalo dos dois focos [6,64 ; 7,84] — abaixo dos dois. Há uma terceira posição na estrutura. | `b1_terreno.py` |
| **Cada cor impressa do esquema corresponde a um sector** | **REFUTADA.** O sector F (válvula 7) e o sector M (válvula 16) têm o mesmo amarelo, ΔRGB 11,1, em extremos opostos da folha. A cor é colorização de mapa, não chave de identidade. | `figuras/base/cor_e_sector.py`* |
| **A mancha de declínio tem a forma de um sector de rega** | **REFUTADA.** Razão comprimento/largura 1,41 e 12° do eixo das fileiras, contra 4,83 e 2° no controlo. 196 × 138 m é um bolo, não uma faixa. *(n = 1; só a `zona0` tem máscara geográfica.)* | `figuras/base/forma_dos_focos.py` |

\* medições em `cor_e_sector.json`; o teste correu inline.

## Fechadas por testemunho directo (tipo 1)

| | |
|---|---|
| **PSA** | Não foi esquecimento: ninguém encomendou ensaio porque **a sintomatologia não era compatível**. Decisão clínica do gestor, 01-09-2026. Testemunho ganha ao cálculo. |
| **Escala do desenho** | 1:3500 em A1 — declarado pelo gestor. Derrubou a minha conclusão de que o desenho não tinha escala única. |

## Retiradas — não repetir sem uma razão nova escrita

As vinte e uma da `LISTA_FINAL_2026-08-31.md` §E e da P06, mais as de 04-09.
As que mais provavelmente voltariam a ser tentadas:

- **«O foco oriental foi replantado»** (retirada 16) — concluído da prominência
  de pérgola sozinha; o NDVI não tem cova nos anos em causa.
- **«Os fossos são conservadores, pelo T5»** (17) — **identidade algébrica**:
  limpar a referência desloca todos os fossos. Um teste que não podia falhar.
- **«O B1 é o comparador sem degrau»** (18) — zero instrumentos independentes.
- **«Blocos vizinhos com degrau 2 a 4× maior»** (19) — estavam **desmatados
  desde 2024** e a queda caía do lado PRÉ da fronteira dos períodos. Tinha
  passado o portão com dois instrumentos e ρ = 0,890, porque **ambos mediam a
  mesma coisa errada**.
- **«A acidez do solo não acompanha o declínio»** (20) — assentava num número
  que o adversário rejeitara nove horas antes.
- **«Um halo com decaimento pela distância»** (12) — ρ ingénuo p = 2e-9; com
  **nulo toroidal**, p = 0,55. O nulo é que estava errado.
- **«O desenho não tem escala única»** (04-09) — a ponta oriental estava lida
  600 px ao lado.
- **Georreferenciação por bloco** (04-09) — 55,9 % dos píxeis que o ICP alinhava
  eram os círculos das próprias válvulas.

## Aberto, e é onde vale a pena gastar

- **Posição de cada válvula dentro do sector.** Cinco tentativas; a melhor deixa
  as válvulas a ≤ 26 m das parcelas mas falha a âncora independente, e dois
  métodos sem dados em comum discordam por 83 m contra um espaçamento de 98 m.
  **Não se resolve com o papel que existe** — resolve-se no terreno, e só
  interessa se houver intervenção a planear.
- **As etiquetas de sector das válvulas 1, 2, 3, 10, 11 e 12.** A do Erica Novo
  (10 ou 11) determina quase todas as outras.
- **Porta-enxerto** — testado e **confundido**: entre blocos as trajectórias
  diferem e o radar confirma em duas órbitas, mas a janela não isola a raiz.
  Não é «fechado» nem «por testar».
- **Nemátodos.** *M. hapla* positivo em quatro unidades colocadas (D2), e
  nenhuma das doze amostras com posição é anterior ao acontecimento (D5).
