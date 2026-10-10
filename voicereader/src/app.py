import gradio as gr
import urllib.request
import urllib.error
import json
from datetime import datetime
import os

# --- Configuração do OpenTelemetry ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Identifica o nosso serviço no Jaeger
resource = Resource(attributes={"service.name": "voicereader-ui"})
provider = TracerProvider(resource=resource)
# Envia os dados para o Jaeger pela rede interna (ai-net) na porta 4318 (HTTP)
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger-otel:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("voicereader.tracer")
# -------------------------------------

os.makedirs("/app/audios", exist_ok=True)

def gerar_audio_local(texto):
    # Span Principal: Mede o tempo total do clique até à resposta na interface
    with tracer.start_as_current_span("fluxo_completo_geracao") as span_principal:
        span_principal.set_attribute("app.tamanho_texto", len(texto))
        
        url = "http://tts:8000/v1/audio/speech"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "model": "tts-1-hd",
            "input": texto,
            "voice": "nova"
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            # Sub-Span 1: Mede exclusivamente a latência do Motor TTS (NVIDIA/CPU)
            with tracer.start_as_current_span("requisicao_api_tts") as api_span:
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        api_span.set_attribute("http.status_code", 200)
                        
                        # Sub-Span 2: Mede o I/O do disco no momento da gravação
                        with tracer.start_as_current_span("gravacao_disco_local") as disco_span:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            caminho_saida = f"/app/audios/leitura_{timestamp}.wav"
                            disco_span.set_attribute("app.caminho_arquivo", caminho_saida)
                            
                            with open(caminho_saida, "wb") as f:
                                f.write(response.read())
                            return caminho_saida
                            
        except urllib.error.HTTPError as e:
            erro_msg = e.read().decode('utf-8')
            span_principal.record_exception(e)
            span_principal.set_status(trace.Status(trace.StatusCode.ERROR, erro_msg))
            raise gr.Error(f"Erro no motor TTS local: {e.code} - {erro_msg}")
        except urllib.error.URLError as e:
            span_principal.record_exception(e)
            span_principal.set_status(trace.Status(trace.StatusCode.ERROR, str(e.reason)))
            raise gr.Error(f"Falha de ligação ao motor TTS: {e.reason}")

with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Leitor Neural Local (Instrumentado com OTel)")
    gr.Markdown("Os rastos de execução são enviados automaticamente para o **Jaeger**.")
    
    with gr.Row():
        text_input = gr.Textbox(label="Texto para Ler", lines=5, placeholder="Escreva aqui...")
    
    generate_btn = gr.Button("Gerar Áudio Neural", variant="primary")
    audio_output = gr.Audio(label="Áudio Gerado")
    
    generate_btn.click(fn=gerar_audio_local, inputs=text_input, outputs=audio_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
