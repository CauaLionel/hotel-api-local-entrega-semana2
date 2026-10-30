
from pathlib import Path
import hashlib

import httpx
import chromadb

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import HotelModel, QuartoModel, ReservaModel


router = APIRouter(
    prefix="/ai",
    tags=["Inteligência Artificial"]
)


# CONFIGURAÇÕES DO OLLAMA

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
OLLAMA_EMBED_URL = "http://host.docker.internal:11434/api/embed"

MODEL = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"

DOCUMENT_PATH = Path("/app/documentos/hotel.txt")


# CONFIGURAÇÃO DO CHROMADB

CHROMA_PATH = "/app/chroma_data"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="documentos_hotel",
    metadata={"hnsw:space": "cosine"}
)


class TextRequest(BaseModel):
    text: str


# GERAÇÃO DE RESPOSTAS PELO OLLAMA

async def ask_ai(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )

            response.raise_for_status()
            return response.json()["response"]

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao Ollama."
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="A IA demorou demais para responder."
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Erro ao solicitar resposta ao Ollama."
        )


# TOOL 1: CONSULTAR HOTÉIS

def consultar_hotel(db: Session):
    hoteis = db.query(HotelModel).all()

    return [
        {
            "id": hotel.id,
            "nome": hotel.nome,
            "localizacao": hotel.localizacao,
            "nota": hotel.nota
        }
        for hotel in hoteis
    ]


# TOOL 2: CONSULTAR RESERVAS

def consultar_reserva(db: Session):
    reservas = db.query(ReservaModel).all()

    return [
        {
            "id": reserva.id,
            "hospede": reserva.hospede,
            "data_entrada": reserva.data_entrada,
            "data_saida": reserva.data_saida,
            "quarto_id": reserva.quarto_id
        }
        for reserva in reservas
    ]


# TOOL 3: CONSULTAR QUARTOS DISPONÍVEIS

def consultar_disponibilidade(db: Session):
    quartos = db.query(QuartoModel).filter(
        QuartoModel.disponivel.is_(True)
    ).all()

    return [
        {
            "id": quarto.id,
            "numero": quarto.numero,
            "preco": quarto.preco,
            "hotel_id": quarto.hotel_id,
            "disponivel": quarto.disponivel
        }
        for quarto in quartos
    ]


# RAG - ETAPA 1: CHUNKING

def dividir_em_chunks(
    texto: str,
    tamanho: int = 500,
    sobreposicao: int = 80
):
    chunks = []
    passo = tamanho - sobreposicao

    for inicio in range(0, len(texto), passo):
        trecho = texto[inicio:inicio + tamanho].strip()

        if trecho:
            chunks.append(trecho)

    return chunks


# RAG - ETAPA 2: EMBEDDINGS

async def gerar_embeddings(textos: list[str]):
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_EMBED_URL,
                json={
                    "model": EMBEDDING_MODEL,
                    "input": textos
                }
            )

            response.raise_for_status()
            return response.json()["embeddings"]

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao Ollama para gerar embeddings."
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="O Ollama demorou demais para gerar embeddings."
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Erro ao gerar embeddings."
        )


# RAG - ETAPA 3: INDEXAÇÃO NO CHROMADB

