# Backlog do produto: épicos e user stories

RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2. Versão 1.0 · 15/10/2026.

Origem: requisitos RF01 a RF11 do Documento de Requisitos (reunião com o cliente em 10/09/2026) e revisão de 24/09 sobre a base sintética. Personas: Renata (gestora central, NIIMA), Ana Lúcia (gestora distrital), Carlos Eduardo (gestor de unidade) e Anderson (técnico do cliente, responsável pela API).

Prioridade MoSCoW herdada do requisito. Estimativa em pontos (Fibonacci). Status em 15/10: Feito = demonstrado no Protótipo 5 ou 6 sobre a base sintética; Em andamento = parcialmente no protótipo; A fazer = SR2 em diante.

## E1. Ingestão e saneamento dos dados

Objetivo: receber os dados do Recife Monitora sem tocar na plataforma atual e entregá-los limpos, com log de qualidade.

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US01 | Como Anderson, quero que o RASTRE.IA leia os três eixos só pelo middleware de leitura, para que nada seja escrito no banco de produção. | Único ponto de leitura em `carregar()`; sem credencial de escrita; teste de contrato por tabela. | RF01, RNF02 | M | 5 | Em andamento (CSV no lugar do middleware) |
| US02 | Como Renata, quero que o NPS seja ingerido diariamente e os eixos 1 e 3 por quadrimestre, para que os alertas usem dado recente. | Job diário de NPS; job por ciclo dos eixos; data da última carga visível na tela. | RF02 | M | 5 | A fazer |
| US03 | Como Anderson, quero que o histórico de vínculo profissional/INE/equipe tenha datas de vigência, para que a agregação respeite migrações. | Tabela de vigência; NPS contado na equipe do dia da interação; INE migrado inicia nova série. | RF03, D4 | M | 8 | A fazer |
| US04 | Como Renata, quero um pipeline de saneamento reproduzível com log de qualidade por ciclo, para saber sobre que base as conclusões foram tiradas. | `preparar_dados.py` roda com um comando; `qualidade_dados.json` com problema, contagem e decisão; tela "Qualidade dos dados". | RF11, RNF05 | M | 8 | Feito |

## E2. Pontuação, agregação e tendências

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US05 | Como Ana Lúcia, quero ver pontuação e NPS já calculados por equipe, distrito e rede, para comparar o meu distrito com a rede. | Valores idênticos aos do Recife Monitora quando não há migração; agregação por equipe, distrito e rede; normalização por n_profissionais quando população ausente. | RF04, RNF06 | M | 5 | Feito |
| US06 | Como Carlos Eduardo, quero ver a tendência da minha equipe entre ciclos (melhora, piora, estagnação), para saber se o plano de ação está funcionando. | Série de 11 ciclos; ciclos sem participação não aparecem como zero; rótulo de tendência por equipe. | RF10 | S | 3 | Feito |
| US07 | Como Renata, quero que zonas, máximos de bloco e pesos por grupo fiquem em configuração, para ajustar quando o NIIMA decidir sem reescrever código. | Parâmetros em `ZONAS`, `BLOCOS` e tabela de pesos; tela Configurações registra fonte (Manual ou dicionário). | RNF08 | M | 3 | Feito (Protótipo 6) |

## E3. Resumo do quadrimestre

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US08 | Como Renata, quero um resumo do quadrimestre com ranking, maiores quedas e ganhos, equipes em zona crítica e causas de perda por eixo, para preparar a devolutiva aos distritos. | Uma versão por nível de gestão; causas de perda em pontos ponderados pelo grupo; anexa o log de qualidade. | RF05 | M | 8 | Feito (tela); exportação em PDF a fazer |
| US09 | Como Ana Lúcia, quero exportar o resumo em PDF, para anexar ao SEI e enviar às unidades. | Botão de exportação; PDF com aviso de dados simulados enquanto a base for sintética. | RF05 | M | 3 | Feito (Protótipo 8, impressão do navegador) |

