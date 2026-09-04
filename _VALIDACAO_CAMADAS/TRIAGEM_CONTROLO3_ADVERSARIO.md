# TRIAGEM DE FONTES — CONTROLO 3, SESSÃO ADVERSÁRIA

**Data:** 04-09-2026 · **Alvo:** `triagem_de_fontes.py` (2.ª versão),
`TRIAGEM_DE_FONTES.md`, `triagem_de_fontes.json`, e a **verificação 8** do
`certificar.py`.

**Método.** Reimplementei o mecanismo inteiro num ficheiro à parte
(`harness.py`, fora deste directório) e confirmei que reproduz o `.json`
publicado **com zero divergências em 1282 ficheiros**. Todas as sondas abaixo
correm sobre essa reimplementação ou sobre cópias em memória — **nenhum ficheiro
do processo foi alterado**, e não corri `git`. O `certificar.py` foi corrido uma
vez, em modo rápido: devolveu **CERTIFICADA**, com todos os defeitos abaixo em
disco.

---

## CONFIRMADO

**K1 · O mecanismo é determinístico e reproduz-se.**
Reimplementação independente a partir do código: 1282/1282 classificações
idênticas às do `triagem_de_fontes.json`. Não há estado escondido nem
dependência de ordem de directório.

**K2 · Nenhum dos 27 factos aponta hoje para um ficheiro classificado morto.**
Os 15 valores de `ficheiro="…"` e os 15 caminhos do `PV`
(`registo_de_factos.py:84-100`) resolvem todos para `CORRENTE`, com duas
excepções que estão **fora do inventário** e não em classe morta:
`ficheiro="LISTA_FINAL"` (D6, sem extensão) e
`PV["esquema"] = "…/Esquema de rega retificado.pdf"` (fora das quatro árvores e
com extensão que o `EXT` não cobre). O `.json` está certo neste ponto — mas ver
LS-1: **isto não é mérito da verificação 8**, que não o testaria.

**K3 · A classe RETIRADO deixou de ter falsos positivos.**
Dois ficheiros, ambos com o cartucho `> # ⚠ RETIRADO` verificado à mão
(`REG01_RESULTADO.md`, `REG01_LANDSAT_REPLICACAO.md`). Os 16 falsos positivos da
1.ª versão desapareceram. A substituição do regex sobre prosa pelo cartucho
literal (`triagem_de_fontes.py:216-217`) resolveu o que dizia resolver.

**K4 · A pré-empção do `_bak_` funciona, e pela razão declarada.**
`triagem_de_fontes.py:144-154` corre **antes** da regra do produtor e impede que
`_bak_20260901/reg01_landsat.py` seja promovido por escrever `reg01_landsat.json`.
Verifiquei: os três ficheiros de `_bak_20260901/` saem `SUBSTITUIDO`, nenhum
`CORRENTE`.

**K5 · A regra do produtor resolve o caso que a motivou.**
`b1_terreno.py` está `CORRENTE` e a cadeia passa por `b1_terreno.json`. O caso
do cabeçalho (`triagem_de_fontes.py:187-191`) é real e está corrigido.

**K6 · A verificação 7b do `certificar.py` bate.**
`p06_hipoteses_e_retirado.py` desenha **21** retiradas; o cabeçalho da secção E
da `LISTA_FINAL` diz «vinte e uma». Contados os dois à mão.

**K7 · A segunda entrada da tabela `DERRUBADAS` está correcta.**
`ganfei_s2/figuras/p10_braudel_mapa.py` traz hoje, em texto, as três correcções
(«extremos opostos» falso, «sem cota» falso, «445 m» aresta errada). O ficheiro
está `CORRENTE` e a linha morta está marcada nele próprio.

---

## CORRIGIDO

