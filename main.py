from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from database import get_db
from crud import obtener_destinos_por_categoria, obtener_todas_las_categorias, consultar_gemini
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from jose import JWTError, jwt
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel): 
    categoria: str

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=403, detail="Token requerido")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

@app.get("/")
def home():
    return {"message": "API funcionando"}

@app.post("/chat")
def obtener_destinos(data: ChatRequest, user_id: int = Depends(get_current_user)):
    db = get_db()
    destinos = obtener_destinos_por_categoria(db, data.categoria)

    if not destinos:
        respuesta_gemini = consultar_gemini(f"{data.categoria}", user_id)        
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


