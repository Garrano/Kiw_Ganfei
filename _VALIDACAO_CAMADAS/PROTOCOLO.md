# Validação em camadas — protocolo

Caso: declínio do kiwi, Emparcelamento de Ganfei, Valença.
Aberto em 28-08-2026.

## Porquê

Em 28-08-2026 descobriu-se que a série de satélite chamada «lóbulo oeste B1»
media vegetação urbana em Valença, do outro lado do rio Minho. A AOI nunca
tinha sido confirmada — o próprio script que a criou lhe chamava «candidato a
B1». Semanas de conclusões assentavam nela: um bloco de controlo são, um
declive de −0,013 NDVI/década, uma distância de 1,06 km, e por fim um «núcleo
em declínio com p < 0,0005» que não existe.

O erro não foi de análise. Foi de **fundação**: uma pergunta da camada mais
funda — *onde fica o pomar* — que nunca foi validada, e sobre a qual se
empilharam quatro camadas de inferência.

Este protocolo existe para que isso não volte a acontecer.

## A pilha

Cada camada só pode assumir como dado aquilo que a camada de baixo certificou.
Nenhuma camada vê as conclusões das camadas de cima.

```
  C5  DECISÃO          desenho de amostragem, Pilar D, gestão
       ▲                depende de tudo
  C4  INFERÊNCIA       diagnóstico diferencial, exclusões, etiologia
       ▲                depende de C0+C1+C2+C3
  C3  BIOLOGIA         patogénios, nemátodos, ITS, microbioma
       ▲                depende de C0 (onde) e C2 (relacionar com o padrão)
  C2  SINAL VEGETAL    NDVI, défice, séries, áreas, tendências
       ▲                depende de C0 (máscaras); lê-se contra C1
  C1  SUBSTRATO        terreno, solo, clima, hidráulica, térmico
       ▲                depende de C0 só para o «onde»
  C0  GEOMETRIA        AOI, polígonos, máscaras, proveniência das cenas
                        depende de nada. É onde tudo assenta.
```

**A camada 0 não estava no seu esquema e é a que falhou.** Fica primeiro.
E a camada 2 — a medição do sinal — fica separada da biologia, porque a
biologia só ganha sentido quando relacionada com um padrão já validado.

## Regras

**1. Herança fechada.** Cada sessão recebe: o certificado de todas as camadas
abaixo, **e o adversário de cada um desses certificados**, e os dados brutos da
sua própria camada. Mais nada. Não recebe as figuras, o dossiê, nem as
conclusões das camadas acima.

> **Emenda de 29-08-2026 — a segunda oração acima é nova, e a razão está
> medida.** Até aqui a regra dizia só «o certificado de todas as camadas
> abaixo». Os ficheiros `*_ADVERSARIO.md` **não são certificados**, e por isso
> eram a **única classe de documento que nenhuma camada tinha autorização para
> herdar** — apesar de serem exactamente onde vivem as retiradas.
>
> **Consequência medida pelo adversário da C4: dezasseis instâncias documentadas
> de correcção perdida, contra uma transportada.** Quinze das dezasseis foram
> apanhadas por adversários posteriores; **nenhuma pela camada que recebeu o
> facto errado.** A C4 denunciou o padrão e cometeu-o na mesma.
>
> **A regra estava a produzir o erro que a cadeia inteira existe para evitar:**
> um facto retirado continuava a subir, porque o documento que o retirava não
> era herdável. Uma linha de emenda vale mais do que todas as retiradas somadas.
>
> **Corolário obrigatório:** onde um certificado e o seu adversário
> discordarem, **ganha o adversário** — pela mesma precedência com que a
> `CAMADA_0_REVISAO_R2.md` ganha sobre o certificado da C0. E onde existir
> revisão posterior (`_R2`), essa ganha sobre ambos.

