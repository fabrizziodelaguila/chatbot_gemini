from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db
from crud import obtener_destinos_por_categoria, obtener_todas_las_categorias
from crud import consultar_gemini
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CategoriaRequest(BaseModel):
    categoria: str

@app.get("/")
def home():
    return {"message": "API funcionando"}

@app.post("/chat")
def obtener_destinos(data: CategoriaRequest):
    db = get_db()
    destinos = obtener_destinos_por_categoria(db, data.categoria)

    if not destinos:
        respuesta_gemini = consultar_gemini(f"{data.categoria}")        
        return {"respuesta_gemini": respuesta_gemini}

    return destinos

@app.get("/categorias")
def listar_categorias():
    db = get_db()
    return obtener_todas_las_categorias(db)

@app.get("/consulta")
def consulta():
    file_path = os.path.join(os.getcwd(), "static", "index.html")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)


