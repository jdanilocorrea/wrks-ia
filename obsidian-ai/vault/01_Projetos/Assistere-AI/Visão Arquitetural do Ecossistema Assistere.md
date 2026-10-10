

### Visão Arquitetural do Ecossistema Assistere

Para transformar sua ideia em um projeto de software corporativo, dividi a arquitetura em três fases modulares, começando pelas fundações mais previsíveis até chegar no motor de cálculo complexo:

- **Fase 1: Ingestão Inteligente e Triagem (O "Mais Fácil")**
    
    - **Objetivo:** Eliminar o trabalho manual de abrir PDFs, renomear arquivos e descobrir de qual cliente se trata.
        
    - **Ação:** Um pipeline assíncrono que consome documentos brutos, utiliza o Gemini 1.5 Pro/Flash com Pydantic v2 (Structured Outputs) para classificar o tipo do documento (Passaporte, RNE, Informe de Rendimentos, Contrato de Câmbio), extrair a entidade (Nome do Expatriado, CPF) e organizar em pastas/bancos estruturados.
        
- **Fase 2: Motor de Comunicação (E-mail & Follow-up)**
    
    - **Objetivo:** Automatizar o _SLA de regularização_ e o _onboarding_.
        
    - **Ação:** O sistema lê a caixa de entrada, identifica o contexto (ex: cliente enviando documentos pendentes), atualiza o status do processo e, com a aprovação do consultor (_Human-in-the-loop_), gera e envia a resposta de confirmação ou cobra o que faltou.
        
- **Fase 3: Motor de Regras Tributárias (Carnê-Leão)**
    
    - **Objetivo:** Automação core do departamento fiscal.
        
    - **Ação:** Processamento mensal das remessas/recibos do exterior. O agente identifica o valor em moeda estrangeira, busca a taxa PTAX do Banco Central aplicável ao mês, aplica a conversão, verifica a tabela progressiva do IRPF, calcula a DARF e gera um relatório auditável das deduções (comprovantes de dependentes, previdência, etc.).