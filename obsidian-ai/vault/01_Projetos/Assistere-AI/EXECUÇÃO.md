
### Mão na Massa: Fase 1 - Classificador de Documentos (MVP)


Vamos começar pelo mais fácil, estruturando o projeto padrão 2026. Abra seu terminal e inicie o ambiente com `uv`:

Bash

```
# Inicializa o projeto e cria a estrutura
uv init assistere_ai
cd assistere_ai

# Adiciona dependências modernas
uv add google-generativeai pydantic python-dotenv
uv add --dev ruff

# Configura o linter (opcional, mas recomendado para o padrão de qualidade)
echo '[tool.ruff]\ntarget-version = "py312"\nline-length = 100' > pyproject.toml
```

Aqui está o código do nosso primeiro módulo de identificação e contextualização de clientes. Ele usa os recursos mais recentes do Gemini para forçar uma saída estruturada JSON que bate perfeitamente com nossas Dataclasses/Pydantic.

**Arquivo: `src/document_intelligence.py`**

Python

```
import asyncio
import os
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega chaves de API (LGPD/Segurança: nunca hardcoded)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Definição Rigorosa do Domínio de Negócio (Pydantic v2)
class DocumentCategory(str, Enum):
    IDENTIFICACAO = "Identificacao Pessoal"
    MIGRATORIO = "Documento Migratorio (RNE/Visto)"
    FISCAL = "Comprovante Fiscal / Renda"
    DESCONHECIDO = "Nao Reconhecido"

class ClientContext(BaseModel):
    full_name: str = Field(description="Nome completo do expatriado ou cliente encontrado no documento.")
    document_id: str | None = Field(default=None, description="Número do documento (CPF, Passaporte, RNE).")
    country_of_origin: str | None = Field(default=None, description="País emissor ou de origem do documento.")

class DocumentAnalysis(BaseModel):
    category: DocumentCategory
    document_type: str = Field(description="Tipo específico. Ex: 'Passaporte', 'Informe de Rendimentos', 'Protocolo Polícia Federal'.")
    client_context: ClientContext
    confidence_score: float = Field(ge=0.0, le=1.0, description="Nível de confiança da IA nesta extração (0 a 1).")
    needs_human_review: bool = Field(description="True se o documento estiver ilegível, rasurado ou gerar dúvidas fiscais/legais.")

# 2. Lógica Assíncrona de Integração com Gemini
async def analyze_document_with_gemini(file_path: Path) -> DocumentAnalysis:
    """
    Analisa um documento físico/PDF utilizando Gemini 1.5 e extrai entidades 
    estruturadas estritamente sob o schema DocumentAnalysis.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Faz o upload do arquivo temporariamente para a API do Gemini
    print(f"[Assistere Agent] Ingerindo documento: {file_path.name}...")
    uploaded_file = genai.upload_file(path=str(file_path))

    # Utilizamos o modelo Flash para triagem rápida e barata
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Você é o sistema de triagem fiscal e migratória da Assistere.
    Analise o documento anexado. Identifique a qual cliente pertence, tipifique o 
    documento e extraia as informações essenciais. Caso o documento pareça ser 
    um rascunho sem assinaturas ou esteja ilegível, marque 'needs_human_review' como true.
    """

    try:
        # Padrão 2026: Injeção de Pydantic para Structured Outputs (response_schema)
        response = await asyncio.to_thread(
            model.generate_content,
            [prompt, uploaded_file],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=DocumentAnalysis,
                temperature=0.1 # Baixa alucinação, alta precisão para compliance
            )
        )
        
        # O parse do JSON retornado pelo Gemini diretamente para o objeto Python
        analysis_result = DocumentAnalysis.model_validate_json(response.text)
        return analysis_result
        
    except ValidationError as e:
        print(f"[Erro de Validação] Falha ao estruturar os dados do LLM: {e}")
        raise
    finally:
        # Higienização: Apaga o arquivo do servidor do Google imediatamente (LGPD)
        genai.delete_file(uploaded_file.name)

# 3. Execução para Teste Local
async def main():
    # Crie um PDF fake de teste chamado 'passaporte_teste.pdf' na raiz do projeto
    test_file = Path("passaporte_teste.pdf")
    
    if test_file.exists():
        result = await analyze_document_with_gemini(test_file)
        print("\n--- Resultado da Triagem (Assistere) ---")
        print(f"Categoria: {result.category.value}")
        print(f"Tipo: {result.document_type}")
        print(f"Cliente: {result.client_context.full_name}")
        print(f"ID: {result.client_context.document_id}")
        print(f"Revisão Humana Necessária: {result.needs_human_review}")
    else:
        print("Adicione um arquivo 'passaporte_teste.pdf' para testar o pipeline.")

if __name__ == "__main__":
    asyncio.run(main())
```