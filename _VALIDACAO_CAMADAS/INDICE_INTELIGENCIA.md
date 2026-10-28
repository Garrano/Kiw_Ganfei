# ÍNDICE DA INTELIGÊNCIA — o que foi medido, e se está certificado

**Gerado por `indice_inteligencia.py`.** Não editar à mão: corre outra vez.

| | |
|---|---|
| guiões que emitem resultado | **198** |
| vivos (não retirados) | **196** |
| **citáveis — passaram pelas DUAS** | **45** |
| no registo dos factos vivos | 15 |
| nomeados por um adversário | 94 |

## Auditorias já feitas — não repetir sem razão nova escrita

| id | data | alvo | veredicto | o que sobreviveu |
|---|---|---|---|---|
| AUD-01 | 2026-08-29 | Camada 4 · terreno e halo | **PARCIAL** | placebo do chao retirado (91% do sinal); nulo toroidal mantido |
| AUD-02 | 2026-08-31 | Controlo 3 · Camada 2 | **PARCIAL** | T5 e identidade algebrica; degrau mantido |
| AUD-03 | 2026-09-01 | REG-01 · replicacao Landsat | **RETIRADO** | conclusao invertida: comparador desmatado em 2024 |
| AUD-04 | 2026-09-03 | Controlo 3 · B1 | **PARCIAL** | enumeracao das 6 parcelas certa; so 4 passam a guarda de cobertura |
| AUD-05 | 2026-09-05 | C3 · clausula da ficha de fuga | **RETIRADO** | desenho conceptual sobrevive; implementacao retirada no mesmo dia |
| AUD-06 | 2026-09-05 | Controlo 4 · P2 as onze cenas | **NAO_DECIDE** | degrau real; numero de acontecimentos nao determinavel |
| AUD-07 | 2026-09-05 | Controlo 4 · P8 as 49 cenas do vao | **PARCIAL** | mascara de nuvem funcionou (r -0.17); regra de classificacao retirada |
| AUD-08 | 2026-09-06 | pre-registo SAR Out-Abr (C9 antes da corrida) | **REDESENHADO** | MDE errado 2.5-5.7x; janela de inverno herdada sem interrogacao |
| AUD-09 | 2026-09-06 | lote de Verao · familia das mascaras | **PARCIAL** | saudavel LIMPA (percentil 34-91 no universo certo, recuo de 30 m exacto, zero celulas de 2025); contagens reconciliam todas; pomar 22,3 % definido por ortofoto POSTERIOR; zona0 sem produtor em codigo |
| AUD-10 | 2026-09-06 | lote de Verao · cadeia serie/fenologia/defice | **PARCIAL** | c2_01/02/03 e c1_14 reproduzem o disco exactamente; SONDA A tinha potencia e passou; foco ORIENTAL limpo (poligono fixo); MAS o centro do foco OCIDENTAL esta no percentil 0,17 de 2421 candidatos - magnitude ocidental nao estimavel; dAICc sub-penalizado 2,40; as 43 corridas sao 1 bit (p=1/36); erro de +-0,02-0,03 nao rastreavel |
| AUD-11 | 2026-09-06 | C9 · criterio de leitura do SAR, ANTES da corrida | **REDESENHADO** | nove correccoes aplicadas antes de ler: zona0 e 87 % o este e 45 % o nu2021; polarizacao por declarar mudava o MDE do verao a dobrar; orbitas correlacionadas r=+0,90 logo MDE do P1 subestimado 1,36x; celula DECLINIO inalcancavel (tecto 1,02 dB contra limiar 0,98); faltava linha para SUBIU e para modo comum; janela do P2 admitia 45 % de concordancias vazias; sanidade do P4 comparava modulos de sinais opostos. AGUENTOU: potencia por estacao robusta a 7 divisoes, portao do controlo nao auto-sabotavel, restricao S1A custa 2 %, nulo temporal 0/10 falsos positivos em VV |
| AUD-12 | 2026-09-06 | C9 · passe confirmatorio sobre o v2 do criterio do SAR | **NAO_APTO** | tres defeitos BLOQUEANTES, todos introduzidos pelas proprias correccoes: §8.3 e §8.4 contradizem-se e o P3 nao tem limiar para a serie que manda ler; o §8.7 cita evidencia do estimador que abole no mesmo paragrafo e sob a especificacao declarada a porta falha p=0,269/0,965; nivel-vs-contraste por declarar e na forma de contraste o chao nu le como encharcamento. AGUENTOU: a escolha do VV (mas a frase que a justifica exagera -- o VH ve o copado em todas as estacoes, so nao o ve modular); a media das orbitas (mas por razao diferente da que escrevi -- nao ha ganho de variancia com r=0,90) |
| AUD-13 | 2026-09-06 | hipotese de leitura minima do SAR + a conjectura que a sustenta | **REFUTADA** | CONJECTURA REFUTADA 3 de 3: os tres bloqueantes do v2 RECORREM na leitura minima. O defeito nao e elaboracao, e especificacao incompleta, e essa e independente do tamanho do desenho. O posto empirico e INVALIDO -- ACF(1) +0,23 e +0,43 quebram a permutabilidade, e sobre o CONTROLO a regra atinge o extremo em 31 de 72 especificacoes defensaveis. O comparador resto move-se 0,87 dB contra 0,91 da referencia -- o criterio que expulsa uma expulsa a outra -- e esta ele proprio no POSTO 11 de 11 no ano a testar. AGUENTOU: VV, S1A, o dedup, o ano hidrologico. A PARTE VERDADEIRA da conjectura: as constantes DERIVADAS de medicao aguentaram todas; as ASSERIDAS partiram todas |
| AUD-14 | 2026-09-06 | criterio v3 do SAR, escrito contra as sete alteracoes | **APTO_COM_ADENDA** | O adversario deu-o por SUBSTANCIALMENTE MELHOR que os tres anteriores e mandou NAO reescrever: fecha os tres bloqueantes da v2, fecha o posto invalido, fecha o comparador unico, e o §0 e achado real que o autor publicou contra o proprio interesse. Prescreveu QUATRO linhas de adenda e autorizou a leitura depois delas. Apanhou ainda: a armadilha de plataforma que esvaziava o ano de tratamento em silencio (IX-09), o MDE do portao com o ano de tratamento no proprio nulo, o mecanismo errado do §0 (IX-10), o tecto contaminado (IX-11), e o IX-02 mal diagnosticado por mim |
| AUD-15 | 2026-09-06 | LEITURA do SAR contra o v3 + adenda | **CONFIRMADO_COM_CORRECCOES** | O NULO REPRODUZ AO ULTIMO DIGITO -- doze Delta, doze MDE, portao e modo comum, zero discrepancias -- e o adversario confirma que e REAL e nao fabricado (contagens de celulas constantes nos onze anos, zero NaN, e o S1C concorda a 0,26 dB). MAS: eu subestimei o achado. O tecto certo e o contraste de copado DE INVERNO (zona0-nu2021: +0,48 e +0,99), nao a amplitude sazonal, e contra ele o MDE excede o tecto nas SEIS celulas por 1,55 a 2,57x. E a zona0 esta AO NIVEL DO CHAO NU no ano de tratamento, deslocamento de 104-106 porcento do tecto, confirmado em S1C -- e abaixo do MDE. A leitura honesta: o instrumento e compativel com a perda TOTAL e com nada, e nao os distingue. Quatro defeitos no codigo corrigidos (o portao de abortar nao podia abortar; portao e modo comum numa base so; o posto suprimido no ecra e escrito no JSON; niveis absolutos em falta). Tres frases corrigidas. A rota do SAR NAO esta fechada -- esta fechada para esta unidade |
| AUD-16 | 2026-09-06 | criterio P3 · declinio contra arranque em VH de inverno | **REFUTADO_ANTES_DE_CORRER** | Aritmetica toda reproduzida a 3 decimais. MAS a premissa fisica falha: o fosso resto-nu2021 mexe-se 0,887 dB DENTRO da estacao sem folha (90 % do MDE) -- mede cobertura do solo, nao estrutura. O tecto certo mede-se directo e ja tem a diluicao: zona0-nu2021 = +1,164 e nao +2,302, logo o racio cai de 2,3x para 1,12x com P(racio<1)=0,17. A celula falha o MEU proprio criterio de admissao (0,32 sd contra 1,8). E o modo comum dispara em VH orb147 a +0,841 = 72 porcento do alcance: o veredicto esta decidido antes de correr. RECOMENDACAO DELE, aceite: certificar e atacar o altura_copado (LiDAR, instrumento genuinamente independente, fecha a condicao 2) e o piso_inverno (piso optico de inverno, mesma logica sem folha com ordens de grandeza mais contraste) -- os dois ja correram e nunca foram certificados nem atacados. Forma H. |
| AUD-17 | 2026-09-06 | os dois instrumentos que ja tinham corrido e nunca foram atacados | **PARCIAL** | O LiDAR AGUENTA-SE: reproduzido dos ladrilhos brutos a 0,000e+00, datado 06-07-2025 sobre 100 porcento das celulas, ancoras que discriminam melhor depois de limpas, e a correlacao com o NDVI ordena-se pelo tempo. FECHA A CONDICAO 2 para factos instantaneos -- o que o SAR nao fez. MAS nao responde a pergunta: uma pergola nua move a estatistica 0,018 contra sd 0,135, sete vezes abaixo; mede FOLHA, nao estrutura, e nao separa instalacao removida de instalacao de pe com planta morta. ACHADO NOVO E VERIFICADO POR MIM: os 3,77 ha sem pergola decompoem-se em 1,57 que NUNCA teve copado e 2,20 que tinha copado em Jul-2024 (NDVI 0,829 contra 0,898 do pomar) e nao tinha nenhum em Jul-2025 -- perda datada por geometria, ANTERIOR a janela do declinio ocidental. PISO DE INVERNO: a medicao sobrevive ao modo comum (N3 a 2,35x o MDE, cinco cenas consecutivas), mas a inferencia nao -- a premissa nao discrimina (pergola sem copado deixa de dar sombra e a erva fica verde) e o sinal NAO PERSISTE (+0,291 para -0,078). Os dois enquadram a mesma perda entre 27-12-2024 e 16-01-2025, de lados opostos. AF-06 mantem-se pretendida: as ancoras do p1 nao separam em 2025 |
| AUD-18 | 2026-09-06 | testemunho do gestor -- tipo 1 | **TIPO_1** | Nao passa por adversario: testemunho de tipo 1 nao se certifica com o guarda.py nem se ataca -- certifica-se dizendo QUEM e QUANDO, e corrige-se perguntando outra vez. Derruba: o nome da mascara zona0 (esta no foco oriental, a 516 m da Zona 0 real), e o B1 como comparador (cortado a base e reenxertado DUAS vezes, 2016 e ~2020). Fixa a tabela de valvulas por sector que estava aberta desde 04-09. E fixa o estatuto da Phytophthora: nunca confirmada por laboratorio de diagnostico |
| AUD-19 | 2026-09-06 | escala do esquema de rega -- adversario independente | **SOBREVIVE_COM_CORRECCOES** | SOBREVIVE a afirmacao central: o desenho ESTA a escala declarada 1:3500 @ A1, e o erro era nosso. O adversario tentou parti-la por quatro vias e falhou nas quatro. A matriz do XObject e 841,680 x 595,440 pt = 11,69 x 8,27 polegadas EXACTAS, logo 200,0000 dpi nos dois eixos -- o dpi nao e inferido do tamanho da pagina. MediaBox = CropBox = ArtBox, sem UserUnit. Cartucho lido a 5x: ESC 1/3500 @ A1. md5 do fluxo embebido = md5 do scan.jpeg, diferenca de pixel zero. E o calibre do adversario contra o parcelario IFAP da 1,2680 m/px, +0,9 % da declarada -- terceira medicao independente dentro de +-1,1 %. As unidades do 0,788 e do 0,6734 SAO comparaveis (0,788 reproduz-se como 0,7773 a 400 dpi), logo os +25,4 % e +7,1 % valem. || PARTE: (1) o diagnostico da causa estava errado -- nao foi o nome do campo, foi a ancora cobrir so 80,5 % do talhao; corrigido. (2) o teste cego da corrida 2 nunca viu o lobo: comps[0] e comps[1] eram as duas metades do corpo, e o cabecalho dizia o contrario do codigo; georref_rega.json RETIRADO para _superseded. (3) o metodo executado nao era o pre-registado -- ICP de contornos sem um unico ponto de controlo, logo os criterios B, D e E ficaram inaplicaveis e o TOL_ESCALA nunca foi usado. (4) o escala_rega.py disparou dois dos seus tres falsificadores e imprimiu veredicto positivo na mesma, e o 5 de 5 era circular. (5) a frase e so aritmetica traz uma hipotese fisica nao verificada: a moldura medida da razao 1,4331 e a banda vai de -0,4 % a +5,6 %. (6) o PDF tem 35 anotacoes vectoriais invisiveis ao scan.jpeg, com areas declaradas 1,77 ha e 1 ha VIVEIRO -> IX-23. (7) contradicao aberta de 24 % no valvulas_por_linha -> IX-24. || O criterio A nunca foi avaliado: as duas corridas cairam em pre-condicao. A afirmacao central vive do cartucho e das tres medicoes, NAO deste exercicio |
| AUD-20 | 2026-09-10 | pontos_de_colheita -- 12 pontos de margem em avanco + pares | **SOBREVIVE_COM_DUAS_CONDICOES** | SOBREVIVE com duas condicoes antes de alguem viajar. O adversario recomputou a correccao de 10-09 A PARTIR DOS DADOS BRUTOS: 346 celulas contra 199, zero em comum, 2,05 m contra 0,11 m -- confirma o IX-25. Testou uma TERCEIRA definicao (faixa de dois aneis): 323 celulas, 2,29 m, nao qualitativamente diferente -- nao ha definicao melhor escondida. || A pergunta central (ha planta viva nos 12 pontos?) foi respondida por DUAS vias que NAO passam pelo chm_altura.npy: (1) ladrilhos LiDAR brutos MDS-MDT em janela 10x10 m -- 1,03 a 2,38 m de altura media, 42 a 100 % da celula acima de 0,5 m; (2) NDVI Sentinel-2 de 2026-07-27, seis semanas atras -- 0,585 a 0,845 nos doze, todos acima da referencia de solo nu. || Os PARES controlam: em 2024 margem e par sao indistinguiveis (+-0,01 a 0,03 em 10 de 12); em 2026 dez dos doze divergem no sentido certo (par mais verde, +0,03 a +0,12). M1-2 e M3-2 ainda nao divergem -- controlos mais fracos, nao invalidos. || Geometria limpa: as 19 distancias par-a-par todas >= 40,0 m; sector do par confirmado por amostragem independente nos 12; cota do par sempre dentro de +-0,31 m contra tolerancia de 1,0 m; UTM->WGS84 ida-e-volta a 0,0 mm; alinhamento de grelha 100 % de concordancia -- nao ha problema de meio-pixel. Tres corridas bit-a-bit identicas. || PARTE: (1) VIES DE ORDENACAO nao documentado -> IX-27; (2) uma mancha de 0,07 ha, 100 % em B2, a 57 m de M2, excluida so por MIN_CELULAS=8 -- unica exclusao que nao e ruido de bordo; (3) a ortofoto 2025 sem folha NAO decide arranque-contra-declinio em M1 e quase enganou o adversario: a textura le como solo lavrado, que e o confundimento ja documentado no AUD-17 §6 (sulco ~ fiada sem folha, prominencia 0,240). Resolvido pelas outras duas vias. || NAO TESTAVEL: altura que baixou entre datas (so ha um voo LiDAR); se a planta esta viva-MAS-SINTOMATICA (nenhum instrumento remoto o faz); qual das tres manchas cresce mais depressa AGORA (a serie temporal de manchas foi RETIRADA por circularidade) |

