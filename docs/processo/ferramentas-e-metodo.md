# Justificativa das ferramentas e do método

RASTRE.IA · Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2. Versão 1.0 · 15/10/2026.

## Método: Duplo Diamante (Design Thinking)

Por que: o desafio chegou como problema aberto ("transformar os dados que já temos em informação para decisão"), não como especificação. O Duplo Diamante separa entender o problema de construir a solução, com divergência e convergência em cada metade, e isso casou com o roteiro da disciplina (imersão, ideação, prototipação, status reports).

Como foi aplicado:

| Fase | Divergir | Convergir | Evidência |
|---|---|---|---|
| Descobrir | Mapa de stakeholders, mapa de empatia, benchmark com 7 referências, revisão de literatura | Matriz CSD, SWOT | Pasta Imersão; site da equipe |
| Definir | Reunião de imersão com o cliente (10/09): 9 questões, 4 decisões | Hipótese de Solução, 3 personas (uma por nível de gestão), Documento de Requisitos RF01 a RF10 | `docs/requisitos.md` |
| Desenvolver | Brainstorming (25 ideias em 4 temas), brainwriting (3 rodadas), SCAMPER, Crazy 8's de 4 integrantes | Tabela de Convergência com critérios explícitos; 3 módulos (alertas, recomendações, assistente) mais o módulo de saneamento que surgiu dos dados | Pasta Ideação |
| Entregar | 6 protótipos incrementais (mvp1 a mvp6) | Protótipo 5 demonstrado no SR1; Protótipo 6 com os ajustes da devolutiva | `app/` |

Alternativas consideradas: Scrum puro (descartado como método principal porque não cobre a fase de descoberta; adotado como cadência de execução dentro do segundo diamante, com sprints quinzenais) e CRISP-DM (adotado para a trilha de dados, conforme o LEIA-ME da base, dentro das fases Definir e Desenvolver).

## Ferramentas

| Ferramenta | Finalidade | Por que esta e não outra | Limite conhecido |
|---|---|---|---|
| Trello | Backlog e acompanhamento das sprints | Gratuito, sem curva de aprendizado para 8 integrantes de perfis diferentes (gestão, design, dados); quadro por épico espelha `docs/processo/backlog.md`; integra com Google Drive | Não gera burndown nem liga cartões ao cronograma; por isso o registro de sprint fica em `docs/processo/sprints.md` |
| FigJam | Oficinas de ideação (brainwriting, Crazy 8's, Tabela de Convergência) e mapa de stakeholders | Quadro infinito com templates prontos para as dinâmicas; permitiu rodar o Crazy 8's de forma assíncrona, com cada integrante postando no seu horário; mesma conta da equipe no Figma usada para a identidade visual | Export para o Drive é manual (PDF/PNG); feito a pedido do professor |
| Google Sites | Site público do projeto, exigido pela disciplina | Hospedagem na conta institucional cesar.school, sem custo nem manutenção; edição por qualquer integrante; publica o processo de Design Thinking para o cliente e o professor | Não hospeda aplicação; o protótipo fica no S3 e é linkado |
| AWS S3 (bucket `ratreia`, us-east-1) | Hospedagem dos 6 protótipos (HTML único com dados embutidos) | Arquivo estático servido com leitura pública, sem servidor nem build; versionamento por pasta (mvp1 a mvp6) preserva cada entrega; custo próximo de zero para 4 MB | Sem HTTPS em domínio próprio e sem controle de acesso; aceitável para base sintética, inadequado para dados reais (RNF05) |
| GitHub (`pspaulosilva/rastreia`) | Código do pipeline, protótipos, documentação e capturas | Repositório público ligado ao site; exigência de Reprodutibilidade e Documentação da rubrica; histórico de versões dos dados e das decisões | Criado em 15/10, após o SR1; o histórico anterior está no Drive |
| Python (pandas, numpy, matplotlib, Playwright) | Pipeline de saneamento, perfilamento, figuras e capturas | Padrão em ciência de dados; reexecutável com um comando; mesma linguagem do futuro serviço de IA | Sem notebook: optou-se por scripts para evitar estado oculto e caminhos absolutos |
| Google Drive | Pasta de entrega avaliada pelo professor | Exigência da disciplina; conta institucional | Links externos (Trello, FigJam, site) exportados para a pasta como evidência estática |
| Claude (Cowork e Claude Code) | Apoio à redação, revisão de documentos e ao trabalho no repositório | Acelera documentação e conferência de números; contexto do projeto registrado em `CLAUDE.md` | Toda saída é revisada pela equipe; nenhum dado real passa por IA externa (RNF01) |

## Entradas e saídas por fase

| Fase | Entradas | Saídas |
|---|---|---|
| Descobrir (semanas 1 a 4) | Briefing do desafio, manuais do Recife Monitora, artigos | Mapa de stakeholders, mapa de empatia, benchmark, matriz CSD, SWOT |
| Definir (semanas 4 a 6) | Reunião com o cliente (10/09), matriz CSD | Hipótese de Solução, personas, Documento de Requisitos, decisões D1 a D4 |
| Desenvolver (semanas 6 a 9) | Requisitos, base sintética (LEIA-ME, dicionário, 5 CSVs) | Ideias convergidas, pipeline de dados, log de qualidade, protótipos 1 a 5 |
| Entregar (SR1, 24/09, e SR2) | Protótipo 5, deck | Apresentação do SR1, devolutiva, backlog e riscos revisados, repositório |
