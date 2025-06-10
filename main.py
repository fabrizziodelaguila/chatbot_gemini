from fastapi import FastAPI, HTTPException, Depends, Request, Body
from pydantic import BaseModel
from database import get_db
from crud import obtener_destinos_por_categoria, obtener_todas_las_categorias, consultar_gemini
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from jose import JWTError, jwt
import time
from passlib.hash import bcrypt
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

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

def crear_token(user_id, username):
    payload = {
        "id": user_id,  # Este campo es esencial para el historial del chat
        "username": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print("🛡️ Token generado:", token)  # 👈 Agregado para depurar
    return token

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    print("🔐 Authorization header recibido:", auth_header)

    if not auth_header:
        print("❌ No Authorization header found")
        raise HTTPException(status_code=403, detail="Token requerido")

    try:
        scheme, token = auth_header.split(" ")
        print("📦 Token extraído:", token)
    except ValueError as e:
        print("❌ Error al dividir el Authorization header:", e)
        raise HTTPException(status_code=403, detail="Formato del token inválido")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("📨 Payload decodificado:", payload)

        username = payload.get("username")
        user_id = payload.get("id")

        if username is None or user_id is None:
            print("❌ Faltan campos en el payload (¿token viejo?)")
            raise HTTPException(status_code=403, detail="Token inválido")

        return {"username": username, "user_id": user_id}

    except JWTError as e:
        print("❌ Error al decodificar el token JWT:", e)
        raise HTTPException(status_code=403, detail="Token inválido")

@app.get("/")
def home():
    return {"message": "API funcionando"}

@app.post("/chat")
def obtener_destinos(data: ChatRequest, user: dict = Depends(get_current_user)):
    db = get_db()
    destinos = obtener_destinos_por_categoria(db, data.categoria)

    if not destinos:
        respuesta_gemini = consultar_gemini(f"{data.categoria}", user["user_id"])
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

@app.post("/refresh-token")
def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=403, detail="Token requerido")

    try:
        scheme, token = auth_header.split(" ")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=403, detail="Token inválido")
    except:
        raise HTTPException(status_code=403, detail="Token inválido")

    # Ahora buscas el ID real del usuario en la base de datos local
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username=?", (username,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_id = row[0]
    nuevo_token = crear_token(user_id, username)
    return {"token": nuevo_token}

@app.post("/login")
def login(data: LoginRequest = Body(...)):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, password FROM usuarios WHERE username=?",
        (data.username,)
    )
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user_id, password_hash = user

    if not bcrypt.verify(data.password, password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token(user_id, data.username)
    print(f"✅ Login exitoso para {data.username} | ID: {user_id}")
    return {"token": token}

@app.post("/register")
def register(data: RegisterRequest):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username=?", (data.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    password_hash = bcrypt.hash(data.password)
    cursor.execute(
        "INSERT INTO usuarios (username, password) VALUES (?, ?)",
        (data.username, password_hash)
    )
    db.commit()
    return {"message": "Usuario registrado exitosamente"}