## Por estação — e é aqui que a assimetria aparece

| estação | guiões vivos | citáveis | fracção |
|---|---|---|---|
| **Primavera/Verão** | 77 | 25 | 32 % |
| **Inverno** | 9 | 1 | 11 % |
| **ambas** | 13 | 5 | 38 % |
| **ano inteiro** | 9 | 5 | 56 % |
| **?** | 88 | 9 | 10 % |

## Por instrumento

| instrumento | vivos | citáveis |
|---|---|---|
| NDVI S2 | 34 | 7 |
| — | 33 | 3 |
| LiDAR | 18 | 5 |
| ortofoto | 14 | 0 |
| NDVI S2 · ortofoto | 13 | 4 |
| IFAP | 9 | 3 |
| NDVI S2 · LiDAR | 9 | 4 |
| LiDAR · ortofoto | 7 | 2 |
| NDVI S2 · LiDAR · ortofoto | 6 | 4 |
| NDVI S2 · Landsat | 5 | 0 |

## Os citáveis — passaram pelo portão E por adversário

| guião | facto | estação | instrumento |
|---|---|---|---|
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_03_proveniencia.py` | — | ano inteiro | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_12_ajuste_esquema.py` | — | Primavera/Verão | — |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_13_georref.py` | — | ? | — |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_04_focos_terreno.py` | — | ? | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_10_nivelamento.py` | — | ? | LiDAR · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_04_referencia.py` | — | Primavera/Verão | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_05_manchas.py` | — | Primavera/Verão | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_06_este_plantado.py` | — | Primavera/Verão | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_08_cruzamento.py` | — | ambas | SAR S1 · NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_09_sar_verificacao.py` | — | ambas | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_12_pergola_2012.py` | — | Primavera/Verão | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_13_coberto_2025.py` | — | Primavera/Verão | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_07_georreferenciar.py` | — | Primavera/Verão | LiDAR · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_09_organismos_contra_padrao.py` | — | ? | — |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_10_esforco_its_becrop.py` | — | ambas | IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C4/c4_01_numeros.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C4/c4_02_razao.py` | — | ambas | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C4/c4_r2_01_multiverso_das_valvulas.py` | — | Primavera/Verão | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C5/c5_01_reetiquetagem.py` | — | ambas | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C5/c5_02_amostragem.py` | — | Primavera/Verão | NDVI S2 · ortofoto · IFAP |
| `_VALIDADE_GESTAO/altura_copado.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `_VALIDADE_GESTAO/amplitude.py` | — | ano inteiro | NDVI S2 |
| `_VALIDADE_GESTAO/emparelhar_moedas.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `_VALIDADE_GESTAO/landsat_independente.py` | — | ano inteiro | NDVI S2 · Landsat · LiDAR |
| `_VALIDADE_GESTAO/paisagem.py` | — | ? | NDVI S2 · LiDAR · IFAP |
| `_VALIDADE_GESTAO/refazer_c2_este.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `_VALIDADE_GESTAO/serie_separada.py` | — | Primavera/Verão | NDVI S2 · LiDAR |
| `_VALIDADE_GESTAO/terreno_contra_declinio.py` | — | Primavera/Verão | NDVI S2 · Landsat · LiDAR |
| `_VALIDADE_GESTAO/triagem_referencia_densa.py` | — | ano inteiro | NDVI S2 · LiDAR |
| `ganfei_s2/fazer_masks_v2.py` | — | Primavera/Verão | NDVI S2 · ortofoto |
| `_VALIDADE_GESTAO/serie_oriental_pergola.py` | A1 | Primavera/Verão | LiDAR · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_09_sar.py` | A2 | Inverno | SAR S1 · NDVI S2 |
| `_VALIDADE_GESTAO/reg01_triagem_descontinuidade.py` | A3 | Primavera/Verão | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `_VALIDADE_GESTAO/multiverso_degrau.py` | B1 | Primavera/Verão | NDVI S2 · LiDAR · IFAP |
| `_VALIDADE_GESTAO/degrau_vs_recta_pergola.py` | B2 | Primavera/Verão | LiDAR |
| `_VALIDADE_GESTAO/satelites_degrau.py` | B3 | Primavera/Verão | LiDAR |
| `_VALIDADE_GESTAO/satelites_sem_2026.py` | B4 | Primavera/Verão | NDVI S2 · LiDAR · IFAP |
| `_VALIDADE_GESTAO/fenologia_por_unidade.py` | B5 | Primavera/Verão | NDVI S2 · LiDAR |
| `_VALIDADE_GESTAO/halo_distancia.py` | B7 | Primavera/Verão | NDVI S2 · LiDAR |
| `_VALIDADE_GESTAO/l1_data_do_voo.py` | C1 | ano inteiro | LiDAR |
| `_VALIDADE_GESTAO/g19_parcelario.py` | C3 | ? | IFAP |
| `_VALIDADE_GESTAO/lobulo_oeste_degrau.py` | C7 | ? | NDVI S2 · LiDAR · ortofoto |
| `_VALIDADE_GESTAO/valvulas_1a5_o_troco_que_falta.py` | C8 | Primavera/Verão | IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_03_mdt.py` | C9 | ? | LiDAR |
| `_VALIDADE_GESTAO/a2_solo_caracterizacao.py` | D9 | ? | NDVI S2 |

