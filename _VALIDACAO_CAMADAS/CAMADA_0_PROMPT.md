# Camada 0 — Geometria e proveniência

*(copiar tudo a partir da linha abaixo para a sessão nova)*

---

És a primeira sessão de uma cadeia de validação em camadas. Lê primeiro
`Downloads\_VALIDACAO_CAMADAS\PROTOCOLO.md`, que explica a pilha e as regras.

A tua camada é a **C0 — geometria e proveniência**. É a base de tudo. Não
herdas nada: não há camada abaixo de ti.

**Não leias o dossiê, as figuras, nem as conclusões.** Não precisas delas e
contaminam-te. Se abrires uma figura por engano, regista isso no certificado.

## Porque esta camada existe

Em 28-08-2026 descobriu-se que a série `sentinel_b1/` — usada durante semanas
como «lóbulo oeste B1», um bloco de kiwi são a 1,06 km — tem a AOI em
(528400, 4654900, 529400, 4655700), que fica **na cidade de Valença, do outro
lado do rio Minho**. O script que a criou (`b1_serie.py`) chama-lhe, na
primeira linha, «candidato a B1». Nunca foi confirmada. Tudo o que dela saiu
está agora em quarentena.

A tua tarefa é garantir que não há mais nenhuma assunção geométrica por
confirmar. Assume que há.

## Materiais

```
Downloads\ganfei_s2\sentinel\          11 GeoTIFF NDVI + masks.json + proveniencia.json
Downloads\ganfei_s2\sentinel_b1\       EM QUARENTENA — ver tarefa 5
Downloads\ganfei_s2\figuras\m1_valvulas.py   o ajuste valvula<->imagem
Downloads\ganfei_s2\_pacote_cowork\tracos_1995_coordenadas.csv
Downloads\_GANFEI_REEXECUCAO_CEGA\SAIDA\     auditoria cega ja concluida
Downloads\Esquema de rega retificado.pdf     o esboco de rega, desenho a mao
Downloads\ganfei_s2\orto\                    ortofotos DGT, 7 epocas
```

Tens internet para reler cenas Sentinel-2 do AWS Open Data se precisares
(colecção `sentinel-2-l2a`, Earth Search STAC v1, sem credenciais).

## TAREFA 1 — a AOI e o polígono

A AOI é (529950, 4654600, 531950, 4655600) em EPSG:32629. O polígono `pomar`
em `masks.json` dá 29,0 ha de copado.

- Vê a imagem verdadeira (RGB, não NDVI) e confirma que a AOI contém o pomar
  **inteiro**. Testa em particular se corta alguma coisa a sul, a leste ou a
  oeste: alarga a janela 700 m em cada direcção e olha.
- O polígono `pomar` segue o copado real, ou inclui outra coisa (caminhos,
  culturas vizinhas, ripícola)? Usa as ortofotos DGT, que têm resolução muito
  melhor que os 10 m do Sentinel.
- O total do pomar segundo o esquema de rega é ≈44,9 ha em 27 válvulas. O
  polígono tem 29,0 ha. **Onde estão as outras ~16 ha?** Esta pergunta está
  em aberto e é tua.

## TAREFA 2 — as máscaras

`masks.json` tem `pomar`, `zona0`, `manchaW`, `saudavel`, `saudavel_2`,
`saudavel_3`.

- Sobrepõe cada uma às imagens de várias datas e diz se a geometria é
  defensável ou arbitrária.
- **A referência sã (4,54 ha, três manchas) é o pivô de toda a análise**: o
  défice é definido contra ela. Se ela própria estiver a descer, todo o défice
  é subestimado. Mede a tendência da referência ao longo das 11 datas.
- Há um defeito conhecido e já registado: a prosa citou contagens de máscara
  booleana (pomar 2906 px, saudavel 446, manchaW 423, zona0 219) quando os
  valores operativos são os do polígono (2903, 454, 427, 220). Confirma quais
  estão certos e regista a discrepância.
- As máscaras são geográficas e estáticas, ou alguma foi derivada do NDVI que
  depois se vai medir? Se alguma for, é circular e tens de o dizer.

## TAREFA 3 — proveniência das cenas

`proveniencia.json` lista 11 datas.

- Confirma que cada cena existe, que o identificador bate certo, e que a
  janela lida corresponde à AOI.
- Harmonização BOA: as cenas posteriores a Janeiro de 2022 têm o offset de
  −1000 aplicado. Verifica `earthsearch:boa_offset_applied` em cada uma e diz
  se a série é comparável ao longo do tempo. **Se não for, a série inteira
  fica em causa.**
- Fenologia: 2019-09-02 e 2025-06-17 estão marcadas como fora da janela de
  plena estação. Está certo? Alguma outra devia estar?
- Máscara de nuvem: o SCL vem a 20 m e é reamostrado para 10 m com vizinho
  mais próximo. Verifica se alguma data tem contaminação residual dentro do
  polígono.

## TAREFA 4 — o ajuste válvula↔imagem

`figuras\m1_valvulas.py` coloca as válvulas 6 a 13 usando duas âncoras dadas
pela gestora (Mancha W no limite B1/B2; Zona 0 = válvulas 8-9-10), e declara
±40 m. As válvulas 1–5 e 14–17 ficaram por colocar.

- O ajuste é defensável? Refá-lo à tua maneira a partir do PDF do esquema e
  diz quanto difere.
