---
name: github-actions-cicd
description: Gera pipelines de CI para o monorepo wrks-ia, focados no subprojeto antigravity-sandbox.
triggers: ["crie o ci/cd", "configure o github actions", "pipeline de deploy"]
allowed_paths: ["./"]
---

### Goal
Gerar um ficheiro de workflow do GitHub Actions (`.yml`) otimizado para Python (uv/ruff) que funcione perfeitamente dentro da arquitetura de monorepo do repositório `jdanilocorrea/wrks-ia`.

### Constraints
* [CRITICAL] O pipeline DEVE utilizar a action oficial do `uv` (`astral-sh/setup-uv`).
* Como estamos num monorepo, o pipeline DEVE ser configurado para acionar (trigger) nos eventos de `push` e `pull_request` APENAS quando houver alterações no path `antigravity-sandbox/**`.
* Todos os jobs (linting, test) DEVEM conter a chave `working-directory: antigravity-sandbox`.
* O pipeline deve validar a qualidade do código correndo `uv run ruff check .` e `uv run ruff format --check .`.

### Instructions
1. Leia o contexto do projeto para garantir o alinhamento com as regras globais.
2. Gere o código YAML do pipeline de integração contínua respeitando estritamente as constraints de monorepo acima.
3. Imprima o código YAML formatado para que o utilizador o possa copiar e mover para o diretório `../.github/workflows/ci_antigravity.yml` na raiz do monorepo.