async def indexar_documento():

    if not DOCUMENT_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Documento do hotel não encontrado."
        )

    documento = DOCUMENT_PATH.read_text(encoding="utf-8")

    hash_documento = hashlib.sha256(
        documento.encode("utf-8")
    ).hexdigest()

    metadata = collection.metadata or {}

    # Evita indexar novamente se o documento não mudou
    if (
        metadata.get("document_hash") == hash_documento
        and collection.count() > 0
    ):
        return

    chunks = dividir_em_chunks(documento)

    if not chunks:
        raise HTTPException(
            status_code=500,
            detail="O documento está vazio."
        )

    embeddings = await gerar_embeddings(chunks)

    # Remove os trechos antigos do documento
    if collection.count() > 0:
        collection.delete(
            where={"source": "hotel.txt"}
        )

    ids = [
        f"hotel-{hash_documento[:12]}-{i}"
        for i in range(len(chunks))
    ]

    metadados = [
        {
            "source": "hotel.txt",
            "chunk": i
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadados
    )

    # Atualiza somente o hash do documento.
    # A função de distância já foi definida na criação da coleção.
    collection.modify(
        metadata={
            "document_hash": hash_documento
        }
    )


# RAG - ETAPA 4: BUSCA SEMÂNTICA

async def buscar_contexto(pergunta: str):

    await indexar_documento()

    embedding_pergunta = await gerar_embeddings([pergunta])

    quantidade = min(3, collection.count())

    if quantidade == 0:
        return ""

    resultados = collection.query(
        query_embeddings=embedding_pergunta,
        n_results=quantidade
    )

    documentos = resultados["documents"][0]

    return "\n\n".join(documentos)


# RESUMIR TEXTO

@router.post("/summarize")
async def summarize(data: TextRequest):

    resumo = await ask_ai(
        "Resuma o texto em português brasileiro, "
        "preservando as informações importantes:\n\n"
        + data.text
    )

    return {
        "texto_original": data.text,
        "resumo": resumo
    }


# CLASSIFICAR TEXTO

@router.post("/classify")
async def classify(data: TextRequest):

    classificacao = await ask_ai(
        "Classifique o texto em uma categoria adequada "
        "e explique brevemente o motivo. Responda em português:\n\n"
        + data.text
    )

    return {
        "texto_original": data.text,
        "classificacao": classificacao
    }


# ANALISAR TEXTO

@router.post("/analyze")
async def analyze(data: TextRequest):

    analise = await ask_ai(
        "Analise o assunto principal, os pontos importantes "
        "e os possíveis problemas do texto:\n\n"
        + data.text
    )

    return {
        "texto_original": data.text,
        "analise": analise
    }


# CONSULTA INTELIGENTE

@router.post("/ask")
async def ask_question(
    data: TextRequest,
    db: Session = Depends(get_db)
):

    pergunta = data.text.lower()

    # TOOL CALLING: RESERVAS

    if any(p in pergunta for p in [
        "reserva",
        "reservas",
        "hóspede",
        "hospede",
        "check-in de",
        "check-out de"
    ]):

        dados = consultar_reserva(db)
        fonte = "banco de dados: reservas"

    # TOOL CALLING: DISPONIBILIDADE

    elif (
        "dispon" in pergunta
        or any(p in pergunta for p in [
            "quarto livre",
            "quartos livres",
            "vaga",
            "vagas"
        ])
    ):

        dados = consultar_disponibilidade(db)
        fonte = "banco de dados: quartos disponíveis"

    # TOOL CALLING: HOTÉIS

    elif any(p in pergunta for p in [
        "quais hotéis",
        "quais hoteis",
        "listar hotéis",
        "listar hoteis",
        "hotel cadastrado",
        "hotéis cadastrados",
        "hoteis cadastrados",
        "localização dos hotéis",
        "localizacao dos hoteis"
    ]):

        dados = consultar_hotel(db)
        fonte = "banco de dados: hotéis"

    # RAG: CONSULTA AOS DOCUMENTOS

    else:

        contexto = await buscar_contexto(data.text)

        resposta = await ask_ai(f"""
Você é um assistente de atendimento de hotel.

Responda em português brasileiro utilizando
somente o contexto recuperado dos documentos.

REGRAS:
- Não invente informações.
- Não utilize conhecimentos externos.
- Se o contexto não responder à pergunta,
  informe que não encontrou essa informação.
- Seja direto e objetivo.

CONTEXTO RECUPERADO:
{contexto}

PERGUNTA:
{data.text}

RESPOSTA:
""")

        return {
            "pergunta": data.text,
            "resposta": resposta,
            "fonte": "ChromaDB - documentos/hotel.txt",
            "contexto_recuperado": contexto
        }

    # RESPOSTAS DIRETAS DO POSTGRESQL

    if not dados:

        resposta = "Nenhum registro foi encontrado no sistema."

    elif fonte == "banco de dados: hotéis":

        resposta = f"Encontrei {len(dados)} hotéis cadastrados:\n"

        for hotel in dados:
            resposta += (
                f"\n- {hotel['nome']}"
                f" (ID: {hotel['id']})"
                f" | Localização: {hotel['localizacao']}"
                f" | Nota: {hotel['nota']}"
            )

    elif fonte == "banco de dados: reservas":

        resposta = f"Encontrei {len(dados)} reservas cadastradas:\n"

        for reserva in dados:
            resposta += (
                f"\n- Reserva {reserva['id']}"
                f" | Hóspede: {reserva['hospede']}"
                f" | Entrada: {reserva['data_entrada']}"
                f" | Saída: {reserva['data_saida']}"
                f" | Quarto ID: {reserva['quarto_id']}"
            )

    else:

        resposta = f"Encontrei {len(dados)} quartos disponíveis:\n"

        for quarto in dados:
            resposta += (
                f"\n- Quarto {quarto['numero']}"
                f" | Hotel ID: {quarto['hotel_id']}"
                f" | Preço: R$ {quarto['preco']:.2f}"
            )

    return {
        "pergunta": data.text,
        "resposta": resposta,
        "fonte": fonte,
        "dados_consultados": dados
    }
