from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

router = APIRouter()

class UserQuery(BaseModel):
    pregunta: str


@router.post("/chat")
async def consultar_pregunta(query: UserQuery):

    await asyncio.sleep(2)

    agent_response = f"¡Hola! Recibí tu pregunta: '{query.pregunta}'. El agente real de LangChain pronto estará conectado aquí."

    return {"respuesta": agent_response}