from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.endpoints import router as api_router
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE_DIR, "static", "index.html")

# instanciamos la aplicación FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return FileResponse(HTML_PATH)

app.include_router(api_router)