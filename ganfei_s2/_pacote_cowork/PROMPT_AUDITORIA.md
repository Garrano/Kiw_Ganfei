# Prompt de auditoria — colar na sessão Cowork

Auditoria adversarial ao caso Ganfei (declínio de kiwi). Objectivo: validar,
refutar, corrigir ou melhorar o trabalho da sessão local e do project chat.
Não é revisão de estilo. É verificação de factos e de método.

## O que tens

O pacote `Ganfei_pacote_Cowork_2026-08-28.zip` (24 ficheiros): CSV de dados,
`masks.json`, `proveniencia.json`, figuras, dois scripts, `LEIA-ME.md` e
`AUDITORIA.md`. Lê o `AUDITORIA.md` primeiro — traz o mapa de rastreabilidade,
a lista do que NÃO está exportado e a lista vermelha escrita pelo próprio autor.

## Regras de prova

1. **Prosa não é evidência.** Nenhuma afirmação minha, da sessão local ou do
   project chat conta como suporte. Só contam células de ficheiros do pacote.
2. **Não corrijas em silêncio.** Toda a alteração vai para a tabela de saída
   com a justificação e a fonte.
3. **Não inventes concordância.** Se um número não bate, diz que não bate,
   mesmo que a diferença pareça pequena.
4. **Se não conseguires verificar, escreve NÃO VERIFICÁVEL.** Não estimes.
5. **Calcula primeiro, compara depois.** Tira o número do CSV antes de ir ver
   o que o dossiê diz. Não deixes o dossiê ancorar-te.

## TAREFA A — varrimento de rastreabilidade

Percorre o dossiê (§20 e anteriores), o mapa e a página do caso. Para cada
afirmação quantitativa, localiza ficheiro + coluna que a sustenta, usando a
tabela do `AUDITORIA.md`. Classifica:

- RASTREÁVEL — aponta ficheiro e coluna
- NÃO RASTREÁVEL — existe no dossiê, não existe em nenhum ficheiro
- CONTRADITÓRIA — o ficheiro diz outra coisa

Devolve a lista completa das NÃO RASTREÁVEIS e das CONTRADITÓRIAS.

## TAREFA B — coerência interna (fazer com os CSV, à mão)

Faz estas contas e diz se fecham. São todas verificáveis sem correr código.

B1. Em `expansao.csv`, a área de cada máscara sai de `*_px_validos` ÷ 100 (ha).
    Confirma que `*_defice_*_ha` ÷ área = `*_defice_*_pct` em todas as linhas.
B2. Em `expansao.csv`, `ref_saudavel_media` e `saudavel_uniao_ndvi_medio` devem
    ser idênticos por construção. Confirma em todas as 11 datas.
B3. Em todas as linhas, o défice severo tem de ser ≤ défice moderado.
B4. Cruza `manchaW_ndvi_medio` (`expansao.csv`) com `manchaW_ndvi`
    (`rededge.csv`) e com `manchaW_ndvi` (`expansao_b1.csv`). Vêm dos mesmos
    cenários e máscaras: têm de ser iguais. Se divergirem, é erro grave.
B5. Cruza `ref_saudavel_media` (`expansao.csv`) com `ref_saudavel_principal`
    (`expansao_b1.csv`) nas mesmas datas.
B6. Em `expansao_b1.csv`, confirma `b1_menos_ref` = `b1_ndvi_medio` −
    `ref_saudavel_principal`.
B7. Em `termico.csv`, calcula ΔT = máscara − saudável por cena, agrega por ano,
    e compara com o que o dossiê afirma para 2025 e 2026.
B8. Em `expansao.csv`, olha para `zona0_defice_moderado_pct` em 2025-08-14 e
    2026-07-27. **Se chegar a 100%, a série está censurada pela máscara** e a
    área deixa de poder crescer. Verifica se o dossiê tira conclusões dessa
    série sem assinalar a censura. Compara com `zona0_alargada_*` em
    `focos_datacao_geometria.csv`.
