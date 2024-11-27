import requests
from googletrans import Translator

# Tu clave de API de Spoonacular
API_KEY = "dfc8cfa0e8e54de1a601f3a040f2f165"

# URL del servicio de traducción
TRANSLATE_API_URL = "https://libretranslate.de/translate"

# Función para traducir texto (de español a inglés o de inglés a español)

# Función para traducir texto
def traducir_texto(texto, origen, destino):
    translator = Translator()
    traduccion = translator.translate(texto, src=origen, dest=destino)
    return traduccion.text


# Función para buscar el ID de la receta por su nombre en inglés
def buscar_receta_por_nombre(nombre_receta):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"query": nombre_receta, "apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        resultados = response.json().get("results", [])
        if resultados:
            return resultados[0]  # Retorna el primer resultado
        else:
            print("No se encontraron recetas con ese nombre.")
            return None
    else:
        print("Error al buscar recetas:", response.status_code)
        return None

# Función para obtener los detalles de una receta por ID en inglés
def obtener_detalles_receta(id_receta):
    url = f"https://api.spoonacular.com/recipes/{id_receta}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener detalles de la receta:", response.status_code)
        return None

# Función principal
def buscar_y_traducir_receta(nombre_receta_espanol):
    # Traducir el nombre de la receta del español al inglés
    nombre_receta_ingles = traducir_texto(nombre_receta_espanol, "es", "en")
    print(f"Buscando receta: {nombre_receta_ingles}")

    # Buscar la receta en inglés usando la API de Spoonacular
    receta_en_ingles = buscar_receta_por_nombre(nombre_receta_ingles)
    if receta_en_ingles:
        print(f"Receta encontrada: {receta_en_ingles['title']} (ID: {receta_en_ingles['id']})")

        # Obtener los detalles de la receta en inglés
        detalles = obtener_detalles_receta(receta_en_ingles['id'])
        if detalles:
            print("\nIngredientes necesarios:")
            for ingrediente in detalles['extendedIngredients']:
                # Traducir cada ingrediente al español
                ingrediente_espanol = traducir_texto(ingrediente['original'], "en", "es")
                print(f"- {ingrediente_espanol}")

            print("\nPasos de elaboración:")
            if 'analyzedInstructions' in detalles and detalles['analyzedInstructions']:
                pasos = detalles['analyzedInstructions'][0]['steps']
                for paso in pasos:
                    # Traducir cada paso al español
                    paso_espanol = traducir_texto(paso['step'], "en", "es")
                    print(f"{paso['number']}. {paso_espanol}")
            else:
                print("No hay pasos disponibles para esta receta.")

# Función para ejecutar el flujo completo
if __name__ == "__main__":
    nombre_receta = input("Ingrese el nombre de la receta que desea buscar: ")
    buscar_y_traducir_receta(nombre_receta)
    print("Hasta la próxima chef :D")