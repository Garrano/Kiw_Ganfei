# Auditoria independente — resultado
Sessão sem acesso ao código nem aos resultados do autor · 28-08-2026

Implementou os seis quadros de raiz a partir da especificação, registou 25
ambiguidades com o impacto **calculado**, e produziu um julgamento.

## Concordância

| quadro | resultado |
|---|---|
| Q3b (térmico residual) | declive −15,88 vs −15,48 · r −0,768 vs −0,756 · resíduo 2025 +0,052 vs +0,07 · 2026 +0,357 vs +0,41 |
| Q4 cotas por máscara | pomar 6,969 vs 6,972 · ref 7,016 vs 7,019 · manchaW 6,669 vs 6,671 · zona0 8,024 vs 8,026 |
| Q4 percentis no pomar | 50 / 52,5 / 32,5 / 92,4 — idênticos |
| Q1 séries de NDVI | máx. \|dif\| 0,007 em 44 comparações |
| Q1 áreas de défice | máx. \|dif\| 0,39 ha |

**A correcção mais consequente do caso — o térmico ser contabilidade de copado —
foi reproduzida por uma implementação independente.** Duas bases de código
diferentes, o mesmo veredicto.

## DEFEITO 1 — convenção de pixel mal documentada (meu)

A especificação diz "um pixel pertence à máscara se o seu **centro** cai dentro
do polígono". O meu código testa o **índice** do pixel (`np.mgrid` → inteiros),
não o centro (+0,5). Meio pixel de diferença.

Os polígonos vêm de `find_contours`, cujos vértices caem entre células — nessa
construção o índice é a convenção correcta. **O código está certo; a
especificação é que está errada.** Consequência medida:

| máscara | eu (índice) | eles (centro) | dif |
|---|---|---|---|
| pomar | 2903 px | 2896 px | −7 |
| referência sã | 454 px | 415 px | **−39 (−8,6 %)** |
| manchaW | 427 px | 425 px | −2 |
| zona0 | 220 px | 221 px | +1 |

A referência é a que mais mexe, e é ela que define o `ref` de tudo. Daí os
±0,007 de NDVI e ±0,39 ha nas áreas. **Nenhuma conclusão muda**, mas cada número
publicado carrega esta incerteza. Corrigir a redacção da especificação para
"índice do pixel", não "centro".

## DEFEITO 2 — domínio da regressão cota~NDVI não especificado (meu)

A especificação diz "excluindo manchaW e zona0" sem dizer **em que domínio**.
Verifiquei os dois:

| domínio | n | declive | r | manchaW vs previsto |
|---|---|---|---|---|
| só dentro do `pomar` | 2 258 | −0,058 | **−0,338** | −0,107 |
| toda a AOI | 17 428 | +0,036 | **+0,325** | **+0,315** |

**O sinal inverte.** Mas os dois ramos não valem o mesmo: sobre toda a AOI a
regressão cruza rio (NDVI negativo, cota 1–3 m), povoado e mata de encosta — é
um artefacto de ocupação do solo, não uma relação agronómica. A previsão de
0,433 de NDVI para a cota da manchaW é, na prática, a previsão para *água*.

Correcção de redacção obrigatória: a afirmação **"o baixo é o sítio saudável"
vale dentro do copado do pomar**, não é uma afirmação de paisagem. Especificar
o domínio em todo o lado.

## ACHADO 3 — metade do défice está fora dos dois focos (deles)

Não foi erro meu de cálculo; foi omissão de enquadramento. Verificado:

| ano | défice no pomar | manchaW | zona0 | **fora dos dois** | % fora |
|---|---|---|---|---|---|
| 2019 | 5,37 ha | 0,11 | 1,19 | 4,08 | 76 % |
| 2022 | 5,09 | 0,00 | 1,30 | 3,79 | 75 % |
| 2024 | 4,73 | 0,13 | 1,25 | 3,35 | 71 % |
| 2025-08 | 7,97 | 1,44 | 2,19 | 4,36 | 55 % |
| **2026** | **11,50** | 3,60 | 2,20 | **5,72** | **50 %** |

Há uma linha de base de 3,4 a 4,9 ha fora dos focos em **todos** os anos —
plausivelmente bordaduras, caminhos e pixels mistos de 10 m, e por isso
estrutural. Mas **de 2024 para 2026 essa componente cresce +2,37 ha**, magnitude
comparável ao crescimento da própria Mancha W (+3,47 ha). Isso não é estrutural.

Consequência: **o declínio de 2025-26 não está confinado à Mancha W e à Zona 0.**
Há uma terceira componente, difusa, de grandeza comparável. O caso tem sido
contado como "dois focos" e isso subestima a extensão. Reformular.

Nota sobre a auditoria adversarial: o árbitro suspeitou de excesso na
"selectividade" por saturação do NDVI. O teste (a) defendeu a selectividade pela
via térmica. Este achado dá-lhe razão por outra via — **em NDVI, metade do
défice novo está fora das máscaras nomeadas.** A referência sã manteve-se plana;
o pomar, no conjunto, não.

## Qualidade das datas (deles)

- **2017-07-02**: excluir. O desvio-padrão da referência é 0,111, cinco vezes o
  das outras datas (0,014–0,040) — neblina ou sombra. Já estava assinalado como
  "instalação"; passa a ter também um problema radiométrico.
- **2025-06-17**: assinalar. É de Junho, fora da janela das restantes.

## Ambiguidades inertes (verificadas, sem efeito)

NaN nas máscaras (os únicos estão fora), percentagem sobre totais vs válidos,
forma do elemento 2×2, conectividade no b1, tipo de percentil.