- **Nota:** um ajuste proporcional directo do esboço põe as válvulas 1–5 em
  E528634–529088 — que é quase exactamente a AOI errada. Confirma isto: é a
  explicação de como o erro nasceu, e é importante que fique provado.

## TAREFA 5 — quarentena de `sentinel_b1/`

Confirma, com a imagem, que a AOI (528400, 4654900, 529400, 4655700) está do
outro lado do rio e não contém pomar. Depois **faz o inventário completo** de
tudo o que derivou dela — ficheiros, CSV, scripts, números — para que se saiba
o que tem de ser apagado ou reetiquetado. Procura em `Downloads\ganfei_s2\`.

Não apagues nada. Lista.

## TAREFA 6 — o que mais está por confirmar

Procura outras assunções geométricas que ninguém validou. Sugestões de onde
olhar, sem te limitares a elas: as coordenadas do traço de 1995; a AOI do
LiDAR; a cobertura das ortofotos; qualquer distância citada em metros.

Para cada uma: é medida, deduzida, ou assumida?

## O que entregar

1. `CAMADA_0_CERTIFICADO.md`, com as cinco secções exactas do protocolo.
   A secção **PASSA PARA CIMA** é a mais importante: é a lista fechada de
   factos geométricos que as camadas seguintes podem usar. Sê avaro. O que
   não estiver lá, não existe para elas.

2. `CAMADA_1_PROMPT.md` para a sessão seguinte, seguindo `MODELO_PROMPT.md`.
   A camada 1 é o **substrato**: terreno, solo, clima, hidráulica, térmico.
   Enche o modelo com o que certificaste, e com as perguntas geométricas que
   ficaram em aberto e que a C1 precisa de saber que estão em aberto.

3. O teu código em `SAIDA_C0\`.

Se encontrares algo que invalide a análise inteira, escreve-o na primeira
linha do certificado e pára. É para isso que serve a paragem de linha.

---

## ADENDA de 28-08-2026, tarde — três achados que mudam a tua tarefa

Depois de escrito o prompt acima, a gestora contestou o mapa M2 e mandou uma
vista de satélite. A verificação contra as ortofotos DGT deu o seguinte, e é
material para ti:

**1. A classificação «nunca esteve são» está ERRADA e tem de ser refeita.**
A M2 pintou 8,21 ha de cinzento com o argumento de que, estando em défice
desde a primeira cena, nunca teriam sido copado — logo seriam caminhos ou
falhas. A ortofoto de 2025 a 25 cm mostra **linhas de pomar contínuas em toda
essa área**. Não são falhas: é pomar plantado que **já estava abaixo da
referência em 2017**.

A consequência é maior do que a correcção: se aquilo já estava em défice na
primeira cena, **o declínio começou antes de 2017 e a série de satélite não
consegue datar o início**. Toda a cronologia do caso assenta numa série que
começa depois do princípio. Testa isto e diz o que sobra.

**2. Houve uma alteração física do coberto entre 2021 e 2025.** Na janela
E530550–531200 / N4654930–4655300, a fracção de área muito clara passa de 8%
(2010) e 9% (2021) para **21% (2025)** — faixas brancas contínuas ao longo das
linhas, compatíveis com rede ou cobertura instalada nesse intervalo.

**3. Mas a cobertura NÃO explica o padrão de défice** — já foi testado, e o
resultado é negativo: a máscara de cobertura ocupa 21% da Mancha W, 22% da
Zona 0 e 25% da referência sã, ou seja é uniforme, e o NDVI sob cobertura é
+0,02 a +0,03 mais ALTO, não mais baixo. Regista este negativo: poupa tempo a
quem vier a seguir, e impede que a hipótese volte a entrar sem prova.

## TAREFA 7 — refazer os dois mapas, com rigor

Os mapas M1 (válvulas e sectores, para a gestora) e M2 (declínio, interno)
estão em `Downloads\ganfei_s2\figuras\`. A gestora rejeitou ambos. As críticas
dela, textuais:

- as zonas marcadas como sem copado têm copado, em particular a região a leste
  adjacente à Mancha W;
- a identificação das válvulas e as linhas **não estão alinhadas com os
  sectores nem com a parcela**;
- não mostram as áreas com porta-enxerto diferente.

As duas primeiras são justas e a segunda é um erro geométrico claro: as
fronteiras foram desenhadas como linhas verticais N–S, quando os sectores do
esquema de rega são faixas **perpendiculares ao eixo da parcela**, que corre
WSW–ENE. Além disso os sectores não atravessam a parcela toda: derivam para
norte ou para sul da conduta, e o esquema mostra duas filas de válvulas.

Refá-los com o rigor que a tua camada exige:

- fronteiras perpendiculares ao eixo real da parcela, não ao norte da folha;
- sectores norte e sul distintos, como no esquema;
- o porta-enxerto como camada própria — Summer Kiwi nas válvulas 2–5, pé
  franco de Erica no resto — desenhado só onde a posição estiver estabelecida;
- a regra da M1 mantém-se e é inegociável: **zero informação de declínio**, que
  a M1 vai ser usada para obter confirmação independente da geometria;
- na M2, substituir o cinzento por uma classe honesta: «já em défice na
  primeira cena — início não datável».

Se concluíres que o esquema de rega não permite fronteiras defensáveis, **diz
isso e desenha só o que se sustenta**. Um mapa com menos informação e sem erro
vale mais do que um completo e errado — foi o erro que já se cometeu duas
vezes neste processo.
