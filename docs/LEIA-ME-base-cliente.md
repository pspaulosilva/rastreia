# Base de dados para o SR1 — Recife Monitora

**Projeto 5 · Gestão de Tecnologia da Informação · CESAR School · 2026.2**

---

## ⚠ Esta base é sintética

Nenhum valor corresponde a equipes, unidades, profissionais ou resultados reais da Secretaria de Saúde do Recife.

A **estrutura** — três eixos somando 1.000 pontos, ciclos quadrimestrais desde 2023, zonas de classificação, granularidade equipe → unidade → distrito sanitário — replica a descrição oficial do programa constante da documentação do desafio. Os **valores** foram gerados por simulação.

### Obrigatório

Toda visualização, slide ou relatório produzido com estes dados deve indicar de forma visível que se trata de base simulada. Um gestor da Secretaria não pode, em nenhum momento, confundir estes números com indicadores reais da rede.

### Por que uma base sintética

A solicitação formal de dados ao cliente está em tramitação e não haverá resposta até o SR1. O roteiro da disciplina prevê expressamente o uso de dataset "real ou simulado, conforme orientação do professor" (Semana 5). Esta base permite que o trabalho técnico avance sem depender do prazo de terceiros.

O atraso no acesso aos dados reais é um **risco de projeto legítimo** e deve constar do mapa de riscos da equipe, com projeção de cenários e plano de mitigação — o critério de Mapeamento de Riscos do SR1 vale 0,75 pt.

---

## Arquivos

```
dados/
├── equipes.csv                 cadastro das equipes da rede
├── resultados_ciclos.csv       resultados por equipe e ciclo
├── eixo3_indicadores.csv       detalhe do Eixo 3, por indicador
├── nps_atributos.csv           detalhe do Eixo 2, por atributo
└── planos_acao.csv             planos de ação e maturidade
DICIONARIO_DE_DADOS.md          estrutura, domínios e regras de negócio
```

Formato CSV, codificação UTF-8, separador vírgula.

---

## Como isto se encaixa no cronograma

| Etapa CRISP-DM | Semana | O que fazer |
|---|---|---|
| Entendimento do Negócio | 1 a 4 | Coberto pela documentação do desafio e pela revisão bibliográfica |
| **Entendimento dos Dados** | 5 | Ler o dicionário. Perfilar a base: grão, volume, tipos, domínios, chaves, integridade entre tabelas, completude |
| **Preparação dos Dados** | 6 | Tratar o que for encontrado. **Documentar cada decisão** — a rubrica exige justificativa, não apenas código |
| **Análise Preliminar / EDA** | 7 | Estatísticas descritivas, correlações, padrões. Visualizações exploratórias |
| Modelagem | 9 em diante | Selecionar a técnica de IA a partir dos padrões encontrados |

## O que a rubrica do SR1 cobra (Técnico, 10,0 pts)

| Item | Pts |
|---|---|
| Entendimento do Conjunto de Dados | 1,5 |
| Limpeza dos Dados | 1,5 |
| Análise Preliminar | 1,0 |
| Processo de Visualização | 2,0 |
| Visualizações Adequadas | 1,0 |
| Visualização Interativa (protótipo) | 1,0 |
| Documentação e Repositório | 1,0 |
| Reprodutibilidade | 1,0 |

Dois avisos sobre os dois últimos itens, que costumam ser subestimados: **Documentação e Repositório** avalia a organização dos notebooks no Drive e no site da equipe, e **Reprodutibilidade** exige que o código seja reexecutável por terceiros — comentado, sem caminhos absolutos da máquina de quem escreveu, e sem depender de passos manuais não registrados.

---

## Recomendação técnica: isole a leitura dos dados

Construa o pipeline de forma que a origem dos dados fique em **um único módulo**. Quando os dados reais chegarem, trocar a fonte deve ser uma alteração localizada, não uma reescrita.

Isso não é conselho de estilo: o critério de Reprodutibilidade cobra isso no SR1, e a Semana 15 prevê explicitamente reexecutar o pipeline com dados atualizados.

Registro técnico relevante, informado pela equipe do cliente em 10/09/2026: as pontuações dos eixos e o NPS são calculados em servidor no momento da exibição e não permanecem armazenados em banco. Os dados reais, quando vierem, chegarão como **valores já calculados** — que é o formato desta base.

---

## Contexto público do programa

O Recife Monitora é uma das três frentes do **Qualifica Atenção Básica**, ao lado do Recife Reconhece e do Recife Experimenta, dentro do programa Recife Cuida. Nasceu de uma cooperação técnica entre o IEPS (Instituto de Estudos para Políticas Públicas de Saúde) e a Prefeitura do Recife, com apoio da Umane, e a plataforma foi lançada em março de 2023, desenvolvida pela GGTI em conjunto com a Emprel.

Há material público relevante para a revisão da literatura e para a contextualização do desafio (Semanas 2 e 3): publicações do IEPS sobre o Qualifica Atenção Básica, o relato de experiência na plataforma Colabora APS da Fiocruz, e uma avaliação de impacto do programa referente ao período 2022–2024 disponível no Observatório da Atenção Primária à Saúde.

Dois pontos dessas fontes que importam para a análise:

**Escala.** Fontes públicas indicam cerca de 300 equipes aderidas até o 3º quadrimestre de 2024. Esta base tem 132 equipes, dimensionada a partir do número de profissionais informado pela equipe técnica do cliente. Os dois números medem coisas diferentes e a referência correta ainda será confirmada. Construam o pipeline sem supor o tamanho da rede — ele precisa funcionar se o volume dobrar.

**Adesão voluntária.** A participação das equipes nos ciclos é voluntária. Isso significa que ausência de uma equipe em um ciclo pode ser decisão dela, e não falha ou desempenho ruim. Vale considerar esse possível viés de seleção ao interpretar qualquer comparação entre equipes ou entre ciclos — e é uma boa pergunta a levar ao cliente.

---

## Observação sobre a qualidade dos dados

Esta base reproduz as condições de uma extração de sistema em produção. Como em qualquer extração real, é esperado que existam divergências entre a estrutura especificada no dicionário e o conteúdo efetivo dos arquivos.

Perfilar antes de analisar. Uma Análise Preliminar construída sobre dados não verificados produz conclusões que não se sustentam, por mais elegante que seja o gráfico.
