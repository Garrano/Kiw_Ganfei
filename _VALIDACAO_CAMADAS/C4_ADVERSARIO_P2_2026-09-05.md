# Controlo 4 · P2 — as onze cenas eram as onze erradas

**Data:** 05-09-2026 · **Alvo:** `p2_onze_cenas.py` + `.json`
**Instrumentos:** portão (`guarda.py`, nove condições) + adversário independente
em sessão separada, sem conhecer a minha leitura.
**Veredicto: o P2 não responde à pergunta que foi escrito para responder, e não
podia ter respondido. `AF-07` mantém-se PRETENDIDA. A frase da `LISTA_FINAL`
§F — «não se pode escrever *um acontecimento*» — fica como está.**

Primeiro Controlo 4. Abriu-se porque a medição de 05-09 mostrou 29 guiões
pós-encerramento fora de qualquer verificação, e o P2 era um deles.

---

## 1 · O achado, e está numa linha de código

```python
ALVO = sorted({c["data"] for c in CENAS if 182 <= c["doy"] <= 244})
```

Esta linha faz **duas** coisas que ninguém verificou.

**O filtro de dia-do-ano proíbe, por construção, qualquer observação dentro do
vão.** A janela sob teste vai de 2025-08-15 a 2026-07-26. A intersecção dessa
janela com o dia-do-ano 182–244 é, e só pode ser, o fim de Agosto de 2025 e
Julho de 2026. **Nenhum resultado possível desta corrida podia seleccionar um
ramo da tabela de decisão.** O critério estava pré-registado — correctamente,
antes de correr — contra um conjunto de cenas que o tornava inalcançável.

**E é um conjunto de datas**, não de cenas: três das onze partilham data com
outra, e o `break` guarda uma por data. **Onze prometidas, oito descarregadas.**

O espaçamento medido:

| | |
|---|---|
| 2025-08-14 → 2025-08-26 | seis pontos em 12 dias |
| **2025-08-26 → 2026-07-02** | **310 dias, zero cenas** |
| 2026-07-02 → 2026-07-27 | quatro pontos em 25 dias |

O vão original era de 347 dias. Ficou em 310. **Encurtou 10,7 %.** As cenas
engrossaram as duas âncoras em vez de as ligar. A frase do adversário da C2 —
*«um degrau entre dois pontos a onze meses de distância é uma interpolação, não
uma medição»* — sobrevive textual, agora a dez meses e uma semana.

---

## 2 · E a resposta estava em disco o tempo todo

O `t2_cenas_descartadas.json` — que o próprio P2 abre — tem o inventário.
Verificado por mim:

```
total inventariado 199 · limpas (<20 % nuvem) 60
limpas DENTRO do vão 2025-09-01 a 2026-06-30: 49
por mês: 2025-09:7 · 10:7 · 11:1 · 12:5 · 2026-02:2 · 03:8 · 04:7 · 05:4 · 06:8
Setembro de 2025: 09-05 (3,6 %) · 09-23 (0,1 %) · 09-25 (0,0 %) · 09-28 (12,8 %) · 09-30 (14,5 %)
```

**Quarenta e nove cenas limpas dentro do vão. O estudo descarregou oito, e todas
caíram fora dele.** Sete só em Setembro de 2025, a quatro e vinte e nove dias do
corte dos 244, uma delas com **0,0 %** de nuvem.

O `ENCERRAMENTO` §5 diz que o número de acontecimentos «é respondível hoje com
onze cenas já inventariadas». **Continua a ser respondível. Eram as onze
erradas, e as quarenta e nove estão na prateleira.**

---

## 3 · O portão — o que passa e o que não

Corrido por mim antes do adversário, e ele repetiu-o em separado com o mesmo
resultado.

