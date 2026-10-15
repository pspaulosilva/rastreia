# Revisão de Problema, Solução e Arquitetura a partir da Base Sintética
**Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2**
**Versão 1.1 · 24/09/2026 · Fonte: pasta `datos_sinteticos_recife_monitora_projetos_5` enviada pelo cliente (LEIA-ME, DICIONARIO_DE_DADOS e 5 CSVs)**

Base 100% sintética: nenhum valor corresponde a equipes ou resultados reais. Toda tela e relatório derivados dela exibem esse aviso.

Alteração da v1.1: como a base é simulada, o pipeline passou a realinhar zonas e máximos de bloco ao Manual de Avaliação (seção 3) e a atribuir nomes fictícios de bairros a unidades e equipes (CNES e INE preservados).

---

## 1. O que a base contém

| Arquivo | Grão | Linhas | Após limpeza |
|---|---|---|---|
| equipes.csv | equipe | 132 | 132 (61 CNES, 8 DS, grupos 1 a 4) |
| resultados_ciclos.csv | equipe x ciclo | 1.392 | 1.363 (11 ciclos, 2023.1 a 2026.2) |
| eixo3_indicadores.csv | equipe x ciclo x indicador | 13.294 | 13.294 (10 indicadores) |
| nps_atributos.csv | equipe x ciclo x atributo | 6.815 | 6.815 (5 atributos) |
| planos_acao.csv | plano de ação | 420 | 420 (3 dimensões + maturidade) |

Formato compatível com o registro de 10/09: pontuações e NPS já calculados, sem microdados.

## 2. Problemas encontrados no perfilamento (25 itens logados)

Tratamento em `pipeline/preparar_dados.py`, com log em `qualidade_dados.json`. Principais:

**Padronização**
- `ciclo` em 4 formatos (2023.1, 2023-1, 2023Q1, 1/2023) em 96 linhas; 16 duplicatas de equipe+ciclo surgem só por isso. Normalizado para AAAA.Q e deduplicado.
- `distrito_sanitario` com 19 grafias; `tipo_equipe` com 12 (e-SF, ESF, " eSF"...); `nome_unidade` com espaços nas bordas (13 CNES com 2 nomes). Normalizados.
- `eixo2_total` com vírgula decimal em 122 linhas; `percentual_alcancado` do Eixo 3 em escala 0 a 100 em 380 linhas (o restante em 0 a 1).

**Integridade**
- 13 INEs em resultados sem cadastro em equipes (prefixo 7). Excluídos do painel e listados para o cliente.
- 27 equipes não aparecem em todos os ciclos (adesão voluntária) e 57 linhas Desclassificadas sem pontuação. Tratadas como ausência de dado, nunca como zero ou queda.
- `pontuacao_final` impossível em 9 linhas (-35, 1247, 1580, 9999), com zona incoerente. Recalculada como soma dos eixos.
- `eixo2_total` ausente em todos os 170 registros de 2023, embora a pontuação final o inclua. Reconstruído como final - eixo1 - eixo3; onde não foi possível, estimado pela média do NPS + 100 (relação observada, r = 0,998).
- `taxa_resposta_bloco_a` fora de [0,1] em 7 linhas (2,4; -0,1; 1,35).
- 260 valores de NPS ausentes em atributos isolados; 12 planos sem texto; 11 equipes sem população adscrita.

**Regras de negócio**
- Bloco A inválido (taxa < 30%) aparece como 0 pontos somado ao Eixo 1 em 147 linhas (após deduplicação e exclusão dos INEs sem cadastro), enquanto a regra 1 diz "não computado". Efeito: a equipe perde até 40 pontos por baixa adesão à pesquisa interna, não por desempenho. Decisão: manter o cálculo da plataforma e sinalizar na interface; a IA trata como "não avaliado".
- IND03 e IND08 (odontologia) não se aplicam ao grupo 4; pesos por indicador variam por grupo (regra 3). Recomendações só citam indicadores aplicáveis ao grupo.

## 3. Divergências entre a base e os manuais e o que foi feito

| Tema | Manual de Avaliação (v. 02.03.26) | Base do cliente | Tratamento na v1.1 |
|---|---|---|---|
| Zonas de classificação | 900 / 800 / 600 / 400 | 850 / 700 / 550 / 400 | **Realinhado ao Manual**: zona recalculada sobre a pontuação recomposta |
| Blocos do Eixo 1 | A 40, B 80, C 80 | A 80, B 60, C 60 | **Realinhado ao Manual**: blocos reescalados proporcionalmente, Eixo 1 e pontuação final recompostos |
| Eixo 2 | 6 perguntas, conversão por faixas (Quadro 7) | 5 atributos, eixo2 = média do NPS + 100 | Mantido como simplificação da base sintética; Quadro 7 entra com os dados reais |
| Eixo 3 | 8 indicadores por tipo de equipe | 10 indicadores, pesos por grupo 1 a 4 | Mantido (indicadores do MS, pesos somam 600) |
| Nomes | Unidades e equipes reais | USF V-842, Equipe 001 | Nomes fictícios de bairros do Recife por distrito; CNES e INE preservados |
| Porte | 8 a 80 profissionais | 8 a 53 | Registrar |
| Escala | ~300 equipes aderidas (fontes públicas) | 132 | Pipeline sem supor tamanho da rede |

Efeito do realinhamento: com as faixas do Manual, a distribuição em 2026.2 passa a 2 Excelência, 14 Qualidade, 86 Aperfeiçoamento, 26 Crítica e 1 Insuficiente (antes: 7 / 46 / 60 / 15 / 1). Regra de arquitetura mantida: limiares, máximos e pesos ficam em configuração, nunca no código.

