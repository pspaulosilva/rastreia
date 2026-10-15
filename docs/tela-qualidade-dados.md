# Tela "Qualidade dos dados"

Tela presente no menu dos Protótipos 3 e 5. Fonte dos dados: `data/saida/qualidade_dados.json`, gerado por `pipeline/preparar_dados.py` (lista `LOG`, 25 itens na base sintética de 24/09/2026).

Acesso: perfis central e distrital (o log descreve a base inteira da rede, por isso é o mesmo nos dois perfis; capturas feitas no perfil distrital). Perfil local não vê a tela.

## Estrutura de cada item do log

| Campo | Conteúdo |
|---|---|
| `tabela` | equipes, resultados, eixo3, nps ou planos |
| `problema` | descrição do problema encontrado na origem |
| `linhas` | quantas linhas foram afetadas (contagem antes do tratamento) |
| `decisao` | o que o pipeline fez e por quê |
| `exemplo` | amostra dos valores originais (opcional) |

## O que a tela mostra

1. **Cabeçalho**: aviso "DADOS SIMULADOS", ciclo de referência, data de geração (`meta.gerado_em`), fonte (`meta.fonte`).

2. **Resumo da base** (cartões): linhas lidas e linhas após limpeza por tabela (132 equipes; 1.392 → 1.363 resultados; 13.294 eixo3; 6.815 nps; 420 planos), total de problemas logados (25), equipes excluídas por INE sem cadastro (13), linhas desclassificadas (57), equipes ausentes em algum ciclo (27).

3. **Tabela de tratamentos**: uma linha por item do log, com as 4 colunas acima, agrupada por tabela de origem. Filtros por tabela e por tipo (padronização, integridade, regra de negócio).

4. **Divergências com o Manual de Avaliação** (bloco fixo): zonas 850/700/550/400 da base versus 900/800/600/400 do Manual; blocos do Eixo 1 A80/B60/C60 versus A40/B80/C80; Eixo 2 com 5 atributos versus 6 perguntas. Decisão aplicada e pergunta pendente ao cliente.

5. **Sinalizações que afetam a leitura do painel**: Bloco A inválido contado como 0 (147 linhas), Eixo 2 reconstruído (flag `e2r` no pacote), pontuação recalculada (9 outliers).

## Regras de exibição

- Nunca mostrar ausência ou desclassificação como zero.
- Cada número do painel que depende de valor reconstruído deve ter indicação visual.
- O log inteiro deve ser exportável (JSON e PDF) para anexar ao resumo do quadrimestre (RNF05).

## Capturas

`docs/capturas/prototipo3-qualidade.png` (pipeline `--modo dicionario`, v1.0) e `docs/capturas/prototipo5-qualidade.png` (pipeline `--modo manual`, v1.1), geradas por `python pipeline/capturar_telas.py --tela qualidade --prototipos 3 5`.
