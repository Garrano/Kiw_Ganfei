# ÍNDICE DA INTELIGÊNCIA — o que foi medido, e se está certificado

**Gerado por `indice_inteligencia.py`.** Não editar à mão: corre outra vez.

| | |
|---|---|
| guiões que emitem resultado | **199** |
| vivos (não retirados) | **197** |
| **citáveis — passaram pelas DUAS** | **46** |
| no registo dos factos vivos | 15 |
| nomeados por um adversário | 98 |

## Por estação — e é aqui que a assimetria aparece

| estação | guiões vivos | citáveis | fracção |
|---|---|---|---|
| **Primavera/Verão** | 79 | 26 | 33 % |
| **Inverno** | 8 | 1 | 12 % |
| **ambas** | 15 | 5 | 33 % |
| **ano inteiro** | 10 | 5 | 50 % |
| **?** | 85 | 9 | 11 % |

## Por instrumento

| instrumento | vivos | citáveis |
|---|---|---|
| — | 34 | 4 |
| NDVI S2 | 33 | 8 |
| LiDAR | 16 | 5 |
| ortofoto | 14 | 0 |
| NDVI S2 · ortofoto | 13 | 3 |
| NDVI S2 · LiDAR | 9 | 4 |
| LiDAR · ortofoto | 8 | 2 |
| IFAP | 8 | 3 |
| NDVI S2 · LiDAR · ortofoto | 6 | 4 |
| NDVI S2 · Landsat | 5 | 0 |

## Os citáveis — passaram pelo portão E por adversário

