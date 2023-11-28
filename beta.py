import pandas as pd
from pytube import YouTube
df = pd.read_csv('canales.csv')
df.index.names = ['Index']
categorias_unicas = df['Categoría'].unique()
def agregar_canal_desde_enlace(enlace_video, df):
    try:
        # Crear un objeto YouTube utilizando el enlace del video
        yt_video = YouTube(enlace_video)

        # Obtener información del canal
        nombre_canal = yt_video.author

        print("Lista de Categorías:")
        for i, categoria in enumerate(categorias_unicas):
            print(f"{i + 1}. {categoria}")
        seleccion = int(input("Seleccione el índice de la categoría para el canal {}: ")) - 1
        categoria = categorias_unicas[seleccion]

        # Obtener la identificación del video del último video
        ultimo_video_id = yt_video.video_id

        # Construir el enlace del último video
        ultimo_video_enlace = f'https://www.youtube.com/watch?v={ultimo_video_id}'

        # Verificar si el canal ya existe en el DataFrame
        if nombre_canal in df['Nombre del canal'].values:
            print(f"El canal '{nombre_canal}' ya está en la lista.")
            return

        # Concatenar el DataFrame temporal con el DataFrame principal
        df.loc[len(df.index)] = [nombre_canal,categoria,ultimo_video_enlace]

        print(f"Canal '{nombre_canal}' agregado con éxito.")

    except Exception as e:
        print(f"Error al agregar el canal: {str(e)}")

# Ejemplo de uso
df = pd.read_csv('canales.csv')  # Cargar DataFrame existente

enlace_video_ejemplo = 'https://www.youtube.com/watch?v=W9BmbWUtrjE'
agregar_canal_desde_enlace(enlace_video_ejemplo, df)

# Guardar el DataFrame actualizado
df.to_csv('canales.csv', index=False)