| | condição | P2 |
|---|---|---|
| 1 | instrumento declarado | cumpre |
| **2** | **mesmo índice** | **FALHA — e é a falha central** |
| 3 | confirmador discorda | n/a — não há confirmador |
| 4 | prova com ficheiro | cumpre |
| 5 | sem instrumento independente | **FALHA como escrito** |
| 6 | âncoras discriminam | **passa por omissão** — `ancoras()` nunca é chamado |
| 7 | reproduz o certificado | cumpre — o adversário reproduziu as duas linhas a **0,00e+00** |
| 8 | fronteira derivada do sinal | **cumpre, atacado e aguentou** |
| **9** | **identidade da unidade no tempo** | passa, mas por acidente de nomes |

**A condição 2 é onde isto morre como contribuição.** O facto foi produzido por
NDVI Sentinel-2. O contributo do P2 são **oito cenas de NDVI Sentinel-2 a mais**
— mesma família de sensor, mesmo catálogo, mesmo produto, mesmas máscaras, mesma
AOI, mesma mão. Não é confirmação: é **densificação do instrumento que já era a
única testemunha.** Fui verificar o que existiria: o SAR pára no inverno de
2024-25, o Landsat é outro NDVI, a ortofoto é data única.

A saída correcta, e a única que o portão autoriza:

```
Facto("numero de acontecimentos na janela 2025-26", instrumento="NDVI Sentinel-2")
  .nao_testavel("nenhum instrumento independente cobre Ago-2025 a Jul-2026")
  .identidade_no_tempo(triagem_referencia_densa.json,
                       nota=["foco OCIDENTAL", "foco ORIENTAL", "resto do pomar"])
  -> VEREDICTO AUTORIZADO
```

**Duas correcções minhas, ambas apanhadas pelo portão.** Passei o SAR como
confirmador com ficheiro e ele recusou: exige `chave`, um termo que tenha de
aparecer no conteúdo da prova — a quinta encarnação de «ausência tratada como
aprovação», fechada a 04-09. E escrevi que o rastreio não cobria as unidades do
P2: **cobre**, sob `foco OCIDENTAL` / `foco ORIENTAL` / `resto do pomar`. Eu é
que usei os nomes errados.

Sobre a condição 9, o adversário viu mais fundo do que eu: ela passa, mas o
passe é oco. As três unidades do P2 são definidas por `COM = chm_altura ≥ 0,5`,
de um voo LiDAR de **2025-07-06** — 38 dias antes da primeira âncora e dentro da
janela do acontecimento. É a maior condição aberta do processo, e **o P2 nunca
menciona o CHM, nem a data do voo, nem que ela está a montante de todos os
números que imprime.**

---

## 4 · O que o disco diz e o P2 não olhou

Na mesma pasta que o P2 lê está `2025-06-17.tif` — verifiquei, existe, e o P2
não o abre. Recomputado pelo adversário com as máscaras do próprio P2:

| | contraste OC |
|---|---|
| 2024-07-22 | **+0,005** |
| **2025-06-17** | **−0,061** |
| aglomerado Ago-2025 | −0,050 |
| aglomerado Jul-2026 | −0,180 |

**A 17-06-2025 — dois meses antes de a janela abrir — o contraste já tinha caído
0,066**, cerca de metade dos 0,130 que o P2 atribui à janela. A leitura que os
dados em disco sustentam é a de **duas descidas**, ambas por datar. A janela do
P2 está posicionada para não conter nenhuma.

---

## 5 · Erros de escrituração — e cinco são forma E

| | o cabeçalho diz | em disco |
|---|---|---|
| 1 | «onze cenas» | **8** — conjunto de datas colapsa três duplicadas |
| 2 | «treze pontos» | **10**, e dez era o máximo possível |
| 3 | «sete em Agosto e quatro em Julho» | 5 datas + 3 datas |
| 4 | «a plataforma de cada cena vai impressa» | **em branco nas duas âncoras** — e são as duas S2C, exactamente as que a ressalva existe para tornar auditáveis |
| 5 | «o mesmo processamento das nove da série» | caminho de código diferente: **sem máscara de nuvem por píxel, sem verificação do desvio BOA** |

