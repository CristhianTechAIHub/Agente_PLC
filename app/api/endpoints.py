from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from agent.workflows import consultar_agente

router = APIRouter()

class UserQuery(BaseModel):
    pregunta: str


@router.post("/chat")
async def consultar_pregunta(query: UserQuery):

    agent_response = await consultar_agente(query.pregunta)

    return {"respuesta": agent_response}