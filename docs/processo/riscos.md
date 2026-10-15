# Mapa de riscos: probabilidade, impacto e cenários

RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2. Versão 1.0 · 15/10/2026. Complementa os riscos R1 a R4 do Documento de Requisitos (10/09), que já tinham mitigação.

Escala: probabilidade e impacto de 1 (baixo) a 5 (alto); exposição = probabilidade x impacto. Dono = quem acompanha o risco na equipe.

## Matriz

| ID | Risco | Prob. | Impacto | Exposição | Gatilho observável | Mitigação (já em curso) | Contingência (se ocorrer) | Dono |
|---|---|---|---|---|---|---|---|---|
| R1 | Middleware de leitura do cliente atrasa e os dados reais não chegam até o SR2 | 5 | 4 | 20 | Sem resposta do NIIMA até a semana 10; pedido formal ainda em tramitação em 15/10 | Pipeline construído sobre a base sintética no esquema real; origem isolada em `carregar()`; contrato de API em definição com Anderson | Entregar o SR2 e o final sobre a base sintética com aviso visível; registrar no cronograma a repactuação e a data limite para troca da fonte | Paulo |
| R2 | GPU do cliente insuficiente para rodar o LLM local do assistente | 3 | 3 | 9 | Hardware não confirmado nas questões 5 e 6 ao cliente | Modelos pequenos quantizados; pipeline analítico (alertas, resumo, recomendações por regra) separado do chatbot | Entregar M1 e M2 sem LLM; assistente fica como piloto em nuvem com dados anonimizados até haver GPU | Pedro |
| R3 | Regras de migração de profissional e INE incorretas distorcem o NPS por equipe | 3 | 4 | 12 | Questão 2 ao cliente sem resposta; 13 INEs sem cadastro na base sintética | Validar regras com Anderson antes de implementar; tabela de vigência (US03); INEs órfãos excluídos e listados | Marcar as equipes afetadas como "em revisão" no painel e não gerar alerta até a regra ser confirmada | Davi |
| R4 | Canais de alerta (e-mail, WhatsApp, Telegram) sem aval institucional | 4 | 2 | 8 | Questão 6 ao cliente sem resposta | E-mail institucional como canal mínimo; WhatsApp e Telegram condicionados à aprovação | Alertas ficam só no painel, com contador por perfil (já implementado no Protótipo 5) | Lorena |
| R5 | Regras do Manual de Avaliação e do dicionário da base continuam divergentes (zonas 900/800/600/400 vs 850/700/550/400; blocos A40/B80/C80 vs A80/B60/C60) | 4 | 3 | 12 | Devolutiva do SR1 aponta Protótipos 3/4 e 5 com faixas diferentes; professor vai esclarecer | Parâmetros em configuração; cada tela registra a faixa usada e a fonte; os dois modos mantidos no pipeline | Adotar a faixa que o professor ou o NIIMA decidir e regerar os pacotes com um comando (`preparar_dados.py` + `embutir_dados.py`) | Paulo |
| R6 | Bloco A inválido (taxa < 30%) penaliza equipes e gera alerta injusto | 3 | 3 | 9 | 147 linhas da base com Bloco A = 0 por baixa adesão à pesquisa interna | Sinalização explícita; alerta de "baixa adesão à pesquisa interna" separado do alerta de desempenho | Excluir o Bloco A da pontuação e reclassificar, se o NIIMA decidir assim (questão 2 da revisão de 24/09) | Mirella |
| R7 | Equipe de 8 integrantes com disponibilidade desigual no fim do semestre | 3 | 3 | 9 | Cartões do Trello parados mais de uma semana; ausência em tutoria | Sprints quinzenais com planejamento, revisão e retrospectiva registrados; dono por épico | Repriorizar pela ordem do backlog (US07, US09, US11 primeiro); cortar E6 do escopo do final se necessário | Maria Eduarda |

## Projeção de cenários para R1 (atraso no acesso ao dado real)

| Cenário | Probabilidade estimada | O que acontece | Efeito no projeto | Resposta |
|---|---|---|---|---|
| Otimista: middleware disponível até a semana 12 | 20% | Anderson entrega endpoints de leitura dos 3 eixos e das vigências | Troca de `carregar()` em uma sprint; reexecução do pipeline na semana 15 com dados reais, como prevê o LEIA-ME | Rodar o pipeline, comparar o log de qualidade real com o sintético e ajustar tratamentos |
| Provável: dados chegam como extração única (CSV) entre as semanas 13 e 15 | 50% | Sem middleware, mas com uma carga avulsa anonimizada | Pipeline roda igual (a origem já é CSV); sem ingestão diária de NPS (US02) nem vigências (US03) | Entregar o final com a carga avulsa; US02 e US03 ficam como próximos passos documentados para o NIIMA |
| Pessimista: nenhum dado real até o final da disciplina | 30% | Pedido formal não é respondido no semestre | Todo o produto é demonstrado sobre a base sintética | Manter o aviso "DADOS SIMULADOS"; entregar o contrato de API e o pipeline prontos para a troca; registrar o risco materializado na retrospectiva e no relatório final |

Em qualquer cenário, o trabalho técnico não para: a base sintética comum reproduz o esquema e os problemas de uma extração real, e o pipeline foi construído sem supor o tamanho da rede (132 equipes hoje, dimensionado para 300+).

## Revisão

Riscos revisados a cada sprint na reunião de planejamento. Mudança de probabilidade ou impacto é registrada aqui com data.
