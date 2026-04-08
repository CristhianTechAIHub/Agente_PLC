from dataclasses import dataclass

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str
    pdf_retriever : any

@dataclass
class ResponseFormat:
    """Esquema de la respuesta estructurada del agente técnico."""
    respuesta_tecnica: str
    requiere_mas_informacion: bool
    fuente_sugerida: str | None = None