# TAREFA 1 — Reprodução · notas de execução
28-08-2026 · sessão de verificação

## Declaração de independência — ler antes de usar

Esta sessão **não é cega**. Antes de receber este exercício, a mesma sessão fez uma
auditoria sobre o pacote de resultados do autor (`ganfei_s2/`), onde leu os CSV de
saída, o `masks.json` e quatro dos scripts (`exportar_auditoria.py`, `metricas.py`,
`termico.py`, `fenologia.py`). Por decisão da gestora, esta sessão executa **apenas a
Tarefa 1** (reprodução, que não depende de cegueira) e a **pergunta 4 da Tarefa 3**
(dependências de execução). A Tarefa 2 e as perguntas 1–3 da Tarefa 3 vão para uma
sessão nova, sem este histórico. Nesta pasta não há nenhuma comparação com os
resultados do autor; os números aqui são os que os scripts produziram, tal e qual.

## Ambiente

- Execução na máquina de trabalho da sessão (Linux, Python 3.11, numpy, scipy,
  rasterio 1.4.4 instalado à hora, matplotlib, requests). A VM local ligada à pasta
  não tem `scipy` nem rede, por isso não foi usada.
- **Rede**: nenhum dos três hosts externos responde a partir de qualquer dos dois
  ambientes (proxy devolve `403 Forbidden` no CONNECT):
  `earth-search.aws.element84.com`, `planetarycomputer.microsoft.com`,
  `sentinel-cogs.s3.us-west-2.amazonaws.com`. Consequência: todos os scripts que vão
  à rede falharam no primeiro pedido. Não é falha dos scripts; é do ambiente. Têm de
  ser corridos por quem tenha saída para esses hosts.
- Pasta de trabalho: cópia integral de `dados/` (cwd), scripts chamados de
  `../scripts/` **sem qualquer alteração**. Os scripts escrevem no cwd; os produtos
  foram copiados para esta pasta. `fazer_masks_v2.py` foi corrido numa segunda cópia
  isolada porque **reescreve o seu próprio input** (ver abaixo).
- Ordem de execução: `metricas` → `exportar_auditoria` → `espalhamento` →
  `b1_analise` → `rededge` → `termico` → `fenologia` → `b1_serie` →
  `fazer_masks_v2` (isolado). A ordem não é arbitrária — ver dependências.
- Logs completos (stdout+stderr, `python -W always`): `log_<script>.txt`.

## Resultado por script

| script | resultado | produtos | erro / nota |
|---|---|---|---|
| `metricas.py` | **FALHOU a meio (exit 1)** | `expansao.csv` ✔ (escrito antes da falha); `expansao.png` ✘; `defice_miniaturas.png` ✘ | `FileNotFoundError: sentinel/proveniencia.json` na linha 65. O ficheiro **não está em `dados/`**. O CSV principal ficou completo (11 linhas × 28 colunas) porque é escrito na linha 54, antes da falha. O script também **escreve** para `sentinel/proveniencia.json` (linha 78) — modifica um ficheiro da pasta de dados. |
| `exportar_auditoria.py` | correu (exit 0) | `focos_datacao_geometria.csv`, `lidar_topografia_por_mascara.csv`, `cota_vs_ndvi.csv` | Só `ResourceWarning` (ficheiros não fechados). Sem NaN reportado. 21 células vazias em `focos_datacao_geometria.csv` (linhas 2021–2023 da manchaW: sem componente de défice, o script escreve `""` — não é NaN, é ausência). |
| `espalhamento.py` | correu (exit 0) | `espalhamento.png`; tabela só no stdout (**não exporta CSV**) | Resultados numéricos existem apenas em `log_espalhamento.txt`. |
| `b1_analise.py` | correu (exit 0) | `expansao_b1.csv`, `b1_serie.png` | **Depende de `expansao.csv`** (linha 23), que é produto de `metricas.py`. Se `metricas.py` não tiver corrido antes, falha. Não está em `dados/`. |
| `rededge.py` | **FALHOU (exit 1)** | nenhum | `FileNotFoundError: sentinel/proveniencia.json` (linha 16), antes de chegar à rede. Mesmo com rede falharia por este motivo. |
| `termico.py` | **FALHOU (exit 1)** | nenhum | `ProxyError` ao pedir token a `planetarycomputer.microsoft.com` (linha 12). Rede. |
| `fenologia.py` | **FALHOU (exit 1)** | nenhum | `ProxyError` em `earth-search.aws.element84.com/v1/search` (linha 21). Rede. |
| `b1_serie.py` | **FALHOU (exit 1)** | nenhum | `FileNotFoundError: sentinel/proveniencia.json` (linha 12), antes de chegar à rede. Este script é o que **gera** `sentinel_b1/*.tif`; os GeoTIFF do lóbulo oeste que estão em `dados/` não podem ser regenerados sem esse ficheiro e sem rede. |
| `fazer_masks_v2.py` | correu (exit 0), em cópia isolada | `masks_regenerado_por_fazer_masks_v2.json` | Escreve para **`sentinel/masks.json`, sobrepondo o input**. O JSON regenerado é **byte-a-byte idêntico** ao `dados/masks.json` e ao `dados/sentinel/masks.json` (que também são idênticos entre si): as máscaras actuais são reprodutíveis a partir de `sentinel/2026-07-27.tif` + regras do script. |

