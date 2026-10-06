
---
criado_em: 2026-10-05
status: 
tags:
  - projeto
  - infraestrutura
---
# Configurar Nginx AI Manager

## 🎯 Objetivo do Projeto
Descreva aqui o que este serviço faz (ex: Servidor de IA, Proxy, Banco de Dados).

## ⚙️ Arquivos de Configuração (Quadlets/Podman)
*Arquivos `.container`, `.network` ou `.volume` usados neste projeto.*

```bash
[Unit]
Description=Nginx AI Manager Container
After=network-online.target
Wants=network-online.target

[Container]
Image=docker.io/library/nginx:latest
ContainerName=nginx-ai-manager
PublishPort=80:80
PublishPort=443:443
# Descomente a linha abaixo caso precise persistir arquivos de configuração ou logs
# Volume=/caminho/no/host:/etc/nginx:Z

[Service]
Restart=always
TimeoutStartSec=300

[Install]
WantedBy=default.target
```


### 💡 Dicas de uso:

1. Salve este conteúdo em um arquivo chamado `nginx-ai-manager.container` dentro do diretório `~/.config/containers/systemd/`.
2. Lembre-se de ajustar os caminhos de volumes caso precise mapear configurações locais, utilizando sempre a flag `:Z` no final para garantir a compatibilidade com o SELinux, conforme listado nas tarefas do seu note [Configurar Nginx AI Manager](app://obsidian.md/Configurar%20Nginx%20AI%20Manager).
3. Após salvar, execute os comandos para carregar e iniciar o serviço:

## 🤖 Análises e Prompts (Gemini)

_Use este espaço para salvar as explicações do Gemini sobre erros, melhorias de código ou diagramas deste serviço._

## ✅ Tarefas do Projeto

- [x] Criar arquivo do Quadlet. ✅ 2026-10-05
    
- [x] Configurar mapeamento de volumes e portas. ✅ 2026-10-05
    
- [x] Ajustar permissões SELinux (flag `:Z`). ✅ 2026-10-05
    
- [x] Recarregar daemon (`systemctl --user daemon-reload`). ✅ 2026-10-05
    
- [x] Iniciar serviço (`systemctl --user start nome.service`). ✅ 2026-10-05