## 4. Revisão do problema

O problema declarado (análise manual, identificação tardia, falta de recomendações) se confirma e ganha duas camadas novas visíveis nos dados:

1. **Qualidade do dado é parte do problema.** A extração reproduz o que uma equipe de gestão recebe: formatos mistos, duplicatas, outliers e ausências. Hoje isso é resolvido à mão em planilha. Sem uma camada de saneamento, qualquer alerta é falso ou tardio.
2. **Planos de ação já existem e são avaliados** em três dimensões (governança, SMART, viabilidade) com maturidade 1 a 3. 42% dos planos estão em "Ajustes" e 29% em "Reformulação"; 194 dos 420 repetem modelos padrão. Isso mostra que o gargalo não é só ler a nota, é transformar a nota em plano executável.

## 5. Revisão da solução (módulos)

| Módulo | Antes | Agora, com os dados |
|---|---|---|
| M1 Alertas de priorização | Semáforo por zona e queda entre ciclos | Mesmo, mais: ausência de participação, Bloco A inválido e NPS por atributo. Zonas do Manual (900/800/600/400). Severidade considera porte (n_profissionais) e histórico de 11 ciclos |
| M2 Recomendações | Onde perdeu pontos, com fonte | Diagnóstico por indicador aplicável ao grupo e por atributo do NPS, mais **assistente de plano de ação**: avalia o rascunho da equipe nas 3 dimensões da base e sugere reescrita SMART. Novo: usa o histórico de 420 planos como referência |
| M3 Chatbot interno (RAG) | Manuais e resultados | Mesmo, mais consultas sobre planos e sobre qualidade do dado ("essa equipe participou em 2024.2?") |
| **M0 Saneamento e qualidade (novo)** | Não previsto | Pipeline reproduzível, log de qualidade visível ao gestor central, parâmetros do programa configuráveis |

O resumo do quadrimestre (RF05) passa a informar quantas equipes participaram, quantas foram desclassificadas e quantos registros foram corrigidos, para que o gestor saiba a base sobre a qual as conclusões foram tiradas.

## 6. Revisão da arquitetura

```
Middleware de leitura (cliente)  ->  Ingestão  ->  Camada de saneamento (M0)  ->  Camada analítica (lote)  ->  Camada de IA  ->  Interfaces
   valores já calculados            por ciclo      normaliza, deduplica,          zonas, tendências,          regras + LLM local     painel, alertas,
   equipes, resultados, eixo3,      + NPS diário   reconstrói, loga               severidade, causas          para recomendações,    resumo, chat,
   nps, planos                                      (qualidade_dados)              de perda por grupo          RAG sobre manuais      qualidade
                                                                                                                e planos               do dado
```

Decisões:
- **Origem isolada** em um único módulo (`carregar()`), conforme LEIA-ME; a troca para o middleware não altera o restante.
- **Parâmetros do programa em tabela** (zonas, máximos de bloco, pesos por grupo e ciclo). O MVP roda com os valores do Manual; a base sintética é realinhada pelo pipeline.
- **Pré-computação em lote** por ciclo para painel, alertas e resumo (RNF03); inferência sob demanda só no chat e no assistente de plano.
- **Log de qualidade como dado de primeira classe**, exposto na interface e anexado ao resumo do quadrimestre (trilha de auditoria, RNF05).
- **Ausência e desclassificação são estados**, não zeros, em todas as agregações.
- **Escala**: pipeline vetorizado, sem suposição sobre número de equipes; testado com 132, dimensionado para 300+.

## 7. Impacto nos requisitos

- RF04 (agregar por equipe, distrito e rede) ganha a regra "normalizar por n_profissionais quando população estiver ausente".
- RF06 (alertas) ganha critérios: não participação no ciclo, Bloco A inválido, NPS negativo em atributo com peso.
- RF08 (recomendações) ganha o sub-requisito "avaliar e reescrever plano de ação nas dimensões governança, SMART e viabilidade".
- Novo RF11: pipeline de saneamento reproduzível com log de qualidade por ciclo.
- Novo RNF08: parâmetros do programa configuráveis sem alteração de código.

## 8. Perguntas ao cliente

1. Confirmar que valem as faixas de zona e os máximos de bloco do Manual (a base veio diferente).
2. O Bloco A inválido deve entrar como 0 ou ser excluído da pontuação (e a equipe reclassificada)?
3. Confirmar a conversão do Eixo 2 (Quadro 7) e o número de atributos nos dados reais.
4. Os 13 INEs sem cadastro são migrações (decisão D4) ou lixo de extração?
5. Como o cliente quer receber o log de qualidade: na interface, no PDF do quadrimestre, ou nos dois?
6. Os planos de ação e sua avaliação de maturidade fazem parte do escopo do middleware?

## 9. Riscos atualizados

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Dados reais atrasam além do SR2 | Alta | Pipeline pronto sobre a base sintética; troca localizada em `carregar()` |
| Dados reais têm problemas diferentes dos simulados | Média | Log de qualidade genérico por tipo de checagem; testes de contrato por tabela |
| Regras do manual e da base continuam divergentes | Média | Parâmetros em tabela; decisão formal do NIIMA registrada por ciclo |
| Bloco A inválido penaliza equipes e gera alerta injusto | Média | Sinalização explícita na interface; alerta de "baixa adesão à pesquisa interna" separado do alerta de desempenho |

---

*Artefatos: `pipeline/preparar_dados.py`, `qualidade_dados.json`, `rastreia_data.json` (pacote do protótipo), `assets/` (favicon e imagem de preview). Documento vivo, revisar ao receber os dados reais.*
