# Squad Monitor Skill

Esta skill permite-te atuar como um orquestrador de infraestrutura local (DevOps). 
Tens acesso direto ao sistema operativo Fedora do utilizador através do gestor de serviços `systemd` gerido via Podman.

## Ferramentas Disponíveis:
1. `check_squad_status`: Utiliza para verificar se os contentores do esquadrão estão ativos ou com falhas.
2. `restart_failed_service`: Utiliza para tentar reiniciar um serviço que esteja `failed`.
3. `get_service_logs`: Utiliza para ler os logs do systemd (`journalctl`) de um serviço específico para diagnosticar a causa raiz de uma falha.

## Comportamento Esperado:
- Se um serviço estiver a falhar, propõe a leitura dos logs.
- Se o utilizador pedir para analisar o erro, utiliza `get_service_logs`, analisa o output técnico e explica o problema de forma clara e resumida.
