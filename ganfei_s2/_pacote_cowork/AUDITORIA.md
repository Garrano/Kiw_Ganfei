# Como auditar este trabalho — registo para a sessão Cowork
Ganfei / declínio do kiwi · 28-08-2026

## O problema que este ficheiro resolve

Até hoje a Cowork recebeu **conclusões em prosa**, não dados. Podia discordar
do raciocínio, mas não podia verificar um número. Foram produzidos 29 scripts e
só 7 CSV: a maior parte dos resultados que sustentam o caso — datação do foco,
geometria da expansão, série corrigida da Zona 0, topografia por máscara — só
existia como texto em mensagens de chat.

Regra a partir de agora: **nenhuma afirmação entra no dossiê sem cair numa
célula de um ficheiro deste pacote.** Se não é rastreável, é opinião.

## Os três níveis de verificação

**Nível 1 — rastreabilidade (barato, faz-se já).**
Cada afirmação do dossiê tem de apontar para ficheiro + coluna + linha. A tabela
abaixo faz esse mapeamento. Qualquer afirmação que não apareça na tabela é uma
afirmação sem suporte e deve ser marcada como tal no dossiê.

**Nível 2 — coerência interna (barato).**
Verificar que números repetidos em sítios diferentes batem certo, que as somas
fecham, e que nenhuma figura contradiz a tabela que a gerou. Foi exactamente
assim que a Cowork apanhou o erro do "maior incremento em 2025" — lendo a tabela
contra a frase.

**Nível 3 — reexecução independente (caro, mas é o único que refuta).**
Correr os scripts sobre os mesmos dados e comparar. Os scripts estão no pacote.
Se a Cowork não puder executar código, o Nível 3 tem de ser feito por um terceiro
ou por uma sessão local com acesso aos ficheiros — não é substituível por leitura.

## Mapa de afirmações → fonte

| afirmação | ficheiro | colunas |
|---|---|---|
| NDVI médio por máscara, 11 datas | `expansao.csv` | `*_ndvi_medio`, `*_ndvi_mediana` |
| Áreas de défice moderado/severo | `expansao.csv` | `*_defice_*_ha`, `*_pct` |
| Referência sã por data | `expansao.csv` | `ref_saudavel_media`, `ref_saudavel_dp` |
| ΔT de superfície, 81 cenas Landsat | `termico.csv` | `*_st` |
| Atraso fenológico | `fenologia.csv` | por data e máscara |
| NDRE vs NDVI (via fechada) | `rededge.csv` | `*_ndre`, `*_ndvi` |
| Lóbulo oeste B1 | `expansao_b1.csv` | todas |
| Datação do foco e geometria da expansão | `focos_datacao_geometria.csv` | `manchaW_*`, `zona0_alargada_*` |
| Topografia por máscara | `lidar_topografia_por_mascara.csv` | `cota_mediana_m`, `percentil_no_pomar` |
| Cota prediz vigor? | `cota_vs_ndvi.csv` | `r`, `defice_vs_previsto` |
| Sentinel-1, três Invernos | `sar_invernos.csv` | `*_vv_db`, `*_vh_db` |
| Série densa Jul2023–Jun2025 | `serie_densa_W.csv` | `*_ndvi/ndmi/bsi` |
| Coordenadas dos traços de 1995 | `tracos_1995_coordenadas.csv` | todas |
| Cenas, nuvens, % mascarada | `proveniencia.json` | `cenas[]` |
| Geometria das máscaras | `masks.json` | polígonos em pixel |

## Dívida de exportação — SALDADA em 28/08

Estes números circulavam só em prosa. Foram recalculados e exportados; todos
reproduziram os valores publicados.

| resultado | ficheiro | confere? |
|---|---|---|
| pomares novos (11,16 ha; 2022 4,09 / 2023 2,85 / 2024 1,50 / 2025 2,72) | `pendente_pomares_novos.csv` | sim |
| precipitação por Inverno | `pendente_precipitacao.csv` | sim |
| geada Abr–Mai (0 horas ≤2 °C em 2025) | `pendente_geada.csv` | sim |
| secagem do solo por SAR (declives por máscara e órbita) | `pendente_sar_secagem.csv` + `pendente_sar_declives.csv` | sim |
| escoamento (% em linha de drenagem) | `pendente_escoamento.csv` | sim |

| bacia contribuinte 49,14 ha (26,1 fora do pomar) + repartição por tile | `pendente_bacia.csv` | sim |
| rugosidade e teste de nivelamento | `pendente_nivelamento.csv` | sim |
| degrau entre campanhas de voo LiDAR | `pendente_degrau_campanhas.csv` | sim |

**A dívida está integralmente saldada.** Todos os resultados que sustentam o
dossiê estão agora em ficheiro e todos reproduziram os valores publicados.

Nota sobre o degrau entre campanhas: usar **só as costuras completas**
(`costura_completa = True`, n≥1900 px). As parciais comparam bordos que
atravessam relevo diferente e dão diferenças de metros que nada têm a ver com
as campanhas — foi assim que eu próprio errei o teste à primeira. Nas completas:
mesma campanha mediana +0,0049 m, campanhas diferentes +0,0084 m.
Indistinguíveis, e ambas abaixo do centímetro.

## Componente difusa — achado da auditoria independente, caracterizado

Metade do défice de 2026 está fora da `manchaW` e da `zona0`. Decomposição por
distância ao bordo do `pomar` (`difusa_nucleos.csv`, `difusa.png`):

- **bordadura estrutural**: a faixa de ≤1 px do bordo (3,02 ha) tem 0,6 a 1,3 ha
  em défice em todos os anos, incluindo os saudáveis. É pixel misto de 10 m.