**2. Paragem de linha.** Se uma sessão rejeitar um facto certificado por uma
camada abaixo, **pára**. Não continua a construir por cima. Escreve o que
rejeitou e porquê, e devolve. A cadeia recomeça na camada afectada.

**3. Um facto, uma prova.** Cada facto certificado tem de nomear o ficheiro e o
cálculo que o sustenta. «Está no dossiê» não é prova. «Foi verificado numa
sessão anterior» não é prova.

**4. A dúvida é resultado.** «Não consegui verificar» é uma saída válida e
obrigatória quando é o caso. Um facto inventado destrói a cadeia inteira;
uma lacuna assinalada não.

**5. Não teorizar acima da própria camada.** A C1 não opina sobre patogénios.
A C3 não opina sobre a causa. Cada camada responde ao que lhe compete.

## O certificado

Cada sessão escreve `CAMADA_n_CERTIFICADO.md` com cinco secções, exactamente:

```
## CONFIRMADO
  facto | ficheiro e cálculo que o prova | margem de erro

## CORRIGIDO
  o que se dizia | o que está certo | o que muda acima

## REJEITADO
  o que não sobrevive | porquê | que conclusões acima caem com ele

## NÃO TESTÁVEL
  o que não se conseguiu verificar | o que faria falta para verificar

## PASSA PARA CIMA
  a lista fechada de factos que a camada seguinte pode tratar como dados.
  Tudo o que não estiver aqui, não passa.
```

E depois escreve `CAMADA_n+1_PROMPT.md` para a sessão seguinte, usando o
modelo em `MODELO_PROMPT.md` e enchendo-o com o que acabou de certificar.

## Conteúdo de cada camada

**C0 · GEOMETRIA** — AOI, polígono do pomar, máscaras zona0 / manchaW /
saudavel×3, proveniência das 11 cenas, bandeiras de fenologia, harmonização
BOA, o ajuste válvula↔imagem da M1, as coordenadas do traço de 1995, e a
quarentena de tudo o que derivou de `sentinel_b1/`.

**C1 · SUBSTRATO** — LiDAR (21 mosaicos, MDT, bacia, ensaio de costura),
boletins de solo A2 (11), térmico Landsat (148 cenas) e a sua retirada,
precipitação ERA5-Land, SAR Sentinel-1 (três Invernos), hidráulica da rede de
rega e origem única, hipótese de nivelamento e truncatura.

**C2 · SINAL VEGETAL** — série NDVI, limiar de défice, zona de referência,
séries da Zona 0 e da Mancha W, geometria de expansão, frente em avanço,
núcleos difusos, e a regra nova da M2 (só conta como declínio o que esteve
comprovadamente são antes).

**C3 · BIOLOGIA** — 212 registos de laboratório, georreferenciação,
*M. hapla*, «Kiwi 1000», ITS e a qualidade de leitura, Becrop e a válvula 27,
a contaminação do caso Kiwi Atlántico, *Rosellinia* de campo contra o negativo
molecular.

**C4 · INFERÊNCIA** — matriz de diagnóstico, livro-razão das exclusões,
o argumento geométrico, a convergência para a subsuperfície.

**C5 · DECISÃO** — desenho de amostragem, árvore do Pilar D, medidas.

## Estado

