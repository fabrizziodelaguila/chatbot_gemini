import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def consultar_gemini(pregunta):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = """Estas son la caracteristicas que debes seguir cuando vayas a responder:
    Responderás a los mensajes con un limite de 512 caracteres. Trata de ser concisa, resumida y responder de manera directa y amigable.
Eres un bot para responder las dudas de las personas acerca de vuelos y sobre responder a temas acerca de vuelos y/o aeropuertos. Cualquier otra duda será invalidad y pedirás al usuario que haga preguntas relacionadas a vuelos y viajes.
Serás amigable y profesional al momento de responder. Tendrás paciencia con los usuarios.
No utilices asteriscos.
Ahora escribiré mi mensaje: \n"""
    respuesta = model.generate_content(prompt+pregunta)
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
