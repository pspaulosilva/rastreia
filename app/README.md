# MVP / protótipos RASTRE.IA

Cinco versões do protótipo, cada uma um único arquivo HTML (CSS e JS embutidos; a única
dependência externa é a fonte do Google Fonts, opcional). Publicados em
`s3://ratreia/mvpN/index.html` (us-east-1, leitura pública) e versionados aqui.

| Arquivo | Versão | Dados | Zonas / blocos do Eixo 1 |
|---|---|---|---|
| `mvp1.html` | Protótipo 1 | exemplo ilustrativo, sem a base comum | faixas do Manual de Avaliação |
| `mvp2.html` | Protótipo 2 | exemplo ilustrativo, sem a base comum | faixas do Manual de Avaliação |
| `mvp3.html` | Protótipo 3 | base comum, pipeline v1.0 (só limpeza), em `<script id="rm-data">` | 850/700/550/400 e A80/B60/C60 (dicionário da base) |
| `mvp4.html` | Protótipo 4 | base comum, pipeline v1.0 | idem |
| `mvp5.html` | Protótipo 5 (mostrado no SR1) | base comum, pipeline v1.1 (realinhado ao Manual) | 900/800/600/400 e A40/B80/C80 (Manual) |

`mvp3` a `mvp5` trazem o aviso "DADOS SIMULADOS", perfis de acesso (central, distrital,
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

`python pipeline/capturar_telas.py --tela qualidade --prototipos 3 5` gera
`docs/capturas/prototipoN-qualidade.png` com Chromium (Playwright). Outras telas:
`painel`, `alertas`, `planos`, `resumo`, `chat`, `config`.
