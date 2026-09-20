# Contexto do Projeto: Antigravity Sandbox

## Visão Geral
Este repositório é um sandbox seguro (Containerized Environment) focado na orquestração de Inteligência Artificial usando a arquitetura de Agentes Autônomos do Google Antigravity CLI.

## Stack Tecnológica Oficial
*   **SO Base:** Fedora Linux 44 (via Podman Rootless).
*   **Linguagem Principal:** Python moderno.
*   **Gestão de Pacotes e Ambiente:** Exclusivamente via `uv`.
*   **Linting/Formatação:** Exclusivamente via `ruff`.
*   **Linguagem Auxiliar:** Rust (Cargo/rustc).

## Regras de Engenharia do Repositório (System Constraints)
1. **Gerenciamento Python:** É estritamente proibido utilizar `pip`, `poetry` ou módulos manuais como `venv`. O ecossistema Astral (`uv` e `ruff`) é a única fonte de verdade.
2. **Ambiente Isolado:** O agente opera dentro de um container Podman restrito (`/workspace`). O agente não deve tentar modificar configurações do host fora deste diretório montado.
3. **Automação:** Toda nova funcionalidade complexa adicionada ao projeto deve ser transformada numa Agent Skill (`SKILL.md`) correspondente dentro de `.agents/skills/`.
4. **Rust Bindings:** Quando o uso de Rust for necessário para performance ou paralelismo (como auxiliares para a IA local), ele deve ser integrado utilizando as ferramentas padrão (`cargo`).
