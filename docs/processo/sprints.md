# Registro de sprints

RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2. Ligado ao cronograma (aba "Revisado 15/10 (SR2)") e ao backlog (`backlog.md`). Sprints quinzenais a partir de 15/10/2026, cada uma com planejamento, revisão e retrospectiva.

## Trabalho retroativo (17/08 a 24/09)

Reconstruído em 15/10 a partir do quadro Trello da equipe ([Projeto 5 · Grupo 4](https://trello.com/b/F49bv4up/projeto-5-grupo-4)) e da coluna "Realizado em" do cronograma. Nesse período a equipe trabalhou por fase do Duplo Diamante, sem cerimônias de sprint registradas; os blocos abaixo agrupam o que foi feito em ciclos de duas semanas, nas semanas do cronograma.

Situação do Trello: o quadro foi criado em 27/08 com as listas Metodologia Scrum, Próximos passos, Em andamento e Entregue; tem 9 cartões e 55 ações, todas entre 27/08 e 31/08. Depois do Kickoff não houve novos cartões, por isso as fases seguintes se apoiam no cronograma e nos documentos do repositório (ver Gestão de tempo em `pontos-fortes-e-melhoria.md`).

### Ciclo R1: 17/08 a 28/08 (S1 e S2) · Kickoff

Objetivo: alinhar escopo e método e preparar a entrega 1 (Kickoff).

| Entrega (cartão do Trello) | Responsáveis no cartão | Situação no Trello |
|---|---|---|
| Metodologia: Scrum escolhido para gerenciar o projeto | (sem responsável) | Lista Metodologia Scrum, 27/08 |
| Cronograma | Duda, Mirella | Entregue, concluído em 27/08 |
| Ciclo de vida | Mirella | Entregue, concluído em 27/08 |
| Artigos de pesquisa | Duda | Entregue, concluído em 27/08 |
| Público-alvo | Paulo | Entregue, concluído em 27/08 |
| Persona | Paulo | Entregue, concluído em 27/08 |
| Mapa de empatia | Paulo | Entregue, concluído em 27/08 |
| Hipóteses de solução | Paulo, Mirella | Entregue, concluído em 27/08 |
| Slide do Kickoff | Paulo, Lorena, Mirella | Em andamento em 27/08; Entregue em 31/08 |

Revisão: Kickoff apresentado em S1 a S2 (cronograma: concluído). Retrospectiva (registrada agora): o quadro funcionou para a entrega do Kickoff, mas não foi mantido nas fases seguintes.

### Ciclo R2: 31/08 a 11/09 (S3 e S4) · Imersão

Objetivo: entender o problema com o cliente e a literatura.

| Entrega | Evidência | Data |
|---|---|---|
| Pesquisa documental e benchmarking | Benchmark com 7 referências; revisão de literatura com 5 artigos | até 24/09 |
| Reunião de imersão com o cliente (9 questões, 4 decisões) | `docs/requisitos.md` | 10/09 |
| Consolidação da imersão | Matriz CSD e Hipótese de Solução | até 24/09 |

Não realizado e repactuado: observação de campo, questionário com equipes e entrevistas com gestores distritais e locais (Sprint 1).

### Ciclo R3: 14/09 a 25/09 (S5 e S6) · Definição, ideação, prototipação e SR1

Objetivo: chegar ao SR1 de 24/09 com diagnóstico, conceito e MVP sobre a base comum.

| Entrega | Evidência | Data |
|---|---|---|
| Personas (3, uma por nível de gestão) e mapa de stakeholders | Material do SR1 | até 24/09 |
| Ideação: 25 ideias, brainwriting, SCAMPER, Crazy 8's no FigJam | Tabela de Convergência | até 24/09 |
| Conceito (módulos M0 a M3) e arquitetura | `docs/revisao-dados-sinteticos-e-arquitetura.md` | 24/09 |
| Protótipos 1 e 2 (baixa fidelidade) | `app/mvp1.html`, `app/mvp2.html` | até 24/09 |
| Base sintética: pipeline de saneamento com 25 problemas logados | `pipeline/preparar_dados.py`, `data/saida/qualidade_dados.json` | até 24/09 |
| Protótipos 3 a 5 sobre a base comum | `app/mvp3.html` a `app/mvp5.html` | 24/09 |
| Entrega SR1 | Apresentação de 24/09 | 24/09 |

Revisão: SR1 apresentado; a devolutiva deixou a nota de Dados condicional ao código, à tela de qualidade e à explicação do Protótipo 5. Retrospectiva (registrada agora): o esforço técnico foi para a base e o MVP, e nem o Trello nem o cronograma acompanharam; affinity mapping, matriz de dores x oportunidades e jornada ficaram para depois.

## Sprint 0 (retroativa): 25/09 a 15/10 · Janela do SR1

Objetivo: cumprir a condição da nota de Dados e os itens recuperáveis da devolutiva.

Planejamento (25/09): entregar código reexecutável, tela "Qualidade dos dados", explicação do Protótipo 5, perfilamento, backlog, riscos, justificativas.

Revisão (15/10): entregue no repositório `pspaulosilva/rastreia` e no Drive. Pipeline reexecutado do zero com as contagens esperadas; pacote embutido no Protótipo 5 idêntico ao gerado pelo pipeline; capturas dos Protótipos 3, 5 e 6 geradas por script; Protótipo 6 publicado com os ajustes da devolutiva.

Retrospectiva: o que faltou no SR1 já existia, mas não estava na pasta. Acordo: nenhuma apresentação sem o material técnico no Drive no mesmo dia.

## Sprint 1: 16/10 a 29/10

Objetivo: fechar a divergência de faixas e preparar a troca da fonte de dados.

| Story | Dono | Critério de pronto |
|---|---|---|
| US07 parâmetros em configuração com fonte registrada | Paulo | Tela Configurações mostra faixa e máximos usados e a fonte |
| US09 exportação do resumo em PDF | Pedro | PDF gerado a partir do Protótipo 6 com aviso de dados simulados |
| Pesquisa de campo: questionário e jornada | Mirella, Lorena | Questionário aplicado ou repactuação registrada no cronograma |
| Cronograma com trilha de dados e status | Maria Eduarda | Coluna de status e datas realizadas preenchidas |

Revisão: (preencher em 29/10)

Retrospectiva: (preencher em 29/10)

## Sprint 2: 30/10 a 12/11

Objetivo: alertas por e-mail e assistente de plano de ação.

| Story | Dono |
|---|---|
| US11 alertas por e-mail institucional | Davi |
| US14 assistente de plano de ação (governança, SMART, viabilidade) | Bruna, Matheus |
| US03 tabela de vigência profissional/INE/equipe | Davi |

## Modelo para as próximas sprints

Planejamento: stories escolhidas pela ordem do backlog, dono e critério de pronto. Revisão: o que foi demonstrado, com link para o commit ou captura. Retrospectiva: manter, parar, começar. Riscos revisados na mesma reunião (`riscos.md`).