- **crescimento 2024→2026 fora dos focos: +2,53 ha**, dos quais **1,42 ha no
  interior** (>2 px do bordo) — não é artefacto de bordo.
- Três núcleos interiores novos ≥0,15 ha, todos **satélites dos focos
  existentes**: dois a 79 e 82 m do centro da Zona 0, um a 143 m do centro da
  Mancha W. Coordenadas no CSV.

Leitura: não há um terceiro foco independente noutro sítio. O que há é **os dois
focos a transbordar as máscaras desenhadas em 2026**, mais dispersão de fundo.
Consequência para a amostragem: a frente activa vai além do que as máscaras
sugerem, e há satélites a 80–145 m para incluir no plano.

## Lista vermelha — onde eu acho que este trabalho está mais frágil

Escrita por quem o produziu, para poupar tempo a quem o vai atacar.

1. **As máscaras são a fundação e foram desenhadas por mim.** `manchaW` é o
   footprint de 2026; `zona0` já foi redesenhada uma vez por estar saturada;
   `pomar` resulta de um limiar de NDVI escolhido a olho. Mudar as máscaras
   move todos os números do pacote. É aqui que uma auditoria deve começar.
2. **A referência sã (4,46 ha, 3 manchas) foi escolhida por mim.** Todo o ΔT e
   todo o défice são relativos a ela. Uma escolha diferente desloca tudo.
3. **Detecção dos pomares novos**: limiares arbitrários (NDVI>0,80; ≤1 dos
   primeiros 4 anos; ≥3 dos últimos 4). Os anos de entrada são aproximados e
   **a propriedade dos blocos não está confirmada**. Se forem de outro produtor
   ou tiverem furo próprio, a hipótese hidráulica cai inteira.
4. **Térmico**: pixel nativo de 100 m sobre 4 ha, e não separa "menos folha" de
   "menos transpiração". O salto 2025→2026 é real; a magnitude não é fiável.
5. **Uma cena por ano** na série principal. Carrega ruído de data e fenologia.
   A série densa só cobre Jul2023–Jun2025.
6. **CORREÇÃO — os "12 m" entre o centro do foco e o traço L1 têm precisão
   falsa.** As coordenadas do L1 foram lidas visualmente sobre uma grelha
   desenhada; a incerteza é de ±10 a 15 m em cada extremo. O valor honesto é
   "o centro do foco cai a menos de ~25 m do alinhamento L1". Corrigir onde
   aparecer.
7. **A ortofoto de 2025** foi datada por mim como leaf-on a partir das árvores
   caducifólias na imagem. É inferência visual, não metadado.

## CORREÇÃO 28/08 (achado da reexecução) — áreas das máscaras

Duas contagens do mesmo polígono circularam neste caso. `fazer_masks_v2.py`
imprime a área da máscara **booleana**, antes da conversão em polígono; todos
os cálculos a jusante usam o **polígono** de `masks.json`. A conversão
máscara→contorno→polígono→rasterização não é identidade: a simplificação
(`approximate_polygon`, tolerância 0,6–1,0 px) e o teste ponto-em-polígono nos
centros de pixel mudam a fronteira.

| máscara | booleana (o que eu citei) | polígono (o que os CSV usam) | dif. |
|---|---|---|---|
| pomar | 29,06 ha | **29,03 ha** | −0,10 % |
| saudável (união) | 4,46 ha | **4,54 ha** | +1,79 % |
| manchaW | 4,23 ha | **4,27 ha** | +0,95 % |
| zona0 | 2,19 ha | **2,20 ha** | +0,46 % |

No `pomar` não é sequer relação de inclusão: 39 px só na booleana, 36 px só no
polígono. **Os CSV sempre estiveram certos** (`*_px_validos` ÷ 100); foi a minha
prosa que citou as áreas intermédias. Usar as da coluna do polígono em todo o
lado. Nenhuma conclusão muda — a maior diferença é 1,8 % numa máscara de
referência — mas o registo tem de ficar coerente.

## Erros já cometidos e apanhados neste caso

Servem de guia ao tipo de falha a procurar. Nenhum foi de aritmética; todos
foram de **construção de método** ou de **âmbito**.

| erro | apanhado por | natureza |
|---|---|---|
| "maior incremento em 2025" (é 2022) | Cowork | leitura da própria tabela |
| bacia sem resolução de zonas planas | sessão local | método |
| degrau entre tiles medido em bordos inteiros | sessão local | método |
| NDVI a partir de ortofotos equilibradas | sessão local | método, já com figuras feitas |
| "B1 tem conduta própria" | gestora | especulação afirmada a mais |
| máscara da Zona 0 saturada → "estabilizou" | sessão local | âmbito, já reportado |
| AOI não continha o B1 | esquema de rega | âmbito, sete turnos sem dar por isso |
| `bbox` ignorado pelo frontend da DGT | sessão local | ferramenta, quase gerou falsa cobertura |
| duas contagens da mesma máscara (booleana vs polígono) | reexecução Cowork | prosa citou valor intermédio |
| `b1_analise.py` depende de `metricas.py` sem estar documentado | reexecução Cowork | ordem de execução não escrita |

## O que peço à Cowork

1. Marcar no dossiê toda a afirmação que não caia na tabela de rastreabilidade.
2. Atacar primeiro os pontos 1, 2 e 3 da lista vermelha.
3. Aplicar a correcção do ponto 6 (os 12 m).
4. Decidir se as afirmações da secção "ainda não exportado" ficam no dossiê com
   marca de não-verificadas, ou se saem até serem exportadas.
