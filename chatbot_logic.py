from database import obtener_destinos_por_categoria, obtener_todas_las_categorias
from gemini_client import generar_respuesta_con_gemini

def detectar_categoria_en_pregunta(pregunta_usuario, categorias_disponibles):
    pregunta_lower = pregunta_usuario.lower()
    for categoria in categorias_disponibles:
        if categoria.lower() in pregunta_lower:
            return categoria
    return None

def responder_usuario(pregunta_usuario):
    categorias_disponibles = obtener_todas_las_categorias()
    categoria_detectada = detectar_categoria_en_pregunta(pregunta_usuario, categorias_disponibles)

    if not categoria_detectada:
        return "Lo siento, no encontré ninguna categoría en tu pregunta."

    destinos = obtener_destinos_por_categoria(categoria_detectada)

    if not destinos:
        return f"No encontré destinos en la categoría '{categoria_detectada}'."

    destinos_texto = "\n".join([
        f"{d.name}: {d.description} (${d.price}) ⭐{d.rating}" for d in destinos
    ])

    prompt = f"""
El usuario preguntó: '{pregunta_usuario}'.
Aquí hay destinos turísticos de la categoría '{categoria_detectada}':
{destinos_texto}
Dale al usuario una recomendación amigable y breve basada en esta información.
"""

    respuesta = generar_respuesta_con_gemini(prompt)
    return respuesta
