from langchain.tools import tool, ToolRuntime
from core.schemas import Context 
@tool
def search_local_pdfs(query: str, runtime: ToolRuntime[Context]) -> str:
    """
    Busca información en la base de conocimientos local (documentos PDF).
    Úsala SIEMPRE que necesites responder preguntas técnicas sobre manuales, equipos o procedimientos.
    """
    # 1. Extraemos el motor de búsqueda
    retriever = runtime.context.pdf_retriever
    
    # 2. Ejecutamos la búsqueda
    documentos_encontrados = retriever.invoke(query)
    
    if not documentos_encontrados:
        return f"No se encontró información sobre '{query}' en los manuales."
        
    # 3. Formateamos la salida INCLUYENDO LA METADATA
    resultados_formateados = []
    
    for i, doc in enumerate(documentos_encontrados):
        texto = doc.page_content
        
        pagina = doc.metadata.get("page", -1) + 1 
        
        archivo_completo = doc.metadata.get("source", "Manual desconocido")
        nombre_archivo = archivo_completo.split("\\")[-1].split("/")[-1] # Limpiamos la ruta
        
        # Construimos un bloque de texto claro para Claude
        bloque = f"--- INICIO FRAGMENTO {i+1} ---\n"
        bloque += f"Fuente: {nombre_archivo} | Página: {pagina}\n"
        bloque += f"Contenido:\n{texto}\n"
        bloque += f"--- FIN FRAGMENTO {i+1} ---"
        
        resultados_formateados.append(bloque)
    
    resultados_texto = "\n\n".join(resultados_formateados)
    
    # 4. Le damos una instrucción explícita al LLM junto con los resultados
    instruccion_final = (
        f"Resultados de la búsqueda para '{query}':\n\n{resultados_texto}\n\n"
        "INSTRUCCIÓN PARA EL AGENTE: Utiliza esta información para responder. "
        "DEBES citar explícitamente el nombre del archivo y el número de página en tu respuesta final."
    )
    
    return instruccion_final