**C1 · A prova de identidade tem 301 cenas em disco, e a triagem classifica as
301 como `NAO_ALCANCADO`.**
`triagem_referencia_densa.py:51,105,108` lê o cache por nome construído:
`os.path.join(CACHE, "%s_%s.npy" % (d, it.id[-6:]))`, com
`CACHE = _VALIDADE_GESTAO/_densa_ganfei`. Nenhum nome literal aparece em código
nenhum, portanto o `TOKEN` (`triagem_de_fontes.py:68`) não os vê.
Contagem: **301 ficheiros em `_densa_ganfei/`, 301 em `NAO_ALCANCADO`, 0 em
`CORRENTE`.** O `triagem_referencia_densa.json` declara `n_cenas: 301` — são
exactamente estes.
Estes 301 ficheiros são a base de prova da **condição 5** do portão, de que
dependem **onze dos 27 factos** (A1, A2, A3, B1–B5, B7, C6 — todos os que passam
por `temporal()`). **Valor certo: `CORRENTE`.**
(O `IGNORA` filtra directórios que contenham `cache`; `_densa_ganfei` não contém,
por isso foram inventariados e depois declarados sem ligação — o pior dos dois
mundos: contam para os 1132 e não contam para nada.)

**C2 · `c2_12_prom_2010.npy` e `c2_12_prom_2021.npy` são prova directa dos
factos C4 e C5 e estão em `NAO_ALCANCADO`.**
`p3_pergola_2010_2012.py:55-57` põe os três nomes numa **tabela**:

```
EPOCAS = [("2010", "c2_12_prom_2010.npy"),
          ("2012", "c2_12_prom_2012.npy"),
          ("2021", "c2_12_prom_2021.npy")]
```

e só à linha **67** faz `P = np.load(os.path.join(C2, fich))`. Medido:
**369 caracteres** entre a tabela e o verbo — a janela é de 200
(`triagem_de_fontes.py:140`). Sonda: `verbo-a-200? False` para os três nomes.
`c2_12_prom_2012.npy` está `CORRENTE` **por acidente** — está no `PV`
(`registo_de_factos.py:93`). O de 2010 e o de 2021 não estão em lado nenhum.
O facto C4 diz «ORI-COM tinha pérgola madura **em 2010** (111 %) e 2012 (79 %)»
e o C5 diz «pico a 2,25 m (2012) e **2,12 m (2021)**». **Valor certo: os três
`CORRENTE`.** O mesmo se aplica a `p4_quando_foi_arrancada.py:94-95` (facto C6).

**C3 · Duas das quatro reconstruções em que o facto C8 assenta estão em
`NAO_ALCANCADO`, e as outras duas estão `CORRENTE` por acidente.**
`valvulas_1a5_o_troco_que_falta.py:77-78`:
`FONTES = ("valvulas_por_area.json", "valvulas_v6.json", "valvulas_v4.json", "valvulas_por_linha.json")`.
Sonda: **nenhum dos quatro** tem verbo na janela de 200. Ficaram assim:

| ficheiro | classe | porquê |
|---|---|---|
| `valvulas_por_area.json` | NAO_ALCANCADO | — |
| `valvulas_v6.json` | NAO_ALCANCADO | — |
| `valvulas_v4.json` | CORRENTE | mencionado num **comentário em prosa** do `registo_de_factos.py` |
| `valvulas_por_linha.json` | CORRENTE | um `join(` numa secção **diferente** do mesmo script, à linha 124 |

O facto C8 é «a partição por válvula testou 60,8 % da exploração», confirmado
por «as quatro reconstruções do esquema». **Duas das quatro estão declaradas sem
ligação a facto vivo. Valor certo: as quatro `CORRENTE`.**

**C4 · 14 ficheiros `orto_AAAA_10m.npy` / `orto_AAAA_50cm.npy` em
`NAO_ALCANCADO`, lidos por um `.py` `CORRENTE`.**
`g08_pomar.py:43,143` — `np.load(os.path.join(SAI, "orto_%s_10m.npy" % ano))`.
Nome construído por `%`; o `TOKEN` exige o literal. **Valor certo: `CORRENTE`.**

