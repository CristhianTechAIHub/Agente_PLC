# codigo principal para la creación de un agente
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from utils.utils import SYSTEM_PROMPT
from utils.llm_config import get_llm
from models.schemas import Context, ResponseFormat
from tools.tools import search_local_pdfs
from langchain.agents.structured_output import ToolStrategy



# 1. Cargar PDFs
loader = PyPDFDirectoryLoader("./docs")
docs = loader.load()

# 2. Cortar el texto en fragmentos (chunks) digeribles para el LLM
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 3. Crear la base de datos vectorial en memoria (FAISS)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(splits, embeddings)

# 4. Convertirlo en un "retriever" (buscador)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # k=3 significa que traerá los 3 fragmentos más relevantes

# Inyectamos el retriever en nuestro contexto actual
current_context = Context(
    user_id="1", 
    pdf_retriever=retriever 
)

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

# asignamos el id de conversacion
config = {"configurable": {"thread_id": "1"}}

# Ahora, cuando el agente invoque search_local_pdfs, tendrá acceso al buscador pre-cargado
response = agent.invoke(
    {"messages": [{"role": "user", "content": "según el manual del SCALANCE SC-600, como debo conectar la alimentación del equipo?"}]},
    config=config,
    context=current_context
)

print("\nRESPUESTA DEL AGENTE:")
print("------------------------")
print(response['structured_response'] if 'structured_response' in response else response)
print("------------------------")