| Camada | Estado | Certificado |
|---|---|---|
| C0 | **feito** 28-08-2026 | `CAMADA_0_CERTIFICADO.md` · código em `SAIDA_C0\` |
| C0 | revisto | `CAMADA_0_REVISAO_R2.md` + suplemento — **substitui o certificado** |
| C1 | **feito** 29-08-2026 | `CAMADA_1_CERTIFICADO.md` · S1–S19 · código e 4 figuras em `SAIDA_C1\` |
| — | adversário da C0 | `CAMADA_0_ADVERSARIO.md` — veredicto: segue com retiradas |
| — | controlo externo | `CAMADA_0_ADENDA_CONTROLO.md` — **não existe controlo de kiwi contemporâneo** |
| — | máscaras geográficas | `REDERIVACAO_MASCARAS.md` + `masks_geograficas.json` |
| — | série re-executada | `_serie_geografica.txt` — grandeza operativa fixada: magnitude |
| — | M1 v3 | `M1_valvulas_v3.png` — sem atribuição ponto→válvula |
| C2 | **feito** 29-08-2026 | `CAMADA_2_CERTIFICADO.md` · V1–V11 · código e 4 figuras em `SAIDA_C2\` |
| — | adversário da C2 | `CAMADA_2_ADVERSARIO.md` — veredicto: segue com R1–R4 |
| — | adenda de LiDAR | `CAMADA_2_ADENDA_LIDAR.md` · L1–L8 — **ganha sobre o certificado da C2** |
| C3 | feito 29-08-2026 | `CAMADA_3_CERTIFICADO.md` · B1–B11 · código e 2 figuras em `SAIDA_C3\` — **histórico: substituído pela R2** |
| — | adversário da adenda de LiDAR | `ADVERSARIO_2026-08-29.md` — **L4 e L6 RETIRADOS**; ver aviso no topo da adenda |
| — | adversário da C3 | `CAMADA_3_ADVERSARIO.md` — **não segue como está**: oito retiradas R1–R8; paragem de linha passa de REJEITADO a **NÃO RESOLVIDO — relato contra documento** |
| C3 | **revisto** 29-08-2026 | `CAMADA_3_CERTIFICADO_R2.md` — **substitui o certificado da C3**. Oito retiradas aplicadas; **T2 e T4 corridos** (`SAIDA_C3\c3_13_T2_T4.py`). A linha «amostras» da G34 passa a **NÃO RESOLVIDO — relato contra documento, precedência por decidir** |
| — | multiverso H2, porta-enxerto | `_MULTIVERSO\AGREGACAO_H2.md` — H2a SUPORTA (3/3 + radar); **H2b INCONCLUSIVO** |
| — | adversário da ronda H1 | `_MULTIVERSO\ADVERSARIO_H1.md` — **o viés do S2C não existe nos dados**: quatro medições emparelhadas de quatro corridas dão ≈ 0, e o **−0,048** não vem de nenhuma delas. **Cai a segunda metade da L5.** Retira também a metade **oriental** de L3 como teste (o voo cai dentro da janela) |
| — | **testemunho do gestor, 29-08** | **o «Kiwi 1000» é o informe 331/2025** e está situado **no lado oeste do maior vazio circular — zona, não ponto**. *(A parametrização «centro E530476 N4655046, a 11,4 m do foco OESTE» foi RETIRADA pelo `CAMADA_4_ADVERSARIO.md`: é o núcleo n.º 22 da corrida B, delimitado por anomalia de NDVI/NDMI, de 2026, aplicado a colheita de 2025-06-06; os 11,4 m eram a distância entre duas estimativas do mesmo centróide pelo mesmo instrumento.)* **O gestor confirmou em 29-08 que viu o vazio NO TERRENO** — logo a colocação é independente do nosso sensoriamento remoto. **Tipo 1, ganha ao documento. B4 cai pelos termos da própria C3.** As **ITS ISFBV0314–17 mantêm-se em NÃO RESOLVIDO** — o gestor não sabe, e os PDF **não existem nesta máquina** (verificado): documento indisponível, não informação inexistente |
| C4 | **feito** 29-08-2026 | `CAMADA_4_CERTIFICADO.md` · D1–D8 · **`SAIDA_C4\c4_razao_exclusoes.csv`: 59 causas, 41 NÃO TESTADAS**, 7 excluídas, 4 excluídas só numa zona e numa data, 5 sustentadas, 2 inconclusivas |
| — | adversário da C4 | `CAMADA_4_ADVERSARIO.md` — **dez retiradas, oito margens alargadas**. Passa intacto D6 («a matriz de diagnóstico tem uma coluna») e D8 (**PSA nunca procurada**). Dele saiu a **emenda à regra 1**: dezasseis correcções perdidas contra uma transportada |
| C5 | **feito** 29-08-2026 | `CAMADA_5_CERTIFICADO.md` · `SAIDA_C5\` — re-etiquetagem das 59 causas (**24 mal rotuladas, 11 procuradas e encontradas**), desenho de amostragem (12 plantas, 48 amostras, dois pares sãos). **Exclusões passam de 7 para 3.** A decisão **não fecha**, e declara-o. **Rejeita a árvore F6 e o desenho F5 do `_pacote_cowork\`** |
| — | adversário da C5 | **a correr** 29-08-2026 |
| — | paisagem | `_VALIDADE_GESTAO\paisagem.py` — a mata madura **não caiu** (−0,0035, p=0,81); cai o ciclo curto (milho −0,077). **O enquadramento do caso aguenta.** Fecha REG-03, **não fecha REG-01** |
| — | testemunho de 29-08 | o **vazio circular foi visto no terreno**, não numa imagem nossa — a colocação do «Kiwi 1000» é **independente** do nosso sensoriamento remoto, e o dossiê deixa de ter zero observações de campo |
| — | pergunta aberta que travava três factos | **RESOLVIDA A METADE.** O «Kiwi 1000» tem lugar (testemunho); as quatro ITS não. **B4 cai; B3 e B11 mudam de razão; B5 mantém-se como afirmação documental** — ver `CAMADA_4_CERTIFICADO.md` §0 e CORRIGIDO |
| — | **condição de arranque não cumprida, e nunca registada** | o **T3** do adversário da C2 — prominência de pérgola sobre a ortofoto de **2025** — era condição de arranque da C3 e **não correu** (não existe `c2_12_prom_2025.npy`). É o teste que distingue copado em declínio de copado arrancado ou re-armado |
| — | **por re-certificar na C0** | a **G10** / a reposição da cena de 2019-09-02 (condição 1 do adversário da C2). A **V11** depende inteiramente dela |
| — | **facto forte que nunca entrou em lista fechada** | a **série Landsat** (`_VALIDADE_GESTAO\landsat.json`) — único instrumento verdadeiramente externo do caso; mede a referência a cair 0,888 → 0,874 → 0,862 |

---

## Controlos (adenda de 28-08-2026)

Ver `CONTROLOS.md`, em ficheiro próprio porque foi escrito com a C0 já a
correr. Aplica-se a partir da C1, e à revisão adversarial da C0.

Em resumo: **não se duplicam sessões** — duas sessões com o mesmo prompt
cometem erros correlacionados e teriam ambas aceitado o «B1». Em vez disso:

1. **Regra do instrumento independente** — nenhum facto passa para cima se só
   foi verificado com o instrumento que o produziu.
2. **Quantidades-âncora** — dez valores que todas as camadas reportam sempre,
   para a divergência saltar sozinha.
3. **Adversário do certificado** — em C0 e C2 apenas, depois de o certificado
   estar escrito, sem acesso aos dados brutos. Prompt em `ADVERSARIO_PROMPT.md`.

**Nota de 29-08-2026, para o `CONTROLOS.md` não continuar a descrever uma
prática que já não é a nossa.** O `CONTROLOS.md` escreve «não se corre
adversário em C1, C3, C4, C5». **Na prática correram-se quatro** — C0, C2, a
adenda de LiDAR, e a C3 — e o coordenador determinou que a **C4** leva também.
Os dois que o `CONTROLOS.md` dispensava (C3 e C4) **produziram as retiradas mais
consequentes da cadeia**: as oito da C3, e a paragem de linha que só o
adversário travou. A regra escrita e a prática divergiram, e é a prática que
tem razão. **A C5 deve assumir que leva adversário.**
