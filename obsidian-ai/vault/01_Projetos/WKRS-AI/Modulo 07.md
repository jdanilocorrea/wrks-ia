## 8. Infraestrutura Agêntica e Skills (Antigravity Sandbox)

Para além dos motores LLM e TTS servidos via web, o laboratório comporta um ecossistema de automação isolado para desenvolvimento de agentes baseados em Inteligência Artificial, gerido sob a arquitetura _Antigravity_.

### 8.1. O Ambiente de Sandbox (`antigravity-sandbox`)

Este diretório é um ambiente Python isolado e efémero. Todo o desenvolvimento e gestão de pacotes é gerido nativamente pela ferramenta ultrarrápida `uv` (armazenando os binários oxidados no diretório `.cache/uv/`).

- **Gestão de Versões:** O ambiente suporta isolamento multiversão do interpretador Python (ex: `python3.14`), permitindo testar agentes com as funcionalidades e sintaxes mais recentes da linguagem sem quebrar dependências de pacotes mais antigos (como os contidos no ambiente virtual `.venv`).
    

### 8.2. Ecossistema de Skills (`.agents/skills/`)

As _Skills_ representam ferramentas discretas e reutilizáveis invocadas pelo motor agêntico. A estrutura atual demonstra uma clara divisão de responsabilidades DevOps e de monitorização, permitindo que a IA interaja com a infraestrutura local:

- **`github-actions-cicd`**: Componente de orquestração de CI/CD para automações GitOps.
    
- **`python-modern-workflow`**: _Skill_ orientada às melhores práticas de empacotamento com suporte às metodologias do `uv` e verificação estrita (`ruff`).
    
- **`podman-log-analyzer`**: Uma prova do paradigma AIOps. A ferramenta permite que um agente faça a ingestão e análise semântica de _logs_ cruas dos contentores Quadlets locais para deteção precoce de falhas no laboratório.
    
- **`squad-monitor`**: Contém o executável (`monitor.py`) responsável pela verificação e orquestração ativa dos agentes, atuando como o elo de execução dentro do Sandbox.