**C5 · A instrumentação do Controlo 3 é invisível à triagem: 86 de 88 ficheiros
`_controlo3_*` em `NAO_ALCANCADO`.**
Só `c8_05_veredicto.json` e `c8_05_veredicto.py` sobrevivem, porque o `.json`
está no `PV`. Ficam de fora, entre outros, `_controlo3_a2/c3a2_06_q3_identidade.py`
e `c3a2_10_veredicto.py` — que produziram a retirada do D8 e as correcções que
estão hoje escritas no `registo_de_factos.py:260-267` — e
`_controlo3_c9/q2b_copado.py`, do controlo que o próprio facto C9 cita
(«B1 a 6,06 m (Controlo 3, com controlo de costura 0,046 m)»,
`registo_de_factos.py:308-310`).
**Causa estrutural:** o Controlo 3 entrega `.md`, e `.md` não propaga
(`triagem_de_fontes.py:133-135`). O instrumento que apanhou as 21 retractações é
o único que a triagem não consegue ver. **Valor certo: os scripts citados por um
`.md` que o registo cita são `CORRENTE`** — ou, em alternativa, a triagem tem de
declarar que não classifica prova de retractação.

**C6 · A regra do produtor promove consumidores.**
`c2_11_figuras.py` foi classificado produtor de `c2_07_sar_pilha.npy`. À linha
**129** só faz `np.load(...)`. O que a janela de 260
(`triagem_de_fontes.py:206`) apanhou foi o `fig.savefig(...)` da **linha 124**,
que pertence a outra figura. **Valor certo: consumidor, não produtor.** A cadeia
publicada em `TRIAGEM_DE_FONTES.md` afirma o contrário.

**C7 · O `PV` sobre-declara: 4 das 15 entradas não são usadas por facto nenhum.**
`PV["valvulas"]`, `PV["esquema"]`, `PV["sar_ver"]` e `PV["c1ab"]` estão definidas
(`registo_de_factos.py:87,92,95,96`) e **nunca passadas a um `confirmar_com`**.
Ainda assim semeiam os respectivos ficheiros como `CORRENTE` e entram no conjunto
`citados` da verificação 8. O `PV` não é o manifesto que o cabeçalho da triagem
diz que é (`triagem_de_fontes.py:156-157`).

---

## REJEITADO

**R1 · «Corrente = há um caminho de *consumo* do registo até ele. Menção em
prosa não conta. Documentos não propagam.»**
(`triagem_de_fontes.py:31-35`, e repetido no cabeçalho do `TRIAGEM_DE_FONTES.md`.)
**Falso.** A semente (`triagem_de_fontes.py:166-169`) corre o `TOKEN` sobre o
**texto inteiro** do `registo_de_factos.py` e do `certificar.py` — docstring e
comentários incluídos — e promove tudo o que casar. Contei **21 dos 145
`CORRENTE`** que entraram por menção em prosa e cujo nome **não aparece** em
`ficheiro=` nem no `PV`. Os piores:

- `ganfei_s2/sar_invernos.py` — promovido pelo comentário do
  `registo_de_factos.py:126` que diz, textualmente, que ele **é exploratório** e
  que a proveniência que apontava para ele **estava errada**. A frase que o
  desqualifica é a frase que o classifica vivo.
- `_VALIDACAO_CAMADAS/A2_CONTROLO3_ADVERSARIO.md`, `C8_CONTROLO3_ADVERSARIO.md`,
  `REG01_RETRACCAO_A3.md`, `CONTROLOS.md` — `CORRENTE`;
  `C9_CONTROLO3_ADVERSARIO.md`, `B1_CONTROLO3_ADVERSARIO.md`,
  `REG01_CONTROLO3_ADVERSARIO.md`, `CAMADA_2_CONTROLO3_ADVERSARIO.md`,
  `P5_RETRACCAO_DO_REPLANTADO.md`, `C4_ADENDA_RAZAO_2026-09-03.md`,
  `PROTOCOLO.md`, `ANTES_DE_COMECAR.md` — `NAO_ALCANCADO`.
  **A classe é decidida por hábito de escrever comentários, não por papel
  probatório.** É a ausência de discriminação que o cabeçalho diz ter corrigido,
  no sítio onde ninguém foi ver.
- `valvulas_v4.json` (duas cópias) — ver C3.

**R2 · «SUBSTITUÍDO — duas fontes, ambas declaradas: uma convenção de directório
e a frase escrita num ficheiro vivo.»** (`triagem_de_fontes.py:219-232`.)
A segunda fonte é **inerte**. O `RE_SUB` não produziu **uma única**
classificação: os 3 `SUBSTITUIDO` vêm todos de `ARRUMADO` (`_bak_20260901/`).
Nenhum ficheiro vivo do corpus usa a forma «substitui `X.py`» que o regex exige.