## Os NÃO citáveis que emitem resultado — por estação

### Primavera/Verão — 52 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDADE_GESTAO/assinatura_espectral.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat · LiDAR · IFAP |
| `ganfei_s2/audit_termico.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat |
| `ganfei_s2/_pacote_cowork/audit_termico.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat |
| `ganfei_s2/b1_analise.py` | falta auditoria independente | NDVI S2 |
| `_VALIDADE_GESTAO/b1_como_unidade.py` | falta certificacao | NDVI S2 · Landsat · ortofoto · IFAP |
| `_VALIDADE_GESTAO/b1_contra_corpo.py` | falta certificacao e auditoria independente | NDVI S2 · LiDAR · IFAP |
| `ganfei_s2/b1_nucleo_interno.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/_pacote_cowork/b1_nucleo_interno.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/b1_serie_verdadeira.py` | falta certificacao | NDVI S2 · ortofoto |
| `ganfei_s2/b1_serie_verdadeira.py` | falta certificacao | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/b1_subblocos.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `ganfei_s2/b1_subblocos.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `_VALIDADE_GESTAO/b1_terreno.py` | falta certificacao | LiDAR · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_02_mascaras.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_11_assuncoes.py` | falta auditoria independente | NDVI S2 · LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_02_costura.py` | falta auditoria independente | LiDAR · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_14_ancoras.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_01_serie.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_02_fenologia.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_03_defice.py` | falta auditoria independente | NDVI S2 |
| `_VALIDADE_GESTAO/_controlo3/c3_06_unidade.py` | falta certificacao | NDVI S2 · Landsat · LiDAR |
| `_VALIDADE_GESTAO/_controlo3/c3_07_mascara_pre.py` | falta certificacao | NDVI S2 · Landsat · LiDAR · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_08_controlo_referencia.py` | falta auditoria independente | — |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_13_T2_T4.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_r2_01_amostras_contra_pergola.py` | falta auditoria independente | LiDAR |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_05_veredicto.py` | falta certificacao | IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C0/ctrl_14_metricas.py` | falta auditoria independente | NDVI S2 · LiDAR · ortofoto |
| `_VALIDADE_GESTAO/degrau_robustez.py` | falta certificacao e auditoria independente | LiDAR |
| `ganfei_s2/difusa.py` | falta certificacao e auditoria independente | NDVI S2 |
| `ganfei_s2/_pacote_cowork/difusa.py` | falta certificacao e auditoria independente | NDVI S2 |
| `ganfei_s2/exportar_auditoria.py` | falta certificacao e auditoria independente | NDVI S2 · LiDAR |
| `ganfei_s2/fazer_masks.py` | falta certificacao | NDVI S2 |
| `ganfei_s2/filtro_w.py` | falta certificacao e auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_MASCARAS/g16_serie.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_MASCARAS/g18_final.py` | falta certificacao | NDVI S2 · ortofoto |
| `_VALIDADE_GESTAO/ifap_cruzamento.py` | falta certificacao | LiDAR · IFAP |
| `ganfei_s2/figuras/m2_declinio.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/metricas.py` | falta auditoria independente | NDVI S2 |
| `_VALIDADE_GESTAO/ocidental_independente.py` | falta certificacao e auditoria independente | NDVI S2 · LiDAR · IFAP |
| `_VALIDADE_GESTAO/orto_297313.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| … e mais 12 | | |

