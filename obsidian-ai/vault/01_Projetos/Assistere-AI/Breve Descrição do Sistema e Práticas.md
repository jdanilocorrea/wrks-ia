
A arquitetura que estamos a desenhar separa rigorosamente o "Cérebro" (LLM/Agente) das "Mãos" (Skills/Ferramentas) e das "Leis" (Domínio). A resposta é um absoluto sim. A IA atuará num ambiente isolado e blindado, garantindo compliance com a LGPD e prevenindo vulnerabilidades de execução, como _prompt injection_.

Na nossa topologia de monorepo, a separação de responsabilidades segue estritamente os padrões empresariais de 2026:

- **O Core Jurídico (`packages/assistere-domain/`):** Contém apenas modelos de dados (Pydantic) e regras de negócio. Não possui dependências de IA.
    
- **O Catálogo de Ferramentas (`packages/assistere-skills/`):** Onde residem as capacidades atómicas e determinísticas. Aqui criamos funções especializadas, como `extrair_texto_pdf()`, `consultar_api_banco_central()` ou `calcular_tabela_irpf()`. Estas _skills_ interagem com o sistema de ficheiros local ou APIs externas, mas são processos tradicionais sem capacidade de raciocínio.
    
- **A Fronteira de Segurança (`apps/mcp-server/`):** Atua como um _firewall_ semântico. Expõe apenas um subconjunto seguro de _skills_ para a IA consumir.
    
- **A Orquestração Isolada (`apps/agent-workers/`):** O ambiente onde os agentes LangGraph operam. O LLM nunca lê o disco local diretamente nem executa comandos no terminal. Ele apenas avalia o contexto, elabora um plano de ação e envia pedidos estruturados (JSON/Tool Calls) para o MCP ou para as _skills_ importadas. Se o agente tentar uma ação não permitida, a _skill_ rejeita a operação com base nos contratos Pydantic.
    

Este padrão de _Agentic Design_ garante que possamos atualizar o modelo base do Gemini no futuro sem alterar o código de cálculo tributário, bem como testar cada _skill_ de extração de dados com testes unitários (pytest) tradicionais.


---

### O Paradigma LangGraph na Assistere (2026)

Diferente de 2023/2024, onde os agentes funcionavam como "caixas pretas" autônomas que tentavam resolver tudo num único prompt longo, o **LangGraph** introduz o conceito de **Máquina de Estados Finita (State Machine) e Cíclica**. Ele modela o raciocínio da IA exatamente como o fluxo de trabalho de um consultor humano da nossa "Big Four".

Aqui estão os três pilares do LangGraph aplicados à Assistere:

1. **Estado Global (State):** O grafo mantém um objeto de "Estado" (nosso Pydantic de `assistere-domain`) que trafega entre todas as etapas. Se o processo é a aprovação de um Visto RN_04, o estado guarda o nome do expatriado, os documentos lidos até agora e os erros encontrados.
    
2. **Nós e Arestas Cíclicas (Nodes & Edges):** Cada etapa do processo (ex: `extrair_dados_passaporte`, `validar_regras_mercosul`) é um "Nó" isolado (uma função Python). As "Arestas" são a lógica de roteamento. Se a IA falhar ao extrair o CPF de um RNE borrado, o grafo pode entrar num _loop_ que tenta realçar a imagem, em vez de simplesmente falhar ou alucinar o dado.
    
3. **Aprovação Humana (Human-in-the-Loop - HITL):** O recurso mais crítico para compliance. O LangGraph permite pausar a execução (_checkpointing_). A IA analisa 50 páginas de extratos bancários do exterior e prepara a DARF do Carnê-Leão. O grafo _pausa_. O analista sênior entra, revisa o estado, ajusta uma dedução (pensão alimentícia) e aperta "Aprovar". A IA então retoma o fluxo e envia o e-mail para o cliente.