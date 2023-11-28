# librerias
# --------------------------------------------------------------------------------------
import pandas as pd
from tabulate import tabulate
from pytube import YouTube
import os
# --------------------------------------------------------------------------------------
# assets
from assets import lista_indice_menu
from assets import menu_inicial
from assets import lista_indice_feed
from assets import menu_feed
from assets import separador
# --------------------------------------------------------------------------------------
def main():
    setup() # Hacemos un setup inicial para asegurarnos que el dataframe este bien creado
    menu() # Empezamos con el menú o "interfaz de usuario"
# --------------------------------------------------------------------------------------
def menu():
    
    # Mensage de bienvenida
    os.system('cls')
    print(menu_inicial)
    
    # Chekeamos que el input del usuario sea valido antes de pasarlo
    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice_menu: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    # Redirección a la función requerida
    if entrada == lista_indice_menu[0]:
        feed()
    elif entrada == lista_indice_menu[1]:
        canales()
    elif entrada == lista_indice_menu[2]:
        categorias()
    elif entrada == lista_indice_menu[3]:
        borrar()
    elif entrada == lista_indice_menu[4]:
        exit()
# --------------------------------------------------------------------------------------
def setup():
    # Intentar cargar el DataFrame desde el archivo existente
    try:
        # df = pd.read_csv('canales.csv', index_col='Nombre del canal')
        df = pd.read_csv('canales.csv')
        df.index.names = ['Index']
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        df = pd.DataFrame(columns=['Nombre del canal', 'Categoría', 'Enlace del último video'])
        # df.set_index('Nombre del canal', inplace=True)
        # df.columns.names= ['group']
        df.to_csv('canales.csv', index=False) # Guardar el DataFrame al final del programa o cuando se realicen cambios
# --------------------------------------------------------------------------------------
def feed():
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    categorias_unicas = df['Categoría'].unique()
    os.system('cls')
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print(menu_feed)

    while True:
        entrada = input("Ingresa el indice para seleccionar una opción: ")
        if entrada not in lista_indice_feed: 
            print("Entrada no valida, vuelve a intentarlo")
            continue
        break
    
    # Redirección a la función requerida
    if entrada == lista_indice_feed[0]:
        pint("N/A")
    elif entrada == lista_indice_feed[1]:
        print("Lista de Categorías:")
        for i, categoria in enumerate(categorias_unicas):
            print(f"{i + 1}. {categoria}")
        seleccion = int(input("Seleccione el índice de la categoría: ")) - 1
        categoria_seleccionada = categorias_unicas[seleccion]
        print(tabulate(df.loc[df['Categoría'] == categoria_seleccionada], headers = 'keys', tablefmt = 'psql'))
        print(separador)
        
    elif entrada == lista_indice_feed[2]:
        print("N/A")
    elif entrada == lista_indice_feed[3]:
        menu()
# --------------------------------------------------------------------------------------
def canales():
    enlace_video_ejemplo = input("Pega el enlace de uno de los videos del canal que quieres agregar: " )
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    agregar_canal_desde_enlace(enlace_video_ejemplo, df)
# --------------------------------------------------------------------------------------
def categorias():
    print("N/A")
# --------------------------------------------------------------------------------------
def borrar():
    print("N/A")
# --------------------------------------------------------------------------------------
def agregar_canal_desde_enlace(enlace_video, df):
    df = pd.read_csv('canales.csv')
    df.index.names = ['Index']
    categorias_unicas = df['Categoría'].unique()
    try:
        # Crear un objeto YouTube utilizando el enlace del video
        yt_video = YouTube(enlace_video)

        # Obtener información del canal
        nombre_canal = yt_video.author

        print("Lista de Categorías:")
        for i, categoria in enumerate(categorias_unicas):
            print(f"{i + 1}. {categoria}")
        seleccion = int(input(f"Seleccione el índice de la categoría para el canal {nombre_canal}: ")) - 1
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
    df.to_csv('canales.csv', index=False)






# --------------------------------------------------------------------------------------
main()
# --------------------------------------------------------------------------------------