## Avisos, NaN, divisões por zero, máscaras vazias

- Nenhum `RuntimeWarning` de numpy (nanmean de array vazio, divisão por zero) em
  nenhum log. Só `ResourceWarning` de ficheiros abertos sem `with`.
- `focos_datacao_geometria.csv`: 21 células vazias — manchaW em 2021-07-16,
  2022-07-31 e 2023-08-07 (7 colunas cada) porque a área de défice é 0,00 ha e não há
  componente conexa. Registado como está.
- `cota_vs_ndvi.csv`: 10 células vazias por construção (a linha de regressão e as
  linhas por foco têm colunas diferentes).
- `expansao.csv`: 10 células vazias na coluna `flag_fenologia` (só 2019-09-02 tem
  texto). Por construção.
- Nenhuma máscara vazia: `*_px_validos` = 2903 / 427 / 220 / 454 em todas as datas.

## Dependências de algo que não está em `dados/` — lista

1. **`sentinel/proveniencia.json`** — exigido por `metricas.py` (lê e reescreve),
   `rededge.py`, `b1_serie.py`. Não existe em `dados/`. Contém, pelos usos no código,
   os IDs das cenas (`prov["cenas"][i]["cena"]`) — a mesma informação está em
   `dados/cenas.json`, mas com outro nome de ficheiro e os scripts não o lêem.
2. **`expansao.csv`** como input de `b1_analise.py` — dependência de execução
   anterior (produto de `metricas.py`).
3. **Rede** (Earth Search, Planetary Computer, bucket `sentinel-cogs`) — `termico.py`,
   `fenologia.py`, `rededge.py`, `b1_serie.py`. Sem rede, três dos cinco quadros da
   especificação (térmico, e tudo o que use NDRE ou a série de Primavera) não são
   reproduzíveis a partir de `dados/`: os TIFF em `dados/sentinel/` são só NDVI de
   11 datas.
4. **Escrita sobre input**: `metricas.py` reescreve `sentinel/proveniencia.json`;
   `fazer_masks_v2.py` reescreve `sentinel/masks.json`. Uma execução altera o estado
   de que a execução seguinte depende. No caso das máscaras, a reexecução deu
   resultado idêntico; no caso da proveniência não foi possível testar (ficheiro em
   falta).
5. **Caminhos**: todos relativos ao cwd (`sentinel/…`, `sentinel_b1/…`, `lidar/…`);
   nenhum caminho absoluto encontrado. Os scripts assumem cwd = pasta que contém
   `sentinel/`, não a pasta `scripts/`.
6. `espalhamento.py` não exporta os seus números — só existem no stdout. Qualquer
   valor de "área de défice no pomar", "n manchas", "circularidade", "deslocamento
   do centróide" ou "distância ao núcleo" que circule em prosa **não tem ficheiro de
   origem** a não ser um log de execução.
7. Contagem de pixels por máscara **difere entre scripts para o mesmo polígono**:
   `fazer_masks_v2.py` imprime saudável 259 / 117 / 70 (união 446 px = 4,46 ha),
   pomar 2906, manchaW 423, zona0 219; `metricas.py` produz 264 / 119 / 71 (união
   454 px = 4,54 ha), pomar 2903, manchaW 427, zona0 220 (coluna `*_px_validos`).
   Mesmo `masks.json`, duas rasterizações. Registado sem interpretação.

## Ficheiros nesta pasta

`expansao.csv`, `expansao_b1.csv`, `focos_datacao_geometria.csv`,
`lidar_topografia_por_mascara.csv`, `cota_vs_ndvi.csv`, `b1_serie.png`,
`espalhamento.png`, `masks_regenerado_por_fazer_masks_v2.json`, nove `log_*.txt`.
Não produzidos: `expansao.png`, `defice_miniaturas.png`, `rededge.*`, `termico.csv`,
`fenologia.*`, `sentinel_b1/*.tif` regenerados, `proveniencia*.json`.
