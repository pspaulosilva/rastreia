# CLAUDE.md - contexto do repositório RASTRE.IA

Leia este arquivo antes de qualquer alteração.

## O que é

Projeto acadêmico (Equipe 4 · Projeto 5 · Gestão de TI · CESAR School · 2026.2) para o cliente SEAB/NIIMA (Secretaria de Saúde do Recife), desafio Recife Monitora: usar IA para analisar os três pilares do programa (autoavaliação, desempenho assistencial, satisfação do usuário) e gerar alertas de priorização, recomendações por equipe e um chatbot interno (RAG) sobre a base própria.

Nome do produto: RASTRE.IA. Site da equipe: sites.google.com/cesar.school/rastreia/home.

## Estado atual (15/10/2026)

- `pipeline/preparar_dados.py`: pipeline completo sobre a base sintética. `--modo manual` (padrão, v1.1) gera o pacote do mvp5; `--modo dicionario` (v1.0) gera o dos mvp3/mvp4.
- `pipeline/perfilar_base.py`: perfilamento, dispersão e figuras (gera `docs/perfilamento-base.md`).
- `pipeline/verificar_prototipo5.py`: prova de que o Protótipo 5 usa o pipeline v1.1 (ver `docs/explicacao-prototipo-5.md`).
- `app/mvp6.html`: **Protótipo 6, o atual** (https://ratreia.s3.us-east-1.amazonaws.com/mvp6/index.html). Pacote `rastreia_data_v6.json` (`--pacote v6`) com os dois modos; faixa e fonte em toda tela; qualidade com antes/depois; análise exploratória. Toda documentação nova deve citar o protótipo mais recente.
- `app/mvp1.html` a `app/mvp5.html`: protótipos anteriores, HTML único com CSS/JS e dados embutidos em `<script id="rm-data">`. O mvp5 (mostrado no SR1) traz exatamente o `rastreia_data.json` do pipeline; `pipeline/embutir_dados.py` atualiza o bloco.
- Os 5 CSVs da base sintética estão em `data/entrada/`; `data/saida/qualidade_dados.json` versionado.
- `docs/processo/`: backlog, riscos, sprints, ferramentas, pontos fortes. `docs/capturas/`: telas.
- Documentos de referência em `docs/`.

## Regras de negócio obrigatórias

Toda alteração deve preservar estas regras (foram conferidas pelo professor contra a base comum):

1. Bloco A do Eixo 1 só é válido com taxa de resposta >= 30%. Inválido entra como 0 e deve ser sinalizado como "não avaliado", nunca como desempenho ruim.
2. Desclassificação e não participação no ciclo são ausência de dado. Nunca aparecem como zero em séries ou médias.
3. "Maior perda no Eixo 3" é calculada em pontos, usando o peso do indicador para o grupo da equipe, e não pelo menor percentual. IND03 e IND08 (odontologia) não se aplicam ao grupo 4.
4. Zonas de classificação: o pipeline usa as faixas do Manual de Avaliação (900/800/600/400). A base sintética veio com 850/700/550/400 (dicionário). Há protótipos que usam as faixas do dicionário. Divergência em aberto com o professor; sempre registrar qual faixa é usada e a fonte.
5. Limiares, máximos de bloco e pesos por grupo ficam em configuração (constante `PARAMETROS`, por modo), nunca espalhados pelo código.
6. A origem dos dados fica isolada em `carregar()`. O middleware de leitura do cliente, quando existir, substitui só essa função.

## Como rodar

```
pip install -r requirements.txt
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida
```

Saída esperada na base de 24/09: `modo=manual equipes=132 resultados=1363 eixo3=12738 nps=6530 planos=420 problemas_logados=28` (25 tratamentos do SR1 e 3 marcados `desde: "SR2"`, que não entram nos pacotes dos Protótipos 3 a 5).

## Convenções

- Nos protótipos, comparações com limiares usam `pts()` (sem arredondar); `score()` só para exibir.

- Português nos nomes, comentários, commits e documentação.
- Sem caminhos absolutos. Sem passos manuais não registrados. Toda dependência em `requirements.txt`.
- Todo número exibido em tela deve ser rastreável a uma função do pipeline.
- Todo tratamento de dado novo entra no `LOG` com problema, contagem e decisão (e `desde=` quando posterior ao SR1).
- Dados limpos excluem tudo o que a regra de negócio exclui das análises (ex.: Eixo 3 e NPS de ciclos desclassificados).
- Todo `open()` e `to_csv()` com `encoding="utf-8"` (o README precisa rodar no Windows).
- Reuniões e sprints registradas no mesmo dia (`docs/processo/atas/`, `sprints.md`).
- Toda tela derivada da base sintética exibe "DADOS SIMULADOS".
- Não usar travessão ("-") em documentos gerados.

## Pendências priorizadas

1. Faixa oficial (Manual ou dicionário) a definir pelo professor/NIIMA; o mvp6 já mostra as duas.
2. Sprint 1 (`docs/processo/sprints.md`): US07 configuração, US09 PDF, pesquisa de campo, cronograma com status.
3. Sempre que o pipeline mudar: rodar `preparar_dados.py` (modos `manual` e `dicionario`), `perfilar_base.py`, `verificar_prototipo5.py`, `embutir_dados.py` e `capturar_telas.py`, nessa ordem.