### Inverno — 8 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_12_sar_lavrado.py` | falta auditoria independente | SAR S1 |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_13_sar_antes_depois.py` | falta auditoria independente | SAR S1 · NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_07_sar_pilha.py` | falta auditoria independente | SAR S1 · NDVI S2 |
| `ganfei_s2/exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `ganfei_s2/_pacote_cowork/exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `_VALIDADE_GESTAO/piso_inverno.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/sar_invernos.py` | falta certificacao | SAR S1 |
| `_VALIDADE_GESTAO/sar_v3.py` | falta certificacao e auditoria independente | SAR S1 |

### ambas — 8 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_06_solo_no_mapa.py` | falta auditoria independente | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_08_clima.py` | falta auditoria independente | — |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_10_ancoras.py` | falta auditoria independente | SAR S1 · NDVI S2 |
| `_VALIDADE_GESTAO/_controlo3_a2/c3a2_05_multiplicidade.py` | falta certificacao | — |
| `ganfei_s2/exportar_pendentes.py` | falta certificacao e auditoria independente | NDVI S2 |
| `ganfei_s2/_pacote_cowork/exportar_pendentes.py` | falta certificacao e auditoria independente | NDVI S2 |
| `ganfei_s2/fenologia.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/_pacote_cowork/fenologia.py` | falta auditoria independente | NDVI S2 |

