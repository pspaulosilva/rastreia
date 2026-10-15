# Perfilamento da base sintética do Recife Monitora

Gerado por `pipeline/perfilar_base.py`. Base 100% sintética (DADOS SIMULADOS).

## 1. Volume e contagem antes e depois da limpeza

| tabela | grão | linhas cruas | linhas após limpeza | removidas | colunas |
|---|---|---|---|---|---|
| equipes | codigo_ine | 132 | 132 | 0 | 9 |
| resultados_ciclos | codigo_ine/ciclo | 1392 | 1363 | 29 | 13 |
| eixo3_indicadores | codigo_ine/ciclo/codigo_indicador | 13294 | 13294 | 0 | 7 |
| nps_atributos | codigo_ine/ciclo/codigo_atributo | 6815 | 6815 | 0 | 6 |
| planos_acao | id_plano | 420 | 420 | 0 | 9 |

## 2. Tipos, completude e domínio por coluna (base crua)

### equipes.csv

| coluna | tipo inferido | nulos | completude | valores distintos | exemplo |
|---|---|---|---|---|---|
| codigo_cnes | numérico | 0 | 100.0% | 61 | 2437842 |
| codigo_ine | numérico | 0 | 100.0% | 132 | 6000000000 |
| nome_unidade | texto/categórico | 0 | 100.0% | 74 | USF V-842 |
| nome_equipe | texto/categórico | 0 | 100.0% | 132 | Equipe 001 |
| distrito_sanitario | texto/categórico | 0 | 100.0% | 19 | Distrito Sanitário V |
| tipo_equipe | texto/categórico | 0 | 100.0% | 12 | eSF |
| grupo | numérico | 0 | 100.0% | 4 | 2 |
| populacao_adscrita | numérico | 11 | 91.7% | 121 | 2455.0 |
| n_profissionais | numérico | 0 | 100.0% | 38 | 15 |

### resultados_ciclos.csv

| coluna | tipo inferido | nulos | completude | valores distintos | exemplo |
|---|---|---|---|---|---|
| codigo_ine | numérico | 0 | 100.0% | 145 | 6000000000 |
| ciclo | numérico | 0 | 100.0% | 43 | 2023.1 |
| eixo1_bloco_a | numérico | 58 | 95.8% | 392 | 57.3 |
| eixo1_bloco_b | numérico | 58 | 95.8% | 336 | 45.1 |
| eixo1_bloco_c | numérico | 58 | 95.8% | 335 | 40.8 |
| eixo1_total | numérico | 58 | 95.8% | 750 | 143.2 |
| taxa_resposta_bloco_a | numérico | 0 | 100.0% | 1189 | 0.6462 |
| bloco_a_valido | texto/categórico | 0 | 100.0% | 2 | True |
| eixo2_total | numérico | 230 | 83.5% | 732 | 122.6 |
| eixo3_total | numérico | 58 | 95.8% | 1005 | 395.8 |
| pontuacao_final | numérico | 58 | 95.8% | 1104 | 661.6 |
| zona_classificacao | texto/categórico | 58 | 95.8% | 5 | Aperfeiçoamento |
| situacao_participacao | texto/categórico | 0 | 100.0% | 2 | Participante |

### eixo3_indicadores.csv

| coluna | tipo inferido | nulos | completude | valores distintos | exemplo |
|---|---|---|---|---|---|
| codigo_ine | numérico | 0 | 100.0% | 132 | 6000000000 |
| ciclo | numérico | 0 | 100.0% | 11 | 2023.1 |
| codigo_indicador | texto/categórico | 0 | 100.0% | 10 | IND01 |
| indicador | texto/categórico | 0 | 100.0% | 10 | Proporção de gestantes com 6 o |
| peso_maximo | numérico | 0 | 100.0% | 14 | 75 |
| percentual_alcancado | numérico | 0 | 100.0% | 5702 | 0.6223 |
| pontos_obtidos | numérico | 0 | 100.0% | 737 | 46.7 |

### nps_atributos.csv

| coluna | tipo inferido | nulos | completude | valores distintos | exemplo |
|---|---|---|---|---|---|
| codigo_ine | numérico | 0 | 100.0% | 132 | 6000000000 |
| ciclo | numérico | 0 | 100.0% | 11 | 2023.1 |
| codigo_atributo | texto/categórico | 0 | 100.0% | 5 | ATR1 |
| atributo | texto/categórico | 0 | 100.0% | 5 | Acolhimento da equipe |
| nps | numérico | 260 | 96.2% | 1289 | 44.6 |
| n_respondentes | numérico | 0 | 100.0% | 137 | 21 |

### planos_acao.csv