**R3 · «É o erro de sempre num disfarce novo — um instrumento a concordar consigo
próprio.»** (`triagem_de_fontes.py:20-21`, dito da 1.ª versão.)
A 2.ª versão tem o mesmo defeito, mais estreito: **consumo é medido por regex
sobre o mesmo texto que o `TOKEN` varre**, e nunca contra a execução. Nenhuma das
sondas C1–C4 acima seria evitável por releitura do código — todas exigiram ir a
um instrumento diferente (correr o padrão contra o disco, medir a distância em
caracteres, ler o `mtime`). É a regra do `CLAUDE.md` a aplicar-se a este ficheiro:
**um regex não se confirma com outro regex.**

**R4 · «NÃO ALCANÇADO … não é "lixo", é a categoria honesta: nada neste processo
o liga a um facto vivo.»** (`triagem_de_fontes.py:44-46`.)
A frase é verdadeira sobre o *mecanismo* e falsa sobre o *processo*. Para os 301
ficheiros de `_densa_ganfei` e para `c2_12_prom_2010.npy`, o que os liga a um
facto vivo existe e está em disco — o que falta é a capacidade de o ver. A
categoria não é honesta enquanto o seu nome afirmar mais do que o teste mede.
Nome que o teste sustenta: **«sem ligação literal detectada»**.

---

## LINE-STOP

### LS-1 · A verificação 8 não bloqueia 8 dos 27 factos. Provado por simulação.

`certificar.py:267-271`:

```python
mortos = {os.path.basename(k): (v, k) for k, v in CL.items() ...}
citados = set(re.findall(r'ficheiro="([^"]+)"', txt_reg))
citados |= {os.path.basename(x) for x in re.findall(r'r"([^"]+\.\w+)"', txt_reg)}
maus = sorted({... for b in citados if b in mortos})
```

Duas falhas, ambas testadas contra uma cópia em memória da classe:

**(a) Os seis scripts do bloco B nunca entram em `citados`.**
`registo_de_factos.py:152-163` declara B1, B2, B3, B4, B5 e B7 num **tuplo**,
não em `ficheiro="…"`:
`("B1", "…", "Sentinel-2", "multiverso_degrau.py", GANFEI)`.
O primeiro regex exige o prefixo `ficheiro=`; o segundo exige um literal `r"…"`.
Nenhum casa. Ficam de fora `multiverso_degrau.py`, `degrau_vs_recta_pergola.py`,
`satelites_degrau.py`, `satelites_sem_2026.py`, `fenologia_por_unidade.py`,
`halo_distancia.py`.
> **Teste 1** — marquei `multiverso_degrau.py` (o `ficheiro=` do facto B1) como
> `RETIRADO` e corri a verificação 8 tal e qual: **`dispara? False`, `maus = []`.**

**(b) Os dois `ficheiro=` com directório nunca casam com `mortos`.**
`citados` guarda `"SAIDA_C1/c1_09_sar.py"` e `"SAIDA_C1/c1_03_mdt.py"`
(`registo_de_factos.py:130,299`) **com o prefixo**; `mortos` é indexado por
`os.path.basename`. `"SAIDA_C1/c1_09_sar.py" in mortos` é sempre `False`.
> **Teste 2** — `SAIDA_C1/c1_09_sar.py` (facto A2) `RETIRADO`: **`dispara? False`.**
> **Teste 3** — `SAIDA_C1/c1_03_mdt.py` (facto C9) `RETIRADO`: **`dispara? False`.**
> **Teste 4 (controlo positivo)** — `landsat.json` (`PV`, string `r"…"`)
> `RETIRADO`: **`dispara? True`, `['landsat.json (RETIRADO)']`.**

**Cobertura real da verificação 8: 19 dos 27 factos.** Os 8 desprotegidos são
A2, C9, B1, B2, B3, B4, B5, B7. A verificação existe, corre, imprime uma linha
verde, e não cobre um terço do registo.

**A verificação 4 tem exactamente o mesmo buraco.** `certificar.py:176` usa
`re.findall(r'ficheiro="([^"]+\.py)"', txt_reg)` — os seis scripts do bloco B
**nunca são verificados quanto a existência em disco**. A linha
«reprodutibilidade: todos os scripts citados existem» é verdadeira e não é o que
o leitor entende que é.

