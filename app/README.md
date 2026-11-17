# MVP / protótipos RASTRE.IA

Oito versões do protótipo; a versão atual é o **Protótipo 8** (`mvp8.html`). Cada uma é um único arquivo HTML (CSS e JS embutidos; a única
dependência externa é a fonte do Google Fonts, opcional). Publicados em
`s3://ratreia/mvpN/index.html` (us-east-1, leitura pública) e versionados aqui.

| Arquivo | Versão | Dados | Zonas / blocos do Eixo 1 |
|---|---|---|---|
| `mvp1.html` | Protótipo 1 | exemplo ilustrativo, sem a base comum | faixas do Manual de Avaliação |
| `mvp2.html` | Protótipo 2 | exemplo ilustrativo, sem a base comum | faixas do Manual de Avaliação |
| `mvp3.html` | Protótipo 3 | base comum, pipeline v1.0 (só limpeza), em `<script id="rm-data">` | 850/700/550/400 e A80/B60/C60 (dicionário da base) |
| `mvp4.html` | Protótipo 4 | base comum, pipeline v1.0 | idem |
| `mvp5.html` | Protótipo 5 (apresentado no SR1, 24/09) | base comum, pipeline v1.1 (realinhado ao Manual) | 900/800/600/400 e A40/B80/C80 (Manual) |
| `mvp6.html` | Protótipo 6 (15/10) | base comum, `preparar_dados.py --pacote v6`: os dois conjuntos de parâmetros no mesmo pacote | Manual por padrão; Dicionário em Configurações ou `?faixas=dicionario` |

| `mvp7.html` | Protótipo 7 (16/11) | mesmo pacote do Protótipo 6 (`--pacote v6`) | idem |
| **`mvp8.html`** | **Protótipo 8 (atual, 16/11)** | mesmo pacote do Protótipo 6 (`--pacote v6`) | idem |

## Protótipo 8: revisão de design e UX

Feito sobre o Protótipo 7, com o mesmo pacote de dados (`embutir_dados.py --verificar` dá "iguais") e a mesma persistência (`rastreia.v7` no `localStorage`, então o que foi registrado no Protótipo 7 continua visível).

