
  
## 3. Infraestrutura Base e Orquestração (GitOps e Quadlets)

O coração do laboratório assenta na declaração da infraestrutura como código (IaC). Em vez de comandos `podman run` imperativos, o estado desejado de cada componente é gravado em ficheiros geridos nativamente pelo `systemd` do Fedora, garantindo que os serviços sobrevivem a reboots e são fáceis de versionar no Git.

  

### 3.1. Estrutura de Diretórios do Monorepo

A infraestrutura está fisicamente guardada na pasta `~/work/development/github/wrks-ia/`. A separação de responsabilidades reflete as melhores práticas de microarquitetura:

  

Plaintext

```
wrks-ia/
├── ai-squad-quadlets/       # (Core) Ficheiros de declaração do Podman (Rede, Volumes, Contentores)
├── nginx-manager-ai/        # Persistência física do Proxy Reverso (Certificados e DB)
├── voicereader/             # Código-fonte Python, pyproject.toml e Containerfile do TTS
└── antigravity-sandbox/     # Ambiente isolado de Agentes e Skills (.agents/)
```

### 3.2. A Rede Interna (`ai-net`)

O isolamento de rede é o principal mecanismo de segurança do laboratório. Todos os contentores são instruídos a acoplar-se a esta rede privada gerida pelo Podman (Container Network Interface - CNI).

  

**Declaração (ai-net.network):**

  

Ini, TOML

```
[Network]
NetworkName=ai-net
DisableDNS=false
```

- O parâmetro `DisableDNS=false` é crítico, pois permite a resolução de nomes interna. É isto que permite que o contentor `nginx-manager-ai` faça proxy para `http://open-webui:8080` apenas chamando o nome do contentor de destino, sem conhecer os endereços IP.
    
      
    

### 3.3. Padrão de Quadlets (Exemplo do Motor TTS)

Um Quadlet converte a configuração complexa de um contentor num serviço Linux nativo. A anatomia típica de um Quadlet do nosso sistema inclui a definição da imagem, o mapeamento de volumes persistentes e o bloqueio de exposição externa.

  

**Declaração (tts.container):**

  

Ini, TOML

```
[Unit]
Description=Motor XTTS v2 Neural
After=network-online.target

[Container]
Image=ghcr.io/matatonic/openedai-speech:latest
ContainerName=tts
Network=ai-net.network

# Bloqueio de rede externa (Segurança por design)
# PublishPort=8000:8000 (Comentado intencionalmente)

# Volumes geridos nativamente pelo Podman
Volume=tts-voices.volume:/app/voices
Volume=tts-config.volume:/app/config

[Install]
WantedBy=default.target
```

- _Operação GitOps:_ Todos os Quadlets no monorepo possuem um _Symlink_ (link simbólico) para a pasta de leitura do systemd no Fedora (`~/.config/containers/systemd/`). Atualizar o ficheiro no Git reflete-se imediatamente no sistema operativo após um `systemctl --user daemon-reload`.
    
      
    

### Módulo 3 👇

## 4. Segurança e Encaminhamento de Tráfego

Para fechar o laboratório a acessos diretos no Fedora (evitando as clássicas vulnerabilidades de portas abertas na rede local), implementou-se um Proxy Reverso central.

  

### 4.1. Nginx Proxy Manager AI (`nginx-manager-ai`)

O contentor encarregue de ser a "Porta da Frente" do sistema e o gestor central de certificados.

  

- **Desafio Técnico Resolvido (s6-overlay em Rootless):** Imagens complexas como o NPM usam o `s6-overlay` que exige privilégios de `root` para arrancar os seus serviços internos. No Podman rootless, foi necessário declarar `User=0:0` no Quadlet. Isto engana o contentor fazendo-o acreditar que é root, quando na verdade o Podman mapeia de forma segura para o UID não-privilegiado do hospedeiro.
    
      
    
- **Isolamento de Portas:** É o único Quadlet do monorepo com a diretiva `PublishPort` ativa (`80:80`, `81:81`, `443:443`). Nenhum outro microsserviço da `ai-net` pode ser atingido pelo exterior (Fedora ou Rede Local).
    
      
    

### 4.2. Resolução de DNS Local (Ficheiro Hosts)

Para evitar o uso do formato `localhost:porta` e testar lógicas de rotas baseadas em _Hostname_ (fundamental para testes de APIs REST e ambientes de _Stage_), o ficheiro `/etc/hosts` do Fedora foi modificado para apontar domínios amigáveis para a máquina local (onde o Nginx está à escuta).

  

**Entradas de DNS Locais:**

  

Plaintext

```
127.0.0.1   chat.ia.local leitor.ia.local tts.ia.local trace.ia.local
```

### 4.3. Rotas de Encaminhamento Interno

O Nginx interceta o tráfego baseado no nome do domínio e reencaminha para a porta interna do contentor de destino, que muitas vezes é diferente da porta externa configurada.

  

|**Subdomínio (Hosts)**|**Destino Interno (Network ai-net)**|**Serviço Servido**|
|---|---|---|
|`chat.ia.local`|`http://open-webui:8080`|Interface Llama|
|`leitor.ia.local`|`http://voicereader:7860`|App Gradio (TTS)|
|`tts.ia.local`|`http://tts:8000`|API XTTS v2|
|`trace.ia.local`|`http://jaeger-otel:16686`|Dashboard Jaeger|