**Correcção mínima:** extrair os nomes por AST (ou pelo objecto `Facto`, que já
tem `.ficheiro`) em vez de por regex sobre o texto-fonte, e comparar por
`basename` dos dois lados. Enquanto isso não estiver feito, a verificação 8
não deve ser citada como garantia.

### LS-2 · Uma afirmação retirada está viva, sem marca, dentro de um `.py` e de um `.json` que a triagem diz `CORRENTE` — e dentro da secção viva da própria `LISTA_FINAL`.

O «1,77 ha / factor 7,1×» foi retirado. Está escrito:

- `C8_CONTROLO3_ADVERSARIO.md:284` — «X3 · "O esquema anota 1,77 ha para o B1;
  o IFAP dá 12,63 ha — factor 7,1×." **sai inteira.**» (não encontrado no
  documento; a medição por caracteres dá ~122 px e nenhum aglomerado se aproxima).
- `LISTA_FINAL_2026-08-31.md:274`, secção E, retirada 21 — «o "1,77 ha" sai
  também: **não está na tinta.**»

E continua escrito, sem marca nenhuma:

- **`LISTA_FINAL_2026-08-31.md:178`** — secção **viva** (a secção E começa à
  linha 235): «**O esquema anota 1,77 ha para o B1; o IFAP dá 12,63 ha — factor
  7,1×.** É uma instância concreta do C7.» **O mesmo documento afirma e retira a
  mesma frase, com 96 linhas de intervalo.** A verificação 2 do `certificar.py`
  não vê isto: compara **códigos** de facto, não conteúdo.
- **`valvulas_1a5_o_troco_que_falta.py:164-165`** — que é o `ficheiro=` do facto
  **C8**, e está `CORRENTE`. Imprime
  `"**O esquema anota 1,77 ha para o mesmo B1** — %.1fx." % (12.63/1.77)`.
- **`valvulas_1a5_o_troco_que_falta.py:196-197`** — escreve o número retirado
  para dentro do `valvulas_1a5.json`: verifiquei o ficheiro em disco,
  `area_esquema_ha: 1.77`, `factor: 7.1`. O `valvulas_1a5.json` está `CORRENTE`
  e é `PV["valvulas"]`.

É **exactamente** a classe que a tabela `DERRUBADAS` existe para cobrir
(«ficheiro vivo, linha morta», `triagem_de_fontes.py:75-92`) e é **o caso que
falta lá**. A tabela tem duas entradas; devia ter pelo menos três, e a terceira
é a única que contamina um **dado** e não só prosa.

### LS-3 · O teste do cartucho `RETIRADO` não apanha um documento retirado, e o mesmo teste governa a verificação 3 do `certificar.py`.

`P5_RETRACCAO_DO_REPLANTADO.md` diz, na sua segunda linha:
«**Retira:** `P3_ORIENTAL_REPLANTADO.md`, §2 e §3.»

`P3_ORIENTAL_REPLANTADO.md` **não tem cartucho**. A sua primeira linha é
`# P3 — o foco oriental foi REPLANTADO. E a correcção sobre a PSA.` — o título
afirma a retirada 16 (`LISTA_FINAL_2026-08-31.md:246`) em maiúsculas. A triagem classifica-o
`NAO_ALCANCADO`, não `RETIRADO`; o `certificar.py:155` usa o mesmo teste e
conta-o entre os **56 vivos**.

A regra do cartucho (`triagem_de_fontes.py:216-217`) é correcta e não tem falsos
positivos (K3) — mas a sua cobertura depende de alguém ter ido escrever o
cartucho, e **não foi escrito em pelo menos um caso**. Um mecanismo cujo teste de
«morto» é «alguém marcou» não pode ser apresentado como o que distingue vivo de
morto em disco, que é a justificação escrita da verificação 8
(`certificar.py:258-260`: «nada em disco distingue um ficheiro vivo de um morto.
A triagem distingue»). **Não distingue: repete a marca.**

