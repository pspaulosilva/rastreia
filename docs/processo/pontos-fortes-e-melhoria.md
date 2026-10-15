# Pontos fortes e pontos de melhoria da equipe

RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2. Versão 1.0 · 15/10/2026. Cada item tem justificativa própria, ligada a um fato do projeto. Substitui os textos repetidos apontados na devolutiva do SR1.

## Pontos fortes

| Ponto forte | Justificativa com fato do projeto |
|---|---|
| Adaptação a imprevistos | A base sintética chegou dias antes do SR1 de 24/09 com 25 problemas de extração (ciclo em 4 formatos, 13 INEs sem cadastro, pontuações de 9999). Em vez de adiar o protótipo, a equipe escreveu o pipeline de saneamento, logou cada tratamento e demonstrou o MVP rodando sobre a base comum na própria apresentação. |
| Colaboração | O Crazy 8's foi feito de forma assíncrona no FigJam por 4 integrantes em horários diferentes e consolidado na Tabela de Convergência; a reunião com o cliente em 10/09 foi conduzida por uma dupla e registrada em ata por outra, de modo que os 8 integrantes tiveram acesso às mesmas 9 questões e 4 decisões. |
| Rigor técnico nas regras de negócio | Fomos a única equipe a aplicar a regra dos pesos do Eixo 3 por grupo (maior perda em pontos, não em percentual) e as faixas de zona do dicionário em telas conferidas número a número pelo professor nos Protótipos 3 e 4. |
| Identidade visual consistente | Deck, site e os 5 protótipos usam o mesmo sistema (nome RASTRE.IA, paleta e tipografia definidas no Figma), o que o professor registrou como ponto positivo no SR1. |
| Qualidade das análises e ideias | A ideação produziu 25 ideias em 4 temas, 3 rodadas de brainwriting e SCAMPER, e a análise dos dados revelou um módulo não previsto (M0, saneamento e qualidade), incorporado à solução. |

## Pontos de melhoria

| Ponto de melhoria | Justificativa com fato do projeto | Ação para o SR2 |
|---|---|---|
| Gestão de tempo | O cronograma entregue no SR1 não foi atualizado: ideação e prototipação apareciam como futuras quando já estavam prontas, e o Trello só tinha cartões do Kickoff e da imersão inicial. | Cronograma com coluna de status e datas realizadas, revisado a cada sprint; Trello espelha o backlog por épico. |
| Priorização | A trilha de dados (acesso, entendimento, limpeza, EDA) não entrou no cronograma, embora tenha consumido a maior parte do esforço técnico antes do SR1. | Trilha de dados como épico E1 com datas; CRISP-DM alinhado às semanas 5 a 7 do roteiro. |
| Documentação do que foi feito | O código do pipeline, o log de qualidade e a tela "Qualidade dos dados" existiam em 24/09, mas não estavam no Drive; a nota de Dados ficou condicional por isso. | Repositório GitHub ligado ao site; toda entrega técnica sobe no Drive no mesmo dia da apresentação. |
| Controle de versão dos dados | O Protótipo 5 usou o pipeline v1.1 (realinhado ao Manual) e os Protótipos 3 e 4 a v1.0, sem que a diferença fosse registrada; o professor não conseguiu reproduzir os números. | Cada tela registra a faixa e os máximos usados com a fonte; `rastreia_data.json` versionado com a data de geração; `verificar_prototipo5.py` como teste de regressão. |
| Pesquisa de campo | Observação de campo, questionário com equipes e jornada do usuário estavam planejados até o SR1 e não foram registrados. | Realizar e registrar até o SR2, ou repactuar no cronograma com o motivo. |
