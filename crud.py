import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import json
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

call_cat = requests.get("https://vuelosapi-e8e4cke5aubjdnah.canadacentral-01.azurewebsites.net/api/categorias")
DB_CAT = call_cat.json()
DB_CAT_NAMES = l = [ i["name"] for i in DB_CAT['categories']]

call_vuelos = requests.get("https://vuelosapi-e8e4cke5aubjdnah.canadacentral-01.azurewebsites.net/api/destinos")
DB_FLY_NOT_NAMES = ["image","categoria_id","id","location"]
DB_FLY = call_vuelos.json()
DB_FLY_DESTINY = [
    {k: v for k, v in x.items() if k not in DB_FLY_NOT_NAMES}
    for x in DB_FLY
]

for i in DB_FLY_DESTINY:
    for k,v in i.items():
        if k == "duration":
            v = f"{v} hours"
        if k == "price":
            v = f"{v} Nuevos Soles Peruanos"
        if k == "rating":
            v = f"{v}/5.0"
# DB_FLY = l = [ i["name"] for i in DB_CAT['categories']]

def consultar_gemini(pregunta):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""Estas son la caracteristicas que debes seguir cuando vayas a responder:
    Responderás a los mensajes con un limite de 2048     caracteres. Trata de ser resumido y responder de manera directa y amigable.
Eres un bot para responder las dudas de las personas acerca de vuelos de viajes y sobre responder a temas acerca de vuelos y/o aeropuertos. Cualquier otra duda será invalida y pedirás al usuario que haga preguntas relacionadas a vuelos, viajes o sus categorias disponibles.
Serás amigable y profesional al momento de responder. Tendrás paciencia con los usuarios.
No utilices asteriscos. Estas son las categorias de viaje: {DB_CAT_NAMES}.
Estos son los viajes disponibles. Estan en un json: {DB_FLY_DESTINY}. Sus duraciones en "duration" están en horas.
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


if __name__ == "__main__":
    pass