**Correcção mínima:** cruzar os «**Retira:** `X`» dos documentos vivos contra o
cartucho de `X`, e falhar quando faltar. É um regex de três linhas e apanha este
caso.

### LS-4 · `fazer_masks_v2.py` está `CORRENTE` — «consulta-se».

`ganfei_s2/fazer_masks_v2.py` é o ficheiro que o `CLAUDE.md` deste projecto nomeia
como a armadilha de higiene número um: o cabeçalho (linhas 1-5) declara
«polígonos **GEOGRAFICOS e ESTATICOS**; nenhum é re-derivado por data» e o código
faz, à linha **23**, `copado = binary_opening((nd > 0.78) & (dist > 5), …)` sobre
a cena de 2026-07-27, e à linha **61** `mw = pomar & (nd < 0.76) & jw`. Máscara
derivada do sinal que se vai medir.

A regra do produtor (`triagem_de_fontes.py:187-213`) promove-o a `CORRENTE`
porque à linha **94** faz `json.dump(masks, open("sentinel/masks.json", "w"))`.
E promove **as três versões ao mesmo tempo**:

| ficheiro | classe | escreve |
|---|---|---|
| `ganfei_s2/fazer_masks.py` | **CORRENTE** | `sentinel/masks.json` |
| `ganfei_s2/fazer_masks_v2.py` | **CORRENTE** | `sentinel/masks.json` |
| `ganfei_s2/_TENTATIVA_FALHADA_mascaras_geograficas.py` | **CORRENTE** | `sentinel/masks_geograficas.json` |
| `_VALIDACAO_CAMADAS/SAIDA_MASCARAS/g18_final.py` | **CORRENTE** | `sentinel/masks_geograficas.json` |
| `_VALIDACAO_CAMADAS/REDERIVACAO_MASCARAS.md` | NAO_ALCANCADO | — |

**Resposta directa à pergunta 2 do encargo: sim — se duas versões de um script
escreverem o mesmo ficheiro, a regra do produtor promove as duas**, e não há
nada na saída que as separe. Os pares
`b1_serie_verdadeira.py`, `linhas_para_valvulas.py` e `exportar_pendentes2.py`
também aparecem duplicados, em duas árvores cada.

Pelo `mtime`, o produtor real de `masks_geograficas.json` (28-08 20:47) é o
`g18_final.py` (20:47), não o `_TENTATIVA_FALHADA…` (20:21) — mas isso soube-se
por ir ao sistema de ficheiros, não pela triagem. Um ficheiro que se autodenomina
**tentativa falhada** e um ficheiro que o `CLAUDE.md` proíbe usar saem os dois na
lista «consulta-se». E o documento que regista a re-derivação das máscaras,
`REDERIVACAO_MASCARAS.md`, sai em `NAO_ALCANCADO`.

**Correcção mínima:** quando N `.py` reclamam o mesmo produto, nenhum é promovido
automaticamente — a saída lista o conflito e alguém decide, como já se faz com
`CONFLITO` (`triagem_de_fontes.py:236-241`). Um prefixo `_TENTATIVA_FALHADA` é
uma declaração do autor, exactamente como `_bak_`, e devia valer o mesmo em
`CONV_SUB` (`triagem_de_fontes.py:149`).

### LS-5 · Os dois níveis contradizem-se no exemplo de bandeira.

A tabela `DERRUBADAS` (`triagem_de_fontes.py:77-83`) tem como primeira entrada
`_VALIDACAO_CAMADAS/CAMADA_1_CERTIFICADO.md`, e a instrução de uso do documento
diz: «se estiver em AFIRMAÇÕES DERRUBADAS, **o ficheiro consulta-se**, mas aquela
linha não» (`triagem_de_fontes.py:53-54`).

A triagem por ficheiro classifica `CAMADA_1_CERTIFICADO.md` como
**`NAO_ALCANCADO`** — «nada o liga a um facto vivo; perguntar antes de usar».

E `C9_CONTROLO3_ADVERSARIO.md`, que é o **«quem»** das duas entradas da tabela,
também está `NAO_ALCANCADO`.