- Alertas agrupados por equipe: os alertas da mesma equipe aparecem juntos, com a severidade mais alta, a contagem e a próxima visita no cabeçalho do grupo. "Agendar visita única" grava a mesma data e o mesmo responsável em todos os alertas abertos da equipe. A caixa "Agrupar por equipe" volta à lista simples. Na janela de acompanhamento, se outro alerta da equipe já tem visita, aparece o atalho "Usar a mesma data".
- Nota de resolução: "Marcar como tratado" (no menu do alerta ou na janela de acompanhamento) pergunta o que resolveu, com respostas prontas e texto livre; a nota aparece no alerta tratado, no histórico e na coluna `resolucao` do CSV. "Tratar sem nota" continua disponível.
- Agenda de visitas: alternador Lista/Agenda na tela de Alertas. A agenda mostra uma visita por equipe e data, em Atrasadas, Esta semana, Próxima semana e Depois, avisa quantas equipes com alerta crítico ainda não têm visita e exporta as visitas em `.ics` (Outlook, Google Agenda, celular).
- Cabeçalho: a linha "Faixas do Manual: ... · trocar", que se repetia abaixo do título, saiu das telas. As faixas em uso ficam em Configurações; um selo ao lado do título só aparece quando as faixas diferem do padrão (Manual), com o texto completo na dica e clique para Configurações. No celular, os filtros do cabeçalho rolam na horizontal em vez de quebrar em várias linhas.
- Página da equipe: resumo no topo com situação, maior perda e próxima ação (o alerta aberto mais urgente ou a primeira recomendação) e atalhos para Evolução, Eixos, Recomendações e Planos de ação.
- Planos de ação: cartões Todos, Reformulação, Ajustes, Aprovados e Sem texto que filtram a lista; busca por equipe, unidade ou trecho do plano; filtro de ciclo (e de distrito no perfil central); lista em páginas de 20; o CSV exporta o filtro atual.
- Resumo do quadrimestre: "Exportar PDF" abre a impressão do navegador com folha de estilo própria (A4, sem menu nem botões, tema claro, ranking completo). Atende à US09 sem servidor; o envio por e-mail segue simulado.
- Assistente: depois da primeira pergunta, as perguntas sugeridas ficam em uma linha com rolagem lateral (no celular, sempre). Ícones no lugar dos emojis de avaliação e de privacidade.
- Acessibilidade: texto cinza e links pequenos com contraste AA (4,5:1 ou mais nos temas claro e escuro); alertas e linhas de tabela alcançáveis por Tab e abertos com Enter; foco visível. Fundos azuis com texto branco usam um tom mais escuro (#4666E6, 4,9:1); selos de faixa, severidade e maturidade com texto mais escuro no tema claro; contador de alertas e marcador de feedback com tinta escura no tema escuro.
- Primeiros passos: cartão no topo do Painel, por perfil, com 4 passos do ciclo na ordem recomendada, barra de andamento e um botão por passo (o próximo passo em destaque). O andamento é calculado com o que já existe: visitas marcadas nos alertas críticos, feedbacks enviados nos alertas de queda, Bloco A e sem dados, alertas pendentes da unidade; passos sem dado próprio (planos, resumo, assistente, distritos) contam como feitos ao serem abertos. Distrital: visitas, feedback, planos para reformular, resumo do quadrimestre. Local: onde a equipe perdeu pontos, alertas, plano de ação, assistente. Central: visitas na rede, feedback, comparação de distritos, resumo. "Recolher" deixa uma linha com o próximo passo; o cartão some quando todos estão feitos e recolhidos.
- Números do Painel clicáveis: cada cartão (pontuação média, participação, abaixo do limite crítico, quedas de 60+, alertas abertos) abre "Como chegamos a este número", com o cálculo passo a passo, as regras aplicadas (ausência de dado fora da média, pontuação sem arredondar, base de comparação), a composição (média por eixo, equipes por zona, entradas e saídas da zona crítica, alertas por tipo) e a lista de equipes que formam o número, cada uma abrindo a página da equipe.
- Primeira visita: dica dispensável na tela de Alertas; estados vazios com orientação.
- Ações dos alertas: o botão principal tem só três rótulos, um por ação: "Enviar feedback" (sem dados, queda forte, Bloco A inválido), "Agendar visita", que vira "Registrar visita" depois de agendada (zona crítica), e "Abrir equipe" (queda moderada, NPS negativo). A recomendação de cada tipo aparece como linha "Recomendado: ..." no alerta aberto. O antigo botão "Acompanhar" saiu: o acompanhamento abre pelo clique na linha ou por "Mais ações".
- Correções: variação de pontos nos títulos dos alertas com vírgula decimal; espaço no fim da página para o botão Feedback não cobrir conteúdo.

## Protótipo 7: feedback do cliente

Feito sobre o Protótipo 6, com o mesmo pacote de dados (`embutir_dados.py --verificar` dá "iguais").

- Alertas: botão Acompanhar abre o acompanhamento do alerta com situação (aberto, agendado, em andamento, tratado, adiado), data da visita técnica, responsável, observações com autor e data, anexo do relatório de visita técnica e histórico. A ação "Agendar visita técnica" abre direto na data.
- Alertas: cartões de acompanhamento (pendentes, agendadas, próximos 7 dias, atrasadas, tratados) que filtram a lista; filtros por severidade, situação, visita técnica, distrito (perfil central) e busca em unidade, responsável e observações; ordenação por urgência ou data da visita; exportação CSV.
- Feedback à unidade: no Assistente (botão no topo, ação em toda resposta sobre uma equipe e pedido em texto, ex.: "Enviar feedback à eSF Engenho do Meio"), no acompanhamento do alerta, nas ações "Contatar unidade" e "Enviar recomendações" e na página da equipe. Texto sugerido com pontuação e recomendações com fonte, editável; canal e-mail institucional ou SEI (WhatsApp sob aprovação); histórico de envios por unidade. Envio simulado.
- Feedback das telas: botão Feedback em todas as telas (sugestão, problema, elogio, dúvida) com marcação opcional de um ponto da tela; as marcações aparecem numeradas sobre a tela. No Assistente, cada resposta tem 👍/👎 e comentário.
- Uso e feedback (painel interno, `?interno=1` ou Configurações): sessões, telas vistas e tempo médio, cliques mais frequentes, uso por dia e por perfil, perguntas e avaliações do assistente, feedbacks com situação (novo, em análise, resolvido, descartado) e "Ver na tela", envios às unidades, exportação JSON e CSV.
- Persistência isolada em `lerStore()`/`salvarStore()` e registro de uso em `track()`: no protótipo tudo fica no `localStorage` do navegador (cada navegador tem os próprios dados); em produção só essas funções passam a gravar na API interna. O registro de uso pode ser desligado em Configurações.
- Revisão da tela de Alertas: cada alerta tem uma ação principal (conforme o tipo e o andamento) e o menu "Mais ações"; clicar na linha abre o acompanhamento; o adiamento guarda a data e o alerta volta a pendente depois de 7 dias; lista de 25 em 25; "Limpar filtros" só aparece com filtro ativo.
- Planos de ação: exportação CSV na tela Planos de ação (recorte do perfil) e na página da equipe; a proposta reescrita pela IA pode ser exportada em texto.
- Ícones nos filtros, nas Configurações e nas janelas de feedback e de acompanhamento; seletores com a seta afastada da borda.
- Correção: a recomendação do Bloco A exibia `${BMAX.a}` literal em vez do máximo do bloco.

## Protótipo 6: ajustes pedidos na devolutiva do SR1

- Toda tela registra, abaixo do título, as faixas de zona em uso e a fonte (Manual ou dicionário); máximos de bloco e versão do pipeline aparecem ao passar o mouse. Configurações troca o conjunto e a escolha fica salva.
- No modo Dicionário, os números coincidem com os do Protótipo 3 corrigido (rede em 2026.2: média 677, 16 abaixo de 550, 9 quedas de 60+); no modo Manual, com os do Protótipo 5 (média 681, 27 abaixo de 600).
- Qualidade dos dados: contagem antes e depois de cada tratamento, situação (corrigido, mantido e sinalizado, conferido), tipo, volume antes e depois por tabela com unicidade da chave, filtro por tabela e exportação do log em JSON.
- Nova tela Análise exploratória (perfis central e distrital): medidas de posição e dispersão, completude da base crua e gráficos interativos. Histograma com escolha da variável e da largura da faixa (clique na barra lista as equipes); boxplot por distrito, grupo ou tipo de equipe (clique na caixa lista as equipes, outliers abrem a equipe); dispersão com eixos à escolha, linha de tendência e zonas que se escondem pela legenda. Dica com os valores ao passar o mouse. Cada análise tem o botão "Interpretar com IA", que escreve o que se pode inferir e o próximo passo a partir das estatísticas do recorte e dos filtros em uso (gerado no próprio navegador, sem IA externa, como o Assistente).
- Comparações com limiares sem arredondamento; cartão de quedas compara com o ciclo anterior.

`mvp3` a `mvp8` trazem o aviso "DADOS SIMULADOS", perfis de acesso (central, distrital,
local), alertas, planos de ação, resumo do quadrimestre, assistente e a tela "Qualidade dos
dados" (perfis central e distrital).

## Rodar

Abrir o arquivo no navegador ou, da raiz do repositório:

```bash
python3 -m http.server 8080 --directory app
# http://localhost:8080/mvp5.html
```

## Reexecutar o pipeline e atualizar o protótipo

```bash
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida
python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json --verificar   # imprime "iguais"
# Protótipos 6, 7 e 8 (atual): pacote com os dois modos
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida --pacote v6
python pipeline/embutir_dados.py --html app/mvp6.html --dados data/saida/rastreia_data_v6.json --verificar   # "iguais"
python pipeline/embutir_dados.py --html app/mvp7.html --dados data/saida/rastreia_data_v6.json --verificar   # "iguais"
python pipeline/embutir_dados.py --html app/mvp8.html --dados data/saida/rastreia_data_v6.json --verificar   # "iguais"
# Protótipos 3 e 4 (pipeline v1.0, parâmetros do dicionário)
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida-dicionario --modo dicionario
python pipeline/embutir_dados.py --html app/mvp3.html --dados data/saida-dicionario/rastreia_data.json --verificar   # "iguais"
python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json             # grava o pacote novo
```

Correção de 15/10 (mvp3 a mvp5): comparações com limiares (zona, abaixo de 550/600, queda de 60) passaram a usar a pontuação sem arredondar (`pts()`); `score()` arredonda só para exibir. O cartão "Quedas de 60+ pontos" compara com o ciclo imediatamente anterior (equipe que não participou dele não conta como queda). No Protótipo 3, perfil central: 16 abaixo de 550 (antes 15, a equipe com 549,9 era arredondada para 550) e 9 quedas (antes 10). No Protótipo 5 nada muda (27 abaixo de 600).

O pacote embutido em `mvp5.html` é idêntico ao que `preparar_dados.py` gera hoje a partir
dos CSVs de `data/entrada/` (conferido com `--verificar`). Os números das telas são,
portanto, rastreáveis até o script.

## Capturas

`python pipeline/capturar_telas.py --tela qualidade --prototipos 6` gera
`docs/capturas/prototipoN-qualidade.png` com Chromium (Playwright). Outras telas:
`painel`, `alertas`, `planos`, `resumo`, `chat`, `analise`, `config`. Todas as do Protótipo 6 já estão em `docs/capturas/`
(`--sufixo=-dicionario --query "?faixas=dicionario"` captura no modo dicionário).
