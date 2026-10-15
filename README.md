# RASTRE.IA

Equipe 4 · Projeto 5 · Gestão de TI · CESAR School · 2026.2 · Desafio Recife Monitora.

Pipeline de saneamento e preparação da base sintética do Recife Monitora, e
documentação da análise que gera os números exibidos nos protótipos.

Base 100% sintética: nenhum valor corresponde a equipes ou resultados reais.

## Estrutura

```
pipeline/preparar_dados.py       script da análise: limpeza, regras de negócio e pacote do protótipo
pipeline/perfilar_base.py        perfilamento escrito, medidas de dispersão e figuras exploratórias
pipeline/verificar_prototipo5.py conferência dos números do Protótipo 5 contra a base comum
pipeline/embutir_dados.py        injeta rastreia_data.json no protótipo (fecha o ciclo pipeline -> tela)
pipeline/capturar_telas.py       capturas das telas dos protótipos com Chromium
app/                             os 6 protótipos; o atual é app/mvp6.html (Protótipo 6); ver app/README.md
data/                            entrada e saída do pipeline (CSVs da base comum versionados; ver data/README.md)
docs/                            documentação; docs/processo/ (backlog, riscos, sprints, ferramentas); docs/capturas/
requirements.txt                 dependências Python
```

## O que o pipeline faz

Lê os 5 CSVs da base sintética do cliente, aplica a limpeza e as regras de
negócio descritas em `docs/revisao-dados-sinteticos-e-arquitetura.md`
(normalização de formatos, deduplicação, reconstrução de valores ausentes,
realinhamento das zonas e dos blocos do Eixo 1 ao Manual de Avaliação,
nomes fictícios de unidades/equipes) e produz:

- `data/saida/limpo/*.csv` - as 5 tabelas tratadas, mesmo grão da origem;
- `data/saida/qualidade_dados.json` - log de cada problema encontrado, quantas
  linhas afetou e a decisão tomada (é a fonte da tela "Qualidade dos dados");
- `data/saida/rastreia_data.json` - pacote compacto consumido pelos protótipos.

A origem dos dados fica isolada na função `carregar()`; quando o middleware de
leitura do cliente estiver disponível, só essa função muda.

## Reprodutibilidade

Sem caminhos absolutos, sem passos manuais não registrados.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# os 5 CSVs da base sintética comum já estão em data/entrada/
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida
python pipeline/perfilar_base.py  --entrada data/entrada --saida data/saida --docs docs
python pipeline/verificar_prototipo5.py --entrada data/entrada --saida data/saida
python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json --verificar   # "iguais"

# Protótipo 6 (atual): pacote com os dois conjuntos de parâmetros
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida --pacote v6
python pipeline/embutir_dados.py --html app/mvp6.html --dados data/saida/rastreia_data_v6.json --verificar   # "iguais"

# Protótipos 3 e 4: mesmo pipeline com os parâmetros do dicionário da base (v1.0)
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida-dicionario --modo dicionario
python pipeline/embutir_dados.py --html app/mvp3.html --dados data/saida-dicionario/rastreia_data.json --verificar   # "iguais"
python pipeline/embutir_dados.py --html app/mvp4.html --dados data/saida-dicionario/rastreia_data.json --verificar   # "iguais"
```

Os pacotes de dados embutidos nos Protótipos 3, 4 (`--modo dicionario`) e 5 (`--modo manual`, padrão) são idênticos aos que o pipeline gera a partir dos CSVs; todo número das telas é rastreável ao script.

Saída esperada do primeiro comando (contagens da base sintética de 24/09/2026):

```
modo=manual equipes=132 resultados=1363 eixo3=13294 nps=6815 planos=420 problemas_logados=25
```

## Documentação

- `CLAUDE.md` - contexto do projeto para trabalhar neste repositório com o Claude Code.
- `docs/requisitos.md` - requisitos funcionais e não funcionais (reunião de imersão, 10/09).
- `docs/revisao-dados-sinteticos-e-arquitetura.md` - perfilamento da base, problemas encontrados, divergências com o Manual de Avaliação e arquitetura da solução.
- `docs/perfilamento-base.md` - perfilamento (volume, tipos, chaves, completude, contagem antes/depois, 25 tratamentos, dispersão) e `docs/figuras/`.
- `docs/explicacao-prototipo-5.md` - por que o Protótipo 5 difere dos Protótipos 3 e 4.
- `docs/LEIA-ME-base-cliente.md` e `docs/DICIONARIO_DE_DADOS.md` - documentação original da base.
- `docs/capturas/` - tela "Qualidade dos dados" do Protótipo 6 (atual) e, como histórico, dos Protótipos 3 e 5 (geradas por `capturar_telas.py`).
- `docs/processo/` - backlog em épicos e user stories, riscos com probabilidade, impacto e cenários, registro de sprints, justificativa de ferramentas e método, pontos fortes e de melhoria.
- `docs/tela-qualidade-dados.md` - especificação da tela "Qualidade dos dados" (o que ela deve mostrar, a partir de `qualidade_dados.json`).

## Protótipo atual

**Protótipo 6** (`app/mvp6.html`, publicado em https://ratreia.s3.us-east-1.amazonaws.com/mvp6/index.html). Reúne os ajustes da devolutiva do SR1: faixa, máximos e fonte registrados em toda tela, troca entre Manual e dicionário, log de qualidade com contagem antes e depois e tela de análise exploratória. Detalhes em `app/README.md`.

## Pendências em aberto

- Definição da faixa de zona oficial (Manual ou dicionário) pelo professor e pelo NIIMA; o Protótipo 6 mostra as duas.
- Trocar a origem (`carregar()`) pelo middleware do cliente quando disponível (risco R1).