O mesmo documento manda consultar e desaconselha consultar o mesmo ficheiro, em
duas secções que se leem com dois minutos de intervalo — e o ficheiro em causa é
onde vive a medição de costura (+0,058 m) que o facto **C9** usa
(`registo_de_factos.py:304-306`). A verificação 7 do `triagem_de_fontes.py:255-259`
só testa que o caminho **existe**; não testa a coerência entre os dois níveis.

---

## Notas de fronteira (não são defeitos, são limites por declarar)

1. **`.png` está fora do `EXT`** (`triagem_de_fontes.py:64`). A segunda entrada
   da `DERRUBADAS` diz, ela própria, que o dano foi que «a versão errada circulou
   **em PNG**». O artefacto que sai do edifício é o único que a triagem não
   consegue classificar.
2. **O `TRIAGEM_DE_FONTES.md` e o `triagem_de_fontes.json` estão `CORRENTE` e
   contêm os 1282 nomes.** Qualquer `grep` futuro do tipo «este ficheiro é
   mencionado nalgum sítio vivo?» devolve verdadeiro para tudo. Auto-contaminação
   do corpus, a partir de agora e para sempre.
3. **Constantes copiadas quebram a cadeia por desenho.** `satelites_degrau.py`
   (facto B3) traz as coordenadas dos núcleos em código, com o comentário
   «coordenadas publicadas no dossiê (`difusa_nucleos.csv`, via memo A07)`.
   Ambas as cópias do `difusa_nucleos.csv` estão `NAO_ALCANCADO`. Pela regra
   declarada está certo; para quem quiser reverificar B3, é a proveniência.
4. **`ANTES_DE_COMECAR.md` está `NAO_ALCANCADO`** — o documento que o `CLAUDE.md`
   manda ler antes de qualquer análise.

---

## Amostra de 15 `NAO_ALCANCADO` (semente 20260904, `random.sample`)

| # | ficheiro | veredicto |
|---|---|---|
| 1 | `_MULTIVERSO/SAIDA_A/06_mask.py` | correcto |
| 2 | `_VALIDACAO_CAMADAS/CAMADA_3_CERTIFICADO_R3.md` | duvidoso — citado por `c4_r2_01_multiverso_das_valvulas.py` (CORRENTE) |
| 3 | `_VALIDACAO_CAMADAS/SAIDA_C0/c0_03_proveniencia.json` | correcto |
| 4 | `_VALIDACAO_CAMADAS/SAIDA_C3/c3_r2_01_amostras.json` | correcto |
| 5 | `_VALIDADE_GESTAO/_controlo3_a2/c3a2_06_q3_identidade.py` | **falso negativo** — ver C5 |
| 6 | `_VALIDADE_GESTAO/_controlo3_a2/c3a2_10_veredicto.py` | **falso negativo** — ver C5 |
| 7 | `_VALIDADE_GESTAO/_controlo3_c8/c8_07_contiguidade.json` | duvidoso — irmão do `c8_05` que está CORRENTE |
| 8 | `_VALIDADE_GESTAO/_controlo3_c9/q2b_copado.py` | **falso negativo** — ver C5 |
| 9 | `_VALIDADE_GESTAO/_densa_ganfei/2018-06-17__0_L2A.npy` | **falso negativo** — ver C1 |
| 10 | `_VALIDADE_GESTAO/_densa_ganfei/2022-07-08__0_L2A.npy` | **falso negativo** — ver C1 |
| 11 | `_VALIDADE_GESTAO/_densa_ganfei/2025-06-30__0_L2A.npy` | **falso negativo** — ver C1 |
| 12 | `ganfei_s2/_pacote_cowork/LACUNA_BIOTICA.md` | correcto |
| 13 | `ganfei_s2/_pacote_cowork/fenologia.csv` | correcto |
| 14 | `ganfei_s2/_reexecucao_1a_sessao/reproducao/log_fazer_masks_v2.txt` | correcto |
| 15 | `ganfei_s2/difusa_nucleos.csv` | fronteira — ver nota 3 |

**6 falsos negativos e 2 duvidosos em 15.** Não é uma taxa: a amostra é enviesada
pela densidade de `_densa_ganfei` (301 dos 1132). Mas basta para o ponto: a
classe `NAO_ALCANCADO` **não** pode ser usada como sinal de que não vale a pena
abrir um ficheiro, que é o uso escrito no cabeçalho.