| guião | facto | estação | instrumento |
|---|---|---|---|
| `proveniencia.py` | — | Primavera/Verão | — |
| `c0_03_proveniencia.py` | — | ano inteiro | NDVI S2 |
| `c0_12_ajuste_esquema.py` | — | Primavera/Verão | — |
| `c0_13_georref.py` | — | ? | — |
| `c1_04_focos_terreno.py` | — | ? | NDVI S2 · ortofoto |
| `c1_10_nivelamento.py` | — | ? | LiDAR · ortofoto |
| `c2_04_referencia.py` | — | Primavera/Verão | NDVI S2 |
| `c2_05_manchas.py` | — | Primavera/Verão | NDVI S2 |
| `c2_06_este_plantado.py` | — | Primavera/Verão | NDVI S2 |
| `c2_08_cruzamento.py` | — | ambas | SAR S1 · NDVI S2 |
| `c2_09_sar_verificacao.py` | — | ambas | NDVI S2 |
| `c2_12_pergola_2012.py` | — | Primavera/Verão | NDVI S2 · ortofoto |
| `c2_13_coberto_2025.py` | — | Primavera/Verão | NDVI S2 · ortofoto |
| `c3_07_georreferenciar.py` | — | Primavera/Verão | LiDAR · IFAP |
| `c3_09_organismos_contra_padrao.py` | — | ? | — |
| `c3_10_esforco_its_becrop.py` | — | ambas | IFAP |
| `c4_01_numeros.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto · IFAP |
| `c4_02_razao.py` | — | ambas | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `c4_r2_01_multiverso_das_valvulas.py` | — | Primavera/Verão | LiDAR |
| `c5_01_reetiquetagem.py` | — | ambas | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `c5_02_amostragem.py` | — | Primavera/Verão | NDVI S2 · ortofoto · IFAP |
| `altura_copado.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `amplitude.py` | — | ano inteiro | NDVI S2 |
| `emparelhar_moedas.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `landsat_independente.py` | — | ano inteiro | NDVI S2 · Landsat · LiDAR |
| `paisagem.py` | — | ? | NDVI S2 · LiDAR · IFAP |
| `refazer_c2_este.py` | — | Primavera/Verão | NDVI S2 · LiDAR · ortofoto |
| `serie_separada.py` | — | Primavera/Verão | NDVI S2 · LiDAR |
| `terreno_contra_declinio.py` | — | Primavera/Verão | NDVI S2 · Landsat · LiDAR |
| `triagem_referencia_densa.py` | — | ano inteiro | NDVI S2 · LiDAR |
| `fazer_masks_v2.py` | — | Primavera/Verão | NDVI S2 |
| `serie_oriental_pergola.py` | A1 | Primavera/Verão | LiDAR · ortofoto |
| `c1_09_sar.py` | A2 | Inverno | SAR S1 · NDVI S2 |
| `reg01_triagem_descontinuidade.py` | A3 | Primavera/Verão | NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `multiverso_degrau.py` | B1 | Primavera/Verão | NDVI S2 · LiDAR · IFAP |
| `degrau_vs_recta_pergola.py` | B2 | Primavera/Verão | LiDAR |
| `satelites_degrau.py` | B3 | Primavera/Verão | LiDAR |
| `satelites_sem_2026.py` | B4 | Primavera/Verão | NDVI S2 · LiDAR · IFAP |
| `fenologia_por_unidade.py` | B5 | Primavera/Verão | NDVI S2 · LiDAR |
| `halo_distancia.py` | B7 | Primavera/Verão | NDVI S2 · LiDAR |
| `l1_data_do_voo.py` | C1 | ano inteiro | LiDAR |
| `g19_parcelario.py` | C3 | ? | IFAP |
| `lobulo_oeste_degrau.py` | C7 | ? | NDVI S2 · LiDAR · ortofoto |
| `valvulas_1a5_o_troco_que_falta.py` | C8 | Primavera/Verão | IFAP |
| `c1_03_mdt.py` | C9 | ? | LiDAR |
| `a2_solo_caracterizacao.py` | D9 | ? | NDVI S2 |

## Os NÃO citáveis que emitem resultado — por estação

### Primavera/Verão — 53 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `_TENTATIVA_FALHADA_mascaras_geograficas.py` | falta certificacao | NDVI S2 · ortofoto |
| `assinatura_espectral.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat · LiDAR · IFAP |
| `audit_termico.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat |
| `audit_termico.py` | falta certificacao e auditoria independente | NDVI S2 · Landsat |
| `b1_analise.py` | falta auditoria independente | NDVI S2 |
| `b1_como_unidade.py` | falta certificacao | NDVI S2 · Landsat · ortofoto · IFAP |
| `b1_contra_corpo.py` | falta certificacao e auditoria independente | NDVI S2 · LiDAR · IFAP |
| `b1_nucleo_interno.py` | falta auditoria independente | NDVI S2 |
| `b1_nucleo_interno.py` | falta auditoria independente | NDVI S2 |
| `b1_serie_verdadeira.py` | falta certificacao | NDVI S2 · ortofoto |
| `b1_serie_verdadeira.py` | falta certificacao | NDVI S2 · ortofoto |
| `b1_subblocos.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `b1_subblocos.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `b1_terreno.py` | falta certificacao | LiDAR · IFAP |
| `c0_02_mascaras.py` | falta auditoria independente | NDVI S2 |
| `c0_11_assuncoes.py` | falta auditoria independente | NDVI S2 · LiDAR |
| `c1_02_costura.py` | falta auditoria independente | LiDAR · ortofoto |
| `c1_14_ancoras.py` | falta auditoria independente | NDVI S2 |
| `c2_01_serie.py` | falta auditoria independente | NDVI S2 |
| `c2_02_fenologia.py` | falta auditoria independente | NDVI S2 |
| `c2_03_defice.py` | falta auditoria independente | NDVI S2 |
| `c3_06_unidade.py` | falta certificacao | NDVI S2 · Landsat · LiDAR |
| `c3_07_mascara_pre.py` | falta certificacao | NDVI S2 · Landsat · LiDAR · ortofoto |
| `c3_08_controlo_referencia.py` | falta auditoria independente | — |
| `c3_13_T2_T4.py` | falta auditoria independente | NDVI S2 |
| `c3_r2_01_amostras_contra_pergola.py` | falta auditoria independente | LiDAR |
| `c8_05_veredicto.py` | falta certificacao | IFAP |
| `ctrl_14_metricas.py` | falta auditoria independente | NDVI S2 · LiDAR · ortofoto |
| `degrau_robustez.py` | falta certificacao e auditoria independente | LiDAR |
| `difusa.py` | falta certificacao e auditoria independente | NDVI S2 |
| `difusa.py` | falta certificacao e auditoria independente | NDVI S2 |
| `estatuto.py` | falta certificacao e auditoria independente | LiDAR · ortofoto |
| `exportar_auditoria.py` | falta certificacao e auditoria independente | NDVI S2 · LiDAR |
| `fazer_masks.py` | falta certificacao | NDVI S2 |
| `filtro_w.py` | falta certificacao e auditoria independente | NDVI S2 |
| `fuga.py` | falta certificacao e auditoria independente | SAR S1 · NDVI S2 · Landsat · LiDAR · ortofoto |
| `g16_serie.py` | falta certificacao e auditoria independente | NDVI S2 · ortofoto |
| `g18_final.py` | falta certificacao | NDVI S2 · ortofoto |
| `gancho_arranque.py` | falta certificacao e auditoria independente | — |
| `ifap_cruzamento.py` | falta certificacao | LiDAR · IFAP |
| … e mais 13 | | |

### Inverno — 7 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `c1_12_sar_lavrado.py` | falta auditoria independente | SAR S1 |
| `c1_13_sar_antes_depois.py` | falta auditoria independente | SAR S1 · NDVI S2 · ortofoto |
| `c2_07_sar_pilha.py` | falta auditoria independente | SAR S1 · NDVI S2 |
| `exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `exportar_pendentes2.py` | falta certificacao | SAR S1 · LiDAR |
| `piso_inverno.py` | falta auditoria independente | NDVI S2 |
| `sar_invernos.py` | falta certificacao | SAR S1 |