### ano inteiro — 4 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_07_termico.py` | falta auditoria independente | NDVI S2 · Landsat |
| `_VALIDADE_GESTAO/reg01_landsat.py` | falta certificacao | NDVI S2 · Landsat · IFAP |
| `_VALIDADE_GESTAO/sar_ano_inteiro.py` | falta certificacao e auditoria independente | SAR S1 · NDVI S2 |
| `ganfei_s2/serie_densa_descontinuidades.py` | falta certificacao e auditoria independente | NDVI S2 |

### ? — 79 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDACAO_CAMADAS/b1_divisao.py` | falta certificacao | ortofoto |
| `ganfei_s2/b1_divisao.py` | falta certificacao | ortofoto |
| `ganfei_s2/b1_serie.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/bacia.py` | falta auditoria independente | LiDAR · ortofoto |
| `ganfei_s2/bacia2.py` | falta auditoria independente | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_01_rasters.py` | falta auditoria independente | NDVI S2 |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_05_orto.py` | falta auditoria independente | ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C0/c0_10_quarentena_b1.py` | falta auditoria independente | NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_01_lidar_inventario.py` | falta auditoria independente | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_05_bacia.py` | falta auditoria independente | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_11_escalas.py` | falta auditoria independente | LiDAR |
| `_VALIDADE_GESTAO/c1ab_contra_kiwi_ifap.py` | falta certificacao e auditoria independente | ortofoto · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_00_inventario.py` | falta certificacao e auditoria independente | LiDAR |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_01_reconciliar.py` | falta certificacao e auditoria independente | IFAP |
| `_VALIDADE_GESTAO/_controlo3/c3_01_triagem_sensibilidade.py` | falta certificacao | — |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_02_desalinhamento.py` | falta certificacao e auditoria independente | — |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_03_alinhamento.py` | falta auditoria independente | — |
| `_VALIDADE_GESTAO/_controlo3/c3_03_margem.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3/c3_04_anos_e_donos.py` | falta certificacao | — |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_04_perfil_registos.py` | falta certificacao e auditoria independente | IFAP |
| `_VALIDADE_GESTAO/_controlo3/c3_08_orto_tres.py` | falta certificacao | Landsat · ortofoto · IFAP |
| `_VALIDACAO_CAMADAS/SAIDA_C3/c3_11_par_contraste_e_ancoras.py` | falta certificacao | LiDAR |
| `_VALIDADE_GESTAO/_controlo3_a2/c3a2_02_matriz.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_a2/c3a2_03_q1_probabilidade.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_a2/c3a2_04_q5_doze.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_01_geometria.py` | falta certificacao | NDVI S2 · ortofoto · IFAP |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_02_saturacao.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_03_estabelecimento.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_04_concordancia.py` | falta certificacao | NDVI S2 · Landsat · ortofoto · IFAP |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_05_multiverso.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_08_cronometro.py` | falta certificacao | NDVI S2 · Landsat |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_09_orto.py` | falta certificacao | NDVI S2 · Landsat · ortofoto |
| `_VALIDADE_GESTAO/_controlo3_b1/c3b1_10_veredicto.py` | falta certificacao | ortofoto |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_01_extrai.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_03_tinta.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_04_sectores.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_06_extrapolacoes.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_07_contiguidade.py` | falta certificacao | — |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_08_o_177.py` | falta certificacao | ortofoto · IFAP |
| `_VALIDADE_GESTAO/_controlo3_c8/c8_09_tres_enumeracoes.py` | falta certificacao | — |
| … e mais 39 | | |

