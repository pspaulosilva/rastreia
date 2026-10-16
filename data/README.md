# Dados

`data/entrada/` contém os 5 CSVs da base sintética comum entregue pelo professor
para o SR1 (`equipes.csv`, `resultados_ciclos.csv`, `eixo3_indicadores.csv`,
`nps_atributos.csv`, `planos_acao.csv`). LEIA-ME e dicionário em `docs/`.

`data/saida/qualidade_dados.json` é versionado (log dos 28 tratamentos, 25 do SR1 e 3 marcados `desde: "SR2"`, com contagem antes em `linhas` e depois em `depois`). `rastreia_data_v6.json` (pacote do Protótipo 6) é gerado com `--pacote v6`. As demais
saídas (`limpo/`, `rastreia_data.json`) são geradas pelo pipeline e não versionadas.

## Para rodar o pipeline

1. Rode (ver `README.md` da raiz):
   ```
   python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida
   ```
2. As saídas aparecem em `data/saida/`: `limpo/*.csv`, `qualidade_dados.json`,
   `rastreia_data.json`.

Nenhum valor da base corresponde a equipes ou resultados reais (base 100%
sintética, conforme LEIA-ME do cliente).
