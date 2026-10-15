# Documento de Requisitos: Recife Monitora + IA
**Equipe 4 · Projeto 5 · GTI · CESAR School · 2026.2**
**Versão 0.2 · 10/09/2026 · Fonte: reunião de imersão com o cliente (Anderson Lopes, André Luiz; monitor Victor Felipe)**

Versão enxuta, espelho do Google Doc da equipe. Q1 e Q4 respondidas em 10/09; D1 e D2 reclassificadas (D1 é decisão da equipe; D2 é desejo do cliente para produção, não restringe o MVP).

---

## 1. Contexto

Reunião de imersão em 10/09/2026 com Anderson Lopes (técnico, responsável pela API e lógica do sistema) e André Luiz, acompanhada pelo monitor Victor Felipe.

Números do programa: 3.000 profissionais, 8 distritos sanitários, 300 gestores com acesso ao sistema, 2 a 3 mil interações de NPS por dia. Stack atual: API Laravel, front próprio e PostgreSQL.

Glossário: **INE** = Identificador Nacional de Equipe; **SEI** = Sistema Eletrônico de Informações (workflow de protocolos); **Eixos** = autoavaliação, satisfação do usuário (NPS) e desempenho assistencial.

## 2. Decisões e restrições

| # | Decisão |
|---|---|
| D1 | Aplicação **externa e paralela** ao Recife Monitora, sem embarcar nada na plataforma atual. Decisão da equipe, para evitar custo e risco de incorporação agora; o cliente concordou. |
| D2 | Processamento de IA **local**, em servidor com GPU NVIDIA dedicada, é o cenário desejado pelo cliente para produção. Não impede que o MVP rode em nuvem. |
| D3 | Acesso aos dados por **middleware somente leitura**, construído pelo cliente sobre os endpoints existentes. |
| D4 | Migrações de profissional ou de INE entre equipes são resolvidas **antes** de gerar qualquer relatório. |

## 3. Requisitos funcionais

Prioridade: **M** = Must, **S** = Should, **C** = Could.

| ID | Requisito | Pri. |
|---|---|---|
| RF01 | Consumir os 3 eixos exclusivamente via middleware de leitura do cliente. | M |
| RF02 | Ingerir NPS diariamente (2-3k interações/dia); eixos 1 e 3 por quadrimestre. | M |
| RF03 | Manter histórico de vínculo profissional↔INE e INE↔equipe com datas de vigência, e agregar por equipe respeitando esse período. | M |
| RF04 | Obter NPS e pontuação dos 3 eixos (1.000 pts/equipe/ciclo) já calculados pela API do cliente (não ficam no banco); agregar por equipe, distrito e rede, normalizando pelo tamanho da equipe (8 a 80 profissionais). | M |
| RF05 | **Resumo do quadrimestre** (urgente): ranking, maiores quedas e ganhos, equipes em zona crítica e causas de perda por eixo, em cada nível de gestão. Exportável em PDF. | M |
| RF06 | Alertas classificados por severidade, com critérios validados pelo NIIMA. Envio por e-mail institucional. | M |
| RF07 | Envio de alertas para grupos de WhatsApp; incidentes críticos por Telegram. | S / C |
| RF08 | Recomendações por equipe indicando onde a pontuação foi perdida e ação sugerida, sempre com fonte citada. | S |
| RF09 | Chatbot interno (RAG) sobre manuais e resultados, restrito à base interna, com fonte e respeitando o perfil de acesso (local, distrital, central). | S |
| RF10 | Tendências entre ciclos por equipe (melhora, piora, estagnação). | S |
| RF11 | Pipeline de saneamento reproduzível com log de qualidade por ciclo (ver `pipeline/preparar_dados.py`). | M |

## 4. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Produção: IA on-premise (GPU NVIDIA), sem chamadas a APIs externas, conforme desejo do cliente. MVP: pode rodar em nuvem, com dados anonimizados ou sintéticos. |
| RNF02 | Sem escrita no banco de produção; leitura apenas via middleware. |
| RNF03 | Suportar 300 usuários simultâneos: relatórios e insights pré-computados em lote; inferência sob demanda só no chatbot. |
| RNF04 | Custo previsível: estimativa de hardware e operação apresentada ao cliente, sem cobrança por token. |
| RNF05 | LGPD: dados em ambiente controlado, anonimização quando necessário, trilha de auditoria. |
| RNF06 | Resultados idênticos aos do Recife Monitora quando não há migração; divergências só por regra documentada. |
| RNF07 | Documentação e transferência de conhecimento ao NIIMA. |
| RNF08 | Parâmetros do programa (zonas, máximos de bloco, pesos por grupo e ciclo) configuráveis sem alteração de código. |

## 5. Regras de negócio

- Avaliação de NPS conta para a equipe em que o profissional estava vinculado na data da interação.
- INE que muda de equipe inicia nova série a partir da data da mudança; histórico anterior fica no contexto de origem.
- Criticidade segue as zonas de classificação do Manual de Avaliação de Qualidade.
- Perfil local vê a própria equipe; distrital vê o distrito; central vê a rede.

## 6. Questões em aberto (Anderson Lopes)

1. NPS é armazenado já calculado ou processado a cada exibição? **Respondido em 10/09:** calculado em servidor a cada exibição, não fica no banco; cliente propõe expor os valores via API. Implicação: consumir indicadores prontos pelo middleware (ajusta RF04).
2. Como o sistema hoje trata migração de profissional e de INE? Existe tabela de vigência?
3. Especificação do middleware: endpoints, formato, autenticação, frequência.
4. Distribuição de equipes por distrito. **Respondido em 10/09:** heterogênea, equipes de 8 a 80 profissionais. Pendente: lista por distrito. Implicação: normalizar indicadores pelo tamanho da equipe.
5. Hardware (GPU) disponível ou previsto e orçamento.
6. E-mail institucional e WhatsApp Business oficiais existem? Telegram é aceito?
7. Anexar o resumo ao SEI é desejado?
8. Formato e prazo do primeiro resumo do quadrimestre.
9. Acesso ao histórico desde 2023 ou só ciclo corrente?

## 7. Riscos

| Risco | Mitigação |
|---|---|
| Middleware atrasa | Iniciar com dados sintéticos no esquema real; fechar contrato de API com Anderson. |
| GPU insuficiente para LLM | Modelos pequenos quantizados; pipeline analítico separado do chatbot. |
| Regras de migração incorretas distorcem NPS | Validar regras com Anderson antes de implementar; testar com casos reais. |
| Canais sem aval institucional | E-mail como canal mínimo; WhatsApp e Telegram condicionados à aprovação. |

## 8. Próximos passos

1. Enviar questões da seção 6 a Anderson e agendar reunião técnica.
2. Definir contrato do middleware (schema dos 3 eixos e vigências).
3. Protótipo do resumo do quadrimestre com dados sintéticos.
4. Estimar custo de hardware para 3 cenários de modelo local.
5. Atualizar Matriz CSD e Hipótese de Solução com D1 a D4.
