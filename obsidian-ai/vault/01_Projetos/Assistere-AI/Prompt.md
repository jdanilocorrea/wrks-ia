
Atue como Assistere Automation Architect. Estamos desenvolvendo uma plataforma de IA Generativa para a Assistere (Consultoria de Mobilidade Global e Tributação de Expatriados). O projeto seguirá arquitetura modular em Python 3.12+, gerenciado via `uv`, linting via `ruff`, adotando tipagem estática rigorosa e programação assíncrona (`asyncio`). Todas as extrações do LLM (Gemini) devem obrigatoriamente usar `Structured Outputs` via Pydantic v2, respeitando as diretrizes da LGPD (anonimização em log).

**Objetivo do Módulo Atual (Fase 1 - MVP):** Desenvolver o subsistema de **Ingestão e Contextualização de Documentos**.

**Requisitos Funcionais:**

1. Receber arquivos (PDFs/Imagens) de clientes e aplicar OCR/Visão Computacional nativa do Gemini.
    
2. Identificar e tipar o documento (ex: Passaporte, CPF, Holerite Estrangeiro, Extrato Bancário).
    
3. Extrair dados contextuais (Nome do Titular, Data de Emissão, País de Origem) mapeando-os para um modelo Pydantic validado.
    
4. Retornar os metadados organizados para posterior arquivamento e acionamento de gatilhos de automação de email (Fase 2).
    

**Restrições:**

- O código deve estar pronto para produção, documentado e incluir tratamento de exceções estruturado para casos onde o LLM falhe na leitura.
    
- Forneça os comandos de setup do ambiente utilizando `uv`.