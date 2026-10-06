
---
criado_em: {{date}}
status: 
tags:
  - projeto
  - infraestrutura
---
# {{title}}

## 🎯 Objetivo do Projeto
Descreva aqui o que este serviço faz (ex: Servidor de IA, Proxy, Banco de Dados).

## ⚙️ Arquivos de Configuração (Quadlets/Podman)
*Arquivos `.container`, `.network` ou `.volume` usados neste projeto.*

```bash
# Cole seus comandos ou arquivos aqui
```

## 🤖 Análises e Prompts (Gemini)

_Use este espaço para salvar as explicações do Gemini sobre erros, melhorias de código ou diagramas deste serviço._

## ✅ Tarefas do Projeto

- [ ] Criar arquivo do Quadlet.
    
- [ ] Configurar mapeamento de volumes e portas.
    
- [ ] Ajustar permissões SELinux (flag `:Z`).
    
- [ ] Recarregar daemon (`systemctl --user daemon-reload`).
    
- [ ] Iniciar serviço (`systemctl --user start nome.service`).