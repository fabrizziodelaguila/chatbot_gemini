import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def consultar_gemini(pregunta):
    model = genai.GenerativeModel("gemini-2.0-flash")
    respuesta = model.generate_content(pregunta)
    return respuesta.text

def obtener_destinos_por_categoria(db, categoria):
    query = """
    SELECT d.name, d.description, d.price, d.rating
    FROM destinos d
    INNER JOIN categoria c ON d.categoria_id = c.id 
    WHERE c.name = ?
    """
    cursor = db.cursor()
    cursor.execute(query, (categoria,))
    resultados = cursor.fetchall()
    
    
    destinos = [
        {"name": row[0], "description": row[1], "price": row[2], "rating": row[3]}
        for row in resultados
    ]
    
    return destinos 

def obtener_todas_las_categorias(db):
    query = "SELECT name FROM categoria"
    cursor = db.cursor()
    cursor.execute(query)
    categorias = [row[0] for row in cursor.fetchall()]
    
    return {"categorias": categorias}  