### ambas — 10 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `c1_06_solo_no_mapa.py` | falta auditoria independente | LiDAR |
| `c1_08_clima.py` | falta auditoria independente | — |
| `c2_10_ancoras.py` | falta auditoria independente | SAR S1 · NDVI S2 |
| `c3a2_05_multiplicidade.py` | falta certificacao | — |
| `exportar_pendentes.py` | falta certificacao e auditoria independente | NDVI S2 |
| `exportar_pendentes.py` | falta certificacao e auditoria independente | NDVI S2 |
| `fenologia.py` | falta auditoria independente | NDVI S2 |
| `fenologia.py` | falta auditoria independente | NDVI S2 |
| `registo_de_factos.py` | falta certificacao | SAR S1 · NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `triagem_de_fontes.py` | falta certificacao | NDVI S2 · Landsat · LiDAR · IFAP |

### ano inteiro — 5 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `c1_07_termico.py` | falta auditoria independente | NDVI S2 · Landsat |
| `indice_inteligencia.py` | falta certificacao e auditoria independente | SAR S1 · NDVI S2 · Landsat · LiDAR · ortofoto · IFAP |
| `reg01_landsat.py` | falta certificacao | NDVI S2 · Landsat · IFAP |
| `sar_ano_inteiro.py` | falta certificacao e auditoria independente | SAR S1 · NDVI S2 |
| `serie_densa_descontinuidades.py` | falta certificacao e auditoria independente | NDVI S2 |

### ? — 76 guiões

| guião | o que falta | instrumento |
|---|---|---|
| `b1_divisao.py` | falta certificacao | ortofoto |
| `b1_divisao.py` | falta certificacao | ortofoto |
| `b1_serie.py` | falta auditoria independente | NDVI S2 |
| `bacia.py` | falta auditoria independente | LiDAR · ortofoto |
| `bacia2.py` | falta auditoria independente | LiDAR |
| `c0_01_rasters.py` | falta auditoria independente | NDVI S2 |
| `c0_05_orto.py` | falta auditoria independente | ortofoto |
| `c0_10_quarentena_b1.py` | falta auditoria independente | NDVI S2 · ortofoto |
| `c1_01_lidar_inventario.py` | falta auditoria independente | LiDAR |
| `c1_05_bacia.py` | falta auditoria independente | LiDAR |
| `c1_11_escalas.py` | falta auditoria independente | LiDAR |
| `c1ab_contra_kiwi_ifap.py` | falta certificacao e auditoria independente | ortofoto · IFAP |
| `c3_00_inventario.py` | falta certificacao e auditoria independente | LiDAR |
| `c3_01_reconciliar.py` | falta certificacao e auditoria independente | IFAP |
| `c3_01_triagem_sensibilidade.py` | falta certificacao | — |
| `c3_02_desalinhamento.py` | falta certificacao e auditoria independente | — |
| `c3_03_alinhamento.py` | falta auditoria independente | — |
| `c3_03_margem.py` | falta certificacao | — |
| `c3_04_anos_e_donos.py` | falta certificacao | — |
| `c3_04_perfil_registos.py` | falta certificacao e auditoria independente | IFAP |
| `c3_08_orto_tres.py` | falta certificacao | Landsat · ortofoto · IFAP |
| `c3_11_par_contraste_e_ancoras.py` | falta certificacao | LiDAR |
| `c3a2_02_matriz.py` | falta certificacao | — |
| `c3a2_03_q1_probabilidade.py` | falta certificacao | — |
| `c3a2_04_q5_doze.py` | falta certificacao | — |
| `c3b1_01_geometria.py` | falta certificacao | NDVI S2 · ortofoto · IFAP |
| `c3b1_02_saturacao.py` | falta certificacao | — |
| `c3b1_03_estabelecimento.py` | falta certificacao | — |
| `c3b1_04_concordancia.py` | falta certificacao | NDVI S2 · Landsat · ortofoto · IFAP |
| `c3b1_05_multiverso.py` | falta certificacao | — |
| `c3b1_08_cronometro.py` | falta certificacao | NDVI S2 · Landsat |
| `c3b1_09_orto.py` | falta certificacao | NDVI S2 · Landsat · ortofoto |
| `c3b1_10_veredicto.py` | falta certificacao | ortofoto |
| `c8_01_extrai.py` | falta certificacao | — |
| `c8_03_tinta.py` | falta certificacao | — |
| `c8_04_sectores.py` | falta certificacao | — |
| `c8_06_extrapolacoes.py` | falta certificacao | — |
| `c8_07_contiguidade.py` | falta certificacao | — |
| `c8_08_o_177.py` | falta certificacao | ortofoto · IFAP |
| `c8_09_tres_enumeracoes.py` | falta certificacao | — |
| … e mais 36 | | |

