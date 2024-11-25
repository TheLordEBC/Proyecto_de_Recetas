import requests
#Implementar traductor

# Tu clave de API de Spoonacular
API_KEY = "dfc8cfa0e8e54de1a601f3a040f2f165"


# Función para buscar el ID de la receta por su nombre
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


# Función para obtener los detalles de una receta por ID
def obtener_detalles_receta(id_receta):
    url = f"https://api.spoonacular.com/recipes/{id_receta}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener detalles de la receta:", response.status_code)
        return None

if __name__ == "__main__":
    #print("Bienvenido, por favor seleccione una opción del siguiente menú")
    # Buscar por nombre
    nombre = input("Ingrese el nombre de la receta que desea buscar: ")
    recetas_por_nombre = buscar_receta_por_nombre(nombre)
    if recetas_por_nombre:
        print(f"Receta encontrada: {recetas_por_nombre['title']} (ID: {recetas_por_nombre['id']})")

        # Obtener detalles de la receta
        detalles = obtener_detalles_receta(recetas_por_nombre['id'])
        if detalles:
            print("\nIngredientes necesarios:")
            for ingrediente in detalles['extendedIngredients']:
                print(f"- {ingrediente['original']}")

            print("\nPasos de elaboración:")
            if 'analyzedInstructions' in detalles and detalles['analyzedInstructions']:
                pasos = detalles['analyzedInstructions'][0]['steps']
                for paso in pasos:
                    print(f"{paso['number']}. {paso['step']}")
            else:
                print("No hay pasos disponibles para esta receta.")
    print("Hasta la próxima chef :D")