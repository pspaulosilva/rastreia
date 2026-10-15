# Dicionário de Dados — Base Recife Monitora

> **Base sintética.** Os valores não correspondem a equipes, unidades, profissionais ou resultados reais da Secretaria de Saúde do Recife. A estrutura replica a descrição oficial do programa constante da documentação do desafio.

Este documento descreve a estrutura **pretendida** da base e as regras de negócio do programa. Como em qualquer extração de sistema em produção, o que está nos arquivos pode divergir do que está especificado aqui — verificar essa aderência faz parte do trabalho de entendimento e preparação dos dados.

## Visão geral

| Arquivo | Grão (1 linha =) |
|---|---|
| `equipes.csv` | uma equipe de saúde |
| `resultados_ciclos.csv` | uma equipe em um ciclo quadrimestral |
| `eixo3_indicadores.csv` | um indicador de uma equipe em um ciclo |
| `nps_atributos.csv` | um atributo de satisfação de uma equipe em um ciclo |
| `planos_acao.csv` | um plano de ação |

## Relacionamentos pretendidos

```
equipes.csv
   │ codigo_ine (chave primária)
   ├──< resultados_ciclos.csv     (codigo_ine + ciclo)
   ├──< eixo3_indicadores.csv     (codigo_ine + ciclo + codigo_indicador)
   ├──< nps_atributos.csv         (codigo_ine + ciclo + codigo_atributo)
   └──< planos_acao.csv           (codigo_ine + ciclo)
```

---

## `equipes.csv` — cadastro da rede

| Campo | Tipo | Domínio pretendido |
|---|---|---|
| `codigo_cnes` | texto | Identificador da unidade de saúde, 7 dígitos |
| `codigo_ine` | texto | Identificador Nacional de Equipe. Chave primária |
| `nome_unidade` | texto | Nome da unidade |
| `nome_equipe` | texto | Rótulo da equipe |
| `distrito_sanitario` | categórico | 8 distritos sanitários (I a VIII) |
| `tipo_equipe` | categórico | `eSF`, `eSB` ou `eMulti` |
| `grupo` | inteiro | 1 a 4. Determina quais indicadores do Eixo 3 se aplicam e com que peso |
| `populacao_adscrita` | inteiro | População vinculada à equipe |
| `n_profissionais` | inteiro | Profissionais na equipe. Conforme o cliente, varia de 8 a 80 |

---

## `resultados_ciclos.csv` — resultados por ciclo

| Campo | Tipo | Domínio pretendido |
|---|---|---|
| `codigo_ine` | texto | Referência a `equipes.csv` |
| `ciclo` | texto | Ciclo quadrimestral no formato `AAAA.Q`, de `2023.1` a `2026.2` |
| `eixo1_bloco_a` | decimal | 0 a 80. Percepção dos profissionais (instrumento anônimo) |
| `eixo1_bloco_b` | decimal | 0 a 60. Processos de trabalho |
| `eixo1_bloco_c` | decimal | 0 a 60. Estrutura e insumos |
| `eixo1_total` | decimal | 0 a 200 |
| `taxa_resposta_bloco_a` | decimal | 0 a 1 |
| `bloco_a_valido` | booleano | Derivado da taxa de resposta, conforme a regra 1 abaixo |
| `eixo2_total` | decimal | 0 a 200. Satisfação do usuário (NPS convertido em pontos) |
| `eixo3_total` | decimal | 0 a 600. Desempenho assistencial |
| `pontuacao_final` | decimal | 0 a 1.000. Soma dos três eixos |
| `zona_classificacao` | categórico | Conforme a regra 6 abaixo |
| `situacao_participacao` | categórico | `Participante` ou `Desclassificada` |

---

## `eixo3_indicadores.csv` — detalhe do Eixo 3

| Campo | Tipo | Domínio pretendido |
|---|---|---|
| `codigo_ine`, `ciclo` | texto | Chave composta |
| `codigo_indicador` | categórico | `IND01` a `IND10` |
| `indicador` | texto | Descrição do indicador |
| `peso_maximo` | inteiro | Pontos máximos do indicador para o grupo daquela equipe. Somam 600 em todos os grupos |
| `percentual_alcancado` | decimal | Desempenho da equipe no indicador |
| `pontos_obtidos` | decimal | Produto do desempenho pelo peso máximo |

---

## `nps_atributos.csv` — detalhe do Eixo 2

| Campo | Tipo | Domínio pretendido |
|---|---|---|
| `codigo_ine`, `ciclo` | texto | Chave composta |
| `codigo_atributo` | categórico | `ATR1` a `ATR5` |
| `atributo` | texto | Acolhimento, tempo de espera, resolutividade, estrutura, vínculo |
| `nps` | decimal | −100 a 100 |
| `n_respondentes` | inteiro | Respostas computadas no atributo naquele ciclo |

---

## `planos_acao.csv` — planos e maturidade

| Campo | Tipo | Domínio pretendido |
|---|---|---|
| `id_plano` | texto | Chave primária |
| `codigo_ine`, `ciclo` | texto | Chave composta |
| `texto_plano` | texto | Texto livre do plano elaborado pela equipe |
| `dim_governanca` | inteiro | 1 a 5 |
| `dim_smart` | inteiro | 1 a 5 |
| `dim_viabilidade` | inteiro | 1 a 5 |
| `nivel_maturidade` | inteiro | 1, 2 ou 3 |
| `rotulo_maturidade` | categórico | `Reformulação` (1), `Ajustes` (2), `Aprovado` (3) |

---

## Regras de negócio do programa

Estas regras vêm da documentação do Recife Monitora e devem ser respeitadas em qualquer análise. Ignorá-las produz conclusão incorreta mesmo com código correto.

1. **Validade do Bloco A.** Equipe com taxa de resposta inferior a 30% tem o Bloco A considerado inválido, e sua pontuação não é computada.
2. **Desclassificação.** Equipe desclassificada em um ciclo não possui pontuação naquele ciclo. Isso é ausência de dado, não desempenho ruim.
3. **Pesos variam por grupo.** A distribuição dos 600 pontos do Eixo 3 entre os indicadores muda conforme o grupo (1 a 4), e nem todos os indicadores se aplicam a todos os grupos.
4. **Porte desigual.** As equipes variam de 8 a 80 profissionais e atendem populações adscritas de tamanhos muito diferentes.
5. **Ciclo quadrimestral.** Três ciclos por ano desde a implantação do programa, em 2023.
6. **Zonas de classificação** sobre a pontuação final: Excelência (≥850), Qualidade (700–849), Aperfeiçoamento (550–699), Crítica (400–549), Insuficiente (<400).

---

## Observação sobre a qualidade dos dados

Esta base reproduz as condições de uma extração real de sistema em produção. Como em qualquer base desse tipo, é esperado encontrar divergências entre o que está especificado aqui e o que está efetivamente nos arquivos.

Perfilar a base antes de analisar — verificar tipos, domínios, unicidade de chaves, integridade referencial, completude e consistência entre tabelas — é parte da etapa de Entendimento dos Dados e condição para que a Análise Preliminar seja confiável.
