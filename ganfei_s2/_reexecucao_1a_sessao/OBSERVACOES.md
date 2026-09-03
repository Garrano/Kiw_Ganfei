# TAREFA 3 — Observações (parcial)

Esta sessão não é cega (ver `reproducao/NOTAS.md`, primeira secção). Por decisão da
gestora responde **só à pergunta 4**. As perguntas 1–3 (geometria das máscaras,
datas a excluir, decisão mais frágil) e toda a Tarefa 2 ficam para a sessão nova,
sem histórico. Não há aqui `independente/`.

## 4. Resultados que dependem da ordem de execução, de estado anterior ou de ficheiro ausente

- **`sentinel/proveniencia.json` não existe em `dados/`** e é lido por três scripts
  (`metricas.py`, `rededge.py`, `b1_serie.py`). `metricas.py` também o reescreve.
  Sem ele: `expansao.csv` sai completo mas o script morre antes das figuras;
  `rededge.py` e `b1_serie.py` não arrancam. A informação equivalente (IDs de cena)
  está em `dados/cenas.json`, que nenhum script lê.
- **`b1_analise.py` lê `expansao.csv`**, produto de `metricas.py`. Ordem obrigatória,
  não documentada em lado nenhum de `dados/`.
- **Dois scripts escrevem sobre os seus inputs**: `fazer_masks_v2.py` →
  `sentinel/masks.json`; `metricas.py` → `sentinel/proveniencia.json`. O estado de
  `dados/` depois de uma corrida não é o de antes. Para as máscaras, a regeneração
  deu JSON idêntico ao fornecido (bom sinal de reprodutibilidade das máscaras
  actuais; nada diz sobre versões anteriores, que não estão em lado nenhum).
- **`sentinel_b1/*.tif` são produto de `b1_serie.py`**, que precisa de
  `proveniencia.json` e de rede. Estão em `dados/` como se fossem dados brutos, mas
  são derivados de uma execução que não é reproduzível a partir desta pasta.
- **`espalhamento.py` não exporta**: as suas tabelas (área de défice no pomar por
  data, número de manchas, circularidade, deslocamento de centróide, distância ao
  núcleo) só existem em stdout. Qualquer número desses em prosa depende de um log
  que não é ficheiro de dados.
- **Rede**: `termico.py`, `fenologia.py`, `rededge.py`, `b1_serie.py` dependem de
  Earth Search / Planetary Computer / `sentinel-cogs`. Nenhum host acessível neste
  ambiente nem na VM local. Três dos cinco quadros da especificação (Q3 térmico e
  tudo o que use NDRE ou Primavera) não têm dados brutos em `dados/`.
- **Mesmo polígono, duas contagens de pixels**: `fazer_masks_v2.py` conta 446 px
  para a união saudável (4,46 ha), `metricas.py` conta 454 (4,54 ha); idem pomar
  2906/2903, manchaW 423/427, zona0 219/220. Qualquer área "de máscara" reportada
  depende de qual dos dois scripts a produziu.
- Nenhum caminho absoluto, nenhuma dependência de variáveis de ambiente, nenhuma
  credencial. Todos os caminhos são relativos ao cwd.
