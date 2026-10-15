# Explicação dos números do Protótipo 5

Resposta ao "Primeiro ponto a esclarecer" da devolutiva do SR1. Verificação reproduzível em `pipeline/verificar_prototipo5.py`.

## O que gerou cada protótipo

| Protótipo | Fonte dos números | Blocos do Eixo 1 | Zonas |
|---|---|---|---|
| 3 e 4 | Base comum como veio (pipeline v1.0, só limpeza) | A 80, B 60, C 60 (dicionário) | 850/700/550/400 (dicionário) |
| 5 (mostrado no SR1) | `rastreia_data.json` do pipeline v1.1 (24/09) | reescalados para A 40, B 80, C 80 (Manual de Avaliação, Quadro 4) | 900/800/600/400 (Manual, Quadro 10) |

A versão 1.1 do pipeline foi feita na véspera do SR1 para alinhar a base sintética ao Manual de Avaliação de Qualidade (v. 02.03.26), porque a base veio com máximos de bloco e faixas de zona diferentes do Manual (ver `docs/revisao-dados-sinteticos-e-arquitetura.md`, seção 3). O Protótipo 5 consumiu esse pacote. Os Protótipos 3 e 4 ficaram sobre a base sem o realinhamento. A equipe não registrou essa diferença de versão na entrega, e esse é o erro.

## Conferência número a número (ciclo 2026.2)

| Equipe | Base crua | Realinhado (v1.1) | Protótipo 5 |
|---|---|---|---|
| Encruzilhada I (INE 6000000032, grupo 1, 21 profissionais) | 405,0 = A 0 + B 28,0 + C 23,7 + E2 100,9 + E3 252,4 | 422,2 = A 0 + B 37,3 + C 31,6 + E2 100,9 + E3 252,4 | 422 |
| Curado III (INE 6000000098, grupo 1, 18 profissionais) | 373,8 = A 0 + B 23,6 + C 29,7 + E2 62,6 + E3 257,9 | 391,6 = A 0 + B 31,5 + C 39,6 + E2 62,6 + E3 257,9 | 392 |
| Média da rede (equipes pontuadas) | 678,3 (n = 133, inclui 4 INEs sem cadastro) | 680,8 (n = 129) | 681 |
| Equipes abaixo de 600 | 26 | 27 | 27 |

Cálculo do reescalonamento: B = 28,0 x 80/60 = 37,3; C = 23,7 x 80/60 = 31,6. O Bloco A é 0 nas duas equipes porque a taxa de resposta ficou abaixo de 30% (0,2116 e 0,246), regra 1 do dicionário. Eixos 2 e 3 não mudam.

## Decisão para o SR2

Aplicada no **Protótipo 6** (`app/mvp6.html`): toda tela mostra a faixa, os máximos e a fonte em uso, e Configurações alterna entre Manual e dicionário sem trocar de arquivo.


Até o professor esclarecer a divergência entre o Manual (5ª versão) e o dicionário da base, cada tela registra qual faixa e quais máximos usa, com a fonte. O pipeline mantém os dois modos, escolhidos por `--modo` em `preparar_dados.py` (parâmetros na constante `PARAMETROS`). Os dois reproduzem exatamente o pacote embutido em cada protótipo:

```bash
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida                                   # v1.1, Manual
python pipeline/embutir_dados.py --html app/mvp5.html --dados data/saida/rastreia_data.json --verificar        # iguais
python pipeline/preparar_dados.py --entrada data/entrada --saida data/saida-dicionario --modo dicionario      # v1.0, dicionário
python pipeline/embutir_dados.py --html app/mvp3.html --dados data/saida-dicionario/rastreia_data.json --verificar   # iguais
python pipeline/embutir_dados.py --html app/mvp4.html --dados data/saida-dicionario/rastreia_data.json --verificar   # iguais
```