## E4. Alertas de priorização

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US10 | Como Ana Lúcia, quero alertas classificados por severidade segundo critérios validados pelo NIIMA, para agir primeiro onde é urgente. | Critérios: zona crítica, queda >= 60 pontos, não participação, Bloco A inválido, NPS negativo em atributo; severidade considera porte e histórico. | RF06 | M | 8 | Feito (critérios); validação do NIIMA a fazer |
| US11 | Como Carlos Eduardo, quero receber alertas por e-mail institucional, para não depender de abrir o painel. | Envio no fechamento do ciclo e no job diário de NPS; registro de envio. | RF06 | M | 5 | A fazer |
| US12 | Como Ana Lúcia, quero alertas em grupo de WhatsApp e incidentes críticos por Telegram, para alcançar as equipes no canal que já usam. | Condicionado ao aval institucional dos canais. | RF07 | S / C | 5 | A fazer |

## E5. Recomendações e plano de ação

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US13 | Como Carlos Eduardo, quero saber onde a minha equipe perdeu pontos e o que fazer, com a fonte citada, para montar o plano de ação. | Diagnóstico por indicador aplicável ao grupo e por atributo do NPS; cada ação cita quadro do Manual ou indicador. | RF08 | S | 8 | Feito |
| US14 | Como Carlos Eduardo, quero que o assistente avalie o rascunho do meu plano de ação em governança, SMART e viabilidade e sugira a reescrita, para sair de "Ajustes" e "Reformulação". | Nota nas 3 dimensões; sugestão de reescrita; usa os 420 planos históricos como referência. | RF08 | S | 8 | Em andamento |

## E6. Assistente interno (chatbot RAG)

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US15 | Como Renata, quero perguntar em linguagem natural sobre manuais e resultados e receber resposta com fonte, para não abrir planilhas. | Respostas só da base interna; fonte citada; respeita perfil de acesso (local, distrital, central). | RF09, RNF01 | S | 13 | Em andamento (respostas roteirizadas no protótipo) |
| US16 | Como Renata, quero que a IA rode em servidor próprio com GPU, sem chamadas externas, para cumprir a LGPD e ter custo previsível. | Modelo local quantizado; sem API externa; estimativa de hardware apresentada ao cliente. | RNF01, RNF04, RNF05 | M | 13 | A fazer |

## E7. Feedback do cliente (16/11/2026)

Origem: feedback do cliente sobre o Protótipo 6.

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US17 | Como Ana Lúcia, quero enviar pelo assistente um feedback a uma unidade, para devolver o diagnóstico sem sair do RASTRE.IA. | Ação em respostas sobre equipe e pedido em texto; texto sugerido com pontuação e recomendações com fonte, editável; canal e-mail institucional ou SEI; histórico por unidade; respeita o perfil. | RF06, RF09 | S | 5 | Feito (Protótipo 7, envio simulado) |
| US18 | Como Ana Lúcia, quero agendar a visita técnica de um alerta, registrar observações e anexar o relatório da visita, e filtrar os alertas por situação e data, para acompanhar o que já foi encaminhado. | Situação, data da visita, responsável, observações com autor e data, anexo, histórico; filtros por severidade, situação, agendamento, distrito e texto; atrasadas destacadas; exportação CSV. | RF06 | M | 8 | Feito (Protótipo 7, dados no navegador) |
| US19 | Como Renata, quero registrar feedback e marcar um ponto da tela, inclusive nas respostas da IA, para a equipe RASTRE.IA saber exatamente o que ajustar. | Botão em todas as telas; tipo e texto; marcação opcional exibida sobre a tela; 👍/👎 e comentário por resposta do assistente; situação do feedback. | RNF05 | S | 5 | Feito (Protótipo 7) |
| US20 | Como equipe RASTRE.IA, queremos medir o uso do app (telas, tempo, cliques, perguntas) num painel interno, para priorizar a próxima versão. | Registro de telas, tempo por tela, cliques, perguntas e envios; painel interno com período; exportação; registro desligável. Em produção, gravação na API interna com trilha de auditoria. | RNF05 | S | 8 | Em andamento (painel no Protótipo 7; dados por navegador até existir a API) |

