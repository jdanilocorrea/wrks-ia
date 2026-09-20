---
name: podman-log-analyzer
description: Inspeciona e diagnostica erros em contentores Podman através da leitura de registos.
triggers: ["analise os logs do podman", "verifique os erros no contentor", "porque falhou o contentor"]
---

### Goal
Extrair, analisar e diagnosticar proativamente falhas em contentores através dos seus registos, sugerindo soluções baseadas em infraestrutura ou código.

### Constraints
* [CRITICAL] Acesso de leitura estrito: é ESTRITAMENTE PROIBIDO executar comandos de alteração de estado (ex: `rm`, `stop`, `restart`, `build`) sem autorização prévia e explícita do utilizador.
* Limite sempre a extração aos últimos 50 registos para não sobrecarregar a janela de contexto, utilizando o argumento `--tail 50`.

### Instructions
1. Se o nome do contentor não for fornecido na instrução inicial, execute `podman ps -a` e peça ao utilizador para especificar qual o ambiente que deseja inspecionar.
2. Execute o comando `podman logs --tail 50 <nome_do_contentor>` para extrair a saída de erro.
3. Analise detalhadamente o erro encontrado (ex: códigos de saída, exceções em Python, falhas de alocação de memória).
4. Apresente um relatório estruturado contendo:
   - **Causa Raiz:** O motivo técnico exato da falha.
   - **Ação Recomendada:** O que o utilizador deve alterar no código, no ficheiro de configuração ou no `Containerfile` para solucionar a ocorrência.