| coluna | tipo inferido | nulos | completude | valores distintos | exemplo |
|---|---|---|---|---|---|
| id_plano | texto/categórico | 0 | 100.0% | 420 | PA00001 |
| codigo_ine | numérico | 0 | 100.0% | 128 | 6000000058 |
| ciclo | numérico | 0 | 100.0% | 11 | 2024.2 |
| texto_plano | texto/categórico | 10 | 97.6% | 215 | Diante da identificação de alt |
| dim_governanca | numérico | 0 | 100.0% | 4 | 4 |
| dim_smart | numérico | 0 | 100.0% | 5 | 5 |
| dim_viabilidade | numérico | 0 | 100.0% | 4 | 3 |
| nivel_maturidade | numérico | 0 | 100.0% | 3 | 3 |
| rotulo_maturidade | texto/categórico | 0 | 100.0% | 3 | Aprovado |

## 3. Chaves e integridade referencial

| tabela | chave | duplicatas na chave (cru) | codigo_ine sem cadastro (cru) | duplicatas após limpeza |
|---|---|---|---|---|
| equipes | codigo_ine | 0 | 0 | 0 |
| resultados_ciclos | codigo_ine+ciclo | 12 | 13 | 0 |
| eixo3_indicadores | codigo_ine+ciclo+codigo_indicador | 0 | 0 | 0 |
| nps_atributos | codigo_ine+ciclo+codigo_atributo | 0 | 0 | 0 |
| planos_acao | id_plano | 0 | 0 | 0 |

## 4. Registro de cada tratamento (qualidade_dados.json)

Contagem = linhas afetadas antes do tratamento; a contagem total após limpeza está na seção 1.

| # | tabela | problema | linhas | decisão |
|---|---|---|---|---|
| 1 | equipes | distrito_sanitario com 19 grafias (maiúsculas, sem acento, 'ds v') | 19 | normalizado para 'DS <romano>' por regex |
| 2 | equipes | tipo_equipe com variações (e-SF, ESF, ' eSF', esb...) | 23 | normalizado para eSF / eSB / eMulti |
| 3 | equipes | nome_unidade com espaços nas bordas (13 CNES com 2 grafias) | 22 | strip; CNES passa a ter 1 nome |
| 4 | equipes | populacao_adscrita ausente | 11 | mantido nulo; normalização por porte usa n_profissionais |
| 5 | equipes | n_profissionais máximo 53 (cliente informou até 80) | 0 | registrado como divergência a confirmar com o cliente |
| 6 | resultados | ciclo em 4 formatos (AAAA.Q, AAAA-Q, AAAAQn, Q/AAAA) | 96 | normalizado para AAAA.Q |
| 7 | resultados | equipe+ciclo duplicados (mesmo conteúdo, ciclo grafado diferente) | 16 | mantida 1 linha por equipe+ciclo |
| 8 | resultados | codigo_ine sem cadastro em equipes.csv (INE 7xxxxxxxxx) | 13 | excluídos do painel; listados para o cliente |
| 9 | resultados | eixo2_total com vírgula decimal | 122 | convertido para ponto |
| 10 | resultados | situacao_participacao = Desclassificada (sem pontuação) | 57 | mantida como ausência de dado, nunca como zero (regra 2) |
| 11 | resultados | taxa < 30% mas bloco_a_valido = True (viola regra 1) | 0 | recalculado: bloco_a_valido = taxa >= 0,30 |
| 12 | resultados | taxa_resposta_bloco_a fora de [0,1] | 7 | taxa anulada; validade do Bloco A mantida como veio |
| 13 | resultados | Bloco A inválido registrado como 0 e somado ao Eixo 1 (regra 1 diz 'não computado') | 147 | mantido como a plataforma calcula (0 pts) e sinalizado; a IA trata como 'não avaliado', não como desempenho ruim |
| 14 | resultados | eixo2_total ausente nos 3 ciclos de 2023, embora pontuacao_final o inclua | 170 | reconstruído como final - eixo1 - eixo3 (sinalizado) |
| 15 | resultados | pontuacao_final impossível (-35, 1247, 1580, 9999) | 9 | recalculada como eixo1 + eixo2 + eixo3; eixo2 ausente estimado pela média do NPS + 100 |
| 16 | resultados | máximos dos blocos do Eixo 1 vieram como A=80, B=60, C=60; Manual define A=40, B=80, C=80 | 1306 | base sintética reescalada proporcionalmente para os máximos do Manual; pontuação final recomposta |
| 17 | resultados | zonas vieram com faixas 850/700/550/400 (dicionário); Manual define 900/800/600/400 | 512 | zona recalculada pelas faixas do Manual (Quadro 10) sobre a pontuação recomposta |
| 18 | resultados | equipes sem linha em alguns ciclos (adesão voluntária) | 89 | ausência tratada como 'não participou', não como queda |
| 19 | eixo3 | percentual_alcancado em escala 0-100 em vez de 0-1 | 380 | dividido por 100; pontos_obtidos conferidos = pct x peso |
| 20 | eixo3 | IND03 e IND08 (odontologia) não se aplicam ao grupo 4; pesos variam por grupo | 0 | recomendações só citam indicadores aplicáveis ao grupo da equipe (regra 3) |
| 21 | nps | nps ausente em atributos isolados | 260 | mantido nulo; média do ciclo ignora o atributo ausente |
| 22 | nps | 5 atributos (acolhimento, espera, resolutividade, estrutura, vínculo) e conversão eixo2 = média NPS + 100, diferentes do Manual (6 perguntas, Quadro 7 por faixas) | 0 | mantido o esquema dos dados como simplificação da base sintética; conversão oficial (Quadro 7) entra com os dados reais |
| 23 | planos | texto_plano vazio ou nulo | 12 | mantido com marcador 'sem texto'; excluído da análise de linguagem |
| 24 | planos | textos repetidos (modelos padrão) | 194 | mantidos; indício de planos genéricos, insumo para a IA |
| 25 | equipes | nomes de unidades (USF V-842) e equipes (Equipe 001) são códigos sintéticos | 132 | substituídos por nomes fictícios de bairros do distrito; CNES e INE preservados como chave |

