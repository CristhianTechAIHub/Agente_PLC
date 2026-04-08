from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import asyncio
import os
import shutil
from agent.workflows import consultar_agente, agregar_documentos

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

class UserQuery(BaseModel):
    pregunta: str


@router.post("/chat")
async def consultar_pregunta(query: UserQuery):
    agent_response = await consultar_agente(query.pregunta)
    return {"respuesta": agent_response}


@router.post("/upload")
async def cargar_documentos(archivos: list[UploadFile] = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)

    rutas_guardadas = []
    for archivo in archivos:
        if not archivo.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"'{archivo.filename}' no es un PDF.")

        destino = os.path.join(DATA_DIR, archivo.filename)
        with open(destino, "wb") as f:
            shutil.copyfileobj(archivo.file, f)
        rutas_guardadas.append(destino)

    fragmentos = agregar_documentos(rutas_guardadas)

    return {
        "archivos_cargados": [a.filename for a in archivos],
        "fragmentos_indexados": fragmentos
    }