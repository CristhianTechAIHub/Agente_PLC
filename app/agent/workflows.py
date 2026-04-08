# codigo principal para la creación de un agente
from langchain_community.document_loaders import PyPDFDirectoryLoader
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

# 1. Cargar PDFs
loader = PyPDFDirectoryLoader("../data")
docs = loader.load()

# 2. Cortar el texto en fragmentos (chunks) digeribles para el LLM
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 3. Crear la base de datos vectorial en memoria (FAISS)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
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

