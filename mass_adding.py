import pandas as pd
from pytube import YouTube
import random

# Función para generar datos aleatorios
def asignar_categorias_aleatorias(num_canales, categorias_disponibles):
    categorias_asignadas = random.choices(categorias_disponibles, k=num_canales)
    return categorias_asignadas

# Función para agregar canales desde una lista de enlaces
def agregar_canales_desde_lista_interactiva():
    try:
        # Leer las categorías disponibles
        df_categorias = pd.read_csv('categorias.csv')
        categorias_disponibles = df_categorias['Categoría'].tolist()

        # Preguntar al usuario cuántos canales va a ingresar
        num_canales = int(input("¿Cuántos canales vas a ingresar?: "))

        # Preguntar al usuario por los enlaces de los canales
        enlaces_canales = []
        for i in range(num_canales):
            enlace = input(f"Ingrese el enlace del canal {i+1}: ")
            enlaces_canales.append(enlace)

        # Generar datos para los nuevos canales
        nombres_canales = []
        links_canales = []
        for enlace in enlaces_canales:
            try:
                yt_video = YouTube(enlace)
                nombre_canal = yt_video.author
                link_canal = f"https://www.youtube.com/{nombre_canal.lower()}"
                nombres_canales.append(nombre_canal)
                links_canales.append(link_canal)
            except Exception as e:
                print(f"Error al obtener información del canal: {str(e)}")
                nombres_canales.append("Nombre_Desconocido")
                links_canales.append("Link_Desconocido")

        categorias_asignadas = asignar_categorias_aleatorias(num_canales, categorias_disponibles)

        # Crear DataFrame con los datos generados
        nuevos_canales = pd.DataFrame({'Nombre del canal': nombres_canales,
                                       'Categoría': categorias_asignadas,
                                       'Link canal': links_canales})
        nuevos_canales.index.names = ['Index']

        # Leer el DataFrame actual
        df_canales = pd.read_csv('canales.csv')
        df_canales.index.names = ['Index']

        # Concatenar el DataFrame actual con los nuevos canales
        df_actualizado = pd.concat([df_canales, nuevos_canales], ignore_index=True)

        # Guardar DataFrame actualizado en el archivo canales.csv
        df_actualizado.to_csv('canales.csv', index=False)

        print(f'Se han agregado {num_canales} canales al archivo canales.csv.')
    except Exception as e:
        print(f'Error al agregar canales: {str(e)}')

# Ejemplo de uso
agregar_canales_desde_lista_interactiva()
