# ÍNDICE DA INTELIGÊNCIA — o que foi medido, e se está certificado

**Gerado por `indice_inteligencia.py`.** Não editar à mão: corre outra vez.

| | |
|---|---|
| guiões que emitem resultado | **190** |
| vivos (não retirados) | **188** |
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

## Por estação — e é aqui que a assimetria aparece

| estação | guiões vivos | citáveis | fracção |
|---|---|---|---|
| **Primavera/Verão** | 74 | 25 | 34 % |
| **Inverno** | 8 | 1 | 12 % |
| **ambas** | 13 | 5 | 38 % |
| **ano inteiro** | 9 | 5 | 56 % |
| **?** | 84 | 9 | 11 % |

## Por instrumento

| instrumento | vivos | citáveis |
|---|---|---|
| NDVI S2 | 33 | 8 |
| — | 31 | 3 |
| LiDAR | 16 | 5 |
| ortofoto | 14 | 0 |
| NDVI S2 · ortofoto | 12 | 3 |
| NDVI S2 · LiDAR | 9 | 4 |
| IFAP | 8 | 3 |
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
| `ganfei_s2/fazer_masks_v2.py` | — | Primavera/Verão | NDVI S2 |
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

### Primavera/Verão — 49 guiões

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
| … e mais 9 | | |

### Inverno — 7 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_12_sar_lavrado.py` | falta auditoria independente | SAR S1 |
| `_VALIDACAO_CAMADAS/SAIDA_C1/c1_13_sar_antes_depois.py` | falta auditoria independente | SAR S1 · NDVI S2 · ortofoto |
| `_VALIDACAO_CAMADAS/SAIDA_C2/c2_07_sar_pilha.py` | falta auditoria independente | SAR S1 · NDVI S2 |
| `ganfei_s2/exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `ganfei_s2/_pacote_cowork/exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `_VALIDADE_GESTAO/piso_inverno.py` | falta auditoria independente | NDVI S2 |
| `ganfei_s2/sar_invernos.py` | falta certificacao | SAR S1 |

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

### ? — 75 guiões

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
| … e mais 35 | | |

