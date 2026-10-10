## 7. Observabilidade Distribuída (OpenTelemetry)

Numa arquitetura de microsserviços gerida por um Proxy Reverso, tentar debugar latências lendo logs de texto puros de contentores isolados é impossível. Por isso, o laboratório implementa uma fundação profissional de _Tracing_.

### 7.1. O Colecionador (Jaeger All-in-One)

- A espinha dorsal da observabilidade é o **Jaeger**. O seu Quadlet (`jaeger-otel.container`) levanta o serviço de forma isolada na rede `ai-net`.
    
- O Jaeger está configurado para ouvir no protocolo nativo **OTLP** (OpenTelemetry Protocol) nas portas internas `4317` (gRPC) e `4318` (HTTP).
    
- A interface gráfica para visualizar a telemetria é servida na porta interna `16686` e acessível através de `[http://trace.ia.local](http://trace.ia.local)`.
    

### 7.2. Instrumentação do Código (O caso do VoiceReader)

O código Python do VoiceReader serve como prova de conceito de instrumentação. A biblioteca `opentelemetry-sdk` é injetada nativamente na imagem do contentor, eliminando _hacks_ manuais.

**Como a Telemetria flui no código:** A geração de áudio no `app.py` está dividida em Spans (blocos de tempo) estruturados de forma hierárquica.

1. `fluxo_completo_geracao` (Span Pai): Mede o tempo total desde que o utilizador clica em "Gerar" até ao áudio aparecer no ecrã.
    
2. `requisicao_api_tts` (Span Filho): Isola e regista estritamente o tempo de resposta da rede ao contactar o LLM/Motor TTS (o estrangulamento clássico).
    
3. `gravacao_disco_local` (Span Filho): Isola a velocidade de I/O de escrita no Bind Mount físico do Fedora.
    

- _Sem Exposição de Portas:_ Porque o Python usa o endereço interno `http://jaeger-otel:4318/v1/traces`, a telemetria nunca sai da rede privada do Podman, evitando _sniffing_ na rede local do sistema operativo hospedeiro.