## 5. Ecossistema de Inteligência Artificial Local

O laboratório executa modelos fundacionais de Inteligência Artificial de forma 100% local, garantindo privacidade absoluta dos dados (sem chamadas a APIs na nuvem externas) e latência controlada.

### 5.1. LLM e Geração de Texto (Ollama + Open-WebUI)

O motor de raciocínio de texto é gerido pelo **Ollama**, que descarrega e executa Large Language Models (LLMs) quantizados diretamente no hardware local.

- **Interface:** A interação humana com os modelos é feita através do **Open-WebUI**, uma interface avançada que consome a API interna do Ollama (acessível via `chat.ia.local`).
    
- **Isolamento de Dados:** Os pesos dos modelos (pesados em GB) e as bases de dados de conversas estão isolados em volumes geridos pelo Podman (`ollama-data.volume` e `open-webui-data.volume`), garantindo que atualizações dos contentores não apagam os históricos.
    

### 5.2. Motor de Leitura Neural (OpenedAI-Speech / XTTS v2)

O ecossistema implementa clonagem de voz _Zero-Shot_ (capacidade de clonar uma voz fornecendo apenas um pequeno ficheiro de áudio de exemplo) através do motor **Coqui XTTS v2**.

- **Simulação de API (Drop-in Replacement):** O serviço utiliza a imagem `openedai-speech`, que envolve o motor XTTS numa API REST que imita perfeitamente o formato da OpenAI (`/v1/audio/speech`). Isto permite que qualquer software compatível com a OpenAI funcione nativamente com este motor local.
    
- **Configuração da Voz Nativa:**
    
    - Modelo configurado: `tts-1-hd`.
        
    - Foi mapeado um ficheiro físico `brasileira.wav` para o interior do volume `tts-voices.volume`.
        
    - O perfil da voz foi batizado de `nova`, forçando o modelo XTTS a extrair as características acústicas (timbre, sotaque português do Brasil, tom feminino) do ficheiro `.wav` em tempo real.