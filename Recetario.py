import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import requests
from io import BytesIO
from googletrans import Translator

# Tu clave de API de Spoonacular
API_KEY = "dfc8cfa0e8e54de1a601f3a040f2f165"

# Función para traducir texto
def traducir_texto(texto, origen, destino):
    translator = Translator()
    try:
        traduccion = translator.translate(texto, src=origen, dest=destino)
        return traduccion.text
    except Exception as e:
        messagebox.showerror("Error de Traducción", f"No se pudo traducir el texto. Error: {e}")
        return None

# Función para obtener recetas sugeridas
def obtener_receta_aleatoria():
    url = "https://api.spoonacular.com/recipes/random"
    params = {"apiKey": API_KEY, "number": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        resultado = response.json().get("recipes", [])
        if resultado:
            return resultado[0]  # Retorna la receta
        else:
            messagebox.showinfo("Sin Resultados", "No se encontró ninguna receta sugerida.")
            return None
    else:
        messagebox.showerror("Error API", f"Error al obtener recetas aleatorias: {response.status_code}")
        return None

# Función para mostrar receta sugerida
def mostrar_receta_sugerida():
    receta = obtener_receta_aleatoria()
    if receta:
        # Traducir el título de la receta
        titulo_espanol = traducir_texto(receta['title'], "en", "es")
        etiqueta_receta_nombre.config(text=f"Receta sugerida: {titulo_espanol}")
        
        # Mostrar la imagen de la receta
        if 'image' in receta:
            try:
                response = requests.get(receta['image'])
                img_data = BytesIO(response.content)
                img = Image.open(img_data).resize((200, 200))
                img_tk = ImageTk.PhotoImage(img)
                etiqueta_receta_imagen.configure(image=img_tk)
                etiqueta_receta_imagen.image = img_tk
            except Exception as e:
                messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen. Error: {e}")

def ocultar_receta_sugerida():
    etiqueta_receta_nombre.pack_forget()  # Oculta el nombre
    etiqueta_receta_imagen.pack_forget()  # Oculta la imagen

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
            messagebox.showinfo("Sin Resultados", "No se encontraron recetas con ese nombre.")
            return None
    else:
        messagebox.showerror("Error API", f"Error al buscar recetas: {response.status_code}")
        return None

# Función para obtener los detalles de una receta por ID en inglés
def obtener_detalles_receta(id_receta):
    url = f"https://api.spoonacular.com/recipes/{id_receta}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error API", f"Error al obtener detalles de la receta: {response.status_code}")
        return None


# Función para buscar y traducir receta
def buscar_y_traducir_receta():
    nombre_receta_espanol = entrada_nombre.get()
    if not nombre_receta_espanol.strip():
        messagebox.showwarning("Entrada Vacía", "Por favor, ingresa un nombre de receta.")
        return

    # Traducir el nombre de la receta
    nombre_receta_ingles = traducir_texto(nombre_receta_espanol, "es", "en")
    if not nombre_receta_ingles:
        return

    # Buscar receta en Spoonacular
    receta_en_ingles = buscar_receta_por_nombre(nombre_receta_ingles)
    if receta_en_ingles:
        detalles = obtener_detalles_receta(receta_en_ingles['id'])
        if detalles:
            mostrar_resultados(detalles)


# Función para mostrar resultados en la interfaz
def mostrar_resultados(detalles):
    ocultar_receta_sugerida()
    resultado_texto.delete(1.0, tk.END)  # Limpiar resultados previos
    resultado_texto.insert(tk.END, f"Receta: {detalles['title']}\n\n")
    
    # Ingredientes
    resultado_texto.insert(tk.END, "Ingredientes necesarios:\n")
    for ingrediente in detalles['extendedIngredients']:
        ingrediente_espanol = traducir_texto(ingrediente['original'], "en", "es")
        resultado_texto.insert(tk.END, f"- {ingrediente_espanol}\n")
    
    # Pasos
    resultado_texto.insert(tk.END, "\nPasos de elaboración:\n")
    if 'analyzedInstructions' in detalles and detalles['analyzedInstructions']:
        pasos = detalles['analyzedInstructions'][0]['steps']
        for paso in pasos:
            paso_espanol = traducir_texto(paso['step'], "en", "es")
            resultado_texto.insert(tk.END, f"{paso['number']}. {paso_espanol}\n")
    else:
        resultado_texto.insert(tk.END, "No hay pasos disponibles para esta receta.\n")

    # Cargar y mostrar la imagen de la receta
    if 'image' in detalles:
        try:
            response = requests.get(detalles['image'])
            img_data = BytesIO(response.content)
            img = Image.open(img_data).resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            etiqueta_imagen.configure(image=img_tk)
            etiqueta_imagen.image = img_tk
        except Exception as e:
            messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen. Error: {e}")

# Función para limpiar resultados
def limpiar_resultados():
    entrada_nombre.delete(0, tk.END)  # Borrar entrada de texto
    resultado_texto.delete(1.0, tk.END)  # Limpiar resultados previos
    etiqueta_imagen.configure(image="")  # Eliminar imagen
    etiqueta_imagen.image = None

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Buscador de Recetas")
ventana.geometry("700x750")

# Etiquetas para mostrar la receta sugerida
etiqueta_receta_nombre = tk.Label(ventana, text="Receta sugerida: Cargando...", font=("Arial", 12, "bold"))
etiqueta_receta_nombre.pack(pady=10)

etiqueta_receta_imagen = tk.Label(ventana)
etiqueta_receta_imagen.pack(pady=10)
# Etiqueta para mostrar la imagen de la receta
etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.pack(pady=10)

# Cargar una receta aleatoria al iniciar la aplicación
mostrar_receta_sugerida()

# Etiqueta y entrada para el nombre de la receta
tk.Label(ventana, text="Nombre de la receta en español:").pack(pady=10)
entrada_nombre = tk.Entry(ventana, width=50)
entrada_nombre.pack(pady=5)

# Botón para buscar receta
tk.Button(ventana, text="Buscar Receta", command=buscar_y_traducir_receta).pack(pady=10)
# Botón para limpiar resultados
tk.Button(ventana, text="Borrar Resultados", command=limpiar_resultados).pack(pady=10)
# Área de texto para mostrar los resultados
resultado_texto = scrolledtext.ScrolledText(ventana, width=70, height=15)
resultado_texto.pack(pady=10)

# Mensajes adicionales
tk.Label(ventana, text="Recuerde ingresar el nombre de la receta con la ortografía correcta para mejores resultados.", fg="blue").pack(pady=5)
tk.Label(ventana, text="No nos hacemos responsables si los resultados no coinciden exactamente con lo solicitado.", fg="red").pack(pady=5)

# Iniciar la aplicación
ventana.mainloop()