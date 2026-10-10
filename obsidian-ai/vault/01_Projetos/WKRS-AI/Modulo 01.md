# Ecossistema de Inteligência Artificial e DevOps Local (`wrks-ia`)

## 1. Visão Geral do Projeto

O projeto **`wrks-ia`** consiste num laboratório local de Inteligência Artificial e ferramentas de desenvolvimento de alto desempenho, arquitetado sob princípios rígidos de DevOps, Infraestrutura como Código (IaC - via GitOps) e segurança.

O objetivo principal é manter um ecossistema de microsserviços (Geração de Texto, Leitura Neural de Voz e Agentes Autónomos) a correr de forma totalmente isolada, persistente e monitorizada numa máquina Linux local, utilizando tecnologias de contentorização sem privilégios de administrador (_rootless_).

### 1.1. Pilares da Arquitetura

- **Isolamento e Segurança (_Rootless_):** Todos os serviços correm em Podman _rootless_, garantindo que nenhuma vulnerabilidade nos contentores comprometa o sistema operativo (Fedora). O tráfego direto (bind de portas host) é bloqueado, forçando o acesso exclusivo via Proxy Reverso.
    
- **Infraestrutura como Código (GitOps):** Toda a definição de redes, volumes e contentores está declarada em ficheiros `.container`, `.network` e `.volume` (systemd Quadlets), versionados num monorepo Git.
    
- **Gestão Moderna de Dependências:** O desenvolvimento de código Python (como as interfaces Gradio) é gerido pela ferramenta `uv`, garantindo resoluções de dependências ultra-rápidas e contentores extremamente leves (construídos a partir do `pyproject.toml`).
    
- **Observabilidade de Nível de Produção:** O ecossistema inclui Tracing Distribuído nativo via OpenTelemetry, exportando métricas de latência de rede, tempo de inferência de IA e I/O de disco para um painel centralizado.
    

## 2. Topologia do Sistema

A infraestrutura está desenhada numa topologia _Hub-and-Spoke_ fechada. O tráfego externo (Navegador do utilizador) não tem acesso direto aos motores de IA, comunicando apenas com um ponto de entrada seguro.

Snippet de código

```
graph TD
    %% Entradas Externas
    User[Navegador Web / Host Fedora]
    
    %% Proxy e DNS
    subgraph Ponto_Entrada [Gateway Segura]
        NPM[Nginx Proxy Manager AI<br/>:80, :81, :443]
    end
    
    %% Rede Interna Isolada
    subgraph AI_Net [Rede Interna: ai-net.network]
        WebUI[Open-WebUI<br/>Porta int: 8080]
        Ollama[Ollama LLM<br/>Porta int: 11434]
        TTS[Motor XTTS v2<br/>Porta int: 8000]
        Reader[VoiceReader Gradio<br/>Porta int: 7860]
        Jaeger[Jaeger OTel Collector<br/>UI: 16686, OTLP: 4318]
        Agentes[Antigravity Sandbox<br/>Skills & Monitorização]
    end

    %% Fluxo de Dados
    User -- "chat.ia.local" --> NPM
    User -- "leitor.ia.local" --> NPM
    User -- "trace.ia.local" --> NPM
    
    NPM -- "Redirecionamento Interno" --> WebUI
    NPM -- "Redirecionamento Interno" --> Reader
    NPM -- "Redirecionamento Interno" --> Jaeger
    
    WebUI -. "Geração de Texto" .-> Ollama
    Reader -. "Clonagem de Voz" .-> TTS
    
    Reader == "Traces (OTLP)" ==> Jaeger
    
    classDef infra fill:#2d3436,stroke:#74b9ff,stroke-width:2px,color:#fff;
    classDef ai fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:#fff;
    classDef obs fill:#e17055,stroke:#ffeaa7,stroke-width:2px,color:#fff;
    
    class NPM infra;
    class WebUI,Ollama,TTS,Reader,Agentes ai;
    class Jaeger obs;
```

### 2.1. Stack Tecnológico (Tech Stack)

- **Sistema Operativo Base:** Linux (Fedora).
    
- **Motor de Contentores:** Podman v4+.
    
- **Orquestração:** systemd / Quadlets.
    
- **Proxy Reverso:** Nginx Proxy Manager (com suporte s6-overlay adaptado para rootless).
    
- **Modelos de Linguagem (LLM):** Ollama integrado com Open-WebUI.
    
- **Motor Texto-para-Fala (TTS):** OpenedAI-Speech (Coqui XTTS v2) com clonagem _zero-shot_ (voz feminina nativa `brasileira.wav`).
    
- **Linguagens e Build Tools:** Python 3.12+, `uv`, `ruff`.
    
- **Observabilidade:** OpenTelemetry SDK (Python) e Jaeger All-in-One.