## E8. Revisão de design e UX (16/11/2026)

Origem: revisão de design e UX do Protótipo 7, aprovada pelo cliente.

| ID | User story | Critérios de aceite | RF | Pri. | Pts | Status |
|---|---|---|---|---|---|---|
| US21 | Como Ana Lúcia, quero ver juntos os alertas da mesma equipe e marcar uma visita única para todos, para não agendar duas visitas no mesmo lugar. | Grupo por equipe com severidade mais alta, contagem e próxima visita; visita única grava data e responsável em todos os alertas abertos; opção de lista simples; aviso de visita já marcada na janela de acompanhamento. | RF06 | S | 5 | Feito (Protótipo 8) |
| US22 | Como Ana Lúcia, quero registrar o que resolveu um alerta ao tratá-lo, para ter histórico na devolutiva. | Pergunta ao tratar, com respostas prontas e texto livre; nota no alerta, no histórico e no CSV; tratar sem nota permitido. | RF06 | S | 2 | Feito (Protótipo 8) |
| US23 | Como Ana Lúcia, quero uma agenda das visitas técnicas por semana, para planejar os deslocamentos. | Uma visita por equipe e data; atrasadas, esta semana, próxima semana e depois; aviso de críticos sem visita; exportação `.ics`. | RF06 | S | 5 | Feito (Protótipo 8) |
| US24 | Como Renata, quero buscar e filtrar os planos de ação por maturidade, ciclo e distrito, para achar os que precisam de reformulação. | Cartões de contagem que filtram; busca por equipe, unidade ou texto; filtro de ciclo e distrito; paginação; CSV do filtro. | RF08 | S | 3 | Feito (Protótipo 8) |
| US25 | Como Carlos Eduardo, quero ver no topo da página da equipe a situação, a maior perda e a próxima ação, para entender o essencial sem rolar a página. | Resumo com três blocos; atalhos para as seções; botão para o acompanhamento do alerta aberto. | RF04 | S | 3 | Feito (Protótipo 8) |
| US26 | Como qualquer usuário, quero cabeçalho enxuto, texto legível, uso por teclado e orientação na primeira visita, para usar o RASTRE.IA sem treinamento. | Faixas só em Configurações (selo no título apenas fora do padrão); três ações fixas nos alertas; contraste AA em texto cinza e links; alertas e tabelas por Tab e Enter; primeiros passos por perfil com andamento; números do Painel com detalhamento do cálculo; perguntas sugeridas em uma linha. | RNF05 | S | 5 | Feito (Protótipo 8) |

## Resumo

| Épico | Stories | Pontos | Feito | Em andamento | A fazer |
|---|---|---|---|---|---|
| E1 Ingestão e saneamento | 4 | 26 | 1 | 1 | 2 |
| E2 Pontuação e tendências | 3 | 11 | 3 | 0 | 0 |
| E3 Resumo do quadrimestre | 2 | 11 | 2 | 0 | 0 |
| E4 Alertas | 3 | 18 | 1 | 0 | 2 |
| E5 Recomendações | 2 | 16 | 1 | 1 | 0 |
| E6 Assistente | 2 | 26 | 0 | 1 | 1 |
| E7 Feedback do cliente | 4 | 26 | 3 | 1 | 0 |
| E8 Revisão de design e UX | 6 | 23 | 6 | 0 | 0 |
| Total | 26 | 157 | 17 | 4 | 5 |

Ordem para o SR2: US09, US11, US14, US03, US15. Quadro no Trello espelha este arquivo (uma lista por épico, um cartão por story).
