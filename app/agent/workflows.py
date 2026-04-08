# codigo principal para la creación de un agente
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from agent.prompts import SYSTEM_PROMPT
from core.llm_config import get_llm
from core.schemas import Context, ResponseFormat
from agent.tools import search_local_pdfs
from langchain.agents.structured_output import ToolStrategy

print("Iniciando configuraciones del agente")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 1. Cargar PDFs iniciales
loader = PyPDFDirectoryLoader("../data")
docs = loader.load()

# 2. Cortar el texto en fragmentos (chunks) digeribles para el LLM
splits = text_splitter.split_documents(docs)

# 3. Crear la base de datos vectorial en memoria (FAISS)
vectorstore = FAISS.from_documents(splits, embeddings)

# 4. Convertirlo en un "retriever" (buscador)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # k=3 significa que traerá los 3 fragmentos más relevantes

checkpointer = InMemorySaver()

model = get_llm()

# creante and runt the agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[search_local_pdfs],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

print("Agente configurado y listo para recibir preguntas.")


def agregar_documentos(file_paths: list[str]) -> int:
    """
    Carga los PDFs indicados, los fragmenta e incorpora al vectorstore existente.
    Devuelve la cantidad de fragmentos añadidos.
    """
    global vectorstore, retriever

    nuevos_docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        nuevos_docs.extend(loader.load())

    if not nuevos_docs:
        return 0

    nuevos_splits = text_splitter.split_documents(nuevos_docs)
    vectorstore.add_documents(nuevos_splits)

    # Actualizar el retriever para que apunte al vectorstore ya modificado
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    return len(nuevos_splits)

# declaramos la función asíncrona para consultar al agente

async def consultar_agente(pregunta: str) -> str:
    # Inyectamos el retriever en nuestro contexto actual
    current_context = Context(
        user_id="1", 
        pdf_retriever=retriever 
    )

    # asignamos el id de conversacion
    config = {"configurable": {"thread_id": "1"}}

    # Ahora, cuando el agente invoque search_local_pdfs, tendrá acceso al buscador pre-cargado
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": pregunta}]},
        config=config,
        context=current_context
    )

    if 'structured_response' in response:
        # Como usaste ToolStrategy(ResponseFormat), la respuesta es un objeto.
        # Convirtámoslo a string temporalmente para ver qué contiene.
        # (Si tu ResponseFormat tiene un campo específico como 'respuesta_final', 
        # deberías usar: return response['structured_response'].respuesta_final)
        return str(response['structured_response'].respuesta_tecnica)

    elif 'messages' in response:
        # Si es una respuesta normal de LangGraph, sacamos el contenido del último mensaje (la IA)
        return response['messages'][-1].content
        
    else:
        # Fallback de seguridad por si cambia la estructura
        return str(response)