## 5. Medidas de dispersão da pontuação final (base limpa, equipes pontuadas)

| ciclo | n | media | mediana | desvio | minimo | q1 | q3 | maximo |
|---|---|---|---|---|---|---|---|---|
| 2023.1 | 100 | 603.3 | 607.6 | 95.4 | 341.0 | 556.9 | 659.5 | 848.6 |
| 2023.2 | 105 | 621.3 | 622.7 | 98.4 | 356.6 | 553.4 | 680.4 | 865.7 |
| 2023.3 | 112 | 622.3 | 623.9 | 95.2 | 358.5 | 562.2 | 686.3 | 848.3 |
| 2024.1 | 115 | 624.9 | 634.8 | 96.1 | 369.6 | 572.0 | 687.9 | 896.2 |
| 2024.2 | 119 | 611.8 | 614.7 | 96.1 | 345.2 | 554.8 | 668.4 | 868.1 |
| 2024.3 | 124 | 652.8 | 657.0 | 93.7 | 380.8 | 604.0 | 716.4 | 907.8 |
| 2025.1 | 125 | 661.4 | 666.5 | 98.7 | 404.4 | 608.4 | 726.8 | 869.8 |
| 2025.2 | 126 | 660.2 | 660.5 | 99.6 | 358.0 | 600.2 | 727.0 | 912.0 |
| 2025.3 | 125 | 665.2 | 663.9 | 101.9 | 386.9 | 600.1 | 723.9 | 917.2 |
| 2026.1 | 126 | 671.6 | 679.5 | 97.5 | 439.4 | 607.0 | 737.6 | 899.0 |
| 2026.2 | 129 | 680.8 | 681.7 | 101.2 | 391.6 | 620.0 | 735.8 | 937.9 |

Observações: no ciclo 2026.2, a mediana (681.7) fica próxima da média (680.8), sem assimetria forte; o desvio padrão de 101.2 pontos sobre uma escala de 1.000 indica dispersão moderada entre equipes; o intervalo interquartil (620.0 a 735.8) concentra metade das equipes na zona de Aperfeiçoamento.

Por distrito sanitário (último ciclo):

| distrito_sanitario | n | media | mediana | desvio |
|---|---|---|---|---|
| DS I | 13 | 717.4 | 733.3 | 83.2 |
| DS II | 14 | 670.5 | 705.0 | 143.3 |
| DS III | 14 | 739.0 | 721.8 | 99.4 |
| DS IV | 15 | 714.8 | 703.5 | 108.4 |
| DS V | 23 | 630.1 | 630.8 | 103.9 |
| DS VI | 19 | 653.9 | 657.2 | 53.2 |
| DS VII | 16 | 692.1 | 690.4 | 86.8 |
| DS VIII | 15 | 670.5 | 680.7 | 86.5 |

Correlação entre pontuação final e número de profissionais no último ciclo: r = -0.06 (fraca); o porte não explica a pontuação, o que sustenta a normalização por porte apenas para alertas, não para o ranking.

## 6. Figuras

- `figuras/hist_pontuacao_final.png`: histograma da pontuação final no ciclo 2026.2 com as faixas de zona do Manual.
- `figuras/boxplot_distrito.png`: boxplot por distrito sanitário.
- `figuras/dispersao_eixo1_eixo3.png`: dispersão Eixo 1 x Eixo 3 (r = 0.77).