B9. Em `rededge.csv`, calcula (NDRE_manchaW − NDRE_saudavel) ÷
    (NDVI_manchaW − NDVI_saudavel) nas datas em que o denominador é > 0,004.
    O dossiê afirma que a razão fica entre 0,84 e 1,12. Confirma ou refuta.

## TAREFA C — lista vermelha (o essencial)

Ataca por esta ordem. Estes três pontos determinam tudo o resto.

C1. **Máscaras.** `masks.json` tem os polígonos. `manchaW` é o footprint de
    2026 — logo os valores anteriores a 2025 dizem o que aquele terreno era
    quando estava são. Isto é legítimo ou é circular? A `zona0` já foi
    redesenhada uma vez. O `pomar` sai de um limiar de NDVI escolhido a olho.
    Pergunta: quais das conclusões do dossiê sobreviveriam a máscaras
    desenhadas por outra pessoa? Marca as que não sobreviveriam.
C2. **Referência sã.** 4,46 ha em 3 manchas, escolhidas pelo autor. Todo o ΔT
    e todo o défice são relativos a ela. Em `expansao.csv`, `ref_saudavel_dp`
    varia entre 0,014 e 0,111 conforme o ano — o que diz isso sobre a
    estabilidade da referência? A de 2017 (0,111) é utilizável?
C3. **Pomares novos.** É o pilar da hipótese hidráulica e **não está
    exportado**. Limiares arbitrários, anos aproximados, propriedade dos blocos
    não confirmada. Decide se pode sustentar o que o dossiê lhe faz sustentar.

## TAREFA D — secção não exportada

O `AUDITORIA.md` lista oito conjuntos de resultados que circularam em prosa e
não existem em ficheiro (precipitação, geada, secagem SAR, pomares novos,
bacia, escoamento, rugosidade, degrau entre campanhas). Decide, um a um:
sai do dossiê, ou fica com marca visível de não-verificado. Justifica.

## TAREFA E — correcções já identificadas

E1. **Aplicar:** os "12 m" entre o centro do foco e o traço L1 têm precisão
    falsa. As coordenadas do L1 foram lidas visualmente sobre uma grelha
    desenhada, com incerteza de ±10 a 15 m por extremo. Substituir por
    "a menos de ~25 m do alinhamento L1" onde aparecer.
E2. **Confirmar:** a correcção do "maior incremento isolado" (é 2022 com
    4,09 ha, não 2025 com 2,72) está aplicada em todo o lado — dossiê, mapa e
    página do caso, não só no LEIA-ME.
E3. **Verificar:** que a retirada do "B1 com conduta própria" está feita em
    todos os documentos, e que a exclusão de falha total de fonte continua
    correctamente fundamentada (origem única + B1 intacto).

## Formato de saída

Uma tabela, uma linha por achado:

| # | onde | afirmação | veredicto | fonte | acção |

Veredicto ∈ {CONFIRMADO, REFUTADO, CORRIGIR, NÃO VERIFICÁVEL, MELHORAR}.
Fonte = ficheiro + coluna, ou "nenhuma".
Acção = a redacção exacta a substituir, quando aplicável.

Ordena por gravidade: primeiro o que muda conclusões, depois o que muda
números, depois o que muda redacção.

No fim, responde a três perguntas em texto corrido:

1. Qual é a conclusão do caso que está pior sustentada pelos dados?
2. Que afirmação do dossiê retirarias já?
3. Que verificação, ainda por fazer, mudaria mais o caso se fosse feita?

## Aviso

O autor deste trabalho já cometeu oito erros neste caso, todos apanhados, e
**nenhum foi de aritmética** — foram de construção de método e de âmbito
(bacia sem resolução de zonas planas, degrau medido em bordos inteiros, NDVI
tirado de ortofotos equilibradas para visualização, máscara saturada lida como
estabilização, AOI que durante sete turnos não continha o bloco B1). A tabela
completa está no `AUDITORIA.md`.

Não gastes o esforço a reconferir contas. Gasta-o a perguntar, para cada
resultado: **este teste mede o que diz medir, e a área analisada é a certa?**