O ponto 5 tem consequência medida. Sem máscara de nuvem, a correlação entre
fracção de nuvem e contraste é **+0,864** em Agosto de 2025 e **+0,986** em
Julho de 2026 — mesmo sinal nos dois aglomerados. Mais nuvem, contraste menos
negativo. É um artefacto do instrumento a operar exactamente sobre a grandeza
que o contraste devia proteger.

E o patamar de 2026 não é patamar: **move-se 0,099 em 23 dias dentro do próprio
aglomerado — 76 % do degrau inteiro que serve para estabelecer**, contra uma
dispersão de 0,005 no aglomerado de 2025. E está confundido: a cena de 02-07 tem
0,01 % de nuvem, a de 25-07 tem 19,2 %; nuvem e dia-do-ano sobem juntos nas três
cenas novas de 2026, e nenhuma cena do desenho os separa.

O JSON tem ainda dois defeitos de ficheiro: contém literais `NaN`, que **não são
JSON válido** (só o analisador não-estrito do Python os aceita), e foi escrito em
cp1252 com `ensure_ascii=False`, pelo que qualquer leitor utf-8 apanha mojibake.
E não traz carimbo de produtor — cláusula S2.

---

## 6 · O que aguentou, e é preciso dizê-lo

O adversário atacou e não partiu:

- **As máscaras não derivam do sinal medido.** As geográficas vêm de ortofoto
  DGT, com vértices declarados; a `manchaW := pomar & (nd2026 < 0,76)` está
  marcada RETIRADA e o P2 não a carrega. `COM` vem do LiDAR. Condição 8 por
  mérito.
- **As unidades são geometricamente disjuntas** — zero píxeis partilhados,
  controlo a ≥ 90 m dos dois focos.
- **A cancelação de plataforma funciona.** S2C menos S2A, em datas adjacentes,
  dá 0,003 no contraste ocidental e 0,0001 no oriental, contra um degrau de
  0,130. **O S2C não explica o degrau.**
- **A fenologia é real e pequena, e aponta ao contrário:** o desvio de 38 dias
  entre aglomerados prevê +0,009, contra −0,130 observados. O degrau
  não-corrigido é, se alguma coisa, conservador.
- **Média contra mediana não inverte nada.**
- **O pré-registo foi genuinamente feito antes de correr**, em prosa
  falsificável. O defeito não é má-fé: é que a C9 não foi honrada — ninguém leu
  a linha 76 contra a tabela — e a C1 não foi calculada.

**O degrau Ago-2025 → Jul-2026 é real nestes dados** e não se explica por
plataforma, fenologia nem estimador. O que não está estabelecido é **quantos
acontecimentos** o produziram, e onde caem.

---

## 7 · O que fica

1. **`AF-07` mantém-se PRETENDIDA.** A fonte não é citável e a cadeia di-lo em
   cada corrida.
2. **A `LISTA_FINAL` §F não muda.** «*Um* acontecimento» continua por escrever.
3. **Acção nova, e é a que vale:** correr as **49 cenas limpas dentro do vão**,
   com máscara de nuvem por píxel, sem o filtro de dia-do-ano, e incluindo
   `2025-06-17`. Custo: descarregar 49 cenas. Decide o que o P2 não decidiu.
4. **O cabeçalho do P2 leva cartucho de correcção** — «onze cenas» e «treze
   pontos» são falsos e liam-se como facto.

## 8 · A lição do primeiro Controlo 4

O P2 tinha tudo o que este processo aprendeu a exigir: pergunta fixa, tabela de
decisão de três ramos escrita antes de correr, ressalva de plataforma, grandeza
certificada em vez de nível absoluto. **E mesmo assim não podia falhar nem
acertar**, porque ninguém calculou o que o filtro herdado deixava dentro da
janela — uma linha de aritmética, sobre um ficheiro que o guião já abre.

A C9 diz que o adversário vê o critério **antes** da corrida. É a cláusula que
teria apanhado isto, e continua em prosa.
