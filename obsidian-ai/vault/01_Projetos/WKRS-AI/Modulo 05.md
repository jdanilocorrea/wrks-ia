## 6. Desenvolvimento Customizado: VoiceReader

O **VoiceReader** é a interface Frontend desenvolvida internamente para interagir de forma otimizada com o motor TTS. Foi desenhada para ser ultraleve e construída sob as premissas de desenvolvimento moderno em Python.

### 6.1. Arquitetura da Aplicação (App Gradio)

- A interface gráfica é construída em **Gradio**, servida internamente na porta `7860`.
    
- **Otimização de Dependências:** Em vez de utilizar bibliotecas pesadas como `requests` ou `openai` para fazer chamadas HTTP ao motor XTTS, a aplicação utiliza a biblioteca nativa `urllib` do Python, reduzindo drasticamente a superfície de ataque e o tamanho do contentor.
    
- **Persistência de Ativos (_Assets_):** Sempre que um áudio é gerado, o código guarda o ficheiro `.wav` localmente na pasta interna `/app/audios` com _timestamp_ (ex: `leitura_20260925_221430.wav`). Através de um _Bind Mount_ físico no Quadlet, esta pasta é refletida instantaneamente na pasta pessoal do utilizador no Fedora (`~/Documentos/Audios_IA`), garantindo acesso fácil aos áudios sem precisar de extraí-los do contentor.
    

### 6.2. Gestão Moderna com `uv` (GitOps Python)

A aplicação abandonou ficheiros obsoletos como `requirements.txt` em favor do padrão moderno `pyproject.toml`, gerido pelo **`uv`** (um instalador de pacotes em Rust, que substitui o `pip` oferecendo velocidades de resolução extremas).

**Ficheiro pyproject.toml:**

Ini, TOML

```
[project]
name = "voicereader"
version = "0.2.0"
description = "Leitor Neural Local (XTTS v2) com Observabilidade OTel"
requires-python = ">=3.12"
dependencies = [
    "gradio>=4.0.0",
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp"
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I"]
```

### 6.3. Contentorização Específica (Containerfile)

Em vez de utilizar uma imagem pública genérica, o VoiceReader tem o seu próprio processo de compilação (_Build_) local através de um `Containerfile`.

**Destaques do Containerfile:**

1. **Base Leve:** Utiliza a imagem oficial `python:3.12-slim`.
    
2. **Injeção do `uv`:** Copia o binário do `uv` diretamente da imagem oficial da _Astral_, permitindo a instalação ultrarrápida do ecossistema a partir do `pyproject.toml`.
    
3. **Compilação Modular:** O _build_ é executado a partir da raiz do monorepo, gerando a imagem local `localhost/voicereader:latest` que o systemd invoca posteriormente.
    

Dockerfile

```
FROM python:3.12-slim
WORKDIR /app
# Injeta o uv diretamente na imagem base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copia e instala as dependências modernas
COPY pyproject.toml .
RUN uv pip install --system .
COPY src/ ./src/
CMD ["python", "src/app.py"]
```